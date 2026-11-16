"""captions.srt (final-reel timeline) + work/captions_source.srt (raw-source timeline)
from the verified transcript. Cues break at punctuation, pauses ≥ 0.25 s, or 6 words.
Usage: python3 -I tools/make_srt.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
tm = json.load(open(ROOT / "timing-map.json"))
src_words = json.load(open(ROOT / "transcript.json"))
out_words = tm["words_output"]

def ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def cues(ws, k0="start", k1="end"):
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        nxt = ws[i + 1] if i + 1 < len(ws) else None
        brk = (w["text"][-1] in "،.؟:…" or nxt is None or nxt[k0] - w[k1] >= 0.25 or len(cur) >= 6)
        if brk:
            out.append((cur[0][k0], cur[-1][k1], " ".join(x["text"] for x in cur)))
            cur = []
    return out

def write(path, cs):
    with open(path, "w", encoding="utf-8") as f:
        for i, (a, b, t) in enumerate(cs, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n‫{t}‬\n\n")

write(ROOT / "captions.srt", cues(out_words))
write(ROOT / "work/captions_source.srt", cues(src_words))
print(open(ROOT / "captions.srt", encoding="utf-8").read()[:1200])
