# Director's prompt — «ميسي: اللاعب رقم 1»: the Messi reel re-made as a video game (HyperFrames)

> A new visual concept for the **same recorded Messi video**. It reuses the finished cut of
> `hyperframes-messi-edit/` (the best takes, the silence removal, the hidden script-reading
> leans, the audio mix, the word timing, the photos, the SFX and the Chawali clip) and replaces
> the paper-notebook graphics with an original pixel-art video-game world.
> An Egyptian-Arabic copy is in `PROMPT_MESSI_GAME_AR.md`. Paste everything below the line as one message.

---

You are the **director, senior Arabic short-form editor, motion designer, and HyperFrames implementer** of a new version of an existing reel. The subject is **Lionel Messi** and how his mind reads the game before it happens. The new idea: **the whole reel is a video game, and Messi is Player 1.** The speaker's script is full of game words — «كمبيوتر», «ماتريكس», «متأخر بخطوة», «فيديو جيم», «NPCs» — so instead of being a metaphor only in the last line, the game becomes the reel's whole world from the first cut. Every cut, screen, word, and sprite must have a reason you can say in one sentence.

**Do not re-edit the speech.** The cut is finished and approved. You are re-designing everything that sits on top of it.

Inspect, plan, design, animate, validate, self-review, preview, and render a premium Arabic 9:16 reel with **HyperFrames as the primary and final system**. Build the complete working project — not recommendations or snippets. **Stop only once**, at the Studio-preview approval gate, before rendering.

---

## 0. What you start from

In this repository, `hyperframes-messi-edit/` is the finished "Engineer's Notebook" version (218.733 s). Read its `REVIEW.md`, `DIRECTOR_NOTES.md`, `FACT_CHECK.md`, `tools/plan.py`, and `tools/build.py` first.

1. Create a new sibling folder `hyperframes-messi-game/` by copying `hyperframes-messi-edit/` **without** `node_modules/`, `snapshots/`, `final_reel.mp4`, and `render.log`, then `npm i`. Never modify `hyperframes-messi-edit/` — the notebook version must stay renderable.
2. Media lives outside git (`assets/media/` is gitignored). If `hyperframes-messi-edit/assets/media/aroll_edit.mp4` and `dialogue.wav` exist, copy them. If they do not exist, rebuild them with the existing pipeline (`python3 -I tools/cut.py && python3 -I tools/audio.py && python3 -I tools/aroll_edit.py`) from the raw video in `source/`; if the raw video is missing too, that is a blocker (§14).
3. **Keep unchanged:** `aroll_edit.mp4` (the single baked presenter clip — it avoids the renderer's first-frame drop), `dialogue.wav`, `timing-map.json`, `transcript.json`, the word ids, `plan.FREEZE` / `plan.TRIM`, the caption groups in `plan.CAPTIONS` (re-style them, don't re-group unless a group breaks the new layout), the SFX placements in `plan.SFX`, the closing Chawali clip, and the eight photos in `assets/photos/`.
4. **Replace:** every template in `tools/scenes/`, the art direction, the caption style, the opening push treatment if needed, and `cover.png`. Keep the build pipeline (`tools/build.py` renders `plan.SCENES` from `tools/scenes/*.html` with `{{ID}}`, `{{w:N}}`, `{{D}}` placeholders and the `rise` / `bin` / `pop` / `fade` / `tl` helpers); extend the helpers if the game needs new ones (e.g. `type` for a dialog box, `step` for frame-stepped sprite motion).
5. Rebuild with `python3 -I tools/cut.py && python3 -I tools/audio.py && python3 -I tools/build.py && python3 -I tools/aroll_edit.py && python3 -I tools/make_srt.py`.

## 1. The script-reading leans — the one rule you must not break

The speaker sometimes leans to read the script and comes back. In the finished cut **every lean is hidden under a full-screen page**, and the presenter windows between them were checked frame by frame with a face tracker. So:

