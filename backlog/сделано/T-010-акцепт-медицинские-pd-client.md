# T-010 Dev · Акцепт согласия на медицинские ПД (Client)

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Приоритет** | **P0** |
| **Спринт** | 0–1 (после [T-009](../сделано/T-009-согласие-медицинские-pd-черновик.md)) |
| **Оценка** | **8–12 ч** |
| **Роль** | dev |
| **Создан** | 2026-05-26 |
| **Закрыт** | 2026-05-27 |

## Контекст

Отдельный экран согласия на **медицинские / особые категории** ПДн для **Client**. Gate **не** на регистрации.

**Триггеры (первый вход):**

1. Маршрут **`/appointments`** (раздел **«Дневник»**)
2. Маршрут **`/measurements`** (раздел **«Прогресс»** / измерения)

Без акцепта текущей редакции — **не показывать** функционал страницы (modal/full-screen gate).

## UX (канон)

| Элемент | Требование |
|---------|------------|
| Заголовок | **«Согласие на обработку медицинских данных»** |
| Текст | Полный текст из `legal_documents` — **прокручиваемая** область (scroll обязателен) |
| Чекбокс | **«Ознакомлен(а) с текстом согласия»** — обязателен, **не** pre-checked ([ревью §7.3](../../07-Юрист/Ревью%20—%20согласие%20медицинские%20ПДн%20v1.0%20(2026-05-24).md)) |
| Кнопка | **«Даю своё согласие»** — primary, активна только при отмеченном чекбоксе |
| Отказ | Закрытие / «Назад» без акцепта — пользователь **не** попадает в функционал |

## Backend

- `POST /api/v1/me/legal-acceptances` (или расширение) с `acceptance_context`: **`first_sensitive_feature`** (или новый контекст по согласованию с юристом)
- Запись в `legal_acceptances` + **расширенный audit** (см. [T-011](../сделано/T-011-legal-acceptances-audit-поля.md)):
  - `accepted_at`
  - `ip_address`
  - `user_agent` (в т.ч. версия ОС — парсинг или отдельное поле `client_os` из клиента)
  - **`device_id`** — стабильный ID устройства с клиента (localStorage / PWA install id; формат зафиксировать в техдоке)

## Критерии готовности

- [x] Текст [T-009](../сделано/T-009-согласие-медицинские-pd-черновик.md) (**утверждён директором 2026-05-26**) в seeder / prod
- [x] Gate на `/appointments` и `/measurements` для Client без акцепта
- [x] Экран акцепта по UX выше
- [x] После акцепта — доступ к разделу; повторный вход без gate
- [x] Feature-тест: без акцепта API трекера/замеров → 403 или gate на UI
- [x] **Pro** и регистрация — **без** этого экрана

## Зависимости

- [T-009](../сделано/T-009-согласие-медицинские-pd-черновик.md) — текст **утверждён** (2026-05-26)
- [T-011](../сделано/T-011-legal-acceptances-audit-поля.md) — поля фиксации (можно параллельно)

## Журнал

### 2026-05-26

- Тикет создан.

### 2026-05-19

- Backend: middleware `client.sensitive.consent`, `SensitiveDataConsentService`, `LegalAcceptanceWriter`, миграция `device_id`/`client_os`, seeder `sensitive_data_consent`, `SensitiveDataConsentTest`, trait `AcceptsSensitiveDataConsent` в тестах.
- Frontend: `SensitiveDataConsentGate.vue`, composable `use-sensitive-data-consent-gate.ts`, обёртки `ClientCalendarPage` / `ClientMeasurementsPage`, Vitest `sensitive-data-consent.test.ts`.
- `build.client` → 121.

### 2026-05-27 · закрытие

- `php artisan test` (SensitiveDataConsent, LegalAcceptance*) + Vitest `sensitive-data-consent.test.ts` green.
- Тикет → **`сделано/`**.
