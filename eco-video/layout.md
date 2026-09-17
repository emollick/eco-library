# Eco's Milan apartment: what layout.json rests on

Companion to `layout.json`, the reconstructed plan of the flat at Piazza Castello 13. The plan
is a reconstruction from public photographs and visitor accounts. No floor plan of the flat
exists in the sources.

## What the sources support

- **Structure.** The Fondazione's "Le biblioteche" page describes a ring-shaped flat with
  reinforced floors and full-height shelving along the corridors (literature, poetry, genre
  fiction, comics, criticism, press and media, art) leading to the big study with its "pettine e
  isola" (comb and island) bookcases, plus the Stanza degli antichi with a balcony on the
  Castello. The 2022 CriticaLetteraria visit gives the walk: salotto, then vestibolo (Joyce,
  Kabbalah, magic, alchemy), then corridoio (the "bosco narrativo", comics top and bottom), then
  studio (dictionaries behind the desk, a whole wall of philosophy from the Presocratics,
  semiotics opposite, his own works in 60 languages and more). Zanni's 2010 account adds:
  corridor fiction only; study right wall his translations, far right books about him; centre
  islands and boxes.
- **Bookcases.** The Fondazione scrollwall galleries are rectified frontal photographs of every
  white bookcase, lettered A to S with a subject caption. Counted by eye at 650 px: A = 25
  corridor bays x 11 shelves (4 above a ladder rail, 7 below); B, C = 3 bays (one half bay) x 11;
  D and I = door surrounds (2 full bays each side, a 2-bay or 1-bay bridge over the door); E = 5
  bays x 5 (low); F, G = 2 bays x 10 (top cropped); H = 7 x 11; L = 4 + 3 + 5 bays x 11; P = 10
  bays x 10 (black box files on the bottom shelf); Q = 6 x 11; M-A and M-B = 5 bays x 6, low, two
  faces of one island; Na, Nb, Nc and Oa, Ob = 3 (or 2 plus end panel) bays x 4 open shelves over
  cupboards; R = 3 x 6; S = 3 x 5. Bay width is taken as 0.80 m (panel proportions give about
  0.77 m), half bays 0.40 m, full height 3.5 m, low units 2.1 m.
- **Rooms read from wide photographs.** The corridor has shelves on one side only, framed prints
  opposite, and is about 1.6 m wide. In the study the bottom row of box files identifies P as the
  long left wall in criticaletteraria_2022_11 and _13, the red Treccani-type set on top of the
  nearest island matches Oa, and the door with over-door shelving in _5 matches I. The rare-book
  room has cherry glazed cabinets on both long walls, an oak table in the middle, a balcony at
  one end and a door with white shelving beyond at the other. The family says the original room
  was elliptical (Rivista Studio 2022); the photographs read as a rectangle, so it is drawn
  6.5 x 3.6 m rectangular.
- **Rare-book order.** The Braidense shelfmarks ECO.01 to ECO.04 plus a running number preserve
  Eco's own shelf order: ECO.01 runs to 1107 (997 used; hermetica and curiosa), ECO.02 to 169
  (19th-century French sets), ECO.03 to 77 (37 used; the most precious books), ECO.04 to 102 (his
  own works). At 30 to 40 volumes per metre the 1,328 volumes need about 34 to 47 shelf metres;
  the two surveyed wall cabinets (6 columns x 7 rows, about 5.8 m each) give some 80 m, so the
  room is loosely shelved with mirabilia between the books. Which run stood on which wall is a
  guess (ECO.01 left then right, ECO.02 and ECO.03 right, ECO.04 on the low door-end shelf).

## The rare room and the walk order

