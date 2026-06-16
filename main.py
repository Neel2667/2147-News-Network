"""Custom 2147 News Network Studio app.

This replaces the Gradio-first approach with a fully custom FastAPI web app so
we can control the UI, controls, layout, and future production workflow.
"""
from __future__ import annotations

import json
import re
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

app = FastAPI(title="2147 News Network Studio", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


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


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    return HTMLResponse((STATIC_DIR / "index.html").read_text(encoding="utf-8"))


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
        headline=req.headline,
        summary=req.summary,
        ticker=req.ticker,
        lower_name=req.lower_name,
        lower_title=req.lower_title,
        source=req.source,
        headline1=req.headline,
        headline2="CEO Jiang Lau Warns of Energy Contract Instability",
        headline3="Synthetic Rights Tribunal Receives AI Voting Petition",
    )
    return HTMLResponse(html)


@app.post("/api/scenes/preview")
def api_scene_preview(req: ScenePreviewRequest) -> HTMLResponse:
    scene = req.scene or {}
    controls = req.controls or {}
    template_name = scene.get("template") or controls.get("template_name") or "premium-base.html"
    html = render_template(
        template_name,
        headline=controls.get("headline") or scene.get("scene") or "Mars Enters Final Voting Cycle",
        summary=controls.get("summary") or scene.get("purpose") or "A developing story from the 2147 causal timeline.",
        ticker=controls.get("ticker") or "MARS TURNOUT PROJECTION RISES TO 91% • LUNAR OXYGEN-CREDIT STRIKE ENTERS NINTH DAY • EUROPA SIGNAL UNDER REVIEW",
        lower_name=controls.get("lower_name") or "ANAYA RAO",
        lower_title=controls.get("lower_title") or "Senior Anchor • Earth-Orbit Media Ring",
        source=controls.get("source") or "Mars Civic Council Election Board",
        headline1=controls.get("headline") or "Mars Enters Final Voting Cycle",
        headline2="CEO Jiang Lau Warns of Energy Contract Instability",
        headline3="Synthetic Rights Tribunal Receives AI Voting Petition",
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


@app.post("/api/export")
def api_export(req: ExportRequest) -> JSONResponse:
    EXPORT_DIR.mkdir(exist_ok=True)
    (EXPORT_DIR / "episode-script.txt").write_text(req.script, encoding="utf-8")
    (EXPORT_DIR / "scene-plan.json").write_text(json.dumps(req.scene_plan, indent=2), encoding="utf-8")
    (EXPORT_DIR / "youtube-metadata.json").write_text(json.dumps(req.metadata, indent=2), encoding="utf-8")
    return JSONResponse({"status": "ok", "files": ["exports/episode-script.txt", "exports/scene-plan.json", "exports/youtube-metadata.json"]})