- **Every full-screen window below must stay full-screen** (a game screen that hides the presenter completely). You may start a window earlier or end it later; **never shorten it, never make it a partial overlay, and never show the presenter through it.** If you move a boundary, re-run the face-tracker check (`mediapipe` FaceLandmarker: nose left of median − 0.09 plus head down, or no face) on the rebuilt `aroll_edit.mp4` and look at contact sheets of every new presenter frame.
- The three overlays (`o0`, `o1`, `o2`) do **not** cover the presenter; keep them as small cards beside him.
- The windows (output seconds, current `index.html`):

| id | window (s) | spoken words under it |
| --- | --- | --- |
| g1 | 1.567–8.733 | «لاعب كرة قدم بيبص في حتة وبيباصي الكورة للاعب تاني موجود في حتة تانية. لاعب» |
| g2 | 11.833–15.100 | «في الحقيقة هو قاعد بيرسم خريطة في دماغه» |
| g3 | 20.500–26.467 | «ودي اسمها هندسة الماتريكس العقلية ليونيل ميسي.» |
| g4 | 32.067–41.600 | «واكتشفوا مصطلح غريب اسمه الماسح الضوئي. ميسي من أكتر اللعيبة اللي بتعمل اسكان للملعب وهو بيتحرك.» |
| g5 | 45.067–52.967 | «عقل ميسي بيكون على حسب سرعة اللاعب اللي قدامه ومكانة مركزه. والزاوية اللي بين رجلين الحارس.» |
| g6 | 54.733–64.733 | «هو بيبقى عارف هو هيعمل بيها إيه. وهيباصيها فين وهيتحرك فين. يعني شايف المستقبل زي ما بنقول كده قبل ما يحصل. عارفين» |
| g7 | 68.200–72.400 | «عارف بينفذ خطة هندسية رسمها في دماغه تعال أقولك» |
| g8 | 74.600–83.933 | «المدافع العادي بيشوف الحركة وبعدين عقله بيبعت إشارة للعضلة علشان تتحرك وتنفذ أمر.» |
| cw1 | 88.800–89.533 | «ينفذها. بس» |
| cw2 | 91.733–92.300 | «خالص بالنسبة» |
| cw3 | 96.033–96.433 | «ميسي» |
| cw4 | 99.867–100.533 | «يحصل. وقبل» |
| g9 | 102.933–109.733 | «هو عارف إن ميسي لو عمل بكتفه يمين عارف إن اللاعب هيروح ناحية الشمال بنسبة تسعة وتسعين في المية.» |
| cw5 | 111.500–111.833 | «ميسي» |
| g10 | 116.000–123.167 | «المدافع بيعمل زي الآلة المكسورة اللي بيحاول يلحق ميسي. دايماً بيكون متأخر بخطوة. المدافع» |
| cw6 | 127.567–128.367 | «المدافع» |
| g11 | 130.667–135.100 | «ميسي بيمشي ببطء. بيخلي المدافع يقرب منه. وبيحس بالأمان.» |
| g12 | 138.733–144.900 | «لكن في تتش سريع جداً. ميسي كل لمس الكورة بعد ما اداله الأمان تماماً.» |
| gp | 155.700–157.967 | «عشان يفترسه.» |
| g13 | 157.967–166.100 | «لا ده كأنه بيكتب معادلة هندسية ماتريكس على سبورة وبيعلمها لكل اللي في الاستاد.» |
| g14 | 168.033–177.633 | «الكورة في رجل ميسي هندسة وموسيقى وهو العازف الوحيد اللي في الملعب كله بيعزف هذه الموسيقى بالكورة. لعيبة» |
| g15 | 183.967–188.833 | «وكأن الكورة بتنام في رجله وبتسمع كلامه.» |
| g16 | 200.533–204.467 | «ميسي هو مؤسس هندسة الماتريكس في الملعب. شاركنا» |
| g17 | 205.267–212.100 | «أكتر لحظة حسيت فيها إن ميسي بيلعب فيديو جيم والناس كلها. NPCs.» |
| g18 | 212.100–218.733 | Chawali clip (no presenter voice) |

The `cw*` windows are 0.33–0.8 s: they are **game flash cards** — one word, one sprite, instantly readable.

