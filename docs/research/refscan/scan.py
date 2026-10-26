"""레퍼런스 채널 수집 + 1단계 판별(얼굴·그래픽 비중). 결과: refscan/channels.json, refscan/gemini/*.md
사용: python3 -I scan.py
"""
import json, statistics as st, subprocess, sys, concurrent.futures as cf
from pathlib import Path

D = Path(__file__).parent
WATCH = Path.home() / ".claude/plugins/cache/claude-video/watch/0.3.2/skills/watch/scripts/watch.py"
QUERIES = ["economics explained animated", "how money works explained", "economics animation documentary", "finance explained animation",
           "why is everything so expensive explained", "housing market explained animation", "AI economy explained", "business explained animated",
           "the economics of explained", "how companies make money explained"]
KNOWN = ["@HowMoneyWorks", "@Vox", "@PolyMatter", "@TheInfographicsShow", "@EconomicsExplained", "@RealLifeLore", "@TheSwedishInvestor",
         "@EconomyMedia", "@Wendoverproductions", "@BusinessCasual", "@WhatIfShow", "@sambeckman"]


def run(cmd, timeout=180):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except Exception as e:
        print("ERR", cmd[:3], e, file=sys.stderr); return ""


# 1) 검색으로 채널 후보 모으기
cands = {}
for q in QUERIES:
    out = run(["yt-dlp", "--flat-playlist", "-J", "--no-warnings", f"ytsearch25:{q}"])
    try: entries = json.loads(out).get("entries") or []
    except Exception: continue
    for e in entries:
        if not e or (e.get("duration") or 0) < 300 or not e.get("channel_id"): continue
        c = cands.setdefault(e["channel_id"], {"url": f"https://www.youtube.com/channel/{e['channel_id']}", "name": e.get("channel"), "hits": 0, "views": 0})
        c["hits"] += 1; c["views"] += e.get("view_count") or 0
top = sorted(cands.values(), key=lambda c: -c["views"])[:22]
urls = [c["url"] for c in top] + [f"https://www.youtube.com/{h}" for h in KNOWN]


# 2) 채널별 최근 30편 → 중앙값·최대 배수·대표 영상
def channel_stats(url):
    out = run(["yt-dlp", "--flat-playlist", "-J", "--no-warnings", "--playlist-end", "30", url.rstrip("/") + "/videos"])
    try: d = json.loads(out)
    except Exception: return None
    if not isinstance(d, dict): return None
    vids = [e for e in (d.get("entries") or []) if e and e.get("view_count") and (e.get("duration") or 0) >= 300]
    if len(vids) < 6: return None
    v = [e["view_count"] for e in vids]; med = st.median(v); best = max(vids, key=lambda e: e["view_count"])
    date = run(["yt-dlp", "--no-warnings", "--playlist-end", "1", "--print", "upload_date", url.rstrip("/") + "/videos"], 60).strip()
    return {"name": d.get("channel") or d.get("uploader"), "url": url, "subs": d.get("channel_follower_count"), "n": len(v), "median": int(med),
            "max_mult": round(best["view_count"] / max(med, 1), 1), "rep_id": best.get("id"), "rep_title": best.get("title"), "rep_views": best["view_count"], "latest": date}


with cf.ThreadPoolExecutor(6) as ex:
    stats = [s for s in ex.map(channel_stats, urls) if s]
seen, chans = set(), []
for s in stats:
    if s["name"] in seen: continue
    seen.add(s["name"]); chans.append(s)
# 성과 조건(5): 중앙값 10만 이상 또는 배수 3배 이상 / 활동 조건(4): 최근 업로드 2025-10 이후
chans = [c for c in chans if (c["median"] >= 100000 or c["max_mult"] >= 3) and c["latest"][:6] >= "202510"]
chans = sorted(chans, key=lambda c: -c["median"])[:30]
print(len(chans), "channels pass views/activity filter", file=sys.stderr)

# 3) Gemini 1단계 판별: 대표 영상 1:00–3:00 구간
Q = ('Answer ONLY with one JSON object, no prose: {"host_face_on_camera": true|false, "real_footage_pct": int, "news_or_film_clips_pct": int, '
     '"designed_graphics_pct": int, "graphics_kind": "e.g. 2D animation / paper collage / infographic / maps / 3D / charts", '
     '"style_one_line": "one sentence on the visual identity", "avg_shot_seconds": number}. Percentages are shares of screen time in this range and should sum to about 100.')
(D / "gemini").mkdir(exist_ok=True)


def judge(c):
    f = D / "gemini" / f"{c['rep_id']}.md"
    if not f.exists():
        out = run(["python3", str(WATCH), f"https://www.youtube.com/watch?v={c['rep_id']}", "--engine", "gemini", "--start", "1:00", "--end", "3:00", "--question", Q], 600)
        f.write_text(out)
    txt = f.read_text(); i, j = txt.find("{"), txt.rfind("}")
    try: c["judge"] = json.loads(txt[i:j + 1])
    except Exception: c["judge"] = None
    return c


with cf.ThreadPoolExecutor(5) as ex:
    chans = list(ex.map(judge, chans))
(D / "channels.json").write_text(json.dumps(chans, ensure_ascii=False, indent=1))
for c in chans:
    j = c.get("judge") or {}
    ok = j and not j.get("host_face_on_camera") and (j.get("designed_graphics_pct") or 0) >= 70
    print(f"{'PASS' if ok else 'fail'} | {c['name'][:28]:28} | subs {c['subs'] or 0:>10,} | med {c['median']:>9,} | x{c['max_mult']:>5} | face {j.get('host_face_on_camera')} | gfx {j.get('designed_graphics_pct')}% | {str(j.get('graphics_kind'))[:40]}")
