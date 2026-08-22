# Katalog istekleri (Phaser şablonlarını bağlayan oturumdan)

Bu dosya `macera-akademi-firebase-11.html` üzerinde çalışan oturum içindir.
Şablon tarafı hazır ve **her oyun baştan sona oynanarak** test edildi;
aşağıdaki satırlar uygulanmadan oyunlar eski DOM oynatıcısında kalıyor.

## PHASER_TIPLER'e eklenecek satırlar

```js
const PHASER_TIPLER = {
  /* ... mevcut satırlar ... */

  numberTrace:    'rakam',        /* 10 oyun · s0–s9 */
  numberWrite:    'rakam',        /* 10 oyun · s10, n1–n9 */
  tallyChart:     'cetele',       /*  6 oyun · v37, w42, y30, z30, p52, h18 */
  surveyChart:    'cetele',       /*  9 oyun · m59, m60, w46, z63, p55, h05, h42, sb06, sb22 */
  holdFill:       'kronometre',   /*  9 oyun · w14, w30, w31, p30, p34, h29, h65, f21, g40 */
  mirrorGrid:     'simetri',      /*  5 oyun · w35, w36, w40, p43, p44 */
  foldMirror:     'simetri',      /*  3 oyun · v32, w34, p41 */
  tiltBalance:    'terazi',       /*  5 oyun · w23, w45, p24, p54, h40 */
  balanceScale:   'terazi',       /*  2 oyun · m24, m44 */
  patternFill:    'oruntu',       /*  6 oyun · m29, m30, m31, m33, v03, v05 */
  countToTarget:  'oruntu',       /*  4 oyun · m11, m12, m22, m28 */
  groupMultiply:  'paketleme',    /*  3 oyun · v18, w20, p21 */
  shareDivide:    'paketleme',    /*  2 oyun · v19, w05 */
  typeWord:       'daktilo',      /*  5 oyun · t09, y14, y56, y60, z16 */
};
```

## Durum

| mekanik | şablon | oyun | test |
|---|---|---|---|
| numberTrace | rakam | 10 | ✅ hepsi bitirildi, completeGame çağrıldı |
| numberWrite | rakam | 10 | ✅ hepsi bitirildi (pick ve timeMs turları dahil) |
| tallyChart | cetele | 6 | ✅ hepsi bitirildi |
| surveyChart | cetele | 9 | ✅ hepsi bitirildi (karar aşaması dahil) |
| holdFill | kronometre | 9 | ✅ 25 turun hepsi tutturuldu |
| mirrorGrid | simetri | 5 | ✅ hepsi bitirildi (dikey ve çift eksen) |
| foldMirror | simetri | 3 | ✅ hepsi bitirildi (katlama animasyonu dahil) |
| tiltBalance | terazi | 5 | ✅ 15 turun hepsi dengelendi |
| balanceScale | terazi | 2 | ✅ hepsi bitirildi (karşılaştırma sorusu dahil) |
| patternFill | oruntu | 6 | ✅ hepsi bitirildi (ortadaki boşluk dahil) |
| countToTarget | oruntu | 4 | ✅ hepsi bitirildi (kule ve geriye sayma dahil) |
| groupMultiply | paketleme | 3 | ✅ hepsi bitirildi (bölmeyle sağlama dahil) |
| shareDivide | paketleme | 2 | ✅ hepsi bitirildi |
| typeWord | daktilo | 5 | ✅ 25 sözcüğün hepsi yazıldı (Â, Ğ, İ dahil) |

## Notlar

- `renderStageWrapped()` içindeki
  `if(g.type === 'numberTrace' || g.type === 'numberWrite' || ...)` satırı DOM
  oynatıcısına ait; `phaserOyunuMu()` ondan önce çalıştığı için değiştirilmesi
  gerekmiyor.
- **numberWrite** turlarında katalog nokta dizisi vermiyor (yalnız `target` +
  `slots`). Şablon basamak izlerini üst pencerenin `digitStrokes()`
  fonksiyonundan okuyor; erişemezse kendi kopyasını kullanıyor. `DIGIT_TPL`
  değişirse şablonun yerel kopyası da güncellenmeli
  (`rakam-phaser.html` → `RAKAM_TPL`).
- **surveyChart** oyunlarında katalogda `successMsg` yok; şablon
  "Veriyi topladın, çeteleyi okudun ve doğru kararı verdin 📋" metnini
  kullanıyor. İstenirse katalogda `successMsg` alanı açılabilir.
