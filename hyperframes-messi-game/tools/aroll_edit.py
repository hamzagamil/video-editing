"""Bake the presenter edit into one continuous video (assets/media/aroll_edit.mp4).

Why: with 120 <video> clips seeking into one proxy, the renderer intermittently drops the first
frame of a clip (a one-frame flash of the page background). One continuous clip has no seams.
Inputs: timing-map.json (segments, freezes), assets/media/aroll.mp4 (graded proxy).
Usage: python3 -I tools/aroll_edit.py
"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FPS = 30
tm = json.load(open(ROOT / "timing-map.json", encoding="utf-8"))
proxy = ROOT / "assets/media/aroll.mp4"
work = ROOT / "assets/media/aroll_edit_parts"
work.mkdir(parents=True, exist_ok=True)
X264 = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an"]


def part(i_s):
    i, s = i_s
    first = round(s["proxy_start"] * FPS)
    n = round(s["duration"] * FPS)
    out = work / f"{i:03d}.mp4"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{first / FPS - 0.01:.4f}", "-i", str(proxy),
                    "-frames:v", str(n), *X264, str(out)], check=True)
    got = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                              "stream=nb_read_packets", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout)
    if got != n:
        sys.exit(f"{s['id']}: {got} frames, expected {n}")
    return out


with ThreadPoolExecutor(4) as ex:
    parts = list(ex.map(part, enumerate(tm["segments"])))
(work / "list.txt").write_text("".join(f"file '{p.name}'\n" for p in parts))
joined = work / "joined.mp4"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "list.txt"),
                "-c", "copy", str(joined)], check=True)

# freeze patches: hold a clean frame over the lean frames (video only)
ins, chain, last = ["-i", str(joined)], [], "0:v"
for k, fz in enumerate(tm.get("freezes", []), 1):
    ins += ["-i", str(ROOT / f'assets/media/stills/{fz["id"]}.jpg')]
    a, b = fz["out_start"], fz["out_start"] + fz["duration"]
    chain.append(f"[{k}:v]scale=1080:1920,format=yuv420p[s{k}];[{last}][s{k}]overlay=0:0:enable='between(t,{a - 0.001:.4f},{b - 0.017:.4f})'[v{k}]")
    last = f"v{k}"
out = ROOT / "assets/media/aroll_edit.mp4"
cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", *ins]
if chain:
    cmd += ["-filter_complex", ";".join(chain), "-map", f"[{last}]"]
cmd += [*X264, "-movflags", "+faststart", str(out)]
subprocess.run(cmd, check=True)
n = int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout)
want = round(tm["output_duration_speech"] * FPS)
print(f"aroll_edit.mp4: {n} frames (timeline {want})")
if n != want:
    sys.exit("frame count mismatch")
