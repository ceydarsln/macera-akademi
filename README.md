# Macera Akademi

Macera Akademi, 1–4. sınıf düzeyleri için 658 müfredat oyunu içeren bir eğitim uygulamasıdır. Ana uygulama tek sayfalık bir web uygulaması olarak çalışır; Android ve iOS tarafında WebView ile paketlenir. Web yayını hesap ve ilerleme verilerini PHP API üzerinden MySQL'de saklar.

## Mevcut durum

- Sürüm: `2.8-test` (`versionCode 20`)
- Toplam oyun: 658
- Phaser motorunda çalışan: 657
- DOM motorunda çalışan: 1 (`v40`)
- Otomatik oynanabilen mekanik kapsamı: 658 / 658
- Android minimum sürüm: API 23
- Ses sırası: hazır Chatterbox kaydı → Piper → sistem TTS

Bu depo, 22 Ağustos 2026 tarihli devir paketinin ve aynı tarihteki canlı Android projesinin doğrulanmış birleşimidir. Ana HTML'nin kaynak kopyası ile Android varlık kopyası başlangıç noktasında SHA-256 düzeyinde aynıdır.

## Dizinler

```text
app/                    Android uygulaması
web/macera-akademi.html Ana uygulama ve oyun kataloğu için tek kaynak
web/api-client.js       PHP/MySQL API istemcisi
web/api/                Güvenli hesap ve oyun API'si
web/database/schema.sql MySQL şeması
web/phaser/             Phaser şablonlarının kaynak sürümleri
tools/                  Eşleme ve otomatik oyun testleri
tools/audio/            Chatterbox manifesti ve üretim araçları
docs/history/           Geçmiş devir notları ve oturum kayıtları
```

`app/src/main/assets/` altındaki web dosyaları Android derleme girdisidir. Bunlar `web/` kaynaklarından aşağıdaki komutla yenilenir:

```bash
./tools/aynala.sh
```

## Web sunucusuna kurulum

Sunucuda PHP 7.4+ ve `pdo_mysql` gereklidir. Depo klonlandıktan sonra:

```bash
./tools/aynala.sh
cp web/api/config.sample.php web/api/config.local.php
```

MySQL'de boş bir veritabanı oluşturup `web/database/schema.sql` dosyasını içe aktarın. Ardından `config.local.php` içine yalnızca sunucudaki gerçek bağlantı bilgilerini yazın ve web sunucusunun document root'unu `web/` klasörüne yönlendirin. Ayrıntılı kontrol listesi [YAYIN_KURULUMU.md](YAYIN_KURULUMU.md) dosyasındadır.

`config.local.php` Git'e eklenmez. Canlı ortam HTTPS olmadan kullanılmamalıdır.

## Debug APK derleme

```bash
JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home" ./gradlew assembleDebug
```

Çıktı `app/build/outputs/apk/debug/app-debug.apk` altında oluşur.

## Birleşik test koşucusu

Bir oyunun yalnızca açılması başarı sayılmaz. Oyun doğru girdilerle baştan sona oynanmalı ve üst uygulamadaki `completeGame` çağrısı gözlenmelidir.

Yerel sunucuyu başlat:

```bash
python3 tools/test_server.py
```

Sunucunun yazdırdığı uygulama adresini aç. Tarayıcı geliştirici konsolunda birleşik koşucuyu yükle:

```js
await (0,eval)(await (await fetch('/tools/macera_test.js')).text())
```

Tüm katalogdaki mekanik ve anlam denetimlerini başlat:

```js
await MACERA_TEST.baslat()
MACERA_TEST.durum()
await MACERA_TEST.bekle()
MACERA_TEST.ozet()
```

`macera_test.js`, genel mekanikler için `kosum.js`, özel Phaser ve DOM mekanikleri için `ucuncu_sinama.js` ve içerik denetimi için `anlam_denetimi.js` araçlarını tek API altında yönlendirir. Raporlar varsayılan olarak `test-results/macera-test-*.json` altında saklanır. Otomatik oyuncusu olmayan oyunlar sessizce atlanmaz; raporda `DESTEKLENMİYOR` olarak görünür.

Tarayıcı konsolu açmadan seçili oyunları veya bir sınıfı çalıştırmak için yerel test sunucusunda `tools/test-harness.html` kullanılabilir:

```text
http://127.0.0.1:8871/tools/test-harness.html?grade=2&anlam=1
http://127.0.0.1:8871/tools/test-harness.html?ids=m06,u03,v40&anlam=1
```

## Son doğrulama — 22 Ağustos 2026

- `fractionCut`, `clockSet`, `moneyBuild`, `placeValueLoad`, `drawSegments` ve `solidScan` kullanan 16 oyun canlı Phaser köprüsünde baştan sona oynandı: **16 / 16 TAMAM**.
- Önceden desteklenmeyen 80 oyun için 14 Phaser mekanik ailesine ve `v40` DOM grafiğine otomatik oyuncular eklendi; bu grup baştan sona **80 / 80 TAMAM** sonuç verdi.
- Paylaşılan `orderSequence` yolu son sürümde yeniden tarandı: toplu turdaki 59 oyun ve özel `m03` yeniden koşusu birlikte **60 / 60 TAMAM**.
- Dört sınıfın 658 oyunluk mekanik ve anlam regresyonu tamamlandı. Uzun oturum raporları ile kaynak sınırına takılan kayıtların küçük-grup yeniden koşuları birlikte **658 / 658 TAMAM · 0 desteklenmeyen · 0 anlam bulgusu** verdi.
- Test koşucusu her oyun geçişinde eski Phaser/WebGL örneğini kapatacak şekilde düzeltildi; yüzlerce oyunluk taramalarda renderer bağlamı birikmiyor.
- Android `assembleDebug` derlemesi başarıyla tamamlandı.
- Anlam denetimindeki 20 kayıt tek tek incelendi: 12 tek-soruluk Türkçe oyunu üçer soruya çıkarıldı, görsel sahnelerden kaynaklanan yanlış pozitif kurallar düzeltildi ve yeniden koşuda **20 / 20 TAMAM · 0 anlam bulgusu** alındı.

## Bilinen açıklar

- `v40` HTML tabanlı özel grafiği nedeniyle bilinçli olarak DOM motorundadır.
- Chatterbox kayıt üretimi tamamlanmadan Piper kaldırılmamalıdır.
- İmzalı AAB, gizlilik politikası ve Play Store varlıkları henüz hazırlanmamıştır.

Geçmiş devir belgeleri bağlam ve kanıt olarak tutulur; güncel çalışma talimatı olarak `README.md`, kaynak kod ve doğrulanmış test sonuçları esas alınır.
