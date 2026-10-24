# yt-faceless-ai

얼굴 없이 운영하는 영어 AI × 경제 설명 채널의 제작 파이프라인. 롱폼(10~13분)을 먼저 만들고, 그걸 잘라 쇼츠·릴스·틱톡을 만든다.

## 한 편이 만들어지는 흐름

`/yt-pipeline` 스킬이 아래 순서를 고정한다(`.claude/skills/yt-pipeline/SKILL.md`). 사람 확인은 4곳.

| 단계 | 도구 | 비용 |
|---|---|---|
| 1. 질문 발굴 | yt-dlp + `/yt-viral` | 0 |
| 2. 리서치 | 1차 자료 + `/watch`(Gemini, 구조 분석만) | 영상당 0.04~0.11달러 |
| 3. 대본 | Claude + `/yt-script` (7단계 비트시트) | 토큰 |
| 4. 패키징 | `/yt-package` | 0 |
| 5. 음성 | Voicebox 로컬 REST | 0 |
| 6. 화면·렌더 | HyperFrames + `/media-use` | 0 |
| 7. 챕터·설명 | `/yt-chapters` + `/yt-seo` | 0 |
| 8. 숏폼 | `/yt-shorts` + HyperFrames 세로 렌더 | 0 |
| 9. 업로드 | `scripts/` (유튜브·릴스), 틱톡 수동 | 0 |
| 10. 측정 | `/yt-retention` · `/yt-comment` · `/yt-audit` · `/yt-plan` | 0 |

AI 생성 영상은 쓰지 않는다. 이유는 `docs/adr/ADR-002-longform-first-no-ai-video.md`.

## 가설 (8주)

주 1~2편으로 8주에 12편. 평균 시청 지속률 35% 이상, 12편 중 1편 이상이 채널 중앙값 5배를 넘으면 통과.

## 폴더

- `episodes/NNN-slug/` — 에피소드별 기획·리서치·대본·상태(STATUS.md)
- `prompts/` — 대본 템플릿
- `scripts/` — 업로드·조립 스크립트
- `docs/adr/` — 되돌리기 어려운 결정 기록
- `output/` — 생성물 (git 제외)

## 준비물

- Higgsfield Plus 계정 (브라우저 로그인 상태, 전용 크롬 프로필)
- Gemini API 키 → `~/.config/watch/.env` 의 `GEMINI_API_KEY=` 줄
- Voicebox 앱 (`/Applications/Voicebox.app`)
- YouTube Data API OAuth 클라이언트 (업로드용, `.env` 에 보관 — 커밋 금지)

자세한 구조는 [ARCHITECTURE.md](ARCHITECTURE.md), 처음 오는 사람은 [ONBOARDING.md](ONBOARDING.md).
