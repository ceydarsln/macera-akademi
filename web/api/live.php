<?php

declare(strict_types=1);

require_once __DIR__ . '/live-questions.php';

const LIVE_QUESTION_COUNT = 8;
const LIVE_QUESTION_MS = 12000;

function live_match_id($value): int
{
    return require_user_id($value, 'Geçersiz canlı maç numarası.');
}

function live_locked_match(PDO $pdo, int $matchId, int $userId): array
{
    $stmt = $pdo->prepare('SELECT * FROM live_matches WHERE id = ? FOR UPDATE');
    $stmt->execute([$matchId]);
    $match = $stmt->fetch();
    if (!$match || ((int) $match['from_user_id'] !== $userId && (int) $match['to_user_id'] !== $userId)) {
        throw new ApiProblem('Canlı maç bulunamadı.', 404, 'live_match_not_found');
    }
    return $match;
}

function live_finish_match(PDO $pdo, array &$match): void
{
    if (!in_array($match['status'], ['countdown', 'playing'], true)) {
        return;
    }
    $fromScore = (int) $match['from_score'];
    $toScore = (int) $match['to_score'];
    $draw = $fromScore === $toScore;
    $winner = $draw ? null : ($fromScore > $toScore ? (int) $match['from_user_id'] : (int) $match['to_user_id']);
    $pdo->prepare("UPDATE live_matches SET status = 'finished', winner_user_id = ?, is_draw = ? WHERE id = ?")
        ->execute([$winner, $draw ? 1 : 0, (int) $match['id']]);
    $match['status'] = 'finished';
    $match['winner_user_id'] = $winner;
    $match['is_draw'] = $draw ? 1 : 0;
}

function live_forfeit_match(PDO $pdo, array &$match, ?int $loserId): void
{
    if (!in_array($match['status'], ['countdown', 'playing'], true)) { return; }
    if ($loserId === null) {
        $pdo->prepare("UPDATE live_matches SET status = 'cancelled', finish_reason = 'forfeit' WHERE id = ?")
            ->execute([(int) $match['id']]);
        $match['status'] = 'cancelled';
        $match['finish_reason'] = 'forfeit';
        return;
    }
    $winner = (int) $match['from_user_id'] === $loserId
        ? (int) $match['to_user_id'] : (int) $match['from_user_id'];
    $pdo->prepare("UPDATE live_matches SET status = 'finished', finish_reason = 'forfeit', "
        . 'forfeit_user_id = ?, winner_user_id = ?, is_draw = 0 WHERE id = ?')
        ->execute([$loserId, $winner, (int) $match['id']]);
    $match['status'] = 'finished';
    $match['finish_reason'] = 'forfeit';
    $match['forfeit_user_id'] = $loserId;
    $match['winner_user_id'] = $winner;
    $match['is_draw'] = 0;
}

