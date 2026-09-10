/* Turning names and records in the prose into links.
 *
 * David asked on 10 September 2026 why a person named on a family page does not
 * take you to that person, and why a record cited in a table does not take you
 * to the record. Both are fair: an evidence-first archive that makes you
 * re-type a name into a search box is not making its evidence reachable.
 *
 * The rule this file enforces is that A LINK NEVER CLAIMS MORE THAN THE ARCHIVE
 * KNOWS. Three destinations, in order:
 *
 *   1. a person page  — only when exactly ONE person of that name is recorded.
 *      Names repeat constantly in this parish (three Maria Falco, four
 *      Pasquale), and sending a reader to one of them would be an unproven
 *      identification dressed up as navigation.
 *   2. the people roster, pre-filtered — when the name is shared. The reader
 *      sees all of them and chooses; the archive does not choose for them.
 *   3. the register, pre-filtered — when there is no person page but the name
 *      does appear in the swept registers.
 *
 * If none of those hold, the name is left as plain text. A dead link is worse
 * than no link.
 */
import { people } from "./people.js";
import register from "../data/register.json";
import line from "../data/line.json";
import living from "../data/living.json";
import { u } from "./url.js";

const norm = (s) =>
  String(s || "")
    .replace(/\s*\(.*?\)\s*/g, " ")
    .replace(/[’‘]/g, "'")          // d’Addio and d'Addio are one name
    .replace(/[«»"]/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();

/* person pages, and which names more than one of them answers to */
const slugByName = new Map();
const shared = new Set();
for (const p of people) {
  const k = norm(p.name);
  if (!k) continue;
  if (slugByName.has(k)) shared.add(k);
  else slugByName.set(k, p.slug);
}

/* Every register row's name, lower-cased once, so a lookup is a scan of
   strings rather than of objects. The register names are descriptive
   ("Carmine Falco (b. 1930) m. …"), so this is a substring test, not equality. */
const registerNames = register.map((r) => norm(r.name));

/** The name as a reader would type it into the search box. */
export function bare(name) {
  return String(name || "")
    .replace(/\s*\(.*?\)\s*/g, " ")
    .replace(/[«»"'’]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

/* The prose keeps the honorific the register itself gave the person —
   «Donn'Anna Quotolo», «Don Claudio Cimmino» — but the register's own name
   field usually drops it. Try both, or the courtesy title costs the reader
   the link. */
const HONORIFIC = /^(?:donn'|donna|don|suor|fra|il dottor|dottor)\s*/i;

export function registerHits(name) {
  const n = norm(name);
  if (n.length < 4) return 0;
  const forms = [n];
  const bareN = n.replace(HONORIFIC, "").trim();
  if (bareN && bareN !== n) forms.push(bareN);
  let c = 0;
  for (const r of registerNames) if (forms.some((f) => r.includes(f))) c++;
  return c;
}

/* The nine generations of the direct line. Most of them have no household
   entry — the later ones lived in Arpaia and Brisbane, not in the Arienzo
   registers — so without this a mention of Carmine Falco of generation eight
   would fall through to a register search. A generation gets its own anchor on
   the direct-line page. Alternative forms in brackets are indexed too:
   "Carmine Antonio (Carminantonio) Falco" answers to all three shapes. */
const genByName = new Map();
const genShared = new Set();
for (const g of line) {
  const raw = String(g.name || "");
  const forms = new Set([norm(raw)]);
  const alt = raw.match(/\(([^)]+)\)/);
  if (alt) {
    forms.add(norm(raw.replace(/\s*\([^)]*\)\s*/, " ")));
    forms.add(norm(raw.replace(/\S+\s*\([^)]*\)/, alt[1])));
  }
  for (const f of forms) {
    if (!f) continue;
    if (genByName.has(f)) genShared.add(f);
    else genByName.set(f, g);
  }
}
/* Two Raffaele Falco stand in this line, generations four and six, and two
   Carmine Antonio Falco, five and seven. A page that writes "Raffaele Falco"
   may mean either — or, on the Ferrara page, a third man of the twentieth
   century who is in the line at all. Sending the reader to one of them would
   be an identification the archive has not made, so a shared forename resolves
   to the list and lets them choose. */

/* Living people are named on this site but carry NOTHING else — no dates, no
   places, no records. There is nothing to link them to but the roster they
   appear in, and that is deliberate. See tools/build_living.py. */
const livingNames = new Set(living.map((r) => norm(r.name)));

/** Where a mention of `name` should go — or null if nowhere honest. */
export function personLink(name) {
  const n = norm(name);
  if (!n) return null;

  if (genByName.has(n) && !genShared.has(n)) {
    const g = genByName.get(n);
    return { href: u("/direct-line") + "#gen-" + g.gen, kind: "gen",
             title: `Generation ${g.gen} of the direct line` };
  }
  if (genShared.has(n)) {
    return { href: u("/people") + "?q=" + encodeURIComponent(bare(name)), kind: "several",
             title: `More than one person in this archive is called ${bare(name)} — the archive does not decide which is meant` };
  }
  if (livingNames.has(n)) {
    return { href: u("/people") + "?q=" + encodeURIComponent(name), kind: "living",
             title: "A living relative — this archive publishes their name and nothing else" };
  }

  if (slugByName.has(n) && !shared.has(n)) {
    return { href: u("/people/" + slugByName.get(n)), kind: "person",
             title: `${name} — their page in this archive` };
  }
  if (shared.has(n)) {
    const many = people.filter((p) => norm(p.name) === n).length;
    return { href: u("/people") + "?q=" + encodeURIComponent(name), kind: "several",
             title: `${many} people of this name are recorded — the archive does not decide which is which` };
  }
  const hits = registerHits(name);
  if (hits > 0) {
    /* the normalised form, not the raw one: the roster searches row text, and
       no row says "Caterina Zampiello (Falco)" — they say "Caterina Zampiello". */
    return { href: u("/register") + "?q=" + encodeURIComponent(bare(name).replace(HONORIFIC, "").trim()), kind: "register",
             title: `${hits} record${hits === 1 ? "" : "s"} in the register name ${name}` };
  }
  return null;
}

export { norm };
