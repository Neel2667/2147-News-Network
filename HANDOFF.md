# Handoff Guide for Future AI/Developer

This file exists so another AI or developer can resume the project without confusion.

## Project Summary

The user wants a complete project for a YouTube channel called **2147 News Network**. It is a fictional news channel broadcasting from the year 2147.

The project should be deployed on Hugging Face Spaces. It should help generate episode scripts, scene plans, and web-based visual templates.

## Critical Constraint

Do not use AI-generated images or AI-generated videos.

Scripts and text may be AI-assisted. Visuals must come from:
- HTML/CSS/SVG/Canvas/WebGL
- public-domain footage
- licensed stock footage
- self-shot footage
- manually designed graphics

## Security Constraint

The user pasted a GitHub token in the chat. Do not use it. Do not save it. Do not paste it into commands. Tell the user to revoke it and create a new token.

## Repository

User repository:

https://github.com/Neel2667/2147-News-Network

If pushing is required, use safe GitHub authentication outside committed files:
- GitHub CLI login
- SSH key
- environment variable provided securely by the platform
- a new revoked/replaced token entered by the user locally, not in chat

## Current File Structure

```text
2147-News-Network/
  README.md
  PROJECT_STATUS.md
  HANDOFF.md
  ROADMAP.md
  requirements.txt
  app.py
  .gitignore
  docs/
  reports/
  episodes/
  templates/
  assets/
  src/
```

## Recommended Next Step

Finish the MVP Gradio app:
- topic input
- generate headlines
- generate script
- generate scene list
- export outputs
- preview visual templates

## MVP Visual Templates

Build these first:
1. opening intro
2. anchor desk
3. headline cards
4. Mars dashboard
5. data chart
6. quote/interview card
7. breaking news alert
8. closing transmission

## First Episode

Title:

**Mars Votes for Independence From Earth | 2147 News Network**

Main story:
Mars enters final voting cycle for independence from Earth Union.

Supporting stories:
- Lunar miners demand oxygen-credit reform
- Pacific floating cities activate storm shields
- Neural privacy treaty passes Earth Union Senate
- Europa probe detects repeating acoustic signal

## Style

Visual style:
- dark navy/black
- cyan holographic UI
- amber/red warnings
- futuristic newsroom
- moving tickers
- animated maps
- dashboards
- serious broadcast tone

## Important Docs

Read in this order:
1. README.md
2. PROJECT_STATUS.md
3. docs/CHAT_CONTEXT.md
4. docs/PREMIUM_UI_DESIGN_SYSTEM.md
5. docs/MASTER_PLAN.md
4. docs/CONTENT_BIBLE.md
5. docs/VISUAL_POLICY.md
6. docs/PRODUCTION_PIPELINE.md
7. docs/REALISM_GUIDE.md
8. docs/CAUSAL_EVENT_ENGINE.md
9. data/events.json
10. data/people.json
11. data/organizations.json
12. data/locations.json
13. data/source_agencies.json
14. episodes/episode-001-mars-independence.json


## Realism Update

The user wants the channel to feel extremely real and specific. Avoid vague references like "the CEO said". Use full names, titles, organizations, locations, timestamps, and source labels. Example: "Helion Grid Systems CEO Jiang Lau said..." Read docs/REALISM_GUIDE.md before generating scripts.


## Causal Event Engine Update

The user wants news to emerge from cause-and-effect, not isolated headline generation. Every event should have causes and ripple effects. Use data/events.json as the beginning of the world timeline. Read docs/CAUSAL_EVENT_ENGINE.md before changing the generator.


## Chat Context File

A curated planning record has been saved at docs/CHAT_CONTEXT.md. It excludes secrets and should be read by any future agent before continuing.


## Premium UI Priority

The user emphasized that UI quality is the main success factor. If the UI looks cheap, nobody will watch, even if the writing is good. Use docs/PREMIUM_UI_DESIGN_SYSTEM.md as a mandatory design reference. The target is Apple-inspired polish: minimal, beautiful typography, glass depth, restrained colors, smooth premium animation, and no cheap cyberpunk clutter.


## Premium UI Templates Built

