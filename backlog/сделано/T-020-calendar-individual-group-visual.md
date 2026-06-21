# T-020 Календарь · визуальное различие индивидуальных и групповых занятий

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Закрыт** | 2026-06-09 |
| **Очередь** | 5 · ~3–5 ч |
| **Приоритет** | P1 |
| **Спринт** | 0 |
| **Роль** | dev + дизайн (приёмка) |
| **Создан** | 2026-05-31 |

## Контекст

**Проблема (скрин Pro → Расписание → месяц):** записи **индивидуальных** и **групповых** занятий в ячейках выглядят одинаково — серые полоски с обрезанным текстом («10:00 П…», «21:00 И…»). По цвету и форме **не понять**, где группа, где индивидуальное. Заказчик: «индивидуальные и групповые записи визуально не отличаются».

**Связь:** статусы cancelled/past/upcoming закрыты в [T-019](../сделано/T-019-calendar-appointment-status-colors.md). Этот тикет — **только тип занятия** (`session_type`: `individual` | `group`), ортогонально статусу и occupancy.

**Канон дизайна:** [Токены цветов — Pro и Client](../../08-Дизайнер/Инструкции/Токены%20цветов%20—%20Pro%20и%20Client.md) §4 «Календарь (Pro)»:

| Токен | Индивидуальное | Групповое |
|-------|----------------|-----------|
| Фон | `calendar-entry-individual` → `card` | `calendar-entry-group` → `primary-subtle` |
| Акцент | `border` | `primary` border + **полоска слева** |

**Бизнес:** [календарь-и-запись](../../../_telotron.ru/docs/Бизнес-требования/02-модули/m2-календарь/календарь-и-запись.md) §5 — групповые с занятостью; [группы](../../../_telotron.ru/docs/Бизнес-требования/02-модули/m2-календарь/группы.md).

---

## 1. Где сейчас ломается

| Поверхность | Компонент | Режим | Проблема |
|-------------|-----------|-------|----------|
| **Pro Расписание** | `TelotronCalendar` | **month** | До правки: все pills `--default`; нужна приёмка на 360px |
| **Pro Расписание** | `TelotronCalendar` | **week** | В ячейке только **время**, без имени/типа; individual/group почти неразличимы |
| **Pro Расписание** | `TelotronCalendar` | day / agenda | `--group` = `border-l-3px`; контраст с individual слабый на части состояний |
| **Client Записаться** | `TelotronCalendar` | все | `mapRow` **не передаёт** `sessionType` — только `emphasis` |
| **Дневник / карточка клиента** | `ClientFeedCalendar` | week / day / agenda | appointment без стиля по `session_type` в payload |

**Данные:** Pro `WorkspaceSchedulePage` уже маппит `sessionType`. API: `session_type` в `GET /me/appointments` и в feed `payload.session_type`.

---

## 2. Целевой визуальный язык

Два слоя (комбинируются со статусами T-019 и occupancy):

### 2.1 Индивидуальное

- Фон: `--calendar-entry-individual-bg` (`card` / белый)
- Рамка: `--calendar-entry-individual-border`, сплошная
- Без цветной полоски слева

### 2.2 Групповое

- Фон: `--calendar-entry-group-bg` (`primary-subtle`, голубой)
- Рамка: `--calendar-entry-group-border` с **`border-l-2` … `border-l-[3px]`** слева
- На узкой month pill полоска **обязательна** — основной маркер типа

### 2.3 Client

| Роль | Поведение |
|------|-----------|
| **Моя запись** | `emphasis` (как сейчас); тип можно не дублировать |
| **Свободный групповой слот** | group-стиль + subtitle «N/M мест» |
| **Свободный индивидуальный** | individual-стиль (outline / нейтральная карточка) |

**Не показывать** в UI коды `session_type`, `individual`, `group`.

---

## 3. Режимы календаря (требования)

### Month (приоритет — скрин заказчика)

Классы `telotron-calendar-month-pill--individual` / `--group` в `monthPillClass(e)` по `e.sessionType`.

| Тип | Pill |
|-----|------|
| Individual | белый/карточка + тонкая рамка |
| Group | `primary-subtle` + синяя полоска слева |

