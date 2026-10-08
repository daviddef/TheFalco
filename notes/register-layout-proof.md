# The layout of every Arienzo DEATH register, proved from the images

*Work-list row 90. Read 7 October 2026, volume by volume, against the manuscript — not inferred
from a decade, a catalogue label or a neighbouring year.*

> **AND THERE IS A SECOND SHELF THIS NOTE DOES NOT COVER — 8 October 2026.**
> Everything here is the **Antenati** series, 1809–1865. Arienzo's registers of **1866–1910** are on
> FamilySearch, 5,471 images, and their layout is a different one: **five separate books to the
> year** — Pubblicazioni, Matrimoni, Nascite, Morti, Cittadinanze — each with a cover and a printed
> title page, and **every year carrying an «INDICE ANNUALE»**, which the Antenati volumes of this
> note mostly do not. Proved for 1866 in
> [`arienzo-civil-registers-1866-1910.md`](arienzo-civil-registers-1866-1910.md); 1867 onward is
> unproved.
>
> **Two things here carry straight over.** *Duplicate exposures* — the 1991 filmer repeated the index
> leaf and the target board, exactly as the Antenati filmings repeat pages, and a second exposure
> counted as a second leaf inflates every page count. And **the discipline itself**: the arithmetic
> «sixty-two images, a hundred and twenty-two acts, so two acts an image» is the same shape as the
> band assumption that published two volumes as read in full when they were half read. *It is written
> down there as arithmetic and marked as not proved.*

## Why this had to be done

A band sweep of one half of each image reads half the acts **consistently**, so the output looks
like a complete sweep and nothing appears to be missing. In 1809 and 1811 both Falco acts that had
already been found happened to sit on right pages, so the method confirmed itself — and two volumes
were published as «read in full» when they were half read.

**Until a volume's layout is proved, every nil published from a sweep of it is only as good as a
guess about how the clerk used the page.**

## The method, which costs one small image per volume

    python3 tools/antenati.py strip <ark> <n> <n+1> --band 0.05 0.21 --half LR --width 1400

That stacks the «Num. d'ordine» line from both halves of two consecutive images. Read the four
numbers. **If image *n* gives N and N+1, and image *n+1* gives N+2 and N+3, there are two acts to
an image, one to a page, and a sweep must use `--half LR`.**

**THE BAND DRIFTS BETWEEN VOLUMES AND THIS IS THE TRAP.** A band that frames the number line in
1816 (`0.055 0.075`) catches the date line instead in 1818, and misses the line entirely in 1822 —
the page sits at a different vertical offset in each volume's filming. **`0.05 0.21` is the band
that holds across the whole series**; it wastes space and never loses the line. *A recipe that
worked on the volume you tested is not a recipe for the series.*

## THE RESULT: THE LAYOUT IS UNIFORM, AND THE EXISTING SWEEPS WERE SOUND

**ALL TWENTY-EIGHT death registers 1816–1843 are proved, and every one of them puts ONE COMPLETE ACT
ON EVERY PAGE, TWO TO AN IMAGE, left page then right.**

