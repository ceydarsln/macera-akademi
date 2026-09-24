# Manuel oyun kalite çizelgesi

Bu belge otomatik regresyon sonuçlarından ayrıdır. Buradaki bir oyun ancak
uygulama arayüzünden açılıp gerçek dokunma, sürükleme, dinleme ve tamamlama
akışı elle denendikten sonra **Geçti** sayılır.

## Kabul ölçütleri

Her oyun için şu noktalar kontrol edilir:

1. Başlık, yönerge ve oynanış aynı görevi anlatıyor mu?
2. Çocuk doğru cevabı yönergede verilen bilgiyle bulabiliyor mu?
3. Yanlış/doğru dokunuş, can, puan ve ilerleme doğru çalışıyor mu?
4. Oyun baştan sona tamamlanabiliyor mu?
5. Metin, seçenekler, çizimler ve geri bildirimler çakışıyor mu?
6. Ses gerektiren oyunda ilk okuma ve **DİNLE** ile tekrar okuma çalışıyor mu?
7. Oyun 1. sınıf düzeyine ve belirtilen kazanıma uygun mu?

Durumlar: **Geçti**, **Düzeltildi · yeniden testte**, **Cihaz sesi bekliyor**,
**Test edilmedi**.

## 1. sınıf · ilk manuel tur