function live_sync_match(PDO $pdo, array &$match): void
{
    if ($match['status'] === 'invited') {
        $stmt = $pdo->prepare(
            "UPDATE live_matches SET status = 'expired' WHERE id = ? AND status = 'invited' "
            . 'AND invite_expires_at <= UTC_TIMESTAMP(3)'
        );
        $stmt->execute([(int) $match['id']]);
        if ($stmt->rowCount() === 1) { $match['status'] = 'expired'; }
    }
    if ($match['status'] === 'lobby') {
        $stmt = $pdo->prepare(
            "UPDATE live_matches SET status = 'expired' WHERE id = ? AND status = 'lobby' "
            . 'AND lobby_expires_at <= UTC_TIMESTAMP(3)'
        );
        $stmt->execute([(int) $match['id']]);
        if ($stmt->rowCount() === 1) { $match['status'] = 'expired'; }
    }
    if (in_array($match['status'], ['countdown', 'playing'], true)) {
        $clock = $pdo->prepare(
            'SELECT starts_at <= UTC_TIMESTAMP(3) AS started, ends_at <= UTC_TIMESTAMP(3) AS ended, '
            . 'TIMESTAMPDIFF(MICROSECOND, from_last_seen_at, LEAST(UTC_TIMESTAMP(3), ends_at)) AS from_absent_us, '
            . 'TIMESTAMPDIFF(MICROSECOND, to_last_seen_at, LEAST(UTC_TIMESTAMP(3), ends_at)) AS to_absent_us '
            . 'FROM live_matches WHERE id = ?'
        );
        $clock->execute([(int) $match['id']]);
        $times = $clock->fetch();
        $fromAbsent = $times && $times['from_absent_us'] !== null && (int) $times['from_absent_us'] >= 20000000;
        $toAbsent = $times && $times['to_absent_us'] !== null && (int) $times['to_absent_us'] >= 20000000;
        if ($match['status'] === 'playing' && ($fromAbsent || $toAbsent)) {
            live_forfeit_match($pdo, $match, $fromAbsent && $toAbsent ? null
                : (int) $match[$fromAbsent ? 'from_user_id' : 'to_user_id']);
        } elseif ($times && (int) $times['ended'] === 1) {
            live_finish_match($pdo, $match);
        } elseif ($match['status'] === 'countdown' && $times && (int) $times['started'] === 1) {
            $pdo->prepare("UPDATE live_matches SET status = 'playing' WHERE id = ?")
                ->execute([(int) $match['id']]);
            $match['status'] = 'playing';
        }
    }
}

function live_touch_match(PDO $pdo, array &$match, int $userId): void
{
    if (!in_array($match['status'], ['lobby', 'countdown', 'playing'], true)) { return; }
    $field = (int) $match['from_user_id'] === $userId ? 'from_last_seen_at' : 'to_last_seen_at';
    $pdo->prepare('UPDATE live_matches SET ' . $field . ' = UTC_TIMESTAMP(3) WHERE id = ?')
        ->execute([(int) $match['id']]);
    $clock = $pdo->prepare('SELECT ' . $field . ' FROM live_matches WHERE id = ?');
    $clock->execute([(int) $match['id']]);
    $match[$field] = $clock->fetchColumn();
}

function live_time_iso($value): ?string
{
    return $value === null ? null : str_replace(' ', 'T', (string) $value) . 'Z';
}

