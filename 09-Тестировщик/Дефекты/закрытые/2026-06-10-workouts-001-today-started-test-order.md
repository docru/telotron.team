# WorkoutsApiTest: хрупкая проверка is_complete по индексу 0 в today-started

**Статус:** verified  
**Приоритет:** medium  
**Зона:** API  
**Модуль:** workouts (§12)  
**Назначено:** разработчик  
**Issue:** —  
**Связи:** `GET /api/v1/me/workout-complex-executions/today-started`, `WorkoutExecutionService::startedToday` (orderByDesc `last_updated_at`)

---

## Окружение

- Стенд: локально `*.telotron.test`, Docker
- Ветка / commit: `871c015`
- `Carbon::setTestNow('2026-05-19 12:00:00 UTC')`

## Предусловия

1. Клиент с `timezone=UTC`, согласие ПДн принято.
2. Назначен активный workout-план с комплексом (1×5 повторений).

## Шаги

```bash
docker compose exec -u sail -T laravel.test php artisan test --filter=WorkoutsApiTest::test_today_started_lists_complete_and_incomplete_from_today_only
```

Сценарий теста:

1. Создать **incomplete** execution (2/5 повторений) в 12:00.
2. Сидом добавить **complete** execution за сегодня 08:00 (5/5).
3. Сидом добавить execution за вчера (не должен попасть в список).
4. `GET today-started?trainer_user_id=…`

## Ожидалось (в тесте)

- 2 записи за сегодня.
- `incompleteId` присутствует в списке.
- `data.workout_complex_executions.0.is_complete === false`.

## Фактически

```
Failed asserting that true is identical to false.
WorkoutsApiTest.php:457
```

На позиции **0** — запись с `is_complete: true` (complete за 08:00). `incompleteId` в списке есть (`assertContains` проходит), но **не на индексе 0**.

Сортировка API: `orderByDesc('last_updated_at')` — порядок может не совпадать с ожиданием теста после изменений в сервисе/патче.

## Предлагаемый фикс

**Вариант A (предпочтительно для теста):** не проверять индекс 0; найти элемент по `incompleteId` в JSON и assert `is_complete === false`; отдельно проверить, что complete-запись за сегодня имеет `is_complete === true`.

**Вариант B:** если продуктово нужен фиксированный порядок (incomplete первым) — зафиксировать в API и обновить техдок; тогда правка в `WorkoutExecutionService::startedToday`.

После фикса: `php artisan test --filter=WorkoutsApiTest` green.

## Дополнительно

- Не воспроизводится в UI gate; блокирует **полный** `php artisan test`.
- Связанный UI: `ClientWorkoutAssignmentsPanel` — `todayStartedExecutions` с тем же endpoint.

## История

| Дата | Кто | Комментарий |
|------|-----|-------------|
| 2026-06-10 | QA | заведён после полного прогона |
| 2026-06-10 | QA | verified: incomplete = старт без PATCH; assert по id, не индекс 0 |
