# How to DISCOVER what Antenati holds — not guess it

**Found 13 September 2026, while hunting Orazio Morgillo's marriage.**

Until today this archive reached Antenati volumes by **guessing arks from an arithmetic rule**
(«Arienzo deaths 1809 = `an_ua14311`, +1 per year»). That rule was derived by hand, it only ever
covered Arienzo, and it is why **San Felice a Cancello — the birthplace of generation four's wife —
was believed to be unavailable for five years. It was there the whole time.**

## The endpoint

```
https://antenati.cultura.gov.it/search-registry/?localita=<TOWN>
https://antenati.cultura.gov.it/search-registry/?localita=<TOWN>&tipologia=Nati
```

It is a server-rendered page and **the ark ids are in the HTML**, so plain `curl` with the usual
browser User-Agent and Referer gets them. Pull them with `grep -o 'an_ua[0-9]*'`.

**Limits.** It returns **ten results at a time** and the pagination parameters have not been worked
out — `&start=` is ignored. `&tipologia=` DOES change the result set and is the useful lever.
Behind it is a Solr index (the query is left in an HTML comment), but the Solr host is an internal
address and is not reachable.

**The right way to use it**: get a handful of arks for a town, resolve their labels with
`python3 tools/antenati.py ids <ark>`, and **recover the series arithmetic from those** — the arks
run +1 per year within a series, and the series end where the next comune alphabetically begins.

## What that established today

| Town | Series | Arks | Notes |
|---|---|---|---|
| **San Felice a Cancello** | Caserta, *Stato civile napoleonico e della restaurazione*. Catalogued as **«San Felice (oggi San Felice a Cancello)»** — which is why it never turned up. | **Matrimoni 1809 = `an_ua50221`, +1/year** (so 1817 = `an_ua50229`) | **Wholly new to this archive.** In its own acts the town calls itself **«Comune di sei Casali d'Arienzo»** — the Six Hamlets of Arienzo. |
| **Forchia** | Caserta, same fondo | **Nati 1820 = `an_ua29049`, +1/year, running to 1861 = `an_ua29090`** | The series then moves to *Formicola*. Forchia after 1861 is in the **Benevento** archive's *Stato civile italiano*, which has NOT been located. |
| Forchia | Benevento, *Stato civile napoleonico* | `an_ua1115155` ff., 1809–1829 | A second, overlapping holding for the same town in a different archive. |

**The lesson for the queue**: before recording a town as unavailable, query
`search-registry/?localita=` for it. The archive's own `data/antenati-processetti.tsv` surveys five
towns; it does not survey San Felice a Cancello at all, and San Felice is where generation four's
wife was born.

---

# Orazio Morgillo × Vincenza Pesce — SEARCHED, NOT FOUND

**Volume**: San Felice a Cancello, Matrimoni **1817** — `an_ua50229`, 22 images, ~40 acts
**Read**: name band of every act, 13 September 2026
**Result**: **no Orazio Morgillo, and no Vincenza Pesce.** The marriage is not in this volume.

This was the right volume to try: Angela Rosa Morgillo was born at San Felice on 24 February 1818,
so the marriage should fall in 1816 or 1817, and a couple normally married in the bride's parish.

**But the sweep was not empty.** It puts both surnames in the town:

- **Morgillo at San Felice** — *Andriana Morgillo*, mother of a bride (act on img 3R);
  *Antonia Morgillo*, mother of a groom (img 4L); a second *Antonia Morgillo*, 42 (img 8L);
  *Angiola Morgillo* (img 19R). The Morgillo were established at San Felice, which is the first
  time this archive has been able to say so.
- **Pesce at San Felice** — **GIOVANNA PESCA, 48, *filatrice*, of strada detta de' Giannacci,
  «figlia delli furono FELICE PESCE ed ANTONIA CERRONE»**, married 8 March 1817; and
  **VENERANDA PESCE**, ~50, mother of a bride (img 15R).

> **The lead worth following**: if Vincenza Pesce was Giovanna's sister, her parents are
> **Felice Pesce and Antonia Cerrone**. That is a testable proposition and not a claim.

## Where to look next, in order

1. **San Felice Matrimoni 1816 = `an_ua50228`** — the other half of the window. Not yet read.
2. **Angela Rosa Morgillo's own birth act**, San Felice, 24 February 1818. It would name both her
   parents outright and settle this without the marriage. The *Nati* series for San Felice has
   **not** been mapped — `an_ua50395` was guessed at and turned out to be marriages. Query
   `search-registry/?localita=San+Felice+a+Cancello&tipologia=Nati` and resolve the labels.
3. San Felice deaths, for Orazio's or Vincenza's own act naming their parents.

---

# Forchia 1897 — NOT REACHED

**Target**: the birth of **Filomena Annecchino, 10 April 1897**, which would name her mother and
settle the Annecchino descent at generation seven.

**Established**: Forchia's Caserta-held births run **1820 (`an_ua29049`) to 1861 (`an_ua29090`)**
and then stop — `an_ua29110` and `an_ua29126` are already *Formicola*. After unification Forchia is
in **Benevento** province, and its post-1861 registers are in the **Archivio di Stato di Benevento,
Stato civile italiano** — a fondo this archive has not located.

**Next step**: `search-registry/?localita=Forchia&tipologia=Nati`, take the arks that resolve to a
Benevento label, and recover that series' arithmetic. The search page confirms Forchia records
exist for years up to **1899**, so 1897 is held; only the ark is missing.
