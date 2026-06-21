# T-028 · Commerce: тарифы, статусы, триал

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [T-026](T-026-commerce-модуль-эпик.md) |
| **Приоритет** | P1 |
| **Спринт** | 2–3 |
| **Роль** | dev |
| **Создан** | 2026-06-12 |
| **Оценка** | 10–12 ч |
| **Зависит от** | [T-027](T-027-commerce-foundation-ledger.md) |

## Контекст

Логика тарифов и статусов счёта: `trial` / `active` / `light` / `frozen`, `effective_tariff`, история смен тарифа. Читает `trial_ends_at` из `trainer_profiles` (A10).

## Критерии готовности

- [ ] `TariffPriceService` — активные цены из `commerce_tariff_prices`, `daily_rate_units`.
- [ ] `TrainerTariffService` — смена тарифа (новая строка `commerce_trainer_tariffs`, деактивация предыдущей).
- [ ] `CommerceStatusResolver` — вычисление `status` и `effective_tariff` (триал → `pro`; конец триала → `light` и т.д.).
- [ ] `TrialService` (расширение A10): один триал на аккаунт; 60 дней по настройке.
- [ ] Переход в `light` при нехватке Ед. (логика без nightly job — job в T-030).
- [ ] Unit/feature-тесты: триал → effective_tariff=pro; end trial → light; смена тарифа → история.

## Вне scope

- Nightly debit, freeze, API, UI.

## Ссылки

- [commerce-модуль-тз-mvp §3, §5](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)
- [commerce-схема §13](../../_telotron.ru/docs/Техдок/03-модули/commerce-схема-данных-mvp.md)

## Журнал

### 2026-06-12

- Подтикет эпика T-026.
