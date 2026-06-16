# Project Status — 2147 News Network

Last updated: 2026-06-15

## Project Goal

Create a Hugging Face deployable web app that helps produce a YouTube channel called **2147 News Network**, a fictional future-news broadcast from the year 2147.

The app should generate scripts, visual plans, scene breakdowns, and browser-based motion graphic previews without using AI-generated images or videos.

## Security Note

A GitHub token was shared in chat by the user. It must **not** be committed, copied into files, stored in environment examples, or used in commands. The user should revoke it and create a fresh token if needed.

## Completed So Far

- Defined the channel concept.
- Defined the no-AI-image/video rule.
- Planned the core episode format.
- Planned recurring news categories.
- Planned reusable visual templates.
- Created initial repository structure.
- Created documentation files.
- Created initial Hugging Face/Gradio app scaffold.
- Created first episode seed data.
- Created first HTML visual preview template.
- Added realism guide for names, organizations, quotes, sources, timestamps, and continuity.
- Added causal event engine plan and initial data files for events, people, organizations, locations, and source agencies.
- Added curated chat context file so future agents can understand the planning history without reading raw chat logs.
- Added premium UI design system emphasizing Apple-inspired polish, minimalism, glass panels, typography, and smooth motion.
- Built premium UI template system with opening intro, anchor desk, headline cards, Mars dashboard, quote card, closing transmission, template renderer, and preview support.
- Started custom FastAPI app to replace Gradio-first workflow, with a premium custom UI and API endpoints.
- Built scene timeline editor and template control panel for editing scene order, duration, templates, lower-thirds, tickers, source labels, and previews.
- Built episode save/load support and created the first pilot episode package for Mars Votes for Independence From Earth.
- Built specialized premium templates: Historical Timeline, Financial Desk, Legal Desk, and Breaking News. Updated pilot scenes to use them.
- Built template-specific controls for Historical Timeline, Financial Desk, Legal Desk, and Breaking News templates.
- Built Science Desk, Earth Climate Map, and Lunar Report premium templates with template-specific controls.
- Added polished one-click pilot loader, dashboard pilot card, health endpoint, and Hugging Face Docker deployment guide.
- Built render/export workflow that creates standalone 1920x1080 scene HTML files, manifest.json, README, and draft.json for OBS/browser recording.
- Added download buttons/links and ZIP bundles for exported production files and render packages.
- Reviewed and polished the pilot episode UI scene by scene; tightened pacing, improved tickers/source labels, added UI review notes, dynamic quote-card controls, and contact sheet.
- Added pilot sound design plan, voiceover timing plan, audio cue sheet, and subtitle draft.
- Added thumbnail and channel launch package for the pilot, including non-AI HTML/CSS thumbnail concept, channel About, YouTube description, pinned comment, upload checklist, and shorts plan.
- Prepared Hugging Face deployment metadata, final deploy checklist, deployment status doc, and .dockerignore.
- Generated a silent code-rendered demo video preview of the pilot UI at 1280x720, 24fps, 42 seconds.
- Re-encoded demo video as browser-compatible H.264/avc1 yuv420p with faststart because mp4v may not play in browser previews.


## In Progress

- Building deterministic script and scene-plan generator.
- Building web-rendered motion graphic templates.
- Preparing Hugging Face Space deployment files.

## Not Started Yet

- Full HTML-to-video export.
- Stock/NASA footage library manager.
- Voiceover pipeline.
- Automated subtitles.
- Advanced timeline editor.
- Advanced map/globe renderer.
- YouTube metadata optimizer.

## Immediate Next Tasks

1. Revoke exposed GitHub token.
2. Push current scaffold to GitHub using safe authentication.
3. Expand Gradio app features:
   - editable episode script
   - editable scene list
   - scene template selection
   - export JSON/text files
4. Connect app.py to data/events.json and generate stories from event ripples.
5. Create Hugging Face Docker Space and connect GitHub repo.
6. Manually preview pilot in deployed app at 1920x1080 and perform OBS recording test.
6. Add video render/export workflow later.
   - anchor desk
   - Mars dashboard
   - breaking news alert
   - data chart
   - quote card
5. Add production documentation for first 10 episodes.

## Definition of Done for MVP

The MVP is complete when a user can:

1. Open the Hugging Face Space.
2. Enter an episode topic.
3. Generate 5–7 future headlines.
4. Generate a full episode script.
5. Generate a scene-by-scene visual plan.
6. Preview at least 5 browser-rendered visual scenes.
7. Export script, subtitles draft, scene JSON, and production notes.


## Broadcast V2 Rebuild

- User rejected first demo as poor quality.
- Started Broadcast V2 rebuild based on real TV news package structure.
- Added `docs/BROADCAST_REBUILD_RESEARCH_AND_PLAN.md`.
- Added `scripts/generate_broadcast_v2_demo.py`.
- Generated `outputs/demo-video/2147-broadcast-v2-demo.mp4`.
- Next: rebuild app templates around V2 broadcast package style.


## Core Broadcast Elements Review

- Created `static/core-broadcast-elements.html` to review logo bug, LIVE bug, clock, lower thirds, straps, ticker, source chips, motion tests, and palette before rebuilding full templates.
- Added sidebar link from custom app.


## Core Elements Polish Fixes

- Fixed ticker overlap with Headlines label.
- Fixed lower-third/name-strap text overflow.
- Added animation pass to core elements: bug, LIVE, clock, sources, story cards, OTS, straps, lower thirds, ticker, and tiles.


