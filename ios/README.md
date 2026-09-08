# Macera Akademi — iOS

Bu hedef, Android uygulamasındaki aynı `macera-akademi.html` ve `phaser/`
kaynaklarını iPhone/iPad üzerinde `WKWebView` içinde çalıştırır. Web içeriği
kopyalanmaz; Xcode derlerken Android hedefinin kullandığı güncel kaynakları
uygulama paketine ekler.

## Çalıştırma

1. `MaceraAkademi.xcodeproj` dosyasını Xcode ile açın.
2. Xcode isterse **Settings → Components** bölümünden iOS platformunu ve bir
   iPhone Simulator çalışma zamanını yükleyin.
3. `MaceraAkademi` hedefinde **Signing & Capabilities** bölümünden Apple
   geliştirici takımınızı seçin.
4. Bir iPhone simülatörü veya bağlı cihaz seçip **Run** düğmesine basın.

Komut satırından imzasız simülatör derlemesi:

```bash
xcodebuild -project ios/MaceraAkademi.xcodeproj \
  -scheme MaceraAkademi \
  -sdk iphonesimulator \
  -configuration Debug \
  CODE_SIGNING_ALLOWED=NO build
```

## iOS uyarlamaları

- JavaScript `AndroidTTS` arayüzü iOS'ta `AVSpeechSynthesizer` ile karşılanır.
- Yerel içerik özel `macera://` kaynağından sunulur; iframe'ler ve kalıcı web
  depolaması aynı köken altında çalışır.
- HTTP(S), telefon ve e-posta bağlantıları uygulamanın dışında açılır.
- Uygulama dikey yönde çalışır ve oyun sırasında ekranın kapanmasını engeller.
- iOS sistem sesi kullanıldığı için Android'e özgü Piper/ONNX dosyaları pakete
  eklenmez.

## App Store hazırlığı

`AppStore/` klasöründe Türkçe mağaza metinleri, gizlilik beyanı taslağı ve
yayımlanmaya hazır gizlilik politikası bulunur. `privacy-policy.html` dosyası
App Store Connect'e girilmeden önce herkese açık bir HTTPS adresinde
yayımlanmalıdır. Uygulamanın içindeki aynı politika karşılama, kayıt ve Ayarlar
ekranlarından açılabilir.

Uygulama hedefi, toplanan verileri ve takip yapılmadığını bildiren
`PrivacyInfo.xcprivacy` dosyasını da pakete ekler.
