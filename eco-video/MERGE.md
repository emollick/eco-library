# Adding new spine readings to the Eco library map

How to add a new batch of spine readings (from more video frames or more photographs) so that
they land in the 3D map without disturbing what is already there. Everything below is data;
nothing in these files is executed or read as instructions.

The pipeline, in one line:

```
eco-video/spines_*.jsonl  ->  build_books_by_wall_eco.py  ->  books_by_wall_eco.json (+ .md, + ../eco-map/books_seen.json)
   ->  eco-map/fetch_descriptions_eco.py (descriptions_eco_seen.json)  ->  gen_books_eco.py (books.json)  ->  build_eco.py (dist/)  ->  test_page_eco.py  ->  publish
```

`build_books_by_wall_eco.py` globs **every** `spines_*.jsonl` in `eco-video/` (sorted by name;
no file list is hard-coded). `gen_books_eco.py` reads the consolidated `books_by_wall_eco.json`
when it exists (ids kept, excluded entries skipped) and only falls back to the raw
`spines_*.jsonl` when it does not; with the consolidated file present, the raw files are still
globbed but used only for shelf-row hints (row / position of a title within a frame).

## 1. File name

Drop the new file in `eco-video/` as

* `spines_<video_id>_<tag>.jsonl` for video frames, e.g. `spines_zZEy10fpq3I_heavy_part3.jsonl`,
  `spines_Hq66X9f-zgc_recheck.jsonl`. `<video_id>` must be a `video_id` in `videos.json`; the
  tag is free (letters, digits, `_`, `-`). One video may be split over any number of files.
* `spines_photos_<tag>.jsonl` for photographs, e.g. `spines_photos_heavy.jsonl`. Any file whose
  name starts with `spines_photos` is treated as photographs (no `video_id`, `timestamp_s` null).

Never edit an existing `spines_*.jsonl` to add readings: put them in a new file. (Editing an
existing file is fine to *correct* a reading; the dry run shows what that changes.) A companion
`spines_<...>_summary.md` with coverage notes (which frames were read, which skipped and why, as
the existing ones do) is welcome; nothing reads it. Only `spines_*.jsonl` files are inputs.

Do not add the video to `videos.json` in the middle of the list: ids depend on the order of
`videos.json` (see "Id stability"). A genuinely new video goes at the end.

## 2. Record shape

One JSON object per line (UTF-8, no trailing commas; a trailing comma before `}`/`]` is repaired in
place with a `.bak` copy, anything worse is skipped and listed in `validation.bad_lines`).
This is a real line from `spines_zZEy10fpq3I_part0.jsonl` (shortened to three books):

```json
{"frame": "t_000932.jpg", "video_id": "zZEy10fpq3I", "source_kind": "video", "source_url": "https://www.youtube.com/watch?v=zZEy10fpq3I&t=572s", "timestamp_s": 572, "time": "00:09:32", "room_id": "study", "wall_id": "study-eco-translations-wall", "wall_name": "shelf bay Q4/Q5, foreign-language editions of Umberto Eco's own books", "view": "shelves", "shelf_rows_visible": 2, "same_as_frame": "t_000926.jpg", "rows": [{"row": 2, "row_label": "lower shelf, mostly Prague Cemetery / History of Beauty foreign editions", "books": [{"pos": 18, "unlabelled": true, "count": 1, "spine_text": "purple spine \"UMBERTO ECO\", title not legible", "language": null, "confidence": "low"}, {"pos": 19, "title": "The Prague Cemetery", "author": "Umberto Eco", "series": null, "publisher": null, "language": "en", "confidence": "high", "spine_text": "THE PRAGUE CEMETERY"}, {"pos": 20, "title": null, "author": "Эко (Umberto Eco)", "series": null, "publisher": null, "language": "ru", "confidence": "medium", "spine_text": "ЭКО / [...] (Russian ed., partial)"}]}], "notes": "Lower shelf of the same Eco-translations bay, mostly further editions of The Prague Cemetery and On Ugliness/History of Beauty in different languages."}
```

A pile / table stack (`view: "stack"`), from `spines_iRXEQVTI95k.jsonl`:

