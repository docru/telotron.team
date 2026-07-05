# T-076 · Pro · онбординг — устойчивость к смене UI (checklist vs tour)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Приоритет** | **P2** (техдолг UX; не блокер activation, но снижает стоимость T-065 / T-055 / рефакторинга навигации) |
| **Спринт** | этап 1 · пилот (после [T-060](../сделано/T-060-pro-onboarding-k-p.md) или параллельно с [T-065](T-065-pro-onboarding-порядок-подготовка-клиент.md)) |
| **Оценка** | **10–14 ч** (рефакторинг конфига + деградация spotlight + контракт-тесты; без смены API) |
| **Роль** | dev (+ архитектор review) |
| **Создан** | 2026-07-05 |
| **Зависит от** | [T-060](../сделано/T-060-pro-onboarding-k-p.md) ✅ (базовый onboarding-bar в коде) |

## Контекст

Pro onboarding (контуры **К** и **П**) уже разделён на:

| Слой | Где | Стабильность |
|------|-----|--------------|
| **Чеклист (goal)** | `TrainerOnboardingStatusResolver` (PHP), `GET /me/onboarding` | высокая — done по фактам продукта |
| **Тур (guide)** | `onboarding-config.ts`, `data-onboarding-target`, `contextualTargets` | низкая — ломается при переносе UI |

При рефакторинге Pro ([T-055](../в-работе/T-055-ux-обновление-pro-client-волна1.md)), смене порядка шагов ([T-065](T-065-pro-onboarding-порядок-подготовка-клиент.md)) или переносе «Пригласить» / назначений на другие страницы приходится править разросшийся `ONBOARDING_SHELL_CONFIG` и разбросанные `data-onboarding-target`.

**Цель:** перенос кнопки/раздела **не ломает** прогресс и coach-bar; spotlight может временно отключиться, но шаг остаётся рабочим.

**Канон прогресса не меняем:** [onboarding-api-pro.md](../../_telotron.ru/docs/Техдок/03-модули/onboarding-api-pro.md), [онбординг-тренера.md](../../_telotron.ru/docs/Бизнес-требования/02-модули/onboarding/онбординг-тренера.md).

## Принцип (зафиксировать в техдоке)

```text
Checklist  = id шага + status (API / PHP)     → источник истины
Tour       = куда вести + подсветка (TS)      → может деградировать
```

Кнопки «Понятно» / «Занятие создано» в bar — **UX**, не источник `done` (done только по данным/API).

## Что сделать

### 1. Реестр действий (action map)

Новый модуль, напр. `resources/ts/shared/composables/onboarding-actions.ts`:

- для каждого `stepId` (ключи из `onboarding-step-ids.ts` / PHP): **`action`** (`clients.invite`, `schedule.create`, …);
- **`routes`**: `{ name, query? }[]` — основной и альтернативные маршруты шага;
- **`anchor`**: string | null — семантический id подсветки (не CSS/DOM);
- **`fallbackLead`**: текст, если spotlight недоступен.

`ONBOARDING_SHELL_CONFIG` **сжать**: маршруты и targets берутся из action map; `contextualTargets` — только там, где без них нельзя (client hub, nested routes).

### 2. Якоря UI (anchor registry)

- Компоненты **регистрируют** якорь (`provideOnboardingAnchor('clients.invite', elementRef)`) вместо/поверх голого `data-onboarding-target`.
- `TelotronOnboardingSpotlight` / `useOnboardingBar`: resolve через реестр; **`data-onboarding-target`** оставить как thin alias на переходный период.
- Если anchor не найден: **не падать** — bar + CTA «Перейти в раздел» + `fallbackLead`; dev-only log (`onboarding-debug`).

### 3. Деградация tour

Правила для `ProOnboardingBar`:

1. anchor найден → spotlight;
2. anchor нет, route есть → bar без spotlight, primary CTA ведёт на route;
3. route нет → только `title`/`lead` из API + «Продолжить позже».

Spotlight **не блокирует** dismiss и навигацию по приложению.

### 4. Контракт step id (PHP ↔ TS)

- PHP: константы/id шагов в одном месте (`TrainerOnboardingStatusResolver` или `OnboardingStepRegistry`).
- TS: `assertOnboardingShellStepIds()` расширить — каждый id есть в **action map** и в PHP registry.
- Vitest/PHPUnit smoke: списки id **К** и **П** совпадают (можно snapshot JSON из seeder + TS enum).

### 5. E2E / feature — outcomes, не DOM

- Дополнить/скорректить сценарий [E2E-07-pro-onboarding.md](../../_telotron.ru/e2e/scenarios/E2E-07-pro-onboarding.md):
  - после действий пользователя `GET /me/onboarding` → шаг `done`;
  - **не** assert на наличие конкретного `data-onboarding-target` (хрупко).
- Feature-тест PHP: resolver + id registry без изменений контракта API.

### 6. Документация (кратко)

Добавить § **«Checklist vs tour»** в [onboarding-api-pro.md](../../_telotron.ru/docs/Техдок/03-модули/onboarding-api-pro.md) (5–10 строк + ссылка на action map).

## Критерии готовности

- [ ] `onboarding-actions.ts` (или экв.) — единая точка: stepId → routes + anchor + fallback.
- [ ] `ONBOARDING_SHELL_CONFIG` не дублирует маршруты; сложные `contextualTargets` только для шагов П с nested UI.
- [ ] Spotlight при отсутствии anchor: bar работает, нет console error в prod.
- [ ] Контракт-тест id шагов PHP ↔ TS green.
- [ ] E2E/ feature проверяют **status done** по API, не spotlight DOM.
- [ ] § в `onboarding-api-pro.md` обновлён.
- [ ] `npm run test:ts` / `php artisan test` (затронутые файлы) green.

## Вне scope

- Смена порядка шагов К/П — [T-065](T-065-pro-onboarding-порядок-подготовка-клиент.md).
- Post-reg баннер / опциональность мастера — [T-070](T-070-упрощение-входа-мастер-баннер.md).
- Server-driven navigation hints из API (можно идеей на потом).
- Client onboarding.

## Ссылки

- [T-060 Pro onboarding К+П](../сделано/T-060-pro-onboarding-k-p.md)
- [onboarding-config.ts](../../_telotron.ru/resources/ts/shared/composables/onboarding-config.ts)
- [TrainerOnboardingStatusResolver.php](../../_telotron.ru/app/Modules/Onboarding/Services/TrainerOnboardingStatusResolver.php)
- [ProOnboardingBar.vue](../../_telotron.ru/resources/ts/widgets/ProOnboardingBar.vue)

## Журнал

### 2026-07-05

- Тикет от архитектора: decouple checklist (API) от tour (UI), снизить хрупкость при переносе экранов.
