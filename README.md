# Umberto Eco's library: a 3D map

A walk-through 3D model of Umberto Eco's private library in his Milan flat on Piazza
Castello, with every shelf slot that could be reconstructed from public sources, the books
that could be identified on them, and a short description of each book where one exists.
The library held about 33,000 books. The rare books, about 1,300 volumes with the 36
incunabula, have been at the Biblioteca Nazionale Braidense in Milan since 2021, where a
room keeps them in Eco's own order. The working library, donated by the family to the
State and lent to the University of Bologna, stayed in the flat until the spring of 2026
and opened on 1 July 2026 as the Biblioteca Eco in Palazzo Poggi, its rooms laid out by
subject as Eco kept them, with over 32,000 volumes.

- **Live site:** https://eco-library-map.netlify.app
- **Artifact copy:** https://claude.ai/code/artifact/00e252bd-d0b3-4cde-96b1-64f01cafc827

## What the page does

The page is a single self-contained HTML file built on three.js. You can orbit the whole
flat or walk through it at eye level, click any book for its sources, its description and
how certain its position is, and follow one of fourteen guided tours: the books behind the
novels and the essays, the rare room, the comics and the feuilletons, each stop quoting Eco
where he wrote or spoke about the book. A room-by-room walk gives the family's words about
each room. An index lists Eco's own copies whose catalogue records note a dedication,
marginalia, underlinings, dog-ears, inserted papers or the ex-libris stamp the heirs
applied, and two colour modes read those notes across the shelves: the marks in Eco's hand,
and the copies inscribed to him, with the giver named. The furniture, the piles, the
artworks and the curiosities the films show open with a crop from the film and a link to
the second they appear, and every book seen on camera links to the video at that second.

The shelves can also be coloured by language, certainty, subject, source, century, and by
whether the footage shows the bookcase at all; the bookcases the films never show are drawn
in fog. The certainty view sorts every book and object into three tiers, certain, guess and
unknown, with filters to show only one tier, and every panel names the tier and the reason
for it.

A first visit opens on a card with three doors: the tours, the walk and the plan. The
address carries where the visitor is (a book, a tour and its stop, a room, the walk, the
English titles, the colour and the filter), so the browser's back button and a copied
address open on the same view. Search finds a book by its title, author, subjects,
description, giver, inscription and marks, and finds the tours and the objects too; "Any
book" opens one at random.

**English titles.** Each book's own title, in the language it was printed in, is the
default and is never replaced. With the English button on, an English title is shown
wherever a title appears and the own title stays beneath it. Where a published English
edition or a standard English title exists, that is what the page shows; otherwise a literal
translation made for this map, marked as such so nobody goes looking for an edition that
does not exist. Descriptions in Italian, French, Spanish or German have English versions
marked "translated here".

**Walking with the keys.** The arrow keys move you through the flat in both views: up and
down walk forward and back, left and right turn on the spot, W A S D do the same with
sidesteps, and Shift hurries. You stay inside the rooms and doorways and slide along shelves
and furniture rather than passing through them. On a phone, a joystick does the walking.

## What is in the map

Counts from the About panel and the footer of the published page:

| | |
|---|---|
| shelf slots | 27,415 in 6 rooms and 57 bookcases; the living-room vitrines and the curiosity cabinet are drawn with their objects and hold no slots; 28 records lie on the "not yet shelved" table, and the 104 Braidense records of the ECO.04 section stand as reference entries on a reference table in the study |
| identified books | 5,247 (the reference entries are not counted) |
| by origin | 354 read from film, 30 seen in photographs, 4,863 from catalogues, 22,196 unidentified |
| by placement | 1,814 catalogued (shelfmark), 220 seen (a reader named the bookcase), 3,185 inferred (room or subject level), 28 unshelved, 104 reference entries, 22,196 filler |
| certainty tiers | 1,592 certain, 3,759 guess, 22,196 unknown (a Braidense ECO.02 or ECO.03 record names a section of the catalogue, not a shelf, so it is a guess); objects 94 high, 36 medium, 3 low confidence |
| catalogue records | 2,105 Braidense, of which 1,816 (sections ECO.01 to ECO.03) are drawn as spines, 185 are set records drawn through their volumes' own records, and 104 belong to ECO.04, the section the library created to gather Eco's own publications for research; 3,047 Bologna, 28 of them with no subject match, laid on the unshelved table |
| with a public description | 2,264 |
| copy notes (Bologna records) | 1,014 dedications to Eco and 6 he wrote himself, 860 with the words transcribed, 1,698 with marginalia, 1,659 underlined, 1,403 dog-eared, 695 with inserts, 2,607 with the ex-libris stamp |
| notable books, books in piles, objects | 154, 112, 133 |
| the piano | 12 piles stacked pile for pile from the film's pull-back (6 on the lid, 6 on the keyboard shelf), 118 books, 86 identified and 32 blank spines, each pile linked to the film |
| on film | 26 of 57 bookcases have direct film evidence; 31 are drawn in fog |
| guided tours | 14 tours and 261 stops, every stop a book on the shelves but four (a bookcase and three comic piles); 96 stops quote Eco or his family word for word from a named, linked source, and 47 show a public-domain or Creative Commons picture of the book |
| English titles | 4,408 of the identified books: 819 titles of published English editions or standard English titles of classical works, 3,589 literal translations made for the map; 1,718 descriptions translated |

