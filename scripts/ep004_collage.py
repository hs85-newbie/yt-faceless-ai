"""EP004 문서 콜라주 — Which majors are AI-proof? 숏 목록만. 부품은 scripts/collage_kit.py.

사용: python3 -I scripts/ep004_collage.py [final] → output/004/03_work/collage/ 에서 npx hyperframes render
숫자: 전부 episodes/004/02_research.md 번호(주석 #N). 전공별은 2024년 한 해.
시간 구조: T 145.3초, 0.382T 55.5(4절 산점도 직후), 0.618T 89.8 = 클라이맥스(5절 "장소·면허·환자에 묶인 일" 띠가 꽂힘).
제목 숏(s1_02)은 썸네일과 같은 구성 — 스튜디오 '동영상에서 선택'으로 고른다.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from golden_kit import fill, fit_size, no_break_hyphen
from collage_kit import COL, F, NYFED, STAN, bars, card, fork, pair, scatter, stamp, strip, timing, write

L, END, G2 = timing("004")
S = lambda k: L[k]
LSE = "Source: NY Fed, Liberty Street Economics (June 2026)"


def trio(t0, rows):
    """카드 세 장(폭 521 · 사이 89): 숫자는 89px — 144로는 521 카드에 꽉 찬다. rows = [(값, kind, 라벨, 작은 글)]."""
    return "".join(card(89 + i * (521 + 89), 233, 521, 377,
                        f'<div class="n" style="color:{COL[k]};font-size:89px">{v}</div><div class="lab">{lab}</div><div class="sub">{sub}</div>',
                        round(t0 + F(13) + i * F(55), 3), 90 + i, rot=(-2.618, 1.618, -2.618)[i]) for i, (v, k, lab, sub) in enumerate(rows))


def tags(t0, names, y=233, seed=100, step=F(13)):
    """작은 이름표 카드를 한 줄 4장씩(폭 377 · 높이 144 · 사이 55)."""
    return "".join(card(89 + (i % 4) * (377 + 55), y + (i // 4) * (144 + 55), 377, 144, f'<div class="lab">{n}</div>',
                        round(t0 + i * step, 3), seed + i, rot=(-2.618, 1.618)[i % 2]) for i, n in enumerate(names))


GCFG = {"title": "WHICH MAJORS<br/>ARE AI-PROOF?", "kicker": "FOR PARENTS", "number": "0.7%", "caption": "unemployed: special<br/>education grads, 2024"}
TITLE = fill("thumbnail", title=no_break_hyphen(GCFG["title"]), title_size=fit_size(GCFG["title"], 1187 - 2 * 89, by="word"),
             kicker=GCFG["kicker"], number=GCFG["number"], number_color="var(--g-good)", caption=GCFG["caption"])

SWEET = [("AEROSPACE", 2.2, 85, "good"), ("", 2.3, 75, "good"), ("", 2.2, 75, "good"), ("", 2.1, 70, "good"),   # WHY: 라벨이 금융 점(2.8, 70)에 겹쳤다
         ("", 3.2, 82, "good"), ("", 2.8, 70, "good"), ("", 3.5, 72, "good")]   # #3 항공우주·토목·건설·간호·전기·금융·경제

SHOTS = {   # 줄 id → (화면, 출처)
    "s1_01": (bars(S("s1_01"), [("SPECIAL EDUCATION", "0.7%", 0.7, "good"), ("ALL MAJORS", "4.2%", 4.2, "neutral"),
                                ("COMPUTER SCIENCE", "7.0%", 7.0, "bad")], "UNEMPLOYED, RECENT GRADS, 2024",
                   times=[round(S("s1_01") + 5.0, 3), round(S("s1_01") + 6.0, 3), round(S("s1_01") + 1.0, 3)]), NYFED),   # #2 #1 #5
    "s1_02": (f'<div class="pop full" data-t="{S("s1_02")}" data-r="0">{TITLE}</div>', ""),
    "s2_01": (card(377, 144, 987, 233, '<div class="kin struck">AI-PROOF</div>', round(S("s2_01") + F(8), 3), 51)
              + strip("WHO&rsquo;S GETTING HIRED. WHAT IT PAYS.", round(S("s2_01") + 5.0, 3), y=487), NYFED),   # #1
    "s3_01": (bars(S("s3_01"), [("SPECIAL EDUCATION", "0.7%", 0.7, "good"), ("MISC. EDUCATION", "1.1%", 1.1, "good"),
                                ("ELEMENTARY ED.", "1.2%", 1.2, "good"), ("ALL MAJORS", "4.2%", 4.2, "neutral")],
                   "UNEMPLOYED, RECENT GRADS, 2024"), NYFED),   # #2 #1
    "s3_02": (bars(S("s3_02"), [("SPECIAL EDUCATION", "$46,000", 46, "bad"), ("ELEMENTARY ED.", "$45,000", 45, "bad"),
                                ("ALL MAJORS", "$58,000", 58, "neutral")], "STARTING PAY, RECENT GRADS, 2024",
                   times=[round(S("s3_02") + 3.0, 3), round(S("s3_02") + 5.5, 3), round(S("s3_02") + 8.0, 3)]), NYFED),   # #2 #1
    "s3_03": (strip("SAFE BY ONE MEASURE. LOW PAY BY ANOTHER.", S("s3_03")), ""),
    "s4_01": (scatter(S("s4_01"), SWEET + [("SPECIAL ED.", 0.7, 46, "neutral"), ("ALL MAJORS", 4.2, 58, "neutral"),
                                          ("COMPUTER SCIENCE", 7.0, 87, "bad")],
                      "UNEMPLOYED &rarr;", "STARTING PAY &uarr;", (0, 8), (40, 90), zone=(4.2, 70)), NYFED),   # #3 #2 #1 #5
    "s4_02": (pair(S("s4_02"), ("2.1%", "good", "NURSING", "unemployed, 2024"), ("$70,000", "pay", "NURSING", "starting pay, 2024"))
              + stamp("13% UNDEREMPLOYED", round(S("s4_02") + 5.0, 3), 610, 680, color="var(--g-good)"), NYFED),   # #3 #4
    "s4_03": (trio(S("s4_03"), [("2.3%", "good", "CIVIL ENGINEERING", "$75,000 to start"), ("2.2%", "good", "AEROSPACE ENG.", "$85,000 to start"),
                                ("2.2%", "good", "CONSTRUCTION", "$75,000 to start")]), NYFED),   # #3
    "s4_04": (tags(S("s4_04") - F(34), ["NURSING", "CIVIL ENG.", "AEROSPACE ENG.", "CONSTRUCTION"], step=F(5))
              + tags(round(S("s4_04") + F(13), 3), ["ELECTRICAL ENG.", "FINANCE", "ECONOMICS"], y=432, seed=110, step=F(21)), NYFED),   # #3
    "s4_05": (pair(S("s4_05"), ("$87,000", "pay", "COMPUTER SCIENCE", "starting pay, 2024"), ("7.0%", "bad", "COMPUTER SCIENCE", "unemployed, 2024"),
                   gap=F(89)), NYFED),   # #5
    "s5_01": (tags(S("s5_01"), ["HOSPITALS", "JOB SITES", "AIRCRAFT", "POWER GRIDS"], y=144, seed=120, step=F(21))
              + strip("TIED TO A PLACE, A LICENSE, A PATIENT.", G2, y=413)
              + card(89, 754, 987, 144, '<div class="note">Our reading, not something the table measures.</div>',
                     round(S("s5_02") - 3.0, 3), 52, rot=1.618), ""),
    "s5_02": (fork(S("s5_02"), '<div class="fk">REMOTE</div><div class="sub">where the gap for young grads opened</div>',
                   '<div class="fk">ON SITE</div><div class="sub">e.g. mechanical engineering</div>'), LSE),   # #6
    "s5_03": (bars(S("s5_03"), [("MOST AI-EXPOSED", "&minus;11%", 11, "bad"), ("LEAST EXPOSED", "+10%", 10, "good")],
                   "EMPLOYMENT CHANGE, LATE 2022 &rarr; MID-2026", times=[round(S("s5_03") + 4.0, 3), round(S("s5_03") + 8.5, 3)]), STAN),   # #7
    "s5_04": (strip("PATTERNS, NOT PROOF.", S("s5_04"))
              + card(89, 754, 987, 144, '<div class="note">One year (2024). Small samples for some majors.</div>',
                     round(S("s5_04") + 2.0, 3), 53, rot=1.618), NYFED),
    "s6_01": (fork(S("s6_01"), '<div class="fk">HIRED</div><div class="sub">below-average unemployment</div>',
                   '<div class="fk">PAID</div><div class="sub">$70,000+ to start</div>'), NYFED),   # #3
    "s6_02": (strip("DOES AI HELP WITH THE WORK, OR DO THE WORK?", S("s6_02"), y=377)
              + stamp("WHAT DOES IT PAY?", round(S("s6_02") + 5.0, 3), 377, 700, color="var(--g-good)", rot=6), ""),
}

if __name__ == "__main__":
    write("004", L, END, SHOTS, "final" in sys.argv)
