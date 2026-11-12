"""EP002 시안 두 장면(무음, 약 30초): 캠퍼스 → 실업률 축 줄서기 → 초봉 산점도. 승인용 시안이지 최종본이 아니다.

사용: python3 -I scripts/ep002_proto.py [v1|golden] → output/002/03_work/proto[_golden]/ (git 제외) 에서 npx hyperframes render
      golden = brand/GOLDEN.md 규칙(황금비·피보나치, 팔레트 A)
조합: HyperFrames + three.js r170(episodes/002/film/assets/lib 재사용) + 레퍼런스 문법(docs/research/ep002-major-viz-references.md):
      정렬 축 + 평균선 + 한 전공만 색, 숫자는 고정 카드 한 자리, 좋은 지표(초봉)만 높이에 싣는다.
숫자: 카드 문구는 episodes/002/02_research.md 7·9·17번 항목, 높이·위치는 같은 NY Fed 전공별 CSV 원값.
"""
import json, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))   # python3 -I는 스크립트 폴더를 경로에 넣지 않는다
from ep002_common import R, CS, CE, buildings
from golden_kit import tokens
G = tokens()

NAME = sys.argv[1] if len(sys.argv) > 1 else "v1"
THEMES = {   # 3D 색(T)과 HTML 카드 규격(C). golden 값은 brand/golden.css와 같다
    "v1": {"T": {"bg": "#f1ece2", "ground": "#efe9dd", "danger": "#e9a796", "safe": "#bcd9b2", "ink": "#1d2421", "pay": "#2c5f8a",
                 "base": "#c9c4ba", "bad": "#d9452b", "focus": "#ffffff", "good": "#3f8f5b"},
           "C": {"bg": "#f1ece2", "ink": "#1d2421", "card": "#fffdf8", "num": 92, "lab": 30, "sub": 32, "tick": 30, "cap": 54,
                 "card_pos": "left: 50%; bottom: 96px; transform: translateX(-50%);", "pad": "18px 34px", "font": "Inter, sans-serif"}},
    "golden": {"T": {"bg": G["main"], "ground": G["main-shade"], "danger": G["loud-tint"], "safe": G["good-tint"], "ink": G["second"],
                     "pay": G["good"], "base": G["neutral"], "bad": G["bad"], "focus": G["sheet"], "good": G["good"]},   # 색은 brand/golden.css에서만
               "C": {"bg": G["main"], "ink": G["ink"], "card": G["sheet"], "num": 144, "lab": 34, "sub": 34, "tick": 34, "cap": 55,
                     "card_pos": "left: 89px; top: 89px;", "pad": "21px 34px", "font": "'Source Sans 3', 'Helvetica Neue', Arial, sans-serif"}},
}
TH = THEMES[NAME]
FILM, OUT = R / "episodes/002/film", R / ("output/002/03_work/proto" + ("" if NAME == "v1" else "_" + NAME))
B = buildings(); ID = {b["name"]: b["id"] for b in B}
AVG_U, AVG_W, END = 4.2, 58000, 39.0   # 02_research.md: 전체 4.2%, 초봉 전체 $58,000

EV = {"lineup": 2.0, "zone": 5.4, "grow": 25.4}
CARDS = [   # (id, 전공, 큰 글씨, 작은 글씨, 색, 시작, 끝, 계속 칠해 둠) — 카드마다 3.5초 이상(읽기 하한)
    ("cs", CS, "7.0%", "7 in 100 recent grads are unemployed", "red", 6.5, 10.5, True),
    ("ah", "Art History", "6.7%", "lower than computer science", "white", 10.5, 14.0, False),
    ("ph", "Philosophy", "5.1%", "lower than computer science", "white", 14.0, 17.5, False),
    ("ce", CE, "7.8%", "the second-highest of 73 majors", "red", 17.5, 21.5, True),   # 02_research 3번: 1위 인류학 7.9%
    ("nu", "Nursing", "2.1%", "one of the safest majors", "green", 21.5, 25.0, False),
    ("cs2", CS, "$87,000", "starting pay, and 7.0% unemployed", "red", 29.6, 34.0, True),
    ("ah2", "Art History", "$45,000", "starting pay, and 6.7% unemployed", "white", 34.0, 38.6, False),
]
HL = [{"id": ID[m], "kind": k, "t": t, "e": e, "keep": keep, "card": f"card-{c}"} for c, m, _, _, k, t, e, keep in CARDS]
XS, HW = 1.3, 4.2 / 100000   # proto.js와 같은 축척
TICKS = [(f"{u}%", u * XS, 0, 5.5, 5.6, 38.9) for u in (2, 6, 8)] + [   # 가로축 눈금은 산점도까지 유지
    ("ALL MAJORS 4.2%", AVG_U * XS, 0, 5.5, 5.6, 38.9),   # 평균은 축 위 4% 자리에(위쪽은 카드 자리)
    ("&larr; FEWER JOBLESS", 2.2, 0, 6.1, 5.6, 38.9), ("MORE JOBLESS &rarr;", 10.0, 0, 6.1, 5.6, 38.9),
    ("ALL MAJORS $58,000", 1.9, AVG_W * HW + 0.25, 4.8, 28.0, 38.9),
    ("HIGH PAY, MORE JOBLESS", 7.6, 4.6, -1.5, 28.4, 38.9),   # 우리 전공이 선 사분면만 이름 붙임
]

