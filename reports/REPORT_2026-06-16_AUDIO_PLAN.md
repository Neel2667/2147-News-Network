# Report — Pilot Sound Design and Voiceover Timing Plan

Date: 2026-06-16

## What Was Built

Added a complete sound design and voiceover timing plan for the pilot episode.

## New Audio Files

```text
episodes/pilot-001-mars-independence/audio/sound_design_plan.md
episodes/pilot-001-mars-independence/audio/voiceover_timing_plan.json
episodes/pilot-001-mars-independence/audio/audio_cue_sheet.md
episodes/pilot-001-mars-independence/audio/subtitles_draft.srt
```

## Sound Direction

The pilot audio direction is:

```text
premium international news + Apple-keynote polish + restrained futuristic newsroom
```

Avoid:

- cheap sci-fi sounds
- aggressive glitch effects
- robotic free TTS feel
- loud whooshes
- cluttered beeps

## Voiceover Plan

Anchor voice:

```text
Anaya Rao
calm, precise, international-news tone
135–150 words per minute
```

Data sections should be slower:

```text
120–135 words per minute
```

## Audio Deliverables Added

### Sound Design Plan

Defines:

- audio philosophy
- voice direction
- music bed rules
- SFX palette
- scene-by-scene sound treatment
- licensing rules
- audio QC checklist

### Voiceover Timing Plan

Structured JSON with:

- scene ID
- scene duration
- voiceover start/end
- estimated words
- voiceover draft
- audio notes

### Audio Cue Sheet

Approximate cue timing for:

- network sting
- lower-third pulse
- headline taps
- data ticks
- timeline ticks
- finance pulse
- legal document reveal
- closing shimmer

### Subtitles Draft

Initial `.srt` subtitle draft for the pilot.

## Package Updates

Updated:

```text
episodes/pilot-001-mars-independence/production_package.json
episodes/saved/2147-001-mars-independence.json
```

The pilot package now references the audio plan files.

## Next Recommended Step

Add a thumbnail and channel launch package:

- pilot thumbnail concept
- channel About text
- description template
- pinned comment disclaimer
- first upload checklist
