# T-003 A1/A11 — минимум prod по runbook

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Закрыт** | 2026-06-11 |
| **Очередь** | 1 · ~8 ч |
| **Приоритет** | P1 |
| **Спринт** | 0 |
| **Роль** | dev / сисадмин |
| **Создан** | 2026-05-21 |

## Контекст

Подготовка **prod** (stage на MVP нет) по [runbook-mvp-prod](../../04-Сисадмин/Инструкции/7-эксплуатация-и-доверие/Инфраструктура/runbook-mvp-prod.md): HTTPS четыре зоны, worker, scheduler, бэкап (по объёму спринта).

**План работ:** [план-деплоя-prod-mvp.md](../../04-Сисадмин/Инструкции/7-эксплуатация-и-доверие/Инфраструктура/план-деплоя-prod-mvp.md).

**Вне scope (gate go/no-go, не блокирует этот тикет):** [T-016](../сделано/T-016-rkn-уведомление-оператор-pd.md) (подано) · [T-021](../бэклог/T-021-rkn-проверка-статуса-уведомления.md) (статус).

## Критерии готовности

- [x] Чеклист runbook §10 (сисадмин) — **2026-05-30**
- [x] Pro/Client/Admin/Public отвечают по HTTPS (`84.252.142.97`, smoke 2026-05-30)
- [x] Протокол/заметка в журнале тикета
- [x] Smoke runbook §5: CSRF SPA, queue job — **2026-06-11** (deploy + ручной прогон)

## Ссылки

- [план-деплоя-prod-mvp](../../04-Сисадмин/Инструкции/7-эксплуатация-и-доверие/Инфраструктура/план-деплоя-prod-mvp.md)
- [план-доработки-период-0](../../../_telotron.ru/docs/Техдок/00-мета/план-доработки-период-0.md) A1, A11
- [T-016](../сделано/T-016-rkn-уведомление-оператор-pd.md) · [T-021](../бэклог/T-021-rkn-проверка-статуса-уведомления.md) — РКН

## Журнал

### 2026-05-21

- Тикет создан для спринта 0.

### 2026-05-22 · planning

- Очередь **1**, ~8 ч — **первый в работу** (длинный полюс к 01.06).
- Async 25.05: что сделано / блокер (DNS, TLS, VPN admin).
- Часть S1–S5 — сисадмин; dev: migrate, build, smoke зон.
- **Prod с нуля** (ВМ/DNS ещё нет) — весь S1–S5 в scope спринта.

### 2026-05-30 · ВМ YC

- **ВМ:** `telotron-prod-01`, `ru-central1-b`, **4 vCPU / 8 GB**, boot **80 GB** + диск **`backups` 50 GB**.
- **IP:** статический **`84.252.142.97`**; SSH **`alex`**, ключ — ok.
- **Снимки:** расписание **`backups`**, 02:00, 10 снимков, привязано к диску **`backups`** (boot без расписания — верно).
- **DNS (REG.RU):** A `@`, `www`, `admin`, `pro`, `client` → **`84.252.142.97`**; MX/SPF/DKIM Mail.ru без изменений.
- **Дальше:** mount `backups`; TLS; cron mysqldump 01:30; VPN; Docker/деплой.

### 2026-05-30 · git + первый bootstrap

- **Deploy key** `telotron-deploy` на prod → GitHub Deploy keys (read-only).
- **`git clone`** → `/opt/telotron/repo`, symlink `/opt/telotron/app`; commit **`9d03d30`** (`origin/main`).
- **`compose.prod.yaml`** в Git — **2026-05-30** (`1ccaeff` и далее)
- Docker build/up: nginx, app, queue, scheduler, mysql, redis.
- Bootstrap: migrate, LegalDocumentSeeder, npm build, config/route/view cache.
- **Smoke:** `https://telotron.ru` → 200; pro/client login → 302; `version.json` ok; scheduler daily purge в списке.
- **Осталось:** smoke CSRF/queue.

### 2026-05-30 · MFA + certbot renew hooks

