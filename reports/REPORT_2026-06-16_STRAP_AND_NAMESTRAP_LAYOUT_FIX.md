# Report — Strap and Name Strap Layout Fix

Date: 2026-06-16

## User Feedback

The user reported:

1. Small text in headline/breaking straps was going outside the box.
2. Anchor name in name straps was gone / there was not enough space.

## Fixes Applied

Updated:

```text
static/core-broadcast-elements.html
```

### Headline / Breaking Strap Fixes

- Increased strap height slightly.
- Reduced label and tag widths.
- Reduced main headline font size slightly.
- Added `min-width: 0` to main content.
- Added `overflow: hidden` and `text-overflow: ellipsis`.
- Forced small text to stay on one line inside the box.
- Reduced small text size.

### Name Strap Fixes

- Reduced role column width.
- Reduced location column width.
- Increased available center name area.
- Reduced name and subtitle font sizes.
- Added text overflow handling.
- Extended animation hold time so the name remains visible longer.

## Current Status

The strap text and name straps should now stay inside their boxes and remain readable.
