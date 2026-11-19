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

## Rendered file (`final_reel.mp4`, `--quality delivery --sdr --strict`, exit 0) — revision 2
- 1080×1920, 30 fps, 6,576 frames, H.264 + AAC 48 kHz stereo, 219.200 s, 217.2 MB (7.9 Mb/s). About 4.2 s shorter than the first render.
- Final mix: **−14.5 LUFS** integrated, LRA 3.2 LU, true peak **−1.1 dBTP**.
- Black frames: per-frame luma (YAVG) scan of every frame finds **no one-frame dips** (min YAVG 98.7). The first revision render had 6 one-frame flashes at clip starts (a renderer seek bug); the presenter is now one baked, continuous clip (`tools/aroll_edit.py`), so there are no clip starts left.
- A/V: rendered audio vs `dialogue.wav` cross-correlation lag 0 ms at 30, 100, 150 and 200 s.
- Lean fixes checked frame by frame in the render: T15 tail (≈74.0 s), fz1 «يحصل.» (100.03 s), fz2/fz3 «تماماً.» / «المدافع» (127.37–127.87 s), the «يفترسه» cut-away (155.70–157.97 s), and the extended G6/G14 pages.
- Left in: a short eyes-down glance on «فهمتش المعادلة» (~200.7 s); the presenter stays centred.
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
