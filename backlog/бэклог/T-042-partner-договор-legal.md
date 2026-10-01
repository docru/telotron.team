# T-042 · Partner: in-app договор (P6)

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · код на ветке `partner` (09.07), в `main` не слит · стык с Commerce (I-003) |
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

### 2026-09-29

- Актуализация: реализация лежит в ветке `partner` (09.07, отстаёт от `main` на 84 коммита). Слияние — вместе с Commerce под DEC-007.

### 2026-06-12

- Подтикет E-002 · блокер: [T-092](T-092-legal-партнёрская-программа-пакет-документов.md).
