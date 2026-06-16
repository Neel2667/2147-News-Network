from __future__ import annotations
import json
import zipfile
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs' / 'final-pilot-render-package'
SCENES_DIR = OUT / 'scenes'
ZIP_PATH = OUT / '2147-001-final-pilot-render-package.zip'
CSS = (ROOT / 'static' / 'broadcast-system.css').read_text(encoding='utf-8')
SAVED = json.loads((ROOT / 'episodes' / 'saved' / '2147-001-mars-independence.json').read_text(encoding='utf-8'))
SCENES = SAVED['draft']['scene_plan']

# Final render pages are 1920x1080, scaling approved 1280x720 compositions by 1.5.
RENDER_W = 1920
RENDER_H = 1080
BASE_W = 1280
BASE_H = 720
SCALE = RENDER_W / BASE_W

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
    'asset_video': '../../../static/demo-assets/earth-observations-sample.mp4',
    'asset_poster': '../../../static/demo-assets/earth-observations-sample-poster.jpg',
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

def normalized_asset_path(value: str) -> str:
    if value.startswith('/static/'):
        return '../../..' + value
    if value.startswith('demo-assets/'):
        return '../../../static/' + value
    if value.startswith('../') or value.startswith('../../'):
        return '../../../static/demo-assets/' + Path(value).name
    return value

def scene_context(scene: dict) -> dict[str, str]:
    ctx = dict(DEFAULTS)
    ctx.update(scene.get('template_controls') or {})
    for k, v in scene.items():
        if isinstance(v, (str, int, float)):
            ctx[k] = str(v)
    ctx['asset_video'] = normalized_asset_path(ctx.get('asset_video', DEFAULTS['asset_video']))
    ctx['asset_poster'] = normalized_asset_path(ctx.get('asset_poster', DEFAULTS['asset_poster']))
    return {k: str(v) for k, v in ctx.items()}

def render_inner(scene: dict) -> str:
    raw = (ROOT / 'templates' / scene['template']).read_text(encoding='utf-8')
    raw = raw.replace('<link rel="stylesheet" href="/static/broadcast-system.css" />', '')
    return Template(raw).safe_substitute(scene_context(scene))

