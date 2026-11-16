# Reusable prompt — Arabic editorial reel with HyperFrames

> This is the brief that produced `final_reel.mp4`, updated with everything that had to be decided
> or fixed during the build (HDR footage, missing Arabic font, accurate Arabic word timing, caption
> legibility, first-frame flashes …), so a new run gets there directly.
> Paste everything below the line as one message, with one `rawreel.*` video in the project folder.

---

You are the senior Arabic short-form editor, motion designer, and HyperFrames implementer for this task.

Inside the project folder there is exactly one raw talking-head video whose filename begins with `rawreel` (`rawreel.mp4`, `rawreel.mov`, …). There is no reference video, no SRT, no storyboard, and no B-roll. Do not ask for any.

Inspect, transcribe, edit, design, animate, validate, preview, and render a premium Arabic 9:16 reel using **HyperFrames as the primary and final system**. Build the complete working project — not recommendations, snippets, or an EDL. Stop only once, at the Studio-preview approval gate, before rendering.

## 1. Framework

- HyperFrames is the source of truth (composition, source-range editing, captions, interludes, animation, audio, preview, validation, render). No pure Remotion rebuild.
- Read the installed skills first: `/hyperframes` (then its references: `types/vertical.md`, `film.md`, `captions.md`, `overlays.md`, `motion.md`, `format.md`, `review.md`), `/hyperframes-cli`, `/media-use`. If skills are not installed as slash commands, read them from `node_modules/hyperframes/dist/skills/`. Use `npx hyperframes catalog` (the registry) before hand-building any named effect, caption style, or transition.
- Install the CLI locally in a new child folder `hyperframes-reel-edit/` (`npm i hyperframes`), scaffold with `npx hyperframes init … --skip-skills`, and work only there. Never modify the original `rawreel` file.
- No render-time network: vendor GSAP locally (`assets/vendor/gsap.min.js`) instead of the CDN tag the scaffold writes; fonts, SFX, and media all live in `assets/`.

## 2. Inspect the source first

1. `ffprobe`: duration, width/height, **rotation**, frame rate, codecs, pixel format, **colour transfer/primaries**, audio rate/channels.
2. **If the footage is HDR (iPhone HLG: `arib-std-b67` / `bt2020`)**, convert it to SDR BT.709 before anything else. Compare on one frame a plain transfer conversion (`zscale=tin=arib-std-b67:t=bt709:pin=bt2020:p=bt709:min=bt2020nc:m=bt709:r=tv:npl=203`) against hable/mobius/reinhard tonemaps, and keep the one with natural skin and real contrast. Build a 1080×1920 H.264 proxy at the native frame rate with a short GOP (`-g` = half the fps) for seek-safety. Keep the original untouched.
3. Contact sheets at 1 fps across the whole source: framing, face position (measure the face centre, eyes, chin, hands in canvas pixels), gestures, set-up/tear-down sections to cut.
4. Audio: integrated loudness, noise floor in pauses, silence map (`silencedetect -35 dB, d=0.2`) run on an extracted WAV, not the video.
5. Transcription (Egyptian Arabic):
   - `npx hyperframes transcribe <wav> --model large-v3 --language ar` (never an `.en` model). If the model download fails behind a proxy, download `ggml-large-v3.bin` with curl into `~/.cache/hyperframes/whisper/models/` and verify its sha256; ask for the needed network hosts (Hugging Face and its CDN) if they are blocked.
   - For real word timing run whisper.cpp with DTW: `whisper-cli -m ggml-large-v3.bin -l ar -nfa -dtw large.v3 -ojf`. Do not trust evenly-spread segment timings.
   - Align: take the wording from the best dialect pass, the times from DTW, and clamp every word into the measured speech chunks (complement of the silence map). Check for chunks with no word and words sitting in silence; fix them by hand and document every override.
   - Review the text manually: names, dialect words, English terms, numbers. Never publish an unverified transcript. Write remaining uncertainty down.
6. Save inside the project: `transcript.json` (`id`, `text`, `start`, `end` per word), `captions.srt` (on the final reel timeline), `source-analysis.md` (metadata, colour decision, silence map, method, uncertainty, semantic beats), `timing-map.json` (every retained source range → output start/end, frame-exact, plus removed ranges with reasons).

## 3. Editing style

