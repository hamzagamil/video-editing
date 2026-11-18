# Director's prompt — Arabic editorial football reel (Messi) with HyperFrames

> Paste everything below the line as one message, with exactly one `rawreel.*` talking-head video
> in the project folder. It extends `PROMPT.md` (the hardened technical brief from the previous
> reel) with a director's pass, a football art direction, a fact/rights guard for a reel about a
> real, active player, and a scored self-review loop before the preview gate.

---

You are the **director, senior Arabic short-form editor, motion designer, and HyperFrames implementer** of this reel. The subject of the narration is **Lionel Messi** (ليونيل ميسي / ليو). You are not a subtitle operator: you own the story, the rhythm, the image system, and the final quality. Every cut, crop, word, and object must have a reason you can state in one sentence.

Inside the project folder there is exactly one raw talking-head video whose filename begins with `rawreel` (`.mp4`, `.mov`, …). There is no reference video, no SRT, no storyboard, no B-roll, no photos, no match footage. Do not ask for any.

Inspect, transcribe, direct, edit, design, animate, validate, self-review, preview, and render a premium Arabic 9:16 reel using **HyperFrames as the primary and final system**. Build the complete working project — not recommendations, snippets, or an EDL. **Stop only once**, at the Studio-preview approval gate, before rendering.

---

## 0. The quality bar in one paragraph

It must feel like a football magazine came alive on a phone: an immediate face-first hook with a fast push-in, a hard cut on the first big claim into a full-screen editorial page (warm paper, one bold monochrome football symbol, huge Arabic headline), back to the presenter for credibility, a longer "hero" scene at the emotional peak, a confident payoff on the face, and a designed closing card. Restrained, precise, truthful, and readable with the sound off.

---

## 1. Framework and skills

- HyperFrames is the source of truth for composition, source-range editing, captions, interludes, animation, audio placement, Studio preview, validation, and render. No pure Remotion rebuild; Remotion only if an installed HyperFrames workflow explicitly requires it.
- Read the installed skills, in this order, and obey them: `/hyperframes`, `/general-video` (this job is a footage remix: silence removal, hard cuts, reframes, captions, full-screen interludes), `/hyperframes-core`, `/hyperframes-creative`, `/hyperframes-animation`, `/hyperframes-keyframes`, `/hyperframes-studio`, `/media-use`, `/hyperframes-audio`, `/hyperframes-registry`, `/hyperframes-cli`. Read the `/hyperframes` references too (`types/vertical.md`, `film.md`, `captions.md`, `overlays.md`, `motion.md`, `format.md`, `review.md`) where present.
- If the skills are not available as slash commands, install the CLI locally and read them from `node_modules/hyperframes/dist/skills/`. If neither works, that is a blocker (§19).
- Work in a new child folder `hyperframes-messi-edit/` (`npm i hyperframes`, `npx hyperframes init … --skip-skills`). Never modify the original `rawreel` file.
- Search `npx hyperframes catalog` before hand-building any named effect, texture, caption style, or transition.
- No render-time network: vendor GSAP locally (`assets/vendor/gsap.min.js`) instead of the scaffold's CDN tag; fonts, SFX, textures, and media all live in `assets/`.

## 2. Technical inspection

1. `ffprobe`: duration, width/height, **rotation**, frame rate, codecs, pixel format, **colour transfer/primaries**, audio sample rate/channels. Record everything in `source-analysis.md`.
2. **HDR footage** (iPhone HLG: `arib-std-b67` / `bt2020`): convert to SDR BT.709 first. Compare on one frame a plain transfer conversion (`zscale=tin=arib-std-b67:t=bt709:pin=bt2020:p=bt709:min=bt2020nc:m=bt709:r=tv:npl=203`) against hable/mobius/reinhard tonemaps; keep the one with natural skin and real contrast. Build a 1080×1920 H.264 proxy at the native frame rate with a short GOP (`-g` = fps/2) for seek-safety.
3. Contact sheets at 1–2 fps across the whole source. Measure in canvas pixels: face centre, eye line, chin, active hands, free negative space, set-up/tear-down sections to cut.
4. Audio on an extracted WAV: integrated loudness, noise floor in pauses, silence map (`silencedetect -35 dB, d=0.2`). Never cut from numbers alone — verify against speech and visible gestures.

