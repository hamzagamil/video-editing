"""Generate the HyperFrames project from timing-map.json + tools/plan.py + scene templates.

  index.html                    root: A-roll clips (muted, graded proxy), dialogue, crop states,
                                scene/overlay hosts, captions host, SFX, closing commentary
  compositions/captions.html    word-timed caption groups (presenter windows only)
  compositions/<scene>.html     from tools/scenes/<scene>.html

Template tokens: {{k:name}} / {{k:name:e}} = scene-local start / end of cue word `name`
(plan.CUES), {{w:N}} / {{w:N:e}} = word N, {{D}} = slot length, {{ID}} = scene id.
Usage: python3 -I tools/build.py
"""
import json, re, sys, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import plan  # noqa: E402

FPS = 30
tm = json.load(open(ROOT / "timing-map.json", encoding="utf-8"))
W = {int(w["id"][1:]): w for w in tm["words_output"]}
SPEECH_END = tm["output_duration_speech"]


def f(t):
    return round(round(t * FPS) / FPS, 4)


def wid(x):
    return plan.CUES[x] if isinstance(x, str) else x


def T(x):
    """resolve a time expression to output seconds"""
    if isinstance(x, (int, float)):
        return float(x)
    kind, ref, *rest = x
    off = rest[0] if rest else 0.0
    if kind == "w":
        return W[wid(ref)]["start"] + off
    if kind == "we":
        return W[wid(ref)]["end"] + off
    if kind == "speech_end":
        return SPEECH_END + float(ref)
    raise ValueError(x)


SCENES = []  # (sid, tpl, start, end, label, kind)
for s in plan.SCENES:
    sid, tpl, a, b, label = s[:5]
    kind = s[5] if len(s) > 5 else "page"
    SCENES.append((sid, tpl, f(T(a)), f(T(b)), label, kind))
TOTAL = f(max(e for _, _, _, e, _, _ in SCENES))

AR = ("U+0600-06FF,U+0750-077F,U+0870-088E,U+0890-0891,U+0897-08E1,U+08E3-08FF,U+200C-200E,"
      "U+2010-2011,U+204F,U+2E41,U+FB50-FDFF,U+FE70-FE74,U+FE76-FEFC")
LA = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
      "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")
FONT_CSS = ""
for wt in (500, 600, 700, 800, 900) if False else (400, 600, 700, 800, 900):
    FONT_CSS += (f"@font-face{{font-family:'Cairo';font-style:normal;font-weight:{wt};font-display:block;"
                 f"src:url('assets/fonts/cairo-arabic-{wt}-normal.woff2') format('woff2');unicode-range:{AR};}}\n")
    FONT_CSS += (f"@font-face{{font-family:'Cairo';font-style:normal;font-weight:{wt};font-display:block;"
                 f"src:url('assets/fonts/cairo-latin-{wt}-normal.woff2') format('woff2');unicode-range:{LA};}}\n")

PALETTE = ("--paper:#E9E0D3; --paper-dark:#D4C8B8; --paper-light:#F6F0E7; --cream:#FFFDF7; "
           "--ink:#1B1D1E; --ink-soft:#3A3D3E; --graphite:#5A5C5E; "
           "--accent-warm:#E66A21; --accent-warm-dark:#C85218; --sky:#75AADB; --sky-ink:#2F5F8A; "
           "--gold:#D8A44A; --pitch:#3F6B4A;")

PAGE_BG = """
  background-color:#E9E0D3;
  background-image:
    linear-gradient(90deg, transparent 989px, rgba(230,106,33,.28) 989px, rgba(230,106,33,.28) 991px, transparent 991px),
    repeating-linear-gradient(0deg, transparent 0 53px, rgba(27,29,30,.055) 53px 54px),
    repeating-linear-gradient(90deg, transparent 0 53px, rgba(27,29,30,.04) 53px 54px),
    radial-gradient(120% 85% at 50% 32%, #F6F0E7 0%, #E9E0D3 58%, #D9CCB9 100%);
"""

