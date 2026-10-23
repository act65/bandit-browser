// Facet filters for the analysis pages (gaps.html) and the status filter on the settings index.
window.bbReady(function () {
  // .facetbar[data-target]: <select data-facet="x"> filters children of #target by data-x; text box by content.
  document.querySelectorAll(".facetbar[data-target]").forEach(function (bar) {
    var list = document.getElementById(bar.dataset.target);
    if (!list) return;
    var selects = bar.querySelectorAll("select[data-facet]");
    var text = bar.querySelector("[data-facet-text]");
    var count = bar.querySelector("[data-count]");
    var apply = function () {
      var want = {};
      selects.forEach(function (s) { if (s.value) want[s.dataset.facet] = s.value; });
      var terms = text ? text.value.toLowerCase().split(/\s+/).filter(Boolean) : [];
      var shown = 0;
      Array.prototype.forEach.call(list.children, function (el) {
        var ok = Object.keys(want).every(function (k) { return el.dataset[k] === want[k]; });
        if (ok && terms.length) {
          var t = el.textContent.toLowerCase();
          ok = terms.every(function (q) { return t.indexOf(q) !== -1; });
        }
        el.hidden = !ok;
        if (ok) shown++;
      });
      if (count) count.textContent = shown + " of " + list.children.length + " shown";
      var qs = new URLSearchParams();
      Object.keys(want).forEach(function (k) { qs.set(k, want[k]); });
      history.replaceState(null, "", qs.toString() ? "#" + qs.toString() : window.location.pathname);
    };
    selects.forEach(function (s) { s.addEventListener("change", apply); });
    var sorter = bar.querySelector("select[data-sort]");
    if (sorter) {
      var orig = Array.prototype.slice.call(list.children);
      sorter.addEventListener("change", function () {
        var items = orig.slice();
        if (sorter.value === "sev") {
          items.sort(function (a, b) { return (a.dataset.sev - b.dataset.sev) || (b.dataset.papers - a.dataset.papers); });
        }
        items.forEach(function (x) { list.appendChild(x); });
      });
    }
    if (text) text.addEventListener("input", apply);
    document.querySelectorAll("[data-set-facet]").forEach(function (b) {
      b.addEventListener("click", function () {
        var s = bar.querySelector('select[data-facet="' + b.dataset.setFacet + '"]');
        if (s) { s.value = b.dataset.value; apply(); }
      });
    });
    // initial state from the hash (#status=poly_gap&regime=...)
    var init = new URLSearchParams(window.location.hash.slice(1));
    selects.forEach(function (s) {
      var v = init.get(s.dataset.facet);
      if (v !== null && Array.prototype.some.call(s.options, function (o) { return o.value === v; })) s.value = v;
    });
    apply();
  });

  // Settings index: status select hides rows whose data-status differs (independent of the text filter).
  var sf = document.getElementById("status-filter");
  if (sf) {
    var tbl = document.querySelector("table.settings");
    var go = function () {
      tbl.querySelectorAll("tbody tr[data-status]").forEach(function (tr) {
        tr.classList.toggle("st-off", !!sf.value && tr.dataset.status !== sf.value);
      });
    };
    sf.addEventListener("change", go);
    go();
  }
});
