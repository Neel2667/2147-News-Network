# Report — Render / Export Workflow

Date: 2026-06-16

## What Was Built

Added the first render/export workflow for turning edited 2147 News Network scenes into video-ready browser assets.

## New Backend Endpoint

```text
POST /api/render/package
```

This creates a render package from the current episode draft.

## New Render Package Output

Render packages are written to:

```text
render_packages/{episode_id}/
```

Each package includes:

```text
README.md
manifest.json
draft.json
scenes/*.html
```

Each scene HTML is a standalone 1920×1080 browser-rendered page suitable for OBS recording or future automation.

## New App UI

The Save, Load & Export Center now includes:

```text
Create Video-Ready Scene Package
```

The app returns links to:

- manifest.json
- render README
- each scene render page

## New Static Route

Render packages are served from:

```text
/renders/{package_id}/...
```

## Documentation Added

Created:

```text
docs/RENDER_EXPORT_WORKFLOW.md
scripts/README_RENDER.md
```

## Current Workflow

For now, the recommended production workflow is:

1. Create render package in app.
2. Open each standalone scene page.
3. Record with OBS at 1920×1080.
4. Assemble clips in DaVinci Resolve/Premiere/CapCut.
5. Add voiceover, music, SFX, subtitles, and final mastering.

## Why This Approach

It avoids heavy automated video-render dependencies for the first version and gives better manual quality control.

## Future Work

Later add:

- Playwright/Chromium capture
- FFmpeg assembly
- audio/subtitle sync
- downloadable MP4 output
- render queue inside app