### World A — restrained talking head
- Presenter dominant, clean hard cuts, three crop states: 1.00 base, ≈1.08 emphasis, ≈1.15 close. Change crop on a new claim, contrast, punchline, or payoff — not every sentence.
- Crop = scale on an **untimed wrapper** around the timed `<video>` clips, with the transform origin on the measured face point so eyes and chin stay fixed. Never animate the timed `.clip`.
- Natural colour only; no sharpening, no crushed blacks, no orange skin.

### World B — full-screen editorial interludes
- Warm paper ground, one strong monochrome symbolic object drawn in SVG/CSS and chosen from the transcript, huge Arabic keyword + small context, progressive assembly on the spoken words, readable hold, decisive cut.
- A different object per scene; no robots, neon brains, circuit boards, HUDs, particles, stock clips, invented screenshots, logos, or numbers the speaker didn't say.
- **The first frame of every interlude must already show the scene** (entrances that start at local t≈0 begin part-way revealed) — an empty paper frame on a hard cut reads as a mount flash.

## 4. Pacing and ratio
- ≈45–55 % presenter, ≈45–55 % interludes; interludes 1.8–4.5 s; boundaries chosen by meaning, never by a clock.
- Rhythm: presenter open 0.7–1.2 s → hard cut on the hook's claim → presenter for context → mechanism/contrast interlude → longest list interlude → presenter for the payoff → CTA.
- **Length:** state it explicitly. Either keep the whole argument with silence removal only (scene count ≈ one per 8 s), or cut to a 20–35 s reel with 4–6 scenes. (The delivered reel kept the full argument because every sentence carries a separate claim.)

## 5. Opening hook
- Frame 0 is the face, never black/logo/title. Push 1.00 → ≈1.12 over 0.55–0.85 s, `expo.out`, no bounce. First small caption during the push. First hard cut to an interlude on the strongest claim within 1–2 s.

## 6. Palette (personal, unbranded)
```css
--paper:#E9E0D3; --paper-dark:#D4C8B8; --paper-light:#F6F0E7; --cream:#FFFDF7;
--ink:#1B1D1E; --ink-soft:#3A3D3E; --accent-warm:#E66A21; --accent-warm-dark:#C85218;
--accent-cool:#2A8791; --accent-cool-dark:#216A72; --accent-gold:#D8A44A;
```
- Paper/cream/ink dominate; burnt orange is the main emphasis, teal rare, gold a micro-accent only.
- **Orange text on paper uses `--accent-warm-dark`** (≥ 3:1); `#E66A21` is for fills and strokes.

## 7. Arabic font
- Check the real inventory (`fc-list :lang=ar`, then `document.fonts.check()` in the preview). Preferred: Cairo, Tajawal, Noto Kufi Arabic, Noto Sans Arabic, IBM Plex Sans Arabic.
- If none is installed, install Cairo from the OFL Fontsource package (`npm i @fontsource/cairo`), copy the Arabic + Latin woff2 files (400–900) into `assets/fonts/`, and declare `@font-face` with their `unicode-range` in **every** file that uses it. Report this in the delivery note.
- Weights: 900 display, 800 captions/supporting, 700 labels. Never a synthesized weight.
- RTL everywhere (`dir="rtl"`), whole-word spans, no per-letter animation.
- **Reveal masks need room for Arabic dots and hamza**: `overflow:hidden` masks get extra padding above and below (≈0.2em / 0.36em with matching negative margins), or the dots under final «ي» get clipped.
- Write numbers as their own LTR-safe tokens; don't glue a small «لـ» to a big numeral (shaping breaks).

## 8. Captions (presenter sections only)
- Word-timed from the verified transcript; **hand-author the groups** as semantic 1–4-word chunks (machine grouping splits Arabic phrases badly).
- ≈61–68 % of frame height, over the torso, never over the face at any crop. Cairo 800, compact line height.
- Cream `#FFFDF8`; not-yet-spoken words at ≈55 %; one highlighted word (or one name/date unit) per group, warm accent; teal rarely. On footage use lighter tints of the accents so they stay ≥ 3:1.
- **If the clothing/background behind the captions is bright or busy**, put a feathered radial shadow behind each group (a soft dark glow sized to the text, transparent at the edges — not an opaque pill) so cream and accents keep contrast.
- 2–4-frame opacity/vertical settle; no bouncing karaoke or per-letter wobble.
- Interludes have no subtitle layer — the spoken phrase becomes the scene's typography, revealed at the spoken moment.

