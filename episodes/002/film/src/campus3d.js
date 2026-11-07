// EP002 3D 캠퍼스(three.js r170). 모든 프레임은 GSAP 타임라인 시각의 함수다(state → render), 무작위는 시드 해시만.
// 생성기 scripts/ep002_campus3d.py가 window.__WORLD(데이터·숏·사건 시각)를 넣고 이 파일을 <script type="module">로 감싼다.
import * as THREE from "three";
import { EffectComposer } from "./assets/lib/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "./assets/lib/addons/postprocessing/RenderPass.js";
import { ShaderPass } from "./assets/lib/addons/postprocessing/ShaderPass.js";
import { OutputPass } from "./assets/lib/addons/postprocessing/OutputPass.js";
import { HorizontalTiltShiftShader } from "./assets/lib/addons/shaders/HorizontalTiltShiftShader.js";
import { VerticalTiltShiftShader } from "./assets/lib/addons/shaders/VerticalTiltShiftShader.js";

const W = window.__WORLD, root = document.querySelector('[data-composition-id="campus3d"]');
const hash = (i) => { let x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };   // 시드 해시(Math.random 금지)
const FOOT = 0.84, FLOOR = 0.2;

// ── 렌더러 ────────────────────────────────────────────
const canvas = root.querySelector("#gl");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(1920, 1080, false);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const scene = new THREE.Scene();
scene.background = new THREE.Color("#b9d3e8");
scene.fog = new THREE.Fog("#c9dcec", 16, 46);   // 원경을 하늘로 녹인다(위쪽 빈 초록 평면 방지)
scene.background = new THREE.Color("#c9dcec");
const camera = new THREE.PerspectiveCamera(26, 1920 / 1080, 0.1, 200);

// ── 빛: 따뜻한 해(그림자) + 하늘빛 ─────────────────────
scene.add(new THREE.HemisphereLight("#eaf3ff", "#7d9a5a", 1.05));
const sun = new THREE.DirectionalLight("#fff1dc", 2.4);
sun.position.set(-9, 16, -4); sun.target.position.set(7.5, 0, 5.5);
sun.castShadow = true; sun.shadow.mapSize.set(4096, 4096); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.02;
Object.assign(sun.shadow.camera, { left: -14, right: 14, top: 14, bottom: -14, near: 1, far: 50 });
scene.add(sun, sun.target);

// ── 질감(캔버스, 결정적) ───────────────────────────────
function canvasTex(w, h, draw, rep) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; } return t;
}
const grassTex = canvasTex(512, 512, (g, w, h) => {
  g.fillStyle = "#9fc27a"; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 9000; i++) { g.fillStyle = `rgba(${hash(i) > .5 ? "70,110,50" : "190,215,150"},${.08 + hash(i + 7) * .1})`; g.fillRect(hash(i + 1) * w, hash(i + 2) * h, 2, 2); }
}, true); grassTex.repeat.set(24, 24);
function wallTex(base, glass) {   // 창문 격자: 칸마다 2열, 층마다 1행
  return canvasTex(128, 128, (g, w, h) => {
    g.fillStyle = base; g.fillRect(0, 0, w, h);
    g.fillStyle = glass; for (const x of [16, 72]) g.fillRect(x, 40, 40, 56);
    g.fillStyle = "rgba(255,255,255,.18)"; for (const x of [16, 72]) g.fillRect(x, 40, 40, 10);
    g.fillStyle = "rgba(0,0,0,.08)"; g.fillRect(0, 118, w, 10);   // 층 경계선
  }, true);
}
function textTex(text, bg, fg, w = 1024, h = 256, font = "900 120px 'Archivo Black', Inter, sans-serif") {
  return canvasTex(w, h, (g) => { g.fillStyle = bg; g.fillRect(0, 0, w, h); g.fillStyle = fg; g.font = font; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(text, w / 2, h / 2 + 6); });
}

// ── 땅: 잔디 · 돌길 · 광장 잔디 ─────────────────────────
const ground = new THREE.Mesh(new THREE.PlaneGeometry(120, 120), new THREE.MeshStandardMaterial({ map: grassTex, roughness: 1 }));
ground.rotation.x = -Math.PI / 2; ground.position.set(7.5, 0, 5); ground.receiveShadow = true; scene.add(ground);
const slab = (x0, z0, x1, z1, color, y) => {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(x1 - x0, z1 - z0), new THREE.MeshStandardMaterial({ color, roughness: .95 }));
  m.rotation.x = -Math.PI / 2; m.position.set((x0 + x1) / 2, y, (z0 + z1) / 2); m.receiveShadow = true; scene.add(m); return m;
};
slab(-1.4, -1.4, 15.4, 11.6, "#e9dfc9", 0.004);                                     // 캠퍼스 돌길 바닥
for (const [ox, oy] of Object.values(W.QUADS)) slab(ox - .3, oy - .3, ox + 4.3, oy + 4.3, "#a8cc80", 0.008);   // 광장 잔디

