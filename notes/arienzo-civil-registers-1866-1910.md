# Arienzo's civil registers of 1866–1910 were never lost

**8 October 2026.** This archive has spent three worklist rows and most of a month reaching the
Arienzo civil acts of 1866–1890 **through certified copies quoted inside other people's marriage
dossiers** — two removes from the register, fifty-two acts recovered, forty-nine of them still
unread. *The registers themselves have been online the whole time, 5,471 images of them, free to
browse, and this archive published that they were lost.*

**THE PROOF, AND IT IS THE MANUSCRIPT.**

The first leaf of the roll is the filmer's target board:

> **LOCALITY OF RECORD — ARIENZO, CASERTA** · **TITLE OF RECORD — STATO CIVILE. PUBBLICAZIONI,
> MATRIMONI, NASCITE, CITTADINANZE E MORTI** · **ANNI (1866 A 1910)** · *Microfilmed by the
> Genealogical Society, Salt Lake City, at the* **TRIBUNALE DI S. MARIA CAPUA V., CASERTA** ·
> operator **Carfora Vincenzo** · filmed **25 November 1991** · roll 5 · project ITLC 8105A.

A target board is the filmer's label, not the record — so the third image settles it. It is the
**bound cover of the first book**, and the clerk's own paste-on label reads, in his hand:

> «**1866** — **Arienzo** — **Pubblicazioni di Matrimoni**»

**Only the manuscript identifies a register, and here it does.**

## What exists

FamilySearch collection **2043630**, «Italy, Caserta, Santa Maria Capua Vetere, Civil Registration
(Tribunale), 1866–1929» — **the same collection this archive has been searching since 16 September.**
Five Arienzo volumes, now indexed image by image in `data/arienzo-fs-tribunale-images.tsv`:

| waypoint | volume as the catalogue states it | images |
|---|---|---:|
| **`MC55-FNT`** | **Nati, matrimoni, morti 1866-1876** · Nati, matrimoni 1877 · Pubblicazioni 1866 · Cittadinanze 1866-69, 1871-72, 1875 | **1,236** |
| **`MC55-VNL`** | Cittadinanze, morti 1877 · **Nati, matrimoni, morti, pubblicazioni 1878-1900** · Cittadinanze 1879-81, 1883, 1885… | **2,898** |
| `MC55-RM9` | Nati, matrimoni, morti, pubblicazioni 1901-1910 · Cittadinanze 1901, 1909-10 | 1,337 |
| `MC55-BM9` | Allegati (nati, pubblicazioni, matrimoni, morti) 1896-1904 | 2,179 |
| `MC5R-9WL` | Allegati (nati, pubblicazioni, matrimoni, morti) 1905-1910 | 2,234 |

**9,884 images in all. 5,471 of them are the registers; the other 4,413 are the allegati — and the
allegati are the processetti this archive has been reading.** *The route taken was one of the five
volumes. The other four were never opened.*

**EVERY YEAR THIS ARCHIVE CALLED LOST — 1866 to 1890 — IS INSIDE `MC55-FNT` AND `MC55-VNL`.**

## How it was missed, which is the part worth keeping

**A FULL-TEXT SEARCH IS NOT A HOLDINGS LIST.** The whole mistake is in that sentence.

This archive searched collection 2043630 by full text, filtered honestly on `content.recordPlace`,
and found that **the Arienzo pages it returns are 1891–1910** — marriage supplements and bann
proclamations. From that it concluded the collection's *Arienzo holding* begins about 1875 and
effectively about 1891, and published it on `/holdings/`.

*Full text reaches only the pages a recogniser has processed.* It had processed the allegati
volumes. **It had not processed the register volumes, so to a full-text query they do not exist** —
and the archive read their silence as absence. It is the same error as «**an index that stops is not
a record that stops**», which this archive had already written down, in a form it did not recognise:
**a search that returns nothing is not a shelf that holds nothing.**

**And the holdings page's own dek says it:** *«Most of the dead ends in this archive were not failures
of searching but failures of knowing what had been filmed.»* This one was committed on that page.

## The door that was open

