#!/usr/bin/env python3
"""Build a proof PDF from ordered comic page images."""
from __future__ import annotations

from pathlib import Path
import re
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAGES_DIR = ROOT / "assets" / "pages"
BUILD_DIR = ROOT / "build"
OUTPUT = BUILD_DIR / "comic-proof.pdf"
DPI = 300
PAGE_RE = re.compile(r"^page-(\d{3})\.(png|jpg|jpeg|tif|tiff)$", re.IGNORECASE)


def page_sort_key(path: Path) -> int:
    match = PAGE_RE.match(path.name)
    if not match:
        return 999999
    return int(match.group(1))


def flatten_for_pdf(path: Path) -> Image.Image:
    img = Image.open(path)
    if img.mode in {"RGBA", "LA"} or (img.mode == "P" and "transparency" in img.info):
        background = Image.new("RGB", img.size, "white")
        rgba = img.convert("RGBA")
        background.paste(rgba, mask=rgba.split()[-1])
        rgba.close()
        img.close()
        return background
    converted = img.convert("RGB")
    img.close()
    return converted


def main() -> int:
    BUILD_DIR.mkdir(exist_ok=True)
    page_paths = sorted(
        [p for p in PAGES_DIR.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}],
        key=page_sort_key,
    )

    if not page_paths:
        print("No pages found. Add page images to assets/pages/ first.")
        return 1

    if len(page_paths) % 4 != 0:
        print(f"Page count is {len(page_paths)}. Saddle-stitch needs a multiple of 4.")
        return 1

    pages = [flatten_for_pdf(path) for path in page_paths]
    first, rest = pages[0], pages[1:]
    first.save(
        OUTPUT,
        save_all=True,
        append_images=rest,
        resolution=DPI,
        quality=95,
    )

    for page in pages:
        page.close()

    print(f"Built {OUTPUT.relative_to(ROOT)} with {len(page_paths)} pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
