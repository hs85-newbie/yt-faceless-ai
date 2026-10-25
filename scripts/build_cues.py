"""내레이션 시간표(transcript.srt + scenes.txt)를 장면 페이지가 읽는 cues.json으로 바꾼다.

사용: python3 -I scripts/build_cues.py output/001 episodes/001/film
출력: <film>/cues.json = {"dur": 초, "scenes": [{"id","start","end"}], "lines": [{"id","scene","t0","t1","text"}]}
"""
import json
import re
import sys
from pathlib import Path

out_dir, film_dir = Path(sys.argv[1]), Path(sys.argv[2])
voice_lines = json.loads((out_dir / "voice" / "lines.json").read_text(encoding="utf-8"))


def sec(ts):
    h, m, s = ts.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


blocks = re.findall(r"\d+\n(\S+) --> (\S+)\n(.+?)\n", (out_dir / "transcript.srt").read_text(encoding="utf-8") + "\n")
assert len(blocks) == len(voice_lines), (len(blocks), len(voice_lines))
lines = [{"id": vl["id"], "scene": vl["scene"], "t0": sec(a), "t1": sec(b), "text": txt} for (a, b, txt), vl in zip(blocks, voice_lines)]

scenes = []
for row in (out_dir / "scenes.txt").read_text(encoding="utf-8").splitlines()[1:]:
    sid, start, end, _ = row.split("\t")
    scenes.append({"id": sid, "start": float(start), "end": float(end)})

dur = round(scenes[-1]["end"] + 1.0, 3)  # 마지막 장면 뒤 1초 여유(끝 화면)
film_dir.mkdir(parents=True, exist_ok=True)
(film_dir / "cues.json").write_text(json.dumps({"dur": dur, "scenes": scenes, "lines": lines}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"cues.json: dur {dur}s, {len(scenes)} scenes, {len(lines)} lines")
