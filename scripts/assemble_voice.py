"""줄별 wav를 하나의 내레이션으로 잇고, 장면 시간표(scenes.txt)와 자막(transcript.srt)을 만든다.

사용: <lemo venv python> scripts/assemble_voice.py output/001/02_raw/voice_v4 output/001/03_work/v4
간격: 같은 장면 안 0.25초, 장면 사이 0.6초, pauses.json이 있으면 해당 줄 뒤에 추가. 장면 경계가 곧 합성·숏폼 자르기 기준이다.
"""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

voice_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
GAP_LINE, GAP_SCENE = 0.12, 0.35  # 2026-11-03 사용자: 중간 쉼 더 줄임
lines = json.loads((voice_dir / "lines.json").read_text(encoding="utf-8"))
words = json.loads((voice_dir / "words.json").read_text(encoding="utf-8")) if (voice_dir / "words.json").exists() else {}
# 선택: pauses.json {줄 id: 초} — 그 줄 뒤에 쉼을 더한다(제목 드롭처럼 화면만 보여 주는 구간)
# WHY: output/은 깃 제외라 쉼 설정이 기기마다 사라졌다 → 레포 episodes/NNN/pauses.json을 먼저 본다(2026-11-04)
ep_pauses = voice_dir.resolve().parents[3] / "episodes" / voice_dir.resolve().parents[1].name / "pauses.json"   # output/NNN/02_raw/voice_vX
pause_file = ep_pauses if ep_pauses.exists() else voice_dir / "pauses.json"
pauses = json.loads(pause_file.read_text(encoding="utf-8")) if pause_file.exists() else {}
print(f"pauses: {pause_file} {pauses}")


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
        gap += pauses.get(lines[i - 1]["id"], 0.0)
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
