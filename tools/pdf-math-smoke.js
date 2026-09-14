'use strict';

/*
 * PDF'lerdeki 49 matematik oyununun 147 turunu tarayıcıda gerçekten
 * etkileşerek tamamlayan regresyon testi. Görsel incelemenin yerine geçmez;
 * sürükleme, seçim, sayaç, hafıza ve veri toplama akışlarının kırılmadığını
 * hızlıca kanıtlar.
 */
const { chromium } = require('playwright');

const ALL_IDS = [
  'm01','m02','m03','m05','m09','m10','m11','m12','m14','m15','m17','m18',
  'm20','m22','m23','m24','m25','m26','m28','m31','m32','m33','m34','m35',
  'm36','m37','m38','m39','m41','m42','m43','m44','m45','m46','m47','m48',
  'm49','m50','m51','m52','m53','m54','m55','m56','m57','m58','m59','m60','m61'
];
const IDS = process.env.PDF_MATH_IDS
  ? process.env.PDF_MATH_IDS.split(',').map(x => x.trim()).filter(Boolean)
  : ALL_IDS;

const BASE = process.env.PDF_MATH_URL ||
  'http://127.0.0.1:8871/app/src/main/assets/phaser/matematik-pdf.html';

async function move(page, pieceSelector, targetSelector) {
  const moved = await page.evaluate(({ pieceSelector, targetSelector }) => {
    const piece = document.querySelector(pieceSelector);
    const target = document.querySelector(targetSelector);
    if (!piece || !target) return { ok:false };
    const bound = typeof piece.onpointerdown;
    target.scrollIntoView({ block: 'center' });
    const a = piece.getBoundingClientRect();
    const start = { clientX: a.left + a.width / 2, clientY: a.top + a.height / 2 };
    piece.dispatchEvent(new PointerEvent('pointerdown', { ...start, pointerId: 41, bubbles: true }));
    const b = target.getBoundingClientRect();
    const end = { clientX: b.left + b.width / 2, clientY: b.top + b.height / 2 };
    piece.dispatchEvent(new PointerEvent('pointermove', { ...end, pointerId: 41, bubbles: true }));
    piece.dispatchEvent(new PointerEvent('pointerup', { ...end, pointerId: 41, bubbles: true }));
    return { ok:true, bound, up:typeof piece.onpointerup, dragActive:!!drag,
      state: JSON.parse(JSON.stringify(state)) };
  }, { pieceSelector, targetSelector });
  if (!moved.ok) throw new Error(`Sürükleme öğesi bulunamadı: ${pieceSelector} → ${targetSelector}`);
  if (process.env.PDF_MATH_DEBUG) console.log('drag', pieceSelector, targetSelector, moved);
  await page.waitForTimeout(80);
}

async function moveMany(page, moves) {
  const result = await page.evaluate(sequence => {
    for (let i = 0; i < sequence.length; i++) {
      const { pieceSelector, targetSelector } = sequence[i];
      const piece = document.querySelector(pieceSelector);
      const target = document.querySelector(targetSelector);
      if (!piece || !target) return { ok:false, index:i, pieceSelector, targetSelector };
      const a = piece.getBoundingClientRect();
      const start = { clientX:a.left + a.width / 2, clientY:a.top + a.height / 2 };
      const b = target.getBoundingClientRect();
      const end = { clientX:b.left + b.width / 2, clientY:b.top + b.height / 2 };
      const pointerId = 70 + i;
      piece.dispatchEvent(new PointerEvent('pointerdown', { ...start, pointerId, bubbles:true }));
      piece.dispatchEvent(new PointerEvent('pointermove', { ...end, pointerId, bubbles:true }));
      piece.dispatchEvent(new PointerEvent('pointerup', { ...end, pointerId, bubbles:true }));
    }
    return { ok:true, state:JSON.parse(JSON.stringify(state)) };
  }, moves);
  if (!result.ok) {
    throw new Error(`Toplu sürükleme öğesi bulunamadı (${result.index}): ${result.pieceSelector} → ${result.targetSelector}`);
  }
  if (process.env.PDF_MATH_DEBUG) console.log('batch', moves.length, result.state);
  await page.waitForTimeout(30);
}

