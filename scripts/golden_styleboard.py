"""황금비·피보나치 규칙(brand/GOLDEN.md) 샘플: 규칙판 · 팔레트 후보 A/B/C × (EP003 콜라주 제목, EP002 썸네일) · EP002 시간 설계도.

사용: python3 -I scripts/golden_styleboard.py → output/002/03_work/golden/ 에서 npx hyperframes snapshot --at 0.5,1.5,…,7.5
숫자: 썸네일 7.0%는 episodes/002/02_research.md, 시간 설계도는 output/002/03_work/v1 내레이션 실측 시각(ep002_common.LINE).
그림: 생성 이미지 없이 CSS·SVG로만(종이 찢김 = clip-path, 망점 = radial-gradient).
"""
import shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))   # python3 -I는 스크립트 폴더를 경로에 넣지 않는다
from ep002_common import LINE

R = Path(__file__).resolve().parents[1]
OUT = R / "output/002/03_work/golden"
PHI = (1 + 5 ** 0.5) / 2
T_EP2 = 270.5   # output/002/03_work/v1/voice.wav 길이(ffprobe)

PAL = {   # GOLDEN.md §5 후보. main 61.8 · second 23.6 · loud 14.6
    "A": dict(name="A · CREAM / NAVY / SIGNAL ORANGE", main="#f2ebdd", sheet="#fbf8f1", second="#1e2a44", second2="#16203a",
              lift="#2c3d63", loud="#f2622e", ink="#1b2233", muted="#5b6478", rule="#d9d0bf", bad="#f2622e", good="#3e64a8", on_loud="#1b2233"),
    "B": dict(name="B · PARCHMENT / MIDNIGHT / GOLD", main="#ece5d3", sheet="#f7f3e8", second="#14161c", second2="#0f1115",
              lift="#23262f", loud="#e5b650", ink="#14161c", muted="#6b6a63", rule="#d6cebb", bad="#e0533d", good="#6f8fb0", on_loud="#14161c"),
    "C": dict(name="C · CHALK / BLACK / LIME", main="#e7e7e2", sheet="#f6f6f2", second="#161616", second2="#0e0e0e",
              lift="#2a2a2a", loud="#d4f23a", ink="#161616", muted="#606060", rule="#d0d0ca", bad="#e0533d", good="#5a7bb5", on_loud="#161616"),
}
vars_ = lambda p: ";".join(f"--{k.replace('_', '-')}:{v}" for k, v in PAL[p].items() if k != "name")


def spiral(x, y, w, h, n=9):
    """황금 사각형을 정사각형으로 잘라 가며 사분원을 잇는다 → (정사각형들, SVG 경로)."""
    sq, d = [], ""
    for i in range(n):
        k = i % 4
        if k == 0: s = h; q = (x, y, s); a, b = (x, y + s), (x + s, y); x += s; w -= s
        elif k == 1: s = w; q = (x, y, s); a, b = (x, y), (x + s, y + s); y += s; h -= s
        elif k == 2: s = h; q = (x + w - s, y, s); a, b = (x + w, y), (x + w - s, y + s); w -= s
        else: s = w; q = (x, y + h - s, s); a, b = (x + s, y + h), (x, y + h - s); h -= s
        sq.append(q)
        d += (f"M{a[0]:.1f},{a[1]:.1f} " if i == 0 else "") + f"A{s:.1f},{s:.1f} 0 0 1 {b[0]:.1f},{b[1]:.1f} "
    return sq, d


assert round(1920 / PHI) == 1187 and round(1080 / PHI) == 667, "GOLDEN.md 표와 같아야 한다"
GW = round(1080 * PHI)
squares, path = spiral((1920 - GW) / 2, 0, GW, 1080)
slides, t = [], 0


def slide(cls, pal, body):
    global t
    slides.append(f'<div class="clip slide {cls}" style="{vars_(pal)}" data-start="{t}" data-duration="1" data-track-index="1">{body}</div>')
    t += 1


