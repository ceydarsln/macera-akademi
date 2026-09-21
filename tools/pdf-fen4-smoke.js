'use strict';

const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const FILE = pathToFileURL(path.join(ROOT, 'app/src/main/assets/phaser/fen4-pdf.html')).href;
const args = process.argv.slice(2);
const start = Math.max(1, Number(args[0]) || 1);
const end = Math.min(48, Number(args[1]) || 30);
const ids = Array.from({ length: end - start + 1 }, (_, i) => `f${String(start + i).padStart(2, '0')}`);
const pause = page => page.waitForTimeout(70);

async function roundData(page) {
  return page.evaluate(() => JSON.parse(JSON.stringify(round(), (k, v) => typeof v === 'function' ? undefined : v)));
}

async function click(page, selector) {
  await page.locator(selector).click();
  await pause(page);
}

function shortestPlanPath(r) {
  const moves = [
    { key: 'U', dx: 0, dy: -1 }, { key: 'D', dx: 0, dy: 1 },
    { key: 'L', dx: -1, dy: 0 }, { key: 'R', dx: 1, dy: 0 }
  ];
  const queue = [{ x: r.basla.x, y: r.basla.y, path: [] }];
  const seen = new Set([`${r.basla.x},${r.basla.y}`]);
  while (queue.length) {
    const current = queue.shift();
    if (current.x === r.hedef.x && current.y === r.hedef.y) return current.path;
    for (const move of moves) {
      const x = current.x + move.dx, y = current.y + move.dy, mark = `${x},${y}`;
      if (x < 0 || y < 0 || x >= r.genislik || y >= r.yukseklik || r.plan[y][x] === '#' || seen.has(mark)) continue;
      seen.add(mark);
      queue.push({ x, y, path: current.path.concat(move.key) });
    }
  }
  throw new Error('Güvenli bisiklet rotası bulunamadı');
}

async function solveRound(page, r) {
  if (r.kind === 'sinifla') {
    for (let n = 0; n < r.kartlar.length; n++) {
      const i = await page.evaluate(() => state.ix || 0);
      await click(page, `[data-kutu="${r.kartlar[i].dogru}"]`);
    }
  } else if (r.kind === 'karar') {
    for (let i = 0; i < r.sorular.length; i++) {
      const q = r.sorular[i];
      const answer = q.secenekler.findIndex(x => x.dogru);
      await click(page, `[data-sec="${answer}"]`);
      if (q.gerekce) {
        const reason = q.gerekce.secenekler.findIndex(x => x.dogru);
        await click(page, `[data-sec="${reason}"]`);
      }
    }
  } else if (r.kind === 'sira') {
    for (const i of r.dogru) await click(page, `[data-kart="${i}"]`);
  } else if (r.kind === 'esle') {
    for (let j = 0; j < r.parcalar.length; j++) {
      const slot = r.parcalar[j].yuva;
      await click(page, `[data-parca="${j}"]`);
      await click(page, `[data-yuva="${slot}"]`);
      const reason = r.yuvalar[slot].gerekce;
      if (reason) {
        const answer = reason.secenekler.findIndex(x => x.dogru);
        await click(page, `[data-ger="${answer}"]`);
      }
    }
  } else if (r.kind === 'kur') {
    while (await page.evaluate(() => round()?.kind === 'kur' && (state.ix || 0) < round().istekler.length)) {
      const wanted = await page.evaluate(() => round().istekler[state.ix || 0].gerekli.slice());
      for (const id of wanted) {
        const index = r.havuz.findIndex(x => x.id === id);
        const already = await page.evaluate(i => (state.icerik || []).includes(i), index);
        if (!already) await click(page, `[data-h="${index}"]`);
      }
    }
  } else if (r.kind === 'sozdiz') {
    for (const i of r.dogruDiziler[0]) await click(page, `[data-soz="${i}"]`);
    await click(page, '#buyukBtn');
    await click(page, `[data-nk="${r.dogruNokta}"]`);
    await click(page, '#onayBtn');
  } else if (r.kind === 'hafiza') {
    for (let pair = 0; pair < r.ciftler.length; pair++) {
      const positions = await page.evaluate(p => state.kartlar.map((x, i) => x.cift === p ? i : -1).filter(i => i >= 0), pair);
      await click(page, `[data-k="${positions[0]}"]`);
      await click(page, `[data-k="${positions[1]}"]`);
      if (r.ciftler[pair].gerekce) {
        const answer = r.ciftler[pair].gerekce.secenekler.findIndex(x => x.dogru);
        await click(page, `[data-ger="${answer}"]`);
      }
    }
  } else if (r.kind === 'gozlem') {
    await page.locator('#oynatBtn').click();
    await page.waitForFunction(() => !state.oynuyor && state.izleme > 0, null, { timeout: 4000 });
    for (const q of r.sorular) {
      const answer = q.secenekler.findIndex(x => x.dogru);
      await click(page, `[data-sec="${answer}"]`);
    }
  } else if (r.kind === 'isit') {
    await page.evaluate(() => {
      const m = round().madde;
      state.oran = 1;
      state.T = m.degisimC;
      state.isitiyor = false;
      state.bozuldu = false;
      state.gozlem = m.gozlem2;
      isitCiz(round());
    });
    await click(page, '#durBtn');
  } else if (r.kind === 'grafik') {
    for (let i = 0; i < r.kategoriler.length; i++) {
      for (let n = 0; n < r.kategoriler[i].hedef; n++) await click(page, `[data-sut="${i}"]`);
    }
    await click(page, '#onayBtn');
  } else if (r.kind === 'deney') {
    let step = 0;
    while (await page.evaluate(() => (state.denenen || []).length < (round().enAzDeneme || 3))) {
      await click(page, `[data-a="${r.anahtarlar[step % r.anahtarlar.length].id}"]`);
      step++;
    }
    for (const q of r.sorular) {
      const answer = q.secenekler.findIndex(x => x.dogru);
      await click(page, `[data-sec="${answer}"]`);
    }
  } else if (r.kind === 'plan') {
    for (const direction of shortestPlanPath(r)) await click(page, `[data-yon="${direction}"]`);
    await click(page, '#calisBtn');
    if (r.gerekce) {
      const answer = r.gerekce.secenekler.findIndex(x => x.dogru);
      await click(page, `[data-ger="${answer}"]`);
    }
  } else if (r.kind === 'yaz') {
    await page.locator('#yaziAlan').fill(r.ornekCevap);
    await page.locator('#yaziAlan').dispatchEvent('input');
    await click(page, '#onayBtn');
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
