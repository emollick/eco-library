# The dense spine pass

A second, denser reading of the footage of Eco's Milan flat, made to identify more books on the
shelves than the first pass in `../books_by_wall_eco.json`. Everything this pass produced is in
this folder, except `../piano_piles.json` and `../piano_piles.jsonl` (the piles on the salotto
piano) and the eight `../spines_<video>_dense.jsonl` files through which the readings reach the
consolidation.

## How the readings were made

**Footage.** The 2022 film *Umberto Eco: la biblioteca del mondo* (YouTube `zZEy10fpq3I`) was cut
into 418 shots, and every shot was classified from a representative frame (shelf close, shelf
far, pile, book held up, rare-book cabinet, other library, nothing). Shots showing books were
re-cut at 5 fps, the sharpest frame of each second kept and near-duplicates dropped; a shot with
a single book or a blurred background gave one or two frames. The other seven videos (the Bologna
reopening, the askanews rare-book room, RAI and news clips, trailers, the Louisiana interview)
were re-read from every kept frame the first pass had skipped or read only in part.

**Reading.** Each frame was read whole and again in four overlapping 2x quadrants, with 3x ninths
for the densest shelves, contrast-stretched and sharpened. Every spine was transcribed as printed
(`spine_text`) before title, author, publisher, language and a reading confidence were recorded
(high = every word legible, medium = most letters, low = a fragment). Shelf-edge call tags
(Q4.9, L11.5, A 13 and the like) and printed subject tabs were recorded per frame.

**Placement.** A frame's books are placed by, in this order: a call tag in the frame; a call tag
within 12 s in the same shot; the first pass's wall label for that frame; the reader's room
guess. `placement_basis` on every frame and sighting says which applied. Tags map to the build's
bookcases as in `../layout.json`: Q4 to study-Q bay 4, L11 to study-L8-12 bay 11, A 13 to
corridor-13, B, C and D to the vestibule, E to the salotto, F, G and H to the art corridor.

**Matching.** Every reading was fuzzy-matched (rapidfuzz, token-set ratio, author-aware) against
the Braidense export, the Bologna export, the notable-books list and the first pass's readings.
`matched` gives the record, the score and the kind of match; `confirms_existing_reading` gives
the id of the first-pass book when the title was already read.

**Tiers.** `certain` means a full title legible and placed by a shelf tag, or a pile in view in a
known room. `probable` means a full title placed only by shot context or room, or a partial read
confirmed by a catalogue match on a known bookcase. `guess` means a fragment, or an unknown
bookcase. A name alone is never certain. Every book carries `tier_reason` in words.

**Timestamps.** `timestamp_s` is the true film second; the 0.96 s offset that `zZEy10fpq3I`
frame labels carry is already applied here, and `source_url` links to that second. The other
videos' frame times are true as they stand.

## Files

- `books_dense_eco.json`: 433 books, one record per distinct book per bookcase or room, each
  with title, author, language, publisher, `bookcase_id`, `room_id`, `bay`, `shelf_from_tag`,
  `pos`, `tier`, `tier_reason`, `best_confidence`, `matched`, `confirms_existing_reading` and
  every entry of `sightings[]` (frame, video, second, link, row, position, confidence, spine
  text). Ids are `video:<video>:<second>:<slug>`.
- `dense_frames_<video>.jsonl`: one line per frame read, in the shape of the parent folder's
  `spines_*.jsonl` files (view, shelf tags, rows of books left to right, unlabelled runs with
  counts) plus `bookcase_id`, `bay`, `placement_basis` and `tier` per book. The 359 spine
  fragments with neither a title nor an author are kept here only.
- `conflicts_resolution.json`: every pair of readings where the two passes read a different
  title at the same row and position of one frame, with the rule applied and the outcome. Pairs
  across two frames of a panning shot are listed but not resolved.
- `film_legibility.json`: per shot class: how many shots the film has, how many were read and
  how many yielded a title, with the shots that show shelves but never come into focus.
- `new_ids_for_descriptions.json`: the 171 book ids this pass added, for the description
  fetcher.
- `summary.json`: the counts below.

## Counts

Frames read: 1,127. Sightings: 1,447. Distinct books: 433.

| video | books |
|---|---|
| zZEy10fpq3I | 220 |
| KZfOaug0mM4 | 73 |
| ygvl-_gtAP8 | 44 |
| M8IWTOFNlOc | 30 |
| FeIUY9EhZgI | 22 |
| NtPk4irDiM8 | 18 |
| iRXEQVTI95k | 15 |
| bcK8rOkcb3k | 11 |

| tier | books |
|---|---|
| probable | 206 |
| guess | 158 |
| certain | 69 |

| best reading confidence | books |
|---|---|
| high | 236 |
| medium | 134 |
| low | 63 |

| against the first pass | books |
|---|---|
| confirms an existing reading | 245 |
| new | 188 |

| catalogue match | books |
|---|---|
| none | 286 |
| bologna | 60 |
| braidense | 50 |
| notable | 37 |

By bookcase (build ids; `room:<room>` means only the room is known):

| bookcase | books |
|---|---|
| room:studio | 114 |
| room:other | 52 |
| room:antichi | 44 |
| room:unknown | 41 |
| study-Q | 38 |
| study-L8-12 | 33 |
| room:bologna | 31 |
| room:salotto | 28 |
| vest-B | 13 |
| room:corridoio | 7 |
| study-M-A | 7 |
| corridor-10 | 7 |
| corridor-02 | 6 |
| corridor2-G | 5 |
| study-Oa | 4 |
| study-L1-4 | 3 |

The piano holds 12 piles, 6 on the lid and 6 on the keyboard shelf, with 118 items: 76 carry a
title or an author (26 certain, 24 probable, 26 guesses) and 42 are blank. Of those, 52 confirm
the first pass, 21 are new and 3 differ, both readings kept.

## What the footage does and does not show

- The film is mostly interviews, archive material and other libraries. Of its 418 shots, 188 show
  no books at all and 69 show libraries that are not Eco's flat (Braidense, Bologna, Tianjin, St
  Gallen, a baroque rotunda, a modern reading room). Books read in those shots are kept but carry
  `room_id` `other` or `bologna`, never a Milan bookcase.
- Shelves of the flat close enough to read: 11 shots, 9 of which yielded titles. The far shelf
  shots (39) are almost all blurred backgrounds behind an interviewee (Eco in the red armchair,
  44:17 to 50:59) and yielded titles in 10.
- The rare-book cabinets: 29 shots, 12 with titles (Kircher, Fludd, Böhme, Swedenborg, Wagenseil,
  Schott, Mabillon, Calmet, the Alessandria local history shelf).
- Books held up or open to the camera: 76 shots. Most are engravings and pages inside a book whose
  title is not shown; titles came from 38.
- Corridor A, the 25 bookcases of the long corridor, appears only in the black-and-white tracking
  shot and in the 43:10 to 44:07 pass, both in motion. Single spines there read only as publisher
  colours and a few surnames. The corridor cannot be read from this film.
- The photographs give layout, not titles. The Fondazione galleries are 650 px; the Zanni 2010
  photograph shows open books in vitrines; no photograph has a legible spine. The 2015
  walk-through exists only at 480p, and no spine in it is legible.
