import { defineConfig } from 'astro/config';
import aliases from './src/data/people-aliases.json' with { type: 'json' };
import register from './src/data/register.json' with { type: 'json' };

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
/* Six of the seven archives call the name namespace /who/. This one called it
   /names/ until Phase 6b. The slugs did not change, only the prefix — and this
   archive's own rule is that a published address does not rot, so all 4,682 of
   them are kept alive. Derived from the register with the same rules the page
   itself uses, so the two cannot drift apart. */
const bare = (n) => String(n || "").replace(/\s*\(.*?\)\s*/g, " ")
  .replace(/[’‘]/g, "'").replace(/\s+/g, " ").trim();
const nameSlug = (s) => s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const isName = (n) => {
  const t = String(n || "").trim();
  return t.length >= 2 && t.length <= 64 && t.split(/\s+/).length <= 7
      && !/[.;:\u2014]\s|\u00ab|\u00bb|\bthe\b|\bnot an\b/i.test(t);
};
const nameRedirects = Object.fromEntries(
  [...new Set(register.filter((r) => isName(bare(r.name))).map((r) => nameSlug(bare(r.name))))]
    .filter(Boolean)
    .map((slug) => [`/names/${slug}`, `${BASE}/who/${slug}/`])
);

export default defineConfig({
  site: 'https://daviddef.github.io',
  base: '/TheFalco',
  build: { format: 'directory' },
  redirects: { ...redirects, ...nameRedirects, '/names': `${BASE}/who/` },
});
