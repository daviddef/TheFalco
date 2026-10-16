/* What this archive's own data says about one family name, counted.
 *
 * 17 October 2026. Two pages need the same numbers: /families/<slug>/ (the page)
 * and /families/ (the index card that points at it), and a count computed in two
 * places is a count that will disagree with itself. Everything here is derived from
 * people.json and nothing is stored: no sentence, no date, no place is typed in.
 *
 * WHO IS COUNTED. Everyone people.json holds under the surname or one of the
 * spellings families.json lists for it (a particle di/de/del/della/lo/la is not part
 * of which family it is; nothing else is folded). Who is living is people.json's own
 * `living` flag (the kit's one test, applied by build_people.py): a living person is
 * counted, and contributes no date, no place and no source to any figure here.
 */
import { people } from "./people.js";

export const norm = (s) =>
  String(s || "").trim().toUpperCase()
    .replace(/^(DI|DE|DEL|DELLA|DELLO|DEI|LA|LO)\s+/, "");

const YR = /\b(1[5-9]\d\d|20\d\d)\b/g;

export function familyNames(fam) {
  return [fam.sn, ...(fam.also || [])].map(norm);
}

export function oldestFirst(list) {
  const y = (x) => Number((String(x.b || "").match(/\b(1[5-9]\d\d|20\d\d)\b/) || [])[1] || 9999);
  return [...list].sort((a, b) => y(a) - y(b));
}

export function stats(fam) {
  const names = familyNames(fam);
  const ours = oldestFirst(people.filter((p) => names.includes(norm(p.surname))));
  const dead = ours.filter((p) => !p.living);
  const nRecord = dead.filter((p) => (p.sources || []).includes("register")).length;
  const yrs = dead.flatMap((p) =>
    [p.b, p.d, ...(p.events || []).map((e) => e.date)]
      .flatMap((x) => String(x || "").match(YR) || []).map(Number));
  const placeCount = new Map();
  for (const p of dead) {
    const seen = new Set([p.bp, p.dp, ...(p.events || []).map((e) => e.place)]
      .map((x) => String(x || "").split(",")[0].trim())
      .filter((x) => x && x !== "—"));
    for (const t of seen) placeCount.set(t, (placeCount.get(t) || 0) + 1);
  }
  return {
    names, ours, dead,
    nLiving: ours.length - dead.length,
    nRecord,
    nTree: dead.length - nRecord,
    yFrom: yrs.length ? Math.min(...yrs) : null,
    yTo: yrs.length ? Math.max(...yrs) : null,
    placesSorted: [...placeCount].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])),
  };
}
