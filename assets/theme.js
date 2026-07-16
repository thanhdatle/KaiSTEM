/* KaiSTEM theme toggle — self-contained, dependency-free.
   Stored choice (localStorage "kaistem-theme": "dark"|"light") wins;
   otherwise follows the OS. Styled via .theme-toggle in styles.css/lesson.css. */
(function () {
  "use strict";
  var KEY = "kaistem-theme";
  var mq = window.matchMedia("(prefers-color-scheme: dark)");
  var SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.4"/><path d="M12 2.5v2.6M12 18.9v2.6M2.5 12h2.6M18.9 12h2.6M5 5l1.8 1.8M17.2 17.2 19 19M19 5l-1.8 1.8M6.8 17.2 5 19"/></svg>';
  var MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.4 14.2A8.5 8.5 0 1 1 9.8 3.6a7 7 0 1 0 10.6 10.6z"/></svg>';

  function stored() {
    try { var v = localStorage.getItem(KEY); return v === "dark" || v === "light" ? v : null; }
    catch (e) { return null; }
  }
  function effective() { return stored() || (mq.matches ? "dark" : "light"); }

  function apply(theme, persist) {
    document.documentElement.dataset.theme = theme;
    if (persist) { try { localStorage.setItem(KEY, theme); } catch (e) { /* private mode: session-only */ } }
    var btn = document.getElementById("kaistem-theme-toggle");
    if (btn) {
      // Icon shows the mode you'd switch TO
      btn.innerHTML = theme === "dark" ? SUN : MOON;
      btn.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
    }
  }

  // Apply ASAP to minimise a wrong-theme flash (runs before first paint when
  // the script tag sits in <head> or early <body>)
  if (stored()) { document.documentElement.dataset.theme = stored(); }

  function init() {
    if (document.getElementById("kaistem-theme-toggle")) { return; }
    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = "kaistem-theme-toggle";
    btn.className = "theme-toggle";
    btn.setAttribute("aria-label", "Toggle dark mode");
    btn.setAttribute("data-print", "hide");
    btn.addEventListener("click", function () {
      apply(effective() === "dark" ? "light" : "dark", true);
    });
    document.body.appendChild(btn);
    apply(effective(), false);
    // No stored choice → keep tracking the OS live
    var onOs = function () { if (!stored()) { apply(effective(), false); } };
    if (mq.addEventListener) { mq.addEventListener("change", onOs); }
    else if (mq.addListener) { mq.addListener(onOs); }
  }

  if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", init); }
  else { init(); }
})();
