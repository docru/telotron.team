# T-033 · Commerce: Pro UI «Тариф и счёт»

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [E-001](../эпики/E-001-commerce-модуль.md) |
| **Приоритет** | P1 |
| **Спринт** | 4–5 |
| **Роль** | dev |
| **Создан** | 2026-06-12 |
| **Оценка** | 12–16 ч |
| **Зависит от** | [T-029](T-029-commerce-платежи-yookassa.md), [T-031](T-031-commerce-gating-api.md), [T-032](T-032-commerce-купоны.md), [T-024](T-024-reminders-одноразовый-лайтбокс.md) |

## Контекст

Раздел Pro для баланса, тарифа, пополнения, купонов, истории. Лайтбокс приостановки — через shell Reminders (T-024), не локальный флаг Commerce.

## Критерии готовности

- [ ] Верхняя планка Pro: chip «N Ед. · ~M дн.» + пиктограмма статуса → `/more/tariff`.
- [ ] Плитка «Тариф и счёт» на «Ещё».
- [ ] Отображение: баланс Ед., тариф, `status`, freeze, capabilities (read-only).
- [ ] Пополнение: произвольная сумма ≥ `min_topup_rub`, quote, redirect `checkout_url`.
- [ ] Купон: apply / active discount / remove.
- [ ] Смена тарифа Лайт ↔ Профи (confirm на даунгрейд).
- [ ] История транзакций (пагинация).
- [ ] Gating UI по `capabilities` (группы и др.).
- [ ] `npm run build` под `-u sail`; Vitest при наличии компонентов.
- [ ] Ручной smoke на stage.

## Вне scope

- Client UI коммерции; [T-025](T-025-ux-подталкивание-партнёрской-ссылки.md) partner CTA на checkout.

## Ссылки

- [commerce-pro-ui-mvp](../../_telotron.ru/docs/Техдок/03-модули/commerce-pro-ui-mvp.md)
- [commerce-модуль-тз-mvp §9](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)
- [frontend-архитектура §6](../../_telotron.ru/docs/Техдок/01-канон-mvp/frontend-архитектура-и-стек-mvp.md)

## Журнал

### 2026-06-12

- Подтикет эпика E-001.
