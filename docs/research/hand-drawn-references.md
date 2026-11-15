# 손그림 레퍼런스 — 코드로 그린 잉크·수채가 손그림으로 읽히는 규칙 (2026-11-16)

계기: EP002 훅 시안(식탁 위 등록금 고지서)이 "손그림 느낌이 적다"(사용자). 원칙만 뽑았고 작품은 복제하지 않는다. 도구는 anidoodle(Apache-2.0), 그림체 견본은 Ink & line-wash(`wren`).

## 레퍼런스 (원문 확인한 것)

| 작가·자료 | 무엇 | 가져온 원칙 |
|---|---|---|
| Liz Steel, 찻잔 스케치 엣지 https://www.lizsteel.com/thinking-about-edges-while-sketching-a-teacup/ | 탁자 위 사물 잉크+수채 | 면이 바뀌는 곳은 잉크, 색이 바뀌는 곳은 물감. 받침·잔 윤곽 일부는 일부러 안 그림 |
| Danny Gregory, "The Art of Breakfast" https://dannygregorysblog.com/2011/07/25/the-art-of-breakfast | 아침 식탁 딥펜+수채 | 딥펜은 "the most human line" — 필압이 불규칙하고 잉크가 마르며 끊김 |
| Quentin Blake, "How I draw" https://quentinblake.com/about-drawing/how-i-draw | 러프 위에 처음 그리듯 | 정확한 형상은 밑에 두고 흐릿하게 따라 한 번에 긋는다 |
| Christoph Niemann, Sunday Sketching https://www.itsnicethat.com/articles/christoph-niemann-sunday-sketching-261016 | 실물+붓·잉크 | "There is no editing" — 같은 경로를 두 번 긋지 않음 |
| Sempé (Liza Donnelly 관람기) https://lizadonnelly.substack.com/p/the-hand-of-the-artist | 가는 펜선+연한 수채 | 흰 종이를 크게 남김 |
| Tom Gauld https://creativelivesinprogress.com/article/tom-gauld | 균일한 선 카툰 | 해칭 간격·각도가 흔들리면 균일한 선도 손맛 |
| RSA Animate https://linesandcolors.com/2010/08/27/rsa-animate-cognitive-media/ | 손그림 해설 영상 | 영상은 페이드인이 아니라 획 순서대로 그려지게 |
| Curtis 외, "Computer-Generated Watercolor"(SIGGRAPH 1997) https://grail.cs.washington.edu/projects/watercolor/ | 수채 효과 정의 | 드라이브러시·가장자리 어두워짐·백런·그래뉼레이션·번짐·글레이징 |

## 규칙 8개 (중요도 순) — EP002 훅 v3 적용 여부

1. 물감은 선 도형과 따로: 한쪽은 넘치고 반대쪽은 못 미쳐 흰 틈 — ✅ (`wet` dx/dy/shrink)
2. 물감 가장자리 짙게, 안은 불균일, 아래에 고임, 백런 — ✅
3. 선은 형상을 흐릿하게 따라 한 번에, 모서리 넘침, 긴 선은 끊김 — ✅
4. 한 획 안에서 굵기 변화(누른 곳 굵게, 뗀 곳 가늘게) — ✅ (pressure 1.75)
5. 빛 쪽 윤곽은 열고 그늘 쪽은 선+해칭 — ✅
6. 화면 안 글자는 전부 손글씨(글꼴 없음) — ✅ (`drafting.ts` 펜 획 대문자). 화면 속 코드는 읽을 한 줄만, 나머지는 손으로 그은 선
7. 흰 종이 크게, 강조색은 한 곳 — ✅ (오렌지는 고지서 AMOUNT DUE만)
8. 원근 미세하게 비뚤게, 연필 밑그림 선 남김 — ✅

영상으로 만들 때: 완성 그림을 페이드인하지 않고 획 순서대로(anidoodle `progress`, drafting `letter` progress) 그린다.
