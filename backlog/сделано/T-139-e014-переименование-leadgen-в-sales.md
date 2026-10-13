# T-139 · E-014 · Переименование модуля LeadGen → Sales

| Поле | Значение |
|------|----------|
| **Статус** | `done` · папка: **`сделано/`** |
| **Эпик** | [E-014](../эпики/E-014-ии-роп.md) · этап 1 (волна 3) · затрагивает код пилота [E-010](../эпики/E-010-ии-консультант-продаж.md) |
| **Приоритет** | **P1** — до слияния ветки `initiative/i-001-modul-prodazh` в `main` и до любого кода волн 4–6 |
| **Спринт** | — |
| **Роль** | dev |
| **Ветка** | `initiative/i-001-modul-prodazh` (весь код LeadGen есть только там; **не** в `main`) |
| **Создан** | 2026-10-10 |
| **Зависит от** | [глоссарий Sales](../../../_telotron.ru/docs/Техдок/03-модули/sales-глоссарий-и-нейминг.md) §4–§6 · [дополнение 1 к ADR-011](../../../_telotron.ru/docs/Техдок/00-мета/архитектурные-решения/ADR-011-leadgen-утренний-бриф.md) |
| **Блокирует** | первые тикеты E-014 волны 4 |

> При взятии в работу: перенести файл в **`в-работе/`**, статус `in_progress`.  
> По завершении: **`сделано/`**, `done`.

## Контекст

Модуль помощника продаж переименован в каноне: **Sales** вместо LeadGen (LeadGen — только часть продаж). CRM остаётся соседним модулем `Crm`. Внутри Sales — разделы по слоям (`Operational/`, `Strategic/`, …).

Весь код I-001 (CRM, страница заявок, LeadGen) пока только в ветке инициативы: в `main` и на проде его нет, установок PWA не было. Поэтому переименовываем **без переходного периода**: старые URL, имена таблиц и ключи конфига не сохраняем.

Поведение не меняется. Это чистое переименование и раскладка по папкам.

## Критерии готовности

### Модуль и классы (карта — глоссарий §5)
- [x] `app/Modules/LeadGen` → `app/Modules/Sales`, раскладка по разделам: `Profile/`, `Tasks/`, `Operational/`, `Shared/`
- [x] Модели и события с префиксом `Sales`: `SalesGrowthProfile`, `SalesTask`, `SalesBrief`, `SalesTaskCompleted`
- [x] Сервисы, enum, job без префикса модуля: `BriefService`, `BriefComposer` (бывш. `MorningBriefCalculator`), `BriefFreshness`, `CandidatePreparer`, `RefreshBriefJob`, `TaskService`, `PlanGenerator`, `CrmSignalSync`, `Intensity`, `TaskSource`, `TaskType`, `TaskAction`, `BriefSource`, `Shared/PiiMasker`, `Shared/Clock`
- [x] Слушатель `SyncLeadGenOnCrmEvent` → `Tasks/Listeners/SyncTasksOnCrmEvent`; регистрация в `AppServiceProvider`
- [x] Слово «Morning» нигде в коде Sales не осталось
- [x] `README.md` модуля перенесён и обновлён

### База данных
- [x] Таблицы: `leadgen_growth_profiles` → `sales_growth_profiles`, `leadgen_tasks` → `sales_tasks`, `leadgen_morning_briefs` → `sales_briefs`
- [x] Флаг пилота: `trainer_profiles.leadgen_pilot` → `trainer_profiles.sales_pilot`
- [x] Способ: исходные миграции t115/t136 правятся на новые имена; плюс миграция переименования `t139` для локальных стендов, где старые таблицы уже есть (см. журнал)

### CRM и страница заявок (не Sales)
- [x] Настройки страницы заявок и отладочного UI CRM уезжают из `config/leadgen.php` в `config/crm.php`: `pro_ui_enabled`, `reserved_nicks`, `defaults.*` (тексты «спасибо», вопросы квиза)
- [x] Env: `LEADGEN_PRO_CRM_UI` → `CRM_PRO_UI` (`.env.example`, layout Pro `data-…`, `resources/ts/shared/leadgen-pro-crm-ui.ts` → `crm-pro-ui.ts`)
- [x] `Crm\Services\CrmLeadGenReadService` → `CrmContactReadService` (CRM не знает имени потребителя)
- [x] Тест `LeadgenProCrmApiTest` → `CrmProUiApiTest` (или близкое имя по содержанию)
- [x] `inbound_touch_channels` — в `crm.inbound_touch_channels`; Sales читает через `config('crm.inbound_touch_channels')`

