"""Generate the HyperFrames project files from timing-map.json + scene templates.

- index.html            root: A-roll source ranges, crop states, scene hosts, captions host, SFX
- compositions/captions.html   word-timed caption groups for every presenter window
- compositions/gN-*.html        scenes from tools/scenes/gN-*.html; {{wN}} / {{wNe}} become the
                                scene-local start / end of transcript word N, {{D}} the slot length

The output is plain static HyperFrames HTML (editable in Studio); rerun after timing changes.
Usage: python3 -I tools/build.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FPS = 30
tm = json.load(open(ROOT / "timing-map.json"))
W = {int(w["id"][1:]): w for w in tm["words_output"]}
SPEECH_END = tm["output_duration_speech"]

def f(t):  # snap to frame grid
    return round(round(t * FPS) / FPS, 4)

# ---------------------------------------------------------------- scenes (output seconds)
SCENES = [
    # id, template, start, end, label
    ("g1", "g1-legend.html", f(22 / FPS), f(151 / FPS), "Route to the cup"),
    ("g2", "g2-armband.html", f(249 / FPS), f(389 / FPS), "Armband: spirit and resolve"),
    ("g3", "g3-contract.html", f(569 / FPS), f(650 / FPS), "Contract to 2030"),
    ("g4", "g4-fork.html", f(697 / FPS), f(796 / FPS), "Fork: technical or off-pitch"),
    ("g5", "g5-subboard.html", f(1005 / FPS), f(1134 / FPS), "Crisis 1: Salah substitution"),
    ("g6", "g6-statements.html", f(1230 / FPS), f(1333 / FPS), "Crisis 2: statements"),
    ("g7", "g7-ban.html", f(1478 / FPS), f(1586 / FPS), "Crisis 3: FIFA ban"),
    ("g8", "g8-rings.html", f(1772 / FPS), f(1883 / FPS), "Crisis 4: escalation"),
    ("g9", "g9-roster.html", f(2058 / FPS), f(2198 / FPS), "Dismissal roster"),
    ("g10", "g10-cta.html", f(2332 / FPS), f(2410 / FPS), "CTA card"),
]
TOTAL = f(2410 / FPS)

# ---------------------------------------------------------------- crop states (A-roll)
# (output time, scale, ease) — scale of the camera wrapper around the face point.
CROP = [
    (0.0, 1.00, "push"),          # opening push 1.00 → 1.12
    (f(151 / FPS), 1.08, None),   # A1 "إلى الخروج…"
    (f(389 / FPS), 1.00, None),   # A2 "انتهت رحلته…"
    (f(493 / FPS), 1.08, None),   # A3 "السؤال هنا"
    (f(650 / FPS), 1.15, None),   # A4 "يمشي فجأة؟"
    (f(796 / FPS), 1.00, None),   # A5 "كانت أكبر…"
    (f(871 / FPS), 1.08, None),   # A6 "الأزمات…"
    (f(1134 / FPS), 1.00, None),  # A7 "وبعدها محمد صلاح…"
    (f(1333 / FPS), 1.08, None),  # A8 "خسّرته…"
    (f(1438 / FPS), 1.15, None),  #    punch "وفوق كل ده"
    (f(1586 / FPS), 1.00, None),  # A9 "بعد أحداث…"
    (f(1663 / FPS), 1.08, None),  # A10 "زاد عليها…"
    (f(1883 / FPS), 1.00, None),  # A11 "هل اضطرت الجبلاية…"
    (f(1971 / FPS), 1.08, None),  #    punch "إن ده مش من مصلحة"
    (f(2198 / FPS), 1.00, None),  # A12 "والبديل…"
    (f(2309 / FPS), 1.15, None),  #    punch "علي ماهر"
]
FACE_ORIGIN = "48% 45.8%"

# ---------------------------------------------------------------- caption highlights
HL = {18: "o", 20: "t", 21: "t", 39: "o", 40: "o", 53: "o", 69: "t", 71: "o",
      89: "o", 102: "o", 118: "t", 125: "o", 136: "o", 145: "t", 159: "o", 160: "o"}

SFX = [  # id, file, output time, volume
    ("sfx-cup", "assets/sfx/click-soft.mp3", None, 0.20),
    ("sfx-board", "assets/sfx/click-soft.mp3", None, 0.20),
    ("sfx-stamp", "assets/sfx/click-soft.mp3", None, 0.24),
    ("sfx-cta", "assets/sfx/pop.mp3", None, 0.16),
]

FONT_CSS = ""
AR = ("U+0600-06FF,U+0750-077F,U+0870-088E,U+0890-0891,U+0897-08E1,U+08E3-08FF,U+200C-200E,"
      "U+2010-2011,U+204F,U+2E41,U+FB50-FDFF,U+FE70-FE74,U+FE76-FEFC")
LA = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
      "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")
for wt in (400, 600, 700, 800, 900):
    FONT_CSS += (f"@font-face{{font-family:'Cairo';font-style:normal;font-weight:{wt};font-display:block;"
                 f"src:url('assets/fonts/cairo-arabic-{wt}-normal.woff2') format('woff2');unicode-range:{AR};}}\n")
    FONT_CSS += (f"@font-face{{font-family:'Cairo';font-style:normal;font-weight:{wt};font-display:block;"
                 f"src:url('assets/fonts/cairo-latin-{wt}-normal.woff2') format('woff2');unicode-range:{LA};}}\n")

PALETTE = """
  --paper:#E9E0D3; --paper-dark:#D4C8B8; --paper-light:#F6F0E7; --cream:#FFFDF7;
  --ink:#1B1D1E; --ink-soft:#3A3D3E; --accent-warm:#E66A21; --accent-warm-dark:#C85218;
  --accent-cool:#2A8791; --accent-cool-dark:#216A72; --accent-gold:#D8A44A;
