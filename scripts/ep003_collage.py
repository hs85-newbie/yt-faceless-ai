"""EP003 문서 콜라주(G안, vox-explainer 방식) — 내레이션 한 줄 = 한 숏. 찢은 종이 카드·망점·종이 결, 두 장 한 그림(on twos).

사용: python3 -I scripts/ep003_collage.py [final] → output/003/03_work/collage/ 에서 npx hyperframes render
숫자: 전부 episodes/003/02_research.md 번호(주석 #N). 화면 규칙: brand/GOLDEN.md(색은 golden.css 토큰, 크기·간격은 피보나치).
시간 구조: T 176.3초, 0.382T 67.4(3절 스탠퍼드), 0.618T 109.0 = 클라이맥스(4절 전공별 띠에서 컴퓨터과학이 마지막에 꽂힘).
제목 숏(s1_02)은 썸네일과 같은 구성 — 맞춤 썸네일 대신 스튜디오 '동영상에서 선택'으로 고른다(채널 전화 인증 불가).
"""
import random, re, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from golden_kit import R, fill, fit_size, line_starts, no_break_hyphen, root_css

VOICE, WORK = R / "output/003/02_raw/voice_v1", R / "output/003/03_work/v1"
OUT = R / "output/003/03_work/collage"
L = line_starts(VOICE, WORK)
END = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(WORK / "voice.wav")],
                           capture_output=True, text=True, check=True).stdout)
F = lambda n: round(n / 30, 3)   # 피보나치 프레임 → 초
G2 = round(END * 0.618, 2)
NYFED, STAN = "Source: NY Fed, The Labor Market for Recent College Graduates", "Source: Brynjolfsson, Chandar &amp; Chen, &ldquo;Canaries in the Coal Mine,&rdquo; Stanford (Aug 2026)"
COL = {"bad": "var(--g-bad)", "good": "var(--g-good)", "pay": "var(--g-good)", "neutral": "var(--g-ink)"}


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


def stamp(text, t, x, y, color="var(--g-bad)", rot=-8):
    return f'<div class="stamp pop" data-t="{t}" data-r="{rot}" data-s="1" style="left:{x}px;top:{y}px;color:{color};border-color:{color}">{text}</div>'


def fork(t0, left, right):
    """갈림길: 손으로 그은 Y자 길(SVG, 선 굵기 5) + 양쪽 종이 카드."""
    road = (f'<svg class="pop road" data-t="{t0}" data-r="0" viewBox="0 0 1920 1080"><path d="M960 1000 C960 760 960 700 960 667 '
            f'M960 667 C900 560 700 520 610 413 M960 667 C1020 560 1220 520 1310 413"/></svg>')
    return road + card(233, 144, 610, 269, left, round(t0 + F(13), 3), 31) + card(1077, 144, 610, 269, right, round(t0 + F(34), 3), 32, rot=1.618)


GCFG = {"title": "IS COLLEGE<br/>STILL WORTH IT<br/>WITH AI?", "kicker": "FOR PARENTS", "number": "5.2%", "caption": "of recent college grads<br/>are unemployed"}
TITLE = fill("thumbnail", title=no_break_hyphen(GCFG["title"]), title_size=fit_size(GCFG["title"], 1187 - 2 * 89, by="word"),
             kicker=GCFG["kicker"], number=GCFG["number"], number_color="var(--g-bad)", caption=GCFG["caption"])

