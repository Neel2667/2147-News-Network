# Report — Final Recording Guide and Auto Renderer

Date: 2026-06-16

## What Was Added

Created final pilot recording/edit/upload guides and an optional Playwright + FFmpeg auto-renderer.

## New Production Guides

```text
episodes/pilot-001-mars-independence/FINAL_RECORDING_GUIDE.md
episodes/pilot-001-mars-independence/FINAL_EDIT_ASSEMBLY.md
episodes/pilot-001-mars-independence/FINAL_UPLOAD_PACKAGE.md
```

## New Automated Renderer

```text
scripts/render/render_html_scenes.py
scripts/render/README.md
requirements-render.txt
```

## Renderer Purpose

The renderer opens the final HTML scene pages, captures PNG frames with Playwright/Chromium, encodes each scene with FFmpeg, and concatenates them into a silent MP4.

## Recommended Production Path

Manual OBS recording is still recommended for the first pilot quality pass. The automated renderer is optional and should be used after the HTML scenes are visually approved.

## Auto Renderer Install

```bash
pip install -r requirements-render.txt
python -m playwright install chromium
```

## Auto Renderer Run

```bash
python scripts/render/render_html_scenes.py
```

Output:

```text
outputs/auto-render/2147-001-auto-render-silent.mp4
```
