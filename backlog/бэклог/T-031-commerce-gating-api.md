# T-031 · Commerce: TariffGate и HTTP API

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [T-026](T-026-commerce-модуль-эпик.md) |
| **Приоритет** | P1 |
| **Спринт** | 4 |
| **Роль** | dev |
| **Создан** | 2026-06-12 |
| **Оценка** | 12–14 ч |
| **Зависит от** | [T-028](T-028-commerce-тарифы-статусы-триал.md), [T-005](T-005-матрица-функция-тариф.md)* |

\*До T-005 — временная матрица из [матрица-тарифов-платформа](../../_telotron.ru/docs/Бизнес-требования/00-канон-mvp/матрица-тарифов-платформа.md).

## Контекст

Gating по тарифу и статусу (B4 ADR-001). Полный HTTP-контракт §4.1m + блок `commerce` в `GET /api/v1/me`.

## Критерии готовности

- [ ] `config/commerce/tariff-capabilities.php` (минимум: `groups=false` на Лайте).
- [ ] `TariffGate`: проверка capability; 403 `commerce-capability-denied`.
- [ ] Интеграция gating в **Groups** (§4.1b) и другие точки из §13 api-http.
- [ ] API: `GET /me/commerce`, `GET /me/commerce/tariffs`, `GET /me/commerce/transactions`, `PATCH /me/commerce/tariff`.
- [ ] Расширение `GET /api/v1/me`: `{ status, effective_tariff, balance_units, capabilities }`.
- [ ] Feature-тесты: Лайт → groups 403; триал → capabilities как Профи.

## Вне scope

- Purchase/coupons (T-029, T-032), Pro UI.

## Ссылки

- [api-http §4.1m, §13](../../_telotron.ru/docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md)
- [commerce-модуль-тз-mvp §3.2, §11](../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md)

## Журнал

### 2026-06-12

- Подтикет эпика T-026.
