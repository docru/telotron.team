# План деплоя prod (MVP)

**Назначение:** пошаговый сценарий **первого** выката и **ручных** последующих релизов на prod. Канон решений — [runbook-mvp-prod.md](runbook-mvp-prod.md). Тикет спринта 0: [T-003-a1-a11-prod-runbook](../../../../backlog/сделано/T-003-a1-a11-prod-runbook.md) **`done`**.

**Окружение:** один **prod** в Яндекс Облаке; **stage нет**. CI/CD на MVP **нет** — `git pull` + ручной перезапуск контейнеров.

**Роли:** **сисадмин** — ВМ, DNS, TLS, VPN, бэкапы, `.env` на сервере; **dev** — compose/worker/scheduler, migrate, build, smoke.

---

## 0. Зафиксированные параметры (без секретов)

| Параметр | Значение |
|----------|----------|
| Облако | Яндекс Облако, ВМ **`telotron-prod-01`**, зона **`ru-central1-b`**, **4 vCPU / 8 GB RAM** (вариант Б) |
| Публичный IP | **`84.252.142.97`** (статический), внутренний `10.129.0.4` |
| SSH | Пользователь **`alex`**, вход **по ключу** (2026-05-30) |
| Диски | Boot **80 GB** SSD + **`backups` 50 GB** SSD (отдельно от boot) |
| Домен | **`telotron.ru` зарегистрирован** в [REG.RU](https://www.reg.ru/) (2026-05-26) |
| DNS | REG.RU → A **`84.252.142.97`**: `@`, `www`, `admin`, `pro`, `client` — **2026-05-30**; MX/SPF/DKIM Mail.ru без изменений |
| Зоны | `telotron.ru`, `admin.telotron.ru`, `pro.telotron.ru`, `client.telotron.ru` |
| Почта | **`@telotron.ru` на Mail.ru** (2026-05-26); SMTP prod — **`admin@telotron.ru`**, **2026-05-30** |
| Админка | Только с **VPN** (WireGuard **10.77.0.0/24**, порт **51820/udp**); `ADMIN_NETWORK_ENFORCE=true` — **2026-05-30** |
| Бэкапы YC | Расписание **`backups`**: ежедневно **02:00**, хранить **10** снимков — на диске **`backups`** (2026-05-30) |
| Mount бэкапов | **`/var/backups/telotron`** — mysql дампы, app-storage, log |
| Секреты | Закрытый `.env` на сервере (`chmod 600`), не в Git |

Дописать позже: ~~CIDR VPN~~ **10.77.0.0/24**; имя cron-скрипта дампа — без паролей и токенов.

---

## 1. Предусловия (до первого деплоя)

### 1.1 Инфраструктура (сисадмин) — дорожка S1–S5

- [x] **S1** ВМ **`telotron-prod-01`** создана (4 vCPU / 8 GB), SSH **`alex`** по ключу — 2026-05-30
- [x] **S1** Статический публичный IP **`84.252.142.97`** — 2026-05-30
- [x] **S1** DNS A на **`84.252.142.97`**: `@`, `www`, `admin`, `pro`, `client` (REG.RU) — 2026-05-30
- [x] **S1** Домен зарегистрирован в REG.RU — 2026-05-26
- [x] **S1** TLS (Let's Encrypt) на четырёх хостах — **2026-05-30**
- [x] **S1** Certbot **renew hooks** (stop/reload nginx) — **2026-05-30**; `certbot.timer`, dry-run OK
- [x] **S1** Диск **`backups`** (50 GB) **смонтирован** в `/var/backups/telotron` на сервере — 2026-05-30
- [x] **S2** VPN → admin — **2026-05-30** (WireGuard, см. §1.2.3)
- [x] **S3** Расписание снимков YC **`backups`** (02:00, 10 снимков) на диск **`backups`** — 2026-05-30
- [x] **S3** Cron **`mysqldump`** → `/var/backups/telotron/mysql` (**01:30**, до снимка) — **2026-05-30**
- [x] **S3** Пробный restore — **2026-05-30** (`telotron-mysql-restore-smoke.sh`, БД `telotron_restore_smoke`)
- [x] **S5** MFA: Yandex Cloud, REG.RU — **2026-05-30**

### 1.2 Приложение (dev + сисадмин)

- [x] Репозиторий на сервере: **`git clone`** в `/opt/telotron/repo`, deploy key — **2026-05-30** (commit `9d03d30`)
- [x] Prod `.env` на сервере — **2026-05-30** (`chmod 600`, SMTP Mail.ru OK)
- [x] Почта `@telotron.ru` заведена в **Mail.ru** — 2026-05-26
- [x] MX/SPF/DKIM для домена в DNS (REG.RU) — **2026-05-30** (см. §1.2.2)
- [x] SMTP Mail.ru прописан в prod `.env`, тест OTP с prod — **2026-05-30** (`admin@telotron.ru`, SMTP + `TelotronOtpMail` OK)
- [x] В compose prod: **queue worker** и **scheduler** — **2026-05-30**
- [x] MySQL и Redis **без** проброса портов на хост — **2026-05-30**

#### 1.2.2 DNS почты (проверка 2026-05-30)

| Запись | Ожидание Mail.ru | Факт |
|--------|------------------|------|
| **MX** | `emx.mail.ru` | `10 emx.mail.ru` ✅ |
| **SPF** | `v=spf1 redirect=_spf.mail.ru` | ✅ + `mailru-domain: …` (верификация) |
| **DKIM** | селектор **`mailru`** | `mailru._domainkey.telotron.ru` ✅ |
| **DMARC** | опционально | не настроен |

SMTP с prod: **`smtp.mail.ru:465`** (SSL) — порт доступен с сервера ✅.

**Prod `.env` (после пароля приложения):**

```env
MAIL_MAILER=smtp
MAIL_SCHEME=smtps
MAIL_HOST=smtp.mail.ru
MAIL_PORT=465
MAIL_USERNAME=noreply@telotron.ru
MAIL_PASSWORD=<пароль для внешнего приложения Mail.ru>
MAIL_FROM_ADDRESS=noreply@telotron.ru
MAIL_FROM_NAME="${APP_NAME}"
AUTH_OTP_STUB_EXPOSE_CODE=false
```

Пароль: Mail.ru → ящик → **Настройки → Безопасность → Пароли для внешних приложений** (не основной пароль). После правки: `config:cache`, smoke OTP.

#### 1.2.3 VPN WireGuard → admin (2026-05-30)

| Параметр | Значение |
|----------|----------|
| Продукт | **WireGuard** на **`telotron-prod-01`** |
| Подсеть VPN | **`10.77.0.0/24`** (сервер `10.77.0.1`, клиент alex `10.77.0.2`) |
| Порт | **51820/udp** (UFW + YC security group) |
| Split-tunnel | `AllowedIPs = 10.77.0.1/32` — через VPN только wg-IP сервера (не публичный IP: иначе петля маршрута на YC) |
| Laravel | `ADMIN_NETWORK_ENFORCE=true`, `ADMIN_ALLOWED_NETWORKS=10.77.0.0/24` |

Конфиг клиента на сервере: **`~/wireguard/telotron-admin-alex.conf`** (`chmod 600`).

**Подключение (рабочая машина, через GUI — как `client_adfinity`):**

```bash
scp telotron-prod:~/wireguard/telotron-admin-alex.conf ~/wireguard/
bash ~/wireguard/setup-telotron-vpn-gui.sh   # один раз: импорт в NetworkManager
```

Дальше — **алиасы в терминале** (GUI для WireGuard в Ubuntu 22.04 нет):

```bash
telotron-on      # включить VPN + admin.telotron.ru → 10.77.0.1
telotron-off     # выключить
telotron-status  # состояние
```

Скрипты: `~/wireguard/telotron-vpn-on.sh`, `telotron-vpn-off.sh`. Перед `telotron-on` выключите **Outline VPN**, если активен.

**Smoke:**

| Проверка | Ожидание |
|----------|----------|
| VPN **выкл** → `curl -I https://admin.telotron.ru/infra-check` | **403** |
| VPN **вкл** → `https://admin.telotron.ru` | Filament login |
| VPN **выкл** → `https://telotron.ru` | **200** (public не затронут) |

**Первый админ Filament:** в prod `.env` задать **`ADMIN_PHONE`** + **`ADMIN_PASSWORD`**, затем:

```bash
docker compose -f compose.prod.yaml exec -u sail -T laravel.test php artisan db:seed --class=AdminUserSeeder --force
```

Сервис: `sudo systemctl status wg-quick@wg0`.

**SSH и MySQL только через VPN (2026-06-20):** UFW — `22` и `3306` только из `10.77.0.0/24`; MySQL проброшен на `10.77.0.1:3306` (Laravel по-прежнему `DB_HOST=mysql`). Подробно: [vpn-ssh-и-mysql-prod.md](vpn-ssh-и-mysql-prod.md).

```bash
telotron-on
ssh -i ~/.ssh/telotron-prod alex@10.77.0.1    # не 84.252.142.97
# DBeaver: host 10.77.0.1:3306, user/password — DB_* в prod .env
```

#### 1.2.1 Git на prod: отдельный deploy key (решение)

Репозиторий **private** (`git@github.com:docru/telotron.ru.git`). Для первого bootstrap код можно доставить **rsync** с рабочей машины; для последующих релизов — **`git pull` на сервере**.

**Решение (2026-05-30):** завести **отдельный SSH-ключ только для prod**, не личный ключ разработчика.

| Шаг | Действие |
|-----|----------|
| 1 | На **`telotron-prod`**: `ssh-keygen -t ed25519 -f ~/.ssh/telotron-deploy -C "telotron-prod deploy" -N ""` |
| 2 | Публичный ключ `~/.ssh/telotron-deploy.pub` → **Deploy keys** репозитория GitHub (read-only) — **2026-05-30** |
| 3 | `~/.ssh/config` на prod: `Host github.com-telotron` → `IdentityFile ~/.ssh/telotron-deploy`, `IdentitiesOnly yes` |
| 4 | Clone: `git clone git@github.com-telotron:docru/telotron.ru.git /opt/telotron/repo`; symlink `/opt/telotron/app` → `repo` |
| 5 | Рабочий каталог compose: **`/opt/telotron/app`** (корень репозитория = Laravel-приложение) |

Права: ключ **`chmod 600`**, только пользователь **`alex`**. Deploy key **не** использовать для других хостов и **не** копировать на dev-машины.

**До настройки ключа:** ручной деплой — rsync/scp с исключениями `vendor/`, `node_modules/`, `.env`, `storage/` (см. §4).

### 1.3 Блокеры вне сисадмина (зафиксировать статус)

- [ ] Уведомление **Роскомнадзора** (оператор ПДн) — для открытия регистрации пользователей; не блокирует технический деплой, но блокирует go-live по [runbook §10](runbook-mvp-prod.md)

---

## 2. Подготовка prod Compose (один раз или при изменении инфраструктуры)

Текущий локальный [compose.yaml](../../../../_telotron.ru/compose.yaml): nginx + `laravel.test` + mysql + redis. Для prod **добавить** (dev):

### 2.1 Обязательные сервисы

| Сервис | Команда / заметка |
|--------|-------------------|
| **queue** | `php artisan queue:work --sleep=3 --tries=3` (или `queue:listen`), `restart: unless-stopped`, тот же образ/volume, что app |
| **scheduler** | `php artisan schedule:work`, `restart: unless-stopped`, **один** экземпляр |

См. [Laravel Scheduler — контроль при деплое](../../../Входящие/Laravel%20Scheduler%20—%20контроль%20при%20деплое.md).

### 2.2 Prod-отличия от local

| Local | Prod |
|-------|------|
| mkcert в `docker/nginx/certs/` | Сертификаты Let's Encrypt (путь в `.env`: `NGINX_SSL_CERT_FILE`, `NGINX_SSL_KEY_FILE`) |
| `telotron.test` | Боевые FQDN в `NGINX_*_HOST` |
| `FORWARD_DB_PORT` / `FORWARD_REDIS_PORT` | **Не публиковать** порты БД/Redis |
| `MAIL_MAILER=log` | SMTP Mail.ru |
| `ADMIN_NETWORK_ENFORCE=false` | `true` + CIDR VPN |

### 2.3 Диск бэкапов и M5

- Cron на хосте или в контейнере: дамп MySQL в каталог на **отдельном диске**.
- Каталог файлов планов / `storage` (M5) — **bind-mount на тот же диск**, чтобы попадал в ежедневный снапшот (путь согласовать с dev).

### 2.4 Сборка и подъём

Из каталога приложения на сервере (`_telotron.ru/` или фактический путь):

```bash
docker compose build
docker compose up -d
docker compose ps
```

---

## 3. Первый деплой (bootstrap)

После §1 и §2, на сервере:

```bash
cd /opt/telotron/app
./scripts/deploy-prod.sh bootstrap --smoke
```

Скрипт: composer, npm build, `key:generate` (если нужно), migrate, LegalDocumentSeeder, AdminUserSeeder (если `ADMIN_*` в `.env`), кэши, restart. Commit — в журнал T-003.

Ручные команды — в [деплой-кода-prod.md](../../../../_telotron.ru/docs/Техдок/04-платформа-и-эксплуатация/деплой-кода-prod.md).

### 3.1 Scheduler (обязательная проверка)

```bash
docker compose exec -u sail laravel.test php artisan schedule:list
docker compose exec -u sail laravel.test php artisan nutrition:purge-expired-meal-photos
```

В списке должна быть **daily** задача `nutrition:purge-expired-meal-photos`.

### 3.2 Queue

```bash
docker compose exec -u sail laravel.test php artisan queue:monitor
# или убедиться, что контейнер queue в статусе Up и в логах нет постоянных crash
docker compose logs -f queue
```

---

## 4. Ручной деплой (каждый следующий релиз)

**На сервере** (`/opt/telotron/app`):

```bash
# обычный релиз
./scripts/deploy-prod.sh --smoke

# с миграциями / риском для БД
./scripts/deploy-prod.sh --backup --smoke
```

Скрипт: `git pull`, composer/npm при изменении lock-файлов, migrate, кэши, restart. **Записать commit** из вывода в журнал T-003.

Подробно: [`деплой-кода-prod.md`](../../../../_telotron.ru/docs/Техдок/04-платформа-и-эксплуатация/деплой-кода-prod.md) (`scripts/deploy-prod.sh --help`).

<details>
<summary>Без скрипта (шаги вручную)</summary>

1. **Бэкап БД** (если миграции):
   ```bash
   /usr/local/bin/telotron-mysql-dump.sh
   ```
2. `git pull` в `/opt/telotron/app` — **записать hash** в журнал.
3.–7. Composer / npm / migrate / кэши / restart — см. техдок § «Ручной релиз».
8. Проверки из §5.

</details>

**PWA:** если менялись SW, precache, layout зон — в том же коммите поднять `build.pro` / `build.client` в `config/version.php`.

---

## 5. Smoke после деплоя

| Проверка | Команда / действие | Ожидание |
|----------|-------------------|----------|
| Public | `curl -I https://telotron.ru` | 200, HTTPS |
| Pro | `curl -I https://pro.telotron.ru/login` | 200 |
| Client | `curl -I https://client.telotron.ru/login` | 200 |
| Pro PWA | `curl -s https://pro.telotron.ru/version.json` | JSON `version` + `build` |
| Client PWA | `curl -s https://client.telotron.ru/version.json` | JSON `version` + `build` |
| Admin | Браузер **через VPN** → `https://admin.telotron.ru` | Filament login |
| Admin без VPN | С обычного IP | **403** |
| CSRF SPA | `curl -I https://pro.telotron.ru/sanctum/csrf-cookie` | Set-Cookie |
| Infra (если есть) | `GET https://admin.telotron.ru/infra-check` (с VPN) | JSON ok |
| OTP e-mail | Тестовый запрос OTP (не stub) | Письмо пришло |
| Scheduler | `schedule:list` + процесс scheduler **Up** | daily purge в списке |
| Queue | Тестовый job / логи worker | Обработка без вечного pending |

При ошибках — **не** считать релиз завершённым; откат по §6.

**Статус smoke (2026-05-30):** ✅ public, pro/client login, PWA version.json, admin VPN+Filament, scheduler, OTP SMTP · ⬜ CSRF SPA, queue job

---

## 6. Откат

| Ситуация | Действие |
|----------|----------|
| Плохой код, БД не тронута | `git checkout <prev-commit>` → §4 шаги 3–8 без migrate |
| Плохая миграция | Остановить трафик (по возможности) → восстановить **дамп БД** из §1.3 → откат git → §4 без migrate |
| Потеря диска / ВМ | Новая ВМ → mount **снапшота** диска или restore дампа → §3 |

После любого restore — повторить **§5** и записать дату в журнал T-003 / runbook §7.

---

## 7. Чеклист runbook §10 (закрытие T-003)

Отметить при закрытии тикета; «перенос» — с датой и причиной.

- [x] Периметр: только 80/443 (+22 SSH); MySQL/Redis не снаружи — **2026-05-30**
- [x] TLS на всех четырёх зонах + certbot renew hooks — **2026-05-30**
- [x] Worker + scheduler в prod — **2026-05-30**
- [x] Бэкапы: cron dump + снапшот диска; пробное восстановление — **2026-05-30** (restore-smoke OK)
- [x] Admin за VPN/CIDR + Filament login — **2026-05-30**
- [x] `.env` вне Git, права минимальны; MFA YC + REG.RU — **2026-05-30**
- [ ] РКН: статус уведомления (не зона сисадмина): _____

---

## 8. Журнал деплоев (шаблон)

Копировать блок в [T-003](../../../../backlog/сделано/T-003-a1-a11-prod-runbook.md) или сюда.

```markdown
### YYYY-MM-DD · deploy

- Commit: `abc1234` (branch: main)
- Кто: …
- Миграции: да/нет
- Smoke §5: ok / блокер: …
- Scheduler проверен: да/нет
- Откат не потребовался / откат: …
```

---

## 9. Связанные документы

- [runbook-mvp-prod.md](runbook-mvp-prod.md)
- [деплой-кода-prod.md](../../../../_telotron.ru/docs/Техдок/04-платформа-и-эксплуатация/деплой-кода-prod.md)
- [Безопасность.md](Безопасность.md)
- [локальная-среда-docker-nginx.md](../../../../_telotron.ru/docs/Техдок/04-платформа-и-эксплуатация/локальная-среда-docker-nginx.md)
- [план-доработки-период-0 §1.3 A1+A11](../../../../_telotron.ru/docs/Техдок/00-мета/план-доработки-период-0.md)
- [домены-маршруты-сессии.md](../../../../_telotron.ru/docs/Техдок/02-зоны/домены-маршруты-сессии.md)
