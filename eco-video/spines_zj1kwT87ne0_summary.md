# Spine-reading summary — zj1kwT87ne0 ("Umberto Eco, Sulla memoria", part 2)

## Overview

All 192 kept frames in `KEEP.csv` were opened and reviewed in timestamp order (00:00–06:50). The video is a mix of:

- a black-and-white studio interview with Eco seated in an armchair (a glass curio cabinet with small objects, not books, blurred in the background),
- several archival film-clip inserts inset over the interview audio (*Things to Come*, 1936; a 1960s adding-machine/calculator ad; *Arte Programmata*, 1963; *Olympia*, 1938 javelin footage — all identified from the closing credits card at 06:44), and
- a closing colour sequence (from ~04:56) in which Eco walks from a piano/statue entryway down a long book-lined corridor into a large dedicated library room, pulls a book from a shelf, and leafs through it, while a title card reads "ANIMA / SOUL — Without memory, there is no soul" and the score plays with no further dialogue.

**Frames read:** 192 (100% of KEEP.csv)
**Frames with shelves/books entered in the JSONL:** 33
**Frames skipped (no shelf, or shelf not usable):** 159 — see `skipped.csv`

## Titles by confidence

| Confidence | Count | Titles |
|---|---|---|
| High | 1 | *Имя розы* (Russian ed. of *The Name of the Rose*), Umberto Eco |
| Medium | 1 | *Inventing the Enemy*, Umberto Eco (English) |
| Low | 2 | untitled French spine "UNE IMAGE / PETIT EN…" (Eco, fr); untitled English cover, author legible, title obscured by camera gear |
| Unlabelled (shelf spines, blur/low-res) | ~31 frames × 3–5 rows each, block counts only | — |

A genuine negative result should be reported plainly: **none of the 31 corridor/library shelf frames yielded legible spine text**, even after cropping to 2–3 overlapping tiles per frame and upscaling 2× with LANCZOS. The walking-camera shot is continuously motion-blurred, and the large-library-room portion (~05:30 onward) is additionally under-exposed/near-grayscale. Every shelf row in the JSONL is therefore recorded as `{"unlabelled": true, "count": N}`, with N a rough visual block-count, not an OCR result. The four legible titles above all come from two static close-up frames of books stacked on a coffee table in the interview room (00:26–00:34), not from the shelves.

One additional legible title was found but is **not** included in the JSONL because it is an editorial graphic insert (a full-screen photograph of the book's cover shown over the interview audio, not a shelf/book physically in frame): *La misteriosa fiamma della Regina Loana*, Umberto Eco (Italian, Bompiani), clearly readable at t_000348–358.jpg (~05:48–05:58). Listed in `skipped.csv` with this explanation.

## Five example titles with timestamps

1. **Имя розы** (*The Name of the Rose*), Умберто Эко — Russian hardback edition — `s_000033_68.jpg` @ 00:33.68 — high confidence
2. **Inventing the Enemy**, Umberto Eco — English paperback (striped cover) — `s_000026_52.jpg` @ 00:26.52 — medium confidence
3. Untitled French spine, "UNE IMAGE / PETIT EN…" — `s_000033_68.jpg` @ 00:33.68 — low confidence (spine text runs off-crop)
4. Untitled English cover, author "UMBERTO ECO" legible, title hidden under camera equipment — `s_000033_68.jpg` @ 00:33.68 — low confidence
5. **La misteriosa fiamma della Regina Loana**, Umberto Eco (Bompiani, it) — full-screen cover insert, not a shelf — `t_000350.jpg` @ 05:50 — high confidence (excluded from JSONL, see above)

## Clearest frame

No shelf frame in this video has individually legible spines. The **best-focused, least motion-blurred** shelf frame — useful as a starting point if a higher-resolution source becomes available — is:

**`t_000552.jpg`** (05:52, room "rare", wall "rare-room-4") — a near-static close shot of Eco reaching for a book directly in front of the camera. Exposure is still very dark/low-contrast and no letters resolve even at 2× tiling, but this frame has the least camera-motion blur of the whole corridor/library sequence.

For legible *text*, the closest frames are the two coffee-table book stacks: `s_000026_52.jpg` and `s_000033_68.jpg` (00:26–00:34), both in the living-room interview setting rather than on a shelf.

## Output files

- `/mnt/project-files/eco-video/spines_zj1kwT87ne0.jsonl` — 33 lines (2 book-cover closeups + 31 shelf/corridor frames)
- `/mnt/project-files/eco-video/skipped.csv` — 159 rows, reasons given per frame
