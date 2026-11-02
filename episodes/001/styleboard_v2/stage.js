// EP001 시안 v2 — 3D 데이터 무대(초록 커팅 매트 위 종이 차트). 숫자는 전부 02_research.md 출처.
// REF: threejs-fundamentals (r170, 헤드리스 스크린샷용 preserveDrawingBuffer)
import * as THREE from './three.module.js';

const W = 1920, H = 1080;
const C = { mat: '#1f5d4c', line: '#3d806b', paper: '#f4efe3', ink: '#1a1a1a', red: '#c8392e',
  mustard: '#e5b650', mustardPale: '#f1d99a', slate: '#6f8fb0', slatePale: '#b9c8d8' };
const FONT = '"Avenir Next Condensed", "DIN Condensed", sans-serif';
const lerp = (a, b, p) => a + (b - a) * p;
const ease = p => p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;

function tex(w, h, draw) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return t;
}
// 종이 결: 고정 시드 잡음이라 매 프레임 같은 결이 나온다
function grain(g, w, h, amt, seed = 7) {
  let s = seed;
  const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < w * h / 30; i++) {
    g.fillStyle = `rgba(0,0,0,${rnd() * amt})`; g.fillRect(rnd() * w, rnd() * h, 1 + rnd() * 2, 1);
  }
}
const matTex = () => tex(2048, 1228, (g, w, h) => {
  g.fillStyle = C.mat; g.fillRect(0, 0, w, h); grain(g, w, h, 0.18);
  g.strokeStyle = C.line;
  for (let x = 0; x <= w; x += 51) { g.lineWidth = x % 255 === 0 ? 2.5 : 1; g.beginPath(); g.moveTo(x, 0); g.lineTo(x, h); g.stroke(); }
  for (let y = 0; y <= h; y += 51) { g.lineWidth = y % 255 === 0 ? 2.5 : 1; g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); }
});
const paperTex = color => tex(256, 256, (g, w, h) => { g.fillStyle = color; g.fillRect(0, 0, w, h); grain(g, w, h, 0.12, color.length * 31); });
// 종이 라벨: 찢긴 가장자리 + 굵은 콘덴스드 글자
function labelTex(lines, { bg = C.paper, fg = C.ink, size = 150, w = 0, h = 300 } = {}) {
  if (!w) { const m = document.createElement('canvas').getContext('2d');
    w = Math.max(...lines.map(l => { m.font = `800 ${l.size || size}px ${FONT}`; return m.measureText(l.text).width; })) + 180; }
  return tex(w, h, (g) => {
    g.beginPath(); g.moveTo(10, 14);
    for (let x = 10; x < w - 10; x += 40) g.lineTo(x, 8 + (x * 7 % 11));
    g.lineTo(w - 8, h - 12);
    for (let x = w - 10; x > 10; x -= 40) g.lineTo(x, h - 6 - (x * 5 % 9));
    g.closePath(); g.fillStyle = bg; g.fill(); grain(g, w, h, 0.08);
    g.fillStyle = fg; g.textAlign = 'center'; g.textBaseline = 'middle';
    lines.forEach((l, i) => { g.font = `800 ${l.size || size}px ${FONT}`; g.fillText(l.text, w / 2, h / 2 + (i - (lines.length - 1) / 2) * (l.size || size) * 1.02); });
  });
}
// hUnits = 라벨 높이(월드 단위), 폭은 글자 길이에서 나온다
function tag(lines, hUnits, opts = {}) {
  const map = labelTex(lines, opts), img = map.image;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(hUnits * img.width / img.height, hUnits),
    new THREE.MeshStandardMaterial({ map, transparent: true, roughness: 1, side: THREE.DoubleSide }));
  m.castShadow = true; return m;
}
const box = (w, h, d, color) => {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshStandardMaterial({ map: paperTex(color), roughness: 0.95 }));
  m.castShadow = true; m.receiveShadow = true; return m;
};

