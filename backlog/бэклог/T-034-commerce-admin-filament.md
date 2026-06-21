# T-034 · Commerce: Admin Filament

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [T-026](T-026-commerce-модуль-эпик.md) |
| **Приоритет** | P1 |
| **Спринт** | 5 (27.07–09.08) |
| **Роль** | dev |
| **Создан** | 2026-06-12 |
| **Оценка** | 8–12 ч |
| **Зависит от** | T-027…T-032 |

## Контекст

Минимальная админка для эксплуатации Commerce на stage и prod ([ТЗ §10](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)).

## Критерии готовности

- [ ] Filament: правка цен → новая строка `commerce_tariff_prices` (деактивация предыдущей).
- [ ] Ручное начисление Ед.: сумма, комментарий, admin user → `commerce_transactions` type `admin_adjustment`.
- [ ] Заморозка / разморозка тренера → `commerce_freezes`.
- [ ] Просмотр `commerce_payment_webhook_logs` (фильтр по provider, payment).
- [ ] CRUD купонов: код, тип, параметры, `starts_at`, `expires_at`, деактивация.
- [ ] Smoke: admin action → отражается в API тренера.

## Вне scope

- Partner admin; полный billing analytics.

## Ссылки

- [commerce-модуль-тз-mvp §10](../../_telotron.ru/docs/Тechдok/03-модули/commerce-модуль-тз-mvp.md)

## Журнал

### 2026-06-12

- Подтикет эпика T-026.
