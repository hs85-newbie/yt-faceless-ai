"""레퍼런스 2차: 고른 영상들의 훅·본문 30초를 컷 단위로 Gemini 분석하고, 비교용 프레임(5초 간격)을 무료로 뽑는다.
사용: python3 -I scripts/refscan/stage2.py episodes/NNN/refs/refscan.json output/NNN/refs
설정(JSON)에 추가: {"videos": {"채널명": "video_id", ...}, "segments": {"hook": ["0:00","0:30"], "body": ["2:00","2:30"]}}
결과: 설정 파일 옆 stage2/{id}_{seg}.md (커밋 가능), 프레임은 두 번째 인자 폴더(남의 영상 프레임이라 커밋 금지)
비용: 영상·구간당 Gemini 1회(약 5천 토큰).
"""
import json, subprocess, sys, concurrent.futures as cf
from pathlib import Path

WATCH = Path.home() / ".claude/plugins/cache/claude-video/watch/0.3.2/skills/watch/scripts/watch.py"
Q = ('Answer ONLY with one JSON object, no prose. List EVERY visual cut in this range. '
     '{"cuts":[{"t":"m:ss","seconds":number,"shot":"kinetic_text|chart|map|collage|character_anim|document_capture|photo|real_footage|ui_mockup|other",'
     '"text_motion":"none|static|kinetic","camera":"static|push|pan|parallax|zoom","transition_in":"hard_cut|whip|wipe|zoom|match|fade|morph|other"}],'
     '"distinct_shot_types":int,"distinct_transitions":int,"avg_shot_seconds":number,'
     '"reproducible_without_video_footage_pct":int,'
     '"reproducibility_note":"can this be rebuilt with HTML/CSS motion + still images + charts, without stock video, AI video or other people clips? one sentence",'
     '"signature_device":"the one recurring visual device that makes this channel recognisable"}')
DEFAULT_SEGS = {"hook": ["0:00", "0:30"], "body": ["2:00", "2:30"]}


def run(cmd, timeout=600):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except Exception as e:
        print("ERR", cmd[:3], e, file=sys.stderr); return ""


def gemini(vid, a, b, f):
    if not f.exists():
        f.write_text(run(["python3", str(WATCH), f"https://www.youtube.com/watch?v={vid}", "--engine", "gemini", "--start", a, "--end", b, "--question", Q]))
    return f


def frames(vid, seg, a, b, fdir):
    clip = fdir / f"{vid}_{seg}.mp4"
    if not clip.exists():
        run(["yt-dlp", "-q", "--no-warnings", "-f", "bv*[height<=480]", "--download-sections", f"*{a}-{b}", "-o", str(clip), f"https://www.youtube.com/watch?v={vid}"])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip), "-vf", "fps=1/5,scale=480:-2", str(fdir / f"{vid}_{seg}_%02d.jpg")])


def main(cfg_path, frame_dir):
    cfg_path = Path(cfg_path); cfg = json.loads(cfg_path.read_text())
    out = cfg_path.parent / "stage2"; fdir = Path(frame_dir); out.mkdir(exist_ok=True); fdir.mkdir(parents=True, exist_ok=True)
    segs = cfg.get("segments", DEFAULT_SEGS)
    jobs = [(v, s, *segs[s]) for v in cfg["videos"].values() for s in segs]
    with cf.ThreadPoolExecutor(4) as ex:
        list(ex.map(lambda j: frames(*j, fdir), jobs))
        for f in ex.map(lambda j: gemini(j[0], j[2], j[3], out / f"{j[0]}_{j[1]}.md"), jobs):
            print("done", f.name, f.stat().st_size)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
