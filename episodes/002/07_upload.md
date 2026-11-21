# EP002 — 업로드 패키지 (7단계 챕터·설명 + 9단계 업로드 준비)

> **비공개 업로드 2026-11-19, https://youtu.be/u5BlSFFWP2c (Counter Ledger).** 제목·설명(챕터 10·출처 3)·태그 9·영어·교육·아동용 아님·AI 사용 아니요·자막 en/ko 게시, 저작권 검사 문제 없음.
> **남은 것:** 맞춤 썸네일(사용자가 Studio에서 `~/Downloads/EP002_thumb.jpg` 직접 선택 — 브라우저 도구로 넣은 파일은 썸네일 칸이 받지 않음, 3회 실패) → 처리·자막·챕터 확인 → 공개 전환(컨펌 게이트)
> 영상 파일은 브라우저 도구 한도(10MB)를 넘어 사용자가 파일 선택(26.8MB).

- 영상: `output/002/04_exports/EP002_final.mp4` (4:31, 1920x1080 30fps). DRAFT 표시 없는 업로드본(`python3 -I scripts/ep002_full_plan.py final`) + 손그림 훅 13초
- 자막: `episodes/002/subs/en.srt`(영어), `episodes/002/subs/ko.srt`(한국어). 95조각, 시각 동일. `scripts/srt_split.py`로 내레이션 줄을 2줄×42자 이하로 나눔
- 썸네일: `output/002/04_exports/EP002_thumb.jpg` (1280x720, `templates/golden/blocks/thumbnail.html`, 7.0% = 지표 색 오렌지)

## 제목
Is Computer Science Still Worth It? What the Job Data Says

## 설명란 (그대로 붙여 넣기 — 외부 링크 없음)

```
Is computer science still worth it? New York Fed data on recent college graduates puts computer engineering and computer science near the top for unemployment among 73 majors, behind art history and philosophy. But the grads who do get hired are far less likely than most to be underemployed, and they earn some of the highest starting salaries. This video looks at both halves of that table, what a Stanford study says about AI and young software workers, and what the government's 10-year outlook projects.

0:00 Before the next tuition bill
0:11 CS: 4th-highest unemployment of 73 majors
0:40 It's not engineering, and it's not math
1:40 Why software? The Stanford study
2:22 The grads who do get hired
2:40 And the pay
3:04 The 10-year outlook
3:33 Degree vs. no degree
4:00 One chart, one corner
4:11 What the data can and can't say

Sources
- New York Fed, The Labor Market for Recent College Graduates (updated Nov 2026; by-major data from the 2024 American Community Survey)
- U.S. Bureau of Labor Statistics, Occupational Outlook Handbook: Software Developers, Quality Assurance Analysts, and Testers
- Brynjolfsson, Chandar & Chen, "Canaries in the Coal Mine," Stanford Digital Economy Lab (revised Aug 2026)

Narration uses a synthetic (AI) voice. Illustrations and charts are drawn in code from the data. No AI-generated video or images.
Original score. Piano samples: "Salamander Grand Piano V3" by Alexander Holm, CC BY 3.0. Orchestral samples: VS Chamber Orchestra: Community Edition, Versilian Studios (CC0).
```

## 태그
is computer science worth it, is computer science still worth it, computer science unemployment rate, computer science major jobs, computer engineering unemployment, best college majors for jobs, entry level software jobs, ai software jobs, new york fed college graduates

(첫 태그는 EP002 1단계 때 유튜브 자동완성에서 실제로 받은 검색어 "is computer science worth it 2026". 나머지는 대본 핵심어 — 자동완성 확인 전)

## 설정
- 카테고리: Education / 언어: English / 아동용 아님
- 변경·합성 콘텐츠 표시: 해당 없음(실존 인물·실제 사건을 사실처럼 꾸민 장면 없음). 설명란에 합성 음성 사용을 밝힘
- 자막: en.srt(English), ko.srt(Korean) 업로드
- 공개 범위: 먼저 비공개로 올려 처리·자막·챕터 확인 → 공개 전환(되돌릴 수 있음)
- 설명란 외부 링크 없음(채널 인증 전 링크 막힘, CLAUDE.md). CC BY 표기는 저작물명·저작자·라이선스명으로 하고, 라이선스 주소는 영상 끝 화면 출처 문구에 있음

## 업로드 직전 컨펌 게이트 (CLAUDE.md)
- 무엇을: 위 영상 + 제목·설명·태그·썸네일 1장·자막 2개
- 어디로: YouTube @Counter_Ledger
- 되돌릴 수 있나: 비공개 단계에선 완전 되돌림. 공개 후엔 비공개 전환·삭제 가능하나 조회·노출 기록은 남음

