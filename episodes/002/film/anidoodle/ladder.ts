import { Gfx, PENCIL, line, tube, type Ctx, type Env } from "./core";
import { Film } from "./film";
import { blob } from "./gallery";
import { C, INK, INK_M, PAPER, hatch, over, pen, wet } from "./inkwash";
import { letter } from "./drafting";

// EP002 장표 삽화 — "Is the career still there? / Is the first job harder now?" (s6_02)
// 비유: 사다리는 위까지 멀쩡한데(직업은 있다) 맨 아래 첫 칸만 빠졌다(첫 일자리가 어렵다). 빠진 칸 자리에만 오렌지.
// 크기 555×686(1:1.236) — 문장 판 왼쪽 빈 칸(x 89~644)에 종이 한 장으로 붙는다.
const W = 555, H = 686;
const LX = (y: number) => 150 - (20 * (y - 40)) / 600, RX = (y: number) => 400 + (20 * (y - 30)) / 610;
const RUNGS = [96, 186, 276, 366, 456], GAP = 556;

export const drawLadder = (ctx: Ctx, _frame: number, env: Env) => {
  const g = new Gfx(ctx, env, 0, INK_M), fit = env.W / W;
  ctx.setTransform(env.scale, 0, 0, env.scale, 0, 0);
  ctx.fillStyle = PAPER; ctx.fillRect(0, 0, env.W, env.H);
  g.push(0, 0, fit);

  // 0. 연필 밑그림: 땅선과 빠진 칸 자리 안내선
  const sk = new Gfx(ctx, env, 0, PENCIL);
  sk.push(0, 0, fit);
  sk.group("ink", () => {
    sk.pen(line([40, 652], [520, 646], 2), { seed: 2, w: 0.6, opacity: 0.22, boil: 0, retrace: false });
    sk.pen(line([LX(GAP) + 10, GAP], [RX(GAP) - 10, GAP], 2), { seed: 3, w: 0.6, opacity: 0.25, boil: 0, retrace: false });
  });
  sk.pop();

  // 1. 물감: 땅 그림자, 레일, 칸. 빠진 칸 자리는 칠하지 않는다(비어 있어야 빠진 것으로 읽힌다)
  wet(g, blob(300, 650, 210, 26, 5, 0.12, 20), C.shadow, { alpha: 0.3, seed: 5, pool: 0.4 });
  wet(g, tube([[LX(36), 36], [LX(640), 640]], 11, 9), C.wood, { alpha: 0.62, seed: 6, pool: 0.6 });
  wet(g, tube([[RX(26), 26], [RX(640), 640]], 11, 9), C.wood, { alpha: 0.62, seed: 7, pool: 0.6, bloom: [RX(300), 300], bloomR: 7 });
  RUNGS.forEach((y, i) => wet(g, tube([[LX(y) + 6, y], [RX(y) - 6, y]], 7, 9), C.wood, { alpha: 0.55, seed: 10 + i, pool: 0.5 }));

  // 2. 펜: 빛 받는 왼쪽 변은 열고 그늘 쪽(오른쪽·아래)만 눌러서
  g.group("plain", () => {
    pen(g, over([LX(36) + 11, 36], [LX(640) + 11, 640], 0.02), 2.2, 30);
    pen(g, over([LX(60) - 11, 60], [LX(330) - 11, 330], 0.02), 1.1, 31, 0.7);
    pen(g, over([RX(26) + 11, 26], [RX(640) + 11, 640], 0.02), 2.4, 32);
    pen(g, over([RX(380) - 11, 380], [RX(620) - 11, 620], 0.02), 1.1, 33, 0.7);
    RUNGS.forEach((y, i) => { pen(g, over([LX(y) + 11, y + 7], [RX(y) - 11, y + 7], 0.03), 1.9, 40 + i); pen(g, line([LX(y) + 40, y - 7], [LX(y) + 120, y - 7]), 0.9, 50 + i, 0.6, 0.6); });
    // 빠진 칸: 양쪽 레일에 부러진 그루터기만
    pen(g, [[LX(GAP) + 11, GAP - 4], [LX(GAP) + 34, GAP - 2], [LX(GAP) + 30, GAP + 6], [LX(GAP) + 11, GAP + 7]], 1.8, 60);
    pen(g, [[RX(GAP) - 11, GAP - 5], [RX(GAP) - 30, GAP - 1], [RX(GAP) - 26, GAP + 7], [RX(GAP) - 11, GAP + 7]], 1.8, 61);
    // 있어야 할 칸의 윤곽만 오렌지 점선 — 꽉 찬 띠로 칠하면 "오렌지 칸"으로 잘못 읽힌다
    for (const dy of [-8, 8]) for (let x = LX(GAP) + 40, k = 0; x < RX(GAP) - 40; x += 30, k++) g.pen(line([x, GAP + dy], [Math.min(x + 17, RX(GAP) - 40), GAP + dy + (k % 2 ? 0.8 : -0.8)]), { w: 2.2, color: C.loud, seed: 90 + k + (dy > 0 ? 40 : 0), wobble: 0.5, boil: 0, opacity: 0.9, retrace: false });
    pen(g, over([40, 652], [250, 650]), 1.6, 62); pen(g, over([330, 648], [520, 646]), 1.6, 63);   // 땅선은 한 번 끊김
    hatch(g, RX(120) + 18, 120, RX(600) + 18, 600, 18, 70);
  });
  g.pop();

  // 3. 손글씨: 위 칸 사이에 CAREER, 빠진 칸 자리에 FIRST JOB(오렌지 한 곳)
  g.push(0, 0, fit);
  g.group("plain", () => {
    letter(g, "CAREER", 277, 141 - 12, { cap: 24, color: INK, seed: 81, slant: 0.06, align: "center", w: 2.2 });
    letter(g, "FIRST JOB", 277, GAP + 34, { cap: 22, color: C.loud, seed: 82, slant: 0.06, align: "center", w: 2.4 });
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
