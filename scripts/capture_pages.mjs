// 원문 페이지를 1920×1080(및 긴 페이지 전체)으로 캡처한다. 렌더 때 푸시인·형광펜을 입힌다.
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
    // 쿠키 배너·고정 헤더가 가리면 캡처 품질이 떨어진다: 흔한 배너 버튼을 닫되, 동의 버튼은 누르지 않는다(거부/닫기만)
    for (const sel of ['button:has-text("Reject")', 'button:has-text("Decline")', 'button:has-text("Close")', '[aria-label="Close"]']) {
      const b = page.locator(sel).first(); if (await b.count() && await b.isVisible().catch(() => false)) { await b.click({ timeout: 1500 }).catch(() => {}); break; }
    }
    await page.screenshot({ path: path.join(outDir, `${p.id}.png`), fullPage: false });
    await page.screenshot({ path: path.join(outDir, `${p.id}_full.png`), fullPage: true }).catch(() => {});
    console.log('OK', p.id);
  } catch (e) { console.log('FAIL', p.id, String(e).slice(0, 120)); }
  await page.close();
}
await browser.close();
