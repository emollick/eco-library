# Spine-reading summary — zZEy10fpq3I, part 6 (t=3600s–4199s, i.e. 01:00:00–01:09:59)

## Frames read
- **269 kept frames** in this slice (`timestamp_seconds` 3600–4199) were reviewed, in timestamp order, from `KEEP.csv`.
- **6 frames** contained legible book text and were written to `spines_zZEy10fpq3I_part6.jsonl` (2 more frames are near-duplicates of these and were logged to the skipped CSV with a `same shelf/cover, no new spines` reason instead of being repeated in the JSONL, per the de-duplication rule).
- **263 frames** had no legible book text and were logged to `skipped_zZEy10fpq3I_part6.csv`.

## Why this segment is so sparse
This ~10-minute stretch of the documentary is almost entirely **B-roll and archival footage**, not shots inside Eco's Milan apartment:
- an animated cartoon dramatizing the Shakespeare/Bacon authorship dispute,
- wide architectural shots of the **Biblioteca Vasconcelos** in Mexico City (its shelves are visible but the paperback spines are far too small/blurred to read even at 2x zoom),
- 19th-century engravings and incunabula page close-ups (Nuremberg-Chronicle-style Latin text, a Monte Cristo illustration, a Freemasonry frontispiece),
- archival talking-head interview footage of Eco on a bare stage/brick-wall set,
- a Leonardo da Vinci "Last Supper" fresco sequence,
- a stylised cinematic re-enactment of a woman in a trench coat, and
- a handful of shots of Eco seated in his apartment study (red leather armchair, glass display case of illuminated manuscripts/objets, blurred wood shelving) where the background is always out of focus.
No genuine shelf-full-of-spines shot from Eco's library appears in this window with legible text, apart from one archival insert (see below).

## What was found, by confidence
- **High confidence (5 titles):**
  - *Francis Bacon: Concealed and Revealed* — Theobald (en) — archival shelf insert
  - *Trattato di semiotica generale* — Umberto Eco (it) — book-cover insert
  - *Il cimitero di Praga* — Umberto Eco (it) — book-cover insert
  - *The Plot: The Secret Story of the Protocols of the Elders of Zion* — Will Eisner, intro by Umberto Eco (en) — book-cover insert
  - *Il pendolo di Foucault* — Umberto Eco (it) — book-cover insert
- **Medium confidence (1 title):** *Shakespeare's Beehive* (en) — partial gilt spine lettering "...ake- ...re's ...hive", same archival shelf insert as the Bacon book
- **Low confidence (2 items):** an unidentified "BACON-S..." gilt spine (right edge of the same archival shelf insert, en); an endpaper/ex-libris page reading "dagli scritti di Umberto Eco" with an "Ex libris Umberto Eco" bookplate — unclear if this is a formal book title (it)

## Rooms / walls labelled and their time ranges
None of the legible-text frames are inside an identifiable room of Eco's apartment — all 6 are non-apartment inserts, so every entry uses `room_id: "other"`:
- `archival-shakespeare-bacon-shelf` — 01:00:07 (single frame, archival footage)
- `insert-trattato-semiotica` — 01:02:48 (book-cover cutaway)
- `insert-cimitero-praga` — 01:04:28 (book-cover cutaway)
- `insert-the-plot-eisner` — 01:05:38 (book-cover cutaway)
- `insert-pendolo-foucault` — 01:05:57 (book-cover cutaway)
- `insert-exlibris-scritti` — 01:07:36 (endpaper/bookplate cutaway)

Eco does appear seated in his actual apartment study (glass display case of manuscripts, red armchair) intermittently across roughly 01:02:20–01:02:34, 01:04:05–01:04:20, and 01:05:49–01:06:12, but the shelving behind him stays out of focus throughout, so no `room_id` other than "other" could be assigned in this slice.

## Five example titles with timestamps
1. *Francis Bacon: Concealed and Revealed* (Theobald) — 01:00:07 — `s_010007_04.jpg`
2. *Trattato di semiotica generale* (Umberto Eco) — 01:02:48 — `t_010248.jpg`
3. *Il cimitero di Praga* (Umberto Eco) — 01:04:28 — `t_010428.jpg`
4. *The Plot* (Will Eisner, intro Umberto Eco) — 01:05:38 — `t_010538.jpg`
5. *Il pendolo di Foucault* (Umberto Eco) — 01:05:57 — `s_010557_21.jpg`

## Frame with clearly legible spines
`/mnt/project-files/eco-video/frames/zZEy10fpq3I/s_010007_04.jpg` (t = 01:00:07) — a sharp, well-lit close-up of two-and-a-bit book spines, with "FRANCIS BACON: CONCEALED AND REVEALED — THEOBALD" fully legible on the center book's front cover and "Shake-...re's ...hive" legible in gilt lettering on the spine to its left.

## Totals
- Frames read: **269**
- Frames with books written to JSONL: **6** (2 additional near-duplicate frames cross-referenced via `same_as_frame` reasoning, logged as skipped)
- Frames skipped (no books): **263**
- Distinct titles: 5 high-confidence, 1 medium-confidence, 2 low-confidence/unlabelled items
