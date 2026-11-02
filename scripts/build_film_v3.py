"""큐시트(구절 기준)를 음성 시간표에 맞춰 cuts.json(초 기준)으로 바꾸고, 렌더 폴더를 꾸리고, 컷 다양성 규칙을 검사한다.

사용: python3 -I scripts/build_film_v3.py episodes/001 output/001/v3
입력: <ep>/film_v3/cuesheet.json, <out>/transcript.srt, <out>/../voice_v3/{lines,words}.json, <out>/../pages/*_marks.json
출력: <out>/film/ (index.html·js·three.module.js·이미지·cuts.json)
규칙(yt-pipeline 6단계): 연속 5컷 안 같은 틀 2회 이하, 전환 4종 이상. 어기면 목록을 찍고 종료 코드 1.
"""
import json, re, shutil, sys
from pathlib import Path

ep, out = Path(sys.argv[1]), Path(sys.argv[2])
root = out.parent                      # output/001
film = out / "film"; film.mkdir(parents=True, exist_ok=True)
sheet = json.loads((ep / "film_v3" / "cuesheet.json").read_text(encoding="utf-8"))["cuts"]
lines = json.loads((root / "voice_v3" / "lines.json").read_text(encoding="utf-8"))
words = json.loads((root / "voice_v3" / "words.json").read_text(encoding="utf-8"))

# 줄 시작·끝(초): assemble_voice가 쓴 transcript.srt 순서 = lines.json 순서
def secs(s):
    h, m, r = s.split(":"); sec, ms = r.split(","); return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000
spans = re.findall(r"(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})", (out / "transcript.srt").read_text(encoding="utf-8"))
assert len(spans) == len(lines), "srt와 lines.json 줄 수 불일치"
LINE = {l["id"]: (secs(a), secs(b)) for l, (a, b) in zip(lines, spans)}
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def resolve(anchor):
    """'s2_01' 줄 시작 / 's2_01$' 줄 끝 / 's2_01@구절' 그 구절 첫 단어 시작."""
    if anchor.endswith("$"): return LINE[anchor[:-1]][1]
    lid, _, phrase = anchor.partition("@")
    t0 = LINE[lid][0]
    if not phrase: return t0
    ws = words[lid]; cat, owner = "", []
    for k, (w, _, _) in enumerate(ws):
        n = norm(w); cat += n; owner += [k] * len(n)
    i = cat.find(norm(phrase))
    if i < 0: raise SystemExit(f"구절을 못 찾음: {anchor} | 받아쓰기: {' '.join(w for w, _, _ in ws)}")
    return t0 + ws[owner[i]][1]


def rel(v, t):   # 문자열 앵커면 컷 시작 기준 초, 숫자면 그대로
    is_anchor = isinstance(v, str) and re.match(r"^s\d+b?_\d\d", v)
    return max(0.0, round(resolve(v) - t - 0.08, 3)) if is_anchor else v


def layout(strips, has_stamp):   # x·y 없는 띠: 화면 가운데에 세로로 쌓는다
    auto = [s for s in strips if "x" not in s]
    hs = [s.get("size", 90) * 1.08 + 18 for s in auto]
    y = (1080 - sum(hs) - 34 * (len(hs) - 1)) / 2 - (120 if has_stamp else 30)
    for i, (s, h) in enumerate(zip(auto, hs)):
        s.update(x=150 + (i % 2) * 70, y=round(y), rot=s.get("rot", -1.5 if i % 2 == 0 else 1.2)); y += h + 34


cuts, imgs = [], set()
for c in sheet:
    c = json.loads(json.dumps(c)); c["t"] = round(resolve(c.pop("at")), 3); cuts.append(c)
for i, c in enumerate(cuts):
    c["d"] = round(cuts[i + 1]["t"] - c["t"], 3) if i + 1 < len(cuts) else c.get("d", 4.0)
    assert c["d"] > 0.4, f"너무 짧은 컷 #{i} ({c['d']}s)"
    for s in c.get("strips", []) + ([c["stamp"]] if "stamp" in c else []):
        s["at"] = rel(s.get("at", 0.1), c["t"])
    for k, v in list(c.get("opt", {}).items()):
        c["opt"][k] = rel(v, c["t"])
    if c["k"] == "kin": layout(c.get("strips", []), "stamp" in c)
    els = c.get("strips", []) + ([c["stamp"]] if "stamp" in c else [])
    if c["k"] == "kin" and els:   # 빈 매트로 시작하지 않게(motionmaxxing G2): 첫 요소는 컷 시작에 이미 떨어지는 중
        min(els, key=lambda e: e["at"])["at"] = -0.12
    if c["k"] == "doc":
        m = json.loads((root / "pages" / f"{c['page']}_marks.json").read_text(encoding="utf-8"))[c.pop("mark")]
        c["img"], c["mark"] = m["file"], {k: m[k] for k in "xywh"}; shutil.copy(root / "pages" / m["file"], film / m["file"])
        if c.get("desk"): imgs.add(root / "styleboard" / "sb3_document.png")
    if c["k"] in ("collage", "print"):
        src = root / ("assets" if c["k"] == "print" else "styleboard") / c["img"]; imgs.add(src)
for f in imgs: shutil.copy(f, film / f.name)
for f in ("index.html", "film.js", "scenes3d.js", "lib3d.js"): shutil.copy(ep / "film_v3" / f, film / f)
shutil.copy(Path.home() / "lemo-opuscar/node_modules/three/build/three.module.js", film / "three.module.js")
(film / "cuts.json").write_text(json.dumps({"cuts": cuts}, ensure_ascii=False, indent=1), encoding="utf-8")

# —— 컷 다양성 검사 ——
key = lambda c: c["k"] + ":" + str(c.get("scene") or c.get("img") or c.get("bg") or "mat")
bad = [(i, key(c)) for i in range(len(cuts)) for c in [cuts[i]] if sum(key(x) == key(c) for x in cuts[max(0, i - 4):i + 1]) > 2]
trs = sorted({c.get("tr", "cut") for c in cuts})
lens = [c["d"] for c in cuts]
print(f"cuts {len(cuts)} · film {cuts[-1]['t'] + cuts[-1]['d']:.1f}s · avg {sum(lens) / len(lens):.1f}s · max {max(lens):.1f}s · transitions {trs}")
print("kinds", {k: sum(c['k'] == k for c in cuts) for k in sorted({c['k'] for c in cuts})})
if bad or len(trs) < 4:
    print("다양성 위반:", bad, "전환 종류", len(trs)); sys.exit(1)
print("diversity OK")
