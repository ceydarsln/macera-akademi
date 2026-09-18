'use strict';

const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
const sharp = require('sharp');

const ROOT = path.resolve(__dirname, '..');
const GAME_FILE = path.join(ROOT, 'app/src/main/assets/phaser/turkce2-pdf.html');
const OUT = path.join(ROOT, 'artifacts', 'turkce2-90-inceleme');
const SHOTS = path.join(OUT, 'screens');
const IDS = Array.from({ length: 90 }, (_, i) => `u${String(i + 1).padStart(2, '0')}`);
const VIEWPORT = { width: 390, height: 844 };

function xml(value) {
  return String(value).replace(/[<>&"']/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&apos;' }[c]));
}

function htmlPage(items) {
  const cards = items.map(x => `<article id="${x.id}"><header><b>${x.id.toUpperCase()}</b><span>${xml(x.title)}</span></header><a href="screens/${x.id}.png" target="_blank"><img src="screens/${x.id}.png" loading="lazy" alt="${x.id.toUpperCase()} ${xml(x.title)} telefon ekranı"></a></article>`).join('');
  const sheets = Array.from({ length: 9 }, (_, i) => `<a href="turkce2-${String(i * 10 + 1).padStart(2, '0')}-${String(i * 10 + 10).padStart(2, '0')}.png" target="_blank">${String(i * 10 + 1).padStart(2, '0')}–${String(i * 10 + 10).padStart(2, '0')}</a>`).join('');
  return `<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Türkçe 2 · U01–U90 İnceleme Galerisi</title><style>*{box-sizing:border-box}body{margin:0;background:#edf4f8;color:#18324a;font-family:system-ui,-apple-system,"Segoe UI",sans-serif}nav{position:sticky;top:0;z-index:5;padding:12px 16px;background:#17364d;color:white;box-shadow:0 3px 15px #17364d55}nav h1{margin:0 0 7px;font-size:20px}nav p{margin:0 0 8px;font-size:13px;opacity:.85}.sheets{display:flex;gap:7px;overflow:auto}.sheets a{color:#17364d;background:#fff;border-radius:10px;padding:5px 9px;text-decoration:none;font-weight:800;white-space:nowrap}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;padding:14px;max-width:1500px;margin:auto}article{overflow:hidden;border-radius:18px;background:#fff;box-shadow:0 7px 22px #18324a20;border:1px solid #c9dbe5}article header{min-height:55px;display:flex;gap:8px;align-items:center;padding:8px 10px}article header b{background:#17364d;color:white;border-radius:9px;padding:5px 7px}article header span{font-size:13px;font-weight:800;line-height:1.15}article a{display:block;background:#dcecf4}article img{display:block;width:100%;height:auto}</style></head><body><nav><h1>Türkçe 2 · 90 oyun telefon incelemesi</h1><p>Her görüntü 390 × 844 px. Büyütmek için oyuna dokunun. Onarlı özetler:</p><div class="sheets">${sheets}</div></nav><main>${cards}</main></body></html>`;
}

async function contactSheet(items, index) {
  const cellW = 236, cellH = 535, thumbW = 220, thumbH = 476;
  const composites = [];
  for (let i = 0; i < items.length; i++) {
    const col = i % 5, row = Math.floor(i / 5), left = col * cellW + 8, top = row * cellH + 45;
    const image = await sharp(path.join(SHOTS, `${items[i].id}.png`)).resize(thumbW, thumbH, { fit: 'fill' }).png().toBuffer();
    composites.push({ input: image, left, top });
    const label = `<svg width="${thumbW}" height="38"><rect width="100%" height="100%" rx="9" fill="#17364d"/><text x="10" y="17" fill="white" font-family="Arial,sans-serif" font-size="15" font-weight="700">${items[i].id.toUpperCase()}</text><text x="10" y="32" fill="white" font-family="Arial,sans-serif" font-size="11">${xml(items[i].title.slice(0, 31))}</text></svg>`;
    composites.push({ input: Buffer.from(label), left, top: row * cellH + 5 });
  }
  const first = index * 10 + 1, last = first + items.length - 1;
  await sharp({ create: { width: cellW * 5, height: cellH * 2, channels: 4, background: '#dcecf4' } })
    .composite(composites)
    .png()
    .toFile(path.join(OUT, `turkce2-${String(first).padStart(2, '0')}-${String(last).padStart(2, '0')}.png`));
}

(async () => {
  fs.mkdirSync(SHOTS, { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.GALLERY_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--allow-file-access-from-files', '--disable-speech-api']
  });
  const page = await browser.newPage({ viewport: VIEWPORT, deviceScaleFactor: 1 });
  const base = pathToFileURL(GAME_FILE).href;
  const items = [];
  for (const id of IDS) {
    await page.goto(`${base}?gallery=1&id=${id}#oyun=${id}`, { waitUntil: 'domcontentloaded' });
    await page.waitForSelector('.hud .round');
    await page.waitForTimeout(90);
    const title = await page.evaluate(() => game.title);
    await page.screenshot({ path: path.join(SHOTS, `${id}.png`) });
    items.push({ id, title });
    process.stdout.write(`✓ ${id} ${title}\n`);
  }
  await browser.close();
  for (let i = 0; i < 9; i++) await contactSheet(items.slice(i * 10, i * 10 + 10), i);
  fs.writeFileSync(path.join(OUT, 'index.html'), htmlPage(items));
  fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify({ viewport: VIEWPORT, count: items.length, games: items }, null, 2));
  console.log(`\n${items.length} ekran görüntüsü ve 9 inceleme sayfası: ${OUT}`);
})().catch(error => { console.error(error); process.exitCode = 1; });
