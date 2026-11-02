"""v3 믹스: 내레이션 + 바닥 음악 + 전환 종류에 맞춘 종이 효과음 → mix.wav(48 kHz 스테레오). 외부 다운로드 없음.

사용: ~/lemo-opuscar/.venv/bin/python scripts/make_audio_v3.py output/001/v3
입력: <out>/voice.wav, <out>/film/cuts.json (컷의 tr = 전환 종류, strips/stamp의 at = 등장 시각)
v2 지적 반영: 전환음이 "쉭" 하나뿐 → 전환 종류마다 다른 소리(종이 넘김·테이프 찢기·휙·도장·종이 떨어짐·틱).
"""
import json, sys
from pathlib import Path

import numpy as np
import soundfile as sf
import soxr

sys.path.insert(0, str(Path.home() / "lemo-opuscar"))
from core.audio import sfx  # noqa: E402

SR = sfx.SR
out = Path(sys.argv[1])
cuts = json.loads((out / "film" / "cuts.json").read_text(encoding="utf-8"))["cuts"]
dur = cuts[-1]["t"] + cuts[-1]["d"]; N = int(dur * SR)
v, vsr = sf.read(out / "voice.wav", dtype="float32")
voice = np.pad(soxr.resample(v, vsr, SR).astype("float32"), (0, N))[:N]


def put(buf, x, at, g=1.0):
    i = int(at * SR)
    if 0 <= i < N: x = x[: N - i] * g; buf[i:i + len(x)] += x.astype("float32")


# —— 종이 효과음(절차 생성) ——
def paper(d=0.42):        # 종이 한 장이 화면을 쓸고 지나감: 대역 잡음이 부풀었다 꺼지고 바스락 잔결
    tt = sfx.t_(d); env = np.sin(np.pi * tt / d) ** 1.5
    crinkle = np.zeros(len(tt))
    for k in range(18):
        c = sfx.click(1.4 + (k % 5) * 0.2, 0.25); i = int(len(tt) * k / 18); crinkle[i:i + len(c)] += c[: len(tt) - i]
    return sfx.norm(sfx.bp(sfx.noise(d), 1200, 7000) * env + crinkle * env) * 0.55
def rip(d=0.38):          # 테이프 찢기: 빠르게 떨리는 잡음
    tt = sfx.t_(d); am = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * (70 + 90 * tt / d) * tt))
    return sfx.norm(sfx.bp(sfx.noise(d), 700, 5200) * am * np.minimum(1, tt / 0.02) * np.exp(-tt / 0.25)) * 0.6
def over(x, y):           # 길이가 다른 두 소리를 겹친다
    n = max(len(x), len(y)); return np.pad(x, (0, n - len(x))) + np.pad(y, (0, n - len(y)))
def stamp():              # 도장: 낮은 쿵 + 딱
    return sfx.norm(over(sfx.thump(1.0, 62), sfx.clack(0.8, 0.6) * 0.5)) * 0.8
def slap():               # 종이가 매트에 떨어짐
    d = 0.18; return sfx.norm(over(sfx.lp(sfx.noise(d), 2600) * sfx.env_exp(d, 0.03), sfx.thump(0.6, 120)[: int(d * SR)] * 0.5)) * 0.55
def tap():                # 띠 하나가 자리 잡음(작게)
    d = 0.08; return sfx.norm(sfx.bp(sfx.noise(d), 900, 4000) * sfx.env_exp(d, 0.012)) * 0.22
def riser(d=1.6):
    tt = sfx.t_(d); return (sfx.bp(sfx.noise(d), 400, 6000) * (tt / d) ** 2 * 0.5).astype("float32")


TR = {"wipe": paper, "rip": rip, "whip": lambda: sfx.whoosh(0.32) * 0.5, "punch": stamp, "drop": slap, "cut": lambda: sfx.click(0.9, 0.35)}
fx = np.zeros(N, dtype="float32")
for i, c in enumerate(cuts):
    if i: put(fx, TR[c.get("tr", "cut")](), c["t"] - 0.12)
    for s in c.get("strips", []) + c.get("props", []): put(fx, tap(), c["t"] + s.get("at", 0))   # v4: 소품이 일어설 때
    if "stamp" in c: put(fx, stamp(), c["t"] + c["stamp"]["at"] + 0.2, 0.8)
    if c.get("scene") == "title": put(fx, riser(), c["t"] - 1.6); put(fx, sfx.thump(1.0, 50) * 0.9, c["t"] + 0.5)

# —— 바닥: 저음 드론 + 0.5초 킥 + 하이햇. 제목 드롭 뒤로는 킥을 한 단계 올린다 ——
t = np.arange(N) / SR
bed = (sfx.lp(np.sin(2 * np.pi * 55 * t) + 0.6 * np.sin(2 * np.pi * 55.4 * t) + 0.4 * np.sin(2 * np.pi * 82.4 * t), 200)[:N] * 0.35).astype("float32")
kick = sfx.lp(np.sin(2 * np.pi * 52 * sfx.t_(0.25)) * sfx.env_exp(0.25, 0.06), 150) * 0.9
hat = sfx.hp(sfx.noise(0.03), 6000) * sfx.env_exp(0.03, 0.006) * 0.18
title_t = next(c["t"] for c in cuts if c.get("scene") == "title")
for s in np.arange(0, dur, 0.5): put(bed, kick, s, (0.6 if int(s * 2) % 4 == 0 else 0.35) * (1.0 if s > title_t else 0.7))
for s in np.arange(0.25, dur, 1.0): put(bed, hat, s)
gain = np.full(N, 10 ** (-25 / 20), dtype="float32")
a, b = int((title_t - 2) * SR), int(title_t * SR); gain[a:b] = np.linspace(gain[a], 10 ** (-18 / 20), b - a)
gain[b:int((title_t + 3) * SR)] = 10 ** (-20 / 20)
close_t = next((c["t"] for c in cuts if c.get("img") == "sb6_conclusion.png" or c.get("scene") == "close"), dur)
gain[int(close_t * SR):] = 10 ** (-33 / 20)
bed *= sfx.lp(gain, 2).astype("float32")

mix = voice * 0.9 + bed + fx * 0.35
peak = float(np.abs(mix).max()); mix *= min(1.0, 0.98 / peak)
sf.write(out / "mix.wav", np.stack([mix, mix], axis=1), SR)
rms = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
print(f"mix.wav {dur:.1f}s | voice {rms(voice):.1f} dBFS, bed {rms(bed):.1f}, fx {rms(fx * 0.35):.1f}, peak {peak:.2f}")
assert rms(voice) - rms(bed) > 7 and rms(voice) - rms(fx * 0.35) > 7, "바닥·효과음이 내레이션에 너무 가깝다"
