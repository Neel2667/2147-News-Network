# Report — Template-Specific Controls

Date: 2026-06-16

## What Was Built

Added template-specific controls to the custom 2147 News Network Studio app for the new premium templates.

## Why This Matters

The app should not only switch templates. It should expose the exact newsroom controls needed for each template type so scenes can be customized without editing code.

## Supported Template-Specific Controls

### Historical Timeline

Template:

```text
templates/historical-timeline.html
```

Controls added:

- Timeline year 1–4
- Timeline title 1–4
- Timeline description 1–4

Used for causal history segments such as:

```text
2136 oxygen-credit protests → 2142 tariff dispute → 2147 referendum
```

### Financial Desk

Template:

```text
templates/financial-desk.html
```

Controls added:

- Person name
- Person title
- Quote
- Metric 1 value/label
- Metric 2 value/label
- Metric 3 value/label
- Finance location

Used for market ripple segments such as Jiang Lau and Helion Grid Systems.

### Legal Desk

Template:

```text
templates/legal-desk.html
```

Controls added:

- Case title
- Case description
- Legal expert name
- Legal expert title
- Legal quote
- Four case metric value/label pairs
- Legal location

Used for tribunal, rights, court, and jurisdiction stories.

### Breaking News

Template:

```text
templates/breaking-news.html
```

Controls added:

- Status
- Time
- Impact level
- Verification desk/source

Used for urgent but premium breaking news packages.

## App Changes

The Scene Timeline panel now includes a **Template-Specific Controls** block. It changes automatically based on the selected scene template.

The selected scene stores template-specific values under:

```json
"template_controls": {}
```

These values are saved, loaded, previewed, and exported with the episode draft.

## Backend Changes

The template rendering context now supports defaults for all premium specialized controls.

Updated endpoint behavior:

```text
POST /api/scenes/preview
```

It now merges:

1. default template values
2. scene `template_controls`
3. live frontend controls

## Pilot Package Updated

Updated the pilot scene plan and saved draft with initial template-specific controls for:

- Historical Context
- Market Ripple
- Legal Ripple

Files updated:

```text
episodes/pilot-001-mars-independence/scene_plan.json
episodes/pilot-001-mars-independence/production_package.json
episodes/saved/2147-001-mars-independence.json
```

## Current Limitations

- Controls are form-based, not visual drag controls yet.
- Financial chart shape is still fixed; only labels/metrics are editable.
- Timeline supports four fixed events for now.

## Recommended Next Step

Build the remaining premium templates:

1. Science Desk
2. Earth Map / Climate Desk
3. Lunar Report

Then add a polished pilot loader button and deploy-ready Hugging Face Space instructions.
