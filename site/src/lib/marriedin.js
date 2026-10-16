/* How a family reaches this line — the rule, in one place.
 *
 * /marriages/ needs it to lay out its sections and the front page needs it to
 * draw the same families, and a rule copied into two pages is a rule that will
 * be two rules by next month. The prose, the stories and the people tables stay
 * on the page; only the QUESTION "how does this surname reach the Falco" lives
 * here, because that is the part that must not drift.
 */
import groups from "../data/married-in.json";

export const other = groups.filter((g) => g.surname !== "Falco");

/* A family can hold people of several reaches at once — 23 of the 77 do, and a
   Bucolo is both a woman who married a Falco and the family she came from. It
   is filed under the STRONGEST reach any of its people has, so the filing is
   deterministic rather than whichever reach happened to be commonest. */
export const STRENGTH = ["blood", "married", "kin", "second", "unconnected"];
export const primary = (g) =>
  STRENGTH.find((s) => (g.reach || []).includes(s)) || "unconnected";

export const GROUPS = [
  { key: "blood", label: "They carry this family's blood" },
  { key: "married", label: "They married a Falco" },
  { key: "kin", label: "The families they came from" },
  { key: "second", label: "They married into one of those" },
  { key: "unconnected", label: "Not yet joined to this family" },
];

/* Just enough for a chart: a name and a number, grouped. The marriages page
   builds the richer version on top of the same filing.
 *
 * THE NUMBER IS THE REACH'S OWN COUNT, NOT `n`. `n` is how many of a family's
 * people are listed, and a family can hold people of several reaches at once, so
 * plotting `n` under a heading about blood drew rows that did not belong under
 * it. `reachCount` has always held the honest figure for the reach being drawn. */
export const chartGroups = GROUPS.map((g) => ({
  key: g.key, label: g.label,
  families: other.filter((x) => primary(x) === g.key)
    .map((x) => ({ surname: x.surname, n: (x.reachCount || {})[g.key] ?? x.n })),
})).filter((g) => g.families.length);
