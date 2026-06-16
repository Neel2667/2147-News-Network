"""Custom 2147 News Network Studio app.

This replaces the Gradio-first approach with a fully custom FastAPI web app so
we can control the UI, controls, layout, and future production workflow.
"""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.template_renderer import available_templates, render_template

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
STATIC_DIR = ROOT / "static"
EXPORT_DIR = ROOT / "exports"
SAVED_EPISODES_DIR = ROOT / "episodes" / "saved"
RENDER_DIR = ROOT / "render_packages"
RENDER_DIR.mkdir(exist_ok=True)

app = FastAPI(title="2147 News Network Studio", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
EXPORT_DIR.mkdir(exist_ok=True)
app.mount("/exports", StaticFiles(directory=EXPORT_DIR), name="exports")
app.mount("/renders", StaticFiles(directory=RENDER_DIR), name="renders")


class EpisodeRequest(BaseModel):
    event_id: str | None = None
    manual_topic: str | None = None
    target_length: str = "8 minutes"
    tone: str = "serious"
    visual_style: str = "premium international Apple-inspired broadcast"


class TemplatePreviewRequest(BaseModel):
    template_name: str
    headline: str = "Mars Enters Final Voting Cycle"
    summary: str = "A historic referendum could reshape political authority across Earth, Mars, Luna, and the Outer Belt."
    ticker: str = "MARS TURNOUT PROJECTION RISES TO 91% • LUNAR OXYGEN-CREDIT STRIKE ENTERS NINTH DAY • EUROPA SIGNAL UNDER REVIEW"
    lower_name: str = "ANAYA RAO"
    lower_title: str = "Senior Anchor • Earth-Orbit Media Ring"
    source: str = "Mars Civic Council Election Board"


class ScenePreviewRequest(BaseModel):
    scene: dict[str, Any]
    controls: dict[str, Any] = {}


class ExportRequest(BaseModel):
    script: str = ""
    scene_plan: Any = None
    metadata: Any = ""


class SaveEpisodeRequest(BaseModel):
    episode_id: str | None = None
    title: str = "Untitled 2147 News Episode"
    draft: dict[str, Any]


class RenderPackageRequest(BaseModel):
    episode_id: str = "2147-001-mars-independence"
    title: str = "Untitled 2147 News Episode"
    draft: dict[str, Any]
    resolution_width: int = 1920
    resolution_height: int = 1080


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "untitled-episode"


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def load_world() -> dict[str, Any]:
    return {
        "events": read_json(DATA_DIR / "events.json", []),
        "people": read_json(DATA_DIR / "people.json", []),
        "organizations": read_json(DATA_DIR / "organizations.json", []),
        "locations": read_json(DATA_DIR / "locations.json", []),
        "sources": read_json(DATA_DIR / "source_agencies.json", []),
        "season": read_json(DATA_DIR / "season_001_plan.json", []),
    }


def index_by_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item.get("id", ""): item for item in items}


def get_event(event_id: str | None) -> dict[str, Any] | None:
    if not event_id:
        return None
    events = index_by_id(load_world()["events"])
    return events.get(event_id)


def analyze_event_payload(event_id: str) -> dict[str, Any]:
    world = load_world()
    events = index_by_id(world["events"])
    people = index_by_id(world["people"])
    orgs = index_by_id(world["organizations"])
    locs = index_by_id(world["locations"])

    event = events.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    causes = [events.get(cid, {"id": cid, "title": cid}) for cid in event.get("causes", [])]
    actors = []
    for aid in event.get("actors", []):
        actors.append(people.get(aid) or orgs.get(aid) or {"id": aid, "name": aid})

    location = locs.get(event.get("location_id"), {"id": event.get("location_id"), "name": event.get("location_id")})
    score = int(event.get("importance", 5)) + len(event.get("ripple_seeds", [])) + len(event.get("actors", []))

    return {
        "event": event,
        "location": location,
        "causes": causes,
        "actors": actors,
        "score": score,
        "editorial_angle": "Cover as a developing causal story: explain what caused it, who is affected, and what ripples come next.",
        "visual_package": [
            "opening-intro-premium.html",
            "anchor-desk.html",
            "headline-cards.html",
            "mars-dashboard.html" if "mars" in event.get("title", "").lower() else "premium-base.html",
            "quote-card.html",
            "closing-transmission.html",
        ],
    }


