# Report — Demo Video Generated

Date: 2026-06-16

## What Was Generated

Created a silent code-rendered demo video for the 2147 News Network pilot UI.

## Output Files

```text
outputs/demo-video/2147-demo-pilot-ui.mp4
outputs/demo-video/2147-demo-poster.png
outputs/demo-video/README.md
```

## Generator Script

```text
scripts/generate_demo_video.py
```

## Specs

```text
Resolution: 1280×720
FPS: 24
Duration: 42 seconds
Frames: 1008
Audio: none / silent
Approx size: 30 MB
```

## Visual Scenes

1. Opening Transmission
2. Anchor Lead-In
3. Top Headlines
4. Mars Referendum Dashboard
5. Historical Timeline
6. Expert Quote
7. Financial Desk
8. Legal Desk
9. Closing Transmission

## Policy Compliance

This is **not AI-generated video** and uses no AI-generated images.

Frames are generated with procedural code using:

- Python
- Pillow
- NumPy
- OpenCV

The video is a motion-graphics demo for UI direction only.

## Limitations

- Silent; no voiceover or music yet.
- 720p demo resolution to keep file size manageable.
- Separate from final browser-template render workflow.
- Intended for quick visual review, not final YouTube upload.


## Browser compatibility fix

The first MP4 was encoded as `mp4v`, which may not play in some browser previews. It has been replaced with a browser-compatible H.264 MP4:

```text
codec: h264 / avc1
pixel format: yuv420p
faststart: enabled
```
