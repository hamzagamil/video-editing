# REVIEW — final render

## Measured
- `hyperframes check`: **0 errors** (lint, runtime, layout, motion, contrast, craft, audio).
- `keyframes`: opening push 1.00 → 1.12 in 0.70 s `expo.out`, then hard crop sets at 26 motivated points.
- A-roll proxy: 15,800 frames = the sum of the 33 graded candidate clips; 137 retained ranges, all frame-snapped.
- Cut points: energy at every edge measured in the source audio; all sit in silence (< −34 dB) after three
  edges were moved (the «زي ما بنقول كده» filler was kept because it has no clean gap).
- Dialogue: −14.5 LUFS integrated, −1.5 dBFS peak (two-pass loudnorm, linear). Final mix to be measured on
  the rendered file. The sound was measured, not heard.
- Snapshots: three passes (first frames and end states of every page, the hit at «تتش» ±, the closing card),
  then `snapshot --review` for seams and phone sheets (stopped early to free CPU for the render, so its
  beat sheets are partial; the rendered file was checked frame by frame at 23 key times instead).

## Rendered file (`final_reel.mp4`, `--quality delivery --sdr --strict`, exit 0) — revision 3
- 1080×1920, 30 fps, 6,562 frames, H.264 + AAC 48 kHz stereo, 218.733 s, 207.9 MB (7.6 Mb/s). 0.47 s shorter than revision 2.
- Final mix: **−14.5 LUFS** integrated, LRA 3.1 LU, sample peak **−1.2 dBFS**.
- Black frames: per-frame luma (YAVG) scan of every frame finds **no one-frame dips** (min YAVG 98.7).
- A/V: rendered audio vs `dialogue.wav` cross-correlation lag 0 ms.
- Leans (reading the script, then coming back): measured with a mediapipe face tracker (nose position + head
  pitch per frame), not by eye alone. The pattern was a lean down-left at the end of a sentence and the return
  at the start of the next one. Fixes:
  - page holds or earlier page starts at about 12 sentence edges (G5–G11, G14–G16);
  - six full-screen word cards over leans that fall inside speech: «عشان ينفذها» (cw1), «أي حاجة خالص»
    (cw2), «ميسي» (cw3, cw5), «قبل ما يحصل» (cw4), «المدافع» (cw6);
  - one silent lean-out after «إنسان.» trimmed (`TRIM` 356.13–356.40);
  - the fz1–fz3 freeze stills dropped: their held frames were themselves mid-lean.
- Tracker run on the final render: no uncovered lean left. Remaining flags were checked on contact sheets and
  are natural: hand-to-head on «عقل ميسي مش» (~94 s), short glances/blinks (~17, 31, 67, 74, 102, 126, 135,
  138, 155 s), one-frame tracker misses at hard cuts, and the 190.7–194.2 s push-in on «عبقرية اتولدت في
  جسم إنسان» (face off-centre because of the crop; he is upright and on camera).
- Cover: `cover.png` (G3 «هندسة الماتريكس», 24 s), re-exported from this render.

## Director's scores (1–5, after the revision pass)
| Scene | Hook | Clarity | Mute | Sync | Colour code | Truth | Craft | Rhythm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 + G1 no-look | 4 | 5 | 5 | 5 | 5 | 5 | 4 | 4 |
| G2 map | – | 4 | 4 | 5 | 5 | 5 | 5 | 4 |
| G3 title (p2) | – | 5 | 5 | 5 | 5 | 5 | 5 | 4 |
| G4 scanner (p3) | – | 4 | 5 | 5 | 5 | 5 | 5 | 4 |
| G5 three measurements | – | 5 | 5 | 5 | 5 | 5 | 5 | 4 |
| G6 sees the future | – | 4 | 5 | 5 | 5 | 5 | 5 | 4 |
| G7 plan | – | 4 | 4 | 5 | 5 | 5 | 5 | 4 |
| G8 chain + card 0.3–0.4 s | – | 5 | 5 | 5 | 5 | 5 | 5 | 4 |
| G9 feint 99 % | – | 4 | 5 | 5 | 5 | 5 | 4 | 4 |
| G10 broken machine | – | 5 | 5 | 5 | 5 | 5 | 5 | 4 |
| G11 trap (p5) → G12 touch (p6) | – | 4 | 4 | 5 | 5 | 5 | 4 | 5 |
| G13 equation | – | 5 | 5 | 4 | 5 | 5 | 5 | 4 |
| G14 musician | – | 5 | 5 | 5 | 5 | 5 | 5 | 4 |
| G15 sleeps (p7) → payoff | – | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| G16 founder · G17 CTA · G18 verse (p8) | – | 5 | 5 | 5 | 5 | 5 | 5 | 4 |

Fixed in the revision pass (each was below 4): four headlines that wrapped onto two lines and collided
(G2, G4, G6, G14); near-empty first frames (G1 now opens on «لاعب كرة قدم», G2/G3 draw their grid at once);
the G12 defender's lunge read as a magnifying glass (now a dashed arrow); kickers moved below the platform
status bar; «في حتة تانية» held longer; the closing line now reads for > 3 s.

## Looked at only
Arabic shaping and dot clearance on every hero word (Cairo, local woff2); bidi of «80%», «99%», «0.3–0.4 ث»;
photos never mirrored, faces not cropped, presenter never covered by a card.

## Warnings kept on purpose
- `outside_safe_zone` (13): kickers at y 280–290 sit under YouTube Shorts' taller top band, and a few wide
  headlines / the caption band touch TikTok's right rail or the lower band. All reading text stays inside
  the 168–1330 px band of the HyperFrames vertical reference; moving everything into the strictest
  per-platform box would shrink the type below a comfortable size.
- `timeline_track_too_dense` / `composition_file_too_large` on `captions.html`: one host holds every caption
  group, as the captions reference prescribes.

## Weakest shot / with more time
- G12 «تتش»: strong hit, but after the flash the page is sparse for ~4 s while he explains the touch; with
  more time I'd add a second beat (the ball leaving the safe circle) on «بعد ما اداله الأمان تماماً».
- The whole reel is 3:43 because of the calm delivery; a 60–90 s cut-down (hook → scanner → secret →
  touch → genius → CTA) would travel better on Reels/TikTok.
- Photo licences are unverified (user-supplied); the Chawali clip carries a music bed (rights risk accepted
  by the user).
