"""내레이션 + 합성 펄스 비트·드론 + 컷마다 효과음을 mix.wav(48 kHz 스테레오)로 만든다. 외부 다운로드 없음.

사용: cd ~/lemo-opuscar && .venv/bin/python <repo>/scripts/make_audio.py <repo>/output/001
입력: output/001/voice.wav, output/001/film/cuts.json (컷마다 s=효과음 코드)
- 바닥: 전자 펄스(0.5초 간격 저음 킥 + 1초 하이햇 틱) + 저음 드론. 내레이션 아래 약 -11 dB, 마지막 장면은 더 낮게.
- 효과음 코드: whoosh, pop, hit, drop, type, tick, riser, none
"""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import soxr

sys.path.insert(0, ".")
from core.audio import sfx  # noqa: E402

SR = sfx.SR
out = Path(sys.argv[1])
cuts = json.loads((out / "film" / "cuts.json").read_text(encoding="utf-8"))["cuts"]
dur = cuts[-1]["t"] + cuts[-1]["d"]
N = int(dur * SR)

v, vsr = sf.read(out / "voice.wav", dtype="float32")
voice = soxr.resample(v, vsr, SR).astype("float32")
voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]

# —— 바닥 음악 ——
t = np.arange(N) / SR
drone = sfx.lp(np.sin(2 * np.pi * 55 * t) + 0.6 * np.sin(2 * np.pi * 55.4 * t) + 0.4 * np.sin(2 * np.pi * 82.4 * t), 200)[:N] * 0.35
kick = sfx.lp(np.sin(2 * np.pi * 52 * sfx.t_(0.25)) * sfx.env_exp(0.25, 0.06), 150) * 0.9
hat = sfx.hp(sfx.noise(0.03), 6000) * sfx.env_exp(0.03, 0.006) * 0.18
bed = np.zeros(N, dtype="float32")


def put(buf, x, at, v=1.0):
    i = int(at * SR)
    if i >= N or i < 0:
        return
    x = x[: N - i] * v
    buf[i:i + len(x)] += x.astype("float32")


for s in np.arange(0, dur, 0.5):
    put(bed, kick, s, 0.6 if int(s * 2) % 4 == 0 else 0.35)
for s in np.arange(0.25, dur, 1.0):
    put(bed, hat, s, 1.0)
bed += drone.astype("float32")

# 음량 자동화: 기본 -27 dB. 큰 숫자·제목 드롭 직전 2초 -20 dB로 상승, 마지막 장면 -36 dB
gain = np.full(N, 10 ** (-27 / 20), dtype="float32")
for c in cuts:
    if c["s"] in ("drop", "hit", "riser"):
        a, b = int(max(0, c["t"] - 2.0) * SR), int(c["t"] * SR)
        gain[a:b] = np.linspace(gain[a], 10 ** (-20 / 20), b - a)
last9 = next(c for c in cuts if c["t"] >= 609.0)
gain[int(last9["t"] * SR):] = 10 ** (-36 / 20)
gain = sfx.lp(gain, 2).astype("float32")
bed *= gain

# —— 효과음 ——
fx = np.zeros(N, dtype="float32")


def riser(d=1.2):
    tt = sfx.t_(d)
    return (sfx.bp(sfx.noise(d), 400, 6000) * (tt / d) ** 2 * 0.6).astype("float32")


def drop():
    d = 0.9
    tt = sfx.t_(d)
    f = 110 * np.exp(-tt * 6) + 40
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * sfx.env_exp(d, 0.35) * 0.9).astype("float32")


def typing(d=1.4, n=12):
    x = np.zeros(int(d * SR), dtype="float32")
    for i in range(n):
        at = int(i * d / n * SR)
        c = sfx.click(1.0 + 0.1 * ((i * 7) % 3), 0.4)
        x[at:at + len(c)] += c[: len(x) - at]
    return x


SFX = {
    "whoosh": lambda: sfx.whoosh(0.3) * 0.5,
    "pop": lambda: sfx.pop() * 0.6,
    "hit": lambda: sfx.thump(1.0, 55) * 0.9,
    "drop": drop,
    "type": typing,
    "tick": lambda: sfx.click(0.9, 0.5),
    "riser": riser,
    "none": lambda: np.zeros(1, dtype="float32"),
}
for c in cuts:
    code = c.get("s", "whoosh")
    at = c["t"] - (1.2 if code == "riser" else 0.0)  # 라이저는 컷 전에 올라와 컷에서 끝난다
    put(fx, SFX[code](), at, 1.0)

# —— 믹스 ——
mix = voice * 0.9 + bed + fx * 0.8
peak = float(np.abs(mix).max())
if peak > 0.98:
    mix *= 0.98 / peak
sf.write(out / "mix.wav", np.stack([mix, mix], axis=1), SR)
rms = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
print(f"mix.wav {dur:.1f}s | voice {rms(voice):.1f} dBFS, bed {rms(bed):.1f} dBFS, fx {rms(fx):.1f} dBFS, peak {peak:.2f}, sfx events {len(cuts)}")
assert rms(voice) - rms(bed) > 7, "바닥 음악이 내레이션에 너무 가깝다"
