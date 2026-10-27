"""레퍼런스 1차: 그 편 컨셉의 검색어로 채널 후보를 모으고, 성과·활동으로 거른 뒤 Gemini로 화면 구성을 판별한다.
사용: python3 -I scripts/refscan/scan.py episodes/NNN/refs/refscan.json
설정(JSON): {"queries": [...], "known": ["@handle", ...], "min_graphics": 70}
결과: 설정 파일 옆 channels.json, stage1/{video_id}.md
비용: 채널당 Gemini 1회(대표 영상 1:00~3:00, 약 1.3만 토큰). 실행 전 예상 금액을 사용자에게 승인받는다.
"""
import json, statistics as st, subprocess, sys, time, concurrent.futures as cf
from pathlib import Path

WATCH = Path.home() / ".claude/plugins/cache/claude-video/watch/0.3.2/skills/watch/scripts/watch.py"
Q = ('Answer ONLY with one JSON object, no prose: {"host_face_on_camera": true|false, "real_footage_pct": int, "news_or_film_clips_pct": int, '
     '"designed_graphics_pct": int, "graphics_kind": "e.g. 2D animation / paper collage / infographic / maps / 3D / charts", '
     '"style_one_line": "one sentence on the visual identity", "avg_shot_seconds": number}. Percentages are shares of screen time in this range and should sum to about 100.')


def run(cmd, timeout=180):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except Exception as e:
        print("ERR", cmd[:3], e, file=sys.stderr); return ""


def candidates(queries, top=22):
    cands = {}
    for q in queries:
        try: entries = json.loads(run(["yt-dlp", "--flat-playlist", "-J", "--no-warnings", f"ytsearch25:{q}"])).get("entries") or []
        except Exception: continue
        for e in entries:
            if not e or (e.get("duration") or 0) < 300 or not e.get("channel_id"): continue
            c = cands.setdefault(e["channel_id"], {"url": f"https://www.youtube.com/channel/{e['channel_id']}", "views": 0})
            c["views"] += e.get("view_count") or 0
    return [c["url"] for c in sorted(cands.values(), key=lambda c: -c["views"])[:top]]


def channel_stats(url):
    """최근 30편(5분 이상) → 중앙값·최고 배수·대표 영상."""
    try: d = json.loads(run(["yt-dlp", "--flat-playlist", "-J", "--no-warnings", "--playlist-end", "30", url.rstrip("/") + "/videos"]))
    except Exception: return None
    if not isinstance(d, dict): return None
    vids = [e for e in (d.get("entries") or []) if e and e.get("view_count") and (e.get("duration") or 0) >= 300]
    if len(vids) < 6: return None
    med = st.median(e["view_count"] for e in vids); best = max(vids, key=lambda e: e["view_count"])
    date = run(["yt-dlp", "--no-warnings", "--playlist-end", "1", "--print", "upload_date", url.rstrip("/") + "/videos"], 60).strip()
    return {"name": d.get("channel") or d.get("uploader"), "url": url, "subs": d.get("channel_follower_count"), "n": len(vids), "median": int(med),
            "max_mult": round(best["view_count"] / max(med, 1), 1), "rep_id": best.get("id"), "rep_title": best.get("title"), "rep_views": best["view_count"], "latest": date}


def judge(c, out):
    f = out / f"{c['rep_id']}.md"
    if not f.exists():
        f.write_text(run(["python3", str(WATCH), f"https://www.youtube.com/watch?v={c['rep_id']}", "--engine", "gemini", "--start", "1:00", "--end", "3:00", "--question", Q], 600))
    txt = f.read_text(); i, j = txt.find("{"), txt.rfind("}")
    try: c["judge"] = json.loads(txt[i:j + 1])
    except Exception: c["judge"] = None
    return c


def main(cfg_path):
    cfg_path = Path(cfg_path); cfg = json.loads(cfg_path.read_text()); D = cfg_path.parent
    urls = candidates(cfg["queries"]) + [f"https://www.youtube.com/{h}" for h in cfg.get("known", [])]
    with cf.ThreadPoolExecutor(6) as ex:
        stats = [s for s in ex.map(channel_stats, urls) if s]
    chans = list({s["name"]: s for s in stats}.values())
    # 성과: 중앙값 10만+ 또는 최고 3배+ / 활동: 최근 업로드가 실행일 기준 12개월 이내
    cutoff = str(int(time.strftime("%Y%m")) - 100)
    chans = sorted([c for c in chans if (c["median"] >= 100000 or c["max_mult"] >= 3) and c["latest"][:6] >= cutoff], key=lambda c: -c["median"])[:30]
    (D / "stage1").mkdir(exist_ok=True)
    with cf.ThreadPoolExecutor(5) as ex:
        chans = list(ex.map(lambda c: judge(c, D / "stage1"), chans))
    (D / "channels.json").write_text(json.dumps(chans, ensure_ascii=False, indent=1))
    for c in chans:
        j = c.get("judge") or {}
        ok = j and not j.get("host_face_on_camera") and (j.get("designed_graphics_pct") or 0) >= cfg.get("min_graphics", 70)
        print(f"{'PASS' if ok else 'fail'} | {c['name'][:28]:28} | med {c['median']:>9,} | x{c['max_mult']:>5} | gfx {j.get('designed_graphics_pct')}% | {str(j.get('graphics_kind'))[:40]}")


if __name__ == "__main__":
    main(sys.argv[1])
