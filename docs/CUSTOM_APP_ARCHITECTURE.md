# Custom App Architecture — 2147 News Network Studio

Last updated: 2026-06-16

## Decision

The project is moving away from a Gradio-first interface. Gradio is useful for quick demos, but the user wants a premium production app with all controls needed for a serious newsroom workflow.

The main app is now a custom FastAPI + HTML/CSS/JavaScript application.

## Why Custom App

A custom app gives full control over:

- premium UI design
- complex controls
- scene timeline editing
- visual preview stage
- export workflow
- event graph interactions
- future drag-and-drop episode builder
- keyboard shortcuts
- advanced newsroom panels
- Apple-inspired animations and layout

## Main Files

```text
main.py                 FastAPI backend
static/index.html       custom app shell
static/styles.css       premium UI styling
static/app.js           frontend controls and API calls
src/template_renderer.py template loader
src/design_tokens.py    visual design constants
Dockerfile              Hugging Face custom deployment
```

## Current App Sections

1. World Dashboard
2. Event Analyzer
3. Episode Builder
4. Scene Timeline
5. Visual Preview
6. Export Center

## API Endpoints

```text
GET  /                         custom app UI
GET  /api/world                world state
GET  /api/events/{id}/analysis event causal analysis
POST /api/episode/generate     episode draft generator
GET  /api/templates            list visual templates
POST /api/templates/preview    render template preview
POST /api/scenes/preview       render selected timeline scene with controls
GET  /api/episodes             list saved drafts
GET  /api/episodes/{id}        load saved draft
POST /api/episodes/save        save current draft
POST /api/render/package       create standalone HTML scene render package
POST /api/export               export current draft
```

## Hugging Face Deployment

Use Docker Space.

The Dockerfile runs:

```text
uvicorn main:app --host 0.0.0.0 --port 7860
```

## Legacy Gradio App

`app.py` may remain temporarily as a legacy prototype, but the production direction is `main.py`.

Future agents should prioritize the custom app.