// ── 나무(광장 둘레, 인스턴스) ───────────────────────────
const trees = [];
for (const [ox, oy] of Object.values(W.QUADS)) for (let k = 0; k <= 4; k++)
  for (const [x, z] of [[ox - .62, oy + k], [ox + 4.62, oy + k], [ox + k, oy - .62], [ox + k, oy + 4.62]]) trees.push([x, z]);
const uniq = [...new Map(trees.map(p => [p.map(v => v.toFixed(2)).join(","), p])).values()];
const trunks = new THREE.InstancedMesh(new THREE.CylinderGeometry(.035, .05, .26, 6), new THREE.MeshStandardMaterial({ color: "#6b4f36" }), uniq.length);
const crowns = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(.2, 1), new THREE.MeshStandardMaterial({ color: "#4f8a45", roughness: .9, flatShading: true }), uniq.length);
const mtx = new THREE.Matrix4(), col = new THREE.Color();
uniq.forEach(([x, z], i) => {
  const s = .85 + hash(i) * .35;
  mtx.makeTranslation(x, .13, z); trunks.setMatrixAt(i, mtx);
  mtx.compose(new THREE.Vector3(x, .26 + .17 * s, z), new THREE.Quaternion(), new THREE.Vector3(s, s * 1.08, s)); crowns.setMatrixAt(i, mtx);
  crowns.setColorAt(i, col.set(hash(i + 9) > .5 ? "#4f8a45" : "#5f9a4c"));
});
for (const m of [trunks, crowns]) { m.castShadow = true; m.receiveShadow = true; scene.add(m); }

// ── 건물: 땅속에서 솟는다(높이 = 실업률 x HS) ─────────────
const ROOFS = ["#5e6268", "#4f7f78", "#8a5a44", "#6d6a63"].map(c => new THREE.MeshStandardMaterial({ color: c, roughness: .8 }));   // 슬레이트·동판·기와
const WALLS = ["#efe4cc", "#e6d6b6", "#ece8df"];
const roofCS = new THREE.MeshStandardMaterial({ color: "#b8401e", roughness: .7 });
const bld = {};
for (const b of W.B) {
  const h = Math.max(.06, b.u * W.HS), cs = b.id === W.CS;
  const i = W.B.indexOf(b);
  const tex = wallTex(cs ? "#ff7a45" : WALLS[Math.floor(hash(i + 3) * 3)], cs ? "#9c3416" : "#6f8796"); tex.repeat.set(FOOT / .42, h / FLOOR);
  const wall = new THREE.MeshStandardMaterial({ map: tex, roughness: .85, emissive: cs ? "#ff5a1f" : "#000000", emissiveIntensity: cs ? .18 : 0 });
  const geo = new THREE.BoxGeometry(FOOT, h, FOOT); geo.translate(0, h / 2, 0);
  const mesh = new THREE.Mesh(geo, [wall, wall, cs ? roofCS : ROOFS[Math.floor(hash(i + 11) * 4)], wall, wall, wall]);
  mesh.castShadow = true; mesh.receiveShadow = true;
  const grp = new THREE.Group(); grp.position.set(b.gx + .5, 0, b.gy + .5); grp.add(mesh); scene.add(grp);
  const edges = new THREE.LineSegments(new THREE.EdgesGeometry(geo), new THREE.LineBasicMaterial({ color: b.id === W.CE ? "#e4572e" : "#1d2421" }));
  edges.visible = b.id === W.CE; mesh.add(edges);
  const plot = slab(b.gx + .5 - FOOT / 2, b.gy + .5 - FOOT / 2, b.gx + .5 + FOOT / 2, b.gy + .5 + FOOT / 2, cs ? "#e98a68" : "#d8ccb2", 0.012);
  bld[b.id] = { b, h, mesh, wall, edges, plot, rise: 0, hi: 0 };
}

