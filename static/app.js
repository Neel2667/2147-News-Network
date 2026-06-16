const state = { world: null, selectedEventId: null, currentDraft: null, templates: [], selectedSceneIndex: 0 };
const $ = (id) => document.getElementById(id);

function switchPanel(id){
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.toggle('active', b.dataset.panel===id));
  document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('active', p.id===id));
}

document.querySelectorAll('.nav-btn').forEach(btn => btn.addEventListener('click', () => switchPanel(btn.dataset.panel)));

async function api(path, options={}){
  const res = await fetch(path, { headers: {'Content-Type':'application/json'}, ...options });
  if(!res.ok) throw new Error(await res.text());
  return res.headers.get('content-type')?.includes('application/json') ? res.json() : res.text();
}

function metric(label, value){ return `<div class="metric"><b>${value}</b><span>${label}</span></div>`; }

async function loadWorld(){
  const world = await api('/api/world');
  state.world = world;
  const c = world.counts;
  $('metricGrid').innerHTML = [
    metric('Active Events', c.active_events), metric('Archived Events', c.archived_events), metric('People', c.people),
    metric('Organizations', c.organizations), metric('Locations', c.locations), metric('Ripple Seeds', c.ripple_seeds)
  ].join('');

  $('activeEvents').innerHTML = world.events.filter(e=>e.status==='active').map(e=>`
    <div class="event-item"><strong>${e.title}</strong><span>${e.date} / ${e.time}<br>${e.summary}</span></div>`).join('') || '<p>No active events.</p>';

  $('sourceList').innerHTML = world.sources.map(s=>`
    <div class="source-item"><strong>${s.name}</strong><span>${s.trust_level}<br>Used for: ${(s.used_for||[]).join(', ')}</span></div>`).join('');

  const eventSelect = $('eventSelect');
  eventSelect.innerHTML = world.events.map(e=>`<option value="${e.id}">${e.title}</option>`).join('');
  const active = world.events.find(e=>e.status==='active') || world.events[0];
  if(active){ eventSelect.value = active.id; state.selectedEventId = active.id; }
}

async function loadTemplates(){
  const data = await api('/api/templates');
  state.templates = data.templates;
  const options = data.templates.map(t=>`<option value="${t}">${t}</option>`).join('');
  $('templateSelect').innerHTML = options;
  $('sceneTemplateInput').innerHTML = options;
  if(data.templates.includes('opening-intro-premium.html')) $('templateSelect').value = 'opening-intro-premium.html';
  renderTemplate();
}

async function analyzeEvent(){
  const id = $('eventSelect').value;
  state.selectedEventId = id;
  const data = await api(`/api/events/${id}/analysis`);
  const e = data.event;
  $('analysisOutput').innerHTML = `
    <div class="event-item"><strong>${e.title}</strong><span>${e.summary}</span></div>
    <div class="event-item"><strong>Score</strong><span>${data.score} newsroom priority points</span></div>
    <div class="event-item"><strong>Location</strong><span>${data.location.name}</span></div>
    <h3>Causes</h3>
    ${data.causes.map(c=>`<div class="event-item"><strong>${c.title}</strong><span>${c.date || ''}</span></div>`).join('') || '<p>No causes recorded.</p>'}
    <h3>Affected Actors</h3>
    ${data.actors.map(a=>`<div class="actor-item"><strong>${a.name}</strong><span>${a.role || a.type || ''} ${a.organization ? '• '+a.organization : ''}</span></div>`).join('')}
  `;
  $('rippleOutput').innerHTML = (e.ripple_seeds||[]).map(r=>`
    <div class="ripple-item"><strong>${r.type}</strong><span>Probability ${r.probability} • +${r.delay_days} days<br>${r.description}</span></div>`).join('') || '<p>No ripple seeds.</p>';
}

