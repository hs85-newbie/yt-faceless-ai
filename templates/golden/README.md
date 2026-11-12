# 황금비·피보나치 템플릿

규칙은 `brand/GOLDEN.md`, 색 값은 `brand/golden.css`에 있다. **색은 바뀔 수 있고 규칙은 지킨다.** 이 폴더의 틀은 색 값을 직접 쓰지 않고 역할 이름(`--g-main`·`--g-second`·`--g-loud`·`--g-bad`·`--g-good`…)만 쓴다. 그래서 팔레트를 바꿀 때는 `golden.css` 값만 바꾸면 된다.

## 새 편에 쓰는 순서

1. 5단계(음성)가 끝나 `lines.json`과 `transcript.srt`가 생긴 뒤, `episodes/NNN/golden.json`을 만든다. EP002 것(`episodes/002/golden.json`)을 복사해서 고친다.
   - `voice`·`work`: 내레이션 폴더(`lines.json`이 있는 곳)와 작업 폴더(`transcript.srt`·`voice.wav`가 있는 곳)
   - `title`·`title_card`·`kicker`·`tag`·`episode_tag`·`doc_title`: 화면 글자(영어)
   - `number`·`number_metric`(`bad`|`good`)·`number_caption`·`card_label`·`card_desc`: 핵심 숫자. `02_research.md`에 출처가 있는 것만
   - `sections`: 절 이름과 그 절의 첫 줄 id
   - `climax`: 클라이맥스 대사의 줄 id(0.618T 근처에 와야 한다)
2. 실행한다.
   ```
   python3 -I scripts/golden.py NNN
   ```
3. 결과를 본다.
   - `episodes/NNN/GOLDEN_PLAN.md`: 전체 길이 T, 0.382T·0.618T와 그 시각에 걸리는 대사, 클라이맥스 줄이 0.618T에서 몇 초 떨어졌는지, 절별 T 비율
   - `output/NNN/03_work/golden/`: 블록 샘플. `npx hyperframes snapshot --at 0.5,1.5,2.5,3.5,4.5`로 정지 화면을 뽑는다

클라이맥스가 0.618T에서 13초 넘게 떨어지면 대본 구성이나 화면 배치를 다시 본다(GOLDEN.md §5-1).

## 블록 (`blocks/`)

| 파일 | 무엇 | 칸 |
|---|---|---|
| `thumbnail.html` | 1187 : 733 분할 썸네일, 숫자 233px | title · kicker · number · number_color · caption |
| `title-card.html` | 콜라주 제목 카드(찢긴 문서·망점·기울인 이름표) | doc_title · episode_tag · title · title_size · tag |
| `number-card.html` | 장면 위에 겹치는 숫자 카드(여백 89 자리) | number · number_color · label · desc |
| `rules-grid.html` | 황금선·황금점·나선·글자 단계·색 면적 안내판 | squares · path |
| `time-plan.html` | 실제 대사 시각 위의 0.382T·0.618T 설계도 | ep · T · bars · marks · climax · legend · fib |

- 칸은 `{{이름}}`으로 비워 두고 `scripts/golden_kit.py`의 `fill()`이 채운다. 빈 칸이 남으면 바로 실패한다.
- 제목 글자 크기는 `fit_size()`가 피보나치 단계(144 → 89 → 55)에서 가장 긴 줄이 들어가는 크기로 고른다.
- 숫자 색은 지표를 따른다. 실업·위험처럼 나쁜 숫자는 `bad`, 초봉처럼 좋은 숫자는 `good`.

## 공용 함수 (`scripts/golden_kit.py`)

`tokens()`(golden.css 읽기) · `fill()` · `fit_size()` · `line_starts()`(대사 시각) · `time_plan()` · `spiral()`. 자기 점검은 `python3 -I scripts/golden_kit.py`.
3D 장면(`scripts/ep002_proto.py golden`)도 색을 `tokens()`에서 읽는다.
