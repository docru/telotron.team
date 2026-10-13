# E-014 strategic eval · v1-gpt4omini

Модель: `just-ai/openai-proxy/gpt-4o-mini`

- Всего вызовов: 37
- expect OK: **27.0%**
- Сумма ₽: **0.6707**

| Агент | n | valid % | expect % | avg ms | ₽ |
|-------|---|---------|----------|--------|---|
| decompose | 2 | 100.0 | 100.0 | 3531 | 0.1072 |
| diagnose | 10 | 100.0 | 60.0 | 3245 | 0.5117 |
| intake | 16 | 0.0 | 0.0 | 760 | 0 |
| propose | 7 | 0.0 | 0.0 | 832 | 0 |
| review | 2 | 100.0 | 100.0 | 1861 | 0.0518 |

## Красные кейсы
- `s01_clear_base_mid` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s02_clear_large_base_urgent` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s03_sparse` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s04_only_niche` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s05_contradiction_base` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s06_pii_phone_name` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s07_pii_multiple_names` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s08_pii_email_nick` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s09_no_base_start` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s10_small_base` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s11_multi_channel_unclear_primary` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s12_consultation_offer` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s13_hours_lt2` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s14_goal_explicit` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s15_complex_services` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `s16_ambiguous_hours` / intake: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_intake_extract\': In context=(\'properties\', \'services\'), \'uniqueItems\' is not permitted."}']
- `t01_onboarding_base_untouched` / propose: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_propose\': In context=(\'properties\', \'strategies\', \'items\', \'properties\', \'knowledge_card_keys\'), \'uniqueItems\' is not permitted."}']
- `t02_large_base_vk` / propose: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_propose\': In context=(\'properties\', \'strategies\', \'items\', \'properties\', \'knowledge_card_keys\'), \'uniqueItems\' is not permitted."}']
- `t03_no_base_warm_circle` / propose: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_propose\': In context=(\'properties\', \'strategies\', \'items\', \'properties\', \'knowledge_card_keys\'), \'uniqueItems\' is not permitted."}']
- `t04_small_base_visibility` / propose: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_propose\': In context=(\'properties\', \'strategies\', \'items\', \'properties\', \'knowledge_card_keys\'), \'uniqueItems\' is not permitted."}']
- `t05_weak_offer` / propose: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_propose\': In context=(\'properties\', \'strategies\', \'items\', \'properties\', \'knowledge_card_keys\'), \'uniqueItems\' is not permitted."}']
- `t06_weekly_follow_up` / diagnose: ['observation_topic_missing']
- `t07_weekly_load_mismatch` / diagnose: ['observation_topic_missing', 'fail_text_promise']
- `t08_profile_change_allowed` / diagnose: ['fail_text_promise']
- `t10_final_round_no_questions` / diagnose: ['fail_text_promise']
- `t11_propose_two_ok` / propose: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_propose\': In context=(\'properties\', \'strategies\', \'items\', \'properties\', \'knowledge_card_keys\'), \'uniqueItems\' is not permitted."}']
- `t12_ethics_restriction` / propose: ['http_400: {"code":"mlp.open.ai.bad.request","message":"Bad request Invalid schema for response_format \'strategic_propose\': In context=(\'properties\', \'strategies\', \'items\', \'properties\', \'knowledge_card_keys\'), \'uniqueItems\' is not permitted."}']
