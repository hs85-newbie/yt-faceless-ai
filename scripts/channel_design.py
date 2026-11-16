"""채널 디자인 시안: EP001과 같은 3D 종이 세계로 배너 2종 + 프로필 1종을 렌더한다(영상 생성 AI 없음, 비용 0).

사용: <lemo venv python> scripts/channel_design.py output/001/03_work/v4/film output/channel
산출: banner_A.png·banner_B.png(2048x1152), banner_*_safe.jpg(모바일 안전영역 1235x338 표시), avatar.png(800x800), avatar_preview.jpg(원형 미리보기)
"""
import json, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

src, out = Path(sys.argv[1]), Path(sys.argv[2])
film = out / "film"; film.mkdir(parents=True, exist_ok=True)
for f in src.iterdir():
    if f.suffix in (".js", ".html") or f.name.startswith("p_"): shutil.copy(f, film / f.name)


def ar(img): w, h = Image.open(film / f"{img}.png").size; return round(w / h, 4)
def cut(img, h, x, z, **kw): return {"t": "cutout", "img": f"{img}.png", "ar": ar(img), "h": h, "x": x, "z": z, "at": 0, **kw}
def card(lines, h, x, z, **kw): return {"t": "card", "lines": lines, "h": h, "x": x, "z": z, "at": 0, **kw}
TITLE = [{"text": "COUNTER LEDGER", "size": 190}]
TAG = ["AI x ECONOMY, CHECKED AGAINST THE SOURCE"]

A = [card(TITLE, 1.15, 0, 0.6, bg="mustard", y=2.75, lean=0),
     card(TAG, 0.42, 0, 0.6, y=2.2, lean=0, nostick=True),   # 이름·소개 모두 모바일 안전영역 안
     cut("p_grad_front", 3.4, -5.0, -0.6),
     {"t": "magnifier", "keys": [{"at": 0, "x": -3.0, "y": 1.9, "z": 1.2}]},
     {"t": "bar", "v": 1.4, "u": 1, "color": "mustardPale", "x": 3.4, "z": -0.4, "at": -1, "wd": 0.9},
     {"t": "bar", "v": 2.2, "u": 1, "color": "mustard", "x": 4.5, "z": -0.4, "at": -1, "wd": 0.9},
     {"t": "bar", "v": 3.0, "u": 1, "color": "red", "x": 5.6, "z": -0.4, "at": -1, "wd": 0.9}]
B = [{"t": "timeline", "years": list(range(2017, 2027)), "w": 8.0, "x": 0, "z": -1.6, "y": 0.4, "at": 0},
     card(TITLE, 1.15, 0, -0.4, bg="red", fg="paper", y=2.95, lean=0, nostick=True),
     card(TAG, 0.42, 0, -0.4, bg="mustard", y=2.4, lean=0, nostick=True),
     cut("p_res_1", 2.8, -6.6, -0.4, ry=8), cut("p_res_2", 2.7, -5.2, -0.6),
     cut("p_remote", 2.4, 5.0, -0.4), cut("p_robot_task", 2.4, 6.6, -0.6)]
P = [card([{"text": "CL", "size": 300}], 2.6, 0, 1.2, bg="mustard", y=0.9, lean=0)]   # 프로필은 ~100px로 보이니 카드 하나만
cuts = [{"t": i * 4.0, "d": 4.0, "props": p} for i, p in enumerate([A, B, P])]
(film / "cuts.json").write_text(json.dumps({"cuts": cuts}, ensure_ascii=False))
subprocess.run(["node", str(Path.home() / "lemo-opuscar/core/render/still.mjs"), str(film), "3.5", "7.5", "11.5", "--out", str(out / "raw")], check=True)

SAFE = (406, 407, 1641, 745)   # 2048x1152 배너에서 모든 기기에 보이는 가운데 1235x338
for name, t in (("A", "3.5"), ("B", "7.5")):
    im = Image.open(out / "raw" / f"t_{t}.jpg").convert("RGB").resize((2048, 1152), Image.LANCZOS)
    im.save(out / f"banner_{name}.png")
    pv = im.copy(); d = ImageDraw.Draw(pv); d.rectangle(SAFE, outline="#ff3b30", width=6)
    pv.resize((1024, 576)).save(out / f"banner_{name}_safe.jpg", quality=88)
im = Image.open(out / "raw" / "t_11.5.jpg").convert("RGB")
w, h = im.size; s = int(h * 0.62); cx, cy = w // 2, int(h * 0.60)
av = im.crop((cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2)).resize((800, 800), Image.LANCZOS)
av.save(out / "avatar.png")
mask = Image.new("L", (800, 800), 0); ImageDraw.Draw(mask).ellipse((0, 0, 800, 800), fill=255)
pv = Image.new("RGB", (800, 800), "#0f0f0f"); pv.paste(av, (0, 0), mask); pv.resize((400, 400)).save(out / "avatar_preview.jpg", quality=88)
print("ok", sorted(p.name for p in out.iterdir() if p.is_file()))
