from __future__ import annotations
import json
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'static' / 'pilot-exact-static-review.html'
CSS = (ROOT / 'static' / 'broadcast-system.css').read_text(encoding='utf-8')
SAVED = json.loads((ROOT / 'episodes/saved/2147-001-mars-independence.json').read_text(encoding='utf-8'))
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
    'asset_video': 'demo-assets/earth-observations-sample.mp4',
    'asset_poster': 'demo-assets/earth-observations-sample-poster.jpg',
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

def ctx_for(scene: dict) -> dict[str, str]:
    ctx = dict(DEFAULTS)
    ctx.update(scene.get('template_controls') or {})
    for k, v in scene.items():
        if isinstance(v, (str, int, float)):
            ctx[k] = str(v)
    # This page lives in /static, so demo-assets/... is the correct relative path.
    for key in ['asset_video', 'asset_poster']:
        val = ctx.get(key, '')
        if val.startswith('/static/'):
            ctx[key] = val.replace('/static/', '')
        elif val.startswith('../') or val.startswith('../../'):
            ctx[key] = 'demo-assets/' + Path(val).name
    return {k: str(v) for k, v in ctx.items()}

def render_scene(scene: dict) -> str:
    raw = (ROOT / 'templates' / scene['template']).read_text(encoding='utf-8')
    raw = raw.replace('<link rel="stylesheet" href="/static/broadcast-system.css" />', '')
    return Template(raw).safe_substitute(ctx_for(scene))

def main() -> None:
    sections = []
    for i, scene in enumerate(SCENES, 1):
        sections.append(f'''
<section class="review-scene">
  <div class="scene-head"><strong>{i:02d}. {scene.get('scene')}</strong><span>{scene.get('template')} • {scene.get('duration')}s</span></div>
  <div class="scene-stage"><div class="scene-scale">{render_scene(scene)}</div></div>
</section>
''')
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>2147 Pilot Exact Static Review</title>
  <style>{CSS}</style>
  <style>
    body{{margin:0;background:#05070d;color:#f8fafc;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;padding:30px}}
    .wrap{{max-width:1500px;margin:auto}}
    .top{{border-bottom:1px solid rgba(255,255,255,.14);padding-bottom:22px;margin-bottom:24px}}
    .eyebrow{{color:#00a6d6;font-size:12px;font-weight:950;letter-spacing:.18em;text-transform:uppercase}}
    h1{{font-family:"Arial Narrow",Impact,sans-serif;font-size:76px;line-height:.84;text-transform:uppercase;margin:0}}
    .note{{max-width:820px;color:#94a3b8;line-height:1.45}}
    .warning{{display:inline-block;margin-top:14px;padding:12px 14px;border-radius:14px;background:rgba(22,163,74,.10);border:1px solid rgba(22,163,74,.35);color:#bbf7d0;font-weight:900}}
    .review-scene{{margin:0 0 28px;padding:18px;border:1px solid rgba(255,255,255,.14);border-radius:24px;background:rgba(255,255,255,.06);box-shadow:0 20px 55px rgba(0,0,0,.24)}}
    .scene-head{{display:flex;justify-content:space-between;gap:18px;margin-bottom:14px;align-items:center}}
    .scene-head strong{{font-size:18px}}
    .scene-head span{{color:#94a3b8;font-size:12px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}}
    .scene-stage{{width:1280px;height:720px;max-width:100%;overflow:hidden;border-radius:18px;background:#03050a;border:1px solid rgba(255,255,255,.12)}}
    .scene-scale{{width:1280px;height:720px;transform-origin:0 0}}
    .scene-scale > *{{width:1280px !important;height:720px !important;min-height:720px !important;border-radius:0 !important}}
    @media(max-width:1350px){{.scene-stage{{width:960px;height:540px}}.scene-scale{{transform:scale(.75)}}}}
    @media(max-width:980px){{body{{padding:18px}}h1{{font-size:52px}}.scene-head{{display:block}}.scene-stage{{width:640px;height:360px}}.scene-scale{{transform:scale(.5)}}}}
  </style>
</head>
<body>
  <main class="wrap">
    <header class="top">
      <div class="eyebrow">Static exact template review</div>
      <h1>Pilot Scenes</h1>
      <p class="note">This page is fully standalone inside <code>/static</code>. It does not use API calls or iframes, so it should load in preview. It renders the actual HTML templates inline.</p>
      <div class="warning">Use this page for visual approval — not the old generated MP4.</div>
    </header>
    {''.join(sections)}
  </main>
</body>
</html>'''
    OUT.write_text(html, encoding='utf-8')
    print('wrote', OUT)

if __name__ == '__main__':
    main()
