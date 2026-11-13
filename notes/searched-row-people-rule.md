# Who a found row is for (rule from 15 Nov 2026)

What's new now says WHO each found row in `site/src/data/searched.json` is for. `docs/row-pages.json` carries
`"peopleFrom": "2026-11-15"`, and from that `searchedOn` day the kit's `check:row-pages` gate refuses a row that reads as
found unless it carries exactly one of:

- `"for": [["/person/slug/", "Name"], ...]` — each path a BUILT page of this archive that is that person's own page,
  the name that page uses, a page once per row, only people the finding is really about; or
- `"nobody": true` — the pages were read and no new person came out. The reason goes in `what`.

Never both. Nothing about the people goes to the Record Atlas (receipts hold only the row key).

**How to apply here**
- A walk batch with «no Falco» or only unplaced sightings is `"nobody": true`.
- A batch that adds or upgrades a person in `data/households.tsv` lists that person's page in `for`.
- Living people: only people this archive already publishes can be listed; never add a page or name for a living
  person to satisfy the gate (see `living-people-rule`).
- Old rows are not backfilled, and no existing row is edited to add the field (editing a row changes its Atlas key).
  A long-running walk row that is extended in place is an existing row; start a new row for new work from 15 Nov.
