'use strict';

// Tasarım denetimi: başlangıç ekranlarını inceler; oynanış/animasyon onayı vermez.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
const sharp = require('sharp');
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'artifacts', 'tasarim-denetimi-2026-09-21');
const ids = (p, n, start = 1, width = 2) => Array.from({ length: n }, (_, i) => p + String(i + start).padStart(width, '0'));
const GROUPS = [
  ['sayma', 'Sayma–Rakam', [...ids('s', 11, 0, 1), ...ids('n', 9, 1, 1)]],
  ['matematik', '1. Sınıf Matematik', ids('m', 61)],
  ['turkce1', '1. Sınıf Türkçe', ids('t', 64)],
  ['matematik2', '2. Sınıf Matematik', ids('v', 42)],
  ['turkce2', '2. Sınıf Türkçe', ids('u', 90)],
  ['matematik3', '3. Sınıf Matematik', ids('w', 48)],
  ['turkce3', '3. Sınıf Türkçe', ids('y', 64)],
  ['matematik4', '4. Sınıf Matematik', ids('p', 56)],
  ['turkce4', '4. Sınıf Türkçe', ids('z', 64)],
  ['fen3', '3. Sınıf Fen', ids('g', 48)],
  ['fen4', '4. Sınıf Fen', ids('f', 48)],
  ['hayatbilgisi2', '2. Sınıf Hayat Bilgisi H01–H30', ids('h', 30)]
];
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
function sourceAudit(slug) {
  const file = `web/phaser/${slug}-pdf-phaser.html`;
  const current = fs.readFileSync(path.join(ROOT, file), 'utf8');
  const prior = execFileSync('git', ['show', `3258e70:${file}`], { cwd: ROOT, encoding: 'utf8' });
  const frames = s => [...s.matchAll(/@keyframes\s+([\w-]+)/g)].map(m => m[1]);
  const before = frames(prior), after = frames(current);
  const diff = execFileSync('git', ['diff', '--numstat', '3258e70', '--', file], { cwd: ROOT, encoding: 'utf8' }).trim();
  return { file, changedSinceCheckpoint: current !== prior, diff, keyframes: after, addedKeyframes: after.filter(x => !before.includes(x)), note: 'CSS sayımı tek başına animasyon kalitesi ölçmez; JS/SVG hareketleri ayrıca incelenmelidir.' };
}

// CSS/SVG ile çizilen nesneler salt SVG varlığına göre sınıflandırılmaz.
// Etiket kutusu sinyalleri özellikle bilinen ortak şablon seçicilerinden alınır.
async function inspect(page) {
  return page.evaluate(() => {
    const stage = document.querySelector('#stage,#visual');
    const visible = el => { const b = el.getBoundingClientRect(), s = getComputedStyle(el); return b.width > 0 && b.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
    const rect = el => { const b = el.getBoundingClientRect(); return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height) }; };
    const targetSelector = '[data-target],[data-yuva],[data-sira-hedef],[data-kutu],[data-canta-hedef],[data-kur-hedef],[data-topla-hedef],[data-process-target],[data-multi-target],[data-slot],[data-tepsi],[data-sira-yuva]';
    const targets = [...document.querySelectorAll(targetSelector)].filter(visible).map(el => ({
      tag: el.tagName, classes: typeof el.className === 'string' ? el.className : el.getAttribute('class'),
      attributes: [...el.attributes].filter(a => a.name.startsWith('data-')).map(a => [a.name, a.value]),
      text: el.textContent.trim().slice(0, 160), insideScene: !!stage?.contains(el),
      svg: !!el.querySelector('svg'), rect: rect(el)
    }));
    const generic = [...document.querySelectorAll('[data-sira-hedef],.yuvakart,[data-kutu],.canta-kutu,.kap[data-kur-hedef]')].filter(visible).map(el => ({ classes: el.getAttribute('class'), text: el.textContent.trim().slice(0, 120) }));
    const prompt = document.querySelector('.prompt');
    const clipping = [...document.querySelectorAll('.prompt,button,.piece,.sirakart,.etiket')].filter(visible).filter(el => {
      const s = getComputedStyle(el); return (['hidden', 'clip'].includes(s.overflowY) && el.scrollHeight > el.clientHeight + 3) || (['hidden', 'clip'].includes(s.overflowX) && el.scrollWidth > el.clientWidth + 3);
    }).map(el => ({ tag: el.tagName, classes: el.getAttribute('class'), text: el.textContent.trim().slice(0, 160), rect: rect(el) }));
    const animations = document.getAnimations().map(a => ({ name: a.animationName || 'WAAPI/transition', target: a.effect?.target?.getAttribute?.('class') || a.effect?.target?.tagName }));
    const r = round();
    return { round: roundIndex + 1, kind: r.kind || 'choose', theme: r.theme || game.theme,
      prompt: prompt?.textContent, targets, genericTargets: generic, clipping,
      stage: stage ? rect(stage) : null, idleAnimations: animations,
      sceneDependsOnState: ['scene','sahne','art'].filter(k => typeof r[k] === 'function'),
      sceneControls: stage ? [...stage.querySelectorAll('button,[role="button"],input,[data-target],[data-scene-action],[data-scene-choice]')].filter(visible).length : 0,
      taskControls: [...document.querySelectorAll('#task button,#task input,#task [data-piece]')].filter(visible).length,
      horizontallyOutside: [...document.querySelectorAll('button,.piece')].filter(visible).filter(el => { const b = el.getBoundingClientRect(); return b.right > innerWidth + 3 || b.left < -3; }).map(el => el.textContent.trim().slice(0, 80))
    };
  });
}

