# 3. Sınıf Hayat Bilgisi PDF Düzeltme Takibi

Kaynak: `3_sinif_hayat_bilgisi_oyunlari_detayli_duzeltmeler.pdf` (46 sayfa, h37–h72).

Bu dosyada "tamamlandı" işareti yalnız şu altı koşul birlikte sağlanınca verilir:

1. Kavramsal model doğrudur — özellikle hak/sorumluluk ilişkisi bire bir takas olarak kurulmaz.
2. Ölçülen kavram mekaniğin içindedir (kroki oyununda kroki ögeleri ve konum ifadeleri, tasarruf oyununda akan su).
3. Cevap ekranın hiçbir yerinde yazılı değildir — blok sayısı, hedef miktar, veri sayıları dâhil.
4. Parça ile hedefi eşleyen emoji/renk ipucu yoktur.
5. 390×844 telefon ekranında hiçbir kart kırpılmaz, yazı taşmaz; dokunma alanları en az 44 px.
6. Üç kademeli tur bulunur ve son turda öğrenci kendi örneğini söyler, yazar ya da uygular.

## Motor dağılımı (test edilen 13 şablon)

| Motor | Şablon | Oyun | Öne çıkan sorun |
|---|---|---|---|
| beltSort | bant | 6 | Kart sol kenarda tamamen kırpılıyor; 3 kutulu turda etiket taşıyor; kutu emojileri cevabı veriyor |
| dragMatch | kopru | 6 | Parça ve hedef aynı emojiyi paylaşıyor; 6'lı turda uzun yazılar çipe sığmıyor |
| serveOrder | pizza | 5 | İstek metni ile kart etiketi aynı sözcükleri kullanıyor; üretim kazanımı kart seçmeye iniyor |
| orderSequence | roket | 5 | Deprem anı ve Cumhuriyet tarihi gibi konularda roket-YAKIT sahnesi |
| catchDrop | radar | 3 | Güvenlik ve kişilik gibi düşünme konuları refleks oyununa bağlanmış |
| memoryPairs | hafiza | 3 | Uzay zemini; "Başla" yazısı kartların üstüne biniyor; can 6 (standart 3) |
| sentenceBuild | matbaa | 2 | Büyük harfli kart ve nokta kartı dizilişi ele veriyor |
| jumpPath | sirik | 1 | Öğrencinin kendi gelişim alanı tanımlı değil; karar bağlamsız |
| tiltBalance | terazi | 1 | **Kavramsal olarak yanlış model**: hak = sorumluluk sayısal denkliği |
| surveyChart | cetele (anket) | 1 | Oy sütun adıyla aynı; sonuç yorumu adımı yok |
| codeGrid | kargo | 1 | Kroki kazanımı labirent ızgarasına inmiş; konum ifadesi yok |
| holdFill | kronometre | 1 | Musluk yerine kronometre; gereken miktar üç yerde söyleniyor |
| graphBuild | grafik | 1 | En oturmuş motor, ama veriler hazır yazılı; toplam sayaç ipucu veriyor |

## Doğrulanmış öncelikli hatalar

| # | Hata | Kanıt | Etkilenen |
|---|---|---|---|
| 1 | Hak-sorumluluk bire bir denklik olarak modellenmiş | h40: sol kefede "3 hak = 3", sağda "0 / 3" sayacı; blok sayısı ekranda yazılı | h40 |
| 2 | Kroki kazanımı labirent ızgarasına inmiş | h62: sokak/yön oku/ölçek yok, bloklar yukarı-sol-sağ, görev metni rotayı söylüyor | h62 |
| 3 | Emoji eşleşmesi bilgiyi devre dışı bırakıyor | h50: 6 eşleşmenin 6'sı da emojiyle çözülebiliyor (itfaiyeci↔ateş, çiftçi↔başak) | 6 köprü oyunu |
| 4 | Kart kenarda kırpılıyor | h63: "Görevlilere haber vermek" ifadesinden yalnız "...ber" görünüyor | 6 bant oyunu |
| 5 | Veri/miktar hazır veriliyor | h66: "Kâğıt: 6 · Plastik: 4 · Metal: 3" yazılı + "0/13 blok"; h65: miktar 3 yerde | h65, h66 |
| 6 | Hayati konularda sahne ciddiyeti bozuk | h64 deprem anı roket-YAKIT sahnesinde; h63 kutu etiketleri taşıyor | h63, h64 |

h37–h72 arasındaki 36 oyunun tamamı yüklendi; motorlarda çökme veya konsol hatası oluşmadı.

## Sınıflar arası ortak kusurlar

Bu derste bulunan üç kusur başka derslerde de rapor edilmişti — tek motor düzeltmesi hepsini çözer:

- **codeGrid kazanım kopukluğu**: 2. sınıf h27 (Doğadan Yön Bulma) ile aynı — ikisinde de yön/konum kavramı ekran yönlerine indirgenmiş.
- **Köprü emoji sızıntısı**: 2. sınıf hayat bilgisi (h09, h21, h31), 4. sınıf Türkçe (z11, z27, z36, z46, z60) ve 3. sınıf Türkçe köprü oyunlarıyla ortak.
- **Bant kartı kırpılması**: 2. sınıf hayat bilgisi (h26), 4. sınıf Türkçe (z41, z50) ile ortak.

