# Premium UI Design System — 2147 News Network

Last updated: 2026-06-15

## Purpose

The most important audience-facing quality factor for 2147 News Network is the UI. Even if the writing and worldbuilding are strong, viewers will leave if the visual design looks cheap.

The channel must feel like a premium international broadcast designed with the restraint, polish, spacing, typography, and motion quality associated with high-end product launches and premium operating systems.

## Design Direction

Use inspiration from premium Apple-style design principles:

- minimal but rich
- elegant spacing
- soft depth
- glass-like translucent panels
- beautiful typography
- cinematic lighting
- fluid motion
- polished transitions
- restrained color
- high clarity
- no visual clutter

Important: this means **inspired by premium design principles**, not copying Apple's branding, layouts, icons, product UI, or trademarks.

## Core Visual Philosophy

The interface should look like:

```text
Apple keynote polish + international news clarity + futuristic orbital newsroom
```

Not like:

```text
cheap cyberpunk dashboard + random neon + noisy sci-fi HUD
```

## Premium UI Rules

### 1. Less, But Better

Do not fill every area with effects. Premium design uses empty space confidently.

Bad:
- too many panels
- too many blinking lines
- random code rain
- excessive grid overlays
- crowded labels

Good:
- one clear focus
- clean hierarchy
- soft panels
- precise typography
- calm motion

### 2. Typography Is the UI

Use typography as the main design element.

Recommended fonts:
- Inter
- SF-like system font stack
- IBM Plex Sans
- Source Sans 3
- Roboto Condensed only for tickers/data labels

Font hierarchy:

```text
Hero headline: 64–96px, bold, tight tracking
Section headline: 34–48px, semibold
Body/news text: 20–28px, regular/medium
Metadata labels: 12–16px, uppercase, letter-spaced
Ticker: 14–18px, medium/semibold
```

Avoid:
- novelty sci-fi fonts
- fake hacker fonts
- outlined text everywhere
- too many font families

### 3. Use Premium Color Restraint

Main palette:

```text
Broadcast Black: #03040A
Deep Navy: #050914
Graphite: #111827
Glass White: rgba(255,255,255,0.08)
Text White: #F8FAFC
Muted Text: #94A3B8
Premium Cyan: #00D9FF
Electric Blue: #2F80FF
Mars Accent: #FF6A2A
Market Amber: #FFB020
Breaking Red: #FF3B3B
Data Green: #25FF9C
```

Use cyan/blue as accents, not as full-screen overload.

### 4. Glass Panels Should Feel Expensive

Panel style:

```text
background: rgba(255,255,255,0.07)
border: 1px solid rgba(255,255,255,0.12)
backdrop blur: 18–32px
border radius: 24–36px
shadow: soft, large, low opacity
```

Avoid harsh borders and cheap neon outlines.

### 5. Motion Should Feel Like Apple

Motion principles:
- smooth easing
- gentle scale
- soft fades
- clean parallax
- natural acceleration/deceleration
- no random shaking unless breaking news

Recommended easing:

```css
cubic-bezier(0.22, 1, 0.36, 1)
```

Animation durations:

```text
micro interaction: 180–300ms
panel reveal: 600–900ms
scene transition: 900–1400ms
hero intro: 2–4s
```

Avoid:
- constant flashing
- cheap glitch spam
- fast chaotic movement
- overuse of scanning lines

### 6. Cinematic Depth

Use layers:

1. soft animated background
2. blurred orbital/map layer
3. glass panel layer
4. text/data layer
5. ticker/lower-third layer

Depth should be subtle and premium, not noisy.

### 7. Data Must Look Editorial, Not Spreadsheet-Like

Charts should feel like Bloomberg/Apple-quality infographics.

Use:
- rounded bars
- smooth line charts
- large numeric callouts
- subtle gridlines
- source label
- timestamp
- clear data hierarchy

Avoid:
- default chart styling
- harsh colors
- tiny unreadable numbers

## Scene Design Standards

### Opening Intro

Should feel like a premium global broadcast opening.

Elements:
- dark orbital background
- slow Earth/Mars/Luna alignment
- glass logo reveal
- soft cyan light sweep
- calm but powerful music sting

Do not overdo glitch effects.

### Anchor Desk

Should feel like a premium virtual studio.

Elements:
- large clean background screen
- subtle orbital map
- clean lower-third
- ticker at bottom
- soft studio lighting
- calm motion background

No cheap avatar required. A silhouette/hologram presenter can be used if designed elegantly.

### Headline Cards

Cards should appear like Apple event slides mixed with broadcast news.

Elements:
- huge headline text
- small category label
- source line
- location/date
- minimal icon/map marker
- smooth card transitions

### Breaking News

Breaking news can be stronger but still premium.

Use:
- red accent
- clean alert panel
- controlled pulse
- strong headline

Avoid:
- siren chaos
- excessive flashing
- messy red overlays

### Mars Dashboard

Mars visuals should be elegant.

Use:
- clean Mars sphere or map made in SVG/Canvas
- soft orange atmosphere glow
- colony markers
- turnout bars
- source label
- not too much sci-fi clutter

### Quote Card

Should feel like a serious news quote card.

Elements:
- person's full name
- title
- organization
- location
- quote
- waveform or small archive-feed label

## UI Quality Checklist

Before any template is accepted:

- Does it look premium within 3 seconds?
- Is the typography beautiful?
- Is spacing generous?
- Are colors restrained?
- Is the animation smooth and not cheap?
- Does every element have purpose?
- Is there a clear focal point?
- Would this look acceptable in an Apple-style keynote or international news broadcast?
- Does it avoid generic cyberpunk clutter?

If any answer is no, redesign.

## What To Avoid Completely

- default Bootstrap-looking UI
- generic sci-fi dashboard kits
- too much neon glow
- random matrix/code rain
- low-quality icons
- cartoonish graphics
- hard shadows
- harsh gradients
- inconsistent spacing
- cheap glitch effects
- too many moving things at once
- unreadable text

## Design System Components To Build

The project should include reusable premium components:

1. glass panel
2. hero headline
3. lower-third
4. ticker
5. timestamp chip
6. source label
7. map marker
8. quote card
9. data card
10. headline card
11. breaking alert
12. chart module
13. orbital background
14. premium transition wrapper

## Implementation Notes

For in-browser preview and Hugging Face compatibility:

- use inline CSS where practical
- avoid external CDN dependencies for preview-critical UI
- use SVG/CSS/Canvas for visuals
- use system font stack if external fonts are unavailable
- keep animations performant
- prefer transform/opacity animations
- avoid heavy DOM counts

## Final Design Standard

The UI is not decoration. The UI is the product.

The viewer should feel:

```text
This is not a cheap fictional YouTube video.
This looks like a serious broadcast system from the future.
```
