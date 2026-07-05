# T-060 · Pro · онбординг тренера (краткий К + полный П)

| Поле | Значение |
|------|----------|
| **Статус** | `done` (core) · папка: **`в-работе/`** → перенос в `сделано/` после merge [T-076](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md) |
| **Приоритет** | **P1** (activation пилота; ниже P0 prod и billing stage) |
| **Спринт** | **2–3** (после slice billing foundation или параллельно при capacity) |
| **Роль** | **дизайнер** (макет + copy UI) → **dev** (+ PO ревью текстов) |
| **Создан** | 2026-06-16 |
| **Оценка** | **~16–24 ч** (3–4 раб. дня при 10–15 ч/нед) |

## Контекст

После регистрации Pro тренер сразу попадает в [расписание](_telotron.ru/resources/ts/app/pro/router/routes.ts) — без маршрута «что делать дальше». Регистрация (legal → MAX/TG/email → Passkey) **уже есть**; **пост-регистрационного мастера нет**.

**Зачем:** KPI пилота — **activation** ([§1.3 плана продвижения](../../02-Маркетолог/План%20продвижения%20—%20этап%201%20Пилот.md)): реальный клиент + занятие в календаре **или** план. Онбординг **ведёт** к тем же действиям, **не блокирует** продукт.

**Канон:** [_telotron.ru/docs/Бизнес-требования/02-модули/onboarding/онбординг-тренера.md](../../_telotron.ru/docs/Бизнес-требования/02-модули/onboarding/онбординг-тренера.md) — два контура **К** и **П**, можно пропустить.

**Тексты UI:** простой язык, ориентир — [Онбординг — инструкция для тренеров.md](../../02-Маркетолог/Инструкции/онбординг-тренеров/Онбординг%20—%20инструкция%20для%20тренеров.md) (маркетинг; не дублировать Word в коде).

**Вне scope тикета:** Word/pandoc для тренеров, Filament-отчёт activation ([T-050](T-050-спринт2-воронка-метрики.md) — отдельно).

---

## Решение

### Два контура

| Контур | Когда | UX |
|--------|-------|-----|
| **Краткий К** | первый вход после reg (пока не dismiss) | **coach-bar** + spotlight в shell; обзор на `/more/onboarding` |
| **Полный П** | после dismiss К или когда К закрыт | тот же coach-bar («Расширенная настройка») + пункт в «Ещё» |

**Реализованный паттерн (2026-06):** не full-page чеклист на `/onboarding`, а **единый движок** `ProOnboardingBar` + `TelotronOnboardingSpotlight`. Legacy `/onboarding`, `/onboarding/full` — редиректы в продукт. Канон: [онбординг-тренера.md](../../_telotron.ru/docs/Бизнес-требования/02-модули/onboarding/онбординг-тренера.md) §4, [E2E-07](../../_telotron.ru/e2e/scenarios/E2E-07-pro-onboarding.md).

**Checklist vs tour ([T-076](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md), 2026-07):**

```text
Checklist = id шага + status (PHP / GET /me/onboarding)  → источник истины done
Tour      = маршруты + подсветка (TS action map)         → может деградировать без потери прогресса
```

Кнопки «Понятно» / «Занятие создано» в bar — **UX-подтверждение**, не источник `done` (только факты в БД).

### Шаги

| ID | Контур | Заголовок (черновик) | Done when | Deep link |
|----|--------|----------------------|-----------|-----------|
| `welcome` | К | Настройка за 15 минут | просмотр / CTA «Начать» | расписание |
| `install_pwa` | К | Установите на телефон | dismiss install banner **или** переход в «Ещё» → install | `/more` |
| `invite_client` | К | Пригласите первого клиента | ≥1 клиент в `trainer_clients` (вкл. self-link) | `/clients` |
| `schedule_or_plan` | К | Занятие в календаре | ≥1 **appointment** у тренера (назначение плана **не** закрывает шаг — MVP) | `/schedule` |
| `create_group` | К, **опц.** | Группа (если ведёте) | ≥1 group **или** skip шага | `/groups` |
| `create_exercise` | П | Упражнение | ≥1 exercise в базе | `/workouts?tab=exercises` |
| `create_complex` | П | Комплекс | ≥1 complex template | `/workouts?tab=complexes` |
| `create_program` | П | Программа тренировок | ≥1 program template | `/workouts?tab=programs` |
| `assign_program` | П | Назначьте программу | ≥1 workout assignment | `/clients` (hub) |
| `partner_invite` | П | Партнёрская ссылка | ≥1 активная `specialist_referral` ссылка | `/more/invites` |
| `nutrition_file` | П | План питания файлом | ≥1 nutrition assignment | `/plans` |
| `feedback` | П | Обратная связь | ≥1 feedback report | `/feedback` |

