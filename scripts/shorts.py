"""롱폼에서 숏폼 만들기(파이프라인 8단계): 구간을 잘라 1080×1920 가운데에 16:9 그대로 얹고, 위에 제목, 아래에 큰 자막.

사용: python3 -I scripts/shorts.py NNN <롱폼.mp4> [id ...]   → output/NNN/04_exports/EPNNN_short_<id>.mp4
설정: episodes/NNN/shorts.json = [{id, t0, t1, kicker, title}] (title 안 <span class='bad|good'>는 지표 색)
자막: episodes/NNN/subs/en.srt에서 구간에 걸친 조각을 잘라 시각을 옮긴다.
화면(brand/GOLDEN.md, yt-pipeline 8단계): 위 제목 칸 656 · 영상 608(1080×16/9) · 자막 띠 216 · 아래 440과 오른쪽 150은 비움(쇼츠 버튼).
"""
import json, re, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))   # python3 -I는 스크립트 폴더를 경로에 넣지 않는다
from golden_kit import R, _em, fit_size, no_break_hyphen, root_css

W, H, VID_Y, VID_H, CAP_H = 1080, 1920, 656, 608, 216   # 656 + 608 + 216 + 440 = 1920
PAD_L, PAD_R = 55, 150                                  # 오른쪽 150 = 쇼츠 좋아요·댓글 버튼 자리


def ts(s):
    h, m, rest = s.split(":"); sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def cues(srt, t0, t1):
    """구간 [t0, t1)에 걸친 자막 조각 → [(시작, 길이, 글)] (구간 기준 초)."""
    out = []
    for b in Path(srt).read_text().strip().split("\n\n"):
        ln = b.splitlines(); a, z = (ts(x.strip()) for x in ln[1].split("-->"))
        a, z = max(a, t0), min(z, t1)
        if z - a > 0.05: out.append((round(a - t0, 3), round(z - a, 3), " ".join(ln[2:])))
    return out


TITLE_H = VID_Y - 89 - 55 - 42 - 21   # 제목 칸 높이 449 = 위 여백 89 · 아래 여백 55 · 머리말 한 줄 42 · 사이 21


def title_size(plain, width=W - PAD_L - PAD_R):
    """가로(가장 긴 단어)와 세로(줄 수 × 크기) 모두 제목 칸에 들어가는 가장 큰 피보나치 크기.
    WHY: 가로만 보면 144가 골라져 여섯 줄이 되어 화면 위로 넘쳤다(숏 3, 2026-11-19)."""
    for size in (144, 89, 55):
        if fit_size(plain, width, sizes=(size,), by="word") != size or _em(max(plain.split(), key=_em)) * size > width: continue
        lines, cur = 1, 0.0
        for w in plain.split():
            ww = _em(w + " ") * size
            if cur and cur + ww > width: lines, cur = lines + 1, 0.0
            cur += ww
        if lines * size <= TITLE_H: return size
    return 55


def page(s, dur, caps):
    """숏 한 편의 index.html."""
    size = title_size(re.sub(r"<[^>]+>", "", s["title"]))
    cap_html = "\n".join(f'<div id="cap{i}" class="clip cap" data-start="{a}" data-duration="{d}" data-track-index="2">{t}</div>' for i, (a, d, t) in enumerate(caps))
    # 끝까지 볼 이유: 마지막 89프레임(2.97초)에 제목 칸이 다음 편 예고로 바뀐다(이어 보기 순서, 2026-11-19 사용자 가이드)
    nxt_t = round(dur - 89 / 30, 3)
    nxt = (f'<div id="nxt" class="clip nxt" data-start="{nxt_t}" data-duration="{round(dur - nxt_t, 3)}" data-track-index="3">'
           f'<div class="kick">{s["next_kicker"]}</div><div class="ttl" style="font-size:{title_size(s["next"])}px">{no_break_hyphen(s["next"])}</div></div>') if s.get("next") else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width={W}, height={H}" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{root_css()}
:root {{ --gb-sans: Inter, 'Helvetica Neue', Arial, sans-serif; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: var(--g-main); font-family: var(--gb-sans); }}
.top {{ position: absolute; left: 0; top: 0; width: {W}px; height: {VID_Y}px; padding: 89px {PAD_R}px 55px {PAD_L}px;
        display: flex; flex-direction: column; justify-content: flex-end; gap: 21px; color: var(--g-ink); }}
.kick {{ font: 800 34px/1.236 var(--gb-sans); letter-spacing: .04em; color: var(--g-ink-soft); }}
.ttl {{ font-family: 'Archivo Black', sans-serif; font-size: {size}px; line-height: 1.0; }}
.ttl .bad {{ color: var(--g-bad); }} .ttl .good {{ color: var(--g-good); }}
#v {{ position: absolute; left: 0; top: {VID_Y}px; width: {W}px; height: {VID_H}px; object-fit: cover; }}
.band {{ position: absolute; left: 0; top: {VID_Y + VID_H}px; width: {W}px; height: {CAP_H}px; background: var(--g-second); }}
.cap {{ position: absolute; left: 0; top: {VID_Y + VID_H}px; width: {W}px; height: {CAP_H}px; padding: 0 {PAD_R}px 0 {PAD_L}px;
        display: flex; align-items: center; font: 800 55px/1.236 var(--gb-sans); color: var(--g-main); }}
.nxt {{ position: absolute; left: 0; top: 0; width: {W}px; height: {VID_Y}px; padding: 89px {PAD_R}px 55px {PAD_L}px; background: var(--g-second);
        display: flex; flex-direction: column; justify-content: flex-end; gap: 21px; color: var(--g-main); }}
.nxt .kick {{ color: var(--g-loud); }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="{W}" data-height="{H}">
<div class="top"><div class="kick">{s["kicker"]}</div><div class="ttl">{no_break_hyphen(s["title"])}</div></div>
<video id="v" class="clip" src="assets/clip.mp4" data-start="0" data-duration="{dur}" data-track-index="1" data-has-audio="true" data-fade-in="0.267" data-fade-out="0.433"></video>
<div class="band"></div>
{cap_html}
{nxt}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
tl.to({{}}, {{ duration: {dur} }}, 0);
window.__timelines["main"] = tl;
</script>
</body></html>
"""


def build(ep, src, s):
    """구간 자르기 → 프로젝트 쓰기 → 렌더. 반환: 완성 mp4 경로."""
    dur = round(s["t1"] - s["t0"], 3)
    proj = R / f"output/{ep}/03_work/shorts/{s['id']}"
    (proj / "assets").mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s["t0"]), "-i", str(src), "-t", str(dur),
                    "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", str(proj / "assets/clip.mp4")], check=True)
    for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(R / f"episodes/{ep}/film/{f}", proj / f)
    (proj / "index.html").write_text(page(s, dur, cues(R / f"episodes/{ep}/subs/en.srt", s["t0"], s["t1"])))
    out = R / f"output/{ep}/04_exports/EP{ep}_short_{s['id']}.mp4"
    subprocess.run(["npx", "hyperframes", "render", "-o", str(out)], cwd=proj, check=True)
    return out


if __name__ == "__main__":
    ep, src, want = sys.argv[1], Path(sys.argv[2]).resolve(), set(sys.argv[3:])
    for s in json.loads((R / f"episodes/{ep}/shorts.json").read_text()):
        if not want or s["id"] in want: print("short", s["id"], "->", build(ep, src, s))
