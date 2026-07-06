# T-091 · Nutrition diary v2: outbox, доки, sign-off

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Приоритет** | P1 |
| **Эпик** | [E-005](../эпики/E-005-nutrition-diary-v2.md) |
| **Оценка** | **6–8 ч** |
| **Зависит от** | [T-088](T-088-nutrition-diary-v2-schema-api.md), [T-089](T-089-nutrition-diary-v2-client-ui.md) |
| **Создан** | 2026-07-06 |

## Контекст

Офлайн-очередь и приёмка эпика. Без working offline дневник регрессирует относительно MVP.

## Outbox

- Новые типы или маппинг: create/update/delete dish, clear slot, photo upload
- `executor.ts` + `outbox-acceptance.test.ts`
- Idempotency + local negative ids для слотов/блюд
- Last-write-wins на текст блюда

## Документация

- [nutrition-питание-схема-данных-mvp.md](../../_telotron.ru/docs/Техдок/03-модули/nutrition-питание-схема-данных-mvp.md) §5
- [api-http-контракт-mvp.md](../../_telotron.ru/docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md) §4.1j
- [трекер.md](../../_telotron.ru/docs/Бизнес-требования/02-модули/m7-m13-трекер-и-вес/трекер.md) §2 — критерии приёмки

## Критерии готовности

- [ ] `MvpReleaseAcceptanceTest` nutrition-сценарий обновлён
- [ ] `npm run test:ts` outbox acceptance зелёный
- [ ] `php artisan test` Nutrition feature suite зелёный
- [ ] PO sign-off чеклист E-005 в журнале эпика
