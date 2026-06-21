# T-017 Скругления — деловой стиль (меньше radius)

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Очередь** | 3 · ~3–4 ч |
| **Приоритет** | P1 |
| **Спринт** | 0 |
| **Роль** | dev + дизайн (приёмка) |
| **Создан** | 2026-05-31 |
| **Закрыт** | 2026-05-31 |

## Контекст

Заказчик: текущие **крупные скругления** (карточки 16px, pill-кнопки `rounded-full`, «мягкие» углы) дают ощущение **расслабленного, домашнего** UI. Для **Телотрон Pro** и public A13 нужен **более деловой** тон: инструмент тренера, не consumer lifestyle.

**Связь:** [T-001](T-001-a13-public-тексты-v2.md) (public v2).

---

## Критерии готовности

- [x] `--radius` = 6px, `--radius-lg` = 8px в `app.css`; shadcn derived tokens согласованы
- [x] Primary CTA public «Начать бесплатно» — **прямоугольная** с лёгким скруглением (~6–8px), **не** capsule/pill
- [x] Карточки public hero/features — углы **8px max**, визуально «строже», чем до правки
- [x] Pro: кнопки «Новое занятие», login/register — **не pill** (`Button` pill → `rounded-md`)
- [x] Avatar, calendar dots, progress track, segmented control — **остались** круглыми/капсулой
- [x] `npm run build` + `npm run test:ts` (100 pass)
- [ ] Дизайн: приёмка на 360px — «деловой» (ожидает визуальный smoke заказчиком)
- [x] Документ Система стилей обновлён

---

## Реализация

- `resources/css/app.css`: токены `--radius` 6px, `--radius-lg` 8px, `--radius-sm`/`--radius-md` явно; public btn/cards/inputs; бейджи `rounded-sm`; filter chips и toast `rounded-md`; segmented `rounded-full` (капсула)
- `resources/ts/components/ui/button/index.ts`: base + pill + icon → `rounded-md`
- Login/Register, legal/sensitive gates, shell icon buttons — убран pill
- `config/version.php`: `build.pro` 109, `build.client` 125
- [Система стилей — Pro и Client (MVP).md](../../08-Дизайнер/Инструкции/Система%20стилей%20—%20Pro%20и%20Client%20(MVP).md) §5, §7.1, §9

---

## Журнал

### 2026-05-31

- Тикет создан по запросу заказчика: меньше скругление, деловой стиль.

### 2026-05-31 (dev)

- Реализованы токены и кнопки; сборка и Vitest green. Визуальная приёмка дизайном — по чеклисту «Приёмка».
