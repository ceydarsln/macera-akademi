# App Store gönderim kontrol listesi

Son paket denetimi: 10 Ekim 2026 — Xcode 26.6, iOS 26.5 SDK
Son iPad ön kontrolü: 9 Ekim 2026 — iPad (A16) simülatörü, iOS 26.5.

## Hazır olanlar (doğrulandı)

| Öge | Durum |
| --- | --- |
| Release derlemesi (`generic/platform=iOS`) | Xcode 26.6 ile arşiv ve App Store Connect IPA dışa aktarımı başarılı |
| Uygulama paketi | Xcode 26.6 arşivindeki `.app` yaklaşık 8,2 MB; mağaza IPA'sı yaklaşık 2,3 MB. Ana HTML kaynak özetiyle eşleşiyor. |
| Sürüm | iOS ve Android `2.8.2 (23)`; iOS IPA dışa aktarımı tamamlandı |
| Bundle ID | `com.maceraakademi.app` |
| Minimum iOS | 15.0 |
| Şifreleme beyanı | `ITSAppUsesNonExemptEncryption = false` (ek belge gerekmez) |
| Uygulama simgesi | 1024×1024, alfa kanalı yok — Apple ölçütüne uygun |
| Açılış rengi | `UILaunchScreen` → `LaunchBackground` renk kümesi mevcut |
| Gizlilik bildirimi | `PrivacyInfo.xcprivacy` pakete giriyor |
| Mağaza metinleri | `metadata-tr.md`, `app-privacy-tr.md`, `privacy-policy.html` hazır |
| Cihaz ailesi | `UIDeviceFamily = [1,2]` — iPhone ve iPad |
| iPad Release simülatörü | 9 Ekim 2026 derlemesi başarılı; pakette `UIDeviceFamily = [1,2]` doğrulandı. 10 Ekim'de Xcode 26.6 ile imzalı iPhone/iPad mağaza IPA'sı da üretildi. |
| Açılış ekranı | Yerel karşılama katmanı: 1. saniyede görünür, içerik gelince kaybolur |
| Ekran görüntüleri | `ekran-goruntuleri/` — iPhone görüntüleri mevcut; iPad gönderim görüntüleri ayrıca hazırlanmalı |

## Gönderim öncesi açık kontroller

1. Apple Developer hesabı ve `L69J7JMD46` takımı Xcode'da doğrulandı. Xcode 26.6, bulut yönetimli Apple Distribution imzasıyla `2.8.2 (23)` IPA'sını başarıyla üretti. Paket: `output/release-paketleri-2026-10-10/ios-2.8.2-app-store-export/MaceraAkademi.ipa`.
2. App Store Connect'te uygulama kaydı mevcut ve yayımdaki sürüm `2.8.1`. Xcode yükleme ön sorgusunda `build 23` için önceki bir build bulunmadı.
3. `2.8.2 (23)` paketi 11 Ekim 2026'da Xcode 26.6 ile App Store Connect'e başarıyla yüklendi. Apple "Uploaded package is processing" yanıtını verdi; işleme/mağaza kabul sonucu ayrıca doğrulanmalı. İncelemeye gönderme veya yayımlama yapılmadı.
4. Gizlilik politikası/destek URL'leri, inceleme ekibi test hesabı, yaş derecelendirmesi ve güncel iPad ekran görüntüleri gönderimden önce App Store Connect'te doğrulanmalı.
5. iPad (A16) / iOS 26.5 simülatöründe Release uygulaması kuruldu ve ana ekranı açıldı; iPhone 17 / iOS 26.5 simülatöründe ilk karşılama ekranı açıldı. Simülatör içindeki dokunma otomasyonu yanıt vermedi; gerçek iPad'de ses ve dokunma testi ile canlı yarışmanın iki ayrı hesapla kabul testi hâlâ açık.

## Çözülen riskler

**iPad (yeniden açık).** Güncel proje `TARGETED_DEVICE_FAMILY = "1,2"`
hedefliyor; önceki iPhone-yalnız kontrolü artık geçerli değil. iPad (A16)
simülatöründe derleme, açılış, misafir sınıf/karakter akışı, arkadaşlar ve
yarışma arenası ekranları geçti. Bu, iki hesapla canlı maç testi değildir.
600 px oyun sütunu korunurken koyu yan bantlar tabletlerde
arka planla uyumlu hale getirildi. Tüm oyunların iPad görsel kabulü, sesin
gerçek iPad'de dinlenmesi ve App Store iPad ekran görüntüleri hâlâ açık.

**Açılıştaki boş ekran (giderildi).** 1,7 MB'lık tek HTML ayrıştırılırken
uygulama boş mor bir ekran gösteriyordu. `WebViewController` artık uygulama
adı, dönen gösterge ve "Maceralar hazırlanıyor…" metninden oluşan yerel bir
karşılama katmanı kuruyor; katman `didFinish` ile kalkıyor, gezinme geri
çağrısı hiç gelmezse 30 saniyelik güvenlik zamanlayıcısı devreye giriyor.
Soğuk başlatma sınandı: 1. saniyede karşılama katmanı, 4. saniyede içerik;
arada boş kare yok.

## Yayın notu

Bu Mac'te sistemin varsayılan `xcodebuild` komutu hâlâ eski Xcode 16.3'e bağlı. Yeniden paketleme gerektiğinde Xcode 26.6'nın geliştirici dizinini `DEVELOPER_DIR` olarak seçin; eski Xcode ile mağaza paketi üretmeyin. IPA'yı yüklemeden önce sürüm ve derleme numarasını App Store Connect'te kontrol edin.
