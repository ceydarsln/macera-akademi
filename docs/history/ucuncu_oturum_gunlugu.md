# Üçüncü oturum — kusur günlüğü (radar/matbaa/tren/tamirhane/kargo/dedektif/grafik/sirik/radarkod)

## radar-phaser.html · catchDrop (42 oyun)
radar-phaser.html (42 catchDrop oyununun tümü) · yakalama örtüşmeyle karar veriliyordu; kapsüller 120–244px, ekran 480px olduğu için ortaya düşen yanlış kapsülden kaçmak fiziksel olarak imkânsızdı — kusursuz oynayan sınama botu bile can kaybediyor, u33/y03'te oyunu tamamen kaybediyordu · overlap kaldırıldı; kapsülün altına parlak "çekirdek" çizildi, update() içinde merkeze en yakın kapsül seçilip |kapsülX − radarX| ≤ 42 eşiği uygulanıyor (SABLON_KURALLARI §5 "kenara değmek = yakalamak değil")
radar-phaser.html · yeni yakalama kuralı ekranda yazılı değildi, çocuk kutunun kenarını değdirip neden sayılmadığını anlamıyordu · oyun başında 4 saniye görünen "🎯 Kapsülün altındaki sarı noktayı çanağın ortasına getir" ipucu eklendi

