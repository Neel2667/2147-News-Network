# Report — Cropping / Space Fix for Pilot V2

Date: 2026-06-16

## User Feedback

The user reported that some elements were cropping because of insufficient space.

## Fixes Applied

Updated all V2 pilot templates with more conservative spacing and smaller internal typography where needed.

## Main Changes

- Increased usable content height while preserving the lower graphics zone.
- Reduced oversized headline typography in dense scenes.
- Reduced padding in data-heavy boards.
- Compacted anchor silhouette and desk layout.
- Compacted data board stats and Mars zone card.
- Compacted timeline typography and event spacing.
- Compacted expert split portrait and quote typography.
- Compacted financial and legal board metrics/quotes/charts.
- Compacted closing screen headline and copy.
- Regenerated standalone approval page.

## Files Updated

```text
templates/broadcast-v2-anchor-studio.html
templates/broadcast-v2-top-stories.html
templates/broadcast-v2-mars-data.html
templates/broadcast-v2-timeline.html
templates/broadcast-v2-expert-split.html
templates/broadcast-v2-financial-board.html
templates/broadcast-v2-legal-board.html
templates/broadcast-v2-close.html
static/pilot-v2-approval.html
```

## Current Status

Pilot V2 approval page should now show all scenes with less cropping and better spacing.
