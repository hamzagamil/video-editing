# BRIEF — Hossam Hassan exit reel (Arabic, 9:16)

## Source
- `../rawreel.mov` (never modified; read-only copy of the supplied `IMG_9154.MOV`).
- One presenter, locked-off medium shot, Egyptian Arabic monologue (~100 s of speech inside a 111.9 s take).
- iPhone HLG HDR (HEVC Main10, BT.2020/ARIB STD-B67), rotated −90° → displayed 2160×3840, 30 fps.

## Deliverable
- 1080×1920, 30 fps (source-native), H.264 + AAC MP4 → `final_reel.mp4` (only after Studio approval).
- HyperFrames is the source of truth: root `index.html`, one sub-composition per graphic scene,
  one caption host, A-roll as source-range `<video>` clips.

## Story (what the speaker says)
Hossam Hassan went from Egyptian football legend to the coach who took the national team to
the World Cup — then left "through the narrow door" on 7 November. The speaker asks how a coach
whose contract ran to 2030 could suddenly go: technical reasons, or off-pitch problems bigger
than he could control? He lists the crises (criticism and substitution of Mohamed Salah vs
Angola, Salah leaving the camp, statements about Mohamed El-Shenawy that cost him fans, a
three-match FIFA ban after the Argentina match at the World Cup, personal-life issues turning
into a media and institutional crisis), asks whether the FA (El-Gabalaya) decided it was not in
the team's interest and dismissed him with his whole staff, and names Ali Maher as the
replacement.

## Edit intent
- Tight silence-trimmed cut (hard cuts only), presenter ↔ full-screen editorial interludes,
  ~50/50, scene boundaries chosen by meaning, not a clock.
- Hook: presenter + fast push-in on "حسام حسن", hard cut to the first editorial scene on
  "أسطورة الكرة المصرية" (~1.0 s).
- World A (presenter): natural SDR conversion of the HLG footage, three crop states
  (1.00 / ~1.08 / ~1.15), motivated punches on new claims; small 1–4-word captions at ~66% height.
- World B (interludes): warm paper ground, one monochrome symbolic object per scene drawn in
  SVG/CSS from the transcript (route + cup, nameplate, contract, fork, substitution board,
  microphone + crowd share, red card + match slots, escalation rings, dismissal roster,
  comment bubble). Huge Arabic keyword + small context; progressive assembly on the spoken word.
- Palette: paper `#E9E0D3` / cream / ink, burnt orange main accent, muted teal rare, gold micro.
- No logos, brand, watermark, music, stock footage, or invented facts. Voice-only audio,
  normalized to −14 LUFS / ≤ −1 dBTP.
- The speaker gives no spoken CTA; the closing card re-asks his own question
  ("فني ولا خارج الملعب؟") with a comment prompt, after the last spoken word.
