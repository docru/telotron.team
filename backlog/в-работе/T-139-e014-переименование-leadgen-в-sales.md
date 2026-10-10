# T-139 · E-014 · Переименование модуля LeadGen → Sales

| Поле | Значение |
|------|----------|
| **Статус** | `in_progress` · папка: **`в-работе/`** |
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
- [ ] `app/Modules/LeadGen` → `app/Modules/Sales`, раскладка по разделам: `Profile/`, `Tasks/`, `Operational/`, `Shared/`
- [ ] Модели и события с префиксом `Sales`: `SalesGrowthProfile`, `SalesTask`, `SalesBrief`, `SalesTaskCompleted`
- [ ] Сервисы, enum, job без префикса модуля: `BriefService`, `BriefComposer` (бывш. `MorningBriefCalculator`), `BriefFreshness`, `CandidatePreparer`, `RefreshBriefJob`, `TaskService`, `PlanGenerator`, `CrmSignalSync`, `Intensity`, `TaskSource`, `TaskType`, `TaskAction`, `BriefSource`, `Shared/PiiMasker`, `Shared/Clock`
- [ ] Слушатель `SyncLeadGenOnCrmEvent` → `Tasks/Listeners/SyncTasksOnCrmEvent`; регистрация в `AppServiceProvider`
- [ ] Слово «Morning» нигде в коде Sales не осталось
- [ ] `README.md` модуля перенесён и обновлён

### База данных
- [ ] Таблицы: `leadgen_growth_profiles` → `sales_growth_profiles`, `leadgen_tasks` → `sales_tasks`, `leadgen_morning_briefs` → `sales_briefs`
- [ ] Флаг пилота: `trainer_profiles.leadgen_pilot` → `trainer_profiles.sales_pilot`
- [ ] Способ: если миграции I-001 ещё не применялись ни на одном общем стенде — правим исходные миграции (`t115_…`, `t136_…`) и делаем `migrate:fresh` локально; иначе — одна миграция переименования. Решение записать в журнал тикета

### CRM и страница заявок (не Sales)
- [ ] Настройки страницы заявок и отладочного UI CRM уезжают из `config/leadgen.php` в `config/crm.php`: `pro_ui_enabled`, `reserved_nicks`, `defaults.*` (тексты «спасибо», вопросы квиза)
- [ ] Env: `LEADGEN_PRO_CRM_UI` → `CRM_PRO_UI` (`.env.example`, layout Pro `data-…`, `resources/ts/shared/leadgen-pro-crm-ui.ts` → `crm-pro-ui.ts`)
- [ ] `Crm\Services\CrmLeadGenReadService` → `CrmContactReadService` (CRM не знает имени потребителя)
- [ ] Тест `LeadgenProCrmApiTest` → `CrmProUiApiTest` (или близкое имя по содержанию)
- [ ] `inbound_touch_channels` — решить при переносе: это знание CRM о касаниях, логично `crm.inbound_touch_channels`; Sales читает его через сервис CRM или конфиг

### Конфиг, сценарии, промпты Sales
- [ ] `config/leadgen.php` → `config/sales.php`; ключи брифа — `sales.operational.brief.*`; `default_timezone` — `sales.default_timezone`
- [ ] Env: `LEADGEN_BRIEF_*` → `SALES_BRIEF_*`
- [ ] Сценарий `leadgen.morning_brief` → `sales.operational.brief_compose`; `prompt_version` → `sales.operational.brief_compose.v1`
- [ ] Файлы промпта: `resources/ai/leadgen/morning_brief.v1.*` → `resources/ai/sales/operational.brief_compose.v1.*`
- [ ] Лимит ИИ в сутки считает `ai_runs` по новому сценарию (старые записи `leadgen.morning_brief` в журнале не мигрируем)

### Консоль и крон
- [ ] `leadgen:brief-due` → `sales:operational-brief-due` (класс команды, `routes/schedule.php`)

### API и Filament
- [ ] `/api/v1/me/leadgen/…` → `/api/v1/me/sales/…`; имена маршрутов `api.v1.me.sales.*`
- [ ] Контроллеры `Api/V1/LeadGen/MeLeadGen*Controller` → `Api/V1/Sales/MeSales*Controller`; `RequiresLeadGenPilot` → `RequiresSalesPilot`
- [ ] `/api/v1/me`: поле `trainer_profile.leadgen_pilot` → `sales_pilot`
- [ ] Filament: галочка «Пилот продаж» в `TrainerProfileResource`
- [ ] `docs/Техдок/01-канон-mvp/api-http-контракт-mvp.md` — пути и поле флага

### Фронтенд Pro
- [ ] `resources/ts/shared/leadgen/` → `shared/sales/` (вкл. тест), `widgets/leadgen/LeadGenBriefCard.vue` → `widgets/sales/SalesBriefCard.vue`
- [ ] Страницы `WorkspaceLeadGenPage` / `WorkspaceLeadGenProfilePage` → `WorkspaceSalesPage` / `WorkspaceSalesProfilePage`
- [ ] Маршруты Pro: `/leadgen` → `/sales`, `/leadgen/profile` → `/sales/profile`; имена `workspace-sales`, `workspace-sales-profile`; `navKey: 'sales'`
- [ ] `auth-session.ts`, `workspace-nav.ts`, `WorkspaceCabinetPage.vue` — флаг `sales_pilot`
- [ ] Надпись в меню остаётся «Поиск клиентов» (смена — решение PO)
- [ ] Поднять `build.pro` в `config/version.php`

### Тесты и проверка
- [ ] Тесты переименованы (`tests/Feature/Api/Sales*`, `tests/Unit/Modules/Sales/*`), поведение тех же сценариев
- [ ] Зелёные: `php artisan test`, `npm run test:ts`, `npx tsc --noEmit`, `npm run build` (всё через `docker compose exec -u sail -T laravel.test …`)
- [ ] `rg -i 'leadgen|lead_gen|morning_?brief' app config routes resources database tests` — пусто, кроме исходных имён файлов миграций, если их решили не трогать
- [ ] Ручная проверка Pro: раздел открывается, бриф считается, «сделано» работает, CRM и страница заявок без изменений

### Документы
- [ ] `app/Modules/README.md`, `app/Modules/Ai/README.md` — без LeadGen
- [ ] ADR-011: запись в журнал «код переименован (T-139)»

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

### 2026-10-10

- Заведён архитектором по решению директора: модуль помощника продаж — **Sales**, CRM — соседний модуль. Найдено при нарезке: `config/leadgen.php` смешивает настройки страницы заявок/CRM и брифа — разносим в `config/crm.php` и `config/sales.php`.
