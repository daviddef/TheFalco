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

**~24 acts read, January to mid-April 1835. No Falco of any age.**

## Notes that change the estimate

- **The register is bound in duplicate.** Page 10 repeats page 9's two acts. If that holds throughout,
  the 46 images carry roughly **46 unique acts**, not 90 — so 1835 is about **half the work**
  originally estimated. Worth confirming as the sweep continues.
- Arienzo's death rate in early 1835 is heavily weighted to infants; adult deaths are the minority,
  which makes scanning faster than the act count suggests.

## Resume here

**Next page: index 14.** Continue to index 45. Then 1836 (`an_ua14338`), 1834 (`an_ua14336`),
1837 (`an_ua14339`), working outward from 1835.

Full year list: 1829 `an_ua14331` · 1830 `14332` · 1831 `14333` · 1832 `14334` · 1833 `14335` ·
1834 `14336` · **1835 `14337`** · 1836 `14338` · 1837 `14339` · 1838 `14340` · then 14341–14345 to 1843.
