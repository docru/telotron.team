#!/usr/bin/env python3
"""Render VK community cover 1920×768 for Telotron Pro."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DESIGN = Path(__file__).resolve().parent.parent
REPO = DESIGN.parent.parent
LOGO = REPO / "_telotron.ru/public/brand/logo-pro-256.png"
OUT_DIR = DESIGN / "vk"
OUT_PNG = OUT_DIR / "vk-cover-pro-1920x768.png"
OUT_JPG = OUT_DIR / "vk-cover-pro-1920x768.jpg"

W, H = 1920, 768

# Pro tokens
BG = (248, 250, 252)  # #F8FAFC
BG_ACCENT = (239, 246, 255)  # #EFF6FF
PRIMARY = (29, 78, 216)  # #1D4ED8
FG = (15, 23, 42)  # #0F172A
MUTED = (100, 116, 139)  # #64748B

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Soft Pro gradient blobs (safe, not at edges)
    draw.ellipse((120, -80, 520, 320), fill=BG_ACCENT)
    draw.ellipse((W - 420, H - 200, W + 80, H + 120), fill=BG_ACCENT)
    draw.rectangle((0, 0, W, H), fill=None)  # noop, keep draw active

    logo = Image.open(LOGO).convert("RGBA")
    logo_h = 200
    logo_w = int(logo.width * (logo_h / logo.height))
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

    title = "Telotron · для тренеров"
    subtitle = "Запись · планы · дневник клиента"
    pilot = "Пилот: 60 дней бесплатно, без оплат до 01.08"

    font_title = load_font(FONT_BOLD, 52)
    font_sub = load_font(FONT_REG, 30)
    font_pilot = load_font(FONT_REG, 24)

    gap_logo_text = 44
    line_gap_1 = 14
    line_gap_2 = 10

    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    sub_bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
    pilot_bbox = draw.textbbox((0, 0), pilot, font=font_pilot)

    text_w = max(
        title_bbox[2] - title_bbox[0],
        sub_bbox[2] - sub_bbox[0],
        pilot_bbox[2] - pilot_bbox[0],
    )
    text_h = (
        (title_bbox[3] - title_bbox[1])
        + line_gap_1
        + (sub_bbox[3] - sub_bbox[1])
        + line_gap_2
        + (pilot_bbox[3] - pilot_bbox[1])
    )

    block_w = logo_w + gap_logo_text + text_w
    block_h = max(logo_h, text_h)

    # Center block in safe zone (~central 1200px for mobile VK crop)
    block_x = (W - block_w) // 2
    block_y = (H - block_h) // 2

    logo_x = block_x
    logo_y = block_y + (block_h - logo_h) // 2
    img.paste(logo, (logo_x, logo_y), logo)

    text_x = block_x + logo_w + gap_logo_text
    text_y = block_y + (block_h - text_h) // 2

    draw.text((text_x, text_y), title, font=font_title, fill=FG)
    y2 = text_y + (title_bbox[3] - title_bbox[1]) + line_gap_1
    draw.text((text_x, y2), subtitle, font=font_sub, fill=MUTED)
    y3 = y2 + (sub_bbox[3] - sub_bbox[1]) + line_gap_2
    draw.text((text_x, y3), pilot, font=font_pilot, fill=PRIMARY)

    # Subtle bottom accent line (Pro)
    draw.line((block_x, H - 48, block_x + block_w, H - 48), fill=PRIMARY, width=3)

    img.save(OUT_PNG, "PNG", optimize=True)
    img.save(OUT_JPG, "JPEG", quality=92, optimize=True, progressive=True)
    print(f"Wrote {OUT_PNG}")
    print(f"Wrote {OUT_JPG}")


if __name__ == "__main__":
    main()
