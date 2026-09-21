# Tasarım denetimi sonrası ilk düzeltme paketi

Bu teslim bütün oyunların yeniden tasarlandığı anlamına gelmez. Beş örnek oyunun sahneleri ve önceki denetimde bulunan mobil yönerge kırpılmaları ele alındı.

## Değişen davranışlar

- **P24 / Eşitlik Terazisi:** İlk iki turda işlem ağırlıkları gerçek sağ kefeye bırakılır. Kefe ve kol doğru değerde dengeye gelir; yanlış değerde uygun tarafa eğilir. Her ifade ayrı tartılır; bulunan eşitlikler kaydedilir, ağırlıklar yanlış biçimde üst üste toplanmaz. Üçüncü turun bilinmeyenleri de aynı terazi üzerinde gösterilir.
- **P15 / Çokluk Ölçeri:** İlk iki turda raftaki nesnelerle dolu kasalar doğrudan arabaya taşınır; kasa sayısı sınırlıdır. Arabadaki kasa dokunarak rafa geri konabilir. Üçüncü tur aynı pazar görselleriyle ters problemi gösterir.
- **Z04 / Kurallı Cümle Makinesi:** Sözcükler matbaanın kağıt bandına bırakılır. Dişliler döner, merdane hareket eder, yeni sözcük baskı animasyonuyla görünür. Üçüncü turda yazılan cümle matbaa kağıdında da gösterilir.
- **F03 / Araştırma Adımları:** Bırakma hedefi doğrudan defter sayfasıdır. Adım sayfaya yazılırken kalem hareket eder. Tekrarlanan harici sıra kutusu kaldırıldı; diğer turlar da defter görselini kullanır.
- **H12 / Afet Çantası:** İlk iki turda su şişesi, fener, battaniye, ilk yardım çantası, düdük, ilaç ve kimlik gibi çizilmiş nesneler açık çantaya taşınır. Nesne içeri yerleşir ve çantada görünür kalır. Yanlış nesne kabul edilmez. Üçüncü tur sözlü gerekçelendirme olarak korunur, aynı çanta görseli kullanılır.
- Matematik 1–4 ve Türkçe 3 başlıklarında yönerge yüksekliği içerikten belirlenir. Önceki denetimdeki **81 oyun / 124 tur** için 390 × 844 boyutunda yönerge kesilmesi yeniden ölçüldü ve giderildiği doğrulandı.

Yeni sahne parçaları mevcut HTML/CSS/SVG altyapısını kullanır; harici ağ veya raster görsel bağımlılığı yoktur. `scene-workshop.js` ve `scene-workshop.css`, `aynala.sh` ile Android varlıklarına da kopyalanır. Sürükleme sırasında üstte ayrı kopya kullanılır; iptal olayında kopya temizlenir ve nesne yerleştirilmez. Dokunarak taşıma korunur. Azaltılmış hareket tercihinde sonuç aynı kalırken eylem animasyonları kapatılır.

## Doğrulama

- Yeni beş oyunun **15/15 turu** tamamlandı.
- Ek regresyon oyunları: P10, P14, P21, P30, Z03, Z18, F02, F04. Yeni oyunlarla birlikte **13 farklı oyun / 39 tur** başarılı.
- Beş farklı sahnede gerçek işaretçi sürüklemesi, duruma yansıma ve beklenen CSS eylem animasyonu doğrulandı.
- Sürükleme iptali, yanlış terazi ağırlığı, kasayı geri koyma, gereksiz çanta malzemesinin reddi ve azaltılmış hareket kontrol edildi.
- Beş oyunun üç turu 320 × 568 ve 844 × 390 ölçülerinde yatay sayfa taşması ve yönerge kırpılması açısından kontrol edildi. Gerektiğinde sahne dikey kaydırılır.
- 390 × 844 ölçüsünde ilk tur, işlem sonrası, ikinci ve üçüncü tur PNG'leri üretildi; terazi stili çakışması ve matbaanın üçüncü turundaki sıkışma görsel inceleme sonrası düzeltildi.
- Tarayıcı doğrulamasıdır; fiziksel Android/iOS cihaz testi ve mobil klavyenin tüm davranışları ayrıca gereklidir. Kalan yüzlerce oyunun görsel/animasyon denetimi kapanmış değildir.

## İnceleme dosyaları

- Önce–sonra galerisi: `artifacts/sahne-duzeltmeleri-2026-09-21/index.html`
- Etkileşim/yerleşim ölçümleri: aynı dizinde `verification.json`
- Denetim öncesi referanslar: `artifacts/tasarim-denetimi-2026-09-21/`
- Tekrar üretim: `tools/verify-scene-workshop.cjs` (tam kontrol); `--scenes-only` önceki yönerge sonucunu koruyup beş sahneyi yeniden kontrol eder.

Sonraki iş: eski paketlerdeki benzer metin-hedef sorunlarını oyun özelinde düzeltmek. Bu beş örneğin tek biçimde bütün oyunlara uygulanması kabul ölçütü değildir.
