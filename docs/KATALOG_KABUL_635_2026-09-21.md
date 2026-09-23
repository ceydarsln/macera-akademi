# 635 oyun: teknik kontrol ve tasarım kabulü

## Son ek: on üçüncü paket

Y37 Benzetme Makinesi'nin ilk turunda kartlar makinenin eşleşme yuvalarına, G37 Bitki İhtiyaçları'nın ilk turunda kaynaklar doğrudan fideye veya yan rafa taşınıyor. Hedefli sahne düzeltmesi kaydı **33 oyuna** ulaştı; güncel otomatik sahne dışı hedef sinyali **51 oyun**. Y36–Y38 ve G36–G38, toplam 6 oyun / 18 tur teknik regresyondan geçti. Ayrıntılar: docs/SAHNE_DUZELTMELERI_13_2026-09-23.md. Aşağıdaki sayılar tarihsel kontrol noktalarıdır.

## Son ek: on ikinci paket

Y31 Kitap Anatomisi'nin ikinci turunda bölümler kitap sayfalarına yerleşiyor; G31 Elektrikle mi Çalışıyor? oyununun ilk iki turunda araçlar uygun enerji istasyonlarına taşınıyor. Hedefli sahne düzeltmesi kaydı **31 oyuna** ulaştı; güncel otomatik sahne dışı hedef sinyali **53 oyun**. Y30–Y32 ve G30–G32, toplam 6 oyun / 18 tur teknik regresyondan geçti. Ayrıntılar: docs/SAHNE_DUZELTMELERI_12_2026-09-23.md. Aşağıdaki sayılar tarihsel kontrol noktalarıdır.

## Son ek: on birinci paket

Y28 Eş Anlam Köprüsü'nün ilk turunda cümleler gerçek köprü geçitlerini kuruyor; G25 Hareket Türleri'nin ilk iki turunda nesneler hareketleri gözlendikten sonra sahnedeki hareket yollarına taşınıyor. Hedefli sahne düzeltmesi kaydı **29 oyuna** ulaştı; güncel otomatik sahne dışı hedef sinyali **55 oyun**. Y27–Y29 ve G24–G26, toplam 6 oyun / 18 tur teknik regresyondan geçti. Ayrıntılar: docs/SAHNE_DUZELTMELERI_11_2026-09-23.md. Aşağıdaki sayılar tarihsel kontrol noktalarıdır.

## Son ek: onuncu paket

Y20 Eş Anlam Ormanı'nın ilk turunda sözcükler ağaç kovuklarında; G18 Kazı Seti'nin ikinci turunda aletler kaba ve hassas toprak bölgelerinde birikiyor. Hedefli sahne düzeltmesi kaydı **27 oyuna** ulaştı; güncel otomatik sahne dışı hedef sinyali **57 oyun**. Y19–Y21 ve G17–G19, toplam 6 oyun / 18 tur teknik regresyondan geçti. Ayrıntılar: docs/SAHNE_DUZELTMELERI_10_2026-09-23.md. Aşağıdaki sayılar tarihsel kontrol noktalarıdır.

## Son ek: dokuzuncu paket

Y52 Eser Haritası'nın ilk iki turunda eserler doğrudan şematik haritanın şehir işaretlerine; G23 Geri Dönüşüm Kutuları'nın ilk turunda nesneler sahnedeki kutuların içine bırakılıyor. Hedefli sahne düzeltmesi kaydı **25 oyuna** ulaştı; güncel otomatik sahne dışı hedef sinyali **59 oyun**. Her iki oyunun üç tur teknik regresyonu geçti. Ayrıntılar: docs/SAHNE_DUZELTMELERI_9_2026-09-23.md. Aşağıdaki önceki sayılar tarihsel kontrol noktalarıdır.

## Son ek: sekizinci paket

Y19/Y58 oyunlarının ilk iki turundaki parçalar doğrudan dergi ve dilekçe sayfalarına yerleşiyor. Hedefli sahne düzeltmesi kaydı **23 oyuna** ulaştı; güncel sahne dışı hedef sinyali **61 oyun**. Dilekçe sıralamasındaki yukarıdan aşağı yönergesiyle ters sıra çelişkisi giderildi. Ayrıntılar: docs/SAHNE_DUZELTMELERI_8_2026-09-23.md. Aşağıdaki eski sayılar önceki paketlerin tarihsel kayıtlarıdır.

