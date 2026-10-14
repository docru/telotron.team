---
key: warm-circle-start
kind: algorithm
version: 2
title: Старт с тёплого круга
summary_for_trainer: >-
  Если своей базы клиентов пока нет, начинаем с людей, которые знают вас лично:
  друзья, коллеги, знакомые по залу и соцсетям. Приводим в порядок профиль,
  рассказываем им, чем вы теперь занимаетесь, и просим подсказать тем, кому
  это пригодится. Без продаж в лоб.
fit:
  old_base_size: ["none", "lt10"]
bottlenecks: [no_base, low_visibility]
default_tasks:
  light:
    - type: strategy.social_profile
      title: "Оформите профиль в соцсети: кто вы и как записаться"
      frequency: once
      minutes: 20
      when: first_week
      hint: В первой строке — для кого вы и с чем помогаете. Ссылка на запись — в шапке, не в посте.
    - type: strategy.content_post
      title: Расскажите в личной соцсети, что теперь ведёте тренировки
      frequency: once
      minutes: 30
      when: first_week
      hint: "Для кого вы, с чем помогаете, как записаться. Один пост или история — самый заметный первый шаг для знакомых."
    - type: strategy.base_collect
      title: Внесите в CRM 5 знакомых, кому может быть интересно
      frequency: once
      minutes: 15
      when: first_week
      hint: Подумайте о тех, кто спрашивал вас про тренировки или питание. Это уже тёплый интерес.
    - type: strategy.base_collect
      title: Добавьте в CRM ещё 2 знакомых
      frequency: { times_per_week: 1 }
      minutes: 10
      when: every_week
      hint: Круг знакомых конечен — список должен немного расти, иначе к 3–4 неделе писать будет некому.
    - type: strategy.base_reactivate
      title: Расскажите 2 знакомым за неделю, чем вы теперь занимаетесь
      frequency: { times_per_week: 1 }
      minutes: 15
      when: every_week
      hint: Просто расскажите, чем занимаетесь, и спросите, нет ли среди их знакомых тех, кому это пригодится. Число — итог на неделю.
    - type: strategy.content_short
      title: Выложите короткую историю о своей работе
      frequency: { times_per_week: 1 }
      minutes: 10
      when: every_week
      hint: Достаточно фото с тренировки и одной фразы. Регулярность важнее красоты.
  moderate:
    - type: strategy.social_profile
      title: "Оформите профиль в соцсети: кто вы и как записаться"
      frequency: once
      minutes: 20
      when: first_week
      hint: В первой строке — для кого вы и с чем помогаете. Ссылка на запись — в шапке.
    - type: strategy.content_post
      title: Расскажите в личной соцсети, что теперь ведёте тренировки
      frequency: once
      minutes: 30
      when: first_week
      hint: "Для кого вы, с чем помогаете, как записаться. Один пост или история — самый заметный первый шаг."
    - type: strategy.base_collect
      title: Внесите в CRM 10 знакомых, кому может быть интересно
      frequency: once
      minutes: 20
      when: first_week
      hint: Вспомните тех, кто спрашивал про тренировки или питание, и коллег по прошлой работе.
    - type: strategy.link_share
      title: Поставьте ссылку на запись в профиль и подпись сообщений
      frequency: once
      minutes: 10
      when: first_week
      hint: Человек, которому интересно, должен записаться в один клик — без переписки «а как к вам попасть».
    - type: strategy.base_collect
      title: Добавьте в CRM ещё 3 знакомых
      frequency: { times_per_week: 1 }
      minutes: 10
      when: every_week
      hint: Список должен немного расти каждую неделю — иначе писать будет некому.
    - type: strategy.base_reactivate
      title: Расскажите 3 знакомым за неделю, чем вы теперь занимаетесь
      frequency: { times_per_week: 1 }
      minutes: 20
      when: every_week
      hint: Расскажите и спросите, нет ли среди их знакомых тех, кому это нужно. Число — итог на неделю.
    - type: strategy.content_short
      title: Выложите короткую историю о своей работе
      frequency: { times_per_week: 2 }
      minutes: 10
      when: every_week
      hint: "Фото или кружок и одна фраза: что сегодня делали и зачем."
    - type: strategy.follow_up
      title: Ответьте и напомните тем, кто проявил интерес
      frequency: { times_per_week: 1 }
      minutes: 10
      when: every_week
      hint: Если человек спросил «а сколько стоит» и пропал — одно напоминание через 3–5 дней нормально.
  intense:
    - type: strategy.social_profile
      title: "Оформите профиль в соцсети: кто вы и как записаться"
      frequency: once
      minutes: 20
      when: first_week
      hint: В первой строке — для кого вы и с чем помогаете. Ссылка на запись — в шапке.
    - type: strategy.content_post
      title: Расскажите в личной соцсети, что теперь ведёте тренировки
      frequency: once
      minutes: 30
      when: first_week
      hint: "Для кого вы, с чем помогаете, как записаться. Один пост или история в начале — самый заметный шаг."
    - type: strategy.base_collect
      title: Внесите в CRM 15 знакомых, кому может быть интересно
      frequency: once
      minutes: 25
      when: first_week
      hint: Друзья, коллеги, знакомые по залу, родители из школы — все, кто знает вас лично.
    - type: strategy.link_share
      title: Поставьте ссылку на запись в профиль и подпись сообщений
      frequency: once
      minutes: 10
      when: first_week
      hint: Человек, которому интересно, должен записаться в один клик.
    - type: strategy.base_collect
      title: Добавьте в CRM ещё 5 знакомых
      frequency: { times_per_week: 1 }
      minutes: 15
      when: every_week
      hint: Список должен расти — иначе к 3–4 неделе писать будет некому.
    - type: strategy.base_reactivate
      title: Расскажите 5 знакомым за неделю, чем вы теперь занимаетесь
      frequency: { times_per_week: 1 }
      minutes: 25
      when: every_week
      hint: Расскажите и попросите совета или рекомендации. Не прикладывайте прайс. Число — итог на неделю.
    - type: strategy.content_post
      title: Опубликуйте пост о своём подходе или результате клиента
      frequency: { times_per_week: 1 }
      minutes: 30
      when: every_week
      hint: Один пост — одна мысль. Результат клиента — только с его согласия.
    - type: strategy.content_short
      title: Выложите короткую историю о своей работе
      frequency: { times_per_week: 2 }
      minutes: 10
      when: every_week
      hint: Фото или кружок и одна фраза. Регулярность важнее красоты.
    - type: strategy.follow_up
      title: Ответьте и напомните тем, кто проявил интерес
      frequency: { times_per_week: 2 }
      minutes: 10
      when: every_week
      hint: Одно напоминание через 3–5 дней — нормально. Не отвечают дважды — больше не пишите.
