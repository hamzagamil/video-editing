"""The edit, written by hand: takes in story order, scenes, cues, captions, crops, sound.

Source times are seconds in ../source/rawreel.mov. Word ids (wN) refer to transcript.json, which
tools/cut.py regenerates from TAKES; after changing TAKES, rerun cut.py and re-check the ids below.
"""

SLIVER_MAX, SLIVER_DB = 0.40, -40.0  # silent slivers between two pauses are dropped (the speaker leans to read there)
PAUSE_SPLIT = 0.20  # silences longer than this inside a take are trimmed (to ~3 + 2 frames); map: silencedetect -34 dB

# Re-transcriptions of stretches where the first pass merged a retake into a stretched word.
WORD_FIXES = [
    ("whisper_fix.json", [[407.6, 431.0], [621.8, 632.0], [634.5, 652.0], [790.8, 803.2]]),
    ("whisper_fix2.json", [[411.6, 422.4]]),
]

# ---------------------------------------------------------------- takes (story order)
TAKES = [
    {"id": "T01", "src": [20.30, 31.72]},   # تخيل إنك بتلعب قدام لاعب كرة قدم بيبص في حتة وبيباصي الكورة للاعب تاني موجود في حتة تانية
    {"id": "T02", "src": [37.50, 42.36]},   # لاعب بيقعد يتمشى 80% في الماتش   (the corrected "في الملعب" dropped)
    {"id": "T03", "src": [49.45, 58.42]},   # في الحقيقة هو قاعد بيرسم خريطة في دماغه إزاي هيلعب الكورة لما توصل له
    {"id": "T04", "src": [67.70, 70.90]},   # ده عقل بيشتغل بسرعة الكمبيوتر
    {"id": "T05", "src": [77.40, 88.95]},   # ودي اسمها هندسة الماتريكس العقلية ليونيل ميسي
    {"id": "T06", "src": [98.40, 104.60]},  # العلماء والخبراء التكتيك قاعدوا يدرسوا عقلية ميسي
    {"id": "T07", "src": [109.58, 113.62]}, # واكتشفوا مصطلح غريب اسمه الماسح الضوئي
    {"id": "T08", "src": [119.50, 127.35]}, # ميسي من أكتر اللعيبة اللي بتعمل اسكان للملعب وهو بيتحرك
    {"id": "T09", "src": [137.48, 141.36]}, # الاسكان ده وهو لسه الكورة في رجل زميله
    {"id": "T10", "src": [160.88, 166.94]}, # عقل ميسي بيكون على حسب سرعة اللاعب اللي قدامه ومكانة مركزه  (third take)
    {"id": "T11", "src": [172.78, 175.90]}, # والزاوية اللي بين رجلين الحارس
    {"id": "T12", "src": [180.48, 199.50]}, # علشان كده ... يعني شايف المستقبل زي ما بنقول كده قبل ما يحصل  (filler kept: no clean gap to cut it)
    {"id": "T13", "src": [233.19, 237.79]}, # عارفين ده معناه ايه ان ميسي مش بيبتكر الكورة في لحظتها  (4th take)
    {"id": "T14", "src": [246.35, 251.12]}, # عارف بينفذ خطة هندسية رسمها في دماغه
    {"id": "T15", "src": [258.62, 266.90]},  # تعال أقولك على سر مرعب.. علمياً المدافع العادي (the held beat was dropped: he leans to read in it)
    {"id": "T16", "src": [274.51, 293.38]}, # بيشوف الحركة وبعدين عقله بيبعت إشارة للعضلة علشان تتحرك وتنفذ أمر
    {"id": "T17", "src": [299.20, 305.80]}, # الحركة دي بتحتاج من 3 إلى 4 عشار من الثانية عشان ينفذها
    {"id": "T18", "src": [310.22, 314.30]}, # بس مع ميسي ده ما بيسويش أي حاجة خالص بالنسبة له
    {"id": "T19", "src": [321.28, 328.80]}, # خبراء كتير بيقولوا إن عقل ميسي مش بيستنى رد الفعل
    {"id": "T20", "src": [351.34, 366.50]}, # ميسي هو اللي بيبرمج رد فعل المدافع قبل ما يحصل. وقبل ما الكورة توصل للمدافع أصلاً
    {"id": "T21", "src": [371.81, 379.25]}, # هو عارف إن ميسي لو عمل بكتفه يمين عارف إن اللاعب هيروح ناحية الشمال بنسبة 99%
    {"id": "T22", "src": [383.44, 385.80]}, # ميسي مش بيجري أسرع من المدافع
    {"id": "T23", "src": [390.10, 395.96]}, # ميسي عايش في المستقبل وراسم السيناريو قبلها بثانية
    {"id": "T24", "src": [416.20, 420.72]}, # المدافع بيعمل زي الآلة المكسورة اللي بيحاول يلحق ميسي  (2nd take)
    {"id": "T25", "src": [427.52, 430.30]}, # دايماً بيكون متأخر بخطوة
    {"id": "T26", "src": [444.46, 450.40]}, # المدافع العادي بيجري ورا الكورة. لكن مع ميسي الدنيا بتختلف تماماً
    {"id": "T27", "src": [472.60, 477.18]}, # المدافع هو اللي بيجري ورا وهم ميسي
    {"id": "T28", "src": [482.70, 497.95]}, # ميسي بيمشي ببطء. بيخلي المدافع يقرب منه. وبيحس بالأمان. وفي لحظة
    {"id": "T29", "src": [503.33, 507.35], "hold": [(507.23, 0.35)]},  # المدافع بيمد رجله عشان يقطع الكورة (held beat)
    {"id": "T30", "src": [517.38, 532.55]}, # لكن في تتش سريع جداً ... دي اللحظة اللي بيكون فيها ميسي سابق عقلية المدافع بثانية
    {"id": "T31", "src": [544.12, 566.80]}, # ميسي مش بيمر ... عشان يفترسه. لا ده كأنه بيكتب معادلة هندسية ماتريكس على سبورة وبيعلمها لكل اللي في الاستاد
    {"id": "T32", "src": [573.32, 591.32]}, # الكورة في رجل ميسي مش لعبة بس. الكورة في رجل ميسي هندسة وموسيقى وهو العازف الوحيد ...
    {"id": "T33", "src": [626.60, 629.30]}, # لعيبة كتيرة بتجري وبتسجل أهداف  (4th take)
    {"id": "T34", "src": [644.60, 650.75]}, # بس التاريخ بيفتكر مين اللي خلى الكورة في رجله موسيقى  (5th take)
    {"id": "T35", "src": [658.75, 682.90], "hold": [(664.31, 0.4)]},  # وكأن الكورة بتنام في رجله وبتسمع كلامه. ميسي مش لعيب كورة. ميسي دي عبقرية اتولدت في جسم إنسان
    {"id": "T36", "src": [769.54, 778.10]}, # لو كنت فاكر إن ميسي شاطر بس عشان بيجيب أجوان، يبقى انت ما فهمتش المعادلة صح  (2nd take)
    {"id": "T37", "src": [715.38, 719.82]}, # ميسي هو مؤسس هندسة الماتريكس في الملعب  (2nd take)
    {"id": "T38", "src": [782.08, 789.40]}, # شاركنا في الكومنتات. أكتر لحظة حسيت فيها إن ميسي بيلعب فيديو جيم
    {"id": "T39", "src": [798.88, 801.75]}, # والناس كلها NPCs  (3rd take)
]

