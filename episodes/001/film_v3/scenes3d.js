// EP001 본편 v3 — 3D 데이터 무대 장면들. 숫자는 전부 02_research.md 출처(장면마다 번호 주석).
// pose(p, cam, tl, opt): p = 컷 진행 0~1, tl = 컷 시작 후 초, opt = cuts.json의 장면 옵션
import { THREE, C, lerp, ease, tag, box, baseScene } from './lib3d.js';

const clamp01 = x => Math.min(1, Math.max(0, x));
const flat = (m, x, z, rz = 0, y = 0.03) => { m.rotation.set(-Math.PI / 2, 0, rz); m.position.set(x, y, z); return m; };
const after = (tl, at, dur = 0.5) => clamp01((tl - at) / dur);

// 제목 드롭: 종이 카드 세 장이 매트에 떨어져 눕는다
function title() {
  const s = baseScene();
  const spec = [['WHAT REALLY HIT', 150, 2.2, -1.2, -2.7, -0.04], ['ENTRY-LEVEL JOBS', 190, 2.7, 0.2, 0.1, 0.03], ['IN 2022', 190, 2.5, 3.6, 2.9, -0.06]];
  const cards = spec.map(([text, size, hU, x, z, rz]) => { const c = tag([{ text, size }], hU); c.userData = { x, z, rz }; s.add(c); return c; });
  for (let i = 0; i < 10; i++) { const a = i / 10 * Math.PI * 2, sc = box(1.7, 0.02, 1.2, C.paper); sc.position.set(Math.cos(a) * 10.5, 0.02, Math.sin(a) * 6.2); sc.rotation.y = i * 0.9; s.add(sc); }
  return { s, pose(p, cam) {
    const q = ease(p);
    cards.forEach((c, i) => { const { x, z, rz } = c.userData, d = clamp01(q * 2.2 - i * 0.3);
      c.position.set(x, 0.04 + i * 0.01 + (1 - d) * 3.5, z); c.rotation.set(-Math.PI / 2 + (1 - d) * 0.35, 0, rz + (1 - d) * 0.4); });
    cam.position.set(lerp(-1.5, 0.8, q), lerp(16.5, 15, q), lerp(9.5, 8.2, q)); cam.lookAt(0.3, 0, 0.4);
  } };
}

// 큰 숫자 카드: 5.6% 실업, 42% 하향 취업 (#1, #2)
function numbers() {
  const s = baseScene();
  const a = tag([{ text: '5.6%', size: 230 }, { text: 'UNEMPLOYED', size: 90 }], 3.6, { h: 420 });
  const b = tag([{ text: '42%', size: 230 }, { text: 'UNDEREMPLOYED', size: 90 }], 3.6, { h: 420, bg: C.mustard });
  s.add(a, b);
  return { s, pose(p, cam, tl, o) {
    const da = after(tl, 0.1, 0.4), db = after(tl, o.second ?? 99, 0.4);
    flat(a, -3.2, 0, -0.05, 0.04 + (1 - da) * 4); a.visible = da > 0;
    flat(b, 3.4, 0.6, 0.06, 0.05 + (1 - db) * 4); b.visible = db > 0;
    cam.position.set(lerp(-2.5, 1.5, ease(p)), 13, 7.5); cam.lookAt(lerp(-1.5, 1.2, ease(p)), 0, 0.3);
  } };
}