The first premium UI templates are implemented and pushed. See `reports/REPORT_2026-06-16_PREMIUM_UI_TEMPLATES.md`. The Gradio app now includes a Premium Visual Preview tab. Templates are self-contained HTML/CSS snippets under `templates/`, rendered via `src/template_renderer.py`.


## Custom App Direction

The user rejected a Gradio-first URL because they want a fully controlled custom app with all newsroom controls. The production direction is now FastAPI + custom HTML/CSS/JS. Read docs/CUSTOM_APP_ARCHITECTURE.md and prioritize main.py/static files over app.py.


## Scene Timeline Editor

The custom app now has a Scene Timeline panel and Template Control Panel. Users can edit scene order, duration, selected template, headline, summary, lower-third, ticker, and source label, then preview the selected scene. See reports/REPORT_2026-06-16_SCENE_TIMELINE_EDITOR.md.


## Episode Save/Load and Pilot Package

The custom app now supports saving and loading episode drafts via `/api/episodes` endpoints. Saved drafts live under `episodes/saved/`. The first pilot production package is at `episodes/pilot-001-mars-independence/`, and a loadable saved draft exists at `episodes/saved/2147-001-mars-independence.json`. See `reports/REPORT_2026-06-16_SAVE_LOAD_AND_PILOT.md`.


## Specialized Premium Templates

Built `historical-timeline.html`, `financial-desk.html`, `legal-desk.html`, and `breaking-news.html`. The pilot saved draft now uses specialized templates for historical context, market ripple, and legal ripple scenes. See `reports/REPORT_2026-06-16_SPECIALIZED_PREMIUM_TEMPLATES.md`.


## Template-Specific Controls

The Scene Timeline panel now shows template-specific controls for Historical Timeline, Financial Desk, Legal Desk, and Breaking News. Values are saved under `scene.template_controls` and passed into template rendering. See `reports/REPORT_2026-06-16_TEMPLATE_SPECIFIC_CONTROLS.md`.


## Science Climate Lunar Templates

Built `science-desk.html`, `earth-climate-map.html`, and `lunar-report.html` with template-specific controls in the Scene Timeline panel. See `reports/REPORT_2026-06-16_SCIENCE_CLIMATE_LUNAR_TEMPLATES.md`.


## Pilot Loader and Deployment Guide

The custom app now has a one-click Load Pilot Episode button in the top bar and dashboard. It loads `2147-001-mars-independence` from `episodes/saved/`. A Hugging Face Docker deployment guide exists at `docs/HUGGING_FACE_DEPLOYMENT.md`. The app has `/health` endpoint.


## Render Export Workflow

The app now has a render package workflow via `POST /api/render/package` and a UI button in Save, Load & Export Center. It creates standalone 1920x1080 HTML scene pages under `render_packages/{episode_id}/`, served from `/renders/{episode_id}/`. Read `docs/RENDER_EXPORT_WORKFLOW.md` and `reports/REPORT_2026-06-16_RENDER_EXPORT_WORKFLOW.md`.


## Download Buttons

The Export Center now shows download links for exported files and render packages, including ZIP bundles. `/exports` serves production exports; `/renders` serves render packages. Runtime artifacts are ignored by Git. Read `docs/DOWNLOADS_AND_PACKAGES.md`.


## Pilot UI Polish Review

The pilot episode has been reviewed and polished scene by scene. See `episodes/pilot-001-mars-independence/ui_polish_review.md` and `ui_review_contact_sheet.html`. The saved pilot draft has been updated. Quote card now has template-specific controls. Next: manually preview at 1920x1080 and do an OBS recording test.


## Pilot Audio Plan

Added sound design, voiceover timing, audio cue sheet, and subtitle draft under `episodes/pilot-001-mars-independence/audio/`. The audio direction is premium international news with restrained futuristic sound design. See `reports/REPORT_2026-06-16_AUDIO_PLAN.md`.


## Launch Package

Added pilot launch package under `launch/` and non-AI HTML/CSS thumbnail concept under `thumbnails/pilot-001/`. Read `launch/LAUNCH_PACKAGE.md` and `reports/REPORT_2026-06-16_LAUNCH_PACKAGE.md`.


## Final Hugging Face Deploy Prep

