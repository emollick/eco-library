# books.json for the Eco library map: schema

The page (`index_eco.html`, built into `eco-map.html`) computes every world position from this file. A regenerated
dataset needs no page edits. The top level is `meta`, `rooms[].bookcases[]`, `objects[]` and `books[]`, with the fields
described below. `gen_books_eco.py` writes the file. Everything is data; nothing in these files is executed.

Lengths are metres, angles degrees. World coordinates are absolute: a room sits at its `origin`, and every bookcase,
object and book position is already in world metres. Shelf 0 is the top shelf; slot 0 is the left-most book facing the
unit (`meta.shelf_convention`).

A field whose value would be null or an empty list is dropped before the file is written, on books and on objects. An
absent key therefore means "not known" or "not applicable", and only `bookcase`, `shelf`, `slot` and `section` are
written as null, on the unshelved and reference entries. Fields marked optional below appear only where they apply.

```jsonc
{
  "meta": {
    "library": "Umberto Eco's library, Piazza Castello 13, Milan (the apartment as it stood before the rare books went to the Braidense in 2021 and the working library to the University of Bologna in 2026)",
    "owner": "Umberto Eco (1932-2016)",
    "generated": "2026-09-17T13:52:19Z",           // when the file was written
    "dataset": "reconstruction from public photographs, visitor accounts, two library catalogues and the spine readings listed in sources; nothing was measured",
    "counts": {
      "books": 27547, "identified": 5247, "rooms": 6, "bookcases": 57,
      "by_origin": {"video": 354, "photo": 30, "catalog": 4863, "unlabelled": 22196},   // the reference entries are counted apart, in `reference`
      "by_placement": {"catalogued": 1814, "seen": 220, "inferred": 3185, "unshelved": 28, "reference": 104, "filler": 22196},
      "unshelved": 28,          // Bologna records no subject rule places: in books[] with no bookcase (see Bologna placement)
      "reference": 104,         // Braidense ECO.04 entries: on the study's reference table, never counted as identified
      "by_language": {"it": 2722, "fr": 1018, "la": 628, ...},    // ISO 639-1 codes, plus "unlabelled" and "unknown"
      "by_room": {"studio": {"name": "...", "slots": 13186, "bookcases": 17, "shelf_metres": 391.6, "by_origin": {...}, "by_placement": {...},
                             "by_source": {...}, "by_tier": {...}, "by_century": {...}, "by_language": {...}, "by_subject": {"<caption>": n},
                             "objects": {"pile": 15, ...}, "objects_by_tier": {...}}, ...},
      "with_description": 2264, "notable": 154, "in_piles": 112, "objects": {"artwork": 38, "pile": 30, ...},
      "notable_missing": 38, "notable_missing_with_nearest": 9,   // works Eco is known to have used that are in no public record (the tours' `missing: true` stops), and how many point at a same-author record
      "notable_missing_by_subject": 18, "notable_missing_room_only": 11,   // of those, how many the subject rules place on a bay, and how many only in a room
      "english_titles": {"books": 4408, "published": 819, "literal": 3589, "descriptions": 1718, "same_as_native": 6, "unmatched": 166,
                         "files": [{"file": "titles_en_eco.json", "entries": 4581}, ...],
                         "no_entry": {"total": 943, "catalog": 804, "video": 98, "photo": 13, "fragments": 28}},   // see English titles
      "display_cleaned": {"annotation": 1040, "author": 119, ...},    // see Display cleaning
      "reading_fixes": ["video:NtPk4irDiM8:65:bernini", ...],         // readings corrected by wall_map_eco.json reading_fixes
      "tiers": {"certain": 1592, "guess": 3759, "unknown": 22196, "by_room": {"studio": {"certain": 57, ...}, ...}, "by_bookcase": {"study-P": {...}, ...},
                "objects": {"certain": 125, "guess": 8}, "note": "...", "reasons": {"<tier_reason pattern>": n}},     // see Certainty tiers
      "by_source": {"video": 354, "photo": 30, "braidense": 1816, "bologna": 3047, "unlabelled": 22196},              // see Overlay counts
      "by_century": {"1400s": 36, ..., "2000s": 599, "unknown": 282, "unlabelled": 22196},
      "by_subject": [{"subject": "...", "subject_it": "...", "books": 1188, "identified": 171, "bookcases": ["study-I", "study-I-over"], "rooms": ["studio"]}],
      "on_film": {"bookcases_on_camera": 26, "bookcases_total": 57, "books_on_camera": 16745},
      "overlay_note": {"subject": "...", "source": "...", "certainty": "...", "century": "...", "language": "...", "on_film": "...", "hand": "...", "given": "..."},   // one line per overlay saying what it rests on (for About)
      "objects_thumbs": {"objects": 132, "bytes": 710748, "quality": 68, "artworks": 38, "no_frame": 1},
      "catalog": {
        "braidense_records": 1816,              // ECO.01 to ECO.03 records drawn in the rare-book cabinets
        "braidense_reference_records": 104,     // ECO.04 records on the reference table
        "braidense_set_records_not_drawn": 185, // set records that stand behind their volumes and hold no slot of their own
        "braidense_export_records": 2105,       // records in the export, before either subtraction
        "braidense_reconciliation": {"export_records": 2105, "set_records_not_drawn": 185, "records_with_parent_set": 590,
                                     "records_noting_works_bound_together": 322, "distinct_shelfmarks_eco01_03": 1459,
                                     "distinct_running_numbers_eco01_03": 1209, "shelfmarks_shared_by_several_records": 199,
                                     "braidense_volumes_at_transfer": 1328, "note": "..."},   // a record is a catalogue entry, not a spine
        "bologna_records": 3047, "bologna_placement_unknown": 28, "bologna_unshelved": ["UBO...", ...], "bologna_rules": {"<rule name>": n},
        "bologna_matched_via": {"record": 2978, "set title": 36, "responsibility": 5},        // see Bologna placement
        "bologna_rescued": [{"id": "UBO00923421", "title": "1", "set_title": "Arte della cucina ...", "rule": "cookbooks and gastronomy", "bookcase": "study-Oa", "how": "set title"}],
        "volume_titles": {"braidense": 594, "bologna": 257, "set within a set": 7, "without a set title": 1, "composed": {...}, "note": "..."},
                                     // numbered volumes whose display title was composed from the UNIMARC 461/462 set title. The top-level
                                     // counts are of the entries served; `composed` is the generator's own tally, which also counts set records
                                     // composed and then set aside, so it may run one higher
        "part_titles_from_responsibility": 2, "title_tails_cleaned": 4, "authors_from_set": {"braidense": 58, "bologna": 2, "note": "..."},
        "bologna_copies": {"with_copy_notes": 3046, "with_eco_inventory": 2606, "with_dedication": 877, "with_annotation_note": 2695,
                           "marks": {"underlinings": 1658, ...}, "with_inscription": 859, "inscribed": 1014, "with_named_giver": 870,
                           "givers": 503, "top_givers": [["Alberto Arbasino", 31], ...],    // distinct givers, and the twelve who inscribed most
                           "given": {"plain": 2026, "named": 870, "unnamed": 144, "eco": 6},   // the classes the "Given to Eco" legend paints
                           "inscribed_by_eco": 6,                                              // copies whose dedication is in Eco's own hand
                           "inscription_how": {"closed": 839, "unclosed": 18, "no-quote": 2},  // how the transcribed inscription was closed
                           "hand": {"0": 1107, "1": 237, "2": 282, "3": 1031, "4": 389}, "hand_any": 1939,   // copies by how many of the four kinds of mark in Eco's hand the note records (marginalia, underlinings, dog-ears, inserts; the ex-libris stamp is the heirs' and does not count)
                           "copy_notes_applied": [{"id": "UBO00189116", "dropped": ["Serao, Matilde"], "note": "..."}]}},   // the copy records copy_notes_eco.json qualified
      "spine": {"frames": 2405, "frames_by_level": {"bookcase": 560, "room": 556, "pile": 425, "subject": 186, "context": 18, "label": 4},
                "frames_unresolved": 0, "rows": 1720, "readings": 508, "consolidated": "books_by_wall_eco.json", "consolidated_books": 587,
                "deduped": 60, "merged_into_catalog": 81, "merged_same_bay": 4, "merged_across_piles": 6, "placed": 382, "unplaced": 0,
                "pile_deferred_only": 5, "author_only_placed": 17, "pile_fillers": 32, "alt_readings": 11, "alt_preferred": 2,
                "piles_with_height": 12, "pile_copies": 4, "pile_ref_*": n,     // the piano reference pass, see Spine-reading frames that become piles
                "dense_*": n,                                                   // the dense pass, see The dense spine pass
                "catalog_match_rejected": 31, "catalog_forced": 5, "catalog_forbidden": 0, "catalog_braidense_cross_room": 5,
                "catalog_moved_to_tag": 4, "pile_sightings_off_flat": 1, "reference_title_on_film": 10,
                "label_hits": {"<label_patterns regex or 'call tag Q'>": n},     // readings placed from a shelf label or call tag visible in the frame
                "rejected_other": [...], "frames_unresolved_labels": [{"room_id": "other", "wall_id": "...", "wall_name": "...", "frames": 4}],
                "video_files": [...], "photo_files": [...]},
      "estimate": {"milan_working_library_volumes": 33000, "moved_to_bologna_volumes": 32000, "rare_volumes_at_transfer": 1328,
                   "rare_records_drawn": 1816, "rare_reference_records": 104, "rare_export_records": 2105,
                   "slots_modelled": 27547, "slots_working_library": 25684, "slot_capacity_working_library": 25836, "slots_rare_room": 1835,
                   "shelf_metres_total": 911.3, "shelf_metres_working_library": 804.4, "mean_spine_width_m": 0.029, "note": "..."}
    },
    "sources": [   // rendered in About; kind: video | photo | catalogue | catalog | text | document
      {"id": "video-Hq66X9f-zgc", "kind": "video", "video_id": "Hq66X9f-zgc", "title": "...", "uploader": "...", "upload_date": "...",
       "url": "https://www.youtube.com/watch?v=...", "duration_s": 413, "books_seen": 4, "spines_file": true},
      {"id": "fondazione-galleries", "kind": "photo", "title": "A Fondazione Umberto Eco photograph (bookcase I)", "frame": "fondazione_17_I.webp",
       "url": "...", "credit": "...", "books_seen": 5},              // title is reader-facing; the file name stays in `frame`
      {"id": "braidense-opac", "kind": "catalogue", "title": "...", "url": "...", "note": "..."}
    ],
    "mappings": {"wall_map": "wall_map_eco.json", "subject_map": "subject_map_eco.json", "objects_map": "objects_map_eco.json", "quotes_file": "quotes_eco.json",
                 "tour_file": "tour_eco.json", "consolidated_books": "books_by_wall_eco.json", "video_objects": "objects_from_video.json",
                 "description_files": [{"file": "descriptions_eco_braidense.json", "entries": 2105, "used": 396, "applied": 334, "by_kind": {"author": 335, "article": 52, "search": 25}}],   // see Descriptions
                 "description_validation": {"rejected": 209, "by_reason": {"truncated text": 112, ...}, "cleaned": {"birth_year": 203, "ipa": 136, "truncation_cut": 14},
                                            "rejected_ids": [{"id": "...", "title": "...", "author": "...", "wikipedia_title": "...", "kind": "author", "reason": "...", "file": "..."}]},
                 "rare_spine_widths_m": {"rare-01": 0.0422, ...}},   // the spine width that makes each rare cabinet's records fill it
    "camera": {"video_id": "zZEy10fpq3I", "rooms_seen_seconds": {"salotto": 441.4, ...}, "bookcases_on_camera": 26, "bookcases_total": 57,
               "objects": {"objects": 247, "ingested": 158, "rule_placed": 125, "auto_placed": 2, ...},
               "auto_placed": [ /* objects placed without a rule, to check */ ], "note": "..."},
    "incunabula": {"files": ["incunabula.json"], "listed": 36, "matched": 36, "added": 0, "unmatched_bids": []},
    "warnings": [],              // the generator's list for the log; a run whose inputs are in order leaves it empty, and the About panel never prints it
    "layout_notes": ["..."],     // layout.json notes minus those addressed to the builder
    "layout_assumptions": {"bay_width_m": 0.8, "half_bay_width_m": 0.4, "full_height_m": 3.5, "low_unit_height_m": 2.1,
                           "shelf_pitch_full_height_m": 0.32, "volumes_per_shelf_metre": [33, 40], "bologna_density_volumes_per_metre": 53},
    "notes": ["..."],            // the reader-facing notes on origins, placements and the rare cabinets, printed in About
    "shelf_convention": "shelf 0 is the top shelf; slot 0 is the left-most book facing the unit",
    "tour": {"title": "A walk through the flat, room by room", "auto": false, "file": "tour_eco.json", "stops": [ /* see Tour */ ]},
    "tours": [ /* see Tours */ ], "walk": { /* see Walk */ }, "notable_tours": [ /* see Notable tours */ ],
    "quotes_general": [ /* quotes with no shelf; shown in About */ ],
    "brief": null,               // always null: a note file for the builder, if one sits in experience/, is never carried into this file
    "english_titles": true,      // at least one book carries title_en; the page shows its English button only then
    "experience": {"folder": ".../eco-sources/experience", "files_present": {"quotes.json": true, ...}, "piles": 30,
                   "quotes": {"placed": 67, "unplaced": [...]}, "tour_stops": 10, "tour_auto": false,
                   "video_quotes": n, "experience_quotes": n, "general_quotes": n, "experience_objects": {...},
                   "route_notes": n, "film_notes": n, "walk_waypoints": 13, "notable_tours": [...],
                   "notable": {"matched": 147, "unmatched": [{"title": "...", "author": "...", "category": "...", "status": "not among the catalogued or filmed books", "nearest_id": null}],
                               "rejected": [{"id": "bologna:UBO03415760", "title": "Ficciones", "record_title": "El Eco de la rosa y Borges", "reason": "the record is not the work (...)"}],   // curated ids refused by the work test (see Notable tours)
                               "books_flagged": 154, "join": "..."}}
  },
  "rooms": [
    {
      "id": "studio", "name": "The big study", "name_it": "Lo studio grande", "short_name": "Study", "order": 6,
      "blurb": "...", "description": "...", "size": [14.0, 10.0], "origin": [23.5, 10.3],   // size [w, d]; origin = the room's north-west corner in world metres
      "door": {"wall": "N", "from": 1.75, "to": 2.45},                     // the first door
      "doors": [{"wall": "N", "from": 1.75, "to": 2.45, "note": "doorway inside bookcase study-I"}],   // all doors; the page cuts the wall at each
      "windows": [{"wall": "W", "offset": 0.9, "width": 1.3, "height": 2.2, "radiator": true, "note": "..."}],   // from layout.json; offset runs from the wall's start on the room-origin side. A listed window is not free wall for a framed print
      "furniture": ["desk with computer near the E wall (...)", ...], "sources": ["fondazione-galleries", ...],
      "position_note": "...",                                             // layout.json note on where the room sits
      "seen_ranges": [[293.0, 305.5], ...], "seen_seconds": 362.0, "seen_video_id": "zZEy10fpq3I",
      "seen_first_url": "https://www.youtube.com/watch?v=...&t=293s",      // from objects_from_video.json rooms_seen
      "bookcases_on_camera": 4, "objects_on_camera": 21,
      "film_notes": [{"label": "...", "description": "...", "url": "...", "timestamp_s": 293}],   // experience objects of kind room / roomnote
      "shelf_metres": 391.6, "catalog_note": null,                        // catalog_note carries text only on the rare-book room
      "quotes": [ /* see Quotes */ ],
      "bookcases": [
        {
          "id": "study-I", "layout_id": "study-I", "label": "I · Ancient, Late Antique, and Ch… (left of door)", "long_label": "...", "order": 1,
          "wall": "N", "x": 24.38, "z": 10.46, "rotationY": 0, "width": 1.6, "height": 3.5, "depth": 0.32, "shelves": 11, "bays": 5,
          "kind": "wall",            // wall | low | island | cabinet | display (piles live in objects[], see below)
          "finish": "white",         // white | cherry | dark | steel: the page's shelving colours
          "y0": 2.22,                // only on door bridges (<id>-over): floor offset of the unit; the page hangs it over the doorway
          "is_door_bridge": true,    // only on <id>-over units
          "fixed_position": true,    // layout.json set x / z / rotationY outright, instead of the page running the unit along its wall
          "setback": 1.1,            // the unit stands this far in front of its wall, still facing the room (the salotto vitrines); objects anchored to it follow
          "subject": "Ancient, Late Antique, and Christian philosophy", "subject_it": "...",
          "fondazione_bay": "I",     // the Fondazione's shelf letter: the page draws it on the shelf edges (Layers > Letters) and names the bay by it
          "confidence": "high", "evidence": "...", "source_ids": ["fondazione-galleries"], "catalog_range": "ECO.01.0001-c.0700",   // catalog_range: rare cabinets
          "est_volumes": [1267, 1536], "glazed": false, "curio": false,
          "photo_url": "https://fondazioneumbertoeco.org/user/themes/quark/images/scrollwall/17_I.webp",
          "room_id": "studio", "quotes": [ /* see Quotes */ ],
          "on_camera": true,         // false = no reading, pile or inventoried object was ever placed on it: the page draws it in fog (Layers > Fog)
          "seen_in_film": [{"label": "...", "description": "...", "url": "...", "timestamp_s": 1234, "time": "00:01:45", "video_id": "...", "frame": "..."}],   // objects and shelf labels the film inventory attached to this bookcase
          "sections": [{"id": "study-I-s", "label": "<subject>", "topic": "<subject_it>", "blurb": "<evidence>", "shelf_from": 0, "shelf_to": 10}],
          "counts": {"slots": 572, "identified": 63, "by_source": {...}, "by_tier": {...}, "by_century": {...}, "by_language": {...}}   // see Overlay counts
        }
      ]
    }
  ],
  "objects": [   // non-shelf items; every one is clickable and opens the panel
    {
      "id": "obj:salotto:piano-pile-01", "room": "salotto",
      "kind": "pile",                // pile | desk | chair | sofa | piano | artwork | curiosity | lamp | ladder | glass_case | other
      "x": 6.195, "z": 6.79,         // world metres (the input files give them room-local, see below)
      "rotation": 180, "base_y": 1.23, "size": [0.22, 0.122, 0.16],       // size is [w, h, d] and is always present
      "label": "Piano lid, pile 1 of 6 (leftmost)", "description": "...", "source_url": "...",
      "video_id": "zZEy10fpq3I", "timestamp_s": 2583, "timestamp_raw_s": 2582, "time": "00:43:03", "video_title": "...", "frame": "t_004302.jpg",
      "confidence": "medium",        // high | medium | low
      "placement": "inferred",       // given | inferred | seen
      "auto": false,                 // true = generated from layout.json's furniture list, with the position guessed
      "quotes": [], "books": ["video:zZEy10fpq3I:2582:sulle-spalle-di-umberto", ...],   // piles only: ids of the books stacked on it (books[].bookcase == the pile id), in slot order
      "books_identified": 4, "books_high": 5, "count": 5,                 // piles only: identified books, the height the film shows, and the effective height
      "on": "obj:salotto:piano", "row": true,                            // `on`: the object this one stands on. `row`: a row of standing books on a top, drawn as spines side by side
      "reference": {"file": "piano_piles.json", "pile_id": "salotto-piano-pile-01", "reader_label": "T1", "level": "lid", "position": "far left of the piano lid", "notes": "..."},   // piles stacked from the film reference
      "shape": "pile",               // semantic shape, see Object geometry
      "primitive": "cylinder",       // the page's simple mesh from objects_map_eco.json `shape` (box | cylinder | sphere | torus | stand | flat | lute | window); absent = box
      "dims_m": [0.22, 0.16, 0.122], // [w, d, h] metres, only when the modelling note or the rule states a size
      "fitted": true, "fit_note": "drawn at the edge of its support: the anchor put it 0.03 m past it",   // an object anchored on another whose rule offset put it past its support's top by less than its own half-width
      "size_note": "...",            // the rule's `size_from`, saying why the drawn size differs from the record's stated dims_m
      "against_wall": "study-P",     // the bookcase the object stands against or on top of; absent for free-standing objects and objects on other objects
      "bookcases": ["study-P"],      // bookcases the object stands against or is attached to
      "facing": 180,                 // degrees, the direction the object faces (= rotation mod 360; 0 faces +z)
      "thumb": "data:image/jpeg;base64,...", "thumb_frame": "t_004302.jpg", "thumb_bytes": 4767, "thumb_crop": "bbox",   // see Object thumbnails; thumb_crop: bbox | hint | centre
      "art_aspect": 1.333,           // artworks with a thumb: w/h of the artwork (dims_m when the note gives a size, else the crop window)
      "tier": "certain", "tier_reason": "seen on film at 43:03; position set from that shot",   // see Certainty tiers; never a rule or file name
      "on_camera": true,
      "placement_note": "Seen on film at 0:55, in front of P · Text theory, linguistics, sem…",   // reader-facing: "Seen on film at m:ss[, <where the rule put it>]" for objects placed by a rule from a frame,
                                     // "Seen in a Fondazione Umberto Eco photograph (bookcase I)" for photographs, "Position inferred from the film[; in front of X]" for guesses
      "placement_url": "https://www.youtube.com/watch?v=zZEy10fpq3I&t=55s",   // the film at that second (objects placed by a rule)
      "sightings": [{"kind": "video", "video_id": "zZEy10fpq3I", "timestamp_s": 2589, "timestamp_raw_s": 2588, "time": "00:43:09", "url": "...", "frame": "...", "image": "...", "label": "..."}],   // every shot of the film inventory that shows it
      "frames_seen": 1, "seen_labels": ["Piano lid pile 1 of 6 (leftmost)"],   // the inventory's own labels for it, at most eight
      "sources": ["experience", "video"], "experience_ids": ["obj-12"]   // where the record came from: the film inventory, the experience files, or both
    }
  ],
  "books": [
    {
      "id": "braidense:VEAE142687",  // braidense:<bid> | bologna:<UBO id> | video:<video id>:<timestamp_s>:<title slug> | photo:<file stem>:<title slug> | u:<n>
      "bookcase": "rare-01", "shelf": 0, "slot": 12, "section": "rare-01-s",   // bookcase may be a pile id (then shelf 0, slot = position from the bottom)
      "title": "Histoires prodigieuses ...", "author": "Pierre Boaistuau", "year": 1560, "date": "1560", "place": "Paris", "publisher": null,
      "language": "fr", "language_name": "French",   // ISO 639-1 where known (it fr en de la es pt nl ru el grc he ...), else the MARC code. The records' three-letter
                                     // forms read to the two-letter code (kor -> ko, lit -> lt, ukr -> uk, bul -> bg); "zxx" is named "no linguistic content", the
                                     // cataloguer's own term. A code with no name is a generator warning, never served as a name. The names are English in both title modes
      "origin": "catalog",           // video | photo | catalog | unlabelled
      "source_kind": "catalog",      // same vocabulary; kept for the description fetcher
      "source_url": "http://opac.braidense.it/bid/VEAE142687",   // video: https://www.youtube.com/watch?v=ID&t=SECONDSs ; photo: the photograph ; catalog: the record
      "catalog": "braidense",        // braidense | bologna | aib-2022 (catalog books)
      "shelfmark": "ECO.01.0227", "all_shelfmarks": "...", "rare": true, "possessor_field": true,   // Braidense records
      "reference": true,             // a Braidense ECO.04 record: see `placement` below
      "subjects": ["..."], "dewey": ["..."], "series": "...", "isbn": "...", "placement_rule": "<subject_map rule name>",   // Bologna records
      "placement_match": "record",   // Bologna records: what the rule matched: record (its own fields) | set title (UNIMARC 461) | responsibility (200 $f/$g)
      "title_raw": "1564, \\Anversa!",           // the title as exported, kept whenever the display pass or the composer changed it (see Display cleaning, Composed titles)
      "set_title": "Summa contra gentiles",   // the set a numbered volume belongs to (UNIMARC 461, or 462/463 for a subset or piece); see Composed titles
      "set_title_raw": "[24-32]: Frederici Ruyschii ...",   // the set title as exported, when a volume-range prefix or a bare volume number and colon was taken off it
      "set_volume": "4",             // the volume number the set title carried (see set_title_raw)
      "volume_statement": "Vol. 5.", // the record's own 200 $a, kept whenever the displayed title was composed
      "part_title": "La chiesa nei tempi moderni",   // the phrase a part's statement of responsibility gave in place of a title
      "author_from_set": true,       // `author` is the set's statement (461 embedded 200 $f), the record having none of its own
      "date_note": "...",            // a curated correction of the record's date (record_notes_eco.json), with the note that says why; the export's own date stays in `date`
      "tier": "certain", "tier_reason": "Braidense shelfmark ECO.01.0227",   // on every book, see Certainty tiers
      "confidence": "high",          // high | medium | low
      "placement": "catalogued",     // catalogued | seen | inferred | unshelved | reference | filler
                                     // unshelved: bookcase, shelf, slot and section are null; the book is in books[] but on no bay (see Bologna placement).
                                     // reference: a record of the Braidense's ECO.04 section, `reference: true`, listed on the study's reference table, tier guess,
                                     // `placement_note` the provenance sentence and the inventory date, `copy.library_copy: true`; never counted as identified
      "placement_note": "the reading names only the room (studio); the bookcase is a guess",   // reader-facing sentence, whenever the place was inferred from a reading,
                                     // a shelf label or the fallback rule, or a record was moved to a bay the film names (see Spine-reading frames, Catalogue matching)
      "shelf_label": "ECO IBERICI (Q4/Q5)",   // readings placed from a shelf label or call tag visible in the frame: the label text (wall_map_eco.json label_patterns, or a parsed call tag such as 'L11.5')
      "reading_note": "The spine reads only 'Bernini'; ...",   // a reading corrected by wall_map_eco.json `reading_fixes` (the fix's note)
      "work": "Il nome della rosa (1980)",    // from a reading fix: the work a translation on the spine belongs to ("Imię róży")
      "video_id": "zZEy10fpq3I", "timestamp_s": 2570, "timestamp_raw_s": 2569, "time": "00:42:50", "video_title": "...",   // video books; timestamp_raw_s is the second in the file the reader worked from
      "photo_credit": "...", "frame": "fondazione_17_I.webp",   // photo books; photo_credit only when the photograph carries a credit
      "sightings": [{"kind": "video", "video_id": "...", "timestamp_s": 24, "timestamp_raw_s": 23.6, "time": "00:00:24", "url": "...", "frame": "t_000024.jpg",
                     "credit": null, "confidence": "high", "bookcase": "...", "level": "bookcase", "dense_id": "...", "dense_tier": "certain"}],
                                     // `level` is how well the frame names the place: bookcase | wall (the reader's tag or wall label names the bay) | label (a subject tab) |
                                     // context (the pass's own description of the wall) | room | subject | fallback | pile
      "frames_seen": 2, "title_variants": ["Inventing the Enemy"], "spine_text": "...", "also_seen": true,   // also_seen: a catalogue record that a reading matched
      "in_pile": true,               // the book lies in a pile object
      "pile_position": 4,            // pile books of a pile with `books_high`: place from the top, 1 = the top spine, unlabelled spines counted (see Spine-reading frames that become piles)
      "pile_filler": true,           // a placeholder spine of a counted pile that no reading identified (see the last entries below)
      "alt_readings": [{"title": "I bambini di Moloch", "author": "Lazzatto", "confidence": "low", "spine_text": "...", "frame": "p_0104.jpg", "video_id": "...",
                        "timestamp_s": 2583, "time": "00:43:03", "url": "...", "source": "spines_zZEy10fpq3I_piano_heavy.jsonl", "first_pass_only": false}],
                                     // the same spine read differently by another reader (or the reader's own `read_as`); the book carries the highest-confidence reading, these are the
                                     // others, also listed in title_variants as "<title> — <author> (<confidence> confidence, second reading, sharper frames at 00:43:03)"
      "author_only": true, "display_title": "Gillo Dorfles (title not readable)",   // a pile book whose spine shows only the author (title null): shown under display_title, tier guess
      "from_reference": true, "fragment": true,   // a pile book the film reference reads that no first-pass reading carried; a fragment is a spine whose title is not legible at all
                                     // (display_title "<author> (title not readable)" or "<publisher> volume (title not readable)")
      "merged_ids": ["video:zZEy10fpq3I:2570:..."],   // reading ids merged into this catalogue record (or into the surviving reading of a merge).
                                     // A book id ending in `~<pile>` (`video:...:by-umberto-eco~pile-04`) is a further copy of a consolidated reading seen with its own sightings
                                     // in more than one pile: one book per pile, the description under the id before the `~`
      "second_copy": true,           // a Bologna record of one title by one author with another record of the same title on the same bookcase; the placement_note names the other record
      "seen_by_tag": {"bookcase": "study-Q", "time": "00:09:13", "url": "...", "video_id": "...", "how": "...", "tags": [], "dense_id": "...", "dense_tier": "probable",
                      "tag_verified": false, "moved_from": "corridor-02", "rule": "Italian writers (author)", "after_move": false},   // a catalogue record a tagged film sighting names: see Catalogue matching
      "seen_elsewhere": {"bookcase": "rare-02", "level": "room", "time": "00:01:10", "url": "...", "video_id": "...", "tags": [], "dense_id": "..."},   // read on another bookcase; the record is not moved
      "seen_on_film_agrees": true,   // the film read the record on the bookcase the shelfmark or the subject rule had given it
      "seen_after_move": true,       // placed by a tag read in the Bologna reinstallation, not in the flat
      "title_seen_on_film": {"time": "00:01:29", "url": "...", "video_id": "...", "bookcase": "study-Q", "level": "bookcase"},   // a reference entry whose title was read on a shelf of the flat
      "notable": {"why": "...", "source_url": "...", "source": "...", "category": "name-of-the-rose", "year": 1980, "rare_book": false,
                  "links": [{"text": "nota di vendita Christie's", "url": "https://www.christies.com/en/lot/lot-2031570"}]},
                                     // gold band on the spine and an entry in the Notable list, grouped by category (see Notable tours); only on the work itself, never on a study of it.
                                     // `links` names a phrase inside `why` and the page prints that phrase as the link
      "copy": {                      // Bologna and Braidense records: the copy fields that make it Eco's copy (UNIMARC 316/317/318 and the holdings)
        "inventory": "ECO 2438", "inventory_date": "2016-09-09", "holding_note": "v. 22", "ex_libris": true, "library_copy": true,
        "holdings": [{"shelfmark": "...", "inventory": "...", "inventory_date": "..."}],   // only when the record has several ECO holdings (volumes, works bound together)
        "provenance": ["Provenienza: Eco, Umberto"], "dedication_by": ["Costantini, Michel"],
        "givers": ["Michel Costantini"],   // the dedication's authors as a reader says the name ('Alberoni, Francesco <1929-2023>' -> 'Francesco Alberoni'); the catalogue form stays in dedication_by
        "inscription": "Per Umberto Eco, con amicizia",   // the words the cataloguer transcribed after the dedication remark, verbatim (the [?] marks kept): that span and only
                                     // that, closed at its own quotation mark (a quotation inside the words stays whole), or the sentence where the export's quote is not closed or
                                     // never opened. A quoted source title, card, page number or clipping is not an inscription. The final stop is kept; four characters is the floor
        "inscribed_by_eco": true,    // the dedication's author heading (317) is Eco's own, so the copy is one he inscribed to someone else: the mark "dedication by Eco" in place of
                                     // "dedication", no givers, the class "eco"
        "giver_note": "The catalogue names Matilde Serao ...",   // from copy_notes_eco.json, printed under the catalogue's dedication line on the card when the record's own fields
                                     // contradict the name; with drop_givers the givers are empty and the copy reads "Inscribed, no giver named"
        "annotation": "Sull'occhietto tracce del timbro tratto da ex libris di Umberto Eco ...; frequenti sottolineature a penna ...",
        "condition": "...", "marks": ["ex-libris stamp", "dedication", "dedication by Eco", "underlinings", "marginalia", "dog-ears", "inserts"], "bub_shelfmark": "BU T 4616 /751160"},
      "incunabulum": true, "istc": "ib00526000", "istc_url": "https://data.cerl.org/istc/ib00526000",   // the 36 incunabula (experience/incunabula.json, matched to the Braidense records)
      "card": {"place": "Venice", "printer": "...", "date": "1482", "format": "4to", "size_cm": "21 x 15", "binding_condition": "...", "provenance": "...",
               "price_dealer": "...", "note": "...", "istc": "...", "istc_url": "...", "source": "Nuovo & Coletto, AIB Studi 2022", "source_url": "...",
               "article_page": "17", "pdf_page": "9"},   // Eco's own card. article_page is the journal's printed page, pdf_page the page of the PDF file; the panel prints neither
      "description": "...", "description_kind": "article", "description_source": "https://it.wikipedia.org/wiki/...", "description_lang": "it",   // merged from the description files (see Descriptions)
                                     // description_kind: article (the work's own article) | search (article found by title search) | author (fallback: the author's article, text
                                     // prefixed "By <author>: ") | edition (a verified one-line note on a translation of Eco's own book) | catalog (an ISTC note on an incunabulum) | none
      "title_en": "The Name of the Rose", "title_en_kind": "published", "title_en_source": "English edition (Harcourt, 1983, tr. William Weaver)",   // see English titles
      "desc_en": "...",              // the description rendered in English (descriptions_en_eco.json), shown in English mode with the same source link and ", translated here"
      "width": 0.039, "height": 0.25 // the drawn spine, in metres
    },
    {"id": "u:000001", "bookcase": "corridor-01", "shelf": 0, "slot": 0, "section": "corridor-01-s", "origin": "unlabelled", "placement": "filler",
     "tier": "unknown", "tier_reason": "empty slot", "width": 0.031, "height": 0.21},
    {"id": "u:pile:piano-pile-02:09", "bookcase": "obj:salotto:piano-pile-02", "shelf": 0, "slot": 0, "origin": "unlabelled", "placement": "filler",
     "pile_filler": true, "pile_position": 9, "spine_text": "Il Novecento (green spine, companion volume; subtitle not legible)",
     "tier": "unknown", "tier_reason": "empty slot", "width": 0.028, "height": 0.23}   // a spine of a counted pile that no reading identified
  ]
}
```

