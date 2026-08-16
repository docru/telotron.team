# Каталог Open Food Facts (T-108 · фаза C.1)

**Роль:** сисадмин. **Код поиска/импорта** — разработчик (`nutrition:import-off-dump`).  
**Канон в Git приложения:** `_telotron.ru/scripts/telotron-off-dump-*.sh`, mount в `compose.prod.yaml` / `compose.yaml`.

## Зачем

Клиент **не** ходит в live API OFF. На сервер кладём **дамп** (TSV tab, `.csv.gz` с сайта OFF), импортируем в MySQL. Лицензия ODbL — атрибуция в UI.

Источник: https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz (~0.9 GB gz). Полный unzip (~9 GB) **не** нужен — импорт читает gzip потоком.

## Пути

| Где | Путь |
|-----|------|
| Хост (канон) | `/var/lib/telotron/off/` |
| `current` | `/var/lib/telotron/off/current.tsv.gz` → symlink на `archive/off_*.gz` |
| Archive | `/var/lib/telotron/off/archive/` |
| Incoming | `/var/lib/telotron/off/incoming/` |
| Маркер успеха | `/var/lib/telotron/off/last-ok` |
| Лог fetch | `/var/backups/telotron/log/off-dump-fetch.log` |
| Лог check | `/var/backups/telotron/log/off-dump-check.log` |
| В контейнере | тот же `/var/lib/telotron/off` (bind-mount **ro**) |

Если на boot-диске мало места — каталог на диск `backups` и `TELOTRON_OFF_DIR=/var/backups/telotron/off` + тот же путь в `TELOTRON_OFF_PATH` для compose.

## Env (prod `.env`)

```bash
NUTRITION_OFF_DUMP_PATH=/var/lib/telotron/off/current.tsv.gz
NUTRITION_OFF_DUMPS_DIR=/var/lib/telotron/off
TELOTRON_OFF_PATH=/var/lib/telotron/off
# опционально для скриптов на хосте:
# TELOTRON_OFF_DIR=/var/lib/telotron/off
# TELOTRON_OFF_RETAIN_DAYS=5
# TELOTRON_OFF_MAX_AGE_DAYS=3
# TELOTRON_OFF_MIN_FREE_GB=5
# TELOTRON_OFF_IMPORT=0   # 1 = после скачивания сразу artisan import (тяжело; обычно вручную)
```

Контейнеру **не** нужен исходящий доступ к `*.openfoodfacts.org` для nutrition — качает только хост-скрипт.

## Установка на prod (один раз)

```bash
sudo mkdir -p /var/lib/telotron/off/{archive,incoming} /var/backups/telotron/log
sudo chown -R alex:alex /var/lib/telotron
sudo chmod 755 /var/lib/telotron /var/lib/telotron/off

sudo install -m 755 -o root -g root /opt/telotron/app/scripts/telotron-off-dump-fetch.sh /usr/local/bin/telotron-off-dump-fetch.sh
sudo install -m 755 -o root -g root /opt/telotron/app/scripts/telotron-off-dump-check.sh /usr/local/bin/telotron-off-dump-check.sh
```

В `.env` — переменные выше. Пересоздать контейнеры с новым volume:

```bash
cd /opt/telotron/app
docker compose -f compose.prod.yaml up -d laravel.test queue scheduler
```

Cron пользователя **`alex`** (скачивание **03:15**, проверка **04:00**):

```bash
( crontab -l 2>/dev/null | grep -v telotron-off-dump- || true
  echo '15 3 * * * /usr/local/bin/telotron-off-dump-fetch.sh'
  echo '0 4 * * * /usr/local/bin/telotron-off-dump-check.sh'
) | crontab -
crontab -l
```

Stage на MVP нет — тот же процесс только на prod (реже можно: `0 3 * * 0` раз в неделю).

## Ручное обновление каталога

```bash
# 1) скачать свежий дамп (~0.9 GB)
/usr/local/bin/telotron-off-dump-fetch.sh
ls -lh /var/lib/telotron/off/current.tsv.gz
tail /var/backups/telotron/log/off-dump-fetch.log

# 2) импорт в MySQL (разработчик / согласованное окно; долго на полном дампе)
cd /opt/telotron/app
docker compose -f compose.prod.yaml exec -u sail -T laravel.test \
  php artisan nutrition:import-off-dump /var/lib/telotron/off/current.tsv.gz --ru-only=1

# 3) проверка свежести
/usr/local/bin/telotron-off-dump-check.sh
```

Опционально автоимпорт после fetch: `TELOTRON_OFF_IMPORT=1` в окружении cron (не включать без окна нагрузки).

## Мониторинг

| Сигнал | Как |
|--------|-----|
| Дамп старше N суток | `telotron-off-dump-check.sh` → exit 1; лог `off-dump-check.log` |
| Мало места | тот же скрипт → exit 2; `df -h /var/lib/telotron` |
| Fetch упал | нет новой строки `OK` в `off-dump-fetch.log`; нет обновления `last-ok` |

На MVP отдельный внешний алерт не обязателен — смотреть логи / exit code cron mail.

## Локальная отладка (без 0.9 GB)

Compose уже монтирует `./storage/app/nutrition/off-dumps` → `/var/lib/telotron/off`.

```bash
cd _telotron.ru
mkdir -p storage/app/nutrition/off-dumps/{archive,incoming}
TELOTRON_OFF_DIR="$(pwd)/storage/app/nutrition/off-dumps" \
TELOTRON_OFF_LOG_DIR="$(pwd)/storage/logs" \
  ./scripts/telotron-off-dump-fetch.sh --from-file tests/Fixtures/nutrition/off-dump-sample.tsv

TELOTRON_OFF_DIR="$(pwd)/storage/app/nutrition/off-dumps" \
TELOTRON_OFF_LOG_DIR="$(pwd)/storage/logs" \
  ./scripts/telotron-off-dump-check.sh

# после recreate laravel.test (новый volume):
docker compose up -d laravel.test
docker compose exec -u sail -T laravel.test \
  php artisan nutrition:import-off-dump /var/lib/telotron/off/current.tsv.gz --ru-only=1
```

## Связи

- Тикет: [T-108](../../../../backlog/в-работе/T-108-ux-kbju-vvod-edy-client.md) §4.1 C.1  
- Деплой: `_telotron.ru/docs/Техдок/04-платформа-и-эксплуатация/деплой-кода-prod.md`  
- Схема: `_telotron.ru/docs/Техдок/03-модули/nutrition-питание-схема-данных-mvp.md`
