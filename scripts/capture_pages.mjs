// 원문 페이지를 1920×1080(및 긴 페이지 전체)으로 캡처하고, 형광펜 문구마다 그 문구가 보이는 화면과 좌표를 기록한다.
// 사용: cd ~/lemo-opuscar && node <repo>/scripts/capture_pages.mjs <repo>/episodes/001/pages.json <repo>/output/001/pages
import fs from 'fs'; import path from 'path';
import { chromium } from '/Users/cjons/lemo-opuscar/node_modules/playwright-core/index.mjs';

const [specPath, outDir] = process.argv.slice(2);
const pages = JSON.parse(fs.readFileSync(specPath, 'utf8'));
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1, locale: 'en-US',
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0 Safari/537.36' });
for (const p of pages) {
  const page = await ctx.newPage();
  try {
    await page.goto(p.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(2500);
    // 쿠키 배너가 가리면 품질이 떨어진다: 거부·닫기 버튼만 누른다(동의는 누르지 않음)
    for (const sel of ['button:has-text("Reject")', 'button:has-text("Decline")', 'button:has-text("Close")', '[aria-label="Close"]']) {
      const b = page.locator(sel).first(); if (await b.count() && await b.isVisible().catch(() => false)) { await b.click({ timeout: 1500 }).catch(() => {}); break; }
    }
    await page.screenshot({ path: path.join(outDir, `${p.id}.png`), fullPage: false });
    await page.screenshot({ path: path.join(outDir, `${p.id}_full.png`), fullPage: true }).catch(() => {});
    const found = {};
    for (const [i, m] of (p.marks || []).entries()) {
      const loc = page.getByText(m, { exact: false }).first();
      try {
        await loc.scrollIntoViewIfNeeded({ timeout: 4000 });
        await page.evaluate(() => window.scrollBy(0, -260));  // 문구를 화면 위쪽에 두되 상단 고정 헤더 아래로
        await page.waitForTimeout(400);
        const box = await loc.boundingBox();
        if (!box) throw new Error('no box');
        const file = `${p.id}__m${i}.png`;
        await page.screenshot({ path: path.join(outDir, file) });
        found[m] = { file, x: Math.round(box.x), y: Math.round(box.y), w: Math.round(box.width), h: Math.round(box.height) };
      } catch (e) { found[m] = null; }
    }
    fs.writeFileSync(path.join(outDir, `${p.id}_marks.json`), JSON.stringify(found, null, 1));
    console.log('OK', p.id, Object.values(found).filter(Boolean).length + '/' + (p.marks || []).length, 'marks');
  } catch (e) { console.log('FAIL', p.id, String(e).slice(0, 120)); }
  await page.close();
}
await browser.close();
