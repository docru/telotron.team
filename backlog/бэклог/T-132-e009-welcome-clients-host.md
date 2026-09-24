# T-132 · E-009 · welcome-clients в host-средах

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [E-009](../эпики/E-009-кросплатформенность.md) · этап 7 |
| **Приоритет** | **P1** (можно параллельно кабинету после T-127/T-129) |
| **Спринт** | — |
| **Роль** | dev |
| **Создан** | 2026-09-24 |
| **Зависит от** | [T-127](T-127-e009-runtime-bootstrap.md), [T-129](T-129-e009-client-update-policy.md); Vk shell-паттерн из [T-131](T-131-e009-vk-adapter-пилот.md) желателен |
| **Связь** | [E-008](../эпики/E-008-зона-лидов.md) · [ADR-007](../../../_telotron.ru/docs/Техдок/00-мета/архитектурные-решения/ADR-007-welcome-clients-зона-лидов.md) |

## Контекст

Третья зона: публичные колбек/квиз (`welcome-clients.*`). Нужен тот же контракт **среды** (Bridge, Back, update/HTML), **без** кабинетной сессии (`authMode: none` / опц. `optionalLaunch` для атрибуции).

Сейчас Blade — адаптер может подключаться тонким JS в layout, не обязательно полный Vue SPA.

## Критерии готовности

- [ ] Zone id `welcome-clients` в bootstrap/runtime
- [ ] Host entry layout: без SW/manifest; HTML no-store / version check (T-129)
- [ ] Back: hide-first; fallback на корень сценария (`/callback|{quiz}/{nick}`) / close
- [ ] `authMode: none` — формы работают без Bearer кабинета
- [ ] Опционально (PO): `optionalLaunch` → передать verified `vk_user_id` в source/мета заявки CRM — отдельный чеклист в тикете при старте
- [ ] Детект VK + VkAdapter (или shared host chrome) на welcome host
- [ ] Тест/smoke: страница записи открывается в host-режиме; заявка пишется в CRM как сейчас
- [ ] Документация welcome-clients-mvp + runtime канон § зона

## Вне scope

- Канал→CRM inbox
- Отдельная сборка public под VK
- Passkey/SW на welcome

## Ссылки

- ADR-008 § welcome-clients · исследование §1.8

## Журнал

### 2026-09-24

- Тикет создан.