| year | ark | images read | act numbers | |
|---|---|---|---|---|
| 1816 | `an_ua14318` | 12–13 | 20 · 21 · 22 · 23 | |
| 1817 | `an_ua14319` | 20–21 | 36 · 37 · 38 · 39 | |
| 1818 | `an_ua14320` | 14–15 | 24 · 25 · 26 · 27 | |
| 1819 | `an_ua14321` | 9–14 | 14 · 15 · 16 · 17 · **16 · 17** · 18 · 19 · 20 · 21 · 22 · 23 | **image 11 re-films image 10** |
| 1820 | `an_ua14322` | 12–13 | 20 · 21 · 22 · 23 | |
| 1821 | `an_ua14323` | 10–11 | 16 · 17 · 18 · 19 | |
| 1822 | `an_ua14324` | 12–13 | 20 · 21 · 22 · 23 | |
| 1823 | `an_ua14325` | 16–17 | 28 · 29 · 30 · 31 | a «BLEED THROUGH» card is filmed between leaves |
| 1824 | `an_ua14326` | 14–15 | 16 · 17 · 18 · 19 | |
| 1825 | `an_ua14327` | 10–11 | 16 · 17 · 18 · 19 | act 17's declarant reads **Giuseppe Falco** — *checked with `isitnew.py` and ALREADY HELD; the 1825 sweep records him declaring in the Cioffi household. Not a find.* |
| 1826 | `an_ua14328` | 14–15 | *blank* · 23 · 24 · 25 | a blank left page mid-volume |
| 1827 | `an_ua14329` | 12–13 | 20 · 21 · 22 · 23 | |
| 1828 | `an_ua14330` | 14–15 | 20 · 21 · 22 · 23 | |
| 1829 | `an_ua14331` | 18–19 | 26 · 27 · 28 · 29 | |
| 1830 | `an_ua14332` | 16–17 | 20 · 21 · 22 · **«Ventuno bis»** | an interpolated act, written freehand on a blank leaf |
| 1831 | `an_ua14333` | 16–17 | 26 · 27 · 28 · 29 | |
| 1832 | `an_ua14334` | 12–14 | 18 · 19 · 20 · 21 | |
| 1833 | `an_ua14335` | 16–17 | 26 · 27 · **26 · 27** | **image 17 re-films image 16** — same foglio 163 |
| 1834 | `an_ua14336` | 14–15 | 24 · 25 · 26 · 27 | |
| 1835 | `an_ua14337` | 12–13 | 16 · 17 · 18 · 19 | *proved 8 Oct, after the rate limit lifted* |
| 1836 | `an_ua14338` | 14–15 | 20 · 21 · 22 · 23 | |
| 1837 | `an_ua14339` | 20–21 | 28 · 29 · 30 · 31 | |
| 1838 | `an_ua14340` | 14–15 | 22 · 23 · 24 · 25 | |
| 1839 | `an_ua14341` | 18–19 | 24 · 25 · 26 · 27 | |
| 1840 | `an_ua14342` | 14–15 | 24 · 25 · 26 · 27 | the number is **printed** in large type from this year |
| 1841 | `an_ua14343` | 14–15 | 22 · 23 · 24 · 25 | |
| 1842 | `an_ua14344` | 14–15 | 18 · 19 · 20 · 21 | |
| 1843 | `an_ua14345` | 12–13 | 14 · 15 · **14 · 15** | **image 13 re-films image 12** — same foglio 149 |

**So the sweeps this archive has published over this series were sound.** Every recorded sweep used
`--half LR`, and with one act to a page that reads both. *No single-half sweep is recorded anywhere
in `notes/`.* **The nils stand.**

## THREE THINGS THE PROOF FOUND THAT NOTHING ELSE WOULD HAVE

**1. THREE VOLUMES CARRY DUPLICATE EXPOSURES.** In 1819, 1833 and 1843 one opening is filmed twice
in succession — the same two act numbers, the same foglio number, a different file and a different
image id. **Image count is therefore NOT page count**, and any arithmetic of the form
«images × 2 = acts» is wrong for at least three volumes in twenty-eight. *It was tested: the three
images differ by as much as any other neighbouring pair, so the duplication is in the filming, not
in the tooling.*

**2. THE HIGHEST ACT NUMBER IS NOT THE ACT COUNT EITHER.** 1830 carries an act numbered
«**Ventuno bis**», written out by hand on a leaf with no printed form. An interpolated act is
invisible to any check that counts forwards from one.

**3. A BLANK PAGE IS NORMAL.** 1826's image 14 has nothing on its left page. *An empty tile in a
contact sheet is not evidence that a sweep failed.*

## What is NOT proved by this

This covers **the Arienzo civil DEATH registers 1816–1843 only**. The birth registers, the marriage
registers, the processetti and every volume of another comune are untouched here, and the coverage
rows for them still state no layout. **The method above costs about twenty seconds and one small
image per volume; there is no reason for any of them to stay unproved.**

---

# The BIRTH registers, and the year the form changed

*Read 7 October 2026, same method, same band.*

## THE BIRTH REGISTERS ARE NOT LAID OUT LIKE THE DEATH REGISTERS, AND THEY CHANGE IN 1820

| years | form | acts per image |
|---|---|---:|
| **1816 – 1819** | the old single-column act, one complete act to a page | **2** |
| **1820 – 1848** | the printed **«ATTO DI NASCITA ‖ INDICAZIONE»** double-column form | **1** |

**Proved volume by volume:**

