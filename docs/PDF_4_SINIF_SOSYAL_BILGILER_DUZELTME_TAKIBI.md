# 4. Sınıf Sosyal Bilgiler PDF Düzeltme Takibi

Kaynak: `4_sinif_sosyal_bilgiler_oyunlari_detayli_duzeltmeler.pdf` (46 sayfa, sb01–sb36).

Bu dosyada "tamamlandı" işareti yalnız şu altı koşul birlikte sağlanınca verilir:

1. Karar için gereken bütün veri ekranda okunur biçimde bulunur (fiyat, hedef değer, grafik).
2. Ölçülen kavram mekaniğin içindedir — grafik kazanımında grafik, renk kazanımında renk bulunur.
3. 390×844 telefon ekranında hiçbir kart kırpılmaz, yazı kesilmez, öge başka ögeyi örtmez.
4. Parça ile hedefi eşleyen emoji/renk ipucu yoktur.
5. Üç kademeli tur bulunur ve son turda öğrenci kendi örneğini/gerekçesini üretir.
6. Ortak şablon yönergeler ("doğru cevabı yakala") oyuna özel yeniden yazılmıştır.

## Motor dağılımı (test edilen 12 şablon)

| Motor | Şablon | Oyun | Öne çıkan sorun |
|---|---|---|---|
| beltSort | bant | 6 | Kart sol kenarda kırpılıyor; renk oyununda kayıp bölüm tam da renk adı; kutu etiketi taşıyor |
| dragMatch | kopru | 6 | Parça yazılarının son sözcüğü çipe sığmıyor; emoji kategoriyi ele veriyor |
| orderSequence | roket | 5 | Cumhuriyet tarihi, ekmeğin yolculuğu, siber zorbalık gibi konularda roket-YAKIT sahnesi |
| serveOrder | pizza | 4 | Bilinçli Alışveriş'te ürün fiyatları yok; sepet toplamı kartların arkasında |
| catchDrop | radar | 3 | Üç oyunun yönergesi aynı: "Radarı sürükleyerek doğru cevabı yakala" |
| sentenceBuild | matbaa | 3 | Büyük harfli kart ve nokta kartı dizilişi ele veriyor |
| memoryPairs | hafiza | 3 | Uzay zemini; "Başla" yazısı kartların üstüne biniyor; can 6 (standart 3) |
| surveyChart | cetele (anket) | 2 | Cevap sütun adıyla aynı; sonuç yorumu adımı yok |
| codeGrid | kargo | 1 | **Diğer sınıflardan daha iyi** — görev metni yön adlarını kullanıyor; ama düğmeler hâlâ ok |
| graphBuild | grafik | 1 | Hedef değerler ekranda yok; oyun deneme-yanılmayla çözülüyor |
| numPad | radarkod | 1 | "Grafik Dedektifi"nde grafik yok; işlem hazır yazılı |
| dragSlider | tren | 1 | Ekran süresi kararı tren-tünel oyununa bağlanmış |

## Doğrulanmış öncelikli hatalar

| # | Hata | Kanıt | Etkilenen |
|---|---|---|---|
| 1 | Karar verisi ekranda yok — oyun oynanamaz | sb25: hedefler kodda var (banyo 6, mutfak 4, çamaşır 5, bahçe 2) ekranda yok; sb28: ürün fiyatları yok | sb25, sb28 |
| 2 | Grafik kazanımında grafik yok, işlem hazır | sb26: başlık "Grafik Dedektifi", ekranda grafik yok, "60 + 40 = ?" yazılı | sb26 |
| 3 | Renk kazanımında renk gösterilmiyor + kırpılıyor | sb08: kart "Koyu yeşil ovalar" yazıyor, sadece "ovalar" görünüyor; renk örneği yok | sb08 |
| 4 | Parça yazıları kesiliyor | sb30: 6 parçanın 5'inde son sözcük okunmuyor | 6 köprü oyunu |
| 5 | Sepet/toplam göstergesi örtülüyor | sb28: "tepsi boş — 0 / 30" ürün kartlarının arkasında | sb28 |
| 6 | Ortak şablon yönerge | sb04, sb17, sb32: "Radarı sürükleyerek doğru cevabı yakala" | 3 radar oyunu |

sb01–sb36 arasındaki 36 oyunun tamamı yüklendi; motorlarda çökme veya konsol hatası oluşmadı.

## Olumlu fark

**Harita Navigasyonu (sb09)** bu dersin olumlu farkı: görev metni "kuzeye ve doğuya ilerle" diyerek
gerçek yön adlarını kullanıyor ve yönerge ekran yönü ile coğrafi yön arasındaki çeviriyi açıklıyor.
2. sınıf Doğadan Yön Bulma (h27) ve 3. sınıf Kroki Rehberi (h62) bu bilgiyi hiç vermiyordu.
codeGrid motoru düzeltilirken bu sürüm başlangıç noktası alınmalı.

## Oyun listesi

