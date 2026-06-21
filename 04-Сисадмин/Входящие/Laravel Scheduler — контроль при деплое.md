# Входящее: Laravel Scheduler (обязательно при деплое)

**От:** разработка (модуль питания, фото приёмов)  
**Дата:** 2026-05-19  
**Приоритет:** обязательно на **prod** до/сразу после выката версии с очисткой фото

---

## Суть

В приложении зарегистрирована **ежедневная** задача:

```text
nutrition:purge-expired-meal-photos
```

Она удаляет файлы фото приёмов пищи старше **14 суток** (`config/nutrition.php` → `meal_photo_retention_days`).  
Без работающего **Laravel Scheduler** диск будет расти бесконечно, хотя в продукте заявлено хранение 2 недели.

Расписание в коде: `_telotron.ru/bootstrap/app.php` → `Schedule::command('nutrition:purge-expired-meal-photos')->daily()`.

---

## Проверка локального Docker (Sail) — 2026-05-19

Проверено в контейнере `laravel.test` (`docker compose` из `_telotron.ru/`):

| Проверка | Результат |
|----------|-----------|
| `crontab -l` | **нет** (утилита `crontab` отсутствует) |
| демон `cron` | **не запущен** |
| `/etc/cron.d/` | только штатный фрагмент **PHP sessionclean**, не Laravel |
| `* * * * * … schedule:run` | **не настроено** |
| отдельный сервис scheduler в `compose.yaml` | **нет** |

**Вывод для dev:** на локальной машине scheduler **сам не крутится**. Для ручной проверки:

```bash
cd _telotron.ru
docker compose exec -u sail laravel.test php artisan schedule:list
docker compose exec -u sail laravel.test php artisan nutrition:purge-expired-meal-photos
# или долгоживущий процесс (удобно в отдельном терминале):
docker compose exec -u sail laravel.test php artisan schedule:work
```

---

## Что нужно на production

Нужен **ровно один** работающий механизм (как в [runbook-mvp-prod.md](../Инструкции/7-эксплуатация-и-доверие/Инфраструктура/runbook-mvp-prod.md), §2):

### Вариант A — отдельный контейнер/процесс (предпочтительно для Docker)

Сервис с `restart: unless-stopped`, например:

```bash
php /var/www/html/artisan schedule:work
```

(путь к `artisan` — по фактическому mount в prod Compose).

### Вариант B — системный cron на хосте или в контейнере приложения

**Каждую минуту**, от пользователя, под которым крутится приложение:

```cron
* * * * * cd /var/www/html && php artisan schedule:run >> /dev/null 2>&1
```

Заменить `/var/www/html` на реальный каталог приложения на prod.

---

## Чек-лист при деплое (добавить в свой сценарий)

- [ ] После выката коммита с `nutrition:purge-expired-meal-photos` выполнить `php artisan schedule:list` **в prod-контейнере** — в списке есть задача `nutrition:purge-expired-meal-photos`, период **daily**.
- [ ] Убедиться, что на prod **запущен** scheduler (вариант A или B выше), процесс не падает после `docker compose restart`.
- [ ] Один раз вручную (в окно обслуживания):  
  `php artisan nutrition:purge-expired-meal-photos`  
  — убедиться, что команда завершается без ошибок (код 0, в логах нет exception).
- [ ] Зафиксировать в заметке к релизу: «scheduler проверен, purge meal photos — daily».

---

## Связанные документы

- Runbook prod: [runbook-mvp-prod.md](../Инструкции/7-эксплуатация-и-доверие/Инфраструктура/runbook-mvp-prod.md) (§2 Scheduler, §6 деплой)
- Канон API/хранения фото: `_telotron.ru/docs/Техдок/03-модули/nutrition-питание-схема-данных-mvp.md` (§ `nutrition_meal_photos`)

---

## Вопросы к сисадмину

Если на prod уже выбран **вариант A или B** — отметьте в этом файле (или в runbook), какой именно, и путь/имя сервиса cron, чтобы разработка не дублировала настройку.
