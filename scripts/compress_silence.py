"""줄별 음성 안의 긴 침묵(문장 사이 쉼)을 줄이고, 단어 시각(words.json)을 같은 만큼 당긴다.

사용: ~/lemo-opuscar/.venv/bin/python scripts/compress_silence.py output/001/02_raw/voice_v4 [최대쉼초=0.16] [기준초=0.28]
원본은 <dir>/orig/에 한 번만 백업하고, 다시 돌리면 항상 원본에서 새로 만든다(누적 압축 방지).
"""
import json, shutil, sys
from pathlib import Path

import numpy as np
import soundfile as sf

d = Path(sys.argv[1]); KEEP = float(sys.argv[2]) if len(sys.argv) > 2 else 0.16; MIN = float(sys.argv[3]) if len(sys.argv) > 3 else 0.28
orig = d / "orig"; orig.mkdir(exist_ok=True)
if not (orig / "words.json").exists(): shutil.copy(d / "words.json", orig / "words.json")
words = json.loads((orig / "words.json").read_text(encoding="utf-8"))
lines = json.loads((d / "lines.json").read_text(encoding="utf-8"))
total = 0.0
for l in lines:
    src = orig / f"{l['id']}.wav"
    if not src.exists(): shutil.copy(d / f"{l['id']}.wav", src)
    a, sr = sf.read(src, dtype="float32"); hop = int(sr * 0.01)
    rms = np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, mode="same"))[::hop]
    quiet = rms < max(1e-4, rms.max() * 0.02)
    cuts = []   # (시작초, 줄인 초)
    i = 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]: j += 1
            dur = (j - i) * 0.01
            if i > 0 and j < len(quiet) and dur > MIN:   # 줄 앞뒤 끝은 assemble이 다룬다
                cuts.append((i * 0.01 + KEEP / 2, dur - KEEP))
            i = j
        else: i += 1
    keep = np.ones(len(a), bool)
    for s, r in cuts: keep[int(s * sr):int((s + r) * sr)] = False
    sf.write(d / f"{l['id']}.wav", a[keep], sr)
    shift = lambda t: t - sum(min(r, max(0.0, t - s)) for s, r in cuts)
    words[l["id"]] = [[w, round(shift(a0), 3), round(shift(b0), 3)] for w, a0, b0 in words[l["id"]]]
    total += sum(r for _, r in cuts)
(d / "words.json").write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
print(f"removed {total:.1f}s of pauses across {len(lines)} lines")
# 자체 점검: 단어 시각이 줄 길이를 넘지 않는다
for l in lines:
    n = len(sf.read(d / f"{l['id']}.wav")[0]) / sr
    assert all(b <= n + 0.05 for _, _, b in words[l["id"]]), l["id"]
