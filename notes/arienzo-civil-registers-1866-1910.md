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

## NOTHING IS ATTACHED TO ANYTHING, AND HERE IS WHY

**Her age, her parents and whether she was wife, widow or child are all on the continuation, and the
continuation is not on the adjacent leaves.** *Checked by name, not assumed*: image 143's right page
carries act **48**, Angela Orologio, entire; image 144's right page carries act **52**, Filomena
Diglio, entire, from its own preamble; image 145's left page opens act **53** from its preamble.
**Three neighbouring pages, three other complete acts.**

> **THIS IS THE SECOND ACT IN TWO DIFFERENT VOLUMES TO DO EXACTLY THIS.** The 1887 Carfora death read
> on the morning of 8 October also ended mid-sentence, at «*residente in A…*», with the filiation
> lost. **Two is a pattern and not an accident, and this archive does not yet know where these
> continuations are.** *Until it does, every act read here may be missing its most load-bearing line,
> and that is now a known hazard rather than a surprise.*

**«Nella casa di MATTEO FALCO» is a lead and nothing more.** Matteo Falco is the father of work-list
row 69's nine children. **But `tools/isitnew.py` returns at least three distinct Antonia Falco in
this archive already**, and more than one Matteo Falco is possible in a town where this is the
commonest surname. **This archive never merges people on a name, and a house is not a kinship any
more than a street was for the Carfora act.** *What would settle it is one line of the continuation.*

**RAFFAELE FALCO, figlio di Vincenzo, aged 47 in 1866 — so born about 1819** — is a Falco this
archive can test against what it holds, and he is recorded here for that purpose and not merged
either.
