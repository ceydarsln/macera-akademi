<?php

declare(strict_types=1);

/** Server-owned live-match questions. Never return `answer` before a player submits. */
function live_options(string $correct, array $wrong): array
{
    $options = [$correct];
    foreach ($wrong as $value) {
        $value = (string) $value;
        if ($value !== $correct && !in_array($value, $options, true)) {
            $options[] = $value;
        }
        if (count($options) === 4) {
            break;
        }
    }
    if (count($options) !== 4) {
        throw new RuntimeException('Canlı yarışma sorusu için dört farklı seçenek üretilemedi.');
    }
    shuffle($options);
    return ['opts' => $options, 'answer' => array_search($correct, $options, true)];
}

function live_numeric(string $question, int $correct, int $spread, string $tip): array
{
    $candidates = [$correct + 1, $correct - 1, $correct + 2, $correct - 2,
        $correct + $spread, $correct - $spread, $correct + 2 * $spread, $correct - 2 * $spread];
    shuffle($candidates);
    $wrong = [];
    foreach ($candidates as $candidate) {
        if ($candidate >= 0 && $candidate !== $correct && !in_array((string) $candidate, $wrong, true)) {
            $wrong[] = (string) $candidate;
        }
    }
    for ($candidate = $correct + 3; count($wrong) < 3; $candidate++) {
        if (!in_array((string) $candidate, $wrong, true)) {
            $wrong[] = (string) $candidate;
        }
    }
    return array_merge(['q' => $question, 'tip' => $tip], live_options((string) $correct, $wrong));
}

function live_pick(array $items)
{
    return $items[random_int(0, count($items) - 1)];
}

