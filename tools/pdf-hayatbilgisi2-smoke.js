'use strict';

const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const FILE = pathToFileURL(path.join(ROOT, 'app/src/main/assets/phaser/hayatbilgisi2-pdf.html')).href;
const args = process.argv.slice(2);
const start = Math.max(1, Number(args[0]) || 1);
const end = Math.min(36, Number(args[1]) || 30);
const ids = Array.from({ length: end - start + 1 }, (_, i) => `h${String(start + i).padStart(2, '0')}`);
const pause = async page => { await page.waitForTimeout(70); if (await page.evaluate(() => !!state.gecis)) await page.waitForFunction(() => !state.gecis); };

async function roundData(page) {
  return page.evaluate(() => JSON.parse(JSON.stringify(round(), (k, v) => typeof v === 'function' ? undefined : v)));
}

async function click(page, selector) {
  await page.locator(selector).click();
  await pause(page);
}

function routeFor(t) {
  const edges = ['ust', 'sag', 'alt', 'sol'];
  const names = ['KUZEY', 'DOĞU', 'GÜNEY', 'BATI'];
  const delta = { ust: [0, -1], sag: [1, 0], alt: [0, 1], sol: [-1, 0] };
  const sun = edges.indexOf(t.gunesKenar);
  const east = t.zaman === 'sabah' ? sun : (sun + 2) % 4;
  const moves = names.map((name, i) => ({ name, delta: delta[edges[(east + i - 1 + 4) % 4]] }));
  const queue = [{ pos: t.baslangic.slice(), path: [] }];
  const seen = new Set([t.baslangic.join(',')]);
  while (queue.length) {
    const current = queue.shift();
    if (current.pos[0] === t.hedef[0] && current.pos[1] === t.hedef[1]) return current.path;
    for (const move of moves) {
      const x = current.pos[0] + move.delta[0], y = current.pos[1] + move.delta[1], mark = `${x},${y}`;
      if (x < 0 || y < 0 || x > 3 || y > 3 || t.engeller.some(e => e[0] === x && e[1] === y) || seen.has(mark)) continue;
      seen.add(mark);
      queue.push({ pos: [x, y], path: current.path.concat(move.name) });
    }
  }
  throw new Error('Yön rotası bulunamadı');
}

async function solveRound(page, r) {
  if (r.kind === 'karar') {
    const answer = r.secenekler.findIndex(x => x.correct);
    await click(page, `[data-sec="${answer}"]`);
    if (r.neden) {
      const reason = r.neden.secenekler.findIndex(x => x.correct);
      await click(page, `[data-neden="${reason}"]`);
    }
  } else if (r.kind === 'sinifla') {
    for (let n = 0; n < r.kartlar.length; n++) {
      const i = await page.evaluate(() => state.ix || 0);
      if (await page.locator('[data-sinif-kart]').count()) await click(page, '[data-sinif-kart]');
      await click(page, `[data-kutu="${r.kartlar[i].dogru}"]`);
    }
  } else if (r.kind === 'sira') {
    for (const i of r.dogru) await click(page, `[data-kart="${i}"]`);
  } else if (r.kind === 'esle') {
    for (let j = 0; j < r.etiketler.length; j++) {
      const slot = r.yuvalar.findIndex(x => x.dogru === j);
      await click(page, `[data-et="${j}"]`);
      await click(page, `[data-yuva="${slot}"]`);
    }
  } else if (r.kind === 'yaz') {
    await page.locator('#yaziAlan').fill(r.ornekCevap);
    await page.locator('#yaziAlan').dispatchEvent('input');
    await click(page, '#yazOk');
  } else if (r.kind === 'konus') {
    await click(page, '#ornekDinle');
    await click(page, '#konusBasla');
    await page.evaluate(() => { state.sure = 1300; state.faz = 2; state.basili = false; konusCiz(round()); });
    for (let i = 0; i < r.olcutler.length; i++) await click(page, `[data-ol="${i}"]`);
    await click(page, '#konusOk');
  } else if (r.kind === 'mesafe') {
    for (const d of r.durumlar) {
      const value = Math.round((d.enAz + d.enCok) / 2 / 5) * 5;
      await page.evaluate(v => { state.olcek = v; mesafeCiz(round()); }, value);
      await click(page, '#mesafeOk');
    }
  } else if (r.kind === 'tus') {
    for (let i = 0; i < r.senaryolar.length; i++) {
      for (const digit of r.numara) await click(page, `[data-tus="${digit}"]`);
      await click(page, '#ara');
    }
  } else if (r.kind === 'canta') {
    const required = r.esyalar.map((x, i) => x.gerekli ? i : -1).filter(i => i >= 0).slice(0, r.gerekenSayi);
    for (const i of required) await click(page, `[data-esya="${i}"]`);
  } else if (r.kind === 'cetele') {
    for (const vote of r.oylar) await click(page, `[data-satir="${vote.dogru}"]`);
  } else if (r.kind === 'yon') {
    for (const tour of r.turlar) {
      for (const direction of routeFor(tour)) await click(page, `[data-yon="${direction}"]`);
      await click(page, '#calistir');
    }
  } else if (r.kind === 'musluk') {
    for (const job of r.isler) {
      await page.evaluate(value => { state.yuzde = value; state.basili = false; muslukCiz(round()); }, Math.ceil((job.enAz + job.enCok) / 2));
      await click(page, '#muslukOk');
    }
  } else if (r.kind === 'tahmin') {
    for (const situation of r.durumlar) {
      await click(page, '#tahminOk');
      const answer = situation.secenekler.findIndex(x => x.correct);
      await click(page, `[data-tsec="${answer}"]`);
    }
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
