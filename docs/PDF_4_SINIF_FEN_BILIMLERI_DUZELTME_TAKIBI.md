# 4. Sınıf Fen Bilimleri PDF Düzeltme Takibi

Kaynak: `4_sinif_fen_bilimleri_oyunlari_detayli_duzeltmeler.pdf` (60 sayfa, f01–f48).
Bu, katalogdaki en büyük ders: 48 oyun, 8 tema, 11 motor.

Bu dosyada "tamamlandı" işareti yalnız şu altı koşul birlikte sağlanınca verilir:

1. Bilimsel model doğrudur — özellikle hâl değişimi sırasında sıcaklığın sabit kaldığı gösterilir.
2. Yanlış cevapta doğru cevap açılmaz; wrongHint metinleri doğru kutunun adını içermez.
3. Karar için gereken veri ekranda okunur biçimde bulunur (grafik hedefleri).
4. 390×844 telefon ekranında hiçbir kart kırpılmaz, parça yazısı kesilmez.
5. Ürün/model kazanımlarında ekranda gerçekten bir şey inşa edilir.
6. Üç kademeli tur bulunur ve son turda öğrenci kendi gözlemini/gerekçesini üretir.

## Motor dağılımı (test edilen 11 şablon)

| Motor | Şablon | Oyun | Öne çıkan sorun |
|---|---|---|---|
| beltSort | bant | 8 | wrongHint doğru cevabı söylüyor; kart kırpılıyor; 4 kutulu turda etiket taşıyor |
| orderSequence | roket | 8 | Deney basamakları ve bilimsel süreç roket-YAKIT sahnesinde |
| dragMatch | kopru | 8 | Parça yazılarının son sözcüğü kesiliyor (6'lı turda 6/6) |
| serveOrder | pizza | 7 | Ürün/model kazanımlarında ekranda hiçbir şey inşa edilmiyor |
| catchDrop | radar | 6 | Altı oyunun tamamı aynı yönerge: "Radarı sürükleyerek doğru cevabı yakala" |
| memoryPairs | hafiza | 4 | Uzay zemini; "Başla" yazısı kartların üstüne biniyor; can 6 (standart 3) |
| dragSlider | tren | 2 | Dünya'nın dönüşü ve ısınma tren-tünel oyununa bağlanmış |
| graphBuild | grafik | 2 | Hedef değerler ekranda yok; iki oyun da deneme-yanılmayla çözülüyor |
| sentenceBuild | matbaa | 1 | Büyük harf ve soru işareti kartı dizilişi ele veriyor |
| holdFill | kronometre | 1 | Kronometre var ocak yok; hedef 3 yerde; **hâl değişimi yanlış modelleniyor** |
| codeGrid | kargo | 1 | Şehir planı yok, düz labirent; güzergâh gerekçesi kurulmuyor |

## Doğrulanmış öncelikli hatalar

| # | Hata | Kanıt | Etkilenen |
|---|---|---|---|
| 1 | Yanlışta doğru cevap ekrana yazılıyor | 67 bant kartının tamamında wrongHint tanımlı; ölçümde 65'i doğru kutu adını içeriyor ("Katı → sıvı = ERİME!") | 8 bant oyunu |
| 2 | Hâl değişimi yanlış modelleniyor | f21: gösterge 0'dan hedefe düz doğrusal artıyor; kaynama sırasında sıcaklığın sabit kaldığı gösterilmiyor | f21 |
| 3 | Grafik hedefleri ekranda yok | f36 (Güneş 3, Rüzgâr 2, Hidro 2, Kömür 3) ve f47 (5/3/4/2) kodda tanımlı, ekranda yok | f36, f47 |
| 4 | Parça yazıları kesiliyor | f46: 6 parçanın 6'sında son sözcük okunmuyor | 8 köprü oyunu |
| 5 | Bant kartı kırpılıyor + sözcük sızıntısı | f19: "Çaydanlıktan buhar çıkar" → yalnız "buhar" görünüyor, cevabı ele veriyor | 8 bant oyunu |
| 6 | Ortak şablon yönerge | f02, f12, f16, f27, f35, f39: aynı radar metni | 6 radar oyunu |
| 7 | Hedef üç yerde söyleniyor | f21: görev metni + "Hedef 100 °C" + ölçek çizgisi | f21 |

f01–f48 arasındaki 48 oyunun tamamı yüklendi; motorlarda çökme veya konsol hatası oluşmadı.

## Olumlu fark

**Emoji sızıntısı bu derste neredeyse yok.** Sekiz köprü oyunundaki 40 eşleşme tek tek
karşılaştırıldı; parça ile hedefin aynı emojiyi paylaştığı yalnız 1 durum bulundu
(f08 Vitamin Köprüsü: havuç simgesi hem "A vitamini" parçasında hem hedefinde).
2–3. sınıf hayat bilgisi ve 3–4. sınıf Türkçe derslerinde bu kusur yaygındı.
Köprü motoru düzeltilirken bu dersin içerik kurgusu örnek alınabilir.

## Oyun listesi (tema bazlı özet)

| Tema | Oyunlar | Ana sorunlar |
|---|---|---|
| 1 · Bilime Yolculuk | f01–f06 | wrongHint sızıntısı, radar yönergesi, roket sahnesi |
| 2 · Sağlıklı Besleniyorum | f07–f12 | wrongHint, tabak kurulmuyor, radar yönergesi |
| 3 · Dünya'mızı Keşfedelim | f13–f18 | 4 kutulu bant taşması, tren-tünel süre ölçeri, radar yönergesi |
| 4 · Maddenin Değişimi | f19–f24 | **Kart kırpılması + kavram sızıntısı; hâl değişimi yanlış modeli** |
| 5 · Mıknatısı Keşfediyorum | f25–f30 | wrongHint, radar yönergesi, pusula kurulmuyor |
| 6 · Enerji Dedektifleri | f31–f36 | Devre kurulmuyor, arıza radarı, **grafik verisi yok** |
| 7 · Işığın Peşinde | f37–f42 | wrongHint, radar yönergesi, ışık kirliliği sahnesi yok |
| 8 · Sürdürülebilir Şehirler | f43–f48 | **Köprü yazı kesilmesi**, maket kurulmuyor, **grafik verisi yok**, labirent |

Oyun bazında ayrıntı PDF'in ilgili sayfalarındadır (her oyun bir sayfa).

## Uygulama sırası önerisi

1. **f21'in bilimsel modeli** — hâl değişimi sırasında sıcaklığın sabit kalması bu temanın çekirdeği; şu an tersi öğretiliyor
2. **wrongHint metinleri (65 kart, 8 oyun)** — içerik düzeltmesi, motor değişikliği gerektirmez, en yüksek etki/çaba oranı
3. f36 ve f47'de grafik hedeflerinin ekrana yazılması (sosyal bilgilerdeki sb25 ile aynı düzeltme)
4. Köprü yazı kesilmesi (8 oyun) ve bant kartı kırpılması (8 oyun) — diğer derslerle ortak motor düzeltmesi
5. Altı radar yönergesinin oyuna özel yeniden yazılması
6. Roket sahnesinin 8 sıralama oyunundan kaldırılması
7. Ürün/model kazanımlarında (f24, f30, f34, f44) ekranda gerçek inşa

## Uygulama durumu

Düzeltmeler `web/phaser/fen4-pdf-phaser.html` altında sıfırdan yazılan derse özel
motorla uygulanıyor; katalogdaki oyunlar parti parti `PHASER_OYUNLAR` üzerinden
bu motora bağlanıyor. Motorda bant, radar-kapsül, roket-yakıt, tren-tünel,
kronometre ve köprü ortak sahneleri hiç yok.

Her parti iki araçla sınanıyor:
- `tools/fen4_denetim.html?ids=f01,f02,…` — her turu 390×844'te açıp kırpılma,
  44 px dokunma alanı, simge sızıntısı ve cevap sızıntısı tarar (kabul ölçütü 2–4).
- `tools/fen4_kosum.html?ids=…` — her oyunu baştan sona gerçekten oynar; üç tur
  bitiyor mu, doğru oynayan can kaybediyor mu diye bakar (ölçüt 6).
- Motorun içindeki `window.__TEST__.denetle()` metin düzeyinde tarar:
  wrongHint doğru kutunun adını içeriyor mu, son tur öğrenci üretimi mi,
  sıralama turunda ekran dizilişi cevabı veriyor mu, `ornekCevap` kendi
  ölçütlerini geçiyor mu.

| Oyun | Eski motor | Yeni sahne ve turlar | Durum |
|---|---|---|---|
| f01 Bilimsel mi? | bant | laboratuvar defteri · sınıfla → karar+gerekçe → yaz | ✅ uygulandı |
| f02 Kaynak Masası | radar | araştırma masası, künyeli kartlar · karar → karşılaştırma → yaz | ✅ uygulandı |
| f03 Araştırma Adımları | roket | araştırma defteri, adımlar deftere yazılır · sıra → karar → yaz | ✅ uygulandı |
| f04 Bilim İnsanı Atölyesi | köprü | laboratuvar, eşleşme sahnede canlanır · eşle+gerekçe → karar → yaz | ✅ uygulandı |
| f05 Araştırma Çantası | tepsi | çanta ekranda gerçekten dolar · kur → karar → yaz | ✅ uygulandı |
| f06 Araştırma Sorusu Defteri | matbaa | kartlar küçük harfle gelir, baş harf ve "?" öğrencinin kararı | ✅ uygulandı |
| f07 Besin İçeriği Masası | bant | besin masası + içerik etiketi (sayılar ekranda) | ✅ uygulandı |
| f08 Vitamin Pazarı | köprü | pazar tezgâhı, etiketlerde simge yok (tek sızıntı noktası kapandı) | ✅ uygulandı |
| f09 Dengeli Tabak | tepsi | tabak ekranda gerçekten dolar, eksik grup yazılı · kur → karar → yaz | ✅ uygulandı |
| f10 Besin İşlevi Kartları | hafıza | vücut şeması önünde kart, can 3, her eşleşme gerekçeli | ✅ uygulandı |
| f11 Besin Testi Deneyi | roket | deney tezgâhı, değişken kontrolü · sıra → karar → yaz | ✅ uygulandı |
| f12 Beslenme ve Sağlık | radar | öncesi-sonrası sahnesi, kısa/uzun vade ayrımı | ✅ uygulandı |
| f13 Küre Kesiti | bant (4 kutu) | öge kesitte vurgulanır, kutu etiketi kutuda kalır | ✅ uygulandı |
| f14 Taş Kürenin İçi | roket | katmanlar kesitte içten dışa oluşur, ölçüm tablosu ekranda | ✅ uygulandı |
| f15 Dünya'nın Hareketleri | köprü + tren | **gözlem kipi**: Dünya döner, gece-gündüz gözlenerek bulunur | ✅ uygulandı |
| f16 Dünya'nın Şekli | radar | gemi/gölge/uydu kanıtları sahnede, kanıt-duyum ayrımı | ✅ uygulandı |
| f17–f48 | — | — | PDF'de |

Parti 1'de (f01–f08) kapatılan doğrulanmış hatalar: **#1** wrongHint sızıntısı
(bu partideki bant oyunları f01 ve f07'de ipuçları artık doğru kutunun adını
içermiyor, motorun öz denetimi bunu sınıyor), **#5** bant kartının kırpılması
(kart artık sabit ve tam genişlikte), **#6** ortak radar yönergesi (f02 kendi
konusunu anlatıyor) ve köprüdeki tek simge sızıntısı (f08).

