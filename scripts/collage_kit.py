"""문서 콜라주(vox-explainer 방식) 공용 부품 — 내레이션 한 줄 = 한 숏. 찢은 종이 카드·망점·종이 결, 두 장 한 그림(on twos).

편 스크립트(scripts/ep00N_collage.py)는 SHOTS만 정하고 write()를 부른다. 껍데기: scripts/collage.html.
화면 규칙: brand/GOLDEN.md(색은 golden.css 토큰, 크기·간격은 피보나치).
"""
import random, re, shutil, subprocess
from pathlib import Path
from golden_kit import R, fit_size, line_starts, no_break_hyphen, root_css

F = lambda n: round(n / 30, 3)   # 피보나치 프레임 → 초
NYFED = "Source: NY Fed, The Labor Market for Recent College Graduates"
STAN = "Source: Brynjolfsson, Chandar &amp; Chen, &ldquo;Canaries in the Coal Mine,&rdquo; Stanford (Aug 2026)"
COL = {"bad": "var(--g-bad)", "good": "var(--g-good)", "pay": "var(--g-good)", "neutral": "var(--g-ink)"}


def timing(ep, voice="voice_v1", work="v1"):
    """(줄 시작 시각 dict, 전체 길이, 0.618T)."""
    v, w = R / f"output/{ep}/02_raw/{voice}", R / f"output/{ep}/03_work/{work}"
    end = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(w / "voice.wav")],
                               capture_output=True, text=True, check=True).stdout)
    return line_starts(v, w), end, round(end * 0.618, 2)


def torn(w, h, seed):
    """찢긴 가장자리 clip-path: 21px마다 0~5px 안쪽으로 흔들림(시드 고정 → 매 렌더 같은 모양)."""
    r, pts = random.Random(seed), []
    for x in range(0, w, 21): pts.append((x, r.uniform(0, 5)))
    for y in range(0, h, 21): pts.append((w - r.uniform(0, 5), y))
    for x in range(w, 0, -21): pts.append((x, h - r.uniform(0, 5)))
    for y in range(h, 0, -21): pts.append((r.uniform(0, 5), y))
    return "polygon(" + ",".join(f"{x:.0f}px {y:.0f}px" for x, y in pts) + ")"


def card(x, y, w, h, body, t, seed, rot=-2.618, bg="var(--g-sheet)", cls=""):
    """종이 카드 하나: 시각 t에 위에서 떨어지듯 붙는다. 회전은 GOLDEN §6(−2.618° / +1.618°)."""
    return (f'<div class="pop tw {cls}" data-t="{t}" data-r="{rot}" style="left:{x}px;top:{y}px">'
            f'<div class="card" style="width:{w}px;height:{h}px;background:{bg};clip-path:{torn(w, h, seed)}">{body}</div></div>')


def num(value, kind, label, sub=""):
    s = f'<div class="sub">{sub}</div>' if sub else ""
    plain = re.sub(r"&[a-z]+;", "x", value)   # 엔티티(&rarr; 등)는 한 글자로 센다
    size = 144 if len(plain) <= 5 else 89     # WHY: $60,000·7.4%→5.2%가 144로는 카드(폭 610) 밖으로 넘쳤다 → 피보나치 한 단계 아래
    return f'<div class="n" style="color:{COL[kind]};font-size:{size}px">{value}</div><div class="lab">{label}</div>{s}'


def pair(t0, a, b, gap=F(21)):
    """두 숫자 카드를 대칭으로(폭 610 · 높이 377 · 사이 144). a·b = (값, kind, 라벨, 작은 글)."""
    x0 = (1920 - 610 * 2 - 144) // 2
    return (card(x0, 233, 610, 377, num(*a), round(t0 + F(8), 3), 11) +
            card(x0 + 610 + 144, 233, 610, 377, num(*b), round(t0 + F(8) + gap, 3), 12, rot=1.618))


def strip(text, t, y=413, seed=21, bg="var(--g-second)", fg="var(--g-main)"):
    """키네틱 문장: 네이비 찢은 띠에 굵은 글씨(89), 황금선 x 89에서 시작, 폭 1187(주 패널)."""
    size = fit_size(text, 1187 - 2 * 55, sizes=(89, 55), by="word")
    return card(89, y, 1187 + 233, 233, f'<div class="kin" style="color:{fg};font-size:{size}px">{no_break_hyphen(text)}</div>', t, seed, bg=bg)


