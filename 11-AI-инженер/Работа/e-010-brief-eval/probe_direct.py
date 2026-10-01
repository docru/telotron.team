"""Пробы шлюза openai-direct для миграции питания (T-135 часть B) и брифа.

Запуск: python3 probe_direct.py > results/probe-direct-YYYY-MM-DD.json
"""

from __future__ import annotations

import json
import re
import sys

from caila import chat, load_key

MODELS = [
    "just-ai/open-router/deepseek/deepseek-v3.2",
    "just-ai/open-router/qwen/qwen3.5-flash-02-23",
    "just-ai/openai-proxy/gpt-4o-mini",
]

# Промпт ансамбля КБЖУ — дословно из NutritionAiEnsembleService (T-110).
KBJU_SYSTEM = (
    "Ты нутрициолог. Оцени КБЖУ блюда на 100 г готового продукта. Ответь ОДНИМ JSON-объектом без markdown, "
    "без reasoning/thinking, без пояснений: {\"energy_kcal_100\":number,\"protein_g_100\":number,"
    "\"fat_g_100\":number,\"carbs_g_100\":number}. Только арабские цифры (например 3, не III). "
    "Все числа ≥0; неизвестно → 0."
)
DISHES = ["гречка с курицей", "борщ со сметаной", "сырники"]

KBJU_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "kbju",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "energy_kcal_100": {"type": "number"},
                "protein_g_100": {"type": "number"},
                "fat_g_100": {"type": "number"},
                "carbs_g_100": {"type": "number"},
            },
            "required": ["energy_kcal_100", "protein_g_100", "fat_g_100", "carbs_g_100"],
            "additionalProperties": False,
        },
    },
}

KEYS = ("energy_kcal_100", "protein_g_100", "fat_g_100", "carbs_g_100")


def parse_kbju(content: str) -> dict | None:
    """Тот же принцип, что у агрегатора: первый JSON-объект с четырьмя числами."""
    m = re.search(r"\{.*\}", content or "", re.S)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if not all(isinstance(obj.get(k), (int, float)) for k in KEYS):
        return None
    return {k: obj[k] for k in KEYS}


def kbju_call(model: str, dish: str, response_format: dict | None, key: str) -> dict:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": KBJU_SYSTEM},
            {"role": "user", "content": f"Блюдо: {dish}"},
        ],
        "temperature": 0,
    }
    if response_format:
        body["response_format"] = response_format
    r = chat(body, timeout=30, key=key)
    parsed = parse_kbju(r.get("content", "")) if r.get("ok") else None
    return {
        "model": model,
        "dish": dish,
        "mode": (response_format or {}).get("type", "none"),
        "ok": r.get("ok"),
        "status": r.get("status"),
        "error": r.get("error"),
        "latency_ms": r.get("latency_ms"),
        "finish_reason": r.get("finish_reason"),
        "parsed": parsed,
        "content_head": (r.get("content") or "")[:160],
        "content_is_pure_json": bool(parsed) and (r.get("content") or "").strip().startswith("{"),
        "tokens_in": r.get("tokens_in"),
        "tokens_out": r.get("tokens_out"),
        "cost_rub": r.get("cost_rub"),
        "cost_source": r.get("cost_source"),
        "upstream_provider": r.get("upstream_provider"),
    }


def main() -> None:
    key = load_key()
    rows = []
    for model in MODELS:
        for dish in DISHES:
            rows.append(kbju_call(model, dish, None, key))
            rows.append(kbju_call(model, dish, {"type": "json_object"}, key))
        rows.append(kbju_call(model, DISHES[0], KBJU_SCHEMA, key))
        print(f"done {model}", file=sys.stderr)
    print(json.dumps(rows, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
