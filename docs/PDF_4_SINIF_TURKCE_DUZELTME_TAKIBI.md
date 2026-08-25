# 4. Sınıf Türkçe PDF Düzeltme Takibi

Kaynak: `4_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf` (76 sayfa, z01–z64).

Bu dosyada "tamamlandı" işareti yalnız şu beş koşul birlikte sağlanınca verilir:

1. Başlıktaki sahne ve karakter, ölçülen Türkçe becerisinin gerçek parçasıdır.
2. Ekranda cevabı sızdıran hiçbir öge yoktur — parça/hedef simge eşleşmesi, kuralı ve işaret yerini söyleyen görev metni, yazılı dikte sözcüğü, tarih sırası, sütun adını tekrarlayan yanıt.
3. Üç farklı tur, değişen içerik ve değişen doğru konumuyla baştan sona oynanır.
4. Yanlış cevap doğruyu söylemeden, içerik üzerinde nedenini gösterir; motor/refleks hatası can kaybettirmez.
5. 390×844 telefon ekranında karar verilecek cümle tam görünür, hiçbir metin kırpılmaz/taşmaz ve dokunma alanları en az 44 px'tir.

## Motor dağılımı (test edilen 15 şablon)

| Motor | Şablon | Oyun sayısı | Öne çıkan sorun |
|---|---|---|---|
| beltSort | bant | 8 | Cümle kartı sol kenarda tamamen kırpılıyor (de/da turunda karar imkânsız); üç kutulu turlarda etiket kutu dışına taşıyor |
| serveOrder | pizza | 8 | Balondaki aday cümleler tepsi kartlarıyla aynı simgeyle etiketli; metin okunmadan çözülüyor |
| punctFix | tamirhane | 8 | Görev metni kuralı ve işaretin yerini söylüyor; "Kalan" sayacı hamle sayısını veriyor; başlık kırpılıyor |
| sentenceBuild | matbaa | 8 | Büyük harfli kart ve nokta kartı dizilişi ele veriyor |
| catchDrop | radar | 6 | Karar süresi düşme hızına bağlı; kapsül/çanak dili |
| orderSequence | roket | 5 | Roket-YAKIT sahnesi başlıkla çelişiyor; tarihler sırayı sayıyla çözdürüyor |
| dragMatch | kopru | 5 | Parça ve hedef aynı simgeyle işaretli — cevap doğrudan veriliyor; 6'lı turda cümleler çipten taşıyor |
| memoryPairs | hafiza | 4 | Sahne uzay; "Başla" yazısı kartların üstüne biniyor; can 6 (standart 3) |
| wordHighlight | dedektif | 4 | Soru başlığı kırpılıyor, metin taşıyor, büyüteç karar verilecek sözcüğü örtüyor |
| jumpPath | sirik | 2 | Bağlam cümlesi ekranda yok; basamak yazıları düşük kontrast |
| codeGrid | kargo | 2 | "Yönerge yazar" kazanımında yalnız yön oku diziliyor |
| typeWord | daktilo | 1 | Dikte edilen sözcük balonda yazılı görünüyor |
| dragSlider | tren | 1 | Su tüketimi sorulurken tren-tünel sahnesi; sayaç "0/3 tren"; dayanak metni yok |
| tallyChart | cetele | 1 | Cevap cümlesi sütun adını birebir içeriyor; çetele yerine rakam sayacı |
| surveyChart | cetele (anket) | 1 | Oy ("Ela") sütun adıyla aynı; "ÇETELE TABLOSU" başlığı seçim oyununa uymuyor; sonuç yorumu adımı yok |

## Kazanım dağılımı

38 yazma (T.Y.), 10 konuşma (T.K.), 9 dinleme (T.D.), 7 okuma (T.O.) hedefli oyun.
Yazma ve konuşma hedeflerinin hiçbirinde şu an gerçek üretim (serbest yazı alanı, ses kaydı) yok.

## 4. sınıfa özgü kazanımlar

Bu sınıfta ilk kez gelen yazım/noktalama hedefleri ayrı dikkat ister:
`de/da` ayrı-birleşik (z41), `ki` ayrı-birleşik (z42, z50), kesme işareti (z12),
üç nokta ve konuşma çizgisi (z20), arasöz virgülü ve kısa çizgi (z35),
yay ayraç ve eğik çizgi (z45), sesteş sözcükler (z10, z11), terim anlam (z26, z46),
bağlaçlar (z33, z34), kaynak gösterme (z32) ve kaynak güvenilirliği (z29).
Bu oyunların hepsinde karar verilecek cümlenin tam görünmesi kritik — şu an bant ve
dedektif motorlarındaki kırpılma bu kazanımları ölçülemez hâle getiriyor.

