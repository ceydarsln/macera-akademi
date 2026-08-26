# 4. Sınıf Matematik PDF Düzeltme Takibi

Kaynak: `output/pdf/4_sinif_matematik_oyunlari_detayli_duzeltmeler.pdf` (67 sayfa, p01–p56).
Şartnamenin yapılandırılmış hâli: `tmp/spec4.json` (PDF üretici betiğinden `tmp/pdfs/extract_math4_spec.py` ile çıkarıldı).
Motor: `web/phaser/matematik4-pdf-phaser.html` (matematik3 çerçevesi + 4. sınıfa özel oynatıcılar).
Katalog bağlantısı: `web/macera-akademi.html` içindeki `PHASER_OYUNLAR` haritasında p01–p56 → `matematik4-pdf`.

**Durum: 56/56 oyun uygulandı** (son güncelleme: 26 Ağustos 2026).

"Uygulamada" işareti yalnız şu koşullar birlikte sağlanınca verilir:

1. Üç tur farklı veriyle baştan sona oynanır (`tools/dom_kosum.html` koşumunda doğrulanır).
2. Sahne cevabı ele vermez: hazır model, sayı, çözüm cümlesi ya da etiket kopyalanamaz.
3. Çocuk gerçek bir karar verir (hangi basamak, hangi kutu, hangi araç, hangi rota).
4. Yanlışta doğruyu söylemeyen, nedeni model üzerinde gösteren geri bildirim gelir.
5. 375×812 telefon ekranında kart tam görünür, hedef alanı ilk ekranda erişilebilir.

## Şartnamenin ortak standardı — motor düzeyinde uygulananlar

- [x] Hareketli kart / düşen kapsül / süre baskısı mekanikleri kaldırıldı; kart karar verilene kadar merkezde ve tam görünür (`renderSerit`).
- [x] Kırpılan bant kartı sorunu bitti: bant duraklı, kart `max-width` ile ortalanıyor.
- [x] Roket-yakıt, tren-tünel ve kronometre ortak motorları sıralama/yuvarlama/ölçme oyunlarından çıkarıldı; yerine sabit yuvalı kule, gerçek sayı doğrusu ve gerçek ölçme araçları kondu.
- [x] Cevabı başlangıçta veren ipuçları kaldırıldı (p01 bölük açıklaması, p10 sipariş çözümü, p19 yuvarlanmış işlem, p26/p39 açılış sesi, p23 hazır çözüm kartı).
- [x] Her oyunda üç değişen tur; bitiş yalnız üçüncü doğru turdan sonra.
- [x] Yanlışta yalnız bir can eksilir, "tekrar dene" okunur; tahmin turlarında `noPenalty` ile can eksilmez.
- [x] Ortak "son soru" adımı (`bitirTur` + `sonSoru`): eylem tamamlandıktan sonra kavramsal doğrulama sorusu geliyor; başarı ondan sonra veriliyor.
- [x] Dokunma hedefleri en az 44 px; `↶ geri al`, `🧽 silgi`, `🧹 tümünü temizle` gerekli oyunlarda mevcut.
- [x] Web kaynağı tek kanonik kaynak; `tools/aynala.sh` ile APK varlığına aynı içerik kopyalanıyor.

## Yayımdan önce zorunlu içerik düzeltmeleri (PDF'in 4. bulgusu)

| Sorun | Nerede | Uygulanan |
|---|---|---|
| "Her adım 10 ya da 1000 kat" ifadesi 1 m = 100 cm geçişini dışlıyordu | p16 | Uzunluk ve kütle merdivenleri ayrıldı; her ok kendi çarpanını taşıyor (×10, ×100, ×1000). |
| Bütün "olabilir" olaylar 5/10'a sabitleniyordu | p50 | Ölçek üç geniş bölgeye çevrildi; sayısal olasılık puanı verilmiyor, tolerans bölge genişliği kadar. |
| 5/2 oranı kesin soruda 2 kabul ediliyordu (doğrusu 2,5) | p56 | Kat sorusu tam kat veren veriyle değiştirildi: 6 ÷ 2 = 3. |
| "Bir taş suya atılınca batacak" koşulsuz kesin sayılıyordu | p50 | Taş örneği çıkarıldı; yerine içeriği görünen torba deneyleri kondu. |

