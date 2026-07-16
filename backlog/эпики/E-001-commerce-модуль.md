# E-001 · Commerce: модуль оплат, тарифов и купонов

| Поле | Значение |
|------|----------|
| **Статус** | `in_progress` · папка: **`эпики/`** (dev T-036 готов; stage sign-off — директор) |
| **Бывш. ID** | T-026 |
| **Приоритет** | P1 (stage ready ориентир **31.07–08**, prod платежей **01.09** · DEC-005) |
| **Спринт** | этап 1 · Пилот · спринты **2–5** |
| **Роль** | dev (+ архитектор на review слайсов) |
| **Создан** | 2026-06-12 |
| **Оценка** | **~80–95 ч** (1 FTE, ~10–15 ч/нед) |

## Контекст

Реализация модуля **`app/Modules/Commerce/`** по канону:

- [commerce-модуль-тз-mvp.md](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)
- [commerce-схема-данных-mvp.md](../../_telotron.ru/docs/Техдок/03-модули/commerce-схема-данных-mvp.md)
- [api-http §4.1m](../../_telotron.ru/docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md)
- [ADR-001 B1–B7](../../_telotron.ru/docs/Техдок/00-мета/архитектурные-решения/ADR-001-scope-billing-partner-01-08.md)
- [ADR-003](../../_telotron.ru/docs/Техдок/00-мета/архитектурные-решения/ADR-003-commerce-tovar-popolnenie-kupony.md) — товар, пополнение, купоны
- [ADR-004](../../_telotron.ru/docs/Техдок/00-мета/архитектурные-решения/ADR-004-commerce-po-уточнения-mvp.md) — уточнения PO 2026-07-08

**Вне эпика:** оплаты клиент→тренер; [автопополнение с карты](../идеи/commerce-автопополнение-с-карты.md). **Partner:** [E-002](E-002-partner-модуль.md) (только `TopupSucceeded` из Commerce). **Public `/tariffs`:** [техдолг](../../_telotron.ru/docs/Техдок/00-мета/техдолг-commerce-mvp.md).

**Зависимости не-dev:**

| Зависимость | Дедлайн | Блокирует |
|-------------|---------|-----------|
| [T-005](../бэклог/T-005-матрица-функция-тариф.md) черновик | 01.07 | gating (T-031) — временно канон-матрица |
| [T-024](../бэклог/T-024-reminders-одноразовый-лайтбокс.md) | до T-033 | лайтбокс при `light`/`frozen` |
| ЮKassa sandbox / stage webhook | 15.07 | T-029 на stage |
| Юр. тексты подписки | 01.07 | тексты в UI T-033 |

---

## Подтикеты (порядок)

| ID | Слайс | Спринт* | Оценка | Зависит от |
|----|-------|---------|--------|------------|
| [T-027](../бэклог/T-027-commerce-foundation-ledger.md) | Foundation: модуль, миграции, ledger | 2 | 12–16 ч | — |
| [T-028](../бэклог/T-028-commerce-тарифы-статусы-триал.md) | Тарифы, статусы, триал | 2–3 | 10–12 ч | T-027 |
| [T-029](../бэклог/T-029-commerce-платежи-yookassa.md) | Платежи + webhook | 3 | 10–14 ч | T-027, T-028 |
| [T-030](../бэклог/T-030-commerce-daily-debit-freeze.md) | Nightly debit + заморозка | 4 | 10–12 ч | T-028 |
| [T-031](../бэклог/T-031-commerce-gating-api.md) | TariffGate + HTTP API | 4 | 12–14 ч | T-028, T-005* |
| [T-032](../бэклог/T-032-commerce-купоны.md) | Купоны bonus/discount | 4 | 8–10 ч | T-027, T-029 |
| [T-035](../бэклог/T-035-commerce-напоминания-триала.md) | Напоминания 14/7/1 | 4 | 6–8 ч | T-028 |
| [T-033](../бэклог/T-033-commerce-pro-ui.md) | Pro UI «Тариф и счёт» | 4–5 | 12–16 ч | T-029, T-031, T-024 |
| [T-034](../бэклог/T-034-commerce-admin-filament.md) | Admin Filament | 5 | 8–12 ч | T-027…T-032 |
| ~~T-047~~ | Public `/tariffs` | — | — | **техдолг** · см. ниже |
| [T-036](../бэклог/T-036-commerce-stage-sign-off.md) | Stage sign-off, E2E, runbook | 5 | 6–8 ч | все выше |

