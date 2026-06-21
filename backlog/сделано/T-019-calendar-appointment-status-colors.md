# T-019 Календарь · цветовые схемы статусов занятий

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Очередь** | 5 · ~6–10 ч |
| **Приоритет** | P1 |
| **Спринт** | 0 |
| **Роль** | dev + дизайн (приёмка) |
| **Создан** | 2026-05-31 |
| **Закрыт** | 2026-05-31 |

## Контекст

**Проблема:** на Pro «Расписание» отменённое занятие (`cancelled`) и предстоящее (`scheduled`) выглядели одинаково — отличие только сырой подписью `cancelled` в subtitle.

**Связанный тикет (отдельно):** различие **индивидуальное / групповое** — [T-020](T-020-calendar-individual-group-visual.md) **`done`**.

**Канон:** [Токены цветов](../../08-Дизайнер/Инструкции/Токены%20цветов%20—%20Pro%20и%20Client.md), [календарь-и-запись](../../../_telotron.ru/docs/Бизнес-требования/02-модули/m2-календарь/календарь-и-запись.md).

---

## Реализация

- `appointment-visual.ts` — фазы `upcoming` / `live` / `past` / `cancelled`, русские метки
- `TelotronCalendar.vue` — модификаторы `--status-*` в agenda / day / week / month
- `WorkspaceSchedulePage`, `ClientBookingPage`, `ClientFeedCalendar` — маппинг статуса
- CSS-токены `--calendar-status-*` в `app.css`
- Vitest: `appointment-visual.test.ts`

---

## Критерии готовности (фаза A+B)

- [x] Pro agenda: отменённое и предстоящее различимы (цвет / зачёркивание)
- [x] Нет сырого `cancelled` / `scheduled` в UI календаря
- [x] Статусные модификаторы в **agenda, day, week, month** (`TelotronCalendar`)
- [x] Pro: `cancelled` читается независимо от occupancy
- [x] Client booking: прошлая «моя» запись слабее предстоящей
- [x] Client feed + Pro client hub: прошлые appointments приглушены
- [x] `appointment-visual.test.ts` + `npm run test:ts` green
- [x] `build.pro` / `build.client` подняты
- [ ] Дизайн: визуальный smoke заказчиком на 360px (опционально)

**Фаза C** (подтверждение выхода, `participation_status`) — вне закрытия, после API.

---

## Журнал

### 2026-05-31

- Тикет создан (скрин agenda: cancelled vs upcoming).
- Закрыт разработчиком. Тип занятия individual/group вынесен в **T-020**.