Прогресс: К — **4** шага (`welcome` не входит); П — **7** шагов. Id синхронизированы: `OnboardingStepRegistry.php` ↔ `onboarding-step-ids.ts`.

**Пилот:**

- **Не упоминать тарифы** в copy онбординга.
- Шаг `create_group` **показывать всем** (gating по тарифам в prod ещё нет).
- **Не блокировать** навигацию: «Пропустить» / «Позже» на К и на баннере П.

**Activation:** критерий «реальный клиент, не тестовый» — как в §1.3 плана; если в коде нет флага test client, **уточнить у PO** перед merge (не считать demo-аккаунты).

---

## Дизайнерские решения

> Канон визуала: [Система стилей Pro/Client](../../08-Дизайнер/Инструкции/Система%20стилей%20—%20Pro%20и%20Client%20(MVP).md), [Спецификация экранов MVP §9](../../08-Дизайнер/Инструкции/Спецификация%20экранов%20MVP.md).  
> Ориентир по смыслу шагов: [Онбординг — инструкция для тренеров.md](../../02-Маркетолог/Инструкции/онбординг-тренеров/Онбординг%20—%20инструкция%20для%20тренеров.md) (скрины `Инструкции/скрины/06`, `08` — **не** копировать Word, только визуальные референсы).

### Принципы (обязательные)

1. **Не блокируем продукт** — онбординг **не** modal-блокер «пройди всё или выйди»; навигация shell (табы) доступна всегда.
2. **Краткий К — activation за 15–30 мин**, не курс из 10 экранов; один экран-чеклист предпочтительнее пошагового wizard.
3. **Простой язык** — без жаргона разработки («resolver», «assignment»); формулировки как в инструкции для тренеров, но короче (1–2 строки lead на шаг).
4. **Mobile-first, Pro density** — `theme-pro`, `telotron-h1/h2`, `body-sm`; primary CTA виден на **360px** без прокрутки на экране welcome.
5. **Без тарифов и оплаты** в copy и иллюстрациях.
6. **Reuse, не новый дизайн-системы слой** — `TelotronCard`, pill-кнопки Pro, Lucide-иконки; **не** отдельная «маркетинговая» тема.

### Краткий К — паттерн UI (факт)

| Решение | Значение |
|---------|----------|
| **Формат** | **Coach-bar** в Pro shell (`ProOnboardingBar`) + spotlight; не отдельный full-page route |
| **Обзор** | `WorkspaceOnboardingPage` — `/more/onboarding` (чеклист К и П, «Продолжить» / reopen) |
| **Legacy** | `/onboarding` → расписание; `/onboarding/full` → workouts (exercises tab) |
| **Welcome** | Первый шаг bar: H1 «Настройка за 15 минут»; CTA **«Начать настройку»** |
| **Прогресс** | `onboarding-bar-progress`: **`N из M`** в bar |
| **Skip всего** | `onboarding-brief-skip-all` в bar |
| **Skip шага** | `onboarding-bar-skip-step` / `onboarding-welcome-later` на опциональных шагах |
| **После dismiss К** | Bar П («Расширенная настройка»); автопоказ К не повторяется |

> **Историческая постановка (2026-06-16):** wireframe full-page чеклиста на `/onboarding` — **не реализован**; заменён coach-bar (см. журнал 2026-06-21). Карточки шагов — на hub `/more/onboarding`, не в отдельном wizard.

### Карточка шага (анатомия)

Единый компонент `.telotron-onboarding-step` (имя для dev):

```
┌─ TelotronCard ─────────────────────────────┐
│ [icon]  Заголовок шага          [✓ done]  │
│         Lead 1–2 строки, muted             │
│         [ Primary CTA → deep link ]        │
│         Позже  (только если опционально)   │
└────────────────────────────────────────────┘
```

| Состояние | Визуал |
|-----------|--------|
| **pending** | обычная карточка, primary CTA активен |
| **done** | `border-success/30`, иконка **Check** зелёная, CTA → **«Готово»** disabled или «Открыть снова» ghost |
| **skipped** | muted border, без акцента (только для явного skip опционального шага) |

