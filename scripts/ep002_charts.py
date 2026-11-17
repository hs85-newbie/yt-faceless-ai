"""EP002 장표 그래프(SVG). 숫자는 전부 episodes/002/02_research.md에 출처가 있는 값만 받는다 — 여기서 새 숫자를 만들지 않는다.

그래프는 장표 글(큰 숫자·설명) '옆'에 곁들인다 — 글을 대신하지 않는다(2026-11-18 사용자 지시).
자리: 세로 황금선 x 733 오른쪽 칸(폭 1098 = 1831 − 733), 높이 610(피보나치).
GOLDEN.md 필수: 위치·크기·간격은 피보나치(8·13·21·34·55·89·144·233·377), 글자는 34(라벨)·55(값), 선 굵기 3.
막대 길이만 데이터 비례(가장 긴 막대 = 377). 막대는 .grow(data-in)로 proto.js가 34프레임 동안 키운다.
"""
from golden_kit import tokens

G = tokens()
COL = {"bad": G["bad"], "good": G["good"], "pay": G["good"], "neutral": G["neutral"]}
NUM = {"bad": G["bad"], "good": G["good"], "pay": G["good"], "neutral": G["ink"]}
FONT = "font-family:'Archivo Black',sans-serif"
W, H, LONG = 1098, 610, 377
F = lambda n: round(n / 30, 3)   # 피보나치 프레임 → 초


def _bar(x, y, w, h, color, t_in, origin):
    """막대 하나. origin = top(아래로 매달림) | bottom(위로 솟음) — 자라는 기준점."""
    return (f'<rect class="grow" data-in="{t_in}" x="{x}" y="{y}" width="{w}" height="{h:.1f}" rx="4" fill="{color}" '
            f'style="transform-box:fill-box;transform-origin:{origin}"/>')


def _label(x, y, text, size=34, anchor="start", weight=700, color=None):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color or G["ink"]}">{text}</text>'


def _svg(parts):
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="overflow:visible">{"".join(parts)}</svg>'


def gap_bars(rows, t_in, base_label):
    """기준선(0)에서 아래로 매달린 격차 막대. rows = [(값 문자열, 수치, kind, 시점, 옅게?)] — 깊어질수록 나쁘다."""
    by, bw, mx, out = 89, 144, max(r[1] for r in rows), []
    out.append(f'<line x1="0" y1="{by}" x2="{W}" y2="{by}" stroke="{G["ink"]}" stroke-width="3"/>')
    out.append(_label(0, by - 21, base_label, weight=600, color=G["ink-soft"]))
    for i, (txt, v, kind, lab, faint) in enumerate(rows):
        x, h = 89 + i * (bw + 377), v / mx * LONG
        out.append(_bar(x, by + 3, bw, h, G["loud-tint"] if faint else COL[kind], t_in + F(21) + i * F(34), "top"))
        tx, ty = x + bw + 21, by + h
        out.append(f'<text x="{tx}" y="{ty - 21:.1f}" font-size="55" style="{FONT}" fill="{NUM[kind]}">{txt}</text>')
        out.append(_label(tx, f"{ty + 34:.1f}", lab))
    return _svg(out)


def paired_bars(panels, t_in):
    """나란한 작은 그래프 여러 개 — 단위가 다른 측정값은 축을 나눈다(이중 축 금지).
    panels = [(제목, [(값 문자열, 수치, kind, 아래 라벨 'A|B'는 두 줄)])]. 판 안 막대 중심은 144·377(피보나치)."""
    n = len(panels); pw, by, out = (W - 89 * (n - 1)) / n, H - 89, []   # 판 사이 89
    for p, (title, bars) in enumerate(panels):
        ox, mx = p * (pw + 89), max(v for _, v, _, _ in bars)
        out.append(_label(ox, 34, title, weight=800))
        out.append(f'<line x1="{ox}" y1="{by}" x2="{ox + pw}" y2="{by}" stroke="{G["ink"]}" stroke-width="3"/>')
        for i, (txt, v, kind, lab) in enumerate(bars):
            cx, h, bw = ox + (144, 377)[i], v / mx * LONG, 89
            out.append(_bar(cx - bw / 2, by - h, bw, h, COL[kind], t_in + F(21) + p * F(34) + i * F(13), "bottom"))
            out.append(f'<text x="{cx}" y="{by - h - 21:.1f}" text-anchor="middle" font-size="55" style="{FONT}" fill="{NUM[kind]}">{txt}</text>')
            for k, part in enumerate(lab.split("|")):   # 줄 간격 42 = 34 × 1.236(제목 줄 간격 규칙)
                out.append(_label(cx, by + 55 + k * 42, part, anchor="middle"))
    return _svg(out)
