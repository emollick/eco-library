# Spine-reading summary — zZEy10fpq3I, part 2 (timestamp_seconds 1200–1799)

## Coverage
- Slice size: 234 kept frames (`timestamp_seconds` in [1200, 1800)) from `KEEP.csv`.
- All 234 frames were visually triaged in timestamp order (via tiled contact sheets covering every frame in the slice, cross-checked against the Italian captions for room/subject context), then candidate shelf frames were opened individually and cropped/upscaled 2x with PIL for close reading.
- Frames with books: **7** (all written to `spines_zZEy10fpq3I_part2.jsonl`).
- Frames with no legible books: **227** (written to `skipped_zZEy10fpq3I_part2.csv`).
- 7 + 227 = 234 ✓.

## Why this segment is sparse
Unlike a segment shot continuously inside Eco's apartment, timestamps 1200–1800 of this documentary are dominated by: talking-head interview footage (podium, TV studio, outdoor, armchair, panel discussion), archival illustrations (Athanasius Kircher engravings, Sephirotic-tree diagrams, reproduced book covers/title pages), a dramatized reading of the 1714 book *Le Chef-d'œuvre d'un Inconnu*, and B-roll of at least two different **institutional/historical libraries** (a grand ornate reading room with galleries and frescoed ceilings, a corridor of stacks, and a dark industrial compactus archive) used to illustrate the narration. Where shelves do appear in the background of interview shots they are consistently out of focus/too distant, and where shelves appear in wide establishing shots the spines are uniformly worn/aged with no legible letterforms (verified by cropping and 2x upscaling representative frames before deciding to skip a whole run). Captions in this window cover: Kircher's encyclopedism (~1217–1252), memory/Borges' "Funes el memorioso" and digital-era information overload (~1260–1520), and Themiseul de Saint-Hyacinthe's *Le Chef-d'œuvre d'un Inconnu* (~1622–1806+).

## Distinct titles by confidence
- **High confidence (8 titles):** the eight legible volumes of *Aufstieg und Niedergang der römischen Welt* (ANRW), Teil II: Principat — Bd. 11.1, 12.1, 12.2, 12.3, 13, 14, 15, 16.1 — all German, all read from `t_002100.jpg`.
- **Medium confidence (1):** the ANRW Tafeln/index volume on the same shelf (partly cropped at the frame edge).
- **Low confidence / unlabelled (2 rows, ~38 physical volumes):** a numbered leather-bound set behind an archival TV-interview subject (`s_002649_25.jpg`, numbers ~9–18 legible, titles not) and a very long numbered wall of leather volumes behind a presenter on a library ladder (`t_002658.jpg`, numbers 59–69 then 1–9+ legible, titles not). Both recorded as `unlabelled: true` per the no-invention rule.

## Rooms / walls labelled, with time ranges
- `unknown` — `anrw-reference-shelf` ("Shelf of the ANRW classics reference set"): 1260s–1268s (`t_002100.jpg`–`t_002108.jpg`). Macro close-up shelf of a German classics reference series; could not confidently place it inside Eco's apartment versus another library used as B-roll for the Kircher segment.
- `study` — `hora-clave-interview-shelf`: 1609s (`s_002649_25.jpg`). Dark-wood shelf visible behind an armchair in archival "Hora Clave 9" TV-interview footage; plausibly Eco's own study but not confirmed.
- `other` — `library-ladder-wall-of-volumes`: 1618s (`t_002658.jpg`). Wood-panelled wall of uniform bound volumes in a dramatized re-enactment scene (actor on a ladder), clearly a different, ornate historical library, not Eco's apartment.
- No `corridor`, `rare`, `living`, or `piano` rooms were identifiable with legible books in this slice.

## Five example titles with timestamps
1. *Aufstieg und Niedergang der römischen Welt*, II. Principat, Bd. 11.1 — `t_002100.jpg`, 00:21:00 (1260s)
2. *Aufstieg und Niedergang der römischen Welt*, II. Principat, Bd. 12.1 — `t_002100.jpg`, 00:21:00 (1260s)
3. *Aufstieg und Niedergang der römischen Welt*, II. Principat, Bd. 13 — `t_002100.jpg`, 00:21:00 (1260s)
4. *Aufstieg und Niedergang der römischen Welt*, II. Principat, Bd. 15 — `t_002100.jpg`, 00:21:00 (1260s)
5. *Aufstieg und Niedergang der römischen Welt*, II. Principat, Bd. 16.1 — `t_002100.jpg`, 00:21:00 (1260s)

## Frame where spines are clearly legible
`/mnt/project-files/eco-video/frames/zZEy10fpq3I/t_002100.jpg` (timestamp 1260s / 00:21:00) — macro close-up of the ANRW shelf; all 8 volume spines are sharply legible without cropping.

## Totals
- Frames read/triaged: 234
- Frames with books recorded: 7
- Frames skipped (no legible books): 227
- Distinct high-confidence titles: 8
- Distinct medium-confidence titles: 1
- Unlabelled/low-confidence groups: 2 (≈38 volumes)
