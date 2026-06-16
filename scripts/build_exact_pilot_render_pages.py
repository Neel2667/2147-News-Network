from __future__ import annotations
import json
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs' / 'pilot-exact-render'
SCENES_DIR = OUT / 'scenes'

BROADCAST_CSS = (ROOT / 'static' / 'broadcast-system.css').read_text(encoding='utf-8')
SAVED = json.loads((ROOT / 'episodes' / 'saved' / '2147-001-mars-independence.json').read_text(encoding='utf-8'))
SCENES = SAVED['draft']['scene_plan']

DEFAULTS = {
    'headline': 'Mars Enters Final Voting Cycle',
    'summary': 'A historic referendum could reshape political authority across Earth, Mars, Luna, and the Outer Belt.',
    'ticker': 'MARS TURNOUT PROJECTED AT 91% • EARTH UNION LEGAL REVIEW BEGINS • HELION GRID SYSTEMS WARNS OF CONTRACT RISK •',
    'lower_name': 'ANAYA RAO',
    'lower_title': 'Senior Anchor • Earth-Orbit Media Ring',
    'lower_role': 'Anchor',
    'lower_location': 'Studio',
    'source': 'Mars Civic Council Election Board',
    'timestamp': '18 Oct 2147 / 19:42 UTC-O',
    'live_label': 'Live',
    'ticker_label': 'Headlines',
    'segment_label': 'Mars Political Desk',
    'asset_video': '../../static/demo-assets/earth-observations-sample.mp4',
    'asset_poster': '../../static/demo-assets/earth-observations-sample-poster.jpg',
    'wall_metric_value': '91%',
    'wall_metric_label': 'Projected Turnout',
    'headline1': 'Mars Enters Final Voting Cycle',
    'headline2': 'Jiang Lau Warns of Energy-Contract Instability',
    'headline3': 'AI Voting Rights Petition Filed',
    'timeline_year_1': '2136',
    'timeline_title_1': 'Lunar oxygen-credit protests',
    'timeline_desc_1': 'Life-support pricing becomes a political issue across off-world settlements.',
    'timeline_year_2': '2142',
    'timeline_title_2': 'Mars challenges cargo tariff authority',
    'timeline_desc_2': 'The Mars Civic Council disputes Earth Union control over interplanetary trade corridors.',
    'timeline_year_3': '2147',
    'timeline_title_3': 'Final referendum cycle begins',
    'timeline_desc_3': 'The autonomy dispute becomes a direct sovereignty vote across 42 Martian settlement zones.',
    'timeline_year_4': 'Next',
    'timeline_title_4': 'Emergency legal and market ripples',
    'timeline_desc_4': 'Earth Union committees, energy companies, labor guilds, and tribunals prepare responses.',
    'quote_context': 'Expert Analysis • University of Valles Marineris',
    'quote_person_name': 'Dr. Ilyan Sen',
    'quote_person_title': 'Political Historian • University of Valles Marineris',
    'quote_text': 'Mars is no longer an outpost. It is a civilization asking for political recognition.',
    'metric_1_value': '+18.6%',
    'metric_1_label': 'Cargo Insurance',
    'metric_2_value': '14 mo.',
    'metric_2_label': 'Contract Risk',
    'metric_3_value': '−4.2%',
    'metric_3_label': 'Mars Bonds',
    'archive_label': 'Archive Feed',
    'archive_year': '2136',
    'archive_metric_label': 'Timeline Archive',
}

def scene_context(scene: dict) -> dict[str, str]:
    ctx = dict(DEFAULTS)
    ctx.update(scene.get('template_controls') or {})
    for k, v in scene.items():
        if isinstance(v, (str, int, float)):
            ctx[k] = str(v)
    # Force paths for standalone output pages.
    if ctx.get('asset_video', '').startswith('/static/'):
        ctx['asset_video'] = '../..' + ctx['asset_video']
    elif ctx.get('asset_video', '').startswith('demo-assets/'):
        ctx['asset_video'] = '../../static/' + ctx['asset_video']
    if ctx.get('asset_poster', '').startswith('/static/'):
        ctx['asset_poster'] = '../..' + ctx['asset_poster']
    elif ctx.get('asset_poster', '').startswith('demo-assets/'):
        ctx['asset_poster'] = '../../static/' + ctx['asset_poster']
    return {k: str(v) for k, v in ctx.items()}