def bars(t0, rows, title, times=None):
    """순위 띠 세 칸: 라벨(x 89~521) · 찢은 종이 띠(x 521부터, 폭 = 값 비례, 최대 987) · 값(띠 끝 + 21).
    WHY: 라벨·값을 띠 안에 넣으면 짧은 띠(0.7%)에서 값이 라벨에 가려졌다(2026-11-22 시안). rows = [(라벨, 값 문자열, 수치, kind)]."""
    mx, out = max(v for _, _, v, _ in rows), [f'<div class="pop btitle" data-t="{t0}" data-r="0">{title}</div>']
    for i, (lab, txt, v, kind) in enumerate(rows):
        t, y, w = (times[i] if times else round(t0 + F(13) + i * F(21), 3)), 233 + i * 144, max(21, int(987 * v / mx))
        out.append(f'<div class="pop blab" data-t="{t}" data-r="0" style="left:89px;top:{y + 21}px">{lab}</div>')
        out.append(card(521, y, w, 89, "", t, 40 + i, rot=0, bg=COL[kind] if kind != "neutral" else "var(--g-neutral)", cls="bar"))
        out.append(f'<div class="pop bval" data-t="{t}" data-r="0" style="left:{521 + w + 21}px;top:{y + 8}px;color:{COL[kind]}">{txt}</div>')
    return "".join(out)


def scatter(t0, pts, xlab, ylab, xr, yr, zone=None):
    """찢은 점 산점도: 판(x 377~1597 · y 233~843), 점 34px. pts = [(라벨, x값, y값, kind)], xr·yr = (최소, 최대).
    zone = (x최대, y최소) → 그 구석(왼쪽 위)을 먼저 깐다."""
    X = lambda v: int(377 + 1220 * (v - xr[0]) / (xr[1] - xr[0]))
    Y = lambda v: int(843 - 610 * (v - yr[0]) / (yr[1] - yr[0]))
    out = [card(377, 233, 1220, 610, "", t0, 70, rot=0),
           f'<div class="pop blab" data-t="{t0}" data-r="0" style="left:377px;top:864px">{xlab}</div>',
           f'<div class="pop blab" data-t="{t0}" data-r="0" style="left:377px;top:178px">{ylab}</div>']
    if zone:
        out.append(card(377, 233, X(zone[0]) - 377, Y(zone[1]) - 233, "", round(t0 + F(21), 3), 71, rot=0, bg="var(--g-neutral)"))
    for i, (lab, x, y, kind) in enumerate(pts):
        t = round(t0 + F(34) + i * F(13), 3)
        out.append(card(X(x) - 17, Y(y) - 17, 34, 34, "", t, 80 + i, rot=0, bg=COL[kind]))
        if lab:
            out.append(f'<div class="pop blab" data-t="{t}" data-r="0" style="left:{X(x) + 21}px;top:{Y(y) - 21}px">{lab}</div>')
    return "".join(out)


def stamp(text, t, x, y, color="var(--g-bad)", rot=-8):
    return f'<div class="stamp pop" data-t="{t}" data-r="{rot}" data-s="1" style="left:{x}px;top:{y}px;color:{color};border-color:{color}">{text}</div>'


def fork(t0, left, right):
    """갈림길: 손으로 그은 Y자 길(SVG, 선 굵기 5) + 양쪽 종이 카드."""
    road = (f'<svg class="pop road" data-t="{t0}" data-r="0" viewBox="0 0 1920 1080"><path d="M960 1000 C960 760 960 700 960 667 '
            f'M960 667 C900 560 700 520 610 413 M960 667 C1020 560 1220 520 1310 413"/></svg>')
    return road + card(233, 144, 610, 269, left, round(t0 + F(13), 3), 31) + card(1077, 144, 610, 269, right, round(t0 + F(34), 3), 32, rot=1.618)


def write(ep, L, end, shots, final, work="v1"):
    """shots = {줄 id: (화면 html, 출처)} → output/NNN/03_work/collage/ (npx hyperframes render로 렌더)."""
    ids, out, body = list(shots), R / f"output/{ep}/03_work/collage", []
    for i, k in enumerate(ids):
        html, src = shots[k]
        t_out = L[ids[i + 1]] if i + 1 < len(ids) else end
        src_html = f'<div class="src">{src}</div>' if src else ""
        body.append(f'<div class="shot" data-in="{L[k]}" data-out="{t_out}">{html}{src_html}</div>')
    draft = "" if final else f'<div id="draft">DRAFT &middot; EP{ep} COLLAGE</div>'
    (out / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy(R / f"output/{ep}/03_work/{work}/mix.wav", out / "assets/mix.wav")
    for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(R / "episodes/002/film" / f, out / f)
    (out / "index.html").write_text((R / "scripts/collage.html").read_text().replace("{{ROOT_CSS}}", root_css()).replace("{{END}}", str(end))
                                    .replace("{{SHOTS}}", "\n".join(body)).replace("{{DRAFT}}", draft))
    print(f"EP{ep} collage: {len(ids)} shots · T {end:.1f}s · 0.618T {round(end * 0.618, 2)} → {out}")
