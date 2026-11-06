"""EP002 최종본 화면: 3D 캠퍼스 비행(HyperFrames + three.js r170, MIT). 모션 테스트 구간 0~89 s.

사용: python3 -I scripts/ep002_campus3d.py
산출: episodes/002/film/index.html, compositions/campus3d.html, assets/voice.wav(git 제외)
조합: HyperFrames(시간·렌더·점검) + three.js(세계·빛·그림자·틸트시프트) + 레지스트리 three 블록 패턴(상태 트윈 → render)
규칙: 건물 높이 = 실업률 x HS, 건물은 땅속에서 솟는다(창문이 늘어나지 않게), 라벨은 3D 지붕을 매 프레임 화면에 투영,
      숫자는 하나씩 카운트업, 카메라는 숏마다 대상 건물 bbox에 맞춤. 2D 콘셉트(ep002_campus.py)와 같은 숏·라벨 시각.
"""
import json, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))   # python3 -I는 스크립트 폴더를 경로에 넣지 않는다
from ep002_common import R, WORK, QUADS, QNAME, CS, CE, EE, ME, buildings, at

FILM = R / "episodes/002/film"
END = 89.0
HS = 0.18                      # 실업률 1%p당 높이(월드 단위, 칸 = 1)
B = buildings(); BY = {b["name"]: b for b in B}

SHOTS = [   # (시작 s, 이동 s, 대상 전공, 방위각 보정 도)
    (0.0, 0.0, ["GATE", CS, "Nursing", "Psychology", "Finance"], 0),   # 정문 뒤에서 캠퍼스를 들여다보는 첫 구도
    (2.6, 1.8, [CS, CE, EE, ME, "Architecture"], -8),
    (at("s2_01"), 1.8, "ALL", 4),
    (at("s2_02@grad"), 1.6, [CS, "Art History", "Philosophy", "Nutrition Sciences"], -12),
    (at("s2_03"), 1.6, "ALL", 0),
    (at("s3_01"), 1.8, [CS, CE, EE, ME], 10),
    (at("s3_03"), 1.8, ["Physics", "Information Systems & Management", "Mathematics", "Finance", "Nursing"], -6),
    (at("s3_04@what sets"), 1.6, [CS, CE, "ROAD_END"], 14),
]
def shot_end(t): return next((s for s, *_ in SHOTS if s > t + 0.01), END)

LABELS = []
def label(name, t, big=None, small=None, kind="num", dy=0, count=True):
    b = BY[name]
    LABELS.append({"id": f"lbl-{b['id']}-{int(t * 10)}", "bid": b["id"], "t": t, "e": shot_end(t), "dy": dy, "kind": kind,
                   "big": f"{b['u']:.1f}%" if big is None else big, "small": name.upper() if small is None else small,
                   "count": b["u"] if (count and big is None) else None})
label(CS, 1.0, big="", small="COMPUTER SCIENCE")
label(CS, at("s1_02@learn to code"), big="SAFE", small="LEARN TO CODE", kind="safe", dy=-90)
label(CE, at("s2_01@second highest"), big="#2", small="COMPUTER ENG. 7.8%", kind="rank", dy=-190)
label(CS, at("s2_01@fourth"), big="#4", small="COMPUTER SCI. 7.0%", kind="rank")
label(CS, at("s2_02@7"))
label("Art History", at("s2_02@art history"))
label("Philosophy", at("s2_02@philosophy"), dy=-170)
label("Nutrition Sciences", at("s2_02@nutrition"), small="NUTRITION")
label(CS, at("s3_01") + 1.2); label(CE, at("s3_01") + 1.4, dy=-200)
label(EE, at("s3_01@electrical")); label(ME, at("s3_01@mechanical"), dy=-170)
label("Physics", at("s3_03@physics")); label("Information Systems & Management", at("s3_03@information systems"), small="INFO SYSTEMS")
label("Mathematics", at("s3_03@mathematics")); label("Finance", at("s3_03@finance")); label("Nursing", at("s3_03@nursing"))
label(CS, at("s3_04@what sets"), big="", small="COMPUTER SCIENCE"); label(CE, at("s3_04@what sets") + 0.2, big="", small="COMPUTER ENGINEERING", dy=-80)

EV = {"cs_rise": 0.3, "majors73": at("s1_01@73"), "wave": at("s2_01@major by"), "level": at("s3_02@4"), "green": at("s3_04@finance and"),
      "road": at("s3_04@straight"), "title": at("s2_03"), "title_end": at("s3_01"),
      "q_end": at("s2_02@grad"), "gate_end": at("s2_01")}
WORLD = {"B": [{k: b[k] for k in ("id", "name", "u", "gx", "gy", "q")} for b in B], "HS": HS, "QUADS": QUADS, "QNAME": QNAME,
         "SHOTS": [{"t": s, "d": d, "who": w, "az": a} for s, d, w, a in SHOTS], "EV": EV, "END": END,
         "CS": BY[CS]["id"], "CE": BY[CE]["id"], "ENG": [BY[n]["id"] for n in (CS, CE, EE, ME)],
         "GREEN": ["finance", "nursing"], "LABELS": [{k: l[k] for k in ("id", "bid", "t", "e", "count")} for l in LABELS]}


