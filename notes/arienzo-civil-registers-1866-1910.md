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


---

# THE LAYOUT, PROVED FROM THE MANUSCRIPT — `MC55-FNT`, 8 October 2026

**The volume is not one register. It is a year's worth of separate books bound onto one roll, five
books to the year, each with its own cover, its own printed title page and its own numbering.**
Surveyed from the thumbnails with `tools/fscontact.py`, then each title page read whole with
`tools/fsgrab.py page`.

| images | book, as its printed title page states it |
|---:|---|
| 1–2 | the filmer's target board, **exposed twice** |
| 3 | cover: «*1866 — Arienzo — Pubblicazioni di Matrimoni*», the clerk's hand |
| **4** | **«Anno 1866 · Comune di Arienzo · Provincia di TERRA DI LAVORO · REGISTRO delle pubblicazioni di Matrimonii»** |
| 5–43 | the acts |
| 44–45 | cover, then **«Anno 1866 … REGISTRO»** — the marriages |
| 46–59 | the acts |
| 60–61 | cover, then **«… REGISTRO delle Nascite»** |
| **62–123** | **THE BIRTHS OF 1866** |
| 124–128 | cover, two leaves of ruled index, then **«… REGISTRO delle Morti»** |
| 129–167 | the acts |
| 168–169 | cover, then **«… REGISTRO delle Dichiarazioni di Cittadinanza»**, with a fifty-centesimi revenue stamp |
| 170–171 | the acts, then the next cover |
| **172** | **«Anno 1867 · COMUNE di Arienzo · PROVINCIA DI TERRA DI LAVORO»** — the year turns |

**PUBBLICAZIONI · MATRIMONI · NASCITE · MORTI · CITTADINANZE, in that order, about 168 images to the
year.** *That is the shape the catalogue's title was describing all along — «Nati, matrimoni, morti
1866-1876 · Pubblicazioni 1866 · Cittadinanze 1866-69…» is a list of books, not a list of series.*

**«PROVINCIA DI TERRA DI LAVORO», not Caserta** — the province kept that name until 1927, and a
search of this archive's own prose for «Terra di Lavoro» is worth doing.

## AND AN ACT WAS READ, so this is no longer the catalogue's word

Image 66, sampled at random from the 1866 births and legible in a single request:

> «*…presentato un bambino di sesso maschile, che dichiara essergli nato il giorno **otto** del andante
> mese, a ore **dieci** d'Italia, dalla di lui moglie **GIUDITTA CRISCI**, figlia del fu **FRANCESCO**,
> sua legittima moglie, e nella casa di sua abitazione posta in questo Comune, **Contrada Maddalena**,
> al quale figlio dichiara di dare il nome di **FRANCESCO**. La quale dichiarazione viene fatta alla
> presenza di **Vincenzo Ruotolo**, figlio di Pietro, di anni cinquantadue, di condizione agricoltore,
> e di **Aniello Guida**, figlio di Pasquale, di anni cinquantatré, di condizione …, residenti in
> questo Comune, testimoni…*»

**A birth act of Arienzo, 1866, in the register this archive said did not survive.** *No kinship is
claimed from it — it was opened to prove the book, not to find a Falco, and a Crisci of Arienzo is
not a Crisci of this line until something says so. **This archive never merges people on a name.***

**What it does prove beyond the book**: the formulary of these years names **the mother in full with
her own filiation** («figlia del fu Francesco»), the **contrada**, and both witnesses with their
fathers and ages. *That is a richer act than the 1809–1865 Antenati forms this archive has been
working from.*


## AND EVERY YEAR HAS AN «INDICE ANNUALE» — which is the whole route

Image **125** is a printed, ruled, two-column **INDICE ANNUALE**: columns «*NOME E COGNOME*» and
«*NUMERO di REGISTRO*», about **sixty names a column, a hundred and twenty a leaf** — most of a
year's births on one page, in one request.

**It is ordered by FORENAME, not surname** — *Aniello Crisci 13 · Agnello Attorato 22 · Alfonso
Diglio 27 · Anna Migliore 30 · Carmine Crisci 72 · Carminantonio Morgillo 91 · Chiara Caracciolo 98
· Domenico Crisci 19 · Filippo Crisci 86 · Francesco Morgillo 21 · Giovanni Ruotolo 1 · Giuseppe de
Lucia 20* — so a surname cannot be looked up; **the leaf has to be read whole.** At one request a
leaf that is not a problem, and **it is still the whole year for two requests.**

**IMAGE 126 IS A DUPLICATE EXPOSURE OF 125**, name for name. *The Antenati volumes do this too and
`register-layout-proof.md` records it; the filmer of 1991 did it as well, and on this roll the target
board is exposed twice at images 1 and 2.* **A second exposure is not a second leaf, and counting it
as one would inflate every page count taken from a contact sheet.**

**NO FALCO STANDS ON THE 1866 BIRTH INDEX LEAF THAT WAS READ** — that is one leaf of a year, not the
year, and nothing is concluded from it.

### THE ARITHMETIC WAS TESTED AND IT IS WRONG

The 1866 births run images **62–123**, sixty-two images, and the highest register number on the index
leaf is **122**. *That is about two acts to an image*, which would make `image ≈ 61 + ⌈act ÷ 2⌉`. It
was published here as arithmetic rather than proof, and then **tested the same hour, the way
`register-layout-proof.md` tests a band: take a number to its predicted image and look.**

**The rule predicts acts 99 and 100 on image 111. Image 111 carries act N.º 113** — margin name
«*Carmina Anzivino*», «*l'anno milleottocento sessantasei, nel giorno **undici del mese di Ottobre***,
nella casa comunale, alle ore quattordici, dinanzi a me **Lorenzo Ruggiero**, assessore delegato del
Comune di **Arienzo**, circondario di Caserta, Provincia di Terra di Lavoro*». **Thirteen acts out
over fifty images, and it would only get worse further down the book.**

**THE RULE IS WITHDRAWN.** *An act is as long as the clerk made it, and the number of acts on an
opening is not a constant anybody may assume — which is the whole lesson of the band sweep that
published two volumes as «read in full» when half of each had been read.* **Go to the index for the
number, then walk to it. Do not interpolate.**

*The facing page of image 111 carries another 1866 birth: «…figlio di **Aniello**, di anni venti…,
agricoltore, domiciliato in questo Comune, **Contrada Capodicienà**… dalla di lui moglie **MARIA
ARRICALE**, figlia del fu **Francesco**… al quale figlio dichiara di dare il nome di **Francesco**».
**Arricale is one of the ten allied surnames work-list row 69 named**, and nothing is concluded from
that: the leaf was opened to test a rule, and this archive never merges people on a name.*


---

# THE SECOND VOLUME IS PROVED TOO, AND EVERY IMAGE CARRIES ITS FILM AND FRAME

**`MC55-VNL`, «Nati, matrimoni, morti, pubblicazioni 1878-1900», 2,898 images** — the volume holding
most of what this archive is looking for. Its image 4 is the same filmer's target board: «*LOCALITY
OF RECORD — **ARIENZO, CASERTA** · STATO CIVILE. PUBBLICAZIONI, MATRIMONI, NASCITE, CITTADINANZE E
MORTI · ANNI (1866 A 1910)*», Tribunale di S. Maria Capua V., **25 November 1991**, operator Carfora
Vincenzo, project ITLC 8105A — **roll 6**, where `MC55-FNT` is roll 5. *Two rolls of one filming.*
Its image 1 is the film's own number plate: **1797493**.

## AND THE BRIDGE NOBODY HAD

**Every `dist.jpg` carries «film NNNNNNN, frame NNNNN» in its JPEG comment segment.**

| waypoint | film in the comment | frame |
|---|---|---|
| `MC55-FNT` | **7059206** | **frame = image + 1780**, exactly, across six samples forty images apart |
| `MC55-VNL` | **7059207** | frame = image |
| the processetti leaves read this morning | **7066612** | — |

**Record Atlas measured this exact gap across 1,349 rows of eight family archives** and concluded
there was no way across it: *the family sessions cite FamilySearch by DGS film number and by image
ark; the atlas holds waypoints; **exactly one row in 1,349 carried a waypoint and the film numbers
matched the atlas zero times**; «there is no bridge on disk».*

**There is now, and it costs one request per volume.** Fetch any image's `dist.jpg`, read the
comment, and you have that volume's film number and the frame offset for every other image in it.
`tools/fsgrab.py page` prints it.

> **TWO IDENTIFIERS, NOT ONE.** The film in the comment is FamilySearch's **DGS** number. It is
> **not** the microfilm roll number printed on the film's own plate — **7059207 in the comment
> against 1797493 on the plate, on the same roll.** Both are real and they are not the same thing.
> *Conflating them would manufacture exactly the false match the atlas has been careful to avoid.*


---

# THE FIRST ACT OUT OF THE LOST YEARS THAT CONCERNS A FALCO — 1866 death n.º 51

**And it was found by the index, in four requests.** The «INDICE ANNUALE» at image 125 turns out to
index the **deaths**, not the births — *demonstrated, not assumed*: it gives act **113** to «**Andrea
Venafra**», and birth act 113 is «Carmina Anzivino» on image 111. **Different person, same number,
therefore a different book**, and the book whose title page follows it at image 128 is «REGISTRO
delle Morti».

