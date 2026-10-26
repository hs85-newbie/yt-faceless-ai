"""2차: 6개 채널 대표 영상의 훅(0:00-0:30)과 본문(2:00-2:30)을 컷 단위로 Gemini 분석 + 무료 프레임 추출.
결과: refscan/s2/{id}_{seg}.md, refscan/frames/{id}_{seg}_NN.jpg
사용: python3 -I stage2.py
"""
import subprocess, sys, concurrent.futures as cf
from pathlib import Path

D = Path(__file__).parent
WATCH = Path.home() / ".claude/plugins/cache/claude-video/watch/0.3.2/skills/watch/scripts/watch.py"
VIDS = {"Antidote": "jPPzvuDIr1w", "PolyMatter": "CXfNGcMSwzU", "LITTLE BIT BETTER": "zxVoCw3P1Gc",
        "Kurzgesagt": "ujkD4SxPKOI", "How Money Works": "QmWyQ-BCD8E", "Economics Explained": "QtZfbWOkoIY"}
SEGS = {"hook": ("0:00", "0:30"), "body": ("2:00", "2:30")}
Q = ('Answer ONLY with one JSON object, no prose. List EVERY visual cut in this range. '
     '{"cuts":[{"t":"m:ss","seconds":number,"shot":"kinetic_text|chart|map|collage|character_anim|document_capture|photo|real_footage|ui_mockup|other",'
     '"text_motion":"none|static|kinetic","camera":"static|push|pan|parallax|zoom","transition_in":"hard_cut|whip|wipe|zoom|match|fade|morph|other"}],'
     '"distinct_shot_types":int,"distinct_transitions":int,"avg_shot_seconds":number,'
     '"reproducible_without_video_footage_pct":int,'
     '"reproducibility_note":"can this be rebuilt with HTML/CSS motion + still images + charts, without stock video, AI video or other people clips? one sentence",'
     '"signature_device":"the one recurring visual device that makes this channel recognisable"}')
(D / "s2").mkdir(exist_ok=True); (D / "frames").mkdir(exist_ok=True)


def run(cmd, timeout=600):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except Exception as e:
        print("ERR", cmd[:3], e, file=sys.stderr); return ""


def gemini(job):
    vid, seg = job; a, b = SEGS[seg]; f = D / "s2" / f"{vid}_{seg}.md"
    if not f.exists():
        f.write_text(run(["python3", str(WATCH), f"https://www.youtube.com/watch?v={vid}", "--engine", "gemini", "--start", a, "--end", b, "--question", Q]))
    return f


def frames(job):
    vid, seg = job; a, b = SEGS[seg]; clip = D / "frames" / f"{vid}_{seg}.mp4"
    if not clip.exists():
        run(["yt-dlp", "-q", "--no-warnings", "-f", "bv*[height<=480]", "--download-sections", f"*{a}-{b}", "-o", str(clip), f"https://www.youtube.com/watch?v={vid}"])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip), "-vf", "fps=1/5,scale=480:-2", str(D / "frames" / f"{vid}_{seg}_%02d.jpg")])
    return clip


jobs = [(v, s) for v in VIDS.values() for s in SEGS]
with cf.ThreadPoolExecutor(4) as ex:
    list(ex.map(frames, jobs))
    for f in ex.map(gemini, jobs):
        print("done", f.name, f.stat().st_size, file=sys.stderr)
