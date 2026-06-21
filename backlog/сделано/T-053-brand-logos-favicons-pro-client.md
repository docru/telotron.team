# T-053 Бренд · зонные логотипы и favicons (Pro / Client)

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Закрыт** | 2026-06-14 |
| **Очередь** | 4 · ~3–5 ч |
| **Приоритет** | P1 |
| **Спринт** | 0 |
| **Роль** | dev + дизайн (приёмка) |
| **Создан** | 2026-06-14 |

## Контекст

Утверждены **две цветовые версии** знака (форма одна):

| Зона | Мастер SVG | Знак |
|------|------------|------|
| **Pro** | `Команда/08-Дизайнер/logo/logo-pro.svg` | синий + красная «Т» |
| **Client** | `Команда/08-Дизайнер/logo/logo-client.svg` | зелёный + красная «Т» |

**PNG/ICO уже сгенерированы** и лежат в `public/` (см. [README](../../../_telotron.ru/public/brand/README.md)). Код **ещё не переключён**: везде один `/brand/logo.png` и общие `/favicons/*` (legacy = Pro).

**Цель:** Pro и Client PWA показывают **свой** логотип в UI и **свои** иконки во вкладке / «Добавить на экран» / precache SW.

Связь: [Стартовые выводы по бренду](../../08-Дизайнер/Инструкции/Стартовые%20выводы%20по%20бренду,%20логотипу%20и%20цветам.md), [логотип в шапке](../../08-Дизайнер/Инструкции/Задание%20разработчику%20—%20логотип%20в%20шапке%20кабинета.md), [T-018](../сделано/T-018-client-shell-header-trener.md) (шапка Client).

---

## 1. Готовые ассеты (не генерировать заново)

### UI — знак без подписи «ТЕЛОТРОН» (текст в шапке отдельно)

| Путь | Размер |
|------|--------|
| `public/brand/logo-pro.png` | 96×96 |
| `public/brand/logo-pro-128.png`, `logo-pro-256.png` | Retina |
| `public/brand/logo-client.png` | 96×96 |
| `public/brand/logo-client-128.png`, `logo-client-256.png` | Retina |
| `public/brand/logo-pro.svg`, `logo-client.svg` | полный мастер |

### Favicon / PWA

| Каталог | Файлы |
|---------|--------|
| `public/favicons/pro/` | `favicon-16x16.png`, `favicon-32x32.png`, `apple-touch-icon.png`, `android-chrome-192x192.png`, `android-chrome-512x512.png`, `favicon.ico` |
| `public/favicons/client/` | тот же набор |

### Пересборка после правки SVG

```bash
bash _telotron.ru/public/brand/sources/generate-brand-assets.sh
```

(ImageMagick `convert`; исходники mark-only: `public/brand/sources/icon-mark-{pro,client}.svg`.)

---

## 2. Канон путей в приложении

| Зона | Логотип UI | Favicon prefix |
|------|------------|----------------|
| **Pro** | `/brand/logo-pro.png` | `/favicons/pro/` |
| **Client** | `/brand/logo-client.png` | `/favicons/client/` |
| **Public A13** (`telotron.ru/`) | `/brand/logo-pro.png` | `/favicons/pro/` (нейтральная витрина платформы) |
| **Filament Admin** | `/brand/logo-pro.png` | `/favicons/pro/favicon.ico` |

**Удалить зависимость от legacy** `/brand/logo.png` и корневого `/favicon.ico` в Pro/Client layout — или оставить symlink/копию Pro только для обратной совместимости вне PWA (не смешивать зоны).

---

## 3. Решение (рекомендуемое)

### 3.1 PHP: единый хелпер зоны

Новый класс или методы в существующем PWA-сервисе, например `BrandAssets::logoPath('pro'|'client')`, `BrandAssets::faviconPrefix(...)`.

Использовать в:
- `PwaZoneShellService::manifestPayload()` — icons **512** из `android-chrome-512x512.png` (сейчас 192 подставлен дважды)
- `PwaZoneShellService::precachePaths()` — зонные logo + favicons

### 3.2 Blade layouts

| Файл | Правка |
|------|--------|
| `resources/views/pro/layout.blade.php` | favicon links → `/favicons/pro/…`, `favicon.ico` → `/favicons/pro/favicon.ico` |
| `resources/views/client/layout.blade.php` | → `/favicons/client/…` |
| `resources/views/public/layout.blade.php` | Pro (витрина) |
| `resources/views/partials/telotron-public-header.blade.php` | logo по зоне (передавать `$brandLogo` из layout) |
| `resources/views/partials/telotron-public-header-landing.blade.php` | `logo-pro.png` |
| `resources/views/pro/login.blade.php`, `client/login.blade.php` | зонный logo |
| `resources/views/public/welcome.blade.php` | `logo-pro.png` (если есть img logo) |

