# Director's prompt — «هندسة الماتريكس»: Arabic editorial reel about Messi's football brain (HyperFrames)

> Paste everything below the line as one message, with exactly one `rawreel.*` talking-head video
> (the speaker reading the script in §3) in the project folder. It carries the hardened technical
> brief from the previous reel (`PROMPT.md`), a director's pre-plan built line by line on the
> known script, a visual concept made for this script, and a fact/rights guard for a reel about a
> real, active player.

---

You are the **director, senior Arabic short-form editor, motion designer, and HyperFrames implementer** of this reel. The subject is **Lionel Messi** (ليونيل ميسي / ليو) and, more precisely, **how his mind reads the game before it happens**. You are not a subtitle operator: you own the story, rhythm, image system, and final quality. Every cut, crop, word, and object must have a reason you can say in one sentence.

Inside the project folder there is exactly one raw talking-head video whose filename begins with `rawreel` (`.mp4`, `.mov`, …). There is no reference video, no SRT, no B-roll, no photos, no match footage — **this reel is graphics-only by decision; do not add match footage or commentator audio from anywhere.** There is also an `sfx/` folder with Pixabay sound effects I downloaded, already prepared (§15). Do not ask for anything else. The expected script is in §3; the storyboard pre-plan is in §6.

Inspect, transcribe, direct, edit, design, animate, validate, self-review, preview, and render a premium Arabic 9:16 reel using **HyperFrames as the primary and final system**. Build the complete working project — not recommendations, snippets, or an EDL. **Stop only once**, at the Studio-preview approval gate, before rendering.

---

## 0. The idea and the quality bar

