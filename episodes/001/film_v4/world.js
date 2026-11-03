// EP001 v4 — 책상 상판(바닥) 위 초록 매트, 그 위에 종이 소재가 서 있는 하나의 세계(2026-11-02 사용자 지시).
// 카메라는 모든 컷에서 한 자리에 고정(사용자 지시: 배경과 바닥은 고정). 컷이 바뀌면 소품만 바뀐다. 전환은 하드 컷뿐.
// 소품은 at 초에 바닥에서 일어선다(종이가 세워지는 움직임). 매끄러운 24fps, 스텝 없음(v3 떨림 원인 제거).
import { THREE, C, tag, box, matTex, tex, grain, paperTex } from './lib3d.js';

const clamp01 = x => Math.min(1, Math.max(0, x));
const outCubic = p => 1 - Math.pow(1 - p, 3);
const MAT_Y = 0.08;                       // 매트 윗면 높이
const ELEV = 10 * Math.PI / 180, DIST = 1.12, AIM = 6.43 * Math.PI / 180;   // 카메라 자리 앙각·거리 배율, 시선 아래 각도(책상 뒤끝이 화면 아래 4할 선에 오도록 계산)
const loader = new THREE.TextureLoader();
const srgb = t => { t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; };

function deskTex() {   // 밝은 원목 책상 상판(레퍼런스의 연한 오크): 가로 결 + 판재 이음선
  return tex(1024, 1024, (g, w, h) => {
    g.fillStyle = '#d2b48a'; g.fillRect(0, 0, w, h);
    let s = 5; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < 260; i++) { const y = rnd() * h; g.strokeStyle = `rgba(120,80,40,${0.04 + rnd() * 0.08})`; g.lineWidth = 1 + rnd() * 2;
      g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(w * 0.3, y + rnd() * 8 - 4, w * 0.7, y + rnd() * 8 - 4, w, y + rnd() * 6 - 3); g.stroke(); }
    g.fillStyle = 'rgba(110,70,35,.25)'; for (let y = 0; y < h; y += 256) g.fillRect(0, y, w, 2);   // 판재 이음선
    grain(g, w, h, 0.05, 3);
  });
}
function cutMatTex() {   // 커팅 매트: 가는 격자 + 5칸마다 조금 진한 선 + 가장자리 눈금 여백
  return tex(2048, 1536, (g, w, h) => {
    g.fillStyle = '#1f6a52'; g.fillRect(0, 0, w, h); grain(g, w, h, 0.10);
    const m = 70, step = (w - 2 * m) / 40;
    for (let i = 0; i <= 40; i++) { const x = m + i * step; g.strokeStyle = i % 5 ? 'rgba(170,215,190,.28)' : 'rgba(190,230,205,.55)'; g.lineWidth = i % 5 ? 1.2 : 2;
      g.beginPath(); g.moveTo(x, m); g.lineTo(x, h - m); g.stroke(); }
    for (let y = m; y <= h - m + 1; y += step) { const i = Math.round((y - m) / step); g.strokeStyle = i % 5 ? 'rgba(170,215,190,.28)' : 'rgba(190,230,205,.55)'; g.lineWidth = i % 5 ? 1.2 : 2;
      g.beginPath(); g.moveTo(m, y); g.lineTo(w - m, y); g.stroke(); }
  });
}

function shelfTex() {   // 밝은 서재(사용자 레퍼런스: 흰 책장·천장 조명·창, 강한 블러). 화면 위 6할을 채운다
  const W = 2048, H = 650, raw = tex(W, H, (g) => {
    let s = 11; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
    g.fillStyle = '#ece6da'; g.fillRect(0, 0, W, H);                                   // 벽
    g.fillStyle = '#f7f4ee'; g.fillRect(0, 0, W, 70);                                  // 천장
    [[520, 40], [1500, 30]].forEach(([x, y]) => { g.fillStyle = '#fffdf6'; g.beginPath(); g.ellipse(x, y, 130, 22, 0, 0, 7); g.fill(); });   // 천장등
    g.fillStyle = '#dcd5c8'; g.fillRect(1730, 120, 300, 420);                           // 창틀
    for (let y = 130; y < 530; y += 18) { g.fillStyle = y % 36 ? '#f4f1ea' : '#e2ddd2'; g.fillRect(1745, y, 270, 14); }   // 블라인드
    const X0 = 230, X1 = 1640, Y0 = 150, Y1 = 560, cw = 117, ch = 82;                   // 흰 책장(칸 격자)
    g.fillStyle = '#f9f7f2'; g.fillRect(X0, Y0, X1 - X0, Y1 - Y0);
    const tones = ['#c9a14a', '#6f8fb0', '#c8392e', '#5e7d4a', '#d9c7a0', '#8c3b2e', '#3a4a5c'];
    for (let y = Y0; y < Y1 - 10; y += ch) for (let x = X0; x < X1 - 10; x += cw) {
      g.fillStyle = '#e8e2d6'; g.fillRect(x + 8, y + 8, cw - 16, ch - 14);                // 칸 안쪽 그늘
      const r = rnd();
      if (r < 0.55) { let bx = x + 14 + rnd() * 20; const n = 3 + Math.floor(rnd() * 6);   // 책 몇 권
        for (let k = 0; k < n && bx < x + cw - 18; k++) { const bw = 6 + rnd() * 6, bh = 34 + rnd() * 26;
          g.fillStyle = tones[Math.floor(rnd() * tones.length)]; g.fillRect(bx, y + ch - 8 - bh, bw, bh); bx += bw + 1; } }
      else if (r < 0.7) { g.fillStyle = tones[Math.floor(rnd() * tones.length)]; g.fillRect(x + 35, y + ch - 36, 44, 28); }   // 상자·소품
    }
    g.fillStyle = '#d9c7a8'; g.fillRect(0, 560, W, H - 560);                           // 바닥(책상 뒤로 거의 가려짐)
  });
  return tex(W, H, (g) => { g.filter = 'blur(10px)'; g.drawImage(raw.image, -30, -30, W + 60, H + 60); });
}