**Its A-column, read at full resolution, holds «ANTONIA FALCO — 51».** *(Also «Antonio Rivetti 74»;
Rivetti is one of row 69's allied surnames.)* **The index is ordered by the initial of the FORENAME
and then by act number ascending** — not alphabetically within the letter — which is worth knowing
before reading forty more of them.

Act 51 was reached by walking: image 145 carries act 54, image 144 carries 50 and 51.

> «*L'anno milleottocentosessantasei, nel giorno **diciassette** del mese di **Giugno**, nella casa
> Comunale, alle ore quattordici. Dinanzi a me **LORENZO RUGGIERO**, segretario del Comune di
> **Arienzo**, Circondario di Caserta, **Provincia di Terra di Lavoro**, delegato a compiere le
> funzioni di Ufficiale dello Stato Civile per gli atti di nascita e di morte dal Sindaco di questo
> Comune con atto del giorno tre Febbrajo corrente anno, approvato dal Signor Procuratore del Re con
> nota del giorno sette detto mese di Febbrajo. Sono comparsi **RAFFAELE FALCO, figlio di VINCENZO,
> di anni quarantasette**, di condizione agricoltore, domiciliato in Arienzo, ed **ANGELO MAJONE,
> figlio del fu Francesco, di anni cinquantasette**, di condizione agricoltore, domiciliato in detto
> Comune di Arienzo, i quali mi hanno dichiarato che nelle **ore dodici d'Italia** del suddetto
> giorno, in questo Comune di Arienzo, **nella casa di MATTEO FALCO**, è morta la nominata **ANTONIA
> FALCO** di condizione*»

**AND IT STOPS THERE.** The ruled block ends at the foot of the page on the word «*condizione*».

## ~~NOTHING IS ATTACHED TO ANYTHING, AND HERE IS WHY~~ — THIS WAS WRONG, AND IS LEFT STANDING

> ~~**Her age, her parents and whether she was wife, widow or child are all on the continuation, and
> the continuation is not on the adjacent leaves.** *Checked by name, not assumed*: image 143's right
> page carries act **48**, Angela Orologio, entire; image 144's right page carries act **52**,
> Filomena Diglio, entire, from its own preamble; image 145's left page opens act **53** from its
> preamble. **Three neighbouring pages, three other complete acts.**~~
>
> ~~**THIS IS THE SECOND ACT IN TWO DIFFERENT VOLUMES TO DO EXACTLY THIS.** … **Two is a pattern and
> not an accident** … every act read here may be missing its most load-bearing line.~~
>
> ~~**«Nella casa di MATTEO FALCO» is a lead and nothing more.**~~

**THE CONTINUATION WAS AT THE TOP OF THE FACING PAGE OF THE SAME OPENING, and the reading above had
only ever looked at the bottom 56% of that page.** Published for about ten minutes; corrected at
`/corrections/`. *It is left here struck through because a correction that hides what it corrected
teaches nobody.*

> «*…**di anni TREDICI**, domiciliata in Arienzo, nata in [Arienzo], **figlia di MATTEO FALCO di
> condizione AGRICOLTORE e di ALESSANDRA CRISCI di condizione TESSITRICE**, domiciliati nella
> **CONTRADA CAMELLARA***»

## ANTONIA FALCO IS A CHILD OF THIS ARCHIVE'S OWN HOUSEHOLD

**Thirteen in June 1866, so born about 1853.** `Matteo Falco & Alessandra Crisci` — married **24
January 1834**, with Domenica born at **strada Camellara** in 1846 and the rest of the children in
the 1870s and 1880s. **She sits between them, and she is the first child of that house to carry a
death act at all.**

*She is placed there on the couple, not on a name.* **Both parents are named in full with their
trades and their street**, and Camellara is this household's own address. *This archive holds at
least three other women called Antonia Falco and would not have placed her on the forename —
`tools/isitnew.py` was run before she was attached, not after.*

**And the lesson is the one the strike-through is for: when an act breaks at a page foot, read the
WHOLE facing page before concluding anything, top first.** `tools/fsgrab.py page` returns the entire
opening in one request, so there was never a cost reason to work in crops. *The crops were for token
economy and they nearly cost a filiation — and did cost a published claim.*

**The 1887 Carfora act is NOT re-opened by this**: it really does end mid-sentence, and its
continuation really is absent from the images this archive holds. **But «two is a pattern» is
withdrawn. There is one.**

**RAFFAELE FALCO, figlio di Vincenzo, aged 47 in 1866 — so born about 1819** — declared the death and
is recorded for testing against what this archive holds. **He is not merged with anybody.**


---

# THE 1866 DEATH INDEX, READ IN FULL — AND THE «PROJA» ERROR, ON THIS ARCHIVE'S OWN SURNAME

**Both leaves of the 1866 «INDICE ANNUALE» of deaths are read** (images 125 and 127; 126 is a
duplicate exposure of 125). **126 acts. Exactly ONE Falco: ANTONIA FALCO, act 51.**

*That is a measured negative for a year this archive had no deaths for at all.* The allied families
are thick on it — **Crisci** (Maria Giuseppa 50, Pellegrino 102, Vincenzo 53, Vincenzo 99),
**Carfora** (Mari'Antonia 42, Maria 92), **Morgillo** (Maria 21, Raffaela 43, Vincenza 34, Vincenzo
75, Pasquale 17, Maria 93), **Guida** (Maria 84), **Lettieri**, **Diglio**, **Attorelli**,
**Majone**, **Venafra**, **Vigliotta**, **Porrino** — *and one Falco.*

## AND HERE IS THE ERROR THIS INDEX PRODUCED, WHICH IS WORTH MORE THAN THE INDEX

Reading the V-block at the scale of a whole-page view, **act 104 was read as «Vincenzo FALCO»** — and
it was announced as a second Falco death, with a chain of reasoning already attached to it: *act 51's
declarant is «**RAFFAELE FALCO, figlio di VINCENZO**», **not «fu Vincenzo»**, so his father was alive
on 17 June; act 104 falls in October; therefore the father died later the same year.* **A tidy,
checkable, completely false story.**

**The act settles it. N.º 104 is «il Signor Don VINCENZO SOSSO, di condizione studente, di anni
diciotto, dimorante in Arienzo, nato in NAPOLI, figlio del Signor Don FEDERICO SOSSO di professione
medico, e di Donna CAROLINA D'AMBROSIO di condizione gentildonna, domiciliati in Napoli»** — died in
the house of Don Pasquale d'Ambrosio. *Not a Falco, not an Arienzo family, not even an Arienzo
birth.* And at magnification the index line plainly reads **Sosso**: the double long-s that the eye
had turned into «-lco».

> **THIS IS THE «PROJA» ERROR EXACTLY, AND THIS ARCHIVE HAD ALREADY WRITTEN IT DOWN:** *the commonest
> surname in the corpus is the one a reader's eye supplies unprompted.* It was written for machine
> transcriptions and it applies just as hard to a human reading a reduced image. **Falco is the
> surname this archive is looking for, which is precisely why it is the one that will appear where it
> is not.**

**THE RULE THIS BUYS: AN INDEX LINE IS A FINDING AID, NEVER A READING.** It gives you a number to
walk to. **The surname is only established by the act** — and «Antonia Falco 51» is established
because act 51 was read, not because the index said so. *Every name taken off these forty-odd index
leaves must be confirmed at its act before it is written down anywhere.*

*Cost of the error: two requests, and it was caught the same minute by the act it predicted. Cost if
the index had been trusted: a Vincenzo Falco who never existed, with a death date, a son and a year —
in a household file.*


---

## 1867 — AND THE ORDER OF THE BOOKS IS NOT CONSTANT

Six title pages of 1867 read whole, one request each:

| image | what the printed title page says |
|---:|---|
| 224 | «Anno **1867** · COMUNE di **Arienzo** · PROVINCIA DI TERRA DI LAVORO · REGISTRO **di Matrimoni**» |
| 236 | «Anno **1867** … REGISTRO **di Morti**» |
| 241 | «Anno **1867** … REGISTRO **di Morti**» — *a second one, and this archive does not yet know why* |
| 277 | «Anno 186[7] … REGISTRO **di Matrimonj**» — with «*Il presente registro, formato di fogli dodici, numerati e vidimati in ufficio. **Il Giudice delegato, Franc. Balsamo***» |
| 281 | «Anno **1867** … REGISTRO **di Cittadinanza**» |
| 285 | «Anno 186[8?] … REGISTRO **d…**» — the year and the kind are both cut by the gutter |

**1866 ran Pubblicazioni · Matrimoni · Nascite · Morti · Cittadinanze. 1867 does not run in that
order**, and until each title page is read there is no telling where a given year's births or deaths
begin. **The book order within a year is not a constant and must not be assumed** — the same lesson
as the two-acts-an-image rule, one level up.

**Two 1867 title pages both say «di Morti» (236 and 241).** *A duplicate exposure, a vidimazione leaf
bound before the register proper, or two volumes of one year — not yet established, and recorded as
not established.*

**«PROVINCIA DI TERRA DI LAVORO» is PRINTED on the 1867 forms** where 1866's clerk wrote it by hand.
Every one of these also carries the Tribunale's own authorisation: «*Il Presidente del Tribunale
Civile di Santa Maria Capua Vetere, visto l'Articolo 357 Codice Civile, delega per la vidimazione del
presente registro…*» — **the court that holds this copy, naming itself on the page.**


---

## THE WHOLE VOLUME IS SURVEYED, AND THE THUMBNAIL BUDGET IS MEASURED TO THE END

**`MC55-FNT` surveyed entire: 1,236 thumbnails, 13 contact sheets, ZERO refusals**, one request a
second, single threaded. *The ~25-per-half-hour ceiling is a DeepZoom ceiling and nothing else* —
this run is **fifty times** that budget on the `dascloud` path with no block at any point.

    python3 tools/fscontact.py data/arienzo-fs-tribunale-images.tsv \
        --waypoint MC55-FNT --out <dir>/fnt --cols 12 --rows 8

**The sheets are not committed.** They are ~1,200 thumbnails of somebody else's scan, reproducible in
twenty-five minutes by the line above, and this repository holds the *index* (`data/arienzo-fs-
tribunale-images.tsv`) and the *readings*, not the images. **What a sheet is for is choosing the leaf
to spend a request on**, and the structure it shows — cover, blank, printed form, running hand,
two-column index, target board — is now written down for 1866 and 1867 above.

**`MC55-VNL` (2,898 images, 1878–1900) has NOT been surveyed.** It is the volume holding most of what
this archive wants, and it is the obvious next run.


---

# THE BIRTH INDEXES OF `MC55-FNT` DO NOT EXIST — and that is a measured negative, not a failure to look

**8 October 2026, work-list row 102.** The plan was to read the birth index of every year 1866–1877
and take out the Falco. **There are none to read**, and here is what was checked before saying so.

## How the volume was mapped, for nothing

**Every cover in the volume was found computationally** — a cover is a near-black thumbnail, and
`mean brightness < 45% of the volume median` finds all **48** of them without a single request. The
leaf after each cover was then fetched whole (46 requests, `tools/fsgrab.py page`) and read.

**THE BOOK MAP OF `MC55-FNT`**, from the printed title pages themselves:

| year | the books, by the image their title page sits on |
|---|---|
| **1866** | Pubblicazioni **4** · Matrimoni **45** · **NASCITE 61** (acts 62–123) · *deaths index 125–127* · Morti **128** (acts 129–167) · Cittadinanze **169** |
| **1867** | 172 · Matrimoni **224** · Morti **236** · Morti **241** *(a second one, unexplained)* · Matrimonj **277** · Cittadinanza **281** |
| **1868** | **NASCITA 297** · Morte **341** · Cittadinanza **383** |
| **1869** | Matrimoni **386** · Matrimoni **407** · **NASCITA 420** · Cittadinanza **463** · Morte **466** |
| **1870** | **NASCITE 492** · Matrimoni **537** · 566 |
| **1871** | Matrimoni **594** · **NASCITA 612** · 656 · *index forms 661–664* |
| 1872–74 | 693 · 716 · Cittadinanza **750** · 753 · 776 · 791 · 827 · 854 · 873 · 909 — **these title pages leave «REGISTRO d___» BLANK**; from 1873 the clerk named the book on the cover only |
| **1875** | Matrimonio **926** · **NASCITA 948** · Cittadinanza **1000** · Morte **1003** |
| **1876** | Matrimonio **1033** · **NASCITA 1057**, **1109** · Morte **1118** · Matrimonio **1145** |
| **1877** | Matrimonio **1156** · **NASCITA 1179** · **NASCITA PARTE II 1232** |

*«**PARTE I**» and «**PARTE II**» appear from 1875 — the printed national form keeps second-part acts
in their own register, and **a sweep of Parte I alone would miss them.***

## WHERE AN INDEX WOULD BE, AND WHAT IS THERE INSTEAD

Checked in **six** years, at both positions an annual index can occupy — bound at the front of a book
behind its cover, or bound at the back after the last act:

| year | front of the births book | back of the births book |
|---|---|---|
| 1866 | cover 60 → title 61, no room | **123 = the officer's closing certificate**, «*Verificato in questo giorno 29 del mese di Gennajo dell'anno 1867*». No index |
| 1870 | cover 491 → title 492 | **535 = last acts + closing certificate.** No index |
| 1871 | cover 611 → title 612 | — |
| 1875 | cover 947 → title 948 | **998 = last acts, then blank printed forms.** No index |
| 1876 | 1109 is the **title page**, not an index | — |
| 1877 | — | **1232 is «PARTE II», a register, not an index** |

**AND THE 1871 PROOF IS THE ONE THAT SETTLES IT.** Images **661–664** are four «**Modulo dell'Indice
annuale**» forms bound together. **Only the first is filled**, and its header reads, at magnification:

> «**Modulo dell'Indice annuale de' Morti nell'anno 1871**»

**Images 663 and 664 are the same printed form, BLANK** — ruled, headed, and never written in. *The
volume was bound with an index form for each series and the clerk completed the deaths one and left
the others empty.* **The births index of 1871 exists as a sheet of paper and holds no names.**

**So the only filled annual indexes in this volume are of DEATHS — 1866 (images 125–127, a
handwritten form by forename initial) and 1871 (images 661–662, the printed form by SURNAME).**

## WHAT THIS MEANS FOR THE WORK

**The births of 1866–1877 must be read as books, not looked up.** That is roughly **four hundred
leaves** across the volume — at one request a leaf it is an afternoon, not a research project, and
`tools/fscontact.py` has already narrowed every birth book to its exact image range above.

*The index was never the point; it was the shortcut. The shortcut is not there for births, and
saying so is worth more than another week of looking for it.*


---

# THE ONE INDEX THAT EXISTS PAYS: TWO FALCO DEATHS OF 1871, READ AND CORROBORATED

The 1871 deaths index (images 661–662) lists **four Falco**: **Raffaele 68 · Fabrizio 69 · Maria 99 ·
Giuseppe 125**. *Index lines are finding aids, so each was taken to its act.* **Acts 68 and 69 sit on
one leaf, image 680**, and their margins read «*Atto di morte di **Raffaele Falco***» and «*Atto di
morte di **Fabrizio Falco***» — **the index is corroborated by the register itself.**

### 1871 n.º 68 — RAFFAELE FALCO, aged one

> «*L'anno milleottocentosettantuno, nel giorno **nove** del mese di **Agosto**, nella casa Comunale,
> alle ore dieci d'Italia. Dinanzi a me **NICOLA TINELLI, SINDACO** di questo Comune di Arienzo,
> Circondario di Caserta, Provincia di Terra di Lavoro, Ufficiale dello Stato Civile; sono comparsi
> **PASQUALE CARFORA di Aniello, di anni quarantotto**, ed **ANTONIO DIGLIO fu Bartolomeo, di anni
> cinquanta** … che alle **ore ventuno dell'otto** del corrente mese di Agosto, in questo Comune,
> **nella casa di PASQUALE FALCO, sita nella CONTRADA CAMELLARA**, è morto **RAFFAELE FALCO,
> contadino, di anno UNO**, nato e domiciliato in Arienzo, **figlio di PASQUALE e di MARIA MARIA
> GUIDA, contadini**, domiciliati in Arienzo.*»

### 1871 n.º 69 — FABRIZIO FALCO, seven months old

> «*…sono comparsi **MARCANTONIO CRISCI fu Giuseppe, calzolaio, di anni cinquantasette**, e
> **FRANCESCO FERRIELLO fu Pietro Ferraro, di anni cinquantadue** … che alle **ore dieci d'Italia di
> oggi** [9 August 1871], in questo Comune, **nella casa di ANTONIO FALCO, sita nella CONTRADA
> CAMELLARA**, è morto **FABRIZIO FALCO, contadino, DI MESI SETTE**, nato e domiciliato in questo
> Comune di Arienzo, **figlio di ANTONIO e di CARMELA GUIDA, contadini**, domiciliati in Arienzo.*»

## AND BOTH LAND ON PEOPLE THIS ARCHIVE ALREADY HOLDS — with the arithmetic agreeing

`tools/isitnew.py` was run **before** anything was written down, and it hit both times:

- **Raffaele Falco, b. 15 August 1870**, «*His father **Pasquale Antonio Falco**, his mother **Maria
  Amelia / Amalia Guida***» — *held from the family tree, which is «unverified unless a record is
  cited».* **The act is the record**: father Pasquale, mother Maria … Guida, Contrada Camellara, and
  «di anno uno» for a child three weeks short of his first birthday.
- **Fabrizio Falco, b. 22 December 1870**, «*His father **Antonio Falco**, his mother **(Maria)
  Carmela di Guida***» — again tree-only, **and with NO DEATH DATE AT ALL.** The act gives it: **9
  August 1871**, and «**di mesi sette**» against a birth of 22 December 1870 is **seven and a half
  months.** *The age and the birth were written by different hands a year apart and they agree.*

**TWO INFANT DEATHS ON CONSECUTIVE DAYS IN THE SAME CONTRADA, FROM TWO DIFFERENT FALCO HOUSEHOLDS,
AND BOTH FATHERS MARRIED A GUIDA.** *Contrada Camellara is the street this archive keeps returning
to — Matteo Falco and Alessandra Crisci are there, and so is the Antonia Falco of 1866.*

> ~~**NOT YET ATTACHED, AND DELIBERATELY.** Placing these two would mean **creating two households
> that this archive has never held as households**…~~
>
> **ATTACHED 9 OCTOBER 2026, AND THE REASON FOR PARKING THEM WAS HALF WRONG.** `Pasquale Falco &
> Maria Amalia Guida` **already existed** — Raffaele's act was one row in an existing file, not a
> structural decision. Only Antonio Falco × Carmela Guida had to be created.
>
> **While they sat here, both men's pages went on saying «No register act has been read for this
> person yet.»** *A reading parked in a note reaches nothing, and no gate can see it:* `check:evidence`
> examines only people named in households.json. **Corrected at `/corrections/`.**
>
> **Raffaele is still two pages, and correctly so.** The merge rule wants the dates to agree and they
> differ by a day — **the act says he died «alle ore ventuno dell'OTTO di Agosto», the tree says the
> 9th, which is the day the act was registered.** *The archive refused the join; that is the
> safeguard working, and the tree's date is the one to doubt.*

**ACTS 99 (Falco Maria) AND 125 (Falco Giuseppe) OF 1871 ARE NOT YET READ.** They are the obvious
next two requests.


---

# ACTS 99 AND 125 — AND 125 IS GIUSEPPE FALCO, WHICH ANSWERS WORK-LIST ROW 3

## 1871 n.º 125 — GIUSEPPE FALCO, ninety-five, «VEDOVO DI ANTONIA GUIDA»

> «*…alle **ore ventidue del NOVE** del corrente mese di **Dicembre** [1871], in questo Comune,
> **nella sua casa di abitazione sita nella CONTRADA CAMELLARA**, è morto **GIUSEPPE FALCO,
> agricoltore, di anni NOVANTACINQUE, VEDOVO DI ANTONIA GUIDA**, nato e domiciliato in Arienzo,
> **figlio de' fu MATTEO e FRANCESCA CRISCI**.*» — declared by **RAFFAELE FALCO di VINCENZO, 53**,
> and **PASQUALE GUIDA fu Fabrizio, 30**, before **Nicola Tinelli, Sindaco**.

**Work-list row 3 is «Giuseppe Falco's death, 1859 onward». This is it**, and it was found by the one
annual index this volume contains, in a register this archive had published as lost.

**FOUR POINTS MAKE THE IDENTIFICATION AND NOT ONE IS THE FORENAME** — *this archive has documented
three men of this name in three consecutive years, one of them on this very street:*

1. «**figlio de' fu MATTEO e FRANCESCA CRISCI**» — **the founders.** He is already held here as
   «**GIUSEPPE FALCO DEL FU MATTEO**» from the acts of 12 January 1810 and 16 February 1811. *This is
   the first record to name both his parents together*, and it ties `giuseppe-falco-antonia-di-guida`
   to `matteo-falco-francesca-crisci` from a document instead of an inference.
2. «**vedovo di ANTONIA GUIDA**» — and this archive had already bracketed her death to **15 November
   1857 – 14 February 1860**. *A widower in 1871 is what that window predicts.*
3. «**CONTRADA CAMELLARA**» — his street in every act from 1810 to 1857.
4. The declarant **RAFFAELE FALCO di VINCENZO, 53**, is the same man who at **forty-seven** declared
   **Antonia Falco's death in 1866**. *Five years, six years of age: the ordinary slippage.*

**THE AGE IS THE WEAKEST PART.** Ninety-five implies birth about **1776**, and his own stated ages in
this archive already run **1772 to 1785**. **The act agrees with the older end of a range this
archive has already published as unreliable, and settles nothing about it.**

**ATTACHED** to `Giuseppe Falco & Antonia di Guida` as his death.

## 1871 n.º 99 — MARIA FALCO, 53, «figlia di GIUSEPPE e della fu ANTONIA GUIDA» — NOT attached

> «*…alle **ore cinque d'Italia del DUE** del corrente mese di **Ottobre**, in questo Comune, nella
> sua casa di abitazione sita nel **VILLAGGIO COSTA**, è morta **MARIA FALCO, contadina, di anni
> CINQUANTATRE, MOGLIE DI RAFFAELE MORGILLO**, nata e domiciliata in questo Comune di Arienzo,
> **figlia di GIUSEPPE e della fu ANTONIA GUIDA**.*» — declared by **Antonio Crisci di Gabriele, 50**
> and **Salvatore Zimbardo fu Clemente, 27**.

**«figlia di GIUSEPPE» — with NO «fu», while her mother has one.** *The clerk marks the dead
explicitly on this form, so her father was alive on 3 October 1871 — and act 125 buries him on 9
December.* **The two acts, ten weeks apart, agree.**

**AND SHE IS STILL NOT ATTACHED, BECAUSE THE ARITHMETIC FIGHTS.** Fifty-three in October 1871 puts
her birth about **1818** — and this household's **Maddalena Falco was born 7 June 1818**. *Two
children of one couple cannot share that year.* So either the age is wrong, or «Maria Falco» is a
daughter born in another year, or this is **a second Giuseppe Falco × Antonia Guida**, which is
exactly the possibility this archive has already written down. **A documented wife — Raffaele
Morgillo — and a street, Villaggio Costa, are what would settle it, and neither has been looked for
yet.**


---

# `MC55-VNL` TOO: NO BIRTH INDEX, AND THE BIRTHS BOOKS END IN «PARTE II»

**The survey of `MC55-VNL` (2,898 images) is running; its first 651 were enough to settle the index
question for a second volume and a second decade.** Covers found the same way — near-black thumbnails
— and the leaf after each read whole.

| image | book |
|---:|---|
| 11 | **ANNO 1877 · ATTI DI MORTE · PARTE I** — *the volume opens where `MC55-FNT` stopped* |
| 47 · **64** · 115 · 118 | 1878: Matrimonio · **NASCITA** · Cittadinanza · Morte |
| 159 · **179** · 243 | 1879: Matrimonio · **NASCITA** · Morte |
| 282 · **304** · 350 | 1880: Matrimonio · **NASCITA** · Cittadinanza |

**AND EVERY BIRTHS BOOK ENDS THE SAME WAY.** The 1878 births run to image 110, and **111 is
«PARTE II · ANNO 1878 · REGISTRO DEGLI ATTI DI NASCITA»** — a second register, not an index — with
its acts on 112 and its closing on 113. The 1880 births do exactly the same at **347–348**.

## THE NEGATIVE, STATED ONCE AND PROPERLY

**Seven year-books checked across two volumes and three decades — 1866, 1870, 1875, 1876, 1877 in
`MC55-FNT`, 1878 and 1880 in `MC55-VNL` — and NOT ONE BIRTHS BOOK CARRIES AN ANNUAL INDEX.** They end
in the officer's closing certificate or in a **Parte II** register.

**The 1871 forms are the proof of intent**: `MC55-FNT` images 661–664 are four «*Modulo dell'Indice
annuale*» sheets bound in together, **only the deaths one filled**, the others ruled, headed and
blank. *Arienzo's clerks indexed their deaths and did not index their births.*

> **SO «READ THE BIRTH INDEXES» HAS NO OBJECT, AND THAT IS THE ANSWER RATHER THAN A FAILURE.** The
> births must be read as books. **What the survey gives instead is every birth book's exact image
> range**, which is the next best thing and did not exist this morning.

**AND «PARTE II» IS THE TRAP WORTH CARRYING AWAY.** From 1875 each year's births are in **two**
registers — Parte I for ordinary declarations, Parte II for acts received from elsewhere, late
registrations and transcriptions. *A sweep of Parte I alone reads a year and misses a category of
birth entirely*, and Parte II is where a child born away from Arienzo would be. **It is short — two
or three leaves a year — and it must never be skipped.**


---

# `MC55-VNL` IS SURVEYED ENTIRE — 2,898 thumbnails, 31 sheets, zero refusals

Both volumes of Arienzo's register run are now surveyed: **4,134 thumbnails across `MC55-FNT` and
`MC55-VNL`, 44 contact sheets, not one refusal**, one request a second throughout. *The thumbnail
endpoint has now been pushed to a hundred and sixty times the DeepZoom budget without a block.*

---

# AND THE NINE CHILDREN ARE NOT IN THESE VOLUMES AT ALL

**Work-list row 69's nine children of Matteo Falco and Alessandra Crisci were born 1837–1851** — the
couple married **24 January 1834** — and the tree gives: **Carmela 1837 · Filomena 1839 · Angela Rosa
1841 · Giuseppe 1841 · Vincenza 1842 · Maria 1843 · Domenica 13 Sep 1846 · Antonia 15 Dec 1851.**

**Every one of them predates 1866, so none of them is in `MC55-FNT` or `MC55-VNL`.** *The volumes
found today open exactly where these children stop.* **Their births are Antenati's**, in the
Napoleonic and Restoration series that runs 1809–1865 — and this archive has swept only **1837, 1845,
1846, 1847, 1848** of the years that matter. **1839, 1841, 1842, 1843 and 1851 had never been
opened.**

*Antenati's nominative index does not help: `/search-nominative/?cognome=Falco&localita=Arienzo` for
these years returns «**Nessun risultato trovato**» — that series is not indexed by name.* **It must be
swept.**


---

# THE BIRTHS BOOKS, READ — three of the nine children now have their birth acts

**The nine children of Matteo Falco and Alessandra Crisci were born 1837–1851, so their births are
ANTENATI's, not FamilySearch's.** Five of those years had never been opened: **1839, 1841, 1842,
1843, 1851**. The method: `tools/antenati.py sweep` over the whole volume at **two bands**, because
`register-layout-proof.md` proves that from 1820 a single act spans an opening — **the right page
carries the declarant, the left page of the NEXT image carries the mother.**

| child | act | born | father's stated age | mother's stated age |
|---|---|---|---|---|
| **FILOMENA FALCO** | **1839 n.º 74** | **20 June 1839**, 9 a.m., strada Camellara | Matteo Falco, **30** | Alessandra Crisci, **28** |
| **VINCENZA FALCO** | **1842 n.º 46** | **18 May 1842**, 2 a.m., strada Camellara | Matteo Falco, **28** | Alessandra Crisci, **32** |
| **ANTONIA FALCO** | **1851 n.º 135** | **15 December 1851**, strada Camellara | Matteo Falco, **40**, *colono* | Alessandra Crisci, **36** |

*Each child's own name comes from the **Indicazione** column — the parish of Sant'Andrea's return of
the baptism, written on the same leaf — because the body of the act never names the child.*

## 1841 IS A COMPLETE DOUBLE-BANDED NIL, AND IT BREAKS THE TREE

**The whole of 1841 was read at BOTH bands — every declarant and every mother, images 2 to 117 — and
there is no Falco declarant and no Alessandra Crisci anywhere in it.** The family tree puts **two**
children in 1841: Angela Rosa and Giuseppe. *They are not there.*

**So the tree's years are not reliable** — which also means **the five years chosen from the tree are
not the right five.** The honest frame is the one the acts give: the couple married **24 January
1834**, and three children are now dated **1839, 1842, 1851**. **The complete answer needs 1835–1852
swept, not the tree's guesses.**

## AND MATTEO FALCO'S AGE IS NOW DEMONSTRABLY UNUSABLE

**Thirty in 1839, twenty-eight in 1842, forty in 1851** — he grows *younger* by two years across
three, then by twelve across nine. Alessandra Crisci runs 28 · 32 · 36, four years per three.
*Neither can date a birth.* **The 1851 act is the only one that gives his trade as «colono»; the other
two say «contadino».**

## A METHOD TRAP, CORRECTED HERE

The big numeral on each left page is the **FOGLIO**, not the act number — it advances by **two** per
opening, so a contact sheet of left pages appears to show twice as many acts as the year has. *The
act number is printed inside the act as «N. d'ordine».* **Vincenza's tail carries folio 92 and her act
is number 46.** A sweep that read folios as act numbers would double every count it reported.


## 1843 IS A NIL TOO — and now two of the tree's three guesses are dead

**The whole of 1843 was read at the MOTHER band — images 2 to 122, every «*è nata da … sua moglie
legittima*» in the year — and ALESSANDRA CRISCI is not in it.** The tree puts **Maria Falco** there.
*She is not.*

**Why the mother band alone is enough for this job, and it halves the work:** the target is a known
**couple**. «Falco» is the commonest surname in the corpus and catches every household in the town;
«**Alessandra Crisci**» catches one. And because the midwife declares perhaps a third of these acts —
*Felicia Martone and Caterina Ruggiero, over and over* — **the declarant band misses exactly those,
while the mother band never does.** The declarant band was run in full for 1839 and 1841 as a
control, and it found nothing the mother band would have missed.

**By-catch recorded and not pursued**, each a Falco mother in a household this archive already holds:
**Giovanna Falco** (1843 img 13), **Francesca Falco, 30** (1843 img 32), **Raffaela Falco, 29** (1843
img 115).

## THE FIVE YEARS, FINISHED

| year | result |
|---|---|
| **1839** | **FILOMENA FALCO, act 74, 20 June** — found |
| **1841** | **COMPLETE NIL, BOTH BANDS**, images 2–117. *The tree puts Angela Rosa AND Giuseppe here.* |
| **1842** | **VINCENZA FALCO, act 46, 18 May** — found |
| **1843** | **COMPLETE NIL**, images 2–122. *The tree puts Maria here.* |
| **1851** | **ANTONIA FALCO, act 135, 15 December** — found |

**Three of the nine children now carry a birth act. Two of the tree's year-guesses are disproved
outright**, and a third — Carmela, said to be 1837 — sits in a year this archive swept in September
for a different woman and found only one Falco birth, which was not hers.

> **SO THE TREE'S YEARS CANNOT CHOOSE THE VOLUMES.** What is solid is the frame the acts give: the
> couple married **24 January 1834**, and their documented children fall **1839 · 1842 · 1846 · 1851**
> — *roughly one every three years.* **The gaps that must still be read are 1835–1838, 1840, 1844,
> 1845, 1847–1850 and 1852**, which is about twelve volumes and a known job, not a guess.


---

# MARIA FALCO IS 1844, NOT 1843 — and 1840 is a third nil

**Arienzo birth act 37 of 1844**, found at the mother band and read from the image:

> «*…**è comparso MATTEO FALCO, di anni TRENTATRE, di professione COLONO, domiciliato in STRADA
> CAMELLARA**, quale ci ha presentato una **FEMINA***» · tail: «*…**è nata da ALESSANDRA CRISCI sua
> moglie legittima, di anni TRENTATRE** … **nel giorno QUINDICI del mese di AGOSTO anno corrente, alle
> ore DUE, nella casa sua propria d'abitazione***» · *Indicazione*: «*il Sacramento del Battesimo è
> stato amministrato a **MARIA FALCO***».

**Born 15 August 1844.** *The family tree says 1843 — and 1843 was read in full at the mother band,
images 2 to 122, and Alessandra Crisci is not in it.* **Four of the nine children now have a birth
act.**

**1840 IS A NIL**, images 2–128 at the mother band. *The tree's Giuseppe is «about 1841» from his own
1887 act; 1840 and 1841 are both now empty, so he was born somewhere else or in another year.*

## THE TAVOLE ARE TRUNCATED BY THE FILMER, AND A CARD SAYS SO

**1840 ends with a «Tavola annuale alfabetica di nati»** — and it is the best instrument in these
volumes when it is whole: **«Numero d'Ordine · Cognomi e Nomi di Nati · Cognomi e Nomi di GENITORI ·
Giorno della Nascita»**, alphabetical by the child's surname, *with both parents on the same line.*
One leaf would answer a year that costs six contact sheets to sweep.

**It stops at C**, exactly as this archive already recorded of 1832 and 1837 — *«Crisci Angelo
Serafino» is the last entry.* **And lying across the page is the filmer's own card:**

> «**THIS INDEX HAS BEEN MICROFILMED ALREADY**»

**So the tavole are not truncated in the BOOK; they are truncated in the FILMING.** *The operator
stopped because the rest had been shot elsewhere* — which is what Arienzo's separate «**Morti,
indice**» volumes (`an_ua14305` ff.) are, and it means **a «Nati, indice» series may exist on
Antenati and has never been looked for.** *That would replace the whole sweep.*

**NOT ESTABLISHED, AND NOT RECORDED AS ABSENT:** `tools/antenati_holdings.py Arienzo` returned
**403 — rate limited** on all six series. **A 403 is a refusal, not an answer**, and this archive does
not publish negatives from one.


---

# 1845, 1849, 1850 AND 1852 — all four are nil, and two of them by a better instrument

**No child of Matteo Falco and Alessandra Crisci was born at Arienzo in any of these years.**

| year | how it was established |
|---|---|
| **1845** | mother band, **images 2–109**. *Images 110–139 were already read in September* — they hold **Maria Felice Falco, act 111**, to **Crescenzo Falco × Maria Morgillo**, not this couple. |
| **1849** | mother band, **images 2–129**, every «*è nata da … sua moglie legittima*» in the year |
| **1850** | **the year's own TAVOLA**, complete |
| **1852** | **the year's own TAVOLA**, complete |

## THE TAVOLE OF 1850 AND 1852 ARE COMPLETE — and that corrects a published generalisation

This archive has recorded that Arienzo's birth *tavole* «**are sporadic, and they fail in three
different ways**»: 1831 has none, 1836 has one never filled in, 1832 and 1837 stop at **C**. **1840
was added to that list this week** — it stops at «*Crisci Angelo Serafino*», with the filmer's card
«THIS INDEX HAS BEEN MICROFILMED ALREADY» lying across it.

**1850 and 1852 are not like that.** Both open with «*Tavola alfabetica annuale de' Nati*» running
the alphabet — C through L on one leaf, M through P on the next, and on — with the columns that
matter:

> «**Numero d'Ordine · Cognomi e Nomi de' Nati · Cognomi e Nomi de' GENITORI · Giorno della
> Nascita**»

**Both parents, on the child's line.** *One leaf answers a year that costs six contact sheets and a
hundred and thirty image fetches to sweep.* **The generalisation «Arienzo's birth tavole fail» is
true of 1831–1840 and FALSE of 1850–1852; the practice changed.** *It is the difference between a
year costing five requests and a year costing a hundred and thirty.*

**AND 1849'S TAVOLA IS BOUND IN AND BLANK** (image 128), so the change is not a clean switch — **it
must be checked year by year, and the check is one image.**

## EIGHT FALCO BIRTHS, NONE OF THEM OURS — recorded as leads

From the two tavole, with their parents exactly as the index gives them:

| year | child | parents |
|---|---|---|
| 1850 | Falco Vincenzo (14) · Falco Giovanni (77) · Falco Carminantonio (59) · Falco Antonio (90) | **Angelo × Cimmino Maria** · **Crescenzo × Morgillo Maria** · **Raffaele × Morgillo Maria Rosa** · **Michele × d'Ambrosio Giovanna** |
| 1852 | Falco Carmine (7) · Falco Antonia (26) · Falco Giovambattista (78) · Falco Maria Carmina (102) | **Luigi × Cimmino Carolina** · **Crescenzo × Morgillo Maria** · **Angelo × Cimmino Maria** · **Michele × d'Ambrosio Maria Giovanna** |

*«Falco Carminantonio, 59, of Raffaele Falco e Morgillo Maria Rosa» is a birth this archive already
holds from the act — **Carmine Antonio Falco, 10 July 1850** — which is a check on the tavola, and it
passes.* **Nothing else here is merged: these are five other Falco households of Arienzo, named and
left where they are.**

## THE BAND IS VOLUME-DEPENDENT, AND 1845 NEARLY PRODUCED A NIL THAT COULD NOT BE SUPPORTED

The mother band calibrated on 1839–1844 — **top 0.045, height 0.145** — sits at the very top edge of
the 1845 leaves, whose text block is set lower. **About a third of that year's first sheets showed
the page above the line rather than the line**, and the names simply were not there to read.

**A nil was not published from them.** The band was widened to **0.04 / 0.22**, all four years were
re-swept, and every tile is legible. *The already-published nils of 1840, 1841 and 1843 rest on
sheets where a mother's name was transcribed from every tile; they are unaffected.*

> **THE RULE: a band proved on one volume is not proved on the next.** It is the same lesson as the
> act-per-image arithmetic and the 1820 form change — *this register series drifts, and every
> instrument calibrated against it has to be re-checked when the volume changes.*


---

# 1835–1838 READ — and CARMELA FALCO is found, on the third day of 1838

**Arienzo birth act 2 of 1838**, the second act of the year:

> «*…**è comparso MATTEO FALCO, di anni VENTOTTO, di professione CONTADINO, domiciliato in STRADA
> CAMELLARA**, quale ci ha presentato una **FEMINA***» · tail: «*…**è nata da ALESSANDRA CRI[SC]I sua
> moglie legittima, di anni VENTIQUATTRO** … **nel giorno TRE del mese di GENNAJO, anno corrente, alle
> ore SEDICI, nella casa sua propria d'abitazione**. Lo stesso ha inoltre dichiarato di dare alla
> nominata il nome di **CARMELA**.*» · *Indicazione*, **Sant'Andrea Apostolo**: «*il Sacramento del
> Battesimo è stato amministrato a **CARMELA FALCO***».

**Born 3 January 1838. The family tree says 1837 — the fourth of its years for this household to be
wrong.**

> **THE MOTHER'S SURNAME IS NOT CRISPLY LEGIBLE AND THE PLACEMENT DOES NOT REST ON IT.** At full
> magnification the word is «Cri» plus a long-s and a terminal that could be *-sci* or *-spi*; both
> surnames are common in this register, and **the control-letter test could not be run — no instance
> of the same scribe writing both was found on these leaves.** *What is legible is the declarant
> **MATTEO FALCO**, the street **STRADA CAMELLARA**, a wife **ALESSANDRA**, and a daughter
> **CARMELA** — the name the tree gives this couple's eldest.*

## THE FOUR YEARS

| year | images read | result |
|---|---|---|
| **1835** | 2–118 | **nil** |
| **1836** | 2–128 | **nil** |
| **1837** | 2–145 | **nil** — *and the sweep CAUGHT the known Falco birth of that year*, «**Raffaela Falco**, ventisei» at image 111, act 108 of Francescantonio Falco. **The instrument is validated against a record this archive already held.** |
| **1838** | 2–120 | **CARMELA FALCO, act 2, 3 January** — and no other |

## SIX OF THE NINE, AND THE SPAN IS NOW CLOSED

| child | act | born |
|---|---|---|
| **Carmela** | 1838 n.º 2 | **3 January 1838** |
| **Filomena** | 1839 n.º 74 | **20 June 1839** |
| **Vincenza** | 1842 n.º 46 | **18 May 1842** |
| **Maria** | 1844 n.º 37 | **15 August 1844** |
| Domenica | 1846 | 13 September 1846 *(already held)* |
| **Antonia** | 1851 n.º 135 | **15 December 1851** |

**Swept and empty: 1835, 1836, 1837, 1840, 1841, 1843, 1845, 1847, 1848, 1849, 1850, 1852.** *With
the six years that produced a child, **every year from 1835 to 1852 is now accounted for.***

## SO WHERE ARE ANGELA ROSA AND GIUSEPPE?

**Not in the Arienzo birth registers of 1835–1852.** The tree puts both in **1841**, which is a
complete double-banded nil; Giuseppe's own 1887 act puts him «about 1841», and this household's
stated ages have already been shown to scatter by four years in each direction.

**Three possibilities, and the archive holds no evidence for any of them yet:**

1. **1834** — *the couple married **24 January 1834** and that volume has never been opened.* A child
   born in the last months of 1834 is entirely possible and is **the one remaining year inside the
   marriage**.
2. **Born outside Arienzo**, in a comune whose registers this archive has not touched.
3. **Never registered civilly** — which for this period would mean a parish baptism and no act.

*The ninth child the tree counts is not named in it, so there is nothing to look for.*


---

# 1834 — ANGELA ROSA FALCO, and the marriage-to-1852 span is now read end to end

**The couple married 24 January 1834. Their first child was born that December.**

**Arienzo birth act 116 of 1834**, images 118–119:

> «*ATTO DI NASCITA — **Num. d'ordine CENTOSEDICI**. L'anno mille ottocento **trentaquattro**, il dì
> **CINQUE** del mese di **DECEMBRE**, ad ore sedici, avanti di noi **FRANCESCO D'AMBROSIO, Sindaco**
> … del Comune di **CORPO D'ARIENZO** … **è comparsa CATERINA RUGGIERO, di anni SESSANTASEI, di
> professione LEVATRICE, domiciliata in strada PORTA DI SOPRA**, quale ci ha presentato una
> **FEMINA***» · tail: «*…**è nata da ALESSANDRA CRISCI, di anni VENTICINQUE, domiciliata in STRADA
> CAMELLARA, e da MATTEO FALCO marito della stessa, di anni VENTICINQUE, di professione COLONO** …
> **nel giorno CINQUE del mese di DECEMBRE, anno corrente, alle ore QUINDICI, nella casa propria di
> detti conjugi** … il nome di **ANGELA ROSA***» · *Indicazione*, Sant'Andrea Apostolo: «*…
> amministrato ad **ANGELA ROSA FALCO***».

**THE TREE PUTS HER IN 1841 — a year read end to end at both bands and empty.** She is **5 December
1834**, ten months and twelve days after her parents' wedding, and **she is the eldest of the nine,
not Carmela.**

## THE MIDWIFE DECLARED HER, WHICH IS WHY SHE WAS NEVER FOUND

**CATERINA RUGGIERO, sixty-six, *levatrice*** stood in for the father. **The act's declarant line
carries no Falco at all** — *a sweep of declarants reads straight past this child.* **It was the
MOTHER band that found her**, and this household is now the plainest argument in the archive for
reading both halves of the opening.

## AND IT SETTLES THE SURNAME THE 1838 ACT LEFT OPEN

**«Alessandra CRISCI» is written plainly here**, in a hand that leaves no doubt — where Carmela's
1838 act left the terminal ambiguous between *-sci* and *-spi*. *Same family, same register series,
four years apart.* **The 1838 reading is corroborated, and the note there still says what it could
not read.**

**Both parents are twenty-five in December 1834, so both born about 1809.** *That agrees exactly with
Matteo's «thirty» in June 1839 — and it puts **Alessandra eight years earlier than the family tree's
«b. 1817»**, which has no record behind it.*

## SEVEN OF THE NINE, AND THE SPAN IS CLOSED

| child | act | born | the tree said |
|---|---|---|---|
| **Angela Rosa** | **1834 n.º 116** | **5 December 1834** | *1841* |
| **Carmela** | 1838 n.º 2 | 3 January 1838 | *1837* |
| **Filomena** | 1839 n.º 74 | 20 June 1839 | 1839 |
| **Vincenza** | 1842 n.º 46 | 18 May 1842 | 1842 |
| **Maria** | 1844 n.º 37 | 15 August 1844 | *1843* |
| Domenica | 1846 | 13 September 1846 | 1846 |
| **Antonia** | 1851 n.º 135 | 15 December 1851 | *1851* |

**Four of the tree's seven datable years were wrong**, and every one was wrong in the same direction
— *later than the act.*

**EVERY YEAR FROM 1834 TO 1852 HAS NOW BEEN READ.** Swept and empty for this couple: **1835, 1836,
1837, 1840, 1841, 1843, 1845, 1847, 1848, 1849, 1850, 1852.**

## WHICH LEAVES GIUSEPPE, AND THAT IS NOW A MEASURED NEGATIVE

**Giuseppe Falco is not in Arienzo's birth registers between his parents' marriage and 1852.** His
own birth act of 1887 — the one that made him a documented man at all — gives his age as
**forty-six**, so about 1841; **1840 and 1841 are both empty, and so is every other year of the
span.**

*What remains: he was born in another comune; or his birth was never registered civilly; or his
stated age is wrong by enough to put him after 1852 — **and this household's ages are wrong by up to
twelve years elsewhere**, so that is not idle.* **The ninth child the tree counts is unnamed, so
there is nothing to look for.**

**By-catch of 1834**, recorded and not pursued: **Angela Raffaela Falco, eighteen, of strada
Camellara, wife of Francescantonio Falco, twenty-seven** (image 26) — *the first-cousin marriage this
archive already holds* — and **Giovanna Falco, twenty-eight** (image 99).


---

# GIUSEPPE IS NOT IN SANTA MARIA A VICO OR CERVINO — and FALCO is not a surname in either

**9 October 2026.** Giuseppe Falco's own 1887 act makes him «about 1841», and Arienzo's 1840 and 1841
are both empty. The two neighbouring comuni of the same tribunale district were read for the same
two years.

| comune | year | images read | result |
|---|---|---:|---|
| **Cervino** | 1840 | 2–66 | **nil** |
| **Cervino** | 1841 | 2–57 | **nil** |
| **Santa Maria a Vico** | 1840 | 2–152 | **nil** |
| **Santa Maria a Vico** | 1841 | 2–159 | **nil** |

**No Alessandra Crisci. And, more decisively, NOT ONE FALCO MOTHER IN ANY OF THE FOUR VOLUMES.**

## THE SURNAMES THEMSELVES ARE THE ANSWER

*Across roughly six hundred acts, these two towns are made of other families.*

- **Cervino**: Pascarella, Vigliotti, Nappa, de Rosa, Caporale, Sarano, Affinito, Jannotti, Oliveto,
  Riserolli, di Benedetto, Bove. **Falco does not appear.**
- **Santa Maria a Vico**: de Lucia, Piscitelli, Nuzzo, Caprio, Savinelli, Abbatiello, Dabbo, Russo,
  Ruggiero, Vigliotti, Bernardo, Magliulo, Barisciano, Carfora. **Falco does not appear.**

**FALCO IS AN ARIENZO SURNAME.** *No Falco family is resident in either town — not one Falco mother
in six hundred birth acts — so a child of this family being born there would be an exception to the
shape of both.*

> **AND THE SENTENCE THAT STOOD HERE WAS TOO BROAD.** It said Falco «*is not a name these
> neighbouring registers carry at all*». **That is true of the BIRTH registers and FALSE of the
> MARRIAGE registers**, where an Arienzo Falco appears as a groom — see below. *The correction
> matters, because it is the marriage registers the search actually needs.*

## TWO NAMES THAT DO MATTER, AND NEITHER IS HIM

- **NUZZO IS A SANTA MARIA A VICO SURNAME.** Antonia Nuzzo fu Pietro, Caterina Nuzzo di Giovanni,
  Giovanna Nuzzo di Domenico, Giovanna Nuzzo fu Pasquale, Rosa Nuzzo di Biase, Antonia Nuzzo fu
  Simone — six mothers in two years. **Giuseppe Falco's wife was NICOLETTA NUZZO.** *That does not
  locate his birth, but it is the first evidence of where his WIFE's family is from, and it is
  recorded as that and nothing more.*
- **CRISCI IS ALSO A SANTA MARIA A VICO SURNAME** — «Lucia Crisci di Domenico», 1840. *His mother's
  surname exists there too. Neither fact puts a Falco in the town.*

## AND THE TAVOLA LESSON REPEATS

**Cervino 1840 and Santa Maria a Vico 1841 both end with a FILLED «Tavola alfabetica annuale de'
Nati» naming BOTH PARENTS** — Cervino's runs to several leaves, SMaV's begins «*1. Agresta Giuseppe —
Agresta Filippo e … de Lucia — 22 Feb 1841*». **Either would have answered its year in two or three
images instead of nine contact sheets.** *Santa Maria a Vico 1840's is bound in and blank, so it
still cannot be assumed — **but the check is one image and it was not made first.*** The same mistake
as Arienzo 1850 and 1852, made again.


---

# THE SANTA MARIA A VICO MARRIAGE REGISTERS — read to 1865, and the rest is behind a login

**Giuseppe Falco and Nicoletta Nuzzo are not in them.** The six years Antenati holds at the end of
the series — **1860, 1861, 1862, 1863, 1864, 1865** — were read through each volume's own
**«TAVOLA ALFABETICA ANNUALE DE' MATRIMONJ»**, which gives, on one line: *the couple, the groom's
**PATRIA**, both sets of parents, the date of the church wedding and the act number.*

> **THE INDEX IS AT THE FRONT OF THESE VOLUMES, NOT THE BACK.** *Two leaves after the cover.* This
> archive looked at the end first — where the Arienzo birth tavole sit — found the last acts and the
> officer's closing, and concluded there was none. **It had been two images away the whole time.**

## BUT A FALCO IS IN THEM, AND HE IS FROM ARIENZO

**1863, entry 11 of the tavola**, read at magnification:

> «**FALCO DOMENICO, e GUIDA DAMIANA** · *patria* **ARIENZO** · **FALCO GIUSEPPE, e GUIDA
> MICHELANGELO** · **15 Giugno 1863** · act **15**»

**An Arienzo man, marrying a Santa Maria a Vico woman, registered at HER comune — exactly the rule
this archive works by.** *That is the mechanism the whole search depends on, and here it is
demonstrated.*

**`tools/isitnew.py` was run before anything was written down and it hit twice:**

- This archive already holds a household «**Domenico Falco (m. 1844, Santa Maria a Vico)** ×
  Mariantonia Frasca». **A Falco of Arienzo had already been found marrying at Santa Maria a Vico,
  nineteen years earlier.**
- And a **Domenico Falco born 25 November 1816** to «**GIUSEPPE FALCO, 36, *massaro*, strada COSTA**»
  and **Gelsomina Vigliotta** — *the Giuseppe Falco of **strada Costa**, whom this archive's own note
  separates from «the Camellara Giuseppe, this line's own», by the phrase «fu Matteo».*

**NOTHING IS MERGED.** *A 1863 groom named Domenico son of Giuseppe could be that man remarried after
a widowing, or a third Domenico; the act itself has not been read, and act 15 of 1863 is where that
would be settled.* **He is not of this line either way: his father is the Costa Giuseppe, not ours.**

## WHAT IS LEFT, AND WHY IT STOPPED

**The marriage this archive wants is 1866 or later.** The family tree puts Nicoletta Nuzzo's birth at
**1855**, which makes the wedding roughly **1873–1882** — *past the end of Antenati's Santa Maria a
Vico series, which stops at 1865.*

**Those years are FamilySearch's `MC5R-M2Q` (1866–1878, 2,156 images) and `MC5R-Q23` (1879–1894,
3,013), both enumerated to disk and both unreadable: the session returned `401 Unauthorized —
anonymous session` partway through the survey.** *David signs in; this archive never enters
credentials.* **A 401 is a refusal and nothing here is recorded as a negative from it.**


