/* THE WHOLE MENU, one list, and the three hub lists that stand behind it. 23 November 2026 (the estate clean-up, task C).
   The header menu and the drawer read MENU (layouts/Base.astro does); the hub pages read the other lists in this file, so a menu and
   the page that holds what left it cannot disagree. No page was renamed, merged or deleted and no address changed: every href below
   was already a built page, only its group moved.
     a menu is  [label, items]
     items      a flat list of [href, label]                          (a short menu: one column)
                or a list of groups { head, href?, items }           (a group is a column; `href` makes its heading a link)
   What left a menu on 23 November 2026, and where it is reached from instead (proof: docs/menu-reach.md):
     the four drawn pages        (Our line drawn, The trees, The Timeline, Blood relatives drawn)  -> one link "Drawn", the hub /drawn/ (DRAWN)
     Roots & Routes             removed from the archive (its address redirects to /trees/)
     nine family pages          (Carfora, Ferrara, Maione, Rivetti, Zampiello, The Wider Family; Cioffi, Crisci, Annecchino and Morgillo stay) -> /families/ (FAMILY_PAGES)
     the place stories          (Arienzo, Strada Camellara, Valle Caudina, Walk the Line, Journeys, Under Whose Rule, Where the Name Went, The Bishop) -> /places/ (PLACE_STORIES)
     five deep dives and the Research Log -> /research/deep-dives/ (lib/research-menu.js) */
import { navGroups } from "./research-menu.js";

/* the four families that stay named in the menu. Labels follow the estate's family-menu rule (David, 12 Nov 2026): the bare surname,
   this archive's own line first (it is The Spine, which leads the Our line menu and is not repeated here), then the other surnames A to Z. */
const NAMED = [["/annecchino/", "Annecchino"], ["/families/cioffi/", "Cioffi"], ["/crisci/", "Crisci"], ["/morgillo/", "Morgillo"]];

export const MENU = [
  ["Start", [["/", "Home"], ["/story/", "The story"], ["/about/", "About"]]],
  ["Our line", [["/direct-line/", "The Spine"], ["/australia/", "Australia"], ["/lines/", "Where they went"]]],
  ["People", [
    { head: "Lists", items: [
      ["/people/", "The People"], ["/who/", "Every Name"], ["/register/", "The Register"], ["/households/", "Households"],
      ["/marriages/", "The Marriages"], ["/graves/", "Graves"],
    ] },
    { head: "Drawn", href: "/drawn/", items: [] },
  ]],
  ["Places & families", [
    { head: "Places", href: "/places/", items: [["/atlas/", "The Atlas"]] },
    { head: "The families", items: [["/families/", "All the families"], ...NAMED] },
  ]],
  ["The name", [["/name/", "The Name"], ["/which-falco/", "Which Falco?"], ["/namesakes/", "Namesakes"], ["/arms/", "Arms"]]],
  /* "Research" is lib/research-menu.js: three groups, the canon's eight core pages, Documents and Gallery, and ONE "Deep dives" heading
     that opens the hub /research/deep-dives/. */
  ["Research", navGroups],
];

/* /drawn/: every drawn page, with what it shows. The first four left the People menu; The Spine is also in the Our line menu. */
export const DRAWN = [
  { href: "/tree/", label: "Our line, drawn", blurb: "The whole documented line, drawn twice: as the chart every archive in the estate shares, and as this archive's own figure." },
  { href: "/trees/", label: "The trees", blurb: "The Falco spine and the families of the Valle Caudina it married, each drawn in the form its own evidence supports." },
  { href: "/bloodline/", label: "Blood relatives, drawn", blurb: "Choose a person and they go to the middle of the chart: parents above, brothers and sisters beside them, children below, and through them the aunts, uncles and cousins." },
  { href: "/timeline/", label: "The Timeline", blurb: "The line, the regimes it lived under, and underneath them the years of register this archive has read act by act." },
  { href: "/direct-line/", label: "The Spine", blurb: "From the Arienzo of the 1730s to Brisbane, each generation joined to the one above it by a record that names a father. Also in the Our line menu." },
];

/* /families/: the family pages that are not named in the menu (the index cards link only /families/<name>/, "Everyone of the name"). */
export const FAMILY_PAGES = [
  { href: "/carfora/", label: "Carfora", blurb: "Five Carfora households on two Arienzo streets, and a gentry Carfora of Santa Maria a Vico that is not joined to any of them." },
  { href: "/ferrara/", label: "Ferrara", blurb: "Giuseppa Ferrara, who married Angelo Zampiello and became Francesca's mother." },
  { href: "/maione/", label: "Maione", blurb: "Costanza Maione of Arienzo, mother of Carminantonio and the one wife in the spine whose own birth record has been found." },
  { href: "/rivetti/", label: "Rivetti", blurb: "Chiara Rivetti, who outlived Pasquale Falco, and the two Rivetti families of Arienzo, one of them gentry, that the archive had to tell apart." },
  { href: "/zampiello/", label: "Zampiello", blurb: "The rarest name in this family by a wide margin and, it turns out, the name of one village." },
  { href: "/wider-family/", label: "The Wider Family", blurb: "Not a pedigree: the brothers and sisters, the households that never left Arienzo, and the Falco who are plainly related but cannot yet be joined." },
];

/* /places/: the place stories that are not named in the menu. */
export const PLACE_STORIES = [
  { href: "/arienzo/", label: "Arienzo", blurb: "A comune of some six thousand people in the province of Caserta, at the western mouth of the Valle Caudina: for at least two centuries the whole world of this family." },
  { href: "/camellara/", label: "Strada Camellara", blurb: "The surname Falco identifies nobody at Arienzo; the street does. Four generations of this family lived on strada Camellara." },
  { href: "/valle-caudina/", label: "The Valle Caudina", blurb: "Three villages, four kilometres apart, in two provinces, and one marriage pool." },
  { href: "/walk/", label: "Walk the Line", blurb: "If you went to Arienzo tomorrow, this is the route: the streets the registers name, and what happened on each." },
  { href: "/journeys/", label: "Journeys", blurb: "The whole geography of this family in five moves, four of which you could walk in a day, and one which you could not." },
  { href: "/rule/", label: "Under Whose Rule", blurb: "Arienzo did not sit still under one flag while this family was in it: Spanish viceroys, Austrians, Bourbons, the French, then Italy." },
  { href: "/diaspora/", label: "Where the Name Went", blurb: "Five towns within a day's walk hold thousands of records under these three surnames, almost none of them this family." },
  { href: "/liguori/", label: "The Bishop", blurb: "A baptism at the Collegiate Church of Sant'Andrea in 1767, the palace beside it, and what that does and does not show." },
];
