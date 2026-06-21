# План реализации: пригласительные ссылки и хаб `/i/{token}`

Документ связывает исследования (`invite-links-voprosy-i-otvety.md`, `invite-tokens-ulid-pk-i-public-token.md`) с кодом в `_telotron.ru/` и техдоком.

## Сделано (MVP-код)

- Таблица `invite_tokens`: PK `id`, колонка `token` (строка **6–10** символов `A–Za–z0–9`), **уникальный индекс `(purpose, token)`** (миграция `2026_05_14_140001_invite_tokens_purpose_token_unique.php`), `purpose`, `owner_user_id`, `revoked_at`, soft delete.
- Генератор **`InvitePublicTokenGenerator`**: алфавит 62 символа, длина от `COUNT(*)` по ступенчатой таблице (§2 исследования), `L_max=10`; используется в **`InviteTokenService`** и **`InviteTokenProvisioner`**.
- Пути **`/i/{token}`** (маршрут `where`: **6–10** `A–Za–z0–9`): зона **Pro** — лендинг для `specialist_referral` и `platform_trainer_recruitment` (разные ключи `localStorage`); зона **Client** — `client_onboarding`; общий blade `invite.invite-landing`.
- Публичный домен: **`GET /i/{token}`** → `PublicInviteHubController` (`public.invite_hub`) — редирект в зону по `purpose`.
- **Антиабьюз:** **`InviteInvalidLandingThrottle`** — при 404 на хабе и лендингах задержка по экспоненте от числа неудач с IP, счётчик в **кэше** (`CACHE_STORE`, в проде обычно Redis), TTL сутки; успех сбрасывает счётчик; настройки **`config/invites.php`** / env (`INVITE_I404_*`).
- **Логи успеха:** `invite.hub_redirect`, `invite.landing_opened` (без полного токена, только префикс и `purpose`).
- URL для Filament: `PlatformTrainerRecruitmentInviteUrl` → **public** хаб.
- Тесты: `PublicInviteHubTest`, `PlatformTrainerInviteLandingTest`, `PlatformTrainerRecruitmentInviteUrlTest`, `InviteInvalidLandingThrottleTest`, `InvitePublicTokenGeneratorTest`; в `phpunit.xml` — `INVITE_I404_BASE_MS=0`.

## Осталось (по желанию / следующие этапы)

### PK = ULID вместо bigint

- По `invite-tokens-ulid-pk-i-public-token.md`: замена `id`, правки всех FK (`trainer_clients`, `referral_attributions`, `otp_challenges`, аудит) — отдельная миграция и релиз.

### SPA и продуктовый онбординг

- Pro: Passkey+OTP + чтение токена из `localStorage` по нужному ключу.
- Client: сценарий после логина (частично уже есть API `trainer-invites/accept`).

### Документация

- При смене контракта — `api-http-контракт-mvp.md` §10, `домены-маршруты-сессии.md` (актуализированы под короткий токен и антиабьюз).
- PWA: правки офлайн-оболочки зоны — см. `config/version.php`.

## Критерии регрессии после правок

- Хаб + лендинги + API создания/принятия токена + Filament URL.
- Миграции с нуля: `migrate:fresh` + полный `php artisan test` в контейнере.
