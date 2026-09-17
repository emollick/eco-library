# objects.json

95 non-book items of the Milan flat, Piazza Castello 13 (ids o01 to o95): rooms and fixtures (4 room records, 2 corridor records, 8 fixtures, 8 rare-book-room fixtures), furniture (18), artworks (11), piles (10), objects and curiosities (34). Built from `objects-notes.md` and the frame corpus under `/mnt/project-files/eco-video/frames/`; nothing was measured, sizes in `modelling_note` are estimates from the footage.

## Fields

| field | meaning |
|---|---|
| `id` | `o01` to `o95` |
| `item` | short label |
| `kind` | room, corridor, fixture, furniture, artwork, pile, object, rare-book-room-fixture |
| `room` | salotto (31), studio (30), antichi (17), corridoio (11), vestibolo (6). No record sits in `corridoio-arte` (see below) |
| `bookcase` | a `books.json` bookcase id when the object belongs to one (study-Q, corridor-08, salotto-vetrine, rare-01 ...), a slash list when several, null otherwise (68 records) |
| `description` | what is seen, with colours and materials |
| `source` | `{type: video or photo, video_id, timestamp_s, url, image}`. `image` is `frames/<file>` for a frame copied into `experience/frames/` (74 key frames), an absolute path under `/mnt/project-files/eco-sources/eco-photos/` for a published photograph, or null for the 14 sightings with no frame (o18, o58, o87, o88, o93, o94, o95 and some `also_seen` entries) |
| `also_seen` | further sightings in the same shape as `source` |
| `confidence` | seen-clearly (88), partially-seen (6), reported-in-text (1: o58, the Arman collage and lute mentioned by the Paris Review) |
| `modelling_note` | suggested size, position and level of detail for the 3D model |

Frame names: `film_t_HHMMSS.jpg` = zZEy10fpq3I (1920x1080, labels uncorrected: true source time = label + 0.96 s); `p1_`, `p2_`, `p3_` = Hq66X9f-zgc, zj1kwT87ne0, B-M8V0PcCrw (854x480, labels already corrected). `timestamp_s` in `source` is the frame label; the `url` already carries `&t=`.

## Walk order (the 2015 Steadicam take, Hq66X9f-zgc 288-372 s; repeated in reverse in the 2022 epilogue, film 4420-4545 s)

| # | room id | what is there | record ids |
|---|---|---|---|
| 1 | `salotto` | Living room. Cognac club armchair (interview seat), upright piano with piles, white plaster nude, three glass vitrines with shells, coral and open antique books, wooden cabinet of curiosities, white sofas, black coffee table with piles and an orrery, TV, floor lamps, burnt-book artwork, framed drawings, miniature library diorama. Windows toward the Castello. | o01, o09, o10, o18-o28, o52-o55, o58-o65, o79-o81, o92, o94 |
| 2 | `vestibolo` | Short passage between salotto and corridor. Coats on hooks both sides, wall of framed prints on the left, white shelves (vest-B/C/D) on the right, GOSH! pasta-flag assemblage on the end wall, black twisted mobile. The door of the rare-book room opens off this passage. | o02, o29, o47-o49, o66 |
| 3 | `corridoio` | The long corridor (about 20 m). Bookcase A (corridor-01..25) along the right wall; left wall shelved only for the first third, then plain with framed prints; sliding ladder on a rail; comics on the top and bottom shelves; horizontal overflow. Ends in a small lobby: French window with iron bars, radiator, speckled grey canvas. | o03, o04, o17, o30, o50, o51, o77, o82, o88-o90 |
| 3b | `corridoio-arte` | Possibly not a separate leg. The shelved stretch on the left at the start of the corridor is the best candidate for cases F/G/H (aesthetics, architecture, contemporary art). Low confidence, no object records. | none |
| 4 | `studio` | The big study, entered by a left turn just before the corridor end (folding step-ladder at the door). Long walls L and P; islands M/N/O forming an aisle; Eco's-works bay Q with the carved plaque; L-shaped black desk with computer under the windows; dictionaries (Nb) behind the desk; door with pinned notes (I) where Eco takes a red-spined book; black round pedestal table, black leather sofa and armchair, wheeled filing cabinet; ceiling fans; windows on an internal terrace with planters. | o05, o07, o11-o15, o31-o39, o56, o71-o76, o78, o83-o86, o91, o93 |
| 5 | `antichi` | Stanza degli antichi, off the vestibule, balcony facing the corner tower of the Castello. Cherry glazed bookcases with drawers (rare-01..03), oak table with six chairs, vellum quartos, magnifying lens on a stand, gilt reading tray, glass case with white porcelain, armchair and floor lamp by the balcony, music stand with score and recorders, pendant lamp on a ceiling rail, framed engravings and maps, specimen jar "Canis familiaris". The family say the room was elliptical. | o06, o08, o16, o40-o46, o57, o67-o70, o87, o95 |

