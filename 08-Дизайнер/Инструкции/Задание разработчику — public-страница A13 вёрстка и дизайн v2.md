# Задание разработчику: public-страница A13 — вёрстка и дизайн v2

**От:** дизайнер (08)  
**Статус:** к передаче в разработку  
**Gate:** период 0, деплой **01.06.2026**  
**Связь:** [ТЗ — public-страница (A13)](../../01-Директор/Инструкции/ТЗ%20—%20public-страница%20проекта%20(A13).md) · [Задание разработчика A13](../../03-Разработчик/Инструкции%20разработка/Задание%20—%20public-страница%20A13%20(период%200).md) · [единый стиль install и auth](Задание%20разработчику%20—%20единый%20стиль%20install%20и%20auth.md) · [Система стилей §8](Система%20стилей%20—%20Pro%20и%20Client%20(MVP).md)

---

## 1. Проблема

На `https://telotron.ru/` (локально `telotron.test`) страница выглядит как **сырой HTML**: чёрный текст на белом, синие подчёркнутые ссылки, нет pill-кнопки, нет ритма секций.

| Причина | Симптом |
|---------|---------|
| **Не собран / не подключён CSS** | `@vite(['resources/css/app.css'])` в `public/layout.blade.php` без `npm run build` или без Vite dev → классы `telotron-*` не действуют |
| **Дизайн v1 слишком плоский** | Даже при подключённом CSS страница — сплошной текст без карточек и визуальной иерархии (замечание заказчика) |

**Код уже есть:** `PublicWelcomeController`, `resources/views/public/welcome.blade.php`, `public/layout.blade.php`, классы в `app.css` (`.telotron-public-landing*`), тесты `PublicWelcomePageTest.php`. Задача — **довести визуал до приёмки** и гарантировать CSS в dev/prod.

---

## 2. Цель

1. Страница **визуально в одной системе** с install/auth Pro (`theme-pro`, Geist, pill CTA, логотип).
2. Контент — **дословно §6.2** [ТЗ A13](../../01-Директор/Инструкции/ТЗ%20—%20public-страница%20проекта%20(A13).md) (не расходиться с тестами без согласования).
3. CTA **«Начать бесплатно»** → `/i/{token}` платформенной ссылки admin (D4).
4. На **360px** и **1280px** — без горизонтального скролла, CTA заметен без прокрутки до футера.

---

## 3. Контент (канон — не менять без ревью)

Копипаст из **ТЗ A13 §6.2**. Ключевые строки для assert в тестах:

| Блок | Текст |
|------|-------|
| H1 | Ведите клиентов в одном приложении |
| Lead | Приглашайте клиентов, ведите расписание занятий, назначайте программы тренировок и план питания. Всё для ежедневной работы с клиентской базой — без таблиц и бессистемных чатов. |
| CTA | Начать бесплатно |
| H2 | Что такое Телотрон / Для кого сервис / Что вы можете делать |
| Client | Клиенты заходят по приглашению тренера. |
| Footer trial | …пробный период 60 дней… (см. §6.2 T-TRIAL) |

**Сейчас в `welcome.blade.php` расхождения** (привести к §6.2): lead про «питания файлами», буллеты про «файлы» вместо программ тренировок — **исправить**.

---

## 4. Дизайн v2 (финальные требования)

### 4.1. Общее

