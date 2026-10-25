# EP001 — 3단계 대본 v2 (게이트 2)

- 이슈 #2 · 기준: `docs/voice.md`, `02_research.md`에 있는 숫자·인용만 사용
- v2 변경: 영어 AI 티 검토(critic) 반영. 대구·한 줄 펀치 제거, 결론을 연구자 확신 수준으로 낮춤, 숫자 한 문장 2개 이하, 용어를 구어로.
- 분량: 1,328단어, 약 8.9분 (절별 구간은 파일 끝)
- 화면 표기: `[CHART]` 차트, `[ARTICLE]` 원문 캡처 무빙+형광펜, `[CUTOUT]` 2D 컷아웃, `[STOCK]` 스톡, `[TEXT]` 큰 글자, `[EST]` 화면에 "Estimate" 표시

## 훅 (hookscore.py v2)

| 순위 | 훅 | 점수 |
|---|---|---|
| 1 | You've been told AI is why new grads can't get hired. A New York Fed study found the trouble started before ChatGPT existed. | 59 WORKABLE (약점: 손해를 말하지 않음. 근거 없는 위협 대신 이걸 택함) |
| 2 | You've been told AI is why new grads can't get hired. The New York Fed checked, and the damage started before ChatGPT existed. | 59 WORKABLE |

## 제목 드롭 문구
**THE FIRST PROBLEM WASN'T AI**

---

## 1. Hook

You've been told AI is why new grads can't get hired. A New York Fed study found the trouble started before ChatGPT existed.

`[CUTOUT] graduate in cap and gown, rejection emails stacking up` → `[TEXT] "AI took the entry-level jobs"` → `[ARTICLE] Liberty Street Economics headline, June 1, 2026`

## 2. The turn

The common version goes like this. Companies adopted ChatGPT, junior work got automated, and the first rung of the career ladder disappeared. CNBC and the Financial Times each made a video along those lines, and each has been watched more than a million times.

`[STOCK] empty office desks` `[CUTOUT] ladder with the bottom rung missing`

Young graduates are struggling. That part is true. The question is why, because the answer changes what a graduate should do about it.

In June 2026, three economists published a study on the New York Fed's research blog. Instead of asking whether AI could replace junior workers, they asked when the problem started, and in which kinds of jobs.

`[ARTICLE] author line: Emanuel, Harrington, Pallais`

Their answer points at something that happened before most companies had touched AI. A second study, from Stanford, then adds a newer problem on top. This video walks through both.

`[TEXT] THE FIRST PROBLEM WASN'T AI` (title drop)

## 3. The gap is real

Start with the gap itself.

The New York Fed tracks recent college graduates, meaning people aged 22 to 27. In the second quarter of 2026, their unemployment rate was about 5.6 percent. Separately, 42 percent of recent grads were underemployed, which means working a job that doesn't need a degree.

`[CHART] two big numbers: 5.6% unemployed / 42% underemployed, source tag NY Fed Q2 2026`

The comparison with older graduates is what makes this interesting. In the years just before the pandemic, roughly 3 in every 100 graduates under 29 were unemployed. In the years after, it was closer to 4 in 100. A 20 percent rise.

`[CHART] under-29 grads: 3.1% (2017–19) → 3.7% (2022–25)`

Over the same years, graduates aged 29 and up went the other way. Their unemployment rate edged down, from 1.9 percent to 1.8.

`[CHART] add second bar pair: 29+ grads 1.9% → 1.8%`

A weak economy would have hurt every graduate. This didn't. It hit the youngest ones, and left people a few years older untouched. On its own, that pattern fits the AI explanation. Juniors get replaced, seniors stay. So the researchers looked closer.

## 4. Timing and job type

They sorted jobs into two groups. Jobs you can do from home, like software engineering. And jobs where you have to show up, like mechanical engineering. The study uses a published index of how remotable each occupation is.

`[CUTOUT] split screen: laptop at kitchen table vs. engineer at a machine` `[TEXT] remotable / non-remotable`

Then they compared young and older workers inside each group.

In the from-home jobs, unemployment for young graduates rose by almost a full percentage point between the pre-pandemic years and 2022 to 2024. Older workers in those same jobs saw a slight decline.

`[CHART] remotable jobs: young line rising ~1 point, older line flat-to-down`

In the show-up jobs, the gap between young and old widened briefly in 2020, then went back to where it had been.

`[CHART] non-remotable jobs: small bump in 2020, back to baseline`

So the gap opened in the jobs that went remote, and it didn't open in the jobs that stayed in person. Remote work itself, by the study's count, has grown about four-fold since the pandemic.

The timing matters as well. The study's comparison window is the pre-pandemic years against 2022 to 2024. The authors note that the rise in young graduate unemployment began before generative AI was in wide use. ChatGPT launched in November 2022.

`[CHART] timeline: 2017–19 baseline · 2020 remote shift · Nov 2022 ChatGPT · 2022–24 comparison window`

## 5. Why distance hurts juniors

Why would working from home hurt new hires more than anyone else?

The researchers had internal data from one Fortune 500 company. When employees sat near each other, they exchanged more feedback and more mentoring. Even a short physical distance reduced that, and it reduced it more for younger workers.

`[CUTOUT] two desks close together with speech bubbles; then the desks slide apart and the bubbles shrink`

A junior job is partly work and partly training. The training tends to happen in small moments, like a senior colleague glancing at your screen or fixing your draft in a few minutes. Take away the shared room and the company is still paying for the work, but the training has become harder to deliver.

