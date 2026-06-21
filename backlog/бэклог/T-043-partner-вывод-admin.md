# T-043 · Partner: вывод, reserve, admin manual (P6–P7)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` |
| **Эпик** | [T-037](T-037-partner-модуль-эпик.md) |
| **Спринт** | 5 |
| **Оценка** | 10–12 ч |
| **Зависит от** | [T-040](T-040-partner-commission-topup.md), [T-041](T-041-partner-http-api.md), [T-042](T-042-partner-договор-legal.md) |

## Критерии готовности

- [ ] `WithdrawalService`: `max_withdraw = balance − 30×daily_rate`; min **1000** ₽; **422** без договора.
- [ ] `POST/GET /me/partner/withdrawals` + `idempotency_key`.
- [ ] `POST /me/partner/payout-methods` — placeholder для token (MVP: manual label ok).
- [ ] Filament: очередь `pending_accountant`; approve → **manual** → `paid` + `partner_withdrawal` ledger.
- [ ] Списание balance при `paid`.
- [ ] Feature-тест: reserve, min amount, full flow manual.

## Журнал

### 2026-06-12

- Подтикет T-037 · ADR P6, P7.
