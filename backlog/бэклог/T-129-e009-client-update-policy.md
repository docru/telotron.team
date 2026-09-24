# T-129 · E-009 · Обновление клиента: defer \| force + busy

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [E-009](../эпики/E-009-кросплатформенность.md) · этап 7 |
| **Приоритет** | **P0** |
| **Спринт** | — |
| **Роль** | dev |
| **Создан** | 2026-09-24 |
| **Зависит от** | [T-127](T-127-e009-runtime-bootstrap.md) (желательно); стык с [T-128](T-128-e009-pwa-adapter.md) |
| **Блокирует** | [T-131](T-131-e009-vk-adapter-пилот.md), [T-132](T-132-e009-welcome-clients-host.md) |

## Контекст

Единый контракт `/version.json`: `build` + `update: defer|force`. Полный reload не mid-screen (упражнение и т.п.). Обязателен для Mini App; желателен и для PWA.

## Критерии готовности

- [ ] `version.json` (зоны) отдаёт `update` (дефолт `defer` если нет поля)
- [ ] Адаптер: `watchClientUpdate` + `reloadDocument` (cache-bust `?b=` при необходимости)
- [ ] Ядро: `busy` / safe-point (минимум: экран тренировки / flush outbox / грязная форма — список зафиксировать в тикете при старте)
- [ ] `defer` → reload на смене раздела / после busy / visibility
- [ ] `force` → ASAP после safe-point, не бесконечно
- [ ] HTML/entry host (и по возможности PWA document): политика `Cache-Control` для anti-stuck (см. ADR §5)
- [ ] Тесты: парсинг policy; сценарий defer не зовёт reload пока busy
- [ ] Канон: кратко в runtime-адаптеры / политика версий

## Вне scope

- Hot-swap одного чанка без reload
- Background Sync

## Ссылки

- ADR-008 §5 · исследование §1.5.1

## Журнал

### 2026-09-24

- Тикет создан.
