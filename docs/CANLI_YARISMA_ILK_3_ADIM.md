# Canlı yarışma: 1–6. adımların uygulama ve kabul durumu

Eski **sonradan oynanan** `duels` ve öğretmen yarışmaları yerinde durur. Arkadaşlar için ayrı bir **eşzamanlı** maç akışı eklendi. Aşağıdaki “uygulandı” ifadesi üretim sunucusunda/gerçek iki cihazda kabul edildiği anlamına gelmez.

## 1–3: sunucu temeli

- Durumlar: `invited` → `lobby` → `countdown` → `playing` → `finished`; ayrıca `declined`, `cancelled`, `expired`. Davet 60 sn, lobi 120 sn, ortak geri sayım 3 sn, 8 soru × 12 sn.
- Yalnızca kabul edilmiş, **aynı sınıftaki** arkadaşlar davet edebilir. Bir oyuncunun birden fazla aktif canlı maçı olamaz.
- Soru seti, doğru seçenek ve puan sunucudadır. `live_state` yalnızca açık soruyu ve dört seçeneği verir; `live_answer` tek cevap ve sunucu zaman penceresi kuralını uygular. İstemciden gelen skor/doğruluk kabul edilmez.
- `live_matches`, `live_match_answers`, `live_match_claims` tabloları yeni kurulum için `web/database/schema.sql`, mevcut kurulum için `web/database/migrations/2026-09-30-live-matches.sql` içindedir.

## 4: canlı ekranlar

`web/macera-akademi.html` ve `web/api-client.js` içinde arena davetleri, kabul/ret, iki tarafın hazır durumu, ortak sayaç, eşzamanlı soru, skor, sonuç, cevap özeti ve ödül ekranı bağlandı. Aynı arkadaş için eski “sonradan oyna” seçeneği korundu. Android WebView'e aynı iki dosyanın kopyası kondu; iOS projesi de bu kopyaları uygulama kaynağı olarak paketliyor.

## 5: kopma, çıkış, yeniden bağlanma

- Açık maç yerel olarak hatırlanır; oturum doğrulaması bitince yeniden açılır. Görünür ekranda yaklaşık saniyede bir durum alınır. Telefon arka plandayken istek yapılmaz; geri dönünce hemen güncellenir.
- Oyuncu en son ne zaman görüldüğüyle sunucuda izlenir. Oyun başladıktan sonra **20 saniye** boyunca dönmeyen oyuncu hükmen kaybeder; ikisi de dönmezse maç iptal olur. Geri sayım sırasında ayrılma yalnızca iptaldir, ödüllü galibiyet değildir.
- Çıkış öncesi açık onay gösterilir. Bekleme/davet aşamasında iptal/ret, oyun başladıktan sonra hükmen sonuç uygulanır. Maç bitişinden sonra otomatik ödül alınmaz; oyuncu “Ödülümü Al” der.

## 6: sonuç ve ödül güvenliği

- Sunucu yalnızca bitmiş maç için XP/altın yazar. Sonuç başına taban ödül, 8/8 bonusu ve üç galibiyet serisi mevcut ödül rakamlarıyla uyumludur. Oyunu terk eden oyuncu 0 XP/altın alır.
- `live_match_claims` birincil anahtarı ve kullanıcı/maç kilitli işlem aynı ödülün iki kez yazılmasını engeller. Tekrar istek önceki ödülü ve güncel profili döndürür.
- Arayüz profil ve yerel önbelleği sunucu yanıtıyla yeniler. Genel `save_profile`, kilitli güncel kayıtla karşılaştırıp daha az kazanılmış altın/maç sayısı taşıyan eski kuyruğun XP, altın ve yarışma istatistiklerini ezmesini engeller. Genel profil sistemi tam sürüm/çakışma denetimli değildir; üretim öncesi gerçek sunucuda yarışma ödülü ile çevrimdışı kayıt yarışını ayrıca sınayın.

## Çalıştırılan kontroller ve kalan kabul

- `tools/test_live_ui.cjs`: iki **izole tarayıcı oturumu** ile davet → kabul → hazır → sekiz ortak soru/cevap → iki sonuç → ödül, maç ekranını yeniden açma ve ikinci ödül isteği senaryosu. Telefon ölçüsündeki ekran görüntüleri `artifacts/canli-yarisma-inceleme/` içindedir. Bu test API taklidi ve hızlandırılmış soru geçişi kullanır; gerçek PHP/MySQL testi değildir.
- Android `:app:assembleDebug --offline` ve iOS kod imzasız `iphoneos` Debug derlemesi başarılı. Bunlar gerçek cihaz oynanışını doğrulamaz.
- `tools/test_live_match_questions.php`: XAMPP PHP 8.2.4 ile kategori/sınıf soru üretimi 960/960 geçti (6 Ekim). Bu, MySQL maç entegrasyon testi değildir.
- Üretime almadan önce veritabanını yedekleyip migrasyonu bir kez uygula; iki gerçek hesap/cihazla davet, geç/çift cevap, 20 sn kopma, çıkış, uygulama kapanıp açılma, iki tarafta sonuç, çift ödül ve farklı sınıf reddini sınayın. Yerel PHP soru testi canlı MySQL entegrasyonu veya aşağıdaki cihaz ön testinin yerini almaz.

## 3 Ekim 2026: gerçek Android ön testi