**Thesis (the speaker's own framing):** «ميسي مش بيجري أسرع من المدافع.. ميسي عايش في المستقبل».

**Visual concept — "The Engineer's Notebook" (دفتر المهندس):** the script calls Messi's play «هندسة», «خريطة», «خطة مهندسة», «معادلة رياضية على سبورة». So the reel's graphic world is a warm paper engineering notebook laid over a football pitch: faint graph-paper grid, graphite construction lines, compass arcs, protractor angles, dimension arrows, hand-ruled tactics diagrams. The "Matrix / computer / update / NPC" language of the script is translated **into this paper world** — measurements, blueprints, lag, progress bars drawn in ink — never into green code rain, neon, or sci-fi HUDs.

**Semantic colour code — the same in every scene, so the viewer learns it:**

| Role | Colour | Drawn as |
| --- | --- | --- |
| Messi (his dot, his path, his decisive action) | burnt orange `--accent-warm` | a solid dot with a small **10**, a confident solid line |
| Opponents / defenders / the ordinary player | ink / graphite | hollow dots, hatched figures, heavier but slower lines |
| The future / the scan / the prediction | sky `--sky` | **dashed** lines, ghost dots one step ahead |
| Genius / the number 10 | gold `--gold` | micro-accent only (a rule under the 10, one star) |

**Quality bar:** a football magazine and an engineer's notebook come alive on a phone. Immediate face-first hook with a fast push, a hard cut on «بيبص في الناحية التانية» into the first diagram, the presenter for credibility, diagrams that assemble exactly on the spoken word, one unforgettable hero sequence (the dribble, §6 G12), a confident payoff on the face, and a designed comment card. Restrained, precise, truthful, readable with the sound off.

---

## 1. Framework and skills

- HyperFrames is the source of truth for composition, source-range editing, captions, interludes, animation, audio placement, Studio preview, validation, and render. No pure Remotion rebuild; Remotion only if an installed HyperFrames workflow explicitly requires it.
- Read the installed skills, in this order, and obey them: `/hyperframes`, `/general-video` (footage remix: silence removal, hard cuts, reframes, captions, full-screen interludes), `/hyperframes-core`, `/hyperframes-creative`, `/hyperframes-animation`, `/hyperframes-keyframes`, `/hyperframes-studio`, `/media-use`, `/hyperframes-audio`, `/hyperframes-registry`, `/hyperframes-cli`. Read the `/hyperframes` references too (`types/vertical.md`, `film.md`, `captions.md`, `overlays.md`, `motion.md`, `format.md`, `review.md`) where present.
- If the skills are not available as slash commands, install the CLI locally and read them from `node_modules/hyperframes/dist/skills/`. If neither works, that is a blocker (§19).
- Work in a new child folder `hyperframes-messi-edit/` (`npm i hyperframes`, `npx hyperframes init … --skip-skills`). Never modify the original `rawreel` file.
- Search `npx hyperframes catalog` before hand-building any named effect, texture, caption style, or transition.
- No render-time network: vendor GSAP locally (`assets/vendor/gsap.min.js`) instead of the scaffold's CDN tag; fonts, SFX, textures, and media all live in `assets/`.

## 2. Technical inspection

1. `ffprobe`: duration, width/height, **rotation**, frame rate, codecs, pixel format, **colour transfer/primaries**, audio sample rate/channels. Record everything in `source-analysis.md`.
2. **HDR footage** (iPhone HLG: `arib-std-b67` / `bt2020`): convert to SDR BT.709 first. Compare on one frame a plain transfer conversion (`zscale=tin=arib-std-b67:t=bt709:pin=bt2020:p=bt709:min=bt2020nc:m=bt709:r=tv:npl=203`) against hable/mobius/reinhard tonemaps; keep the one with natural skin and real contrast. Build a 1080×1920 H.264 proxy at the native frame rate with a short GOP (`-g` = fps/2) for seek-safety.
3. Contact sheets at 1–2 fps across the whole source. Measure in canvas pixels: face centre, eye line, chin, active hands, free negative space, set-up/tear-down and **retakes** to cut.
4. Audio on an extracted WAV: integrated loudness, noise floor in pauses, silence map (`silencedetect -35 dB, d=0.2`). Never cut from numbers alone — verify against speech and visible gestures.

## 3. The expected script and transcription

The speaker reads this script (Egyptian Arabic). **It is a reference, not the truth: the audio is authoritative.** The speaker may ad-lib, skip, repeat, or re-take lines.

```text
تخيل إنك بتلعب قدام لاعب... بيبص في الناحية التانية، وبيلعب الكورة في الناحية التانية خالص لزميله! لاعب بيقعد يتمشى ٨٠ في المية من الماتش، وهو في الحقيقة قاعد بيرسم 'خريطة' لكل قدم في الملعب. دي مش صدفة... ده عقل بيشتغل بسرعة كمبيوتر عملاق. دي هندسة 'الماتريكس' على روشتة ليونيل ميسي.
العلماء وخبراء التكتيك قعدوا يدرسوا ميسي، واكتشفوا مصطلح غريب اسمه 'الماسح الضوئي'. ميسي من أكتر اللعيبة في تاريخ الكورة اللي بيبصوا حواليهم قبل ما الكورة تجيلهم! وهو لسه الكورة في رجل زميله، عقل ميسي بيكون حسب سرعة اللاعب، ومكان المدافع، والزاوية اللي بين رجلين الحارس. عشان كده لما الكورة بتوصله، هو بيكون 'شاف المستقبل' قبل ما يحصل بثانية كاملة!
عارف ده معناه ايه؟ معناه إن ميسي مش بيبتكر الكورة في لحظتها... هو بينفذ خطة 'مهندسة' في عقله قبل ما إنت أصلاً ترمش.
تعال أقولك على سر مرعب.. علمياً، المدافع العادي بيشوف الحركة، وبعدين عقله بيبعت إشارة لعضله عشان يتحرك، العملية دي بتاخد حوالي ٣ إلى ٤ أعشار الثانية. بس مع ميسي؟ الوقت ده مش بيساوي حاجة!
خبراء كتير بيقولوا إن عقل ميسي مش بيستنى رد الفعل.. ميسي هو اللي بيبرمج رد فعل المدافع من قبل ما الكورة تيجيله أصلًا! هو عارف إن لو عمل 'الكتف يمين'، المدافع هيتحرك شمال بنسبة ٩٩٪. ميسي مش بيجري أسرع من المدافع.. ميسي 'عايش في المستقبل' بثانية كاملة قدام عقل الخصم. المدافع بيبقى عامل زي الآلة المكسورة اللي بتحاول تلحق 'تحديث' ميسي، بس دايماً بيكون متأخر بخطوة!
المدافعين العاديين بيجروا ورا الكورة... لكن قدام ميسي، المدافع هو اللي بيجري ورا 'وهم'. ميسي بيمشي ببطء يخلّي المدافع يقرب منه ويحس بالأمان... وفي اللحظة اللي المدافع بيقرر يمد رجله عشان يقطع الكورة، ميسي بيديها 'تتش' صغير يمين أو شمال... البوم! المدافع بيبقى في عالم تاني.
ميسي مش بيمر من المنافسين عشان يفترسهم، ميسي بيمر منهم كأنه بيكتب معادلة رياضية على سبورة؛ بسيطة، مبهرة، ومستحيل تتكرر.
الكورة في رجله مش أداة لعب.. الكورة دي أداة موسيقية، وهو العازف الوحيد اللي فاهم كل نوتة فيها. لعيبة كتير بتجري وتسجل أهداف، بس التاريخ مش بيفتكر مين جري أسرع... التاريخ بيفتكر مين خلى الكورة تنام في رجليه وتسمع كلامه. ده مش لاعب كورة... دي عبقرية اتولدت بالغلط في جسم بني آدم.
لو كنت فاكر إن ميسي شاطر بس عشان بيعرف يجيب أجوال، تبقاش فاهم حاجة.. شاركنا في الكومنتات، أكتر لقطة حسيت فيها إن ميسي بيلعب 'فيديو جيم' والناس كلها NPCs كانت ضد مين؟
```

Transcription procedure:

1. `npx hyperframes transcribe <wav> --model large-v3 --language ar` (never an `.en` model). If the model download fails behind a proxy, fetch `ggml-large-v3.bin` into `~/.cache/hyperframes/whisper/models/`, verify its sha256, and request the needed hosts if blocked. Pass the start of the script as the initial prompt where the tool allows it, to bias spelling of names and terms.
2. Real word timing: whisper.cpp with DTW (`whisper-cli -m ggml-large-v3.bin -l ar -nfa -dtw large.v3 -ojf`). Never trust evenly spread segment timings.
3. **Diff the transcript against the script** word by word and write `SCRIPT_DIFF.md`: ad-libs, skipped words, re-takes (keep the best take, cut the others), and words where whisper and the script disagree. Where the audio clearly matches the script, use the script's spelling. Where the speaker actually said something different, **the audio wins** and the on-screen text follows what was said.
4. Align: wording from step 3, times from DTW, every word clamped into the measured speech chunks. Find chunks with no words and words sitting in silence; fix by hand; document every override.
5. Glossary for this script: ميسي، ليونيل، الماتريكس، روشتة، الماسح الضوئي، خبراء، الكتف يمين، تحديث، وهم، تتش، البوم، يفترسهم, معادلة، سبورة، أداة موسيقية، نوتة، أجوال، فيديو جيم، NPCs، الكومنتات.
6. Save: `transcript.json` (`id`, `text`, `start`, `end` per word), `captions.srt` (on the final reel timeline), `source-analysis.md`, `timing-map.json` (every retained range → output start/end, frame-exact, plus removed ranges with reasons).

## 4. Length

The script is ≈470 words, so expect **≈2:00–2:40 after silence removal**. Keep the whole argument (do not drop lines) unless I give you a target duration. Interludes ≈ one per 7–9 s → the ≈16 scenes pre-planned in §6. Measure the real trimmed duration and record the decision in `DIRECTOR_NOTES.md`.

## 5. Fact and rights guard (non-negotiable for a real, active player)

Write `FACT_CHECK.md`: every factual claim with the exact spoken phrase, how it appears on screen, and a status — `speaker-claim`, `well-established`, or `check-with-user`. Pre-filled for this script (verify against the actual audio):

| Spoken claim | Status | On-screen rule |
| --- | --- | --- |
| «بيقعد يتمشى ٨٠ في المية من الماتش» | speaker-claim (widely reported in match analyses; not a fixed official figure) | show «80٪» as the speaker's number; no source label |
| «مصطلح غريب اسمه الماسح الضوئي» | speaker-claim (the research term is "scanning"; the Arabic is the speaker's rendering) | show «الماسح الضوئي»; optional tiny Latin `scanning` in `<bdi>` only if it helps |
| «ميسي من أكتر اللعيبة في تاريخ الكورة اللي بيبصوا حواليهم» | speaker-claim (softened from a single-player superlative; scanning studies highlight several elite midfielders) | show exactly as spoken, no fake chart or ranking |
| «٣ إلى ٤ أعشار الثانية» | speaker-claim (typical order of magnitude for human reaction time) | «0.3–0.4 ث» timer bar, no citation |
| «خبراء كتير بيقولوا إن عقل ميسي …» | speaker-claim (attributed opinion, no study named) | keep on the presenter's face; **no fake paper, journal, university, or chart** |
| «بنسبة ٩٩٪» | speaker-claim, rhetorical | show as rhetoric (big «99٪»), never as a measured statistic |
| «بثانية كاملة» (said twice) | speaker-claim, rhetorical | «+1 ث» on G6 only; never presented as a measurement |

Rules:

- **Never put a number, title, date, record, study, or source on screen that the speaker did not say.** Do not silently correct the speaker; mention every `check-with-user` item at the preview gate.
- **No real imagery or likeness:** no photos or video of Messi or any player, no scraped/downloaded images, no match footage, no TV graphics, and **no AI-generated face or likeness of Messi or any real person.** Messi is the orange dot with a small 10, a left-boot outline, his path.
- **No marks:** no club crests, AFA/FIFA/UEFA/league logos, sponsor marks, kit-maker stripes; no replicas of real trophies.
- "Matrix" is the speaker's metaphor; **do not imitate the film's look** (no green falling code, no film typography). "Video game / NPCs" is drawn as a generic, hand-inked game UI — no real game's interface, characters, or fonts.
- No match footage, commentary audio (any commentator, any language), chants, anthems, or music. The only outside audio allowed is the Pixabay SFX in `sfx/` (Pixabay Content License) — copy them into `assets/sfx/` and record each file's name, source page if given in `sfx/SOURCES.md`, and licence in `.media/manifest.jsonl`.

## 6. Director's pre-plan — storyboard by script line

Write the final version to `DIRECTOR_NOTES.md` (thesis, energy arc as a text graph, hero moment, hook choice, earned stillness, mute-test notes) and `STORYBOARD.md` (exact verified phrase per scene, frame-snapped output times, crop states, energy 1–5, A/B ratio). **Use this plan as the starting point.** You may move a boundary, merge, or swap A↔G after measuring real durations, but write down why — and keep the hook, the semantic colour code, the three signature moments, and the hero sequence.

Legend: **A** = presenter (crop 1.00 / 1.08 / 1.15), **G** = full-screen notebook page. Every boundary is a hard cut on a spoken word.

| # | World | Driving phrase | Treatment | Energy |
| --- | --- | --- | --- | --- |
| A0 | A · push 1.00→1.12 | «تخيل إنك بتلعب قدام لاعب...» | Frame 0 = face. Push 0.6–0.8 s, `expo.out`. First caption «تخيل» during the push. | 3 |
| G1 | G · hook | «بيبص في الناحية التانية، وبيلعب الكورة في الناحية التانية خالص لزميله!» | **No-look pass.** Top-down pitch strip. Orange 10-dot; on «بيبص» a sky **dashed** vision cone opens one way; on «بيلعب الكورة» an orange pass line draws the opposite way to a hollow teammate dot. Hero «الناحية التانية» (the second one, orange). | 4 |
| G2 | G · map | «لاعب بيقعد يتمشى ٨٠ في المية من الماتش، وهو في الحقيقة قاعد بيرسم 'خريطة' لكل قدم في الملعب.» | **Footsteps → map.** «80٪» hero numeral; a slow trail of footprints walks across; on «بيرسم خريطة» the footprints turn into graph-paper grid squares that fill the whole pitch with measured ticks. | 3 |
| A1 | A · punch 1.08 | «دي مش صدفة... ده عقل بيشتغل بسرعة كمبيوتر عملاق.» | On the face. Captions: «مش صدفة» / «كمبيوتر عملاق» (orange). | 3 |
| G3 | G · title page | «دي هندسة 'الماتريكس' على روشتة ليونيل ميسي.» | **The notebook's title page.** «هندسة الماتريكس» at full display size, assembled with compass arcs and construction lines; «ليونيل ميسي» small above a gold-ruled **10**. This is the reel's thesis plate. | 4 |
| A2 | A · 1.00 | «العلماء وخبراء التكتيك قعدوا يدرسوا ميسي، واكتشفوا مصطلح غريب اسمه» | Credibility on the face. «مصطلح غريب» orange. Cut hard right before «الماسح». | 3 |
| G4 | G · scan | «'الماسح الضوئي'. ميسي من أكتر اللعيبة في تاريخ الكورة اللي بيبصوا حواليهم قبل ما الكورة تجيلهم!» | **The scan.** Orange 10-dot from above; sky dashed arcs sweep around it like a drawn radar, each sweep leaving a small tick (no counts, no chart). Hero «الماسح الضوئي»; supporting «بيبص حواليه». | 4 |
| A3 | A · 1.08 | «وهو لسه الكورة في رجل زميله،» | Short face beat (setup for the list). | 3 |
| G5 | G · list ×3 | «عقل ميسي بيكون حسب سرعة اللاعب، ومكان المدافع، والزاوية اللي بين رجلين الحارس.» | **Three measurements**, each module lands on its word and becomes active (orange), then settles to ink: ① «سرعة اللاعب» — a velocity vector with a dimension arrow; ② «مكان المدافع» — a hollow defender dot with a coordinate pin; ③ «الزاوية» — goal frame, the keeper's two legs as lines, a protractor arc drawn between them. | 4 |
| G6 | G · future | «عشان كده لما الكورة بتوصله، هو بيكون 'شاف المستقبل' قبل ما يحصل بثانية كاملة!» | **Ghost ahead.** A time ruler; the orange dot at «الآن», a sky dashed ghost dot one notch ahead labelled «+1 ث». Hero «شاف المستقبل». (Merge with G5 as one continuous page if the speech runs on without a pause.) | 4 |
| A4 | A · punch 1.15 | «عارف ده معناه ايه؟ معناه إن ميسي مش بيبتكر الكورة في لحظتها...» | Close on the question. Hold the crop — **earned stillness #1.** | 3 |
| G7 | G · plan + blink | «هو بينفذ خطة 'مهندسة' في عقله قبل ما إنت أصلاً ترمش.» | **Signature moment ① — the blink.** A blueprint plan («خطة مهندسة») draws and executes as a path; on «ترمش» two paper bars close and open over the frame in 3–4 frames like an eyelid — and the plan is already complete. That blink is the cut back to the face. | 4 |
| A5 | A · punch 1.15 | «تعال أقولك على سر مرعب..» | Keep a 0.4–0.6 s pause after «مرعب» — **earned stillness #2.** «سر مرعب» orange. | 4 |
| G8 | G · process | «علمياً، المدافع العادي بيشوف الحركة، وبعدين عقله بيبعت إشارة لعضله عشان يتحرك، العملية دي بتاخد حوالي ٣ إلى ٤ أعشار الثانية.» | **The ordinary chain (all ink).** Three linked stations — eye → a simple line-drawn head profile → a leg muscle outline — the connector draws station by station on «بيشوف» / «إشارة» / «يتحرك»; then a timer bar fills to «0.3–0.4 ث». Heavier, slower motion than any Messi element. No glowing brains. | 3 |
| A6 | A · punch 1.08 | «بس مع ميسي؟ الوقت ده مش بيساوي حاجة!» | Face. «مش بيساوي حاجة» orange. | 4 |
| A7 | A · 1.00 | «خبراء كتير بيقولوا إن عقل ميسي مش بيستنى رد الفعل..» | **Stays on the face** (credibility claim, no fake study visual). | 3 |
| G9 | G · shoulder feint | «ميسي هو اللي بيبرمج رد فعل المدافع من قبل ما الكورة تيجيله أصلًا! هو عارف إن لو عمل 'الكتف يمين'، المدافع هيتحرك شمال بنسبة ٩٩٪.» | **Programming the defender.** Top-down duel: on «الكتف يمين» an orange shoulder arrow dips right; the ink defender dot slides left along a sky dashed "predicted" line drawn *before* he moves. «99٪» lands as rhetoric-sized hero numeral. | 4 |
| A8 | A · punch 1.15 | «ميسي مش بيجري أسرع من المدافع.. ميسي 'عايش في المستقبل' بثانية كاملة قدام عقل الخصم.» | **The thesis on the face.** «عايش في المستقبل» across two caption states, orange. | 5 |
| G10 | G · lag | «المدافع بيبقى عامل زي الآلة المكسورة اللي بتحاول تلحق 'تحديث' ميسي، بس دايماً بيكون متأخر بخطوة!» | **Signature moment ② — the lag.** An ink-drawn progress bar «تحديث»: Messi's bar (orange) completes; the defender's bar stutters. The defender element alone gets the reel's **only** disruption effect: 2–3 offset graphite ghost copies stepping a frame behind (no RGB split, no noise). «متأخر بخطوة» hero. | 4 |
| A9 | A · 1.08 | «المدافعين العاديين بيجروا ورا الكورة... لكن قدام ميسي، المدافع هو اللي بيجري ورا 'وهم'.» | Face. «وهم» orange. | 4 |
| G11 | G · hero, part 1 | «ميسي بيمشي ببطء يخلّي المدافع يقرب منه ويحس بالأمان...» | **Hero sequence begins — the trap.** Slow orange footsteps; the ink defender closes in; a calm sky circle «الأمان» forms around him. Deliberately slow motion — the stillness before the hit. | 4 |
| A10 | A · 1.15 | «وفي اللحظة اللي المدافع بيقرر يمد رجله عشان يقطع الكورة،» | Tension on the face, close crop, no movement. | 5 |
| G12 | G · hero, part 2 | «ميسي بيديها 'تتش' صغير يمين أو شمال... البوم! المدافع بيبقى في عالم تاني.» | **Signature moment ③ — the touch.** Same diagram as G11 (shared-element continuity): the defender's leg line extends; on «تتش» a tiny orange touch arrow; one held beat; on «البوم!» hard hierarchy hit — «البوم» fills the frame for 6–10 frames with the reel's single low impact SFX, the safe circle shatters into two arcs, the defender dot is displaced off the page edge. «في عالم تاني» settles small. | 5 |
| A11 | A · 1.08 | «ميسي مش بيمر من المنافسين عشان يفترسهم،» | Face (contrast setup). | 3 |
| G13 | G · equation | «ميسي بيمر منهم كأنه بيكتب معادلة رياضية على سبورة؛ بسيطة، مبهرة، ومستحيل تتكرر.» | **The dribble as an equation.** A chalk-on-paper board: the orange dribble path is written stroke by stroke as if handwritten, ink defender dots as terms; then three words stack on their words: «بسيطة» (ink), «مبهرة» (ink), «مستحيل تتكرر» (orange, biggest). | 4 |
| G14 | G · music | «الكورة في رجله مش أداة لعب.. الكورة دي أداة موسيقية، وهو العازف الوحيد اللي فاهم كل نوتة فيها.» | **The ball as a note.** Five staff lines draw; small balls sit on them as notes; on «العازف الوحيد» one orange ball-note lifts above the staff. Hero «أداة موسيقية». (Start on the face for «مش أداة لعب» if the rhythm needs it.) | 3 |
| A12 | A · 1.00 | «لعيبة كتير بتجري وتسجل أهداف، بس التاريخ مش بيفتكر مين جري أسرع...» | Face. «مين جري أسرع» half-opacity context, then cut. | 3 |
| G15 | G · stillness | «التاريخ بيفتكر مين خلى الكورة تنام في رجليه وتسمع كلامه.» | **The quietest page.** A left-boot outline from above, a ball resting against it; almost no motion — one slow line draw. Hero «تنام في رجليه». | 3 |
| A13 | A · punch 1.15 | «ده مش لاعب كورة... دي عبقرية اتولدت بالغلط في جسم بني آدم.» | **Payoff on the face**, longest hold of a single crop. «عبقرية» in orange (the only caption with a gold underline). | 5 |
| A14 | A · 1.00 → 1.08 | «لو كنت فاكر إن ميسي شاطر بس عشان بيعرف يجيب أجوال، تبقاش فاهم حاجة.. شاركنا في الكومنتات،» | CTA setup on the face; punch on «شاركنا». | 4 |
| G16 | G · CTA card | «أكتر لقطة حسيت فيها إن ميسي بيلعب 'فيديو جيم' والناس كلها NPCs كانت ضد مين؟» | **Comment card.** Hand-inked generic game frame: the orange 10-dot with a small «P1» tag, ink dots labelled `NPC` (in `<bdi>`); a comment-bubble outline draws; hero «ضد مين؟»; small «اكتب في الكومنتات». Hold fully built ≥ 1.0 s after the last word. No black ending, no reset tail. | 4 |

Target ratio ≈ 48–55 % presenter / 45–52 % pages; check it after measuring and adjust only by meaning.

## 7. World A — the presenter

- The presenter dominates A sections. Clean hard cuts. Three crop states: **1.00** base, **≈1.08** emphasis, **≈1.15** close; changes only where §6 (or a measured reason) says, not every sentence.
- Crop = scale on an **untimed wrapper** around the timed `<video>` clips, transform origin on the measured face point so eyes and chin stay fixed. Never animate the timed `.clip`. Keep eyes, chin, and active hands inside frame at every crop.
- Natural colour: no sharpening, no crushed blacks, no orange skin. A very light warm lift is allowed so the footage sits next to the paper pages.

## 8. World B — the notebook pages

- Each page: warm paper with a faint graph-paper grid (`--paper-dark` at low opacity), **one** focal diagram/object, **one** dominant Arabic keyword at display size plus small context, progressive assembly synced to the spoken words, a readable hold, a decisive cut.
- Structure every page as **entrance → build → proof/hold → exit/cut**.
- **The first frame of every page already shows the scene** (entrances that start at local t≈0 begin part-way revealed). An empty paper frame on a hard cut reads as a mount flash.
- Pitch diagrams are top-down and minimal: only the lines the idea needs (a touchline, a box, a goal frame), in `--pitch` or graphite at 1.5–3 px.
- No second subtitle layer on pages: the spoken phrase becomes the page's typography, each chunk revealed at its spoken moment.

## 9. Art direction — palette and texture

```css
--paper:#E9E0D3; --paper-dark:#D4C8B8; --paper-light:#F6F0E7; --cream:#FFFDF7;
--ink:#1B1D1E;   --ink-soft:#3A3D3E;   --graphite:#5A5C5E;
--accent-warm:#E66A21; --accent-warm-dark:#C85218;   /* Messi + main emphasis */
--sky:#75AADB;         --sky-ink:#2F5F8A;            /* future / scan / prediction (dashed) */
--gold:#D8A44A;                                      /* the 10 and «عبقرية» only */
--pitch:#3F6B4A;                                     /* rare: pitch-diagram lines only */
```

- **Text contrast:** orange text on paper uses `--accent-warm-dark`; sky text uses `--sky-ink`; `#E66A21` and `#75AADB` are for fills, strokes, and chips. On footage, use lighter tints so they stay ≥ 3:1.
- Textures resolved locally via `/media-use` or a registry primitive: subtle paper grain, graph grid, optional chalk stroke for G13 only. One texture per page at most.
- Avoid: green code rain, neon, glowing brains, circuit boards, sci-fi HUDs, lens flares, fire/lightning, glossy 3D, glassmorphism, particles, rainbow palettes.

## 10. Opening and ending

**Opening:** frame 0 is the face — never black, logo, title, or fade. Push 1.00 → ≈1.12 over 0.55–0.85 s, `expo.out`, no bounce, no return. First small caption during the push. Hard cut into G1 on «بيبص في الناحية التانية», within ≈1–2 s.

**Ending:** presenter visible through the CTA setup (A14); hard cut to G16 on «أكتر لقطة»; card fully built and held ≥ 1.0 s after «ضد مين؟». Never end on black, never reset an animation at the tail.

## 11. Arabic typography and bidi

- Check the real font inventory (`fc-list :lang=ar`, then `document.fonts.check()` in the preview). Preferred: Cairo, Tajawal, Noto Kufi Arabic, Noto Sans Arabic, IBM Plex Sans Arabic. If none is installed, install Cairo from the OFL Fontsource package (`npm i @fontsource/cairo`), copy Arabic + Latin woff2 (400–900) into `assets/fonts/`, and declare `@font-face` with `unicode-range` in **every** file that uses it. Report how the font was obtained.
- Weights: 900 display, 800 captions/supporting, 700 labels, 500 small copy. Never a synthesized weight.
- `dir="rtl"` everywhere; whole-word spans; natural Arabic line breaks; **never split or animate individual letters**.
- **Reveal masks need room for Arabic dots and hamza:** `overflow:hidden` masks get ≈0.2em top / 0.36em bottom padding with matching negative margins, or the dots under «ي» get clipped.
- **Mixed scripts:** wrap Latin tokens (`NPC`, `P1`, `scanning`) and numerals in `<bdi>` or `unicode-bidi:isolate`. One digit system across the reel: Western digits (`80٪`, `0.3–0.4 ث`, `99٪`, `10`, `+1 ث`). Do not glue «بـ»/«لـ» to a big numeral — separate tokens.
- Directional words matter in this script («يمين» / «شمال»): pitch diagrams are drawn from **the viewer's** point of view, and «الكتف يمين» moves visually to the viewer's right. Check every arrow against its word.

## 12. Captions (presenter sections only)

- Word-timed from the verified transcript; **hand-author** semantic 1–4-word groups (machine grouping splits Arabic phrases badly).
- ≈61–68 % of frame height, over the torso, never over the face at any crop, above platform UI. Display font at 800, compact line height, no opaque pill.
- Cream `#FFFDF8`; not-yet-spoken words at ≈50–55 %; **one** highlighted word per group in orange (the highlight words are named in §6), sky rarely (only for «المستقبل»), gold only the underline under «عبقرية».
- If the clothing/background behind the captions is bright or busy, use a feathered radial shadow sized to each group so contrast stays ≥ 3:1.
- 2–4-frame opacity/vertical settle or a clean hard replacement. No bouncing karaoke, no per-letter wobble, no overshoot on every word.

## 13. Motion language

Energy comes from hierarchy changes, progressive assembly, and decisive cuts — not nonstop movement. **2–4 motion rules per page** from: masked word rise; short staggered assembly; scale settle; **path draw** (`stroke-dashoffset`, long-tailed ease, completing on the spoken word); small object pose change; restrained page drift (≤ 2 %); shared-element continuity (G11 → G12 use the same diagram).

**Motion encodes the idea:** Messi's elements move with crisp, early, decisive eases; defenders' elements move later and heavier; sky "future" lines always appear **before** the thing they predict. This is the whole reel in one rule.

Timing at the measured fps: entrances 6–12 frames, exits shorter, stagger 2–5 frames, readable hold 10–20 frames; hard cuts over dissolves. The blink (G7) and the «البوم» hit (G12) are the only "transition" effects in the reel; the lag ghosts (G10) are the only disruption effect.

Forbidden: continuous random motion, any other glitch, liquid morphs, chrome/3D text, particles, excessive parallax, spinning objects, transition-pack variety, animations that reset at the tail.

Seek-safe only: one paused GSAP timeline per composition registered on `window.__timelines`, `fromTo` everywhere, no `Date.now()`, `performance.now()`, unseeded `Math.random()`, timers, or `repeat:-1`. **Scene-unique ids for every GSAP selector** (scene scripts share one document).

## 14. Silence removal and source editing

- Remove leading/trailing dead air, set-up/tear-down, and bad takes. Internal pauses > ≈0.24 s → keep ≈3 frames after speech and ≈2 before the next word. **Keep longer on purpose:** after «سر مرعب..» (0.4–0.6 s), the «...» before «البوم!» (one held beat), and before «ده مش لاعب كورة...». Do not delete every breath.
- Never cut inside a syllable (check suspicious spots on a spectrogram); never cut off a gesture that completes the sentence.
- Separate `<video>` clips with `data-media-start` / `data-duration` / `data-start`, all on the frame grid; derive each duration from the rounded edges so neighbours abut exactly. If audio is separated, its ranges match the picture exactly. Dialogue continues uninterrupted under pages.

## 15. Audio and sound design

- The original dialogue is authoritative. Denoise only if the noise floor needs it; no robotic gating. High-pass ≈70 Hz, gentle compression, two-pass loudnorm to ≈ **−14 LUFS** integrated, ≤ **−1 dBTP**, no pumping.
- No music unless supplied. Voice-only beats unlicensed music.
- **Sound concept — the sound follows the same code as the colour:** Messi's sounds are **light, crisp, and early** (taps, clicks, a soft whoosh); the defender's sounds are **heavy, low, and late** (thud, stutter, slide); **the future is heard before it is seen** — a reverse swell that peaks exactly on the frame the event happens. Voice is always the hero.
- **Files.** The SFX live in `sfx/` at the project root. **Use `sfx/prepared/*.wav` first** — already trimmed, faded, 48 kHz, transients at −3 dBFS peak and beds at −20 LUFS — and read `sfx/sfx-manifest.json` for each file's peak offset, tick/beat grid, and origin (place each clip so its peak lands on the target frame: start = target − `peak_s`). Prepared set: `04-reverse` (made from the boom), `06-clock`, `08-heartbeat`, `09-tap`, `10-impact`, `11-roar`, `15-crowd-far` (made from the crowd). Every ★★★ is covered. Any other row whose file is missing: use the closest bundled `/media-use` SFX or leave that hit out — never fetch audio from anywhere else. Copy what you use into `assets/sfx/` and log `sfx/SOURCES.md` provenance in `.media/manifest.jsonl`.
- **Sync:** impacts and taps land on the visual frame or 1 frame before it; whooshes and reverse swells are placed so their **peak** (not their start) hits the motion/word; ticks and heartbeats sit on a steady grid and stop on a word. Measure each file's peak offset and place by the peak.

| File in `sfx/` | Tier | Scene / exact moment | Level vs. voice | Rule |
| --- | --- | --- | --- | --- |
| *(none)* | — | A0 hook, first ≈1–2 s | — | **voice only.** The first sound effect in the reel is the G1 whoosh |
| `01-whoosh.mp3` | ★★ | G1 pass line on «بيلعب الكورة»; G9 shoulder arrow on «الكتف يمين» | −16 to −20 dB | these two uses only, never on ordinary cuts |
| `02-data.mp3` | ★ | G3, as «هندسة الماتريكس» assembles; ends on the title lock | −20 to −24 dB | ≤ 1.2 s, soft texture, not sci-fi |
| `03-ping.mp3` | ★ | G4, one soft ping per scan sweep | −22 dB | max 3 pings, falling slightly in level |
| `04-reverse.mp3` | ★★★ | G6 peaks on «شاف المستقبل»; G9 peaks on the frame the defender starts to move | −16 to −20 dB | **the sound of the future** — it arrives before the event |
| `05-click.mp3` | ★★ | G7 eyelid close on «ترمش» | −16 dB | one click |
| `06-clock.mp3` | ★★★ | G8, under the timer bar filling to «0.3–0.4 ث» | −20 to −24 dB | ticks **stop dead** on «بس مع ميسي؟» (A6) |
| `07-glitch.mp3` | ★ | G10, under the lagging defender bar | −20 dB | ≤ 0.6 s, the reel's only glitch sound |
| `08-heartbeat.mp3` | ★★★ | from G11 «بيمشي ببطء», continuing under A10 | −16 to −20 dB | beats slow slightly; **stops completely** after «يقطع الكورة» |
| `09-tap.mp3` | ★★★ | G12, the tiny touch on «تتش» | −14 to −18 dB | small, crisp. Then **one held beat of voice-only silence** |
| `10-impact.mp3` | ★★★ | G12 on «البوم!» | loudest SFX, still ≥ 8 dB under the voice peak | the single impact in the reel |
| `11-roar.mp3` | ★★★ | G12, 1–1.5 s crowd surge starting with the impact, fading under «في عالم تاني» | −18 to −22 dB | replaces commentator audio; once only |
| `12-grass.mp3` | ★ | G12, a thin layer 2–4 frames after the impact as the defender slides off the page | −22 dB | only if it doesn't muddy the impact |
| `13-chalk.mp3` | ★★ | G13, while the dribble path is "written" on the board | −20 to −24 dB | follows the stroke timing; stops when the path completes |
| `14-note.mp3` | ★★ | G14, one soft single note when the orange ball-note lifts on «العازف الوحيد» | −18 to −22 dB | a single note, never a melody or music bed |
| `15-crowd-far.mp3` | ★★ | slow fade-in from G15 «تنام في رجليه», under A13 and the CTA card | −26 to −30 dB | a slight lift under «عبقرية»; fades out over the final hold, no hard stop |
| `16-pop.mp3` | ★ | G16, the comment bubble finishing its draw | −20 dB | soft |

- **Restraint rules:** at most one SFX at a time except the G12 stack (tap → silence → impact + roar); never let an SFX cover the onset of a highlighted keyword; after the G12 roar fades, give ≥ 1 s of voice-only before the next SFX.
- After placing them, re-measure the final mix: ≈ −14 LUFS integrated, ≤ −1 dBTP, and every word intelligible at each SFX moment (render a short audio excerpt per moment and compare short-term loudness of voice vs. SFX). List each SFX with its placed time and level in `REVIEW.md`.

## 16. Implementation contract

- 1080×1920, native fps (else 30000/1001, reported), final H.264 + AAC MP4.
- Readable Studio tracks: A-roll picture, dialogue audio, pages, captions (one captions host, `data-track-kind="captions"`), SFX.
- One sub-composition per page; `class="clip"` with the supported `data-*` timing attributes; never animate `display`/`visibility`/`autoAlpha` on a `.clip` — animate a child wrapper. Unique ids across the assembled document.
- Safe zones: essential text within x 80–1000, y 140–1650, and as far as possible inside the platform clear band `check` uses (≈ y 290–1250, x 120–888). CTA card comfortably above the bottom controls.
- No render-time network requests of any kind.

## 17. Verification and the director's review loop

1. Write `BRIEF.md`, `source-analysis.md`, transcript artifacts, `SCRIPT_DIFF.md`, `DIRECTOR_NOTES.md`, `FACT_CHECK.md`, `STORYBOARD.md`, `timing-map.json`. Then build the full project — do not stop after planning.
2. `npx hyperframes lint` after the first structural pass and after every major timing change.
3. `npx hyperframes check --json` until **0 errors**; fix contrast, overlap, font, motion, and layout findings; justify every warning you keep.
4. `npx hyperframes keyframes` for the opening push, every crop change, and the G11 → G12 hand-off.
5. Snapshots: exact first frame; push at 0/25/50/75/100 %; every hard cut ±1 frame; first frame, midpoint, and completed state of every page; each module of G5; the blink frames in G7; the lag in G10; G12 before/at/after «البوم»; CTA hold; final-minus-hold and the exact final frame. Then `npx hyperframes snapshot --review` (seams + phone sheets at 360 px).
6. **Director's review — score every scene 1–5** in `REVIEW.md` on: **Hook** (face at frame 0, push lands, first cut on «بيبص في الناحية التانية»); **Clarity** (one focal object, one dominant phrase, readable at 360 px); **Mute test** (understood with sound off); **Sync** (every reveal on its spoken word ±2 frames); **Colour code** (orange = Messi, ink = defender, dashed sky = future — never broken); **Truth** (nothing beyond what was said, no likeness/crest/trophy/fake study); **Craft** (shaping, dot clearance, bidi, arrows match يمين/شمال, contrast, no flashes, no reset tails); **Rhythm** (boundaries by meaning; G12 feels like the peak). Anything below 4 gets fixed and re-snapshotted. Do **at least one full revision pass** before the preview gate; name the weakest shot and what you would do with more time.
7. Check for: black flashes, empty first frames, missing-font frames, broken shaping, clipped dots or captions, bidi reordering, sub-composition mount flashes, lingering pages, reset tails, A/V desync.
8. `npx hyperframes preview --background`, confirm it answers 200, give me the **preview URL**, the scores, the `SCRIPT_DIFF.md` summary, and every `check-with-user` item. **Wait for approval.** This is the only pause.
9. After approval: `npx hyperframes render --quality delivery --fps <fps> --sdr --format mp4 --strict -o final_reel.mp4`, and export `cover.png` (1080×1920) from the strongest page — G3 «هندسة الماتريكس» or G12 «البوم» — as a thumbnail candidate.
10. Verify with ffprobe (1080×1920, expected fps, H.264, AAC, non-zero size, duration = root `data-duration`), ebur128 loudness, blackdetect, decoded frames at key times, and A/V sync (audio onsets vs planned word times).

## 18. Delivery report

The project folder, `final_reel.mp4`, `cover.png`, `captions.srt`, `transcript.json`, `timing-map.json`, and a short report: original/final duration, removed ranges and re-takes, number of scenes, the hero moment, actual A/B ratio, fonts and weights (and how the font was obtained), registry/media dependencies with provenance, director's scores after revision, validation status, kept warnings with reasons, transcript uncertainty and script differences, open fact-check items.

## 19. Stop and report — never pretend success

Stop with a concrete blocker if: no or more than one ambiguous `rawreel.*`; media cannot be decoded; the Arabic transcript remains materially uncertain after review; no installed or installable font shapes Arabic correctly; HyperFrames skills/CLI cannot run; a beat can only be shown by inventing evidence or using a real likeness/crest/trophy and no truthful abstract alternative works; `check` still reports an unresolved error.