SCENE_BASE_CSS = """
#root { position:absolute; inset:0; overflow:hidden; direction:rtl; %s
  font-family:'Cairo', sans-serif; color:var(--ink); }
#root .grain { position:absolute; inset:0; width:1080px; height:1920px; mix-blend-mode:overlay; opacity:.32; pointer-events:none; }
#root .kicker { position:absolute; left:80px; right:80px; text-align:center; font-weight:700;
  font-size:46px; line-height:1.3; color:var(--ink-soft); }
#root .hero { position:absolute; left:70px; right:70px; text-align:center; font-weight:900;
  line-height:1.12; color:var(--ink); }
#root .lbl { position:absolute; font-weight:800; font-size:44px; line-height:1.2; color:var(--ink); }
#root .mask { display:block; overflow:hidden; padding:0.2em 0.06em 0.36em; margin:-0.1em -0.06em -0.2em; }
#root .mask.il { display:inline-block; }
#root .mask > .in { display:block; }
#root .w { display:inline-block; }
#root .warm { color:var(--accent-warm-dark); }
#root .sky { color:var(--sky-ink); }
#root .gold { color:#9C7426; }
#root .soft { color:var(--ink-soft); }
#root bdi, #root .ltr { unicode-bidi:isolate; direction:ltr; }
#root svg { position:absolute; overflow:visible; }
#root .print { position:absolute; background:var(--cream); padding:14px 14px 18px; box-shadow:0 10px 26px rgba(27,29,30,.22), 0 1px 0 rgba(27,29,30,.12); }
#root .print img { display:block; width:100%%; height:100%%; object-fit:cover; }
#root .print .tape { position:absolute; width:150px; height:42px; top:-20px; left:50%%; margin-left:-75px;
  background:rgba(236,224,196,.82); box-shadow:0 1px 2px rgba(27,29,30,.15); }
#root .stamp { position:absolute; font-weight:900; color:var(--accent-warm-dark); border:6px solid var(--accent-warm-dark);
  padding:2px 22px 10px; border-radius:10px; }
""" % ("",)

SCENE_JS = """
  const tl = gsap.timeline({ paused: true });
  const E0 = (t) => t < 0.06;
  const rise = (s, t, d = 0.34) => tl.fromTo(s, E0(t) ? { yPercent: 40, opacity: 0.6 } : { yPercent: 108, opacity: 0 }, { yPercent: 0, opacity: 1, duration: d, ease: "expo.out" }, t);
  const bin = (s, t, d = 0.16) => tl.fromTo(s, E0(t) ? { opacity: 0.55, filter: "blur(3px)" } : { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: d, ease: "power2.out" }, t);
  const bout = (s, t, d = 0.14) => tl.fromTo(s, { opacity: 1, filter: "blur(0px)" }, { opacity: 0, filter: "blur(8px)", duration: d, ease: "power2.in", immediateRender: false }, t);
  const draw = (s, t, d, e = "power2.inOut") => tl.fromTo(s, { strokeDashoffset: E0(t) ? 60 : 110 }, { strokeDashoffset: 0, duration: d, ease: e }, t);
  const pop = (s, t, d = 0.3) => tl.fromTo(s, { scale: E0(t) ? 0.6 : 0, transformOrigin: "50% 50%" }, { scale: 1, duration: d, ease: "expo.out" }, t);
  const fade = (s, t, to = 1, d = 0.2) => tl.fromTo(s, { opacity: E0(t) ? 0.5 : 0 }, { opacity: to, duration: d, ease: "power2.out" }, t);
  const off = (s, t, d = 0.12) => tl.fromTo(s, { opacity: 1 }, { opacity: 0, duration: d, ease: "power2.in", immediateRender: false }, t);
  const snapIn = (s, t, rot = -2) => tl.fromTo(s, { opacity: E0(t) ? 0.7 : 0, scale: 1.05, rotation: rot - 1.2, transformOrigin: "50% 40%" }, { opacity: 1, scale: 1, rotation: rot, duration: 0.18, ease: "power3.out" }, t);
  const slam = (s, t) => tl.fromTo(s, { opacity: 0, scale: 1.45, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.16, ease: "power4.out" }, t);
  const tint = (s, t, c, d = 0.12) => tl.fromTo(s, { color: "#1B1D1E" }, { color: c, duration: d, ease: "none", immediateRender: false }, t);
"""


