"""qwen3.5-flash: текущий путь T-110 vs openai-direct, с/без отключения рассуждений.

Парсинг — как в NutritionAiKbjuAggregator: последний объект с "energy_kcal_100".
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request

from caila import chat, load_key
from probe_direct import DISHES, KBJU_SYSTEM, KEYS

OLD_OPENROUTER = "https://caila.io/api/providers/openrouter/v1/chat/completions"


def parse_like_product(content: str) -> dict | None:
    chunks = re.findall(r"\{[^{}]*\"energy_kcal_100\"[^{}]*\}", content or "", re.S)
    for chunk in reversed(chunks):
        try:
            obj = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        if all(isinstance(obj.get(k), (int, float, str)) for k in KEYS):
            return {k: obj[k] for k in KEYS}
    return None


def old_path(body: dict, key: str) -> dict:
    req = urllib.request.Request(
        OLD_OPENROUTER,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "X-Mlp-Provider": "openrouter",
        },
        method="POST",
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            j = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"http_{e.code}: {e.read().decode()[:200]}", "latency_ms": int((time.perf_counter() - t0) * 1000)}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e), "latency_ms": int((time.perf_counter() - t0) * 1000)}
    choice = (j.get("choices") or [{}])[0]
    u = j.get("usage") or {}
    return {
        "ok": True,
        "content": (choice.get("message") or {}).get("content") or "",
        "finish_reason": choice.get("finish_reason"),
        "tokens_out": u.get("completion_tokens"),
        "cost_rub": u.get("cost"),
        "latency_ms": int((time.perf_counter() - t0) * 1000),
    }


def main() -> None:
    key = load_key()
    rows = []
    for dish in DISHES:
        msgs = [{"role": "system", "content": KBJU_SYSTEM}, {"role": "user", "content": f"Блюдо: {dish}"}]
        variants = [
            ("old_path", lambda: old_path({"model": "qwen/qwen3.5-flash-02-23", "messages": msgs, "temperature": 0}, key)),
            ("direct", lambda: chat({"model": "just-ai/open-router/qwen/qwen3.5-flash-02-23", "messages": msgs, "temperature": 0}, 40, key)),
            ("direct_reasoning_off", lambda: chat({"model": "just-ai/open-router/qwen/qwen3.5-flash-02-23", "messages": msgs, "temperature": 0, "reasoning": {"enabled": False}}, 40, key)),
            ("old_path_reasoning_off", lambda: old_path({"model": "qwen/qwen3.5-flash-02-23", "messages": msgs, "temperature": 0, "reasoning": {"enabled": False}}, key)),
        ]
        for name, fn in variants:
            r = fn()
            content = r.get("content") or ""
            rows.append({
                "dish": dish,
                "variant": name,
                "ok": r.get("ok"),
                "error": r.get("error"),
                "latency_ms": r.get("latency_ms"),
                "finish_reason": r.get("finish_reason"),
                "tokens_out": r.get("tokens_out"),
                "cost_rub": r.get("cost_rub"),
                "thinking_in_content": content.lstrip().startswith("Thinking"),
                "parsed_like_product": parse_like_product(content),
                "content_head": content[:100],
                "content_tail": content[-160:],
            })
            print(f"done {dish} {name}", file=sys.stderr)
    print(json.dumps(rows, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
