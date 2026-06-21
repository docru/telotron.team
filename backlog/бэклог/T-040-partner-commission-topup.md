# T-040 · Partner: начисления L1/L2/L3 на topup (P4)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` |
| **Эпик** | [T-037](T-037-partner-модуль-эпик.md) |
| **Спринт** | 4–5 |
| **Оценка** | 12–14 ч |
| **Зависит от** | [T-038](T-038-partner-foundation-config.md), [T-029](T-029-commerce-платежи-yookassa.md) |

## Критерии готовности

- [ ] `CommissionService`: слушатель `TopupSucceeded` (Commerce).
- [ ] Обход `referral_attributions` до 3 предков; L1 **20%**, L2 **5%**, L3 **2,5%**.
- [ ] L3 только если у beneficiary `partner_profiles.contract_signed_at` set.
- [ ] Skip: `platform_trainer_recruitment` attribution; base = 0.
- [ ] Атомарно: `commerce_accounts.balance` ↑ + `commerce_transactions` `partner_commission` + `partner_commissions` row.
- [ ] UK идемпотентности ([схема §3](../../_telotron.ru/docs/Техдок/03-модули/partner-схема-данных-mvp.md)).
- [ ] Feature-тест: A→B→C topup → commissions; platform invite topup → 0; L3 без договора → нет L3.

## Журнал

### 2026-06-12

- Подтикет T-037 · ADR P4, P8.
