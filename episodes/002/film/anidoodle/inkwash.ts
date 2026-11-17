import { Gfx, line, poly, rng, type Ctx, type Env, type Medium, type P } from "./core";
import { blob, bounds, clamp, clipped, fillShape, mix } from "./gallery";

// Ink & line-wash(wren 방식) 공용 도구 — EP002 훅(tuition)과 장표 삽화(sketches)가 같은 손맛을 쓰게.
export const INK_M: Medium = { nib: 1.7, taper: 1, pressure: 1.75, retrace: false, wobble: 1.35, rough: 0.6 };
export const INK = "#1b2233", PAPER = "#f6f0e2";
export const C = { wood: "#cdb48e", navy: "#1e2a44", loud: "#f2622e", grey: "#9aa1ae", shadow: "#8c8399", coffee: "#6b4329", mug: "#e9e2d2", pencil: "#e7ae3e" };

// 물감: 선보다 살짝 크게·어긋나게 깔고(dx, dy, shrink), 아래쪽에 안료가 고이고, 원하면 백런 하나
export const wet = (g: Gfx, pts: P[], color: string, o: { alpha: number; seed: number; pool?: number; bloom?: P | null; bloomR?: number; shrink?: number; dx?: number; dy?: number }) => {
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
export const pen = (g: Gfx, pts: P[], w: number, seed: number, op = 0.92, wob = 0.9, progress = 1) => g.pen(pts, { w, color: INK, seed, wobble: wob, boil: 0, taper: 1, opacity: op, retrace: false, progress });
// 모서리를 넘치는 직선: 양 끝을 조금씩 더 그어 손이 멈추지 않은 것처럼
export const over = (a: P, b: P, k = 0.04): P[] => { const dx = b[0] - a[0], dy = b[1] - a[1]; return line([a[0] - dx * k, a[1] - dy * k], [b[0] + dx * k, b[1] + dy * k], 1.5); };
// 해칭: 그림자 안에 같은 방향의 짧은 펜 선. p로 한 획씩 차례로
export const hatch = (g: Gfx, x0: number, y0: number, x1: number, y1: number, n: number, seed: number, p = 1) => {
  const r = rng(seed);
  for (let i = 0; i < n; i++) { const t = i / n, x = x0 + (x1 - x0) * t, y = y0 + (y1 - y0) * t, a = r(), b = r(); pen(g, [[x, y], [x + 26 + a * 10, y + 18 + b * 6]], 0.8, seed + i, 0.55, 0.4, clamp(p * n - i)); }
};
export const corners = (cx: number, cy: number, w: number, h: number): P[] => [[cx - w / 2, cy - h / 2], [cx + w / 2, cy - h / 2], [cx + w / 2, cy + h / 2], [cx - w / 2, cy + h / 2]];
// 물감용 사각형: 변마다 점을 촘촘히 — 네 점만 주면 번짐이 둥글게 뭉개져 타원이 된다
export const sheet = (pts: P[]) => poly(pts, 14);
// 물감이 번져 나가는 모습: 왼쪽 위(붓이 처음 닿은 곳)에서 불규칙한 젖은 경계가 퍼진다. 경계 안쪽만 보인다
export const flood = (ctx: Ctx, env: Env, fit: number, pts: P[], p: number, seed: number, fn: () => void) => {
  if (p <= 0) return;
  if (p >= 1) { fn(); return; }
  const b = bounds(pts), ox = b.x0 + (b.x1 - b.x0) * 0.25, oy = b.y0 + (b.y1 - b.y0) * 0.3, R = Math.hypot(b.x1 - ox, b.y1 - oy) * 1.2 * p;
  const front = blob(ox, oy, R, R * 0.92, seed + 50, 0.22, 24);
  ctx.save(); ctx.setTransform(env.scale * fit, 0, 0, env.scale * fit, 0, 0);
  ctx.beginPath(); front.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.closePath(); ctx.clip();
  fn(); ctx.restore();
};

