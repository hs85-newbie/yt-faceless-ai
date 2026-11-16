import { Gfx, PENCIL, line, oval, poly, rng, tube, turn, type Ctx, type Env, type Medium, type P } from "./core";
import { Film } from "./film";
import { blob, bounds, clamp, clipped, fillShape, mix, smooth } from "./gallery";
import { letter } from "./drafting";

// EP002 훅 정지 화면 v2 — Ink & line-wash(wren 방식). 위에서 본 부엌 식탁: 등록금 고지서(초점) · 'learn to code' 노트북 · 커피잔 · 연필.
// 손그림으로 읽히게: 물감이 선 밖으로 번지고 아래에 고이며 백런, 흰 종이는 칠하지 않고 남김, 펜은 모서리를 넘치고
// 빛 받는 쪽은 열어 두며 그늘 쪽만 눌러 그음, 연필 밑그림 선이 남음, 그림자는 해칭, 잉크 튐, 글자는 손으로 옮겨 적은 듯 흔들림.
// 색: brand/golden.css 팔레트 A 역할(크림 종이 · 네이비 잉크 · 오렌지 한 곳). 고지서에 금액 없음(출처 없는 숫자 금지). 빛은 왼쪽 위.
const INK_M: Medium = { nib: 1.7, taper: 1, pressure: 1.75, retrace: false, wobble: 1.35, rough: 0.6 };
const INK = "#1b2233", PAPER = "#f6f0e2";
const C = { wood: "#cdb48e", navy: "#1e2a44", loud: "#f2622e", grey: "#9aa1ae", shadow: "#8c8399", coffee: "#6b4329", mug: "#e9e2d2", pencil: "#e7ae3e" };
const BILL_C: P = [820, 540], BILL_A = -6;

// 물감: 선보다 살짝 크게·어긋나게 깔고(dx, dy, shrink), 아래쪽에 안료가 고이고, 원하면 백런 하나
const wet = (g: Gfx, pts: P[], color: string, o: { alpha: number; seed: number; pool?: number; bloom?: P | null; bloomR?: number; shrink?: number; dx?: number; dy?: number }) => {
  const { alpha, seed, pool = 0.55, bloom = null, bloomR = 26, shrink = 1.07, dx = 7, dy = 6 } = o, b = bounds(pts);
  g.group("paint", () => {
    g.wash(pts, color, { alpha, seed, dx, dy, shrink, rim: true });
    clipped(g, pts, () => {
      const c = g.cur, gr = c.createLinearGradient(0, b.y0 + (b.y1 - b.y0) * 0.45, 0, b.y1 + 2);
      const hx = (a: number) => Math.round(255 * clamp(a)).toString(16).padStart(2, "0");
      gr.addColorStop(0, color + "00"); gr.addColorStop(0.75, color + hx(alpha * pool * 0.6)); gr.addColorStop(1, color + hx(alpha * pool * 1.3));
      c.fillStyle = gr; c.fillRect(b.x0 - 20, b.y0, b.x1 - b.x0 + 40, b.y1 - b.y0 + 20);
    });
    if (bloom) {
      const bl = blob(bloom[0], bloom[1], bloomR, bloomR * 0.8, seed + 7, 0.32, 18);
      fillShape(g, bl, PAPER, 0.42);
      const c = g.cur; c.strokeStyle = mix(color, INK, 0.25); c.globalAlpha = alpha * 0.9; c.lineWidth = 1.6;
      c.beginPath(); bl.forEach(([x, y], i) => (i ? c.lineTo(x, y) : c.moveTo(x, y))); c.closePath(); c.stroke(); c.globalAlpha = 1;
    }
  });
};
const pen = (g: Gfx, pts: P[], w: number, seed: number, op = 0.92, wob = 0.9) => g.pen(pts, { w, color: INK, seed, wobble: wob, boil: 0, taper: 1, opacity: op, retrace: false });
// 모서리를 넘치는 직선: 양 끝을 조금씩 더 그어 손이 멈추지 않은 것처럼
const over = (a: P, b: P, k = 0.04): P[] => { const dx = b[0] - a[0], dy = b[1] - a[1]; return line([a[0] - dx * k, a[1] - dy * k], [b[0] + dx * k, b[1] + dy * k], 1.5); };
// 해칭: 그림자 안에 같은 방향의 짧은 펜 선
const hatch = (g: Gfx, x0: number, y0: number, x1: number, y1: number, n: number, seed: number) => {
  const r = rng(seed);
  for (let i = 0; i < n; i++) { const t = i / n, x = x0 + (x1 - x0) * t, y = y0 + (y1 - y0) * t; pen(g, [[x, y], [x + 26 + r() * 10, y + 18 + r() * 6]], 0.8, seed + i, 0.55, 0.4); }
};
const rot = (pts: P[]) => turn(pts, BILL_C[0], BILL_C[1], BILL_A);
const corners = (cx: number, cy: number, w: number, h: number): P[] => [[cx - w / 2, cy - h / 2], [cx + w / 2, cy - h / 2], [cx + w / 2, cy + h / 2], [cx - w / 2, cy + h / 2]];
// 물감용 사각형: 변마다 점을 촘촘히 — 네 점만 주면 번짐이 둥글게 뭉개져 타원이 된다
const sheet = (pts: P[]) => poly(pts, 14);

