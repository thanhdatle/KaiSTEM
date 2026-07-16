/* ==========================================================================
   KaiSTEM card deck — mental-rotation trials, drawn as exact SVG.

   Why SVG and not AI images: a rotation task is only valid if the "same"
   shape is provably the same shape turned. An image generator cannot
   guarantee that; an SVG transform can.

   A trial shows one target shape, then two candidates:
     · the target, rotated             → the answer ("same shape, just turned")
     · the target, mirrored then rotated → a chiral decoy (a different shape)
   Mirror-versus-rotation discrimination is the core of the Children's Mental
   Transformation Task (Levine et al. 2012). That discrimination is the part
   that trains; see reference/0002-visual-thinking-evidence.html.

   Usage, from a lesson, after lesson.js:
     CARDS.mount({ mount:"#deck", title:"…", trials:[{shape:"ell", angle:90}] })
   ========================================================================== */
(function (global) {
  "use strict";

  /* Four chiral shapes on a 100×100 box. Chiral means the mirror image cannot
     be produced by any rotation — so the decoy is always genuinely a different
     shape, never an accidental duplicate of the answer. */
  var SHAPES = {
    ell:  "30,10 50,10 50,70 80,70 80,90 30,90",
    ess:  "25,25 65,25 65,50 85,50 85,75 45,75 45,50 25,50",
    flag: "30,10 30,90 42,90 42,58 78,42 42,26 42,10",
    boot: "35,10 57,10 57,62 82,74 78,90 35,78"
  };

  var NAMES = { ell: "the corner", ess: "the zigzag", flag: "the flag", boot: "the boot" };

  function svg(shape, angle, mirror) {
    var pts = SHAPES[shape];
    if (!pts) throw new Error("cards.js: unknown shape '" + shape + "'");
    // Mirror about the box's vertical midline first, then rotate about centre.
    var t = "rotate(" + angle + " 50 50)" + (mirror ? " translate(100 0) scale(-1 1)" : "");
    var label = (mirror ? "a flipped version of " : "") + (NAMES[shape] || shape) +
      (angle ? ", turned " + angle + " degrees" : "");
    // Padded viewBox: the farthest vertex sits exactly 50 units from the centre
    // of rotation, so at 45°/135° an unpadded box clips the stroke.
    return '<svg viewBox="-7 -7 114 114" role="img" aria-label="' + label + '">' +
      '<polygon points="' + pts + '" transform="' + t + '" ' +
      'fill="var(--accent)" fill-opacity="0.18" ' +
      'stroke="var(--accent-deep)" stroke-width="3" stroke-linejoin="round"/></svg>';
  }

  /* Which side holds the answer.

     Deterministic — no Math.random — so the printed sheet and the on-screen
     deck always agree, and reopening never reshuffles under the child.

     But NOT alternating: a simple A,B,A,B key can be beaten by a child who
     tracks "the other side from last time" without ever turning a shape.
     So we use the Thue–Morse sequence (parity of the popcount of i), which is
     balanced over any prefix of even length and provably cube-free — it
     contains no XXX repetition, hence no short positional rule to latch onto. */
  function sideOf(i) {
    var bits = 0;
    for (var n = i; n > 0; n >>= 1) bits ^= n & 1;
    return bits ? "b" : "a";
  }

  function mount(cfg) {
    var host = document.querySelector(cfg.mount);
    if (!host) return;
    var trials = cfg.trials || [];
    if (!trials.length) return;
    var i = 0;
    var answered = [];

    host.innerHTML =
      '<button class="deck-launch" type="button" aria-haspopup="dialog">' +
        '<span aria-hidden="true">🃏</span> ' + (cfg.launcherLabel || "Cards") +
      "</button>" +
      '<div class="deck" hidden role="dialog" aria-modal="true" aria-label="' +
        (cfg.title || "Card deck") + '">' +
        '<div class="deck-bar">' +
          "<span><strong>" + (cfg.title || "Card deck") + "</strong></span>" +
          '<button class="deck-close" type="button" aria-label="Close the deck">✕</button>' +
        "</div>" +
        '<div class="deck-stage"></div>' +
        '<div class="deck-nav">' +
          '<button data-nav="prev" type="button">← Back</button>' +
          '<span class="deck-dots" aria-live="polite"></span>' +
          '<button data-nav="next" type="button">Next →</button>' +
        "</div>" +
      "</div>" +
      '<div class="deck-print"></div>';

    var deck  = host.querySelector(".deck");
    var stage = host.querySelector(".deck-stage");
    var dots  = host.querySelector(".deck-dots");
    var prev  = host.querySelector('[data-nav="prev"]');
    var next  = host.querySelector('[data-nav="next"]');

    function paint() {
      var t = trials[i];
      var right = sideOf(i);
      var picked = answered[i];

      function choice(side) {
        var isRight = side === right;
        var s = picked ? (isRight ? "right" : "wrong") : "";
        return '<button class="deck-choice" type="button" data-side="' + side + '"' +
          (s ? ' data-state="' + s + '"' : "") +
          ' aria-label="Choice ' + side.toUpperCase() + '">' +
          svg(t.shape, isRight ? t.angle : (t.angle + 180) % 360, !isRight) +
          '<span class="mark" aria-hidden="true">' + (isRight ? "✓" : "✕") + "</span>" +
        "</button>";
      }

      var verdict = picked
        ? (picked === right
            ? "Yes — same shape, just turned."
            : "That one is flipped. It is a different shape.")
        : "";

      stage.innerHTML =
        '<p class="deck-prompt">' +
          (cfg.prompt || "Which one is <em>the same shape, just turned</em>?") + "</p>" +
        '<div class="deck-target">' + svg(t.shape, 0, false) + "</div>" +
        '<div class="deck-choices">' + choice("a") + choice("b") + "</div>" +
        '<p class="deck-verdict"' +
          (picked ? ' data-state="' + (picked === right ? "right" : "wrong") + '"' : "") +
          ' role="status">' + verdict + "</p>";

      dots.textContent = (i + 1) + " / " + trials.length;
      prev.disabled = i === 0;
      next.disabled = i === trials.length - 1;
    }

    function open()  { deck.hidden = false; paint(); host.querySelector(".deck-close").focus(); }
    function close() { deck.hidden = true;  host.querySelector(".deck-launch").focus(); }

    host.addEventListener("click", function (e) {
      var el = e.target.closest && e.target.closest("button");
      if (!el) return;
      if (el.classList.contains("deck-launch")) return open();
      if (el.classList.contains("deck-close"))  return close();
      if (el.getAttribute("data-nav") === "prev" && i > 0) { i--; return paint(); }
      if (el.getAttribute("data-nav") === "next" && i < trials.length - 1) { i++; return paint(); }
      if (el.classList.contains("deck-choice") && !answered[i]) {
        answered[i] = el.getAttribute("data-side");
        paint();
      }
    });

    document.addEventListener("keydown", function (e) {
      if (deck.hidden) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowRight" && i < trials.length - 1) { i++; paint(); }
      else if (e.key === "ArrowLeft"  && i > 0) { i--; paint(); }
    });

    /* ---- print face: the same trials, cut-out sized, plus an answer key ---- */
    var cards = trials.map(function (t, n) {
      var aIsRight = sideOf(n) === "a";
      return '<div class="print-card">' +
        '<p class="cap">Card ' + (n + 1) + " · " + (NAMES[t.shape] || t.shape) + "</p>" +
        '<div class="row">' +
          svg(t.shape, 0, false) +
          '<span class="vs">→</span>' +
          svg(t.shape, aIsRight ? t.angle : (t.angle + 180) % 360, !aIsRight) +
          svg(t.shape, aIsRight ? (t.angle + 180) % 360 : t.angle, aIsRight) +
        "</div>" +
        '<p class="pick"><span>A</span><span>B</span></p>' +
      "</div>";
    }).join("");

    var key = trials.map(function (t, n) { return (n + 1) + sideOf(n).toUpperCase(); }).join("  ·  ");

    host.querySelector(".deck-print").innerHTML =
      "<h1>" + (cfg.title || "Card deck") + "</h1>" +
      '<p class="note">' + (cfg.printNote ||
        "Cut along the dashed lines. Show the left shape, then ask which of the two on the right is the same shape, just turned. Fold the answer key under before you start.") +
      "</p>" +
      '<div class="print-grid">' + cards + "</div>" +
      '<p class="print-key"><strong>Answer key</strong> — ' + key + "</p>";
  }

  global.CARDS = { mount: mount, svg: svg, shapes: Object.keys(SHAPES) };
})(window);
