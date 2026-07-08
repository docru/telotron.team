# T-034 · Commerce: Admin Filament

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [E-001](../эпики/E-001-commerce-модуль.md) |
| **Приоритет** | P1 |
| **Спринт** | 5 (27.07–09.08) |
| **Роль** | dev |
| **Создан** | 2026-06-12 |
| **Оценка** | 8–12 ч |
| **Зависит от** | T-027…T-032 |

## Контекст

Минимальная админка для эксплуатации Commerce на stage и prod ([ТЗ §10](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)).

## Критерии готовности

- [ ] Filament: группа **Commerce** — см. [commerce-admin-filament-mvp](../../_telotron.ru/docs/Техдок/03-модули/commerce-admin-filament-mvp.md).
- [ ] Цены → новая строка `commerce_tariff_prices`.
- [ ] Ручное начисление Ед. → `admin_adjustment` (comment required).
- [ ] Freeze / unfreeze на view тренера.
- [ ] Webhook logs + payments read-only.
- [ ] CRUD купонов (individual auto-code).
- [ ] Shield permissions; smoke по §9 админ-дока.

## Вне scope

- Partner admin; полный billing analytics.

## Ссылки

- [commerce-admin-filament-mvp](../../_telotron.ru/docs/Техдок/03-модули/commerce-admin-filament-mvp.md)
- [commerce-модуль-тз-mvp §10](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)

## Журнал

### 2026-06-12

- Подтикет эпика E-001.