const BILL = rot(corners(820, 540, 520, 690));
const SCREEN: P[] = [[1270, 214], [1800, 232], [1792, 556], [1264, 546]];
const BASE: P[] = [[1238, 562], [1818, 574], [1872, 756], [1186, 742]];

export const drawTuition = (ctx: Ctx, _frame: number, env: Env) => {
  const g = new Gfx(ctx, env, 0, INK_M);
  ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0);
  ctx.fillStyle = PAPER; ctx.fillRect(0, 0, env.W, env.H);
  const fit = env.W / 1920;
  g.push(0, 0, fit);

  // 0. 연필 밑그림: 원근 안내선과 고지서 자리 — 지우지 않고 남겨 둔다
  const sketch = new Gfx(ctx, env, 0, PENCIL);
  sketch.push(0, 0, fit);
  sketch.group("ink", () => {
    sketch.pen(line([120, 960], [1860, 880], 2), { seed: 2, w: 0.7, opacity: 0.22, boil: 0, retrace: false });
    sketch.pen(rot(corners(826, 546, 540, 706)), { seed: 3, closed: true, w: 0.6, opacity: 0.2, boil: 0 });
    sketch.pen(oval(334, 334, 128, 124, 14), { seed: 4, closed: true, w: 0.6, opacity: 0.2, boil: 0 });
  });
  sketch.pop();

  // 1. 물감 — 바탕 한 번(가장자리는 종이로 남김), 그다음 그림자, 물체(흰 고지서는 칠하지 않음)
  wet(g, smooth([[90, 120], [1840, 90], [1880, 980], [70, 1010]], true, 8), C.wood, { alpha: 0.32, seed: 1, pool: 0.4, bloom: [1500, 900], bloomR: 60 });
  wet(g, sheet(rot(corners(846, 568, 520, 690))), C.shadow, { alpha: 0.32, seed: 2, pool: 0.5 });
  wet(g, blob(356, 360, 124, 118, 3, 0.08, 20), C.shadow, { alpha: 0.28, seed: 3 });
  wet(g, sheet([[1212, 592], [1856, 604], [1904, 792], [1204, 780]]), C.shadow, { alpha: 0.26, seed: 4 });
  g.group("plain", () => fillShape(g, sheet(BILL), PAPER, 1));   // 종이는 아래를 가린다: 고지서 자리는 종이색으로 덮고 칠하지 않음
  wet(g, sheet(rot(corners(820, 262, 470, 74))), C.navy, { alpha: 0.82, seed: 6, pool: 0.6, shrink: 0.95, dx: -6, dy: 2 });   // 선에 못 미쳐 흰 틈
  wet(g, sheet(rot(corners(830, 742, 400, 88))), C.loud, { alpha: 0.6, seed: 7, pool: 0.7, bloom: [960, 736], bloomR: 18, shrink: 0.94, dx: 8, dy: -3 });
  wet(g, sheet(SCREEN), C.navy, { alpha: 0.9, seed: 9, pool: 0.5, bloom: [1700, 470], bloomR: 34 });
  wet(g, sheet(BASE), C.grey, { alpha: 0.42, seed: 8, pool: 0.6 });
  wet(g, blob(330, 330, 118, 116, 10, 0.04, 22), C.mug, { alpha: 0.6, seed: 10, pool: 0.5 });
  wet(g, blob(330, 330, 90, 88, 11, 0.05, 20), C.coffee, { alpha: 0.88, seed: 11, pool: 0.9, bloom: [300, 300], bloomR: 22 });
  wet(g, tube([[548, 908], [782, 818]], 10, 9), C.pencil, { alpha: 0.75, seed: 13, pool: 0.6 });

  // 2. 펜 — 초점(고지서)부터. 빛 받는 위·왼쪽 변은 끊어 두고, 그늘 쪽 오른쪽·아래 변은 눌러서
  g.group("plain", () => {
    const [a, b, c, d] = BILL;
    pen(g, over(a, [a[0] + (b[0] - a[0]) * 0.55, a[1] + (b[1] - a[1]) * 0.55]), 1.2, 21, 0.75);   // 윗변 앞 절반만
    pen(g, over([a[0] + (b[0] - a[0]) * 0.7, a[1] + (b[1] - a[1]) * 0.7], b), 1.1, 22, 0.7);
    const m1: P = [b[0] + (c[0] - b[0]) * 0.46, b[1] + (c[1] - b[1]) * 0.46], m2: P = [b[0] + (c[0] - b[0]) * 0.52, b[1] + (c[1] - b[1]) * 0.52];
    pen(g, over(b, m1, 0.02), 2.4, 23); pen(g, over(m2, c, 0.03), 2.4, 26); pen(g, over(c, d), 2.6, 24);   // 긴 변은 한 번 끊김                                  // 그늘 쪽은 굵게
    pen(g, over(d, [d[0] + (a[0] - d[0]) * 0.6, d[1] + (a[1] - d[1]) * 0.6]), 1.4, 25, 0.8);   // 왼변은 아래만
    for (let i = 0; i < 6; i++) {   // 본문 줄: 글자 대신 손으로 그은 줄
      const y = 452 + i * 42, x2 = i % 2 ? 960 : 1040;
      pen(g, rot(line([600, y], [x2, y], (i % 3) - 1)), 0.9, 30 + i, 0.5, 0.6);
    }
    hatch(g, 1060, 300, 1110, 900, 22, 200);                                                   // 고지서 그림자 해칭
    // 노트북
    pen(g, over(SCREEN[0], SCREEN[1]), 1.3, 42, 0.8); pen(g, over(SCREEN[1], SCREEN[2]), 2.2, 43); pen(g, over(SCREEN[2], SCREEN[3]), 2.2, 44); pen(g, over(SCREEN[3], SCREEN[0]), 1.2, 45, 0.7);
    pen(g, over(BASE[1], BASE[2]), 2.2, 46); pen(g, over(BASE[2], BASE[3]), 2.4, 47); pen(g, over(BASE[3], BASE[0]), 1.3, 48, 0.75);
    for (let k = 0; k < 4; k++) pen(g, line([1290 + k * 14, 610 + k * 32], [1760 - k * 6, 618 + k * 32]), 0.7, 50 + k, 0.4, 0.5);
    hatch(g, 1820, 610, 1880, 780, 10, 220);
    // 잔: 위쪽 테는 열고 아래쪽만 눌러서, 손잡이
    const rim = smooth(blob(330, 330, 118, 116, 10, 0.04, 22), true, 4);
    pen(g, rim.slice(Math.floor(rim.length * 0.15), Math.floor(rim.length * 0.75)), 2.2, 60);
    pen(g, smooth([[440, 292], [494, 296], [502, 352], [448, 368]], false, 6), 2.4, 61);
    hatch(g, 380, 430, 460, 470, 6, 240);
    // 연필
    const pt = tube([[548, 908], [782, 818]], 10, 9);
    pen(g, pt.slice(0, Math.floor(pt.length / 2)), 1.4, 70, 0.85);
    pen(g, [[548, 908], [522, 922], [544, 898]], 1.6, 71);
    // 잉크 튐
    const r = rng(90);
    for (let i = 0; i < 14; i++) fillShape(g, blob(140 + r() * 1650, 120 + r() * 860, 1.4 + r() * 3, 1.4 + r() * 3, 300 + i, 0.2, 8), INK, 0.55 + r() * 0.35);
  });
  g.pop();

  // 3. 글자 — 글꼴 없이 펜으로 쓴 대문자(drafting.ts). 고지서 글자는 고지서와 함께 -6도 기울임
  const R = (BILL_A * Math.PI) / 180;
  g.push(BILL_C[0], BILL_C[1], fit, R);
  g.group("plain", () => {
    const at = (x: number, y: number): [number, number] => [x - BILL_C[0], y - BILL_C[1]];
    letter(g, "STATE UNIVERSITY", ...at(606, 250), { cap: 24, color: PAPER, seed: 401, slant: 0.05 });
    letter(g, "TUITION & FEES", ...at(588, 318), { cap: 32, color: INK, seed: 402, slant: 0.05, w: 2.6 });
    letter(g, "FALL SEMESTER", ...at(590, 366), { cap: 15, color: INK, seed: 403, slant: 0.05 });
    letter(g, "B.S. COMPUTER SCIENCE", ...at(590, 394), { cap: 15, color: INK, seed: 404, slant: 0.05 });
    letter(g, "AMOUNT DUE", ...at(672, 728), { cap: 24, color: INK, seed: 405, slant: 0.05, w: 2.4 });
  });
  g.pop();
  g.push(0, 0, fit);
  g.group("plain", () => {
    const r = rng(410);   // 노트북 화면: 읽을 한 줄만 글자로, 나머지 코드는 손으로 그은 짧은 선 묶음
    [[1312, 286, 6], [1340, 448, 4], [1312, 494, 5]].forEach(([x, y, n], k) => {
      let cx = x;
      for (let i = 0; i < n; i++) { const w = 28 + r() * 60; g.pen(line([cx, y], [cx + w, y + (r() - 0.5) * 3]), { w: 3, color: "#8fa3c4", seed: 420 + k * 10 + i, opacity: 0.8, boil: 0, retrace: false, wobble: 0.6 }); cx += w + 14; }
    });
    letter(g, "LEARN TO CODE", 1312, 330, { cap: 28, color: C.loud, seed: 406, slant: 0.1, w: 2.8 });
    letter(g, "= NEVER OUT OF WORK?", 1330, 392, { cap: 20, color: PAPER, seed: 407, slant: 0.1 });
  });
  g.pop();

  // 4. 종이 결
  g.paper("paper", 0.14);
  g.paper("coldpress", 0.22);
};

export const tuition: Film = {
  meta: { title: "tuition", W: 1920, H: 1080, fps: 30, bpm: 60, durationFrames: 1 },
  assets: { images: {} },
  shots: [{ id: "tuition", start: 0, end: 1, draw: drawTuition }],
};