A record is a catalogue entry, never a count of volumes: a set record stands behind its
volumes, works bound together share a shelfmark, and the ECO.04 entries are references.
Every book carries its origin, its placement and its certainty tier, so the map is honest
about what is known: the rare-book room is catalogued shelf by shelf, the working library is
mostly subject-level placement, and the unidentified slots are drawn as anonymous spines.

## Sources

- **Biblioteca Nazionale Braidense OPAC**, fondo Umberto Eco: 2,105 records with shelfmarks
  ECO.01 to ECO.04, exported in UNIMARC and flattened to CSV
  (`eco-sources/braidense_eco_all.*`). The catalogue documents the transferred collection
  and its ordering. Its ECO.04 section brings together publications by Eco for research and
  does not by itself establish a copy's original position in the flat.
- **University of Bologna SBN-UBO catalogue** (SebinaYOU): the 3,047 records with possessor
  "Eco, Umberto" at the Biblioteca Universitaria, with the notes on Eco's copies (inventory
  number, dedications, underlinings, ex-libris), harvested with
  `eco-sources/scripts/bologna_harvest.py` into `eco-sources/bologna_eco_modern.jsonl`.
- **Fondazione Umberto Eco**, "Le biblioteche": the bookcase-by-bookcase photographic survey
  with subject captions for bookcases A to S. Its captions drive the subject placement of the
  Bologna records and the shelf-letter layer.
- **Video.** The 2015 *Codice Italia* footage ("Umberto Eco, Sulla memoria", the corridor
  walk), the 2022 documentary *Umberto Eco: La biblioteca del mondo*, its trailers, news
  clips of the Braidense and Bologna rooms, and two Louisiana Channel interviews: twelve
  videos, listed in `eco-video/videos.json`. Frames were cut every two seconds and the
  spines read frame by frame (`eco-video/spines_*.jsonl`), the whole 2022 film a second time
  at five frames a second (`eco-video/dense/`), and the readings consolidated into
  `eco-video/books_by_wall_eco.json`. The 2015 footage exists only at 480p, so most legible
  spines come from the 2022 film.
- **Photographs.** The Fondazione's survey images, the room photographs published by
  CriticaLetteraria and Curti Parini, Andrea Zanni's 2010 photographs, and press images.
  `eco-sources/eco-photos/sources.json` lists each with its address, credit and what can be
  read in it; the photographs themselves are not in the repository, apart from Zanni's,
  which he released under CC BY-SA.
- **Eco's own words** about the library, from his essays, interviews, *This Is Not the End
  of the Book* and the films, collected with citations in
  `eco-sources/experience/quotes.json`, and Nuovo and Coletto's 2022 article on the 36
  incunabula in AIB studi (`eco-sources/aib_224.pdf`).

## How the map is made

The rooms and bookcases are reconstructed in `eco-video/layout.json` from the Fondazione's
survey, the films and visitor accounts; no floor plan of the flat has been published, and
`eco-video/layout.md` says what each measurement rests on. The living room is drawn at its
footage size, with the plaster statue beside the first of three free-standing glass vitrines
whose contents are modelled from the film, and the study's free-standing units stand across
the room as the film shows them; the evidence is in `eco-video/salotto/` and
`eco-video/studio/`.

Each shelf slot is filled by the strongest evidence available. A spine read in the footage
or a photograph is placed where it was seen, with the bookcase named by the reader or by
the frame's context. A Braidense record is placed by its shelfmark in the rare room's own
order. A Bologna record is placed by the subject its cataloguers gave it, through the rules
in `eco-map/subject_map_eco.json`, which follow the Fondazione's captions for each bookcase.
Every slot that no identified book fills holds an anonymous spine, so the shelves look as
full as they were. Objects come from an inventory of the footage
(`eco-video/objects_from_video.json`) with hand-written rules in
`eco-map/objects_map_eco.json` for where each stands and which frame shows it.

Book descriptions come from Wikipedia, asking the edition of each book's own language
before English. Where no article on the book exists, one sentence about the author is given
instead and marked as such; a validation step rejects truncated texts, wrong articles and
editors mistaken for authors. `eco-map/README.md` explains the matching rules and the
pipeline, and `eco-map/schema_eco.md` describes every field of the data file the page reads.

