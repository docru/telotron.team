# T-032 · Commerce: купоны bonus / discount

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [E-001](../эпики/E-001-commerce-модуль.md) |
| **Приоритет** | P1 |
| **Спринт** | 4 |
| **Роль** | dev |
| **Создан** | 2026-06-12 |
| **Оценка** | 8–10 ч |
| **Зависит от** | [T-027](T-027-commerce-foundation-ledger.md), [T-029](T-029-commerce-платежи-yookassa.md) |

## Контекст

- **`bonus` / `discount`** + **`individual` / `promotional`** (ADR-004).
- Пополнение: **`units_to_credit` ≥ min_topup_rub** (1000), не привязано к тарифу — см. журнал ТЗ 2026-07-08.

## Критерии готовности

- [ ] `CouponService`: `scope`; promotional — admin code + `max_redemptions`; individual — генерация 8 символов; UK redemption на тренера.
- [ ] `bonus`: немедленное зачисление → `commerce_transactions` type `coupon_bonus`.
- [ ] `discount`: привязка; quote/purchase со смешанной ценой; `remaining_budget_units` на active; `commerce_coupon_redemptions`.
- [ ] API: `POST .../coupons/apply`, `DELETE .../coupons/active`; просроченный купон → **422**.
- [ ] Feature-тесты: bonus; discount частично; `valid_days_after_activation` истёк → purchase без скидки / 422 на apply.

## Вне scope

- Partner-скидка S; admin CRUD (T-034).

## Ссылки

- [commerce-модуль-тз-mvp §6](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)
- [commerce-схема §9](../../_telotron.ru/docs/Техдок/03-модули/commerce-схема-данных-mvp.md)

## Журнал

### 2026-06-12

- Подтикет эпика E-001.

### 2026-07-08

- Канон: bonus/discount; срок после активации; пополнение без привязки к тарифу.

### 2026-07-08 (scope)

- ADR-004: `individual` / `promotional`.