\*Спринты — по [плану Пилота](../../_telotron.ru/docs/Техдок/00-мета/план-разработки-этап-1-пилот.md); неделя отпуска 06–12.07 без новых слайсов.

**Связанный (не подтикет эпика):** [T-024](../бэклог/T-024-reminders-одноразовый-лайтбокс.md) — Reminders, блокирует UX T-033.

---

## Критерии закрытия эпика E-001

Чеклист **ADR-001 Billing B1–B7** прогнан на **stage** (не prod):

Легенда: ☑ — покрыто автотестами / dev-доставкой; ☐ — нужен stage или prod.

- ☐ **B1** — ЮKassa sandbox: checkout, webhook, ошибки, логи `commerce_payment_webhook_logs` *(prod gate 01.09; PHPUnit — mock webhook)*
- ☑ **B2** — триал 30 дн., один на аккаунт; на триале **Профи**
- ☑ **B3** — Лайт + Профи; нехватка Ед. → freeze → light
- ☑ **B4** — gating: Лайт без групп; **только Лайт vs Профи**
- ☑ **B5** — напоминания триала 14/7/1 (T-035)
- ☑ **B6** — счёт Ед., nightly debit МСК, freeze
- ☑ **B7** — feature-тесты модуля + runbook §14 ТЗ + E2E «триал → пополнение → списание → light» (T-036 dev)
- ☑ **C+** — купоны bonus/discount; admin *(☑ PHPUnit/Filament)*; лайтбокс *(☐ T-024 stub, не prod UX)*

**Prod go/no-go** — отдельно **01.09**, не закрытие эпика.

---

## Дорожка (Mermaid)

```mermaid
flowchart TD
  T027[T-027 Foundation] --> T028[T-028 Тарифы]
  T028 --> T029[T-029 Платежи]
  T028 --> T030[T-030 Debit + Freeze]
  T028 --> T031[T-031 Gating + API]
  T028 --> T035[T-035 Trial reminders]
  T029 --> T032[T-032 Купоны]
  T029 --> T033[T-033 Pro UI]
  T031 --> T033
  T024[T-024 Reminders lightbox] --> T033
  T032 --> T034[T-034 Admin]
  T033 --> T036[T-036 Stage sign-off]
  T034 --> T036
  T030 --> T036
  T035 --> T036
```

---

## Журнал

### 2026-06-12

- Эпик и подтикеты T-027…T-036 созданы по канону Commerce и плану этапа 1 Пилот.

### 2026-07-08 (уточнения PO)

- [ADR-004](../../_telotron.ru/docs/Техдок/00-мета/архитектурные-решения/ADR-004-commerce-po-уточнения-mvp.md): Профи 3000 ₽; max — заглушка; freeze 10 дн./эпизод (без годового лимита); купоны individual/promotional; даунгрейд сам; Partner — только событие.
- T-047 → [техдолг](../../_telotron.ru/docs/Техдок/00-мета/техдолг-commerce-mvp.md).

### 2026-07-08

- Ссылка на [ADR-003](../../_telotron.ru/docs/Техдок/00-мета/архитектурные-решения/ADR-003-commerce-tovar-popolnenie-kupony.md); автопополнение — [идея](../идеи/commerce-автопополнение-с-карты.md).

### 2026-07-08 (T-036 dev)

- **T-036 dev-deliverable:** `CommerceLifecycleSignOffTest` (триал → webhook topup → `commerce:daily-debit` → freeze → light → gating); E2E `pro-commerce.flow.spec.ts`; [commerce-runbook-mvp.md](../../_telotron.ru/docs/Техдок/03-модули/commerce-runbook-mvp.md).
- Чеклист B1–B7 + C+ обновлён: ☑ автотесты/runbook/E2E smoke; ☐ B1 stage sandbox + director sign-off; ☐ лайтбокс T-024.
- Эпик **не** `done` — ждёт stage прогон с реальной ЮKassa и подпись директора.
