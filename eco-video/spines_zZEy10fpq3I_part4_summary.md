# Spine-reading summary — zZEy10fpq3I, part 4 (2400s–3000s)

Slice: frames with `timestamp_seconds >= 2400` and `< 3000` from
`/mnt/project-files/eco-video/frames/zZEy10fpq3I/KEEP.csv` (video time
~00:40:00–00:49:58). Source is the 2022 documentary *Umberto Eco: la
biblioteca del mondo*.

## Coverage

- **Frames in slice (KEEP.csv):** 239
- **Frames read via the Read tool:** 239 (100%)
- **Frames skipped (no legible shelf/book content):** 152 — logged in
  `spines_zZEy10fpq3I_part4.csv`-sibling file
  `/mnt/project-files/eco-video/skipped_zZEy10fpq3I_part4.csv`
- **Frames with book/shelf content recorded:** 87 — one JSON line each in
  `/mnt/project-files/eco-video/spines_zZEy10fpq3I_part4.jsonl`
- 152 + 87 = 239, so every frame in the slice is accounted for.

Skipped frames were mostly: archival black-and-white interview/lecture
footage (Eco at a lectern, on a red velvet chair, on a white sofa, in an
orange leather chair, at a panel/podium), vintage RAI television-studio
footage, a hand-drawn cartoon sequence illustrating "Name of the Rose"
monk characters (Malachia, Cellario, Severino, Alinardo), archival
photographs (conferences, football/stadium shots, news broadcasts,
Einstein/Pope Pius XII stills), and comic-panel/illustration close-ups —
none of these show legible book spines.

## Distinct titles recorded, by confidence

(Counted from non-`unlabelled` book entries across all 87 frame records;
the same physical book seen again on a repeated shelf was only counted
once, at its first legible timestamp, via `same_as_frame` chaining.)

| Confidence | Distinct titles |
|---|---|
| high (clearly legible spine/cover text) | 50 |
| medium (partial text / recognizable publisher or series) | 32 |
| low (guess from fragment, color, or context) | 19 |

Runs of spines with no readable text were recorded as
`{"unlabelled": true, "count": N}` rather than invented.

## Rooms / walls and their time ranges

| wall_id | time range | frames | description |
|---|---|---|---|
| rare-glass-cabinet-1 | 00:40:30–00:40:32 | 2 | glass-fronted cabinet of rare/bound volumes |
| rare-glass-cabinet-2 | 00:40:34–00:40:36 | 2 | continuation of the glass cabinet |
| study-desk-piles-1 | 00:42:50–00:43:02 | 7 | desk/study area with stacked books and papers |
| corridor-shelf-A | 00:43:12–00:43:30 | 8 | corridor shelving, Pinocchio / Salgari / popular-fiction section |
| stacks_shelf_sonzogno | 00:43:28 | 1 | archive stacks, woman browsing, Sonzogno-imprint adventure titles |
| stacks_shelf_A_baudelaire | 00:44:34–00:44:36 | 2 | archive stacks, shelf-edge tag "A / BAUDELAIRE HUYSMANS" |
| held-book-memoria-vegetale | 00:44:50–00:44:56 | 2 | book held to camera |
| interview-graybeard-1 | 00:44:58–00:45:14 | 8 | interview setting with background shelving |
| eco-foreign-editions-1 | 00:45:16–00:45:38 | 5 | shelf of foreign-language Eco editions |
| scholarly-shelf-Q49 | 00:46:16–00:46:39 | 4 | shelving with catalog tags "Q4.9/Q6.8/Q6.9" |
| book-cover-superuomo | 00:47:02–00:47:04 | 3 | "Il superuomo di massa" book cover shown to camera |
| montage-name-of-the-rose | 00:47:34–00:47:44 | 6 | graphic montage of foreign editions of "The Name of the Rose" (not a physical shelf — documentary title-card sequence) |
| eco-archival-red-chair | 00:47:48–00:48:58 | 17 | recurring archival interview clip, red velvet vest, red leather chair, blurred manuscript stand |
| eco-archival-white-sofa | 00:48:06–00:48:38 | 2 | recurring archival clip, white sofa, glass display case |
| interview-mustache-wooden-shelf | 00:48:12–00:48:24 | 5 | different interviewee, wooden shelving background |
| manuscript-tractatus-venenis | 00:48:40–00:48:44 | 3 | extreme close-up of a Latin manuscript, "Tractatus de Venenis" (gothic black-letter) |
| eco-archival-lecture | 00:48:59.6–00:49:24 | 9 | recurring archival clip, panel/podium, plant and water bottle |

(One frame, t_004746.jpg at 00:47:46, sits between the Name-of-the-Rose
montage and the red-chair archival clip and was recorded with
`wall_id: null` as a transitional/ambiguous graphic frame.)

## Five example titles with timestamps

1. **Il nome della rosa** (it) — t_004250.jpg, 00:42:50
2. **Pinocchio** (it) — t_004312.jpg, 00:43:12
3. **Il Corsaro delle Tenebre** (it, Casa Editrice Sonzogno, Milano) — t_004316.jpg, 00:43:16
4. **Storia del racconto popolare: prima del fumetto** (it) — t_004318.jpg, 00:43:18
5. **Lo scaffale infinito** (it) — t_004258.jpg, 00:42:58

## Best example of clearly legible spines

`/mnt/project-files/eco-video/frames/zZEy10fpq3I/t_004250.jpg` — a
close, sharply focused shelf shot yielding over 20 high-confidence
titles in one frame (Italian and a few German/French/Polish editions),
including *Il nome della rosa*, *Der ewige Faschismus*, *Giorgio
Morandi: une rétrospective*, and *L'era della comunicazione*.

Two other strong candidates: `t_004514.jpg` (a clean "OPERE"/Gobineau
shelf) and the `t_004840.jpg`–`t_004844.jpg` sequence, an extreme
close-up of the Latin "Tractatus de Venenis" manuscript page.
