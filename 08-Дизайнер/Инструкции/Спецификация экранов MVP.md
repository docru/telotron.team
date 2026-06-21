# Спецификация экранов MVP — Pro и Client

**Статус:** канон вёрстки приоритетных экранов (май 2026)  
**Связь:** [Система стилей (MVP)](Система%20стилей%20—%20Pro%20и%20Client%20(MVP).md) · [Токены цветов](Токены%20цветов%20—%20Pro%20и%20Client.md) · [Решения совещания — UI](Решения%20совещания%20—%20требования%20UI.md) · ТЗ §14

**Охват:** 6 приоритетных экранов + общий shell + состояния empty / error / loading. Остальные экраны §14 наследуют shell и компоненты без отдельной спеки.

**Референсы Pinterest:** CRM (shell, KPI), календари (полоса дат, agenda), Sportup (подтверждение записи), FITNEX (блок «Сегодня» на Client).

---

## 0. Общий shell (Pro и Client)

**Тема:** `theme-pro` / `theme-client` на `<html>`.  
**Компоненты:** `AppHeader`, `BottomTabBar`, опционально `OfflineBanner`.

```
┌─────────────────────────────────────────┐
│ [Logo] Телотрон · Pro|Client    🔔  👤 │  AppHeader 56px
├─────────────────────────────────────────┤
│ OfflineBanner (если нет сети / Pro)     │  необязательно
├─────────────────────────────────────────┤
│                                         │
│           <main> scroll                 │  padding: --page-px 16px
│                                         │  gap секций: --section-gap
│                                         │
├─────────────────────────────────────────┤
│ [sticky CTA — только Pro клиенты]       │  опционально
├─────────────────────────────────────────┤
│  🏠      📅      ⋯                      │  BottomTabBar 56px + safe-area
└─────────────────────────────────────────┘
```

| Элемент | Pro | Client |
|---------|-----|--------|
| Tab 1 | Клиенты (`Users`) | Главная (`Home`) |
| Tab 2 | Календарь (`Calendar`) | Календарь (`Calendar`) |
| Tab 3 | Ещё (`MoreHorizontal`) | Планы (`FileText`) или Профиль |
| Header actions | Уведомления, профиль | То же |
| OfflineBanner | «Изменения расписания доступны только онлайн» | На главной/календаре при офлайне записи |

**ТЗ:** viewport ~430px; touch target ≥40px Pro / ≥44px Client.

---

## 1. Pro — Список клиентов

**Маршрут / модуль:** workspace, M1.  
**ТЗ:** §14.3 — кнопка «Пригласить» над списком, copy + share.

### 1.1. Блок-схема (default, есть клиенты)

```
AppHeader
─────────────────────────────────────
[не показывать MetricCard-карусель — макс. 0–2 KPI опционально после онбординга]

┌─ sticky над списком ─────────────────┐
│  Button primary full-width           │  «Пригласить клиента»
└──────────────────────────────────────┘

h2 «Клиенты»                    body-sm «N активных»

ListRow × N
  Avatar | Иванов И. · след. занятие Пт 10:00 | >
ListRow
  ...

BottomTabBar · active: Клиенты
```

### 1.2. Компоненты

| Блок | Компонент | Стили / поведение |
|------|-----------|-------------------|
| CTA | `Button` primary | `rounded-full`, full-width, sticky `bottom: tabbar + 8px`, z-index над списком |
| Заголовок секции | `h2` + `caption` | «Клиенты», счётчик muted |
| Строка | `ListRow` | Avatar md, title = ФИО, subtitle = «Следующее: …» или «Нет занятий» |
| Переход | tap ListRow | → экран §2 Карточка клиента |

### 1.3. Состояния

| Состояние | Оформление |
|-----------|------------|
| **Loading** | Skeleton: 1× sticky button + 6× ListRow |
| **Empty** (после онбординга недопустим как норма; первый вход — ок) | Card centered: иконка `Users`, «Пока нет клиентов», «Пригласите первого — ссылка займёт минуту», Button primary → инвайты или copy inline |
| **Error** | Toast destructive + «Не удалось загрузить список. Повторите попытку.» + Button ghost «Обновить» |

### 1.4. Voice

- «Вы»; CTA: «Пригласить клиента» (без местоимения).

### 1.5. Не на этом экране

- Партнёрская ссылка (только §5 Инвайты).
- Группы, фильтры, поиск (post-MVP / минимум).

---

## 2. Pro — Карточка клиента

**Маршрут:** из списка клиентов.  
**ТЗ:** §14.3, §14.7 (планы), §14.9 (вес).

