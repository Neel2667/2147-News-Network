import json
from pathlib import Path

import gradio as gr

from src.template_renderer import available_templates, render_template

ROOT = Path(__file__).parent
EPISODE_PATH = ROOT / "episodes" / "episode-001-mars-independence.json"
DATA_DIR = ROOT / "data"


def load_json(path: Path, fallback):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def load_seed_episode():
    return load_json(EPISODE_PATH, {})


def load_world():
    return {
        "events": load_json(DATA_DIR / "events.json", []),
        "people": load_json(DATA_DIR / "people.json", []),
        "organizations": load_json(DATA_DIR / "organizations.json", []),
        "locations": load_json(DATA_DIR / "locations.json", []),
        "sources": load_json(DATA_DIR / "source_agencies.json", []),
    }


def by_id(items):
    return {item.get("id"): item for item in items}


def active_event_choices():
    events = load_world()["events"]
    return [f"{e.get('id')} — {e.get('title')}" for e in events]


def summarize_world():
    world = load_world()
    events = world["events"]
    active = [e for e in events if e.get("status") == "active"]
    archived = [e for e in events if e.get("status") == "archive"]
    ripples = sum(len(e.get("ripple_seeds", [])) for e in events)
    lines = [
        "# 2147 Newsroom World Dashboard",
        "",
        f"Active events: **{len(active)}**",
        f"Archived context events: **{len(archived)}**",
        f"Known people: **{len(world['people'])}**",
        f"Known organizations: **{len(world['organizations'])}**",
        f"Known locations: **{len(world['locations'])}**",
        f"Ripple seeds: **{ripples}**",
        "",
        "## Active Developing Stories",
    ]
    for e in active:
        lines += [
            f"### {e.get('title')}",
            f"- Date: {e.get('date')} / {e.get('time')}",
            f"- Category: {e.get('category')}",
            f"- Importance: {e.get('importance')}/10",
            f"- Summary: {e.get('summary')}",
        ]
    return "\n".join(lines)


def analyze_event(choice: str):
    world = load_world()
    event_id = (choice or "").split(" — ")[0]
    events = by_id(world["events"])
    people = by_id(world["people"])
    orgs = by_id(world["organizations"])
    locs = by_id(world["locations"])
    event = events.get(event_id)
    if not event:
        return "Select an event to analyze.", "[]"

    cause_lines = []
    for cid in event.get("causes", []):
        c = events.get(cid, {"title": cid})
        cause_lines.append(f"- {c.get('date', 'unknown')}: {c.get('title')}")

    actor_lines = []
    for aid in event.get("actors", []):
        actor = people.get(aid) or orgs.get(aid) or {"name": aid, "type": "unknown"}
        label = actor.get("name") or actor.get("id")
        detail = actor.get("role") or actor.get("type") or actor.get("organization") or ""
        actor_lines.append(f"- **{label}** — {detail}")

    loc = locs.get(event.get("location_id"), {})
    ripple_lines = []
    for r in event.get("ripple_seeds", []):
        ripple_lines.append(
            f"- **{r.get('type')}** / probability {r.get('probability')} / +{r.get('delay_days')} days: {r.get('description')}"
        )

    report = f"""# Event Analysis

## Main Event

**{event.get('title')}**

{event.get('summary')}

- Date: {event.get('date')}
- Time: {event.get('time')}
- Category: {event.get('category')}
- Status: {event.get('status')}
- Importance: {event.get('importance')}/10
- Location: {loc.get('name', event.get('location_id'))}

## Why This Event Exists

{chr(10).join(cause_lines) if cause_lines else '- No earlier causes recorded yet.'}

## Affected Actors

{chr(10).join(actor_lines) if actor_lines else '- No actors recorded.'}

## Direct Effects

{chr(10).join('- ' + x for x in event.get('direct_effects', []))}

## Likely Ripple Events

{chr(10).join(ripple_lines) if ripple_lines else '- No ripple seeds recorded.'}

## Newsroom Angle

This should be covered as a serious developing story, with the background causes shown clearly so the audience feels the event is part of a real historical chain.
"""
    return report, json.dumps(event, indent=2)


