"""Проверочный набор тренеров для diagnose / propose / decompose / review v1.

Запуск: python3 trainers_set.py → trainers-v1.json
"""

from __future__ import annotations

import json
from pathlib import Path

from knowledge_stub import (
    ALLOWED_TYPES,
    DEFAULT_TASKS_LIGHT_REACTIVATE,
    cards_for,
    default_tasks,
)


def profile(**kw) -> dict:
    base = {
        "specialization": "персональные тренировки",
        "services": ["workouts"],
        "goal_clients_per_month": 4,
        "old_base_size": "10_30",
        "channels": ["tg"],
        "hours_per_week": "2_5",
        "urgency": "normal",
        "offer": "free_trial",
        "offer_note": None,
        "about": "Тренер, есть бывшие клиенты.",
        "intensity": "moderate",
    }
    base.update(kw)
    return base


def case(
    cid: str,
    desc: str,
    *,
    tags: list[str],
    agents: list[str],
    profile_data: dict,
    diagnose_input: dict | None = None,
    expect_diagnose: dict | None = None,
    propose_input: dict | None = None,
    expect_propose: dict | None = None,
    decompose_input: dict | None = None,
    expect_decompose: dict | None = None,
    review_input: dict | None = None,
    expect_review: dict | None = None,
) -> dict:
    out: dict = {
        "id": cid,
        "description": desc,
        "tags": tags,
        "agents": agents,
        "profile": profile_data,
    }
    if diagnose_input is not None:
        out["diagnose"] = {"input": diagnose_input, "expect": expect_diagnose or {}}
    if propose_input is not None:
        out["propose"] = {"input": propose_input, "expect": expect_propose or {}}
    if decompose_input is not None:
        out["decompose"] = {"input": decompose_input, "expect": expect_decompose or {}}
    if review_input is not None:
        out["review"] = {"input": review_input, "expect": expect_review or {}}
    return out


PROFILE_ALLOWED = {
    "services": ["workouts", "nutrition", "complex"],
    "old_base_size": ["none", "lt10", "10_30", "gt30"],
    "channels": ["vk", "ok", "tg", "max"],
    "hours_per_week": ["lt2", "2_5", "gt5"],
    "urgency": ["urgent", "normal", "no_rush"],
    "offer": ["free_trial", "paid_trial", "consultation"],
}


def diag_base(mode: str, prof: dict, **extra) -> dict:
    d = {
        "mode": mode,
        "final_round": False,
        "round": 0,
        "profile": prof,
        "profile_allowed": PROFILE_ALLOWED,
        "funnel": {"new_contacts_7d": 0, "in_progress": 0, "clients_new_7d": 0},
        "facts": None,
        "clarification_answers": [],
        "observations_active": [],
        "observations_dismissed": [],
        "mismatch_flags": [],
        "current_strategy": None,
        "week_plan_performance": None,
    }
    d.update(extra)
    flags = d["mismatch_flags"]
    askable = [f for f in PROFILE_ALLOWED if prof.get(f) in (None, []) or f in flags]
    d["askable_fields"] = askable
    d["profile_allowed"] = {f: PROFILE_ALLOWED[f] for f in askable}
    return d


CASES: list[dict] = []

# --- t01: онбординг, база не тронута ---
p1 = profile(
    old_base_size="10_30",
    about="Было человек пятнадцать, давно никому не писала.",
    intensity="light",
    hours_per_week="lt2",
)
CASES.append(
    case(
        "t01_onboarding_base_untouched",
        "Онбординг: база 10–30, касаний нет → bottleneck base_untouched",
        tags=["onboarding", "base_untouched"],
        agents=["diagnose", "propose"],
        profile_data=p1,
        diagnose_input=diag_base(
            "strategy_run",
            p1,
            funnel={"new_contacts_7d": 0, "in_progress": 0, "clients_new_7d": 0, "legacy_base_contacts": 2, "legacy_touches_30d": 0},
        ),
        expect_diagnose={
            "bottleneck_any": ["base_untouched"],
            "data_quality_any": ["sufficient", "partial"],
            "questions_max": 3,
            "no_client_zero_phrase": True,
        },
        propose_input={
            "profile": p1,
            "diagnosis": {
                "data_quality": "partial",
                "strengths": ["Есть база людей, которые вас уже знают."],
                "bottlenecks": [{"code": "base_untouched", "text": "Базу можно снова включить в работу."}],
                "hypotheses": ["Давно не было повода написать."],
                "opportunities": ["Несколько личных сообщений бывшим."],
                "skill_gaps": [],
                "assumptions": ["Готовы писать лично."],
                "questions": [],
                "observations": [],
                "profile_change_proposals": [],
            },
            "knowledge_cards": cards_for("reactivate-old-base", "follow-up-routine", "offer-and-booking"),
            "past_strategies": [],
            "active_observations": [],
        },
        expect_propose={
            "strategies_min": 2,
            "strategies_max": 3,
            "recommended_cards_any": ["reactivate-old-base"],
            "forbidden_card_keys": [],
        },
    )
)

