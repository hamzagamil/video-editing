"""captions.srt for the whole dialogue on the final reel timeline (sentence-sized cues, <= 42 chars).
Usage: python3 -I tools/make_srt.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
words = json.load(open(ROOT / "transcript.json", encoding="utf-8"))
caption_text = {"80": "80", "%": "%"}


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms % 3600000 // 60000:02d}:{ms % 60000 // 1000:02d},{ms % 1000:03d}"


cues, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    text = " ".join(x["text"] for x in cur).replace("80 %", "80%")
    nxt = words[i + 1] if i + 1 < len(words) else None
    end_sentence = w["text"].endswith((".", "؟", "?", "،"))
    gap = nxt is not None and nxt["start"] - w["end"] > 0.45
    if nxt is None or end_sentence or gap or len(text) > 36 or nxt["take"] != w["take"] and len(text) > 18:
        cues.append((cur[0]["start"], max(cur[-1]["end"], cur[0]["start"] + 0.6), text))
        cur = []
out = []
for n, (a, b, t) in enumerate(cues, 1):
    nb = cues[n][0] if n < len(cues) else b
    out.append(f"{n}\n{ts(a)} --> {ts(min(b + 0.2, nb))}\n{t}\n")
(ROOT / "captions.srt").write_text("\n".join(out), encoding="utf-8")
print(len(cues), "cues")
