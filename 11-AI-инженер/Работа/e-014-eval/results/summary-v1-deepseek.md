# E-014 strategic eval · v1-deepseek

Модель: `just-ai/open-router/deepseek/deepseek-v3.2`

- Всего вызовов: 37
- expect OK: **83.8%**
- Сумма ₽: **5.4547**

| Агент | n | valid % | expect % | avg ms | ₽ |
|-------|---|---------|----------|--------|---|
| decompose | 2 | 100.0 | 100.0 | 11306 | 0.3937 |
| diagnose | 10 | 90.0 | 60.0 | 20094 | 1.817 |
| intake | 16 | 100.0 | 87.5 | 3234 | 1.2483 |
| propose | 7 | 100.0 | 100.0 | 19975 | 1.7663 |
| review | 2 | 100.0 | 100.0 | 7854 | 0.2294 |

## Красные кейсы
- `s06_pii_phone_name` / intake: ["channels_missing_['max']"]
- `s14_goal_explicit` / intake: ['old_base_lt10']
- `t02_large_base_vk` / diagnose: ['fail_text_promise']
- `t03_no_base_warm_circle` / diagnose: ['fail_text_promise']
- `t06_weekly_follow_up` / diagnose: ['fail_text_promise']
- `t08_profile_change_allowed` / diagnose: ['RemoteDisconnected: Remote end closed connection without response']
