# T-132 · E-009 · welcome-clients в host-средах

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** · код в ветке `initiative/i-001-modul-prodazh` (26.09), не в `main` |
| **Эпик** | [E-009](../эпики/E-009-кросплатформенность.md) · этап 7 |
| **Приоритет** | **P1** |
| **Обновлён** | 2026-09-26 |

## Критерии готовности

- [x] Zone id `welcome-clients` в runtime типах / layout `data-zone`
- [x] Host chrome: без SW/manifest; HTML no-store; `/version.json` + watch
- [x] Back hide-first / history.back / close (VK)
- [x] `authMode: none` — формы без Bearer
- [x] optionalLaunch CRM — вне пилота (не сделано; можно follow-up)
- [x] Детект VK + host-chrome на welcome
- [x] WelcomeLeadPagesTest зелёный; version endpoint
- [x] Канон runtime обновлён

## Журнал

### 2026-09-29

- Перенесён в `сделано/` при актуализации бэклога: код в ветке `initiative/i-001-modul-prodazh` (26.09), не в `main`.

### 2026-09-26

- `welcome-clients/host-chrome.ts`, version.json, NoStoreHtmlResponse, vite entry.

### 2026-09-24

- Тикет создан.
