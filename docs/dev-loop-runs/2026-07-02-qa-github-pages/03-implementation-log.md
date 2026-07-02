# Implementation Log

## OCR And Data
- Rendered the 28-page scanned PDF with Poppler.
- Added `scripts/vision_ocr.swift` to run macOS Vision OCR and emit page/line coordinates.
- Added `scripts/build_questions.py` to parse OCR lines into chapter-aware Q&A records.
- Fixed chapter resets, two-column ordering, merged OCR lines, and missing answer-marker fallback.
- Generated `src/data/questions.json`.

## Web App
- Added a zero-dependency static app in `index.html`, `src/app.js`, and `src/styles.css`.
- Added search, chapter filtering, list review, flashcard mode, answer reveal, and local learned-state persistence.
- Added `assets/source-preview.png` from the first PDF page as a visual source cue.
- Added responsive desktop/mobile layout.

## Build And Deployment Prep
- Added `scripts/validate_data.mjs` for data integrity checks.
- Added `scripts/build_site.mjs` to produce a Pages-ready `dist` folder.
- Added `.github/workflows/pages.yml` to deploy `dist` with GitHub Pages Actions.
- Added `.gitignore` to exclude the source PDF, temporary OCR files, and build output.

## Verification Commands
- `npm test` - passed.
- `npm run build` - passed.
- Browser verification on `http://localhost:4173` - passed.
- Browser verification of built `dist` package on `http://localhost:4174` - passed.

## Browser Evidence
- `artifacts/screenshots/desktop-default.png`
- `artifacts/screenshots/desktop.png`
- `artifacts/screenshots/mobile.png`

## Deployment Status
Local Git repository initialized on `main`. Remote GitHub Pages publishing is blocked because no `gh` CLI is installed and the GitHub connector has no installed accounts or accessible repositories in this environment.