qlbls = "\n".join(f'    <div id="q-{q}" class="clip qlbl" data-start="0" data-duration="{EV["q_end"]}" data-track-index="4" '
                  f'data-wx="{ox + 2}" data-wy="0.5" data-wz="{oy + 4.6}" data-oy="0">{QNAME[q]}</div>' for q, (ox, oy) in QUADS.items())


def label_html(l):
    big = f'<b class="big">{l["big"]}</b>' if l["big"] else ""
    return (f'<div id="{l["id"]}" class="clip lbl {l["kind"]}" data-start="{l["t"]}" data-duration="{round(l["e"] - l["t"], 2)}" '
            f'data-track-index="2" data-bid="{l["bid"]}" data-oy="{l["dy"]}">{big}<span class="small">{l["small"]}</span><i class="lead"></i></div>')


comp = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; background: #9fc27a; overflow: hidden; font-family: Inter, sans-serif; }}
    #gl {{ position: absolute; inset: 0; width: 1920px; height: 1080px; }}
    .lbl {{ position: absolute; left: 0; top: 0; transform: translate(-50%, -100%); display: flex; flex-direction: column; align-items: center; color: #1d2421; }}
    .lbl .big {{ font-family: "Archivo Black", sans-serif; font-size: 80px; line-height: .95; font-variant-numeric: tabular-nums;
                 background: #f4ecdc; padding: 8px 18px 2px; border: 3px solid #1d2421; box-shadow: 6px 6px 0 rgba(29,36,33,.25); }}
    .lbl .small {{ font-weight: 700; font-size: 30px; background: #1d2421; color: #f4ecdc; padding: 4px 12px; margin-top: -3px; white-space: nowrap; }}
    .qlbl {{ position: absolute; left: 0; top: 0; transform: translate(-50%, -50%); background: #24453a; color: #fff; font-weight: 800;
             font-size: 30px; padding: 8px 18px; border-radius: 3px; white-space: nowrap; box-shadow: 0 4px 0 rgba(0,0,0,.25); }}
    .qlbl.jobs {{ background: #1d2421; font-family: "Archivo Black", sans-serif; font-weight: 400; font-size: 40px; padding: 14px 24px; }}
    .lbl .lead {{ width: 3px; height: 30px; background: #1d2421; }}
    .lbl.rank .big {{ background: #e4572e; color: #fff; border-color: #a63a1c; }}
    .lbl.safe .big {{ background: #3f8f5b; color: #fff; border-color: #2c6a42; }}
    #title {{ position: absolute; left: 50%; top: 120px; transform: translateX(-50%); background: #1d2421; color: #f4ecdc;
              font-family: "Archivo Black", sans-serif; font-size: 72px; line-height: 1; padding: 24px 44px; white-space: nowrap; }}
    #sign-level {{ position: absolute; right: 96px; top: 120px; background: rgba(244,236,220,.92); border: 3px solid #1d2421; padding: 14px 22px;
                   font-weight: 700; font-size: 34px; color: #1d2421; }}
    #sign-level b {{ font-family: "Archivo Black", sans-serif; font-weight: 400; }}
    #src {{ position: absolute; left: 40px; bottom: 34px; background: rgba(29,36,33,.82); color: #f4ecdc; font-size: 28px; padding: 7px 14px; }}
  </style>
  <div id="root" data-composition-id="campus3d" data-width="1920" data-height="1080">
    <canvas id="gl" width="1920" height="1080" data-layout-ignore></canvas>
{chr(10).join('    ' + label_html(l) for l in LABELS)}
    <div id="title" class="clip" data-hold data-start="{EV['title']}" data-duration="{round(EV['title_end'] - EV['title'], 2)}" data-track-index="3">IS COMPUTER SCIENCE STILL WORTH IT?</div>
    <div id="sign-level" class="clip" data-start="{EV['level']}" data-duration="{round(shot_end(EV['level']) - EV['level'], 2)}" data-track-index="3">ALL MAJORS: <b>4.2%</b></div>
{qlbls}
    <div id="q-jobs" class="clip qlbl jobs" data-start="{round(EV['road'] + 0.9, 2)}" data-duration="{round(END - EV['road'] - 0.9, 2)}" data-track-index="4"
         data-wx="9.5" data-wy="1.25" data-wz="-3.2" data-oy="0">ENTRY-LEVEL SOFTWARE JOBS</div>
    <div id="src">Source: NY Fed, The Labor Market for Recent College Graduates (2024 data)</div>
  </div>
  <script type="module">
    window.__WORLD = {json.dumps(WORLD)};
{(FILM / "src/campus3d.js").read_text()}
  </script>
</template>
"""
(FILM / "compositions/campus3d.html").write_text(comp)
shutil.copy(WORK / "voice.wav", FILM / "assets/voice.wav")
(FILM / "index.html").write_text(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script type="importmap">{{"imports": {{"three": "./assets/lib/three.module.js"}}}}</script>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #9fc27a; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1920" data-height="1080">
      <div id="campus3d" data-composition-id="campus3d" data-composition-src="compositions/campus3d.html" data-start="0" data-duration="{END}"
           data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <audio id="vo" src="assets/voice.wav" data-start="0" data-duration="{END}" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
print(f"3D: buildings {len(B)} · labels {len(LABELS)} · shots {len(SHOTS)} · events {EV}")
