"""Small HTML template loader for Gradio previews.

The templates are self-contained HTML snippets with inline CSS so they render
inside Hugging Face/Gradio previews without external network access.
"""
from __future__ import annotations

from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates"


def render_template(name: str, **context: str) -> str:
    path = TEMPLATE_DIR / name
    if not path.exists():
        return f"<div style='padding:24px;color:white;background:#050914'>Template not found: {name}</div>"
    raw = path.read_text(encoding="utf-8")
    return Template(raw).safe_substitute(**{k: str(v) for k, v in context.items()})


def available_templates() -> list[str]:
    return sorted(p.name for p in TEMPLATE_DIR.glob("*.html"))
