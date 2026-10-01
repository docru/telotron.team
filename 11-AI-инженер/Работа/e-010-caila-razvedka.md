# Разведка Caila · E-010

| Поле | Значение |
|------|----------|
| **Дата** | 2026-10-01 |
| **Цель** | Проверить tools / JSON / stream / latency для ИИ-консультанта |
| **Связь** | [черновик архитектуры](e-010-ai-konsultant-chernovik-arhitektury.md) · T-110 клиент |
| **Секреты** | ключ не логировали; в отчёте только статусы и обезличенные фрагменты |

---

## 1) Вывод коротко

**Caila уже умеет то, что нужно для E-010**, в том числе через **наши текущие URL** из T-110:

| Возможность | Наш путь T-110 | Документированный adapters |
|-------------|----------------|----------------------------|
| Обычный chat | ✅ | ✅ |
| `tools` / `tool_choice` | ✅ gpt-4o-mini, deepseek, qwen | ✅ openai-proxy и open-router |
| `response_format: json_object` | ✅ openai + deepseek | не гоняли отдельно |
| `response_format: json_schema` (strict) | ✅ **gpt-4o-mini** через `CAILA_OPENAI_BASE_URL` | — |
| `stream: true` (SSE) | ✅ openai + deepseek | — |
| Latency короткого ответа | ~1.3–2.3 с | ~1.7–2.9 с на tools |

**Не нужен** парсинг команд из текста: нативный tool calling работает.

**Риск:** `qwen/qwen3.5-flash-02-23` на коротком `max_tokens` уходит в «Thinking Process…» и режет ответ; для чата/tools лучше не брать как основную модель без отдельной настройки.

---

## 2) Какие шлюзы есть

### Уже в продукте (T-110)

| Env | URL | Как зовём модель |
|-----|-----|------------------|
| `CAILA_OPENROUTER_BASE_URL` | `https://caila.io/api/providers/openrouter/v1` | `deepseek/…`, `qwen/…` + заголовок `X-Mlp-Provider: openrouter` |
| `CAILA_OPENAI_BASE_URL` | `https://caila.io/api/openai/v1` | `gpt-4o-mini` |

Клиент: `_telotron.ru/app/Modules/Nutrition/Ai/CailaOpenAiChatClient.php` — сейчас **только** parallel chat, **без** tools/stream/`response_format` (кроме json_object на openai-ветке).

### Документированные Caila

| Шлюз | URL | Заметка |
|------|-----|---------|
| OpenAI adapter | `https://caila.io/api/adapters/openai` | model = `author/service[/model]`; поля кроме `model`/`stream`/`messages` уходят в config (tools туда же) |
| OpenAI direct | `https://caila.io/api/adapters/openai-direct` | прокси «как у провайдера», Caila только биллинг; для ассистентов в доках часто рекомендуют его |
| OpenRouter через adapter | model вида `just-ai/open-router/deepseek/deepseek-v3.2` | проверено на direct + tools ✅ |