## Son ek: yedinci paket

F25/F26'nın ilk turları gerçek mıknatıs deneyine dönüştürüldü. Hedefli sahne düzeltmesi kaydı **21 oyuna** ulaştı; güncel sahne dışı hedef sinyali **63 oyun**. Gözlem cevapları artık sürükleme hedefi sayılmıyor, gerçek mıknatıs hedefi ayrıca sayılıyor. Ayrıntılar: docs/SAHNE_DUZELTMELERI_7_2026-09-21.md. Aşağıdaki 19 oyun / 65 sinyal değerleri altıncı paket kontrol noktasının tarihsel kaydıdır.

## Gerçek durum

İstenen ilk üç iş katalog genelinde tamamlanmış değildir. Üç tur teknik çözüm testi tamamlandı; sahne, arayüz ve eylem-sonuç animasyonu kabulü oyun bazında devam ediyor.

- Önceki denetimle aynı 12 gruptaki **635 oyun / 1.905 tur**, teknik çözüm koşumundan geçti.
- Her turun başlangıcı doğru oyun kimliğiyle 390×844 ölçüsünde kaydedildi: **1.905 PNG**.
- Bu kayıtların yönerge kırpılması ve yatay kontrol taşması ölçümlerinde bayrak yok.
- **65 oyunda** en az bir sahne dışı hedef sinyali sürüyor. Bu otomatik DOM sinyali kesin hata veya kalan iş sayısı değildir. Örneğin dil etkinliklerinde metin hedefi uygun olabilir.
- **19 oyunda hedefli sahne düzeltmesi** yapıldı: önceki üç pakette 13, bu devam çalışmasında 6. Bazılarının yalnız sürükleme/sınıflama turları yenilendi.
- **635 oyunun tümü için tam tasarım kabulü açık.** Hiçbir oyun yalnız teknik test nedeniyle tasarım onayı almadı. 19 oyunun kapsamı ve kanıtı ayrıca kaydedildi.

## Bu devam çalışmasındaki altı oyun

| Oyun | Değişen turlar | Sahnedeki davranış |
|---|---|---|
| G07 Canlı Sınıflama Masası | 1, 2 | Çizilmiş canlı örnekleri ahşap koleksiyon çekmecelerine yerleşir, sınıflandırılan örnekler görünür kalır. |
| Z10 Sözcük Tasnifi | 1, 2 | Sözcük çiftleri kitap biçiminde ilgili rafa oturur; raf içeriği birikir. |
| H07 Alışkanlıklar Panosu | 1 | Resimli alışkanlık kartları pano kağıdına iğnelenir. |
| Y02 Erdem Kâşifi | 1, 2 | Davranış kanıtları erdem günlüğüne yazılır ve damgalanır. |
| Y12 Neden-Sonuç Köprüsü | 1 | Neden doğrudan sonuç sahnesine bırakılır; yağmur/birikinti, sınav sonucu, uyanma ve solma sahnede görülür. |
| P37 Açı Aralıkları | 1, 2, 3 | Açı ölçerin kolu yerleştirilen dereceye döner; açık aralıklar ve 360° dönüş izi gösterilir. Son turda aynı ölçere iki açı konabilir. |

Diğer tur türleri korundu; bütün altı oyunun baştan sona yeniden tasarlandığı iddia edilmiyor. Oyun kuralları ve doğru cevaplar değiştirilmedi. G07'de bitki açıklamalarındaki “arı” harflerinin yanlışlıkla arı çizimi seçmesine yol açan eşleşme daraltıldı.

## Ortak etkileşim düzeltmesi

Matematik 3/4, Türkçe 3/4, Fen 3/4 ve Hayat Bilgisi 2 içindeki eski sürükleme yardımcılarında, iptal edilen işaretçi olayının bırakma gibi kabul edilmesi giderildi. W05'in özel meyve paylaşma işleyicisinde de iptal, aktif sürükleme ve görsel temizliği ayrıldı.

verify-drag-cancel.cjs: W01, P21, Y02, P10, W05, Y07, Z18, G01, F01, H02. On örnekte iptal durum/can/tur verisini değiştirmedi ve iptal sonrasında normal sürükleme çalıştı. Bu, tüm oyunlarda her iptal olasılığının test edildiği anlamına gelmez.

## Doğrulama ve sınırları

