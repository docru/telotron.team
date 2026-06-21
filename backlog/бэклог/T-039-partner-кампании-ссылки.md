# T-039 · Partner: кампании и лимиты ссылок (P1)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` |
| **Эпик** | [T-037](T-037-partner-модуль-эпик.md) |
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

### 2026-06-12

- Подтикет T-037 · ADR P1.