### Маппинг шагов К → UI

| ID | Иконка (Lucide) | Заголовок (UI) | Lead (черновик) | Primary CTA | Примечание |
|----|-----------------|----------------|-----------------|-------------|------------|
| `welcome` | `Sparkles` или logo mark | Добро пожаловать | «За 15–30 минут пригласите клиента и поставьте занятие или план.» | **Начать** | без deep link |
| `install_pwa` | `Smartphone` | Установите на телефон | «Открывайте кабинет с главного экрана — как обычное приложение.» | **Установить** → `/install` | опционально; **«Позже»** |
| `invite_client` | `UserPlus` | Пригласите первого клиента | «Отправьте ссылку **реальному** клиенту — так увидите продукт в работе.» | **Пригласить** → `/clients` или `/more` | акцент activation |
| `schedule_or_plan` | `CalendarDays` | Занятие или план | «Поставьте занятие в календаре **или** назначьте план тренировок.» | **Открыть календарь** / secondary **Планы** | два CTA допустимы |
| `create_group` | `Layers` | Группа (если ведёте) | «Создайте группу, если работаете с несколькими клиентами сразу.» | **Создать группу** → `/groups` | **опц.**; явный **«Пропустить шаг»** |

**Шаг `install_pwa`:** переиспользовать copy из [TelotronInstallBanner.vue](_telotron.ru/resources/ts/widgets/TelotronInstallBanner.vue) / `voiceForZone('pro')`, не писать второй текст.

**Шаг `invite_client`:** если к моменту реализации в [T-055](../в-работе/T-055-ux-обновление-pro-client-волна1.md) появится inline-приглашение на `WorkspaceClientsPage` — deep link туда; иначе `/more` + `ProInvitesPanel`.

### Полный П — паттерн UI (факт)

| Решение | Значение |
|---------|----------|
| **Формат** | Тот же **coach-bar** (`onboarding-full-bar`) после dismiss К |
| **Entry point 1** | Bar «Расширенная настройка» в shell |
| **Entry point 2** | `onboarding-more-entry` на [WorkspaceMorePage.vue](_telotron.ru/resources/ts/pages/workspace/WorkspaceMorePage.vue) + hub `/more/onboarding` |
| **Dismiss bar П** | `onboarding-full-dismiss` («Не сейчас») → `POST dismiss scope=full_banner` |
| **Тон** | Спокойный, без urgency; не блокер пилота |

### Маппинг шагов П → UI (факт в resolver)

| ID | Заголовок (UI) | Lead (факт) | CTA → |
|----|----------------|-------------|-------|
| `create_exercise` | Упражнение | Добавьте хотя бы одно упражнение в базу | `/workouts` |
| `create_complex` | Комплекс | Соберите комплекс: подходы, повторы | `/workouts` |
| `create_program` | Программа | Создайте программу из комплексов | `/workouts` |
| `assign_program` | Назначьте программу | Клиент → «Тренировки» → «Назначения» | `/clients` |
| `partner_invite` | Партнёрская ссылка | Раздел «Приглашения» в «Ещё» | `/more/invites` |
| `nutrition_file` | План питания | Библиотека «Планы» → назначение в карточке клиента | `/plans` |
| `feedback` | Обратная связь | Напишите, если что-то непонятно на пилоте | `/feedback` |

Маршруты и якоря spotlight — в `onboarding-actions.ts` ([T-076](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md)).

### Поведение после deep link

1. Тренер уходит по CTA в раздел продукта → выполняет действие → возвращается (back или таб **«Настройка»** / пункт меню).
2. При открытии экрана онбординга — **refetch**; выполненные шаги с анимацией **check** (лёгкая, без confetti).
3. Если все шаги К **done** — экран К больше не показывается автоматически (даже без dismiss).
4. **Конфликт с install-баннером:** пока активен экран К с шагом `install_pwa` pending — **не дублировать** [TelotronInstallBanner](_telotron.ru/resources/ts/widgets/TelotronInstallBanner.vue) на том же первом заходе (suppress в layout hook).

### Приоритет показа (первый вход)

```
auth OK → расписание + coach-bar К (если brief не dismissed и есть pending)
         → dismiss К → coach-bar П
         → hub /more/onboarding всегда доступен
         → one-time lightboxes [T-024] — после dismiss К или если К уже dismissed
```