> **숏폼 3편 공개 2026-11-21** (1편 9OclCzEUJl4, 2편 mrg0VAfyH6I, 3편 IROeW_zq3H8). "관련 동영상" 연결은 스튜디오가 '이미 이용 가능, 새로고침' 안내만 반복해 못 함(채널 인증 필요 추정, 미확인)
> **롱폼 결정(2026-11-21 사용자): 공개본 u5BlSFFWP2c 유지, 교체본 업로드·삭제 취소.** EP002_final2.mp4(썸네일 장면판)는 보관만
> **숏폼 3편 비공개 업로드 2026-11-21** (Counter Ledger Shorts 탭, 1편 youtube.com/shorts/9OclCzEUJl4). 영어·교육·아동용 아님·AI 아니요·태그 4. 남은 것: 각 숏 "관련 동영상"에 롱폼 연결 → 공개 전환(컨펌 게이트)
> **주의(2026-11-21 확인):** 롱폼 u5BlSFFWP2c가 이미 '공개' 상태(11/19 게시, 조회 0). Claude가 바꾸지 않음. 교체본 업로드·기존본 삭제는 보류하고 사용자 결정 대기

## 숏폼 3개 (2026-11-19, `python3 -I scripts/shorts.py 002 output/002/04_exports/EP002_final2.mp4`)

설명란 공통 끝부분(외부 링크 없음):
```
Full video on this channel: "Is Computer Science Still Worth It? What the Job Data Says"
Sources: New York Fed, The Labor Market for Recent College Graduates (2024 by-major data); U.S. Bureau of Labor Statistics, Occupational Outlook Handbook; Stanford Digital Economy Lab, "Canaries in the Coal Mine" (Aug 2026).
Narration uses a synthetic (AI) voice. No AI-generated video or images. Piano samples: "Salamander Grand Piano V3" by Alexander Holm, CC BY 3.0.
```

| 파일 | 길이 | 제목 | 설명 첫 줄 |
|---|---|---|---|
| `EP002_short_1.mp4` | 36초 | Is Computer Science Still Worth It? Part 1/3: CS Grads Are More Jobless Than Art History Grads | Is computer science still worth it? Part 1 of 3. New York Fed data: recent CS grads are unemployed at 7.0%, higher than art history (6.7%) and philosophy (5.1%). |
| `EP002_short_2.mp4` | 36초 | Is Computer Science Still Worth It? Part 2/3: The Ones Who Get Hired Start at $87,000 | Is computer science still worth it? Part 2 of 3. Only 19% of employed CS grads are underemployed (39% across all majors), and they start around $87,000 (all majors: $58,000). |
| `EP002_short_3.mp4` | 16초 | Is Computer Science Still Worth It? Part 3/3: Software Jobs +10% Projected, First Jobs Harder | Is computer science still worth it? Part 3 of 3. BLS projects software jobs to grow 10% over the next decade. The first job is harder to land right now. |

- 롱폼 연결: 업로드 후 각 숏 "관련 동영상"에 롱폼 지정(스튜디오 설정, 외부 링크 아님)
- 썸네일: 숏 첫 화면이 제목 칸이라 그대로 표지가 됨
- 시리즈(2026-11-19 사용자 숏츠 가이드): 이어 볼 순서 1→2→3, 마지막 89프레임은 다음 편 예고, 제목·설명 첫 줄은 검색어 "Is computer science still worth it"로 시작. '내 경험 훅'은 얼굴 없는 채널이라 지어내지 않고 부모에게 묻는 2인칭 질문으로 대신
- 첫 3초 = 답(2026-11-20 스레드 가이드 검토 후 사용자 승인): 제목은 구체적 답, 1편은 미술사 6.7% 카드 1.83초 콜드 오픈(음악만), 2·3편은 군더더기 첫 문장 삭제

## 롱폼 교체본 (영상 안 썸네일 구간)
- `EP002_final2.mp4`: 0:34~0:40 제목 장면이 썸네일과 같은 구성(제목 + 7.0%). 맞춤 썸네일 대신 스튜디오 "동영상에서 선택"으로 이 구간을 고른다(채널 전화 인증 불가, 2026-11-19 사용자)
- 유튜브는 올린 영상 파일을 바꿀 수 없어 새로 올리고, 기존 비공개본(u5BlSFFWP2c, 조회 0)을 지워야 한다
