# T-012 Dev · Публикация юрдокументов v1.0 (3 документа регистрации)

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Родитель** | [T-007](../бэклог/T-007-legal-privacy-v1-compliance.md) §1 |
| **Приоритет** | **P1** (gate A9) |
| **Очередь** | 3a · **~4–6 ч** |
| **Спринт** | 0 |
| **Роль** | dev |
| **Создан** | 2026-05-27 |
| **Закрыт** | 2026-05-27 |

## Контекст

Черновики v1.0 готовы у юриста; в prod/seeder — **заглушки** `2026-05-01`. Нужно опубликовать **полные** тексты регистрационного комплекта.

**Документы:**

| `document_key` | Черновик |
|----------------|----------|
| `privacy_policy` | [Политика v1.0](../../07-Юрист/Политика%20конфиденциальности%20v1.0%20—%20черновик.md) |
| `terms_of_service` | [ПСогл v1.0](../../07-Юрист/Пользовательское%20соглашение%20v1.0%20—%20черновик.md) |
| `personal_data_consent` | [Согласие на ПДн v1.0](../../07-Юрист/Согласие%20на%20обработку%20ПДн%20v1.0%20—%20черновик.md) |

**Канон:** реквизиты и e-mail — **`config('telotron.public')`**, не хардкод в теле.

**Блокер merge на prod (юрист):** тексты можно залить после пометки «можно публиковать»; технически — подготовить механизм и stage.

## Задачи

| # | Задача |
|---|--------|
| 1 | Редакция в `legal_documents`: `version` = **`2026-06-01`** (или согласованный канон Filament); `effective_at` / `published_at` |
| 2 | Тело: markdown → `body_snapshot` (seeder **или** artisan-команда **или** Filament — без дублирования реквизитов вручную) |
| 3 | Шапка каждого документа: **дата + v1.0**; блок оператора/e-mail — **из конфига** при сборке текста |
| 4 | `/legal/privacy`, `/legal/terms` — 200, актуальный текст; API `GET /legal/documents` — `has_body: true` для трёх ключей |
| 5 | Обновить `LegalDocumentSeeder` / тесты (`M0LegalNotificationsTest`, `PublicWelcomePageTest`) под новую версию |
| 6 | *(Опционально в том же PR)* `sensitive_data_consent` — полный текст из [T-009](../../07-Юрист/Согласие%20на%20обработку%20медицинских%20данных%20v1.0%20—%20черновик.md) вместо stub (для [T-010](../сделано/T-010-акцепт-медицинские-pd-client.md)) |

## Критерии готовности

- [x] Три документа v1.0 в БД; реквизиты совпадают с `config/telotron.php`
- [x] `/legal/privacy`, `/legal/terms` — полный текст, не stub
- [x] Регистрация Pro/Client подтягивает те же редакции из API
- [x] Feature-тесты green (legal/M0/public/sensitive)

## Зависимости

- **После:** [T-013](T-013-legal-age-18-gate.md), [T-014](T-014-legal-revision-banner.md) — логичнее на актуальных текстах
- **Не блокирует:** [T-015](T-015-public-privacy-request-form.md)

## Ссылки

- [LegalDocumentSeeder](../../../_telotron.ru/database/seeders/LegalDocumentSeeder.php)
- [PublicLegalDocumentController](../../../_telotron.ru/app/Http/Controllers/Public/PublicLegalDocumentController.php)
- [Сборка-политики-v1-факты](../../07-Юрист/Сборка-политики-v1-факты.md)

## Журнал

### 2026-05-27

- Тикет выделен из [T-007](../бэклог/T-007-legal-privacy-v1-compliance.md).

### 2026-05-19

- Источники: `database/legal-sources/v1.0/*.md` (4 файла, включая `sensitive_data_consent`).
- `LegalDocumentBodyAssembler` — сборка `body_snapshot` из markdown + `config('telotron.public')`, канон `2026-06-01` / v1.0.
- `LegalDocumentSeeder` + `php artisan legal:publish-v1-sources` — публикация; при `effective_at` в будущем — `now()->subDay()` для каталога до даты вступления.
- Тесты обновлены под `2026-06-01`; unit `LegalDocumentBodyAssemblerTest`.

### 2026-05-31 · backlog

- Тикет в **`сделано/`** (сверка индекса).
