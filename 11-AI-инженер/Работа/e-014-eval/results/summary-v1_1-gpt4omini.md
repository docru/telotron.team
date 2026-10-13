# E-014 strategic eval · v1_1-gpt4omini

Модель: `just-ai/openai-proxy/gpt-4o-mini`

- Всего вызовов: 135
- expect OK: **97.8%**
- Сумма ₽: **6.9072**

| Агент | n | valid % | expect % | avg ms | ₽ |
|-------|---|---------|----------|--------|---|
| decompose | 15 | 100.0 | 100.0 | 4348 | 0.9846 |
| diagnose | 33 | 100.0 | 100.0 | 3573 | 2.3783 |
| intake | 48 | 100.0 | 93.8 | 1817 | 1.8001 |
| propose | 21 | 100.0 | 100.0 | 4531 | 1.22 |
| review | 18 | 100.0 | 100.0 | 2002 | 0.5242 |

## По прогонам

| Прогон | expect % |
|--------|----------|
| 1 | 97.8 |
| 2 | 97.8 |
| 3 | 97.8 |

## Красные кейсы
- run 1 · `s05_contradiction_base` / intake: ['unclear_missing_old_base_size']
- run 2 · `s05_contradiction_base` / intake: ['unclear_missing_old_base_size']
- run 3 · `s05_contradiction_base` / intake: ['unclear_missing_old_base_size']
