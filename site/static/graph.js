// Settings graph (graph.html): Cytoscape.js + dagre, data embedded as JSON in the page.
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
    elements.push({ group: "nodes", data: Object.assign({}, n, {
      size: 14 + 7 * Math.sqrt(total), total: total,
      short: n.name.length > 52 ? n.name.slice(0, 51) + "…" : n.name
    }) });
  });
  data.edges.forEach(function (e, i) {
    elements.push({ group: "edges", data: Object.assign({ id: "e" + i, source: e.s, target: e.t }, e), classes: e.kind });
  });
  // Overview: groups of settings (objective x environment x action space x feedback)
  (data.groups || []).forEach(function (g) {
    elements.push({ group: "nodes", classes: "grp", data: Object.assign({}, g, {
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
      { selector: "node.grp", style: { "label": "data(name)", "text-max-width": 150, "font-size": 12, "color": fg } }
    ];
  };

  var cy = cytoscape({ container: holder, elements: elements, style: style(), wheelSensitivity: 0.25,
                       minZoom: 0.15, maxZoom: 3 });
  var groupEls = cy.elements(".grp, .gedge");
  var settingEls = cy.elements().not(groupEls);

  var layoutName = hasDagre ? "dagre" : "cose";
  var qv = new URLSearchParams(window.location.search);
  var view = (qv.get("focus") || qv.get("view") === "all" || qv.get("layout")) ? "all" : "overview";
  var qs = new URLSearchParams(window.location.search);
  if (qs.get("layout") === "cose" || qs.get("layout") === "dagre") layoutName = qs.get("layout");
  var nbBox = document.getElementById("show-nb");
  var showNb = function (on) {
    nbBox.checked = on;
    if (view === "all") cy.edges(".neighbour").style("display", on ? "element" : "none");
  };
  var runLayout = function (name) {
    layoutName = name;
    showNb(name !== "dagre");  // the hierarchy reads best without the unordered links
    var opts;
    if (name === "dagre" && hasDagre) {
      // Rank by specialisation edges only; neighbour edges just come along for the ride.
      // Settings with no specialisation edge go in a grid beside the hierarchy.
      var directed = settingEls.edges().not(".neighbour");
      var ranked = directed.connectedNodes();
      var loose = settingEls.nodes().not(ranked);
      opts = { name: "dagre", rankDir: "BT", nodeSep: 22, rankSep: 64, edgeSep: 8, ranker: "network-simplex",
               fit: false, animate: false };
      ranked.union(directed).layout(opts).run();
      var bb = ranked.boundingBox();
      var cols = Math.max(2, Math.ceil(Math.sqrt(loose.length * 0.6)));
      var cell = 70;
      loose.sort(function (a, b) { return b.data("total") - a.data("total"); }).forEach(function (n, i) {
        n.position({ x: bb.x2 + 90 + (i % cols) * cell, y: bb.y1 + Math.floor(i / cols) * cell });
      });
      cy.fit(settingEls, 24);
    } else {
      settingEls.layout({ name: "cose", animate: false, nodeRepulsion: function () { return 9000; },
                  idealEdgeLength: function (e) { return e.hasClass("neighbour") ? 90 : 60; },
                  edgeElasticity: function (e) { return e.hasClass("neighbour") ? 60 : 160; },
                  gravity: 0.6, numIter: 2500, padding: 24, randomize: true }).run();
    }
  };
  runLayout(layoutName);
  // Overview layout (computed once): dagre over the group graph, labels counted in spacing
  if (groupEls.length) {
    groupEls.layout(hasDagre
      ? { name: "dagre", rankDir: "BT", nodeSep: 30, rankSep: 90, edgeSep: 10, fit: false, animate: false,
          nodeDimensionsIncludeLabels: true }
      : { name: "cose", animate: false, fit: false }).run();
  }
  var setView = function (v) {
    view = v;
    document.querySelectorAll("button[data-view]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.view === v)); });
    document.querySelectorAll("button[data-layout], #show-nb").forEach(function (b) { b.disabled = v === "overview"; });
    if (v === "overview") {
      settingEls.style("display", "none");
      groupEls.style("display", "element");
      cy.fit(groupEls, 30);
    } else {
      groupEls.style("display", "none");
      settingEls.style("display", "element");
      showNb(nbBox.checked);
      cy.fit(settingEls, 24);
    }
  };
  window.addEventListener("load", function () {
    cy.resize();
    cy.fit(cy.elements(":visible"), focused ? 50 : 30);
  });

  // Hover tooltip
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
  var esc = function (s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; };
  cy.on("mouseover", "node", function (ev) {
    var d = ev.target.data();
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
    highlight(ev.target);
  });
  cy.on("mouseover", "edge", function (ev) {
    var d = ev.target.data();
    var kind = d.kind === "neighbour" ? "neighbours" : d.kind === "reduction" ? "reduction (special → general)" : "specialisation (special → general)";
    showTip("<b>" + esc(d.dim) + ": " + esc(d.from) + " → " + esc(d.to) + "</b>" + kind, ev.renderedPosition);
  });
  cy.on("mouseout", "node, edge", function () {
    tip.hidden = true;
    if (!focused) clearHl();
    else { cy.elements().removeClass("faded"); focused.addClass("hl"); }
  });
  cy.on("tap", "node", function (ev) {
    var d = ev.target.data();
    if (ev.target.hasClass("grp")) {  // open the group: all settings, its members highlighted
      setView("all");
      var hits = cy.nodes().filter(function (x) { return d.members.indexOf(x.id()) !== -1; });
      cy.elements().addClass("faded");
      hits.removeClass("faded").addClass("hl");
      focused = hits;
      cy.fit(hits, 60);
      return;
    }
    window.location.href = d.url;
  });
  cy.on("mouseover", "node", function () { holder.style.cursor = "pointer"; });
  cy.on("mouseout", "node", function () { holder.style.cursor = ""; });

  var focused = null;
  var visibleHood = function (n) { return n.union(n.connectedEdges(":visible").connectedNodes()); };
  var clearHl = function () { cy.elements().removeClass("faded hl"); };
  var highlight = function (node) {
    var hood = node.closedNeighborhood();
    cy.elements().addClass("faded");
    hood.removeClass("faded").addClass("hl");
  };

  // ?focus=<slug> from a setting page
  var params = new URLSearchParams(window.location.search);
  var focusSlug = params.get("focus");
  if (focusSlug) {
    var n = cy.nodes().filter(function (x) { return x.data("slug") === focusSlug; });
    if (n.length) {
      // Neighbourhood view: only the setting and its immediate covers / neighbours, laid out
      // on their own so that every label is readable. The full graph is one click away.
      focused = n;
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
      document.querySelectorAll("button[data-layout]").forEach(function (b) { b.disabled = true; });
    }
  }

  // Controls
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
  if (!focusSlug) setView(view);
  else document.querySelectorAll("button[data-view]").forEach(function (b) {
    b.setAttribute("aria-pressed", String(b.dataset.view === "all"));
  });
  document.getElementById("graph-search").addEventListener("input", function (ev) {
    var q = ev.target.value.toLowerCase().trim();
    focused = null;
    clearHl();
    if (!q) return;
    var hits = cy.nodes().filter(function (x) { return x.data("name").toLowerCase().indexOf(q) !== -1; });
    cy.elements().addClass("faded");
    hits.removeClass("faded").addClass("hl");
    if (hits.length) focused = hits;
  });

  // Follow the colour scheme
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    var onChange = function () { cy.style(style()); };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
  }
});
