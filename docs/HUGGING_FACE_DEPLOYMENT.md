# Hugging Face Deployment Guide — 2147 News Network Studio

Last updated: 2026-06-16

## Deployment Type

Use a **Hugging Face Docker Space**.

The production app is a custom FastAPI + HTML/CSS/JavaScript application. It is **not** a Gradio-first app.

## Why Docker Space

Docker gives us full control over:

- custom UI
- FastAPI backend
- static frontend
- future render/export workflows
- project file structure
- advanced controls that Gradio cannot provide cleanly

## Required Files

The repo already includes:

```text
Dockerfile
main.py
requirements.txt
static/index.html
static/styles.css
static/app.js
templates/
data/
episodes/
```

## Hugging Face Space Setup

1. Go to Hugging Face.
2. Create a new Space.
3. Choose:

```text
SDK: Docker
```

4. Connect or upload this GitHub repository:

```text
https://github.com/Neel2667/2147-News-Network
```

5. Make sure the Space builds from the root of the repo.

## Dockerfile Behavior

The Dockerfile runs:

```bash
uvicorn main:app --host 0.0.0.0 --port 7860
```

Hugging Face expects the app to listen on port `7860`, which is already configured.

## Local Test Before Deploy

Run:

```bash
cd 2147-News-Network
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 7860
```

Open:

```text
http://localhost:7860
```

Health check:

```text
http://localhost:7860/health
```

Expected response:

```json
{"status":"ok","app":"2147 News Network Studio"}
```

## First Production Action After Deploy

Click:

```text
Load Pilot Episode
```

This loads:

```text
2147-001-mars-independence
```

Then open:

```text
Scene Timeline
```

Preview and tune each pilot scene.

## Important Persistence Note

On Hugging Face Spaces, files written at runtime may not be permanently committed back to GitHub automatically.

For serious production persistence, use one of these later:

1. commit saved drafts back to GitHub manually
2. Hugging Face persistent storage
3. external database
4. export JSON and download it

For now, the app includes a saved pilot draft in the repository:

```text
episodes/saved/2147-001-mars-independence.json
```

## Environment Variables

No secrets are currently required.

Do not put GitHub tokens or API keys in the repo.

## Current App Sections

- World Dashboard
- Event Analyzer
- Episode Builder
- Scene Timeline
- Visual Preview
- Save, Load & Export Center

## Next Deployment Improvements

- Add authentication if the app becomes private production software.
- Add persistent storage.
- Add download buttons for saved/exported packages.
- Add video render queue when render workflow is ready.


## Metadata Files Added

The root `README.md` now includes Hugging Face Space metadata. Additional deployment references:

```text
docs/HF_SPACE_METADATA.md
docs/FINAL_DEPLOY_CHECKLIST.md
docs/DEPLOYMENT_STATUS.md
```

A `.dockerignore` file has also been added to keep runtime artifacts and local files out of Docker build context.
