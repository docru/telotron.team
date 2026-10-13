"""Проверка черновиков карточек по правилам e-014-volna-4-tipy-i-kartochki.md §4."""

import pathlib
import sys

import yaml

TYPES = {
    "strategy.base_collect", "strategy.base_reactivate", "strategy.follow_up",
    "strategy.trial_convert", "strategy.referral_ask", "strategy.offer_setup",
    "strategy.link_share", "strategy.social_profile", "strategy.content_post",
    "strategy.content_short", "strategy.community_engage",
    "strategy.partner_outreach", "strategy.review_collect",
}
BOTTLENECKS = {
    "base_untouched", "no_base", "low_visibility", "weak_offer", "slow_response",
    "no_follow_up", "low_conversion", "no_referrals", "irregular_activity",
}
FIT = {
    "services": {"workouts", "nutrition", "complex"},
    "old_base_size": {"none", "lt10", "10_30", "gt30"},
    "channels": {"vk", "ok", "tg", "max"},
    "hours_per_week": {"lt2", "2_5", "gt5"},
    "urgency": {"urgent", "normal", "no_rush"},
    "offer": {"free_trial", "paid_trial", "consultation"},
}
METRICS = {"tasks_done", "contacts_added", "dialogs_started", "leads_new"}
KINDS = {"algorithm", "tactic", "template", "restriction"}
CAPS = {"light": 100, "moderate": 180, "intense": 360}  # sales.strategic.weekly_minutes, 2026-10-13


def per_week(freq) -> int:
    if freq == "once":
        return 1
    if freq == "daily":
        return 7
    return int(freq["times_per_week"])


def check(path: pathlib.Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    _, head, body = text.split("---", 2)
    card = yaml.safe_load(head)
    e = errors.append

    if card["key"] != path.stem:
        e("key != имя файла")
    if card["kind"] not in KINDS:
        e(f"kind {card['kind']}")
    if len(card["title"]) > 60:
        e("title > 60")
    if len(card["summary_for_trainer"]) > 300:
        e(f"summary {len(card['summary_for_trainer'])} > 300")
    for field, values in (card.get("fit") or {}).items():
        if field not in FIT or not set(values) <= FIT[field]:
            e(f"fit {field}={values}")
    for b in card.get("bottlenecks") or []:
        if b not in BOTTLENECKS:
            e(f"bottleneck {b}")
    if not body.strip():
        e("пустое тело")

    if card["kind"] in ("algorithm", "tactic"):
        tasks = card.get("default_tasks") or {}
        if set(tasks) != set(CAPS):
            e(f"интенсивности {sorted(tasks)}")
        for level, items in tasks.items():
            first = every = 0
            for t in items:
                if t["type"] not in TYPES:
                    e(f"{level}: тип {t['type']}")
                if len(t["title"]) > 100:
                    e(f"{level}: title > 100")
                if not 5 <= t["minutes"] <= 60:
                    e(f"{level}: minutes {t['minutes']}")
                if len(t.get("hint", "")) > 200:
                    e(f"{level}: hint {len(t['hint'])} > 200 ({t['title']})")
                if t["when"] not in ("first_week", "every_week"):
                    e(f"{level}: when {t['when']}")
                load = t["minutes"] * per_week(t["frequency"])
                if t["when"] == "first_week":
                    first += load
                else:
                    every += load
            week1 = first + every
            if week1 > CAPS[level]:
                e(f"{level}: нагрузка недели 1 {week1} > {CAPS[level]}")
            print(f"  {level}: неделя 1 = {week1} мин, дальше = {every} мин")
            if every == 0:
                e(f"{level}: нет задач every_week")
        for m in card.get("default_milestones") or []:
            if not 1 <= m["week"] <= 6:
                e(f"веха {m['position']}: week {m['week']}")
            for c in m["criteria"]:
                if c["metric"] not in METRICS:
                    e(f"веха {m['position']}: metric {c['metric']}")
                if set(c["min"]) != set(CAPS):
                    e(f"веха {m['position']}: min по интенсивностям")
                if c.get("task_type") and c["task_type"] not in TYPES:
                    e(f"веха {m['position']}: task_type {c['task_type']}")
    elif card.get("default_tasks"):
        e("restriction с default_tasks")
    return errors


def main() -> int:
    failed = 0
    for path in sorted(pathlib.Path(__file__).parent.glob("*.md")):
        print(path.name)
        errs = check(path)
        for err in errs:
            print(f"  ОШИБКА: {err}")
        failed += bool(errs)
    print(f"\nКарточек с ошибками: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
