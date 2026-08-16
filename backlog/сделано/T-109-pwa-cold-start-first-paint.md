# T-109 · PWA cold-start: ускорить отрисовку первого экрана (Pro + Client)

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** |
| **Эпик** | — (платформа / PWA; стык с frontend offline) |
| **Приоритет** | **P1** |
| **Спринт** | — |
| **Роль** | **разработчик (03)** · review: архитектор при split shell |
| **Создан** | 2026-08-08 |
| **Оценка** | 5–8 SP |
| **Источник** | аудит cold-start 2026-08-08 (директор → агент) |

> При взятии в работу: перенести в **`в-работе/`**, статус `in_progress`.  
> **Имя файла:** без пробелов.

---

## Контекст

На cold start авторизованный пользователь долго видит **пустой** `#telotron-spa`: HTML без skeleton → блокирующий CSS + Google Fonts `@import` → eager JS (~400KB) → **`await auth.hydrateIfNeeded()` до `app.mount()`** (последовательно `GET /ping` → `GET /me`) → lazy chunk → API экрана.

**Client** тяжелее: `warmupClientOfflineBundles()` (в т.ч. calendar ~557KB) конкурирует с home API; fan-out `linked-trainers` / `reminder-inbox` / calendar / chart.  
**Pro** проще (clients list), но тоже блокируется hydrate и тянет Client offline (Dexie) через shared shell.

Цель: раньше показать **осмысленный кадр** (shell / skeleton), сократить сеть до first paint, не ломая auth, offline, SW.

---

## Проблема (критический путь)

1. Blade: пустой `#telotron-spa` (`resources/views/{pro,client}/layout.blade.php`)
2. `resources/css/app.css` — `@import` Geist с fonts.googleapis.com
3. Eager entry ~400KB; shared shell тянет Dexie / Client offline **в Pro**
4. `resources/ts/app/{pro,client}/main.ts` — `await auth.hydrateIfNeeded()` **перед** `app.mount()`
5. Lazy route + page APIs
6. Client: `warmup-client-offline-bundles.ts` сразу после auth

---

## Scope

### P0 — разблокировать paint

1. **Не блокировать mount на hydrate**  
   - Shell / skeleton сразу; hydrate в фоне.  
   - Guards / страницы учитывают `auth.status === 'unknown'` (spinner внутри shell, не белый экран, без мигания login).  
   - Редиректы: guest → login, incomplete register, legal, client anketa — без регрессий.

2. **Blade splash / skeleton** в `#telotron-spa` до JS (логотип + «Загрузка…»); убрать при mount.

3. **Шрифты**  
   - Убрать `@import` Google Fonts из `app.css`.  
   - Self-host Geist или non-blocking `link` + `font-display: swap`.

### P1 — JS graph и Client boot

4. **Развязать Pro shell от Client offline**  
   - Dexie / `client-offline` / Client trainer header не в Pro entry graph (zone-split или lazy Client-only).  
   - Проверка: после `npm run build` Pro бандл без Dexie.

5. **Client warmup**  
   - Не в том же тике, что mount home: `requestIdleCallback` / после first paint / после home summary.  
   - Calendar chunk не качать на каждом cold start без захода в календарь.

6. **Свести дубли API на Client boot**  
   - Один `linked-trainers`.  
   - Progressive home: greeting/shell → summary (calendar/chart не обязаны блокировать первый кадр).

### P2 (тот же PR или follow-up)

7. SW precache не усугубляет first paint (register уже non-blocking — проверить приоритет).  
8. Короткая заметка в техдок (frontend / offline зоны) про boot sequence.

---

## Вне scope

- Redesign IA / новые экраны  
- Смена контракта `/me` без нужды  
- Filament Admin  
- Micro-frontends  

---

## Критерии готовности

- [x] Cold start (auth): до shell нет длительного белого экрана без индикатора (Blade skeleton и/или Vue shell).
- [x] `hydrateIfNeeded` не единственный gate перед `app.mount()` без UI.
- [x] В `app.css` нет `@import` на `fonts.googleapis.com`.
- [x] Pro production entry **не** включает Dexie / client-offline (bundle graph / grep после build).
- [x] Client: warmup calendar отложен (idle / после first paint), не синхронно с mount home.
- [x] Регрессии зелёные: Vitest 408; контракт T-109; E2E smoke (см. журнал).
- [x] Before/after: Pro static graph без Dexie; Pro `main` ~15KB entry (+ shared chunks); Client calendar не в cold warmup.
- [x] Журнал тикета: что сделано по P0/P1; P2 — сделано.

---

## Технические якоря

| Файл | Роль |
|------|------|
| `resources/ts/app/{pro,client}/main.ts` | mount vs hydrate |
| `resources/ts/shared/stores/auth-session.ts` | `/ping` + `/me` |
| `resources/ts/widgets/TelotronAppShell.vue` | eager imports |
| `resources/ts/shared/pwa/warmup-client-offline-bundles.ts` | Client warmup |
| `resources/css/app.css` | fonts |
| `resources/views/{pro,client}/layout.blade.php` | SPA root / SW |

Команды: только через Docker Sail (`docker compose exec -u sail …` из `_telotron.ru/`).

---

## Ссылки

- Frontend / offline: `_telotron.ru/docs/Техдок/01-канон-mvp/frontend-архитектура-и-стек-mvp.md`
- Зоны SW: `docs/Техдок/02-зоны/pro/зона-pro-offline-и-версии.md`, `…/client/зона-client-offline-и-версии.md`
- Аудит: чат директора 2026-08-08 (cold-start Pro+Client)

---

## Риски

- Guards и `auth.status === 'unknown'` — без мигания login / ложного guest.
- Не сломать Client outbox / offline после отложенного warmup и shell split.
- После zone-split shell — reminder bell / trainer header на Client.

---

## Журнал

### 2026-08-08

- Тикет заведён в `бэклог/` по запросу директора (сформулировать задачу разработчику → сделать тикет).
- Scope: P0 paint unblock + fonts; P1 Pro/Client bundle split + Client warmup/API; метрики в PR.

### 2026-08-08 · реализация

**P0:** Blade splash (`partials/telotron-spa-boot`); Geist self-host (`@fontsource-variable/geist`); `main.ts` mount без `await hydrate` (guard ждёт); shell boot при `unknown`.

**P1:** Client trainer header / reminder sheet — `defineAsyncComponent` (Pro static graph **без Dexie**); `scheduleClientOfflineWarmup` idle, calendar убран из cold warmup; `linked-trainers` через store `ensureLoaded` (+ booking); home — calendar раньше chart, warmup после summary.

**P2:** заметка cold start в `frontend-архитектура-и-стек-mvp.md`; SW register без изменений (уже non-blocking).

**Проверки:** Vitest 408; E2E grep `pro registration|client` — 14 passed; `build.pro` 249 / `build.client` 236.
