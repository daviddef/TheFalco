# Arienzo MARRIAGES 1858 and 1859 — a sweep this archive had ALREADY DONE, and the three things it still turned up

**Read 23 September 2026 from the images. It should not have been read at all.**

**`site/src/data/searched.json` already carried the answer**, recorded **21 September 2026**:

> «*Arienzo civil MARRIAGE registers — ANTENATI `an_ua14261` (35 images), `an_ua14262` (39), `an_ua14263` (28), `an_ua14264` (38). **Every act read at the name band** … **1858 AND 1859 HOLD NO FALCO AT ALL** — thirty-nine and twenty-eight images, every act read.*»

**My image counts came out at thirty-nine and twenty-eight. The earlier pass was right, and I repeated it.**

## HOW THE DUPLICATION HAPPENED — the archive contradicted itself and I believed the wrong half

**Work-list rows 39 and 40 both said**, in terms: *«the Arienzo marriage registers for **1857–1860** — four volumes, `an_ua14261`–`an_ua14264` — **have never been swept for Falco**»*. **`searched.json` said they had, two days earlier.** Two files of this archive disagreed about whether four volumes had been opened, and **nothing in the nineteen-step chain compares them** → [[archive-contradicts-itself]].

**I read `notes/QUEUE.md` and the work list before starting, and that was not enough.** The coverage data IS the record of what has been read; the work list is a record of what someone *thought* still needed reading. **[[read-the-queue-first]] must be widened: before sweeping any volume, grep `searched.json` for its ark.** One `grep an_ua14262 site/src/data/searched.json` would have cost a second and saved the pass.

## WHAT THE DUPLICATE PASS ACTUALLY ADDED

**It was avoidable. It was not sterile.**

### 1. It proved the layout, which the earlier record does not state

The 21 September row says «**read at the name band**» and **does not say which half**. This archive's standing hazard is that *a band reading one half of each image reads half the acts consistently, so nothing looks missing* → [[half-page-sweeps]].

**In these volumes an act BEGINS on the RIGHT page** — «*Atto di solenne promessa di matrimonio · Num. d'ordine N*» — and that page carries the date, the officer, **the groom with both his parents and the bride with both hers**. **The LEFT page of the next image holds the PREVIOUS act's four witnesses.** So the right half is the whole of the evidence, and `image = act + 2`.