# Leans that overlap speech: (source from, source to, clean source frame held over them). Video only.
FREEZE = [
    (450.17, 450.40, 450.13),  # tail of «تماماً.» (T26)
]

# Source spans removed by hand: the lean continues after the last word, in silence.
TRIM = [(261.03, 261.40), (264.38, 264.45), (356.13, 356.40), (682.45, 682.90)]

# Whisper spelling -> what was said (checked against the audio context; Egyptian spelling kept)
SPELL = {
    "مصطلع": "مصطلح", "والخبراء": "وخبراء", "قاعدوا": "قعدوا", "الكرة": "الكورة", "لي": "له",
    "المدافقة": "المدافع", "عالش": "عايش", "قبليها": "قبلها", "يفترسوه": "يفترسه", "بيكتم": "بيكتب",
    "صبورة": "سبورة", "شوتر": "شاطر", "إجوان": "أجوان", "أن": "إن", "ان": "إن", "ايه": "إيه",
    "أصلا": "أصلاً", "تماما": "تماماً", "باللعيب": "باللعيب",
}

import json as _json
from pathlib import Path as _P
# Photo treatment: media-treatment "Monochrome Screen Print" (ink #1B1D1E on paper #EFE6D8), persisted
# with `hyperframes media-treatment` and reused for every print (see tools/photo_grade.json).
PHOTO_GRADE = _json.loads((_P(__file__).parent / "photo_grade.json").read_text())

