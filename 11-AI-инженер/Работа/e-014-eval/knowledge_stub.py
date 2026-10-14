"""Урезанные карточки методик для входа Стратега/Декомпозера в проверочном наборе."""

from __future__ import annotations

from pathlib import Path

import yaml

CARDS_DIR = Path(__file__).resolve().parent.parent / "e-014-kartochki"


def default_tasks(key: str, intensity: str, when: str | None = None) -> list[dict]:
    """default_tasks из черновика карточки, частота — в формате входа Декомпозера."""
    text = (CARDS_DIR / f"{key}.md").read_text(encoding="utf-8")
    card = yaml.safe_load(text.split("---", 2)[1])
    out = []
    for t in card["default_tasks"][intensity]:
        if when and t["when"] != when:
            continue
        freq = t["frequency"]
        if freq == "once":
            f = {"kind": "once", "times_per_week": None}
        elif freq == "daily":
            f = {"kind": "daily", "times_per_week": None}
        else:
            f = {"kind": "times_per_week", "times_per_week": int(freq["times_per_week"])}
        out.append({**t, "frequency": f})
    return out

CARDS = [
    {
        "key": "reactivate-old-base",
        "kind": "algorithm",
        "title": "Вернуть бывших клиентов",
        "summary_for_trainer": "Собрать базу и писать бывшим лично по несколько человек в неделю.",
        "fit": {"old_base_size": ["10_30", "gt30"]},
        "bottlenecks": ["base_untouched", "no_follow_up"],
    },
    {
        "key": "warm-circle-start",
        "kind": "algorithm",
        "title": "Старт с тёплого круга",
        "summary_for_trainer": "Начать со знакомых и аккуратного профиля в соцсети.",
        "fit": {"old_base_size": ["none", "lt10"]},
        "bottlenecks": ["no_base", "low_visibility"],
    },
    {
        "key": "steady-content",
        "kind": "algorithm",
        "title": "Регулярное присутствие в соцсети",
        "summary_for_trainer": "Одна соцсеть, посты и истории по графику.",
        "fit": {},
        "bottlenecks": ["low_visibility", "irregular_activity"],
    },
    {
        "key": "offer-and-booking",
        "kind": "tactic",
        "title": "Понятное предложение и простая запись",
        "summary_for_trainer": "Сформулировать оффер и проверить страницу записи.",
        "fit": {},
        "bottlenecks": ["weak_offer"],
    },
    {
        "key": "follow-up-routine",
        "kind": "tactic",
        "title": "Доводить разговоры до записи",
        "summary_for_trainer": "Регулярные мягкие напоминания замолчавшим.",
        "fit": {},
        "bottlenecks": ["no_follow_up", "low_conversion", "slow_response"],
    },
    {
        "key": "referrals",
        "kind": "tactic",
        "title": "Рекомендации от клиентов",
        "summary_for_trainer": "Просить довольных клиентов порекомендовать вас.",
        "fit": {},
        "bottlenecks": ["no_referrals"],
    },
    {
        "key": "local-partners",
        "kind": "tactic",
        "title": "Партнёры рядом",
        "summary_for_trainer": "Договориться с массажистом, клубом, магазином рядом.",
        "fit": {"hours_per_week": ["2_5", "gt5"]},
        "bottlenecks": ["no_base", "low_visibility"],
    },
    {
        "key": "service-listings",
        "kind": "tactic",
        "title": "Анкета на площадках услуг",
        "summary_for_trainer": "Анкета на Авито Услуги или Профи.ру и ответы на обращения.",
        "fit": {},
        "bottlenecks": ["no_base", "low_visibility", "weak_offer"],
    },
    {
        "key": "ethics-and-law",
        "kind": "restriction",
        "title": "Этика и закон",
        "summary_for_trainer": "Писать только тем, кто знает вас или сам проявил интерес.",
        "fit": {},
        "bottlenecks": [],
    },
    {
        "key": "mvp-scope-exclusions",
        "kind": "restriction",
        "title": "Что помощник пока не предлагает",
        "summary_for_trainer": (
            "Пока бесплатные способы: база, знакомые, соцсети, партнёры, запись, "
            "Авито/Профи. Платной рекламы, набора через зал клуба и многодневных "
            "челленджей в план сам не ставит."
        ),
        "fit": {},
        "bottlenecks": [],
    },
]

# Актуальные default_tasks light для reactivate — из файла карточки (T-140).
DEFAULT_TASKS_LIGHT_REACTIVATE = default_tasks("reactivate-old-base", "light")

ALLOWED_TYPES = [
    "strategy.base_collect",
    "strategy.base_reactivate",
    "strategy.follow_up",
    "strategy.trial_convert",
    "strategy.referral_ask",
    "strategy.offer_setup",
    "strategy.link_share",
    "strategy.social_profile",
    "strategy.listing_setup",
    "strategy.content_post",
    "strategy.content_short",
    "strategy.community_engage",
    "strategy.partner_outreach",
    "strategy.review_collect",
]


def cards_for(*keys: str) -> list[dict]:
    by_key = {c["key"]: c for c in CARDS}
    out = [by_key[k] for k in keys if k in by_key]
    for always in ("ethics-and-law", "mvp-scope-exclusions"):
        if always not in keys and always in by_key:
            out.append(by_key[always])
    return out
