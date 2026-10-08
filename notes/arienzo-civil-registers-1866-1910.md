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

> **NOT YET ATTACHED, AND DELIBERATELY.** Placing these two would mean **creating two households that
> this archive has never held as households** — Pasquale Antonio Falco × Maria Amalia Guida, and
> Antonio Falco × Carmela Guida — both of which exist here only as lines in `notes/QUEUE.md` and the
> tree. *That is a structural decision about the shape of the archive, not a reading, and it is left
> for a deliberate pass rather than taken at the end of a long one.* **The readings are complete and
> the evidence is here when it is made.**

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
