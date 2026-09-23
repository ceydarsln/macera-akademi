# On üçüncü paket — Benzetme makinesi ve bitki serası

Bu paket Y37 Benzetme Makinesi ve G37 Bitki İhtiyaçları oyunlarının ilk turlarını kapsar. Diğer turların kuralları ve doğru cevapları korunmuştur; katalog genelinde tasarım onayı değildir.

## Değişen oynanış

- Y37: Bulut, yıldız, tilki ve kaplumbağa kartları artık ayrı cevap kutularına değil, makinenin ilgili benzetme yuvasına sürüklenir. Doğru çift yuvada kalır; makinenin altındaki kâğıda tamamlanan benzetmeler basılır. Anlamsız benzetmeyi seçme ve kendi benzetmesini yazma turları korunur.
- G37: Bir kaynak bitki için gerekliyse kart doğrudan fide/toprak bölgesine, değilse seranın yan rafına sürüklenir. Su, ışık, hava, uygun sıcaklık ve mineral ihtiyacı karşılandıkça fide aşamalı büyür; gereksiz nesneler rafta birikir. Fazla su üzerine karar ve yazma turları korunur.
- Yanlış hedef ilerletmez; iptal edilen sürükleme yerleştirme yapmaz. Seçip dokunma/klavye alternatifi ve azaltılmış hareket desteği vardır. 320×568 telefonda kaynak ve sahne hedefleri aynı anda görünür; yatay ekranda da etkileşim yapılabilir.

## Doğrulama ve sınırlar

`tools/verify-scene-simile-greenhouse.cjs`: yenilenen turlarda **12 doğru gerçek fare sürüklemesi** (Y37 4, G37 8), yanlış hedef, iptal, klavye alternatifi, yerleşme/büyüme animasyonu ve azaltılmış hareket tercihi kontrol edildi. Her iki oyunun üçer tur başlangıcı 320×568, 390×844 ve 844×390 ölçülerinde taşma/kırpılma açısından incelendi. Dar dikey ve yatay ekranda gerçek yerleştirme ayrıca yapıldı. Kanıt: `artifacts/sahne-duzeltmeleri-13-2026-09-23/verification.json`.

Y36–Y38 ve G36–G38 için **6 oyun / 18 tur** teknik çözüm regresyonu geçti. Katalog kaydı **635/635 oyun** teknik geçti; tüm katalog son değişiklikten sonra topluca yeniden çalıştırılmadı ve tasarım onayı değildir. Hedefli sahne düzeltmesi kaydı **33 oyun**; otomatik sahne dışı hedef sinyali **51 oyun**. Sinyal kesin hata sayısı değildir. Fiziksel cihaz/WebView ve kullanıcı görsel onayı açıktır.

İnceleme galerisi: `artifacts/sahne-duzeltmeleri-13-2026-09-23/index.html`. PNG'ler sabittir; animasyonu oyun bağlantısından izleyin.
