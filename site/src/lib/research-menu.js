/* THE RESEARCH MENU: one list, read by the header menu (layouts/Base.astro), the drawer, the hub page /research/ and the two group
   pages. 12 November 2026 (the research-menu trial, wave 3): "Evidence" and "Investigations" became one "Research" menu with three
   groups. Nothing is renamed and no address changes: every item keeps the address it had. The labels of the eight pages the estate's
   Evidence canon names (kit data/evidence-menu.json) are unchanged. `asks` is the canon's question for those pages. `atlas: true`
   marks a page whose registers and places the Record Atlas also carries. */
export const RESEARCH = [
  { id: "to-do", head: "To do", href: "/research/to-do/",
    dek: "What is not known yet, what has been asked of other people, and what is being worked on.",
    items: [
      { href: "/open-questions/", label: "Open Questions", asks: "What is not known, and what would settle it?" },
      { href: "/errands/", label: "Errands", asks: "What has been asked of other people, or needs someone standing in a place?" },
      { href: "/worklist/", label: "The work list", asks: "What is being done, by whom, since when?" },
    ] },
  { id: "whats-new", head: "What's new", href: "/whats-new/",
    dek: "What was read, found and taken back lately, newest first, and the same record in full.",
    items: [
      { href: "/searched/", label: "What Has Been Read", asks: "What was looked at, and what did it not turn up?" },
      { href: "/corrections/", label: "Corrections", asks: "What did this archive get wrong?" },
      { href: "/changes/", label: "What changed", asks: "What happened, most recent first?" },
      { href: "/research-log/", label: "Research Log", blurb: "The working notes, one file per register volume, written while reading and never tidied afterwards." },
    ] },
  { id: "sources-and-method", head: "Sources & method", href: "/research/sources-and-method/",
    dek: "What this archive stands on, how it grades a claim, and the longer studies of one body of records.",
    items: [
      { href: "/sources/", label: "Sources", atlas: true, asks: "What does this stand on, and where do I check?" },
      { href: "/method/", label: "Method", asks: "What would make you believe or not believe this?" },
      { href: "/documents/", label: "Documents", asks: "What is reproduced whole, and what does it say?" },
      { href: "/gallery/", label: "Gallery", asks: "What do the pages themselves look like?" },
      { sub: "Deep dives", id: "deep-dives",
        note: "A single body of records studied on its own, at length. Each is also linked from the Sources page.",
        items: [
          { href: "/antenati/", label: "Antenati", atlas: true, blurb: "What the Italian State Archives' portal holds for Arienzo and Benevento, opened by hand, and the two questions it answered that were not the answers we wanted." },
          { href: "/processetti/", label: "The Processetti", blurb: "The marriage files: everything a couple had to prove before they could marry. Which volumes exist, which are read, and the richest document this archive has." },
          { href: "/holdings/", label: "Holdings", atlas: true, blurb: "A map of the registers themselves: what exists, where, and what does not, so that no gap is found twice." },
          { href: "/the-library/", label: "The Library", atlas: true, blurb: "The bibliography: the record sets read, the working data kept in the open, and the much larger body not yet touched." },
          { href: "/dna/", label: "The DNA", blurb: "Two DNA tests, eight generations deep: what the result confirms, what it refuses to claim, and how far back it can see." },
        ] },
    ] },
];
/* the header menu's shape: [group, ...] with { head, href, items: [[href, label] | { sub }] } */
export const navGroups = RESEARCH.map((g) => ({
  head: g.head, href: g.href,
  items: g.items.flatMap((x) => x.sub ? [{ sub: x.sub }, ...x.items.map((y) => [y.href, y.label])] : [[x.href, x.label]]),
}));

/* the deep dives, for the Sources page: [[label, href, blurb]] */
export const deepDives = RESEARCH.flatMap((g) => g.items).filter((x) => x.id === "deep-dives").flatMap((x) => x.items)
  .map((d) => [d.label, d.href, d.blurb]);
