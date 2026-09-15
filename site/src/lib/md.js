/* One markdown renderer for every page that prints a string out of a data file.
 *
 * The corrections page published its own asterisks for a week — 151 entries of
 * literal `**`, 60 of literal backticks — and it was invisible from the source
 * and from the data, showing only in the built HTML. The fix was written into
 * that one page. An audit then found the SAME fault on twenty-three others:
 * /households and /register and /searched, and nineteen /who/ pages printing a
 * plate filename in backticks. The evidence strings are one corpus and they
 * reach half a dozen templates, so the renderer belongs here and not in a page.
 *
 * Escape first, then render — the data file stays plain text and no markup a
 * transcription happens to contain can get through.
 *
 * Bold must be non-greedy and must tolerate a single-asterisk italic inside it:
 * «**San Felice a Cancello, *Matrimoni* 1844**» is the common shape in this
 * archive, and a [^*] bold pattern mis-pairs across it and nests tags wrongly.
 *
 * Guillemets are deliberately NOT auto-italicised. This archive's transcriptions
 * already write «*…*» by hand where they want emphasis, and wrapping them again
 * would double the markup on several hundred quotations.
 */
export const esc = (t) =>
  String(t ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

export const md = (t, u) =>
  esc(t)
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g,
      (_, a, b) => `<a href="${b.startsWith("/") && u ? u(b) : b}">${a}</a>`)
    .replace(/\*\*([\s\S]+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*\n]+)\*/g, "<em>$1</em>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\n\s*\n/g, "<br><br>");
