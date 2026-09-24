# T-127 · E-009 · Bootstrap RuntimeAdapter (detect + registry)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [E-009](../эпики/E-009-кросплатформенность.md) · этап 7 |
| **Приоритет** | **P0** |
| **Спринт** | — |
| **Роль** | arch + dev |
| **Создан** | 2026-09-24 |
| **Зависит от** | [ADR-008](../../../_telotron.ru/docs/Техдок/00-мета/архитектурные-решения/ADR-008-ядро-среды-адаптеры.md) · [runtime-адаптеры](../../../_telotron.ru/docs/Техдок/01-канон-mvp/runtime-адаптеры-сред-mvp.md) |
| **Блокирует** | [T-128](T-128-e009-pwa-adapter.md), [T-131](T-131-e009-vk-adapter-пилот.md), [T-132](T-132-e009-welcome-clients-host.md) |

## Контекст

Интерфейс `RuntimeAdapter` уже в `resources/ts/shared/runtime/`. Нужен **каркас**: детект среды, registry, один активный адаптер на загрузку, доступ из bootstrap Pro/Client (пока stub/`Null` + заготовка под PWA).

## Критерии готовности

- [ ] Детект `LaunchEnvironment` (default `pwa`; VK/OK/MAX/TG — по Bridge / query / globals, без вызова SDK из ядра экранов)
- [ ] `getRuntimeAdapter()` / `setRuntimeAdapter` (или Pinia/provide) — один экземпляр на сессию страницы
- [ ] `ProductZone` включает `welcome-clients` в типах runtime (расширение `telotron-zone` — в этом или T-132)
- [ ] Pro/Client `main.ts` вызывают `adapter.init({ zone, root })` до hydrate auth
- [ ] Stub/Pwa placeholder: минимальный stub с `authMode: 'cookie'` **или** сразу тонкий делегат (полная выноска — T-128)
- [ ] Ядро экранов **не** импортирует vk-bridge / Telegram / MAX
- [ ] Vitest: detect + registry; контрактный тест остаётся зелёным
- [ ] Док: ссылка в каноне runtime при необходимости

## Вне scope

- Полный `PwaAdapter` (T-128)
- Backend launch verify (T-130)
- VkAdapter UI (T-131)

## Ссылки

- ADR-008 · `resources/ts/shared/runtime/runtime-adapter.ts`

## Журнал

### 2026-09-24

- Тикет создан (нарезка этапа 7).
