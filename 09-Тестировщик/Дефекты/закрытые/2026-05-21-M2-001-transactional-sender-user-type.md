# TransactionalMessageSender: неверный тип User → 500 на cancel/restore/schedule

**Статус:** closed  
**Приоритет:** blocker  
**Зона:** API  
**Модуль:** M2  
**Назначено:** разработчик  
**Issue:** —  
**Связи:** `SchedulingApiTest`, `AppointmentCancellationNotifier`, commit `e2fcc14` / `2f07e04`, T-002 gate, [Критичные сценарии MVP](../../Инструкции/Критичные%20сценарии%20MVP.md) S-01

---

## Окружение

- Стенд: локально Docker, `php artisan test`
- Ветка / commit: `2f07e04`
- Регрессия после `feat(scheduling): оповещения об отмене/восстановлении…` и доработок `TransactionalMessageSender`

## Предусловия

1. Пользователи с записью на занятие (тренер + клиент).
2. Любая операция, вызывающая `AppointmentCancellationNotifier` → `TransactionalMessageSender::sendToPrimary()`.

## Шаги

```bash
cd _telotron.ru
docker compose exec -u sail -T laravel.test php artisan test --filter=SchedulingApiTest
```

Или вручную через API:

1. Pro создаёт групповое занятие с постоянными участниками — **POST** `/api/pro/appointments`.
2. Pro отменяет занятие — **DELETE** `/api/pro/appointments/{id}`.
3. Client снимает запись — **DELETE** `/api/client/appointments/{id}/leave`.

## Ожидалось

- HTTP **201** / **200** / **204** по контракту.
- Уведомления клиентам/тренеру через основной канал (или graceful skip, если канал недоступен).
- `SchedulingApiTest`: **20/20** pass.

## Фактически

**7 падений** в `Tests\Feature\Api\SchedulingApiTest` (полный прогон: **282 passed, 7 failed**):

| Тест | HTTP / ошибка |
|------|----------------|
| `pro crud appointment reschedule cancel` | 500 вместо 201 |
| `pro create group appointment notifies permanent members` | 500 вместо 201 |
| `pro cancel notifies booked clients primary channel` | 500 вместо 200 |
| `client leave notifies trainer primary channel` | 500 вместо 204 |
| `client my scope shows trainer cancelled appointment` | **TypeError** |
| `pro restore notifies booked clients primary channel` | 500 вместо 200 |
| `client leave` | 500 вместо 204 |

Типовая ошибка:

```text
App\Modules\Identity\Notifications\TransactionalMessageSender::sendToPrimary():
Argument #1 ($user) must be of type App\Modules\Identity\Notifications\User,
App\Modules\Identity\Models\User given,
called in AppointmentCancellationNotifier.php on line 47
```

## Причина (код)

В `app/Modules/Identity/Notifications/TransactionalMessageSender.php` в сигнатурах используется неимпортированный `User`. PHP резолвит его в текущем namespace как несуществующий `Notifications\User`, тогда как вызывающий код передаёт `Models\User`.

Дополнительно в том же файле вызывается `Http::asForm()` (строка ~70) **без** `use Illuminate\Support\Facades\Http;` — при доставке через Telegram упадёт с `Class "Http" not found`.

Для сравнения: в `UserPrimaryChannelResolver.php` импорт `Models\User` указан корректно.

## Предлагаемый фикс

```php
use App\Modules\Identity\Models\User;
use Illuminate\Support\Facades\Http;
```

в `TransactionalMessageSender.php`. После — перегнать `SchedulingApiTest` и полный `php artisan test`.

## Дополнительно

- **Не дефект тестов:** `SchedulingApiTest` корректно ловит регрессию API.
- **Vitest** на том же SHA: **121/121** green.
- **E2E** на том же прогоне не стартовал из‑за инфраструктуры (nginx Exited, CSRF cookie недоступен из контейнера) — отдельный вопрос среды, не этот баг.

## История

| Дата | Кто | Комментарий |
|------|-----|-------------|
| 2026-05-21 | QA | заведён: 7/289 PHPUnit fail, TypeError в TransactionalMessageSender |
| 2026-05-21 | dev | fix: импорты `Models\User` и `Http` в TransactionalMessageSender; SchedulingApiTest 21/21 |
