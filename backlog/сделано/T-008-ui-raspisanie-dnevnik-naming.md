# T-008 UI · «Расписание» (Pro) и «Дневник» (Client)

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Приоритет** | P1 |
| **Спринт** | 0–1 |
| **Роль** | dev |
| **Создан** | 2026-05-26 |
| **Закрыт** | 2026-05-27 |

## Контекст

Решение директора: в UI **тренера** раздел M2 — **«Расписание»**; у **клиента** сводный раздел (feed, тренировки, питание, трекеры) — **«Дневник»**. Канон: [Глоссарий](../../01-Директор/Инструкции/1-контекст-и-правила/Глоссарий.md) v0.15, [календарь-и-запись](../../../_telotron.ru/docs/Бизнес-требования/02-модули/m2-календарь/календарь-и-запись.md).

**Частично сделано (2026-05-26):** `workspace-nav.ts`, routes, `WorkspaceSchedulePage`, `ClientCalendarPage` (h1), `HomePage`, `ProClientHubPage`, welcome feature card.

## Критерии готовности

- [x] Pro: нижняя вкладка, «Ещё», `/schedule`, meta `sectionTitle` — **Расписание**
- [x] Client: нижняя вкладка, `/appointments`, meta — **Дневник**
- [x] Pro → карточка клиента: вкладка feed — **Дневник** (вид клиента)
- [x] Внутри раздела «Дневник» подвкладки режима просмотра («Календарь» / «Лента») — **не** путать с названием раздела; при конфликте «Дневник питания» для nutrition sub-tab
- [x] `grep -r 'Календарь' resources/ts` — только комментарии / режимы просмотра / API-ошибки, не nav/title раздела
- [x] Vitest/ smoke при наличии assert на старые подписи — обновить
- [x] `npm run build` под sail

## Ссылки

- Файлы: `resources/ts/shared/workspace-nav.ts`, `app/pro/router/routes.ts`, `app/client/router/routes.ts`

## Журнал

### 2026-05-26

- Тикет создан; базовая правка labels в коде (см. контекст).

### 2026-05-27

- Доводка: `telotron-theme` (офлайн/загрузка), `TelotronCalendar` voice pro/client, `ClientBookingPage`, Vitest `workspace-nav.test.ts` + routes acceptance.

### 2026-05-27 · закрытие

- Все критерии закрыты; `npm run test:ts` (workspace-nav, routes.acceptance) green.
- Тикет → **`сделано/`**.
