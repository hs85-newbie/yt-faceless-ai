"""황금비·피보나치 규칙(brand/GOLDEN.md) 샘플 정지 화면 3장: 구조 설명판 · EP003 콜라주 제목 카드 · EP002 썸네일.

사용: python3 -I scripts/golden_styleboard.py → output/002/03_work/golden/ 에서 npx hyperframes snapshot --at 0.5,1.5,2.5
숫자: 썸네일의 7.0%는 episodes/002/02_research.md(NY Fed 전공별 CSV). 콜라주 카드는 숫자 없음.
그림: 생성 이미지 없이 CSS·SVG로만(종이 찢김 = clip-path, 망점 = radial-gradient).
"""
import shutil
from pathlib import Path

R = Path(__file__).resolve().parents[1]
OUT = R / "output/002/03_work/golden"
PHI = (1 + 5 ** 0.5) / 2
FIB = [8, 13, 21, 34, 55, 89, 144, 233]


def spiral(x, y, w, h, n=9):
    """황금 사각형을 정사각형으로 잘라 가며 사분원을 잇는다 → (정사각형들, SVG 경로)."""
    sq, d = [], ""
    for i in range(n):
        k = i % 4
        if k == 0: s = h; q = (x, y, s); cx, cy = x + s, y + s; a, b = (x, y + s), (x + s, y); x += s; w -= s
        elif k == 1: s = w; q = (x, y, s); cx, cy = x, y + s; a, b = (x, y), (x + s, y + s); y += s; h -= s
        elif k == 2: s = h; q = (x + w - s, y, s); cx, cy = x + w - s, y; a, b = (x + w, y), (x + w - s, y + s); w -= s
        else: s = w; q = (x, y + h - s, s); cx, cy = x + s, y + h - s; a, b = (x + s, y + h), (x, y + h - s); h -= s
        sq.append(q)
        d += (f"M{a[0]:.1f},{a[1]:.1f} " if i == 0 else "") + f"A{s:.1f},{s:.1f} 0 0 1 {b[0]:.1f},{b[1]:.1f} "
    return sq, d


GW = round(1080 * PHI)   # 1747: 높이 1080의 황금 사각형
squares, path = spiral((1920 - GW) / 2, 0, GW, 1080)
assert round(1920 / PHI) == 1187 and round(1080 / PHI) == 667, "GOLDEN.md 표와 같아야 한다"
sq_svg = "".join(f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}"/>' for x, y, s in squares)
pts = "".join(f'<circle cx="{x}" cy="{y}" r="13"/>' for x in (733, 1187) for y in (413, 667))
scale = "".join(f'<div style="font-size:{n}px">{n}</div>' for n in (34, 55, 89, 144))
swatch = "".join(f'<div style="flex:{f};background:{c}"><span>{f}%</span></div>'
                 for f, c in ((61.8, "#f3ead8"), (23.6, "#2b1f17"), (14.6, "#b8862b")))

S1 = f"""
<div id="s1" class="clip slide paper" data-start="0" data-duration="1" data-track-index="1">
  <svg class="grid" viewBox="0 0 1920 1080">
    <g class="sq">{sq_svg}</g><path class="sp" d="{path}"/>
    <line x1="733" y1="0" x2="733" y2="1080"/><line x1="1187" y1="0" x2="1187" y2="1080"/>
    <line x1="0" y1="413" x2="1920" y2="413"/><line x1="0" y1="667" x2="1920" y2="667"/>
    <g class="pt">{pts}</g>
  </svg>
  <div class="s1-title">GOLDEN RULES<br/><small>&phi; = 1.618 &middot; 8 13 21 34 55 89 144</small></div>
  <div class="s1-scale">{scale}</div>
  <div class="s1-sw">{swatch}</div>
  <div class="s1-note">x 733 / 1187 &middot; y 413 / 667</div>
</div>"""

S2 = """
<div id="s2" class="clip slide walnut" data-start="1" data-duration="1" data-track-index="1">
  <div class="doc"><div class="doc-h">THE LABOR MARKET FOR RECENT COLLEGE GRADUATES</div>
    <div class="doc-l"></div><div class="doc-l s"></div><div class="doc-l"></div><div class="doc-l s"></div>
    <div class="doc-bars"><i style="height:89px"></i><i style="height:144px"></i><i style="height:55px"></i><i style="height:233px" class="hot"></i><i style="height:89px"></i></div>
    <div class="dots"></div></div>
  <div class="tag t1">EPISODE 3</div>
  <div class="title">IS COLLEGE<br/>STILL<br/>WORTH IT?</div>
  <div class="tag t2">FOR PARENTS &middot; NY FED DATA</div>
  <div class="rule"></div>
</div>"""

S3 = """
<div id="s3" class="clip slide paper" data-start="2" data-duration="1" data-track-index="1">
  <div class="th-left"><div class="th-q">IS COMPUTER<br/>SCIENCE STILL<br/>WORTH IT?</div><div class="th-k">FOR PARENTS</div></div>
  <div class="th-right"><div class="th-n">7.0%</div><div class="th-c">of recent CS grads<br/>are unemployed</div></div>
</div>"""

CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1920px; height: 1080px; overflow: hidden; background: #f3ead8; }
  .slide { position: absolute; inset: 0; overflow: hidden; font-family: 'Source Sans 3', 'Helvetica Neue', Arial, sans-serif; color: #1d1a16; }
  .paper { background: #f3ead8; } .walnut { background: radial-gradient(circle at 1187px 413px, #3b2b20 0, #2b1f17 610px, #1f1610 1080px); color: #f3ead8; }
  .grid { position: absolute; inset: 0; width: 1920px; height: 1080px; fill: none; }
  .grid .sq rect { stroke: #b8862b; stroke-width: 2; stroke-dasharray: 8 13; opacity: .55; }
  .grid .sp { stroke: #b8862b; stroke-width: 5; }
  .grid line { stroke: #1d1a16; stroke-width: 3; opacity: .35; }
  .grid .pt circle { fill: #c4432b; }
  .s1-title { position: absolute; left: 89px; top: 89px; font-family: "Archivo Black", sans-serif; font-size: 89px; line-height: 1.236; }
  .s1-title small { font-family: 'IBM Plex Mono', Menlo, monospace; font-size: 34px; font-weight: 600; color: #7a6a5a; }
  .s1-scale { position: absolute; left: 1242px; top: 433px; display: flex; align-items: baseline; gap: 34px; font-family: "Archivo Black", sans-serif; line-height: 1; }
  .s1-sw { position: absolute; left: 89px; right: 89px; bottom: 89px; height: 89px; display: flex; border: 3px solid #1d1a16; }
  .s1-sw div { display: flex; align-items: center; padding-left: 21px; } .s1-sw span { font: 700 34px 'IBM Plex Mono', Menlo, monospace; color: #b8862b; mix-blend-mode: normal; }
  .s1-sw div:first-child span { color: #1d1a16; } .s1-sw div:nth-child(2) span { color: #f3ead8; } .s1-sw div:last-child span { color: #1d1a16; }
  .s1-note { position: absolute; left: 754px; top: 680px; font: 600 34px 'IBM Plex Mono', Menlo, monospace; color: #7a6a5a; }
  /* S2 콜라주: 종이 문서 + 망점 + 기울인 이름표. 제목은 황금점(1187,413) 왼쪽 위에 걸친다 */
  .doc { position: absolute; left: 144px; top: 144px; width: 589px; height: 754px; background: #f3ead8; color: #1d1a16; padding: 55px;
         transform: rotate(-2.618deg); box-shadow: 8px 8px 13px rgba(0,0,0,.35);
         clip-path: polygon(0 0, 100% 0, 100% 92%, 94% 95%, 88% 92%, 81% 96%, 73% 93%, 64% 97%, 55% 93%, 47% 96%, 38% 92%, 30% 96%, 21% 93%, 13% 97%, 6% 93%, 0 96%); }
  .doc-h { font: 800 34px/1.236 'Source Sans 3', Arial, sans-serif; letter-spacing: .02em; margin-bottom: 34px; }
  .doc-l { height: 13px; background: #cbbca5; margin-bottom: 21px; } .doc-l.s { width: 61.8%; }
  .doc-bars { display: flex; align-items: flex-end; gap: 21px; height: 233px; margin-top: 55px; border-bottom: 3px solid #1d1a16; }
  .doc-bars i { flex: 1; background: #7a6a5a; } .doc-bars i.hot { background: #c4432b; }
  .dots { position: absolute; right: 0; bottom: 0; width: 377px; height: 233px; opacity: .35;
          background: radial-gradient(circle, #1d1a16 3px, transparent 3.5px) 0 0 / 13px 13px; }
  .title { position: absolute; left: 822px; top: 233px; font-family: "Archivo Black", sans-serif; font-size: 144px; line-height: 1.0; color: #f3ead8; white-space: nowrap; }
  .tag { position: absolute; background: #fffaf0; color: #1d1a16; font: 800 34px 'Source Sans 3', Arial, sans-serif; padding: 13px 21px; box-shadow: 8px 8px 13px rgba(0,0,0,.35); }
  .t1 { left: 822px; top: 144px; transform: rotate(-2.618deg); background: #e5b650; }
  .t2 { left: 1187px; top: 754px; transform: rotate(1.618deg); }
  .rule { position: absolute; left: 822px; top: 699px; width: 233px; height: 5px; background: #e5b650; }
  /* S3 썸네일: 1187 : 733 분할. 숫자는 데이터색(나쁨) 233px */
  .th-left { position: absolute; left: 0; top: 0; width: 1187px; height: 1080px; padding: 89px; display: flex; flex-direction: column; justify-content: center; }
  .th-q { font-family: "Archivo Black", sans-serif; font-size: 144px; line-height: 1.0; }
  .th-k { margin-top: 55px; align-self: flex-start; background: #b8862b; color: #fffaf0; font: 800 55px 'Source Sans 3', Arial, sans-serif; padding: 8px 21px; transform: rotate(-1.618deg); }
  .th-right { position: absolute; left: 1187px; top: 0; width: 733px; height: 1080px; background: #2b1f17; color: #f3ead8; display: flex; flex-direction: column; justify-content: center; padding: 55px; }
  .th-n { font-family: "Archivo Black", sans-serif; font-size: 233px; line-height: 1.0; color: #e0563f; letter-spacing: -.02em; }
  .th-c { margin-top: 34px; font: 700 55px/1.236 'Source Sans 3', Arial, sans-serif; }
"""

OUT.mkdir(parents=True, exist_ok=True)
for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(R / "episodes/002/film" / f, OUT / f)
(OUT / "index.html").write_text(f"""<!doctype html>
<html lang="en">
  <head><meta charset="UTF-8" /><meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script><style>{CSS}</style></head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="3" data-width="1920" data-height="1080">{S1}{S2}{S3}
    </div>
    <script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }}).to({{}}, {{ duration: 3 }});</script>
  </body>
</html>
""")
print("styleboard:", OUT, "· spiral squares", len(squares))