Root README now has Hugging Face Space metadata for Docker. Added `.dockerignore`, `docs/HF_SPACE_METADATA.md`, `docs/FINAL_DEPLOY_CHECKLIST.md`, and `docs/DEPLOYMENT_STATUS.md`. Next action: create a Hugging Face Docker Space and connect this GitHub repo.


## Demo Video Generated

A silent code-rendered demo video has been created at `outputs/demo-video/2147-demo-pilot-ui.mp4` with poster `outputs/demo-video/2147-demo-poster.png`. It is not AI-generated video; it is procedural Python/Pillow/OpenCV motion graphics. Generator script: `scripts/generate_demo_video.py`. See `reports/REPORT_2026-06-16_DEMO_VIDEO.md`.


## Demo Video Browser Fix

The original demo MP4 used mp4v and may not play in browser previews. It has been replaced with browser-compatible H.264/avc1 yuv420p faststart at `outputs/demo-video/2147-demo-pilot-ui.mp4`. `scripts/generate_demo_video.py` now transcodes with imageio-ffmpeg.


## Broadcast V2 Rebuild

The user strongly rejected the first demo as pathetic and not watchable. A new direction has started: real broadcast news package, not generic sci-fi UI. Read `docs/BROADCAST_REBUILD_RESEARCH_AND_PLAN.md`. New demo: `outputs/demo-video/2147-broadcast-v2-demo.mp4`. Next agent should rebuild templates around V2 broadcast style.


## Core Broadcast Elements Review Page

Created `static/core-broadcast-elements.html` as the review page for the new V2 news-channel identity system. It showcases the core elements first: bug, LIVE bug, clock, lower thirds, ticker, headline/breaking straps, source chips, motion tests, and palette. User wants to approve these before larger templates are rebuilt.


## Core Elements Polish Fixes

User requested more polish: ticker overlapped label, name straps overflowed, and elements felt static. Fixed `static/core-broadcast-elements.html` with protected ticker window, safer lower-third text overflow handling, and animation loops for core elements. See `reports/REPORT_2026-06-16_CORE_ELEMENTS_POLISH_FIXES.md`.


## Ticker and Animation Variation Fix

User said ticker text disappeared and animations were too similar. Updated `static/core-broadcast-elements.html`: ticker text now visible immediately in a protected ticker window, and animations vary by element type. See `reports/REPORT_2026-06-16_TICKER_AND_ANIMATION_VARIATION_FIX.md`.


## Strap and Name Strap Layout Fix

User reported strap small text overflowing and anchor names disappearing in name straps. Fixed `static/core-broadcast-elements.html` by reducing side column widths, adding overflow/ellipsis handling, reducing font sizes, and extending animation hold time. See `reports/REPORT_2026-06-16_STRAP_AND_NAMESTRAP_LAYOUT_FIX.md`.


## Long Name Strap Fix

User said long names cannot be truncated. Updated `static/core-broadcast-elements.html`: lower-third examples are now full-width stacked layouts, names wrap naturally, ellipsis removed, long-name example added. See `reports/REPORT_2026-06-16_LONG_NAME_STRAP_FIX.md`.


## Apple-Inspired Core Polish

User asked to take inspiration from Apple colors, shapes, and animations. Updated `static/core-broadcast-elements.html` with material-like depth, rounded shapes, subtle shadows, backdrop blur, refined pills, and varied fluid motion. Added report `reports/REPORT_2026-06-16_APPLE_INSPIRED_CORE_POLISH.md`.


## Label Alignment Fix

User noted the BREAKING red label extended farther than the HEADLINES label. Fixed by matching ticker label width to strap label width in `static/core-broadcast-elements.html`.


## Broadcast System V2 Extraction

Approved core elements have been extracted into `static/broadcast-system.css` and `static/broadcast-components.js`. Showcase: `/static/broadcast-system-showcase.html`. Documentation: `docs/BROADCAST_SYSTEM_V2.md`. Next: rebuild V2 templates using these components only.


## First Broadcast V2 Templates

Built the first five full Broadcast V2 templates and updated pilot scenes s01-s05 to use them. See `reports/REPORT_2026-06-16_BROADCAST_V2_FIRST_TEMPLATES.md`. Next rebuild s06-s09: expert split, financial board, legal board, close.


## Broadcast V2 Pilot Complete