```json
{"frame": "s_000055_60.jpg", "video_id": "iRXEQVTI95k", "source_kind": "video", "source_url": "https://www.youtube.com/watch?v=iRXEQVTI95k&t=55s", "timestamp_s": 55.6, "time": "00:00:55", "room_id": "rare", "wall_id": "w6", "wall_name": "Table display: comics and pipes", "view": "stack", "shelf_rows_visible": 1, "same_as_frame": null, "rows": [{"row": 1, "row_label": "table", "books": [{"pos": 1, "title": "Mandrake", "author": null, "series": null, "publisher": null, "language": "it", "confidence": "high", "spine_text": "MANDRAKE"}]}], "notes": "Two issues of the Italian 'Mandrake' comic displayed on a table with a pair of tobacco pipes."}
```

A photograph, from `spines_photos.jsonl` (note `source_credit`, `timestamp_s: null`, no `video_id`,
and the Fondazione bookcase letter in `wall_name`):

```json
{"frame": "fondazione_01_E.webp", "source_kind": "photo", "source_url": "https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/01_E.webp", "source_credit": "Foto Studio Curti Parini (curtiparini.com) for Fondazione Umberto Eco", "timestamp_s": null, "room_id": "study", "wall_id": null, "wall_name": "Bookcase 'E' (Fondazione lettering), Milan apartment working library: caption 'Ancient art and art catalogues'", "view": "shelves", "shelf_rows_visible": 5, "rows": [{"row": 3, "row_label": "3", "books": [{"pos": 3, "title": "Bernini", "author": null, "series": null, "publisher": null, "language": "it", "confidence": "medium", "spine_text": "BERNINI"}, {"unlabelled": true, "count": 33}]}], "notes": "..."}
```

### Frame-level fields

| field | video | photo | meaning |
|---|---|---|---|
| `frame` | required | required | the frame's file name (`t_HHMMSS.jpg`, `s_HHMMSS_ff.jpg`) or the photo file name; the stem becomes part of photo ids and photo wall ids |
| `video_id` | required | absent | YouTube id, must be in `videos.json` |
| `source_kind` | `"video"` | `"photo"` | anything else is normalised from the file name with a warning |
| `source_url` | required | required | video: **recomputed** from `videos.json` `url` + the corrected second, so write whatever is convenient; photo: used verbatim as the page's source link, so it must be the real public URL |
| `source_credit` | - | recommended | shown as the photo credit |
| `timestamp_s` | required, numeric | `null` | the raw frame time, see section 3 |
| `time` | optional | - | `HH:MM:SS`, informational |
| `room_id` | required | required | one of the reader room ids below |
| `wall_id` | recommended | optional | free text, the reader's label for one physical shelf / table / cabinet; see section 4 |
| `wall_name` | recommended | recommended | free text; **this is where the shelf labels and call tags must appear**; see section 4 |
| `view` | required | required | `shelves`, `closeup`, `person`, `other`, `stack` (free text is tolerated with a warning: text containing "shelf" or "close" counts as a shelf view, anything else as "other") |
| `shelf_rows_visible` | optional | optional | number of shelf rows in the frame; used to place a row on the rendered bookcase |
| `same_as_frame` | optional | optional | the canonical frame of the same camera setup; informational (see section 6) |
| `rows` | required (may be `[]`) | required | list of `{"row": n, "row_label": "...", "books": [...]}`; `row` 1 = top |
| `notes` | required (may be `""`) | required | free text for humans; **only** its "not Eco's" phrases affect the pipeline (section 5) |

### Book entries inside `rows[].books`

