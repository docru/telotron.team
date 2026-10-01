# T-129 · E-009 · Обновление клиента: defer \| force + busy

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** · код в ветке `initiative/i-001-modul-prodazh` (26.09), не в `main` |
| **Эпик** | [E-009](../эпики/E-009-кросплатформенность.md) · этап 7 |
| **Приоритет** | **P0** |
| **Спринт** | — |
| **Роль** | dev |
| **Создан** | 2026-09-24 |
| **Обновлён** | 2026-09-26 |
| **Зависит от** | [T-127](T-127-e009-runtime-bootstrap.md); стык с [T-128](T-128-e009-pwa-adapter.md) |
| **Блокирует** | [T-131](T-131-e009-vk-adapter-пилот.md), [T-132](T-132-e009-welcome-clients-host.md) |

## Контекст

Единый контракт `/version.json`: `build` + `update: defer|force`. Полный reload не mid-screen (упражнение и т.п.). Обязателен для Mini App; желателен и для PWA.

## Критерии готовности

- [x] `version.json` (зоны) отдаёт `update` (дефолт `defer` из `config/version.update`)
- [x] Адаптер: `watchClientUpdate` + `reloadDocument` (cache-bust `?b=`)
- [x] `busy` / safe-point: тренировка · flush outbox · API `dirty-form` (`setClientUpdateBusy`)
- [x] `defer` → reload на смене раздела / после busy / visibility
- [x] `force` → ASAP после safe-point
- [x] HTML workspace SPA: `Cache-Control: no-store`
- [x] Тесты: Vitest policy; DomainRoutingTest `update` + workspace no-store
- [x] Канон: `runtime-адаптеры-сред-mvp.md` § Обновления

## Вне scope

- Hot-swap одного чанка без reload
- Background Sync
- Массовая проводка `dirty-form` на все формы (API готов; экраны подключают по мере нужды)

## Ссылки

- ADR-008 §5 · исследование §1.5.1 · busy: тренировка / outbox / грязная форма

## Журнал

### 2026-09-29

- Перенесён в `сделано/` при актуализации бэклога: код в ветке `initiative/i-001-modul-prodazh` (26.09), не в `main`.

### 2026-09-26

- `config/version.update` + payload; `client-update-policy.ts`; wiring Pro/Client main + outbox + workout execution; docs.

### 2026-09-25

- Dev-блок C: busy = тренировка + outbox flush + грязная форма.

### 2026-09-24

- Тикет создан.