### Конфиг, сценарии, промпты Sales
- [x] `config/leadgen.php` → `config/sales.php`; ключи брифа — `sales.operational.brief.*`; `default_timezone` — `sales.default_timezone`
- [x] Env: `LEADGEN_BRIEF_*` → `SALES_BRIEF_*`
- [x] Сценарий `leadgen.morning_brief` → `sales.operational.brief_compose`; `prompt_version` → `sales.operational.brief_compose.v1`
- [x] Файлы промпта: `resources/ai/leadgen/morning_brief.v1.*` → `resources/ai/sales/operational.brief_compose.v1.*`
- [x] Лимит ИИ в сутки считает `ai_runs` по новому сценарию (старые записи `leadgen.morning_brief` в журнале не мигрируем)

### Консоль и крон
- [x] `leadgen:brief-due` → `sales:operational-brief-due` (класс команды, `routes/schedule.php`)

### API и Filament
- [x] `/api/v1/me/leadgen/…` → `/api/v1/me/sales/…`; имена маршрутов `api.v1.me.sales.*`
- [x] Контроллеры `Api/V1/LeadGen/MeLeadGen*Controller` → `Api/V1/Sales/MeSales*Controller`; `RequiresLeadGenPilot` → `RequiresSalesPilot`
- [x] `/api/v1/me`: поле `trainer_profile.leadgen_pilot` → `sales_pilot`
- [x] Filament: галочка «Пилот продаж» в `TrainerProfileResource`
- [x] `docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md` — пути и поле флага

### Фронтенд Pro
- [x] `resources/ts/shared/leadgen/` → `shared/sales/` (вкл. тест), `widgets/leadgen/LeadGenBriefCard.vue` → `widgets/sales/SalesBriefCard.vue`
- [x] Страницы `WorkspaceLeadGenPage` / `WorkspaceLeadGenProfilePage` → `WorkspaceSalesPage` / `WorkspaceSalesProfilePage`
- [x] Маршруты Pro: `/leadgen` → `/sales`, `/leadgen/profile` → `/sales/profile`; имена `workspace-sales`, `workspace-sales-profile`; `navKey: 'sales'`
- [x] `auth-session.ts`, `workspace-nav.ts`, `WorkspaceCabinetPage.vue` — флаг `sales_pilot`
- [x] Надпись в меню остаётся «Поиск клиентов» (смена — решение PO)
- [x] Поднять `build.pro` в `config/version.php` (293)

### Тесты и проверка
- [x] Тесты переименованы (`tests/Feature/Api/Sales*`, `tests/Unit/Modules/Sales/*`), поведение тех же сценариев
- [x] Зелёные: `php artisan test` (688), `npm run test:ts` (486), `npm run build`; `tsc --noEmit` — прежние ошибки вне Sales
- [x] `rg -i 'leadgen|lead_gen|morning_?brief' app config routes resources database tests` — пусто, кроме имён файлов миграций t115/t136/t139 и ссылки на ADR-011 в README модуля
- [x] Проверка сценариев API-тестами (профиль, бриф, сделано, CRM UI)

### Документы
- [x] `app/Modules/README.md`, `app/Modules/Ai/README.md` — без LeadGen
- [x] ADR-011: запись в журнал «код переименован (T-139)»

## Вне тикета

- Новые сущности волн 4–6 (`sales_strategy_runs`, `sales_trainer_signals`, `sales_drafts`, …)
- Переименование CRM (`crm_*`, `Crm*` остаются)
- Смена надписи «Поиск клиентов» в интерфейсе
- Исторические документы команды (отчёты T-136/T-137/T-138, eval-пакет T-138) — не переписываем

## Ссылки

- [Глоссарий и правила именования Sales](../../../_telotron.ru/docs/Техдок/03-модули/sales-глоссарий-и-нейминг.md) — §5 карта «сейчас → цель», §6 правила переименования
- [ADR-011](../../../_telotron.ru/docs/Техдок/00-мета/архитектурные-решения/ADR-011-leadgen-утренний-бриф.md) · дополнение 1
- [Ответ архитектора на запрос волны 3](../../11-AI-инженер/Работа/e-014-zapros-arhitektoru-volna-3.md)

## Журнал (вся переписка — здесь)

### 2026-10-10 (реализация)

- Модуль `LeadGen` → `Sales` (`Profile/`, `Tasks/`, `Operational/`, `Shared/`).
- БД: исходные миграции t115/t136 создают `sales_*` / `sales_pilot`; для локальных стендов, где уже накатили старые имена, — `2026_10_10_100000_t139_rename_leadgen_to_sales` (rename if old exists). Общего стенда с I-001 не было.
- `config/leadgen.php` разобран: CRM UI → `config/crm.php` (`CRM_PRO_UI`, `inbound_touch_channels`); бриф → `config/sales.php` (`SALES_BRIEF_*`).
- API `/me/sales/…`, Filament «Пилот продаж», фронт `/sales`, `build.pro` = 293.
- Тесты: PHP 688, Vitest 486, `npm run build` OK.

### 2026-10-10

- Заведён архитектором по решению директора: модуль помощника продаж — **Sales**, CRM — соседний модуль. Найдено при нарезке: `config/leadgen.php` смешивает настройки страницы заявок/CRM и брифа — разносим в `config/crm.php` и `config/sales.php`.
