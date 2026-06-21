# Задание разработчику: public-страница A13 (период 0)

**Статус:** **P0** — gate деплоя **01.06.2026**  
**Владелец:** разработчик (03)  
**Приёмка:** дизайнер (визуал §7.1) · маркетолог (тексты §6.2 ТЗ) · юрист (footer §4 ТЗ) · тестировщик (smoke)

## Канон (читать в порядке)

| # | Документ | Что брать |
|---|----------|-----------|
| 1 | [ТЗ — public-страница (A13)](../../01-Директор/Инструкции/ТЗ%20—%20public-страница%20проекта%20(A13).md) | **§0** решения директора · **§6.2** тексты (копипаст) · **§6.3–6.5** CTA, юр. URL, приёмка |
| 2 | [Задание дизайнера — вёрстка v2](../../08-Дизайнер/Инструкции/Задание%20разработчику%20—%20public-страница%20A13%20вёрстка%20и%20дизайн%20v2.md) | **§4–7** layout, CSS, wireframe, чеклист визуала |
| 3 | [план-доработки-период-0 §1.2](../../../_telotron.ru/docs/Техдок/00-мета/план-доработки-период-0.md) | Нумерация задач **13.0–13.4** |

**Правило конфликта:** тексты — **ТЗ §6.2**; визуал и разметка — **дизайн v2**. Расхождение с тестами — только после ревью маркетолога/директора.

---

## Текущее состояние кода (май 2026)

**База есть:** `PublicWelcomeController`, `public/welcome.blade.php`, `TelotronWebsiteInviteSeeder`, `PlatformWebsiteTrainerInvite`, тесты `PublicWelcomePageTest`.

**Осталось для gate A13:**

1. Тексты — **дословно ТЗ §6.2** (сейчас есть расхождения: H1 «…приложении», lead, формулировки MVP «файлами»).
2. Визуал — чеклист [дизайн v2 §7](../../08-Дизайнер/Инструкции/Задание%20разработчику%20—%20public-страница%20A13%20вёрстка%20и%20дизайн%20v2.md) (CSS/Vite build, feature-grid).
3. Приёмка маркетолог / юрист / дизайнер по ТЗ.

---

## Цель

Довести **A13** до приёмки: `https://telotron.ru/` — рабочая страница, CTA **«Начать бесплатно»** → **`/i/{token}`** (admin, «С сайта telotron»), стили `theme-pro` + Vite `app.css`.

**Вне scope:** тарифы (период I), аналитика, og:image, маркетинговая витрина C7.

---

## Чеклист задач

### 13.0 · Seeder и CTA (D3–D4)

| ☐ | Задача | Критерий |
|---|--------|----------|
| ☐ | `TelotronWebsiteInviteSeeder` (или актуальное имя) в `DatabaseSeeder` | После `db:seed`: запись `platform_trainer_recruitment`, **title = «С сайта telotron»**, owner — **admin** |
| ☐ | Idempotent seeder | Повторный seed не дублирует активную ссылку |
| ☐ | `PlatformWebsiteTrainerInvite` / resolver для welcome | Только **admin** + `platform_trainer_recruitment` + точный title; **не** `specialist_referral` тренера |
| ☐ | href CTA | `route('public.invite_hub', ['token' => $token])` |
| ☐ | Нет ссылки | UI: `.telotron-public-notice`; `Log::warning('public.welcome_missing_platform_invite')` — **не** битый href |

### 13.1 · Страница и контент

| ☐ | Задача | Критерий |
|---|--------|----------|
| ☐ | `PublicWelcomeController` + `resources/views/public/welcome.blade.php` | `GET /` на public-домене, без auth |
| ☐ | Тексты | **Дословно** ТЗ §6.2 (раздел «6.2 Контент страницы») |
| ☐ | Строка Client | «Клиенты заходят по приглашению тренера.» |
| ☐ | Footer | T-TRIAL, T-MED, ссылки `/legal/privacy`, `/legal/terms`, реквизиты §6.2 |
| ☐ | Нет CTA на `pro.` / `client.` | Только `/i/{token}` |

### 13.2 · MAX

| ☐ | Канонический URL | `https://telotron.ru/` — см. [max-бот-прод-страница](../../../_telotron.ru/docs/Техдок/03-модули/max-бот-прод-страница-и-интеграция.md) |

### 13.3 · Дизайн v2 + CSS

| ☐ | Задача | Критерий |
|---|--------|----------|
| ☐ | `public/layout.blade.php` | `html.theme-pro`, `@vite(['resources/css/app.css'])` |
| ☐ | Hero | Карточка `.telotron-public-hero-card`, pill CTA |
| ☐ | Секции | Feature-grid для «Для кого» / «Возможности» — [дизайн v2 §4.4](../../08-Дизайнер/Инструкции/Задание%20разработчику%20—%20public-страница%20A13%20вёрстка%20и%20дизайн%20v2.md) |
| ☐ | `app.css` | Классы v2: hero-card, feature-grid, feature-card, notice |
| ☐ | **Vite build** | `docker compose exec -u sail laravel.test npm run build` — без build страница «сырая» |
| ☐ | Meta | title, description, `theme-color` #1D4ED8 — [дизайн v2 §5.4](../../08-Дизайнер/Инструкции/Задание%20разработчику%20—%20public-страница%20A13%20вёрстка%20и%20дизайн%20v2.md) |
| ☐ | Адаптив | 360px и 1280px, CTA в hero на mobile |

### 13.4 · Тесты

| ☐ | Команда | Критерий |
|---|---------|----------|
| ☐ | `php artisan test --filter=PublicWelcomePageTest` | green (контейнер Sail) |
| ☐ | `DomainRoutingTest` | public welcome не сломан |
| ☐ | `/legal/privacy`, `/legal/terms` | 200, layout public |

---

## Файлы (ориентир)

| Файл | Назначение |
|------|------------|
| `app/Http/Controllers/Public/PublicWelcomeController.php` | CTA URL |
| `app/Modules/Invites/.../PlatformWebsiteTrainerInvite.php` | Резолв ссылки (D4) |
| `database/seeders/TelotronWebsiteInviteSeeder.php` | 13.0 |
| `resources/views/public/welcome.blade.php` | Контент + разметка v2 |
| `resources/views/public/layout.blade.php` | Vite + theme-pro |
| `resources/views/partials/telotron-public-header-landing.blade.php` | Шапка |
| `resources/css/app.css` | Стили landing |
| `tests/Feature/Public/PublicWelcomePageTest.php` | Приёмка |
| `routes/web.php` | `GET /`, legal routes |

**Не трогать без причины:** `config/version.php` `build.pro` / `build.client` (не PWA public).

---

## Команды (из `_telotron.ru/`)

```bash
docker compose exec -u sail -T laravel.test php artisan db:seed --class=TelotronWebsiteInviteSeeder
docker compose exec -u sail -T laravel.test php artisan test --filter=PublicWelcomePageTest
docker compose exec -u sail laravel.test npm run build
```

---

## Связанные задания (не A13, но рядом)

| Задание | Статус |
|---------|--------|
| [Единый стиль install и auth](../../08-Дизайнер/Инструкции/Задание%20разработчику%20—%20единый%20стиль%20install%20и%20auth.md) | Отдельный P0/P1 — не блокирует A13, но общий визуал |
| A10 `trial_ends_at` | Параллельно период 0 |
| A9 юр. тексты в `legal_documents` | Footer ссылки должны открываться |

---

## Журнал

| Дата | Изменение |
|------|-----------|
| 2026-05-21 | Задание создано: синтез ТЗ A13 + дизайн v2 + план 13.0–13.4 |
