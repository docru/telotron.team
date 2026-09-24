# T-128 · E-009 · PwaAdapter (вынос текущего PWA)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [E-009](../эпики/E-009-кросплатформенность.md) · этап 7 |
| **Приоритет** | **P0** |
| **Спринт** | — |
| **Роль** | dev |
| **Создан** | 2026-09-24 |
| **Зависит от** | [T-127](T-127-e009-runtime-bootstrap.md) |
| **Блокирует** | [T-131](T-131-e009-vk-adapter-пилот.md) (нужен рабочий шов auth/HTTP) |

## Контекст

Сейчас cookie Sanctum, SW, Passkey, install **вшиты** в shared/layouts. Вынести в `PwaAdapter` **без смены UX** (регресс PWA = блокер).

## Критерии готовности

- [ ] `PwaAdapter` реализует `RuntimeAdapter`: `authMode: 'cookie'`
- [ ] `ensureAuthReady` / `applyAuthToRequest` — CSRF + `credentials: 'same-origin'` (сейчас `sanctum.ts` + `api-client`)
- [ ] `apiJson` берёт auth-патч из адаптера (не хардкод cookie в каждом вызове)
- [ ] Passkey: `supportsPasskey` / ceremony через адаптер; UI по `capabilities().hasPasskey`
- [ ] Install nudge / `beforeinstallprompt` — через адаптер; скрытие по capabilities
- [ ] SW register + version-check layout: либо вызываются из адаптера, либо layout зовёт только `adapter` API (host layout в T-131 без SW)
- [ ] `storageNamespace(): 'pwa'`
- [ ] Регресс: Vitest auth/api; smoke Pro/Client login; outbox Client flush
- [ ] Нет изменений продуктового UX кабинета

## Вне scope

- Bearer / launchToken
- VkAdapter, host Back
- `update: defer|force` политика момента — можно заложить хуки, полная логика в [T-129](T-129-e009-client-update-policy.md)

## Ссылки

- ADR-008 §6 п.1 · исследование этап 2

## Журнал

### 2026-09-24

- Тикет создан.
