# T-075 · Упрощение входа · уборка legacy Pro auth и рефакторинг

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** · фаза 5: legacy Pro → 404; уборка кода ✓ |
| **Эпик** | [E-003](../эпики/E-003-упрощение-входа.md) · **Упрощение входа** |
| **Приоритет** | P2 (после выката нового потока Pro) |
| **Оценка** | **8–14 ч** |
| **Роль** | dev |
| **Создан** | 2026-07-03 |

## Контекст

После [T-068](T-068-упрощение-входа-sms-бот-напоминания.md) (фазы 2–3) для зоны **Pro** новый поток: `phone/start` → `phone/verify` → `register/complete` → wizard шагов 2–3. Старые маршруты временно отдают **410 Gone** ([E-003](../эпики/E-003-упрощение-входа.md) Q&A #3, #8).

**Client** по-прежнему использует legacy-пути (`register/draft`, `otp/login`, recovery через мессенджер) — **не трогаем** в этом тикете.

Цель тикета: **удалить** мёртвый код Pro, **свести** дублирование, **обновить** тесты и канон — без изменения поведения Client.

## Scope

### Backend · удалить или вынести из Pro

- [ ] Маршруты и handlers, помеченные deprecated для `zone=pro`:
  - `POST /register/draft`, `/register/otp/*`, `/register/passkey/*` (ветки Pro в `SpaPasskeyRegisterController`);
  - `POST /otp/login/*` (ветки Pro в `SpaOtpLoginController`);
  - `POST /recovery/*` (ветки Pro в `SpaPasskeyRecoveryController`).
- [ ] Ключи сессии legacy Pro-регистрации в `SpaAuthSession`, если не используются Client:
  - `REGISTER_STEP1`, `REGISTER_LEGAL_SNAPSHOT`, `REGISTER_ATTEST`, `OTP_REGISTER_CHALLENGE_ID` — оставить только то, что нужно Client.
- [ ] `RegistrationDraftService` — если после выноса Client остаётся только для Client, переименовать/задокументировать зону.
- [ ] `OtpChallenge::CHANNEL_SMS` — убрать пометки deprecated; единый канал Mobile ID / stub для Pro phone OTP.
- [ ] Middleware `DeprecateLegacyProAuth` (или аналог) — **удалить** после снятия маршрутов; маршруты Pro не регистрировать вместо 410.
- [ ] Ветвления `if ($zone === 'pro')` в общих контроллерах — по возможности разделить на Pro-специфичные классы или трейты **без** дублирования логики Client.

### Frontend · Pro only

- [ ] Удалить мёртвые ветки Pro в `RegisterPage.vue` / `LoginPage.vue` (старый draft + OTP MAX/TG на регистрации).
- [ ] Убрать ссылки на `telotron_pro_last_phone` и прочие неиспользуемые ключи (миграция не делаем — [E-003](../эпики/E-003-упрощение-входа.md) Q&A #10).
- [ ] Маршрут `/recovery` для Pro — редирект на `/login` (если ещё остался заглушкой).
- [ ] Vitest: удалить/переписать тесты, завязанные на deprecated Pro API.

### Тесты

- [ ] Удалить или перенести в «Client-only» feature-тесты старых Pro flow (`SpaAuthFlowTest` и др.).
- [ ] Сохранить регрессию Client: `register/draft`, OTP login, recovery — **зелёные**.
- [ ] Нет обращений к 410-м Pro endpoint в E2E (кроме негативных, если оставим на переходный период — затем убрать).

### Документация

- [ ] Обновить [регистрация-и-вход-max-passkey](../../../_telotron.ru/docs/Бизнес-требования/02-модули/auth/регистрация-и-вход-max-passkey.md) — только новый Pro-поток.
- [ ] `app/Modules/Identity/README.md` — без упоминания снятых Pro recovery / старой регистрации.
- [ ] При необходимости — краткая заметка в техдок API (`api-http-контракт`).

## Не в scope

- Client wizard и Client auth API.
- Post-reg nudge ([T-067](T-067-упрощение-входа-pwa-напоминания.md), [T-070](T-070-упрощение-входа-мастер-баннер.md)).
- Юрдокументы ([T-073](T-073-legal-смс-пилот-обновление-документов.md)).

## Зависимости

- [T-068](T-068-упрощение-входа-sms-бот-напоминания.md) — новые Pro API и UI на prod/staging.
- [T-071](T-071-упрощение-входа-passkey-опционально.md) — рег. шаг 3 и вход по ключу в новом потоке.
- Рекомендуется: **1–2 спринта** после выката Pro (убедиться, что нет обращений к 410 в логах).

## Критерии готовности

- [x] Для Pro нет зарегистрированных legacy auth/register/recovery маршрутов (404).
- [x] Client flow без регрессий (PHPUnit + E2E client auth).
- [x] Нет мёртвого Pro-кода в `RegisterPage` / `LoginPage` / общих auth-контроллерах (или явно помечен `client-only`).
- [x] Канон auth в `docs/` обновлён (`регистрация-и-вход-max-passkey.md`).
- [x] Полный прогон тестов зелёный (495 PHPUnit).

## Журнал

### 2026-07-05 (завершение)

- **`RegisterPage.vue`:** удалён мёртвый script (~600 строк legacy draft/OTP/MAX/TG); остались обёртки `ProRegisterWizard` / `ClientRegisterWizard`.
- **`LoginPage.vue`:** сняты legacy recovery (`recovery/otp/*`, `setup_passkey`) и третья зона; Pro/Client — только SMS + passkey.
- Vitest: `login-page.pro-auth.test.ts` обновлён.
- **`pro-phone-auth-storage.ts`:** удалён deprecated alias `shouldShowProPasskeyButton`.
- **`SpaAuthSession`**, **`Identity/README.md`:** уточнены комментарии (legacy keys — Client-only).
- Vitest: `login-page.pro-auth.test.ts` (RegisterPage shell + LoginPage без legacy recovery); PHPUnit auth-related — зелёные.

### 2026-07-05

- Статус **`in_progress`**: фаза 5 — legacy Pro routes → 404 (`ProPhoneAuthFlowTest`); удаление мёртвого кода и `DeprecateLegacyProAuth` ✓ (middleware уже снят ранее).

### 2026-07-03

- Тикет создан по запросу директора: отдельная задача на уборку legacy после нового Pro-потока.
