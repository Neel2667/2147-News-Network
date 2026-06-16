# Report — Final Pilot Render Package

Date: 2026-06-16

## What Was Created

Created the final pilot render package from the approved exact HTML scenes.

## Output Folder

```text
outputs/final-pilot-render-package/
```

## Files

```text
outputs/final-pilot-render-package/index.html
outputs/final-pilot-render-package/README.md
outputs/final-pilot-render-package/manifest.json
outputs/final-pilot-render-package/scenes/*.html
outputs/final-pilot-render-package/2147-001-final-pilot-render-package.zip
```

## Resolution

The render scenes are set up for:

```text
1920x1080
```

The approved 1280x720 compositions are scaled by 1.5 inside the render pages.

## Recording Workflow

1. Open `outputs/final-pilot-render-package/index.html`.
2. Open each scene page in `scenes/`.
3. Record each scene at 1920x1080 with OBS/browser capture.
4. Use `manifest.json` for durations.
5. Assemble in video editor.
6. Add voiceover, music, SFX, and subtitles.

## Important

This package is generated from the approved HTML templates. It replaces rough procedural MP4 previews for production recording.

## Generator

```text
scripts/build_final_pilot_render_package.py
```
