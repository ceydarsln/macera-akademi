# 1. Sınıf Sayma PDF Düzeltme Takibi

Kaynak: `1_sinif_sayma_oyunlari_detayli_duzeltmeler.pdf` (27 sayfa, s0–s10 ve n1–n9, 20 oyun).

Bu dosyada "tamamlandı" işareti yalnız şu altı koşul birlikte sağlanınca verilir:

1. Rakamın biçimi doğru: kavisli rakamlar (0, 2, 3, 5, 6, 8, 9) eğrisel çizilir, hiçbirinde köşe görünmez.
2. Yazım yönü zorunlu tutulmaya devam eder — mevcut sıralı kontrol noktası yapısı korunur.
3. Başlıktaki sahne gerçekten çizilir; bitiş ödülü ekranda görünen bir olaya bağlanır.
4. Yazılacak sayı ekranda yazılı görünmez; yalnız sesli söylenir ve tekrar dinlenebilir.
5. Yoldan sapma can kaybettirmez; ekran sarsıntısı ve kırmızı flaş kaldırılır.
6. Üç kademeli tur (kılavuzlu → soluk kılavuzlu → kılavuzsuz) ve sayı-miktar eşleştirmesi bulunur.

## Motorun doğru çalışan yanı

`rakam-phaser.html` yazım YÖNÜNÜ doğru biçimde zorunlu tutuyor: çizim yalnız BAŞLA noktasından
başlıyor ve kontrol noktalarına sırayla değmek gerekiyor, bu yüzden çocuk rakamı ters yönde
çizemiyor. Bu yapı korunmalı, düzeltmeler sırasında bozulmamalı.

## Doğrulanmış teknik hatalar

| # | Hata | Kanıt | Etkilenen |
|---|---|---|---|
| 1 | Kılavuz ve iz düz çizgiyle (`moveTo`/`lineTo`) çiziliyor, eğri yok | `rakam-phaser.html` `kilavuzuCiz()` ve `iziCiz()`; ekranda 0 sekizgen, 8 zikzak, 6 ve 9 altıgen | 7 rakam: 0, 2, 3, 5, 6, 8, 9 |
| 2 | `cfg.scene` motor tarafından hiç okunmuyor | Motor `cfg.ink`, `cfg.guide`, `cfg.finale` okuyor; `cfg.scene` için tek referans yok | 20 oyunun tamamı |
| 3 | Hedef sayı ekranda büyük yazılı + arkada hayalet şablon | n1, n4, n5 ekran görüntüleri | n1–n9 (9 oyun) |
| 4 | Seçim sorusunun cevabı ekranın 4 yerinde yazılı | n3: "Hangi yumurtada 12 yazıyor?" — 12 dört yerde | n3, n7 |
| 5 | Yoldan sapma (74 px) can kaybettiriyor + sarsıntı + kırmızı flaş | `izKoptu()` → `this.can--`, `cameras.main.shake/flash` | 20 oyunun tamamı |
| 6 | 17 oyun tek turluk | Yalnız n6 (3 tur), n7 ve n9 (2 tur) çok turlu | 17 oyun |
| 7 | Rakam çizme oyunlarında seslendirme tanımı yok | s0–s9 `cfg.speak` boş | 10 oyun |
| 8 | Süre baskısı | n4: 45 saniye geri sayım | n4 |

## Sabitler (referans)

`CAN_SAYISI = 3` · `YAKALA = 36 px` (kontrol noktasına değme) · `SAPMA = 74 px` (iz kopma eşiği)
· `HEDEF = {x0:104, y0:262, en:272, boy:314}` (çizim alanı).

## Oyun listesi

| ID | Oyun | Sahne (tanımlı, çizilmiyor) | Ana sorun | Durum |
|---|---|---|---|---|
| s0 | Uyuyan Ayı | cave | 0 sekizgen çiziliyor; mağara/ayı yok | PDF'de |
| s1 | Roket Fırlatma | space | Biçim doğru (1 düz); sahne ve tur eksik | PDF'de |
| s2 | Kuğu Gölü | lake | 2'nin üst kavisi köşeli | PDF'de |
| s3 | Zıplayan Kurbağa | pond | 3'ün iki kavisi zikzak | PDF'de |
| s4 | Yelkenli Gemi | sea | Biçim doğru (4 düz); sahne ve tur eksik | PDF'de |
| s5 | Elma Kurdu | apple | 5'in göbek kavisi köşeli | PDF'de |
| s6 | Salyangoz Kabuğu | leaf | 6'nın dairesi altıgen | PDF'de |
| s7 | Bumerang Atışı | valley | Biçim doğru (7 düz); sahne ve tur eksik | PDF'de |
| s8 | Sonsuzluk Yarışı | track | 8 tamamen köşeli zikzak | PDF'de |
| s9 | Uçan Balon | clouds | 9'un dairesi altıgen | PDF'de |
| s10 | Büyücü ve Kazanı | wizard | 0 köşeli; onlar-birler nesne temsili yok | PDF'de |
| n1 | Uzay Şifresi | airlock | "14" ekranda yazılı + hayalet şablon | PDF'de |
| n2 | Kayıp Hazine Haritası | map | "17" ekranda yazılı; harita yok | PDF'de |
| n3 | Dinozor Kuluçkası | nest | Soru cevabı 4 yerde yazılı; yumurta yok | PDF'de |
| n4 | Sihirli Daktilo | typewriter | 45 sn süre baskısı; "16" yazılı; daktilo yok | PDF'de |
| n5 | Gökyüzü Fırçası | opensky | Kılavuzsuz oyun ama "19" yazılı duruyor | PDF'de |
| n6 | Robotun Bataryası | robot | Tur yapısı örnek (3 tur); sahne yok | PDF'de |
| n7 | Karışık Vagonlar | wagons | Renk seçimi soyut; vagon görseli yok | PDF'de |
| n8 | Elma Toplama Kampı | orchard | Sayı-miktar bağı kurulmuyor | PDF'de |
| n9 | Buzul Penguenleri | iceberg | 2 tur; sahne yok | PDF'de |

"PDF'de" = düzeltme şartnamesi yazıldı, uygulamaya henüz aktarılmadı.

## Uygulama sırası önerisi

Bulguların çoğu tek tek oyuna değil `rakam-phaser.html` motoruna ait. Sırasıyla:
1. Eğrisel çizim (7 rakamı aynı anda düzeltir)
2. `cfg.scene` okuma ve 20 sahnenin çizimi
3. Sapma cezasının kaldırılması ve seslendirme (20 oyunu birden etkiler)
4. Hedef sayının gizlenmesi ve kademeli hayalet şablon (9 oyun)
5. Üç turlu yapı ve sayı-miktar eşleştirmesi (17 oyun)
