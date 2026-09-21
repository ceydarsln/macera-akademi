# İkinci sahne düzeltme paketi — 21 Eylül 2026

## Kapsam

Bu paket tüm kataloğun tamamlandığı anlamına gelmez. Denetimdeki beş oyunun sorunlu sürükleme sahneleri ele alındı; diğer tur türlerinin öğrenme kuralları korundu.

- **P03 Basamak Değeri Köprüsü:** Üç turda rakam/değer parçaları köprünün eksik döşemelerine yerleşir. Parça oturma animasyonu ve tamamlanınca kısa bisiklet geçişi vardır. Sıfır basamakların farklı yerleri korunur.
- **P08 Okunuş Eşleştirme:** İlk turda okunuşlar sayı defterinin sayfalarına yerleşir. Sayfa hareketi, sonraki hafıza turunda kart çevirme hareketi ve dinleme köşesi eklendi. Hafıza ve dinleme kuralları değiştirilmedi.
- **Y10 Zıt Anlam Aynası:** İlk iki turda aynaya bırakılan doğru sözcük karşıtının resmini açar. Yanlış eşleşmede resim açılmaz. Son yazma turuna uzun–kısa karşılaştırma sahnesi kondu; yazma denetimi korundu.
- **G05 Keşif Çantası:** İlk iki turda kaynak dosyaları açık çantaya sürüklenir, nedenleriyle içeride kalır. Yanlış kaynak kabul edilmez. Son serbest yazma turu korunmuştur.
- **F05 Araştırma Çantası:** İlk turda kaynak dosyaları, künyeleri görünür biçimde açık çantaya yerleşir. Ara isteklerde çanta boşalmaz; son eklenen kaynağın da görünmesi sağlandı. Sonraki karar ve yazma turları korunmuştur.

Matematik/Türkçe parçaları hedeflerle aynı sırada gösterilmez. Sürükleme iptal edildiğinde işlem yapılmaz; dokunma/klavye alternatifleri korunur. Azaltılmış hareket tercihinde sonuç kalır, yeni CSS animasyonları kapanır. Küçük ekranlarda içerik gerektiğinde dikey kaydırılır.

## Teknik sınır

Yeni `scene-discovery.js/css` yalnız seçilen sahnelere bağlıdır. Önceki `scene-workshop` sürükleme yardımcılarını kullanır; bütün oyunların ortak oynatıcıları yeniden tasarlanmamıştır. `aynala.sh` yeni varlıkları Android paketine kopyalar.

## Doğrulama

- `tools/verify-scene-discovery.cjs`: İlk eylemde yanlış hedef/kaynak, pointercancel, durum değişimi, aktif animasyon ve azaltılmış hareket kontrolü; 320×568, 390×844 ve 844×390 ölçülerinde 15 tur başlangıcında yönerge/yatay taşma kontrolü.
- 390×844 ekranda seçilen sahnelerin bütün sürükleme turları **40/40 nesne yerleştirmesiyle** tamamlandı: P03 18, P08 3, Y10 8, G05 7, F05 4. F05 son kaynak dahil dört kaynağın görünürlüğü de kontrol edildi.
- Üç turluk çözüm testleri: P02, P03, P08, P09, P15, P24; Y09, Y10, Y11; G04, G05, G06; F03, F04, F05, F06. **16 oyun / 48 tur geçti.** Bu çözüm testleri ile gerçek sürükleme testleri farklı kontrollerdir.
- Dört şablonun gömülü JavaScript sözdizimi, web/Android birebir eşitliği ve `git diff --check` kontrol edildi.
- Görsel inceleme: Beş oyunun 390×844 başlangıç ve etkileşim görüntüleri üzerinden kontrol; ayna etiketi/görsel çelişkisi ve çantalarda gereksiz dekor yüksekliği düzeltildi.
- Fiziksel Android/iPhone cihaz testi yapılmadı; testler yerel masaüstü Chrome üzerinde yürütüldü.

## İnceleme çıktıları

`artifacts/sahne-duzeltmeleri-2-2026-09-21/index.html`: Önce / yeni / işlem sonrası karşılaştırma, 2. ve 3. tur ekranları, çalışır oyun bağlantıları.

`verification.json`: Test sonuçları ve tüm sürükleme turlarındaki yerleştirme sayıları. Ekran görüntüleri animasyon kaydı değildir; hareket oyun bağlantısında görülür.

## Devam

Diğer oyunların denetim bulguları `docs/OYUN_TASARIM_DENETIMI_2026-09-21.md` içindedir. Bu beş oyun ve önceki beş oyun, 635 oyunun tamamının görsel/etkileşim onayı olarak sayılmamalıdır. Sonraki paket yine gerçek sahne hedefi, eylem sonucu ve telefon erişilebilirliği üzerinden seçilmelidir.
