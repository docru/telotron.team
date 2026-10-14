---
key: service-listings
kind: tactic
version: 1
title: Анкета на площадках услуг
summary_for_trainer: >-
  Оформляем понятную анкету на Авито Услуги или Профи.ру (и похожих): кто вы,
  для кого, что предлагаете, как связаться. Раз в неделю отвечаем на обращения
  и слегка обновляем текст. Особенно полезно начинающим и в регионах.
bottlenecks: [no_base, low_visibility, weak_offer]
default_tasks:
  light:
    - type: strategy.listing_setup
      title: Оформите анкету на одной площадке услуг
      frequency: once
      minutes: 40
      when: first_week
      hint: "Авито Услуги или Профи.ру: для кого вы, с чем помогаете, район или онлайн, как записаться. Фото — живое, не сток."
    - type: strategy.listing_setup
      title: Ответьте на обращения с площадки или обновите анкету
      frequency: { times_per_week: 1 }
      minutes: 15
      when: every_week
      hint: Ответ в день обращения заметно повышает шанс записи. Если обращений нет — проверьте текст и фото анкеты. Если таких людей нет — задача выполнена.
  moderate:
    - type: strategy.listing_setup
      title: Оформите анкету на одной площадке услуг
      frequency: once
      minutes: 40
      when: first_week
      hint: "Для кого → что получит → как начать. Укажите онлайн или район. Ссылка на запись Telotron — если площадка позволяет."
    - type: strategy.link_share
      title: Добавьте ссылку на запись в анкету или ответное сообщение
      frequency: once
      minutes: 10
      when: first_week
      hint: Человеку с площадки должно быть просто перейти к записи без долгой переписки.
    - type: strategy.listing_setup
      title: Ответьте на обращения с площадки или обновите анкету
      frequency: { times_per_week: 2 }
      minutes: 15
      when: every_week
      hint: Ответ в день обращения. Раз в неделю — мелкая правка текста или фото. Если обращений нет — задача про проверку анкеты всё равно полезна.
    - type: strategy.follow_up
      title: Напомните тем, кто написал с площадки и замолчал
      frequency: { times_per_week: 1 }
      minutes: 10
      when: every_week
      hint: Одно напоминание через 3–5 дней. Если таких людей нет — задача выполнена.
  intense:
    - type: strategy.listing_setup
      title: Оформите анкеты на двух площадках услуг
      frequency: once
      minutes: 50
      when: first_week
      hint: "Например Авито Услуги и Профи.ру. Текст один по смыслу, подправьте под правила площадки. Без платного продвижения в MVP."
    - type: strategy.link_share
      title: Добавьте ссылку на запись в анкеты и шаблоны ответов
      frequency: once
      minutes: 15
      when: first_week
      hint: Заготовка короткого ответа со ссылкой на запись экономит время при потоке сообщений.
    - type: strategy.listing_setup
      title: Ответьте на обращения с площадок или обновите анкеты
      frequency: { times_per_week: 3 }
      minutes: 15
      when: every_week
      hint: Ответ в день обращения. Без платного поднятия анкеты — только текст, фото и скорость ответа.
    - type: strategy.follow_up
      title: Напомните тем, кто написал с площадки и замолчал
      frequency: { times_per_week: 2 }
      minutes: 10
      when: every_week
      hint: Одно напоминание через 3–5 дней. Если таких людей нет — задача выполнена.
default_milestones:
  - position: 1
    title: Анкета на площадке готова
    week: 2
    criteria:
      - { metric: tasks_done, task_type: strategy.listing_setup, min: { light: 2, moderate: 3, intense: 4 } }
  - position: 2
    title: Пошли разговоры с площадки
    week: 4
    criteria:
      - { metric: dialogs_started, min: { light: 1, moderate: 2, intense: 3 } }
  - position: 3
    title: Появились заявки
    week: 6
    criteria:
      - { metric: leads_new, min: { light: 1, moderate: 1, intense: 2 } }
---
# Анкета на площадках услуг

**Когда применять.** Базы мало или о тренере почти не знают; особенно начинающие и регионы. Диагноз: `no_base`, `low_visibility`, иногда `weak_offer`. Люди на Авито Услуги / Профи.ру уже ищут услугу — им нужен понятный профиль и быстрый ответ.

**Почему работает.** Площадка приводит заинтересованных. Решает не «красота» анкеты, а ясность (для кого / что / как начать) и ответ в тот же день.

**Шаги.**
1. Выбрать одну площадку (при intense — две): оформить анкету без обещаний результата в цифрах.
2. Указать онлайн или район; по возможности — ссылку на запись.
3. Каждую неделю отвечать на обращения и слегка обновлять текст/фото.
4. Тем, кто написал и замолчал, — одно мягкое напоминание.

**На что смотреть.** Анкета оформлена; разговоры и заявки (в т. ч. если тренер вносит обращения из площадки в CRM вручную).

**Ограничения.** Без платного продвижения и покупки «подъёма» в MVP (см. `mvp-scope-exclusions`). Не обещать результат в цифрах. Не передавать контакты третьим лицам. Сначала — `ethics-and-law`.

**Сочетается с:** `offer-and-booking` (что предлагать и как записаться), `warm-circle-start`, `follow-up-routine`.
