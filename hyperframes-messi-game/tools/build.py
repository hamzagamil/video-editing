"""Generate the HyperFrames project from timing-map.json + tools/plan.py + scene templates.

  index.html                    root: A-roll clips (muted, graded proxy), dialogue, crop states,
                                scene/overlay hosts, captions host, SFX, closing commentary
  compositions/captions.html    word-timed caption groups (presenter windows only)
  compositions/<scene>.html     from tools/scenes/<scene>.html

Template tokens: {{k:name}} / {{k:name:e}} = scene-local start / end of cue word `name`
(plan.CUES), {{w:N}} / {{w:N:e}} = word N, {{D}} = slot length, {{ID}} = scene id.
Usage: python3 -I tools/build.py
"""
import json, subprocess, re, sys, math
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

FONT_CSS += ("@font-face{font-family:'PS2P';font-style:normal;font-weight:400;font-display:block;"
             "src:url('assets/fonts/press-start-2p-latin-400-normal.woff2') format('woff2');}\n")

PALETTE = ("--bg:#0E1424; --bg-2:#162036; --grid:#22304D; --pitch:#1E5A36; --pitch-2:#246B40; --line:#D9F2E4; "
           "--p1:#FF7A1A; --p1-dark:#C2540A; --npc:#8A93A8; --npc-dark:#4A5268; --future:#46D7FF; "
           "--future-dark:#1B8FB3; --gold:#FFC845; --alert:#FF4D5E; --text:#FFF6E5; --text-dim:#AEB7C9;")

PAGE_BG = """
  background-color:#0E1424;
  background-image:
    repeating-linear-gradient(0deg, rgba(255,255,255,.028) 0 2px, transparent 2px 6px),
    repeating-linear-gradient(0deg, transparent 0 39px, rgba(70,215,255,.06) 39px 40px),
    repeating-linear-gradient(90deg, transparent 0 39px, rgba(70,215,255,.06) 39px 40px),
    radial-gradient(120% 80% at 50% 38%, #18233D 0%, #0E1424 70%, #0A0F1C 100%);
"""

