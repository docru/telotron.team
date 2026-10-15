"""Прогон sales.tools.draft_message.v2.

  python3 run_draft_v2.py --tag draft-v2-gpt4omini
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
sys.path.insert(0, str(HERE.parent / "e-010-brief-eval"))
from caila import chat, load_key  # noqa: E402

PROMPT_VERSION = "sales.tools.draft_message.v2"
SYSTEM = (HERE.parent / "e-014-prompts" / f"{PROMPT_VERSION}.system.txt").read_text(encoding="utf-8")
SCHEMA = json.loads(
    (HERE.parent / "e-014-schemas" / f"{PROMPT_VERSION}.schema.json").read_text(encoding="utf-8")
)

MACRO_RE = re.compile(r"\{\{name_\d+\}\}")
PROMISE_RE = re.compile(
    r"гарантир|точно (придут|получите)|\b\d+\s+(нов\w*\s+)?(клиент|заяв)", re.I
)
TY_RE = re.compile(r"\b(ты|тебе|тебя|твой|твоя|напиши|ответь)\b", re.I)
VY_RE = re.compile(r"\b(вы|вам|вас|ваш\w*|напишите|ответьте)\b", re.I)


def validate(content: str, inp: dict) -> tuple[dict | None, list[str]]:
    errors: list[str] = []
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return None, ["invalid_json"]
    drafts = data.get("drafts")
    why = data.get("why_so")
    if not isinstance(drafts, list) or not drafts:
        return None, ["no_drafts"]
    if not isinstance(why, list) or not (3 <= len(why) <= 5):
        errors.append(f"why_so_len_{len(why) if isinstance(why, list) else 'bad'}")
    expected_refs = [p["ref"] for p in inp["people"]] if inp["people"] else [None]
    if len(drafts) != len(expected_refs):
        errors.append(f"drafts_count_{len(drafts)}_ne_{len(expected_refs)}")
    seen = []
    for d in drafts:
        if not isinstance(d, dict):
            errors.append("draft_not_object")
            continue
        ref, body = d.get("person_ref"), d.get("body")
        seen.append(ref)
        if not isinstance(body, str) or len(body.strip()) < 10:
            errors.append(f"body_short_{ref}")
            continue
        if ref is None:
            if MACRO_RE.search(body) or MACRO_RE.search(d.get("alt_body") or ""):
                errors.append("macro_in_generic")
        else:
            if ref not in body and "{{name" not in body:
                # soft: require macro in body when person present
                if not MACRO_RE.search(body):
                    errors.append(f"missing_macro_{ref}")
            for m in MACRO_RE.findall(body):
                if m != ref:
                    errors.append(f"wrong_macro_{m}_for_{ref}")
    if sorted([str(x) for x in seen]) != sorted([str(x) for x in expected_refs]):
        # order may differ — check set equality
        if set(map(str, seen)) != set(map(str, expected_refs)):
            errors.append(f"refs_mismatch_{seen}")
    if errors:
        return None, errors
    return data, []


def expect_checks(data: dict, inp: dict, exp: dict) -> list[str]:
    misses = []
    drafts = data["drafts"]
    if "drafts_count" in exp and len(drafts) != exp["drafts_count"]:
        misses.append(f"count_{len(drafts)}")
    if "refs" in exp:
        got = [d["person_ref"] for d in drafts]
        if set(map(str, got)) != set(map(str, exp["refs"])):
            misses.append(f"refs_{got}")
    if exp.get("bodies_distinct"):
        bodies = [d["body"].strip().lower() for d in drafts]
        if len(set(bodies)) < len(bodies):
            misses.append("bodies_not_distinct")
    if exp.get("must_macro"):
        for d in drafts:
            if d["person_ref"] and not MACRO_RE.search(d["body"]):
                misses.append(f"no_macro_{d['person_ref']}")
    if exp.get("no_macro"):
        for d in drafts:
            if MACRO_RE.search(d["body"]) or MACRO_RE.search(d.get("alt_body") or ""):
                misses.append("unexpected_macro")
    if exp.get("forbid_promise"):
        blob = " ".join(d["body"] for d in drafts) + " " + " ".join(data.get("why_so") or [])
        if PROMISE_RE.search(blob):
            misses.append("promise")
    if exp.get("address") == "ty":
        for d in drafts:
            if VY_RE.search(d["body"]):
                misses.append(f"vy_in_ty_{d['person_ref']}")
    if "why_so_min" in exp and len(data.get("why_so") or []) < exp["why_so_min"]:
        misses.append("why_so_short")
    if "why_so_max" in exp and len(data.get("why_so") or []) > exp["why_so_max"]:
        misses.append("why_so_long")
    address = inp["profile"]["style"]["address"]
    if address == "vy":
        for d in drafts:
            if TY_RE.search(d["body"]) and not VY_RE.search(d["body"]):
                # allow if neither strongly; fail if clear ty verbs without vy
                if re.search(r"\b(напиши|ответь|ты)\b", d["body"], re.I):
                    misses.append(f"ty_in_vy_{d['person_ref']}")
    return misses


def run_case(case: dict, model: str, key: str, run_no: int) -> dict:
    inp = case["input"]
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": json.dumps(inp, ensure_ascii=False)},
        ],
        "temperature": 0.3,
        "max_tokens": 1200,
        "response_format": SCHEMA,
    }
    r = chat(body, timeout=45, key=key)
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
        res.update(valid=False, expect_ok=False, validation_errors=[r.get("error")])
        return res
    data, verrs = validate(r.get("content") or "", inp)
    res["validation_errors"] = verrs
    res["valid"] = data is not None
    if data is None:
        res["expect_ok"] = False
        return res
    misses = expect_checks(data, inp, case["expect"])
    res.update(parsed=data, expect_misses=misses, expect_ok=not misses)
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="just-ai/openai-proxy/gpt-4o-mini")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--tag", default="draft-v2-gpt4omini")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()

    cases = json.loads((HERE / "draft-set-v2.json").read_text(encoding="utf-8"))
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
        "expect_pct": round(100 * sum(1 for r in results if r.get("expect_ok")) / n, 1),
        "all_ok_pct": round(
            100 * sum(1 for r in results if r.get("valid") and r.get("expect_ok")) / n, 1
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
        if not (r.get("valid") and r.get("expect_ok")):
            print(
                f"!! {r['case']} r{r['run']}: v={r.get('validation_errors')} e={r.get('expect_misses')}"
            )


if __name__ == "__main__":
    main()
