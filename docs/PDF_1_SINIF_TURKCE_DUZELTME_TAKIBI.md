# 1. Sınıf Türkçe PDF Düzeltme Takibi

Kaynak: `output/pdf/1_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf` (t01–t09, 9 oyun).
Şartnamenin yapılandırılmış hâli: `tmp/spec_t.json` (`tmp/pdfs/build_turkish1_detailed_corrections.py`).
Motor: `web/phaser/turkce1-pdf-phaser.html` (turkce2 çerçevesi + sayma motorunun SVG sahne/iz katmanı).

**Durum: 9/9 oyun uygulandı — 1. sınıf Türkçe tamamlandı.**

## Başlangıç durumu

Oyunlar katalogda vardı ama kendi motorları yoktu: `numberTrace`, `tapSelect`, `dragMatch`,
`orderSequence` ve `typeWord` genel motorlarında açılıyorlardı. Şartnamenin ilk maddesi tam da
bunu söylüyor: *"Türkçe hedefi başka motorların içinde kayboluyor. Gökyüzü Çizeri sayacında
'rakam' yazıyor. Hece Treni köprü, Zıp Zıp Kurbağa ve Gizemli Sandık balık/kova, Kelime
Fabrikası köprü motorunda açılıyor. Başlık ve gerçek eylem birçok oyunda uyuşmuyor."*

## Şartnamenin üç tema kuralı ve motordaki karşılığı

| Tema | Şartname | Motor |
|---|---|---|
| Tema 1 · Harf ve ses | "Harf adı ile ses birbirinden ayrılmalı; dinleme görevi yazılı cevabı önceden göstermemelidir. Büyük-küçük harf ve farklı güvenli yazı biçimleri, hız baskısı olmadan ayırt edilmelidir." | `ciz` mekaniği harfi üç kılavuz düzeyinde gerçek işaretçiyle yazdırıyor, ilerleme "harf" diyor; `sepet` ve `konum` mekaniklerinde nesne adları cevaptan önce yazılmıyor, yalnız dinleme düğmesi var; `balon` mekaniğinde süre baskısı yok, harfler iki yazı biçiminde ve iki boyutta geliyor. |
| Tema 2 · Hece | "Sesler harf adlarıyla kopuk okunmamalı; soldan sağa kesintisiz kaynaştırılmalıdır. Açık ve kapalı heceler aynı seslerin ters sırası dahil çoklu örneklerle karşılaştırılmalıdır. Kurbağa, tren ve uzay gemisi sahneleri gerçek oyun eylemini taşımalıdır." | `tren`, `kurbaga` ve `uzay` mekanikleri kendi SVG sahnelerinde çalışıyor; hedef hece yalnız sesli veriliyor, yazı ancak kurulduktan sonra açılıyor; açık/kapalı etiketini çocuk seçiyor; ters sıralı çiftler (NA-AN, ET-TE, AT-TA, EN-NE) ayrı aşamalarda karşılaştırılıyor. |
| Tema 3 · Kelime, anlama, dikte | "Kelime cevabı başlangıçta görünmemeli; hece sentezi anlam resmi veya bağlamla doğrulanmalıdır. Okuduğunu anlama aynı kelimeyi eşleme değil, etiketsiz görsel, cümle ve mini metin sorularına ilerlemelidir. Dikte sırasında hedef kelime bütün görünür alanlardan gizlenmeli ve harf paleti karıştırılmalıdır." | `fabrika` üretim bitene kadar kelimeyi yazmıyor, anlamsız dizide bant duruyor; `sandik` anahtarlarında yazı yok, kelime → cümle → mini metin + anlam sorusu diye ilerliyor; `dikte` hedefi hiçbir yerde yazmıyor, paleti her aşamada karıştırıyor, DİNLE sınırsız ve cezasız, GÖSTER iki denemeden önce açılmıyor. |

## Oyunlar

