// EP001 v4 — 책상 상판(바닥) 위 초록 매트, 그 위에 종이 소재가 서 있는 하나의 세계(2026-11-02 사용자 지시).
// 카메라는 모든 컷에서 한 자리에 고정(사용자 지시: 배경과 바닥은 고정). 컷이 바뀌면 소품만 바뀐다. 전환은 하드 컷뿐.
// 소품은 at 초에 바닥에서 일어선다(종이가 세워지는 움직임). 매끄러운 24fps, 스텝 없음(v3 떨림 원인 제거).
import { THREE, C, tag, box, matTex, tex, grain } from './lib3d.js';

const clamp01 = x => Math.min(1, Math.max(0, x));
const outCubic = p => 1 - Math.pow(1 - p, 3);
const MAT_Y = 0.08;                       // 매트 윗면 높이
const ELEV = 26 * Math.PI / 180, DIST = 1.12;   // 모든 컷 공통 카메라 앙각·거리 배율
const loader = new THREE.TextureLoader();
const srgb = t => { t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; };

function deskTex() {   // 나무 책상 상판: 결 무늬
  return tex(1024, 1024, (g, w, h) => {
    g.fillStyle = '#7a5236'; g.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 3) { g.fillStyle = `rgba(${40 + (y * 13) % 30},20,10,${0.06 + ((y * 7) % 11) / 120})`; g.fillRect(0, y, w, 2); }
    grain(g, w, h, 0.12, 3);
  });
}

function shelfTex() {   // 멀리 있는 서재 책장(레퍼런스: 탁상 촬영의 흐린 배경 — 여러 단, 작은 책등, 선반 줄, 강한 블러)
  const W = 2048, H = 400, raw = tex(W, H, (g) => {
    g.fillStyle = '#2e2118'; g.fillRect(0, 0, W, H);
    let s = 11; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
    const spines = ['#8c3b2e', '#2f4a5c', '#c9a14a', '#e8dfcc', '#4f6b3a', '#6a3a4a', '#b46a3a', '#3a3a3a', '#d9c7a0'];
    for (let y0 = -20; y0 < H; y0 += 62) {                  // 단 높이 62px ≈ 프레임 안 3~4단
      for (let x = 0; x < W;) {
        if (x % 420 < 12) { x += 12; continue; }              // 칸막이(세로 판) 자리
        if (rnd() < 0.04) { x += 30 + rnd() * 40; continue; }
        const bw = 5 + rnd() * 5, bh = 44 * (0.7 + rnd() * 0.3);
        g.fillStyle = spines[Math.floor(rnd() * spines.length)]; g.fillRect(x, y0 + 52 - bh, bw, bh); x += bw + 1;
      }
      g.fillStyle = '#5a3d27'; g.fillRect(0, y0 + 52, W, 8);   // 선반 판
    }
    g.fillStyle = '#4a3222'; for (let x = 0; x < W; x += 420) g.fillRect(x, 0, 12, H);   // 칸막이
    for (let i = 0; i < 14; i++) { const x = rnd() * W, y = rnd() * H, r = 8 + rnd() * 18;   // 보케(불빛·책 등 반사)
      const b = g.createRadialGradient(x, y, 0, x, y, r); b.addColorStop(0, 'rgba(255,220,160,.5)'); b.addColorStop(1, 'rgba(255,220,160,0)');
      g.fillStyle = b; g.fillRect(x - r, y - r, 2 * r, 2 * r); }
  });
  return tex(W, H, (g) => { g.filter = 'blur(9px) brightness(0.82)'; g.drawImage(raw.image, -20, -20, W + 40, H + 40); });
}

function makeBase() {   // 책상 + 매트 + 빛. 모든 컷이 같은 바닥을 공유한다
  const g = new THREE.Group();
  const dt = deskTex(); dt.wrapS = dt.wrapT = THREE.RepeatWrapping; dt.repeat.set(6, 6);
  const desk = new THREE.Mesh(new THREE.BoxGeometry(70, 1.5, 38), new THREE.MeshStandardMaterial({ map: dt, roughness: 0.8 }));
  desk.position.set(0, -0.75, 5); desk.receiveShadow = true; g.add(desk);   // 매트 뒤로 조금만 이어지고 끝난다(뒤끝 z=-14)
  const mt = matTex();
  const top = new THREE.MeshStandardMaterial({ map: mt, roughness: 1 }), edge = new THREE.MeshStandardMaterial({ color: '#174a3d', roughness: 1 });
  const mat = new THREE.Mesh(new THREE.BoxGeometry(34, MAT_Y, 20), [edge, edge, top, edge, edge, edge]);
  mat.position.y = MAT_Y / 2; mat.receiveShadow = true; g.add(mat);
  g.add(new THREE.HemisphereLight('#fff4e2', '#3a2a1e', 1.25));
  const key = new THREE.DirectionalLight('#ffe9cc', 2.8); key.position.set(-9, 16, 10); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048); Object.assign(key.shadow.camera, { left: -18, right: 18, top: 14, bottom: -14, far: 60 });
  key.shadow.radius = 5; key.shadow.bias = -0.0005; g.add(key);
  return g;
}

