/* WHO SHARES A NAME. One rule, used by the person page ("Others of the same name") and by the /who/<name>/ page ("Has the archive
 * identified anyone of this name?"), so the two cannot disagree (23 November 2026, one page per person).
 *
 * A person's name is read the way the /who/ pages have always read it: the parenthesis that tells two apart is dropped («Pasquale Falco
 * (of Michele, d. 1862)» is a Pasquale Falco), so is a nickname after «detto» («Pasquale Falco detto Zimbardo» is a Pasquale Falco who
 * was called Zimbardo: 5 November 2026), case is folded, and nothing else is. A question mark, an accent or a spelling that differs is a
 * different name here, as it is on /who/. They are NOT merged: two people of a name are two people.
 */
import { people } from "./people.js";
import register from "../data/register.json";

const bare = (n) => String(n || "").replace(/\s*\(.*?\)\s*/g, " ")
  .replace(/[’‘]/g, "'").replace(/\s+/g, " ").trim();

/** The name two people must share to be "of the same name". */
export const nameKey = (n) => bare(n).replace(/\s+detto\s+.+$/i, "").toLowerCase();

const SETS = new Map();
for (const p of people) {
  const k = nameKey(p.name);
  if (!SETS.has(k)) SETS.set(k, []);
  SETS.get(k).push(p);
}

/** Everybody in the archive who bears this name (the key, or a name as written). */
export const bearersOf = (name) => SETS.get(nameKey(name)) || [];

/** The others of a person's name: the rest of their set, in the order people.json holds them. */
export const othersOf = (p) => bearersOf(p.name).filter((q) => q.slug !== p.slug);

/** The people a /who/<name>/ page identifies: those whose name, read as above, is exactly this name as the register wrote it
 *  (so the page of «Pasquale Falco detto Zimbardo», a name only the register could write, identifies nobody under the nickname). */
export const bearersOfWritten = (name) => SETS.get(bare(name).toLowerCase()) || [];

/** What a namesake's line says about them, the words the /who/ page has used: where the archive holds them. A living person is a name and a
 *  town, as everywhere. */
export const whereHeld = (p) => p.gen ? `generation ${p.gen} of the direct line`
  : p.household ? `in the household of ${p.household}`
  : p.living ? ("living" + (p.place ? ", " + p.place : "")) : "from the family tree";

/* THE /who/ PAGE OF A NAME, if there is one: the register's own rule (pages/who/index.astro and [slug].astro), so a link made from here lands.
   A name the register never wrote has no page, and a person of such a name links nothing. */
const slugify = (x) => x.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const isName = (n) => {
  const t = String(n || "").trim();
  return t.length >= 2 && t.length <= 64 && t.split(/\s+/).length <= 7 && !/[.;:\u2014]\s|\u00ab|\u00bb|\bthe\b|\bnot an\b/i.test(t);
};
/** The slug of the /who/ page a register row is listed on, or null (the row's name is not a name the register writes a page for). */
export const whoSlugOfRow = (r) => { const n = bare(r.name); if (!isName(n)) return null; return slugify(n) || null; };
const WHO = new Set();
for (const r of register) { const k = whoSlugOfRow(r); if (k) WHO.add(k); }

/** The slug of the /who/ page that gathers the register's records of this person's name, or null. */
export const whoSlugOf = (name) => {
  const k = slugify(nameKey(name));
  return k && WHO.has(k) ? k : null;
};