async function generateEpisode(){
  const data = await api('/api/episode/generate', { method:'POST', body: JSON.stringify({
    event_id: $('eventSelect').value,
    manual_topic: $('manualTopic').value,
    target_length: $('targetLength').value,
    tone: $('tone').value
  })});
  state.currentDraft = data;
  state.selectedSceneIndex = 0;
  $('headlineOutput').innerHTML = data.headlines.map(h=>`<li>${h}</li>`).join('');
  $('scriptOutput').textContent = data.script;
  $('sceneOutput').textContent = JSON.stringify(data.scene_plan, null, 2);
  renderSceneTimeline();
  loadSelectedSceneControls();
  previewSelectedScene();
}

async function renderTemplate(){
  const html = await api('/api/templates/preview', { method:'POST', body: JSON.stringify({
    template_name: $('templateSelect').value,
    headline: $('previewHeadline').value,
    summary: 'A historic referendum could reshape political authority across Earth, Mars, Luna, and the Outer Belt.'
  })});
  $('templateStage').innerHTML = html;
}


function formatRuntime(totalSeconds){
  const m = Math.floor(totalSeconds/60);
  const sec = String(totalSeconds%60).padStart(2,'0');
  return `${m}:${sec}`;
}

function currentScenes(){
  if(!state.currentDraft) state.currentDraft = { scene_plan: [] };
  if(!Array.isArray(state.currentDraft.scene_plan)) state.currentDraft.scene_plan = [];
  return state.currentDraft.scene_plan;
}

function sceneLabel(scene, index){
  return scene.scene || scene.name || `Scene ${index+1}`;
}

const templateSpecificSchemas = {
  'historical-timeline.html': [
    ['control-subtitle','Timeline Event 1'], ['timeline_year_1','Year 1'], ['timeline_title_1','Title 1'], ['timeline_desc_1','Description 1','textarea','wide-field'],
    ['control-subtitle','Timeline Event 2'], ['timeline_year_2','Year 2'], ['timeline_title_2','Title 2'], ['timeline_desc_2','Description 2','textarea','wide-field'],
    ['control-subtitle','Timeline Event 3'], ['timeline_year_3','Year 3'], ['timeline_title_3','Title 3'], ['timeline_desc_3','Description 3','textarea','wide-field'],
    ['control-subtitle','Timeline Event 4'], ['timeline_year_4','Year 4'], ['timeline_title_4','Title 4'], ['timeline_desc_4','Description 4','textarea','wide-field']
  ],
  'financial-desk.html': [
    ['finance_person_name','Person Name'], ['finance_person_title','Person Title'], ['finance_quote','Quote','textarea','wide-field'],
    ['control-subtitle','Metric Cards'], ['metric_1_value','Metric 1 Value'], ['metric_1_label','Metric 1 Label'], ['metric_2_value','Metric 2 Value'], ['metric_2_label','Metric 2 Label'], ['metric_3_value','Metric 3 Value'], ['metric_3_label','Metric 3 Label'],
    ['finance_location','Finance Location']
  ],
  'legal-desk.html': [
    ['legal_case_title','Case/Filing Title'], ['legal_case_desc','Case Description','textarea','wide-field'],
    ['legal_person_name','Legal Expert Name'], ['legal_person_title','Legal Expert Title'], ['legal_quote','Legal Quote','textarea','wide-field'],
    ['control-subtitle','Case Metrics'], ['legal_metric_1_value','Metric 1 Value'], ['legal_metric_1_label','Metric 1 Label'], ['legal_metric_2_value','Metric 2 Value'], ['legal_metric_2_label','Metric 2 Label'], ['legal_metric_3_value','Metric 3 Value'], ['legal_metric_3_label','Metric 3 Label'], ['legal_metric_4_value','Metric 4 Value'], ['legal_metric_4_label','Metric 4 Label'],
    ['legal_location','Legal Location']
  ],
  'breaking-news.html': [
    ['breaking_status','Status'], ['breaking_time','Time'], ['breaking_impact','Impact Level'], ['breaking_verification','Verification Desk']
  ],
  'science-desk.html': [
    ['science_mission','Mission / Consortium'], ['science_signal_status','Signal Status'], ['science_instrument','Instrument'], ['science_depth','Depth'], ['science_review_stage','Review Stage'], ['science_signal_count','Confirmed Repeats'], ['science_location','Science Location']
  ],
  'earth-climate-map.html': [
    ['climate_region','Climate Region'], ['control-subtitle','Climate Metrics'], ['climate_metric_1_value','Metric 1 Value'], ['climate_metric_1_label','Metric 1 Label'], ['climate_metric_2_value','Metric 2 Value'], ['climate_metric_2_label','Metric 2 Label'], ['climate_metric_3_value','Metric 3 Value'], ['climate_metric_3_label','Metric 3 Label'], ['climate_metric_4_value','Metric 4 Value'], ['climate_metric_4_label','Metric 4 Label']
  ],
  'lunar-report.html': [
    ['lunar_region','Lunar Region'], ['lunar_location','Lunar Location'], ['lunar_person_name','Person Name'], ['lunar_person_title','Person Title'], ['control-subtitle','Lunar Metrics'], ['lunar_metric_1_value','Metric 1 Value'], ['lunar_metric_1_label','Metric 1 Label'], ['lunar_metric_2_value','Metric 2 Value'], ['lunar_metric_2_label','Metric 2 Label'], ['lunar_metric_3_value','Metric 3 Value'], ['lunar_metric_3_label','Metric 3 Label'], ['lunar_metric_4_value','Metric 4 Value'], ['lunar_metric_4_label','Metric 4 Label']
  ]
};

