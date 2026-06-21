#!/usr/bin/env python3
"""Сборка xlsx «Юнит-экономика — руководитель партнёрской сети» (stdlib, без openpyxl)."""

from __future__ import annotations

import zipfile
from pathlib import Path

OUT = Path(__file__).with_name(
    "Юнит-экономика — руководитель партнёрской сети.xlsx"
)


def col_letter(n: int) -> str:
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


Cell = tuple[str | None, str | None]  # (value, formula)


def sheet_xml(rows: dict[int, dict[int, Cell]]) -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
        "<sheetData>",
    ]
    for r in sorted(rows):
        parts.append(f'<row r="{r}">')
        for c in sorted(rows[r]):
            ref = f"{col_letter(c)}{r}"
            val, formula = rows[r][c]
            if formula:
                parts.append(f'<c r="{ref}"><f>{formula}</f></c>')
            elif val is None:
                continue
            elif val.replace(".", "", 1).replace("-", "", 1).isdigit():
                parts.append(f'<c r="{ref}"><v>{val}</v></c>')
            else:
                parts.append(
                    f'<c r="{ref}" t="inlineStr"><is><t>{esc(val)}</t></is></c>'
                )
        parts.append("</row>")
    parts.extend(["</sheetData>", "</worksheet>"])
    return "".join(parts)


def build_model_sheet() -> str:
    """Лист «Модель» — один сценарий, все формулы."""
    r: dict[int, dict[int, Cell]] = {}

    def put(row: int, col: int, val: str | None = None, formula: str | None = None) -> None:
        r.setdefault(row, {})[col] = (val, formula)

    # A — подписи, B — значения/формулы
    put(1, 1, "Юнит-экономика Telotron · руководитель партнёрской сети")
    put(2, 1, "Маржа компании = MRR − выплаты L1/L2/L3 − % руководителю (из маржи, не из % тренеров)")
    put(3, 1, "Комиссия эквайринга/topup и payout — cost компании (не удерживается с партнёра, partner-модуль-тз-mvp §7.3)")

    put(4, 1, "1. ТАРИФЫ И СТАВКИ ПАРТНЁРКИ")
    put(5, 1, "Цена Профи, ₽/мес")
    put(5, 2, "5000")
    put(6, 1, "Цена Максимальный, ₽/мес")
    put(6, 2, "10000")
    put(7, 1, "Доля L1 от базы пополнения")
    put(7, 2, "0.2")
    put(8, 1, "Доля L2 (от базы L2-уровня)")
    put(8, 2, "0.05")
    put(9, 1, "Доля L3 (от базы L3-уровня)")
    put(9, 2, "0.025")

    put(11, 1, "2. МАСШТАБ (ввод)")
    put(12, 1, "Всего платящих тренеров")
    put(12, 2, "100")
    put(13, 1, "Доля платящих через партнёрскую сеть (0–1)")
    put(13, 2, "0.7")
    put(14, 1, "Доля Профи среди платящих (0–1)")
    put(14, 2, "0.85")
    put(15, 1, "Доля Макс среди платящих (0–1)")
    put(15, 2, "0.15")
    put(16, 1, "Партнёров с договором (L3)")
    put(16, 2, "10")
    put(17, 1, "Ср. платящих L1 на партнёра")
    put(17, 2, "6")
    put(18, 1, "Всего платящих на уровне L2 (в сети)")
    put(18, 2, "15")
    put(19, 1, "Всего платящих на уровне L3 (в сети)")
    put(19, 2, "5")
    put(20, 1, "Ср. абонплата партнёра, ₽ (обычно Профи)")
    put(20, 2, "5000")
    put(21, 1, "Ставка руководителя сети (0–1)")
    put(21, 2, "0.07")

    put(23, 1, "3. ПРОМЕЖУТОЧНЫЕ")
    put(24, 1, "Средний MRR на платящего, ₽")
    put(24, 2, formula="B14*B5+B15*B6")
    put(25, 1, "MRR всего, ₽/мес")
    put(25, 2, formula="B12*B24")
    put(26, 1, "MRR через партнёрскую сеть, ₽/мес")
    put(26, 2, formula="B12*B13*B24")
    put(27, 1, "Платящих L1 (расчётное, min)")
    put(27, 2, formula="MIN(B16*B17,B12*B13)")
    put(28, 1, "MRR по ветке L1, ₽")
    put(28, 2, formula="B27*B24")

    put(30, 1, "4. ВЫПЛАТЫ ПАРТНЁРАМ (тренерам)")
    put(31, 1, "Начисления L1, ₽/мес")
    put(31, 2, formula="B28*B7")
    put(32, 1, "Начисления L2, ₽/мес")
    put(32, 2, formula="B18*B24*B8")
    put(33, 1, "Начисления L3, ₽/мес")
    put(33, 2, formula="B19*B24*B9")
    put(34, 1, "Итого партнёрские начисления, ₽/мес")
    put(34, 2, formula="SUM(B31:B33)")

    put(36, 1, "5. ОБОРОТ ПАРТНЁРКИ (база для % руководителя)")
    put(37, 1, "Ср. начисления на 1 партнёра, ₽")
    put(37, 2, formula="IF(B16=0,0,B34/B16)")
    put(38, 1, "Ср. оборот 1 партнёра = max(0; начисл. − абонп.)")
    put(38, 2, formula="MAX(0,B37-B20)")
    put(39, 1, "Оборот сети (сумма по партнёрам), ₽/мес")
    put(39, 2, formula="B16*B38")
    put(40, 1, "Вознаграждение руководителя, ₽/мес")
    put(40, 2, formula="B39*B21")

    put(42, 1, "6. МАРЖА КОМПАНИИ")
    put(43, 1, "MRR вне сети (прямой вход), ₽")
    put(43, 2, formula="B25-B26")
    put(44, 1, "Маржа на сетевой MRR, ₽")
    put(44, 2, formula="B26-B34-B40")
    put(45, 1, "Маржа на прямом MRR, ₽")
    put(45, 2, formula="B43")
    put(46, 1, "Маржа компании ИТОГО, ₽/мес")
    put(46, 2, formula="B44+B45")
    put(47, 1, "Маржа % от общего MRR")
    put(47, 2, formula="IF(B25=0,0,B46/B25)")
    put(48, 1, "Руководитель % от общего MRR")
    put(48, 2, formula="IF(B25=0,0,B40/B25)")
    put(49, 1, "Партнёрка % от общего MRR")
    put(49, 2, formula="IF(B25=0,0,B34/B25)")

    put(51, 1, "7. КОНТРОЛЬ")
    put(52, 1, "Партнёров без «оборота» (начисл. < абонп.)")
    put(52, 2, formula='IF(B38=0,B16,IF(B37<B20,B16,0))')
    put(53, 1, "Порог L1 для нуля оборота (только L1, Профи)")
    put(53, 2, formula="IF(B24*B7=0,0,CEILING(B20/(B24*B7),1))")

    return sheet_xml(r)