```
https://api.familysearch.org/platform/records/waypoints/<WAYPOINT>?cc=<COLLECTION>
```

**No cookie, no token, no browser, and not behind the security service** that answers
`www.familysearch.org/service/*` with a 403. It returns up to 1,000 image arks a page with
`links.next` for the rest, and hands you the DeepZoom template in the same payload. The arks are
ordinary DeepZoom arks — `tools/fsgrab.py` reads them.

`tools/fswaypoint.py` walks it, one request a second, identified in the User-Agent.

**AND THE WAYPOINTS WERE ON THIS MACHINE SINCE 22 SEPTEMBER.** Record Atlas harvested this endpoint
across 3,504 collections — 3.1 million volumes — and `data/fs-waypoints.json` has held Arienzo's five
all along, under `path: ["Arienzo"]`.

> **A FIRST VERSION OF THIS PARAGRAPH SAID «nothing on the map ever pointed at Arienzo». THAT WAS
> TOO STRONG AND IS CORRECTED HERE** rather than quietly swapped. The atlas's Arienzo page does
> carry the collection, and the volumes are tied to the place. **What is true is narrower and more
> useful**, and both halves were checked in the atlas's own built files:
>
> 1. **`data/collections.json` files 2043630 under «Italy» as a COUNTRY** — `places: [{Italy,
>    COUNTRY}]`, `crosses: []` — although its 565 volumes carry a comune in `path` for **99 Caserta
>    comuni**. So on `site/public/p/arienzo.json` it appears as `rank 4, where null, km 294`: a
>    national entry **294 km away, in the same undifferentiated list as Torino and Trento.** It is on
>    the page and it is invisible, which is not the same as absent.
> 2. **The place page renders «the oldest sixty» volumes of 414**, deliberately and for a good reason
>    — rendering every volume took the site to 570 MB. For Arienzo the oldest sixty are **all
>    1809–1817**, so a town whose filmed coverage runs 1809–1910 shows only its first nine years, and
>    the 1866–1910 registers are never on the page.
>
> Neither is a mistake in the atlas's data; both are a shape that hides exactly this kind of volume.
> Reported to David rather than edited: another session is working in that repository today.

## What this costs the old route, and what it does not

**Nothing already read becomes wrong.** The fifty-two harvested acts are still fifty-two acts, the
three read from the image are still read, and the certified copies remain *certified copies made by
the office that held the originals* — for a year whose original is damaged they would still be the
better witness.

**But the method was the long way round and must not be taken again.** A certified copy quoted in a
dossier gives one act, found by whoever happened to marry later; the register gives **every act of
every year, in order, with the index**.

- **Rows 39 and 40** — the two deaths the processetti did not hold. *Of course they did not: a death
  only enters a processetto if a child of the dead married afterwards and left the dossier here.*
  **The death registers of 1866–1900 are `MC55-FNT` and `MC55-VNL`, with their own yearly indexes.**
- **Row 69** — the nine children of Matteo Falco and Alessandra Crisci. Births, in order, with the
  index at the back of each year.
- **Row 95, and the Santa Maria a Vico lead this archive rejected on cost** — *Santa Maria a Vico,
  Cervino and San Felice a Cancello are all in this same collection,* with volumes of their own.
  Ninety-nine comuni of the Caserta plain are. **Forchia, Arpaia and Durazzano are not** — Benevento
  province, a different tribunale, and that gap is unchanged.

## What is NOT yet proved

- **No act has been read from these volumes.** Two leaves were read — the target board and a cover —
  and both say Arienzo 1866. **The years inside are the catalogue's word, not the manuscript's**,
  until a register leaf is magnified. *The catalogue is a contact sheet.*
- **The yearly order within a volume is unknown.** 1,236 images for 1866–1877 is about a hundred a
  year, which fits; where each year starts is not yet established and wants the same treatment
  `notes/register-layout-proof.md` gave the Antenati volumes.
- **Whether the registers duplicate Antenati before 1866 is untested** — these are the *tribunale*
  copies, as Antenati's are, so they may be the same filming or a second one. **A second filming of
  the same page is this archive's cheapest corroboration** and would be worth knowing.
