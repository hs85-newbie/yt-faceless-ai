"""대본(03_script.md)에서 낭독 문장을 장면별로 뽑아 TTS 입력(lines.json)과 장면 계획(scenes_plan.json)을 만든다.

사용: python3 -I scripts/extract_lines.py episodes/001/03_script.md output/001/voice am_michael
"""
import json
import re
import sys
from pathlib import Path

script_path, out_dir, voice = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
text = script_path.read_text(encoding="utf-8")
body = text.split("## 1. Hook")[1].split("## 화면 출처 메모")[0]
parts = re.split(r"^## (\d+b?)\. (.*)$", body, flags=re.M)
blocks = [("1", "Hook", parts[0])] + [(parts[i], parts[i + 1].strip(), parts[i + 2]) for i in range(1, len(parts), 3)]

lines, scenes = [], []
for sid, title, txt in blocks:
    k = 0
    for para in re.split(r"\n\s*\n", txt):
        if para.lstrip().startswith("`"):  # 화면 지시 단락은 통째로 제외 (화살표로 이어진 것 포함)
            continue
        para = re.sub(r"`[^`]*`", "", para).strip()
        if not para or para.startswith("#") or not re.search(r"[A-Za-z]", para):  # 구분선·기호만 있는 줄 제외
            continue
        k += 1
        lines.append({"id": f"s{sid}_{k:02d}", "scene": sid, "text": para, "voice": voice, "speed": 0.92, "lang": "en-us"})
    scenes.append({"scene": sid, "title": title, "n_lines": k})

out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "lines.json").write_text(json.dumps(lines, ensure_ascii=False, indent=1), encoding="utf-8")
(out_dir / "scenes_plan.json").write_text(json.dumps(scenes, ensure_ascii=False, indent=1), encoding="utf-8")
assert lines and all(l["text"] for l in lines), "빈 문장"
print(len(lines), "lines in", len(scenes), "scenes:", [(s["scene"], s["n_lines"]) for s in scenes])