// ── 정문 아치 · 구역 표지판 ─────────────────────────────
const brick = new THREE.MeshStandardMaterial({ color: "#8a3b2b", roughness: .8 });
const gate = new THREE.Group(); gate.position.set(9.5, 0, 11.9); gate.rotation.y = 0;
for (const x of [-.95, .95]) { const p = new THREE.Mesh(new THREE.BoxGeometry(.22, .95, .22), brick); p.position.set(x, .475, 0); p.castShadow = true; gate.add(p); }
const lintel = new THREE.Mesh(new THREE.BoxGeometry(2.3, .36, .16), [brick, brick, brick, brick,
  new THREE.MeshStandardMaterial({ map: textTex("STATE UNIVERSITY", "#8a3b2b", "#f4ead7", 1024, 160, "900 92px 'Archivo Black', Inter, sans-serif") }), brick]);
lintel.position.set(0, 1.05, 0); lintel.castShadow = true; gate.add(lintel); scene.add(gate);
const qsigns = [];
for (const [q, [ox, oy]] of Object.entries(W.QUADS)) {
  const s = new THREE.Group(); s.position.set(ox + 2, 0, oy + 4.62); s.rotation.y = Math.PI / 4;   // 카메라 쪽(+x+z)을 본다
  const board = new THREE.Mesh(new THREE.BoxGeometry(1.5, .32, .05), [brick, brick, brick, brick,
    new THREE.MeshStandardMaterial({ map: textTex(W.QNAME[q], "#24453a", "#ffffff", 1024, 220, "800 92px Inter, sans-serif") }), brick]);
  board.position.y = .42; board.castShadow = true; s.add(board);
  for (const x of [-.6, .6]) { const p = new THREE.Mesh(new THREE.BoxGeometry(.04, .3, .04), brick); p.position.set(x, .13, 0); s.add(p); }
  s.visible = false; scene.add(s); qsigns.push(s);   // 글자는 HTML .qlbl이 맡는다(작은 3D 글자는 안 읽힘)
}

// ── 4.2% 기준 유리판(공학 구역) · 첫 직장 길(리본) ───────
const level = new THREE.Mesh(new THREE.BoxGeometry(4.8, .015, 4.8), new THREE.MeshBasicMaterial({ color: "#9ec9f0", transparent: true, opacity: 0, depthWrite: false }));   // 반사광 없이(눈부심 방지)
level.position.set(7, 4.2 * W.HS, 2); scene.add(level);
const levelEdge = new THREE.LineSegments(new THREE.EdgesGeometry(level.geometry), new THREE.LineBasicMaterial({ color: "#1d4f7a", transparent: true, opacity: 0 }));
level.add(levelEdge);
const ROAD = [[5.5, 3.95], [5.5, 4.5], [9.5, 4.5], [9.5, -1.0], [9.5, -3.2]];   // CS 앞 → 공학·과학 사잇길 → 캠퍼스 밖
const roadCurve = new THREE.CatmullRomCurve3(ROAD.map(([x, z]) => new THREE.Vector3(x, .06, z)), false, "catmullrom", .05);
const roadGeo = new THREE.TubeGeometry(roadCurve, 160, .07, 8, false);
const road = new THREE.Mesh(roadGeo, new THREE.MeshStandardMaterial({ color: "#1d2421", roughness: .6 })); road.castShadow = true; scene.add(road);
const ROAD_END = new THREE.Vector3(9.5, 0, -3.2);
const jobsSign = new THREE.Group(); jobsSign.position.copy(ROAD_END); jobsSign.rotation.y = Math.PI / 4;
const jb = new THREE.Mesh(new THREE.BoxGeometry(2.4, .44, .06), [brick, brick, brick, brick,
  new THREE.MeshStandardMaterial({ map: textTex("ENTRY-LEVEL SOFTWARE JOBS", "#1d2421", "#f4ecdc", 1600, 300, "900 80px 'Archivo Black', Inter, sans-serif") }), brick]);
jb.position.y = .62; jb.castShadow = true; jobsSign.add(jb);
for (const x of [-1, 1]) { const p = new THREE.Mesh(new THREE.BoxGeometry(.05, .42, .05), brick); p.position.set(x, .2, 0); jobsSign.add(p); }
scene.add(jobsSign);

