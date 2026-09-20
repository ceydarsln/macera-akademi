'use strict';

const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const FILE = pathToFileURL(path.join(ROOT, 'app/src/main/assets/phaser/hayatbilgisi2-pdf.html')).href;

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
    { id: 'h01', kind: 'sinif' }, { id: 'h02', kind: 'sinif' },
    { id: 'h04', kind: 'sira' }, { id: 'h05', kind: 'sinif' },
    { id: 'h06', kind: 'sira' }, { id: 'h07', kind: 'sinif' },
    { id: 'h08', kind: 'mesafe' }, { id: 'h09', kind: 'esle' },
    { id: 'h10', kind: 'tus' }, { id: 'h11', kind: 'sira' },
    { id: 'h12', kind: 'canta' }, { id: 'h13', kind: 'esle' },
    { id: 'h14', kind: 'sinif' }, { id: 'h15', kind: 'sira' },
    { id: 'h16', kind: 'sinif' }, { id: 'h18', kind: 'cetele' },
    { id: 'h19', kind: 'esle' }, { id: 'h21', kind: 'esle' },
    { id: 'h22', kind: 'sira' }, { id: 'h23', kind: 'esle' },
    { id: 'h24', kind: 'sinif' }, { id: 'h25', kind: 'esle' },
    { id: 'h26', kind: 'sinif' }, { id: 'h27', kind: 'yon' },
    { id: 'h28', kind: 'sira' }, { id: 'h29', kind: 'musluk' },
    { id: 'h30', kind: 'tahmin' }
  ];
  for (const check of checks) {
    await page.goto(`${FILE}?scene-smoke=${check.id}#oyun=${check.id}`, { waitUntil: 'domcontentloaded' });
    if (check.kind === 'sinif') {
      const target = await page.evaluate(() => round().kartlar[state.ix || 0].dogru);
      await drag(page, '[data-sinif-kart]', `[data-kutu="${target}"]`);
      if (await page.evaluate(i => state.sayim[i], target) !== 1) throw new Error(`${check.id}: sınıflandırma yerleşmedi`);
    } else if (check.kind === 'sira') {
      const first = await page.evaluate(() => round().dogru[0]);
      await drag(page, `[data-kart="${first}"]`, '[data-sira-hedef]');
      if (await page.evaluate(() => state.dizi[0]) !== first) throw new Error(`${check.id}: sıra kartı yerleşmedi`);
    } else if (check.kind === 'esle') {
      const slot = await page.evaluate(() => round().yuvalar.findIndex(x => x.dogru === 0));
      await drag(page, '[data-et="0"]', `[data-yuva="${slot}"]`);
      if (await page.evaluate(i => state.yerlesen[i], slot) !== 0) throw new Error(`${check.id}: eşleştirme yerleşmedi`);
    } else if (check.kind === 'canta') {
      const first = await page.evaluate(() => round().esyalar.findIndex(x => x.gerekli));
      await drag(page, `[data-esya="${first}"]`, '[data-canta-hedef]');
      if (!await page.evaluate(i => state.alinan.includes(i), first)) throw new Error(`${check.id}: malzeme çantaya girmedi`);
    } else if (check.kind === 'cetele') {
      const target = await page.evaluate(() => round().oylar[0].dogru);
      await drag(page, '[data-cetele-kart]', `[data-satir="${target}"]`);
      if (await page.evaluate(i => state.say[i], target) !== 1) throw new Error(`${check.id}: çetele işareti eklenmedi`);
    } else if (check.kind === 'mesafe') {
      await page.locator('#mesafeAlan').evaluate(el => { el.value = '75'; el.dispatchEvent(new Event('input', { bubbles: true })); });
      if (await page.evaluate(() => state.olcek) !== 75) throw new Error(`${check.id}: mesafe ölçeri hareket etmedi`);
    } else if (check.kind === 'tus') {
      await page.locator(`[data-tus="${(await page.evaluate(() => round().numara))[0]}"]`).click();
      if ((await page.evaluate(() => state.giris)).length !== 1) throw new Error(`${check.id}: telefon tuşu çalışmadı`);
    } else if (check.kind === 'yon') {
      await page.locator('[data-yon="KUZEY"]').click();
      if (await page.evaluate(() => state.prog[0]) !== 'KUZEY') throw new Error(`${check.id}: yön bloğu programa eklenmedi`);
    } else if (check.kind === 'musluk') {
      const box = await page.locator('#musluk').boundingBox();
      await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
      await page.mouse.down();
      await page.waitForTimeout(180);
      await page.mouse.up();
      await page.waitForTimeout(60);
      if (await page.evaluate(() => state.yuzde) <= 0) throw new Error(`${check.id}: musluk basılı tutmayla dolmadı`);
    } else if (check.kind === 'tahmin') {
      await page.locator('#tahminAlan').evaluate(el => { el.value = '10'; el.dispatchEvent(new Event('input', { bubbles: true })); });
      if (await page.evaluate(() => state.tahmin) !== 10) throw new Error(`${check.id}: tahmin ölçeri hareket etmedi`);
    }
    console.log(`✓ ${check.id} gerçek sahne etkileşimi`);
  }
  await browser.close();
  console.log(`\n${checks.length}/${checks.length} Hayat Bilgisi 2 sahne etkileşimi geçti.`);
})().catch(error => { console.error(error); process.exitCode = 1; });
