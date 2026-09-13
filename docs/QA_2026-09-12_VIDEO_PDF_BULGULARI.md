# Macera Akademi — Video ve PDF Bulguları / Debug Roadmap

Tarih: 12 Eylül 2026
İncelenen sürüm: repo `main`, `b8c1227` (`2.8.2`, `versionCode 23`)
Kaynaklar: 3:07 uzunluğundaki sessiz ekran kaydı ve `22_Macera_Akademi_Web_ve_PWA_Test_Raporu.pdf`

## Kapsam ve durum işaretleri

Video canlı uygulama kaydı değil; WhatsApp'ta paylaşılan, çoğu 8 Eylül tarihli ekran görüntülerinin ve çizimli notların kaydıdır. Bu nedenle video maddeleri önce “rapor edilen hata” kabul edilir. Debug başlamadan güncel `main` üzerinde yeniden üretilmelidir.

- **KODDA DOĞRULANDI:** Güncel kaynak kodda sorun veya risk doğrudan görülüyor.
- **YENİDEN ÜRET:** Videoda görülüyor; güncel sürümde hâlâ olup olmadığı cihazda doğrulanmalı.
- **KISMEN GÜNCEL:** Güncel kodda bu konuya yönelik değişiklik var; kullanıcı deneyimi yine test edilmeli.
- **RAPOR DÜZELTİLMELİ:** PDF'deki teknik iddia güncel kodla uyuşmuyor veya kanıtı eksik.
- **ÜRÜN KARARI:** Hata çözümünden önce beklenen davranış netleştirilmeli.

## PDF'deki hata ve riskler

| ID | Öncelik | Bulgu | Güncel kod karşılaştırması | Durum |
|---|---:|---|---|---|
| P-01 | Yüksek | Oturum anahtarı `macera-api-token-v1` düz metin olarak `localStorage` içinde tutuluyor; XSS oluşursa token okunabilir. | `web/api-client.js` bunu doğruluyor. | **KODDA DOĞRULANDI** |
| P-02 | Kritik iddiası | Çocuk mesajlaşmasında küfür/XSS filtresi olmadığı belirtilmiş. | Uygulama serbest metin almıyor; istemci ve PHP API yalnızca altı hazır mesaj kimliğine izin veriyor ve sadece kabul edilmiş arkadaşlara gönderiyor. Serbest metin açılmadıkça NLP küfür filtresi önerisi bu akış için geçerli değil. Yine de çıktı kodlama, hız sınırlama ve kötüye kullanım kaydı test edilmeli. | **RAPOR DÜZELTİLMELİ** |
| P-03 | Orta | Service worker'ın blob URL'den yüklendiği ve Phaser varlıklarını çevrimdışı önbelleğe alamayabileceği yazılmış. | Güncel kaynakta blob ile üretilen şey service worker değil, web manifest. Kayıtlı bir service worker ve çevrimdışı asset cache'i bulunamadı. Sonuçta çevrimdışı PWA eksikliği gerçek, fakat gerekçe yanlış. | **KODDA DOĞRULANDI + RAPOR DÜZELTİLMELİ** |
| P-04 | Yüksek | `contestSubmit` ve `duelCreate` için hız sınırı yoksa puanlar botlarla manipüle edilebilir. | Bu iki endpoint'te rate limit yok. Daha önemlisi, sunucu istemcinin yolladığı `score`, `correct` ve cevap özetlerini kabul ediyor; yalnızca geniş sayı aralığı kontrolü yapıyor. | **KODDA DOĞRULANDI** |
| P-05 | Orta | Ağ kesildiğinde ilerleme yalnızca yerel profile yazılıyor, otomatik senkron garantisi yok. | `saveState()` hatayı yutuyor; IndexedDB kuyruğu, idempotency anahtarı ve `online` olayında otomatik tekrar yok. | **KODDA DOĞRULANDI** |

> 12 Eylül 2026 uygulama notu — `P-04` için yarışma/düello toplamları artık sekiz cevaplık dökümden sunucuda yeniden hesaplanıyor; istemcinin toplam puanı, doğru sayısı, süreleri, sınıfı ve kategorisi doğrulanıyor. Kullanıcı+IP temelli hız sınırı eklendi ve sınıf yarışmasında ilk geçerli sonuç değiştirilemez hâle getirildi. `P-05` için IndexedDB tabanlı, idempotent ve artan bekleme süreli senkron kuyruğu eklendi; gerçek MySQL ortamındaki uçtan uca ağ kesintisi testi yayın öncesinde yapılmalıdır.