---

# `MC5R-M2Q` READ — Santa Maria a Vico's marriages 1873–1877, and Giuseppe is in none of them

**The session was signed in again on 9 October and the volume surveyed entire: 2,156 thumbnails, 23
sheets, zero refusals.** *The 117 fetched before the 401 were cached and skipped — the ark list came
from the open API and never needed the cookie.*

## THE BOOK MAP, from 49 covers found by brightness and the leaf after each read whole

| year | marriage material | how it was read |
|---|---|---|
| **1873** | **tavola, images 1061–1065** | B · C · D · **then L** — *no E, F or G section exists* |
| **1874** | **tavola, image 1185 and 1272** | D · **F = «Folgieri Pio» alone** · G |
| **1875** | **no tavola — acts 1377–1404** | **swept act by act at the margin box**, Parte I acts 1–47 **and Parte II** |
| **1876** | **tavola, image 1569** | E · **F = «Francescopi Alessandro», «Fruggiero Vincenzo»** · G · L |
| **1877** | **tavola, image 1748** | D · E · **then M** — *no F section exists* |

**NOT ONE FALCO GROOM IN ANY OF THE FIVE YEARS.**

## THE INSTRUMENT, AND IT IS THE BEST ONE YET

**«Tavola alfabetica annuale de' MATRIMONI»**, bound at the FRONT of each year's marriage book,
printed with the columns: **«COGNOMI E NOMI de' SPOSI · PATRIA · COGNOMI E NOMI de' GENITORI · GIORNO
della celebrazione»**. *The couple, where the groom is FROM, and both sets of parents, on one line.*
**One leaf answers a year.**

