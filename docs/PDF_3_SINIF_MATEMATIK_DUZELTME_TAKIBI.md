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
- `ertele(fn,ms)`: geciken geri çağrılar tur değiştiyse çalışmaz. `render`,
  `wrong`, `updateStage` ve `renderRound` artık oyun bittikten sonra çağrılırsa
  sessizce çıkar (koşumda seyrek görülen "round().prompt undefined" hatası).