**The audio wins over any written script.** On screen, show what was actually said (e.g. «شايف المستقبل», not «شاف المستقبل»; there is no «البوم» in this recording). The earlier written script is not a source for on-screen text.

## 2. The idea and the quality bar

**Concept — "Player 1" (اللاعب رقم 1):** an original pixel-art football game seen from above, with a game HUD. Messi is **P1**; defenders are **NPCs** running slow, predictable scripts. His scan is the game's radar; "seeing the future" is the aim-assist trajectory that appears before the move; the late defender is **LAG**; the decisive touch is the moment the NPC's script breaks. The reel's last line («بيلعب فيديو جيم والناس كلها NPCs») becomes the payoff of a world the viewer has been inside the whole time.

**Semantic colour code — the same in every screen, so the viewer learns it:**

| Role | Colour | Drawn as |
| --- | --- | --- |
| Messi / P1 (his sprite, his path, his input) | P1 orange `--p1` | a solid pixel sprite with a small **10**, a «P1» tag above it, crisp step motion |
| NPCs / defenders / the ordinary player | NPC grey `--npc` | grey sprites, «NPC» tags, heavier and later motion |
| The future / scan / prediction | cyan `--future` | **dashed** pixel paths, ghost sprites one step ahead, radar sweeps |
| Genius / achievements / the 10 | gold `--gold` | achievement toasts, the underline under «عبقرية», the final screen |
| Lag / error (defender only) | red `--alert` | the «LAG» tag and the stuttering bar — nowhere else |

**Quality bar:** a polished indie game trailer on a phone. Face at frame 0, a fast push, a hard cut into the first game screen, the presenter for credibility, game screens that assemble exactly on the spoken word, one unforgettable hero sequence (g11 → g12), the payoff on the face, a character-select comment card, and the commentator's verse as the end-credits screen. Clean, readable with the sound off, never noisy.

## 3. Rights and truth guard (non-negotiable)

- **Original game only.** No real game's HUD, menus, fonts, sprites, sounds, or logos — not EA SPORTS FC/FIFA, eFootball/PES, Football Manager, Nintendo, Sega, or any arcade classic. No famous sprite silhouettes, no coin/power-up/jump sounds from known games. "Matrix" is the speaker's metaphor: no green falling code, no film typography.
- **No likeness of Messi or any real person generated or drawn**: the P1 sprite is a generic figure in P1 orange with a «10»; never a pixel portrait of his face. Real imagery only from the eight photos (§7). No club or national kits recreated on sprites, no crests, federation/league logos, sponsor marks, or trophy replicas.
- **Numbers on screen are only the speaker's numbers**: «80٪», «3–4 أعشار الثانية» (shown as «0.3–0.4 ث»), «99٪» (rhetoric), «بثانية» (shown as «+1 ث»). **No fake score, XP value, rating, level number, stat, or ranking.** Bars and meters carry no numbers. Keep `FACT_CHECK.md` from the notebook version and add a line for any new on-screen text.
- «خبراء كتير بيقولوا…» stays on the presenter's face — no fake study, paper, or chart.
- Audio: no music, no commentary except the closing Chawali clip (once, at the very end, never under the voice). Game UI blips may be **synthesized locally** (`ffmpeg -f lavfi aevalsrc` / `sine` with short envelopes) or taken from bundled `/media-use` SFX — short single blips, never a melody or chiptune bed. Log their provenance in `.media/manifest.jsonl`.

## 4. Art direction

```css
--bg:#0E1424;      --bg-2:#162036;     --grid:#22304D;        /* night screen, pixel grid */
--pitch:#1E5A36;   --pitch-2:#246B40;  --line:#D9F2E4;        /* pixel pitch stripes + lines */
--p1:#FF7A1A;      --p1-dark:#C2540A;                          /* Messi / P1 */
--npc:#8A93A8;     --npc-dark:#4A5268;                         /* defenders / NPCs */
--future:#46D7FF;  --future-dark:#1B8FB3;                      /* scan / prediction (dashed) */
--gold:#FFC845;                                                /* achievements, «عبقرية» */
--alert:#FF4D5E;                                               /* lag/error on the defender only */
--text:#FFF6E5;    --text-dim:#AEB7C9;
```

