"""Прогон sales.strategic.* v1 по проверочному набору e-014-eval.

  cd …/e-014-eval
  python3 run_strategic_eval.py --model just-ai/openai-proxy/gpt-4o-mini --tag gpt4omini --runs 3
  python3 run_strategic_eval.py --model just-ai/open-router/deepseek/deepseek-v3.2 --tag deepseek
  python3 run_strategic_eval.py --model just-ai/open-router/qwen/qwen3.5-flash-02-23 --tag qwen --reasoning-off

Результаты: results/run-<tag>.json, results/summary-<tag>.md, results/texts-<tag>.md
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import statistics
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "e-010-brief-eval"))
from caila import chat, load_key  # noqa: E402

PROMPTS = ROOT / "e-014-prompts"
SCHEMAS = ROOT / "e-014-schemas"

CLIENT_ZERO_RE = re.compile(
    r"клиентов\s*:\s*0|клиентов\s+0|нет\s+клиент|клиентов\s+пока\s+нет|ни\s+одного\s+клиент",
    re.I,
)
# Обещание результата, а не пересказ анкеты («база из 10–30 клиентов», «цель — 4 клиента»).
FAIL_TEXT = re.compile(
    r"гарантир"
    r"|точно (придут|получите|будет)"
    r"|обязательно (придут|запишутся|купят)"
    r"|(придут|получите|наберёте|наберете|появятся)\s+(ещё\s+|еще\s+)?\d+\s+(нов\w+\s+)?(клиент|заяв)"
    r"|цел\w*[^.]{0,40}(реалистичн|достижим)",
    re.I,
)
JARGON = re.compile(r"bottleneck|конверси|оффер|воронк|\bлид(ы|ов|ам|ами)?\b|\bCTA\b", re.I)
PROMPT_EXAMPLE_QUESTIONS = {
    "Писали ли вы бывшим клиентам за последние месяцы?",
}
BASE_WITH = {"10_30", "gt30"}
BASE_WITHOUT = {"none", "lt10"}


def load_schema(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def diagnose_schema(base: dict, inp: dict) -> dict:
    """Схема вопроса под конкретный запрос: profile_field только из askable_fields, options — коды поля."""
    schema = copy.deepcopy(base)
    item = schema["json_schema"]["schema"]["properties"]["questions"]["items"]
    props = item["properties"]
    allowed = inp.get("profile_allowed") or {}

    def variant(field, free_text: bool, options: dict) -> dict:
        v = copy.deepcopy(item)
        v["properties"]["profile_field"] = {"type": "null"} if field is None else {"type": "string", "enum": [field]}
        v["properties"]["allow_free_text"] = {"type": "boolean", "enum": [free_text]}
        v["properties"]["options"] = options
        return v

    variants = [variant(None, True, props["options"])]
    for field in inp.get("askable_fields") or []:
        codes = allowed.get(field) or []
        if len(codes) >= 2:
            opts = {"type": "array", "minItems": 2, "maxItems": 5, "items": {"type": "string", "enum": codes}}
            variants.append(variant(field, False, opts))
    schema["json_schema"]["schema"]["properties"]["questions"]["items"] = {"anyOf": variants}
    return schema


def all_strings(obj) -> list[str]:
    out: list[str] = []
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            out.extend(all_strings(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(all_strings(v))
    return out


def parse_json(content: str) -> tuple[dict | None, str | None]:
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return None, f"invalid_json:{e.msg}"
    if not isinstance(data, dict):
        return None, "not_object"
    return data, None


def check_no_client_zero(data: dict, exp: dict) -> list[str]:
    if not exp.get("no_client_zero_phrase"):
        return []
    misses = []
    for s in all_strings(data):
        if CLIENT_ZERO_RE.search(s):
            misses.append("client_zero_phrase")
            break
    return misses


NEGATION = re.compile(r"(\bбез|\bне|\bни|\bникаких|\bизбега\w*|\bвместо|\bисключ\w*)\s+(\w+\s+){0,4}$", re.I)


def negated(text: str, start: int) -> bool:
    return bool(NEGATION.search(text[max(0, start - 40):start]))


def check_must_not_contain(data: dict, exp: dict) -> list[str]:
    misses = []
    blob = " ".join(all_strings(data)).lower()
    for sub in exp.get("must_not_contain", []):
        hits = [m.start() for m in re.finditer(re.escape(sub.lower()), blob)]
        if any(not negated(blob, i) for i in hits):
            misses.append(f"contains_{sub[:20]}")
    return misses


def expect_intake(data: dict, exp: dict, inp: dict) -> list[str]:
    misses = []
    if exp.get("old_base_size") and data.get("old_base_size") != exp["old_base_size"]:
        misses.append(f"old_base_{data.get('old_base_size')}")
    if exp.get("hours_per_week") and data.get("hours_per_week") != exp["hours_per_week"]:
        misses.append(f"hours_{data.get('hours_per_week')}")
    if exp.get("urgency") and data.get("urgency") != exp["urgency"]:
        misses.append(f"urgency_{data.get('urgency')}")
    if exp.get("offer") and data.get("offer") != exp["offer"]:
        misses.append(f"offer_{data.get('offer')}")
    if exp.get("goal_clients_per_month") and data.get("goal_clients_per_month") != exp["goal_clients_per_month"]:
        misses.append(f"goal_{data.get('goal_clients_per_month')}")
    if "services_any" in exp:
        if data.get("services") not in exp["services_any"]:
            misses.append(f"services_{data.get('services')}")
    if ch := exp.get("channels_include"):
        got = set(data.get("channels") or [])
        if not set(ch) <= got:
            misses.append(f"channels_missing_{ch}")
    if ch_all := exp.get("channels_include_all"):
        got = set(data.get("channels") or [])
        if set(ch_all) - got:
            misses.append("channels_not_all")
    if exp.get("channels_min") and len(data.get("channels") or []) < exp["channels_min"]:
        misses.append("channels_too_few")
    unclear = set(data.get("unclear") or [])
    for f in exp.get("must_unclear", []):
        if f not in unclear:
            misses.append(f"unclear_missing_{f}")
    if exp.get("unclear_min") and len(unclear) < exp["unclear_min"]:
        misses.append("unclear_too_few")
    for f in exp.get("must_not_unclear", []):
        if f in unclear:
            misses.append(f"unclear_unwanted_{f}")
    if exp.get("must_unclear_any"):
        if not unclear & set(exp["must_unclear_any"]):
            misses.append("unclear_none_of_expected")
    if exp.get("specialization_not_null") and not (data.get("specialization") or "").strip():
        misses.append("specialization_empty")
    if exp.get("old_base_size_any") and data.get("old_base_size") not in exp["old_base_size_any"]:
        misses.append(f"old_base_{data.get('old_base_size')}")
    if exp.get("hours_per_week_any") and data.get("hours_per_week") not in exp["hours_per_week_any"]:
        misses.append(f"hours_{data.get('hours_per_week')}")
    misses.extend(check_must_not_contain(data, exp))
    return misses


def diagnose_consistency(data: dict, inp: dict) -> list[str]:
    """Проверки кода D-серии, не зависящие от expect кейса."""
    misses = []
    codes = {b.get("code") for b in data.get("bottlenecks") or [] if isinstance(b, dict)}
    base = (inp.get("profile") or {}).get("old_base_size")
    if "no_base" in codes and base in BASE_WITH:
        misses.append("bottleneck_no_base_vs_profile")
    if "base_untouched" in codes and base in BASE_WITHOUT:
        misses.append("bottleneck_untouched_vs_profile")
    if {"no_base", "base_untouched"} <= codes:
        misses.append("bottleneck_base_contradiction")
    if inp.get("final_round") and data.get("questions"):
        misses.append("final_round_questions")
    allowed = inp.get("profile_allowed") or {}
    flags = set(inp.get("mismatch_flags") or [])
    questions = data.get("questions") or []
    if len(questions) > 3:
        misses.append("questions_gt_3")
    keys = [q.get("key") for q in questions]
    if len(keys) != len(set(keys)):
        misses.append("questions_key_dup")
    for q in questions:
        opts = q.get("options") or []
        if not 2 <= len(opts) <= 5:
            misses.append(f"question_options_count_{q.get('key')}")
        field = q.get("profile_field")
        if field:
            filled = (inp.get("profile") or {}).get(field) not in (None, [], "")
            if filled and field not in flags:
                misses.append(f"question_on_filled_field_{field}")
            if q.get("allow_free_text"):
                misses.append(f"question_free_text_with_field_{field}")
            if not set(opts) <= set(allowed.get(field) or []):
                misses.append(f"question_options_not_allowed_{field}")
        elif not q.get("allow_free_text"):
            misses.append(f"question_no_free_text_{q.get('key')}")
        if inp.get("mode") == "weekly" and (q.get("text") or "").strip() in PROMPT_EXAMPLE_QUESTIONS:
            misses.append("question_copied_from_prompt")
    for field in ("strengths", "opportunities", "assumptions"):
        if any(re.match(r"\s*тренер\b", s, re.I) for s in data.get(field) or []):
            misses.append(f"third_person_{field}")
    for p in data.get("profile_change_proposals") or []:
        field = p.get("field")
        if field not in flags:
            misses.append(f"proposal_without_flag_{field}")
        elif p.get("proposed_value") not in (allowed.get(field) or []):
            misses.append(f"proposal_value_{p.get('proposed_value')}")
    if inp.get("mode") == "weekly" and (inp.get("facts") or inp.get("week_plan_performance")):
        if not data.get("observations"):
            misses.append("weekly_no_observations")
    return misses


def expect_diagnose(data: dict, exp: dict, inp: dict) -> list[str]:
    misses = diagnose_consistency(data, inp)
    codes = [b.get("code") for b in data.get("bottlenecks") or [] if isinstance(b, dict)]
    if exp.get("bottleneck_any") and not set(exp["bottleneck_any"]) & set(codes):
        misses.append(f"bottleneck_not_in_{exp['bottleneck_any']}")
    if exp.get("data_quality_any") and data.get("data_quality") not in exp["data_quality_any"]:
        misses.append(f"data_quality_{data.get('data_quality')}")
    q = data.get("questions") or []
    if exp.get("questions_forbidden") and q:
        misses.append("questions_not_empty")
    if "questions_max" in exp and len(q) > exp["questions_max"]:
        misses.append(f"questions_gt_{exp['questions_max']}")
    if exp.get("question_fields_any"):
        asked = {x.get("profile_field") for x in q}
        if not asked & set(exp["question_fields_any"]):
            misses.append("question_field_missing")
    if exp.get("profile_change_empty") and (data.get("profile_change_proposals") or []):
        misses.append("profile_change_not_empty")
    if exp.get("profile_change_fields_any"):
        fields = [p.get("field") for p in data.get("profile_change_proposals") or []]
        if not set(fields) & set(exp["profile_change_fields_any"]):
            misses.append("profile_change_field_missing")
    if exp.get("observations_topics_any"):
        topics = [o.get("topic") for o in data.get("observations") or []]
        if not set(topics) & set(exp["observations_topics_any"]):
            misses.append("observation_topic_missing")
    misses.extend(check_no_client_zero(data, exp))
    misses.extend(check_must_not_contain(data, exp))
    misses.extend(check_promise(data))
    return sorted(set(misses))


def check_promise(data: dict) -> list[str]:
    misses = []
    for s in all_strings(data):
        if any(not negated(s, m.start()) for m in FAIL_TEXT.finditer(s)):
            misses.append("fail_text_promise")
        if JARGON.search(s):
            misses.append("jargon")
    return sorted(set(misses))


def expect_propose(data: dict, exp: dict, inp: dict) -> list[str]:
    misses = []
    strategies = data.get("strategies") or []
    if exp.get("strategies_min") and len(strategies) < exp["strategies_min"]:
        misses.append(f"strategies_lt_{exp['strategies_min']}")
    if exp.get("strategies_max") and len(strategies) > exp["strategies_max"]:
        misses.append(f"strategies_gt_{exp['strategies_max']}")
    rec = [s for s in strategies if s.get("is_recommended")]
    if len(rec) != 1:
        misses.append(f"recommended_count_{len(rec)}")
    if exp.get("recommended_cards_any"):
        keys = set()
        for s in strategies:
            if s.get("is_recommended"):
                keys.update(s.get("knowledge_card_keys") or [])
        if not keys & set(exp["recommended_cards_any"]):
            misses.append("recommended_card_missing")
    for bad in exp.get("forbidden_card_keys", []):
        for s in strategies:
            if bad in (s.get("knowledge_card_keys") or []):
                misses.append(f"forbidden_card_{bad}")
    known = {c["key"] for c in inp.get("knowledge_cards") or []}
    for s in strategies:
        for k in s.get("knowledge_card_keys") or []:
            if k not in known:
                misses.append(f"unknown_card_{k}")
    misses.extend(check_must_not_contain(data, exp))
    misses.extend(check_promise(data))
    return misses


def week_minutes(items: list[dict]) -> int:
    total = 0
    for it in items:
        m = it.get("minutes") or 0
        freq = it.get("frequency") or {}
        kind = freq.get("kind")
        if kind == "once":
            mult = 1
        elif kind == "daily":
            mult = 7
        elif kind == "times_per_week":
            mult = freq.get("times_per_week") or 1
        else:
            mult = 1
        total += m * mult
    return total


def expect_decompose(data: dict, exp: dict, inp: dict) -> list[str]:
    misses = []
    items = data.get("items") or []
    if "milestones_max" in exp and len(data.get("milestones") or []) > exp["milestones_max"]:
        misses.append("milestones_too_many")
    if exp.get("items_min") and len(items) < exp["items_min"]:
        misses.append("items_too_few")
    if exp.get("items_max") and len(items) > exp["items_max"]:
        misses.append("items_too_many")
    if exp.get("milestones_min") is not None:
        if len(data.get("milestones") or []) < exp["milestones_min"]:
            misses.append("milestones_too_few")
    if cap := exp.get("minutes_cap"):
        if week_minutes(items) > cap:
            misses.append(f"minutes_over_{week_minutes(items)}")
    allowed = set(exp.get("types_only_from") or [])
    if allowed:
        for it in items:
            if it.get("type") not in allowed:
                misses.append(f"type_bad_{it.get('type')}")
    misses.extend(check_must_not_contain(data, exp))
    misses.extend(check_promise(data))
    return misses


def expect_review(data: dict, exp: dict, inp: dict) -> list[str]:
    misses = []
    if exp.get("status_any") and data.get("status") not in exp["status_any"]:
        misses.append(f"status_{data.get('status')}")
    if exp.get("forbid_status") and data.get("status") in exp["forbid_status"]:
        misses.append(f"forbidden_status_{data.get('status')}")
    if exp.get("recommendation_any") and data.get("recommendation") not in exp["recommendation_any"]:
        misses.append(f"rec_{data.get('recommendation')}")
    if exp.get("recommendation_not") and data.get("recommendation") in exp["recommendation_not"]:
        misses.append(f"rec_forbidden_{data.get('recommendation')}")
    misses.extend(check_no_client_zero(data, exp))
    misses.extend(check_promise(data))
    clients_new = (inp.get("facts") or {}).get("clients_new") or 0
    if clients_new > 0 and not any("клиент" in s.lower() for s in data.get("what_works") or []):
        misses.append("clients_not_in_what_works")
    return misses


def call_model(
    model: str,
    system: str,
    user: dict,
    schema: dict,
    max_tokens: int,
    key: str,
    extra_body: dict | None = None,
    use_schema: bool = True,
) -> dict:
    body: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
        ],
        "temperature": 0.2,
        "max_tokens": max_tokens,
    }
    if use_schema:
        body["response_format"] = schema
    if extra_body:
        body.update(extra_body)
    return chat(body, timeout=90, key=key)


def run_one(
    case_id: str,
    agent: str,
    inp: dict,
    exp: dict,
    model: str,
    key: str,
    extra_body: dict | None,
    use_schema: bool = True,
    run_no: int = 1,
) -> dict:
    cfg = {
        "intake": ("strategic.intake_extract.v1.system.txt", "strategic.intake_extract.v1.schema.json", 900, expect_intake),
        "diagnose": ("strategic.diagnose.v1.system.txt", "strategic.diagnose.v1.schema.json", 1400, expect_diagnose),
        "propose": ("strategic.propose.v1.system.txt", "strategic.propose.v1.schema.json", 2200, expect_propose),
        "decompose": ("strategic.decompose.v1.system.txt", "strategic.decompose.v1.schema.json", 2200, expect_decompose),
        "review": ("strategic.review.v1.system.txt", "strategic.review.v1.schema.json", 900, expect_review),
    }[agent]
    system = (PROMPTS / cfg[0]).read_text(encoding="utf-8")
    schema = load_schema(cfg[1])
    if agent == "diagnose" and "askable_fields" in inp:
        schema = diagnose_schema(schema, inp)
    r = call_model(model, system, inp, schema, cfg[2], key, extra_body, use_schema)
    out = {
        "case": case_id,
        "agent": agent,
        "run": run_no,
        "ok_http": r.get("ok"),
        "error": r.get("error"),
        "latency_ms": r.get("latency_ms"),
        "tokens_in": r.get("tokens_in"),
        "tokens_out": r.get("tokens_out"),
        "cost_rub": r.get("cost_rub"),
        "content": r.get("content"),
    }
    if not r.get("ok"):
        out.update(valid=False, expect_ok=False, expect_misses=[r.get("error") or "http"])
        return out
    data, perr = parse_json(r.get("content") or "")
    if data is None:
        out.update(valid=False, expect_ok=False, expect_misses=[perr])
        return out
    misses = cfg[3](data, exp, inp)
    out.update(valid=True, parsed=data, expect_misses=misses, expect_ok=not misses)
    return out


def build_jobs() -> list[tuple[str, str, dict, dict]]:
    stories = json.loads((HERE / "stories-v1.json").read_text(encoding="utf-8"))
    trainers = json.loads((HERE / "trainers-v1.json").read_text(encoding="utf-8"))
    jobs: list[tuple[str, str, dict, dict]] = []
    for c in stories:
        jobs.append((c["id"], "intake", c["input"], c.get("expect") or {}))
    for c in trainers:
        for agent in ("diagnose", "propose", "decompose", "review"):
            block = c.get(agent)
            if block:
                jobs.append((c["id"], agent, block["input"], block.get("expect") or {}))
    return jobs


def summarize(results: list[dict]) -> dict:
    by_agent: dict[str, list] = {}
    for r in results:
        by_agent.setdefault(r["agent"], []).append(r)
    summary = {"total": len(results), "agents": {}}
    for agent, rows in sorted(by_agent.items()):
        valid = sum(1 for x in rows if x.get("valid"))
        expect_ok = sum(1 for x in rows if x.get("expect_ok"))
        lat = [x["latency_ms"] for x in rows if x.get("latency_ms")]
        cost = sum(x.get("cost_rub") or 0 for x in rows)
        summary["agents"][agent] = {
            "n": len(rows),
            "valid_pct": round(100 * valid / len(rows), 1) if rows else 0,
            "expect_pct": round(100 * expect_ok / len(rows), 1) if rows else 0,
            "latency_ms_avg": int(statistics.mean(lat)) if lat else None,
            "cost_rub_sum": round(cost, 4),
        }
    summary["cost_rub_total"] = round(sum(r.get("cost_rub") or 0 for r in results), 4)
    summary["expect_pct_all"] = round(
        100 * sum(1 for r in results if r.get("expect_ok")) / len(results), 1
    ) if results else 0
    return summary


def write_md(tag: str, results: list[dict], summary: dict, model: str) -> None:
    lines = [
        f"# E-014 strategic eval · {tag}",
        "",
        f"Модель: `{model}`",
        "",
        f"- Всего вызовов: {summary['total']}",
        f"- expect OK: **{summary['expect_pct_all']}%**",
        f"- Сумма ₽: **{summary['cost_rub_total']}**",
        "",
        "| Агент | n | valid % | expect % | avg ms | ₽ |",
        "|-------|---|---------|----------|--------|---|",
    ]
    for agent, s in summary["agents"].items():
        lines.append(
            f"| {agent} | {s['n']} | {s['valid_pct']} | {s['expect_pct']} | {s['latency_ms_avg']} | {s['cost_rub_sum']} |"
        )
    runs = sorted({r.get("run", 1) for r in results})
    if len(runs) > 1:
        lines += ["", "## По прогонам", "", "| Прогон | expect % |", "|--------|----------|"]
        for n in runs:
            rows = [r for r in results if r.get("run", 1) == n]
            pct = round(100 * sum(1 for r in rows if r.get("expect_ok")) / len(rows), 1)
            lines.append(f"| {n} | {pct} |")
    lines.append("")
    lines.append("## Красные кейсы")
    for r in results:
        if not r.get("expect_ok"):
            lines.append(
                f"- run {r.get('run', 1)} · `{r['case']}` / {r['agent']}: {r.get('expect_misses') or r.get('error')}"
            )
    (HERE / "results" / f"summary-{tag}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_texts(tag: str, results: list[dict]) -> None:
    """Тексты для тренера из первого прогона — для ручного просмотра тона."""
    fields = {
        "diagnose": ["strengths", "bottlenecks", "opportunities", "assumptions", "questions", "observations"],
        "propose": ["strategies"],
        "decompose": ["plan_rationale", "items"],
        "review": ["status", "recommendation", "what_works", "what_does_not", "suggestions", "explanation"],
    }
    lines = [f"# Тексты для ручного просмотра · {tag}", ""]
    for r in results:
        if r.get("run", 1) != 1 or r["agent"] not in fields or not r.get("parsed"):
            continue
        lines.append(f"## {r['case']} · {r['agent']}")
        lines.append("")
        lines.append("```json")
        part = {k: r["parsed"].get(k) for k in fields[r["agent"]]}
        lines.append(json.dumps(part, ensure_ascii=False, indent=1))
        lines.append("```")
        lines.append("")
    (HERE / "results" / f"texts-{tag}.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--agents", default="", help="через запятую: intake,diagnose,propose,decompose,review")
    ap.add_argument("--reasoning-off", action="store_true", help='добавить reasoning: {"enabled": false} (qwen)')
    ap.add_argument("--no-schema", action="store_true", help="не передавать response_format")
    args = ap.parse_args()

    key = load_key()
    only = {a for a in args.agents.split(",") if a}
    jobs = [j for j in build_jobs() if not only or j[1] in only]
    extra = {"reasoning": {"enabled": False}} if args.reasoning_off else None
    tasks = [(n, j) for n in range(1, args.runs + 1) for j in jobs]

    def work(t):
        n, (cid, agent, inp, exp) = t
        return run_one(cid, agent, inp, exp, args.model, key, extra, not args.no_schema, n)

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for i, r in enumerate(pool.map(work, tasks), 1):
            results.append(r)
            print(f"[{i}/{len(tasks)}] run{r['run']} {r['case']}/{r['agent']} valid={r.get('valid')} expect={r.get('expect_ok')}")

    summary = summarize(results)
    summary["runs"] = args.runs
    summary["schema"] = not args.no_schema
    summary["reasoning_off"] = args.reasoning_off
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    payload = {"model": args.model, "tag": args.tag, "summary": summary, "results": results}
    (out_dir / f"run-{args.tag}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    write_md(args.tag, results, summary, args.model)
    write_texts(args.tag, results)
    print("summary:", json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