# --- t02: большая база, moderate ---
p2 = profile(old_base_size="gt30", hours_per_week="2_5", intensity="moderate", channels=["vk"])
CASES.append(
    case(
        "t02_large_base_vk",
        "Большая база, ВК — реактивация уместна",
        tags=["onboarding", "base_untouched"],
        agents=["diagnose", "propose"],
        profile_data=p2,
        diagnose_input=diag_base(
            "strategy_run",
            p2,
            funnel={"new_contacts_7d": 1, "in_progress": 1, "clients_new_7d": 0, "legacy_base_contacts": 40, "legacy_touches_30d": 1},
        ),
        expect_diagnose={"bottleneck_any": ["base_untouched", "no_follow_up"], "no_client_zero_phrase": True},
        propose_input={
            "profile": p2,
            "diagnosis": {
                "data_quality": "sufficient",
                "strengths": ["Большая база бывших клиентов.", "Есть канал ВК."],
                "bottlenecks": [{"code": "base_untouched", "text": "База почти не в работе."}],
                "hypotheses": [],
                "opportunities": ["Системные касания по базе."],
                "skill_gaps": [],
                "assumptions": [],
                "questions": [],
                "observations": [],
                "profile_change_proposals": [],
            },
            "knowledge_cards": cards_for("reactivate-old-base", "steady-content", "follow-up-routine"),
            "past_strategies": [],
            "active_observations": [],
        },
        expect_propose={"strategies_min": 2, "recommended_cards_any": ["reactivate-old-base"]},
    )
)

# --- t03: нет базы ---
p3 = profile(old_base_size="none", about="Только сертифицировалась, клиентов не было.", intensity="moderate")
CASES.append(
    case(
        "t03_no_base_warm_circle",
        "Нет базы → не предлагать reactivate-old-base",
        tags=["onboarding", "no_base"],
        agents=["diagnose", "propose"],
        profile_data=p3,
        diagnose_input=diag_base("strategy_run", p3),
        expect_diagnose={"bottleneck_any": ["no_base", "low_visibility"], "no_client_zero_phrase": True},
        propose_input={
            "profile": p3,
            "diagnosis": {
                "data_quality": "sufficient",
                "strengths": ["Есть канал и готовность начать."],
                "bottlenecks": [{"code": "no_base", "text": "Своей базы пока нет — старт с круга знакомых."}],
                "hypotheses": [],
                "opportunities": ["Тёплый круг и аккуратный профиль."],
                "skill_gaps": [],
                "assumptions": [],
                "questions": [],
                "observations": [],
                "profile_change_proposals": [],
            },
            "knowledge_cards": cards_for("warm-circle-start", "steady-content", "offer-and-booking", "local-partners"),
            "past_strategies": [],
            "active_observations": [],
        },
        expect_propose={
            "strategies_min": 2,
            "recommended_cards_any": ["warm-circle-start", "steady-content"],
            "forbidden_card_keys": ["reactivate-old-base"],
        },
    )
)

# --- t04: lt10 + low visibility ---
p4 = profile(old_base_size="lt10", channels=["tg"], about="Мало кого знаю в теме.")
CASES.append(
    case(
        "t04_small_base_visibility",
        "Маленькая база / низкая видимость",
        tags=["onboarding", "low_visibility"],
        agents=["diagnose", "propose"],
        profile_data=p4,
        diagnose_input=diag_base("strategy_run", p4),
        expect_diagnose={"bottleneck_any": ["no_base", "low_visibility"]},
        propose_input={
            "profile": p4,
            "diagnosis": {
                "data_quality": "partial",
                "strengths": ["Есть Telegram."],
                "bottlenecks": [{"code": "low_visibility", "text": "О вас пока мало кто знает."}],
                "hypotheses": [],
                "opportunities": ["Профиль и короткие публикации."],
                "skill_gaps": [],
                "assumptions": ["База совсем небольшая."],
                "questions": [],
                "observations": [],
                "profile_change_proposals": [],
            },
            "knowledge_cards": cards_for("warm-circle-start", "steady-content"),
            "past_strategies": [],
            "active_observations": [],
        },
        expect_propose={"strategies_min": 2, "recommended_cards_any": ["warm-circle-start", "steady-content"]},
    )
)

