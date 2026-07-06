# T-080 · Workouts v2: схема БД, миграция, API foundation

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** · закрыт **06.07.2026** |
| **Приоритет** | P1 |
| **Эпик** | [E-004](../эпики/E-004-workouts-v2.md) |
| **Оценка** | **14–18 ч** |
| **Создан** | 2026-07-06 |

## Критерии готовности

- [x] Таблицы `workout_training_templates`, `workout_assigned_trainings`, `workout_training_executions`
- [x] Миграция `complex_templates` → training templates; assigned complexes → assigned trainings
- [x] Drop `workout_plan_templates`, `workout_assigned_plans`, старые complex/plan API
- [x] Статусы назначения: `draft` / `active` / `archived`
- [x] Инвариант: одно незавершённое выполнение на клиента
- [x] Feature-тесты миграции на фикстурах v1

## Хвост → T-081

Pro/Client Vue ещё на v1 URL — пересборка UI в [T-081](../бэклог/T-081-workouts-v2-pro-constructor.md).

## Журнал

### 2026-07-06

- Backend foundation: миграция, `WorkoutV1ToV2Migrator`, API §4.1k, PHPUnit **22/22** (`--filter=Workout`).
