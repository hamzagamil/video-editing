# REVIEW — game version («ميسي: اللاعب رقم 1»), pre-render

## Measured
- `hyperframes lint`: 0 errors (2 warnings: `captions.html` is long/dense — 83 word-timed groups in one host,
  kept so captions stay one Studio track).
- `hyperframes check --json`: **ok, 0 errors**. Kept warnings: `outside_safe_zone` for «شايف المستقبل» (g6,
  YouTube Shorts right column; the line is centred and fully readable) and one caption group at 85 s (same
  position as every caption, over the torso). Info: g11 «يقرب منه» line box.
- Contrast: 23/23 samples pass.
- Lean windows: identical to the approved notebook cut (all 24 full-screen windows), cw5 0.07 s longer (only
  covers more). No presenter frame was added, so the face-tracker result of the notebook render still holds.
- Snapshots: 3 passes (52 + 18 + 9 frames) — every screen's middle and final state, each `cw` flash, g10 lag,
  g12 before/at/after the touch, g17 hold, the end credits. Fixed after review: 9 hero lines that wrapped out
  of their box, the g1 toast covering the pass, g8 label on its bar, g12 kicker overlap, the g13 star never
  showing, g16 star over its kicker, g18 star on the photo tag, HUD tags moved inside the platform safe band.

## Photos (Ordered Palette Dither, game palette; never mirrored, presenter never covered)
| Photo | Scene · word | Check |
| --- | --- | --- |
| p1 walking | o0 · «يتمشى» | player card beside him, 1.15 s ✓ |
| p2 portrait | g3 · «ليونيل ميسي» | P1 character portrait under the title ✓ (also `cover.png`) |
| p3 scan | g4 · «الماسح الضوئي» | 1.2 s, then shrinks into the radar ✓ |
| p4 study | o1 · «يدرسوا» | scout card + «ميسي» label, 1.1 s ✓ |
| p5 trap | g11 · «يقرب منه» | 0.9 s ✓ |
| p6 dribble | g12 · «تتش» | full flash 0.6 s on the impact ✓ |
| p7 ball | g15 · «بتنام» | 1.2 s ✓ |
| p8 celebration | g18 · first commentary word | holds to the end ✓ |

## Added sounds (synthesized locally; everything else unchanged from the notebook mix)
| id | file | time | level |
| --- | --- | --- | --- |
| ui-ach1 | ui-up.wav | g1 toast (≈4.88 s) | −17 dB |
| ui-lag | ui-lag.wav | «يلحق» (≈118.96 s) | −20 dB |
| ui-ach2 | ui-up.wav | g12 toast (≈140.35 s), inside the G12 stack | −17 dB |
| sfx-stamp | ui-up.wav (was a click) | «مؤسس» (≈201.44 s) | −16 dB |
| ui-select | ui-select.wav | NPC slots (≈209.32 s) | −16 dB |

## Director's scores (1–5, after one revision pass)
| Screen | Hook | Clarity | Mute | Sync | Colour | Truth | Craft | Rhythm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| opening + g1 no-look | 5 | 4 | 5 | 5 | 5 | 5 | 4 | 5 |
| g2 fog of war | – | 5 | 4 | 5 | 5 | 5 | 4 | 4 |
| g3 title | – | 5 | 5 | 5 | 5 | 5 | 5 | 4 |
| g4 radar | – | 4 | 5 | 4 | 5 | 5 | 4 | 4 |
| g5 lock-on ×3 | – | 4 | 5 | 5 | 5 | 5 | 4 | 4 |
| g6 aim assist | – | 5 | 5 | 5 | 5 | 5 | 4 | 5 |
| g7 move list | – | 4 | 4 | 5 | 5 | 5 | 4 | 4 |
| g8 NPC processing | – | 4 | 5 | 5 | 5 | 5 | 4 | 4 |
| cw1–cw6 flashes | – | 5 | 5 | 5 | 5 | 5 | 4 | 5 |
| g9 NPC script | – | 4 | 5 | 5 | 5 | 5 | 4 | 4 |
| g10 LAG | – | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| g11 → g12 the touch | – | 5 | 5 | 5 | 5 | 5 | 4 | 5 |
| gp wrong answer | – | 5 | 5 | 4 | 5 | 5 | 4 | 5 |
| g13 equation + stadium | – | 4 | 4 | 5 | 5 | 5 | 4 | 4 |
| g14 rhythm lane | – | 4 | 4 | 4 | 5 | 5 | 4 | 4 |
| g15 idle | – | 5 | 5 | 5 | 5 | 5 | 4 | 4 |
| g16 achievement | – | 5 | 5 | 5 | 5 | 5 | 5 | 4 |
| g17 character select | – | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| g18 end credits | – | 5 | 5 | 5 | 5 | 5 | 4 | 5 |

**Weakest shot:** g14 — the rhythm lane reads as a game, but the falling notes are small at 360 px. With more
time: bigger ball-notes and a short lane glow on each hit.

## Rendered file (`final_reel.mp4`, `--quality delivery --sdr --strict`, exit 0)
- 1080×1920, 30 fps, 6,562 frames, H.264 + AAC, 218.733 s, 187.9 MB.
- Final mix: **−14.5 LUFS** integrated, LRA 3.1 LU, sample peak **−1.0 dBFS**.
- Black frames: per-frame luma scan finds **no one-frame dips** (min YAVG 40.5: the dark game screens).
- A/V: rendered audio vs `dialogue.wav` cross-correlation lag 0 ms at 30, 100, 150 and 200 s.
- Decoded frames checked at 25 key times (opening tag, every `cw` flash, fog reveal, title, radar photo, aim
  assist, LAG, the touch flash and toast, wrong answer, stadium, rhythm, idle, «عبقرية», achievement, select,
  credits): all screens render as snapshotted, Arabic shaping and dots intact, no stale frames.
- Cover: `cover.png` (g3 title screen with the P1 portrait, 26.3 s).
