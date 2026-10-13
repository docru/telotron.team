# E-014 strategic eval · v1_1-deepseek

Модель: `just-ai/open-router/deepseek/deepseek-v3.2`

- Всего вызовов: 45
- expect OK: **86.7%**
- Сумма ₽: **7.5618**

| Агент | n | valid % | expect % | avg ms | ₽ |
|-------|---|---------|----------|--------|---|
| decompose | 5 | 80.0 | 80.0 | 17157 | 1.4274 |
| diagnose | 11 | 100.0 | 81.8 | 14873 | 2.6019 |
| intake | 16 | 100.0 | 93.8 | 3553 | 1.3027 |
| propose | 7 | 100.0 | 85.7 | 17461 | 1.5517 |
| review | 6 | 100.0 | 83.3 | 7925 | 0.6781 |

## Красные кейсы
- run 1 · `s07_pii_multiple_names` / intake: ['old_base_None']
- run 1 · `t01_onboarding_base_untouched` / diagnose: ['fail_text_promise']
- run 1 · `t01_onboarding_base_untouched` / propose: ['fail_text_promise']
- run 1 · `t05_weak_offer` / diagnose: ['fail_text_promise']
- run 1 · `t15_review_on_track_zero_clients` / review: ['jargon']
- run 1 · `t19_decompose_light_cap` / decompose: ["invalid_json:Expecting ',' delimiter"]
