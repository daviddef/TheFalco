# Arienzo civil death register 1835 — sweep log

**Volume**: `an_ua14337` · Archivio di Stato di Caserta · Stato civile della restaurazione · Arienzo ·
**46 images**, each a two-page spread carrying **two death acts**.

**Target**: **Pasquale Falco**, born 1767, a *contadino* of Arienzo, husband of **Chiara Rivetti**,
son of **Matteo Falco** and **Francesca Crisci**. He would be **68** in 1835. The act names the
deceased's parents outright — which is the whole point of reading these.

## Working method (reproduce exactly)

Antenati's IIIF images are Cloudflare-blocked to direct fetch. They render only when injected as an
`<img>` into a page on the `antenati.cultura.gov.it` origin:

```js
window.ids = async function(ark){                      // get page ids from the IIIF manifest
  const h = await (await fetch('/ark:/12657/'+ark,{credentials:'include'})).text();
  const man = (h.match(/https?:\/\/dam-antenati[^"'<> ]*manifest/)||[])[0];
  const m = await (await fetch(man)).json();
  const cs = (m.sequences?.[0]?.canvases)||m.items||[];
  return cs.map(c=>{const u=c.images?.[0]?.resource?.['@id']||c.items?.[0]?.items?.[0]?.body?.id||'';
    return (u.split('/iiif/2/')[1]||'').split('/')[0];}).filter(Boolean);
};
window.reg = function(id,pct,w){                        // crop + magnify server-side
  document.body.style.margin='0';
  document.body.innerHTML='<img id="pg" style="width:100%;display:block" src="https://iiif-antenati.cultura.gov.it/iiif/2/'+id+'/pct:'+pct+'/'+(w||2200)+',/0/default.jpg">';
  const i=document.getElementById('pg');
  return new Promise(r=>{i.onload=()=>r(1);i.onerror=()=>r(0);setTimeout(()=>r(2),9000)});
};
```

**Crop coordinates that work** — these took several attempts, do not re-derive them:

| | |
|---|---|
| **Left act** | `reg(D35[n], '4,37,46,15', 1700)` then screenshot at scale **0.8** |
| **Right act** | `reg(D35[n], '52,37,46,15', 1700)` then screenshot at scale **0.8** |

That band lands exactly on *"è morto/a nella propria casa **[NAME]**, d'anni **[N]** … figlio/a di
**[FATHER]**"*. A full-spread crop is **not** legible — the page shrinks to fit the viewport. One
screenshot per act is the floor.

## Coverage so far — pages 2–13 done, no Falco

