# Report — Long Name Strap Fix

Date: 2026-06-16

## User Feedback

The user reported that if a name is long, the name strap truncates it, which will not work for a real news channel.

## Fixes Applied

Updated:

```text
static/core-broadcast-elements.html
```

## Name Strap Changes

- Replaced the 3-column sample grid with a full-width stacked lower-third review section.
- Increased lower-third height.
- Increased available name area.
- Removed name truncation / ellipsis behavior.
- Allowed names to wrap naturally.
- Added `overflow-wrap:anywhere` for very long names.
- Kept role and location columns readable.
- Added a long-name example:

```text
Dr. Alexandria Sen-Moreau
```

- Added a long breaking headline example:

```text
Mars Referendum Final Certification Window
```

## Current Status

Lower thirds should now support longer names and headlines without truncating critical information.
