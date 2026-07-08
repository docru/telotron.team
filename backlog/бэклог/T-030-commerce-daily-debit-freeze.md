# T-030 · Commerce: nightly debit и заморозка

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [E-001](../эпики/E-001-commerce-модуль.md) |
| **Приоритет** | P1 |
| **Спринт** | 4 (13–26.07) |
| **Роль** | dev |
| **Создан** | 2026-06-12 |
| **Оценка** | 10–12 ч |
| **Зависит от** | [T-028](T-028-commerce-тарифы-статусы-триал.md) |

## Контекст

Ежедневное списание по **Europe/Moscow** и заморозка аккаунта. При новом эпизоде `light`/`frozen` — вызов `OneTimeLightboxService::schedule` ([T-024](T-024-reminders-одноразовый-лайтбокс.md)).

## Критерии готовности

- [ ] `DailyDebitJob`: платный тариф, не в freeze; `balance >= daily_rate` → списание; иначе флаг нехватки (freeze с D+1, ADR-004).
- [ ] Идемпотентность: UK `(trainer_user_id, debit_date)` в `commerce_daily_debits`.
- [ ] `FreezeService`: `planned_end_date`, `trial_ended`; лимиты `config/commerce/commerce.php` → `freeze`; по окончании без оплаты → `light`.
- [ ] Scheduler: cron МСК (на stage — ручной запуск + тест).
- [ ] При переходе в `light`/`frozen` (новый эпизод) — `OneTimeLightboxService::schedule(..., prompt_key=commerce.suspension)` (если T-024 готов; иначе stub + тест с mock).
- [ ] Feature-тесты: debit ok; insufficient → freeze → light; лимит 10 дн./эпизод; годовой лимит; повтор job за дату — без дубля.

## Вне scope

- Admin UI freeze (T-034), prod cron.

## Ссылки

- [commerce-модуль-тз-mvp §4.3, §5](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)
- [reminders-одноразовый-лайтбокс-mvp §4](../../_telotron.ru/docs/Техдок/03-модули/reminders-одноразовый-лайтбокс-mvp.md)

## Журнал

### 2026-06-12

- Подтикет эпика E-001.

### 2026-07-08

- ADR-004: freeze → light; лимиты в конфиге.