"""

# ---------------------------------------------------------------- scene files
SCENE_BASE_CSS = """
#root { position:absolute; inset:0; overflow:hidden; direction:rtl; %s
  background: radial-gradient(120%% 85%% at 50%% 30%%, #F6F0E7 0%%, #E9E0D3 56%%, #DACDBB 100%%);
  font-family:'Cairo', sans-serif; color:var(--ink); }
#root .sheet { position:absolute; inset:46px; border:2px solid rgba(27,29,30,.09); border-radius:4px; }
#root .kicker { position:absolute; left:80px; right:80px; text-align:center; font-weight:700;
  font-size:46px; line-height:1.3; color:var(--ink-soft); }
#root .hero { position:absolute; left:70px; right:70px; text-align:center; font-weight:900;
  line-height:1.12; color:var(--ink); }
#root .mask { display:block; overflow:hidden; padding:0.2em 0.06em 0.36em; margin:-0.1em -0.06em -0.2em; }
#root .mask > .in { display:block; }
#root .w { display:inline-block; }
#root .warm { color:var(--accent-warm); }
#root .cool { color:var(--accent-cool); }
#root .warmd { color:var(--accent-warm-dark); }
#root .tag { position:absolute; top:150px; right:84px; font:800 34px/1 'Cairo',sans-serif;
  letter-spacing:.02em; color:var(--ink); direction:ltr; }
#root .tag b { color:var(--accent-warm); }
#root .tag i { font-style:normal; color:rgba(27,29,30,.35); }
#root svg { position:absolute; overflow:visible; }
""" % ("".join(PALETTE.split("\n")))

def render_scene(sid, tpl, start, end):
    src = (ROOT / "tools/scenes" / tpl).read_text(encoding="utf-8")
    dur = round(end - start, 4)

    def rep(m):
        n, e = int(m.group(1)), m.group(2)
        w = W[n]
        t = (w["end"] if e else w["start"]) - start
        return f"{max(0.0, round(t, 3))}"
    src = re.sub(r"\{\{w(\d+)(e?)\}\}", rep, src)
    src = src.replace("{{D}}", f"{dur}").replace("{{ID}}", sid)
    m = re.search(r"<!--STYLE-->(.*?)<!--/STYLE-->", src, re.S)
    style = m.group(1) if m else ""
    body = re.sub(r"<!--STYLE-->.*?<!--/STYLE-->", "", src, flags=re.S)
    sm = re.search(r"<script>.*?</script>", body, re.S)
    script = sm.group(0) if sm else ""
    body = body.replace(script, "")
    html = f"""<template>
  <style>
{FONT_CSS}{SCENE_BASE_CSS}{style}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{dur}" lang="ar" dir="rtl">
    <div class="sheet" aria-hidden="true"></div>
{body.strip()}
  </div>
  {script.strip()}
