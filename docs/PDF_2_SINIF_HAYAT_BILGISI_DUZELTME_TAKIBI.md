# 2. Sınıf Hayat Bilgisi PDF Düzeltme Takibi

Kaynak: `2_sinif_hayat_bilgisi_oyunlari_detayli_duzeltmeler.pdf` (46 sayfa, h01–h36).

Bu dosyada "tamamlandı" işareti yalnız şu altı koşul birlikte sağlanınca verilir:

1. Ölçülen kavram mekaniğin içinde bulunur (yön oyununda güneş ve yön adları, mesafe oyununda gerçek mesafe, tasarruf oyununda akan su).
2. Cevap ekranın hiçbir yerinde yazılı değildir — başlık, alt başlık, görev metni, kart etiketi, ölçek çizgisi dâhil.
3. Tanıma gerektiren kazanımlarda gerçek görsel kullanılır (trafik levhası, tarihî mekân, teknoloji ürünü).
4. Parça ile hedefi eşleyen emoji/renk ipucu yoktur.
5. 390×844 telefon ekranında hiçbir kart kırpılmaz, yazı taşmaz; dokunma alanları en az 44 px.
6. Üç kademeli tur bulunur ve son turda öğrenci kendi örneğini söyler, yazar ya da uygular.

## Motor dağılımı (test edilen 13 şablon)

| Motor | Şablon | Oyun | Öne çıkan sorun |
|---|---|---|---|
| beltSort | bant | 6 | Kart sol kenarda tamamen kırpılıyor; kutu emojileri cevabı veriyor; 4 kutulu turda etiket taşıyor |
| serveOrder | pizza | 5 | Kartlarda "GÜÇLÜ:/GELİŞİM:/PLAN:" kategori etiketi yazılı — içerik okunmadan çözülüyor |
| orderSequence | roket | 5 | Dünyevi konularda (acil çağrı, Atatürk, teknoloji) roket-YAKIT sahnesi |
| catchDrop | radar | 4 | Karar süresi düşme hızına bağlı; 2 oyunun yönergesi birbirinin aynı |
| memoryPairs | hafiza | 4 | Uzay zemini; "Başla" yazısı kartların üstüne biniyor; can 6 (standart 3) |
| dragMatch | kopru | 3 | Parça ve hedef aynı emojiyle işaretli; trafik levhası görseli yok, yazıyla veriliyor |
| sentenceBuild | matbaa | 2 | Büyük harfli kart ve nokta kartı dizilişi ele veriyor |
| dragSlider | tren | 2 | Kişisel alan ve israf tren-tünel oyununa indirgenmiş; sayaç "0/4 tren" |
| numPad | radarkod | 1 | Aranacak numara alt başlıkta yazılı; 4 turun dördünde de aynı cevap |
| tallyChart | cetele | 1 | Cevap cümlesi sütun adını birebir içeriyor; çetele yerine rakam |
| surveyChart | cetele (anket) | 1 | Oy sütun adıyla aynı; sonuç yorumu adımı yok |
| codeGrid | kargo | 1 | Yön kazanımı ekran yönleriyle çözdürülüyor; güneş yok, yön adı yok |
| holdFill | kronometre | 1 | Musluk yerine kronometre; gereken miktar üç yerde söyleniyor |

## Doğrulanmış öncelikli hatalar

| # | Hata | Kanıt | Etkilenen |
|---|---|---|---|
| 1 | Yön kazanımı ile mekanik kopuk | h27: bloklar yukarı/sol/sağ/aşağı, güneş ekranda yok, görev metni "yukarı ve sağa ilerle" diyor | h27 |
| 2 | Cevap ekranda yazılı | h10 alt başlık "112'yi tuşla"; h29 görev metni + "Hedef 1 bardak" + ölçek çizgisi; h02 kart etiketleri | h02, h05, h09, h10, h18, h26, h29 |
| 3 | Emoji/renk eşleşmesi | h09: okul geçidi levhası ile "Burada çocuklar geçer" aynı emoji; yeşil ışık ile "Geçebilirsin" aynı renk | h09, h21, h31, h26 |
| 4 | Tanıma kazanımında görsel yok | h09: kazanım levhayı tanımayı istiyor, ekranda "DUR levhası" yazısı var | h09, h19, h20, h32 |
| 5 | Koruyucu kazanım tren oyununa inmiş | h08: kişisel alan, tren-tünel + soyut sözcükler; iki figür arası mesafe yok | h08, h30 |
| 6 | Kart kenarda kırpılıyor | h26: "Çiçeklerin açması" ifadesinden yalnız "...ması" görünüyor | 6 bant oyunu |
| 7 | Ortak şablon yönerge | h17 ve h20: "Radarı sürükleyerek doğru cevabı yakala" — konu geçmiyor | h17, h20 |

Otuz altı oyunun tamamı yüklendi; motorlarda çökme veya konsol hatası oluşmadı.

## Oyun listesi