### Parti 2 (f09–f16) notları

Kapatılan doğrulanmış hatalar: **#6** radar yönergesi (f12 ve f16 kendi konularını
anlatıyor, seçenekler sabit), **#5/#1** bant kusurları (f13'te dört kutulu tur;
etiketler kutu içinde kalıyor, ipuçları kutu adını söylemiyor), roket sahnesi
(f11, f14) ve hafıza motorunun uzay zemini ile 6 canı (f10 artık 3 can, kartlar
konunun sahnesinde ve her açılışta karışıyor).

Bu partide iki yeni kip yazıldı:
- **gözlem** — tren-tünel ve kronometrenin yerine geçiyor. Ölçülen olgu ekranda
  canlanıyor; gözlem yapılmadan seçenekler açılmıyor, yeniden izlemek ceza değil.
- **hafıza** — yanlış çiftte kartlar hemen kapanmıyor, iki içerik yan yana okunup
  farkı soruluyor; her doğru çift bir gerekçe adımıyla doğrulanıyor.

Sınama sırasında bulunan ve düzeltilen üç gerçek kusur:
1. **Gizli sekmede `requestAnimationFrame` hiç çalışmıyor.** Yalnız ona bağlanan
   gözlem animasyonu orada sonsuza kilitleniyor ve tur çözülemez hâle geliyordu
   (uygulama arka plana alındığında öğrenci hiç cevap veremezdi). Kare isteği
   artık rAF ile zamanlayıcının ilk çalışanına bağlanıyor; `t` duvar saatinden
   hesaplandığı için seyrek tik animasyonu yavaşlatır ama durdurmaz.
2. **Aydınlık yarım küre Güneş'in tersine bakıyordu.** Dünya-Güneş sahnesi
   kuzey kutbunun üstünden bakış olarak yeniden çizildi; karanlık yarım küre
   her zaman Güneş'ten kaçıyor ve şehrin gündüz mü gece mi olduğu yazıyor.
   Bu, f15'in öğretmek istediği kavramın ta kendisiydi.
3. **f14'te seçenek metni ölçüm satırındaki sayıyı birebir tekrar ediyordu**
   ("Manto (~2900 km)"); karar karşılaştırma olmaktan çıkıp eşleştirmeye
   dönüyordu. Tablo ekranda kaldı (ölçüt 3), sayı seçeneklerden kaldırıldı.

Sınama: `fen4_denetim.html` f01–f16 için 48 turun tamamında temiz;
`fen4_kosum.html` on altı oyunu baştan sona oynayıp can kaybetmeden bitiriyor;
`window.__TEST__.denetle()` 16 oyunda kusursuz.
