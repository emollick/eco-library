# Eco library map

This folder holds the 3D map of Umberto Eco's Milan library. Four pieces make it: a generator that
turns two library catalogues, the spine readings taken from films of the flat and a set of curated
tables into `books.json`; a single-page viewer that draws every shelf from that file; a build step
that packs page and data into stand-alone pages; and a catalogue pipeline that supplies the book
descriptions.

The library is thousands of individual titles in Italian, French, Latin, German, Spanish and
English. `books.json` is documented in `schema_eco.md`. The page computes every world position from
that file, so a regenerated dataset needs no edit to the page.

## Running it

```sh
cd eco-map
python3 gen_books_eco.py     # books.json and books_for_descriptions.json, with a report on stdout
python3 build_eco.py         # dist/: index.html + books.json + vendor/, eco-map.html, eco-map-artifact.html, preview.jpg
python3 check_piano.py       # the piano piles against the film reference; exit 1 on any difference
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 test_page_eco.py    # the Playwright suite over dist/
```

`make_preview_eco.py` redraws `preview.jpg` when the picture is out of date. It reads the built
page, so it runs after `build_eco.py` and before the build that ships the new picture.

## The files

| file | what it is |
|---|---|
| `gen_books_eco.py` | The generator. Reads the catalogues, the film readings and the tables below; writes `books.json` and `books_for_descriptions.json`; prints the report. |
| `index_eco.html` | The page: markup, styles and the module that builds the scene with three.js, in one file. |
| `build_eco.py` | Packs the page and the data into `dist/`. |
| `make_preview_eco.py` | Renders `preview.jpg` from the built page in headless Chromium. |
| `test_page_eco.py` | The Playwright suite over `dist/`. |
| `check_piano.py` | Compares the piano piles in `books.json` with `eco-video/piano_piles.json`, pile for pile and spine for spine. |
| `schema_eco.md` | The shape of `books.json`, field by field, with the certainty tiers, the placement rules and the rule for English titles. |
| `books.json` | The dataset the page reads. |
| `books_for_descriptions.json` | The generator's second output: the book list `fetch_descriptions_eco.py` takes as input. |
| `vendor/` | three.js r160 under the MIT licence: `three.module.min.js`, `OrbitControls.js`, `PointerLockControls.js`. |
| `tour-images/` | Forty-seven pictures from Wikimedia Commons, one for each tour stop that shows the book. The generator embeds a 200-pixel copy in `books.json`. Credits and licences are in `NOTICE.md` at the repository root. |
| `preview.jpg` | The picture the page's `og:image` and `twitter:image` tags name, 1200 by 630. |
| `dist/` | The built output. |

## The generator

### What it reads from the rest of the repository

From `eco-video/`:

| file | what it gives |
|---|---|
| `layout.json` | The six rooms with their walls, bookcases, bays, shelves, widths and subject captions. The geometry source. |
| `books_by_wall_eco.json` | The deduplicated film and photograph spine readings. When it is absent the raw `spines_*.jsonl` and `spines_photos.jsonl` are read instead; when it is present those files only supply shelf-row hints. |
| `videos.json` | Video titles and addresses, and the `timestamp_offset_s` added to a reader's raw second before a link is made. Falls back to `meta/*.info.json`. |
| `objects_from_video.json` | The furniture, piles, artworks and curiosities inventoried from the footage, with the `rooms_seen` ranges behind the fog layer. |
| `piano_piles.json` | The film reference for the piles on the piano: order, titles and blanks, pile by pile. Tolerated when absent. |
| `quotes_*.json` | Quotations transcribed from the captions of each film, one file per video. |

From `eco-sources/`:

| file | what it gives |
|---|---|
| `braidense_eco_all.csv` | 2,105 Braidense records of the rare-book room, shelfmarks ECO.01 to ECO.04. |
| `braidense_eco_all.mrc` | The same records as UNIMARC. Only the 461/462 set titles of numbered volumes are read from it. Tolerated when absent. |
| `bologna_eco_modern.jsonl` | 3,047 SBN-UBO records of the working library: title, author, year, language, subjects, ISBN, and the copy fields (inventory number, provenance, dedication, ex-libris stamp, underlinings, marginalia, dog-ears, inserts). |
| `fondazione_galleries.json` | The Fondazione Umberto Eco's gallery pictures and captions. |
| `experience/` | `quotes.json`, `objects.json`, `notable_books.json`, `incunabula.json`, all optional. |

Every one of these is data. Nothing in them is executed, and nothing fetched from the web is ever
treated as an instruction.

