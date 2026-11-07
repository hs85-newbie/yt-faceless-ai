"""EP002 공통: NY Fed 전공별 데이터 → 캠퍼스 배치, 내레이션 단어 시각. 2D 콘셉트·3D 최종본이 함께 쓴다.

배치 규칙: 6개 구역(4x4 칸, 칸 사이 1칸 길), 같은 숏에 라벨이 함께 뜨는 건물은 화면 가로로 떨어뜨린다(POS).
"""
import csv, json, re
from pathlib import Path

R = Path(__file__).resolve().parents[1]
DATA = R / "output/002/02_raw/data/bymajor.csv"
VOICE = R / "output/002/02_raw/voice_v1"
WORK = R / "output/002/03_work/v1"

QUADS = {"hum": (0, 0), "eng": (5, 0), "sci": (10, 0), "hed": (0, 5), "soc": (5, 5), "bus": (10, 5)}
QNAME = {"hum": "ARTS & HUMANITIES", "eng": "ENGINEERING", "sci": "SCIENCES", "hed": "HEALTH & EDUCATION", "soc": "SOCIAL SCIENCES", "bus": "BUSINESS"}
CS, CE, EE, ME = "Computer Science", "Computer Engineering", "Electrical Engineering", "Mechanical Engineering"
CAT = {
    "eng": [CS, CE, EE, ME, "General Engineering", "Aerospace Engineering", "Chemical Engineering", "Civil Engineering",
            "Industrial Engineering", "Miscellaneous Engineering", "Engineering Technologies", "Miscellaneous Technologies",
            "Information Systems & Management", "Architecture", "Construction Services"],
    "hum": ["Art History", "Philosophy", "Fine Arts", "Performing Arts", "Commercial Art & Graphic Design", "Theology and Religion",
            "English Language", "Foreign Language", "Liberal Arts", "History", "Ethnic Studies", "Interdisciplinary Studies",
            "Communications", "Journalism", "Mass Media", "Advertising and Public Relations"],
    "sci": ["Physics", "Mathematics", "Biology", "Biochemistry", "Miscellaneous Biological Science", "Chemistry", "Earth Sciences",
            "Miscellaneous Physical Sciences", "Agriculture", "Animal and Plant Sciences", "Environmental Studies", "Geography"],
    "hed": ["Nutrition Sciences", "Nursing", "Health Services", "Medical Technicians", "Pharmacy", "Treatment Therapy",
            "Family and Consumer Sciences", "General Education", "Early Childhood Education", "Elementary Education",
            "Secondary Education", "Special Education", "Miscellaneous Education"],
    "soc": ["Psychology", "Criminal Justice", "Public Policy and Law", "Social Services", "Anthropology", "Economics",
            "Political Science", "Sociology", "General Social Sciences", "International Affairs"],
    "bus": ["Finance", "General Business", "Accounting", "Business Management", "Business Analytics", "Marketing", "Leisure and Hospitality"],
}
POS = {CS: (5, 3), CE: (7, 3), EE: (6, 0), ME: (8, 0), "Physics": (10, 0), "Mathematics": (13, 0),
       "Art History": (1, 3), "Philosophy": (3, 1), "Nutrition Sciences": (0, 5)}
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def buildings():
    """전공 73개 → [{id, name, u(실업률 %), w(초봉 $), gx, gy, q}]. CSV 값 그대로, 소수 1자리."""
    rows = {r["Major"]: r for r in csv.DictReader(DATA.open()) if r["Major"] != "Overall"}
    assert sorted(sum(CAT.values(), [])) == sorted(rows), "전공 73개가 구역에 정확히 한 번씩"
    out = []
    for q, names in CAT.items():
        ox, oy = QUADS[q]
        free = [(ox + k % 4, oy + k // 4) for k in range(16) if (ox + k % 4, oy + k // 4) not in POS.values()]
        for n in names:
            gx, gy = POS[n] if n in POS else free.pop(0)
            out.append({"id": slug(n), "name": n, "u": round(float(rows[n]["Unemployment Rate"]), 1),
                        "w": int(rows[n]["Median Wage Early Career"]), "gx": gx, "gy": gy, "q": q})
    assert len({(b["gx"], b["gy"]) for b in out}) == len(out), "칸 중복"
    return out


_secs = lambda s: (lambda h, m, r: int(h) * 3600 + int(m) * 60 + float(r.replace(",", ".")))(*s.split(":"))
_lines = json.loads((VOICE / "lines.json").read_text())
_words = json.loads((VOICE / "words.json").read_text())
LINE = {l["id"]: _secs(a) for l, (a, _) in zip(_lines, re.findall(r"(\S+) --> (\S+)", (WORK / "transcript.srt").read_text()))}
_norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def at(anchor, lead=0.15):
    """'s2_01' = 줄 시작, 's2_01@major by' = 그 구절 첫 단어가 들리기 lead초 전(절대 초)."""
    lid, _, ph = anchor.partition("@")
    if not ph: return LINE[lid]
    cat, own = "", []
    for k, (w, _, _) in enumerate(_words[lid]): n = _norm(w); cat += n; own += [k] * len(n)
    i = cat.find(_norm(ph)); assert i >= 0, anchor
    return round(LINE[lid] + max(0, _words[lid][own[i]][1]) - lead, 2)


if __name__ == "__main__":   # 자기 점검
    B = buildings(); assert len(B) == 73 and {b["name"] for b in B} >= {CS, CE, EE, ME}
    assert at("s2_01") < at("s2_01@major by") < at("s2_02"), "시각 순서"
    print("ok", len(B), at("s2_01@major by"))
