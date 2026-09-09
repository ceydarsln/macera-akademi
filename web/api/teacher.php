<?php

declare(strict_types=1);

require __DIR__ . '/bootstrap.php';

function optional_date(array $data, string $key): ?string
{
    $value = trim((string) ($data[$key] ?? ''));
    if ($value === '') {
        return null;
    }
    $date = DateTimeImmutable::createFromFormat('!Y-m-d', $value);
    $errors = DateTimeImmutable::getLastErrors();
    if (!$date || (is_array($errors) && ($errors['warning_count'] > 0 || $errors['error_count'] > 0))
        || $date->format('Y-m-d') !== $value) {
        throw new ApiProblem($key . ' alanı YYYY-AA-GG biçiminde olmalı.', 422, 'validation_error');
    }
    return $value;
}

function bool_value($value): bool
{
    if (is_bool($value)) {
        return $value;
    }
    return filter_var($value, FILTER_VALIDATE_BOOLEAN);
}

function string_list($value, int $maxItems = 700): array
{
    if (!is_array($value)) {
        throw new ApiProblem('gameIds bir liste olmalı.', 422, 'validation_error');
    }
    $result = [];
    foreach ($value as $item) {
        $id = trim((string) $item);
        if ($id === '' || strlen($id) > 64 || !preg_match('/^[A-Za-z0-9_-]+$/', $id)) {
            throw new ApiProblem('Geçersiz oyun kimliği.', 422, 'validation_error');
        }
        $result[$id] = true;
        if (count($result) > $maxItems) {
            throw new ApiProblem('Bir ödeve en fazla ' . $maxItems . ' oyun eklenebilir.', 422, 'validation_error');
        }
    }
    return array_keys($result);
}

function assignment_payload(array $row): array
{
    return [
        'id' => (string) $row['id'],
        'title' => (string) $row['title'],
        'grade' => $row['grade'] !== null ? (int) $row['grade'] : null,
        'subj' => (string) $row['subject'],
        'gameIds' => json_column($row['game_ids_json'], []),
        'due' => $row['due_date'] ? (string) $row['due_date'] : '',
        'note' => (string) $row['note'],
        'active' => (bool) $row['active'],
        'createdAtIso' => (string) $row['created_at'],
    ];
}

function contest_payload(array $row): array
{
    return [
        'id' => (string) $row['id'],
        'title' => (string) $row['title'],
        'kind' => (string) $row['kind'],
        'catId' => (string) $row['category_id'],
        'catLabel' => (string) $row['category_label'],
        'grade' => (int) $row['grade'],
        'seed' => (int) $row['seed'],
        'startsAt' => $row['starts_at'] ? (string) $row['starts_at'] : '',
        'endsAt' => $row['ends_at'] ? (string) $row['ends_at'] : '',
        'active' => (bool) $row['active'],
        'createdAtIso' => (string) $row['created_at'],
    ];
}