**And where a year has no tavola — 1875 — the printed form still gives it away for almost nothing:**
from 1866 each act carries a **NAME BOX down the outer margin** with «Numero N» and the two
surnames. **A strip of the outer margins reads every couple in the book without opening a single
act.** `fsmargin.py` does it; twenty-eight leaves became four strips.

## WHAT IS STILL NOT COVERED, SAID PLAINLY

- **1878's marriage book was not located in this volume.** Its deaths (1957–2007), its births index
  (2012) and its Parte I title pages are mapped; the marriages are not.
- **1866–1872 were not read at all.** *The window this archive is working to — Nicoletta Nuzzo born
  1855 on the tree, so a wedding about 1873–1882 — does not reach them, but they are part of the
  volume and they are unread.*
- **1879–1882, the rest of the window, is `MC5R-Q23`** — 3,013 images, enumerated to disk, unsurveyed.

*Santa Maria a Vico does take Arienzo grooms: the 1863 tavola has **Falco Domenico of Arienzo**, and
the 1876 one has **Guida Angelandrea of Arienzo**. The mechanism is real; this is simply not where
Giuseppe married, in the years read.*


---

# `MC5R-Q23` — three of its marriage years read, and Giuseppe is in none of them

**Santa Maria a Vico, 1879–1894, 3,013 images.** *The ark index came from the open API and is on disk
as `data/smav-q23-tribunale-images.tsv`; the thumbnail survey is part-run.*

