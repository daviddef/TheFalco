/* The people of this archive, and how they are joined to each other.
 *
 * The graph itself is built by tools/build_people.py, which merges the
 * register households with the family tree and marks EVERY relationship with
 * where it came from — `register`, `tree`, or `both`. That file carries the
 * reasoning; this one is the loader, and it keeps the API the rest of the site
 * has always used so that no existing /people/<slug> URL changes.
 */
import all from "../data/people.json";

const kebab = (s) =>
  String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

const clean = (s) => String(s || "").replace(/\s*\(.*?\)\s*/g, " ").replace(/\s+/g, " ").trim();

export const people = all.map((p) => ({ ...p, display: p.name }));
export const bySlug = new Map(people.map((p) => [p.slug, p]));

export function findPerson(name, household) {
  const n = clean(name);
  if (household) {
    /* A woman who was a daughter in one house and a wife in another is now ONE
       record, filed under the house she headed. Looking her up by the house
       she was born in has to find her too, or her own parents' page loses her. */
    const hit = people.find((p) => clean(p.name) === n &&
      (p.household === household || p.alsoChildIn === household));
    if (hit) return hit;
  }
  const all = people.filter((p) => clean(p.name) === n);
  return all.length === 1 ? all[0] : null;
}

export function householdMembers(hname) {
  return people.filter((p) => p.household === hname || p.alsoChildIn === hname);
}

/** A relationship bucket with its sources resolved to full person records. */
export function kin(p, bucket) {
  return (p[bucket] || []).map((e) => ({ ...e, person: bySlug.get(e.slug) || null }));
}

export { kebab, clean };
