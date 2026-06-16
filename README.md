# 2147 News Network

**2147 News Network** is a fictional futuristic YouTube news-show production system. It creates scripts, scene plans, web-rendered motion graphics, and production notes for a speculative news broadcast set in the year **2147**.

> Tagline: **Broadcasting from tomorrow.**

## Core Rule

This project does **not** use AI-generated images or AI-generated videos.

Allowed:
- AI-assisted text/script generation
- manually designed HTML/CSS/SVG visuals
- procedural Canvas/WebGL animations
- public-domain footage such as NASA media
- licensed stock footage
- self-shot footage
- charts, maps, dashboards, tickers, and lower-thirds generated with code

Not allowed:
- AI-generated future city images
- AI-generated video clips
- AI avatars
- AI-generated photorealistic characters/backgrounds

## Current Status

See [`PROJECT_STATUS.md`](PROJECT_STATUS.md) and [`HANDOFF.md`](HANDOFF.md).

## Planned Deployment

The production tool is designed for **Hugging Face Spaces** using **Gradio**.

## Main Outputs

The app will generate:
- fictional future headlines
- episode script
- scene-by-scene video plan
- narration script
- ticker text
- lower-third text
- visual template choices
- YouTube title, description, tags
- HTML preview scenes for web-rendered graphics

## First Target Episode

**Mars Votes for Independence From Earth | 2147 News Network**

A serious fictional broadcast covering:
- Mars independence referendum
- Lunar oxygen-credit strike
- Pacific floating city storm shields
- neural privacy law
- Europa ocean probe signal


## Custom Studio App

The production tool is now a custom FastAPI app, not a Gradio-first interface.

Run locally:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 7860
```

Open:

```text
http://localhost:7860
```

Use the **Load Pilot Episode** button to open the first production package:

```text
2147-001-mars-independence
```

## Hugging Face Deployment

Deploy as a **Docker Space**. See:

```text
docs/HUGGING_FACE_DEPLOYMENT.md
```


## Render / Export Workflow

The custom app can create video-ready scene packages. In the app, open **Save, Load & Export Center** and click:

```text
Create Video-Ready Scene Package
```

This creates standalone 1920×1080 HTML scene files under:

```text
render_packages/{episode_id}/
```

Read:

```text
docs/RENDER_EXPORT_WORKFLOW.md
```