// 막대: 29세 미만 3.1→3.7%, 경력 대졸 1.9→1.8% (#4, #5). opt.focus = 'young' | 'all'
function bars() {
  const s = baseScene(), U = 1.25, items = [];
  [[-5.2, 3.1, C.mustardPale, '3.1%'], [-2.9, 3.7, C.mustard, '3.7%'], [2.9, 1.9, C.slatePale, '1.9%'], [5.2, 1.8, C.slate, '1.8%']].forEach(([x, v, col, txt], i) => {
    const b = box(1.9, 1, 1.9, col), t = tag([{ text: txt, size: 190 }], 1.0); s.add(b, t); items.push({ b, t, x, h: v * U, i });
    s.add(flat(tag([{ text: i % 2 ? '2022–25' : '2017–19', size: 150 }], 0.55), x, 1.55));
  });
  s.add(flat(tag([{ text: 'UNDER 29', size: 170 }], 0.85, { bg: C.mustard }), -4.05, 2.55, 0.03, 0.035));
  s.add(flat(tag([{ text: 'OLDER GRADS', size: 170 }], 0.85, { bg: C.slate }), 4.05, 2.55, -0.03, 0.035));
  const chip = tag([{ text: '+20%', size: 200 }], 0.9, { bg: C.red, fg: C.paper }); s.add(chip);
  return { s, pose(p, cam, tl, o) {
    const q = ease(p), all = o.focus === 'all';
    items.forEach(({ b, t, x, h, i }) => { const g = all ? (i < 2 ? 1 : clamp01(q * 2 - (i - 2) * 0.3)) : (i < 2 ? clamp01(q * 2.2 - i * 0.35) : 0.02);
      b.scale.y = Math.max(0.02, h * g); b.position.set(x, b.scale.y / 2, 0); t.position.set(x, b.scale.y + 0.7, 0.2); t.visible = g > 0.3; t.rotation.set(-0.12, 0, (i % 2 ? -1 : 1) * 0.04); });
    chip.position.set(-1.2, 3.7 * U + 0.2, 0.6); chip.rotation.z = -0.12; chip.visible = all || tl > (o.chipAt ?? 99);
    const cx = all ? lerp(-3, 1.5, q) : lerp(-6.5, -5, q);
    cam.position.set(cx, all ? 7.8 : 7, all ? 15.5 : 14.5); cam.lookAt(all ? cx * 0.6 : -4.1, 2.2, 0.4);
  } };
}

function arrow(col, len, up) {
  const g = new THREE.Group(), m = box(0.5, len, 0.5, col), head = new THREE.Mesh(new THREE.ConeGeometry(0.75, 0.9, 4), m.material);
  m.position.y = len / 2; head.position.y = len + 0.4; head.rotation.y = Math.PI / 4; head.castShadow = true; g.add(m, head);
  if (!up) g.rotation.z = Math.PI; return g;
}
// 원격 가능 직종 vs 대면 직종 (#6, #18). 정확한 수치가 없는 변화는 막대 대신 화살표+문구로만 표시
function lanes() {
  const s = baseScene(), lane = (z, txt, col) => { const st = box(16, 0.05, 3.2, C.paper); st.position.set(0.5, 0.03, z); s.add(st);
    s.add(flat(tag([{ text: txt, size: 160 }], 1.1, { bg: col }), -5.6, z + 1.0, 0.02, 0.08)); };
  lane(-2.4, 'FROM-HOME JOBS', C.mustard); lane(2.6, 'SHOW-UP JOBS', C.slate);
  const up = arrow(C.red, 2.6, true), down = arrow(C.slate, 0.9, false); up.position.set(-2.5, 0.06, -2.4); down.position.set(2.5, 1.6, -2.4); s.add(up, down);
  const tUp = tag([{ text: 'YOUNG GRADS ≈ +1 PT', size: 140 }], 0.95), tDn = tag([{ text: 'OLDER · SLIGHT DECLINE', size: 140 }], 0.95); s.add(tUp, tDn);
  const bump = box(2.2, 1.2, 1.2, C.red); bump.position.set(-2.5, 0.6, 2.6); s.add(bump);
  const back = box(9, 0.25, 1.2, C.slatePale); back.position.set(3.6, 0.15, 2.6); s.add(back);
  s.add(flat(tag([{ text: '2020', size: 160 }], 0.8), -2.5, 1.7, 0, 0.09));
  const tShow = tag([{ text: 'GAP WIDENED IN 2020, THEN WENT BACK', size: 130 }], 0.95); s.add(tShow);
  return { s, pose(p, cam, tl, o) {
    const q = ease(p), show = o.focus === 'show', g = show ? 1 : clamp01(q * 2);
    up.scale.y = Math.max(0.05, g); down.scale.y = Math.max(0.05, clamp01(q * 2 - 0.4));
    tUp.position.set(-2.5, 3.9 * g + 0.4, -2.2); tDn.position.set(2.8, 2.9, -2.2); tDn.visible = q > 0.35 || show;
    const b = show ? clamp01(q * 2.5) : 0; bump.scale.y = Math.max(0.02, Math.sin(b * Math.PI)); bump.position.y = bump.scale.y * 0.6;
    back.visible = tShow.visible = show && q > 0.45; tShow.position.set(3.6, 1.2, 2.9);
    cam.position.set(lerp(-2.5, 2, q), 13.5, show ? 15.5 : 12.5); cam.lookAt(lerp(-1, 1.2, q), 0.6, show ? 2.0 : -1.2);
  } };
}

