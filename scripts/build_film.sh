#!/usr/bin/env bash
# 장면 페이지를 렌더용 폴더(output/NNN/film)에 모으고, 지정한 시각의 정지 화면을 찍어 한 장(sheet.jpg)으로 묶는다.
# 사용: scripts/build_film.sh 001 [t1 t2 ...]   (시각을 안 주면 각 장면 시작 +2초)
set -euo pipefail
EP="$1"; shift || true
LIB=/Users/cjons/lemo-opuscar
SRC="episodes/$EP/film"; OUT="output/$EP/film"
mkdir -p "$OUT/assets"
cp "$SRC/index.html" "$SRC/cues.json" "$OUT/"
cp brand/tokens.css "$OUT/tokens.css"
cp output/$EP/assets/*.png "$OUT/assets/" 2>/dev/null || true
if [ $# -eq 0 ]; then
  set -- $(python3 -I -c "import json;[print(round(s['start']+2,1)) for s in json.load(open('$OUT/cues.json'))['scenes']]")
fi
rm -rf "$OUT/stills"
(cd "$LIB" && node core/render/still.mjs "$PWD/../yt-faceless-ai/.claude/worktrees/ep001/$OUT" "$@" --out "$PWD/../yt-faceless-ai/.claude/worktrees/ep001/$OUT/stills" --size 1920x1080)
"$LIB/.venv/bin/python" "$LIB/core/render/sheet.py" "$OUT/sheet.jpg" "$OUT"/stills/*.jpg --cols 3 --w 640
echo "sheet: $OUT/sheet.jpg"
