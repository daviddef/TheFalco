# The Falco Archive

An evidence-first family archive for the **Falco** family of **Arienzo** (province of Caserta,
Campania) — and of Arpaia, Forchia, Benevento, and Brisbane.

> *Falco* is the Latin for falcon. It became a surname twice over: as a Lombard personal name handed
> down as a patronymic, and as a nickname for the quick, the sharp-eyed, or the falconer. It was
> therefore coined independently, many times, in many places. **There is no single founding Falco
> family.** The work of this archive is to establish which Falcos are actually connected, and to say
> plainly where the evidence stops.

## What is here

- **Nine generations**, eight of them resting on a named record, from Pasquale Falco and Chiara
  Rivetti — a married couple of the Collegiate parish of Sant'Andrea at Arienzo in the 1790s — down
  to Brisbane.
- **The three welds** that join the generations: the 1875 death of Vincenzo Falco naming his father
  Pasquale; the 1880 death of Raffaele naming his father Vincenzo; the 1850 birth of Carmine Antonio
  naming his father Raffaele.
- **The Arienzo registers**: baptisms 1672–1738 and 1761–1837, marriages 1754–1900, deaths
  1733–1888 — digitised, and now searchable by machine handwriting recognition.
- **The marriage network**: 361 register pages mentioning a Falco, read for the other names on the
  same pages. Crisci on 113, Morgillo on 76, Martone on 49, de Lucia on 40, Rivetti on 17,
  Arricale on 15. Every in-law surname of the direct line is there, repeatedly.
- **The case against Agostino Falcone** — the generation above Pasquale that is commonly asserted
  and that this archive does not accept. See `/method/`.
- **The name**: 46,749 bearers worldwide, its two independent origins, and why the Portuguese and
  Angolan Falcos are almost certainly a different name entirely.

## Method

| | |
|---|---|
| **Documented** | A named source with a reference, and where possible the scan. |
| **Inferred** | A reasoned conclusion from documented facts, with the reasoning written out so it can be overturned. |
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
data/                            direct-line.tsv, record-citations.tsv, arienzo-baptisms-fulltext.tsv
notes/                           baseline-surname.md, findings.md, QUEUE.md
site/src/data/                   line, places, sources
site/src/pages/                  the archive itself
```

## Sources

Arienzo parish registers, Collegiate Church of Sant'Andrea · Italy, Caserta, Santa Maria Capua Vetere,
Civil Registration (Tribunale), 1866–1929 · Italy, Caserta, Civil Registration (State Archive),
1809–1866 · Italy, Benevento, Civil Registration (State Archive), 1810–1942 · Archdiocese of Benevento
Catholic Church Records, 1575–1908 · FamilySearch · Forebears · Cognomix.

Nothing here yet reaches past 1790. That is the work.
