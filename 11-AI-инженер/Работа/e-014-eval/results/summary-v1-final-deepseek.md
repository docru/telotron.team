# E-014 strategic eval · v1-final-deepseek

Модель: `just-ai/open-router/deepseek/deepseek-v3.2`

- Всего вызовов: 88
- expect OK: **59.1%**
- Сумма ₽: **13.7813**

| Агент | n | valid % | expect % | avg ms | ₽ |
|-------|---|---------|----------|--------|---|
| decompose | 10 | 90.0 | 90.0 | 12186 | 2.5376 |
| diagnose | 20 | 100.0 | 35.0 | 15707 | 4.3959 |
| intake | 32 | 100.0 | 93.8 | 3584 | 2.4377 |
| propose | 14 | 100.0 | 0.0 | 16383 | 3.1239 |
| review | 12 | 100.0 | 50.0 | 7149 | 1.2862 |

## По прогонам

| Прогон | expect % |
|--------|----------|
| 1 | 54.5 |
| 2 | 63.6 |

## Красные кейсы
- run 1 · `s07_pii_multiple_names` / intake: ['old_base_None']
- run 1 · `t01_onboarding_base_untouched` / diagnose: ['jargon']
- run 1 · `t01_onboarding_base_untouched` / propose: ['jargon']
- run 1 · `t02_large_base_vk` / diagnose: ['jargon', 'question_no_free_text_base_contact_history']
- run 1 · `t02_large_base_vk` / propose: ['jargon']
- run 1 · `t03_no_base_warm_circle` / propose: ['jargon']
- run 1 · `t04_small_base_visibility` / propose: ['jargon']
- run 1 · `t05_weak_offer` / diagnose: ['fail_text_promise']
- run 1 · `t05_weak_offer` / propose: ['jargon']
- run 1 · `t06_weekly_follow_up` / diagnose: ['jargon']
- run 1 · `t07_weekly_load_mismatch` / diagnose: ['question_no_free_text_base_contact_plan', 'question_no_free_text_content_focus']
- run 1 · `t08_profile_change_allowed` / diagnose: ['jargon', 'question_no_free_text_base_contact_recent', 'question_no_free_text_content_type']
- run 1 · `t09_profile_change_forbidden` / diagnose: ['question_no_free_text_base_contact_attempt', 'question_no_free_text_tg_activity_type']
- run 1 · `t10_final_round_no_questions` / diagnose: ['jargon']
- run 1 · `t11_propose_two_ok` / propose: ['jargon']
- run 1 · `t12_ethics_restriction` / propose: ['jargon']
- run 1 · `t13_decompose_first_plan` / decompose: ["invalid_json:Expecting ',' delimiter"]
- run 1 · `t16_review_not_failed_on_clients` / review: ['jargon']
- run 1 · `t22_review_done_no_results` / review: ['jargon']
- run 1 · `t23_review_with_clients` / review: ['jargon']
- run 2 · `s07_pii_multiple_names` / intake: ['old_base_None']
- run 2 · `t01_onboarding_base_untouched` / propose: ['jargon']
- run 2 · `t02_large_base_vk` / propose: ['jargon']
- run 2 · `t03_no_base_warm_circle` / diagnose: ['question_no_free_text_tg_activity_type']
- run 2 · `t03_no_base_warm_circle` / propose: ['jargon']
- run 2 · `t04_small_base_visibility` / propose: ['jargon']
- run 2 · `t05_weak_offer` / diagnose: ['fail_text_promise', 'question_no_free_text_base_contact_recent']
- run 2 · `t05_weak_offer` / propose: ['jargon']
- run 2 · `t07_weekly_load_mismatch` / diagnose: ['question_no_free_text_base_contact_recent', 'question_no_free_text_content_type']
- run 2 · `t08_profile_change_allowed` / diagnose: ['question_no_free_text_base_contact_attempt', 'question_no_free_text_content_focus']
- run 2 · `t10_final_round_no_questions` / diagnose: ['jargon']
- run 2 · `t11_propose_two_ok` / propose: ['jargon']
- run 2 · `t12_ethics_restriction` / propose: ['jargon']
- run 2 · `t15_review_on_track_zero_clients` / review: ['jargon']
- run 2 · `t16_review_not_failed_on_clients` / review: ['jargon']
- run 2 · `t23_review_with_clients` / review: ['jargon']
