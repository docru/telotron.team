---
key: steady-content
kind: algorithm
version: 2
title: Регулярное присутствие в соцсети
summary_for_trainer: >-
  Ведём одну соцсеть по простому графику: понятный профиль, посты о вашем
  подходе и результатах клиентов (с их согласия), короткие истории, полезные
  ответы в сообществах. Доверие копится постепенно — это способ на недели, а не
  на один день.
bottlenecks: [low_visibility, irregular_activity]
default_tasks:
  light:
    - type: strategy.social_profile
      title: "Оформите профиль в соцсети: кто вы и как записаться"
      frequency: once
      minutes: 20
      when: first_week
      hint: В первой строке — для кого вы и с чем помогаете. Ссылка на запись — в шапке.
    - type: strategy.content_post
      title: Опубликуйте пост
      frequency: { times_per_week: 1 }
      minutes: 30
      when: every_week
      hint: "Один пост — одна мысль: частая ошибка, простое упражнение, ответ на вопрос клиента."
    - type: strategy.content_short
      title: Выложите короткую историю
      frequency: { times_per_week: 1 }
      minutes: 10
      when: every_week
      hint: Фото или кружок с тренировки и одна фраза. Регулярность важнее красоты.
  moderate:
    - type: strategy.social_profile
      title: "Оформите профиль в соцсети: кто вы и как записаться"
      frequency: once
      minutes: 20
      when: first_week
      hint: В первой строке — для кого вы и с чем помогаете. Ссылка на запись — в шапке.
    - type: strategy.link_share
      title: Поставьте ссылку на запись в профиль и закреплённый пост
      frequency: once
      minutes: 10
      when: first_week
      hint: Человек, которому интересно, должен записаться в один клик.
    - type: strategy.content_post
      title: Опубликуйте пост
      frequency: { times_per_week: 2 }
      minutes: 30
      when: every_week
      hint: Чередуйте пользу и себя — сегодня совет, в следующий раз история клиента (с согласия) или как вы работаете.
    - type: strategy.content_short
      title: Выложите короткую историю
      frequency: { times_per_week: 2 }
      minutes: 10
      when: every_week
      hint: Фото или кружок и одна фраза. Регулярность важнее красоты.
    - type: strategy.community_engage
      title: Ответьте на вопрос в тематическом или местном чате
      frequency: { times_per_week: 1 }
      minutes: 15
      when: every_week
      hint: Помогите по существу, без рекламы. Ссылка на себя — только если правила чата разрешают.
  intense:
    - type: strategy.social_profile
      title: "Оформите профиль в соцсети: кто вы и как записаться"
      frequency: once
      minutes: 20
      when: first_week
      hint: В первой строке — для кого вы и с чем помогаете. Ссылка на запись — в шапке.
    - type: strategy.link_share
      title: Поставьте ссылку на запись в профиль и закреплённый пост
      frequency: once
      minutes: 10
      when: first_week
      hint: Человек, которому интересно, должен записаться в один клик.
    - type: strategy.content_post
      title: Опубликуйте пост
      frequency: { times_per_week: 3 }
      minutes: 30
      when: every_week
      hint: Больше пользы, реже приглашение. Например, два полезных поста или истории клиента (с согласия) — и один с приглашением на пробную.
    - type: strategy.content_short
      title: Выложите короткую историю
      frequency: { times_per_week: 4 }
      minutes: 10
      when: every_week
      hint: Покажите обычный рабочий день — люди выбирают тренера, с которым им будет комфортно.
    - type: strategy.community_engage
      title: Ответьте на вопрос в тематическом или местном чате
      frequency: { times_per_week: 2 }
      minutes: 15
      when: every_week
      hint: Помогите по существу, без рекламы. Ссылка на себя — только если правила чата разрешают.
default_milestones:
  - position: 1
    title: Профиль готов, публикации пошли
    week: 2
    criteria:
      - { metric: tasks_done, task_type: strategy.social_profile, min: { light: 1, moderate: 1, intense: 1 } }
      - { metric: tasks_done, task_type: strategy.content_post, min: { light: 1, moderate: 3, intense: 4 } }
  - position: 2
    title: Публикации стали регулярными
    week: 4
    criteria:
      - { metric: tasks_done, task_type: strategy.content_post, min: { light: 3, moderate: 6, intense: 8 } }
  - position: 3
    title: Появились заявки
    week: 6
    criteria:
      - { metric: leads_new, min: { light: 1, moderate: 2, intense: 3 } }
---
# Регулярное присутствие в соцсети

**Когда применять.** О тренере мало кто знает, контента нет или он появляется рывками. Диагноз: `low_visibility`, `irregular_activity`. Подходит при любом размере базы; обычно — вторая стратегия в паре с работой с базой или знакомыми.

**Почему работает.** Люди выбирают тренера, которого «уже видели»: регулярный контент создаёт доверие до первого сообщения. Эффект накопительный: первые недели — про регулярность, заявки появляются позже. Тренеру сроки не обещать.

**Шаги.**
1. Одна основная соцсеть из выбранных тренером (не все сразу).
2. Профиль: для кого, с чем помогает, ссылка на запись.
3. Посты по графику: польза, подход, истории клиентов (с согласия), приглашение на пробную.
4. Короткие истории — между постами, без подготовки.
5. При большей интенсивности — полезные ответы в тематических чатах и сообществах (для офлайн-тренера — и в местных).

**На что смотреть.** Регулярность публикаций (код видит выполненные задачи), затем заявки со страницы записи. Охваты и лайки система не видит — не обещать их.

**Ограничения.** Не обещать результат в цифрах («минус 10 кг за месяц»). Фото и истории клиентов — только с их согласия. Не спамить в чужих сообществах. Сначала — карточка `ethics-and-law`.

**Сочетается с:** `warm-circle-start`, `reactivate-old-base`, `offer-and-booking`.
