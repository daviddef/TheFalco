# Audit of every image and scan in the archive — 8 September 2026

Prompted by a reader's question: *"can you make sure your documents have been looked at
properly, and all images/scans have been correctly reviewed?"* The answer was no. Every
photograph plate had been captioned from its **filename**, not from the image. This is the
full result, kept because the errors are instructive.

## What was wrong

| File | Was captioned | What it actually is |
|---|---|---|
| `4503276_Angelo-Zampiello-portrait-b.jpg` | "A second portrait." | **The Croce al Merito di Guerra certificate**, Ministero dell'Africa Italiana, 1938 — the proof of a claim the site was calling *uncorroborated* |
| `4503277_Angelo-Zampiello-portrait-a.jpg` | "Angelo Zampiello, 1895–1972… served in the Second Italo-Abyssinian War" | The **reverse** of a document, inscribed *"li 14 Dicembre 1948 — Giordano Angelo"* |
| `4503258_Giuseppa-Ferrara-portrait.jpg` | "Giuseppa Ferrara, wife of Angelo Zampiello" | **Francesca Zampiello's birth extract**, Comune di Arpaia, atto n. 20 |
| `4503259_Francesca-Zampiello-and-Carmine-marriage.jpg` | "Married at Benevento in 1955" | **Marriage extract, Comune di ARPAIA, atto n. 1, 15 January 1955** — right year, wrong town |
| `4000088_Angelo-Zampiello-d.jpg` | "From the family's own scans." | Angelo Zampiello's **memorial card**, giving 31 Aug 1895 – 25 Apr 1972. Was also lying on its side |
| `4000090` and `4000095` | two different couples | **The same photograph**, filed twice under two different names |
| `4500840`, `4000037`, `4500702` | portraits / "a group photograph" | **Modern colour photographs of living people** — published in breach of this archive's own stated policy |

## What was done
- The three photographs of living people were **removed from the published build** and moved to
  `photos/withheld-living/`, which is not deployed.
- The duplicate was delisted and the surviving copy captioned honestly as an unidentified couple.
- The memorial card was rotated upright.
- The four documents were reclassified from *photo* to *register* and given real transcriptions
  and citations.

## What it changed in the record
1. **Angelo Zampiello's war service is corroborated.** See `notes/zampiello-war-cross.md`.
2. **Tommaso Zampiello** enters the archive — Angelo's father, named on the certificate.
3. **Francesca Zampiello's birth is documented**, not merely family-reported: 27 April 1928 at
   Arpaia, daughter of Angelo Zampiello and Giuseppa Ferrara.
4. **The marriage was at Arpaia, not Benevento**, on 15 January 1955.

## The lesson, recorded so it is not repeated
Filenames are not evidence. Every image must be opened and read before it is described, and a
thumbnail is not enough — the marriage date was very nearly published as *15 April 1957* from a
contact sheet, and reads *15 01 1955* when actually enlarged.
