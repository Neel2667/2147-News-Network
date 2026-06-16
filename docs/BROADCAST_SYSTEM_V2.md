# Broadcast System V2 — Reusable Core Components

Last updated: 2026-06-16

## Purpose

The approved core broadcast identity elements have been extracted into reusable frontend files so all future templates use the same professional visual language.

## Files

```text
static/broadcast-system.css
static/broadcast-components.js
static/broadcast-system-showcase.html
```

## Review URLs

Core design review page:

```text
/static/core-broadcast-elements.html
```

Reusable component showcase:

```text
/static/broadcast-system-showcase.html
```

## Component CSS Classes

### Frame and layout

```text
.bcast-frame
.bcast-safe
.bcast-top-left
.bcast-top-right
```

### Identity and metadata

```text
.bcast-bug
.bcast-live
.bcast-clock
.bcast-source
```

### Broadcast graphics

```text
.bcast-strap
.bcast-ticker
.bcast-lower-third
.bcast-story-panel
.bcast-ots
```

## JavaScript Helpers

The global helper is:

```js
window.Broadcast2147
```

Available helpers:

```js
Broadcast2147.bug()
Broadcast2147.live()
Broadcast2147.clock()
Broadcast2147.source()
Broadcast2147.strap()
Broadcast2147.ticker()
Broadcast2147.lowerThird()
Broadcast2147.storyPanel()
Broadcast2147.marsOts()
```

## Design Rules

- Use these components for all V2 templates.
- Do not redesign lower thirds, tickers, or bug independently per template.
- Long names must wrap, not truncate.
- The ticker must use a protected ticker window and must not overlap the label.
- Breaking and Headlines label widths must align.
- Motion should vary by element type.
- Apple-inspired polish is allowed: soft material depth, rounded surfaces, restrained color, smooth purposeful motion.

## Next Step

Rebuild the first full templates using this system:

```text
broadcast-v2-cold-open.html
broadcast-v2-anchor-studio.html
broadcast-v2-top-stories.html
broadcast-v2-mars-data.html
broadcast-v2-timeline.html
```
