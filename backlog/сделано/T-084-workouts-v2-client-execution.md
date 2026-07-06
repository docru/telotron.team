# T-084 · Workouts v2: Client оркестратор выполнения

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** · закрыт **06.07.2026** |
| **Приоритет** | P1 |
| **Эпик** | [E-004](../эпики/E-004-workouts-v2.md) |
| **Оценка** | **16–20 ч** |
| **Зависит от** | [T-083](T-083-workouts-v2-client-list-start.md) |
| **Создан** | 2026-07-06 |

## Критерии готовности

- [x] PATCH execution: полный JSON, idempotency на шаг
- [x] Статусы `in_progress` / `paused` / `completed`
- [x] Resume с паузы
- [ ] ~~Офлайн~~ → **техдолг** (вне DoD E-004)
- [x] Feature-тесты completion_percent

## Журнал

### 2026-07-06

- `ClientWorkoutExecutionForm`: пауза, отдых, Далее / Следующее / Пауза / Завершить; PATCH `workout-training-executions`.
- Commit `e1c8d48`.