function live_question(string $category, int $grade): array
{
    if ($category === 'topla') {
        $ranges = [1 => [[2, 9], [2, 9], 2], 2 => [[12, 58], [11, 40], 10],
            3 => [[105, 480], [105, 480], 100], 4 => [[1050, 4800], [1050, 4800], 1000]];
        [$left, $right, $spread] = $ranges[$grade];
        $a = random_int($left[0], $left[1]);
        $b = random_int($right[0], $right[1]);
        return live_numeric("➕ <b>$a + $b</b> = ?", $a + $b, $spread, "$a + $b = " . ($a + $b));
    }
    if ($category === 'cikar') {
        $ranges = [1 => [6, 19, 2, 1, 2], 2 => [35, 98, 12, 10, 10],
            3 => [320, 980, 105, 100, 100], 4 => [3200, 9800, 1050, 1000, 1000]];
        [$min, $max, $bMin, $gap, $spread] = $ranges[$grade];
        $a = random_int($min, $max);
        $b = random_int($bMin, $a - $gap);
        return live_numeric("➖ <b>$a − $b</b> = ?", $a - $b, $spread, "$a − $b = " . ($a - $b));
    }
    if ($category === 'carp') {
        $a = $grade === 4 ? random_int(12, 49) : random_int(2, $grade === 2 ? 5 : 10);
        $b = random_int($grade === 4 ? 3 : 2, $grade === 4 ? 9 : 10);
        return live_numeric("✖️ <b>$a × $b</b> = ?", $a * $b, max($a, $b), "$a × $b = " . ($a * $b));
    }
    if ($category === 'bol') {
        $divisor = random_int($grade === 3 ? 2 : 3, $grade === 3 ? 10 : 9);
        $quotient = random_int($grade === 3 ? 2 : 11, $grade === 3 ? 10 : 49);
        $a = $divisor * $quotient;
        return live_numeric("➗ <b>$a ÷ $divisor</b> = ?", $quotient, 2, "$a ÷ $divisor = $quotient");
    }
    if ($category === 'sayi') {
        $kind = random_int(1, 4);
        $limit = $grade === 1 ? 20 : 100;
        if ($kind === 1) {
            $n = random_int(3, $limit - 3);
            return array_merge(['q' => "🔢 <b>$n</b> sayısından sonra gelen sayı hangisidir?", 'tip' => "$n → " . ($n + 1)],
                live_options((string) ($n + 1), [$n - 1, $n + 2, $n - 2]));
        }
        if ($kind === 2) {
            $step = live_pick($grade === 1 ? [2, 5] : [2, 3, 5, 10]);
            $start = $step * random_int(1, max(1, intdiv($limit - 3 * $step, $step)));
            $answer = $start + 3 * $step;
            return array_merge(['q' => '🪜 Örüntüde sıradaki sayı: <b>' . "$start, " . ($start + $step)
                . ', ' . ($start + 2 * $step) . ', ?</b>', 'tip' => "$step ritmiyle → $answer"],
                live_options((string) $answer, [$answer + $step, $answer - $step, $answer + 1]));
        }
        if ($kind === 3) {
            $set = [];
            while (count($set) < 4) {
                $set[random_int(5, $limit)] = true;
            }
            $numbers = array_keys($set);
            return array_merge(['q' => '📏 Hangi sayı en büyüktür?', 'tip' => 'En büyük sayı ' . max($numbers)],
                live_options((string) max($numbers), array_map('strval', array_diff($numbers, [max($numbers)]))));
        }
        if ($grade === 1) {
            $n = random_int(11, 19);
            $answer = $n % 10;
            return array_merge(['q' => "🧮 <b>$n</b> sayısının birler basamağındaki rakam kaçtır?",
                'tip' => "$n → birler basamağı $answer"],
                live_options((string) $answer, [intdiv($n, 10), $answer + 1, $answer - 1,
                    $answer + 2, $answer - 2]));
        }
        $n = random_int(21, 98);
        $answer = intdiv($n, 10);
        return array_merge(['q' => "🧮 <b>$n</b> sayısının onlar basamağındaki rakam kaçtır?",
            'tip' => "$n → onlar basamağı $answer"],
            live_options((string) $answer, [$n % 10, $answer + 1, $answer - 1, $answer + 2, $answer - 2]));
    }
    if ($category === 'kesir') {
        $kind = random_int(1, 3);
        if ($kind === 1) {
            $den = live_pick([2, 3, 4, 5, 6, 8]);
            $num = random_int(1, $den - 1);
            $answer = "$num/$den";
            $wrong = [(($den - $num) . "/$den"), "$num/" . ($den + 1), ($num + 1) . "/$den",
                "1/$den", "$den/$den", '1/4', '2/3', '3/4', '2/5'];
            return array_merge(['q' => '🍕 ' . str_repeat('🟠', $num) . str_repeat('⚪', $den - $num)
                . '<br>Boyalı parçalar bütüne göre hangi kesirdir?', 'tip' => "$den eş parçanın $num tanesi → $answer"],
                live_options($answer, $wrong));
        }
        if ($kind === 2) {
            $den = live_pick([4, 5, 6, 8, 10]);
            $x = random_int(1, $den - 1);
            do { $y = random_int(1, $den - 1); } while ($x === $y);
            $larger = max($x, $y);
            return array_merge(['q' => "⚖️ <b>$x/$den</b> ile <b>$y/$den</b> kesirlerinden hangisi büyüktür?",
                'tip' => "Payı büyük olan → $larger/$den"],
                live_options("$larger/$den", [min($x, $y) . "/$den", "$den/$den", "1/$den", "2/$den", "3/$den"]));
        }
        $den = live_pick([6, 8, 10, 12]);
        $eaten = random_int(2, $den - 2);
        return live_numeric("🎂 $den dilim pastanın $eaten dilimi yendi. Kaç dilim kaldı?",
            $den - $eaten, 2, "$den − $eaten = " . ($den - $eaten));
    }
    if ($category === 'saat') {
        $kind = random_int(1, 3);
        if ($kind === 1) {
            $hour = random_int(1, 12);
            $minute = live_pick([0, 15, 30, 45]);
            $answer = sprintf('%02d:%02d', $hour, $minute);
            $wrong = [sprintf('%02d:%02d', $hour, ($minute + 15) % 60),
                sprintf('%02d:%02d', $hour % 12 + 1, $minute),
                sprintf('%02d:%02d', $hour, ($minute + 30) % 60)];
            return array_merge(['q' => "🕐 Saat $hour" . ($minute === 0 ? '' : " ve $minute dakika") . '. Rakamla nasıl yazılır?',
                'tip' => $answer], live_options($answer, $wrong));
        }
        if ($kind === 2) {
            $hours = random_int(2, 6);
            return live_numeric("⏱️ $hours saat kaç dakikadır?", $hours * 60, 60, "$hours × 60 = " . ($hours * 60));
        }
        $count = random_int(2, 6);
        $coin = live_pick([25, 50]);
        $answer = $count * $coin;
        $wrong = [$answer + $coin, $answer - $coin, $answer + 25, $answer - 25, $answer + 50];
        return array_merge(['q' => "🪙 $count tane $coin kuruş kaç kuruştur?", 'tip' => "$count × $coin = $answer kuruş"],
            live_options("$answer kuruş", array_map(static function ($v) { return "$v kuruş"; }, $wrong)));
    }
    if ($category === 'hece') {
        $bank = ['top' => 'top', 'ev' => 'ev', 'su' => 'su', 'kuş' => 'kuş', 'elma' => 'el-ma',
            'kitap' => 'ki-tap', 'kalem' => 'ka-lem', 'okul' => 'o-kul', 'çiçek' => 'çi-çek',
            'defter' => 'def-ter', 'sınıf' => 'sı-nıf', 'araba' => 'a-ra-ba', 'kelebek' => 'ke-le-bek',
            'pencere' => 'pen-ce-re', 'öğretmen' => 'öğ-ret-men', 'bilgisayar' => 'bil-gi-sa-yar',
            'kütüphane' => 'kü-tüp-ha-ne', 'ayakkabı' => 'a-yak-ka-bı'];
        if (random_int(0, 1) === 0) {
            $word = live_pick(array_keys($bank));
            $count = substr_count($bank[$word], '-') + 1;
            return array_merge(['q' => "🔤 <b>$word</b> sözcüğü kaç hecelidir?", 'tip' => $bank[$word] . " → $count hece"],
                live_options((string) $count, [($count + 1), max(1, $count - 1), ($count + 2), ($count + 3)]));
        }
        $target = random_int(1, 4);
        $matching = array_keys(array_filter($bank, static function ($v) use ($target) { return substr_count($v, '-') + 1 === $target; }));
        $others = array_keys(array_filter($bank, static function ($v) use ($target) { return substr_count($v, '-') + 1 !== $target; }));
        shuffle($others);
        $answer = live_pick($matching);
        return array_merge(['q' => "🔤 Hangi sözcük $target hecelidir?", 'tip' => $bank[$answer]],
            live_options($answer, $others));
    }
    if ($category === 'eszit') {
        $synonyms = [['büyük', 'iri'], ['küçük', 'ufak'], ['hızlı', 'çabuk'], ['cevap', 'yanıt'],
            ['siyah', 'kara'], ['hediye', 'armağan'], ['konuk', 'misafir'], ['yıl', 'sene'],
            ['kalp', 'yürek'], ['fakir', 'yoksul'], ['doktor', 'hekim'], ['kelime', 'sözcük']];
        $antonyms = [['büyük', 'küçük'], ['uzun', 'kısa'], ['sıcak', 'soğuk'], ['gece', 'gündüz'],
            ['ıslak', 'kuru'], ['ucuz', 'pahalı'], ['zor', 'kolay'], ['dolu', 'boş'],
            ['iyi', 'kötü'], ['genç', 'yaşlı'], ['temiz', 'kirli'], ['erken', 'geç']];
        $opposite = random_int(0, 1) === 1;
        $pair = live_pick($opposite ? $antonyms : $synonyms);
        $reverse = random_int(0, 1) === 1;
        $word = $pair[$reverse ? 1 : 0];
        $answer = $pair[$reverse ? 0 : 1];
        $wrong = [];
        foreach (array_merge($synonyms, $antonyms) as $candidate) {
            foreach ($candidate as $value) {
                if ($value !== $word && $value !== $answer && !in_array($value, $pair, true)) {
                    $sameMeaning = false;
                    foreach ($synonyms as $synonymPair) {
                        if (in_array($answer, $synonymPair, true) && in_array($value, $synonymPair, true)) {
                            $sameMeaning = true;
                            break;
                        }
                    }
                    if ($sameMeaning) { continue; }
                    $wrong[] = $value;
                }
            }
        }
        shuffle($wrong);
        $type = $opposite ? 'zıt' : 'eş';
        return array_merge(['q' => "🔁 <b>$word</b> sözcüğünün $type anlamlısı hangisidir?",
            'tip' => "$word → $answer"], live_options($answer, $wrong));
    }
    if ($category === 'essesli') {
        $bank = [
            ['yüz', 'Kütüphanede yüz kitap var.', 'yüz sayısı (100)'],
            ['yüz', 'Havuzda dikkatli yüz!', 'yüzmek eylemi'],
            ['kaz', 'Gölde bir kaz yüzüyordu.', 'kümes hayvanı'],
            ['kaz', 'Bahçede küçük bir çukur kaz.', 'kazmak eylemi'],
            ['yaz', 'Yaz gelince denize gideriz.', 'yaz mevsimi'],
            ['yaz', 'Adını deftere yaz.', 'yazmak eylemi'],
            ['gül', 'Bahçedeki gül kokuyor.', 'çiçek'],
            ['gül', 'Şakama biraz gül.', 'gülmek eylemi'],
            ['çay', 'Bir bardak çay içtik.', 'içecek'],
            ['çay', 'Köyün yanından bir çay akıyor.', 'küçük akarsu'],
        ];
        $entry = live_pick($bank);
        $wrong = [];
        foreach ($bank as $item) {
            if ($item[2] !== $entry[2]) { $wrong[] = $item[2]; }
        }
        shuffle($wrong);
        return array_merge(['q' => '🎭 ' . $entry[1] . '<br><b>' . $entry[0] . '</b> burada hangi anlamdadır?',
            'tip' => $entry[2]], live_options($entry[2], $wrong));
    }
    if ($category === 'nokta') {
        $sentences = [['Bugün hava çok güzel', '.'], ['Sen nerede oturuyorsun', '?'],
            ['Aman, ne kadar büyümüşsün', '!'], ['Kardeşim okula gitti', '.'],
            ['Bu kitabı kim getirdi', '?'], ['Eyvah, otobüsü kaçırdık', '!'],
            ['Yarın pikniğe gideceğiz', '.'], ['Saat kaçta buluşuyoruz', '?'],
            ['Yaşa, takımımız kazandı', '!'], ['Annem yemek hazırlıyor', '.'],
            ['Ödevini bitirdin mi', '?'], ['Ne güzel bir sürpriz', '!']];
        [$sentence, $punctuation] = live_pick($sentences);
        $names = ['.' => 'nokta ( . )', '?' => 'soru işareti ( ? )', '!' => 'ünlem işareti ( ! )', ',' => 'virgül ( , )'];
        return array_merge(['q' => "✍️ «{$sentence}» cümlesinin sonuna hangi işaret gelir?",
            'tip' => $sentence . $punctuation], live_options($names[$punctuation], array_values($names)));
    }
    throw new ApiProblem('Canlı yarışma kategorisi bulunamadı.', 422, 'invalid_game_category');
}

function live_build_questions(string $category, int $grade): array
{
    competition_category($category, $grade);
    $categories = ['topla', 'cikar', 'carp', 'bol', 'sayi', 'kesir', 'saat', 'hece', 'eszit', 'essesli', 'nokta'];
    $available = array_values(array_filter($categories, static function ($id) use ($grade) {
        try { competition_category($id, $grade); return true; }
        catch (ApiProblem $e) { return false; }
    }));
    shuffle($available);
    $questions = [];
    $seen = [];
    for ($attempt = 0; count($questions) < 8 && $attempt < 200; $attempt++) {
        $kind = $category === 'mix' ? $available[count($questions) % count($available)] : $category;
        $question = live_question($kind, $grade);
        if (!isset($question['q'], $question['opts'], $question['answer']) || count($question['opts']) !== 4
            || $question['answer'] < 0 || $question['answer'] > 3 || isset($seen[$question['q']])) {
            continue;
        }
        $seen[$question['q']] = true;
        $question['category'] = $kind;
        $questions[] = $question;
    }
    if (count($questions) !== 8) {
        throw new ApiProblem('Yarışma soruları hazırlanamadı.', 503, 'questions_unavailable');
    }
    return $questions;
}
