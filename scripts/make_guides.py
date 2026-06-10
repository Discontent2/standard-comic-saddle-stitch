#!/usr/bin/env python3
"""Create printable page guide templates for standard comic full-bleed pages."""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"

DPI = 300
FULL_W, FULL_H = 2063, 3150
BLEED = round(0.125 * DPI)
SAFE = round((0.125 + 0.375) * DPI)  # bleed plus 0.375 in inside trim
TRIM_BOX = (BLEED, BLEED, FULL_W - BLEED, FULL_H - BLEED)
SAFE_BOX = (SAFE, SAFE, FULL_W - SAFE, FULL_H - SAFE)


def main() -> None:
    TEMPLATES.mkdir(exist_ok=True)
    img = Image.new("RGB", (FULL_W, FULL_H), "white")
    draw = ImageDraw.Draw(img)

    # Outer canvas edge
    draw.rectangle((0, 0, FULL_W - 1, FULL_H - 1), outline=(0, 0, 0), width=4)

    # Bleed/trim/safe guides
    draw.rectangle(TRIM_BOX, outline=(220, 0, 0), width=4)
    draw.rectangle(SAFE_BOX, outline=(0, 130, 0), width=4)

    # Center line hints
    draw.line((FULL_W // 2, 0, FULL_W // 2, FULL_H), fill=(180, 180, 180), width=1)
    draw.line((0, FULL_H // 2, FULL_W, FULL_H // 2), fill=(180, 180, 180), width=1)

    # Labels are intentionally minimal and outside likely live art areas.
    draw.text((50, 50), "FULL BLEED: 2063 x 3150 px", fill=(0, 0, 0))
    draw.text((50, 90), "RED = TRIM", fill=(220, 0, 0))
    draw.text((50, 130), "GREEN = SAFE ZONE", fill=(0, 130, 0))

    out = TEMPLATES / "standard-comic-full-bleed-guide.png"
    img.save(out, dpi=(DPI, DPI))
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