**1858: images 3–38, THIRTY-SIX acts. 1859: images 3–27, TWENTY-FIVE acts** *(1859's last printed form, act 26 on image 28, was never filled in)*. **Sixty-one acts, no Falco as groom, as bride, or as a parent of either** — which independently confirms the earlier nil **and** establishes that the band it used cannot have been the wrong one, because the wrong one holds no names at all.

*Both volumes were identified from the manuscript — «**Degli atti di MATRIMONI … mille ottocento cinquantotto**» — not the catalogue, which gives only the year* → [[naming-a-volume]]. The 1858 volume carries an archivist's tab: **«WHOLE VOLUME — FADED INK»**.

### 2. A FOURTH CHIARA RIVETTI — and she bears on work-list row 87

**1858, act 23, 26 August** (`an_ua14262` img 25), read from the image at 3,200 px:

> «*comparsi nella Casa Comunale **SAVERIO GUIDA**, di anni **ventisei**, nato in **Arienzo**, di professione **contadino**, **figlio di LUIGI GUIDA DEFUNTO**, di professione **agrimensore**, domiciliato **ivi**, **e di CHIARA RIVETTI**, domiciliata **ivi**; e **CARMINA CIMMINO**, di anni **ventiquattro**, figlia di **[Michel]e Cimmino defunto**, **artiere**, e di **MARIA LAUDATO***»

**THE SURNAME WAS PROVED, NOT ASSUMED.** In this hand «Rivetti» opens with a stroke readable as a capital V. **The control is in the same volume**: act 6 writes **«Lucia Rivetti»** and **«Maria Rivetti»** in the same pen with the identical initial, and writes **«Arricale»** with a plainly different A → [[surname-ligature-test]], [[di-guida-parents]].

**SHE IS NOT THIS LINE'S CHIARA RIVETTI, AND THE PROOF NEEDS NO HANDWRITING AND NO «FU».** Pasquale Falco's widow died **13 September 1843** «*di anni OTTANTA*» — born about **1763**. **Saverio Guida was twenty-six in August 1858, so born about 1832.** *A woman born in 1763 does not bear a child in 1832.* → [[quondam-not-evidence]]

**WHY IT MATTERS.** Row 87 reasons that **three** Falco men each recorded with a wife «Chiara Rivetti» is not credible, so she is **one woman** and the clerks wrote the husband's forename three ways — and it leans on **exactly one Chiara Rivetti death in fifty years of registers**. **Here is a Chiara Rivetti alive at Arienzo in 1858, married to a man of another surname, who is ALSO absent from those fifty years.** *The absence of a second death does not show there was only one woman; it shows the death series does not reach them.* **The case for collapsing MICHELE into MICHELANGELO is weaker than that row states.** Nothing is merged or unmerged on it → [[chiara-rivetti-three-husbands]].

### 3. The word that defeated the 1854 act

**1859, act 18** gives a father's trade in a clearer hand: «*figlia di **[Raff]aele Crisci**, di professione **MINISCALCO***».

**That is the word** magnified seven times that morning on Raffaela Falco's death act (`an_ua14356`, 20 April 1854) and deliberately left unread. **MINISCALCO — a farrier.** The letter taken for a «p» is a **long italic ſ**: mini-**ſc**-a-l-c-o. **And this archive already held the term**: `data/people-register.tsv` carries «*Alfonso Ruggiero, **71, MINISCALCO**, strada Terra Murata*».

**So Raffaela Falco's two declarants — MATTEO and CLEMENTE, sixty-six and forty, of strada Porta di Sopra — were farriers.** *Their surname is still faint and still not claimed.*

**THE LESSON.** A word that will not separate at a scan's maximum resolution **may be legible in another document in another hand** — and the cheapest place to look is **this archive's own transcriptions**, not more pixels → [[harvesting-is-not-holding]].

### 4. By-catch: ARRICALE, and a candidate that must NOT be promoted

Row 9 wants **Giovanna Arricale's siblings**. Three Arricale appeared; **none is established as one**:

| act | person | parents |
|---|---|---|
| **1858 act 6** | **LUCIA ARRICALE**, 22 (b. c.1836), m. Clemente Cimmino | **Gaetano Arricale *defunto*** and **Maria Rivetti** |
| **1858 act 25** | — | **Pellegrina Arricale**, the bride's mother |
| **1859 act 10** | **ANTONIA ARRICALE**, 27 (b. c.1832), m. Angelo Magliato of San Felice | **FRANCESCO ARRICALE** *(living)* and **ANGELA PIGNATELLI** |

**ANTONIA IS A CANDIDATE, NOT A SISTER.** This archive's **GIOVANNA ARRICALE** was born **22 December 1848** to **Francesco Arricale and PASQUA FALCO**. Antonia's father is also a **Francesco Arricale** — but **her mother is ANGELA PIGNATELLI**, new here, and **sixteen years** separate the two daughters. *A Francesco Arricale with two wives explains it exactly; so do two men of one name, in a town where this archive has repeatedly proved a name identifies nobody.* **Nothing joins them and nothing is claimed.** *Antonia's own birth act, about 1832, would name her mother and settle it* → [[wrong-negatives]].

*All three Arricale, plus Angela Pignatelli, Luigi Guida and Saverio Guida, were run through `tools/isitnew.py` before being written here. All are new; «Antonia Arricale» matched only two parish machine-readings of 1792 and 1794, a different woman.*

---

**The surnames these two years actually run on:** Morgillo, Crisci, Lottieri, Martone, Diglio, Porcino, Carfora, Cimmino, Gimbardo, Majone, Abbatelli — with grooms from **San Felice**, **Santa Maria a Vico**, **Arpaia**, **Forchia** and **Cervinara**.