- **Pixel grammar:** build sprites, HUD frames, and pitch tiles as SVG `<rect>`s on an 8 px grid (135 × 240 cells on the 1080 × 1920 canvas) with `shape-rendering:crispEdges`; scale raster art with `image-rendering:pixelated`. Integer positions only. Hard 4–8 px stepped shadows, no blur, no gradients except a very faint screen vignette.
- **Motion feels like a game:** sprites move in **steps** (GSAP `steps(n)` or snapping to the 8 px grid at 12–15 sprite fps), while HUD text and cuts stay at 30 fps. P1 steps are quick and early; NPC steps are slower and late.
- **HUD kit (designed once, reused everywhere):** dialog box (pixel border, `--bg-2` fill) for the Arabic hero phrase; small tags (`P1`, `NPC`, `LAG`); a radar/minimap; a dashed aim trajectory; a progress bar without numbers; an achievement toast (gold border, small icon, Arabic title); a "character-select" grid.
- Optional, subtle: a 2–3 % opacity scanline texture on game screens only. No CRT bulge, no chromatic aberration, no noise, no screen shake except one 3–4 frame nudge on the g12 hit.
- Avoid: neon glow, sci-fi HUD clutter, 3D, glossy, particles, rainbow palettes, more than one HUD element animating at once.

## 5. Typography and bidi

- Arabic: **Cairo** (already in `assets/fonts/`, OFL), weights 900 hero / 800 captions / 700 labels. Arabic is **never** faked into a pixel font and **never split into letters**; it gets the game look from the pixel dialog box and a hard stepped shadow.
- Latin HUD tokens (`P1`, `NPC`, `LAG`, `LOADING`, `LEVEL UP`, `PRESS START`): an OFL pixel font — install `@fontsource/press-start-2p` (or `@fontsource/silkscreen`), copy the woff2 into `assets/fonts/`, declare `@font-face` in every file that uses it. Latin tokens are small accents; the Arabic phrase is always the dominant word. Wrap every Latin token and numeral in `<bdi>`.
- Reveal masks keep room for Arabic dots: ≈0.2em top / 0.36em bottom padding with matching negative margins. `dir="rtl"`, whole-word spans, Western digits (`80٪`, `0.3–0.4 ث`, `99٪`, `10`, `+1 ث`).
- «يمين» / «شمال» are drawn from the **viewer's** point of view; check every arrow against its word.
- "Typing" dialog text is revealed **word by word**, never letter by letter.

## 6. Storyboard — every screen on the real words

Write the final plan to `DIRECTOR_NOTES.md` and `STORYBOARD.md`. **A** = presenter, **G** = full-screen game screen. Hard cuts on spoken words, as in the current cut. You may change the treatment inside a window freely; the windows themselves follow §1.

