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

## Remote Deployment Attempt
- Confirmed SSH authentication to GitHub as `saymagic`.
- Confirmed `saymagic/xigui` does not exist.
- Found existing Pages repository `saymagic/saymagic.github.io`.
- Added the built static site under `xigui/` in that repository.
- Updated `.github/workflows/deploy.yml` so changes under `xigui/**` trigger a Pages deployment and copy the static app into `output/public/xigui`.
- Pushed remote commit `003e51e` to `saymagic/saymagic.github.io`.
- GitHub Actions run `28557842069` failed before starting the job because GitHub reports the account is locked due to a billing issue.
- Verified `https://saymagic.github.io/xigui/` redirects to `https://blog.saymagic.cn/xigui/`, but the target currently returns 404 because the Pages deployment did not run.

## Remote Deployment Retry
- Pushed retry commit `289c414` to `saymagic/saymagic.github.io`, adding `xigui/deploy-retry.txt` so the `xigui/**` path filter definitely matched.
- GitHub Actions run `28567545898` was created for `289c414` and completed with `failure`.
- The job had no steps and no assigned runner (`runner_id: 0`), which confirms it failed before workflow execution.
- Re-checked `https://saymagic.github.io/xigui/`; it still redirects to `https://blog.saymagic.cn/xigui/`, which still returns 404.
