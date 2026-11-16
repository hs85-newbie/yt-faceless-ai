"""유튜브 자막 트랙(en.srt, ko.srt)을 만든다. 글자는 대본 원문(lines.json), 시각은 단어 정렬(words.json)과 줄 시각(transcript.srt).

사용:
  1) <lemo venv python> scripts/make_subs.py output/001/02_raw/voice_v4 output/001/03_work/v4 episodes/001/subs
     → subs/en.srt + subs/cues.json(번역할 조각 목록; ko가 비어 있으면 채워 넣는다)
  2) cues.json의 "ko"를 채운 뒤 같은 명령을 다시 돌리면 subs/ko.srt가 생긴다(시각은 en과 같다).
규칙: 조각은 문장 → 쉼표 → 단어 순으로 쪼개 한 조각 42자 이하. 조각 시작 = 그 조각 첫 단어가 들리는 시각.
"""
import json
import re
import sys
from pathlib import Path

voice_dir, work, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
MAX = 42
lines = json.loads((voice_dir / "lines.json").read_text(encoding="utf-8"))
words = json.loads((voice_dir / "words.json").read_text(encoding="utf-8"))
secs = lambda s: (lambda h, m, r: int(h) * 3600 + int(m) * 60 + float(r.replace(",", ".")))(*s.split(":"))
spans = re.findall(r"(\S+) --> (\S+)", (work / "transcript.srt").read_text(encoding="utf-8"))
assert len(spans) == len(lines), "transcript.srt와 lines.json 줄 수 불일치"
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def pieces(text):
    """문장 → 쉼표·콜론 → 단어 순으로 42자 이하 조각."""
    out_ = []
    for sent in re.split(r"(?<=[.?!])\s+", text.strip()):
        parts = [sent] if len(sent) <= MAX else re.split(r"(?<=[,:;])\s+", sent)
        for p in parts:
            buf = ""
            for w in p.split():
                if buf and len(buf) + 1 + len(w) > MAX: out_.append(buf); buf = w
                else: buf = f"{buf} {w}".strip()
            if buf: out_.append(buf)
    merged = []   # 너무 짧은 꼬리(3단어 미만)는 앞 조각에 붙인다(42자를 조금 넘어도 허용)
    for p in out_:
        if merged and len(p.split()) < 3 and len(merged[-1]) + len(p) < MAX + 14: merged[-1] += " " + p
        else: merged.append(p)
    return merged


def fmt(t):
    h, r = divmod(max(0.0, t), 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"


cues = []
for line, (a, b) in zip(lines, spans):
    t0, t1 = secs(a), secs(b)
    ws = words[line["id"]]
    cat, owner = "", []   # 받아쓰기 단어를 이어 붙인 글자열 + 각 글자의 단어 번호
    for k, (w, _, _) in enumerate(ws): n = norm(w); cat += n; owner += [k] * len(n)
    ps, pos, starts = pieces(line["text"]), 0, []
    for j, p in enumerate(ps):
        key = norm(" ".join(p.split()[:2]))[:8] or norm(p)[:8]
        i = cat.find(key, pos) if key else -1
        if i < 0:   # 못 찾으면 글자 비율로 추정
            frac = sum(len(x) for x in ps[:j]) / max(1, sum(len(x) for x in ps)); starts.append(t0 + frac * (t1 - t0)); continue
        starts.append(t0 + max(0.0, ws[owner[i]][1])); pos = i + len(key)
    for j, p in enumerate(ps):
        end = starts[j + 1] - 0.04 if j + 1 < len(ps) else t1
        cues.append({"id": f"{line['id']}.{j}", "start": round(starts[j], 3), "end": round(max(end, starts[j] + 0.8), 3), "en": p})

old = {}
cj = out / "cues.json"
if cj.exists(): old = {c["id"]: c.get("ko", "") for c in json.loads(cj.read_text(encoding="utf-8"))}
for c in cues: c["ko"] = old.get(c["id"], "")
cj.write_text(json.dumps(cues, ensure_ascii=False, indent=1), encoding="utf-8")


def write(lang):
    body = "\n".join(f"{n}\n{fmt(c['start'])} --> {fmt(c['end'])}\n{c[lang]}\n" for n, c in enumerate(cues, 1))
    (out / f"{lang}.srt").write_text(body, encoding="utf-8")


write("en")
missing = sum(1 for c in cues if not c["ko"])
if not missing: write("ko")
lens = [c["end"] - c["start"] for c in cues]
print(f"cues {len(cues)} · min {min(lens):.1f}s · max {max(lens):.1f}s · ko 미번역 {missing}")