Источники: [OpenAI adapter](https://docs.caila.io/api/rest/openai-api), [OpenAI direct](https://docs.caila.io/api/rest/direct-api), схема GPT [`mlp-data-gpt.yml`](https://caila.io/specs/mlp-data-gpt.yml) (есть `tools`, `tool_calls`, `stream`, `finish_reason: tool_calls`).

---

## 3) Матрица живых проб (2026-10-01)

Один ключ workspace. Без ПДн. Стоимость OpenRouter-моделей приходит в `usage.cost` (сверка с прайсом — §3.1).

### A · Базовый chat (наши URL)

| # | Модель | Latency | Результат |
|---|--------|---------|-----------|
| A1 | deepseek-v3.2 @ openrouter | 2.3 с | ✅ «ок» |
| A2 | gpt-4o-mini @ openai | 1.3 с | ✅ |
| A3 | qwen3.5-flash @ openrouter | 1.4 с | ⚠️ `finish_reason=length`, в content — «Thinking Process…» при `max_tokens=20` |

### B · JSON object

| # | Модель | Latency | Результат |
|---|--------|---------|-----------|
| B1 | gpt-4o-mini | 1.5 с | ✅ валидный JSON |
| B2 | deepseek | 8.6 с | ✅ валидный JSON (медленнее) |

### C · JSON Schema (strict) — сценарий утреннего брифа

| # | Модель | Latency | Результат |
|---|--------|---------|-----------|
| C1 | gpt-4o-mini | 1.7 с | ✅ объект `{tasks:[{title,why}]}` по схеме |

*(deepseek + json_schema в этой сессии не гоняли — при необходимости добить отдельным прогоном.)*

### D · Tool calling (наши URL)

Инструмент-заглушка `get_daily_snapshot(include_funnel: bool)`, `tool_choice=required`.

| # | Модель | Latency | Результат |
|---|--------|---------|-----------|
| D1 | gpt-4o-mini | 1.5 с | ✅ `finish_reason=tool_calls`, args `{"include_funnel":true}` |
| D2 | deepseek | 3.4 с | ✅ tool_calls |
| D3 | qwen | 1.9 с | ✅ tool_calls, но в `content` длинный reasoning-текст |

### E · Streaming SSE

| # | Модель | Latency до конца | Результат |
|---|--------|------------------|-----------|
| E1 | gpt-4o-mini | 1.3 с | ✅ `text/event-stream`, чанки `data: {…delta…}` |
| E2 | deepseek | 1.3 с | ✅ SSE |

### F · Документированные adapters + tools

| # | Путь | Результат |
|---|------|-----------|
| F1 | `adapters/openai` + `just-ai/openai-proxy/gpt-4o-mini` | ✅ tools |
| F2 | `adapters/openai-direct` + `just-ai/openai-proxy/gpt-4o-mini` | ✅ tools |
| F3 | `adapters/openai-direct` + `just-ai/open-router/deepseek/deepseek-v3.2` | ✅ tools |
| F4 | `adapters/openai` + `provider:openrouter` + model `deepseek/…` | ❌ 404 «Account deepseek not found» — этот способ вызова **не использовать** без уточнения формата |

### G · Более длинный ответ

gpt-4o-mini ~3.1 с на ~160 completion tokens — ок для советов/брифа.

### 3.1 Сверка `usage.cost` с прайсом

Прайс: `Команда/01-Директор/caila-llm-prices.csv` (₽ за 1М токенов). Для `openai`-шлюза (gpt-4o-mini) поле `cost` не приходит.

| Проба | Токены вх / вых | По прайсу, ₽ | `usage.cost` | Отношение |
|-------|-----------------|--------------|--------------|-----------|
| D3 qwen, tools | 292 / 110 | 0,0059 | 0,0062 | ×1,04 |
| A1 deepseek | 11 / 2 | 0,00044 | 0,00068 | ×1,5 |
| D2 deepseek, tools | 330 / 33 | 0,0119 | 0,0312 | ×2,6 |
| B2 deepseek, json | 16 / 9 | 0,00092 | 0,0031 | ×3,4 |

Выводы:

- `usage.cost`, по всей видимости, **в рублях** (qwen совпал с прайсом).  
- **deepseek через OpenRouter — в 1,5–3,4 раза дороже прайса**, разброс от запроса к запросу. Вероятная причина — OpenRouter маршрутизирует на разных апстрим-провайдеров с разной ценой (в SSE виден `provider: DigitalOcean`).  
- Для бюджета брать **фактический `usage.cost`**, а не прайс; прайс для deepseek — нижняя граница.  
- Проверить: можно ли закрепить апстрим-провайдера OpenRouter через Caila (поле `provider` в теле — у OpenRouter оно есть; через Caila не проверяли).

---

## 4) Рекомендации для E-010

### Шлюз

1. **Ближайший путь:** расширить/вынести текущий клиент T-110 (наши два base URL). Tools/stream/json уже работают — меньше сюрпризов.  
2. **Альтернатива на ADR:** унифицировать на `adapters/openai-direct` с model id `just-ai/openai-proxy/…` и `just-ai/open-router/…` — так проще один base URL.  
3. Не опираться на F4-стиль (`provider` + короткий model) без отдельной проверки.

### Модели (черновой конфиг сценариев)

| Сценарий | Модель | Почему |
|----------|--------|--------|
| `morning_brief` / structured JSON | **gpt-4o-mini** | json_schema + стабильный JSON, ~1.7 с |
| Чат + tools | **gpt-4o-mini** или **deepseek-v3.2** | оба отдают tool_calls; mini быстрее и чище |
| Дешёвое извлечение сигналов навыков | deepseek / позже проверить qwen | qwen пока с оговоркой про thinking |
| Стратегия / совещание | сильная модель (выбрать отдельно по цене) | не обязательно в первом куске |

Qwen из ансамбля КБЖУ **не** брать как default для консультанта, пока не отключим/не ограничим thinking и не проверим RU без утечки рассуждений в `content`.

### Таймауты

- T-110: 20 с — для брифа и одного tool-раунда достаточно.  
- Для чата с **несколькими** tool-шагами (до 5): таймаут **на шаг** 20–30 с + общий бюджет job (например 90 с).  
- Deepseek на JSON иногда ~8 с — не ставить 5 с как в старом дефолте клиента.

### Что добавить в общий AI-адаптер

- `chat` (non-stream)  
- `chatStream` (SSE)  
- `tools` + разбор `tool_calls`  
- `response_format`: `json_object` и `json_schema`  
- учёт `usage` / `cost` в AiTrace  
- единый `request_id`, логи без ключей и без сырых ПДн  

Nutrition потом мигрирует на адаптер (отдельный шаг).

### Eval / пилот

- Первый сценарий `morning_brief` — только **json_schema**, без tools (как в архитектуре).  
- Tool calling — во втором куске (чат).  
- Стриминг UI — опционально; API уже позволяет.

---

## 5) Открытые хвосты разведки

- [x] `json_schema` на deepseek через openrouter — плоская схема КБЖУ работает; вложенная схема брифа — **нет** (`-1` в `task_id`/`order`, 34% валидных) — [T-138 §7.3](e-010-brief-prompt-v1-eval.md)  
- [ ] Полный round-trip: tool_call → наше сообщение `role=tool` → финальный ответ  
- [ ] Streaming + tools одновременно (нужно ли для UX)  
- [x] Единица `usage.cost` и сверка с прайсом — §3.1 (₽; deepseek дороже прайса ×1,5–3,4)  
- [ ] Закрепление апстрим-провайдера OpenRouter для deepseek (стабильная цена)  
- [ ] Стоимость gpt-4o-mini по факту (поле `cost` не приходит — смотреть детализацию расходов в кабинете Caila)  
- [ ] Список моделей для «сильного» слота совещания (цена × качество)  
- [ ] Нужен ли `adapters/openai/v1` вместо `/api/openai/v1` в долгую
- [x] **Блокер миграции Nutrition (решение архитектора 2026-10-01: один шлюз `openai-direct`):** на `openai-direct` прогнать `json_schema`, `json_object`, все 3 модели КБЖУ (deepseek, qwen, gpt-4o-mini), наличие `usage.cost` — **снят**: все 3 работают; qwen — только с `reasoning: {"enabled": false}` и без `response_format`; у gpt-4o-mini нет `usage.cost` — [T-138 §2](e-010-brief-prompt-v1-eval.md)

---

## 6) Влияние на черновик архитектуры

Подтверждено:

- нативный tool calling — **да**;  
- строгий JSON для сценариев — **да** (минимум на gpt-4o-mini);  
- stream — **да**, если захотим печатать ответ по мере генерации;  
- общий адаптер поверх Caila — разумный следующий шаг с архитектором.

Не подтверждена необходимость менять провайдера: **Caila остаётся**.

---

## Журнал

### 2026-10-01

- Живые пробы A–G; tools/JSON/stream на наших URL и на openai / openai-direct; F4-паттерн отвергнут.
- Сверка `usage.cost` с прайсом: qwen ≈ прайс, deepseek ×1,5–3,4 (маршрутизация OpenRouter).
- Результаты зафиксированы в журнале [E-010](../../backlog/эпики/E-010-ии-консультант-продаж.md).
- T-138: пробы `openai-direct` для 3 моделей КБЖУ, deepseek на схеме брифа — хвосты §5 закрыты, детали в [отчёте](e-010-brief-prompt-v1-eval.md). Оговорка про qwen в §4 снимается параметром `reasoning: {"enabled": false}`.