| Параметр | Значение |
|----------|----------|
| Layout | `public/layout.blade.php`: `html.theme-pro`, `@vite(['resources/css/app.css'])` |
| Колонка | `max-width: 40rem`, центр, `--page-px` |
| Фон | `bg-background` (#F8FAFC), **без** градиента/noise старого welcome |
| Шрифт | Geist из `app.css` |

### 4.2. Шапка

```
[logo 40] Телотрон          [ Начать бесплатно ]   ← desktop ≥640px
```

| Правило | Деталь |
|---------|--------|
| Компонент | `partials/telotron-public-header-landing` |
| Без подписи «Pro» | Только «Телотрон» |
| CTA desktop | `.telotron-public-btn-primary`, не full-width |
| CTA mobile | **Скрыть** в header; CTA только в hero (уже так) |

### 4.3. Hero (акцентный блок)

Обернуть H1 + lead + CTA в **карточку**:

| Свойство | Значение |
|----------|----------|
| Контейнер | `.telotron-card` или новый `.telotron-public-hero-card` |
| Фон | `bg-card`, `border border-border`, `rounded-[var(--radius-lg)]` |
| Акцент | опционально `border-primary/20` или `bg-primary/5` |
| Padding | 20–24px |
| H1 | `.telotron-h1`; на landing допустим модификатор **крупнее**: `text-xl` / `1.375rem` только для `.telotron-public-landing-hero h1` |
| CTA | `.telotron-public-btn-primary`, mobile **full-width**, desktop `max-w-[20rem]` |

Если CTA недоступен (`$ctaUrl === null`) — **не** голый текст; блок `.telotron-public-notice` (muted, border dashed).

### 4.4. Секции «Для кого» и «Возможности»

**Не** сплошные `<ul>` на всю ширину.

| Секция | Вёрстка |
|--------|---------|
| «Для кого» | Вводный абзац + **сетка 2×2** карточек-пунктов на `sm+`, на mobile — столбец |
| «Что вы можете делать» | **5 карточек** в колонке или 2 колонки на `sm+` |

**Карточка пункта** (новый класс `.telotron-public-feature-card`):

- `rounded-lg border border-border/60 bg-muted/10 px-3 py-2.5`
- Слева маркер: круг 6px `bg-primary` **или** иконка Lucide 16px в inline SVG (Users, Calendar, Dumbbell, FileText, Check) — **без** npm на blade: inline SVG из heroicons/lucide path в partial
- Текст: `text-sm text-foreground`

**Отступы между секциями:** `gap: var(--section-gap)` (24px) в `.telotron-public-landing-main`.

### 4.5. Блок «Клиенты»

Одна строка, `text-sm text-muted-foreground`, **без** карточки; можно с иконкой `UserPlus` 16px muted.

### 4.6. Footer

| Элемент | Стиль |
|---------|--------|
| Контейнер | `.telotron-public-footer`: `border-t`, `pt-6`, `mt-10` |
| Триал / медицина | `text-xs text-muted-foreground` |
| Ссылки | `.telotron-public-footer-links a` — **primary**, не дефолтный синий браузера |
| Реквизиты | `text-xs`, компактно, переносы на mobile |

### 4.7. Юридические страницы

`/legal/privacy`, `/legal/terms` — тот же `public/layout` + `.telotron-public-legal__body`; регрессия не ломать.

---

## 5. Техническая реализация

### 5.1. Файлы

| Файл | Действие |
|------|----------|
| `resources/views/public/welcome.blade.php` | Тексты §6.2; разметка hero-card + feature-grid |
| `resources/views/public/layout.blade.php` | Проверить `@vite`; при необходимости `@vite(['resources/css/app.css', ...])` |
| `resources/css/app.css` | Классы v2: `.telotron-public-hero-card`, `.telotron-public-feature-grid`, `.telotron-public-feature-card`, `.telotron-public-notice` |
| `resources/views/partials/telotron-public-header-landing.blade.php` | Без изменений логики, только если нужны отступы |
| `tests/Feature/Public/PublicWelcomePageTest.php` | Обновить строки при смене copy на §6.2 |
| `database/seeders/TelotronWebsiteInviteSeeder.php` | Убедиться в `DatabaseSeeder` для локали |

**Не трогать:** `build.pro` / `build.client` (это не PWA).

### 5.2. CSS в dev и prod

| Среда | Действие |
|-------|----------|
| **Локально** | После правок `app.css`: `docker compose exec -u sail laravel.test npm run build` **или** `npm run dev` + `APP_ENV=local` |
| **Проверка** | В DevTools → Network есть загрузка `app-*.css` из `/build/assets/`, не 404 |
| **Прод** | CI/deploy включает `npm run build`; без build страница останется «сырой» |

Добавить в `docs/Техдок/04-платформа-и-эксплуатация/` короткую заметку **или** комментарий в README deploy: public blade зависит от Vite build.

### 5.3. CTA и seeder

| # | Требование |
|---|------------|
| S1 | `TelotronWebsiteInviteSeeder`: `platform_trainer_recruitment`, title **«С сайта telotron»**, owner **admin** |
| S2 | `PlatformWebsiteTrainerInvite` — не подставляет ссылку тренера (D4) |
| S3 | href = `route('public.invite_hub', $token)` |
| S4 | Нет ссылки — сообщение в UI, `Log::warning('public.welcome_missing_platform_invite')` |

### 5.4. Meta

```html
<title>Телотрон — сервис для фитнес-тренеров</title>
<meta name="description" content="Ведите клиентов, расписание и программы тренировок в одном сервисе. Начните бесплатный пробный период для тренеров.">
<meta name="theme-color" content="#1D4ED8">
```

---

## 6. Wireframe v2 (итог)

```
┌─────────────────────────────────────────┐
│ [logo] Телотрон          [Начать бесплатно] │
├─────────────────────────────────────────┤
│ ╭─────────────────────────────────────╮ │
│ │ H1                                  │ │
│ │ lead                                │ │
│ │ [ Начать бесплатно — full width ]   │ │
│ ╰─────────────────────────────────────╯ │
│ H2 Что такое…  (абзац)                  │
│ H2 Для кого…   (абзац)                  │
│ ┌──────────┐ ┌──────────┐             │
│ │ • пункт  │ │ • пункт  │  2×2 grid   │
│ └──────────┘ └──────────┘             │
│ H2 Что вы можете…                       │
│ ┌ пункт ┐ ┌ пункт ┐                     │
│ └ …     └ …     (5 cards)               │
│ Клиенты заходят по приглашению…        │
├─────────────────────────────────────────┤
│ footer: trial · disclaimer · links      │
└─────────────────────────────────────────┘
```

---

## 7. Критерии приёмки

### 7.1. Визуал

- [ ] На `telotron.test/` / prod: **фон** `#F8FAFC`, **кнопка** синяя pill, **не** системный `<a>` синий.
- [ ] Hero в **карточке** с отступами; H1 читается как заголовок, не как body.
- [ ] Пункты «Для кого» и «Возможности» — **карточки/сетка**, не голый маркированный список на всю ширину.
- [ ] Footer: ссылки **primary**, реквизиты компактно.
- [ ] 360px: без горизонтального скролла; CTA виден в первом экране (hero).

### 7.2. Контент и функционал

- [ ] Тексты соответствуют **ТЗ A13 §6.2** (или обновлены тесты по согласованию).
- [ ] CTA ведёт на `/i/{token}` admin platform link.
- [ ] Нет прямых ссылок на `pro.telotron.ru` / `client.` в CTA.
- [ ] `/legal/privacy` и `/legal/terms` — 200, стилизованы.

### 7.3. Тесты и сборка

- [ ] `php artisan test --filter=PublicWelcomePageTest` (в контейнере Sail).
- [ ] `npm run build` в контейнере; в HTML есть link на собранный CSS.
- [ ] Регрессия: `DomainRoutingTest` public welcome.

### 7.4. Вне scope

- [ ] Тарифы, аналитика, og:image, полноценный маркетинговый лендинг (C7).
- [ ] Изменение логики invite / регистрации.

---

## 8. Приоритет и оценка

**P0** для gate **01.06** (MAX + первое впечатление).

**Оценка:** 1–1,5 дня (вёрстка v2 + проверка Vite + выравнивание текстов с §6.2).

---

## 9. Журнал

| Дата | Изменение |
|------|-----------|
| 2026-05-21 | Задание v2: плоский UI + риск без Vite build; карточки hero/features |
