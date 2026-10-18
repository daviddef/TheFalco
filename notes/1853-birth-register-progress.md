# Arienzo civil BIRTH register 1853 — read end to end (`an_ua14450`)

> **Delegated read, 18 October 2026; every Falco act re-opened by the archive's own hand.**
> A delegated reader read every act of this volume at about 2,200 px a spread and wrote a roster; it
> reported that **during the middle of its run several image results came back blank** and that it
> carried on transcribing, so **the roster is a finding aid and nothing in it is cited unless it was
> re-opened.** Every Falco act, margin and witness line of this volume was then **re-opened at about 2,400 px
> and read again from the image** (the act 108 witness line and the margins of acts 15 and 16); where the delegated text and the image
> differ, the image decides. The households this produced are in `households.json`; the volume's row is in
> `searched.json` and on `/searched`.

## Volume facts
- Ark an_ua14450, 126 images. Year proved from the manuscript: tavola heading "Tavola alfabetica annuale de' nati per l'anno milleottocentocinquantatre 1853"; every act reads "L'anno mille ottocento cinquantatre"; first act 2 Jan 1853 (image 10R), last act 31 Dec 1853.
- Acts: N = 110 (tavola closing line "numero cento dieci"; register: acts 1-110 unbroken, no gap, no duplicate). Acts 111, 112, 113 are blank pre-printed forms (images 124R, 125, 126; stamped "BLANK PAGES"; "END" pencilled on 111).
- Images: 1 cover, 2-3 title/certificates, 4-9 TAVOLA (page I img4, II img5, III img6 ... closing img9), 10-124 acts, 125-126 blank forms.
- LAYOUT (differs from 1854-56): each image is a spread; the RIGHT page opens act N (header, declarant = very often the levatrice Rosa Balletta, mother, father, all on that one page, with the "Indicazione" baptism column beside it); the LEFT page of the NEXT image carries the end of act N (witnesses, signatures) and the marginal notes (marriages) for act N. So one act = R page of image i + L page of image i+1. One act per image. Images 12, 70, 76, 111 are second filmings of the preceding opening (duplicates, no new acts).
- Rows in 1853.tsv: `image` is the image whose RIGHT page opens the act; witnesses/margins are from image+1 L.
- Tavola (read): page II (img5) covers D..M. The Falco slot is between "Faccia 56" and "Ferrara 63": NO Falco row. So no child surnamed Falco was born in 1853. (Tavola rows cross-checked against ~30 of my act rows: surnames/numbers/dates agreed.)

## Falco appearances (all confirmed at 3300 px unless stated)
No Falco child, father, mother or declarant. Three Falco names in MARGINAL notes (marriage of the child, twenty+ years later) and one Falco WITNESS:
1. Act 15 (opens img25R, 11 Feb 1853, Raffaele Arricale, son of Carmine Arricale 30 contadino and Pasqua Rivetti, strada Santa Lucia): margin on img26L "A 18 Luglio 1880 l'uff. dello stato civ. d'Arienzo pose Raffaele Arricale con Costanza FALCO; Caserta 27 Agosto 1881". (Candidate link: Costanza Falco b. 15 Aug 1855, daughter of Angelo Falco -- see 1855 act 69; not asserted.)
2. Act 16 (img26R, 11 Feb 1853, Maria Costanza Zimbardo, daughter of Aniello Zimbardo 40 bracciale and Elisabetta Laudato, strada Croce): margin on img27L "A 3 Luglio 1876 ... pose Maria Costanza Zimbardo con Giovan Battista FALCO; Caserta 5 Giugno 1884".
3. Act 56 (img67R, 29 Jun 1853, Angelo Raffaele Faccia, son of Domenico Faccia 36 contadino and Rosa Dato, strada Porta di sopra): margin on img68L "A 3 Marzo 1875 ... pose Angelo Raffaele Faccia con Andreana FALCO; Caserta 2 Agosto 1884". Note the act 56 row in the TSV sits on image 66; the margin is on image 67L. (Candidates: Andreana Falco b. 1854 act 24 or b. 1855 act 10 -- not asserted.)
4. Act 108 (opens img121R, 25 Dec 1853, Giuseppe Natale Ferriello, son of Michele Ferriello 42 sartore and Mariangela Daddio 30, strada Santa Lucia): WITNESS on img122L "Crescenzo FALCO di anni trentadue, di professione contadino, domiciliato [in] strada Camellara" with Gennaro Morgillo (45, contadino, strada Croce). Letters Falco confirmed by magnifying the word at 2x on the 3300 px render: F-a-l-c-o, no i between the C and o... (ligature test: five letters). Declarant Rosa Balletta. Margins: Ferriello m. Emilia Filomena Rivetti 28 Sep 1876; m.(2) Marianna Palazzo 12 Jan 1893.
Near-misses checked and rejected: none outstanding.

## What is proven
- All 110 acts were seen (opened, numbered 1..110 without gap). No Falco appears as child/parent/declarant/midwife in any of them (tavola F slot empty, and every act row read).
- Limitation: the transcription of ~8 acts is "poor" (surnames of parents partly unsure); 83 "fair" means readable at 2200 px but several given names/ages carry a "?" in the TSV. Child names for a few acts (e.g. act 2 male, parents Fabrizio Cimmino and Grazia Diglio) were not read. Because only the RIGHT-page header and the next LEFT-page margins/witnesses were transcribed, a Falco witness on an act whose left page was not studied at 3300 px could be missed; every left page was viewed at 2200 px and Falco was looked for.
