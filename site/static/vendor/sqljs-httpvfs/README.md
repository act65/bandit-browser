# sql.js-httpvfs 0.8.12 (vendored)

Unmodified `dist/` files of [sql.js-httpvfs](https://github.com/phiresky/sql.js-httpvfs) (Apache-2.0, see
LICENSE; it bundles sql.js, MIT, and SQLite 3.35, public domain). Vendored because a Web Worker must be
served from the page's own origin. `index.js` defines `window.createDbWorker`; the worker fetches the
database with HTTP range requests, so only the pages a query touches are downloaded.