- Yeni altı oyunun yenilenen turlarında **55 gerçek fare sürüklemesi**: G07 15, Z10 12, H07 6, Y02 8, Y12 4, P37 10.
- Yanlış hedef, sürükleme iptali, klavye seçimi, eylem animasyonu ve azaltılmış hareket tercihi ayrı kontrol edildi.
- Altı oyunun üçer tur başlangıcı 320×568, 390×844 ve 844×390 ölçülerinde taşma/kırpılma açısından test edildi.
- Son hedefli regresyon **24 oyun / 72 tur** geçti: P11, P16, P24, P37, P38, Y01, Y02, Y03, Y10, Y11, Y12, Y13, G07, Z10, H07, W01, W05, P21, P10, Y07, Z18, G01, F01, H02. P37'nin son yönerge/dönüş izi değişikliğinden sonra üç turu ayrıca tekrar geçti.
- Katalog koşumu bazı mekaniklerde programatik tıklama veya durum kurulumu kullanır; 635 oyunda gerçek dokunma/sürükleme testi değildir. Fen koşucuları mevcut çözüm yordamlarını kullanır.
- Yerel Chrome testleri fiziksel Android/iPhone/WebView testi değildir. Ses kalitesi, gerçek telefon klavyesi ve tüm animasyon süreleri ayrıca değerlendirilmeli.
- Görsel kanıt PNG'dir, video değildir. Hareket için galeri içindeki oyun bağlantısı kullanılmalıdır.
- Katalog kayıtları farklı test zamanlarından gelir. Son oyunlara yönelik regresyon, 635 oyunun tümünün son değişiklikten sonra yeniden koşulduğu anlamına gelmez.
- Yeni koşum kayıtlarına HTML ve bağlı yerel JS/CSS içeriğinin SHA-256 özeti eklendi. Daha eski kayıtlarda özet yok; geçmiş kayıtların HEAD alanı kaydedilmemiş çalışma ağacı değişikliklerini temsil etmez.

## Dosyalar ve yeniden çalıştırma

- artifacts/katalog-kabul-635/index.html: 635 oyunun üç tur galerisi ve filtrelenebilir durum listesi.
- artifacts/katalog-kabul-635/results.json: teknik çözüm kayıtları.
- artifacts/katalog-kabul-635/acceptance-ledger.json: her oyun için ayrı teknik/tasarım/sinyal kaydı.
- docs/OYUN_SAHNE_KANITLARI.json: 19 oyundaki hedefli düzeltmelerin kalıcı kapsam listesi.
- artifacts/sahne-duzeltmeleri-4-2026-09-21/index.html: G07, Z10, H07 önce/sonra.
- artifacts/sahne-duzeltmeleri-5-2026-09-21/index.html: Y02, Y12 önce/sonra.
- artifacts/sahne-duzeltmeleri-6-2026-09-21/index.html: P37 önce/sonra.
- tools/catalog-acceptance.cjs: tam koşum; kimlik verilirse yalnız o oyunlar. --resume mevcut kayıtları (başarısızlar dahil) atlar; başarısızları yeniden denemek için kimlik verilmeli. --report-only tarayıcı açmadan raporu yeniler.
- tools/verify-scene-collections.cjs, tools/verify-scene-stories.cjs, tools/verify-scene-ranges.cjs: yeni sahnelerin işaretçi ve görünüm kanıtlarını yeniden üretir.
- tools/verify-drag-cancel.cjs: ortak iptal regresyonu.

## Kalan iş

1. 635 oyunun açık tasarım kayıtlarını oyun oyun incelemek; gerçek hedef/nesne bağlantısını, anlamlı sonucu ve uygun animasyonu eksik olduğu yerde tamamlamak.
2. Önce sahne dışı hedef sinyali veren oyunları elle değerlendirmek. Sinyalsiz olmak kabul değildir; diğer oyunlar da ayrıca incelenmeli.
3. Üç tur teknik testine ek olarak tüm farklı mekaniklerde gerçek giriş, son tur geçişi, yanlış işlem, tekrar başlatma ve küçük ekran davranışını doğrulamak.
4. Kullanıcı görsel onayı ve gerçek cihaz/WebView testinden önce katalog genelinde “bitti” dememek.

H31–H36, Hayat Bilgisi 3 ve Sosyal Bilgiler 4 bu 635 oyunluk denetimin kapsamı dışında kalır.