| field | meaning |
|---|---|
| `pos` | position from the left within the row, 1-based (a warning when missing) |
| `title` | the title as read on the spine, in the spine's language and script; `null` when only the author is legible (author-only entries are kept, listed as "[no title; author only]", and dedupe only on compatible authors) |
| `author` | as read; `null` when not on the spine. Do not copy a neighbour's author onto a spine that shows none (this is the one known error in the data, fixed by hand in `wall_map_eco.json` `reading_fixes`) |
| `series`, `publisher` | as read, else `null` |
| `language` | ISO 639-1 of the spine text (`it`, `fr`, `de`, `en`, `la`, `es`, `ru`, `bg`, `tr`, `he`, ...); drives which Wikipedia edition is asked for the description |
| `confidence` | `high` / `medium` / `low`, section 7 |
| `spine_text` | **always record it**: the exact lettering seen, in reading order, with `/` between lines and `[...]` or `...` for illegible parts; parentheses for what is inferred. It is the audit trail of the reading and is shown on the page unaltered |
| `notes` | optional, per book |
| `read_as` | optional, `{"title": ..., "author": ...}`: what this reader actually read when `title` / `author` were aligned to an earlier reading's spelling of the same spine, or a substantive alternative the reader wants kept (a bracketed fragment such as `[Colonna]` may stay in here, never in `author`). `gen_books_eco.py` shows it as an alternative reading on the book (`alt_readings`); it never makes a second book |
| `{"unlabelled": true, "count": n}` | a run of `n` spines with no legible text (a `spine_text` describing them is tolerated). Counted, never turned into a book |

Anything with neither `title` nor `author` is counted as one unlabelled spine.

## 3. Frame timestamp rule (raw frame times, never pre-corrected)

`timestamp_s` is the `timestamp_seconds` value `process_video.py` gave that frame in the
video's `KEEP.csv` (or `INDEX.csv`), **copied as is**:

* for the 11 official and news videos the frame names and times are true source times, so
  KEEP.csv says `24.96`, `33.6`, ... and `t_000025.jpg` is at 24.96 s;
* for `zZEy10fpq3I` (the 2022 documentary) the labels are the raw `fps=0.5` slot times:
  `t_000932.jpg` -> `timestamp_s: 572` (= 9:32), not 572.96. `videos.json` carries
  `"timestamp_offset_s": 0.96` for this video and `0` for all others; `build_books_by_wall_eco.py`
  adds it when it writes `timestamp_s` (corrected) next to `timestamp_raw_s` (as written) and when
  it builds the `&t=NNs` link. **Do not add the 0.96 yourself**, and do not use the corrected time
  in `timestamp_s`: the book id is built from `int(timestamp_raw_s)`, so a pre-corrected value
  would give the same frame a different id.

Scene frames `s_HHMMSS_ff.jpg` carry exact `pts_time` values; copy those too.

## 4. room_id, wall_id, wall_name and the shelf labels the placement uses

