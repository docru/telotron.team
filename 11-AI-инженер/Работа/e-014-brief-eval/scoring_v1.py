#!/usr/bin/env python3
"""Эталон TaskScorer v1 (волна 6): скоринг → отсечение уровней → пороги → топ.

Детерминированно, без ИИ. Веса — e-014-schemas/sales.operational.scoring.weights.v1.json.
Запуск: python3 scoring_v1.py → results/scoring-v1-examples.md; код выхода 1 при расхождении с ожиданием.
Также проверяет длину шаблонов «зачем» (sales.why-templates.v1.json).
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMAS = ROOT.parent / "e-014-schemas"
W = json.loads((SCHEMAS / "sales.operational.scoring.weights.v1.json").read_text(encoding="utf-8"))
WHY = json.loads((SCHEMAS / "sales.why-templates.v1.json").read_text(encoding="utf-8"))

STRATEGY_ORDER = [
    "base_reactivate", "follow_up", "trial_convert", "referral_ask", "base_collect",
    "base_describe", "offer_setup", "link_share", "partner_outreach", "listing_setup", "community_engage",
    "content_post", "content_short", "social_profile", "review_collect",
]
CRM_ORDER = ["reply_new_contact", "next_action", "remind_stale"]


def tier(t: str) -> int:
    return W["tiers"].get(t, 3)


def type_rank(t: str) -> int:
    kind, name = t.split(".", 1)
    if kind == "crm":
        return CRM_ORDER.index(name)
    return 10 + STRATEGY_ORDER.index(name)


@dataclass
class Task:
    id: int
    type: str
    name: str | None = None
    stage: str | None = None          # new · in_progress · client · former · legacy_base
    overdue_days: int = 0
    touch_days: int = 0               # дней с последнего касания (0 — нет касаний / сегодня)
    postponed: int = 0                # сколько раз «Отложить» по этой задаче
    status: str = "open"              # open · done · dismissed · carried_over
    note: str = ""


@dataclass
class Case:
    id: str
    title: str
    intensity: str
    tasks: list[Task]
    rejected_14d: dict[str, int] = field(default_factory=dict)   # тип → число «Не сейчас» за 14 дней
    skills: dict[str, int] = field(default_factory=dict)         # навык → уровень (по умолчанию 1)
    expect_top: list[int] = field(default_factory=list)          # ожидаемый бриф по правилам (task_id)
    expect_candidates: list[int] | None = None                   # ожидаемый список в ИИ (порядок)
    comment: str = ""


def score(task: Task, case: Case, has_urgent_crm: bool) -> tuple[int, dict]:
    t = task.type
    f: dict[str, int] = {}
    f["type"] = W["type_weight"][t]
    f["source"] = W["source_bonus"]["strategy" if t.startswith("strategy.") else "crm_signal"]
    if t in W["overdue"]["applies_to"]:
        cap = W["overdue"]["cap_days"][t]
        f["overdue"] = W["overdue"]["per_day"] * min(task.overdue_days, cap)
    if t.startswith("crm.") and task.stage:
        f["stage"] = W["stage"][task.stage]
    if t in W["touch_age"]["applies_to"]:
        f["touch_age"] = W["touch_age"]["per_day"] * min(task.touch_days, W["touch_age"]["cap_days"])
    if task.postponed:
        f["postponed"] = W["postponed"]["from_count_3"] if task.postponed >= 3 else W["postponed"]["by_count"][str(task.postponed)]
    rej = case.rejected_14d.get(t, 0)
    if rej and t not in W["rejected_type"]["not_applied_to"]:
        key = "strategy.*" if t.startswith("strategy.") else t
        f["rejected"] = max(W["rejected_type"]["per_reject"][key] * rej, W["rejected_type"]["cap"][key])
    skill = W["type_skill"].get(t)
    if t.startswith("strategy.") and skill and case.skills.get(skill, 1) == 0 and has_urgent_crm:
        f["skill_new"] = W["skill_new"]["value"]
    total = max(W["floor"], sum(f.values()))
    return total, f


def prepare(case: Case) -> dict:
    open_tasks = [t for t in case.tasks if t.status == "open"]
    has_urgent = any(tier(t.type) <= 1 for t in open_tasks)
    rows = []
    for t in open_tasks:
        s, f = score(t, case, has_urgent)
        rows.append({"task": t, "tier": tier(t.type), "score": s, "factors": f})
    rows.sort(key=lambda r: (r["tier"], -r["score"], type_rank(r["task"].type), r["task"].id))

    n_max = W["items_max"][case.intensity]
    kept, count = [], 0
    for lvl in range(4):
        if count >= n_max:
            break
        grp = [r for r in rows if r["tier"] == lvl]
        kept.extend(grp)
        count += len(grp)

    th = W["thresholds"]
    low = [r for r in kept if r["score"] < th["drop_below_always"]]
    if low and len(kept) > len(low):
        kept = [r for r in kept if r["score"] >= th["drop_below_always"]]
    mid = [r for r in kept if r["score"] < th["drop_below_if_enough"]]
    if mid and len(kept) - len(mid) >= n_max:
        kept = [r for r in kept if r["score"] >= th["drop_below_if_enough"]]

    kept = kept[: W["candidates_max"]]
    kept_ids = {r["task"].id for r in kept}
    for i, r in enumerate(rows, 1):
        r["rank"] = i
        r["included"] = r["task"].id in kept_ids
    return {"rows": rows, "candidates": [r["task"].id for r in kept], "top": [r["task"].id for r in kept[:n_max]], "n_max": n_max}


def plural_days(n: int) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return f"{n} день"
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return f"{n} дня"
    return f"{n} дней"


def why_for(task: Task) -> str:
    v = WHY["templates"][task.type]
    name = (task.name or "").split(" ")[0][:20] or None
    days = task.overdue_days if task.type != "crm.remind_stale" else task.touch_days
    if name and days and "named_overdue" in v:
        tpl = v["named_overdue"]
    elif name and "named" in v and ("{days}" not in v["named"] or days):
        tpl = v["named"]
    else:
        tpl = v["default"]
    return tpl.replace("{name}", name or "").replace("{days}", plural_days(days))


S = "strategy."
CASES: list[Case] = [
    Case("s01", "Утро light: две заявки — обе в топ, старшая первой", "light", [
        Task(1, "crm.reply_new_contact", "Анна", "new", overdue_days=0),
        Task(2, "crm.reply_new_contact", "Игорь", "new", overdue_days=2),
        Task(3, "crm.next_action", "Олег", "in_progress", overdue_days=0, touch_days=3),
        Task(4, S + "base_reactivate"),
        Task(5, S + "content_post"),
    ], expect_top=[2, 1], expect_candidates=[2, 1],
        comment="Уровень 0 уже заполняет light (2) → договорённость и план не уходят в ИИ."),
    Case("s02", "Договорённости: просроченная выше сегодняшней", "moderate", [
        Task(1, "crm.next_action", "Мария", "in_progress", overdue_days=0, touch_days=2),
        Task(2, "crm.next_action", "Павел", "in_progress", overdue_days=2, touch_days=6),
        Task(3, "crm.remind_stale", "Света", "in_progress", touch_days=12),
        Task(4, S + "follow_up"),
    ], expect_top=[2, 1, 3], expect_candidates=[2, 1, 3],
        comment="2 договорённости < 3 → берётся уровень 2; план (уровень 3) не нужен."),
    Case("s03", "Только план: порядок по типу", "moderate", [
        Task(1, S + "review_collect"),
        Task(2, S + "content_post"),
        Task(3, S + "base_reactivate"),
        Task(4, S + "social_profile"),
    ], expect_top=[3, 2, 4],
        comment="Все ≥20 → порог не режет; review_collect и social_profile по 20 — равенство решает порядок типов (профиль раньше отзывов)."),
    Case("s04", "Новый навык при срочной CRM опускается", "moderate", [
        Task(1, "crm.reply_new_contact", "Анна", "new"),
        Task(2, S + "partner_outreach"),
        Task(3, S + "content_post"),
    ], skills={"partner_outreach": 0, "content_regular": 1},
        expect_top=[1, 3, 2],
        comment="partner_outreach 25 − 10 (навык впервые + есть заявка) = 15 < content_post 21; порог 20 не режет (без него осталось бы 2 < 3)."),
    Case("s05", "Без срочной CRM новый навык не штрафуется", "moderate", [
        Task(1, S + "partner_outreach"),
        Task(2, S + "content_post"),
    ], skills={"partner_outreach": 0},
        expect_top=[1, 2]),
    Case("s06", "Тип часто «Не сейчас» уходит вниз", "moderate", [
        Task(1, S + "follow_up"),
        Task(2, S + "content_post"),
        Task(3, S + "link_share"),
        Task(4, S + "offer_setup"),
    ], rejected_14d={S + "follow_up": 2},
        expect_top=[4, 3, 2], expect_candidates=[4, 3, 2],
        comment="follow_up 33 − 20 = 13 < 20 и сильных ≥3 → в ИИ не уходит (откладывание, не удаление)."),
    Case("s07", "Отложенная один раз — чуть выше; трижды — ниже", "intense", [
        Task(1, S + "link_share", postponed=1),
        Task(2, S + "base_collect"),
        Task(3, S + "base_reactivate", postponed=3),
        Task(4, S + "content_post"),
    ], expect_top=[1, 2, 3],
        comment="link_share 25+5=30 > base_collect 27; base_reactivate 35−10=25 (≥3 переноса — не навязываем)."),
    Case("s08", "Пусто кроме слабой задачи — всё равно показать", "light", [
        Task(1, S + "content_short"),
    ], rejected_14d={S + "content_short": 2},
        expect_top=[1], expect_candidates=[1],
        comment="20 − 20 = 0 < 10, но других нет → оставляем."),
    Case("s09", "Напоминания: дольше без касания — выше (потолок 20 дней)", "light", [
        Task(1, "crm.remind_stale", "Катя", "in_progress", touch_days=8),
        Task(2, "crm.remind_stale", "Дима", "in_progress", touch_days=20),
        Task(3, "crm.remind_stale", "Лена", "in_progress", touch_days=45),
        Task(4, S + "base_reactivate"),
    ], expect_top=[2, 3], expect_candidates=[2, 3, 1],
        comment="Дима и Лена оба на потолке 40 → равенство по id; base_reactivate не берётся (уровень 2 уже 3 ≥ 2)."),
    Case("s10", "Смешанный moderate: заявка + план, отклонённые и выполненные не идут", "moderate", [
        Task(1, "crm.reply_new_contact", "Юля", "new", overdue_days=1),
        Task(2, S + "base_reactivate", status="dismissed"),
        Task(3, S + "follow_up"),
        Task(4, S + "content_post", status="done"),
        Task(5, S + "trial_convert", postponed=1),
        Task(6, S + "community_engage"),
    ], expect_top=[1, 5, 3], expect_candidates=[1, 5, 3, 6],
        comment="trial_convert 33+5=38 > follow_up 33; community_engage 23 ≥ 20 → остаётся кандидатом для ИИ."),
]


def fmt_factors(f: dict) -> str:
    return " ".join(f"{k}{'+' if v >= 0 else ''}{v}" for k, v in f.items() if v)


def main() -> int:
    out = ["# Скоринг v1 — примеры «кандидаты дня → порядок»", "",
           f"Веса: `{W['version']}` · сгенерировано `scoring_v1.py`. Бриф по правилам = первые items_max кандидатов.", ""]
    fails = 0
    for c in CASES:
        res = prepare(c)
        ok_top = res["top"] == c.expect_top
        ok_cand = c.expect_candidates is None or res["candidates"] == c.expect_candidates
        status = "ok" if ok_top and ok_cand else "FAIL"
        fails += status == "FAIL"
        out += [f"## {c.id} · {c.title} · {c.intensity} (items_max {res['n_max']}) · {status}", ""]
        out += ["| # | id | тип | кто | балл | факторы | в ИИ |", "|---|----|-----|-----|------|---------|------|"]
        for r in res["rows"]:
            t = r["task"]
            who = t.name or "—"
            out.append(f"| {r['rank']} | {t.id} | `{t.type}` | {who} | **{r['score']}** | {fmt_factors(r['factors'])} | {'да' if r['included'] else 'нет'} |")
        skipped = [t for t in c.tasks if t.status != "open"]
        if skipped:
            out.append("")
            out.append("Не кандидаты: " + ", ".join(f"{t.id} `{t.type}` ({t.status})" for t in skipped))
        out += ["", f"Бриф по правилам: {res['top']} · ожидалось {c.expect_top}"]
        if c.expect_candidates is not None:
            out.append(f"Кандидаты в ИИ: {res['candidates']} · ожидалось {c.expect_candidates}")
        out.append("")
        out.append("«Зачем» (шаблон):")
        by_id = {t.id: t for t in c.tasks}
        for tid in res["top"]:
            out.append(f"- {tid}: {why_for(by_id[tid])}")
        if c.comment:
            out += ["", f"> {c.comment}"]
        out.append("")

    out += ["## Шаблоны «зачем»: длина", "", "| тип | вариант | символов | текст |", "|-----|---------|----------|-------|"]
    for t, variants in WHY["templates"].items():
        for v, tpl in variants.items():
            txt = tpl.replace("{name}", "Александра"[:20]).replace("{days}", plural_days(12))
            n = len(txt)
            low = f" {txt.lower()} "
            bad = n > 120 or txt.count(".") > 1 or any(p in low for p in (" ты ", " тебе ", " тебя ", " твой ", " твои ", " твоих "))
            fails += bad
            out.append(f"| `{t}` | {v} | {n}{' **FAIL**' if bad else ''} | {txt} |")

    missing = [f"strategy.{s}" for s in STRATEGY_ORDER if f"strategy.{s}" not in WHY["templates"]] + \
              [f"crm.{s}" for s in CRM_ORDER if f"crm.{s}" not in WHY["templates"]]
    if missing:
        fails += 1
        out.append(f"\nНет шаблона: {missing}")

    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "scoring-v1-examples.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"cases={len(CASES)} fails={fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