</template>
"""
    (ROOT / "compositions" / tpl).write_text(html, encoding="utf-8")
    return dur

# ---------------------------------------------------------------- captions
def a_windows():
    """Output windows where the presenter is on screen."""
    wins, t = [], 0.0
    for sid, tpl, s, e, _ in SCENES:
        if s > t:
            wins.append((t, s))
        t = e
    return [(a, min(b, SPEECH_END)) for a, b in wins if a < SPEECH_END]

# Hand-authored semantic caption chunks (word ids), presenter windows only.
CAPTION_GROUPS = [
    [2, 3],
    [14, 15], [16, 17, 18], [19, 20, 21],
    [32, 33], [34, 35, 36], [37, 38, 39],
    [40, 41], [42, 43], [44, 45, 46, 47],
    [52, 53], [54, 55],
    [63, 64], [65, 66, 67, 68], [69, 70],
    [71, 72, 73], [74, 75], [76, 77, 78],
    [86, 87, 88], [89, 90], [91],
    [97], [98, 99, 100], [101, 102, 103], [104, 105, 106],
    [115, 116], [117, 118], [119, 120, 121],
    [122, 123], [124, 125], [126, 127],
    [134, 135, 136], [137], [138, 139, 140], [141, 142, 143], [144, 145, 146],
    [156, 157, 158], [159, 160],
]

def caption_groups():
    wins = a_windows()
    groups = []
    for ids in CAPTION_GROUPS:
        ws = [W[n] for n in ids]
        win = next(w for w in wins if w[0] - 0.05 <= ws[0]["start"] < w[1])
        groups.append({"words": ws, "win": win})
    for g in groups:
        g["start"] = f(max(g["win"][0], g["words"][0]["start"] - 0.04))
    for i, g in enumerate(groups):
        a, b = g["win"]
        nxt = groups[i + 1] if i + 1 < len(groups) else None
        end = min(g["words"][-1]["end"] + 0.30, b)
        if nxt and nxt["win"] == g["win"]:
            end = nxt["start"] if nxt["start"] - g["words"][-1]["end"] < 0.35 else min(end, nxt["start"])
        g["end"] = f(end)
    return groups

def render_captions():
    groups = caption_groups()
    items, script = [], []
    for i, g in enumerate(groups, 1):
        gid = f"c{i:02d}"
        chars = sum(len(w["text"]) for w in g["words"]) + len(g["words"]) - 1
        size = max(58, min(86, int(880 / max(1, chars * 0.52))))
        spans = []
        for w in g["words"]:
            n = int(w["id"][1:])
            cls = "cw" + (" hl-o" if HL.get(n) == "o" else " hl-t" if HL.get(n) == "t" else "")
            spans.append(f'<span id="{gid}-w{n}" class="{cls}">{w["text"]}</span>')
        dur = round(g["end"] - g["start"], 4)
        items.append(f'    <div id="{gid}" class="cg clip" data-start="{g["start"]}" data-duration="{dur}" '
                     f'data-track-index="0" style="font-size:{size}px"><div id="{gid}-in" class="ci">'
                     + " ".join(spans) + "</div></div>")
        script.append(f'  tl.fromTo("#{gid}-in", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.1, ease:"power2.out"}}, {g["start"]});')
        for w in g["words"]:
            n = int(w["id"][1:])
            t = max(g["start"], round(w["start"], 3))
            col = {"o": "#FF8A3D", "t": "#62C6CF"}.get(HL.get(n), None)
            to = f'{{opacity:1, duration:0.067, ease:"none"' + (f', color:"{col}"' if col else "") + "}"
            frm = '{opacity:0.5' + (', color:"#FFFDF8"' if col else "") + "}"
            script.append(f'  tl.fromTo("#{gid}-w{n}", {frm}, {to}, {t});')
    html = f"""<template>
  <style>
{FONT_CSS}
#root {{ position:absolute; inset:0; pointer-events:none; }}
#root .cg {{ position:absolute; left:0; right:0; top:1180px; text-align:center; direction:rtl;
  font-family:'Cairo', sans-serif; font-weight:800; line-height:1.18; color:#FFFDF8; overflow:visible; }}
#root .ci {{ position:relative; isolation:isolate; display:inline-block; max-width:900px; padding:0 34px; }}
#root .ci::before {{ content:""; position:absolute; left:-70px; right:-70px; top:-34px; bottom:-30px; z-index:0;
  background: radial-gradient(closest-side, rgba(14,12,10,.72) 0%, rgba(14,12,10,.62) 52%, rgba(14,12,10,.28) 80%, rgba(14,12,10,0) 100%); }}