def build_scenarios_sheet() -> str:
    """Лист «Сценарии» — три пресета, ссылки на формулы модели через дублированную логику в строках."""
    r: dict[int, dict[int, Cell]] = {}

    def put(row: int, col: int, val: str | None = None, formula: str | None = None) -> None:
        r.setdefault(row, {})[col] = (val, formula)

    put(1, 1, "Сценарии (меняйте жёлтые ячейки — столбцы B, D, F)")
    put(2, 1, "Параметр")
    put(2, 2, "Ранний")
    put(2, 4, "100 платников")
    put(2, 6, "Амбиция")

    labels = [
        (4, "Платящих тренеров"),
        (5, "Доля через сеть"),
        (6, "Партнёров с договором"),
        (7, "Ср. L1 / партнёр"),
        (8, "L2 платящих"),
        (9, "L3 платящих"),
        (10, "Ставка руководителя"),
    ]
    early = ["30", "0.5", "3", "4", "5", "2", "0.05"]
    mid = ["100", "0.7", "10", "6", "15", "5", "0.07"]
    high = ["200", "0.8", "20", "8", "40", "15", "0.1"]

    for i, (row, label) in enumerate(labels):
        put(row, 1, label)
        put(row, 2, early[i])
        put(row, 4, mid[i])
        put(row, 6, high[i])

    # Shared constants from model concept (Pro 5000, Max 10000, 85/15 mix, rates)
    put(12, 1, "— константы (как на листе Модель) —")
    put(13, 1, "Цена Профи")
    put(13, 2, "5000")
    put(14, 1, "Цена Макс")
    put(14, 2, "10000")
    put(15, 1, "Доля Профи")
    put(15, 2, "0.85")
    put(16, 1, "Доля Макс")
    put(16, 2, "0.15")
    put(17, 1, "Абонплата партнёра")
    put(17, 2, "5000")
    put(18, 1, "L1 / L2 / L3")
    put(18, 2, "0.2")
    put(18, 3, "0.05")
    put(18, 4, "0.025")

    put(20, 1, "РЕЗУЛЬТАТ")
    put(20, 2, "Ранний")
    put(20, 4, "100 пл.")
    put(20, 6, "Амбиция")

    put(21, 1, "MRR всего, ₽")
    for res_col, in_col in [(3, 2), (5, 4), (7, 6)]:
        p = col_letter(in_col)
        put(
            21,
            res_col,
            formula=f"{p}4*($B$15*$B$13+$B$16*$B$14)",
        )

    put(22, 1, "MRR сети, ₽")
    for res_col, in_col in [(3, 2), (5, 4), (7, 6)]:
        p = col_letter(in_col)
        put(
            22,
            res_col,
            formula=f"{p}4*{p}5*($B$15*$B$13+$B$16*$B$14)",
        )

    put(23, 1, "Партнёрские выплаты, ₽")
    for res_col, in_col in [(3, 2), (5, 4), (7, 6)]:
        p = col_letter(in_col)
        avg = "($B$15*$B$13+$B$16*$B$14)"
        put(
            23,
            res_col,
            formula=(
                f"MIN({p}6*{p}7,{p}4*{p}5)*{avg}*$B$18"
                f"+{p}8*{avg}*$C$18"
                f"+{p}9*{avg}*$D$18"
            ),
        )

    put(24, 1, "Оборот сети, ₽")
    for res_col, in_col in [(3, 2), (5, 4), (7, 6)]:
        p = col_letter(in_col)
        rc = col_letter(res_col)
        put(
            24,
            res_col,
            formula=f"IF({p}6=0,0,{p}6*MAX(0,{rc}23/{p}6-$B$17))",
        )

    put(25, 1, "Руководитель, ₽")
    for res_col, in_col in [(3, 2), (5, 4), (7, 6)]:
        p = col_letter(in_col)
        rc = col_letter(res_col)
        put(25, res_col, formula=f"{rc}24*{p}10")

    put(26, 1, "Маржа компании, ₽")
    for res_col in [3, 5, 7]:
        rc = col_letter(res_col)
        put(26, res_col, formula=f"{rc}21-{rc}23-{rc}25")

    put(27, 1, "Маржа %")
    for res_col in [3, 5, 7]:
        rc = col_letter(res_col)
        put(27, res_col, formula=f"IF({rc}21=0,0,{rc}26/{rc}21)")

    return sheet_xml(r)


