# T-131 · E-009 · VkAdapter + host shell (пилот)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [E-009](../эпики/E-009-кросплатформенность.md) · этап 7 |
| **Приоритет** | **P0** |
| **Спринт** | — |
| **Роль** | dev |
| **Создан** | 2026-09-24 |
| **Зависит от** | [T-128](T-128-e009-pwa-adapter.md), [T-129](T-129-e009-client-update-policy.md), [T-130](T-130-e009-auth-launch-token.md) |
| **Блокирует** | закрытие пилота E-009 этап 7 (кабинет) |

## Контекст

Пилот **VK Mini Apps**: общий билд, `VkAdapter`, layout **без** SW/manifest PWA. Вход без OTP/Passkey UI — Bridge + exchange (T-130).

## Критерии готовности

- [ ] `VkAdapter`: Bridge init ≤30с; `authMode: 'launchToken'`; capabilities без Passkey/SW/install/offline shell
- [ ] Host layout/entry зоны пилота: **нет** SW register, **нет** manifest PWA
- [ ] Same-origin митигации (ADR §5b): unregister SW при host; `storageNamespace: 'vk'`
- [ ] Auth: launch → T-130 → `applyAuthToRequest` с Bearer
- [ ] Host Back: hide-first; иначе → главная зоны; на главной → close
- [ ] Update: T-129 (defer/force) на host HTML
- [ ] Скрыть UI `hasPasskey` / `hasInstallPrompt`
- [ ] Ручной/авто smoke: открытие в VK (или iframe-mock) → кабинет API без cookie
- [ ] PWA регресс не сломан
- [ ] Зона пилота зафиксирована PO: **Client** и/или **Pro** (не welcome — тот [T-132](T-132-e009-welcome-clients-host.md))

## Вне scope

- Каталог VK / модерация (чеклист продукта отдельно)
- OK/MAX/TG adapters (тонкие копии позже)
- Stack-back по history

## Ссылки

- ADR-008 · исследование §1.5, §5

## Журнал

### 2026-09-24

- Тикет создан.
