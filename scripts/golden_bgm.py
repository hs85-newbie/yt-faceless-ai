"""편 공용 배경음악(코드 작곡, 생성 AI 없음) + 내레이션 아래 덕킹 믹스. EP002에서 만든 것을 편마다 쓰게 일반화(2026-11-22).

사용: ~/lemo-opuscar/.venv/bin/python -I scripts/golden_bgm.py NNN → <work>/bgm.wav, mix.wav, credits.txt
설정: episodes/NNN/bgm.json = {voice, work, title, p1, climax_from, counter, close} (값은 줄 id — 그 줄이 시작하는 시각)
악기: lemo-opuscar sampler — Salamander Grand Piano(CC BY 3.0, 설명란에 출처 필수) + VSCO 2 CE(CC0). 출처 문구는 credits.txt.
구조(brand/GOLDEN.md §5-1): 피아노만 → 제목에서 현악 → 0.382T 낮고 차분 → climax_from에서 차올라 0.618T 정점 → 풀며 끝.
"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path.home() / "lemo-opuscar"))                      # lemo core
import numpy as np
import soundfile as sf
from core.audio import sampler as S
from core.audio.sfx import SR
from golden_kit import R, line_starts

EP = sys.argv[1]
CFG = json.loads((R / f"episodes/{EP}/bgm.json").read_text())
WORK = R / CFG["work"]
LINE = line_starts(R / CFG["voice"], WORK)
END = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(WORK / "voice.wav")],
                           capture_output=True, text=True, check=True).stdout)
G1, G2 = END * 0.382, END * 0.618
T_TITLE, T_P1, T_PAY, T_COUNTER, T_CLOSE = (LINE[CFG[k]] for k in ("title", "p1", "climax_from", "counter", "close"))
BEAT = 60 / 72
BAR = 4 * BEAT
CHORDS = {"Am": ["A2", "E3", "A3", "C4", "E4"], "F": ["F2", "C3", "F3", "A3", "C4"], "C": ["C3", "G3", "C4", "E4", "G4"],
          "G": ["G2", "D3", "G3", "B3", "D4"], "Dm": ["D3", "A3", "D4", "F4", "A4"], "E": ["E2", "B2", "E3", "G#3", "B3"]}
PROG = {"main": ["Am", "F", "C", "G"], "dark": ["Am", "Dm", "F", "E"], "lift": ["F", "C", "G", "Am"]}
S.seed(13)


def section(t):
    """이 시각에 쓸 진행·밀도: (진행, 피아노 음 간격(박), 현악 세기)."""
    if t < T_TITLE: return "main", 1, 0.0
    if t < T_P1: return "main", 2, 0.35
    if t < G1: return "main", 1, 0.3
    if t < T_PAY: return "dark", 2, 0.28
    if t < G2: return "lift", 0.5, 0.3 + 0.4 * (t - T_PAY) / max(G2 - T_PAY, 1e-6)   # 차오름
    if t < T_COUNTER: return "lift", 1, 0.45
    if t < T_CLOSE: return "main", 2, 0.25
    return "main", 2, 0.3


def events():
    ev, bar_i, t = [], 0, 0.0
    while t < END - 1.5:
        prog, step, strings = section(t)
        ch = CHORDS[PROG[prog][bar_i % 4]]
        ev.append((t, "piano", ch[0], BAR, 0.42, -0.15))   # 마디 첫 박 저음 + 위 음들로 분산화음
        k, b = 0, 0.0
        while b < 4 - 1e-6:
            if b > 0 or step < 1:
                ev.append((t + b * BEAT, "piano", ch[1 + k % 4], BEAT * 2, 0.30 + 0.12 * (step < 1), 0.2 * ((k % 2) * 2 - 1)))
            k += 1; b += step
        if strings > 0:   # 현악 패드: 근음·5도·3도 긴 음
            for p, inst, pan in ((ch[0], "cellos", -0.3), (ch[2], "violas", 0.1), (ch[3], "violins", 0.35)):
                ev.append(dict(t=t, inst=inst, pitch=p, dur=BAR + 0.4, vel=min(0.85, strings), pan=pan, attack=0.6, release=1.2))
        t += BAR; bar_i += 1
    ev.append((G2, "timpani", "F2", 3.0, 0.45, 0))   # 0.618T 정점: 팀파니(음높이 악기) + 피아노 F
    ev.append(dict(t=G2, inst="piano", pitch="F2", dur=4.0, vel=0.55, pan=0))
    for p in ("A2", "E3", "A3", "C#4", "E4"):         # 끝: 가장조로 풀어 울림
        ev.append(dict(t=END - 6.0, inst="piano", pitch=p, dur=5.5, vel=0.4, pan=0))
    return ev


ev = events()
mix = S.room(S.render(ev, dur=END), size=0.55, mix=0.22)
fade = np.ones(len(mix)); n_in, n_out = int(SR * 2), int(SR * 4)
fade[:n_in] = np.linspace(0, 1, n_in); fade[-n_out:] = np.linspace(1, 0, n_out)
out = WORK / "bgm.wav"
sf.write(out, (mix * fade[:, None]).astype(np.float32), SR)
(WORK / "credits.txt").write_text("\n".join(S.credits(["piano", "cellos", "violas", "violins", "timpani"])) + "\n")
# 덕킹: 내레이션이 나오면 음악을 눌러 내리고(사이드체인), 음악은 내레이션보다 약 15~16dB 아래(EP002 실측)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(WORK / "voice.wav"), "-i", str(out), "-filter_complex",
                "[0:a]aresample=48000,asplit=2[v][sc];[1:a]volume=0.55[m];"
                "[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=25:release=450[d];"
                "[v][d]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]",
                "-map", "[o]", "-ar", "48000", str(WORK / "mix.wav")], check=True)
print(f"EP{EP} bgm {END:.1f}s · events {len(ev)} · 0.382T {G1:.1f} · climax {T_PAY:.1f} → 0.618T {G2:.1f} → {WORK / 'mix.wav'}")
