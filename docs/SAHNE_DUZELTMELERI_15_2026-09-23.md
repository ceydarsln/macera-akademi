# On beşinci paket — Atasözü yaşam sahneleri ve kayaç inceleme istasyonları

Bu paket Y42 Atasözü Köprüsü ve G13 Kayaç-Maden Masası oyunlarının ilk turlarını kapsar. Diğer turların kuralları ve doğru cevapları korunmuştur; katalog genelinde tasarım onayı değildir.

## Değişen oynanış

- Y42: Atasözü kartları artık sahnenin altındaki açıklama kutularına değil; günlük birikim, saklama, bütçeye göre harcama ve birlikte çalışma olaylarının içine sürüklenir. Doğru söz olay sahnesinde kalır ve kısa bir hareket oynar. İkinci karar ve üçüncü yazma turları korunur.
- G13: Kuvars, granit, kömür ve diğer örnekler alt taraftaki sınıf düğmelerine değil; kristal büyüteci, karma taneli kayaç tepsisi veya maden arabası istasyonuna yerleştirilir. Örnekler ilgili istasyonda birikir. İkinci eşleme ve üçüncü yazma turları korunur.
- Yanlış hedef ilerletmez; iptal edilen sürükleme yerleştirme yapmaz. Seçip dokunma/klavye alternatifi ve azaltılmış hareket desteği vardır. 320×568 telefonda kaynak ve hedefler aynı anda görünür; yatay ekranda da etkileşim yapılabilir.

## Doğrulama ve sınırlar

`tools/verify-scene-proverb-geology.cjs`: yenilenen turlarda **12 doğru gerçek fare sürüklemesi** (Y42 4, G13 8), yanlış hedef, iptal, klavye alternatifi, yerleşme animasyonu ve azaltılmış hareket tercihi kontrol edildi. Her iki oyunun üçer tur başlangıcı 320×568, 390×844 ve 844×390 ölçülerinde taşma/kırpılma açısından incelendi. Dar dikey ve yatay ekranda gerçek yerleştirme ayrıca yapıldı. Kanıt: `artifacts/sahne-duzeltmeleri-15-2026-09-23/verification.json`.

Y41–Y43 ve G12–G14 için **6 oyun / 18 tur** teknik çözüm regresyonu geçti. Katalog kaydı **635/635 oyun** teknik geçti; tüm katalog son değişiklikten sonra topluca yeniden çalıştırılmadı ve tasarım onayı değildir. Hedefli sahne düzeltmesi kaydı **37 oyun**; otomatik sahne dışı hedef sinyali **47 oyun**. Sinyal kesin hata sayısı değildir. Fiziksel cihaz/WebView ve kullanıcı görsel onayı açıktır.

İnceleme galerisi: `artifacts/sahne-duzeltmeleri-15-2026-09-23/index.html`. PNG'ler sabittir; animasyonu oyun bağlantısından izleyin.
