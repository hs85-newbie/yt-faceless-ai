"""EP002 스토리라인 C '캠퍼스 지도 비행' — HyperFrames 장면 생성기(모션 테스트 0~89 s).

사용: python3 -I scripts/ep002_campus.py
입력: output/002/02_raw/data/bymajor.csv(NY Fed 전공별 2024), output/002/02_raw/voice_v1/{lines,words}.json,
      output/002/03_work/v1/transcript.srt(줄 시각), output/002/03_work/v1/voice.wav
산출: episodes/002/film/index.html, compositions/campus.html, assets/voice.wav(git 제외)
규칙(SPEC.md): 건물 높이 = 실업률 x 44 px, 카메라는 숏마다 대상 건물 bbox에 맞춤, 라벨은 내레이션 단어 시각에 착지.
"""
import csv, json, re, shutil
from pathlib import Path

R = Path(__file__).resolve().parents[1]
FILM = R / "episodes/002/film"
DATA = R / "output/002/02_raw/data/bymajor.csv"
VOICE = R / "output/002/02_raw/voice_v1"
WORK = R / "output/002/03_work/v1"
END = 89.0
TW, TH, PX = 110, 55, 44          # 타일 폭·높이(px), 실업률 1%p당 높이(px)

# ── 데이터: 전공 → 구역 ──────────────────────────────
QUADS = {   # 구역: (블록 원점 gx, gy), 4x4 칸
    "hum": (0, 0), "eng": (5, 0), "sci": (10, 0), "hed": (0, 5), "soc": (5, 5), "bus": (10, 5)}
ENG = ["Computer Science", "Computer Engineering", "Electrical Engineering", "Mechanical Engineering"]   # 공학 구역 앞줄
CAT = {
    "eng": ENG + ["General Engineering", "Aerospace Engineering", "Chemical Engineering", "Civil Engineering", "Industrial Engineering",
                  "Miscellaneous Engineering", "Engineering Technologies", "Miscellaneous Technologies", "Information Systems & Management",
                  "Architecture", "Construction Services"],
    "hum": ["Art History", "Philosophy", "Fine Arts", "Performing Arts", "Commercial Art & Graphic Design", "Theology and Religion",
            "English Language", "Foreign Language", "Liberal Arts", "History", "Ethnic Studies", "Interdisciplinary Studies",
            "Communications", "Journalism", "Mass Media", "Advertising and Public Relations"],
    "sci": ["Physics", "Mathematics", "Biology", "Biochemistry", "Miscellaneous Biological Science", "Chemistry", "Earth Sciences",
            "Miscellaneous Physical Sciences", "Agriculture", "Animal and Plant Sciences", "Environmental Studies", "Geography"],
    "hed": ["Nutrition Sciences", "Nursing", "Health Services", "Medical Technicians", "Pharmacy", "Treatment Therapy",
            "Family and Consumer Sciences", "General Education", "Early Childhood Education", "Elementary Education",
            "Secondary Education", "Special Education", "Miscellaneous Education"],
    "soc": ["Psychology", "Criminal Justice", "Public Policy and Law", "Social Services", "Anthropology", "Economics",
            "Political Science", "Sociology", "General Social Sciences", "International Affairs"],
    "bus": ["Finance", "General Business", "Accounting", "Business Management", "Business Analytics", "Marketing", "Leisure and Hospitality"],
}
rows = {r["Major"]: r for r in csv.DictReader(DATA.open()) if r["Major"] != "Overall"}
assert sorted(sum(CAT.values(), [])) == sorted(rows), "전공 73개가 구역에 정확히 한 번씩 들어가야 한다"
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
B = []   # 건물: id, name, u(실업률), gx, gy, quad
# 같은 숏에 라벨이 함께 뜨는 건물은 화면 가로로 2칸 이상 떨어뜨린다(라벨 겹침 방지)
POS = {"Computer Science": (5, 3), "Computer Engineering": (7, 3), "Electrical Engineering": (6, 0), "Mechanical Engineering": (8, 0),
       "Physics": (10, 0), "Mathematics": (13, 0), "Art History": (1, 3), "Philosophy": (3, 1), "Nutrition Sciences": (0, 5)}
