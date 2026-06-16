const state = { world: null, selectedEventId: null, currentDraft: null };
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
  $('templateSelect').innerHTML = data.templates.map(t=>`<option value="${t}">${t}</option>`).join('');
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
  $('headlineOutput').innerHTML = data.headlines.map(h=>`<li>${h}</li>`).join('');
  $('scriptOutput').textContent = data.script;
  $('sceneOutput').textContent = JSON.stringify(data.scene_plan, null, 2);
}

async function renderTemplate(){
  const html = await api('/api/templates/preview', { method:'POST', body: JSON.stringify({
    template_name: $('templateSelect').value,
    headline: $('previewHeadline').value,
    summary: 'A historic referendum could reshape political authority across Earth, Mars, Luna, and the Outer Belt.'
  })});
  $('templateStage').innerHTML = html;
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

(async function init(){
  await loadWorld();
  await loadTemplates();
  await analyzeEvent();
  await generateEpisode();
})();
