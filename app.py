import json
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).parent
EPISODE_PATH = ROOT / "episodes" / "episode-001-mars-independence.json"


def load_seed_episode():
    with open(EPISODE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_episode(topic: str, length: str, tone: str):
    """Deterministic MVP generator.

    This first version does not call an external LLM. It creates a usable
    episode plan from templates. Later this can be replaced or extended with
    AI-assisted text generation while still avoiding AI-generated images/videos.
    """
    if not topic.strip():
        topic = "Mars independence referendum"

    seed = load_seed_episode()
    title = f"{topic.title()} | 2147 News Network"

    headlines = [
        f"{topic.title()} dominates the 2147 interplanetary news cycle.",
        "Lunar workers call for oxygen-credit reform after emergency council talks.",
        "Pacific floating cities activate storm shields before superstorm season.",
        "Earth Union Senate expands neural privacy protections.",
        "Europa research probe reports a repeating signal beneath the ice."
    ]

    script = f"""2147 NEWS NETWORK — EPISODE DRAFT

Tone: {tone}
Target length: {length}

ANCHOR OPENING:
Good evening. This is 2147 News Network, broadcasting from the Earth-Orbit Media Ring.
Tonight's lead story: {topic}.

HEADLINES:
""" + "\n".join(f"- {h}" for h in headlines) + f"""

MAIN STORY:
The story of {topic} has become one of the defining questions of 2147. Officials across Earth, Luna, Mars, and the Outer Belt are watching closely as the decision could reshape law, trade, migration, and identity across human civilization.

DATA PANEL:
- Broadcast year: 2147
- Main region: Earth-Mars-Luna network
- Public impact: high
- Political sensitivity: elevated
- Visual package: holographic maps, vote dashboards, expert quote cards, data ticker

FICTIONAL EXPERT QUOTE:
Dr. Ilyan Sen, University of Valles Marineris:
\"This is not just a policy dispute. It is a test of whether human civilization can govern across worlds.\"

CLOSING:
For Earth, Luna, Mars, and the Outer Belt, this is 2147 News Network. End transmission.
"""

    scenes = [
        {"scene": "Opening Transmission", "duration": "15s", "template": "opening_intro", "visual": "Logo, globe grid, cyan transmission lines"},
        {"scene": "Headline Montage", "duration": "45s", "template": "headline_cards", "visual": "Animated cards and lower ticker"},
        {"scene": "Anchor Desk", "duration": "45s", "template": "anchor_desk", "visual": "Futuristic newsroom with main topic panel"},
        {"scene": "Main Data Dashboard", "duration": "90s", "template": "data_dashboard", "visual": "Charts, counters, timeline, region markers"},
        {"scene": "Expert Quote", "duration": "30s", "template": "quote_card", "visual": "Silhouette card, waveform, quote text"},
        {"scene": "Closing Transmission", "duration": "25s", "template": "closing_transmission", "visual": "End transmission and subscribe CTA"},
    ]

    scene_json = json.dumps(scenes, indent=2)
    metadata = f"""YouTube Title:
{title}

Description:
This is a fictional speculative news broadcast set in the year 2147. Created for entertainment and worldbuilding purposes.

Tonight on 2147 News Network: {topic} and other major developments across Earth, Mars, Luna, and the Outer Belt.

Tags:
2147 news, future news, sci fi news, fictional broadcast, futurism, Mars, AI rights, space politics, climate future
"""

    return "\n".join(headlines), script, scene_json, metadata


def load_intro_html():
    path = ROOT / "templates" / "opening-intro.html"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "<p>Template not found.</p>"


with gr.Blocks(title="2147 News Network") as demo:
    gr.Markdown("# 2147 News Network")
    gr.Markdown("Fictional future-news episode generator. No AI-generated images or videos.")

    with gr.Row():
        topic = gr.Textbox(label="Episode Topic", value="Mars independence referendum")
        length = gr.Dropdown(["5 minutes", "8 minutes", "12 minutes", "20 minutes"], value="8 minutes", label="Target Length")
        tone = gr.Dropdown(["serious", "dramatic", "documentary", "urgent breaking news"], value="serious", label="Tone")

    btn = gr.Button("Generate Episode Draft")

    headlines = gr.Textbox(label="Headlines", lines=7)
    script = gr.Textbox(label="Episode Script", lines=20)
    scenes = gr.Code(label="Scene Plan JSON", language="json")
    metadata = gr.Textbox(label="YouTube Metadata", lines=10)

    gr.Markdown("## Opening Intro HTML Preview")
    intro_preview = gr.HTML(value=load_intro_html())

    btn.click(generate_episode, inputs=[topic, length, tone], outputs=[headlines, script, scenes, metadata])

if __name__ == "__main__":
    demo.launch()
