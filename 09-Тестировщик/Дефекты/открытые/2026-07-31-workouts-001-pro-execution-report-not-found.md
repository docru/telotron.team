# Pro: отчёт о выполнении тренировки — «Ресурс не найден»

**Статус:** fixed  
**Приоритет:** high  
**Зона:** Pro  
**Модуль:** workouts  
**Назначено:** —  
**Issue:** —  
**Связи:** E2E `e2e/specs/workouts-v2.flow.spec.ts` → `pro sees completed execution with plan vs fact` / `e2e/fixtures/workouts.ts` `proVerifyTrainerReport` / commit `95e995d`

---

## Окружение

- Стенд: локально `*.telotron.test` (Docker Sail)
- Ветка / commit: `95e995d` (на момент прогона 2026-07-31)
- Браузер: Playwright Chromium (project `flow`)

## Предусловия

1. E2E Trainer / E2E Client из `E2eSeeder`.
2. Pro создал упражнение и шаблон, назначил клиенту (`workouts-v2` шаги 1–2).
3. Client выполнил тренировку до 100% (шаг 2 зелёный).

## Шаги

1. Открыть hub клиента: `/workspace/clients/{id}?section=workouts&sub=calendar`.
2. Кликнуть событие выполнения с именем шаблона `E2E Workout …`.
3. В диалоге ожидать детали упражнения (имя упражнения, «Подход 1», «План:» / «Факт:»).

## Ожидалось

Диалог показывает plan vs fact по подходам упражнения из шаблона (имя упражнения, план и факт).

## Фактически

Диалог открывается с заголовком клиента и названием шаблона (`E2E Workout …`, «Выполнение: 100%»), но вместо деталей — текст **«Ресурс не найден.»**  
E2E: `expect(dialog.getByText(exerciseName)).toBeVisible()` → timeout.

Артефакт: `e2e/test-results/workouts-v2.flow-E2E-Worko-229e6-execution-with-plan-vs-fact-flow/error-context.md`

## Дополнительно

- Шаги 1–2 того же serial-сценария проходят — назначение и выполнение на Client ок.
- Похоже на 404 при подгрузке execution/report payload в lightbox/dialog Pro (не на устаревший селектор: exercise name отсутствует в DOM, зато есть явная ошибка продукта).
- Автотест **не ослаблять**: ожидание plan/fact корректно относительно ТЗ offline/workouts report.

## История

| Дата | Кто | Комментарий |
|------|-----|-------------|
| 2026-07-31 | QA | заведён после полного прогона; тесты календаря/регистрации починены отдельно |
| 2026-07-31 | dev | fixed: в `ClientFeedCalendar` снова объявлен prop `trackedClientUserId` (регрессия T-101 `60ef1dd`); без него Pro ходил в Client `/me/…` → 404 «Ресурс не найден.» |
