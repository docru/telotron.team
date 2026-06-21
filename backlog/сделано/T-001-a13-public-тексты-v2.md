# T-001 A13 public — тексты и визайн v2

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Закрыт** | 2026-06-11 |
| **Очередь** | 2 · ~6 ч |
| **Приоритет** | P1 |
| **Спринт** | 0 |
| **Роль** | dev + PO (тексты) |
| **Создан** | 2026-05-21 |

## Контекст

Публичная страница `telotron.ru` (A13): выровнять контент §6.2 ТЗ и визуал [v2](../../08-Дизайнер/Инструкции/Задание%20разработчику%20—%20public-страница%20A13%20вёрстка%20и%20дизайн%20v2.md).

Stage на MVP **нет** — приёмка на **prod** после deploy ([T-003](T-003-a1-a11-prod-runbook.md) **`done`**).

## Критерии готовности

- [x] Тексты согласованы с [ТЗ A13](../../01-Директор/Инструкции/ТЗ%20—%20public-страница%20проекта%20(A13).md) §6.2
- [x] Визуал v2 внедрён в welcome/public (карточки hero/features — `app.css`)
- [x] CTA `/i/{token}`, footer, юр. ссылки — **в коде** (`welcome.blade.php`, `telotron-public-footer`, `PlatformWebsiteTrainerInvite`, `/legal/*`, [T-015](../сделано/T-015-public-privacy-request-form.md), radius [T-017](../сделано/T-017-radius-delovoy-stil.md))
- [x] `PublicWelcomePageTest` green (CTA, footer, `/i/{token}` → Pro)
- [x] Smoke **prod** `https://telotron.ru`: «Начать бесплатно» → `/i/{token}`; footer: privacy, terms, ФОС — **2026-06-11** (ручной прогон, [T-002](T-002-a8-критичные-сценарии.md))

## Ссылки

- [план-доработки-период-0](../../../_telotron.ru/docs/Техдок/00-мета/план-доработки-период-0.md) §1.2 A13
- `tests/Feature/Public/PublicWelcomePageTest.php`

## Журнал

### 2026-05-21

- Тикет создан для спринта 0.

### 2026-05-22 · planning

- Очередь **2**: сначала черновик текстов (PO, §6.2 ТЗ), затем v2 в коде, smoke **prod** (stage нет).
- Параллельно с **T-003**; не блокирует инфру.

### 2026-05-24 · dev

- `welcome.blade.php`: тексты §6.2 (lead, about, буллеты, capabilities, meta).
- Реквизиты footer только из `config('telotron.public.operator')`.
- `PublicWelcomePageTest` обновлён под §6.2.

### 2026-05-31 · сверка

- Критерии **кода** закрыты: v2 layout, CTA, footer + [T-015](../сделано/T-015-public-privacy-request-form.md), деловой radius [T-017](../сделано/T-017-radius-delovoy-stil.md).
- **Открыто:** deploy + smoke prod ([T-002](T-002-a8-критичные-сценарии.md)).

### 2026-05-31 · backlog

- Тикет → **`в-работе/`** (статус `in_progress`).

### 2026-06-11 · backlog

- Код ✅; **открыто:** deploy `fb8f6d9` → smoke prod (в составе T-002).

### 2026-06-11 · закрытие

- Deploy prod + ручной smoke PUB-01–02 ([Ручной прогон gate 01.06](../../09-Тестировщик/Инструкции/Ручной%20прогон%20gate%2001.06.md)).
- Тикет → **`сделано/`**.
