# Önceki oyun paketleri: arayüz, animasyon ve etkileşim denetimi

Tarih: 21 Eylül 2026 · İncelenen sürüm: `a0f9c19`

## Sonuç

Önceki paketlerin tümünü “oyuna özel arayüz ve anlamlı animasyonları tamamlandı” diye nitelemek doğru değil. İlk matematik paketinde belirgin sahne ve animasyon tasarımı var; sonraki paketlerde yapılan işin önemli bir kısmı ortak etkileşim koduna sürükleme eklemek. Bazı sahneler eyleme göre değişiyor; bazıları dekor olarak kalıyor. Her oyun için tasarım kabulü yeniden gerekli.

Bu denetimde oyun kaynakları veya uygulama kopyaları değiştirilmedi. Bulgular giderilmiş sayılmıyor.

## Kapsam ve kanıt sınırı

- Önceki paket/galeri listelerindeki **635 oyun**, **12 ders grubu**.
- Her oyunun üç turunun başlangıcı ayrı ayrı oluşturuldu: **1.905 başlangıç görünümü**. Tur indeksini değiştirerek görünüm incelendi; bu işlem turu oynayıp bitirmek değildir.
- Her oyunun ilk turu 390 × 844 ölçüsünde yeniden görüntülendi: **635 PNG**. URL’de hem sorgu hem hash oyun kimliği içeriyor; okunan `GAME_ID` istenen kimlikle doğrulandı. Her oyun ayrı sayfada açıldı.
- Her gruptaki farklı ilk-tur mekaniklerinden seçilmiş **120 ekran**, 12 paftada görsel olarak incelendi. 635 görüntünün tamamı tek tek elle değerlendirilmiş değildir.
- M37, V02, P15, Z04, F03 ve H12’de gerçek fareyle sürükleme yapıldı; önce–sonra ekranları ve durum değişimi kaydedildi.
- Z09’un üçüncü turundaki konuşma düğmesi gerçek 1,4 saniye basma/bırakma ile kontrol edildi; bu örnekte süre bırakıldığında durdu. Kaynaktaki yeniden çizim şüphesi bu denemede hata olarak doğrulanmadı.
- Kaynaklar `3258e70` kontrol noktasıyla karşılaştırıldı. CSS animasyon adı sayısı yalnız yardımcı kanıttır; JavaScript, SVG ve geçişleri kapsayan bir kalite puanı değildir.
- Bu kapsam tüm uygulama kataloğu değildir. H31–H36, 3. sınıf Hayat Bilgisi ve 4. sınıf Sosyal Bilgiler gibi henüz bu yenileme paketlerinde sunulmayan gruplar kapsam dışında.
- Gerçek telefon/WebView, tüm etkileşimler, ses kalitesi ve tüm animasyon süreleri bu çalışmada baştan sona test edilmedi.

## Paket bazında otomatik tarama

“Ortak kutu” yalnız belirli ortak şablon seçicilerini sayar; bütün sorunlu tasarımların sayısı değildir. Dil oyununda sözcük/cümle kartı kullanımı pedagojik olarak uygun olabilir. “Sahne dışı” DOM yerleşimidir; tek başına hata kararı değildir. Sütunlar örtüşür, toplanamaz. Sıfır değer tasarım onayı anlamına gelmez.

| Paket | Oyun | Ortak kart/kutu hedefi sinyali | Sahne dışı hedef sinyali | Yönerge kırpılan oyun |
|---|---:|---:|---:|---:|
| Sayma–Rakam | 20 | 0 | 0 | 0 |
| Matematik 1 | 61 | 0 | 0 | 16 |
| Türkçe 1 | 64 | 0 | 0 | 0 |
| Matematik 2 | 42 | 0 | 0 | 34 |
| Türkçe 2 | 90 | 74 | 0 | 0 |
| Matematik 3 | 48 | 1 | 0 | 1 |
| Türkçe 3 | 64 | 0 | 14 | 18 |
| Matematik 4 | 56 | 0 | 6 | 12 |
| Türkçe 4 | 64 | 30 | 18 | 0 |
| Fen 3 | 48 | 28 | 21 | 0 |
| Fen 4 | 48 | 19 | 10 | 0 |
| Hayat Bilgisi 2 H01–H30 | 30 | 15 | 8 | 0 |
| **Toplam kapsam / sinyal** | **635** | **167** | **77** | **81** |

Başlangıç taramasında sayfa JavaScript hatası kaydedilmedi. Bu, oynanış veya tasarım kabulü değildir.

