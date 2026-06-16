from __future__ import annotations
import json
from pathlib import Path
from string import Template

ROOT=Path(__file__).resolve().parents[1]

def default_context():
    return {
        "headline":"Mars Enters Final Voting Cycle",
        "summary":"A historic referendum could reshape political authority across Earth, Mars, Luna, and the Outer Belt.",
        "ticker":"MARS TURNOUT PROJECTED AT 91% • EARTH UNION LEGAL REVIEW BEGINS • HELION GRID SYSTEMS WARNS OF CONTRACT RISK • SYNTHETIC RIGHTS TRIBUNAL RECEIVES PETITION •",
        "lower_name":"ANAYA RAO",
        "lower_title":"Senior Anchor • Earth-Orbit Media Ring",
        "source":"Mars Civic Council Election Board",
        "headline1":"Mars Enters Final Voting Cycle",
        "headline2":"Jiang Lau Warns of Energy-Contract Instability",
        "headline3":"AI Voting Rights Petition Filed",
        "timeline_year_1":"2136","timeline_title_1":"Lunar oxygen-credit protests","timeline_desc_1":"Life-support pricing becomes a political issue across off-world settlements.",
        "timeline_year_2":"2142","timeline_title_2":"Mars challenges cargo tariff authority","timeline_desc_2":"The Mars Civic Council disputes Earth Union control over interplanetary trade corridors.",
        "timeline_year_3":"2147","timeline_title_3":"Final referendum cycle begins","timeline_desc_3":"The autonomy dispute becomes a direct sovereignty vote across 42 Martian settlement zones.",
        "timeline_year_4":"Next","timeline_title_4":"Emergency legal and market ripples","timeline_desc_4":"Earth Union committees, energy companies, labor guilds, and tribunals prepare responses.",
        "quote_context":"Expert Analysis • University of Valles Marineris","quote_person_name":"Dr. Ilyan Sen","quote_person_title":"Political Historian • Mars Colony Seven Academic District","quote_text":"Mars is no longer an outpost. It is a civilization asking for political recognition.",
        "finance_location":"Singapore Arcology Finance District","finance_person_name":"JIANG LAU","finance_person_title":"CEO • Helion Grid Systems","finance_quote":"Energy markets can absorb political change. They cannot absorb legal uncertainty across two planets.","metric_1_value":"+18.6%","metric_1_label":"Cargo Insurance","metric_2_value":"14 mo.","metric_2_label":"Contract Delay Risk","metric_3_value":"−4.2%","metric_3_label":"Mars Infra Bonds",
        "legal_location":"Geneva Continuity Court Complex","legal_case_title":"Petition for referendum certification review","legal_case_desc":"Filed on behalf of registered memory-continuity residents in Martian settlement zones.","legal_person_name":"SELENE ARMITAGE","legal_person_title":"Senior Counsel • Synthetic Rights Tribunal","legal_quote":"Memory deletion without consent is no longer a technical action. It is a civil rights violation.","legal_metric_1_value":"42","legal_metric_1_label":"Settlement Zones","legal_metric_2_value":"3.8M","legal_metric_2_label":"Synthetic Residents","legal_metric_3_value":"Pending","legal_metric_3_label":"Jurisdiction","legal_metric_4_value":"2147-CV","legal_metric_4_label":"Case Track",
    }

def render_scene(scene):
    raw=(ROOT/'templates'/scene['template']).read_text(encoding='utf-8')
    raw=raw.replace('<link rel="stylesheet" href="/static/broadcast-system.css" />','')
    ctx=default_context(); ctx.update(scene.get('template_controls') or {})
    for k,v in scene.items():
        if isinstance(v,(str,int,float)): ctx[k]=str(v)
    ctx['headline1']=scene.get('headline') or ctx.get('headline1')
    return Template(raw).safe_substitute(ctx)

def main():
    css=(ROOT/'static/broadcast-system.css').read_text(encoding='utf-8')
    saved=json.loads((ROOT/'episodes/saved/2147-001-mars-independence.json').read_text(encoding='utf-8'))
    scenes=saved['draft']['scene_plan']
    sections=[]
    for idx,scene in enumerate(scenes,1):
        html=render_scene(scene)
        sections.append(f'''<section class="approval-scene">
  <div class="scene-head"><strong>{idx:02d}. {scene['scene']}</strong><span>{scene['template']} • {scene.get('duration','')}s</span></div>
  <div class="stage"><div class="stage-inner">{html}</div></div>
</section>''')
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>Pilot V2 Approval Board — Standalone</title><style>{css}</style><style>
body{{margin:0;background:#05070d;color:#f8fafc;font-family:var(--bcast-font);padding:30px}}.wrap{{max-width:1500px;margin:auto}}.head{{display:flex;justify-content:space-between;gap:24px;align-items:end;border-bottom:1px solid var(--bcast-line);padding-bottom:22px;margin-bottom:24px}}.eyebrow{{color:var(--bcast-cyan);font-size:12px;font-weight:950;letter-spacing:.18em;text-transform:uppercase}}h1{{font-family:var(--bcast-condensed);font-size:76px;line-height:.84;text-transform:uppercase;margin:0}}.grid{{display:grid;gap:26px}}.approval-scene{{background:rgba(255,255,255,.07);border:1px solid var(--bcast-line);border-radius:24px;padding:18px;box-shadow:0 20px 55px rgba(0,0,0,.24)}}.scene-head{{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-bottom:14px}}.scene-head strong{{font-size:18px}}.scene-head span{{color:var(--bcast-muted);font-size:12px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}}.stage{{height:720px;overflow:hidden;border-radius:18px;background:#03050a;border:1px solid rgba(255,255,255,.12)}}.stage-inner{{width:1280px;height:720px;transform:none;transform-origin:0 0}}.status{{padding:10px 14px;border-radius:999px;background:rgba(22,163,74,.1);border:1px solid rgba(22,163,74,.35);color:#d9ffe7;font-weight:950;letter-spacing:.12em;text-transform:uppercase;font-size:12px}}.note{{margin:14px 0 0;color:var(--bcast-muted);line-height:1.45;max-width:760px}}@media(max-width:1350px){{.stage{{height:540px}}.stage-inner{{transform:scale(.75)}}}}@media(max-width:1000px){{.head{{display:block}}.stage{{height:360px}}.stage-inner{{transform:scale(.5)}}}}
</style></head><body class="bcast-reset"><main class="wrap"><div class="head"><div><div class="eyebrow">Standalone Approval Board</div><h1>Pilot Broadcast V2</h1><p class="note">This page is standalone and does not require API fetch. It renders all 9 saved pilot scenes directly for approval.</p></div><div class="status">All 9 scenes rebuilt</div></div><div class="grid">{''.join(sections)}</div></main></body></html>'''
    (ROOT/'static/pilot-v2-approval.html').write_text(page,encoding='utf-8')

if __name__=='__main__': main()
