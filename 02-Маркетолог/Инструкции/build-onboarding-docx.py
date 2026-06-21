#!/usr/bin/env python3
"""Сборка «Онбординг — инструкция для тренеров.docx/.pdf» со встроенными скринами."""

from __future__ import annotations

import re
import shutil
import subprocess
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
SRC_DIR = BASE / "онбординг-тренеров"
BUILD = BASE / ".build-onboarding-docx"
MEDIA = BUILD / "media"
SOURCE_MD = BUILD / "source.md"
TEMP_DOCX = BUILD / "docx-temp.docx"
FIXED_DOCX = BUILD / "docx-fixed.docx"
OUT = BASE / "Онбординг — инструкция для тренеров.docx"
OUT_PDF = BASE / "Онбординг — инструкция для тренеров.pdf"
SOFFICE = Path("/usr/lib/libreoffice/program/soffice")
LOGO_SRC = BASE.parent.parent / "08-Дизайнер" / "logo" / "logo-pro.svg"
COVER_LOGO = MEDIA / "cover-logo.png"
IMAGE_SCALE = 0.25  # 720×1600 → ~180×400, чтобы скрины помещались на страницу A4

# Pro theme (см. «Токены цветов — Pro и Client»)
COLOR_PRIMARY = "1D4ED8"
COLOR_FOREGROUND = "0F172A"
COLOR_MUTED = "64748B"
COLOR_BACKGROUND = "F8FAFC"

PAGE_BREAK = (
    "```{=openxml}\n"
    '<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n'
    "```\n\n"
)
PAGE_BREAK_HEADING = re.compile(
    r"^## (Шаг \d|Если ведёте группы|Минимум за первые 2 дня|Как нам помочь обратной связью)",
)

CHECKLIST_TABLE = """| ✓ | Действие |
|---|----------|
| ☐ | Вы зарегистрировались в Pro |
| ☐ | Один **реальный** клиент принял приглашение |
| ☐ | Есть **занятие** в календаре **или** **план** клиенту |"""

CHECKLIST_LIST = """- ☐ Вы зарегистрировались в Pro
- ☐ Один **реальный** клиент принял приглашение
- ☐ Есть **занятие** в календаре **или** **план** клиенту"""

INTRO_TABLE = """| | |
|--|--|
| **Пилот** | до **31 июля 2026** — пробный период, всё нужное для работы открыто |
| **Регистрация** | **только** по **личной ссылке** `telotron.ru/i/…` из сообщения (WhatsApp, VK, Telegram) |
| **Вход в кабинет** | [pro.telotron.ru](https://pro.telotron.ru/) — когда **уже** зарегистрировались |"""

INTRO_LIST = """- **Пилот** — до **31 июля 2026** — пробный период, всё нужное для работы открыто
- **Регистрация** — **только** по **личной ссылке** `telotron.ru/i/…` из сообщения
- **Вход в кабинет** — [pro.telotron.ru](https://pro.telotron.ru/) — когда **уже** зарегистрировались"""

MISSING_TABLE = """| | |
|--|--|
| Оплата занятий клиентом через Telotron | в разработке |
| Автонапоминания о тренировке в MAX | позже |
| Чат с клиентом внутри приложения | пока общайтесь как привыкли (Telegram и т.д.) |
| SMS-коды | нет, только MAX / Telegram / e-mail |"""

MISSING_LIST = """- **Оплата занятий клиентом через Telotron** — в разработке
- **Автонапоминания о тренировке в MAX** — позже
- **Чат с клиентом внутри приложения** — пока общайтесь как привыкли (Telegram и т.д.)
- **SMS-коды** — нет, только MAX / Telegram / e-mail"""

CONTACTS_TABLE = """| | |
|--|--|
| **Алексей Русаков** | основатель, поддержка пилота |
| **Телефон** | +7 (900) 255-99-40 |
| **VK** | [vk.com/id224642120](https://vk.com/id224642120) |
| **Группа** | [Telotron · для тренеров](https://vk.com/club239586245) |
| **Сайт** | [telotron.ru](https://telotron.ru/) |"""

CONTACTS_LIST = """- **Алексей Русаков** — основатель, поддержка пилота
- **Телефон** — +7 (900) 255-99-40
- **VK** — [vk.com/id224642120](https://vk.com/id224642120)
- **Группа** — [Telotron · для тренеров](https://vk.com/club239586245)
- **Сайт** — [telotron.ru](https://telotron.ru/)"""