### PDF'nin kendi içindeki kalite sorunları

| ID | Bulgu | Neden önemli? |
|---|---|---|
| R-01 | “Canlı API Teşhis Modalı (MySQL Ping)” ekran görüntüsü kırık/boş. | Bulguyu doğrulayan görsel kanıt yok. |
| R-02 | Rapor `v1.0.4-prod` diyor; güncel uygulama `2.8.2`. | Test edilen build/commit belirsiz. |
| R-03 | Rapor giriş, kayıt ve gizlilik için `#loginModal`, `#registerModal`, `#privacyModal` seçicilerini veriyor; güncel uygulama bunları ekran render fonksiyonlarıyla açıyor. | Test adımları güncel DOM ile tekrarlanamaz. |
| R-04 | 8/8 başarılı test ve kesin milisaniye değerleri verilmiş fakat cihaz, tarayıcı, ağ, commit, ölçüm komutu ve ham çıktı belirtilmemiş. | Sonuçlar tekrarlanabilir değil. |
| R-05 | Beş teknik düzeltmeden sonra “KVKK/COPPA tam uyumlu” olunacağı söylenmiş. | Hukuki uyum; ebeveyn onayı, veri minimizasyonu, saklama/silme süreleri, aydınlatma ve çocuk hakları gibi daha geniş bir inceleme gerektirir. |

## Videodaki hata ve talepler

### Genel uygulama davranışı

| ID | Zaman | Bulgu | Durum |
|---|---:|---|---|
| V-01 | 00:00–03:07 | Birçok oyunda içerik ekranın üstünde sıkışıyor; altta veya bazen üstte çok büyük boş alan kalıyor. Oyun alanı telefon ekranını dengeli doldurmuyor. | **ORTAK KABUK DÜZELTİLDİ** — iframe üst payı azaltıldı, Phaser sahnelerinin esnek yüksekliği etkinleştirildi; oyun-özel görsel kabul testleri sürüyor. |
| V-02 | 01:24–01:33 | Bazı oyunlarda aynı yönerge hem üstte hem oyun alanında tekrar ediyor. Özellikle Vagon Ekspresi örnek gösterilmiş. | **DÜZELTİLDİ VE TEST EDİLDİ** — üst kabuktaki ikinci yönerge kaldırıldı; m10 üzerinde tek yönerge doğrulandı. |
| V-03 | 00:27 | 3. sınıf ana ekranında “SAYMA” butonu görünüyor; bunun kaldırılması isteniyor. | **DÜZELTİLDİ** — SAYMA artık yalnızca 1. sınıfta gösteriliyor. |
| V-04 | 00:30–00:36 | Kişiselleştirme seçimleri “BİTTİ” denmeden hemen kaydoluyor; geri çıkınca eski görünüm geri gelmiyor. | **DÜZELTİLDİ VE TEST EDİLDİ** — taslak görünüm eklendi; BİTTİ kaydediyor, İptal/geri eski görünümü koruyor. |
| V-05 | 00:30–00:36 | Ses azaltıldığında sesin kısılmadığı/kapanmadığı belirtilmiş. | **DÜZELTİLDİ; CİHAZ TESTİ BEKLİYOR** — 0–100 seviye ayarı Web Speech, oyun efektleri, Android sistem TTS, hazır kayıt ve Piper motoruna bağlandı. Fiziksel Android cihazda ses yüksekliği kabul testi yapılmalı. |
| V-06 | 00:45 civarı | Arkadaş yarışması, karşı taraf gelmeden/yanıtlamadan başlıyor gibi görünüyor. | **ÜRÜN KARARI** — mevcut sistem canlı eşzamanlı yarış değil, sıralı meydan okuma: gönderen önce oynuyor, rakip sonra cevaplıyor. Canlı yarış isteniyorsa mimari değişir; yalnızca metin/akış sorunuysa bekleme ekranı yeterlidir. |

### Oyun bazlı bulgular

