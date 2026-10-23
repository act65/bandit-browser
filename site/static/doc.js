// Shell pages (setting.html?s=<slug>, paper.html?p=<id>): fetch the page's HTML from the
// database, inject it, then fire "bb:doc" so site.js / plots.js / analysis.js initialise on it.
document.addEventListener("DOMContentLoaded", function () {
  var host = document.getElementById("doc");
  if (!host) return;
  var kind = host.dataset.kind;
  var key = new URLSearchParams(window.location.search).get(kind === "setting" ? "s" : "p");
  var fail = function (msg) {
    host.innerHTML = '<p class="notice">' + msg + ' <a href="explore.html#tab=' + kind + 's">Browse all ' + kind + "s →</a></p>";
  };
  if (!key) { fail("No " + kind + " given."); return; }
  window.bbQuery("SELECT title, html FROM docs WHERE kind = ? AND key = ?", [kind, key]).then(function (rows) {
    if (!rows.length) { fail("No " + kind + " <code>" + window.bbEsc(key) + "</code> in the database."); return null; }
    document.title = rows[0].title + " · bandit-browser";
    return window.bbGunzip(rows[0].html).then(function (html) {
      host.innerHTML = html;
      document.dispatchEvent(new Event("bb:doc"));
      if (window.location.hash) {
        var target = document.getElementById(decodeURIComponent(window.location.hash.slice(1)));
        if (target) target.scrollIntoView();
      }
    });
  }).catch(function (err) {
    fail("Could not read the database (" + window.bbEsc(err && err.message || err) + ").");
  });
});
