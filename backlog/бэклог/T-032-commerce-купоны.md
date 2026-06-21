# T-032 · Commerce: купоны A/B

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [T-026](T-026-commerce-модуль-эпик.md) |
| **Приоритет** | P1 |
| **Спринт** | 4 |
| **Роль** | dev |
| **Создан** | 2026-06-12 |
| **Оценка** | 8–10 ч |
| **Зависит от** | [T-027](T-027-commerce-foundation-ledger.md), [T-029](T-029-commerce-платежи-yookassa.md) |

## Контекст

Купоны тип **A** (бонус Ед.) и **B** (скидка на пакет, частичное использование, смешанная цена). Срок действия: `starts_at`, **`expires_at`** (null = без срока).

## Критерии готовности

- [ ] `CouponService`: apply / active / remove; проверка `starts_at`, `expires_at`, лимитов, `is_active`.
- [ ] Тип A: немедленное зачисление → `commerce_transactions` type `coupon_bonus`.
- [ ] Тип B: привязка активного купона; расчёт quote/purchase со смешанной ценой; списание `remaining_budget_units`; `commerce_coupon_redemptions`.
- [ ] API: `POST .../coupons/apply`, `DELETE .../coupons/active`; просроченный купон → **422**.
- [ ] Feature-тесты: A начисление; B частичная скидка; expires_at в прошлом → 422.

## Вне scope

- Partner-скидка S; admin CRUD (T-034).

## Ссылки

- [commerce-модуль-тз-mvp §6](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)
- [commerce-схема §9](../../_telotron.ru/docs/Техдок/03-модули/commerce-схема-данных-mvp.md)

## Журнал

### 2026-06-12

- Подтикет эпика T-026.