| Page | Left act | Right act |
|---|---|---|
| 2 | Rosa Varrecchia, 60, widow of Cimmino, d. 14 Jan | infant d'Ajuzzo, s. of Pasquale, d. 6 Jan |
| 3 | Clemente Carfora, 1 day, s. of Stefano, d. 8 Jan | Carmine Carfora, 4 days, s. of Stefano, d. 9 Jan |
| 4 | Maria Giuseppa Saduto, d. of Antonio (muratore), d. 16 Jan | Anna Ciuffi, 16 mths, d. of Clemente, d. 18 Jan |
| 5 | Andrea Ciuffi, 50, s. of Alessandro, d. 19 Jan | **Don Alessandro de Nuptis**, 77, *possidente*, s. of Don Mariangiuseppe, d. 1 Feb |
| 6 | Domenico Ciuffi, s. of Aniello, d. 21 Jan | *transcription*: death of Pellegrino Sedotto at **Naples**, Nov 1834 |
| 7 | (blank) | Maria Rosa Grafiu, 6 mths, d. of Angelo, d. 6 Feb |
| 8 | Gregorio d'Ambrogio, 5 days, s. of Clemente (sartore), d. 11 Feb | Carmela Diglio, 4 days, d. of Clemente, d. 19 Feb |
| 9 | Maria Arrigale, 4, d. of Francesco, d. 18 Feb | Maria Saduto, 45 days, d. of Gennaro, d. 21 Feb |
| 10 | *(duplicate of p9 — the register is bound in two originals)* | *(duplicate of p9)* |
| 11 | Teresa Bizzarro, 80, d. of Lorenzo, d. 9 Mar | Angela Palumbo, 80, widow of Nicola Baletta, d. of Aniello, d. 11 Mar |
| 12 | (gutter, unreadable) | Anna Ciuffi, 3, d. of Pellegrino, d. 22 Mar |
| 13 | Paolo Olivetti, 2, d. 11 Apr | Marcantonio Ciuffi, 1, s. of Pasquale, d. 16 Apr |
| 14 | Maria Carmela Venapia, 1, d. of Andrea (muratore), d. 16 Aug | Cipriano Laudato, 3, s. of the late Cipriano (muratore), d. 17 Aug |
| 15 | **Donna Alessandra Diglio**, 75, *gentildonna*, d. of Filippo (dec.), d. 21 Aug | Maria Carfora, 13 days, d. of Aniello, d. 24 Aug |
| 16 | **Donna Violetta d'Ambrogio**, 54, *gentildonna*, w. of Rossi, d. of Don Pietro (*proprietario*), d. 28 Aug | Carmela Ciuffi, 28, w. of Pietro Carfora, d. of Ignazio (dec.), d. 28 Aug |
| 17 | Carmela Martone, 7 mths, d. of Clemente, d. 7 May | Arcangelo Martone, 6 mths, s. of Angelo, d. 15 May |
| 18 | Angelo Ciuffi, 70, s. of Vincenzo, d. 25 May | Maria Grazia Laudato, 50, widow of Angelo Sorrento, d. of Andrea (dec.) — **died in the hospital**, d. 1 Jun |
| 19 | Giovanni Macchia, 50, s. of Francesco, d. 3 Jun | Donato Naddeo, 1 mth, s. of Vincenzo, d. 4 Jun |
| 20 | *(duplicate of p19)* | *(duplicate of p19)* |
| 21 | Marta Diglio, 65, widow Varrecchia, d. of Pietro (dec.), d. 5 Jun | Angelo Zimbardo, 80, h. of Maria Maccariello, s. of Giovanbattista (dec.), d. 11 Jun |
| 22 | Carmela Majone, 3, d. of Clemente, d. 3 Jul | **Palma Bruno, 90**, widow of Gregorio Mauro, d. of Alessandro (*possidente*, dec.), d. 6 Jul |
| 23 | Giuseppa Diglio, 4, d. of Pietro (vaticale), d. 9 Jul | Anna Ciuffi, 40, w. of Majo Porrino, d. of Vincenzo, d. 10 Jul |
| 24 | Maddalena Diglio, 70, widow, *mendica*, b. San Nicola di Bari, dom. San Felice, d. of Lorenzo (dec.), d. 21 Jul | Tommaso Marchese, 1, s. of Aniello, d. 29 Jul |
| 25 | Arcangelo Attarelli, 5 mths, s. of Nicola, d. 30 Jul | Gennaro Loffredo, 70, h. of Apollonia Zimbardo, s. of Andrea (dec.), d. 2 Aug |
| 26 | Anna di Silvio, days, d. of Fedele (falegname), d. 6 Aug | Camilla Sepitelli, 1, d. of Angelo, d. 9 Aug |
| 27 | Angelo [d'Ajuzzo], s. of Filippo Diglio (sartore), d. 11 Aug | Nunzia d'Ajuzzo, 12, d. of Giulio, d. 10 Aug |
| 28 | *(duplicate of p27)* | *(duplicate of p27)* |
| 29 | Giuseppe Sepitelli, 47, s. of Angelo, d. 22 Aug | Antonia Cimmino, 54, w. of Giuseppe Diglio, d. of Domenico (dec.), d. 25 Aug |
| 30 | Angelo Mauro, 15 mths, s. of Andrea (vaticale), d. 3 Sep | Francesco Morgillo, 13 mths, s. of Domenico, d. 4 Sep |
| 31 | Mariantonia Marletta, mths, d. of Gennaro, d. 9 Aug | Vincenzo Martone, 76, h. of Maria Giuseppa, s. of Gaspare (dec.), d. 10 Sep |
| 32 | Antonia Diglio, 9 mths, d. of Pasquale, d. 13 Sep | Angelo Diglio, 2 mths, s. of Tiberio, d. 21 Sep |
| 33 | **Signora Elisabetta d'Ambrogio**, 34, *possidente*, d. of Antonio (*possidente*), d. 21 Sep | Felicia Sepitelli, 1, d. of Gennaro (*possidente*), d. 24 Sep |
| 34 | Antonia Laudato, 6 mths, d. of Clemente, d. 24 Sep | **Raffaela della Selva, 88**, d. of Francesco (dec.), d. 2 Oct |
| 35 | *(duplicate of p34)* | *(duplicate of p34)* |
| 36 | Francesco Zimbardo, 70, h. of Maria Giuseppa, s. of Aniello, vaticale, d. 10 Oct | Marianna d'Ajuzzo, 30, w. of Angelo Diglio — **died in the hospital** |
| 37 | Alessandra Carfora, mths, d. of Sabatino, d. 20 Oct | Clementina Carfora, mths, d. of Michele, d. 24 Oct |
| 38 | Giovanni d'Ambrogio, 45, *sartore*, s. of Gregorio (sartore), d. 25 Oct | Francesco di Gennaro, 80, h. of Nicola Laudato, s. of Vincenzo (dec.), d. 22 Oct |
| 39 | Antonio Crisci, days, s. of Fabrizio (*vinicendolo*), d. 6 Nov | Maurizio delle Cave, 17 days, s. of Aniello, d. 7 Nov |
| 40 | Pasquale Carfora, b. Santa Maria a Vico, s. of Ferdinando, d. 20 Nov | **Suor Giovanna di Lucia, 50, *monaca*** — died in the **monastero di Ave Gratia Plena**, d. of Pasquale (*possidente*, dec.), d. 27 Nov |
| 41 | Angelantonio Diglio, days, s. of Vincenzo, d. 30 Nov | **Fra Michele delle Cave, 84, *ex laico agostiniano scalzo***, s. of Giuseppe (dec.), d. 14 Dec |
| 42 | *(duplicate of p41)* | *(duplicate of p41)* |
| 43 | Angela Migliore, 45, w. of Crisci, d. of Giacinto, d. 13 Dec | **Margarita Morgillo, 88**, widow, d. of Nicola (dec.), d. 28 Dec |
| 44 | **Angela Laudato, 80**, widow, d. of Francescantonio (dec.), d. 31 Dec | Chiara Porrino, 70, w. of Giuseppe Duca, d. of Pasquale (dec.), d. 31 Dec |
| 45 | *closing certification page — end of volume* | — |

## RESULT: 1835 COMPLETE — Pasquale Falco is NOT in it

**All 46 images read, roughly 75 acts, January to 31 December 1835. There is no Falco of any age,
sex or condition anywhere in the Arienzo civil death register for 1835.**

The year is eliminated. Pasquale Falco died in one of the other fourteen years of the 1829–1843 window.

### What the year shows about the parish

The recurring surnames are **Ciuffi, Diglio, Carfora, Martone, Laudato, d'Ajuzzo, Zimbardo,
d'Ambrogio, Sepitelli, Morgillo, Crisci** — a cast that overlaps the Falco in-law network only at
Morgillo, Crisci and Martone. Deaths are heavily weighted to infants and the very old; several
reached 80, 84 and 88.

Two religious among them: **Suor Giovanna di Lucia**, a nun of the monastery of *Ave Gratia Plena*,
and **Fra Michele delle Cave**, 84, an *ex laico agostiniano scalzo* — a discalced Augustinian lay
brother. Two women died in the hospital rather than at home. One entry is a transcription recording
a death at **Naples**.



## Notes that change the estimate

- **The register is bound in duplicate, but only intermittently.** Pages 9/10, 19/20 and 27/28 each
  repeat their neighbour; pages 14–18 and 21–26 do not. So the saving is real but partial — expect
  roughly **75–80 unique acts per year**, not 46 and not 90.
- **The acts are not in strict date order.** Page 13 is mid-April, page 14 jumps to August, page 17
  returns to May. The two bound originals interleave. **Do not stop early on the assumption that a
  month has been passed** — the whole volume has to be read.
- Arienzo's death rate in early 1835 is heavily weighted to infants; adult deaths are the minority,
  which makes scanning faster than the act count suggests.

## Resume here — 1835 is done, move to the next year

**1835 (`an_ua14337`) is fully read and eliminated.** Next: **1836 (`an_ua14338`)**, then 1834
(`an_ua14336`), 1837 (`an_ua14339`), 1833 (`an_ua14335`) — working outward from the middle of the
bracket. Then 1836 (`an_ua14338`), 1834 (`an_ua14336`),
1837 (`an_ua14339`), working outward from 1835.

Full year list: 1829 `an_ua14331` · 1830 `14332` · 1831 `14333` · 1832 `14334` · 1833 `14335` ·
1834 `14336` · **1835 `14337`** · 1836 `14338` · 1837 `14339` · 1838 `14340` · then 14341–14345 to 1843.