function baseScene() {
  const s = new THREE.Scene(); s.background = new THREE.Color('#174a3d'); s.fog = new THREE.Fog('#174a3d', 22, 60);
  const mt = matTex(); mt.wrapS = mt.wrapT = THREE.RepeatWrapping; mt.repeat.set(3, 3);
  const mat = new THREE.Mesh(new THREE.PlaneGeometry(150, 90), new THREE.MeshStandardMaterial({ map: mt, roughness: 1 }));
  mat.rotation.x = -Math.PI / 2; mat.receiveShadow = true; s.add(mat);
  s.add(new THREE.HemisphereLight('#fff6e6', '#2a4a40', 1.4));
  const key = new THREE.DirectionalLight('#fff1d6', 2.6); key.position.set(-8, 14, 9); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048); Object.assign(key.shadow.camera, { left: -16, right: 16, top: 12, bottom: -12, far: 50 });
  key.shadow.radius = 4; s.add(key);
  return s;
}

// 장면 1: 제목 드롭 — 종이 카드 세 장이 매트 위로 떨어져 눕는다(위에서 내려다보는 콜라주 시점)
function titleScene() {
  const s = baseScene();
  const spec = [['WHAT REALLY HIT', 150, 2.2, -1.2, -2.7, -0.04], ['ENTRY-LEVEL JOBS', 190, 2.7, 0.2, 0.1, 0.03], ['IN 2022', 190, 2.5, 3.6, 2.9, -0.06]];
  const cards = spec.map(([text, size, hU, x, z, rz]) => {
    const c = tag([{ text, size }], hU); c.userData = { x, z, rz }; s.add(c); return c;
  });
  for (let i = 0; i < 10; i++) {
    const sc = box(1.7, 0.02, 1.2, C.paper), ang = i / 10 * Math.PI * 2;
    sc.position.set(Math.cos(ang) * 10.5, 0.02, Math.sin(ang) * 6.2); sc.rotation.y = i * 0.9; s.add(sc);
  }
  const tapeMat = new THREE.MeshStandardMaterial({ color: '#efe0a8', transparent: true, opacity: 0.8, roughness: 1 });
  const tapes = [[-6.6, -3.4, 0.7], [7.4, 3.6, -0.6]].map(([x, z, r]) => { const t = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 0.5), tapeMat);
    t.rotation.set(-Math.PI / 2, 0, r); t.position.set(x, 0.06, z); s.add(t); return t; });
  return { s, pose(p, cam) {
    const q = ease(p);
    cards.forEach((c, i) => { const { x, z, rz } = c.userData, d = Math.min(1, Math.max(0, q * 1.7 - i * 0.28));
      c.position.set(x, 0.04 + i * 0.01 + (1 - d) * 3.5, z); c.rotation.set(-Math.PI / 2 + (1 - d) * 0.35, 0, rz + (1 - d) * 0.4); });
    tapes.forEach(t => { t.visible = q > 0.7; });
    cam.position.set(lerp(-1.5, 0.8, q), lerp(16.5, 15, q), lerp(9.5, 8.2, q)); cam.lookAt(0.3, 0, 0.4);
  } };
}

// 장면 2: 29세 미만 3.1% → 3.7% vs 경력 대졸 1.9% → 1.8% (LSE 2026-06-01)
function dataAScene() {
  const s = baseScene(), U = 1.25, bars = [];
  const spec = [[-5.2, 3.1, C.mustardPale, '3.1%'], [-2.9, 3.7, C.mustard, '3.7%'], [2.9, 1.9, C.slatePale, '1.9%'], [5.2, 1.8, C.slate, '1.8%']];
  spec.forEach(([x, v, col, txt], i) => {
    const b = box(1.9, 1, 1.9, col); s.add(b);
    const t = tag([{ text: txt, size: 190 }], 1.0); s.add(t);
    bars.push({ b, t, x, h: v * U, i });
    const yr = tag([{ text: i % 2 ? '2022–25' : '2017–19', size: 150 }], 0.55);
    yr.rotation.x = -Math.PI / 2; yr.position.set(x, 0.03, 1.55); s.add(yr);
  });
  [['UNDER 29', -4.05, C.mustard], ['OLDER GRADS', 4.05, C.slate]].forEach(([t, x, col]) => {
    const g = tag([{ text: t, size: 170 }], 0.85, { bg: col });
    g.rotation.x = -Math.PI / 2; g.rotation.z = x < 0 ? 0.03 : -0.03; g.position.set(x, 0.035, 2.55); s.add(g);
  });
  const chip = tag([{ text: '+20%', size: 200 }], 0.9, { bg: C.red, fg: C.paper }); s.add(chip);
  return { s, pose(p, cam) {
    const q = ease(p);
    bars.forEach(({ b, t, x, h, i }) => { const g = Math.min(1, Math.max(0.02, q * 1.5 - i * 0.12));
      b.scale.y = h * g; b.position.set(x, h * g / 2, 0); t.position.set(x, h * g + 0.7, 0.2); t.rotation.set(-0.12, 0, (i % 2 ? -1 : 1) * 0.04); });
    chip.position.set(-1.2, 3.7 * U + 0.2, 0.6); chip.rotation.z = -0.12; chip.visible = q > 0.55;
    cam.position.set(lerp(-3.5, -0.5, q), lerp(7, 7.8, q), lerp(17, 15.5, q)); cam.lookAt(0, 2.0, 0.6);
  } };
}