## Oyun listesi

| ID | Oyun | Ana sorun | Durum |
|---|---|---|---|
| h37 | Gelişim Basamakları | Öğrencinin kendi hedefi tanımlı değil; karar bağlamsız | PDF'de |
| h38 | Plan Masası | Takvim/süre görünmüyor; servis tezgâhı | PDF'de |
| h39 | Okul Hakları Bandı | Bant kırpılması; okul ortamı yok | PDF'de |
| h40 | Hak-Sorumluluk Terazisi | Kavramsal yanlış model; blok sayısı ekranda | PDF'de |
| h41 | Çocuk Hakları Köprüsü | Emoji eşleşmesi; hak görselleri yok | PDF'de |
| h42 | Proje Oylaması | Oy seçenek adıyla aynı; sonuç yorumu yok | PDF'de |
| h43 | Sağlık Denetim Bandı | Gün akışı görselleşmiyor; bant kırpılması | PDF'de |
| h44 | Güvenlik Radarı | Güvenlik kararı hız oyununa bağlanmış | PDF'de |
| h45 | Güvenlik Adımları | Roket sahnesi; senaryo sahnesi yok | PDF'de |
| h46 | Trafik Kuralı Köprüsü | Emoji eşleşmesi; kuralın sonucu gösterilmiyor | PDF'de |
| h47 | Acil Çağrı Cümlesi | Kart dizme; görevli geri bildirimi yok | PDF'de |
| h48 | Trafik Afişi Atölyesi | "Özgün ürün" kazanımı kart seçmeye inmiş | PDF'de |
| h49 | Aile-Toplum Bandı | Ölçek farkı görselleşmiyor; bant kırpılması | PDF'de |
| h50 | Meslek Köprüsü | 6 eşleşmenin 6'sı emojiyle çözülebiliyor; yazı taşması | PDF'de |
| h51 | Meslek Atölyesi | Etiket kopyası; araç kullanımı görünmüyor | PDF'de |
| h52 | Yardımlaşma Kartları | Erişilebilirlik sahnesi yok | PDF'de |
| h53 | Proje Adımları | Roket sahnesi; süreç görselleşmiyor | PDF'de |
| h54 | Yardımlaşma Cümlesi | İzin isteyen ifade ayrımı yok; kart dizme | PDF'de |
| h55 | Koruma Bandı | Mekân fotoğrafı yok; bant kırpılması | PDF'de |
| h56 | Yönetim Köprüsü | Emoji eşleşmesi; bina görseli yok | PDF'de |
| h57 | Atatürk Kartları | Uzay zemini; özellik-başarı bağı gösterilmiyor | PDF'de |
| h58 | Kişilik Radarı | Kapsül-radar; yakın anlamlı çeldirici yok | PDF'de |
| h59 | Birlik Panosu | Etiket kopyası; pano sahnesi yok | PDF'de |
| h60 | Cumhuriyet Yolu | Roket sahnesi; tarihler sırayı ele veriyor | PDF'de |
| h61 | Doğa Köprüsü | Emoji eşleşmesi; fayda sahnesi yok | PDF'de |
| h62 | Kroki Rehberi | Kroki değil labirent; konum ifadesi yok | PDF'de |
| h63 | Afet Zaman Bandı | Kart tamamen kırpıldı; etiket taşması; kutu emojileri | PDF'de |
| h64 | Deprem Anı Adımları | Hayati konu roket-YAKIT sahnesinde | PDF'de |
| h65 | Sürdürülebilirlik Musluğu | Kronometre var musluk yok; miktar 3 yerde | PDF'de |
| h66 | Geri Dönüşüm Grafiği | Veriler hazır yazılı; toplam sayaç ipucu veriyor | PDF'de |
| h67 | Bilimsel Gelişme Köprüsü | Emoji eşleşmesi; öncesi-sonrası yok | PDF'de |
| h68 | Teknoloji Denge Bandı | Durum sahnesi yok; bant kırpılması | PDF'de |
| h69 | İletişim Zaman Şeridi | Roket sahnesi; ürün görselleri yok | PDF'de |
| h70 | Sanatçı Kartları | Eser örneği yok; uzay zemini | PDF'de |
| h71 | Sanat Sergisi | Etiket kopyası; sergi kurulmuyor | PDF'de |
| h72 | Etki Radarı | Öncesi-sonrası karşılaştırması yok | PDF'de |

"PDF'de" = düzeltme şartnamesi yazıldı, uygulamaya henüz aktarılmadı.

## Uygulama sırası önerisi

1. **h40'ın kavramsal modeli** — tek oyun ama yanlış bir hak anlayışı öğretiyor, en öncelikli
2. Köprü emoji sızıntısı (6 oyun + diğer derslerdeki köprüler)
3. Bant kartı kırpılması (6 oyun + diğer derslerdeki bantlar)
4. h62 ve 2. sınıf h27'nin birlikte düzeltilmesi (codeGrid motoru)
5. h63/h64 afet oyunlarının sahne ciddiyeti
6. h65/h66'da veri ve miktarın öğrenciye bırakılması
