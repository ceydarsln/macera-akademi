# 4. Sınıf Sosyal Bilgiler PDF Düzeltme Takibi

Kaynak: `output/pdf/4_sinif_sosyal_bilgiler_oyunlari_detayli_duzeltmeler.pdf` (46 sayfa, sb01–sb36).
Motor: `web/phaser/sosyal4-pdf-phaser.html` → `web/phaser/sosyal4-pdf.html` → `app/src/main/assets/phaser/sosyal4-pdf.html`.
Katalog bağlantısı: `PHASER_OYUNLAR` içinde sb01–sb36 → `'sosyal4-pdf'`.

**Durum: 36 / 36 tamamlandı.**

Bir oyun ancak şu altı koşul birlikte sağlanınca "tamamlandı" sayıldı:

1. Karar için gereken bütün veri ekranda okunur biçimde bulunur (fiyat, hedef değer, grafik, renk).
2. Ölçülen kavram mekaniğin içindedir — grafik kazanımında grafik, renk kazanımında rengin kendisi bulunur.
3. 390×844 telefon ekranında hiçbir kart kırpılmaz, yazı kesilmez, öge başka ögeyi örtmez.
4. Parça ile hedefi eşleyen emoji/renk ipucu yoktur; ipucu metni doğru seçeneğin adını söylemez.
5. Üç kademeli tur bulunur ve son turda öğrenci kendi örneğini/gerekçesini üretir.
6. Ortak şablon yönergeler ("doğru cevabı yakala") oyuna özel yeniden yazılmıştır.

## Ortak motorlardan çıkış

PDF'nin ana bulgusu 36 oyunun 12 genel şablona sıkışmış olmasıydı: bant, köprü, roket-yakıt,
pizza-tepsi, radar-kapsül, matbaa, hafıza, çetele, kargo, grafik, radarkod, tren-tünel.
Yeni motorda bunların hiçbiri yok. Her oyun konusuna ait bir sahnede geçiyor
(mahalle, okul, harita, ev, meclis, market, mesajlaşma ekranı) ve turlar
sahneye özel bileşenlerle kuruluyor.

Bu ders için motora eklenen yeni bileşenler:

| Bileşen | Ne yapar | Kullanan |
|---|---|---|
| `harita` | Renk anahtarı ve renkli bölgeler; karar **renk adından değil rengin kendisinden** verilir | sb08 |
| `anket` | Çetele; **çocuğun kendi cevabı sayıma katılır**, cevap sütun adıyla aynı olmaz | sb06, sb22 |
| `tepsi` (bütçeli) | Kart üstünde fiyat, üstte **bütçe / sepet / kalan** şeridi — kartların arkasında kalmaz | sb12, sb15, sb28 |
| `graph` | Hedef değerleri grafikten okunan sütun kurma | sb25 |

## Doğrulanmış öncelikli hataların durumu

| # | Hata | Etkilenen | Durum |
|---|---|---|---|
| 1 | Karar verisi ekranda yok — oyun oynanamaz | sb25, sb28 | ✅ hedef değerler grafikte, fiyatlar kart üstünde |
| 2 | Grafik kazanımında grafik yok, işlem hazır | sb26 | ✅ gerçek sütun grafiği, hazır işlem kaldırıldı |
| 3 | Renk kazanımında renk gösterilmiyor + kırpılıyor | sb08 | ✅ renkli harita bölgeleri + renk anahtarı |
| 4 | Parça yazıları kesiliyor | 6 köprü oyunu | ✅ eşleme bileşeni yazıyı sarmalıyor |
| 5 | Sepet/toplam göstergesi örtülüyor | sb28 | ✅ bütçe şeridi kartların önünde |
| 6 | Ortak şablon yönerge | sb04, sb17, sb32 | ✅ her tur kendi sorusunu soruyor |

## Doğrulama

| Denetim | Araç | Sonuç |
|---|---|---|
| Her turun gerçekten bitirilebilmesi | `tools/dom_kosum.html` (ENGINE11 / tur11), 36 oyun × 3 tur | ✅ 36/36, kalan yok, hata yok |
| Yazma turu ölçütleri kendi örnek cevabıyla tutarlı mı; her karakter ekran klavyesinde yazılabiliyor mu | `__SOSYAL4_TEST__.olcutDenetimi()` | ✅ boş liste |
| 390×844 taşma, ekran dışı öge, 24px altı dokunma hedefi, yönergenin doğru cevabı sızdırması | `tmp/sb_denetim.html` | ✅ sorun yok |
| Katalogdan açılış, çift seslendirme, mobil taşma | Tarayıcıda `openGame('sb01')`, 375×812 | ✅ iframe doğru motora gidiyor, yatay taşma yok |