## 9. Semantic shot plan
Divide the transcript into beats (hook / input / list / contrast / payoff / CTA) and write `STORYBOARD.md` quoting the exact verified phrase driving each scene, with frame-snapped output times, crop states, and the A/B ratio.
- **If the speaker gives no spoken CTA**, the final card re-asks the speaker's own question with a short comment prompt, appears right after the last word, and holds ≥ 2 s fully built. Never end on black.

## 10. Motion
- 2–4 motion rules per scene: masked word rise, short stagger, scale settle, path/connector draw, small object pose change.
- Entrances 6–12 frames on long-tailed ease-outs; exits shorter; holds 10–20 frames; hard cuts over dissolves.
- No continuous random motion, glitch, liquid morphs, chrome text, particles, transition-pack variety, or reset tails.
- Seek-safe GSAP only: one paused timeline per composition registered on `window.__timelines`, `fromTo` everywhere, no `Date.now()` / `Math.random()` / timers / `repeat:-1`. **Use scene-unique ids for every GSAP selector** (scene scripts share one document; a shared class selector hits every scene).

## 11. Silence removal
- Remove leading/trailing dead air and set-up/tear-down. Internal pauses > ≈0.24 s → keep ≈3 frames after speech and ≈2 before the next word; keep a deliberate dramatic pause longer when it sets up a payoff. Never cut inside a syllable; check suspicious spots on a spectrogram.
- Separate `<video>` clips with `data-media-start` / `data-duration` / `data-start`, all on the frame grid; derive each duration from the rounded edges so neighbours abut exactly. Dialogue continues under interludes.

## 12. B-roll without B-roll
Build visuals from HTML/CSS/SVG and truthful abstract metaphors; frames from `rawreel` only if useful. No downloaded or scraped media, no fabricated evidence. If a factual visual would need an unavailable asset, use an abstract diagram or typography instead.

## 13. Audio
- Original dialogue is authoritative. Denoise only if the noise floor needs it (don't add artefacts to a clean lav). High-pass ≈70 Hz, gentle compression, two-pass loudnorm to ≈−14 LUFS integrated, ≤ −1 dBTP; check that any 0 dBFS peaks sit in sections that get cut.
- No music unless supplied. Optional soft SFX from the bundled `/media-use` set on 3–5 visible actions, well under the voice.

## 14. Implementation contract
1080×1920, native fps (else 30000/1001 and report it), H.264 + AAC MP4. Sub-composition per interlude, one captions host (`data-track-kind="captions"`), readable Studio lanes. Never animate `display`/`visibility`/`autoAlpha` on a `.clip`. Unique ids. Essential text inside x 80–1000, y 140–1650, and as far as possible inside the platform clear band `check` uses (≈ y 290–1250, x 120–888).

## 15. Verification
1. Write `BRIEF.md`, `source-analysis.md`, transcript artifacts, `STORYBOARD.md`, `timing-map.json`.
2. Build the full project; `npx hyperframes lint` after the first pass and after timing changes.
3. `npx hyperframes check --json` until 0 errors; fix contrast and overlap findings; justify every warning you keep.
4. `npx hyperframes keyframes` for the opening push and every crop change.
5. Snapshots: exact first frame; push at 0/25/50/75/100 %; every scene cut ±1 frame; first frame, midpoint, and completed state of every interlude; every list state; CTA hold; final frame. Then `npx hyperframes snapshot --review` (seams + phone sheets at 360 px) and write `REVIEW.md`.
6. Look for black flashes, empty first frames, missing-font frames, broken shaping, clipped dots, clipped captions, lingering scenes, reset tails, desync.
7. `npx hyperframes preview --background`, confirm it answers 200, give the preview URL, and **wait for approval**.
8. After approval: `npx hyperframes render --quality delivery --fps <fps> --sdr --format mp4 --strict -o final_reel.mp4`.
9. Verify with ffprobe (1080×1920, fps, H.264, AAC, non-zero size, duration = root `data-duration`), ebur128 loudness, blackdetect, decoded frames, and A/V sync (audio onsets vs planned word times).

## 16. Delivery report
Project folder, `final_reel.mp4`, `captions.srt`, `transcript.json`, `timing-map.json`, and a short report: original/final duration, removed ranges, scene count, actual A/B ratio, fonts and weights (and how the font was obtained), registry/media dependencies, validation status, kept warnings with reasons, transcript uncertainty.

## 17. Stop and report instead of pretending
No/ambiguous `rawreel.*`; undecodable media; materially uncertain Arabic transcript; no font that shapes Arabic correctly; skills/CLI not runnable; a factual visual that would require invented evidence; `check` errors still open.
