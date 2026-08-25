# 3. Sınıf Türkçe PDF Düzeltme Takibi

Kaynak: `3_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf` (76 sayfa, y01–y64).

Bu dosyada "tamamlandı" işareti yalnız şu beş koşul birlikte sağlanınca verilir:

1. Başlıktaki sahne ve karakter, ölçülen Türkçe becerisinin gerçek parçasıdır.
2. Ekranda cevabı sızdıran hiçbir öge yoktur (yazılı dikte sözcüğü, işaret adı, tarih sırası, simge kopyası, sütun adı).
3. Üç farklı tur, değişen içerik ve değişen doğru konumuyla baştan sona oynanır.
4. Yanlış cevap doğruyu söylemeden, içerik üzerinde nedenini gösterir; motor/refleks hatası can kaybettirmez.
5. 390×844 telefon ekranında hiçbir metin kırpılmaz/taşmaz ve dokunma alanları en az 44 px'tir.

## Motor dağılımı (test edilen 14 şablon)

| Motor | Şablon | Oyun sayısı | Öne çıkan sorun |
|---|---|---|---|
| beltSort | bant | 8 | Bant hızı okuma süresine karışıyor; kart kenarda kırpılıyor |
| punctFix | tamirhane | 8 | Yönerge doğru işaretin adını söylüyor; "Kalan" satırı görev metniyle çakışıyor |
| sentenceBuild | matbaa | 8 | Büyük harfli kart ve nokta kartı dizilişi ele veriyor |
| serveOrder | pizza | 7 | Balon simgesi ile kart simgesi birebir; içerik okunmadan çözülüyor |
| memoryPairs | hafiza | 5 | Sahne uzay; "Başla" yazısı kartların üstüne biniyor; can 6 (standart 3) |
| orderSequence | roket | 5 | Roket-YAKIT sahnesi başlıkla çelişiyor; tarihler sırayı sayıyla çözdürüyor |
| catchDrop | radar | 4 | Karar süresi düşme hızına bağlı; kapsül/çanak dili |
| dragMatch | kopru | 4 | Köprü görseli yok; uzun cümleler parça çipine sığmıyor |
| dragSlider | tren | 3 | Ses oyunlarında tren-tünel sahnesi; hiç gerçek ses dinletilmiyor |
| wordHighlight | dedektif | 3 | Metin panelden taşıyor, soru başlığı kırpılıyor, büyüteç hedefi örtüyor |
| typeWord | daktilo | 3 | Dikte edilen sözcük balonda yazılı görünüyor |
| codeGrid | kargo | 3 | "Yönerge yazar" kazanımında yalnız yön oku diziliyor |
| jumpPath | sirik | 2 | Bağlam cümlesi ekranda yok; basamak yazıları düşük kontrast |
| tallyChart | cetele | 1 | Cevap cümlesi sütun adını birebir içeriyor; çetele yerine rakam sayacı |

## Kazanım dağılımı

36 yazma (T.Y.), 9 dinleme (T.D.), 8 konuşma (T.K.), 11 okuma (T.O.) hedefli oyun.
Yazma ve konuşma hedeflerinin hiçbirinde şu an gerçek üretim (serbest yazı alanı, ses kaydı) yok.

## Oyun listesi