| Kimlik | Oyun | İlk bulgu | Yapılan düzeltme | Manuel sonuç |
|---|---|---|---|---|
| m01 | Trafik Polisi | Belirgin bir mantık veya etkileşim hatası görülmedi. | Değişiklik gerekmedi. | **Geçti** · iki mavi araç sola, iki kırmızı araç sağa sürüklenerek tamamlandı. |
| m02 | Pusula Korsanı | Belirgin bir mantık veya etkileşim hatası görülmedi. | Değişiklik gerekmedi. | **Geçti** · sol üstten iki sağa ve bir aşağı hareketle hedefe ulaşıldı. |
| m03 | Dağcı Keçi | Belirgin bir mantık veya etkileşim hatası görülmedi. | Değişiklik gerekmedi. | **Geçti** · ileri, yukarı, ileri, yukarı, yukarı dizisiyle tamamlandı. |
| m04 | Gölge Avcıları | Belirgin bir mantık veya etkileşim hatası görülmedi. | Değişiklik gerekmedi. | **Geçti** · elmanın doğru gölgesi sürüklenip eşleştirildi. |
| m05 | Çorap Eşleştirme | Belirgin bir mantık veya etkileşim hatası görülmedi. | Değişiklik gerekmedi. | **Geçti** · kısa kırmızı çorabın eşi sürüklenerek bulundu. |
| m06 | Anahtar ve Kilit | Belirgin bir mantık veya etkileşim hatası görülmedi. | Değişiklik gerekmedi. | **Geçti** · kilide uyan yatay anahtar seçildi. |
| m07 | Dedektif Ayak İzi | Belirgin bir mantık veya etkileşim hatası görülmedi. | Değişiklik gerekmedi. | **Geçti** · önce yanlış iz ile can/uyarı, ardından dört çizgili doğru iz ve tamamlama doğrulandı. |
| m08 | Meyve Suyu Şişeleri | Sıvı seviyesi sorusu yerine hareketli deniz etiketlerini ağla yakalama oyunu açılıyordu. | Referans şişe ve üç farklı doluluk seviyeli şişeden oluşan gerçek sıvı karşılaştırma sahnesi yapıldı. | **Geçti** · daha az dolu A için doğru geri bildirim, yarım dolu B ile tamamlama elle doğrulandı. |
| m09 | Çarkıfelek Dişlileri | Kartlarda “6 dişli / 8 dişli” yazdığı için çocuk dişleri saymadan cevabı görüyordu. | Gerçek 6, 7 ve 8 dişli çarklar ile 6/8 hedef yuvaları çizildi; diş uçları belirginleştirildi. | **Geçti** · yanlış 7 ve 8→6 eşleşmelerinde geri bildirim/can; ardından 6→6 ve 8→8 ile tamamlama doğrulandı. |
| m10 | Parmak Canavarları | Kısa cevaplara doğrudan dokunulamıyor, boş alandan atılan mermi hareketli seçenekleri ıskalıyordu. | Tüm cevaplar doğrudan dokunulur yapıldı; bu oyun için sabit ve eşit aralıklı seçenek düzeni eklendi. | **Geçti** · 5+2=7, 5+5=10 ve 1+5=6 turları tek tek tamamlandı. |
| m11 | Uzaylı Asansörü | Belirgin bir mantık veya etkileşim hatası görülmedi. | Değişiklik gerekmedi. | **Geçti** · 0→10, 11’den geri alıp 10’a dönüş ve 16’da “1 onluk 6 birlik” ile tamamlama doğrulandı. |
| m12 | Pazar Kasası | Sayma mekaniği doğru; “Okuma, Dinleme” kapsamındaki cihaz sesi tarayıcıdan doğrulanamıyor. | Değişiklik gerekmedi. | Oynanış **Geçti** · 20 portakal iki onluk çerçeveye tek tek eklendi. Fiziksel Android hoparlör testi **Cihaz sesi bekliyor**. |
| m13 | Kement Atma | “Koyuna dokun” yönergesine rağmen su altında kaçan koyunlar kepçeyle kovalanıyordu. | Sabit koyunların doğrudan seçildiği ve seçilenlerin gerçek 4’lü ağıla taşındığı çayır sahnesi yapıldı. | **Geçti** · dört farklı koyun tek tek seçilip ağılda grup oluşturuldu. |
| m14 | Sihirli Büyüteç | Doğru balık kepçeden kaçıyor, yoldaki nesne can götürebiliyor; “kırmızı” denen 🐠 sarı görünüyordu. | Sabit, gerçekten kırmızı/mavi çizilmiş balıklar ve doğrudan seçim sahnesi yapıldı. | **Geçti** · yanlış bitki seçimi ve can/uyarı; ardından 3 kırmızı + 2 mavi balıkla tamamlama doğrulandı. |
| m15 | Şipşak Hafıza | Meyvelerin kısa gösterimi Phaser’da hiç uygulanmıyor; cevaplar hafıza yerine hareketli hedef vurmayı ölçüyordu. | `flashMs/flashContent` desteği eklendi; 3 elma + 2 armut 1,6 saniye gösteriliyor ve cevaplar sabitleniyor. | **Geçti** · geçici kartın açılıp kapanması, 5 ve “3 ve 2” cevaplarıyla iki tur doğrulandı. |
| m16 | Orman Maratonu | Belirgin bir mantık veya etkileşim hatası görülmedi. | Değişiklik gerekmedi. | **Geçti** · 2. sıradaki tavşan için yanlış uyarısı, 3. sıradaki kaplumbağa ile tamamlama doğrulandı. |
| m17 | Uzaylı Apartmanı | Katlar yukarıdan aşağı 1–5 metin satırıydı; bina ve uzaylı yoktu. | Gerçek beş katlı binada 1. kat alta, 5. kat üste yerleştirildi; kargo sürükleme eklendi. | **Geçti** · 3. kata yanlış bırakma uyarısı ve 4. kata doğru teslim doğrulandı. |
| m18 | Dondurma Kulesi | Külah yerine metin satırları vardı; top sırası ve dondurma kulesi görünmüyordu. | 24 Eylül'de çakışan hedefler yeniden çizildi: toplar gerçek külah üstündeki yuvalara, alttan üste doğru yerleşiyor. | **Düzeltildi · manuel yeniden testte** · eski sürüm elle geçmişti; yeni sürümün 18 otomatik ekran/tur ve gerçek sürükleme senaryosu geçti, fakat insan gözüyle yeniden onay verilmedi. |
| m19 | Otobüs Durakları | Belirgin bir mantık veya etkileşim hatası görülmedi. | Değişiklik gerekmedi. | **Geçti** · 1. durak için yanlış uyarısı, otobüsten sayılan 2. durak ile tamamlama doğrulandı. |
| m20 | Şampiyonlar Kürsüsü | Kürsü yerine aynı biçimli 1/2/3 metin satırları vardı. | 1. ortada/en yüksek, 2. solda, 3. sağda olacak gerçek kürsü yapıldı. | **Geçti** · yanlış basamak geri bildirimi; çita 1., tavşan 2., kaplumbağa 3. yerleştirilerek tamamlandı. |
| m21 | Vagon Ekspresi | Yatay sıra kazanımına rağmen vagonlar dikey metin satırlarıydı; lokomotif yoktu. | Lokomotif solda, arkasında soldan sağa dört gerçek vagon çizildi. | **Geçti** · 2. vagon için yanlış uyarısı, lokomotiften 3. vagona zürafa bırakılarak tamamlama doğrulandı. |
| m22 | Gökyüzü Asansörü | Düğmeler `AL/GERİ AL` diyordu; katlar etiketsizdi; paket 0. katta kule içindeydi. | YUKARI/AŞAĞI düğmeleri, görünür 1–4 kat numarası ve zemin başlangıcı eklendi. | **Geçti** · 0→4, dört ayrı dokunuşla tamamlandı. |
| m23 | Obur Canavarın Tabakları | Çilekler su altında 3/7/5 grupları hâlinde dağınıktı; tabaklar görünmüyordu. | Üzerlerinde sayılar yazmadan 3, 7 ve 5 çilek taşıyan üç gerçek tabak çizildi. | **Geçti** · 3 çilekli A tabağı için yanlış uyarısı, 7 çilekli B tabağıyla tamamlama doğrulandı. |
| m24 | Adalet Terazisi | Yanlış karşılaştırma uyarısı pencerenin arkasında kalıyor, eşitleme için elma kartını sürüklemek gerektiği anlaşılmıyor ve başarı cümlesi iki kez yazılıyordu. | Uyarı pencerenin içine alındı; elma kartını sağ kefeye sürükleme yönergesi açıklaştırıldı; yinelenen başarı metni kaldırıldı. | **Geçti** · yanlış “Eşit”, doğru “Daha Az” ve sağ kefeye iki elma sürükleyerek 5=5 eşitliği elle doğrulandı. |
| m25 | İkiz Kardeşlerin Sepetleri | Sepetler yerine su altında hareketli metin etiketleri ağla yakalanıyordu. | Her birinde dört kırmızı elma bulunan iki gerçek sepet ve doğrudan seçilen dört karşılaştırma kartı yapıldı; yanlış uyarısının yerleşimi düzeltildi. | **Geçti** · “Biri daha çok” yanlış uyarısı; meyve, renk ve sayı benzerliklerinin üçü seçilerek tamamlama doğrulandı. |
| m26 | Uzay Üssü Geri Sayımı | Yönerge 20→1 dediği hâlde oyun yalnız 20,19,18,17,16'yı istiyordu. | Gerçek 20→1 geri sayımına çevrildi; her dokunuşta bir sayı ve bir roket azalıyor. | **Geçti** · 20→15→10→5→1 durakları ve tamamlama elle doğrulandı. |
| m27 | Zıpzıp Kurbağa | 5’er ritmik sayma yönergesine rağmen uzayda hareket eden sayı blokları roket yakıt hunisine atılıyordu; kurbağa ve sayma yolu yoktu. | 5, 10, 15, 20 nilüferlerinden oluşan sabit gölet yolu ve her doğru sayıda ilerleyen kurbağa sahnesi yapıldı. | **Geçti** · 12 için yanlış uyarısı/can; 5→10→15→20 sırasıyla dört zıplama ve tamamlama doğrulandı. |
| m28 | Yeraltı Madencisi | Belirgin bir mantık veya etkileşim hatası görülmedi. | Değişiklik gerekmedi. | **Geçti** · 20→19 inişi, 19→20 geri alma ve ardından 20’den 1. kata 19 ayrı dokunuşla kesintisiz iniş/tamamlama doğrulandı. |
| m29 | Büyülü Orman Yolu | Üçgen/kare/beşgen ve seçeneklerin yanında 3/4/5/6 sayıları yazıyor, doğru cevap şekli saymadan görülebiliyordu; Unicode çokgenleri de kenar saymaya elverişsiz küçüklükteydi. | Sayı etiketleri kaldırıldı; gerçek, büyük üçgen–kare–beşgen dizisi ile beşgen/altıgen/yıldız seçenekleri çizildi. | **Geçti** · beşgen için yanlış uyarısı/can, gerçek altıgen seçimi ve boş taşın tamamlanması doğrulandı. |
| m30 | Uzaylı Merdiveni | Sayı örüntüsü uzaylı ve merdiven olmadan aynı düz metin kartlarında gösteriliyordu. | 2, 4, 6, ? yazılı gerçek yükselen basamaklar, basamakları çıkan uzaylı ve 7/8/9 seçim kartları yapıldı. | **Düzeltildi · yeniden testte** · yerel tarayıcı izni otomatik engellendiği için yanlış/doğru dokunma ve bitiş henüz elle onaylanmadı. |
| m37 | Küçük İcatlar Pazarı | Sekiz bilye tahminden önce sayılabiliyor, seçeneklerde gerçek 8 yoktu. | Buzlu cam tamamen kapatıldı; 5/8/11 seçenekleri ve daha açık tahmin yönergesi verildi. | **Geçti** · 8 seçildi, sekiz bilye tek tek açılıp sayıldı ve oyun tamamlandı. |
| m48 | Sihirli Ayna | `10 □ = 8` ve `−2` gösterimi belirsiz, 1. sınıf için uygunsuzdu; hareketli kısa cevaplara dokunmak da gereksiz zorlayıcıydı. | Sorular “kaç çıkar / kaç ekle” diline, seçenekler doğal sayılara çevrildi; doğrudan dokunulan sabit cevap düzeni kullanıldı. | **Geçti** · 2, 3 ve 4 cevaplı üç tur arka arkaya elle tamamlandı. |
| t01 | Gökyüzü Çizeri | A çizme yönergesine rağmen rastgele uçan 1–5 meteorlarına dokunuluyordu. | Oyun gerçek üç çizgili A izleme mekaniğine geçirildi. | **Geçti** · iki eğik ve bir yatay çizgi sürüklenerek A tamamlandı. |
| t09 | Sihirli Daktilo | Dikte sözcüğü “aynı metin” filtresinde yutuluyor; DİNLE başarısız olsa bile oyun ses var sanıyordu. | Dikte ilk okumayı kendi sahnesinde yapıyor; DİNLE zorunlu tekrar okuyor ve köprü gerçek başarı değeri döndürüyor. | Yazma/tamamlama **Geçti** · NANE dört harfle tamamlandı. Fiziksel Android hoparlör testi **Cihaz sesi bekliyor**. |

## İlerleme

- Toplam katalog: **658 oyun**
- Bu yeni, elle oynanan kabul turunda güncel sürümü tamamen geçen: **30 oyun**
- Düzeltildi, son yeniden testi süren: **2 oyun** (M18 ve M30)
- Oynanışı geçen, fiziksel cihaz sesi bekleyen: **2 oyun**
- Kalan oyunlar sınıf ve ders sırasıyla bu belgeye eklenecek; otomatik test
  sonucu manuel kabul yerine kullanılmayacak.
