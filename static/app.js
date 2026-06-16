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

async function exportDraft(){
  if(!state.currentDraft) await generateEpisode();
  const result = await api('/api/export', { method:'POST', body: JSON.stringify({
    script: state.currentDraft.script,
    scene_plan: state.currentDraft.scene_plan,
    metadata: state.currentDraft.metadata
  })});
  $('exportStatus').textContent = `Exported: ${result.files.join(', ')}`;
}

$('analyzeBtn').addEventListener('click', analyzeEvent);
$('eventSelect').addEventListener('change', analyzeEvent);
$('generateBtn').addEventListener('click', generateEpisode);
$('renderTemplateBtn').addEventListener('click', renderTemplate);
$('templateSelect').addEventListener('change', renderTemplate);
$('exportBtn').addEventListener('click', exportDraft);
$('addSceneBtn').addEventListener('click', addScene);
$('duplicateSceneBtn').addEventListener('click', duplicateScene);
$('deleteSceneBtn').addEventListener('click', deleteScene);
$('saveSceneBtn').addEventListener('click', () => { saveSelectedScene(); previewSelectedScene(); });
$('previewSceneBtn').addEventListener('click', previewSelectedScene);
['sceneNameInput','sceneDurationInput','sceneTemplateInput','sceneHeadlineInput','sceneSummaryInput','lowerNameInput','lowerTitleInput','tickerInput','sourceInput'].forEach(id => {
  $(id).addEventListener('change', saveSelectedScene);
});

(async function init(){
  await loadWorld();
  await loadTemplates();
  await analyzeEvent();
  await generateEpisode();
})();
