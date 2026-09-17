# Spine-reading summary — Hq66X9f-zgc ("Umberto Eco, Sulla memoria", part 1)

## Frames read

- **179 / 179** kept frames (per `KEEP.csv`) opened and reviewed in timestamp order, `t_000000.jpg` (0s) → `t_000648.jpg` (408s).
- **35** frames contain a bookshelf or a legible book and were written to `spines_Hq66X9f-zgc.jsonl` (34 `view:"shelves"` + 1 `view:"closeup"`).
- **144** frames had no shelves/books at all (talking-head interview coverage, black title cards/leader, or archival film inserts) and were logged to `skipped_Hq66X9f-zgc.csv` with a reason each.
- The video is a talking-head interview shot mostly in Eco's living room, cut with 1911/1924 archival film clips and 2015 Mosul-museum-destruction news footage as B-roll for the "Library" chapter. Eco only walks past his actual shelving late in the video, in one continuous tracking shot from **t≈296s to t≈362s** (`t_000454.jpg`–`t_000602.jpg`), matching the pipeline's own note (`notes.json`: "Corridor walk through the shelves at ~t=328–362s"). Italian auto-captions run under this stretch as instrumental music only (`[Musica]`), so captions gave no room names.

## Titles by confidence

| Confidence | Count | Note |
|---|---|---|
| high | 1 | Book cover + spine legible with author and title |
| medium | 1 | Distinctive partial title phrase legible |
| low | 0 | No guesses were made — see below |
| unlabelled (aggregate) | ~815 books across 34 shelf frames | Counted, not identified |

**No low-confidence guesses were recorded.** At this stream's native resolution (854×480, itag 135 — 1080p/720p were not offered for this upload per `notes.json`) combined with the camera's walking motion blur, book spines in the corridor/study sequence never resolved to legible letterforms, even after cropping into 2–4 overlapping tiles, upscaling 2× with LANCZOS, and in one case re-cropping a single spine at 4× (`tiles/Hq66X9f-zgc/t_000552_greenspine_x4.png`). Colour and gilt-tooling texture were visible; individual letters were not. Per the task's "never invent" rule, every one of those runs is recorded as `{"unlabelled": true, "count": N}` rather than guessed. This matches the pipeline's own assessment ("Spines visible but text only partly legible at 480p") — in practice, across every frame tested, "partly legible" did not extend to actual letterforms.

## Example titles with timestamps

Only two books were actually legible anywhere in the 179 frames, both in a single non-shelf **closeup** shot of a book stack on the living-room coffee table (not the corridor shelving):

1. **t=00:00:34 (`s_000033_60.jpg`)** — *Имя розы* (**Umberto Eco**, Russian edition of *The Name of the Rose*), cover spine reads "УМБЕРТО ЭКО / ИМЯ РОЗЫ" — **high confidence**, language `ru`.
2. **t=00:00:34 (`s_000033_60.jpg`, same frame)** — white paperback beneath it, French, spine reads "...AGE PEUT EN...", consistent with *Une image peut en cacher une autre* — **medium confidence** (partial title phrase, author not visible), language `fr`.

No further individual titles could be confidently read anywhere in the shelf-walking sequence (see below).

## Frame with clearly legible spines

**`/mnt/project-files/eco-video/frames/Hq66X9f-zgc/s_000033_60.jpg`** (t=00:00:34) — coffee-table close-up, not a shelf, but the only frame in the whole set with confidently readable book text (Russian Eco cover + partial French spine, both above).

No frame of the actual bookshelves (the corridor/study walk, `t_000454`–`t_000602`) reached legible resolution; the clearest of those is `t_000546.jpg` (t=00:05:46), where Eco faces the shelf directly and colour/texture is sharpest, but no letters resolve even under tiling.

## Notes

- **File naming:** the skipped-frame list of this video is `skipped_Hq66X9f-zgc.csv`; the generic `skipped.csv` belongs to another video's reading, so the two must not be confused, and overwriting my first output. `spines_Hq66X9f-zgc.jsonl` survived only because it was already video-specifically named. I regenerated the skip list under a collision-safe name, **`/mnt/project-files/eco-video/skipped_Hq66X9f-zgc.csv`** (matching the `skipped_B-M8V0PcCrw.csv` convention the other worker used), and did not touch the other workers' files. The generic `skipped.csv` currently on disk belongs to a different video, not this one.
- Frames under `/mnt/project-files/eco-video/library-map/` and `/mnt/project-files/eco-video/library-video/` were not present in this environment and, per instructions, were not touched in any case.
- `notes.json` (pre-existing) and my own review agree the visible spines are not resolvable at this resolution; nothing here contradicts that, it just confirms it exhaustively across every frame with shelves in view.
