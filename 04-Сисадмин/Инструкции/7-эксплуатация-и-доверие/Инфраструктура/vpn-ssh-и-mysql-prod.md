# VPN: SSH и MySQL на prod

**Назначение:** доступ к **`telotron-prod-01`** по SSH и к MySQL **только через WireGuard** (`10.77.0.0/24`). Публичный IP **`84.252.142.97`** — сайты (80/443) и подключение к VPN (51820/udp); **не** SSH и **не** MySQL.

Связанные документы: [план-деплоя-prod-mvp.md](план-деплоя-prod-mvp.md) §1.2.3, [runbook-mvp-prod.md](runbook-mvp-prod.md) §3.

---

## Параметры VPN (без секретов)

| Параметр | Значение |
|----------|----------|
| Подсеть | **`10.77.0.0/24`** |
| Сервер (prod wg0) | **`10.77.0.1`** |
| Порт WireGuard | **51820/udp** (открыт в UFW и YC) |
| Клиентский конфиг | **`~/wireguard/telotron-admin-alex.conf`** на prod; локально — `scp telotron-prod:~/wireguard/...` |

**Split-tunnel:** в конфиге клиента `AllowedIPs = 10.77.0.1/32` — через VPN идёт только трафик на wg-IP сервера (SSH, admin, MySQL). Публичные сайты — напрямую.

---

## Подключение (рабочая машина)

### 1. Включить VPN

```bash
telotron-on          # алиас → ~/wireguard/telotron-vpn-on.sh
telotron-status      # handshake, admin smoke
```

Перед `telotron-on` выключите **Outline VPN**, если активен.

### 2. SSH

```bash
ssh -i ~/.ssh/telotron-prod alex@10.77.0.1
# или Host telotron-prod в ~/.ssh/config → HostName 10.77.0.1
```

При первом подключении к `10.77.0.1` ssh попросит принять **отдельный** host key (это не тот же ключ, что у `84.252.142.97`).

**Не работает** с публичного IP после ужесточения UFW: `ssh alex@84.252.142.97` → timeout/refused.

### 3. MySQL с локальной машины (DBeaver, PhpStorm, mysql CLI)

**Laravel на prod не меняется:** в prod `.env` остаётся `DB_HOST=mysql` — приложение ходит в контейнер MySQL по внутренней docker-сети, как раньше.

Ниже — только для **вашего компьютера** после `telotron-on`:

| Поле | Значение |
|------|----------|
| Host | **`10.77.0.1`** |
| Port | **`3306`** |
| Database | из prod `.env` → `DB_DATABASE` (обычно `laravel`) |
| User | `DB_USERNAME` (обычно `sail`) |
| Password | `DB_PASSWORD` из prod `.env` на сервере |

```bash
# пример CLI (пароль — из prod .env)
mysql -h 10.77.0.1 -P 3306 -u sail -p laravel
```

Redis **не** проброшен наружу — только из контейнеров на сервере.

---

## Что настроено на сервере

### UFW

| Порт | Кто может |
|------|-----------|
| 51820/udp | любой (вход в VPN) |
| 80, 443/tcp | любой (сайты) |
| 22/tcp | только **`10.77.0.0/24`** |
| 3306/tcp | только **`10.77.0.0/24`** |

Применение / повтор после сброса:

```bash
sudo /opt/telotron/app/scripts/telotron-prod-vpn-firewall.sh
```

### Docker Compose

В **`compose.prod.yaml`**: MySQL слушает **`10.77.0.1:3306`**, не `0.0.0.0`.

Переопределение (если wg-IP другой): `MYSQL_VPN_BIND=10.77.0.1:3306` в prod `.env`.

После смены bind:

```bash
cd /opt/telotron/app
docker compose -f compose.prod.yaml up -d mysql
```

---

## Новый peer WireGuard

1. На prod: добавить `[Peer]` в `/etc/wireguard/wg0.conf`, `sudo wg syncconf wg0 …`
2. Выдать клиенту `.conf` с уникальным `10.77.0.x/32`
3. UFW уже разрешает всю подсеть `10.77.0.0/24` — отдельное правило не нужно

---

## Smoke после изменений

```bash
# VPN выкл → SSH на публичный IP — fail
ssh -o ConnectTimeout=5 alex@84.252.142.97 true   # ожидание: timeout/refused

# VPN вкл
telotron-on
ssh -o ConnectTimeout=5 alex@10.77.0.1 true       # ok
mysql -h 10.77.0.1 -u sail -p -e 'SELECT 1'         # ok

# Сайты без VPN
curl -sI https://telotron.ru | head -1              # HTTP/1.1 200
```

---

## Восстановление доступа

Если потерян SSH: **консоль Yandex Cloud** (serial/VNC) под пользователем с sudo → временно `sudo ufw allow 22/tcp` или запустить `telotron-prod-vpn-firewall.sh` после проверки wg0.

---

## История

| Дата | Изменение |
|------|-----------|
| 2026-06-20 | SSH и MySQL только через VPN; MySQL bind `10.77.0.1:3306` |