### 2.1. Блок-схема

```
AppHeader + back
─────────────────────────────────────
Card (шапка)
  Avatar lg | ФИО h1
              body-sm: пол · возраст N лет
  Row: «Вес» 72,5 кг  >     (ListRow-like, tap → Sheet/Modal прогресса)

section gap

Card «Занятия»
  h2 + link «В календарь»
  EventListRow × 1–3 (ближайшие)
  empty: «Нет запланированных занятий»

Card «Планы»
  h2 + Button ghost «Планы» / список назначенных
  ListRow: название плана · дата | >

Card «Заметки» (если в MVP) — secondary, body-sm

BottomTabBar (остаётся на Клиенты или текущий tab)
```

### 2.2. Компоненты

| Блок | Компонент | Примечание |
|------|-----------|------------|
| Шапка | `Card` + `Avatar` lg | Инициалы; без фото |
| Вес | `ListRow` или кликабельная строка | Открывает модал графика (1/3/6/12 мес, default 3) — §14.9 |
| Занятия | `EventListRow` | Индивид: border neutral; группа: `primary-subtle` + border primary |
| Планы | `ListRow` | Переход к назначению/скачиванию meta |

### 2.3. Состояния

| Состояние | Оформление |
|-----------|------------|
| **Loading** | Skeleton шапки + 2 Card |
| **Error** | Toast; шапка из кэша если есть |
| **Модалка веса** | Sheet или full Modal: простой line chart, segmented 1/3/6/12 мес |

### 2.4. Voice

- «Вы»; «Откройте прогресс веса» в подсказке при первом tap.

---

## 3. Pro — Календарь

**Маршрут:** tab Календарь.  
**ТЗ:** §14.1, §14.5 — month/week/day/agenda; отмена с причиной; офлайн без мутаций.

### 3.1. Блок-схема (default: month)

```
AppHeader
OfflineBanner (если offline)
─────────────────────────────────────
Segmented: [ Month | Week | Day | Agenda ]   ghost/primary active

Row: < Май 2026 >                    icon buttons

CalendarMonth grid
  ячейки дней · точка под датой если есть занятия
  today: ring primary 30%

Week: сетка 3×3 (7 дней Пн–Вс + 2 пустые ячейки), без горизонтального скролла на 430px. Day — список занятий выбранного дня.

section gap

h2 «Сегодня» / выбранный день

EventListRow × N
  │ индивид — border slate
  │ группа — bg primary-subtle
  tap → Sheet детали занятия

FAB optional: «+» только online → Sheet создание (или кнопка в header)

BottomTabBar · active: Календарь
```

### 3.2. Sheet — детали занятия (Pro)

```
Sheet
  h2 · время · тип (индивид / группа)
  ListRow участники (группа)
  M4: «Подтвердили 3 · не ответили 2» — caption + раскрытие
  Button secondary «Перенести»
  Button destructive «Отменить»
    → вложенная форма: Textarea «Причина» required + Button destructive «Подтвердить отмену»
```

### 3.3. Компоненты

| Блок | Компонент |
|------|-----------|
| Переключатель вида | Segmented control (4 режима) |
| Сетка | `CalendarMonth` |
| Неделя | `TelotronCalendar` week — grid 3×3 |
| Полоса дней (legacy) | — не горизонтальный scroll на 430px |
| Событие | `EventListRow` + семантика цветов §Токены 4.1 |
| Создание/редакт | `Dialog` + `Input` datetime-local; тип занятия — см. §3.6 |
| Офлайн | `OfflineBanner` + disabled на FAB/мутациях |

### 3.6. Dialog «Новое занятие» (канон продукта)

**Группа не обязательна.** Тренер на любом тарифе создаёт **индивидуальные** занятия без раздела «Группы». Группа нужна **только** для типа «Групповое» (тариф **Профи+**, модуль групп) — [календарь-и-запись](../../../_telotron.ru/docs/Бизнес-требования/02-модули/m2-календарь/календарь-и-запись.md).

```
Dialog «Новое занятие»
  если есть хотя бы одна группа (Профи+):
    Radio: ● Индивидуальное (по умолчанию)  ○ Групповое
    если «Групповое» → Select «Группа»
  иначе (Лайт / без групп):
    только поля даты-времени (тип = индивидуальное, без переключателя)
  Input datetime-local «Начало» / «Окончание»
  Footer: [Создать] primary · [Отмена] ghost
```

**Запрещено в UI:** блокировка «Сначала создайте группу…», disabled «Индивидуальное (скоро)», кнопка «Создать» только при `groups.length > 0`.

