<?php

declare(strict_types=1);

$context = stream_context_create([
    'http' => [
        'timeout' => 5,
        'ignore_errors' => true,
    ],
]);
$urls = [
    'http://127.0.0.1/api/index.php?action=health',
    'http://127.0.0.1/api/teacher.php?action=health',
];

foreach ($urls as $url) {
    $body = @file_get_contents($url, false, $context);
    $result = is_string($body) ? json_decode($body, true) : null;
    if (!is_array($result) || ($result['ok'] ?? false) !== true) {
        exit(1);
    }
}

exit(0);
