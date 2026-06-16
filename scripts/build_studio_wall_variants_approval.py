from __future__ import annotations
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / 'static/broadcast-system.css').read_text(encoding='utf-8')

BASE_CTX = {
    'asset_video': 'demo-assets/earth-observations-sample.mp4',
    'asset_poster': 'demo-assets/earth-observations-sample-poster.jpg',
    'live_label': 'Live',
    'timestamp': '18 Oct 2147 / 19:42 UTC-O',
    'segment_label': 'Mars Political Desk',
    'headline': 'Mars Enters Final Voting Cycle',
    'summary': 'A sovereignty referendum across 42 Martian settlement zones could create the first independent off-world republic.',
    'source': 'NASA public domain sample',
    'wall_metric_value': '91%',
    'wall_metric_label': 'Projected Turnout',
    'lower_role': 'Anchor',
    'lower_name': 'ANAYA RAO',
    'lower_title': 'Senior Anchor • Earth-Orbit Media Ring',
    'lower_location': 'Studio',
    'ticker_label': 'Headlines',
    'ticker': 'MARS TURNOUT PROJECTED AT 91% • EARTH UNION LEGAL REVIEW BEGINS • HELION GRID WARNING •',
    'headline1': 'Mars Enters Final Voting Cycle',
    'headline2': 'Jiang Lau Warns of Energy-Contract Instability',
    'headline3': 'AI Voting Rights Petition Filed',
    'metric_1_value': '+18.6%',
    'metric_1_label': 'Cargo Insurance',
    'metric_2_value': '14 mo.',
    'metric_2_label': 'Contract Risk',
    'metric_3_value': '−4.2%',
    'metric_3_label': 'Mars Bonds',
    'quote_context': 'Expert Analysis • University of Valles Marineris',
    'quote_person_name': 'Dr. Ilyan Sen',
    'quote_person_title': 'Political Historian • University of Valles Marineris',
    'quote_text': 'Mars is no longer an outpost. It is a civilization asking for political recognition.',
    'archive_label': 'Archive Feed',
    'archive_year': '2136',
    'archive_metric_label': 'Timeline Archive',
}

VARIANTS = [
    {
        'name': 'Footage Wall',
        'template': 'broadcast-v2-studio-wall-footage.html',
        'description': 'Primary approved style for stock footage and B-roll reports.',
        'ctx': {
            'segment_label': 'Mars Political Desk',
            'headline': 'Mars Enters Final Voting Cycle',
            'wall_metric_value': '91%',
            'wall_metric_label': 'Projected Turnout',
        },
    },
    {
        'name': 'Map Wall',
        'template': 'broadcast-v2-studio-wall-map.html',
        'description': 'For Earth-Mars routes, Mars zones, Lunar mining belts and climate paths.',
        'ctx': {
            'segment_label': 'Route Analysis',
            'headline': 'Earth–Mars Corridor Under Review',
            'summary': 'Cargo insurance and treaty risk now affect long-range infrastructure contracts.',
            'source': 'Outer Belt Trade Registry',
            'ticker_label': 'Map',
            'ticker': 'EARTH-MARS CORRIDOR • CERES CARGO DELAYS • MARS INFRA BONDS −4.2% •',
        },
    },
    {
        'name': 'Data Wall',
        'template': 'broadcast-v2-studio-wall-data.html',
        'description': 'For vote models, market numbers, legal case metrics and telemetry.',
        'ctx': {
            'segment_label': 'Referendum Data Board',
            'headline': 'Independence Model Leads',
            'ticker_label': 'Data',
            'ticker': 'INDEPENDENCE 57% • UNION 39% • UNDECIDED 4% • TURNOUT 91% •',
        },
    },
    {
        'name': 'Quote Wall',
        'template': 'broadcast-v2-studio-wall-quote.html',
        'description': 'For expert analysis, official statements and strong quote moments.',
        'ctx': {
            'segment_label': 'Expert Analysis',
            'headline': 'Dr. Ilyan Sen',
            'lower_role': 'Expert',
            'lower_name': 'ANAYA RAO',
            'lower_title': 'Senior Anchor • Earth-Orbit Media Ring',
            'ticker_label': 'Analysis',
            'ticker': 'UNIVERSITY OF VALLES MARINERIS • ARCHIVE FEED VERIFIED •',
        },
    },
    {
        'name': 'Archive Wall',
        'template': 'broadcast-v2-studio-wall-archive.html',
        'description': 'For historical context footage and causal backstory segments.',
        'ctx': {
            'archive_label': 'Archive Feed',
            'headline': 'Why This Vote Exists',
            'summary': 'The Mars referendum follows oxygen-credit protests, tariff disputes and settlement autonomy demands.',
            'archive_year': '2136',
            'archive_metric_label': 'Timeline Archive',
            'source': '2147NN Timeline Archive',
            'ticker_label': 'Archive',
            'ticker': '2136 OXYGEN-CREDIT PROTESTS • 2142 CARGO TARIFF DISPUTE • 2147 REFERENDUM •',
        },
    },
]