- **surveyChart** cevapları yalnız seçenek kimliği (`responses:['cik','cil']`).
  Şablon her oyu doğru sütuna işletiyor (tallyChart ile aynı mekanik), sonda
  karar sorusunu soruyor. DOM sürümü oyları kendisi sayıyordu.

- **foldMirror**'daki `cfg.half` bir SVG PARÇASI (sarmalayıcı `<svg>` yok) ve
  içinde kübik eğri (`C`) var. Ortak çizici `svgciz.js` yol komutlarından
  C/Q'yu desteklemiyor — kalp/kelebek yarımları köşeli çıkıyordu. Bu yüzden
  `simetri-phaser.html` kendi küçük C destekli çizicisini taşıyor
  (`svgYol` / `svgParcaCiz`). `svgciz.js`'e C desteği eklenirse şablondaki
  yerel çizici kaldırılabilir.
- **mirrorGrid**'de beklenen kareler uygulamadaki `mgTargets()` kuralıyla
  birebir aynı hesaplanıyor (dikey / yatay / çift eksen, eksen üstündeki kare
  kendisi, zaten verilen kareler istenmez). Kural değişirse şablondaki
  `aynaHedefleri()` de güncellenmeli.

- **tiltBalance/balanceScale**: turun iki modu veriden çıkarılıyor —
  tek başına sol değere eşit blok VARSA "eşit olanı seç", yoksa (ya da
  `rightStart` / `repeat` varsa) "blokları biriktirerek eşitle". Biriktirme
  turunda çocuk çıkmaza girebiliyordu (22 hedefe 12+9=21 koyup 1 eksik
  kalmak); şablona **"↺ Kefeyi boşalt"** düğmesi eklendi — eksik bırakmak
  hata sayılmadığı için can götürmüyor.
- **balanceScale**'de `cfg.compare.options` düz metin dizisi ve doğru cevap
  ayrı alanda (`correct`); şablon eşleştirmeyi metin karşılaştırarak yapıyor.
  Diğer mekaniklerdeki `{label, correct}` biçimine geçirilirse daha sağlam
  olur.

## Şablon–mekanik eşlemesinde düzeltme

Görevde `paketleme-phaser.html` countToTarget'e, `kronometre-phaser.html`
"süre tahmini"ne atanmıştı. Şablonların İÇİNDEKİ mekanikler farklı çıktı;
eşleme şablonun gerçekten uyguladığı mekaniğe göre yapıldı:

| şablon | görevdeki varsayım | şablonun gerçekte uyguladığı |
|---|---|---|
| oruntu | patternFill | patternFill **+ countToTarget** |
| paketleme | countToTarget | **groupMultiply + shareDivide** |
| kronometre | timeEstimate (katalogda yok) | **holdFill** |
| terazi | balanceScale | balanceScale **+ tiltBalance** |
| simetri | symmetryDraw (katalogda yok) | **mirrorGrid + foldMirror** |
| cetele | surveyChart, tallyChart | aynı ✔ |

## Şablonu olmayan mekanikler (bilgi)

Aşağıdaki tipin bu 11 şablon içinde karşılığı yok:

    placeValueLoad  2 oyun

---
## UYGULANDI (uygulama oturumu)

- `PHASER_TIPLER` satırları eklendi: numberTrace/numberWrite→rakam,
  tallyChart/surveyChart→cetele, holdFill→kronometre. (44 oyun DOM'dan çıktı.)
- surveyChart için `successMsg` alanı: şablonun kendi metni yeterli görüldü,
  katalogda alan açılmadı. İhtiyaç sürerse tekrar yaz.

---
## UYGULANDI — 2. parti (uygulama oturumu, 22 Ağustos)

- Zip'teki 11 şablon ~/Downloads'a ve assets/phaser'a kopyalandı.
- PHASER_TIPLER'e eklendi: mirrorGrid/foldMirror→simetri,
  tiltBalance/balanceScale→terazi, patternFill/countToTarget→oruntu,
  groupMultiply/shareDivide→paketleme, typeWord→daktilo. (+35 oyun)
- kesirsaat eşlemesi BİLEREK eklenmedi (test edilmedi notuna istinaden).
  Test edilince "fractionCut/clockSet → kesirsaat" satırını buraya yaz.