- **MFA** Yandex Cloud + REG.RU — включено.
- Hooks: `scripts/install-certbot-renew-hooks.sh` → `/etc/letsencrypt/renewal-hooks/`.
- `certbot renew --dry-run --no-random-sleep-on-renew` — **OK**; лог `/var/backups/telotron/log/certbot-renew.log`.

### 2026-05-30 · restore-smoke MySQL (S3)

- Скрипт **`scripts/telotron-mysql-restore-smoke.sh`** → `/usr/local/bin/telotron-mysql-restore-smoke.sh`.
- Restore в **`telotron_restore_smoke`** (prod **`telotron`** не тронут); дамп **`telotron_20260530_125908.sql.gz`** (~40K).
- Проверка: **50** таблиц (совпало с prod), **1** user, **24** migrations; test DB удалена.

### 2026-05-30 · admin login + deploy d5b95e6

- **`telotron-on`** → Filament login OK.
- `./scripts/deploy-prod.sh --smoke` → **d5b95e6**; migrate: nothing; smoke OK.

### 2026-05-30 · deploy 48bbf37

- `git pull` + `./scripts/deploy-prod.sh --composer --npm --smoke` → **48bbf37**.
- Миграция `2026_05_27_100000_add_device_fields_to_legal_acceptances`.
- Smoke: public 200, pro/client 302, version.json ok.

### 2026-05-30 · бэкапы MySQL (S3)

- Скрипт **`/usr/local/bin/telotron-mysql-dump.sh`** (репо: `scripts/telotron-mysql-dump.sh`).
- Каталог **`/var/backups/telotron/mysql/`**, лог **`/var/backups/telotron/log/mysql-dump.log`**.
- Cron **`alex`**: `30 1 * * *` — до снимка YC 02:00.
- Пробный дамп **2026-05-30** (~15K, БД после bootstrap).
- Restore-smoke: см. запись **2026-05-30 · restore-smoke** выше.

### 2026-05-30 · SMTP Mail.ru

- Prod `.env`: `MAIL_MAILER=smtp`, `admin@telotron.ru`, `AUTH_OTP_STUB_EXPOSE_CODE=false`.
- Smoke: `Mail::raw` и `TelotronOtpMail` — **OK** (письма на `admin@telotron.ru`).

### 2026-05-30 · VPN + admin

- **WireGuard** на prod: `10.77.0.0/24`, UDP **51820**, клиент `~/wireguard/telotron-admin-alex.conf`.
- `.env`: `ADMIN_NETWORK_ENFORCE=true`, `ADMIN_ALLOWED_NETWORKS=10.77.0.0/24`.
- Smoke: admin **403** без VPN; public **200**; Filament login с VPN — OK (**2026-05-30**).

### 2026-05-26

- **REG.RU:** домен `telotron.ru` зарегистрирован.
- **Mail.ru:** почта для `@telotron.ru` заведена.
- **Дальше по S1:** после создания ВМ в YC — A/AAAA для четырёх хостов; MFA в REG.RU; TLS.
- **Дальше по почте:** MX/SPF/DKIM в DNS, SMTP в prod `.env`, smoke OTP.

### 2026-05-31 · сверка backlog + certbot в Git

- Prod commit: **`4452c91`** (`8c007a9` hooks, `66c417c` restore-smoke, `d5b95e6` admin Shield).
- Runbook §10 (сисадмин): периметр, TLS, worker/scheduler, бэкап+restore, VPN+admin, MFA, certbot renew — **закрыто**.
- **РКН** подано — [T-016](../сделано/T-016-rkn-уведомление-оператор-pd.md); проверка статуса — [T-021](../бэклог/T-021-rkn-проверка-статуса-уведомления.md).
- **Открыто (tech):** smoke §5 CSRF SPA, queue job.

### 2026-05-31 · backlog

- Тикет → **`в-работе/`** (статус `in_progress`).

### 2026-06-11 · backlog

- Local HEAD **`fb8f6d9`** (автотесты green); prod всё ещё **`4452c91`** — отставание ~18 коммитов.
- **Открыто:** deploy + smoke §5 (CSRF SPA, queue job).

### 2026-06-11 · deploy + закрытие

- Deploy prod **`fb8f6d9`**; smoke §5 (CSRF SPA, queue) в составе ручного прогона.
- Тикет → **`сделано/`**.
