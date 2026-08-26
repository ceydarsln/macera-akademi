# 3. Sınıf Türkçe PDF Düzeltme Takibi

Kaynak: `output/pdf/3_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf` (76 sayfa, y01–y64).
Şartnamenin yapılandırılmış hâli: `tmp/spec_y.json` (PDF üretici betiğinden `tmp/pdfs/extract_turkish3_spec.py` ile çıkarıldı).
Motor: `web/phaser/turkce3-pdf-phaser.html` (matematik4 çatısı + Türkçeye özel oynatıcılar).
Katalog bağlantısı: `PHASER_OYUNLAR` haritasında y01–y64 → `turkce3-pdf`.

**Durum: 64/64 oyun uygulandı** (son güncelleme: 26 Ağustos 2026).

Bu dosyada "Uygulamada" işareti yalnız şu beş koşul birlikte sağlanınca verilir:

1. Başlıktaki sahne ve karakter, ölçülen Türkçe becerisinin gerçek parçasıdır.
2. Ekranda cevabı sızdıran hiçbir öge yoktur (yazılı dikte sözcüğü, işaret adı, tarih sırası, simge kopyası, sütun adı).
3. Üç farklı tur, değişen içerik ve değişen doğru konumuyla baştan sona oynanır.
4. Yanlış cevap doğruyu söylemeden, içerik üzerinde nedenini gösterir; motor/refleks hatası can kaybettirmez.
5. 390×844 telefon ekranında hiçbir metin kırpılmaz/taşmaz ve dokunma alanları en az 44 px'tir.

## Kaldırılan ortak motorlar

Şartnamenin ana bulgusu, başlıkla ilgisiz ortak motorlardı. Hepsi bu derste kaldırıldı:

| Kaldırılan | Yerine gelen | Kaç oyunda |
|---|---|---|
| Yürüyen bant (kart kenarda kırpılıyor, hız karara karışıyor) | Duraklı şerit: kart karar verilene kadar ortada ve tam görünür | 8 |
| Roket–yakıt hunisi (kartlar uzayda süzülüyor) | Sabit yuvalı sıra şeridi / gerçek şema (zaman şeridi, su döngüsü, kitap, tören) | 5 |
| Tren–tünel sürgüsü (hiç ses dinletilmiyor) | Gerçek ortam + her düzeyde **gerçekten o ses şiddetinde** örnek | 3 |
| Radar–kapsül yakalama (refleks karara karışıyor) | Sabit seçenek + karar öncesi kanıt işaretleme | 4 |
| Daktilo (hedef sözcük balonda yazılı) | Dikte: sözcük yalnız seste, harf havuzu karışık, tekrar dinleme cezasız | 3 |
| Hafıza kartı (6 can, konum ezberi) | Açık iki sütun eşleştirme + gerekçe adımı; can 3'e çekildi | 5 |
| Tepsi–servis (balon simgesi kart simgesiyle aynı) | Kartlarda etiket değil **içerik**; seçim metinden çıkarımla | 7 |

## Yazma kazanımı: ekran klavyesi ve ölçüt (rubrik) motoru

64 oyunun **36'sı yazma** kazanımı. Şartname "hazır kartı seçmek ya da dizmek gerçek yazma
kanıtı değildir" diyor. Bu yüzden motora Türkçe ekran klavyesi eklendi:

- 29 harf + boşluk + `. ? ! , ’ :` + isteğe bağlı rakam sırası (`rakam:true`).
- Büyük harf ayrı bir karar: `state.buyuk` başta açık, her harften sonra kapanıyor; `İ/I/Ş/Ğ/Ü/Ö/Ç` için Türkçeye özel büyütme haritası kullanılıyor (`toUpperCase()` i→I yapıyor).
- Doğruluk tek bir cevapla değil **ölçütlerle** sınanıyor: `buyuk`, `nokta`, `bitis`, `sozcuk>=N`, `cumle>=N`, `icerir:`, `icermez:`. Ölçütler yazarken canlı ✅/⬜ işaretleniyor.
- "Bitir" düğmesi eksik ölçütü **adıyla** söylüyor, doğru cümleyi söylemiyor.
- Sözcük çipleri yalnız erişim desteği; tek başına başarı sayılmıyor.

## Doğrulama

