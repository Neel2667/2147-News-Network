# Report — Ticker Visibility and Animation Variation Fix

Date: 2026-06-16

## User Feedback

The user reported:

1. Ticker text disappeared.
2. Animations felt too similar.
3. Motion needs variation across elements.

## Fixes Applied

Updated:

```text
static/core-broadcast-elements.html
```

## Ticker Fix

The ticker no longer starts off-screen with excessive padding. It now uses:

- fixed `Headlines` label
- separate `.ticker-window`
- duplicated ticker text spans
- immediate visible crawl text
- protected overflow area so text cannot overlap the label

## Animation Variation

Replaced similar reveal loops with varied broadcast-style motion:

- bug: horizontal settle + shine sweep
- LIVE pill: pulse/brightness animation
- clock: subtle broadcast blink
- source chips: light sweep
- story panel: slide from left
- over-the-shoulder panel: zoom reveal
- normal strap: clip-path wipe
- breaking strap: horizontal urgent slide
- Mars graphic: pulse
- data bars: grow/pulse
- lower third 1: slide from left
- lower third 2: slide from bottom
- lower third 3: breaking pop/brightness
- tiles: subtle float
- ticker: continuous crawl

## Current Status

The core elements page should now have visible ticker text and more varied animation language.
