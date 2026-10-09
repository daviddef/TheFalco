# THERE ARE INDEXES. This archive read 1,350 acts by eye without them.

**Found 13 September 2026.** `notes/QUEUE.md` has said, for months:

> **No index, no indice decennale, no marginal surnames** — all three checked and absent.
> One screenshot per act.

**That is wrong.** Antenati's own catalogue lists, for **Arienzo alone**:

| Type | Volumes |
|---|---|
| **Morti, indice** | **39** |
| **Matrimoni, indice** | **44** |
| **Diversi, indice** | **17** |
| | **100 index volumes** |

And the other towns: **Forchia** 29 *Matrimoni, indice* + 9 *Diversi, indice*; **San Felice a
Cancello** 28 + 27 + 20 + 4 = **79**; Moiano, Paolisi and Arpaia likewise.

## The ark arithmetic — verified

**Arienzo MARRIAGE indexes: 1809 = `an_ua14108`, +1 per year** (1818 = `an_ua14117` ✓), 44 volumes,
so **1809 to about 1852**. Two to four images each.

> **They cannot reach Matteo Falco's marriage.** He married Francesca Crisci about 1760–66, half a
> century before civil registration begins. **That marriage is in the parish books or nowhere** —
> which is the same conclusion the death indexes force about his death. Both of the founder's
> vital events are outside the civil series entirely.

## The DEATH ark arithmetic — verified

**Arienzo death indexes: 1809 = `an_ua14271`, +1 per year.**
Checked: 1818 = `an_ua14280` ✓, 1828 = `an_ua14290` ✓, 1834 = `an_ua14296` ✓.

Each is **one to four images**. A year of the death register is ~50 images and ~90 acts.

## What an index actually contains

The 1818 index (`an_ua14280`, 3 images), column by column:

> **Num.° d'Ordine | Nomi e Cognomi de' Defunti | Patria | Professione | NOMI E COGNOMI DE'
> GENITORI | Giorno della Morte**

**Every death of the year, with BOTH PARENTS NAMED, on one opening.** That is the same information
the sweeps have been extracting act by act, one screenshot at a time.

## Two cautions, because this is not a free lunch

1. **The sort order changes from year to year.** 1818 is alphabetical by **forename** (Crescenzo,
   Colomba, Carmosina, … Maria, Marco). 1834 is by **SURNAME** (Angivino, Arrigale, Attorelli,
   Ambrosio, Cossi, Cimmino, Carfora, Cava, Cioffi…). Check before assuming.
2. **The scans are not always complete.** The 1834 index is **one image covering A–C only** and is
   marked END. A name beyond C is simply not there. **An absence in an index is not a negative** —
   check the image count against the alphabet before recording one.

## What this changes