def generate_episode_payload(req: EpisodeRequest) -> dict[str, Any]:
    world = load_world()
    people = index_by_id(world["people"])
    orgs = index_by_id(world["organizations"])
    event = get_event(req.event_id)

    topic = req.manual_topic or "Mars independence referendum"
    if event:
        topic = event.get("title", topic)
        headlines = [event.get("title", topic)] + [r.get("description", "") for r in event.get("ripple_seeds", [])[:4]]
        causes = [c for c in event.get("causes", [])]
        direct_effects = event.get("direct_effects", [])
    else:
        headlines = [
            f"{topic.title()} dominates the 2147 interplanetary news cycle.",
            "Earth Union officials prepare a formal response after orbital market uncertainty.",
            "Lunar Workers Guild renews life-support pricing demands.",
            "Synthetic Rights Tribunal requests jurisdictional review.",
            "Outer Belt Trade Registry warns of cargo insurance volatility.",
        ]
        causes = []
        direct_effects = []

    leila = people.get("person_leila_moreau", {})
    jiang = people.get("person_jiang_lau", {})
    ilyan = people.get("person_ilyan_sen", {})
    mars_council = orgs.get("org_mars_civic_council", {})

    script = f"""2147 NEWS NETWORK — PREMIUM EPISODE DRAFT

VISUAL STANDARD:
{req.visual_style}. The UI must look premium, minimal, international, and cinematic. Avoid cheap cyberpunk clutter.

TARGET LENGTH: {req.target_length}
TONE: {req.tone}

ANCHOR OPENING — ANAYA RAO:
Good evening. This is 2147 News Network, broadcasting from the New Delhi Orbital Broadcast Hub. Tonight's lead story: {topic}.

TOP HEADLINES:
""" + "\n".join(f"- {h}" for h in headlines) + f"""

MAIN REPORT:
According to {mars_council.get('name', 'Mars Civic Council')} records and interplanetary governance filings, tonight's development is not an isolated event. It follows years of off-world disputes over life-support pricing, cargo tariffs, settlement autonomy, and voting rights.

BACKGROUND CAUSAL CONTEXT:
Cause event IDs: {', '.join(causes) if causes else 'No cause IDs selected in this draft'}
Direct effects: {'; '.join(direct_effects) if direct_effects else 'To be determined by newsroom analysis'}

NAMED POLITICAL REACTION:
{leila.get('name', 'Leila Moreau')}, {leila.get('role', 'President')} of the {leila.get('organization', 'Mars Civic Council')}, said, “This is not a rejection of Earth. It is a demand for a legal structure that matches the reality of off-world life.”

MARKET REACTION:
{jiang.get('name', 'Jiang Lau')}, {jiang.get('role', 'Chief Executive Officer')} of {jiang.get('organization', 'Helion Grid Systems')}, warned that unresolved Earth-Mars treaty language could delay long-term fusion-grid contracts and cargo insurance pricing.

EXPERT CONTEXT:
{ilyan.get('name', 'Dr. Ilyan Sen')}, {ilyan.get('role', 'Political Historian')} at the {ilyan.get('organization', 'University of Valles Marineris')}, said, “Mars is no longer an outpost. It is a civilization asking for political recognition.”

CLOSING:
For Earth, Luna, Mars, and the Outer Belt, this is 2147 News Network. End transmission.
"""

    scene_plan = [
        {"id": "s01", "scene": "Opening Transmission", "duration": 15, "template": "opening-intro-premium.html", "purpose": "Establish premium network identity."},
        {"id": "s02", "scene": "Anchor Desk", "duration": 45, "template": "anchor-desk.html", "purpose": "Introduce lead story with Anaya Rao lower-third."},
        {"id": "s03", "scene": "Headline Cards", "duration": 45, "template": "headline-cards.html", "purpose": "Show top headlines and source labels."},
        {"id": "s04", "scene": "Data Dashboard", "duration": 90, "template": "mars-dashboard.html", "purpose": "Show numbers, source, and visual proof layer."},
        {"id": "s05", "scene": "Expert Quote", "duration": 35, "template": "quote-card.html", "purpose": "Add named expert credibility."},
        {"id": "s06", "scene": "Closing Transmission", "duration": 25, "template": "closing-transmission.html", "purpose": "Premium signoff and continuity."},
    ]

    metadata = {
        "title": f"{topic} | 2147 News Network",
        "description": "This is a fictional speculative news broadcast set in the year 2147. Created for entertainment and worldbuilding purposes.",
        "tags": ["2147 news", "future news", "fictional broadcast", "futurism", "Mars", "space politics", "AI rights"],
    }

    return {
        "title": metadata["title"],
        "headlines": headlines,
        "script": script,
        "scene_plan": scene_plan,
        "metadata": metadata,
    }


