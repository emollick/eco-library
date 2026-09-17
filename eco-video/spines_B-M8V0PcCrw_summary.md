# Spine-reading summary — B-M8V0PcCrw ("Umberto Eco, Sulla memoria", part 3)

Source: `/mnt/project-files/eco-video/frames/B-M8V0PcCrw/` (KEEP.csv, 172 kept frames,
854x480 source resolution — the best stream this upload offered).
Output: `spines_B-M8V0PcCrw.jsonl` (39 frame entries with visible shelves/books),
`skipped_B-M8V0PcCrw.csv` (133 frames with no legible shelf).

## Frames read

All 172 kept frames were opened in timestamp order. 39 show a shelf, glass cabinet,
or a book close enough to log; 133 are talking-head interview shots, black/dark
transition frames, title/chapter cards, camera-crew shots, or cutaway film-clip
inserts (from *Häxan*, B. Christensen 1922, and *The Kid*, C. Chaplin 1921) with no
shelf content, and are listed in `skipped_B-M8V0PcCrw.csv` with a reason each.

The film is mostly a seated interview (Eco talking about memory, lists, and his
father) shot with a shallow depth of field — a glass curio cabinet is visible
behind him throughout but is always out of focus. The corridor-of-shelves walk the
brief promised happens near the end, roughly **t=5:08–6:14** (`t_000508.jpg` through
`t_000614.jpg`): Eco gets up, walks down a long white-shelved corridor lined
floor-to-ceiling with books, passes a gallery wall of framed prints, and ends in a
second book-lined study/office room where he pulls one volume down and leafs
through it before the credits (clip attributions confirm *Häxan* / *The Kid* as the
two archival inserts).

## Titles recovered, by confidence

- **High confidence (title/author both clearly legible): 3 distinct titles**
  - *Inventing an Enemy* — Umberto Eco (English) — t=0:24
  - *Имя розы* (The Name of the Rose) — Умберто Эко / Umberto Eco (Russian) — t=0:34, repeated t=0:36
  - *Italia Vostra* (Italian) — t=4:46
- **Medium confidence (partial letters + recognisable phrasing): 1 title**
  - *Une image peut en cacher une autre* (French) — t=0:34 — spine reads "UNE IMAGE PEUT EN..."; matched to
    the 2009 Grand Palais exhibition catalogue on that theme by partial text.
- **Low confidence: 0**

All four titled books above come from **coffee-table/hand-held close-ups early in
the video** (t=0:24–4:46), not from the corridor shelves.

The 34 frames covering the actual corridor-and-office shelf walk (t=5:08–6:14) all
carry visible, in-scene bookshelves, but **no spine text is legible on any of
them** — confirmed by cropping 2–4 overlapping tiles per frame, upscaling 2x (and
4x on one test crop, `t_000614.jpg`) with PIL/LANCZOS, and inspecting each tile.
The camera is handheld and walking continuously, the room is dimly lit, and the
854x480 source (the best stream `process_video.py` could obtain for this upload)
does not hold enough real detail for the upscale to recover — motion blur plus
JPEG/resolution limits, not a cropping problem. Those 34 entries in the JSONL
record an approximate visible-spine count per frame as `{"unlabelled": true,
"count": N}` rather than inventing titles. One further frame, `s_000315_92.jpg`
(t=3:16), shows a glass cabinet with two large illuminated-manuscript facsimiles
displayed open on stands — visually distinctive but not spine-labelled and not
title-legible either.

## 5 example titles with timestamps

| Title | Language | Timestamp | Frame |
|---|---|---|---|
| Inventing an Enemy — Umberto Eco | en | 00:00:24 | `t_000024.jpg` |
| Имя розы (The Name of the Rose) — Umberto Eco | ru | 00:00:34 | `t_000034.jpg` |
| Имя розы (The Name of the Rose) — Umberto Eco (same book, second frame) | ru | 00:00:36 | `t_000036.jpg` |
| Une image peut en cacher une autre | fr | 00:00:34 | `t_000034.jpg` |
| Italia Vostra | it | 00:04:46 | `t_000446.jpg` |

## Frame with the clearest legible spines

`/mnt/project-files/eco-video/frames/B-M8V0PcCrw/t_000034.jpg` — coffee-table
close-up showing the Russian edition of *Il nome della rosa* resting on a French
paperback, both spines readable without tiling.

## Totals

- Kept frames read: **172 / 172**
- Frames logged with shelves/books (JSONL entries): **39**
- Frames skipped (no legible shelf): **133**
- Distinct titled books recovered: **4** (3 high confidence, 1 medium confidence, 0 low)
- Frames with shelves visible but text illegible even after tiling/upscaling: **35**
  (34 corridor/office walk frames + 1 glass-cabinet manuscript-display frame)