The tours are written in `eco-map/tours_eco.json`. A stop is a book, an object, a bookcase or
a room: in the orbit view the camera flies to it, in the walk view the visitor is stood at a
station in front of it and the arrow keys keep walking. Each caption is an exhibition label,
and each quotation is word for word from a named, linked source: the *Paris Review*
interview, *This Is Not the End of the Book*, the Tanner and Borges lectures, essays and
columns, the Louisiana Channel interviews, the family's words in the 2022 film and at the
Braidense. Where a free copy exists on Wikimedia Commons the card shows a picture of the
book, credited.

## Layout of this repository

| folder | contents |
|---|---|
| `eco-map/` | the page (`index_eco.html`), the generator and the build, preview and test scripts, the mapping tables, `books.json`, the description files, the English titles and descriptions, the tours and their pictures, the vendored three.js, `dist/` with the built pages, and `schema_eco.md` |
| `eco-video/` | the room and bookcase layout (`layout.json`), the spine readings per video and the dense pass, the consolidated book list, the objects inventoried from the footage, the twelve piano piles, the list of videos, and the frame-cutting and consolidation scripts |
| `eco-sources/` | the Braidense and Bologna exports and harvest scripts, the list of public sources, the list of photographs, the article on the incunabula, and `experience/` (quotations, objects, notable books, incunabula, the arrangement of the rooms) |
| `netlify/` | the staging and deploy scripts and the site record for the Netlify site |

Not in the repository: the videos and the frames cut from them, the room photographs (other
than Zanni's), the films' subtitles and download metadata, the Wikipedia lookup cache, and
the full texts of the two copyrighted works the research read (Eco and Carrière's book and
the *Paris Review* interview). `.gitignore` keeps them out of a working copy's commits.

## Rebuilding the map

The scripts find each other by the folder layout above, so run them from a checkout of this
repository. Python 3 with Pillow (for the object thumbnails and the tour pictures) is enough
for the first two steps; the page checks need Playwright with Chromium.

```sh
cd eco-map
python3 gen_books_eco.py --piano-ref ../eco-video/piano_piles.json   # reads ../eco-video and ../eco-sources, writes books.json, prints the placement report
python3 check_piano.py       # confirms the twelve piano piles against the film reading
python3 build_eco.py         # dist/eco-map.html (self-contained), dist/eco-map-artifact.html, dist/index.html + books.json + vendor/
python3 test_page_eco.py     # headless Chromium page checks (about an hour and a half), writes screenshots/
```

The generator prints the counts by origin, placement and room, the rejected spine readings,
the objects it placed automatically, the unmatched notable books and the unplaced
quotations. Edit the mapping tables (`wall_map_eco.json`, `subject_map_eco.json`,
`objects_map_eco.json`, `quotes_eco.json`, `tour_eco.json`, `tours_eco.json`,
`walk_eco.json`) and rerun. Because the film frames and the room photographs are not in the
repository, a run from a fresh clone warns that the thumbnail frames are missing and leaves
the objects without their thumbnails; the committed `books.json` was generated with them
present and carries the thumbnails.

The description pipeline (`convert_braidense.py`, `convert_bologna.py`,
`prewarm_summaries.py`, `fetch_descriptions_eco.py`, `expand_*.py`) is documented in
`eco-map/README.md`. It talks to Wikipedia, which allows about 500 requests an hour per
address, so a full run takes many hours; its outputs (`descriptions_eco_*.json`) are
committed and merged on rebuild, so you do not need to run it to rebuild the page. The two
`convert_*.py` scripts read the catalogue exports from the path in their `SRC` constant;
point it at `../eco-sources/` when running from a checkout.

To recreate the spine readings from scratch, `eco-video/README.md` has the download,
frame-cutting and dedupe commands, and `eco-video/build_books_by_wall_eco.py` consolidates
the readings.

## Redeploying

`netlify/README.md` has the three steps: stage the page with `netlify/stage.py`, get a
one-time upload command from the Netlify tooling for the site in `netlify/sites.json`, and
run `netlify/deploy.sh`, which uploads, waits for the site to serve the new page and checks
it in headless Chromium. No Netlify token is stored in this repository.

The artifact copy is republished by uploading `eco-map/dist/eco-map-artifact.html` as a new
version of the artifact at the address above.

## Licence and rights

The work made for this map is released under the MIT licence (`LICENSE`), copyright 2026
Ethan Mollick. The catalogue records, the Wikipedia descriptions, the pictures from Wikimedia
Commons, the quotations and the films the map was built from belong to their libraries,
authors, photographers and producers and keep their own terms; `NOTICE.md` says what each is
and under which terms it is used here.
