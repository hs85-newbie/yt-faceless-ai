"""황금비·피보나치 템플릿 공용 함수 (규칙: brand/GOLDEN.md, 색: brand/golden.css).

tokens()      golden.css의 --g-* 값 → dict (팔레트를 바꾸면 여기서 읽는 값만 바뀐다)
fill()        templates/golden/blocks/*.html 의 {{키}} 채우기
line_starts() 내레이션 lines.json + transcript.srt → {줄 id: 시작 초}
time_plan()   0.382T·0.618T와 가장 가까운 줄, 클라이맥스 줄의 위치
spiral()      황금 사각형 → 정사각형 목록 + 나선 SVG 경로
"""
import json, re
from pathlib import Path

R = Path(__file__).resolve().parents[1]
BLOCKS = R / "templates/golden/blocks"
PHI = (1 + 5 ** 0.5) / 2
FIB = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]


def tokens():
    """brand/golden.css → {'main': '#f2ebdd', ...} (접두어 --g- 제거, 하이픈 유지)."""
    css = (R / "brand/golden.css").read_text()
    return {k: v.strip() for k, v in re.findall(r"--g-([a-z0-9-]+):\s*([^;]+);", css)}


def root_css():
    """블록이 쓰는 :root 변수 — golden.css 원문 그대로 인라인."""
    return (R / "brand/golden.css").read_text()


def fill(name, **vals):
    """블록 템플릿의 {{키}}를 채운다. 빠진 키가 있으면 바로 실패(빈칸으로 렌더되지 않게)."""
    html = (BLOCKS / f"{name}.html").read_text()
    out = re.sub(r"\{\{(\w+)\}\}", lambda m: str(vals[m.group(1)]), html)
    assert "{{" not in out, f"{name}: 채우지 않은 칸"
    return out


# shortcut: Archivo Black 대문자 글자 폭(em) 근사. 기본 0.70, 넓은 M·W, 좁은 I·J·구두점. 소문자 많은 제목이면 표를 늘린다.
_W = {**dict.fromkeys("MW", 0.95), "I": 0.33, "J": 0.55, "L": 0.62, " ": 0.28, "-": 0.40, ".": 0.30, ",": 0.30, "?": 0.60, "%": 0.90}


def _em(s):
    return sum(_W.get(ch, 0.70) for ch in re.sub(r"&\w+;", "-", s).upper())


def fit_size(html_text, width, sizes=(144, 89, 55), by="line"):
    """가장 긴 줄(by="line", 줄바꿈 금지 제목) 또는 가장 긴 단어(by="word", 단어 단위로 접히는 제목)가
    width에 들어가는 가장 큰 피보나치 글자 크기."""
    parts = re.split(r"<br\s*/?>", html_text)
    if by == "word": parts = [w for p in parts for w in p.split()]
    longest = max(_em(p) for p in parts)
    return next((s for s in sizes if longest * s <= width), sizes[-1])


def no_break_hyphen(html_text):
    """ENTRY-LEVEL이 하이픈에서 줄바뀌지 않게(U+2011)."""
    return html_text.replace("-", "&#8209;")


def _secs(s):
    h, m, r = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(r.replace(",", "."))


def line_starts(voice_dir, work_dir):
    """lines.json의 줄 순서와 transcript.srt 큐 순서가 같다는 파이프라인 약속(5단계)을 쓴다."""
    lines = json.loads((Path(voice_dir) / "lines.json").read_text())
    cues = re.findall(r"(\S+) --> (\S+)", (Path(work_dir) / "transcript.srt").read_text())
    assert len(cues) >= len(lines), "transcript.srt 큐가 줄 수보다 적다"
    return {l["id"]: _secs(a) for l, (a, _) in zip(lines, cues)}


def time_plan(starts, T, climax_id=None):
    """황금 시점(0.382T·0.618T)마다 가장 가까운 줄과, 클라이맥스 줄이 0.618T에서 얼마나 떨어졌나."""
    near = lambda t: min(starts, key=lambda k: abs(starts[k] - t))
    plan = {f: {"t": round(T * f, 1), "line": near(T * f), "line_t": round(starts[near(T * f)], 1)} for f in (1 / PHI ** 2, 1 / PHI)}
    if climax_id:
        c = starts[climax_id]
        plan["climax"] = {"line": climax_id, "t": round(c, 1), "frac": round(c / T, 3), "off": round(c - T / PHI, 1)}
    return plan


def spiral(x, y, w, h, n=9):
    sq, d = [], ""
    for i in range(n):
        k = i % 4
        if k == 0: s = h; q = (x, y, s); a, b = (x, y + s), (x + s, y); x += s; w -= s
        elif k == 1: s = w; q = (x, y, s); a, b = (x, y), (x + s, y + s); y += s; h -= s
        elif k == 2: s = h; q = (x + w - s, y, s); a, b = (x + w, y), (x + w - s, y + s); w -= s
        else: s = w; q = (x, y + h - s, s); a, b = (x + s, y + h), (x, y + h - s); h -= s
        sq.append(q)
        d += (f"M{a[0]:.1f},{a[1]:.1f} " if i == 0 else "") + f"A{s:.1f},{s:.1f} 0 0 1 {b[0]:.1f},{b[1]:.1f} "
    return sq, d


if __name__ == "__main__":   # 자기 점검
    t = tokens(); assert {"main", "second", "loud", "bad", "good", "ink"} <= set(t), t
    assert round(1920 / PHI) == 1187 and round(1080 / PHI) == 667
    p = time_plan({"a": 0.0, "b": 100.0, "c": 170.0}, 270.5, "c")
    assert p[1 / PHI]["line"] == "c" and abs(p["climax"]["off"] - 2.8) < 0.1, p
    # 렌더로 확인한 경우: 'IS COLLEGE/STILL/WORTH IT?' 144 들어감, 'SCIENCE STILL' 144 넘침, 'ENTRY-LEVEL' 144 넘침(하이픈에서 접힘)
    assert fit_size("IS COLLEGE<br/>STILL<br/>WORTH IT?", 1009) == 144 and fit_size("IS COMPUTER<br/>SCIENCE STILL", 1009) == 89
    assert fit_size("IS COMPUTER<br/>SCIENCE STILL", 1009, by="word") == 144 and fit_size("IS AI TAKING<br/>ENTRY-LEVEL", 1009, by="word") == 89
    print("ok", t["main"], t["second"], t["loud"])