def generate_episode(topic: str, length: str, tone: str, event_choice: str):
    world = load_world()
    event_id = (event_choice or "").split(" — ")[0]
    event = by_id(world["events"]).get(event_id)
    people = by_id(world["people"])
    orgs = by_id(world["organizations"])

    if event:
        topic = event.get("title")
        ripples = event.get("ripple_seeds", [])[:4]
        headlines = [event.get("title")] + [r.get("description") for r in ripples]
    else:
        if not topic.strip():
            topic = "Mars independence referendum"
        headlines = [
            f"{topic.title()} dominates the 2147 interplanetary news cycle.",
            "Lunar workers call for oxygen-credit reform after emergency council talks.",
            "Pacific floating cities activate storm shields before superstorm season.",
            "Earth Union Senate expands neural privacy protections.",
            "Europa research probe reports a repeating signal beneath the ice.",
        ]

    leila = people.get("person_leila_moreau", {})
    jiang = people.get("person_jiang_lau", {})
    mars_council = orgs.get("org_mars_civic_council", {})

    title = f"{topic} | 2147 News Network"
    script = f"""2147 NEWS NETWORK — PREMIUM EPISODE DRAFT

Tone: {tone}
Target length: {length}
Visual standard: Apple-inspired premium broadcast UI with glass depth, restrained color, beautiful typography, and smooth motion.

ANCHOR OPENING — ANAYA RAO:
Good evening. This is 2147 News Network, broadcasting from the New Delhi Orbital Broadcast Hub. Tonight's lead story: {topic}.

TOP HEADLINES:
""" + "\n".join(f"- {h}" for h in headlines) + f"""

MAIN REPORT:
The story is developing across Earth, Luna, Mars, and the Outer Belt. According to the {mars_council.get('name', 'Mars Civic Council')}, the latest update is connected to earlier off-world governance disputes and is now creating new political, legal, and market consequences.

BACKGROUND CONTEXT:
This event should be presented not as an isolated headline, but as the latest chapter in a causal chain. Earlier oxygen-credit protests, Earth-Mars tariff disputes, and settlement autonomy debates created the conditions for tonight's development.

NAMED REACTION:
{leila.get('name', 'Leila Moreau')}, {leila.get('role', 'President')} of the {leila.get('organization', 'Mars Civic Council')}, said, “This is not a rejection of Earth. It is a demand for a legal structure that matches the reality of off-world life.”

MARKET REACTION:
{jiang.get('name', 'Jiang Lau')}, {jiang.get('role', 'CEO')} of {jiang.get('organization', 'Helion Grid Systems')}, warned that unresolved treaty language could delay long-term fusion-grid contracts and cargo insurance pricing.

VISUAL PACKAGE:
- premium opening transmission
- anchor desk with lower-third
- headline cards
- Mars referendum dashboard
- expert quote card
- closing transmission

CLOSING:
For Earth, Luna, Mars, and the Outer Belt, this is 2147 News Network. End transmission.
"""

    scenes = [
        {"scene": "Opening Transmission", "duration": "15s", "template": "opening-intro-premium.html", "visual": "Premium orbital intro, glass logo reveal, Earth/Mars/Luna network."},
        {"scene": "Anchor Desk", "duration": "45s", "template": "anchor-desk.html", "visual": "Anaya Rao lower-third, premium newsroom wall, main headline panel."},
        {"scene": "Headline Cards", "duration": "45s", "template": "headline-cards.html", "visual": "Apple-style headline cards with source labels and timestamps."},
        {"scene": "Mars Dashboard", "duration": "90s", "template": "mars-dashboard.html", "visual": "Mars globe, colony markers, referendum data bars."},
        {"scene": "Expert Quote", "duration": "35s", "template": "quote-card.html", "visual": "Dr. Ilyan Sen quote card with archive waveform."},
        {"scene": "Closing Transmission", "duration": "25s", "template": "closing-transmission.html", "visual": "Elegant end transmission with orbit rings."},
    ]

    metadata = f"""YouTube Title:
{title}

Description:
This is a fictional speculative news broadcast set in the year 2147. Created for entertainment and worldbuilding purposes.

Tonight on 2147 News Network: {topic} and related developments across Earth, Luna, Mars, and the Outer Belt.

Tags:
2147 news, future news, sci fi news, fictional broadcast, futurism, Mars, AI rights, space politics, climate future
"""
    return "\n".join(headlines), script, json.dumps(scenes, indent=2), metadata


