# T-011 Dev · Техническая фиксация всех legal-акцептов

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Приоритет** | P1 |
| **Спринт** | 0–1 |
| **Оценка** | **4–6 ч** |
| **Роль** | dev |
| **Создан** | 2026-05-26 |
| **Закрыт** | 2026-05-27 |

## Контекст

Директор: **все акцепты** должны **технически фиксироваться** одинаково надёжно. Для медицинского согласия — минимум: время, IP, версия ОС, уникальный ID устройства.

**Пути акцепта:**

1. Регистрация — `SpaPasskeyRegisterController::recordRegistrationLegalAcceptancesFromSession`
2. API — `POST /api/v1/me/legal-acceptances` (`MeLegalAcceptanceController`)

## Задачи

| # | Задача |
|---|--------|
| 1 | **Аудит:** таблица «какой акцепт / где / какие поля пишутся» |
| 2 | Миграция: `device_id` (nullable string), опц. `client_os` / `acceptance_metadata` JSON |
| 3 | Клиент: генерация/хранение **stable device_id**; передача в API акцепта |
| 4 | Единый сервис записи `LegalAcceptance` — registration + API + [T-010](../сделано/T-010-акцепт-медицинские-pd-client.md) |
| 5 | Тесты: registration + POST legal-acceptances сохраняют IP, UA, device_id |
| 6 | Док: строка в [api-http-контракт-mvp](../../../_telotron.ru/docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md) §legal-acceptances |

## Критерии готовности

- [x] Отчёт аудита в журнале тикета (до/после)
- [x] Registration legal acceptances — те же поля, что POST API
- [x] Нет акцепта «без следа» в prod-потоках MVP
- [x] Юрист/директор могут показать запись по user_id + document_key

## Журнал

### 2026-05-26

- Тикет создан; текущая схема — см. `LegalAcceptance` model, migration `2026_05_13_120000`.

### 2026-05-19 — аудит до/после

| Поток | До | После |
|-------|-----|--------|
| `POST /me/legal-acceptances` | `accepted_at`, `ip`, `user_agent`; без `device_id` / `client_os` | `LegalAcceptanceWriter::record()` — все поля; `device_id` обязателен для `first_sensitive_feature` |
| Регистрация `passkey/verify` | `firstOrCreate` только `accepted_at`, `ip`, `user_agent` | `LegalAcceptanceWriter::recordOnce()` + `device_id`, `client_os` с клиента |
| Client gate T-010 | — | `device-id.ts`, передача в POST |
| Client регистрация | — | `RegisterPage` → `device_id` / `client_os` на `passkey/verify` |

Миграция: `2026_05_27_100000_add_device_fields_to_legal_acceptances` (`device_id`, `client_os`).

Тесты: `LegalAcceptanceWriterTest`, `LegalAcceptanceAuditTest`, `SensitiveDataConsentTest` (device_id).

### 2026-05-27 · закрытие

- Все критерии закрыты; audit-тесты green.
- Тикет → **`сделано/`**.
