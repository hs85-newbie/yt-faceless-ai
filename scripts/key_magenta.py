"""마젠타(#FF00FF) 배경을 투명으로 빼고, 남은 종이 조각만 여백 없이 잘라 PNG로 저장한다.

사용: python3 -I scripts/key_magenta.py output/001/02_raw/paper output/001/02_raw/paper_cut
배경 판정: 분홍(R−G 크고 B−G도 큼). Gemini가 순색 대신 그늘진 분홍 종이를 깔아서 색차로 판정한다.
종이 조각은 가장 큰 덩어리 하나만 남긴다(구석의 회색 얼룩 등 제거). 가장자리 분홍 번짐은 색을 중화한다.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

src, dst = Path(sys.argv[1]), Path(sys.argv[2]); dst.mkdir(parents=True, exist_ok=True)
for f in sorted(src.glob("*.png")):
    a = np.asarray(Image.open(f).convert("RGB")).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = np.clip(((r - g) - 45) / 35, 0, 1) * np.clip(((b - g) - 15) / 25, 0, 1)   # 0 = 종이, 1 = 분홍 배경
    lab, n = ndimage.label(m < 0.5)
    keep = lab == (np.argmax(np.bincount(lab.ravel())[1:]) + 1)   # 가장 큰 종이 덩어리
    keep = ndimage.binary_fill_holes(keep)
    alpha = (1 - m) * 255 * ndimage.binary_dilation(keep, iterations=3)
    a[..., 0] = np.where(m > 0, np.minimum(r, g + (b - g) * 0.3 + 20), r)   # 반투명 테두리의 분홍기 제거
    a[..., 2] = np.where(m > 0, np.minimum(b, g + 20), b)
    # 분홍 반사광 제거: 채도 낮은 픽셀(크림 종이)만 밝기는 두고 색을 크림(#f4efe3)으로 돌린다. 머스터드·빨강·청회색은 채도가 높아 그대로
    mx, mn = a.max(axis=2), a.min(axis=2); sat = (mx - mn) / (mx + 1)
    w = np.clip((0.30 - sat) / 0.12, 0, 1)[..., None]
    lum = a.mean(axis=2, keepdims=True); cream = np.array([244, 239, 227], np.float32) / 236.7
    a = a * (1 - w) + lum * cream * w
    rgba = np.dstack([np.clip(a, 0, 255), alpha]).astype(np.uint8)
    ys, xs = np.where(alpha > 20)
    assert len(xs) > 1000, f"{f.name}: 종이가 거의 안 남음(배경 판정 실패)"
    pad = 6
    crop = rgba[max(0, ys.min() - pad):ys.max() + pad, max(0, xs.min() - pad):xs.max() + pad]
    Image.fromarray(crop).save(dst / f.name)
    print(f.name, crop.shape[1], "x", crop.shape[0], f"keep {100 * (alpha > 20).mean():.0f}%")