| # | Ad | Kip | Uygulanan düzeltme | Durum |
|---|---|---|---|---|
| t01 | Gökyüzü Çizeri | yazma | İlerleme etiketi "rakam" değil "harf"; üç kılavuz düzeyi (yoğun nokta → başlangıç-bitiş → çizgisiz); büyük A ve küçük a ayrı yazılıyor; "son hamleyi sil" yalnız son bölümü geri alıyor, motor sapması can götürmüyor; bitişte yazı /a/ sesiyle eşleştiriliyor. | Uygulamada |
| t02 | Sesli Sepet | dinleme | Gerçek pazar/sepet sahnesi; ilk turda kelime yazıları gizli, her nesnenin adı ayrı dinleme dokunuşuyla çalınıyor; baş-orta-son konumu ayrı turda ve her konum iki örnekle; son turda /a/–/e/ iki sepete ayrılıyor. | Uygulamada |
| t03 | Su Altı Baloncukları | okuma | Balık/kova motoru kaldırıldı, gerçek yuvarlak baloncuklar patlıyor; çeldiriciler anlamlı görsel yakınlıktan (N-M, N-H, n-m, n-h); iki yazı biçimi ve iki boyut; süre baskısı yok; yanlışta iki harf yan yana büyütülerek karşılaştırılıyor. | Uygulamada |
| t04 | Hece Treni | okuma | Köprü motoru kaldırıldı, gerçek lokomotif ve iki vagon; hedef hece yalnız sesli, yazı sonda açılıyor; iki açık ve iki kapalı hece, ters sıralı çiftler dâhil; açık/kapalı etiketini çocuk seçiyor. | Uygulamada |
| t05 | Zıp Zıp Kurbağa | okuma | Gölet ve nilüfer sahnesi; hedef ilk turda yazılı değil; yapraklar sabit, süre ilk iki turda ölçülmüyor; AN-NA ve EN-NE çiftleri karşılaştırılıyor; akıcılık süresi yalnız dizi doğru bitince gösteriliyor. | Uygulamada |
| t06 | Mıknatıslı Uzay Gemisi | okuma | Meteorlar sabit; yönerge çözüm sırasını söylemiyor; iki ayrı yuva ve "son meteoru geri gönder" düğmesi; ET-TE, EN-NE, AT-TA ters sıra çiftleri; son aşamada hece kelime görseliyle bağlanıyor. | Uygulamada |
| t07 | Kelime Fabrikası | yazma | Köprü motoru kaldırıldı, gerçek üretim bandı; hedef resim ve sesle veriliyor, kelime yazısı üretim bitince açılıyor; anlamsız dizide bant duruyor; ALET, NANE, ANNE ve üç heceli ELMALAR; son turda kelime anlamlı cümleye yerleştiriliyor. | Uygulamada |
| t08 | Gizemli Sandık | okuma | Gerçek sandık, kilit ve anahtar; anahtarlarda yazı yok, yalnız resim; kelime → kısa cümle → iki cümlelik mini metin; son turda anlam sorusu yanıtlanıyor; dinleme açıkça "erişim desteği" diye işaretli ve cezasız. | Uygulamada |
| t09 | Sihirli Daktilo | yazma | Hedef kelime hiçbir görünür alanda yazılı değil; harf paleti her aşamada karıştırılıyor ve hedef harfleri doğru sırada dizmiyor; DİNLE sınırsız ve cezasız; GÖSTER iki bağımsız denemeden önce kapalı; ipuçları kademeli (hece sayısı → ilk ses → kısa ön izleme); yanlış harf yazılanları silmiyor; NANE, MASA, ANNE, ALET ve "ELMA AL" öbeği. | Uygulamada |

## Kabul ölçütü denetimi (tools/tr1_denetim.html)

`tools/tr2_denetim.html`ten uyarlandı; 9 oyunun 27 turunu 390×844'te tek tek çizip tarıyor:
kırpılma, 44 px dokunma alanı, harf/hece kartlarında emoji ipucu ve kipe özgü cevap sızıntısı
(t01'de "rakam" sözcüğü, işitsel turlarda nesne adı, hece turlarında kurulacak hece,
dikte turunda hedef kelime ve palet sırası). İlk taramada çıkan ve düzeltilen bulgular:

| # | Bulgu | Kapsam | Düzeltme |
|---|---|---|---|
| 1 | Seçenekler veri sırasında çiziliyordu: hece kasaları hep ilk iki kutu, doğru anahtar hep ilk anahtar, doğru resim hep ilk kart. Cevap dizilişten okunabiliyordu. | t01, t06, t07, t08, t09 | `gs()` — oyun kimliği, tur ve aşamadan türeyen tohumlu görünüm sırası. `data-*` gerçek dizini taşıdığı için doğruluk mantığı ve koşum etkilenmiyor. |
| 2 | Karıştırmak tek başına yetmedi: doğru parçalar yan yana ve doğru sırada kalınca cevap yine okunuyordu (ör. `NE EL MA LAR AN`). | t04, t06, t07 | `gsHavuz()` — doğru dizinin bitişik olmadığı bir permütasyon aranıyor. |
| 3 | `dikte` boşluk yuvasında "boşluk" yazısı 44 px'lik kutuya sığmayıp yatayda kırpılıyordu. | t09 tur 3 | Yuvada `␣` simgesi, altında "␣ = boşluk yuvası" açıklaması. |

Düzeltmelerden sonra: **27/27 tur temiz.**

## Canlı tarayıcı testinde bulunan ve düzeltilen kusur

| # | Kusur | Düzeltme |
|---|---|---|
| 4 | `opensky` sahnesinin dekor uçağı ile yazım çizgisindeki uçak aynı anda görünüyordu; çocuk hangisini izleyeceğini bilemez. | `sahneSvg(..., karakterSiz)` — yazma turunda sahnenin kendi karakteri gizleniyor. |

Test kapsamı: 375×812 ve 1280×800. Denenen senaryolar: yanlış yerden çizime başlama (cezasız,
yön hatırlatması), "son hamleyi sil" (bütün harfi silmiyor, can götürmüyor), etiket seçmeden
sepete dokunma (cezasız uyarı), yanlış sepet (ipucu cevabı söylemeden), art arda üç hızlı yanlış
dokunuş (tek can), dikte ipuçlarının kademeli açılması, GÖSTER kilidi ve iki denemeden sonra
açılması, yanlış harfte yazılanların korunması, tur geçişleri ve bitiş ekranı.
Konsolda hata yok, ağ isteklerinin tamamı 200. Koşum: `tools/dom_kosum.html#ids=t01…t09` → 9/9.
