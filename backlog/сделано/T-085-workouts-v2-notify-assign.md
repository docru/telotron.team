# T-085 · Workouts v2: уведомления при назначении

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** · закрыт **06.07.2026** |
| **Приоритет** | P1 |
| **Эпик** | [E-004](../эпики/E-004-workouts-v2.md) |
| **Оценка** | **4–6 ч** |
| **Зависит от** | [T-082](T-082-workouts-v2-pro-assignments.md) |
| **Создан** | 2026-07-06 |

## Критерии готовности

- [x] Событие при `assign` только из `draft`
- [x] Лента: тип события «новая тренировка» (`workout_assigned_training`)
- [x] Push/мессенджер — best effort (`WorkoutAssignmentNotifier`)
- [x] Тест: назначение → клиент видит в ленте

## Журнал

### 2026-07-06

- `WorkoutAssignmentNotifier`, feed в `ClientCalendarFeedService`; тест `test_assign_creates_workout_assigned_training_feed_event_for_client`.
- Commit `70d14c6`.
