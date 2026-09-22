# Rescoped out of the dataset — 2026-09-22

On 2026-09-22 the project owner narrowed the scope of this repository:

> "When I say coupons I mean products to purchase, not events and museums, etc."

The two shards in this folder were **verified work** (each line was read verbatim from the
issuer's official page on 2026-09-22 and carries full citations), but they list museum and
attraction **admission** programs, not product coupons. They are therefore removed from the
published dataset (`data/entries/`) and from the site build, and kept here so the evidence is
not lost and the decision is auditable.

| File | Contents | Why archived |
| --- | --- | --- |
| `07-museums-for-all-sf.json` | 26 SF Museums For All venue entries, transcribed from the SF Human Services Agency listing | Venue admission, not a product purchase |
| `08-bay-area-access-programs.json` | 23 Bay Area access-program entries (Exploratorium, CalAcademy-adjacent, library passes, transit, etc.) | Admission / benefit programs, not product coupons |

The `no-spend-free` and `community-access` taxonomy entries, the `free_admission` /
`reduced_admission` deal types and the admission value kinds were retired from
`data/meta.json` alongside these shards. The two museum-related records that survive in
`data/entries/10-excluded-unverified.json` stay there as rejection provenance, now also marked
out of scope.

To revive this material as a separate project (e.g. a free-attractions board), copy the shards
back into `data/entries/`, restore the taxonomy rows, and re-run
`python3 scripts/build_site.py`.