def render_scene(sid, tpl, start, end, kind):
    src = (ROOT / "tools/scenes" / tpl).read_text(encoding="utf-8")
    dur = round(end - start, 4)

    def rep(m):
        kindtok, ref, e = m.group(1), m.group(2), m.group(3)
        n = plan.CUES[ref] if kindtok == "k" else int(ref)
        w = W[n]
        t = (w["end"] if e else w["start"]) - start
        if t < -0.001 or t > dur + 0.001:
            print(f"  ! {sid}: cue {ref} at local {t:.3f}s outside slot 0..{dur}")
        return f"{max(0.0, round(t, 3))}"
    src = re.sub(r"\{\{([kw]):([^:}]+)(:e)?\}\}", rep, src)
    src = re.sub(r"\{\{cv:([\d.]+)\}\}", lambda m: m.group(1), src)
    src = src.replace("{{grade}}", json.dumps(plan.PHOTO_GRADE).replace("'", "&#39;"))
    src = src.replace("{{D}}", f"{dur}").replace("{{ID}}", sid)
    m = re.search(r"<!--STYLE-->(.*?)<!--/STYLE-->", src, re.S)
    style = m.group(1) if m else ""
    body = re.sub(r"<!--STYLE-->.*?<!--/STYLE-->", "", src, flags=re.S)
    sm = re.search(r"<script>(.*?)</script>", body, re.S)
    script = sm.group(1) if sm else ""
    body = re.sub(r"<script>.*?</script>", "", body, flags=re.S)
    page = kind == "page"
    page_css = ("#root {" + PAGE_BG + "}\n") if page else ""
    grain = '    <img class="grain" src="assets/textures/paper-grain.png" alt="" aria-hidden="true" data-layout-ignore>\n' if page else ""
    html = f"""<template>
  <style>
{FONT_CSS}{SCENE_BASE_CSS}{page_css}{style}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{dur}" lang="ar" dir="rtl" style="{PALETTE}">
{grain}{body.strip()}
  </div>
  <script>{SCENE_JS}{script.rstrip()}
  window.__timelines["{sid}"] = tl;
  </script>
</template>
"""
    (ROOT / "compositions" / tpl).write_text(html, encoding="utf-8")
    return dur


def a_windows():
    """output windows where the presenter is the picture (pages cut him away; overlays don't)"""
    wins, t = [], 0.0
    for sid, tpl, s, e, _, kind in sorted(SCENES, key=lambda x: x[2]):
        if kind != "page":
            continue
        if s > t:
            wins.append((t, s))
        t = max(t, e)
    if t < SPEECH_END:
        wins.append((t, SPEECH_END))
    return [(a, min(b, SPEECH_END)) for a, b in wins if a < SPEECH_END]


def caption_groups():
    wins = a_windows()
    groups = []
    for ids in plan.CAPTIONS:
        ws = [W[n] for n in ids]
        win = next((w for w in wins if w[0] - 0.08 <= ws[0]["start"] < w[1]), None)
        if win is None:
            print("  ! caption group outside presenter windows:", " ".join(w["text"] for w in ws))
            continue
        groups.append({"words": ws, "win": win})
    for g in groups:
        g["start"] = f(max(g["win"][0], g["words"][0]["start"] - 0.04))
    for i, g in enumerate(groups):
        a, b = g["win"]
        nxt = groups[i + 1] if i + 1 < len(groups) else None
        end = min(g["words"][-1]["end"] + 0.35, b)
        if nxt and nxt["win"] == g["win"]:
            end = nxt["start"] if nxt["start"] - g["words"][-1]["end"] < 0.45 else min(end, nxt["start"])
        g["end"] = f(end)
    return groups