default_milestones:
  - position: 1
    title: Профиль готов, круг знакомых собран
    week: 2
    criteria:
      - { metric: tasks_done, task_type: strategy.social_profile, min: { light: 1, moderate: 1, intense: 1 } }
      - { metric: contacts_added, min: { light: 5, moderate: 10, intense: 15 } }
  - position: 2
    title: Первые разговоры
    week: 4
    criteria:
      - { metric: dialogs_started, min: { light: 2, moderate: 3, intense: 5 } }
  - position: 3
    title: Пошли заявки и разговоры
    week: 6
    criteria:
      - { metric: dialogs_started, min: { light: 3, moderate: 5, intense: 8 } }
      - { metric: leads_new, min: { light: 1, moderate: 1, intense: 2 } }
---
# Старт с тёплого круга

**Когда применять.** Своей базы клиентов нет или почти нет (`old_base_size` = `none` / `lt10`): начинающий тренер, переезд, смена формата. Диагноз: `no_base`, часто `low_visibility`.

**Почему работает.** Первые клиенты новичка почти всегда приходят от знакомых и их знакомых. Им не нужно доказывать, что тренер настоящий, — нужно узнать, что он теперь этим занимается.

**Шаги.**
1. Привести в порядок профиль в основной соцсети: для кого, с чем помогает, ссылка на запись.
2. Один раз в начале — пост или история в личной соцсети: «теперь веду тренировки / сопровождение, вот для кого и как записаться».
3. Собрать в CRM знакомых и каждую неделю немного дополнять список.
4. Каждую неделю лично рассказывать нескольким, чем занимается, и просить совета / рекомендации — не продавать. Число в задаче — **на всю неделю**.
5. Поддерживать видимость короткими историями; при большей интенсивности — постами.
6. Отвечать и напоминать тем, кто проявил интерес.

**На что смотреть.** Готов ли профиль, сколько знакомых внесено, сколько разговоров началось. Заявки появляются не сразу — сначала разговоры; тренеру сроки не обещать.

**Ограничения.** Не писать незнакомым людям в личные сообщения. Не давить на знакомых: одному знакомому — одно личное сообщение о новой работе, без повторных «ну как, надумал?». Круг знакомых конечен — не планировать больше сообщений, чем людей в списке. Сначала — карточка `ethics-and-law`.

**Сочетается с:** `steady-content` (если тренер готов вести соцсеть), `local-partners` / партнёры (если есть смежные специалисты или авторы каналов), `offer-and-booking`, `service-listings` (площадки услуг).
