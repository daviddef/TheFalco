import households from "../data/households.json";
import line from "../data/line.json";

const kebab = (s) =>
  String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

const clean = (s) => String(s || "").replace(/\s*\(.*?\)\s*/g, " ").replace(/\s+/g, " ").trim();

/* One person = one name inside one household. Names repeat constantly in this
   parish — there are three Maria Falcos and four Pasquales — so the household
   is part of the identity, and we never silently merge two of them. */
function build() {
  const byKey = new Map();

  for (const h of households) {
    for (const m of h.members) {
      const key = h.name + "|" + m.person;
      if (!byKey.has(key)) {
        byKey.set(key, {
          name: m.person,
          display: m.person,
          household: h.name,
          role: m.role,
          events: [],
        });
      }
      const p = byKey.get(key);
      if (m.role !== "child" && p.role === "child") p.role = m.role;
      if (m.event && m.event !== "—") {
        p.events.push({
          event: m.event, date: m.date, place: m.place,
          evidence: m.evidence, ark: m.ark,
        });
      } else if (m.evidence) {
        p.events.push({ event: "named", date: m.date, place: m.place, evidence: m.evidence, ark: m.ark });
      }
    }
  }

  const people = [...byKey.values()];

  // slugs, disambiguated by household when a name repeats
  const counts = {};
  for (const p of people) counts[kebab(clean(p.name))] = (counts[kebab(clean(p.name))] || 0) + 1;
  const used = new Set();
  for (const p of people) {
    const base = kebab(clean(p.name));
    let slug = counts[base] > 1 ? `${base}-of-${kebab(p.household).slice(0, 34)}` : base;
    while (used.has(slug)) slug += "-2";
    used.add(slug);
    p.slug = slug;
  }

  // attach the direct line
  const lineByName = new Map(line.map((g) => [clean(g.name), g]));
  for (const p of people) {
    const g = lineByName.get(clean(p.name));
    /* A generation is only itself in the household it heads. Vincenzo and
       Andreana called two sons Pasquale; neither is Pasquale of generation
       two, and the archive must not quietly promote a dead infant into the
       direct line just because the name matches. */
    const headsThisHouse = p.household.split(/\s*&\s*/).some((n) => clean(n) === clean(p.name));
    if (g && headsThisHouse) { p.gen = g.gen; p.line = g; }
  }

  // parents, read off the household name
  for (const p of people) {
    const parts = p.household.split(/\s*&\s*/);
    if (p.role === "child" && parts.length === 2 && !/strada|\(/i.test(p.household)) {
      p.parents = parts.map((n) => {
        const par = people.find((q) => q.household === p.household && clean(q.name) === clean(n));
        return { name: n, slug: par ? par.slug : null };
      });
    }
  }

  return people;
}

export const people = build();
export const bySlug = new Map(people.map((p) => [p.slug, p]));

export function findPerson(name, household) {
  const n = clean(name);
  if (household) {
    const hit = people.find((p) => p.household === household && clean(p.name) === n);
    if (hit) return hit;
  }
  const all = people.filter((p) => clean(p.name) === n);
  return all.length === 1 ? all[0] : null;
}

export function householdMembers(hname) {
  return people.filter((p) => p.household === hname);
}

export { kebab, clean };
