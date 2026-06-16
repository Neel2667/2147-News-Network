/* 2147 News Network — Broadcast Components V2
   Small helper functions for generating approved broadcast elements.
   These are dependency-free and safe for static previews.
*/

(function () {
  const esc = (value = "") => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const repeatTicker = (text) => {
    const safe = esc(text);
    return `<span>${safe}</span><span>${safe}</span>`;
  };

  const Broadcast2147 = {
    bug({ compact = false, invert = false } = {}) {
      return `
        <div class="bcast-bug ${compact ? "bcast-bug--compact" : ""} ${invert ? "bcast-bug--invert" : ""}">
          <div class="bcast-bug__mark">2147</div>
          <div class="bcast-bug__word">News<br>Network</div>
          <div class="bcast-bug__accent"></div>
        </div>`;
    },

    live(label = "Live") {
      return `<div class="bcast-live">${esc(label)}</div>`;
    },

    clock(text = "18 Oct 2147 / 19:42 UTC-O") {
      return `<div class="bcast-clock">${esc(text)}</div>`;
    },

    source(text, { dark = false, label = "Source" } = {}) {
      return `
        <div class="bcast-source ${dark ? "bcast-source--dark" : ""}">
          <b class="bcast-source__label">${esc(label)}</b>
          <span class="bcast-source__text">${esc(text)}</span>
        </div>`;
    },

    strap({
      label = "Developing",
      headline = "Mars referendum enters final hours",
      sub = "Earth Union officials prepare emergency legal review",
      tag = "Live 2147",
      breaking = false,
    } = {}) {
      return `
        <div class="bcast-strap ${breaking ? "bcast-strap--breaking" : ""}">
          <div class="bcast-strap__label">${esc(label)}</div>
          <div class="bcast-strap__main">
            <strong class="bcast-strap__headline">${esc(headline)}</strong>
            <span class="bcast-strap__sub">${esc(sub)}</span>
          </div>
          <div class="bcast-strap__tag">${esc(tag)}</div>
        </div>`;
    },

    ticker({
      label = "Headlines",
      text = "MARS TURNOUT PROJECTED AT 91% • EARTH UNION LEGAL REVIEW BEGINS • HELION GRID SYSTEMS WARNS OF CONTRACT RISK •",
    } = {}) {
      return `
        <div class="bcast-ticker">
          <div class="bcast-ticker__label">${esc(label)}</div>
          <div class="bcast-ticker__window">
            <div class="bcast-ticker__crawl">${repeatTicker(text)}</div>
          </div>
        </div>`;
    },

    lowerThird({
      role = "Anchor",
      name = "Anaya Rao",
      title = "Senior Anchor • Earth-Orbit Media Ring",
      location = "New Delhi Orbital Hub",
      variant = "left",
    } = {}) {
      const variantClass = variant === "bottom" ? "bcast-lower-third--bottom" : variant === "breaking" ? "bcast-lower-third--breaking" : "";
      return `
        <div class="bcast-lower-third ${variantClass}">
          <div class="bcast-lower-third__role">${esc(role)}</div>
          <div class="bcast-lower-third__name">
            <strong>${esc(name)}</strong>
            <span>${esc(title)}</span>
          </div>
          <div class="bcast-lower-third__loc">${esc(location)}</div>
        </div>`;
    },

    storyPanel({
      kicker = "Breaking / Mars Sovereignty",
      headline = "Mars Votes On Independence",
      summary = "Final voting cycle underway across 42 recognized settlement zones.",
    } = {}) {
      return `
        <article class="bcast-story-panel">
          <div class="bcast-story-panel__kicker">${esc(kicker)}</div>
          <h3>${esc(headline)}</h3>
          <p>${esc(summary)}</p>
        </article>`;
    },

    marsOts() {
      return `
        <aside class="bcast-ots">
          <div class="bcast-mars-orb"></div>
          <div style="position:absolute;left:30px;top:38px;font-family:var(--bcast-condensed);font-size:48px;line-height:.86;text-transform:uppercase;">57%<br>Independence</div>
          <div style="position:absolute;left:30px;right:30px;bottom:30px;display:grid;gap:10px;">
            <div style="display:grid;grid-template-columns:112px 1fr 42px;gap:9px;align-items:center;font-size:12px;font-weight:900;"><b>YES</b><div style="height:10px;border-radius:999px;background:rgba(255,255,255,.18);overflow:hidden;"><div style="width:57%;height:100%;background:var(--bcast-green);border-radius:999px;"></div></div><b>57</b></div>
            <div style="display:grid;grid-template-columns:112px 1fr 42px;gap:9px;align-items:center;font-size:12px;font-weight:900;"><b>UNION</b><div style="height:10px;border-radius:999px;background:rgba(255,255,255,.18);overflow:hidden;"><div style="width:39%;height:100%;background:var(--bcast-mars);border-radius:999px;"></div></div><b>39</b></div>
          </div>
        </aside>`;
    },
  };

  window.Broadcast2147 = Broadcast2147;
})();