# ---------------------------------------------------------------- cue words (ids in transcript.json)
CUES = {
    "g1_look": 8, "g1_pass": 11, "g1_other": 16,
    "g2_truth": 27, "g2_draw": 30, "g2_map": 31, "g2_head": 33,
    "g3_eng": 47, "g3_matrix": 48, "g3_mental": 49, "g3_lionel": 50, "g3_messi": 51,
    "o1_mind": 57, "o1_messi": 58,
    "g4_term": 60, "g4_strange": 61, "g4_named": 62, "g4_scanner": 63, "g4_messi": 65, "g4_scan": 71, "g4_moving": 74,
    "g5_speed": 88, "g5_pos": 92, "g5_angle": 94, "g5_keeper": 98,
    "g6_do": 109, "g6_pass": 112, "g6_move": 114, "g6_sees": 117, "g6_future": 118, "g6_before": 123,
    "g7_plan": 139, "g7_drew": 141, "g7_head": 143,
    "g8_ordinary": 151, "g8_sees": 152, "g8_move": 153, "g8_then": 154, "g8_brain": 155, "g8_signal": 157,
    "g8_muscle": 158, "g8_moves": 160, "g8_exec": 161,
    "o2_second": 172,
    "g9_shoulder": 218, "g9_knows2": 220, "g9_go": 223, "g9_left": 225, "g9_by": 226, "g9_pct": 227,
    "g10_machine": 248, "g10_catch": 252, "g10_always": 254, "g10_late": 256,
    "g11_walk": 277, "g11_lets": 279, "g11_near": 281, "g11_feels": 283, "g11_safe": 284,
    "g12_touch": 295, "g12_very": 297,
    "g13_writes": 332, "g13_eq": 333, "g13_on": 336, "g13_board": 337, "g13_teach": 338,
    "g14_eng": 354, "g14_music": 355, "g14_player": 357, "g14_only": 358, "g14_field": 361,
    "g15_sleeps": 384, "g15_foot": 386, "g15_listens": 387, "g15_words": 388,
    "g16_is": 417, "g16_founder": 418, "g16_eng": 419, "g16_matrix": 420, "g16_in": 421, "g16_field": 422,
    "g17_video": 433, "g17_people": 435, "g17_npc": 437,
}

L = -0.04  # pages cut in a frame before the word that drives them
CLOSING_AT = ("speech_end", 0.5)
CLOSING = {"file": "17-chawali.wav", "at": CLOSING_AT, "dur": 5.333, "gain_db": -1.0}