### The tables next to the generator

These are edited by hand. Regenerate after editing any of them.

| file | what it decides |
|---|---|
| `wall_map_eco.json` | Spine-reader wall labels and room aliases to layout bookcase ids (`@pile` means a pile object), with the `reading_fixes` that correct a reading. |
| `subject_map_eco.json` | Bologna subject, Dewey and title rules to target bookcases, with a `fallback` for a record no rule matches. |
| `objects_map_eco.json` | How the filmed and inventoried objects are merged and placed: `anchor` on a bookcase, on another object or on a free wall spot; `attach` to a bookcase; `skip`; `create` for a thing neither inventory lists; the drawn `size`; the frame or photograph its thumbnail is cropped from. |
| `quotes_eco.json` | Quotations transcribed from the captions, each with its raw video second, its Italian and English text and a target. |
| `tour_eco.json` | The room-by-room tour that follows the film's long take through the flat: target, caption, quote reference. |
| `tours_eco.json` | The sourced tours. Each is an ordered list of stops whose `target` is a book, an object, a bookcase or a room, with a caption, a `source`, an optional verbatim quote with its attribution, an optional picture from `tour-images/` and an optional catalogue `record`. |
| `walk_eco.json` | The waypoints of the film walk replay: video clock second, world position and camera target, caption, quote reference. |
| `record_notes_eco.json` | Curated notes on single catalogue records: a corrected date, the note printed after the year, whether an edition is documented as posthumous. The export's own dates stay in the data. |
| `copy_notes_eco.json` | Qualifications of the Bologna copy records: a giver to drop, the note to print instead, the source for it. |
| `titles_en_eco.json`, `descriptions_en_eco.json` | English titles and descriptions for the page's Native / English switch, keyed by book id. Optional. `schema_eco.md` gives the rule a title follows and what `title_en_kind` means. |
| `descriptions_eco_seen.json`, `descriptions_eco_braidense.json`, `descriptions_eco_bologna.json` | The fetched descriptions, keyed by book id. Merged when present, tolerated when absent. |
| `descriptions_eco_overrides.json` | Read before the three files above and wins outright: a text checked by hand, or `description: null` to block every fetched text for that id. |

### Ids, origins, placements

Ids are `braidense:<bid>`, `bologna:<UBO id>`, `video:<video id>:<raw second>:<title slug>`,
`photo:<file stem>:<title slug>`, and `u:<n>` for a placeholder.

Origin is `video`, `photo`, `catalog` or `unlabelled`. Placement is `catalogued` (a shelfmark),
`seen` (a reader named the bookcase), `inferred` (room or subject level), `reference` (a catalogue
section entry listed on a table rather than shelved), `unshelved` (no rule places it) or `filler`.
Certainty is `certain`, `guess` or `unknown`, and every entry carries the sentence that says why.
`schema_eco.md` defines all of them.

Every slot on every working-library bookcase that no identified book takes is filled with an
`unlabelled` placeholder, so the shelves are as full as they are in the flat. The rare-book cabinets
hold only the catalogued records, with spine widths set so the records fill the cabinets. `--no-fill`
skips the filler while debugging.

### The report

`gen_books_eco.py` prints, on stdout: the slot and identified counts by origin, placement, language,
room and cabinet; the subject rules that placed the Bologna records and the records no rule matched;
the certainty tiers with their reasons; the copy-note counts; the spine readings by the level that
placed them, and the readings it rejected as not Eco's books; the piles with their heights against
the film reference; the descriptions merged and the descriptions it refused; the English title
counts; the quotations placed and unplaced; the tours with their stops; the notable books it could
not match; and the objects it placed automatically. Warnings are printed as they happen, prefixed
`WARN`, and also land in `meta.warnings`.

`--dropped-log FILE` writes a JSON-lines record of the Braidense entries not drawn as spines, the set
records and the editions printed after the collection left the flat, together with the recent
editions drawn as guesses.

### The film frames are not in the repository

`eco-video/frames/` holds the frames cut from the films. It is about a gigabyte per film and is
never committed, and neither are the room photographs the object thumbnails are cropped from. A
fresh clone that runs the generator therefore prints a warning for each object whose thumbnail frame
is missing, and writes a `books.json` whose objects carry no `thumb`. The page draws a neutral
canvas in place of the picture and says so.

The committed `books.json` was generated with the frames present and carries the thumbnails, so the
built pages show them. Regenerating without the frames drops them. Thumbnails and the embedded tour
pictures also need Pillow; without it the generator warns and leaves both out.