## Doğrulanan örnekler ve yapılması gerekenler

### 1. P24 — Eşitlik Terazisi: kefe yerine metin paneli

Ekranda gerçek terazi kolu/kefesi yerine iki panel ve eşittir işareti var. Sağ panel “SAĞ KEFE kartları buraya sürükle” diyor. Alt açıklama bunu “gerçek sağ kefe” diye tanımlıyor. Kullanıcının daha önce reddettiği etiket-hedef düzeni hâlâ mevcut.

Gerekli değişiklik: işlemler ağırlık temsili olarak gerçek kefeye yerleşmeli; denge sahnede görülmeli. Sayı/işlem kartının bulunması sorun değil, hedefin ve sonucunun terazi davranışını göstermemesi sorun.

Kanıt: `artifacts/tasarim-denetimi-2026-09-21/screens/matematik4-p24.png`.

### 2. P15 — Çokluk Ölçeri: nesne yerine işlem kartı

“Bir kasa al (6 elma)” kartı alttaki tepsi kutusuna sürükleniyor. Sonuçta bu kart tepside metin olarak görünüyor. Yukarıdaki kasa seçimi ve toplam güncelleniyor; dolayısıyla sahne bütünüyle tepkisiz değil. Ancak çocuk görünen kasayı tutup taşımıyor.

Gerekli değişiklik: yukarıdaki kasa doğrudan tutulmalı, seçilen kasalar hedefe taşınmalı ve içindeki nesneler korunmalı.

Kanıt: `etkilesimler/matematik4-p15-once.png` ve `matematik4-p15-sonra.png`.

### 3. Z04 — Kurallı Cümle Makinesi: makine dekor olarak kalıyor

Doğru ilk sözcük sürüklendiğinde aşağıdaki ortak sıra kutusuna ekleniyor. Makine SVG’si değişmiyor; bırakma anından 150 ms sonraki örneklemede aktif animasyon yok. Bu tek örneklem başka zamanlarda animasyon olmadığını kanıtlamaz; ancak test edilen adım makine üzerinde görünür bir işlem oluşturmuyor.

Gerekli değişiklik: sözcükler makinenin gerçek bandına/kağıdına yerleşmeli; bandın veya baskı mekanizmasının hareketi kurulan cümleyi göstermeli. Türkçe dersinde anlamlı metin kartları korunabilir.

Kaynak: `web/phaser/turkce4-pdf-phaser.html`, `siraCiz` (390. satır).
Kanıt: `etkilesimler/turkce4-z04-once.png` ve `turkce4-z04-sonra.png`.

### 4. F03 — Araştırma Adımları: sahne güncelleniyor, hedef ayrı

Sürükleme sonrasında araştırma defterinde ilk adım yazılıyor; bu olumlu bir sahne geri bildirimi. Ancak bırakma alanı defterin dışında ikinci bir kesikli kutu. Aynı içerik defter, hedef kutusu ve alttaki kartta tekrar ediyor.

Gerekli değişiklik: kart doğrudan defterin sayfasına bırakılmalı; yazılma/yerleşme orada gösterilmeli.

Kaynak: `web/phaser/fen4-pdf-phaser.html`, `siraCiz` ve `[data-sira-hedef]` (785. satır).
Kanıt: `etkilesimler/fen4-f03-once.png` ve `fen4-f03-sonra.png`.

### 5. H12 — Afet Çantası: görsel çanta ve bırakma alanı farklı

Su şişesi yazılı düğme olarak taşınıyor. Resimdeki çanta değişmiyor; altında ayrı kutuya “Su şişesi” etiketi ekleniyor. Doluluk çubuğu ilerliyor. Bu, şişeyi gerçek çantaya koyma deneyimini karşılamıyor.

Kaynak: `web/phaser/hayatbilgisi2-pdf-phaser.html`, `cantaCiz` (678. satır).
Kanıt: `etkilesimler/hayatbilgisi2-h12-once.png` ve `hayatbilgisi2-h12-sonra.png`.

### 6. M37 ve V02: korunabilecek etkileşim, ayrı görsel kalite ihtiyacı

M37’de bilye gerçekten kefe hedefinde görünüyor; terazi eğim değeri ilk bilyede −10,0 dereceden −8,8 dereceye, kefe yükseklikleri ±21 pikselden ±18,4 piksele değişti. V02’de onluk çubuk kırmızı vagon hedefinde yerleşti. Bu örneklerde hedef bağlantısı metin paneline göre daha doğru. V02’nin küçük, ekranın ortasında kalan sahnesi ve yerleşim hareketi ayrıca geliştirilmelidir. Bu iki örneğe kapsamlı animasyon/tasarım onayı verilmedi.

