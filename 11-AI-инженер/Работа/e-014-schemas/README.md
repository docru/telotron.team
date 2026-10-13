# Схемы ответов `sales.strategic.*` (черновик волны 4)

Канон правил: [e-014-volna-4-kontrakty.md](../e-014-volna-4-kontrakty.md).

После утверждения переносятся в `_telotron.ru/resources/ai/sales/` с теми же именами файлов.

| Файл | Сценарий |
|------|----------|
| `strategic.intake_extract.v1.schema.json` | Разбор рассказа → поля профиля + `unclear` |
| `strategic.diagnose.v1.schema.json` | Диагност (онбординг и неделя) |
| `strategic.propose.v1.schema.json` | Стратег |
| `strategic.decompose.v1.schema.json` | Декомпозер |
| `strategic.review.v1.schema.json` | Монитор |

**OpenAI strict:** не использовать `uniqueItems` в схемах (HTTP 400). Дубликаты отсекает код.

Ограничение `final_round` (вопросы запрещены) схема JSON сама по режиму не ветвит — оркестратор передаёт в промпт `final_round=true`, код отклоняет непустой `questions`.
