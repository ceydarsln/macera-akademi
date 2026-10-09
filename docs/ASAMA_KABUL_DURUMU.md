# Sekiz aşamanın gerçek kabul durumu

28 Eylül 2026. Teknik testin geçmesi, oyunun bütün etkileşimlerinin veya görsel tasarımının kabul edildiği anlamına gelmez. Bu belge önceki kapsamlı “bitti” ifadelerinin yerine geçer.

| Aşama | Kanıtlanan kapsam | Tam kapsam durumu |
| --- | --- | --- |
| 1 — M41/M45/M47 | Üç oyunun üç turu, üç boyutta 27 gerçek seçim/sonuç senaryosu; yanlış, geçiş, bitiş ve yeniden başlatma geçti. | Hedefli uygulama ve tarayıcı doğrulaması tamamlandı; fiziksel cihaz ve insan onayı ayrıca bekler. |
| 2 — Diğer matematik sahneleri | M51/M54/M58/M59/M60 için 45 senaryo; önceki ölçüm/dondurma/sayı çizimi paketleri. Bu tur M13 seçim geri alma yarışı, küçük hedefler ve W32 mozaik düzeltildi. | Bütün matematik oyunlarının tüm davranışları ve estetik/pedagojik kalitesi ayrı ayrı kabul edilmedi. |
| 3 — Türkçe sahne bağlantıları | 17 T oyununun üç tur/üç boyutta 153 senaryosu geçti. Yatay üretim bandında hedef/palet yan yana düzeni korundu. | Diğer Türkçe oyunlarında oyun özelinde tam kabul bekler. |
| 4 — Üst sınıflar | Önceki 364 oyunluk başlangıç taraması, 27 hedefli oyun/243 tur-ekran kaydı; bunların 27 kaydı yalnız başlangıçtır, hepsi tamamlanmış oynanış değildir. W32'nin gerçek yerleştirme ve dış çevre akışı bu tur ayrıca doğrulandı. | Bütün 364 oyunun ayrı ayrı animasyon, yazma, yanlış işlem, geri alma ve son durum kabulü tamamlanmadı. |
| 5 — Fen/hayat deneyleri | 126 oyunda normal sürelerle üç doğal tur, oyun sonu ve yeniden başlatma; 87 oyunun ilk turunda yanlış işlem/yeniden deneme ve uygulanabilir dokunma iptali. Önceki sekiz hedefli deneyin ayrıntılı sahne kontrolleri korunur. | Doğru oynanış bütün 126 oyuna yayıldı. Bütün oyunların her turunda hata yolları, sahne sonuçlarının tek tek görsel değerlendirmesi ve fiziksel cihaz kabulü hâlâ açık. |
| 6 — 635 oyunun tam oynanış kabulü | 635 oyunun 1905 tur teknik çözüm kaydı ve kaynak parmak izi; 5715 başlangıç yerleşimi kontrolü. Hedefli doğal tur oynanışları ayrı kaydedilir. | **Açık.** Teknik çözücüler bazı türlerde durum/eşleştirme yardımcıları kullanır; hepsi gerçek işaretçi/dokunma testi değildir. Her oyunda doğru/yanlış/iptal/can bitişi/yeniden başlatma/doğal geçiş/oyun sonu kanıtı henüz yok. |
| 7 — Gerçek telefon ve ses | Samsung SM-A065F Android telefona üretim uygulamasından ayrı `com.maceraakademi.app.test` kuruldu. V02'nin üç turu gerçek sürüklemeyle tamamlandı; yanlış seçim ve hedef dışı bırakma kontrol edildi. V03'te ilk tur, V05'te ilk süsleme ve V04'te ilk ritmik adım sahnede doğrulandı. Android 15+ durum çubuğu taşması ve V02–V05 alt kontrol görünürlüğü düzeltildi. | **Kısmen açık.** Bu, tek telefon ve dört hedefli oyundur. Sesin gerçekten duyulması, yön değiştirme, klavye, diğer oyunlar ve iPhone kabulü henüz doğrulanmadı. |
| 8 — Kullanıcı görsel onayı | Hedefli galeriler ve kabul takibi hazırlanır. | **Sizin onayınız bekliyor.** Otomatik test, sizin beğeni/onayınız olarak kaydedilmez. |

