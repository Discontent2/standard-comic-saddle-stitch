#!/usr/bin/env python3
"""Validate comic page images for standard comic saddle-stitch printing."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAGES_DIR = ROOT / "assets" / "pages"

EXPECTED_WIDTH = 2063
EXPECTED_HEIGHT = 3150
DPI = 300
PAGE_NAME_RE = re.compile(r"^page-(\d{3})\.(png|jpg|jpeg|tif|tiff)$", re.IGNORECASE)


@dataclass
class PageReport:
    path: Path
    width: int
    height: int
    dpi: tuple[int, int] | None
    ok_name: bool
    ok_size: bool


def image_dpi(img: Image.Image) -> tuple[int, int] | None:
    raw = img.info.get("dpi")
    if not raw:
        return None
    try:
        return tuple(round(float(v)) for v in raw[:2])  # type: ignore[index]
    except Exception:
        return None


def collect_pages() -> list[Path]:
    return sorted(
        [p for p in PAGES_DIR.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}],
        key=lambda p: p.name.lower(),
    )


def main() -> int:
    if not PAGES_DIR.exists():
        print(f"Missing page folder: {PAGES_DIR}")
        return 2

    paths = collect_pages()
    if not paths:
        print("No page images found in assets/pages/. Add files named page-001.png, page-002.png, etc.")
        return 1

    reports: list[PageReport] = []
    for path in paths:
        with Image.open(path) as img:
            width, height = img.size
            reports.append(
                PageReport(
                    path=path,
                    width=width,
                    height=height,
                    dpi=image_dpi(img),
                    ok_name=bool(PAGE_NAME_RE.match(path.name)),
                    ok_size=(width, height) == (EXPECTED_WIDTH, EXPECTED_HEIGHT),
                )
            )

    errors = 0
    print("\nComic page validation")
    print("=" * 24)
    print(f"Target: {EXPECTED_WIDTH} × {EXPECTED_HEIGHT} px at {DPI} DPI")
    print(f"Pages found: {len(reports)}")

    if len(reports) % 4 != 0:
        errors += 1
        print(f"[FAIL] Page count must be divisible by 4 for saddle-stitch. Current count: {len(reports)}")
    else:
        print("[ OK ] Page count is divisible by 4.")

    for index, report in enumerate(reports, start=1):
        prefix = "[ OK ]"
        notes: list[str] = []

        if not report.ok_name:
            prefix = "[FAIL]"
            errors += 1
            notes.append("name should look like page-001.png")

        expected_name = f"page-{index:03d}"
        if report.path.stem.lower() != expected_name:
            prefix = "[FAIL]"
            errors += 1
            notes.append(f"expected reading-order name {expected_name}{report.path.suffix.lower()}")

        if not report.ok_size:
            prefix = "[WARN]" if prefix == "[ OK ]" else prefix
            notes.append(f"size is {report.width} × {report.height}, expected {EXPECTED_WIDTH} × {EXPECTED_HEIGHT}")

        if report.dpi and report.dpi != (DPI, DPI):
            notes.append(f"DPI metadata is {report.dpi[0]} × {report.dpi[1]}, expected {DPI} × {DPI}")
        elif not report.dpi:
            notes.append("no DPI metadata; pixel size matters most, but add 300 DPI before final upload")

        suffix = f" - {'; '.join(notes)}" if notes else ""
        print(f"{prefix} {report.path.name}{suffix}")

    if errors:
        print("\nFix failed items before sending to print. Warnings are worth checking before proofing.")
        return 1

    print("\nLooks ready for a proof PDF. The tiny paper dragon has been appeased.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
