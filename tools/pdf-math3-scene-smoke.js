'use strict';

const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const FILE = pathToFileURL(path.join(ROOT, 'app/src/main/assets/phaser/matematik3-pdf.html')).href;

async function drag(page, from, to) {
  const a = await page.locator(from).boundingBox();
  const b = await page.locator(to).boundingBox();
  if (!a || !b) throw new Error(`Sürükleme elemanı bulunamadı: ${from} -> ${to}`);
  await page.mouse.move(a.x + a.width / 2, a.y + a.height / 2);
  await page.mouse.down();
  await page.mouse.move(b.x + b.width / 2, b.y + b.height / 2, { steps: 8 });
  await page.mouse.up();
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.SMOKE_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--allow-file-access-from-files', '--disable-speech-api']
  });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const checks = [
    { id: 'w01', from: '[data-piece="y0"]', to: '[data-target="cekirdek"]', value: 'state.toplam', expected: 100 },
    { id: 'w02', from: '[data-piece="y0"]', to: '[data-target="cekirdek"]', value: 'state.toplam', expected: 100 },
    { id: 'w05', from: '[data-share-piece]', to: '[data-share="a"]', value: 'state.a', expected: 1 },
    { id: 'w09', from: '[data-piece="d1"]', to: '[data-target="tepsi"]', value: 'locked', expected: true },
    { id: 'w32', from: '[data-parca="0"]', to: '[data-yuva="0"]', value: 'state.yerlesen[0]', expected: 0 },
    { id: 'w34', from: '[data-sec="0"]', to: '[data-ayna-hedef]', value: 'locked', expected: true },
    { id: 'w43', from: '[data-kart="7"]', to: '[data-yer="0"]', value: 'state.yerlesen[0]', expected: 7 },
    { id: 'w48', from: '[data-kart="2"]', to: '[data-yer="0"]', value: 'state.siklik[0]', expected: 2,
      setup: 'state.faz=3;state.sayim=[2,5,3];state.siklik=[null,null,null];state.kartlar=[2,5,3];projeCiz(round())' }
  ];

  for (const check of checks) {
    await page.goto(`${FILE}?scene-smoke=${check.id}#oyun=${check.id}`, { waitUntil: 'domcontentloaded' });
    if (check.setup) await page.evaluate(code => Function(code)(), check.setup);
    await page.waitForSelector(check.from);
    await drag(page, check.from, check.to);
    const actual = await page.evaluate(expr => Function(`return ${expr}`)(), check.value);
    if (JSON.stringify(actual) !== JSON.stringify(check.expected)) throw new Error(`${check.id}: ${check.value} = ${actual}, beklenen ${check.expected}`);
    console.log(`✓ ${check.id} gerçek sürükleme`);
  }
  await browser.close();
  console.log(`\n${checks.length}/${checks.length} sahne hedefi gerçek işaretçi sürüklemesiyle geçti.`);
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
