# The layout of every Arienzo DEATH register, proved from the images

*Work-list row 90. Read 7 October 2026, volume by volume, against the manuscript — not inferred
from a decade, a catalogue label or a neighbouring year.*

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

**Twenty-seven of the twenty-eight death registers 1816–1843 are proved, and every one of them puts
ONE COMPLETE ACT ON EVERY PAGE, TWO TO AN IMAGE, left page then right.**

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
| 1835 | `an_ua14337` | — | **NOT YET PROVED** | the host rate-limited; *not a negative* |
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
