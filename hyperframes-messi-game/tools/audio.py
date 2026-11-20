"""Cut the dialogue to the retained ranges and process it.

  ../source/work/audio48k.wav  (original camera/lav audio, untouched)
  -> assets/media/dialogue.wav (same ranges as the picture, 4 ms edge fades,
     high-pass 70 Hz, gentle compression, two-pass loudnorm to -14.5 LUFS / -1.5 dBTP)
Usage: python3 -I tools/audio.py
"""
import json, subprocess, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT.parent / "source" / "work"
tm = json.load(open(ROOT / "timing-map.json", encoding="utf-8"))
tmp = WORK / "dlg"
tmp.mkdir(exist_ok=True)

parts = []
for s in tm["segments"]:
    p = tmp / f"{s['id']}.wav"
    d = s["duration"]
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(s["src_start"]), "-t", str(d),
                    "-i", str(WORK / "audio48k.wav"),
                    "-af", f"afade=t=in:d=0.004,afade=t=out:st={max(0, d - 0.004):.4f}:d=0.004",
                    "-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", str(p)], check=True)
    parts.append(p)
lst = tmp / "list.txt"
lst.write_text("".join(f"file '{p}'\n" for p in parts))
raw = tmp / "dialogue_raw.wav"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                "-c:a", "pcm_s24le", str(raw)], check=True)

chain = "highpass=f=70,acompressor=threshold=-21dB:ratio=2.4:attack=12:release=140:makeup=2"
r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(raw), "-af",
                    chain + ",loudnorm=I=-14.5:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True)
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))
ln = (f"loudnorm=I=-14.5:TP=-1.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
out = ROOT / "assets/media/dialogue.wav"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(raw), "-af", chain + "," + ln,
                "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(out)], check=True)
r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(out), "-af", "ebur128=peak=true", "-f", "null", "-"],
                   capture_output=True, text=True)
summ = r.stderr[r.stderr.rfind("Summary"):]
print("dialogue:", " ".join(re.findall(r"I:\s+-?[\d.]+ LUFS|Peak:\s+-?[\d.]+ dBFS", summ)))
print("duration", subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                                 capture_output=True, text=True).stdout.strip(), "expected", tm["output_duration_speech"])