SCENE_BASE_CSS = """
#root { position:absolute; inset:0; overflow:hidden; direction:rtl;
  font-family:'Cairo', sans-serif; color:var(--text); }
#root .px { font-family:'PS2P', monospace; direction:ltr; unicode-bidi:isolate; letter-spacing:0; }
#root .hero { position:absolute; left:70px; right:70px; text-align:center; font-weight:900; line-height:1.15;
  color:var(--text); text-shadow: 6px 6px 0 #0A0F1C; }
#root .kicker { position:absolute; left:80px; right:80px; text-align:center; font-weight:800;
  font-size:48px; line-height:1.3; color:var(--text-dim); text-shadow: 4px 4px 0 #0A0F1C; }
#root .lbl { position:absolute; font-weight:800; font-size:42px; line-height:1.2; color:var(--text); text-shadow: 4px 4px 0 #0A0F1C; }
#root .mask { display:block; overflow:hidden; padding:0.2em 0.06em 0.36em; margin:-0.1em -0.06em -0.2em; }
#root .mask.il { display:inline-block; }
#root .mask > .in { display:block; }
#root .w { display:inline-block; }
#root .p1c { color:var(--p1); }
#root .fut { color:var(--future); }
#root .gld { color:var(--gold); }
#root .npcc { color:var(--npc); }
#root .red { color:var(--alert); }
#root .dim { color:var(--text-dim); }
#root bdi, #root .ltr { unicode-bidi:isolate; direction:ltr; }
#root svg { position:absolute; overflow:visible; shape-rendering:crispEdges; }
#root svg text { shape-rendering:auto; }
/* pixel dialog box: notched corners + hard drop shadow */
#root .box { position:absolute; background:var(--bg-2); color:var(--text); text-align:center;
  box-shadow: 0 -8px 0 0 var(--text), 0 8px 0 0 var(--text), -8px 0 0 0 var(--text), 8px 0 0 0 var(--text),
              8px 16px 0 0 #05080F, 16px 8px 0 0 #05080F, 16px 16px 0 0 #05080F; }
#root .box.gold { box-shadow: 0 -8px 0 0 var(--gold), 0 8px 0 0 var(--gold), -8px 0 0 0 var(--gold), 8px 0 0 0 var(--gold),
              8px 16px 0 0 #05080F, 16px 8px 0 0 #05080F, 16px 16px 0 0 #05080F; }
#root .box.p1 { box-shadow: 0 -8px 0 0 var(--p1), 0 8px 0 0 var(--p1), -8px 0 0 0 var(--p1), 8px 0 0 0 var(--p1),
              8px 16px 0 0 #05080F, 16px 8px 0 0 #05080F, 16px 16px 0 0 #05080F; }
#root .box.npc { box-shadow: 0 -8px 0 0 var(--npc), 0 8px 0 0 var(--npc), -8px 0 0 0 var(--npc), 8px 0 0 0 var(--npc),
              8px 16px 0 0 #05080F, 16px 8px 0 0 #05080F, 16px 16px 0 0 #05080F; }
#root .box.red { box-shadow: 0 -8px 0 0 var(--alert), 0 8px 0 0 var(--alert), -8px 0 0 0 var(--alert), 8px 0 0 0 var(--alert),
              8px 16px 0 0 #05080F, 16px 8px 0 0 #05080F, 16px 16px 0 0 #05080F; }
#root .box .hero, #root .box .kicker { position:static; text-shadow:none; }
#root .tag { position:absolute; font-family:'PS2P', monospace; direction:ltr; unicode-bidi:isolate; font-size:28px; line-height:1;
  padding:12px 14px 10px; color:#0E1424; background:var(--p1); box-shadow: 6px 6px 0 #05080F; white-space:nowrap; }
#root .tag.npc { background:var(--npc); }
#root .tag.fut { background:var(--future); }
#root .tag.gold { background:var(--gold); }
#root .tag.red { background:var(--alert); color:#FFF6E5; }
#root .tag.dark { background:#0E1424; color:var(--text-dim); box-shadow: 0 0 0 4px var(--grid); }
/* the in-game viewport: a pixel pitch inside a frame */
#root .view { position:absolute; left:80px; width:920px; overflow:hidden; background-color:var(--pitch);
  background-image: repeating-linear-gradient(0deg, var(--pitch) 0 80px, var(--pitch-2) 80px 160px);
  box-shadow: 0 0 0 8px var(--text), 0 0 0 16px #0E1424, 16px 16px 0 8px #05080F; }
#root .view.dark { background-color:#0A0F1C; background-image: repeating-linear-gradient(0deg, transparent 0 39px, rgba(70,215,255,.10) 39px 40px), repeating-linear-gradient(90deg, transparent 0 39px, rgba(70,215,255,.10) 39px 40px); }
#root .view svg { left:0; top:0; }
/* HUD top bar shared by the game screens */
#root .hud { position:absolute; left:140px; right:190px; top:292px; height:56px; }
#root .hud .tag { top:0; }
#root .hud .p1t { right:0; }
#root .hud .mode { left:0; }
#root .hud .nm { position:absolute; right:110px; top:-6px; font-weight:800; font-size:40px; color:var(--text); text-shadow:4px 4px 0 #05080F; }
/* game cards for photos */
#root .card { position:absolute; background:#0E1424; padding:12px; box-shadow: 0 0 0 8px var(--text), 0 0 0 16px #0E1424, 14px 14px 0 8px #05080F; }
#root .card img { display:block; width:100%%; height:100%%; object-fit:cover; image-rendering:pixelated; }
#root .card .tag { top:-30px; right:12px; }
""" % ()