## matbaa-phaser.html · sentenceBuild (25 oyun)
matbaa-phaser.html (100 turun 88'i: z61/z04/z31/z34/z22/sb05/sb23/z15/z47 … hepsi) · kızaktaki kartlar tek satıra diziliyordu; toplam genişlik 846px'e çıkarken kızak 452px — kartlar ekran dışına taşıyordu · punto/kart boyu cümlenin GERÇEK genişliğinden seçiliyor (21→15px), kartlar satırlara sarılıyor, kızak yüksekliği tura göre çiziliyor (olculeriSec/satirlaraBol/kizagiCiz)
matbaa-phaser.html (tüm 25 oyun) · kartlar yerçekimiyle masaya dökülüyordu; 8–10 kart 480px masada kilitlenip üst üste biniyordu, dokunulan kart yerine üstte kalan komşu tutuluyordu (z61'de 41 ıskalama üst üste) · her karta yuva verildi (masaYuvalariHesapla), yerçekimi kapatıldı, kartlar yuvasına süzülüyor; yanlış bırakılan kart fırlatılmak yerine yuvasına dönüyor
matbaa-phaser.html · dokunma alanı görselden ±12px genişti, komşu kartın alanı bu kartın merkezini örtüyordu · pay ±4px'e indirildi

## tren-phaser.html · dragSlider (21 oyun)
tren-phaser.html (110 tick: y06 sessiz/fısıltı/normal/bağırma, w11 3/10·1 bütün, w18 "150 ↖ başlangıç" …) · ticks[].label alanı hiç okunmuyordu, çocuk anlamlı ölçek yerine çıplak sayı görüyordu · duraklariUret artık {deger, etiket} döndürüyor; etiket varsa tünelde o yazılıyor, karşılaştırma yine değerle yapılıyor
tren-phaser.html (13 tur: p36 {v}°, y06 {v} / 10, p31 {v} cm …) · cfg.rounds[].format ayrıştırılıyor ama HİÇ kullanılmıyordu; açı oyununda "90" yazıyordu, "90°" değil · etiketi olmayan durakların yazısı format ile üretiliyor, "Seçilen: 90°" olarak gösteriliyor
tren-phaser.html · tünel etiketi sabit 24px yazılıyordu; 5 duraklı turda tünel 86px ve uzun etiketler komşu tünellerin üstüne biniyordu · etiketYaz() genişliğe sığan en büyük puntoyu (23→11px) seçip satır sarıyor

## tamirhane-phaser.html · punctFix (16 oyun)
tamirhane-phaser.html (93 büyük-harf düzeltmesinin 31'i özel ad: y05 ahmet/zeynep, y13 kemal/atatürk/selanik'te, y51 nisan …) · onarılacak sözcüğün altına kırmızı çizgi çiziliyor ve YALNIZ o sözcük titriyordu; hangi sözcüğün özel ad olduğunu bulmak görevin kendisiyken cevap işaretle veriliyordu · kırmızı tamir çizgisi ve titreme kaldırıldı, bütün sözcükler aynı görünüyor
tamirhane-phaser.html · işaret kaldırılınca çocuğun kaç düzeltme aradığını bilmesi gerekiyor · tezgâhın üstüne "Kalan: 🔠 2 büyük harf · ✒️ 1 işaret" sayacı eklendi (hangi sözcük olduğunu söylemiyor)
tamirhane-phaser.html · işaret kartlarının dokunma alanı ±12px payla komşu kartın alanına giriyordu (kartlar 44px, aralık 52px) · pay ±4px'e indirildi

## kargo-phaser.html · codeGrid (15 oyun)
kargo-phaser.html (32 turun 30'u: 6x5, 6x6, 7x6 ızgaralar — w38/y18/y43/y61/z18/z43/p46/h27/h62/sb09/f48/g48) · hücre 88px SABİTTİ; 7x6 ızgara 616x528px ediyor, 480x800 ekranda yanlardan ve program şeridinin üstünden taşıyordu, hücreler/dron/hedef ekran dışında kalıyordu · hücre ölçüsü tur başına hesaplanıyor (izgaraOlcuHesapla: 34–88px arası, banda ortalanıyor), duvar/hedef/dron emojileri de hücreye göre ölçekleniyor
kargo-phaser.html (32 tur) · duvar emojisi r.wallEmoji okunuyor ama çizimde genel '🚧' kullanılıyordu; turun timsah/kaya/dağ/su engeli hiç görünmüyordu · t.duvarEmoji çiziliyor
kargo-phaser.html (32 tur) · gorev ve ipucu aynı alandan (r.hint) besleniyordu, aynı cümle ekranda iki kez yazılıyor ve ızgaraya kalan yeri yiyordu · ikinci satır kaldırıldı, görev yazısı şeridin altına alındı

## dedektif-phaser.html · wordHighlight (14 oyun)
dedektif-phaser.html (9 tur OYNANAMAZ: y26 ×3, z07, z40 ×2, z42 ×2, u26) · cevap metindeki simgeyle TAM eşitlikle karşılaştırılıyordu; cevap "kütüpanede" iken simge "Kütüpanede" (cümle başı), cevap "paşa" iken "paşa," — doğru sözcüğe dokunan çocuk hata alıyor, 3 can bitince oyunu kaybediyordu · anahtar() ile kenar noktalaması atılıp Türkçe küçük harfe çevrilerek karşılaştırılıyor
dedektif-phaser.html (23 tur: u51, u57, y26, y50, z07, z40, z42 …) · rounds[].fixTo (yanlış yazımın doğru hâli: "kütüpanede → Kütüphanede", "festival → şenlik") hiç okunmuyordu; çocuk yanlışı buluyor ama doğrusunu görmüyordu · düzeltilmiş biçim deftere sarı kartla yazılıyor ve "yanlış → doğru" iletisi gösteriliyor
dedektif-phaser.html · defter kartının genişliği kaynak sözcüğün genişliğinden alınıyordu; düzeltilmiş biçim daha uzun olunca yazı kutudan taşıyordu · genişlik yazının gerçek ölçüsünden alınıyor

## grafik-phaser.html · graphBuild (11 oyun)
grafik-phaser.html (w48 hedef 7, g44 hedef 7) · sütun kapasitesi AZAMI 6 SABİTTİ; 7 blok isteyen sütunda 7. blok çizilen oyuğun üstüne taşıyordu · AZAMI verideki en büyük hedeften hesaplanıyor, blok boyu ona göre küçülüyor
grafik-phaser.html (11 oyunun tümü) · hedef sayı üç ayrı yerden ele veriliyordu: sütun etiketi "0 / 5" yazıyor, ızgarada hedef yüksekliğindeki çizgi sarı vurguluyor, depoda tam hedef sayısı kadar blok bulunuyordu — çocuk ekrandaki kaynak veriyi hiç okumuyordu · etiket yalnız geçerli sayıyı gösteriyor, ölçek çizgileri eşitlendi, depo hedef+2 fazlalı blok veriyor
grafik-phaser.html · sürükleme sırasında yalnız EKSİK sütunlar parlıyordu (hangi sütuna blok gerektiğini söylüyordu) · bütün sütunlar bırakma hedefi olarak parlıyor
grafik-phaser.html · sütun dolduğunda "Elma sütunu zaten dolu (5)." iletisi hedefi yazıyordu · "Verilere yeniden bak: Elma sütununda gereken kadar blok var." iletisiyle değiştirildi

## radarkod-phaser.html · numPad (10 oyun)
radarkod-phaser.html (p01 ve p18 — 8 tur, iki oyun baştan sona OYNANAMAZ) · AZAMI_BASAMAK 3 SABİTTİ ama cevaplar 245612, 103020, 500000, 36908, 5634, 3348, 4000, 3766; çocuk cevabı tuşlayamıyordu · basamak sınırı turların gerçek cevaplarından hesaplanıyor (3–7 arası)
radarkod-phaser.html · rakam kartları TUP_X−46+sıra×46 ile diziliyordu; 6 basamakta 230px ediyor, tüp 168px — kartlar tüpün dışına çıkıyordu · aralık ve kart genişliği tüpe sığacak şekilde hesaplanıyor, diziliş tüpün ortasına göre

## Beş şablonda ortak düğme kusuru
radarkod / kargo / tren / grafik / sirik -phaser.html · dugmeYap() geri çağrıyı basma tween'inin SONUNDA çalıştırıyordu (≈180ms); tuş takımında aynı tuşa üst üste basılınca bir basış yutuluyordu (sınamada "500000" yerine "50000" yazıldı) ve her dokunuş 180ms gecikmeyle işliyordu · işlem hemen yapılıyor, tween yalnız görsel geri bildirim olarak kaldı
tren-phaser.html (21 dragSlider oyununun TAMAMI) · tekSatir() TURLAR eşlemesinde çağrılıyor ama şablonda hiç tanımlı değildi; betik yüklenirken ReferenceError verip TURLAR kurulamıyor, oyunlar boş ekranla açılıyordu · duzMetin üzerinden tekSatir() tanımı eklendi
tren-phaser.html (21 oyunun tümü) · turun sonucu fizik çarpışmasıyla belirleniyordu: tren 430px/sn ile 36px'lik tünel ağzından geçiyor, kare gecikmesi 120ms'ye çıkınca bir karede 52px yol alıp ağzı atlıyor ve overlap hiç tetiklenmiyordu — tur sessizce sonuçsuz kalıyor, tren yukarı kaçıp raya dönüyor, çocuk neden bir şey olmadığını anlamıyordu · sonuç ONAYLA anındaki seçimden belirleniyor (sonucuVer/agizBul), uçuş yalnız canlandırma; overlap kaldırıldı
tren-phaser.html · update() içindeki "yukarı kaçan treni geri al" kurtarması onaylandi bayrağını sıfırlamıyordu, tur kilitli kalıyordu · kurtarma kaldırıldı (tren artık serbest uçmuyor)

## radar-phaser.html · ipucu şeridi konumu
radar-phaser.html · yeni eklenen "🎯 çekirdeği ortala" ipucu BOY-128'de radar çanağının üstüne biniyordu (ekran görüntüsünde görüldü) · şerit BOY-205'e taşındı, çanağın tam üstünde duruyor

## grafik-phaser.html · kaynak kutusu taşması
grafik-phaser.html (w48: "1 kitap: 5 · 2 kitap: 7 · 3 kitap: 4 · 4+ kitap: 2" gibi 3 satırlık kaynaklar) · çetele kaynağı kutusu 56px SABİTTİ; uzun metin kutudan taşıp altındaki sütun sayaçlarının ("0 / 0 / 0 / 0") üstüne biniyordu · kutu yüksekliği metnin gerçek ölçüsünden hesaplanıyor, konumu yönerge şeridinin altına bağlandı (seritAlt)

## Sınama kapsamı (otomatik oyuncularla baştan sona oynanarak) — TAMAMLANDI
catchDrop 42/42 · sentenceBuild 25/25 · dragSlider 21/21 · punctFix 16/16 · codeGrid 15/15 · wordHighlight 14/14 · graphBuild 11/11 · numPad 10/10 · jumpPath 10/10
**TOPLAM: 164/164 oyun baştan sona oynanıp completeGame çağrısı doğrulandı.**
Ölçüt: her oyunda otomatik bot oynadı, completeGame çağrısı görüldü (KAYIT.bitti), can kaybı ve kutu/etiket taşması ölçüldü, ekran görüntüsüyle görsel doğrulama yapıldı.
Dokuz şablonun tamamı tek başına da hatasız yükleniyor (konsol hatası yok, veri yapıları kuruluyor).
