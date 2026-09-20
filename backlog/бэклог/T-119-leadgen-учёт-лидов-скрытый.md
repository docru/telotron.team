# T-119 · E-006 · CRM · домен контактов + API (headless)

| Поле | Значение |
|------|----------|
| **Статус** | `done` · реализация в `_telotron.ru` |
| **Эпик** | [E-006](../эпики/E-006-crm-тренера.md) · **P0** (было P1 «учёт за кадром») |
| **Приоритет** | **P0** · ядро безголовой CRM |
| **Спринт** | не назначен |
| **Роль** | arch + dev |
| **Создан** | 2026-08-22 |
| **Обновлён** | 2026-09-20 |
| **Зависит от** | [T-113](T-113-leadgen-discovery-adr-экраны.md), [ADR-006](../../../_telotron.ru/docs/Техдок/00-мета/архитектурные-решения/ADR-006-crm-headless.md) (**accepted**) |
| **Блокирует** | E-008 запись лида в CRM, E-010 чтение/заметки, тонкий Pro UI |

## Контекст

Домен **`CrmContact`** + заметки + next action + **HTTP/доменные контракты**.  
Потребители: Pro UI, **E-008** (server-side), **E-010**.  
Не показываем Kanban; UI — тонкий список/карточка.

## Критерии готовности

- [x] Модель **`CrmContact`:** trainer_id, имя, телефон/канал связи, **source**, **status**, next_action_*, client_user_id / invite ref
- [x] Статусы: `new` \| `in_progress` \| `client` \| `former` \| `declined`
- [x] **`CrmNote`:** body, author_type (trainer \| ai \| system)
- [x] Доменный сервис: create/update/status/note; **автосклейка** по телефону + история касаний (`CrmTouch`)
- [x] Pro HTTP API (auth trainer) — для **отладочного** UI + документация api-http §4.1b1
- [x] События: created / status_changed / note_added / next_action_changed
- [x] Стык M1: переход в `client` / `former` без дубля учёта
- [x] Тесты: CRUD, изоляция trainer_id, склейка, события, заметка от ai (`CrmContactsApiTest`)

## Вне scope

- Публичная форма E-008, ИИ-чат E-010 (потребляют домен)
- Продуктовый UI тренера (только отладка — T-114/T-124)
- Риск слива / Kanban / CSV

## Уточнения перед срезом (2026-09-20)

| # | Решение |
|---|---------|
| A1 | T-119 = домен + HTTP + тесты + api-http; **без** отладочного UI (T-114/T-124) |
| A2 | События — Laravel `Event` на старте (лента/outbox для ИИ — с E-010) |
| A3 | При склейке — отдельная сущность касания (канал + дата), не только заметка |
| B4 | Телефон **опционален**; склейка, когда номер есть и совпал |
| B5 | `source`: `manual` \| `legacy_base` \| `booking_page` \| `channel` \| `other` |
| B6 | Переходы этапов **свободные** (при склейке этап не откатывать назад); `former→in_progress`, `client→former` ок |
| B7 | Если телефон уже в `trainer_clients` → сразу `client` + `client_user_id` |

Ответы: **A `1 1 1`** · **B `1 1 1 1`**.

## Журнал

### 2026-09-20 (срез)

- Реализовано: миграции `crm_contacts` / `crm_notes` / `crm_touches`, `CrmContactService`, Pro API `/api/v1/me/crm-contacts*`, события, api-http + [crm-headless-mvp](../../../_telotron.ru/docs/Техдок/03-модули/crm-headless-mvp.md).
- `CrmContactsApiTest` — 7 passed.

### 2026-09-20 (уточнение среза)

- Блоки A/B закрыты: без UI в тикете; Laravel Event; `CrmTouch`; телефон опц.; полный `source`; свободные этапы; авто `client` при M1.

### 2026-09-20 (вечер)

- PO финал: `former`, автосклейка, UI = отладка.

### 2026-09-20

- Перепрофилирован: ядро headless CRM; приоритет **P0**.
