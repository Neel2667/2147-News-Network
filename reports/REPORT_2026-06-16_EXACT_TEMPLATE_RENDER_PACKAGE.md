# Report — Exact Template Render Package

Date: 2026-06-16

## Issue

The user correctly reported that the generated preview video did not match the designed templates and looked much lower quality.

## Cause

The MP4 preview was generated with a separate Python/Pillow/OpenCV drawing script. It was only an approximation, not a browser render of the approved HTML templates.

## Fix / New Direction

The preview source of truth is now the actual HTML templates, not procedural approximation videos.

## New Exact Render Package

Created:

```text
outputs/pilot-exact-render/index.html
outputs/pilot-exact-render/scenes/*.html
outputs/pilot-exact-render/manifest.json
```

## Generator

```text
scripts/build_exact_pilot_render_pages.py
```

## Purpose

This renders the actual saved pilot scene templates into standalone HTML pages. This should be used for visual approval and OBS/browser recording.

## Important

Do not use the old generated MP4 for quality approval. It does not represent the approved design accurately.

Use:

```text
outputs/pilot-exact-render/index.html
```

as the review entry point.
