# spines_rMSOvDAyH5c summary

**Video:** "Umberto Eco: Advice to the Young" — Louisiana Channel, 93 s clip, 1080p.
**Frames in KEEP.csv:** 22. **Frames read (Read tool, full size):** 22. **Frames with book/library content logged in spines_rMSOvDAyH5c.jsonl:** 16. **Frames skipped (title/credit/black cards):** 6 (see skipped_rMSOvDAyH5c.csv).

## What's in the shot
The whole clip is one static, shallow-depth-of-field talking-head setup: Eco in an orange leather
armchair, with a glass-fronted display cabinet behind him holding two open illuminated-manuscript
facsimile pages, and further bookshelves beyond that, entirely out of focus. This framing does not
change for the length of the clip (no camera moves, no cutaways), so all 16 content frames are
logged as `same_as_frame: "s_000023_96.jpg"`, the sharpest/most representative frame, which carries
the full description.

**Room:** `rare` — a glass display case for open, illuminated volumes reads as a rare-book/manuscript
display rather than an everyday working shelf (`study`), so it was matched to the rare-books room
over the alternatives.

## Legibility
No spine or manuscript text is legible at any timestamp. 2-6 overlapping tiles were cropped from the
cabinet region and the background shelf corner of the sharpest frames (`s_000023_96.jpg`,
`t_000053.jpg`, `t_000117.jpg`), upscaled 3x with LANCZOS + unsharp mask, and inspected — the blur is
optical (shallow depth of field / bokeh), not resolution-limited, so no amount of sharpening recovers
text. The two manuscript pages on the visible cabinet shelf are logged as
`{"unlabelled": true, "count": 2}`; the background shelving is described only in notes, not counted,
since no reliable item count could be read off it.

## Confidence breakdown
- High: 0 titles
- Medium: 0 titles
- Low: 0 titles
- Unlabelled items logged: 2 per frame x 16 frames (the two open manuscript pages, repeated per frame since framing never changes)

## Example frames (5)
| timestamp | frame | note |
|---|---|---|
| 00:00:05 | t_000005.jpg | same_as_frame -> s_000023_96.jpg |
| 00:00:16 | s_000015_96.jpg | same_as_frame -> s_000023_96.jpg |
| 00:00:24 | s_000023_96.jpg | **canonical/clearest frame** — full description |
| 00:00:53 | t_000053.jpg | same_as_frame -> s_000023_96.jpg |
| 00:01:17 | t_000117.jpg | same_as_frame -> s_000023_96.jpg, last content frame before credits |

**Clearest frame:** `/mnt/project-files/eco-video/frames/rMSOvDAyH5c/s_000023_96.jpg`

## Quotes about his library or specific books
None. The captions (0:04-1:25) cover Eco's general writing advice to young authors (not becoming
"an artist," genius as "10% inspiration and 90% perspiration," not publishing too early, not
"pretending to receive the Nobel Prize"), but at no point does he name a specific book or describe
his library/collection, so `quotes_rMSOvDAyH5c.json` is an empty array.
