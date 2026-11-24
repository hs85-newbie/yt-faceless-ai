"""EP003 문서 콜라주(G안) — 숏 목록만. 부품은 scripts/collage_kit.py.

사용: python3 -I scripts/ep003_collage.py [final] → output/003/03_work/collage/ 에서 npx hyperframes render
숫자: 전부 episodes/003/02_research.md 번호(주석 #N).
시간 구조: T 176.3초, 0.382T 67.4(3절 스탠퍼드), 0.618T 109.0 = 클라이맥스(4절 전공별 띠에서 컴퓨터과학이 마지막에 꽂힘).
제목 숏(s1_02)은 썸네일과 같은 구성 — 맞춤 썸네일 대신 스튜디오 '동영상에서 선택'으로 고른다(채널 전화 인증 불가).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from golden_kit import fill, fit_size, no_break_hyphen
from collage_kit import F, NYFED, STAN, bars, card, fork, num, pair, stamp, strip, timing, write

L, END, G2 = timing("003")

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


if __name__ == "__main__":
    write("003", L, END, SHOTS, "final" in sys.argv)
