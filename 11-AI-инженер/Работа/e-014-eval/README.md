# E-014 · Проверочный набор стратегического слоя v1

| Поле | Значение |
|------|----------|
| **Волна** | [e-014-volna-4-strategicheskiy-sloy.md](../e-014-volna-4-strategicheskiy-sloy.md) шаг 3 |
| **Промпты** | [e-014-prompts/](../e-014-prompts/) |
| **Схемы** | [e-014-schemas/](../e-014-schemas/) |
| **Проверки** | [e-014-volna-4-proverki.md](../e-014-volna-4-proverki.md) |
| **Статус** | вымышленные кейсы; реальные обезличенные — после пилота |

## Файлы

| Файл | Что |
|------|-----|
| `stories_set.py` → `stories-v1.json` | 16 рассказов для `intake_extract` |
| `trainers_set.py` → `trainers-v1.json` | 24 тренера для diagnose / propose / decompose / review |
| `knowledge_stub.py` | урезанные карточки для входа Стратега; `default_tasks` для Декомпозера читаются из `../e-014-kartochki` |
| `run_strategic_eval.py` | прогон: `--runs`, `--workers`, `--agents`, `--reasoning-off`, `--no-schema`; схема вопросов Диагноста собирается под запрос |
| `rescore.py` | переоценка сохранённых `results/run-<tag>.json` по текущим проверкам, без вызова моделей |

Пересборка JSON:

```bash
cd …/e-014-eval && python3 stories_set.py && python3 trainers_set.py
```

## Покрытие рассказов

| Тема | Кейсы |
|------|-------|
| Полный ясный рассказ | s01, s02 |
| Мало данных → много `unclear` | s03, s04 |
| Противоречие | s05 |
| Чужие ПДн в тексте (имена, телефон) — не должны попасть в ответ | s06, s07, s08 |
| База none / lt10 / 10_30 / gt30 | s01, s09, s10, s02 |
| Разные каналы и offer | s11–s14 |
| Питание / комплекс | s15, s16 |

## Покрытие тренеров

| Тема | Кейсы |
|------|-------|
| Онбординг, база не тронута | t01, t02 |
| Нет базы → тёплый круг / контент | t03, t04 |
| Слабое предложение | t05 |
| Неделя: follow-up, load mismatch | t06, t07 |
| Правка анкеты (есть / нет флагов) | t08, t09 |
| final_round без вопросов | t10 |
| Стратег: 2 vs 3, restriction | t11, t12 |
| Декомпозер first / weekly + потолок минут | t13, t14 |
| Монитор: on_track при 0 клиентов; не failed из‑за клиентов | t15, t16 |
| Декомпозер: intense / две карточки, weekly continue, light — потолок 100 | t17, t18, t19 |
| Монитор: too_early, behind / adjust, задачи сделаны — результатов нет, есть клиенты (показать) | t20, t21, t22, t23 |
| Пустые поля анкеты → вопросы только по `askable_fields` | t24 |

Общие проверки на всех ответах (не зависят от кейса): обещания, жаргон, «клиентов: 0», формат вопросов D5–D7, вопросы по заполненным полям, коды узких мест против анкеты, наблюдения на совещании, правки анкеты без флага, «Тренер…» вместо «вы». Стоп-слова — с учётом отрицания.

## Поля `expect` (код прогона, шаг 4)

**stories:** `must_set`, `must_unclear`, `must_not_contain` (подстроки в about/offer_note/specialization), `services_any`, `old_base_size`, …

**diagnose:** `data_quality_any`, `bottleneck_any`, `questions_max`, `questions_forbidden` (final_round), `profile_change_empty`, `no_client_zero_phrase`

**propose:** `strategies_min/max`, `recommended_cards_any`, `forbidden_card_keys`

**decompose:** `items_max`, `types_only_from`, `minutes_cap`, `milestones_min` (first_plan)

**review:** `status_any`, `recommendation_any`, `forbid_failed_if`, `no_client_zero_phrase`

Все кейсы — вымысел, без реальных ПДн пилота.

## Прогон (шаг 4)

```bash
python3 run_strategic_eval.py --model just-ai/openai-proxy/gpt-4o-mini --tag v1_1-gpt4omini --runs 3 --workers 6
python3 run_strategic_eval.py --model just-ai/open-router/deepseek/deepseek-v3.2 --tag v1_1-deepseek
python3 run_strategic_eval.py --model just-ai/open-router/qwen/qwen3.5-flash-02-23 --tag v1_1-qwen --reasoning-off
python3 rescore.py v1_1-gpt4omini v1_1-deepseek   # после правки проверок
```

Нужен сетевой доступ к Caila; ключ читается из `_telotron.ru/.env` и никуда не пишется.

Отчёт: [e-014-strategic-eval-v1.md](../e-014-strategic-eval-v1.md).
