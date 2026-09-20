'use strict';

const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const FILE = pathToFileURL(path.join(ROOT, 'app/src/main/assets/phaser/fen4-pdf.html')).href;

async function drag(page, from, to) {
  const a = await page.locator(from).boundingBox();
  const b = await page.locator(to).boundingBox();
  if (!a || !b) throw new Error(`Sürükleme elemanı bulunamadı: ${from} -> ${to}`);
  await page.mouse.move(a.x + a.width / 2, a.y + a.height / 2);
  await page.mouse.down();
  await page.mouse.move(b.x + b.width / 2, b.y + b.height / 2, { steps: 10 });
  await page.mouse.up();
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: process.env.SMOKE_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', args: ['--allow-file-access-from-files', '--disable-speech-api'] });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const checks = [
    { id: 'f01', kind: 'sinif' },
    { id: 'f03', kind: 'sira' },
    { id: 'f04', kind: 'esle' },
    { id: 'f05', kind: 'kur' },
    { id: 'f06', kind: 'sozdiz' },
    { id: 'f07', kind: 'sinif' },
    { id: 'f08', kind: 'esle' },
    { id: 'f09', kind: 'kur' },
    { id: 'f11', kind: 'sira' },
    { id: 'f13', kind: 'sinif' },
    { id: 'f14', kind: 'sira' },
    { id: 'f19', kind: 'sinif' },
    { id: 'f20', kind: 'sinif' },
    { id: 'f22', kind: 'sira' },
    { id: 'f24', kind: 'kur' },
    { id: 'f25', kind: 'sinif' },
    { id: 'f26', kind: 'sinif' },
    { id: 'f29', kind: 'sira' },
    { id: 'f30', kind: 'kur' }
  ];
  for (const check of checks) {
    await page.goto(`${FILE}?scene-smoke=${check.id}#oyun=${check.id}`, { waitUntil: 'domcontentloaded' });
    if (check.kind === 'sinif') {
      const target = await page.evaluate(() => round().kartlar[state.ix || 0].dogru);
      await drag(page, '[data-sinif-kart]', `[data-kutu="${target}"]`);
      const actual = await page.evaluate(i => state.sayim[i], target);
      if (actual !== 1) throw new Error(`${check.id}: sınıflandırma yerleşmedi`);
    } else if (check.kind === 'sira') {
      const first = await page.evaluate(() => round().dogru[0]);
      await drag(page, `[data-kart="${first}"]`, '[data-sira-hedef]');
      const actual = await page.evaluate(() => state.dizi[0]);
      if (actual !== first) throw new Error(`${check.id}: sıra kartı yerleşmedi`);
    } else if (check.kind === 'esle') {
      const slot = await page.evaluate(() => round().parcalar[0].yuva);
      await drag(page, '[data-parca="0"]', `[data-yuva="${slot}"]`);
      const actual = await page.evaluate(i => state.yerlesen[i], slot);
      if (actual !== 0) throw new Error(`${check.id}: eşleştirme kartı yerleşmedi`);
    } else if (check.kind === 'kur') {
      const first = await page.evaluate(() => {
        const id = round().istekler[0].gerekli[0];
        return round().havuz.findIndex(x => x.id === id);
      });
      await drag(page, `[data-h="${first}"]`, '[data-kur-hedef]');
      const actual = await page.evaluate(i => (state.icerik || []).includes(i), first);
      if (!actual) throw new Error(`${check.id}: malzeme gerçek düzeneğe yerleşmedi`);
    } else if (check.kind === 'sozdiz') {
      const first = await page.evaluate(() => round().dogruDiziler[0][0]);
      await drag(page, `[data-soz="${first}"]`, '[data-soz-hedef]');
      const actual = await page.evaluate(() => state.dizi[0]);
      if (actual !== first) throw new Error(`${check.id}: sözcük cümle yuvasına yerleşmedi`);
    }
    console.log(`✓ ${check.id} gerçek sahne sürüklemesi`);
  }
  await browser.close();
  console.log(`\n${checks.length}/${checks.length} Fen 4 sahne hedefi gerçek işaretçi sürüklemesiyle geçti.`);
})().catch(error => { console.error(error); process.exitCode = 1; });