### Деградация tour ([T-076](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md))

1. Якорь найден (`onboarding-anchor-registry`) → spotlight.
2. Якоря нет, route есть → bar + `onboarding-tour-fallback` + CTA «Перейти в раздел».
3. Route нет → только `title`/`lead` из API.

Spotlight **не блокирует** dismiss и навигацию по shell.

### Иллюстрации и скрины

| Вариант | Решение |
|---------|---------|
| **MVP (рекомендуется)** | Только **Lucide-иконки** + опционально **мини-скрин** 48–64px справа в карточке для `invite_client` / `schedule_or_plan` (кадры из `Инструкции/скрины/06`, `08`) |
| **Post-MVP** | Иллюстрация hero welcome — **не блокирует** slice 1–2 |
| **Запрещено** | Стоковые фото «тренер в зале»; медицинская символика |

### Deliverables дизайнера (slice 0)

- [ ] Wireframe / Figma: **Brief K** — mobile **360px** (обязательно), desktop **1280px** (желательно) — **отложено**; в проде coach-bar
- [x] Реализованный UX: coach-bar + hub (см. [E2E-07](../../_telotron.ru/e2e/scenarios/E2E-07-pro-onboarding.md))
- [ ] Таблица **финальных UI-текстов** — частично в resolver; PO-ревью по желанию

### Design QA (критерии приёмки визуала)

- [x] **«Пропустить настройку»** (`onboarding-brief-skip-all`) в bar
- [x] Контраст и touch targets — Lucide + Pro shell
- [x] Empty/error: `GET /me/onboarding` fail — тихий fail, shell работает
- [x] Термины UI: «Клиенты», «Расписание», «Тренировки»
- [x] Suppress `TelotronInstallBanner` при активном шаге `install_pwa` ([T-076](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md) не меняет это поведение)

---

## UX-правила

1. После auth: если `brief_onboarding_dismissed_at` пуст **и** есть pending шаги К → **coach-bar К** на расписании (не блокирует табы).
2. «Пропустить всё» → `POST dismiss scope=brief` → bar П; автопоказ К не повторяется.
3. Полный П: coach-bar + `onboarding-more-entry` в «Ещё» + hub `/more/onboarding`; «Не сейчас» → `full_banner` dismiss.
4. Шаги **auto-done** по refetch `GET /me/onboarding` после действий в продукте (источник истины — resolver).
5. PWA: `install_pwa` ведёт в «Ещё»; suppress [TelotronInstallBanner](_telotron.ru/resources/ts/widgets/TelotronInstallBanner.vue) при активном шаге.
6. Tour ([T-076](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md)): перенос UI не ломает progress; при отсутствии якоря — `fallbackLead` в bar.

---

## Backend

### Миграция `trainer_profiles`

- `brief_onboarding_dismissed_at` — nullable timestamp
- `full_onboarding_banner_dismissed_at` — nullable timestamp (скрыть баннер П)

### `TrainerOnboardingStatusResolver` + `OnboardingStepRegistry`

Вычисляет `status`: `pending` | `done` | `skipped` по каждому step id. Канонические id — `OnboardingStepRegistry.php` (контракт с TS `onboarding-step-ids.ts`, проверка в `assertOnboardingShellStepIds()`).

### API (Pro, `auth:sanctum`)

```
GET  /api/v1/me/onboarding
POST /api/v1/me/onboarding/dismiss   { "scope": "brief" | "full_banner" }
```

Ответ `GET` (черновик):

```json
{
  "data": {
    "brief": {
      "dismissed": false,
      "progress": { "done": 1, "total": 4 },
      "steps": [
        { "id": "welcome", "status": "done", "title": "…", "lead": "…", "href": null }
      ]
    },
    "full": {
      "banner_dismissed": false,
      "progress": { "done": 0, "total": 7 },
      "steps": [ … ]
    }
  }
}
```

Контракт: [onboarding-api-pro.md](../../_telotron.ru/docs/Техдок/03-модули/onboarding-api-pro.md) (§ Checklist vs tour — [T-076](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md)).

### Тесты

- Feature: `MeOnboardingApiTest` — новый тренер, invite, appointment, dismiss/reopen.
- Unit: `TrainerOnboardingStatusResolverTest`, `OnboardingStepRegistryTest`.

---

## Frontend (Pro)

