# T-047 · Commerce: публичная страница тарифов (telotron.ru)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [T-026](T-026-commerce-модуль-эпик.md) |
| **Приоритет** | P2 (маркетинг public; не блокер платежей **01.08**) |
| **Спринт** | 3–4 (можно параллельно с T-031 после конфигов) |
| **Роль** | dev |
| **Создан** | 2026-06-12 |
| **Оценка** | 6–8 ч |
| **Зависит от** | [T-031](T-031-commerce-gating-api.md)* (конфиг `tariff-capabilities`), [T-028](T-028-commerce-тарифы-статусы-триал.md)* (цены из БД) |

\* **MVP без полного Commerce:** страницу можно выпустить раньше на `fallback_prices` из конфига; после T-028 подключить активные строки `commerce_tariff_prices`. Конфиг capabilities — общий с T-031 (не дублировать матрицу в Blade).

## Контекст

На **public**-домене (`telotron.ru`) нужна **отдельная SSR-страница** с таблицей тарифов **Лайт / Профи / Максимальный**: цены и **включённые модули** (capabilities). Единый источник матрицы — `config/commerce/tariff-capabilities.php` (тот же, что для gating и Pro UI).

Канон: [commerce-модуль-тз-mvp §9.4](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md), [домены-маршруты-сессии](../../_telotron.ru/docs/Техдок/02-зоны/домены-маршруты-сессии.md), [матрица-тарифов-платформа](../../_telotron.ru/docs/Бизнес-требования/00-канон-mvp/матрица-тарифов-платформа.md).

## Что сделать

### Маршрут и контроллер

- `GET /tariffs` в `routes/web.php` (public-домен), имя **`public.tariffs`**.
- `PublicTariffsController` (invokable), стиль A13 как `PublicWelcomeController`.
- View: `resources/views/public/tariffs.blade.php`, layout `public.layout`.

### Конфиги (если ещё нет после T-031)

| Файл | Содержание |
|------|------------|
| `config/commerce/tariff-capabilities.php` | `light` / `pro` / `max` → bool по ключам (`groups`, `partner`, `invites_multi_link`, `growth_*`, …) |
| `config/commerce/public-tariff-labels.php` | подписи строк для public, `order`, опц. `section` |
| `config/commerce/public-tariffs.php` | названия тарифов, `tariff_order`, тексты страницы, **`fallback_prices`** до появления БД |

Минимум capabilities на MVP: **`groups=false` на Лайте** (B4 ADR-001); остальное — по матрице PO / T-005.

### Сбор данных

- `App\Modules\Commerce\Support\PublicTariffPageDataBuilder`:
  - строки таблицы — из `tariff-capabilities` + labels (сортировка по `order`);
  - цены — **активные** `commerce_tariff_prices`, если таблица есть; иначе `public-tariffs.fallback_prices`;
  - формат цены Лайта: «0 ₽»; платные — «N ₽ / 30 дн.» + footnote про ежедневное списание (1 Ед. = 1 ₽).

### UI

- Таблица: колонки — тарифы, строки — модули; ячейки ✓ / — (accessible: `aria-label`).
- Горизонтальный scroll на узких экранах (классы в `app.css`, префикс `telotron-public-tariffs-*`).
- CTA «Начать бесплатно» — тот же `PlatformWebsiteTrainerInvite` / hub, что на `/`.
- Ссылки **«Тарифы»**: секция на landing `/` + пункт в `telotron-public-footer`.
- `PublicSiteViewData`: `tariffsUrl` для footer/landing.

### Тесты

- Feature-тест `PublicTariffsPageTest`:
  - `GET https://telotron.test/tariffs` → 200;
  - видны названия трёх тарифов и ключевые строки (например «Группы», «Партнёрская программа»);
  - матрица совпадает с конфигом (✓ на Профи для `groups`, — на Лайте);
  - цены из fallback (до миграций) или из seeder (после T-028).

## Критерии готовности

- [ ] Маршрут `public.tariffs`, страница без auth.
- [ ] Таблица строится **только** из конфига capabilities + labels (не хардкод в Blade).
- [ ] Цены: БД при наличии, иначе fallback.
- [ ] Навигация с `/` и footer.
- [ ] Feature-тест(ы) green.
- [ ] `npm run build` под `-u sail` (если менялся CSS).

## Вне scope

- Pro UI тарифов (T-033), checkout, купоны.
- Client/public API JSON для тарифов.
- Юридические тексты оферты по подписке (ждёт юриста).

## Ссылки

- [commerce-модуль-тз-mvp §3.2, §9.4](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)
- [commerce-схема §3](../../_telotron.ru/docs/Техдок/03-модули/commerce-схема-данных-mvp.md) — `commerce_tariff_prices`
- [PublicWelcomeController](../../_telotron.ru/app/Http/Controllers/Public/PublicWelcomeController.php) — образец A13

## Журнал

### 2026-06-12

- Тикет от архитектора: public `/tariffs`, конфиг capabilities, без дублирования gating-матрицы.