## Ticker and Animation Variation Fix

- Fixed ticker text disappearing by removing off-screen padding and using duplicated visible ticker spans.
- Added varied animations: bug shine, live pulse, story slide, OTS zoom, strap wipe, breaking slide, lower-third variations, data bar grow, source sweep.


## Strap and Name Strap Layout Fix

- Fixed small text overflow in headline/breaking straps.
- Fixed name strap spacing so anchor/expert names remain visible.
- Added safer ellipsis behavior and longer animation hold times.


## Long Name Strap Fix

- Removed truncation from name straps.
- Rebuilt lower-third review as full-width stacked examples.
- Long names now wrap instead of disappearing.


## Apple-Inspired Core Polish

- Applied Apple-inspired polish to core broadcast elements: layered material surfaces, soft depth, rounded shapes, restrained colors, varied fluid motion, and clearer hierarchy.
- Added Apple-inspired polish section to `static/core-broadcast-elements.html`.


## Label Alignment Fix

- Aligned `BREAKING` and `HEADLINES` red label widths in the core broadcast elements page.


## Broadcast System V2 Extraction

- Created `static/broadcast-system.css` and `static/broadcast-components.js`.
- Created `static/broadcast-system-showcase.html`.
- Added `docs/BROADCAST_SYSTEM_V2.md`.
- Future V2 templates must use these reusable components.


## First Broadcast V2 Templates

- Built first five full templates using `broadcast-system.css`: cold open, anchor studio, top stories, Mars data board, and timeline.
- Updated first five pilot scenes to use V2 templates.


## Broadcast V2 Pilot Complete

- Built remaining V2 templates: expert split, financial board, legal board, close.
- Updated all nine pilot scenes to Broadcast System V2.
- Added `static/pilot-v2-approval.html` for user approval.


## Pilot V2 Approval Standalone Fix

- Fixed approval board API fetch error by making `static/pilot-v2-approval.html` standalone with inlined CSS and pre-rendered scenes.


## Pilot V2 Overlap Fix

- Fixed overlap between main content, straps, lower thirds, and tickers in V2 templates.
- Anchor lower third now sits above ticker.
- Approval page now displays full-size 1280x720 scenes on large screens.
- Added `scripts/build_pilot_v2_approval.py`.


## Cropping / Space Fix

- Compacted V2 pilot templates to prevent cropped elements.
- Regenerated standalone approval page.


## Asset Integration Review Page

- Created `static/asset-integration-review.html` showing how stock footage, maps, archive footage, field reports, and info cards will appear inside Broadcast System V2.


## Asset Final Look Options

- Created `static/asset-final-look-options.html` with four finished-looking directions for footage/maps/info integration: clean global news, studio video wall, Apple-clean premium report, and data-heavy Bloomberg style.


## Real Footage Final Look Options

- Downloaded NASA/public-domain Earth observations sample footage.
- Created `static/asset-final-look-options.html` with more finished options.
- Generated `outputs/final-look-options/2147-real-footage-options.mp4` showing four final-look directions with real sample footage.
- Added asset license log and manifest.


## Official Studio Video Wall Template

- User selected Option B as preferred style.
- Built `templates/broadcast-v2-studio-video-wall.html`.
- Mounted `/assets` in FastAPI for video assets.
- Updated pilot scene s02 to use official Studio + Video Wall template.
- Added `static/studio-video-wall-approval.html`.


## Studio Video Wall Check Fix

- Removed fake anchor silhouette from official Studio + Video Wall template.
- Replaced with cleaner anchor desk information card and animated broadcast lines.
- Regenerated Studio Video Wall and Pilot V2 approval pages.


## Studio Wall Anchor and Footage Fix

- Reintroduced a CSS-rendered anchor figure in Studio + Video Wall.
- Added visible real video wall support and fallback footage layer.
- Copied sample footage to `static/demo-assets/` for reliable preview.


## Studio Wall Visible Anchor and Footage Fix

- Added poster image extracted from sample footage so video wall is visible even if video autoplay fails.
- Enlarged CSS anchor figure and added z-index layering.
- Regenerated approval pages.


## Studio Video Wall Direct Review

- Added `static/studio-video-wall-direct-review.html` as a self-contained page to verify anchor and footage visibility.


## Direct Image Review Fix

- Created `static/studio-video-wall-direct-review.png` and simplified review page to show guaranteed rendered image preview with anchor and footage visible.


## Approved Studio Template Rebuild

- User approved direct Studio + Video Wall composition.
- Rebuilt `broadcast-v2-studio-video-wall.html` to match approved image with visible anchor and footage wall.
- Regenerated pilot approval page.


## Studio Wall Variant Templates

- Built Studio Wall variants: footage, map, data, quote, archive.
- These extend the approved Studio + Video Wall direction into reusable story formats.


## Studio Wall Variants Approval Page

- Created `static/studio-wall-variants-approval.html`.
- Added generator script `scripts/build_studio_wall_variants_approval.py`.
- Page shows footage, map, data, quote, and archive variants for approval.


## Studio Wall Variants Approved

- User approved all Studio Wall variants: footage, map, data, quote, archive.
- Updated pilot scene plan to use all approved variants.
- Added `s05b Archive Context` scene using archive variant.
- Regenerated `static/pilot-v2-approval.html`.


## Pilot Studio Wall Preview Video

- Generated `outputs/pilot-preview/2147-pilot-studio-wall-preview.mp4` using approved Studio Wall variants.
- Added generator script `scripts/generate_pilot_studio_wall_preview.py`.