## 28 Eylül — kesintisiz deney girdileri ve genişletilmiş oynanış

- F21/F23: ısıtma sırasında kontrol düğmesi her karede silinip yeniden oluşturulmuyor. Düğme doğrudan ocağın üzerinde. Dokunmayı iptal etme, tuş bırakma ve odak kaybı ısıtmayı durduruyor.
- G40: sulama düğmesinde işaretçi yakalama, iptal, odak kaybı ve Enter/Space desteği var.
- G27/H08/H30/Z23: ölçüm/tahmin sürgüsü hareket ederken yeniden oluşturulmuyor; sürekli dokunma ve klavye odağı korunuyor. Ölçek değişince sahne güncelleniyor.
- Fen 3/4, hayat bilgisi 2, Türkçe 3/4 ve matematik 4'te ortak sürükleme işlevi, iptalden kalmış tıklama engelini sonraki yeni dokunuşta temizliyor. Yanlış/iptal taramasında yakalanan gerçek bir giriş sorunudur.
- Yedi oyunda üç boyutta 21 kontrol: dokunma iptali, bırakma, odak kaybı veya kesintisiz sürgü hareketi. Bu bir fiziksel telefon testi değildir.
- 126 fen/hayat oyununun 378 turu, cevap/can/tur durumu atanmadan gerçek tarayıcı fare/klavye girdileriyle oynandı. Bazı sürükleme oyunlarında desteklenen dokun-seç/dokun-bırak yolu kullanılır; bütün işlemler gerçek sürükleme olarak raporlanmaz.
- 87 oyunun ilk turunda üç yanlış işlem ve yeniden deneme kontrol edildi; sürükleme kaynağı olanlarda Chromium dokunma iptali de sınandı. Bu kayıt diğer iki turun hata yollarını kapsamıyor.
- Günün ilk bağlantı kontrolünde telefon görünmedi; sonra Samsung SM-A065F USB hata ayıklama ile bağlandı. `com.maceraakademi.app.test` üretim uygulamasının üzerine yazılmadan telefona kuruldu.
- V02 Kargo Treni'nin üç turu fiziksel telefonda gerçek vagona sürüklemeyle oynandı (34, 47, 62). Yanlış seçim can azalttı; hedef dışına sürükleme ilerletmedi. V03'te nilüfere yerleştirilen sayı tek kez gösterildi; V04'te 2 seçimi uzaylıyı sonraki tramboline taşıdı; V05'te mum pastadaki gerçek boşluğa yerleşti. V03/V04/V05'in üçer tur tamamı sınanmadı.
- Android `:app:assembleDebug --offline` başarılı; güncel test APK'si `app/build/outputs/apk/debug/app-debug.apk`. Gerçek telefon sınaması başlamıştır, fakat kapsamlı cihaz/ses kabulü açık kalır.

Yeni galeri: `artifacts/fen-hayat-katalog-oynanis/index.html`.
Kontrol görüntüleri: `artifacts/fen-hayat-katalog-oynanis/kontroller.html`.
Kanıtlar: aynı klasörde `results.json`, `rejection.json`; `artifacts/surekli-deney-kontrolleri/results.json`.
Yeniden üretim: `tools/verify-science-catalog-native.cjs`, `tools/verify-science-rejection.cjs`, `tools/verify-continuous-controls.cjs`, `tools/render-science-catalog-review.cjs`.
Doğal oynanış aracında `--retry` yalnız güncel kaynak parmak iziyle geçmiş kayıtları korur. Galeri üreticisi 126/87/21 başarılı kayıt ve doğal oynanışın güncel kaynak eşleşmesini zorunlu tutar.

## Bu turda yapılan değişiklikler

