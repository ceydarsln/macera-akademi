<?php

declare(strict_types=1);

final class ApiProblem extends RuntimeException
{
    public int $status;
    public string $errorCode;

    public function __construct(string $message, int $status = 400, string $errorCode = 'bad_request')
    {
        parent::__construct($message);
        $this->status = $status;
        $this->errorCode = $errorCode;
    }
}

function env_text(string $name, string $default = ''): string
{
    $value = getenv($name);
    return $value === false ? $default : trim((string) $value);
}

function env_bool(string $name, bool $default = false): bool
{
    $value = getenv($name);
    if ($value === false || trim((string) $value) === '') {
        return $default;
    }
    return filter_var($value, FILTER_VALIDATE_BOOLEAN);
}

function environment_config(): ?array
{
    $name = env_text('MACERA_DB_NAME');
    $user = env_text('MACERA_DB_USER');
    if ($name === '' || $user === '') {
        return null;
    }

    $originText = env_text(
        'MACERA_ALLOWED_ORIGINS',
        'https://maceraakademi.com.tr,https://www.maceraakademi.com.tr,https://appassets.androidplatform.net,null'
    );
    $origins = array_values(array_filter(array_map('trim', explode(',', $originText)), static function ($value) {
        return $value !== '';
    }));

    return [
        'database' => [
            'host' => env_text('MACERA_DB_HOST', 'db'),
            'port' => (int) env_text('MACERA_DB_PORT', '3306'),
            'name' => $name,
            'user' => $user,
            'password' => env_text('MACERA_DB_PASSWORD'),
            'charset' => env_text('MACERA_DB_CHARSET', 'utf8mb4'),
        ],
        'allowed_origins' => $origins,
        'token_ttl_days' => (int) env_text('MACERA_TOKEN_TTL_DAYS', '90'),
        'debug' => env_bool('MACERA_DEBUG', false),
    ];
}

function api_config(): array
{
    static $config = null;
    if (is_array($config)) {
        return $config;
    }

    $path = __DIR__ . '/config.local.php';
    $loaded = is_file($path) ? require $path : environment_config();
    if ($loaded === null) {
        throw new ApiProblem(
            'Sunucu yapılandırması eksik. config.local.php dosyasını veya MACERA_DB_* ortam değişkenlerini tanımlayın.',
            503,
            'config_missing'
        );
    }
    if (!is_array($loaded) || empty($loaded['database'])) {
        throw new ApiProblem('Sunucu yapılandırması geçersiz.', 503, 'config_invalid');
    }
    $config = $loaded;
    return $config;
}

function api_cors(): void
{
    $origin = isset($_SERVER['HTTP_ORIGIN']) ? (string) $_SERVER['HTTP_ORIGIN'] : '';
    if ($origin === '') {
        return;
    }

    $config = api_config();
    $allowed = isset($config['allowed_origins']) && is_array($config['allowed_origins'])
        ? $config['allowed_origins']
        : [];
    if (!in_array($origin, $allowed, true)) {
        throw new ApiProblem('Bu kaynaktan API erişimine izin verilmiyor.', 403, 'origin_denied');
    }

    header('Access-Control-Allow-Origin: ' . $origin);
    header('Vary: Origin');
    header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Macera-Token');
    header('Access-Control-Max-Age: 86400');
}

function db(): PDO
{
    static $pdo = null;
    if ($pdo instanceof PDO) {
        return $pdo;
    }

    $db = api_config()['database'];
    $host = (string) ($db['host'] ?? 'localhost');
    $port = (int) ($db['port'] ?? 3306);
    $name = (string) ($db['name'] ?? '');
    $user = (string) ($db['user'] ?? '');
    $password = (string) ($db['password'] ?? '');
    $charset = (string) ($db['charset'] ?? 'utf8mb4');
    if ($name === '' || $user === '' || $password === '' || $password === 'BURAYA_GUCLU_PAROLA_YAZIN') {
        throw new ApiProblem('MySQL bağlantı bilgileri güvenli biçimde tamamlanmamış.', 503, 'config_invalid');
    }

    $dsn = sprintf('mysql:host=%s;port=%d;dbname=%s;charset=%s', $host, $port, $name, $charset);
    try {
        $pdo = new PDO($dsn, $user, $password, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ]);
    } catch (PDOException $e) {
        throw new ApiProblem('MySQL bağlantısı kurulamadı.', 503, 'database_unavailable');
    }
    return $pdo;
}

