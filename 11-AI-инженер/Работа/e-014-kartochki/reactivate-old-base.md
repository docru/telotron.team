---
key: reactivate-old-base
kind: algorithm
version: 2
title: Вернуть бывших клиентов
summary_for_trainer: >-
  Собираем в CRM тех, с кем вы уже занимались, и каждую неделю пишем нескольким
  лично: как дела, чем вы сейчас занимаетесь, что есть время для занятий. Тем,
  кто не ответил, — одно вежливое напоминание. С этого обычно проще всего
  начать: эти люди вас уже знают.
fit:
  old_base_size: ["10_30", "gt30"]
bottlenecks: [base_untouched, no_follow_up]
default_tasks:
  light:
    - type: strategy.base_collect
      title: Внесите в CRM 5 бывших клиентов
      frequency: once
      minutes: 15
      when: first_week
      hint: Начните с тех, с кем расстались хорошо и кто занимался дольше месяца. Телефон или ник в соцсети — достаточно.
    - type: strategy.base_collect
      title: Добавьте в CRM ещё 3 бывших клиента
      frequency: { times_per_week: 1 }
      minutes: 10
      when: every_week
      hint: Список должен расти вместе с сообщениями — иначе к 3–4 неделе писать будет некому.
    - type: strategy.base_reactivate
      title: Напишите 3 людям из старой базы за неделю
      frequency: { times_per_week: 1 }
      minutes: 25
      when: every_week
      hint: Пишите лично, не рассылкой. Спросите, как дела, и одной фразой скажите, чем вы сейчас занимаетесь. Число в названии — итог на неделю.
    - type: strategy.follow_up
      title: Напомните о себе тем, кто не ответил
      frequency: { times_per_week: 1 }
      minutes: 10
      when: every_week
      hint: Одно напоминание через 3–5 дней — нормально. Если снова тишина, больше не пишите — человек вернётся, когда будет готов.
  moderate:
    - type: strategy.base_collect
      title: Внесите в CRM 10 бывших клиентов
      frequency: once
      minutes: 25
      when: first_week
      hint: Начните с тех, с кем расстались хорошо. Отметьте в заметке, чем занимались, — пригодится для сообщения.
    - type: strategy.base_collect
      title: Добавьте в CRM ещё 5 бывших клиентов
      frequency: { times_per_week: 1 }
      minutes: 15
      when: every_week
      hint: Список должен расти вместе с сообщениями — иначе к 3–4 неделе писать будет некому.
    - type: strategy.base_reactivate
      title: Напишите 5 людям из старой базы за неделю
      frequency: { times_per_week: 1 }
      minutes: 30
      when: every_week
      hint: Вспомните, с какой целью человек приходил, и упомяните это. Число в названии — итог на неделю, не за один раз.
    - type: strategy.follow_up
      title: Напомните о себе тем, кто не ответил
      frequency: { times_per_week: 2 }
      minutes: 10
      when: every_week
      hint: Одно напоминание через 3–5 дней — нормально. Если снова тишина — больше не пишите.
    - type: strategy.trial_convert
      title: Предложите встречу или пробную тем, кто откликнулся
      frequency: { times_per_week: 1 }
      minutes: 10
      when: every_week
      hint: "Тем, кто ответил с интересом: предложите два конкретных времени. Если таких людей нет — задача выполнена."
  intense:
    - type: strategy.base_collect
      title: Внесите в CRM 15 бывших клиентов
      frequency: once
      minutes: 30
      when: first_week
      hint: Пройдитесь по переписке и старым записям. Отметьте, чем занимались, — пригодится для сообщения.
    - type: strategy.base_collect
      title: Добавьте в CRM ещё 5 бывших клиентов
      frequency: { times_per_week: 1 }
      minutes: 15
      when: every_week
      hint: Список должен расти вместе с сообщениями — иначе к 3–4 неделе писать будет некому.
    - type: strategy.base_reactivate
      title: Напишите 8 людям из старой базы за неделю
      frequency: { times_per_week: 1 }
      minutes: 40
      when: every_week
      hint: Пишите лично, с общим контекстом. Не прикладывайте прайс в первом сообщении. Число в названии — итог на неделю.
    - type: strategy.follow_up
      title: Напомните о себе тем, кто не ответил
      frequency: { times_per_week: 3 }
      minutes: 10
      when: every_week
      hint: Одно напоминание через 3–5 дней. Если снова тишина — больше не пишите.
    - type: strategy.trial_convert
      title: Предложите встречу или пробную тем, кто откликнулся
      frequency: { times_per_week: 2 }
      minutes: 10
      when: every_week
      hint: "Тем, кто ответил с интересом: два конкретных времени. Если таких людей нет — задача выполнена."
default_milestones:
  - position: 1
    title: База собрана, первые сообщения отправлены
    week: 2
    criteria:
      - { metric: contacts_added, source: legacy_base, min: { light: 5, moderate: 10, intense: 15 } }
      - { metric: tasks_done, task_type: strategy.base_reactivate, min: { light: 1, moderate: 1, intense: 1 } }
  - position: 2
    title: Пошли ответы
    week: 4
    criteria:
      - { metric: dialogs_started, min: { light: 2, moderate: 4, intense: 6 } }
  - position: 3
    title: Разговоры стали регулярными
    week: 6
    criteria:
      - { metric: dialogs_started, min: { light: 3, moderate: 6, intense: 10 } }
      - { metric: tasks_done, task_type: strategy.follow_up, min: { light: 3, moderate: 6, intense: 10 } }
---
# Вернуть бывших клиентов

**Когда применять.** У тренера есть бывшие клиенты или учёт старых занятий (от 10 человек), но им давно не писали. Диагноз: `base_untouched`; часто вместе с `no_follow_up`.

**Почему работает.** Бывший клиент уже знает тренера, его подход и цены. Частые причины ухода — график, переезд, пауза, а не недовольство. Личное сообщение снимает барьер «неудобно вернуться».

**Шаги.**
1. Собрать в CRM бывших клиентов (источник «старая база»): контакт и коротко — с чем приходили.
2. Каждую неделю дополнять список и писать нескольким лично: интерес к человеку, одна фраза о текущей работе тренера, без давления и прайса. Число сообщений в задаче — **на всю неделю**, не за один заход.
3. Тем, кто ответил с интересом, — предложить встречу или пробную, с конкретным временем.
4. Тем, кто не ответил, — одно напоминание через 3–5 дней. После второго молчания — не писать.

**На что смотреть.** Сколько человек внесено, сколько сообщений отправлено, сколько диалогов началось. Если ответ будет, он чаще приходит в первые дни после сообщения; тренеру сроки не обещать.

**Правило напоминаний.** Человеку, который не ответил на первое сообщение, — одно напоминание. Два напоминания — только тем, кто уже был в разговоре (см. `follow-up-routine`).

**Ограничения.** Только люди, которые сами были клиентами. Не массовая рассылка. Отказ («не пишите») — отметить в CRM и больше не писать. Не планировать больше сообщений, чем людей в списке. Сначала — карточка `ethics-and-law`.

**Сочетается с:** `follow-up-routine` (если разговоры затухают), `offer-and-booking` (если нечего предложить конкретно), `referrals` (если вернувшиеся довольны).
