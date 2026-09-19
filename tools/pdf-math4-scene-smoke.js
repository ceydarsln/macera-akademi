'use strict';

const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const FILE = pathToFileURL(path.join(ROOT, 'app/src/main/assets/phaser/matematik4-pdf.html')).href;

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
    { id: 'p04', from: '[data-card="n98760"]', to: '[data-slot="0"]', value: 'state.slots[0]', expected: 'n98760' },
    { id: 'p10', from: '[data-add="ceyrek"]', to: '[data-tepsi]', value: 'state.tray[0]', expected: 'ceyrek' },
    { id: 'p12', from: '[data-card="u2"]', to: '[data-slot="0"]', value: 'state.slots[0]', expected: 'u2' },
    { id: 'p15', from: '[data-add="kasa"]', to: '[data-tepsi]', value: 'state.tray[0]', expected: 'kasa' },
    { id: 'p21', from: '[data-piece="a"]', to: '[data-target="k1"]', value: 'state.placed.k1', expected: 1 },
    { id: 'p24', from: '[data-item="0"]', to: '[data-multi-target]', value: 'state.selected[0]', expected: 'a' },
    { id: 'p48', from: '[data-card="s1"]', to: '[data-slot="0"]', value: 'state.slots[0]', expected: 's1' },
    { id: 'p51', from: '[data-action="0"]', to: '[data-process-target]', value: 'state.steps[0]', expected: 'grup' },
    { id: 'p52', from: '[data-tally-source]', to: '[data-tally-target="yaz"]', value: 'state.counts.yaz', expected: 1 },
    { id: 'p53', from: '[data-graph-source]', to: '[data-graph-target="futbol"]', value: 'state.counts.futbol', expected: 1 },
    { id: 'p55', from: '[data-tally-source]', to: '[data-tally-target="futbol"]', value: 'state.counts.futbol', expected: 1 }
  ];

  for (const check of checks) {
    await page.goto(`${FILE}?scene-smoke=${check.id}#oyun=${check.id}`, { waitUntil: 'domcontentloaded' });
    await page.waitForSelector(check.from);
    await drag(page, check.from, check.to);
    const actual = await page.evaluate(expr => Function(`return ${expr}`)(), check.value);
    if (JSON.stringify(actual) !== JSON.stringify(check.expected)) throw new Error(`${check.id}: ${check.value} = ${actual}, beklenen ${check.expected}`);
    console.log(`✓ ${check.id} gerçek sürükleme`);
  }
  await browser.close();
  console.log(`\n${checks.length}/${checks.length} Matematik 4 sahne hedefi gerçek işaretçi sürüklemesiyle geçti.`);
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
