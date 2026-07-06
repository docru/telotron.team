# T-067 · Упрощение входа · PWA не на reg + напоминания

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** |
| **Эпик** | [E-003](../эпики/E-003-упрощение-входа.md) · **Упрощение входа** |
| **Слайс** | C-01 |
| **Приоритет** | P1 |
| **Спринт** | этап 1 · Пилот |
| **Оценка** | **4–6 ч** |
| **Роль** | dev (+ дизайнер copy nudge) |
| **Создан** | 2026-06-25 |

## Контекст

Установка PWA **не обязательна** на регистрации и не блокирует первый вход. Периодически — мягкое напоминание «для удобства».

Сейчас: `install_pwa` опционален в [T-060](../сделано/T-060-pro-onboarding-k-p.md); [TelotronInstallBanner](../../../_telotron.ru/resources/ts/widgets/TelotronInstallBanner.vue).

## Критерии готовности

- [x] Reg Pro/Client **не требует** install PWA; нет блокирующего шага install на wizard reg.
- [x] После reg: nudge-ритм (`CabinetInstallNudge`, cooldown N дней в `install-prompt.ts`).
- [x] При активном шаге `install_pwa` в онбординге — suppress дублирующего баннера (канон T-060).
- [ ] После `beforeinstallprompt` / успешной установки — опциональный toast «откройте с главного экрана» (F-04).
- [x] Vitest/smoke: `install-prompt.test.ts`, reg без install проходит.

## Журнал

### 2026-07-05

- Статус **`done`**: фаза 4 E-003 (`CabinetInstallNudge`, cooldown, suppress при `install_pwa`).

### 2026-06-25

- Подтикет эпика E-003 создан.
