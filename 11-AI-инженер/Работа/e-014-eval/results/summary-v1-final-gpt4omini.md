# E-014 strategic eval · v1-final-gpt4omini

Модель: `just-ai/openai-proxy/gpt-4o-mini`

- Всего вызовов: 132
- expect OK: **67.4%**
- Сумма ₽: **6.1707**

| Агент | n | valid % | expect % | avg ms | ₽ |
|-------|---|---------|----------|--------|---|
| decompose | 15 | 100.0 | 100.0 | 4747 | 1.0122 |
| diagnose | 30 | 100.0 | 40.0 | 4147 | 1.8648 |
| intake | 48 | 100.0 | 87.5 | 1859 | 1.6618 |
| propose | 21 | 100.0 | 23.8 | 4519 | 1.1521 |
| review | 18 | 100.0 | 83.3 | 2021 | 0.4799 |

## По прогонам

| Прогон | expect % |
|--------|----------|
| 1 | 63.6 |
| 2 | 70.5 |
| 3 | 68.2 |

## Красные кейсы
- run 1 · `s05_contradiction_base` / intake: ['unclear_missing_old_base_size']
- run 1 · `s14_goal_explicit` / intake: ['old_base_lt10']
- run 1 · `t01_onboarding_base_untouched` / diagnose: ['question_no_free_text_old_base_size']
- run 1 · `t01_onboarding_base_untouched` / propose: ['jargon']
- run 1 · `t02_large_base_vk` / diagnose: ['question_free_text_with_field_channels']
- run 1 · `t02_large_base_vk` / propose: ['jargon']
- run 1 · `t03_no_base_warm_circle` / propose: ['jargon']
- run 1 · `t04_small_base_visibility` / diagnose: ['question_free_text_with_field_channels']
- run 1 · `t05_weak_offer` / diagnose: ['question_free_text_with_field_offer', 'question_options_not_allowed_offer']
- run 1 · `t05_weak_offer` / propose: ['jargon']
- run 1 · `t06_weekly_follow_up` / diagnose: ['jargon', 'question_options_not_allowed_urgency']
- run 1 · `t07_weekly_load_mismatch` / diagnose: ['question_options_not_allowed_urgency']
- run 1 · `t08_profile_change_allowed` / diagnose: ['question_no_free_text_offer', 'question_no_free_text_urgency']
- run 1 · `t09_profile_change_forbidden` / diagnose: ['question_free_text_with_field_channels', 'question_free_text_with_field_urgency', 'question_options_not_allowed_channels', 'question_options_not_allowed_urgency']
- run 1 · `t11_propose_two_ok` / propose: ['jargon']
- run 1 · `t22_review_done_no_results` / review: ['jargon']
- run 2 · `s05_contradiction_base` / intake: ['unclear_missing_old_base_size']
- run 2 · `s14_goal_explicit` / intake: ['old_base_lt10']
- run 2 · `t01_onboarding_base_untouched` / diagnose: ['question_options_not_allowed_old_base_size']
- run 2 · `t01_onboarding_base_untouched` / propose: ['jargon']
- run 2 · `t02_large_base_vk` / propose: ['jargon']
- run 2 · `t03_no_base_warm_circle` / propose: ['jargon']
- run 2 · `t04_small_base_visibility` / propose: ['jargon']
- run 2 · `t05_weak_offer` / propose: ['jargon']
- run 2 · `t06_weekly_follow_up` / diagnose: ['jargon']
- run 2 · `t07_weekly_load_mismatch` / diagnose: ['question_options_not_allowed_channels', 'question_options_not_allowed_offer', 'question_options_not_allowed_urgency']
- run 2 · `t08_profile_change_allowed` / diagnose: ['question_options_not_allowed_channels', 'question_options_not_allowed_offer', 'question_options_not_allowed_urgency']
- run 2 · `t09_profile_change_forbidden` / diagnose: ['question_free_text_with_field_channels', 'question_options_not_allowed_channels']
- run 2 · `t11_propose_two_ok` / propose: ['jargon']
- run 3 · `s05_contradiction_base` / intake: ['unclear_missing_old_base_size']
- run 3 · `s14_goal_explicit` / intake: ['old_base_lt10']
- run 3 · `t01_onboarding_base_untouched` / propose: ['jargon']
- run 3 · `t02_large_base_vk` / diagnose: ['question_options_not_allowed_offer', 'question_options_not_allowed_old_base_size']
- run 3 · `t02_large_base_vk` / propose: ['jargon']
- run 3 · `t03_no_base_warm_circle` / propose: ['jargon']
- run 3 · `t05_weak_offer` / diagnose: ['question_options_not_allowed_offer']
- run 3 · `t05_weak_offer` / propose: ['jargon']
- run 3 · `t06_weekly_follow_up` / diagnose: ['jargon', 'question_no_free_text_follow_up_experience']
- run 3 · `t08_profile_change_allowed` / diagnose: ['jargon', 'question_free_text_with_field_channels']
- run 3 · `t09_profile_change_forbidden` / diagnose: ['question_free_text_with_field_channels', 'question_options_not_allowed_channels']
- run 3 · `t11_propose_two_ok` / propose: ['jargon']
- run 3 · `t21_review_behind_low_done` / review: ['jargon']
- run 3 · `t22_review_done_no_results` / review: ['jargon']