Kanıt: `etkilesimler/matematik-m37-*`, `etkilesimler/matematik2-v02-*`, `etkilesimler/probes.json`.

## Telefon yönergeleri: 81 oyun / 124 tur

Tarama, `.prompt` elemanlarında `overflow:hidden` ile gerçek metin yüksekliğinin kutuyu aşmasını buldu. Diğer kontrol sınıflarında bu ölçüte göre kırpılma kaydedilmedi. M05 ilk tur görüntüsünde yönergenin sonundaki “sürükle” sözcüğünün kaybolduğu görsel olarak da doğrulandı. Diğer 80 oyundaki kayıtlar DOM ölçümüdür.

- Matematik 1: M05, M07, M09, M20, M33, M37, M39, M40, M43, M51, M52, M53, M55, M57, M58, M59.
- Matematik 2: V01, V02, V05, V06, V07, V08, V10, V12, V13, V14, V17, V19, V20, V21, V22, V23, V24, V25, V26, V27, V28, V29, V30, V32, V33, V34, V35, V36, V37, V38, V39, V40, V41, V42.
- Matematik 3: W03.
- Türkçe 3: Y02, Y05, Y06, Y09, Y11, Y12, Y13, Y17, Y22, Y25, Y26, Y33, Y34, Y37, Y39, Y49, Y62, Y64.
- Matematik 4: P03, P07, P08, P18, P19, P26, P31, P43, P44, P50, P51, P55.

Gerekli değişiklik: yönerge yüksekliği içeriğe göre büyümeli; boş sahne alanı yeniden dengelenmeli. Yalnız yazıyı küçültmek uygun çözüm değil. Klavye açıkken ve küçük yatay ekranlarda ayrıca doğrulama gerekli.

## Kaynak geçmişindeki kapsam farkı

Sayma–Rakamın 20 oyunu önceki 257 ekranlık pakette bulunuyor, fakat `sayma-pdf-phaser.html` dosyası `3258e70` ile bugünkü sürüm arasında aynı. Bu aralıkta bu oyunlara yeni tasarım yapılmış sayılamaz; daha eski çalışmaları hakkında bu karşılaştırma hüküm vermez.

Matematik 1’de bu aralıkta oyuna özgü yeni CSS animasyonları ve sahne yapıları var. Diğer 11 grupta yeni CSS keyframe adı yok; bazı gruplarda JS ile sahne güncellemesi ve önceki animasyonlar bulunuyor. “Yeni keyframe yok” sonucu “hiç animasyon yok” şeklinde yorumlanmamalı.

## Düzeltme sırası ve kabul ölçütü

1. Yönergeleri kırpılan 81 oyunun ortak mobil başlık düzenini düzeltmek.
2. P24, P15, H12, F03 ve Z04’ü gerçek hedef ve sonuç animasyonuyla örnek düzeltme paketi yapmak.
3. Sonra aynı sorunu paylaşan oyunları `audit.json` içindeki kimlik/tur kayıtlarından tarayarak paket paket düzeltmek. Tema adı/renk değiştirmek yeterli sayılmamalı.
4. Her oyun için ayrı kayıt: arayüz, hedefle nesne örtüşmesi, eylem-sonuç animasyonu, mobil yerleşim, üç tur oynanış. Birinin geçmesi diğerlerine onay sayılmamalı.

## Dosyalar

- Galeri: `artifacts/tasarim-denetimi-2026-09-21/index.html`
- Ayrıntılı oyun/tur envanteri: `artifacts/tasarim-denetimi-2026-09-21/audit.json`
- 635 ilk-tur ekranı: aynı dizinde `screens/`
- Gerçek etkileşim ölçümleri ve önce–sonra görüntüleri: `etkilesimler/`
- Tekrar üretilebilir araçlar: `tools/audit-game-design.cjs`, `tools/audit-game-design-interactions.cjs`

İlk deneme aracındaki yalnız hash ile gezinme ve tarayıcı sayfasını uzun süre tekrar kullanma sorunları giderildi; bu rapor son, oyun kimliği doğrulamalı ve her oyun için ayrı sayfa kullanan başarılı koşumun `audit.json` verisine dayanır. Video bağımlılığı kurulmadı; kanıtlar PNG ve JSON olarak tutuldu.
