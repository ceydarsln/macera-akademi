# On dördüncü paket — Jest/mimik aynası ve madde deney tezgâhı

Bu paket Y38 Jest ve Mimik Aynası'nın ilk iki turunu ve G19 Maddenin Hâlleri'nin ilk iki turunu kapsar. Diğer turların kuralları ve doğru cevapları korunmuştur; katalog genelinde tasarım onayı değildir.

## Değişen oynanış

- Y38: Yüz ve beden ipucu kartları artık dışarıdaki duygu cevap kutularına değil, ayna yüzeylerine sürüklenir. Doğru eşleşmede yüz aynada görünür; beden duruşu mutluluk, üzüntü, öfke, şaşkınlık, korku ve heyecana göre değişir. İkinci turdaki yakın duygular korunur; üçüncü canlandırma turuna dokunulmadı.
- G19: Madde örneği katılar için tepsiye, sıvılar için deney kabına veya gazlar için balona sürüklenir. Örnekler düzenekte birikir; ikinci turdaki kum, un, bal ve buhar gibi zor örneklerin sınıflandırması da aynı deney sahnesinde yapılır. Üçüncü gerekçeli yazma turu korunur.
- Yanlış hedef ilerletmez; iptal edilen sürükleme yerleştirme yapmaz. Seçip dokunma/klavye alternatifi ve azaltılmış hareket desteği vardır. 320×568 telefonda kaynak ve hedefler aynı anda görünür; yatay ekranda da etkileşim yapılabilir.

## Doğrulama ve sınırlar

`tools/verify-scene-mirror-matter.cjs`: yenilenen turlarda **23 doğru gerçek fare sürüklemesi** (Y38 8, G19 15), yanlış hedef, iptal, klavye alternatifi, yerleşme animasyonu ve azaltılmış hareket tercihi kontrol edildi. Her iki oyunun üçer tur başlangıcı 320×568, 390×844 ve 844×390 ölçülerinde taşma/kırpılma açısından incelendi. Dar dikey ve yatay ekranda gerçek yerleştirme ayrıca yapıldı. Kanıt: `artifacts/sahne-duzeltmeleri-14-2026-09-23/verification.json`.

Y37–Y39 ve G18–G20 için **6 oyun / 18 tur** teknik çözüm regresyonu geçti. Katalog kaydı **635/635 oyun** teknik geçti; tüm katalog son değişiklikten sonra topluca yeniden çalıştırılmadı ve tasarım onayı değildir. Hedefli sahne düzeltmesi kaydı **35 oyun**; otomatik sahne dışı hedef sinyali **49 oyun**. Sinyal kesin hata sayısı değildir. Fiziksel cihaz/WebView ve kullanıcı görsel onayı açıktır.

İnceleme galerisi: `artifacts/sahne-duzeltmeleri-14-2026-09-23/index.html`. PNG'ler sabittir; animasyonu oyun bağlantısından izleyin.
