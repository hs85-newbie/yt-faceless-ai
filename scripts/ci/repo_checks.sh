#!/usr/bin/env bash
# WHY: 퍼블릭 레포라 비밀값·생성물이 실수로 올라가는 걸 PR 단계에서 막는다.
set -euo pipefail
fail=0

# 1) 생성물·비밀 파일이 추적되고 있으면 실패
bad=$(git ls-files | grep -E '\.(mp4|mov|wav|mp3|m4a)$|(^|/)\.env($|\.)|credentials|token.*\.json$' || true)
if [ -n "$bad" ]; then echo "추적되면 안 되는 파일:"; echo "$bad"; fail=1; fi

# 2) 프로젝트 스킬은 name·description 프런트매터가 있어야 로드된다
for f in .claude/skills/*/SKILL.md; do
  [ -e "$f" ] || continue
  head -1 "$f" | grep -q '^---$' || { echo "프런트매터 없음: $f"; fail=1; }
  grep -q '^name: ' "$f" || { echo "name 없음: $f"; fail=1; }
  grep -q '^description:' "$f" || { echo "description 없음: $f"; fail=1; }
done

# 3) 파이썬 스크립트는 최소한 문법이 맞아야 한다
py=$(git ls-files '*.py' || true)
if [ -n "$py" ]; then python3 -m py_compile $py || fail=1; fi

[ "$fail" -eq 0 ] && echo "repo checks OK"
exit "$fail"