**The volume does NOT run year by year in a single line.** Probing at fifty-image steps shows the
books interleaved — deaths, births, marriages, an index, deaths again — so the marriage books had to
be found by probe rather than by arithmetic.

| year | marriage material | how read | result |
|---|---|---|---|
| **1880** | **«MODULO DELL'INDICE ANNUALE *dei Matrimoni*», image 139**; book 141+ | **the whole index**, 25 couples, A–R | **F section = «Fannucci Alfonso» ALONE** |
| **1882** | book 487–514 | **margin-box sweep**, Parte I acts 1–35 **and Parte II** | no Falco |
| **1883** | book 643–670 | **margin-box sweep**, Parte I acts 1–29 **and Parte II** | no Falco |

**NOT ONE FALCO GROOM IN ANY OF THE THREE.**

## THE 1880 INDEX IS WORTH KEEPING FOR ITS OWN SAKE

It is the **«Modulo dell'Indice annuale dei Matrimoni»** — two columns a page, **groom and bride with
each one's patronymic, and the act number**. Twenty-five couples on one leaf. *The sections run A · B
· C · D · **E** · **F** · L · M · N · P · R — the alphabet is complete and the F section holds one
man who is not a Falco.*

**And it carries a NUZZO:** «*19 — **NUZZO Clemente di Michele** / Greco M.ª Giuseppa fu Carmine —
act 9*». **Nicoletta Nuzzo's family marries at Santa Maria a Vico**, which is the reason for looking
here at all — *and it is still not Giuseppe.*

## WHAT IS NOT COVERED, AND IT IS MOST OF THE VOLUME

- **1879, 1881 and 1884–1894 are unread.** Their marriage books were not located; the survey that
  would find every cover is **645 of 3,013 images in** and was deliberately left running rather than
  raced against the probes.
- *The working window — Nicoletta Nuzzo born 1855 on the tree, so a wedding about 1873–1882 — is
  **covered for 1880 and 1882 and open for 1879 and 1881.***

**`tools/fsmargin.py` earns its place again**: the 1882 and 1883 books, fifty-six leaves between
them, became eight strips and two readings. *No act was opened.*


---

# THE SURVEY IS FINISHED AND 1879 AND 1881 ARE READ — no Falco groom, but a FALCO BRIDE

**`MC5R-Q23` surveyed entire: 3,013 thumbnails, 32 sheets, zero refusals. 58 covers found by
brightness.** *Both Santa Maria a Vico volumes are now surveyed end to end — 5,169 thumbnails
between them, and not one refusal in either.*

## AND THE COVERS SETTLED A QUESTION THE CATALOGUE HAD ALREADY ANSWERED

**1879's marriages are NOT in this volume.** The catalogue title says it plainly — «*Morti,
cittadinanze **1879**; Nati, pubblicazioni, matrimoni, morti, cittadinanze **1880**-1893*» — **1879
here is deaths and citizenships only.** *Its marriages are at the far end of the PREVIOUS volume,
`MC5R-M2Q`, images 2125–2152, behind a section of allegati from S. Felice a Cancello.* **A volume's
own title is a holdings statement and this one was read too quickly the first time.**

| year | where | how read | result |
|---|---|---|---|
| **1879** | **`MC5R-M2Q` 2125–2152** | **«MODULO DELL'INDICE ANNUALE. Matrimoni», images 2130–2131** | **F = «Fruggiero Antonio fu Raffaele» and «Fierro Nicola di Angelantonio»** |
| **1881** | **`MC5R-Q23` 311–337** | **the index on the facing page of image 311** | **F = «Fantarella Andrea di Paolo» ALONE** |

