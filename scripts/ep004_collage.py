"""EP004 문서 콜라주 v2 — Which majors are AI-proof? 숏 목록만. 부품은 scripts/collage_kit.py.

사용: python3 -I scripts/ep004_collage.py [final] → output/004/03_work/collage/ 에서 npx hyperframes render
숫자: 전부 episodes/004/02_research.md 번호(주석 #N). 대본 v2(자료 보강, 34줄).
썸네일 구간: s1_04 제목 숏 — 제목 문장 뒤 2.967초 정지(episodes/004/pauses.json). 스튜디오 '동영상에서 선택'으로 고른다.
T 382.3초 · 0.382T 146.1(4절 교육 전공 끝) · 0.618T 236.3 = 클라이맥스(6절 s6_03에 'WIN ON BOTH' 도장).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from golden_kit import fill, fit_size, no_break_hyphen
from collage_kit import COL, F, NYFED, STAN, bars, card, fork, num, pair, scatter, stamp, strip, timing, write

L, END, G2 = timing("004", voice="voice_v2", work="v2")
S = lambda k: L[k]
T = lambda k, d: round(L[k] + d, 3)   # 줄 시작 + d초
DAL = "Source: Dallas Fed, Dodini &amp; Smith, &ldquo;AI plays a role in weak labor market for college graduates&rdquo; (Sep 2026)"
CLE = "Source: Cleveland Fed, Cline &amp; Kaymak, Economic Commentary 2026-26 (Nov 2026)"
ANT = "Source: Anthropic, Massenkoff &amp; McCrory, &ldquo;Labor market impacts of AI&rdquo; (Mar 2026)"
MSR = "Source: Microsoft Research, Tomlinson et al., &ldquo;Working with AI&rdquo; (Oct 2026)"
BLS = "Source: U.S. Bureau of Labor Statistics, Employment Projections 2025&ndash;2035 (Aug 2026)"
CPS = "Source: U.S. Bureau of Labor Statistics, Current Population Survey (2025)"
GAL = "Source: Lumina Foundation&ndash;Gallup (Apr 2026)"
NACE = "Source: NACE (Apr &amp; May 2026)"


def trio(t0, rows):
    """카드 세 장(폭 521 · 사이 89): 숫자는 89px — 144로는 521 카드에 꽉 찬다. rows = [(값, kind, 라벨, 작은 글)]."""
    return "".join(card(89 + i * (521 + 89), 233, 521, 377,
                        f'<div class="n" style="color:{COL[k]};font-size:89px">{v}</div><div class="lab">{lab}</div><div class="sub">{sub}</div>',
                        round(t0 + F(13) + i * F(55), 3), 90 + i, rot=(-2.618, 1.618, -2.618)[i]) for i, (v, k, lab, sub) in enumerate(rows))


def tags(t0, names, y=233, seed=100, step=F(13)):
    """작은 이름표 카드를 한 줄 4장씩(폭 377 · 높이 144 · 사이 55)."""
    return "".join(card(89 + (i % 4) * (377 + 55), y + (i // 4) * (144 + 55), 377, 144, f'<div class="lab">{n}</div>',
                        round(t0 + i * step, 3), seed + i, rot=(-2.618, 1.618)[i % 2]) for i, n in enumerate(names))


def stack(t0, x, head, kind, names, seed):
    """제목 도장 + 이름표 세로 세 장(폭 610 · 높이 144 · 사이 34)."""
    out = [stamp(head, t0, x, 178, color=COL[kind], rot=-3)]
    for i, n in enumerate(names):
        out.append(card(x, 377 + i * (144 + 34), 610, 144, f'<div class="lab">{n}</div>', round(t0 + F(21) + i * F(13), 3), seed + i,
                        rot=(-2.618, 1.618)[i % 2]))
    return "".join(out)


def word(x, text, sub, t, seed, rot=-2.618):
    """큰 낱말 카드(폭 610 · 높이 269): 55px 굵은 글 + 작은 설명."""
    return card(x, 233, 610, 269, f'<div class="kin" style="font-size:55px;color:var(--g-ink)">{text}</div><div class="sub">{sub}</div>', t, seed, rot=rot)


def single(t, value, kind, label, sub, seed=60):
    """숫자 카드 한 장, 가운데(폭 610 · 높이 377)."""
    return card((1920 - 610) // 2, 233, 610, 377, num(value, kind, label, sub), t, seed)


def note(text, t, seed=52, y=787):
    return card(89, y, 987, 144, f'<div class="note">{text}</div>', t, seed, rot=1.618)


GCFG = {"title": "WHICH MAJORS<br/>ARE AI-PROOF?", "kicker": "FOR PARENTS", "number": "42%",
        "caption": "of bachelor&rsquo;s students weighed<br/>switching majors over AI"}   # #25
TITLE = fill("thumbnail", title=no_break_hyphen(GCFG["title"]), title_size=fit_size(GCFG["title"], 1187 - 2 * 89, by="word"),
             kicker=GCFG["kicker"], number=GCFG["number"], number_color="var(--g-bad)", caption=GCFG["caption"])

SWEET = [("AEROSPACE", 2.2, 85, "good"), ("", 2.3, 75, "good"), ("", 2.2, 75, "good"), ("", 2.1, 70, "good"),   # WHY: 간호 라벨이 금융 점(2.8, 70)에 겹쳤다
         ("", 3.2, 82, "good"), ("", 2.8, 70, "good"), ("", 3.5, 72, "good")]   # #3 항공우주·토목·건설·간호·전기·금융·경제

SHOTS = {   # 줄 id → (화면, 출처)
    "s1_01": (word(233, "COMPUTER SCIENCE", "built for the tech economy", T("s1_01", F(8)), 31)
              + word(1077, "NURSING &middot; EDUCATION", "", T("s1_01", 4.5), 32, rot=1.618)
              + stamp("MOST EXPOSED", T("s1_01", 2.5), 144, 540) + stamp("LEAST EXPOSED", T("s1_01", 6.0), 1000, 680, color="var(--g-good)", rot=6), DAL),   # #22
    "s1_02": (strip("MORE EXPOSED. FEWER EMPLOYED.", S("s1_02")), DAL),   # #22
    "s1_03": (pair(S("s1_03"), ("42%", "bad", "THOUGHT ABOUT SWITCHING", "bachelor&rsquo;s students, because of AI"),
                   ("13%", "neutral", "ALREADY SWITCHED", "bachelor&rsquo;s students, Oct 2025"), gap=F(55)), GAL),   # #25
    "s1_04": (f'<div class="pop full" data-t="{S("s1_04")}" data-r="0">{TITLE}</div>', ""),
    "s2_01": (card(377, 144, 987, 233, '<div class="kin struck">AI-PROOF</div>', T("s2_01", F(8)), 51)
              + strip("WHERE IS IT SHOWING UP?", T("s2_01", 6.0), y=487), ""),
    "s3_01": (stack(T("s3_01", 3.0), 144, "MOST EXPOSED", "bad", ["COMPUTER SCIENCE", "COMPUTER ENGINEERING", "LANGUAGES"], 140)
              + stack(T("s3_01", 6.0), 987, "LEAST EXPOSED", "good", ["NURSING", "EDUCATION", "PSYCHOLOGY"], 150), DAL),   # #22
    "s3_02": (pair(S("s3_02"), ("1.7 PTS", "bad", "LOWER EMPLOYMENT", "per 10 pts more automatable tasks"),
                   ("&minus;5%", "bad", "FIRST-YEAR EARNINGS", "more vs. less exposed, 2021&rarr;2024"), gap=6.0), DAL),   # #22
    "s3_03": (bars(S("s3_03"), [("ALL AGES", "&asymp;1 pt", 1, "bad"), ("AGES 23&ndash;30", "&asymp;2 pts", 2, "bad")],
                   "EXTRA UNEMPLOYMENT, MOST vs. LEAST AI-EXPOSED JOBS", times=[T("s3_03", 2.0), T("s3_03", 7.0)]), CLE),   # #23
    "s3_04": (pair(S("s3_04"), ("&minus;14%", "bad", "AGES 22&ndash;25", "getting into AI-exposed jobs, vs. 2022"),
                   ("NO DROP", "neutral", "OVER 25", "same measure"), gap=4.0), ANT),   # #21
    "s3_05": (bars(S("s3_05"), [("MOST AI-EXPOSED", "&minus;11%", 11, "bad"), ("LEAST EXPOSED", "+10%", 10, "good")],
                   "EMPLOYMENT CHANGE, LATE 2022 &rarr; MID-2026", times=[T("s3_05", 4.0), T("s3_05", 8.5)]), STAN),   # #7
    "s3_06": (strip("AI IS CHANGING WHO GETS IN.", S("s3_06")), ""),
    "s4_01": (bars(S("s4_01"), [("SPECIAL EDUCATION", "0.7%", 0.7, "good"), ("MISC. EDUCATION", "1.1%", 1.1, "good"),
                                ("ELEMENTARY ED.", "1.2%", 1.2, "good"), ("ALL MAJORS", "4.2%", 4.2, "neutral")],
                   "UNEMPLOYED, RECENT GRADS, 2024"), NYFED),   # #2 #1
    "s4_02": (bars(S("s4_02"), [("SPECIAL EDUCATION", "$46,000", 46, "bad"), ("ELEMENTARY ED.", "$45,000", 45, "bad"),
                                ("ALL MAJORS", "$58,000", 58, "neutral")], "STARTING PAY, RECENT GRADS, 2024",
                   times=[T("s4_02", 3.0), T("s4_02", 5.5), T("s4_02", 8.0)]), NYFED),   # #2 #1
    "s4_03": (strip("SAFE BY ONE MEASURE. LOW PAY BY ANOTHER.", S("s4_03")), ""),
    "s5_01": (bars(S("s5_01"), [("TRANSLATORS", "0.49", 0.492, "bad"), ("WRITERS", "0.45", 0.454, "bad"), ("CUSTOMER SERVICE", "0.41", 0.408, "bad"),
                                ("ORAL SURGEONS", "0.03", 0.026, "good"), ("PHLEBOTOMISTS", "0.02", 0.022, "good")],
                   "AI APPLICABILITY SCORE, BY JOB", times=[T("s5_01", 4.0 + i * 1.2) for i in range(3)] + [T("s5_01", 9.0), T("s5_01", 10.0)]), MSR),   # #18
    "s5_02": (strip("HIGH SCORE &ne; JOB GONE.", S("s5_02"))
              + note("Weak link between AI applicability and pay (r = 0.13).", T("s5_02", 5.0)), MSR),   # #18 #19
    "s5_03": (bars(S("s5_03"), [("ALL JOBS", "+3.5%", 3.5, "neutral"), ("HEALTHCARE PRACT.", "+8.0%", 8.0, "good"),
                                ("OFFICE &amp; ADMIN", "&minus;4.0%", 4.0, "bad")], "PROJECTED JOB GROWTH, 2025&ndash;35",
                   times=[T("s5_03", 6.0), T("s5_03", 9.0), T("s5_03", 11.0)]), BLS),   # #8
    "s5_04": (pair(S("s5_04"), ("+41%", "good", "NURSE PRACTITIONERS", "fastest-growing job, 2025&ndash;35"),
                   ("$132,300", "pay", "MEDIAN PAY", "nurse practitioners, May 2025"), gap=4.0), BLS),   # #9
    "s6_01": (scatter(S("s6_01"), SWEET + [("SPECIAL ED.", 0.7, 46, "neutral"), ("ALL MAJORS", 4.2, 58, "neutral"),
                                          ("COMPUTER SCIENCE", 7.0, 87, "bad")],
                      "UNEMPLOYED &rarr;", "STARTING PAY &uarr;", (0, 8), (40, 90), zone=(4.2, 70)), NYFED),   # #3 #2 #1 #5
    "s6_02": (pair(S("s6_02"), ("2.1%", "good", "NURSING", "unemployed, 2024"), ("$70,000", "pay", "NURSING", "starting pay, 2024"))
              + stamp("13% UNDEREMPLOYED", T("s6_02", 5.0), 610, 680, color="var(--g-good)"), NYFED),   # #3 #4
    "s6_03": (trio(S("s6_03"), [("2.3%", "good", "CIVIL ENGINEERING", "$75,000 to start"), ("2.2%", "good", "AEROSPACE ENG.", "$85,000 to start"),
                                ("2.2%", "good", "CONSTRUCTION", "$75,000 to start")])
              + tags(T("s6_03", 9.5), ["ELECTRICAL ENG.", "FINANCE", "ECONOMICS"], y=677, seed=110, step=F(21))
              + stamp("WIN ON BOTH", G2, 1040, 760, color="var(--g-good)"), NYFED),   # #3 — 0.618T 클라이맥스
    "s6_04": (bars(S("s6_04"), [("REGISTERED NURSES", "+6%", 6, "good"), ("CIVIL ENGINEERS", "+6%", 6, "good"),
                                ("FINANCIAL ANALYSTS", "+7%", 7, "good")], "PROJECTED JOB GROWTH, 2025&ndash;35",
                   times=[T("s6_04", 5.0), T("s6_04", 6.5), T("s6_04", 8.0)]), BLS),   # #10 #14 #17
    "s7_01": (bars(S("s7_01"), [("HEALTHCARE PRACT.", "71.3%", 71.3, "good"), ("ALL WORKERS", "21.6%", 21.6, "neutral"),
                                ("COMPUTER &amp; MATH", "6.4%", 6.4, "bad")], "WORKERS HOLDING A LICENSE, 2025",
                   times=[T("s7_01", 2.5), T("s7_01", 4.0), T("s7_01", 5.0)]), CPS),   # #24
    "s7_02": (word(233, "PE LICENSE", "civil engineers sign off on public projects", T("s7_02", F(8)), 33)
              + word(1077, "CPA LICENSE", "150 semester hours of school", T("s7_02", 4.0), 34, rot=1.618)
              + stamp("SOMEONE LICENSED SIGNS", T("s7_02", 9.0), 377, 556)
              + note("Our reading, not something these tables measure.", T("s7_02", 11.0)), BLS),   # #14 #16
    "s7_03": (pair(S("s7_03"), ("+9%", "good", "ELECTRICIANS", "projected growth, 2025&ndash;35"),
                   ("4&ndash;5 YRS", "neutral", "APPRENTICESHIP", "most states require a license"), gap=4.0), BLS),   # #15
    "s8_01": (pair(S("s8_01"), ("$87,000", "pay", "COMPUTER SCIENCE", "starting pay, 2024"), ("7.0%", "bad", "COMPUTER SCIENCE", "unemployed, 2024"),
                   gap=F(89)), NYFED),   # #5
    "s8_02": (pair(S("s8_02"), ("+10%", "good", "SOFTWARE DEVELOPERS", "median $135,980"),
                   ("&minus;7%", "bad", "COMPUTER PROGRAMMERS", "projected, 2025&ndash;35 &middot; AI named"), gap=5.0), BLS),   # #11 #12
    "s8_03": (pair(S("s8_03"), ("75%", "bad", "COMPUTER PROGRAMMERS", "of tasks already seen in AI use"),
                   ("30%", "good", "OF ALL WORKERS", "no AI use seen: cooks, mechanics, bartenders"), gap=5.0), ANT),   # #20
    "s8_04": (single(T("s8_04", F(8)), "&minus;2%", "bad", "GRAPHIC DESIGNERS", "projected, 2025&ndash;35 &middot; AI design tools named"), BLS),   # #13
    "s8_05": (strip("NOT JUST THE MAJOR. THE WORK INSIDE IT.", S("s8_05")), ""),
    "s9_01": (strip("PATTERNS, NOT PROOF.", S("s9_01"))
              + note("Exposure measures differ. Mostly job data, not majors. Major data: 2024 only.", T("s9_01", 2.0)), ""),
    "s9_02": (pair(S("s9_02"), ("+5.6%", "good", "PLANNED HIRING", "new grads, Class of 2026"),
                   ("25%+", "neutral", "OF EMPLOYERS", "say AI cut some entry-level tasks"), gap=6.0), NACE),   # #26 #27
    "s10_01": (fork(S("s10_01"), '<div class="fk">HIRED</div><div class="sub">below-average unemployment</div>',
                    '<div class="fk">PAID</div><div class="sub">$70,000+ to start</div>'), NYFED),   # #3
    "s10_02": (strip("DOES AI HELP WITH THE WORK, OR DO THE WORK?", S("s10_02"), y=377)
               + stamp("WHAT DOES IT PAY?", T("s10_02", 5.0), 377, 700, color="var(--g-good)", rot=6), ""),
}

if __name__ == "__main__":
    write("004", L, END, SHOTS, "final" in sys.argv, work="v2")
