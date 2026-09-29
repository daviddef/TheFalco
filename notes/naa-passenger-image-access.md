# Reading a NAA passenger list image

*Written 29 September 2026, after four failed routes to one page.*

## The index names the page

The Passenger arrivals index does not only cite an item. **Each row links to the image of
that passenger's own entry**, and the sequence number is in the link:

    /SearchNRetrieve/Interface/ViewImage.aspx?B=30139890&S=21
                                                         ^^^^ the page

`B` is the item barcode, `S` the image sequence. For NAA: K269 item 30139890 — the ss *Castel
Bianco*, Fremantle, 7 November 1956 — **Carmine Falco's entry is on page 21 of 29.**

This was in the page on 28 September and was missed, because the results table was read as
text and the link behind the row was never looked at. **A sweep of pages 14–29 was planned on
the strength of that.** Read the anchors, not the cells.

## The route that works

Everything else returns «Session expired» or an exception page:

| route | result |
|---|---|
| `ItemDetail.aspx?Barcode=…` direct | **Session expired**, always, live session or not |
| `ViewImage.aspx?B=…&S=…` direct | **Exception error**, always |
| `PassengerSearch.aspx` → *Search* → listing → `location.href` to the ViewImage link | **works** |

Within that route:

- The guest session is minted by the *search as a guest* link on the expired-session page, or
  simply by loading `BasicSearch.aspx` fresh.
- **Fill the form with the page's own controls.** Assigning `.value` in script and calling
  `.click()` on the button produced `Displaying 0 of 0` every time; driving the real inputs and
  the real button returned the two rows.
- **The viewer opens in a popup.** Clicking the link is blocked; assign `location.href` instead.
- Searching two fields at once is fine; adding **Item ID** to a surname returns nothing.

## Why the page is still not read

`/SearchNRetrieve/NAAMedia/ShowImage.aspx?B=30139890&S=21&T=P&R=0` returns

    HTTP 200 · Content-Type: image/jpeg · 4316 × 3070 · chunked, no Content-Length

and the body then **dies mid-stream at 1,590,848 bytes**, with

    net::ERR_QUIC_PROTOCOL_ERROR

repeatably, across three attempts and two tabs. A `T=T` thumbnail request is refused in 65 ms.

**This is an HTTP/3 transport failure, not an access restriction.** The National Archives sends
the image; the connection breaks. It must not be recorded as blocked, paywalled or restricted —
the item is Open and digitised and the server is serving it.

**The cut is at the same byte every time** — 1,590,848, across four attempts in three tabs. That
is not a flaky connection; it is a deterministic stop, and it looks like a proxy response cap
rather than anything the archive intends.

**AND THE PARTIAL FILE CANNOT BE SALVAGED, BECAUSE THE SCAN IS A PROGRESSIVE JPEG.** The truncated
bytes were streamed with `response.body.getReader()`, kept through the failure, closed with an
`FFD9` marker and handed to `createImageBitmap`. **It decodes — to the full 4316 × 3070 — and it is
blank grey.** *A baseline JPEG stores the image top to bottom, so three quarters of the file would
have been three quarters of the page; a progressive JPEG stores the whole page coarsely and then
refines it, so a truncated one carries a sliver of the top edge and nothing else.* Roughly fifty
pixels of three thousand survived.

**So partial delivery is worth nothing here, and the only thing that helps is a complete transfer.**

Other things learned, so they are not learned again:

- **One image request per session state.** After a stalled transfer the next request for the same
  image returns a 2,191-byte exception page. The search has to be redone from `PassengerSearch.aspx`.
- **The page's own CSP blocks every way of getting bytes out of the browser**: `connect-src 'self'`
  refuses a POST to `127.0.0.1`, and `default-src 'self'` refuses the hidden iframe a form would
  post into. A `blob:` download with `a.download` produced no file either.
- The obvious fix is a client that does not speak HTTP/3 — `curl` would do it — but the session
  cookie that matters is `HttpOnly` and cannot be read out of the browser. **Credentials and
  sessions are David's to hand over; nothing was taken from the browser to work around this.**

**WHAT WOULD ACTUALLY FINISH THIS.** Opening
`recordsearch.naa.gov.au` → *Passenger arrivals* → **FALCO / CARMINE** → the 1956 row's image link,
in an ordinary browser window, and reading page 21. *It is a few seconds of a person's time and an
unknown number of hours of this one's.*

## What the page can and cannot give

The form is a Commonwealth Department of Health quarantine passenger list. Its columns are

> No. · NAME · CLASS · PORT OF EMBARKATION · PORT OF INTENDED DEBARKATION ·
> ADDRESS AT DESTINATION IN AUSTRALIA

**There is no age column, so this document can never confirm a birth year.** What page 21 would
give is his **intended port** and his **Australian address** — which is what would tie the 1956
arrival to Brisbane, or break it.
