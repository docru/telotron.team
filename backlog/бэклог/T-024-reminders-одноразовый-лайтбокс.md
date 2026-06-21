# T-024 · Reminders: одноразовый лайтбокс при открытии приложения

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Приоритет** | P1 (блокирует UX Commerce к 01.08) |
| **Спринт** | этап 1 · пилот, до Commerce UI |
| **Роль** | dev (+ архитектор на review API) |
| **Создан** | 2026-06-12 |

## Контекст

Нужен **общий механизм** «показать модальное окно один раз при следующем открытии PWA», без дублирования в каждом модуле.

**Первый потребитель:** [Commerce](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md) — лайтбокс «платные функции приостановлены» при переходе в `light`/`frozen` (один раз на эпизод заморозки). Эпик Commerce: [T-026](T-026-commerce-модуль-эпик.md) (интеграция в [T-030](T-030-commerce-daily-debit-freeze.md)).

Доработка — в модуле **`Reminders`** (M4 / оповещения): in-app слой уже там; лайтбокс — **отдельный тип in-app prompt**, не путать с `reminders_deliveries` по занятиям.

Канон: [reminders-одноразовый-лайтбокс-mvp.md](../../_telotron.ru/docs/Техдок/03-модули/reminders-одноразовый-лайтбокс-mvp.md).

## Критерии готовности

- [ ] Таблица `reminders_one_time_lightboxes` (или согласованное имя) + модель в `app/Modules/Reminders/`.
- [ ] API §4.1d: `GET /api/v1/me/one-time-lightboxes` (ожидающие показа); `POST /api/v1/me/one-time-lightboxes/{id}/dismiss` с `idempotency_key`.
- [ ] Pro shell: после `hydrate` запросить список; показать **первый** pending; по закрытию — dismiss.
- [ ] Сервис `OneTimeLightboxService`: `schedule(user, prompt_key, episode_key, payload)` — идемпотентно на пару `(user_id, prompt_key, episode_key)`.
- [ ] **Commerce:** при входе в `light`/`frozen` вызывает schedule с `prompt_key=commerce.suspension`, `episode_key=commerce_freeze:{id}` или timestamp эпизода; **без** таблицы `commerce_suspension_notice_dismissals`.
- [ ] Feature-тест: schedule → GET pending → dismiss → GET пусто; повтор dismiss идемпотентен.
- [ ] Док: api-http §4.1d и techdoc обновлены. *(2026-06-12: канон обновлён)*

## Вне scope тикета

- Push/TG для того же текста (только in-app лайтбокс).
- Редактор промптов в Filament (hardcode/copy из `payload` JSON достаточно для MVP).

## Ссылки

- [commerce-модуль-тз-mvp §9.2](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)
- [commerce-схема-данных-mvp](../../_telotron.ru/docs/Техдок/03-модули/commerce-схема-данных-mvp.md)
- [api-http §4.1d / §4.1m](../../_telotron.ru/docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md)
- [оповещения (бизнес)](../../_telotron.ru/docs/Бизнес-требования/02-модули/m4-уведомления/оповещения.md)

## Журнал

### 2026-06-12

- Тикет создан по решению архитектора: лайтбокс — в Reminders, не в Commerce.
