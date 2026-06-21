# T-018 Client · шапка: логотип + имя тренера

| Поле | Значение |
|------|----------|
| **Статус** | `done` |
| **Закрыт** | 2026-06-09 |
| **Очередь** | 4 · ~4–6 ч |
| **Приоритет** | P1 |
| **Спринт** | 0 |
| **Роль** | dev + дизайн (приёмка) |
| **Создан** | 2026-05-31 |

## Контекст

Заказчик: **не нравится** текущий вывод имени тренера у клиента.

**Сейчас (несогласованно):**

| Экран | Слева в sticky-шапке |
|-------|----------------------|
| Главная, Дневник | Только **имя тренера** или нативный `<select>` — **без логотипа** (`TelotronClientTrainerShellHeader`, `clientTrainerHeader: true`) |
| Прогресс, Профиль, Поддержка | **Логотип + «Телотрон» + «Client»** — **без имени тренера** (`TelotronPublicHeader`) |

Клиент теряет и бренд, и контекст «с кем я работаю» в зависимости от вкладки.

**Цель:** единая шапка Client после входа — **логотип Телотрон + имя активного тренера**; в перспективе — **аватар тренера**. Переключение при нескольких тренерах — без `<select>` в header.

Связь: [логотип в шапке кабинета](../../08-Дизайнер/Инструкции/Задание%20разработчику%20—%20логотип%20в%20шапке%20кабинета.md) (Pro), [T-017 radius](../сделано/T-017-radius-delovoy-stil.md) (деловой стиль, `rounded-md`).

---

## Решение (канон UI)

### Макет — зеркало Pro, вторая строка = тренер

**Pro (эталон):**

```
[logo 40]  Телотрон              [🔔] [👤]
           Pro
```

**Client (целевой):**

```
[logo 40]  Телотрон              [🔔] [👤]
           Иван Петров ▼
```

| Правило | Деталь |
|---------|--------|
| Строка 1 | **Телотрон** (как Pro), подпись **«Client» не показывать** |
| Строка 2 | `activeTrainerDisplayName` из `useClientActiveTrainerStore` |
| Один тренер | Имя без chevron, не кликабельно |
| Несколько тренеров | Имя + `ChevronDown`; тап → **Sheet** со списком тренеров |
| Где показывать | **Все** авторизованные экраны Client — убрать флаг `route.meta.clientTrainerHeader` |
| Высота | По умолчанию `--header-h` (56px); если с аватаром тесно — **64px только для Client** (согласовать на приёмке) |

### Этап 2 (в этом тикете — задел, без API фото)

Между логотипом и текстом — **`TelotronAvatar`** по `display_name` (инициалы), `size="sm"`:

```
[logo 32] [AV 28]  Телотрон
                   Иван Петров ▼
```

Логотип **не убирать**. Когда появится `avatar_url` в API — подставить фото (отдельный подпункт, не блокер MVP тикета).

### Sheet «Ваши тренеры» (если `linkedTrainers.length > 1`)

- Список: аватар (инициалы) + имя; галочка / highlight у активного
- Подпись: «Данные на главной и в дневнике — от выбранного тренера»
- Выбор → `trainerStore.setActiveTrainerUserId(id)`; закрыть sheet
- Контент страниц с `trainer_user_id` перечитывается (как при смене select сейчас)

### Запрещено

- Нативный `<select>` в шапке
- Только имя без логотипа
- Разные шапки на разных вкладках Client
- Pill/capsule для переключателя (T-017)

---

## Файлы

| Файл | Действие |
|------|----------|
| `resources/ts/widgets/TelotronClientTrainerShellHeader.vue` | Переписать: logo + 2 строки + avatar + sheet |
| `resources/ts/widgets/TelotronAppShell.vue` | Client: **всегда** новый header; убрать ветку `showClientTrainerHeader` / `TelotronPublicHeader` для Client shell |
| `resources/ts/app/client/router/routes.ts` | Удалить `clientTrainerHeader` из meta |
| `resources/ts/env.d.ts` | Удалить `clientTrainerHeader?` |
| `resources/css/app.css` | Стили `.telotron-client-shell-header*`; при необходимости `--header-h-client` |
| Новый (опц.) | `TelotronClientTrainerPickerSheet.vue` |
| `resources/ts/shared/stores/client-active-trainer.ts` | Без смены контракта; регрессия смены тренера |
| `config/version.php` | **`build.client`** +1 |

**Тесты (добавить/обновить):**

- Vitest: рендер header при 1 / N тренерах (mock store)
- При наличии e2e Client — smoke смены тренера

**API (post-MVP, не блокер):** `GET /me/linked-trainers` — поле `avatar_url` nullable.

---

## Критерии готовности

- [x] На **всех** вкладках Client: **логотип + «Телотрон»** (центр) + имя тренера (колонка слева) — единый `TelotronAppShell`
- [x] Подпись **«Client»** в шапке **отсутствует**
- [x] Один тренер: имя без переключателя
- [x] Несколько тренеров: `TelotronClientTrainerPickerSheet`, **не** `<select>`
- [x] `TelotronAvatar` (инициалы) в колонке тренера
- [x] Смена тренера → `setActiveTrainerUserId` (store без смены контракта)
- [x] Pro shell **без регрессии** (`TelotronPublicHeader` + Pro)
- [x] `npm run test:ts` green; `build.client` **161**
- [ ] Приёмка дизайн: 360px (опционально)

---

## Вне scope

- Загрузка фото тренера (API + Pro профиль)
- Filament / Admin
- Дублирование имени тренера крупным блоком в body главной (если есть — убрать отдельным микро-тикетом)

---

## Ссылки

- Store: `resources/ts/shared/stores/client-active-trainer.ts`
- API: `GET /api/v1/me/linked-trainers` — §4.1 [api-http-контракт](../../../_telotron.ru/docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md)
- `TelotronPublicHeader.vue`, `TelotronAvatar.vue`

---

## Журнал

### 2026-05-31

- Тикет создан по согласованию с заказчиком: logo + имя тренера, sheet при нескольких тренерах, задел под аватар.

### 2026-06-09 · закрытие

- Реализация: `633ebfe` — `TelotronClientTrainerShellHeader`, picker sheet, `--header-h-client`.
- Удалён `route.meta.clientTrainerHeader`; acceptance-тесты `TelotronClientTrainerShellHeader.acceptance.test.ts`.
- Макет: тренер слева, бренд по центру (отличие от черновика «2 строки под logo» — согласовано в коде).
- Тикет → **`сделано/`**.