## Quotes

`rooms[].quotes`, `rooms[].bookcases[].quotes` and `objects[].quotes` are arrays of

```jsonc
{"text": "English text", "text_it": "testo italiano", "source": "title of the source", "url": "https://...",
 "speaker": "Umberto Eco", "context": "a voice-over, not Eco speaking on camera",
 "where": {"video_id": "...", "timestamp_s": 123, "url": "https://www.youtube.com/watch?v=...&t=123s"}}
```

Quotes come from `quotes_eco.json` (read first), then `experience/quotes.json`, then the eco-video quote files. For the same
video and timestamp the entry from `quotes_eco.json` wins on text, speaker and source, so the 51:04 line of the film carries its
single attribution, "Renate Ramge Eco", with the `context` note that it is a voice-over.
The page shows the first quote of a bookcase or object as a small floating card above its label (visible when near), room quotes
as a card under the room name, and every quote in the panel when the bookcase, room or object is clicked. The tour bar also shows
a stop's quote. `meta.quotes_general` holds the quotes with no shelf of their own; About prints them.

## Tour

`meta.tour = {"title": "...", "auto": bool, "file": "tour_eco.json", "stops": [...]}` with stops

```jsonc
{"id": "stop-studio", "target": "studio",   // a room id, bookcase id, object id or book id
 "kind": "room",                            // room | bookcase | object | book; informational
 "caption": "The big study: ...", "url": "https://... (optional 'more' link)",
 "quote": { /* a quote object, optional */ },
 "camera": {"pos": [x, y, z], "target": [x, y, z]}   // optional explicit camera in world metres; otherwise the page frames the target}
```

