# yt-faceless-ai

얼굴 없이 운영하는 영어 테크·AI 유튜브 채널의 제작 파이프라인. 쇼츠 매일 1편을 2주 실측한 뒤 8분 영상으로 확장할지 결정한다.

## 한 편이 만들어지는 흐름

| 단계 | 도구 | 비용 |
|---|---|---|
| 1. 조사 | `/yt-viral` (잘 되는 영상 수집) → `/watch` (Gemini가 영상 구조 분석) | Gemini 8분 1편 0.04~0.11달러 |
| 2. 대본 | Claude Opus 5.5 + `/yt-script` · `/yt-shorts` + `/ai-video-storyboard` (클립별 프롬프트) | 토큰 |
| 3. 클립 | Higgsfield 웹 화면을 Claude in Chrome으로 조작 (Kling 3.0 720p) | Plus 월 59달러 |
| 4. 조립 | HyperFrames(모션 그래픽) + Voicebox(내레이션) + `/embedded-captions`(자막) | 0 |
| 5. 업로드 | `scripts/` 의 YouTube Data API 업로드 | 0 |
| 6. 측정 | `/yt-retention` · `/yt-audit` | 0 |

힉스필드를 MCP가 아니라 브라우저로 쓰는 이유: 무제한 모델 혜택은 higgsfield.ai 웹 화면에서만 적용되고 MCP·CLI는 크레딧만 차감되기 때문이다(공식 요금 페이지, 2026-10-23 확인).

## 가설 (2주 실측)

14일 동안 쇼츠 15편을 올려 합산 조회수가 10만 미만이면 주제를 바꾼다. 이상이면 8분 영상 주 2편으로 확장한다.

## 폴더

- `prompts/` — 대본·클립 프롬프트 템플릿
- `scripts/` — 업로드·조립 스크립트
- `docs/adr/` — 되돌리기 어려운 결정 기록
- `output/` — 생성물 (git 제외)

## 준비물

- Higgsfield Plus 계정 (브라우저 로그인 상태, 전용 크롬 프로필)
- Gemini API 키 → `~/.config/watch/.env` 의 `GEMINI_API_KEY=` 줄
- Voicebox 앱 (`/Applications/Voicebox.app`)
- YouTube Data API OAuth 클라이언트 (업로드용, `.env` 에 보관 — 커밋 금지)

자세한 구조는 [ARCHITECTURE.md](ARCHITECTURE.md), 처음 오는 사람은 [ONBOARDING.md](ONBOARDING.md).