// ── 카메라: 숏마다 대상 bbox에 맞춘 상태 ─────────────────
const AZ0 = Math.PI / 4, EL = 0.62;   // 기본 방위(+x+z 쪽에서), 앙각 ~35°
function frameFor(who, azDeg) {
  let pts = [];
  const add = (b) => { const k = bld[b]; const { gx, gy } = k.b; pts.push([gx, 0, gy], [gx + 1, k.h, gy + 1]); };
  if (who === "ALL" || who === "ALL+GATE") { for (const id in bld) add(id); if (who === "ALL+GATE") pts.push([gate.position.x, 1.2, gate.position.z]); }
  else for (const n of who) { if (n === "ROAD_END") pts.push([ROAD_END.x - 1.3, 1.0, ROAD_END.z + 1.3], [ROAD_END.x + 1.3, 1.0, ROAD_END.z - 1.3]);
    else if (n === "GATE") pts.push([gate.position.x - 1.3, 1.3, gate.position.z], [gate.position.x + 1.3, 0, gate.position.z]); else add(W.B.find(b => b.name === n).id); }
  const lo = [0, 1, 2].map(i => Math.min(...pts.map(p => p[i]))), hi = [0, 1, 2].map(i => Math.max(...pts.map(p => p[i])));
  const c = lo.map((v, i) => (v + hi[i]) / 2), r = Math.hypot(hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]) / 2;
  let dist = Math.max(4.2, r / Math.sin(THREE.MathUtils.degToRad(26) / 2) * 0.62);
  const g = Array.isArray(who) && who.includes("GATE");   // 첫 구도: 정문이 앞에 온전히 보이게 조금 물리고 정문 쪽으로 당김
  if (g) { dist *= 1.22; c[0] += 0.8; c[2] += 1.1; }
  return { tx: c[0], ty: c[1] * 0.6, tz: c[2], dist, az: AZ0 + THREE.MathUtils.degToRad(azDeg) };
}
const SH = W.SHOTS.map(s => ({ ...s, f: frameFor(s.who, s.az) }));
const cam = { ...SH[0].f };
const v3 = new THREE.Vector3();
function placeCamera() {
  camera.position.set(cam.tx + cam.dist * Math.cos(EL) * Math.sin(cam.az), cam.ty + cam.dist * Math.sin(EL), cam.tz + cam.dist * Math.cos(EL) * Math.cos(cam.az));
  camera.lookAt(cam.tx, cam.ty, cam.tz); camera.updateMatrixWorld();
}

// ── 후처리: 틸트시프트(모형을 내려다보는 느낌) ───────────
const composer = new EffectComposer(renderer);
composer.setPixelRatio(1); composer.setSize(1920, 1080);
composer.addPass(new RenderPass(scene, camera));
const hts = new ShaderPass(HorizontalTiltShiftShader), vts = new ShaderPass(VerticalTiltShiftShader);
hts.uniforms.h.value = 1.6 / 1920; vts.uniforms.v.value = 1.6 / 1080; hts.uniforms.r.value = vts.uniforms.r.value = 0.5;
composer.addPass(hts); composer.addPass(vts); composer.addPass(new OutputPass());

// ── 라벨: 3D 지붕을 화면에 투영 ──────────────────────────
const LBL = [...root.querySelectorAll(".lbl, .qlbl")];
let tl = null;
function syncLabels() {   // 투영 후, 같은 시각에 보이는 라벨끼리 겹치면 아래쪽(앞쪽)부터 놓고 위로 비켜 쌓는다
  const t = tl ? tl.time() : 0, placed = [], items = [];
  for (const el of LBL) {
    const live = t >= +el.dataset.start && t < +el.dataset.start + +el.dataset.duration;
    const k = el.dataset.bid ? bld[el.dataset.bid] : null;
    if (k) v3.set(k.b.gx + .5, k.h * k.rise + .02, k.b.gy + .5); else v3.set(+el.dataset.wx, +el.dataset.wy, +el.dataset.wz);
    v3.project(camera);
    items.push({ el, live, x: (v3.x + 1) / 2 * 1920, y: (1 - v3.y) / 2 * 1080 - 8 + +el.dataset.oy, w: el.offsetWidth || 260, h: el.offsetHeight || 140 });
  }
  items.sort((a, b) => b.y - a.y);
  for (const it of items) {
    if (it.live) {
      const y0 = it.y;
      for (let guard = 0; guard < 40; guard++) {
        const hit = placed.find(p => Math.abs(p.x - it.x) < (p.w + it.w) / 2 + 12 && it.y > p.y - p.h - 8 && it.y - it.h < p.y + 8);
        if (!hit) break;
        if (hit.y - hit.h - 10 - it.h > 40) it.y = hit.y - hit.h - 10;        // 위로 비킬 공간이 있으면 위로
        else { it.y = y0; it.x = hit.x + (hit.w + it.w) / 2 + 14; }           // 없으면 옆으로(화면 위로 잘리지 않게)
      }
      it.x = Math.min(1920 - it.w / 2 - 24, Math.max(it.w / 2 + 24, it.x)); it.y = Math.max(it.h + 24, it.y);
      placed.push(it);
    }
    it.el.style.left = it.x.toFixed(1) + "px"; it.el.style.top = it.y.toFixed(1) + "px";
  }
}

