# The Arienzo «Diversi» register — a whole series this archive had never opened

**17 September 2026.** Found while hunting for the separate filming of the birth *tavole*
(work-list row 10). It is not the tavole. It is something better.

## What it is

The title page, `an_ua14071` image 1:

> **Atti per le nascite avvenuti in un viaggio di mare, Per le Ricognizioni, Adozioni, Persone
> defunte e fuori del proprio domicilio, e Morti-Nati** — Provincia di Terra di Lavoro,
> Circondario di Arienzo, Distretto di Nola, Comune di Corpo d'Arienzo.

Births at sea · recognitions · adoptions · **people who died away from their own home** ·
stillbirths.

**The third of those is why this matters.** When an Arienzo person died somewhere else, the
comune where they died drew the act, and a certified copy was transmitted to Arienzo — «*abbiamo
ricevuto per mezzo del Signor Sottintendente di questo Distretto copia certificata dal Sindaco e
Cancelliere del Comune di …, d'un atto di morte del tenor seguente*» — and **copied into this
register in full**. Every clause of the original survives: age, trade, street, both parents,
whether they were dead, and the surviving children with their ages.

**So a death this archive cannot find in the Arienzo death register may be here, because the
person did not die at Arienzo.** Rows 39 and 40 — Giuseppe Falco of Antonia di Guida, and
Antonia di Guida herself — are exactly that shape.

## Where it is

`tools/antenati_holdings.py Arienzo` lists **Diversi: 40 years — 1703, 1812–1813, 1820,
1822–1835, 1837–1840, 1842–1850, 1853, 1855–1860, 1864–1865**, first ark `an_ua14064`.

The volumes are **one to eight images each** — the whole series is smaller than a single year
of deaths. Confirmed arks so far, by asking `tools/antenati.py ids` for the breadcrumb year:

| ark | year | images |
|---|---|---|
| `an_ua14056` | 1835 | 1 |
| `an_ua14057` | 1837 | 1 |
| `an_ua14058` | 1839 | 1 |
| `an_ua14059` | 1840 | 2 |
| `an_ua14060` | 1846 | 2 |
| `an_ua14061` | 1848 | 1 |
| `an_ua14062` | 1849 | 1 |
| `an_ua14071` | 1825 | 4 |
| `an_ua14080` | 1831 | 2 |
| `an_ua14095` | 1848 | 8 |

**THE ARITHMETIC IS NOT LINEAR AND MUST NOT BE GUESSED.** `14056`–`14062` run ascending by year
with gaps, but `14071` is 1825 and `14058` is 1839 — so at least two sub-series are interleaved
in this ark range. **Probe each ark and read the breadcrumb**; do not extrapolate. This archive
has already been burned three times by ark arithmetic (see the method page).

**Antenati rate-limits hard.** Seven probes at 0.8 s apart earned a 403 on the eighth. Space
them, and remember a 403 is «wait», never «missing».

## What the 1825 volume holds — read from the image

Two acts, both deaths of Arienzo people that happened elsewhere.

**Act 1**, received from the Comune of **Nola**, act 179 of 1825, drawn 5 November:

> «*…è morto nella **Masseria di Domenico de Luca** … nel luogo detto **Fabrica**, nominato
> **CRESCENZO CRISCI**, di anni **cinquantatré**, **marito di ANGELA QUOTOLO**, nato in
> **Arienzo** … di professione **colono** … **figlio di ALESSANDRO CRISCI DEFUNTO e di CARMINA
> SORRINO**, domiciliata nel medesimo Comune di Arienzo … il quale **ha lasciato superstiti
> quattro figli, cioè ANIELLO d'anni QUINDICI, SANTE d'anni DODICI, CARMINA d'anni DIECI e MARIA
> ROSA d'anni CINQUE***»

Declared at Nola by two brothers of the dead man — **Domenico Crisci**, colono, and **Gabriele
Crisci** — both domiciled at Arienzo. He died **4 November 1825**.

**Act 2**, received from the Comune of **Aversa**: a woman of fifty-five who died **«nel Real
Stabilimento delle Donne Matte»**, the royal asylum for insane women at Aversa, on 16 October.
The clerk left her profession, her domicile and **both her parents blank** — dashes across the
page. A person who died in an institution and whose family the institution did not know.

## What it does for the archive

**CRESCENZO CRISCI × ANGELA QUOTOLO were already here**, but only as the parents of **Aniello
Crisci**, who married **Giovanna Falco** on 6 September 1829. This act now gives that household
its own document: his death, his age, his trade, **his own parents**, and **Aniello's birth year
— about 1810, so nineteen at his wedding.**

**AND IT REMOVES THE AGE OBJECTION TO A LINK THIS ARCHIVE HAD FILED AS A RESEMBLANCE.**
**ALESSANDRA CRISCI**, who married **Matteo Falco** on 24 January 1834, has her parents given in
the marriage index as «*CRISCI [forename lost to the fold shadow], [QUO]TOLO ANGELA*». The
archive wrote: «*Angela Quotolo is not a rare name at Arienzo, so it is filed as a resemblance
and not a fact*» — and that stands, because the forename is still unread.

But the obvious objection — *she is not among his four surviving children* — **is answered by
the act's own arithmetic**. The four are aged **15, 12, 10 and 5**, and **he was fifty-three**.
A man of fifty-three whose eldest living child is fifteen either married at thirty-eight or has
older children who are not on this list. **The list is of MINORS**, which is what these acts
record, because minors need a tutor. **An adult daughter would not appear, and Alessandra —
marrying in 1834 — need only have been born before 1810.**

**It is still a resemblance. It is no longer a resemblance with a hole in it.**

## What to do next

1. **Probe the rest of the ark block and build the year map**, patiently, one request every few
   seconds. Forty volumes, most of them one or two images.
2. **Read every one for FALCO** — the whole series is about 120 images, comparable to a single
   year of the death register, and it covers 1812–1865.
3. **Look first at 1849 onward** (`an_ua14061`, `an_ua14062` and the 1853–1865 volumes), because
   **Giuseppe Falco of Antonia di Guida is alive in November 1849 and in no volume since**, and
   the one place his death could hide is a comune that is not Arienzo.
