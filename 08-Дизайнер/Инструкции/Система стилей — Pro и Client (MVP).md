# Система стилей — Pro и Client (MVP)

**Статус:** канон для разработчика и Figma (май 2026)  
**Аудитория:** вёрстка (`resources/css/app.css`), shadcn-vue, layout Pro/Client  
**Связь:** [Токены цветов](Токены%20цветов%20—%20Pro%20и%20Client.md) · [Спецификация экранов MVP](Спецификация%20экранов%20MVP.md) · [Решения совещания — UI](Решения%20совещания%20—%20требования%20UI.md)

Один продукт **Телотрон**, две темы: **`theme-pro`** / **`theme-client`**. Один набор компонентов, разные акценты и плотность.

---

## 1. Архитектура

```
:root                    ← нейтрали, радиусы, тени, типографика (общее)
  └── .theme-pro         ← primary синий, фон #F8FAFC, compact
  └── .theme-client      ← primary зелёный, фон #FFFFFF, comfortable
```

Класс темы на `<html>` в `pro.layout` / `client.layout` (или на `#app` в SPA).

**Не делать:** отдельные `ProButton.vue` / `ClientButton.vue` — только CSS-переменные и utility `telotron-density-*`.

---

## 2. Цвета

Полные таблицы HEX и правила календаря/офлайн — в [Токены цветов — Pro и Client](Токены%20цветов%20—%20Pro%20и%20Client.md).

### 2.1. Семантика (обе зоны)

| CSS-переменная | HEX |
|----------------|-----|
| `--foreground` | `#0F172A` |
| `--muted-foreground` | `#64748B` |
| `--border` | `#E2E8F0` |
| `--destructive` | `#DC2626` |
| `--destructive-foreground` | `#FFFFFF` |
| `--warning` | `#D97706` |
| `--success` | `#16A34A` |
| `--offline` | `#94A3B8` |

### 2.2. `theme-pro`

| Переменная | HEX |
|------------|-----|
| `--primary` | `#1D4ED8` |
| `--primary-hover` | `#1E40AF` |
| `--primary-foreground` | `#FFFFFF` |
| `--primary-subtle` | `#EFF6FF` |
| `--background` | `#F8FAFC` |
| `--card` | `#FFFFFF` |
| `--ring` | `#93C5FD` |

### 2.3. `theme-client`

| Переменная | HEX |
|------------|-----|
| `--primary` | `#16A34A` |
| `--primary-hover` | `#15803D` |
| `--primary-foreground` | `#FFFFFF` |
| `--primary-subtle` | `#F0FDF4` |
| `--background` | `#FFFFFF` |
| `--card` | `#FFFFFF` |
| `--ring` | `#86EFAC` |

### 2.4. Календарь (доп. переменные)

**Pro:**

| Переменная | Значение |
|------------|----------|
| `--calendar-entry-individual-bg` | `var(--card)` |
| `--calendar-entry-individual-border` | `var(--border)` |
| `--calendar-entry-group-bg` | `var(--primary-subtle)` |
| `--calendar-entry-group-border` | `var(--primary)` |

**Client:**

| Переменная | Значение |
|------------|----------|
| `--calendar-slot-free-border` | `var(--primary)` |
| `--calendar-slot-booked-bg` | `var(--primary-subtle)` |
| `--calendar-slot-offline-opacity` | `0.4` |

---

## 3. Типографика (Geist)

| Стиль | Pro | Client | Weight | Применение |
|-------|-----|--------|--------|------------|
| `display` | 28px / 32px line | 30px / 34px | 600 | KPI-число на MetricCard |
| `h1` | 20px / 26px | 22px / 28px | 600 | Заголовок экрана |
| `h2` | 16px / 22px | 18px / 24px | 600 | Заголовок секции |
| `body` | **14px** / 20px | **16px** / 24px | 400 | Основной текст |
| `body-sm` | 13px / 18px | 14px / 20px | 400 | Подписи в списках |
| `caption` | 12px / 16px | 12px / 16px | 400 | Метки, время в agenda |
| `label` | 12px / 16px | 13px / 18px | 500 | Поля форм |
| `button` | 14px / 20px | 16px / 22px | 500 | Текст в кнопках |

**Utility (Tailwind):**

- Pro: на корне `text-sm` (14px body).
- Client: на корне `text-base` (16px body).

**Цифры в метриках:** `font-variant-numeric: tabular-nums`.

---

## 4. Отступы и сетка

База **4px**. Контейнер контента: max-width ориентир **430px**, горизонтальный padding **`--page-px`**.

