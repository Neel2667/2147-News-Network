# Final Deploy Checklist — Hugging Face Space

Last updated: 2026-06-16

## 1. GitHub Repository Check

- [ ] Latest code pushed to GitHub main branch
- [ ] `Dockerfile` exists
- [ ] `requirements.txt` exists
- [ ] `main.py` exists
- [ ] `static/` frontend exists
- [ ] `templates/` visual templates exist
- [ ] `episodes/saved/2147-001-mars-independence.json` exists
- [ ] root `README.md` includes Hugging Face Space metadata
- [ ] no tokens or secrets committed

## 2. Local Test

Run locally:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 7860
```

Open:

```text
http://localhost:7860
```

Check:

- [ ] app loads
- [ ] `/health` returns ok
- [ ] World Dashboard loads
- [ ] Load Pilot Episode button works
- [ ] Scene Timeline opens
- [ ] templates preview correctly
- [ ] Save Draft works
- [ ] Export Current Draft works
- [ ] Create Video-Ready Scene Package works
- [ ] download links appear

## 3. Hugging Face Space Creation

Create new Space:

```text
SDK: Docker
Name: 2147-News-Network-Studio
```

Recommended visibility at first:

```text
Private
```

Then connect/upload repo.

## 4. Build Verification

After Hugging Face build starts:

- [ ] Docker build completes
- [ ] app starts on port 7860
- [ ] no missing dependency errors
- [ ] `/health` works
- [ ] root app page loads

## 5. First App Test on Hugging Face

In deployed app:

- [ ] click **Load Pilot Episode**
- [ ] verify the app switches to Scene Timeline
- [ ] preview Opening Transmission
- [ ] preview Mars Dashboard
- [ ] preview Financial Desk
- [ ] preview Legal Desk
- [ ] create render package
- [ ] open at least one render scene URL
- [ ] download production export ZIP

## 6. Known Persistence Warning

Runtime-generated files may not persist permanently on Hugging Face unless persistent storage is enabled.

This affects:

```text
exports/
render_packages/
episodes/saved/ edits made at runtime
```

For now:

- [ ] download exports after generating
- [ ] commit important saved drafts back to GitHub manually
- [ ] consider Hugging Face persistent storage later

## 7. Security Check

- [ ] no GitHub token in files
- [ ] no API keys in repo
- [ ] no `.env` committed
- [ ] no private SSH keys committed
- [ ] deployment settings do not expose secrets

## 8. Final Pre-Launch Check

Before sharing publicly:

- [ ] UI looks premium
- [ ] no broken templates
- [ ] pilot loads reliably
- [ ] README clearly says fictional/speculative
- [ ] launch package exists
- [ ] no AI-generated imagery is used