PROTO = {"B": [{k: b[k] for k in ("id", "name", "u", "w", "gx", "gy")} for b in B], "avgU": AVG_U, "avgW": AVG_W,
         "EV": EV, "HL": HL, "END": END, "THEME": TH["T"]}
tick_html = "\n".join(f'    <div class="tick fade" data-in="{a}" data-out="{o}" data-wx="{x}" data-wy="{y}" data-wz="{z}">{t}</div>'
                      for t, x, y, z, a, o in TICKS)
card_html = "\n".join(f'    <div id="card-{c}" class="card {k}{" pay" if big.startswith("$") else ""}"><b>{big}</b><span><i>{m.upper()}</i>{small}</span></div>'
                      for c, m, big, small, k, *_ in CARDS)
caps = [("73 MAJORS, ONE CAMPUS", 0.3, 1.9), ("LINE THEM UP BY UNEMPLOYMENT", 2.2, 5.2), ("NOW ADD STARTING PAY", 25.4, 29.3)]
cap_html = "\n".join(f'    <div class="cap fade" data-in="{a}" data-out="{o}">{t}</div>' for t, a, o in caps)

C = TH["C"]
comp = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; background: {C["bg"]}; overflow: hidden; font-family: {C["font"]}; color: {C["ink"]}; }}
    #gl {{ position: absolute; inset: 0; width: 1920px; height: 1080px; }}
    .fade, .card, #pin {{ opacity: 0; }}
    .tick {{ position: absolute; left: 0; top: 0; font-weight: 800; font-size: {C["tick"]}px; white-space: nowrap; letter-spacing: .02em; }}
    .cap {{ position: absolute; left: 50%; top: 70px; transform: translateX(-50%); font-family: "Archivo Black", sans-serif; font-size: {C["cap"]}px; white-space: nowrap; }}
    .card {{ position: absolute; {C["card_pos"]} display: flex; align-items: center; gap: 34px;
             background: {C["card"]}; border: 3px solid {C["ink"]}; padding: {C["pad"]}; box-shadow: 8px 8px 0 rgba(29,26,22,.18); white-space: nowrap; }}
    .card b {{ font-family: "Archivo Black", sans-serif; font-weight: 400; font-size: {C["num"]}px; line-height: 1; font-variant-numeric: tabular-nums; }}
    .card span {{ display: flex; flex-direction: column; font-size: {C["sub"]}px; font-weight: 600; line-height: 1.236; }}
    .card i {{ font-style: normal; font-weight: 900; font-size: {C["lab"]}px; letter-spacing: .04em; }}
    .card.red b {{ color: {TH["T"]["bad"]}; }} .card.green b {{ color: {TH["T"]["good"]}; }}
    .card.pay b {{ color: {TH["T"]["pay"]}; }}   /* 숫자 색은 지표를 따른다: 초봉 = 좋은 지표 */
    #pin {{ position: absolute; left: 0; top: 0; width: 4px; height: 70px; background: #1d2421; }}
    #pin::before {{ content: ""; position: absolute; left: -9px; top: -18px; width: 22px; height: 22px; border-radius: 50%; background: #1d2421; }}
    #src {{ position: absolute; left: 50%; bottom: 22px; transform: translateX(-50%); font-size: 28px; color: #5b5f5a; white-space: nowrap; }}
    #draft {{ position: absolute; right: 40px; top: 36px; font-size: 28px; font-weight: 800; color: #9a3b2b; border: 2px solid #9a3b2b; padding: 4px 10px; }}
  </style>
  <div id="root" data-composition-id="proto" data-width="1920" data-height="1080">
    <canvas id="gl" width="1920" height="1080" data-layout-ignore></canvas>
{tick_html}
{cap_html}
{card_html}
    <div id="pin"></div>
    <div id="src">Source: NY Fed, recent college graduates by major (2024 data)</div>
    <div id="draft">DRAFT &middot; NO SOUND</div>
  </div>
  <script type="module">
    window.__PROTO = {json.dumps(PROTO)};
{(FILM / "src/proto.js").read_text()}
  </script>
</template>
"""
(OUT / "compositions").mkdir(parents=True, exist_ok=True)
(OUT / "compositions/proto.html").write_text(comp)
shutil.copytree(FILM / "assets/lib", OUT / "assets/lib", dirs_exist_ok=True)
for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(FILM / f, OUT / f)
(OUT / "index.html").write_text(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script type="importmap">{{"imports": {{"three": "./assets/lib/three.module.js"}}}}</script>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: {TH["C"]["bg"]}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1920" data-height="1080">
      <div id="proto" data-composition-id="proto" data-composition-src="compositions/proto.html" data-start="0" data-duration="{END}"
           data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
assert all(m in ID for _, m, *_ in CARDS), "카드 전공명이 CSV에 있어야 한다"
print(f"proto: {OUT} · buildings {len(B)} · cards {len(CARDS)} · ticks {len(TICKS)}")