# ---------------------------------------------------------------- scenes: (id, template, start, end, label[, kind])
SCENES = [
    ("g1", "g1-nolook.html", ("w", 5, L), ("w", 19, 0.45), "No-look pass (holds into «لاعب بيقعد»)"),
    ("o0", "o0-walk.html", ("w", 21, -0.05), ("w", 26, L), "Card: walking (p1)", "overlay"),
    ("g2", "g2-map.html", ("w", 26, L), ("w", 34, L), "Footsteps become a map"),
    ("g3", "g3-title.html", ("w", 45, L), ("w", 52, L), "Title page: هندسة الماتريكس (p2)"),
    ("o1", "o1-study.html", ("w", 56, -0.05), ("w", 59, L), "Card: studied (p4)", "overlay"),
    ("g4", "g4-scan.html", ("w", 59, L), ("w", 75, L), "The scanner (p3)"),
    ("g5", "g5-calc.html", ("w", 83, L), ("w", 99, -0.005), "Three measurements"),
    ("g6", "g6-future.html", ("w", 105, L), ("w", 126, 0.68), "Sees the future (holds over his lean back into frame)"),
    ("g7", "g7-plan.html", ("w", 137, L), ("w", 145, 0.07), "A plan, then executed (holds over his lean back)"),
    ("g8", "g8-chain.html", ("w", 150, L), ("w", 163, -0.005), "The ordinary defender's chain"),
    ("o2", "o2-timer.html", ("w", 166, -0.05), ("w", 175, L), "Card: 0.3-0.4 s", "overlay"),
    ("cw1", "cw1-tanfiz.html", ("w", 174, -0.03), ("w", 175, 0.07), "Cut-away «عشان ينفذها» (covers a lean)"),
    ("cw2", "cw2-khales.html", ("w", 183, -0.02), ("w", 186, 0.0), "Cut-away «أي حاجة خالص بالنسبة له» (covers a lean)"),
    ("cw3", "cw3-messi.html", ("w", 196, L), ("w", 196, 0.36), "Cut-away «ميسي» (covers a lean)"),
    ("cw4", "cw4-yehsal.html", ("w", 205, 0.0), ("w", 206, 0.2), "Cut-away «قبل ما يحصل» (covers a lean)"),
    ("g9", "g9-feint.html", ("w", 212, L), ("w", 231, -0.005), "Shoulder feint, 99%"),
    ("cw5", "cw5-messi.html", ("w", 237, L), ("w", 237, 0.3), "Cut-away «ميسي» (covers a lean)"),
    ("g10", "g10-lag.html", ("w", 245, L), ("w", 258, 0.42), "The broken machine (holds over his lean back)"),
    ("cw6", "cw6-defender.html", ("w", 269, L), ("w", 269, 0.77), "Cut-away «المدافع» (covers a lean)"),
    ("g11", "g11-trap.html", ("w", 276, -0.25), ("w", 285, L), "The trap (p5)"),
    ("g12", "g12-touch.html", ("w", 293, L), ("w", 307, L), "The touch - hero (p6)"),
    ("gp", "gp-pounce.html", ("w", 327, L), ("w", 329, L), "Cut-away: «عشان يفترسه» (covers a lean)"),
    ("g13", "g13-equation.html", ("w", 329, L), ("w", 343, L), "An equation on a board"),
    ("g14", "g14-music.html", ("w", 350, L), ("w", 367, 0.6), "The only musician (holds over his lean back into frame)"),
    ("g15", "g15-sleep.html", ("w", 382, -0.24), ("w", 389, -0.005), "The ball sleeps (p7)"),
    ("g16", "g16-founder.html", ("w", 416, -0.2), ("w", 423, 0.25), "Founder (title callback)"),
    ("g17", "g17-cta.html", ("w", 426, L), CLOSING_AT, "CTA: video game / NPCs"),
    ("g18", "g18-closing.html", CLOSING_AT, ("speech_end", 0.5 + 5.333 + 1.3), "Closing verse (p8)"),
]

# ---------------------------------------------------------------- presenter crop states
FACE_ORIGIN = "50% 35%"
PUSH_TO, PUSH_DUR = 1.12, 0.7
CROP = [
    (("w", 19, L), 1.00), (("w", 34, L), 1.08), (("w", 40, L), 1.15), (("w", 52, L), 1.00),
    (("w", 75, L), 1.08), (("w", 99, L), 1.00), (("w", 126, L), 1.08), (("w", 144, L), 1.15),
    (("w", 163, L), 1.00), (("w", 175, L), 1.08), (("w", 186, L), 1.00), (("w", 196, L), 1.08),
    (("w", 231, L), 1.08), (("w", 237, L), 1.15), (("w", 258, L), 1.00), (("w", 269, L), 1.08),
    (("w", 285, L), 1.15), (("w", 307, L), 1.08), (("w", 319, L), 1.00), (("w", 343, L), 1.08),
    (("w", 367, L), 1.00), (("w", 372, L), 1.08), (("w", 389, L), 1.15), (("w", 400, L), 1.00),
    (("w", 410, L), 1.08), (("w", 423, L), 1.08),
]

