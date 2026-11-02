// EP001 본편 v3 — 3D 공통 부품(종이 질감·라벨·매트 무대). 시안 v2 stage.js에서 분리.
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


export { THREE, W, H, C, FONT, lerp, ease, tag, box, baseScene, paperTex };
