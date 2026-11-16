# Source analysis — `rawreel.mov`

## Metadata (ffprobe)
| Field | Value |
| --- | --- |
| Container | QuickTime MOV, 111.892 s, 37.6 Mb/s, 526 MB |
| Video | HEVC Main 10, 3840×2160 coded, rotation −90° → displays 2160×3840 (9:16 portrait) |
| Frame rate | 30/1 nominal (avg 251775/8392 = 30.0003), 3357 frames |
| Colour | yuv420p10le, BT.2020 primaries, ARIB STD-B67 (HLG) transfer — iPhone HDR |
| Audio | AAC-LC, 48 kHz, stereo (dual-mono lav) |
| Other | 5 Apple metadata tracks (ignored) |

Decision: deliver 1080×1920 @ 30 fps (source-native, no conversion). The HLG footage is converted to
SDR BT.709 with zscale (HLG→BT.709 transfer, BT.2020→BT.709 primaries, npl 203) — compared against
hable/mobius/reinhard tonemaps on the same frame; the plain conversion kept natural skin and real
contrast, the tonemaps were flat or blown (`work/tm/compare.png`). Proxy: `assets/media/aroll.mp4`
(H.264 CRF 15, GOP 15 for seek-safety, processed dialogue muxed in). The original is untouched.

## Picture
- One locked-off medium shot for the whole take: presenter seated centre-left on a striped gold
  sofa, white wall + embroidered hanging above, sheer curtain right. Grey hoodie, navy/white
  striped polo, wireless lav receiver in both hands.
- 0.0–3.0 s: empty sofa, presenter walks in and adjusts the camera. 3.0–5.6 s: sits, settles,
  says "مساء الخير". 5.8–107 s: talks to camera with small hand movements around the receiver
  (lap level, bottom of frame). 107–111.9 s: reaches for the camera, frame lurches.
- In the 1080×1920 frame: face centre ≈ (520, 880), eyes y≈865, head top y≈650, chin y≈1120,
  hands y≈1700–1900. The face is slightly left of and above frame centre → crop origin
  48% / 45.8% keeps eyes and chin fixed for every punch; captions at y≈1270 stay on the torso.
- Bright, high-key exposure; wall near clipping but holds detail after the SDR conversion.

## Audio
- Very clean lav: noise floor −75 dBFS RMS in pauses, speech RMS ≈ −35 dBFS, integrated −31.4 LUFS,
  peak −3.3 dBFS (the 0 dBFS peaks are camera-handling thumps in 0–5.6 s and 107 s+, both cut).
- No denoise needed (would only add artefacts). Chain: high-pass 70 Hz → gentle compressor
  (−30 dB, 2.2:1, 12/220 ms) → loudnorm (I −14, TP −1.5, LRA 11) → −14.0 LUFS, speech peaks
  −1.5 dBTP.

## Silence map (silencedetect −35 dB, ≥ 0.2 s), seconds
0.00–0.95, 0.96–1.57, 1.58–1.84, 1.94–2.45, 3.46–3.69, 4.18–4.38, **4.69–5.83**, 10.71–11.34,
12.81–13.11, 13.50–14.26, 14.94–15.45, 15.47–15.93, 18.81–19.43, 20.20–20.94, 24.31–24.56,
25.04–26.34, 29.42–30.20, 32.01–32.94, 36.66–37.25, 38.07–38.33, 40.64–42.18, 46.47–46.84,
48.06–49.21, 51.92–52.57, 53.34–53.96, 55.65–56.84, 57.76–57.97, 60.55–61.38, 62.09–62.48,
64.84–65.68, 66.70–68.99, 69.64–69.88, 74.03–74.24, 75.02–76.87, 77.13–77.68, 80.69–81.35,
81.88–82.95, 85.81–86.95, 88.79–89.67, 90.40–91.21, 93.92–95.40, 97.41–97.68, 99.69–100.07,
100.23–101.40, 101.77–102.00, 102.44–102.82, 103.15–103.38, 104.93–106.15, 106.96–110.01, …

