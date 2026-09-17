# zZEy10fpq3I — spine-reading summary, part 7 (t ≥ 4200s / 70:00 to end, ~4814s)

## Coverage
- Slice: all `KEEP.csv` rows with `timestamp_seconds >= 4200`, in timestamp order.
- **250 frames read** (every filename in the slice was opened with the Read tool).
- **7 frames** yielded legible book/spine text and are recorded in `spines_zZEy10fpq3I_part7.jsonl`.
- **243 frames** had no legible spines and are recorded in `skipped_zZEy10fpq3I_part7.csv` (talking-head shots of the Cenacolo/Last Supper analysis, website/blog screenshots, an out-of-focus/backlit corridor sequence, and — from ~4536s to the very end (4814s) — the film's full end-credits roll, confirmed by direct inspection at several points spread across that stretch).

## What's actually in this slice
This part of the documentary is **not** continuously inside Eco's apartment. In chronological order it covers:
1. ~70:00–72:30 — a scholar discussing Leonardo's *Last Supper* (Cenacolo Vinciano) and the "Milo Temesvar" literary hoax; talking-head and fresco/manuscript-page shots only, no shelves.
2. ~73:00–74:30 — a segment on "libraries of the world" that cuts to stock/B-roll footage of a large modern public library, explicitly captioned in the end credits as **Binhai Library, Tianjin, China**.
3. ~74:20–74:40 — the film's **"Epilogo"** title card, followed by a static shot of a miniature (dollhouse-scale) shadow-box diorama of a fireplace/library nook, decorated with tiny framed photos of Umberto Eco himself.
4. ~74:40–75:20 — a return to the **real apartment**: a girl on rollerblades skates down the long white-shelved corridor, then into a smaller **rare-book room**, where a 17th-century volume lies open on a table and a glass cabinet holds a shelf of **Athanasius Kircher** first/early editions.
5. ~75:36 (4536s) onward — full end credits (cast, crew, the library-donation notice, and library photo-credit cards), confirmed black-background/text-card content straight through to the last kept frame at 4814s.

## Distinct titles by confidence
**High (6):**
- *Encyclopaedia Judaica* — t_011308.jpg (4388s)
- *Le Robert* (French dictionary) — s_011431_96.jpg (4471s)
- *Ars Magna Sciendi, Sive Combinatoria*, Athanasius Kircher — t_011512.jpg (4512s)
- *Kircheri de Arte Magnetica*, Athanasius Kircher — s_011513_00.jpg (4513s)
- *Joco-seriorum Naturae et Artis, sive Magiae Naturalis*, Athanasius Kircherus — s_011513_00.jpg (4513s)
- *Obeliscus Aegyptiacus*, Athanasius Kircher — s_011513_00.jpg (4513s)

**Medium (5):**
- 中共党史人物传 (Chinese CPC-history biographical series) — t_011310.jpg (4390s)
- *Intertesto*, Mario Ciampi — t_011426.jpg (4466s)
- *Clave: diccionario de uso del español actual* — s_011431_96.jpg (4471s)
- *Iter Exstaticum* (Kircher-related) — s_011513_00.jpg (4513s)
- *Tabula Kircheriana* — s_011513_00.jpg (4513s)

**Low (2):**
- "Stendhal" (author name on a miniature spine) — t_011336.jpg (4416s)
- "ARTE" (partial word on a miniature spine, unlabelled title) — t_011336.jpg (4416s)

## Rooms / walls identified, with time ranges
| room_id | wall_id | wall_name | time range |
|---|---|---|---|
| other | world-libraries-stock-1 | Stock B-roll of Binhai Library, Tianjin (not Eco's apartment) | 4388–4390s |
| other | epilogue-diorama-miniature | Miniature diorama shadow-box (Epilogo segment) | 4416–4440s (static shot repeated) |
| corridor | corridor-shelving-main | Real apartment — long white shelving corridor | 4466–4470s |
| other | exterior-window-view-1 | Real apartment, exterior courtyard view through two windows | 4471s |
| rare | rare-books-table / rare-books-kircher-cabinet | Real apartment — rare-book room, table + Kircher cabinet | 4504–4529s |
| (credits) | — | End-credits roll, black background | 4536–4814s (end) |

## 5 example titles with timestamps
1. *Encyclopaedia Judaica* — 4388s (t_011308.jpg)
2. *Le Robert* — 4471s (s_011431_96.jpg)
3. *Kircheri de Arte Magnetica* (Athanasius Kircher) — 4513s (s_011513_00.jpg)
4. *Ars Magna Sciendi, Sive Combinatoria* (Athanasius Kircher) — 4512s (t_011512.jpg)
5. *Intertesto* (Mario Ciampi) — 4466s (t_011426.jpg)

## Most clearly legible frame
`/mnt/project-files/eco-video/frames/zZEy10fpq3I/s_011513_00.jpg` — a glass-cabinet shelf of Athanasius Kircher rare editions in the apartment's rare-book room; spine text is sharp and legible even before cropping (six titles read at high/medium confidence from this one frame).

## Notes on scope/quality
- Several frames in this slice show real footage but are **not** Eco's personal collection (the Tianjin library B-roll, the exterior courtyard view); these were still recorded per instructions since shelves/spines were visible and legible, with `room_id: "other"` and notes flagging the non-apartment context.
- The miniature diorama (t_011336.jpg and its duplicates) is an artistic prop, not a real bookshelf; its "spines" are printed facsimiles too small to read reliably beyond two fragments.
- No inventions: every unreadable run of books was recorded as `{"unlabelled": true, "count": N}` rather than guessed.
