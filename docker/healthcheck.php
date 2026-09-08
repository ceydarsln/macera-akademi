<?php

declare(strict_types=1);

$context = stream_context_create([
    'http' => [
        'timeout' => 5,
        'ignore_errors' => true,
    ],
]);
$body = @file_get_contents('http://127.0.0.1/api/index.php?action=health', false, $context);
$result = is_string($body) ? json_decode($body, true) : null;

exit(is_array($result) && ($result['ok'] ?? false) === true ? 0 : 1);
