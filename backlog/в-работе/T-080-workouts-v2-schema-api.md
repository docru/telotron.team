# T-080 · Workouts v2: схема БД, миграция, API foundation

| Поле | Значение |
|------|----------|
| **Статус** | `in_progress` · папка: **`в-работе/`** · старт **06.07.2026** |
| **Приоритет** | P1 |
| **Эпик** | [E-004](../эпики/E-004-workouts-v2.md) |
| **Оценка** | **14–18 ч** |
| **Создан** | 2026-07-06 |

## Контекст

Фундамент v2: новые таблицы, миграция данных, удаление программ, HTTP-маршруты по [api-http §4.1k](../../_telotron.ru/docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md).

**Срез старта E-004 (06.07):** живых назначений v1 нет; cutover без коммуникации пилоту; обратная совместимость API v1 не сохраняем.

## Критерии готовности

- [ ] Таблицы `workout_training_templates`, `workout_assigned_trainings`, `workout_training_executions`
- [ ] Миграция `complex_templates` → training templates; assigned complexes → assigned trainings
- [ ] Drop `workout_plan_templates`, `workout_assigned_plans`, старые complex/plan API
- [ ] Статусы назначения: `draft` / `active` / `archived`
- [ ] Инвариант: одно незавершённое выполнение на клиента
- [ ] Feature-тесты миграции на фикстурах v1

## Ссылки

- [workout-тренировки-схема-данных-v2](../../_telotron.ru/docs/Техдок/03-модули/workout-тренировки-схема-данных-v2.md)
- [ADR-002](../../_telotron.ru/docs/Техдок/00-мета/архитектурные-решения/ADR-002-workouts-v2-dvuhurovnevaya-model.md)

## Журнал

### 2026-07-06

- Взято в работу — первый слайс [E-004](../эпики/E-004-workouts-v2.md).
