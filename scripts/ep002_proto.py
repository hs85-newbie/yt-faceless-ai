"""EP002 시안 두 장면(무음, 39초): 캠퍼스 → 실업률 축 줄서기 → 초봉 산점도. 승인용 시안이지 최종본이 아니다.

사용: python3 -I scripts/ep002_proto.py [v1|golden] → output/002/03_work/proto[_golden]/ (git 제외) 에서 npx hyperframes render
빌더: scripts/ep002_scene.py. 레퍼런스 문법: docs/research/ep002-major-viz-references.md.
숫자: 카드 문구는 episodes/002/02_research.md 3·7·9·17번 항목, 높이·위치는 같은 NY Fed 전공별 CSV 원값.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))   # python3 -I는 스크립트 폴더를 경로에 넣지 않는다
from ep002_common import CS, CE
from ep002_scene import AVG_U, AVG_W, HW, XS, build

THEME = sys.argv[1] if len(sys.argv) > 1 else "v1"
END, LINEUP, ZONE, GROW = 39.0, 2.0, 5.4, 25.4
CARDS = [   # 카드마다 3.5초 이상(읽기 하한). 숫자 색 = 지표(평균 4.2%보다 나쁘면 bad)
    dict(id="cs", major=CS, big="7.0%", small="7 in 100 recent grads are unemployed", kind="red", num="bad", t=6.5, e=10.5, keep=True),
    dict(id="ah", major="Art History", big="6.7%", small="lower than computer science", kind="white", num="bad", t=10.5, e=14.0),
    dict(id="ph", major="Philosophy", big="5.1%", small="lower than computer science", kind="white", num="bad", t=14.0, e=17.5),
    dict(id="ce", major=CE, big="7.8%", small="the second-highest of 73 majors", kind="red", num="bad", t=17.5, e=21.5, keep=True),
    dict(id="nu", major="Nursing", big="2.1%", small="one of the safest majors", kind="green", num="good", t=21.5, e=25.0),
    dict(id="cs2", major=CS, big="$87,000", small="starting pay, and 7.0% unemployed", kind="red", num="pay", t=29.6, e=34.0, keep=True),
    dict(id="ah2", major="Art History", big="$45,000", small="starting pay, and 6.7% unemployed", kind="white", num="pay", t=34.0, e=38.6),
]
TICKS = [(f"{u}%", u * XS, 0, 5.5, 5.6, 38.9) for u in (2, 6, 8)] + [
    ("ALL MAJORS 4.2%", AVG_U * XS, 0, 5.5, 5.6, 38.9),
    ("&larr; FEWER JOBLESS", 2.6, 0, 6.1, 5.6, 38.9), ("MORE JOBLESS &rarr;", 10.0, 0, 6.1, 5.6, 38.9),
    ("ALL MAJORS $58,000", 1.9, AVG_W * HW + 0.25, 4.8, 28.0, 38.9),
    ("HIGH PAY, MORE JOBLESS", 7.6, 4.6, -1.5, 28.4, 38.9),
]
TL = [
    {"at": LINEUP, "obj": "st", "to": {"mix": 1}, "d": 3.2, "ease": "none"},
    {"at": LINEUP, "obj": "cam", "to": {"k": 1}, "d": 3.2},
    {"at": ZONE, "obj": "st", "to": {"zone": 1}, "d": 0.6, "ease": "power2.out"},
    {"at": GROW, "obj": "st", "to": {"grow": 1}, "d": 2.2, "ease": "power3.inOut"},
    {"at": GROW, "obj": "cam", "to": {"k": 2}, "d": 2.6},
    {"at": GROW + 2.2, "obj": "st", "to": {"pay": 1}, "d": 0.6},
]
CAPS = [("73 MAJORS, ONE CAMPUS", 0.3, 1.9), ("LINE THEM UP BY UNEMPLOYMENT", 2.2, 5.2), ("NOW ADD STARTING PAY", 25.4, 29.3)]

build({"name": "proto" + ("" if THEME == "v1" else "_" + THEME), "end": END, "cards": CARDS, "ticks": TICKS, "caps": CAPS,
       "tl": TL, "draft": "DRAFT &middot; NO SOUND"}, THEME)