const templateSpecificDefaults = {
  timeline_year_1:'2136', timeline_title_1:'Lunar oxygen-credit protests', timeline_desc_1:'Life-support pricing becomes a political issue across off-world settlements.',
  timeline_year_2:'2142', timeline_title_2:'Mars challenges cargo tariff authority', timeline_desc_2:'The Mars Civic Council disputes Earth Union control over interplanetary trade corridors.',
  timeline_year_3:'2147', timeline_title_3:'Final referendum cycle begins', timeline_desc_3:'The autonomy dispute becomes a direct sovereignty vote across 42 Martian settlement zones.',
  timeline_year_4:'Next', timeline_title_4:'Emergency legal and market ripples', timeline_desc_4:'Earth Union committees, energy companies, labor guilds, and tribunals prepare responses.',
  finance_person_name:'JIANG LAU', finance_person_title:'CEO • Helion Grid Systems', finance_quote:'Energy markets can absorb political change. They cannot absorb legal uncertainty across two planets.',
  metric_1_value:'+18.6%', metric_1_label:'Cargo Insurance', metric_2_value:'14 mo.', metric_2_label:'Contract Delay Risk', metric_3_value:'−4.2%', metric_3_label:'Mars Infra Bonds', finance_location:'Singapore Arcology Finance District',
  legal_case_title:'Petition for referendum certification review', legal_case_desc:'Filed on behalf of registered memory-continuity residents in Martian settlement zones.', legal_person_name:'SELENE ARMITAGE', legal_person_title:'Senior Counsel • Synthetic Rights Tribunal', legal_quote:'Memory deletion without consent is no longer a technical action. It is a civil rights violation.',
  legal_metric_1_value:'42', legal_metric_1_label:'Settlement Zones', legal_metric_2_value:'3.8M', legal_metric_2_label:'Synthetic Residents', legal_metric_3_value:'Pending', legal_metric_3_label:'Jurisdiction', legal_metric_4_value:'2147-CV', legal_metric_4_label:'Case Track', legal_location:'Geneva Continuity Court Complex',
  breaking_status:'LIVE', breaking_time:'19:42', breaking_impact:'High', breaking_verification:'2147NN Editorial Desk',
  science_mission:'Europa Oceanic Research Consortium', science_signal_status:'Repeating acoustic pattern', science_instrument:'Cryo-hydrophone array K-4', science_depth:'18.6 km beneath ice', science_review_stage:'Independent verification', science_signal_count:'3', science_location:'Europa Research Base K-4',
  climate_region:'Pacific Floating City Cluster 12', climate_metric_1_value:'72 hrs', climate_metric_1_label:'Shield Window', climate_metric_2_value:'Category 6', climate_metric_2_label:'Storm Model', climate_metric_3_value:'18.4M', climate_metric_3_label:'Residents Covered', climate_metric_4_value:'94%', climate_metric_4_label:'Grid Readiness',
  lunar_region:'Lunar South Pole Mining Belt', lunar_location:'Shackleton Habitat Cluster', lunar_metric_1_value:'+22%', lunar_metric_1_label:'Oxygen Credit Cost', lunar_metric_2_value:'9 days', lunar_metric_2_label:'Strike Duration', lunar_metric_3_value:'31 sites', lunar_metric_3_label:'Affected Mines', lunar_metric_4_value:'4.2M t', lunar_metric_4_label:'Helium-3 Delayed', lunar_person_name:'TARO VENN', lunar_person_title:'Lunar Labor Analyst • Shackleton Habitat Cluster'
};

