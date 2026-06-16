# Hugging Face Space Metadata — 2147 News Network Studio

Last updated: 2026-06-16

## Recommended Space Settings

```yaml
title: 2147 News Network Studio
emoji: 🛰️
colorFrom: blue
colorTo: cyan
sdk: docker
app_port: 7860
pinned: false
```

These settings have been added to the top of the root `README.md` as Hugging Face Space metadata.

## Recommended Space Name

```text
2147-News-Network-Studio
```

## Short Description

```text
A custom future-news production studio for building premium fictional broadcasts from the year 2147.
```

## Long Description

```text
2147 News Network Studio is a custom FastAPI + HTML/CSS/JavaScript production tool for creating a fictional international news broadcast from the year 2147. It includes a causal world-event system, premium Apple-inspired UI templates, scene timeline editing, template-specific controls, pilot episode package, export tools, and video-ready scene render packages.
```

## Tags

```text
future-news
fictional-broadcast
worldbuilding
fastapi
docker
video-production
motion-graphics
sci-fi
futurism
```

## Visibility Recommendation

For early development:

```text
Private
```

For public demo after first polish pass:

```text
Public
```

## Runtime

The app runs on port:

```text
7860
```

Docker command:

```bash
uvicorn main:app --host 0.0.0.0 --port 7860
```

## Health Check

After deployment, open:

```text
https://YOUR-SPACE.hf.space/health
```

Expected:

```json
{"status":"ok","app":"2147 News Network Studio"}
```