**NO FALCO GROOM IN EITHER.**

## BUT 1881 HAS A FALCO BRIDE, AND SHE IS NEW

> «**13 — Marca (della) Cristofaro fu Giuseppe / FALCO FILOMENA fu ANTONIO — act 30**»

**A Falco woman marrying at Santa Maria a Vico in 1881, daughter of a dead Antonio Falco.**

*`tools/isitnew.py` was run before this was written down.* **She is not this archive's Filomena
Falco**: the one born 20 June 1839 to Matteo Falco and Alessandra Crisci married **Antonio Crisci**
and is named as his wife in the birth act of their son in 1872. *Nor is she the Filomena Falco who
died aged one in 1839.* **Nothing is merged. She is a third woman of the name, and her father is a
dead Antonio Falco who is not the Antonio Falco × Carmela Guida of this archive — that one was still
alive in 1891.** *The act itself, number 30 of 1881, is unread.*

**AND THE NUZZO ARE EVERYWHERE IN THESE INDEXES**: 1880 gives «Nuzzo Clemente di Michele»; 1881 gives
**«Nuzzo Ferdinando di Michelangelo», «Nuzzo Salvatore fu Giuseppe»** and a «Nuzzolo Raffaele di
Giuseppe». *Nicoletta Nuzzo's family is a Santa Maria a Vico family — which is why this was the right
place to look, and makes the absence of her husband the more pointed.*

## THE RUNNING NEGATIVE ON GIUSEPPE

**He is now absent from:** Arienzo's births **1834–1852** entire · Cervino's and Santa Maria a Vico's
births **1840–41** · Santa Maria a Vico's marriages **1860–65, 1873–77, 1879–1883**.

*Still unread at Santa Maria a Vico: marriages **1866–1872**, **1878**, and **1884–1894**.*

---

# 9 OCTOBER 2026 — 1884 IS READ, AND THE TOOL THAT READ IT HAD BEEN READING HALF A BOOK

## THE BUG FIRST, BECAUSE IT TAINTS WHAT CAME BEFORE

`tools/fsmargin.py` sweeps the **Numero box** that the printed form from 1866 prints down the
**outer edge** of each act. Two acts to an opening, one per page, so two crops per image: the left
page's box and the right page's.

**It cropped the right page at `0.515–0.675` — the blank INNER edge of the right-hand form.**
The left crop was right, the right crop photographed nothing. So every book swept with it was read
on its **odd-numbered acts only**, and reported as a whole book.

**The tell was in the output the whole time and I did not read it as a tell**: the labels ran
`2 · 4 · 6 · 8` down one band and `1 · 3 · 5 · 7` down the other, and a register whose acts run odd
on every left page and odd again on every right page is not a register. *A sweep that returns a tidy
run of odd numbers is not a book; it is half a book.*

Found by pulling **one whole leaf** — `MC5R-Q23` image 811 — after three failed attempts to find an
act by number. The leaf shows «**Numero 11 — Cioffi Michele / Piscitelli Maria Teresa**» at the far
left and «**Numero 12 — Sinti-Roger Tommaso Francesco / Petrucci Vincenza**» at the far **right**.
*One full-leaf `dist.jpg` would have caught this on the first book.*

**Crop corrected to `0.790–0.945` and the comment in the file now names the mistake.**

### THE RE-READ, AND IT COST NOTHING

`fsmargin.py` caches every leaf it fetches, so re-cutting the right band was **zero requests**.
**Four books re-swept on their even acts:**

| year | Parte I | even acts now read | Parte II | Falco? |
|---|---|---|---|---|
| **1875** | 1–48 | **2–48** | **n. 2 De Lucia × De Orazio · n. 4 Batista × Sibilio** | no |
| **1879** | 1–38 | **2–38** | **n. 2 Pisco × Moluso · n. 4 De Lucia × Valentino · n. 6 Migliore × Ruggiero** | no |
| **1882** | 1–36 | **2–36** | **n. 2 Marco × Dec** | no |
| **1883** | 1–29 | **2–28** | **n. 2 Sofia × Vigliotti** | no |

**The four nils stand — but they stood on half the evidence until today, and that is published
rather than quietly repaired.** *1873's Parte II (images 1066–1072) is hand-written on lined paper
with no printed Numero box, so the margin band cannot read it. **It is seen and NOT read**, and is
not counted as a negative.*

## 1884 READ ENTIRE — Parte I acts 1–57, both pages, and Parte II

**No Falco groom and no Falco bride in the printed register.** The book ends at act 57; act 58 is a
blank form.

## AND THE ONE AMBIGUOUS INDEX LINE RESOLVES — IN A PART OF THE BOOK NOBODY HAD OPENED

The 1884 yearly index (image 802) carried, under **F**, a line this archive could not read:

> «**Fa—o (de) Bartolomeo / Santoro Clementina**»

— ambiguous between **Falco** and **Fallo** at every magnification, and its register number matched
**no act in the printed book**. Three acts were opened on three different readings of that number
(38 = Ruggiero Carlo, 58 = a blank form, 34 = Vigliotti Arcangelo) before the book was swept whole.

**It matched no act because the printed register is only PARTE I.**

**`MC5R-Q23` image 835R opens a second register** — a title page, then acts written by hand on
**lined paper**, numbered from one again. This is **Parte II**: marriages not celebrated at the Casa
Comunale. **Parte II, act 3, is the F-section line:**

> «*L'anno milleottocentottantaquattro addì **quattordici di Luglio** a ore pomeridiane **nove e
> minuti trenta** nella Casa posta alla **Piazza Municipio Numero Trenta**. Avendo la Signora
> **Santoro Clementina** col mezzo del certificato del medico Signor **Matteo Aniello** in data di
> oggi stesso giustificato, che **per una contusione al ginocchio destro** è ella stessa
> assolutamente impedita di recarsi alla Casa Comunale per celebrare il matrimonio, io **Carfora
> Alfonso Sindaco** … col mio Segretario Signor **Savastano Donato** mi sono trasferito in questa
> casa ove ho trovato: Primo il Signor **Commendatore DE FALCO BARTOLOMEO, di anni sessantasei,
> proprietario, nato in NAPOLI, residente in ARIENZO**, figlio del fu Signor **Eufemio** residente
> in vita in Napoli, e della fu Signora **DE GIORGIO MARIANTONIA** … Secondo la detta Signora
> **SANTORO CLEMENTINA, di anni trentasette, proprietaria, nata a CASERTA**, residente in
> Santamaria a Vico, figlia del fu Signor **Matteo** … e della Signora **HUEBER ISABELLA**,
> residente in **Valle di Maddaloni***»

**She was lame, so the mayor came to her house at half past nine at night. That is the whole reason
this act is not in the printed book.**

The documents are the publications made at Santa Maria a Vico on 29 June and 6 July 1884 **«e di
quelle eseguite nel Comune di ARIENZO nei suindicati giorni»** — *the act's own statement that one
of them lived at Arienzo, and he is the one who was not resident at Santa Maria a Vico.*

Witnesses, all **proprietari**: Cav. **Pasquale Ruoti** 73 · Cav. **Tommaso Ruoti** 64 ·
**Giuseppe de Ferrellis** 37 · **Giovanni de Ferrellis** 33. Both spouses signed.

### HE IS NOT JOINED TO ANYTHING

**`de Falco` is not `Falco`, and nothing here merges them.** This archive already holds a gentry
**de Falco** of Arienzo — *Don Francesco Falco, proprietario*, whose daughter **Donna Raffaela de'
Falco** died a nun in the Monastero d'Ave Gratia Plena in 1836. **Bartolomeo was born at Naples to
Neapolitan parents**; nothing read joins him to that house either. He is recorded as
`bartolomeo-de-falco-clementina-santoro` **because anyone searching Arienzo for a Falco in the
1880s will meet a Commendatore, and should meet him already labelled.**

## THE METHOD FINDING, AND IT IS THE BIGGEST OF THE THREE

**PARTE II IS WHERE THE INTERESTING MARRIAGE IS.** Parte II holds what Parte I cannot: the bride
too ill to walk to the town hall, the marriage celebrated elsewhere and transcribed, the deathbed
marriage, the proxy. **These are exactly the marriages of people who moved** — and a man who cannot
be found in his own town's register is, by definition, a man who moved.

**In 1884 the ONLY Falco-adjacent act in the entire volume was in Parte II.**

So: **sweep to the end of the volume, not to the end of the printed acts.** The blank form after the
last act is not the end of the book — it is the middle of it.

## THE RUNNING NEGATIVE ON GIUSEPPE, RESTATED

**Absent from:** Arienzo's births **1834–1852** entire · Cervino's and Santa Maria a Vico's births
**1840–41** · Santa Maria a Vico's marriages **1860–65, 1873–77, 1879–1884** — *and 1875, 1879,
1882, 1883 and 1884 now on both pages and through Parte II.*

*Still unread at Santa Maria a Vico: marriages **1866–1872**, **1878**, and **1885–1894**.*

---

# 1885 READ ENTIRE — no Falco, and a SECOND NICOLETTA NUZZO

**`MC5R-Q23` images 1032–1067.** Yearly index at **1032R–1033L**; printed register **acts 1–47**,
images 1035–1058 (act 48 is a blank form); **Parte II** at 1060–1064.

## THE INDEX SETTLES THE YEAR IN ONE PAGE

«**MODULO DELL'INDICE ANNUALE dei matrimoni 1885**», and it is the cleanest instrument this volume
has yielded: one line per marriage, groom over bride, with the father's name on the groom
(«*fu Antonio*», «*di Gennaro*») and the register number in its own column.

**The F section has ONE entry and it is not a Falco:**

> «**18 — Ferrara Giuseppe di Gennaro / Di Caprio Mª Michela — reg. 22**»

**The margin sweep of all 47 acts agrees.** Parte II is a single sheet: an **extract from the
register of SAN FELICE A CANCELLO**, «Renotolo Giuseppe / Liparulo Clementina», 11 October 1885.

## AND ENTRY 21 IS THE NAME OF GIUSEPPE FALCO'S WIFE

> «**21 — Guida Antonio fu Lorenzo / NUZZO NICOLETTA — reg. 28**»

**The act was read rather than reasoned about** — *an index line is a finding aid, never a reading* —
and it is **act 28, 30 August 1885, ten fifteen in the morning**:

> «*1.° **Guida Antonio**, di anni **sessantasette**, contadino, nato in Santamaria a Vico, residente
> in Santamaria a Vico, figlio **del fu Lorenzo** … e **della fu Pascarella Lucia** …
> 2.° **Nuzzo Nicoletta**, di anni **cinquantatré**, contadina, **nata in Santamaria a Vico**,
> residente in detto Comune, **figlia del fu Domenico** … e di **Mª fu Stola Mariantonia***»

Witnesses **Luca Carfora**, 33, *possidente*, and **Alfonso Porrino**, 58, *sarto*; publications 16
and 23 August; **both spouses illiterate**.

### SHE IS NOT OURS, AND THE ARCHIVE'S OWN RECORD IS WHAT PROVES IT

**`tools/isitnew.py` was run before a word of this was written down.** This archive holds **Nicoletta
Nuzzo alive and living with Giuseppe Falco at Arienzo, via Orticelli 4, on 22 September 1887**,
bearing their daughter Maria — *«da **NICOLETTA NUZZO sua moglie, CONTADINA, seco lui convivente**»*,
Arienzo birth act 114 of 1887, read from the image.

**A woman cannot be married to Giuseppe Falco at Arienzo in September 1887 and marrying Antonio Guida
at Santa Maria a Vico in August 1885.** So **there are two women of the name**, and the second one is
now fully named: **Nicoletta Nuzzo, born about 1832 at Santa Maria a Vico, daughter of the late
DOMENICO NUZZO and the late MARIANTONIA STOLA.** *Nothing is merged. She is recorded so that the next
search for «Nicoletta Nuzzo at Santa Maria a Vico» does not stop here and think it has arrived.*

**The age is worth keeping too.** Ours was married to a man who was **46 in 1887**, so born about
**1841**; this one was born about **1832**. *That is not proof on its own — nine years is an ordinary
gap — but it is one more thing that does not fit.*

## THE RUNNING NEGATIVE

*Still unread at Santa Maria a Vico: marriages **1866–1872**, **1878**, and **1886–1894**.*

---

# 1886 AND 1887 — no Falco, and the yearly index turns out to read a whole year in one leaf

## 1886 — `MC5R-Q23` 1248–1280

Index at **1248R–1249L**; Parte I **acts 1–42**, images 1251–1274; **Parte II acts 1–4**, 1276–1278.
Swept at the margin box on both pages, and the index read.

**The F section has three entries and none is a Falco:**

> 22 **Ferrara Michele** / De Lucia Mariantonia — reg. **5**
> 23 **Fontana Salvatore Maria** / Tabaresta Erminia Francesca — reg. **2. S.**
> 24 **Ferrellis (de) Giovanni** / Piscitelli Filomena — reg. **4. S.**

## AND «S.» IN THE NUMBER COLUMN MEANS *PARTE SECONDA*

**Proved, not inferred.** The 1886 index's four «S.» entries — 1. S., 2. S., 4. S. and (entry 29)
Langella Giovanni 1. S. — are matched **one for one** by the margin boxes of **Parte II acts 1, 2 and
4** at images 1276–1278: «Langella Giovanni / De Ferrellis Maria» is Parte II n. 1, «Signor Fontana
Salvatore Maria / Signora Taborista Erminia Francesca» is n. 2, «Signor De Ferrellis Giovanni /
Signorina Piscitelli Filomena» is n. 4.

**And 1887 writes it out in full: «1. P.S.», «2. P.S.», «3. P.S.», «4. P.S.»** — *Parte Seconda*.

