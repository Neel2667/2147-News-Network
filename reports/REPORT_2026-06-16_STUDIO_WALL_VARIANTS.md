# Report — Studio Wall Variant Templates

Date: 2026-06-16

## What Was Built

Created Studio + Video Wall variant templates based on the approved Studio Wall direction.

## New Templates

```text
templates/broadcast-v2-studio-wall-footage.html
templates/broadcast-v2-studio-wall-map.html
templates/broadcast-v2-studio-wall-data.html
templates/broadcast-v2-studio-wall-quote.html
templates/broadcast-v2-studio-wall-archive.html
```

## Variants

### Footage

Uses the approved anchor + video wall composition with footage/poster support.

### Map

Anchor on left, map/route wall on right.

### Data

Anchor on left, data board / metrics wall on right.

### Quote

Anchor on left, expert quote wall on right.

### Archive

Anchor on left, archive footage wall on right with archive-oriented labels.

## Backend Defaults

Added default archive fields to template context:

```text
archive_label
archive_year
archive_metric_label
```

## Next Step

Create a Studio Wall Variants approval page so the user can review all five variants together.
