<?php

declare(strict_types=1);

require __DIR__ . '/../web/api/bootstrap.php';
require __DIR__ . '/../web/api/live-questions.php';

$cases = 0;
foreach (['topla', 'cikar', 'carp', 'bol', 'sayi', 'kesir', 'saat', 'hece', 'eszit', 'essesli', 'nokta', 'mix'] as $category) {
    for ($grade = 1; $grade <= 4; $grade++) {
        try { competition_category($category, $grade); }
        catch (ApiProblem $e) { continue; }
        for ($run = 0; $run < 30; $run++) {
            $questions = live_build_questions($category, $grade);
            if (count($questions) !== 8 || count(array_unique(array_column($questions, 'q'))) !== 8) {
                throw new RuntimeException("$grade/$category: sekiz farklı soru yok");
            }
            foreach ($questions as $question) {
                if (count($question['opts']) !== 4 || count(array_unique($question['opts'])) !== 4
                    || !is_int($question['answer']) || $question['answer'] < 0 || $question['answer'] > 3
                    || trim($question['q']) === '') {
                    throw new RuntimeException("$grade/$category: geçersiz soru");
                }
                if ($grade === 1 && $category === 'sayi'
                    && strpos($question['q'], 'onlar basamağındaki') !== false) {
                    throw new RuntimeException('1. sınıfa 20 üstü basamak sorusu üretildi');
                }
                if ($category === 'nokta' && preg_match('/«[^»]+»/u', $question['q']) !== 1) {
                    throw new RuntimeException('Noktalama sorusunda cümle görünmüyor');
                }
            }
            $cases++;
        }
    }
}
echo "Canlı soru üretimi: $cases / $cases başarılı\n";
