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
| h01 | Arkadaşlık Bandı | Bant kırpılması; okul bahçesi sahnesi yok | PDF'de |
| h02 | Güçlü Yönler Panosu | Kartlarda kategori etiketi yazılı; özdeğerlendirme yok | PDF'de |
| h03 | Etkin Dinleme Radarı | Sınıf ortamı yok; karar hıza bağlı | PDF'de |
| h04 | Duygu Cümlesi Makinesi | Duygu ifadesi hazır kart dizmeye inmiş | PDF'de |
| h05 | Sınıf Oylaması | Oy sütun adıyla aynı; sonuç yorumu yok | PDF'de |
| h06 | Karar Adımları | Roket-YAKIT sahnesi | PDF'de |
| h07 | Alışkanlık Bandı | Gün akışı görselleşmiyor; bant kırpılması | PDF'de |
| h08 | Kişisel Alan Ölçeri | Koruyucu kazanım tren-tünel oyununa indirgenmiş | PDF'de |
| h09 | Trafik İşareti Köprüsü | Gerçek levha görseli yok; emoji eşleşmesi cevabı veriyor | PDF'de |
| h10 | Acil Çağrı Telefonu | "112'yi tuşla" alt başlıkta yazılı; 4 tur aynı cevap | PDF'de |
| h11 | Acil Çağrı Adımları | Roket sahnesi; gerçek çağrı ekranı yok | PDF'de |
| h12 | Afet Çantası Atölyesi | Servis tezgâhı; çanta doluluğu görünmüyor | PDF'de |
| h13 | Nezaket Kartları | Uzay zemini; durum sahnesi yok | PDF'de |
| h14 | Görgü Kuralları Bandı | Toplumsal ortam görselleşmiyor | PDF'de |
| h15 | Aile Cümlesi Makinesi | Aile sahnesi yok; kart dizme | PDF'de |
| h16 | Görev Panosu | Etiket kopyası; gerçek sorumluluk üstlenme yok | PDF'de |
| h17 | Aile Radarı | Ortak "doğru cevabı yakala" yönergesi | PDF'de |
| h18 | Görev Çetelesi | Cevap sütun adını içeriyor; çetele yerine rakam | PDF'de |
| h19 | Gezi Rehberi | Mekân fotoğrafı yok; etiket kopyası | PDF'de |
| h20 | Çevre Radarı | Ortak "doğru cevabı yakala" yönergesi | PDF'de |
| h21 | Yönetim Köprüsü | Emoji eşleşmesi; bina görseli yok | PDF'de |
| h22 | Atatürk'ün Okul Yılları | Roket sahnesi; tarihler sırayı ele veriyor | PDF'de |
| h23 | Bayram Kartları | Uzay zemini; bayram sahnesi yok | PDF'de |
| h24 | Bayram Ayırma Bandı | Görsel kanıt yok; bant kırpılması | PDF'de |
| h25 | Mevsim Kartları | Mevsim manzarası yok | PDF'de |
| h26 | Hava Olayı Bandı | Kart tamamen kırpıldı; kutu emojileri cevabı veriyor | PDF'de |
| h27 | Doğadan Yön Bulma | Kazanım-mekanik kopuk: güneş yok, yön adı yok | PDF'de |
| h28 | Afet Hazırlık Adımları | Roket sahnesi; ev sahnesi yok | PDF'de |
| h29 | Tasarruf Musluğu | Kronometre var musluk yok; miktar 3 yerde söyleniyor | PDF'de |
| h30 | İsraf Ölçeri | Tren-tünel; israf görseli yok | PDF'de |
| h31 | Bilim İnsanı Köprüsü | Emoji eşleşmesi; katkının sonucu görünmüyor | PDF'de |
| h32 | Teknoloji Zaman Şeridi | Roket sahnesi; ürün görselleri yok | PDF'de |
| h33 | Eski-Yeni Bandı | Müze vitrini yok; bant kırpılması | PDF'de |
| h34 | Sanat Kartları | Günlük yaşam sahnesi yok | PDF'de |
| h35 | Sanat Atölyesi | Etiket kopyası; üretim görünmüyor | PDF'de |
| h36 | Buluş Radarı | Öncesi-sonrası karşılaştırması yok | PDF'de |

"PDF'de" = düzeltme şartnamesi yazıldı, uygulamaya henüz aktarılmadı.

## Uygulama sırası önerisi

Bulguların çoğu motor düzeyinde. Sırasıyla:
1. Bant kartı kırpılması (6 oyun) — aynı kusur 4. sınıf Türkçe'de de var, tek düzeltme iki dersi birden çözer
2. Parça-hedef emoji eşleşmesi (3 köprü + 1 bant) — Türkçe derslerindeki köprü oyunlarıyla ortak
3. Cevabı sızdıran başlık/görev metni/kart etiketi (7 oyun) — içerik düzeltmesi, motor değişikliği gerektirmez
4. Tren-tünel ve kronometre motorlarının konuya uygun sahnelerle değiştirilmesi (3 oyun)
5. h27'nin yön adlarıyla ve güneşle yeniden kurulması (tek oyun ama kazanım şu an hiç ölçülmüyor)
