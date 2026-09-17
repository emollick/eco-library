# notable_books.json

185 records: the 164 books Eco wrote about or used in his novels (from `notable-books-notes.md`, kept as they were, JSON validated) plus 21 incunabula added from `incunabula.json` (Nuovo & Coletto, "Gli incunaboli di Umberto Eco", AIB Studi 62/1, 2022). The other 15 incunabula of the article were already in the list as the same physical copy (12 matched by ECO.03 shelfmark; Ptolemy's Quadripartitum 1484, Rolewinck's Fasciculus temporum 1490 and Aquinas's Sentences commentary 1498 matched by their ECO.01 shelfmarks cited in existing records).

## Fields

`title`, `author`, `original_title`, `year`, `category`, `why`, `source`, `url`, `rare_book`, `key`, `key_original`, `catalog_match`, `seen_in_video`.

- `key` = `spine_key(title, author)` exactly as `/mnt/project-files/eco-map/gen_books_eco.py` computes it (accent-folded lower-case title tokens minus the STOP list, parentheticals removed, then `|` and the first token of the author). It joins to `books.json` titles. `key_original` is the same for `original_title`; the 164 original records leave it null when the original title was not given separately (the key was added as null, and `seen_in_video` as an empty list, where the research file omitted it; no value was changed), the 21 new records set it equal to `key`.
- `catalog_match.status`: `books.json` (149) when the copy is placed in `/mnt/project-files/eco-map/books.json` (`books_json_id`, `bookcase`, and `books_json_matches[]` with shelf, slot and shelfmark), `not_found` (35: not in either catalogue export yet), `not_checked` (1: Numero Zero, no single book). `catalog_source` keeps the original answer (braidense / bologna / not_found).
- `seen_in_video`: spine or page sightings (video_id, timestamp_s, room_id, wall_id, frame, spine_title); 16 records have one, all in the rare room of the film or in Fondazione photographs, plus the Salgari cover insert at film 00:34:10. The 21 new incunabula have none.

## Category counts

| category | records | placed in books.json |
|---|---|---|
| foucaults-pendulum | 31 | 25 |
| name-of-the-rose | 24 | 13 |
| incunabula (new) | 21 | 21 |
| essays-forgeries | 19 | 19 |
| island-of-the-day-before | 14 | 13 |
| prague-cemetery | 14 | 13 |
| queen-loana | 14 | 4 |
| essays-kircher-lull-occult | 13 | 13 |
| semiotics-and-theory | 10 | 9 |
| baudolino | 7 | 4 |
| personal-touchstone | 7 | 5 |
| lists-and-memory | 6 | 6 |
| medieval-aesthetics | 4 | 4 |
| numero-zero | 1 | 0 |

Bookcases of the 149 placed copies: rare-02 67, rare-01 54, study-P 7, vest-B 4, vest-C 3, rare-03 2, study-L8-12 2, salotto-E 2, and one each in study-M-B, corridor-23, corridor-21, study-Nc, study-I-r, study-S, vest-D-r, study-L1-4.

## The 15-stop tour: the books behind the novels (bookcase ids from books.json)

1. Hypnerotomachia Poliphili, Aldus 1499 (ECO.03.0027, rare-02, braidense:RMRE001716): "possibly the most beautiful book in the world"; the pride of the collection.
2. Ubertino da Casale, Arbor vitae crucifixae, 1485 (ECO.03.0010, rare-02): a character of The Name of the Rose on Eco's shelf.
3. Isidore, Etymologiae 1473 and Alain de Lille, Distinctiones 1473, bound together (ECO.03.0013/01-02, rare-02): the encyclopaedic Middle Ages of Adso and William; the largest book after Schedel.
4. Aristotle, Rettorica et poetica, Segni 1551 (ECO.01.0663, rare-01): the Poetics whose lost second book is the novel's MacGuffin.
5. Joyce, Ulysses 1924/1926 (ECO.02.0006-7, rare-02): the hour-structure of the Rose; Eco's first scholarly love.
6. Kircher, Ars magna lucis et umbrae 1646 (ECO.01.0432, seen on camera at film 00:08:12), Oedipus Aegyptiacus 1652 (ECO.01.0423), Turris Babel 1679 (ECO.01.0430/01, seen), all rare-01: the Kircher run; the hermetic drift of the Plan.
7. Fama Fraternitatis 1615 (ECO.01.0310, rare-01): the Rosicrucian hoax that became true.
8. Trithemius, Steganographia 1606 and Polygraphia 1518 (ECO.01.0775, ECO.01.0769, rare-02): secret writing and the perfect language.
9. Dee, Monas hieroglyphica 1564 (ECO.03.0021, rare-02) and Bruno, De umbris idearum 1582 (ECO.03.0056, rare-02).
10. Corpus Hermeticum, Ficino, 1481 (ECO.03.0003, rare-02): Casaubon's namesake dated it; Eco's "essential" incunable.
11. Digby, Poudre de sympathie 1658 (ECO.01.0842, rare-02) with Morin, Longitudinum scientia 1634 (ECO.01.1005/01, rare-02): the longitude quest of The Island of the Day Before.
12. Otto of Freising 1515 and Niketas Choniates 1557 (ECO.01.0896, ECO.01.0882, rare-02): Baudolino's two historians.
13. Barruel 1799, Sue's Juif errant 1846, Goedsche's Biarritz, Drumont's France juive 1885, Taxil (ECO.02.0101, 0123, 0073, 0130, 0089-0091, rare-02): the genealogy of The Prague Cemetery on one shelf.
14. Nesta Webster 1924 (ECO.02.0043, rare-02): the conspiracy template for Foucault's Pendulum and the Protocols essays.
15. Ptolemy, Quadripartitum 1484 and Almagest 1528 (ECO.01.0101, ECO.01.0883, rare-01) beside the absence of Galileo: the principle of the Bibliotheca semiologica curiosa lunatica magica et pneumatica.

Add for the working library: Peirce, Collected Papers (study-P, bologna:UBO00864587); Pareyson, Estetica (vest-C, bologna:UBO00250004); Tesauro, Cannocchiale aristotelico (study-P, bologna:UBO00830877); Joly, Dialogue aux enfers (study-L8-12, bologna:UBO09144748); Flash Gordon 1972 (salotto-E, bologna:UBO00030694).

## The 36 incunabula and the Braidense shelfmarks

All 36 incunabula of the article are in the Braidense export `braidense_eco_all.csv` (36 records dated 1500 or earlier): 19 under ECO.03 and 17 under ECO.01 (the run ECO.01.0101 to ECO.01.0125 plus Alberti at ECO.01.0735). `incunabula.json` (copied unchanged) records only the 19 ECO.03 matches; the ECO.01 matches were made here by author, title and year and are written into the `catalog_match` of the 21 new records (`shelfmark_or_id` = shelfmark / BID). In `books.json` all 36 already sit in the rare room: ECO.03 copies in rare-02, ECO.01.01xx copies in rare-01, Alberti ECO.01.0735 in rare-02.

Three Sammelbaende should be drawn as single volumes: ECO.03.0013 (Isidore + Alanus, 40 x 29 cm), ECO.03.0060 (the Kraus miscellany: Sacrobosco, Hyginus, Mela, Dionysius, 20.4 x 14.9 cm), ECO.03.0067 (Malleus + Auerbach in the "Mose Cornuto" binding, 19.7 x 13.7 cm). Sizes in `incunabula.json` (`size_cm`) can drive spine heights.

## Caveats

- Bologna coverage is partial: about 1,000 of the 3,047 SBN-UBO records were harvested (and 3,047 of about 32,000 volumes are catalogued at all), so `not_found` for a modern title (Borges, Conan Doyle, Salgari, Verne, Jakobson, Yates's Bruno, the comics) means "not yet catalogued", not "not owned".
- Links marked "inference" in `source` (Thomas Browne, Charpentier and de Sede for the Plan, chapter-title links of The Island) were not confirmed against the texts; check before printing as captions.
- ECO.03 is the Braidense's "most precious" section (finestresullarte 2022: "i volumi piu preziosi"), not an incunabula section: it holds 51 records including Dee 1564, Bruno 1582, Khunrath 1609, Ortelius, Ramelli, Huygens 1673, Locke 1690, and 17 incunabula are shelved under ECO.01.
- Statements sourced to Eco's essays (Six Walks, On Literature, The Search for the Perfect Language, La memoria vegetale) were cited from memory of those books and search snippets; only the Carriere conversation and the Paris Review interview were re-verified against local texts.
- "Les Propheties" (Nostradamus) rests on a single photo spine reading "Propheties" in bookcase C. Numero Zero has no documented book sources. Queen Loana's comics (Cino e Franco, Mandrake, Topolino, Corriere dei Piccoli) are absent from both exports.