# --- t05: weak offer ---
p5 = profile(offer="free_trial", offer_note=None, about="Не знаю, как сформулировать предложение.")
CASES.append(
    case(
        "t05_weak_offer",
        "Слабое предложение / запись",
        tags=["onboarding", "weak_offer"],
        agents=["diagnose", "propose"],
        profile_data=p5,
        diagnose_input=diag_base(
            "strategy_run",
            p5,
            funnel={"new_contacts_7d": 0, "in_progress": 2, "clients_new_7d": 0, "booking_page_leads_30d": 0},
        ),
        expect_diagnose={"bottleneck_any": ["weak_offer", "base_untouched", "no_follow_up"]},
        propose_input={
            "profile": p5,
            "diagnosis": {
                "data_quality": "sufficient",
                "strengths": ["Уже есть диалоги в работе."],
                "bottlenecks": [{"code": "weak_offer", "text": "Предложение и запись можно сделать понятнее."}],
                "hypotheses": [],
                "opportunities": ["Короткий оффер и ссылка на запись."],
                "skill_gaps": [],
                "assumptions": [],
                "questions": [],
                "observations": [],
                "profile_change_proposals": [],
            },
            "knowledge_cards": cards_for("offer-and-booking", "reactivate-old-base", "follow-up-routine"),
            "past_strategies": [],
            "active_observations": [],
        },
        expect_propose={"recommended_cards_any": ["offer-and-booking"]},
    )
)

# --- t06: weekly follow-up ---
p6 = profile(intensity="moderate")
CASES.append(
    case(
        "t06_weekly_follow_up",
        "Совещание: диалоги затухают — вопросы шире допустимы",
        tags=["weekly", "no_follow_up"],
        agents=["diagnose"],
        profile_data=p6,
        diagnose_input=diag_base(
            "weekly",
            p6,
            facts={
                "tasks_done": 3,
                "tasks_planned": 6,
                "dialogs_started": 1,
                "leads_new": 0,
                "clients_new": 0,
                "in_progress_stale": 8,
            },
            current_strategy={"name": "Вернуть бывших", "weeks_elapsed": 2},
            week_plan_performance={"done_ratio": 0.5, "skipped_types": ["strategy.follow_up"]},
        ),
        expect_diagnose={
            "bottleneck_any": ["no_follow_up", "low_conversion", "irregular_activity"],
            "questions_max": 3,
            "no_client_zero_phrase": True,
            "observations_topics_any": ["follow_up_gap", "plan_fit", "base_usage"],
        },
    )
)

# --- t07: load mismatch weekly ---
p7 = profile(hours_per_week="gt5", intensity="intense")
CASES.append(
    case(
        "t07_weekly_load_mismatch",
        "Заявлено gt5, факт выполнения как light — наблюдение load",
        tags=["weekly", "load"],
        agents=["diagnose"],
        profile_data=p7,
        diagnose_input=diag_base(
            "weekly",
            p7,
            facts={"tasks_done": 1, "tasks_planned": 8, "minutes_done": 40, "clients_new": 0},
            mismatch_flags=[],  # ещё нет 2 недель — правку не предлагать
            current_strategy={"name": "Контент", "weeks_elapsed": 1},
            week_plan_performance={"done_ratio": 0.12},
        ),
        expect_diagnose={
            "profile_change_empty": True,
            "observations_topics_any": ["load", "plan_fit", "irregular_activity"],
            "no_client_zero_phrase": True,
        },
    )
)

# --- t08: profile change allowed ---
p8 = profile(hours_per_week="gt5", intensity="intense")
CASES.append(
    case(
        "t08_profile_change_allowed",
        "mismatch_flags hours_per_week 2+ недель — можно proposal",
        tags=["weekly", "profile_change"],
        agents=["diagnose"],
        profile_data=p8,
        diagnose_input=diag_base(
            "weekly",
            p8,
            facts={"tasks_done": 2, "tasks_planned": 10, "minutes_done": 50, "clients_new": 1},
            mismatch_flags=["hours_per_week"],
            current_strategy={"name": "Контент", "weeks_elapsed": 3},
            week_plan_performance={"done_ratio": 0.2},
        ),
        expect_diagnose={
            "profile_change_fields_any": ["hours_per_week"],
            "no_client_zero_phrase": True,  # clients_new=1 — фраза «0» всё равно запрещена
        },
    )
)

