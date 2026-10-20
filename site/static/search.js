// Faceted search (search.html) over window.BB_SEARCH (static/search-data.js, written by site/build.py).
// State lives in the URL hash: #mode=bounds&side=lower&origin=inherited&ymin=2015 …
document.addEventListener("DOMContentLoaded", function () {
  var root = document.getElementById("search");
  var D = window.BB_SEARCH;
  if (!root) return;
  if (!D) { root.innerHTML = '<p class="notice">No search index (static/search-data.js).</p>'; return; }
  var S = D.settings, B = D.bounds;
  var h = function (tag, cls, parent, text) {
    var x = document.createElement(tag);
    if (cls) x.className = cls;
    if (text != null) x.textContent = text;
    if (parent) parent.appendChild(x);
    return x;
  };
  var lab = function (dim, v) { return (D.labels[dim] && D.labels[dim][v]) || String(v).replace(/_/g, " "); };
  var DIMLAB = { environment: "Environment", action_space: "Action space", feedback: "Feedback", context: "Context",
                 noise: "Noise", objective: "Objective", function_class: "Function class",
                 instance_assumptions: "Instance assumptions", extras: "Extras" };

  // Facet definitions. kind: "s" = setting facet, "b" = bound facet. get returns a list of values.
  var regLab = function (r) { return D.regimes[r] || r; };
  var stLab = function (s) { return D.status[s] || s; };
  var facets = [];
  Object.keys(DIMLAB).forEach(function (d) {
    facets.push({ key: d, label: DIMLAB[d], kind: "s", get: function (s) { return s.f[d] || []; }, show: function (v) { return lab(d, v); } });
  });
  facets.push({ key: "regime", label: "Regime (for status)", kind: "s", single: true, get: function (s) { return Object.keys(s.cells); }, show: regLab });
  facets.push({ key: "cell", label: "Status", kind: "s", show: stLab, get: function (s, st) {
    var r = st.regime && st.regime.length ? st.regime : null;
    return Object.keys(s.cells).filter(function (k) { return !r || r.indexOf(k) !== -1; }).map(function (k) { return s.cells[k]; });
  } });
  facets.push({ key: "upSrc", label: "Upper bounds", kind: "s", get: function (s) { return [s.upSrc]; }, show: function (v) { return v === "inherited" ? "inherited only" : v; } });
  facets.push({ key: "loSrc", label: "Lower bounds", kind: "s", get: function (s) { return [s.loSrc]; }, show: function (v) { return v === "inherited" ? "inherited only" : v; } });
  var bf = [
    ["side", "Side", function (b) { return b.side; }],
    ["reg", "Quantity · dependence", function (b) { return b.reg; }, regLab],
    ["nota", "Notation", function (b) { return b.nota; }],
    ["origin", "Own / inherited", function (b) { return b.inh ? "inherited" : "own"; }],
    ["af", "Algorithm family", function (b) { return b.af; }],
    ["conf", "Confidence", function (b) { return b.conf; }],
    ["rs", "Instance class", function (b) { return b.rs ? "restricted" : "unrestricted"; }],
    ["paper", "Paper", function (b) { return b.p; }, function (v) { return paperCite[v] || v; }]
  ];
  var paperCite = {};
  B.forEach(function (b) { paperCite[b.p] = b.c + " · " + b.p; });
  bf.forEach(function (x) {
    facets.push({ key: x[0], label: x[1], kind: "b", get: function (b) { return [x[2](b)]; }, show: x[3] || function (v) { return String(v).replace(/_/g, " "); } });
  });

  // ------------------------------------------------------------ state
  var st = {};
  var mode = "settings", ymin = "", ymax = "", text = "";
  var readHash = function () {
    var q = new URLSearchParams(window.location.hash.slice(1));
    st = {};
    facets.forEach(function (f) { var v = q.get(f.key); if (v) st[f.key] = v.split(","); });
    mode = q.get("mode") === "bounds" ? "bounds" : "settings";
    ymin = q.get("ymin") || ""; ymax = q.get("ymax") || ""; text = q.get("q") || "";
  };
  var writeHash = function () {
    var parts = ["mode=" + mode];
    facets.forEach(function (f) { if (st[f.key] && st[f.key].length) parts.push(f.key + "=" + st[f.key].map(encodeURIComponent).join(",")); });
    if (ymin) parts.push("ymin=" + ymin);
    if (ymax) parts.push("ymax=" + ymax);
    if (text) parts.push("q=" + encodeURIComponent(text));
    history.replaceState(null, "", "#" + parts.join("&"));
  };

  var anyB = function () {
    return ymin || ymax || facets.some(function (f) { return f.kind === "b" && st[f.key] && st[f.key].length; });
  };
  var passF = function (f, item, skip) {
    if (f.key === skip) return true;
    var want = st[f.key];
    if (!want || !want.length) return true;
    var have = f.get(item, st);
    return want.some(function (w) { return have.indexOf(w) !== -1; });
  };
  var passB = function (b, skip) {
    if (ymin && !(b.y >= Number(ymin))) return false;
    if (ymax && !(b.y <= Number(ymax))) return false;
    return facets.every(function (f) { return f.kind !== "b" || passF(f, b, skip); });
  };
  var passS = function (s, skip) {
    if (text && (s.name + " " + s.id).toLowerCase().indexOf(text.toLowerCase()) === -1) return false;
    return facets.every(function (f) { return f.kind !== "s" || passF(f, s, skip); });
  };
  var matchBySetting = function (skip) {
    var m = {};
    B.forEach(function (b) { if (passB(b, skip)) m[b.s] = (m[b.s] || 0) + 1; });
    return m;
  };

  // ------------------------------------------------------------ layout
  root.innerHTML = "";
  var top = h("div", "toolbar", root);
  var seg = h("div", "seg", top);
  h("span", "", seg, "Results");
  var mb = {};
  ["settings", "bounds"].forEach(function (m) {
    var b = h("button", "", seg, m === "settings" ? "Settings" : "Bounds");
    b.type = "button";
    b.addEventListener("click", function () { mode = m; run(); });
    mb[m] = b;
  });
  var tbox = h("input", "filter", top);
  tbox.type = "search"; tbox.placeholder = "Setting name contains…"; tbox.setAttribute("aria-label", "Setting name");
  tbox.addEventListener("input", function () { text = tbox.value.trim(); run(); });
  var clear = h("button", "linkbtn", top, "clear all");
  clear.type = "button";
  clear.addEventListener("click", function () { st = {}; ymin = ymax = text = ""; tbox.value = ""; run(); });
  var layout = h("div", "search-grid", root);
  var side = h("aside", "facets", layout);
  var main = h("div", "results-pane", layout);

  var narrow = window.matchMedia && window.matchMedia("(max-width: 760px)").matches;
  var LIMIT = 100;
  var shownLimit = LIMIT;
  var run = function () {
    writeHash();
    mb.settings.setAttribute("aria-pressed", String(mode === "settings"));
    mb.bounds.setAttribute("aria-pressed", String(mode === "bounds"));
    renderFacets();
    renderResults();
  };

  var renderFacets = function () {
    side.innerHTML = "";
    var groups = [["Settings", "s"], ["Bounds", "b"]];
    groups.forEach(function (g) {
      h("h3", "fgroup", side, g[0]);
      facets.filter(function (f) { return f.kind === g[1]; }).forEach(function (f) {
        // counts: items passing every other facet
        var counts = {};
        if (f.kind === "s") {
          var mbs = anyB() ? matchBySetting(null) : null;
          S.forEach(function (s, i) {
            if (mbs && !mbs[i]) return;
            if (!passS(s, f.key)) return;
            var seen = {};
            f.get(s, st).forEach(function (v) { if (!seen[v]) { seen[v] = 1; counts[v] = (counts[v] || 0) + 1; } });
          });
        } else {
          var okS = {};
          S.forEach(function (s, i) { okS[i] = passS(s, null); });
          B.forEach(function (b) {
            if (!okS[b.s] || !passB(b, f.key)) return;
            f.get(b).forEach(function (v) { counts[v] = (counts[v] || 0) + 1; });
          });
        }
        var sel = st[f.key] || [];
        var vals = Object.keys(counts);
        sel.forEach(function (v) { if (vals.indexOf(v) === -1) vals.push(v); });
        if (!vals.length) return;
        vals.sort(function (a, b) { return (counts[b] || 0) - (counts[a] || 0) || (a < b ? -1 : 1); });
        var det = h("details", "facet", side);
        det.open = sel.length > 0 || (!narrow && ["environment", "action_space", "cell", "side", "reg", "origin"].indexOf(f.key) !== -1);
        var sm = h("summary", "", det, f.label);
        if (sel.length) h("span", "badge", sm, String(sel.length));
        var ul = h("ul", vals.length > 10 ? "long" : "", det);
        vals.forEach(function (v) {
          var li = h("li", "", ul);
          var l = h("label", "", li);
          var cb = h("input", "", l);
          cb.type = "checkbox";
          cb.checked = sel.indexOf(v) !== -1;
          cb.addEventListener("change", function () {
            var cur = st[f.key] || [];
            if (f.single) cur = [];
            cur = cur.filter(function (x) { return x !== v; });
            if (cb.checked) cur.push(v);
            st[f.key] = cur;
            shownLimit = LIMIT;
            run();
          });
          h("span", "", l, f.show(v));
          h("span", "fc", l, String(counts[v] || 0));
        });
      });
      if (g[1] === "b") {
        var det = h("details", "facet", side);
        det.open = !!(ymin || ymax);
        h("summary", "", det, "Year");
        var row = h("div", "years", det);
        var mk = function (val, ph, set) {
          var i = h("input", "", row);
          i.type = "number"; i.placeholder = ph; i.value = val; i.min = 1950; i.max = 2100;
          i.addEventListener("change", function () { set(i.value); run(); });
        };
        mk(ymin, "from", function (v) { ymin = v; });
        h("span", "muted", row, "–");
        mk(ymax, "to", function (v) { ymax = v; });
      }
    });
  };

  var tex = function (node, s) {
    if (window.katex && s) { try { katex.render(s, node, { throwOnError: false, strict: "ignore" }); return; } catch (e) { /* fall through */ } }
    node.textContent = s || "";
  };
  var stBadge = function (parent, s) { h("span", "badge st st-" + s, parent, stLab(s)); };

  var renderResults = function () {
    main.innerHTML = "";
    var mbs = anyB() ? matchBySetting(null) : null;
    if (mode === "settings") {
      var rows = [];
      S.forEach(function (s, i) { if ((!mbs || mbs[i]) && passS(s, null)) rows.push([s, i]); });
      h("p", "small muted", main, rows.length + " of " + S.length + " settings" + (mbs ? " (with at least one matching bound)" : ""));
      if (!rows.length) return;
      var wrap = h("div", "scroll", main);
      var t = h("table", "searchres", wrap);
      var hr = h("tr", "", h("thead", "", t));
      ["Setting", "Status by regime", mbs ? "Matching bounds" : "Papers"].forEach(function (x) { h("th", "", hr, x); });
      var tb = h("tbody", "", t);
      rows.slice(0, shownLimit).forEach(function (r) {
        var s = r[0];
        var tr = h("tr", "", tb);
        var a = h("a", "", h("td", "", tr), s.name);
        a.href = "settings/" + s.slug + ".html#rates";
        var td = h("td", "stcells", tr);
        Object.keys(s.cells).sort(function (a, b) { return (b === "regret|worst_case") - (a === "regret|worst_case") || (a < b ? -1 : 1); })
          .forEach(function (k) {
            var span = h("span", "stc", td);
            stBadge(span, s.cells[k]);
            h("span", "muted", span, " " + regLab(k));
          });
        if (!Object.keys(s.cells).length) h("span", "muted small", td, "no comparable bounds");
        h("td", "num", tr, String(mbs ? mbs[r[1]] : s.papers));
      });
      more(rows.length);
    } else {
      var okS = {};
      S.forEach(function (s, i) { okS[i] = passS(s, null); });
      var bs = B.filter(function (b) { return okS[b.s] && passB(b, null); });
      h("p", "small muted", main, bs.length + " of " + B.length + " bounds");
      if (!bs.length) return;
      var wrap2 = h("div", "scroll", main);
      var t2 = h("table", "searchres", wrap2);
      var hr2 = h("tr", "", h("thead", "", t2));
      ["Setting", "Bound", "Regime", "Paper · algorithm"].forEach(function (x) { h("th", "", hr2, x); });
      var tb2 = h("tbody", "", t2);
      bs.slice(0, shownLimit).forEach(function (b) {
        var s = S[b.s];
        var tr = h("tr", "", tb2);
        var a = h("a", "", h("td", "c-setting", tr), s.name);
        a.href = "settings/" + s.slug + ".html#rates";
        var td = h("td", "c-bound", tr);
        var f = h("div", "formula", td);
        if (b.t) tex(f, b.t); else h("code", "", f, b.e || "");
        var bd = h("div", "badges", td);
        h("span", "badge " + (b.side === "upper" ? "inst" : "worst"), bd, b.side);
        if (b.inh) h("span", "badge inh", bd, "inherited");
        if (b.conf === "low" || b.conf === "medium") h("span", "badge conf-" + b.conf, bd, b.conf + " confidence");
        if (b.rs) h("span", "badge muted-badge", bd, "restricted instances");
        h("td", "small", tr, regLab(b.reg));
        var tdp = h("td", "small", tr);
        var pa = h("a", "", tdp, b.c);
        pa.href = "papers/" + b.p.toLowerCase().replace(/[^a-z0-9_.-]+/g, "-") + ".html";
        if (b.a) h("div", "muted", tdp, b.a);
        if (b.af && b.af !== "none") h("div", "muted", tdp, b.af.replace(/_/g, " "));
      });
      more(bs.length);
    }
  };
  var more = function (n) {
    if (n <= shownLimit) return;
    var b = h("button", "linkbtn", main, "show " + Math.min(LIMIT, n - shownLimit) + " more (" + (n - shownLimit) + " hidden)");
    b.type = "button";
    b.addEventListener("click", function () { shownLimit += LIMIT; renderResults(); });
  };

  readHash();
  tbox.value = text;
  run();
  window.addEventListener("hashchange", function () {
    readHash(); tbox.value = text; shownLimit = LIMIT; run();
  });
});
