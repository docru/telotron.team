"""Прогон sales.operational.brief.v2.

  python3 run_brief_v2.py --model just-ai/openai-proxy/gpt-4o-mini --runs 1 --tag v2-gpt4omini
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
E010 = HERE.parent / "e-010-brief-eval"
sys.path.insert(0, str(E010))
from caila import chat, load_key  # noqa: E402

PROMPT_VERSION = "sales.operational.brief.v2"
SYSTEM = (HERE.parent / "e-014-prompts" / f"{PROMPT_VERSION}.system.txt").read_text(encoding="utf-8")
SCHEMA = json.loads(
    (HERE.parent / "e-014-schemas" / f"{PROMPT_VERSION}.schema.json").read_text(encoding="utf-8")
)

WHY_MAX = 160
WHY_TARGET = 120
MACRO_RE = re.compile(r"\{\{name_\d+\}\}")

TYPE_PRIORITY = [
    "crm.reply_new_contact",
    "crm.next_action",
    "crm.remind_stale",
    "strategy.base_reactivate",
    "strategy.follow_up",
    "strategy.trial_convert",
    "strategy.referral_ask",
    "strategy.base_collect",
    "strategy.offer_setup",
    "strategy.link_share",
    "strategy.partner_outreach",
    "strategy.listing_setup",
    "strategy.community_engage",
    "strategy.content_post",
    "strategy.content_short",
    "strategy.social_profile",
    "strategy.review_collect",
]
ITEMS_MAX = {"light": 2, "moderate": 3, "intense": 3}


def tier(task_type: str) -> int:
    return {"crm.reply_new_contact": 0, "crm.next_action": 1, "crm.remind_stale": 2}.get(task_type, 3)


def prepare_candidates(candidates: list[dict], intensity: str) -> list[dict]:
    rank = {t: i for i, t in enumerate(TYPE_PRIORITY)}
    ordered = sorted(
        candidates,
        key=lambda c: (rank.get(c["type"], len(rank)), -c["overdue_days"], c["task_id"]),
    )
    n_max = ITEMS_MAX.get(intensity, 3)
    kept, count = [], 0
    for lvl in range(4):
        if count >= n_max:
            break
        group = [c for c in ordered if tier(c["type"]) == lvl]
        kept.extend(group)
        count += len(group)
    return kept


FAIL_PATTERNS = {
    "promise": re.compile(
        r"гарантир|точно (придут|получите|будет)|обязательно (придут|запишутся)|\b\d+\s+(нов\w*\s+)?(клиент|заяв)",
        re.I,
    ),
    "name_in_why": re.compile(r"\{\{name_\d+\}\}|(?<![а-яё])(он|она)(?![а-яё])", re.I),
    "price": re.compile(r"₽|\bруб", re.I),
}
TY_RE = re.compile(
    r"\b(ты|тебе|тебя|тобой|твой|твоя|твоё|твое|твои|напиши|ответь|сделай)\b", re.I
)
VY_RE = re.compile(
    r"\b(вы|вам|вас|ваш\w*|напишите|ответьте|сделайте)\b", re.I
)


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
    intensity = inp["profile"]["intensity"]
    n_max = min(ITEMS_MAX.get(intensity, 3), len(cand_ids))
    if not 1 <= len(items) <= n_max:
        errors.append(f"items_count_{len(items)}_not_in_1..{n_max}")
    seen_ids: set[int] = set()
    for it in items:
        tid, order, why = it.get("task_id"), it.get("order"), it.get("why")
        if not isinstance(tid, int) or tid not in cand_ids:
            errors.append(f"task_id_not_candidate_{tid}")
        if tid in seen_ids:
            errors.append(f"task_id_duplicate_{tid}")
        seen_ids.add(tid)
        if not isinstance(why, str) or not why.strip():
            errors.append(f"why_empty_{tid}")
            continue
        if len(why) > WHY_MAX:
            errors.append(f"why_too_long_{tid}")
        if MACRO_RE.search(why):
            errors.append(f"macro_in_why_{tid}")
    if errors:
        return None, errors
    return sorted(items, key=lambda x: x["order"]), []


def rule_checks(items: list[dict], inp: dict) -> list[str]:
    fails = []
    address = inp["profile"]["style"]["address"]
    for it in items:
        why, tid = it["why"], it["task_id"]
        for name, rx in FAIL_PATTERNS.items():
            if rx.search(why):
                fails.append(f"{name}_{tid}")
        if address == "vy" and TY_RE.search(why):
            fails.append(f"address_ty_in_vy_{tid}")
        if address == "ty" and VY_RE.search(why):
            fails.append(f"address_vy_in_ty_{tid}")
    return fails


def expect_checks(items: list[dict], exp: dict) -> list[str]:
    ids = [it["task_id"] for it in items]
    s = set(ids)
    misses = []
    if "items_min" in exp and len(ids) < exp["items_min"]:
        misses.append(f"items_lt_{exp['items_min']}")
    if "items_max" in exp and len(ids) > exp["items_max"]:
        misses.append(f"items_gt_{exp['items_max']}")
    if "top1_any" in exp and ids and ids[0] not in exp["top1_any"]:
        misses.append(f"top1_{ids[0]}")
    for tid in exp.get("must_include", []):
        if tid not in s:
            misses.append(f"missing_{tid}")
    for group in exp.get("include_any", []):
        if not s & set(group):
            misses.append(f"none_of_{group}")
    if "only_from" in exp and not s <= set(exp["only_from"]):
        misses.append(f"outside_{sorted(s - set(exp['only_from']))}")
    if exp.get("address") == "ty":
        for it in items:
            if VY_RE.search(it["why"]):
                misses.append(f"address_not_ty_{it['task_id']}")
    return misses


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
    r = chat(body, timeout=20, key=key)
    res = {
        "case": case["id"],
        "run": run_no,
        "ok_http": r.get("ok"),
        "error": r.get("error"),
        "latency_ms": r.get("latency_ms"),
        "cost_rub": r.get("cost_rub"),
        "content": r.get("content"),
    }
    if not r.get("ok"):
        res.update(valid=False, rules_ok=False, expect_ok=False, validation_errors=[r.get("error")])
        return res
    items, verrs = validate(r.get("content") or "", inp)
    res["validation_errors"] = verrs
    res["valid"] = items is not None
    if items is None:
        res.update(rules_ok=False, expect_ok=False)
        return res
    fails = rule_checks(items, inp)
    misses = expect_checks(items, case["expect"])
    res.update(items=items, rule_fails=fails, rules_ok=not fails, expect_misses=misses, expect_ok=not misses)
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="just-ai/openai-proxy/gpt-4o-mini")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--tag", default="v2-gpt4omini")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    cases = json.loads((HERE / "golden-set-v2.json").read_text(encoding="utf-8"))
    key = load_key()
    jobs = [(c, run) for run in range(1, args.runs + 1) for c in cases]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda j: run_case(j[0], args.model, key, j[1]), jobs))

    n = len(results)
    lat = [r["latency_ms"] for r in results if r.get("latency_ms") is not None]
    costs = [r["cost_rub"] for r in results if r.get("cost_rub") is not None]
    summary = {
        "prompt_version": PROMPT_VERSION,
        "model": args.model,
        "runs": args.runs,
        "calls": n,
        "valid_pct": round(100 * sum(1 for r in results if r.get("valid")) / n, 1),
        "rules_pct": round(100 * sum(1 for r in results if r.get("rules_ok")) / n, 1),
        "expect_pct": round(100 * sum(1 for r in results if r.get("expect_ok")) / n, 1),
        "all_ok_pct": round(
            100 * sum(1 for r in results if r.get("valid") and r.get("rules_ok") and r.get("expect_ok")) / n, 1
        ),
        "latency_ms_mean": round(statistics.mean(lat)) if lat else None,
        "cost_rub_sum": round(sum(costs), 4) if costs else None,
    }
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / f"run-{args.tag}.json").write_text(
        json.dumps({"summary": summary, "results": results}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    for r in results:
        if not (r.get("valid") and r.get("rules_ok") and r.get("expect_ok")):
            print(
                f"!! {r['case']} r{r['run']}: v={r.get('validation_errors')} "
                f"f={r.get('rule_fails')} e={r.get('expect_misses')}"
            )


if __name__ == "__main__":
    main()