| id | Screen | Treatment | Energy |
| --- | --- | --- | --- |
| A 0–1.57 | Opening | Frame 0 = face. Push 1.00 → 1.12 in 0.55–0.85 s, `expo.out`. On the push a tiny «P1» pixel tag snaps in above his head (inside the safe zone, off his face) and disappears on the cut. First caption «تخيل». | 3 |
| g1 | **No-look pass** | Top-down pixel pitch. P1 sprite; on «بيبص في حتة» a cyan dashed vision cone opens one way; on «بيباصي الكورة» the ball travels in pixel steps the other way to a teammate sprite. Dialog box: «بيبص في حتة… وبيباصي في حتة تانية». A small gold toast on the pass: «باصة من غير ما يبص». | 4 |
| A + o0 | «بيقعد يتمشى 80 % في الماتش» | o0 = `p1-walking` as a **player card** (pixel frame, «P1» tag, «80٪») beside the presenter, ≤ 35 % width, 1.0 s. | 3 |
| g2 | **Fog of war** | A minimap fully dark; on «بيرسم خريطة» tiles reveal outward from P1 until the whole pitch is mapped. Hero «بيرسم خريطة في دماغه». | 3 |
| A | «ده عقل بيشتغل بسرعة الكمبيوتر» | Caption highlight «بسرعة الكمبيوتر» (P1 orange). | 3 |
| g3 | **Title screen** | The game's title «هندسة الماتريكس» in a big pixel-framed logo, «ليونيل ميسي» under it, `p2-portrait` as the P1 character portrait (§7 treatment) in a pixel frame. A short «PRESS START» blink (finite, 2 blinks) ends on the cut. This is `cover.png`. | 4 |
| A + o1 | «العلماء… قعدوا يدرسوا عقلية ميسي» | o1 = `p4-study` as a small "scouting" card with a grey bracket and the label «ميسي». | 3 |
| g4 | **Radar** | `p3-scan` appears for ≈1.2 s with cyan sweeps from his eyes, then shrinks into the P1 sprite at the centre of a radar; sweeps reveal NPC blips one by one (no counts). Hero «الماسح الضوئي», support «اسكان للملعب». | 4 |
| A | «الاسكان ده وهو لسه كورة في رجل زميله» | Face. | 3 |
| g5 | **Target lock ×3** | Three lock-on brackets snap on their words: «سرعة اللاعب» (a speed arrow on an NPC), «مكانة مركزه» (a position pin), «الزاوية اللي بين رجلين الحارس» (a goalkeeper sprite, a cyan angle drawn between the legs). Meters without numbers. | 4 |
| g6 | **Aim assist — the future** | A cyan dashed trajectory draws the pass and the run **before** P1 moves («هيباصيها فين وهيتحرك فين»), with a ghost P1 one step ahead tagged «+1 ث»; then P1 follows the ghost exactly. Hero «شايف المستقبل». | 4 |
| A | «ده معناه إيه إن ميسي مش بيبتكر الكورة في لحظتها» | Close crop, hold — earned stillness. | 3 |
| g7 | **Plan loaded → executed** | A move list of pixel arrows («خطة هندسية») fills in, then P1 executes it step by step on the pitch; the last arrow lights as the plan completes. Holds over «تعال أقولك». | 4 |
| A | «على سر مرعب. علمياً» | Keep the pause after «مرعب». | 4 |
| g8 | **NPC processing** | Grey pipeline: eye → head → leg muscle, each node turns on with its word («بيشوف» / «إشارة» / «تتحرك»), a «LOADING» bar crawls (no number). All grey, slower than anything P1 does. | 3 |
| A + o2 | «الحركة دي بتحتاج من 3 إلى 4 عشار من الثانية» | o2 = a small timer card «0.3–0.4 ث» with the grey loading bar. | 3 |
| cw1 | Flash | «عشان ينفذها» — the grey bar finally completes on an NPC. | 4 |
| cw2 | Flash | «أي حاجة خالص» — an empty bar beside P1. | 4 |
| cw3 | Flash | «ميسي» — the P1 sprite with its tag, big. | 4 |
| cw4 | Flash | «قبل ما يحصل» — a cyan ghost sprite ahead of P1. | 4 |
| g9 | **Programming the NPC** | Duel: on «بكتفه يمين» a P1 shoulder input arrow to the viewer's right; the NPC's script line (cyan dashed) to the left is drawn **before** he moves, then he follows it. «99٪» as a big rhetoric numeral in the dialog box (no "accuracy" label). | 4 |
| cw5 | Flash | «ميسي» — P1 sprite. | 4 |
| A | «عايش في المستقبل…» | Thesis on the face, cyan highlight on «المستقبل» only. | 5 |
| g10 | **LAG** (signature ②) | P1 moves smoothly; the NPC stutters with 2–3 ghost copies a step behind, a red «LAG» tag, a connection meter dropping (no numbers). The reel's only glitch effect. Hero «متأخر بخطوة». | 4 |
| cw6 | Flash | «المدافع» — the NPC sprite with its grey tag. | 4 |
| g11 | **The trap** (hero part 1) | `p5-trap` for 1.0 s, then the same scene as pixels: P1 walks in slow steps, the NPC closes in, a calm cyan circle «منطقة الأمان» forms. Heartbeat SFX under it (already placed). | 4 |
| A | «وفي لحظة المدافع بيمد رجله…» | Tension on the face, close crop, no movement. | 5 |
| g12 | **The touch** (signature ③) | Same scene continues (shared elements): the NPC's leg extends; on «تتش» a tiny P1 touch arrow; one frozen beat; then the impact (already placed): `p6-dribble` flashes 0.5–0.7 s, the safe circle breaks into pixels, the NPC tumbles off the screen edge in steps, gold toast «تتش». | 5 |
| A | «…سابق عقلية المدافع بثانية…» | Face. | 4 |
| gp | **Wrong answer** | «يفترسه» in the dialog box, struck through by a red pixel X — the speaker immediately rejects the idea. | 4 |
| g13 | **The equation** | A pixel blackboard: P1's dribble path writes itself as an equation stroke by stroke, NPCs as terms; pixel crowd in the stands lights row by row on «لكل اللي في الاستاد». | 4 |
| g14 | **Rhythm lane** | A five-lane rhythm track; balls arrive as notes; P1 hits each one exactly on the line; on «العازف الوحيد» one orange note rises above the track. Hero «العازف الوحيد». | 3 |
| A | «…التاريخ بيفتكر…» | Face. | 3 |
| g15 | **Idle** | The quietest screen: P1 standing, the ball resting at his foot with a small «z z» idle animation; `p7-ball` for 1.2 s. Hero «الكورة بتنام في رجله». | 3 |
| A | «ميسي دي عبقرية اتولدت في جسم إنسان…» | Payoff on the face, longest crop hold; «عبقرية» gold-underlined (the only gold caption). No HUD. | 5 |
| g16 | **Achievement unlocked** | A large gold toast «مؤسس هندسة الماتريكس» with a pixel star badge (no trophy shape). | 4 |
| A | «في الكومنتات.» | Face. | 4 |
| g17 | **Character select** | A select screen: the P1 slot filled, a row of grey «NPC» slots with «؟»; prompt «اكتب في الكومنتات: كانت ضد مين؟». Holds ≈0.5 s fully built, hard cut to g18. | 4 |
| g18 | **End credits** | Chawali clip plays in full. `p8-celebration` (§7 treatment) rises in on the first word; the verse sets as two lines on their words — «بلغة الغناء أنت **موّال**» / «وبلغة الشعر أنت **قافية**» (rhyme words orange); «— عصام الشوالي» small; a gold pixel rule under «قافية». The CTA stays as one small line. Hold ≥ 0.6 s after the clip. No black ending, no reset tail. | 5 |

