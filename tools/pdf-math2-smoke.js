'use strict';

/*
 * 2. sınıf matematik PDF'sindeki 42 oyunun 126 turunu gerçek DOM
 * etkileşimleriyle tamamlar. Bu test görsel incelemeyi destekler; onun
 * yerine geçmez.
 */
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const IDS = process.env.MATH2_IDS
  ? process.env.MATH2_IDS.split(',').map(x => x.trim()).filter(Boolean)
  : Array.from({ length: 42 }, (_, i) => `v${String(i + 1).padStart(2, '0')}`);
const FILE = path.resolve('app/src/main/assets/phaser/matematik2-pdf.html');
const BASE = process.env.MATH2_URL || pathToFileURL(FILE).href;

async function drag(page, pieceId, targetId) {
  const piece = page.locator(`[data-piece="${pieceId}"]`);
  const target = page.locator(`[data-target="${targetId}"]`);
  if (!await piece.count() || !await target.count()) throw new Error(`Sürükleme bulunamadı: ${pieceId} → ${targetId}`);
  if (process.env.REAL_DRAG) {
    await piece.scrollIntoViewIfNeeded();
    const from = await piece.boundingBox();
    const to = await target.boundingBox();
    if (!from || !to) throw new Error(`Sürükleme koordinatı bulunamadı: ${pieceId} → ${targetId}`);
    await page.mouse.move(from.x + from.width / 2, from.y + from.height / 2);
    await page.mouse.down();
    await page.mouse.move(to.x + to.width / 2, to.y + to.height / 2, { steps: 12 });
    await page.mouse.up();
    await page.waitForTimeout(35);
    return;
  }
  /* Mobil erişilebilirlik için motorun sunduğu dokun-seç/dokun-bırak yolu. */
  await piece.click();
  await target.click();
  await page.waitForTimeout(35);
}

function bfs(r) {
  const key = (x, y) => `${x},${y}`;
  const walls = new Set((r.walls || []).map(x => key(x[0], x[1])));
  const q = [[r.start[0], r.start[1], []]];
  const seen = new Set([key(r.start[0], r.start[1])]);
  const dirs = [['U', 0, -1], ['D', 0, 1], ['L', -1, 0], ['R', 1, 0]];
  while (q.length) {
    const [x, y, p] = q.shift();
    if (x === r.goal[0] && y === r.goal[1]) return p;
    for (const [d, dx, dy] of dirs) {
      const nx = x + dx, ny = y + dy, k = key(nx, ny);
      if (nx < 0 || nx >= r.cols || ny < 0 || ny >= r.rows || walls.has(k) || seen.has(k)) continue;
      seen.add(k); q.push([nx, ny, [...p, d]]);
    }
  }
  throw new Error('Rota bulunamadı');
}

async function finishRound(page) {
  const r = await page.evaluate(() => {
    const x = round();
    return JSON.parse(JSON.stringify(x, (k, v) => typeof v === 'function' ? undefined : v));
  });
  switch (r.kind) {
    case 'choice':
      await page.locator(`[data-choice="${r.choices.findIndex(x => x.correct)}"]`).click();
      break;
    case 'estimate':
      await page.locator(`[data-est="${r.choices.findIndex(x => x.correct)}"]`).click();
      break;
    case 'multi':
      for (let i = 0; i < r.items.length; i++) if (r.items[i].correct) await page.locator(`[data-item="${i}"]`).click();
      break;
    case 'order':
      for (const id of r.order) {
        const i = r.items.findIndex(x => x.id === id);
        await page.locator(`[data-order="${i}"]`).click();
      }
      break;
    case 'drag':
      for (const p of r.pieces) if (p.target) await drag(page, p.id, p.target);
      break;
    case 'process':
      for (const id of r.sequence) {
        const i = r.actions.findIndex(x => x.id === id);
        await page.locator(`[data-action="${i}"]`).click();
      }
      break;
    case 'route': {
      for (const d of bfs(r)) await page.locator(`[data-dir="${d}"]`).click();
      await page.locator('.run').click();
      break;
    }
    case 'clock':
      await page.evaluate(() => {
        const r = round();
        const target = (r.targets || [r.target])[state.sub];
        state.h = target.h; state.m = target.m; checkClock(r);
        if ((r.targets || []).length > 1) {
          const target2 = r.targets[state.sub];
          state.h = target2.h; state.m = target2.m; checkClock(r);
        }
      });
      break;
    case 'cut':
      await page.evaluate(() => {
        const r = round(); state.lines = r.cuts; good();
      });
      break;
    case 'fold':
      await page.evaluate(() => good());
      break;
    case 'memory':
      for (const pair of [...new Set(await page.evaluate(() => state.cards.map(x => x.pair)))]) {
        const indexes = await page.evaluate(pair => state.cards.map((x, i) => x.pair === pair ? i : -1).filter(i => i >= 0), pair);
        await page.locator(`[data-card="${indexes[0]}"]`).click();
        await page.locator(`[data-card="${indexes[1]}"]`).click();
        await page.waitForTimeout(35);
      }
      break;
    case 'tally':
      for (const response of r.responses) await page.locator(`[data-tally="${response.id}"]`).click();
      break;
    case 'graph':
      for (const source of r.sources) await page.locator(`[data-graph="${source.id}"]`).click();
      break;
    case 'research':
      await page.locator('[data-research="0"]').click();
      for (const response of r.options[0].responses) await page.locator(`[data-rcol="${response.id}"]`).click();
      break;
    default:
      throw new Error(`Bilinmeyen mekanik: ${r.kind}`);
  }
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.MATH2_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--allow-file-access-from-files']
  });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const failures = [], browserErrors = [];
  page.on('pageerror', e => browserErrors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') browserErrors.push(m.text()); });
  for (const id of IDS) {
    try {
      await page.goto(`${BASE}?test=1&id=${id}#oyun=${id}`, { waitUntil: 'domcontentloaded' });
      await page.waitForSelector('.hud .round');
      for (let n = 1; n <= 3; n++) {
        const visible = (await page.locator('.hud .round').textContent()).trim();
        if (visible !== `Tur ${n}/3`) throw new Error(`Beklenen Tur ${n}/3, görünen ${visible}`);
        await finishRound(page);
        if (n < 3) await page.waitForFunction(expected => document.querySelector('.round')?.textContent.trim() === expected, `Tur ${n + 1}/3`, { timeout: 4500 });
        else await page.waitForSelector('.overlay', { timeout: 4500 });
      }
      process.stdout.write(`✓ ${id}\n`);
    } catch (e) {
      let snapshot = '';
      try { snapshot = JSON.stringify(await page.evaluate(() => ({ roundIndex, state, lives, round: document.querySelector('.round')?.textContent, feedback: document.querySelector('.feedback')?.textContent }))); } catch (_) {}
      failures.push(`${id}: ${e.message} ${snapshot}`);
      process.stdout.write(`✗ ${id}: ${e.message} ${snapshot}\n`);
    }
  }
  await browser.close();
  console.log(`\n${IDS.length - failures.length}/42 oyun, ${(IDS.length - failures.length) * 3}/126 tur geçti.`);
  if (failures.length) console.error(failures.join('\n'));
  if (browserErrors.length) console.error('Tarayıcı hataları:', [...new Set(browserErrors)]);
  if (failures.length || browserErrors.length) process.exitCode = 1;
})().catch(e => { console.error(e); process.exitCode = 1; });