| Токен | Pro | Client |
|-------|-----|--------|
| `--page-px` | 16px | 16px |
| `--section-gap` | 16px | 20px |
| `--card-padding` | 16px | 16px |
| `--list-row-py` | 10px | 12px |
| `--stack-gap-sm` | 8px | 8px |
| `--stack-gap-md` | 12px | 16px |

---

## 5. Радиусы, тени, обводки

| Токен | Значение |
|-------|----------|
| `--radius` | `6px` (0.375rem) — inputs, мелкие блоки |
| `--radius-md` | `6px` (0.375rem) — кнопки, поля |
| `--radius-sm` | `4px` (0.25rem) — бейджи, мелочи |
| `--radius-lg` | `8px` (0.5rem) — Card, Sheet, hero public |
| `--radius-full` | `9999px` — Avatar, calendar dots, progress track, segmented «капсула» |
| `--shadow-card` | `0 1px 3px rgb(15 23 42 / 0.08)` |
| `--shadow-sheet` | `0 -4px 24px rgb(15 23 42 / 0.12)` |
| `--border-width` | `1px` |

Focus: `outline: 2px solid var(--ring); outline-offset: 2px`.

---

## 6. Размеры компонентов

| Компонент | Pro | Client |
|-----------|-----|--------|
| Primary button height | 40px | 44px |
| Secondary button height | 36px | 40px |
| Icon button | 40×40px | 44×44px |
| Touch target min | 40px | 44px |
| Header height | 56px | 56px |
| Bottom tab bar | 56px + safe-area | то же |
| Avatar sm / md | 32 / 40px | 36 / 44px |
| Input height | 40px | 44px |

---

## 7. Компоненты (спецификация)

Один код в `components/ui` + зонные обёртки при необходимости. Стили через `bg-primary`, `text-muted-foreground` и т.д.

### 7.1. Button

| Вариант | Вид |
|---------|-----|
| `primary` | `bg-primary text-primary-foreground rounded-md`, высота по зоне |
| `secondary` | `border border-border bg-card` |
| `ghost` | без фона, `text-foreground` |
| `destructive` | `bg-destructive` |

Disabled: opacity 0.5, не менять hue.

### 7.2. Card

- `bg-card`, `rounded-[var(--radius-lg)]`, `shadow-[var(--shadow-card)]`, `p-[var(--card-padding)]`.
- Заголовок: `h2`; подзаголовок: `muted-foreground`, `body-sm`.

### 7.3. MetricCard

- Иконка в квадрате `40px`, фон `primary/10`, иконка `text-primary`.
- Число: `display`; подпись: `caption`.
- Тренд ↑: `text-success`; ↓: `text-destructive` (обе зоны одинаково).

### 7.4. ListRow

- Flex: Avatar (инициалы) + column + ChevronRight.
- Title: `body` medium; subtitle: `muted-foreground`, `body-sm`.
- Divider: `border-b border-border` последний без линии.

### 7.5. QuickActionGrid

- 2×2, gap 12px; ячейка: `rounded-lg`, `bg-primary/10`, иконка `text-primary`, подпись `caption`.

### 7.6. BottomTabBar

- `bg-card`, `border-t border-border`, 3–4 иконки Lucide 24px.
- Active: `text-primary` + точка 4px `bg-primary` под иконкой.
- Inactive: `text-muted-foreground`.

### 7.7. Sheet (bottom)

- `rounded-t-[var(--radius-lg)]`, `shadow-sheet`, handle 32×4px `bg-border`.
- Pro: отмена занятия — поле «Причина» обязательное.

### 7.8. Toast

- Success: иконка + `success`; Error/409: `destructive`.
- Pro copy «вы»; Client «ты» (см. §10).

### 7.9. OfflineBanner

- Фон `offline-subtle` (`#F1F5F9`), текст `foreground`, иконка `offline`.
- Pro: «Изменения расписания доступны только онлайн».
- Client: «Запись на занятие — при подключении к сети».

### 7.10. FeatureGate (тариф Light)

- Card с Lock icon, `muted` фон, CTA «Доступно на Профи» — `primary` outline.
- **Не** серый «сломанный» экран.

### 7.11. Calendar (общие части)

- `CalendarStrip`: горизонтальные дни, selected = круг `bg-primary text-primary-foreground`.
- `EventListRow`: время `caption` + title `body` + цветная полоска 4px слева (семантика §2.4).
- Pro default view: **month**; Client: **agenda**.

### 7.12. Avatar

- Круг, `rounded-full`, фон `primary-subtle`, текст `primary`, инициалы 2 буквы, **без** фото по умолчанию.

### 7.13. Skeleton

- `bg-muted` animate-pulse, те же размеры что Card/ListRow.

---

## 8. Shell (layout)

