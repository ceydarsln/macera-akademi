# 3. Sınıf Matematik PDF Düzeltme Takibi

Kaynak: `output/pdf/3_sinif_matematik_oyunlari_detayli_duzeltmeler.pdf` (58 sayfa, w01–w48).
Şartnamenin yapılandırılmış hâli: `tmp/spec3.json` (PDF üretici betiğinden çıkarıldı).
Motor: `web/phaser/matematik3-pdf-phaser.html` (matematik2 çerçevesi + 3. sınıf yardımcıları).

"Uygulamada" işareti yalnız şu koşullar birlikte sağlanınca verilir:

1. Üç tur farklı veriyle baştan sona oynanır (`tools/dom_kosum.html` ile doğrulanır).
2. Sahne cevabı ele vermez: hazır model, sayı ya da etiket kopyalanamaz.
3. Çocuk gerçek bir karar verir (hangi modül, hangi tünel, hangi adım).
4. Yanlışta doğruyu söylemeyen, nedeni gösteren geri bildirim gelir.
5. 375×812 telefon ekranında hedef alanı ve seçenekler ilk ekranda görünür.

| ID | Oyun | Kazanım | Uygulanan ana düzeltme | Durum |
|---|---|---|---|---|
| w01 | Mega Uzay Çekirdeği | 1000'e kadar sayı temsilleri | Hareketli kapsül yakalama kaldırıldı; çocuk fazlalıklı havuzdan yüzlük/onluk/birlik seçerek sayıyı kuruyor, sonra dört gösterimi eşliyor. Sahnede hazır model yok. | Uygulamada |
| w02 | Altın Kubbe | Esnek sayı çözümleme | Sayaç bulmacası yerine tek tek taş yerleştirme; aynı sayı üç farklı çözümlemeyle (3y+4o+8b, 2y+16o, 506'da boş onluk) kuruluyor. | Uygulamada |
| w03 | Hızlı Tren Sinyalleri | Onluğa/yüzlüğe yuvarlama | Uzaklıklar sayı doğrusunda gerçek değerlerle yazılıyor; gerekçe ekranda kalıyor, sürgü cevabı önceden vermiyor. | Uygulamada |
| w04 | Sihirli Fasulye Sırığı | Ritmik sayma | Rota çizgisi cevabı söylüyordu; dal artık yalnız doğru seçimden sonra büyüyor. Çeldiriciler ±2 komşuluğunda. İleri 8'er, geri 8'er, 100'er turları. | Uygulamada |
| w05 | Meyve Paylaşımı | Tek ve çift sayıları keşfetme | Sayı kartına dokunmak yerine çocuk meyveleri iki tabağa birer birer dağıtıyor; artan tek meyve görünür kalıyor, TEK/ÇİFT kararı bundan sonra veriliyor. | Uygulamada |
| w06 | Tek-Çift Laboratuvarı | Toplamların tek-çift yapısı | Kural ezberi yerine iki sayının noktaları eşleştiriliyor; artan noktalar toplamın tek mi çift mi olduğunu gösteriyor. | Uygulamada |
| w07 | Mimarlık Akademisi | Şekil-sayı örüntüsü | Örüntü kuralı yazılı verilmiyordu; kule adımları tek tek kuruluyor, sıradaki adımın taş sayısı önceki farklardan çıkarılıyor. | Uygulamada |
| w08 | Kavanozdaki Misketler | Stratejik tahmin | Rastgele seçenek yerine görünür bir örnek grup (10'luk/5'lik) ölçü alınıyor; tahmin bu ölçünün kaç kez sığdığından yapılıyor. | Uygulamada |
| w09 | Pizza Şefi | Bütün, yarım ve çeyrek | Fiş artık doğru paletin etiketini söylemiyor: 1. turda görsel model, 2. turda kesir sembolü, 3. turda sözel sipariş var. Dilimlerin üstünde yazı yok; tepsi gerçek daire alanında toplanıyor, aynı miktar farklı bileşimlerle kurulabiliyor. 1/8 yalnız 3. turda açıklanarak giriyor. | Uygulamada |
| w10 | Çikolata Fabrikası | Eş parçalar ve birim kesir | Yuvarlak disk ve "2'ye Böl" düğmeleri kaldırıldı; kare bölmeli gerçek tablet üzerinde kesme çizgisini çocuk kendi çekiyor, yanlış çizgiye dokununca kalkıyor. Parçalar ayrılıp seçildikten sonra 1/payda etiketi açılıyor. 3. turda hazır gelen eş olmayan kesim düzeltiliyor. | Uygulamada |
| w11 | Kesir Asansörü | Pay ve payda ilişkisi | Yatay tren/tünel/ray tamamen kaldırıldı; 0 ile 1 bütün arasında on eş aralıklı dikey kuyu var, kabin parmakla sürüklenip katlara mıknatıslanıyor. Geçilen kat (pay) ve bütün kat (payda) ayrı renkte sayılıyor; ilerleme "görev" olarak yazıyor. | Uygulamada |
| w12 | Zaman Kulesi | Analog ve dijital saat | Ok düğmeleri artık tek yol değil: ibreler uçlarından sürükleniyor, yönerge de bunu söylüyor. Zaman tek dakika sayacıyla tutulduğu için akrep dakikaya göre sürekli ilerliyor (14.45'te 2 ile 3 arasının dörtte üçünde). Dijital hedef ve günlük dil ayrı kartlarda. | Uygulamada |
| w13 | Zaman Tüneli Bandı | Zaman birimi dönüşümleri | Yürüyen bant kaldırıldı: kart karar verilene kadar ortada duruyor, hiçbir kenarda kırpılmıyor. Kutular "7 gün", "12 ay", "24 saat", "60 dakika", "60 saniye" olarak sayı+birim taşıyor. Doğru eşlemeden sonra grup modeli (numaralı çipler / noktalar) açılıyor. 3. turda 365 gün = 52 tam hafta + 1 gün modeli gösteriliyor, artık yıl da anlatılıyor. | Uygulamada |
| w14 | Kronometre Arenası | Süre tahmini | Hedef süre ve işaretli bölge kaldırıldı. Çocuk önce tahminini kaydediyor (hedef görünmüyor), sonra gerçek kronometreyle işi yapıp ölçüyor; tahmin / ölçüm / fark üçlü kartı sonda geliyor. Can eksilmiyor. Eylemler kişisel hıza bağlı 100 m koşu yerine ad yazma, 10 el çırpma, kısa cümle okuma. | Uygulamada |
| w15 | Ölçüm İstasyonu | Uygun uzunluk ve kütle birimi | Beşli karışık satır ikiye ayrıldı: önce "uzunluk mu, kütle mi?", sonra o ailenin cm-m-km ya da g-kg-ton ölçeği. Eksik olan gram eklendi. Nesne kartı sabit ve tam görünür; yanlış ailede nicelik sorusuna geri dönülüyor. 3. turda aynı kalemin boyu ile kütlesi peş peşe soruluyor. | Uygulamada |
| w16 | Banka Gişesi | Parada eşdeğerlik | Yasak çekmeceler kilitli ve nedeni yazılı; kilide basmak can götürmüyor. Paralar tepside gerçek yüzleriyle diziliyor, 100 kuruşluk gruplar çerçeveleniyor ve "1 TL" etiketi alıyor. Toplam çift gösterimle yazılıyor (250 kr = 2 TL 50 kr), fazla ödemede son para geri alınabiliyor. 3. tur aynı tutarı iki farklı bileşimle istiyor. | Uygulamada |
| w17 | Zihin Arenası | Tahminî ve gerçek sonucu ilişkilendirme | Düşen sayı kapsülleri ve kalkan kaldırıldı; işlem panosu sabit. Tur yedi adım: iki sayıyı sayı doğrusunda yuvarla → parçalayarak (279 = 200 + 70 + 9) adım adım kesin sonucu bul → tahminle kesin sonucu aynı eksende işaretle → farkı bul → farkı yorumla. Başarı ancak yorum adımından sonra veriliyor. | Uygulamada |
| w18 | Akıllı Asansör | Toplama ve çıkarmanın tersliği | Yatay tren/tünel/sürgü gitti; numaralı dikey kuyu var, kabin sürükleniyor. Çıkış mavi, dönüş kırmızı iz bırakıyor ve iki iz üst üste geliyor. İlerleme "görev" olarak yazıyor. Her turda ileri işlem ve tersi aynı başlangıç/varış üzerinde doğrulanıp iki eşitlik yan yana yazılıyor. | Uygulamada |
| w19 | Uzay Kargo Bandı | 10 ve 100 ile çarpma-bölme | "Sağa sıfır ekle" kutuları kaldırıldı. Çocuk rakamları basamak tablosunda kaydırıyor; açıklama "basamak değeri 10 katına çıktı" diyor, boşalan basamakta 0'ın yer tutucu rolü gösteriliyor. Sağa kayamayan sayıda kart kaybolmuyor, nedeni yazılıyor. | Uygulamada |
| w20 | Şeker Çiftliği | Çarpma ve bölmenin ilişkisi | Otomatik doldurma kaldırıldı: 32 şeker bantta duruyor, çocuk kutulara tek tek yerleştiriyor ve her kutudaki nesne ayrı ayrı sayılabiliyor. Kutu doldukça 4, 8, 12 … ritmik sayma şeridi oluşuyor. Fazla dokunulan kutu tek başına uyarılıyor, düzen bozulmuyor. Sonra aynı kutular üzerinde önce çarpma sonra bölme ifadesi seçiliyor. | Uygulamada |
| w21 | Labirent Robotu | Yönergeyi işlem diline dönüştürme | Fasulye sırığı motoru kaldırıldı: duvarlı istasyonlardan oluşan robot laboratuvarı ve program şeridi var. Çocuk işlem kartlarını sırayla şeride diziyor, "Çalıştır" deyince robot istasyon istasyon ilerliyor ve her bloğun altında ara sonuç (12 → 36) kalıcı yazıyor. Hatalı blok kırmızıya dönüyor, robot kapıya taşınmıyor. 3. turda çocuk zinciri sözel cümleye çeviriyor. | Uygulamada |
| w22 | Doğa Dedektifleri | Verilerden problem kurma | Roket-yakıt motoru gitti; 3 çadır ve her çadırda 4 çocuk gerçekten görünüyor. Hazır çözüm kartı başlangıçta yok: çocuk önce gerekli verileri seçiyor (gereksiz veri seçilirse neden gerekmediği tartışılıyor), sonra kelime kartlarıyla soru cümlesini kuruyor, çözüm ancak bundan sonra seçiliyor. 3. turda bölme sorusunun çarpma sağlaması da yapılıyor. | Uygulamada |
| w23 | Kozmik Tahterevalli | Eşitliğin anlamı | Yönerge kaç doğru beklendiğini açıkça yazıyor ("3 tane var"). Karta dokununca değeri kefeye biniyor, kefe açısı farkla orantılı eğiliyor ve iki değer birden okunuyor. Yanlış kart eleniyor ama tur bitmiyor; bütün eşdeğer ifadeler bulunana kadar sürüyor. 3. turda 20 + ? = 35 eksik bloğu ekleniyor. | Uygulamada |
| w24 | Fırıncının Tezgâhı | Kısa ve verimli işlem stratejisi | Sipariş metni artık "4 tepsi × 12" demiyor, yalnız toplam simiti söylüyor. 12'lik tepside 12 simit gerçekten görünüyor, tekler ayrı duruyor. Doğru ama uzun yol yanlış sayılmıyor: sipariş tamamlanınca "daha az işlemle olur mu?" seçeneği çıkıyor ve işlem sayısı tek tek koymakla karşılaştırılıyor. İpucu kademeli: önce büyük grup, sonra 12'nin katları. | Uygulamada |
| w25 | 3D Geometri Tarayıcısı | Küpün köşe, ayrıt ve yüzleri | Açılış sesi artık sayı vermiyor ("bütün köşeleri bul"). Küp parmakla döndürülen gerçek 3B model: öndeki öğeler büyük ve dokunulabilir, arkadakiler sönük ve dokunulamaz, hepsine ancak döndürerek erişiliyor. Aynı öğeye ikinci dokunuş saymıyor. 8-12-6 özeti yalnız tamamlandığında çıkıyor; yüz turunda açınım eşleşiyor. | Uygulamada |
| w26 | Şekil Kalesi | Çokgenleri kenar sayısına göre sınıflama | Bant kaldırıldı, şekil ekranda sabit ve tam görünür. Çocuk kenarlara tek tek dokunup numaralandırıyor; kapılar ancak bütün kenarlar izlenince açılıyor. Kapılarda ad + kenar sayısı + örnek var. Düzensiz, dönmüş, içbükey çokgenler ve bir açık çizgi ("çokgen değil") kullanılıyor. Yanlış kapıda şekil kaybolmuyor, can gitmiyor. | Uygulamada |
| w27 | Köşegen Dedektifi | Kare ve dikdörtgende köşegen | Açılış sesi sonucu vermiyor; yalnız "komşu olmayan köşeleri birleştir" diyor. İki köşe seçilince çizgi gerçekten oluşuyor, komşu seçimde çizgi kenar rengine dönüp farkı açıklıyor. İki köşegen çizilince kesişim vurgulanıyor ve uzunluklar ölçülüp karşılaştırılıyor. 3. turda üçgen karşı örneği: çocuk nedeni kendisi seçiyor. | Uygulamada |
| w28 | Geometri Stüdyosu | Araç kullanarak şekil çizme | Hazır kenarlar kaldırıldı: köşeleri çocuk ızgarada kendi seçiyor. Cetvel kenar uzunluklarını birim cinsinden yazıyor, gönye köşelere konup dik açıyı yeşil/kırmızı halkayla gösteriyor. Karede eş kenar ve dik açı ölçütleri ayrı ayrı denetlenip hangisinin sağlanmadığı söyleniyor (dikdörtgen çeldiricisi dâhil). Son köşe silinebiliyor, bitişte kenar/köşe ve kullanılan araç raporlanıyor. | Uygulamada |
| w29 | Çevre Avcıları | Çevreyi tahmin etme ve ölçme | Tren/tünel motoru kaldırıldı; gerçek kitap ve kenar boyunca dizilen birimler var. Tahmin aşamasında kenar uzunlukları GÖRÜNMÜYOR, çocuk göz kararı seçiyor ve ceza yok. Sonra her kenara dokunup ölçüyor, birimler boşluksuz diziliyor, en son toplam seçiliyor; tahmin-ölçüm farkı raporlanıyor. | Uygulamada |
| w30 | İp Dolama Serüveni | Eğri çevreyi ip ile ölçme | Kronometre kadranı ve süre şeridi gitti. Kutu, başlangıç mandalı ve ip var: çocuk parmağıyla çevrede dolaşıyor, iz gerçek açıyla büyüyor, tam tura ulaşmadan ölçüme geçilmiyor. Sonra ip düzleştirilip cetvelde sıfırdan okunuyor; 2. turda iki ip alt alta karşılaştırılıyor. | Uygulamada |
| w31 | Sıvı Laboratuvarı | Litre tahmini ve ölçme | Yatay süre şeridi kaldırıldı; dereceli sürahi ve musluk var. Önce dereceler kapalıyken çocuk tahmin çizgisini sürüklüyor, sonra dereceler açılıyor ve musluk basılı tutularak seviye yükseliyor. Taşma cezasız, geri boşaltılabiliyor. Son aşamada su 1 litrelik kaplara aktarılarak bağımsız doğrulanıyor; 3. turda dar/geniş kap karşılaştırması var. | Uygulamada |
| w32 | Mozaik Atölyesi | Şekillerle tasarım ve çevre | Parçalar gerçekten birleşiyor: ortak kenarlar kesik çizgiyle içeride kalıyor ve dokunulamıyor. Çocuk yalnız dış sınırdaki birim kenarları izleyip sayıyor. Ayrı çevrelerin toplamı ile birleşik çevre karşılaştırılıyor (ev 7→5, petek 18→14, roket 14→8); yanlış olan "bireysel çevreleri topla" yolu artık kabul edilmiyor. | Uygulamada |

## Motor tarafında eklenenler

- `renderSequence`: ritmik sayma (aynı seçenek listesinden sırayla doğru değerler).
- `toplamKanca(hedef)` + `hedefToplam` alanı: fazlalıklı modül havuzu; hedefe
  ulaşınca tur biter, aşınca can götürmeyen uyarı gelir.
- `renderDrag` sırası hedef→havuz olarak değişti (telefonda hedef ilk ekranda).
- `.hundred-flat`, `.core`, `.dome`, `.rail-line`, `.beanstalk` sahne stilleri.
- `renderShare`: iki tabağa birer birer dağıtma, artan nesne görünür kalır (w05).
- `renderBar` + `bar` mekaniği: kare bölmeli tablet, çocuğun çektiği kesme
  çizgileri (kenardan kenara, 1/8 adımıyla kılavuza oturur), yanlış çizgiye
  dokununca kalkar; `barParcalar()` alan eşliğini ve parça sayısını denetler,
  ardından parça seçme fazı birim kesri açar (w10).
- `renderLift` + `lift` mekaniği: on eş aralıklı dikey kuyu, kabin dikey
  sürüklemeyle katlara mıknatıslanır (w11).
- `renderClock` yeniden yazıldı: zaman tek bir dakika sayacında (`state.tm`)
  tutulur, akrep `tm*0.5°` ile sürekli hesaplanır, yelkovan sürüklenirken saat
  gerçek saatteki gibi taşınır; 5 dakikalık düğmeler erişilebilirlik yolu olarak
  kalır ve yönerge bunu söyler (w12).
- `kesirKanca(hedef)`: dilim değerleri sekizde bir biriminde toplanır, tepsi
  gerçek daire alanı üzerinde dolar; taşmada tur yeniden kurulur (w09).
- `turuTazele()`: hedefi aşan toplama kancalarında tur kilitlenmesin diye sahne
  yeniden kuruluyor (w01–w04'teki çıkmaz da bununla kapandı).
- `renderTiming` + `timing`: tahmin aşaması (hedef gizli) → gerçek zamanlı
  kronometre (`performance.now`) → tahmin/ölçüm/fark raporu; can eksiltmez (w14).
- `renderStation` + `station`: iki adımlı karar — önce nicelik (uzunluk/kütle),
  sonra o ailenin birimi; her nesne için ayrı kaydedilir, sonunda istasyon
  raporu açılır (w15).
- `renderPara` + `para`: kilitli/açık para çekmeceleri, tepside 100 kuruşluk
  gruplama, kuruş+TL çift gösterimi, son parayı geri alma ve "farklı bileşim"
  koşulu (w16).
- `renderArena` + `arena`: yuvarlama → parçalayarak hesaplama → fark → yorum
  adımlarını tek tur içinde zincirleyen adım listesi; `sayiDogrusu()` ortak
  yardımcısı tahmin ile kesin sonucu aynı eksende işaretler (w17).
- `renderTers` + `tersi`: numaralı dikey kuyu, sürüklenen kabin, çıkış/dönüş
  izleri ve her adımda kurulan eşitlik satırı (w18).
- `renderKargo` + `kargo`: beş sütunlu basamak tablosu, rakamları sola/sağa
  kaydırma, değişen basamakların vurgulanması, sağa kayamama gerekçesi (w19).
- `renderSeker` + `seker`: bant → kutulara tek tek yerleştirme (yalnız ilgili
  kutu güncellenir), ritmik sayma şeridi, ardından çarpma ve bölme ifadesi
  seçimi (w20).
- `renderRobot` + `robot`: istasyonlu labirent, silinebilir program şeridi,
  her blokta ara sonuç, hatalı blokta kırmızı vurgu; isteğe bağlı sözel
  okuma sorusu (w21).
- `renderProblem` + `problem`: veri seçme → kelime kartlarıyla soru kurma →
  çözüm (ve gerekirse sağlama) aşamaları; gereksiz veri gerekçesiyle
  reddediliyor (w22).
- `renderTerazi` + `terazi`: farkla orantılı eğilen kefe, çoklu doğru ve
  eksik blok aşamaları, elenmiş kartların işaretlenmesi (w23).
- `renderFirin` + `firin`: tepsi/tek paketleme, işlem sayacı, kademeli ipucu,
  "doğru ama daha kısası var mı?" karşılaştırması (w24).
- `renderKup` + `kup`: gerçek 3B döndürme (yaw/pitch), derinliğe göre
  erişilebilirlik, kalıcı işaretleme ve küp açınımı (w25).
- `renderSekil` + `sekil`: kenar izleme ve numaralandırma, kenarlar bitmeden
  açılmayan kapılar, doğruda şeklin döndürülmesi (w26).
- `renderKosegen` + `kosegen`: köşe çifti seçimi, komşu/komşu değil ayrımı,
  kesişim vurgusu ve uzunluk ölçümü (w27).
- `renderStudyo` + `studyo`: nokta ızgarasında serbest köşe seçimi, cetvel
  ölçümü, gönye ile dik açı denetimi ve ölçüte göre gerekçeli ret (w28).
- `renderCevre` + `cevre`: tahmin (uzunluklar gizli) → kenar kenar ölçme →
  toplam seçimi → tahmin/ölçüm/fark raporu (w29).
- `renderIp` + `ip`: dairenin çevresinde açı biriktiren gerçek sürükleme,
  tam tur denetimi, ipin cetvelde düzleştirilip okunması (w30).
- `renderSivi` + `sivi`: derecesiz kapta tahmin çizgisi, basılı tutulan
  muslukla yükselen seviye, 1 litrelik kaplarla doğrulama (w31).
- `renderMozaik` + `mozaik`: parçaların yuvalara yerleştirilmesi,
  `mozaikKenar()` ile ortak/dış kenar ayrımı, dış sınırın izlenerek sayılması
  ve ayrı çevre toplamıyla karşılaştırma (w32).
- `gecisBasla(fn,ms)`: aşama ilerledikten sonra sahne henüz yenilenmemişken
  gelen dokunuşlar bir sonraki aşamanın verisine uygulanıyordu; geçiş boyunca
  girdi kilitleniyor. (Gizli sekmede tarayıcı oyunun zamanlayıcısını kıstığı
  için bu boşluk saniyelere çıkabiliyordu.)
- `ertele(fn,ms)`: geciken geri çağrılar tur değiştiyse çalışmaz. `render`,
  `wrong`, `updateStage` ve `renderRound` artık oyun bittikten sonra çağrılırsa
  sessizce çıkar (koşumda seyrek görülen "round().prompt undefined" hatası).
