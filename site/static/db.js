// Shared access to the atlas database (data/atlas-<hash>.db.NNN, described by data/config.json).
// sql.js-httpvfs runs SQLite in a Web Worker and reads the file with HTTP range requests, so a
// query downloads only the database pages it touches. The page's <meta name="bb-db"> names the
// database version, so a cached config.json from an earlier build is never used.
(function () {
  var worker = null;
  var abs = function (u) { return new URL(u, document.baseURI).toString(); };
  window.bbDB = function () {
    if (!worker) {
      if (!window.createDbWorker) return Promise.reject(new Error("sql.js-httpvfs did not load"));
      var meta = document.querySelector('meta[name="bb-db"]');
      var v = meta ? "?v=" + meta.content : "";
      worker = window.createDbWorker([{ from: "jsonconfig", configUrl: abs("data/config.json" + v) }],
        abs("static/vendor/sqljs-httpvfs/sqlite.worker.js"), abs("static/vendor/sqljs-httpvfs/sql-wasm.wasm"));
    }
    return worker;
  };
  // rows as objects: [{col: value, ...}, ...]
  window.bbQuery = function (sql, params) {
    return window.bbDB().then(function (w) { return w.db.query(sql, params || []); });
  };
  // documents are gzip-compressed HTML
  window.bbGunzip = function (bytes) {
    var stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"));
    return new Response(stream).text();
  };
  window.bbEsc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };
})();