## Tema 1 — Sayılar ve Nicelikler (1)

| ID | Oyun | Uygulanan ana düzeltme | Durum |
|---|---|---|---|
| p01 | Sayı Sarayı Kasası | "Binler bölüğü 245, birler bölüğü 612" açıklaması kaldırıldı. Yalnız okunuş veriliyor; çocuk altı pencereyi tek tek kuruyor, sıfırlı basamakları kendisi dolduruyor. Yanlışta yalnız ilgili basamak çerçeveleniyor. | Uygulamada |
| p02 | Bölük Ayırma Bandı | Bant duraklı; kart ortada ve tam görünür. Her turda yeni altı basamaklı sayı; 3. turda çocuk sayıyı kendisi üçlü gruplara ayırıyor. | Uygulamada |
| p03 | Basamak Değeri Köprüsü | Altı basamağın hepsi ayrı kart; birler basamağındaki 2 de kullanılıyor. Sıfır değerli basamaklar (0 × 10.000 = 0) açıkça yer alıyor. | Uygulamada |
| p04 | Sıralama Kulesi | Roket/yakıt görseli gitti; kartlar hareket etmiyor. Sabit yuvalı kule, yanlış komşulukta ilk farklı basamağı gösteren karşılaştırma, 3. turda ara kart ekleme. | Uygulamada |
| p05 | Yuvarlama Treni | Ray gerçek sayı doğrusu; komşulara uzaklıklar ölçekli çiziliyor ve sayılıyor. Sürgü her turda tarafsız konumda başlıyor; 6500 yarım durumu ayrı ele alınıyor. | Uygulamada |
| p06 | Gökdelen Asansörü | Yaprak/rota motoru gitti; dikey kuyuda kat yalnız doğru seçimden sonra iz bırakıyor. Yüzer/biner, ileri/geri dört görev de ayrı ayrı tamamlanıyor. | Uygulamada |
| p07 | Örüntü Radarı | Kapsüller sabit. Çocuk önce kural kartını, sonra eksik terimi seçmeden başarı alamıyor; 3. turda çarpımsal ve toplamsal örüntü karşılaştırılıyor. | Uygulamada |
| p08 | Okunuş Eşleştirme | İlk tur açık iki sütun (kırpılma yok); kapalı kart yalnız 2. turda ve az sayıda. 3. tur dinleme turu. | Uygulamada |

## Tema 2 — Sayılar ve Nicelikler (2)

| ID | Oyun | Uygulanan ana düzeltme | Durum |
|---|---|---|---|
| p09 | Kesir Tasnif Bandı | Her kartın yanında kesir şeridi/daire modeli var; sınıflama sembolden değil "kaç bütün doldu" sorusundan yapılıyor. 2 tam 1/4 ile 9/4 aynı miktar olarak bağlanıyor. | Uygulamada |
| p10 | Pastane Siparişi | Fişte yalnız sembol var; çözüm cümlesi gizli. Parçalar tepside kalıyor, tek tek geri alınabiliyor; 7/4 iki farklı sunumla karşılaştırılıyor. | Uygulamada |
| p11 | Denk Kesir Köprüsü | Süs emojileri kaldırıldı; her kart kesir şeridi. ×2, ×3 genişletme ve sadeleştirme ayrı turlarda. | Uygulamada |
| p12 | Birim Kesir Kulesi | Roket sahnesi gitti; aynı boydaki bütünler 2-3-4-6-8-10-12 parçaya bölünmüş şeritlerle gösteriliyor. 3. turda etiketsiz model adlandırılıyor. | Uygulamada |
| p13 | En Büyük Kesir Radarı | Düşen kapsül yok; dört kesir aynı anda sabit ve modelli. Görev yönü başlıkta sabit; 3. turda 2/3 ile 3/4 ortak 12'lik şeritlerde karşılaştırılıyor. | Uygulamada |
| p14 | Kesir Hesap Makinesi | "2 + 3 = ?" ara işlemi kaldırıldı. Payda ayrı adımda soruluyor, pay modelden sayılıyor; 3. turda bileşik kesir tam sayılıya çevriliyor. | Uygulamada |
| p15 | Çokluk Ölçeri | Tren/tünel gitti; sepet ve nesneler görünür, eş kasalar kuruluyor. 3. tur ters problem (bir grup → bütün). | Uygulamada |
| p16 | Birim Dönüşüm Kartları | Uzunluk ve kütle ayrı merdiven; her ok kendi çarpanını taşıyor. Açık sütun eşleştirme önce, hafıza turu sonra. | Uygulamada |