SCENE_JS = """
  const tl = gsap.timeline({ paused: true });
  const E0 = (t) => t < 0.06;
  const rise = (s, t, d = 0.3) => tl.fromTo(s, E0(t) ? { yPercent: 40, opacity: 0.6 } : { yPercent: 108, opacity: 0 }, { yPercent: 0, opacity: 1, duration: d, ease: "steps(5)" }, t);
  const bin = (s, t, d = 0.1) => tl.fromTo(s, { opacity: E0(t) ? 0.6 : 0 }, { opacity: 1, duration: d, ease: "steps(2)" }, t);
  const off = (s, t, d = 0.07) => tl.fromTo(s, { opacity: 1 }, { opacity: 0, duration: d, ease: "steps(2)", immediateRender: false }, t);
  const pop = (s, t, d = 0.2) => tl.fromTo(s, { scale: E0(t) ? 0.6 : 0, transformOrigin: "50% 50%" }, { scale: 1, duration: d, ease: "steps(4)" }, t);
  const fade = (s, t, to = 1, d = 0.16) => tl.fromTo(s, { opacity: E0(t) ? 0.5 : 0 }, { opacity: to, duration: d, ease: "steps(3)" }, t);
  const slam = (s, t) => tl.fromTo(s, { opacity: 0, scale: 1.5, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.14, ease: "steps(4)" }, t);
  const draw = (s, t, d, e = "steps(8)") => tl.fromTo(s, { strokeDashoffset: E0(t) ? 50 : 100 }, { strokeDashoffset: 0, duration: d, ease: e }, t);
  // stepped sprite move (12-15 sprite fps feel): n steps over d seconds
  const step = (s, t, to, d, n) => tl.to(s, Object.assign({ duration: d, ease: "steps(" + (n || Math.max(2, Math.round(d * 12))) + ")", immediateRender: false }, to), t);
  // words revealed one by one (never letters): list of [selector, time]
  const typeW = (pairs) => pairs.forEach(([s, t]) => bin(s, t, 0.06));
  // finite blink: n blinks with a period
  const blink = (s, t, n, per = 0.36) => { for (let i = 0; i < n; i++) { tl.set(s, { opacity: 0 }, t + i * per + per / 2); tl.set(s, { opacity: 1 }, t + (i + 1) * per); } };
  const card = (s, t) => tl.fromTo(s, { opacity: E0(t) ? 0.7 : 0, scale: 1.04 }, { opacity: 1, scale: 1, duration: 0.15, ease: "steps(3)" }, t);
  // reveal the children of a group one after another over d seconds (dashed paths, rings, crowds)
  const seq = (q, t, d) => { const n = document.querySelectorAll(q).length || 1; tl.fromTo(q, { opacity: 0 }, { opacity: 1, duration: 0.001, ease: "none", stagger: { each: d / n } }, t); };
  const toast = (s, t) => tl.fromTo(s, { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.18, ease: "steps(4)" }, t);
"""

