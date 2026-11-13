/* Stories — picture-book flip. Turns <div class="book" data-book> of
   <section class="leaf"> pages into a one-page-at-a-time book.
   Turn pages by: tapping the right/left side of the page, swiping,
   the big buttons, or the arrow keys. Remembers the page in the URL hash.

   Full screen: an immersive "storytime" overlay (works on iPhone, where
   Safari has no Fullscreen API for pages) plus the real Fullscreen API
   where the browser has one. Held sideways it becomes an open book:
   picture on the left, words on the right, pages turning over the spine.

   No JS → the leaves stay a normal stacked story (book.css). */
(function () {
  "use strict";

  var SWIPE_PX = 40;          // horizontal travel that counts as a swipe
  var BACK_ZONE = 0.33;       // single page: tap the left third to go back
  var TURN_MS = 900;          // a little longer than the CSS transition
  var SPREAD_RATIO = 1.15;    // full screen wider than this → sideways layout
  var SPREAD_MIN_W = 700;     // narrower sideways screens get picture + words on one page
  var TAP_GUARD_MS = 380;     // ignore page taps this soon after a turn (no double skips)
  var FULL_KEY = "kaistem-book-full";
  var FONT_STEPS = [1.5, 1.4, 1.3, 1.22, 1.15, 1.08, 1.0, 0.94, 0.88]; // rem, full screen

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) { n.className = cls; }
    if (text) { n.textContent = text; }
    return n;
  }

  function folioText(index, total) {
    return index > 0 && index < total - 1 ? index + " / " + (total - 2) : "";
  }

  function buildLeaf(leaf, index, total) {
    var front = el("div", "leaf-front");
    while (leaf.firstChild) { front.appendChild(leaf.firstChild); }
    var folio = folioText(index, total);
    if (folio) { front.appendChild(el("span", "folio", folio)); }
    var back = el("div", "leaf-back");
    back.setAttribute("aria-hidden", "true");
    leaf.appendChild(front);
    leaf.appendChild(back);
  }

  /* Open-book spread (full screen, sideways). Sheet k sits on the right:
     its front is page k's words, its back is page k+1's picture — so turning
     it over the spine lands the next picture on the left, like a real book. */
  function buildSpread(leaves) {
    var total = leaves.length;
    var spread = el("div", "book-spread");
    spread.setAttribute("aria-hidden", "true");
    var base = el("div", "spread-base");
    var firstImg = leaves[0].querySelector("img");
    if (firstImg) { base.appendChild(firstImg.cloneNode(false)); }
    spread.appendChild(base);
    var sheets = leaves.map(function (leaf, k) {
      var sheet = el("div", "sheet" + (leaf.classList.contains("cover") ? " cover" : "") +
                                      (leaf.classList.contains("end") ? " end" : ""));
      var front = el("div", "sheet-front");
      var text = leaf.querySelector(".leaf-text");
      if (text) { front.appendChild(text.cloneNode(true)); }
      var folio = folioText(k, total);
      if (folio) { front.appendChild(el("span", "folio", folio)); }
      var back = el("div", "sheet-back");
      var nextImg = k + 1 < total ? leaves[k + 1].querySelector("img") : null;
      if (nextImg) {
        var img = nextImg.cloneNode(false);
        img.removeAttribute("loading");
        back.appendChild(img);
      }
      sheet.appendChild(front);
      sheet.appendChild(back);
      spread.appendChild(sheet);
      return sheet;
    });
    return { root: spread, sheets: sheets };
  }

  function buildControls() {
    var bar = el("div", "book-controls");
    var prev = el("button", "book-btn prev", "← Back");
    var next = el("button", "book-btn next", "Turn →");
    var mid = el("div", "book-mid");
    var count = el("p", "book-count");
    var full = el("button", "book-full");
    prev.type = "button";
    next.type = "button";
    full.type = "button";
    full.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg><span>Full screen</span>';
    count.setAttribute("aria-live", "polite");
    mid.appendChild(count);
    mid.appendChild(full);
    bar.appendChild(prev);
    bar.appendChild(mid);
    bar.appendChild(next);
    var close = el("button", "book-close");
    close.type = "button";
    close.setAttribute("aria-label", "Close full screen");
    close.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>';
    var hint = el("p", "book-hint", "Tap the page or swipe to turn · ← → keys on a computer");
    return { bar: bar, prev: prev, next: next, count: count, full: full, close: close, hint: hint };
  }

  function pageFromHash(total) {
    var m = /^#page-(\d+)$/.exec(window.location.hash);
    if (!m) { return 0; }
    var n = parseInt(m[1], 10);
    return n >= 0 && n < total ? n : 0;
  }

  function nativeFullscreenElement() {
    return document.fullscreenElement || document.webkitFullscreenElement || null;
  }

  function init(book) {
    var leaves = Array.prototype.slice.call(book.children).filter(function (c) {
      return c.classList.contains("leaf");
    });
    var total = leaves.length;
    if (total < 2) { return; }

    leaves.forEach(function (leaf, i) { buildLeaf(leaf, i, total); });
    var spread = buildSpread(leaves);
    book.classList.add("is-flip");
    book.setAttribute("role", "region");
    book.setAttribute("aria-roledescription", "picture book");

    // Stage = book + spread + controls; it is what goes full screen.
    var stage = el("div", "book-stage");
    book.parentNode.insertBefore(stage, book);
    var ui = buildControls();
    stage.appendChild(ui.close);
    var area = el("div", "book-area");
    area.appendChild(book);
    area.appendChild(spread.root);
    stage.appendChild(area);
    stage.appendChild(ui.bar);
    stage.insertAdjacentElement("afterend", ui.hint);
    var standalone = window.navigator.standalone === true;
    var canNative = !!(document.documentElement.requestFullscreen || document.documentElement.webkitRequestFullscreen);
    if (!canNative && !standalone) {
      // iPhone: pages can't go truly full screen, but a home-screen icon can
      ui.hint.appendChild(document.createElement("br"));
      ui.hint.appendChild(document.createTextNode("iPhone tip: Share → Add to Home Screen opens it truly full screen."));
    }

    var current = -1;
    var isFull = false;
    var isSpread = false;
    var settleTimer = 0;
    var lastTurn = 0;
    var pushedHistory = false;
    var wakeLock = null;
    var inerted = [];

    /* ---- sizing ---------------------------------------------------------- */

    function textOverflows(texts) {
      return texts.some(function (t) { return t.scrollHeight > t.clientHeight + 1; });
    }

    // Inline page: one shared height = the tallest picture + words.
    function fitInline() {
      book.style.width = "";
      var tallest = 0;
      leaves.forEach(function (leaf) {
        var img = leaf.querySelector("img");
        var text = leaf.querySelector(".leaf-text");
        var textH = 0;
        if (text) {            // measure the words at their natural height
          text.style.flex = "none";
          textH = text.offsetHeight;
          text.style.flex = "";
        }
        var h = (img ? img.offsetHeight : 0) + textH;
        if (h > tallest) { tallest = h; }
      });
      if (tallest > 0) { book.style.height = Math.ceil(tallest) + "px"; }
    }

    // Full screen: fill the area, then step the words down until every page fits.
    function fitFull() {
      var w = area.clientWidth, h = area.clientHeight;
      var sideways = w > h * SPREAD_RATIO;
      isSpread = sideways && w >= SPREAD_MIN_W;
      var isSide = sideways && !isSpread;
      stage.classList.toggle("is-spread", isSpread);
      stage.classList.toggle("is-side", isSide);
      var texts;
      if (isSide) {
        // small phone held sideways: picture (~58%) and words share one page
        book.style.width = Math.floor(w) + "px";
        book.style.height = Math.floor(Math.min(h, w * 0.58 * 0.75)) + "px";
        texts = leaves.map(function (l) { return l.querySelector(".leaf-text"); });
      } else if (isSpread) {
        // two 4:3 halves side by side, as big as the screen allows
        var sw = Math.min(w, h * 8 / 3);
        spread.root.style.width = Math.floor(sw) + "px";
        spread.root.style.height = Math.floor(Math.min(h, sw * 3 / 8)) + "px";
        texts = spread.sheets.map(function (s) { return s.querySelector(".leaf-text"); });
      } else {
        var bw = Math.min(w, h * 0.72, 760);
        book.style.width = Math.floor(bw) + "px";
        book.style.height = Math.floor(Math.min(h, bw * 1.75)) + "px";
        texts = leaves.map(function (l) { return l.querySelector(".leaf-text"); });
      }
      texts = texts.filter(Boolean);
      for (var i = 0; i < FONT_STEPS.length; i++) {
        stage.style.setProperty("--leaf-fs", FONT_STEPS[i] + "rem");
        if (!textOverflows(texts)) { break; }
      }
    }

    function fit() {
      if (isFull) { fitFull(); } else { fitInline(); }
    }

    /* ---- page state ------------------------------------------------------ */

    function stackSet(items, turning) {
      items.forEach(function (item, i) {
        var flipped = i < current;
        item.classList.toggle("is-flipped", flipped);
        // unflipped: first on top. flipped: last-turned on top.
        item.style.zIndex = item === turning ? total + 1 : (flipped ? i + 1 : total - i);
      });
    }

    function stack(turnFrom, turnTo) {
      function turner(items) {
        if (turnFrom < 0) { return null; }
        return turnTo > turnFrom ? items[turnFrom] : items[turnTo];
      }
      stackSet(leaves, turner(leaves));
      stackSet(spread.sheets, turner(spread.sheets));
      leaves.forEach(function (leaf, i) {
        var hidden = i !== current;
        leaf.setAttribute("aria-hidden", hidden ? "true" : "false");
        if ("inert" in leaf) { leaf.inert = hidden; }
      });
    }

    function label() {
      if (current === 0) { return "Cover"; }
      if (current === total - 1) { return "The end"; }
      return "Page " + current + " of " + (total - 2);
    }

    function go(n, fromHash) {
      n = Math.max(0, Math.min(total - 1, n));
      if (n === current) { return; }
      var from = current;
      current = n;
      lastTurn = Date.now();
      stack(from, n);
      window.clearTimeout(settleTimer);
      if (from >= 0) { settleTimer = window.setTimeout(function () { stack(-1, -1); }, TURN_MS); }

      ui.prev.disabled = current === 0;
      ui.next.disabled = current === total - 1;
      ui.next.textContent = current === 0 ? "Open →" : "Turn →";
      ui.count.textContent = label();
      if (!fromHash && window.history && window.history.replaceState) {
        var url = current === 0 ? window.location.pathname + window.location.search : "#page-" + current;
        window.history.replaceState(null, "", url);
      }
    }

    /* ---- full screen ----------------------------------------------------- */

    // Everything outside the stage goes inert while the book is open.
    function setBackgroundInert(on) {
      if (!on) {
        inerted.forEach(function (n) { n.inert = false; });
        inerted = [];
        return;
      }
      if (!("inert" in document.body)) { return; }
      var node = stage;
      while (node && node !== document.body) {
        Array.prototype.forEach.call(node.parentNode.children, function (sib) {
          if (sib !== node && !sib.inert && sib.tagName !== "SCRIPT") { sib.inert = true; inerted.push(sib); }
        });
        node = node.parentNode;
      }
    }

    // Keep the screen awake mid-story (where the browser allows it).
    function setWakeLock(on) {
      if (!("wakeLock" in navigator)) { return; }
      if (on) {
        navigator.wakeLock.request("screen").then(function (lock) { wakeLock = lock; })
          .catch(function () { /* low battery or not allowed: the story still works */ });
      } else if (wakeLock) {
        wakeLock.release().catch(function () {});
        wakeLock = null;
      }
    }
    document.addEventListener("visibilitychange", function () {
      if (isFull && document.visibilityState === "visible") { setWakeLock(true); }
    });
    window.addEventListener("popstate", function () {
      if (isFull) { pushedHistory = false; setFull(false, { fromPop: true }); }
    });

    function setFull(on, opts) {
      var fromPop = !!(opts && opts.fromPop);
      var restoring = !!(opts && opts.restoring);
      if (on === isFull) { return; }
      isFull = on;
      stage.classList.toggle("is-full", on);
      document.documentElement.classList.toggle("book-locked", on);
      ui.full.setAttribute("aria-pressed", on ? "true" : "false");
      try { if (on) { sessionStorage.setItem(FULL_KEY, "1"); } else { sessionStorage.removeItem(FULL_KEY); } }
      catch (err) { /* private mode: no restore, that's fine */ }
      setBackgroundInert(on);
      setWakeLock(on);
      if (on && !pushedHistory && window.history && window.history.pushState) {
        // Android back button / browser back closes the book instead of leaving the page
        window.history.pushState({ bookFull: true }, "", window.location.href);
        pushedHistory = true;
      }
      if (!on && pushedHistory && !fromPop) {
        pushedHistory = false;
        window.history.back();
      }
      if (!on) { pushedHistory = false; }
      if (on) {
        stage.setAttribute("role", "dialog");
        stage.setAttribute("aria-modal", "true");
        stage.setAttribute("aria-label", book.getAttribute("aria-label") || "Picture book");
        // real full screen needs a tap, so a restored session gets the overlay only
        var req = restoring ? null : (stage.requestFullscreen || stage.webkitRequestFullscreen);
        if (req) {
          try {
            var p = req.call(stage);
            if (p && p.catch) { p.catch(function () { /* overlay alone is fine */ }); }
          } catch (err) { /* overlay alone is fine */ }
        }
        stage.setAttribute("tabindex", "-1");
        stage.focus({ preventScroll: true });
      } else {
        stage.removeAttribute("role");
        stage.removeAttribute("aria-modal");
        stage.removeAttribute("aria-label");
        stage.removeAttribute("tabindex");
        stage.classList.remove("is-spread");
        stage.classList.remove("is-side");
        stage.style.removeProperty("--leaf-fs");
        book.style.width = "";
        isSpread = false;
        if (nativeFullscreenElement()) {
          var exit = document.exitFullscreen || document.webkitExitFullscreen;
          if (exit) {
            try {
              var q = exit.call(document);
              if (q && q.catch) { q.catch(function () {}); }
            } catch (err) { /* already out */ }
          }
        }
        ui.full.focus({ preventScroll: true });
      }
      // let the new layout settle, then size it
      window.requestAnimationFrame(fit);
    }

    function onNativeChange() {
      // user left native full screen (Esc, system gesture) → leave ours too
      if (isFull && !nativeFullscreenElement()) { setFull(false); }
      else { window.requestAnimationFrame(fit); }
    }
    document.addEventListener("fullscreenchange", onNativeChange);
    document.addEventListener("webkitfullscreenchange", onNativeChange);

    ui.full.addEventListener("click", function () { setFull(true); });
    ui.close.addEventListener("click", function () { setFull(false); });
    ui.prev.addEventListener("click", function () { go(current - 1); });
    ui.next.addEventListener("click", function () { go(current + 1); });

    /* ---- gestures -------------------------------------------------------- */

    function gestures(surface, backZone) {
      var startX = 0, startY = 0, tracking = false, swiped = false;
      surface.addEventListener("pointerdown", function (e) {
        tracking = true; swiped = false; startX = e.clientX; startY = e.clientY;
      });
      surface.addEventListener("pointerup", function (e) {
        if (!tracking) { return; }
        tracking = false;
        var dx = e.clientX - startX, dy = e.clientY - startY;
        if (Math.abs(dx) > SWIPE_PX && Math.abs(dx) > Math.abs(dy)) {
          swiped = true;
          if (Date.now() - lastTurn < TAP_GUARD_MS) { return; }
          go(dx < 0 ? current + 1 : current - 1);
        }
      });
      surface.addEventListener("pointercancel", function () { tracking = false; });
      surface.addEventListener("click", function (e) {
        if (swiped) { swiped = false; return; }
        if (e.target.closest("a, button")) { return; }
        if (Math.abs(e.clientY - startY) > SWIPE_PX) { return; }
        if (Date.now() - lastTurn < TAP_GUARD_MS) { return; }
        var box = surface.getBoundingClientRect();
        var x = (e.clientX - box.left) / box.width;
        go(x < backZone ? current - 1 : current + 1);
      });
    }
    gestures(book, BACK_ZONE);
    gestures(spread.root, 0.5);   // open book: left page = back, right page = forward

    document.addEventListener("keydown", function (e) {
      if (e.altKey || e.ctrlKey || e.metaKey) { return; }
      if (e.target.closest && e.target.closest("input, textarea, select")) { return; }
      if (e.key === "ArrowRight") { e.preventDefault(); go(current + 1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); go(current - 1); }
      else if (e.key === "Escape" && isFull) { setFull(false); }
      else if ((e.key === "f" || e.key === "F") && !e.shiftKey) { setFull(!isFull); }
    });
    window.addEventListener("hashchange", function () { go(pageFromHash(total), true); });

    var fitTimer = 0;
    window.addEventListener("resize", function () {
      window.clearTimeout(fitTimer);
      fitTimer = window.setTimeout(fit, 120);
    });
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(fit); }
    leaves.forEach(function (leaf) {
      var img = leaf.querySelector("img");
      if (img && !img.complete) { img.addEventListener("load", fit); }
    });

    fit();
    go(pageFromHash(total), true);
    // came back (reload, edge-swipe back and forward) while the book was open → reopen it
    try { if (sessionStorage.getItem(FULL_KEY) === "1") { setFull(true, { restoring: true }); } }
    catch (err) { /* no storage: start inline */ }
  }

  function start() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-book]"), init);
  }
  if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", start); }
  else { start(); }
})();