## Tema 3 — İşlemlerden Cebirsel Düşünmeye

| ID | Oyun | Uygulanan ana düzeltme | Durum |
|---|---|---|---|
| p17 | Zihin Radarı | Hareketli kapsüller gitti; masa sabit. Ara işlem yalnız çocuk parçaları yerleştirdikçe not defterinde oluşuyor; telafi stratejisi ayrı tur. | Uygulamada |
| p18 | Dört Basamak Kasası | Yalnız son sonuç yerine her sütun sırayla giriliyor; elde ve onluk bozma ayrı adımlarda soruluyor. Sıfırlı çıkarmada bozma zinciri binlikten birliğe izleniyor. | Uygulamada |
| p19 | Tahmin Terazisi | Tren sürgüsü ve hazır "50×20" metni gitti. Çocuk önce yuvarlıyor, tahminini kaydediyor, gerçek sonucu sonra buluyor ve farkı yorumluyor. Bölmede "bölünebilir dost sayı" ayrıca ele alınıyor. | Uygulamada |
| p20 | Kısa Yol Bandı | "Sıfır ekle/sil" tek kural olmaktan çıktı; basamak tablosunda kayma gösteriliyor ve basamak değerinin nasıl değiştiği ayrı adımda yazdırılıyor. | Uygulamada |
| p21 | Robot Paketleme Bandı | 42 dokunuş yerine 7'li paket kartları (en fazla 6 anlamlı dokunuş). Aynı dizi üzerinde çarpma ve iki ters bölme kuruluyor; her turda farklı bilinmeyen. | Uygulamada |
| p22 | Yönerge Labirenti | Yaprak kapılar gitti; ara sonuçlar not defterinde kalıyor, yanlış yalnız o adıma dönüyor. 2. tur eksik komut, 3. tur çocuğun kurduğu zincir. | Uygulamada |
| p23 | Problem Kurma Masası | Hazır "(5×12)−8" çözüm kartı başlangıçta yok. Çocuk cümle şeridini kuruyor; işlem en sonda seçiliyor. 3. turda gereksiz bilgi ayrılıp yeni problem kuruluyor. | Uygulamada |
| p24 | Eşitlik Terazisi | Tek dokunuşla denge kurma gitti; birden fazla doğru eşitlik kabul ediliyor. Eşitliğe aynı sayıyı ekleme dönüşümü ve bilinmeyen kutulu eşitlikler eklendi. | Uygulamada |

## Tema 4 — Nesnelerin Geometrisi (1)

| ID | Oyun | Uygulanan ana düzeltme | Durum |
|---|---|---|---|
| p25 | Açınım Ayırma Bandı | "6 dikdörtgen yüz" etiketi kaldırıldı; kart ortada ölçekli açınım çizimi. Kapanmayan çeldirici ağ eklendi. | Uygulamada |
| p26 | Küp Tarayıcısı | Açılış sesi sonucu söylemiyor; sayaç toplamı gizli. Her dokunuş numaralanıyor, tekrar dokunma ikinci kez saymıyor. Köşe-ayrıt-yüz üç ayrı tur. | Uygulamada |
| p27 | Üçgen Çeşitleri Bandı | Üçgen merkezde büyük; cetvel şeridi var. Çocuk üç kenarı da ölçmeden sınıf sorulmuyor; 3. turda döndürülmüş üçgenle sınıfın değişmediği görülüyor. | Uygulamada |
| p28 | Köşe-Kenar Stüdyosu | Açılış sesi sonucu söylemiyor. Şekil kapandıktan sonra köşe/kenar sayısı soruluyor; köşegenin kenar olmadığı ayrıca açıklanıyor. | Uygulamada |
| p29 | Çevre Hesap Makinesi | "7 × 4" ipucu kaldırıldı. Şekil ölçekli çiziliyor, çocuk dış sınırı kenar kenar dolaşıyor; formül tur sonunda genelleme olarak açılıyor. Ters çevre problemi eklendi. | Uygulamada |
| p30 | İp Dolama Deneyi | Kronometre kadranı ve zamanlama toleransı gitti. İp gerçekten yay yay sarılıyor, cetvelde okunuyor; iki farklı çaplı kutu karşılaştırılıyor. | Uygulamada |
| p31 | Alan Tahmin Ölçeri | Tren gitti; ızgara önce yarı saydam. Tahmin kaydedilmeden sayım açılmıyor ve tahmin turunda can eksilmiyor. Standart olmayan birimler gerçek oranla döşeniyor. | Uygulamada |
| p32 | Ölçme Aracı Deposu | Tek etiket seçimi yerine üç adımlı akış: nicelik → araç → ölçüm adımı. Eğri çevrede ip + cetvel sırası kuruluyor. | Uygulamada |

