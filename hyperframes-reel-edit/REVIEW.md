# REVIEW — pre-render (Studio approval gate)

## Creative calls
- Kept the whole argument (≈77.7 s of speech after silence removal) rather than cutting it to a
  20–35 s reel: every sentence carries a distinct claim, and the brief forbids dropping factual
  claims. Scene count scaled with length: 9 interludes + CTA card (≈ one per 8 s).
- Cut the pre-roll greeting «مساء الخير» (spoken while sitting down, frame unsettled) so frame 0 is
  the face on «حسام حسن». Ends on «علي ماهر»; the trailing «و… طيب» is cut.
- The speaker never says a CTA. The closing card re-asks his own question (فني؟ ولا خارج الملعب؟)
  with «اكتب رأيك في التعليقات». It appears after the last word and holds 2.0 s fully built.
- Footage is HLG HDR; converted to SDR BT.709 (plain transfer conversion beat three tonemaps on
  skin and contrast). No further grade — the look stays natural, no sharpening.
- Captions use a feathered radial shadow (not a pill) because the shirt's white stripes made cream
  and orange unreadable without it (contrast fixed from 1.4:1 to ≥ 3:1 in `check`).
- Orange text on paper uses `--accent-warm-dark` (#C85218, 3.4:1); `#E66A21` stays for fills and
  strokes. Teal appears only in 4 caption highlights; gold only on the cup rim and CTA dots.

## Measured
- `hyperframes check`: ok — 0 errors (lint, runtime, layout, motion, contrast, craft, audio).
- Keyframes: opening push 1.00 → 1.12, 0.70 s expo.out, then hard crop sets at 15 cut points.
- Snapshots: first frame; push at 0/25/50/75/100 %; every scene cut ±1 frame (19 seams); first
  frame + midpoint of every interlude; `snapshot --review` (53 seams, phone sheets at 360 px).
- Audio (source chain): −14.0 LUFS integrated, speech peaks −1.5 dBTP. Final mix to be re-measured
  on the rendered file. The sound was measured, not heard.

## Looked at only
- Arabic shaping/joining on every hero word (Cairo, local woff2); dot clearance under final «ي».
- Jump cuts inside presenter sections: small head/hand shifts, normal for a silence-trimmed
  locked-off take; crop punches sit on several of them.

## Warnings kept on purpose
- `timeline_track_too_dense` (captions.html, 38 groups): one caption host holds every group, as
  the captions reference prescribes.
- `outside_safe_zone` on the caption band: captions sit at 61–67 % height as the brief requires;
  that edges below the strict Reels/Shorts clear band (65 %). Essential scene text is inside
  y≈290–1310.

## Weakest shot / with more time
- G1 middle (1.0–2.4 s) is sparse: the hero word and one route node while the route waits for
  «لمدرب». With more time I would start the route a beat earlier.
- G8 rings are the most abstract metaphor; they read as "spreading", but a stranger may need the
  words.