| ID | Oyun | Ana sorun | Durum |
|---|---|---|---|
| h01 | Arkadaşlık Bandı | Bant kırpılması; okul bahçesi sahnesi yok | ✔ uygulandı |
| h02 | Güçlü Yönler Panosu | Kartlarda kategori etiketi yazılı; özdeğerlendirme yok | ✔ uygulandı |
| h03 | Etkin Dinleme Radarı | Sınıf ortamı yok; karar hıza bağlı | ✔ uygulandı |
| h04 | Duygu Cümlesi Makinesi | Duygu ifadesi hazır kart dizmeye inmiş | ✔ uygulandı |
| h05 | Sınıf Oylaması | Oy sütun adıyla aynı; sonuç yorumu yok | ✔ uygulandı |
| h06 | Karar Adımları | Roket-YAKIT sahnesi | ✔ uygulandı |
| h07 | Alışkanlık Bandı | Gün akışı görselleşmiyor; bant kırpılması | ✔ uygulandı |
| h08 | Kişisel Alan Ölçeri | Koruyucu kazanım tren-tünel oyununa indirgenmiş | ✔ uygulandı |
| h09 | Trafik İşareti Köprüsü | Gerçek levha görseli yok; emoji eşleşmesi cevabı veriyor | ✔ uygulandı |
| h10 | Acil Çağrı Telefonu | "112'yi tuşla" alt başlıkta yazılı; 4 tur aynı cevap | ✔ uygulandı |
| h11 | Acil Çağrı Adımları | Roket sahnesi; gerçek çağrı ekranı yok | ✔ uygulandı |
| h12 | Afet Çantası Atölyesi | Servis tezgâhı; çanta doluluğu görünmüyor | ✔ uygulandı |
| h13 | Nezaket Kartları | Uzay zemini; durum sahnesi yok | ✔ uygulandı |
| h14 | Görgü Kuralları Bandı | Toplumsal ortam görselleşmiyor | ✔ uygulandı |
| h15 | Aile Cümlesi Makinesi | Aile sahnesi yok; kart dizme | ✔ uygulandı |
| h16 | Görev Panosu | Etiket kopyası; gerçek sorumluluk üstlenme yok | ✔ uygulandı |
| h17 | Aile Radarı | Ortak "doğru cevabı yakala" yönergesi | ✔ uygulandı |
| h18 | Görev Çetelesi | Cevap sütun adını içeriyor; çetele yerine rakam | ✔ uygulandı |
| h19 | Gezi Rehberi | Mekân fotoğrafı yok; etiket kopyası | ✔ uygulandı |
| h20 | Çevre Radarı | Ortak "doğru cevabı yakala" yönergesi | ✔ uygulandı |
| h21 | Yönetim Köprüsü | Emoji eşleşmesi; bina görseli yok | ✔ uygulandı |
| h22 | Atatürk'ün Okul Yılları | Roket sahnesi; tarihler sırayı ele veriyor | ✔ uygulandı |
| h23 | Bayram Kartları | Uzay zemini; bayram sahnesi yok | ✔ uygulandı |
| h24 | Bayram Ayırma Bandı | Görsel kanıt yok; bant kırpılması | ✔ uygulandı |
| h25 | Mevsim Kartları | Mevsim manzarası yok | ✔ uygulandı |
| h26 | Hava Olayı Bandı | Kart tamamen kırpıldı; kutu emojileri cevabı veriyor | ✔ uygulandı |
| h27 | Doğadan Yön Bulma | Kazanım-mekanik kopuk: güneş yok, yön adı yok | ✔ uygulandı |
| h28 | Afet Hazırlık Adımları | Roket sahnesi; ev sahnesi yok | ✔ uygulandı |
| h29 | Tasarruf Musluğu | Kronometre var musluk yok; miktar 3 yerde söyleniyor | ✔ uygulandı |
| h30 | İsraf Ölçeri | Tren-tünel; israf görseli yok | ✔ uygulandı |
| h31 | Bilim İnsanı Köprüsü | Emoji eşleşmesi; katkının sonucu görünmüyor | ✔ uygulandı |
| h32 | Teknoloji Zaman Şeridi | Roket sahnesi; ürün görselleri yok | ✔ uygulandı |
| h33 | Eski-Yeni Bandı | Müze vitrini yok; bant kırpılması | ✔ uygulandı |
| h34 | Sanat Kartları | Günlük yaşam sahnesi yok | ✔ uygulandı |
| h35 | Sanat Atölyesi | Etiket kopyası; üretim görünmüyor | ✔ uygulandı |
| h36 | Buluş Radarı | Öncesi-sonrası karşılaştırması yok | ✔ uygulandı |

"✔ uygulandı" = düzeltme yeni motora aktarıldı, tarayıcıda oynanarak doğrulandı.

## Uygulama sırası önerisi