def render_template(template_name: str, ctx: dict[str, str]) -> str:
    raw = (ROOT / 'templates' / template_name).read_text(encoding='utf-8')
    raw = raw.replace('<link rel="stylesheet" href="/static/broadcast-system.css" />', '')
    final = dict(BASE_CTX)
    final.update(ctx)
    return Template(raw).safe_substitute(final)

def main() -> None:
    sections = []
    for i, variant in enumerate(VARIANTS, 1):
        html = render_template(variant['template'], variant['ctx'])
        sections.append(f'''
        <section class="variant">
          <div class="variant-head">
            <div><div class="eyebrow">Variant {i:02d}</div><h2>{variant['name']}</h2></div>
            <p>{variant['description']}</p>
          </div>
          <div class="stage"><div class="stage-inner">{html}</div></div>
        </section>
        ''')

    page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Studio Wall Variants Approval</title>
  <style>{CSS}</style>
  <style>
    body {{ margin:0; background:#05070d; color:#f8fafc; font-family:var(--bcast-font); padding:30px; }}
    .wrap {{ max-width:1500px; margin:auto; }}
    .top {{ display:flex; justify-content:space-between; gap:26px; align-items:end; border-bottom:1px solid var(--bcast-line); padding-bottom:24px; margin-bottom:28px; }}
    .eyebrow {{ color:var(--bcast-cyan); font-size:12px; font-weight:950; letter-spacing:.18em; text-transform:uppercase; }}
    h1 {{ font-family:var(--bcast-condensed); font-size:clamp(54px,7vw,96px); line-height:.84; text-transform:uppercase; margin:0; }}
    .top p {{ max-width:620px; color:var(--bcast-muted); line-height:1.45; margin:0; }}
    .variant {{ margin:0 0 34px; padding:18px; border:1px solid var(--bcast-line); border-radius:26px; background:rgba(255,255,255,.065); box-shadow:0 24px 70px rgba(0,0,0,.26); }}
    .variant-head {{ display:flex; align-items:end; justify-content:space-between; gap:18px; margin-bottom:14px; }}
    .variant-head h2 {{ font-family:var(--bcast-condensed); font-size:42px; line-height:.88; text-transform:uppercase; margin:0; }}
    .variant-head p {{ max-width:620px; color:var(--bcast-muted); font-size:14px; line-height:1.38; margin:0; }}
    .stage {{ width:1280px; height:720px; max-width:100%; overflow:hidden; border-radius:22px; background:#03050a; border:1px solid rgba(255,255,255,.14); }}
    .stage-inner {{ width:1280px; height:720px; transform-origin:0 0; }}
    .decision {{ padding:18px; border-radius:18px; background:rgba(0,166,214,.08); border:1px solid rgba(0,166,214,.26); color:#dff7ff; line-height:1.5; }}
    @media(max-width:1350px) {{ .stage {{ width:960px; height:540px; }} .stage-inner {{ transform:scale(.75); }} }}
    @media(max-width:980px) {{ .top,.variant-head {{ display:block; }} .stage {{ width:640px; height:360px; }} .stage-inner {{ transform:scale(.5); }} }}
  </style>
</head>
<body>
  <main class="wrap">
    <header class="top">
      <div><div class="eyebrow">Approval Board</div><h1>Studio Wall Variants</h1></div>
      <p>These are the five reusable Studio + Video Wall variants built from the approved direction. Review them before we update the pilot scenes and asset workflow.</p>
    </header>
    {''.join(sections)}
    <div class="decision"><b>Approval request:</b> confirm which variants are acceptable, and tell me if any specific variant needs layout/spacing/color changes.</div>
  </main>
</body>
</html>'''
    (ROOT / 'static/studio-wall-variants-approval.html').write_text(page, encoding='utf-8')

if __name__ == '__main__':
    main()
