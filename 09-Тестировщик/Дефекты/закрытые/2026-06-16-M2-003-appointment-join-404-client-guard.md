# Client join/leave: 404 «Ресурс не найден» при сессии guard `client`

**Статус:** verified  
**Приоритет:** blocker  
**Зона:** Client / API  
**Модуль:** M2  
**Назначено:** —  
**Issue:** —  
**Связи:** E2E-01, E2E-05, E2E-06; commit `3535849` (регрессия); fix `e168ba0`

---

## Окружение

- Стенд: локально `*.telotron.test` (Docker Sail + nginx)
- Ветка / commit: `3535849` (баг), verified на `e168ba0`
- `build.client`: 177
- Браузер: Playwright Chromium (E2E)

## Предусловия

1. `E2E_ENABLED=true`, выполнен `E2eSeeder` (слоты E2E Gate / E2E Solo на завтра).
2. Клиент авторизован через сессию guard **`client`** (E2E `/__e2e/login` на `client.telotron.test` или обычный OTP/passkey login — тот же guard).

## Шаги

1. Открыть Client PWA → «Дневник» → «Записаться».
2. Выбрать слот **E2E Gate** (завтра 14:00) — слот виден, `GET …/me/appointments?scope=bookable` возвращает `id` (например `8`).
3. Нажать **«Записаться»** в диалоге слота (`POST /api/v1/me/appointments/{id}/join`).

## Ожидалось

- HTTP **201**, сообщение «Ты записан на…» в UI.
- Аналогично для leave (`DELETE …/join`) после успешной записи.

## Фактически

- HTTP **404** RFC 9457: `detail`: «Ресурс не найден.»
- В диалоге красный alert **«Ресурс не найден.»**
- Список bookable по-прежнему показывает слот (GET без route binding работает).

## Дополнительно

- **PHPUnit** `SchedulingApiTest` (join/leave) — **green**, но тесты используют `actingAs($user, 'web')`, что маскирует баг.
- **PHPUnit** с `actingAs($user, 'client')` тоже **green**: `actingAs` вызывает `Auth::shouldUse('client')` до dispatch, route binding видит пользователя.
- **Реальная HTTP-сессия** (curl после `/__e2e/login` + CSRF): `POST …/appointments/8/join` → **404** (воспроизведено QA).
- **Корневая причина:** `Route::bind('appointment')` в `AppServiceProvider` вызывает `Auth::user()` **до** middleware `pwa.auth`, который через `PwaZoneAuth::authenticateRequestForHost()` выставляет default guard зоны. При логине только в guard `client`/`pro` `Auth::user()` на этапе binding = `null` → `ModelNotFoundException` → 404.
- **Фикс:** middleware `PreparePwaZoneAuthGuard` в `bootstrap/app.php` (prepend api, до SubstituteBindings); feature-тест `AppointmentJoinClientGuardBindingTest`.

## История

| Дата | Кто | Комментарий |
|------|-----|-------------|
| 2026-06-16 | QA | заведён после прогона Vitest/PHPUnit green, E2E 7/11 (3 fail join) |
| 2026-06-20 | Dev | fix: `PreparePwaZoneAuthGuard` + `AppointmentJoinClientGuardBindingTest` |
| 2026-06-16 | QA | verified: Vitest 143/143, PHPUnit 316/316, E2E 11/11 на `e168ba0` |