Keep at least one or two presenter sections with **no HUD at all** — the face carries the credibility.

## 7. Photos — game cards, short, the presenter stays the star

Same files, same scenes, same limits as the notebook version: each 0.8–1.2 s (the g12 flash 0.5–0.7 s), ≤ ≈8 % of the reel, never in the first 2 s, never on «عايش في المستقبل» or «عبقرية», never covering the presenter's face or hands, never mirrored, one at a time. `p1`→o0, `p2`→g3, `p3`→g4, `p4`→o1, `p5`→g11, `p6`→g12, `p7`→g15, `p8`→g18.

**New treatment:** load `/media-use` and follow its `references/media-treatments.md`. A limited-palette ordered-dither look (downsample to ≈240 px wide, 5–6 colours from §4, nearest-neighbour upscale) inside a pixel card frame with a small tag. He must stay recognisable; never alter his face or body. Keep `CREDITS.txt` («صور ميسي: Wikimedia Commons», authors not verified).

## 8. Captions (presenter sections only)

- Keep the existing groups and word timing. New style: Cairo 800, `--text`, not-yet-spoken words at ≈50 %, **one** highlighted word per group in P1 orange (cyan only for «المستقبل», gold only for «عبقرية»), a hard 4 px stepped shadow in `--bg` plus a feathered shadow if contrast drops below 3:1.
- Position ≈61–68 % of frame height, over the torso, never over the face at any crop.
- 2–3 frame pop-in, or a clean hard replacement. No bouncing karaoke, no letter animation.