| Артефакт | Назначение |
|----------|------------|
| `useTrainerOnboarding.ts` | load, dismiss, refresh, reopen |
| `useOnboardingBar.ts` | состояние coach-bar, spotlight, confirm |
| `ProOnboardingBar.vue` | coach-bar К и П (`onboarding-bar` / `onboarding-full-bar`) |
| `TelotronOnboardingSpotlight.vue` | подсветка якоря |
| `WorkspaceOnboardingPage.vue` | hub `/more/onboarding` (чеклисты К и П) |
| `onboarding-config.ts` | shell config (сжат; маршруты из action map) |
| `onboarding-actions.ts` | **T-076:** stepId → routes + anchor + `fallbackLead` |
| `onboarding-anchor-registry.ts` | **T-076:** семантические якоря UI |
| `onboarding-step-ids.ts` | id шагов К/П (контракт с PHP) |
| `onboarding-hints.ts` | contextual hints для nested UI |
| `App.vue` (pro) | provide onboarding, suppress install nudge |

**Не реализовано (заменено):** `ProBriefOnboardingPage`, `ProOnboardingStepCard`, `ProFullOnboardingPage`, `ProOnboardingShellBanner`.

**Vitest:** `useTrainerOnboarding.test.ts`, `onboarding-config.test.ts`, `useOnboardingBar.test.ts`, `onboarding-actions.test.ts`, `onboarding-anchor-registry.test.ts`.

---

## E2E и testid

Канон селекторов: [E2E-07-pro-onboarding.md](../../_telotron.ru/e2e/scenarios/E2E-07-pro-onboarding.md), spec `e2e/specs/pro-onboarding.flow.spec.ts`.

### Реализованные `data-testid` (coach-bar + hub)

| Элемент | `data-testid` |
|---------|----------------|
| Brief bar | `onboarding-bar` |
| Full bar | `onboarding-full-bar` |
| Bar shell | `onboarding-bar-shell` |
| Progress | `onboarding-bar-progress` |
| Primary CTA | `onboarding-bar-primary` |
| Пропустить К | `onboarding-brief-skip-all` |
| Не сейчас П | `onboarding-full-dismiss` |
| Tour fallback | `onboarding-tour-fallback` |
| Entry в «Ещё» | `onboarding-more-entry` |
| Hub | `workspace-onboarding-page` |
| Контур | `onboarding-contour-brief`, `onboarding-contour-full` |
| Шаг на hub | `onboarding-step-{scope}-{stepId}` |
| Spotlight | `onboarding-spotlight` |

### Правила assert ([T-076](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md))

- **Done** шага — по `GET /me/onboarding` (`status: done`), не по наличию spotlight/`data-onboarding-target`.
- **Не assert** на конкретный DOM-якорь tour — хрупко при рефакторинге UI.
- Историческая таблица testid для `ProBriefOnboardingPage` / `ProOnboardingStepCard` — **снята** (паттерн coach-bar).

### Критерий (закрыто)

- [x] Testid bar + hub по E2E-07.
- [x] Vitest smoke на bar и action map.
- [x] E2E-07 green в CI (при поднятом стеке).

---

## Подтикеты (порядок)

| Slice | Содержание | Статус |
|-------|------------|--------|
| **0** | Дизайн wireframe | отложено; в проде coach-bar |
| **1** | Миграция + resolver + API + PHP tests | ✅ |
| **2** | Coach-bar К + dismiss + deep links + E2E-07 | ✅ |
| **3** | Coach-bar П + hub + «Ещё» | ✅ |
| **4** | Vitest, E2E-07, design QA | ✅ |
| **+T-076** | Action map, anchor registry, деградация tour, контракт id PHP↔TS | в коде, merge pending |

---

## Критерии готовности (DoD)

- [ ] **Дизайн slice 0** (Figma) — отложено; не блокер activation.
- [x] После первого входа — **coach-bar К** с «Пропустить всё».
- [x] Dismiss на сервере; автопоказ К не повторяется.
- [x] `invite_client` auto-done при клиенте; `schedule_or_plan` — при **appointment** (не plan-only).
- [x] Hub **«Продолжить настройку»** + чеклист П в `/more/onboarding` и «Ещё».
- [x] Deep links + auto-done по API после действий.
- [x] Нет тарифов / оплаты в copy.
- [x] PHPUnit + Vitest green.
- [x] E2E-07; assert **done** по API ([T-076](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md)).
- [x] `data-testid` по E2E-07 (coach-bar + hub).
- [ ] Merge [T-076](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md) → перенос тикета в `сделано/`.