Eco's route timed on Hq66X9f-zgc (film label in brackets): 293 [46] rises from the armchair, passes piano (left) and statue (right), exits the salotto door; 301 [54] vestibule, coats, GOSH! ahead; 305 [58] turns right past the print wall; 309-321 [62-74] long corridor, case A on the right, ladder; 327 [80] balcony door ahead; 329-331 [82-84] turns left into the study past the step-ladder; 341 [94] aisle between the islands; 345-347 [98-100] desk; 349-357 [102-110] door with notes, takes a red-spined book, leafs through it; 361-371 [114-124] wide shot walking away down the study, fans and round table.

## ASCII floor plan (hypothesis)

```
                              N (Castello side, Piazza Castello)
   +----------------------+     +-----------------------------+
   |  ANTICHI  (rare)     |     |          SALOTTO            |
   |  balcony -> Castello | [d] | piano  statue  vitrines x3  |
   |  oak table, cherry   |     | armchair sofas TV  cabinet  |
   |  cases rare-01..03   |     | windows -> Castello         |
   +--------+-------------+     +--------------+--------------+
            | door (off vestibule)             | door (frames)
       +----+----------------------------------+----+
       |  VESTIBOLO: coats | prints(left) | B,C,D (right) | GOSH! wall
       +----+----------------------------------+----+
            | right turn
   +--------+------------------------------------------------------+---+
   | CORRIDOIO  case A (corridor-01..25) along the right wall ---> |   |  balcony door
   |            left: F/G/H? shelves (first third) then prints     | L |  (iron bars,
   |            sliding ladder                                     |   |  radiator,
   +---------------------------------------------------------+-----+---+  speckled canvas)
                                                             | left turn (step-ladder)
                     +---------------------------------------+-----------+
                     |  STUDIO                 windows -> internal terrace |
                     |  P wall (box files)      desk (L-shaped)  Nb dicts  |
                     |  islands M / N / O  <-- aisle -->   Q (Eco bay)     |
                     |  round table, black sofa, filing cab.  [door I,     |
                     |  fans                                   notes]      |
                     +----------------------------------------------------+
```

Confidence: salotto -> vestibolo -> corridoio -> studio adjacency and the two turns (right, then left): high, seen in two independent takes. Rare room off the vestibule: high (film 424 s shows coats and white shelves through its door; the Braidense family text places it "all'inizio del lungo corridoio che porta allo studio"). Rare-room balcony to the Castello: high (Fondazione caption, film 306 s). Orientation of the study relative to the corridor, the position of the terrace, and whether the study far door (I) closes a ring back toward the salotto: low, never filmed. Corridor length is an estimate from walking time (about 18 s at walking pace). No floor plan exists in any source.

## Fondazione letter to room hypothesis

- A (corridor-01..25): corridor right wall. High.
- B, C, D: vestibule white shelves; D's door surround may frame the rare-room or the salotto door. Medium.
- E: low case behind the vitrines in the salotto (ancient-art catalogues). Low.
- F, G, H: left-hand shelved stretch at the corridor start (`corridoio-arte`). Medium-low.
- I: surround of the study far door with pinned notes (Eco takes a book there). Medium.
- L, P: long study walls (P has a bottom row of black box files). High.
- Q: Eco's own works bay, labels Q4/Q5/"ECO IBERICI", carved plaque. High.
- M, N, O: study islands (Nb dictionaries behind the desk; Oa carries the red Treccani set). High.
- R, S: small units in the study. Medium.

