# Spine-reading summary — zZEy10fpq3I, part 3 (1800–2400s)

## Coverage

- **Slice**: frames with `timestamp_seconds >= 1800` and `< 2400` from `KEEP.csv` — **252 frames**, all read via the Read tool in timestamp order.
- **Frames with books recorded**: 12 (9 distinct camera setups, chained via `same_as_frame` where the camera dwelt on the same shelf/book).
- **Frames skipped (no legible shelves/spines)**: 240 — logged individually with a reason in `skipped_zZEy10fpq3I_part3.csv`.
- 252 = 240 + 12, i.e. every frame in the slice is accounted for exactly once.

## Distinct titles by confidence

**High confidence (20 distinct titles)**
- *Alcifrone ossia il filosofo minuzioso* — George Berkeley
- *Amphitheatrum Sapientiae Socraticae Joco-Seriae* (Latin, author not stated on spine)
- *Apocalittici e integrati* — Umberto Eco
- *Critica della ragion pura* — Immanuel Kant
- *Des signes et de l'art de penser considérés dans leurs rapports mutuels*, tomes 1–4 — Joseph-Marie Degérando
- *Dizionario filosofico* — Voltaire
- *Filosofia della rivelazione* — Schelling
- *I misteri della jungla nera* — Emilio Salgari
- *Il Corsaro Nero* — Emilio Salgari
- *La misteriosa fiamma della Regina Loana* — Umberto Eco
- *La scienza nuova. Le tre edizioni del 1725, 1730 e 1744* — Giambattista Vico
- *La tradizione signorile nella filosofia americana e altri saggi* — George Santayana
- *Le tigri di Mompracem* — Emilio Salgari
- *Saggio sull'intelletto umano* — John Locke
- *Sandokan alla riscossa* — Emilio Salgari
- *Trattato della natura umana* — David Hume
- *Tutte le opere (1721–1754)* — Montesquieu

**Medium confidence (3 distinct titles)**
- *Critica della ragion pratica* — Immanuel Kant
- *La scienza nuova* — Giambattista Vico
- *La tradizione signorile nella Spagna americana* — George Santayana (initial, more distant read of the same volume later corrected to the high-confidence title above once a closer frame was available; both entries kept for audit trail)

**Low confidence (1 distinct title, 2 spine variants)**
- *Champollion* — Jean Lacouture (spine visible but partly obscured; author name legible on one copy, not the other)

Plus numerous `{"unlabelled": true, "count": N}` runs on the crowded philosophy shelf (s_003519_33.jpg / t_003520.jpg) and the antique shelf row (t_003012.jpg) where spines were visible but too small, angled, or out of focus to transcribe reliably.

## Rooms / walls, with time ranges

| room_id | wall / view | time range |
|---|---|---|
| `grand_baroque_library_archival` | antique shelf row + single-volume macro insert (rack-focus establishing shot; busts, globes, green-and-gold fresco walls — archival B-roll, not Eco's apartment) | 00:30:12 – 00:30:20 |
| `other` | printed book covers/cards shown to camera (Salgari paperback cover gallery; a held book cover; a title-card insert) | 00:34:10 – 00:34:36 |
| `study` | Eco's home-library philosophy shelf — Bompiani "Il Pensiero Occidentale" series, with hand-written paper call-number tags (L11.5–L11.7, L12.5–L12.7 "LINGUE") on the shelf edge | 00:35:17 – 00:35:22 |

All remaining time in the slice (present-day narrator segments on a Turin balcony and in an empty theater with a glowing book-lamp prop; archival Umberto Eco interview close-ups against plain or damask backgrounds; a Bologna station 1980-bombing memorial sequence; a grandmother reading a picture book to a child; antique atlas/manuscript content pages being turned; hand-drawn caricature sketches; a superhero comic cover; military-parade archival footage; a university study hall) contained no legible book spines and was logged to the skip CSV.

## Five example titles with timestamps

1. **La scienza nuova. Le tre edizioni del 1725, 1730 e 1744** (Giambattista Vico) — `t_003520.jpg`, 00:35:20
2. **Des signes et de l'art de penser considérés dans leurs rapports mutuels, tome 1** (Joseph-Marie Degérando) — `t_003012.jpg`, 00:30:12
3. **Apocalittici e integrati** (Umberto Eco) — `t_003436.jpg`, 00:34:36
4. **Critica della ragion pura** (Immanuel Kant) — `s_003519_33.jpg`, 00:35:19
5. **Amphitheatrum Sapientiae Socraticae Joco-Seriae** — `s_003020_12.jpg`, 00:30:20.125

## One clearly-legible frame

`/mnt/project-files/eco-video/frames/zZEy10fpq3I/t_003520.jpg` — a close, well-lit shot of Eco's home-library philosophy shelf (Bompiani "Il Pensiero Occidentale" series) with several spines and a hand-written "L11.7 / L12.7 LINGUE" call-number tag clearly readable; verified with PIL-tiled crops during transcription.

## Notes on the two non-apartment book finds

Two of the four book-bearing frame clusters (`t_003012.jpg`/`s_003020_12.jpg`, timestamps ~00:30:12–00:30:20) show a different, grander library — carved stone/fresco walls, marble busts, terrestrial globes — used as brief archival/establishing-shot B-roll rather than Eco's own Milan apartment. They are included per the task's instruction to read every kept frame in the slice, but are tagged with a distinct `room_id` (`grand_baroque_library_archival`) so they can be filtered out downstream if the map-builder wants apartment-only shelving.