function makeBase() {   // 책상 + 매트 + 빛. 모든 컷이 같은 바닥을 공유한다
  const g = new THREE.Group();
  const dt = deskTex(); dt.wrapS = dt.wrapT = THREE.RepeatWrapping; dt.repeat.set(3, 2);
  const desk = new THREE.Mesh(new THREE.BoxGeometry(70, 1.5, 38), new THREE.MeshStandardMaterial({ map: dt, roughness: 0.8 }));
  desk.position.set(0, -0.75, 5); desk.receiveShadow = true; g.add(desk);   // 매트 뒤로 조금만 이어지고 끝난다(뒤끝 z=-14)
  const mt = cutMatTex();
  const top = new THREE.MeshStandardMaterial({ map: mt, roughness: 1 }), edge = new THREE.MeshStandardMaterial({ color: '#1a5a45', roughness: 1 });
  // 매트는 실제 커팅 매트처럼 책상보다 작게: 둘레로 원목이 보여야 책상으로 읽힌다(사용자 지적: 격자 타일처럼 보임)
  const mat = new THREE.Mesh(new THREE.BoxGeometry(17, MAT_Y, 12.75), [edge, edge, top, edge, edge, edge]);
  mat.position.set(0, MAT_Y / 2, -1.6); mat.receiveShadow = true; g.add(mat);
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
  const Hm = p.w * H / W, mesh = new THREE.Mesh(new THREE.PlaneGeometry(p.w, Hm), m); mesh.castShadow = true;
  const s = stander(mesh, { lean: 12, ...p });
  if (p.enter === 'unroll') {   // 두루마리: 위끝 고정, 아래 롤이 굴러 내려가며 기사가 드러난다(2026-11-03 사용자 요청)
    t.repeat.y = 0.001; t.offset.y = 0.999;
    const roll = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, p.w * 1.01, 32), new THREE.MeshStandardMaterial({ map: paperTex(C.paper), roughness: 0.9 }));
    roll.rotation.z = Math.PI / 2; roll.castShadow = true; s.add(roll);
    const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, p.w * 1.04, 16), new THREE.MeshStandardMaterial({ color: '#8a6a45', roughness: 0.6 }));
    rod.rotation.z = Math.PI / 2; rod.position.set(0, Hm + 0.02, 0.06); rod.castShadow = true; s.add(rod);   // 위끝 막대: 걸린 두루마리로 읽히게
    s.userData.unroll = { mesh, roll, t, Hm, dur: p.dur ?? 0.9 };
  }
  return s;
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
    if (u.unroll) {   // 서 있는 채로, 위에서 아래로 펼친다
      const { mesh, roll, t, Hm, dur } = u.unroll, q = u.at < 0 ? 1 : outCubic(clamp01((tl - Math.max(0, u.at)) / dur)), sh = Math.max(0.001, q);
      o.visible = true; o.rotation.x = -u.lean;
      mesh.scale.y = sh; mesh.position.y = Hm * (1 - sh / 2);   // 위끝(Hm)은 그대로, 보이는 부분만 늘어난다
      t.repeat.y = sh; t.offset.y = 1 - sh;                    // 늘이지 않고 위쪽부터 잘라 보여 준다
      const r = 0.06 + 0.22 * (1 - q); roll.scale.set(r, 1, r); roll.position.set(0, Hm * (1 - sh), r + 0.02); roll.visible = q < 0.999;
      return;
    }
    const a = u.at <= 0 ? 1 : outCubic(clamp01((tl - u.at) / 0.45));
    o.visible = a > 0; o.rotation.x = -u.lean - (1 - a) * (Math.PI / 2 - u.lean);   // 누워 있다가 일어선다
  });
}

export function makeWorld(canvas, cuts) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  r.setPixelRatio(1); r.setSize(1920, 1080, false);
  r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.05; r.shadowMap.enabled = true;
  const cam = new THREE.PerspectiveCamera(30, 1920 / 1080, 0.1, 300), base = makeBase();
  // 고정 카메라: 책상 높이에 가깝게 두고 살짝만 내려다본다(사용자 지시: 책상 4할 + 배경 6할)
  const d = 15.3 * DIST;
  cam.position.set(0, 2.2 + d * Math.sin(ELEV), d * Math.cos(ELEV));
  cam.lookAt(0, cam.position.y - Math.sin(AIM) * 10, cam.position.z - Math.cos(AIM) * 10);
  // 책상 뒤끝 너머 화면 윗부분을 채우는 먼 책장. 카메라에 붙여 화면과 평행하게 둔다(깊이 75 = 책상보다 뒤)
  const shelf = new THREE.Mesh(new THREE.PlaneGeometry(82, 26), new THREE.MeshBasicMaterial({ map: shelfTex(), fog: false, toneMapped: false }));
  shelf.position.set(0, 8.5, -75); cam.add(shelf);   // 화면 위끝부터 책상 뒤끝 아래까지
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