| year | ark | act numbers at images 20–21 | |
|---|---|---|---|
| 1816 | `an_ua14413` | 36 · 37 · 38 · 39 | old form, **two to an image** |
| 1817 | `an_ua14414` | 39 · 40 · 41 · 42 | printed *sedici* struck and corrected to *diciassette* |
| 1818 | `an_ua14415` | 2 · 3 · 4 · 5 | low numbers this deep in the volume — *it is bound twice, as the progress note says* |
| 1819 | `an_ua14416` | 36 · 37 · 38 · 39 | **the last year of the old form** |
| 1820 | `an_ua14417` | 18 · 19 | **the new form begins — one to an image** |
| 1821 | `an_ua14418` | 18 · 19 | |
| 1822 | `an_ua14419` | 19 · 20 | |
| 1823 | `an_ua14420` | 18 · 19 | |
| 1824 | `an_ua14421` | 19 · 20 | |
| 1825 | `an_ua14422` | 19 · 20 | |
| 1826 | `an_ua14423` | 19 · 20 | act 19's tail names **Maria Falco** with Francesco Cioffi — *already held* |
| 1827 | `an_ua14424` | 19 · 20 | |
| 1828 | `an_ua14425` | 18 · 19 | |
| 1829 | `an_ua14426` | 18 · 19 | |
| 1830 | `an_ua14427` | 19 · 20 | |
| 1831 | `an_ua14428` | 19 · 20 | |
| 1832 | `an_ua14429` | 18 · 19 | |
| 1833 | `an_ua14430` | 18 · 19 | |
| 1834 | `an_ua14431` | 19 · 20 | |
| 1835 | `an_ua14432` | 19 · 20 | |
| 1836 | `an_ua14433` | 18 · 19 | |
| 1837 | `an_ua14434` | 19 · 20 | |
| 1838 | `an_ua14435` | 19 · 20 | |
| 1839 | `an_ua14436` | 19 · 20 | act 19's tail names a mother **GIOVANNA FALCO, 34** — *a lead, not a find; see below* |
| 1840 | `an_ua14437` | 19 · 20 | the act number is **printed** from this year |
| 1841 | `an_ua14438` | 19 · 20 | |
| 1842 | `an_ua14439` | 19 · 20 | |
| 1843 | `an_ua14440` | 19 · 20 | |
| 1844 | `an_ua14441` | 15 · 16 | |
| 1845 | `an_ua14442` | 19 · 20 | |
| 1846 | `an_ua14443` | 19 · 20 | |
| 1847 | `an_ua14444` | 18 · 19 | |
| 1848 | `an_ua14445` | 19 · 20 | |

**The archive's own numbers agree.** 1819 is *«74 images, 137 acts»* — 1.85 to an image. 1825 is
*«all 134 acts on 133 folios, images 2–141»* — one to an image. **The change is in the data as well
as on the page.**

## WHY THIS MATTERS MORE THAN THE DEATH SERIES DID

**In the new form a single act SPANS AN OPENING.** The right page carries the act's HEAD — number,
date, declarant, the child — in two printed columns, the second being the parish *Indicazione* of
the baptism, numbered identically. **The LEFT page of the NEXT image carries that act's TAIL: the
mother, the witnesses and the signature.**

So from 1820 on:

- **a sweep of the right half sees the declarant and the child, and NEVER the mother;**
- **a sweep of the left half sees the mother, and never the act number or the declarant.**

**THIS IS THE MECHANISM BEHIND A FAILURE THIS ARCHIVE ALREADY KNEW THE SYMPTOM OF.** The 1831 birth
row says of act 71: *«The declarant here is the father, a CIOFFI. A sweep of the declarant line sees
no Falco in this act at all — the Falco is the mother, three lines over on the facing leaf.»* **That
is not a quirk of 1831. It is the form, every year from 1820, and it is why the re-reads at the
PARENTS band kept finding Falco mothers the first passes could not have seen.**

**The practical rule, which was never written down:** *for an Arienzo birth register of 1820 or
later, a sweep must read **both halves** and must treat the left half as belonging to the PREVIOUS
act.* A contact sheet that pairs image *n* right with image *n* left is pairing two different
families.


---

## BOTH SERIES ARE NOW COMPLETE — 8 October 2026

**Sixty-one volumes proved from the manuscript**: the Arienzo civil DEATH registers **1816–1843**
(28 volumes, two acts to an image throughout) and the BIRTH registers **1816–1848** (33 volumes,
two to an image until 1819 and **one** from 1820). *Nothing in either series was taken on trust from
a neighbouring year.*

## A LEAD THAT IS NOT A FIND, AND WHY IT IS NOT PUBLISHED

Proving the 1839 birth register meant looking at two of its images, and the tail of **act 19** names
the mother as «*… è nata da **GIOVANNA FALCO** sua moglie legittima, di anni **trentaquattro***» —
a Falco mother, about **1805**.

**It is written down here as a LEAD and nowhere else.** Three reasons, and each alone is enough:

1. **It was read off a contact-sheet band, and a contact sheet is triage.** This archive has twice
   had a band-resolution reading contradicted by the act in the very same volume.
2. **The 1839 register has never been swept.** `isitread.py` says so, and the work list already
   records **1839–1844 — six volumes** as an open gap. *One act seen in passing is not a sweep, and
   publishing it would make an unswept year look read.*
3. **The surname alone identifies nobody** here, and this archive holds more than one Giovanna Falco.

*When 1839 is swept properly, act 19 is where to start.*