// 아래 모서리를 축으로 일어서는 소품. h = 높이(월드 단위), lean = 뒤로 기운 각도
function stander(mesh, p) {
  const pivot = new THREE.Group(); mesh.position.y = mesh.geometry.parameters.height / 2; pivot.add(mesh);
  pivot.position.set(p.x || 0, MAT_Y + 0.01, p.z || 0); pivot.rotation.y = (p.ry || 0) * Math.PI / 180;
  pivot.userData = { at: p.at ?? 0, lean: (p.lean ?? 4) * Math.PI / 180 };
  return pivot;
}
function cutout(p) {    // 투명 배경 종이 조각
  const t = srgb(loader.load(p.img)), m = new THREE.MeshStandardMaterial({ map: t, alphaTest: 0.5, roughness: 1, side: THREE.DoubleSide });
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(p.h * p.ar, p.h), m); mesh.castShadow = true; mesh.receiveShadow = true;
  return stander(mesh, p);
}
function card(p) {      // 서 있는 글자 카드
  const lines = p.lines.map(l => typeof l === 'string' ? { text: l } : l);
  const mesh = tag(lines, p.h || 1.0, { bg: p.bg ? C[p.bg] || p.bg : C.paper, fg: p.fg ? C[p.fg] || p.fg : C.ink, size: p.size || 150 });
  mesh.material.alphaTest = 0.5; mesh.material.transparent = false;
  const s = stander(mesh, p); s.children[0].position.y += p.y || 0;   // y: 종이 막대에 꽂아 들어 올린 카드
  if (p.y) { const st = box(0.09, p.y, 0.05, C.paper); st.position.set(0, p.y / 2, -0.03); s.add(st); }
  return s;
}
function doc(p) {       // 원문 캡처를 찢은 종이 한 장으로 세운다
  const img = new Image(); img.src = p.img;
  const k = p.crop, W = 1400, H = Math.round(W * k.h / k.w);
  const t = tex(W, H, () => {});
  img.decode().then(() => {
    const g = t.image.getContext('2d');
    g.beginPath(); g.moveTo(0, 18);
    for (let x = 0; x <= W; x += 28) g.lineTo(x, 6 + ((x * 7) % 17));
    for (let y = 0; y <= H; y += 28) g.lineTo(W - 4 - ((y * 5) % 9), y);
    for (let x = W; x >= 0; x -= 28) g.lineTo(x, H - 6 - ((x * 3) % 15));
    g.closePath(); g.save(); g.clip();
    g.fillStyle = '#fff'; g.fillRect(0, 0, W, H);
    g.drawImage(img, k.x, k.y, k.w, k.h, 0, 0, W, H);
    if (p.hl) { g.globalCompositeOperation = 'multiply'; g.fillStyle = 'rgba(255,225,77,.55)';
      g.fillRect((p.hl.x - k.x) * W / k.w, (p.hl.y - k.y) * H / k.h, p.hl.w * W / k.w, p.hl.h * H / k.h); }
    g.restore(); t.needsUpdate = true;
  });
  const m = new THREE.MeshStandardMaterial({ map: t, alphaTest: 0.5, roughness: 0.9, side: THREE.DoubleSide });
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(p.w, p.w * H / W), m); mesh.castShadow = true;
  return stander(mesh, { lean: 12, ...p });
}
function bar(p) {       // 종이 막대: at에 자라난다. v = 값, u = 값 1당 높이
  const b = box(p.wd || 1.8, 1, p.wd || 1.8, C[p.color] || p.color);
  const g = new THREE.Group(); g.add(b); g.position.set(p.x, MAT_Y, p.z || 0);
  g.userData = { bar: b, at: p.at ?? 0, h: p.v * p.u };
  return g;
}
const MAKE = { cutout, card, doc, bar };

function poseProps(props, tl) {
  props.forEach(o => {
    const u = o.userData;
    // at < 0: 앞 컷에서 이어진 것(완성 상태로 둠). at = 0: 컷 시작부터 서 있음. at > 0: 그 구절에서 일어서거나 자람
    if (u.bar) { const g = u.at < 0 ? 1 : outCubic(clamp01((tl - u.at) / 0.9)), h = Math.max(0.01, u.h * g);
      u.bar.scale.y = h; u.bar.position.y = h / 2; o.visible = g > 0; return; }
    const a = u.at <= 0 ? 1 : outCubic(clamp01((tl - u.at) / 0.45));
    o.visible = a > 0; o.rotation.x = -u.lean - (1 - a) * (Math.PI / 2 - u.lean);   // 누워 있다가 일어선다
  });
}

export function makeWorld(canvas, cuts) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  r.setPixelRatio(1); r.setSize(1920, 1080, false);
  r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.05; r.shadowMap.enabled = true;
  const cam = new THREE.PerspectiveCamera(30, 1920 / 1080, 0.1, 300), base = makeBase();
  // 고정 카메라: 매트 중앙(0, 2.2, 0)을 앙각 ELEV로 내려다본다
  const tgt = new THREE.Vector3(0, 2.2, 0), d = 15.3 * DIST;
  cam.position.set(0, tgt.y + d * Math.sin(ELEV), d * Math.cos(ELEV)); cam.lookAt(tgt);
  // 책상 뒤끝 너머 화면 윗부분을 채우는 먼 책장. 카메라에 붙여 화면과 평행하게 둔다(깊이 75 = 책상보다 뒤)
  const shelf = new THREE.Mesh(new THREE.PlaneGeometry(82, 16.4), new THREE.MeshBasicMaterial({ map: shelfTex(), fog: false }));
  shelf.position.set(0, 13.2, -75); cam.add(shelf);
  const scenes = cuts.map(c => {
    const s = new THREE.Scene(); s.background = new THREE.Color('#2a1d14'); s.fog = new THREE.Fog('#2a1d14', 30, 70);
    s.userData.props = (c.props || []).map(p => { const o = MAKE[p.t](p); s.add(o); return o; });
    return s;
  });
  return { render(i, t) {
    const c = cuts[i], s = scenes[i], tl = t - c.t;
    if (base.parent !== s) s.add(base);
    poseProps(s.userData.props, tl);
    if (cam.parent !== s) s.add(cam);
    r.render(s, cam);
  } };
}