# --- t09: profile change forbidden without flags ---
p9 = profile(hours_per_week="gt5")
CASES.append(
    case(
        "t09_profile_change_forbidden",
        "Без mismatch_flags proposals должны быть пусты (проверка кода отбросит)",
        tags=["weekly", "profile_change"],
        agents=["diagnose"],
        profile_data=p9,
        diagnose_input=diag_base(
            "weekly",
            p9,
            facts={"minutes_done": 30, "clients_new": 0},
            mismatch_flags=[],
            current_strategy={"name": "База", "weeks_elapsed": 4},
        ),
        expect_diagnose={"profile_change_empty": True, "no_client_zero_phrase": True},
    )
)

# --- t10: final_round ---
p10 = profile(old_base_size="10_30")
CASES.append(
    case(
        "t10_final_round_no_questions",
        "final_round=true → questions запрещены",
        tags=["onboarding", "final_round"],
        agents=["diagnose"],
        profile_data=p10,
        diagnose_input=diag_base("strategy_run", p10, final_round=True, round=1),
        expect_diagnose={"questions_forbidden": True, "questions_max": 0},
    )
)

# --- t24: онбординг, в анкете пусто urgency и channels → вопросы только про них ---
p24 = profile(old_base_size="10_30", urgency=None, channels=[])
CASES.append(
    case(
        "t24_onboarding_empty_fields",
        "Пустые поля анкеты: вопрос вида А только по askable_fields",
        tags=["onboarding", "questions"],
        agents=["diagnose"],
        profile_data=p24,
        diagnose_input=diag_base("strategy_run", p24),
        expect_diagnose={"question_fields_any": ["urgency", "channels"], "questions_max": 3},
    )
)

# --- t11: propose 2 strategies ok ---
p11 = profile(old_base_size="none", hours_per_week="lt2", intensity="light")
CASES.append(
    case(
        "t11_propose_two_ok",
        "Мало ресурсов — достаточно 2 стратегий, не натягивать третью",
        tags=["propose"],
        agents=["propose"],
        profile_data=p11,
        propose_input={
            "profile": p11,
            "diagnosis": {
                "data_quality": "sufficient",
                "strengths": ["Готовность начать с малого."],
                "bottlenecks": [{"code": "no_base", "text": "Базы нет."}],
                "hypotheses": [],
                "opportunities": ["Тёплый круг."],
                "skill_gaps": [],
                "assumptions": [],
                "questions": [],
                "observations": [],
                "profile_change_proposals": [],
            },
            "knowledge_cards": cards_for("warm-circle-start", "offer-and-booking"),
            "past_strategies": [],
            "active_observations": [],
        },
        expect_propose={"strategies_min": 2, "strategies_max": 3, "recommended_cards_any": ["warm-circle-start"]},
    )
)

# --- t12: ethics / no cold outreach ---
p12 = profile(old_base_size="none")
CASES.append(
    case(
        "t12_ethics_restriction",
        "Restriction ethics всегда во входе; стратегии без холодных рассылок",
        tags=["propose", "ethics"],
        agents=["propose"],
        profile_data=p12,
        propose_input={
            "profile": p12,
            "diagnosis": {
                "data_quality": "sufficient",
                "strengths": ["Есть канал."],
                "bottlenecks": [{"code": "no_base", "text": "Базы нет."}],
                "hypotheses": [],
                "opportunities": ["Знакомые и контент."],
                "skill_gaps": [],
                "assumptions": [],
                "questions": [],
                "observations": [],
                "profile_change_proposals": [],
            },
            "knowledge_cards": cards_for("warm-circle-start", "steady-content"),
            "past_strategies": [],
            "active_observations": [],
        },
        expect_propose={
            "strategies_min": 2,
            "must_not_contain": ["незнакомым", "холодн", "спам", "куплю базу", "парсинг"],
            "recommended_cards_any": ["warm-circle-start", "steady-content"],
        },
    )
)