async function info(page) {
  return page.evaluate(() => {
    const r = round();
    return {
      kind: r.kind || 'choose',
      choices: r.choices || [],
      stages: r.stages || [],
      pieces: r.pieces || [],
      expected: r.expected || [],
      options: r.options || [],
      start: r.start || 0,
      target: r.target,
      targetCount: r.targetCount,
      removeCount: r.removeCount,
      sequence: r.sequence || [],
      pairs: r.pairs || [],
      items: r.items || [],
      responses: r.responses || [],
      finalChoices: r.finalChoices || []
    };
  });
}

async function verifyIdentityAndLayout(page, id) {
  const audit = await page.evaluate(expectedId => {
    const scene = document.querySelector('.scene');
    const atmosphere = document.querySelector('.scene-atmosphere');
    const particles = document.querySelector('.success-particles');
    const overflow = [...document.querySelectorAll('.hud,.visual,.task,[data-choice],.piece,.target,.action,.sound')]
      .filter(el => {
        const r = el.getBoundingClientRect();
        return r.width > 0 && (r.left < -1 || r.right > innerWidth + 1);
      })
      .map(el => el.className || el.tagName);
    return {
      hasIdentity: !!scene?.classList.contains(`game-${expectedId}`),
      motion: [...(scene?.classList || [])].find(x => x.startsWith('motion-')) || '',
      accent: scene?.style.getPropertyValue('--scene-accent') || '',
      atmosphereCount: atmosphere?.children.length || 0,
      particleCount: particles?.children.length || 0,
      horizontalOverflow: overflow
    };
  }, id);
  if (!audit.hasIdentity || !audit.motion || !audit.accent ||
      audit.atmosphereCount !== 4 || audit.particleCount !== 8 ||
      audit.horizontalOverflow.length) {
    throw new Error(`Sahne kimliği/yerleşim denetimi başarısız: ${JSON.stringify(audit)}`);
  }
}

async function clickCorrect(page, choices) {
  const i = choices.findIndex(x => x.correct);
  if (i < 0) throw new Error('Doğru seçenek tanımlı değil');
  await page.locator(`[data-choice="${i}"]`).click();
}

