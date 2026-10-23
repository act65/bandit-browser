// Settings graph (graph.html): Cytoscape.js, data embedded as JSON in the page.
// Node positions for the hierarchy and force layouts are computed when the site is built
// (site/layout.py); the browser only runs a layout for the small ?focus= neighbourhood view.
document.addEventListener("DOMContentLoaded", function () {
  var holder = document.getElementById("cy");
  var raw = document.getElementById("graph-data");
  if (!holder || !raw || !window.cytoscape) {
    if (holder) holder.textContent = "The graph needs JavaScript and cdnjs.cloudflare.com; see the settings index instead.";
    return;
  }
  if (window.cytoscapeDagre) cytoscape.use(cytoscapeDagre);
  var data = JSON.parse(raw.textContent);
  var hasDagre = !!window.dagre && !!window.cytoscapeDagre;

  var css = function (name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); };
  var colourKey = "sa";
  try { colourKey = localStorage.getItem("bb-colour") || "sa"; } catch (e) { /* ignore */ }
  var qcol = new URLSearchParams(window.location.search).get("colour");
  if (qcol === "sa" || qcol === "se" || qcol === "st") colourKey = qcol;
  if (colourKey === "st" && !document.querySelector('button[data-colour="st"]')) colourKey = "sa";

  var elements = [];
  data.nodes.forEach(function (n) {
    var total = n.up + n.lo;
    elements.push({ group: "nodes", position: { x: n.hx, y: n.hy }, data: Object.assign({}, n, {
      size: 14 + 7 * Math.sqrt(total), total: total,
      short: n.name.length > 52 ? n.name.slice(0, 51) + "…" : n.name
    }) });
  });
  data.edges.forEach(function (e, i) {
    elements.push({ group: "edges", data: Object.assign({ id: "e" + i, source: e.s, target: e.t }, e), classes: e.kind });
  });
  // Overview: groups of settings (environment x action space)
  (data.groups || []).forEach(function (g) {
    elements.push({ group: "nodes", classes: "grp", position: { x: g.x, y: g.y }, data: Object.assign({}, g, {
      size: 18 + 6 * Math.sqrt(g.results), total: g.results, short: g.name }) });
  });
  (data.gedges || []).forEach(function (e, i) {
    elements.push({ group: "edges", classes: "gedge", data: { id: "g" + i, source: e.s, target: e.t } });
  });

  var style = function () {
    var fg = css("--fg"), muted = css("--muted"), surface = css("--surface");
    var slot = function (ele) {
      if (colourKey === "st") return css("--st-" + (ele.data("st") || "none")) || css("--s0");
      return css("--s" + ele.data(colourKey)) || css("--s0");
    };
    return [
      { selector: "node", style: {
        "width": "data(size)", "height": "data(size)", "background-color": slot,
        "border-width": 2, "border-color": surface,
        "label": "", "font-size": 12, "color": muted, "text-valign": "bottom", "text-margin-y": 3,
        "text-wrap": "wrap", "text-max-width": 140, "min-zoomed-font-size": 6,
        "text-background-color": surface, "text-background-opacity": 0.7, "text-background-padding": 1
      } },
      { selector: "node[total >= 6]", style: { "label": "data(short)" } },
      { selector: "node[total = 0]", style: { "background-opacity": 0.45 } },
      { selector: "edge", style: { "width": 1.6, "line-color": css("--edge"), "curve-style": "bezier",
        "target-arrow-shape": "triangle", "target-arrow-color": css("--edge"), "arrow-scale": 0.9, "opacity": 0.85 } },
      { selector: "edge.reduction", style: { "line-style": "dashed" } },
      { selector: "edge.neighbour", style: { "width": 1, "line-color": css("--edge-faint"), "target-arrow-shape": "none", "opacity": 0.9 } },
      { selector: ".faded", style: { "opacity": 0.12 } },
      { selector: "node.hl", style: { "label": "data(short)", "border-color": fg, "border-width": 3, "color": fg, "font-weight": 600, "z-index": 10 } },
      { selector: "edge.hl", style: { "opacity": 1, "width": 2.4, "z-index": 9 } },
      { selector: "edge.neighbour.hl", style: { "line-color": muted } },
      // neighbourhood view (?focus=): every node labelled in full, with room to read it
      { selector: "node.local", style: { "label": "data(name)", "text-max-width": 150, "font-size": 12,
        "color": fg, "text-background-opacity": 0.85 } },
      { selector: "node.local.hl", style: { "font-weight": 700, "border-width": 4 } },
      { selector: "node.grp", style: { "label": "data(name)", "text-max-width": 170, "font-size": 20, "color": fg, "text-wrap": "wrap" } }
    ];
  };

  var cy = cytoscape({ container: holder, elements: elements, style: style(), wheelSensitivity: 0.25,
                       minZoom: 0.05, maxZoom: 3, layout: { name: "preset" } });
  var groupEls = cy.elements(".grp, .gedge");
  var settingEls = cy.elements().not(groupEls);
  var esc = function (s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; };

  var qv = new URLSearchParams(window.location.search);
  var focusSlug = qv.get("focus");
  var layoutName = qv.get("layout") === "cose" ? "cose" : "dagre";
  var view = (focusSlug || qv.get("view") === "all" || qv.get("layout")) ? "all" : "overview";
  var nbBox = document.getElementById("show-nb");

  // ---- state: filters (which settings are shown) and a selection (highlighted, survives hover)
  var hidden = { sa: {}, se: {} };
  var selection = null;
  var passes = function (n) { return !hidden.sa[n.data("sa")] && !hidden.se[n.data("se")]; };
  var showNb = function (on) {
    nbBox.checked = on;
    if (view === "all") cy.edges(".neighbour").style("display", on ? "element" : "none");
  };
  var countNote = document.getElementById("gf-count");
  var applyVisibility = function () {
    cy.batch(function () {
      if (view === "overview") {
        settingEls.style("display", "none");
        groupEls.nodes().forEach(function (g) { g.style("display", passes(g) ? "element" : "none"); });
        groupEls.edges().style("display", "element");
      } else {
        groupEls.style("display", "none");
        settingEls.nodes().forEach(function (n) { n.style("display", passes(n) ? "element" : "none"); });
        settingEls.edges().not(".neighbour").style("display", "element");
        showNb(nbBox.checked);
      }
    });
    if (countNote) {
      var all = view === "overview" ? groupEls.nodes() : settingEls.nodes();
      countNote.textContent = all.filter(":visible").length + " of " + all.length +
        (view === "overview" ? " groups shown" : " settings shown");
    }
  };
  var applyBase = function () {  // the resting highlight state: the selection, or nothing
    cy.batch(function () {
      cy.elements().removeClass("faded hl");
      if (selection && selection.length) {
        cy.elements().addClass("faded");
        var inner = selection.edgesWith(selection);
        selection.union(inner).removeClass("faded");
        selection.addClass("hl");
      }
    });
  };
  var select = function (nodes) { selection = nodes && nodes.length ? nodes : null; applyBase(); };
  var fitVisible = function (pad) {
    var vis = cy.elements(":visible");
    if (vis.length) cy.fit(vis, pad || 30);
  };

  var runLayout = function (name) {
    layoutName = name;
    showNb(name !== "dagre");  // the hierarchy reads best without the unordered links
    cy.batch(function () {
      settingEls.nodes().forEach(function (n) {
        var d = n.data();
        n.position(name === "dagre" ? { x: d.hx, y: d.hy } : { x: d.fx, y: d.fy });
      });
    });
    if (view === "all") fitVisible(24);
  };
  var setView = function (v) {
    view = v;
    document.querySelectorAll("button[data-view]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.view === v)); });
    document.querySelectorAll("button[data-layout], #show-nb").forEach(function (b) { b.disabled = v === "overview"; });
    applyVisibility();
    applyBase();
    fitVisible(v === "overview" ? 30 : 24);
  };

  // ---- filter checkboxes
  var boxes = document.querySelectorAll("input[data-f]");
  var syncBoxes = function () {
    boxes.forEach(function (b) { b.checked = !hidden[b.dataset.f][b.value]; });
  };
  boxes.forEach(function (b) {
    b.addEventListener("change", function () {
      hidden[b.dataset.f][b.value] = !b.checked;
      applyVisibility(); applyBase(); fitVisible();
    });
  });
  var setAll = function (key, on) {
    boxes.forEach(function (b) { if (b.dataset.f === key) hidden[key][b.value] = !on; });
    syncBoxes(); applyVisibility(); applyBase(); fitVisible();
  };
  document.querySelectorAll("a[data-all], a[data-none]").forEach(function (a) {
    a.addEventListener("click", function (ev) {
      ev.preventDefault();
      setAll(a.dataset.all || a.dataset.none, !!a.dataset.all);
    });
  });
  var onlyGroup = function (g) {  // show just a group's action space and environment
    ["sa", "se"].forEach(function (key) {
      boxes.forEach(function (b) { if (b.dataset.f === key) hidden[key][b.value] = String(g[key]) !== b.value; });
    });
    syncBoxes();
  };

  // ---- hover tooltip and transient highlight (on top of the selection)
  var tip = document.getElementById("cy-tip");
  var wrap = holder.parentElement;
  var showTip = function (html, pos) {
    tip.innerHTML = html;
    tip.hidden = false;
    var box = holder.getBoundingClientRect(), wbox = wrap.getBoundingClientRect();
    var x = pos.x + box.left - wbox.left + 14, y = pos.y + box.top - wbox.top + 14;
    x = Math.min(x, wbox.width - tip.offsetWidth - 4);
    tip.style.left = Math.max(0, x) + "px";
    tip.style.top = y + "px";
  };
  var STATUS_LABEL = { tight: "tight", log_gap: "log gap", poly_gap: "poly gap", no_lower: "no comparable lower bound",
                       no_upper: "no comparable upper bound", conflict: "conflict", none: "no comparable bounds" };
  var hoverHl = function (node) {
    var hood = node.closedNeighborhood();
    cy.batch(function () {
      if (!selection) cy.elements().addClass("faded");
      hood.removeClass("faded").addClass("hl");
    });
  };
  cy.on("mouseover", "node", function (ev) {
    var d = ev.target.data();
    holder.style.cursor = "pointer";
    if (ev.target.hasClass("grp")) {
      showTip("<b>" + esc(d.name) + "</b>" + d.n + " setting" + (d.n === 1 ? "" : "s") + " · " + d.results +
              " results<div class=\"muted\">click to show its settings</div>", ev.renderedPosition);
      return;
    }
    showTip("<b>" + esc(d.name) + "</b>" + d.up + " upper · " + d.lo + " lower · " + d.papers + " paper" + (d.papers === 1 ? "" : "s") +
            ((d.iu || d.il) ? '<div class="muted">+' + d.iu + " upper · +" + d.il + " lower inherited</div>" : "") +
            '<div class="muted">' + esc(d.action_space) + " · " + esc(d.environment) + "</div>" +
            (d.streg !== undefined && d.st ? '<div><span class="dot st-' + esc(d.st) + '"></span>' + esc(STATUS_LABEL[d.st] || d.st) +
             (d.streg ? ' <span class="muted">(' + esc(d.streg) + ")</span>" : "") + "</div>" : ""), ev.renderedPosition);
    if (!focusSlug) hoverHl(ev.target);
  });
  cy.on("mouseover", "edge", function (ev) {
    var d = ev.target.data();
    if (!d.dim) return;
    var kind = d.kind === "neighbour" ? "neighbours" : d.kind === "reduction" ? "reduction (special → general)" : "specialisation (special → general)";
    showTip("<b>" + esc(d.dim) + ": " + esc(d.from) + " → " + esc(d.to) + "</b>" + kind, ev.renderedPosition);
  });
  cy.on("mouseout", "node, edge", function () {
    tip.hidden = true;
    holder.style.cursor = "";
    if (!focusSlug) applyBase();
  });
  cy.on("tap", "node", function (ev) {
    var d = ev.target.data();
    if (ev.target.hasClass("grp")) {  // open the group: its settings, selected, other groups filtered out
      onlyGroup(d);
      setView("all");
      var hits = cy.nodes().filter(function (x) { return d.members.indexOf(x.id()) !== -1; });
      select(hits);
      if (hits.length) cy.fit(hits, 60);
      return;
    }
    window.location.href = d.url;
  });
  cy.on("tap", function (ev) { if (ev.target === cy && !focusSlug) select(null); });  // background clears

  // ---- ?focus=<slug> from a setting page: its neighbourhood only, laid out on its own
  if (focusSlug) {
    var n = cy.nodes().filter(function (x) { return x.data("slug") === focusSlug; });
    if (n.length) {
      var hood = n.closedNeighborhood();
      cy.elements().not(hood).style("display", "none");
      hood.style("display", "element");
      hood.nodes().addClass("local");
      n.addClass("hl");
      var lay = hasDagre
        ? { name: "dagre", rankDir: "BT", nodeSep: 24, rankSep: 110, edgeSep: 12, fit: true, padding: 40, animate: false,
            nodeDimensionsIncludeLabels: true }
        : { name: "concentric", fit: true, padding: 50, animate: false,
            concentric: function (x) { return x.same(n) ? 2 : 1; }, levelWidth: function () { return 1; } };
      hood.layout(lay).run();
      var note = document.createElement("p");
      note.className = "cy-local-note small";
      note.innerHTML = "Neighbourhood of <b>" + esc(n.data("name")) + "</b>: arrows point from special cases up to " +
        "more general settings. <a href=\"graph.html\">Show the full graph →</a>";
      holder.parentElement.parentElement.insertBefore(note, holder.parentElement);
      document.querySelectorAll("button[data-layout], button[data-view], input[data-f]").forEach(function (b) { b.disabled = true; });
    } else {
      focusSlug = null;
    }
  }

  // ---- controls
  var bind = function (sel, attr, fn) {
    var btns = document.querySelectorAll(sel);
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        fn(b.getAttribute(attr));
      });
    });
    return btns;
  };
  var setColour = function (key) {
    colourKey = key;
    document.getElementById("legend-sa").hidden = key !== "sa";
    document.getElementById("legend-se").hidden = key !== "se";
    var lst = document.getElementById("legend-st");
    if (lst) lst.hidden = key !== "st";
    cy.style(style());
    try { localStorage.setItem("bb-colour", key); } catch (e) { /* ignore */ }
  };
  bind("button[data-colour]", "data-colour", setColour).forEach(function (x) {
    x.setAttribute("aria-pressed", String(x.dataset.colour === colourKey));
  });
  setColour(colourKey);
  bind("button[data-layout]", "data-layout", runLayout).forEach(function (x) {
    x.setAttribute("aria-pressed", String(x.dataset.layout === layoutName));
  });
  nbBox.addEventListener("change", function (ev) { showNb(ev.target.checked); });
  bind("button[data-view]", "data-view", setView);
  if (!focusSlug) {
    runLayout(layoutName);
    setView(view);
  } else {
    document.querySelectorAll("button[data-view]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.view === "all"));
    });
  }
  window.addEventListener("load", function () {
    cy.resize();
    if (focusSlug) cy.fit(cy.elements(":visible"), 50); else fitVisible();
  });
  document.getElementById("graph-search").addEventListener("input", function (ev) {
    var q = ev.target.value.toLowerCase().trim();
    if (!q) { select(null); return; }
    var pool = view === "overview" ? groupEls.nodes() : settingEls.nodes();
    select(pool.filter(function (x) { return x.visible() && x.data("name").toLowerCase().indexOf(q) !== -1; }));
  });

  // Follow the colour scheme
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    var onChange = function () { cy.style(style()); };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
  }
});