```
┌──────────────────────────────────┐ 56px  AppHeader: logo + zone badge + actions
│  scrollable main (page-px)       │
│                                  │
├──────────────────────────────────┤ 56px + safe-area  BottomTabBar
└──────────────────────────────────┘
```

- **Logo:** один знак; подпись «Pro» / «Client» — `caption`, `muted-foreground`.
- Sticky CTA (Pro список клиентов): `Пригласить` — `primary`, full-width, над tab bar.

---

## 9. CSS для `app.css` (копипаст-ориентир)

Ниже — HEX; в проекте допустима конвертация в `oklch` для shadcn, **сохраняя те же визуальные значения**.

```css
:root {
  --foreground: #0f172a;
  --muted-foreground: #64748b;
  --muted: #f1f5f9;
  --border: #e2e8f0;
  --destructive: #dc2626;
  --destructive-foreground: #ffffff;
  --warning: #d97706;
  --success: #16a34a;
  --offline: #94a3b8;
  --offline-subtle: #f1f5f9;

  --radius: 0.375rem;
  --radius-lg: 0.5rem;
  --shadow-card: 0 1px 3px rgb(15 23 42 / 0.08);
  --shadow-sheet: 0 -4px 24px rgb(15 23 42 / 0.12);

  --page-px: 1rem;
  --header-h: 3.5rem;
  --tabbar-h: 3.5rem;
}

.theme-pro {
  --primary: #1d4ed8;
  --primary-hover: #1e40af;
  --primary-foreground: #ffffff;
  --primary-subtle: #eff6ff;
  --background: #f8fafc;
  --card: #ffffff;
  --ring: #93c5fd;
  --accent: var(--warning);

  --btn-h: 2.5rem;
  --calendar-entry-group-bg: var(--primary-subtle);
  --calendar-entry-group-border: var(--primary);
}

.theme-client {
  --primary: #16a34a;
  --primary-hover: #15803d;
  --primary-foreground: #ffffff;
  --primary-subtle: #f0fdf4;
  --background: #ffffff;
  --card: #ffffff;
  --ring: #86efac;

  --btn-h: 2.75rem;
  --calendar-slot-offline-opacity: 0.4;
}

/* Плотность: на html.theme-pro → text-sm; theme-client → text-base */
```

Маппинг на shadcn: `--primary` → `--color-primary` через существующий `@theme inline` в `app.css`.

---

## 10. Voice (микрокопи)

| | Pro | Client |
|--|-----|--------|
| Обращение | вы | ты |
| Ошибка сети | «Проверьте подключение к сети» | «Проверь подключение к сети» |
| 409 слот | «Этот слот уже занят. Выберите другое время» | «Этот слот уже занят. Выбери другое время» |
| Успех записи | «Запись сохранена» | «Запись сохранена» |
| Empty клиенты | «Пока нет клиентов. Пригласите первого» | — |
| CTA | без «ты/вы»: «Пригласить клиента», «Записаться» | |

---

## 11. PWA / manifest

| | Pro | Client |
|--|-----|--------|
| `theme_color` | `#1D4ED8` | `#16A34A` |
| `background_color` | `#F8FAFC` | `#FFFFFF` |

См. [Токены цветов §7](Токены%20цветов%20—%20Pro%20и%20Client.md) — известные расхождения в layout Client исправить при вёрстке.

---

## 12. Референсы Pinterest (роль)

| Пин | Что внедряем в систему |
|-----|------------------------|
| CRM mobile | MetricCard, QuickActionGrid, Tab bar, Card |
| Календари (9 экранов) | CalendarStrip, agenda, event row, sheet |
| Sportup | Подтверждение записи, полоса дат |
| FITNEX | Только блок «Сегодня» + простой график (Client), не orange primary |

---

## 13. Порядок внедрения (разработчик)

1. `:root` + `.theme-pro` / `.theme-client` в `app.css`.
2. Классы темы на layout Pro/Client + `theme_color` manifest.
3. Shell: Header + BottomTabBar.
4. Button, Card, ListRow, MetricCard.
5. Pro: клиенты + sticky CTA → календарь.
6. Client: главная + OfflineBanner + календарь agenda.
7. Toast, Sheet, FeatureGate, Skeleton.

---

## 14. Приёмка

- [ ] Pro синий / Client зелёный на CTA и active tab.
- [ ] Одинаковые формы Card/Button/Sheet в обеих зонах.
- [ ] Client primary не `#1D4ED8` в коде.
- [ ] Календарь: семантические цвета слотов, не радуга.
- [ ] Нет стоковых фото на MVP-экранах.

---

## 15. Журнал

| Дата | Изменение |
|------|-----------|
| 2026-05 | Полная система стилей MVP (дизайнер 08) |
