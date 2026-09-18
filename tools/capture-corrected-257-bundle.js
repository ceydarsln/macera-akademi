'use strict';

const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'artifacts', 'guncellenen-257-oyun');
const ASSETS = path.join(ROOT, 'app/src/main/assets/phaser');
const VIEWPORT = { width: 390, height: 844 };
const ids = (prefix, start, end, width = 2) => Array.from({ length: end - start + 1 }, (_, i) => `${prefix}${String(start + i).padStart(width, '0')}`);
const GROUPS = [
  { folder: '01-sayma-rakam', label: '1. Sınıf Sayma ve Rakam', file: 'sayma-pdf.html', ids: [...ids('s', 0, 10, 1), ...ids('n', 1, 9, 1)], capture: true },
  { folder: '02-matematik-1', label: '1. Sınıf Matematik', ids: ids('m', 1, 61), source: path.join(ROOT, 'artifacts/matematik-103-inceleme/screens') },
  { folder: '03-turkce-1', label: '1. Sınıf Türkçe', file: 'turkce1-pdf.html', ids: ids('t', 1, 64), capture: true },
  { folder: '04-turkce-2', label: '2. Sınıf Türkçe', ids: ids('u', 1, 90), source: path.join(ROOT, 'artifacts/turkce2-90-inceleme/screens') },
  { folder: '05-matematik-2', label: '2. Sınıf Matematik — Güncellenenler', ids: [...ids('v', 1, 15), 'v21', 'v23', 'v24', 'v25', 'v31', 'v34', 'v36'], source: path.join(ROOT, 'artifacts/matematik-103-inceleme/screens') }
];

function copyExisting(group) {
  const target = path.join(OUT, group.folder);
  fs.mkdirSync(target, { recursive: true });
  for (const id of group.ids) {
    const source = path.join(group.source, `${id}.png`);
    if (!fs.existsSync(source)) throw new Error(`Kaynak ekran görüntüsü eksik: ${source}`);
    fs.copyFileSync(source, path.join(target, `${id}.png`));
  }
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  for (const group of GROUPS.filter(x => x.source)) copyExisting(group);

  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.GALLERY_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--allow-file-access-from-files', '--disable-speech-api']
  });
  const page = await browser.newPage({ viewport: VIEWPORT, deviceScaleFactor: 1 });
  const manifest = [];
  for (const group of GROUPS) {
    const target = path.join(OUT, group.folder);
    fs.mkdirSync(target, { recursive: true });
    if (group.capture) {
      const base = pathToFileURL(path.join(ASSETS, group.file)).href;
      for (const id of group.ids) {
        await page.goto(`${base}?bundle=257&id=${id}#oyun=${id}`, { waitUntil: 'domcontentloaded' });
        await page.waitForSelector('.hud');
        await page.waitForTimeout(90);
        const title = await page.evaluate(() => game.title);
        await page.screenshot({ path: path.join(target, `${id}.png`) });
        manifest.push({ id, title, group: group.label, file: `${group.folder}/${id}.png` });
        process.stdout.write(`✓ ${id} ${title}\n`);
      }
    } else {
      for (const id of group.ids) manifest.push({ id, title: '', group: group.label, file: `${group.folder}/${id}.png` });
    }
  }
  await browser.close();

  const actual = GROUPS.reduce((sum, group) => sum + group.ids.length, 0);
  if (actual !== 257) throw new Error(`Paket sayısı 257 yerine ${actual}`);
  fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify({ viewport: VIEWPORT, count: actual, games: manifest }, null, 2));
  fs.writeFileSync(path.join(OUT, 'README.txt'), [
    'GÜNCELLENEN 257 OYUN — TELEFON EKRAN GÖRÜNTÜLERİ',
    'Boyut: 390 x 844 px',
    '',
    ...GROUPS.map(group => `${group.folder}: ${group.ids.length} oyun — ${group.label}`),
    '',
    `TOPLAM: ${actual} oyun`
  ].join('\n'));
  console.log(`\n${actual} oyunluk paket hazır: ${OUT}`);
})().catch(error => { console.error(error); process.exitCode = 1; });
