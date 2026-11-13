# Menu regroup, PR A: reach proof

Compared: the build of `main` (the kit pin PR, 714b2c3) against the build of this change, built the same way.

## Counts

| menu | entries before | entries after |
|---|---:|---:|
| Start | 11 | 3 |
| Our line | 3 | 3 |
| The families | 16 | – |
| People & places | 14 | – |
| The name | 4 | 4 |
| Research | 18 | 19 |
| People | – | 11 |
| Places & families | – | 21 |
| **all menus** | 66 | 61 |

Entries are counted as the header draws them (a group heading counts as an entry). The one address that left every menu in the count is none: see `menu-a-moves.md` (What's new left Start and is the What's new group head of Research).

## The /families/ index, read from the build

The page body (`<main>`) of `/families/` links these family addresses, in this order: `/families/crisci/`, `/families/morgillo/`, `/families/rivetti/`, `/families/zampiello/`, `/families/annecchino/`, `/families/guida/`, `/families/quotolo/`, `/families/maione/`, `/families/arricale/`, `/families/esposito/`, `/families/vigliotta/`, `/families/carfora/`, `/families/cioffi/`, `/families/diglio/`, `/families/zimbardo/`, `/families/biondo/`, `/families/cimmino/`.

## Each family entry of the old menu

| menu address | label | in the new menu | linked from the /families/ index (same address) | verdict |
|---|---|---|---|---|
| `/wider-family/` | The Wider Family | yes | no | stays in the menu (a hub, not a family page) |
| `/zampiello/` | Zampiello | yes | no | stays in the menu — **needs index fix** (the index does not link this address) |
| `/annecchino/` | Annecchino | yes | no | stays in the menu — **needs index fix** (the index does not link this address) |
| `/maione/` | Maione | yes | no | stays in the menu — **needs index fix** (the index does not link this address) |
| `/ferrara/` | Ferrara | yes | no | stays in the menu — **needs index fix** (the index does not link this address) |
| `/morgillo/` | Morgillo | yes | no | stays in the menu — **needs index fix** (the index does not link this address) |
| `/carfora/` | Carfora | yes | no | stays in the menu — **needs index fix** (the index does not link this address) |
| `/crisci/` | Crisci | yes | no | stays in the menu — **needs index fix** (the index does not link this address) |
| `/rivetti/` | Rivetti | yes | no | stays in the menu — **needs index fix** (the index does not link this address) |
| `/families/cioffi/` | Cioffi | yes | yes | stays in the menu |
| `/families/diglio/` | Diglio | no | yes | left the menu: reachable from the index |
| `/families/zimbardo/` | Zimbardo | no | yes | left the menu: reachable from the index |
| `/families/biondo/` | Biondo | no | yes | left the menu: reachable from the index |
| `/families/cimmino/` | Cimmino | no | yes | left the menu: reachable from the index |
| `/liguori/` | The Bishop | yes | no | stays in the menu — **needs index fix** (the index does not link this address) |

## Kept in the menu and listed as needing an index fix

- `/zampiello/` (Zampiello)
- `/annecchino/` (Annecchino)
- `/maione/` (Maione)
- `/ferrara/` (Ferrara)
- `/morgillo/` (Morgillo)
- `/carfora/` (Carfora)
- `/crisci/` (Crisci)
- `/rivetti/` (Rivetti)
- `/liguori/` (The Bishop)

**Seven families have two pages with one title.** `/annecchino/`, `/morgillo/`, `/crisci/`, `/rivetti/`, `/zampiello/`, `/maione/` and `/carfora/` (the addresses the menu has always used, each its own canonical page) are not the same page as `/families/<name>/` (the addresses the index links); the two differ in size and content in the build. So the index does not reach the page the menu offers, and a menu entry may leave only where the index links that same address. Four of the nine stay as the four largest (Morgillo, Cioffi, Annecchino, Crisci; Cioffi's menu address is the index's own); the rest stay for the same reason. Which page of each pair is the family page is a decision for a later change (an index edit or a merge); this change touches neither.

## Order of the index, reported

The index lists the families in this order: Crisci, Morgillo, Rivetti, Zampiello, Annecchino, Guida, Quotolo, Maione, Arricale, Esposito, Vigliotta, Carfora, Cioffi, Diglio, Zimbardo, Biondo, Cimmino. That is not A to Z; the menu is, as the rule says. No index edit is made here.

