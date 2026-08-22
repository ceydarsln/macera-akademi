# Macera Akademi — Tam Paket (22 Ağustos, 2.8-test)

Üç paralel oturumun bütün çalışması bu pakette birleştirilmiş hâlde.

## Durum

- 658 oyunun **641'i (%97) Phaser motorunda**. Kalan 17: drawSegments (6),
  placeValueLoad (2), fractionCut (2), moneyBuild (2), clockSet (2),
  solidScan (2), 1 özel choiceQuestion — bunlar eski DOM oynatıcısında
  çalışmaya devam ediyor, kırık değiller.
- Otomatik oynanarak sınanan oyun: 1. sınıf matematik 49/51 + sayma,
  2. sınıf 123, 3. sınıf 97/101, diğer oturumlardan 79 + 164.
- APK: MaceraAkademi-2.8-test.apk (versionCode 20) — her şey içinde.
- Ses: 470/2151 Chatterbox kaydı üretildi (sürüyor; bitince
  araclar/uygulamaya_kopyala.sh ile uygulamaya alınacak).

## Klasörler

    MaceraAkademi-2.8-test.apk   telefona kurulacak son sürüm
    uygulama/
      macera-akademi-firebase-11.html   ana uygulama + oyun kataloğu (kaynak)
      macera-akademi.html               APK'daki kopyası (birebir aynı)
      assets-phaser/                    APK'nın kullandığı 29 şablon + svgciz.js
    sablonlar/                          şablonların ~/Downloads'taki kaynak hâlleri
                                        (CDN Phaser ile; aynala.sh bunları çevirir)
    araclar/
      aynala.sh          şablonları APK varlıklarına kopyalar (CDN→yerel, damga)
      kosum.js           otomatik oyun test koşucusu (tarayıcı konsolunda)
      anlam_denetimi.js  "görev anlamlı mı" taraması (cevap etikette yazıyor mu vb.)
      metinler.py/uret.py/uygulamaya_kopyala.sh   Chatterbox ses üretim hattı
    belgeler/
      SABLON_KURALLARI.md   şablon yazım kuralları + üç oturumun iş bölümü
      katalog_istekleri.md  oturumlar arası istek/uygulama günlüğü
      ucuncu_oturum_gunlugu.md + UCUNCU_OTURUM_TUM_DEGISIKLIKLER.md
                            üçüncü oturumun kusur günlüğü ve tam kaynakları

## Yeni bir makinede kurulum

1. `sablonlar/` içeriğini ve `uygulama/macera-akademi-firebase-11.html`'i
   ~/Downloads'a koy; MaceraAkademi-3 projesini aç.
2. `araclar/aynala.sh` çalıştır (yollar ~/Downloads'a göre).
3. `JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home" ./gradlew assembleDebug`

## Bilinen eksikler

- kesirsaat şablonu yazıldı ama TEST EDİLMEDİ → kataloğa bilerek bağlanmadı.
- para (moneyBuild/placeValueLoad) ve geometri (drawSegments/solidScan)
  şablonları hiç bağlanmadı.
- 3. sınıfta h69 tek başarısız otomatik test (roket blok kırpması düzeltildi,
  yeniden doğrulanacak); 4. sınıf benim şablonlarımda henüz taranmadı.
- Ses üretimi sürüyor; Piper hâlâ APK'da (kayıtlar bitince çıkarılacak).
