# The Falco Archive

An evidence-first family archive for the **Falco** family of **Arienzo** (province of Caserta,
Campania) — and of Arpaia, Forchia, Benevento, and Brisbane.

> *Falco* is the Latin for falcon. It became a surname twice over: as a Lombard personal name handed
> down as a patronymic, and as a nickname for the quick, the sharp-eyed, or the falconer. It was
> therefore coined independently, many times, in many places. **There is no single founding Falco
> family.** The work of this archive is to establish which Falcos are actually connected, and to say
> plainly where the evidence stops.

## What is here

- **Nine generations, every one documented**, from **Matteo Falco** and **Francesca Crisci** of the
  parish of Sant'Andrea at Arienzo — whose children were baptised there from 1767 — down to Brisbane.
- **Pasquale Falco's baptism, 24 October 1767**, naming his parents: *infantem natum ex Mattheo Falco,
  ed Francisca Crisci … qui nominatus est Paschalis*. It replaced an asserted ancestor,
  Agostino Falcone, for whom no record has ever been produced.
- **Three reconstructed households** — Matteo's, Pasquale's and Vincenzo's — 26 register entries with
  citations, including the children who died: Maria Angela, baptised February 1802, buried March 1805
  *aetatis suae annorum 3 circiter*.
- **The marriage that welds the line**: *Vincentium Falco filium Paschalis, e Clarae Rivetta, e
  Andreanam Crisci filiam Arcangeli* — four people named in one sentence.
- **A date contradiction closed**: an entry machine-read as 1780 says, in Latin words,
  *octogesimo nono* — 1789. Words beat digits.
- **The Arienzo registers**: baptisms 1672–1738 and 1761–1837, marriages 1754–1900, deaths 1733–1888.
  11.3 MB of machine transcription harvested and searched — 2,059 baptism pages, 1,596 marriage and
  death pages.
- **The bishop next door** — the church in these registers was the second seat of the bishop of
  Sant'Agata de' Goti, and from 1762 to 1775 that bishop was **Alfonso Maria de' Liguori**, who lived
  in the palace beside it. He did not baptise anyone here; the archive says so plainly.
- **The names**: Falco, 46,749 bearers and two independent origins; **Zampiello, about 123 in the
  world** — 37 of them in Italy.

## Method

| | |
|---|---|
| **Documented** | A named source with a reference, and where possible the scan. |
| **Inferred** | A reasoned conclusion from documented facts, with the reasoning written out so it can be overturned. |
| **Superseded** | Asserted in the family record, and now displaced by a document that says otherwise. |
| **Disputed** | Asserted in the family record but unsupported, or contradicted, by what can be seen. |
| **Family lore** | Told, remembered, not corroborated. Kept because it is precious; labelled because pretending otherwise is how family myths become family history. |

**Living people are omitted from the build entirely** — not hidden, not gated, not present in the
output. A removal request is honoured within days, without argument and without requiring a reason.

## Running it

```bash
cd site
npm install
npm run dev      # http://localhost:4322
npm run build    # static output in site/dist
```

Deploys to GitHub Pages on every push to `main`.

## Layout

```
data/                            direct-line.tsv, record-citations.tsv, households.tsv,
                                 falco-parentage.tsv, arienzo-pages.tsv,
                                 arienzo-marr-death-pages.tsv
notes/                           baseline-surname.md, findings.md, QUEUE.md
site/src/data/                   line, places, sources
site/src/pages/                  the archive itself
```

## Sources

Arienzo parish registers, Collegiate Church of Sant'Andrea · Italy, Caserta, Santa Maria Capua Vetere,
Civil Registration (Tribunale), 1866–1929 · Italy, Caserta, Civil Registration (State Archive),
1809–1866 · Italy, Benevento, Civil Registration (State Archive), 1810–1942 · Archdiocese of Benevento
Catholic Church Records, 1575–1908 · FamilySearch · Forebears · Cognomix.

The line now reaches 1767 with a document, and Matteo Falco was an adult by 1759. Above him the
baptism register has a gap between 1738 and 1761. Closing it is the work.
