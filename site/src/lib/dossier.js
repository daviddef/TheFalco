/* WHAT OF A NAME'S REGISTER PAGE IS HONESTLY ABOUT ONE PERSON (one page per person, dossiers, 23 November 2026).
 *
 * /who/<name>/ is a page about a NAME. It gathers every register row that carries the name, and says so at the top: «gathered because they share a
 * name, and for no other reason». Falco's rows are not prose about people; they are lines of a register, 13,643 of them, and a name that has exactly
 * one bearer in the archive is NOT therefore a name with one bearer in the parish: «Caterina Zampiello» is one woman here (b. 1925) and the name of
 * twenty-seven rows, most of them baptisms of the 1870s and 1890s. Putting a name's rows on the page of its one bearer would put other women's
 * baptisms on hers. So this file does not move rows by name. A row is repeated on a person's page only when the DATA ties it to that person, by one
 * of two tests the page can state and a reader can check:
 *
 *   page    the row is a line of the very register page (a register image) or act (an Antenati index entry, a FamilySearch record) that this
 *           person's own page already cites as an event; the name matches and the place in the register is the same.
 *   parents the row names BOTH of the parents the person's page draws for them, on a day that is one of the days of their own events.
 *
 * and only when it is not ambiguous (no other page of the same name is tied to it by either test), is not already printed on the page (the row's
 * words are not in an event's evidence), and is not the archive's own reconstructed household or tree row (those ARE the page's events and family,
 * drawn from the same data). A living person, a person the kit holds out, and any row dated 1946 or later are never folded. Everything else stays on
 * /who/, and the person's page says how many records it is and links them: it does not say they are this person's.
 *
 * tools/checkdossiers.py re-derives all of this from register.json and people.json in Python and compares it with the built pages.
 */
import { createHash } from "node:crypto";
import register from "../data/register.json";
import { people } from "./people.js";
import { whoSlugOfRow, whoSlugOf } from "./namesets.js";

const bare = (n) => String(n || "").replace(/\s*\(.*?\)\s*/g, " ").replace(/[’‘]/g, "'").replace(/\s+/g, " ").trim();

export const rowId = (r) => createHash("sha1").update([r.name, r.detail, r.link || "", r.source || ""].join("␟")).digest("hex").slice(0, 10);

const MON = { jan: 1, gen: 1, gennaio: 1, january: 1, feb: 2, febbraio: 2, february: 2, mar: 3, marzo: 3, march: 3, apr: 4, aprile: 4, april: 4,
  may: 5, mag: 5, maggio: 5, jun: 6, giu: 6, giugno: 6, june: 6, jul: 7, lug: 7, luglio: 7, july: 7, aug: 8, ago: 8, agosto: 8, august: 8,
  sep: 9, set: 9, sept: 9, settembre: 9, september: 9, oct: 10, ott: 10, ottobre: 10, october: 10, nov: 11, novembre: 11, november: 11,
  dec: 12, dic: 12, dicembre: 12, december: 12 };
/** Every full calendar day a text names, as «YYYY-M-D»: «8 Oct 1884», «8 ottobre 1884», «Oct 8 1884», «1884-10-08», «08/10/1884». */
export function daysIn(text) {
  const s = String(text || "").toLowerCase(), out = new Set();
  let m;
  const a = /\b(\d{1,2})\s+([a-z]+)\.?\s+(\d{4})\b/g;
  while ((m = a.exec(s))) if (MON[m[2]]) out.add(`${+m[3]}-${MON[m[2]]}-${+m[1]}`);
  const b = /\b([a-z]{3,9})\s+(\d{1,2}),?\s+(\d{4})\b/g;
  while ((m = b.exec(s))) if (MON[m[1]]) out.add(`${+m[3]}-${MON[m[1]]}-${+m[2]}`);
  const c = /\b(\d{4})-(\d{2})-(\d{2})\b/g;
  while ((m = c.exec(s))) out.add(`${+m[1]}-${+m[2]}-${+m[3]}`);
  const d = /\b(\d{2})\/(\d{2})\/(\d{4})\b/g;
  while ((m = d.exec(s))) out.add(`${+m[3]}-${+m[2]}-${+m[1]}`);
  return out;
}

