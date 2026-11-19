"""문장 단위 transcript.srt → 업로드용 자막(한 조각 최대 2줄 × 42자). 시각은 줄 안에서 글자 수 비례로 나눈다.

사용: python3 scripts/srt_split.py <transcript.srt> <out.srt>
WHY: 내레이션 한 줄이 15초·200자까지 가서 그대로 올리면 화면을 덮는다. 자르는 순서는 문장 끝 → 쉼표 → 단어 경계.
"""
import re
import sys

MAX = 84   # 2줄 × 42자(유튜브 권장 한 줄 길이)


def ts(s):
    h, m, rest = s.split(":"); sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def fmt(t):
    ms = round(t * 1000); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def pieces(text):
    """문장으로 나눈 뒤, 긴 문장은 가운데에 가까운 쉼표나 단어 경계에서 반으로 나눈다."""
    out = []
    for sent in re.split(r"(?<=[.?!])\s+(?=[A-Z\"“])", text.strip()):
        stack = [sent]
        while stack:
            s = stack.pop(0)
            if len(s) <= MAX: out.append(s); continue
            mid, cuts = len(s) / 2, [m.end() for m in re.finditer(r",\s", s)] or [m.start() for m in re.finditer(r"\s", s)]
            k = min(cuts, key=lambda c: abs(c - mid))
            stack[:0] = [s[:k].strip(), s[k:].strip()]
    return out


def main(src, dst):
    blocks = [b for b in open(src).read().strip().split("\n\n") if "-->" in b]
    n, out = 0, []
    for b in blocks:
        lines = b.splitlines(); a, z = (ts(x.strip()) for x in lines[1].split("-->")); text = " ".join(lines[2:])
        ps = pieces(text); total = sum(len(p) for p in ps); t = a
        for p in ps:
            e = t + (z - a) * len(p) / total; n += 1
            out.append(f"{n}\n{fmt(t)} --> {fmt(e)}\n{p}\n"); t = e
    open(dst, "w").write("\n".join(out))
    print(f"{len(blocks)} lines -> {n} cues -> {dst}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
