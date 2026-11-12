"""EP002 3D 장면 빌더: 계획(plan)을 받아 HyperFrames 프로젝트를 쓴다. 계획은 ep002_proto.py(두 장면 시안)·ep002_full_plan.py(풀 길이).

계획 dict: name, end, cards, ticks, caps, tl, plates(HTML 목록), cams(선택), audio(선택, wav 경로), draft(우상단 표시)
카드: {id, major?, big, label?, small, kind(건물색 red|white|green|None), num(bad|good|pay|neutral), t, e, keep?}
규칙: brand/GOLDEN.md — 색은 golden.css(theme golden)에서만, 숫자 색은 지표를 따른다(전체 평균보다 나쁘면 bad, 좋으면 good).
"""
import json, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))   # python3 -I는 스크립트 폴더를 경로에 넣지 않는다
from ep002_common import R, buildings
from golden_kit import tokens, root_css

G = tokens()
FILM = R / "episodes/002/film"
XS, HW = 1.3, 4.2 / 100000   # proto.js와 같은 축척(실업률 1%p = 가로 1.3, 초봉 $10만 = 높이 4.2)
AVG_U, AVG_W = 4.2, 58000    # 02_research.md: 전체 4.2%, 초봉 전체 $58,000
SANS = "Inter, 'Helvetica Neue', Arial, sans-serif"   # 렌더러 번들 글꼴(Source Sans 3는 번들 아님 — 파일을 넣기 전까지 Inter)
THEMES = {   # 3D 색(T)과 HTML 카드 규격(C). golden 값은 brand/golden.css와 같다
    "v1": {"T": {"bg": "#f1ece2", "ground": "#efe9dd", "danger": "#e9a796", "safe": "#bcd9b2", "ink": "#1d2421", "pay": "#2c5f8a",
                 "base": "#c9c4ba", "bad": "#d9452b", "focus": "#ffffff", "good": "#3f8f5b"},
           "C": {"bg": "#f1ece2", "ink": "#1d2421", "card": "#fffdf8", "num": 92, "lab": 30, "sub": 32, "tick": 30, "cap": 54,
                 "card_pos": "left: 50%; bottom: 96px; transform: translateX(-50%);", "pad": "18px 34px", "font": "Inter, sans-serif"}},
    "golden": {"T": {"bg": G["main"], "ground": G["main-shade"], "danger": G["loud-tint"], "safe": G["good-tint"], "ink": G["second"],
                     "pay": G["good"], "base": G["neutral"], "bad": G["bad"], "focus": G["sheet"], "good": G["good"]},
               "C": {"bg": G["main"], "ink": G["ink"], "card": G["sheet"], "num": 144, "lab": 34, "sub": 34, "tick": 34, "cap": 55,
                     "card_pos": "left: 89px; top: 89px;", "pad": "21px 34px", "font": SANS}},
}


def plate(t_in, t_out, title, rows, foot, note=""):
    """전면 데이터 판(크림 바탕). rows = [(숫자, bad|good|neutral, 설명)] — 숫자 144px, 설명 34px, 제목 55px, 여백 89."""
    # 숫자 7자 넘으면(1,905,400 · $134,040) 피보나치 한 단계 아래 89px — 옆 칸과 겹치지 않게
    cells = "".join(f'<div class="pr"><b class="n-{c}"{" style=\"font-size:89px\"" if len(n) > 7 else ""}>{n}</b><span>{lab}</span></div>'
                    for n, c, lab in rows)
    nt = f'<div class="pn">{note}</div>' if note else ""
    return (f'<div class="plate fade" data-in="{t_in}" data-out="{t_out}"><div class="pt">{title}</div>'
            f'<div class="pg">{cells}</div>{nt}<div class="pf">{foot}</div></div>')


