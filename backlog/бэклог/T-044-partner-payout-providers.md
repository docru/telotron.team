# T-044 · Partner: PayoutProvider и webhook задел

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` |
| **Эпик** | [T-037](T-037-partner-модуль-эпик.md) |
| **Спринт** | 5 |
| **Оценка** | 6–8 ч |
| **Зависит от** | [T-043](T-043-partner-вывод-admin.md) |

## Критерии готовности

- [ ] `PayoutProviderInterface` + `ManualPayoutProvider` (production path в MVP).
- [ ] `YooKassaPayoutProvider` — stub / disabled в config.
- [ ] Admin approve → channel `provider` вызывает adapter (mock в тестах).
- [ ] `POST /api/v1/webhooks/payouts/{provider}` + `partner_payout_webhook_logs`.
- [ ] Unit-тест manual provider; webhook идемпотентность.

## Журнал

### 2026-06-12

- Подтикет T-037 · prod API payout — когда договор ЮKassa.