function live_match_view(PDO $pdo, array $match, int $userId): array
{
    $from = (int) $match['from_user_id'] === $userId;
    $stmt = $pdo->prepare(
        'SELECT UTC_TIMESTAMP(3) AS server_now, '
        . 'TIMESTAMPDIFF(MICROSECOND, starts_at, UTC_TIMESTAMP(3)) AS elapsed_us FROM live_matches WHERE id = ?'
    );
    $stmt->execute([(int) $match['id']]);
    $clock = $stmt->fetch();
    $count = $pdo->prepare('SELECT user_id, COUNT(*) AS n FROM live_match_answers WHERE match_id = ? GROUP BY user_id');
    $count->execute([(int) $match['id']]);
    $answerCounts = [(int) $match['from_user_id'] => 0, (int) $match['to_user_id'] => 0];
    foreach ($count->fetchAll() as $row) { $answerCounts[(int) $row['user_id']] = (int) $row['n']; }
    $claim = $pdo->prepare('SELECT 1 FROM live_match_claims WHERE match_id = ? AND user_id = ?');
    $claim->execute([(int) $match['id'], $userId]);
    $view = [
        'id' => (string) $match['id'], 'status' => (string) $match['status'],
        'grade' => (int) $match['grade'], 'catId' => (string) $match['category_id'],
        'catLabel' => (string) $match['category_label'],
        'from' => (string) $match['from_user_id'], 'to' => (string) $match['to_user_id'],
        'fromName' => (string) $match['from_name'], 'toName' => (string) $match['to_name'],
        'myReady' => (bool) $match[$from ? 'from_ready' : 'to_ready'],
        'opponentReady' => (bool) $match[$from ? 'to_ready' : 'from_ready'],
        'myScore' => (int) $match[$from ? 'from_score' : 'to_score'],
        'opponentScore' => (int) $match[$from ? 'to_score' : 'from_score'],
        'myCorrect' => (int) $match[$from ? 'from_correct' : 'to_correct'],
        'opponentCorrect' => (int) $match[$from ? 'to_correct' : 'from_correct'],
        'myAnswered' => $answerCounts[$userId],
        'opponentAnswered' => $answerCounts[(int) $match[$from ? 'to_user_id' : 'from_user_id']],
        'rewardClaimed' => (bool) $claim->fetchColumn(),
        'serverNow' => live_time_iso($clock['server_now']),
        'inviteExpiresAt' => live_time_iso($match['invite_expires_at']),
        'lobbyExpiresAt' => live_time_iso($match['lobby_expires_at']),
        'opponentLastSeenAt' => live_time_iso($match[$from ? 'to_last_seen_at' : 'from_last_seen_at']),
        'startsAt' => live_time_iso($match['starts_at']),
        'endsAt' => live_time_iso($match['ends_at']),
        'questionCount' => LIVE_QUESTION_COUNT, 'secondsPerQuestion' => intdiv(LIVE_QUESTION_MS, 1000),
        'winner' => $match['status'] === 'finished'
            ? ((int) $match['is_draw'] === 1 ? 'draw' : (string) $match['winner_user_id']) : null,
        'finishReason' => $match['status'] === 'finished' ? (string) $match['finish_reason'] : null,
        'forfeitUserId' => $match['forfeit_user_id'] !== null ? (string) $match['forfeit_user_id'] : null,
    ];
    if ($match['status'] === 'playing' && $clock['elapsed_us'] !== null) {
        $index = intdiv(max(0, (int) $clock['elapsed_us']), LIVE_QUESTION_MS * 1000);
        if ($index >= 0 && $index < LIVE_QUESTION_COUNT) {
            $questions = json_column($match['questions_json'], []);
            $question = $questions[$index];
            $view['questionIndex'] = $index;
            $view['question'] = ['q' => $question['q'], 'opts' => $question['opts'],
                'category' => $question['category']];
            $ownAnswer = $pdo->prepare('SELECT option_index, is_correct, points FROM live_match_answers '
                . 'WHERE match_id = ? AND user_id = ? AND question_index = ?');
            $ownAnswer->execute([(int) $match['id'], $userId, $index]);
            $submitted = $ownAnswer->fetch();
            $view['myAnswer'] = $submitted ? ['optionIndex' => (int) $submitted['option_index'],
                'correct' => (bool) $submitted['is_correct'], 'points' => (int) $submitted['points']] : null;
        }
    }
    if ($match['status'] === 'finished') {
        $recap = $pdo->prepare('SELECT question_index, is_correct FROM live_match_answers '
            . 'WHERE match_id = ? AND user_id = ? ORDER BY question_index');
        $recap->execute([(int) $match['id'], $userId]);
        $view['myAnswers'] = array_map(static function ($row) {
            return ['questionIndex' => (int) $row['question_index'], 'correct' => (bool) $row['is_correct']];
        }, $recap->fetchAll());
    }
    return $view;
}

