"""EP002 장표 그래프(SVG). 숫자는 전부 episodes/002/02_research.md에 출처가 있는 값만 받는다 — 여기서 새 숫자를 만들지 않는다.

규칙(brand/GOLDEN.md + dataviz): 축 하나, 막대 끝 4px 둥글림, 값은 막대에 직접 표기, 숫자 색은 지표를 따른다.
막대는 .grow(data-in)로 proto.js가 시간에 맞춰 키운다. 크기 단위는 피보나치(34·55·89·144·233).
"""
from golden_kit import tokens

G = tokens()
COL = {"bad": G["bad"], "good": G["good"], "pay": G["good"], "neutral": G["neutral"]}
NUM = {"bad": G["bad"], "good": G["good"], "pay": G["good"], "neutral": G["ink"]}
FONT = "font-family:'Archivo Black',sans-serif"


def _bar(x, y, w, h, color, t_in, origin):
    """막대 하나. origin = top(아래로 매달림) | bottom(위로 솟음) — 자라는 기준점."""
    return (f'<rect class="grow" data-in="{t_in}" x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{color}" '
            f'style="transform-box:fill-box;transform-origin:{origin}"/>')


def gap_bars(rows, t_in, base_label, W=1742, H=560, per=20):
    """기준선(0)에서 아래로 매달린 격차 막대. rows = [(값 문자열, 수치, kind, 설명, 옅게?)] — 깊어질수록 나쁘다."""
    by, bw, out = 89, 233, []
    out.append(f'<line x1="0" y1="{by}" x2="{W}" y2="{by}" stroke="{G["ink"]}" stroke-width="3"/>')
    out.append(f'<text x="0" y="{by - 21}" font-size="34" font-weight="600" fill="{G["ink-soft"]}">{base_label}</text>')
    for i, (txt, v, kind, lab, faint) in enumerate(rows):
        x, h = 233 + i * (bw + 610), v * per   # 막대 사이 610: 옆 막대 설명(34px)이 다음 막대에 가리지 않게
        out.append(_bar(x, by + 3, bw, h, G["loud-tint"] if faint else COL[kind], t_in + 0.5 + i * 0.9, "top"))
        tx, ty = x + bw + 34, by + h
        out.append(f'<text x="{tx}" y="{ty - 34}" font-size="89" style="{FONT}" fill="{NUM[kind]}">{txt}</text>')
        out.append(f'<text x="{tx}" y="{ty + 8}" font-size="34" font-weight="600" fill="{G["ink"]}">{lab}</text>')
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="overflow:visible">{"".join(out)}</svg>'


def paired_bars(panels, t_in, W=1742, H=560, top=280):
    """나란한 작은 그래프 여러 개 — 단위가 다른 측정값은 축을 나눈다(이중 축 금지).
    panels = [(제목, [(값 문자열, 수치, kind, 아래 라벨)])]. 각 판 안에서 가장 큰 값이 top px."""
    pw, by, out = (W - 89 * (len(panels) - 1)) / len(panels), H - 89, []
    for p, (title, bars) in enumerate(panels):
        ox, mx = p * (pw + 89), max(v for _, v, _, _ in bars)
        out.append(f'<text x="{ox}" y="34" font-size="34" font-weight="800" fill="{G["ink"]}" letter-spacing="1">{title}</text>')
        out.append(f'<line x1="{ox}" y1="{by}" x2="{ox + pw}" y2="{by}" stroke="{G["ink"]}" stroke-width="3"/>')
        for i, (txt, v, kind, lab) in enumerate(bars):
            cx, h, bw = ox + pw * (0.27 + 0.46 * i), v / mx * top, 144
            out.append(_bar(cx - bw / 2, by - h, bw, h, COL[kind], t_in + 0.5 + p * 0.9 + i * 0.3, "bottom"))
            out.append(f'<text x="{cx}" y="{by - h - 21}" text-anchor="middle" font-size="89" style="{FONT}" fill="{NUM[kind]}">{txt}</text>')
            for k, part in enumerate(lab.split("|")):
                out.append(f'<text x="{cx}" y="{by + 42 + k * 34}" text-anchor="middle" font-size="28" font-weight="700" fill="{G["ink"]}">{part}</text>')
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="overflow:visible">{"".join(out)}</svg>'