That company's response followed the incentive. When its offices closed, it hired fewer inexperienced workers. For teams that stayed distributed, it continued to favor experienced hires even after the offices reopened. In the authors' words, a firm "shies away from employing inexperienced workers if distance creates barriers to training and development."

`[ARTICLE] quote highlight`

Two cautions before going further. The inside view comes from a single company, so it can't stand in for the whole economy. And the authors' wording is careful: they say remote work "can explain" the rise and "has meaningfully contributed" to it. The national numbers and the company data point the same direction, but that is still an argument, not a closed case.

`[TEXT] Evidence: 1 company · wording: "can explain"`

## 6. The 64 percent

How much of the problem does remote work account for?

The researchers ran what they call a back-of-the-envelope calculation. Their estimate: remote work can explain about 64 percent of the recent increase in unemployment among young college graduates. Treat it as a rough size, not a measurement.

`[CHART] donut, 64% filled` `[EST]`

They also tested the obvious objection. Maybe the from-home jobs are simply the same jobs AI is good at. So they held each occupation's AI exposure fixed and ran the comparison again. The gap between young and older workers was still there, in both groups of jobs.

`[TEXT] AI exposure held constant → gap persists`

That is the first problem. It shows up in the jobs that went remote, and on the New York Fed's estimate it accounts for a large share of the rise through 2024.

It isn't the whole picture, because a second study looks at the same years and finds something else.

## 7. The second problem

In August 2026, Erik Brynjolfsson and two colleagues at Stanford updated a study based on payroll records from ADP. They focused on workers aged 22 to 25 in the occupations most exposed to AI.

`[ARTICLE] Stanford Digital Economy Lab, Aug 12, 2026`

By June 2026, employment for those young workers was about 19 percent below where it would have been if it had kept pace with young workers in less exposed jobs. A year earlier, the same gap was 15 percent. It has been widening.

`[CHART] gap line: 15% (July 2025 data) → 19% (June 2026 data)`

Two details connect this to the Fed study. The gap holds up when the authors control for interest rates and for remote work. And experienced workers in the same occupations show no comparable gap.

A separate working paper from the U.S. Census Bureau found a related pattern. In the industries most exposed to AI, employment of workers aged 22 to 24 fell 12 percent over the ten quarters after ChatGPT's release. In less exposed industries it held steady. That paper also estimates that up to a quarter of the decline may trace back to interest rate increases, which leaves most of it unexplained by rates.

`[CHART] Census: most-exposed industries −12%, others flat` `[TEXT] up to 1/4: interest rates`

The Stanford gap also has a shape. The declines are concentrated in occupations where AI tends to do the task instead of the person. Where AI is mainly used to help workers, young employment is flat or rising.

`[CUTOUT] two jobs side by side: one where a robot hand does the task, one where it hands a tool to the person`

The Stanford authors attach their own cautions. They describe these as descriptive patterns, not causal estimates. Some of the differences appear before generative AI was widely used. The gap shrinks when education is taken into account. And their payroll sample shows larger gaps than national surveys do, mostly in education, health care, and public administration.

`[TEXT] "descriptive patterns, not causal estimates"`

## 8. Putting the two together

`[CHART] one timeline with two shaded bands. Band 1: New York Fed, remote work, comparison window 2017–19 vs 2022–24. Band 2: Stanford, AI-exposed occupations, Nov 2022 to Jun 2026. The bands overlap from late 2022 on.`

The two studies cover overlapping years, so this isn't a clean handoff from one cause to the next. They ask different questions.

The New York Fed study finds the early gap in jobs that went remote, and finds that AI exposure doesn't explain it. The Stanford study finds a newer and growing gap in jobs where AI does the task, and finds that remote work doesn't explain that one. The simplest reading is that two causes are stacking, and the data can't yet say how much weight each carries.

That still leaves a graduate with two questions worth asking about any job. Will this role put me near people who can teach me? And is AI in this job doing the work, or helping someone do it? These aren't career advice from us. They are the two lines the studies happen to draw.

## 9. Close

Most of the conversation about young workers and AI is about what comes next. The numbers suggest the trouble began earlier, when offices emptied out and companies stopped training people they couldn't see.

`[CUTOUT] graduate looking at two paths on the horizon` → `[TEXT] Which of the two questions applies to your search?` → end card (channel name only)

So, looking at your own job search: which of those two questions applies to you?

---

## 화면 출처 메모
- 숫자와 인용은 전부 `02_research.md`의 1·2·4·5·6·7·8·9·10·11·12·14번과 16~24번(v2에서 추가한 1차 확인 사실).
- 기사 캡처는 원문 페이지(뉴욕 연준·스탠퍼드·인구조사국). 뉴스 방송 클립은 쓰지 않는다.

## 분량·타임스탬프 (자동 계산, 150wpm)

| 절 | 제목 | 단어 | 구간 |
|---|---|---:|---|
| 1 | Hook | 23 | 0:00–0:09 |
| 2 | The turn | 135 | 0:00–0:54 |
| 3 | The gap is real | 157 | 0:54–1:56 |
| 4 | Timing and job type | 178 | 1:56–3:08 |
| 5 | Why distance hurts juniors | 219 | 3:08–4:35 |
| 6 | The 64 percent | 144 | 4:35–5:33 |
| 7 | The second problem | 275 | 5:33–7:23 |
| 8 | Putting the two together | 143 | 7:23–8:20 |
| 9 | Close | 54 | 8:20–8:41 |

합계 1,328단어, 약 8.9분.
