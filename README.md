# Macera Akademi

Macera Akademi, 1–4. sınıf düzeyleri için 658 müfredat oyunu içeren bir Android eğitim uygulamasıdır. Ana uygulama tek sayfalık bir web uygulaması olarak çalışır ve Android tarafında WebView ile paketlenir.

## Mevcut durum

- Sürüm: `2.8-test` (`versionCode 20`)
- Toplam oyun: 658
- Phaser motorunda çalışan: 657
- DOM motorunda çalışan: 1 (`v40`)
- Otomatik oynanabilen mekanik kapsamı: 578 / 658
- Android minimum sürüm: API 23
- Ses sırası: hazır Chatterbox kaydı → Piper → sistem TTS

Bu depo, 22 Ağustos 2026 tarihli devir paketinin ve aynı tarihteki canlı Android projesinin doğrulanmış birleşimidir. Ana HTML'nin kaynak kopyası ile Android varlık kopyası başlangıç noktasında SHA-256 düzeyinde aynıdır.

## Dizinler

```text
app/                    Android uygulaması
web/macera-akademi.html Ana uygulama ve oyun kataloğu için tek kaynak
web/phaser/             Phaser şablonlarının kaynak sürümleri
tools/                  Eşleme ve otomatik oyun testleri
tools/audio/            Chatterbox manifesti ve üretim araçları
docs/history/           Claude devir notları ve geçmiş oturum kayıtları
```

`app/src/main/assets/` altındaki web dosyaları Android derleme girdisidir. Bunlar `web/` kaynaklarından aşağıdaki komutla yenilenir:

```bash
./tools/aynala.sh
```

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

`macera_test.js`, genel mekanikler için `kosum.js`, on beş özel mekanik için `ucuncu_sinama.js` ve içerik denetimi için `anlam_denetimi.js` araçlarını tek API altında yönlendirir. Raporlar varsayılan olarak `test-results/macera-test-*.json` altında saklanır. Otomatik oyuncusu olmayan oyunlar sessizce atlanmaz; raporda `DESTEKLENMİYOR` olarak görünür.

## Son doğrulama — 22 Ağustos 2026

- `fractionCut`, `clockSet`, `moneyBuild`, `placeValueLoad`, `drawSegments` ve `solidScan` kullanan 16 oyun canlı Phaser köprüsünde baştan sona oynandı: **16 / 16 TAMAM**.
- 658 oyunluk katalog dört sınıf grubunda tarandı. Otomatik oyuncusu bulunan 578 mekanik sonuç, tam tarama ve sorunlu kayıtların sakin tek-oturum yeniden koşuları birlikte değerlendirildiğinde tamamlandı; otomatik oyuncusu olmayan 80 kayıt açıkça `DESTEKLENMİYOR` olarak raporlandı.
- Paylaşılan `orderSequence` yolu son sürümde yeniden tarandı: toplu turdaki 59 oyun ve özel `m03` yeniden koşusu birlikte **60 / 60 TAMAM**.
- Android `assembleDebug` derlemesi başarıyla tamamlandı.
- Anlam denetiminde 20 içerik uyarısı kaldı; bunlar mekanik çökme değil, içerik derinliği/görsel ölçüt inceleme kuyruğudur.

## Bilinen açıklar

- 80 katalog oyunu için henüz otomatik oyuncu yoktur; birleşik raporda `DESTEKLENMİYOR` görünürler.
- Anlam denetiminin işaretlediği 20 içerik kaydı insan incelemesi beklemektedir.
- `v40` HTML tabanlı özel grafiği nedeniyle bilinçli olarak DOM motorundadır.
- Chatterbox kayıt üretimi tamamlanmadan Piper kaldırılmamalıdır.
- İmzalı AAB, gizlilik politikası ve Play Store varlıkları henüz hazırlanmamıştır.

Geçmiş devir belgeleri bağlam ve kanıt olarak tutulur; güncel çalışma talimatı olarak `README.md`, kaynak kod ve doğrulanmış test sonuçları esas alınır.
