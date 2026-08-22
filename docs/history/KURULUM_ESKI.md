# 📱 Macera Akademi — Android APK Oluşturma

Bu klasör, oyunu Android uygulamasına (APK) çeviren **hazır Android Studio projesidir**.
Oyunun tamamı `app/src/main/assets/macera-akademi.html` içindedir; internet gerektirmez.

---

## Yol 1 — Android Studio ile APK (önerilen)

1. [Android Studio](https://developer.android.com/studio) indir ve kur (ücretsiz).
2. Android Studio'yu aç → **Open** → bu klasörü (`MaceraAkademi`) seç.
   - "Trust Project?" sorusu çıkarsa **Trust** de.
3. ⏳ **EN ÖNEMLİ ADIM: Gradle senkronizasyonunun bitmesini bekle.**

   Ekranın en altında şöyle bir yazı ve ilerleme çubuğu göreceksin:

   ```
   Importing 'MaceraAkademi' Gradle Project  ▓▓▓▓▓░░░░░
   ```

   **Bu yazı kaybolana kadar Build menüsündeki komutlar gri (pasif) kalır ve tıklanmaz.**
   İlk açılışta Gradle ve kütüphaneler indirildiği için **5-15 dakika** sürebilir.
   İnternet bağlantısı gerekir. Bittiğinde alt çubukta ilerleme kalmaz ve
   sol taraftaki `app` klasörü açılabilir hâle gelir.

4. Senkronizasyon bittikten sonra üst menü:

   **Build → Generate App Bundles or APKs → Generate APKs**

   > Android Studio sürümüne göre bu menünün adı farklı olabilir:
   > - Yeni sürümler: **Build → Generate App Bundles or APKs → Generate APKs**
   > - Eski sürümler: **Build → Build Bundle(s) / APK(s) → Build APK(s)**
   >
   > İkisi de aynı işi yapar.

5. İşlem bitince sağ altta çıkan bildirimde **locate** yazısına bas. APK şuradadır:

   ```
   app/build/outputs/apk/debug/app-debug.apk
   ```

6. Bu dosyayı telefona kopyala ve dokunarak kur.
   (Telefon "bilinmeyen kaynak" uyarısı verirse → *Ayarlar → Bu kaynağa izin ver*)

### Google Play'e yüklemek istersen
Play Store imzalı sürüm ister:
**Build → Generate Signed Bundle / APK → Android App Bundle** → yeni bir keystore oluştur
(şifresini kaybetme, güncellemeler için gerekir).

---

## 🔧 Sorun giderme

### "Build menüsündeki seçenekler gri, tıklanmıyor"
Gradle senkronizasyonu hâlâ sürüyor (3. adım). Alt çubuktaki ilerleme çubuğu bitene kadar bekle.
Senkronizasyon bitmemişse hiçbir derleme komutu çalışmaz — bu normaldir, hata değildir.

### "Senkronizasyon çok uzun sürüyor / takıldı"
- İnternet bağlantını kontrol et (Gradle ilk kez ~150 MB indirir).
- Sağ üstteki 🐘 **Gradle** sekmesinden veya **View → Tool Windows → Build** panelinden
  ne yaptığını görebilirsin.
- Yine olmazsa: **File → Sync Project with Gradle Files** ile yeniden dene.

### "Plugin/AGP sürüm uyarısı çıktı" veya "This project uses a newer/older AGP"
Bu proje Android Gradle Plugin 8.2.2 ile hazırlandı. Çok yeni bir Android Studio
kullanıyorsan sürüm yükseltmek isteyebilir. Çözüm:
**Tools → AGP Upgrade Assistant** → önerilen sürüme yükselt → tekrar senkronize et.
Bu otomatik olarak `build.gradle` dosyalarını günceller, elle bir şey yapmana gerek yok.

### "Unsupported Java / JDK" hatası
**File → Settings (macOS: Android Studio → Settings) → Build, Execution, Deployment →
Build Tools → Gradle** → *Gradle JDK* olarak Android Studio ile gelen JDK'yı seç
(genelde "jbr-21" veya "Embedded JDK").

### "SDK location not found"
**Tools → SDK Manager** → Android SDK'yı kur (Studio genelde ilk açılışta sorar).
`local.properties` dosyası Studio tarafından otomatik oluşturulur, sen elle yazmayacaksın.

### Hâlâ olmuyorsa
**View → Tool Windows → Build** panelini aç, kırmızı hata metnini kopyala.
Hata mesajı olmadan sorunun nedenini tahmin etmek zordur.

---

## Yol 2 — APK'sız kurulum (5 saniye, bilgisayar gerekmez)

APK derlemek istemiyorsan `macera-akademi.html` dosyasını telefona at ve Chrome ile aç:

1. Chrome'da dosyayı aç.
2. Sağ üst **⋮** menü → **Ana ekrana ekle**.
3. Ana ekranda tilki simgeli "Macera" uygulaması çıkar; tam ekran açılır, adres çubuğu görünmez.

Fark: APK gerçek bir uygulamadır (Play Store'a yüklenebilir, paylaşılabilir);
"ana ekrana ekle" ise aynı deneyimi verir ama Chrome'a bağlıdır.

---

## Projede neler var

| Dosya | Görevi |
|---|---|
| `app/src/main/assets/macera-akademi.html` | **Oyunun tamamı** (70 oyun) — Firebase bağlantılı sürüm |
| `app/src/main/assets/macera-akademi-cihazda.html` | Alternatif: tamamen çevrimdışı sürüm |
| `app/src/main/java/.../MainActivity.java` | Oyunu tam ekran WebView'de, https kaynağı olarak açar |
| `AndroidManifest.xml` | Uygulama adı, ikon, dikey ekran kilidi |
| `res/drawable/ic_launcher_foreground.xml` | Tilki uygulama simgesi (vektör) |
| `app/build.gradle` | Android 6.0+ (minSdk 23) hedefler |
| `gradle/wrapper/` | Gradle sürümünü projeye sabitler (ilk açılışı kolaylaştırır) |

### Yapılan Android ayarları
- **Dikey ekran kilidi** — çocuk telefonu çevirdiğinde düzen bozulmaz
- **Ekran açık kalır** — oyun sırasında ekran kararmaz
- **Geri tuşu** oyun içindeyse oyun listesine, listede ise ana sayfaya döner (uygulamadan atmaz)
- **Sesli direktifler** için otomatik ses oynatma izni açık
- **İlerleme kaydı**: hesapsız modda telefonda, hesaplı modda sunucuda (cihazlar arası)
- **https kaynağı** (WebViewAssetLoader) sayesinde Firebase sorunsuz çalışır
- **Yakınlaştırma kapalı** ve sistem yazı boyutu düzeni bozmaz

---

---

## Hesap sistemi hakkında

Uygulamada gerçek bir kayıt/giriş sistemi vardır:

- Şifreler **düz metin olarak saklanmaz**; her hesap için rastgele bir "tuz" (salt) üretilip
  SHA-256 özeti alınır (cihazda güvenli kripto yoksa yinelemeli yedek özet kullanılır).
- Aynı cihazda **birden fazla hesap** olabilir; her hesabın seviyesi, altını ve
  tamamladığı oyunlar birbirinden tamamen ayrıdır.
- Oturum açık kalır; uygulamayı kapatıp açtığında aynı hesapla devam eder.
- Hesap işlemleri: şifre değiştirme, çıkış yapma, hesabı silme.

**Önemli:** Veriler **telefonun kendi depolamasında** tutulur (sunucu yoktur).
Yani hesap sadece o cihazda geçerlidir; telefon değişirse hesap taşınmaz.
Farklı cihazlardan aynı hesaba girmek veya arkadaş/mesaj özelliklerini çalıştırmak için
bir sunucu (API) gerekir. Kod bunun için hazırlandı: tüm veri erişimi `DB` nesnesinin
`read / write / remove` fonksiyonlarından geçer; bunları bir API çağrısına çevirmek yeterlidir.

### Sınıf mantığı
- **1. sınıf** seçilirse ana ekranda yalnızca **Matematik** ve **Türkçe** görünür (70 oyun hazır).
- **2, 3, 4. sınıf** seçilirse bütün sekmeler görünür, ancak içine girildiğinde
  "oyunlar hazırlanıyor" bilgisi çıkar (o sınıflar için oyun henüz eklenmedi).
- Yeni sınıf oyunu eklemek için oyun tanımına `grade: 2` gibi bir değer vermek yeterlidir.

---

## 🔌 Firebase / sunucu bağlantısı — APK'da neden çalışır?

Bu önemli bir ayrıntı: **HTML dosyası `file://` olarak yüklenmiyor.**

Tarayıcılar (ve WebView), diskten açılan `file://` sayfalarında Firestore'un kullandığı
bağlantı türünü ve yerel veritabanını (IndexedDB) engelliyor. Böyle bir sayfada
kimlik doğrulama çalışır ama **veri okuma/yazma sessizce askıda kalır**.

Bu projede `WebViewAssetLoader` kullanılıyor: dosya uygulamanın içinden
`https://appassets.androidplatform.net/assets/...` adresinden sunuluyor.
Sayfa gerçek bir **https kaynağına** sahip olduğu için:

- Firestore bağlantısı normal kurulur (hesap, ilerleme, arkadaşlar çalışır)
- Oturum kalıcı olur, çevrimdışı önbellek çalışır
- `file://` kısıtlamaları hiç devreye girmez

Yani **APK'da localhost / python komutu gibi geçici çözümlere gerek yoktur.**

### Assets içindeki iki dosya

| Dosya | Ne yapar |
|---|---|
| `macera-akademi.html` | **Uygulamanın yüklediği dosya.** Firebase bağlantılı sürüm: hesap açma/giriş, cihazlar arası ilerleme, arkadaşlar + hazır mesajlar, ayrıca **hesapsız mod** (internetsiz de çalışır). |
| `macera-akademi-cihazda.html` | Tamamen çevrimdışı sürüm. Hesaplar yalnızca o cihazda tutulur, sunucu hiç kullanılmaz. |

Sunucusuz sürümü kullanmak istersen: `macera-akademi.html` dosyasını sil,
`macera-akademi-cihazda.html` dosyasının adını `macera-akademi.html` yap, APK'yı yeniden derle.

> Not: Firebase sürümündeki **hesapsız mod** da internet gerektirmiyor. Yani çoğu durumda
> Firebase sürümü yeterlidir — internet varsa hesap açılır, yoksa hesapsız oynanır.

---

## 🔊 Sesli okuma (Android)

Android WebView'in kendi konuşma motoru (`speechSynthesis`) sessiz kalıyor. Bu yüzden
uygulama **telefonun yerleşik Türkçe metin okuma motoruna** köprüyle bağlanır
(`MainActivity` içindeki `TtsBridge` → HTML tarafında `window.AndroidTTS`).

Her talimatın yanında bir **🔊 düğmesi** vardır; çocuk ilk okumayı duymazsa
tekrar dinleyebilir.

**Ses gelmiyorsa:** telefonda Türkçe ses paketi kurulu olmayabilir. Uygulama bunu
algılayıp bilgi verir. Kurulum: *Ayarlar → Erişilebilirlik → Metin okuma çıkışı →
Google Metin Okuma → Dilleri yükle → Türkçe*.

## 🌐 İnternet izni

`AndroidManifest.xml` içinde şu izinler bulunur:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

**Bu izin olmadan** uygulama açılır ve oyunlar çalışır (hepsi yerel), ancak
hesap açma/giriş sırasında *"Firebase kütüphanesi yüklenemedi"* hatası verir.
Silmeyin.

## Oyunu güncellemek
Yeni bir `macera-akademi.html` aldığında sadece
`app/src/main/assets/macera-akademi.html` dosyasının üzerine yaz ve APK'yı yeniden derle.
Başka hiçbir şeyi değiştirmen gerekmez.

## Uygulama adını / paket adını değiştirmek
- Görünen ad: `app/src/main/res/values/strings.xml` → `app_name`
- Paket adı (Play Store'da tekil olmalı): `app/build.gradle` içindeki `applicationId`
  ve `namespace` satırları + `MainActivity.java` en üstteki `package` satırı.
