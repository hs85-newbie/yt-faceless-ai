// EP001 v4 — 책상 상판(바닥) 위 초록 매트, 그 위에 종이 소재가 서 있는 하나의 세계(2026-11-02 사용자 지시).
// 카메라는 모든 컷에서 한 자리에 고정(사용자 지시: 배경과 바닥은 고정). 컷이 바뀌면 소품만 바뀐다. 전환은 하드 컷뿐.
// 소품은 at 초에 바닥에서 일어선다(종이가 세워지는 움직임). 매끄러운 24fps, 스텝 없음(v3 떨림 원인 제거).
import { RoundedBoxGeometry } from './RoundedBoxGeometry.js';
import { THREE, C, FONT, tag, box, matTex, tex, grain, paperTex } from './lib3d.js';

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
  if (p.board) mesh.userData.board = true;   // 돋보기가 확대해 읽을 수 있는 판
  const s = stander(mesh, p); s.children[0].position.y += p.y || 0;   // y: 종이 막대에 꽂아 들어 올린 카드
  if (p.y && !p.nostick) { const st = box(0.09, p.y, 0.05, C.paper); st.position.set(0, p.y / 2, -0.03); s.add(st); }
  return s;
}
function doc(p) {       // 원문 캡처를 찢은 종이 한 장으로 세운다
  const img = new Image(); img.src = p.img;
  const k = p.crop, W = 1400, H = p.enter === 'laptop' ? 875 : Math.round(W * k.h / k.w);
  const t = tex(W, H, () => {});
  img.decode().then(() => {
    const g = t.image.getContext('2d');
    if (p.enter === 'laptop') {   // 16:10 노트북 화면: 브라우저 주소창 + 원문 캡처
      g.fillStyle = '#ffffff'; g.fillRect(0, 0, W, H);
      const bar = Math.round(H * 0.075);
      g.fillStyle = '#e9eaee'; g.fillRect(0, 0, W, bar);
      [['#ff5f57', 0], ['#febc2e', 1], ['#28c840', 2]].forEach(([c, i]) => { g.fillStyle = c; g.beginPath(); g.arc(bar * 0.6 + i * bar * 0.55, bar / 2, bar * 0.17, 0, 7); g.fill(); });
      g.fillStyle = '#ffffff'; const ux = bar * 2.6, uw = W - ux - bar * 0.8; g.beginPath(); g.roundRect(ux, bar * 0.2, uw, bar * 0.6, bar * 0.3); g.fill();
      g.fillStyle = '#5f6368'; g.font = `500 ${Math.round(bar * 0.36)}px -apple-system, "Helvetica Neue", sans-serif`; g.textBaseline = 'middle';
      g.fillText(p.url || 'libertystreeteconomics.newyorkfed.org', ux + bar * 0.4, bar / 2);
      const sc = W / k.w, ch = Math.min(H - bar, k.h * sc);
      g.drawImage(img, k.x, k.y, k.w, ch / sc, 0, bar, W, ch);
      if (p.hl) { g.globalCompositeOperation = 'multiply'; g.fillStyle = 'rgba(255,225,77,.55)'; g.fillRect((p.hl.x - k.x) * sc, bar + (p.hl.y - k.y) * sc, p.hl.w * sc, p.hl.h * sc); g.globalCompositeOperation = 'source-over'; }
      t.needsUpdate = true; return;
    }
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
  if (p.enter === 'laptop') {   // 실제 노트북 형태(2026-11-03 사용자: 종이 노트북 조악)
    const Ws = p.w, Hs = Ws * H / W, side = 0.16, top = 0.24, bot = 0.34, LW = Ws + 2 * side, LH = Hs + top + bot, LT = 0.09, BT = 0.17, D = LH * 0.72;
    const alu = new THREE.MeshStandardMaterial({ color: '#c8cbd0', metalness: 0.35, roughness: 0.42 });
    const g = new THREE.Group(); g.position.set(p.x || 0, MAT_Y, p.z || 0); g.rotation.y = (p.ry || 0) * Math.PI / 180;
    const base = new THREE.Mesh(new RoundedBoxGeometry(LW, BT, D, 4, 0.07), alu); base.position.set(0, BT / 2, D / 2); base.castShadow = base.receiveShadow = true; g.add(base);
    const well = new THREE.Mesh(new THREE.PlaneGeometry(LW * 0.9, D * 0.42), new THREE.MeshStandardMaterial({ color: '#2b2d31', roughness: 0.8 }));
    well.rotation.x = -Math.PI / 2; well.position.set(0, BT + 0.002, D * 0.28); g.add(well);
    const cols = 15, rows = 5, kw = (LW * 0.9) / cols, kd = (D * 0.42) / rows;
    const keys = new THREE.InstancedMesh(new RoundedBoxGeometry(kw * 0.82, 0.03, kd * 0.78, 2, 0.012), new THREE.MeshStandardMaterial({ color: '#17181b', roughness: 0.6 }), cols * rows);
    const mtx = new THREE.Matrix4(); let n = 0;
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) { mtx.makeTranslation(-LW * 0.45 + kw * (c + 0.5), BT + 0.016, D * 0.28 - D * 0.21 + kd * (r + 0.5)); keys.setMatrixAt(n++, mtx); }
    g.add(keys);
    const pad = new THREE.Mesh(new RoundedBoxGeometry(LW * 0.34, 0.006, D * 0.3, 2, 0.003), new THREE.MeshStandardMaterial({ color: '#bfc2c7', metalness: 0.3, roughness: 0.3 }));
    pad.position.set(0, BT + 0.003, D * 0.72); g.add(pad);
    const hinge = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, LW * 0.8, 20), new THREE.MeshStandardMaterial({ color: '#2b2d31', roughness: 0.5 }));
    hinge.rotation.z = Math.PI / 2; hinge.position.set(0, BT + 0.02, 0.02); g.add(hinge);
    const lid = new THREE.Group(); lid.position.set(0, BT, 0.02); g.add(lid);
    const shell = new THREE.Mesh(new RoundedBoxGeometry(LW, LH, LT, 4, 0.04), alu); shell.position.set(0, LH / 2, -LT / 2); shell.castShadow = true; lid.add(shell);
    const glass = new THREE.Mesh(new THREE.PlaneGeometry(LW - 0.02, LH - 0.02), new THREE.MeshStandardMaterial({ color: '#0c0d0f', roughness: 0.15, metalness: 0.1 }));
    glass.position.set(0, LH / 2, 0.002); lid.add(glass);
    const cam = new THREE.Mesh(new THREE.CircleGeometry(0.025, 16), new THREE.MeshBasicMaterial({ color: '#1f2a33' })); cam.position.set(0, LH - top / 2, 0.003); lid.add(cam);
    const screen = new THREE.Mesh(new THREE.PlaneGeometry(Ws, Hs), new THREE.MeshBasicMaterial({ map: t, toneMapped: false }));
    screen.position.set(0, bot + Hs / 2, 0.004); lid.add(screen);
    g.userData = { at: p.at ?? 0, laptop: { lid, screen } };
    return g;
  }
  const Hm = p.w * H / W, seg = p.enter === 'fold' ? [32, 24] : [1, 1];
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(p.w, Hm, seg[0], seg[1]), m); mesh.castShadow = true;
  const s = stander(mesh, { lean: 12, ...p });
  if (p.enter === 'fold') {   // 네 번 접힌 신문이 떨어진 뒤 위아래 → 좌우로 펼쳐진다. 크기는 그대로(2026-11-03 사용자: 구겨짐 어색)
    m.side = THREE.FrontSide;
    const back = new THREE.Mesh(mesh.geometry, new THREE.MeshStandardMaterial({ color: '#f4efe3', emissive: '#4a443a', roughness: 1, side: THREE.BackSide }));
    back.castShadow = true; mesh.add(back);   // 뒷면은 인쇄 없는 종이
    s.userData.fold = { mesh, flat: Float32Array.from(mesh.geometry.attributes.position.array), w: p.w, Hm };
  }
  return s;
}
function bar(p) {       // 종이 막대: at에 자라난다. v = 값, u = 값 1당 높이
  const b = box(p.wd || 1.8, 1, p.wd || 1.8, C[p.color] || p.color);
  const g = new THREE.Group(); g.add(b); g.position.set(p.x, MAT_Y, p.z || 0);
  g.userData = { bar: b, at: p.at ?? 0, h: p.v * p.u };
  return g;
}
function bubble(p) {    // 말풍선: 둥근 종이 + 아래쪽 꼬리(tail: 'left'|'right'). 화자는 꼬리 방향의 소품
  const lines = p.lines, size = p.size || 120, W = 1400;
  const m0 = document.createElement('canvas').getContext('2d'); m0.font = `800 ${size}px "Avenir Next Condensed", "DIN Condensed", sans-serif`;
  const tw = Math.max(...lines.map(l => m0.measureText(l).width)), w = Math.min(W, tw + 200), bh = lines.length * size * 1.15 + 140, h = bh + 120;
  const t = tex(w, h, (g) => {
    const r = 70; g.fillStyle = '#fbf8f0'; g.strokeStyle = '#1a1a1a'; g.lineWidth = 10;
    g.beginPath(); g.moveTo(r, 8); g.arcTo(w - 8, 8, w - 8, bh, r); g.arcTo(w - 8, bh, 8, bh, r);
    const tx = p.tail === 'right' ? w * 0.72 : w * 0.22, dir = p.tail === 'right' ? 1 : -1;
    g.lineTo(tx + 60, bh); g.lineTo(tx + dir * 90, h - 10); g.lineTo(tx - 20, bh);
    g.arcTo(8, bh, 8, 8, r); g.arcTo(8, 8, w - 8, 8, r); g.closePath(); g.fill(); g.stroke();
    grain(g, w, h, 0.05); g.fillStyle = '#1a1a1a'; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.font = `800 ${size}px "Avenir Next Condensed", "DIN Condensed", sans-serif`;
    lines.forEach((l, i) => g.fillText(l, w / 2, bh / 2 + (i - (lines.length - 1) / 2) * size * 1.15 + size * 0.06));
  });
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(p.h * w / h, p.h), new THREE.MeshStandardMaterial({ map: t, alphaTest: 0.5, roughness: 1, side: THREE.DoubleSide }));
  mesh.castShadow = true; const st = stander(mesh, p); st.children[0].position.y += p.y || 0; return st;
}
function timeline(p) {  // 종이 연표 띠(두 막대에 꽂힘): 가로선 + 연도 눈금. 돋보기가 확대해 읽는 판
  const yrs = p.years, W = 2400, H = 480, m = 170, step = (W - 2 * m) / (yrs.length - 1), ly = H * 0.4;
  const t = tex(W, H, (g) => {
    g.beginPath(); g.moveTo(10, 16);
    for (let x = 10; x < W - 10; x += 40) g.lineTo(x, 8 + (x * 7 % 11));
    g.lineTo(W - 8, H - 12);
    for (let x = W - 10; x > 10; x -= 40) g.lineTo(x, H - 6 - (x * 5 % 9));
    g.closePath(); g.fillStyle = C.paper; g.fill(); grain(g, W, H, 0.08);
    g.strokeStyle = g.fillStyle = C.ink; g.lineWidth = 10;
    g.beginPath(); g.moveTo(m - 80, ly); g.lineTo(W - m + 70, ly); g.stroke();
    g.beginPath(); g.moveTo(W - m + 110, ly); g.lineTo(W - m + 55, ly - 30); g.lineTo(W - m + 55, ly + 30); g.fill();   // 화살표 머리
    g.textAlign = 'center'; g.textBaseline = 'middle'; g.font = `800 104px ${FONT}`; g.lineWidth = 8;
    yrs.forEach((y, i) => { const x = m + i * step; g.beginPath(); g.moveTo(x, ly - 42); g.lineTo(x, ly + 42); g.stroke(); g.fillText(String(y), x, H * 0.74); });
  });
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(p.w, p.w * H / W), new THREE.MeshStandardMaterial({ map: t, alphaTest: 0.5, roughness: 1, side: THREE.DoubleSide }));
  mesh.castShadow = true; mesh.userData.board = true;
  const s = stander(mesh, { lean: 0, ...p }); s.children[0].position.y += p.y || 0;
  [-0.36, 0.36].forEach(f => { const st = box(0.09, p.y, 0.05, C.paper); st.position.set(f * p.w, p.y / 2, -0.03); s.add(st); });
  return s;
}
// 3D 돋보기(2026-11-03 사용자: 종이 이미지 렌즈가 깨짐). keys = [{at,x,y,z}] 렌즈 중심 경로, 구절마다 0.5초에 미끄러져 옮겨 간다.
// 렌즈 안은 시선이 뒤 판(board)에 닿는 자리를 zoom배 확대한 그림 → 실제 돋보기처럼 읽힌다
function magnifier(p) {
  const R = p.r || 0.75, Rg = R - 0.08, g = new THREE.Group();
  const rim = new THREE.Mesh(new THREE.TorusGeometry(R, 0.11, 20, 72), new THREE.MeshStandardMaterial({ map: paperTex(C.mustard), roughness: 0.7 }));
  rim.castShadow = true; g.add(rim);
  const inner = new THREE.Mesh(new THREE.TorusGeometry(Rg - 0.02, 0.035, 12, 72), new THREE.MeshStandardMaterial({ color: C.paper, roughness: 0.8 }));
  inner.position.z = 0.05; g.add(inner);
  const hl = 1.15, d = new THREE.Vector2(Math.SQRT1_2, -Math.SQRT1_2);   // 손잡이는 오른쪽 아래로
  const handle = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.12, hl, 24), new THREE.MeshStandardMaterial({ map: paperTex('#d39a3a'), roughness: 0.7 }));
  handle.rotation.z = -3 * Math.PI / 4; handle.position.set(d.x * (R + 0.06 + hl / 2), d.y * (R + 0.06 + hl / 2), 0); handle.castShadow = true; g.add(handle);
  const zoom = new THREE.Mesh(new THREE.CircleGeometry(Rg, 72), new THREE.MeshStandardMaterial({ transparent: true, alphaTest: 0.5, roughness: 1 }));
  zoom.visible = false; g.add(zoom);
  const glass = new THREE.Mesh(new THREE.CircleGeometry(Rg, 72), new THREE.MeshStandardMaterial({ color: '#d6e6ec', transparent: true, opacity: 0.18, roughness: 0.05, depthWrite: false }));
  glass.position.z = 0.01; g.add(glass);
  const shine = new THREE.Mesh(new THREE.RingGeometry(Rg * 0.6, Rg * 0.74, 40, 1, Math.PI * 0.58, Math.PI * 0.32), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0.5, depthWrite: false }));
  shine.position.z = 0.02; g.add(shine);   // 유리 반사 한 줄
  g.userData = { mag: { keys: p.keys, zoom, R: Rg, M: p.zoom || 1.8, maps: {} } };
  return g;
}
const ray = new THREE.Raycaster(), v3 = new THREE.Vector3(), v2 = new THREE.Vector2();
function updateLens(s, cam) {   // 렌즈 중심을 지나는 시선이 닿은 판의 그 자리를 확대해 렌즈에 붙인다
  s.updateMatrixWorld();
  s.userData.props.forEach(o => {
    const m = o.userData.mag; if (!m || !o.visible) return;
    m.zoom.getWorldPosition(v3).project(cam); ray.setFromCamera(v2.set(v3.x, v3.y), cam);
    const hit = ray.intersectObjects(s.userData.boards, false)[0];
    m.zoom.visible = !!hit; if (!hit) return;
    const b = hit.object, map = m.maps[b.uuid] ||= Object.assign(b.material.map.clone(), { needsUpdate: true });
    if (m.zoom.material.map !== map) { m.zoom.material.map = map; m.zoom.material.needsUpdate = true; }
    const D = 2 * m.R; map.repeat.set(D / (b.geometry.parameters.width * m.M), D / (b.geometry.parameters.height * m.M));
    map.offset.set(hit.uv.x - map.repeat.x / 2, hit.uv.y - map.repeat.y / 2);
  });
}
const MAKE = { cutout, card, doc, bar, bubble, timeline, magnifier };

