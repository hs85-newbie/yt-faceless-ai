// EP001 본편 v3 — 컷 시간표(cuts.json)를 받아 t초의 한 프레임을 그린다. 페이지 계약: window.DUR, window.render(t), window.READY
// 종이 요소는 2프레임마다 한 번 움직인다(12fps 스텝, vox-explainer 규칙). 3D 카메라만 매끄럽게 움직인다.
import { makeStage } from './scenes3d.js';

const step = t => Math.floor(t * 12) / 12;
const ease = p => p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
const clamp01 = x => Math.min(1, Math.max(0, x));
const el = (tag, cls, css = '', html = '') => { const e = document.createElement(tag); if (cls) e.className = cls; e.style.cssText = css; e.innerHTML = html; return e; };

function strip(s) {   // {text, x, y, size, rot, cls, at}
  const e = el('div', 'strip ' + (s.cls || ''), `left:${s.x}px;top:${s.y}px;font-size:${s.size || 64}px`, s.text);
  e.dataset.at = s.at ?? 0; e.dataset.rot = s.rot ?? 0; return e;
}
function addStrips(root, list = []) { list.forEach(s => root.appendChild(strip(s))); }
function sig(root, c) {
  if (c.src) root.appendChild(el('div', 'src', '', 'Source: ' + c.src));
  if (c.est) root.appendChild(el('div', 'chip', 'left:40px;bottom:84px;top:auto', 'ESTIMATE'));
  // 구석 채널명은 넣지 않는다(motionmaxxing G5 C1·C2). 채널명은 엔드카드에만
}

const BUILD = {
  collage(c, r) { const bg = el('div', 'bg', `background-image:url(${c.img})`); r.appendChild(bg); r._cam = bg; },
  print(c, r) {   // 옛 컷아웃을 흰 테두리 사진으로 매트에 붙인다(검은 여백 대신)
    r.appendChild(el('div', 'mat')); const f = el('div', 'print', `left:${c.px ?? 380}px;top:${c.py ?? 150}px;transform:rotate(${c.prot ?? -2}deg)`);
    f.appendChild(el('img', '', `width:${c.pw ?? 900}px`)).src = c.img; r.appendChild(f);
    r.appendChild(el('div', 'tape', `left:${(c.px ?? 380) + 40}px;top:${(c.py ?? 150) - 18}px;transform:rotate(-14deg)`)); r._cam = f; },
  doc(c, r) {     // 원문 캡처를 찢은 종이로: 표시 상자 주변만 잘라 크게, 형광펜이 왼쪽에서 그어진다
    r.appendChild(el('div', c.desk ? 'bg' : 'mat', c.desk ? 'background-image:url(sb3_document.png)' : ''));
    const m = c.mark, pad = 70, x0 = Math.max(0, m.x - pad), y0 = Math.max(0, m.y - pad * 1.6), w0 = Math.min(1920 - x0, m.w + pad * 2), h0 = Math.min(1080 - y0, m.h + pad * 3.2);
    const k = Math.min(1300 / w0, 720 / h0), W = w0 * k, H = h0 * k;
    const d = el('div', 'doc', `left:${(1920 - W) / 2}px;top:${(1080 - H) / 2 - 20}px;width:${W}px;height:${H}px;transform:rotate(${c.rot ?? -1.2}deg)`);
    const img = el('img', '', `position:absolute;left:${-x0 * k}px;top:${-y0 * k}px;width:${1920 * k}px`); img.src = c.img; d.appendChild(img);
    const hl = el('div', 'hlbar', `left:${(m.x - x0) * k}px;top:${(m.y - y0) * k}px;height:${m.h * k}px;width:${m.w * k}px`); hl.dataset.at = c.hlAt ?? 0.6; d.appendChild(hl);
    r.appendChild(d); r._cam = d;
  },
  kin(c, r) { r.appendChild(el('div', c.bg === 'paper' ? 'paperbg' : c.bg === 'red' ? 'redbg' : 'mat')); r._cam = r; },   // 글자 카드도 카메라가 종이 위를 민다
  gl(c, r) { r._gl = true; },
  end(c, r) { r.appendChild(el('div', 'mat')); const e = el('div', 'endcard', '', 'COUNTER LEDGER<small>data, not drama</small>'); e.dataset.at = 0.05; r.appendChild(e); },
};

function build(c) {
  const r = el('div', 'cut'); BUILD[c.k](c, r);
  if (c.stamp) { const s = el('div', 'stamp', `left:${c.stamp.x}px;top:${c.stamp.y}px;font-size:${c.stamp.size || 56}px`, c.stamp.text); s.dataset.at = c.stamp.at ?? 0; s.dataset.rot = -7; r.appendChild(s); }
  addStrips(r, c.strips); if (c.k !== 'end') sig(r, c);
  document.getElementById('dom').appendChild(r); return r;
}

