# SPEC — EP002 "Is computer science still worth it?" · 스토리라인 C 캠퍼스 지도 비행

GOAL:    부모가 "컴퓨터과학은 망한 전공이 아니라, 첫 직장이 유난히 어려운 고위험·고수익 전공"이라고 이해하고 끝난다.
OUTPUT:  HyperFrames 0.9.19, 1920 x 1080, 30 fps. 2D(SVG 등각 투영), 생성형 이미지·영상 0.
TIME:    전체 270.5 s + 엔드카드 2 s ≈ 272.5 s x 30 = 8,175 frames. 모션 테스트: 0~89 s(2,670 frames). 음악 없음(내레이션이 시계).
DATA:    하나의 데이터 모듈 = NY Fed 전공별 CSV(2024) 73개 전공. 건물 높이 = 신입 실업률(1%p = 44 px). 숫자 표기는 소수 1자리.

LOOK:    매체 = 낮 햇빛의 등각 캠퍼스 모형(블록 건물).
         ground 잔디 #b9d68c(노이즈 3%), 보도 #efe6d2, 건물 윗면 #e7e2d8 · 왼면 #c9c2b6 · 오른면 #aaa397.
         ink #1d2421. accent = CS 건물 #e4572e 하나뿐(윗면 #f0703f, 왼면 #d24e28, 오른면 #b8401e). CE는 accent 테두리 4 px만.
         비교 강조 = 금융·간호 #3f8f5b(첫 기둥 끝 한 번). 기준선(전체 4.2%) = ink 60% 점선 3 px.
         display Archivo Black, 숫자 84~120 px, tabular-nums. 라벨 Inter 700 30 px(최소 28 px), 자간 0.
         그림자: 건물마다 오른쪽 아래로 높이의 0.55배 평행사변형, #1d2421 18%. 비네트·그레인 없음.
OBJECTS: 건물(대지 마름모 + 세 면 + 지붕), 지붕 위 숫자 판, 깃발(SAFE·초록 #3f8f5b), 정문 아치 배너(제목),
         도로(건물에서 캠퍼스 밖 표지판 "ENTRY-LEVEL SOFTWARE JOBS"까지), 표지판(기준 4.2%).
MOTION:  건물 솟기 = power3.out 0.8 s(24 f), 73개 동시 솟기는 대각선 파도 2.4 s(스태거 = (gx+gy)x40 ms).
         카메라 = power2.inOut 1.2~1.8 s, 한 번에 한 이동. 라벨·숫자 = 착지 0.25 s power4.out(크기 0.85→1, 투명 0→1), 착지 후 고정.
         도로 = 그리기 1.0 s power1.inOut. 제목 = 0.35 s 내려앉음 후 고정.
SHOTS:   0.0 전경, 대지만 보임 → 0.3 CS 솟음(7.0) + 라벨 / 8.6 "Learn to code" SAFE 깃발
         11.7 카메라 후퇴 → "major by major" 73개 파도 솟기 → "second-highest" CE #2 → "fourth" CS #4
         24.8 인문 구역으로 이동: 미술사 6.7·철학 5.1·영양 4.5 숫자 판, 각 이름에 맞춰
         34.7 고공 전경 + 정문 배너 제목 "IS COMPUTER SCIENCE STILL WORTH IT?" (40.4까지 정지)
         40.5 공학 구역으로 하강: 전기 3.2·기계 4.4 / 53.6 기준선 4.2 점선 + 표지판
         63.3 과학·경영·보건 구역: 물리 6.6·정보시스템 6.0·수학 5.8·금융 2.8·간호 2.1
         77.2 "Finance and nursing" 두 건물 초록 / "entry-level software jobs" CS·CE에서 캠퍼스 밖 표지판까지 도로 그리기
BANNED:  spec.md 기본 금지 전부 + 어두운 바탕, 글로우, 건물이 계속 흔들리거나 숨 쉬는 움직임, 범례, 숫자 동시 카운트업,
         지도 위 장식용 HUD·코너 라벨, 내레이션 문장을 화면에 그대로 쓰기.
QA:      0.0(첫 프레임 = 썸네일, 검지 않음), 1.5(CS만 솟음), 23(CE #2·CS #4 읽힘), 37(제목 전체 읽힘),
         60(공학 4동 숫자·기준선), 86(도로와 표지판), 출처 띠가 매 프레임 왼쪽 아래.
SOURCE:  화면 출처 "Source: NY Fed, The Labor Market for Recent College Graduates (2024 data)" 22 px, 반투명 띠.
