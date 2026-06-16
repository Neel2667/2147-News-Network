# Render / Export Workflow — 2147 News Network Studio

Last updated: 2026-06-16

## Purpose

This workflow turns edited episode scenes into **video-ready browser assets**.

The current system does not yet render final MP4 automatically. Instead, it creates standalone 1920×1080 HTML render pages for each scene, plus a manifest that tells the editor/producer how long each scene should be recorded.

This is the safest high-quality first step because the visuals are web-rendered, editable, and recordable using OBS or a browser capture workflow.

## In-App Workflow

1. Open the custom app.
2. Click **Load Pilot Episode**.
3. Go to **Scene Timeline**.
4. Tune every scene.
5. Go to **Save, Load & Export Center**.
6. Click **Create Video-Ready Scene Package**.

The app creates:

```text
render_packages/{episode_id}/
  README.md
  manifest.json
  draft.json
  scenes/
    01-s01.html
    02-s02.html
    ...
```

These files are served at:

```text
/renders/{episode_id}/scenes/01-s01.html
```

## What Each Scene File Is

Each scene file is a standalone HTML page with:

- 1920×1080 render frame by default
- full premium template visual
- scene metadata overlay
- correct template controls
- no external network dependency

## Manual OBS Recording Workflow

Recommended first production method:

1. Open each scene render URL in a browser.
2. Set browser zoom to 100%.
3. Use OBS browser/window capture at 1920×1080.
4. Record for the scene's `duration_seconds` from `manifest.json`.
5. Save each clip as:

```text
scene-01-opening-transmission.mp4
scene-02-anchor-lead-in.mp4
...
```

6. Assemble in:

- DaVinci Resolve
- Premiere Pro
- CapCut Desktop
- Final Cut
- or FFmpeg later

7. Add:

- voiceover
- music bed
- sound effects
- subtitles
- final mastering

## Manifest Format

Example:

```json
{
  "package_id": "2147-001-mars-independence",
  "resolution": { "width": 1920, "height": 1080 },
  "total_runtime_seconds": 425,
  "scenes": [
    {
      "index": 1,
      "id": "s01",
      "title": "Opening Transmission",
      "duration_seconds": 15,
      "template": "opening-intro-premium.html",
      "url": "/renders/2147-001-mars-independence/scenes/01-s01.html"
    }
  ]
}
```

## Why Not Automatic MP4 Yet?

Automatic browser-to-video rendering is possible, but it requires more infrastructure:

- Playwright/Chromium
- frame capture
- FFmpeg assembly
- timing control
- font/render consistency
- larger Docker image

For the first production version, OBS/manual render gives better control and fewer deployment problems.

## Future Automated Render Plan

Later, add:

1. Playwright scene recorder
2. PNG frame sequence export
3. FFmpeg MP4 assembly
4. voiceover/subtitle sync
5. render queue in the custom app
6. downloadable final MP4

## Quality Notes

Before recording:

- preview every scene
- check text readability
- check lower-thirds
- check ticker speed
- check template-specific values
- avoid clutter
- keep UI premium and smooth

The goal is not just rendering video — the goal is an international-level broadcast look.
