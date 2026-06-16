# Final Recording Guide — 2147-001 Pilot

Episode: **Mars Votes for Independence From Earth | 2147 News Network**

## Source of Truth

Use the final render package:

```text
outputs/final-pilot-render-package/index.html
```

Individual scene pages:

```text
outputs/final-pilot-render-package/scenes/
```

Do **not** record from older procedural MP4 previews.

## Recording Resolution

Recommended:

```text
1920×1080
24 fps or 30 fps
```

The render pages are built for 1920×1080.

## OBS Setup

### Canvas

```text
Base Canvas: 1920×1080
Output Resolution: 1920×1080
FPS: 30 or 24
```

### Source

Use one of:

```text
Browser Source
Window Capture
Display Capture
```

Recommended for first test:

```text
Window Capture of browser window
```

### Browser Settings

- Use Chrome/Chromium/Edge.
- Set browser zoom to 100%.
- Open each scene page in its own tab.
- Fullscreen browser if possible.
- Hide bookmarks bar.
- Ensure page is at top-left and not scrolled.

## Scene Recording Order

Use `outputs/final-pilot-render-package/manifest.json` as the authoritative scene list.

Current order:

| # | Scene | File | Duration |
|---:|---|---|---:|
| 1 | Opening Transmission | `01-s01.html` | 16s |
| 2 | Anchor Lead-In | `02-s02.html` | 48s |
| 3 | Top Headlines | `03-s03.html` | 38s |
| 4 | Mars Referendum Dashboard | `04-s04.html` | 78s |
| 5 | Historical Context | `05-s05.html` | 62s |
| 6 | Archive Context | `06-s05b.html` | 32s |
| 7 | Expert Quote | `07-s06.html` | 34s |
| 8 | Market Ripple | `08-s07.html` | 52s |
| 9 | Legal Ripple | `09-s08.html` | 50s |
| 10 | Closing Transmission | `10-s09.html` | 24s |

## Clip Naming

Save recordings as:

```text
scene-01-opening-transmission.mp4
scene-02-anchor-lead-in.mp4
scene-03-top-headlines.mp4
scene-04-mars-dashboard.mp4
scene-05-historical-context.mp4
scene-06-archive-context.mp4
scene-07-expert-quote.mp4
scene-08-market-ripple.mp4
scene-09-legal-ripple.mp4
scene-10-closing-transmission.mp4
```

## Recording Tips

- Record 1–2 seconds extra at the start and end of each scene.
- Trim in the editor.
- If a scene has an animated ticker, let it run naturally.
- If video wall footage does not autoplay, click once in the browser and reload.
- Check scene text readability before recording.

## QC Before Editing

- [ ] all clips are 1920×1080
- [ ] no browser UI visible
- [ ] no mouse cursor visible
- [ ] ticker visible and moving
- [ ] anchor visible in Studio Wall scenes
- [ ] footage/poster visible in video wall
- [ ] no elements overlapping or cropped
- [ ] each clip has a few extra frames for trimming
