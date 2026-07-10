#!/usr/bin/env python3
"""Сборка PDF: коммерческие one-pager для инвестора / партнёра."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
INSTR = ROOT / "Инструкции"
READY = ROOT / "Готовые документы"
SOFFICE = Path("/usr/lib/libreoffice/program/soffice")

VARIANTS = {
    "1p": {
        "source": INSTR / "Telotron — one-pager инвестор партнёр.md",
        "pdf": READY / "Telotron — one-pager инвестор партнёр.pdf",
        "build": BASE / ".build-one-pager-investor",
        "margin": "1.2cm",
        "fontsize": "9pt",
    },
    "3p": {
        "source": INSTR / "Telotron — инвестор партнёр 3 страницы.md",
        "pdf": READY / "Telotron — инвестор партнёр 3 страницы.pdf",
        "build": BASE / ".build-investor-3p",
        "margin": "1.2cm",
        "fontsize": "9pt",
    },
}


def build(variant: str) -> None:
    cfg = VARIANTS[variant]
    source: Path = cfg["source"]
    out_pdf: Path = cfg["pdf"]
    build_dir: Path = cfg["build"]
    out_docx = build_dir / "document.docx"

    if not source.exists():
        print(f"ERROR: нет {source}", file=sys.stderr)
        sys.exit(1)

    build_dir.mkdir(parents=True, exist_ok=True)
    READY.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "pandoc",
            str(source),
            "-o",
            str(out_docx),
            "--standalone",
            "-V",
            f"geometry:margin={cfg['margin']}",
            "-V",
            f"fontsize={cfg['fontsize']}",
        ],
        check=True,
    )

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
            str(build_dir),
            str(out_docx),
        ],
        check=True,
    )

    built = build_dir / "document.pdf"
    if not built.exists():
        print("ERROR: PDF не создан", file=sys.stderr)
        sys.exit(1)

    built.replace(out_pdf)
    print(f"OK: {out_pdf}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Сборка PDF one-pager Telotron.")
    parser.add_argument(
        "--variant",
        choices=VARIANTS.keys(),
        default="1p",
        help="1p — один лист; 3p — три страницы (по умолчанию: 1p)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="собрать все варианты",
    )
    args = parser.parse_args()

    if args.all:
        for key in VARIANTS:
            build(key)
    else:
        build(args.variant)


if __name__ == "__main__":
    main()
