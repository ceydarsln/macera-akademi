# Ses ve Kalan İşler Denetimi

Denetim tarihi: 26 Ağustos 2026

## Merkezi ses zinciri

`web/macera-akademi.html` içindeki iframe oyunları `parent.oku(metin, tekrar)` çağrısına gider. Bu köprü tilki balonunu günceller, ses ayarı kapalıysa ses üretmez ve aynı metni yalnız kullanıcı tekrar istemediyse yinelenmeden `speakNow()` işlevine verir. `speakNow()` Android'de `AndroidTTS.speak()` köprüsünü, köprü yoksa `speechSynthesis`i kullanır; tarayıcı sesi `tr-TR`, `0.95` hız ve `1.0` perde ile kuruludur. Android köprüsünün sırası hazır OGG kaydı → yerel sistem TTS → Piper'dır. Ağ gerektiren TTS sesi ancak yerel Türkçe ses yoksa seçilir; Piper da yalnız sistem TTS kullanılamıyorsa tembel başlatılır.

İframe `speak()` işlevleri `parent.oku()` başarılı olunca erken döner; bu nedenle normal köprü yolunda çift okuma yoktur. Köprü bulunmadığında yerel `speechSynthesis` geri dönüş yoludur. Sosyal4'te ses şiddeti karşılaştırması için ayrı `seslendir()` bilerek yerel Web Speech kullanır; `onend`/`onerror` yanında güvenlik zaman aşımı bulunduğundan ses olayı gelmese de oyun kilitlenmez.

## Uygulanan merkezi düzeltme

- `web/macera-akademi.html` ve Android varlık eşi `app/src/main/assets/macera-akademi.html`: `stopSpeech()` hem sözleşmede bulunan `AndroidTTS.stop()` çağrısını hem de varsa `speechSynthesis.cancel()`ı kullanır. Yeni oyun açılışında, yeniden denemede ve `gamePlayer` ekranından çıkışta çağrılır. Böylece önceki tur, başarı veya yönerge sesi yeni oyuna/ekrana sarkmaz.
- `app/src/main/java/com/maceraakademi/app/MainActivity.java`: `TtsBridge.stop()` bekleyen `ttsPending` metnini de temizler. TTS motoru geç başlatıldığında eski oyunun metninin sonradan okunması önlenir.
- `app/src/main/java/com/maceraakademi/app/MainActivity.java`: Hazır kayıt yokken saniyeler süren cihaz içi üretim yerine hazırlanmış yerel sistem TTS ana motor oldu. Her tekrar çağrısı benzersiz utterance kimliğiyle ana iş parçacığında başlar; ağ sesi seçilmediği için bağlantı gecikmesi oluşmaz.
- `app/src/main/java/com/maceraakademi/app/PiperSes.java`: `durdur()` artık yalnız AudioTrack'i kapatmakla kalmaz, etkin üretim neslini de iptal eder. Eski oyun üretiminin tek iş kuyruğunda yeni oyunu bekletmesi önlenir.

## Öğrenci konuşması ve kayıt durumu

| Sahip | Dosya ve oyun | Kanıt | Sonuç / yapılacak iş |
| --- | --- | --- | --- |
| Türkçe4 | `web/phaser/turkce4-pdf.html`, `z09`, `z21`, `z27`, `z37`, `z39`, `z61` | `konusCiz()` yalnız `Date.now()` farkını ve basılı tutma süresini ölçer; `MediaRecorder`/`SpeechRecognition` yoktur. Üç tur koşumu 64/64 ve 390×844 ölçümü 64/64 temiz geçmiştir. | Gerçek kayıt veya tanıma yoktur. Sahibi "Konuşman kaydedildi/aldık" metnini "Konuşma süresi yeterli" olarak düzeltiyor; öz değerlendirme korunur. |
| Sosyal4 | `web/phaser/sosyal4-pdf.html`, genel `renderKonus()` (sb01–sb36 içinde `kind:'konus'` örneği yok) | `renderKonus()` örneği TTS ile dinletip ölçüt kutularını işaretletir; `MediaRecorder`/`SpeechRecognition` yoktur. ENGINE11 koşumu 36/36 geçmiştir. | Gerçek kayıt/tanıma yoktur; UI bunu iddia etmemelidir. Dosya Sosyal görevinin sahipliğindedir, burada değiştirilmedi. |
| Fen4 | `web/phaser/fen4-pdf.html`, `f01`–`f48` | `speak()` köprü başarılıysa erken döner; tur ilerlemesi ses olayına bağlı değildir. | Merkezi durdurma düzeltmesi tüm Fen4 oyunlarını kapsar. Fen katalog eşlemesine dokunulmadı. |

## Hazır kayıt kapsamı

- `tools/audio/manifest.json`: 2.151 benzersiz temizlenmiş metin, 102.710 karakter; en uzun metin 179 karakterdir. Alan dağılımı: `say` 1.032, `speak` 636, `okSay` 213, `orderSay` 177, `revealSay` 93.
- `app/src/main/assets/ses/`: 0 adet `.ogg`; Git ağacında yalnız `.klasor` yer tutucusu vardır. Bu nedenle pratikte bütün metinler Piper veya sistem TTS'ye düşer.
- `tools/audio/uret.py`, Chatterbox modelini ilk çalıştırmada indirebilir ve eksik OGG'leri üretir. Büyük model indirme veya toplu üretim bu denetimde başlatılmadı.

## Kalan entegrasyon işleri

1. Kayıt üretimi kullanıcı onayıyla ayrı yürütülmeli; sonra `tools/audio/uygulamaya_kopyala.sh` ile `app/src/main/assets/ses/` içine alınmalı ve cihazda hazır kayıt, Piper ve sistem TTS düşüşleri denenmeli.
2. `tools/audio/metinler.py` hem girdi hem çıktı için `/Users/ceyda/Downloads/...` sabit yolunu kullanıyor. Araç, depo içindeki güncel `web/macera-akademi.html` ve isteğe bağlı Phaser metinlerinden tekrarlanabilir manifest üretecek şekilde düzenlenmeli; bunu yaptıktan sonra manifest kapsamı yeniden sayılmalı.
3. Yeni/özelleşmiş Phaser oyunlarının dinleme metinleri mevcut manifest çıkarıcısının beş alanlı taramasına girmiyor. Hazır kayıt hedefleniyorsa çıkarıcı, `web/phaser/*-phaser.html` içindeki çağrılan ses metinlerini de kapsamalı.
4. Fiziksel Android cihazda şu yedek senaryolar ayrıca doğrulanmalı: Türkçe sistem ses paketini kaldırıp Piper'a düşme ve TTS hazır olmadan ses isteyip sonra ekran değiştirme. Yerel Android emülatörü disk alanı yetersizliği nedeniyle bu turda başlatılamadı.

## Bu denetimde doğrulananlar

- Her iki `macera-akademi.html` kopyası JavaScript olarak ayrıştırıldı; `stopSpeech()` hem yerel köprü hem Web Speech iptalini çağırıyor, `openGame()` ve `gamePlayer` çıkışı çağrıları mevcut.
- `JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home" ./gradlew :app:compileDebugJavaWithJavac` başarıyla tamamlandı.
- Yerel tarayıcıda `u27` dinleme akışında `Dinle` ve `Tekrar dinle` art arda çalıştırıldı; sayaç 2'ye çıktı, üst yönerge tekrar düğmesi iki kez çağrıldı ve konsol hatası oluşmadı.
- `lintRelease` ve imzalı `bundleRelease` başarılı tamamlandı; lint engelleyici hata bildirmedi.
