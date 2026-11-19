"""Edit decision: selected source takes -> retained ranges -> output timeline.

Inputs (../source/work)
  whisper_large.json (+ whisper_fix*.json overrides)  word-level transcript, source seconds
  silence.txt          silencedetect map of the source audio (-38 dB, >= 0.25 s)
  ranges.json          candidate ranges rendered (graded) to clips/Rnn.mp4 -> concatenated aroll.mp4
  tools/plan.py        TAKES: source spans in story order, text corrections, deliberate holds

Rule: inside each take span, every silence longer than PAUSE_SPLIT is removed, keeping ~3 frames
after speech and ~2 before the next word; a `hold` keeps a deliberate pause instead.

Outputs: transcript.json, timing-map.json (output timeline), printed edit summary.
Usage: python3 -I tools/cut.py
"""
import json, sys, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT.parent / "source" / "work"
sys.path.insert(0, str(ROOT / "tools"))
import plan  # noqa: E402

FPS = 30
FR = 1 / FPS


def snap(t):
    return round(round(t * FPS) / FPS, 4)


def load_words(name):
    out = []
    for seg in json.load(open(WORK / name, encoding="utf-8")):
        for w in seg["words"]:
            t = w["w"].strip()
            if t:
                out.append({"text": t, "s": w["s"], "e": w["e"], "p": w["p"]})
    return out


words = load_words("whisper_large.json")
for name, rngs in plan.WORD_FIXES:
    inside = lambda w: any(a <= w["s"] < b for a, b in rngs)  # noqa: E731
    words = [w for w in words if not inside(w)] + [w for w in load_words(name) if inside(w)]
words.sort(key=lambda w: w["s"])
PUNCT = ".,،?؟!…"
for w in words:
    core = w["text"].strip(PUNCT)
    tail = w["text"][len(w["text"].rstrip(PUNCT)):]
    if core in plan.SPELL:
        w["text"] = plan.SPELL[core] + tail

sil = [tuple(map(float, l.split()[:2])) for l in open(WORK / "silence.txt")]
ranges = json.load(open(WORK / "ranges.json"))


def clip_frames(i):
    p = WORK / "clips" / f"R{i:02d}.mp4"
    if not p.exists():
        a_, b_ = ranges[i - 1]
        print(f"  (clip R{i:02d} not rendered yet: estimating its frame count)")
        return round((b_ - a_) * FPS) + 1
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                        "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return int(r.stdout.strip())


offs, acc = [], 0
for i in range(1, len(ranges) + 1):
    offs.append(acc / FPS)
    acc += clip_frames(i)


def to_proxy(t):
    for (a, b), o in zip(ranges, offs):
        if a - 1e-6 <= t <= b + 1e-6:
            return o + (t - a)
    raise ValueError(f"source time {t} outside every rendered range")


def voiced(a, b, holds):
    """keep-intervals inside [a, b]: speech, padded, with long pauses removed (unless held)"""
    cuts = []
    for s, e in sil:
        s2, e2 = max(s, a), min(e, b)
        if e2 - s2 < plan.PAUSE_SPLIT:
            continue
        keep_after = 3 * FR
        for ht, hs in holds:
            if abs(ht - s2) < 0.35:
                keep_after = max(keep_after, hs)
        cs, ce = s2 + keep_after, e2 - 2 * FR
        if s2 <= a + 0.01:
            cs = a
        if e2 >= b - 0.01:
            ce = b
        if ce - cs > FR:
            cuts.append((cs, ce))
    keep, t = [], a
    for cs, ce in sorted(cuts):
        if cs > t:
            keep.append((t, cs))
        t = max(t, ce)
    if t < b:
        keep.append((t, b))
    return [(snap(x), snap(y)) for x, y in keep if snap(y) - snap(x) >= FR]


segments, out_words, removed = [], [], []
out_t, prev_end, wid = 0.0, None, 0
for take in plan.TAKES:
    a, b = take["src"]
    ra, rb = next((x, y) for x, y in ranges if x - 0.3 <= (a + b) / 2 <= y + 0.3)
    a, b = max(a, ra), min(b, rb)
    keep = voiced(a, b, take.get("hold", []))
    tw = [w for w in words if a - 0.02 <= (w["s"] + w["e"]) / 2 <= b]
    fixes = take.get("text")
    if fixes is not None:
        if len(fixes) != len(tw):
            sys.exit(f"take {take['id']}: {len(tw)} words, {len(fixes)} corrections\n  " +
                     " ".join(f"{w['text']}" for w in tw))
        tw = [dict(w, text=t) for w, t in zip(tw, fixes)]
    for s, e in keep:
        dur = snap(e - s)
        seg = {"id": f"a{len(segments) + 1:02d}", "take": take["id"], "src_start": s, "src_end": e,
               "out_start": snap(out_t), "duration": dur, "proxy_start": round(to_proxy(s), 4)}
        if prev_end is not None and s - prev_end > 0.02:
            removed.append({"src_start": prev_end, "src_end": s,
                            "reason": "pause trimmed" if s - prev_end < 2.5 else "retake / set-up / dead air"})
        prev_end = e
        segments.append(seg)
        out_t += dur

    def src2out(t):
        best = None
        for sg in segments:
            if sg["take"] != take["id"]:
                continue
            if sg["src_start"] - 1e-6 <= t <= sg["src_end"] + 1e-6:
                return sg["out_start"] + (t - sg["src_start"])
            if t < sg["src_start"] and best is None:
                best = sg["out_start"]  # word starts inside a removed pause -> next kept frame
        return best if best is not None else out_t

    for w in tw:
        wid += 1
        st, en = src2out(w["s"]), src2out(w["e"])
        if en - st > 1.2:  # whisper stretched the word over a removed pause
            en = st + min(0.8, max(0.25, 0.09 * len(w["text"])))
        out_words.append({"id": f"w{wid}", "text": w["text"], "start": round(st, 3), "end": round(max(en, st + 0.12), 3),
                          "take": take["id"], "src": [round(w["s"], 3), round(w["e"], 3)], "p": round(w["p"], 3)})

total = snap(out_t)
json.dump(out_words, open(ROOT / "transcript.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"fps": FPS, "source": "../source/rawreel.mov -> graded SDR proxy assets/media/aroll.mp4 (concatenated candidate ranges)",
           "candidate_ranges": ranges, "proxy_offsets": [round(o, 4) for o in offs],
           "output_duration_speech": total, "segments": segments, "removed": removed,
           "words_output": [{k: w[k] for k in ("id", "text", "start", "end")} for w in out_words]},
          open(ROOT / "timing-map.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(segments)} retained ranges, {len(out_words)} words, speech timeline {total:.3f}s")
for t in plan.TAKES:
    ws = [w for w in out_words if w["take"] == t["id"]]
    if ws:
        print(f"  {t['id']:<5} {ws[0]['start']:7.2f}-{ws[-1]['end']:7.2f}  " +
              " ".join(f"{w['text']}[{w['id'][1:]}]" for w in ws))