All nine pilot scenes now use Broadcast System V2 templates. Approval page: `/static/pilot-v2-approval.html`. New templates: expert split, financial board, legal board, close. See `reports/REPORT_2026-06-16_BROADCAST_V2_REMAINING_TEMPLATES.md`.


## Pilot V2 Approval Standalone Fix

User hit fetch parse URL error on `/static/pilot-v2-approval.html`. The page is now standalone with inlined CSS and pre-rendered scenes, no API needed. See `reports/REPORT_2026-06-16_APPROVAL_PAGE_STANDALONE_FIX.md`.


## Pilot V2 Overlap Fix

User reported elements overlapping in the approval board. Fixed by creating protected lower graphics space in templates, moving anchor lower-third above ticker, making approval page full-size on large screens, and adding `scripts/build_pilot_v2_approval.py` to regenerate approval page. See `reports/REPORT_2026-06-16_PILOT_V2_OVERLAP_FIX.md`.


## Cropping Space Fix

User reported elements cropping due to limited space. Compacted V2 templates and regenerated `static/pilot-v2-approval.html`. See `reports/REPORT_2026-06-16_CROPPING_SPACE_FIX.md`.


## Asset Integration Review Page

Created `static/asset-integration-review.html` for user approval. It shows how stock footage, maps, archive footage, field reports, and info cards will be integrated with the V2 broadcast graphics. No real stock assets yet; only procedural placeholders.


## Asset Final Look Options

User said the asset integration page looked like a wireframe. Created `static/asset-final-look-options.html` with more finished visual directions for approval: Clean Global News, Studio Video Wall, Apple-Clean Premium Report, and Data-Heavy Bloomberg Style.


## Real Footage Final Look Options

User requested actual downloaded sample video, not wireframes. Downloaded NASA/public-domain sample footage to `assets/footage/nasa/earth-observations-sample.mp4`, created `static/asset-final-look-options.html`, and generated `outputs/final-look-options/2147-real-footage-options.mp4`. See `reports/REPORT_2026-06-16_REAL_FOOTAGE_OPTIONS_DEMO.md`.


## Official Studio Video Wall Template

User chose Option B as preferred direction. Built `templates/broadcast-v2-studio-video-wall.html`, mounted `/assets`, updated pilot scene s02, and added `static/studio-video-wall-approval.html` for approval. See `reports/REPORT_2026-06-16_OFFICIAL_STUDIO_VIDEO_WALL_TEMPLATE.md`.


## Studio Video Wall Check Fix

User said Studio + Video Wall was not proper. Removed fake anchor silhouette from `broadcast-v2-studio-video-wall.html` and replaced it with a clean anchor desk info card. Regenerated `/static/studio-video-wall-approval.html` and `/static/pilot-v2-approval.html`.


## Studio Wall Anchor and Footage Fix

User said Studio + Video Wall had no anchor or footage. Reintroduced CSS-rendered anchor figure and moved sample footage to `static/demo-assets/earth-observations-sample.mp4` for reliable preview. Template has fallback animated footage layer if video fails.


## Studio Wall Visible Anchor and Footage Fix

User still saw no anchor/footage. Added `static/demo-assets/earth-observations-sample-poster.jpg`, inserted visible poster under video, enlarged CSS anchor figure, and regenerated approval pages. If old page appears, hard refresh.


## Studio Video Wall Direct Review

Added `static/studio-video-wall-direct-review.html` because user could not see anchor/footage in previous review pages. This page is self-contained and should be used for direct visual approval.


## Direct Image Review Fix

User still could not see anchor/footage in HTML/CSS preview. Created `static/studio-video-wall-direct-review.png` and changed direct review page to display the rendered image. If user approves, convert this exact composition into animated reusable template.


## Approved Studio Template Rebuild

User approved the direct rendered Studio + Video Wall image. Converted that composition into `templates/broadcast-v2-studio-video-wall.html` with visible CSS anchor and footage wall. Direct image remains as reference.


## Studio Wall Variant Templates

Built variants: `broadcast-v2-studio-wall-footage.html`, `broadcast-v2-studio-wall-map.html`, `broadcast-v2-studio-wall-data.html`, `broadcast-v2-studio-wall-quote.html`, `broadcast-v2-studio-wall-archive.html`. Next create approval page for all variants.