## Oyun listesi

| ID | Oyun | Gerçek eylem kabul ölçütü | Durum |
|---|---|---|---|
| z01 | Katılıyorum Bandı | Görüş panoda sabit; karar gerekçe ve öneriyle tamamlanır. | PDF'de |
| z02 | Yayınevi Masası | Kartlarda aday cümleler; balon simge kopyası kaldırılır. | PDF'de |
| z03 | Noktalama Atölyesi | Görev metni işaret adını söylemez; öğrenci cümleleri yazar. | PDF'de |
| z04 | Kurallı Cümle Makinesi | Kartlar küçük harfle; devrik-kurallı karşılaştırması yapılır. | PDF'de |
| z05 | Erdem Sözlüğü | Gerçek sözlük sayfası; madde başı, tanım ve örnek birlikte. | PDF'de |
| z06 | Sözcük Anlamı Radarı | Seçenekler sabit; bağlam ipucu karar öncesi işaretlenir. | PDF'de |
| z07 | Yazım Hatası Avcısı | Metin taşmaz, büyüteç örtmez; kalem otomatik düzeltmez. | PDF'de |
| z08 | Hikâye Basamakları | Metin görünür; tahmin metin kanıtıyla gerekçelendirilir. | PDF'de |
| z09 | Zaman Şeridi | Roket kaldırılır; tarihler ilk turda gizli. | PDF'de |
| z10 | Sözcük Tasnif Bandı | Çift sabit kartta, örnek cümleyle; bant akışı kaldırılır. | PDF'de |
| z11 | Sesteş Köprüsü | Parça-hedef simge eşleşmesi KALDIRILIR; cümleler çipe sığar. | PDF'de |
| z12 | Kesme İşareti Tamirhanesi | Kesmenin ayırdığı ek renkli; kesme istemeyen çeldiriciler var. | PDF'de |
| z13 | Doğru Bilgi Radarı | Kartlar sabit; her kartta "kaynağı gör" düğmesi. | PDF'de |
| z14 | Mektup Masası | Gerçek mektup kâğıdı; öğrenci mektubu yazar, imzasını ekler. | PDF'de |
| z15 | Zıt Anlam Makinesi | Zıt çift iki kefeli sahnede karşı karşıya gelir. | PDF'de |
| z16 | Kahramanlık Diktesi | Hedef sözcük balonda YAZILMAZ; harf havuzu karışıktır. | PDF'de |
| z17 | Kaynak Ayırma Bandı | Gerçek enerji görselleri; tartışmalı örnekler ölçütle savunulur. | PDF'de |
| z18 | Afet Robotu | Oklar yazılı yönerge kartına dönüşür; öğrenci yönergeyi yazar. | PDF'de |
| z19 | Eş Anlam Ormanı | Ağaç kovukları; çift aynı cümlede iki kez okunarak doğrulanır. | PDF'de |
| z20 | Üç Nokta ve Konuşma Çizgisi | Görev metni işaretin yerini söylemez; başlık kırpılmaz. | PDF'de |
| z21 | Su Döngüsü | Gerçek döngü şeması; adımlar şemadaki yerine yerleşir. | PDF'de |
| z22 | Yarım Metin Atölyesi | Önceki bölüm panelde; devamı öğrenci tarafından yazılır. | PDF'de |
| z23 | Tasarruf Ölçer | Tren kaldırılır; tahmin ekrandaki bilgi metnine dayanır. | PDF'de |
| z24 | Doğa Dergisi Masası | Bölümler taslak sayfaya oturur; öğrenci kendi planını yazar. | PDF'de |
| z25 | Kütüphane Görevlisi | Amaç açıklayıcı cümle; tür kapaktan çıkarımla bulunur. | PDF'de |
| z26 | Anlam Tasnif Bandı | Cümle sabit; üç kutu etiketi kutu içinde kalır. | PDF'de |
| z27 | Atasözü Köprüsü | Simge eşleşmesi kaldırılır; anlam canlandırmayla gösterilir. | PDF'de |
| z28 | Yazışma Masası | Gerçek e-posta ekranı; öğrenci e-postayı yazar. | PDF'de |
| z29 | Kaynak Denetim Radarı | Kartlarda yazar, tarih, kurum görünür; ölçütle karşılaştırılır. | PDF'de |
| z30 | Okur Kimliği Anketi | Cevap tür adını söylemez; çetele çizgisi, beşinci dördü keser. | PDF'de |
| z31 | Dilek Kutusu | Tür seçimi ayrı adım; öğrenci önerisini yazar. | PDF'de |
| z32 | Araştırma Adımları | Adımlar panoda; kaynak gösterme kurala uygun yapılır. | PDF'de |
| z33 | Bağlaç Ayırma Bandı | Cümle sabit, boşluk vurgulu; kutu etiketleri sığar. | PDF'de |
| z34 | Bağlaç Makinesi | Bağlaç işlevi animasyonla gösterilir; öğrenci iki yönde yazar. | PDF'de |
| z35 | Arasöz Atölyesi | Gerçek broşür; arasöz virgülü sıralama virgülünden ayrılır. | PDF'de |
| z36 | Neden-Sonuç Köprüsü | Simge eşleşmesi kaldırılır; zincirleme ilişki kurulur. | PDF'de |
| z37 | Eş Anlam Sahnesi | Gerçek tiyatro sahnesi; çift aynı replikte doğrulanır. | PDF'de |
| z38 | Sözcük Anlamı Radarı | Seçenekler sabit; mecaz-gerçek karşılaştırması yapılır. | PDF'de |
| z39 | Sunum Masası | Gerçek kürsü ve dinleyici; öğrenci sunum yapıp kaydeder. | PDF'de |
| z40 | Yazım Denetçisi | Metin taşmaz; ayrı-birleşik kuralları karışık verilir. | PDF'de |
| z41 | "de/da" Denetim Bandı | Cümle kartı tam görünür; "dahi/bile" testi uygulanır. | PDF'de |
| z42 | "ki" Düzeltme Kalemi | Başlık tam, metin taşmaz, büyüteç hedefi örtmez. | PDF'de |
| z43 | Kodlama Laboratuvarı | Program numaralı cümleler hâlinde okunur. | PDF'de |
| z44 | Mucit Atölyesi | İstek amaç-araç-adım planı; simge kopyası kaldırılır. | PDF'de |
| z45 | Deney Raporu Dizgisi | Görev metni işaretin yerini SÖYLEMEZ; sayaç kapanır. | PDF'de |
| z46 | Terim Köprüsü | Simge eşleşmesi kaldırılır; günlük-terim anlam ayrılır. | PDF'de |
| z47 | Yönerge Makinesi | Cümle deney animasyonunu tetikler; ayrıntı farkı gösterilir. | PDF'de |
| z48 | Araştırma Adımları | Soru-hipotez-deney-gözlem-sonuç panoda görselleşir. | PDF'de |
| z49 | Müze Rehberi | Somut/somut olmayan miras ayrımı; simge kopyası kaldırılır. | PDF'de |
| z50 | "ki" Denetim Bandı | Cümle tam görünür; bağlaç ve ilgi eki karşılaştırılır. | PDF'de |
| z51 | Miras Panosu Dizgisi | Gerçek pano; kesme ve büyük harf birlikte istenir. | PDF'de |
| z52 | Miras Haritası | Türkiye haritası sahne; miras şehrine yerleşir. | PDF'de |
| z53 | Miras Zinciri | Usta-çırak atölye sahnesi; roket kaldırılır. | PDF'de |
| z54 | Eş Anlam Makinesi | Çift aynı cümlede yer değiştirerek anlamı korur. | PDF'de |
| z55 | Türkçe Koruma Kalemi | Metin taşmaz; karşılığı öğrenci seçer ve cümleyi yazar. | PDF'de |
| z56 | Miras Bekçisi Radarı | Yakalama kaldırılır; niyet-etki ayrımı yapılır. | PDF'de |
| z57 | Demokrasi Bandı | Adalet meydanı; hak-özgürlük farkı tartışılır. | PDF'de |
| z58 | Dilekçe Masası | Gerçek dilekçe şablonu; öğrenci doldurur. | PDF'de |
| z59 | Bildiri Dizgisi | İşaretin anlamı değiştirmesi örnekle gösterilip seslendirilir. | PDF'de |
| z60 | Denge Köprüsü | Simge eşleşmesi kaldırılır; kalaslar köprüyü dengede tutar. | PDF'de |
| z61 | Söz Hakkı Makinesi | Cümle mikrofonda okunur; gerekçeli-gerekçesiz görüş ayrılır. | PDF'de |
| z62 | Gizlilik Kalkanı | Yakalama kaldırılır; izin kavramı işlenir. | PDF'de |
| z63 | Sınıf Seçimi | Oy sütun adını tekrarlamaz; çetele görünür; sonuç yorumlanır. | PDF'de |
| z64 | Karar Basamakları | Gerçek meclis süreci; bağlam ekranda sürekli durur. | PDF'de |

"PDF'de" = düzeltme şartnamesi yazıldı, uygulamaya henüz aktarılmadı.