## The page

`index_eco.html` is the whole viewer. It fetches `books.json`, builds the rooms, the bookcases and
every spine with three.js, and offers two cameras: Orbit, which turns and zooms over the plan, and
Walk, at eye level, with the arrow keys or WASD on a desktop and a joystick on a phone.

The top bar carries the room buttons, the two camera modes, the Colour menu (language, certainty,
subject, source, century, on film, Eco's hand, given to Eco), an English button shown only when
`books.json` carries English titles, the search box, Any book, Tours, a More menu (Eco's walk,
Notable books, fog on the unfilmed shelves, the Fondazione's shelf letters) and About. A first visit
opens on a card with three doors into the map, the scene drifting behind it and the top bar still
live: once a session, and never on a link that names a state.

Clicking a book, a bookcase, a room or an object opens its panel: the sources with their links, the
description, the reason it is placed where it is, the Bologna copy notes, the incunabulum card.
Search runs over titles, authors, subjects, descriptions, givers, inscriptions, marks, tours and
objects.

A tour flies the camera to each stop in Orbit, or stands the visitor at a clear station in front of
it in Walk, opens the stop's panel and shows a card with the caption, the quotation and the source.
Eco's walk replays the film's path along `meta.walk`, with the quotations at their shelves and links
back into the video.

The address carries the state: `#book=`, `#case=`, `#object=`, `#room=`, `#tour=` with `stop=`, and
`mode=walk`, `lang=en`, `colour=`, `show=`. Copy link on a book card and Link on a tour card add the
exact viewpoint as `eye=` and `at=`, so a link lands where it was copied. Back and Forward walk the
entries the page itself made.

## The build

`build_eco.py` reads `index_eco.html` and `books.json` and writes four things into `dist/`:

| output | what it is |
|---|---|
| `index.html` with `books.json` and `vendor/` beside it | The loose page. It fetches the data and imports three.js from `./vendor/`. `--cdn` keeps the CDN import map instead. |
| `eco-map.html` | One file. three.js is inlined and served to the module through `blob:` URLs named by an import map; `books.json` is inlined too. |
| `eco-map-artifact.html` | The same single file for hosts that ignore import maps or block `blob:` module scripts. The module specifiers are rewritten as the page loads, falling back to the jsdelivr ESM builds of three.js r160. |
| `preview.jpg` | Copied from this folder when it exists. |

`--three` takes either the flat `vendor/` folder shipped here or an unpacked npm `three` package
(`build/three.module.min.js`, `examples/jsm/controls/*.js`); both layouts are accepted. The two
single-file builds ship each filler slot compact (id, bookcase, shelf, slot, width, height and a
flag), and the page's `loadData()` restores origin, placement, tier and section from it. `books.json`
itself stays complete. The script prints the size of each output and stops with an error if the
artifact file reaches the 16 MB limit.

`make_preview_eco.py` serves `dist/` locally, opens the loose page at 1200 by 630 on a room given by
`--room`, waits for the flight and the label passes to settle, and writes the JPEG. The footer, the
hint box and the object plates are hidden first, so the picture is the room alone. Deployment stages
`preview.jpg` beside `index.html`; see `netlify/stage.py`.

## The tests

`test_page_eco.py` needs the Playwright Python package and a Chromium build:

```sh
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 test_page_eco.py [--dist dist] [--shots screenshots]
```

`PLAYWRIGHT_BROWSERS_PATH` names the folder the browsers already sit in and defaults to
`/opt/pw-browsers`. The suite takes whatever Chromium build is there, rather than the one the Python
package expects, so nothing is downloaded during a run. `PW_CHROMIUM` names an executable outright
and overrides the search. `make_preview_eco.py` reads the same two variables.

The suite copies `dist/` to a temporary folder, serves it over a local HTTP server and drives
`index.html` there. The environment variable `SCRATCH` names the folder the temporary copy is made
in; without it the system temporary folder is used. Screenshots go to the folder `--shots` names,
`screenshots/` by default, created on the run.

What it checks: no console errors; a rendered scene (a canvas that is not black, frames per second
above zero); every room button, with a screenshot each; a book with a video, photo or catalogue
source opening a panel with a working source link, and an unlabelled book opening the placeholder
panel; search; the walk toggle; the colour overlays, their legend counts against `meta.counts` and
the certainty filters; object thumbnails, spine lettering and the Eco's copies index; works in no
record shown as ghost cards; spine luminance at eye level and label occlusion measured from the
screenshots; an incunabulum pickable through the cabinet glass; the opening card on desktop and on a
phone; the address, the links that land on it and Copy link; the More menu;
the two copy-note colour modes with their legends and inscriptions; Any book; the preview tags and
picture; the phone layout, with the tour card clear of the joystick and the Exit walk button; and
every tour, stop by stop, with the target resolving, the camera arriving, the panel opening, the
spine unoccluded and no nearer than 0.9 m in Orbit, and a walk station inside the stop's room and out
of the furniture. A book hidden by the certainty filter must still appear at its stop as a stand-in
spine, and Esc must leave the filter as it was.

It then loads `eco-map.html` and `eco-map-artifact.html` from `file://` and requires both to reach
the same ready state, and finally runs `check_piano.py` over `books.json`. Exit code 1 on any
failure.

`check_piano.py` can be run on its own. For every pile the film reference lists it compares the
number of spines, the kind of spine at each position from the top, the title of a titled entry
(exactly, as a fragment the map's fuller title completes, by reading id, or as one of the map's
alternative readings), the absence of a title where the reference has none, the author where both
give one, and the stack heights. It prints every difference and exits 1 when there is one.

## Book descriptions

Descriptions are short public summaries from Wikipedia, in the edition of each book's own language
before English. They are fetched once and committed, so the map builds without a network.

### `fetch_descriptions_eco.py`

```sh
python3 fetch_descriptions_eco.py --input books_for_descriptions.json                  # full run -> descriptions_eco.json
python3 fetch_descriptions_eco.py --input books_for_descriptions.json --dry-run        # print the plan, no network
python3 fetch_descriptions_eco.py --input books_for_descriptions.json --limit 50       # first 50 books only
python3 fetch_descriptions_eco.py --input books_for_descriptions.json --resume         # keep what is in the output, skip those ids
python3 fetch_descriptions_eco.py --input books_for_descriptions.json --lang-order it,en   # the same edition order for every book
python3 fetch_descriptions_eco.py --input books_for_descriptions.json --verbose        # one line per book with its timing
python3 fetch_descriptions_eco.py --input books_for_descriptions.json --offline        # cache only, for re-running the matching rules
```

Other options: `--out` (default `descriptions_eco.json` next to the script), `--cache-dir` (default
`cache/`), `--workers` (default 6). It needs `requests` and nothing else from outside the standard
library.

**Input**: a JSON list of books, each `{"id", "title", "author", "language", "year"?, "publisher"?,
"source_kind": "video"|"photo"|"catalog", "confidence"}`. `language` may be an ISO code, a MARC code
or a name (`it`, `fre`, `ger`, `lat`, `Italian`). `author` may be `Given Surname` or `Surname,
Given`, with dates in `()` or `<>`, which are stripped.

**Output**, keyed by book id:

```json
"s001": {"description": "Il nome della rosa è il romanzo d'esordio di Umberto Eco, pubblicato nel 1980. ...",
         "description_kind": "article", "description_source": "https://it.wikipedia.org/wiki/Il_nome_della_rosa",
         "wikipedia_title": "Il nome della rosa", "wikipedia_lang": "it"}
```

`description_kind` says how honest the text is about the book:

| kind | meaning |
|---|---|
| `article` | The summary of the Wikipedia article whose title is the book's normalised title, fetched directly. |
| `search` | The same, but the article came through the search API, and only when the hit's title equals the book title or the book title plus the author's surname. |
| `author` | No article on the book, so one sentence about the author, phrased `By AUTHOR (b. YEAR): ...`. |
| `none` | Nothing found. `description` is `null`. |

**Order of requests** per book: the editions for its language (`it`, `fr`, `de`, `es` give that
edition then `en`; Latin gives `it` then `en`; anything else `en`), and within each edition first the
REST summary endpoint for the normalised title (leading series numbering, a subtitle after a colon
and trailing volume or edition notes stripped, accents kept), then the search API. A direct hit must
be a standard article naming the author in its lead, or, for a book with no usable author, an article
describing a written work. A redirect that lands on a page titled differently from the book, such as
`De docta ignorantia` to `Nicola Cusano` on it.wikipedia, is refused. A title of more than 12 words
(`MAX_SEARCH_WORDS`, mostly long truncated Latin catalogue titles) skips the search step: a quoted
phrase that long can never pass the exact-title rule, and every request counts against the budget.
Descriptions are the first two sentences of the extract, at most 320 characters.

**Caching and politeness**: every HTTP result, 404s included, is cached as `cache/<lang>/<kind>-<sha1
of the normalised query>.json`, so a rerun or a `--resume` costs no requests. HTTP 429 and 5xx are
retried with backoff, up to six times, honouring `Retry-After` and pausing every worker together;
those responses are never cached. Requests go through `HTTPS_PROXY` when it is set, verify TLS
against `/root/.ccr/ca-bundle.crt` when that file exists, and identify themselves as
`EcoLibraryMap/1.0`. Progress is saved and printed every 100 books.

**The budget is about 500 requests an hour.** That is Wikimedia's stated limit for anonymous
clients, per address, shared across every edition and both endpoints. Measured on this egress: 534
successful requests an hour, with nearly every request answered by a 429 whose `Retry-After` of 20 to
60 seconds is exactly the refill time. The per-book wall clock is dominated by those pauses, not by
the 0.3 s a request itself takes. A run needing thousands of single-title requests therefore takes
many hours, which is what the prewarm scripts are for.

### Braidense rare books

```sh
python3 convert_braidense.py                                  # -> books_braidense.json, braidense_id_map.json
python3 prewarm_summaries.py --input books_braidense.json     # batch-fill the summary cache, 20 titles per request
python3 prioritise_braidense.py                               # reorder: ECO.03 section, pre-1600, authors with an article first
python3 fetch_descriptions_eco.py --input books_braidense.json --resume --workers 6 --out descriptions_braidense.json
python3 expand_braidense.py                                   # -> descriptions_eco_braidense.json keyed "braidense:<bid>"
```

`convert_braidense.py` makes one query per distinct normalised title and author: multi-volume records
collapse into the first record's id, and bare volume records (`Vol. 1.`, `2`) into one query per
author and shelfmark set. `braidense_id_map.json` maps every `braidense:<bid>` to the id of the query
that covers it. The author comes from the statement of responsibility with roles and honorifics
dropped (`a cura di`, `par`, `by`, `von`, `compiled by`, `M.`, `l'abbé`) and only the first name
kept. A statement naming nobody (`par l'auteur de ...`, `par une Société de professeurs`) or naming
only the writer of a preface gives `null`, as do the 1,390 records with no statement at all, most of
them Latin title pages whose title already carries the author in the genitive. Year is the first
four-digit year in `date`, else the catalogue's `year` column. Language maps MARC
`ita/fre/lat/eng/ger/spa` to ISO and passes other codes (`grc`, `heb`, `mul`) through, which the
fetcher treats as English only.

`prewarm_summaries.py` asks the Action API (`prop=extracts|description|pageprops|info`, `exintro`,
redirects followed) for every title variant and author name the fetcher would ask for, 20 titles per
request, and writes the answers into `cache/<lang>/summary-*.json` in the REST summary's shape
(`type`, `title`, `description`, `extract` for the first lead paragraph, `content_urls`), marked
`"via": "prewarm-action-api"`. Misses and invalid titles become 404 entries. The fetcher, run
afterwards with `--resume`, then spends its budget on searches alone. Existing cache entries are
never overwritten.

`prioritise_braidense.py` reorders the list in place so that, when a run has to be paused or shares
the budget, the queries most likely to matter go first: one point each for an ECO.03 shelfmark (the
most precious section), for printing before 1600, and for an author whose name resolves to a person's
article in the pre-warmed cache. Stable sort by score; nothing else changes.

`expand_braidense.py` copies each query's result to every bid in the map. It can be run on a partial
output at any time, since the fetcher saves every 100 books.

### Bologna modern books

The BUB harvest is too big for one request per title (about 5,000 title and edition pairs plus 3,000
author names), so it is done by prewarming alone: batch queries of exact titles and author names,
then the fetcher offline. The per-book search stage never runs for it.

```sh
python3 convert_bologna.py                                                     # -> books_bologna.json, bologna_id_map.json
python3 prewarm_bologna.py --input books_bologna.json --what titles            # probe 50/request, extracts 20/request
python3 fetch_descriptions_eco.py --input books_bologna.json --offline --out descriptions_bologna.json
python3 prewarm_bologna.py --input books_bologna.json --what authors --unresolved descriptions_bologna.json
python3 fetch_descriptions_eco.py --input books_bologna.json --offline --out descriptions_bologna.json
python3 expand_bologna.py                                                      # -> descriptions_eco_bologna.json keyed "bologna:<record id>"
```

`convert_bologna.py` makes one query per distinct normalised title and author: 3,047 records give
2,966 queries. The title is UNIMARC 200 $a with the SBN sorting markers (`Il *nome`, `<<Les >>`)
removed, a trailing ` / responsibility` dropped and leading volume numbering (`1: `, `2.1.: `, `t. 2:
`, `°1!: `) stripped before the fetcher's `clean_title`. A record whose own title is only a volume
number takes its parent record's title (461 $a), so the volumes of one work share a query, which
covers 84 records. The author is the main author (700) as `Given Surname`, with the SBN qualifiers
resolved (`Bruyne, Edgar : de` to `Edgar de Bruyne`, `William : of#Ockham` to `William of Ockham`; a
leading `De` or `Di` that belongs to the surname is kept), else a 702 with author role 070, else the
statement of responsibility when it is a bare personal name. Editors and translators are never
promoted, so 523 queries carry no author.

`prewarm_bologna.py` is `prewarm_summaries.py` in two stages. It first probes 50 titles per request
(`prop=info|pageprops`, redirects followed) and caches every miss at once as a 404 summary entry,
then fetches `exintro` extracts for the surviving titles only, 20 per request. With `--what authors
--unresolved descriptions_bologna.json` it takes only the authors of books that got no article.
`--dry-run` counts the requests without touching the network. On this list: 5,305 title pairs of
which 660 exist, 108 probes plus 36 extract batches, 144 successful requests and 173 HTTP calls with
29 rate-limit retries; then 2,893 author pairs of which 1,640 exist, 61 plus 85, 146 successful and
161 HTTP with 15 retries. **290 successful requests, 334 HTTP in all**, 45 minutes of wall clock
while sharing the address with the Braidense fetch.

`expand_bologna.py` tests each result before copying it to every record id, because an exact title
match across editions can land on a different thing of the same name. An `article` whose lead says
the page is a film or a surname index is dropped to `none`; three Bevilacqua and Berto novels hit
their film adaptations and `Giacobetti` a surname list. An `article` whose page is the person the
book is by, which happens with artist monographs and anthologies titled with the author's name
(`Leonardo Cremonini`, `T.S. Eliot`, `John Dee`), is turned into an `author` description. An `author`
description whose person was born after the book appeared is a homonym and is dropped. A short
hand-made `REJECT` list drops the rest: `Paolo Conti: sculture` hitting a footballer, the journals
`Desk` and `Colophon` hitting the furniture and the printing term, `Piccole italiane` hitting the
organisation, and the semiotics volume `Sense and sensibility` hitting Jane Austen. Every adjustment
is printed. Over 3,047 records the result is 135 `article`, 4 `search`, 1,703 `author` and 1,205
`none`. A known limit of the `author` kind: a homonym born *before* the book is not caught, such as
an 1828 policeman named Luigi Berti standing in for the critic who wrote `L'imagismo` in 1944.

### The pipeline's files

| file | what it is |
|---|---|
| `books_braidense.json`, `books_bologna.json` | The deduplicated query lists the converters write. |
| `books_seen.json` | The film and photograph readings taken from a generator run's `books_for_descriptions.json`. This is the list the fetcher read to write `descriptions_eco_seen.json`. |
| `braidense_id_map.json`, `bologna_id_map.json` | Every record id to the id of the query that covers it. |
| `descriptions_braidense.json`, `descriptions_bologna.json` | The fetcher's raw output, keyed by query id. The expanders turn these into the `descriptions_eco_*.json` files the generator reads. |
| `sample_books_eco.json`, `sample_descriptions_eco.json` | Ten books and their output, exercising the paths: direct articles in it, fr, de and en; a Latin book found on en.wikipedia by search after the it.wikipedia redirect to its author was refused; catalogue-style titles with numbering, a subtitle and a volume number; an invented anonymous title giving `none`; and two obscure or invented titles by well-known authors giving `author`. |

`reconcile_braidense.py` reads `eco-sources/braidense_eco_all.mrc` and reconciles the export with the
library's own count of the transferred collection, 1,328 volumes in 73 boxes. Into the folder `--out`
names it writes `braidense-reconciliation.jsonl` (one line per record: what the record is, its ECO
shelfmarks and inventory numbers, the links to parent and component records, and the evidence),
`braidense-shelfmarks.jsonl` (one line per ECO.01 to ECO.03 running number, with the strings and
records under it and the volumes it stands for) and `reconciliation-summary.json` (the counts the
About text quotes). A record is a catalogue entry, not a spine, so the summary gives the physical
volumes as a range and never forces the library's figure.
