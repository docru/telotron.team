---
key: follow-up-routine
kind: tactic
version: 1
title: Доводить разговоры до записи
summary_for_trainer: >-
  Многие разговоры затухают не из-за отказа, а потому что человек отвлёкся.
  Несколько раз в неделю проходим по тем, кто проявил интерес и замолчал, и
  мягко напоминаем. Тем, кто был на пробной, — предлагаем продолжение.
bottlenecks: [no_follow_up, low_conversion, slow_response]
default_tasks:
  light:
    - type: strategy.follow_up
      title: Напомните о себе тем, кто замолчал
      frequency: { times_per_week: 2 }
      minutes: 10
      when: every_week
      hint: Напоминание — не «ну что, решили?», а новый повод — вопрос, совет, свободное время на неделе.
    - type: strategy.trial_convert
      title: Предложите продолжение тем, кто был на пробной
      frequency: { times_per_week: 1 }
      minutes: 10
      when: every_week
      hint: Напомните, что получилось на пробной, и предложите конкретный формат и время следующего занятия.
  moderate:
    - type: strategy.follow_up
      title: Напомните о себе тем, кто замолчал
      frequency: { times_per_week: 3 }
      minutes: 10
      when: every_week
      hint: Новый повод вместо «ну что, решили?». Одно напоминание через 3–5 дней — нормально.
    - type: strategy.trial_convert
      title: Предложите продолжение тем, кто был на пробной
      frequency: { times_per_week: 2 }
      minutes: 10
      when: every_week
      hint: Лучше всего — в течение 1–2 дней после пробной, пока впечатление свежее.
  intense:
    - type: strategy.follow_up
      title: Напомните о себе тем, кто замолчал
      frequency: { times_per_week: 5 }
      minutes: 10
      when: every_week
      hint: Новый повод вместо «ну что, решили?». Не отвечают дважды — оставьте в покое и отметьте в CRM.
    - type: strategy.trial_convert
      title: Предложите продолжение тем, кто был на пробной
      frequency: { times_per_week: 3 }
      minutes: 10
      when: every_week
      hint: В течение 1–2 дней после пробной. Предложите конкретный формат и два времени на выбор.
default_milestones:
  - position: 1
    title: Напоминания вошли в привычку
    week: 2
    criteria:
      - { metric: tasks_done, task_type: strategy.follow_up, min: { light: 3, moderate: 5, intense: 8 } }
  - position: 2
    title: Затухшие разговоры возобновились
    week: 4
    criteria:
      - { metric: dialogs_started, min: { light: 2, moderate: 3, intense: 5 } }
  - position: 3
    title: Разговоры доходят до следующего шага
    week: 6
    criteria:
      - { metric: dialogs_started, min: { light: 3, moderate: 5, intense: 8 } }
      - { metric: tasks_done, task_type: strategy.trial_convert, min: { light: 2, moderate: 4, intense: 6 } }
---
# Доводить разговоры до записи

**Когда применять.** Диалоги начинаются, но затухают; в CRM много контактов «в работе» без движения; часто срабатывают напоминания о забытых контактах. Диагноз: `no_follow_up`, `low_conversion`; при долгих ответах на заявки — `slow_response`.

**Почему работает.** Большая часть «не ответил» — это «отвлёкся», а не «нет». Мягкое напоминание с новым поводом возвращает разговор; предложение сразу после пробной ловит момент максимального интереса.

**Шаги.**
1. Несколько раз в неделю проходить по контактам «в работе», которые молчат больше 3–5 дней.
2. Писать с новым поводом: вопрос, полезный совет, свободное время.
3. После пробной / консультации — в течение 1–2 дней предложить конкретное продолжение.
4. После двух напоминаний без ответа — оставить в покое, отметить в CRM.

**На что смотреть.** Регулярность напоминаний, сколько контактов вернулось в разговор. Заявкам отвечать быстро — это сигналы CRM в брифе, не задачи стратегии.

**Ограничения.** Не больше двух напоминаний подряд без ответа. Не давить сроками («только сегодня»), если это неправда. Сначала — карточка `ethics-and-law`.

**Сочетается с:** `reactivate-old-base`, `warm-circle-start`, `steady-content` — как вторая часть любой стратегии, где уже есть разговоры.
