import { Gfx, PENCIL, line, tube, type Ctx, type Env } from "./core";
import { Film } from "./film";
import { blob } from "./gallery";
import { C, INK, INK_M, PAPER, hatch, over, pen, wet } from "./inkwash";
import { letter } from "./drafting";

// EP002 장표 삽화 — "Is the career still there? / Is the first job harder now?" (s6_02)
// 비유: 사다리는 위까지 멀쩡한데(직업은 있다) 맨 아래 첫 칸만 빠졌다(첫 일자리가 어렵다). 빠진 칸 자리에만 오렌지.
// GOLDEN.md 필수: 종이는 황금 직사각형 555 × 898(= 555 × φ, 폭 555 = 황금선 733 − 바깥 여백 89 × 2).
// 칸 간격 144, 레일 사이 377(위)→419(아래, 기울기 21), 손글씨 대문자 34, 점선 21 · 주기 34 — 전부 피보나치.
const W = 555, H = 898;
const LX = (y: number) => 89 - (21 * (y - 34)) / 830, RX = (y: number) => 466 + (21 * (y - 34)) / 830;
const RUNGS = [89, 233, 377, 521, 665], GAP = 809, GROUND = 864;

export const drawLadder = (ctx: Ctx, _frame: number, env: Env) => {
  const g = new Gfx(ctx, env, 0, INK_M), fit = env.W / W, mid = (LX(GAP) + RX(GAP)) / 2;
  ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0);
  ctx.fillStyle = PAPER; ctx.fillRect(0, 0, env.W, env.H);
  g.push(0, 0, fit);

  // 0. 연필 밑그림: 땅선과 빠진 칸 자리 안내선
  const sk = new Gfx(ctx, env, 0, PENCIL);
  sk.push(0, 0, fit);
  sk.group("ink", () => {
    sk.pen(line([34, GROUND], [521, GROUND - 5], 2), { seed: 2, w: 0.6, opacity: 0.22, boil: 0, retrace: false });
    sk.pen(line([LX(GAP) + 13, GAP], [RX(GAP) - 13, GAP], 2), { seed: 3, w: 0.6, opacity: 0.25, boil: 0, retrace: false });
  });
  sk.pop();

  // 1. 물감: 땅 그림자, 레일, 칸. 빠진 칸 자리는 칠하지 않는다(비어 있어야 빠진 것으로 읽힌다)
  wet(g, blob(mid, GROUND, 233, 21, 5, 0.12, 20), C.shadow, { alpha: 0.3, seed: 5, pool: 0.4 });
  wet(g, tube([[LX(34), 34], [LX(GROUND), GROUND]], 13, 9), C.wood, { alpha: 0.62, seed: 6, pool: 0.6 });
  wet(g, tube([[RX(34), 34], [RX(GROUND), GROUND]], 13, 9), C.wood, { alpha: 0.62, seed: 7, pool: 0.6, bloom: [RX(377), 377], bloomR: 8 });
  RUNGS.forEach((y, i) => wet(g, tube([[LX(y) + 8, y], [RX(y) - 8, y]], 8, 9), C.wood, { alpha: 0.55, seed: 10 + i, pool: 0.5 }));

  // 2. 펜: 빛 받는 왼쪽 변은 열고 그늘 쪽(오른쪽·아래)만 눌러서
  g.group("plain", () => {
    pen(g, over([LX(34) + 13, 34], [LX(GROUND) + 13, GROUND], 0.02), 2.2, 30);
    pen(g, over([LX(55) - 13, 55], [LX(377) - 13, 377], 0.02), 1.1, 31, 0.7);
    pen(g, over([RX(34) + 13, 34], [RX(GROUND) + 13, GROUND], 0.02), 2.4, 32);
    pen(g, over([RX(521) - 13, 521], [RX(809) - 13, 809], 0.02), 1.1, 33, 0.7);
    RUNGS.forEach((y, i) => { pen(g, over([LX(y) + 13, y + 8], [RX(y) - 13, y + 8], 0.03), 1.9, 40 + i); pen(g, line([LX(y) + 55, y - 8], [LX(y) + 144, y - 8]), 0.9, 50 + i, 0.6, 0.6); });
    // 빠진 칸: 양쪽 레일에 부러진 그루터기만
    pen(g, [[LX(GAP) + 13, GAP - 5], [LX(GAP) + 34, GAP - 2], [LX(GAP) + 30, GAP + 8], [LX(GAP) + 13, GAP + 8]], 1.8, 60);
    pen(g, [[RX(GAP) - 13, GAP - 5], [RX(GAP) - 34, GAP - 2], [RX(GAP) - 30, GAP + 8], [RX(GAP) - 13, GAP + 8]], 1.8, 61);
    // 있어야 할 칸의 윤곽만 오렌지 점선(21 긋고 13 비움) — 꽉 찬 띠로 칠하면 "오렌지 칸"으로 잘못 읽힌다
    for (const dy of [-8, 8]) for (let x = LX(GAP) + 55, k = 0; x < RX(GAP) - 55; x += 34, k++) g.pen(line([x, GAP + dy], [Math.min(x + 21, RX(GAP) - 55), GAP + dy + (k % 2 ? 0.8 : -0.8)]), { w: 2.2, color: C.loud, seed: 90 + k + (dy > 0 ? 40 : 0), wobble: 0.5, boil: 0, opacity: 0.9, retrace: false });
    pen(g, over([34, GROUND], [233, GROUND - 2]), 1.6, 62); pen(g, over([322, GROUND - 3], [521, GROUND - 5]), 1.6, 63);   // 땅선은 한 번 끊김
    hatch(g, RX(144) + 21, 144, RX(809) + 21, 809, 21, 70);
  });
  g.pop();

  // 3. 손글씨(대문자 34): 맨 위 두 칸 사이에 CAREER, 빠진 칸 바로 위에 FIRST JOB(오렌지 한 곳)
  g.push(0, 0, fit);
  g.group("plain", () => {
    letter(g, "CAREER", mid, (RUNGS[0] + RUNGS[1]) / 2 - 17, { cap: 34, color: INK, seed: 81, slant: 0.06, align: "center", w: 2.6 });
    letter(g, "FIRST JOB", mid, (RUNGS[4] + GAP) / 2 - 17, { cap: 34, color: C.loud, seed: 82, slant: 0.06, align: "center", w: 2.8 });
  });
  g.pop();

  g.paper("paper", 0.14);
  g.paper("coldpress", 0.22);
};

export const ladder: Film = {
  meta: { title: "ladder", W, H, fps: 30, bpm: 60, durationFrames: 1 },
  assets: { images: {} },
  shots: [{ id: "ladder", start: 0, end: 1, draw: drawLadder }],
};