## Tema 5 — Nesnelerin Geometrisi (2): açılar

| ID | Oyun | Uygulanan ana düzeltme | Durum |
|---|---|---|---|
| p33 | Açı Avcısı Radarı | Düşen metin kapsülleri gitti; nesneler büyük ve sabit. Çocuk köşeyi ve iki kolu işaretliyor; kol uzunluğunun açıyı değiştirmediği gösteriliyor. | Uygulamada |
| p34 | Açı Döndürücü | Kronometre kadranı ve hazır hedef sayısı gitti. Sabit ışın + sürüklenen ikinci ışın, derece yayı, isteğe bağlı açıölçer. | Uygulamada |
| p35 | Açı Tasnif Bandı | Açı merkezde büyük; kâğıt köşesi referansı her kartta. Önce "dik açıdan küçük/eşit/büyük", sonra tür adı. 89-90-91 sınır turu eklendi. | Uygulamada |
| p36 | Kâğıt Köşesi Deneyi | Tren sürgüsü gitti; gerçek kâğıt köşesi şablonu ardışık yerleştiriliyor. Elle katlanan yarım köşenin belirsizliği ve açıölçer standardı karşılaştırılıyor. | Uygulamada |
| p37 | Açı Özellik Köprüsü | Simge ikonlar yerine gerçek açı çizimi ve derece yayı; hedefler açık sayı aralıklarıyla. 3. turda aynı hedefe birden çok açı geliyor. | Uygulamada |
| p38 | Açı Kartları | İlk tur açık kartlar; kapalı hafıza turu sonra. Nesne kartlarında gerçek açı çizimi var; 3. turda çocuk kendi örneğini seçiyor. | Uygulamada |
| p39 | Açı Çizim Stüdyosu | Kırpılan etiketler ve erken başarı sesi gitti. İlk ışın sabit, ikincisi serbest; tür adıyla, dereceyle ve adlandırmayla üç ayrı görev. | Uygulamada |
| p40 | Derece Hesap Makinesi | "90+90", "90÷2", "4×90" ipuçları kaldırıldı. Dik açı parçaları çiziliyor; çocuk parçaları birleştirip bölerek dereceyi modelden çıkarıyor. | Uygulamada |

## Tema 6 — Nesnelerin Geometrisi (3): simetri ve kodlama

