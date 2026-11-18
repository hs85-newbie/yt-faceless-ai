import { Gfx, PENCIL, line, oval, rng, tube, turn, type Ctx, type Env, type P } from "./core";
import { Film } from "./film";
import { blob, clamp, fillShape, smooth } from "./gallery";
import { C, INK, INK_M, PAPER, corners, flood, hatch, over, pen, sheet, wet } from "./inkwash";
import { letter } from "./drafting";

// EP002 훅 v3 — Ink & line-wash(wren 방식). 위에서 본 부엌 식탁: 등록금 고지서(초점) · 'learn to code' 노트북 · 커피잔 · 연필.
// 손그림으로 읽히게: 물감이 선 밖으로 번지고 아래에 고이며 백런, 흰 종이는 칠하지 않고 남김, 펜은 모서리를 넘치고
// 빛 받는 쪽은 열어 두며 그늘 쪽만 눌러 그음, 연필 밑그림 선이 남음, 그림자는 해칭, 잉크 튐, 글자는 손으로 옮겨 적은 듯 흔들림.
// 색: brand/golden.css 팔레트 A 역할(크림 종이 · 네이비 잉크 · 오렌지 한 곳). 고지서에 금액 없음(출처 없는 숫자 금지). 빛은 왼쪽 위.
// 같은 그림을 두 번 쓴다: tuition = 완성 정지 화면, tuitionhook = 내레이션 단어에 맞춰 획 순서대로 그려지는 11.7초 영상.
// WHY: 페이드인이 아니라 획 순서대로(RSA Animate 원칙, docs/research/hand-drawn-references.md). 정지 화면은 모든 진행도가 1이라 v3와 같다.
const BILL_C: P = [820, 540], BILL_A = -6;
const FPS = 30, HOOK_S = 13;   // GOLDEN §5-1 "훅은 첫 13초"(피보나치 초). 13초에 3D 캠퍼스로 넘어간다
// 손글씨 크기: cap(대문자 높이) = 글자 크기 × 0.7(Inter 대문자 높이 비율). GOLDEN §3 글자 크기 34 → cap 24, 55 → cap 38
const CAP34 = 24, CAP55 = 38;
// GOLDEN §4: 움직임 길이는 피보나치 프레임. 시작 시각은 내레이션 단어에 맞추고, 길이만 가장 가까운 피보나치 프레임으로
const FIB = [8, 13, 21, 34, 55, 89];
const snap = (sec: number) => FIB.reduce((p, c) => (Math.abs(c - sec * FPS) < Math.abs(p - sec * FPS) ? c : p)) / FPS;

const rot = (pts: P[]) => turn(pts, BILL_C[0], BILL_C[1], BILL_A);

const BILL = rot(corners(820, 540, 520, 690));
const SCREEN: P[] = [[1270, 214], [1800, 232], [1792, 556], [1264, 546]];
const BASE: P[] = [[1238, 562], [1818, 574], [1872, 756], [1186, 742]];

