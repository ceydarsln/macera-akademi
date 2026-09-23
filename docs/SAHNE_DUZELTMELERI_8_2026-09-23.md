# Sekizinci paket — Yazı doğrudan sayfada

Bu paket Y19 Doğa Dergisi Masası ve Y58 Dilekçe Masası oyunlarının ilk iki turunu kapsar. Üçüncü yazma turları korunmuştur. Katalog genelinde tasarım onayı anlamına gelmez.

## Değişen oynanış

- Y19: Çocuk başlık, giriş, gelişme ve sonuç parçalarını derginin gerçek sayfasına yerleştirir. İkinci turda örnek cümleler aynı sayfanın ilgili alanlarında görünür. Gelişme bölümünde sütun vurgusu, başlıkta ayrı tipografi ve doğa çizimi vardır. Yerleştirme anında kısa baskı animasyonu oynar.
- Y58: Tarih, makam, istek metni ve kimlik alanı dilekçe kâğıdı üzerinde doldurulur. İkinci turda örnek içerikler aynı alanlara yazılır. Doğru yerleşme kısa yazı animasyonuyla görünür. Gerçek kişisel bilgi girmesi istenmez.
- Y58 ilk turundaki “yukarıdan aşağı” yönergesiyle veri dizisinin ters olması giderildi; sıra tarih → makam → istek metni → ad-soyad olarak düzenlendi. Bu, oyunun kendi sonuç metniyle uyumludur.
- Kaynak kartlar karışık sıradadır. Yanlış alana bırakma ilerlemeyi artırmaz. İptal edilen sürükleme yerleştirme yapmaz. Dokunarak seçme ve klavyeyle etkinleştirme alternatifleri vardır.
- Azaltılmış hareket tercihinde animasyon kapanır; tamamlanan sayfa ve sonuç korunur. Kısa yatay ekranda kaynak tepsisi sayfanın yanına yerleşir, içerik dikey kaydırılır.

## Kod sınırı ve denetim

scene-pages.js/css yalnız Y19 ve Y58 oyunlarının kule/sürükleme turlarına bağlanır. Diğer Türkçe 3 oyunları eski çizicilerini kullanır. tools/aynala.sh yeni varlıkları Android kopyasına taşır.

tools/verify-scene-pages.cjs iki oyunda toplam **16 gerçek fare yerleştirmesi** yaptı: her oyunda ilk iki turda dört parça. Yanlış hedef, sürükleme iptali, klavye alternatifi, animasyon, azaltılmış hareket ve 320×568, 390×844, 844×390 başlangıç düzenleri kontrol edildi. Küçük dikey ve yatay ekranda kaynak/sayfa etkileşimi ayrıca denendi. artifacts/sahne-duzeltmeleri-8-2026-09-23/verification.json test kaydıdır.

Y18, Y19, Y20, Y57, Y58, Y59, Y02 ve Y12 için **8 oyun / 24 tur** teknik çözüm regresyonu geçti. Bu teknik koşum, katalogdaki diğer oyunların son değişiklikten sonra baştan test edildiği anlamına gelmez. Yerel tarayıcı testleri fiziksel telefon/WebView doğrulaması değildir.

Görsel inceleme galerisi: artifacts/sahne-duzeltmeleri-8-2026-09-23/index.html. Her oyunda başlangıç, tamamlanmış ilk tur ve tamamlanmış ikinci tur PNG'leri ile oyun bağlantısı bulunur. Görseller animasyon videosu değildir.

Güncel izleme kaydında 635 oyun / 1.905 tur teknik çözümden geçiyor; denetim sonrası hedefli sahne düzeltmesi **23 oyun**, otomatik sahne dışı hedef sinyali **61 oyun**. Sinyal, doğrulanmış hata sayısı değildir. 635 oyunun tam tasarım ve gerçek cihaz kabulü açıktır.
