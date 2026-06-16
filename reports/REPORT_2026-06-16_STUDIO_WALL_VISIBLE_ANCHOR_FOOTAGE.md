# Report — Studio Wall Visible Anchor and Footage Fix

Date: 2026-06-16

## Issue

The user still could not see anchor or footage in the Studio + Video Wall review.

## Fixes Applied

### Footage Visibility

Added a real poster image extracted from the sample video:

```text
static/demo-assets/earth-observations-sample-poster.jpg
```

The Studio Video Wall now shows this poster image immediately, even if the browser does not autoplay/load the MP4. The video still loads on top when available.

### Anchor Visibility

Made the CSS-rendered anchor figure larger and more obvious:

- larger head
- larger torso
- clearer hair/head/neck/body separation
- explicit z-index layering
- anchor desk card remains visible above desk

### Updated Files

```text
templates/broadcast-v2-studio-video-wall.html
static/studio-video-wall-approval.html
static/pilot-v2-approval.html
static/demo-assets/earth-observations-sample-poster.jpg
```

## Review URLs

```text
/static/studio-video-wall-approval.html
/static/pilot-v2-approval.html
```

## Note

If browser cache shows the old version, perform a hard refresh.