| ID | Zaman | Oyun | Raporda istenen değişiklik | Güncel durum |
|---|---:|---|---|---|
| G-01 | 00:00–00:15 | `m10` Parmak Canavarları / yakınındaki ilk ekran | Üst sıkışıklığı azalt, oyunu aşağı doğru yay. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — sahne mobil yüksekliği kullanıyor; parmak grupları ve cevap alanı çakışmadan görünüyor, doğru cevapla ilerleme doğrulandı. |
| G-02 | 00:21 | `h38` Plan Masası | Ekran gösterilmiş; açık bir yazılı hata cümlesi yok. Görsel olarak aynı dikey yerleşim sorunu incelenmeli. | **AÇIK HATA BULUNAMADI / GÖRSEL DOĞRULANDI** — 390×844 mobil görünümde pano, hedef kartı ve üç takvim kutusu birbirine çarpmadan tam sahneye yayılıyor. Kaynak kayıtta yazılı bir hata tarifi olmadığı için yeni kanıt gelirse yeniden açılmalı. |
| G-03 | 00:39 | `m11` Uzaylı Asansörü | Alt boşluğu kullan; karışık uzaylıları doğrudan asansör kabinine sürüklet; tam ekran yap. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — mobil bırakma olayını kesen sürükleme hatası giderildi; uzaylı kabine bırakılınca sayaç ilerliyor ve hedef tamamlanınca sonraki tura geçiliyor. |
| G-04 | 00:42–00:48 | Kimliği görüntüde görünmeyen toplama oyunu (`336 + 428`) | Alt taraftaki büyük boşluğu kaldır, sahneyi tam yüksekliğe yay. | **YENİDEN ÜRET; önce oyun kimliği bulunmalı** |
| G-05 | 00:51–00:57 | `m14` Sihirli Olta / `m15` Şipşak Hafıza çevresi | Gerçek olta görünümü kullan; gereksiz emoji kalabalığını azalt; perde/oyun sahnesini tam ekrana yay. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — olta emojisi çizimli olta gövdesiyle değiştirildi, balığın oltayla yakalanması çalışıyor; hafıza önizlemesi mobil sahneye taşmadan yayılıyor. |
| G-06 | 00:57–01:00 | `m16` Orman Maratonu | Tek turda kalma/ilerlememe; üç tura çıkar ve boş alanı doldur. | **DÜZELTİLDİ VE TEST EDİLDİ** — üç farklı sıra sorusu, toplam 600 puan ve üçüncü turda bitiş doğrulandı. |
| G-07 | 01:03–01:09 | `m17` Uzaylı Apartmanı | Katları yatay değil dikey üst üste çiz; her katta uzaylı göster; işaretlenen ölü alanı kaldır. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — beş kat yukarıdan aşağıya dikey apartman olarak çizildi, her kata uzaylı eklendi ve paket doğru kata bırakıldı. |
| G-08 | 01:12–01:18 | `m18` Dondurma Kulesi | Külah üzerinde dikey yuvalar oluştur; topları sürükleyip sırayla yuvalara bırak. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — üç dikey yuva külahla görsel olarak birleştirildi; topların doğru yuvalara sürüklenmesi mobil boyutta doğrulandı. |
| G-09 | 01:18–01:24 | `m19` Otobüs Durakları | Alt boşluğu kaldır; tek tur yerine üç tur yap. | **DÜZELTİLDİ VE TEST EDİLDİ** — üç farklı durak sorusu, toplam 600 puan ve üçüncü turda bitiş doğrulandı. |
| G-10 | 01:21–01:27 | `m20` Şampiyonlar Kürsüsü | 1–2–3 kürsüleri üst arayüzle çakışıyor; aşağı taşı ve sahneyi büyüt. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — üç geniş kürsü alt sahnede çakışmadan görünüyor; yarışmacının birinci kürsüye sürüklenmesi ve puan ilerlemesi doğrulandı. |
| G-11 | 01:24–01:30 | `m21` Vagon Ekspresi | Tekrarlanan yönergeyi kaldır; puan/canları yeniden konumlandır; zürafayı gerçek üçüncü vagona sürüklet; boşluğu kullan. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — tek yönerge bandı, yatay lokomotif-vagon sahnesi ve zürafanın gerçek üçüncü vagona bırakılması mobil boyutta doğrulandı. |
| G-12 | 01:30–01:33 | `m22` Gökyüzü Asansörü | Oyunu dikeyde tam ekran yap. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — asansör sahnesi mobil yüksekliği kullanıyor ve kat göstergesindeki koyu temada görünmeyen sayı düzeltilerek doğrulandı. |
| G-13 | 01:33–01:39 | `m23` Obur Canavarın Tabakları | Tabakları tam ekrana yay; cevabı tabağa doğrudan dokunarak ver; işaretli ek alanları kaldır. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — yinelenen alt cevap kartları kaldırıldı; üç büyük tabak tek seçim yüzeyi oldu ve doğru tabağa doğrudan dokunma doğrulandı. |
| G-14 | 01:39–01:45 | `m24` Adalet Terazisi | “SOL KEFE” gibi gereksiz alanı kaldır; teraziyi büyüt; elmayı kefeye sürüklenebilir yap. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — ayrı hedef kutusu kaldırıldı; kesikli hedef gerçek kefe üzerine alındı ve iki elmanın kefeye bırakılmasıyla 5↔5 dengesi doğrulandı. |
| G-15 | 01:48–01:54 | `m25` İkiz Kardeşlerin Sepetleri | İki ayrı sepet/kutu göster; dördüncü emojiden sonraki eksik nesneleri düzelt. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — iki ayrı saplı sepet içinde onar nesne eksiksiz çizildi; yedi farklı çiftin dokunularak tamamlanması doğrulandı. |
| G-16 | 01:57–02:03 | `m26` Uzay Üssü Geri Sayımı | Çizimdeki rampa düzenine yaklaştır; sayıları doğru konumlara sürükleyerek geri sayma etkileşimi kur. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — geri say düğmesi kaldırıldı; her sıradaki sayı kartı roket rampasına sürükleniyor ve 10’dan 1’e ilk turun tamamlanıp ikinci tura geçmesi doğrulandı. |
| G-17 | 02:06–02:15 | `m28` Yeraltı Madencisi | Sahneyi tam ekran yap; kazanırken düz metin yerine mücevher/ödül animasyonu göster. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — maden asansörü mobil sahneyi dolduruyor; doğru kata inişte mücevher ve parıltı ödül animasyonu oynuyor. |
| G-18 | 02:15–02:21 | `m27` Zıpzıp Kurbağa | 10'a dokununca kurbağa 10 taşına zıplasın; yanlış seçenek gri olup cevabı ele vermesin; 12 ve 17 gibi iki makul çeldirici kullan. | **DÜZELTİLDİ VE TEST EDİLDİ** — oyun özel `roket` motorundaki kurbağa sahnesine bağlı; 12/17 aynı görsel dilde ve kurbağanın 5 ile 10 taşlarına zıplaması tarayıcıda doğrulandı. |
| G-19 | 02:21–02:27 | `m29` Büyülü Orman Yolu | Üst boşluğu kaldır; tek tur yerine üç tur yap. | **DÜZELTİLDİ VE TEST EDİLDİ** — 3-4-5, 4-5-6 ve 3-5-7 çokgen örüntüleri üçüncü turdan sonra bitiyor. |
| G-20 | 02:27–02:33 | `m30` Uzaylı Merdiveni | Tek tur yerine üç tur; oyunu aşağı doğru büyüt ve işaretli sıkışıklıkları gider. | **DÜZELTİLDİ VE TEST EDİLDİ** — +2, +3 ve +5 örüntüleri, puan aktarımı ve üçüncü tur bitişi doğrulandı. |
| G-21 | 02:33–02:39 | `m31` Eriyen Kardan Adam | Basit kart görünümü yerine çizimdeki katmanlı/kademeli kardan adam sahnesine yaklaştır. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — basit emoji yerine üç gövdeli, şapkalı ve kollu katmanlı kardan adam çizildi; doğru cevapta yeniden tamamlanma animasyonu doğrulandı. |
| G-22 | 02:39–02:57 | `m33` Örüntü Treni ve Eksik Vagon | Treni büyüt; etkileşimi “vagonu kancaya sürükle” yerine “kancayı vagona götür” olarak değiştir; bitince metin yerine tren hareket animasyonu oynat. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — tek kanca doğru vagon seçeneğine sürükleniyor; doğru eşleşmede trenin sağa hareket ederek sahneden çıkması doğrulandı. |
| G-23 | 02:57–03:07 | `m34` Hızlı Tahminci Karınca | Oyunu büyüt; yaprak kümelerini tek yaprak gibi görünmeyecek biçimde tek tek çiz; seçenekleri `< 5`, `= 5`, `> 5` yap; bitişte yaprak düşme animasyonu göster. | **ÇÖZÜLDÜ / TARAYICIDA DOĞRULANDI** — yapraklar ayrı büyük nesneler halinde çizildi, üç karşılaştırma etiketi korundu ve doğru cevapta yaprak düşme animasyonu oynadı. |

