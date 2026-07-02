# Implementation Plan

## Architecture Summary
Create a Vite static app. OCR the PDF into structured JSON, normalize questions, and render a responsive Q&A study interface entirely in the browser.

## Files Expected To Change
- `package.json`, `index.html`, `src/*`
- `scripts/vision_ocr.swift` for macOS Vision OCR
- `scripts/build_questions.py` for parsing OCR output into app data
- `docs/dev-loop-runs/2026-07-02-qa-github-pages/*` for process evidence
- `.github/workflows/pages.yml` for GitHub Pages deployment

## Task Order
1. Render PDF pages and OCR them with page/line coordinates.
2. Parse OCR lines into chapter-aware Q&A records.
3. Create the Vite app and responsive study UI.
4. Add automated checks for data integrity and build.
5. Run local browser verification on desktop and mobile viewport sizes.
6. Initialize Git/GitHub Pages deployment if possible.
7. Record verification and acceptance evidence.

## Test Strategy
- Data integrity check: question count, required fields, duplicate IDs, empty answer detection.
- Build check: `npm run build`.
- Browser check: open local app, verify nonblank render, search/filter/reveal interactions, screenshot desktop/mobile.
- Deployment check: push GitHub Pages workflow or deploy branch and verify the published URL if credentials allow.

## Risks
- OCR may misread Chinese punctuation or color-highlighted text.
- The first page includes cover/table-of-contents content in the left column, so parsing must ignore non-question text.
- GitHub Pages deployment may be blocked if no authenticated GitHub account is available locally.

## Acceptance Mapping
- Requirements PDF processing: Tasks 1-2.
- Responsive app: Task 3 plus browser screenshots.
- Complete usability: Tasks 3-4.
- Real testing: Tasks 4-5.
- GitHub Pages: Task 6.
