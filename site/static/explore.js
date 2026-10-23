// Explore (explore.html): Settings, Papers, Bounds and Gaps as SQL queries over the atlas database
// (static/db.js). Each tab is a query spec: a FROM clause, facet columns, a text search, sort
// orders and a row renderer. One engine builds the WHERE clause, the facet counts (each facet
// counted under all the other filters) and the paging. State lives in the URL hash, e.g.
// #tab=gaps&status=log_gap,poly_gap&environment=stochastic_iid&q=linear&page=2
(function () {
  var esc = function (s) { return window.bbEsc(s); };
  var PAGE = 50;
  var LAB = {};  // dim -> value -> label (labels table)
  var lab = function (dim, v) {
    if (v == null || v === "") return "none";
    return (LAB[dim] && LAB[dim][v]) || String(v).replace(/_/g, " ");
  };
  var SUP = { ".": "·", "-": "⁻" };
  var sup = function (x) { return String(x).replace(/[0-9.\-]/g, function (c) { return SUP[c] || "⁰¹²³⁴⁵⁶⁷⁸⁹".charAt(+c); }); };
  var rate = function (s) {  // "0.5·log^0.5" -> "0.5 log^0.5", "0·log^1" -> "log¹"
    if (s == null) return "–";
    var p = String(s).split("·log^"), a = parseFloat(p[0]), b = p[1];
    var at = isNaN(a) ? p[0] : (a === 0 && b ? "" : String(+a.toFixed(3)));
    var lg = b && b !== "0" ? "log" + sup(b) : "";
    return [at, lg].filter(Boolean).join(" ") || "0";
  };
  var STATUS_RANK = "CASE c.status WHEN 'conflict' THEN 0 WHEN 'poly_gap' THEN 1 WHEN 'log_gap' THEN 2 " +
                    "WHEN 'no_lower' THEN 3 WHEN 'no_upper' THEN 4 WHEN 'tight' THEN 5 ELSE 6 END";
  var tex = function (t, fallback) {
    if (t) return '<span class="math ex-tex" data-tex="' + esc(t) + '">' + esc(t) + "</span>";
    return fallback ? "<code>" + esc(fallback) + "</code>" : '<span class="muted">–</span>';
  };
  var settingLink = function (slug, name) { return '<a href="setting.html?s=' + encodeURIComponent(slug) + '">' + esc(name) + "</a>"; };
  var paperLink = function (slug, cite, title) {
    return slug ? '<a href="paper.html?p=' + encodeURIComponent(slug) + '" title="' + esc(title || "") + '">' + esc(cite || slug) + "</a>" : "";
  };
  var statusBadge = function (st) { return '<span class="badge st st-' + esc(st || "none") + '">' + esc(lab("status", st || "none")) + "</span>"; };
  var countCell = function (own, inh) { return "<b>" + own + "</b>" + (inh ? ' <span class="muted">+' + inh + "</span>" : ""); };

  var dimFacet = function (key, label, table, multi) {
    return { key: key, label: label, col: table + "." + key, dim: key, multi: !!multi };
  };
  var TABS = {
    settings: {
      label: "Settings", what: "settings",
      from: "settings s",
      text: { fts: "settings_fts", col: "s.slug" },
      facets: [
        dimFacet("environment", "Environment", "s"), dimFacet("action_space", "Action space", "s"),
        dimFacet("feedback", "Feedback", "s"), dimFacet("objective", "Objective", "s"), dimFacet("noise", "Noise", "s"),
        dimFacet("context", "Context", "s"), dimFacet("function_class", "Function class", "s", true),
        dimFacet("instance_assumptions", "Instance assumptions", "s", true), dimFacet("extras", "Extras", "s", true),
        dimFacet("learner_knows", "Learner knows", "s", true),
        { key: "status", label: "Status (most relevant regime)", col: "s.status", dim: "status" },
        { key: "up_src", label: "Upper bounds", col: "s.up_src", dim: "src" },
        { key: "lo_src", label: "Lower bounds", col: "s.lo_src", dim: "src" }
      ],
      select: "s.slug, s.name, s.environment, s.action_space, s.n_papers, s.n_upper, s.n_lower, s.n_inh_upper, s.n_inh_lower, s.status, s.status_regime",
      sorts: [["papers", "most papers", "s.n_papers DESC, (s.n_upper + s.n_lower) DESC, s.name"],
              ["bounds", "most bounds", "(s.n_upper + s.n_lower + s.n_inh_upper + s.n_inh_lower) DESC, s.name"],
              ["name", "name", "s.name"]],
      head: ["Setting", "Papers", "Upper", "Lower", "Status"],
      row: function (r) {
        return [settingLink(r.slug, r.name) + '<div class="muted small">' + esc(lab("environment", r.environment)) + " · " +
                esc(lab("action_space", r.action_space)) + "</div>",
                r.n_papers, countCell(r.n_upper, r.n_inh_upper), countCell(r.n_lower, r.n_inh_lower),
                statusBadge(r.status) + (r.status_regime ? '<div class="muted small">' + esc(lab("regime", r.status_regime)) + "</div>" : "")];
      }
    },
    papers: {
      label: "Papers", what: "papers",
      from: "papers p",
      text: { fts: "papers_fts", col: "p.slug" },
      facets: [
        { key: "period", label: "Period", col: "CASE WHEN p.year IS NULL THEN 'unknown' WHEN p.year < 2000 THEN 'before 2000' ELSE (p.year / 5 * 5) || '–' || (p.year / 5 * 5 + 4) END" },
        { key: "extracted", label: "Extracted", col: "CASE p.extracted WHEN 1 THEN 'yes' ELSE 'no' END" },
        { key: "has_results", label: "Results", col: "CASE WHEN p.n_results > 0 THEN 'some' ELSE 'none' END" }
      ],
      select: "p.slug, p.cite, p.title, p.authors, p.year, p.venue, p.n_settings, p.n_results",
      sorts: [["year", "newest", "p.year DESC, p.cite"], ["oldest", "oldest", "p.year, p.cite"],
              ["results", "most results", "p.n_results DESC, p.year DESC"], ["cite", "author", "p.cite"]],
      head: ["Paper", "Year", "Settings", "Results"],
      row: function (r) {
        return [paperLink(r.slug, r.cite, r.title) + '<div class="small">' + esc(r.title) + "</div>" +
                (r.venue ? '<div class="muted small">' + esc(r.venue) + "</div>" : ""),
                r.year || "", r.n_settings, r.n_results];
      }
    },
    bounds: {
      label: "Bounds", what: "bounds",
      from: "bounds b JOIN settings s ON s.id = b.setting_id",
      text: { like: ["s.name", "b.algorithm", "b.cite", "b.paper_id"] },
      facets: [
        { key: "side", label: "Side", col: "b.side" },
        { key: "regime", label: "Quantity · dependence", col: "b.regime", dim: "regime" },
        { key: "origin", label: "Own / inherited", col: "CASE b.inherited WHEN 1 THEN 'inherited' ELSE 'own' END" },
        { key: "in_rate", label: "Used for the rate", col: "CASE b.in_rate WHEN 1 THEN 'yes' ELSE 'no (restricted, algorithm-specific, ...)' END" },
        { key: "notation", label: "Notation", col: "b.notation" },
        { key: "algorithm_family", label: "Algorithm family", col: "b.algorithm_family" },
        { key: "confidence", label: "Extraction confidence", col: "b.confidence" },
        dimFacet("environment", "Environment", "s"), dimFacet("action_space", "Action space", "s")
      ],
      defaults: { origin: ["own"] },
      select: "b.id, b.side, b.regime, b.inherited, b.tex, b.expr, b.cite, b.paper_id, b.algorithm, b.year, s.slug, s.name",
      sorts: [["setting", "setting", "s.n_papers DESC, s.name, b.side DESC, b.regime"], ["newest", "newest", "b.year DESC, s.name"],
              ["oldest", "oldest", "b.year, s.name"]],
      head: ["Bound", "Setting", "Paper", "Algorithm"],
      row: function (r) {
        return ['<span class="badge ' + (r.side === "upper" ? "worst" : "inst") + '">' + esc(r.side) + "</span> " +
                tex(r.tex, r.expr) + '<div class="muted small">' + esc(lab("regime", r.regime)) + (r.inherited ? " · inherited" : "") + "</div>",
                settingLink(r.slug, r.name), paperLink(r.paper_id, r.cite) + (r.year ? ' <span class="muted">' + r.year + "</span>" : ""),
                esc(r.algorithm || "")];
      }
    },
    gaps: {
      label: "Gaps", what: "setting × regime cells",
      from: "cells c JOIN settings s ON s.id = c.setting_id",
      text: { fts: "settings_fts", col: "s.slug" },
      facets: [
        { key: "status", label: "Status", col: "c.status", dim: "status" },
        { key: "regime", label: "Quantity · dependence", col: "c.regime", dim: "regime" },
        { key: "triage", label: "Gap triage", col: "COALESCE(c.triage, 'untriaged')" },
        { key: "relies", label: "Rests on inherited bounds", col: "CASE c.relies_inherited WHEN 1 THEN 'yes' ELSE 'no' END" },
        dimFacet("environment", "Environment", "s"), dimFacet("action_space", "Action space", "s"),
        dimFacet("feedback", "Feedback", "s")
      ],
      defaults: { status: ["conflict", "poly_gap", "log_gap"] },
      select: "s.slug, s.name, s.n_papers, c.regime, c.status, c.per_var, c.up_tex, c.lo_tex, c.up_cite, c.lo_cite, c.triage",
      sorts: [["status", "gap size, then papers", STATUS_RANK + ", s.n_papers DESC, s.name"],
              ["papers", "most papers", "s.n_papers DESC, " + STATUS_RANK]],
      head: ["Setting · regime", "Status · triage", "Rates (↑ upper ↓ lower)", "Best bounds"],
      row: function (r) {
        var pv = {};
        try { pv = JSON.parse(r.per_var || "{}"); } catch (e) { /* ignore */ }
        var rates = Object.keys(pv).map(function (v) {
          var x = pv[v], sym = { Delta: "1/Δ", delta: "1/δ", epsilon: "1/ε" }[v] || v;
          return '<span class="pv pv-' + esc(x.status || "") + '"><b>' + esc(sym) + "</b> ↑" + esc(rate(x.upper)) + " ↓" + esc(rate(x.lower)) + "</span>";
        }).join("");
        return [settingLink(r.slug, r.name) + '<div class="muted small">' + esc(lab("regime", r.regime)) + " · " + r.n_papers + " paper" + (r.n_papers === 1 ? "" : "s") + "</div>",
                statusBadge(r.status) + "<div>" + (r.triage ? '<span class="badge tri tri-' + esc(r.triage) + '">' + esc(r.triage.replace(/_/g, " ")) + "</span>"
                                                    : '<span class="badge muted-badge">untriaged</span>') + "</div>",
                '<div class="pvs">' + rates + "</div>",
                '<div class="ex-best"><span class="muted">↑</span> ' + tex(r.up_tex) + (r.up_cite ? ' <span class="muted small">' + esc(r.up_cite) + "</span>" : "") +
                '</div><div class="ex-best"><span class="muted">↓</span> ' + tex(r.lo_tex) + (r.lo_cite ? ' <span class="muted small">' + esc(r.lo_cite) + "</span>" : "") + "</div>"];
      }
    }
  };
  var ORDER = ["settings", "papers", "bounds", "gaps"];

  // ------------------------------------------------------------ state <-> URL hash
  var st;
  var readHash = function () {
    var q = new URLSearchParams(window.location.hash.slice(1));
    var tab = TABS[q.get("tab")] ? q.get("tab") : "settings";
    var spec = TABS[tab], f = {};
    spec.facets.forEach(function (x) { var v = q.get(x.key); if (v) f[x.key] = v.split(","); });
    if (!q.has("custom")) Object.keys(spec.defaults || {}).forEach(function (k) { if (!f[k]) f[k] = spec.defaults[k].slice(); });
    st = { tab: tab, f: f, q: q.get("q") || "", sort: q.get("sort") || spec.sorts[0][0], page: Math.max(1, +q.get("page") || 1) };
  };
  var writeHash = function () {
    var q = new URLSearchParams();
    q.set("tab", st.tab);
    Object.keys(st.f).forEach(function (k) { if (st.f[k].length) q.set(k, st.f[k].join(",")); });
    q.set("custom", "1");  // defaults applied once; afterwards the hash says exactly what is selected
    if (st.q) q.set("q", st.q);
    if (st.sort !== TABS[st.tab].sorts[0][0]) q.set("sort", st.sort);
    if (st.page > 1) q.set("page", st.page);
    history.replaceState(null, "", "#" + q.toString());
  };

  // ------------------------------------------------------------ SQL
  var where = function (spec, skipKey) {
    var parts = [], params = [];
    spec.facets.forEach(function (x) {
      var vals = st.f[x.key];
      if (!vals || !vals.length || x.key === skipKey) return;
      if (x.multi) {
        parts.push("(" + vals.map(function () { return "(' ' || " + x.col + " || ' ') LIKE ?"; }).join(" OR ") + ")");
        vals.forEach(function (v) { params.push("% " + v + " %"); });
      } else {
        parts.push(x.col + " IN (" + vals.map(function () { return "?"; }).join(",") + ")");
        params.push.apply(params, vals);
      }
    });
    var q = st.q.trim();
    if (q) {
      if (spec.text.fts) {
        var m = q.split(/\s+/).map(function (t) { return '"' + t.replace(/"/g, "") + '"*'; }).join(" ");
        parts.push(spec.text.col + " IN (SELECT slug FROM " + spec.text.fts + " WHERE " + spec.text.fts + " MATCH ?)");
        params.push(m);
      } else {
        q.split(/\s+/).forEach(function (t) {
          parts.push("(" + spec.text.like.map(function (c) { return c + " LIKE ?"; }).join(" OR ") + ")");
          spec.text.like.forEach(function () { params.push("%" + t + "%"); });
        });
      }
    }
    return { sql: parts.length ? " WHERE " + parts.join(" AND ") : "", params: params };
  };

  // ------------------------------------------------------------ UI
  var root, tabsNav, gen = 0;
  var render = function () {
    var spec = TABS[st.tab], my = ++gen;
    tabsNav.innerHTML = ORDER.map(function (t) {
      return '<a href="#tab=' + t + '"' + (t === st.tab ? ' aria-current="page"' : "") + ">" + TABS[t].label + "</a>";
    }).join("");
    if (!root.querySelector(".ex-grid") || root.dataset.tab !== st.tab) {
      root.dataset.tab = st.tab;
      root.innerHTML = '<div class="ex-grid"><aside class="ex-facets"></aside><section class="ex-main">' +
        '<div class="ex-bar"><input class="filter ex-q" type="search" placeholder="Search ' + esc(spec.what) + '…" aria-label="Search">' +
        '<label class="small">Sort <select class="ex-sort">' + spec.sorts.map(function (s) {
          return '<option value="' + s[0] + '">' + esc(s[1]) + "</option>"; }).join("") + "</select></label>" +
        '<a href="#tab=' + st.tab + '&custom=1" class="small ex-clear">clear filters</a></div>' +
        '<p class="ex-count muted small"></p><div class="ex-results"></div><div class="ex-pager"></div></section></div>';
      var qbox = root.querySelector(".ex-q"), timer = null;
      qbox.value = st.q;
      qbox.addEventListener("input", function () {
        clearTimeout(timer);
        timer = setTimeout(function () { st.q = qbox.value; st.page = 1; writeHash(); render(); }, 250);
      });
      var sortSel = root.querySelector(".ex-sort");
      sortSel.value = st.sort;
      sortSel.addEventListener("change", function () { st.sort = sortSel.value; st.page = 1; writeHash(); render(); });
    }
    var w = where(spec);
    var sortSql = (spec.sorts.filter(function (s) { return s[0] === st.sort; })[0] || spec.sorts[0])[2];
    var countQ = window.bbQuery("SELECT COUNT(*) AS n FROM " + spec.from + w.sql, w.params);
    var rowsQ = window.bbQuery("SELECT " + spec.select + " FROM " + spec.from + w.sql + " ORDER BY " + sortSql +
                               " LIMIT " + PAGE + " OFFSET " + (st.page - 1) * PAGE, w.params);
    var facetQs = spec.facets.map(function (x) {
      var fw = where(spec, x.key);
      return window.bbQuery("SELECT " + x.col + " AS v, COUNT(*) AS n FROM " + spec.from + fw.sql + " GROUP BY v", fw.params);
    });
    Promise.all([countQ, rowsQ].concat(facetQs)).then(function (res) {
      if (my !== gen) return;  // a newer query superseded this one
      var total = res[0][0].n, rows = res[1];
      root.querySelector(".ex-count").textContent = total === 0 ? "No matches." :
        "Showing " + ((st.page - 1) * PAGE + 1) + "–" + Math.min(total, st.page * PAGE) + " of " + total + " " + spec.what + ".";
      root.querySelector(".ex-results").innerHTML = rows.length ? '<div class="ex-scroll"><table class="ex-table"><thead><tr>' +
        spec.head.map(function (h) { return "<th>" + esc(h) + "</th>"; }).join("") + "</tr></thead><tbody>" +
        rows.map(function (r) { return "<tr>" + spec.row(r).map(function (c) { return "<td>" + c + "</td>"; }).join("") + "</tr>"; }).join("") +
        "</tbody></table></div>" : "";
      renderMath(root.querySelector(".ex-results"));
      var pages = Math.ceil(total / PAGE);
      root.querySelector(".ex-pager").innerHTML = pages > 1 ?
        (st.page > 1 ? '<button type="button" data-page="' + (st.page - 1) + '">← previous</button>' : "") +
        ' <span class="muted small">page ' + st.page + " of " + pages + "</span> " +
        (st.page < pages ? '<button type="button" data-page="' + (st.page + 1) + '">next →</button>' : "") : "";
      root.querySelectorAll(".ex-pager button").forEach(function (b) {
        b.addEventListener("click", function () { st.page = +b.dataset.page; writeHash(); render(); window.scrollTo(0, root.offsetTop - 60); });
      });
      renderFacets(spec, res.slice(2));
    }).catch(function (err) {
      if (my !== gen) return;
      root.querySelector(".ex-count").textContent = "Query failed: " + (err && err.message || err);
    });
  };

  var renderFacets = function (spec, counts) {
    var box = root.querySelector(".ex-facets");
    var open = {};
    box.querySelectorAll("details").forEach(function (d) { open[d.dataset.key] = d.open; });
    box.innerHTML = spec.facets.map(function (x, i) {
      var agg = {};
      counts[i].forEach(function (r) {
        var vs = x.multi ? String(r.v || "none").split(" ") : [r.v == null ? "none" : String(r.v)];
        vs.forEach(function (v) { agg[v] = (agg[v] || 0) + r.n; });
      });
      var sel = st.f[x.key] || [];
      sel.forEach(function (v) { if (!(v in agg)) agg[v] = 0; });
      var vals = Object.keys(agg).sort(function (a, b) { return agg[b] - agg[a] || a.localeCompare(b); });
      if (!vals.length || (vals.length === 1 && !sel.length && x.key !== "status")) return "";
      var narrow = window.matchMedia && window.matchMedia("(max-width: 820px)").matches;  // phones: facets start closed
      var isOpen = x.key in open ? open[x.key] : (sel.length > 0 || (!narrow && i < 3));
      return '<details data-key="' + x.key + '"' + (isOpen ? " open" : "") + "><summary>" + esc(x.label) +
        (sel.length ? ' <span class="badge">' + sel.length + "</span>" : "") + "</summary><ul" + (vals.length > 12 ? ' class="long"' : "") + ">" +
        vals.map(function (v) {
          var on = sel.indexOf(v) !== -1;
          return '<li><label><input type="checkbox" data-k="' + x.key + '" value="' + esc(v) + '"' + (on ? " checked" : "") + "> " +
            esc(x.dim ? lab(x.dim, v) : v) + ' <span class="muted">' + agg[v] + "</span></label></li>";
        }).join("") + "</ul></details>";
    }).join("");
    box.querySelectorAll("input[data-k]").forEach(function (cb) {
      cb.addEventListener("change", function () {
        var k = cb.dataset.k, cur = st.f[k] || [];
        st.f[k] = cb.checked ? cur.concat([cb.value]) : cur.filter(function (v) { return v !== cb.value; });
        st.page = 1; writeHash(); render();
      });
    });
  };

  var renderMath = function (scope) {
    if (!window.katex) return;
    scope.querySelectorAll(".math[data-tex]").forEach(function (el) {
      try { window.katex.render(el.dataset.tex, el, { throwOnError: false, strict: "ignore" }); } catch (e) { /* keep raw */ }
    });
  };

  document.addEventListener("DOMContentLoaded", function () {
    root = document.getElementById("explore");
    tabsNav = document.getElementById("ex-tabs");
    if (!root) return;
    window.addEventListener("hashchange", function () {
      var tab = st && st.tab;
      readHash();
      if (tab !== st.tab) root.dataset.tab = "";
      render();
    });
    window.bbQuery("SELECT dim, value, label FROM labels").then(function (rows) {
      rows.forEach(function (r) { (LAB[r.dim] = LAB[r.dim] || {})[r.value] = r.label; });
      LAB.src = { own: "own", inherited: "inherited only", none: "none" };
      readHash();
      render();
    }).catch(function (err) {
      root.innerHTML = '<p class="notice">Could not open the database (' + esc(err && err.message || err) + ").</p>";
    });
  });
})();
