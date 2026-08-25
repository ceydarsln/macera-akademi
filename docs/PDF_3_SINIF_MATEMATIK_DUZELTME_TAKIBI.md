# 3. Sınıf Matematik PDF Düzeltme Takibi

Kaynak: `output/pdf/3_sinif_matematik_oyunlari_detayli_duzeltmeler.pdf` (58 sayfa, w01–w48).
Şartnamenin yapılandırılmış hâli: `tmp/spec3.json` (PDF üretici betiğinden çıkarıldı).
Motor: `web/phaser/matematik3-pdf-phaser.html` (matematik2 çerçevesi + 3. sınıf yardımcıları).

"Uygulamada" işareti yalnız şu koşullar birlikte sağlanınca verilir:

1. Üç tur farklı veriyle baştan sona oynanır (`tools/dom_kosum.html` ile doğrulanır).
2. Sahne cevabı ele vermez: hazır model, sayı ya da etiket kopyalanamaz.
3. Çocuk gerçek bir karar verir (hangi modül, hangi tünel, hangi adım).
4. Yanlışta doğruyu söylemeyen, nedeni gösteren geri bildirim gelir.
5. 375×812 telefon ekranında hedef alanı ve seçenekler ilk ekranda görünür.

| ID | Oyun | Kazanım | Uygulanan ana düzeltme | Durum |
|---|---|---|---|---|
| w01 | Mega Uzay Çekirdeği | 1000'e kadar sayı temsilleri | Hareketli kapsül yakalama kaldırıldı; çocuk fazlalıklı havuzdan yüzlük/onluk/birlik seçerek sayıyı kuruyor, sonra dört gösterimi eşliyor. Sahnede hazır model yok. | Uygulamada |
| w02 | Altın Kubbe | Esnek sayı çözümleme | Sayaç bulmacası yerine tek tek taş yerleştirme; aynı sayı üç farklı çözümlemeyle (3y+4o+8b, 2y+16o, 506'da boş onluk) kuruluyor. | Uygulamada |
| w03 | Hızlı Tren Sinyalleri | Onluğa/yüzlüğe yuvarlama | Uzaklıklar sayı doğrusunda gerçek değerlerle yazılıyor; gerekçe ekranda kalıyor, sürgü cevabı önceden vermiyor. | Uygulamada |
| w04 | Sihirli Fasulye Sırığı | Ritmik sayma | Rota çizgisi cevabı söylüyordu; dal artık yalnız doğru seçimden sonra büyüyor. Çeldiriciler ±2 komşuluğunda. İleri 8'er, geri 8'er, 100'er turları. | Uygulamada |

## Motor tarafında eklenenler

- `renderSequence`: ritmik sayma (aynı seçenek listesinden sırayla doğru değerler).
- `toplamKanca(hedef)` + `hedefToplam` alanı: fazlalıklı modül havuzu; hedefe
  ulaşınca tur biter, aşınca can götürmeyen uyarı gelir.
- `renderDrag` sırası hedef→havuz olarak değişti (telefonda hedef ilk ekranda).
- `.hundred-flat`, `.core`, `.dome`, `.rail-line`, `.beanstalk` sahne stilleri.
