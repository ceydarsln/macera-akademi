# On birinci paket — Kurulan köprü ve hareket yolları

Bu paket Y28 Eş Anlam Köprüsü'nün birinci turunu ve G25 Hareket Türleri'nin ilk iki turunu kapsar. Diğer turların kuralları ve cevapları korunmuştur; katalog genelinde tasarım onayı değildir.

## Değişen oynanış

- Y28: Köprü yalnız sayaç olmaktan çıktı. Bağlam cümlesi, doğru eş anlamlı sözcüğün bulunduğu geçidin boş tahtasına sürüklenir. Doğru cümle geçitte kalır ve kısa tahta-kurulma animasyonu oynar. İkinci karar ve üçüncü konuşma turları korunur.
- G25: Nesne artık sahnede çizim ve adıyla yer alır. Çocuk “Hareketi izle” düğmesiyle dönme, sallanma, yön değiştirme, yuvarlanma veya ilerlemeyi gözlemler; ardından nesneyi park sahnesinin ilgili hareket yoluna sürükler. İlk turdaki üç temel yol ile ikinci turdaki birleşik hareket yolları ayrı adlandırılmıştır. Yerleşen nesneler yol üzerinde birikir. Üçüncü yazma turu korunur.
- Yanlış hedef ilerletmez; iptal edilen sürükleme yerleştirme yapmaz. Seçip dokunma/klavye alternatifi ve azaltılmış hareket desteği vardır. 320×568 ekranda Y28'in dört kaynak cümlesi birlikte görünür. Yatay ekranda kaynak ve hedefler aynı anda kullanılabilir.

## Doğrulama ve sınırlar

`tools/verify-scene-bridges-motion.cjs`: yenilenen turlarda **18 gerçek fare sürüklemesi** (Y28 4, G25 14), yanlış hedef, iptal, klavye alternatifi, hareket izleme animasyonu, yerleşme animasyonu ve azaltılmış hareket tercihleri kontrol edildi. Üçer turun başlangıcı 320×568, 390×844 ve 844×390 ölçülerinde taşma/kırpılma açısından incelendi. Dar dikey ve yatay ekranda gerçek yerleştirme ayrıca yapıldı. Kanıt: `artifacts/sahne-duzeltmeleri-11-2026-09-23/verification.json`.

Y27–Y29 ve G24–G26 için **6 oyun / 18 tur** teknik çözüm regresyonu geçti. Katalog kaydı **635/635 oyun** teknik geçti; tüm katalog son değişiklikten sonra topluca yeniden çalıştırılmadı ve tasarım onayı değildir. Hedefli sahne düzeltmesi kaydı **29 oyun**; otomatik sahne dışı hedef sinyali **55 oyun**. Sinyal kesin hata sayısı değildir. Fiziksel cihaz/WebView ve kullanıcı görsel onayı açıktır.

İnceleme galerisi: `artifacts/sahne-duzeltmeleri-11-2026-09-23/index.html`. PNG'ler sabittir; animasyonu oyun bağlantısından izleyin.
