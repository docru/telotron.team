# T-042 · Partner: in-app договор (P6)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` |
| **Эпик** | [E-002](../эпики/E-002-partner-модуль.md) |
| **Спринт** | 4 |
| **Оценка** | 6–8 ч |
| **Зависит от** | [T-038](T-038-partner-foundation-config.md), [T-092](T-092-legal-партнёрская-программа-пакет-документов.md) |

## Критерии готовности

- [ ] Legal document `partner_program_agreement` (или key из [T-092](T-092-legal-партнёрская-программа-пакет-документов.md)) в `legal_documents`.
- [ ] `POST /me/legal-acceptances` с `acceptance_context=partner_program` → `partner_profiles.contract_signed_at`.
- [ ] После акцепта: unlimited invites (T-039), L3 enabled, withdrawal UI unlocked.
- [ ] Feature-тест: accept → profile updated; повтор — 409.

## Журнал

### 2026-06-12

- Подтикет E-002 · блокер: [T-092](T-092-legal-партнёрская-программа-пакет-документов.md).
