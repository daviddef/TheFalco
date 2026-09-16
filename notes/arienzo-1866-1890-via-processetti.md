# Arienzo's missing years, 1866–1890 — reached through the marriage supplements

**Worklist row 62, 16 September 2026.** Read this before spending another pass looking for
Arienzo's post-Unification registers as *registers*.

## Where they are not

- **Antenati**: nothing. `tools/antenati_holdings.py Arienzo` reads the year facet the
  search page leaves in its Solr query, so it lists every year the town holds, not the ten
  rendered. **Nati, Matrimoni and Morti each run 1809–1865 and stop.** This is a facet
  answer, not a probe — it is complete.
- **FamilySearch `M9J1-SZX`, «Italy, Campania, Births, from 1825 to 2000»**: a collection
  this archive had never searched. **563 hits for Arienzo + Falco, of which ZERO are placed
  at Arienzo.** Every one is a neighbouring comune — Pomigliano d'Arco 56, Aversa 54, Sessa
  Aurunca 46, Santa Maria a Vico 42. **The collection holds no Arienzo pages.** A clean nil,
  measured from `content.recordPlace` on all 563, not from the hit count.
- **FamilySearch `M9J1-SMK` Deaths**: 703 hits, 216 placed at Arienzo — the *parish* death
  register, undated, already swept in September. Nothing new.

## Where they are

**FamilySearch collection `2043630` — «Italy, Caserta, Santa Maria Capua Vetere, Civil
Registration (Tribunale), 1866–1929».**

The Arienzo material in it is **marriage supplements, marriage proclamations and bann
supplements, 1891–1910** — *processetti*. A processetto binds in **certified copies of the
civil acts of the couple and their dead parents**, transcribed in full by the clerk who
issued them. **So the lost registers of 1866–1890 survive inside the surviving registers of
1891–1910**, act by act, in the hand of the office that held the originals.

### The sweep

Logged in to `familysearch.org` in the in-app browser, via `javascript_tool`:

```
/service/search/fulltext/search?count=50&m.defaultFacets=on&m.queryRequireDefault=on
  &offset=0&c.collectionId=on&f.collectionId=2043630
  &q.anyPlace=Arienzo&q.text=Falco
```

`1503` hits; page it 50 at a time in parallel batches of 20. **Filter on
`content.recordPlace` — `q.anyPlace` is a weighting, not a filter.** 405 entries are placed
at Arienzo, **202 of them distinct pages** (the rest are duplicate framings of the same
image). Years present: 1891, 1893, 1894, 1896, 1897, 1899, 1900–1910.

Find the extracts with:

```js
/Estratto dal[ ]?registro[^]{0,60}?per l' anno\s*(\d{4})/gi
```

## What one pass recovered

**Seventeen certified extracts, every one of them from a year Antenati does not hold.**
Arienzo civil acts of **1871, 1872, 1873, 1874, 1875, 1878, 1879, 1880, 1881, 1883, 1887,
1889**.

> **THESE ARE HARVESTED, NOT HELD.** Every line below is FamilySearch's machine
> transcription of a handwritten copy — two removes from the register. A machine
> transcription is a candidate, exactly as a contact sheet is. **Nothing here may enter a
> household until the image at the ark has been read.** The OCR is visibly noisy: it renders
> Arienzo as «Chienno», «Criengo», «Orienzo» and «Artento» on the same pages.

### Already held — the consistency check that passed

- **Birth 1873 n.39, RAFFAELE FALCO**, b. 6 April 1873. Declared by **Carminantonio Falco
  di Raffaele**, contadino, 22, **via degli Orti**; mother **Giovanna Arricale fu
  Francesco**. *The archive already holds this act and its address.*
  `3:1:3QS7-L97N-1D3Q`
- **Death 1883 n.60, PASQUALE FALCO**, 44, agricoltore, **via Camellara numero cinque**,
  d. 26 Sep 1883, «del fu Francesco… e della fu Raffaela Falco», husband of **Maria Amalia
  Guida**. Declarants Pasquale Saccavino, 30, and Luigi Maione, 41. *Already held, from the
  processetti volume.* Appears **twice** in this sweep, in two different 1896 supplements.
  `3:1:3QS7-897N-1DLW`, `3:1:3QS7-897N-1D23`