# 0 규칙판
sq_svg = "".join(f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}"/>' for x, y, s in squares)
pts = "".join(f'<circle cx="{x}" cy="{y}" r="13"/>' for x in (733, 1187) for y in (413, 667))
scale = "".join(f'<div style="font-size:{n}px">{n}</div>' for n in (34, 55, 89, 144))
swatch = "".join(f'<div style="flex:{f};background:var(--{c})"><span>{f}%</span></div>' for f, c in ((61.8, "main"), (23.6, "second"), (14.6, "loud")))
slide("main-bg", "A", f"""<svg class="grid" viewBox="0 0 1920 1080"><g class="sq">{sq_svg}</g><path class="sp" d="{path}"/>
  <line x1="733" y1="0" x2="733" y2="1080"/><line x1="1187" y1="0" x2="1187" y2="1080"/>
  <line x1="0" y1="413" x2="1920" y2="413"/><line x1="0" y1="667" x2="1920" y2="667"/><g class="pt">{pts}</g></svg>
  <div class="s1-title">GOLDEN RULES<br/><small>&phi; = 1.618 &middot; 8 13 21 34 55 89 144</small></div>
  <div class="s1-scale">{scale}</div><div class="s1-sw">{swatch}</div><div class="s1-note">x 733 / 1187 &middot; y 413 / 667</div>""")

# 1~6 팔레트 후보 × (콜라주 제목, 썸네일)
for p in "ABC":
    slide("second-bg", p, f"""<div class="doc"><div class="doc-h">THE LABOR MARKET FOR RECENT COLLEGE GRADUATES</div>
      <div class="doc-l"></div><div class="doc-l s"></div><div class="doc-l"></div><div class="doc-l s"></div>
      <div class="doc-bars"><i style="height:89px"></i><i style="height:144px"></i><i style="height:55px"></i><i style="height:233px" class="hot"></i><i style="height:89px"></i></div>
      <div class="dots"></div></div>
      <div class="tag t1">EPISODE 3</div><div class="title">IS COLLEGE<br/>STILL<br/>WORTH IT?</div>
      <div class="tag t2">FOR PARENTS &middot; NY FED DATA</div><div class="rule"></div><div class="pname">{PAL[p]['name']}</div>""")
    slide("main-bg", p, f"""<div class="th-left"><div class="th-q">IS COMPUTER<br/>SCIENCE STILL<br/>WORTH IT?</div><div class="th-k">FOR PARENTS</div></div>
      <div class="th-right"><div class="th-n">7.0%</div><div class="th-c">of recent CS grads<br/>are unemployed</div></div><div class="pname dark">{PAL[p]['name']}</div>""")

# 7 시간 설계도: 실제 절 경계 위에 0.382T·0.618T
X0, XW = 89, 1920 - 2 * 89
px = lambda s: X0 + s / T_EP2 * XW
SEC = [("HOOK", "s1_01"), ("FLIP", "s2_01"), ("PILLAR 1", "s3_01"), ("PILLAR 2", "s4_01"), ("PILLAR 3 · PAY", "s5_01"),
       ("PILLAR 4", "s6_01"), ("COUNTER", "s7_01"), ("CHART", "s8_01"), ("CLOSE", "s9_01")]
bars = ""
for i, (n, lid) in enumerate(SEC):
    a = LINE[lid]; b = LINE[SEC[i + 1][1]] if i + 1 < len(SEC) else T_EP2
    bars += f'<div class="sec{" alt" if i % 2 else ""}" style="left:{px(a):.0f}px;width:{px(b) - px(a):.0f}px"><span>{i + 1}</span></div>'
marks = "".join(f'<div class="gm" style="left:{px(T_EP2 * f):.0f}px"><b>{lab}</b><i>{T_EP2 * f:.1f}s</i></div>'
                for f, lab in ((1 / PHI ** 2, "0.382T &middot; ACT 2"), (1 / PHI, "0.618T &middot; CLIMAX: PAY RISES")))
