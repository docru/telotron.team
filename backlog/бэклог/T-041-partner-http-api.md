# T-041 · Partner: HTTP API §4.1n (P3, P5)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` |
| **Эпик** | [E-002](../эпики/E-002-partner-модуль.md) |
| **Спринт** | 4–5 |
| **Оценка** | 8–10 ч |
| **Зависит от** | [T-038](T-038-partner-foundation-config.md), [T-040](T-040-partner-commission-topup.md) |

## Критерии готовности

- [ ] `GET /api/v1/me/partner` — договор, `max_withdraw_units`, reserve, month aggregates.
- [ ] `GET /api/v1/me/partner/referrals` — пагинация; кампания, дата, status (trial/paying).
- [ ] `GET /api/v1/me/partner/stats?month=YYYY-MM` — L1/L2/L3 sums + event counts **без ПД**.
- [ ] Канон в [api-http §4.1n](../../_telotron.ru/docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md).
- [ ] Feature-тесты контрактов JSON.

## Журнал

### 2026-06-12

- Подтикет E-002 · ADR P3, P5.