function renderTemplateSpecificControls(scene){
  const template = $('sceneTemplateInput').value;
  const schema = templateSpecificSchemas[template] || [];
  const wrap = $('templateSpecificControls');
  $('specificTemplateLabel').textContent = schema.length ? template : 'No specialized controls';
  wrap.classList.toggle('two', schema.length > 0);
  if(!schema.length){ wrap.innerHTML = '<p style="margin:0;color:var(--muted);font-size:13px;line-height:1.4">This template uses the standard headline, summary, lower-third, ticker, and source controls.</p>'; return; }
  const controls = scene.template_controls || {};
  wrap.innerHTML = schema.map(field => {
    if(field[0] === 'control-subtitle') return `<div class="control-subtitle">${field[1]}</div>`;
    const [key,label,type='input',klass=''] = field;
    const value = controls[key] ?? templateSpecificDefaults[key] ?? '';
    if(type === 'textarea') return `<label class="${klass}">${label}<textarea class="specific-input" data-key="${key}">${value}</textarea></label>`;
    return `<label class="${klass}">${label}<input class="specific-input" data-key="${key}" value="${value}" /></label>`;
  }).join('');
  wrap.querySelectorAll('.specific-input').forEach(input => input.addEventListener('change', saveSelectedScene));
}

function collectTemplateSpecificControls(){
  const controls = {};
  document.querySelectorAll('#templateSpecificControls .specific-input').forEach(input => {
    controls[input.dataset.key] = input.value;
  });
  return controls;
}

function renderSceneTimeline(){
  const scenes = currentScenes();
  const total = scenes.reduce((sum,s)=>sum + Number(s.duration || s.duration_seconds || 0), 0);
  $('totalRuntime').textContent = formatRuntime(total);
  $('sceneTimeline').innerHTML = scenes.map((scene, index)=>`
    <div class="scene-item ${index===state.selectedSceneIndex?'active':''}" data-index="${index}">
      <div class="scene-index">${String(index+1).padStart(2,'0')}</div>
      <div class="scene-info">
        <strong>${sceneLabel(scene,index)}</strong>
        <span>${scene.template || 'No template'}<br>${scene.purpose || scene.visual || ''}</span>
        <div class="scene-move">
          <button class="mini-btn" data-move="up" data-index="${index}">Up</button>
          <button class="mini-btn" data-move="down" data-index="${index}">Down</button>
        </div>
      </div>
      <div class="scene-duration">${Number(scene.duration || scene.duration_seconds || 0)}s</div>
    </div>
  `).join('') || '<p>No scenes yet. Generate an episode or add a scene.</p>';

  document.querySelectorAll('.scene-item').forEach(item => {
    item.addEventListener('click', (ev) => {
      const move = ev.target?.dataset?.move;
      if(move){ ev.stopPropagation(); moveScene(Number(ev.target.dataset.index), move); return; }
      state.selectedSceneIndex = Number(item.dataset.index);
      renderSceneTimeline();
      loadSelectedSceneControls();
      previewSelectedScene();
    });
  });
}

