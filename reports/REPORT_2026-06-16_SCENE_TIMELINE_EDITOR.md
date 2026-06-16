# Report — Scene Timeline Editor and Template Control Panel

Date: 2026-06-16

## What Was Built

Added a custom **Scene Timeline Editor** and **Template Control Panel** to the 2147 News Network Studio custom app.

This continues the move away from Gradio and toward a fully controlled premium newsroom application.

## Updated App Sections

A new sidebar section was added:

```text
Scene Timeline
```

The app now has:

1. World Dashboard
2. Event Analyzer
3. Episode Builder
4. Scene Timeline
5. Visual Preview
6. Export Center

## Scene Timeline Editor Features

The timeline now supports:

- viewing all scenes from the generated episode draft
- selecting a scene
- seeing scene number, template, purpose, and duration
- calculating total runtime
- adding a new scene
- duplicating the selected scene
- deleting the selected scene
- moving scenes up/down
- syncing timeline changes back to the scene-plan JSON

## Template Control Panel Features

For the selected scene, the user can edit:

- scene name
- duration in seconds
- template file
- headline
- summary/purpose
- lower-third name
- lower-third title
- ticker text
- source label

The selected scene can then be previewed immediately in the custom app.

## Backend Additions

Added a new request model and endpoint:

```text
POST /api/scenes/preview
```

This renders a selected scene using its template and current controls.

## Template Parameter Improvements

Updated templates to accept more dynamic fields:

- `anchor-desk.html` now supports `$lower_name` and `$lower_title`
- `headline-cards.html` now supports `$source`
- `mars-dashboard.html` now supports `$source`

## Files Modified

```text
main.py
static/index.html
static/styles.css
static/app.js
templates/anchor-desk.html
templates/headline-cards.html
templates/mars-dashboard.html
```

## Current Limitations

- Timeline edits are in-browser only until exported.
- There is not yet a persistent saved episode database.
- No drag-and-drop yet; movement is done with Up/Down buttons.
- Template controls are basic text controls for now.
- No video render/export yet.

## Recommended Next Step

Build episode save/load support:

```text
1. Save current episode draft as JSON
2. Load saved episode drafts
3. Create first pilot episode production package
4. Add more template-specific controls
5. Add drag-and-drop timeline later
```
