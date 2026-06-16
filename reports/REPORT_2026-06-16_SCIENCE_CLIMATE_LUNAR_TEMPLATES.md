# Report — Science, Climate, and Lunar Premium Templates

Date: 2026-06-16

## What Was Built

Added three new premium newsroom templates for later Season 1 stories:

```text
templates/science-desk.html
templates/earth-climate-map.html
templates/lunar-report.html
```

These expand the visual language beyond the Mars pilot and prepare the app for Europa science, Earth climate, and Luna labor/economy episodes.

## Template 1 — Science Desk

File:

```text
templates/science-desk.html
```

Purpose:

Premium science segment for deep-space missions, probe data, signal verification, and research disputes.

Best for:

- Europa probe signal episodes
- Titan atmospheric research
- asteroid geology reports
- solar storm science explainers

Template-specific controls added:

- Mission / consortium
- Signal status
- Instrument
- Depth
- Review stage
- Confirmed repeat count
- Science location

## Template 2 — Earth Climate Map

File:

```text
templates/earth-climate-map.html
```

Purpose:

Earth climate and adaptation reports with a premium map/globe visual.

Best for:

- Pacific floating cities storm shields
- superstorm alerts
- sea-wall expansion
- fusion-grid climate stress
- migration/weather bureau stories

Template-specific controls added:

- Climate region
- Four climate metric value/label pairs

## Template 3 — Lunar Report

File:

```text
templates/lunar-report.html
```

Purpose:

Lunar economy, mining, oxygen-credit, helium-3, labor, and habitat reports.

Best for:

- Lunar oxygen strike
- helium-3 supply delays
- mining safety incidents
- Lunar Resource Authority decisions

Template-specific controls added:

- Lunar region
- Lunar location
- Person name
- Person title
- Four lunar metric value/label pairs

## App Updates

The Scene Timeline template-specific control system now supports:

```text
science-desk.html
earth-climate-map.html
lunar-report.html
```

The backend template context now includes safe default values for all three templates.

## Season Coverage Improved

The project now has premium template coverage for:

- Mars politics
- historical context
- finance/markets
- legal/tribunal stories
- breaking news
- science missions
- Earth climate adaptation
- lunar labor/economy

## Recommended Next Step

Add a one-click pilot loader / launch workflow, then prepare Hugging Face Docker deployment instructions and a polished README section for running the custom app.