## Ortak kök nedenler

1. **Oyun kabuğu/viewport standardı yok:** Her motor farklı yükseklik, üst bar ve alt boşluk kullanıyor. Tek tek CSS yamaları yerine ortak güvenli alan ve ölçekleme kuralı gerekiyor.
2. **Katalog ile gerçek oyun motoru ayrışıyor:** Katalogda tek turlu tanım dururken bazı kimlikler özel üç turlu HTML'e yönleniyor, bazıları genel motora düşüyor. Test hangi motorun açıldığını kaydetmeli.
3. **Etkileşim standardı tutarsız:** Benzer öğrenme hedefleri bazen düğme, bazen dokunma, bazen sürükleme kullanıyor. Pedagojik kabul ölçütü oyun başına yazılmalı.
4. **Bitiş geri bildirimi çoğunlukla metin ağırlıklı:** Videoda hareketli, nesneyle ilişkili ödül animasyonları isteniyor.
5. **Sunucu istemci skoruna güveniyor:** Yarışma güvenliği yalnızca hız limitiyle değil, sunucu doğrulaması ve tekrar saldırısı önleme ile çözülmeli.
6. **PWA/çevrimdışı katmanı tamamlanmamış:** Manifest var; service worker/asset cache ve güvenilir senkron kuyruğu yok.

