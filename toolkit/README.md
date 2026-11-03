# 도구함 — Counter Ledger에서 쓰는·검토한 스킬과 도구

이 채널 제작에 쓰거나 검토한 스킬·도구를 한곳에 모은 목록이다. 사용자가 공유한 것은 지금 쓰지 않아도 모두 적었다.
라이선스는 2026-11-03 GitHub 조회값이다. 정책은 MIT·Apache 2.0만 쓰고, 예외는 사용자 승인 건만 쓴다(Remotion·whisperX·web-design-guidelines).

상태 구분: **사용 중** = EP001 제작에 실제로 씀 · **설치됨** = 깔려 있고 필요할 때 씀 · **참고만** = 설치 없이 자료로 봄 · **보류** = 결정 대기 · **안 씀** = 쓰지 않기로 함

## 1. 지금 제작에 쓰는 것

| 이름 | 출처 | 라이선스 | 어디에 쓰나 | 상태 |
|---|---|---|---|---|
| yt-pipeline | 이 레포 `.claude/skills/yt-pipeline` | MIT(레포) | 10단계 제작 순서와 사람 확인 게이트 | 사용 중 |
| youtube-agent-skill (yt-viral·script·package·chapters·seo·shorts·retention·comment·audit·plan·edit) | github.com/Jakeschincariol/youtube-agent-skill | MIT | 주제 발굴, 훅 채점, 제목·썸네일, 챕터·설명, 숏폼, 업로드 후 분석. `yt-edit`은 합성 음성이라 안 씀 | 사용 중 |
| watch (claude-video 플러그인) | github.com/bradautomates/claude-video | MIT | 레퍼런스 영상을 Gemini로 분석(구조만, 대본 복제 금지) | 사용 중 |
| lemo-opuscar | github.com/lemomo-ai/lemo-opuscar | MIT | 렌더 엔진(정지 화면·영상·음량 맞춤), Kokoro 음성, Whisper 대조, 효과음 | 사용 중 |
| Three.js Skills | github.com/CloudAI-X/threejs-skills | MIT | 책상·매트·종이 소품 3D 장면 | 사용 중 |
| motion-graphics-skills (vox-explainer·animated-chart 등 15종) | github.com/charlie947/motion-graphics-skills | MIT | 종이 콜라주 규칙, 차트·제목 연출 기법 | 사용 중(일부) |
| motionmaxxing | github.com/Tejashmakwana/motionmaxxing | Apache-2.0 | 렌더 후 점검 게이트(빈 화면·엔드카드·화면 장식) | 사용 중 |
| bang-motion | github.com/bangtutorial/bang-motion | MIT | 키네틱 글자 규칙 | 설치됨 |
| Kokoro TTS (lemo-opuscar 안) | github.com/hexgrad/kokoro | Apache-2.0 | 영어 내레이션 `am_michael` | 사용 중 |
| Gemini API (이미지·영상 분석) | Google AI Studio 유료 키 | 유료 서비스 | 종이 소재 생성, 레퍼런스 분석 | 사용 중(호출마다 비용 승인) |
| yt-dlp · ffmpeg | brew | 무료 | 레퍼런스 수집, 합치기·인코딩 | 사용 중 |
| humanize-korean | github.com/epoko77-ai/im-not-ai | MIT | 한국어 보고서 문체 점검 | 사용 중 |

## 2. 설치돼 있고 필요할 때 쓰는 것

