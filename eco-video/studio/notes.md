# The big study, read against the film

What the footage shows of the big study, and how the map draws it. Film times are true times of
the 2022 documentary (video `zZEy10fpq3I`; frame names carry the raw second, true = raw + 0.96 s,
and links add 1 s). The compass is map-local: the door wall is N, P is the S wall, Q, R and S the
E wall.

## Free-standing bookcases in the middle of the floor

At 1:14:27 to 1:14:31 (frames t_011426, t_011428, t_011430) the camera looks along an aisle
between a wall-high bookcase on the left and a 2.1 m unit on the right whose shelves face the
aisle. The unit ends at a cross aisle where a low white unit stands across its end, with the
calligraphy and a photograph on top. A girl skates along the cross aisle past the ends of
further units of the same height. These are the *pettine* (comb) units the Fondazione's
lettering calls N and O: teeth standing across the room, ends towards the aisle in front of P,
cross aisles between them. Photographs criticaletteraria_2022_5, _11 and _13 show the same teeth
end-on.

The map draws the five N and O faces across the room at right angles to P, running from z 6.3 to
8.7 with 1.3 m of aisle before P, in a row from x 6.5 to 10.8 with cross aisles of 1.6 m: Nb
alone facing E, Oa and Ob back to back, Na and Nc back to back. Each free unit carries a
`position` key in `../layout.json`, which `gen_books_eco.py` reads.

Which tooth is which, which faces are back to back and the exact spacing are guesses, and each
unit's panel says so. The Fondazione lists three N faces and two O faces without a plan, and the
film never shows the whole row. The M island (books by and about Eco, face B towards the door)
stands parallel to the door wall: film 1:29 and 1:15:11 show it so, as does the 2015 walk-through
at 5:33 to 5:37.

## The desk and the chair

The black desk with the computer stands in the aisle before the tall shelving, anchored 1.4 m in
front of Q by the 2015 interview, at z 2.5 to 4.1. The black leather lounge chair (film 44:09) is
anchored in front of L8-12 at z 1.3 to 2.2, x 11.5 to 12.4. Nothing in the footage fixes the
desk's place along Q, since the 2015 interview shows it against tall shelving from one side only;
it sits where it clears the chair. A check asserts that no two floor-standing pieces in the study
overlap by footprint. The floor boxes at the base of P stand 1 m along P from the sofa, which
their evidence does not fix either.

## The low white unit at the comb end

At 5:23 to 5:31 (t_000522 to t_000530) the top of the low white unit at a comb end carries, left
to right, two stacks of books, the framed calligraphy ("I know that you believe you
understand..."), a framed black-and-white photograph, then a row of about twenty-five white
Bompiani paperbacks of the uniform ECO series, and at their right end the small carved wooden
plaque UMBERTO ECO. The spines of *Dall'albero al labirinto* and *Baudolino* can be read at 5:27.

The map draws the unit as two open shelves, 1.4 x 0.35 m and 1.05 m high, across the near end of
tooth Nb, with the stacks, the calligraphy and photograph, the row of paperbacks (white spines
with ECO lettering blocks, linked to 5:27) and the plaque at the row's right end. The paperbacks
count as unknown books, so they vanish under "Certain only" like the other anonymous piles. The
two readable titles are named in the panel but not added to the catalogue, because the dense
spine pass marked that close-up "other library / insert" and the map keeps to the pass's verdicts
for shelving books. The white framed print on top of Na is a separate piece.

## The walls and the windows

Two readings of the room fit the footage and cannot be told apart from stills:

- **Reading A, the map's:** P on the wall opposite the door (S), Q, R and S on the E wall, the
  desk row and windows on the S wall west of P, the W wall bare.
- **Reading B:** Q and the L run share one long wall (4.8 + 9.2 = 14.0 m, the room's length), the
  windows and the balcony door are on the wall at right angles to it with the sofa at the balcony
  end, and P faces them.

Nothing in the film settles this, since no shot pans from a window to a lettered bay. The map
follows reading A. What both readings agree on is drawn:

- A window with a radiator and a stone sill to the right of the door on entering (film 1:15:13,
  t_011512; the 1:15:09 note reads "radiator under the window at right"). It sits 0.9 m from the
  door corner, with the radiator under it.
- The desk row's own windows (film 1:43, t_000142; 2015 interview 5:47): a window with a slatted
  blind and a radiator over the desk, and a floor-length French window with dark louvred shutters
  beside it, the sofa next to the French window at 13:19 (t_001318). They stand on the map's S
  wall west of P, with the radiator and the French window's full height stated. Their wall is the
  map's, not a verified one.

The rest of the W wall stays bare, the far end of the room beyond P is unmodelled, and the sofa
stands at S rather than beside the French window as reading B would have it, because moving it
would move P.

## Files

`studio_objects.json` lists the pieces this survey placed: position, size, confidence, the frame
and the film second behind each one, and the bookcase positions the plan uses.