`tour_eco.json` gives every stop whose caption names a thing a target that is that bookcase or object, and, where the page's
automatic framing picks the wrong thing (a coat rail, spine tops behind a bay plate, a blank wall, the desk from above), an
eye-level `camera` (y 1.5 to 1.7 m, 1.4 to 3.8 m from the target, inside the room and clear of the shelving). The vestibule stop
targets bookcase C with B and D in view, the two bookcase A stops run along the corridor at bays A2 and A13, the turn targets the
French window at the corridor end, and the desk stop is a three-quarter view of the desk row from inside the study.

Without `experience/tour.json` the generator writes one stop per room, in room order, with the first sentence of the room blurb
and the room's first quote, and sets `auto: true`.

## Walk

`meta.walk` replays the film's long take as an animated camera path (`walk_eco.json`, the "Eco's walk" button):

```jsonc
{"title": "Eco's walk, 2015", "video_id": "Hq66X9f-zgc", "video_title": "...", "film_video_id": "zZEy10fpq3I", "film_title": "...",
 "film_label_offset_s": -247, "film_time_offset_s": 0.96, "source": "...", "duration_s": 73.0,
 "route_notes": [{"id": "...", "item": "...", "description": "...", "note": "...", "url": "...", "video_id": "...", "timestamp_s": 293}],
 "waypoints": [{"t": 293.2,                     // seconds on the video_id clock; the page interpolates a CatmullRom path between waypoints
                "pos": [x, y, z], "look": [x, y, z],   // world metres: where the camera stands and what it faces
                "room": "salotto", "caption": "...", "quote": { /* quote object, shown when the waypoint is reached */ },
                "url": "https://www.youtube.com/watch?v=Hq66X9f-zgc&t=293s", "film_url": "...", "film_label_s": 46}]}
```

