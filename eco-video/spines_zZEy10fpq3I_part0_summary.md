# Spine reading summary — zZEy10fpq3I, part 0 (0s–599s)

## Coverage
- Slice: 318 kept frames with `timestamp_seconds` in [0, 600) from `KEEP.csv`.
- 23 frames written to `spines_zZEy10fpq3I_part0.jsonl` (10 of these are "anchor" frames with full rows; 13 are `same_as_frame` continuation/duplicate frames, several of which add newly-legible books).
- 295 frames written to `skipped_zZEy10fpq3I_part0.csv`, each with a specific reason (opening titles/logos, a ~2-minute b/w tracking-shot credit sequence with the corridor shelving permanently out of focus, talking-head interviews, archival TV/funeral footage, an ex-libris bookplate print, held comics, manuscript text pages, archival photographs, or motion-blurred/duplicate shelf pans already covered by an anchor frame).
- 23 + 295 = 318 — every frame in the slice is accounted for exactly once.

## Distinct titles by confidence
- **High** (title/author clearly legible): 29 book entries, e.g. *Tela Ignea Satanae* (Wagenseil), *Histoire des langues*, *Anatomiae Amphitheatrum* / *De Macrocosmi Historia* (Robert Fludd), *Artis Cabalisticae*, *Petrus Galatinus*, *Aristotelis Opera*, *Ars Magna Lucis et Umbrae* (Athanasius Kircher), and 15 foreign-language editions of Umberto Eco's own novels (Danish, Ukrainian, Russian, Dutch, Croatian, English, Lithuanian, German, Polish).
- **Medium** (partial letters + recognisable pattern/publisher): 16 entries, e.g. *De Sepulchris Hebraeorum*, *De Coelo et de Inferno*, Gaffarel's *Curiositez*, *Opus Mago-Cabbalisticum* (Sallwigt), *Philosophia Nova* / *Philosophia Moysaica*, *Bongo*, *Il libro rosso*, *Il giardino delle camelie*, plus several more foreign Eco editions (Turkish, Bulgarian, Czech, Greek, Russian, Hebrew).
- **Low** (guess/very partial): 3 entries — a French "Traité des..." fragment, an uncertain Michael Maier attribution, and a hand-lettered vellum spine ("...ctionarii Scripturae...").
- Roughly 60+ additional books are recorded as `unlabelled` bulk counts (blank, worn, or too-far-to-read spines within an otherwise-legible row), per the "never invent" instruction.

## Rooms / walls identified, with time ranges
- **rare / rare-hermetica-shelf** — open wooden shelving of 17th–18th c. occult/hermetic and antiquarian volumes (Wagenseil, Fludd, Bongo, Galatinus, Caramuel…). 00:06:00–00:06:12 and again 00:08:28–00:08:34 (camera returns to the same shelf).
- **rare / rare-glass-cabinet-table** — glass-fronted wooden bookcase, interview standing beside it. 00:07:03–00:07:06.
- **rare / rare-manuscript-table** — table with a row of vellum-bound folios (*Aristotelis Opera*, *Richardus a Sancto Victore*). 00:07:44–00:08:08.
- **rare / rare-kircher-book** — open folio, Kircher's *Ars Magna Lucis et Umbrae*. 00:08:12.
- **study / study-labeled-sections** — Eco's own working library, shelves labelled by author/subject/language. 00:05:22–00:05:26.
- **study / study-general-shelves** — general (non-Eco) modern shelving, panning shot. 00:09:04–00:09:12.
- **study / study-eco-translations-wall** — dedicated bay (labelled "Q4"/"Q5"/"ECO IBERICI") of foreign editions of Eco's own novels, in at least 15 languages. 00:09:26–00:09:32.
- Everything before ~00:05:22 (opening titles, a stylised b/w tracking shot through a corridor of blurred shelving, talking-head interview segments, archival TV/funeral footage about Eco's death, an ex-libris bookplate print, and a Linus/Ecolinus comic being handled) contained no shelf frame with legible spines and was logged to `skipped_zZEy10fpq3I_part0.csv`.

## Five example titles with timestamps
1. *Tela Ignea Satanae, Tom. I* — Johann Christoph Wagenseil — `t_000602.jpg`, 00:06:02 (362s)
2. *Histoire des langues* — `t_000602.jpg`, 00:06:02 (362s)
3. *Artis Cabalisticae* — `t_000606.jpg`, 00:06:06 (366s)
4. *Ars Magna Lucis et Umbrae* — Athanasius Kircher — `t_000812.jpg`, 00:08:12 (492s)
5. *De begraafplaats van Praag* (Dutch ed. of *The Prague Cemetery*) — Umberto Eco — `t_000926.jpg`, 00:09:26 (566s)

## Frame with clearly legible spines
`/mnt/project-files/eco-video/frames/zZEy10fpq3I/t_000926.jpg` — the "ECO IBERICI"/Q4 shelf bay of foreign-language editions of Eco's own books; roughly 15 spines are cleanly legible in one shot.

(A close second: `t_000828.jpg` for the hermetica shelf, and `t_000812.jpg` for the Kircher title page.)