function poseProps(props, tl) {
  props.forEach(o => {
    const u = o.userData;
    // at < 0: 앞 컷에서 이어진 것(완성 상태로 둠). at = 0: 컷 시작부터 서 있음. at > 0: 그 구절에서 일어서거나 자람
    if (u.bar) { const g = u.at < 0 ? 1 : outCubic(clamp01((tl - u.at) / 0.9)), h = Math.max(0.01, u.h * g);
      u.bar.scale.y = h; u.bar.position.y = h / 2; o.visible = g > 0; return; }
    if (u.mag) {    // 경로를 따라 미끄러짐(앞 이동이 끝나기 전에 다음 구절이 오면 지금 자리에서 이어 간다) + 손에 든 듯한 아주 작은 흔들림
      const k = u.mag.keys; o.visible = tl >= k[0].at; o.position.set(k[0].x, k[0].y, k[0].z);
      for (let i = 1; i < k.length && tl >= k[i].at; i++) o.position.lerp(v3.set(k[i].x, k[i].y, k[i].z), outCubic(clamp01((tl - k[i].at) / (k[i].dur || 0.5))));
      o.position.y += 0.03 * Math.sin(tl * 4.2); o.rotation.z = 0.04 * Math.sin(tl * 2.7);
      return;
    }
    if (u.laptop) {
      const t0 = u.at < 0 ? 99 : tl - Math.max(0, u.at), q = outCubic(clamp01(t0 / 0.5)), on = clamp01((t0 - 0.35) / 0.2);
      o.visible = true; u.laptop.lid.rotation.x = Math.PI / 2 * (1 - q) - 0.33 * q;   // 덮인 상태 → 12° 뒤로 젖힘
      u.laptop.screen.material.color.setScalar(0.04 + 0.96 * on);
      return;
    }
    if (u.fold) {   // 0~0.25초 떨어짐, 0.25~0.6초 윗장 펼침, 0.6~0.95초 오른장 펼침
      const { mesh, flat, w, Hm } = u.fold, t0 = u.at < 0 ? 99 : tl - Math.max(0, u.at);
      const drop = outCubic(clamp01(t0 / 0.25)), a2 = Math.PI * (1 - outCubic(clamp01((t0 - 0.25) / 0.35))), a1 = Math.PI * (1 - outCubic(clamp01((t0 - 0.6) / 0.35)));
      o.visible = t0 >= 0; o.rotation.x = -u.lean;
      const pos = mesh.geometry.attributes.position;
      for (let i = 0; i < pos.count; i++) {
        let x = flat[i * 3], y = flat[i * 3 + 1], z = 0;
        if (x > 0) { z = x * Math.sin(a1) + 0.004 * (a1 / Math.PI); x = x * Math.cos(a1); }   // 오른쪽 반을 앞으로 접음
        if (y > 0) { const yy = y * Math.cos(a2) - z * Math.sin(a2), zz = y * Math.sin(a2) + z * Math.cos(a2) + 0.008 * (a2 / Math.PI); y = yy; z = zz; }   // 윗 반을 앞으로 접음
        pos.array[i * 3] = x; pos.array[i * 3 + 1] = y; pos.array[i * 3 + 2] = z;
      }
      pos.needsUpdate = true; mesh.geometry.computeVertexNormals();
      mesh.position.x = (w / 4) * (a1 / Math.PI);                     // 접힌 동안 가운데로
      mesh.position.y = Hm / 2 + (1 - drop) * 3;                      // 아랫반이 매트에 닿는다
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
    s.userData.boards = []; s.traverse(o => { if (o.userData.board) s.userData.boards.push(o); });
    return s;
  });
  return { render(i, t) {
    const c = cuts[i], s = scenes[i], tl = t - c.t;
    if (base.parent !== s) s.add(base);
    poseProps(s.userData.props, tl);
    if (cam.parent !== s) s.add(cam);
    updateLens(s, cam);
    r.render(s, cam);
  } };
}