## Tours

`meta.tours` (from `tours_eco.json`) is the list of the fourteen guided tours:

```jsonc
{"id": "rose", "title": "...", "blurb": "...", "dropped": 0,     // dropped: stops the generator refused, counted
 "stops": [{"id": "rose-01", "target": "<book, bookcase or object id>", "kind": "book",   // book | bookcase | object
            "title": "Il nome della rosa (1980)", "caption": "...",
            "source": {"kind": "catalogue", "label": "...", "url": "..."},   // kind: catalogue | essay | novel | interview | film | article
            "quote": {"text": "...", "lang": "it", "translation": "...", "attribution": "...", "url": "..."} | null,
            "image": {"src": "data:image/jpeg;base64,...", "alt": "...", "credit": "...", "link": "...", "w": 200, "h": 71} | null,
            "record": "braidense:BA10112230"}]}                  // optional
```

`record` is the id of a reference entry (the Braidense's ECO.04 record of the same book) on a stop that opens on a copy filmed in
the flat. The tour card prints it as `Catalogue record: <title>, <publisher> <year> (Biblioteca Braidense, reference
section <shelfmark>)`, a link that opens the entry's panel in place. The generator drops, with a warning, a `record` that is not a
reference entry or that is the stop's own target.

A stop's `id` is its stable name in `tours_eco.json`, not its position in the tour. The tours are ordered by the `stops` list, so
a stop may keep its id after the list is reordered: the Baudolino tour's seventh stop is `baudolino-06`, its fifth `baudolino-08`.
A record that names a stop by number counts along the list.


## Notable tours

`meta.notable_tours` groups the flagged books by `notable.category`, one entry per novel, essay or theme, in the order of
`notable_books.json`:

```jsonc
{"id": "notable-name-of-the-rose", "category": "name-of-the-rose", "title": "The Name of the Rose (1980)",
 "books": ["braidense:...", ...], "missing": 13, "stops": [...]}
```

`stops` keeps every entry of the category in file order, matched or not. For a book that is in the library:

```jsonc
{"id": "braidense:...", "title": "<notable title>", "author": "...", "year": 1323, "why": "...", "missing": false,
 "match": "work" | "collected" | "listed", "note": null}
```

and for one that is not:

```jsonc
{"id": null, "title": "...", "author": "...", "year": 1944, "why": "...", "source": "...", "missing": true,
 "note": "not among the catalogued or filmed books[; the nearest record by the same author is '<title>' (<id>)]",
 "nearest_id": "...", "nearest_title": "...", "nearest_bookcase": "...",
 "subject_bookcase": "...", "subject_rule": "...", "subject_room": "..."}
```

`title`, `author`, `year`, `why` and `source` come from `notable_books.json`; `meta.counts.notable_missing` totals the missing
stops, 13 for The Name of the Rose alone (Borges, Conan Doyle, the Beatus, Bernard Gui, the Physiologus). The Notable list shows
the categories as sections. "Tour these shelves" runs a tour from spine to spine over the matched ones and lists the missing ones
as text ("N more sources Eco is known to have used are not in the public catalogues: ..."), with the nearest same-author record as
a link where one exists.

`nearest_id` is the curated id refused by the work test when it is another title by the same author, else the library's nearest
record whose *author field* carries the notable's surname and, where both give one, the same given name (Yates to *L'arte della
memoria*, Mandeville to the 1480 *Viaggi*, Dumas to *Ascanio*). It is never a title that merely names the author, and never
Maurizio Bettini for Mario Bettini or Léon Gautier for Théophile.

A missing stop with no `nearest_id` carries `subject_bookcase` and `subject_rule`, the bookcase the subject rules give the work's
title and author, and the card says `shelf guessed by subject: <subject>`. When no rule matches it carries only `subject_room`,
the room of the fallback bookcase; the card says so and the room panel opens. `meta.counts.notable_missing_by_subject` and
`notable_missing_room_only` count the two cases.

The join is on the **work**, never on a surname found anywhere: the notable's title or original title (Latin-folded four-letter
stems for a curated id, five-letter stems for the open search over every identified book) against the record's title, set title
and title variants, with the notable's author required to be the record's *main* author (its author field, or the name at the head
of a Latin title: "Aurelii Augustini ... De ciuitate Dei") whenever both name one. A curated id from `notable_books.json`
(`catalog_match.books_json_id`) is accepted when it passes that test (`match: "work"`), when it is the author's collected works
(`"collected"`: Cyrano's *Oeuvres diverses* for *L'Autre Monde*), or, in the `incunabula` category, when the AIB Studi shelfmark
identifies the record (`"listed"`). A curated id that fails (Guglielmi's *El Eco de la rosa y Borges* for *Ficciones*, Bayard's
*Il caso del mastino dei Baskerville*, *Leggere I promessi sposi*, Bignami's Galileo pamphlet, Sosnowski's *Borges y la cabala*)
is listed in `meta.experience.notable.rejected` with the reason, and the entry becomes a missing stop. When the refused record is
another title by the same author (Yates's *Cabbala e occultismo* for *Giordano Bruno and the Hermetic Tradition*) the stop's note
names it as the nearest record.

## Display cleaning

Every string the page shows goes through `clean_display()` at the end of the run, and `meta.counts.display_cleaned` counts the
fields changed. The SBN and UNIMARC export's bracket markers become brackets (`1564, \Anversa!` to `1564, [Anversa]`, `°1!:` to
`[1]:`, `Paris [etc.!` to `Paris [etc.]`, `s.n.!` to `[s.n.]`); a `!` with no bracket open, as in *Goodbye, Kant!* or the 'GOSH!'
picture, is left alone, and an exclamation set between dashes ("-chissà!-") is not a sic mark. Non-sorting markers go (`<<Les >>`,
`Il *nome`, `La *diagonale`; the asterisks of an anonymised `M***` stay). A `[!]` sic mark prints as `[sic]`, and `title_raw`
keeps the `[!]`. SBN name qualifiers are joined (`William : of#Ockham` to `William of Ockham`, `Albertus : Magnus` to `Albertus
Magnus`, `Balzac, Honoré : de` to `Balzac, Honoré de`, `\a cura di! X` to `[a cura di] X`). The volume-range prefix of a set
(`[24-32]: Frederici Ruyschii ...`) is dropped from titles and set titles, and a leading part numbering (`1.[1]: `) from display
titles; `title_raw` and `set_title_raw` keep the export form. Internal provenance inside a citation (`(local carriere.txt)`) is
removed, and runs of spaces collapse.

