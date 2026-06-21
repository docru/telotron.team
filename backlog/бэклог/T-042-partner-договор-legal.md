# T-042 · Partner: in-app договор (P6)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` |
| **Эпик** | [T-037](T-037-partner-модуль-эпик.md) |
| **Спринт** | 4 |
| **Оценка** | 6–8 ч |
| **Зависит от** | [T-038](T-038-partner-foundation-config.md), legal document |

## Критерии готовности

- [ ] Legal document `partner_program_agreement` (или согласованный key) в `legal_documents`.
- [ ] `POST /me/legal-acceptances` с `acceptance_context=partner_program` → `partner_profiles.contract_signed_at`.
- [ ] После акцепта: unlimited invites (T-039), L3 enabled, withdrawal UI unlocked.
- [ ] Feature-тест: accept → profile updated; повтор — 409.

## Журнал

### 2026-06-12

- Подтикет T-037 · блокер: текст от юриста к 01.07.
