# E-014 strategic eval · v1-final-qwen

Модель: `just-ai/open-router/qwen/qwen3.5-flash-02-23`

- Всего вызовов: 88
- expect OK: **50.0%**
- Сумма ₽: **2.1696**

| Агент | n | valid % | expect % | avg ms | ₽ |
|-------|---|---------|----------|--------|---|
| decompose | 10 | 100.0 | 50.0 | 6266 | 0.3984 |
| diagnose | 20 | 100.0 | 5.0 | 4489 | 0.5628 |
| intake | 32 | 100.0 | 93.8 | 2653 | 0.5731 |
| propose | 14 | 100.0 | 7.1 | 6135 | 0.4406 |
| review | 12 | 100.0 | 58.3 | 2989 | 0.1947 |

## По прогонам

| Прогон | expect % |
|--------|----------|
| 1 | 52.3 |
| 2 | 47.7 |

## Красные кейсы
- run 1 · `s15_complex_services` / intake: ["services_['workouts', 'nutrition', 'complex']"]
- run 1 · `t01_onboarding_base_untouched` / diagnose: ['question_no_free_text_None']
- run 1 · `t01_onboarding_base_untouched` / propose: ['recommended_count_0', 'recommended_card_missing', 'jargon']
- run 1 · `t02_large_base_vk` / propose: ['fail_text_promise']
- run 1 · `t03_no_base_warm_circle` / diagnose: ['question_no_free_text_None', 'questions_key_dup']
- run 1 · `t03_no_base_warm_circle` / propose: ['recommended_count_0', 'recommended_card_missing']
- run 1 · `t04_small_base_visibility` / diagnose: ['question_no_free_text_None', 'questions_key_dup']
- run 1 · `t05_weak_offer` / diagnose: ['bottleneck_no_base_vs_profile', 'jargon', 'question_no_free_text_None', 'questions_key_dup']
- run 1 · `t05_weak_offer` / propose: ['recommended_count_0', 'recommended_card_missing', 'jargon']
- run 1 · `t06_weekly_follow_up` / diagnose: ['jargon', 'question_no_free_text_None', 'questions_key_dup']
- run 1 · `t07_weekly_load_mismatch` / diagnose: ['question_no_free_text_None', 'questions_key_dup']
- run 1 · `t08_profile_change_allowed` / diagnose: ['profile_change_field_missing', 'question_no_free_text_None', 'questions_key_dup']
- run 1 · `t09_profile_change_forbidden` / diagnose: ['jargon', 'question_no_free_text_None', 'questions_key_dup', 'weekly_no_observations']
- run 1 · `t10_final_round_no_questions` / diagnose: ['bottleneck_no_base_vs_profile']
- run 1 · `t11_propose_two_ok` / propose: ['jargon']
- run 1 · `t12_ethics_restriction` / propose: ['recommended_count_0', 'recommended_card_missing', 'jargon']
- run 1 · `t13_decompose_first_plan` / decompose: ['jargon']
- run 1 · `t14_decompose_weekly_adjust` / decompose: ['minutes_over_185']
- run 1 · `t15_review_on_track_zero_clients` / review: ['jargon']
- run 1 · `t16_review_not_failed_on_clients` / review: ['jargon']
- run 1 · `t17_decompose_intense_two_cards` / decompose: ['jargon']
- run 2 · `s15_complex_services` / intake: ["services_['workouts', 'nutrition', 'complex']"]
- run 2 · `t01_onboarding_base_untouched` / diagnose: ['question_no_free_text_None', 'questions_key_dup']
- run 2 · `t01_onboarding_base_untouched` / propose: ['recommended_count_0', 'recommended_card_missing', 'jargon']
- run 2 · `t02_large_base_vk` / diagnose: ['jargon']
- run 2 · `t02_large_base_vk` / propose: ['recommended_count_0', 'recommended_card_missing', 'jargon']
- run 2 · `t03_no_base_warm_circle` / diagnose: ['jargon', 'question_no_free_text_None', 'questions_key_dup']
- run 2 · `t03_no_base_warm_circle` / propose: ['recommended_count_0', 'recommended_card_missing', 'jargon']
- run 2 · `t04_small_base_visibility` / diagnose: ['jargon', 'question_no_free_text_None', 'questions_key_dup']
- run 2 · `t04_small_base_visibility` / propose: ['recommended_count_0', 'recommended_card_missing']
- run 2 · `t05_weak_offer` / diagnose: ['bottleneck_no_base_vs_profile', 'jargon', 'question_no_free_text_None', 'questions_key_dup']
- run 2 · `t05_weak_offer` / propose: ['jargon']
- run 2 · `t06_weekly_follow_up` / diagnose: ['jargon', 'question_no_free_text_None', 'questions_key_dup']
- run 2 · `t07_weekly_load_mismatch` / diagnose: ['jargon', 'question_no_free_text_None', 'questions_key_dup']
- run 2 · `t08_profile_change_allowed` / diagnose: ['profile_change_field_missing', 'question_no_free_text_None', 'questions_key_dup']
- run 2 · `t09_profile_change_forbidden` / diagnose: ['bottleneck_no_base_vs_profile', 'question_no_free_text_None', 'questions_key_dup', 'weekly_no_observations']
- run 2 · `t10_final_round_no_questions` / diagnose: ['bottleneck_no_base_vs_profile']
- run 2 · `t11_propose_two_ok` / propose: ['recommended_count_0', 'recommended_card_missing', 'jargon']
- run 2 · `t12_ethics_restriction` / propose: ['recommended_count_0', 'recommended_card_missing', 'jargon']
- run 2 · `t13_decompose_first_plan` / decompose: ['jargon']
- run 2 · `t15_review_on_track_zero_clients` / review: ['jargon']
- run 2 · `t16_review_not_failed_on_clients` / review: ['jargon']
- run 2 · `t17_decompose_intense_two_cards` / decompose: ['jargon']
- run 2 · `t23_review_with_clients` / review: ['jargon']
