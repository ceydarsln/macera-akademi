#!/usr/bin/env node
// End-to-end live match against an isolated local PHP/MySQL server only.
const assert = require('node:assert/strict');

const base = process.env.LIVE_LOCAL_API || 'http://127.0.0.1:8872/api/index.php';
const url = new URL(base);
if (url.hostname !== '127.0.0.1' || url.protocol !== 'http:') {
  throw new Error('This test may only target an HTTP server on 127.0.0.1.');
}

async function call(action, data = {}, token = '', expectedStatus = 200) {
  const response = await fetch(base, {
    method: 'POST',
    headers: { 'content-type': 'application/json', ...(token ? { authorization: `Bearer ${token}` } : {}) },
    body: JSON.stringify({ action, ...data }),
  });
  const body = await response.json();
  assert.equal(response.status, expectedStatus, `${action}: ${JSON.stringify(body)}`);
  if (expectedStatus < 400) assert.equal(body.ok, true, `${action}: ${JSON.stringify(body)}`);
  return body;
}

async function main() {
  const suffix = Date.now().toString(36);
  const create = async (name) => (await call('register', {
    username: `${name}_${suffix}`, email: `${name}_${suffix}@example.invalid`,
    password: 'local-test-only', grade: 1,
  }, '', 201)).data;
  const a = await create('PlayerA');
  const b = await create('PlayerB');
  const aId = a.user.uid;
  const bId = b.user.uid;
  const aToken = a.token;
  const bToken = b.token;

  await call('live_invite', { oppUid: bId, catId: 'topla' }, aToken, 403);
  await call('friend_request', { uid: bId }, aToken);
  await call('friend_accept', { uid: aId }, bToken);
  const invited = await call('live_invite', { oppUid: bId, catId: 'topla' }, aToken, 201);
  const matchId = invited.data.match.id;
  assert.equal(invited.data.match.status, 'invited');
  assert.equal((await call('live_list', {}, bToken)).data.matches[0].id, matchId);
  assert.equal((await call('live_accept', { matchId }, bToken)).data.match.status, 'lobby');
  await call('live_ready', { matchId }, aToken);
  assert.equal((await call('live_ready', { matchId }, bToken)).data.match.status, 'countdown');

  const answered = new Set();
  const started = Date.now();
  let final = null;
  while (Date.now() - started < 110000) {
    const first = (await call('live_state', { matchId }, aToken)).data.match;
    const second = (await call('live_state', { matchId }, bToken)).data.match;
    if (first.status === 'finished') {
      final = first;
      break;
    }
    if (first.status === 'playing' && !answered.has(first.questionIndex)) {
      const index = first.questionIndex;
      const match = /<b>(\d+) \+ (\d+)<\/b>/.exec(first.question.q);
      assert.ok(match, `Unexpected addition question: ${first.question.q}`);
      const correct = String(Number(match[1]) + Number(match[2]));
      const correctIndex = first.question.opts.indexOf(correct);
      assert.ok(correctIndex >= 0, 'Correct option missing');
      const wrongIndex = first.question.opts.findIndex((option) => option !== correct);
      if (index === 0) {
        await call('live_answer', { matchId, questionIndex: index, optionIndex: 9 }, aToken, 422);
      }
      const aAnswer = (await call('live_answer', {
        matchId, questionIndex: index, optionIndex: correctIndex,
      }, aToken)).data.answer;
      assert.equal(aAnswer.correct, true);
      assert.ok(aAnswer.points > 0);
      if (index === 0) {
        await call('live_answer', {
          matchId, questionIndex: index, optionIndex: correctIndex,
        }, aToken, 409);
      }
      const bAnswer = (await call('live_answer', {
        matchId, questionIndex: index, optionIndex: wrongIndex,
      }, bToken)).data.answer;
      assert.equal(bAnswer.correct, false);
      answered.add(index);
      process.stdout.write(`Soru ${index + 1}/8: iki gerçek hesap yanıtladı.\n`);
      if (index === 1) {
        await call('live_answer', { matchId, questionIndex: 0, optionIndex: 0 }, aToken, 409);
      }
    }
    await new Promise((resolve) => setTimeout(resolve, 1500));
  }
  assert.equal(answered.size, 8, `Only ${answered.size} questions answered`);
  assert.ok(final, 'Match did not finish');
  assert.equal(final.finishReason, 'score');
  assert.equal(final.winner, aId);
  assert.equal(final.myCorrect, 8);
  assert.equal(final.opponentCorrect, 0);

  const firstClaim = (await call('live_claim', { matchId }, aToken)).data;
  const repeatedClaim = (await call('live_claim', { matchId }, aToken)).data;
  assert.equal(firstClaim.claimed, true);
  assert.equal(repeatedClaim.claimed, false);
  assert.deepEqual(repeatedClaim.profile, firstClaim.profile);
  assert.deepEqual(repeatedClaim.reward, firstClaim.reward);
  assert.equal(firstClaim.reward.result, 'win');
  assert.equal(firstClaim.reward.xp, 65);
  assert.equal((await call('live_claim', { matchId }, bToken)).data.reward.result, 'loss');
  process.stdout.write('CANLI_API_OK: friendship, invite, accept, ready, 8 timed questions, invalid/duplicate/late rejection, result, one-time reward.\n');
}

main().catch((error) => { process.stderr.write(`${error.stack || error}\n`); process.exitCode = 1; });
