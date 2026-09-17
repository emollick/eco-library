# spines_M8IWTOFNlOc summary

**Video:** Umberto Eco interview, Louisiana Channel, ~24.5 min, 1080p.
**Frames in KEEP.csv:** 466. **Frames read (Read tool, full size):** 466 (via 16 contact sheets of thumbnails first, then every distinct angle at full resolution). **Frames logged in spines_M8IWTOFNlOc.jsonl:** 460. **Frames skipped:** 6 (title card, 2 exterior establishing shots, 3 closing-credit cards -- see skipped_M8IWTOFNlOc.csv).

## Method
Built 16 contact sheets (30 thumbnails each, filename+timestamp labelled) covering all 466 kept frames in timestamp order to find camera/angle changes, per the task's guidance that the background is mostly static. Five distinct camera setups ("walls") were found:

| wall_id | room_id | what it is | frame range | outcome |
|---|---|---|---|---|
| `_W1` | rare | Orange armchair + glass display cabinet (two open illuminated-manuscript pages), the main interview backdrop | ~15s-1401s and 1417-1425s (423 frames) | background permanently out of focus; unreadable at every timestamp checked |
| `_W2` | study | Writing desk with pigeonhole/grid shelving, seen once as Eco walks to it (~10-13s) and again close-up while he reads (~66-85s) | 14 frames | shelving too small/blurred even close-up; unreadable |
| `_W5` | study | A real bookshelf close-up + two book piles on a desk, cut in right after Eco says "I am a rare books collector too" / "There are my books..." | 1403-1415s (10 frames) | **readable** -- see below |
| `_W4` | study | Floor-to-ceiling metal shelving + rolling library ladder holding dozens of foreign editions of Eco's own works | 1442-1461s (13 frames) | **readable** -- see below |
| (title/exterior/credits) | -- | Louisiana Channel bumper, Milan street exterior, closing credits | 6 frames | no book content, skipped |

For `_W1` and `_W2` (blurred, static, 437 frames combined) each was read carefully once at its sharpest frame, and every other frame of the same setup was logged with `same_as_frame` pointing back to that canonical frame, per the task's instruction for repeated backgrounds. `_W5` and `_W4` (where real spine text is visible) were each cropped into 2-6 overlapping tiles with PIL, upscaled 2-4x LANCZOS with unsharp-mask sharpening, and read tile by tile.

`_W1` is the *same physical setup* (same armchair, same glass cabinet with the same two manuscript pages) as the companion 93-second clip `rMSOvDAyH5c`, confirming both were filmed in the same session/room.

## Legibility and confidence
- High confidence titles: 8 (5 of Eco's own works across languages/piles, 3 by other authors on his desk)
- Medium confidence: 2 (title clear, author or exact spine text partly obscured)
- Low confidence: 4 (author clear, title not resolved, or vice versa)
- Unlabelled runs logged: 2 manuscript pages x 423 `_W1` frames; ~20 unlabelled spines x 14 `_W2` frames; small unlabelled runs within the `_W5` shelf/stack rows; ~63 unlabelled spines across the two `_W4` shelf rows (approximate visible-spine counts, not exact/invented figures)

## Example frames (5)
| timestamp | frame | wall | note |
|---|---|---|---|
| 00:01:21 | t_000121.jpg | `_W2` (study, desk) | canonical desk close-up; pigeonhole shelving confirmed unreadable |
| 00:06:29 | t_000629.jpg | `_W1` (rare) | canonical interview shot; same cabinet as rMSOvDAyH5c |
| 00:23:23 | t_002323.jpg | `_W5` (study) | **clearest single-spine frame** -- "Umberto Eco, A paso de cangrejo" fully legible |
| 00:23:31 | t_002331.jpg | `_W5` (study) | sharpest book-stack frame; 4 titles read at high confidence |
| 00:24:05 | t_002405.jpg | `_W4` (study) | own-works wall; "The Island of the Day Before", "Baudolino", Greek "The Prague Cemetery" |

**Clearest frame overall:** `/mnt/project-files/eco-video/frames/M8IWTOFNlOc/t_002331.jpg` (book stack, four full titles + two authors legible at high/medium confidence).

## Titles found (high + medium confidence)
- *A paso de cangrejo* -- Umberto Eco (es)
- *Lavorando anche per il futuro* -- Mario Andreose (it)
- *Il ritorno di Himmelfarb* -- Michael Kruger (it)
- *Razza e destino* -- Editori Laterza, author not legible (it)
- *Dando buca a Godot* -- Stefano Bartezzaghi (it)
- *Le cose che ho imparato* -- Gianni Riotta (it)
- *The Island of the Day Before* -- Umberto Eco (en)
- *Baudolino* -- Umberto Eco (it)
- *To Koimeterio tes Pragas* (The Prague Cemetery) -- Umberto Eco (el)
- *The Prague Cemetery* -- Umberto Eco, second/English copy, partly hidden by ladder strut (en)

## Quotes about his library or specific books
10 remarks logged in `quotes_M8IWTOFNlOc.json`, all about his library/reading/collecting, including: designing the library labyrinth for *The Name of the Rose* (07:30); "I am a rare books collector too" and his collection of "fake books" such as Ptolemy over Galileo (22:30-22:43); the size of his collection -- "about 50,000" total, "35,000" in this Milan flat, up from 30,000 when he moved in 25 years earlier (22:49-23:07); "I don't read -- I write" (23:10); the Woody Allen "War and Peace" quick-reading joke (23:47); and "There are my books -- translations ... and they are books on me" (24:07), spoken just before the camera cuts to the `_W4` wall of his own works.
