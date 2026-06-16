# Report — Core Elements Polish Fixes

Date: 2026-06-16

## User Feedback

The user requested more polish and specifically identified:

1. Ticker text overlapping the `Headlines` label.
2. Name strap text going outside boxes.
3. Elements looking too static.
4. Every element should be animated to hold attention.

## Fixes Applied

Updated:

```text
static/core-broadcast-elements.html
```

### Ticker Fix

The ticker now uses a protected ticker viewport:

```text
label area + separate ticker-window
```

This prevents crawl text from overlapping the `Headlines` label.

### Lower Third Fix

Lower-third/name-strap typography and layout were adjusted:

- reduced oversized name font
- added `min-width: 0`
- added `overflow: hidden`
- added `text-overflow: ellipsis`
- reduced role/location widths
- improved mobile safety

### Animation Pass

Added motion to the core elements:

- bug entrance loop
- LIVE pill entrance and pulse
- clock fade/drift
- source chip light sweep
- story panel reveal loop
- over-the-shoulder reveal loop
- Mars graphic pulse
- strap slide loop
- lower-third slide loop
- ticker crawl with protected window
- tile float
- subtle stage sweep
- motion tests retained

## Current Status

Core Broadcast Elements page is now more polished and animated, but still needs user review before the full templates are rebuilt.