// 타임라인 (#4, #10, #12, #15). opt.mode = 'nyfed' | 'bands'
const X = y => (y - 2021.5) * 2.4;   // 1년 = 2.4 단위
function timeline() {
  const s = baseScene(), strip = box(26, 0.05, 1.1, C.paper); strip.position.set(0, 0.03, 0); s.add(strip);
  const marks = [[2017, '2017'], [2020, '2020'], [2022.83, 'NOV 2022 · CHATGPT', C.red], [2025, '2025'], [2026.5, 'JUN 2026']].map(([y, txt, bg]) => {
    const t = flat(tag([{ text: txt, size: 150 }], 0.95, bg ? { bg, fg: C.paper } : {}), X(y), 1.35, 0, 0.07); s.add(t); return t; });
  const band = (y0, y1, z, col, txt) => { const b = box(X(y1) - X(y0), 0.12, 1.0, col); b.position.set((X(y0) + X(y1)) / 2, 0.1, z); s.add(b);
    const t = flat(tag([{ text: txt, size: 140 }], 0.85, { bg: col }), (X(y0) + X(y1)) / 2, z - 1.05, 0.01, 0.2); s.add(t); return [b, t]; };
  const nyA = band(2017, 2020, -1.4, C.mustard, 'BEFORE: 2017–19'), nyB = band(2022, 2025, -1.4, C.mustard, 'AFTER: 2022–24');
  const st = band(2022.83, 2026.5, -3.8, C.red, 'STANFORD: NOV 2022 → JUN 2026');
  const nyLab = flat(tag([{ text: 'NEW YORK FED: REMOTE WORK', size: 140 }], 0.85, { bg: C.mustard }), X(2018.5), -3.3, 0, 0.2); s.add(nyLab);
  return { s, pose(p, cam, tl, o) {
    const q = ease(p), bands = o.mode === 'bands';
    [...nyA, ...nyB].forEach(m => { m.visible = q > (bands ? 0.05 : 0.3); });
    [...st, nyLab].forEach(m => { m.visible = bands && q > 0.35; });
    marks[2].scale.setScalar(1 + 0.15 * Math.sin(clamp01(q * 3 - 1.2) * Math.PI));
    cam.position.set(lerp(-4, 3, q), bands ? 13 : 9.5, bands ? 8.5 : 7.5); cam.lookAt(lerp(-3.5, 2.5, q), 0, bands ? -1.8 : -0.4);
  } };
}

// 100칸 그리드: 64%는 저자 어림값 (#8)
function grid() {
  const s = baseScene(), tiles = [];
  for (let i = 0; i < 100; i++) { const on = i < 64, t = box(0.88, 0.06, 0.88, on ? C.red : C.paper);
    t.userData = { on, x: (i % 10 - 4.5) * 1.02 + 3.2, z: (Math.floor(i / 10) - 4.5) * 1.02, i }; s.add(t); tiles.push(t); }
  return { s, pose(p, cam) {
    const q = ease(p);
    tiles.forEach(t => { const { on, x, z, i } = t.userData, d = on ? clamp01(q * 2.2 - i / 64) : 0;
      t.position.set(x, 0.04 + d * 0.35, z); t.rotation.set(d * 0.08, 0, (1 - d) * (on ? 0.4 : 0) * Math.sin(i)); });
    cam.position.set(lerp(1.5, 0.5, q), lerp(15.5, 14.5, q), lerp(10.5, 9.5, q)); cam.lookAt(1.2, 0, 0.4);
  } };
}