| ID | Oyun | Gerçek eylem kabul ölçütü | Durum |
|---|---|---|---|
| y01 | Dinleme Stüdyosu | Davranışlar canlandırma sahnesi olarak sabit gelir; öğrenci düzeltmeyi kendi cümlesiyle söyler. | PDF'de |
| y02 | Erdem Kâşifi | Kâşif çadırı sahnesi; eşleşme davranıştaki kanıt sözcükle doğrulanır; can 3'e eşitlenir. | PDF'de |
| y03 | Hikâye Kâhini | Küre sabit; başlık+kapak kanıtıyla tahmin yapılır, metinle doğrulanır. | PDF'de |
| y04 | Yayınevi Masası | Kartlarda etiket değil aday cümleler; balon simge kopyası kaldırılır. | PDF'de |
| y05 | Noktalama Tamirhanesi | Yönerge işaret adını söylemez; öğrenci iki cümleyi klavyeyle yazar. | PDF'de |
| y06 | Ses Düzeyi Ayarı | Tren kaldırılır; her düzeyde gerçek ses dinletilir, öğrenci kaydeder. | PDF'de |
| y07 | Cümle Kurma Makinesi | Kartlar küçük harfle gelir; alternatif kurallı diziliş kabul edilir. | PDF'de |
| y08 | Erdem Kalemi | Metin taşmaz, büyüteç örtmez; ana duygu iki kanıtla ifade edilir. | PDF'de |
| y09 | Zaman Şeridi | Roket kaldırılır; tarihler ilk turda gizli, sıralama içerikten yapılır. | PDF'de |
| y10 | Zıt Anlam Aynası | Ayna sahnesi gerçek; bağlama duyarlı zıt çiftler eklenir. | PDF'de |
| y11 | Kısaltma Atölyesi | Bant durur; kesme işareti ve ek renkli gösterilir, öğrenci eki yazar. | PDF'de |
| y12 | Neden-Sonuç Köprüsü | Gerçek köprü; doğru eşleşme kalas ekler; yazılar çipe sığar. | PDF'de |
| y13 | Özel Ad Tamirhanesi | Özel ad türleri renk kodlu; cins isim çeldiricisi bulunur. | PDF'de |
| y14 | Kahramanlık Diktesi | Hedef sözcük balonda YAZILMAZ; harf havuzu karışıktır. | PDF'de |
| y15 | Doğru Bilgi Radarı | Kartlar sabit; her kartta "kaynağı gör" düğmesi bulunur. | PDF'de |
| y16 | Bayram Mesajı Makinesi | Mesaj panoya asılır; öğrenci kendi mesajını yazar. | PDF'de |
| y17 | Doğa Ayırma Bandı | Varlıklar görselli ve sabit; ham-işlenmiş çeldiricileri bulunur. | PDF'de |
| y18 | Afet Çantası Robotu | Oklar yazılı yönerge kartına dönüşür; program cümle olarak okunur. | PDF'de |
| y19 | Doğa Dergisi Masası | Bölümler taslak sayfadaki yerlerine oturur; öğrenci kendi planını yazar. | PDF'de |
| y20 | Eş Anlam Ormanı | Ağaç kovukları sahnesi; bağlamda değişmeyen eş anlamlılar karşılaştırılır. | PDF'de |
| y21 | Doğa Günlüğü Tamiri | Gerçek defter sayfası; konuşma aktarımı iki nokta+tırnakla çalışılır. | PDF'de |
| y22 | Yağmur Döngüsü | Gerçek su döngüsü şeması; adımlar şemadaki yerine yerleşir. | PDF'de |
| y23 | Mevsim Basamakları | Bağlam cümlesi ekranda sürekli; basamak yazıları kontrastlı. | PDF'de |
| y24 | Yarım Metin Atölyesi | Önceki cümleler panelde görünür; son cümle öğrenci tarafından yazılır. | PDF'de |
| y25 | Kütüphane Görevlisi | Gerçek raf ve kapaklar; tür kapaktan çıkarımla bulunur. | PDF'de |
| y26 | Yazım Hatası Avcısı | Kalem otomatik düzeltmez; öğrenci doğru biçimi seçer veya yazar. | PDF'de |
| y27 | İki Metin Terazisi | İki metin yan yana görünür; aynı konu / aynı ileti ayrımı yapılır. | PDF'de |
| y28 | Eş Anlam Köprüsü | Sözcükler cümle bağlamıyla verilir; öğrenci cümle kurup söyler. | PDF'de |
| y29 | Mektup Yazı İşleri | Gerçek mektup şablonu; öğrenci mini mektubu klavyeyle yazar. | PDF'de |
| y30 | Okur Kimliği Anketi | Cevap cümlesi tür adını söylemez; çetele çizgisiyle birikir, beşinci dördü keser. | PDF'de |
| y31 | Kitap Anatomisi | Bölümler sıralanınca kitap gerçekten kurulur; işlev sorusu sorulur. | PDF'de |
| y32 | Dilek Kutusu | Tür seçimi ayrı adım; öğrenci dileğini iki cümleyle yazar. | PDF'de |
| y33 | Sanat Atölyesi Siparişi | İstek açıklayıcı metin; seçim amaçla gerekçelendirilir. | PDF'de |
| y34 | Yetenek Ayırma Bandı | Üç gerçek stant; çok alanlı etkinlikler ölçüt tartışmasıyla verilir. | PDF'de |
| y35 | Duygu Noktalaması | Replik seçilen işarete göre farklı tonda seslendirilir. | PDF'de |
| y36 | Vurgu ve Tonlama Ayarı | Tren kaldırılır; her seçimde gerçek sunum sesi dinletilir. | PDF'de |
| y37 | Benzetme Makinesi | Benzeyen-benzetilen görsel gösterilir; kurulan benzetme resimlenir. | PDF'de |
| y38 | Jest ve Mimik Aynası | Gerçek yüz/beden çizimleri; duygu animasyonla canlanır. | PDF'de |
| y39 | Sözcük Anlamı Radarı | Seçenekler sabit; bağlam ipucu karar öncesi işaretlenir. | PDF'de |
| y40 | Yetenek Basamakları | Hikâye metni görünür; tahmin metin kanıtıyla gerekçelendirilir. | PDF'de |
| y41 | Gerçek mi Mecaz mı? | Cümle sabit okunur kartta; aynı sözcük iki kullanımda karşılaştırılır. | PDF'de |
| y42 | Atasözü Köprüsü | Anlam kısa canlandırmayla gösterilir; yaşam durumuna bağlanır. | PDF'de |
| y43 | Kodlama Laboratuvarı | Program numaralı cümleler hâlinde okunur; öğrenci yönergeyi yazar. | PDF'de |
| y44 | Mucit Atölyesi | İstek amaç-araç-adım planı olarak okunur; eleme gerekçelenir. | PDF'de |
| y45 | Deney Raporu Tamiri | Gerçek rapor şablonu; listeleme iki nokta ve virgülle çalışılır. | PDF'de |
| y46 | Gürültü Ölçer | Her ortamın gerçek ses kaydı çalınır; öğrenci kontrol listesi doldurur. | PDF'de |
| y47 | Deyim Makinesi | Deyim bölünmez blok; uygun bağlam seçilir, öğrenci cümle yazar. | PDF'de |
| y48 | Araştırma Adımları | Bilim panosu; eksik adım bulma görevi eklenir. | PDF'de |
| y49 | Müze Rehberi | Gerçek eser görselleri; istek çıkarım gerektirir, öğrenci eser tanıtır. | PDF'de |
| y50 | Türkçe Koruma Kalemi | Kalem otomatik değiştirmez; öğrenci karşılığı seçip cümleyi yazar. | PDF'de |
| y51 | Bayram Panosu Dizgisi | Gerçek pano; kesme işareti ve tarih yazımı eklenir. | PDF'de |
| y52 | Eser Haritası | Türkiye haritası sahne; eser şehrine yerleşir, bilgi cümlesi okunur. | PDF'de |
| y53 | Tören Sırası | Adımlar sıralandıkça tören canlanır; hatalı adım bulma eklenir. | PDF'de |
| y54 | Kültür Bekçisi | Davranışlar görselli ve sabit; niyet-etki ayrımı çalışılır. | PDF'de |
| y55 | Vatan Şiiri Makinesi | Cümle panoya asılıp okunur; öğrenci kendi cümlesini yazar. | PDF'de |
| y56 | Kültür Diktesi | Hedef sözcük yazılmaz; kültür sözcükleri görselle desteklenir. | PDF'de |
| y57 | Hak mı Sorumluluk mu? | Adalet terazisi; hak-sorumluluk çifti birlikte verilir. | PDF'de |
| y58 | Dilekçe Masası | Gerçek dilekçe şablonu; öğrenci kurgusal dilekçeyi doldurur. | PDF'de |
| y59 | Hak Bildirisi Tamiri | İşaretin anlamı nasıl değiştirdiği örnekle gösterilir ve seslendirilir. | PDF'de |
| y60 | Pekiştirme Diktesi | Hedef sözcük yazılmaz; farklı pekiştirme türleri dinletilir. | PDF'de |
| y61 | Güvenli Yol Yönergesi | Gerçek mahalle; tehlikeler gerekçeli; öğrenci yönergeyi yazar. | PDF'de |
| y62 | Denge Köprüsü | Hak ve sorumluluk kalasları köprüyü dengede tutar; yazılar sığar. | PDF'de |
| y63 | Söz Hakkı Makinesi | Cümle mikrofonda sesli okunur; öğrenci isteğini yazıp sunar. | PDF'de |
| y64 | Gizlilik Kalkanı | Yakalama kaldırılır; karar gerekçe seçilerek verilir. | PDF'de |

"PDF'de" = düzeltme şartnamesi yazıldı, uygulamaya henüz aktarılmadı.
