# SpaAuthFlowTest падает при AUTH_OTP_STUB_EXPOSE_CODE=false в .env

**Статус:** verified  
**Приоритет:** medium  
**Зона:** API  
**Модуль:** M0  
**Назначено:** разработчик  
**Issue:** —  
**Связи:** `tests/Feature/Api/SpaAuthFlowTest.php`, gate автотесты T-002

---

## Окружение

- Стенд: локально `*.telotron.test`, Docker `laravel.test`
- Ветка / commit: `871c015`
- `.env`: `AUTH_OTP_STUB_EXPOSE_CODE=false`

## Предусловия

1. В `.env` приложения `AUTH_OTP_STUB_EXPOSE_CODE=false` (как перед prod).
2. `php artisan test` из контейнера.

## Шаги

```bash
cd _telotron.ru
docker compose exec -u sail -T laravel.test php artisan test --filter=SpaAuthFlowTest::test_register_otp_start_creates_user
```

## Ожидалось

Тест green: в ответе `POST …/register/otp/start` есть `debug_otp` (6 цифр), пользователь создан.

## Фактически

```
Failed asserting that an array has the key 'debug_otp'.
tests/Feature/Api/SpaAuthFlowTest.php:230
```

Ответ `200`, `data.step=otp_sent`, `data.channel=email`, но **без** `debug_otp` — поведение API корректно при `stub_expose_code=false`.

## Предлагаемый фикс

Тест **не должен** зависеть от `.env` хоста:

- в `setUp()` теста или в начале метода: `config(['auth_otp.stub_expose_code' => true]);`
- либо отдельный тест «без stub» по аналогии с `EmailOtpFlowTest::assertJsonMissingPath('debug_otp')`.

После фикса: полный `php artisan test` green на том же SHA.

## Дополнительно

- Канон: `config/auth_otp.php` default `true`, `.env.example` комментирует `false` для prod.
- Регрессия CI/local: не блокирует prod UI, блокирует **автопрогон gate**.

## История

| Дата | Кто | Комментарий |
|------|-----|-------------|
| 2026-06-10 | QA | заведён после полного прогона: 275 pass, 2 fail |
| 2026-06-10 | QA | verified: `config(['auth_otp.stub_expose_code' => true])` в тесте |
