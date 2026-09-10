/* Which page of this archive writes a surname up.
 *
 * The de Franceschi site carries a «where it is written up» column on its
 * roster, so that a name in a list is a door into the prose rather than a dead
 * string. This is the Falco equivalent: a surname to the page that argues about
 * it. Only surnames that genuinely have a page are listed — an entry here is a
 * promise that the page discusses the family, not merely that it mentions it.
 */
export const WRITTEN_UP = {
  ANNECCHINO: ["/annecchino", "Annecchino"],
  ANNICCHINO: ["/annecchino", "Annecchino"],
  ZAMPIELLO:  ["/zampiello", "Zampiello"],
  MAIONE:     ["/maione", "Maione"],
  MAJONE:     ["/maione", "Maione"],
  FERRARA:    ["/ferrara", "Ferrara"],
  FERRARO:    ["/ferrara", "Ferrara"],
  CRISCI:     ["/crisci", "Crisci"],
  RIVETTI:    ["/rivetti", "Rivetti"],
  MORGILLO:   ["/morgillo", "Morgillo"],
  FALCO:      ["/direct-line", "The direct line"],
  LIGUORI:    ["/liguori", "The Bishop"],
  CIOFFI:     ["/method", "The Cossi/Cioffi reading"],
  COSSI:      ["/method", "The Cossi/Cioffi reading"],
};

/** [href, label] for a surname, or null. */
export function writtenUp(surname) {
  return WRITTEN_UP[String(surname || "").toUpperCase()] || null;
}
