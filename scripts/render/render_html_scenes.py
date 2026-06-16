"""Automated HTML scene renderer using Playwright + FFmpeg.

This is optional. Manual OBS recording is recommended for the first pilot.

What it does:
1. Opens each final render scene HTML page in Chromium.
2. Captures PNG frames at a chosen FPS for each scene duration.
3. Uses FFmpeg to encode each scene to MP4.
4. Concatenates scene MP4s into one silent preview/final video.

Install:
    pip install -r requirements-render.txt
    python -m playwright install chromium

Run:
    python scripts/render/render_html_scenes.py
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "outputs" / "final-pilot-render-package"
MANIFEST = PACKAGE / "manifest.json"
OUT_DIR = ROOT / "outputs" / "auto-render"
FRAMES_DIR = OUT_DIR / "frames"
SCENE_VIDEO_DIR = OUT_DIR / "scene-videos"
FINAL_VIDEO = OUT_DIR / "2147-001-auto-render-silent.mp4"
FPS = 24
WIDTH = 1920
HEIGHT = 1080


def ffmpeg() -> str:
    return imageio_ffmpeg.get_ffmpeg_exe()


def ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    SCENE_VIDEO_DIR.mkdir(parents=True, exist_ok=True)


def capture_scene(page, scene: dict) -> Path:
    idx = scene["index"]
    duration = int(scene["duration_seconds"])
    scene_file = (PACKAGE / scene["file"]).resolve()
    scene_frames = FRAMES_DIR / f"scene-{idx:02d}"
    scene_frames.mkdir(parents=True, exist_ok=True)

    page.goto(scene_file.as_uri(), wait_until="networkidle")
    page.set_viewport_size({"width": WIDTH, "height": HEIGHT})
    page.wait_for_timeout(500)

    total_frames = duration * FPS
    for frame in range(total_frames):
        path = scene_frames / f"frame-{frame:05d}.png"
        page.screenshot(path=str(path), full_page=False)
        # Advance wall-clock time; CSS/video animations are time based.
        page.wait_for_timeout(int(1000 / FPS))
        if frame % (FPS * 5) == 0:
            print(f"scene {idx:02d}: frame {frame}/{total_frames}")

    out_video = SCENE_VIDEO_DIR / f"scene-{idx:02d}.mp4"
    cmd = [
        ffmpeg(), "-y",
        "-framerate", str(FPS),
        "-i", str(scene_frames / "frame-%05d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-r", str(FPS),
        str(out_video),
    ]
    subprocess.check_call(cmd)
    return out_video


def concat_videos(videos: list[Path]) -> None:
    concat_file = OUT_DIR / "concat.txt"
    concat_file.write_text("\n".join(f"file '{v.resolve()}'" for v in videos), encoding="utf-8")
    cmd = [
        ffmpeg(), "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(FINAL_VIDEO),
    ]
    subprocess.check_call(cmd)


def main() -> None:
    ensure_dirs()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    videos: list[Path] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=1)
        for scene in manifest["scenes"]:
            videos.append(capture_scene(page, scene))
        browser.close()
    concat_videos(videos)
    print("Final silent render:", FINAL_VIDEO)


if __name__ == "__main__":
    main()