#root .cw {{ display:inline-block; opacity:.55; position:relative; z-index:1;
  text-shadow: 0 2px 3px rgba(12,10,8,.5), 0 0 14px rgba(12,10,8,.35); }}
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

# ---------------------------------------------------------------- root
def render_root(scene_durs, sfx_times):
    vids = []
    for s in tm["segments"]:
        vids.append(
            f'        <video id="{s["id"]}" class="clip aroll" src="assets/media/aroll.mp4" '
            f'data-start="{s["out_start"]}" data-duration="{s["duration"]}" data-media-start="{s["src_start"]}" '
            f'data-has-audio="true" data-volume="1" data-track-index="0" playsinline preload="auto"></video>')
    hosts = []
    for sid, tpl, s, e, label in SCENES:
        hosts.append(
            f'      <div id="{sid}" class="scene-host" data-composition-id="{sid}" data-composition-src="compositions/{tpl}" '
            f'data-start="{s}" data-duration="{round(e - s, 4)}" data-track-index="2" data-track-kind="graphics" '
            f'data-width="1080" data-height="1920" title="{label}"></div>')
    sfx = []
    for (sid, file, _, vol), t in zip(SFX, sfx_times):
        sfx.append(f'      <audio id="{sid}" class="clip" src="{file}" data-start="{t}" data-duration="0.36" '
                   f'data-volume="{vol}" data-track-index="4"></audio>')
    cam = [f'  tl.set(cam, {{ transformOrigin: "{FACE_ORIGIN}", scale: 1 }}, 0);',
           '  tl.fromTo(cam, { scale: 1 }, { scale: 1.12, duration: 0.7, ease: "expo.out" }, 0);']
    for t, sc, kind in CROP[1:]:
        cam.append(f'  tl.set(cam, {{ scale: {sc} }}, {t});')
    html = f"""<!doctype html>
<html lang="ar" dir="rtl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Hossam Hassan — reel</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{FONT_CSS}
      :root {{{PALETTE}}}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#1B1D1E; }}
      #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; background:#1B1D1E; }}
      #aroll-cam {{ position:absolute; left:0; top:0; width:1080px; height:1920px; z-index:1; }}
      #aroll-cam video {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
      .scene-host {{ z-index:10; }}
      #captions {{ z-index:5; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-fps="30"
         data-width="1080" data-height="1920">
      <!-- World A: presenter. Untimed camera wrapper (crop states) around the timed source ranges. -->
      <div id="aroll-cam">
{chr(10).join(vids)}
      </div>
      <!-- Word-timed captions (presenter windows only) -->
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html"
           data-start="0" data-duration="{SPEECH_END}" data-track-index="3" data-track-kind="captions"
           data-width="1080" data-height="1920"></div>
      <!-- World B: full-screen editorial interludes -->
{chr(10).join(hosts)}
      <!-- SFX (bundled Pixabay set via /media-use), well under the dialogue -->
{chr(10).join(sfx)}
    </div>
    <script>
  const tl = gsap.timeline({{ paused: true }});
  const cam = document.getElementById("aroll-cam");
{chr(10).join(cam)}
  window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")

if __name__ == "__main__":
    (ROOT / "compositions").mkdir(exist_ok=True)
    durs = {}
    for sid, tpl, s, e, _ in SCENES:
        if (ROOT / "tools/scenes" / tpl).exists():
            durs[sid] = render_scene(sid, tpl, s, e)
    S = {sid: s for sid, _, s, _, _ in SCENES}
    sfx_times = [f(S["g1"] + 3.96), f(S["g5"] + (W[82]["start"] - S["g5"])), f(S["g9"] + (W[150]["start"] - S["g9"])), f(S["g10"] + 0.46)]
    render_root(durs, sfx_times)
    groups = render_captions()
    a_total = sum(b - a for a, b in a_windows())
    g_total = sum(e - s for _, _, s, e, _ in SCENES)
    print(f"total {TOTAL}s  A-roll {a_total:.3f}s ({a_total/TOTAL*100:.1f}%)  graphics {g_total:.3f}s ({g_total/TOTAL*100:.1f}%)")
    print(f"caption groups {len(groups)}")
    for g in groups:
        print(f'  {g["start"]:7.3f}-{g["end"]:7.3f} ' + " ".join(w["text"] for w in g["words"]))