**So the index itself has been pointing at Parte II the whole time**, in a column this archive was
reading as if it held one run of numbers. *That is what defeated the 1884 de Falco line: its number
was a Parte II number, and three Parte I acts were opened on three readings of it before the volume
was swept whole.*

## 1887 — `MC5R-Q23` 1479–1480, read from the index alone

> «**Indice annuale pel Registro dei Matrimonii dell'anno 1887**»

**Fifty-five entries, A to Z, Parte I to act 51 and four Parte Seconda acts. The E/F section is:**

> 17 **Fantarella Domenico** / Di Francesco Antonia — **1. P.S.**
> 18 **Frasca Antonio** / Vigliotti Maria Grazia — **2. P.S.**

**NO FALCO, as groom or as bride.**

## THE METHOD FINDING: THE YEARLY INDEX NAMES **BOTH** SPOUSES

**Every entry is two lines — the groom on the first, the bride on the second** — so although the
index is *alphabetised by the groom*, **a surname search over it covers the brides as well.** One
leaf, sometimes two, reads a whole year for any name.

**That is thirty leaves of margin sweep replaced by two**, and it is how the rest of this volume
should be read. *With the standing caution intact: an index line is a finding aid, never a reading —
the Sosso error was an index line. **A nil may rest on the index; a hit must be taken to the act.***

**By-catch, not merged:** **1887 entry 47, «Rivetti Nicola / Vigliotti Luigia», reg. 49.** *Rivetti is
one of this archive's own surnames — Chiara Rivetti married Pasquale Falco — and this is a Rivetti at
Santa Maria a Vico in 1887. **No kinship is claimed and the act is unread.***

## THE RUNNING NEGATIVE

*Still unread at Santa Maria a Vico: marriages **1866–1872**, **1878**, and **1888–1894**.*

---

# 1866–1872 AT SANTA MARIA A VICO — AND A FALCO FAMILY LIVING THERE

## HOW THE INDEXES WERE FOUND, BECAUSE THE METHOD IS REUSABLE

`MC5R-M2Q` is 2,156 images and holds every series — nati, matrimoni, morti, pubblicazioni,
cittadinanze — for 1866–1878, one book after another with nothing to say where a book begins.

**A cover in this film is a near-black thumbnail.** The 2,156 thumbnails were already cached from an
earlier survey, so **mean brightness below 45% of the volume median found 53 book boundaries at zero
requests**. Then **the leaf immediately after each cover is the book's printed title page** — and 28
of those, fetched in **28 requests**, named every register in the first thousand images:

> img 2 «1866 · S. Maria a Vico · Matrimonj» · img 306 «Anno 1868 · REGISTRO delle Nascite» ·
> img 372 «REGISTRO DI MORTE» · img 441 «REGISTRO Anno 1869 Nascita» · img 550 «REGISTRO di
> MATRIMONIO 69» · img 604 «REGISTRO Anno 1869 di Cittadinanza» · img 874 «Anno 1872 … REGISTRO di
> Nascite» · img 936 «Anno 1872 … REGISTRO di Matrimoni»

**Covers from thumbnails, titles from the leaf after the cover.** *That is a whole film mapped for
twenty-eight requests, and it is how the rest of this collection should be opened.*

## FIVE YEARS READ

| year | index | marriages | Falco? |
|---|---|---:|---|
| **1866** | img 59–60, «*Indice Annuale de' Matrimoni dell'anno 1866*» | **28** | no |
| **1867** | img 211, «*Indice degli atti di matrimonii celebrati nel Comune di S.ta Maria a Vico dell'anno 1867*» | **35** | no |
| **1870** | img 672–673, «*Indice de' Matrimoni contratti nell'anno 1870*» | **64** | no |
| **1871** | img 804–805, «*Indice Alfabetico dei Matrimoni dell'anno 1871*» | **47** | no |
| **1872** | img 934–935, «*Tavola alfabetica annuale de' MATRIMONI*» | **33 entries, reg. to 36** | **YES** |

*Every one of these indexes names **both** spouses, so the brides are covered too.*

## 1868 AND 1869 ARE NOT READ, AND NO NEGATIVE IS CLAIMED FOR THEM

**The book behind the 1868 cover at image 356 was never used.** Fifteen leaves, ruled and blank,
with a single stray margin note, closed in the clerk's hand: «*chiusa in questo giorno trenta di
Dicembre dell'anno 1868*». **The 1869 book at 551 is a supplement of *trascrizioni*** — its acts are
numbered in the **fifties** and are transcriptions received from other comuni.

**So the main marriage registers of 1868 and 1869 are not in the part of this film that has been
mapped**, and they are recorded as *not located* rather than as empty. *An unused supplement is not
a year's marriages, and reading it as one would be the same mistake as reading a full-text search as
a holdings list.*

# AND NOW THE FINDING: A FALCO HOUSEHOLD AT SANTA MARIA A VICO

The 1872 tavola, entry 10:

> «**10 | 35 | Folgieri Salvatore** e | S.ta Mª a Vico | *di Clemente e fu Daddio Rachele* | **28
> Dicembre** — **e FALCO LUCIA** | Idem | *di Antonio e della Zorca Vincenza*»

**The tavola is a finding aid, so the act was read.** Image 952, left page:

> «*Numero d'ordine **trentacinque** — Atto di matrimonio tra Salvatore Folgieri e Lucia Falco.
> L'anno milleottocentosettantadue il giorno **ventotto Dicembre** in Santamaria a Vico. Innanzi a me
> **Gabriele Bernardo Sindaco** … ed alla presenza di **Pietro Marletta fu Matteo, d'anni
> sessantacinque**, e di **Fabrizio de Lucia fu Giuseppe, di anni cinquantadue**, ambo **scrivani
> comunali** … sono comparsi **Salvatore Folgieri, di anni trenta, colono**, residente in Santamaria
> a Vico, figlio di **Clemente**, colono, e della fu **Rachele Daddio**, **e LUCIA FALCO, di anni
> VENTIQUATTRO, COLONA, residente in SANTAMARIA A VICO, figlia di ANTONIO e di VINCENZA DELLA ZORCA,
> COLONI, RESIDENTI COLLA FIGLIA** … **essendo gli sposi analfabeti***»

**Father, mother and daughter, all three coloni, all three living at Santa Maria a Vico.**
Held as `antonio-falco-vincenza-della-zorca`. **Lucia born about 1848.**

*`tools/isitnew.py` was run before a word of this was written. She is **not** the archive's Francesca
Maria Lucia Falco, baptised at Arienzo in 1812 and married in 1839. **Nothing is merged.***

## WHICH BREAKS A SENTENCE THIS ARCHIVE PUBLISHED THIS MORNING

> «**FALCO IS AN ARIENZO SURNAME.** *No Falco family is resident in either town.*»

**What survives**: not one Falco mother appears in Santa Maria a Vico's births of **1840 and 1841**,
and that reading stands. **What does not survive is the present tense.** *A family absent from a
town's birth register in 1840 may have moved there by 1872, and this one had. The error was turning
a two-year nil into a statement about the town.* A `major` correction is published.

## AND IT MAY BE TWO SISTERS

The 1881 index at the same comune: «*Marca (della) Cristofaro fu Giuseppe / **FALCO FILOMENA fu
ANTONIO**, act 30*».

**Antonio Falco is alive in December 1872 and «fu» — dead — by 1881**, and both women marry out of
the same small comune. **He is NOT the archive's Antonio Falco × Carmela Guida**, who was alive in
1891. *That is a reason to look, not a proof of sisterhood. **The 1881 act is unread.***

## THE RUNNING NEGATIVE ON GIUSEPPE

**Absent as a groom from Santa Maria a Vico's marriages of 1860–67, 1870–77, 1879–87.**
*Unread: **1868, 1869** (registers not located) and **1888–1894**.*

---

# THEY ARE SISTERS — the 1881 act is read, and it brackets Antonio Falco's death

**`MC5R-Q23` image 329, right page. Santa Maria a Vico, marriage act 30 of 1881.**

> «*L'anno milleottocento **ottantuno**, addì **quindici** di **Ottobre**, a ore antimeridiane
> **undici** e minuti **quarantacinque**, nella Casa comunale di Santamaria a Vico … Avanti di me
> **Nuzzi Felice, assessore anziano funzionante da Sindaco** …
> **1.° Della Marca Cristofaro, di anni trentadue, colono, nato in S. Felice a Cancello**, figlio
> del fu Giuseppe e di Di Palma Mariantonia, colona;
> **2.° FALCO FILOMENA, di anni VENTISEI, COLONA, NATA IN SANTAMARIA A VICO, residente in
> Santamaria a Vico, FIGLIA DEL FU ANTONIO** … **e di DELLA TORRE VINCENZA**, residente in detto
> Comune*»

Witnesses **Pietro Marletta** and **Alfonso Porrino**, both *sarti* of the comune.

## WHAT IT SETTLES

**Same father Antonio, same mother Vincenza, same comune, both daughters coloni.** **Filomena is
Lucia's sister**, and the house is now three generations deep in documents rather than one act.

**And this archive had published her as a stranger.** On the morning of 9 October the 1881 index line
«*FALCO FILOMENA fu ANTONIO*» was written up as **«a third woman of the name»** whose act was unread.
*It is read now, and she is not a third woman: she is of this house. **The note that called her a
stranger is left standing above this one**, because that is how this archive handles being wrong.*

**THE MOTHER'S SURNAME IS SETTLED: «DELLA TORRE».** The 1881 hand is clean. The 1872 act's rendering —
recorded here as «della ?orca», unresolved rather than normalised — is consistent with it. *The
uncertainty stays on the page it came from.*

**FILOMENA WAS BORN AT SANTA MARIA A VICO, about 1855.** So the Falco household was living there by
**1855**, not merely by 1872. *That is twenty-six years earlier than the archive's statement that no
Falco family lived in the town, and fourteen years after the birth registers of 1840–41 that the
statement rested on.*

## AND IT BRACKETS A DEATH, WHICH IS THE NEXT THING TO READ

**Antonio Falco is alive on 28 December 1872 and «fu» on 15 October 1881.**

**His death act is in Santa Maria a Vico's death registers of 1873–1881** — and a death act of this
period gives the dead man's **age, his birthplace and his parents**.

> **If Antonio Falco was born at ARIENZO, this household is a bridge between the two towns, and the
> search for Giuseppe stops being a search of one comune.**

*That is the next job: the annual death indexes of 1873–1881, which the cover map already makes
cheap to find.*

## A NOTE ON THE MARGIN BOX, SO THE NEXT SWEEP DOES NOT MISREAD THIS BOOK

**The 1881 book does not lay its Numero box where the 1884 book does.** Here each page carries its
own box at the **inner** edge — the right page's box sits at about **x = 0.52**, not 0.80 — so a
margin sweep tuned to 1884 reads the odd acts of 1881 and calls them the book. *The crop is a
property of the printing, not of the collection: **look at one whole leaf before trusting a band**,
every time the printer changes.*

---

# A SECOND FALCO HOUSE AT SANTA MARIA A VICO — and the death tavole are the instrument

**Antonio Falco, father of Lucia and Filomena, died between 28 December 1872 and 15 October 1881.**
Santa Maria a Vico's annual **death tavole** were opened to find him, and they are the richest
finding aid in this collection: four columns — **«N.° DEL REGISTRO · COGNOMI E NOMI de' MORTI ·
COGNOMI E NOMI de' GENITORI · EPOCA DELLA MORTE»** — so **a death tavola names the dead person's
PARENTS** and gives the day and month.

Found with the cover map: the tavola is the leaf after the deaths cover. **1873 at image 1087,
1874 at 1216.**

| year | F section | Falco? |
|---|---|---|
| **1873** | entries 88–92: Ferraro, Froggiero ×3, Filippone | **no** |
| **1874** | entries 41–48: Fonace, Fontanella ×2, Froggiero ×3, Fanino — **and entry 47** | **YES** |

> «**47 | 176 | FALCO ANTONIO | Giuseppe e [Verdicchio] Orsola | 24 [Novembre]**»

## AND THE ACT IS NOT THE MAN WE WERE LOOKING FOR — IT IS A DIFFERENT HOUSE

**Image 1266, right page, act 176, read at magnification:**

> «*L'anno milleottocentosettantaquattro il giorno **ventisette Novembre** alle ore nove
> antimeridiane … sono comparsi **Pietro Marletta fu Matteo, d'anni sessantasette, inserviente
> comunale**, domiciliato in questo Comune, Via Perrecchia, e **Fabrizio de Lucia fu Giuseppe,
> d'anni cinquantaquattro**, di condizione simile, domiciliato ivi Via Riesi; i quali hanno
> dichiarato che nel giorno suddetto alle ore **sette antimeridiane** in questo Comune **nella casa
> di sua abitazione sita alla VIA SANT'APOLLONIA è morto ANTONIO FALCO, D'ANNI DUE, figlio di
> GIUSEPPE ed ORSOLA VERDICCHIO, COLONI, domiciliati ivi***»

**A child of two, born about 1872** — not the Antonio who gave two daughters away. *The tavola named
him «Falco Antonio» and the age is nowhere on the tavola. **This is the Sosso rule again: the index
told the truth and the act told the meaning.***

## WHICH MAKES TWO FALCO HOUSEHOLDS IN THE TOWN, NOT ONE

| household | where | documented by |
|---|---|---|
| **Antonio Falco × Vincenza della Torre** | Santa Maria a Vico | daughters' marriages, 1872 and 1881 |
| **Giuseppe Falco × Orsola Verdicchio** | **Via Sant'Apollonia** | son's death, 1874 |

**No kinship is claimed between them.** *Two Falco families at Santa Maria a Vico in the 1870s is
the finding; joining them would be a guess.*

### AND THIS GIUSEPPE FALCO IS NOT OURS — from dates, not from a feeling about the name

