# Arienzo civil BIRTH register 1819 — sweep COMPLETE

**Volume:** `an_ua14416` (Arienzo, Nati 1819), **74 images, 137 acts.**
**Year confirmed FROM THE MANUSCRIPT**, per the standing rule: the title page (image 1, right)
reads «*Dal primo Gennajo a tutto il dì trentuno Dicembre mille ottocento **diciannove***», and the
last acts (image 72) are dated 26 and 28 December 1819, «*Comune di **Corpo d'Arienzo***».
The printed form is not struck — this year the print and the manuscript agree.

## THERE IS NO ANNUAL TAVOLA

Both ends checked. Image 1 is the title page; images 73–74 are a blank form and the Procuratore
del Re's certificate about removing blank leaves.

**The last leaf's LEFT page carries a twenty-one row list** headed «*Nomi, e cognomi de' genitori |
Giorno della nascita | Osservazioni*», with dates scattered across the whole year. Surnames in it:
Rivetti, Arrigale, Laudato, Morgillo, Pesciutelli, Cossi, di Lucia, Cioffi, Martone, d'Ambrosio,
Lizzarulo, delle Cave, Lettieri, Sposito, Balletta, della Morte, Sapano, Morgillo. **No Falco.**

**It is NOT the year's index** — twenty-one rows against 137 acts. Treat it as a supplementary
list. **A short list at the back of a volume is not a tavola; count its rows against the act total
before trusting it.**

## Method: six contact sheets

`python3 tools/antenati.py sweep an_ua14416 --range A B --band 0.14 0.145 --half LR --cols 2 --width 2400`

Ranges 2–13, 14–25, 26–37, 38–49, 50–61, 62–72. The band catches «*è comparso [FATHER], di anni
[AGE], di professione [TRADE], domiciliato … strada [STREET]*». Twenty-four tiles a sheet.

**THE BAND DRIFTS.** Act blocks are not at a constant vertical offset; a tight three-line band
(0.075) loses the name on perhaps a third of tiles. **0.145 is the working height** — it wastes
space but never loses the line.

## THE THREE FALCO ACTS

| Act | Date | Child | Father | Mother | Street |
|---|---|---|---|---|---|
| **33**, f.206 | **18 Mar**, 7.30am | **DOMENICO CLEMENTE** | **Giuseppe Falco**, *massaro di campagna* | **Gelsomina Vigliotta** | Camellara |
| **99**, f.239 | **11 Oct**, 5am | **CRESCENZO** (see below) | **Giuseppe Falco**, 40, contadino | **Antonia di Guida**, 31 | Camellara |
| **133** | **21 Dec**, 10am | **LUIGI** | **Vincenzo Falco**, 26, contadino | **Andreana Crisci**, 22 | Camellara |

**Act 33 is a necronym.** This couple buried Domenico (2y 4m) and Rosaria on **15 March 1819**,
eleven hours apart — both already in the archive. **Three days later this boy was born and given
the dead brother's name.**

**Act 33 carries a MARGINAL MARRIAGE:** «*Con atto **6 agosto 1856** at[to] **21** in **S[anta]
Maria a Vico** il Falco sposò **DOMENICA VIGLIOTTI** di Giuseppe*». **A birth act can reach a
marriage in another comune.** New instrument — see the open item on Nunziata Falco.

**Act 99's given name DID NOT RESOLVE in the civil hand.** Antenati refuses `--width 4000` on this
leaf («*Requests for scales in excess of 100% are not allowed*» — **the cap is per-leaf, not 3400
everywhere**). The name was supplied instead by the PARISH page **already harvested here and never
parsed**: `3Q9M-CSD3-13CH-7`, October 1819, «*et Josepho Falco et Anto[nia] di [Guida] Conjugibus*»,
margin «*Cresantios*» = **CRESCENTIUS**. `data/falco-baptisms-parsed.tsv` has the row with the
child column **blank**. Two series, same parents, same month.

**Act 133 is NOT a new child.** The parish baptism «*nominatus est Aloysius*», dated «Dec 1819»,
was already in `households.json`. It was written up as a discovery and the same-pass check caught
it **before publication**. What is new: the day, the hour, the street, both parents' ages.

## NEGATIVES

- **ROSARIA FALCO is not in 1819.** She died 15 March 1819, daughter of Giuseppe Falco and Gelsomina
  Vigliotta, and is absent from 1816, 1817, 1818 **and now 1819**. Every year she could be in has
  been read. Her birth act does not exist in the Arienzo civil series.
- **No Maria Rosa Falco** (daughter of the Michele Falco of strada Camellara, b. c.1817–18, d. May
  1834 aged 16). 1817, 1818 and 1819 all read. Try 1820.

## TWO READINGS THE CONTACT SHEET GOT WRONG

Both were the reading I was hoping for; both fell at magnification.

1. **«Alfonso Diglio … strada Camellara»** (act 67) is **strada TERRA MURATA**. Not the husband of
   the fourth Maria Falco.
2. That man's wife, read as **«…Falco»**, is **SILVIO** — no F crossbar, l-v-i-o not l-c-o.

**A contact sheet may produce a candidate. It may never produce a record.**

## A CONTROL FOR THE COSSI / CIOFFI TRAP

Act 22, 19 February 1819: «*Francesco **COSSI**, 30, contadino … strada **COSSI***» — wife **Teresa
Morgillo**. **The same word twice in one sentence, as a name and as a street.** Where a street
carries the surname it checks the reading with no judgement at all. This man is thirty in 1819
(b. c.1789); the strada Camellara **Francesco CIOFFI** is twenty-seven in 1824 (b. c.1797).
**Different men, different ages, different streets.**
