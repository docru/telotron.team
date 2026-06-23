# Скрины для «Онбординг — инструкция для тренеров.md»

Файлы `01` … `10` — вставлены в инструкцию. Полный архив с осмысленными именами: `../../Скрины/`.

| Файл | Что на скрине |
|------|----------------|
| `01_glavnaya_posle_ssylki.jpeg` | Главная telotron.ru после перехода по ссылке |
| `02_registratsiya_pravila.jpeg` | Регистрация Pro, шаг 1: галочки юрдокументов |
| `03_registratsiya_max_bot.jpeg` | Регистрация Pro, шаг 2: команда для бота MAX |
| `04_registratsiya_passkey.jpeg` | Регистрация Pro, шаг 3: Passkey |
| `05_ustanovka_pro.jpeg` | Страница «Установите приложение» (Pro) |
| `06_klienty_ssylka.jpeg` | Раздел «Клиенты»: ссылка для клиента |
| `07_client_registratsiya.jpeg` | Регистрация Client: «Приглашён тренером…» |
| `08_raspisanie.jpeg` | Календарь Pro, вид «Неделя» |
| `09_programmy_trenirovok.jpeg` | «Тренировки» → шаблон программы |
| `10_gruppy.jpeg` | Создание группы |
| `11_client_glavnaya.jpeg` | Client: главная, трекеры (питание, вода, шаги, сон) |
| `12_client_dnevnik_trenirovka.jpeg` | Client: дневник → тренировка, подходы и вес |

Сборка Word (из каталога `Инструкции/`):

```bash
python3 build-onboarding-docx.py
```

Скрипт конвертирует JPEG, встраивает 10 скринов, собирает `.docx` и `.pdf` (для отправки тренерам удобнее PDF).
