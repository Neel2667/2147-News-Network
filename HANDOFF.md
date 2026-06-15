# Handoff Guide for Future AI/Developer

This file exists so another AI or developer can resume the project without confusion.

## Project Summary

The user wants a complete project for a YouTube channel called **2147 News Network**. It is a fictional news channel broadcasting from the year 2147.

The project should be deployed on Hugging Face Spaces. It should help generate episode scripts, scene plans, and web-based visual templates.

## Critical Constraint

Do not use AI-generated images or AI-generated videos.

Scripts and text may be AI-assisted. Visuals must come from:
- HTML/CSS/SVG/Canvas/WebGL
- public-domain footage
- licensed stock footage
- self-shot footage
- manually designed graphics

## Security Constraint

The user pasted a GitHub token in the chat. Do not use it. Do not save it. Do not paste it into commands. Tell the user to revoke it and create a new token.

## Repository

User repository:

https://github.com/Neel2667/2147-News-Network

If pushing is required, use safe GitHub authentication outside committed files:
- GitHub CLI login
- SSH key
- environment variable provided securely by the platform
- a new revoked/replaced token entered by the user locally, not in chat

## Current File Structure

```text
2147-News-Network/
  README.md
  PROJECT_STATUS.md
  HANDOFF.md
  ROADMAP.md
  requirements.txt
  app.py
  .gitignore
  docs/
  reports/
  episodes/
  templates/
  assets/
  src/
```

## Recommended Next Step

Finish the MVP Gradio app:
- topic input
- generate headlines
- generate script
- generate scene list
- export outputs
- preview visual templates

## MVP Visual Templates

Build these first:
1. opening intro
2. anchor desk
3. headline cards
4. Mars dashboard
5. data chart
6. quote/interview card
7. breaking news alert
8. closing transmission

## First Episode

Title:

**Mars Votes for Independence From Earth | 2147 News Network**

Main story:
Mars enters final voting cycle for independence from Earth Union.

Supporting stories:
- Lunar miners demand oxygen-credit reform
- Pacific floating cities activate storm shields
- Neural privacy treaty passes Earth Union Senate
- Europa probe detects repeating acoustic signal

## Style

Visual style:
- dark navy/black
- cyan holographic UI
- amber/red warnings
- futuristic newsroom
- moving tickers
- animated maps
- dashboards
- serious broadcast tone

## Important Docs

Read in this order:
1. README.md
2. PROJECT_STATUS.md
3. docs/MASTER_PLAN.md
4. docs/CONTENT_BIBLE.md
5. docs/VISUAL_POLICY.md
6. docs/PRODUCTION_PIPELINE.md
7. docs/REALISM_GUIDE.md
8. docs/CAUSAL_EVENT_ENGINE.md
9. data/events.json
10. data/people.json
11. data/organizations.json
12. data/locations.json
13. data/source_agencies.json
14. episodes/episode-001-mars-independence.json


## Realism Update

The user wants the channel to feel extremely real and specific. Avoid vague references like "the CEO said". Use full names, titles, organizations, locations, timestamps, and source labels. Example: "Helion Grid Systems CEO Jiang Lau said..." Read docs/REALISM_GUIDE.md before generating scripts.


## Causal Event Engine Update

The user wants news to emerge from cause-and-effect, not isolated headline generation. Every event should have causes and ripple effects. Use data/events.json as the beginning of the world timeline. Read docs/CAUSAL_EVENT_ENGINE.md before changing the generator.
