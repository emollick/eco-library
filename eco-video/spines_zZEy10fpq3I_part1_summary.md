# Spines summary — zZEy10fpq3I, part 1 (600s–1200s)

Source: "Umberto Eco: La biblioteca del mondo" (2022), YouTube id `zZEy10fpq3I`, 1080p frames.
Slice covers KEEP.csv frames with `600 <= timestamp_seconds < 1200` (288 frames), read in timestamp order.

## Totals
- Frames read: 288 (all kept frames in the 600–1200s slice)
- Frames with legible book content recorded: 6 (in `spines_zZEy10fpq3I_part1.jsonl`)
- Frames skipped (no legible spines): 282 (in `skipped_zZEy10fpq3I_part1.csv`)
- Distinct titles recorded:
  - **High confidence:** Le Garzantine: Medioevo; Thesaurus Anatomicus (Frederik Ruysch); Turris Babel (Kircher); Ars Magna Lucis et Umbrae (Kircher, two copies — one gilt-printed spine, one hand-lettered ink spine); Ars Magna Sciendi (Kircher); Mundus Subterraneus (Kircher); Numero Zero (Umberto Eco); L'isola del giorno prima (Umberto Eco) — 8 titles
  - **Medium confidence:** Tempus, Aevum, Aeternitas; Obeliscus [Aegyptiacus?] (Kircher); China Illustrata (Kircher) — 3 titles
  - **Low confidence:** none recorded (unreadable spines were left as `unlabelled` counts rather than guessed)

## Rooms / walls identified, with time ranges in this slice
- **Fondazione Umberto Eco archive room** (`room_id: other`, `wall_id: fondazione-archive-1`) — white modular shelving, comic clippings, event photo standee — **786–788s**. Not one of the private-apartment rooms in `layout.md`; likely a Fondazione cataloguing/study room.
- **Rare-book room / Stanza degli antichi** (`room_id: rare`) — cherry/glazed cabinets and a table, matching `layout.md`'s rare-book room description — **844–874s** (Thesaurus Anatomicus, held book and open-page close-up) and **1040–1052s** (Athanasius Kircher shelf, `wall_id: rare-kircher-shelf`).
- **Office/interview shelving** (`room_id: other`, `wall_id: office-shelf-1`) — plain white shelving with paperback stacks, a desk piled with books — **1066s**. Distinct plainer setting, likely not the apartment itself.
- **Card-catalog archive room** — wooden card-catalogue cabinets, a man browsing — **1152–1198s**. Shelves visible only blurred/out of focus or through glass reflection; no legible spines, all skipped.
- Everything else in the slice (roughly 600–782s, 803–843s, 875–1039s, 1053–1065s, 1067–1151s) is talking-head interview footage, an unrelated grand historic library used as B-roll, open-book illustration/engraving close-ups (alchemical and anatomical plates, a Noah's Ark plate, Turris Babel plate, an ear-anatomy plate, bird-song notation plate), or book-cover title-card graphics — no shelf spines to record.

## Five example titles with timestamps
1. **Le Garzantine: Medioevo** — 786s (t_001306.jpg), Fondazione archive room
2. **Turris Babel** (Athanasius Kircher) — 1040s (t_001720.jpg), rare-book room Kircher shelf
3. **Ars Magna Sciendi** (Athanasius Kircher) — 1040s (t_001720.jpg), rare-book room Kircher shelf
4. **Mundus Subterraneus** (Athanasius Kircher) — 1052s (t_001732.jpg), rare-book room Kircher shelf
5. **Numero Zero** (Umberto Eco, Bompiani) — 1066s (t_001746.jpg), office/interview desk stack

## Clearest example frame
`/mnt/project-files/eco-video/frames/zZEy10fpq3I/t_001720.jpg` (1040s) — a crisp, well-lit, in-focus shot of a single rare-book-room shelf holding five Athanasius Kircher volumes with fully legible gilt and printed spine titles (Turris Babel, Ars Magna Lucis et Umbrae, Ars Magna Sciendi, China Illustrata, and a shelfmarked Obeliscus volume).

## Notes
- The Thesaurus Anatomicus identification (t_001434, 874s) is from a legible open-page running header ("THESAURUS ANAT...") rather than a spine, corroborated by the Italian captions in this window where a granddaughter recalls "il tesaurus anatomicus" and "il giardino degli scheletri" — recorded per task instructions to use captions only for context, not as invented content.
- Two frames (t_001404, and the s_001411_96 pair) show gilt leather spines held up to the camera in the rare-book room, but backlighting/motion blur make the tooled titles genuinely illegible at any crop/upscale; these were left unlabelled rather than guessed, per the "never invent" rule.
- The Kircher shelf (1040–1052s) was recorded across two frames (t_001720 as primary, t_001732 for two additional spines revealed by a further pan) using `same_as_frame` so each physical book is listed once, at its first legible timestamp.