// 두 더미 비교: 스탠퍼드 +10/−11% (#13) 또는 인구조사국 −12%·유지 (#10). 모서리선 = 시작 높이
function stacks(o) {
  const s = baseScene(), base = 4, edge = new THREE.LineBasicMaterial({ color: C.paper, transparent: true, opacity: 0.75 });
  const items = o.items.map(([x, k, col, txt, lab]) => {
    const st = box(3, 1, 2.2, C[col]); s.add(st);
    const g = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(3.04, base, 2.24)), edge); g.position.set(x, base / 2, 0); s.add(g);
    const t = tag([{ text: txt, size: 190 }], 1.1); s.add(t);
    s.add(flat(tag([{ text: lab, size: 150 }], 0.8, { bg: C[col] }), x, 1.9));
    return { st, t, x, k };
  });
  return { s, pose(p, cam) {
    const q = ease(p);
    items.forEach(({ st, t, x, k }) => { const h = base * lerp(1, k, clamp01(q * 1.6 - 0.2));
      st.scale.y = h; st.position.set(x, h / 2, 0); t.position.set(x, Math.max(h, base) + 0.85, 0.3); t.rotation.z = x < 0 ? 0.04 : -0.05; });
    cam.position.set(lerp(6.5, 1, q), lerp(7, 8.5, q), lerp(18.5, 14.5, q)); cam.lookAt(lerp(0.8, -0.4, q), 3.4, 0.5);
  } };
}

// 기준금리 계단: 0.08% (2022-01) → 5.33% (2023-08) → 2024 중반까지 유지 (#15). 중간 월 값은 그리지 않는다
function rates() {
  const s = baseScene(), U = 0.9, cols = [];
  [[-6, 0.08, 'JAN 2022', '0.08%'], [0, 5.33, 'AUG 2023', '5.33%'], [6, 5.33, 'MID-2024', '5.33%']].forEach(([x, v, d, txt], i) => {
    const b = box(2.4, 1, 2.4, i ? C.red : C.slatePale), t = tag([{ text: txt, size: 190 }], 1.0); s.add(b, t);
    s.add(flat(tag([{ text: d, size: 150 }], 0.6), x, 1.9)); cols.push({ b, t, x, h: Math.max(0.12, v * U), i });
  });
  return { s, pose(p, cam) {
    const q = ease(p);
    cols.forEach(({ b, t, x, h, i }) => { const g = clamp01(q * 2.2 - i * 0.45); b.scale.y = Math.max(0.05, h * g); b.position.set(x, b.scale.y / 2, 0);
      t.position.set(x, b.scale.y + 0.75, 0.3); t.visible = g > 0.2; });
    cam.position.set(lerp(-5, 4, q), lerp(9.5, 7, q), lerp(19, 14, q)); cam.lookAt(lerp(-1.5, 1.5, q), 2.4, 0);
  } };
}

const MAKERS = { title, numbers, bars, lanes, timeline, grid, rates,
  stanford: () => stacks({ items: [[-3.4, 1.10, 'slate', '≈ +10%', 'LEAST EXPOSED'], [3.4, 0.89, 'red', '≈ −11%', 'MOST AI-EXPOSED']] }),
  census: () => stacks({ items: [[-3.4, 1.0, 'slate', 'HELD STEADY', 'LESS EXPOSED INDUSTRIES'], [3.4, 0.88, 'red', '−12%', 'MOST AI-EXPOSED INDUSTRIES']] }) };

export function makeStage(canvas) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  r.setPixelRatio(1); r.setSize(1920, 1080, false);
  r.toneMapping = THREE.ACESFilmicToneMapping; r.shadowMap.enabled = true;
  const cam = new THREE.PerspectiveCamera(38, 1920 / 1080, 0.1, 200), cache = {};
  return { render(name, p, tl, opt = {}) {
    const sc = cache[name] ??= MAKERS[name]();
    sc.pose(p, cam, tl, opt); r.render(sc.s, cam);
  } };
}