ECO.03 is the section of most precious books, not an incunabula section: Dee 1564, Bruno 1582,
Khunrath 1609 and Locke 1690 stand there alongside the incunabula (Braidense; AIB Studi 2022).
It has its own glazed cabinet in the plan, `rare-04`, captioned "most precious books (ECO.03)"
and drawn on the balcony wall beside the balcony door; the running numbers give the order within
the run, not the wall, so the placement is a guess. `rare-02` holds the end of ECO.01 and the
French sets of ECO.02. Seventeen of Eco's 36 incunabula are absent from the Braidense export;
the map adds them from the incunabula list in `eco-sources/experience/` as catalogue books
(source AIB Studi 2022, with ISTC ids) on that wall.

The Stanza degli antichi sits at the start of the long corridor that leads to the study, not at
the end of the walk, so the room order is salotto (1), vestibolo (2), antichi (3), corridoio (4),
corridoio-arte (5), studio (6). The room's door is on its S wall and opens onto the corridor's
print wall a few metres after the vestibule, recorded as `doors_extra` on the corridor.

The vestibolo is a passage, drawn 3 x 4.5 m. The salotto door is on its N wall, offset 0.5 m and
aligned with the salotto's S door; bookcase D and its door bridge are on the E wall opening into
the corridor, whose W doorway is D's 1.45 m door span; C stands on the S end wall beside the
GOSH! picture, and B with the coats and prints opposite. The map's world plan
(`gen_books_eco.py` ROOM_PLAN) follows the same order: salotto, vestibule below it, corridor
running east from the vestibule, the art leg and the study at the far end, the rare room north
of the corridor start.

## Counts and reconciliation

- 6 rooms, 53 bookcase records, 134 bays: salotto 3 (E, vitrines, wooden cabinet), vestibolo 3
  (B, C, D), corridor 25 (A1 to A25), second corridor 3 (F, G, H), study 15 (I, L x3, P, Q, R, S,
  M x2, N x3, O x2), Stanza degli antichi 4 (rare-01 to rare-04).
- Shelf metres: working library about 804 m (corridor 220, study 392, art leg 94, vestibule 70,
  salotto 43 including objects), and 911 m in all with the rare room.
- At 33 to 40 volumes per metre the working shelving holds some 26,500 to 32,200 volumes against
  the Fondazione's figure of about 33,000 (32,000 and more moved to Bologna). Bologna re-shelved
  them on 600 linear metres (about 53 per metre), so Milan capacity exceeds the count. That fits
  the photographs: gaps, flat piles, boxes on the floor, and piles on the piano and the tables
  that the plan does not model. If bays are 0.75 m the figure drops about 6 per cent; if F and G
  have an eleventh shelf it rises about 0.3 per cent. The A to S survey plus the rare room
  accounts for essentially the whole library, and no unphotographed room of shelving is needed.

## Open questions (confidence flags in the JSON)

1. The rooms for C (books on books), E (ancient art) and F, G, H (art, design, aesthetics) are
   placed in the vestibule, the salotto and a second corridor leg on subject grounds only (low
   confidence). The Fondazione text puts "arte e iconologia" in the corridors, and E may be a
   salotto unit.
2. Which door D and I frame (vestibule to corridor? salotto to vestibule? corridor to study?),
   and where the Stanza degli antichi opens. Its door photograph shows white full-height shelving
   beyond, so the far side is a corridor or the study.
3. Whether L1-12 continues on the same wall as I (drawn as one 13.2 m N wall) or turns a corner;
   whether R and S are wall units or islands.
4. How the island faces pair back to back. M-A and M-B are assumed to be one island; Na, Nb, Nc
   and Oa, Ob are drawn as comb teeth in front of P.
5. Compass orientation. Wall letters are map-local. The balcony faces the Castello, and the flat
   is on Piazza Castello 13, top floor.
6. Where a bookcase sits along the film's timeline. The 2015 Ferrario walks and the 2022 film are
   listed as sources, but no bookcase cites a frame time. The film's 00:00:53 to 00:01:02 (floors,
   eviction) and 00:01:38 (his own books and translations, that is Q and M-B) are the only caption
   anchors the plan uses.
7. The Fondazione's high-resolution originals and the Unibo shelf-by-shelf survey would settle bay
   widths and every open point above. Neither is public.
