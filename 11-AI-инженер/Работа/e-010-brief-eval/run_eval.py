"""Прогон leadgen.morning_brief по проверочному набору.

Запуск:
  python3 run_eval.py --model just-ai/openai-proxy/gpt-4o-mini --runs 3 --tag gpt4omini
  python3 run_eval.py --model just-ai/open-router/deepseek/deepseek-v3.2 --runs 1 --tag deepseek

Результаты: results/run-<tag>.json (сырые ответы + проверки) и results/review-<tag>.md (why с демо-именами).
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from caila import chat, load_key

HERE = Path(__file__).resolve().parent
PROMPT_VERSION = "leadgen.morning_brief.v1"
SYSTEM = (HERE / "prompt" / f"{PROMPT_VERSION}.system.txt").read_text(encoding="utf-8")
SCHEMA = json.loads((HERE / "prompt" / f"{PROMPT_VERSION}.schema.json").read_text(encoding="utf-8"))

WHY_MAX = 160          # жёсткий лимит валидации (ADR-011 §3)
WHY_TARGET = 120       # цель из промпта; превышение — предупреждение
MACRO_RE = re.compile(r"\{\{name_\d+\}\}")

# --- Продуктовая валидация (ADR-011 §3): нарушение → бриф по правилам ---


def validate(content: str, inp: dict) -> tuple[list[dict] | None, list[str]]:
    errors: list[str] = []
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return None, ["invalid_json"]
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return None, ["no_items"]

    cand_ids = {c["task_id"] for c in inp["candidates"]}
    refs = {p["ref"] for p in inp["people"]}
    n_max = min(3, len(cand_ids))

    if not 1 <= len(items) <= n_max:
        errors.append(f"items_count_{len(items)}_not_in_1..{n_max}")

    seen_ids, seen_orders = set(), set()
    for it in items:
        if not isinstance(it, dict):
            errors.append("item_not_object")
            continue
        tid, order, why = it.get("task_id"), it.get("order"), it.get("why")
        if not isinstance(tid, int) or tid not in cand_ids:
            errors.append(f"task_id_not_candidate_{tid}")
        if tid in seen_ids:
            errors.append(f"task_id_duplicate_{tid}")
        seen_ids.add(tid)
        if not isinstance(order, int) or order < 1 or order in seen_orders:
            errors.append(f"order_bad_{order}")
        seen_orders.add(order)
        if not isinstance(why, str) or not why.strip():
            errors.append(f"why_empty_{tid}")
            continue
        if len(why) > WHY_MAX:
            errors.append(f"why_too_long_{tid}_{len(why)}")
        for tok in re.findall(r"\{\{[^{}]*\}\}", why):
            if not MACRO_RE.fullmatch(tok) or tok not in refs:
                errors.append(f"macro_unknown_{tid}_{tok}")
        rest = MACRO_RE.sub("", why)
        if "{" in rest or "}" in rest or re.search(r"name_\d+", rest):
            errors.append(f"macro_broken_{tid}")
        if re.search(r"\}\}[а-яёa-z]", why, re.I):
            errors.append(f"macro_suffix_{tid}")

    if errors:
        return None, errors
    return sorted(items, key=lambda x: x["order"]), []


# --- Проверки правил (eval): fail — нарушение правил промпта; warn — смотреть глазами ---

FAIL_PATTERNS = {
    "promise": re.compile(r"гарантир|точно (придут|получите|будет)|обязательно (придут|запишутся|купят)|\b\d+\s+(нов\w*\s+)?(клиент|заяв)", re.I),
    "medical": re.compile(r"(?<![а-яё])леч|лекарств|диагноз|обезбол|мазь|компресс|таблет|растяжк|разминк", re.I),
    "name_in_why": re.compile(r"\{\{name_\d+\}\}|(?<![а-яё])(он|она)(?![а-яё])", re.I),
    "price": re.compile(r"₽|\bруб|\d+\s*(р\.|тыс)", re.I),
    "phone": re.compile(r"\+?\d[\d\s\-()]{8,}\d"),
    "nick": re.compile(r"@\w{3,}"),
}
WARN_PATTERNS = {
    "nutrition_terms": re.compile(r"калори|белк|углевод|рацион|диет|перекус", re.I),
    "declension_prep": re.compile(r"\b(для|у|от|к|с|со|о|об|про|без)\s+\{\{name_", re.I),
    "gender_past": re.compile(r"\{\{name_\d+\}\}\s+([а-яё]+л[аи]?)\b", re.I),
    "reproach": re.compile(r"давно пора|опять|снова не|забыл|затянул|не сделал", re.I),
}
TY_RE = re.compile(r"\b(ты|тебе|тебя|тобой|твой|твоя|твоё|твое|твои|твоих|напиши|ответь|сделай|отправь|подтверди|добавь|опубликуй|свяжись|напомни|уточни|проверь|заполни|внеси|обнови)\b", re.I)
VY_RE = re.compile(r"\b(вы|вам|вас|вами|ваш\w*|напишите|ответьте|сделайте|отправьте|подтвердите|добавьте|опубликуйте|свяжитесь|напомните|уточните|проверьте|заполните|внесите|обновите)\b", re.I)


# why описывает другую задачу (модель перепутала task_id): тема плана у задачи CRM и наоборот
PLAN_TOPIC_RE = re.compile(r"старой баз|из базы|бывш\w* клиент|пост(?![а-яё])|поста|публикац|контент|страниц", re.I)
CRM_TOPIC_RE = re.compile(r"(ответ\w*|отвеч\w*) на заявк|договорённост|договоренност", re.I)


def rule_checks(items: list[dict], inp: dict) -> tuple[list[str], list[str]]:
    fails, warns = [], []
    address = inp["profile"]["style"]["address"]
    types = {c["task_id"]: c["type"] for c in inp["candidates"]}
    for it in items:
        why = it["why"]
        tid = it["task_id"]
        is_crm = types.get(tid, "").startswith("crm.")
        if (is_crm and PLAN_TOPIC_RE.search(why)) or (not is_crm and CRM_TOPIC_RE.search(why)):
            fails.append(f"why_other_task_{tid}")
        for name, rx in FAIL_PATTERNS.items():
            if rx.search(why):
                fails.append(f"{name}_{tid}")
        for name, rx in WARN_PATTERNS.items():
            if rx.search(why):
                warns.append(f"{name}_{tid}")
        if address == "vy" and TY_RE.search(why):
            fails.append(f"address_ty_in_vy_{tid}")
        if address == "ty" and VY_RE.search(why):
            fails.append(f"address_vy_in_ty_{tid}")
        if len(why) > WHY_TARGET:
            warns.append(f"why_over_{WHY_TARGET}_{tid}_{len(why)}")
    return fails, warns


def expect_checks(items: list[dict], inp: dict, exp: dict) -> list[str]:
    ids = [it["task_id"] for it in items]
    s = set(ids)
    misses = []
    if "items_min" in exp and len(ids) < exp["items_min"]:
        misses.append(f"items_lt_{exp['items_min']}")
    if "items_max" in exp and len(ids) > exp["items_max"]:
        misses.append(f"items_gt_{exp['items_max']}")
    if "top1_any" in exp and ids and ids[0] not in exp["top1_any"]:
        misses.append(f"top1_{ids[0]}_not_in_{exp['top1_any']}")
    for tid in exp.get("must_include", []):
        if tid not in s:
            misses.append(f"missing_{tid}")
    for group in exp.get("include_any", []):
        if not s & set(group):
            misses.append(f"none_of_{group}")
    if "only_from" in exp and not s <= set(exp["only_from"]):
        misses.append(f"outside_only_from_{sorted(s - set(exp['only_from']))}")
    for group in exp.get("not_together", []):
        if set(group) <= s:
            misses.append(f"together_{group}")
    return misses


TYPE_PRIORITY = [
    "crm.reply_new_contact",
    "crm.next_action",
    "crm.remind_stale",
    "plan.page",
    "plan.base",
    "plan.touch",
    "plan.post",
    "plan.meeting",
    "plan.profile",
]


ITEMS_MAX = {"light": 2, "moderate": 3, "intense": 3}


def tier(task_type: str) -> int:
    """Уровень приоритета: 0 заявки, 1 договорённости, 2 напоминания, 3 план."""
    return {"crm.reply_new_contact": 0, "crm.next_action": 1, "crm.remind_stale": 2}.get(task_type, 3)


def prepare_candidates(candidates: list[dict], intensity: str) -> list[dict]:
    """Подготовка кандидатов кодом T-136 до вызова модели (и для брифа по правилам).

    1) сортировка: тип по TYPE_PRIORITY, затем overdue_days по убыванию;
    2) отсечение уровней: уровни берутся целиком сверху, пока набранных задач меньше максимума
       пунктов для intensity; нижние уровни модели не передаются.
    """
    rank = {t: i for i, t in enumerate(TYPE_PRIORITY)}
    ordered = sorted(candidates, key=lambda c: (rank.get(c["type"], len(rank)), -c["overdue_days"], c["task_id"]))
    n_max = ITEMS_MAX.get(intensity, 3)
    kept, count = [], 0
    for lvl in range(4):
        if count >= n_max:
            break
        group = [c for c in ordered if tier(c["type"]) == lvl]
        kept.extend(group)
        count += len(group)
    return kept


def run_case(case: dict, model: str, key: str, run_no: int) -> dict:
    src = case["input"]
    inp = dict(src, candidates=prepare_candidates(src["candidates"], src["profile"]["intensity"]))
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": json.dumps(inp, ensure_ascii=False)},
        ],
        "temperature": 0.2,
        "max_tokens": 400,
        "response_format": SCHEMA,
    }
    r = chat(body, timeout=15, key=key)
    res = {
        "case": case["id"],
        "run": run_no,
        "ok_http": r.get("ok"),
        "error": r.get("error"),
        "latency_ms": r.get("latency_ms"),
        "tokens_in": r.get("tokens_in"),
        "tokens_out": r.get("tokens_out"),
        "cost_rub": r.get("cost_rub"),
        "cost_source": r.get("cost_source"),
        "content": r.get("content"),
    }
    if not r.get("ok"):
        res.update(valid=False, validation_errors=[r.get("error") or "http"], rules_ok=False, expect_ok=False)
        return res
    items, verrs = validate(r.get("content") or "", inp)
    res["validation_errors"] = verrs
    res["valid"] = items is not None
    if items is None:
        res.update(rules_ok=False, expect_ok=False, rule_fails=[], rule_warns=[], expect_misses=[])
        return res
    fails, warns = rule_checks(items, inp)
    misses = expect_checks(items, inp, case["expect"])
    res.update(
        items=items,
        rule_fails=fails,
        rule_warns=warns,
        rules_ok=not fails,
        expect_misses=misses,
        expect_ok=not misses,
    )
    return res


def render(items: list[dict], case: dict) -> list[str]:
    titles = {c["task_id"]: c["title"] for c in case["input"]["candidates"]}
    out = []
    for it in items:
        why = it["why"]
        title = titles.get(it["task_id"], "?")
        for ref, name in case["demo_names"].items():
            why = why.replace(ref, name)
            title = title.replace(ref, name)
        out.append(f"{it['order']}. [{it['task_id']}] {title}\n   → {why}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    cases = json.loads((HERE / "golden-set-v1.json").read_text(encoding="utf-8"))
    key = load_key()
    jobs = [(c, run) for run in range(1, args.runs + 1) for c in cases]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda j: run_case(j[0], args.model, key, j[1]), jobs))

    n = len(results)
    lat = [r["latency_ms"] for r in results if r.get("latency_ms") is not None]
    costs = [r["cost_rub"] for r in results if r.get("cost_rub") is not None]
    tin = [r["tokens_in"] for r in results if r.get("tokens_in")]
    tout = [r["tokens_out"] for r in results if r.get("tokens_out")]
    summary = {
        "prompt_version": PROMPT_VERSION,
        "model": args.model,
        "runs": args.runs,
        "calls": n,
        "valid_rate": sum(r["valid"] for r in results) / n,
        "rules_rate": sum(r["rules_ok"] for r in results) / n,
        "expect_rate": sum(r["expect_ok"] for r in results) / n,
        "all_ok_rate": sum(r["valid"] and r["rules_ok"] and r["expect_ok"] for r in results) / n,
        "latency_ms_mean": round(statistics.mean(lat)) if lat else None,
        "latency_ms_p95": sorted(lat)[max(0, int(len(lat) * 0.95) - 1)] if lat else None,
        "latency_ms_max": max(lat) if lat else None,
        "tokens_in_mean": round(statistics.mean(tin)) if tin else None,
        "tokens_out_mean": round(statistics.mean(tout)) if tout else None,
        "cost_rub_mean": round(statistics.mean(costs), 5) if costs else None,
        "cost_source": results[0].get("cost_source"),
    }

    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / f"run-{args.tag}.json").write_text(
        json.dumps({"summary": summary, "results": results}, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    by_case = {c["id"]: c for c in cases}
    lines = [f"# Ревью ответов · {PROMPT_VERSION} · {args.model}", "", "Имена — демо-подстановка вместо макросов.", ""]
    for r in sorted(results, key=lambda x: (x["case"], x["run"])):
        c = by_case[r["case"]]
        flag = "OK" if r["valid"] and r["rules_ok"] and r["expect_ok"] else "!!"
        lines.append(f"## {flag} {r['case']} · прогон {r['run']} · {r['latency_ms']} мс")
        lines.append(f"_{c['description']}_")
        if c["expect"].get("manual"):
            lines.append(f"Смотреть: {c['expect']['manual']}")
        lines.append("")
        if r.get("items"):
            lines.append("```text")
            lines.extend(render(r["items"], c))
            lines.append("```")
        else:
            lines.append(f"Невалидно: {r.get('validation_errors')} · `{(r.get('content') or '')[:200]}`")
        problems = (r.get("rule_fails") or []) + (r.get("expect_misses") or [])
        if problems:
            lines.append(f"Проблемы: {problems}")
        if r.get("rule_warns"):
            lines.append(f"Предупреждения: {r['rule_warns']}")
        lines.append("")
    (out_dir / f"review-{args.tag}.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=1))
    for r in results:
        if not (r["valid"] and r["rules_ok"] and r["expect_ok"]):
            print(f"!! {r['case']} run{r['run']}: v={r.get('validation_errors')} f={r.get('rule_fails')} e={r.get('expect_misses')}")


if __name__ == "__main__":
    main()
