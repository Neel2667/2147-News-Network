# Report — Episode Save/Load and Pilot Package

Date: 2026-06-16

## What Was Built

Added episode save/load support to the custom 2147 News Network Studio app and created the first pilot episode production package.

## New App Features

The Export Center is now a **Save, Load & Export Center**.

It supports:

- saving the current edited episode draft
- selecting saved episode drafts
- loading saved drafts into the app
- refreshing the saved draft list
- exporting current draft files

## Backend Endpoints Added

```text
GET  /api/episodes
GET  /api/episodes/{episode_id}
POST /api/episodes/save
```

Saved drafts are written to:

```text
episodes/saved/
```

## Pilot Episode Package Created

Created first pilot package:

```text
episodes/pilot-001-mars-independence/
```

Files:

```text
README.md
script.md
scene_plan.json
metadata.json
production_notes.md
production_package.json
```

Also created a saved app draft:

```text
episodes/saved/2147-001-mars-independence.json
```

This lets the custom app load the pilot episode draft.

## Season Plan Added

Created:

```text
data/season_001_plan.json
```

This defines the first 10-episode connected season, **The Mars Sovereignty Crisis**.

## First Pilot Episode

Title:

```text
Mars Votes for Independence From Earth | 2147 News Network
```

Main event:

```text
event_2147_001_mars_referendum_final_cycle
```

Pilot scene package includes:

1. Opening Transmission
2. Anchor Lead-In
3. Top Headlines
4. Mars Referendum Dashboard
5. Historical Context
6. Expert Quote
7. Market Ripple
8. Legal Ripple
9. Closing Transmission

## Current Limitations

- Save/load writes JSON files locally inside the repo workspace.
- No user authentication yet.
- No visual drag-and-drop timeline yet; timeline movement is via Up/Down buttons.
- No video rendering yet.

## Recommended Next Step

Build template-specific controls and more premium templates:

1. Breaking News template
2. Financial Desk template
3. Legal Desk template
4. Timeline/History template
5. Episode package loader shortcut for pilot episode
