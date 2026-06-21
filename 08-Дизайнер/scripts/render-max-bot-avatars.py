#!/usr/bin/env python3
"""MAX bot avatars 500×500: Pro / Client logo + подпись, safe zone для круглой обрезки."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DESIGN = Path(__file__).resolve().parent.parent
REPO = DESIGN.parent.parent
OUT_DIR = DESIGN / "max"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

SIZE = 500
# Отступ от края под круглую маску MAX (~диаметр 500, контент внутри ~88%)
SAFE_INSET = 42

# Pro / Client tokens
PRO_BG = (248, 250, 252)
PRO_ACCENT = (239, 246, 255)
PRO_PRIMARY = (29, 78, 216)

CLIENT_BG = (255, 255, 255)
CLIENT_ACCENT = (240, 253, 244)
CLIENT_PRIMARY = (22, 163, 74)

FG = (15, 23, 42)
MUTED = (100, 116, 139)


@dataclass(frozen=True)
class BotAvatarSpec:
    zone: str
    logo_path: Path
    bg: tuple[int, int, int]
    accent: tuple[int, int, int]
    zone_color: tuple[int, int, int]
    zone_label: str
    subtitle: str
    logo_height: int


SPECS = (
    BotAvatarSpec(
        zone="pro",
        logo_path=REPO / "_telotron.ru/public/brand/logo-pro-256.png",
        bg=PRO_BG,
        accent=PRO_ACCENT,
        zone_color=PRO_PRIMARY,
        zone_label="Pro",
        subtitle="для тренеров",
        logo_height=188,
    ),
    BotAvatarSpec(
        zone="client",
        logo_path=REPO / "_telotron.ru/public/brand/logo-client-256.png",
        bg=CLIENT_BG,
        accent=CLIENT_ACCENT,
        zone_color=CLIENT_PRIMARY,
        zone_label="Client",
        subtitle="для клиентов",
        logo_height=188,
    ),
)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def render(spec: BotAvatarSpec) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    img = Image.new("RGB", (SIZE, SIZE), spec.bg)
    draw = ImageDraw.Draw(img)

    inner = SAFE_INSET
    draw.ellipse((inner, inner, SIZE - inner, SIZE - inner), fill=spec.accent)

    f_brand = font(FONT_BOLD, 30)
    f_zone = font(FONT_BOLD, 24)
    f_sub = font(FONT_REG, 17)

    brand = "Телотрон"
    gap_logo_text = 10
    gap_lines = 4

    logo = Image.open(spec.logo_path).convert("RGBA")
    logo_w = int(logo.width * (spec.logo_height / logo.height))
    logo = logo.resize((logo_w, spec.logo_height), Image.LANCZOS)

    tw1, th1 = text_size(draw, brand, f_brand)
    tw2, th2 = text_size(draw, spec.zone_label, f_zone)
    tw3, th3 = text_size(draw, spec.subtitle, f_sub)
    text_w = max(tw1, tw2, tw3)
    text_h = th1 + gap_lines + th2 + gap_lines + th3

    block_h = spec.logo_height + gap_logo_text + text_h
    block_w = max(logo_w, text_w)

    block_x = (SIZE - block_w) // 2
    block_y = (SIZE - block_h) // 2

    logo_x = block_x + (block_w - logo_w) // 2
    logo_y = block_y
    img.paste(logo, (logo_x, logo_y), logo)

    text_x = block_x + (block_w - text_w) // 2
    y = logo_y + spec.logo_height + gap_logo_text

    draw.text((text_x + (text_w - tw1) // 2, y), brand, font=f_brand, fill=FG)
    y += th1 + gap_lines
    draw.text((text_x + (text_w - tw2) // 2, y), spec.zone_label, font=f_zone, fill=spec.zone_color)
    y += th2 + gap_lines
    draw.text((text_x + (text_w - tw3) // 2, y), spec.subtitle, font=f_sub, fill=MUTED)

    base = OUT_DIR / f"max-bot-avatar-{spec.zone}-500"
    png = base.with_suffix(".png")
    jpg = Path(str(base) + ".jpg")
    img.save(png, "PNG", optimize=True)
    img.save(jpg, "JPEG", quality=92, optimize=True, progressive=True)
    margin = min(block_x, block_y, SIZE - block_x - block_w, SIZE - block_y - block_h)
    print(f"Wrote {png} (logo {logo_w}×{spec.logo_height}, safe margin ~{margin}px)")


def main() -> None:
    for spec in SPECS:
        render(spec)


if __name__ == "__main__":
    main()