The standing recipe in QUEUE.md — *"~90 acts/year, ~1,350 total, one screenshot per act"* — should
be replaced. **Read the index first**; go to the act only for the entries that matter. The acts
still carry what the index does not (street, hour, declarants, the «parente» wording that this
archive's best finds have turned on), so the register is not obsolete — but it is no longer the
place to START.

**This is the third wrong negative of the same shape in one day**: the 1814 processetto recorded as
"not in the volume"; San Felice a Cancello recorded as unread when it had never been looked for;
and now indexes recorded as absent when there are a hundred. All three came from checking once,
concluding, and writing the conclusion down as a rule. See `notes/wrong-negatives.md` equivalents
and `notes/antenati-holdings-discovery.md`.

## What to do with them next

- **Sebastiano Falco and Colomba Montefusco** at San Felice — 27 *Morti, indice* volumes to check
  instead of 30 death registers.
- **Gioacchino Falco**, whose parents no record names — his death is given as 14 Feb 1851.
- **The second Giuseppe Rivetti** — which of the two, Giovanna Bega's husband or Lucia Cioffi's.
- ~~Every year of Arienzo deaths 1809–1815~~ — **DONE 13 Sep 2026**, see
  `notes/1809-1814-death-indexes.md`. Six Falco, including a new daughter of generation two.
- **The separate «Morti, indice» series runs 1809–1847 — thirty-nine volumes, matching the
  catalogue count exactly. AFTER 1847 the index is BOUND INTO THE REGISTER ITSELF**, at the front
  (verified in 1851, `an_ua14353`). So every year has a finding aid in one form or the other, and
  the act-by-act sweep was never necessary for any of them.

## AND THE RECORD TYPES THEMSELVES WERE BEING GUESSED — 10 October 2026

`tools/antenati_holdings.py` asked Antenati for six record types:

```python
KINDS = ["Nati", "Matrimoni", "Morti", "Diversi", "Allegati", "Cittadinanze"]
```

**«Allegati» is not a value Antenati uses.** Asking for it returns the facet's own empty answer —
«*Allegati 1 years: 1703*», and **1703 is an artefact year that comes back on every query for every
town** — and this archive read that as *the processetti are not online*. **Moiano, Paolisi and San
Felice a Cancello have carried «unexamined» ever since.**

**The real value is «Matrimoni, processetti», and all four towns have it:**

| town | years | first ark |
|---|---|---|
| **Arienzo** | 1809–1835, 1837–1865 | `an_ua14149` |
| **Moiano** | **1809–1860** | **`an_ua1116121`** |
| **Paolisi** | **1817–1835, 1837–1860** | **`an_ua975596`** |
| **San Felice a Cancello** | **1817, 1819–1822, 1824–1865** | **`an_ua50166`** |

**VERIFIED TWO WAYS BEFORE IT WAS WRITTEN DOWN.** *Arienzo's first ten processetti arks run
**14149–14158**, and the 1814 volume this archive read in September is **`an_ua14154`** — inside
that range at exactly `14149 + (1814 − 1809)`.* **And San Felice's 1817 volume was opened**: 680
images; leaf 2 a Latin parish extract certifying a baptism of **1798**, leaf 3 an Italian one for a
birth of **25 May 1793** «*della Parte Chiesa di **S. Felice Martire di questa Terra d'ARIENZO***».

> **San Felice a Cancello's marriage dossiers bind certificates from Arienzo's own parishes.** *That
> is the reason to read them, and it is not the reason they were opened.*

**The tool no longer guesses.** It reads the town's own `tipologia_ss` facet off the page — the same
principle the rest of the file already followed. **San Felice a Cancello offers thirty-four record
types**, among them «*Matrimoni, indici decennali*», «*Nati, indice*», «*Nati, indice quadriennale*»
and «*Morti, indice*» — **decennial and four-yearly indexes nobody here had asked for, while this
archive read acts by eye.**

*The three towns stay «unexamined» on `/processetti`, deliberately: they are **located, not read**,
and softening the word would hide the work that is left.*

## AND SAN FELICE A CANCELLO'S MARRIAGE INDEX IS THE BEST FINDING AID THIS ARCHIVE HAS MET

`an_ua50137` — the **1815** volume, **four images** — is headed «*Indice de' Casali di S. Felice d'Arienzo per l'anno 1815*» and ruled in four columns:

> «**Nomi e Cognomi degli SPOSI** | **Nomi e Cognomi de' GENITORI** | **Patria** | Giorno della celebrazione del Matrimonio»

**Both spouses, BOTH SETS OF PARENTS, each one's home town and the date — two lines to a marriage,
a whole year in four images.** *The town calls itself «li sei Casali d'Arienzo» at the head of it.*

**The series runs 1815, 1817–1819, 1825–1845, 1847–1849** — twenty-eight volumes of three to six
images each, **about 112 images for twenty-eight years.** *That is the cheapest reading of a town
this archive has ever had available, and it was out of reach only because the tool was asking for a
record type Antenati does not use.*

**1815 read out: no Morgillo × Pesce.** The year's one Morgillo groom is «*34 — **Pasquale
Morgillo**, fu Matteo e [Bordia] Laudato / **Carmina B——**, fu Domenico e Rosa Steffolino*»,
25 September 1815. **1814's forty-two acts read out too** (`an_ua50226`, images 2–23): no Morgillo ×
Pesce, and the year's one Morgillo is a bride — «*Maria Rosa Morgillo, d'anni ventiquattro,
filatrice, figlia maggiore di **Gennaro Morgillo** d'anni settanta, bracciale*».

> **So ANGELA ROSA MORGILLO's parents did not marry at San Felice in 1814, 1815, 1816 or 1817.**
> *What is left there is **1809–1813** — `an_ua50221`–`an_ua50225`, ninety images — or they married
> in another comune.*

## AND SAN FELICE'S WHOLE MARRIAGE RECORD TO 1818 IS NOW READ — the Morgillo × Pesce marriage is not in it

**Five more volumes read act by act on 10 October**: `an_ua50221` (1809), `an_ua50222` (1810),
`an_ua50223` (1811), `an_ua50224` (1812), `an_ua50225` (1813) — **ninety images** — on top of 1814
(`an_ua50226`, forty-two acts) and the 1815 index.

> **THE DENSITY IS STATED BECAUSE IT DECIDES WHETHER THE NEGATIVE IS WORTH ANYTHING.** A first pass
> put **fourteen images on one sheet**. This archive's own rule, written after the 1819 sweep, is
> **nine** — «*at four columns the names are gone, and a negative off an illegible sheet is worth
> nothing*». **Everything here was re-read at nine images to a sheet before a word of it was written
> down**, 1814 included.

**NOT ONE MORGILLO × PESCE IN SEVEN YEARS.** *Both surnames are in the town and they never meet:*

- **Nicola Morgillo**, 19, «*figlio del fu **Biaggio Morgillo** e della Sig.ra **Rosa d'Addio***»,
  married **Anna della Marca** in **1809**
- **Antonio Morgillo**, 25, «*figlio del fu **Giuseppe Morgillo** e di **Angela [Pascarello]***»,
  married a **Basilicata** in **1810**
- **Gelsomina Morgillo**, 29, «*figlia maggiore del fu **Giuseppe Morgillo** … e di **Angela
  Pascarello***», married in **1812** — *the same house as Antonio*
- **Rachele Morgillo**, 29, «*figlia del fu **Pasquale***», and **Maria Rosa Morgillo**, 24,
  «*figlia maggiore di **Gennaro Morgillo**, d'anni settanta*», both married in **1814**
- **Pasquale Morgillo**, «*fu Matteo*», married **Carmina B——** in **1815**
- And **Pesce**: *Pellegrino Pesce «figlio di **Giuseppe Pesce**» (1811), Tommaso Pesce's son (1814),
  **Giuseppa Pesce** and **Catarina Pesce** as mothers.*

### SO THE QUESTION MOVES TOWNS

**Angela Rosa Morgillo was born at San Felice on 24 February 1818, and her parents did not marry
there** — not in 1809, 1810, 1811, 1812, 1813, 1814, 1815, 1816 or 1817. *The last two were read in
September; the rest today.*

> **They married in another comune.** The places these registers themselves keep naming are
> **Santa Maria a Vico d'Arienzo**, **Arienzo**, **Cancello**, **Maddaloni** and **Forchia** — and
> the bride's own town is the one to try first, which is exactly what the marriage act would name
> and no other document will.