| ID | Oyun | Ana sorun | Durum |
|---|---|---|---|
| sb01 | Birlik Bandı | Bant kırpılması; mahalle sahnesi yok | PDF'de |
| sb02 | Kendini Tanıma Panosu | Kart etiketleri; özdeğerlendirme yok | PDF'de |
| sb03 | Saygı Köprüsü | Emoji eşleşmesi; okul sahnesi yok | PDF'de |
| sb04 | Sosyal Bilgiler Radarı | Ortak "doğru cevabı yakala" yönergesi | PDF'de |
| sb05 | Saygı Cümlesi Makinesi | Kart dizme; serbest üretim yok | PDF'de |
| sb06 | Sınıf İlgi Anketi | Cevap sütun adıyla aynı; yorum yok | PDF'de |
| sb07 | Harita Anahtarı Köprüsü | Gerçek harita yok; emoji eşleşmesi | PDF'de |
| sb08 | Harita Rengi Bandı | Renk gösterilmiyor; renk adı kırpılıyor | PDF'de |
| sb09 | Harita Navigasyonu | Yön adları iyi; düğmeler hâlâ ok, kuzey oku yok | PDF'de |
| sb10 | Doğa-İnsan Kartları | Coğrafya görseli yok; uzay zemini | PDF'de |
| sb11 | Afet Önlem Adımları | Roket sahnesi; ev sahnesi yok | PDF'de |
| sb12 | Aile Afet Planı | "Ürün oluştur" kazanımı kart seçmeye inmiş | PDF'de |
| sb13 | Oyuncak Zaman Şeridi | Roket sahnesi; kanıt kavramı işlenmiyor | PDF'de |
| sb14 | Değişen-Değişmeyen Bandı | Karşılaştırma sahnesi yok; bant kırpılması | PDF'de |
| sb15 | Aile Tarihi Atölyesi | Soy ağacı ekranda oluşmuyor | PDF'de |
| sb16 | Ortak Miras Kartları | Miras görseli yok; uzay zemini | PDF'de |
| sb17 | Miras Radarı | Ortak "doğru cevabı yakala" yönergesi | PDF'de |
| sb18 | Kaynak Köprüsü | Gerçek kaynak görseli yok; emoji eşleşmesi | PDF'de |
| sb19 | Cumhuriyet Zaman Şeridi | Roket sahnesi; tarihler sırayı ele veriyor | PDF'de |
| sb20 | Cumhuriyet Köprüsü | Öncesi-sonrası gösterilmiyor; emoji eşleşmesi | PDF'de |
| sb21 | Öncesi-Sonrası Bandı | Dönem fotoğrafı yok; bant kırpılması | PDF'de |
| sb22 | Sınıf Başkanı Seçimi | Oy aday adıyla aynı; gizli oy ve yorum yok | PDF'de |
| sb23 | Demokrasi Cümlesi | Kart dizme; meclis sahnesi yok | PDF'de |
| sb24 | Millî Mücadele Kartları | Dönem görseli yok; uzay zemini | PDF'de |
| sb25 | Su Tüketim Grafiği | **Hedef değerler ekranda yok — oynanamaz** | PDF'de |
| sb26 | Grafik Dedektifi | **Grafik yok; işlem hazır yazılı** | PDF'de |
| sb27 | İstek-İhtiyaç Bandı | Market rafı yok; bant kırpılması | PDF'de |
| sb28 | Bilinçli Alışveriş | **Ürün fiyatları yok — oynanamaz** | PDF'de |
| sb29 | Ürünün Yolculuğu | Roket sahnesi; üretim zinciri görselleşmiyor | PDF'de |
| sb30 | Ekonomi Köprüsü | 6 parçanın 5'inde son sözcük kesiliyor | PDF'de |
| sb31 | Dijital Güvenlik Bandı | Arayüz sahnesi yok; bant kırpılması | PDF'de |
| sb32 | Paylaşım Radarı | Ortak yönerge; gerekçelendirme yok | PDF'de |
| sb33 | Bilim İnsanı Köprüsü | Emoji eşleşmesi; merak-keşif bağı gösterilmiyor | PDF'de |
| sb34 | Siber Zorbalık Adımları | Roket sahnesi; mesajlaşma ekranı yok | PDF'de |
| sb35 | Ekran Süresi Ölçeri | Tren-tünel; saat çizelgesi yok | PDF'de |
| sb36 | Güvenlik Cümlesi | Kart dizme; gerekçe alanı yok | PDF'de |

"PDF'de" = düzeltme şartnamesi yazıldı, uygulamaya henüz aktarılmadı.

## Uygulama sırası önerisi

1. **sb25, sb26, sb28** — üçü de veri eksikliğinden ölçüm yapamıyor, ikisi fiilen oynanamaz durumda
2. sb08'de rengin gösterilmesi (kazanımın tam merkezi)
3. Köprü yazı kırpılması (6 oyun) ve bant kartı kırpılması (6 oyun)
4. Köprü emoji sızıntısı — diğer derslerle ortak
5. Roket sahnesinin 5 sıralama oyunundan kaldırılması
6. codeGrid motoru: sb09 sürümü temel alınarak 2. ve 3. sınıf sürümleri de düzeltilir
