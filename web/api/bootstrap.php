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

function api_config(): array
{
    static $config = null;
    if (is_array($config)) {
        return $config;
    }

    $path = __DIR__ . '/config.local.php';
    if (!is_file($path)) {
        throw new ApiProblem(
            'Sunucu yapılandırması eksik. api/config.sample.php dosyasını config.local.php olarak kopyalayın.',
            503,
            'config_missing'
        );
    }

    $loaded = require $path;
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
    $charset = (string) ($db['charset'] ?? 'utf8mb4');
    if ($name === '') {
        throw new ApiProblem('MySQL veritabanı adı tanımlanmamış.', 503, 'config_invalid');
    }

    $dsn = sprintf('mysql:host=%s;port=%d;dbname=%s;charset=%s', $host, $port, $name, $charset);
    try {
        $pdo = new PDO($dsn, (string) ($db['user'] ?? ''), (string) ($db['password'] ?? ''), [
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
    if (strlen($value) > $max * 4) {
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
