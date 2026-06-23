#!/usr/bin/env python3
"""Сборка «Презентация — Telotron для тренеров.docx/.pdf» со скринами продукта."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
PRESENTATION_DIR = BASE / "Презентация — Telotron для тренеров"
SRC_DIR = BASE / "онбординг-тренеров"
BUILD = BASE / ".build-presentation-pdf"
MEDIA = BUILD / "media"
SOURCE_MD = BUILD / "source.md"
TEMP_DOCX = BUILD / "docx-temp.docx"
FIXED_DOCX = BUILD / "docx-fixed.docx"
SOFFICE = Path("/usr/lib/libreoffice/program/soffice")
LOGO_SRC = BASE.parent.parent / "08-Дизайнер" / "logo" / "logo-pro.svg"
COVER_LOGO = MEDIA / "cover-logo.png"
IMAGE_SCALE = 0.28
MAX_IMG_HEIGHT_PX = 340

VERSION = "1.3"
SOURCE_BASENAME = "Презентация — Telotron для тренеров"
OUT: Path
OUT_PDF: Path

COLOR_PRIMARY = "1D4ED8"
COLOR_FOREGROUND = "0F172A"
COLOR_MUTED = "64748B"
COLOR_BACKGROUND = "F8FAFC"

PAGE_BREAK = (
    "```{=openxml}\n"
    '<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n'
    "```\n\n"
)
SLIDE_HEADING = re.compile(r"^## ")

FEATURES_TABLE = """| Для вас (Pro) | Для клиента (Client) |
|---------------|----------------------|
| Календарь занятий | Ваши записи и планы |
| Клиенты и приглашения | Дневник (еда, вода, замеры — если нужно) |
| Программы тренировок | Отдельное приложение на телефоне |
| Планы питания (файлом) | Напоминания через MAX / Telegram |
| Группы и групповые занятия | |"""

FEATURES_LIST = """**Для вас (Pro):** календарь · клиенты · программы · планы питания · группы

