# Report — Pilot V2 Approval Page Standalone Fix

Date: 2026-06-16

## Issue

The Pilot V2 Approval page failed with:

```text
Failed to execute 'fetch' on 'Window': Failed to parse URL from /api/episodes/2147-001-mars-independence
```

This happened because the page relied on runtime API fetches, which may not work in static previews or sandboxed environments.

## Fix

Rebuilt:

```text
static/pilot-v2-approval.html
```

as a standalone static approval board.

## What Changed

- No API fetch required.
- Inlined `broadcast-system.css`.
- Rendered all 9 pilot scenes directly into the page.
- Uses the saved pilot scene data from:

```text
episodes/saved/2147-001-mars-independence.json
```

## Result

The approval page should now open directly and show all 9 scenes without needing the FastAPI backend.
