# EP001 v3 — 제작 노트 (motionmaxxing 점검 기록)

- 결과물: `output/001/long_v3.mp4` (1920×1080, 24fps, 489.75초 = 8분 9.8초, −14.2 LUFS, true peak −1.1 dBFS). git 제외.
- 재현: `output/001/voice_v3/pauses.json` = `{"s2_04": 2.5}`(제목 드롭 쉼)을 만든 뒤 assemble_voice → build_film_v3 → video.mjs → make_audio_v3 → mux.sh.
- 원본: 이 폴더(`index.html`·`film.js`·`scenes3d.js`·`lib3d.js`·`cuesheet.json`), 빌드 `scripts/build_film_v3.py`, 믹스 `scripts/make_audio_v3.py`.

## 하나의 생각
"첫 번째 파도는 AI가 아니었다"를 숫자가 놓인 매트 위에서 직접 보여 준다. 뼈대는 3D 데이터 무대(PolyMatter식), 질감은 종이 콜라주, 글자는 떨어지는 종이 띠.

## 무엇이 진짜이고 무엇이 그림인가
| 종류 | 내용 |
|---|---|
| 진짜 캡처 | 뉴욕 연준 Liberty Street(제목·저자·64%·Fortune 500·인용·can explain), 스탠퍼드 DEL(저자·금리·descriptive), 인구조사국 CES-WP-26-27(초록·통화정책) |
| 숫자 | 전부 `02_research.md` 출처. 64%는 화면에 ESTIMATE |
| 도식(값 없음) | 원격 가능 직종 화살표(약 +1%p, 경력자 소폭 하락), 대면 직종 2020 혹(높이에 값 의미 없음) |
| 생성 이미지 | Gemini 콜라주 배경 5장(sb1·sb2·sb3·sb5·sb6, 이전 세션 생성분 재사용), v1 컷아웃 4장(사진 인화 형태). 사람·로고·UI로 오인될 요소 없음 |

## 게이트 (스크립트 수치)
| 게이트 | 결과 | 근거 |
|---|---|---|
| G0 렌더 | PASS | 489.75초, 기대 489.70초, 오디오 있음 (look.py) |
| G2 빈 화면 | PASS | 3프레임 넘는 평평한 구간 없음 (look.py) |
| G3 엔드카드 | PASS | 마지막 고정 1.21초, 마지막 샷 5.33초 = 1% (look.py) |
| G5 화면 장식 | PASS | 구석 채널명 제거 후 (lint.mjs) |
| G1 근거 판독 | 눈으로 확인 | 원문 캡처는 표시 상자 주변을 잘라 1300px 폭까지 확대, 형광펜 |
| G4 한 화면 한 주인공 | 눈으로 확인 | 3D·문서·콜라주 컷은 통과. 글자 카드 일부는 빈 바탕에 띠 1~2개라 약함 |

- 움직임 지표(프레임 간 평균 밝기 변화): 1.6/255. look.py의 사람 기준 띠(4.4~9.8)는 짧은 홍보 영상 기준이라, 같은 도구로 레퍼런스 30초 구간을 재서 비교했다: PolyMatter 0.8, How Money Works 1.9, LITTLE BIT BETTER 2.8, Antidote 3.1.
- 컷 수 62(감지 81), 평균 샷 6.05초, 전환 6종(cut·drop·punch·rip·whip·wipe), 다양성 규칙 통과(build_film_v3.py).
- 로컬 ffmpeg에 drawtext가 없어 look.py는 시각 표기 없이 시트를 만들었다(임시 사본에서 끔, 원본 스킬 파일은 그대로).

## 남은 약점 (사용자 판단 필요)
- 글자 카드 26개 중 빈 바탕 위 띠 1~2개짜리가 슬라이드처럼 보일 수 있다. 개선안: 관련 콜라주·3D 위에 띠를 얹기.
- 스탠퍼드 3D 장면은 카메라가 느려 9.8초간 거의 정지(정지 판정 기준 0.35/255).
- 구석 채널명 제거는 앞서 정한 "채널 서명"의 일부를 바꾼 것. 대신 유튜브 스튜디오 브랜딩 워터마크를 권장.