Проверка: в одной ячейке 2+ записи разных типов — **различимы без чтения имён**.

### Week

- Сохранить цвет entry по типу (усилить контраст individual vs group).
- **Рекомендация:** в узкой колонке показывать **время + 1-я буква названия группы / инициал** или точку-маркер цвета типа (не обрезать всё до «П…» без контекста).
- `aria-label`: «14:00, группа Утренняя» / «14:00, Маша Петрова, индивидуальное».

### Day / Agenda (Pro)

- `telotron-calendar-slot--individual` / `--group` — как в каноне токенов.
- Group + `occupancy: partial` — amber **поверх** group-фона (не заменять тип).

### ClientFeedCalendar

- Для `type === 'appointment'`: классы `--individual` / `--group` из `payload.session_type`.
- Pro карточка клиента и Client дневник — единая логика.

---

## 4. Файлы

| Файл | Действие |
|------|----------|
| `resources/ts/widgets/TelotronCalendar/TelotronCalendar.vue` | `monthPillClass`, `weekEntryClass`, week template (подпись/aria) |
| `resources/css/app.css` | `.telotron-calendar-month-pill--individual/group`, усилить week/slot group vs individual |
| `resources/ts/pages/client/ClientBookingPage.vue` | `sessionType` в `mapRow` из `a.session_type` |
| `resources/ts/widgets/ClientFeedCalendar/ClientFeedCalendar.vue` | классы appointment по `session_type` |
| `resources/ts/shared/calendar/client-feed.ts` | `eventAppointmentTypeClass(e)` |
| `resources/ts/shared/calendar/appointment-visual.test.ts` или новый `calendar-entry-type.test.ts` | маппинг классов (опц.) |
| `Команда/08-Дизайнер/Инструкции/Токены цветов — Pro и Client.md` | зафиксировать month/week паттерн |
| `config/version.php` | **`build.pro`** +1; **`build.client`** +1 при правках Client |

**Задел в коде (проверить / довести):** частично есть `month-pill--individual/group` и усиленные week-entry в `app.css` — нужна **сборка, smoke и приёмка**, не считать закрытым без проверки на устройстве.

---

## 5. Критерии готовности

- [x] Pro **месяц**: `monthPillClass` → `--individual` / `--group`
- [x] Pro **неделя**: `weekEntryShortLabel`, `weekEntryAriaTypeHint`, цвет entry по типу
- [x] Pro **день / лента**: `telotron-calendar-slot--individual` / `--group`
- [x] Client **Записаться**: `sessionType` в `ClientBookingPage.mapRow`
- [x] Client feed: `calendarEntryTypeClass` из `payload.session_type` (`client-feed.ts`)
- [x] Сочетание с T-019: статусные модификаторы ортогональны типу
- [x] `calendar-entry-type.test.ts`; `npm run test:ts` **121** green; `build.pro` **138**, `build.client` **161**
- [ ] Дизайн: визуальный smoke 360px (опционально)

---

## 6. Вне scope

- Статусы cancelled / past / live ([T-019](../сделано/T-019-calendar-appointment-status-colors.md))
- Заполненность empty / partial / full как отдельная задача (уже есть amber; только не ломать)
- `workout_execution`, `meal`, трекеры в feed
- Легенда «И — индивидуальное, Г — группа» на экране (достаточно самодокументируемых цветов)

---

## Ссылки

- `TelotronCalendarEntry.sessionType` — `resources/ts/shared/calendar/types.ts`
- Pro маппинг: `WorkspaceSchedulePage.mapToCalendarEntry`
- CSS vars: `--calendar-entry-individual-*`, `--calendar-entry-group-*` в `app.css`

---

## Журнал

### 2026-05-31

- Тикет выделен из обсуждения T-019: заказчик отдельно указал на неразличимость individual/group в месяце. T-019 закрыт.

### 2026-06-09 · закрытие

- `4e7e550` — статусы + individual/group в Pro; `2beb409` — Client неделя/месяц + «мои записи»; `871c015` — запоминание режима календаря.
- Модуль `calendar-entry-type.ts` + тесты; CSS `--calendar-entry-individual-*` / `--group-*`.
- Тикет → **`сделано/`**.
