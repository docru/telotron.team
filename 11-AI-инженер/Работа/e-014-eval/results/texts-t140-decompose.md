# Тексты для ручного просмотра · t140-decompose

## t13_decompose_first_plan · decompose

```json
{
 "plan_rationale": "Этот план на первую неделю направлен на создание базы бывших клиентов и начало общения с ними. Важно внести контакты в CRM и начать диалог, чтобы установить связь и вернуть интерес к тренировкам.",
 "items": [
  {
   "key": "collect_five_clients",
   "type": "strategy.base_collect",
   "title": "Внесите в CRM 5 бывших клиентов",
   "frequency": {
    "kind": "once",
    "times_per_week": null
   },
   "minutes": 15,
   "milestone_position": 1,
   "hint": "Начните с тех, с кем расстались хорошо и кто занимался дольше месяца. Телефон или ник в соцсети — достаточно."
  },
  {
   "key": "collect_three_more_clients",
   "type": "strategy.base_collect",
   "title": "Добавьте в CRM ещё 3 бывших клиента",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 1
   },
   "minutes": 10,
   "milestone_position": 3,
   "hint": "Список должен расти вместе с сообщениями — иначе к 3–4 неделе писать будет некому."
  },
  {
   "key": "reactivate_three_clients",
   "type": "strategy.base_reactivate",
   "title": "Напишите 3 людям из старой базы за неделю",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 1
   },
   "minutes": 25,
   "milestone_position": 2,
   "hint": "Пишите лично, не рассылкой. Спросите, как дела, и одной фразой скажите, чем вы сейчас занимаетесь."
  },
  {
   "key": "follow_up_no_response",
   "type": "strategy.follow_up",
   "title": "Напомните о себе тем, кто не ответил",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 1
   },
   "minutes": 10,
   "milestone_position": null,
   "hint": "Одно напоминание через 3–5 дней — нормально. Если снова тишина, больше не пишите."
  }
 ]
}
```

## t14_decompose_weekly_adjust · decompose

```json
{
 "plan_rationale": "На этой неделе мы сосредоточимся на активном взаимодействии с бывшими клиентами, добавляя новых в CRM и напоминая о себе тем, кто не ответил. Это поможет увеличить шансы на возвращение клиентов и повысит активность в общении.",
 "items": [
  {
   "key": "add_clients_to_crm",
   "type": "strategy.base_collect",
   "title": "Добавьте в CRM ещё 3 бывших клиента",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 1
   },
   "minutes": 10,
   "milestone_position": 1,
   "hint": "Список должен расти вместе с сообщениями — иначе к 3–4 неделе писать будет некому."
  },
  {
   "key": "message_old_clients",
   "type": "strategy.base_reactivate",
   "title": "Напишите 3 людям из старой базы за неделю",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 1
   },
   "minutes": 25,
   "milestone_position": 1,
   "hint": "Пишите лично, не рассылкой. Спросите, как дела, и одной фразой скажите, чем вы сейчас занимаетесь."
  },
  {
   "key": "follow_up_no_response",
   "type": "strategy.follow_up",
   "title": "Напомните о себе тем, кто не ответил",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 1
   },
   "minutes": 10,
   "milestone_position": 1,
   "hint": "Одно напоминание через 3–5 дней — нормально. Если снова тишина, больше не пишите."
  }
 ]
}
```

## t17_decompose_intense_two_cards · decompose

```json
{
 "plan_rationale": "На этой неделе важно создать базу для работы и привлечь внимание знакомых к вашим услугам. Это поможет установить контакт и начать получать заявки на тренировки.",
 "items": [
  {
   "key": "social_profile_setup",
   "type": "strategy.social_profile",
   "title": "Оформите профиль в соцсети: кто вы и как записаться",
   "frequency": {
    "kind": "once",
    "times_per_week": null
   },
   "minutes": 20,
   "milestone_position": 1,
   "hint": "В первой строке — для кого вы и с чем помогаете. Ссылка на запись — в шапке."
  },
  {
   "key": "content_post_announcement",
   "type": "strategy.content_post",
   "title": "Расскажите в личной соцсети, что теперь ведёте тренировки",
   "frequency": {
    "kind": "once",
    "times_per_week": null
   },
   "minutes": 30,
   "milestone_position": 1,
   "hint": "Для кого вы, с чем помогаете, как записаться. Один пост или история в начале — самый заметный шаг."
  },
  {
   "key": "crm_initial_collect",
   "type": "strategy.base_collect",
   "title": "Внесите в CRM 15 знакомых, кому может быть интересно",
   "frequency": {
    "kind": "once",
    "times_per_week": null
   },
   "minutes": 25,
   "milestone_position": 1,
   "hint": "Друзья, коллеги, знакомые по залу, родители из школы — все, кто знает вас лично."
  },
  {
   "key": "link_share_profile",
   "type": "strategy.link_share",
   "title": "Поставьте ссылку на запись в профиль и подпись сообщений",
   "frequency": {
    "kind": "once",
    "times_per_week": null
   },
   "minutes": 10,
   "milestone_position": 1,
   "hint": "Человек, которому интересно, должен записаться в один клик."
  },
  {
   "key": "offer_setup",
   "type": "strategy.offer_setup",
   "title": "Сформулируйте предложение и проверьте страницу записи",
   "frequency": {
    "kind": "once",
    "times_per_week": null
   },
   "minutes": 30,
   "milestone_position": 1,
   "hint": "Одна фраза: для кого → что получит → как начать. Пройдите запись сами с телефона."
  }
 ]
}
```

