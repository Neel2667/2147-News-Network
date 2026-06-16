# Report — First Broadcast V2 Templates

Date: 2026-06-16

## What Was Built

Created the first full templates using the reusable Broadcast System V2 components.

## New Templates

```text
templates/broadcast-v2-cold-open.html
templates/broadcast-v2-anchor-studio.html
templates/broadcast-v2-top-stories.html
templates/broadcast-v2-mars-data.html
templates/broadcast-v2-timeline.html
```

## System Used

All templates use:

```text
static/broadcast-system.css
```

They reuse the approved V2 broadcast language:

- logo bug
- LIVE pill
- clock
- source chip
- headline/breaking strap
- ticker
- long-name safe lower third
- broadcast-safe frame
- Apple-inspired material polish
- varied motion

## Pilot Updated

Updated the first five pilot scenes to use the new V2 templates:

| Scene | New Template |
|---|---|
| s01 Opening Transmission | broadcast-v2-cold-open.html |
| s02 Anchor Lead-In | broadcast-v2-anchor-studio.html |
| s03 Top Headlines | broadcast-v2-top-stories.html |
| s04 Mars Referendum Dashboard | broadcast-v2-mars-data.html |
| s05 Historical Context | broadcast-v2-timeline.html |

Updated:

```text
episodes/pilot-001-mars-independence/scene_plan.json
episodes/pilot-001-mars-independence/production_package.json
episodes/saved/2147-001-mars-independence.json
```

## Next Recommended Templates

Rebuild remaining pilot scenes:

```text
broadcast-v2-expert-split.html
broadcast-v2-financial-board.html
broadcast-v2-legal-board.html
broadcast-v2-close.html
```
