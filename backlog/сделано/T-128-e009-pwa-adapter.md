# T-128 · E-009 · PwaAdapter (вынос текущего PWA)

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** · код в ветке `initiative/i-001-modul-prodazh` (26.09), не в `main` |
| **Эпик** | [E-009](../эпики/E-009-кросплатформенность.md) · этап 7 |
| **Приоритет** | **P0** |
| **Спринт** | — |
| **Роль** | dev |
| **Создан** | 2026-09-24 |
| **Обновлён** | 2026-09-26 |
| **Зависит от** | [T-127](T-127-e009-runtime-bootstrap.md) |
| **Блокирует** | [T-131](T-131-e009-vk-adapter-пилот.md) (нужен рабочий шов auth/HTTP) |

## Контекст

Сейчас cookie Sanctum, SW, Passkey, install **вшиты** в shared/layouts. Вынести в `PwaAdapter` **без смены UX** (регресс PWA = блокер).

## Критерии готовности

- [x] `PwaAdapter` реализует `RuntimeAdapter`: `authMode: 'cookie'`
- [x] `ensureAuthReady` / `applyAuthToRequest` — CSRF + `credentials: 'same-origin'`
- [x] `apiJson` / `apiMultipartJson` берут auth-патч из адаптера
- [x] Passkey: ceremony через адаптер; UI по `capabilities().hasPasskey`
- [x] Install nudge / BIP — через адаптер; скрытие по capabilities
- [x] SW register + version-check через адаптер; layout без inline SW; globals на `/install`
- [x] `storageNamespace(): 'pwa'`
- [x] Регресс Vitest: runtime / auth / outbox / login-page (smoke E2E — отдельно при поднятом стеке)
- [x] Нет изменений продуктового UX кабинета

## Вне scope

- Bearer / launchToken
- VkAdapter, host Back
- Полная политика `update: defer|force` + busy — [T-129](T-129-e009-client-update-policy.md)

## Журнал

### 2026-09-29

- Перенесён в `сделано/` при актуализации бэклога: код в ветке `initiative/i-001-modul-prodazh` (26.09), не в `main`.

### 2026-09-26

- PwaAdapter: CSRF, Passkey, BIP, SW, watchClientUpdate.
- api-client / Login / Profile / InstallNudge через адаптер.
- SW убран из blade; globals + adapter регистрируют SW.
- Vitest runtime/auth/outbox зелёный. Закрыт.

### 2026-09-24

- Тикет создан.
