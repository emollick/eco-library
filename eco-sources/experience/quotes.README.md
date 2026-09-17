# quotes.json

67 quotations about Umberto Eco's library (ids q01 to q67), a plain JSON array. The text of each quotation is verbatim from the source named in its record; nothing is edited except the auto-caption clean-ups, which `notes` records.

## Fields (every record has exactly these 14 keys)

| field | type | meaning |
|---|---|---|
| `id` | string | `q01` to `q67`, stable |
| `text` | string | the quotation in its original language, untouched |
| `language` | `it` or `en` | language of `text` |
| `translation` | string or null | English translation when `text` is Italian (working translations made for this project, not published ones, unless `notes` says otherwise); null when `text` is already English |
| `speaker` | string | who said it: Umberto Eco (50 records), Carlotta Eco, Nassim Nicholas Taleb, Riccardo Fedriga, Renate Ramge, James Bradburne, Fondazione Umberto Eco, journalists, film voice-overs |
| `source` | string | bibliographic citation (book, interview, film with caption time) |
| `url` | string | where the text was read; may carry a note in parentheses |
| `timestamp_s` | integer or null | seconds into the video for spoken lines; null when the source is not a video. For the film zZEy10fpq3I the value is the caption start time on the YouTube clock (no frame-label correction needed) |
| `video_id` | string or null | YouTube id: zZEy10fpq3I (2022 film, 18 records), Hq66X9f-zgc / zj1kwT87ne0 / B-M8V0PcCrw (Sulla memoria 2015), ygvl-_gtAP8 (subtitled clip), M8IWTOFNlOc (Louisiana Channel) |
| `topic` | string | one of read-them-all, antilibrary, the-library-as-tool, arrangement-by-subject, room-order, corridor-walk, rare-books, collecting, reading-habits, lists-and-memory, other |
| `room` | string or null | the room the quotation speaks of: salotto, vestibolo, corridoio, corridoio-arte, studio, antichi; null for general statements (32 records) |
| `bookcase` | string or null | a `books.json` bookcase id (`study-Q`) or a Fondazione letter when only that is known (`A` = the corridor case, corridor-01..25); null otherwise |
| `verification` | string | verbatim-from-source (34), auto-caption (21, Italian YouTube auto-captions, cleaned only where certain), quoted-in-secondary-source (11), paraphrase (1) |
| `notes` | string or null | context, caption corrections, and a `Research placement: '...'` line when the placement in words says more than `room` and `bookcase` do |

Placement counts: antichi 18, corridoio 12, studio 5, unplaced 32. Bookcase: A 6, study-Q 1.

For `gen_books_eco.py` (`--experience`): the generator reads `target`, `text_it` and `where`; derive `target = bookcase or room`, `text_it = text if language == 'it'`, `where = {video_id, timestamp_s, url}`; letters such as `A` resolve through `wall_map_eco.json`.

## The 8 display picks

1. **q02** (read-them-all, Italian original, Come giustificare una biblioteca privata 1990/1992): the three answers, ending "No, questi sono quelli che debbo leggere entro il mese prossimo, gli altri li tengo all'università". English: q03 (Weaver) or q09 (Carrière conversation). Place: the entrance (salotto door).
2. **q24** (corridor-walk, Spiegel 2009): "I have a hallway for literature that's 70 meters long. I walk through it several times a day, and I feel good when I do." Place: corridoio, bookcase A.
3. **q08** (antilibrary, Taleb 2007): "Read books are far less valuable than unread ones ... Let us call this collection of unread books an antilibrary." Place: any unlabelled shelf; entrance.
4. **q29** (the-library-as-tool, De Bibliotheca 1981): "la funzione ideale di una biblioteca è di essere un po' come la bancarella del bouquiniste ... libera accessibilità ai corridoi degli scaffali". Place: shelves in general, corridor.
5. **q11 / q20** (rare-books, Carrière 2009 / Paris Review 2008): "It is a Bibliotheca Semiologica Curiosa Lunatica Magica et Pneumatica ... I have Ptolemy, who was wrong ... but not Galileo, who was right" and "I prefer lunatic science." Place: antichi. Italian wording: q12.
6. **q31** (film 00:01:55): "La biblioteca è effettivamente simbolo e realtà di una memoria collettiva ... vede Dio come la biblioteca delle biblioteche". Place: corridoio, the opening walk.
7. **q46** (Carlotta Eco, film 00:44:09): "era una cosa viva: non era un archivio". Place: corridoio; the arrangement legend.
8. **q26** (lists-and-memory, Spiegel 2009): "We like lists because we don't want to die." Alternative for the entrance: **q36** (film 00:08:40, evicted because the shelves threatened the walls).

Other lines worth using: q15 (secretary forbidden to catalogue; re-sorting per project), q38 (vegetal memory, 00:09:36), q43 ("non fatevi ricattare", 00:34:06), q44 (curiosity, 00:41:01), q45 (Carlotta on the corridor order, 00:43:09), q63 (Fedriga: the literatures converging on the feuilleton), q60 (the family on the Stanza degli antichi), q34 (the rare-room section labels read aloud, 00:07:00).

## Not recorded

The popular English line "a library is not a place where you go to read books but a place where you go to find books you haven't read" has no primary source with this wording. The closest genuine texts are q29 (1981) and q05 (2007).
