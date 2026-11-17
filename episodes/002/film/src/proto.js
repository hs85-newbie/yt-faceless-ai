// EP002 시안: "캠퍼스가 그래프가 된다" 두 장면(three.js r170). 프레임 = 타임라인 시각의 함수(state → render).
// 장면 1: 회색 캠퍼스 → 건물이 실업률 축(왼쪽 안전, 오른쪽 위험)으로 줄을 선다. 평균 4.2% 세로선, 오른쪽 바닥은 붉게.
// 장면 2: 건물이 초봉만큼 솟고 카메라가 옆으로 내려와 산점도(가로 = 실업률, 높이 = 초봉)가 된다.
// 생성기 scripts/ep002_proto.py가 window.__PROTO(전공 73개·평균·장면 시각)를 넣는다.
import * as THREE from "three";

const P = window.__PROTO, T = P.THEME, root = document.querySelector('[data-composition-id="proto"]');
const XS = 1.3, FOOT = 0.42, GAP = 0.5, HW = 4.2 / 100000;   // 실업률 1%p당 가로 1.3, 초봉 $10만 = 높이 4.2
const ux = (u) => u * XS;

// ── 렌더러·빛 ─────────────────────────────────────────
const renderer = new THREE.WebGLRenderer({ canvas: root.querySelector("#gl"), antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(1920, 1080, false);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
const scene = new THREE.Scene(); scene.background = new THREE.Color(T.bg);
const camera = new THREE.PerspectiveCamera(24, 1920 / 1080, 0.1, 200);
scene.add(new THREE.HemisphereLight("#ffffff", "#c9c2b4", 1.4));
const sun = new THREE.DirectionalLight("#fff4e6", 1.8);
sun.position.set(-6, 14, 10); sun.target.position.set(6, 0, 2); sun.castShadow = true;
sun.shadow.mapSize.set(4096, 4096); sun.shadow.bias = -0.0004;
Object.assign(sun.shadow.camera, { left: -14, right: 14, top: 14, bottom: -14, near: 1, far: 50 });
scene.add(sun, sun.target);

// ── 바닥: 크림 + 평균선 오른쪽 위험 구역 ─────────────────
const ground = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({ color: T.ground, roughness: 1 }));
ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
const zoneMat = (c) => new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: 0, depthWrite: false });
const AVG = ux(P.avgU), XMAX = ux(9.5);
const danger = new THREE.Mesh(new THREE.PlaneGeometry(XMAX - AVG, 7), zoneMat(T.danger));
danger.rotation.x = -Math.PI / 2; danger.position.set((AVG + XMAX) / 2, 0.005, 1.6); scene.add(danger);
const safe = new THREE.Mesh(new THREE.PlaneGeometry(AVG, 7), zoneMat(T.safe));
safe.rotation.x = -Math.PI / 2; safe.position.set(AVG / 2, 0.005, 1.6); scene.add(safe);
const axis = new THREE.Mesh(new THREE.BoxGeometry(XMAX, 0.02, 0.05), new THREE.MeshBasicMaterial({ color: T.ink, transparent: true, opacity: 0 }));
axis.position.set(XMAX / 2, 0.012, 5.1); scene.add(axis);
const avgLine = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.02, 7.4), new THREE.MeshBasicMaterial({ color: T.ink, transparent: true, opacity: 0 }));
avgLine.position.set(AVG, 0.014, 1.5); scene.add(avgLine);
// 장면 2: 평균 초봉 높이의 얇은 유리판
const payPlane = new THREE.Mesh(new THREE.PlaneGeometry(XMAX, 7), new THREE.MeshBasicMaterial({ color: T.pay, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false }));
payPlane.rotation.x = -Math.PI / 2; payPlane.position.set(XMAX / 2, P.avgW * HW, 1.6); scene.add(payPlane);
const payLine = new THREE.Mesh(new THREE.BoxGeometry(XMAX + 0.6, 0.035, 0.035), new THREE.MeshBasicMaterial({ color: T.pay, transparent: true, opacity: 0 }));
payLine.position.set(XMAX / 2 - 0.3, P.avgW * HW, 4.8); scene.add(payLine);   // 판은 옅게, 앞 가장자리에 선 하나로 읽힌다
// 장면 2: 옆에서 보면 바닥의 평균선이 안 보이므로 4.2% 자리에 얇은 세로 벽을 세운다
const avgWall = new THREE.Mesh(new THREE.PlaneGeometry(7, 4.6), new THREE.MeshBasicMaterial({ color: T.ink, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false }));
avgWall.rotation.y = Math.PI / 2; avgWall.position.set(AVG, 2.3, 1.6); scene.add(avgWall);

// ── 건물: 캠퍼스 칸 → 실업률 축 위 벌떼 배치(겹치면 뒤 줄로) ──
const sorted = [...P.B].sort((a, b) => a.u - b.u), rows = [];
for (const b of sorted) {   // 같은 줄 안에서 가로로 FOOT+여유만큼 떨어질 때까지 뒤 줄로
  let r = 0; while ((rows[r] ?? -9) > ux(b.u) - (FOOT + 0.06)) r++;
  rows[r] = ux(b.u); b.ax = ux(b.u); b.az = 4.4 - r * GAP;
}
const COL = { base: new THREE.Color(T.base), red: new THREE.Color(T.bad), white: new THREE.Color(T.focus), green: new THREE.Color(T.good) };
const bld = {};
for (const b of P.B) {
  const mat = new THREE.MeshStandardMaterial({ color: COL.base.clone(), roughness: .75 });
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1).translate(0, 0.5, 0), mat);
  mesh.castShadow = mesh.receiveShadow = true; scene.add(mesh);
  bld[b.id] = { b, mesh, mat, tint: 0, kind: "base" };
}

