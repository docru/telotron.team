# T-094 · Client: трекеры за последние 2 недели (календарь недели + ввод)

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`бэклог/`** (перенос в архив — по процессу команды) |
| **Приоритет** | P1 |
| **Спринт** | по capacity (Client UX) |
| **Роль** | dev |
| **Создан** | 2026-07-14 |
| **Оценка** | 6–10 ч |

## Контекст

Сейчас клиент заполняет воду / шаги / сон **только за сегодня** — блок ввода на **главной** (`ClientTrackerHomePage`) жёстко работает с `localTodayYmd()`.

Вкладка **«Трекеры»** (`/trackers`) открывает ленту-календарь (`ClientCalendarPage`, `feedSection: trackers`) — удобно смотреть историю, **неудобно** дописывать пропущенные дни.

**Запрос PO:** на странице «Трекеры» — как в дневнике питания: сверху **недельная линейная полоса дней**, ниже — **тот же блок ввода**, что на главной; можно править дни за **последние 2 недели**.

### Канон UX (ориентиры в коде)

| Что | Где |
|-----|-----|
| Недельная полоса дней | `TelotronWeekDayPicker.vue` + логика недели в `shared/nutrition-diary.ts` (`weekRangeForAnchor`, `shiftWeek`) |
| Образец страницы | `ClientNutritionDiaryPage.vue` |
| Блок ввода трекеров | `features/tracking/ClientTrackerDayEditor.vue` (главная + `/trackers`) |
| API Client | `PATCH/GET /api/v1/me/tracker-daily-entries` — см. [api-http §4.1](../../_telotron.ru/docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md); схема [tracker-дневник](../../_telotron.ru/docs/Техдок/03-модули/tracker-дневник-схема-данных-mvp.md) |

## Решение PO

1. **Окно редактирования:** последние **14 календарных дней** в TZ клиента, включая сегодня → самый старый день = `сегодня − 13`.
2. **Будущие дни:** недоступны (как в питании: `disableFutureDays`).
3. **Главная:** остаётся быстрый ввод **только за сегодня** (без недельного календаря).
4. **Вкладка «Трекеры»:** экран ввода по выбранному дню (не лента-календарь как основной UI). Ленту истории трекеров в общем Client-календаре **не ломать** (Pro / общая лента могут остаться).

## Критерии готовности

### UI — страница «Трекеры»

- [x] Маршрут `/trackers` (`workspace-trackers`) → `ClientTrackersPage.vue`.
- [x] Вверху: **линейный календарь недели** на базе `TelotronWeekDayPicker`.
- [x] Сдвиг недели **назад** ограничен окном 14 дней; дни вне окна и будущее — неактивны.
- [x] Основная часть: тот же UX (`ClientTrackerDayEditor`).
- [x] При смене дня — загрузка/сохранение за выбранный `day`.
- [x] Подсветка дней с данными через `GET …?from&to`.
- [x] `npm run build` через Sail.

### Рефакторинг

- [x] `ClientTrackerDayEditor` — общий блок ввода; главная только today.

### API / бэкенд

- [x] PATCH / water-portions: окно 14 дней в IANA TZ клиента (`TrackerEditableDayWindow`).
- [x] Канон: api-http + tracker-дневник §3 UX.

### Тесты

- [x] Feature PHP: окно day / TZ Europe/Moscow.
- [x] Vitest: `editable-day-window.test.ts` + routes acceptance.
- [ ] Ручной smoke (по желанию QA).

## Вне scope

- Редактирование глубже 14 дней (история только read-only в календаре/ленте).
- Новые метрики трекера; вес / измерения (модуль Changes).
- Менять Pro-экран клиента (чтение дневника тренером).
- Сегмент «две полные ISO-недели» с понедельника — **нет**, только скользящие 14 дней от «сегодня».

## Ссылки

- `resources/ts/pages/client/ClientTrackersPage.vue`
- `resources/ts/features/tracking/ClientTrackerDayEditor.vue`
- `resources/ts/pages/client/ClientTrackerHomePage.vue`
- `app/Modules/Tracking/Support/TrackerEditableDayWindow.php`
- [tracker-дневник-схема-данных-mvp](../../_telotron.ru/docs/Техдок/03-модули/tracker-дневник-схема-данных-mvp.md)

## Журнал

### 2026-07-14

- Тикет по запросу PO: окно 14 дней, UI как у дневника питания, блок ввода как на главной.
- Реализовано: API-окно, редактор, `/trackers` с WeekDayPicker, канон, тесты; `build.client` → 216.