// 획 순서표(초). 내레이션 단어 시각(voice_v2): tuition 0.77 · computer science 1.81 · first job 6.07 · s1_02 7.13 · learn to code 8.88 · never 10.01
const make = (anim: boolean) => (ctx: Ctx, frame: number, env: Env) => {
  const t = anim ? frame / FPS : Infinity;
  const at = (a: number, b: number) => (t === Infinity ? 1 : clamp((t - a) / snap(b - a)));
  const g = new Gfx(ctx, env, 0, INK_M);
  ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0);
  ctx.fillStyle = PAPER; ctx.fillRect(0, 0, env.W, env.H);
  const fit = env.W / 1920;
  const fl = (pts: P[], a: number, b: number, seed: number, fn: () => void) => flood(ctx, env, fit, pts, at(a, b), seed, fn);
  g.push(0, 0, fit);

  // 0. 연필 밑그림: 원근 안내선과 고지서 자리 — 지우지 않고 남겨 둔다
  const sketch = new Gfx(ctx, env, 0, PENCIL);
  sketch.push(0, 0, fit);
  sketch.group("ink", () => {
    sketch.pen(line([120, 960], [1860, 880], 2), { seed: 2, w: 0.7, opacity: 0.22, boil: 0, retrace: false, progress: at(0, 0.6) });
    sketch.pen(rot(corners(826, 546, 540, 706)), { seed: 3, closed: true, w: 0.6, opacity: 0.2, boil: 0, progress: at(0.15, 0.8) });
    sketch.pen(oval(334, 334, 128, 124, 14), { seed: 4, closed: true, w: 0.6, opacity: 0.2, boil: 0, progress: at(0.4, 0.9) });
  });
  sketch.pop();

  // 1. 물감 — 바탕 한 번(가장자리는 종이로 남김), 그다음 그림자, 물체(흰 고지서는 칠하지 않음). 각 물감은 제 시각에 번져 나온다
  const TABLE = smooth([[90, 120], [1840, 90], [1880, 980], [70, 1010]], true, 8);
  fl(TABLE, 0.3, 1.5, 1, () => wet(g, TABLE, C.wood, { alpha: 0.32, seed: 1, pool: 0.4, bloom: [1500, 900], bloomR: 60 }));
  const BILL_SH = sheet(rot(corners(846, 568, 520, 690)));
  fl(BILL_SH, 0.6, 1.2, 2, () => wet(g, BILL_SH, C.shadow, { alpha: 0.32, seed: 2, pool: 0.5 }));
  const MUG_SH = blob(356, 360, 124, 118, 3, 0.08, 20);
  fl(MUG_SH, 3.6, 4.1, 3, () => wet(g, MUG_SH, C.shadow, { alpha: 0.28, seed: 3 }));
  const LAP_SH = sheet([[1212, 592], [1856, 604], [1904, 792], [1204, 780]]);
  fl(LAP_SH, 7.1, 7.6, 4, () => wet(g, LAP_SH, C.shadow, { alpha: 0.26, seed: 4 }));
  if (at(0.6, 0.61) > 0) g.group("plain", () => fillShape(g, sheet(BILL), PAPER, 1));   // 종이는 아래를 가린다: 고지서 자리는 종이색으로 덮고 칠하지 않음
  const HEAD = sheet(rot(corners(820, 262, 470, 74)));
  fl(HEAD, 2.5, 3.0, 6, () => wet(g, HEAD, C.navy, { alpha: 0.82, seed: 6, pool: 0.6, shrink: 0.95, dx: -6, dy: 2 }));   // 선에 못 미쳐 흰 틈
  const DUE = sheet(rot(corners(830, 742, 400, 88)));
  fl(DUE, 5.5, 6.1, 7, () => wet(g, DUE, C.loud, { alpha: 0.6, seed: 7, pool: 0.7, bloom: [960, 736], bloomR: 18, shrink: 0.94, dx: 8, dy: -3 }));
  const SCR = sheet(SCREEN);
  fl(SCR, 7.15, 7.85, 9, () => wet(g, SCR, C.navy, { alpha: 0.9, seed: 9, pool: 0.5, bloom: [1700, 470], bloomR: 34 }));
  const KB = sheet(BASE);
  fl(KB, 7.4, 8.0, 8, () => wet(g, KB, C.grey, { alpha: 0.42, seed: 8, pool: 0.6 }));
  const MUG = blob(330, 330, 118, 116, 10, 0.04, 22), COF = blob(330, 330, 90, 88, 11, 0.05, 20);
  fl(MUG, 3.8, 4.4, 10, () => wet(g, MUG, C.mug, { alpha: 0.6, seed: 10, pool: 0.5 }));
  fl(COF, 4.1, 4.7, 11, () => wet(g, COF, C.coffee, { alpha: 0.88, seed: 11, pool: 0.9, bloom: [300, 300], bloomR: 22 }));
  const PEN_T = tube([[548, 908], [782, 818]], 10, 9);
  fl(PEN_T, 6.6, 7.0, 13, () => wet(g, PEN_T, C.pencil, { alpha: 0.75, seed: 13, pool: 0.6 }));

  // 2. 펜 — 초점(고지서)부터. 빛 받는 위·왼쪽 변은 끊어 두고, 그늘 쪽 오른쪽·아래 변은 눌러서
  g.group("plain", () => {
    const [a, b, c, d] = BILL;
    pen(g, over(a, [a[0] + (b[0] - a[0]) * 0.55, a[1] + (b[1] - a[1]) * 0.55]), 1.2, 21, 0.75, 0.9, at(2.0, 2.25));   // 윗변 앞 절반만
    pen(g, over([a[0] + (b[0] - a[0]) * 0.7, a[1] + (b[1] - a[1]) * 0.7], b), 1.1, 22, 0.7, 0.9, at(2.25, 2.4));
    const m1: P = [b[0] + (c[0] - b[0]) * 0.46, b[1] + (c[1] - b[1]) * 0.46], m2: P = [b[0] + (c[0] - b[0]) * 0.52, b[1] + (c[1] - b[1]) * 0.52];
    pen(g, over(b, m1, 0.02), 2.4, 23, 0.92, 0.9, at(2.4, 2.6)); pen(g, over(m2, c, 0.03), 2.4, 26, 0.92, 0.9, at(2.6, 2.8)); pen(g, over(c, d), 2.6, 24, 0.92, 0.9, at(2.8, 3.05));   // 긴 변은 한 번 끊김, 그늘 쪽은 굵게
    pen(g, over(d, [d[0] + (a[0] - d[0]) * 0.6, d[1] + (a[1] - d[1]) * 0.6]), 1.4, 25, 0.8, 0.9, at(3.05, 3.25));   // 왼변은 아래만
    for (let i = 0; i < 6; i++) {   // 본문 줄: 글자 대신 손으로 그은 줄
      const y = 487 + i * 34, x2 = i % 2 ? 960 : 1040;   // 줄 간격 34(피보나치), 글자가 커진 만큼 아래로
      pen(g, rot(line([600, y], [x2, y], (i % 3) - 1)), 0.9, 30 + i, 0.5, 0.6, at(4.1 + i * 0.12, 4.22 + i * 0.12));
    }
    hatch(g, 1060, 300, 1110, 900, 22, 200, at(4.85, 5.5));                                    // 고지서 그림자 해칭
    // 잔: 위쪽 테는 열고 아래쪽만 눌러서, 손잡이
    const rim = smooth(blob(330, 330, 118, 116, 10, 0.04, 22), true, 4);
    pen(g, rim.slice(Math.floor(rim.length * 0.15), Math.floor(rim.length * 0.75)), 2.2, 60, 0.92, 0.9, at(4.6, 5.0));
    pen(g, smooth([[440, 292], [494, 296], [502, 352], [448, 368]], false, 6), 2.4, 61, 0.92, 0.9, at(5.0, 5.2));
    hatch(g, 380, 430, 460, 470, 6, 240, at(5.2, 5.45));
    // 연필
    pen(g, PEN_T.slice(0, Math.floor(PEN_T.length / 2)), 1.4, 70, 0.85, 0.9, at(6.8, 7.0));
    pen(g, [[548, 908], [522, 922], [544, 898]], 1.6, 71, 0.92, 0.9, at(7.0, 7.1));
    // 노트북 — 두 번째 문장("For twenty years…")과 함께
    const LP: [P, P, number, number, number][] = [[SCREEN[0], SCREEN[1], 1.3, 42, 0.8], [SCREEN[1], SCREEN[2], 2.2, 43, 0.92], [SCREEN[2], SCREEN[3], 2.2, 44, 0.92], [SCREEN[3], SCREEN[0], 1.2, 45, 0.7],
      [BASE[1], BASE[2], 2.2, 46, 0.92], [BASE[2], BASE[3], 2.4, 47, 0.92], [BASE[3], BASE[0], 1.3, 48, 0.75]];
    LP.forEach(([p, q, w, s, op], i) => pen(g, over(p, q), w, s, op, 0.9, at(7.4 + i * 0.13, 7.53 + i * 0.13)));
    for (let k = 0; k < 4; k++) pen(g, line([1290 + k * 14, 610 + k * 32], [1760 - k * 6, 618 + k * 32]), 0.7, 50 + k, 0.4, 0.5, at(8.3 + k * 0.07, 8.37 + k * 0.07));
    hatch(g, 1820, 610, 1880, 780, 10, 220, at(8.58, 8.85));
    // 잉크 튐 — 마지막에 펜을 털듯 한 방에
    const r = rng(90);
    for (let i = 0; i < 14; i++) { const x = 140 + r() * 1650, y = 120 + r() * 860, rx = 1.4 + r() * 3, ry = 1.4 + r() * 3, op = 0.55 + r() * 0.35; if (at(11.0 + i * 0.012, 11.01 + i * 0.012) > 0) fillShape(g, blob(x, y, rx, ry, 300 + i, 0.2, 8), INK, op); }
  });
  g.pop();

  // 3. 글자 — 글꼴 없이 펜으로 쓴 대문자(drafting.ts). 고지서 글자는 고지서와 함께 -6도 기울임
  const R = (BILL_A * Math.PI) / 180;
  g.push(BILL_C[0], BILL_C[1], fit, R);
  g.group("plain", () => {
    const xy = (x: number, y: number): [number, number] => [x - BILL_C[0], y - BILL_C[1]];
    letter(g, "TUITION & FEES", ...xy(588, 318), { cap: CAP55, color: INK, seed: 402, slant: 0.05, w: 2.6, progress: at(0.8, 1.75) });
    letter(g, "B.S. COMPUTER SCIENCE", ...xy(590, 422), { cap: CAP34, color: INK, seed: 404, slant: 0.05, progress: at(1.8, 2.4) });
    letter(g, "STATE UNIVERSITY", ...xy(606, 250), { cap: CAP34, color: PAPER, seed: 401, slant: 0.05, progress: at(3.0, 3.5) });
    letter(g, "FALL SEMESTER", ...xy(590, 377), { cap: CAP34, color: INK, seed: 403, slant: 0.05, progress: at(3.5, 4.0) });
    letter(g, "AMOUNT DUE", ...xy(672, 728), { cap: CAP34, color: INK, seed: 405, slant: 0.05, w: 2.4, progress: at(6.0, 6.6) });
  });
  g.pop();
  g.push(0, 0, fit);
  g.group("plain", () => {
    const r = rng(410);   // 노트북 화면: 읽을 한 줄만 글자로, 나머지 코드는 손으로 그은 짧은 선 묶음
    let n0 = 0;
    [[1312, 286, 6], [1340, 448, 4], [1312, 494, 5]].forEach(([x, y, n], k) => {
      let cx = x;
      for (let i = 0; i < n; i++, n0++) { const w = 28 + r() * 60; g.pen(line([cx, y], [cx + w, y + (r() - 0.5) * 3]), { w: 3, color: "#8fa3c4", seed: 420 + k * 10 + i, opacity: 0.8, boil: 0, retrace: false, wobble: 0.6, progress: at(8.0 + n0 * 0.06, 8.06 + n0 * 0.06) }); cx += w + 14; }
    });
    letter(g, "LEARN TO CODE", 1312, 330, { cap: CAP55, color: C.loud, seed: 406, slant: 0.1, w: 2.8, progress: at(8.9, 9.85) });
    letter(g, "= NEVER OUT OF WORK?", 1330, 392, { cap: CAP34, color: PAPER, seed: 407, slant: 0.1, progress: at(10.0, 10.95) });
  });
  g.pop();

  // 4. 종이 결
  g.paper("paper", 0.14);
  g.paper("coldpress", 0.22);
};

export const drawTuition = make(false);
export const tuition: Film = {
  meta: { title: "tuition", W: 1920, H: 1080, fps: 30, bpm: 60, durationFrames: 1 },
  assets: { images: {} },
  shots: [{ id: "tuition", start: 0, end: 1, draw: drawTuition }],
};
// 훅 영상: 2장 1프레임(on twos, 초당 그림 15장) — 손으로 그린 애니메이션의 박자
const HOOK_F = Math.ceil(HOOK_S * FPS);
export const tuitionhook: Film = {
  meta: { title: "tuitionhook", W: 1920, H: 1080, fps: FPS, bpm: 60, durationFrames: HOOK_F, step: 2, holds: [[Math.round(11.2 * FPS), HOOK_F, "다음 장면 전, 완성 그림을 읽는 시간"]] },
  assets: { images: {} },
  shots: [{ id: "hook", start: 0, end: HOOK_F, draw: make(true) }],
};
