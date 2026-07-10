# Разработка · сборка маркетинговых материалов

Скрипты, временные каталоги `.build-*` и артефакты `.docx`. **PDF для отправки** попадают в [Готовые документы/](../Готовые%20документы/).

| Каталог | Скрипт | Результат |
|---------|--------|-----------|
| [презентация/](презентация/) | `build-presentation-pdf.py` | `Готовые документы/Презентация … v1.3.pdf` |
| [онбординг/](онбординг/) | `build-onboarding-docx.py` | `Готовые документы/Онбординг … .pdf` |
| [one-pager-investor/](one-pager-investor/) | `build-one-pager-pdf.py` | `Готовые документы/Telotron — one-pager … .pdf`, `… 3 страницы.pdf` |

## Зависимости

`pandoc`, `imagemagick` (`convert`), LibreOffice (`soffice`).

## Примеры

```bash
cd презентация && python3 build-presentation-pdf.py
cd ../онбординг && python3 build-onboarding-docx.py
cd ../one-pager-investor && python3 build-one-pager-pdf.py --all
```

Исходники markdown: [Инструкции/](../Инструкции/). Скрины: [Инструкции/скрины/](../Инструкции/скрины/).