function loadSelectedSceneControls(){
  const scenes = currentScenes();
  const scene = scenes[state.selectedSceneIndex];
  if(!scene){
    $('selectedSceneLabel').textContent = 'No scene selected';
    return;
  }
  $('selectedSceneLabel').textContent = `${String(state.selectedSceneIndex+1).padStart(2,'0')} — ${sceneLabel(scene,state.selectedSceneIndex)}`;
  $('sceneNameInput').value = scene.scene || '';
  $('sceneDurationInput').value = Number(scene.duration || scene.duration_seconds || 30);
  $('sceneTemplateInput').value = scene.template || state.templates[0] || 'premium-base.html';
  $('sceneHeadlineInput').value = scene.headline || scene.scene || '';
  $('sceneSummaryInput').value = scene.summary || scene.purpose || scene.visual || '';
  $('lowerNameInput').value = scene.lower_name || 'ANAYA RAO';
  $('lowerTitleInput').value = scene.lower_title || 'Senior Anchor • Earth-Orbit Media Ring';
  $('tickerInput').value = scene.ticker || 'MARS TURNOUT PROJECTION RISES TO 91% • LUNAR OXYGEN-CREDIT STRIKE ENTERS NINTH DAY • EUROPA SIGNAL UNDER REVIEW';
  $('sourceInput').value = scene.source || 'Mars Civic Council Election Board';
  renderTemplateSpecificControls(scene);
}

function saveSelectedScene(){
  const scenes = currentScenes();
  const scene = scenes[state.selectedSceneIndex];
  if(!scene) return;
  scene.scene = $('sceneNameInput').value || scene.scene;
  scene.duration = Number($('sceneDurationInput').value || scene.duration || 30);
  delete scene.duration_seconds;
  scene.template = $('sceneTemplateInput').value;
  scene.headline = $('sceneHeadlineInput').value;
  scene.summary = $('sceneSummaryInput').value;
  scene.purpose = $('sceneSummaryInput').value;
  scene.lower_name = $('lowerNameInput').value;
  scene.lower_title = $('lowerTitleInput').value;
  scene.ticker = $('tickerInput').value;
  scene.source = $('sourceInput').value;
  scene.template_controls = collectTemplateSpecificControls();
  $('sceneOutput').textContent = JSON.stringify(scenes, null, 2);
  renderSceneTimeline();
  loadSelectedSceneControls();
}

function addScene(){
  const scenes = currentScenes();
  scenes.push({
    id: `s${String(scenes.length+1).padStart(2,'0')}`,
    scene: 'New Premium Scene',
    duration: 30,
    template: 'premium-base.html',
    purpose: 'Describe the editorial purpose of this scene.',
    headline: 'New Developing Story',
    summary: 'A new scene added to the premium episode timeline.',
    lower_name: 'ANAYA RAO',
    lower_title: 'Senior Anchor • Earth-Orbit Media Ring',
    ticker: 'EARTH • LUNA • MARS • OUTER BELT — DEVELOPING TIMELINE',
    source: '2147 News Network Editorial Desk'
  });
  state.selectedSceneIndex = scenes.length - 1;
  $('sceneOutput').textContent = JSON.stringify(scenes, null, 2);
  renderSceneTimeline(); loadSelectedSceneControls(); previewSelectedScene();
}

function duplicateScene(){
  const scenes = currentScenes();
  const scene = scenes[state.selectedSceneIndex];
  if(!scene) return;
  const copy = JSON.parse(JSON.stringify(scene));
  copy.id = `${copy.id || 'scene'}_copy_${Date.now()}`;
  copy.scene = `${copy.scene || 'Scene'} Copy`;
  scenes.splice(state.selectedSceneIndex+1, 0, copy);
  state.selectedSceneIndex += 1;
  $('sceneOutput').textContent = JSON.stringify(scenes, null, 2);
  renderSceneTimeline(); loadSelectedSceneControls(); previewSelectedScene();
}

function deleteScene(){
  const scenes = currentScenes();
  if(!scenes.length) return;
  scenes.splice(state.selectedSceneIndex, 1);
  state.selectedSceneIndex = Math.max(0, Math.min(state.selectedSceneIndex, scenes.length-1));
  $('sceneOutput').textContent = JSON.stringify(scenes, null, 2);
  renderSceneTimeline(); loadSelectedSceneControls(); previewSelectedScene();
}

