# 구조

```
[참고 영상 URL]
   │  /yt-viral → 후보 선정
   ▼
[/watch (Gemini)] ── 구조 분석 메모 (훅·전개·CTA 타이밍)
   ▼
[Opus 5.5 + /yt-script] ── 영어 대본 (60초, 클립 4~6개)
   │  /ai-video-storyboard → 클립별 프롬프트 (시각 일관성)
   ▼
[Higgsfield 웹 ← Claude in Chrome] ── 클립 mp4 (Kling 3.0 720p)
   ▼
[HyperFrames] 제목 카드·숫자 그래픽·전환   [Voicebox] 내레이션 wav   [/embedded-captions] 영어 자막
   ▼
[ffmpeg 합성] ── output/short_NNN_vN.mp4 (1080x1920)
   ▼
[scripts/upload] ── YouTube Data API (컨펌 게이트 뒤)
   ▼
[/yt-retention] ── 2주 후 측정
```

## 결정 기록
- 되돌리기 어려운 결정은 `docs/adr/ADR-NNN.md` 에 남긴다. 첫 항목은 ADR-001(힉스필드 브라우저 경로).