**API:** `POST /api/v1/me/appointments` с `session_type: individual` без `training_group_id`; для `group` — с `training_group_id`.

**Календарь:** индивидуальное — заголовок «Индивидуальное», стиль `border` slate (§Токены 4.1); групповое — `bg primary-subtle`, подпись с ёмкостью.

### 3.4. Состояния

| Состояние | Оформление |
|-----------|------------|
| **Loading** | Skeleton grid + 3 EventListRow |
| **Empty day** | «На этот день занятий нет» + Button «Добавить занятие» (online) |
| **Light gate группа** | Скрыть/заблокировать только radio «Групповое» и select группы; **не** блокировать создание занятия |

### 3.5. Voice

- «Укажите причину отмены»; «Занятие отменено».

---

## 4. Pro — Инвайты (в «Ещё» или отдельный пункт)

**ТЗ:** §14.3 — клиентская и партнёрская ссылки; клиентская primary.

### 4.1. Блок-схема

```
AppHeader + back (если из «Ещё»)
─────────────────────────────────────
h1 «Приглашения»

Card primary emphasis — клиент
  h2 «Ссылка для клиента»
  body-sm пояснение (без маркетингового hype)
  Row: [ readonly url truncate ] 
  Button primary «Скопировать» | Button secondary icon Share

section gap --section-gap-lg

Card secondary — партнёр
  h2 «Партнёрская ссылка»
  caption «Для приглашения коллег-тренеров»
  те же Copy + Share, визуально слабее (secondary button default)

ListRow «Активные ссылки» (Maximum/trial) — если есть многоссылочность

BottomTabBar
```

### 4.2. Правила оформления

- **Клиентская карточка** выше, `Card` с border `primary/20` или лёгкий `primary-subtle` фон заголовка.
- **Партнёрская** — обычный `Card`, без конкурирования с primary CTA.
- Иконки: `Link`, `Share2` (Lucide).

### 4.3. Состояния

| Состояние | Оформление |
|-----------|------------|
| **Loading** | Skeleton 2 Card |
| **Success copy** | Toast success «Ссылка скопирована» |
| **Error** | Toast destructive |

---

## 5. Client — Главная

**ТЗ:** §14.6 (M4), §14.7 (планы), §14.8 (M7-lite), §14.9 (вес).  
**Референс:** один макет **online + offline** (баннер и тусклые слоты в блоке «Занятия»).

### 5.1. Блок-схема (online)

```
AppHeader
─────────────────────────────────────
body «Привет, {имя}»                    h1 необязательно, body 16px достаточно

Card primary-subtle bg «Сегодня»       M7-lite
  h2 «Сегодня»
  Checkbox row × 3–5 (быстрый дневник)
  Input optional «Заметка» одна строка
  Button primary sm «Сохранить» или auto-save indicator

section gap

Card «Занятия»
  h2 + link «Календарь»
  EventListRow ближайшие 1–2
  Button ghost «Записаться» → календарь

Card M4 (условно, если есть активный запрос)
  body «Подтверди занятие завтра в 10:00»
  Button primary full «Подтвердить»

Card «Вес»
  Row: последний вес + Button ghost «Прогресс»

Card «Мои планы»
  ListRow: название | download icon
  empty: «Тренер пока не назначил планов»

Banner PWA install (после первого входа, dismissible)

BottomTabBar · active: Главная
```

### 5.2. Блок-схема (offline — тот же экран)

```
+ OfflineBanner «Запись на занятие — при подключении к сети»

Card «Занятия»
  EventListRow с opacity 40%, icon WifiOff offline
  слоты записи не показывать как CTA

M7-lite и вес — **доступны** (локальная запись / кэш), если по ТЗ разрешено
Планы — только уже закэшированные ссылки или «Нужна сеть»
```

### 5.3. Компоненты

| Блок | Компонент |
|------|-----------|
| Сегодня | `Card` + `primary-subtle` + чекбоксы shadcn |
| M4 | `Card` + один `Button` primary |
| Вес | `Input` number или `ListRow` + модал графика |
| Планы | `ListRow` + icon `Download` |
| Install PWA | `Card` muted + `Button` secondary |

### 5.4. Состояния

| Состояние | Оформление |
|-----------|------------|
| **Loading** | Skeleton: Card «Сегодня» + 2 Card; **не блокировать** поле веса (ТЗ §14.9) |
| **Empty занятий** | «Ближайших занятий нет» + «Записаться» |
| **409** (с календаря) | Toast: «Этот слот уже занят. Выбери другое время» |