def render_captions():
    groups = caption_groups()
    items, script = [], []
    for i, g in enumerate(groups, 1):
        gid = f"c{i:02d}"
        chars = sum(len(plan.CAPTION_TEXT.get(int(w["id"][1:]), w["text"])) for w in g["words"]) + len(g["words"]) - 1
        size = max(60, min(88, int(900 / max(1, chars * 0.52))))
        spans = []
        for w in g["words"]:
            n = int(w["id"][1:])
            hl = plan.HL.get(n)
            cls = "cw" + (f" hl-{hl}" if hl else "")
            txt = plan.CAPTION_TEXT.get(n, w["text"]).strip(".,،")
            spans.append(f'<span id="{gid}-w{n}" class="{cls}">{txt}</span>')
        dur = round(g["end"] - g["start"], 4)
        items.append(f'    <div id="{gid}" class="cg clip" data-start="{g["start"]}" data-duration="{dur}" '
                     f'data-track-index="0" style="font-size:{size}px"><div id="{gid}-in" class="ci">'
                     + " ".join(spans) + "</div></div>")
        script.append(f'  tl.fromTo("#{gid}-in", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.1, ease:"power2.out"}}, {g["start"]});')
        for w in g["words"]:
            n = int(w["id"][1:])
            t = max(g["start"], round(w["start"], 3))
            col = {"o": "#FF8A3D", "s": "#9CCBF0", "g": "#FF8A3D"}.get(plan.HL.get(n))
            to = '{opacity:1, duration:0.067, ease:"none"' + (f', color:"{col}"' if col else "") + "}"
            frm = '{opacity:0.5' + (', color:"#FFFDF8"' if col else "") + "}"
            script.append(f'  tl.fromTo("#{gid}-w{n}", {frm}, {to}, {t});')
    html = f"""<template>
  <style>
{FONT_CSS}
#root {{ position:absolute; inset:0; pointer-events:none; }}
#root .cg {{ position:absolute; left:0; right:0; top:{plan.CAPTION_TOP}px; text-align:center; direction:rtl;
  font-family:'Cairo', sans-serif; font-weight:800; line-height:1.18; color:#FFFDF8; overflow:visible; }}
#root .ci {{ position:relative; isolation:isolate; display:inline-block; max-width:900px; padding:0 34px; }}
#root .ci::before {{ content:""; position:absolute; left:-70px; right:-70px; top:-34px; bottom:-30px; z-index:0;
  background: radial-gradient(closest-side, rgba(14,12,10,.62) 0%, rgba(14,12,10,.5) 52%, rgba(14,12,10,.2) 80%, rgba(14,12,10,0) 100%); }}
#root .cw {{ display:inline-block; opacity:.5; position:relative; z-index:1;
  text-shadow: 0 2px 3px rgba(12,10,8,.55), 0 0 14px rgba(12,10,8,.35); }}
#root .cw.hl-g {{ border-bottom:5px solid #D8A44A; padding-bottom:2px; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" lang="ar" dir="rtl">
{chr(10).join(items)}
  </div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
{chr(10).join(script)}
  window.__timelines["captions"] = tl;
  </script>
</template>
"""
    (ROOT / "compositions/captions.html").write_text(html, encoding="utf-8")
    return groups


def db(x):
    return round(10 ** (x / 20), 4)