A served title, set title, volume statement or part title never ends with " /", " :", ";" or "|", and never holds a pipe: an inner
pipe becomes ": ". `meta.counts.catalog.title_tails_cleaned` counts the strings changed.

Elisions are closed at the end of the pass and inside the inscriptions: a lower-case elided form (l', d', un', dell', all', nell',
sull', quell', c', s', m', t', n', j', qu') before a space and a word is closed anywhere, a capitalised form only where a title or
a sentence begins, and never inside a quotation the cataloguer opened.

Cleaning is applied to books (title, set title, volume statement, part title, title variants, author, place, date, publisher,
series, the notable `why` and `source`, the copy notes), objects (label, description, seen labels, placement note, video title),
rooms and bookcases (names, blurbs, evidence, labels), quotes, the tour and walk captions, the notable tours' stops and
`meta.experience.notable.unmatched`, `meta.notes`, `meta.layout_notes`, `meta.counts.overlay_note` and `meta.sources`.
`spine_text`, the raw reading of the spine, is never cleaned.

No note on the page names a mapping file, a rule, a frame file or a `meta.*` key. Photographs are named by their source
(`photo_name()`: "a Fondazione Umberto Eco photograph (bookcase I)", "a CriticaLetteraria photograph (November 2022)"), film
moments by their minute ("Seen on film at 13:02"), and `meta.counts.spine.video_files` and `photo_files` carry base names only.

## Composed titles

A catalogue record of one volume of a set often carries no title of its own, only a number. The generator composes a title a
reader can use, and keeps the catalogue's own words beside it.

A record with a UNIMARC 461 link (set), or 462 or 463 (subset, piece), gives `set_title`, the set a numbered volume ('2', 'Vol. 1',
'1: A-E') belongs to. The displayed title is then composed as `<set title>, vol. N[: own title]`, from the Bologna jsonl and,
through `--braidense-mrc`, from the Braidense .mrc. A bare volume statement is composed too ('Tome second', 'Volume 1 di 2' to
'vol. 1 of 2'), and a slash followed by a digit ('3/4: Exact logic') as 'vol. 3/4', the Peirce volumes 3 and 4 bound as one. The
composer reads tomus, pars, volumen, liber, libro, partie, fascicolo, deel, cahier, heft, the Latin ordinals, a bracketed number
and a year range ('Vol.1 1857-1866' to 'vol. 1: 1857-1866'). The volume's own title loses its ISBD tail, an unclosed bracket and a
closing stop; the set's trailing range ('Tome premier [-quatrieme]') and closing stop are dropped; a volume title that repeats the
set's is dropped, and one that opens with it is kept whole with the number after it.

`set_title_raw` keeps the set title as exported when something was taken off it: a volume-range prefix (`[24-32]: Frederici
Ruyschii ...`), or the catalogue's own bare volume number and colon ("4: La filosofia moderna"), a set within a set. In the second
case the number goes to `set_volume` and `set_title` keeps the rest, so the composed title reads "La filosofia moderna, vol. 5:
G. G. F. Hegel" and never "4: La filosofia moderna, vol. 5: ...".

`volume_statement` keeps the record's own 200 $a whenever the title was composed, on Braidense and Bologna records alike. A record
with no set link whose own title is only a bare number, a colon and a title ("2: L'Eta romantica") is composed the same way: the
title becomes "L'Eta romantica, vol. 2", `volume_statement` keeps the catalogue's form, and `title_en` never keeps a bare number
the native title lost. A statement that opens with a range ("1-2: Principles of philosophy", "31.1-2: Rhetorica ...") keeps the
range as the volume number, with the catalogue's hyphen and no spaces: "vol. 1-2: Principles of philosophy". A composed, bare or
English title that prints "vol. N: M", a volume number, a colon and a bare number, is a generator warning.

`part_title` covers a volume record whose own title is only its number and whose statement of responsibility is not a name. The
set's statement (461 embedded 200 $f) becomes the author line (`author_from_set`), the phrase becomes the part's title, the
composed title reads "<set>, vol. 5-1: La chiesa nei tempi moderni", and `volume_statement` keeps the record's own words.

`author_from_set` marks a record with no statement of responsibility of its own, whose `author` is the set's, as the catalogue
transcribes it. A set statement that is only surnames ('Manara, Eco') is written out from the record's own 700/701 headings ('Milo
Manara, Umberto Eco'); any other statement stands as transcribed. A set statement that goes on to name the volumes is not used.

A Bologna title is built from the record's own 200 subfields with the catalogue's punctuation: $a, a further $a after " ; ", $e
after " : ", $d after " = ". The responsibility, the material designation and a title by another author stay out. Where that
differs from the export's `title_full`, which joined the subfields with a bare space, `title_raw` keeps the export's form.

`meta.counts.catalog.volume_titles` counts the composed titles, and `part_titles_from_responsibility` and `authors_from_set` the
two cases above.

## Reading fixes (`wall_map_eco.json` `reading_fixes`)

`{"<reading id>": {"<field>": <value or null>, "note": "..."}}` overwrites fields of one consolidated reading, or of the catalogue
record it was merged into, through `merged_ids`. `null` removes the field, the note becomes the book's `reading_note`, and the ids
go to `meta.counts.reading_fixes`. The fields a fix may set are `title`, `author`, `language`, `series`, `publisher`,
`spine_text`, `confidence`, `placement_note`, `work` and `catalog_record`.

Fixes are for a reader's slip that the consolidation kept. `video:NtPk4irDiM8:65:bernini` read "Bernini" with the author of the
neighbouring spine (Christian Tümpel, whose *Rembrandt* is its own reading, `video:KZfOaug0mM4:74:rembrandt`); the fix clears the
author and the copied spine text.

The fixes are applied twice. First to the consolidated reading as it is ingested (`title_as_read` and `author_as_read` are cleared
and the reading is marked `fixed`), so that the corrected title takes part in the pile and same-bay merges: a fixed reading whose
corrected title is another reading's native title merges into it, the native reading's id survives, and the fixed id goes to
`merged_ids`. Then again after the books are built, to attach the notes.

The piano pass of the 2022 film (raw 2570 to 2582 s) has nine such fixes: the first reader's "inconsolabile pensiero" is Calasso's
*L'innominabile attuale*, "Sulle spalle dei giganti" on pile 01 is the Festschrift *Sulle spalle di Umberto*, "omicidio di Umberto
Eco" is the spine of *L'eredità di Umberto Eco* (pile 05, one book, not two), a bare "Eco" on pile 06 is the German *Auf den
Schultern von Riesen*, and five author-only readings take their title from the second reading (*L'anima ciliegia*, *Storie di
percorso*, *Una passione a Manhattan*, *Breve autobiografia*, *Cerchi di capire, prof*). An id in the file that no reading carries
any more gives `WARN reading_fixes: no reading with id`.

`catalog_record` is read at the catalogue merge and never copied onto the book: `"braidense:<bid>"` forces the record a reading is
attached to, `false` forbids any match. A catalogue record that a fixed reading was merged into shows the fix's note as
`reading_note`. A fixed reading merged in the same bay with a native reading of the same title leaves the id to the native one, as
in the piles.

## The `experience/` input files

All optional; `gen_books_eco.py --experience DIR`, default `eco-sources/experience/`.

* `objects.json`: a list (or `{"objects": [...]}`) of objects. Fields: `id` (optional; an id equal to an auto-generated furniture
  object replaces it), `room` (layout room id or an alias from `wall_map_eco.json`: study, living, rare), `kind` (guessed from the
  label when absent), `position` `[x, z]` **in metres from the room's north-west corner** (or `{"x":..,"z":..}`; omitted means a
  free spot is chosen), `rotation` (degrees), `base_y`, `size` `[w, h, d]`, `label`, `description`, `source`, `source_url`,
  `video_id`, `timestamp_s`, `confidence`, `quotes`, and for piles `books` (a list of `{title, author, language, confidence,
  video_id, timestamp_s, source_url}`; **not yet consumed**: piles from files are drawn as anonymous stacks, and titled piles come
  from the spine readers' "stack" frames). The research brief's own shape is read too: 95 records of rooms, fixtures, furniture,
  artworks, piles and objects with a `modelling_note`, merged with `eco-video/objects_from_video.json` through
  `objects_map_eco.json` (the experience record wins where both name the same thing). Kinds `room` and `roomnote` become
  `rooms[].film_notes`, and `route` records become `meta.walk.route_notes`.
* `quotes.json`: a list (or `{"quotes": [...]}`) of quote objects as above plus `target`: a bookcase id (`study-P`), a layout id
  (`vest-D`), a Fondazione letter (`P`), a room id or alias, or an object id. Unmatched targets are listed in
  `meta.experience.quotes.unplaced`.
* `notable_books.json`: a list (or `{"books": [...]}`) of `{"match": {"id": ..} | {"title": .., "author": ..}, "why": "...",
  "source_url": "...", "first_only": false}`. `title`, `author` and `id` may also sit at the top level, and the research brief's
  shape with `catalog_match.books_json_id`, `key`, `category` and a 15-stop `tour` is read too. Matched by id, else by normalised
  title (stop words dropped) and the author's surname; every matching copy is flagged unless `first_only`. Misses are listed in
  `meta.experience.notable.unmatched`.
* `incunabula.json`: the 36 incunabula of the AIB Studi 2022 list with Eco's card data and ISTC ids, matched to Braidense records
  by bid, shelfmark, or title tokens and year. An unmatched one would be added as a `catalog: "aib-2022"` book on the ECO.03 cabinet.
* `tour.json`: `{"title": "...", "stops": [...]}` as above.
* `layout.json` bookcases may carry `offset_m`: wall run left free before the unit. `rare-04` (ECO.03, the "most precious" cabinet
  on the balcony wall) has 0.5 m so that it starts clear of the left-hand cabinet `rare-01`, which is 0.45 m deep and runs to
  0.57 m of that corner. Without it, ECO.03.0001 (Durand's *Rationale*, 1480) sits inside the end of rare-01 and a click on it
  picks a rare-01 spine. A bookcase may also carry `setback_m`: the unit stands free that far in front of its wall, still facing
  the room (the salotto vitrines). The bookcase then carries `setback` in `books.json`, objects anchored to it (`anchor.bookcase`)
  follow it, and wall occupancy for auto-placed objects is unchanged. `layout.json` may also list a room's `windows`, which the
  page draws and which are not free wall for a framed print.
* `brief.md`: an optional note file for the builder. When one is present it is read and not copied into `books.json`, so the page
  never shows it.

Two further input files sit next to the generator rather than in `experience/`:

* `record_notes_eco.json`: curated corrections of a record's date, keyed by book id, `{"year": 1886, "date_note": "...",
  "note": "...", "source": "...", "posthumous": true}`. The export's own date stays in `date`, and `date_note` says why the year
  differs.
* `copy_notes_eco.json` (`--copy-notes`): qualifications of University of Bologna copy records whose own fields contradict one
  another, keyed by record id: `giver_note` (printed under the catalogue's dedication line on the card), `drop_givers` (the name
  comes off the "Given to Eco" colouring and the givers list, while the catalogue's line stays as evidence), `status` and
  `source`. One record uses it, UBO00189116, the Serao line; `meta.counts.catalog.bologna_copies.copy_notes_applied` lists what
  was applied.

## Film objects (`eco-video/objects_from_video.json` + `objects_map_eco.json`)

Each of the inventoried objects (with `shot`, `room`, `kind`, `label`, `position_hint`, `timestamp_s`) is matched against the
rules of `objects_map_eco.json` in order: `match` (label regex), `hint` (position_hint regex), `kinds`, `rooms`. A rule gives
`position` (room-local metres), or an `anchor`: `{bookcase, dist, along, on_top}` in front of or on a bookcase, `{object, offset,
on_top}` on another object, `{wall, at, dist}`, or `auto` for the first free wall spot. It may also give `size`, `shape`, `attach`
(the object becomes a `seen_in_film` line of a bookcase instead of a mesh), `skip`, or `each` (one object per sighting). An
integer `count` on the rule wins over the inventory's count from a single frame, as for the six dining chairs. An inventory
description's "(layout '<id>')" cross-reference is dropped.

A rule's `walls` lists the spine-reading walls (`books_by_wall_eco.json` `wall_id`s) whose titles lie on the object. An entry is a
wall id, or `{"wall": "study-desk-piles-1", "raw_from": 2582, "raw_to": 2590}` restricting it to a window of raw film seconds, so
one wall can feed two piles of one piece of furniture. An entry with `"defer": true` is only a fallback: a consolidated book read
on that wall is placed by its sightings on other, non-deferred walls, and comes to the deferred entry's object only when it has
none (`meta.counts.spine.pile_deferred_only`).

The object's room wins over the reader's room label. The "study desk piles" wall of the film's 42:50 to 43:03 pass is the salotto
piano, and its books are piano books, not desk books; that wall is deferred to the twelve per-pile walls `salotto-piano-pile-01`
to `-12` of `spines_zZEy10fpq3I_piano.jsonl` and `spines_zZEy10fpq3I_piano_heavy.jsonl`, two independent readings of the same
pass, one wall per physical stack (piles 01 to 06 on the lid, 07 to 12 on the keyboard shelf, left to right as seen from the
front), each its own `obj:salotto:piano-pile-NN`.

An `anchor` on another object may give `along_frac`: the fraction of the carrying object's width at which the thing stands, 0 at
that object's left end as seen from its front, 1 at its right end ("on the lid at 0.35 of its length" is `{"object":
"obj:salotto:piano", "on_top": true, "along_frac": 0.35}`). It adds to `offset[0]`, and `offset[1]` and `base_y` still say how far
forward and how high (the keyboard-shelf piles: `offset [0, 0.30]`, `base_y 0.78`).

A rule may also state `dims_m` (`[w, d, h]` metres, copied to the object when no modelling note gives a size), `crop` (the
thumbnail window of the object's best frame, fractions `[x0, y0, x1, y1]`) and, for a pile, `books_high`: the number of spines
counted in the stack, copied to the object as `books_high` and `count`. The twelve piano piles are 5, 9, 11, 13, 7 and 8 high on
the lid and 11, 18, 14, 4, 9 and 9 on the keyboard shelf, counted from the sharper 1080p frames; the rule's `books_high_source`
says where the count comes from.

Objects with no rule are auto-placed in the room and listed in `meta.camera.auto_placed` for checking. `rooms_seen` gives
`rooms[].seen_*`. A bookcase is `on_camera` when a reading, a pile or an inventoried object was placed on it.

A layout unit whose label says "cabinet of curiosities", or whose id is `salotto-wood`, is `kind: cabinet`, `glazed: true`,
`curio: true`, and gets no filler slots: the page draws its shelves with objects (eggs, bottles, oval frames, a bust, a clock, a
specimen under glass, a few books lying flat) instead of a book run. Its `seen_in_film` lists each sighting once, label and second.

## Spine-reading frames that become piles

A frame whose `view` is `stack`, `pile` or `piano`, or whose wall label resolves to `@pile` in `wall_map_eco.json` (coffee-table
close-ups, "held to camera", desk piles), becomes a pile object in the room the frame names (`room_id`, or the wall label matched
against the room aliases and patterns). One pile per distinct `wall_id` per room. Its titles are deduplicated across frames like
shelf readings and become `books[]` entries with `bookcase` = the pile id, `in_pile: true`, `placement: "seen"` and the usual
video or photo source fields. The pile sits on the room's first desk, table or piano object when there is one (`on`, `base_y` its
height), otherwise on the floor at a free spot.

Within a pile the books are stacked as the reader saw them. When a stack frame's row is labelled "top to bottom" (or "from the
top"), each title's `pos` in the raw spine file is its place from the top, so the largest `pos` gets `slot` 0, the bottom. Titles
no frame positions this way go beneath, in reading order.

One physical sighting group is one placement. Readings of the same work (title tokens and author surname) on the same layout unit
are merged (`meta.counts.spine.merged_same_bay`), and readings of the same work in two piles of the same room within 60 s of the
same video are merged into the inventory-seeded reading (`merged_across_piles`); the surviving book keeps the other ids in
`merged_ids` and all sightings. Two readings that each have their own non-deferred sightings in two different piles are two
copies, not one: the consolidated reading is placed once per pile, the second copy with id `<id>~<pile>`
(`meta.counts.spine.pile_copies`). A consolidation that merged the same reading across piles by title (an author-only "Umberto
Eco" on the piano and on the coffee table) therefore still gives one book per pile.

**Piles with a counted height** (`books_high` on the object, from the `objects_map_eco.json` rule) are rendered exactly as high as
the film shows. The pile's readings are stacked by the fullest reading of that pile, the raw frame row with the most entries, with
unlabelled runs counted by their `count`. Each identified book takes that row's position from the top (`pile_position`, 1 the top
spine; a title, or for an author-only spine the row's single entry with that author). Books that row does not list take their
position from another reading scaled to the height, collisions push down, and books no reading positions go beneath. `slot` =
`books_high` - `pile_position`, so slot 0 is the bottom.

The positions no reading identified become **pile fillers**: blank books `u:pile:<pile>:<NN>` with `origin: "unlabelled"`,
`placement: "filler"`, `pile_filler: true`, `pile_position`, and the raw reading's `spine_text` describing the spine where it gave
one. Identified books plus fillers come to `books_high` (`meta.counts.spine.pile_fillers`). The object's `count` is the effective
height, `books_identified` the number of identified books, and `books` their ids in slot order. A pile whose object has no
`books_high` is stacked by the reader's `pos` from the top, with unpositioned books beneath, and has no fillers.

**Piles stacked from the film reference.** `gen_books_eco.py --piano-ref` (default `eco-video/piano_piles.json`) stacks the twelve
piano piles from the reference reading of the film's 42:50 to 43:04 frames. For every pile the reference's `book_count` is the
height, and every position from the top is filled by the reading the reference names (`matched.id`), else by the reading whose
title, title fragment, spine text or author agrees, else by a first-pass reading whose spine text the reference reads as a blank
(kept, since the frame confirms it), else by a second copy of a reading of another pile (`id~<pile>`, `reading_note` "a second
copy: ..."), else by a book born from the reference itself (`from_reference: true`, sightings on `wall_id` `piano-reference`, id
`video:<vid>:<raw second>:<slug>`). An unreadable title becomes an author-only or publisher-only fragment (`fragment: true`) with
`display_title` "<author> (title not readable)" or "<publisher> volume (title not readable)". A first-pass reading that the
reference reads differently at the same position is kept as an alternative (`alt_readings`, shown as "Also read as"). A blank of
the reference is a blank filler carrying the reference's spine description. `objects[].reference` records how each pile was
stacked. `check_piano.py` compares `books.json` with the reference (count, order, kind of spine at every position, titles, and the
heights 5/9/11/13/7/8 and 11/18/14/4/9/9) and exits 1 on any difference; `test_page_eco.py` runs it as its last check.

**Author-only readings** (`title: null`, an author on the spine) are placed only in piles, never on shelves
(`meta.counts.spine.author_only_placed`). The book has `author_only: true`, `display_title` "<Author> (title not readable)", tier
`guess` ("only the author's name was read ...; the title is not legible"), the film link of its sightings, and the id
`video:<vid>:<raw s>:by-<author slug>`. A `reading_fixes` entry may give such a reading its title.

**Alternative readings.** Where the two readers read the same spine differently, or a reader listed a `read_as` alternative in the
raw file, the readings are compared per sighting. The highest-confidence one is the book's `title` and `author`; on a tie the
first reading (`spines_zZEy10fpq3I_piano.jsonl`) wins, and `meta.counts.spine.alt_preferred` counts the books where the second
reading won. The others go to `alt_readings`, deduplicated by normalised title and author with an absent author matching any, and,
as strings, to `title_variants` ("Also read as" on the page). Spelling variants of the same reading are not alternatives; they are
`title_variants` only. `meta.counts.spine.alt_readings` counts the entries, and `piles_with_height` the piles rendered from a
`books_high`.

Readings whose frame names only the room are placed from the **shelf label** visible in the frame before falling back to the room
default. `wall_map_eco.json` `label_patterns` are `[regex, target, level?, name?]` rows matched against the wall name, view or
labels ("ECO IBERICI" and "Q4/Q5" to `study-Q`; "Pensiero Occidentale" and the L11.x and L12.x call tags to `study-L8-12`; the
FRANCOFORTE and DELEUZE subject tabs to `study-M-A` at level `label`), and a bare call tag `<letter><bay>[.shelf]` (A 48, L4.10,
Q4.9) is parsed into the Fondazione bay (`tag_targets`).

The level a row gives decides the placement. `wall` gives `placement: "seen"` with `shelf_label` on the book. `label`, a tab that
names a subject rather than a bay, gives `inferred` with a reason. `context`, a row whose text is the spine pass's own name for a
wall ("Own-works library wall", "Umberto Eco's own works" to `study-Q`), takes the bay as `inferred` at tier guess, with the note
"read on film at <time>; the shot shows no shelf tag, and bookcase <name> is inferred from the shot's context", and no
`shelf_label`. A `wall`-level row whose matched span is not tag-like (not a call tag, not upper-case lettering, not quoted) is
treated as `context` too, with a warning, so a pass's wall description can never stand as a shelf label. Only a frame with nothing
else known falls back to the room default, bay P in the study, as a `guess`.

`wall_map_eco.json` `patterns` may also send a wall label to `@subject` (the ANRW "archive shelf" and "classics reference set"
frames of the 2022 film, which name no room): the reading is placed by `subject_map_eco.json` from its title (`classics reference
sets (ANRW)` to bookcase I, the Fondazione's ancient-world caption) with placement `inferred`, tier `guess` and the note "the shot
shows no room or shelf label; the bookcase is inferred from the subject (...)". The "seen after the move to Bologna" wording is
kept for frames whose room label is the Bologna reinstallation. The `books by Eco` author rule also matches the readers' forms of
the name (`Umberto Eco`, `Umberto Eko`, `Умберто Эко`), so every filmed edition or translation of Eco's own books goes to bookcase
Q, never to the "materials on Eco" island. Where no subject rule matches a reading, the placement note reads "no subject rule
matches the reading, so a fallback bookcase of the room".

## Which sighting places a reading

Every sighting carries `level`: `bookcase` or `wall` (the reader's tag or wall label names the bay), `label` (a subject tab),
`context` (the pass's own description of the wall), `room`, `subject`, `fallback`, `pile`. The sighting that *places* a shelf
reading is the most specific one (bookcase or wall, then label, then the rest), then the clearest, then the earliest. A dense
sighting counts as naming the bookcase only when the pass placed it by a tag or a first-pass label. The clearest sighting still
gives title, author, `confidence` and the primary link. A `seen` book's tier follows the confidence of the sighting that named its
bookcase.

A consolidated sighting whose dense frame carries `timestamp_true_s` links to that true second (`timestamp_s`, `time`, `url`).
Pile sightings whose frame names no room of the flat are dropped from the piles, and a reading left with none goes to
`meta.counts.spine.rejected_other` with its `url`.

## Catalogue matching

A film or photograph reading may turn out to be a book the catalogues already hold. A dense-pass match or an exact-title candidate
attaches only when it agrees (`match_agrees`): the surname as a word of the record, allowing a Latin ending; or the whole title;
or two significant title words. `sive` and `seu` are stop words. The exact-title index keys a record by its title before the colon
as well, so a reading that is the main title alone meets its record.

A reading with any rare-room sighting is matched against the Braidense records. A working-shelf reading with no Bologna record is
tried against the Braidense rare-room records (the surname in the author or heading the Latin title, two shared words with a share
of at least 0.5, or three shared words), so a folio read on a working shelf is its record's sighting and never a second shelved
book. A title read on a shelf of the flat is a copy in the flat, drawn where it was read; the library's ECO.04 reference copy of
the same book is not that copy, and keeps `title_seen_on_film` instead.

When a tagged film sighting names a bookcase for a Bologna record, the record is moved there: `placement: "seen"`,
`seen_on_film_agrees`, and the note "read on film at ... on bookcase X (call tag ...); the subject rule 'R' had placed this record
on bookcase Y". The record carries `seen_by_tag` with `bookcase`, `time`, `url`, `video_id`, `how`, `tags`, `dense_id`,
`dense_tier`, `tag_verified`, `moved_from`, `rule` and `after_move`. It is certain only when the tag is verified in the frame and
the shot is in the flat.

`seen_elsewhere` records a reading of the record on another bookcase without moving it. It carries `level`, and its placement note
says "in the same room (the shot names no bookcase)" or "in a shot that names no room or bookcase" instead of naming a guessed
bookcase.

`seen_after_move` marks video books placed by a tag read in the Bologna reinstallation. Their tier reasons read "seen in the
Bologna reinstallation; the room and the bookcase are guessed from the subject, not read in the flat", "no room or shelf label in
the shot; the room and the bookcase are guessed from the subject, not read in the flat", or "read in the Bologna reinstallation at
a shelf carrying the Milan tag of bookcase X (the reinstallation keeps the tags); not read in the flat".

`second_copy` is set on Bologna records of one title by one author on one bookcase, with the note "two copies: ..." or "second
copy: the Bologna catalogue holds another record of this edition or title (a different edition or printing) on this bookcase,
UBO... (year, publisher)".

`meta.counts.spine` counts the outcomes: `catalog_match_rejected`, `catalog_forced`, `catalog_forbidden`,
`catalog_braidense_cross_room`, `catalog_moved_to_tag`, `pile_sightings_off_flat`, `pile_readings_off_flat`.

## The dense spine pass

The heavy spine pass (`eco-video/dense/`, converted to the eight `eco-video/spines_<video>_dense.jsonl` files) adds, on video books
and on the catalogue records it matched:

* `dense_ids`: the pass's `video:<id>:<second>:<slug>` ids behind the book's sightings.
* `dense`: `{ids, tier, reason, placing, placing_tier, placing_reason, placing_basis, tag_verified, tags, sightings,
  first_pass_sightings}`. The pass's own tier is `certain`, `probable` or `guess`, with its reason in words; `placing` says how the
  frame was placed (a call tag in the frame, a tag in the same shot, the first pass's wall, the room); `tag_verified` says whether
  the map's own parser accepts that tag; and the two sighting counts say which sightings come from which pass.
* sightings may carry `dense_id` and `dense_tier`.
* on catalogue records: `dense_match` (`kind`, `score`), `seen_on_film_agrees` (the pass read the record on the bookcase the
  shelfmark or the subject rule gave it; Bologna records so confirmed become `seen`) and `seen_elsewhere` (read on another
  bookcase; the record is not moved).
* tier reasons: "dense pass probable: ...", "dense pass guess: ..." and "dense pass read the full title on bookcase X, but the call
  tag that placed it ... is not in the frame or the same shot, or is not a tag the map recognises" (a dense `certain` kept at
  guess). A dense `certain` with a verified shelf tag stays certain, `probable` and room-only placements are guess, and books of
  other libraries are never shelved in the flat.
* `meta.counts.spine` gains the `dense_*` counters, among them `dense_conflict_dropped` (first-pass sightings that lost their slot
  to a dense reading of the same frame under the same-slot rule, `eco-video/dense/conflicts_resolution.json`) and
  `dense_conflict_readings_lost`. A reading can be rejected with "every sighting lost its slot to a dense-pass reading".

## Certainty tiers

Every book and every object carries `tier` and a short `tier_reason`. The tier says how far the *position* is evidenced, not
whether the book existed: every identified book is a real record or a real reading.

| tier | books | objects |
|---|---|---|
| `certain` | `placement: catalogued` with an ECO.01 shelfmark (the running number keeps the order of the shelves: "Braidense shelfmark ECO.01.0412, in the rare-book room's shelf order"); `placement: seen` with confidence `high` or `medium` at an identified bookcase ("read on film at 00:42:56 at bookcase P", "read in photograph fondazione_17_I.webp at bookcase I"); a pile book with that confidence whose pile is itself `certain` | placed by an `objects_map_eco.json` rule (a `position` or an `anchor`, that is, a position note) from a film frame or photograph that shows it |
| `guess` | Braidense ECO.02 and ECO.03 records (sections of the catalogue, not shelves: "Braidense shelfmark ECO.02.0136: section ECO.02 records books kept in the room off its shelves (on the desk, for example); the cabinet is a stand-in"); ECO.04 reference entries ("Braidense reference section ECO.04 (ECO.04.0001): the library's set of Eco's own publications; presence and position in the flat not established"); Bologna records ("Bologna record placed by subject rule 'semiotics'"; "Bologna record with no subject match; not shelved (Milan position unknown)" for the `unshelved` ones); readings resolved only to a room, a subject tab or by subject ("reading names only the room (studio); bookcase guessed (no shelf label visible in the frame)", "shelf label names a subject ('FRANCOFORTE / DELEUZE'); the bay is inferred from the Fondazione caption", "seen after the move to Bologna; Milan bookcase inferred from the subject"); low-confidence readings; pile books whose pile position is a guess; the two Braidense records without a parsable shelfmark | auto-placed from a position hint, set in front of or on top of a bookcase that objects.json only names, piles built from the spine readers' frames (set on the room's first table), layout.json furniture |
| `unknown` | the filler ("empty slot") | never: every object is evidenced by a frame, a photograph, a text or the layout |

`meta.counts.tiers` gives the totals, `by_room`, `by_bookcase`, `objects` and `reasons`, the reason strings with the varying parts
elided so that a reader can see what the tiers rest on. The same counts sit in `meta.counts.by_room[].by_tier` and
`rooms[].bookcases[].counts.by_tier`.

## Object geometry

`objects[]` carry, next to the page's `size` (`[w, h, d]`) and `rotation`:

* `shape`: a semantic shape for the page's mesh library, from the object kind and its labels. `desk_L` (the L-shaped study desk),
  `desk`, `table` (round, coffee, dining, oak, console tables), `chair`, `armchair` (club, leather, Eames, lounge), `sofa`,
  `lamp_floor`, `lamp_desk` (also the reading lens and brass lamps), `ladder`, `piano_upright`, `piano_grand`, `glass_case`,
  `artwork` (canvases, panels, assemblages), `print` (framed prints, engravings, maps, drawings, photographs, posters,
  caricatures, comics, calligraphy, mirrors), `sculpture` (statues, busts, figurines, the plaque), `globe` (globe, orrery), `jar`,
  `instrument` (lute, recorders, music stand), `pile`, `rug`, `box` (cabinets, chests, filing cabinet, CD tower, TV, stool,
  diorama boxes, trays), `other`.
* `primitive`: what `objects_map_eco.json` `shape` said: `cylinder`, `sphere`, `torus`, `stand`, `flat`, `lute`, `window`. Absent
  means a box.
* `dims_m`: `[w, d, h]` in metres when the experience record's modelling note states a size (`2.4 x 1.0 x 0.78 m` is width by
  depth by height; two numbers are width by height for artworks, width by depth otherwise) or the object's
  `objects_map_eco.json` rule states `dims_m` (the piano piles: 0.22 by 0.16 m and 0.0245 m per book counted). Absent when the
  size is only the kind's default or a rule's guess.
* `against_wall`: the bookcase id the object stands in front of or on top of (its rule's `anchor.bookcase`, or the bookcase
  objects.json names). Absent for free-standing objects and for objects on other objects (`on`, or the rule's `anchor.object`).
* `facing`: degrees, the object's front direction (`rotation` mod 360; 0 faces +z, the same convention as `rotationY` on
  bookcases).
* `fitted` and `fit_note`: an object anchored on another whose rule offset put it past its support's top by less than its own
  half-width is drawn at the edge of the support, and the note says so.

## Object thumbnails

Every object that has a frame or a photograph gets `thumb`, a JPEG data URL of a crop of it, at most 256 px on the long side,
quality 68. The whole set is kept under 2.5 MB by lowering the quality in steps of 8, then dropping the lowest-priority kinds:
artworks, curiosities, desks, piano and piles come first.

The image is the experience record's own `source.image` when it has one (the film frame or photograph the brief chose for the
object), else the film inventory's `best_frame`, else, for piles from the spine readers' frames, the frame of the first reading.
The crop is an explicit `bbox` or `crop` `[x0, y0, x1, y1]` (fractions of the frame, or pixels) when the object record, the
sighting or the objects_map rule gives one (`thumb_crop: "bbox"`); otherwise the centre 60% of the frame, 50% for artworks, slid
towards the side the position hint or modelling note names (left, right, above, high, top, floor, below, bottom:
`thumb_crop: "hint"`, else `"centre"`).

`thumb_frame` names the file and `thumb_bytes` the JPEG size; `meta.counts.objects_thumbs` has the totals. Artworks also get
`art_aspect` (w/h): the note's size when it states one, else the crop's. The frames themselves are never copied into `books.json`.

## Overlay counts

The page's overlays recolour the spines per book and tint the shelf frames where the dimension is per bookcase. The legends read
their counts from `meta.counts` and fall back to counting `books[]` when a key is absent. The classes are computed the same way
for the library (`meta.counts.by_*`), each room (`meta.counts.by_room[].by_*`) and each bookcase
(`rooms[].bookcases[].counts.by_*`).

| overlay | key | class of a book |
|---|---|---|
| Subject | `by_subject` (library: a list with the bookcases and rooms of each caption; room: `{caption: n}`); per bookcase it is `bookcases[].subject` | the Fondazione caption of the bookcase the book sits on (layout.json `subject`, `subject_it`) |
| Source | `by_source` | `video`, `photo`, `braidense`, `bologna` (or `aib-2022`), `unlabelled`: `origin`, with `catalog` split by `catalog` |
| Certainty | `by_tier` / `meta.counts.tiers` | `tier` |
| Century | `by_century` | `year` by hundred-year block, `1400s` to `2000s`; `unknown` when the record or reading has no year; `unlabelled` for the filler |
| Language | `by_language` | `language` (ISO 639-1); `unknown` and `unlabelled` as above |
| On film | `on_film`, `rooms[].bookcases[].on_camera` | the bookcase was on camera (a reading, a pile or an inventoried object of the film was placed on it) |
| Eco's hand | counted by the page from `copy.marks` (`meta.counts.catalog.bologna_copies.hand` is the generator's tally) | `4`, `3`, `2`, `1`, `0`: how many of marginalia, underlinings, dog-ears and inserts the copy note records; a copy record without a `marks` array is `0`, a copy with no mark noted. `-1`: no copy record (a rare book, a film reading, a photographed book, the one Bologna record without one). `unlabelled` for the filler, by origin, so a reading with no title is still a reading |
| Given to Eco | counted by the page from `copy.givers`, `copy.marks` and `copy.inscribed_by_eco` (`bologna_copies.given` is the generator's tally) | `named`: a giver is named. `unnamed`: a dedication noted, no name. `eco`: a dedication in Eco's own hand, "Inscribed by Eco himself". `plain`: a Bologna copy without a dedication, and a copy record without marks. `none`: no copy record. `unlabelled` for the filler. The legend lists `bologna_copies.top_givers` as links into Eco's copies |

A Bologna record with a copy record is "Eco's copy": the colour, the tooltip, the legends and the copies list share that one
definition. `meta.counts.overlay_note` gives one sentence per overlay stating what it rests on, for the About panel.

## Bologna placement

`classify()` tries the record's own fields first: `author` regex on the 700 author, `dewey` prefixes, `publisher` regex on the
210 $c imprint, `subjects` regexes on the subject headings and Dewey labels alone, `keywords` on subjects plus Dewey labels plus
series plus title plus title_full, accents folded. Only when nothing matches does it retry with the UNIMARC 461 set title and the
responsibility statements (200 $f/$g) appended to the keyword text, so numbered volume parts ("2", "Vol. 1", "1: A-E") are placed
by their set without moving any record the plain fields already place. `placement_match` on the book and
`meta.counts.catalog.bologna_matched_via` say which pass placed it, and `bologna_rescued` lists the records placed only by the
second pass, to check.

A record neither pass places is **unshelved**: `placement: "unshelved"`, `bookcase`, `shelf`, `slot` and `section` null, tier
`guess`, and the placement note "no subject match; not shelved on any bay (the Milan position of this record is unknown)". It
stays in `books[]` for search and the Notable list but occupies no slot, so the fiction corridor does not collect the
unclassifiable records. `meta.counts.unshelved` and `meta.counts.catalog.bologna_unshelved` (the ids) count them, and
`bologna_placement_unknown` is the same number.

The imprint (210 $c) is exposed to the rules only through a rule's own `publisher` regex, matched in both passes: in the keyword
text, university presses and "Edizioni di Storia e Letteratura" would hit generic words such as `universit` and `letteratur`.

A rule's `subjects` regexes are read on the record's subject headings and Dewey labels alone, never on the title or the series.
Five such rules stand before the topical rules of the study and the corridors (`subject_map_eco.json`: "Italian literature",
"French literature", "English-language literature", "German literature", "other literatures ..."), each with the Dewey prefixes of
its literature (850-859, 840-849, 810-829, 830-838, and 839, 860-869, 891-899; the classical literatures 870-889 stay with the
ancient-philosophy rule) and the same name and bookcases as the keyword rule of that literature further down, so the cataloguer's
own class puts a novel on its corridor before a word of its title can put it on a study island. The literary-theory island's rule
does not match the bare word "narrativa", the Dewey label of every post-war Italian novel, but narratology, narrativity or a
narrative word joined to a theory word. `placement_rule` and `tier_reason` name the rule, and a record placed by a class-first
rule prints the same rule name as one placed by the keyword rule of the same literature.

## Descriptions

`descriptions_eco_overrides.json` (review overrides) is read first and wins outright: a `verified: true` text is used as it
stands, and a `description: null` entry with a `rejected` note blocks every fetched description for that id. Then
`descriptions_eco.json` (when present) and `descriptions_eco_seen.json`, `descriptions_eco_braidense.json` and
`descriptions_eco_bologna.json` next to it are merged in that order. The first file with a description for an id wins; any of them
may be absent or partial. The fetch scripts rewrite the fetched files wholesale, which is why the overrides live apart. A reading
merged into a catalogue record also takes the description of any of its `merged_ids`. `meta.mappings.description_files` reports
per file `entries`, `used` (entries with a description not already taken), `applied` (books carrying a description from that file)
and `by_kind`.

Every fetched description is validated on merge (`validate_description`; entries marked `verified: true` bypass it). A rejected
description leaves the book with `description_kind: "none"` and no description. The book itself does not carry the reason; the
totals are in `meta.mappings.description_validation.by_reason` and the reason for each book in its `rejected_ids` list, one entry
per book with `id`, `title`, `author`, `wikipedia_title`, `kind`, `reason` and `file`. The grounds for rejection:

* a disambiguation page;
* an article whose first sentence says the subject is a film, opera, television series, album or fictional character rather than
  the book (the Italian "opera", meaning work, is not a medium);
* an `author` fallback whose book author is empty (unless the article's person heads a Latin title, "Athanasii Kircheri ...") or is
  a role statement ("a cura di", "introduction by", "herausgegeben von", "compiled by"), or whose article names neither the author
  nor the book;
* a title article sharing no word (four-letter Latin-folded stems, or the whole short title: "Là-bas") with the book's title, set
  title, variants or author;
* an article on a work merely named inside the book's title ("Leggere I promessi sposi" is not the novel, while "Athanasii
  Kircheri ... China ... illustrata" is Kircher's own book because the leading words are the author);
* a truncated text (unbalanced parentheses, an ending such as "geboren 5." or "vol.") that has no earlier complete sentence to cut
  back to;
* an `edition` description (a card read from a frame, "<Language> edition of ...") whose leading language word names a language
  other than the entry's `language` (`edition_contradiction`), so that a card never says one language on its Language row and
  another in its text.

Cleaned rather than rejected: IPA pronunciations, a truncated last sentence when a complete one precedes it, and a
"By <author> (b. YEAR):" prefix whose birth year is implausible for the book's date (fewer than 12 or more than 110 years before
it).

## English titles

`titles_en_eco.json` and `descriptions_en_eco.json` sit next to the generator and drive the page's Native / English switch.

**The rule.** The native title is the default and is never replaced. It stays in `title`, and it is what the page shows unless the
reader turns the English button on. Nothing in the data is overwritten. Books with no entry keep their native title in both
modes: they are already in English, or they are proper names, or they are fragments. An entry of kind `literal` is a translation
made for this map, not the title of any English edition, and the page marks it as such so that a reader does not go hunting for an
edition that does not exist.

**How an entry is keyed.** By the book id of `books.json`: `braidense:<bid>`, `bologna:<UBO id>`, `video:<video>:<second>:<slug>`,
`photo:<stem>:<slug>`. A book takes an entry keyed by its own id or by one of its `merged_ids`. Ids added by a later build have no
entry until the file is refreshed.

**The fields.** Both files are optional, may be partial, may be a list of `{id, ...}` instead of an object, and keys starting with
`_` are notes. `descriptions_en_eco.json` accepts `description_en` or `description` for `desc_en`.

| field | meaning |
|---|---|
| `title_en` | the English title |
| `kind` | `published` (the title of an English edition, or the standard English name of a classical work) or `literal` (a faithful translation made here) |
| `source` | where the English title comes from, as a reader-facing string: `literal translation`, `English edition (publisher, year, translator)`, `English original (publisher, year)`, `standard English title`, or a Wikipedia or Wikidata address |
| `confidence` | `high`, `medium` or `low` |
| `desc_en` | in `descriptions_en_eco.json`: the description rendered in English |

On the book these become `title_en` (string), `title_en_kind` (`published` or `literal`), `title_en_source` (string, optional) and
`desc_en` (string, optional). An English title equal to the native one, ignoring case, is dropped and counted in `same_as_native`;
entries for ids not in the library are counted in `unmatched`; books with a non-English title and no entry are counted in
`no_entry`, by origin. `meta.english_titles` is true when at least one book carries `title_en`, and the page shows its English
button only then. `meta.counts.english_titles` is `{books, published, literal, descriptions, same_as_native, unmatched, no_entry,
files: [{file, entries}]}`.

`desc_en` is shown in English mode with the same source link and the words ", translated here". Descriptions already in English,
and the catalogue notes on the incunabula, need no entry.

Examples:

| id | native | English | kind |
|---|---|---|---|
| `braidense:MOD1707629` | Il nome della rosa | The Name of the Rose | published |
| `bologna:UBO00307638` | Lezioni americane : sei proposte per il prossimo millennio | Six Memos for the Next Millennium | published |
| `bologna:UBO00421351` | La struttura delle rivoluzioni scientifiche | The Structure of Scientific Revolutions | published |
| `bologna:UBO01012639` | Trattato di semiotica generale | A Theory of Semiotics | published |
| `bologna:UBO01141995` | I promessi sposi | The Betrothed | published |
| `bologna:UBO00436664` | Torah e filosofia : percorsi del pensiero ebraico | Torah and Philosophy: Paths of Jewish Thought | literal |

Two conventions hold across the file. Volume numbers in `title_en` follow the native title exactly, lower-case "vol." with the
catalogue's numbering, such as "vol. 2.1". Early-modern Latin and German titles are shortened to the work, and dedications and
printers' puffs are dropped.

## Vocabulary

* `origin`: `video` (spine read in a frame of a listed video), `photo` (read in a published photograph), `catalog` (Braidense
  rare-book record with the Milan shelfmark, or Bologna record placed by subject), `unlabelled` (placeholder).
* `placement`: `catalogued` (the shelfmark fixes the run and its order; the cabinet is a guess), `seen` (the reader placed it on
  that bookcase or pile, or a shelf label in the frame names the bay), `inferred` (subject rule, subject tab, room-level reading,
  or the fallback bookcase), `unshelved` (a Bologna record no rule places: on no bay), `reference` (a Braidense ECO.04 record, on
  the study's reference table, its presence in the flat not established), `filler` (placeholder).
* Resolution levels of a reading (`meta.counts.spine.frames_by_level`): `bookcase` and `wall` (a wall name or a shelf label or
  call tag naming the bay) give `seen`; `label` (a subject tab), `context` (the pass's own description of the wall), `subject`,
  `room` and `fallback` give `inferred` with a `placement_note`; `pile` makes a pile object.
* `tier`: `certain`, `guess`, `unknown`. `confidence`: `high`, `medium`, `low`.