function respond(array $payload, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

function input_data(): array
{
    $raw = file_get_contents('php://input');
    if ($raw === false || trim($raw) === '') {
        return $_POST;
    }
    if (strlen($raw) > 1048576) {
        throw new ApiProblem('İstek çok büyük.', 413, 'payload_too_large');
    }
    $data = json_decode($raw, true);
    if (!is_array($data)) {
        throw new ApiProblem('Geçersiz JSON isteği.', 400, 'invalid_json');
    }
    return $data;
}

function need_string(array $data, string $key, int $max = 255, bool $allowEmpty = false): string
{
    $value = isset($data[$key]) ? trim((string) $data[$key]) : '';
    if (!$allowEmpty && $value === '') {
        throw new ApiProblem($key . ' alanı gerekli.', 422, 'validation_error');
    }
    $length = preg_match_all('/./us', $value, $characters);
    if ($length === false) {
        throw new ApiProblem($key . ' alanı geçerli UTF-8 metni olmalı.', 422, 'validation_error');
    }
    if ($length > $max) {
        throw new ApiProblem($key . ' alanı çok uzun.', 422, 'validation_error');
    }
    return $value;
}

function int_between($value, int $min, int $max, int $fallback): int
{
    if (!is_numeric($value)) {
        return $fallback;
    }
    $number = (int) $value;
    return max($min, min($max, $number));
}

function username_key(string $username): string
{
    $value = trim($username);
    $value = strtr($value, [
        'Ç' => 'c', 'Ğ' => 'g', 'İ' => 'i', 'I' => 'i', 'Ö' => 'o', 'Ş' => 's', 'Ü' => 'u',
        'ç' => 'c', 'ğ' => 'g', 'ı' => 'i', 'ö' => 'o', 'ş' => 's', 'ü' => 'u',
    ]);
    $value = strtolower($value);
    $value = preg_replace('/[^a-z0-9]+/', '.', $value) ?? '';
    return trim($value, '.');
}

function json_value($value, $fallback)
{
    return is_array($value) ? $value : $fallback;
}

function json_db($value): string
{
    $encoded = json_encode($value, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    if (!is_string($encoded)) {
        throw new ApiProblem('Veri JSON biçimine çevrilemedi.', 422, 'invalid_profile');
    }
    return $encoded;
}

function json_column($value, $fallback)
{
    if (!is_string($value) || $value === '') {
        return $fallback;
    }
    $decoded = json_decode($value, true);
    return is_array($decoded) ? $decoded : $fallback;
}

function profile_from_row(array $row): array
{
    return [
        'uid' => (string) $row['id'],
        'username' => (string) $row['username'],
        'grade' => (int) $row['grade'],
        'email' => (string) ($row['parent_email'] ?? ''),
        'level' => (int) $row['level'],
        'xp' => (int) $row['xp'],
        'coins' => (int) $row['coins'],
        'coinsEarned' => (int) $row['coins_earned'],
        'look' => json_column($row['look_json'] ?? '', []),
        'owned' => json_column($row['owned_json'] ?? '', []),
        'badges' => json_column($row['badges_json'] ?? '', []),
        'duelStats' => json_column($row['duel_stats_json'] ?? '', []),
        'settings' => json_column($row['settings_json'] ?? '', []),
        'completed' => json_column($row['completed_json'] ?? '', []),
        'teacherCode' => (string) ($row['teacher_code'] ?? ''),
        'teacher' => (string) ($row['teacher_name'] ?? ''),
        'teacherUid' => isset($row['teacher_id']) && $row['teacher_id'] !== null ? (string) $row['teacher_id'] : '',
    ];
}

function bearer_token(array $data): string
{
    if (!empty($_SERVER['HTTP_X_MACERA_TOKEN'])) {
        return trim((string) $_SERVER['HTTP_X_MACERA_TOKEN']);
    }
    if (!empty($_SERVER['HTTP_AUTHORIZATION']) && preg_match('/^Bearer\s+(.+)$/i', (string) $_SERVER['HTTP_AUTHORIZATION'], $m)) {
        return trim($m[1]);
    }
    return isset($data['_token']) ? trim((string) $data['_token']) : '';
}

function current_user(array $data): array
{
    $token = bearer_token($data);
    if ($token === '') {
        throw new ApiProblem('Oturum bulunamadı. Lütfen yeniden giriş yapın.', 401, 'unauthorized');
    }

    $hash = hash('sha256', $token, true);
    $stmt = db()->prepare(
        'SELECT u.* FROM api_tokens t JOIN users u ON u.id = t.user_id '
        . 'WHERE t.token_hash = ? AND t.expires_at > UTC_TIMESTAMP() LIMIT 1'
    );
    $stmt->bindValue(1, $hash, PDO::PARAM_LOB);
    $stmt->execute();
    $user = $stmt->fetch();
    if (!$user) {
        throw new ApiProblem('Oturumun süresi doldu. Lütfen yeniden giriş yapın.', 401, 'session_expired');
    }

    db()->prepare('UPDATE api_tokens SET last_used_at = UTC_TIMESTAMP() WHERE token_hash = ?')
        ->execute([$hash]);
    return $user;
}

function issue_token(int $userId): string
{
    $raw = bin2hex(random_bytes(32));
    $hash = hash('sha256', $raw, true);
    $days = int_between(api_config()['token_ttl_days'] ?? 90, 1, 365, 90);
    $stmt = db()->prepare(
        'INSERT INTO api_tokens (user_id, token_hash, expires_at, created_at, last_used_at) '
        . 'VALUES (?, ?, DATE_ADD(UTC_TIMESTAMP(), INTERVAL ' . $days . ' DAY), UTC_TIMESTAMP(), UTC_TIMESTAMP())'
    );
    $stmt->bindValue(1, $userId, PDO::PARAM_INT);
    $stmt->bindValue(2, $hash, PDO::PARAM_LOB);
    $stmt->execute();
    return $raw;
}

function active_class_for_teacher(int $teacherId): ?array
{
    $stmt = db()->prepare(
        'SELECT code, name, grade, teacher_name, active, created_at, updated_at '
        . 'FROM classes WHERE teacher_id = ? AND active = 1 ORDER BY updated_at DESC LIMIT 1'
    );
    $stmt->execute([$teacherId]);
    $row = $stmt->fetch();
    return $row ?: null;
}

function teacher_profile_from_row(array $row, ?array $class = null): array
{
    if ($class === null) {
        $class = active_class_for_teacher((int) $row['id']);
    }
    return [
        'uid' => (string) $row['id'],
        'username' => (string) $row['username'],
        'fullName' => (string) ($row['display_name'] ?? ''),
        'email' => (string) ($row['email'] ?? ''),
        'class' => $class ? [
            'code' => (string) $class['code'],
            'name' => (string) $class['name'],
            'grade' => (int) $class['grade'],
        ] : null,
    ];
}

function current_teacher(array $data): array
{
    $token = bearer_token($data);
    if ($token === '') {
        throw new ApiProblem('Öğretmen oturumu bulunamadı. Lütfen yeniden giriş yapın.', 401, 'unauthorized');
    }

    $hash = hash('sha256', $token, true);
    $stmt = db()->prepare(
        'SELECT t.* FROM teacher_tokens tt JOIN teachers t ON t.id = tt.teacher_id '
        . 'WHERE tt.token_hash = ? AND tt.expires_at > UTC_TIMESTAMP() AND t.active = 1 LIMIT 1'
    );
    $stmt->bindValue(1, $hash, PDO::PARAM_LOB);
    $stmt->execute();
    $teacher = $stmt->fetch();
    if (!$teacher) {
        throw new ApiProblem('Öğretmen oturumunun süresi doldu. Lütfen yeniden giriş yapın.', 401, 'session_expired');
    }

    $touch = db()->prepare('UPDATE teacher_tokens SET last_used_at = UTC_TIMESTAMP() WHERE token_hash = ?');
    $touch->bindValue(1, $hash, PDO::PARAM_LOB);
    $touch->execute();
    return $teacher;
}

function issue_teacher_token(int $teacherId): string
{
    $raw = bin2hex(random_bytes(32));
    $hash = hash('sha256', $raw, true);
    $days = int_between(api_config()['token_ttl_days'] ?? 90, 1, 365, 90);
    $stmt = db()->prepare(
        'INSERT INTO teacher_tokens (teacher_id, token_hash, expires_at, created_at, last_used_at) '
        . 'VALUES (?, ?, DATE_ADD(UTC_TIMESTAMP(), INTERVAL ' . $days . ' DAY), UTC_TIMESTAMP(), UTC_TIMESTAMP())'
    );
    $stmt->bindValue(1, $teacherId, PDO::PARAM_INT);
    $stmt->bindValue(2, $hash, PDO::PARAM_LOB);
    $stmt->execute();
    return $raw;
}

function new_class_code(): string
{
    $alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    for ($attempt = 0; $attempt < 30; $attempt++) {
        $code = '';
        for ($i = 0; $i < 6; $i++) {
            $code .= $alphabet[random_int(0, strlen($alphabet) - 1)];
        }
        $stmt = db()->prepare('SELECT 1 FROM classes WHERE code = ? LIMIT 1');
        $stmt->execute([$code]);
        if (!$stmt->fetchColumn()) {
            return $code;
        }
    }
    throw new ApiProblem('Yeni sınıf kodu üretilemedi. Lütfen tekrar deneyin.', 503, 'class_code_unavailable');
}

function teacher_class_or_fail(int $teacherId): array
{
    $class = active_class_for_teacher($teacherId);
    if (!$class) {
        throw new ApiProblem('Aktif sınıf bulunamadı.', 409, 'class_missing');
    }
    return $class;
}

function teacher_owns_record(string $table, string $id, int $teacherId): bool
{
    if (!in_array($table, ['assignments', 'contests'], true)) {
        return false;
    }
    $stmt = db()->prepare(
        'SELECT 1 FROM ' . $table . ' r JOIN classes c ON c.code = r.class_code '
        . 'WHERE r.id = ? AND c.teacher_id = ? LIMIT 1'
    );
    $stmt->execute([$id, $teacherId]);
    return (bool) $stmt->fetchColumn();
}

function public_user(int $userId): ?array
{
    $stmt = db()->prepare('SELECT id, username, grade, level FROM users WHERE id = ? LIMIT 1');
    $stmt->execute([$userId]);
    $row = $stmt->fetch();
    if (!$row) {
        return null;
    }
    return [
        'uid' => (string) $row['id'],
        'username' => (string) $row['username'],
        'grade' => (int) $row['grade'],
        'level' => (int) $row['level'],
    ];
}

function require_user_id($value, string $message = 'Geçersiz kullanıcı.'): int
{
    if (!is_numeric($value) || (int) $value <= 0) {
        throw new ApiProblem($message, 422, 'validation_error');
    }
    return (int) $value;
}

function rate_key(string $action): string
{
    $ip = isset($_SERVER['REMOTE_ADDR']) ? (string) $_SERVER['REMOTE_ADDR'] : 'unknown';
    return hash('sha256', $action . '|' . $ip);
}

function rate_limit(string $action, int $maxAttempts = 12, int $windowMinutes = 10): void
{
    $pdo = db();
    $key = rate_key($action);
    $pdo->beginTransaction();
    try {
        $stmt = $pdo->prepare('SELECT attempts, window_started_at FROM api_rate_limits WHERE rate_key = ? FOR UPDATE');
        $stmt->execute([$key]);
        $row = $stmt->fetch();
        $expired = !$row || strtotime((string) $row['window_started_at']) < time() - ($windowMinutes * 60);
        if ($expired) {
            $pdo->prepare(
                'INSERT INTO api_rate_limits (rate_key, attempts, window_started_at) VALUES (?, 1, UTC_TIMESTAMP()) '
                . 'ON DUPLICATE KEY UPDATE attempts = 1, window_started_at = UTC_TIMESTAMP()'
            )->execute([$key]);
        } else {
            if ((int) $row['attempts'] >= $maxAttempts) {
                throw new ApiProblem('Çok fazla deneme yapıldı. Biraz bekleyip tekrar deneyin.', 429, 'rate_limited');
            }
            $pdo->prepare('UPDATE api_rate_limits SET attempts = attempts + 1 WHERE rate_key = ?')->execute([$key]);
        }
        $pdo->commit();
    } catch (Throwable $e) {
        if ($pdo->inTransaction()) {
            $pdo->rollBack();
        }
        throw $e;
    }
}

function clear_rate_limit(string $action): void
{
    db()->prepare('DELETE FROM api_rate_limits WHERE rate_key = ?')->execute([rate_key($action)]);
}

/**
 * Validate and normalize an eight-question contest/duel result.
 *
 * The browser is not allowed to choose the stored totals.  We rebuild them
 * from the per-question timings and correctness flags using the same formula
 * as the game.  This also gives the API a deliberately small, predictable
 * payload to persist instead of arbitrary client JSON.
 */
function competition_result(array $data, int $questionCount = 8, int $secondsPerQuestion = 12): array
{
    $answers = json_value($data['answers'] ?? null, []);
    if (count($answers) !== $questionCount || array_keys($answers) !== range(0, $questionCount - 1)) {
        throw new ApiProblem('Yarışma cevapları eksik veya geçersiz.', 422, 'invalid_game_result');
    }

    $normalized = [];
    $correct = 0;
    $score = 0;
    $streak = 0;
    $maxMs = $secondsPerQuestion * 1000;

    foreach ($answers as $answer) {
        if (!is_array($answer) || !isset($answer['ok']) || !is_bool($answer['ok'])
            || !isset($answer['ms']) || !is_int($answer['ms'])
            || $answer['ms'] < 0 || $answer['ms'] > $maxMs || $answer['ms'] % 100 !== 0) {
            throw new ApiProblem('Yarışma cevap dökümü geçersiz.', 422, 'invalid_game_result');
        }

        $isCorrect = $answer['ok'];
        $answerScore = 0;
        if ($isCorrect) {
            $answerScore = 10
                + max(0, (int) round(10 * (1 - ($answer['ms'] / $maxMs))))
                + min($streak, 5) * 2;
            $correct++;
            $streak++;
        } else {
            $streak = 0;
        }

        if (isset($answer['score']) && (!is_int($answer['score']) || $answer['score'] !== $answerScore)) {
            throw new ApiProblem('Yarışma puanı cevaplarla uyuşmuyor.', 422, 'invalid_game_result');
        }
        $score += $answerScore;
        $normalized[] = ['ok' => $isCorrect, 'ms' => $answer['ms'], 'score' => $answerScore];
    }

    if (!isset($data['score']) || !is_int($data['score']) || $data['score'] !== $score
        || !isset($data['correct']) || !is_int($data['correct']) || $data['correct'] !== $correct) {
        throw new ApiProblem('Yarışma toplamı cevaplarla uyuşmuyor.', 422, 'invalid_game_result');
    }

    return ['answers' => $normalized, 'score' => $score, 'correct' => $correct];
}

function competition_category(string $categoryId, int $grade): array
{
    $categories = [
        'topla' => ['Toplama', [1, 2, 3, 4]],
        'cikar' => ['Çıkarma', [1, 2, 3, 4]],
        'carp' => ['Çarpma', [2, 3, 4]],
        'bol' => ['Bölme', [3, 4]],
        'sayi' => ['Sayılar ve Örüntü', [1, 2]],
        'kesir' => ['Kesirler', [3, 4]],
        'saat' => ['Saat ve Para', [2, 3]],
        'hece' => ['Hece ve Sözcük', [1, 2]],
        'eszit' => ['Eş ve Zıt Anlam', [2, 3, 4]],
        'essesli' => ['Eş Sesli Sözcükler', [3, 4]],
        'nokta' => ['Noktalama ve Yazım', [3, 4]],
        'mix' => ['Karışık Dersler', [1, 2, 3, 4]],
    ];
    if (!isset($categories[$categoryId]) || !in_array($grade, $categories[$categoryId][1], true)) {
        throw new ApiProblem('Bu sınıf için geçersiz yarışma kategorisi.', 422, 'invalid_game_category');
    }
    return ['id' => $categoryId, 'label' => $categories[$categoryId][0]];
}

function same_pair(int $a, int $b): array
{
    return $a < $b ? [$a, $b] : [$b, $a];
}

function accepted_friends(int $a, int $b): bool
{
    [$low, $high] = same_pair($a, $b);
    $stmt = db()->prepare(
        "SELECT 1 FROM friendships WHERE user_low_id = ? AND user_high_id = ? AND status = 'accepted' LIMIT 1"
    );
    $stmt->execute([$low, $high]);
    return (bool) $stmt->fetchColumn();
}

function class_for_code(string $code): ?array
{
    $stmt = db()->prepare(
        'SELECT c.code, c.name, c.grade, c.teacher_id, '
        . "COALESCE(NULLIF(c.teacher_name, ''), t.display_name, t.username, '') AS teacher_name "
        . 'FROM classes c LEFT JOIN teachers t ON t.id = c.teacher_id WHERE c.code = ? AND c.active = 1 LIMIT 1'
    );
    $stmt->execute([strtoupper($code)]);
    $row = $stmt->fetch();
    return $row ?: null;
}