## Çözüm roadmap'i

### Aşama 0 — Güncel sürümde yeniden üretim ve kabul listesi (0,5–1 gün)

1. `b8c1227` için web ve Android test build'ini sabitle; rapora commit, cihaz, tarayıcı ve viewport ekle.
2. Video maddelerini 390×844, 412×915 ve masaüstünde aç; her maddeyi `Açık / Düzelmiş / Ürün kararı` olarak işaretle.
3. Açılan her oyunda gerçek motor URL'sini, tur sayısını ve ekran kaydını sakla.
4. Kimliği belirsiz `336+428` oyunu ve m14/m15 çevresindeki balık/perde akışını kesin kimliğe bağla.

**Çıkış ölçütü:** Her satırın güncel build'de kanıtı ve tek cümlelik kabul kriteri bulunur.

### Aşama 1 — Güvenlik ve veri bütünlüğü (2–4 gün)

1. `contest_submit`, `duel_create`, `duel_respond` ve `message_send` için kullanıcı+IP bazlı hız sınırı ekle.
2. Yarışma/düello skorunu istemciden körlemesine kabul etmeyi bırak: sunucu oturum kimliği, oyun/seed, soru sayısı, geçerli skor üst sınırı, süre ve tekrar gönderim anahtarı doğrulasın.
3. Bearer token'ı `localStorage` yerine `HttpOnly; Secure; SameSite` cookie oturumuna taşı; cookie kullanıldığı için CSRF savunmasını da aynı değişiklikte tasarla.
4. Hazır mesaj allowlist'ini koru; çıktı kodlama ve yetkilendirme testleri ekle. Serbest mesaj yokken NLP filtresi ekleme.

**Çıkış ölçütü:** Sahte yüksek skor, hızlı tekrar, başkasının düellosuna yanıt ve token okuma senaryoları başarısız olur.

### Aşama 2 — PWA ve çevrimdışı dayanıklılık (2–3 gün)

1. Statik ve sürümlü `manifest.webmanifest` + `sw.js` oluştur; uygulama kabuğu ve gerekli Phaser varlıkları için cache stratejisi tanımla.
2. Profil/ilerleme yazımlarını IndexedDB kuyruğuna al; bağlantı gelince otomatik tekrar, exponential backoff ve idempotency uygula.
3. Kullanıcıya `çevrimdışı`, `senkron bekliyor`, `senkronlandı`, `çakışma` durumlarını açıkça göster.

**Çıkış ölçütü:** Uçak modunda tamamlanan oyun, uygulama kapanıp açılsa da kalır ve bağlantı geri gelince yalnızca bir kez MySQL'e yazılır.

### Aşama 3 — Ortak oyun kabuğu ve uygulama ayarları (2–3 gün)

