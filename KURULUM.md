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

Depo kökünde birleşik test sunucusunu başlat:

```bash
python3 tools/test_server.py
```

Ardından tarayıcıda şu adresi aç:

```text
http://127.0.0.1:8870/app/src/main/assets/macera-akademi.html
```

Bu adres oyunların statik kontrolü içindir. Hesap, arkadaşlık ve sınıf özelliklerinin uçtan uca testi için PHP + MySQL kurulumu gerekir; canlı sunucu adımları `YAYIN_KURULUMU.md` dosyasındadır.

Geliştirici konsolunda test araçlarını tek giriş noktasından yükle:

```js
await (0,eval)(await (await fetch('/tools/macera_test.js')).text())
```

Yaygın komutlar:

```js
await MACERA_TEST.baslat()                              // mekanik + anlam, tüm katalog
await MACERA_TEST.baslat({ sinif:1, ders:'math' })      // filtreli koşu
await MACERA_TEST.baslat({ idler:['m01','u04'] })       // seçili oyunlar
await MACERA_TEST.baslat({ kip:'anlam' })               // yalnız anlam denetimi
MACERA_TEST.durum()                                     // ilerleme
await MACERA_TEST.bekle()                               // tamamlanmış JSON nesnesi
MACERA_TEST.ozet()                                      // kısa metin özeti
MACERA_TEST.durdur()                                    // güvenli iptal isteği
```

Koşucu oyunu yalnız açmakla yetinmez; doğru girdilerle baştan sona oynayıp `completeGame` çağrısını doğrular. Sonuçlar `test-results/` altında tek JSON raporunda saklanır. Bu klasör Git tarafından izlenmez.

## Ses üretimi

Manifest `tools/audio/manifest.json` dosyasındadır. Üretilen geçici OGG dosyaları `tools/audio/ses/` altında tutulur ve bu klasör Git tarafından yok sayılır. Kayıtların tamamı doğrulandıktan sonra:

```bash
./tools/audio/uygulamaya_kopyala.sh
```

Piper, tüm kayıtlar doğrulanmadan kaldırılmamalıdır. `piperi_cikar.sh` geçmiş oturumdan kalan yardımcıdır ve Android kodu elle düzenlenmeden tek başına kullanılmamalıdır.

## Geçmiş belgeler

Geçmiş devir notları ve eski kurulum belgesi `docs/history/` altında korunur. Bunlar geçmiş bağlamdır; güncel kaynak ve test sonuçları önceliklidir.