def render_scene(scene: dict, idx: int) -> str:
    raw = (ROOT / 'templates' / scene['template']).read_text(encoding='utf-8')
    raw = raw.replace('<link rel="stylesheet" href="/static/broadcast-system.css" />', '')
    inner = Template(raw).safe_substitute(scene_context(scene))
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{idx:02d} — {scene.get('scene','Scene')}</title>
  <style>{BROADCAST_CSS}</style>
  <style>
    html, body {{ margin:0; width:100%; height:100%; background:#05070d; overflow:hidden; }}
    body {{ display:grid; place-items:center; }}
    .render-frame {{ width:1280px; height:720px; overflow:hidden; background:#03050a; }}
    .render-frame > * {{ width:1280px !important; height:720px !important; min-height:720px !important; }}
  </style>
</head>
<body>
  <main class="render-frame">{inner}</main>
</body>
</html>'''

def main() -> None:
    SCENES_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for idx, scene in enumerate(SCENES, 1):
        name = f'{idx:02d}-{scene["id"]}.html'
        (SCENES_DIR / name).write_text(render_scene(scene, idx), encoding='utf-8')
        manifest.append({
            'index': idx,
            'id': scene['id'],
            'scene': scene.get('scene'),
            'template': scene.get('template'),
            'duration': scene.get('duration'),
            'file': f'scenes/{name}',
        })
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    cards = []
    for item in manifest:
        cards.append(f'''
          <section class="scene-card">
            <div class="scene-head"><strong>{item['index']:02d}. {item['scene']}</strong><span>{item['template']} • {item['duration']}s</span></div>
            <iframe src="{item['file']}" loading="lazy"></iframe>
          </section>''')
    index = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>Exact Pilot Render Pages</title>
<style>
body{{margin:0;background:#05070d;color:#f8fafc;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;padding:30px}}.wrap{{max-width:1500px;margin:auto}}.top{{border-bottom:1px solid rgba(255,255,255,.14);padding-bottom:22px;margin-bottom:24px}}.eyebrow{{color:#00a6d6;font-size:12px;font-weight:950;letter-spacing:.18em;text-transform:uppercase}}h1{{font-family:"Arial Narrow",Impact,sans-serif;font-size:76px;line-height:.84;text-transform:uppercase;margin:0}}p{{color:#94a3b8;line-height:1.45}}.scene-card{{margin:0 0 28px;padding:18px;border:1px solid rgba(255,255,255,.14);border-radius:24px;background:rgba(255,255,255,.06)}}.scene-head{{display:flex;justify-content:space-between;gap:18px;margin-bottom:14px}}.scene-head span{{color:#94a3b8;font-size:12px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}}iframe{{width:1280px;height:720px;max-width:100%;border:0;border-radius:18px;background:#03050a}}.warning{{padding:14px 16px;border-radius:14px;background:rgba(215,25,32,.10);border:1px solid rgba(215,25,32,.28);color:#fecaca;margin:18px 0}}
</style></head><body><main class="wrap"><div class="top"><div class="eyebrow">Exact HTML Template Render</div><h1>Pilot Scenes</h1><p>These pages render the actual HTML templates. This is the source of truth. The earlier generated MP4 was a rough procedural approximation and should not be used for quality approval.</p><div class="warning">Approve these HTML scene renders, not the old generated MP4.</div></div>{''.join(cards)}</main></body></html>'''
    (OUT / 'index.html').write_text(index, encoding='utf-8')
    print('wrote', OUT / 'index.html')

if __name__ == '__main__':
    main()