function moveScene(index, direction){
  const scenes = currentScenes();
  const target = direction === 'up' ? index-1 : index+1;
  if(target < 0 || target >= scenes.length) return;
  [scenes[index], scenes[target]] = [scenes[target], scenes[index]];
  state.selectedSceneIndex = target;
  $('sceneOutput').textContent = JSON.stringify(scenes, null, 2);
  renderSceneTimeline(); loadSelectedSceneControls(); previewSelectedScene();
}

async function previewSelectedScene(){
  saveSelectedScene();
  const scenes = currentScenes();
  const scene = scenes[state.selectedSceneIndex];
  if(!scene){ $('scenePreviewStage').innerHTML = ''; return; }
  const html = await api('/api/scenes/preview', { method:'POST', body: JSON.stringify({
    scene,
    controls: {
      ...collectTemplateSpecificControls(),
      headline: $('sceneHeadlineInput').value,
      summary: $('sceneSummaryInput').value,
      ticker: $('tickerInput').value,
      lower_name: $('lowerNameInput').value,
      lower_title: $('lowerTitleInput').value,
      source: $('sourceInput').value
    }
  })});
  $('scenePreviewStage').innerHTML = html;
}


async function refreshSavedEpisodes(){
  const data = await api('/api/episodes');
  const select = $('savedEpisodeSelect');
  if(!data.episodes.length){
    select.innerHTML = '<option value="">No saved drafts yet</option>';
    return;
  }
  select.innerHTML = data.episodes.map(e=>`<option value="${e.episode_id}">${e.episode_id} — ${e.title} (${e.scene_count} scenes)</option>`).join('');
}

function collectCurrentDraft(){
  if(!state.currentDraft) state.currentDraft = { title: $('saveEpisodeTitle').value, headlines: [], script: '', scene_plan: [], metadata: {} };
  try {
    const sceneText = $('sceneOutput').textContent.trim();
    if(sceneText) state.currentDraft.scene_plan = JSON.parse(sceneText);
  } catch(err) {
    console.warn('Scene JSON parse failed; using in-memory scene plan.', err);
  }
  state.currentDraft.script = $('scriptOutput').textContent || state.currentDraft.script || '';
  state.currentDraft.title = $('saveEpisodeTitle').value || state.currentDraft.title || 'Untitled 2147 News Episode';
  state.currentDraft.headlines = Array.from($('headlineOutput').querySelectorAll('li')).map(li => li.textContent);
  return state.currentDraft;
}

async function saveDraft(){
  const draft = collectCurrentDraft();
  const result = await api('/api/episodes/save', { method:'POST', body: JSON.stringify({
    episode_id: $('saveEpisodeId').value,
    title: $('saveEpisodeTitle').value,
    draft
  })});
  $('saveStatus').textContent = `Saved: ${result.episode.episode_id} — ${result.episode.title}`;
  await refreshSavedEpisodes();
  $('savedEpisodeSelect').value = result.episode.episode_id;
}

async function loadDraftById(id, options={ switchToTimeline:true }){
  if(!id){ $('loadStatus').textContent = 'No saved draft selected.'; return; }
  const payload = await api(`/api/episodes/${id}`);
  const draft = payload.draft || {};
  state.currentDraft = draft;
  state.selectedSceneIndex = 0;
  $('saveEpisodeId').value = payload.episode_id || id;
  $('saveEpisodeTitle').value = payload.title || draft.title || id;
  $('headlineOutput').innerHTML = (draft.headlines || []).map(h=>`<li>${h}</li>`).join('');
  $('scriptOutput').textContent = draft.script || '';
  $('sceneOutput').textContent = JSON.stringify(draft.scene_plan || [], null, 2);
  renderSceneTimeline();
  loadSelectedSceneControls();
  previewSelectedScene();
  $('loadStatus').textContent = `Loaded: ${payload.episode_id} — ${payload.title}`;
  $('saveStatus').textContent = `Active draft: ${payload.episode_id}`;
  if($('savedEpisodeSelect')) $('savedEpisodeSelect').value = payload.episode_id || id;
  if(options.switchToTimeline) switchPanel('timeline');
}

