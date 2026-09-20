'use strict';

const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
let ids;
if (args.length && args.length <= 2 && args.every(x => /^\d+$/.test(x))) {
  const start = Math.max(1, Number(args[0]));
  const end = Math.min(64, Number(args[1] || args[0]));
  ids = Array.from({ length: Math.max(0, end - start + 1) }, (_, i) => `z${String(start + i).padStart(2, '0')}`);
} else {
  ids = args.length ? args : Array.from({ length: 30 }, (_, i) => `z${String(i + 1).padStart(2, '0')}`);
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.SMOKE_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--allow-file-access-from-files', '--disable-speech-api']
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 820 } });
  const url = `${pathToFileURL(path.join(ROOT, 'tools', 'dom_kosum.html')).href}#ids=${ids.join(',')}`;
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => window.SONUC && window.SONUC.bitti, null, { timeout: Math.max(120000, ids.length * 18000) });
  const sonuc = await page.evaluate(() => window.SONUC);
  await browser.close();

  for (const id of sonuc.gecti) process.stdout.write(`✓ ${id}\n`);
  for (const hata of sonuc.hatalar) process.stderr.write(`✗ ${hata}\n`);
  console.log(`\n${sonuc.gecti.length}/${ids.length} oyun, ${sonuc.gecti.length * 3}/${ids.length * 3} tur geçti.`);
  if (sonuc.kaldi.length) process.exitCode = 1;
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
