#!/usr/bin/env python3
"""Сборка PDF: Telotron — one-pager инвестор партнёр."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
INSTR = ROOT / "Инструкции"
READY = ROOT / "Готовые документы"
BUILD = BASE / ".build-one-pager-investor"
SOURCE = INSTR / "Telotron — one-pager инвестор партнёр.md"
OUT_DOCX = BUILD / "one-pager.docx"
OUT_PDF = READY / "Telotron — one-pager инвестор партнёр.pdf"
SOFFICE = Path("/usr/lib/libreoffice/program/soffice")


def main() -> None:
    if not SOURCE.exists():
        print(f"ERROR: нет {SOURCE}", file=sys.stderr)
        sys.exit(1)

    BUILD.mkdir(parents=True, exist_ok=True)
    READY.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "pandoc",
            str(SOURCE),
            "-o",
            str(OUT_DOCX),
            "--standalone",
            "-V",
            "geometry:margin=1.2cm",
            "-V",
            "fontsize=9pt",
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
            str(BUILD),
            str(OUT_DOCX),
        ],
        check=True,
    )

    built = BUILD / "one-pager.pdf"
    if not built.exists():
        print("ERROR: PDF не создан", file=sys.stderr)
        sys.exit(1)

    built.replace(OUT_PDF)
    print(f"OK: {OUT_PDF}")


if __name__ == "__main__":
    main()
