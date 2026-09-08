<?php

declare(strict_types=1);

require __DIR__ . '/bootstrap.php';

try {
    api_cors();
    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'OPTIONS') {
        respond(['ok' => true]);
    }

    $data = input_data();
    $action = isset($data['action']) ? (string) $data['action'] : (string) ($_GET['action'] ?? 'health');
    $pdo = db();

    if ($action === 'health') {
        $pdo->query('SELECT 1')->fetchColumn();
        respond(['ok' => true, 'data' => [
            'service' => 'Macera Akademi API',
            'database' => 'mysql',
            'time' => gmdate('c'),
        ]]);
    }

    if ($action === 'register') {
        rate_limit('register', 8, 30);
        $username = need_string($data, 'username', 20);
        $email = need_string($data, 'email', 190);
        $password = need_string($data, 'password', 200);
        $grade = int_between($data['grade'] ?? 1, 1, 4, 1);

        if (strlen($username) < 3 || !preg_match('/^[A-Za-z0-9ÇĞİıÖŞÜçğöşü_ .-]+$/u', $username)) {
            throw new ApiProblem('Kahraman adı en az 3 karakter olmalı ve yalnızca izin verilen karakterleri içermeli.', 422, 'validation_error');
        }
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new ApiProblem('Geçerli bir e-posta adresi yazın.', 422, 'validation_error');
        }
        if (strlen($password) < 6) {
            throw new ApiProblem('Şifre en az 6 karakter olmalı.', 422, 'validation_error');
        }
        $key = username_key($username);
        if ($key === '') {
            throw new ApiProblem('Bu kahraman adı kullanılamıyor.', 422, 'validation_error');
        }

        $profile = isset($data['profile']) && is_array($data['profile']) ? $data['profile'] : [];
        $level = int_between($profile['level'] ?? 1, 1, 100000, 1);
        $xp = int_between($profile['xp'] ?? 0, 0, 2000000000, 0);
        $coins = int_between($profile['coins'] ?? 0, 0, 2000000000, 0);
        $coinsEarned = int_between($profile['coinsEarned'] ?? 0, 0, 2000000000, 0);

        $pdo->beginTransaction();
        try {
            $stmt = $pdo->prepare(
                'INSERT INTO users '
                . '(username, username_key, parent_email, password_hash, grade, level, xp, coins, coins_earned, '
                . 'look_json, owned_json, badges_json, duel_stats_json, settings_json, completed_json) '
                . 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            );
            $stmt->execute([
                $username,
                $key,
                $email,
                password_hash($password, PASSWORD_DEFAULT),
                $grade,
                $level,
                $xp,
                $coins,
                $coinsEarned,
                json_db(json_value($profile['look'] ?? null, [])),
                json_db(json_value($profile['owned'] ?? null, [])),
                json_db(json_value($profile['badges'] ?? null, [])),
                json_db(json_value($profile['duelStats'] ?? null, [])),
                json_db(json_value($profile['settings'] ?? null, [
                    'sound' => true, 'music' => true, 'taskNotif' => true, 'rewardNotif' => true,
                ])),
                json_db(json_value($profile['completed'] ?? null, [])),
            ]);
            $userId = (int) $pdo->lastInsertId();
            $token = issue_token($userId);
            $pdo->commit();
        } catch (PDOException $e) {
            if ($pdo->inTransaction()) {
                $pdo->rollBack();
            }
            if ((string) $e->getCode() === '23000') {
                throw new ApiProblem('Bu kahraman adı zaten alınmış. Başka bir ad deneyin.', 409, 'username_taken');
            }
            throw $e;
        } catch (Throwable $e) {
            if ($pdo->inTransaction()) {
                $pdo->rollBack();
            }
            throw $e;
        }

        clear_rate_limit('register');
        $stmt = $pdo->prepare('SELECT * FROM users WHERE id = ?');
        $stmt->execute([$userId]);
        respond(['ok' => true, 'data' => [
            'token' => $token,
            'user' => profile_from_row($stmt->fetch()),
        ]], 201);
    }

    if ($action === 'login') {
        rate_limit('login', 12, 10);
        $username = need_string($data, 'username', 60);
        $password = need_string($data, 'password', 200);
        $stmt = $pdo->prepare('SELECT * FROM users WHERE username_key = ? LIMIT 1');
        $stmt->execute([username_key($username)]);
        $user = $stmt->fetch();
        if (!$user || !password_verify($password, (string) $user['password_hash'])) {
            throw new ApiProblem('Kahraman adı veya şifre yanlış.', 401, 'invalid_credentials');
        }

        clear_rate_limit('login');
        $pdo->prepare('UPDATE users SET last_login_at = UTC_TIMESTAMP() WHERE id = ?')->execute([(int) $user['id']]);
        $token = issue_token((int) $user['id']);
        respond(['ok' => true, 'data' => [
            'token' => $token,
            'user' => profile_from_row($user),
        ]]);
    }

    $user = current_user($data);
    $userId = (int) $user['id'];

    if ($action === 'me') {
        respond(['ok' => true, 'data' => ['user' => profile_from_row($user)]]);
    }

    if ($action === 'logout') {
        $hash = hash('sha256', bearer_token($data), true);
        $stmt = $pdo->prepare('DELETE FROM api_tokens WHERE token_hash = ?');
        $stmt->bindValue(1, $hash, PDO::PARAM_LOB);
        $stmt->execute();
        respond(['ok' => true, 'data' => ['loggedOut' => true]]);
    }

    if ($action === 'save_profile') {
        $profile = isset($data['profile']) && is_array($data['profile']) ? $data['profile'] : [];
        $teacherCode = strtoupper(preg_replace('/\s+/', '', trim((string) ($profile['teacherCode'] ?? ''))) ?? '');
        if (strlen($teacherCode) > 32) {
            throw new ApiProblem('Öğretmen kodu çok uzun.', 422, 'validation_error');
        }
        $class = $teacherCode !== '' ? class_for_code($teacherCode) : null;

        $stmt = $pdo->prepare(
            'UPDATE users SET grade = ?, level = ?, xp = ?, coins = ?, coins_earned = ?, '
            . 'look_json = ?, owned_json = ?, badges_json = ?, duel_stats_json = ?, settings_json = ?, '
            . 'completed_json = ?, teacher_code = ?, teacher_name = ?, teacher_id = ?, updated_at = UTC_TIMESTAMP() '
            . 'WHERE id = ?'
        );
        $stmt->execute([
            int_between($profile['grade'] ?? $user['grade'], 1, 4, (int) $user['grade']),
            int_between($profile['level'] ?? $user['level'], 1, 100000, (int) $user['level']),
            int_between($profile['xp'] ?? $user['xp'], 0, 2000000000, (int) $user['xp']),
            int_between($profile['coins'] ?? $user['coins'], 0, 2000000000, (int) $user['coins']),
            int_between($profile['coinsEarned'] ?? $user['coins_earned'], 0, 2000000000, (int) $user['coins_earned']),
            json_db(json_value($profile['look'] ?? null, json_column($user['look_json'], []))),
            json_db(json_value($profile['owned'] ?? null, json_column($user['owned_json'], []))),
            json_db(json_value($profile['badges'] ?? null, json_column($user['badges_json'], []))),
            json_db(json_value($profile['duelStats'] ?? null, json_column($user['duel_stats_json'], []))),
            json_db(json_value($profile['settings'] ?? null, json_column($user['settings_json'], []))),
            json_db(json_value($profile['completed'] ?? null, json_column($user['completed_json'], []))),
            $class ? $teacherCode : null,
            $class ? (string) $class['teacher_name'] : '',
            $class && $class['teacher_id'] !== null ? (int) $class['teacher_id'] : null,
            $userId,
        ]);
        respond(['ok' => true, 'data' => [
            'saved' => true,
            'classFound' => $teacherCode === '' || $class !== null,
            'class' => $class ? [
                'code' => (string) $class['code'],
                'teacherName' => (string) $class['teacher_name'],
                'teacherUid' => $class['teacher_id'] !== null ? (string) $class['teacher_id'] : '',
                'name' => (string) $class['name'],
            ] : null,
        ]]);
    }

    if ($action === 'change_password') {
        rate_limit('change_password', 8, 15);
        $oldPassword = need_string($data, 'oldPassword', 200);
        $newPassword = need_string($data, 'newPassword', 200);
        if (!password_verify($oldPassword, (string) $user['password_hash'])) {
            throw new ApiProblem('Eski şifre yanlış.', 403, 'wrong_password');
        }
        if (strlen($newPassword) < 6) {
            throw new ApiProblem('Yeni şifre en az 6 karakter olmalı.', 422, 'validation_error');
        }
        $pdo->beginTransaction();
        try {
            $pdo->prepare('UPDATE users SET password_hash = ?, updated_at = UTC_TIMESTAMP() WHERE id = ?')
                ->execute([password_hash($newPassword, PASSWORD_DEFAULT), $userId]);
            $currentHash = hash('sha256', bearer_token($data), true);
            $stmt = $pdo->prepare('DELETE FROM api_tokens WHERE user_id = ? AND token_hash <> ?');
            $stmt->bindValue(1, $userId, PDO::PARAM_INT);
            $stmt->bindValue(2, $currentHash, PDO::PARAM_LOB);
            $stmt->execute();
            $pdo->commit();
        } catch (Throwable $e) {
            $pdo->rollBack();
            throw $e;
        }
        clear_rate_limit('change_password');
        respond(['ok' => true, 'data' => ['changed' => true]]);
    }

    if ($action === 'delete_account') {
        rate_limit('delete_account', 6, 30);
        $password = need_string($data, 'password', 200);
        if (!password_verify($password, (string) $user['password_hash'])) {
            throw new ApiProblem('Parola yanlış.', 403, 'wrong_password');
        }
        $pdo->prepare('DELETE FROM users WHERE id = ?')->execute([$userId]);
        clear_rate_limit('delete_account');
        respond(['ok' => true, 'data' => ['deleted' => true]]);
    }

    if ($action === 'class_lookup') {
        $code = strtoupper(preg_replace('/\s+/', '', need_string($data, 'code', 32)) ?? '');
        $class = class_for_code($code);
        respond(['ok' => true, 'data' => ['class' => $class ? [
            'code' => (string) $class['code'],
            'name' => (string) $class['name'],
            'grade' => (int) $class['grade'],
            'teacherName' => (string) $class['teacher_name'],
            'teacherUid' => $class['teacher_id'] !== null ? (string) $class['teacher_id'] : '',
        ] : null]]);
    }

    if ($action === 'class_progress') {
        $code = strtoupper(need_string($data, 'code', 32));
        if ($code !== strtoupper((string) ($user['teacher_code'] ?? '')) || !class_for_code($code)) {
            throw new ApiProblem('Geçerli bir sınıf bağlantısı bulunamadı.', 403, 'class_denied');
        }
        $doneIds = json_value($data['doneIds'] ?? null, []);
        $stmt = $pdo->prepare(
            'INSERT INTO class_progress '
            . '(class_code, user_id, username, grade, level, xp, coins, done_count, done_ids_json, duel_wins, duel_best) '
            . 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '
            . 'ON DUPLICATE KEY UPDATE username = VALUES(username), grade = VALUES(grade), level = VALUES(level), '
            . 'xp = VALUES(xp), coins = VALUES(coins), done_count = VALUES(done_count), '
            . 'done_ids_json = VALUES(done_ids_json), duel_wins = VALUES(duel_wins), '
            . 'duel_best = VALUES(duel_best), updated_at = UTC_TIMESTAMP()'
        );
        $stmt->execute([
            $code, $userId, (string) $user['username'],
            int_between($data['grade'] ?? 1, 1, 4, 1),
            int_between($data['level'] ?? 1, 1, 100000, 1),
            int_between($data['xp'] ?? 0, 0, 2000000000, 0),
            int_between($data['coins'] ?? 0, 0, 2000000000, 0),
            count($doneIds), json_db($doneIds),
            int_between($data['duelWins'] ?? 0, 0, 2000000000, 0),
            int_between($data['duelBest'] ?? 0, 0, 2000000000, 0),
        ]);
        respond(['ok' => true, 'data' => ['saved' => true]]);
    }

    if ($action === 'class_data') {
        $code = strtoupper(need_string($data, 'code', 32));
        if ($code !== strtoupper((string) ($user['teacher_code'] ?? '')) || !class_for_code($code)) {
            throw new ApiProblem('Geçerli bir sınıf bağlantısı bulunamadı.', 403, 'class_denied');
        }
        $stmt = $pdo->prepare(
            'SELECT id, title, grade, subject, game_ids_json, due_date, note, created_at '
            . 'FROM assignments WHERE class_code = ? AND active = 1 ORDER BY created_at DESC'
        );
        $stmt->execute([$code]);
        $assignments = [];
        foreach ($stmt->fetchAll() as $row) {
            $assignments[] = [
                'id' => (string) $row['id'], 'title' => (string) $row['title'],
                'grade' => $row['grade'] !== null ? (int) $row['grade'] : null,
                'subj' => (string) $row['subject'], 'gameIds' => json_column($row['game_ids_json'], []),
                'due' => $row['due_date'] ? (string) $row['due_date'] : '', 'note' => (string) $row['note'],
                'createdAtIso' => (string) $row['created_at'],
            ];
        }
        $stmt = $pdo->prepare(
            'SELECT id, title, kind, category_id, category_label, grade, seed, starts_at, ends_at '
            . 'FROM contests WHERE class_code = ? AND active = 1 '
            . 'AND (starts_at IS NULL OR starts_at <= UTC_DATE()) '
            . 'AND (ends_at IS NULL OR ends_at >= UTC_DATE()) ORDER BY ends_at ASC, created_at DESC'
        );
        $stmt->execute([$code]);
        $contests = [];
        foreach ($stmt->fetchAll() as $row) {
            $contests[] = [
                'id' => (string) $row['id'], 'title' => (string) $row['title'], 'kind' => (string) $row['kind'],
                'catId' => (string) $row['category_id'], 'catLabel' => (string) $row['category_label'],
                'grade' => (int) $row['grade'], 'seed' => (int) $row['seed'],
                'startsAt' => $row['starts_at'] ? (string) $row['starts_at'] : '',
                'endsAt' => $row['ends_at'] ? (string) $row['ends_at'] : '',
            ];
        }
        respond(['ok' => true, 'data' => ['assignments' => $assignments, 'contests' => $contests]]);
    }

    if ($action === 'contest_submit') {
        $contestId = need_string($data, 'contestId', 64);
        $stmt = $pdo->prepare('SELECT * FROM contests WHERE id = ? AND active = 1 LIMIT 1');
        $stmt->execute([$contestId]);
        $contest = $stmt->fetch();
        if (!$contest || strtoupper((string) $contest['class_code']) !== strtoupper((string) ($user['teacher_code'] ?? ''))) {
            throw new ApiProblem('Bu yarışmaya katılma yetkiniz yok.', 403, 'contest_denied');
        }
        $score = int_between($data['score'] ?? 0, 0, 2000000000, 0);
        $correct = int_between($data['correct'] ?? 0, 0, 10000, 0);
        $stmt = $pdo->prepare(
            'INSERT INTO contest_scores (contest_id, user_id, class_code, username, score, correct_count, grade) '
            . 'VALUES (?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE '
            . 'score = GREATEST(score, VALUES(score)), correct_count = IF(VALUES(score) >= score, VALUES(correct_count), correct_count), '
            . 'grade = VALUES(grade), submitted_at = UTC_TIMESTAMP()'
        );
        $stmt->execute([
            $contestId, $userId, (string) $contest['class_code'], (string) $user['username'],
            $score, $correct, int_between($data['grade'] ?? $user['grade'], 1, 4, (int) $user['grade']),
        ]);
        respond(['ok' => true, 'data' => ['saved' => true]]);
    }

    if ($action === 'contest_board') {
        $contestId = need_string($data, 'contestId', 64);
        $stmt = $pdo->prepare('SELECT class_code FROM contests WHERE id = ? AND active = 1 LIMIT 1');
        $stmt->execute([$contestId]);
        $code = $stmt->fetchColumn();
        if (!$code || strtoupper((string) $code) !== strtoupper((string) ($user['teacher_code'] ?? ''))) {
            throw new ApiProblem('Bu sıralamayı görme yetkiniz yok.', 403, 'contest_denied');
        }
        $stmt = $pdo->prepare(
            'SELECT user_id, username, score, correct_count, grade, submitted_at '
            . 'FROM contest_scores WHERE contest_id = ? ORDER BY score DESC, submitted_at ASC LIMIT 100'
        );
        $stmt->execute([$contestId]);
        $list = [];
        foreach ($stmt->fetchAll() as $row) {
            $list[] = [
                'uid' => (string) $row['user_id'], 'username' => (string) $row['username'],
                'score' => (int) $row['score'], 'correct' => (int) $row['correct_count'],
                'grade' => (int) $row['grade'], 'at' => (string) $row['submitted_at'],
            ];
        }
        respond(['ok' => true, 'data' => ['list' => $list]]);
    }

    if ($action === 'friend_lookup') {
        $name = need_string($data, 'username', 60);
        $stmt = $pdo->prepare('SELECT id FROM users WHERE username_key = ? LIMIT 1');
        $stmt->execute([username_key($name)]);
        $otherId = $stmt->fetchColumn();
        if (!$otherId) {
            respond(['ok' => true, 'data' => ['user' => null]]);
        }
        if ((int) $otherId === $userId) {
            throw new ApiProblem('Bu sizin kendi adınız.', 422, 'self_lookup');
        }
        respond(['ok' => true, 'data' => ['user' => public_user((int) $otherId)]]);
    }

    if ($action === 'friends_list') {
        $stmt = $pdo->prepare(
            'SELECT f.status, f.requester_id, '
            . 'CASE WHEN f.user_low_id = ? THEN f.user_high_id ELSE f.user_low_id END AS other_id, '
            . 'u.username, u.level, u.grade FROM friendships f '
            . 'JOIN users u ON u.id = CASE WHEN f.user_low_id = ? THEN f.user_high_id ELSE f.user_low_id END '
            . 'WHERE f.user_low_id = ? OR f.user_high_id = ? ORDER BY f.updated_at DESC'
        );
        $stmt->execute([$userId, $userId, $userId, $userId]);
        $result = ['friends' => [], 'incoming' => [], 'outgoing' => []];
        foreach ($stmt->fetchAll() as $row) {
            $item = [
                'uid' => (string) $row['other_id'], 'username' => (string) $row['username'],
                'level' => (int) $row['level'], 'grade' => (int) $row['grade'], 'status' => (string) $row['status'],
            ];
            if ($row['status'] === 'accepted') {
                $result['friends'][] = $item;
            } elseif ((int) $row['requester_id'] === $userId) {
                $result['outgoing'][] = $item;
            } else {
                $result['incoming'][] = $item;
            }
        }
        respond(['ok' => true, 'data' => $result]);
    }

    if ($action === 'friend_request') {
        $otherId = require_user_id($data['uid'] ?? null);
        if ($otherId === $userId || !public_user($otherId)) {
            throw new ApiProblem('Geçersiz arkadaş isteği.', 422, 'validation_error');
        }
        [$low, $high] = same_pair($userId, $otherId);
        try {
            $pdo->prepare(
                "INSERT INTO friendships (user_low_id, user_high_id, requester_id, status) VALUES (?, ?, ?, 'pending')"
            )->execute([$low, $high, $userId]);
        } catch (PDOException $e) {
            if ((string) $e->getCode() === '23000') {
                throw new ApiProblem('Bu kişiyle zaten bir arkadaşlık veya bekleyen istek var.', 409, 'friendship_exists');
            }
            throw $e;
        }
        respond(['ok' => true, 'data' => ['sent' => true]]);
    }

    if ($action === 'friend_accept') {
        $otherId = require_user_id($data['uid'] ?? null);
        [$low, $high] = same_pair($userId, $otherId);
        $stmt = $pdo->prepare(
            "UPDATE friendships SET status = 'accepted' WHERE user_low_id = ? AND user_high_id = ? "
            . "AND status = 'pending' AND requester_id = ?"
        );
        $stmt->execute([$low, $high, $otherId]);
        if ($stmt->rowCount() !== 1) {
            throw new ApiProblem('Bu istek artık beklemiyor.', 409, 'request_not_pending');
        }
        respond(['ok' => true, 'data' => ['accepted' => true]]);
    }

    if ($action === 'friend_remove') {
        $otherId = require_user_id($data['uid'] ?? null);
        [$low, $high] = same_pair($userId, $otherId);
        $pdo->prepare('DELETE FROM friendships WHERE user_low_id = ? AND user_high_id = ?')->execute([$low, $high]);
        respond(['ok' => true, 'data' => ['removed' => true]]);
    }

    if ($action === 'messages_list') {
        $stmt = $pdo->prepare(
            'SELECT m.id, m.from_user_id, m.preset_id, m.created_at, m.read_at, u.username AS from_name '
            . 'FROM messages m JOIN users u ON u.id = m.from_user_id '
            . 'WHERE m.to_user_id = ? ORDER BY m.created_at DESC LIMIT 50'
        );
        $stmt->execute([$userId]);
        $list = [];
        foreach ($stmt->fetchAll() as $row) {
            $list[] = [
                'id' => (string) $row['id'], 'from' => (string) $row['from_user_id'],
                'fromName' => (string) $row['from_name'], 'presetId' => (string) $row['preset_id'],
                'readAt' => $row['read_at'] ? (string) $row['read_at'] : null,
                'at' => strtotime((string) $row['created_at']) ?: 0,
            ];
        }
        respond(['ok' => true, 'data' => ['list' => $list]]);
    }

    if ($action === 'messages_read') {
        $pdo->prepare('UPDATE messages SET read_at = UTC_TIMESTAMP() WHERE to_user_id = ? AND read_at IS NULL')
            ->execute([$userId]);
        respond(['ok' => true, 'data' => ['read' => true]]);
    }

    if ($action === 'message_send') {
        $otherId = require_user_id($data['uid'] ?? null);
        $preset = need_string($data, 'presetId', 40);
        $allowed = ['selam', 'iyi_oyun', 'tebrikler', 'yarisalim', 'harikaydin', 'gorusuruz'];
        if (!in_array($preset, $allowed, true)) {
            throw new ApiProblem('Geçersiz hazır mesaj.', 422, 'validation_error');
        }
        if (!accepted_friends($userId, $otherId)) {
            throw new ApiProblem('Yalnızca kabul edilmiş arkadaşlara mesaj gönderebilirsiniz.', 403, 'not_friends');
        }
        $pdo->prepare('INSERT INTO messages (from_user_id, to_user_id, preset_id) VALUES (?, ?, ?)')
            ->execute([$userId, $otherId, $preset]);
        respond(['ok' => true, 'data' => ['sent' => true]], 201);
    }

    if ($action === 'duel_create') {
        $otherId = require_user_id($data['oppUid'] ?? null);
        if (!accepted_friends($userId, $otherId)) {
            throw new ApiProblem('Yalnızca arkadaşlarınıza meydan okuyabilirsiniz.', 403, 'not_friends');
        }
        $other = public_user($otherId);
        if (!$other) {
            throw new ApiProblem('Rakip bulunamadı.', 404, 'user_not_found');
        }
        $answers = json_value($data['answers'] ?? null, []);
        $stmt = $pdo->prepare(
            'INSERT INTO duels (from_user_id, to_user_id, from_name, to_name, grade, category_id, '
            . 'category_label, seed, from_score, from_correct, from_answers_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        );
        $stmt->execute([
            $userId, $otherId, (string) $user['username'], (string) $other['username'],
            int_between($data['grade'] ?? 1, 1, 4, 1), need_string($data, 'catId', 40),
            need_string($data, 'catLabel', 100), (int) ($data['seed'] ?? 1),
            int_between($data['score'] ?? 0, 0, 2000000000, 0),
            int_between($data['correct'] ?? 0, 0, 10000, 0), json_db($answers),
        ]);
        respond(['ok' => true, 'data' => ['id' => (string) $pdo->lastInsertId()]], 201);
    }

    if ($action === 'duel_respond') {
        $duelId = require_user_id($data['duelId'] ?? null, 'Geçersiz düello.');
        $pdo->beginTransaction();
        try {
            $stmt = $pdo->prepare('SELECT * FROM duels WHERE id = ? FOR UPDATE');
            $stmt->execute([$duelId]);
            $duel = $stmt->fetch();
            if (!$duel || (int) $duel['to_user_id'] !== $userId || $duel['status'] !== 'pending') {
                throw new ApiProblem('Bu meydan okuma artık yanıtlanamıyor.', 409, 'duel_not_pending');
            }
            $toScore = int_between($data['score'] ?? 0, 0, 2000000000, 0);
            $toCorrect = int_between($data['correct'] ?? 0, 0, 10000, 0);
            $fromScore = (int) $duel['from_score'];
            $isDraw = $toScore === $fromScore ? 1 : 0;
            $winner = $isDraw ? null : ($toScore > $fromScore ? $userId : (int) $duel['from_user_id']);
            $stmt = $pdo->prepare(
                "UPDATE duels SET status = 'done', to_score = ?, to_correct = ?, to_answers_json = ?, "
                . 'winner_user_id = ?, is_draw = ?, played_at = UTC_TIMESTAMP() WHERE id = ?'
            );
            $stmt->execute([
                $toScore, $toCorrect, json_db(json_value($data['answers'] ?? null, [])),
                $winner, $isDraw, $duelId,
            ]);
            $pdo->prepare('INSERT INTO duel_claims (duel_id, user_id) VALUES (?, ?)')->execute([$duelId, $userId]);
            $pdo->commit();
        } catch (Throwable $e) {
            if ($pdo->inTransaction()) {
                $pdo->rollBack();
            }
            throw $e;
        }
        respond(['ok' => true, 'data' => [
            'saved' => true,
            'winner' => $isDraw ? 'draw' : (string) $winner,
        ]]);
    }

    if ($action === 'duels_list') {
        $stmt = $pdo->prepare(
            'SELECT * FROM duels WHERE from_user_id = ? OR to_user_id = ? ORDER BY created_at DESC LIMIT 40'
        );
        $stmt->execute([$userId, $userId]);
        $list = [];
        foreach ($stmt->fetchAll() as $row) {
            $claimStmt = $pdo->prepare('SELECT user_id FROM duel_claims WHERE duel_id = ?');
            $claimStmt->execute([(int) $row['id']]);
            $claimed = array_map('strval', $claimStmt->fetchAll(PDO::FETCH_COLUMN));
            $winner = (int) $row['is_draw'] === 1 ? 'draw' : ($row['winner_user_id'] !== null ? (string) $row['winner_user_id'] : null);
            $list[] = [
                'id' => (string) $row['id'], 'from' => (string) $row['from_user_id'],
                'to' => (string) $row['to_user_id'], 'fromName' => (string) $row['from_name'],
                'toName' => (string) $row['to_name'], 'grade' => (int) $row['grade'],
                'catId' => (string) $row['category_id'], 'catLabel' => (string) $row['category_label'],
                'seed' => (int) $row['seed'], 'status' => (string) $row['status'], 'claimed' => $claimed,
                'fromScore' => (int) $row['from_score'], 'fromCorrect' => (int) $row['from_correct'],
                'fromAnswers' => json_column($row['from_answers_json'], []),
                'toScore' => $row['to_score'] !== null ? (int) $row['to_score'] : null,
                'toCorrect' => $row['to_correct'] !== null ? (int) $row['to_correct'] : null,
                'winner' => $winner, 'at' => strtotime((string) $row['created_at']) ?: 0,
            ];
        }
        respond(['ok' => true, 'data' => ['list' => $list]]);
    }

    if ($action === 'duel_claim') {
        $duelId = require_user_id($data['duelId'] ?? null, 'Geçersiz düello.');
        $stmt = $pdo->prepare(
            "SELECT 1 FROM duels WHERE id = ? AND status = 'done' AND (from_user_id = ? OR to_user_id = ?) LIMIT 1"
        );
        $stmt->execute([$duelId, $userId, $userId]);
        if (!$stmt->fetchColumn()) {
            throw new ApiProblem('Ödülü alınabilecek bir düello bulunamadı.', 404, 'duel_not_found');
        }
        $stmt = $pdo->prepare('INSERT IGNORE INTO duel_claims (duel_id, user_id) VALUES (?, ?)');
        $stmt->execute([$duelId, $userId]);
        respond(['ok' => true, 'data' => ['claimed' => $stmt->rowCount() === 1]]);
    }

    throw new ApiProblem('Bilinmeyen API işlemi.', 404, 'action_not_found');
} catch (ApiProblem $e) {
    respond(['ok' => false, 'error' => ['code' => $e->errorCode, 'message' => $e->getMessage()]], $e->status);
} catch (Throwable $e) {
    $debug = false;
    try {
        $debug = (bool) (api_config()['debug'] ?? false);
    } catch (Throwable $ignored) {
    }
    respond(['ok' => false, 'error' => [
        'code' => 'server_error',
        'message' => $debug ? $e->getMessage() : 'Sunucuda beklenmeyen bir hata oluştu.',
    ]], 500);
}