for q, names in CAT.items():
    ox, oy = QUADS[q]
    free = [(ox + k % 4, oy + k // 4) for k in range(16) if (ox + k % 4, oy + k // 4) not in POS.values()]
    for n in names:
        gx, gy = POS[n] if n in POS else free.pop(0)
        B.append({"id": slug(n), "name": n, "u": round(float(rows[n]["Unemployment Rate"]), 1), "gx": gx, "gy": gy, "q": q})
assert len({(b["gx"], b["gy"]) for b in B}) == len(B), "칸 중복"
B.sort(key=lambda b: (b["gx"] + b["gy"], b["gx"]))   # 그리는 순서(뒤 → 앞)
BY = {b["name"]: b for b in B}


# ── 기하: 등각 투영(월드 px) ──────────────────────────
def iso(gx, gy, h=0.0): return ((gx - gy) * TW / 2, (gx + gy) * TH / 2 - h)
def corners(b, h, a=0.14):
    g = [(b["gx"] + a, b["gy"] + a), (b["gx"] + 1 - a, b["gy"] + a), (b["gx"] + 1 - a, b["gy"] + 1 - a), (b["gx"] + a, b["gy"] + 1 - a)]
    return [iso(x, y, hh) for x, y in g for hh in (0, h)]
def roof(b): x, y = iso(b["gx"] + .5, b["gy"] + .5, b["u"] * PX); return x, y


# ── 시간: 내레이션 단어 시각 ──────────────────────────
secs = lambda s: (lambda h, m, r: int(h) * 3600 + int(m) * 60 + float(r.replace(",", ".")))(*s.split(":"))
lines = json.loads((VOICE / "lines.json").read_text()); words = json.loads((VOICE / "words.json").read_text())
LINE = {l["id"]: secs(a) for l, (a, _) in zip(lines, re.findall(r"(\S+) --> (\S+)", (WORK / "transcript.srt").read_text()))}
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
def at(anchor, lead=0.15):
    lid, _, ph = anchor.partition("@")
    if not ph: return LINE[lid]
    cat, own = "", []
    for k, (w, _, _) in enumerate(words[lid]): n = norm(w); cat += n; own += [k] * len(n)
    i = cat.find(norm(ph)); assert i >= 0, anchor
    return round(LINE[lid] + max(0, words[lid][own[i]][1]) - lead, 2)


# ── 카메라: 대상 건물이 화면 안에 들어오게 ──────────────
def fit(names, extra=(), pad=(240, 300, 170)):
    pts = [p for n in names for p in corners(BY[n], BY[n]["u"] * PX)] + list(extra)
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts); y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    sx, top, bot = pad
    s = min((1920 - 2 * sx) / (x1 - x0), (1080 - top - bot) / (y1 - y0), 1.9)
    return {"s": round(s, 4), "x": round(960 - s * (x0 + x1) / 2, 1), "y": round((top + 1080 - bot) / 2 - s * (y0 + y1) / 2, 1)}
def scr(cam, p): return cam["s"] * p[0] + cam["x"], cam["s"] * p[1] + cam["y"]

ALL = [b["name"] for b in B]
ROAD_END = iso(8.6, -2.6)   # 공학 구역 위쪽 캠퍼스 밖
CS, CE, EE, ME = ENG
SHOTS = [   # (시작 시각, 이동 길이, 대상)
    (0.0, 0.0, fit([CS, CE, EE, ME, "Architecture"], pad=(420, 330, 200))),
    (at("s2_01"), 1.6, fit(ALL, pad=(150, 230, 120))),
    (at("s2_02@grad"), 1.4, fit([CS, "Art History", "Philosophy", "Nutrition Sciences"])),
    (at("s2_03"), 1.4, fit(ALL, pad=(220, 380, 110))),
    (at("s3_01"), 1.6, fit([CS, CE, EE, ME])),
    (at("s3_03"), 1.6, fit(["Physics", "Information Systems & Management", "Mathematics", "Finance", "Nursing"])),
    (at("s3_04@what sets"), 1.4, fit([CS, CE], extra=[ROAD_END], pad=(300, 300, 200))),
]
def cam_at(t): return [c for s, _, c in SHOTS if s <= t][-1]
def shot_end(t): return next((s for s, _, _ in SHOTS if s > t + 0.01), END)


# ── 라벨(HTML 클립): 카메라가 멈춘 숏 안에서만 ─────────
LABELS = []   # (id, 시작, 끝, x, y, 큰 글자, 작은 글자, 종류)
def label(name, t, big=None, small=None, kind="num", dy=0):
    x, y = roof(BY[name])   # 월드 좌표(지붕 중심), 화면 위치는 syncLabels()가 매 프레임 계산, dy = 화면 px 엇갈림
    LABELS.append((f"lbl-{BY[name]['id']}-{int(t * 10)}", t, shot_end(t), round(x, 1), round(y, 1), dy,
                   big if big is not None else f"{BY[name]['u']:.1f}%", small if small is not None else name.upper(), kind))
label(CS, 1.0, big="", small="COMPUTER SCIENCE")
label(CS, at("s1_02@learn to code"), big="SAFE", small="LEARN TO CODE", kind="safe", dy=-70)
label(CE, at("s2_01@second highest"), big="#2", small="COMPUTER ENG. 7.8%", kind="rank", dy=-200)
label(CS, at("s2_01@fourth"), big="#4", small="COMPUTER SCI. 7.0%", kind="rank")
label(CS, at("s2_02@7"), dy=-10)
label("Art History", at("s2_02@art history"))
label("Philosophy", at("s2_02@philosophy"), dy=-170)   # CS와 화면 같은 세로줄
label("Nutrition Sciences", at("s2_02@nutrition"), small="NUTRITION")
label(CS, at("s3_01") + 1.2); label(CE, at("s3_01") + 1.4, dy=-170)
label(EE, at("s3_01@electrical")); label(ME, at("s3_01@mechanical"), dy=-170)
label("Physics", at("s3_03@physics")); label("Information Systems & Management", at("s3_03@information systems"), small="INFO SYSTEMS")
label("Mathematics", at("s3_03@mathematics")); label("Finance", at("s3_03@finance")); label("Nursing", at("s3_03@nursing"))
label(CS, at("s3_04@what sets"), big="", small="COMPUTER SCIENCE"); label(CE, at("s3_04@what sets") + 0.2, big="", small="COMPUTER ENGINEERING", dy=-90)
LEVEL_T = at("s3_02@4"); GREEN_T = at("s3_04@finance and"); ROAD_T = at("s3_04@straight")
TITLE_T = at("s2_03")   # 숏 D 시작과 같이(앞 숏 라벨과 겹치지 않게)
SIGN = {"id": "sign-level", "t": LEVEL_T, "end": shot_end(LEVEL_T)}


# ── HTML 쓰기 ─────────────────────────────────────────
def label_html(l):
    i, t, e, x, y, dy, big, small, kind = l
    big_html = f'<b class="big">{big}</b>' if big else ""
    return (f'<div id="{i}" class="clip lbl {kind}" data-start="{t}" data-duration="{round(e - t, 2)}" data-track-index="2" '
            f'data-wx="{x}" data-wy="{y}" data-oy="{dy}" style="left:0;top:0">{big_html}<span class="small">{small}</span><i class="lead"></i></div>')

ground = [iso(-1.2, -1.2), iso(15.2, -1.2), iso(15.2, 10.2), iso(-1.2, 10.2)]
quads = "".join(f'<polygon class="lawn" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in [iso(ox - .25, oy - .25), iso(ox + 4.25, oy - .25), iso(ox + 4.25, oy + 4.25), iso(ox - .25, oy + 4.25)])}"/>' for ox, oy in QUADS.values())
road = [iso(BY[CS]["gx"] + .5, BY[CS]["gy"] - .2), iso(BY[CS]["gx"] + .5, -1.4), ROAD_END]
bld = "".join(f'<g id="b-{b["id"]}" class="bld{" cs" if b["name"] == CS else " ce" if b["name"] == CE else ""}">'
              f'<polygon class="sh"/><polygon class="l"/><polygon class="r"/><polygon class="t"/></g>' for b in B)
camera_tl = "\n".join(f'    tl.to("#world", {{attr: {{transform: "translate({c["x"]} {c["y"]}) scale({c["s"]})"}}, duration: {d}, ease: "power2.inOut"}}, {s});'
                      for s, d, c in SHOTS[1:])
c0 = SHOTS[0][2]
HI = sorted({(l[0].split("-")[1:-1] and "-".join(l[0].split("-")[1:-1]), l[1], l[2]) for l in LABELS if l[7] == "num"})
hi_tl = "\n".join(   # 라벨이 붙은 동안 그 건물에 검은 윤곽(뒤 건물이 가려도 어느 건물인지 보이게)
    f'    tl.set("#b-{bid} .t, #b-{bid} .l, #b-{bid} .r", {{attr: {{stroke: "#1d2421", "stroke-width": 3}}}}, {t});\n'
    f'    tl.set("#b-{bid} .t, #b-{bid} .l, #b-{bid} .r", {{attr: {{stroke: "none"}}}}, {round(e - 0.01, 2)});'
    for bid, t, e in HI if bid not in (BY[CS]["id"], BY[CE]["id"]))
def pushed(c, k=1.035): return {"s": round(c["s"] * k, 4), "x": round(960 - (960 - c["x"]) * k, 1), "y": round(540 - (540 - c["y"]) * k, 1)}
push_tl = "\n".join(   # 도착 후 다음 숏까지 3.5% 천천히 다가감(정지 화면 방지)
    f'    tl.to("#world", {{attr: {{transform: "translate({p["x"]} {p["y"]}) scale({p["s"]})"}}, duration: {round(shot_end(s + 0.01) - (s + d) - 0.05, 2)}, ease: "sine.inOut"}}, {round(s + d, 2)});'
    for s, d, c in SHOTS for p in [pushed(c)] if shot_end(s + 0.01) - (s + d) > 1.5)
rise_cs = f'    tl.fromTo(H, {{"{BY[CS]["id"]}": 0}}, {{"{BY[CS]["id"]}": {BY[CS]["u"] * PX}, duration: 0.8, ease: "power3.out", onUpdate: draw}}, 0.3);'
wave_t = at("s2_01@major by")
rise_all = "\n".join(f'    tl.fromTo(H, {{"{b["id"]}": 0}}, {{"{b["id"]}": {round(b["u"] * PX, 1)}, duration: 0.8, ease: "power3.out", onUpdate: draw}}, {round(wave_t + (b["gx"] + b["gy"]) * 0.04, 2)});'
                     for b in B if b["name"] != CS)
level = []   # 공학 4동 벽에 4.2% 기준선
for n in ENG:
    p = corners(BY[n], 4.2 * PX); W, S, E = p[7], p[5], p[3]   # (x,y) 순서: 각 꼭짓점 (0,h) 쌍 → 홀수가 높이 h
    level.append(f'<polyline class="lvl" points="{W[0]:.1f},{W[1]:.1f} {S[0]:.1f},{S[1]:.1f} {E[0]:.1f},{E[1]:.1f}"/>')

comp = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; background: #a9c97c; overflow: hidden; font-family: Inter, sans-serif; }}
    #map {{ position: absolute; inset: 0; }}
    .ground {{ fill: #efe6d2; }} .lawn {{ fill: #b9d68c; }}
    .bld .t {{ fill: #e7e2d8; }} .bld .l {{ fill: #c9c2b6; }} .bld .r {{ fill: #aaa397; }} .bld .sh {{ fill: #1d2421; opacity: .18; }}
    .bld.cs .t {{ fill: #f0703f; }} .bld.cs .l {{ fill: #d24e28; }} .bld.cs .r {{ fill: #b8401e; }}
    .bld.ce .t, .bld.ce .l, .bld.ce .r {{ stroke: #e4572e; stroke-width: 4; stroke-linejoin: round; }}
    .lvl {{ fill: none; stroke: #1d2421; stroke-opacity: .6; stroke-width: 3; stroke-dasharray: 10 8; }}
    #road, #road-case {{ fill: none; stroke-linecap: round; stroke-linejoin: round; }}   /* 지도 경로선: 건물 위 레이어 */
    #road {{ stroke: #1d2421; stroke-width: 12; }} #road-case {{ stroke: #efe6d2; stroke-width: 24; }}
    .lbl {{ position: absolute; transform: translate(-50%, -100%); display: flex; flex-direction: column; align-items: center; color: #1d2421; }}
    .lbl .big {{ font-family: "Archivo Black", sans-serif; font-size: 84px; line-height: .95; font-variant-numeric: tabular-nums;
                 background: #efe6d2; padding: 6px 16px 2px; border: 3px solid #1d2421; }}
    .lbl .small {{ font-weight: 700; font-size: 30px; letter-spacing: 0; background: #1d2421; color: #efe6d2; padding: 4px 12px; margin-top: -3px; white-space: nowrap; }}
    .lbl .lead {{ width: 3px; height: 26px; background: #1d2421; }}
    .lbl.rank .big {{ background: #e4572e; color: #fff; border-color: #e4572e; }}
    .lbl.safe .big {{ background: #3f8f5b; color: #fff; border-color: #3f8f5b; }}
    #title {{ position: absolute; left: 50%; top: 150px; transform: translateX(-50%); background: #1d2421; color: #efe6d2;
              font-family: "Archivo Black", sans-serif; font-size: 72px; line-height: 1; padding: 24px 44px; white-space: nowrap; }}
    #sign-level {{ position: absolute; left: 1380px; top: 150px; background: #efe6d2; border: 3px solid #1d2421; padding: 14px 22px;
                   font-weight: 700; font-size: 34px; color: #1d2421; }}
    #sign-road {{ position: absolute; background: #1d2421; color: #efe6d2; font-family: "Archivo Black", sans-serif; font-size: 44px; padding: 16px 26px;
                  transform: translate(-50%, -100%); white-space: nowrap; }}
    #src {{ position: absolute; left: 40px; bottom: 34px; background: rgba(29,36,33,.82); color: #efe6d2; font-size: 28px; padding: 7px 14px; }}
  </style>
  <div id="root" data-composition-id="campus" data-width="1920" data-height="1080">
    <svg id="map" viewBox="0 0 1920 1080" data-layout-ignore>
      <g id="world" transform="translate({c0['x']} {c0['y']}) scale({c0['s']})">
        <polygon class="ground" points="{' '.join(f'{x:.1f},{y:.1f}' for x, y in ground)}"/>{quads}
        <g id="shadows"></g>{bld}
        <g id="levels" opacity="0">{''.join(level)}</g>
        <polyline id="road-case" pathLength="100" stroke-dasharray="100 120" stroke-dashoffset="110" points="{' '.join(f'{x:.1f},{y:.1f}' for x, y in road)}"/>
        <polyline id="road" pathLength="100" stroke-dasharray="100 120" stroke-dashoffset="110" points="{' '.join(f'{x:.1f},{y:.1f}' for x, y in road)}"/>
      </g>
    </svg>
{chr(10).join('    ' + label_html(l) for l in LABELS)}
    <div id="title" class="clip" data-hold data-start="{TITLE_T}" data-duration="{round(at('s3_01') - TITLE_T, 2)}" data-track-index="3">IS COMPUTER SCIENCE STILL WORTH IT?</div>
    <div id="sign-level" class="clip" data-start="{SIGN['t']}" data-duration="{round(SIGN['end'] - SIGN['t'], 2)}" data-track-index="3">ALL MAJORS: 4.2%</div>
    <div id="sign-road" class="clip" data-start="{round(ROAD_T + 0.8, 2)}" data-duration="{round(END - ROAD_T - 0.8, 2)}" data-track-index="3"
         style="left:{scr(SHOTS[-1][2], ROAD_END)[0]:.1f}px;top:{scr(SHOTS[-1][2], ROAD_END)[1] - 20:.1f}px">ENTRY-LEVEL SOFTWARE JOBS</div>
    <div id="src">Source: NY Fed, The Labor Market for Recent College Graduates (2024 data)</div>
  </div>
  <script>
    const B = {json.dumps([{"id": b["id"], "gx": b["gx"], "gy": b["gy"]} for b in B])};
    const H = Object.fromEntries(B.map(b => [b.id, 0]));
    const TW = {TW}, TH = {TH}, A = 0.14;
    const iso = (x, y, h) => [(x - y) * TW / 2, (x + y) * TH / 2 - h];
    const pts = a => a.map(p => p[0].toFixed(1) + "," + p[1].toFixed(1)).join(" ");
    function hull(P) {{   // 그림자 = 바닥 + 높이만큼 오른쪽 아래로 민 바닥의 볼록 껍질
      P = P.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]);
      const c = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
      const lo = [], up = [];
      for (const p of P) {{ while (lo.length > 1 && c(lo[lo.length - 2], lo[lo.length - 1], p) <= 0) lo.pop(); lo.push(p); }}
      for (const p of P.slice().reverse()) {{ while (up.length > 1 && c(up[up.length - 2], up[up.length - 1], p) <= 0) up.pop(); up.push(p); }}
      return lo.slice(0, -1).concat(up.slice(0, -1));
    }}
    const shadows = document.querySelector("#shadows");
    function draw() {{
      for (const b of B) {{
        const h = H[b.id], g = document.getElementById("b-" + b.id);
        const f = [[b.gx + A, b.gy + A], [b.gx + 1 - A, b.gy + A], [b.gx + 1 - A, b.gy + 1 - A], [b.gx + A, b.gy + 1 - A]];
        const lo = f.map(([x, y]) => iso(x, y, 0)), hi = f.map(([x, y]) => iso(x, y, h));
        g.querySelector(".l").setAttribute("points", pts([lo[3], lo[2], hi[2], hi[3]]));
        g.querySelector(".r").setAttribute("points", pts([lo[2], lo[1], hi[1], hi[2]]));
        g.querySelector(".t").setAttribute("points", pts(hi));
        const off = lo.map(p => [p[0] + h * 0.55, p[1] + h * 0.18]);
        g.querySelector(".sh").setAttribute("points", h > 0 ? pts(hull(lo.concat(off))) : "");
      }}
    }}
    draw();
    const tl = gsap.timeline({{ paused: true }});
{rise_cs}
{rise_all}
{camera_tl}
{push_tl}
    const world = document.querySelector("#world"), LBL = [...document.querySelectorAll(".lbl")];
    function syncLabels() {{   // 라벨을 월드 지붕 점에 붙인다(카메라가 밀려도 따라감)
      const m = world.transform.baseVal.consolidate().matrix;
      for (const el of LBL) {{
        const x = +el.dataset.wx, y = +el.dataset.wy;
        el.style.left = (m.a * x + m.c * y + m.e).toFixed(1) + "px";
        el.style.top = (m.b * x + m.d * y + m.f - 26 + +el.dataset.oy).toFixed(1) + "px";
      }}
    }}
    tl.eventCallback("onUpdate", syncLabels); syncLabels();
    tl.fromTo("#levels", {{opacity: 0}}, {{opacity: 1, duration: 0.3}}, {LEVEL_T});
    tl.to("#levels", {{opacity: 0, duration: 0.2}}, {round(shot_end(LEVEL_T) - 0.2, 2)});
    tl.to(["#b-finance .t", "#b-nursing .t"], {{fill: "#3f8f5b", duration: 0.3}}, {GREEN_T});   // CSS 클래스 색을 이기려면 인라인 스타일
    tl.to(["#b-finance .l", "#b-finance .r", "#b-nursing .l", "#b-nursing .r"], {{fill: "#2f6e45", duration: 0.3}}, {GREEN_T});
    tl.fromTo(["#road-case", "#road"], {{attr: {{"stroke-dashoffset": 110}}}}, {{attr: {{"stroke-dashoffset": 0}}, duration: 1.0, ease: "power1.inOut"}}, {ROAD_T});
{hi_tl}
    document.querySelectorAll(".lbl, #title, #sign-level, #sign-road").forEach(el => {{
      const t0 = parseFloat(el.dataset.start);
      tl.fromTo(el.children.length ? el.children : el, {{opacity: 0, scale: 0.85}}, {{opacity: 1, scale: 1, duration: 0.25, ease: "power4.out", stagger: 0.04}}, t0);
    }});
    tl.to({{}}, {{duration: 0.01}}, {END - 0.01});
    window.__timelines["campus"] = tl;
  </script>
</template>
"""
(FILM / "compositions").mkdir(exist_ok=True); (FILM / "assets").mkdir(exist_ok=True)
(FILM / "compositions/campus.html").write_text(comp)
shutil.copy(WORK / "voice.wav", FILM / "assets/voice.wav")
(FILM / ".gitignore").write_text("assets/*.wav\nrenders/\n.hyperframes/\n")
(FILM / "index.html").write_text(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #a9c97c; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1920" data-height="1080">
      <div id="campus" data-composition-id="campus" data-composition-src="compositions/campus.html" data-start="0" data-duration="{END}"
           data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <audio id="vo" src="assets/voice.wav" data-start="0" data-duration="{END}" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
print(f"buildings {len(B)} · labels {len(LABELS)} · shots {len(SHOTS)} · title {TITLE_T} · level {LEVEL_T} · road {ROAD_T}")
