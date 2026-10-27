"""Gemini 이미지 생성으로 컷아웃 그림을 뽑는다. 색은 brand/tokens.css 팔레트로 제한한다.

사용: python3 -I scripts/gen_images.py episodes/001/assets.json output/001/assets
키: ~/.config/watch/.env 의 GEMINI_API_KEY (프로젝트 전용 키). 비용은 장당 약 0.04달러(gemini-2.5-flash-image).
배경은 투명 대신 채널 배경색(#0f1115)으로 깔아 어두운 장면에 그대로 얹는다.
"""
import base64
import json
import sys
import urllib.request
from pathlib import Path

MODEL = "gemini-2.5-flash-image"
STYLE = ("Flat vector illustration, paper-cutout look, strong silhouettes, minimal detail, no text, no watermark, "
         "no gradients, no photorealism. The whole canvas is pure black (#0f1115) edge to edge: no floor, no ground plane, no horizon band, no lighter area anywhere; objects float on black. Palette only: "
         "ink #e8e6df, accent #e5b650, secondary #6f8fb0. Composition centered with generous empty margin. 16:9.")

spec_path, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
key = [l.split("=", 1)[1].strip() for l in open(Path.home() / ".config/watch/.env") if l.startswith("GEMINI_API_KEY=")][0]
out_dir.mkdir(parents=True, exist_ok=True)
spec = json.loads(spec_path.read_text(encoding="utf-8"))
only = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None  # 일부만 다시 뽑기
spec = [i for i in spec if not only or i["id"] in only]

for item in spec:
    style = "" if item.get("raw") else STYLE  # raw: 프롬프트가 자체 스타일을 정할 때(예: 종이 콜라주)
    body = {"contents": [{"parts": [{"text": f"{item['prompt']} {style}"}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9"}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        res = json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        print("FAIL", item["id"], e.code, e.read()[:200]); continue
    parts = res["candidates"][0]["content"]["parts"]
    img = next((p["inlineData"] for p in parts if "inlineData" in p), None)
    if not img:
        print("FAIL", item["id"], "no image in response"); continue
    ext = "png" if "png" in img["mimeType"] else "jpg"
    (out_dir / f"{item['id']}.{ext}").write_bytes(base64.b64decode(img["data"]))
    print("OK", item["id"], img["mimeType"])