| 이름 | 출처 | 라이선스 | 어디에 쓰나 | 상태 |
|---|---|---|---|---|
| HyperFrames 묶음 (core·cli·animation·registry·media-use·embedded-captions 등) | github.com/heygen-com/hyperframes | Apache-2.0 | HTML 영상 렌더, 400여 기성 블록, 자막 | 설치됨(EP001은 lemo-opuscar 엔진 사용) |
| Video Shotcraft | github.com/Vincentwei1021/video-shotcraft | Apache-2.0 (Remotion 사용) | 제품 홍보형 카메라 연출 레시피 | 설치됨 |
| Clipify | github.com/louisedesadeleer/clipify | MIT | 롱폼에서 숏폼 구간 자르기·세로 변환 | 설치됨(숏폼 단계에서 whisper 설치 필요) |
| archify | github.com/tt-a1i/archify | Apache-2.0 | 설명 도표(흐름도·타임라인) 생성 | 설치됨(이슈 #9) |
| hallmark · emil-design-eng · web-design-guidelines | nutlope/hallmark · emilkowalski/skills · vercel-labs/agent-skills | MIT · MIT · README만 MIT(예외 승인) | 웹 화면 만들 때(피드백 도구 등) | 설치됨 |
| ai-video-storyboard | 로컬 스킬 | - | AI 영상 클립 샷 리스트(EP002 Seedance 시험 때) | 설치됨 |

## 3. 참고만 하는 것

| 이름 | 출처 | 라이선스 | 어디에 쓰나 |
|---|---|---|---|
| awesome-opus5-5-videos | github.com/yihui-dev/awesome-opus5-5-videos | MIT | 코드로 만든 3D·설명 영상 418편과 프롬프트. 4b 레퍼런스 단계에서 훑어봄 |
| awesome-claude-video-skills | github.com/zhuyansen/awesome-claude-video-skills | 미표기 | 영상 스킬 목록(2026-11-02 조사의 출발점) |
| claude-code-video-toolkit | github.com/digitalsamba/claude-code-video-toolkit | MIT | Remotion 템플릿 부분 차용 후보. 화면 대부분이 유료·AI 영상·스톡 의존 |
| Remotion | github.com/remotion-dev/remotion | 자체 라이선스(4인 이상 유료) | 예외 승인(2026-10-26). Shotcraft가 내부에서 씀 |
| 정부 R&D 발표자료 3곳 | 농림식품기술기획평가원·부처합동설명회·KISTEP | 공공누리(유형 확인 필요) | 한국 관련 편 1차 자료 후보 |
| AI Camera Movements · Cinematique | 인스타 게시물(ai.favmag) | 무료 열람 | 카메라 무빙·영화 기법 참고(AI 영상 생성용은 안 씀) |

## 4. 보류·안 쓰는 것

| 이름 | 출처 | 라이선스 | 이유 | 상태 |
|---|---|---|---|---|
| Voicebox | github.com/jamiepine/voicebox | MIT | 처음 계획한 내레이션 도구. Kokoro로 대체 | 안 씀 |
| 힉스필드(Higgsfield) | higgsfield.ai | 유료 | 무제한 혜택은 자동화에 못 씀(ADR-001 폐기, ADR-002) | 안 씀 |
| Seedance | 힉스필드·Atlas 등 경유 | 유료 | AI 생성 영상. EP002에서 5컷 이내 시험 결정이 있으나 레포 규칙(AI 영상 금지)과 충돌, 결정 필요 | 보류 |
| Nyx Motion | peerpush.com/p/nyx-motion | 유료 | 사용자가 출처 확인 중 | 보류 |
| remotion-dev/skills (공식) | github.com/remotion-dev/skills | LICENSE 없음 | Remotion 본체 예외와 별개, 별도 승인 필요 | 보류 |
| hypit | github.com/hypit-ai/hypit | 자체 라이선스 | Kling·Seedance·Veo AI 영상 의존. 2026-11-02 삭제(백업 `~/archive/2026-11-02-hypit-removed/`) | 안 씀 |
| OpenMontage | github.com/calesthio/OpenMontage | AGPL-3.0 | 라이선스 정책 밖, 핵심이 스톡·음악 API | 안 씀 |
| OpenCut | github.com/OpenCut-app/OpenCut | MIT | 사람이 쓰는 편집기. 새 버전(자동 렌더·MCP) 나오면 재검토 | 보류 |
| pixelfx | github.com/patch-gg/pixelfx | MIT | 게임용 픽셀 이펙트, 채널과 무관 | 안 씀 |
| Ruflo | github.com/ruvnet/ruflo | MIT | 다중 에이전트 하네스. 이 규모엔 과함 | 안 씀 |
| MotionClone | github.com/blixvip/MotionClone | 미표기 | 남의 영상 모션 복제, 비진정성 정책 위험 | 안 씀 |
| shader-skills | (사용자 공유 이미지, 출처 미확인) | 미확인 | 셰이더 효과. 필요해지면 출처 확인 | 보류 |
| platformtree 30개 스킬 목록 | 인스타 게시물 이미지 | - | 2026-10-26 검토. Shotcraft·Clipify만 채택 | 참고만 |

## 관련 보고서

- `~/docs/reports/2026-10-24-yt-skill-stack-skill-list.md` — 첫 스킬 목록
- `~/docs/reports/2026-11-02-yt-skill-stack-video-skills-scan.md` — 영상 스킬 640여 개 조사
- `docs/adr/` — 힉스필드·AI 영상 결정 기록
