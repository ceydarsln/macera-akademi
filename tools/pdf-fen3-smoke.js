'use strict';

const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const FILE = pathToFileURL(path.join(ROOT, 'app/src/main/assets/phaser/fen3-pdf.html')).href;
const args = process.argv.slice(2);
const start = Math.max(1, Number(args[0]) || 1);
const end = Math.min(48, Number(args[1]) || 30);
const ids = Array.from({ length: end - start + 1 }, (_, i) => `g${String(start + i).padStart(2, '0')}`);
const pause = async page => { await page.waitForTimeout(65); if (await page.evaluate(() => !!state.gecis)) await page.waitForFunction(() => !state.gecis); };

async function roundData(page) {
  return page.evaluate(() => JSON.parse(JSON.stringify(round(), (k, v) => typeof v === 'function' ? undefined : v)));
}

async function click(page, selector) {
  await page.locator(selector).click();
  await pause(page);
}

function shortestPath(r, from, to) {
  const moves = [
    { symbol: '⬆️', dx: 0, dy: -1 },
    { symbol: '⬇️', dx: 0, dy: 1 },
    { symbol: '⬅️', dx: -1, dy: 0 },
    { symbol: '➡️', dx: 1, dy: 0 }
  ];
  const blocked = new Set(r.engeller.map(([x, y]) => `${x},${y}`));
  const queue = [{ x: from[0], y: from[1], path: [] }];
  const seen = new Set([`${from[0]},${from[1]}`]);
  while (queue.length) {
    const current = queue.shift();
    if (current.x === to[0] && current.y === to[1]) return current.path;
    for (const move of moves) {
      const x = current.x + move.dx;
      const y = current.y + move.dy;
      const key = `${x},${y}`;
      if (x < 0 || y < 0 || x >= r.en || y >= r.boy || blocked.has(key) || seen.has(key)) continue;
      seen.add(key);
      queue.push({ x, y, path: current.path.concat(move.symbol) });
    }
  }
  throw new Error(`Gözlem yolu bulunamadı: ${from} -> ${to}`);
}

async function solveRound(page, r) {
  if (r.kind === 'sinifla') {
    for (let n = 0; n < r.kartlar.length; n++) {
      const i = await page.evaluate(() => state.ix || 0);
      if (await page.locator('[data-sinif-kart]').count()) await click(page, '[data-sinif-kart]');
      await click(page, `[data-kutu="${r.kartlar[i].dogru}"]`);
    }
  } else if (r.kind === 'sira') {
    for (const i of r.dogru) await click(page, `[data-kart="${i}"]`);
  } else if (r.kind === 'esle') {
    for (let j = 0; j < r.etiketler.length; j++) {
      const i = r.yuvalar.findIndex(y => y.dogru === j);
      await click(page, `[data-et="${j}"]`);
      await click(page, `[data-yuva="${i}"]`);
    }
  } else if (r.kind === 'karar') {
    const i = r.secenekler.findIndex(x => x.correct);
    await click(page, `[data-sec="${i}"]`);
    if (r.neden) {
      const j = r.neden.secenekler.findIndex(x => x.correct);
      await click(page, `[data-neden="${j}"]`);
    }
  } else if (r.kind === 'topla') {
    for (const i of r.gerekli) await click(page, `[data-oge="${i}"]`);
  } else if (r.kind === 'hafiza') {
    for (let pair = 0; pair < r.ciftler.length; pair++) {
      const positions = await page.evaluate(p => (state.kartlar || []).map((x, i) => x.cift === p ? i : -1).filter(i => i >= 0), pair);
      await click(page, `[data-hk="${positions[0]}"]`);
      await click(page, `[data-hk="${positions[1]}"]`);
      const j = r.ciftler[pair].secenekler.findIndex(x => x.correct);
      await click(page, `[data-hs="${j}"]`);
    }
  } else if (r.kind === 'grafik') {
    for (let i = 0; i < r.gruplar.length; i++) for (let n = 0; n < r.gruplar[i].sayi; n++) await click(page, `[data-sut="${i}"]`);
  } else if (r.kind === 'olcum') {
    await page.locator('#olcek').evaluate((el, value) => { el.value = value; el.dispatchEvent(new Event('input', { bubbles: true })); }, String(r.dogru));
    await click(page, '#olcOk');
  } else if (r.kind === 'sula') {
    await page.evaluate(value => {
      state.verilen = value;
      state.sonuc = '';
      sulaCiz(round());
    }, Math.ceil((r.uygunAlt + r.uygunUst) / 2));
    await click(page, '#sulaOk');
  } else if (r.kind === 'tus') {
    for (const digit of String(r.dogru)) await click(page, `[data-tus="${digit}"]`);
    await click(page, '[data-tus="ok"]');
  } else if (r.kind === 'cumle') {
    for (const i of r.kabul[0]) await click(page, `[data-kel="${i}"]`);
    await page.waitForSelector('[data-bit]', { timeout: 2000 });
    const correct = r.bitirme.findIndex(x => x.correct);
    await click(page, `[data-bit="${correct}"]`);
  } else if (r.kind === 'gozlem') {
    for (let targetIndex = 0; targetIndex < r.noktalar.length; targetIndex++) {
      const from = await page.evaluate(() => (state.pos || round().basla).slice());
      const target = r.noktalar[targetIndex];
      const path = shortestPath(r, from, [target.x, target.y]);
      if (path.length > 10) throw new Error(`Gözlem yolu 10 adımı aşıyor: ${path.length}`);
      for (const symbol of path) await click(page, `[data-yon="${symbol}"]`);
      await page.locator('[data-yon="git"]').click();
      await page.waitForFunction(() => state.soruNokta != null, null, { timeout: 3000 });
      const correct = target.secenekler.findIndex(x => x.correct);
      await click(page, `[data-gs="${correct}"]`);
    }
  } else if (r.kind === 'yaz') {
    await page.locator('#yaziAlan').fill(r.ornekCevap);
    await page.locator('#yaziAlan').dispatchEvent('input');
    await click(page, '#yazOk');
  } else {
    throw new Error(`Bilinmeyen kip: ${r.kind}`);
  }
}

if (require.main === module) (async () => {
  const browser = await chromium.launch({ headless: true, executablePath: process.env.SMOKE_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', args: ['--allow-file-access-from-files', '--disable-speech-api'] });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const passed = [];
  for (const id of ids) {
    await page.goto(`${FILE}?test=1&smoke=${id}#oyun=${id}`, { waitUntil: 'domcontentloaded' });
    for (let turn = 0; turn < 3; turn++) {
      const before = await page.evaluate(() => roundIndex);
      const r = await roundData(page);
      await solveRound(page, r);
      await page.waitForFunction(old => roundIndex > old || !!document.querySelector('.overlay'), before, { timeout: 8000 });
    }
    const result = await page.evaluate(() => ({ done: !!document.querySelector('.overlay'), lives }));
    if (!result.done || result.lives !== 3) throw new Error(`${id}: bitiş=${result.done}, can=${result.lives}`);
    passed.push(id);
    console.log(`✓ ${id}`);
  }
  await browser.close();
  console.log(`\n${passed.length}/${ids.length} oyun, ${passed.length * 3}/${ids.length * 3} tur geçti.`);
})().catch(error => { console.error(error); process.exitCode = 1; });
module.exports = { solveRound };
