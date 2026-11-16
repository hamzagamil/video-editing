"""Build the verified word-level transcript.

Text: manually reviewed Egyptian-Arabic wording (whisper large-v3, two passes, corrected).
Timing: whisper.cpp DTW token times (large-v3, -nfa -dtw large.v3), snapped onto speech
activity from ffmpeg silencedetect (-35 dB, 0.2 s) so no word starts or ends inside silence.

Usage: python3 -I tools/align.py  (from the project folder)
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
dtw = json.load(open(ROOT / "work/dtw2_words.json"))

# (verified text, dtw indexes it covers). Corrections vs raw ASR are noted.
WORDS = [
    ("مساء", [0]), ("الخير،", [1]),
    ("حسام", [2]), ("حسن،", [3]),                # ASR: "حسام حسام"
    ("من", [4]), ("أسطورة", [5]), ("الكرة", [6]), ("المصرية،", [7]),
    ("لمدرب", [8]), ("يقود", [9]), ("المنتخب", [10]), ("في", [11]),
    ("كأس", [12]), ("العالم،", [13]),
    ("إلى", [14]), ("الخروج", [15]), ("من", [16]), ("الباب", [17]),
    ("الضيق", [18]),                            # ASR: "الطيق"
    ("يوم", [19]), ("7", [20]), ("نوفمبر.", [21]),
    ("حسام", [22]), ("حسن،", [23]),              # ASR: "حسام حسام"
    ("الاسم", [24]), ("اللي", [25]), ("كان", [26]), ("كله", [27]),
    ("يرمز", [28]), ("إلى", [29]), ("الروح", [30]), ("والعزيمة،", [31]),
    ("انتهت", [32]), ("رحلته", [33]), ("مع", [34]), ("المنتخب", [35]),
    ("المصري", [36]), ("بشكل", [37]), ("محدش", [38]),
    ("يصدّقه.", [39]),                          # ASR: "تصدق"
    ("السؤال", [40]), ("هنا:", [41]), ("إزاي", [42]), ("مدرب", [43]),
    ("قاد", [44]), ("مصر", [45]), ("في", [46]), ("المونديال،", [47]),
    ("وكان", [48]), ("عقده", [49]), ("مستمر", [50]),
    ("لـ2030،", [51, 52]),                      # spoken "العشرين تلاتين"
    ("يمشي", [53]), ("فجأة؟", [54]),
    ("هل", [55]), ("السبب", [56]),              # ASR pass 2: "السبع"
    ("هو", [57]), ("كان", [58]), ("فني،", [59]),
    ("ولا", [60]), ("مشاكل", [61]), ("خارج", [62]), ("الملعب", [63]),
    ("كانت", [64]), ("أكبر", [65]), ("من", [66]), ("إنه", [67]), ("هو", [68]),
    ("يقدر", [69]), ("يسيطر", [70]), ("عليها؟", [71]),
    ("الأزمات", [72]),                          # ASR: "الإزامات"
    ("داخل", [73]), ("المنتخب", [74]), ("بدأت", [75]),
    ("لما", [76]),                              # spoken twice (false start), kept verbatim
    ("الفترة", [77]), ("الأخيرة", [78]),
    ("لما", [79]), ("انتقادات", [80]), ("لمحمد", [81]), ("صلاح", [82]),
    ("وتبديله", [83]), ("في", [84]), ("مباراة", [85]), ("أنجولا،", [86]),
    ("وبعدها", [87]), ("محمد", [88]), ("صلاح", [89]), ("غادر", [90]),
    ("المنتخب.", [91]),
    ("وكمان", [92]), ("تصريحات", [93]), ("حسام", [94]), ("عن", [95]),
    ("محمد", [96]), ("الشناوي", [97]),
    ("خسّرته", [98]),                           # ASR: "وخسرته"
    ("شريحة", [99]), ("كبيرة", [100]), ("جدًا", [101]), ("من", [102]),
    ("الجماهير", [103]), ("المصرية.", [104]),
    ("وفوق", [105]), ("كل", [106]), ("ده،", [107]),   # ASR: "دوت"
    ("عقوبة", [108]), ("الإيقاف", [109]), ("اللي", [110]),
    ("جت", [111]),                               # ASR: "جاءت"
    ("3", [112]), ("مباريات", [113]),            # spoken "تلات"
    ("من", [114]), ("الفيفا", [115]), ("بعد", [116]), ("أحداث", [117]),
    ("مباراة", [118]), ("الأرجنتين", [119]), ("في", [120]), ("كأس", [121]),
    ("العالم.", [122]),
    ("زاد", [123]), ("عليها", [124]), ("حياته", [125]), ("الشخصية،", [126]),
    ("والأزمات", [127]), ("الشخصية", [128]), ("تحولت", [129]), ("ساعتها", [130]),
    ("إلى", [131]),
    ("أزمة", [132]),                             # ASR pass 1 "زماة", pass 2 "أزمات"
    ("إعلامية", [133]), ("ومؤسسية.", [134]),
    ("هل", [135]), ("اضطرت", [136]),
    ("الجبلاية", [137]),                         # ASR: "الجبلية/الجبالية" (Egyptian FA HQ)
    ("وقتها", [138]), ("إن", [139]), ("هي", [140]), ("تشوف", [141]),
    ("إن", [142]), ("ده", [143]), ("مش", [144]), ("من", [145]),
    ("مصلحة", [146]), ("المنتخب،", [147]),
    ("فاضطرت", [148]),                           # ASR: "فاتطرت"
    ("إن", [149]), ("هي", [150]), ("تقيل", [151]), ("حسام", [152]),
    ("حسن", [153]), ("والجهاز", [154]), ("المعاون", [155]), ("كله.", [156]),
    ("والبديل", [157]), ("كان", [158]), ("ساعتها", [159]), ("علي", [160]),
    ("ماهر", [161]), ("و…", [162]),
    ("طيب.", [163]),
]

# Manual start overrides (seconds), verified on the spectrogram / silence map, where DTW
# placed a word inside silence or out of order.
OVERRIDE_START = {
    2: 5.83,   # "حسام" — DTW put it at 4.32 inside the greeting; speech resumes 5.83
    3: 6.17,   # "حسن"
    0: 3.62, 1: 4.00,
    79: 46.90,  # "انتقادات" belongs to the chunk after the 46.47 pause
    97: 61.45,   # "خسّرته" is the 61.38–62.09 chunk (DTW 60.68 sat in the pause)
    157: 102.85, # "كان" (drawn-out "والبديل" fills 101.40–102.45)
    107: 69.05, # "عقوبة" is the short 68.99–69.64 chunk (DTW said 67.06, inside silence)
}

def silences():
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(ROOT / "work/dialogue48k.wav"),
         "-af", "silencedetect=noise=-35dB:d=0.2", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", out)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", out)]
    return list(zip(st, en))

SIL = silences()

# speech chunks = complement of silences inside [0, 111.89]
CH = []
prev = 0.0
for a, b in SIL:
    if a - prev > 0.05:
        CH.append([prev, a])
    prev = b
if 111.89 - prev > 0.05:
    CH.append([prev, 111.89])

def chunk_of(t):
    for k, (a, b) in enumerate(CH):
        if a <= t < b:
            return k
    # inside a silence: attach to the nearer neighbouring chunk edge
    best, bd = 0, 1e9
    for k, (a, b) in enumerate(CH):
        d = min(abs(t - a), abs(t - b))
        if d < bd:
            best, bd = k, d
    return best

words = []
for i, (text, idx) in enumerate(WORDS):
    t = OVERRIDE_START.get(i, dtw[idx[0]]["s"])
    words.append({"text": text, "t": t, "k": chunk_of(t)})
# chunk assignment must be monotonic
for i in range(1, len(words)):
    words[i]["k"] = max(words[i]["k"], words[i - 1]["k"])

from collections import defaultdict
groups = defaultdict(list)
for i, w in enumerate(words):
    groups[w["k"]].append(i)

def clen(txt):
    return len(re.sub(r"[^\w]", "", txt)) + 1.5

for k, ids in groups.items():
    a, b = CH[k]
    ts = [words[i]["t"] for i in ids]
    ok = all(a - 0.05 <= x <= b for x in ts[1:]) and all(ts[j] < ts[j + 1] for j in range(len(ts) - 1))
    if ok and len(ids) > 1:
        starts = [a] + [max(a, min(x, b - 0.06)) for x in ts[1:]]
    else:  # character-proportional spread across the chunk
        L = [clen(words[i]["text"]) for i in ids]
        tot = sum(L); acc = 0; starts = []
        for l in L:
            starts.append(a + (b - a) * acc / tot); acc += l
    for j, i in enumerate(ids):
        words[i]["start"] = round(starts[j], 3)
        words[i]["end"] = round(starts[j + 1] if j + 1 < len(ids) else b, 3)

# a speech chunk with no word is the audible tail of the previous word (drawn-out vowel)
for k, (a, b) in enumerate(CH):
    if k not in groups:
        prev = [w for w in words if w["end"] <= a + 1e-6]
        if prev and a - prev[-1]["end"] < 0.45:
            prev[-1]["end"] = round(b, 3)

for i, w in enumerate(words):
    w["id"] = f"w{i}"
out = [{"id": w["id"], "text": w["text"], "start": w["start"], "end": w["end"]} for w in words]
json.dump(out, open(ROOT / "transcript.json", "w"), ensure_ascii=False, indent=1)
json.dump(SIL, open(ROOT / "work/silences.json", "w"))
for w in out:
    print(f'{w["id"]:>5} {w["start"]:7.3f}-{w["end"]:7.3f} {w["text"]}')