Bulguların çoğu motor düzeyinde. Sırasıyla:
1. Bant kartı kırpılması (6 oyun) — aynı kusur 4. sınıf Türkçe'de de var, tek düzeltme iki dersi birden çözer
2. Parça-hedef emoji eşleşmesi (3 köprü + 1 bant) — Türkçe derslerindeki köprü oyunlarıyla ortak
3. Cevabı sızdıran başlık/görev metni/kart etiketi (7 oyun) — içerik düzeltmesi, motor değişikliği gerektirmez
4. Tren-tünel ve kronometre motorlarının konuya uygun sahnelerle değiştirilmesi (3 oyun)
5. h27'nin yön adlarıyla ve güneşle yeniden kurulması (tek oyun ama kazanım şu an hiç ölçülmüyor)

## Uygulama (26 Ağustos 2026)

Otuz altı oyunun tamamı `web/phaser/hayatbilgisi2-pdf-phaser.html` içindeki yeni
sahne motoruna taşındı. Kaldırılan ortak şablonlar: bant (beltSort), radar-kapsül
(catchDrop), servis tezgâhı (serveOrder), roket-yakıt (orderSequence),
tren-tünel (dragSlider), hafıza kartı (memoryPairs), kronometre (holdFill),
rakam sayacı (tallyChart/surveyChart) ve ekran oklu ızgara (codeGrid).

Yerlerine konan mekanikler: `sinifla`, `karar` (+ gerekçe basamağı), `sira`,
`esle`, `mesafe`, `tus`, `canta`, `cetele`, `yon`, `musluk`, `tahmin`, `yaz`,
`konus`. Tanıma gerektiren kazanımlarda gerçek çizim kullanıldı: trafik levhaları
(sekizgen DUR, kırmızı yuvarlak girilmez, mavi kare yaya geçidi, kırmızı üçgen
okul geçidi), mekânlar, yönetim binaları, mevsim manzaraları, teknoloji ürünleri
ve sanat sahneleri.

### Doğrulanmış öncelikli hataların karşılığı

| # | Hata | Nasıl giderildi |
|---|---|---|
| 1 | Yön kazanımı ile mekanik kopuk (h27) | Bloklar KUZEY/GÜNEY/DOĞU/BATI oldu; hangi ekran kenarının hangi yön olduğu yalnız güneşin konumundan çıkarılıyor. Sabah turunda doğu sağda, akşam turunda batı yukarıda; aynı ekran yönü iki turda farklı yön adına karşılık geliyor |
| 2 | Cevap ekranda yazılı (h02, h05, h09, h10, h18, h26, h29) | Kart kategori etiketleri, "112'yi tuşla" alt başlığı, "Hedef 1 bardak" satırı ve ölçek çizgisi kaldırıldı; oy ve çetele cümleleri artık sütun adını içermiyor |
| 3 | Emoji/renk eşleşmesi (h09, h21, h31, h26) | Parça ve hedeflerde emoji kalmadı; karar levhanın biçim-rengine, binanın işlevine, katkının içeriğine dayanıyor |
| 4 | Tanıma kazanımında görsel yok (h09, h19, h20, h32) | Gerçek levha, mekân ve ürün çizimleri eklendi |
| 5 | Koruyucu kazanım tren oyununa inmiş (h08, h30) | h08'de iki figür arasındaki boşluk gerçekten ayarlanıyor ve ekranda canlanıyor; h30'da akan musluk ve dolan kova görünüyor |
| 6 | Kart kenarda kırpılıyor (6 bant oyunu) | Bant kaldırıldı; kart sabit, sarmalanıyor. 320x568 ve 390x844'te kırpılma yok |
| 7 | Ortak şablon yönerge (h17, h20) | Genel "doğru cevabı yakala" yönergesi kaldırıldı, her oyun kendi konusunu anlatıyor. Katalogdaki "Radar"/"Bant" adları da hizalandı |

### Doğrulama

- `tools/dom_kosum.html#ids=h01,...,h36` — 36 oyun, 108 tur, **36/36 geçiyor**
- `tools/hb2_denetim.html` — 108 turun her birinde kırpılma, dokunma alanı (>=44 px,
  elementFromPoint ile isabet), etiket emojisi ve cevap sızıntısı taraması
- Tarayıcıda gerçek etkileşim: yanlış cevap, üst üste yanlışla can bitmesi, hızlı
  art arda tıklama, boş/kısa/çok uzun yazı girişi, örnek cümleyi kopyalama,
  yanlış yön programı, taşan musluk; 390x844, 320x568 ve 1280x800 görünümleri;
  uygulama içinde oyun açma, bitirme, ← ile çıkma ve sayfa yenileme

### Denetimde kalan iki bulgu (incelendi, tasarım gereği)

- **h19 tur 2** ve **h21 tur 2**: doğru seçeneğin metni sahnede de görünüyor
  ("A · Kale", "Belediye"). Bu iki turda öğrenciye adı verilmiş iki seçenek
  karşılaştırılıyor; ölçülen şey adın kendisi değil, hangisinin tarihî mekân
  olduğu ve hangi birimin o hizmeti yürüttüğü. Ad gizlenirse soru sorulamaz.
