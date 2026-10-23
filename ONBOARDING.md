# 처음 오는 사람을 위한 안내

1. 저장소 받기
   ```bash
   git clone https://github.com/hs85-newbie/yt-faceless-ai.git && cd yt-faceless-ai
   ```
2. 기본 도구 확인 (없으면 `brew install ffmpeg yt-dlp`)
   ```bash
   ffmpeg -version | head -1   # 예상: ffmpeg version 7.x
   yt-dlp --version            # 예상: 2026.xx.xx
   ```
3. 영상 분석 키: `~/.config/watch/.env` 를 열어 `GEMINI_API_KEY=` 뒤에 키를 붙인다. 채팅·커밋에 키를 적지 않는다.
4. Claude Code를 이 폴더에서 열면 `CLAUDE.md` 규칙이 자동 적용된다. 첫 명령 예:
   ```
   /yt-viral AI tools for developers
   ```