PAIRS: list[tuple[str, str]] = [
    ("01_glavnaya_posle_ssylki.jpeg", "01_glavnaya_posle_ssylki.jpg"),
    ("02_registratsiya_pravila.jpeg", "02_registratsiya_pravila.jpg"),
    ("03_registratsiya_max_bot.jpeg", "03_registratsiya_max_bot.jpg"),
    ("04_registratsiya_passkey.jpeg", "04_registratsiya_passkey.jpg"),
    ("05_ustanovka_pro.jpeg", "05_ustanovka_pro.jpg"),
    ("06_klienty_ssylka.jpeg", "06_klienty_ssylka.jpg"),
    ("07_client_registratsiya.jpeg", "07_client_registratsiya.jpg"),
    ("08_raspisanie.jpeg", "08_raspisanie.jpg"),
    ("09_programmy_trenirovok.jpeg", "09_programmy_trenirovok.jpg"),
    ("10_gruppy.jpeg", "10_gruppy.jpg"),
]


def strip_title_heading(text: str) -> str:
    """H1 переносится на титульную страницу."""
    lines = text.splitlines(keepends=True)
    idx = 0
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    if idx < len(lines) and lines[idx].startswith("# "):
        del lines[idx]
        while idx < len(lines) and lines[idx].strip() == "":
            del lines[idx]
    return "".join(lines)


