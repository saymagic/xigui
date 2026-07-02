# Requirements Baseline

## Goal
Build a complete, responsive Q&A study website from `2025年系规-案例论文必背300问.pdf`, verify it with real local tests, and deploy it with GitHub Pages.

## Non-goals
- Do not rewrite or editorially alter the source content beyond OCR cleanup needed for readability.
- Do not require a backend service or user account.
- Do not depend on remote assets at runtime.

## User-visible Behavior
- A static web app opens directly to the study experience.
- Users can search questions and answers.
- Users can filter by chapter/category.
- Users can switch between list review and flashcard-style memorization.
- Answers can be hidden/revealed for recitation practice.
- The layout works well on desktop and mobile screens.
- Progress/favorite-like study state can persist locally when practical.

## Acceptance Criteria
- The PDF is processed into structured Q&A data.
- The app renders all parsed questions with question text, answer text, chapter, and optional mnemonic/keywords.
- Search and chapter filters work without page reloads.
- Desktop and mobile viewports are visually verified in a browser.
- Build/test commands pass.
- GitHub Pages deployment is complete or any external blocker is documented with exact next steps.

## Constraints
- Current workspace starts with only the PDF file and no Git repository.
- The PDF has no embedded text layer and must be OCR'd from rendered pages.
- The final site should be static and suitable for GitHub Pages.

## Assumptions
- OCR errors are acceptable only if minimized and the site remains useful for review.
- GitHub deployment may require local `gh` authentication and/or creating a new repository if no remote exists.
- A Vite static app is appropriate because the repo is empty and GitHub Pages can serve the built output.

## Open Questions
- None blocking. If no existing GitHub remote exists, create or use a Pages-capable repository through available local GitHub tooling when possible.

## Source Request
`/goal 结合文档制作一个问答的网页，支持好pc和移动端的适配。保证完整可用，且做过真实的测试。然后从GitHub Pages进行部署。`

## Repo Context
- Path: `/Users/saymagic/workspace/xigui`
- Initial contents: `2025年系规-案例论文必背300问.pdf`
- Git status at start: not a Git repository.
- Feature loop dependency note: required Superpowers skills were unavailable, so this run uses a reduced inline workflow with artifacts.
