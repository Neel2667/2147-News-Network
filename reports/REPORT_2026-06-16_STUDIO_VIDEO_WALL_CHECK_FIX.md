# Report — Studio Video Wall Check Fix

Date: 2026-06-16

## Issue

The user said the Studio + Video Wall template was not proper and asked to check it.

## Diagnosis

The fake anchor silhouette was likely making the layout look cheap / not final. The video wall direction is good, but the left anchor area needed to feel more like a professional broadcast information module rather than a fake person.

## Fixes Applied

Updated:

```text
templates/broadcast-v2-studio-video-wall.html
static/studio-video-wall-approval.html
static/pilot-v2-approval.html
```

## Changes

- Removed the fake anchor/person silhouette from the official Studio + Video Wall template.
- Replaced it with a clean anchor desk information card.
- Added animated broadcast lines inside the anchor card.
- Kept the desk base for studio depth.
- Updated approval pages.
- Changed pilot saved asset path for better standalone preview compatibility.

## Current Review Pages

```text
/static/studio-video-wall-approval.html
/static/pilot-v2-approval.html
```
