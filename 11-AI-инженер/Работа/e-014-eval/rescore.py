#!/usr/bin/env python3
"""Переоценка сохранённых ответов по текущим проверкам без вызова моделей.

  python3 rescore.py v1-final-deepseek v1-final-qwen
"""
from __future__ import annotations

import json
import sys

import run_strategic_eval as R

CHECKS = {
    "intake": R.expect_intake,
    "diagnose": R.expect_diagnose,
    "propose": R.expect_propose,
    "decompose": R.expect_decompose,
    "review": R.expect_review,
}


def rescore(tag: str) -> dict:
    path = R.HERE / "results" / f"run-{tag}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    jobs = {(c, a): (i, e) for c, a, i, e in R.build_jobs()}
    for r in payload["results"]:
        if not r.get("parsed"):
            continue
        inp, exp = jobs[(r["case"], r["agent"])]
        misses = CHECKS[r["agent"]](r["parsed"], exp, inp)
        r.update(expect_misses=misses, expect_ok=not misses)
    old = payload["summary"]
    summary = R.summarize(payload["results"])
    for k in ("runs", "schema", "reasoning_off"):
        if k in old:
            summary[k] = old[k]
    summary["rescored"] = True
    payload["summary"] = summary
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    R.write_md(tag, payload["results"], summary, payload["model"])
    return summary


def main() -> None:
    for tag in sys.argv[1:]:
        s = rescore(tag)
        print(tag, s["expect_pct_all"], {a: v["expect_pct"] for a, v in s["agents"].items()})


if __name__ == "__main__":
    main()