## t18_decompose_weekly_continue · decompose

```json
{
 "plan_rationale": "На этой неделе мы продолжим активно публиковать контент в социальных сетях, чтобы поддерживать интерес к вашим услугам и привлекать новых клиентов. Учитывая высокую степень выполнения предыдущего плана, мы сосредоточимся на регулярных публикациях и взаимодействии с сообществом.",
 "items": [
  {
   "key": "content_post_1",
   "type": "strategy.content_post",
   "title": "Опубликуйте пост",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 2
   },
   "minutes": 30,
   "milestone_position": null,
   "hint": "Чередуйте пользу и себя — сегодня совет, в следующий раз история клиента (с согласия) или как вы работаете."
  },
  {
   "key": "content_short_1",
   "type": "strategy.content_short",
   "title": "Выложите короткую историю",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 2
   },
   "minutes": 10,
   "milestone_position": null,
   "hint": "Фото или кружок и одна фраза. Регулярность важнее красоты."
  },
  {
   "key": "community_engage_1",
   "type": "strategy.community_engage",
   "title": "Ответьте на вопрос в тематическом или местном чате",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 1
   },
   "minutes": 15,
   "milestone_position": null,
   "hint": "Помогите по существу, без рекламы. Ссылка на себя — только если правила чата разрешают."
  }
 ]
}
```

## t19_decompose_light_cap · decompose

```json
{
 "plan_rationale": "Этот план на первую неделю поможет заложить основу для работы с бывшими клиентами. Внесение клиентов в CRM и активные сообщения помогут восстановить связь и увеличить шансы на возвращение.",
 "items": [
  {
   "key": "add_old_clients_crm",
   "type": "strategy.base_collect",
   "title": "Внесите в CRM 5 бывших клиентов",
   "frequency": {
    "kind": "once",
    "times_per_week": null
   },
   "minutes": 15,
   "milestone_position": 1,
   "hint": "Начните с тех, с кем расстались хорошо и кто занимался дольше месяца. Телефон или ник в соцсети — достаточно."
  },
  {
   "key": "add_more_old_clients_crm",
   "type": "strategy.base_collect",
   "title": "Добавьте в CRM ещё 3 бывших клиента",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 1
   },
   "minutes": 10,
   "milestone_position": null,
   "hint": "Список должен расти вместе с сообщениями — иначе к 3–4 неделе писать будет некому."
  },
  {
   "key": "message_old_clients",
   "type": "strategy.base_reactivate",
   "title": "Напишите 3 людям из старой базы за неделю",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 1
   },
   "minutes": 25,
   "milestone_position": null,
   "hint": "Пишите лично, не рассылкой. Спросите, как дела, и одной фразой скажите, чем вы сейчас занимаетесь."
  },
  {
   "key": "remind_nonresponders",
   "type": "strategy.follow_up",
   "title": "Напомните о себе тем, кто не ответил",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 1
   },
   "minutes": 10,
   "milestone_position": null,
   "hint": "Одно напоминание через 3–5 дней — нормально. Если снова тишина, больше не пишите."
  },
  {
   "key": "remind_silent_clients",
   "type": "strategy.follow_up",
   "title": "Напомните о себе тем, кто замолчал",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 2
   },
   "minutes": 10,
   "milestone_position": null,
   "hint": "Пишите с новым поводом: вопрос, полезный совет, свободное время на этой неделе."
  },
  {
   "key": "offer_trial_followup",
   "type": "strategy.trial_convert",
   "title": "Предложите продолжение тем, кто был на пробной",
   "frequency": {
    "kind": "times_per_week",
    "times_per_week": 1
   },
   "minutes": 10,
   "milestone_position": null,
   "hint": "Напомните, что получилось на пробной, и предложите конкретный формат и время."
  }
 ]
}
```