**`room_id`** (reader's vocabulary, mapped by `ROOM_MAP` in the script):

| reader `room_id` | layout room | effect |
|---|---|---|
| `living` | `salotto` | Living room |
| `vestibule` | `vestibolo` | Entrance hall |
| `corridor` | `corridoio` | Long corridor (bookcase A). The art leg (`corridoio-arte`) is reached through a wall label matching `corridor-art`, `art corridor`, `second corridor` |
| `study` | `studio` | The big study |
| `rare` | `antichi` | Room of the Ancients (rare-book room / Studiolo) |
| `bologna-reinstalled` | `bologna` | the 2026 Bologna reinstallation: Eco's books, no Milan position; placed by subject rules (`inferred`) |
| `unknown` | `unknown` | not assignable to a Milan room; kept, placed only if a wall label resolves (the ANRW shelf goes to `@subject`) |
| `other` | `other` | **not Eco's shelves** (other libraries, B-roll, book-cover inserts, logo cards, screen grabs): see section 5 |

`grand_baroque_library_archival` and `archive_stacks` are legacy ids that map to `other`; do not
use them. Any other `room_id` is a validation error and the line is skipped.

**`wall_id`** is your name for one physical shelf, cabinet, table or pile within one video.
The consolidation namespaces it as `<video_id>:<wall_id>` (`photo:<wall_id or frame stem>` for
photographs) and merges every frame with the same `wall_id` into one wall record. That matters for
three reasons:

1. `gen_books_eco.py` resolves where a reading goes from the **wall record**: the wall's
   `wall_name` (= the `wall_name` of the *earliest* frame with that `wall_id`) and the sighting's
   `wall_id` (prefix stripped) are matched against `eco-map/wall_map_eco.json` (`aliases`,
   `patterns`, `label_patterns`, the Fondazione letters) and the call-tag parser. A new file that
   repeats an existing shelf must therefore reuse the **same `wall_id` string** (case-sensitive;
   look it up in `books_by_wall_eco.json` `walls[].wall_id` or `.md` "Walls"), and should repeat
   the same `wall_name`. If your new frame is earlier than the existing ones, its `wall_name`
   becomes the wall's name: keep the shelf label in it. The dry run prints `WALL RENAMED` when this
   happens.
2. A `view: "stack"` frame (or a `wall_id` matching `coffee.?table|table.?closeup|desk.?stack|
   table stack|pile on the table`, or any alias in `wall_map_eco.json` whose value is `@pile`)
   becomes a **pile object**, one per distinct `wall_id` per room. Use one `wall_id` per physical
   pile so its books stack together.
3. Book ids do not depend on `wall_id`, but the wall list, pile membership and the "seen" /
   "inferred" placement do.

**Shelf labels** (the Fondazione's hand-written call tags visible on the shelf edges, and the
subject tabs). They are read from `wall_id` + `wall_name` **only**, never from `notes`, and only for
readings in the working-library rooms (`study`, `corridor`, `vestibule`, `living`; not `rare`,
whose cabinets are placed from the Braidense shelfmarks). Two mechanisms, in this order:

* `wall_map_eco.json` `label_patterns`: `[regex, target]` or `[regex, target, "label", name]`,
  tried case-insensitively on `wall_id + " " + wall_name`. Currently:
  `ECO IBERICI` / `Q4/Q5` / "foreign-language editions of Umberto Eco" / "Eco's own works" ->
  `study-Q` (seen); `Pensiero Occidentale` -> `study-L8-12`; `L11.x` / `L12.x` / "call tags
  L11/L12" -> `study-L8-12`; `FRANCOFORTE` / `DELEUZE` / "Frankfurt School" -> `study-M-A` at level
  `label` (a subject tab, so placement `inferred` with the tab as reason); `Encyclopédie ... L11`
  -> `study-L8-12`. Add a row there for a new label rather than inventing a wall alias.
* the generic call-tag parser: `<letter> <bay>[.<shelf>]` with a letter in `letters` of
  `wall_map_eco.json` (`A`-`S`) and, for `A`, bay <= 25: `A 48` is ignored (there is no corridor bay
  48), `A 13` -> `corridor-13`, `L4.10` -> `study-L1-4`, `L11.5` -> `study-L8-12`, `Q4.9` ->
  `study-Q`. Regex: `(?<![A-Za-z0-9.])([A-S])\s?(\d{1,2})(?:\.\d{1,2})?(?![A-Za-z0-9])`. A tag in
  a room where that unit does not exist is dropped.

So: write the tags exactly as seen (`Q4/Q5`, `L11.5`, `A 13`, `ECO IBERICI`) in `wall_name`, and
also in `notes` for the human reader if you like; `notes` alone places nothing. A photograph's
`wall_name` should carry the Fondazione letter as `Bookcase 'E'` or `Bookcase 'A', shelves 7-12`
(bays 7-12 of the corridor); the forms `L1-4`, `M-A`, `Na`, `Ob`, `antichi-SX`, `rare-02` are also
recognised as bare words.

When no label is known, a `study` reading falls back to `room_default` (`study-P`) with tier
"guess" and the reason stated; that is honest but uninformative, so prefer a label whenever the
frame shows one.

## 5. Exclusion rule (room "other" and "not Eco's" notes)

A frame is excluded when its `room_id` is `other`, or when its `notes` / `wall_name` contain a
phrase such as "not Eco's shelves", "not part of Eco's apartment", "not the private apartment",
"distinct from the Eco apartment", "(not Eco's ...)" (regex `NOT_ECO_RE` in the script; "not
the Milan apartment" alone does *not* exclude, because the Bologna frames say that). Books read on
such frames are still consolidated, but:

* a book is `excluded: true` only when **every** one of its sightings is on an excluded frame
  (kept in `books_by_wall_eco.json` with `exclude_reason` for the audit, absent from
  `books_seen.json`, listed by `gen_books_eco.py` under `rejected_other`, never drawn);
* a book seen both on an excluded frame and in an Eco room keeps only its Eco-room sightings
  (`dropped_other_sightings` counts the rest; the wall records still list it).

Use `other` for anything that is not one of Eco's shelves: other libraries, stock footage, a book
cover shown as an insert, a printed page, a logo card. Use `unknown` (not `other`) when the shelf
may well be Eco's but you cannot tell which room. Two trailer shelves whose room was identified
later are re-tagged by `ROOM_OVERRIDES` in the script.

## 6. same_as_frame, duplicates and dedupe

* `same_as_frame`: the canonical frame of the same camera setup, when you logged several frames
  of one dwell. The pipeline ignores it, but readers use it to avoid re-reading; a frame with
  `same_as_frame` may still carry `rows` (only what is newly legible, or the full list again;
  either is fine). Frames with `rows: []` still count as frames of the wall and help the
  "what the camera saw" layer.
* Dedupe key (`dedupe_rule` in the JSON): normalised title (lower-case, accents and punctuation
  stripped, a trailing parenthetical gloss such as "(The Name of the Rose)" dropped, a leading
  it/fr/en/de/es article dropped, volume words bd/band/vol/tome/teil/principat dropped) plus
  author compatibility (token sets in a subset relation; a missing author is a wildcard on an
  exact title match). So "Имя розы (The Name of the Rose)" and "Имя розы" merge, "Der Friedhof in
  Prag / Eco" and "Der Friedhof in Prag / Umberto Eco" merge, but "The Prague Cemetery" (en) and
  "Il cimitero di Praga" (it) are, correctly, two books. Two copies of the same title on one
  frame become one book with two sightings.
* Do not invent: a spine you cannot read is `unlabelled`, a title you can only partly read is
  `low` confidence with the fragments in `spine_text`, a title you infer from fragments gets the
  inference in `spine_text` in parentheses. Nothing is ever "completed" from memory of what Eco
  owned.

A second, independent reading of frames already read (`spines_zZEy10fpq3I_piano_heavy.jsonl` re-reads the piano pass of `spines_zZEy10fpq3I_piano.jsonl`
from 1080p frames) reuses the first file's `wall_id` **and** `wall_name` strings exactly (the builder warns `WALL RENAMED` otherwise), and gives its frames the
`timestamp_s` of the KEEP.csv slot they re-shoot (`p_0104.jpg`, true 2580.6 s, is the 2582 slot; `p_0054.jpg`, true 2571.0 s, the 2570 slot; the true time
may sit in `timestamp_true_s`, `same_as_frame` names the slot's frame) so that the ids of the books it confirms do not change. Where it agrees with the first
reading it spells the title / author as the consolidated file does (`read_as` keeps its own reading); where it differs it keeps its own title with the first
reading's in `read_as`, or vice versa, and the generator picks the higher confidence. Its `unlabelled` runs count the spines nobody could read, so that a
stack frame's row adds up to the pile's height (`objects_map_eco.json` `books_high`).

## 7. Confidence

Per book, `high` / `medium` / `low`:

* `high`: title (and author when printed) read in full, no ambiguity;
* `medium`: partly read or inferred from unambiguous fragments / a known edition design;
* `low`: fragments only, or a guess that should be checked.

The consolidated book carries `best_confidence` (the highest of its sightings; title/author are
taken from that sighting). `gen_books_eco.py` puts `low` readings in the "guess" tier. Any other
value is tolerated with a warning and ranks below `low`.

## 8. Id stability

`id` = `video:<video_id>:<int raw timestamp_s>:<title slug>` or `photo:<frame stem>:<title slug>`
(`by-<author slug>` for author-only entries; `-2`, `-3` suffixes when two distinct books collide),
from the book's **first** sighting: videos in `videos.json` order, then raw second; photographs
after all videos, in file-name order (`spines_photos.jsonl` first), then line order. A rerun on
the same files gives byte-identical output apart from `generated_at`.

Adding a file **cannot** change an existing id, except in these cases, all of which the dry run
prints as `ID CHANGED old -> new (reason)` or `MERGED DUPLICATES`:

* (a) it adds an **earlier sighting** of a known book: an earlier second of the same video, a
  sighting in a video listed earlier in `videos.json`, or a video sighting of a book so far seen
  only in photographs;
* (b) it **bridges two clusters** of the same title: an author-less reading merges with any
  author, so it can join "X / author A" and "X / author B" into one book (which keeps one of the
  two ids);
* (c) it adds the **first included sighting** of a book so far seen only on excluded frames (the
  book gets an id from the included sighting; its excluded sightings are dropped from the list).

An id that changes must be renamed in the eco-map files keyed by id (the dry run says which):
`descriptions_eco_seen.json` (or just let the fetcher fetch it again), `descriptions_eco_overrides.json`,
`wall_map_eco.json` `reading_fixes`, and any `tour_eco.json` / `quotes_eco.json` /
`objects_map_eco.json` entry that names a book. `books.json` ids are regenerated anyway.

## 9. Merge steps

**(a)** Put the new file(s) in `eco-video/` as `spines_<video_id>_<tag>.jsonl` or
`spines_photos_<tag>.jsonl` (section 1).

**(b)** Consolidate, dry run first:

```sh
cd eco-video
python3 build_books_by_wall_eco.py --dry-run     # writes nothing; lists BAD lines, NEW FILE, NEW BOOK, NEW SIGHTING, ID CHANGED, MERGED DUPLICATES, REMOVED, NEW WALL, WALL RENAMED, totals, descriptions to fetch, referenced old ids
python3 build_books_by_wall_eco.py               # books_by_wall_eco.json + books_by_wall_eco.md, and ../eco-map/books_seen.json (rewritten completely)
python3 build_books_by_wall_eco.py --dry-run     # must now end with "no changes"
```

Fix every `BAD` line before the real run (a skipped line is a lost frame). Read the `ID CHANGED`
/ `MERGED` / `WALL RENAMED` lines and decide whether they are what you meant; a `WALL RENAMED`
whose new name lost its call tag will move books from "seen" to "guess".

**(c)** Descriptions for the new books. `books_seen.json` is the full list of included books
(the script rewrites it; nothing to append). `--resume` keeps every entry already in the output
and looks up only the ids that are missing, so:

```sh
cd eco-map
python3 prewarm_summaries.py --input books_seen.json                  # optional but recommended: 20 titles per request into cache/, then the fetcher spends its budget on searches only
python3 fetch_descriptions_eco.py --input books_seen.json --resume --workers 6 --out descriptions_eco_seen.json
```

Rate limit: about **500 requests per hour** get through to Wikimedia; past that nearly every
request is answered 429 with a `Retry-After` of 20-60 s, which the fetcher honours (a shared pause
across workers, up to six retries, never cached). A batch of a few dozen new books takes minutes;
hundreds take an hour or more, which is what the prewarm step shortens (see the README section
"Book descriptions"). The `descriptions to fetch` list of the dry run is exactly the set of ids
this step will look up. Check the result with

```sh
python3 -c "import json; d=json.load(open('descriptions_eco_seen.json')); s=json.load(open('books_seen.json')); m=[b['id'] for b in s if b['id'] not in d]; print(len(d),'entries;',len(m),'missing:',m[:10])"
```

If the dry run reported `ID CHANGED old -> new` and the old id had a description, either let the
fetcher find it again (the cache makes direct lookups free; only a search costs a request) or copy
the entry:

```sh
python3 -c "import json,sys; p='descriptions_eco_seen.json'; d=json.load(open(p)); old,new=sys.argv[1:3]; d[new]=d.pop(old); json.dump(d,open(p,'w'),ensure_ascii=False,indent=1)" 'video:...:old' 'video:...:new'
```

and rename the key in `descriptions_eco_overrides.json` / `wall_map_eco.json` `reading_fixes` when
the dry run listed them under `REFERENCED OLD ID`.

**(d)** Regenerate and test the map (do not edit `index_eco.html` for a data update):

```sh
cd eco-map
python3 gen_books_eco.py            # books.json + books_for_descriptions.json; the report must say "spine source: consolidated books_by_wall_eco.json (N books, ...)"
python3 build_eco.py                # dist/eco-map.html, dist/eco-map-artifact.html (must stay under 16 MB), dist/index.html + books.json + vendor/
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 test_page_eco.py   # headless Chromium smoke test; exit code 0, "all checks passed"; never run `playwright install`
```

In the `gen_books_eco.py` report look at: `spines:` (`frames_unresolved` should not grow: an
unresolved frame is a wall label nothing in `wall_map_eco.json` matches; add an alias, a pattern
or a `label_patterns` row), `rejected_other` (the excluded readings; check that only `other`
frames are there), `WARN reading_fixes: no reading with id` (an id in `reading_fixes` that no
longer exists), the description validation counts, and `by_placement.seen` (new readings with a
shelf label should raise it, not `inferred`). Open `dist/index.html` and find one of the new
books with the search box.

**(e)** Publish the rebuilt page. `dist/eco-map-artifact.html` is the single-file version.
The loose build (`dist/index.html`, `books.json`, `vendor/`) goes to the live site with the
kit in `netlify/`: `stage.py` copies and rewrites it into a staging folder, `deploy.sh` uploads
that folder and runs the Playwright check against the site.

## 9a. The dense-pass files

The dense pass of `dense/` reaches the consolidation as ordinary `spines_<video>_dense.jsonl`
files, one for each of eight videos. Their book entries carry the audit fields `dense_id`,
`dense_tier`, `dense_reason`, `dense_read_confidence`, `dense_placement_basis`,
`dense_bookcase_id`, `dense_bay`, `dense_shelf_from_tag`, `dense_tags`, `dense_match`,
`dense_confirms` and `read_as` (the sighting's own spelling when the consolidated title
differs); frames re-shot inside a first-pass slot carry `timestamp_true_s` and `same_as_frame`
(section 6). The consolidation ignores the fields it does not know; `eco-map/gen_books_eco.py`
reads them from the raw files.

Where the two passes read a different title at the same row and position of the same frame, the
higher confidence wins and a tie goes to the first pass. A losing dense entry is withheld from
the file and named in the frame's `dense_conflicts`; a winning one marks the first-pass sighting
`drop_first_pass`, which the generator skips at ingestion. Pairs across two frames of a panning
shot are reported, not resolved. `dense/conflicts_resolution.json` is the record of every pair
and its outcome.

## 10. Checklist for the reader of new frames

* [ ] File named `spines_<video_id>_<tag>.jsonl` / `spines_photos_<tag>.jsonl`, one JSON object per line, in `eco-video/`.
* [ ] `timestamp_s` copied raw from the video's `KEEP.csv`; no +0.96 for `zZEy10fpq3I`.
* [ ] `room_id` from the table in section 4; `other` only for shelves that are not Eco's; `unknown` when the room is unclear.
* [ ] A shelf that is already in `books_by_wall_eco.json` reuses its exact `wall_id` and `wall_name` so the frames merge into the same wall (and the same pile); a shelf that is new gets a fresh, descriptive `wall_id`.
* [ ] Every call tag or subject tab visible on the shelf edge is written in `wall_name` exactly as seen (`Q4/Q5`, `L11.5`, `A 13`, `ECO IBERICI`, `FRANCOFORTE`); `notes` alone does not place anything.
* [ ] `view: "stack"` for piles and table stacks; `shelves` / `closeup` for shelf frames.
* [ ] Every readable spine has `spine_text` with the exact lettering; illegible runs are `{"unlabelled": true, "count": n}`; nothing is invented or completed from memory; a neighbour's author is never copied onto a spine that shows none.
* [ ] `title` in the spine's own language and script; `language` is the ISO code of that text; `confidence` is `high` / `medium` / `low`.
* [ ] A spine that repeats a known book is logged again anyway (it becomes a second sighting, not a duplicate) with the same title spelling when the spine shows the same text.
* [ ] `python3 build_books_by_wall_eco.py --dry-run` shows no `BAD` lines, and every `ID CHANGED` / `MERGED DUPLICATES` / `WALL RENAMED` line is understood before the real run.
* [ ] Steps (c) to (e) done in order, and `test_page_eco.py` passed on the exact file that is published.
