# Промпты `sales.strategic.*` v1 (черновик волны 4)

| Поле | Значение |
|------|----------|
| **Контракты** | [e-014-volna-4-kontrakty.md](../e-014-volna-4-kontrakty.md) |
| **Схемы** | [e-014-schemas/](../e-014-schemas/) |
| **Проверки кода** | [e-014-volna-4-proverki.md](../e-014-volna-4-proverki.md) |
| **Куда в код** | после утверждения → `_telotron.ru/resources/ai/sales/` |

| Файл | Сценарий |
|------|----------|
| `strategic.intake_extract.v1.system.txt` | Разбор рассказа → поля анкеты |
| `strategic.diagnose.v1.system.txt` | Диагност (онбординг / совещание) |
| `strategic.propose.v1.system.txt` | Стратег |
| `strategic.decompose.v1.system.txt` | Декомпозер |
| `strategic.review.v1.system.txt` | Монитор |

Сообщения: `system` = файл; `user` = JSON входа (одной строкой). Ответ — только JSON по схеме. Few-shot: сжатый пример внутри файла (MVP без таблицы примеров); правила — [контракты §7](../e-014-volna-4-kontrakty.md#7-few-shot-формат-отбор-обновление).

**Версия текста — v1.1** (2026-10-13, после прогона [e-014-strategic-eval-v1.md](../e-014-strategic-eval-v1.md)). Имена файлов остаются `*.v1.*` — контракт схем не менялся; `prompt_version` в коде — `v1.1`. Черновики до правок — `drafts/`.

Диагносту код передаёт `askable_fields` и собирает схему вопросов под запрос — без этого промпт не удерживает модель от переспрашивания анкеты.
