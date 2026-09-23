# Onuncu paket — Sözcük kovukları ve kazı katmanları

Bu paket Y20 Eş Anlam Ormanı'nın birinci turunu ve G18 Kazı Seti'nin ikinci turunu kapsar. Diğer turların kuralları korunmuştur; katalog genelinde tasarım onayı değildir.

## Değişen oynanış

- Y20: Başlangıçtaki boş “orman” yazısı yerine dört ağaç ve doğrudan ağaç gövdesinde eş anlam kovukları var. Çocuk sözcüğü eşinin kovuğuna sürükler; doğru çift ağaçta kalır ve kısa büyüme animasyonu görünür. Metin/kanıt ve yazma turları aynı kaldı.
- G18: “Kaba iş / ince iş” alttaki ayrı düğmeler olmaktan çıktı. İki hedef, kazı sahnesinin fosilden uzak toprak bölgesi ve fosile yakın hassas bölgesidir. Alet küçük çizimiyle uygun bölgeye bırakılır, orada birikir ve kısa yerleşme animasyonu oynar. İlk tur set kurma ve üçüncü tur kazı planı korunur.
- Yanlış hedef ilerletmez, iptal edilen sürükleme yerleştirme yapmaz. Seçip dokunma/klavye alternatifi ve azaltılmış hareket desteği vardır. 320×568 telefonda Y20'nin dört kartı birlikte görünür; G18'de nesne ve kazı bölgesi aynı anda görünür. Yatay ekranda kaynak tepsisi sahnenin yanında durur.

## Doğrulama ve sınırlar

`tools/verify-scene-forest-dig.cjs`: yenilenen turlarda **10 gerçek fare sürüklemesi** (Y20 4, G18 6), yanlış hedef, iptal, klavye alternatifi, animasyon, azaltılmış hareket ve 320×568 / 390×844 / 844×390 düzenleri kontrol edildi. Dar dikey ve yatay ekranda gerçek yerleştirme ayrıca denendi. Kanıt: `artifacts/sahne-duzeltmeleri-10-2026-09-23/verification.json`.

Y19–Y21 ve G17–G19 için **6 oyun / 18 tur** teknik çözüm regresyonu geçti. Katalog kaydı **635/635 oyun** teknik geçti; bu tüm oyunların son değişiklikten sonra yeniden koşulduğu veya tasarım kabulü aldığı anlamına gelmez. Hedefli sahne düzeltmesi kaydı **27 oyun**; otomatik sahne dışı hedef sinyali **57 oyun**. Sinyal, kesin hata sayısı değildir. Fiziksel cihaz/WebView ve kullanıcı görsel onayı açıktır.

İnceleme galerisi: `artifacts/sahne-duzeltmeleri-10-2026-09-23/index.html`. PNG sabittir; animasyonu bağlantıdaki oyunda görün.