def saved_episode_path(episode_id: str) -> Path:
    safe_id = slugify(episode_id)
    return SAVED_EPISODES_DIR / f"{safe_id}.json"


def save_episode_payload(req: SaveEpisodeRequest) -> dict[str, Any]:
    SAVED_EPISODES_DIR.mkdir(parents=True, exist_ok=True)
    episode_id = slugify(req.episode_id or req.title)
    payload = {
        "episode_id": episode_id,
        "title": req.title,
        "draft": req.draft,
        "save_format": "2147nn-studio-draft-v1",
    }
    saved_episode_path(episode_id).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload


def list_saved_episodes() -> list[dict[str, Any]]:
    SAVED_EPISODES_DIR.mkdir(parents=True, exist_ok=True)
    items = []
    for path in sorted(SAVED_EPISODES_DIR.glob("*.json")):
        data = read_json(path, {})
        draft = data.get("draft", {})
        items.append({
            "episode_id": data.get("episode_id", path.stem),
            "title": data.get("title") or draft.get("title") or path.stem,
            "path": str(path.relative_to(ROOT)),
            "scene_count": len(draft.get("scene_plan", [])),
        })
    return items


def load_saved_episode(episode_id: str) -> dict[str, Any]:
    path = saved_episode_path(episode_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Saved episode not found")
    return read_json(path, {})


def template_default_context() -> dict[str, str]:
    return {
        "headline": "Mars Enters Final Voting Cycle",
        "summary": "A historic referendum could reshape political authority across Earth, Mars, Luna, and the Outer Belt.",
        "ticker": "MARS TURNOUT PROJECTION RISES TO 91% • LUNAR OXYGEN-CREDIT STRIKE ENTERS NINTH DAY • EUROPA SIGNAL UNDER REVIEW",
        "lower_name": "ANAYA RAO",
        "lower_title": "Senior Anchor • Earth-Orbit Media Ring",
        "source": "Mars Civic Council Election Board",
        "headline1": "Mars Enters Final Voting Cycle",
        "headline2": "CEO Jiang Lau Warns of Energy Contract Instability",
        "headline3": "Synthetic Rights Tribunal Receives AI Voting Petition",
        "timeline_year_1": "2136",
        "timeline_title_1": "Lunar oxygen-credit protests",
        "timeline_desc_1": "Life-support pricing becomes a political issue across off-world settlements.",
        "timeline_year_2": "2142",
        "timeline_title_2": "Mars challenges cargo tariff authority",
        "timeline_desc_2": "The Mars Civic Council disputes Earth Union control over interplanetary trade corridors.",
        "timeline_year_3": "2147",
        "timeline_title_3": "Final referendum cycle begins",
        "timeline_desc_3": "The autonomy dispute becomes a direct sovereignty vote across 42 Martian settlement zones.",
        "timeline_year_4": "Next",
        "timeline_title_4": "Emergency legal and market ripples",
        "timeline_desc_4": "Earth Union committees, energy companies, labor guilds, and tribunals prepare responses.",
        "finance_person_name": "JIANG LAU",
        "finance_person_title": "CEO • Helion Grid Systems",
        "finance_quote": "Energy markets can absorb political change. They cannot absorb legal uncertainty across two planets.",
        "metric_1_value": "+18.6%",
        "metric_1_label": "Cargo Insurance",
        "metric_2_value": "14 mo.",
        "metric_2_label": "Contract Delay Risk",
        "metric_3_value": "−4.2%",
        "metric_3_label": "Mars Infra Bonds",
        "finance_location": "Singapore Arcology Finance District",
        "legal_case_title": "Petition for referendum certification review",
        "legal_case_desc": "Filed on behalf of registered memory-continuity residents in Martian settlement zones.",
        "legal_person_name": "SELENE ARMITAGE",
        "legal_person_title": "Senior Counsel • Synthetic Rights Tribunal",
        "legal_quote": "Memory deletion without consent is no longer a technical action. It is a civil rights violation.",
        "legal_metric_1_value": "42",
        "legal_metric_1_label": "Settlement Zones",
        "legal_metric_2_value": "3.8M",
        "legal_metric_2_label": "Synthetic Residents",
        "legal_metric_3_value": "Pending",
        "legal_metric_3_label": "Jurisdiction",
        "legal_metric_4_value": "2147-CV",
        "legal_metric_4_label": "Case Track",
        "legal_location": "Geneva Continuity Court Complex",
        "quote_context": "Expert Analysis • University of Valles Marineris",
        "quote_person_name": "Dr. Ilyan Sen",
        "quote_person_title": "Political Historian • Mars Colony Seven Academic District",
        "quote_text": "Mars is no longer an outpost. It is a civilization asking for political recognition.",
        "breaking_status": "LIVE",
        "breaking_time": "19:42",
        "breaking_impact": "High",
        "breaking_verification": "2147NN Editorial Desk",
        "science_mission": "Europa Oceanic Research Consortium",
        "science_signal_status": "Repeating acoustic pattern",
        "science_instrument": "Cryo-hydrophone array K-4",
        "science_depth": "18.6 km beneath ice",
        "science_review_stage": "Independent verification",
        "science_signal_count": "3",
        "science_location": "Europa Research Base K-4",
        "climate_region": "Pacific Floating City Cluster 12",
        "climate_metric_1_value": "72 hrs",
        "climate_metric_1_label": "Shield Window",
        "climate_metric_2_value": "Category 6",
        "climate_metric_2_label": "Storm Model",
        "climate_metric_3_value": "18.4M",
        "climate_metric_3_label": "Residents Covered",
        "climate_metric_4_value": "94%",
        "climate_metric_4_label": "Grid Readiness",
        "lunar_region": "Lunar South Pole Mining Belt",
        "lunar_location": "Shackleton Habitat Cluster",
        "lunar_metric_1_value": "+22%",
        "lunar_metric_1_label": "Oxygen Credit Cost",
        "lunar_metric_2_value": "9 days",
        "lunar_metric_2_label": "Strike Duration",
        "lunar_metric_3_value": "31 sites",
        "lunar_metric_3_label": "Affected Mines",
        "lunar_metric_4_value": "4.2M t",
        "lunar_metric_4_label": "Helium-3 Delayed",
        "lunar_person_name": "TARO VENN",
        "lunar_person_title": "Lunar Labor Analyst • Shackleton Habitat Cluster",
    }


def build_template_context(*contexts: dict[str, Any]) -> dict[str, str]:
    merged: dict[str, Any] = template_default_context()
    for ctx in contexts:
        if ctx:
            merged.update(ctx)
    return {k: str(v) for k, v in merged.items() if v is not None}


def zip_directory(source_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in source_dir.rglob("*"):
            if file_path == zip_path or file_path.is_dir():
                continue
            zf.write(file_path, file_path.relative_to(source_dir))


def scene_render_context(scene: dict[str, Any]) -> dict[str, str]:
    return build_template_context(scene.get("template_controls", {}), {
        "headline": scene.get("headline") or scene.get("scene") or "2147 News Network",
        "summary": scene.get("summary") or scene.get("purpose") or scene.get("visual") or "Premium future-news scene.",
        "ticker": scene.get("ticker"),
        "lower_name": scene.get("lower_name"),
        "lower_title": scene.get("lower_title"),
        "source": scene.get("source"),
        "headline1": scene.get("headline") or scene.get("scene"),
    })


def standalone_scene_html(scene: dict[str, Any], index: int, total: int, width: int, height: int) -> str:
    template_name = scene.get("template") or "premium-base.html"
    inner = render_template(template_name, **scene_render_context(scene))
    title = scene.get("scene") or f"Scene {index + 1}"
    duration = scene.get("duration") or scene.get("duration_seconds") or 30
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} - 2147 News Network Render</title>
  <style>
    html, body {{ margin:0; width:100%; height:100%; background:#03040A; overflow:hidden; }}
    body {{ display:grid; place-items:center; font-family:Inter,-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',system-ui,sans-serif; }}
    .render-frame {{ width:{width}px; height:{height}px; transform-origin:center; }}
    .render-frame > div {{ width:100% !important; height:100% !important; min-height:{height}px !important; border-radius:0 !important; }}
    .render-meta {{ position:fixed; left:18px; top:14px; z-index:99999; padding:8px 10px; border-radius:999px; background:rgba(0,0,0,.42); color:#DDFBFF; font:700 11px/1.2 system-ui; letter-spacing:.08em; text-transform:uppercase; opacity:.28; }}
    @media (max-width: {width}px) {{ .render-frame {{ transform:scale(calc(100vw / {width})); }} }}
    @media (max-height: {height}px) {{ .render-frame {{ transform:scale(min(calc(100vw / {width}), calc(100vh / {height}))); }} }}
  </style>
</head>
<body>
  <div class="render-meta">Scene {index + 1}/{total} - {duration}s - {template_name}</div>
  <main class="render-frame">{inner}</main>
</body>
</html>"""


def create_render_package(req: RenderPackageRequest) -> dict[str, Any]:
    package_id = slugify(req.episode_id or req.title)
    package_dir = RENDER_DIR / package_id
    scenes_dir = package_dir / "scenes"
    scenes_dir.mkdir(parents=True, exist_ok=True)

    draft = req.draft or {}
    scenes = draft.get("scene_plan") or []
    manifest_scenes = []
    for index, scene in enumerate(scenes):
        scene_id = slugify(scene.get("id") or f"scene-{index+1}")
        file_name = f"{index+1:02d}-{scene_id}.html"
        html = standalone_scene_html(scene, index, len(scenes), req.resolution_width, req.resolution_height)
        (scenes_dir / file_name).write_text(html, encoding="utf-8")
        duration = int(scene.get("duration") or scene.get("duration_seconds") or 30)
        manifest_scenes.append({
            "index": index + 1,
            "id": scene.get("id") or scene_id,
            "title": scene.get("scene") or f"Scene {index+1}",
            "duration_seconds": duration,
            "template": scene.get("template"),
            "file": f"scenes/{file_name}",
            "url": f"/renders/{package_id}/scenes/{file_name}",
        })

    manifest = {
        "package_id": package_id,
        "title": req.title,
        "resolution": {"width": req.resolution_width, "height": req.resolution_height},
        "total_runtime_seconds": sum(s["duration_seconds"] for s in manifest_scenes),
        "scene_count": len(manifest_scenes),
        "scenes": manifest_scenes,
        "workflow": {
            "manual_recording": "Open each scene URL, record with OBS at 1920x1080, then assemble according to duration_seconds.",
            "future_automation": "Use Playwright/Chromium frame capture or OBS automation to record scenes."
        }
    }
    (package_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (package_dir / "draft.json").write_text(json.dumps(draft, indent=2, ensure_ascii=False), encoding="utf-8")
    readme = f"""# Render Package - {req.title}

Package ID: `{package_id}`

Resolution: {req.resolution_width}x{req.resolution_height}
Scenes: {len(manifest_scenes)}
Total runtime: {manifest['total_runtime_seconds']} seconds

## Manual Recording Workflow

1. Open each scene HTML URL in order.
2. Record browser window with OBS at {req.resolution_width}x{req.resolution_height}.
3. Use each scene's `duration_seconds` from `manifest.json`.
4. Assemble clips in DaVinci Resolve, Premiere, CapCut, or FFmpeg.
5. Add voiceover, music, SFX, subtitles, and final color/sound polish.

## Files

- `manifest.json` - scene list and durations
- `draft.json` - source episode draft
- `scenes/*.html` - standalone video-ready scene pages
"""
    (package_dir / "README.md").write_text(readme, encoding="utf-8")
    zip_path = package_dir / f"{package_id}-render-package.zip"
    zip_directory(package_dir, zip_path)
    return {
        "status": "ok",
        "package_id": package_id,
        "manifest_url": f"/renders/{package_id}/manifest.json",
        "readme_url": f"/renders/{package_id}/README.md",
        "zip_url": f"/renders/{package_id}/{package_id}-render-package.zip",
        "scene_urls": [s["url"] for s in manifest_scenes],
        "manifest": manifest,
    }


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    return HTMLResponse((STATIC_DIR / "index.html").read_text(encoding="utf-8"))


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "app": "2147 News Network Studio"})


@app.get("/api/world")
def api_world() -> JSONResponse:
    world = load_world()
    events = world["events"]
    payload = {
        "counts": {
            "active_events": len([e for e in events if e.get("status") == "active"]),
            "archived_events": len([e for e in events if e.get("status") == "archive"]),
            "people": len(world["people"]),
            "organizations": len(world["organizations"]),
            "locations": len(world["locations"]),
            "sources": len(world["sources"]),
            "ripple_seeds": sum(len(e.get("ripple_seeds", [])) for e in events),
        },
        **world,
    }
    return JSONResponse(payload)


@app.get("/api/events/{event_id}/analysis")
def api_analyze_event(event_id: str) -> JSONResponse:
    return JSONResponse(analyze_event_payload(event_id))


@app.post("/api/episode/generate")
def api_generate_episode(req: EpisodeRequest) -> JSONResponse:
    return JSONResponse(generate_episode_payload(req))


@app.get("/api/templates")
def api_templates() -> JSONResponse:
    return JSONResponse({"templates": available_templates()})


@app.post("/api/templates/preview")
def api_template_preview(req: TemplatePreviewRequest) -> HTMLResponse:
    html = render_template(
        req.template_name,
        **build_template_context({
            "headline": req.headline,
            "summary": req.summary,
            "ticker": req.ticker,
            "lower_name": req.lower_name,
            "lower_title": req.lower_title,
            "source": req.source,
            "headline1": req.headline,
        }),
    )
    return HTMLResponse(html)


@app.post("/api/scenes/preview")
def api_scene_preview(req: ScenePreviewRequest) -> HTMLResponse:
    scene = req.scene or {}
    controls = req.controls or {}
    template_name = scene.get("template") or controls.get("template_name") or "premium-base.html"
    html = render_template(
        template_name,
        **build_template_context(scene.get("template_controls", {}), controls, {
            "headline": controls.get("headline") or scene.get("headline") or scene.get("scene") or "Mars Enters Final Voting Cycle",
            "summary": controls.get("summary") or scene.get("summary") or scene.get("purpose") or "A developing story from the 2147 causal timeline.",
            "ticker": controls.get("ticker") or scene.get("ticker"),
            "lower_name": controls.get("lower_name") or scene.get("lower_name"),
            "lower_title": controls.get("lower_title") or scene.get("lower_title"),
            "source": controls.get("source") or scene.get("source"),
            "headline1": controls.get("headline") or scene.get("headline") or scene.get("scene"),
        }),
    )
    return HTMLResponse(html)


@app.get("/api/episodes")
def api_list_saved_episodes() -> JSONResponse:
    return JSONResponse({"episodes": list_saved_episodes()})


@app.get("/api/episodes/{episode_id}")
def api_load_saved_episode(episode_id: str) -> JSONResponse:
    return JSONResponse(load_saved_episode(episode_id))


@app.post("/api/episodes/save")
def api_save_episode(req: SaveEpisodeRequest) -> JSONResponse:
    payload = save_episode_payload(req)
    return JSONResponse({"status": "ok", "episode": {"episode_id": payload["episode_id"], "title": payload["title"]}})


@app.post("/api/render/package")
def api_create_render_package(req: RenderPackageRequest) -> JSONResponse:
    return JSONResponse(create_render_package(req))


@app.post("/api/export")
def api_export(req: ExportRequest) -> JSONResponse:
    EXPORT_DIR.mkdir(exist_ok=True)
    script_path = EXPORT_DIR / "episode-script.txt"
    scene_path = EXPORT_DIR / "scene-plan.json"
    metadata_path = EXPORT_DIR / "youtube-metadata.json"
    readme_path = EXPORT_DIR / "README.md"
    script_path.write_text(req.script, encoding="utf-8")
    scene_path.write_text(json.dumps(req.scene_plan, indent=2, ensure_ascii=False), encoding="utf-8")
    metadata_path.write_text(json.dumps(req.metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    readme_path.write_text(
        "# 2147 News Network Export\n\nFiles in this package:\n\n- episode-script.txt\n- scene-plan.json\n- youtube-metadata.json\n",
        encoding="utf-8",
    )
    zip_path = EXPORT_DIR / "2147-production-export.zip"
    zip_directory(EXPORT_DIR, zip_path)
    files = [
        {"name": "episode-script.txt", "url": "/exports/episode-script.txt"},
        {"name": "scene-plan.json", "url": "/exports/scene-plan.json"},
        {"name": "youtube-metadata.json", "url": "/exports/youtube-metadata.json"},
        {"name": "README.md", "url": "/exports/README.md"},
        {"name": "2147-production-export.zip", "url": "/exports/2147-production-export.zip"},
    ]
    return JSONResponse({"status": "ok", "files": files, "zip_url": "/exports/2147-production-export.zip"})
