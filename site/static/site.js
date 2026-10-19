// KaTeX rendering, filter boxes, settings grouping and source popovers. No framework.
document.addEventListener("DOMContentLoaded", function () {
  if (window.katex) {
    document.querySelectorAll(".math[data-tex]").forEach(function (el) {
      try {
        katex.render(el.dataset.tex, el, { throwOnError: false, errorColor: "#8a8a8f", displayMode: false, strict: "ignore" });
      } catch (err) {
        /* leave the raw TeX in place */
      }
    });
  }

  // A filter box filters the rows of the next table.filterable (or .filterable-cards) after it.
  document.querySelectorAll("input.filter").forEach(function (input) {
    var host = input.closest(".toolbar") || input;
    var el = host.nextElementSibling;
    if (!el) return;
    var tbl = el.matches("table.filterable") ? el : el.querySelector("table.filterable");
    var cards = el.matches(".filterable-cards") ? el : null;
    if (!tbl && !cards) return;
    input.addEventListener("input", function () {
      var terms = input.value.toLowerCase().split(/\s+/).filter(Boolean);
      var match = function (node) {
        var t = node.textContent.toLowerCase();
        return terms.every(function (q) { return t.indexOf(q) !== -1; });
      };
      if (cards) {
        Array.prototype.forEach.call(cards.children, function (c) { c.hidden = !match(c); });
        return;
      }
      var rows = Array.prototype.slice.call(tbl.tBodies[0].rows);
      rows.forEach(function (tr) { if (!tr.classList.contains("group")) tr.hidden = !match(tr); });
      // hide group headers with no visible rows
      var header = null, any = false;
      rows.forEach(function (tr) {
        if (tr.classList.contains("group")) {
          if (header) header.hidden = !any;
          header = tr; any = false;
        } else if (!tr.hidden) { any = true; }
      });
      if (header) header.hidden = !any;
    });
  });

  // Settings index: group rows by a data attribute.
  var gtable = document.querySelector("table.groupable");
  if (gtable) {
    var tbody = gtable.tBodies[0];
    var rows = Array.prototype.slice.call(tbody.rows);
    var ncol = gtable.tHead.rows[0].cells.length;
    var regroup = function (attr) {
      tbody.querySelectorAll("tr.group").forEach(function (g) { g.remove(); });
      var sorted = rows.slice().sort(function (a, b) {
        if (attr) {
          var ga = a.dataset[attr], gb = b.dataset[attr];
          var na = groupSize[attr][ga], nb = groupSize[attr][gb];
          if (ga !== gb) return nb - na || (ga < gb ? -1 : 1);
        }
        return b.dataset.n - a.dataset.n;
      });
      var last = null;
      sorted.forEach(function (tr) {
        if (attr && tr.dataset[attr] !== last) {
          last = tr.dataset[attr];
          var g = document.createElement("tr");
          g.className = "group";
          g.innerHTML = '<th colspan="' + ncol + '"></th>';
          g.firstChild.textContent = last + " ";
          var c = document.createElement("span");
          c.className = "muted";
          c.textContent = "· " + groupCount[attr][last] + " settings";
          g.firstChild.appendChild(c);
          tbody.appendChild(g);
        }
        tbody.appendChild(tr);
      });
    };
    var groupSize = {}, groupCount = {};
    ["action_space", "environment"].forEach(function (attr) {
      groupSize[attr] = {}; groupCount[attr] = {};
      rows.forEach(function (tr) {
        var k = tr.dataset[attr];
        groupSize[attr][k] = (groupSize[attr][k] || 0) + Number(tr.dataset.n);
        groupCount[attr][k] = (groupCount[attr][k] || 0) + 1;
      });
    });
    var buttons = document.querySelectorAll(".seg button[data-group]");
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        buttons.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        regroup(b.dataset.group);
        try { localStorage.setItem("bb-group", b.dataset.group); } catch (err) { /* ignore */ }
      });
    });
    var initial = "action_space";
    try { var saved = localStorage.getItem("bb-group"); if (saved !== null) initial = saved; } catch (err) { /* ignore */ }
    buttons.forEach(function (x) { x.setAttribute("aria-pressed", String(x.dataset.group === initial)); });
    regroup(initial);
  }

  // Only one source popover open at a time; Escape or outside click closes it.
  var pops = document.querySelectorAll("details.pop");
  pops.forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (d.open) pops.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });
  document.addEventListener("click", function (ev) {
    pops.forEach(function (d) { if (d.open && !d.contains(ev.target)) d.open = false; });
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") pops.forEach(function (d) { d.open = false; });
  });
});