**Ours was married to NICOLETTA NUZZO and fathering children by her at Arienzo through exactly these
years** — Filomena in 1872, Vincenza in 1874, both from certified extracts in the processetti. **He
cannot also be the husband of Orsola Verdicchio in the same two years.**

*`tools/isitnew.py` on **Verdicchio** returns «nothing, in any corpus». The name is new to this
archive.*

## WHAT IS STILL OPEN

**Antonio Falco × Vincenza della Torre is not in the death tavole of 1873 or 1874.** He died
**1875–1881**, and those tavole are the next six leaves to read: *1875 and 1876 in `MC5R-M2Q`,
1877 and 1878 in the same film, 1879–1881 in `MC5R-Q23`.* **His act would give his age, his parents
and — the only question that matters — HIS BIRTHPLACE.**

## THE DEATH TAVOLE, YEAR BY YEAR

| year | tavola | F section | Falco? |
|---|---|---|---|
| **1873** | img 1087–1090 | Ferraro, Froggiero ×3, Filippone | no |
| **1874** | img 1216–1219 | Fonace, Fontanella ×2, Froggiero ×3, Fanino, **Falco Antonio** | **the two-year-old** |
| **1876** | img 1604–1605 | **two entries only**: Froggiero Mª Rosa, Fantarella Andrea | no |
| **1878** | img 1927–1928 | Fantarella ×3, Froggieri ×4, Ferrara | no |

**Antonio Falco × Vincenza della Torre is in none of them.** *He died in **1875, 1877, 1879, 1880 or
1881**.*

## AND THE FILM IS TWO REELS SPLICED, WHICH IS WHY THE YEARS ARE OUT OF ORDER

**Image 1475 is an END board**, and 1476 is a fresh target: «*ORIGINALE CONSERVATO PRESSO … **TRIBUNALE
DI S. MARIA CAPUA V., CASERTA** … LOCALITY OF RECORD **SANTA MARIA A VICO, CASERTA** … TITLE OF
RECORD **STATO CIVILE ANNI 1866 A 1910 — NASCITE, PUBBLICAZIONI…***», operator *Carfora Vincenzo /
919*, reduction 42×.

**So `MC5R-M2Q` is not one continuous run of years**: it is two reels, and the second restarts the
series. *That is why 1876's deaths tavola sits at 1604 while 1876's births title page sits at 1478 —
and it is why «the next year must be a hundred images further on» has been the wrong instinct in
this volume all day.* **Read the title page; never the position.**

## AND AN ARIENZO DOCUMENT IS BOUND INSIDE SANTA MARIA A VICO'S DEATHS

**Image 1407**, in the 1874 deaths *Parte Seconda*: a letter on the headed paper of the **MUNICIPIO
DI ARIENZO**, «*N. 640 … Arienzo li 26 Ottobre 1874*».

*Parte II of a death register holds deaths that happened elsewhere and were transmitted — so **the
comune of Arienzo wrote into Santa Maria a Vico's register**. **Parte II of these books is a place
where Arienzo people appear in a Santa Maria a Vico volume**, and this archive has not read a single
Parte II of the deaths.*

## 1877 TOO — and its tavola is a loose slip bound in the MIDDLE of the book

The 1877 deaths tavola is not at the front. **It is a loose folded sheet laid over images 1799–1804**,
after the last printed act, and the camera caught it six times as it shifted.

> **F section, entries 52–56**: Fontanella Giovanni · Froggiero Raffaele · Froggieri Angela ·
> Froggieri Giuseppa · Fontanella Andrea. **No Falco.**

*The margin sweep of images 1777–1835 agrees: eighty-seven printed acts, no Falco among them.*

## WHERE ANTONIO FALCO'S DEATH MUST BE

| year | read | Falco |
|---|---|---|
| 1873 | tavola | no |
| 1874 | tavola + act | **a two-year-old of another house** |
| 1875 | **NOT READ — the deaths book is not located** | — |
| 1876 | tavola | no |
| 1877 | tavola + whole register swept | no |
| 1878 | tavola | no |
| 1879, 1880, 1881 | **NOT READ** (`MC5R-Q23`) | — |

**So he died in 1875, 1879, 1880 or 1881.** *Four years left, and the Q23 cover map already puts the
1879 deaths register at image 6.*

# AND A FALCO BIRTH AT SANTA MARIA A VICO IN 1880 — located, NOT read

**`MC5R-Q23` image 63 is «MODULO DELL'INDICE ANNUALE delle nascite 1880».** Its **F** section opens:

> «**57 — Falco M.ª A—ª di Giuseppe —— — reg. 4**»

**A Falco child born at Santa Maria a Vico in 1880 to a GIUSEPPE.** *The index's register-number
column has misled this archive four times in two days, and act 4 of the 1880 births is «**Diglio
Antonio**» — so **the number is not to be trusted and the entry is recorded as LOCATED, NOT READ**.
The 1880 births register runs from image 64 and must be swept at the margin box to find her.*

**Whose child she is matters.** *Giuseppe Falco × Orsola Verdicchio were at Via Sant'Apollonia in
1874 and are the obvious house. **But this archive's own Giuseppe Falco is also a Giuseppe with a
wife**, and the only way to tell is the act — which names the mother.*

---

# «NATO IN ARIENZO» — ANTONIO FALCO IS FOUND, AND HE CROSSES THE FOUR KILOMETRES

**`MC5R-Q23` image 157 is «MODULO DELL'INDICE ANNUALE delle morti 1880», and its F section reads:**

> Froggiero Clemente fu Salvatore — 5
> **FALCO ANTONIO fu GIUSEPPE — 63**
> Fantanella Teresa fu Michele — 124

**The act was read, not assumed.** Image **175, right page**:

> «*L'anno milleottocento **ottanta**, addì **nove** di **Maggio**, a ore antimeridiane **otto** e
> minuti **venti**, nella Casa comunale. Avanti di me **Migliore Pietro Sindaco** … sono comparsi
> **Salvatore Froggiero, di anni quarantasei, colono** … e **Agostino Garofano, di anni cinquanta,
> colono** … i quali mi hanno dichiarato che a ore antimeridiane **quattro** di **ieri**, nella casa
> posta in **VIA MAIANIELLO al numero UNDICI**, è morto **ANTONIO FALCO, di anni SETTANTA, COLONO,
> residente in Santa Maria a Vico, NATO IN ARIENZO, da fu GIUSEPPE, colono … e da Ma[ria] GELSOMINA
> NOBILE, colona … MARITO DI VINCENZA DELLA TORRE***»

Witnesses **Pietro Marletta, 73, sarto** and **Alfonso Porrino, 54, sarto**.

## WHAT IT SETTLES

**«MARITO DI VINCENZA DELLA TORRE» is what makes this him** and not another man of the name — *and
the comune did hold another: the two-year-old Antonio Falco who died in 1874.* **A name alone would
have got this wrong; the wife's name got it right.**

- **Died 8 May 1880 at four in the morning**, Via Maianiello 11, aged **seventy** → **born about 1810**
- **BORN AT ARIENZO**
- son of the late **GIUSEPPE FALCO**, *colono*, and of **Ma[ria] GELSOMINA NOBILE**, *colona*

**The Falco of Santa Maria a Vico came from Arienzo.** *This is the first document this archive holds
that carries a Falco across the four kilometres between the two comuni and says so in the manuscript.*

**And the bracket closes exactly where it was predicted**: alive 28 December 1872, dead by 15 October
1881 — **8 May 1880**.

## THE FATHER IS A GIUSEPPE FALCO, AND THE MOTHER IS A QUESTION

The mother is written «**Ma — Gelsomina Nobile**». **GELSOMINA is legible; the surname is not
certain**, and *Nobile* is recorded **as a reading, not as a resolution**.

**This archive already holds a Giuseppe Falco of Arienzo whose wife was a Gelsomina**: «*Giuseppe
Falco, **36**, massaro di campo of **STRADA COSTA***, and **GELSOMINA VIGLIOTTA**», the parents of
Domenico Falco born 25 November 1816 — the couple this archive separates from its own line
«*by street and wife*». **Thirty-six in 1816 is born about 1780, which is exactly right for a son
born about 1810.**

**NOTHING IS MERGED.** *One act says Vigliotta and the other says Nobile, and two surnames are two
surnames until one of them is re-read.* **What is established is the birthplace. What is offered is
a candidate father.**

> **THE TEST IS ONE VOLUME AWAY**: Arienzo's births of about **1810** — `an_ua14407` (1810) and its
> neighbours — for a **Falco son of Giuseppe and a Gelsomina**. *And Arienzo's marriage registers for
> **Giuseppe Falco × Gelsomina**, which would give Giuseppe's own parents.*

## AND THE «STRADA COSTA» GIUSEPPE MATTERS FOR A SECOND REASON

The 1863 Santa Maria a Vico marriage tavola already held «**Falco Domenico of ARIENZO**» marrying
**Guida Damiana**, father «**Falco Giuseppe**» — *read on 9 October and set aside as «the strada Costa
Giuseppe, not this line».* **Domenico Falco, son of Giuseppe, born at Arienzo 25 November 1816,
married at Santa Maria a Vico in 1863. Antonio Falco, son of a Giuseppe, born at Arienzo about 1810,
died at Santa Maria a Vico in 1880.**

*Two sons of a Giuseppe Falco of Arienzo, both ending up at Santa Maria a Vico, six years apart in
age. **That is a family moving, and it is the shape the search for Giuseppe has been missing.***

---

# AND THE ARIENZO BIRTH ACT WAS ALREADY IN THIS ARCHIVE, READ AND UNCONNECTED

`tools/isitread.py an_ua14406 an_ua14407 an_ua14408` — **run before a single new tile was fetched** —
reports Arienzo's births of **1809, 1810, 1811, 1812 and 1813 all read act by act**. And
`searched.json` for **1813** says:

> **«Act 2, 5 January 1813** — *è comparso **GIUSEPPE FALCO**, di anni **trentatré**, di professione
> **contadino**, domiciliato in detto Comune, **strada COSTA** … da **GELSOMINA VIGLIOTTA** sua
> moglie legittima, di anni **ventotto**, un **maschio** … a cui si è dato il nome di **ANTONIO***.
> The OTHER Giuseppe Falco — of strada Costa, not of Antonia di Guida — and **ANTONIO FALCO is a
> child that household did not have**.»

**That act was read weeks ago, written up, and left as a curiosity.** *It is the same man.*

## THE FIVE AGREEMENTS AND THE ONE DISAGREEMENT, SET OUT PLAINLY

| | Arienzo, birth act 2 of 1813 | Santa Maria a Vico, death act 63 of 1880 |
|---|---|---|
| forename | **ANTONIO** | **ANTONIO** |
| father | **GIUSEPPE FALCO**, contadino, 33 | **fu GIUSEPPE**, colono |
| mother's forename | **GELSOMINA**, 28 | **GELSOMINA** |
| mother's surname | **VIGLIOTTA** | **NOBILE** ← *the disagreement* |
| birthplace | Arienzo, **strada Costa** | «**NATO IN ARIENZO**» |
| date | **5 January 1813** | «**di anni SETTANTA**» → about 1810 |

**The age is three years out, and that is ordinary here.** *This archive's own note on the 1812
volume says it plainly: «these clerks round constantly, and the same day produced a groom aged
«thirty-two» whose birth act makes him thirty-one».* A son of a dead woman, dead himself, aged by two
neighbours at four in the morning, is the softest age in the corpus.

**The mother's surname is the only real obstacle, and it is a reading.** *«Ma—ª GELSOMINA NOBILE» was
magnified three times and the surname does not resolve to Vigliotta — it is not a near-miss, it is a
different word.* **Against it: GELSOMINA is an uncommon forename, and `GIUSEPPE FALCO × GELSOMINA
VIGLIOTTA` is attested in this archive in 1810, 1813 and 1816.**

## SO IT IS PUBLISHED AS A CANDIDATE AND NOT AS A MERGE

**This archive never merges people on a name, and it is not going to start on five agreements and a
contradicted surname.** *What is established is in the manuscript: an Antonio Falco, born at Arienzo
about 1810 to a Giuseppe Falco and a Gelsomina, died a colono at Santa Maria a Vico on 8 May 1880,
husband of Vincenza della Torre.*

**What follows if the identification holds** — and it is written here so the next person can test it
rather than rediscover it:

> **THE STRADA COSTA FALCO HOUSEHOLD MOVED FROM ARIENZO TO SANTA MARIA A VICO.** Antonio, born 1813,
> died there in 1880 with his father recorded as «*domiciliato in Santa Maria a Vico*». His brother
> **DOMENICO**, born at Arienzo 25 November 1816 to the same couple, **married at Santa Maria a Vico
> in 1863** — act 15, father «Falco Giuseppe» — which this archive read on 9 October and set aside.
> **Two brothers, one town, and the father's domicile given as that town in 1880.**

**AND IT IS NOT THIS LINE.** *Our Giuseppe Falco is a son of **Matteo Falco × Alessandra Crisci**, of
the **CAMELLARA** household — the one told apart from strada Costa «*by street and wife*». **The
strada Costa house is a different Falco family and is held as one.*** **But it proves the road: an
Arienzo Falco household did move to Santa Maria a Vico, and its people are in that comune's registers
under «nato in Arienzo».**

## THE THREE TESTS, IN ORDER OF CHEAPNESS

1. **Re-read the mother's surname in the 1880 act** against another capital N and another capital V
   in the same clerk's hand — the control-letter test. *One tile.*
2. **Arienzo's marriages for GIUSEPPE FALCO × GELSOMINA VIGLIOTTA**, which would give Giuseppe's own
   parents and settle whether he is the «*di Francesco*» of the 1810 patronymic.
3. **Santa Maria a Vico's deaths for GIUSEPPE FALCO himself** — the 1880 act says he died before his
   son and was domiciled in that comune, so his act should be in the same series.
