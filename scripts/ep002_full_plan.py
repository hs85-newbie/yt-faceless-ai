"""EP002 풀 길이 드래프트(270.5초, 내레이션 포함): 캠퍼스 → 실업률 축 → 데이터 판 → 0.618T에 초봉이 솟는 산점도 → 요약.

사용: python3 -I scripts/ep002_full_plan.py [final] → output/002/03_work/full/ 에서 npx hyperframes render (final = 업로드본, DRAFT 표시 없음)
구조: episodes/002/03_script.md "화면 구조 확정" 절 · brand/GOLDEN.md §5-1 (0.382T = 103초 2막, 0.618T = 167초 클라이맥스)
숫자 출처(episodes/002/02_research.md 표 번호 — 화면에는 번호를 내보내지 않는다):
      1·2·3 전공별 실업률·순위 · 4 전기·기계공학 · 6 하향 취업 · 7·8 초봉·중간 경력 · 9·17 간호·물리·수학·금융 ·
      10·11·12 학위 유무 비교 · 13·14 BLS(14는 [전망] → 화면에 PROJECTION) · 15·16 스탠퍼드 Canaries.
시각: ep002_common.at() — 내레이션 단어가 들리기 0.15초 전.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))   # python3 -I는 스크립트 폴더를 경로에 넣지 않는다
from ep002_common import CS, CE, EE, ME, LINE, WORK, at
from ep002_scene import AVG_U, AVG_W, HW, XS, build, plate, statement
from golden_kit import fill, fit_size, no_break_hyphen
from ep002_charts import gap_bars, paired_bars
ART = Path(__file__).resolve().parents[1] / "output/anidoodle_test/out"   # 손그림 삽화 렌더(git 제외)

import subprocess
END = round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(WORK / "voice.wav")],
                                 capture_output=True, text=True, check=True).stdout), 1)   # 실제 내레이션 길이(음성 버전이 바뀌면 따라감)
L = LINE
def until(t): return round(t - 0.05, 2)   # 다음 카드가 뜨기 직전에 끈다

# ── 3D 카메라 4구도: 캠퍼스 · 실업률 축 · 산점도 · CS 구석(황금점) ──
CAMS = [{"p": [17, 14, 19], "t": [6.5, 0, 4]}, {"p": [6.2, 10.5, 15.5], "t": [6.2, 0, 2.2]},
        {"p": [6.2, 7.5, 19.5], "t": [6.2, 1.6, 2.0]}, {"p": [12.6, 6.6, 17.0], "t": [7.4, 2.0, 2.4]}]

S2, S3, S5, S8 = L["s2_01"], L["s3_01"], L["s5_01"], L["s8_01"]
PAY = L["s5_03"]                      # "And the pay." 159.5초 — 여기서 솟기 시작
F = lambda n: round(n / 30, 3)        # GOLDEN §4: 길이는 30fps 피보나치 프레임
GOLD = round(END * 0.618, 1)          # 167.2초: 산점도 완성, 카메라가 CS 구석으로
TL = [
    {"at": 0.0, "obj": "cam", "to": {"z": 0.86}, "d": S2 - 0.5, "ease": "sine.inOut"},          # 훅 동안 천천히 다가감
    {"at": S2, "obj": "st", "to": {"mix": 1}, "d": F(89), "ease": "none"},
    {"at": S2, "obj": "cam", "to": {"k": 1, "z": 1}, "d": F(89)},
    {"at": S2 + F(89), "obj": "st", "to": {"zone": 1}, "d": F(21)},
    {"at": S3, "obj": "cam", "to": {"z": 0.9}, "d": L["s3_05"] - S3, "ease": "sine.inOut"},        # 1기둥 동안 천천히
    {"at": S5, "obj": "cam", "to": {"z": 1}, "d": F(55)},
    {"at": PAY, "obj": "st", "to": {"grow": 1}, "d": F(144)},              # 클라이맥스: 솟음
    {"at": PAY, "obj": "cam", "to": {"k": 2}, "d": GOLD - PAY - 0.2},
    {"at": PAY + F(144), "obj": "st", "to": {"pay": 1}, "d": F(21)},
    {"at": GOLD, "obj": "cam", "to": {"k": 3}, "d": F(89)},               # 0.618T: CS가 황금점으로
    {"at": S8, "obj": "cam", "to": {"k": 2}, "d": F(89)},                                         # 요약: 산점도 전체
]

def card(i, major, big, small, kind, num, t, e, label=None, keep=False):
    return dict(id=i, major=major, big=big, small=small, kind=kind, num=num, t=t, e=e, label=label, keep=keep)

c = [
    card("code", CS, "SAFE?", "&ldquo;learn to code&rdquo; &middot; the advice for 20 years", "red", "neutral", at("s1_02@learn to code"), until(S2), "LEARN TO CODE", keep=True),
    card("ce1", CE, "#2", "7.8% unemployed, of 73 majors", "red", "bad", at("s2_01@second highest"), until(at("s2_01@computer science is")), keep=True),
    card("cs1", CS, "#4", "7.0% unemployed", "red", "bad", at("s2_01@computer science is"), until(L["s2_02"]), keep=True),
    card("cs2", CS, "7.0%", "new CS grads unemployed", "red", "bad", at("s2_02@7"), until(at("s2_02@art history"))),
    card("ah", "Art History", "6.7%", "lower than computer science", "white", "bad", at("s2_02@art history"), until(at("s2_02@philosophy"))),
    card("ph", "Philosophy", "5.1%", "lower than computer science", "white", "bad", at("s2_02@philosophy"), until(at("s2_02@nutrition"))),
    card("nu", "Nutrition Sciences", "4.5%", "lower than computer science", "white", "bad", at("s2_02@nutrition"), until(L["s2_03"]), label="NUTRITION"),
    card("ee", EE, "3.2%", "same campuses, much of the same math", "green", "good", at("s3_01@electrical"), until(at("s3_01@mechanical"))),
    card("me", ME, "4.4%", "mechanical engineering", "white", "bad", at("s3_01@mechanical"), until(L["s3_02"])),
    card("all", None, "4.2%", "all recent grads", None, "neutral", L["s3_02"], until(at("s3_02@so the trouble")), label="ALL MAJORS"),
    card("phy", "Physics", "6.6%", "number-heavy, still above average", "white", "bad", at("s3_03@physics"), until(at("s3_03@information"))),
    card("is", "Information Systems & Management", "6.0%", "number-heavy, still above average", "white", "bad", at("s3_03@information"), until(at("s3_03@mathematics")), label="INFO SYSTEMS"),
    card("ma", "Mathematics", "5.8%", "number-heavy, still above average", "white", "bad", at("s3_03@mathematics"), until(at("s3_03@but finance"))),
    card("fi", "Finance", "2.8%", "just as heavy on math", "green", "good", at("s3_03@but finance"), until(at("s3_03@nursing")), keep=True),
    card("nr", "Nursing", "2.1%", "a demanding science major", "green", "good", at("s3_03@nursing"), until(L["s3_04"]), keep=True),
    card("u_all", None, "39%", "of all recent grads work jobs that don't need a degree", None, "neutral", at("s5_02@for all recent"), until(at("s5_02@for art history")), label="UNDEREMPLOYED"),
    card("u_ah", "Art History", "45%", "underemployed", "white", "bad", at("s5_02@for art history"), until(at("s5_02@for philosophy"))),
    card("u_ph", "Philosophy", "47%", "underemployed", "white", "bad", at("s5_02@for philosophy"), until(at("s5_02@for computer science"))),
    card("u_cs", CS, "19%", "underemployed", "red", "good", at("s5_02@for computer science"), until(at("s5_02@for computer engineering")), keep=True),
    card("u_ce", CE, "16%", "underemployed", "red", "good", at("s5_02@for computer engineering"), until(PAY), keep=True),
    card("p_cs", CS, "$87,000", "typical early-career pay", "red", "pay", at("s5_03@87"), until(at("s5_03@computer engineering")), keep=True),
    card("p_ce", CE, "$90,000", "early-career pay", "red", "pay", at("s5_03@computer engineering"), until(at("s5_03@all majors")), keep=True),
    card("p_all", None, "$58,000", "all majors, early career", None, "neutral", at("s5_03@all majors"), until(at("s5_03@art history")), label="ALL MAJORS"),
    card("p_ah", "Art History", "$45,000", "early-career pay", "white", "neutral", at("s5_03@art history"), until(at("s5_03@by mid")), ),
    card("p_mid", CS, "$120,000", "mid-career, vs. $87,000 for all majors", "red", "pay", at("s5_03@by mid"), until(L["s5_04"]), keep=True),
    card("r_nu", "Nursing", "2.1%", "unemployed &middot; pays well with far less risk", "green", "good", at("s8_01@nursing"), until(at("s8_01@electrical")), keep=True),
    card("r_ee", EE, "3.2%", "unemployed &middot; pays well with far less risk", "green", "good", at("s8_01@electrical"), until(L["s9_01"]), keep=True),
]

TV = (S2 + 3.6, END)   # 축 눈금은 줄선 뒤 끝까지(판이 덮는 동안은 가려짐)
TICKS = [(f"{u}%", u * XS, 0, 5.5, *TV) for u in (2, 6, 8)] + [
    ("ALL MAJORS 4.2%", AVG_U * XS, 0, 5.5, *TV),
    ("&larr; FEWER JOBLESS", 2.6, 0, 6.1, *TV), ("MORE JOBLESS &rarr;", 10.0, 0, 6.1, *TV),
    ("ALL MAJORS $58,000", 1.9, AVG_W * HW + 0.25, 4.8, PAY + 4.6, END),
]
CAPS = [("73 MAJORS, ONE CAMPUS", at("s1_01@among 73"), until(at("s1_02@learn to code"))),
        ("CONCENTRATED IN SOFTWARE MAJORS", at("s3_02@so the trouble"), until(L["s3_03"])),
        ("HARD MATH DOESN&rsquo;T PREDICT IT", L["s3_04"], until(at("s3_04@what sets"))),
        ("THE GRADS WHO DO GET HIRED", S5, until(at("s5_02@for all recent"))),
        ("HIGH RISK, HIGH REWARD", L["s5_04"], until(L["s6_01"])),
        ("ONE CORNER BY ITSELF", S8, until(at("s8_01@nursing")))]

# WHY: 맞춤 썸네일은 채널 전화 인증이 필요해 쓸 수 없다(2026-11-19 사용자). 제목 장면("So is computer science still worth it?")을
#      썸네일과 같은 구성(templates/golden/blocks/thumbnail.html, episodes/002/golden.json 값)으로 그려 스튜디오 '동영상에서 선택'으로 고른다.
GCFG = json.loads((Path(__file__).resolve().parents[1] / "episodes/002/golden.json").read_text())
PLATES = [
    f'<div class="fade" data-in="{L["s2_03"]}" data-out="{until(S3)}" style="position:absolute;inset:0">'
    + fill("thumbnail", title=no_break_hyphen(GCFG["title"]), title_size=fit_size(GCFG["title"], 1187 - 2 * 89, by="word"), kicker=GCFG["kicker"],
           number=GCFG["number"], number_color={"bad": "var(--g-bad)", "good": "var(--g-good)"}[GCFG["number_metric"]], caption=GCFG["number_caption"]) + "</div>",
    statement(at("s3_04@what sets"), until(L["s3_05"]), "Straight into entry-level software jobs.",
              "What sets computer science and computer engineering apart is where they lead.", dark=True),
    statement(L["s3_05"], until(L["s4_01"]), "2024 data. One year. Small samples.",
              "Treat the exact ranking as rough. The gap between software and the rest is the part to take seriously."),
    plate(L["s4_01"], until(L["s4_02"]), "Workers aged 22&ndash;25 in the most AI-exposed jobs, incl. software developers",
          [("15%", "bad", "lower employment than young workers in less-exposed jobs, July 2025"),
           ("19%", "bad", "lower by June 2026")],
          "Source: Brynjolfsson, Chandar &amp; Chen, &ldquo;Canaries in the Coal Mine,&rdquo; Stanford Digital Economy Lab (rev. Aug 2026), ADP payroll data",
          chart=gap_bars([("15%", 15, "bad", "JULY 2025", True), ("19%", 19, "bad", "JUNE 2026", False)],
                         L["s4_01"], "0 = young workers in less-exposed jobs")),
    statement(L["s4_02"], until(L["s4_03"]), "Fewer hires. Not more layoffs.",
              "And no evidence of widespread job loss across the whole economy.", dark=True),
    statement(L["s4_03"], until(S5), "Patterns, not proof of cause.",
              "Remote work and interest rates were moving at the same time. (See our last video.)"),
    plate(L["s6_01"], until(L["s6_02"]), "Software developers, QA analysts &amp; testers",
          [("1,905,400", "neutral", "jobs in 2025"), ("$134,040", "pay", "median pay, 2025"),
           ("+10%", "good", "PROJECTION: growth 2025&ndash;35, much faster than average")],
          "Source: U.S. Bureau of Labor Statistics, Occupational Outlook Handbook", note="A projection, not a promise."),
    statement(L["s6_02"], until(L["s7_01"]), "Is the career still there? Forecast: yes.<br/>Is the first job harder now? Data: yes.",
              "Two questions parents often mix up.", dark=True, art="ladder.png"),
    plate(L["s7_01"], until(L["s7_02"]), "A degree still beats no degree (ages 22&ndash;27)",
          [("5.2%", "good", "recent grads unemployed, Sept 2026"), ("7.4%", "bad", "young workers without a degree, Sept 2026"),
           ("$60,000", "pay", "recent grads, median pay 2025"), ("$40,000", "neutral", "young high-school grads, 2025")],
          "Source: NY Fed, The Labor Market for Recent College Graduates",
          chart=paired_bars([("UNEMPLOYED, SEPT 2026", [("5.2%", 5.2, "good", "RECENT|GRADS"), ("7.4%", 7.4, "bad", "NO|DEGREE")]),
                             ("MEDIAN PAY, 2025", [("$60K", 60000, "pay", "RECENT|GRADS"), ("$40K", 40000, "neutral", "HIGH-SCHOOL|GRADS")])],
                            L["s7_01"])),
    statement(L["s7_02"], until(S8), "Not whether to go to college. Which major.",
              "For the first job, the major now matters more than the old advice admitted.", dark=True),
    statement(L["s9_01"], until(L["s9_02"]), "Harder to get than almost any other. Paid better than almost any other.",
              "The first job out of a software degree, 2024. What the data can&rsquo;t say yet: whether AI is the reason, or whether it lasts."),
    statement(L["s9_02"], END, "What&rsquo;s their plan for the first job?", "Not &ldquo;should they switch?&rdquo;", dark=True),
]

build({"name": "full", "end": END, "cards": c, "ticks": TICKS, "caps": CAPS, "tl": TL, "cams": CAMS, "plates": PLATES, "art": [ART / "ladder.png"],
       "audio": WORK / "mix.wav", "draft": None if "final" in sys.argv else "DRAFT &middot; FULL LENGTH",   # mix = 내레이션 + BGM 덕킹(scripts/golden_bgm.py 002)
       "credit": (L["s9_02"], END, "Original score. Piano samples: &ldquo;Salamander Grand Piano V3&rdquo; by Alexander Holm, CC BY 3.0 (creativecommons.org/licenses/by/3.0). Orchestral samples: VS Chamber Orchestra: Community Edition, Versilian Studios (CC0)."),
       "src": "Source: NY Fed, The Labor Market for Recent College Graduates (by major, 2024)"}, "golden")
assert all(x["t"] < x["e"] for x in c), [x["id"] for x in c if x["t"] >= x["e"]]
print(f"0.382T = {END * 0.382:.1f}s (s4_01 {L['s4_01']:.1f}) · 0.618T = {GOLD}s · pay rises from {PAY:.1f}s")