Вынести блок `<link rel="icon" …>` в partial `partials/telotron-favicons.blade.php` с параметром `$zone`.

### 3.3 Vue SPA

| Файл | Правка |
|------|--------|
| `TelotronPublicHeader.vue` | logo из prop или `import.meta`/inject зоны → `logo-pro` / `logo-client` |
| `TelotronAppShell.vue` | то же (сейчас hardcode `logo.png`) |

Опционально: `shared/brand-assets.ts` — `brandLogoSrc(zone: 'pro'|'client')`, `srcset` для 128/256.

### 3.4 Retina в шапке

Для `size-10` (40px) достаточно `logo-*-96.png`; при желании:

```html
<img src="/brand/logo-pro.png" srcset="/brand/logo-pro-128.png 2x" … />
```

### 3.5 Версия PWA

После смены путей в precache и layout:

- **`build.pro`** +1
- **`build.client`** +1

Иначе установленные PWA не подтянут новые иконки.

---

## 4. Матрица поверхностей

| Поверхность | Pro | Client |
|-------------|-----|--------|
| Install / login blade | logo-pro | logo-client |
| SPA auth (`TelotronPublicHeader`) | logo-pro | logo-client |
| Authenticated shell | logo-pro | logo-client |
| Tab favicon | favicons/pro | favicons/client |
| Apple touch / Android chrome | favicons/pro | favicons/client |
| `manifest.webmanifest` | icons pro | icons client |
| SW precache | pro paths | client paths |
| Public welcome | logo-pro | — |

---

## 5. Критерии готовности

- [x] Pro: во вкладке браузера и на «Добавить на экран» — **синий** знак; Client — **зелёный**
- [x] Шапка login + кабинет: Pro — `logo-pro.png`, Client — `logo-client.png`
- [x] Нет регрессии: `alt="Телотрон"`, размер ~40px в shell, `object-contain`
- [x] `manifest.webmanifest` Pro и Client отдают **разные** `icons[]` (512 использует реальный 512)
- [x] Precache SW включает зонные logo + favicons
- [x] Public A13 и Filament — Pro-ассеты
- [x] Legacy `/brand/logo.png` не используется в Pro/Client коде (или документирован как deprecated)
- [x] `build.pro` и `build.client` подняты
- [ ] Smoke: hard refresh / переустановка PWA на телефоне — иконка зоны верная
- [ ] Дизайн: sign-off по [Токены цветов](../../08-Дизайнер/Инструкции/Токены%20цветов%20—%20Pro%20и%20Client.md)

### Тесты (минимум)

- [x] Feature или unit: `PwaZoneShellService` manifest/precache для pro vs client содержат разные пути icons/logo
- [ ] При наличии — обновить e2e PWA smoke, если проверяют precache

---

## 6. Вне scope

- Новая отрисовка SVG (ассеты готовы)
- Maskable icons (`purpose: maskable`) — post-MVP
- Логотип в нижней tab bar
- Смена `theme_color` (уже зонная в manifest)
- Hero `brand/hero.png` на A13

---

## 7. Файлы (ориентир diff)

| Файл |
|------|
| `app/Modules/Identity/Pwa/PwaZoneShellService.php` |
| `app/Support/BrandAssets.php` (новый, опц.) |
| `resources/views/pro/layout.blade.php`, `client/layout.blade.php`, `public/layout.blade.php` |
| `resources/views/partials/telotron-public-header*.blade.php` |
| `resources/views/pro/login.blade.php`, `client/login.blade.php` |
| `resources/ts/widgets/TelotronPublicHeader.vue`, `TelotronAppShell.vue` |
| `resources/ts/shared/brand-assets.ts` (новый, опц.) |
| `app/Modules/Admin/Providers/AdminPanelProvider.php` |
| `config/version.php` |
| `tests/Unit/.../PwaZoneShellServiceTest.php` или Feature |

---

## Ссылки

- Ассеты: `_telotron.ru/public/brand/README.md`
- Дизайн SVG: `Команда/08-Дизайнер/logo/`
- Скрипт: `public/brand/sources/generate-brand-assets.sh`

---

## Журнал

### 2026-06-14

- Тикет: PNG/ICO сгенерированы, wiring в код — задача разработчика.

### 2026-06-14 (реализация)

- `BrandAssets`, partial `telotron-favicons`, зонные пути в layout/SPA/PWA manifest/precache.
- `build.pro` 140, `build.client` 163; тесты `BrandAssetsTest`, обновлён `DomainRoutingTest`.
