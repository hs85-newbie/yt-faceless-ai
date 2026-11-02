"""v4 큐시트(구절 기준)를 음성 시간표에 맞춰 cuts.json(초 기준)으로 바꾸고 렌더 폴더를 꾸린다.

사용: python3 -I scripts/build_film_v4.py episodes/001 output/001/v4 [끝 앵커]
  끝 앵커(예: s3_04$)를 주면 그 시각에서 자른다 → 모션 테스트용.
입력: <ep>/film_v4/cuesheet.json, <out>/transcript.srt, <out>/../voice_v4/{lines,words}.json, <out>/../pages/*_marks.json, <out>/../paper_cut/*.png
규칙: 컷 하나 = 생각 하나 + 그림 하나(글자만 있는 컷 금지), 전환은 하드 컷뿐.
"""
import json, re, shutil, sys
from pathlib import Path
from PIL import Image

ep, out = Path(sys.argv[1]), Path(sys.argv[2]); root = out.parent
film = out / "film"; film.mkdir(parents=True, exist_ok=True)
sheet = json.loads((ep / "film_v4" / "cuesheet.json").read_text(encoding="utf-8"))["cuts"]
lines = json.loads((root / "voice_v4" / "lines.json").read_text(encoding="utf-8"))
words = json.loads((root / "voice_v4" / "words.json").read_text(encoding="utf-8"))
secs = lambda s: (lambda h, m, r: int(h) * 3600 + int(m) * 60 + float(r.replace(",", ".")))(*s.split(":"))
spans = re.findall(r"(\S+) --> (\S+)", (out / "transcript.srt").read_text(encoding="utf-8"))
assert len(spans) == len(lines), "srt와 lines.json 줄 수 불일치"
LINE = {l["id"]: (secs(a), secs(b)) for l, (a, b) in zip(lines, spans)}
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def resolve(anchor):
    """'s2_01' 줄 시작 / 's2_01$' 줄 끝 / 's2_01@구절' 그 구절 첫 단어 시작."""
    if anchor.endswith("$"): return LINE[anchor[:-1]][1]
    lid, _, phrase = anchor.partition("@"); t0 = LINE[lid][0]
    if not phrase: return t0
    cat, owner = "", []
    for k, (w, _, _) in enumerate(words[lid]): n = norm(w); cat += n; owner += [k] * len(n)
    i = cat.find(norm(phrase))
    if i < 0: raise SystemExit(f"구절을 못 찾음: {anchor} | 받아쓰기: {' '.join(w for w, _, _ in words[lid])}")
    return t0 + words[lid][owner[i]][1]


cuts = []
for c in sheet:
    c = json.loads(json.dumps(c)); c["t"] = round(resolve(c.pop("at")), 3); cuts.append(c)
end = resolve(sys.argv[3]) + 1.0 if len(sys.argv) > 3 else None
if end: cuts = [c for c in cuts if c["t"] < end]
for i, c in enumerate(cuts):
    nxt = cuts[i + 1]["t"] if i + 1 < len(cuts) else (end or c["t"] + c.get("d", 4.0))
    c["d"] = round(nxt - c["t"], 3); assert c["d"] > 0.8, f"너무 짧은 컷 #{i} ({c['d']}s)"
    assert any(p["t"] != "card" for p in c.get("props", [])), f"컷 #{i}: 글자만 있는 컷"
    for p in c.get("props", []):
        p["at"] = max(0.0, round(resolve(p["at"]) - c["t"] - 0.15, 3)) if isinstance(p.get("at"), str) else p.get("at", 0.0)
        if p["t"] == "cutout":
            src = root / "paper_cut" / f"{p['img']}.png"; w, h = Image.open(src).size
            p["img"] = src.name; p["ar"] = round(w / h, 4); shutil.copy(src, film / src.name)
        if p["t"] == "doc":
            m = json.loads((root / "pages" / f"{p['page']}_marks.json").read_text(encoding="utf-8"))[p.pop("mark")]
            pad = p.pop("pad", 90); x0, y0 = max(0, m["x"] - pad), max(0, m["y"] - pad)
            p["crop"] = {"x": x0, "y": y0, "w": min(1920 - x0, m["w"] + 2 * pad), "h": min(1080 - y0, m["h"] + 2 * pad)}
            if p.pop("highlight", False): p["hl"] = {k: m[k] for k in "xywh"}
            p["img"] = m["file"]; shutil.copy(root / "pages" / m["file"], film / m["file"])
for f in ("index.html", "world.js"): shutil.copy(ep / "film_v4" / f, film / f)
shutil.copy(ep / "film_v3" / "lib3d.js", film / "lib3d.js")
shutil.copy(Path.home() / "lemo-opuscar/node_modules/three/build/three.module.js", film / "three.module.js")
(film / "cuts.json").write_text(json.dumps({"cuts": cuts}, ensure_ascii=False, indent=1), encoding="utf-8")
lens = [c["d"] for c in cuts]
print(f"cuts {len(cuts)} · film {cuts[-1]['t'] + cuts[-1]['d']:.1f}s · avg {sum(lens) / len(lens):.1f}s · min {min(lens):.1f}s · max {max(lens):.1f}s")
