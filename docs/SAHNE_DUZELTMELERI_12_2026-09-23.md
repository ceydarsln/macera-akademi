# On ikinci paket — Kitap sayfaları ve enerji istasyonları

Bu paket Y31 Kitap Anatomisi'nin ikinci turunu ve G31 Elektrikle mi Çalışıyor? oyununun ilk iki turunu kapsar. Diğer turların kuralları ve doğru cevapları korunmuştur; katalog genelinde tasarım onayı değildir.

## Değişen oynanış

- Y31: Bölüm kartları alttaki ayrı soru kutularına değil, işlevlerini anlatan gerçek kitap sayfalarına yerleştirilir. Dört sayfa kapak/iç sayfa görünümüyle ayrışır; doğru bölüm sayfada kalır ve kısa sayfa-yazılma animasyonu oynar. İlk sıralama ve üçüncü yazma turları korunur.
- G31: Çocuk aracı çizimiyle birlikte enerji atölyesinde görür ve ilk turda elektrikli/elektriksiz, ikinci turda priz/pil/el gücü istasyonuna sürükler. Araç çizimleri istasyonda birikir; bağlanma animasyonu ve açıklama görünür. Üçüncü yazma turu korunur. Kaşık, oyuncak araba ve kalemtıraş için karışmayacak ayrı çizimler yapıldı.
- Yanlış hedef ilerletmez; iptal edilen sürükleme yerleştirme yapmaz. Seçip dokunma/klavye alternatifi ve azaltılmış hareket desteği vardır. 320×568 telefonda kitabın dört sayfası, kaynak kartlar ve yönerge birlikte görünür. Yatay ekranda kaynak ve hedefler aynı anda kullanılabilir.

## Doğrulama ve sınırlar

`tools/verify-scene-book-power.cjs`: yenilenen turlarda **18 gerçek fare sürüklemesi** (Y31 4, G31 14), yanlış hedef, iptal, klavye alternatifi, yerleşme animasyonu ve azaltılmış hareket tercihi kontrol edildi. Üçer turun başlangıcı 320×568, 390×844 ve 844×390 ölçülerinde taşma/kırpılma açısından incelendi. Dar dikey ve yatay ekranda gerçek yerleştirme ayrıca yapıldı. Kanıt: `artifacts/sahne-duzeltmeleri-12-2026-09-23/verification.json`.

Y30–Y32 ve G30–G32 için **6 oyun / 18 tur** teknik çözüm regresyonu geçti. Katalog kaydı **635/635 oyun** teknik geçti; tüm katalog son değişiklikten sonra topluca yeniden çalıştırılmadı ve tasarım onayı değildir. Hedefli sahne düzeltmesi kaydı **31 oyun**; otomatik sahne dışı hedef sinyali **53 oyun**. Sinyal kesin hata sayısı değildir. Fiziksel cihaz/WebView ve kullanıcı görsel onayı açıktır.

İnceleme galerisi: `artifacts/sahne-duzeltmeleri-12-2026-09-23/index.html`. PNG'ler sabittir; animasyonu oyun bağlantısından izleyin.
