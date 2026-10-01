"""Минимальный клиент Caila openai-direct для проб и eval (без зависимостей).

Ключ читается из _telotron.ru/.env (CAILA_API_KEY) и никуда не пишется.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[4] / "_telotron.ru" / ".env"
DIRECT_BASE_URL = "https://caila.io/api/adapters/openai-direct"

# ₽ за 1М токенов (Команда/01-Директор/caila-llm-prices.csv) — для моделей, где Caila не отдаёт usage.cost.
PRICE_RUB_PER_M = {
    "just-ai/openai-proxy/gpt-4o-mini": (18.63, 74.52),
    "just-ai/open-router/deepseek/deepseek-v3.2": (31.2984, 46.9476),
    "just-ai/open-router/qwen/qwen3.5-flash-02-23": (8.073, 32.292),
}


def load_key() -> str:
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("CAILA_API_KEY="):
            key = line.split("=", 1)[1].strip().strip('"').strip("'")
            if key:
                return key
    raise RuntimeError("CAILA_API_KEY не найден в _telotron.ru/.env")


def chat(body: dict, timeout: float = 30.0, key: str | None = None) -> dict:
    """POST chat/completions. Возвращает нормализованный результат, без ключа."""
    key = key or load_key()
    req = urllib.request.Request(
        f"{DIRECT_BASE_URL}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    t0 = time.perf_counter()
    out: dict = {"model": body.get("model"), "ok": False}
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            out["status"] = resp.status
    except urllib.error.HTTPError as e:
        out["status"] = e.code
        out["error"] = f"http_{e.code}: {e.read().decode('utf-8', errors='replace')[:300]}"
        out["latency_ms"] = int((time.perf_counter() - t0) * 1000)
        return out
    except Exception as e:  # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
        out["latency_ms"] = int((time.perf_counter() - t0) * 1000)
        return out

    out["latency_ms"] = int((time.perf_counter() - t0) * 1000)
    try:
        j = json.loads(raw)
    except json.JSONDecodeError:
        out["error"] = "non_json_response"
        out["raw"] = raw[:300]
        return out

    choice = (j.get("choices") or [{}])[0]
    msg = choice.get("message") or {}
    usage = j.get("usage") or {}
    tin = usage.get("prompt_tokens")
    tout = usage.get("completion_tokens")
    cost = usage.get("cost")
    cost_source = "caila" if cost is not None else None
    if cost is None and tin is not None and tout is not None and body.get("model") in PRICE_RUB_PER_M:
        pin, pout = PRICE_RUB_PER_M[body["model"]]
        cost = tin * pin / 1e6 + tout * pout / 1e6
        cost_source = "price_csv"

    out.update(
        ok=True,
        content=msg.get("content") or "",
        tool_calls=msg.get("tool_calls"),
        finish_reason=choice.get("finish_reason"),
        tokens_in=tin,
        tokens_out=tout,
        cost_rub=cost,
        cost_source=cost_source,
        upstream_provider=j.get("provider"),
    )
    return out
