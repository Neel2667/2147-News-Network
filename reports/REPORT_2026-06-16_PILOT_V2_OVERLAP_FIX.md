# Report — Pilot V2 Overlap Fix

Date: 2026-06-16

## Issue

The user reported that elements were overlapping each other on the Pilot V2 Approval page.

## Root Causes

1. Main scene content areas extended too far downward and overlapped the lower headline strap area.
2. The Anchor Studio scene had a lower third and ticker occupying the same bottom area.
3. The approval page scaled scenes down, which made overlaps look worse and made review less accurate.

## Fixes Applied

### Template Layout Fixes

Updated these templates:

```text
templates/broadcast-v2-anchor-studio.html
templates/broadcast-v2-top-stories.html
templates/broadcast-v2-mars-data.html
templates/broadcast-v2-timeline.html
templates/broadcast-v2-expert-split.html
templates/broadcast-v2-financial-board.html
templates/broadcast-v2-legal-board.html
templates/broadcast-v2-close.html
```

Changes:

- Raised main content bottom boundaries to leave a protected broadcast graphics zone.
- Anchor studio content now leaves space for both lower third and ticker.
- Anchor lower third is positioned above the ticker.

### Approval Page Fix

Updated:

```text
static/pilot-v2-approval.html
```

It now shows full 1280×720 scenes on larger screens instead of scaling them by default.

### Utility Script Added

Created:

```text
scripts/build_pilot_v2_approval.py
```

This regenerates the standalone approval page from the saved pilot draft and current templates.

## Current Status

The approval page should now show each scene with proper spacing between content, straps, lower thirds, and tickers.