---

## Зависимости

| | |
|--|--|
| **Не блокирует** | [T-026](T-026-commerce-модуль-эпик.md) billing |
| **Стык** | activation метрики [T-004](T-004-оценка-привлечения-воронка.md), [T-050](T-050-спринт2-воронка-метрики.md) |
| **Параллель** | [T-055](../в-работе/T-055-ux-обновление-pro-client-волна1.md) UX — deep link «Пригласить»; [T-024](T-024-reminders-одноразовый-лайтбокс.md) — порядок показа после К |
| **Следующий слой** | [T-076](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md) устойчивость tour (в коде); [T-065](../бэклог/T-065-pro-onboarding-порядок-подготовка-клиент.md) порядок шагов |

---

## Ссылки

- [онбординг-тренера.md](../../_telotron.ru/docs/Бизнес-требования/02-модули/onboarding/онбординг-тренера.md)
- [Онбординг — инструкция для тренеров.md](../../02-Маркетолог/Инструкции/онбординг-тренеров/Онбординг%20—%20инструкция%20для%20тренеров.md) · PDF-сборка закрыта в [T-061](../сделано/T-061-онбординг-инструкция-тренеров-pdf.md)
- [TrainerProfile.php](../../_telotron.ru/app/Modules/Identity/Models/TrainerProfile.php)
- [onboarding-api-pro.md](../../_telotron.ru/docs/Техдок/03-модули/onboarding-api-pro.md) · § Checklist vs tour
- [T-076 устойчивость tour](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md)
- [E2E-07](../../_telotron.ru/e2e/scenarios/E2E-07-pro-onboarding.md)
- [Цели этапов 2026 · activation](../../01-Директор/Инструкции/Цели%20этапов%202026.md)
- [Спецификация экранов MVP §7](../../08-Дизайнер/Инструкции/Спецификация%20экранов%20MVP.md) — прогресс точками, не wizard bar
- [Решения совещания — UI §4.3](../../08-Дизайнер/Инструкции/Решения%20совещания%20—%20требования%20UI.md)

---

## Журнал

### 2026-06-16

- Тикет создан (отделён от задачи Word для тренеров). Scope: **К + П** сразу. ID **T-060** (T-059 занят auth-gate).

### 2026-06-16 · design

- Добавлен блок **«Дизайнерские решения»**: паттерн чеклиста (не wizard), анатомия карточки шага, маппинг К/П, entry points для П, suppress install banner, deliverables и design QA.
- Slice **0** (дизайн) в подтикетах; роль — дизайнер → dev.

### 2026-06-16 · QA

- Добавлен § **«E2E-метки для автотестов (задание dev)»**: конвенция `data-testid` (`onboarding-*`), таблица обязательных меток по компонентам и step id, `data-status` на карточках, критерий в DoD и slice 2–3. Подготовка к E2E-07 (Playwright онбординг Pro).

### 2026-06-21

- **Срез 1 в коде:** coach-bar, hub, reopen, spotlight, экран завершения; E2E-07 + PHPUnit/Vitest.
- **Freeze пилота** ([Цели этапов §freeze](../../01-Директор/Инструкции/Цели%20этапов%202026.md#freeze-scope-пилота-21062026)): срезы 2–3 — только P0 или по feedback.

### 2026-06-24

- Обратная связь тренера: порядок шагов «сначала подготовка, потом клиент». Вынесено в [T-065](../бэклог/T-065-pro-onboarding-порядок-подготовка-клиент.md) (дельта к этому тикету).

### 2026-07-05 · T-076 sync

- Тикет приведён к **фактическому** UX: coach-bar + hub (не full-page чеклист).
- Зафиксированы **7 шагов П** (`create_exercise`, `create_complex`, …), `schedule_or_plan` = только appointment.
- Добавлен слой **[T-076](../бэклог/T-076-pro-onboarding-устойчивость-ui-checklist-tour.md):** `onboarding-actions.ts`, `onboarding-anchor-registry.ts`, `OnboardingStepRegistry.php`, деградация spotlight, E2E assert по API.
- DoD и E2E-метки обновлены под coach-bar; статус **done (core)**, перенос в `сделано/` — после merge T-076.
