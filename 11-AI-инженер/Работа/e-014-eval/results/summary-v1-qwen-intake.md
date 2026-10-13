# E-014 strategic eval · v1-qwen-intake

Модель: `just-ai/open-router/qwen/qwen3.5-flash-02-23`

- Всего вызовов: 16
- expect OK: **87.5%**
- Сумма ₽: **0.2503**

| Агент | n | valid % | expect % | avg ms | ₽ |
|-------|---|---------|----------|--------|---|
| intake | 16 | 100.0 | 87.5 | 2559 | 0.2503 |

## Красные кейсы
- `s06_pii_phone_name` / intake: ["channels_missing_['max']"]
- `s15_complex_services` / intake: ["services_['workouts', 'nutrition', 'complex']"]