# ---------------------------------------------------------------- pixel sprites (built at build time as SVG rects)
SPR = {
    "player": [
        "....hhhh....",
        "...hhhhhh...",
        "...hssssh...",
        "...ssssss...",
        "....ssss....",
        "..TTTTTTTT..",
        ".sTTTTTTTTs.",
        ".sTTttttTTs.",
        "..TTTTTTTT..",
        "...wwwwww...",
        "...ww..ww...",
        "...ss..ss...",
        "..kkk..kkk..",
    ],
    "keeper": [
        "....hhhh....",
        "...hhhhhh...",
        "...hssssh...",
        "...ssssss...",
        "....ssss....",
        "..TTTTTTTT..",
        "gTTTTTTTTTTg",
        "g.TTttttTT.g",
        "..TTTTTTTT..",
        "...wwwwww...",
        "...ww..ww...",
        "...ss..ss...",
        "..kkk..kkk..",
    ],
    "ball": [".WW.", "WKWW", "WWKW", ".WW."],
    "star": [
        "....Y....",
        "....Y....",
        "...YYY...",
        "YYYYYYYYY",
        ".YYYYYYY.",
        "..YYYYY..",
        "..YY.YY..",
        ".YY...YY.",
        ".Y.....Y.",
    ],
    "x": ["R.....R", ".R...R.", "..R.R..", "...R...", "..R.R..", ".R...R.", "R.....R"],
    "eye": ["..WWWWW..", ".WWWWWWW.", "WWWKKKWWW", "WWWKKKWWW", "WWWKKKWWW", ".WWWWWWW.", "..WWWWW.."],
}
VARIANTS = {
    "p1": {"T": "#FF7A1A", "t": "#C2540A", "w": "#FFF6E5"},
    "npc": {"T": "#8A93A8", "t": "#4A5268", "w": "#22304D"},
    "mate": {"T": "#FFF6E5", "t": "#AEB7C9", "w": "#22304D"},
    "keeper": {"T": "#4A5268", "t": "#22304D", "w": "#22304D", "g": "#AEB7C9"},
}
BASE = {"h": "#2B2027", "s": "#D9A17A", "k": "#0E1424", "W": "#FFF6E5", "K": "#0E1424", "Y": "#FFC845", "R": "#FF4D5E"}


def sprite(name, sid, x, y, px, variant="p1", outline=True):
    rows = SPR[name]
    ghost = variant == "ghost"
    col = dict(BASE)
    col.update(VARIANTS.get("p1" if ghost else variant, {}))
    filled = {(c, r) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch != "."}
    out = []
    if outline:
        oc = "#1B8FB3" if ghost else "#0A0F1C"
        ring = {(c + dc, r + dr) for c, r in filled for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1))} - filled
        out += [f'<rect x="{c*px}" y="{r*px}" width="{px}" height="{px}" fill="{oc}"/>' for c, r in sorted(ring)]
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            fill = "#46D7FF" if ghost else col.get(ch, "#FF00FF")
            out.append(f'<rect x="{c*px}" y="{r*px}" width="{px}" height="{px}" fill="{fill}"/>')
    op = ' opacity=".6"' if ghost else ""
    return f'<g id="{sid}" transform="translate({x} {y})"{op}>' + "".join(out) + "</g>"


