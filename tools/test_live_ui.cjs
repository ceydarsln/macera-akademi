/* Two isolated browser sessions exercise the real arena UI with a local API double.
 * Run with NODE_PATH pointing to Playwright and LIVE_TEST_CHROME pointing to Chrome. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const url = pathToFileURL(path.resolve(__dirname, '../web/macera-akademi.html')).href;
const now = () => new Date().toISOString();
const screenshotDir = process.env.LIVE_TEST_SCREENSHOTS || '';
if (screenshotDir) fs.mkdirSync(screenshotDir, { recursive: true });
async function capture(page, name) {
  if (!screenshotDir) return;
  await page.evaluate(() => {
    window.scrollTo(0, 0);
    document.querySelector('.app-shell').scrollTop = 0;
  });
  await page.waitForTimeout(350);
  if (process.env.LIVE_TEST_DEBUG) {
    const detail = await page.evaluate(() => {
      const top = document.querySelector('.dl-top');
      const title = top && top.querySelector('.dl-top-t');
      const primary = [...document.querySelectorAll('button')].find(b => /Kabul et|Ödülümü Al/.test(b.textContent));
      return { scrollY: window.scrollY, bodyTop: document.body.scrollTop,
        shellScroll: document.querySelector('.app-shell').scrollTop,
        top: top && { y: top.getBoundingClientRect().top, height: top.getBoundingClientRect().height,
          text: top.textContent.trim(), visibility: getComputedStyle(top).visibility },
        title: title && { rect: title.getBoundingClientRect().toJSON(), color: getComputedStyle(title).color,
          opacity: getComputedStyle(title).opacity, display: getComputedStyle(title).display },
        hit: document.elementFromPoint(100,30)?.outerHTML.slice(0,120),
        button: primary && { text: primary.textContent.trim(), disabled: primary.disabled,
          color: getComputedStyle(primary).color, background: getComputedStyle(primary).backgroundColor,
          opacity: getComputedStyle(primary).opacity } };
    });
    console.log(name, detail);
  }
  await page.screenshot({ path: path.join(screenshotDir, name + '.png'), animations: 'disabled' });
}
let match = null;
let nextId = 1;
let claims = new Set();

function view(uid) {
  const from = uid === '101';
  const own = from ? 'from' : 'to';
  const other = from ? 'to' : 'from';
  const current = { ...match };
  delete current.ready;
  delete current.score;
  delete current.correct;
  delete current.answers;
  return {
    ...current,
    myReady: match.ready[own], opponentReady: match.ready[other],
    myScore: match.score[own], opponentScore: match.score[other],
    myCorrect: match.correct[own], opponentCorrect: match.correct[other],
    myAnswered: match.answers[own].length, opponentAnswered: match.answers[other].length,
    rewardClaimed: claims.has(uid),
    serverNow: now(), questionCount: 8, secondsPerQuestion: 12,
    questionIndex: match.status === 'playing' ? match.questionIndex : undefined,
    question: match.status === 'playing'
      ? { q: `2 + ${match.questionIndex + 2} kaç eder?`,
        opts: [3, 4, 5, 6].map(n => String(n + match.questionIndex)), category: 'Toplama' }
      : undefined,
    myAnswer: match.answers[own].find(a => a.questionIndex === match.questionIndex) || null,
    myAnswers: match.status === 'finished'
      ? match.answers[own].map(answer => ({ questionIndex: answer.questionIndex, correct: answer.correct }))
      : undefined,
  };
}

async function mockApi(uid, action, data = {}) {
  if (action === 'live_list') {
    if (!match) return { matches: [] };
    return { matches: [{ ...view(uid), fromScore: match.score.from, toScore: match.score.to }] };
  }
  if (action === 'live_invite') {
    assert.equal(uid, '101');
    assert.equal(data.oppUid, '102');
    match = {
      id: String(nextId++), status: 'invited', from: '101', to: '102',
      fromName: 'Oyuncu A', toName: 'Oyuncu B', grade: 1,
      catId: data.catId, catLabel: 'Toplama',
      inviteExpiresAt: new Date(Date.now() + 60000).toISOString(),
      lobbyExpiresAt: null, startsAt: null, endsAt: null,
      ready: { from: false, to: false }, score: { from: 0, to: 0 },
      correct: { from: 0, to: 0 }, answers: { from: [], to: [] }, questionIndex: 0,
      winner: null, finishReason: null, forfeitUserId: null,
    };
    return { match: view(uid) };
  }
  assert.ok(match && data.matchId === match.id, 'match id');
  if (action === 'live_accept') {
    match.status = 'lobby';
    match.lobbyExpiresAt = new Date(Date.now() + 120000).toISOString();
  } else if (action === 'live_ready') {
    match.ready[uid === '101' ? 'from' : 'to'] = true;
    if (match.ready.from && match.ready.to) {
      match.status = 'countdown';
      match.startsAt = new Date(Date.now() + 3000).toISOString();
      match.endsAt = new Date(Date.now() + 99000).toISOString();
    }
  } else if (action === 'live_state') {
    if (match.status === 'countdown' && Date.now() >= Date.parse(match.startsAt)) match.status = 'playing';
  } else if (action === 'live_answer') {
    assert.equal(match.status, 'playing');
    const side = uid === '101' ? 'from' : 'to';
    assert.equal(data.questionIndex, match.questionIndex);
    assert.equal(match.answers[side].length, match.questionIndex);
    const correct = data.optionIndex === 1;
    const answer = { questionIndex: match.questionIndex,
      optionIndex: data.optionIndex, correct, points: correct ? 20 : 0 };
    match.answers[side].push(answer);
    match.score[side] += answer.points;
    match.correct[side] += Number(correct);
    if (match.answers.from.length > match.questionIndex &&
        match.answers.to.length > match.questionIndex) {
      if (match.questionIndex === 7) {
        match.status = 'finished';
        match.winner = match.score.from === match.score.to ? 'draw'
          : match.score.from > match.score.to ? '101' : '102';
        match.finishReason = 'score';
      } else {
        // Advance the fake server clock; production uses full 12-second windows.
        match.questionIndex++;
        match.startsAt = new Date(Date.now() - match.questionIndex * 12000).toISOString();
      }
    }
    return { match: view(uid), answer };
  } else if (action === 'live_claim') {
    const claimed = !claims.has(uid);
    claims.add(uid);
    return { claimed, match: view(uid),
      reward: { result: match.winner === uid ? 'win' : 'loss', xp: 65, coin: 35,
        levelBonus: 0, lines: [['Zafer', 40, 20], ['Kusursuz 8/8', 25, 15]] },
      profile: { level: 1, xp: 65, coins: 35, coinsEarned: 35,
        duelStats: { wins: match.winner === uid ? 1 : 0 } } };
  } else if (action === 'live_leave') {
    match.status = 'cancelled';
  }
  return { match: view(uid) };
}

async function session(browser, uid, name) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.exposeFunction('mockLiveApi', (action, data) => mockApi(uid, action, data));
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.evaluate(({ uid, name }) => {
    window.myUid = () => uid;
    window.liveApiCall = (action, data) => window.mockLiveApi(action, data);
    state.isGuest = false;
    state.loggedIn = true;
    state.currentUser = name;
    state.hero.name = name;
    state.hero.grade = 1;
    go('home');
  }, { uid, name });
  return { context, page, errors };
}

(async () => {
  const browser = await chromium.launch({
    headless: true, executablePath: process.env.LIVE_TEST_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  });
  try {
    const a = await session(browser, '101', 'Oyuncu A');
    const b = await session(browser, '102', 'Oyuncu B');
    await a.page.evaluate(() => liveInvite('102', 'Oyuncu B', 'topla'));
    await a.page.getByText('Arkadaşının kabul etmesini bekliyoruz').waitFor();
    await b.page.evaluate(() => openArena());
    await b.page.getByText('Oyuncu A seni davet etti').waitFor();
    await capture(b.page, '01-davet-arena');
    await b.page.getByRole('button', { name: 'Kabul et' }).first().click();
    await b.page.getByRole('button', { name: 'Daveti Kabul Et' }).click();
    await a.page.getByRole('button', { name: 'Hazırım!' }).waitFor();
    await a.page.getByRole('button', { name: 'Hazırım!' }).click();
    await a.page.getByText('Rakibin bekleniyor').waitFor();
    await a.page.locator('#toastEl').waitFor({ state: 'detached', timeout: 4000 });
    await capture(a.page, '02-bekleme-odasi');
    await b.page.getByRole('button', { name: 'Hazırım!' }).click();
    await a.page.getByText('İkiniz de hazırsınız!').waitFor();
    // Simulate leaving the screen and reopening the same in-progress match.
    await b.page.evaluate(() => { go('home'); return liveOpen('1'); });
    for (let question = 0; question < 8; question++) {
      const prompt = `2 + ${question + 2} kaç eder?`;
      await a.page.getByText(prompt).waitFor({ timeout: 8000 });
      await b.page.getByText(prompt).waitFor({ timeout: 8000 });
      if (question === 0) await capture(a.page, '03-canli-soru');
      await a.page.getByRole('button', { name: String(question + 4), exact: true }).click();
      await b.page.getByRole('button', { name: String(question + 3), exact: true }).click();
    }
    await a.page.getByText('ZAFER!').waitFor();
    await b.page.getByText('BU KEZ OLMADI').waitFor();
    await capture(a.page, '04-sonuc');
    await capture(b.page, '06-rakip-sonucu');
    await a.page.getByRole('button', { name: 'Ödülümü Al' }).click();
    await a.page.getByText('Ödül hesabına eklendi').waitFor();
    await a.page.locator('#toastEl').waitFor({ state: 'detached', timeout: 4000 });
    await capture(a.page, '05-odul');
    const repeated = await a.page.evaluate(() => liveApiCall('live_claim', { matchId: '1' }));
    assert.equal(repeated.claimed, false, 'repeated claim stays idempotent');
    assert.equal(claims.size, 1);
    assert.deepEqual(a.errors, []);
    assert.deepEqual(b.errors, []);
    console.log('Canlı UI: iki oturum, davet, kabul, hazır, 8 ortak soru, cevap, sonuç, ödül başarılı.');
    await a.context.close();
    await b.context.close();
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
