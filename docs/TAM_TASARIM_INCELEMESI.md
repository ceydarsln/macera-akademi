# Tam tasarım incelemesi — çalışma kaydı

635 oyunun teknik testten geçmesi, tasarımının veya animasyonunun onaylandığı anlamına gelmez.
Öncelikli dış hedef sinyalleri değerlendirildi: 12 somut hedef sahnedeki nesneye taşındı; 27 kavramsal sinyalden biri cümleye yerleştirme olarak düzeltildi, 26'sı doğrudan karar olarak uygun bulundu. Bu çalışma, 635 oyunun gerçek etkileşim, sonuç animasyonu ve tam tasarım kabulü yerine geçmez.

## Kesinti sonrası devam noktası

- `artifacts/tam-tasarim-incelemesi/sheets.json`: 106 pafta, 635 oyun, oyun başına üç tur görüntüsü.
- Pafta 001–106'nın tamamı ilk görünüm açısından incelendi: 635 oyun, 1905 başlangıç görünümü. Bu, üç turun oynanıp onaylandığı anlamına gelmez.
- İlk taramadaki 47 dış hedef sinyalinden Y47, Y62, Z01, G43, H26, H05, F07 ve F13 daha önce sahneye bağlanmıştı. Sonraki 39 sinyalin 12 somut örneği bu turda düzeltildi. 27 kavramsal sinyalin biri (Z33) gerçek cümle yuvasına dönüştürüldü; 26'sı doğrudan karar olarak uygun bulundu. Güncel teknik dış hedef sayısı 26'dır; bu sayı tek başına hata sayısı değildir.
- Görüntüler önceki katalog testlerinden gelir; yeni bir çalıştırma veya animasyon kanıtı değildir.
- `definitions.json` oyun tanımlarını içerir. İlk görünüm incelemesi, gerçek sürükleme ve sonuç animasyonu testinden ayrı tutulur.

## Açık bulgular

