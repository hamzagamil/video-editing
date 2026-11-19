# Brief

Arabic 9:16 reel about Messi's football brain, cut from one talking-head recording (`../source/rawreel.mov`,
iPhone HLG HDR, 13.5 min) following `../hyperframes-reel-edit/PROMPT_MESSI.md`.

- Delivery: 1080×1920, 30 fps, H.264 + AAC, HyperFrames as the source of truth.
- Presenter look: HLG → SDR (hable) + natural correction; crop states 1.00 / 1.08 / 1.15 around the face.
- Pages: "The Engineer's Notebook" — warm graph paper, graphite lines, Cairo 700–900, orange (Messi),
  ink (defenders), dashed sky (the future), gold as a micro-accent.
- Photos: 8 user-supplied images, screen-printed (media-treatment Monochrome Screen Print), ≤ 1.2 s each.
- Sound: dialogue −14.5 LUFS; Pixabay SFX tied to visible actions; user-supplied Chawali clip to close.
- Truth: nothing on screen the speaker did not say (`FACT_CHECK.md`).

Build: `python3 -I tools/cut.py && python3 -I tools/audio.py && python3 -I tools/build.py && python3 -I tools/make_srt.py`
(the graded A-roll proxy `assets/media/aroll.mp4` is rendered from `../source/work/clips/`, see `source-analysis.md`).
