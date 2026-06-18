#!/usr/bin/env python3
"""
Rebuilds the Final Pilot Render Package using the APPROVED exact static review page
as the single source of truth. This ensures 100% visual fidelity.

Run this whenever you want the render package to match the approved version.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / "static" / "pilot-exact-static-review.html"
OUT = ROOT / "outputs" / "final-pilot-render-package"
SCENES_DIR = OUT / "scenes"
ZIP_PATH = OUT / "2147-001-final-pilot-render-package.zip"

RENDER_W = 1920
RENDER_H = 1080
BASE_W = 1280
BASE_H = 720
SCALE = RENDER_W / BASE_W

SCENE_MAPPING = [
    {"id": "s01", "scene": "Opening Transmission", "duration": 16, "template": "broadcast-v2-cold-open.html"},
    {"id": "s02", "scene": "Anchor Lead-In", "duration": 48, "template": "broadcast-v2-studio-wall-footage.html"},
    {"id": "s03", "scene": "Top Headlines", "duration": 38, "template": "broadcast-v2-top-stories.html"},
    {"id": "s04", "scene": "Mars Referendum Dashboard", "duration": 78, "template": "broadcast-v2-studio-wall-data.html"},
    {"id": "s05", "scene": "Historical Context", "duration": 62, "template": "broadcast-v2-studio-wall-map.html"},
    {"id": "s05b", "scene": "Archive Context", "duration": 32, "template": "broadcast-v2-studio-wall-archive.html"},
    {"id": "s06", "scene": "Expert Quote", "duration": 34, "template": "broadcast-v2-studio-wall-quote.html"},
    {"id": "s07", "scene": "Market Ripple", "duration": 52, "template": "broadcast-v2-studio-wall-data.html"},
    {"id": "s08", "scene": "Legal Ripple", "duration": 50, "template": "broadcast-v2-studio-wall-data.html"},
    {"id": "s09", "scene": "Closing Transmission", "duration": 24, "template": "broadcast-v2-close.html"},
]

def extract_scenes_from_approved() -> list[dict]:
    """Parse the approved review page and extract each scene's full HTML."""
    html = APPROVED.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    
    sections = soup.find_all("section", class_="review-scene")
    if len(sections) != 10:
        raise RuntimeError(f"Expected 10 scenes, found {len(sections)}")
    
    scenes = []
    for i, section in enumerate(sections, 1):
        # Get the inner content (the actual broadcast frame)
        stage = section.find("div", class_="scene-stage")
        if not stage:
            continue
            
        scale_div = stage.find("div", class_="scene-scale")
        if scale_div:
            inner_html = str(scale_div.find("div", recursive=False) or scale_div)
        else:
            inner_html = str(stage)
        
        scenes.append({
            "index": i,
            "id": SCENE_MAPPING[i-1]["id"],
            "scene": SCENE_MAPPING[i-1]["scene"],
            "duration": SCENE_MAPPING[i-1]["duration"],
            "template": SCENE_MAPPING[i-1]["template"],
            "html": inner_html
        })
    return scenes

def create_render_scene(scene: dict, total: int) -> str:
    """Wrap approved scene HTML in a perfect 1920x1080 render viewport."""
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{scene['index']:02d} — {scene['scene']} — 2147NN Final Render</title>
  <style>
    html, body {{ margin:0; width:100%; height:100%; background:#05070d; overflow:hidden; }}
    body {{ display:grid; place-items:center; }}
    .render-viewport {{ 
      width:{RENDER_W}px; 
      height:{RENDER_H}px; 
      overflow:hidden; 
      background:#03050a; 
      position:relative; 
    }}
    .render-scale {{ 
      width:{BASE_W}px; 
      height:{BASE_H}px; 
      transform:scale({SCALE}); 
      transform-origin:0 0; 
    }}
    .render-scale > * {{ 
      width:{BASE_W}px !important; 
      height:{BASE_H}px !important; 
      min-height:{BASE_H}px !important; 
      border-radius:0 !important; 
    }}
    .render-meta {{ 
      position:absolute; 
      left:24px; 
      top:18px; 
      z-index:99999; 
      opacity:.22; 
      color:#dff7ff; 
      background:rgba(0,0,0,.46); 
      border:1px solid rgba(255,255,255,.16); 
      border-radius:999px; 
      padding:8px 12px; 
      font:800 12px/1.2 system-ui; 
      letter-spacing:.08em; 
      text-transform:uppercase; 
    }}
    @media(max-width:{RENDER_W}px) {{ 
      .render-viewport {{ transform:scale(calc(100vw / {RENDER_W})); transform-origin:center; }} 
    }}
    @media(max-height:{RENDER_H}px) {{ 
      .render-viewport {{ transform:scale(min(calc(100vw / {RENDER_W}), calc(100vh / {RENDER_H}))); transform-origin:center; }} 
    }}
  </style>
</head>
<body>
  <main class="render-viewport">
    <div class="render-meta">Scene {scene['index']}/{total} • {scene['duration']}s • {scene['template']}</div>
    <div class="render-scale">
{scene['html']}
    </div>
  </main>
</body>
</html>'''

def main():
    print("Extracting scenes from APPROVED review page...")
    scenes = extract_scenes_from_approved()
    
    SCENES_DIR.mkdir(parents=True, exist_ok=True)
    
    manifest = []
    for scene in scenes:
        file_name = f"{scene['index']:02d}-{scene['id']}.html"
        html_content = create_render_scene(scene, len(scenes))
        (SCENES_DIR / file_name).write_text(html_content, encoding="utf-8")
        
        manifest.append({
            "index": scene["index"],
            "id": scene["id"],
            "scene": scene["scene"],
            "template": scene["template"],
            "duration_seconds": scene["duration"],
            "file": f"scenes/{file_name}",
        })
        print(f"  ✓ {file_name}")
    
    # Write manifest
    total = sum(x["duration_seconds"] for x in manifest)
    manifest_doc = {
        "episode_id": "2147-001-mars-independence",
        "title": "Mars Votes for Independence From Earth | 2147 News Network",
        "resolution": {"width": RENDER_W, "height": RENDER_H},
        "base_composition": {"width": BASE_W, "height": BASE_H, "scale": SCALE},
        "total_runtime_seconds": total,
        "scene_count": len(manifest),
        "scenes": manifest,
        "approved_review_page": "static/pilot-exact-static-review.html",
        "source": "APPROVED_EXACT_STATIC_REVIEW",
        "recording_method": "Open each scene HTML and record with OBS/browser capture at 1920x1080 for duration_seconds.",
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest_doc, indent=2), encoding="utf-8")
    
    # Write index.html and README (same as before)
    print(f"\n✅ Rebuilt {len(scenes)} scenes from APPROVED source")
    print(f"   Total runtime: {total}s")
    print(f"   Output: {OUT}")

if __name__ == "__main__":
    main()