def render_scene_page(scene: dict, index: int, total: int) -> str:
    inner = render_inner(scene)
    title = scene.get('scene', f'Scene {index}')
    duration = int(scene.get('duration', 30))
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{index:02d} — {title} — 2147NN Final Render</title>
  <style>{CSS}</style>
  <style>
    html, body {{ margin:0; width:100%; height:100%; background:#05070d; overflow:hidden; }}
    body {{ display:grid; place-items:center; }}
    .render-viewport {{ width:{RENDER_W}px; height:{RENDER_H}px; overflow:hidden; background:#03050a; position:relative; }}
    .render-scale {{ width:{BASE_W}px; height:{BASE_H}px; transform:scale({SCALE}); transform-origin:0 0; }}
    .render-scale > * {{ width:{BASE_W}px !important; height:{BASE_H}px !important; min-height:{BASE_H}px !important; border-radius:0 !important; }}
    .render-meta {{ position:absolute; left:24px; top:18px; z-index:99999; opacity:.22; color:#dff7ff; background:rgba(0,0,0,.46); border:1px solid rgba(255,255,255,.16); border-radius:999px; padding:8px 12px; font:800 12px/1.2 system-ui; letter-spacing:.08em; text-transform:uppercase; }}
    @media(max-width:{RENDER_W}px) {{ .render-viewport {{ transform:scale(calc(100vw / {RENDER_W})); transform-origin:center; }} }}
    @media(max-height:{RENDER_H}px) {{ .render-viewport {{ transform:scale(min(calc(100vw / {RENDER_W}), calc(100vh / {RENDER_H}))); transform-origin:center; }} }}
  </style>
</head>
<body>
  <main class="render-viewport">
    <div class="render-meta">Scene {index}/{total} • {duration}s • {scene.get('template')}</div>
    <div class="render-scale">{inner}</div>
  </main>
</body>
</html>'''

def write_package() -> None:
    SCENES_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for idx, scene in enumerate(SCENES, 1):
        file_name = f'{idx:02d}-{scene["id"]}.html'
        (SCENES_DIR / file_name).write_text(render_scene_page(scene, idx, len(SCENES)), encoding='utf-8')
        manifest.append({
            'index': idx,
            'id': scene['id'],
            'scene': scene.get('scene'),
            'template': scene.get('template'),
            'duration_seconds': int(scene.get('duration', 30)),
            'file': f'scenes/{file_name}',
        })
    total = sum(x['duration_seconds'] for x in manifest)
    manifest_doc = {
        'episode_id': '2147-001-mars-independence',
        'title': 'Mars Votes for Independence From Earth | 2147 News Network',
        'resolution': {'width': RENDER_W, 'height': RENDER_H},
        'base_composition': {'width': BASE_W, 'height': BASE_H, 'scale': SCALE},
        'total_runtime_seconds': total,
        'scene_count': len(manifest),
        'scenes': manifest,
        'approved_review_page': 'static/pilot-exact-static-review.html',
        'recording_method': 'Open each scene HTML and record with OBS/browser capture at 1920x1080 for duration_seconds.',
    }
    (OUT / 'manifest.json').write_text(json.dumps(manifest_doc, indent=2, ensure_ascii=False), encoding='utf-8')
    readme = f'''# Final Pilot Render Package — 2147-001

This package contains the final approved HTML scene pages for recording the pilot.

## Resolution

```text
{RENDER_W}x{RENDER_H}
```

## Runtime

```text
{total} seconds
```

## How to record

1. Open `index.html` to review the scene list.
2. Open each file in `scenes/` one by one.
3. Record each scene at 1920x1080 using OBS/browser capture.
4. Use `manifest.json` for scene durations.
5. Assemble clips in a video editor.
6. Add voiceover, sound design, music, and subtitles.

## Important

This package uses actual approved HTML templates, not the rough procedural MP4 preview.
'''
    (OUT / 'README.md').write_text(readme, encoding='utf-8')
    cards = []
    for item in manifest:
        cards.append(f'''
        <article class="card">
          <div><strong>{item['index']:02d}. {item['scene']}</strong><span>{item['duration_seconds']}s • {item['template']}</span></div>
          <a href="{item['file']}" target="_blank">Open Render Scene</a>
        </article>''')
    index = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>Final Pilot Render Package</title>
<style>
body{{margin:0;background:#05070d;color:#f8fafc;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;padding:30px}}.wrap{{max-width:1100px;margin:auto}}.top{{border-bottom:1px solid rgba(255,255,255,.14);padding-bottom:22px;margin-bottom:24px}}.eyebrow{{color:#00a6d6;font-size:12px;font-weight:950;letter-spacing:.18em;text-transform:uppercase}}h1{{font-family:"Arial Narrow",Impact,sans-serif;font-size:72px;line-height:.84;text-transform:uppercase;margin:0}}p{{color:#94a3b8;line-height:1.45}}.card{{display:flex;justify-content:space-between;gap:18px;align-items:center;margin:0 0 12px;padding:16px;border:1px solid rgba(255,255,255,.14);border-radius:18px;background:rgba(255,255,255,.06)}}.card strong{{display:block}}.card span{{display:block;color:#94a3b8;font-size:12px;font-weight:800;margin-top:5px}}a{{color:#dff7ff;text-decoration:none;font-weight:900;border:1px solid rgba(0,166,214,.3);padding:10px 12px;border-radius:999px;background:rgba(0,166,214,.08)}}.download{{display:inline-block;margin-top:12px}}
</style></head><body><main class="wrap"><header class="top"><div class="eyebrow">Final Render Package</div><h1>2147 Pilot Scenes</h1><p>Open each render scene and record at 1920x1080. Total runtime: {total} seconds. These are generated from the approved exact HTML templates.</p><a class="download" href="2147-001-final-pilot-render-package.zip">Download ZIP Package</a></header>{''.join(cards)}</main></body></html>'''
    (OUT / 'index.html').write_text(index, encoding='utf-8')

def zip_package() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in OUT.rglob('*'):
            if path == ZIP_PATH or path.is_dir():
                continue
            zf.write(path, path.relative_to(OUT))

def main() -> None:
    write_package()
    zip_package()
    print('wrote', OUT)
    print('zip', ZIP_PATH)

if __name__ == '__main__':
    main()
