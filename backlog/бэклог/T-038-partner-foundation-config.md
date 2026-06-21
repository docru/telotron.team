# T-038 · Partner: foundation и config

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` |
| **Эпик** | [T-037](T-037-partner-модуль-эпик.md) |
| **Спринт** | 4 |
| **Оценка** | 8–10 ч |

## Критерии готовности

- [ ] `app/Modules/Partner/` — каркас модуля.
- [ ] Миграции: `partner_profiles`, `partner_commissions`, `partner_payout_methods`, `partner_withdrawal_requests`, `partner_payout_webhook_logs` ([схема §11](../../_telotron.ru/docs/Техдок/03-модули/partner-схема-данных-mvp.md)).
- [ ] `config/partner/withdrawal.php` — `min_amount_rub` => **1000**, `reserve_days` => **30**.
- [ ] `config/partner/commission-rates.php` — L1/L2/L3.
- [ ] `config/partner/payout-providers.php` — enabled: **`manual`** only.
- [ ] `config/partner/invite-limits.php` — `max_active_without_contract` => 1.
- [ ] Factory + smoke-тест создания `partner_profiles`.

## Журнал

### 2026-06-12

- Подтикет T-037.