- Pusulanın iğnesi kuzey işaretine oturur. Malzeme, başlığa değil gerçek deney SVG'sine bırakılır.
- F32'de pil/kablo/ampul/anahtar eksikleri ve açık anahtar sahnede görünür. İlk kurulumda ampul yalnız son test adımıyla yanar.
- F34'te yalıtkan çubuk, aynı yönde seri bağlanmış iki ayrı pil ve son devre görüntüsü gösterilir. Yeni soruda önceki sorunun açıklaması kalmaz.
- F41'de konu dışı park maketi yerine lamba siperi, aşağı yönlendirme, zamanlayıcı, sensör, parlaklık ve perde işlemleri gece aydınlatma sahnesini değiştirir. Doğru malzeme kimlikleri/öğrenme doğrulayıcısı korunur; adlar ve yazı ölçütü konuya uygun hale getirilir.
- H29'da musluk kolu lavabonun üzerinde gerçek kontroldür. Basılı tutma suyu artırır; bırakma/iptal durdurur. Enter/Space desteği ve odak kaybında durma vardır. Eski hata açıklaması yeni su akıtma işleminde kaldırılır.
- G45'in hedefleri farklı yaşam alanı çizimleridir; yerleştirilen etiket alanda kalır.
- Kurulumun son parçası eklendiğinde de model yeniden çizilir. Bitmiş deneyde eski işlem düğmeleri temizlenir; sonuç sahnede görünür.
- Kısa ekranlarda içerik kesilmek yerine kaydırılabilir. Cüce Adımı'nın özel görsel düzeni ortak sahne boyutu kuralına sokulmaz; Türkçe'nin özel yatay yan yana düzeni korunur.
- 13 oyundaki küçük hedef sinyalleri giderildi: M02/M17/M26/M33/M38/V05/V09/V23/W32/W44/Z01/G25/H05. Genel estetik kalite iddiası değil, tarayıcıda ölçülen hedef boyutu düzeltmesidir.
- M13'te hedef sayıya ulaşıp hemen seçim geri alınırsa bekleyen başarı artık geçersiz olur; üç tur ve üç boyutta dokuz senaryo geçti.
- W32'de mozaik tüm parçaların sınırlarına göre ölçeklenip ortalanır. Negatif koordinatlar da çerçevede kalır. Yatayda palet yan taraftadır; sürüklenen parçanın paleti çökertip hedefi kaydırması önlenir. Dokuz senaryoda bütün parçalar, yanlış parça, iptal, dış kenarların sayılması, doğal geçiş, bitiş ve yeniden başlatma geçti. Negatif denemeler üçüncü turda üretim can sıfırlamasını tetikleyebilir; test gerçek sıfırlama süresini bekler, can/cevap enjekte etmez.

## Kanıtları yeniden üretmek

Yerel Node yolu: `/Users/ceyda/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`.
Playwright için `NODE_PATH=/Users/ceyda/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules` gerekir.

- `tools/catalog-acceptance.cjs --refresh-stale`: yalnız değişmiş kaynağa ait eski teknik kayıtları yeniler. `--resume` eski kaynağı yenilemenin yerine geçmez.
- `tools/audit-all-round-layouts.cjs`: 635 × 3 tur × 3 boyut; başlangıç taşma/kesilme ve küçük kontrol sinyalleri. Bu araç oyunu oynamaz.
- `tools/verify-science-completion.cjs`: sekiz deney için doğal üç tur. Negatif denemeleri ayırmak için her turda test canını yeniler; 25/30 ms hızlı test geçişleri görüntü alınabilsin diye uzatılır. Ses oynatma kapalıdır.
- `tools/verify-science-native-input.cjs`: üretim süreleriyle can sıfırlaması, Chromium yerel dokunması/iptali ve musluk klavyesi; cevap veya can enjekte etmez.
- `tools/verify-sheep-selection.cjs`: seçim geri alma ve bekleyen başarı iptali.
- `tools/verify-mosaic-native.cjs`: mozaik parçaları ve dış çevre; doğal üç tur.
- `tools/render-completion-ledger.cjs`: eski kaynaklı teknik kayıt veya eksik/başarısız kanıt varsa raporu yayımlamaz.
- `tools/release_static_check.cjs`: HTML betikleri ve yerel dosya bağlantıları.

İnceleme: `artifacts/fen-hayat-tamamlama/index.html`.
635 oyunluk ayrı kabul takibi: `artifacts/tam-kabul-takibi/index.html` ve `ledger.json`.
Ekran görüntüleri/statik ölçüm sonuçları otomatik estetik, gerçek cihaz, ses veya kullanıcı onayı değildir.