# --- t13: decompose first_plan ---
p13 = profile(intensity="light", hours_per_week="lt2")
CASES.append(
    case(
        "t13_decompose_first_plan",
        "Первый план после выбора реактивации, light, cap 100",
        tags=["decompose", "first_plan"],
        agents=["decompose"],
        profile_data=p13,
        decompose_input={
            "phase": "first_plan",
            "strategy": {
                "name": "Вернуть бывших",
                "summary": "Письма бывшим клиентам.",
                "knowledge_card_keys": ["reactivate-old-base", "ethics-and-law"],
                "horizon_weeks": 6,
            },
            "profile": p13,
            "default_tasks": DEFAULT_TASKS_LIGHT_REACTIVATE,
            "allowed_types": ALLOWED_TYPES,
            "weekly_minutes_cap": 100,
            "milestones_existing": [],
            "previous_plan_performance": None,
            "monitor_recommendation": None,
        },
        expect_decompose={
            "items_min": 1,
            "items_max": 10,
            "minutes_cap": 100,
            "milestones_min": 1,
            "types_only_from": ALLOWED_TYPES,
            "must_not_contain": ["Марин", "+7"],
        },
    )
)

# --- t14: decompose weekly adjust ---
p14 = profile(intensity="moderate", hours_per_week="2_5")
CASES.append(
    case(
        "t14_decompose_weekly_adjust",
        "Недельный план при recommendation=adjust, cap 180",
        tags=["decompose", "weekly"],
        agents=["decompose"],
        profile_data=p14,
        decompose_input={
            "phase": "weekly",
            "strategy": {
                "name": "Вернуть бывших",
                "summary": "Письма бывшим.",
                "knowledge_card_keys": ["reactivate-old-base"],
                "horizon_weeks": 6,
            },
            "profile": p14,
            "default_tasks": [t for t in DEFAULT_TASKS_LIGHT_REACTIVATE if t["when"] == "every_week"],
            "allowed_types": ALLOWED_TYPES,
            "weekly_minutes_cap": 180,
            "milestones_existing": [{"position": 1, "title": "Первые сообщения", "status": "pending"}],
            "previous_plan_performance": {
                "done_ratio": 0.3,
                "skipped_types": ["strategy.follow_up"],
            },
            "monitor_recommendation": "adjust",
        },
        expect_decompose={
            "items_min": 1,
            "items_max": 10,
            "minutes_cap": 180,
            "milestones_min": 0,
            "types_only_from": ALLOWED_TYPES,
        },
    )
)

# --- t15: review on_track, 0 clients ---
p15 = profile()
CASES.append(
    case(
        "t15_review_on_track_zero_clients",
        "Задачи делаются, диалоги есть, clients_new=0 → не failed, не писать про 0 клиентов",
        tags=["review"],
        agents=["review"],
        profile_data=p15,
        review_input={
            "strategy": {
                "name": "Вернуть бывших",
                "summary": "База",
                "started_on": "2026-09-01",
                "horizon_ends_on": "2026-10-13",
                "knowledge_card_keys": ["reactivate-old-base"],
            },
            "milestones": [
                {
                    "position": 1,
                    "title": "Первые сообщения",
                    "due_on": "2026-09-15",
                    "status": "done",
                    "success_criteria": [{"metric": "dialogs_started", "min": 2}],
                    "progress": {"dialogs_started": 3},
                }
            ],
            "facts": {
                "tasks_done": 5,
                "tasks_planned": 6,
                "dialogs_started": 3,
                "leads_new": 1,
                "clients_new": 0,
            },
            "plan_performance": {"done_ratio": 0.83},
            "weeks_elapsed": 2,
        },
        expect_review={
            "status_any": ["on_track", "behind"],
            "recommendation_any": ["continue", "adjust"],
            "forbid_status": ["failed"],
            "no_client_zero_phrase": True,
        },
    )
)

