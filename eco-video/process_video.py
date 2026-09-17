#!/usr/bin/env python3
"""Cut interval + scene-change frames from one video, index them, dedupe by phash.

Usage: process_video.py VIDEO_ID VIDEO_FILE
Writes /mnt/project-files/eco-video/frames/VIDEO_ID/{t_HHMMSS.jpg, s_HHMMSS_ff.jpg, INDEX.csv, KEEP.csv}
"""
import csv, os, re, shutil, subprocess, sys, json
import tempfile
from PIL import Image, ImageStat
import imagehash

FFMPEG = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")   # where the frames go: eco-video/frames/<video id>/
LOCAL = os.path.join(tempfile.gettempdir(), "eco-dl", "work")   # a fast local work folder; the frames are moved to ROOT when the run ends
SCENE_THRESH = 0.3
HAMMING = 6
DARK_MEAN = 25  # 0-255 grayscale mean below which a frame is flagged "dark"

def hhmmss(t):
    t = int(t)
    return f"{t//3600:02d}{(t%3600)//60:02d}{t%60:02d}"

def run(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def main(vid, path):
    out = os.path.join(LOCAL, vid)
    tmp = os.path.join(out, "_tmp")
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(tmp)

    # probe duration / resolution
    p = run([FFMPEG, "-i", path])
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", p.stderr)
    duration = int(m[1])*3600 + int(m[2])*60 + float(m[3]) if m else None
    m = re.search(r"Video: .*?, (\d{2,5})x(\d{2,5})", p.stderr)
    res = f"{m[1]}x{m[2]}" if m else None
    m = re.search(r"([\d.]+) fps", p.stderr)
    fps = float(m[1]) if m else 25.0
    print(f"[{vid}] duration={duration} res={res}")

    rows = []
    # 1) interval frames: one every 2 s. fps=0.5 output slot k (0-based) is labelled 2k s by ffmpeg, but the
    #    filter emits the LAST source frame that rounds into the slot, i.e. source pts = 2k + 1 - 1/fps
    #    (verified with showinfo checksums: slot 45 <- pts 90.96 at 25 fps). We record the source pts.
    r = run([FFMPEG, "-hide_banner", "-loglevel", "error", "-i", path, "-vf", "fps=0.5",
             "-q:v", "2", os.path.join(tmp, "int_%05d.jpg")])
    if r.returncode: print(r.stderr); sys.exit(1)
    ints = sorted(f for f in os.listdir(tmp) if f.startswith("int_"))
    for f in ints:
        k = int(f[4:9]) - 1
        t = round(2 * k + 1 - 1 / fps, 3)
        name = f"t_{hhmmss(round(t))}.jpg"
        os.rename(os.path.join(tmp, f), os.path.join(out, name))
        rows.append((name, t, "interval"))
    print(f"[{vid}] interval frames: {len(ints)}")

    # 2) scene-change frames with showinfo to recover pts
    r = run([FFMPEG, "-hide_banner", "-i", path, "-vf", f"select='gt(scene,{SCENE_THRESH})',showinfo",
             "-vsync", "vfr", "-q:v", "2", os.path.join(tmp, "sc_%05d.jpg")])
    pts = [float(x) for x in re.findall(r"Parsed_showinfo.*?pts_time:\s*([\d.]+)", r.stderr)]
    scs = sorted(f for f in os.listdir(tmp) if f.startswith("sc_"))
    if len(pts) != len(scs):
        print(f"[{vid}] WARNING showinfo count {len(pts)} != scene frames {len(scs)}")
    seen = set()
    for f, t in zip(scs, pts):
        ff = int(round((t - int(t)) * 100)) % 100
        name = f"s_{hhmmss(t)}_{ff:02d}.jpg"
        if name in seen:  # two cuts within the same centisecond (unlikely)
            name = f"s_{hhmmss(t)}_{ff:02d}b.jpg"
        seen.add(name)
        os.rename(os.path.join(tmp, f), os.path.join(out, name))
        rows.append((name, round(t, 3), "scene"))
    print(f"[{vid}] scene frames: {len(scs)}")
    shutil.rmtree(tmp)

    rows.sort(key=lambda r: (r[1], r[2] != "interval"))
    with open(os.path.join(out, "INDEX.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["filename", "timestamp_seconds", "source"]); w.writerows(rows)

    # 3) dedupe by perceptual hash vs previous kept frame; flag very dark frames
    keep, prev = [], None
    for name, t, src in rows:
        im = Image.open(os.path.join(out, name))
        h = imagehash.phash(im)
        mean = ImageStat.Stat(im.convert("L")).mean[0]
        if prev is not None and (h - prev) <= HAMMING:
            continue
        prev = h
        keep.append((name, t, str(h), "dark" if mean < DARK_MEAN else ""))
    with open(os.path.join(out, "KEEP.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["filename", "timestamp_seconds", "phash", "flag"]); w.writerows(keep)
    print(f"[{vid}] frames_total={len(rows)} frames_kept={len(keep)} dark={sum(1 for k in keep if k[3])}")
    json.dump({"video_id": vid, "duration_s": duration, "resolution_obtained": res,
               "frames_total": len(rows), "frames_kept": len(keep)},
              open(os.path.join(out, "_stats.json"), "w"))

    # 4) copy the finished folder to the project mount (rclone mount dislikes rapid writes: retry per file)
    import time
    dest = os.path.join(ROOT, vid)
    os.makedirs(dest, exist_ok=True)
    names = sorted(os.listdir(out))
    for name in names:
        src = os.path.join(out, name)
        for attempt in range(8):
            try:
                shutil.copyfile(src, os.path.join(dest, name))
                if os.path.getsize(os.path.join(dest, name)) == os.path.getsize(src): break
            except OSError as e:
                print(f"[{vid}] copy retry {attempt} {name}: {e}")
            time.sleep(1 + attempt)
        else:
            print(f"[{vid}] COPY_FAILED {name}"); sys.exit(2)
    missing = [n for n in names if not os.path.exists(os.path.join(dest, n))]
    print(f"[{vid}] copied {len(names)} files to {dest}; missing={len(missing)}")
    shutil.rmtree(out)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
