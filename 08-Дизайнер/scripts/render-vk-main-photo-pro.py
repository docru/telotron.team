#!/usr/bin/env python3
"""VK community main photo (square): Pro logo ≥400px, safe padding for circular crop."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

DESIGN = Path(__file__).resolve().parent.parent
REPO = DESIGN.parent.parent
LOGO = REPO / "_telotron.ru/public/brand/logo-pro-256.png"
OUT_DIR = DESIGN / "vk"
OUT_PNG = OUT_DIR / "vk-main-photo-pro-1080.png"
OUT_JPG = OUT_DIR / "vk-main-photo-pro-1080.jpg"

# VK: главное фото сообщества; при вставке обрезка в круг.
SIZE = 1080
LOGO_MIN_PX = 400
# Логотип ~37% стороны → ~200px отступ от края до знака (круг mode≈диаметр 1080)
LOGO_HEIGHT = 420

BG = (248, 250, 252)  # #F8FAFC
BG_ACCENT = (239, 246, 255)  # #EFF6FF


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    assert LOGO_HEIGHT >= LOGO_MIN_PX, "logo must be at least 400px"

    img = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    # Мягкий фон Pro (внутри «безопасного» круга)
    pad = int(SIZE * 0.08)
    draw.ellipse(
        (pad, pad, SIZE - pad, SIZE - pad),
        fill=BG_ACCENT,
    )

    logo = Image.open(LOGO).convert("RGBA")
    logo_w = int(logo.width * (LOGO_HEIGHT / logo.height))
    logo = logo.resize((logo_w, LOGO_HEIGHT), Image.LANCZOS)

    x = (SIZE - logo_w) // 2
    y = (SIZE - LOGO_HEIGHT) // 2
    img.paste(logo, (x, y), logo)

    # Debug guide (optional preview) — uncomment to see VK circle crop:
    # draw.ellipse((0, 0, SIZE - 1, SIZE - 1), outline=(200, 200, 200), width=1)

    img.save(OUT_PNG, "PNG", optimize=True)
    img.save(OUT_JPG, "JPEG", quality=92, optimize=True, progressive=True)
    margin = min(x, y)
    print(f"Wrote {OUT_PNG} ({SIZE}×{SIZE}, logo {logo_w}×{LOGO_HEIGHT}, margin ~{margin}px)")


if __name__ == "__main__":
    main()