# --- t16: review not failed on clients only ---
p16 = profile()
CASES.append(
    case(
        "t16_review_not_failed_on_clients",
        "Выполнение задач высокое, клиентов 0 — failed запрещён",
        tags=["review"],
        agents=["review"],
        profile_data=p16,
        review_input={
            "strategy": {
                "name": "Контент",
                "summary": "Посты",
                "started_on": "2026-08-01",
                "horizon_ends_on": "2026-09-12",
                "knowledge_card_keys": ["steady-content"],
            },
            "milestones": [
                {
                    "position": 2,
                    "title": "Регулярность",
                    "due_on": "2026-09-01",
                    "status": "done",
                    "success_criteria": [{"metric": "tasks_done", "min": 8}],
                    "progress": {"tasks_done": 10},
                }
            ],
            "facts": {
                "tasks_done": 10,
                "tasks_planned": 10,
                "dialogs_started": 2,
                "leads_new": 0,
                "clients_new": 0,
            },
            "plan_performance": {"done_ratio": 1.0},
            "weeks_elapsed": 5,
        },
        expect_review={
            "forbid_status": ["failed"],
            "recommendation_not": ["change_strategy"],
            "no_client_zero_phrase": True,
        },
    )
)


# --- t17: decompose first_plan intense, две карточки, cap 360 ---
p17 = profile(intensity="intense", hours_per_week="gt5", urgency="urgent", old_base_size="none", channels=["vk"])
CASES.append(
    case(
        "t17_decompose_intense_two_cards",
        "Первый план intense: тёплый круг + предложение, cap 360, вехи обязательны",
        tags=["decompose", "first_plan"],
        agents=["decompose"],
        profile_data=p17,
        decompose_input={
            "phase": "first_plan",
            "strategy": {
                "name": "Старт с тёплого круга",
                "summary": "Знакомые, профиль, понятное предложение.",
                "knowledge_card_keys": ["warm-circle-start", "offer-and-booking", "ethics-and-law"],
                "horizon_weeks": 6,
            },
            "profile": p17,
            "default_tasks": default_tasks("warm-circle-start", "intense") + default_tasks("offer-and-booking", "intense"),
            "allowed_types": ALLOWED_TYPES,
            "weekly_minutes_cap": 360,
            "milestones_existing": [],
            "previous_plan_performance": None,
            "monitor_recommendation": None,
        },
        expect_decompose={
            "items_min": 3,
            "items_max": 10,
            "minutes_cap": 360,
            "milestones_min": 1,
            "types_only_from": ALLOWED_TYPES,
        },
    )
)

# --- t18: decompose weekly continue, moderate, план выполнен ---
p18 = profile(intensity="moderate", hours_per_week="2_5", channels=["tg"])
CASES.append(
    case(
        "t18_decompose_weekly_continue",
        "Недельный план при continue: контент, moderate, cap 180, без новых вех",
        tags=["decompose", "weekly"],
        agents=["decompose"],
        profile_data=p18,
        decompose_input={
            "phase": "weekly",
            "strategy": {
                "name": "Регулярно в соцсети",
                "summary": "Посты и истории по графику.",
                "knowledge_card_keys": ["steady-content", "ethics-and-law"],
                "horizon_weeks": 6,
            },
            "profile": p18,
            "default_tasks": default_tasks("steady-content", "moderate", when="every_week"),
            "allowed_types": ALLOWED_TYPES,
            "weekly_minutes_cap": 180,
            "milestones_existing": [{"position": 1, "title": "Публикации пошли", "status": "done"}],
            "previous_plan_performance": {"done_ratio": 0.9, "skipped_types": []},
            "monitor_recommendation": "continue",
        },
        expect_decompose={
            "items_min": 1,
            "items_max": 10,
            "minutes_cap": 180,
            "milestones_max": 0,
            "types_only_from": ALLOWED_TYPES,
        },
    )
)

# --- t19: decompose light, урезать до cap ---
p19 = profile(intensity="light", hours_per_week="lt2", old_base_size="gt30")
CASES.append(
    case(
        "t19_decompose_light_cap",
        "Light с двумя карточками: набор шире потолка — уложиться в 100 минут",
        tags=["decompose", "first_plan", "cap"],
        agents=["decompose"],
        profile_data=p19,
        decompose_input={
            "phase": "first_plan",
            "strategy": {
                "name": "Вернуть бывших и доводить разговоры",
                "summary": "Старая база и напоминания.",
                "knowledge_card_keys": ["reactivate-old-base", "follow-up-routine", "ethics-and-law"],
                "horizon_weeks": 6,
            },
            "profile": p19,
            "default_tasks": default_tasks("reactivate-old-base", "light") + default_tasks("follow-up-routine", "light"),
            "allowed_types": ALLOWED_TYPES,
            "weekly_minutes_cap": 100,
            "milestones_existing": [],
            "previous_plan_performance": None,
            "monitor_recommendation": None,
        },
        expect_decompose={
            "items_min": 1,
            "items_max": 10,
            "minutes_cap": 100,
            "milestones_min": 1,
            "types_only_from": ALLOWED_TYPES,
        },
    )
)