1. Phaser oyunları için ortak `min-height`, safe-area, başlık/ilerleme alanı ve responsive canvas kuralı oluştur.
2. Yönergeyi tek kaynakta göster; puan/can/geri düğmesi için sabit bölgeler tanımla.
3. Kişiselleştirmede taslak kopya kullan: `BİTTİ = kaydet`, geri/iptal = eski görünümü geri yükle.
4. Ses için açık/kapalıya ek gerçek seviye kontrolü getir; Web Speech, Android TTS ve efekt seslerine aynı tercihi uygula.
5. 3. sınıf menüsündeki SAYMA kararını uygula; kaldırılacaksa sınıfa göre menü konfigürasyonuna taşı.

**Çıkış ölçütü:** Hedef telefonlarda oyun kontrolleri kesilmez, gereksiz ölü alan kalmaz, yönerge tekrarlanmaz ve BİTTİ/İptal doğru çalışır.

### Aşama 4 — Oyun mekanikleri: işlev önce (3–5 gün)

1. **Tur/ilerleme grubu:** `m16`, `m19`, `m29`, `m30` gerçekten üç farklı tur oynatmalı ve üçüncü turdan sonra bitmeli.
2. **Sürükleme/dokunma grubu:** `m11`, `m17`, `m18`, `m21`, `m23`, `m24`, `m26`, `m27`, `m33` videodaki beklenen doğrudan nesne etkileşimine geçirilmeli.
3. **İçerik/doğru ipucu grubu:** `m25` eksik nesneler, `m27` cevabı ele veren gri seçenek ve `m34` tek yaprak gibi okunan kümeler düzeltilmeli.
4. Yarışma için ürün kararı uygulanmalı: sıralı meydan okuma korunacaksa “rakip daha sonra oynayacak” açıklaması; canlı yarış isteniyorsa hazır/katıldı durum makinesi ve gerçek zamanlı kanal.

**Çıkış ölçütü:** Her oyunun otomatik veya kayıtlı manuel testi; üç tur, doğru/yanlış akışı, sürükle-bırak hedefi ve tamamlanma kaydı üzerinden geçer.

### Aşama 5 — Görsel kalite ve ödül animasyonları (2–4 gün)

1. `m17`, `m20`, `m21`, `m22`, `m24`, `m31` sahnelerini çizimli beklentiye göre yeniden dengele.
2. `m28` mücevher, `m27` kurbağa zıplaması, `m33` tren hareketi, `m34` yaprak düşmesi gibi bağlamsal bitiş animasyonlarını ekle.
3. Emoji kalabalığını azalt; eğitim nesnelerini net SVG/Phaser çizimleriyle ayır.

**Çıkış ölçütü:** Önce/sonra ekran görüntüsü karşılaştırmasında her hedef viewport'ta sahne okunaklı ve dengeli görünür.

### Aşama 6 — Regresyon, yayın ve raporun yenilenmesi (1–2 gün)

1. Web, PWA ve Android için smoke test; giriş/kayıt, öğretmen bağlantısı, çevrimdışı ilerleme, yarışma ve seçili oyun matrisi.
2. API kötüye kullanım testleri, XSS/output encoding kontrolü ve veri silme/oturum sonlandırma testleri.
3. PDF'yi gerçek sürüm/commit, ölçüm yöntemi, çalışan ekran görüntüleri ve kanıt bağlantılarıyla yeniden üret.
4. Yayın öncesi yedek, migration ve rollback adımlarını yaz.

**Çıkış ölçütü:** Açık kritik/yüksek hata yok; orta/düşük kalanlar bilinen sorun listesinde; kurulum ve rollback prova edilmiş.

## Önerilen debug başlangıç sırası

1. `P-04` sahte skor + rate limit — veri bütünlüğü ve yarışma güveni.
2. `P-05` çevrimdışı kuyruk — çocuk ilerlemesinin kaybolmasını önleme.
3. `V-04` kişiselleştirme BİTTİ/İptal — küçük kapsamlı, net ve kolay doğrulanabilir ilk UI düzeltmesi.
4. `V-01/V-02` ortak oyun kabuğu — çok sayıda oyunu tek seferde iyileştirir.
5. `m16/m19/m29/m30` tur hataları, ardından sürükleme ve görsel oyun paketleri.
6. `P-01` cookie oturumu — kapsamı geniş olduğu için testleri hazırlandıktan sonra kontrollü migration.

Bu belge ilk incelemeyle oluşturulmuş, aynı gün başlayan debug çalışmasının gerçekleşen durumlarıyla güncellenmiştir. “Düzeltildi” işaretli maddeler yerel kaynakta ve Android varlık aynasında bulunur; canlı sunucuya yayın ayrı bir adımdır.