// ── 카메라: 세 구도 사이를 섞는다 ───────────────────────
const K = P.CAMS || [
  { p: [17, 14, 19], t: [6.5, 0, 4] },          // 0 캠퍼스 내려다보기
  { p: [6.2, 10.5, 15.5], t: [6.2, 0, 2.2] },    // 1 실업률 축 정면 위
  { p: [6.2, 7.5, 19.5], t: [6.2, 1.6, 2.0] },   // 2 산점도: 앞에서 조금 높게(뒤 줄 건물이 가려지지 않게)
];
const cam = { k: 0, z: 1 };   // k = 구도 사이 위치(0~K.length-1), z = 대상 쪽으로 다가가는 비율(1 = 그대로)
const lerp = (a, b, t) => a + (b - a) * t;
function placeCamera() {
  const i = Math.min(K.length - 2, Math.floor(cam.k)), t = cam.k - i, A = K[i], Bk = K[i + 1];
  const tg = A.t.map((v, j) => lerp(v, Bk.t[j], t)), ps = A.p.map((v, j) => lerp(v, Bk.p[j], t));
  camera.position.set(...ps.map((v, j) => tg[j] + (v - tg[j]) * cam.z));
  camera.lookAt(...tg); camera.updateMatrixWorld();
}

// ── HTML: 눈금(투영) · 고정 카드 · 사분면 이름 ───────────
const v3 = new THREE.Vector3();
const TICKS = [...root.querySelectorAll(".tick")];
const pin = root.querySelector("#pin");
function project(x, y, z) { v3.set(x, y, z).project(camera); return [(v3.x + 1) / 2 * 1920, (1 - v3.y) / 2 * 1080]; }

const st = { mix: 0, grow: 0, zone: 0, tick: 0, pay: 0, pinId: "", pinOn: 0 };
function render() {
  const s = st.mix * st.mix * (3 - 2 * st.mix);   // smoothstep
  for (const id in bld) {
    const k = bld[id], b = k.b, d = Math.min(1, Math.max(0, s * 1.6 - b.delay));   // 건물마다 조금씩 늦게 출발
    const e = d * d * (3 - 2 * d);
    const x = lerp(b.gx * 0.95 + 0.5, k.b.ax, e), z = lerp(b.gy * 0.95 - 2, k.b.az, e);
    const w = lerp(0.78, FOOT, e), h = lerp(0.42, 0.28, e) + (b.w * HW - 0.28) * st.grow;
    k.mesh.position.set(x, 0, z); k.mesh.scale.set(w, Math.max(0.02, h), w);
    k.mat.color.copy(COL.base).lerp(COL[k.kind === "base" ? "base" : k.kind], k.tint);
  }
  danger.material.opacity = 0.75 * st.zone; safe.material.opacity = 0.55 * st.zone;
  axis.material.opacity = avgLine.material.opacity = st.zone;
  payPlane.material.opacity = 0.05 * st.pay; avgWall.material.opacity = 0.1 * st.pay; payLine.material.opacity = st.pay;
  placeCamera();
  for (const el of TICKS) {
    const [x, y] = project(+el.dataset.wx, +el.dataset.wy, +el.dataset.wz);
    el.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) translate(-50%, -50%)`;
  }
  const k = bld[st.pinId];
  if (k) { const p = k.mesh.position; const [x, y] = project(p.x, k.mesh.scale.y + 0.05, p.z); pin.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) translate(-50%, -100%)`; }
  pin.style.opacity = k ? st.pinOn : 0;
  renderer.render(scene, camera);
}
for (const b of P.B) b.delay = (b.gx + b.gy) / 22 * 0.6;

// ── 타임라인 ───────────────────────────────────────────
const tl = gsap.timeline({ paused: true, onUpdate: render });
// 장면 계획(P.TL): 생성기가 정한 {at, obj: "st"|"cam", to, d, ease}를 그대로 건다
const OBJ = { st, cam };
for (const s of P.TL) tl.to(OBJ[s.obj], { ...s.to, duration: s.d, ease: s.ease || "power2.inOut" }, s.at);
// 강조: 카드가 바뀔 때마다 그 건물만 색, 핀 하나만. id가 없으면 카드만
for (const h of P.HL) {
  const k = h.id ? bld[h.id] : null;
  if (k) {
    tl.set(k, { kind: h.kind }, h.t);
    tl.fromTo(k, { tint: 0 }, { tint: 1, duration: 0.35, ease: "power2.out", immediateRender: false }, h.t);
    if (!h.keep) tl.to(k, { tint: 0, duration: 0.3 }, h.e);
    tl.set(st, { pinId: h.id }, h.t);
    tl.fromTo(st, { pinOn: 0 }, { pinOn: 1, duration: 0.25, immediateRender: false }, h.t);
    tl.to(st, { pinOn: 0, duration: 0.2 }, h.e);
  }
  const card = root.querySelector("#" + h.card);
  tl.fromTo(card, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out", immediateRender: false }, h.t);
  tl.to(card, { opacity: 0, duration: 0.2 }, h.e);
}
for (const el of root.querySelectorAll(".fade"))
  tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, +el.dataset.in).to(el, { opacity: 0, duration: 0.3 }, +el.dataset.out);
for (const el of root.querySelectorAll(".grow"))   // 장표 그래프 막대: 제 시각에 기준선에서 자란다
  tl.fromTo(el, { scaleY: 0 }, { scaleY: 1, duration: 0.8, ease: "power2.out", immediateRender: false }, +el.dataset.in);
tl.to({}, { duration: 0.01 }, P.END - 0.01);
render();
window.__timelines["proto"] = tl;
