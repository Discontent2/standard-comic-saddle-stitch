# Standard Comic Saddle-Stitch Kit

A production repo for turning generated comic images into a real printed saddle-stitch comic.

## Book target

| Spec | Value |
|---|---:|
| Trim size | 6.625 in × 10.25 in |
| Bleed | 0.125 in on every edge |
| Full-bleed canvas | 6.875 in × 10.5 in |
| Print resolution | 300 DPI |
| Full-bleed pixels | 2063 × 3150 px |
| Trim pixels | 1988 × 3075 px |
| Binding | Saddle-stitch |
| Page count rule | Multiple of 4 |

## Folder map

```text
assets/pages/       final interior pages named page-001.png, page-002.png, etc.
assets/covers/      cover files, usually cover-front.png and cover-back.png
assets/reference/   reference art, character sheets, notes, old generations
templates/          guide templates for full-bleed pages
scripts/            validation and PDF build helpers
build/              exported print PDFs, ignored by git except .gitkeep
docs/               print checklist and production notes
```

## Fast workflow

1. Save the original generated images from ChatGPT.
2. Put final interior pages in `assets/pages/`.
3. Rename them in reading order:
   - `page-001.png`
   - `page-002.png`
   - `page-003.png`
4. Keep the page count divisible by 4.
5. Run validation:

```bash
python scripts/validate_pages.py
```

6. Build a proof PDF:

```bash
python scripts/build_pdf.py
```

The PDF lands in `build/comic-proof.pdf`.

## Recommended page canvas

Use this canvas for full-bleed image generation or upscaling:

```text
2063 px × 3150 px at 300 DPI
```

Keep important faces, text, and speech balloons inside the safe zone. The bleed area is sacrificial paper-meat. Let backgrounds run into it, not lettering.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Print proof rule

Always order one proof before ordering a stack. Screens lie. Paper tells the truth.
