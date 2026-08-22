# Kurulum ve geliştirme

## Gereksinimler

- macOS üzerinde Android Studio
- Android SDK 34
- Android Studio ile gelen JDK 17 veya daha yeni uyumlu JBR

`local.properties` makineye özeldir ve Git'e eklenmez. Android Studio projeyi ilk açtığında SDK yolunu bu dosyaya yazar.

## Kaynakları Android varlıklarına eşleme

Ana uygulama kaynağı `web/macera-akademi.html`, Phaser şablonları ise `web/phaser/` altındadır. Android derlemesinden önce çalıştır:

```bash
./tools/aynala.sh
```

Betik Phaser CDN bağlantılarını yerel `phaser.min.js` dosyasına çevirir, `svgciz.js` için önbellek damgası ekler ve kaynakları `app/src/main/assets/` altına kopyalar.

## Debug APK

```bash
JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home" ./gradlew assembleDebug
```

Çıktı:

```text
app/build/outputs/apk/debug/app-debug.apk
```

## Yerel web testi

Depo kökünde basit bir HTTP sunucusu başlat:

```bash
python3 -m http.server 8870
```

Ardından tarayıcıda şu adresi aç:

```text
http://localhost:8870/app/src/main/assets/macera-akademi.html
```

Otomatik testler oyunu yalnız açmakla yetinmez; doğru girdilerle baştan sona oynayıp `completeGame` çağrısını doğrular. Test araçları `tools/` altındadır.

## Ses üretimi

Manifest `tools/audio/manifest.json` dosyasındadır. Üretilen geçici OGG dosyaları `tools/audio/ses/` altında tutulur ve bu klasör Git tarafından yok sayılır. Kayıtların tamamı doğrulandıktan sonra:

```bash
./tools/audio/uygulamaya_kopyala.sh
```

Piper, tüm kayıtlar doğrulanmadan kaldırılmamalıdır. `piperi_cikar.sh` geçmiş oturumdan kalan yardımcıdır ve Android kodu elle düzenlenmeden tek başına kullanılmamalıdır.

## Geçmiş belgeler

Claude devir notları ve eski kurulum belgesi `docs/history/` altında korunur. Bunlar geçmiş bağlamdır; güncel kaynak ve test sonuçları önceliklidir.
