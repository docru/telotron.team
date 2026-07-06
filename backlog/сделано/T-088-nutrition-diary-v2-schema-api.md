# T-088 · Nutrition diary v2: схема и API

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** · закрыт **06.07.2026** |
| **Приоритет** | P1 |
| **Эпик** | [E-005](../эпики/E-005-nutrition-diary-v2.md) |
| **Оценка** | **8–12 ч** |
| **Зависит от** | — |
| **Создан** | 2026-07-06 |

## Контекст

Замена плоской модели `nutrition_meals` на **слот приёма** + **блюда**. Канон полей — в [E-005](../эпики/E-005-nutrition-diary-v2.md).

## Backend

- Миграция: `nutrition_meal_slots`, `nutrition_meal_dishes`; `nutrition_meal_photos` → FK на `meal_slot_id`; drop `nutrition_meals`
- `meal_type`: `breakfast` \| `lunch` \| `dinner` \| `snack`
- `meal_date` date (день в TZ клиента при записи)
- UNIQUE `(client_user_id, meal_date, meal_type)`
- Фото: 1 на slot; retention 14 суток — без изменения политики

## API (черновик)

| Метод | Путь | Назначение |
|-------|------|------------|
| `GET` | `/api/v1/me/nutrition-diary?from=&to=` | Слоты за диапазон дат + вложенные `dishes[]`, `photo?` |
| `PUT` | `/api/v1/me/nutrition-diary/slots` | Upsert слота (date + type) — lazy create |
| `POST` | `…/slots/{id}/dishes` | Добавить блюдо |
| `PATCH` | `…/dishes/{id}` | name, amount, amount_unit, sort_order |
| `DELETE` | `…/dishes/{id}` | Удалить блюдо |
| `POST` | `…/slots/{id}/clear` | Очистить приём (блюда + фото) |
| `POST` | `…/slots/{id}/photos` | Фото (как сейчас, 409 если уже есть — или replace) |

Идемпотентность на mutating — как в текущем `MeNutritionMealController`.

## Критерии готовности

- [x] Миграция на пустых данных; старые таблицы удалены
- [x] Модели + сервис в `app/Modules/Nutrition/`
- [x] Feature-тесты CRUD слота/блюда, unique constraint, photo 409/replace
- [x] Pro `showPhoto` по новому FK (view rights без изменений)

## Журнал

### 2026-07-06

- Закрыт в рамках E-005: схема v2, API `/nutrition-diary`, `NutritionDiaryApiTest` 8/8.
