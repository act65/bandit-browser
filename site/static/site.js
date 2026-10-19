// Renders LaTeX spans with KaTeX and wires up filter boxes.
document.addEventListener("DOMContentLoaded", function () {
  if (window.katex) {
    document.querySelectorAll(".math[data-tex]").forEach(function (el) {
      try {
        katex.render(el.dataset.tex, el, { throwOnError: false, displayMode: false });
      } catch (err) {
        /* leave the raw TeX in place */
      }
    });
  }

  // A filter box filters the rows of the next table.filterable after it.
  document.querySelectorAll("input.filter").forEach(function (input) {
    var el = input.nextElementSibling;
    var tbl = el && (el.matches("table") ? el : el.querySelector("table.filterable"));
    if (!tbl) return;
    var rows = Array.prototype.slice.call(tbl.tBodies[0].rows);
    input.addEventListener("input", function () {
      var terms = input.value.toLowerCase().split(/\s+/).filter(Boolean);
      rows.forEach(function (tr) {
        var t = tr.textContent.toLowerCase();
        tr.hidden = !terms.every(function (q) { return t.indexOf(q) !== -1; });
      });
    });
  });
});