| ID | Oyun | Uygulanan ana düzeltme | Durum |
|---|---|---|---|
| p41 | Ayna Odası | "Aynadaki gibi ters çevrilmiş" etiketi kaldırıldı; üç seçenek de gerçek şekil ön izlemesi (doğru yansıma, çevrilmemiş, ölçeği bozuk). Dikey, yatay ve eğik eksen ayrı turlarda. | Uygulamada |
| p42 | Simetri Denetim Bandı | Harfler sistem fontu değil vektör çizim; denetlenen eksen kartın üzerinde sürekli çizili. Harflerin yanına kelebek/vazo motifleri eklendi; 3. turda eksen yönünün kararı değiştirdiği gösteriliyor. | Uygulamada |
| p43 | Simetri Dokuma Tezgâhı | Silgi, geri al ve tümünü temizle eklendi; kalan eş nokta sayacı var. 2. tur yatay eksen, 3. tur hatalı hücreleri düzeltme. | Uygulamada |
| p44 | Mozaik Ustası | Kaynak hücreler kilitli; palet ve yönerge kaydırmasız. 3. turda dikey, yatay ve çapraz eşteki üç hata bulunup düzeltiliyor. | Uygulamada |
| p45 | Simetri Doğrusu Çizimi | Açılış sesi sayıyı ve çizgi türünü söylemiyor. Her çizgi katlama testine giriyor; dikdörtgende köşegenin neden reddedildiği, dairede sayısızlık gösteriliyor. | Uygulamada |
| p46 | Kodlama Mimarı | Robotun geçtiği hücreler artık bir plan oluşturuyor; çalışırken aktif blok parlıyor. Birden çok geçerli rota kabul edilip adım sayıları karşılaştırılıyor; 3. turda dikdörtgenin dış sınırı kodlanıyor. | Uygulamada |
| p47 | Simetri Sayısı Köprüsü | Hazır sayı çiftleri gitti; çocuk önce doğruları çizip katlama testinden geçiriyor, sayı ondan sonra soruluyor. Çeşitkenar üçgen (0) çeldiricisi eklendi. | Uygulamada |
| p48 | Simetri Adımları | Roket kaldırıldı; kartlar sabit iş akışı şeridinde sıralanıyor ve her adım örnek şekilde uygulanıyor. 2. tur eksik adım, 3. tur yanlış sıralamanın teşhisi. | Uygulamada |

## Tema 7 — Olasılık ve Veriye Dayalı Araştırma

| ID | Oyun | Uygulanan ana düzeltme | Durum |
|---|---|---|---|
| p49 | Olasılık Bandı | Koşulsuz günlük cümleler çıkarıldı; her kartta deneyin koşulu (zarın yüzleri, torbanın içeriği) yazılı. Mümkün sonuçlar kümesi önce gösteriliyor, sınıf sonra seçiliyor. | Uygulamada |
| p50 | Olasılık Ölçeği | Tren gitti; ölçek üç geniş bölge. "Olabilir" olaylara 5/10 gibi sayısal değer verilmiyor; torba içeriği görünür ve içerik değişince olay yeniden sınıflanıyor. | Uygulamada |
| p51 | Araştırma Planı Masası | "İlk iki adım" gibi hazır seçtirme gitti. Çocuk hedef grubu, değişkeni ve soruyu kartlardan kuruyor; süreç kartları en sonda özet olarak sıralanıyor. Tek cevaplı bilgi sorusunun neden dağılım üretmediği ayrıca soruluyor. | Uygulamada |
| p52 | Veri Toplama Çetelesi | Yanıtlar kategori sözcüğünü doğrudan içermiyor; kategori seçimi anlamdan çıkarılıyor. Her adımda işlenen yanıt sayısı ile çetele toplamı karşılaştırılıyor, geri al var. | Uygulamada |
| p53 | Grafik Fabrikası | Sıklık üstte hazır yazmıyor; kaynak standart çetele. Bütün bloklar aynı biçim, eksen 0'dan 1'er artıyor ve "1 blok = 1 kişi" anahtarı yazılı. 3. turda hatalı grafik düzeltiliyor. | Uygulamada |
| p54 | Veri Terazisi | Kaynak sütun grafiği üstte sürekli görünür; "3/5" kesir görünümlü etiket yerine "… sütunu / … kişi" yazılıyor. Toplam görevi terazi yerine ayrı toplam panelinde. | Uygulamada |
| p55 | Sonuç Değerlendirme | Yönergedeki düğme adı ekrandakiyle aynı. Çetele grafiğe dönüşüyor; en az iki doğru yorum seçiliyor ve "bütün okul futbolu sever" iddiasının neden çıkarılamayacağı örneklem sınırıyla açıklanıyor. | Uygulamada |
| p56 | Grafik Hesap Makinesi | Sayı listesi yerine gerçek sütun grafiği ve "1 blok = 1 kişi" anahtarı. **Kat sorusu 6 ÷ 2 = 3 verisiyle değiştirildi** (eski 5/2 = 2 kabulü hatalıydı). | Uygulamada |

## Doğrulama

1. **Tam koşum:** `tools/dom_kosum.html#ids=p01,…,p56` — 56 oyun × 3 tur, tamamı geçiyor.
   Çözücü `tur5()` içinde; motor dosyası eşlemesi `motorDosyasi()` içindeki `'p'` dalında.
