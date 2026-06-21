# T-054 Auth · отдельные боты MAX и Telegram для Pro / Client

| Поле | Значение |
|------|----------|
| **Статус** | `in_progress` · папка: **`в-работе/`** |
| **Приоритет** | P1 |
| **Спринт** | 1 |
| **Роль** | dev |
| **Создан** | 2026-06-14 |

## Контекст

Ранее один бот MAX и один Telegram обслуживали обе зоны PWA. Продуктово и для модерации MAX нужны **разные боты**:

| Зона | Аудитория | MAX | Telegram |
|------|-----------|-----|----------|
| **Pro** | тренеры | существующий бот | существующий бот (пока) |
| **Client** | клиенты тренеров | **новый** бот (создан в MAX) | отдельный бот (создать) |

OTP, привязка при регистрации и транзакционные уведомления идут через бота **своей** зоны. Webhook relay prod→local (`WEBHOOK_DEV_RELAY_*`) — **общий**.

Связь: [регистрация-и-вход-max-passkey](../../../_telotron.ru/docs/Бизнес-требования/02-модули/auth/регистрация-и-вход-max-passkey.md), [max-бот-прод-страница](../../../_telotron.ru/docs/Техдок/03-модули/max-бот-прод-страница-и-интеграция.md).

## Решение

### .env (зонные)

```env
MAX_BOT_TOKEN_PRO=…
MAX_BOT_NICK_PRO=…
MAX_BOT_TOKEN_CLIENT=…
MAX_BOT_NICK_CLIENT=…

TELEGRAM_BOT_TOKEN_PRO=…
TELEGRAM_BOT_USERNAME_PRO=…
TELEGRAM_BOT_TOKEN_CLIENT=…
TELEGRAM_BOT_USERNAME_CLIENT=…
```

Legacy `MAX_BOT_TOKEN` / `TELEGRAM_BOT_TOKEN` — fallback **только для pro** (обратная совместимость).

Общие: `MAX_WEBHOOK_SECRET`, `MAX_WEBHOOK_URL` (база), `TELEGRAM_WEBHOOK_SECRET_TOKEN`, `WEBHOOK_DEV_RELAY_*`.

### Код

- `App\Support\MessengerBots` — токены, ники, URL webhook по зоне.
- `App\Support\MessengerBotZoneResolver` — роль пользователя → `pro` | `client`.
- Webhook: `POST /api/v1/webhooks/max/{zone}`, `…/telegram/{zone}`.
- `php artisan max:webhook set --zone=pro|client`
- `php artisan max:updates:poll --zone=pro|client`

## Критерии готовности

- [x] Конфиг и `.env.example` с зонными переменными
- [x] OTP/bind/уведомления используют бота зоны API-запроса или роли пользователя
- [x] Webhook по зоне; relay зеркалит фактический path
- [x] Тесты `MessengerBotsTest`, обновлены OTP flow tests
- [ ] **Операции:** в `.env` prod/local прописать `MAX_BOT_TOKEN_CLIENT` / `MAX_BOT_NICK_CLIENT` (токен второго бота)
- [ ] **Операции:** перевести Pro webhook на `…/max/pro` (`php artisan max:webhook set --zone=pro`), если ещё на старом URL
- [x] **Операции:** создать Telegram-бота для Client
- [ ] **Операции:** прописать `TELEGRAM_*_CLIENT` в prod/local `.env`
- [ ] **Операции:** setWebhook Telegram для `/api/v1/webhooks/telegram/client`

## Журнал

### 2026-06-14

- Решение зафиксировано в auth-доке (открытый вопрос закрыт).
- Реализация: `MessengerBots`, зонные webhook, команды `--zone`.

### 2026-06-16

- **Операции (директор):** TG-бот Client **создан**; канонические аватарки Pro/Client обновлены ([T-053 brand](../сделано/T-053-brand-logos-favicons-pro-client.md)).
- Подключено приложение «Телега» на телефоне и ПК для работы в TG без VPN.
- Остаётся: env `TELEGRAM_*_CLIENT`, webhook client, MAX client token/webhook.