## 3. Transcription (Egyptian Arabic, football vocabulary)

1. `npx hyperframes transcribe <wav> --model large-v3 --language ar` (never an `.en` model). If the model download fails behind a proxy, fetch `ggml-large-v3.bin` into `~/.cache/hyperframes/whisper/models/`, verify its sha256, and request the needed hosts if blocked.
2. Real word timing: whisper.cpp with DTW (`whisper-cli -m ggml-large-v3.bin -l ar -nfa -dtw large.v3 -ojf`). Never trust evenly spread segment timings.
3. Align: wording from the best dialect pass, times from DTW, every word clamped into the measured speech chunks. Find chunks with no words and words sitting in silence; fix by hand; document every override.
4. **Football glossary — correct mis-hearings only when the audio supports it:** ميسي، ليو، ليونيل، الأرجنتين، منتخب التانجو، الألبيسيليستي، روساريو، لاماسيا، برشلونة/البارسا، باريس سان جيرمان، إنتر ميامي، الكامب نو، الكرة الذهبية / البالون دور، كوبا أمريكا، كأس العالم / المونديال، دوري الأبطال/التشامبيونز، الليجا، مارادونا، رونالدو، جوارديولا، سكالوني، تشافي، إنييستا، سواريز، نيمار، دي ماريا، هاتريك، أسيست، مراوغة، ركلة حرة، العشرة/رقم 10، GOAT، الكلاسيكو.
5. Manual review against the audio: names, dialect, English/Spanish terms, every number and date. Never animate an unverified transcript. Write any remaining uncertainty down.
6. Save: `transcript.json` (`id`, `text`, `start`, `end` per word), `captions.srt` (on the final reel timeline), `source-analysis.md`, `timing-map.json` (every retained range → output start/end, frame-exact, plus removed ranges with reasons).

## 4. Director's pass — before any design (write `DIRECTOR_NOTES.md`)

Answer these from the verified transcript. Short, decisive, no generic filler.