### New candidates — Falco

- **Birth 1880 n.120, ANGELO FALCO**, b. 24 Dec 1880, **Corso Caudino numero ottanta**.
  Father **Vincenzo Falco, 30, vetturale**; mother **Angela Pellone**. Witnesses Giuseppe
  Morgillo, 56, agricoltore, and Domenico Carfora, 46, calzolaio. `3:1:3QS7-997N-PW2F`
- **Death 1889 n.57, VINCENZO FALCO**, 39, *viaticale*, d. 12 Sep 1889 at **Corso Caudino
  numero ottanta**, «nato in Arienzo da **ANGELO**, viaticale, e da **ANNAMARIA CIMMINO**,
  donna di casa». Declarants Gaetano Liparulo, 40, and Pasquale Perrotta, 36, both sarti.
  `3:1:3QSQ-G97N-596`
  **The two acts are one man**: 30 in December 1880 and 39 in September 1889. He named his
  son for his own father, and the archive gains **ANGELO FALCO × ANNAMARIA CIMMINO** — a
  household it has never held. *Cimmino is the surname of Luigi Falco's wife Carolina.*
- **Birth 1887 n.114, MARIA FALCO**, b. 22 Sep 1887, **via Orticelli numero quattro**.
  Father **Giuseppe Falco, 46, agricoltore** (b. c.1841); mother **Nicoletta Nuzzo**.
  `3:1:3QS7-897N-P3N5`

### New candidates — two Falco sisters «fu Matteo»

- **Birth 1872 n.80, ARCANGELO LORENZO CRISCI**, b. 11 Aug 1872, **via Camellara**. Father
  **Antonio Crisci di Arcangelo**, *peperniere*, 48; mother **FILOMENA FALCO FU MATTEO**.
  `3:1:3QS7-897N-5R1`
- **Birth 1874 n.36, ALESSANDRA MORGILLO**, b. 8 May 1874, **piazza Valletta**. Father
  **Carmine Morgillo fu Antonio**, contadino, 26; mother **VINCENZA FALCO FU MATTEO**.
  `3:1:3QS7-897N-16SB`
- Same couple again: **Birth 1878 n.99, ANTONIA MORGILLO**, b. 22 Aug 1878, **piazza
  Valletta numero uno**, Carmine Morgillo 29, **Vincenza Falco**. `3:1:3QS7-L97N-5992`
- And **Birth 1881 n.35, VINCENZO MORGILLO**, b. 6 May 1881, same house, Carmine Morgillo
  33, **Vincenza Falco**. `3:1:3QS7-897N-P7F5`

### And they are not new people — they are tree names that had no documents

**Checked against every corpus in the same pass, with `tools/isitnew.py`, before any of this
was written down.** The tree already holds **MATTEO FALCO × ALESSANDRA CRISCI** (married
24 January 1834) with **nine children — Angela Rosa, Carmela, Filomena, Giuseppe, Vincenza,
Maria, Domenica, Clementina, Antonia — and `records: 0` against every single one.** Nine
names and not one document.

Three of the nine now have one, and the agreement is not circular:

| the tree says | the extract says |
|---|---|
| **Filomena Falco (Crisci)**, dau. of Matteo & Alessandra, m. **Antonio Crisci** | «**FILOMENA FALCO FU MATTEO**», wife of «**Antonio Crisci di Arcangelo**, peperniere, 48», via Camellara, 1872 |
| **Vincenza Falco (Morgillo)**, dau. of Matteo & Alessandra, m. **Carmine Morgillo** | «**VINCENZA FALCO FU MATTEO**», wife of «**Carmine Morgillo fu Antonio**, contadino, 26», piazza Valletta, 1874 |
| **Giuseppe Falco**, son of Matteo & Alessandra, m. **Nicoletta Nuzzo** | «**Giuseppe Falco**, 46, agricoltore», via Orticelli, whose wife is «**Nicoletta Nuzzo**», 1887 |

**Neither source got this from the other.** The tree is a family reconstruction; the extracts
are a clerk's certified copies, machine-read out of a volume nobody has indexed. They agree
on three husbands, on the patronymic, and — for Giuseppe, 46 in 1887, born about 1841 — on an
age that fits a couple married in January 1834.

