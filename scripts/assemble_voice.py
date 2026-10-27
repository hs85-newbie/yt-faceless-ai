"""줄별 wav를 하나의 내레이션으로 잇고, 장면 시간표(scenes.txt)와 자막(transcript.srt)을 만든다.

사용: <lemo venv python> scripts/assemble_voice.py output/001/voice output/001
간격: 같은 장면 안 0.5초, 장면 사이 1.0초. 장면 경계가 곧 합성·숏폼 자르기 기준이다.
"""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

voice_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
GAP_LINE, GAP_SCENE = 0.5, 1.0
lines = json.loads((voice_dir / "lines.json").read_text(encoding="utf-8"))
words = json.loads((voice_dir / "words.json").read_text(encoding="utf-8")) if (voice_dir / "words.json").exists() else {}


def fmt(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"


chunks, srt, scenes, cursor, sr = [], [], {}, 0.0, None
for i, line in enumerate(lines):
    audio, rate = sf.read(voice_dir / f"{line['id']}.wav", dtype="float32")
    assert sr in (None, rate), "샘플레이트 불일치"
    sr = rate
    if i > 0:
        gap = GAP_SCENE if lines[i - 1]["scene"] != line["scene"] else GAP_LINE
        chunks.append(np.zeros(int(gap * sr), dtype="float32")); cursor += gap
    start, dur = cursor, len(audio) / sr
    chunks.append(audio); cursor += dur
    srt.append(f"{len(srt) + 1}\n{fmt(start)} --> {fmt(cursor)}\n{line['text']}\n")
    sc = scenes.setdefault(line["scene"], {"start": start, "end": cursor, "lines": []})
    sc["end"] = cursor; sc["lines"].append(line["id"])

out_dir.mkdir(parents=True, exist_ok=True)
sf.write(out_dir / "voice.wav", np.concatenate(chunks), sr)
(out_dir / "transcript.srt").write_text("\n".join(srt), encoding="utf-8")
rows = ["scene\tstart_sec\tend_sec\tlines"] + [f"{k}\t{v['start']:.3f}\t{v['end']:.3f}\t{','.join(v['lines'])}" for k, v in scenes.items()]
(out_dir / "scenes.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
assert abs(cursor - sum(len(c) for c in chunks) / sr) < 0.01
print(f"voice.wav {cursor/60:.1f} min, {len(lines)} lines, {len(scenes)} scenes -> {out_dir}")
