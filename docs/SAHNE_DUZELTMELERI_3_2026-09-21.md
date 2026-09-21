# Üçüncü sahne düzeltme paketi — 21 Eylül 2026

## Kapsam

Üç matematik oyununun sürükleme sahneleri yenilendi. Tüm katalog veya bu oyunların bütün tur türleri yeniden tasarlanmış değildir.

- **P11 Denk Kesir Köprüsü:** Üç turdaki kesir şeritleri eşit boyda bütünler üzerinde, aynı başlangıç çizgisine oturur. Boyalı uçlar hizalanır; pay ve paydanın genişletme/sadeleştirme çarpanı gösterilir. İkinci turdaki iki 1/3 hedefi artık ×2 ve ×3 olarak açıkça ayrılır; yönerge de bu koşulu belirtir.
- **P16 Birim Dönüşüm Kartları:** İlk iki turda uzunluk çubukları cetvelin sıfır çizgisine oturur. Farklı birimler, dönüşüm çarpanı ve eşit uzunluk sonucu görünür. Çizimler temsili ölçektedir; ekranın fiziksel santimetresi değildir. Üçüncü turdaki kütle hafızası korunmuştur.
- **P38 Açı Kartları:** Birinci ve üçüncü turda duvar–zemin, makas, kitap, yol ve dönüş çizimleri açı modeline yerleşir. Nesnenin köşesi ve kolları modelle aynı koordinatları kullanır. Model kolu eylem sırasında döner. İkinci turdaki hafıza ve son açıklama sorusu korunmuştur.

## Uygulama

`scene-measure.js/css` yalnız P11/P16/P38 sürükleme turlarına bağlanır. Önceki paketlerdeki `scene-workshop` sürükleme yardımcısı kullanılır. İptal edilen sürükleme işlem yapmaz; kaynak ve hedefe dokunma veya klavyeyle etkinleştirme alternatifi vardır. Azaltılmış hareket tercihinde yeni animasyonlar kapanır, sonuç korunur.

`tools/aynala.sh` yeni dosyaları Android varlıklarına kopyalar. Kullanıcının mevcut devir ZIP/PDF dosyaları kapsam dışındadır ve değiştirilmemiştir.

## Doğrulama

- `tools/verify-scene-measure.cjs`: Yanlış hedef, sürükleme iptali, klavye alternatifi, aktif eylem animasyonu ve azaltılmış hareket kontrolü.
- Bütün yeni sürükleme turları 390×844 ekranda gerçek fare sürüklemesiyle: P11 9, P16 7, P38 5 — toplam **21 yerleştirme**.
- Üç oyunun üçer tur başlangıcı 320×568, 390×844 ve 844×390 ölçülerinde: yönerge kırpılması ve sayfa/sahne yatay taşması kontrolü. Bu ölçümler fiziksel cihaz testi değildir.
- Tam çözüm regresyonu **12 oyun / 36 tur** geçti: P03, P08, P10, P11, P12, P15, P16, P17, P24, P37, P38, P39. Son etkileşim koşumunun kaydı aşağıdaki JSON dosyasındadır.
- Son yerleştirme animasyonunun soru/tur geçişiyle kesilmemesi için normal oynanışta 700 ms beklenir. Hızlı çözüm testi modunda bu bekleme kaldırılır.
- Gömülü JavaScript ve yeni JS sözdizimi, yeni varlıkların kaynak/Android eşitliği, `git diff --check` kontrol edildi.
- P11/P16/P38 başlangıç/sonuç ekranları ve P11/P16 ikinci tur ekranları görsel olarak incelendi. Birim çarpanı ifadesi `1 cm = 10 mm · sayı ×10` biçiminde netleştirildi; uzunluğun kendisinin 10 katına çıktığı izlenimi giderildi.

## İnceleme

`artifacts/sahne-duzeltmeleri-3-2026-09-21/index.html`: Önce / yeni / işlem sonrası görseller ve çalışır oyun bağlantıları.

`artifacts/sahne-duzeltmeleri-3-2026-09-21/verification.json`: Son başarılı etkileşim ve yerleşim test kaydı.

Görseller sabittir, animasyon kaydı değildir. Diğer denetim bulguları ve fiziksel Android/iPhone doğrulaması henüz tamamlanmış sayılmaz.