async function contactSheet(items, filename) {
  if (!items.length) return;
  const composites = [], cellW = 208, cellH = 464, cols = 6;
  for (let i = 0; i < items.length; i++) {
    const x = i % cols * cellW, y = Math.floor(i / cols) * cellH;
    composites.push({ input: await sharp(path.join(OUT, items[i].screenshot)).resize(195, 422).toBuffer(), left: x + 6, top: y + 36 });
    const label = `<svg width="208" height="36"><rect width="208" height="36" fill="#18324a"/><text x="7" y="14" fill="white" font-size="12" font-family="Arial">${esc(items[i].id.toUpperCase())} · ${esc(items[i].rounds[0].kind)}</text><text x="7" y="29" fill="white" font-size="10" font-family="Arial">${esc(items[i].title.slice(0, 31))}</text></svg>`;
    composites.push({ input: Buffer.from(label), left: x, top: y });
  }
  await sharp({ create: { width: cols * cellW, height: Math.ceil(items.length / cols) * cellH, channels: 4, background: '#dfedf3' } }).composite(composites).png().toFile(path.join(OUT, filename));
}

async function main() {
  fs.mkdirSync(path.join(OUT, 'screens'), { recursive: true });
  const sources = Object.fromEntries(GROUPS.map(([slug]) => [slug, sourceAudit(slug)]));
  const browser = await chromium.launch({ headless: true, executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', args: ['--allow-file-access-from-files', '--disable-speech-api'] });
  const results = [];
  let next = 0;
  const jobs = GROUPS.flatMap(([slug, label, games]) => games.map(id => ({ slug, label, id })));
  try {
    await Promise.all([0, 1].map(async () => {
      while (next < jobs.length) {
        const job = jobs[next++], errors = [];
        const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
        await page.addInitScript(() => { try { speechSynthesis.speak = () => {}; speechSynthesis.cancel = () => {}; } catch (_) {} });
        page.on('pageerror', e => errors.push(e.message));
        const entry = { ...job, rounds: [] };
        try {
          const file = pathToFileURL(path.join(ROOT, `app/src/main/assets/phaser/${job.slug}-pdf.html`)).href;
          // Kimlik sorguda da yer alır: yalnız hash değişirse eski belge okunabilir.
          await page.goto(`${file}?design-audit=20260921&id=${job.id}#oyun=${job.id}`, { waitUntil: 'load' });
          const metadata = await page.evaluate(() => ({ title: game.title, count: game.rounds.length, actualId: GAME_ID }));
          if (metadata.actualId !== job.id) throw new Error(`Kimlik uyuşmazlığı: ${metadata.actualId} / ${job.id}`);
          Object.assign(entry, metadata);
          for (let i = 0; i < metadata.count; i++) {
            // Yalnız tur başlangıç görünümü. Tur çözülmüş sayılmaz.
            if (i > 0) await page.evaluate(n => { roundIndex = n; state = {}; locked = false; render(); }, i);
            await page.waitForTimeout(75);
            entry.rounds.push(await inspect(page));
            if (i === 0) {
              entry.screenshot = `screens/${job.slug}-${job.id}.png`;
              await page.screenshot({ path: path.join(OUT, entry.screenshot) });
            }
          }
        } catch (e) { entry.error = e.message; console.log(`${job.slug}/${job.id}: ${e.message.slice(0, 250)}`); }
        entry.errors = [...new Set(errors)]; results.push(entry);
        await page.close();
        fs.writeFileSync(path.join(OUT, 'partial.json'), JSON.stringify(results));
        if (results.length % 50 === 0) console.log(`${results.length}/${jobs.length} başlangıç ekranı tarandı`);
      }
    }));
  } finally { await browser.close(); }
  results.sort((a, b) => jobs.findIndex(x => x.slug === a.slug && x.id === a.id) - jobs.findIndex(x => x.slug === b.slug && x.id === b.id));
  const groups = [];
  for (const [slug, label] of GROUPS) {
    const games = results.filter(x => x.slug === slug);
    const representative = [], seen = new Set();
    for (const g of games.filter(g => g.rounds.length && g.screenshot)) {
      const kind = g.rounds[0].kind;
      if (!seen.has(kind) && representative.length < 12) { seen.add(kind); representative.push(g); }
    }
    const sheet = `${slug}-ornekler.png`;
    await contactSheet(representative, sheet);
    groups.push({ slug, label, count: games.length, rounds: games.reduce((n,g) => n + g.rounds.length, 0),
      gamesWithGenericTargets: games.filter(g => g.rounds.some(r => r.genericTargets.length)).length,
      gamesWithClippingSignals: games.filter(g => g.rounds.some(r => r.clipping.length)).length,
      gamesWithOutsideSignals: games.filter(g => g.rounds.some(r => r.horizontallyOutside.length)).length,
      gamesWithExternalTargets: games.filter(g => g.rounds.some(r => r.targets.some(t => !t.insideScene))).length,
      errors: games.filter(g => g.error || g.errors.length).length,
      representativeIds: representative.map(g => g.id), sheet, source: sources[slug] });
  }
  const report = { date: '2026-09-21', commit: execFileSync('git',['rev-parse','--short','HEAD'],{cwd:ROOT,encoding:'utf8'}).trim(),
    method: '635 oyun kapsamı; tüm turların başlangıç DOM ölçümleri, oyun başına ilk turun ekran görüntüsü. Otomatik sinyaller tasarım kusuru veya onay hükmü değildir. Canlı etkileşim ve anlamlı animasyon için seçilmiş örnekler ayrıca incelenir.',
    groups, games: results };
  fs.writeFileSync(path.join(OUT, 'audit.json'), JSON.stringify(report, null, 2));
  const table = groups.map(g => `<tr><td><a href="#${g.slug}">${esc(g.label)}</a></td><td>${g.count}</td><td>${g.rounds}</td><td>${g.gamesWithGenericTargets}</td><td>${g.gamesWithClippingSignals}</td><td>${g.gamesWithExternalTargets}</td></tr>`).join('');
  const sections = groups.map(g => `<section id="${g.slug}"><h2>${esc(g.label)}</h2><a href="${g.sheet}">Mekaniklerden seçilmiş örnek paftası</a><div class="grid">${results.filter(x => x.slug === g.slug).map(x => `<article><b>${esc(x.id.toUpperCase())} · ${esc(x.title || '')}</b><a href="${x.screenshot}"><img loading="lazy" src="${x.screenshot}" alt="${esc(x.id)} başlangıç ekranı"></a><p>${esc([...new Set(x.rounds.map(r => r.kind))].join(', '))}</p><small>${x.rounds.some(r=>r.genericTargets.length)?'Ortak kart/kutu hedefi — tasarım incelemesi gerekli':'Bu seçicilerde ortak kutu sinyali yok; kalite onayı değildir'}</small></article>`).join('')}</div></section>`).join('');
  fs.writeFileSync(path.join(OUT, 'index.html'), `<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Oyun tasarım denetimi</title><style>body{font:16px system-ui;background:#edf3f8;color:#18324a;margin:24px}table{border-collapse:collapse;width:100%}th,td{padding:8px;border:1px solid #adbdc9;text-align:left}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(205px,1fr));gap:18px}article{background:white;padding:10px;border-radius:12px}img{width:100%;margin-top:8px}small{display:block}a{color:#14558c}section{margin-top:40px}</style><h1>Önceki paketler · tasarım denetimi</h1><p>${esc(report.method)}</p><p>Oyun dosyaları değiştirilmedi. Rakamlar otomatik inceleme sinyalleridir; oyunların tamamının elle oynandığı anlamına gelmez.</p><table><tr><th>Paket</th><th>Oyun</th><th>Tur başlangıcı</th><th>Kart/kutu sinyali</th><th>Metin kırpma sinyali</th><th>Sahne dışı hedef</th></tr>${table}</table>${sections}</html>`);
  console.log(JSON.stringify(groups.map(({source, ...g}) => ({...g, addedKeyframes:source.addedKeyframes, changedSinceCheckpoint:source.changedSinceCheckpoint})), null, 2));
  console.log(`Rapor: ${OUT}`);
}
main().catch(e => { console.error(e); process.exitCode = 1; });