- Samsung SM-A065F USB hata ayıklama ile bağlandı. Ana `com.maceraakademi.app` paketine dokunulmadı; ayrı `com.maceraakademi.app.test` paketi `adb install -r` ile güncellendi ve açıldı.
- Açılış, Yarışma arenası, Toplama kategorisinin dokunma tepkisi ve Android geri tuşuyla ana ekrana dönüş cihazda geçti. Görseller `artifacts/canli-yarisma-cihaz/` altında.
- Üretim API sağlık isteği MySQL bağlantısı için `ok:true` döndürdü. Bu, canlı maç tablolarının yüklenmiş olduğunu veya canlı maçın çalıştığını **kanıtlamaz**.
- Telefonda şu an misafir profili açık olduğu için canlı arkadaş maçı oluşturulamadı. Gerçek iki hesaplı davet, sekiz soru, kopma/yeniden bağlanma ve ödül yazımı hâlâ doğrulanmadı; ikinci oyuncu ve giriş gerektirir.

## 5 Ekim 2026: telefonsuz web kontrolü

- İki bağımsız Chrome oturumuyla yerel web testini tekrar çalıştırdık: davet, kabul, iki tarafın hazır olması, sekiz soru, sonuç ve tek seferlik ödül başarılı. Bu testin API katmanı taklittir; gerçek sunucu testi değildir.
- Yayındaki `https://maceraakademi.com.tr/` ve `api-client.js` dosyalarında canlı yarışma kodu yok; `https://maceraakademi.com.tr/api/live.php` HTTP 404 dönüyor. Dolayısıyla yereldeki özellik üretime henüz yüklenmemiş ve gerçek iki hesapla web maçı şu anda denenemez.
- O gün PHP çalıştırıcısı sistem PATH'inde bulunamamıştı. `web/api-client.js` sözdizimi, Android'e kopyalanan web dosyalarının birebir eşliği ve `git diff --check` geçti. PHP/MySQL entegrasyonu, veritabanı migrasyonu ve iki gerçek hesaplı üretim kabulü açık kaldı.

## 6 Ekim 2026: iPad ve yayın ön kontrolü

- iPad (A16), iOS 26.5 simülatöründe güncel Debug derlemesi kuruldu ve açıldı. Misafir sınıf seçimi, karakter oluşturma, arkadaşlar ve yarışma arenası ekranları çalıştı. Tabletin iki yanındaki koyu bantlar arka planla uyumlu hale getirildi; gerçek iPad ses kalitesi ve tam oyun oynanışı bu simülatör kontrolüyle kanıtlanmaz.
- Web sitesi HTTP 200, üretim API'si MySQL sağlık yanıtında `ok:true` döndürdü; fakat `api/live.php` 404. Yerelde iki oturumlu sekiz soruluk arayüz testi yine geçti. Canlı yarışma henüz üretimde değil.
- GitHub `main` dalı `b8c1227` sürümünde; yerel yarışma dosyaları ve veritabanı geçişi commit edilmemiş. Sunucuda otomatik dağıtım yapılandırması yok; yalnız GitHub'a kod göndermek canlı siteyi değiştirmez. Veritabanı yedeği/geçişi ve sunucu dağıtımı için erişim yöntemi belirlenmelidir.
- XAMPP içindeki PHP 8.2.4 bulundu. Sözdizimi taraması geçti; soru üretimi testi önce noktalama kategorisinde `«$sentence»` değişken yorumlama hatası yakaladı. `«{$sentence}»` yapılarak düzeltildi. Ayrıca 1. sınıf sayılarında yanlışlıkla 21–98 arası onlar basamağı sorusu üretilebildiği görüldü; bu sınıf için 11–19 arası birler basamağı sorusuna çevrildi. Teste iki koruma eklendi ve 960 kategori/sınıf örneği uyarısız geçti. Yerel MySQL maç testi aşağıda yapıldı; canlı yayındaki iki hesaplı sınama hâlâ açık.

## 6 Ekim 2026: gerçek yerel PHP/MySQL maç kabulü

- Üretimden ayrı, yalnız `127.0.0.1` üzerinde çalışan geçici XAMPP PHP ve MariaDB kuruldu. `tools/test_live_server.cjs` iki geçici hesabı API üzerinden oluşturdu; arkadaşlık, davet, kabul, hazır olma ve sunucu saatine göre açılan **sekiz sorunun tamamı** gerçek HTTP/MySQL işlemleriyle geçti. Bir oyuncu 8 doğru, diğeri 8 yanlış verdi; kazanan ve skor sunucuda doğru oluştu.
- Geçersiz seçenek, aynı soruya ikinci cevap ve süresi geçmiş soruya cevap reddedildi. Kazananın ödül talebi ilk seferde yazıldı, ikinci istekte yeniden yazılmadı; kaybedenin ödülü ayrıca doğrulandı. Bu, önceki API taklitli arayüz testinden farklı olarak gerçek yerel backend testidir.
- Ayrı bir geçici veritabanına mevcut commit'teki eski `schema.sql` yüklendi ve `2026-09-30-live-matches.sql` migrasyonu uygulanınca üç canlı yarışma tablosu oluştu. Üretim veritabanına dokunulmadı.
- Açık işler: üretim veritabanı yedeği ve migrasyon, web dosyalarının sunucuya dağıtımı, iki gerçek cihaz/hesapla bağlantı-kopma-ses kabulü. Yerel başarılı test yayındaki sitenin güncellendiği anlamına gelmez.