1. M17: apartmanın katları sahne altından kesiliyor; hedeflerin gerçek pencerelerde ve tamamen görünür olması gerekiyor.
2. M38: elma grupları/araba dar ekranda taşmış. Yönerge hareketi izlemeyi istiyor ama sahne statik işlem işareti göstererek cevabı veriyor.
3. Sayı çizme oyunları: çizim alanı geniş sahnede küçük kalıyor. Harf çizme oyunlarında başlıktan bağımsız tekrar eden uçak/gökyüzü teması var.
4. M18: dondurma hedefleri ve yazılar çakışıyor. M36: ölçülen gerçek nesne yerine yazılı kart görünüyor.
5. M41, M42, M45, M47, M49: büyük boşluk ve küçük işlem/emoji; eylem-sonuç gösterimi ayrıca incelenmeli.
6. M51: iade kamyonu küçük simge ve büyük kutu. M54: hedef sınırları çakışıyor. M58: gölge kontrastı zayıf.
7. T04,T06,T07,T09,T14,T21,T22,T30,T38,T46,T47,T48,T51,T54,T64: kelime yuvaları çizilmiş makine/vagondan kopuk; gerçek nesne üzerinde birleşme ve çıktı incelenmeli.
8. T02: sahne ve alt hedefler yineleniyor. T62: görsel okuma görevinde gerçek resim yerine metin var.
9. V01–V23: birçok sahnede küçük merkezi çizim ve aşırı boşluk. V02 vagon hedefi çok küçük; V06 balon kontrastı düşük; V07 fotoğraf sıralamasında gerçek çerçeveler yok. V10 kasa ve V18 paketleme hedefleri etiketli kutu gibi.
10. M59/M60 grafiklerinin başlangıçta boş olması tek başına hata sayılmadı; cevap sonrası gelişimi sınanmalı.
11. V24–V42: V24 kilim, V25 şekil kapıları, V29–V30 programlama ızgarası ve V31–V32 simetri alanı sahneyle ilişkili. V26–V28 deney araçları ve V33–V36 nesneleri hâlâ çok küçük. V27 cevap hücreleri görünen 3B nesnelerden kopuk. V38 hasat, V39–V42 grafik etkinliklerinde nesne etkileşiminin grafiğe yansıması ayrıca sınanmalı.
12. U01–U53: genel ilk sahne tasarımları konuya göre farklı, ancak çok sayıda metin oyunu küçük dekoratif emoji kullanıyor. U24/U38/U39 gibi ipucuna bağlı metin oyunlarında süsleme etkileşim kanıtı sayılmaz. U41'in geri dönüşüm hedefleri yazılı yuva; gerçek fabrika ayrıştırmasına dönüşmeli. U47 sesli oyun test ortamında sesi kapalı gösteriyor; gerçek ses akışı ayrıca test edilmeli.
13. Y47 deyim makinesi ve Y62 denge köprüsünün ilk turunda işaretlenen hedefler sonradan sahneye taşındı; diğer turların görsel kabulü ayrıca bekliyor.
14. Z01 tartışma çemberinde görüş seçenekleri karakterlerin/konuşma balonlarının altında ayrı butonlardı (madde 24'teki düzeltme ile değişti). Z12 kesme işareti ve Z13 bilgi denetiminde kararlar çizilmiş çalışma masasından ayrı. Kavramsal sınıflandırma için fiziksel metafor gerekir; mevcut davranışın etkileşim testi bekliyor.
15. U54–U90: metin türü için pano temaları çeşitli, fakat çoğu oyunda ilk iki tur cevap kartı sadece metin kutusuna bırakılıyor. U80 geri dönüşüm bandı, U83 bayram sabahı gibi başlıkların çizimi cevap eylemine doğrudan bağlı değil. U63 film şeridi ve U64 kürsü düzeninde seçenekler ayrı alanda; sonuç hareketi sınanmalı.
16. W01–W48: geometri ızgarası, simetri, kesir asansörü ve dokuma tezgâhı gibi nesneye bağlı düzenler var. W03 tren sinyallerinde ray çok küçük; W04 fasulye sırası tek küçük sayı etiketi; W06 tek-çift laboratuvarında küçük işlem kartı ve geniş boşluk; W07 mimarlık blokları küçücük. W14 kronometre arenası metin-sayı kutusu, kronometre çizimi yok. W17 zihin arenası sayı doğrusu ekranın ortasında küçük. W19 kargo bandı gerçek bant göstermiyor. W24 fırın tezgâhı başlangıçta yalnız sayaçlar. W25 üç boyutlu küp görevi büyük ve anlaşılır.
17. Y01–Y11: konuşma/dil oyunları için defter, matbaa ve stüdyo örnekleri var; Y03 sahnede ipucu görseli çok küçük. Y05 noktalama tamirhanesi ilk turda metin panosu göreve uygun. Y06 ses düzeyi ayarı görsel deney düzeyi ölçer/geri bildirimle pekiştirilmeli. Y10 zıt anlam aynası fiziksel aynada gerçek kartlar; Y11 yazım atölyesi görsel hedefe bağlı.
18. Y47 ve Y62'nin ilk tur hedefleri sahneye taşındı; tur 2–3 henüz genel tasarım onayı almadı. M17 ve M38 sahneleri güncellendi; doğrulama dosyaları `artifacts/apartman-market-denetimi` ve `artifacts/deyim-denge-denetimi` klasörlerinde.
19. P01–P56: P26 küp taraması, P27–P30 ölçerek çizme, P34 açı döndürme, P43–P47 simetri ızgaraları ve P49–P56 grafik/olasılık düzenleri konuya bağlıdır. P31–P33'te ölçme aracı sahnesi küçük veya yok; P48'in sıralama yuvaları anlatılan simetri çiziminden kopuk. Bazı P01–P25 sahnelerinde tek küçük nesne ve geniş boşluk var. Ölçme/çizme sonucunu görmeden onay verilmedi.
20. Z01–Z64: Z01'in fikir hedefleri, Z17/Z49'un somut sınıflandırma sahneleri ve Z33'ün cümle yuvası düzeltildi. Z12/Z13/Z26/Z29/Z31/Z40–Z42/Z50/Z51/Z56/Z57/Z62 doğrudan kavramsal karar olarak değerlendirildi; tek bir sahne şablonuna dönüştürülmedi. Metin düzeltme ve üretme turları ayrıca içerik/klavye denetimi gerektiriyor.
21. G01–G48: G13 kayaç, G19 hâl, G23 geri dönüşüm, G25 hareket, G31 elektrik, G37 bitki gibi özelleştirilmiş fiziksel sahneler var. G43 yaşam alanı hedefleri; G15/G16 maden ve G26/G30 kuvvet hedefleri sahneye bağlandı. G45 habitat eşleştirmesinin görsel sonucu ayrıca incelenmeli. G17/G33 dahil kavramsal sınıflandırmalar doğrudan karar olarak değerlendirildi; tam görsel kabul verilmedi.
22. F01–F48: F07 besin numunesi analiz kabına, F13 gözlem kartı Dünya modeline taşındı. F19/F20/F33/F37 somut sınıflandırmaları da artık sahnedeki nesnelere yapılıyor. F01/F43 doğrudan kavramsal karar olarak değerlendirildi. F30 pusula, F32/F34 devre ve F40/F41 ışık kirliliği maketinin tam etkileşim kabulü ayrıca bekliyor.
23. H01–H30: H08 kişisel alanı kaydırıcıyla, H10 telefonu tuşlarla, H12 afet çantasını nesnelerle, H27 yön bulmayı haritayla işliyor. H24 bayram sınıflandırması sahneye bağlandı; H01/H02/H14/H16 doğrudan kavramsal karar olarak değerlendirildi. H26'nın mevsim hedefleri, H05'in oy sandığı düzeltildi. H29 su deneyinin ve H13 nezaket oyununun tam görsel kabulü ayrıca bekliyor.
24. Z01'in iki sınıflandırma turunda görüş kartı çocukların konuşma balonlarına, G43'ün iki turunda canlı kartı ilgili yaşam alanına, H26'nın ilk turunda hava kartı mevsim bahçesine sürükleniyor. H05'in ilk turunda oy kartı sınıf sandıklarına giriyor ve sayım sandığın içinde görünür. Yanlış/iptal/telefon-yatay ekran denetimi `artifacts/sinif-sahneleri-denetimi` klasöründe 12 senaryo ile geçti. Bunlar oyunların bütün turlarına tasarım onayı değildir.

## 39 dış hedef sinyalinin sonucu

Bu sinyal yalnız `data-kutu` hedefinin `#stage` dışında olduğunu gösterir; tek başına sürükleme zorlandığı veya oyunun bozuk olduğu anlamına gelmez. İlk ayrım ve uygulama sonucu:

- **Somut hedefler (12/12 düzeltildi):** Z17 enerji kaynağı, Z49 miras örneği; G15 maden/eşya, G16 örnek sınıflama, G26/G30 kuvvet etkisi, G42 ürün yetişme yeri; F19 hâl değişimi, F20 ısı akışı, F33 enerji kaynağı, F37 ışık kaynağı; H24 bayram sahnesi. Her birinde farklı, konuya ait sahne nesneleri hedef olarak çizildi. Kaynak kart bu nesneye sürüklenebiliyor; yanlış nesne kabul edilmiyor, doğru nesnede öğe görünüyor. 320×568, 390×844 ve 844×390 ekranlarda 36 senaryo, 213 gerçek sürükleme ve yanlış/iptal denetimi geçti. [Ekran ve etkileşim kanıtları](../artifacts/somut-hedefler-12/index.html).
- **Kavramsal karar/okuma (27/27 değerlendirildi):** Z12/Z13/Z26/Z29/Z31/Z33/Z40/Z41/Z42/Z50/Z51/Z56/Z57/Z62; G01/G04/G10/G17/G33/G35/G46; F01/F43; H01/H02/H14/H16. Z33'te bağlaç sözcüğü artık gerçek cümle boşluğuna yerleşiyor; 320×568, 390×844 ve 844×390 ekranlarda gerçek sürükleme ve yanlış seçim testi geçti. Kalan 26 oyundaki `data-kutu` bir fiziksel kap değil, doğrudan anlam/karar seçimi olduğundan sahne dışı düğme uygundur. 28 turda yanlış yanıtın reddi, bütün kartların çözümü ve 390×844 taşma kontrolü geçti. [Kavramsal denetim paftası](../artifacts/kavramsal-hedef-denetimi/index.html).

Güncel dış hedef sayısı 26'dır ve hepsi kavramsal karar olarak açıklanmıştır. Bu, diğer 635 oyunun ya da bu 26 oyunun tüm turlarının görsel/oyun tasarımı onayı değildir.

## F07 ve F13 hedefli devam

- F07'nin ilk turunda besin örneği yalnızca fiziksel analiz kabının ağzına bırakılabiliyor; yanındaki yazı bırakma hedefi değil. Yerleştirme sonrasında kaptaki sıvı seviyesi değişiyor, numune içeride görünüyor. F13'te gözlem Dünya modelindeki dört görünür bölgeden birine bırakılıyor ve seçilen bölgede beliriyor. İki oyunun ikinci ve üçüncü turları bu düzenlemede değiştirilmedi.
- `artifacts/besin-dunya-denetimi/index.html`: 320×568, 390×844 ve 844×390 ekranları; altışar gerçek sürükleme, yanlış hedef ve iptal denetimi. `artifacts/katalog-kabul-635` üç turun teknik çözümünü kaydeder. Bunlar insan eliyle verilmiş tam tasarım onayı değildir.