def build_help_sheet() -> str:
    r: dict[int, dict[int, Cell]] = {}

    def put(row: int, col: int, val: str) -> None:
        r.setdefault(row, {})[col] = (val, None)

    put(1, 1, "Справка")
    put(3, 1, "Оборот партнёра P = max(0; L1+L2+L3 начисления P − абонплата P)")
    put(4, 1, "Оборот сети = Σ по всем партнёрам с договором")
    put(5, 1, "Руководитель = ставка × оборот сети (платит компания, не урезая L1/L2/L3)")
    put(6, 1, "Маржа = MRR − все партнёрские начисления − руководитель")
    put(8, 1, "Канон: модуль-партнерка L1 20%, L2 5%, L3 2,5%")
    put(9, 1, "Документ: 01-цели-этапа-пилот.md + решение директора 2026-06")
    put(11, 1, "Лист «Модель» — основной калькулятор. Меняйте синие ячейки столбца B.")
    put(12, 1, "Лист «Сценарии» — три колонки для сравнения.")

    return sheet_xml(r)


def write_xlsx(path: Path) -> None:
    workbook = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets>
<sheet name="Модель" sheetId="1" r:id="rId1"/>
<sheet name="Сценарии" sheetId="2" r:id="rId2"/>
<sheet name="Справка" sheetId="3" r:id="rId3"/>
</sheets>
</workbook>"""

    workbook_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>"""

    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>
<fills count="1"><fill><patternFill patternType="none"/></fill></fills>
<borders count="1"><border/></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>
</styleSheet>"""

    sheets = [
        build_model_sheet(),
        build_scenarios_sheet(),
        build_help_sheet(),
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/styles.xml", styles)
        for i, xml in enumerate(sheets, 1):
            zf.writestr(f"xl/worksheets/sheet{i}.xml", xml)


if __name__ == "__main__":
    write_xlsx(OUT)
    print(f"Written: {OUT}")
