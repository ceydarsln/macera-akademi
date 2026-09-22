# Yedinci paket — Mıknatıs deneyleri

Başlangıç: 21 Eylül 2026. Kullanım sınırında kesilen doğrulama 23 Eylül 2026'da tamamlandı. Mevcut bağlantıları korumak için paket klasörünün adı değiştirilmedi.

## Kapsam

F25 Mıknatıs Kutusu ve F26 Kutuplar oyunlarının ilk turları yenilendi. İkinci turdaki karar/gerekçe ve üçüncü turdaki yazma etkinlikleri korundu. Bu paket tüm kataloğun veya bu iki oyunun bütün tur türlerinin tasarım onayı değildir.

- F25: Çivi, plastik kaşık, çelik ataç, bardak, folyo, bakır tel, nikel para ve tahta kalem ayrı çizimlerle gösterilir. Çocuk nesneyi doğrudan soldaki sabit mıknatısa yaklaştırır. Çekilen nesne uca doğru hareket eder; çekilmeyen nesne deneme konumunda kalır.
- F26: Her iki mıknatıs da N ve S kutuplarıyla görünür. NN/NS/SS/SN eşleşmeleri korunur; karşı karşıya olan kutuplar doğru uçlarda çizilir. Yaklaştırılan mıknatıs aynı kutupta uzaklaşır, farklı kutupta yaklaşır. Soldaki mıknatıs sabittir.
- Akış artık “tahmini yazı kutusuna sürükle” değil, **nesneyi yaklaştır → hareketi gözle → sonucu kaydet**. Bu bilinçli bir ilk-tur öğretim akışı değişikliğidir; doğru sonuçlar değişmedi. Sonraki tur gözlenen örüntüyü yorumlatır.
- Gözlem bitmeden cevaplar etkinleşmez. Yanlış cevap deney kaydını artırmaz. Doğru cevap gerekçesiyle deftere işlenir; önceki kayıtlar korunur.
- “Deneyi tekrar yap” aynı nesneyi, ilerlemeyi artırmadan yeniden denemeyi sağlar.
- Nesneyi seçip mıknatısa dokunma ve klavyeyle etkinleştirme alternatifleri vardır. İptal edilen veya hedef dışına bırakılan sürükleme deneyi başlatmaz.
- Azaltılmış hareket tercihinde son konum ve gözlem korunur, hareket animasyonu kapatılır.

Bu bir öğretici ekran modelidir; sürekli kuvvet/mesafe hesaplayan fizik motoru değildir. Kullanıcıya ekran üzerinde de belirtilir.

## Kod sınırı

scene-magnets.js/css yalnız F25/F26 sınıflama turlarına bağlanır. Diğer Fen oyunlarının çizicisi değişmedi. Aynalama betiği yeni varlıkları Android paketine kopyalar.

Katalog tarayıcısı gerçek mıknatıs hedefini sayar. data-observation-answer ile işaretlenen cevap düğmeleri sürükleme hedefi sayılmaz; bunlarda bırakma işleyicisi yoktur. Diğer oyunların hedef tarama ölçütü değiştirilmedi.

## Doğrulama

- tools/verify-scene-magnets.cjs: F25'te sekiz, F26'da dört olmak üzere **12 gerçek fare sürüklemesiyle deney ve doğru gözlem kaydı**.
- Her iki oyunda yanlış cevap, hedef dışına bırakma, işaretçi iptali, klavye alternatifi, tekrar deneme, azaltılmış hareket, animasyon adı ve hareket sırasında cevap kilidi ayrı denetlendi.
- Deneyin tek başına puan/ilerleme sağlamadığı; doğru gözlem cevabından sonra kayıt sayısının bir arttığı doğrulandı.
- Üç turun başlangıcı 320×568, 390×844 ve 844×390 ölçülerinde yatay taşma/yönerge kırpılması açısından kontrol edildi.
- Ek gerçek sürükleme kontrolü, 844×390 ekranda cevapların deney alanının üstüne bindiğini yakaladı. Sahne ve cevap bölümlerinin flex ile daralması kaldırıldı; kısa ekranlarda içerik dikey kaydırılıyor. Son koşumda iki oyunun 320×568 ve 844×390 deneyleri, kaynak/hedefin başka kontroller altında kalmadığı kontrolüyle geçti.
- İki oyunda 320×568 ve 844×390 ölçülerinde aşağı kaydırarak cevabı seçme ve bir sonraki nesneye geçme de ayrı bir tarayıcı kontrolünde geçti.
- F03, F05, F24, F25, F26, F27: **6 oyun / 18 tur** teknik çözüm regresyonu geçti. Fen çözüm aracı yeni deney için dokunarak seçme/yaklaştırma adımlarını kullanır.
- 133 HTML dosyasının gömülü JS ve yerel varlık taraması geçti; yeni JS sözdizimi ve kaynak/Android eşitliği kontrol edildi.
- PNG incelemesinde nesne çizimleri, kutup yönleri ve sonuç konumları değerlendirildi. Fiziksel telefon/WebView testi yapılmadı.

## İnceleme ve devam

- artifacts/sahne-duzeltmeleri-7-2026-09-21/index.html: önce/yeni/iki farklı deney ekranı ve çalışır oyun bağlantıları.
- Aynı klasörde verification.json: etkileşim ve yerleşim testleri.
- docs/OYUN_SAHNE_KANITLARI.json: denetim sonrasındaki hedefli sahne düzeltmesi kaydı artık **21 oyun**.
- artifacts/katalog-kabul-635/index.html: güncellenmiş üç tur kayıtları.

Önceki “65 sahne dışı hedef sinyali” sayısındaki F25/F26 artık gerçek mıknatıs hedefini kullanır; kalan sinyal **63 oyun**. Bu sayı kesin hata veya toplam kalan oyun sayısı değildir. 635 oyunun tamamı için görsel/etkileşim kabulü hâlâ açık; teknik çözüm testi tasarım onayı değildir.
