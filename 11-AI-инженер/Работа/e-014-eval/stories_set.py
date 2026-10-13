"""Проверочный набор рассказов для sales.strategic.intake_extract v1.

Запуск: python3 stories_set.py → stories-v1.json
"""

from __future__ import annotations

import json
from pathlib import Path

ALLOWED = {
    "services": ["workouts", "nutrition", "complex"],
    "channels": ["vk", "ok", "tg", "max"],
    "old_base_size": ["none", "lt10", "10_30", "gt30"],
    "hours_per_week": ["lt2", "2_5", "gt5"],
    "urgency": ["urgent", "normal", "no_rush"],
    "offer": ["free_trial", "paid_trial", "consultation"],
}


def case(cid: str, desc: str, story: str, expect: dict) -> dict:
    return {
        "id": cid,
        "description": desc,
        "input": {"story": story, "allowed": ALLOWED},
        "expect": expect,
    }


CASES = [
    case(
        "s01_clear_base_mid",
        "Ясный рассказ: силовые, база ~15, Telegram, без спешки, бесплатная пробная",
        "Я тренер по силовым, веду в зале и онлайн. Бывших клиентов примерно пятнадцать, "
        "им давно не писала. Времени часа три-четыре в неделю. Клиенты нужны без спешки. "
        "Бесплатная пробная. Основной канал — телега.",
        {
            "services_any": [["workouts"], ["workouts", "complex"]],
            "old_base_size": "10_30",
            "channels_include": ["tg"],
            "hours_per_week": "2_5",
            "urgency": "no_rush",
            "offer": "free_trial",
            "must_not_unclear": ["old_base_size", "channels", "hours_per_week", "offer"],
        },
    ),
    case(
        "s02_clear_large_base_urgent",
        "Большая база, срочно, ВК, платная пробная",
        "Работаю персональным тренером уже пять лет. В телефоне больше сорока бывших клиентов. "
        "Нужны новые срочно — кредиты. Пишу во ВКонтакте. Предлагаю платную пробную тренировку. "
        "Могу уделять больше пяти часов в неделю.",
        {
            "old_base_size": "gt30",
            "channels_include": ["vk"],
            "hours_per_week": "gt5",
            "urgency": "urgent",
            "offer": "paid_trial",
        },
    ),
    case(
        "s03_sparse",
        "Очень короткий рассказ — почти всё unclear",
        "Нужны клиенты. Я тренер.",
        {
            "must_unclear_any": [
                "services",
                "old_base_size",
                "channels",
                "hours_per_week",
                "urgency",
                "offer",
                "goal_clients_per_month",
            ],
            "unclear_min": 4,
        },
    ),
    case(
        "s04_only_niche",
        "Только ниша, остальное пусто",
        "Помогаю женщинам после родов вернуться в форму, онлайн.",
        {
            "must_unclear_any": ["old_base_size", "channels", "hours_per_week", "offer"],
            "specialization_not_null": True,
        },
    ),
    case(
        "s05_contradiction_base",
        "Противоречие про базу → old_base unclear",
        "Базы клиентов у меня нет совсем. Но я регулярно пишу своим тридцати бывшим ученикам в WhatsApp. "
        "Канал — Telegram. Часов мало, меньше двух. Не горю. Консультация бесплатная.",
        {
            "must_unclear": ["old_base_size"],
            "channels_include": ["tg"],
            "hours_per_week": "lt2",
            "offer": "consultation",
        },
    ),
    case(
        "s06_pii_phone_name",
        "В рассказе имя клиента и телефон — не должны попасть в about/specialization",
        "Я нутрициолог. Клиентка Марина Петрова, телефон +7 916 555-44-33, очень довольна. "
        "Бывших человек восемь. Время 2–5 часов. Канал ОК. Бесплатная консультация. Без спешки.",
        {
            "services_any": [["nutrition"], ["nutrition", "complex"], ["complex"]],
            "old_base_size": "lt10",
            "channels_include": ["ok"],
            "must_not_contain": ["Марина", "Петрова", "916", "555-44-33", "+7"],
        },
    ),
    case(
        "s07_pii_multiple_names",
        "Несколько имён знакомых — не копировать",
        "Знакомые Сергей и Ольга спрашивали про тренировки. Игорь обещал привести жену. "
        "Своей базы почти нет. Веду в Telegram. Часа три в неделю. Хочу пятерых клиентов в месяц. "
        "Срочности нет. Бесплатная пробная.",
        {
            "old_base_size_any": ["none", "lt10"],
            "channels_include": ["tg"],
            "goal_clients_per_month": 5,
            "must_not_contain": ["Сергей", "Ольга", "Игорь"],
        },
    ),
    case(
        "s08_pii_email_nick",
        "Почта и ник — не копировать",
        "Пишите мне на coach_anna@mail.ru или в телеге @anna_fit_pro. Я тренер по йоге. "
        "Базы нет. Часов меньше двух. Не горю. Оффер — консультация. Канал телега.",
        {
            "old_base_size": "none",
            "channels_include": ["tg"],
            "hours_per_week": "lt2",
            "must_not_contain": ["coach_anna@mail.ru", "@anna_fit_pro", "mail.ru"],
        },
    ),
    case(
        "s09_no_base_start",
        "Старт с нуля",
        "Только получила сертификат. Клиентов ещё не было. Буду вести в ВК и телеге. "
        "Часа четыре в неделю. Хочу набрать первых. Бесплатная пробная. Без сильной спешки.",
        {
            "old_base_size": "none",
            "channels_include_all": ["vk", "tg"],
            "offer": "free_trial",
            "hours_per_week_any": ["2_5", "gt5"],
        },
    ),
    case(
        "s10_small_base",
        "Маленькая база lt10",
        "Было человек пять-шесть клиентов в прошлом году. Сейчас на паузе. Канал ОК. "
        "Меньше двух часов в неделю. Нужны люди не срочно. Платная пробная.",
        {
            "old_base_size": "lt10",
            "channels_include": ["ok"],
            "hours_per_week": "lt2",
            "offer": "paid_trial",
        },
    ),
    case(
        "s11_multi_channel_unclear_primary",
        "Много каналов названо — channels могут заполниться все; цель может быть unclear",
        "Силовые и функционал. База около двадцати. Сижу и в ВК, и в телеге, и в Max — не знаю что выбрать. "
        "Часов пять плюс. Срочно нужны клиенты. Бесплатная пробная.",
        {
            "old_base_size": "10_30",
            "urgency": "urgent",
            "offer": "free_trial",
            "channels_min": 2,
        },
    ),
    case(
        "s12_consultation_offer",
        "Оффер консультация, питание",
        "Нутрициолог, веду разборы питания. Базы нет. Telegram. Два-пять часов. "
        "Предлагаю консультацию. Темп спокойный.",
        {
            "services_any": [["nutrition"], ["complex"]],
            "old_base_size": "none",
            "offer": "consultation",
            "channels_include": ["tg"],
        },
    ),
    case(
        "s13_hours_lt2",
        "Явно мало времени",
        "Тренер зала. Бывших много — больше тридцати. ВК. Свободного времени почти нет, меньше двух часов. "
        "Не горю. Бесплатная пробная.",
        {
            "old_base_size": "gt30",
            "hours_per_week": "lt2",
            "channels_include": ["vk"],
            "urgency": "no_rush",
        },
    ),
    case(
        "s14_goal_explicit",
        "Явная цель по числу клиентов",
        "Онлайн-тренер. Хочу стабильно десять новых клиентов в месяц. База человек двенадцать. "
        "Телега. Часов больше пяти. Срочно. Платная пробная.",
        {
            "goal_clients_per_month": 10,
            "old_base_size": "10_30",
            "hours_per_week": "gt5",
            "urgency": "urgent",
            "offer": "paid_trial",
        },
    ),
    case(
        "s15_complex_services",
        "Комплекс: тренировки + питание",
        "Веду и тренировки, и питание вместе. Базы нет. Max и телега. Часа три. Без спешки. Консультация.",
        {
            "services_any": [["complex"], ["workouts", "nutrition"]],
            "old_base_size": "none",
            "offer": "consultation",
        },
    ),
    case(
        "s16_ambiguous_hours",
        "Часы сформулированы туманно → hours unclear",
        "Тренер. База средняя, штук двадцать. ВК. Времени сколько получится — иногда много, иногда ноль. "
        "Бесплатная пробная. Не срочно.",
        {
            "old_base_size": "10_30",
            "channels_include": ["vk"],
            "offer": "free_trial",
            "must_unclear": ["hours_per_week"],
        },
    ),
]


def main() -> None:
    out = Path(__file__).with_name("stories-v1.json")
    out.write_text(json.dumps(CASES, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {len(CASES)} stories → {out.name}")


if __name__ == "__main__":
    main()