1. **Tam koşum:** `tools/dom_kosum.html#ids=y01,…,y64` — 64 oyun × 3 tur, tamamı geçiyor.
   Çözücü `tur8()`; yazma turlarında örnek cevap **ekran klavyesinin tuşlarına basılarak** yazılıyor,
   böylece klavye yolu her turda sınanmış oluyor.
2. **Motor öz denetimi:** `__TURKCE3_TEST__.olcutDenetimi()` — her yazma turunun örnek cevabı
   kendi ölçütlerini geçiyor mu ve her karakteri ekran klavyesinde var mı? (Bu denetim y17, y20,
   y13 ve y54'teki dört hatayı koşuma girmeden yakaladı.)
3. **Düzen ve sızıntı denetimi:** `tmp/y_denetim.html` — 64 oyun × 3 tur; 390×844'te yatay taşma,
   ekran dışına çıkan öge, `elementFromPoint` ile gerçek isabet testi ve
   "yönerge/sahne doğru seçeneği birebir söylüyor mu" sızıntı kontrolü. **64/64 temiz.**
4. **Uygulamada elle deneme:** katalogdan y01, y05 ve y07 gerçek tıklamalarla açılıp oynandı.

### Geliştirme sırasında bulunup düzeltilenler

| Bulgu | Düzeltme |
|---|---|
| Cümle kurma "bütün kartları kullan" diyordu; şartname 2. turda çeldirici sözcük istiyor | Geçerlilik yalnız kabul edilen dizilişlerle sınanıyor |
| Klavyede kesme işareti yoktu (`TBMM’de`, `Samsun’a` yazılamıyordu) | `’` tuşu eklendi |
| Klavyede iki nokta yoktu (`Gözlem:` yazılamıyordu) | `:` tuşu eklendi |
| Klavyede rakam yoktu (`23 Nisan` yazılamıyordu) | Tura özel rakam sırası (`rakam:true`) |
| `speechSynthesis.onend` sesi kapalı cihazda hiç gelmiyor, sahne kilitleniyordu | Her seslendirmeye emniyet süresi |
| İki oyunda çeldirici seçenek `C('...',{})` yazıldığı için **doğru** sayılıyordu | `C('...')` olarak düzeltildi; kaynakta tarama yapıldı |
| Okuma panelinde kısa sözcüklerin dokunma alanı 24 px altındaydı | `w` ögesi `inline-block` + iç boşluk, satır aralığı 1.9 |

## Oyun oyun durum

| ID | Oyun | Kaldırılan motor | Uygulanan ana düzeltme | Durum |
|---|---|---|---|---|
| y01 | Dinleme Stüdyosu | bant | Karanlık bant gitti; gerçek kayıt stüdyosu, davranışlar kısa canlandırma sahnesi ve kart sabit. 3. turda çocuk söz alma kuralını kendi cümlesiyle yazıyor. | Uygulamada |
| y02 | Erdem Kâşifi | hafıza kartı motoru | Uzay sahnesi ve 6 can gitti; kartlar açık iki sütunda eşleşiyor, yakın erdem çeldiricileri var, son turda kendi örneği yazılıyor. | Uygulamada |
| y03 | Hikâye Kâhini | radar/kapsül yakalama motoru | Düşen kapsüller gitti; küre sabit. Çocuk önce hangi ipucunu kullandığını işaretliyor, son turda “Bence … çünkü …” kalıbını kuruyor. | Uygulamada |
| y04 | Yayınevi Masası | tepsi-servis motoru | Servis tezgâhı ve simge kopyası gitti; kartlarda KONU/ANA FİKİR etiketi değil aday cümleler var. Son turda ana fikir kendi cümlesiyle yazılıyor. | Uygulamada |
| y05 | Noktalama Tamirhanesi | tamirhane motoru | Yönerge artık işaretin adını söylemiyor, “Kalan” sayacı kaldırıldı; yanlışta cümle o işaretin tonuyla okunuyor. Son turda bozuk cümle baştan yazılıyor. | Uygulamada |
| y06 | Ses Düzeyi Ayarı | tren-tünel motoru | Tren-tünel gitti; her düzeye dokununca örnek cümle GERÇEKTEN o ses şiddetinde okunuyor. Son tur öz değerlendirmeli konuşma. | Uygulamada |
| y07 | Cümle Kurma Makinesi | matbaa/baskı kızağı motoru | Kartlar küçük harfle geliyor; baş harf ve son işaret çocuğun ayrı kararı. Kurallı alternatif dizilişler kabul ediliyor, havuzda çeldirici sözcük var. | Uygulamada |
| y08 | Erdem Kalemi | dedektif tutanağı motoru | Metin panelden taşmıyor, büyüteç yok; cevap seçenekleri ancak KANIT işaretlendikten sonra açılıyor. | Uygulamada |
| y09 | Zaman Şeridi | roket-yakıt motoru | Roket-yakıt gitti; gerçek zaman şeridi. İlk turda tarihler gizli, sıralama olay metninden yapılıyor. | Uygulamada |
| y10 | Zıt Anlam Aynası | hafıza kartı motoru | Ayna odası; bağlama duyarlı çiftler (binmek-inmek, erken-geç) ve kendi karşılaştırma cümlesi. | Uygulamada |
| y11 | Kısaltma Atölyesi | bant | Bant akışı gitti; kural kutusu ekranda kalıyor, ek OKUNUŞA göre seçiliyor, son turda kesme işareti çocuk tarafından konuyor. | Uygulamada |
| y12 | Neden-Sonuç Köprüsü | eşleştirme köprüsü motoru | Köprü görseli kuruldu, çipe sığan kısa metinler; aynı ilişki “çünkü” ve “bu yüzden” ile iki yönde kuruluyor. | Uygulamada |
| y13 | Özel Ad Tamirhanesi | tamirhane motoru | Özel ad türleri ayrıldı; “mayıs/Mayıs” gibi bağlama duyarlı çeldiriciler var. Son turda cümle baştan yazılıyor (rakam sırası açık). | Uygulamada |
| y14 | Kahramanlık Diktesi | daktilo motoru | Hedef sözcük hiçbir yerde yazmıyor; harf havuzu karışık, benzer sesler (c/ç, g/ğ) çeldirici, tekrar dinleme cezasız. | Uygulamada |
| y15 | Doğru Bilgi Radarı | radar/kapsül yakalama motoru | Radar-kapsül gitti; her kartın yanında kaynak var ve “kısmen doğru” ayrımı yapılıyor. | Uygulamada |
| y16 | Bayram Mesajı Makinesi | matbaa/baskı kızağı motoru | Kartlar küçük harfle; hitap virgülü ve kutlama ünlemi birlikte çalışılıyor, son turda kendi mesajı yazılıyor. | Uygulamada |
| y17 | Doğa Ayırma Bandı | bant | Bant hızı gitti; ham-işlenmiş ayrımı (pamuk/tişört, süt/peynir) ölçüt tartışmasıyla veriliyor. | Uygulamada |
| y18 | Afet Çantası Robotu | kargo/robot ızgara motoru | Yön okları YAZILI yönerge kartlarına dönüştü; program cümle olarak okunuyor, robot okurken uyguluyor. | Uygulamada |
| y19 | Doğa Dergisi Masası | tepsi-servis motoru | Tepsi gitti; bölümler sayfa taslağına yerleşiyor ve bölüm adı ile İÇERİĞİ eşleştiriliyor. | Uygulamada |
| y20 | Eş Anlam Ormanı | hafıza kartı motoru | Orman sahnesi; “ak akçe” gibi kalıplaşmış kullanımda eş anlamlının yer değiştiremediği gösteriliyor. | Uygulamada |
| y21 | Doğa Günlüğü Tamiri | tamirhane motoru | Defter sayfası; iki nokta ve tırnak görevleriyle veriliyor, konuşma aktarımı ayrı turda çalışılıyor. | Uygulamada |
| y22 | Yağmur Döngüsü | roket-yakıt motoru | Roket gitti; gerçek su döngüsü şeması. 2. turda döngüye ait olmayan çeldirici adım var. | Uygulamada |
| y23 | Mevsim Basamakları | sırık/basamak motoru | Bağlam cümlesi ekranda sürekli duruyor; yanlışta can gitmiyor (noPenalty). Son tur öz değerlendirmeli konuşma. | Uygulamada |
| y24 | Yarım Metin Atölyesi | matbaa/baskı kızağı motoru | Yarım metin panelde duruyor; kişi, zaman ve konu tutarlılığı kanıt işaretlenerek sınanıyor. | Uygulamada |
| y25 | Kütüphane Görevlisi | tepsi-servis motoru | Kapaktan tür çıkarımı yapılıyor; aynı türde iki kitaptan okurun ilgisine uyan seçiliyor. | Uygulamada |
| y26 | Yazım Hatası Avcısı | dedektif tutanağı motoru | Kalem otomatik düzeltmiyor; doğru yazımı çocuk seçiyor. “de/da” ayrı-bitişik kuralı ayrı turda. | Uygulamada |
| y27 | İki Metin Terazisi | bant | İki metin YAN YANA; “aynı konu” ile “aynı ileti” ayrımı vurgulanıyor. | Uygulamada |
| y28 | Eş Anlam Köprüsü | eşleştirme köprüsü motoru | Sözcükler kısa cümle bağlamıyla veriliyor; “ihtiyar ağaç” örneğiyle bağlam sınırı tartışılıyor. | Uygulamada |
| y29 | Mektup Yazı İşleri | tamirhane motoru | Gerçek mektup şablonu; hitap virgülü, tarih yazımı ve kapanış birlikte çalışılıyor. | Uygulamada |
| y30 | Okur Kimliği Anketi | çetele motoru | Yanıtlar sütun adını birebir söylemiyor; işaretler çetele çizgisiyle birikiyor, beşinci çizgi dördünü kesiyor. | Uygulamada |
| y31 | Kitap Anatomisi | roket-yakıt motoru | Roket gitti; bölümler sıralandıkça kitap kuruluyor ve bölüm İŞLEVİ eşleştiriliyor. | Uygulamada |
| y32 | Dilek Kutusu | matbaa/baskı kızağı motoru | Önce tür (istek/şikâyet/öneri) seçiliyor; aynı konu üç türde karşılaştırılıyor, son turda nazik dil rubriği uygulanıyor. | Uygulamada |
| y33 | Sanat Atölyesi Siparişi | tepsi-servis motoru | İstek malzeme adını söylemiyor; teknikten çıkarım yapılıyor, çekici ama amaca uymayan araç çeldirici. | Uygulamada |
| y34 | Yetenek Ayırma Bandı | bant | Bant hızı gitti; ritmik jimnastik gibi iki alana uyan etkinlikte ölçüt seçilip savunuluyor. | Uygulamada |
| y35 | Duygu Noktalaması | tamirhane motoru | Replik seçilen işarete göre FARKLI TONDA seslendiriliyor; aynı cümle üç işaretle karşılaştırılıyor. | Uygulamada |
| y36 | Vurgu ve Tonlama Ayarı | tren-tünel motoru | Tren gitti; her düzey gerçek sesle. Vurgu yeri değişince anlamın değiştiği örnekler karşılaştırılıyor. | Uygulamada |
| y37 | Benzetme Makinesi | matbaa/baskı kızağı motoru | Benzeyen-benzetilen-yön görselleşti; anlamsız benzetmenin neden komik olduğu tartışılıyor. | Uygulamada |
| y38 | Jest ve Mimik Aynası | hafıza kartı motoru | Kartlarda yüz ve BEDEN ipucu ayrı veriliyor; şaşkınlık-korku, mutluluk-heyecan çeldiricileri var. | Uygulamada |
| y39 | Sözcük Anlamı Radarı | radar/kapsül yakalama motoru | Kapsüller gitti; cümle sabit panelde, karar öncesi bağlam ipucu işaretleniyor. Aynı sözcük ikinci bağlamda farklı anlamda. | Uygulamada |
| y40 | Yetenek Basamakları | sırık/basamak motoru | Hikâye metni ekranda duruyor; tahminler metindeki kanıta bağlanıyor, düşme cezası yok. | Uygulamada |
| y41 | Gerçek mi Mecaz mı? | bant | Bant hızı gitti; cümle sabit okunur kartta, koyu sözcük vurgulu. Aynı sözcüğün iki kullanımı yan yana. | Uygulamada |
| y42 | Atasözü Köprüsü | eşleştirme köprüsü motoru | Anlam ile sözcük benzerliği ayrıldı; yakın anlamlı atasözü çeldiricileri var. | Uygulamada |
| y43 | Kodlama Laboratuvarı | kargo/robot ızgara motoru | Yön blokları yazılı yönerge kartlarına dönüştü; hatalı programı okuyup adımı bulma görevi eklendi. | Uygulamada |
| y44 | Mucit Atölyesi | tepsi-servis motoru | İstek amaç-araç-adım içeren deney planı olarak okunuyor; çekici ama planı bozan araç çeldirici. | Uygulamada |
| y45 | Deney Raporu Tamiri | tamirhane motoru | Gerçek rapor şablonu; iki nokta ve virgülle listeleme birlikte kullanılıyor. | Uygulamada |
| y46 | Gürültü Ölçer | tren-tünel motoru | Tren gitti; ölçer gerçek ses örnekleriyle çalışıyor, aynı ortamın farklı saatleri karşılaştırılıyor. | Uygulamada |
| y47 | Deyim Makinesi | matbaa/baskı kızağı motoru | Deyim bölünmez tek blok; uygun bağlam seçiliyor ve son turda kendi cümlesi yazılıyor. | Uygulamada |
| y48 | Araştırma Adımları | roket-yakıt motoru | Roket gitti; bilim panosunda soru-kaynak-not-sunum akışı ve “atlanan adım” görevi var. | Uygulamada |
| y49 | Müze Rehberi | tepsi-servis motoru | İstek eserin adını söylemiyor; işlev ve biçimden çıkarım yapılıyor, benzer eserlerde şehir/mimar ayırt ediliyor. | Uygulamada |
| y50 | Türkçe Koruma Kalemi | dedektif tutanağı motoru | Kalem otomatik değiştirmiyor; Türkçe karşılık bağlama göre seçiliyor (online → çevrim içi). | Uygulamada |
| y51 | Bayram Panosu Dizgisi | tamirhane motoru | Özel adlar karışık cümlelerde; tarih yazımı ve kesme işareti ekleniyor, düzelen cümle panoya asılıyor. | Uygulamada |
| y52 | Eser Haritası | hafıza kartı motoru | Harita sahne oldu; eşleşme kısa bilgi cümlesiyle kanıtlanıyor, aynı şehirden iki eser çeldirici. | Uygulamada |
| y53 | Tören Sırası | roket-yakıt motoru | Roket gitti; adımlar sıralandıkça tören canlanıyor, araya karışan yanlış adım bulunuyor. | Uygulamada |
| y54 | Kültür Bekçisi | bant | Bant hızı gitti; niyet-etki ayrımı (iyi niyetle silmek de zarar verir) ikinci turda çalışılıyor. | Uygulamada |
| y55 | Vatan Şiiri Makinesi | matbaa/baskı kızağı motoru | Kartlar küçük harfle, işaret çocuğun kararı; coşku tonuna uymayan sözcük çeldirici. | Uygulamada |
| y56 | Kültür Diktesi | daktilo motoru | Hedef sözcük balonda yazmıyor; kültür sözcükleri görsel kartla destekleniyor, “ğ” sesi ayrı turda. | Uygulamada |
| y57 | Hak mı Sorumluluk mu? | bant | Bant gitti; aynı konunun hak ve sorumluluk çifti birlikte veriliyor. | Uygulamada |
| y58 | Dilekçe Masası | tepsi-servis motoru | Gerçek dilekçe şablonu; bölüm sırası ve içeriği eşleştiriliyor, kişisel veri istenmiyor. | Uygulamada |
| y59 | Hak Bildirisi Tamiri | tamirhane motoru | İşaret seçimi cümlenin ANLAMINI nasıl değiştirdiğiyle gösteriliyor; aynı cümle üç sahnede karşılaştırılıyor. | Uygulamada |
| y60 | Pekiştirme Diktesi | daktilo motoru | Hedef sözcük yazmıyor; bitişik yazım kuralı ekranda kalıyor, farklı pekiştirme türleri dinletiliyor. | Uygulamada |
| y61 | Güvenli Yol Yönergesi | kargo/robot ızgara motoru | Yön blokları yazılı yönergeye dönüştü; tehlike noktaları gerekçeli, iki rotadan güvenli olan seçiliyor. | Uygulamada |
| y62 | Denge Köprüsü | eşleştirme köprüsü motoru | Çipe sığan kısa metinler; bir hakka birden çok sorumluluk bağlanabildiği gösteriliyor. | Uygulamada |
| y63 | Söz Hakkı Makinesi | matbaa/baskı kızağı motoru | Kürsüde cümle sesli okunuyor; kaba, çekingen ve uygun üslup karşılaştırılıyor. | Uygulamada |
| y64 | Gizlilik Kalkanı | radar/kapsül yakalama motoru | Kalkan-yakalama gitti; karar gerekçe seçilerek veriliyor ve bağlama göre değişen örnekler var (okulda söylerim, internette yazmam). | Uygulamada |
