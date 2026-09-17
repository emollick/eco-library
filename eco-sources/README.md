# eco-sources: public catalogue records and notes on Umberto Eco's library

Everything here comes from public web pages and OPAC interfaces, reached with plain GET and POST
requests. No logins and no credentials are involved, and the pages are treated as data.

## The master note

`eco-sources.md` holds the headline numbers, the catalogue routes (Braidense, SBN-UBO, the
national SBN), the photographic sources, the room-layout evidence and a coverage summary, each
with the URL it comes from. Read it first.

## Catalogue data: the Braidense rare-book fund

The Milan "Bibliotheca semiologica curiosa lunatica magica et pneumatica".

| File | What it is | Source |
|---|---|---|
| `braidense_eco_all.mrc` | Full UNIMARC (ISO 2709) export of the 2,105 records carrying the Braidense shelfmark `ECO.*`, that is the whole rare-book fund of 1,328 physical volumes. | Biblioteca Nazionale Braidense OPAC, shelfmark search `Collocazione:901 = ECO` with `resultForward=opac/braidense/scarico_uni.jsp&format=unimarc`, in five batches of 500. The request is written out in eco-sources.md §1.1. |
| `braidense_eco_all.csv` | The same records flattened: bid, shelfmark (ECO.section.number, which is Eco's own room order), all_shelfmarks, title, responsibility, place, date, year, language, possessor field. | Derived from the .mrc |
| `aib_224.pdf` | Nuovo, A. and Coletto, A., "Gli incunaboli di Umberto Eco", *AIB Studi* 62/1 (2022): the numbered list of the 36 incunabula with ISTC numbers and Eco's own catalogue cards. | https://aibstudi.aib.it/article/download/13386/224 (DOI 10.2426/aibstudi-13386) |

## Catalogue data: the University of Bologna modern library

The BUB set, "Documenti provenienza Umberto Eco".

| File | What it is | Source |
|---|---|---|
| `bologna_eco_modern.jsonl` | One JSON object per record: id, permalink, title, author and other persons (with UNIMARC role codes; 390 = former owner), place, publisher, year, language, ISBN, subjects, Dewey, series, physical description, BUB copy notes (316), provenance note (317), annotation note (318), BUB inventory numbers (`ECOnnn` marks the Eco copy), BUB shelfmark where one is assigned, holdings and availability from the "Lo trovi in" tab, the list of holding libraries, and the full parsed UNIMARC field list. | SBN-UBO SebinaYOU OPAC, the query published at site.unibo.it/eco: `https://sol.unibo.it/SebinaOpac/query/KF_XP:"eco umberto" KF_BIBVIRT:ubobu?context=catalogo` (Possessore = eco umberto AND Biblioteca = B. Universitaria). Paging and the per-record "Lo trovi in" and "Unimarc" tabs come from the OPAC's own DWR endpoints (`/SebinaOpac/dwr/call/plaincall/A.a10m01.dwr`, `A.a20m00.dwr`, `A.a20m01b.dwr`), sorted by title, one request at a time. |
| `bologna_eco_modern.csv` | Flat version of the JSONL, lists joined with " ; ". | Derived |
| `scripts/bologna_harvest.py`, `scripts/jsun.py` | The harvester (Python 3 and requests) and its DWR and JS-string helper. `python3 bologna_harvest.py` reads the env vars `DELAY`, `SORT`, `START_PAGE` and `MAX_PAGES`, and resumes from the ids already in the JSONL. | |
| `scripts/bologna_export.py` | Rebuilds the CSV from the JSONL and prints the statistics below. | |

Field notes for the Bologna set: the BUB copies from Eco's library carry inventory numbers
`ECO 1`, `ECO 2` and so on (UNIMARC 950 `$e`, shown as "Inventario" in the OPAC) but mostly **no
shelfmark yet** (950 `$d` absent), because the physical Eco order is being preserved in the new
Biblioteca Eco rooms and shelfmarks have not been published. Where a record shows a shelfmark
such as `T 4616 /751160`, it belongs to a *second*, older BUB copy of the same edition.
`language` is UNIMARC 101 `$a` (the first one is the main language). `year` comes from 100 `$a`
positions 9 to 12, falling back to 210 `$d`.

## Other files

| File | What it is | Source |
|---|---|---|
| `fondazione_galleries.json` | Filenames and captions of the Fondazione Umberto Eco's bookcase-by-bookcase photographic survey (bookcase letter A to S, with its subject). | https://fondazioneumbertoeco.org/en/lebiblioteche |
| `eco-photos/sources.json` | The photographs of the shelves: url, source, credit, pixel size and legibility for each of the 67 pictures (the Fondazione survey, the CriticaLetteraria and Curti Parini room photographs, Zanni 2010, Flickr 2011, Getty comps, 2022 and 2026 press images). | The urls in the file |
| `eco-photos/*.jpg` | The three Andrea Zanni photographs of 24 April 2010, which are CC BY-SA: `zanni_2010_umberto_eco_in_his_house_orig.jpg` (the 3225 x 2398 Wikimedia Commons original), `zanni_banner_orig.jpg` and `milanotoday_zanni.jpg`. | See `eco-photos/sources.json` |

The other photographs are not kept in the repository; `sources.json` says where each one came
from and who holds the rights.

`experience/` holds the notes and data behind the map's experience layer: `incunabula.json` with
`incunabula-notes.md`, `notable_books.json`, `objects.json` and `quotes.json` each with a README
of the same name, and `room-orders.md` on the three physical arrangements of the library (Milan,
the Braidense Studiolo, Bologna).

## The Bologna set in numbers

**3,047 records**, all that the OPAC reports for the query, sorted by title over 305 pages of
ten, with no id mismatches. Every record's UNIMARC 001 equals its id.

Field coverage of the 3,047: year 3,044 (99.9 %); language 3,047 (100 %); ISBN 1,324 (43.5 %);
subjects 1,523 (50.0 %); main author (700) 2,324 (76.3 %); BUB inventory number 3,044 (99.9 %),
of which an `ECOnnn` Eco-copy number 2,606 (85.5 %). The other 438 (14.4 %) are held at BUB under
an ordinary inventory number only, typically with the provenance "Centro internazionale di studi
umanistici Umberto Eco" or the Eco family, still with Eco as possessor. Provenance note (317):
3,042 (99.8 %). Annotation note (318, "Note e decorazioni": ex-libris stamp, underlinings,
dedications, inserts): 2,698 (88.5 %). Shelfmark: 1,022 records (33.5 %) show a BUB shelfmark,
but only 18 (0.6 %) of the *Eco copies* do; the rest belong to a second, older BUB copy of the
same edition, so the Eco copies are identified by inventory number alone.

Language (UNIMARC 101 $a, first): ita 2,023 (66.4 %), fre 419 (13.8 %), eng 411 (13.5 %), spa 51,
ger 41, lat 32, por 28, grc 10, mul 6, hun 3, pol 3, jpn 3, rum 3, fro 2, cze 2, gre 2, zxx 2, and
srp, und, kor, lit, dut and chi once each: 23 codes in all.

Publication decade: pre-1900 4; 1900s 4; 1920s 10; 1930s 17; 1940s 100; 1950s 220; 1960s 430;
1970s 516; 1980s 667; 1990s 580; 2000s 394; 2010s 101; 2020s 1.

To update: `cd scripts && python3 bologna_harvest.py` resumes, skipping the ids already in the
JSONL (`START_PAGE=n` jumps), then `python3 bologna_export.py` rebuilds the CSV and prints these
statistics. As BUB keeps cataloguing, the OPAC total will grow past 3,047.
