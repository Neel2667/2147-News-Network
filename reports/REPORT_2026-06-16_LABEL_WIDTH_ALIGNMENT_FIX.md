# Report — Breaking / Headlines Label Alignment Fix

Date: 2026-06-16

## User Feedback

The user pointed out that the `BREAKING` label and `HEADLINES` label were not using the same horizontal area. The breaking label extended farther than the headlines label.

## Fix Applied

Updated:

```text
static/core-broadcast-elements.html
```

Changed ticker label width from:

```css
168px
```

to:

```css
184px
```

This matches the headline/breaking strap label width, so both red label blocks align vertically.
