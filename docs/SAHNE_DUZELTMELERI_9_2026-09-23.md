# Dokuzuncu paket — Harita ve geri dönüşümde gerçek hedefler

Bu paket Y52 Eser Haritası'nın ilk iki turunu ve G23 Geri Dönüşüm Kutuları'nın ilk turunu kapsar. Her iki oyunun kalan tur türleri korunmuştur. Katalog genelinde tasarım onayı anlamına gelmez.

## Değişen oynanış

- Y52: Eser kartı, sahnedeki şematik Türkiye haritasının ilgili şehir işaretine sürüklenir. Yerleşen eserin adı işarette kalır. İkinci turda İstanbul'un cami ve saray hedefleri ayrıdır. Kısa yerleşme animasyonu, seç-dokun ve klavye alternatifleri bulunur. Üçüncü yazma turu değişmedi.
- G23: Atık nesnesi, alttaki yazı hedefine değil, sahnedeki renkli kutunun ağzına bırakılır. Kutuda biriken nesneler resimleriyle görünür. Nesneler için oyun verisinden türetilen küçük çizimler ve düşme animasyonu vardır. İkinci karar ve üçüncü yazma turları değişmedi; sınıflama cevapları da değiştirilmedi.
- 320×568 ekranda harita kartları yatay tepside, harita ve en az bir kart aynı anda görünür; diğer kartlar için kaydırma yönergesi vardır. Geri dönüşüm kutuları bu boyutta kısalır. 844×390 yatay ekranda kutular ve nesne yan yana görünür.
- Yanlış hedefte ilerleme olmaz. İptal edilen sürükleme yerleştirme yapmaz. Azaltılmış hareket tercihinde animasyon kapanır, sonuç görünür kalır.

## Doğrulama ve sınırlar

`tools/verify-scene-destinations.cjs`: yenilenen turlarda **16 gerçek fare yerleştirmesi** (Y52 8, G23 8), ayrıca yanlış hedef, iptal, klavye alternatifi, animasyon ve azaltılmış hareket kontrolleri. Üçer tur başlangıcı 320×568, 390×844 ve 844×390 ölçülerinde yatay taşma ve yönerge kırpılması açısından kontrol edildi. Dar telefon ile yatay ekranda gerçek kaynak-hedef yerleştirmesi ayrıca denendi. Kanıt: `artifacts/sahne-duzeltmeleri-9-2026-09-23/verification.json`.

Y52 ve G23 ile komşu Y51, Y53, G22 ve G24 için **6 oyun / 18 tur** teknik çözüm regresyonu geçti; katalog kaydı **635/635 oyun** teknik geçti durumunda. Bu, bütün oyunların son değişikliklerden sonra topluca yeniden koşulduğu veya tasarım kabulü aldığı anlamına gelmez. Katalogdaki otomatik sahne dışı hedef sinyali **59 oyun**; bu kesin hata sayısı değildir. Denetim sonrası hedefli sahne düzeltmesi kaydı **25 oyun**. Fiziksel telefon/Android WebView ve kullanıcı görsel onayı hâlâ gereklidir.

Görsel inceleme: `artifacts/sahne-duzeltmeleri-9-2026-09-23/index.html`. PNG'ler sabittir; hareketi görmek için galerideki oyun bağlantıları kullanılmalıdır.