def insert_step_page_breaks(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    for line in lines:
        if PAGE_BREAK_HEADING.match(line):
            while out and out[-1].strip() == "":
                out.pop()
            if out and out[-1].strip() == "---":
                out.pop()
            while out and out[-1].strip() == "":
                out.pop()
            out.append(PAGE_BREAK)
        out.append(line)
    return "".join(out)


def prepare_media() -> None:
    if BUILD.exists():
        shutil.rmtree(BUILD)
    MEDIA.mkdir(parents=True)

    for src_name, dst_name in PAIRS:
        src = SRC_DIR / src_name
        dst = MEDIA / dst_name
        scale_pct = int(IMAGE_SCALE * 100)
        subprocess.run(
            [
                "convert",
                str(src),
                "-strip",
                "-interlace",
                "none",
                "-resize",
                f"{scale_pct}%",
                str(dst),
            ],
            check=True,
        )

    if LOGO_SRC.exists():
        subprocess.run(
            [
                "convert",
                str(LOGO_SRC),
                "-background",
                "none",
                "-density",
                "300",
                "-resize",
                "480x480",
                str(COVER_LOGO),
            ],
            check=True,
        )


def prepare_markdown() -> None:
    text = (BASE / "Онбординг — инструкция для тренеров.md").read_text(encoding="utf-8")
    cut = text.split("## Для команды (не отправлять тренеру)")[0]
    for src_name, dst_name in PAIRS:
        cut = cut.replace(f"онбординг-тренеров/{src_name}", f"media/{dst_name}")
    cut = cut.replace(INTRO_TABLE, INTRO_LIST)
    cut = cut.replace(CHECKLIST_TABLE, CHECKLIST_LIST)
    cut = cut.replace(MISSING_TABLE, MISSING_LIST)
    cut = cut.replace(CONTACTS_TABLE, CONTACTS_LIST)
    cut = strip_title_heading(cut)
    cut = insert_step_page_breaks(cut)
    SOURCE_MD.write_text(cut, encoding="utf-8")


def run_pandoc() -> None:
    subprocess.run(
        [
            "pandoc",
            str(SOURCE_MD),
            "-o",
            str(TEMP_DOCX),
            "--standalone",
            f"--resource-path={BUILD}",
        ],
        check=True,
        cwd=BUILD,
    )


def _run_props(*, size: int, color: str, bold: bool = False) -> str:
    bold_xml = "<w:b/><w:bCs/>" if bold else ""
    return (
        f"<w:rPr>{bold_xml}<w:color w:val=\"{color}\"/>"
        f"<w:sz w:val=\"{size}\"/><w:szCs w:val=\"{size}\"/></w:rPr>"
    )


def _centered_para(content: str, *, before: int = 0, after: int = 120) -> str:
    return (
        f'<w:p><w:pPr><w:jc w:val="center"/>'
        f'<w:spacing w:before="{before}" w:after="{after}" w:line="276" w:lineRule="auto"/>'
        f"</w:pPr>{content}</w:p>"
    )


def _text_run(text: str, *, size: int, color: str, bold: bool = False) -> str:
    return f"<w:r>{_run_props(size=size, color=color, bold=bold)}<w:t>{text}</w:t></w:r>"


def _accent_bar() -> str:
    return (
        '<w:p><w:pPr><w:jc w:val="center"/>'
        f'<w:spacing w:before="160" w:after="240"/>'
        f'<w:shd w:val="clear" w:color="auto" w:fill="{COLOR_PRIMARY}"/>'
        f'<w:ind w:left="2160" w:right="2160"/>'
        "</w:pPr><w:r><w:t> </w:t></w:r></w:p>"
    )


def _cover_logo_paragraph(image_rid: str) -> str:
    cx = cy = 1260000  # ~3,5 см
    return _centered_para(
        (
            "<w:r><w:drawing><wp:inline distT=\"0\" distB=\"0\" distL=\"0\" distR=\"0\">"
            f'<wp:extent cx="{cx}" cy="{cy}"/>'
            '<wp:effectExtent b="0" l="0" r="0" t="0"/>'
            '<wp:docPr descr="Telotron logo" title="" id="0" name="Picture"/>'
            '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            "<pic:pic><pic:nvPicPr>"
            '<pic:cNvPr descr="cover-logo.png" id="0" name="Picture"/>'
            "<pic:cNvPicPr><a:picLocks noChangeArrowheads=\"1\" noChangeAspect=\"1\"/></pic:cNvPicPr>"
            "</pic:nvPicPr><pic:blipFill>"
            f'<a:blip r:embed="{image_rid}"/>'
            "<a:stretch><a:fillRect/></a:stretch>"
            "</pic:blipFill><pic:spPr bwMode=\"auto\">"
            f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            "<a:noFill/><a:ln w=\"9525\"><a:noFill/><a:headEnd/><a:tailEnd/></a:ln>"
            "</pic:spPr></pic:pic></a:graphicData></a:graphic>"
            "</wp:inline></w:drawing></w:r>"
        ),
        before=3200,
        after=160,
    )


def _find_hyperlink_rid(rels_xml: str, url: str) -> str | None:
    pattern = rf'Id="(rId\d+)"[^>]*Target="{re.escape(url)}"'
    match = re.search(pattern, rels_xml)
    return match.group(1) if match else None


def _next_rid(rels_xml: str) -> str:
    ids = [int(x) for x in re.findall(r'Id="rId(\d+)"', rels_xml)]
    return f"rId{max(ids) + 1 if ids else 1}"


def build_title_page_xml(cover_image_rid: str, pro_link_rid: str) -> str:
    parts = [
        _centered_para(
            _text_run(" ", size=2, color=COLOR_BACKGROUND),
            before=0,
            after=0,
        ),
        _cover_logo_paragraph(cover_image_rid),
        _centered_para(
            _text_run("Telotron", size=72, color=COLOR_PRIMARY, bold=True),
            after=80,
        ),
        _centered_para(
            _text_run("Как начать работу", size=44, color=COLOR_FOREGROUND, bold=True),
            after=60,
        ),
        _centered_para(
            _text_run("Инструкция для тренера", size=28, color=COLOR_MUTED),
            after=120,
        ),
        _accent_bar(),
        _centered_para(
            _text_run("Пилот · до 31 июля 2026", size=24, color=COLOR_MUTED),
            before=200,
            after=80,
        ),
        _centered_para(
            (
                f'<w:hyperlink r:id="{pro_link_rid}">'
                f"<w:r>{_run_props(size=28, color=COLOR_PRIMARY, bold=True)}"
                "<w:t>pro.telotron.ru</w:t></w:r></w:hyperlink>"
            ),
            after=160,
        ),
        _centered_para(
            _text_run("Расписание · планы · дневник", size=22, color=COLOR_MUTED),
            before=1200,
            after=0,
        ),
        '<w:p><w:r><w:br w:type="page"/></w:r></w:p>',
    ]
    return "".join(parts)


def _add_relationship(rels_xml: str, relationship: str) -> str:
    return rels_xml.replace("</Relationships>", f"{relationship}</Relationships>", 1)


def insert_title_page(
    xml: str,
    rels_xml: str,
    cover_logo: Path,
) -> tuple[str, str, bytes | None]:
    if not cover_logo.exists():
        return xml, rels_xml, None

    cover_rid = _next_rid(rels_xml)
    rels_xml = _add_relationship(
        rels_xml,
        (
            f'<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Id="{cover_rid}" Target="media/cover-logo.png"/>'
        ),
    )

    pro_link_rid = _find_hyperlink_rid(rels_xml, "https://pro.telotron.ru/")
    if pro_link_rid is None:
        pro_link_rid = _next_rid(rels_xml)
        rels_xml = _add_relationship(
            rels_xml,
            (
                f'<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
                f'Id="{pro_link_rid}" Target="https://pro.telotron.ru/" TargetMode="External"/>'
            ),
        )

    title_xml = build_title_page_xml(cover_rid, pro_link_rid)
    xml = xml.replace("<w:body>", f"<w:body>{title_xml}", 1)
    return xml, rels_xml, cover_logo.read_bytes()


def fix_image_ids() -> None:
    with zipfile.ZipFile(TEMP_DOCX, "r") as zin:
        xml = zin.read("word/document.xml").decode("utf-8")
        rels_xml = zin.read("word/_rels/document.xml.rels").decode("utf-8")
        content_types = zin.read("[Content_Types].xml").decode("utf-8")

        xml, rels_xml, cover_bytes = insert_title_page(xml, rels_xml, COVER_LOGO)

        pic_id = 0

        def repl_docpr(match: re.Match[str]) -> str:
            nonlocal pic_id
            pic_id += 1
            return f"{match.group(1)}{pic_id}{match.group(3)}"

        xml = re.sub(
            r'(<wp:docPr[^>]*\sid=")(\d+)("[^>]*name="Picture")',
            repl_docpr,
            xml,
        )

        cnv_id = 0

        def repl_cnv(match: re.Match[str]) -> str:
            nonlocal cnv_id
            cnv_id += 1
            attrs = re.sub(r'descr="[^"]*"', f'descr="image_{cnv_id}"', match.group(1))
            return f'<pic:cNvPr{attrs}id="{cnv_id}" name="Picture" />'

        xml = re.sub(r'<pic:cNvPr([^>]*?)id="\d+" name="Picture" />', repl_cnv, xml)
        xml = fix_docx_tables(xml)

        if cover_bytes is not None and 'Extension="png"' not in content_types:
            content_types = content_types.replace(
                "</Types>",
                '<Default Extension="png" ContentType="image/png"/></Types>',
            )

        with zipfile.ZipFile(FIXED_DOCX, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    data = xml.encode("utf-8")
                elif item.filename == "word/_rels/document.xml.rels":
                    data = rels_xml.encode("utf-8")
                elif item.filename == "[Content_Types].xml":
                    data = content_types.encode("utf-8")
                zout.writestr(item, data)
            if cover_bytes is not None:
                zout.writestr("word/media/cover-logo.png", cover_bytes)

    shutil.copy2(FIXED_DOCX, OUT)
    ids = re.findall(r'<wp:docPr[^>]*\sid="(\d+)"[^>]*name="Picture"', xml)
    media = [n for n in zipfile.ZipFile(OUT).namelist() if n.startswith("word/media/")]
    print(f"OK: {OUT}")
    print(f"images in docx: {len(media)}; wp:docPr ids: {ids}")


def fix_docx_tables(xml: str) -> str:
    """Pandoc 2.9 иногда даёт tblW=0 и пустой tblGrid — LibreOffice ломает вёрстку."""

    def fix_table(match: re.Match[str]) -> str:
        table = match.group(0)
        table = table.replace(
            '<w:tblW w:type="pct" w:w="0.0" />',
            '<w:tblW w:type="pct" w:w="5000" />',
        )
        if "<w:tblGrid />" in table or "<w:tblGrid></w:tblGrid>" in table:
            first_row = re.search(r"<w:tr[^>]*>(.*?)</w:tr>", table, re.DOTALL)
            if first_row:
                cols = len(re.findall(r"<w:tc[ >]", first_row.group(1)))
                if cols == 2:
                    widths = ("1800", "8200")
                elif cols == 1:
                    widths = ("5000",)
                else:
                    widths = tuple(str(5000 // cols) for _ in range(cols))
                grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
                table = re.sub(
                    r"<w:tblGrid\s*/>|<w:tblGrid></w:tblGrid>",
                    f"<w:tblGrid>{grid}</w:tblGrid>",
                    table,
                    count=1,
                )
        elif re.search(r"<w:tblGrid>.*?<w:gridCol", table, re.DOTALL):
            first_row = re.search(r"<w:tr[^>]*>(.*?)</w:tr>", table, re.DOTALL)
            if first_row and len(re.findall(r"<w:tc[ >]", first_row.group(1))) == 2:
                grid = '<w:gridCol w:w="1800"/><w:gridCol w:w="8200"/>'
                table = re.sub(
                    r"<w:tblGrid>.*?</w:tblGrid>",
                    f"<w:tblGrid>{grid}</w:tblGrid>",
                    table,
                    count=1,
                )
        return table

    return re.sub(r"<w:tbl>.*?</w:tbl>", fix_table, xml, flags=re.DOTALL)


def export_pdf() -> None:
    soffice = SOFFICE if SOFFICE.exists() else Path("/usr/bin/libreoffice")
    subprocess.run(
        [
            str(soffice),
            "--headless",
            "--nologo",
            "--nofirststartwizard",
            "--convert-to",
            "pdf",
            "--outdir",
            str(BUILD),
            str(OUT),
        ],
        check=True,
    )
    built = BUILD / "Онбординг — инструкция для тренеров.pdf"
    shutil.copy2(built, OUT_PDF)
    print(f"OK: {OUT_PDF}")


def main() -> None:
    prepare_media()
    prepare_markdown()
    run_pandoc()
    fix_image_ids()
    export_pdf()


if __name__ == "__main__":
    main()
