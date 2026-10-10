# Backlog ревизии архитектуры (MVP)

Стартовый список из [Что фиксировать в техдоке](../Инструкции/Что%20фиксировать%20в%20техдоке.md). Закрытые пункты — галочка + ссылка на ADR или PR.

- [ ] Сверка `app/Modules/*` с `backend-архитектура-модулей-mvp.md`
- [ ] Pro vs Client: границы `resources/ts/shared/` vs zone apps
- [ ] Единый паттерн idempotency + outbox для мутаций Client
- [ ] Граница Scheduling ↔ Groups ↔ Reminders
- [ ] Audit на мутациях с ПД (152-ФЗ)
- [ ] Задел billing/partner → **Commerce** [ТЗ](../../../_telotron.ru/docs/Техдок/03-модули/commerce-модуль-тз-mvp.md) · **Partner** [ТЗ](../../../_telotron.ru/docs/Техдок/03-модули/partner-модуль-тз-mvp.md)
- [ ] **E-014 ИИ-РОП** · запрос LLM-инженера (волна 3): [e-014-zapros-arhitektoru-volna-3.md](../../11-AI-инженер/Работа/e-014-zapros-arhitektoru-volna-3.md) — `source=strategy`, черновики HITL, сигналы тренера, оркестратор в LeadGen, лимиты, ADR