## Ten iconic moments for a "replay Eco's walk" feature

Times: Hq66X9f-zgc (colour, 480p) and the film zZEy10fpq3I (black and white, 1080p). The black-and-white opening credits of the 2022 film (about 46-136 s) are the same 2015 Steadicam take in 1080p: `film_label = Hq66_t - 247` (checked on 301/54, 327/80, 349/102). Frame labels of the film are uncorrected; the true source time on the YouTube clock is `film_label + 0.96`. Frame timestamps are sampled every 2 s, so all values are within 1-2 s.

| # | Hq66X9f-zgc (s) | film label (s) | film source time (s) | what happens | key frames |
|---|---|---|---|---|---|
| 1 | 293 | 46 | 46.96 | Eco rises from the armchair; piano with piles left, white statue right, framed pictures round the salotto door | p1_t_000453, p1_t_000455 |
| 2 | 301 | 54 | 54.96 | Vestibule: coats on both sides, GOSH! pasta flag straight ahead, black mobile above | p1_t_000501, film_t_000054, film_t_000056 |
| 3 | 305 | 58 | 58.96 | Turn right past the wall of framed prints; white shelves B/C/D on the other side | p1_t_000505, p2_t_000505 |
| 4 | 309-321 | 62-74 | 62.96-74.96 | The long corridor, case A sliding past on the right, ladder on its rail, prints on the left | p1_t_000509 to p1_t_000521, film_t_000102, film_t_000104 |
| 5 | 327 | 80 | 80.96 | Corridor end: French window with iron bars, radiator, speckled canvas | p1_t_000527, film_t_000118, film_t_000120 |
| 6 | 329-331 | 82-84 | 82.96-84.96 | Left turn into the study past the folding step-ladder | p1_t_000529, p1_t_000531, film_t_000124 |
| 7 | 345-347 | 98-100 | 98.96-100.96 | Arrival at the L-shaped desk under the windows; dictionaries behind | p1_t_000545, p1_t_000547, film_t_000142 |
| 8 | 349-357 | 102-110 | 102.96-110.96 | Door with pinned notes; Eco takes down a red-spined book and leafs through it | p1_t_000549 to p1_t_000555, film_t_000144 |
| 9 | 361-371 | 114-124 | 114.96-124.96 | Wide shot, Eco walking away down the study; ceiling fans, round table, black sofa | p1_t_000601, p1_t_000609, film_t_000156 |
| 10 | none (2022 only, colour) | 4442-4526 | 4442.96-4526.96 | Epilogue: salotto reveal with vitrines and orrery (4442), girl on roller skates to the corridor-end balcony door (4504), round table with piles (4510), rare room through to the corridor (4526). Use as the return leg | film_t_011402, film_t_011412, film_t_011504, film_t_011510, film_t_011526 |

Also useful: film 306-326 (rare-room balcony, wooden cabinet, plaque and Q labels: film_t_000506 to film_t_000526), 460 (rare-room table with lens and vellum quartos: film_t_000740), 3220-3240 (music stand, recorders: film_t_005340), 3050-3058 (salotto artworks, GOSH! in colour: film_t_005050 to film_t_005058), 2574-2600 (piano piles and corridor comics: film_t_004254 to film_t_004320).

## Honest limits

No floor plan exists; the sketch is inferred from camera turns and walking time. What lies beyond door I is never shown. E in the salotto and F/G/H on the corridor left are inferences. In the 2015 walk (480p) spines are illegible; the 1080p film credits fix textures but are monochrome. The Arman collage and the lute (Paris Review 2008) were not found in any frame. The recorder clip at film 3240 is probably Monte Cerignone, not Milan (o87). Pile contents are legible only on the piano top (Vattimo, Morandi, MacGregor, "Der ewige Faschismus", "Il nome della rosa", "I mutanti") and in case Q; all other piles are generic stacks. o95 is the Braidense reconstruction, not the flat.
