# Бэклог (очередь)

Тикеты, которые **ещё не взяты** в работу. Статус в файле: `backlog` или `ready`.

Взял задачу → перенеси файл в [`../в-работе/`](../в-работе/).

## Приоритет пилота · T-066 (упрощение входа Pro)

| ID | Статус | Фокус |
|----|--------|-------|
| [T-066](T-066-упрощение-входа-эпик.md) | `backlog` · **P1** | **Эпик** · gate директора ☑ 03.07 · gate юриста ☐ |
| [T-073](T-073-legal-смс-пилот-обновление-документов.md) | `backlog` · P1 | Юрдоки под СМС (до dev T-068) |
| [T-072](T-072-invite-ссылки-код-wo-link-public.md) | `backlog` | Код ссылки · `wo_link` / `public` |
| [T-068](T-068-упрощение-входа-sms-бот-напоминания.md) | `backlog` | Страница телефона · SMS · localStorage · профиль |
| [T-069](T-069-упрощение-входа-legal-одна-страница.md) | `backlog` | Рег. шаг 1 · 2 юрдока «Принять» |
| [T-071](T-071-упрощение-входа-passkey-опционально.md) | `backlog` | Рег. шаг 3 · Passkey **обяз.** · guard кабинета |
| [T-070](T-070-упрощение-входа-мастер-баннер.md) | `backlog` | Post-reg баннер мастера |
| [T-067](T-067-упрощение-входа-pwa-напоминания.md) | `backlog` | Post-reg PWA nudge |
| [T-075](T-075-упрощение-входа-legacy-cleanup.md) | `backlog` · P2 | Уборка legacy Pro auth **после** выката |
| [T-074](T-074-заключить-договор-sms-aero.md) | `backlog` | Договор SMS Aero · до **01.08** · не блокирует пилот |
| [T-064](T-064-auth-верификация-телефона-149-фз.md) | `backlog` | Закрыть вместе с T-068 |

**Client** в v1 эпика **не меняем**. [T-062](../отменено/T-062-client-регистрация-единый-шаг-согласий.md) — `cancelled`.

## Пилот · маркетинг и activation

| ID | Статус | Фокус |
|----|--------|-------|
| [T-048](T-048-спринт2-vk-пакет-запуска.md) | `backlog` · частично | VK пакет · хвост чеклист/календарь |
| [T-049](T-049-спринт2-личные-связи-реестр.md) | `backlog` · частично | Реестр ≥40 |
| [T-050](T-050-спринт2-воронка-метрики.md) | `backlog` | Воронка reg · метрики T-066 |
| [T-051](T-051-спринт2-qm-юр-тексты.md) | `backlog` | Q-M юр. тексты постов |
| [T-052](T-052-тз-crm-продвижение-пилот.md) | `backlog` | ТЗ CRM (Filament — позже) |
| [T-056](T-056-скрины-pro-vk-пилот.md) | `backlog` · частично | Альбом VK |
| [T-065](T-065-pro-onboarding-порядок-подготовка-клиент.md) | `backlog` · P1 | Порядок шагов мастера · стык T-070 |
| [T-076](T-076-pro-onboarding-устойчивость-ui-checklist-tour.md) | `backlog` · P2 | Onboarding checklist vs tour · action map |

## PO · продукт

| ID | Статус | Фокус |
|----|--------|-------|
| [T-004](T-004-оценка-привлечения-воронка.md) | `backlog` | Воронка привлечения |
| [T-005](T-005-матрица-функция-тариф.md) | `backlog` | Матрица функция × тариф |
| [T-024](T-024-reminders-одноразовый-лайтбокс.md) | `backlog` | Reminders лайтбокс |
| [T-025](T-025-ux-подталкивание-партнёрской-ссылки.md) | `backlog` | UX partner share |
| [T-058](T-058-public-landing-hero-визуал.md) | `backlog` | Public landing hero |

## Commerce · stage к 01.08

| ID | Статус | Фокус |
|----|--------|-------|
| [T-026](T-026-commerce-модуль-эпик.md) | `backlog` | **Эпик** → T-027…T-036 |
| [T-027](T-027-commerce-foundation-ledger.md) | `backlog` | Foundation |
| [T-028](T-028-commerce-тарифы-статусы-триал.md) | `backlog` | Тарифы |
| [T-029](T-029-commerce-платежи-yookassa.md) | `backlog` | YooKassa |
| [T-030](T-030-commerce-daily-debit-freeze.md) | `backlog` | Debit + freeze |
| [T-031](T-031-commerce-gating-api.md) | `backlog` | Gating + API |
| [T-032](T-032-commerce-купоны.md) | `backlog` | Купоны |
| [T-033](T-033-commerce-pro-ui.md) | `backlog` | Pro UI |
| [T-034](T-034-commerce-admin-filament.md) | `backlog` | Admin |
| [T-035](T-035-commerce-напоминания-триала.md) | `backlog` | Trial reminders |
| [T-036](T-036-commerce-stage-sign-off.md) | `backlog` | Stage sign-off |
| [T-047](T-047-commerce-public-тарифы.md) | `backlog` | Public `/tariffs` |

## Partner · stage к 01.08

| ID | Статус | Фокус |
|----|--------|-------|
| [T-037](T-037-partner-модуль-эпик.md) | `backlog` | **Эпик** → T-038…T-046 |
| [T-038](T-038-partner-foundation-config.md) | `backlog` | Foundation |
| [T-039](T-039-partner-кампании-ссылки.md) | `backlog` | Кампании |
| [T-040](T-040-partner-commission-topup.md) | `backlog` | L1/L2/L3 |
| [T-041](T-041-partner-http-api.md) | `backlog` | API |
| [T-042](T-042-partner-договор-legal.md) | `backlog` | Договор |
| [T-043](T-043-partner-вывод-admin.md) | `backlog` | Вывод |
| [T-044](T-044-partner-payout-providers.md) | `backlog` | Payout |
| [T-045](T-045-partner-pro-ui.md) | `backlog` | Pro UI |
| [T-046](T-046-partner-stage-sign-off.md) | `backlog` | Stage sign-off |

---

**Период 0 Go:** T-001…T-003 → [`../сделано/`](../сделано/). Полный индекс → [`../README.md`](../README.md).

*Обновлено 2026-07-03.*