async function finishRound(page) {
  const r = await info(page);
  switch (r.kind) {
    case 'choose':
    case 'pattern':
    case 'estimate':
    case 'plateChoice':
      await clickCorrect(page, r.choices);
      break;
    case 'stages':
      for (const stage of r.stages) {
        await clickCorrect(page, stage.choices);
        await page.waitForTimeout(720);
      }
      break;
    case 'drag':
      await moveMany(page, r.pieces.filter(x => x.target).map(p => ({
        pieceSelector:`[data-piece="${p.id}"]`,
        targetSelector:`[data-target="${p.target}"]`
      })));
      break;
    case 'grid': {
      const correct = await page.evaluate(() => {
        const r = round();
        return r.start + r.dx + r.dy * 5;
      });
      await page.locator(`[data-cell="${correct}"]`).click();
      break;
    }
    case 'sequence':
      for (const expected of r.expected) {
        const i = r.options.findIndex(x => x.value === expected);
        await page.locator(`[data-choice="${i}"]`).click();
        await page.waitForTimeout(70);
      }
      break;
    case 'count':
      for (let i = 0; i < Math.abs(r.target - r.start); i++) {
        await page.locator('[data-delta]').first().click();
        await page.waitForTimeout(35);
      }
      break;
    case 'load':
    case 'balanceLoad':
      await moveMany(page, Array.from({ length:r.targetCount - r.start }, () => ({
        pieceSelector:'[data-piece="supply"]',
        targetSelector:'[data-target="loadTarget"]'
      })));
      break;
    case 'countDrag':
      await moveMany(page, Array.from({ length:r.start - r.target }, (_,i) => ({
        pieceSelector:`[data-piece="n${r.start - 1 - i}"]`,
        targetSelector:'[data-target="countTarget"]'
      })));
      break;
    case 'remove':
      await moveMany(page, Array.from({ length:r.removeCount }, () => ({
        pieceSelector:'[data-piece]',
        targetSelector:'[data-target="returnCart"]'
      })));
      await clickCorrect(page, r.choices);
      break;
    case 'memory':
      await page.evaluate(() => { state.remaining = 1; });
      await page.waitForTimeout(1200);
      await clickCorrect(page, r.choices);
      break;
    case 'diff':
      for (let i = 0; i < r.pairs.length; i++) {
        if (r.pairs[i][2]) await page.locator(`[data-diff="${i}"]`).first().click();
      }
      break;
    case 'multi':
      for (const item of r.items.filter(x => x.correct)) {
        await page.locator(`[data-item="${item.id}"]`).click();
      }
      break;
    case 'catch':
      await moveMany(page, r.sequence.map(color => ({
        pieceSelector:'[data-piece="hook"]',
        targetSelector:`[data-target="${color}"]`
      })));
      break;
    case 'survey':
      for (const response of r.responses) {
        await page.locator('#ask').click();
        await page.locator(`[data-col="${response.id}"]`).click();
      }
      await clickCorrect(page, r.finalChoices);
      break;
    default:
      throw new Error(`Bilinmeyen mekanik: ${r.kind}`);
  }
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.PDF_MATH_CHROME ||
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const page = await browser.newPage({
    viewport: { width: 390, height: 844 },
    reducedMotion: 'reduce'
  });
  const failures = [];
  const consoleErrors = [];
  page.on('pageerror', e => consoleErrors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });

  for (const id of IDS) {
    try {
      await page.goto(`${BASE}?smoke=${id}#oyun=${id}`, { waitUntil: 'domcontentloaded' });
      await page.waitForSelector('.hud .round');
      await verifyIdentityAndLayout(page, id);
      for (let turn = 1; turn <= 3; turn++) {
        const label = `Tur ${turn}/3`;
        const visible = await page.locator('.hud .round').textContent();
        if (visible.trim() !== label) throw new Error(`Beklenen ${label}, görünen ${visible}`);
        await finishRound(page);
        if (turn < 3) await page.waitForFunction(
          expected => document.querySelector('.hud .round')?.textContent.trim() === expected,
          `Tur ${turn + 1}/3`, { timeout: 4000 }
        );
        else {
          await page.waitForTimeout(220);
          if (await page.locator('.overlay').count() !== 1) {
            throw new Error('Tamamlama katmanı oluşmadı');
          }
        }
      }
      process.stdout.write(`✓ ${id}\n`);
    } catch (e) {
      let snapshot = '';
      try {
        snapshot = JSON.stringify(await page.evaluate(() => ({
          roundIndex,
          round: document.querySelector('.hud .round')?.textContent,
          state,
          lives,
          overlay: document.querySelector('.overlay-card')?.innerText || ''
        })));
      } catch (_) {}
      failures.push(`${id}: ${e.message} ${snapshot}`);
      process.stdout.write(`✗ ${id}: ${e.message} ${snapshot}\n`);
    }
  }

  await browser.close();
  console.log(`\n${IDS.length - failures.length}/${IDS.length} oyun, ${(IDS.length - failures.length) * 3}/${IDS.length * 3} tur geçti.`);
  if (consoleErrors.length) {
    console.error('Tarayıcı hataları:', [...new Set(consoleErrors)]);
  }
  if (failures.length || consoleErrors.length) process.exitCode = 1;
})().catch(e => { console.error(e); process.exitCode = 1; });
