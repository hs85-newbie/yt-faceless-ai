"""황금비·피보나치 템플릿 → 에피소드 계획서 + 블록 샘플 화면.

사용: python3 -I scripts/golden.py NNN
입력: episodes/NNN/golden.json (제목·숫자·절 구분·클라이맥스 줄, 내레이션 폴더), brand/golden.css (색), templates/golden/blocks/ (화면 틀)
산출: episodes/NNN/GOLDEN_PLAN.md (0.382T·0.618T와 걸리는 줄, 클라이맥스 위치)
      output/NNN/03_work/golden/ (HyperFrames: 규칙판·제목 카드·썸네일·숫자 카드·시간 설계도 → npx hyperframes snapshot)
규칙: brand/GOLDEN.md. 색 값은 바뀌어도 이 스크립트와 블록은 그대로다(역할 이름만 쓴다).
"""
import json, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))   # python3 -I는 스크립트 폴더를 경로에 넣지 않는다
from golden_kit import R, PHI, fill, fit_size, line_starts, no_break_hyphen, root_css, spiral, time_plan

EP = sys.argv[1]
CFG = json.loads((R / f"episodes/{EP}/golden.json").read_text())
starts = line_starts(R / CFG["voice"], R / CFG["work"])
T = round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(R / CFG["work"] / "voice.wav")], capture_output=True, text=True, check=True).stdout), 1)
plan = time_plan(starts, T, CFG.get("climax"))
G1, G2 = 1 / PHI ** 2, 1 / PHI
NUM_COLOR = {"bad": "var(--g-bad)", "good": "var(--g-good)"}[CFG["number_metric"]]

# ── 계획서 ─────────────────────────────────────────────
sec = CFG["sections"]
rows = "\n".join(f"| {i + 1} | {n.replace('&middot;', '·')} | `{lid}` | {starts[lid]:.1f} | {starts[lid] / T:.3f} |" for i, (n, lid) in enumerate(sec))
c = plan.get("climax")
(R / f"episodes/{EP}/GOLDEN_PLAN.md").write_text(f"""# EP{EP} 황금 시간 계획 (자동 생성: python3 -I scripts/golden.py {EP})

규칙: `brand/GOLDEN.md` §5-1. 입력: `episodes/{EP}/golden.json`, 내레이션 `{CFG['work']}/voice.wav`.

- 전체 길이 T = **{T}초**
- 0.382T = **{plan[G1]['t']}초** → 가장 가까운 줄 `{plan[G1]['line']}`({plan[G1]['line_t']}초): 2막 시작
- 0.618T = **{plan[G2]['t']}초** → 가장 가까운 줄 `{plan[G2]['line']}`({plan[G2]['line_t']}초): 클라이맥스 자리
""" + (f"- 클라이맥스 줄 `{c['line']}` = {c['t']}초({c['frac']}T), 0.618T와 {c['off']:+.1f}초 차이 — {CFG.get('climax_note', '')}\n" if c else "") + f"""- 훅은 첫 13초. 숏은 3·5·8·13·21초. 움직임은 8·13·21·34·55 프레임.

| # | 절 | 첫 줄 | 시작(초) | T 비율 |
|---|---|---|---|---|
{rows}
""")

# ── 블록 샘플 ──────────────────────────────────────────
X0, XW = 89, 1920 - 2 * 89
px = lambda s: X0 + s / T * XW
bars = "".join(f'<div class="sec{" alt" if i % 2 else ""}" style="left:{px(starts[lid]):.0f}px;width:{px(starts[sec[i + 1][1]] if i + 1 < len(sec) else T) - px(starts[lid]):.0f}px"><span>{i + 1}</span></div>'
               for i, (_, lid) in enumerate(sec))
marks = "".join(f'<div class="gm" style="left:{px(plan[f]["t"]):.0f}px"><b>{lab}</b><i>{plan[f]["t"]}s</i></div>'
                for f, lab in ((G1, "0.382T &middot; ACT 2"), (G2, "0.618T &middot; CLIMAX")))
climax = f'<div class="cm" style="left:{px(c["t"]):.0f}px"><b>CLIMAX LINE {c["line"]}</b><i>{c["t"]}s = {c["frac"]}T</i></div>' if c else ""
legend = "".join(f"<span><b>{i + 1}</b> {n}</span>" for i, (n, _) in enumerate(sec))
fib = "".join(f'<div class="fb" style="width:{s * 21}px">{s}s</div>' for s in (3, 5, 8, 13, 8, 5, 3))
sq, path = spiral((1920 - round(1080 * PHI)) / 2, 0, round(1080 * PHI), 1080)
blocks = [
    fill("rules-grid", squares="".join(f'<rect x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}"/>' for x, y, s in sq), path=path),
    fill("title-card", doc_title=CFG["doc_title"], episode_tag=CFG["episode_tag"], title=no_break_hyphen(CFG["title_card"]), tag=CFG["tag"],
         title_size=fit_size(CFG["title_card"], 1920 - 822 - 89)),   # 제목 왼쪽 822, 오른쪽 여백 89
    fill("thumbnail", title=no_break_hyphen(CFG["title"]), title_size=fit_size(CFG["title"], 1187 - 2 * 89, by="word"), kicker=CFG["kicker"], number=CFG["number"], number_color=NUM_COLOR, caption=CFG["number_caption"]),
    '<div style="position:absolute;inset:0;background:var(--g-main)"></div>' +
    fill("number-card", number=CFG["number"], number_color=NUM_COLOR, label=CFG["card_label"], desc=CFG["card_desc"]),
    fill("time-plan", ep=f"EP{EP}", T=T, bars=bars, marks=marks, climax=climax, legend=legend, fib=fib),
]
slides = "\n".join(f'<div class="clip" style="position:absolute;inset:0;overflow:hidden" data-start="{i}" data-duration="1" data-track-index="1">{b}</div>'
                   for i, b in enumerate(blocks))
OUT = R / f"output/{EP}/03_work/golden"
OUT.mkdir(parents=True, exist_ok=True)
for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(R / "episodes/002/film" / f, OUT / f)
(OUT / "index.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1920, height=1080" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{root_css()}
:root {{ --gb-sans: 'Source Sans 3', 'Helvetica Neue', Arial, sans-serif; --gb-mono: 'IBM Plex Mono', Menlo, monospace; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: var(--g-main); font-family: var(--gb-sans); }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{len(blocks)}" data-width="1920" data-height="1080">
{slides}
</div>
<script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }}).to({{}}, {{ duration: {len(blocks)} }});</script>
</body></html>
""")
print(f"EP{EP}: T={T}s · 0.382T={plan[G1]['t']} ({plan[G1]['line']}) · 0.618T={plan[G2]['t']} ({plan[G2]['line']})"
      + (f" · climax {c['line']} {c['frac']}T" if c else "") + f" · blocks {len(blocks)} → {OUT}")