function live_handle(string $action, array $data, array $user, PDO $pdo): void
{
    $userId = (int) $user['id'];
    if ($action === 'live_invite') {
        rate_limit('live_invite:' . $userId, 12, 1);
        $otherId = require_user_id($data['oppUid'] ?? null);
        if ($otherId === $userId || !accepted_friends($userId, $otherId)) {
            throw new ApiProblem('Canlı maça yalnızca arkadaşını davet edebilirsin.', 403, 'not_friends');
        }
        $other = public_user($otherId);
        $grade = (int) $user['grade'];
        if (!$other || (int) $other['grade'] !== $grade) {
            throw new ApiProblem('Canlı yarışta iki oyuncunun sınıfı aynı olmalı.', 422, 'grade_mismatch');
        }
        $category = competition_category(need_string($data, 'catId', 40), $grade);
        $questions = live_build_questions($category['id'], $grade);
        $pdo->beginTransaction();
        try {
            $ids = same_pair($userId, $otherId);
            $lock = $pdo->prepare('SELECT id, grade FROM users WHERE id IN (?, ?) ORDER BY id FOR UPDATE');
            $lock->execute($ids);
            $grades = [];
            foreach ($lock->fetchAll() as $lockedUser) {
                $grades[(int) $lockedUser['id']] = (int) $lockedUser['grade'];
            }
            if (($grades[$userId] ?? 0) !== $grade || ($grades[$otherId] ?? 0) !== $grade) {
                throw new ApiProblem('Canlı yarışta iki oyuncunun sınıfı aynı olmalı.', 422, 'grade_mismatch');
            }
            $friend = $pdo->prepare('SELECT status FROM friendships WHERE user_low_id = ? '
                . 'AND user_high_id = ? FOR UPDATE');
            $friend->execute($ids);
            if ($friend->fetchColumn() !== 'accepted') {
                throw new ApiProblem('Arkadaşlık artık geçerli değil.', 403, 'not_friends');
            }
            $active = $pdo->prepare(
                "SELECT * FROM live_matches WHERE (from_user_id IN (?, ?) OR to_user_id IN (?, ?)) "
                . "AND status IN ('invited','lobby','countdown','playing') ORDER BY id FOR UPDATE"
            );
            $active->execute([$ids[0], $ids[1], $ids[0], $ids[1]]);
            foreach ($active->fetchAll() as $existing) {
                live_sync_match($pdo, $existing);
                if (in_array($existing['status'], ['invited', 'lobby', 'countdown', 'playing'], true)) {
                    throw new ApiProblem('Oyunculardan birinin aktif canlı maçı var.', 409, 'live_match_active');
                }
            }
            $stmt = $pdo->prepare(
                'INSERT INTO live_matches (from_user_id, to_user_id, from_name, to_name, grade, '
                . 'category_id, category_label, questions_json, invite_expires_at) '
                . 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, DATE_ADD(UTC_TIMESTAMP(3), INTERVAL 60 SECOND))'
            );
            $stmt->execute([$userId, $otherId, (string) $user['username'], (string) $other['username'],
                $grade, $category['id'], $category['label'], json_db($questions)]);
            $matchId = (int) $pdo->lastInsertId();
            $match = live_locked_match($pdo, $matchId, $userId);
            $view = live_match_view($pdo, $match, $userId);
            $pdo->commit();
        } catch (Throwable $e) {
            if ($pdo->inTransaction()) { $pdo->rollBack(); }
            throw $e;
        }
        respond(['ok' => true, 'data' => ['match' => $view]], 201);
    }

    if ($action === 'live_list') {
        $pdo->beginTransaction();
        try {
            $active = $pdo->prepare(
                "SELECT * FROM live_matches WHERE (from_user_id = ? OR to_user_id = ?) "
                . "AND status IN ('invited','lobby','countdown','playing') ORDER BY id FOR UPDATE"
            );
            $active->execute([$userId, $userId]);
            foreach ($active->fetchAll() as $pending) { live_sync_match($pdo, $pending); }
            $pdo->commit();
        } catch (Throwable $e) {
            if ($pdo->inTransaction()) { $pdo->rollBack(); }
            throw $e;
        }
        $stmt = $pdo->prepare(
            'SELECT m.id, m.status, m.category_id, m.category_label, m.from_user_id, m.to_user_id, '
            . 'm.from_name, m.to_name, m.from_score, m.to_score, m.winner_user_id, m.is_draw, '
            . 'm.finish_reason, m.forfeit_user_id, m.invite_expires_at, m.lobby_expires_at, '
            . 'm.starts_at, m.ends_at, m.created_at, c.user_id AS claimed_user_id '
            . 'FROM live_matches m LEFT JOIN live_match_claims c ON c.match_id = m.id AND c.user_id = ? '
            . 'WHERE m.from_user_id = ? OR m.to_user_id = ? ORDER BY m.created_at DESC LIMIT 40'
        );
        $stmt->execute([$userId, $userId, $userId]);
        $matches = [];
        foreach ($stmt->fetchAll() as $row) {
            $matches[] = [
                'id' => (string) $row['id'], 'status' => (string) $row['status'],
                'catId' => (string) $row['category_id'], 'catLabel' => (string) $row['category_label'],
                'from' => (string) $row['from_user_id'], 'to' => (string) $row['to_user_id'],
                'fromName' => (string) $row['from_name'], 'toName' => (string) $row['to_name'],
                'fromScore' => (int) $row['from_score'], 'toScore' => (int) $row['to_score'],
                'winner' => $row['status'] === 'finished'
                    ? ((int) $row['is_draw'] === 1 ? 'draw' : (string) $row['winner_user_id']) : null,
                'finishReason' => $row['status'] === 'finished' ? (string) $row['finish_reason'] : null,
                'forfeitUserId' => $row['forfeit_user_id'] !== null ? (string) $row['forfeit_user_id'] : null,
                'rewardClaimed' => $row['claimed_user_id'] !== null,
                'inviteExpiresAt' => live_time_iso($row['invite_expires_at']),
                'lobbyExpiresAt' => live_time_iso($row['lobby_expires_at']),
                'startsAt' => live_time_iso($row['starts_at']), 'endsAt' => live_time_iso($row['ends_at']),
                'createdAt' => live_time_iso($row['created_at']),
            ];
        }
        respond(['ok' => true, 'data' => ['matches' => $matches]]);
    }

    if ($action === 'live_claim') {
        $matchId = live_match_id($data['matchId'] ?? null);
        $pdo->beginTransaction();
        try {
            // Lock user before match: live_invite uses the same lock order.
            $profileStmt = $pdo->prepare('SELECT * FROM users WHERE id = ? FOR UPDATE');
            $profileStmt->execute([$userId]);
            $profile = $profileStmt->fetch();
            $match = live_locked_match($pdo, $matchId, $userId);
            live_sync_match($pdo, $match);
            if ($match['status'] !== 'finished') {
                throw new ApiProblem('Ödül için canlı maçın bitmesi gerekir.', 409, 'live_match_not_finished');
            }
            $existing = $pdo->prepare('SELECT reward_json FROM live_match_claims WHERE match_id = ? AND user_id = ?');
            $existing->execute([$matchId, $userId]);
            $savedReward = $existing->fetchColumn();
            $claimed = $savedReward === false;
            $stats = json_column($profile['duel_stats_json'], []);
            if ($claimed) {
                $draw = (int) $match['is_draw'] === 1;
                $win = !$draw && (int) $match['winner_user_id'] === $userId;
                $forfeited = (int) ($match['forfeit_user_id'] ?? 0) === $userId;
                $result = $draw ? 'draw' : ($win ? 'win' : 'loss');
                $base = $forfeited ? [0, 0, 'Maçtan ayrılma']
                    : ($result === 'win' ? [40, 20, 'Zafer']
                    : ($result === 'draw' ? [20, 10, 'Berabere'] : [10, 5, 'Katılım']));
                $xpGain = $base[0];
                $coinGain = $base[1];
                $lines = [[$base[2], $base[0], $base[1]]];
                $from = (int) $match['from_user_id'] === $userId;
                // A forfeit result cannot grant the perfect-answer bonus.
                $perfect = !$forfeited && $match['finish_reason'] === 'score'
                    && (int) $match[$from ? 'from_correct' : 'to_correct'] === LIVE_QUESTION_COUNT;
                if ($perfect) {
                    $xpGain += 25; $coinGain += 15;
                    $lines[] = ['Kusursuz 8/8', 25, 15];
                }
                $previousWins = (int) ($stats['wins'] ?? 0);
                if ($result === 'win') {
                    $stats['wins'] = $previousWins + 1;
                    $stats['streak'] = (int) ($stats['streak'] ?? 0) + 1;
                    $stats['best'] = max((int) ($stats['best'] ?? 0), (int) $stats['streak']);
                    if ($stats['streak'] % 3 === 0) {
                        $xpGain += 30; $coinGain += 20;
                        $lines[] = ['Üç maçlık zafer serisi', 30, 20];
                    }
                } elseif ($result === 'draw') {
                    $stats['draws'] = (int) ($stats['draws'] ?? 0) + 1;
                } else {
                    $stats['losses'] = (int) ($stats['losses'] ?? 0) + 1;
                    $stats['streak'] = 0;
                }
                $level = (int) $profile['level'];
                $totalXp = (int) $profile['xp'] + $xpGain;
                $levelUps = intdiv($totalXp, 100);
                $newLevel = min(100000, $level + $levelUps);
                $newXp = $totalXp % 100;
                $levelBonus = $levelUps * 25;
                $newCoins = min(2000000000, (int) $profile['coins'] + $coinGain + $levelBonus);
                $newEarned = min(2000000000, (int) $profile['coins_earned'] + $coinGain + $levelBonus);
                $reward = ['result' => $result, 'xp' => $xpGain, 'coin' => $coinGain,
                    'levelBonus' => $levelBonus, 'levelUps' => $levelUps, 'previousWins' => $previousWins,
                    'lines' => $lines];
                $pdo->prepare('INSERT INTO live_match_claims (match_id, user_id, reward_json) VALUES (?, ?, ?)')
                    ->execute([$matchId, $userId, json_db($reward)]);
                $pdo->prepare('UPDATE users SET level = ?, xp = ?, coins = ?, coins_earned = ?, '
                    . 'duel_stats_json = ?, updated_at = UTC_TIMESTAMP() WHERE id = ?')
                    ->execute([$newLevel, $newXp, $newCoins, $newEarned, json_db($stats), $userId]);
                $profile['level'] = $newLevel;
                $profile['xp'] = $newXp;
                $profile['coins'] = $newCoins;
                $profile['coins_earned'] = $newEarned;
                $profile['duel_stats_json'] = json_db($stats);
            } else {
                $reward = json_column($savedReward, []);
            }
            $view = live_match_view($pdo, $match, $userId);
            $pdo->commit();
        } catch (Throwable $e) {
            if ($pdo->inTransaction()) { $pdo->rollBack(); }
            throw $e;
        }
        respond(['ok' => true, 'data' => [
            'claimed' => $claimed, 'reward' => $reward, 'match' => $view,
            'profile' => ['level' => (int) $profile['level'], 'xp' => (int) $profile['xp'],
                'coins' => (int) $profile['coins'], 'coinsEarned' => (int) $profile['coins_earned'],
                'duelStats' => json_column($profile['duel_stats_json'], [])],
        ]]);
    }

    if (!in_array($action, ['live_state', 'live_accept', 'live_decline', 'live_ready', 'live_cancel',
        'live_leave', 'live_answer'], true)) {
        throw new ApiProblem('Bilinmeyen canlı maç işlemi.', 404, 'action_not_found');
    }
    $matchId = live_match_id($data['matchId'] ?? null);
    $pdo->beginTransaction();
    try {
        $match = live_locked_match($pdo, $matchId, $userId);
        live_sync_match($pdo, $match);
        $from = (int) $match['from_user_id'] === $userId;
        $answerResult = null;
        if ($action === 'live_accept') {
            if ($from || $match['status'] !== 'invited') {
                throw new ApiProblem('Bu davet artık kabul edilemiyor.', 409, 'live_invite_unavailable');
            }
            $pdo->prepare("UPDATE live_matches SET status = 'lobby', "
                . 'lobby_expires_at = DATE_ADD(UTC_TIMESTAMP(3), INTERVAL 120 SECOND) WHERE id = ?')
                ->execute([$matchId]);
            $expiry = $pdo->prepare('SELECT lobby_expires_at FROM live_matches WHERE id = ?');
            $expiry->execute([$matchId]);
            $match['status'] = 'lobby';
            $match['lobby_expires_at'] = $expiry->fetchColumn();
        } elseif ($action === 'live_decline') {
            if ($from || $match['status'] !== 'invited') {
                throw new ApiProblem('Bu davet artık reddedilemiyor.', 409, 'live_invite_unavailable');
            }
            $pdo->prepare("UPDATE live_matches SET status = 'declined' WHERE id = ?")->execute([$matchId]);
            $match['status'] = 'declined';
        } elseif ($action === 'live_cancel') {
            if (!in_array($match['status'], ['invited', 'lobby'], true) || ($match['status'] === 'invited' && !$from)) {
                throw new ApiProblem('Bu maç artık iptal edilemiyor.', 409, 'live_cancel_unavailable');
            }
            $pdo->prepare("UPDATE live_matches SET status = 'cancelled' WHERE id = ?")->execute([$matchId]);
            $match['status'] = 'cancelled';
        } elseif ($action === 'live_leave') {
            if ($match['status'] === 'invited' && $from) {
                $pdo->prepare("UPDATE live_matches SET status = 'cancelled' WHERE id = ?")->execute([$matchId]);
                $match['status'] = 'cancelled';
            } elseif ($match['status'] === 'invited' && !$from) {
                $pdo->prepare("UPDATE live_matches SET status = 'declined' WHERE id = ?")->execute([$matchId]);
                $match['status'] = 'declined';
            } elseif ($match['status'] === 'lobby') {
                $pdo->prepare("UPDATE live_matches SET status = 'cancelled' WHERE id = ?")->execute([$matchId]);
                $match['status'] = 'cancelled';
            } elseif ($match['status'] === 'countdown') {
                // No question has opened yet; leaving now must not award a free win.
                $pdo->prepare("UPDATE live_matches SET status = 'cancelled' WHERE id = ?")->execute([$matchId]);
                $match['status'] = 'cancelled';
            } elseif ($match['status'] === 'playing') {
                live_forfeit_match($pdo, $match, $userId);
            }
        } elseif ($action === 'live_ready') {
            if (!in_array($match['status'], ['lobby', 'countdown'], true)) {
                throw new ApiProblem('Hazır olmak için rakibinin daveti kabul etmesi gerekir.', 409, 'live_not_in_lobby');
            }
            if ($match['status'] === 'lobby') {
                $field = $from ? 'from_ready' : 'to_ready';
                $pdo->prepare('UPDATE live_matches SET ' . $field . ' = 1 WHERE id = ?')->execute([$matchId]);
                $match[$field] = 1;
                if ((int) $match['from_ready'] === 1 && (int) $match['to_ready'] === 1) {
                    $pdo->prepare(
                        "UPDATE live_matches SET status = 'countdown', "
                        . 'starts_at = DATE_ADD(UTC_TIMESTAMP(3), INTERVAL 3 SECOND), '
                        . 'ends_at = DATE_ADD(UTC_TIMESTAMP(3), INTERVAL 99 SECOND), '
                        . 'from_last_seen_at = UTC_TIMESTAMP(3), to_last_seen_at = UTC_TIMESTAMP(3) WHERE id = ?'
                    )->execute([$matchId]);
                    $stmt = $pdo->prepare('SELECT starts_at, ends_at, from_last_seen_at, to_last_seen_at '
                        . 'FROM live_matches WHERE id = ?');
                    $stmt->execute([$matchId]);
                    $times = $stmt->fetch();
                    $match['status'] = 'countdown';
                    $match['starts_at'] = $times['starts_at'];
                    $match['ends_at'] = $times['ends_at'];
                    $match['from_last_seen_at'] = $times['from_last_seen_at'];
                    $match['to_last_seen_at'] = $times['to_last_seen_at'];
                }
            }
        } elseif ($action === 'live_answer') {
            $index = $data['questionIndex'] ?? null;
            $option = $data['optionIndex'] ?? null;
            if (!is_int($index) || $index < 0 || $index >= LIVE_QUESTION_COUNT
                || !is_int($option) || $option < 0 || $option > 3) {
                throw new ApiProblem('Geçersiz soru veya seçenek.', 422, 'invalid_live_answer');
            }
            if ($match['status'] !== 'playing') {
                throw new ApiProblem('Canlı soru şu anda cevaplanamıyor.', 409, 'live_not_playing');
            }
            $clock = $pdo->prepare('SELECT TIMESTAMPDIFF(MICROSECOND, starts_at, UTC_TIMESTAMP(3)) AS elapsed_us '
                . 'FROM live_matches WHERE id = ?');
            $clock->execute([$matchId]);
            $elapsedMs = intdiv((int) $clock->fetchColumn(), 1000);
            if ($elapsedMs < 0 || intdiv($elapsedMs, LIVE_QUESTION_MS) !== $index) {
                throw new ApiProblem('Bu sorunun cevap süresi doldu veya henüz başlamadı.', 409, 'live_question_closed');
            }
            $previous = $pdo->prepare('SELECT question_index, is_correct FROM live_match_answers '
                . 'WHERE match_id = ? AND user_id = ? AND question_index < ? ORDER BY question_index DESC');
            $previous->execute([$matchId, $userId, $index]);
            $streak = 0;
            $expected = $index - 1;
            foreach ($previous->fetchAll() as $item) {
                if ((int) $item['question_index'] !== $expected || (int) $item['is_correct'] !== 1) { break; }
                $streak++;
                $expected--;
            }
            $questions = json_column($match['questions_json'], []);
            $question = $questions[$index];
            $correct = $option === (int) $question['answer'];
            $responseMs = $elapsedMs - $index * LIVE_QUESTION_MS;
            $points = $correct ? 10 + max(0, (int) round(10 * (1 - $responseMs / LIVE_QUESTION_MS)))
                + min($streak, 5) * 2 : 0;
            $exists = $pdo->prepare('SELECT 1 FROM live_match_answers WHERE match_id = ? AND user_id = ? '
                . 'AND question_index = ?');
            $exists->execute([$matchId, $userId, $index]);
            if ($exists->fetchColumn()) {
                throw new ApiProblem('Bu soruya zaten cevap verdin.', 409, 'live_answer_duplicate');
            }
            $pdo->prepare('INSERT INTO live_match_answers '
                . '(match_id, user_id, question_index, option_index, is_correct, response_ms, points) '
                . 'VALUES (?, ?, ?, ?, ?, ?, ?)')
                ->execute([$matchId, $userId, $index, $option, $correct ? 1 : 0, $responseMs, $points]);
            $prefix = $from ? 'from' : 'to';
            $pdo->prepare('UPDATE live_matches SET ' . $prefix . '_score = ' . $prefix . '_score + ?, '
                . $prefix . '_correct = ' . $prefix . '_correct + ? WHERE id = ?')
                ->execute([$points, $correct ? 1 : 0, $matchId]);
            $match[$prefix . '_score'] = (int) $match[$prefix . '_score'] + $points;
            $match[$prefix . '_correct'] = (int) $match[$prefix . '_correct'] + ($correct ? 1 : 0);
            $answerResult = ['questionIndex' => $index, 'correct' => $correct,
                'points' => $points, 'responseMs' => $responseMs];
            $count = $pdo->prepare('SELECT user_id, COUNT(*) AS n FROM live_match_answers '
                . 'WHERE match_id = ? GROUP BY user_id');
            $count->execute([$matchId]);
            $counts = [];
            foreach ($count->fetchAll() as $item) { $counts[(int) $item['user_id']] = (int) $item['n']; }
            if (($counts[(int) $match['from_user_id']] ?? 0) === LIVE_QUESTION_COUNT
                && ($counts[(int) $match['to_user_id']] ?? 0) === LIVE_QUESTION_COUNT) {
                live_finish_match($pdo, $match);
            }
        }
        live_touch_match($pdo, $match, $userId);
        $view = live_match_view($pdo, $match, $userId);
        $pdo->commit();
    } catch (Throwable $e) {
        if ($pdo->inTransaction()) { $pdo->rollBack(); }
        throw $e;
    }
    respond(['ok' => true, 'data' => ['match' => $view, 'answer' => $answerResult]]);
}
