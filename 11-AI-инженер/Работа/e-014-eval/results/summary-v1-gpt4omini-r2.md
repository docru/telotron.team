# E-014 strategic eval · v1-gpt4omini-r2

Модель: `just-ai/openai-proxy/gpt-4o-mini`

- Всего вызовов: 37
- expect OK: **81.1%**
- Сумма ₽: **1.5473**

| Агент | n | valid % | expect % | avg ms | ₽ |
|-------|---|---------|----------|--------|---|
| decompose | 2 | 100.0 | 100.0 | 3076 | 0.1004 |
| diagnose | 10 | 100.0 | 50.0 | 3414 | 0.5203 |
| intake | 16 | 100.0 | 87.5 | 1667 | 0.4951 |
| propose | 7 | 100.0 | 100.0 | 4541 | 0.381 |
| review | 2 | 100.0 | 100.0 | 1782 | 0.0505 |

## Красные кейсы
- `s05_contradiction_base` / intake: ['unclear_missing_old_base_size']
- `s06_pii_phone_name` / intake: ["channels_missing_['max']"]
- `t06_weekly_follow_up` / diagnose: ['observation_topic_missing']
- `t07_weekly_load_mismatch` / diagnose: ['observation_topic_missing', 'fail_text_promise']
- `t08_profile_change_allowed` / diagnose: ['fail_text_promise']
- `t09_profile_change_forbidden` / diagnose: ['fail_text_promise']
- `t10_final_round_no_questions` / diagnose: ['fail_text_promise']