def dash(sid, x1, y1, x2, y2, color, w=8, seg=16, gap=12):
    import math as _m
    L = _m.hypot(x2 - x1, y2 - y1)
    n = max(1, int((L + gap) // (seg + gap)))
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    out = []
    for i in range(n):
        a = i * (seg + gap)
        b = min(L, a + seg)
        out.append(f'<line x1="{round(x1+ux*a)}" y1="{round(y1+uy*a)}" x2="{round(x1+ux*b)}" y2="{round(y1+uy*b)}" '
                   f'stroke="{color}" stroke-width="{w}" stroke-linecap="square"/>')
    return f'<g id="{sid}">' + "".join(out) + "</g>"


def ring(sid, cx, cy, r, color, sz=10, n=None):
    import math as _m
    n = n or max(12, int(2 * _m.pi * r / (sz * 2.4)))
    out = []
    for i in range(n):
        a = 2 * _m.pi * i / n - _m.pi / 2
        x = round((cx + r * _m.cos(a)) / 4) * 4 - sz // 2
        y = round((cy + r * _m.sin(a)) / 4) * 4 - sz // 2
        out.append(f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{color}"/>')
    return f'<g id="{sid}">' + "".join(out) + "</g>"


def expand_sprites(src):
    src = re.sub(r"\{\{dash:([^}]+)\}\}", lambda m: (lambda p: dash(p[0], *map(int, p[1:5]), p[5], *map(int, p[6:])))(m.group(1).split(":")), src)
    src = re.sub(r"\{\{ring:([^}]+)\}\}", lambda m: (lambda p: ring(p[0], *map(int, p[1:4]), p[4], *map(int, p[5:])))(m.group(1).split(":")), src)
    def rep(m):
        parts = m.group(1).split(":")
        name, sid, x, y, px = parts[:5]
        var = parts[5] if len(parts) > 5 else "p1"
        return sprite(name, sid, int(x), int(y), int(px), var)
    return re.sub(r"\{\{spr:([^}]+)\}\}", rep, src)


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
    src = expand_sprites(src)
    m = re.search(r"<!--STYLE-->(.*?)<!--/STYLE-->", src, re.S)
    style = m.group(1) if m else ""
    body = re.sub(r"<!--STYLE-->.*?<!--/STYLE-->", "", src, flags=re.S)
    sm = re.search(r"<script>(.*?)</script>", body, re.S)
    script = sm.group(1) if sm else ""
    body = re.sub(r"<script>.*?</script>", "", body, flags=re.S)
    page = kind == "page"
    page_css = ("#root {" + PAGE_BG + "}\n") if page else ""
    grain = ""
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
        script.append(f'  tl.fromTo("#{gid}-in", {{opacity:0, y:12}}, {{opacity:1, y:0, duration:0.1, ease:"steps(3)"}}, {g["start"]});')
        for w in g["words"]:
            n = int(w["id"][1:])
            t = max(g["start"], round(w["start"], 3))
            col = {"o": "#FF8A3D", "s": "#5FDCFF", "g": "#FF8A3D"}.get(plan.HL.get(n))
            to = '{opacity:1, duration:0.067, ease:"none"' + (f', color:"{col}"' if col else "") + "}"
            frm = '{opacity:0.5' + (', color:"#FFF6E5"' if col else "") + "}"
            script.append(f'  tl.fromTo("#{gid}-w{n}", {frm}, {to}, {t});')
    html = f"""<template>
  <style>
{FONT_CSS}
#root {{ position:absolute; inset:0; pointer-events:none; }}
#root .cg {{ position:absolute; left:0; right:0; top:{plan.CAPTION_TOP}px; text-align:center; direction:rtl;
  font-family:'Cairo', sans-serif; font-weight:800; line-height:1.18; color:#FFF6E5; overflow:visible; }}
#root .ci {{ position:relative; isolation:isolate; display:inline-block; max-width:900px; padding:0 34px; }}
#root .ci::before {{ content:""; position:absolute; left:-70px; right:-70px; top:-34px; bottom:-30px; z-index:0;
  background: radial-gradient(closest-side, rgba(10,15,28,.62) 0%, rgba(10,15,28,.5) 52%, rgba(10,15,28,.2) 80%, rgba(10,15,28,0) 100%); }}
#root .cw {{ display:inline-block; opacity:.5; position:relative; z-index:1;
  text-shadow: 4px 4px 0 #0A0F1C, 0 0 14px rgba(10,15,28,.35); }}
#root .cw.hl-g {{ border-bottom:8px solid #FFC845; padding-bottom:0; }}
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
    # the presenter edit is baked into one continuous clip by tools/aroll_edit.py (segments + freeze
    # patches): 120 seeks into one proxy made the renderer drop the first frame of some clips.
    stills = ROOT / "assets/media/stills"
    stills.mkdir(parents=True, exist_ok=True)
    for fz in tm.get("freezes", []):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(fz["still_proxy"]), "-i",
                        str(ROOT / "assets/media/aroll.mp4"), "-frames:v", "1", "-q:v", "1",
                        str(stills / f'{fz["id"]}.jpg')], check=True)
    vids = [f'        <video id="aroll" class="clip aroll" src="assets/media/aroll_edit.mp4" data-start="0" '
            f'data-duration="{SPEECH_END}" data-media-start="0" muted playsinline preload="auto" data-track-index="0"></video>']
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
    <title>ميسي: اللاعب رقم 1</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{FONT_CSS}
      :root {{ {PALETTE} }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0E1424; }}
      #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:#0E1424; }}
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
      <!-- World B: full-screen game screens, plus overlay cards over the presenter -->
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
