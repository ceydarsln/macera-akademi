# App Store gönderim kontrol listesi

Denetim tarihi: 4 Eylül 2026 — Xcode 16.3, iOS 18.4 SDK
Son güncelleme: iPad riski ve açılış ekranı giderildi.

## Hazır olanlar (doğrulandı)

| Öge | Durum |
| --- | --- |
| Release derlemesi (`-sdk iphoneos`) | `** BUILD SUCCEEDED **`, hata ve uyarı yok |
| Uygulama paketi | 7,3 MB; `macera-akademi.html` + 46 oyun dosyası eksiksiz |
| Sürüm | `CFBundleShortVersionString 2.8.1`, `CFBundleVersion 22` — Android ile eşit |
| Bundle ID | `com.maceraakademi.app` |
| Minimum iOS | 15.0 |
| Şifreleme beyanı | `ITSAppUsesNonExemptEncryption = false` (ek belge gerekmez) |
| Uygulama simgesi | 1024×1024, alfa kanalı yok — Apple ölçütüne uygun |
| Açılış rengi | `UILaunchScreen` → `LaunchBackground` renk kümesi mevcut |
| Gizlilik bildirimi | `PrivacyInfo.xcprivacy` pakete giriyor |
| Mağaza metinleri | `metadata-tr.md`, `app-privacy-tr.md`, `privacy-policy.html` hazır |
| Cihaz ailesi | `UIDeviceFamily = [1]` — yalnız iPhone |
| Açılış ekranı | Yerel karşılama katmanı: 1. saniyede görünür, içerik gelince kaybolur |
| Ekran görüntüleri | `ekran-goruntuleri/` — iPhone 6.9" (1320×2868) |

## Engelleyiciler — yalnız hesap sahibi çözebilir

1. **İmzalama takımı yok.** Arşiv denemesi şu hatada durdu:
   `Signing for "MaceraAkademi" requires a development team.`
   `security find-identity -p codesigning` → **0 geçerli kimlik**.
   Gerekenler: Apple Developer Program üyeliği (yıllık 99 USD), Xcode >
   Settings > Accounts'a Apple kimliğiyle giriş, ardından hedefin
   Signing & Capabilities bölümünde takımın seçilmesi.

2. **App Store Connect kaydı.** `com.maceraakademi.app` kimliğiyle uygulama
   kaydı oluşturulmalı.

3. **Yükleme kimlik doğrulaması.** App Store Connect > Users and Access >
   Integrations bölümünden API anahtarı üretilip `.p8` dosyası
   `~/.appstoreconnect/private_keys/` içine konmalı. (Bu adımı parola/anahtar
   girmeyi gerektirdiği için ben yapamam.)

4. **Gizlilik politikası URL'si.** `privacy-policy.html` herkese açık bir HTTPS
   adresinde, uygulamanın PHP/MySQL sunucusuyla birlikte yayımlanmalı.

5. **Destek URL'si** ve inceleme ekibi için **süreli test hesabı**.

6. **Yaş derecelendirme anketi** App Store Connect üzerinden doldurulmalı.

## Çözülen riskler

**iPad (giderildi).** `TARGETED_DEVICE_FAMILY` `"1,2"` iken iPad'de içerik
telefon genişliğinde bir sütunda kalıyor, iki yanda geniş koyu boşluk
oluşuyordu; Apple bunu "iPad'e uyarlanmamış" diye geri çevirebiliyor. Hedef
`"1"` yapıldı. Derlenmiş pakette `UIDeviceFamily = [1]` doğrulandı. Uygulama
iPad'de uyumluluk kipinde çalışmayı sürdürür, iPad ekran görüntüsü
zorunluluğu ve ret riski kalktı.

**Açılıştaki boş ekran (giderildi).** 1,7 MB'lık tek HTML ayrıştırılırken
uygulama boş mor bir ekran gösteriyordu. `WebViewController` artık uygulama
adı, dönen gösterge ve "Maceralar hazırlanıyor…" metninden oluşan yerel bir
karşılama katmanı kuruyor; katman `didFinish` ile kalkıyor, gezinme geri
çağrısı hiç gelmezse 30 saniyelik güvenlik zamanlayıcısı devreye giriyor.
Soğuk başlatma sınandı: 1. saniyede karşılama katmanı, 4. saniyede içerik;
arada boş kare yok.

## Engeller kalkınca yayın komutları

```bash
TEAM_ID=XXXXXXXXXX ./ios/yayinla.sh arsiv
TEAM_ID=XXXXXXXXXX ./ios/yayinla.sh ipa
ASC_KEY_ID=... ASC_ISSUER_ID=... ./ios/yayinla.sh dogrula
ASC_KEY_ID=... ASC_ISSUER_ID=... ./ios/yayinla.sh yukle
```
