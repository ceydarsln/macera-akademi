# Macera Akademi

Macera Akademi, 1–4. sınıf düzeyleri için 658 müfredat oyunu içeren bir Android eğitim uygulamasıdır. Ana uygulama tek sayfalık bir web uygulaması olarak çalışır ve Android tarafında WebView ile paketlenir.

## Mevcut durum

- Sürüm: `2.8-test` (`versionCode 20`)
- Toplam oyun: 658
- Phaser motorunda çalışan: 641
- DOM motorunda çalışan: 17
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

## Test ölçütü

Bir oyunun yalnızca açılması başarı sayılmaz. Oyun doğru girdilerle baştan sona oynanmalı ve üst uygulamadaki `completeGame` çağrısı gözlenmelidir. Mevcut koşucular:

- `tools/kosum.js`
- `tools/ucuncu_sinama.js`
- `tools/anlam_denetimi.js`

Koşucuların tek çatı altında birleştirilmesi ve sonuçların JSON olarak saklanması devam eden ilk altyapı işidir.

## Bilinen açıklar

- `fractionCut` ve `clockSet` için `kesirsaat` şablonu hazır fakat doğrulanmamıştır.
- `moneyBuild`/`placeValueLoad` için `para`, `drawSegments`/`solidScan` için `geometri` şablonları henüz canlı katalog köprüsüne dönüştürülmemiştir.
- `v40` HTML tabanlı özel grafiği nedeniyle bilinçli olarak DOM motorundadır.
- Chatterbox kayıt üretimi tamamlanmadan Piper kaldırılmamalıdır.
- İmzalı AAB, gizlilik politikası ve Play Store varlıkları henüz hazırlanmamıştır.

Geçmiş devir belgeleri bağlam ve kanıt olarak tutulur; güncel çalışma talimatı olarak `README.md`, kaynak kod ve doğrulanmış test sonuçları esas alınır.
