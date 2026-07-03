# T-068 · Упрощение входа · страница телефона, localStorage, API, профиль, прерванный reg

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [T-066](T-066-упрощение-входа-эпик.md) · **Упрощение входа** |
| **Зона** | страница телефона · рег. **шаг 2** (профиль) · прогресс reg · post-reg каналы |
| **Приоритет** | P1 |
| **Оценка** | **18–24 ч** |
| **Роль** | dev |
| **Создан** | 2026-06-25 |

> **Старт после gate** [T-066](T-066-упрощение-входа-эпик.md) (юрист). **Scope v1 — только Pro.** Client — старые пути без изменений.

Канон и тех. решения: [T-066 § тех. Q&A](T-066-упрощение-входа-эпик.md) (#1…#16).

## Контекст

- Страница телефона: СМС Aero, оферта + 18+, вход по СМС или по ключу (условия в localStorage).
- Регистрация: 3 шага после СМС (формальности → профиль → ключ). Рег. шаг 1 UI — [T-069](T-069-упрощение-входа-legal-одна-страница.md); рег. шаг 3 — [T-071](T-071-упрощение-входа-passkey-опционально.md).
- Старые Pro API (`register/draft`, `register/otp/*`, `passkey/login` + обязательный OTP, `recovery/*` через мессенджер) — **снять** ([T-066](T-066-упрощение-входа-эпик.md) Q&A #3, #8).

## localStorage (браузер)

| Ключ | Тип | Описание |
|------|-----|----------|
| `telotron.auth.remembered_phone_e164` | string | Последний номер (E164) при отправке СМС |
| `telotron.auth.had_successful_login` | boolean | «Уже входил с этого устройства» |
| `telotron.auth.passkey_credential_hint` | string? | **Credential id** с этого устройства (Q&A #12) |

**Правила** ([T-066](T-066-упрощение-входа-эпик.md)):

- Показать кнопку ключа: remembered phone + `had_successful_login` + номер в поле совпадает + есть hint.
- **Отправка СМС:** перезаписать номер; сбросить `had_successful_login` и hint (**только** localStorage).
- **Вход по ключу:** storage **не менять**.
- **После успешного входа/завершения рег. шага 1:** `had_successful_login=true`.
- **После привязки ключа (рег. шаг 3 / профиль):** записать hint.
- Старый `telotron_pro_last_phone` — **не мигрировать** (Q&A #10).

Партнёрский токен в браузере — без изменений (`telotron.pro.*_invite.v1`).

## Сессия Laravel (сервер)

Заменить legacy `REGISTER_STEP1` / `REGISTER_LEGAL_SNAPSHOT` для Pro:

| Ключ сессии | Содержимое |
|-------------|------------|
| `telotron.spa.reg_phone_e164` | Нормализованный номер |
| `telotron.spa.reg_otp_challenge_id` | id challenge |
| `telotron.spa.reg_sms_verified` | `true` после успешного OTP (ветка reg) |
| `telotron.spa.reg_terms_snapshot` | `{ document_key, version, accepted_at }` для `terms_of_service` с шага телефона (Q&A #2) |
| `telotron.spa.reg_age_confirmed` | `true` если галочка 18+ на шаге телефона |

Сессия истекла до `register/complete` → с начала, новый СМС (Q&A #6). User в БД **не создаётся** до `register/complete`.

## API · Pro (новые пути)

Префикс: `/api/v1/auth/pro/`. Client — прежние маршруты.

### 1. Страница телефона · СМС

#### `POST /phone/start`

**Тело:**

```json
{
  "phone": "+79991234567",
  "age_confirmed": true
}
```

**Сервер:**

- Нормализация E164; `age_confirmed` обязателен.
- Фиксация в сессии: `reg_phone_e164`, снимок оферты (`reg_terms_snapshot` — актуальная опубликованная `terms_of_service`; UI «Продолжая…» на клиенте; запись в `legal_acceptances` **позже**, Q&A #2).
- SMS Aero + `otp_challenges`; rate limit.
- Вне production: в ответе `debug_otp` (Q&A #9).
- User **не создаётся**.

**Ответ:** `{ "status": "otp_sent", "debug_otp?": "123456" }`

#### `POST /phone/verify`

**Тело:** `{ "code": "123456" }`

**Ветка login** (User найден по `phone` + `site_zone=pro`):

- Sanctum session; `phone_verified_at` при необходимости.
- Вычислить `registration_incomplete` (Q&A #11, без поля в БД):
  - `step_2` — нет обязательных полей профиля (имя, фамилия, пол);
  - `step_3` — профиль полон, нет активного WebAuthn credential;
  - `null` — кабинет.
- Очистить reg-ключи сессии.

**Ответ login:**

```json
{
  "status": "logged_in",
  "registration_incomplete": "step_2" | "step_3" | null
}
```

**Ветка reg** (User не найден):

- `reg_sms_verified=true`; номер в сессии.
- User **не создаётся**.

**Ответ reg:** `{ "status": "registration_continue" }` → UI рег. шаг 1.

### 2. Вход по ключу (существующий номер)

[T-071](T-071-упрощение-входа-passkey-опционально.md) — отдельные `POST /passkey/login/options` + `/verify` **или** переиспользовать имена при полной замене старых Pro handlers.

- Только если на клиенте выполнены условия localStorage (Q&A #12).
- После verify — тот же `registration_incomplete`, что у СМС-login.
- **localStorage не менять** (Q&A #12).
- Recovery через MAX/TG/e-mail для Pro — **убрать** (Q&A #8).

### 3. Рег. шаг 1 · `POST /register/complete`

**Условие сессии:** `reg_sms_verified` + `reg_phone_e164` + `reg_terms_snapshot` + `reg_age_confirmed`.

**Тело:**

```json
{
  "acceptances": [
    { "document_key": "privacy_policy", "version": "v1.0" },
    { "document_key": "personal_data_consent", "version": "v1.0" }
  ],
  "device_id": "stable-uuid",
  "client_os": "Android 14",
  "idempotency_key": "uuid",
  "partner_invite_token": "optional-6-10-chars"
}
```

**Сервер (одна транзакция):**

1. Проверить session + полный набор документов Pro + `age_confirmed` из сессии.
2. Добавить к batch `terms_of_service` из `reg_terms_snapshot` (Q&A #2).
3. `LegalAcceptanceWriter::recordOnce`, context `registration`, audit [T-011](../сделано/T-011-legal-acceptances-audit-поля.md).
4. Создать `User` (`phone`, `site_zone=pro`, `phone_verified_at=now()`).
5. Создать **пустой** `trainer_profiles` (Q&A #14).
6. **Партнёр** (Q&A #1, #15, [T-072](T-072-invite-ссылки-код-wo-link-public.md)):
   - есть `partner_invite_token` в теле **или** токен из браузера (как сейчас) → обычная атрибуция;
   - иначе → активная ссылка с `link_code=wo_link` из конфига.
7. Sanctum login; очистить reg-ключи сессии.

**Идемпотентность:** `idempotency_key` на весь batch (повтор — без дубля User/acceptances).

**Ответ:** `{ "status": "logged_in", "registration_incomplete": "step_2" }`

### 4. Рег. шаг 2 · профиль

**`PATCH /api/v1/me/trainer-profile`** (существующий, Q&A #14).

- Обязательны: имя, фамилия, пол; дата рождения **не** обязательна (Pro).
- После успеха UI → рег. шаг 3.
- Прогресс на сервере: полнота профиля по полям (Q&A #11), отдельный флаг **не** вводим.

### 5. Прогресс регистрации (сервер + фронт)

Класс/сервис `ProRegistrationProgressResolver` (имя на усмотрение dev):

| Состояние | Условие | Куда вести |
|-----------|---------|------------|
| Нет User | — | Страница телефона |
| Нет профиля | нет имени/фамилии/пола | Рег. шаг 2 |
| Нет ключа | нет активного credential | Рег. шаг 3 (жёсткий guard, Q&A #5, #16) |
| Готово | всё есть | Кабинет |

- Guard маршрутов кабинета: при `step_3` доступен только wizard рег. шага 3 (+ logout).
- После login (СМС или ключ): редирект по таблице (Q&A #4, #5).

### 6. Legacy Pro (миграция)

- Data migration: `phone_verified_at = created_at` (или `now()`) для существующих Pro с credential (Q&A #7).
- Объём — единицы записей.

### 7. Снять для Pro (410 или удалить маршруты)

- `POST /register/draft`, `/register/otp/start`, `/register/otp/verify`, `/register/passkey/*`
- Старый login: обязательный Passkey → OTP
- `POST /recovery/*` (мессенджер/e-mail recovery)

Client — без изменений.

### 8. Смена телефона

`POST /me/phone/change/*` — вне критичного пути эпика; отдельный тикет по возможности.

## Страница телефона · UI (чеклист)

- [ ] Подстановка `remembered_phone_e164`.
- [ ] Оферта: «Продолжая, вы соглашаетесь…» + ссылка.
- [ ] Галочка 18+ обязательна.
- [ ] Кнопка ключа — по правилам localStorage.
- [ ] Сброс hint и `had_successful_login` при отправке СМС.
- [ ] После verify: login → отметка входа + редирект по `registration_incomplete`; reg → рег. шаг 1.

## Критерии готовности

### Страница телефона + localStorage

- [ ] Все правила показа/скрытия кнопки ключа.
- [ ] Поведение storage на СМС / вход по ключу.
- [ ] `debug_otp` только вне production.
- [ ] Feature-тесты: login vs reg; localStorage; сброс hint при СМС.

### `phone/start` + `phone/verify`

- [ ] SMS Aero; anti-fraud; User не создаётся на шаге телефона.
- [ ] Login: `registration_incomplete` step_2 / step_3 / null.
- [ ] Reg: session `sms_verified` без User.

### `register/complete`

- [ ] Транзакция User + пустой trainer_profile + acceptances (включая terms из сессии).
- [ ] Партнёр: токен в запросе/браузере **или** `wo_link` ([T-072](T-072-invite-ссылки-код-wo-link-public.md)).
- [ ] Idempotency; audit [T-011](../сделано/T-011-legal-acceptances-audit-поля.md).

### Рег. шаг 2

- [ ] `PATCH /me/trainer-profile`; обязательные имя, фамилия, пол.
- [ ] Незавершённый профиль → редирект на шаг 2 после входа.

### Прогресс + legacy

- [ ] `ProRegistrationProgressResolver` без поля `registration_step` в БД.
- [ ] Миграция `phone_verified_at` для legacy Pro.
- [ ] Старые Pro auth routes сняты; Client не затронут.

### Post-reg · каналы

- [ ] MAX/TG не на reg; мягкий nudge после кабинета.

### T-064

- [ ] SMS Pro + `phone_verified_at` + юрист → закрыть [T-064](T-064-auth-верификация-телефона-149-фз.md).

## Зависимости

- [T-069](T-069-упрощение-входа-legal-одна-страница.md) — UI рег. шага 1
- [T-071](T-071-упрощение-входа-passkey-опционально.md) — рег. шаг 3, вход по ключу, лимит 3 credential
- [T-072](T-072-invite-ссылки-код-wo-link-public.md) — `link_code`, `wo_link`
- [T-064](T-064-auth-верификация-телефона-149-фз.md)

## Журнал

### 2026-07-03 · синхрон с Q&A #1…#16

- Эскиз API переписан: session keys, `register/complete`, `ProRegistrationProgressResolver`, снятие legacy Pro routes.
- Профиль: только `PATCH /me/trainer-profile`; без `registration_step` в БД.
- Партнёр: токен или `wo_link`; `public` — через обычную ссылку в браузере.
- `debug_otp`, без миграции старого localStorage, legacy `phone_verified_at`.

### 2026-07-03

- 2 юрдока на рег. шаге 1 Pro; terms + 18+ на телефоне.

### 2026-06-25

- Первый эскиз API phone/start + register/complete.