def review_input(strategy_name: str, weeks: int, facts: dict, done_ratio: float, milestones: list[dict]) -> dict:
    return {
        "strategy": {
            "name": strategy_name,
            "summary": strategy_name,
            "started_on": "2026-09-01",
            "horizon_ends_on": "2026-10-13",
            "knowledge_card_keys": ["reactivate-old-base"],
        },
        "milestones": milestones,
        "facts": facts,
        "plan_performance": {"done_ratio": done_ratio},
        "weeks_elapsed": weeks,
    }


# --- t20: review too_early ---
CASES.append(
    case(
        "t20_review_too_early",
        "Первая неделя, данных мало → too_early, без смены стратегии",
        tags=["review"],
        agents=["review"],
        profile_data=profile(),
        review_input=review_input(
            "Вернуть бывших",
            0,
            {"tasks_done": 1, "tasks_planned": 4, "dialogs_started": 0, "leads_new": 0, "clients_new": 0},
            0.25,
            [{"position": 1, "title": "Первые сообщения", "due_on": "2026-09-15", "status": "pending",
              "success_criteria": [{"metric": "contacts_added", "min": 5}], "progress": {"contacts_added": 2}}],
        ),
        expect_review={
            "status_any": ["too_early"],
            "recommendation_not": ["change_strategy"],
            "no_client_zero_phrase": True,
        },
    )
)

# --- t21: review behind — задачи не делаются ---
CASES.append(
    case(
        "t21_review_behind_low_done",
        "Задачи почти не делались 3 недели → behind + adjust, а не «стратегия плохая»",
        tags=["review"],
        agents=["review"],
        profile_data=profile(),
        review_input=review_input(
            "Вернуть бывших",
            3,
            {"tasks_done": 2, "tasks_planned": 15, "dialogs_started": 0, "leads_new": 0, "clients_new": 0},
            0.13,
            [{"position": 1, "title": "Первые сообщения", "due_on": "2026-09-15", "status": "missed",
              "success_criteria": [{"metric": "tasks_done", "min": 4}], "progress": {"tasks_done": 2}}],
        ),
        expect_review={
            "status_any": ["behind"],
            "recommendation_any": ["adjust"],
            "no_client_zero_phrase": True,
        },
    )
)

# --- t22: review — задачи делаются, промежуточных результатов нет 5 недель ---
CASES.append(
    case(
        "t22_review_done_no_results",
        "Выполнение высокое, но диалогов и заявок нет 5 недель → смена допустима",
        tags=["review"],
        agents=["review"],
        profile_data=profile(),
        review_input=review_input(
            "Вернуть бывших",
            5,
            {"tasks_done": 22, "tasks_planned": 24, "dialogs_started": 0, "leads_new": 0, "clients_new": 0},
            0.92,
            [{"position": 2, "title": "Пошли ответы", "due_on": "2026-09-29", "status": "missed",
              "success_criteria": [{"metric": "dialogs_started", "min": 4}], "progress": {"dialogs_started": 0}}],
        ),
        expect_review={
            "status_any": ["behind", "failed"],
            "recommendation_any": ["adjust", "change_strategy"],
            "no_client_zero_phrase": True,
        },
    )
)

# --- t23: review — есть клиенты, можно упомянуть ---
CASES.append(
    case(
        "t23_review_with_clients",
        "Есть 2 новых клиента — упоминание допустимо, статус on_track",
        tags=["review"],
        agents=["review"],
        profile_data=profile(),
        review_input=review_input(
            "Вернуть бывших",
            3,
            {"tasks_done": 12, "tasks_planned": 14, "dialogs_started": 6, "leads_new": 2, "clients_new": 2},
            0.86,
            [{"position": 2, "title": "Пошли ответы", "due_on": "2026-09-29", "status": "done",
              "success_criteria": [{"metric": "dialogs_started", "min": 4}], "progress": {"dialogs_started": 6}}],
        ),
        expect_review={
            "status_any": ["on_track"],
            "recommendation_any": ["continue"],
        },
    )
)


def main() -> None:
    out = Path(__file__).with_name("trainers-v1.json")
    out.write_text(json.dumps(CASES, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {len(CASES)} trainers → {out.name}")


if __name__ == "__main__":
    main()