// 등장: at 이후 0.25초 동안 위에서 떨어져 자리 잡음(스텝)
// 자리 잡은 뒤에도 종이가 아주 조금 흔들린다(멈춘 화면 방지, motionmaxxing 법칙 8)
function animate(r, tl) {
  r.querySelectorAll('[data-at]').forEach((e, k) => {
    const a = clamp01((tl - +e.dataset.at) / 0.25), rot = +e.dataset.rot || 0;
    if (e.classList.contains('hlbar')) { e.style.clipPath = `inset(0 ${100 - a * 100}% 0 0)`; return; }
    e.style.opacity = a > 0 ? 1 : 0;
    const sway = a * 0.7 * Math.sin(tl * 1.1 + k * 1.7), bob = a * 4 * Math.sin(tl * 0.9 + k);
    e.style.transform = `translateY(${(1 - a) * -70 + bob}px) rotate(${rot + (1 - a) * 7 + sway}deg) scale(${1 + (1 - a) * 0.12})`;
  });
}
function camMove(r, c, p) {   // 켄 번스: cam = [s0, x0, y0, s1, x1, y1]
  if (!r._cam) return; const [s0, x0, y0, s1, x1, y1] = c.cam || (c.k === 'kin' ? [1.0, 0, 0, 1.1, -50, -22] : [1.0, 0, 0, 1.14, -60, -26]), q = ease(p);
  const base = r._cam.classList.contains('doc') ? ` rotate(${c.rot ?? -1.2}deg)` : '';
  r._cam.style.transform = `translate(${x0 + (x1 - x0) * q}px, ${y0 + (y1 - y0) * q}px) scale(${s0 + (s1 - s0) * q})` + base;
}

// 전환: 다음 컷 경계 앞뒤 0.25초. 바뀌는 순간은 경계 그 자체
const TW = 0.25;
function transition(cuts, i, t) {
  const cam = document.getElementById('cam'), wipe = document.getElementById('wipe'), rip = document.getElementById('rip');
  cam.style.transform = ''; cam.style.filter = ''; wipe.style.transform = 'translateX(-130%)'; rip.style.transform = 'translateX(-150%) rotate(-12deg)';
  const cur = cuts[i], nxt = cuts[i + 1];
  let tr, u;   // u: -1(경계 직전) ~ +1(경계 직후)
  if (t - cur.t < TW && i > 0) { tr = cur.tr; u = (t - cur.t) / TW; } else if (nxt && nxt.t - t < TW) { tr = nxt.tr; u = -(nxt.t - t) / TW; } else return;
  const a = (u + 1) / 2;
  if (tr === 'wipe') wipe.style.transform = `translateX(${-130 + a * 260}%)`;
  else if (tr === 'rip') rip.style.transform = `translateX(${-150 + a * 300}%) rotate(-12deg)`;
  else if (tr === 'whip') { cam.style.transform = `translateX(${-u * 38}%)`; cam.style.filter = `blur(${(1 - Math.abs(u)) * 14}px)`; }
  else if (tr === 'punch') cam.style.transform = `scale(${u < 0 ? 1 + (1 + u) * 0.18 : 0.88 + u * 0.12})`;
  else if (tr === 'drop' && u > 0) cam.style.transform = `translateY(${(1 - ease(u)) * -100}%)`;
}

export async function start() {
  const { cuts } = await (await fetch('cuts.json')).json();
  const stage = makeStage(document.getElementById('gl'));
  const roots = cuts.map(build);
  const srcs = [...new Set(cuts.flatMap(c => [c.img, c.desk && 'sb3_document.png']).filter(Boolean))];
  await Promise.all(srcs.map(s => { const im = new Image(); im.src = s; return im.decode().catch(() => console.error('missing ' + s)); }));
  await document.fonts.ready;
  window.DUR = cuts.at(-1).t + cuts.at(-1).d;
  let shown = -1;
  window.render = t => {
    let i = cuts.findIndex(c => t < c.t + c.d); if (i < 0) i = cuts.length - 1;
    const c = cuts[i], r = roots[i], tl = step(t - c.t), p = clamp01(tl / c.d);
    if (shown !== i) { roots.forEach((x, k) => x.classList.toggle('on', k === i)); shown = i; }
    document.getElementById('gl').style.visibility = r._gl ? 'visible' : 'hidden';
    if (r._gl) stage.render(c.scene, clamp01((t - c.t) / c.d), t - c.t, c.opt || {});
    animate(r, tl); camMove(r, c, p); transition(cuts, i, t);
  };
  window.render(0); window.READY = true;
}