def preview_template(template_name: str, headline: str, summary: str):
    ticker = "MARS TURNOUT PROJECTION RISES TO 91% • LUNAR OXYGEN-CREDIT STRIKE ENTERS NINTH DAY • EUROPA SIGNAL UNDER REVIEW"
    return render_template(
        template_name,
        headline=headline or "Mars Enters Final Voting Cycle",
        summary=summary or "A historic referendum could reshape political authority across Earth, Mars, Luna, and the Outer Belt.",
        ticker=ticker,
        headline1="Mars Enters Final Voting Cycle",
        headline2="CEO Jiang Lau Warns of Energy Contract Instability",
        headline3="Synthetic Rights Tribunal Receives AI Voting Petition",
    )


def export_bundle(script: str, scenes: str, metadata: str):
    export_dir = ROOT / "exports"
    export_dir.mkdir(exist_ok=True)
    (export_dir / "episode-script.txt").write_text(script or "", encoding="utf-8")
    (export_dir / "scene-plan.json").write_text(scenes or "[]", encoding="utf-8")
    (export_dir / "youtube-metadata.txt").write_text(metadata or "", encoding="utf-8")
    return "Exported to exports/episode-script.txt, exports/scene-plan.json, and exports/youtube-metadata.txt"


templates = available_templates()
default_template = "opening-intro-premium.html" if "opening-intro-premium.html" in templates else templates[0]

with gr.Blocks(title="2147 News Network", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 2147 News Network")
    gr.Markdown("Premium future-news production system. No AI-generated images or videos. UI quality is the product.")

    with gr.Tab("World Dashboard"):
        refresh_world = gr.Button("Refresh World Dashboard")
        world_md = gr.Markdown(value=summarize_world())
        refresh_world.click(summarize_world, outputs=world_md)

    with gr.Tab("Event Analyzer"):
        event_choice = gr.Dropdown(active_event_choices(), label="Select World Event", value=active_event_choices()[-1] if active_event_choices() else None)
        analyze_btn = gr.Button("Analyze Event")
        analysis_md = gr.Markdown()
        event_json = gr.Code(label="Event JSON", language="json")
        analyze_btn.click(analyze_event, inputs=event_choice, outputs=[analysis_md, event_json])

    with gr.Tab("Episode Generator"):
        with gr.Row():
            topic = gr.Textbox(label="Manual Topic Override", value="Mars independence referendum")
            length = gr.Dropdown(["5 minutes", "8 minutes", "12 minutes", "20 minutes"], value="8 minutes", label="Target Length")
            tone = gr.Dropdown(["serious", "dramatic", "documentary", "urgent breaking news"], value="serious", label="Tone")
        btn = gr.Button("Generate Premium Episode Draft")
        headlines = gr.Textbox(label="Headlines", lines=7)
        script = gr.Textbox(label="Episode Script", lines=22)
        scenes = gr.Code(label="Scene Plan JSON", language="json")
        metadata = gr.Textbox(label="YouTube Metadata", lines=10)
        export_btn = gr.Button("Export Draft Files")
        export_status = gr.Textbox(label="Export Status")
        btn.click(generate_episode, inputs=[topic, length, tone, event_choice], outputs=[headlines, script, scenes, metadata])
        export_btn.click(export_bundle, inputs=[script, scenes, metadata], outputs=export_status)

    with gr.Tab("Premium Visual Preview"):
        gr.Markdown("## Premium UI Templates")
        with gr.Row():
            template_select = gr.Dropdown(templates, value=default_template, label="Template")
            preview_headline = gr.Textbox(label="Preview Headline", value="Mars Enters Final Voting Cycle")
        preview_summary = gr.Textbox(label="Preview Summary", value="A historic referendum could reshape political authority across Earth, Mars, Luna, and the Outer Belt.")
        preview_btn = gr.Button("Render Template")
        preview = gr.HTML(value=preview_template(default_template, "Mars Enters Final Voting Cycle", "A historic referendum could reshape political authority across Earth, Mars, Luna, and the Outer Belt."))
        preview_btn.click(preview_template, inputs=[template_select, preview_headline, preview_summary], outputs=preview)

if __name__ == "__main__":
    demo.launch()
