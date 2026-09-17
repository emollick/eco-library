# Spine-reading summary — zZEy10fpq3I, part 5 (3000s–3600s)

## Frames read
- Slice size: **269** kept frames (timestamp_seconds ≥ 3000 and < 3600), all read in timestamp order.
- Frames with books recorded: **3**
- Frames skipped (no shelf / not Eco's apartment / illegible): **266**

This is an unusually low "hit rate" for the slice because most of 3000–3600s is *not* B-roll of Eco's own shelves:
roughly the first minute is archival sketches (his own maze/character drawings for *The Name of the Rose*) followed
by a long sweeping shot of the **St. Gallen Abbey library** in Switzerland (identified by the "ST. GALLUS" inscription
and Baroque twin towers) shown as illustrative B-roll while he discusses the abbeys that inspired his novel. Later,
~3436s–3600s is a **dramatized reading segment** ("Zoe Tavarelli" reading an Eco essay on Shakespeare/Bacon) shot in
a modern **university law library** (numbered aisle signs 175–177, law textbooks in English/Italian) — a different,
identifiable location, not Eco's Milan apartment. Both were treated as "different location" and excluded from the
spines file rather than misattributed to Eco's own collection. The remainder is talking-head interview footage,
archival engravings/animation illustrating Robert Fludd and the Bacon–Shakespeare authorship controversy, and a
few extreme close-ups (mirror, glass vitrine) too shallow-focus to read.

## Distinct titles by confidence
- **High confidence (4):**
  - *Everyman's Talmud* — Abraham Cohen (en)
  - *Annuario Filosofico 1993* — Mursia (it)
  - *Annuario Filosofico 1994* — Mursia (it)
  - *Le Roy Soleil* (fr)
- **Medium confidence (2):**
  - *Ernst Blochs Wirkung* (de)
  - *L'attico reclamato* (it)
- **Low confidence (0 named)** — one Hebrew-script spine and a single bold "K" initial were judged too fragmentary
  to name safely and were folded into unlabelled counts rather than guessed.

## Rooms / walls labelled, with time ranges
| room_id | wall_id | time range | notes |
|---|---|---|---|
| living | living-gosh-shelf | 00:50:56–00:50:58 (3056–3058s) | White modern shelf beside a framed "GOSH!" print |
| study | study-francoforte-deleuze | 00:53:12–00:53:18 (3192–3198s) | Shelving with subject tabs "FRANCOFORTE" / "DELEUZE" |
| rare | rare-leather-shelf-eco | 00:57:04 (3424s) | Antiquarian leather-bound shelf behind Eco's interview seat |
| other (unrecorded) | — | 00:50:15–00:50:48 (3015–3048s) | St. Gallen Abbey library, Switzerland — B-roll, not Eco's apartment |
| other (unrecorded) | — | 00:57:16–00:59:59 (3436–3599.7s) | University law library — dramatized reading segment, not Eco's apartment |

## Five example titles with timestamps
1. *Everyman's Talmud* (Abraham Cohen, en) — t_005058.jpg, 00:50:58 (3058s)
2. *Ernst Blochs Wirkung* (de) — t_005312.jpg, 00:53:12 (3192s)
3. *Annuario Filosofico 1993* (Mursia, it) — t_005312.jpg, 00:53:12 (3192s)
4. *Annuario Filosofico 1994* (Mursia, it) — t_005312.jpg, 00:53:12 (3192s)
5. *Le Roy Soleil* (fr) — t_005704.jpg, 00:57:04 (3424s)

## Clearest frame for legible spines
**t_005704.jpg** (00:57:04 / 3424s) — Eco seated for interview directly in front of a sharp, well-lit antiquarian
leather-bound shelf; the gilt-lettered "LE ROY SOLEIL" spine is clearly legible, along with the general character
(worn red/brown leather, gilt bands) of the surrounding volumes.

## Output files
- `/mnt/project-files/eco-video/spines_zZEy10fpq3I_part5.jsonl` (3 lines)
- `/mnt/project-files/eco-video/skipped_zZEy10fpq3I_part5.csv` (266 rows + header)