### 5.5. Voice

- «Ты» в подсказках; CTA: «Подтвердить», «Записаться».

### 5.6. Не на главной

- Стоковые фото, кольца KPI, каталог тренировок, meal planner.

---

## 6. Client — Календарь (agenda-first)

**ТЗ:** §14.1, §14.5 — agenda; слоты outline; offline 40%.

### 6.1. Блок-схема

```
AppHeader
OfflineBanner (offline)
─────────────────────────────────────
CalendarStrip                         горизонтальные дни, selected primary circle

h2 «{День недели, дата}»

Agenda list:
  TimeSlotRow FREE (online)
    caption 10:00
    Card outline border-primary «Свободно» tap → BookingSheet
  TimeSlotRow BOOKED
    primary-subtle «Тренировка с {тренер}»
  TimeSlotRow OFFLINE
    opacity 40%, icon offline, некликабельно

Segmented опционально: [ Agenda | Month ] — month вторичен

BottomTabBar · active: Календарь
```

### 6.2. Sheet — запись (Client)

```
BookingSheet
  h2 «Запись на 10:00»
  body подтверждение даты
  Button primary «Записаться»
  Button ghost «Отмена»
```

После 409: Toast destructive (см. §5.4).

### 6.3. Компоненты

| Блок | Компонент | Токен |
|------|-----------|-------|
| Свободный слот | `Card` outline | `calendar-slot-free` |
| Моя запись | `Card` fill | `calendar-slot-booked` |
| Offline слот | `Card` | `opacity: var(--calendar-slot-offline-opacity)` |
| Полоса дат | `CalendarStrip` | общий с Pro |

### 6.4. Состояния

| Состояние | Оформление |
|-----------|------------|
| **Loading** | Skeleton strip + 5 rows |
| **Empty day** | «Нет свободных слотов в этот день» |
| **Success** | Toast success «Ты записан на …» |

---

## 7. Client — Онбординг (связанный поток, 3 шага)

Не в «шестёрке» hi-fi, но **в приоритете MVP** — кратко для вёрстки.

| Шаг | Содержание | Компоненты |
|-----|------------|------------|
| 1 | «Тебя пригласил тренер {имя}» — абстракт, без фото | `Card` + `Button` primary «Продолжить» |
| 2 | ФИО, пол | `Input` ×2, select/segmented пол |
| 3 | Дата рождения | date picker native или `Input` |
| Финал | → вход Passkey / OTP | отдельно §14.11 |

Progress: 3 точки `caption`, не длинный wizard progress bar.

---

## 8. Сводная таблица: экран → компоненты

| Экран | Компоненты (обязательные) |
|-------|---------------------------|
| Shell | AppHeader, BottomTabBar, OfflineBanner |
| Pro клиенты | Button, ListRow, Avatar, Skeleton, Toast |
| Pro карточка | Card, Avatar, ListRow, EventListRow, Sheet (вес) |
| Pro календарь | Segmented, CalendarMonth, CalendarStrip, EventListRow, Sheet, FeatureGate |
| Pro инвайты | Card ×2, Button, Toast, Input readonly |
| Client главная | Card, Checkbox, Input, EventListRow, Button, Toast, OfflineBanner |
| Client календарь | CalendarStrip, Card slots, BookingSheet, Toast, OfflineBanner |

---

## 9. Общие состояния (все экраны)

| Тип | Правило |
|-----|---------|
| **Skeleton** | Повторяет геометрию реального блока, не generic spinner на весь экран |
| **Empty** | Card по центру, Lucide 48px muted, 2 строки текста, 1 CTA |
| **Error сети** | Toast + OfflineBanner где применимо |
| **Error API** | Toast destructive, текст по Voice зоны |
| **FeatureGate** | Только Pro, Light без групп |

---

## 10. Порядок вёрстки для разработчика

1. Shell + темы  
2. Pro: §1 Список клиентов → §2 Карточка → §3 Календарь → §4 Инвайты  
3. Client: §5 Главная (сразу вариант с OfflineBanner) → §6 Календарь  
4. §7 Онбординг при инвайте  
5. Проход empty/skeleton по чеклисту §9  

**Приёмка:** тестировщик сверяет с §9 [Система стилей](Система%20стилей%20—%20Pro%20и%20Client%20(MVP).md) и этим документом + ТЗ §14.

---

## 11. Журнал

| Дата | Изменение |
|------|-----------|
| 2026-05 | Первая спецификация 6+ экранов MVP (дизайнер 08) |