// ── 그리기: 상태 → 장면 ───────────────────────────────
const fx = { level: 0, road: 0, green: 0, qsign: 1, gate: 1, plots: -1 };
const green = new THREE.Color("#3f8f5b"), cream = new THREE.Color("#ffffff");
function render() {
  for (const id in bld) {
    const k = bld[id]; k.mesh.position.y = -k.h * (1 - k.rise); k.mesh.visible = k.rise > 0.001;
    k.edges.visible = id === W.CE || k.hi > 0.5;
  }
  for (const id in bld) { const k = bld[id], p = Math.max(0, 1 - Math.abs(fx.plots - (k.b.gx + k.b.gy) / 22) * 6); if (id !== W.CS) k.plot.material.color.set("#d8ccb2").lerp(new THREE.Color("#f4c95d"), p); }
  for (const id of W.GREEN) bld[id].wall.color.copy(cream).lerp(green, fx.green);
  level.material.opacity = 0.1 * fx.level; levelEdge.material.opacity = fx.level;
  roadGeo.setDrawRange(0, Math.floor(roadGeo.index.count * fx.road / 3) * 3);
  jobsSign.visible = fx.road > 0.6; jobsSign.scale.setScalar(Math.min(1, Math.max(0.001, (fx.road - 0.6) / 0.4)));
  for (const s of qsigns) s.visible = false;
  gate.visible = fx.gate > 0.5;
  placeCamera(); syncLabels(); composer.render();
}

// ── 타임라인 ────────────────────────────────────────────
tl = gsap.timeline({ paused: true, onUpdate: render });
const E = W.EV;
tl.fromTo(bld[W.CS], { rise: 0 }, { rise: 1, duration: 0.9, ease: "power3.out" }, E.cs_rise);
for (const id in bld) if (id !== W.CS) {
  const { gx, gy } = bld[id].b;
  tl.fromTo(bld[id], { rise: 0 }, { rise: 1, duration: 0.9, ease: "power3.out" }, E.wave + (gx + gy) * 0.045);
}
SH.forEach((s, i) => {
  if (i > 0) tl.to(cam, { ...s.f, duration: s.d, ease: "power2.inOut" }, s.t);
  const next = i + 1 < SH.length ? SH[i + 1].t : W.END, arrive = s.t + s.d;
  if (next - arrive > 1.5) tl.to(cam, { dist: s.f.dist * 0.95, duration: next - arrive - 0.05, ease: "sine.inOut" }, arrive + 0.02);   // 머무는 동안 5% 다가감
});
tl.fromTo(fx, { plots: -0.2 }, { plots: 1.2, duration: 1.6, ease: "none" }, E.majors73);   // "73 majors": 대지가 앞에서 뒤로 차례로 빛난다
tl.set(fx, { qsign: 0 }, E.q_end); tl.set(fx, { gate: 0 }, E.gate_end);
tl.fromTo(fx, { level: 0 }, { level: 1, duration: 0.6, ease: "power2.out" }, E.level);
tl.to(fx, { level: 0, duration: 0.3 }, SH.find(s => s.t > E.level).t);
tl.fromTo(fx, { green: 0 }, { green: 1, duration: 0.4 }, E.green);
tl.fromTo(fx, { road: 0 }, { road: 1, duration: 1.2, ease: "power1.inOut" }, E.road);
for (const l of W.LABELS) {   // 라벨 동안 건물 윤곽 + 숫자 카운트업(하나씩)
  tl.set(bld[l.bid], { hi: 1 }, l.t); tl.set(bld[l.bid], { hi: 0 }, l.e - 0.01);
  const el = root.querySelector("#" + l.id), big = el.querySelector(".big");
  tl.fromTo(el.children, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.3, ease: "power4.out", stagger: 0.05 }, l.t);
  if (l.count != null && big) { const n = { v: 0 }; tl.fromTo(n, { v: 0 }, { v: l.count, duration: 0.7, ease: "power2.out", onUpdate: () => { big.textContent = n.v.toFixed(1) + "%"; } }, l.t); }
}
for (const el of root.querySelectorAll("#title, #sign-level"))
  tl.fromTo(el, { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.35, ease: "power4.out" }, parseFloat(el.dataset.start));
tl.to({}, { duration: 0.01 }, W.END - 0.01);
render();
window.__timelines["campus3d"] = tl;