S = lambda k: L[k]
SHOTS = {   # 줄 id → (화면, 출처)
    "s1_01": (pair(S("s1_01"), ("5.2%", "bad", "RECENT GRADS", "unemployed, Sept 2026"), ("4.0%", "neutral", "ALL WORKERS", "unemployed, Sept 2026")), NYFED),   # #1
    "s1_02": (f'<div class="pop full" data-t="{S("s1_02")}" data-r="0">{TITLE}</div>', ""),
    "s2_01": (fork(S("s2_01"), '<div class="fk">DEGREE</div>', '<div class="fk">NO DEGREE</div>'), ""),
    "s2_02": (pair(S("s2_02"), ("7.4%", "bad", "NO DEGREE", "ages 22&ndash;27, Sept 2026"), ("5.2%", "good", "RECENT GRADS", "ages 22&ndash;27, Sept 2026"), gap=F(55)), NYFED),   # #2 #1
    "s2_03": (pair(S("s2_03"), ("$60,000", "pay", "DEGREE", "median pay, ages 22&ndash;27, 2025"), ("$40,000", "neutral", "HIGH SCHOOL", "median pay, ages 22&ndash;27, 2025"), gap=F(89))
              + stamp("1.5&times; THE PAY", round(S("s2_03") + 7.0, 3), 1187, 667, color="var(--g-good)"), NYFED),   # #3
    "s2_04": (strip("THE DEGREE STILL WINS.", S("s2_04")), ""),
    "s3_01": (pair(S("s3_01"), ("15%", "bad", "JULY 2025", "lower employment, ages 22&ndash;25, most AI-exposed jobs"),
                   ("19%", "bad", "JUNE 2026", "lower employment, ages 22&ndash;25, most AI-exposed jobs"), gap=F(144) * 2), STAN),   # #7
    "s3_02": (card(377, 233, 987, 233, '<div class="kin struck">MORE LAYOFFS</div>', round(S("s3_02") + F(8), 3), 51)
              + stamp("FEWER HIRES", round(S("s3_02") + 2.0, 3), 987, 413)
              + card(377, 610, 987, 144, '<div class="note">Patterns, not proof of cause.</div>', round(S("s3_02") + 6.0, 3), 52, rot=1.618), STAN),   # #8
    "s3_03": (strip("THE FIRST RUNG IS SHRINKING.", S("s3_03")), ""),
    "s4_01": (card(377, 144, 1166, 610, '<div class="dip">BACHELOR&rsquo;S DEGREE</div><div class="sub">2024 recent grads</div>', round(S("s4_01") + F(8), 3), 61)
              + stamp("39% UNDEREMPLOYED", round(S("s4_01") + 3.0, 3), 610, 610), NYFED),   # #4
    "s4_02": (bars(S("s4_02"), [("SPECIAL EDUCATION", "0.7%", 0.7, "good"), ("NURSING", "2.1%", 2.1, "good"), ("FINANCE", "2.8%", 2.8, "good"),
                                ("ALL MAJORS", "4.2%", 4.2, "neutral"), ("COMPUTER SCIENCE", "7.0%", 7.0, "bad")], "UNEMPLOYED, RECENT GRADS, 2024",
                   times=[round(S("s4_02") + F(13) + i * F(34), 3) for i in range(4)] + [G2]), NYFED),   # #5 — 0.618T에 CS
    "s4_03": (bars(S("s4_03"), [("COMPUTER SCIENCE", "19%", 19.1, "good"), ("ART HISTORY", "45%", 45.3, "bad"), ("PHILOSOPHY", "47%", 47.1, "bad")],
                   "UNDEREMPLOYED, RECENT GRADS WITH A JOB, 2024"), NYFED),   # #4
    "s4_04": (strip("NOT ONE BET. DOZENS OF THEM.", S("s4_04")), ""),
    "s5_01": (fork(S("s5_01"), num("5.2%", "good", "DEGREE", "unemployed &middot; $60,000 pay"), num("7.4%", "bad", "NO DEGREE", "unemployed &middot; $40,000 pay")), NYFED),   # #1 #2 #3
    "s5_02": (strip("LESS MARGIN FOR ERROR.", S("s5_02")), ""),
    "s6_01": (pair(S("s6_01"), ("5.2%", "good", "UNEMPLOYED, WITH A DEGREE", "vs 7.4% with no degree, Sept 2026"), ("1.5&times;", "pay", "THE PAY", "degree vs high school, 2025")), NYFED),   # #1 #2 #3
    "s6_02": (strip("IT DEPENDS ON THE MAJOR.", S("s6_02")), ""),
    "s6_03": (strip("WHICH DEGREE? WHAT FIRST JOB?", S("s6_03"), y=377) + stamp("5.2%", round(S("s6_03") + 1.0, 3), 1430, 144)
              + stamp("4.0%", round(S("s6_03") + 1.5, 3), 1540, 760, color="var(--g-ink)", rot=6), ""),
}
IDS = list(SHOTS)


def page(final):
    shots = []
    for i, k in enumerate(IDS):
        html, src = SHOTS[k]
        t_out = L[IDS[i + 1]] if i + 1 < len(IDS) else END
        src_html = f'<div class="src">{src}</div>' if src else ""
        shots.append(f'<div class="shot" data-in="{L[k]}" data-out="{t_out}">{html}{src_html}</div>')
    draft = "" if final else '<div id="draft">DRAFT &middot; EP003 COLLAGE</div>'
    return (R / "scripts/ep003_collage.html").read_text().replace("{{ROOT_CSS}}", root_css()).replace("{{END}}", str(END)) \
        .replace("{{SHOTS}}", "\n".join(shots)).replace("{{DRAFT}}", draft)


if __name__ == "__main__":
    final = "final" in sys.argv
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy(WORK / "mix.wav", OUT / "assets/mix.wav")
    for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(R / "episodes/002/film" / f, OUT / f)
    (OUT / "index.html").write_text(page(final))
    print(f"EP003 collage: {len(IDS)} shots · T {END:.1f}s · 0.618T {G2} → {OUT}")
