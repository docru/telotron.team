# T-029 · Commerce: платежи — провайдер, ЮKassa, webhook

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [T-026](T-026-commerce-модуль-эпик.md) |
| **Приоритет** | P1 |
| **Спринт** | 3 (29.06–05.07) |
| **Роль** | dev |
| **Создан** | 2026-06-12 |
| **Оценка** | 10–14 ч |
| **Зависит от** | [T-027](T-027-commerce-foundation-ledger.md), [T-028](T-028-commerce-тарифы-статусы-триал.md) |

## Контекст

Checkout и зачисление через абстракцию провайдера. MVP — **`YooKassaPaymentProvider`**. Webhook провайдер-агностичен: `POST /api/v1/webhooks/payments/{provider}`.

## Критерии готовности

- [ ] `config/commerce/payment-providers.php` (enabled, default `yookassa`, env-секреты).
- [ ] `PaymentProviderInterface` + `YooKassaPaymentProvider` (create checkout, parse webhook, verify signature).
- [ ] `PurchaseService`: quote + create payment; пакеты **кратно 30 дням**; запись `commerce_payments` (`provider`, `provider_payment_id`, `checkout_url`, `provider_payload`).
- [ ] Webhook handler: идемпотентность по `(provider, provider_payment_id)`; успех → `topup` + `succeeded`; лог `commerce_payment_webhook_logs`.
- [ ] API: `POST .../purchase/quote`, `POST .../purchase` (§4.1m); опц. `provider` в теле.
- [ ] Feature-тест с **mock** `PaymentProviderInterface`; unit-тест адаптера ЮKassa (без сети или VCR).
- [ ] Stage: sandbox ЮKassa + webhook URL (сисадмин) — smoke в журнале тикета.

## Вне scope

- Купоны на checkout (T-032), prod keys, возвраты.

## Ссылки

- [commerce-модуль-тз-mvp §7](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)
- [api-http §4.1m](../../_telotron.ru/docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md)

## Журнал

### 2026-06-12

- Подтикет эпика T-026.