try {
    api_cors();
    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'OPTIONS') {
        respond(['ok' => true]);
    }

    $data = input_data();
    $action = isset($data['action']) ? (string) $data['action'] : (string) ($_GET['action'] ?? 'health');
    $pdo = db();

    if ($action === 'health') {
        $pdo->query('SELECT 1 FROM teacher_tokens LIMIT 1');
        respond(['ok' => true, 'data' => [
            'service' => 'Macera Akademi Öğretmen API',
            'database' => 'mysql',
            'time' => gmdate('c'),
        ]]);
    }

    if ($action === 'register') {
        rate_limit('teacher_register', 6, 30);
        $username = username_key(need_string($data, 'username', 80));
        $password = need_string($data, 'password', 200);
        $fullName = need_string($data, 'fullName', 120);
        $email = trim((string) ($data['email'] ?? ''));
        $className = trim((string) ($data['className'] ?? '')) ?: 'Sınıfım';
        $grade = int_between($data['grade'] ?? 1, 1, 4, 1);

        if (strlen($username) < 3) {
            throw new ApiProblem('Kullanıcı adı en az 3 karakter olmalı.', 422, 'validation_error');
        }
        if (strlen($password) < 8) {
            throw new ApiProblem('Şifre en az 8 karakter olmalı.', 422, 'validation_error');
        }
        if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new ApiProblem('Geçerli bir e-posta adresi yazın.', 422, 'validation_error');
        }
        if (strlen($email) > 190 || strlen($className) > 120) {
            throw new ApiProblem('Girilen bilgiler çok uzun.', 422, 'validation_error');
        }

        $pdo->beginTransaction();
        try {
            $stmt = $pdo->prepare(
                'INSERT INTO teachers (username, password_hash, display_name, email) VALUES (?, ?, ?, ?)'
            );
            $stmt->execute([$username, password_hash($password, PASSWORD_DEFAULT), $fullName, $email]);
            $teacherId = (int) $pdo->lastInsertId();
            $code = new_class_code();
            $pdo->prepare(
                'INSERT INTO classes (code, teacher_id, teacher_name, name, grade, active) VALUES (?, ?, ?, ?, ?, 1)'
            )->execute([$code, $teacherId, $fullName, $className, $grade]);
            $token = issue_teacher_token($teacherId);
            $pdo->commit();
        } catch (PDOException $e) {
            if ($pdo->inTransaction()) {
                $pdo->rollBack();
            }
            if ((string) $e->getCode() === '23000') {
                throw new ApiProblem('Bu öğretmen kullanıcı adı zaten kullanılıyor.', 409, 'username_taken');
            }
            throw $e;
        } catch (Throwable $e) {
            if ($pdo->inTransaction()) {
                $pdo->rollBack();
            }
            throw $e;
        }

        clear_rate_limit('teacher_register');
        $stmt = $pdo->prepare('SELECT * FROM teachers WHERE id = ?');
        $stmt->execute([$teacherId]);
        respond(['ok' => true, 'data' => [
            'token' => $token,
            'teacher' => teacher_profile_from_row($stmt->fetch()),
        ]], 201);
    }

    if ($action === 'login') {
        rate_limit('teacher_login', 12, 10);
        $username = username_key(need_string($data, 'username', 80));
        $password = need_string($data, 'password', 200);
        $stmt = $pdo->prepare('SELECT * FROM teachers WHERE username = ? AND active = 1 LIMIT 1');
        $stmt->execute([$username]);
        $teacher = $stmt->fetch();
        if (!$teacher || !password_verify($password, (string) $teacher['password_hash'])) {
            throw new ApiProblem('Kullanıcı adı veya şifre yanlış.', 401, 'invalid_credentials');
        }
        clear_rate_limit('teacher_login');
        $token = issue_teacher_token((int) $teacher['id']);
        respond(['ok' => true, 'data' => [
            'token' => $token,
            'teacher' => teacher_profile_from_row($teacher),
        ]]);
    }

    $teacher = current_teacher($data);
    $teacherId = (int) $teacher['id'];

    if ($action === 'me') {
        respond(['ok' => true, 'data' => ['teacher' => teacher_profile_from_row($teacher)]]);
    }

    if ($action === 'logout') {
        $hash = hash('sha256', bearer_token($data), true);
        $stmt = $pdo->prepare('DELETE FROM teacher_tokens WHERE token_hash = ?');
        $stmt->bindValue(1, $hash, PDO::PARAM_LOB);
        $stmt->execute();
        respond(['ok' => true, 'data' => ['loggedOut' => true]]);
    }

    if ($action === 'overview') {
        $class = teacher_class_or_fail($teacherId);
        $counts = [];
        foreach ([
            'students' => 'SELECT COUNT(*) FROM class_progress WHERE class_code = ?',
            'assignments' => 'SELECT COUNT(*) FROM assignments WHERE class_code = ? AND active = 1',
            'contests' => 'SELECT COUNT(*) FROM contests WHERE class_code = ? AND active = 1',
        ] as $key => $sql) {
            $stmt = $pdo->prepare($sql);
            $stmt->execute([(string) $class['code']]);
            $counts[$key] = (int) $stmt->fetchColumn();
        }
        respond(['ok' => true, 'data' => [
            'teacher' => teacher_profile_from_row($teacher, $class),
            'counts' => $counts,
        ]]);
    }

    if ($action === 'profile_save') {
        $fullName = need_string($data, 'fullName', 120);
        $email = trim((string) ($data['email'] ?? ''));
        $className = need_string($data, 'className', 120);
        $grade = int_between($data['grade'] ?? 1, 1, 4, 1);
        if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new ApiProblem('Geçerli bir e-posta adresi yazın.', 422, 'validation_error');
        }
        if (strlen($email) > 190) {
            throw new ApiProblem('E-posta adresi çok uzun.', 422, 'validation_error');
        }
        $class = teacher_class_or_fail($teacherId);
        $pdo->beginTransaction();
        try {
            $pdo->prepare('UPDATE teachers SET display_name = ?, email = ?, updated_at = UTC_TIMESTAMP() WHERE id = ?')
                ->execute([$fullName, $email, $teacherId]);
            $pdo->prepare(
                'UPDATE classes SET teacher_name = ?, name = ?, grade = ?, updated_at = UTC_TIMESTAMP() '
                . 'WHERE code = ? AND teacher_id = ?'
            )->execute([$fullName, $className, $grade, (string) $class['code'], $teacherId]);
            $pdo->commit();
        } catch (Throwable $e) {
            if ($pdo->inTransaction()) {
                $pdo->rollBack();
            }
            throw $e;
        }
        $stmt = $pdo->prepare('SELECT * FROM teachers WHERE id = ?');
        $stmt->execute([$teacherId]);
        respond(['ok' => true, 'data' => ['teacher' => teacher_profile_from_row($stmt->fetch())]]);
    }

    if ($action === 'change_password') {
        rate_limit('teacher_change_password', 8, 15);
        $oldPassword = need_string($data, 'oldPassword', 200);
        $newPassword = need_string($data, 'newPassword', 200);
        if (!password_verify($oldPassword, (string) $teacher['password_hash'])) {
            throw new ApiProblem('Eski şifre yanlış.', 403, 'wrong_password');
        }
        if (strlen($newPassword) < 8) {
            throw new ApiProblem('Yeni şifre en az 8 karakter olmalı.', 422, 'validation_error');
        }
        $pdo->beginTransaction();
        try {
            $pdo->prepare('UPDATE teachers SET password_hash = ?, updated_at = UTC_TIMESTAMP() WHERE id = ?')
                ->execute([password_hash($newPassword, PASSWORD_DEFAULT), $teacherId]);
            $currentHash = hash('sha256', bearer_token($data), true);
            $stmt = $pdo->prepare('DELETE FROM teacher_tokens WHERE teacher_id = ? AND token_hash <> ?');
            $stmt->bindValue(1, $teacherId, PDO::PARAM_INT);
            $stmt->bindValue(2, $currentHash, PDO::PARAM_LOB);
            $stmt->execute();
            $pdo->commit();
        } catch (Throwable $e) {
            if ($pdo->inTransaction()) {
                $pdo->rollBack();
            }
            throw $e;
        }
        clear_rate_limit('teacher_change_password');
        respond(['ok' => true, 'data' => ['changed' => true]]);
    }

    if ($action === 'class_regenerate') {
        $class = teacher_class_or_fail($teacherId);
        $code = new_class_code();
        $pdo->beginTransaction();
        try {
            $pdo->prepare('UPDATE classes SET active = 0, updated_at = UTC_TIMESTAMP() WHERE teacher_id = ? AND active = 1')
                ->execute([$teacherId]);
            $pdo->prepare(
                'INSERT INTO classes (code, teacher_id, teacher_name, name, grade, active) VALUES (?, ?, ?, ?, ?, 1)'
            )->execute([$code, $teacherId, (string) $teacher['display_name'], (string) $class['name'], (int) $class['grade']]);
            $pdo->commit();
        } catch (Throwable $e) {
            if ($pdo->inTransaction()) {
                $pdo->rollBack();
            }
            throw $e;
        }
        respond(['ok' => true, 'data' => ['class' => [
            'code' => $code,
            'name' => (string) $class['name'],
            'grade' => (int) $class['grade'],
        ]]]);
    }

    if ($action === 'students_list') {
        $class = teacher_class_or_fail($teacherId);
        $stmt = $pdo->prepare(
            'SELECT user_id, username, grade, level, xp, coins, done_count, done_ids_json, duel_wins, duel_best, updated_at '
            . 'FROM class_progress WHERE class_code = ? ORDER BY done_count DESC, xp DESC, username ASC'
        );
        $stmt->execute([(string) $class['code']]);
        $list = [];
        foreach ($stmt->fetchAll() as $row) {
            $list[] = [
                'uid' => (string) $row['user_id'],
                'username' => (string) $row['username'],
                'grade' => (int) $row['grade'],
                'level' => (int) $row['level'],
                'xp' => (int) $row['xp'],
                'coins' => (int) $row['coins'],
                'doneCount' => (int) $row['done_count'],
                'doneIds' => json_column($row['done_ids_json'], []),
                'duelWins' => (int) $row['duel_wins'],
                'duelBest' => (int) $row['duel_best'],
                'updatedAt' => (string) $row['updated_at'],
            ];
        }
        respond(['ok' => true, 'data' => ['list' => $list]]);
    }

    if ($action === 'assignments_list') {
        $class = teacher_class_or_fail($teacherId);
        $stmt = $pdo->prepare('SELECT * FROM assignments WHERE class_code = ? ORDER BY created_at DESC');
        $stmt->execute([(string) $class['code']]);
        respond(['ok' => true, 'data' => ['list' => array_map('assignment_payload', $stmt->fetchAll())]]);
    }

    if ($action === 'assignment_create') {
        $class = teacher_class_or_fail($teacherId);
        $title = need_string($data, 'title', 160);
        $grade = int_between($data['grade'] ?? $class['grade'], 1, 4, (int) $class['grade']);
        $subject = need_string($data, 'subj', 40);
        if (!in_array($subject, ['math', 'turkish', 'count', 'life', 'social', 'science'], true)) {
            throw new ApiProblem('Geçersiz ders seçimi.', 422, 'validation_error');
        }
        $gameIds = string_list($data['gameIds'] ?? []);
        if (!$gameIds) {
            throw new ApiProblem('En az bir oyun seçin.', 422, 'validation_error');
        }
        $due = optional_date($data, 'due');
        $note = trim((string) ($data['note'] ?? ''));
        if (strlen($note) > 500) {
            throw new ApiProblem('Ödev notu çok uzun.', 422, 'validation_error');
        }
        $id = bin2hex(random_bytes(16));
        $pdo->prepare(
            'INSERT INTO assignments (id, class_code, title, grade, subject, game_ids_json, due_date, note, active) '
            . 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)'
        )->execute([$id, (string) $class['code'], $title, $grade, $subject, json_db($gameIds), $due, $note]);
        respond(['ok' => true, 'data' => ['id' => $id]], 201);
    }

    if ($action === 'assignment_toggle') {
        $id = need_string($data, 'id', 64);
        if (!teacher_owns_record('assignments', $id, $teacherId)) {
            throw new ApiProblem('Ödev bulunamadı.', 404, 'assignment_not_found');
        }
        $pdo->prepare('UPDATE assignments SET active = ? WHERE id = ?')
            ->execute([bool_value($data['active'] ?? false) ? 1 : 0, $id]);
        respond(['ok' => true, 'data' => ['saved' => true]]);
    }

    if ($action === 'assignment_delete') {
        $id = need_string($data, 'id', 64);
        if (!teacher_owns_record('assignments', $id, $teacherId)) {
            throw new ApiProblem('Ödev bulunamadı.', 404, 'assignment_not_found');
        }
        $pdo->prepare('DELETE FROM assignments WHERE id = ?')->execute([$id]);
        respond(['ok' => true, 'data' => ['deleted' => true]]);
    }

    if ($action === 'contests_list') {
        $class = teacher_class_or_fail($teacherId);
        $stmt = $pdo->prepare('SELECT * FROM contests WHERE class_code = ? ORDER BY starts_at DESC, created_at DESC');
        $stmt->execute([(string) $class['code']]);
        respond(['ok' => true, 'data' => ['list' => array_map('contest_payload', $stmt->fetchAll())]]);
    }

    if ($action === 'contest_create') {
        $class = teacher_class_or_fail($teacherId);
        $title = need_string($data, 'title', 160);
        $kind = need_string($data, 'kind', 20);
        if (!in_array($kind, ['daily', 'weekly'], true)) {
            throw new ApiProblem('Geçersiz yarışma türü.', 422, 'validation_error');
        }
        $categories = [
            'topla' => ['Toplama', [1, 2, 3, 4]], 'cikar' => ['Çıkarma', [1, 2, 3, 4]],
            'carp' => ['Çarpma', [2, 3, 4]], 'bol' => ['Bölme', [3, 4]],
            'sayi' => ['Sayılar ve Örüntü', [1, 2]], 'kesir' => ['Kesirler', [3, 4]],
            'saat' => ['Saat ve Para', [2, 3]], 'hece' => ['Hece ve Sözcük', [1, 2]],
            'eszit' => ['Eş ve Zıt Anlam', [2, 3, 4]], 'essesli' => ['Eş Sesli Sözcükler', [3, 4]],
            'nokta' => ['Noktalama ve Yazım', [3, 4]], 'mix' => ['Karışık Dersler', [1, 2, 3, 4]],
        ];
        $catId = need_string($data, 'catId', 40);
        if (!isset($categories[$catId])) {
            throw new ApiProblem('Geçersiz yarışma konusu.', 422, 'validation_error');
        }
        $grade = int_between($data['grade'] ?? $class['grade'], 1, 4, (int) $class['grade']);
        if (!in_array($grade, $categories[$catId][1], true)) {
            throw new ApiProblem('Bu yarışma konusu seçilen sınıf düzeyine uygun değil.', 422, 'validation_error');
        }
        $startsAt = optional_date($data, 'startsAt');
        $endsAt = optional_date($data, 'endsAt');
        if ($startsAt !== null && $endsAt !== null && $endsAt < $startsAt) {
            throw new ApiProblem('Yarışma bitiş tarihi başlangıçtan önce olamaz.', 422, 'validation_error');
        }
        $id = bin2hex(random_bytes(16));
        $seed = random_int(1, 2000000000);
        $pdo->prepare(
            'INSERT INTO contests (id, class_code, title, kind, category_id, category_label, grade, seed, starts_at, ends_at, active) '
            . 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)'
        )->execute([
            $id, (string) $class['code'], $title, $kind, $catId, $categories[$catId][0],
            $grade, $seed, $startsAt, $endsAt,
        ]);
        respond(['ok' => true, 'data' => ['id' => $id]], 201);
    }

    if ($action === 'contest_toggle') {
        $id = need_string($data, 'id', 64);
        if (!teacher_owns_record('contests', $id, $teacherId)) {
            throw new ApiProblem('Yarışma bulunamadı.', 404, 'contest_not_found');
        }
        $pdo->prepare('UPDATE contests SET active = ? WHERE id = ?')
            ->execute([bool_value($data['active'] ?? false) ? 1 : 0, $id]);
        respond(['ok' => true, 'data' => ['saved' => true]]);
    }

    if ($action === 'contest_delete') {
        $id = need_string($data, 'id', 64);
        if (!teacher_owns_record('contests', $id, $teacherId)) {
            throw new ApiProblem('Yarışma bulunamadı.', 404, 'contest_not_found');
        }
        $pdo->prepare('DELETE FROM contests WHERE id = ?')->execute([$id]);
        respond(['ok' => true, 'data' => ['deleted' => true]]);
    }

    if ($action === 'contest_board') {
        $id = need_string($data, 'id', 64);
        if (!teacher_owns_record('contests', $id, $teacherId)) {
            throw new ApiProblem('Yarışma bulunamadı.', 404, 'contest_not_found');
        }
        $stmt = $pdo->prepare(
            'SELECT user_id, username, score, correct_count, grade, submitted_at '
            . 'FROM contest_scores WHERE contest_id = ? ORDER BY score DESC, submitted_at ASC LIMIT 200'
        );
        $stmt->execute([$id]);
        $list = [];
        foreach ($stmt->fetchAll() as $row) {
            $list[] = [
                'uid' => (string) $row['user_id'],
                'username' => (string) $row['username'],
                'score' => (int) $row['score'],
                'correct' => (int) $row['correct_count'],
                'grade' => (int) $row['grade'],
                'at' => (string) $row['submitted_at'],
            ];
        }
        respond(['ok' => true, 'data' => ['list' => $list]]);
    }

    throw new ApiProblem('Bilinmeyen öğretmen API işlemi.', 404, 'action_not_found');
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
