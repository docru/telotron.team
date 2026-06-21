# T-027 · Commerce: foundation — модуль, миграции, ledger

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [T-026](T-026-commerce-модуль-эпик.md) |
| **Приоритет** | P1 |
| **Спринт** | 2 (15–28.06) |
| **Роль** | dev |
| **Создан** | 2026-06-12 |
| **Оценка** | 12–16 ч |

## Контекст

Первый слайс Commerce: каркас модуля, все таблицы по [схеме §15](../../_telotron.ru/docs/Техдок/03-модули/commerce-схема-данных-mvp.md), сервис проводок. Без платежей и UI.

## Критерии готовности

- [ ] `app/Modules/Commerce/` — структура (Models, Services, Providers, routes placeholder).
- [ ] Миграции в порядке схемы: `commerce_tariff_prices`, `commerce_accounts`, `commerce_trainer_tariffs`, `commerce_transactions`, `commerce_payments`, `commerce_coupons`, `commerce_coupon_redemptions`, `commerce_freezes`, `commerce_daily_debits`, `commerce_payment_webhook_logs`.
- [ ] Сидер начальных цен (`light`=0, `pro`, `max`).
- [ ] Backfill `commerce_accounts` + начальный тариф для существующих `trainer_profiles`.
- [ ] `CommerceAccountService`: создание счёта, атомарная проводка (`balance_units` + `commerce_transactions` в одной DB-транзакции).
- [ ] Factory `CommerceAccount` для тестов.
- [ ] Feature-тест: регистрация тренера → счёт создан; проводка меняет баланс и пишет ledger.

## Вне scope

- HTTP API, платежи, jobs, gating, UI.

## Ссылки

- [commerce-схема-данных-mvp](../../_telotron.ru/docs/Техдок/03-модули/commerce-схема-данных-mvp.md)
- [commerce-модуль-тз-mvp §4.4, §12](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)

## Журнал

### 2026-06-12

- Подтикет эпика T-026.
