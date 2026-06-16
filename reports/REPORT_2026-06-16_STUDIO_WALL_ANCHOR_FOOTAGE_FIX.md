# Report — Studio Wall Anchor and Footage Fix

Date: 2026-06-16

## User Feedback

The user reported that the Studio + Video Wall template had no anchor or footage visible.

## Fixes Applied

Updated:

```text
templates/broadcast-v2-studio-video-wall.html
static/studio-video-wall-approval.html
static/pilot-v2-approval.html
```

## Anchor Fix

- Reintroduced a CSS-rendered anchor figure.
- Added a more polished anchor desk card with anchor name/title.
- Kept the studio desk base.
- Avoided AI-generated or photorealistic avatar imagery.

## Footage Fix

- Copied NASA sample footage into:

```text
static/demo-assets/earth-observations-sample.mp4
```

- Updated Studio + Video Wall template to use a video wall with:
  - real video source support
  - fallback animated footage layer if video does not load
  - `onloadeddata` opacity reveal

## Updated Pilot

Pilot scene s02 now points to:

```text
/static/demo-assets/earth-observations-sample.mp4
```

## Current Review Pages

```text
/static/studio-video-wall-approval.html
/static/pilot-v2-approval.html
```
