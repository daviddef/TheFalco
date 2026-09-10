import { defineConfig } from 'astro/config';
import aliases from './src/data/people-aliases.json' with { type: 'json' };

/* Joining two half-records into one person changes that person's address —
   Chiara Rivetti used to live at two URLs, one per household, and now lives at
   one. Every old address is kept alive as a redirect. A public archive that
   renumbers its own people and lets the old links rot is not much of an
   archive. The map is written by tools/build_people.py. */
/* The redirect TARGET is emitted verbatim, so it has to carry the base path
   itself — without it the meta-refresh sends the reader to
   daviddef.github.io/people/… and straight into a 404. */
const BASE = '/TheFalco';
const redirects = Object.fromEntries([
  ...Object.entries(aliases).map(([from, to]) => [`/people/${from}`, `${BASE}/people/${to}`]),
  /* /emigration is the de Franceschi name for what this site already covers in
     full at /australia — the 1964 crossing, the ship, the arrival. The URL
     exists so the two archives line up; a second thin page would not. */
  ["/emigration", `${BASE}/australia`],
]);

// GitHub Pages project site. To serve from a custom domain later,
// set base to '/' and site to that domain.
export default defineConfig({
  site: 'https://daviddef.github.io',
  base: '/TheFalco',
  build: { format: 'directory' },
  redirects,
});