Katalog bağlanırken `text = ''` koşuluna `'sosyal4-pdf'` dalı eklendi: motor kendi tur yönergesini
okuduğu için kataloğun eski tek-tur metni artık üstüne binmiyor.

### Sesli öz değerlendirme sınırı

`konus` akışı öğrencinin örneği dinleyip cevabını **sesli söylemesini** ve ölçütlerle kendini
değerlendirmesini sağlar. Mikrofon kaydı veya konuşma tanıma yapmaz (`MediaRecorder` /
`SpeechRecognition` kullanılmaz); arayüz de kayıt ya da tanıma sonucu olduğunu iddia etmez.

## Oyun listesi

| ID | Oyun | Turlar | Yapılan | Durum |
|---|---|---|---|---|
| sb01 | Birlik Bandı | bant → bant → yazma | Mahalle sahnesi; davranış kartı tam okunur, kırpılma yok · 3. tur: kendi örneğini yazar | ✅ |
| sb02 | Kendini Tanıma Panosu | bant → seçim → yazma | Kart etiketi taşmıyor; 2. tur özdeğerlendirme sorusu · 3. tur: kendini bir cümleyle tanıtır | ✅ |
| sb03 | Saygı Köprüsü | eşleme → bant → yazma | Okul sahnesi; emoji artık kategoriyi ele vermiyor · 3. tur: saygı cümlesi üretir | ✅ |
| sb04 | Sosyal Bilgiler Radarı | seçim → seçim → yazma | Ortak “yakala” yönergesi gitti; her tur kendi sorusunu sorar · 3. tur: gerekçe yazar | ✅ |
| sb05 | Saygı Cümlesi Makinesi | cümle kurma → seçim → yazma | Kart dizilişi büyük harf/nokta ipucu vermiyor · 3. tur: serbest saygı cümlesi | ✅ |
| sb06 | Sınıf İlgi Anketi | çetele → seçim → yazma | Çetele; **çocuğun kendi cevabı sayıma katılıyor**, cevap sütun adıyla aynı değil · 3. tur: sonuç yorumu | ✅ |
| sb07 | Harita Anahtarı Köprüsü | eşleme → eşleme → yazma | Renk anahtarlı gerçek harita; emoji eşleşmesi kaldırıldı · 3. tur: anahtarı açıklar | ✅ |
| sb08 | Harita Rengi Bandı | harita → harita → yazma | **Rengin kendisi ekranda**; karar renk adından değil renkten veriliyor · 3. tur: renk-yer yorumu | ✅ |
| sb09 | Harita Navigasyonu | yön → yön → yazma | Yön adları düğmede yazılı, kuzey oku eklendi · 3. tur: rota tarif eder | ✅ |
| sb10 | Doğa-İnsan Kartları | eşleme → bant → yazma | Coğrafya sahnesi; uzay zemini kaldırıldı · 3. tur: doğa-insan etkisi yazar | ✅ |
| sb11 | Afet Önlem Adımları | sıralama → sıralama → yazma | Ev sahnesi; roket-yakıt sahnesi kaldırıldı, adımlar sırayla dizilir · 3. tur: kendi önlemi | ✅ |
| sb12 | Aile Afet Planı | sepet → seçim → yazma | “Ürün oluştur” gerçekten üretim: plan öğelerini seçip toplar · **kişisel veri istenmez** · 3. tur: plan cümlesi | ✅ |
| sb13 | Oyuncak Zaman Şeridi | sıralama → seçim → yazma | Zaman şeridi; kanıt kavramı turda işleniyor · 3. tur: kanıt gerekçesi | ✅ |
| sb14 | Değişen-Değişmeyen Bandı | bant → bant → yazma | Karşılaştırma sahnesi; kart kırpılması giderildi · 3. tur: değişen/değişmeyen örneği | ✅ |
| sb15 | Aile Tarihi Atölyesi | sepet → bant → yazma | Soy ağacı ekranda oluşuyor · **ad soyad yazdırılmaz** · 3. tur: aile hikâyesi cümlesi | ✅ |
| sb16 | Ortak Miras Kartları | eşleme → bant → yazma | Miras görseli; uzay zemini kaldırıldı · 3. tur: miras örneği yazar | ✅ |
| sb17 | Miras Radarı | seçim → seçim → yazma | Ortak yönerge gitti; her tur kendi sorusu · 3. tur: gerekçe yazar | ✅ |
| sb18 | Kaynak Köprüsü | eşleme → seçim → yazma | Gerçek kaynak görselleri; emoji eşleşmesi kaldırıldı · 3. tur: kaynak seçimi gerekçesi | ✅ |
| sb19 | Cumhuriyet Zaman Şeridi | sıralama → seçim → yazma | Zaman şeridi; tarihler artık sırayı ele vermiyor · 3. tur: dönem yorumu | ✅ |
| sb20 | Cumhuriyet Köprüsü | eşleme → çoklu seçim → yazma | Öncesi-sonrası yan yana gösteriliyor; çoklu seçim · 3. tur: değişim cümlesi | ✅ |
| sb21 | Öncesi-Sonrası Bandı | bant → bant → yazma | Dönem sahnesi; bant kırpılması giderildi · 3. tur: karşılaştırma cümlesi | ✅ |
| sb22 | Sınıf Başkanı Seçimi | çetele → seçim → yazma | **Gizli oy** akışı; oy aday adıyla aynı değil · 3. tur: sonuç yorumu | ✅ |
| sb23 | Demokrasi Cümlesi | cümle kurma → seçim → yazma | Meclis sahnesi; kart dizilişi ipucu vermiyor · 3. tur: demokrasi cümlesi | ✅ |
| sb24 | Millî Mücadele Kartları | eşleme → bant → yazma | Dönem görseli; uzay zemini kaldırıldı · 3. tur: kendi cümlesi | ✅ |
| sb25 | Su Tüketim Grafiği | grafik kurma → seçim → yazma | **Hedef değerler grafikte okunur** (banyo 6 · mutfak 4 · çamaşır 5 · bahçe 2) · 3. tur: tasarruf önerisi | ✅ |
| sb26 | Grafik Dedektifi | seçim → seçim → yazma | **Gerçek sütun grafiği** eklendi, hazır işlem kaldırıldı; 2. tur iki yılı karşılaştırır · 3. tur: grafik yorumu | ✅ |
| sb27 | İstek-İhtiyaç Bandı | bant → bant → yazma | Market rafı sahnesi; bant kırpılması giderildi · 3. tur: istek/ihtiyaç örneği | ✅ |
| sb28 | Bilinçli Alışveriş | sepet → sepet → yazma | **Ürün fiyatları kart üstünde**, bütçe/sepet/kalan şeridi kartların önünde · 3. tur: seçim gerekçesi | ✅ |
| sb29 | Ürünün Yolculuğu | sıralama → sıralama → yazma | Üretim zinciri görselleşti; roket sahnesi kaldırıldı · 3. tur: zincir cümlesi | ✅ |
| sb30 | Ekonomi Köprüsü | eşleme → sıralama → yazma | Parça yazıları tam okunuyor (son sözcük kesilmiyor) · 3. tur: ekonomi cümlesi | ✅ |
| sb31 | Dijital Güvenlik Bandı | bant → bant → yazma | Gerçek arayüz sahnesi; bant kırpılması giderildi · 3. tur: kendi kuralı | ✅ |
| sb32 | Paylaşım Radarı | bant → bant → yazma | Ortak yönerge gitti; her tur paylaşım kararını gerekçelendirir · 3. tur: gerekçe yazar | ✅ |
| sb33 | Bilim İnsanı Köprüsü | eşleme → seçim → yazma | Merak-keşif bağı turda gösteriliyor; emoji eşleşmesi kaldırıldı · 3. tur: merak cümlesi | ✅ |
| sb34 | Siber Zorbalık Adımları | sıralama → bant → yazma | Mesajlaşma ekranı; roket sahnesi kaldırıldı · 3. tur: kendi tepkisi | ✅ |
| sb35 | Ekran Süresi Ölçeri | seçim → seçim → yazma | Saat çizelgesi eklendi; tren-tünel sahnesi kaldırıldı · 3. tur: ekran süresi kuralı | ✅ |
| sb36 | Güvenlik Cümlesi | cümle kurma → cümle kurma → yazma | Gerekçe alanı var (“çünkü” zorunlu) · 3. tur: iki cümlelik güvenlik kuralı | ✅ |

## Sonraki ders

Kalan: 4. sınıf fen bilimleri (f01–f48, kısmen bağlı) ve 3. sınıf fen bilimleri (48).
Motor numarası çakışmaması için yeni ders **ENGINE12 / tur12** ile başlamalı;
`tools/dom_kosum.html` içinde `grep -n "const ENGINE[0-9]"` ile önce boş numara doğrulanmalı.
