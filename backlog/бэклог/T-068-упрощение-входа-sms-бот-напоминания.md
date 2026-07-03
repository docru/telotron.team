# T-068 · Упрощение входа · страница телефона, localStorage, API, профиль, прерванный reg

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [T-066](T-066-упрощение-входа-эпик.md) · **Упрощение входа** |
| **Зона** | страница телефона · рег. **шаг 2** (профиль) · guard прерванного reg · post-reg каналы |
| **Приоритет** | P1 |
| **Оценка** | **18–24 ч** |
| **Роль** | dev |
| **Создан** | 2026-06-25 |

> **Старт после gate** [T-066](T-066-упрощение-входа-эпик.md). **Scope v1 — только Pro.**

## Контекст

Канон: [T-066 § страница телефона](T-066-упрощение-входа-эпик.md) · [§ localStorage](T-066-упрощение-входа-эпик.md) · [§ прерванная регистрация](T-066-упрощение-входа-эпик.md).

## localStorage · ключи (предложение dev)

| Ключ | Тип | Описание |
|------|-----|----------|
| `telotron.auth.remembered_phone_e164` | string | Последний номер с отправки OTP |
| `telotron.auth.had_successful_login` | boolean | «Ранее входил с этого устройства» |
| `telotron.auth.passkey_credential_hint` | string? | Id/hint для показа кнопки Passkey |

Правила чтения/записи — строго по канону T-066 (OTP сбрасывает отметку и hint; Passkey-login не трогает storage).

## Страница телефона · UI

- [ ] Подстановка `remembered_phone_e164` в поле.
- [ ] Текст `terms_of_service`: «Продолжая, вы соглашаетесь…» + ссылка.
- [ ] **Галочка 18+** обязательна перед OTP.
- [ ] Кнопка Passkey — только при выполнении всех условий канона.
- [ ] На **отправке OTP**: перезапись телефона; сброс `had_successful_login` и `passkey_credential_hint` (**только localStorage**, credential на сервере не трогаем).
- [ ] После OTP verify: login → `had_successful_login=true`; reg → session only.

## API · эскиз (Pro)

### Телефон + SMS (без User)

| Метод | Путь | После успеха |
|-------|------|--------------|
| `POST` | `/api/v1/auth/pro/phone/start` | `phone_e164`, `otp_challenge_id` в session |
| `POST` | `/api/v1/auth/pro/phone/verify` | login **или** `sms_verified=true` |

`phone/start`: SMS Aero; rate limit; anti-fraud. Тело может включать `terms_accepted`, `age_confirmed` для audit/session.

`phone/verify`:

- User **найден** → Sanctum; ответ + `registration_incomplete` (`step_2` | `step_3` | null).
- User **не найден** → `session[sms_verified]=true`, **без User**.

### Завершение рег. шага 1 (User + acceptances)

| Метод | Путь | Условие |
|-------|------|---------|
| `POST` | `/api/v1/auth/pro/register/complete` | session: `sms_verified` + `phone_e164` |

Тело: `acceptances[{document_key, version}]` — Pro: `privacy_policy`, `personal_data_consent` + `terms_of_service` (с шага телефона, session/audit), `age_confirmed`, `device_id`, `client_os`, `idempotency_key`, опц. `partner_invite_token`.

Транзакция: User + `phone_verified_at` + N × `legal_acceptances` + partner (invite как сейчас; **главный партнёр — out of scope**).

### Рег. шаг 2 · профиль

| Метод | Путь |
|-------|------|
| `PATCH` | `/api/v1/me/profile` или `POST /api/v1/auth/pro/register/profile` |

Имя, фамилия, пол обяз.; **ДР опциональна** для Pro. Флаг `registration_profile_completed`.

### Login (существующий номер)

Passkey — [T-071](T-071-упрощение-входа-passkey-опционально.md). При Passkey-login **не** менять localStorage.

### Guard прерванной регистрации

- [ ] Поле на User: `registration_step` (`legal_pending` | `profile_pending` | `passkey_pending` | `complete`) или эквивалент.
- [ ] Прерван до рег. шага 1: нет User — только новый OTP.
- [ ] После login: redirect на незавершённый шаг 2 или 3.

### Смена телефона (вне критичного пути эпика)

`POST /api/v1/me/phone/change/start` + `verify` — по возможности в этом тикете или отдельно.

## Критерии готовности

### Страница телефона + localStorage

- [ ] Все правила показа/скрытия Passkey.
- [ ] Поведение storage на OTP / Passkey-login по канону.
- [ ] Feature-тесты localStorage + ветвление login/reg.

### register/complete

- [ ] Транзакция User + acceptances; idempotency.
- [ ] Audit [T-011](../сделано/T-011-legal-acceptances-audit-поля.md).

### Рег. шаг 2 · профиль

- [ ] Обязательные: имя, фамилия, пол; ДР **не** обязательна (Pro).
- [ ] Незавершённый профиль → guard на шаг 2 после login.

### Post-reg · каналы

- [ ] MAX/TG не на reg; nudge после кабинета (мягкий).

### T-064

- [ ] SMS Pro + `phone_verified_at` + юрист → закрыть [T-064](T-064-auth-верификация-телефона-149-фз.md).

## Зависимости

[T-069](T-069-упрощение-входа-legal-одна-страница.md) · [T-071](T-071-упрощение-входа-passkey-опционально.md) · [T-064](T-064-auth-верификация-телефона-149-фз.md)

## Журнал

### 2026-07-03

- 2 юрдока на рег. шаге 1 Pro; terms + 18+ на телефоне; сброс Passkey hint только localStorage.

### 2026-06-25

- Первый эскиз API phone/start + register/complete.
