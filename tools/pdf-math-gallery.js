'use strict';

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const IDS = [
  'm01','m02','m03','m05','m09','m10','m11','m12','m14','m15','m17','m18',
  'm20','m22','m23','m24','m25','m26','m28','m31','m32','m33','m34','m35',
  'm36','m37','m38','m39','m41','m42','m43','m44','m45','m46','m47','m48',
  'm49','m50','m51','m52','m53','m54','m55','m56','m57','m58','m59','m60','m61'
];
const BASE = process.env.PDF_MATH_URL ||
  'http://127.0.0.1:8871/app/src/main/assets/phaser/matematik-pdf.html';
const OUT = path.resolve(process.env.PDF_MATH_GALLERY || 'tmp/pdf-math-gallery');

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.PDF_MATH_CHROME ||
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  for (const id of IDS) {
    await page.goto(`${BASE}?gallery=${id}#oyun=${id}`, { waitUntil: 'domcontentloaded' });
    await page.waitForSelector('.hud .round');
    await page.screenshot({ path: path.join(OUT, `${id}.png`) });
    process.stdout.write(`✓ ${id}\n`);
  }
  await browser.close();
  console.log(`${IDS.length} ekran: ${OUT}`);
})().catch(e => { console.error(e); process.exitCode = 1; });