# ---------------------------------------------------------------- captions (presenter windows only)
CAPTION_TOP = 1170
CAPTIONS = [
    [1, 2], [3, 4],
    [21], [22, 24, 25],
    [34, 35], [36, 37], [38, 39], [40, 41], [42, 43, 44],
    [52, 53, 54], [55, 56], [57, 58],
    [75, 76], [77, 78], [79, 80, 81, 82],
    [99, 100], [101, 102, 103, 104],
    [127, 128, 129], [130, 131, 132], [133, 134], [135, 136],
    [145], [146, 147, 148], [149],
    [163, 164, 165], [166, 167, 168, 169, 170], [171, 172], [173, 174], [175, 176, 177], [178, 179, 180],
    [181, 182, 183],
    [186, 187, 188], [189, 190, 191], [192, 193], [194, 195], [197, 198], [199], [200, 201, 202],
    [203, 204, 205], [207, 208], [209, 210, 211],
    [231, 232, 233], [234, 235, 236], [238], [239, 240], [241, 242], [243, 244],
    [259], [260, 261, 262], [263, 264, 265], [266, 267, 268], [270, 271], [272, 273, 274, 275],
    [285, 286], [287, 288, 289], [290, 291, 292],
    [307, 308, 309, 310], [311, 312, 313], [314, 315], [316, 317], [318], [319, 320, 321], [322, 323],
    [324, 325, 326],
    [343, 344, 345, 346], [347, 348, 349],
    [368, 369], [370, 371], [372, 373], [374, 375], [376, 377, 378], [379, 380], [381],
    [389, 390, 391, 392], [393, 394], [395], [396, 397, 398, 399],
    [400, 401, 402], [403, 404, 405], [406, 407, 408, 409], [410, 411, 412, 413], [414, 415],
    [424, 425],
]
CAPTION_TEXT = {22: "80%", 378: "الكورة", 79: "الكورة"}
# one highlight per group: o = warm, s = sky (the future), g = «عبقرية» (warm + gold underline)
HL = {21: "o", 22: "o", 44: "o", 56: "o", 82: "o", 103: "o", 129: "o", 133: "o", 148: "o", 167: "o",
      172: "o", 177: "o", 180: "o", 193: "o", 199: "o", 205: "o", 211: "o", 234: "o", 240: "s", 244: "o",
      262: "o", 267: "o", 274: "o", 289: "o", 315: "o", 318: "o", 348: "o", 374: "o",
      381: "o", 392: "o", 395: "g", 405: "o", 414: "o", 425: "o"}

# ---------------------------------------------------------------- sound: (id, file, at, gain dB, dur | (from, to), extra attrs)
def _between(a, b):
    return ("between", a, b)


SFX = [
    ("sfx-future1", "04-reverse.wav", ("w", 118, -1.59), -12, 1.62, ""),            # the future is heard before it is seen
    ("sfx-clock", "06-clock.wav", ("w", 166, -0.13), -7, _between(("w", 166, -0.13), ("w", 175, -0.02)), ' data-fade-out="0.02"'),
    ("sfx-future2", "04-reverse.wav", ("w", 225, -1.69), -12, 1.62, ""),            # peaks as the defender starts to move
    ("sfx-heart1", "08-heartbeat.wav", ("w", 277, -0.12), -8, 4.5, ' data-fade-out="0.05"'),
    ("sfx-heart2", "08-heartbeat.wav", ("w", 277, 4.38), -8, _between(("w", 277, 4.38), ("we", 292, 0.05)), ' data-fade-out="0.08"'),
    ("sfx-tap", "09-tap.wav", ("w", 295, -0.16), -9, 0.36, ""),
    ("sfx-impact", "10-impact.wav", ("w", 295, -0.06), -6, 3.0, ""),
    ("sfx-roar", "11-roar.wav", ("w", 295, -0.02), -9, 2.5, ""),
    ("sfx-crowd", "15-crowd-far.wav", ("w", 382, -0.04), -12, _between(("w", 382, -0.04), CLOSING_AT), ' data-fade-in="2" data-fade-out="0.5"'),
    ("sfx-plan", "click-soft.mp3", ("w", 143, 0.1), -14, 0.36, ""),
    ("sfx-stamp", "click-soft.mp3", ("w", 418, 0.12), -12, 0.36, ""),
    ("sfx-bubble", "pop.mp3", ("we", 437, 0.3), -16, 0.36, ""),
]