def statement(t_in, t_out, text, sub="", dark=False):
    """문장 하나를 크게(89px) — 황금점(733, 413) 기준 왼쪽 정렬. dark = 보조색(네이비) 바탕."""
    s = f'<div class="ss">{sub}</div>' if sub else ""
    return f'<div class="stmt fade{" dark" if dark else ""}" data-in="{t_in}" data-out="{t_out}"><div class="st">{text}</div>{s}</div>'


def build(plan, theme="golden"):
    TH, C = THEMES[theme], THEMES[theme]["C"]
    B = buildings(); ID = {b["name"]: b["id"] for b in B}
    out = R / f"output/002/03_work/{plan['name']}"
    cards = plan["cards"]
    assert all(c.get("major") in (None, *ID) for c in cards), "카드 전공명이 CSV에 있어야 한다"
    hl = [{"id": ID[c["major"]] if c.get("major") else None, "kind": c.get("kind") or "white", "t": c["t"], "e": c["e"],
           "keep": c.get("keep", False), "card": f"card-{c['id']}"} for c in cards]
    data = {"B": [{k: b[k] for k in ("id", "name", "u", "w", "gx", "gy")} for b in B], "avgU": AVG_U, "avgW": AVG_W,
            "HL": hl, "TL": plan["tl"], "END": plan["end"], "THEME": TH["T"], **({"CAMS": plan["cams"]} if plan.get("cams") else {})}
    tick_html = "\n".join(f'    <div class="tick fade" data-in="{a}" data-out="{o}" data-wx="{x}" data-wy="{y}" data-wz="{z}">{t}</div>'
                          for t, x, y, z, a, o in plan["ticks"])
    card_html = "\n".join(f'    <div id="card-{c["id"]}" class="card n-{c["num"]}"><b>{c["big"]}</b><span><i>{c.get("label") or c["major"].upper()}</i>{c["small"]}</span></div>'
                          for c in cards)
    cap_html = "\n".join(f'    <div class="cap fade" data-in="{a}" data-out="{o}">{t}</div>' for t, a, o in plan["caps"])
    T = TH["T"]
    comp = f"""<template>
  <style>
    {root_css()}
    #root {{ --gb-sans: {SANS}; --gb-mono: 'IBM Plex Mono', Menlo, monospace;
             position: absolute; inset: 0; background: {C["bg"]}; overflow: hidden; font-family: {C["font"]}; color: {C["ink"]}; }}
    #gl {{ position: absolute; inset: 0; width: 1920px; height: 1080px; }}
    .fade, .card, #pin {{ opacity: 0; }}
    .tick {{ position: absolute; left: 0; top: 0; font-weight: 800; font-size: {C["tick"]}px; white-space: nowrap; letter-spacing: .02em; }}
    .cap {{ position: absolute; left: 50%; top: 70px; transform: translateX(-50%); font-family: "Archivo Black", sans-serif; font-size: {C["cap"]}px; white-space: nowrap; }}
    .card {{ position: absolute; {C["card_pos"]} display: flex; align-items: center; gap: 34px;
             background: {C["card"]}; border: 3px solid {C["ink"]}; padding: {C["pad"]}; box-shadow: 8px 8px 0 rgba(29,26,22,.18); white-space: nowrap; }}
    .card b {{ font-family: "Archivo Black", sans-serif; font-weight: 400; font-size: {C["num"]}px; line-height: 1; font-variant-numeric: tabular-nums; }}
    .card span {{ display: flex; flex-direction: column; font-size: {C["sub"]}px; font-weight: 600; line-height: 1.236; }}
    .card i {{ font-style: normal; font-weight: 900; font-size: {C["lab"]}px; letter-spacing: .04em; }}
    .n-bad b, b.n-bad {{ color: {T["bad"]}; }} .n-good b, b.n-good {{ color: {T["good"]}; }} .n-pay b, b.n-pay {{ color: {T["pay"]}; }}
    #pin {{ position: absolute; left: 0; top: 0; width: 4px; height: 70px; background: {C["ink"]}; }}
    #pin::before {{ content: ""; position: absolute; left: -9px; top: -18px; width: 22px; height: 22px; border-radius: 50%; background: {C["ink"]}; }}
    #src {{ position: absolute; left: 50%; bottom: 22px; transform: translateX(-50%); font-size: 28px; color: {G["ink-soft"]}; white-space: nowrap; }}
    #draft {{ position: absolute; right: 40px; top: 36px; font-size: 28px; font-weight: 800; color: {G["main"]}; background: {G["second"]}; padding: 4px 13px; z-index: 5; }}
    .plate {{ position: absolute; inset: 0; background: {G["main"]}; padding: 89px; display: flex; flex-direction: column; gap: 55px; }}
    .plate .pt {{ font-family: "Archivo Black", sans-serif; font-size: 55px; line-height: 1.236; max-width: 1187px; }}
    .plate .pg {{ display: flex; flex-wrap: wrap; gap: 55px 89px; align-items: flex-start; }}
    .plate .pr {{ display: flex; flex-direction: column; gap: 13px; max-width: 610px; }}
    .plate .pr b {{ font-family: "Archivo Black", sans-serif; font-weight: 400; font-size: 144px; line-height: 1; color: {G["ink"]}; }}
    .plate .pr span {{ font: 600 34px/1.236 {SANS}; }}
    .plate .pn {{ font: 700 34px/1.236 {SANS}; color: {G["second"]}; border-left: 8px solid {G["loud"]}; padding-left: 21px; max-width: 1187px; }}
    .plate .pf {{ margin-top: auto; font: 600 28px {SANS}; color: {G["ink-soft"]}; }}
    .stmt {{ position: absolute; inset: 0; background: {G["main"]}; padding: 0 89px 0 733px; display: flex; flex-direction: column; justify-content: center; gap: 34px; }}
    .stmt.dark {{ background: {G["second"]}; color: {G["main"]}; }}
    .stmt .st {{ font-family: "Archivo Black", sans-serif; font-size: 89px; line-height: 1.0; text-wrap: balance; }}
    .stmt .ss {{ font: 600 34px/1.236 {SANS}; opacity: .8; }}
  </style>
  <div id="root" data-composition-id="proto" data-width="1920" data-height="1080">
    <canvas id="gl" width="1920" height="1080" data-layout-ignore></canvas>
{tick_html}
{cap_html}
{card_html}
    <div id="pin"></div>
    <div id="src">{plan.get("src", "Source: NY Fed, recent college graduates by major (2024 data)")}</div>
{chr(10).join("    " + p for p in plan.get("plates", []))}
    <div id="draft">{plan["draft"]}</div>
  </div>
  <script type="module">
    window.__PROTO = {json.dumps(data)};
{(FILM / "src/proto.js").read_text()}
  </script>
</template>
"""
    (out / "compositions").mkdir(parents=True, exist_ok=True)
    (out / "compositions/proto.html").write_text(comp)
    shutil.copytree(FILM / "assets/lib", out / "assets/lib", dirs_exist_ok=True)
    for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(FILM / f, out / f)
    audio = ""
    if plan.get("audio"):
        (out / "assets").mkdir(exist_ok=True); shutil.copy(plan["audio"], out / "assets/voice.wav")
        audio = f'<audio id="vo" src="assets/voice.wav" data-start="0" data-duration="{plan["end"]}" data-track-index="5" data-volume="1"></audio>'
    (out / "index.html").write_text(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script type="importmap">{{"imports": {{"three": "./assets/lib/three.module.js"}}}}</script>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: {C["bg"]}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{plan["end"]}" data-width="1920" data-height="1080">
      <div id="proto" data-composition-id="proto" data-composition-src="compositions/proto.html" data-start="0" data-duration="{plan["end"]}"
           data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      {audio}
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
    print(f"{plan['name']}: {out} · buildings {len(B)} · cards {len(cards)} · ticks {len(plan['ticks'])} · plates {len(plan.get('plates', []))}")
    return out
