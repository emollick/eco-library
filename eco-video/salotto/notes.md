# The salotto, read against the film

What the footage and the published photographs show of the living room, and the geometry the
files here record. The evidence is the salotto ranges of `../objects_from_video.json` (517
frames in 28 ranges) and the room photographs: the key views are the 74:04 to 74:13 wide shot
from the sofa side, the 50:51 wide shot from the vestibolo-door corner, the 03:50 to 04:12
two-shot towards the window wall, the 62:33 and 64:00 club-armchair set-ups, the 65:52 archive
interview at the dining table, the 42:51 to 43:04 piano pull-back, the Curti Parini 2022
photographs of the cases, the cabinet wall and the piano, and Zanni's 2010 photograph.

## Files

- `salotto_layout.json`: the room block in the shape of `../layout.json`, with size, walls,
  openings and bookcases.
- `salotto_objects.json`: 39 objects in the shape of the map's `objects_map_eco.json` rules, each
  with position [x, z] in room-local metres, rotation, size [w, d, h], confidence, the evidence
  behind it (frame file, film second, link at that second) and `build_now`, where the build puts
  the same piece.
- `salotto_inventory.json`: the same room as a wall-by-wall inventory, with the coordinate frame
  and the size estimate it rests on.
- `salotto_plan.png`: a top-down plan of the room.
- `crops/photo_zanni_2010.jpg`: Zanni's 2010 photograph, which shows the display cases with open
  antique books.

## Coordinate frame

x runs from the W wall (0) to the E wall (7.5), z from the S wall (0) to the N wall (7.6), the
same convention as the build. N is the side where the vestibolo door is, since the build puts the
vestibolo north of the salotto, so the windows on Piazza Castello come out on the S wall. The
absolute compass orientation of the flat is not verified. About 7.5 m east to west by 7.6 m north
to south is the smallest room that fits both wall sequences; the sitting area takes the N half,
the dining pocket and the window furniture the S half.

## What the footage shows

High confidence unless marked otherwise.

**E wall, from the N corner southward.** The vestibolo door, in the N wall at its E end, with a
glazed transom and a mirror on the leaf (Eco walks out through it at 00:50 past the 'fine'
canvas); a column of three small prints with the small dark side cabinet and the telephone below;
the white 'fine' canvas; the plaster statue standing against the wall on a plinth; a short pier;
a bright opening, window or glazed door (medium); then the dark wooden credenza, its glazed top
holding shells and oval family photographs, with CD racks, hi-fi and curios, and south of it the
dining pocket.

**The glass cases.** Three steel-and-glass cases, about 0.8 x 0.45 x 1.9 m each, stand in a row
1.3 m in front of the E wall rather than against it, running south from directly south of the
statue: case 1 with open illuminated facsimiles, two shadow-box dioramas on top and the miniature
library filmed at 73:41; case 2 with antique books and a brass stand on top; case 3 with shells,
urchins, pomegranates, lotus pods and a porcupine fish. From the sofa side the statue is
immediately left of case 1 (Curti Parini photograph and 74:13). The credenza shows behind cases 2
and 3, and dining chairs show through case 2.

**The dining pocket.** A dark wooden table with six Thonet-style chairs in white seat covers,
south of case 3 and in front of the credenza (Curti Parini photograph, the 65:52 archive
interview, the far left of 03:50).

**The seating.** Around the low coffee table of book piles, with the brass orrery and a
candlestick on it: sofa A on the N side under a dark-framed painting, with the arc floor lamp and
its large parchment shade standing beside the vestibolo door and reaching over the sofa's E end;
the tan leather club armchair in front of cases 1 and 2 facing W, which is Eco's interview seat;
a white armchair in front of the statue; a white armchair to the SE of the table (Carlotta's seat
at 03:50, medium); a white sofa against the window wall under the ropes painting (Renate's seat
at 03:50, medium).

**S wall, the window wall, from the E corner westward.** Three small framed paintings over a low
wooden chest; a chrome floor lamp; a folding X-stool, a lectern with a magazine and a small table
with books in front of window 1, a French window with a radiator and the view of the Castello
tower at 05:07; the ropes painting, an assemblage of straps and wood; window 2 (medium: seen only
at the far left of 50:51); two framed drawings and a small hanging object at the SW corner.

**W wall, from the S corner northward.** Blank wall, with no piano there (50:51 shows it empty);
door 2, its leaf open into the room, with a chrome floor lamp beside it; the burnt-book
assemblage; the glazed dark pine cabinet of curiosities and bottles, 2.4 m, which the build calls
salotto-wood; a small gilt-framed painting; the flat-screen TV on a stand (medium).

**N wall, from the E corner westward.** The dark-framed painting over sofa A; a gilt oil painting;
then, at low to medium confidence, the upright piano with its twelve piles and the child-Jesus
figure on top, two large framed drawings above it, the blue tile panel and the 'eco' print west of
it and a picture east of it, near the NW corner by the TV. The piano's wall is the one thing no
shot fixes: the pull-back shows only the piano, 50:51 rules out the W wall, and the photograph
pairing and the corner objects favour the western part of the N wall.

## Unresolved

Whether the bright opening behind case 1 is a window or a door; which room door 2 leads to; the
exact place of the piano along the N wall; and whether the white-framed print seen at 50:51 hangs
on the N wall east of the dark painting or on the door pier. Both places for the print are
listed, and one should be kept.

Frame numbers are 1 fps frames of `zZEy10fpq3I`, and the film seconds quoted here already include
the 0.96 s offset.
