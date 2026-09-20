'use strict';

const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const FILE = pathToFileURL(path.join(ROOT, 'app/src/main/assets/phaser/fen3-pdf.html')).href;

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
    { id: 'g01', kind: 'sinif' },
    { id: 'g02', kind: 'sira' },
    { id: 'g03', kind: 'esle' },
    { id: 'g05', kind: 'topla' },
    { id: 'g14', kind: 'sira' },
    { id: 'g22', kind: 'topla' },
    { id: 'g23', kind: 'sinif' },
    { id: 'g24', kind: 'grafik' },
    { id: 'g29', kind: 'sira' }
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
      const slot = await page.evaluate(() => round().yuvalar.findIndex(y => y.dogru === 0));
      await drag(page, '[data-et="0"]', `[data-yuva="${slot}"]`);
      const actual = await page.evaluate(i => state.yerlesen[i], slot);
      if (actual !== 0) throw new Error(`${check.id}: eşleştirme kartı yerleşmedi`);
    } else if (check.kind === 'topla') {
      const first = await page.evaluate(() => round().gerekli[0]);
      await drag(page, `[data-oge="${first}"]`, '[data-canta]');
      const actual = await page.evaluate(() => state.alinan[0]);
      if (actual !== first) throw new Error(`${check.id}: araç çantaya girmedi`);
    } else if (check.kind === 'grafik') {
      await drag(page, '[data-grafik-blok]', '[data-sut="0"]');
      const actual = await page.evaluate(() => state.kondu[0]);
      if (actual !== 1) throw new Error(`${check.id}: grafik bloğu yerleşmedi`);
    }
    console.log(`✓ ${check.id} gerçek sahne sürüklemesi`);
  }
  await browser.close();
  console.log(`\n${checks.length}/${checks.length} Fen 3 sahne hedefi gerçek işaretçi sürüklemesiyle geçti.`);
})().catch(error => { console.error(error); process.exitCode = 1; });