**Two further things follow, and both are dates the archive did not have.**
**Matteo Falco was dead before 11 August 1872**, because his daughter is «fu Matteo» in that
act. And **Vincenza's first recorded daughter is named ALESSANDRA** — her mother's name, in
a family this archive has documented naming after grandparents for four generations.

**ANGELO FALCO, and why he is a lead and not a merge.** The tree holds an **Angelo Falco,
son of Vincenzo Falco and Andreana Crisci** — generation three — with `records: 0`. The
extracts give an **Angelo Falco × Annamaria Cimmino** whose son Vincenzo was born about 1850
and who lived at Corso Caudino 80. A son called **Vincenzo** is what Angelo son of Vincenzo
would name his boy; and **his brother Luigi Falco married Carolina CIMMINO**, so two
brothers marrying two Cimmino women would be ordinary here. **It is a shape, not a proof, and
the archive does not merge on a shape.**

**PASQUALINA FALCO — the merge this pass refused.** The tree holds a Pasqualina Falco,
daughter of **Pasquale Antonio Falco and Maria Amalia Guida**, and the archive already holds
her birth act, 1877 act 20. The extract's Pasqualina is «**Falco DI Vincenzo**» and is
already married with a daughter born in July 1872. **Different father, impossible dates: two
women.** Had this pass not run `isitnew.py` first, they would have been one.

### New candidates — the wider family

- **Birth 1872 n.71, MARIA CARMINA LOFFREDO**, b. 28 Jul 1872, **via Orticelli**. Father
  Raffaele Loffredo, contadino, 37; mother **PASQUALINA FALCO DI VINCENZO** — «di», so her
  father Vincenzo was **living** in 1872. `3:1:3QS7-997N-16S8`
- **Birth 1879 n.12 — AT FORCHIA, not Arienzo.** Maria Francesca Protolino, father
  Angelantonio Protolino di Gennaro, *carrese*, 36, of Forchia, **luogo detto Sant'Alfonso**;
  mother **TERESA FALCO DI LUIGI**. `3:1:3QS7-L97J-MS7V`
  *Forchia is where Aniello Falco declared his infant son's death in 1937.*
- **Birth 1871 n.125, GIUSEPPE GENOVESE**, b. 13 Nov 1871, **contrada Santa Lucia**. Father
  Vincenzo Genovese di Emidio, 27; mother **GELSOMINA ARRICALE DI VINCENZO**.
  `3:1:3QS7-L97N-1DCZ`
- **Birth 1881 n.5, VINCENZO MORGILLO**, b. 6 Jan 1881, **via Camellara numero nove** —
  father Gennaro Morgillo, 33, agricoltore; mother Maria Giovanna Zimbardo.
  `3:1:3QS7-L97N-5GR` **The second house number ever recovered for strada Camellara.**
- **Birth 1875 n.42, MARIA CARMINA MORGILLO**, via Pizzola n.15, Francesco Morgillo 32 ×
  Angela Landato. `3:1:3QS7-L97J-MSCY`
- **Birth 1887 n.139, MARIANTONIA CRISCI**, **villaggio Crisci numero uno**, Agostino Crisci
  32 × Maria Porzia Lauriello. `3:1:3QS7-997N-P31T`
- **Birth 1879 n.113, PASQUALE RUOTOLO**, **villaggio Crisci numero quattro**, Raffaele
  Ruotolo 36 × Giuditta Guida. `3:1:3QS7-997N-P3YM`

## What this does NOT answer

**Neither VINCENZO FALCO of Andreana Crisci nor GIUSEPPE FALCO of Antonia di Guida is in
any of the seventeen.** Rows 39 and 40 stay open. But the instrument that would hold them is
now identified, and only one name has been swept through it.

## What to do next

1. **Read the images.** Every ark above is citable and renderable. Nothing enters a
   household before that.
2. **Sweep the other names.** This pass ran `q.text=Falco` only. Crisci, Guida, Arricale,
   Annecchino, Carfora, Cimmino, Morgillo and Zampiello have not been run.
3. **Sweep for the extract wording itself**, not for a surname — `q.text=Estratto` — which
   enumerates every processetto in the collection regardless of whose family it is.