2. **Kenar durum taraması:** `tmp/m4_kenar.html` — her mekaniğe özgü hatalı kullanım denemesi
   (boş giriş, aşırı uzun giriş, sıra dışı adım, yanlış hedef, aynı ögeye iki kez dokunma,
   geri al / silgi / tümünü temizle, hızlı art arda tıklama). 56/56 oyunda JS hatası yok,
   tur kilitlenmesi yok.
3. **Tarayıcıda elle oynama:** uygulama kabuğundan (misafir girişi → 4. sınıf → Matematik)
   p01, p02, p27 ve p43 gerçek fare tıklamalarıyla baştan sona oynandı; yanlış cevap, can
   kaybı, üç canın bitmesi, tur geçişi ve bitiş ekranı (puan/XP/altın) doğrulandı.
4. **Ölçüm:** 375×812'de 56 oyunun hiçbirinde yatay taşma ya da ekran dışına çıkan öge yok.

### Canlı testte bulunup düzeltilenler

| Bulgu | Düzeltme |
|---|---|
| CSS sınıf adları devralınan 3. sınıf stilleriyle çakışıyordu (`.lab`, `.tick`, `.numline`, `.pv-cell`, `.scale`, `.tray`, `.board`, `.pan`, `.program`, `.pv-table`); sayı doğrusu etiketleri kutu içinde ve kırpılmış çiziliyordu | Bütün 4. sınıf sınıf adları `m4-` ön ekiyle ayrıldı |
| Sahne kutusu esneyip içeriği kırpıyordu | `.stage{flex-shrink:0}` |
| Yönergedeki `:` işareti "bölü", `-` işareti "eksi" diye okunuyordu ("ölç bölü her kenara") | `speech()` artık işareti yalnız **iki sayı arasında** sözcüğe çeviriyor; `°` "derece" okunuyor |
| Tilki konuşma balonu okunan metni gösterdiği için `:` yerine konan virgül balonda görünüyordu | `:` sözcüğe değil boşluğa çevriliyor |
| İp Dolama'da (p30) ilk yay dışında bir yerden başlayan çocuk turu bitiremiyordu | Sarmaya herhangi bir yaydan başlanabilir; sonraki yayın **komşu** olması yeterli |
| Küp Tarayıcısı'nda sayaç "0 / 8" yazarak cevabı önceden veriyordu | `gizliToplam` ile p26'nın üç turunda toplam gizlendi |
| İnce SVG çizgi ve yaylarda dokunma alanı 24 px'in altındaydı (p26, p27, p29, p30, p33) | Görünür öğenin üstüne saydam, 26–28 px kalınlığında ayrı dokunma alanı çizildi |
| Üçgen sahnesinde cetvel etiketi cetvel şeridiyle üst üste biniyordu | Şerit yukarı alındı, tuval 6 px uzatıldı |
| Adres çubuğundaki `#oyun` değişince (tarayıcı geri tuşu) sahne eski oyunda kalıyordu | `hashchange` dinleyicisi eklendi |
| "Pencereyi boşalt" seçili pencere zaten boşken hiçbir şey yapmıyordu | Seçili pencere boşsa son dolan pencere geri alınıyor |
| Sütun grafiğinde dikey eksen sayıları sütun yüksekliklerinden kopuk çiziliyordu (p53–p56) | `eksenliGrafik` yeniden yazıldı: eksen çentikleri ve sayılar sütun yüksekliğine birebir hizalı, sütun etiketleri tek satırda |
| Katalogdaki alt başlıklar kaldırılan mekaniği anlatıyordu ("Makası doğru tünele çevir", "Eksik sayıyı yakala", "Büyük olanı yakala", "Sihirli mührü seç") | 27 oyunun alt başlığı şartnamedeki başlıkla hizalandı |

## Kalan / şartname dışı notlar

- p31 ve p50'deki tahmin turlarında tolerans bilinçli olarak geniş tutuldu (tahmin bir kavram, kesin ölçü değil); bu turlarda can eksilmiyor.
- p46'nın 3. turunda rota "tam olarak dikdörtgenin sınırı" olarak doğrulanıyor (`exact:true`); içeri giren rota kabul edilmiyor.
- Ses dosyaları henüz üretilmedi; motor `parent.oku()` köprüsü ya da tarayıcı `speechSynthesis` ile Türkçe okuyor.
