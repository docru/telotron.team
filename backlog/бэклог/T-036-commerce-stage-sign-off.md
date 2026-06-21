# T-036 · Commerce: stage sign-off, E2E, runbook

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [T-026](T-026-commerce-модуль-эпик.md) |
| **Приоритет** | P1 |
| **Спринт** | 5 |
| **Роль** | dev + директор (sign-off stage) |
| **Создан** | 2026-06-12 |
| **Оценка** | 6–8 ч |
| **Зависит от** | T-027…T-035, [T-024](T-024-reminders-одноразовый-лайтбокс.md) |

## Контекст

Финальный прогон **ADR-001 B1–B7** на stage к **31.07**. Закрывает эпик T-026 (prod — отдельный gate **01.08**).

## Критерии готовности

- [ ] E2E (feature или Dusk/manual script): триал → пополнение (sandbox) → nightly debit → нехватка → `light` → лайтбокс.
- [ ] Runbook §14 ТЗ проверен на stage: webhook delay, dub webhook, missed debit, balance reconcile.
- [ ] Чеклист B1–B7 + C+ отмечен в журнале эпика T-026.
- [ ] Регрессия критичных сценариев A8 перед sign-off.
- [ ] Запись sign-off stage ready (директор / dev) с датой и commit.

## Вне scope

- Prod ЮKassa; prod gating; Partner P1–P8.

## Ссылки

- [commerce-модуль-тз-mvp §13–§14](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)
- [ADR-001](../../_telotron.ru/docs/Техдок/00-мета/архитектурные-решения/ADR-001-scope-billing-partner-01-08.md)

## Журнал

### 2026-06-12

- Подтикет эпика T-026.
