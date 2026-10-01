# T-131 · E-009 · VkAdapter + host shell (пилот)

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** · код в ветке `initiative/i-001-modul-prodazh` (26.09), не в `main` |
| **Эпик** | [E-009](../эпики/E-009-кросплатформенность.md) · этап 7 |
| **Приоритет** | **P0** |
| **Обновлён** | 2026-09-26 |
| **Зависит от** | T-128, T-129, T-130, T-134 |

## Критерии готовности

- [x] `VkAdapter`: Bridge init ≤30с; `authMode: launchToken`; caps без Passkey/SW/install
- [x] Host layout: нет manifest при vk query; SW unregister в адаптере
- [x] `storageNamespace: 'vk'`; Bearer в sessionStorage
- [x] Auth: launch → T-130/T-134 → `applyAuthToRequest` Bearer
- [x] Host Back: hide-first; иначе home / close
- [x] Update: watchClientUpdate (T-129)
- [x] UI Passkey/install скрыт по capabilities
- [x] Vitest bootstrap VkAdapter
- [x] Зоны Client и Pro
- [x] User без phone; first_entry T-134

## Журнал

### 2026-09-29

- Перенесён в `сделано/` при актуализации бэклога: код в ветке `initiative/i-001-modul-prodazh` (26.09), не в `main`.

### 2026-09-26

- `vk-adapter.ts`, bootstrap, host Back в main, layout без manifest на VK query.

### 2026-09-24

- Тикет создан.