**Для клиента (Client):** записи и планы · дневник · отдельное приложение · напоминания MAX/TG"""

PILOT_TABLE = """| | |
|--|--|
| **Срок** | **60 дней** бесплатно · полный функционал |
| **Оплата** | **не раньше 01.08.2026** · карта на пилоте **не нужна** |
| **Кого ищем** | **10–15 тренеров**, которые ведут **своих** клиентов (очно и/или онлайн) |
| **Что просим** | зарегистрироваться, провести **1 реального клиента** в приложении, **2–4 недели** честной обратной связи |
| **Чего не просим** | публичную рекламу, блог, «продавать» сервис |"""

PILOT_LIST = """- **Срок** — **60 дней** бесплатно, полный функционал
- **Оплата** — не раньше **01.08.2026**, карта на пилоте не нужна
- **Кого ищем** — **10–15 тренеров** со своими клиентами (очно и/или онлайн)
- **Что просим** — reg, **1 реальный клиент** в приложении, **2–4 недели** обратной связи
- **Чего не просим** — публичную рекламу и «продавать» сервис"""

MISSING_LIST = """- Оплата занятий клиентом через Telotron — в разработке
- Чат с клиентом внутри приложения — пока привычные мессенджеры
- SMS-коды — вход через MAX, Telegram или e-mail"""

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
    ("08_raspisanie.jpeg", "08_raspisanie.jpg"),
    ("05_ustanovka_pro.jpeg", "05_ustanovka_pro.jpg"),
    ("06_klienty_ssylka.jpeg", "06_klienty_ssylka.jpg"),
    ("09_programmy_trenirovok.jpeg", "09_programmy_trenirovok.jpg"),
    ("12_client_dnevnik_trenirovka.jpeg", "12_client_dnevnik_trenirovka.jpg"),
    ("11_client_glavnaya.jpeg", "11_client_glavnaya.jpg"),
    ("07_client_registratsiya.jpeg", "07_client_registratsiya.jpg"),
    ("10_gruppy.jpeg", "10_gruppy.jpg"),
]


def configure_outputs(version: str) -> Path:
    global VERSION, OUT, OUT_PDF
    VERSION = version
    stem = f"{SOURCE_BASENAME} v{version}"
    out_dir = PRESENTATION_DIR
    OUT = out_dir / f"{stem}.docx"
    OUT_PDF = out_dir / f"{stem}.pdf"
    return PRESENTATION_DIR / f"{stem}.md"


def replace_image_paths(text: str) -> str:
    for src_name, dst_name in PAIRS:
        for prefix in ("../онбординг-тренеров/", "онбординг-тренеров/"):
            text = text.replace(f"{prefix}{src_name}", f"media/{dst_name}")
    return text


def strip_title_heading(text: str) -> str:
    """Убирает H1, подзаголовок и --- до первого слайда (##). Титул — в cover page."""
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if SLIDE_HEADING.match(line):
            return "".join(lines[i:])
    return text


def strip_horizontal_rules(text: str) -> str:
    """--- между слайдами в DOCX даёт лишние разрывы; слайды разделяем только Heading2."""
    return re.sub(r"^---\s*\n", "", text, flags=re.MULTILINE)


def fix_slide_page_breaks(xml: str) -> str:
    """Разрыв страницы на самом Heading2 (кроме первого слайда), без пустого абзаца."""
    pattern = re.compile(
        r"(<w:p><w:pPr>)(<w:pStyle w:val=\"Heading2\" />(?:\s*<w:pageBreakBefore />)?)(</w:pPr>)",
    )
    seen = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal seen
        seen += 1
        if seen == 1:
            return match.group(0)
        return f"{match.group(1)}<w:pageBreakBefore />{match.group(2)}{match.group(3)}"

    return pattern.sub(repl, xml)


def prepare_media() -> None:
    if BUILD.exists():
        shutil.rmtree(BUILD)
    MEDIA.mkdir(parents=True)

    scale_pct = int(IMAGE_SCALE * 100)
    for src_name, dst_name in PAIRS:
        subprocess.run(
            [
                "convert",
                str(SRC_DIR / src_name),
                "-strip",
                "-interlace",
                "none",
                "-resize",
                f"{scale_pct}%",
                "-resize",
                f"x{MAX_IMG_HEIGHT_PX}>",
                str(MEDIA / dst_name),
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


def prepare_markdown(source_md: Path) -> None:
    text = source_md.read_text(encoding="utf-8")
    cut = text.split("## Для команды (не отправлять тренеру)")[0]
    cut = replace_image_paths(cut)
    cut = cut.replace(FEATURES_TABLE, FEATURES_LIST)
    cut = cut.replace(PILOT_TABLE, PILOT_LIST)
    cut = cut.replace(CONTACTS_TABLE, CONTACTS_LIST)
    cut = strip_title_heading(cut)
    cut = strip_horizontal_rules(cut)
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
    cx = cy = 1260000
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


def _next_rid(rels_xml: str) -> str:
    ids = [int(x) for x in re.findall(r'Id="rId(\d+)"', rels_xml)]
    return f"rId{max(ids) + 1 if ids else 1}"


def _find_hyperlink_rid(rels_xml: str, url: str) -> str | None:
    pattern = rf'Id="(rId\d+)"[^>]*Target="{re.escape(url)}"'
    match = re.search(pattern, rels_xml)
    return match.group(1) if match else None


def build_title_page_xml(cover_image_rid: str, site_link_rid: str) -> str:
    parts = [
        _centered_para(_text_run(" ", size=2, color=COLOR_BACKGROUND), before=0, after=0),
        _cover_logo_paragraph(cover_image_rid),
        _centered_para(_text_run("Telotron", size=72, color=COLOR_PRIMARY, bold=True), after=80),
        _centered_para(_text_run("Для тренера", size=44, color=COLOR_FOREGROUND, bold=True), after=60),
        _centered_para(_text_run("Расписание · планы · дневник клиента", size=26, color=COLOR_MUTED), after=120),
        _accent_bar(),
        _centered_para(_text_run("Пилот · 60 дней бесплатно", size=24, color=COLOR_MUTED), before=200, after=80),
        _centered_para(
            (
                f'<w:hyperlink r:id="{site_link_rid}">'
                f"<w:r>{_run_props(size=28, color=COLOR_PRIMARY, bold=True)}"
                "<w:t>telotron.ru</w:t></w:r></w:hyperlink>"
            ),
            after=160,
        ),
        _centered_para(_text_run("Июнь–июль 2026", size=22, color=COLOR_MUTED), before=1200, after=0),
        '<w:p><w:r><w:br w:type="page"/></w:r></w:p>',
    ]
    return "".join(parts)


def _add_relationship(rels_xml: str, relationship: str) -> str:
    return rels_xml.replace("</Relationships>", f"{relationship}</Relationships>", 1)


def insert_title_page(xml: str, rels_xml: str, cover_logo: Path) -> tuple[str, str, bytes | None]:
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

    site_link_rid = _find_hyperlink_rid(rels_xml, "https://telotron.ru/")
    if site_link_rid is None:
        site_link_rid = _next_rid(rels_xml)
        rels_xml = _add_relationship(
            rels_xml,
            (
                f'<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
                f'Id="{site_link_rid}" Target="https://telotron.ru/" TargetMode="External"/>'
            ),
        )

    title_xml = build_title_page_xml(cover_rid, site_link_rid)
    xml = xml.replace("<w:body>", f"<w:body>{title_xml}", 1)
    return xml, rels_xml, cover_logo.read_bytes()


def fix_docx_tables(xml: str) -> str:
    def fix_table(match: re.Match[str]) -> str:
        table = match.group(0)
        table = table.replace('<w:tblW w:type="pct" w:w="0.0" />', '<w:tblW w:type="pct" w:w="5000" />')
        return table

    return re.sub(r"<w:tbl>.*?</w:tbl>", fix_table, xml, flags=re.DOTALL)


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
        xml = fix_slide_page_breaks(xml)
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
    media = [n for n in zipfile.ZipFile(OUT).namelist() if n.startswith("word/media/")]
    print(f"OK: {OUT}")
    print(f"images in docx: {len(media)}")


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
    built = BUILD / OUT_PDF.name
    shutil.copy2(built, OUT_PDF)
    print(f"OK: {OUT_PDF}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Сборка презентации Telotron для тренеров (PDF/DOCX).")
    parser.add_argument(
        "--version",
        default="1.3",
        choices=("1.2", "1.3"),
        help="версия markdown-исходника (по умолчанию: 1.3)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_md = configure_outputs(args.version)
    if not source_md.exists():
        print(f"ERROR: нет файла {source_md}", file=sys.stderr)
        sys.exit(1)

    prepare_media()
    prepare_markdown(source_md)
    run_pandoc()
    fix_image_ids()
    export_pdf()


if __name__ == "__main__":
    main()
