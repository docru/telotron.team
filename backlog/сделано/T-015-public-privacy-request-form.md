# T-015 Dev · Публичная форма обращений по ПДн (ФОС)

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Родитель** | [T-007](../бэклог/T-007-legal-privacy-v1-compliance.md) §4 |
| **Приоритет** | **P2** (желательно к **01.06**, можно сразу после P1) |
| **Очередь** | 3d · **~6–10 ч** |
| **Спринт** | 0–1 |
| **Роль** | dev |
| **Создан** | 2026-05-27 |
| **Закрыт** | 2026-05-27 |

## Контекст

[Сборка-политики-v1-факты](../../07-Юрист/Сборка-политики-v1-факты.md) §8.3: к **01.06** каналы по ПДн — **e-mail** (`admin@telotron.ru`, уже на A13) **+ форма на сайте**.

**Не в scope:** реестр `privacy_requests` в админке, SLA-трекинг — отдельное решение ([T-007](../бэклог/T-007-legal-privacy-v1-compliance.md) §5).

## Критерии готовности

- [x] Форма доступна без авторизации на `telotron.ru`
- [x] В политике и на A13 — **рабочая** ссылка (не «при размещении»)
- [x] Обращение доходит до `admin@telotron.ru` (или согласованный канал)

## Реализация

- URL: **`/legal/privacy-request`** (`public.privacy-request`)
- POST → `PrivacyRequestMail` на `config('telotron.public.contact_email')`, без записи ПДн в БД/логи тела
- Rate limit: `public-privacy-request` (5/мин/IP), honeypot, CSRF
- Footer A13 + юрдокументы: ссылка «Обращения по персональным данным»
- Источники v1.0 обновлены; на prod: `php artisan legal:publish-v1-sources`

## Журнал

### 2026-05-27

- Тикет выделен из [T-007](../бэклог/T-007-legal-privacy-v1-compliance.md).

### 2026-05-19

- `PublicPrivacyRequestController`, `PrivacyRequestType`, `PrivacyRequestMail`, тесты `PublicPrivacyRequestTest`.

### 2026-05-31 · backlog

- Тикет в **`сделано/`** (сверка индекса).
