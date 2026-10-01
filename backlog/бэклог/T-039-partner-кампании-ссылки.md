# T-039 · Partner: кампании и лимиты ссылок (P1)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · код на ветке `partner` (09.07), в `main` не слит · стык с Commerce (I-003) |
| **Эпик** | [E-002](../эпики/E-002-partner-модуль.md) |
| **Спринт** | 4 |
| **Оценка** | 8–10 ч |
| **Зависит от** | [T-038](T-038-partner-foundation-config.md) |

## Критерии готовности

- [ ] `PartnerInviteLimitService`: без договора — max **1** active `specialist_referral`; с договором — unlimited.
- [ ] Расширение `POST /me/invite-tokens` (`purpose=specialist_referral`): `title` = кампания; **422** при превышении лимита.
- [ ] Счётчик регистраций на token (`referral_attributions`).
- [ ] `platform_trainer_recruitment` — без изменений выпуска; флаг **no_commission** в Partner.
- [ ] Feature-тест: 2-я ссылка без договора → 422; с договором → ok; отзыв.

## Журнал

### 2026-09-29

- Актуализация: реализация лежит в ветке `partner` (09.07, отстаёт от `main` на 84 коммита). Слияние — вместе с Commerce под DEC-007.

### 2026-06-12

- Подтикет E-002 · ADR P1.
