# T-014 Dev · Баннер новой редакции юрдокументов

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Родитель** | [T-007](../бэклог/T-007-legal-privacy-v1-compliance.md) §3 |
| **Приоритет** | **P1** |
| **Очередь** | 3c · **~6–8 ч** |
| **Спринт** | 0–1 |
| **Роль** | dev |
| **Создан** | 2026-05-27 |
| **Закрыт** | 2026-05-27 |

## Контекст

При публикации новой редакции обязательных документов пользователь **не может** работать в Pro/Client, пока не примет её ([Сборка §12](../../07-Юрист/Сборка-политики-v1-факты.md)).

**Обязательный набор для баннера (MVP):** `privacy_policy`, `terms_of_service`, `personal_data_consent`.

**Не входит:** `sensitive_data_consent` — отдельный gate [T-010](T-010-акцепт-медицинские-pd-client.md).

## Backend

| # | Задача |
|---|--------|
| 1 | В **`GET /api/v1/me`** (или вложенно `legal.pending_acceptances`): список **непринятых** опубликованных редакций из каталога vs `legal_acceptances` пользователя |
| 2 | Элемент: `document_key`, `version`, `legal_document_version_id`, `title`, ссылка на тело (`GET /legal/documents/{key}?version=`) |
| 3 | Акцепт: существующий **`POST /api/v1/me/legal-acceptances`**, контекст **`reconsent`** — зафиксировано в [api-http](../../../_telotron.ru/docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md) |
| 4 | Идемпотентность и **`device_id`** — через [T-011](T-011-legal-acceptances-audit-поля.md) (`LegalAcceptanceWriter`) |

## Frontend (Pro + Client)

| # | Задача |
|---|--------|
| 5 | **Незакрываемый** full-screen / modal overlay, пока есть `pending_acceptances` |
| 6 | Список документов + просмотр текста; одна галка / кнопка «Принимаю актуальные условия» (согласовать с PO — можно одну галку на комплект, как при регистрации) |
| 7 | После успешного POST — снять overlay, обновить `auth-session` / `GET /me` |

## Критерии готовности

- [x] После публикации новой редакции (Filament/seeder) залогиненный пользователь видит баннер
- [x] Без акцепта — нет доступа к основному UI (навигация заблокирована)
- [x] После акцепта всех pending — работа возобновляется
- [x] Feature-тест API pending + POST; ручной сценарий или e2e в журнале тикета

## Зависимости

- **После** [T-012](T-012-legal-documents-v1-publish.md) (удобно тестировать второй редакцией)
- [T-011](T-011-legal-acceptances-audit-поля.md) — done

## Ссылки

- [MeController](../../../_telotron.ru/app/Http/Controllers/Api/V1/Identity/MeController.php)
- [MeLegalAcceptanceController](../../../_telotron.ru/app/Http/Controllers/Api/V1/Identity/MeLegalAcceptanceController.php)
- [LegalDocument::currentCatalog()](../../../_telotron.ru/app/Modules/Legal/Models/LegalDocument.php)

## Журнал

### 2026-05-27

- Тикет выделен из [T-007](../бэклог/T-007-legal-privacy-v1-compliance.md).

### 2026-05-19

- `MandatoryLegalAcceptanceService` + `legal.pending_acceptances` в `GET /me`.
- `LegalRevisionGate` (Pro/Client), `acceptance_context: reconsent`, `build.pro` 108 / `build.client` 124.
- Тесты: `LegalRevisionPendingTest`, Vitest `mandatory-legal-acceptances.test.ts`.
- **Ручная проверка:** залогиниться без акцептов → overlay; Filament/seeder — вторая редакция `privacy_policy` → один pending; «Продолжить» → overlay снимается.

### 2026-05-31 · backlog

- Тикет в **`сделано/`** (сверка индекса).