Every cut was checked against the transcript: no pause is removed inside a word, and the
spectrogram of 101–107 s confirmed "والبديل" is one drawn-out word (101.4–102.5) and that the
1.2 s pause before "علي ماهر" is deliberate (kept at 0.40 s).

## Transcription method
1. `hyperframes transcribe` (whisper.cpp v1.9.5, `ggml-large-v3`, sha256-verified, `--language ar`).
2. whisper.cpp large-v3 with DTW token timestamps (`-nfa -dtw large.v3`) for word timing.
3. Manual review: dialect wording from pass 1 (pass 2 drifted to MSA), proper names corrected
   (حسام حسن، الجبلاية، علي ماهر، الشناوي), mishearings fixed (الضيق، خسّرته، ده، جت، أزمة).
4. Word times = DTW starts clamped into measured speech chunks (complement of the silence map);
   chunk edges come from the waveform, not the model. Four manual overrides, documented in
   `tools/align.py`.
5. Remaining uncertainty (minor, does not change meaning): "يرمز" vs "بيرمز"; "أزمة" vs "أزمات"
   (pass 1 heard a singular); "محدش يصدّقه" (ASR "محدش تصدق"); a possible very short "ما" before
   "يقدر" at 38.7 s that one pass produced with low confidence — omitted.

## Content summary and semantic beats (source times)
| # | Source | Beat | Verified words |
| --- | --- | --- | --- |
| 0 | 3.6–4.2 | greeting (cut) | مساء الخير |
| 1 | 5.8–10.7 | Hook: legend → World Cup coach | حسام حسن، من أسطورة الكرة المصرية، لمدرب يقود المنتخب في كأس العالم |
| 2 | 11.3–14.9 | Contrast: the exit | إلى الخروج من الباب الضيق يوم 7 نوفمبر |
| 3 | 15.9–21.0 | What the name meant | حسام حسن، الاسم اللي كان كله يرمز إلى الروح والعزيمة |
| 4 | 21.0–25.0 | Emotional statement | انتهت رحلته مع المنتخب المصري بشكل محدش يصدّقه |
| 5 | 26.3–33.7 | The question | السؤال هنا: إزاي مدرب قاد مصر في المونديال، وكان عقده مستمر لـ2030، يمشي فجأة؟ |
| 6 | 33.7–40.6 | Fork: technical vs off-pitch | هل السبب هو كان فني، ولا مشاكل خارج الملعب كانت أكبر من إنه هو يقدر يسيطر عليها؟ |
| 7 | 42.2–55.7 | Crisis 1: Salah | الأزمات داخل المنتخب بدأت … لما انتقادات لمحمد صلاح وتبديله في مباراة أنجولا، وبعدها محمد صلاح غادر المنتخب |
| 8 | 56.8–64.8 | Crisis 2: El-Shenawy statements | وكمان تصريحات حسام عن محمد الشناوي خسّرته شريحة كبيرة جدًا من الجماهير المصرية |
| 9 | 65.7–75.0 | Crisis 3: FIFA ban | وفوق كل ده، عقوبة الإيقاف اللي جت 3 مباريات من الفيفا بعد أحداث مباراة الأرجنتين في كأس العالم |
| 10 | 76.9–85.8 | Crisis 4: personal → institutional | زاد عليها حياته الشخصية، والأزمات الشخصية تحولت ساعتها إلى أزمة إعلامية ومؤسسية |
| 11 | 86.9–100.2 | The FA's decision | هل اضطرت الجبلاية وقتها إن هي تشوف إن ده مش من مصلحة المنتخب، فاضطرت إن هي تقيل حسام حسن والجهاز المعاون كله |
| 12 | 101.4–106.9 | Payoff: replacement | والبديل كان ساعتها … علي ماهر |
| — | 106.9–111.9 | tail (cut) | و… طيب. |

Claims are the speaker's own; the edit visualises them without adding numbers, results, logos,
photos or screenshots.
