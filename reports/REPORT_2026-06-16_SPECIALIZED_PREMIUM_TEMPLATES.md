# Report — Specialized Premium Templates

Date: 2026-06-16

## What Was Built

Added four specialized premium broadcast templates for 2147 News Network Studio:

```text
templates/historical-timeline.html
templates/financial-desk.html
templates/legal-desk.html
templates/breaking-news.html
```

These replace generic placeholder scenes and make the pilot episode feel more like an international-level news broadcast.

## Template 1 — Historical Timeline

File:

```text
templates/historical-timeline.html
```

Purpose:

Show cause-and-effect context behind an event.

Best use:

- Mars referendum background
- oxygen-credit protests
- Earth-Mars tariff disputes
- long-running legal/political conflicts

Pilot usage:

```text
Scene s05 — Historical Context
```

## Template 2 — Financial Desk

File:

```text
templates/financial-desk.html
```

Purpose:

Show market ripple effects with premium finance-news visuals.

Includes:

- named CEO quote section
- market metrics
- animated chart
- source label
- financial ticker

Pilot usage:

```text
Scene s07 — Market Ripple
```

## Template 3 — Legal Desk

File:

```text
templates/legal-desk.html
```

Purpose:

Show tribunal, court, rights, and legal-process stories.

Includes:

- tribunal filing panel
- jurisdiction/case metrics
- named legal expert quote
- source label
- legal ticker

Pilot usage:

```text
Scene s08 — Legal Ripple
```

## Template 4 — Breaking News

File:

```text
templates/breaking-news.html
```

Purpose:

Premium urgent alert package without cheap siren/glitch clutter.

Best use:

- emergency sovereignty hearing
- orbital transit incident
- superstorm alert
- confirmed referendum result
- Europa signal confirmation

## Pilot Package Updated

Updated:

```text
episodes/pilot-001-mars-independence/scene_plan.json
episodes/pilot-001-mars-independence/production_package.json
episodes/pilot-001-mars-independence/production_notes.md
episodes/saved/2147-001-mars-independence.json
```

The saved pilot draft now loads with the specialized templates.

## Current Visual Coverage for Pilot

The pilot now uses:

1. `opening-intro-premium.html`
2. `anchor-desk.html`
3. `headline-cards.html`
4. `mars-dashboard.html`
5. `historical-timeline.html`
6. `quote-card.html`
7. `financial-desk.html`
8. `legal-desk.html`
9. `closing-transmission.html`

## Recommended Next Step

Add more template-specific controls to the app, especially for:

- timeline event years/text
- financial metrics
- legal case metrics
- breaking news status fields
- quote person/name/title customization