def render_root():
    vids = []
    for s in tm["segments"]:
        vids.append(
            f'        <video id="{s["id"]}" class="clip aroll" src="assets/media/aroll.mp4" '
            f'data-start="{s["out_start"]}" data-duration="{s["duration"]}" data-media-start="{s["proxy_start"]}" '
            f'muted playsinline preload="auto" data-track-index="0"></video>')
    hosts = []
    for sid, tpl, s, e, label, kind in SCENES:
        z = 10 if kind == "page" else 7
        hosts.append(
            f'      <div id="{sid}" class="scene-host" data-composition-id="{sid}" data-composition-src="compositions/{tpl}" '
            f'data-start="{s}" data-duration="{round(e - s, 4)}" data-track-index="{2 if kind == "page" else 5}" data-track-kind="graphics" '
            f'data-width="1080" data-height="1920" title="{label}" style="z-index:{z}"></div>')
    sfx = []
    lanes = []  # simple lane packing for overlapping SFX
    for sid, file, at, gain_db, dur, extra in plan.SFX:
        t = f(T(at))
        d = round(f(T(dur[2])) - f(T(dur[1])), 4) if isinstance(dur, tuple) else round(dur, 4)
        lane = 0
        while any(l == lane and not (t >= e or t + d <= s) for l, s, e in lanes):
            lane += 1
        lanes.append((lane, t, t + d))
        sfx.append(f'      <audio id="{sid}" class="clip" src="assets/sfx/{file}" data-start="{t}" data-duration="{d}" '
                   f'data-volume="{db(gain_db)}" data-track-index="{7 + lane}"{extra}></audio>')
    cam = [f'  tl.set(cam, {{ transformOrigin: "{plan.FACE_ORIGIN}", scale: 1 }}, 0);',
           f'  tl.fromTo(cam, {{ scale: 1 }}, {{ scale: {plan.PUSH_TO}, duration: {plan.PUSH_DUR}, ease: "expo.out" }}, 0);']
    for at, sc in plan.CROP:
        cam.append(f'  tl.set(cam, {{ scale: {sc} }}, {f(T(at))});')
    vo = plan.CLOSING
    vo_t = f(T(vo["at"]))
    html = f"""<!doctype html>
<html lang="ar" dir="rtl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>هندسة الماتريكس — Messi reel</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{FONT_CSS}
      :root {{ {PALETTE} }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#1B1D1E; }}
      #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:#1B1D1E; }}
      #aroll-cam {{ position:absolute; left:0; top:0; width:1080px; height:1920px; z-index:1; }}
      #aroll-cam video {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
      .scene-host {{ position:absolute; inset:0; }}
      #captions {{ z-index:5; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-fps="30"
         data-width="1080" data-height="1920">
      <!-- World A: presenter. Untimed camera wrapper (crop states) around the timed source ranges (graded SDR proxy). -->
      <div id="aroll-cam">
{chr(10).join(vids)}
      </div>
      <!-- Dialogue: the same retained ranges, processed to -14 LUFS (tools/audio.py) -->
      <audio id="dialogue" class="clip" src="assets/media/dialogue.wav" data-start="0" data-duration="{SPEECH_END}" data-volume="1" data-track-index="1"></audio>
      <!-- Word-timed captions (presenter windows only) -->
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html"
           data-start="0" data-duration="{SPEECH_END}" data-track-index="3" data-track-kind="captions"
           data-width="1080" data-height="1920"></div>
      <!-- World B: notebook pages, plus overlay cards over the presenter -->
{chr(10).join(hosts)}
      <!-- SFX (Pixabay, prepared in ../sfx/prepared) -->
{chr(10).join(sfx)}
      <!-- Closing commentary clip (user-supplied) -->
      <audio id="closing-vo" class="clip" src="assets/sfx/{vo["file"]}" data-start="{vo_t}" data-duration="{vo["dur"]}" data-volume="{db(vo["gain_db"])}" data-track-index="6"></audio>
    </div>
    <script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  const cam = document.getElementById("aroll-cam");
{chr(10).join(cam)}
  tl.set({{}}, {{}}, {TOTAL});
  window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    (ROOT / "compositions").mkdir(exist_ok=True)
    for sid, tpl, s, e, _, kind in SCENES:
        render_scene(sid, tpl, s, e, kind)
    render_root()
    groups = render_captions()
    a_total = sum(b - a for a, b in a_windows())
    g_total = sum(e - s for _, _, s, e, _, k in SCENES if k == "page")
    print(f"total {TOTAL}s  speech {SPEECH_END}s  A-roll {a_total:.2f}s ({a_total/TOTAL*100:.1f}%)  pages {g_total:.2f}s ({g_total/TOTAL*100:.1f}%)")
    print(f"caption groups {len(groups)}")
    for sid, tpl, s, e, label, kind in SCENES:
        print(f"  {sid:<5} {s:7.3f}-{e:7.3f} ({e-s:5.2f}s) {kind:<7} {label}")
