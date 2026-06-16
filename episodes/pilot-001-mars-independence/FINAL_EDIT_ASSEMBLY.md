# Final Edit Assembly Guide — 2147-001 Pilot

## Editing Software

Use any of:

- DaVinci Resolve
- Premiere Pro
- Final Cut
- CapCut Desktop
- Kdenlive

## Timeline Settings

```text
Resolution: 1920×1080
Frame rate: match recording, preferably 24 or 30 fps
Audio sample rate: 48 kHz
```

## Video Track Layout

```text
V1 — Rendered scene clips
V2 — Optional subtitles / overlays
V3 — Optional final correction cards
```

## Audio Track Layout

```text
A1 — Anchor voiceover
A2 — Music bed
A3 — Transition stings
A4 — UI/data SFX
A5 — Ambience/texture
A6 — Master limiter/export
```

## Assembly Order

1. Opening Transmission
2. Anchor Lead-In
3. Top Headlines
4. Mars Referendum Dashboard
5. Historical Context
6. Archive Context
7. Expert Quote
8. Market Ripple
9. Legal Ripple
10. Closing Transmission

## Voiceover Source

Use:

```text
episodes/pilot-001-mars-independence/audio/voiceover_timing_plan.json
```

## Sound Design Source

Use:

```text
episodes/pilot-001-mars-independence/audio/sound_design_plan.md
episodes/pilot-001-mars-independence/audio/audio_cue_sheet.md
```

## Subtitle Draft

Use:

```text
episodes/pilot-001-mars-independence/audio/subtitles_draft.srt
```

Adjust subtitle timing after final voiceover is recorded.

## Music/SFX Direction

- Keep music low under voice.
- Use restrained news stings.
- Avoid cheap sci-fi beeps.
- Data sounds should be subtle.
- No copyrighted news themes.

## Audio Master Target

```text
Integrated loudness: around -14 LUFS
True peak: below -1.0 dBTP
```

## Export Settings

Recommended YouTube export:

```text
Format: MP4
Codec: H.264
Resolution: 1920×1080
FPS: same as timeline
Bitrate: 12–20 Mbps
Audio: AAC, 48 kHz, 320 kbps
```

## Final QC

- [ ] all scenes are in correct order
- [ ] voiceover is clear
- [ ] music is not too loud
- [ ] SFX are subtle
- [ ] subtitles are synced
- [ ] no visual crops/overlaps
- [ ] disclaimer appears in YouTube description
- [ ] exported video plays in browser
