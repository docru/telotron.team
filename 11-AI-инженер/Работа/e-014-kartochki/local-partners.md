---
key: local-partners
kind: tactic
version: 1
title: Партнёры рядом
summary_for_trainer: >-
  Договариваемся с теми, у кого уже есть ваши будущие клиенты: фитнес-клуб,
  массажист, нутрициолог, спортивный магазин, детский центр. Взаимные
  рекомендации, совместная пробная, ваша визитка у них. Подходит, если вы
  работаете офлайн и есть пара часов в неделю.
fit:
  hours_per_week: ["2_5", gt5]
bottlenecks: [no_base, low_visibility]
default_tasks:
  light:
    - type: strategy.partner_outreach
      title: Составьте список 3 мест рядом, где бывают ваши будущие клиенты
      frequency: once
      minutes: 20
      when: first_week
      hint: Подумайте, куда ещё ходят люди, которым нужен тренер, — массаж, магазин спортпита, детские секции, клубы.
    - type: strategy.partner_outreach
      title: Предложите сотрудничество одному месту из списка
      frequency: { times_per_week: 1 }
      minutes: 20
      when: every_week
      hint: Начните с пользы для партнёра — что получит он. Предложите простое — взаимные рекомендации.
  moderate:
    - type: strategy.partner_outreach
      title: Составьте список 5 мест рядом, где бывают ваши будущие клиенты
      frequency: once
      minutes: 20
      when: first_week
      hint: Массаж, магазин спортпита, детские секции, клубы, кабинеты нутрициологов — кто работает с тем же человеком.
    - type: strategy.partner_outreach
      title: Предложите сотрудничество одному месту из списка
      frequency: { times_per_week: 2 }
      minutes: 20
      when: every_week
      hint: Начните с пользы для партнёра. Предложите простое — взаимные рекомендации или совместную пробную.
    - type: strategy.community_engage
      title: Ответьте на вопрос в чате района или дома
      frequency: { times_per_week: 2 }
      minutes: 15
      when: every_week
      hint: Помогите по существу, без рекламы. Ссылка на себя — только если правила чата разрешают.
  intense:
    - type: strategy.partner_outreach
      title: Составьте список 8 мест рядом, где бывают ваши будущие клиенты
      frequency: once
      minutes: 20
      when: first_week
      hint: Массаж, спортпит, детские секции, клубы, нутрициологи, корпоративные спортзалы.
    - type: strategy.partner_outreach
      title: Предложите сотрудничество одному месту из списка
      frequency: { times_per_week: 3 }
      minutes: 20
      when: every_week
      hint: Начните с пользы для партнёра. Договорённость закрепите письменно — что делает каждый.
    - type: strategy.community_engage
      title: Ответьте на вопрос в чате района или дома
      frequency: { times_per_week: 3 }
      minutes: 15
      when: every_week
      hint: Помогите по существу, без рекламы. Ссылка на себя — только если правила чата разрешают.
default_milestones:
  - position: 1
    title: Первые предложения партнёрам отправлены
    week: 2
    criteria:
      - { metric: tasks_done, task_type: strategy.partner_outreach, min: { light: 2, moderate: 3, intense: 4 } }
  - position: 2
    title: Есть договорённости с партнёрами
    week: 4
    criteria:
      - { metric: tasks_done, task_type: strategy.partner_outreach, min: { light: 3, moderate: 5, intense: 8 } }
  - position: 3
    title: Пришли люди от партнёров
    week: 6
    criteria:
      - { metric: leads_new, min: { light: 1, moderate: 1, intense: 2 } }
---
# Партнёры рядом

**Когда применять.** Тренер работает офлайн (зал, студия, район), базы мало, есть 2+ часа в неделю (`hours_per_week` = `2_5` / `gt5`). Диагноз: `no_base`, `low_visibility`.

**Почему работает.** Партнёр уже общается с людьми, которым нужен тренер, и пользуется их доверием. Рекомендация от массажиста или продавца спортпита весит больше рекламы.

**Шаги.**
1. Список мест рядом, где бывают будущие клиенты.
2. Предложение партнёру с его выгодой: взаимные рекомендации, совместная пробная, визитка / QR на запись.
3. Параллельно — полезные ответы в местных чатах района.

**На что смотреть.** Сколько предложений отправлено; заявки со страницы записи. Договорённость с партнёром система не видит — отмечается выполнением задачи.

**Ограничения.** Не передавать партнёру контакты своих клиентов без их согласия. Не обещать партнёру комиссию, о которой тренер не договорился. Не рекламировать в чатах, где это запрещено. Сначала — карточка `ethics-and-law`.

**Сочетается с:** `warm-circle-start`, `offer-and-booking`.
