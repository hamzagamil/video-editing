"""Silence-trim planner → timing-map.json.

Keeps every speech chunk between the first kept word ("حسام", w2) and the end of
"ماهر" (w160). Internal pauses longer than MIN_CUT are shortened to ~3 frames of room on
each side; shorter pauses are kept untouched. All cut points sit on the 30 fps frame grid.

Usage: python3 -I tools/plan_edit.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FPS = 30
words = json.load(open(ROOT / "transcript.json"))
SIL = json.load(open(ROOT / "work/silences.json"))

FIRST_WORD, LAST_WORD = 2, 160
MIN_CUT = 0.24          # pauses shorter than this stay as they are
PAD_OUT = 0.10          # room kept after speech before a cut (3 frames)
PAD_IN = 0.067          # room kept before speech after a cut (2 frames)
# pauses kept longer on purpose (source pause start → total seconds kept)
KEEP_LONGER = {
    104.930: 0.40,      # beat before the replacement's name "علي ماهر"
}

def fr(t):
    return round(round(t * FPS) / FPS, 4)

src_in = fr(words[FIRST_WORD]["start"] - 0.067)
src_out = fr(words[LAST_WORD]["end"] + 0.0)

ranges = []
cur = src_in
removed = [{"src_start": 0.0, "src_end": src_in, "why": "camera set-up, greeting 'مساء الخير' while settling"}]
for a, b in SIL:
    if a < src_in or a >= src_out:
        continue
    dur = b - a
    keep = KEEP_LONGER.get(round(a, 3))
    if keep:
        cut_a = fr(a + keep * 0.6)
        cut_b = fr(b - keep * 0.4)
    elif dur > MIN_CUT:
        cut_a = fr(a + PAD_OUT)
        cut_b = fr(b - PAD_IN)
    else:
        continue
    if cut_b - cut_a < 2 / FPS:
        continue
    ranges.append([cur, cut_a])
    removed.append({"src_start": cut_a, "src_end": cut_b, "why": f"pause {dur:.2f}s → kept {dur-(cut_b-cut_a):.2f}s"})
    cur = cut_b
ranges.append([cur, src_out])
removed.append({"src_start": src_out, "src_end": 111.8917, "why": "trailing 'و…', 'طيب', presenter stands up"})

segs = []
tf = 0  # running output position in frames
for i, (a, b) in enumerate(ranges):
    fa, fb = round(a * FPS), round(b * FPS)
    n = fb - fa
    o0, o1 = round(tf / FPS, 4), round((tf + n) / FPS, 4)
    segs.append({"id": f"a{i+1:02d}", "src_start": round(fa / FPS, 4), "src_end": round(fb / FPS, 4),
                 "out_start": o0, "out_end": o1,
                 "duration": round(o1 - o0, 4), "frames": n,
                 "src_frame_in": fa, "out_frame_in": tf})
    tf += n
total = round(tf / FPS, 4)

def to_out(ts):
    for s in segs:
        if s["src_start"] - 1e-6 <= ts <= s["src_end"] + 1e-6:
            return round(s["out_start"] + ts - s["src_start"], 3)
    # inside a removed gap → snap to the next segment start
    for s in segs:
        if ts < s["src_start"]:
            return s["out_start"]
    return total

out_words = []
for w in words[FIRST_WORD:LAST_WORD + 1]:
    out_words.append({"id": w["id"], "text": w["text"],
                      "src_start": w["start"], "src_end": w["end"],
                      "start": to_out(w["start"]), "end": to_out(w["end"])})

tm = {"fps": FPS, "source": "../rawreel.mov", "proxy": "assets/media/aroll.mp4",
      "output_duration_speech": total, "segments": segs, "removed": removed,
      "words_output": out_words}
json.dump(tm, open(ROOT / "timing-map.json", "w"), ensure_ascii=False, indent=1)
print("segments", len(segs), "speech output", total)
for s in segs:
    print(f'{s["id"]} src {s["src_start"]:8.3f}-{s["src_end"]:8.3f}  out {s["out_start"]:7.3f}-{s["out_end"]:7.3f}')
print()
line = []
for w in out_words:
    line.append(f'{w["id"]}:{w["text"]}@{w["start"]:.2f}')
print(" ".join(line))
