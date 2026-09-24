# T-130 · E-009 · Auth launchToken: verify VK sign → Bearer

| Поле | Значение |
|------|----------|
| **Статус** | `backlog` · папка: **`бэклог/`** |
| **Эпик** | [E-009](../эпики/E-009-кросплатформенность.md) · этап 7 |
| **Приоритет** | **P0** |
| **Спринт** | — |
| **Роль** | arch + dev (Identity) |
| **Создан** | 2026-09-24 |
| **Зависит от** | ADR-008 §4 |
| **Блокирует** | [T-131](T-131-e009-vk-adapter-пилот.md) |

## Контекст

В host-средах cookie SPA ненадёжны. Нужен серверный путь: verify подписанного launch (`sign` / позже initData) → **наша** сессия (Bearer или эквивалент) для Pro/Client API. PWA cookie path **не ломать**.

## Критерии готовности

- [ ] Конфиг секрета VK Mini App (не в фронте); staging ≠ prod
- [ ] Endpoint exchange: client передаёт launch params явно → verify HMAC/`sign`, TTL `vk_ts` → session token
- [ ] Middleware/guard: API принимает Bearer **рядом** с Sanctum SPA cookie (не вместо PWA)
- [ ] Identity link: `vk_user_id` ↔ User зоны (создание/привязка — правила PO при старте: авто vs confirm phone)
- [ ] Не доверять client-only данным; не вечный проброс raw launch на каждый запрос
- [ ] Feature-тесты: valid/invalid/expired sign; изоляция зон
- [ ] Документация `api-http` § auth host / E-009
- [ ] Заготовка интерфейса verify для MAX/TG initData (можно stub), без реализации пилота

## Вне scope

- OTP-боты MAX/TG (другой контур)
- Полный Ok/Max/Telegram adapter
- UI логина Mini App (его нет — T-131)

## Уточнить при старте (коротко)

| # | Вопрос | Дефолт |
|---|--------|--------|
| 1 | Зона пилота token path | Client (или обе) |
| 2 | Новый vk_user без телефона | создать User / требовать link — **PO** |

## Ссылки

- ADR-008 §4 · VK protect sign / request auth

## Журнал

### 2026-09-24

- Тикет создан.