## 9. Sound

- Dialogue and the existing mix stay (≈ −14.5 LUFS, ≤ −1 dBTP). Keep all `plan.SFX` placements.
- Add at most a few UI blips (§3): a soft blip when a dialog box appears (not every one), a short rising blip on achievement toasts (g1, g12, g16), a low buzz under the g10 «LAG» tag (≤ 0.6 s), a select blip on g17. Each ≥ 8 dB under the voice, never on the onset of a highlighted word, never two at once except the g12 stack.
- Re-measure the final mix and list every added sound with its time and level in `REVIEW.md`.

## 10. Implementation contract

- 1080×1920, 30 fps, H.264 + AAC MP4; root duration stays 218.733 s unless §1 forces a change.
- One sub-composition per screen; `class="clip"`; never animate `display` / `visibility` / `autoAlpha` on a `.clip`; scene-unique ids for every GSAP selector.
- Seek-safe: one paused GSAP timeline per composition on `window.__timelines`, `fromTo` everywhere, no `Date.now()`, `performance.now()`, unseeded `Math.random()`, timers, or `repeat:-1` (blinks and loops are finite and explicit).
- The first frame of every screen already shows the scene (no empty frame on a hard cut).
- Safe zones: essential text within x 80–1000, y 140–1650, and inside the platform clear band `check` uses (≈ y 290–1250, x 120–888) wherever possible.
- No render-time network: GSAP from `assets/vendor/`, fonts and media in `assets/`.

## 11. Verification and the director's review loop

1. `npx hyperframes lint`, then `npx hyperframes check --json` until **0 errors**; justify every kept warning.
2. Re-run the lean check (§1) if any boundary moved; otherwise confirm in `REVIEW.md` that every window in §1 is still a full-screen cover.
3. Snapshots: frame 0 and the push; every hard cut ±1 frame; first frame, midpoint, and final state of every screen; each `cw` flash; g10 lag; g12 before/at/after the touch; g17 hold and the cut to g18; each verse line on its word; the final frame. Then `npx hyperframes snapshot --review` (seams + 360 px phone sheets).
4. **Score every screen 1–5** in `REVIEW.md` on Hook, Clarity (one focal sprite, one dominant Arabic phrase, readable at 360 px), Mute test, Sync (±2 frames), Colour code (orange P1, grey NPC, dashed cyan future, red only for lag), Truth (no fake numbers, no real game's look, no likeness), Craft (crisp pixels, Arabic shaping and dots, bidi, arrows match يمين/شمال, no flashes, no reset tails), Rhythm (g12 feels like the peak). Fix anything below 4; do at least one full revision pass; name the weakest shot.
5. `npx hyperframes preview --background`, confirm 200, give me the **preview URL**, the scores, and any open fact or rights item. **Wait for approval.** This is the only pause.
6. After approval: `npx hyperframes render --quality delivery --fps 30 --sdr --format mp4 --strict -o final_reel.mp4`; export `cover.png` from g3. Verify with ffprobe, ebur128, a per-frame luma dip scan for black flashes, A/V sync against `assets/media/dialogue.wav`, and contact sheets at every `cw` window.

## 12. Delivery report

`final_reel.mp4`, `cover.png`, `CREDITS.txt`, `captions.srt`, and a short report: what changed from the notebook version, number of screens, the hero moment, fonts (and how the pixel font was obtained), added sounds and their provenance, director's scores after revision, validation status, kept warnings, and confirmation that every lean window is still covered.

## 13. Commit

Commit the new project (no media, no `node_modules`) on the working branch and push. Commit messages never include a model name.

## 14. Stop and report — never pretend success

Stop with a concrete blocker if: the finished cut or its media cannot be found or rebuilt; a lean window cannot stay covered; no font shapes Arabic correctly; HyperFrames cannot run; a beat can only be shown with a fake number, a real game's look, or a real likeness; `check` still reports an unresolved error.
