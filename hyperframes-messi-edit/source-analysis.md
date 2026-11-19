# Source analysis — `rawreel.mov`

## Metadata (ffprobe)
- 811.28 s (13 min 31 s), 3.79 GB, QuickTime MOV from an iPhone.
- Video: HEVC Main 10, 3840×2160 stored, **rotation −90** → vertical 2160×3840, yuv420p10le,
  **HDR HLG** (`arib-std-b67`, BT.2020 primaries/matrix, tv range), 30 fps nominal (avg 30.002, slightly variable).
- Audio: AAC-LC 48 kHz stereo, 118 kb/s, lav mic (BOYA). Integrated −25.7 LUFS, peak −5.8 dBFS,
  noise floor ≈ −59 dB (clean room, no denoise needed).

## Colour decision
Compared on one frame: plain HLG→709 transfer (natural skin, but the cream wall clips), `tonemap=hable`
(flat, dark), `tonemap=mobius` (washed, pink). Chosen: **hable** for highlight roll-off, then a correction
on top — S-curve lifting the face (mids 0.5→0.585), saturation +10 %, slight warm balance (R +0.02 / B −0.03),
very light vignette. Wall stays warm cream (it matches the paper palette), skin natural, blacks not crushed.
Filter chain in `tools/grade.txt`, applied at 1080×1920 with the tonemap after the downscale (3.2× realtime).

## Framing
Medium shot, presenter centred on an ornate cream/gold chair, black shirt, lav visible. Face centre ≈
(540, 660) px on the 1080×1920 canvas (eye line ≈ 34 %), chin ≈ 52 %, head top ≈ 22 %. Hands gesture in the
lower third. Between takes he leans out of frame to read — every such stretch is cut.

## Speech, silence, takes
- silencedetect −34 dB / 0.2 s on the WAV (−38 dB map kept for reference): ≈ 290 s of speech in 811 s.
- Many lines have 2–5 takes. The best (complete, most fluent, latest) take of each line was chosen; see
  `SCRIPT_DIFF.md` and `tools/plan.py` (TAKES, with the source time of every take).
- Retained: 137 ranges, 216.3 s of speech. Removed: 595 s — 50 retake / set-up / dead-air ranges and the rest
  pauses > 0.20 s trimmed to ~3 frames after speech and ~2 before the next word. Deliberate holds kept after
  «سر مرعب» (0.5 s), «يقطع الكورة» (0.35 s) and «كلامه» (0.4 s).
- Cut points were checked for energy: every edge sits in silence (< −34 dB) except where a phrase runs on
  with no gap; there the cut was moved or the phrase kept (the «زي ما بنقول كده» filler stays for that reason).

## Transcription method
faster-whisper large-v3 (int8, CPU) on each candidate take with an Egyptian-dialect prompt; four stretches
where the model merged a retake into one stretched word were re-transcribed separately (`whisper_fix*.json`).
Word times come from whisper's alignment, clamped to the kept ranges; spelling corrected for dialect and
names (`plan.SPELL`). Remaining uncertainty: the phrase «ميسي كل لمس الكورة بعد ما اداله الأمان تماماً»
is not fully intelligible — it plays in the audio but is not put on screen.

## Semantic beats
hook (no-look pass) → walking 80 % → mental map → computer brain → title «هندسة الماتريكس» → studied →
the scanner → three measurements → sees the future → a plan, not improvisation → secret: the ordinary
defender's 0.3–0.4 s chain → Messi programs the defender → shoulder feint 99 % → lives in the future →
the broken machine → chasing an illusion → the trap → **the touch (peak)** → an equation on a board →
the only musician → history remembers → the ball sleeps → genius (payoff) → founder → CTA → closing verse.
