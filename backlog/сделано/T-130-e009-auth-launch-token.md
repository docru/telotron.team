# T-130 · E-009 · Auth launchToken: verify VK sign → Bearer

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** · код в ветке `initiative/i-001-modul-prodazh` (26.09), не в `main` |
| **Эпик** | [E-009](../эпики/E-009-кросплатформенность.md) · этап 7 |
| **Приоритет** | **P0** |
| **Спринт** | — |
| **Роль** | arch + dev (Identity) |
| **Создан** | 2026-09-24 |
| **Обновлён** | 2026-09-26 |
| **Зависит от** | [T-133](T-133-e009-identity-credentials.md) (**blocker**), ADR-008 §4 |
| **Блокирует** | [T-131](T-131-e009-vk-adapter-пилот.md) |

## Контекст

В host-средах cookie SPA ненадёжны. Нужен серверный путь: verify подписанного launch (`sign` / позже initData) → **наша** сессия (Bearer или эквивалент) для Pro/Client API. PWA cookie path **не ломать**.

**Предусловие:** [T-133](T-133-e009-identity-credentials.md) — User без обязательного телефона; credential типа `vk` (и др.).

## Критерии готовности

- [x] Конфиг секрета VK Mini App (не в фронте); staging ≠ prod (env Pro/Client)
- [x] Endpoint exchange: `POST /api/v1/auth/{pro\|client}/launch/vk` → verify HMAC/`sign`, TTL `vk_ts` → Sanctum token
- [x] `pwa.auth` принимает Bearer **рядом** с session cookie (зона должна совпадать)
- [x] Найти/создать User по **credential `vk`**, не по phone; телефон не требовать
- [x] Не доверять client-only данным; не вечный проброс raw launch
- [x] Feature-тесты: valid/invalid/expired sign; User без phone; изоляция зон
- [x] Документация `api-http` § auth host / E-009
- [x] Заготовка интерфейса verify для MAX/TG (`StubHostLaunchParamsVerifier`)

## Вне scope

- OTP-боты MAX/TG (другой контур)
- Полный Ok/Max/Telegram adapter
- UI логина Mini App (его нет — T-131)
- Модель credentials (T-133) — сделано ранее

## Уточнить при старте (коротко)

| # | Вопрос | Решение |
|---|--------|---------|
| 1 | Зона пилота token path | **Client и Pro** |
| 2 | Автосоздание User по новому `vk` | да, без телефона (`VK_MINI_APP_AUTO_CREATE_USER`) |
| 3 | Где Bearer | **sessionStorage** (клиент — T-131 `VkAdapter`) |

## Ссылки

- ADR-008 §4 · `config/host_launch.php` · `App\Modules\Identity\HostLaunch\*`

## Журнал

### 2026-09-29

- Перенесён в `сделано/` при актуализации бэклога: код в ветке `initiative/i-001-modul-prodazh` (26.09), не в `main`.

### 2026-09-26

- `VkLaunchParamsVerifier` + `HostLaunchAuthExchange` + controller; Bearer в `PwaZoneAuth`; тесты `HostLaunchVkAuthTest`; api-http; `.env.example`.

### 2026-09-24

- Тикет создан.