now = f'<div class="nowm" style="left:{px(LINE["s8_01"]):.0f}px"><b>NOW: SCATTER FIRST SHOWN</b><i>{LINE["s8_01"]:.1f}s = 0.884T &rarr; becomes recap</i></div>'
fib = "".join(f'<div class="fb" style="width:{s * 21}px">{s}s</div>' for s in (3, 5, 8, 13, 8, 5, 3))
slide("main-bg", "A", f"""<div class="tl-title">EP002 IN GOLDEN TIME<br/><small>T = {T_EP2}s &middot; real narration timings</small></div>
  <div class="tl">{bars}{marks}{now}</div>
  <div class="legend">{"".join(f"<span><b>{i + 1}</b> {n}</span>" for i, (n, _) in enumerate(SEC))}</div>
  <div class="fibrow"><em>SHOT RHYTHM</em>{fib}</div>""")
DUR = t

CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1920px; height: 1080px; overflow: hidden; background: #f2ebdd; }
  .slide { position: absolute; inset: 0; overflow: hidden; font-family: 'Source Sans 3', 'Helvetica Neue', Arial, sans-serif; color: var(--ink); }
  .main-bg { background: var(--main); }
  .second-bg { background: radial-gradient(circle at 1187px 413px, var(--lift) 0, var(--second) 610px, var(--second2) 1080px); color: var(--main); }
  .pname { position: absolute; right: 34px; bottom: 21px; font: 700 34px 'IBM Plex Mono', Menlo, monospace; color: var(--main); opacity: .8; }
  .pname.dark { color: var(--ink); }
  .grid { position: absolute; inset: 0; width: 1920px; height: 1080px; fill: none; }
  .grid .sq rect { stroke: var(--loud); stroke-width: 2; stroke-dasharray: 8 13; opacity: .55; }
  .grid .sp { stroke: var(--loud); stroke-width: 5; } .grid line { stroke: var(--ink); stroke-width: 3; opacity: .35; } .grid .pt circle { fill: var(--second); }
  .s1-title { position: absolute; left: 89px; top: 89px; font-family: "Archivo Black", sans-serif; font-size: 89px; line-height: 1.236; }
  .s1-title small, .tl-title small { font-family: 'IBM Plex Mono', Menlo, monospace; font-size: 34px; font-weight: 600; color: var(--muted); }
  .s1-scale { position: absolute; left: 1242px; top: 433px; display: flex; align-items: baseline; gap: 34px; font-family: "Archivo Black", sans-serif; line-height: 1; }
  .s1-sw { position: absolute; left: 89px; right: 89px; bottom: 89px; height: 89px; display: flex; border: 3px solid var(--ink); }
  .s1-sw div { display: flex; align-items: center; padding-left: 21px; } .s1-sw span { font: 700 34px 'IBM Plex Mono', Menlo, monospace; color: var(--ink); }
  .s1-sw div:nth-child(2) span { color: var(--main); }
  .s1-note { position: absolute; left: 754px; top: 680px; font: 600 34px 'IBM Plex Mono', Menlo, monospace; color: var(--muted); }
  .doc { position: absolute; left: 144px; top: 144px; width: 589px; height: 754px; background: var(--main); color: var(--ink); padding: 55px;
         transform: rotate(-2.618deg); box-shadow: 8px 8px 13px rgba(0,0,0,.35);
         clip-path: polygon(0 0, 100% 0, 100% 92%, 94% 95%, 88% 92%, 81% 96%, 73% 93%, 64% 97%, 55% 93%, 47% 96%, 38% 92%, 30% 96%, 21% 93%, 13% 97%, 6% 93%, 0 96%); }
  .doc-h { font: 800 34px/1.236 'Source Sans 3', Arial, sans-serif; letter-spacing: .02em; margin-bottom: 34px; }
  .doc-l { height: 13px; background: var(--rule); margin-bottom: 21px; } .doc-l.s { width: 61.8%; }
  .doc-bars { display: flex; align-items: flex-end; gap: 21px; height: 233px; margin-top: 55px; border-bottom: 3px solid var(--ink); }
  .doc-bars i { flex: 1; background: var(--muted); } .doc-bars i.hot { background: var(--bad); }
  .dots { position: absolute; right: 0; bottom: 0; width: 377px; height: 233px; opacity: .35; background: radial-gradient(circle, var(--ink) 3px, transparent 3.5px) 0 0 / 13px 13px; }
  .title { position: absolute; left: 822px; top: 233px; font-family: "Archivo Black", sans-serif; font-size: 144px; line-height: 1.0; color: var(--main); white-space: nowrap; }
  .tag { position: absolute; background: var(--sheet); color: var(--ink); font: 800 34px 'Source Sans 3', Arial, sans-serif; padding: 13px 21px; box-shadow: 8px 8px 13px rgba(0,0,0,.35); }
  .t1 { left: 822px; top: 144px; transform: rotate(-2.618deg); background: var(--loud); color: var(--on-loud); }
  .t2 { left: 1187px; top: 754px; transform: rotate(1.618deg); }
  .rule { position: absolute; left: 822px; top: 699px; width: 233px; height: 5px; background: var(--loud); }
  .th-left { position: absolute; left: 0; top: 0; width: 1187px; height: 1080px; padding: 89px; display: flex; flex-direction: column; justify-content: center; background: var(--second); color: var(--main); }
  .th-q { font-family: "Archivo Black", sans-serif; font-size: 144px; line-height: 1.0; }
  .th-k { margin-top: 55px; align-self: flex-start; background: var(--loud); color: var(--on-loud); font: 800 55px 'Source Sans 3', Arial, sans-serif; padding: 8px 21px; transform: rotate(-1.618deg); }
  .th-right { position: absolute; left: 1187px; top: 0; width: 733px; height: 1080px; background: var(--sheet); color: var(--ink); display: flex; flex-direction: column; justify-content: center; padding: 55px; }
  .th-n { font-family: "Archivo Black", sans-serif; font-size: 233px; line-height: 1.0; color: var(--bad); letter-spacing: -.02em; }
  .th-c { margin-top: 34px; font: 700 55px/1.236 'Source Sans 3', Arial, sans-serif; }
  .tl-title { position: absolute; left: 89px; top: 89px; font-family: "Archivo Black", sans-serif; font-size: 89px; line-height: 1.236; }
  .tl { position: absolute; left: 0; top: 489px; width: 1920px; height: 89px; }
  .sec { position: absolute; top: 0; height: 89px; background: var(--second); border-right: 3px solid var(--main); display: flex; align-items: center; justify-content: center; }
  .sec.alt { background: var(--lift); } .sec span { font: 800 34px 'IBM Plex Mono', Menlo, monospace; color: var(--main); }
  .gm, .nowm { position: absolute; top: -144px; height: 233px; border-left: 5px solid var(--loud); padding-left: 13px; white-space: nowrap; }
  .gm b, .nowm b { display: block; font: 800 34px 'Source Sans 3', Arial, sans-serif; } .gm i, .nowm i { font: 600 34px 'IBM Plex Mono', Menlo, monospace; font-style: normal; color: var(--muted); }
  .nowm { top: 89px; height: 144px; display: flex; flex-direction: column; justify-content: flex-end; transform: translateX(-100%); border-left: none; border-right: 3px dashed var(--muted); padding: 0 13px 0 0; text-align: right; }
  .legend { position: absolute; left: 89px; right: 89px; top: 787px; display: flex; flex-wrap: wrap; gap: 13px 34px; font: 600 34px 'Source Sans 3', Arial, sans-serif; }
  .legend b { font-family: 'IBM Plex Mono', Menlo, monospace; color: var(--loud); }
  .fibrow { position: absolute; left: 89px; bottom: 89px; display: flex; align-items: center; gap: 8px; font: 800 34px 'IBM Plex Mono', Menlo, monospace; }
  .fibrow em { font-style: normal; margin-right: 21px; color: var(--muted); }
  .fb { height: 55px; background: var(--second); color: var(--main); display: flex; align-items: center; justify-content: center; }
"""

OUT.mkdir(parents=True, exist_ok=True)
for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(R / "episodes/002/film" / f, OUT / f)
(OUT / "index.html").write_text(f"""<!doctype html>
<html lang="en">
  <head><meta charset="UTF-8" /><meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script><style>{CSS}</style></head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080">
{chr(10).join(slides)}
    </div>
    <script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }}).to({{}}, {{ duration: {DUR} }});</script>
  </body>
</html>
""")
print("styleboard:", OUT, "· slides", DUR)
