"""내레이션 + 합성 배경음 + 효과음을 하나의 mix.wav(48 kHz 스테레오)로 만든다. 외부 다운로드 없음.

사용: cd ~/lemo-opuscar && .venv/bin/python <repo>/scripts/make_audio.py <repo>/output/001
- 배경음: 저음 드론(두 음을 살짝 어긋나게) + 갈색 잡음 바닥 + 1초 시계 초침. 내레이션 아래 약 -22 dB, 장면 전환 직전 살짝 올라옴.
- 효과음: 장면 시작마다 낮은 타격음, 줄(비트) 시작마다 아주 작은 휙 소리, 제목 드롭에 큰 타격음, 큰 숫자에 팝.
"""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import soxr

sys.path.insert(0, ".")  # lemo-opuscar 루트에서 실행
from core.audio import sfx  # noqa: E402

SR = sfx.SR
out = Path(sys.argv[1])
cues = json.loads((out / "film" / "cues.json").read_text(encoding="utf-8"))
dur = cues["dur"]
N = int(dur * SR)

# 내레이션 (24 kHz 모노 → 48 kHz)
v, vsr = sf.read(out / "voice.wav", dtype="float32")
voice = soxr.resample(v, vsr, SR).astype("float32")
voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]

# 배경음: 드론
t = np.arange(N) / SR
drone = (np.sin(2 * np.pi * 55 * t) + 0.7 * np.sin(2 * np.pi * 55.3 * t) + 0.5 * np.sin(2 * np.pi * 82.4 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.05 * t)))
drone = sfx.lp(drone, 220) * 0.4
bed = sfx.lp(sfx.brown(dur), 400) * 0.12
tick = np.zeros(N, dtype="float32")
tk = sfx.hp(sfx.noise(0.012), 3000) * sfx.env_exp(0.012, 0.003) * 0.25
for s in range(int(dur)):
    i = s * SR
    tick[i:i + len(tk)] += tk[: N - i] if i + len(tk) > N else tk
bgm = (drone[:N] + bed[:N]).astype("float32") + tick[:N]  # 길이 반올림 차이 정리

# 배경음 음량 자동화: 기본 -27 dB, 각 장면 시작 2초 전부터 -19 dB로 올렸다가 장면 시작에 되돌림, 마지막 장면은 -40 dB
gain = np.full(N, 10 ** (-27 / 20), dtype="float32")
for sc in cues["scenes"]:
    a, b = int(max(0, sc["start"] - 2.0) * SR), int(sc["start"] * SR)
    gain[a:b] = np.linspace(gain[a], 10 ** (-19 / 20), b - a)
last = cues["scenes"][-1]
gain[int(last["start"] * SR):] = 10 ** (-40 / 20)
gain = sfx.lp(gain, 2).astype("float32")  # 부드럽게
bgm *= gain

# 효과음
fx = np.zeros(N, dtype="float32")


def put(x, at, v=1.0):
    i = int(at * SR)
    if i >= N:
        return
    x = x[: N - i] * v
    fx[i:i + len(x)] += x


for sc in cues["scenes"]:
    put(sfx.thump(1.0, 60), sc["start"], 0.5)
for ln in cues["lines"]:
    put(sfx.whoosh(0.3), ln["t0"], 0.12)
# 제목 드롭: s2_04의 후반 비트(줄 길이 절반 지점)
s2_04 = next(l for l in cues["lines"] if l["id"] == "s2_04")
put(sfx.thump(1.0, 48), s2_04["t0"] + (s2_04["t1"] - s2_04["t0"] + 0.5) / 2, 1.0)
# 큰 숫자 2개 (s3_02 두 비트), 64% 도넛 (s6_02), 펀치라인 차트 (s8_01)
s3_02 = next(l for l in cues["lines"] if l["id"] == "s3_02")
half = (s3_02["t1"] - s3_02["t0"] + 0.5) / 2
put(sfx.pop(), s3_02["t0"] + 0.3, 0.5); put(sfx.pop(), s3_02["t0"] + half + 0.3, 0.5)
for lid in ("s6_02", "s8_01", "s7_02"):
    l = next(l for l in cues["lines"] if l["id"] == lid)
    put(sfx.thump(1.0, 55), l["t0"] + 0.2, 0.6)

# 믹스: 음성 기준, 배경음은 이미 자동화로 낮춤. 최종 라우드니스는 mux.sh의 loudnorm이 맞춘다.
mix = voice * 0.9 + bgm + fx * 0.8
peak = np.abs(mix).max()
if peak > 0.98:
    mix *= 0.98 / peak
stereo = np.stack([mix, mix], axis=1)
sf.write(out / "mix.wav", stereo, SR)
rms = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
print(f"mix.wav {dur:.1f}s | voice {rms(voice):.1f} dBFS, bgm {rms(bgm):.1f} dBFS, fx {rms(fx):.1f} dBFS, peak {peak:.2f}")
assert rms(voice) - rms(bgm) > 8, "배경음이 내레이션에 너무 가깝다"