const hasTok = (text, tok) => new RegExp("(?<![A-Za-z0-9_-])" + tok.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![A-Za-z0-9_])").test(text);
const imgOf = (t) => {
  const m = /\bimg\.?\s*(\d+)\s*([lr])?\b/i.exec(String(t || "")) || /\bimage\s+(\d+)\s*([LR])?\b/.exec(String(t || ""));
  return m ? { n: +m[1], side: (m[2] || "").toLowerCase() } : null;
};

/** Is this row a line of the register page or act that one of this person's events already cites? */
export function samePage(r, p) {
  const l = r.link || "";
  const evs = (p.events || []).map((e) => String(e.ark || ""));
  let m = /^https:\/\/antenati\.cultura\.gov\.it\/ark:\/12657\/(an_u[ad]\d+)$/.exec(l);
  if (m) {
    const id = m[1];
    if (id.startsWith("an_ud")) return evs.some((a) => hasTok(a, id));
    const ri = imgOf(r.source);                       // a register volume is not a page: the image must be the same one
    if (!ri) return false;
    return evs.some((a) => { if (!hasTok(a, id)) return false; const ei = imgOf(a); return !!ei && ei.n === ri.n && (!ei.side || !ri.side || ei.side === ri.side); });
  }
  m = /^https:\/\/www\.familysearch\.org\/ark:\/61903\/(?:1:1|3:1):([0-9A-Z]{4}-[0-9A-Z]{3,4}(?:-[0-9A-Z0-9]{1,4}){0,2})$/.exec(l);
  return !!m && evs.some((a) => hasTok(a, m[1]));
}

/** Does this row name both parents the page draws, on a day of one of the person's own events? */
export function sameParents(r, p) {
  const par = (p.parents || []).filter((e) => !e.superseded).map((e) => bare(e.name).toLowerCase());
  if (par.length < 2) return false;
  const d = String(r.detail || "").toLowerCase();
  if (!par.slice(0, 2).every((x) => x && d.includes(x))) return false;
  const mine = new Set((p.events || []).flatMap((e) => [...daysIn(e.date)]));
  return [...daysIn(r.detail)].some((x) => mine.has(x));
}

const plain = (s) => String(s || "").replace(/[*_`]/g, "").replace(/\s+/g, " ").trim().toLowerCase();
const yearOf = (s) => { const m = String(s || "").match(/\b(1[5-9]\d\d|20\d\d)\b/g); return m ? Math.max(...m.map(Number)) : 0; };

/* the rows of each /who/ page, by the page's slug, as the page's own template lists them */
const ROWS = new Map();
for (const r of register) { const s = whoSlugOfRow(r); if (!s) continue; if (!ROWS.has(s)) ROWS.set(s, []); ROWS.get(s).push(r); }
const BEARERS = new Map();                           // who slug -> the people whose name that page is the register page of
for (const p of people) { const s = whoSlugOf(p.name); if (!s) continue; if (!BEARERS.has(s)) BEARERS.set(s, []); BEARERS.get(s).push(p); }

const KIND_OWN = new Set(["household", "tree"]);

/** What of the register page of this person's name belongs on their page.
 *  Returns null when the name has no register page. `held` is true for a living person and for one the kit holds out: nothing is folded for them. */
export function dossierOf(p, held = false) {
  const slug = whoSlugOf(p.name);
  if (!slug) return null;
  const rows = ROWS.get(slug) || [];
  const bearers = BEARERS.get(slug) || [];
  const own = rows.filter((r) => KIND_OWN.has(r.kind)).length;
  const out = { slug, total: rows.length, own, folded: [], already: 0, ambiguous: 0, bearers: bearers.length, tooRecent: 0 };
  if (held || p.living) return { ...out, other: rows.length - own, held: true };
  const evid = (p.events || []).map((e) => plain(e.evidence));
  for (const r of rows) {
    if (KIND_OWN.has(r.kind)) continue;
    const why = samePage(r, p) ? "page" : sameParents(r, p) ? "parents" : null;
    if (!why) continue;
    if (bearers.some((q) => q.slug !== p.slug && (samePage(r, q) || sameParents(r, q)))) { out.ambiguous++; continue; }
    if (yearOf(r.detail) >= 1946) { out.tooRecent++; continue; }
    const t = plain(r.detail);
    if (t && evid.some((e) => e.includes(t))) { out.already++; continue; }
    out.folded.push({ ...r, id: rowId(r), why });
  }
  out.other = rows.length - own - out.folded.length;
  return out;
}