1. **Thesis** — the one sentence the reel argues (in Arabic, in the speaker's own terms).
2. **Angle** — what kind of Messi story this is (legacy, comeback, rivalry, record, a single match, a myth vs. reality, a lesson…). The visual language follows the angle.
3. **Emotional arc** — split the narration into beats and give each an energy level 1–5. Draw it as a text graph. There must be one clear peak and at least one deliberate release.
4. **Hero moment** — the single beat that gets the most ambitious scene (longest build, strongest hierarchy, the one image the viewer remembers). Usually the peak of the arc, not the hook.
5. **Hook options** — list three candidate first-cut points (the exact word for the hard cut into the first interlude) and choose one with a reason: strongest claim, most surprising number, or most famous name.
6. **Earned stillness** — pick 1–2 places where the edit deliberately holds: a kept 0.35–0.6 s pause before the biggest line, or the presenter held without a crop change while saying something emotional. Stillness makes the cuts hit.
7. **Mute test plan** — for every beat, what the viewer understands with the sound off (most reels are watched muted). If a beat fails, fix it with typography, not more motion.
8. **Ending** — what the last spoken line is, and what the closing card says (§10 rules).

## 5. Fact and rights guard (non-negotiable for a real, active player)

Write `FACT_CHECK.md`: a table of every factual claim in the transcript (titles, trophies, goals, records, dates, clubs, transfers, quotes, comparisons) with three columns — exact spoken phrase, how it is shown on screen, status:

- `speaker-claim` — shown as the speaker said it, nothing added;
- `well-established` — a fact you are confident is true as stated;
- `check-with-user` — possibly wrong, ambiguous, or **time-sensitive** (Messi's career is ongoing; records, clubs, and tournament results change — never assume his current club, retirement status, or the latest tournament outcome from memory).

Rules:

- **Never put a number, title, date, or record on screen that the speaker did not say.** Do not "upgrade" a claim with extra stats. Do not silently correct the speaker; list suspected errors under `check-with-user` and mention them at the preview gate.
- Do not invent quotes from Messi or anyone else. A quote card is allowed only for words the speaker explicitly attributes, worded exactly as spoken.
- **No real imagery or likeness:** no photos or video of Messi or any player, no scraped or downloaded images, no match footage, no TV graphics, and **no AI-generated likeness or face of Messi or any real person.** Messi is represented only through symbols: the number 10, a left foot / boot outline, a ball trajectory, a generic jersey silhouette, a captain's armband, a pitch diagram, a career route.
- **No marks:** no club crests, AFA/FIFA/UEFA/CONMEBOL/league logos, sponsor marks, kit-maker stripes or swooshes, or replicas of real trophies. Trophies are drawn as **generic, abstract** cups/balls/medals (e.g. "a line-drawn cup", "a golden sphere"), never the recognisable World Cup, Champions League, or Ballon d'Or designs.
- Club or national-team **colours** may appear only as small semantic chips when that team is named (e.g. a sky-blue/white stripe band on «الأرجنتين»), never as the reel's identity, never with a crest.
- No music, crowd recordings, commentary audio, or anthems you did not generate or get bundled locally with a clear licence. Record provenance of every asset in `.media/manifest.jsonl`.

If a beat can only be shown truthfully with an unavailable real asset, replace it with an abstract diagram or a typography treatment.

## 6. Art direction — "Matchday Editorial"

Think: a vintage matchday programme crossed with a modern sports magazine and a coach's tactics board. Tactile paper, ink, chalk, print.

### Palette (personal, unbranded)

```css
--paper:#E9E0D3; --paper-dark:#D4C8B8; --paper-light:#F6F0E7; --cream:#FFFDF7;
--ink:#1B1D1E;   --ink-soft:#3A3D3E;
--accent-warm:#E66A21; --accent-warm-dark:#C85218;   /* main emphasis: conflict, peak, hero word */
--sky:#75AADB;         --sky-ink:#2F5F8A;            /* secondary: Argentina / identity, used sparingly */
--gold:#D8A44A;                                      /* micro-accent: titles, trophies, the "10" only */
--pitch:#3F6B4A;                                     /* rare: pitch-diagram lines only */
```

- Paper/cream/ink dominate every interlude. Burnt orange is the main emphasis. Sky is the secondary accent and stays rare. Gold is a micro-accent only (a cup rim, a star, the 10). Pitch green only for diagram lines, never a background.
- **Text contrast:** orange text on paper uses `--accent-warm-dark`; sky text on paper uses `--sky-ink`; `#E66A21` and `#75AADB` are for fills, strokes, and chips. On footage use lighter tints of the accents so they stay ≥ 3:1.
- Textures (resolved locally via `/media-use` or a registry primitive, never fetched at render): subtle paper grain, optional halftone dot on one object per scene, optional chalk stroke for tactical arrows. One texture per scene at most.
- Avoid: stadium-light lens flares, neon, fire/lightning effects, glossy 3D trophies, sports-broadcast HUD templates, glassmorphism, rainbow palettes, particles.

### Symbol library (pick from the transcript; never the same object twice)

| Spoken idea | Symbolic object (SVG/CSS, monochrome + one accent) |
| --- | --- |
| greatness / GOAT / legacy | a large **10** set like a jersey number, with a thin gold rule; or a stacked "hall" of plaque cards |
| a goal / finishing | a ball's curved trajectory drawn into a goal-frame outline; net lines tighten on the spoken word |
| dribbling / vision | a chalk tactics board: dots as defenders, one dotted path weaving through them |
| a career move / transfer | a route map: city/club **names as text nodes** (no crests) connected by a drawn path, RTL direction |
| a trophy / title | a generic line-drawn cup; a slot fills or a star is added on the word |
| a final / a single match | a scoreboard card or a match ticket stub with only the spoken details |
| a record / a number | the numeral as hero typography, counting only if the speaker counts; a ruler/tally |
| rivalry / comparison | a split page or a balance scale; the winning side gains weight and the accent |
| pressure / criticism / doubt | a newspaper-headline card with redaction bars, a fractured card, a falling line |
| captaincy / leadership | an armband outline with the spoken word set in it |
| left foot / technique | a boot outline from above with a strike arc |
| comeback / redemption | a path that dips and climbs, the climb drawn on the spoken phrase |
| question / CTA | an oversized keyword + a comment-bubble outline |

## 7. World A — the presenter

- The presenter stays visually dominant in A sections. Clean hard cuts. Three crop states: **1.00** base, **≈1.08** emphasis, **≈1.15** close. Change crop on a new claim, contrast, punchline, or payoff — not every sentence.
- Crop = scale on an **untimed wrapper** around the timed `<video>` clips, transform origin on the measured face point so eyes and chin stay fixed. Never animate the timed `.clip`. Keep eyes, chin, and active hands inside frame at every crop.
- Natural colour only: no sharpening, no crushed blacks, no orange skin. A very light warm lift is allowed if it helps the footage sit next to the paper scenes.

## 8. World B — full-screen editorial interludes

Each interlude is a designed 9:16 page, not a stock insert:

- warm paper ground; **one** strong monochrome symbolic object from §6; **one** dominant Arabic keyword at display size plus small supporting context; progressive assembly synced to the spoken words; a readable hold; a decisive cut.
- Structure every scene as **entrance → build → proof/hold → exit/cut**. One focal object and one dominant phrase at a time.
- **The first frame of every interlude already shows the scene** (entrances that start at local t≈0 begin part-way revealed). An empty paper frame on a hard cut reads as a mount flash.
- The hero-moment scene (§4.4) is the longest and richest: 3–5 modules or a full transformation, active element oversized in orange, completed elements settling to ink/cream/sky.
- No second subtitle layer on interludes: the spoken phrase becomes the scene's typography, each chunk revealed at its spoken moment. Keep every important claim; invent nothing.

## 9. Pacing, structure, and length

- Ratio ≈ **45–55 % presenter / 45–55 % interludes**, adapted to meaning: emotional or credibility-critical lines stay on the face.
- Interlude length: short 1.8–2.5 s, normal 2.8–4.0 s, hero scene up to ≈4.5–5 s if the speech needs it.
- Rhythm: presenter open 0.7–1.2 s → hard cut on the hook claim → presenter for context → mechanism/contrast interlude → presenter → **hero scene at the peak** → presenter for the payoff → CTA setup on the face → optional closing card.
- **Length decision, stated in `DIRECTOR_NOTES.md`:** silence removal is always applied. If the trimmed speech is ≤ ≈40 s, keep it all with 4–6 scenes. If longer, keep the whole argument (do not drop factual claims) and scale to ≈ one interlude per 7–8 s — unless I tell you a target duration.
- Never alternate on a clock. Meaning decides every boundary, and every boundary is a hard cut on a spoken word.

## 10. Opening and ending

**Opening:** frame 0 is the face — never black, logo, title, or a fade. Push 1.00 → ≈1.12 over 0.55–0.85 s with a strong ease-out (`expo.out`), no bounce, no return. The first small word-timed caption appears during the push. The first hard cut into an interlude lands on the chosen hook word within 1.0–2.0 s.

**Ending:** keep the presenter visible through the CTA setup; on the spoken CTA keyword, punch in or hard-cut to the closing card (oversized keyword, one minimal outline icon, one short Arabic instruction). Hold it fully built ≥ 12–18 frames after the last word (≥ 2 s if there is no spoken CTA). **If the speaker gives no CTA**, the card re-asks the speaker's own question or thesis (e.g. their own framing of the debate) with «اكتب رأيك في التعليقات» — do not invent a GOAT debate the speaker did not raise. Never end on black, never reset an animation at the tail.

## 11. Arabic typography and bidi

- Check the real font inventory (`fc-list :lang=ar`, then `document.fonts.check()` in the preview). Preferred: Cairo, Tajawal, Noto Kufi Arabic, Noto Sans Arabic, IBM Plex Sans Arabic. If none is installed, install Cairo from the OFL Fontsource package (`npm i @fontsource/cairo`), copy Arabic + Latin woff2 (400–900) into `assets/fonts/`, and declare `@font-face` with `unicode-range` in **every** file that uses it. Report how the font was obtained.
- Weights: 900 display headlines, 800 captions/supporting, 700 labels, 500 small copy. Never a synthesized weight.
- `dir="rtl"` everywhere; whole-word spans; natural Arabic line breaks; **never split or animate individual letters**.
- **Reveal masks need room for Arabic dots and hamza:** `overflow:hidden` masks get ≈0.2em top / 0.36em bottom padding with matching negative margins, or the dots under «ي» get clipped.
- **Mixed scripts:** wrap Latin tokens (GOAT, PSG, Ballon d'Or) and numerals in `<bdi>` or `unicode-bidi:isolate` so they never reorder the Arabic line. Use one digit system consistently across the reel (default Western digits 0–9 for scores, years, and records). Do not glue a small «لـ»/«بـ» to a big numeral — set them as separate tokens.
- Big numerals (10, scores, years) are allowed as hero typography only when spoken.

## 12. Captions (presenter sections only)

- Word-timed from the verified transcript; **hand-author** semantic 1–4-word groups (machine grouping splits Arabic phrases badly).
- ≈61–68 % of frame height, over the torso, never over the face at any crop, above platform UI. Display font at 800, compact line height, no opaque pill.
- Cream `#FFFDF8`; not-yet-spoken words at ≈50–55 %; **one** highlighted word per group (a name, number, or the key verb) in the warm accent, sky rarely (e.g. «الأرجنتين»), gold never in captions.
- If the clothing/background behind the captions is bright or busy, use a feathered radial shadow sized to each group (transparent at the edges) so contrast stays ≥ 3:1.
- 2–4-frame opacity/vertical settle or a clean hard replacement. No bouncing karaoke, no per-letter wobble, no overshoot on every word.

## 13. Motion language

Energy comes from hierarchy changes, progressive assembly, and decisive cuts — not nonstop movement. Use **2–4 motion rules per scene** from:

- masked word/line rise; short staggered assembly; scale settle;
- **path draw** — ball trajectories, dribble routes, career routes, tactical arrows drawn with `stroke-dashoffset` on a long-tailed ease, timed so the path completes on the spoken word;
- small object pose change (a cup tilts upright, a card flips, an armband tightens);
- restrained camera drift on the page (≤ 2 %);
- semantic hand-off between scenes when two consecutive interludes share an idea (e.g. the ball that finishes one path starts the next).

Timing at the measured fps: entrances 6–12 frames on long-tailed ease-outs, exits shorter, stagger 2–5 frames, readable hold 10–20 frames; hard cuts over dissolves.

Forbidden: continuous random motion, glitch (unless the transcript is literally about a mistake/error), liquid morphs, chrome/3D text, fire or lightning, particles, excessive parallax, spinning objects, transition-pack variety, animations that reset at the tail.

Seek-safe only: one paused GSAP timeline per composition registered on `window.__timelines`, `fromTo` everywhere, no `Date.now()`, `performance.now()`, unseeded `Math.random()`, timers, or `repeat:-1`. **Scene-unique ids for every GSAP selector** (scene scripts share one document).

## 14. Silence removal and source editing

- Remove leading/trailing dead air and set-up/tear-down. Internal pauses > ≈0.24 s → keep ≈3 frames after speech and ≈2 before the next word. Keep the "earned stillness" pauses from §4.6 longer on purpose. Do not delete every breath.
- Never cut inside a syllable (check suspicious spots on a spectrogram); never cut off a hand gesture that completes the sentence.
- Separate `<video>` clips with `data-media-start` (source offset), `data-duration` (retained length), `data-start` (output placement), all on the frame grid; derive each duration from the rounded edges so neighbours abut exactly. If audio is separated, its ranges match the picture exactly. Dialogue continues uninterrupted under interludes.

## 15. Audio and sound design

- The original dialogue is authoritative. Denoise only if the noise floor needs it; no robotic gating. High-pass ≈70 Hz, gentle compression, two-pass loudnorm to ≈ **−14 LUFS** integrated, ≤ **−1 dBTP**, no pumping.
- No music unless supplied. Voice-only is preferable to unlicensed music.
- Sound design (bundled `/media-use` or locally generated only, provenance recorded): 3–6 soft, meaningful hits on visible actions — a path completing into the goal frame, a card stamp, the cup settling, the closing-card lockup. A short referee-whistle or soft crowd swell is allowed **once**, only if locally generated/licensed, only at the hero moment, and at least ≈15 dB under the voice. No commentary, no chants, no anthems.

## 16. Implementation contract

- 1080×1920, native fps (else 30000/1001, reported), final H.264 + AAC MP4.
- Readable Studio tracks: A-roll picture, dialogue audio, graphic scenes, captions (one captions host, `data-track-kind="captions"`), SFX.
- One sub-composition per interlude; `class="clip"` with the supported `data-*` timing attributes; never animate `display`/`visibility`/`autoAlpha` on a `.clip` — animate a child wrapper. Unique ids across the assembled document.
- Safe zones: essential text within x 80–1000, y 140–1650, and as far as possible inside the platform clear band `check` uses (≈ y 290–1250, x 120–888). Closing card comfortably above the bottom controls.
- No render-time network requests of any kind.

## 17. Verification and the director's review loop

1. Write `BRIEF.md`, `source-analysis.md`, transcript artifacts, `DIRECTOR_NOTES.md`, `FACT_CHECK.md`, `STORYBOARD.md` (exact verified phrase per scene, frame-snapped output times, crop states, energy level, A/B ratio), and `timing-map.json`. Then build the full project — do not stop after planning.
2. `npx hyperframes lint` after the first structural pass and after every major timing change.
3. `npx hyperframes check --json` until **0 errors**; fix contrast, overlap, font, motion, and layout findings; justify every warning you keep.
4. `npx hyperframes keyframes` for the opening push, every crop change, and every scene hand-off.
5. Snapshots: exact first frame; push at 0/25/50/75/100 %; every hard cut ±1 frame; first frame, midpoint, and completed state of every interlude; every module state of the hero scene; closing-card hold; final-minus-hold and the exact final frame. Then `npx hyperframes snapshot --review` (seams + phone sheets at 360 px).
6. **Director's review — score every scene 1–5** in `REVIEW.md` on:
   - **Hook** — face at frame 0, push lands, first cut within 2 s on the strongest word;
   - **Clarity** — one focal object, one dominant phrase, readable at 360 px;
   - **Mute test** — the beat is understood with the sound off;
   - **Sync** — every reveal lands on its spoken word (±2 frames);
   - **Truth** — nothing on screen beyond what was said; no likeness, crest, or trophy replica;
   - **Craft** — Arabic shaping, dot clearance, contrast, no flashes, no reset tails;
   - **Rhythm** — boundaries motivated by meaning; the hero moment feels like the peak.
   Anything below 4 gets fixed and re-snapshotted. Do **at least one full revision pass** before the preview gate, and name the weakest shot and what you would do with more time.
7. Check for: black flashes, empty first frames, missing-font frames, broken shaping, clipped dots or captions, bidi reordering, sub-composition mount flashes, lingering scenes, reset tails, A/V desync.
8. `npx hyperframes preview --background`, confirm it answers 200, give me the **preview URL**, the scores, and every `check-with-user` item from `FACT_CHECK.md`. **Wait for approval.** This is the only pause.
9. After approval: `npx hyperframes render --quality delivery --fps <fps> --sdr --format mp4 --strict -o final_reel.mp4`. Also export `cover.png` (1080×1920) from the strongest interlude frame as a thumbnail candidate.
10. Verify with ffprobe (1080×1920, expected fps, H.264, AAC, non-zero size, duration = root `data-duration`), ebur128 loudness, blackdetect, decoded frames at key times, and A/V sync (audio onsets vs planned word times).

## 18. Delivery report

The project folder, `final_reel.mp4`, `cover.png`, `captions.srt`, `transcript.json`, `timing-map.json`, and a short report: original/final duration, removed ranges, number of scenes, the hero moment, actual A/B ratio, fonts and weights (and how the font was obtained), registry/media dependencies with provenance, director's scores after revision, validation status, kept warnings with reasons, transcript uncertainty, and open fact-check items.

## 19. Stop and report — never pretend success

Stop with a concrete blocker if: no or more than one ambiguous `rawreel.*`; media cannot be decoded; the Arabic transcript remains materially uncertain after review; no installed or installable font shapes Arabic correctly; HyperFrames skills/CLI cannot run; a beat can only be shown by inventing evidence or using a real likeness/crest/trophy and no truthful abstract alternative works; `check` still reports an unresolved error.
