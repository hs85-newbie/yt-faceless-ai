"""모션 테스트 점검용: 컷 경계마다 앞 2프레임·뒤 4프레임(24fps 그대로)을 한 줄로 뽑아 시트 한 장에 모은다.
yt-pipeline 모션 테스트 게이트의 "전환 앞뒤를 24fps로 본다"를 실행하는 도구.

사용: python3 -I scripts/cut_strips.py output/001/04_exports/EP001_v4_motiontest.mp4 output/001/03_work/v4/film/cuts.json output/001/03_work/v4/strips.jpg
"""
import json, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image

video, cuts_path, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
cuts = json.loads(cuts_path.read_text(encoding="utf-8"))["cuts"]
OFFS = [-2, -1, 0, 1, 3, 6]                      # 프레임 단위(1/24초)
W, H = 320, 180
rows = [c["t"] for c in cuts[1:]] + [cuts[0]["t"] + 0.0]
sheet = Image.new("RGB", (W * len(OFFS), H * len(rows)), "#111")
with tempfile.TemporaryDirectory() as tmp:
    for r, t in enumerate(rows):
        for k, o in enumerate(OFFS):
            ts = max(0.0, t + o / 24); f = Path(tmp) / f"{r}_{k}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ts:.4f}", "-i", video, "-frames:v", "1", "-vf", f"scale={W}:{H}", str(f)], check=True)
            sheet.paste(Image.open(f), (k * W, r * H))
sheet.save(out, quality=82)
print(out, len(rows), "boundaries ×", len(OFFS), "frames")