// 장면 3: 원격 근무가 증가분의 64%를 설명(저자 어림값 → 화면에 Estimate 표시)
function gridScene() {
  const s = baseScene(), tiles = [];
  for (let i = 0; i < 100; i++) {
    const on = i < 64, t = box(0.88, 0.06, 0.88, on ? C.red : C.paper);
    t.userData = { on, x: (i % 10 - 4.5) * 1.02 + 3.2, z: (Math.floor(i / 10) - 4.5) * 1.02, i }; s.add(t); tiles.push(t);
  }
  return { s, pose(p, cam) {
    const q = ease(p);
    tiles.forEach(t => { const { on, x, z, i } = t.userData; const d = on ? Math.min(1, Math.max(0, q * 2.2 - i / 64)) : 0;
      t.position.set(x, 0.04 + d * 0.35, z); t.rotation.set(d * 0.08, 0, (1 - d) * (on ? 0.4 : 0) * Math.sin(i)); });
    cam.position.set(lerp(1.5, 0.5, q), lerp(15.5, 14.5, q), lerp(10.5, 9.5, q)); cam.lookAt(1.2, 0, 0.4);
  } };
}

// 장면 4: 스탠퍼드 — 22~25세 고용, 노출 상위 두 분위 약 −11%, 하위 세 분위 약 +10% (2022-11 → 2026-06)
function waveScene() {
  const s = baseScene(), base = 4;
  const edgeMat = new THREE.LineBasicMaterial({ color: C.paper, transparent: true, opacity: 0.75 });
  const stacks = [[-3.4, 1.10, C.slate, '≈ +10%', 'LEAST EXPOSED'], [3.4, 0.89, C.red, '≈ −11%', 'MOST AI-EXPOSED']].map(([x, k, col, txt, lab]) => {
    const st = box(3, 1, 2.2, col); s.add(st);
    // 2022-11 시작 높이를 모서리선만으로 남긴다
    const ghost = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(3.04, base, 2.24)), edgeMat);
    ghost.position.set(x, base / 2, 0); s.add(ghost);
    const t = tag([{ text: txt, size: 190 }], 1.1); s.add(t);
    const l = tag([{ text: lab, size: 150 }], 0.8, { bg: col });
    l.rotation.x = -Math.PI / 2; l.position.set(x, 0.03, 1.9); s.add(l);
    return { st, t, x, k };
  });
  return { s, pose(p, cam) {
    const q = ease(p);
    stacks.forEach(({ st, t, x, k }) => { const h = base * lerp(1, k, Math.min(1, q * 1.4));
      st.scale.y = h; st.position.set(x, h / 2, 0); t.position.set(x, Math.max(h, base) + 0.85, 0.3); t.rotation.z = x < 0 ? 0.04 : -0.05; });
    cam.position.set(lerp(5, 2.5, q), lerp(7.5, 8.2, q), lerp(17, 16, q)); cam.lookAt(0, 3.6, 0.5);
  } };
}

export function makeStage(canvas) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  r.setPixelRatio(1); r.setSize(W, H, false);
  r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.0; r.shadowMap.enabled = true;
  const cam = new THREE.PerspectiveCamera(38, W / H, 0.1, 200);
  const scenes = { title: titleScene(), dataA: dataAScene(), grid: gridScene(), wave: waveScene() };
  return { render(name, p) { const sc = scenes[name]; sc.pose(p, cam); r.render(sc.s, cam); } };
}
