# eco-video: book spines read from public footage of Umberto Eco's library

This folder holds the readings of the books on the shelves of Eco's Milan flat, taken from
public YouTube uploads and from published photographs, together with the plan of the flat
those readings are placed in. One video, `zZEy10fpq3I`, is an unofficial upload of the full
2022 documentary *Umberto Eco: La biblioteca del mondo* (80 minutes, largely shot inside the
flat); the other eleven are official or news-channel uploads.

Video files and the frames cut from them are not kept in the repository. Every reading names
its video, its frame and its second, so any spine can be checked against the film on YouTube.

## Files

| File | What it is |
|---|---|
| `videos.json` | One record per video: id, title, uploader, upload date, duration, the resolution the frames were cut from, frame counts, `timestamp_offset_s` and notes. |
| `spines_<video_id>[_<tag>].jsonl` | The readings of one video's frames, one JSON object per frame: room, wall, view, rows of books left to right with `spine_text`, language and confidence, and runs of illegible spines as counts. `MERGE.md` documents every field. |
| `spines_photos.jsonl` | The same shape for photographs, with the picture's public URL and credit in place of a video id. |
| `spines_*_dense.jsonl` | The second, denser reading of eight of the videos; see `dense/README.md`. |
| `spines_*_summary.md` | Per reading file: how many frames were read, how many yielded a title, which walls were identified, what is legible and what is not. |
| `skipped*.csv` | `filename,reason` for every frame that was opened and gave nothing. |
| `books_by_wall_eco.json`, `.md` | The consolidation of all the `spines_*.jsonl` files: one record per distinct book with all its sightings, one per wall. The `.md` is the readable version. |
| `build_books_by_wall_eco.py` | Writes those two files and `../eco-map/books_seen.json` from every `spines_*.jsonl` in this folder. `--dry-run` lists what a new file would change. |
| `layout.json`, `layout.md` | The reconstructed plan of the flat: six rooms, their bookcases, bays and shelves. `layout.md` says what each part of the plan rests on and what is a guess. |
| `objects_from_video.json` | The film's shots grouped by room, with the furniture, pictures and piles visible in each and the camera move. |
| `piano_piles.json`, `.jsonl` | The twelve piles of books on the salotto piano, six on the lid and six on the keyboard shelf, listed top to bottom. |
| `quotes_<video_id>.json` | Lines transcribed from a video, each with its second, its link and a note on what it is about. |
| `process_video.py` | Cuts frames from a video file and indexes them. |
| `build_videos_json.py` | Assembles `videos.json`. |
| `MERGE.md` | How to add a new batch of readings so they land in the map without disturbing what is there. |
| `dense/` | The dense reading pass: its books, its frame files and what the footage does and does not show. |
| `studio/`, `salotto/` | The two rooms surveyed in detail against the film, with their objects and geometry. |

## Frames and timestamps

`process_video.py VIDEO_ID VIDEO_FILE` cuts two kinds of frame with ffmpeg: interval frames,
one every two seconds, and scene-change frames wherever the picture changes by more than 0.3.
It then hashes every frame with `imagehash.phash` in timestamp order and drops a frame whose
Hamming distance to the last kept frame is 6 or less. Frames with a mean grey level under 25
are kept and flagged `dark`. The run writes `t_HHMMSS.jpg` and `s_HHMMSS_ff.jpg` files, an
`INDEX.csv` of every frame and a `KEEP.csv` of the frames worth reading.

Timestamps are relative to the start of the video as served, with no trimming. The interval
filter labels output slot k as 2k seconds but emits the last source frame that rounds into
that slot, so the picture in slot k is the source frame at 2k + 1 - 1/fps, about a second
later than the label. Frame names and `timestamp_seconds` therefore carry the source time,
which puts interval frames at 1, 3, 5 ... seconds rather than 0, 2, 4.

The frames of `zZEy10fpq3I` keep the raw slot labels instead, because other files read them by
name: their true source time is the label plus 0.96 s. `videos.json` records this per video as
`timestamp_offset_s`, 0.96 for `zZEy10fpq3I` and 0 for the other eleven. A reader wanting the
real second computes `timestamp_seconds + timestamp_offset_s`, and a `&t=NNs` link for a
`zZEy10fpq3I` frame adds one second. Scene-change frames carry exact `pts_time` values and need
no correction.

## What the footage is worth

* Resolutions differ by source. The 2022 and 2026 uploads are 1080p, the three 2015 *Sulla
  memoria* parts are 480p, and the two short news clips (askanews, Corriere) are 360p. No spine
  in the 2015 walk-through is legible.
* `M8IWTOFNlOc` is a static talking-head interview with the shelves out of focus behind the
  speaker. Its kept frames are mostly near-identical and of little use for spine reading.
* The dedupe keeps every frame that differs by more than Hamming 6 from the one before it, so a
  slow pan keeps almost all of its frames. Talking heads are not detected; that judgement is
  left to whoever reads the frames.
* The photographs carry structure rather than titles. The Fondazione's bookcase survey is
  served at 650 px and shows the layout of every case; no spine on it can be read.
