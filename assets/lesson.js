/* ==========================================================================
   KaiSTEM lesson engine (vanilla JS).
   Renders an interactive lesson page from a global `LESSON` data object.
   Ported from the Claude Design "Mobile-first lesson page design" component
   (originally an x-dc / DCLogic component) to a dependency-free runtime that
   works on static GitHub Pages.

   A lesson page only needs:
     <div id="app"></div>
     <script>window.LESSON = { ... }</script>
     <script src="../assets/lesson.js"></script>

   See assets/LESSON-SCHEMA.md for the data shape.
   ========================================================================== */
(function () {
  "use strict";

  var L = window.LESSON;
  if (!L) { console.error("[lesson] window.LESSON is not defined"); return; }

  var root = document.getElementById("app");
  if (!root) { console.error("[lesson] #app container not found"); return; }

  var STORE = "kaistem-" + (L.storageKey || "lesson");
  var NAME = L.childName || "Kai";
  var DAYS = L.days || [];
  var N = DAYS.length;

  /* ---- state + persistence ------------------------------------------------ */
  function load() {
    try { return JSON.parse(localStorage.getItem(STORE) || "{}"); }
    catch (e) { return {}; }
  }
  function blankJournal() {
    var rows = (L.journal && L.journal.rows) || 5;
    var out = [];
    for (var i = 0; i < rows; i++) out.push({ item: "", guess: null, result: null, cols: {} });
    return out;
  }
  var saved = load();
  var state = {
    mode: saved.mode || L.defaultMode || "prep",
    day: clampDay(saved.day || 1),
    sheetOpen: false,
    gear: saved.gear || {},
    journal: saved.journal || blankJournal()
  };

  function save() {
    try {
      localStorage.setItem(STORE, JSON.stringify({
        mode: state.mode, day: state.day, gear: state.gear, journal: state.journal
      }));
    } catch (e) {}
  }
  function clampDay(n) { return Math.min(Math.max(n | 0, 1), N || 1); }

  /* ---- tiny html helpers -------------------------------------------------- */
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  // Author-supplied rich strings may contain intentional inline markup
  // (e.g. <strong>, <em>). Those live in the trusted LESSON object.
  function rich(s) { return s == null ? "" : String(s); }
  function nameify(s) { return rich(s).replace(/\{name\}/g, esc(NAME)); }
  function attr(s) { return esc(s); }

  /* ---- section builders --------------------------------------------------- */
  function heroBlock() {
    var h = L.hero || {};
    var titleHTML = h.titleHTML || esc(L.title || "");
    var tags = (h.tags || []).map(function (t) {
      var cls = t.lead ? "tag lead-tag" : "tag";
      return '<span class="' + cls + '">' + rich(t.text || t) + "</span>";
    }).join("");
    return '' +
      '<header class="hero">' +
        '<p class="kicker">' + esc(h.kicker || "") + "</p>" +
        "<h1>" + titleHTML + "</h1>" +
        (h.subHTML ? '<p class="sub">' + nameify(h.subHTML) + "</p>" : "") +
        (tags ? '<div class="tags">' + tags + "</div>" : "") +
      "</header>";
  }

  function loopBlock() {
    var steps = L.loop || [];
    if (!steps.length) return "";
    var cards = steps.map(function (s) {
      return '<div class="loop-card ' + esc(s.tone || "") + '">' +
        '<div class="emoji">' + rich(s.emoji) + "</div>" +
        '<div class="name">' + esc(s.name) + "</div></div>";
    }).join("");
    return '' +
      '<div class="loop-wrap">' +
        '<p class="label">' + esc(L.loopLabel || "The loop · same every day") + "</p>" +
        '<div class="loop-scroll">' + cards + "</div>" +
      "</div>";
  }

  function modeBar() {
    var prep = state.mode === "prep";
    var pl = L.prepLabel || { main: "Prep", sub: " · the night before", emoji: "📋" };
    var rl = L.runLabel || { main: "Run", sub: " · live", emoji: "🧪" };
    return '' +
      '<div class="modebar" data-print="hide"><div class="seg">' +
        '<button class="seg-btn ' + (prep ? "on" : "") + '" data-act="mode" data-val="prep">' +
          '<span class="e">' + rich(pl.emoji) + "</span> " + esc(pl.main) +
          '<span class="muted">' + esc(pl.sub) + "</span></button>" +
        '<button class="seg-btn ' + (!prep ? "on" : "") + '" data-act="mode" data-val="run">' +
          '<span class="e">' + rich(rl.emoji) + "</span> " + esc(rl.main) +
          '<span class="muted">' + esc(rl.sub) + "</span></button>" +
      "</div></div>";
  }

  /* -- PREP ----------------------------------------------------------------- */
  function winBlock() {
    var w = L.win; if (!w) return "";
    return '<section class="section" style="margin-top:18px;"><div class="win-box">' +
      '<p class="label">' + esc(w.label || "The win this earns") + "</p>" +
      '<p class="body">' + nameify(w.html) + "</p></div></section>";
  }

  function gearBlock() {
    var p = L.prep || {};
    if (!p.gear) return "";
    var rows = p.gear.map(function (g) {
      var on = !!state.gear[g.id];
      return '<button class="gear-row ' + (on ? "on" : "") + '" data-act="gear" data-id="' + attr(g.id) + '">' +
        '<span class="gear-box">' + (on ? "✓" : "") + "</span>" +
        '<span class="gear-label"><strong>' + rich(g.strong) + "</strong>" + rich(g.rest || "") + "</span>" +
      "</button>";
    }).join("");
    return '<section class="section">' +
      '<p class="eyebrow">' + esc(p.gearKicker || "Gather the night before") + "</p>" +
      '<h2 class="h2">' + esc(p.gearTitle || "What you'll prepare") + "</h2>" +
      (p.gearLead ? '<p class="lead">' + nameify(p.gearLead) + "</p>" : "") +
      '<div class="gear-list">' + rows + "</div></section>";
  }

  function calloutsBlock() {
    var p = L.prep || {};
    if (!p.deepDive) return "";
    var d = p.deepDive;
    var cards = (d.blocks || []).map(function (b) {
      return '<div class="callout ' + esc(b.tone || "") + '">' +
        '<p class="label">' + rich(b.label) + "</p>" +
        '<p class="body">' + rich(b.html) + "</p></div>";
    }).join("");
    return '<section class="section">' +
      '<p class="eyebrow ' + esc(d.eyebrowTone || "test") + '">' + esc(d.kicker || "The important part") + "</p>" +
      '<h2 class="h2">' + esc(d.title || "") + "</h2>" +
      (d.lead ? '<p class="lead">' + nameify(d.lead) + "</p>" : "") +
      '<div class="callouts">' + cards + "</div></section>";
  }

  function safetyBlock() {
    var s = (L.prep || {}).safety; if (!s) return "";
    return '<section class="section" style="margin-top:26px;"><div class="sunk-panel">' +
      '<p class="label">' + esc(s.label || "⚠ Safety check") + "</p>" +
      '<p class="body">' + nameify(s.html) + "</p></div></section>";
  }

  function setupBlock() {
    var p = L.prep || {};
    if (!p.setup) return "";
    var steps = (p.setup.steps || []).map(function (t, i) {
      return '<div class="step"><span class="n">' + (i + 1) + "</span><p>" + nameify(t) + "</p></div>";
    }).join("");
    return '<section class="section">' +
      '<p class="eyebrow">' + esc(p.setup.kicker || "Setup") + "</p>" +
      '<h2 class="h2">' + esc(p.setup.title || "The night before") + "</h2>" +
      '<div class="steps">' + steps + "</div></section>";
  }

  function arcBlock() {
    var a = L.arc || {};
    var rows = DAYS.map(function (d) {
      return '<button class="arc-row" data-act="jump" data-day="' + d.n + '">' +
        '<span class="arc-day">DAY ' + d.n + "</span>" +
        '<span class="arc-mid"><span class="arc-title">' + rich(d.title) + "</span>" +
        '<span class="arc-sub">' + esc(d.stars) + " · " + esc(d.tag || "") + "</span></span>" +
        '<span class="arc-arrow">→</span></button>';
    }).join("");
    return '<section class="section">' +
      '<p class="eyebrow">' + esc(a.kicker || "The arc") + "</p>" +
      '<h2 class="h2">' + esc(a.title || "Same loop, one notch harder") + "</h2>" +
      (a.lead ? '<p class="lead">' + nameify(a.lead) + "</p>" : "") +
      '<div class="arc">' + rows + "</div></section>";
  }

  function prepView() {
    return '<div class="z">' +
      winBlock() + gearBlock() + calloutsBlock() + safetyBlock() + setupBlock() + arcBlock() +
    "</div>";
  }

  /* -- RUN ------------------------------------------------------------------ */
  function stepperBlock() {
    var pills = DAYS.map(function (d) {
      return '<button class="pill ' + (state.day === d.n ? "on" : "") + '" data-act="day" data-day="' + d.n + '">' + d.n + "</button>";
    }).join("");
    return '<div class="stepper" data-print="hide"><div class="row">' + pills + "</div></div>";
  }

  function activeDayBlock() {
    var d = DAYS[state.day - 1];
    if (!d) return "";
    var ask = (d.ask || []).map(function (line) {
      return '<p class="ask-line"><span class="q" aria-hidden="true">“</span>' + nameify(line) + "</p>";
    }).join("");
    var watch = (d.watch || []).map(function (w) {
      return '<div class="watch-row"><span class="icon">' + rich(w.icon) + "</span><span>" + nameify(w.text) + "</span></div>";
    }).join("");
    return '<section class="section" style="margin-top:14px;"><div class="day-head">' +
      '<p class="eyebrow">Day ' + d.n + " · " + esc(d.stars) + esc(d.lead || "") + "</p>" +
      "<h2>" + rich(d.title) + "</h2>" +
      '<p class="day-goal">' + nameify(d.goal) + "</p>" +
      '<div class="do-cards">' +
        '<div class="do-card"><p class="label">⏱ Set up</p><p class="body">' + nameify(d.setup) + "</p></div>" +
        '<div class="do-card"><p class="label">▶ Do</p><p class="body">' + nameify(d.doText) + "</p></div>" +
      "</div>" +
      '<div class="ask-box"><div class="ask-head">' +
        '<p class="label">🗣 Say this</p>' +
        '<button class="bigview-btn" data-act="openSheet" data-print="hide">Big view ↗</button>' +
      '</div><div class="ask-lines">' + ask + "</div></div>" +
      '<div class="watch"><p class="label">Watch for</p><div class="watch-rows">' + watch + "</div></div>" +
      '<div class="done"><span>✓</span><p><strong>Done when</strong> — ' + nameify(d.done) + "</p></div>" +
    "</div></section>";
  }

  function poleA(j) { return (j.poles && j.poles.a) || { key: "float", icon: "⬆", label: "float" }; }
  function poleB(j) { return (j.poles && j.poles.b) || { key: "sink", icon: "⬇", label: "sink" }; }
  function countResult(k) { return state.journal.filter(function (r) { return r.result === k; }).length; }

  function journalRow(j, r, i) {
    if (j.type === "log") {
      var cols = (j.columns || [{ key: "note", placeholder: "" }]).map(function (c) {
        return '<input class="j-input" data-act="jinput" data-i="' + i + '" data-key="' + attr(c.key) +
          '" data-kind="col" placeholder="' + attr(c.placeholder || "") + '">';
      }).join('<span class="j-sep"></span>');
      return '<div class="journal-row"><span class="j-idx">' + (i + 1) + "</span>" + cols + "</div>";
    }
    var a = poleA(j), b = poleB(j);
    function btn(kind, pole, on) {
      var cls = "jbtn " + (on ? (pole === a.key ? "on-float" : "on-sink") : "");
      return '<button class="' + cls + '" data-act="jstamp" data-i="' + i + '" data-kind="' + kind +
        '" data-pole="' + attr(pole) + '" title="' + attr(kind + " " + pole) + '">' +
        rich(pole === a.key ? a.icon : b.icon) + "</button>";
    }
    return '<div class="journal-row">' +
      '<span class="j-idx">' + (i + 1) + "</span>" +
      '<input class="j-input" data-act="jinput" data-i="' + i + '" data-key="item" data-kind="item" placeholder="' +
        attr(j.itemPlaceholder || "what we tested") + '">' +
      '<div class="j-btns">' +
        btn("guess", a.key, r.guess === a.key) + btn("guess", b.key, r.guess === b.key) +
        '<span class="j-sep"></span>' +
        btn("result", a.key, r.result === a.key) + btn("result", b.key, r.result === b.key) +
      "</div></div>";
  }

  function journalBlock() {
    var j = L.journal; if (!j) return "";
    var rowsHTML = state.journal.map(function (r, i) { return journalRow(j, r, i); }).join("");
    var foot = "";
    if (j.type !== "log") {
      var a = poleA(j), b = poleB(j);
      var fa = countResult(a.key), fb = countResult(b.key);
      var tmpl = j.countLabel || "🔢 " + a.label + "s {a} · " + b.label + "s {b}";
      tmpl = tmpl.replace("{a}", '<strong class="float">' + fa + "</strong>")
                 .replace("{b}", '<strong class="sink">' + fb + "</strong>");
      foot = '<div class="journal-foot">' +
        '<span>guess</span>' +
        '<span class="float">' + rich(a.icon) + " " + esc(a.label) + "</span>" +
        '<span class="sink">' + rich(b.icon) + " " + esc(b.label) + "</span>" +
        '<span class="count">' + tmpl + "</span></div>";
    }
    return '<section class="section" style="margin-top:34px;" id="journal">' +
      '<p class="eyebrow test">' + esc(j.kicker || "The keepsake") + "</p>" +
      '<h2 class="h2">' + esc(j.title || "Science journal") + "</h2>" +
      (j.intro ? '<p class="lead">' + nameify(j.intro) + "</p>" : "") +
      '<div class="journal"><div class="journal-head">' +
        '<p class="title">' + nameify(j.headerTitle || "My log") + "</p>" +
        '<span class="date">Date ____ / ____</span></div>' +
        '<div class="journal-rows">' + rowsHTML + "</div>" + foot +
      "</div>" +
      (j.said ? '<p class="journal-said">' + nameify(j.said) + "</p>" : "") +
    "</section>";
  }

  function qbankBlock() {
    var q = L.qbank; if (!q || !q.items) return "";
    var items = q.items.map(function (it) {
      return '<div class="q"><span class="moment">' + esc(it.moment) + "</span>" +
        '<span class="say">' + nameify(it.say) + "</span></div>";
    }).join("");
    return '<section class="section" style="margin-top:34px;">' +
      '<p class="eyebrow">' + esc(q.kicker || "Magic words") + "</p>" +
      '<h2 class="h2">' + esc(q.title || "Question bank") + "</h2>" +
      (q.intro ? '<p class="lead">' + nameify(q.intro) + "</p>" : "") +
      '<div class="qbank">' + items + "</div></section>";
  }

  function faqBlock() {
    var f = L.faq; if (!f || !f.items) return "";
    var items = f.items.map(function (it) {
      return "<details><summary>" + nameify(it.q) + '<span class="plus">+</span></summary>' +
        '<div class="body">' + nameify(it.a) + "</div></details>";
    }).join("");
    return '<section class="section" style="margin-top:34px;">' +
      '<p class="eyebrow">' + esc(f.kicker || "If it wobbles") + "</p>" +
      '<h2 class="h2">' + esc(f.title || "Troubleshooting") + "</h2>" +
      '<div class="faq">' + items + "</div></section>";
  }

  function runView() {
    return '<div class="z">' + stepperBlock() + activeDayBlock() + journalBlock() + qbankBlock() + faqBlock() + "</div>";
  }

  /* -- footer / fab / sheet ------------------------------------------------- */
  function footerBlock() {
    var f = L.footer || {};
    var links = (f.links || []).map(function (l) {
      return '<a href="' + attr(l.href) + '">' + rich(l.label) + "</a>";
    }).join("");
    return '<footer class="foot">' +
      (f.teacherHTML ? '<div class="teacher"><p>' + nameify(f.teacherHTML) + "</p></div>" : "") +
      (links ? '<div class="foot-links" data-print="hide">' + links + "</div>" : "") +
    "</footer>";
  }

  function fabBlock() {
    if (state.mode !== "run" || state.sheetOpen) return "";
    var d = DAYS[state.day - 1];
    return '<button class="fab" data-act="openSheet" data-print="hide">🗣 Say this · Day ' + (d ? d.n : "") + "</button>";
  }

  function sheetBlock() {
    if (!state.sheetOpen) return "";
    var d = DAYS[state.day - 1]; if (!d) return "";
    var lines = (d.ask || []).map(function (line) {
      return '<p class="sheet-line">' + nameify(line) + "</p>";
    }).join("");
    return '<div class="sheet" data-print="hide">' +
      '<div class="sheet-backdrop" data-act="closeSheet"></div>' +
      '<div class="sheet-card">' +
        '<div class="sheet-grip"></div>' +
        '<div class="sheet-head"><p class="label">🗣 Say this · Day ' + d.n + " · " + rich(d.title) + "</p>" +
          '<button class="sheet-close" data-act="closeSheet">✕</button></div>' +
        '<div class="sheet-lines">' + lines + "</div>" +
        '<p class="sheet-note">Ask one. Then wait five whole seconds before rescuing the silence.</p>' +
      "</div></div>";
  }

  function locatorBlock() {
    return '<div class="locator">' +
      '<a href="' + attr((L.footer && L.footer.homeHref) || "../index.html") + '">← All projects</a>' +
      "<span>PROJECT " + pad(L.index) + " / " + pad(L.total) + "</span></div>";
  }
  function pad(n) { return ("0" + (n || 0)).slice(-2); }

  /* ---- render ------------------------------------------------------------- */
  function render() {
    var body = state.mode === "prep" ? prepView() : runView();
    root.innerHTML =
      '<div class="l-root">' +
        '<div class="blob blob-a" aria-hidden="true"></div>' +
        '<div class="blob blob-b" aria-hidden="true"></div>' +
        locatorBlock() + heroBlock() + loopBlock() + modeBar() +
        body + footerBlock() + fabBlock() + sheetBlock() +
      "</div>";
    syncInputs();
  }

  // Set input values from state after each render (avoids attribute escaping
  // and keeps state authoritative for the journal).
  function syncInputs() {
    var inputs = root.querySelectorAll('input[data-act="jinput"]');
    for (var k = 0; k < inputs.length; k++) {
      var el = inputs[k];
      var i = +el.getAttribute("data-i");
      var key = el.getAttribute("data-key");
      var kind = el.getAttribute("data-kind");
      var row = state.journal[i]; if (!row) continue;
      el.value = (kind === "col") ? ((row.cols && row.cols[key]) || "") : (row[key] || "");
    }
  }

  /* ---- interactions ------------------------------------------------------- */
  function setMode(m) { state.mode = m; save(); render(); }
  function setDay(n) { state.day = clampDay(n); state.sheetOpen = false; save(); render(); }
  function jumpToDay(n) { state.mode = "run"; state.day = clampDay(n); save(); render(); window.scrollTo({ top: 0, behavior: "auto" }); }
  function openSheet() { state.sheetOpen = true; render(); }
  function closeSheet() { state.sheetOpen = false; render(); }
  function toggleGear(id) { state.gear[id] = !state.gear[id]; save(); render(); }
  function stamp(i, kind, pole) {
    var r = state.journal[i]; if (!r) return;
    r[kind] = (r[kind] === pole ? null : pole);
    save(); render();
  }

  root.addEventListener("click", function (e) {
    var t = e.target.closest("[data-act]"); if (!t) return;
    var act = t.getAttribute("data-act");
    if (act === "mode") setMode(t.getAttribute("data-val"));
    else if (act === "day") setDay(+t.getAttribute("data-day"));
    else if (act === "jump") jumpToDay(+t.getAttribute("data-day"));
    else if (act === "openSheet") openSheet();
    else if (act === "closeSheet") closeSheet();
    else if (act === "gear") toggleGear(t.getAttribute("data-id"));
    else if (act === "jstamp") stamp(+t.getAttribute("data-i"), t.getAttribute("data-kind"), t.getAttribute("data-pole"));
  });

  // Journal text inputs update state silently (no re-render → no focus loss).
  root.addEventListener("input", function (e) {
    var t = e.target;
    if (t.getAttribute && t.getAttribute("data-act") === "jinput") {
      var i = +t.getAttribute("data-i");
      var key = t.getAttribute("data-key");
      var kind = t.getAttribute("data-kind");
      var row = state.journal[i]; if (!row) return;
      if (kind === "col") { row.cols = row.cols || {}; row.cols[key] = t.value; }
      else { row[key] = t.value; }
      save();
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && state.sheetOpen) closeSheet();
  });

  // Apply per-lesson theme tokens, then paint.
  if (L.theme) {
    var rs = document.documentElement.style;
    Object.keys(L.theme).forEach(function (k) { rs.setProperty(k, L.theme[k]); });
  }
  if (L.title) document.title = L.title;
  render();
})();