async function loadDraft(){
  await loadDraftById($('savedEpisodeSelect').value);
}

async function loadPilotEpisode(){
  await refreshSavedEpisodes();
  await loadDraftById('2147-001-mars-independence');
}

async function createRenderPackage(){
  const draft = collectCurrentDraft();
  const result = await api('/api/render/package', { method:'POST', body: JSON.stringify({
    episode_id: $('saveEpisodeId').value || '2147-001-mars-independence',
    title: $('saveEpisodeTitle').value || draft.title || 'Untitled 2147 News Episode',
    draft,
    resolution_width: Number($('renderWidth').value || 1920),
    resolution_height: Number($('renderHeight').value || 1080)
  })});
  $('renderStatus').textContent = `Render package created: ${result.package_id} • ${result.manifest.scene_count} scenes • ${result.manifest.total_runtime_seconds}s`;
  const links = [
    `<a href="${result.zip_url}" download><span>Download full render package ZIP</span><span>ZIP</span></a>`,
    `<a href="${result.manifest_url}" target="_blank" download><span>Download/Open manifest.json</span><span>JSON</span></a>`,
    `<a href="${result.readme_url}" target="_blank" download><span>Download/Open render README</span><span>MD</span></a>`,
    ...result.scene_urls.map((url, index)=>`<a href="${url}" target="_blank" download><span>Open Scene ${String(index+1).padStart(2,'0')} Render Page</span><span>HTML</span></a>`)
  ];
  $('renderLinks').innerHTML = links.join('');
}

async function exportDraft(){
  if(!state.currentDraft) await generateEpisode();
  const result = await api('/api/export', { method:'POST', body: JSON.stringify({
    script: state.currentDraft.script,
    scene_plan: state.currentDraft.scene_plan,
    metadata: state.currentDraft.metadata
  })});
  $('exportStatus').textContent = `Exported ${result.files.length} production files.`;
  $('exportLinks').innerHTML = result.files.map(file => `<a href="${file.url}" download target="_blank"><span>${file.name}</span><span>${file.name.endsWith('.zip') ? 'ZIP' : 'Download'}</span></a>`).join('');
}

$('analyzeBtn').addEventListener('click', analyzeEvent);
$('eventSelect').addEventListener('change', analyzeEvent);
$('generateBtn').addEventListener('click', generateEpisode);
$('renderTemplateBtn').addEventListener('click', renderTemplate);
$('templateSelect').addEventListener('change', renderTemplate);
$('exportBtn').addEventListener('click', exportDraft);
$('renderPackageBtn').addEventListener('click', createRenderPackage);
$('saveDraftBtn').addEventListener('click', saveDraft);
$('loadDraftBtn').addEventListener('click', loadDraft);
$('refreshSavedBtn').addEventListener('click', refreshSavedEpisodes);
$('loadPilotBtn').addEventListener('click', loadPilotEpisode);
$('loadPilotDashboardBtn').addEventListener('click', loadPilotEpisode);
$('addSceneBtn').addEventListener('click', addScene);
$('duplicateSceneBtn').addEventListener('click', duplicateScene);
$('deleteSceneBtn').addEventListener('click', deleteScene);
$('saveSceneBtn').addEventListener('click', () => { saveSelectedScene(); previewSelectedScene(); });
$('previewSceneBtn').addEventListener('click', previewSelectedScene);
['sceneNameInput','sceneDurationInput','sceneHeadlineInput','sceneSummaryInput','lowerNameInput','lowerTitleInput','tickerInput','sourceInput'].forEach(id => {
  $(id).addEventListener('change', saveSelectedScene);
});
$('sceneTemplateInput').addEventListener('change', () => { saveSelectedScene(); loadSelectedSceneControls(); previewSelectedScene(); });

(async function init(){
  await loadWorld();
  await loadTemplates();
  await refreshSavedEpisodes();
  await analyzeEvent();
  await generateEpisode();
})();
