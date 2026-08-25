# 2. Sınıf Türkçe PDF Düzeltme Takibi

Kaynak: `output/pdf/2_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf` (u01–u90, 90 oyun).
Şartnamenin yapılandırılmış hâli: `tmp/spec_u.json` (katalog + `build_turkish2_detailed_corrections.py`).
Motor: `web/phaser/turkce2-pdf-phaser.html` (matematik3 çerçevesi + Türkçeye özgü mekanikler).

**Durum: 76/90 oyun uygulandı.**

## Şartnamenin dört kip kuralı ve motordaki karşılığı

| Kip | Şartname | Motor |
|---|---|---|
| Okuma | "Öğrenci cevaptan önce metindeki kanıtı işaretlesin; doğru seçenek ancak kanıtla tutarlı olduğunda kabul edilsin." | `kanit` mekaniği: metindeki aday bölümler önceden vurgulanmaz, yalnız dokunulabilir olduğu bellidir. Gerekli kanıt işaretlenmeden seçenekler açılmaz; yanlış kanıtta cevap söylenmez, soruya geri gönderilir. |
| Yazma | "Son turda öğrenci gerçek bir sözcük, cümle, yönerge veya form alanı üretsin; hazır cümle seçimi tek başına başarı sayılmasın." | `yaz` mekaniği: gerçek metin alanı. Ölçütler (en az sözcük, büyük harf, bitiş işareti, geçmesi gereken sözcük, satır sayısı) yazarken canlı işaretlenir. `yasak` listesiyle örnek cümlenin kopyalanması reddedilir. Kelime bankası yalnız erişim desteğidir. |
| Dinleme | "İlk dinleme turunda hedef metin ve cevap anahtarı görünmesin; ses en az iki kez tekrar edilebilsin ve tekrar dinleme ceza oluşturmasın." | `dinle` mekaniği: metin ekranda yazılı değil, seçenekler ancak dinledikten sonra açılır, tekrar dinleme sınırsız ve cezasız. |
| Konuşma | "Örnek dinletildikten sonra öğrenci kısa bir ses kaydı alsın veya öz değerlendirme rubriğiyle konuşsun; vurgu, hitap, sıra ve anlaşılabilirlik ayrı kaydedilsin." | `konus` mekaniği: önce örnek dinlenir, sonra "basılı tut ve konuş" ile gerçek sesli üretim yapılır (süre ölçülür, 1,2 saniyeden kısa konuşma kabul edilmez), ardından ölçütler tek tek işaretlenir. |

## Motor tarafında eklenenler

- `kanit`: kanıt-önce-cevap; çeldirici aday bölümler.
- `yaz`: canlı ölçüt denetimi, kelime bankası, kopyalama reddi.
- `dinle`: metinsiz dinleme, cezasız tekrar.
- `konus`: örnek → sesli üretim → öz değerlendirme rubriği.
- `sira`: sabit kartlarla olay sıralama (hareketli kart yakalama kaldırıldı).
- `esle`: gerçek sahnede etiket yerleştirme (genel PARÇALAR/hedef kutuları kaldırıldı).
- `duzelt`: doğru biçim otomatik verilmez; öğrenci metni gerçekten düzenler.

| ID | Oyun | Kip | Uygulanan ana düzeltme | Durum |
|---|---|---|---|---|
| u01 | Kapak Dedektifi | okuma | Genel eşleştirme motoru kaldırıldı: kütüphane rafı ve kapak ayrıntıları var. Konu seçeneği ancak kapaktaki iki kanıt işaretlendikten sonra açılıyor; 2. turda konu ile ayrıntı (saat, silgi) ayrıştırılıyor; 3. turda başlık ile kapak çelişiyor ve çocuk tahminini "çünkü" ile kendi cümlesinde yazıyor. | Uygulamada |
| u02 | Masal Treni | konuşma | Roket-yakıt motoru gitti; lokomotif ve sabit vagonlar var, kartlar hareket etmiyor. 2. turda ortadaki iki olay yakın anlamlı çeldirici. 3. turda çocuk masalı "çünkü/sonunda" ile sesli anlatıp kendini rubrikle değerlendiriyor. | Uygulamada |
| u03 | Kelime Ormanı | yazma | Uzay lazeri kaldırıldı; sözcüğün geçtiği cümle orman tabelasında sabit duruyor. Anlam seçeneği ancak bağlam ipucu işaretlenince açılıyor. 2. turda aynı sözcük iki bağlamda karşılaştırılıyor; 3. turda çocuk kendi cümlesini yazıyor. | Uygulamada |
| u04 | Noktalama Yağmuru | yazma | Sarı nokta-kapsül dili kaldırıldı; cümleler sabit ve tonuyla okunuyor. 2. turda aynı cümle gövdesi üç işaretle karşılaştırılıyor. 3. turda çocuk iki cümleyi kendi yazıp soru işareti ve ünlemi kendisi koyuyor. | Uygulamada |
| u05 | Sihirli Erdem Ağacı | okuma | Cevap elması ancak olay kanıtı işaretlendikten sonra seçilebiliyor. 2. turda saygı ile yardımlaşma iki kısa olayla ayrıştırılıyor. 3. turda çocuk kendi yaşamından örnek cümle yazıyor. | Uygulamada |
| u06 | Robotun Nezaket Yolu | yazma | Komut kartları sabit; robot gerçek kaldırım ve yaya geçidinde ilerliyor. 2. turda iki komut dizisinden güvenli ve nazik olanı, tehlikeli adım işaretlenerek seçiliyor. 3. turda çocuk dört adımlı yeni bir yönerge yazıyor. | Uygulamada |
| u07 | Kırık Köprü | yazma | Köprünün eksik tahtaları anlam bağını temsil ediyor; 2. turda iki yakın tamamlama metindeki ipucu (buz) işaretlenerek ayrıştırılıyor; 3. turda çocuk yeni bir cümleyi "çünkü" ile kendi sözüyle tamamlıyor. | Uygulamada |
| u08 | 5N1K Dedektifi | okuma | Büyüteç kaldırıldı; metin geniş satır aralığıyla sabit duruyor. Kim/ne zaman/nerede/niçin ayrı kutulara metnin kendi sözcükleriyle taşınıyor. 2. turda açık bilgi ile çıkarım ayrıştırılıyor; 3. turda beş bilgilik tablo bağımsız dolduruluyor. | Uygulamada |
| u09 | Duygu Aynası | okuma | Karakterin yüzü hazır emojiyle verilmiyor; beden dili ve olay ipuçları ayrı ayrı işaretleniyor. 2. turda aynı olayda iki karakterin farklı duygusu nedenleriyle karşılaştırılıyor; 3. turda çocuk duyguyu iki kanıtla birlikte yazıyor. | Uygulamada |
| u10 | Ana Fikir Tohumu | okuma | Önce destekleyici ayrıntılar işaretleniyor, sonra ana fikir seçiliyor. 2. turda "arılar" (konu) ile "çalışmak önemlidir" (ana fikir) ayrı kutulara ayrılıyor; 3. turda çocuk yeni paragrafın ana fikrini yazıp iki ayrıntıyla destekliyor. | Uygulamada |
| u11 | Sihirli Fosforlu Kalem | yazma | Hedef sözcük cevabı baştan söylemiyor; çocuk eş anlamlı çifti cümlede kendisi buluyor. 2. turda eş anlamlıların her cümlede yer değiştiremeyeceği gösteriliyor ("kara sular" / "siyah kalem"); 3. turda ikisi ayrı cümlelerde kullanılıyor. | Uygulamada |
| u12 | Paragraf Asansörü | yazma | Kartlar sabit, zaman bağları görünür. 2. turda konuya uymayan dördüncü cümle yerleştirilemiyor ve nedeni söyleniyor; 3. turda çocuk giriş-gelişme-sonuç yapısında kendi paragrafını yazıyor. | Uygulamada |
| u13 | Noktalama Akvaryumu | yazma | Baloncuklar gerçek cümle parçası; virgülün sıralama ve hitap görevleri ayrı turlarda çalışılıyor. 3. turda çocuk iki cümleyi kendi yazıp virgül ve soru işaretini kendisi koyuyor. | Uygulamada |
| u14 | Kayıp Kitaplık | okuma | Mevsim/yer bilgisi metinde yazmıyor; çocuk iki ipucunu işaretleyip çıkarım yapıyor. 2. turda tek ipucunun yetmediği gösteriliyor; 3. turda çıkarım "Bence … çünkü metinde …" kalıbıyla yazılıyor. | Uygulamada |
| u15 | Anlamını Bulan Işıldak | yazma | Işıldak hedef sözcüğü değil bağlam ipuçlarını aydınlatıyor; seçenekler sabit. 2. turda yakın iki anlam kanıtla ayrıştırılıyor; 3. turda tahmin-sözlük-kullanım üç adımı tamamlanıyor. | Uygulamada |
| u16 | Hazine Haritası | okuma | Yönerge okunup sırayla uygulanıyor; 2. turda sağ-sol ve önce-sonra içeren dört adımlı rota var; 3. turda çocuk üç adımlı kendi yönergesini yazıyor. | Uygulamada |
| u17 | Karakterlerin Sohbeti | konuşma | Aynı istek arkadaş, öğretmen ve yabancı büyük için ayrı ayrı karşılaştırılıyor. 3. turda çocuk özür-hitap-teşekkür içeren diyaloğu sesli canlandırıp rubrikle değerlendiriyor. | Uygulamada |
| u18 | Zıt Anlamlılar Ekspresi | yazma | Köprü kutuları kaldırıldı, çiftler vagonlarda yan yana. 2. turda önce-sonra ve erken-geç gibi bağlama duyarlı çiftlere geçiliyor; 3. turda iki çift aynı paragrafta kullanılıyor. | Uygulamada |
| u19 | Neden-Sonuç Köprüsü | okuma | Her neden sonucuna bağlanıyor; 2. turda aynı ilişki "çünkü" ve "bu yüzden" ile iki yönde kuruluyor; 3. turda biri doğa biri günlük yaşamdan iki cümle yazılıyor. | Uygulamada |
| u20 | Zaman Şeridi | konuşma | Roket-yakıt sahnesi kaldırıldı, yatay zaman şeridi ve sabit kartlar var. 2. turda önce/ardından/daha sonra/en sonunda ayırt ediliyor; 3. turda çocuk üç cümlelik sözlü özet yapıyor. | Uygulamada |
| u21 | İstiklâl Kâşifi | yazma | El yazması defter sabit; parlayan sözcük ile bağlam ipucu aynı görüş alanında. "Cephe/cephane" gibi yakın sözcükler ayrı cümlelerde karşılaştırılıyor; 3. turda sözlük kontrolünden sonra yeni cümle yazılıyor. | Uygulamada |
| u22 | Noktalama Muhafızları | yazma | Kapsül/radar dili kaldırıldı; cümleler sabit ve tonuyla okunuyor. 2. turda aynı gövde üç işaretle karşılaştırılıyor; 3. turda tören üzerine üç cümle yazılıp nokta-soru-ünlemle bitiriliyor. | Uygulamada |
| u23 | Yarım Kalan Mektup | yazma | Devam seçenekleri metnin üslubuna uyuyor; 2. turda kişi, zaman ve duygu tutarlılığı sınanıyor ("dün" diyen metne gelecek zamanlı devam reddediliyor). 3. turda çocuk mektubun sonunu kendi yazıyor. | Uygulamada |
| u24 | Karakter Aynası | konuşma | Venn aynası: yalnız Atatürk / ikisinde de / yalnız sen bölgeleri. 2. turda "benzer olmak aynı olmak değildir" ayrımı kuruluyor; 3. turda bir benzerlik ve bir fark tam cümleyle yazılıyor. | Uygulamada |
| u25 | Tabela Avcısı | okuma | Su altı balık-ağ motoru kaldırıldı; tarihî sokakta matbaa, el yazısı ve okul yazısı tabelaları var. 2. turda MANAV/MANAJ/MANEVRA çeldiricileri harf harf ayırt ediliyor; 3. turda çocuk tabelayı sesli okuyup biçim değişse de sözcüğün aynı kaldığını açıklıyor. | Uygulamada |
| u26 | Büyük Harf Kalkanı | yazma | Doğru biçim otomatik verilmiyor: çocuk telgraf metnini gerçekten düzenliyor, beş ölçüt canlı denetleniyor. 2. turda kişi/şehir/bayram/kurum adları ayrılıyor; 3. turda iki cümle klavyeyle yeniden yazılıyor. | Uygulamada |
| u27 | Doğruluk Terazisi | dinleme | Kayıt metni ekranda yazılı değil, tekrar dinleme cezasız. 2. turda kısmen doğru bilgi ile tümüyle yanlış bilgi ayrılıyor; 3. turda karar "Biliyorum çünkü …" ile gerekçelendiriliyor. | Uygulamada |
| u28 | Hitap Yıldızları | konuşma | Arkadaş, öğretmen ve misafir için ayrı hitaplar; 2. turda selamlaşma-hitap-vedalaşma konuşmanın farklı yerlerine yerleştiriliyor; 3. turda iki turlu diyalog sesli canlandırılıyor. | Uygulamada |
| u29 | Örneklendirme Ağacı | yazma | Balık-ağ motoru kaldırıldı; destekleyen, ilgisiz ve ters örnekler ayrı dallara ayrılıyor. 3. turda çocuk kendi örnek cümlesini yazıyor. | Uygulamada |
| u30 | Vurgu Stüdyosu | konuşma | Meteora nişan alma yerine iki kayıt dinlenip karşılaştırılıyor; düz/aşırı/uygun vurgu ayırt ediliyor. 3. turda çocuk dizeyi sesli okuyup vurgu-hız-duraklama rubriğiyle değerlendiriyor. | Uygulamada |
| u31 | Kayıp İleti Şifresi | okuma | Kasa ancak ana ileti ile kanıt birlikte seçilince açılıyor; konu/ana ileti/ayrıntı üç ayrı çarka ayrılıyor. 3. turda ileti kendi cümlesiyle yazılıp kanıtla destekleniyor. | Uygulamada |
| u32 | Orman Kâşifleri | okuma | Canlılar metindeki gözlenen eylemlere göre sınıflanıyor; 2. turda ördek örneğiyle ölçüt değişince grubun da değiştiği gösteriliyor. 3. turda çocuk yeni canlı ekleyip gerekçe yazıyor. | Uygulamada |
| u33 | Soru Yağmuru | yazma | Edatlar aynı görünümde; seçim son ünlüye göre yapılıyor. 2. turda bitişik yazılmış edatlar çocuk tarafından ayrılıyor (doğru biçim verilmiyor). 3. turda dört edatla dört soru cümlesi yazılıyor. | Uygulamada |
| u34 | İklim Makinesi | okuma | Etiket köprüsü yerine neden-sonuç kabloları; 2. turda tek nedenin iki sonucu gösteriliyor. 3. turda çocuk kendi gözlemini neden-sonuç cümlesine çeviriyor. | Uygulamada |
| u35 | Bukalemunun Şiiri | yazma | Benzeyen ve benzetilen metinde işaretleniyor; uygun/uygunsuz benzetme karşılaştırılıyor. 3. turda çocuk özgün benzetme dizesi yazıyor. | Uygulamada |
| u36 | Kayıp İzci | yazma | Hareketli uzay hedefleri kaldırıldı; izci günlüğünde bağlam ipucu işaretleniyor. Aynı sözcük iki doğa cümlesinde inceleniyor; 3. turda tahmin-sözlük-yeni cümle döngüsü bağımsız tamamlanıyor. | Uygulamada |
| u37 | Doğa Fotoğrafçısı | yazma | Cümleler balık değil fotoğraf alt yazısı kartı; olay/yer/ayrıntı ayrıştırılıyor. 3. turda başlık + bağlantılı iki cümle yazılıyor. | Uygulamada |
| u38 | Bilmece Kutusu | okuma | Konu seçenekleri ancak iki görsel ipucu işaretlenince açılıyor; aynı başlığa uyan iki kapaktan güçlü olan kanıtla seçiliyor. 3. turda yeni başlık için tahmin cümlesi yazılıyor. | Uygulamada |
| u39 | Fikir Terazisi | okuma | Katılıyorum/katılmıyorum kefeleri gerekçe taşıyor; güçlü ve zayıf gerekçe karşılaştırılıyor. 3. turda karar tam cümleyle gerekçelendiriliyor. | Uygulamada |
| u40 | Hata Avcısı Papağan | konuşma | Dört okuyuş yalnız sesle ayırt ediliyor (yazılı etiket cevabı vermiyor); hız, ses ve anlaşılırlık ayrı ölçüt. 3. turda çocuk aynı cümleyi okuyup öz düzeltme yapıyor. | Uygulamada |
| u41 | Sınıflandırma Fabrikası | okuma | Nesneler sabit karar noktalarında; metindeki nesne ile kutu rengi tutarlı. 2. turda malzeme yerine amaç ölçütü kullanılıyor. 3. turda üç yeni nesne gerekçesiyle yazılıyor. | Uygulamada |
| u42 | Orman Postacısı | yazma | Kısa mesaj kim-nerede-ne yaptı kartlarıyla genişletiliyor; 3. turda üç cümlelik posta yazılıyor. | Uygulamada |
| u43 | Dinleyici Karşısında | konuşma | Göz teması, ses, sıra ve beden dili ayrı ölçüt; hangi kuralın bozulduğu metinden bulunuyor. 3. turda 30 saniyelik konuşma yapılıp rubrikle değerlendiriliyor. | Uygulamada |
| u44 | Sözlük Kâşifi | yazma | Roket motoru kaldırıldı, sözcük kartları sözlük sayfasına diziliyor. 2. turda ilk harf aynıyken ikinci harfe bakılıyor; 3. turda beş sözcük bağımsız sıralanıyor. | Uygulamada |
| u45 | Sessiz Okuma Dedektifi | okuma | Süre baskısı yok; anlam soruları sabit kartlarda. Açık bilgi / çıkarım / ana fikir soruları ayrıştırılıyor. 3. turda çocuk okuma stratejisini ve zorlandığı yeri yazıyor. | Uygulamada |
| u46 | Kitap Kurdunun Odası | okuma | Balık ağı kaldırıldı; ışık, ses ve oturuş gerçek nesnelerle düzenleniyor. 2. turda iki uygun düzenden daha iyisi gerekçeyle seçiliyor; 3. turda üç maddelik plan yazılıyor. | Uygulamada |
| u47 | Gerçeklik Tarayıcısı | dinleme | Cümle yalnız sesli veriliyor; gerçek / olası / hayal ürünü ayrı kategorilerde çalışılıyor. 3. turda gerekçe yazılıyor. | Uygulamada |
| u48 | Tiyatro Sahnesi | konuşma | Meteor yerine karakterin yüzü ve bedeni; aynı cümlenin sevinç, korku ve şaşkınlık beden dili karşılaştırılıyor. 3. turda çocuk iki duyguyla canlandırıyor. | Uygulamada |
| u49 | Kısaltma Postanesi | yazma | Tam ad ↔ kısaltma eşleşmesi; noktalı (unvan) ve noktasız (kurum, ölçü) kısaltmalar ayrılıyor. 3. turda üç kısaltma cümle içinde yazılıyor. | Uygulamada |
| u50 | Broşür Dedektifi | okuma | Broşürün harita/saat/hayvan bölümleri aynı sayfada; metin ile görselin tamamlandığı ve ÇELİŞTİĞİ örnekler karşılaştırılıyor. 3. turda iki bilgi kendi cümlesiyle yazılıyor. | Uygulamada |
| u51 | Editörün Kırmızı Kalemi | yazma | Doğru biçim otomatik gelmiyor; çocuk metni satır satır kendisi düzenliyor. Yazım / büyük harf / noktalama hataları ayrı türlere ayrılıyor; 3. turda paragrafın tamamı bağımsız düzeltiliyor. | Uygulamada |
| u52 | Tablet ve Kitap | yazma | Tablet ve basılı sözlük iki gerçek kaynak; bir sözcüğün birden çok anlamından bağlama uyanı seçiliyor. 3. turda kaynak adı, anlam ve yeni cümle birlikte yazılıyor. | Uygulamada |
| u53 | Kitap Kapağı Yapbozu | okuma | Balık-ağ kaldırıldı; başlık, görsel ve yazar alanı sabit parçalarla tamamlanıyor. 2. turda başlığa uyan ama ayrıntısı yanlış kapak eleniyor; 3. turda alt başlık ve tahmin yazılıyor. | Uygulamada |
| u54 | Odaklanma Ustası | dinleme | Dinleme odasındaki engeller gerçek nesnelerle düzenleniyor; dış çevre engeli ile kendi davranışı ayrı ayrı ele alınıyor. 3. turda üç maddelik kontrol listesi yazılıyor. | Uygulamada |
| u55 | Kelime Aşçısı | yazma | Sözcük kavanozları sabit; bağlam ipucu işaretlenmeden seçenek açılmıyor. Yakın anlamlı "yemek/atıştırmak" ayrımı yapılıyor; 3. turda kendi cümlesi yazılıyor. | Uygulamada |
| u56 | Mikrofon Sende | konuşma | Roket yakıtı yerine sabah-öğle-akşam kartları; 2. turda bugüne ait olmayan olay yerleştirilemiyor. 3. turda gün üç bağlantılı cümleyle sesli anlatılıyor. | Uygulamada |
| u57 | Matbaa Tamircisi | yazma | Dokununca otomatik çözüm gelmiyor; metin elle düzenleniyor. Cümle başı, özel ad ve nokta hataları ayrı türlere ayrılıyor; 3. turda karışık metin bağımsız düzeltiliyor. | Uygulamada |
| u58 | Beden Dili Orkestrası | konuşma | Robotun tam bedeni görünüyor; uygun ve aşırı beden dili karşılaştırılıyor. 3. turda cümle uygun jest ve mimikle canlandırılıyor. | Uygulamada |
| u59 | Gerçeklik Dedektörü | dinleme | Cümleler yalnız sesli veriliyor; gerçek / mümkün / hayal ürünü üç grupta sınıflandırılıyor. 3. turda çocuk bir gerçek ve bir hayal cümlesi yazıp farkı açıklıyor. | Uygulamada |
| u60 | Yetenek Aynası | okuma | Venn aynasında iki metnin ortak ve özgü mesajları ayrılıyor; konu benzerliği ile ileti benzerliği ayrı örnekle karşılaştırılıyor. 3. turda ortak ileti ve bir fark yazılıyor. | Uygulamada |
| u61 | Dijital Mektup Arkadaşım | yazma | Hitap, gövde ve kapanış gerçek yazı alanları; arkadaş ile öğretmen üslubu ayrı turda. 3. turda mektup baştan sona çocuk tarafından yazılıyor (gönderme yok, ön izleme). | Uygulamada |
| u62 | Maceranı Seç Kütüphanesi | okuma | İlgi kartları ve kapaklar birlikte; iki uygun metinden AMACA uyanı seçiliyor. 3. turda çocuk ilgisini ve seçim gerekçesini yazıyor. | Uygulamada |
| u63 | Film Şeridi | yazma | Kareler sabit; 2. turda geri dönüş karesi sıraya girmiyor ve nedeni söyleniyor. 3. turda üç cümlelik özet yazılıyor. | Uygulamada |
| u64 | Kürsü Heyecanı | konuşma | Roket sahnesi kaldırıldı; not kartları giriş-gelişme-sonuç panosuna yerleşiyor, ana fikir ile örnek ayrılıyor. 3. turda çocuk kendi planıyla konuşuyor. | Uygulamada |
| u65 | Yazarın Çalışma Masası | yazma | Masa, ışık, araç ve düzen gerçek nesnelerle; fiziksel düzen ile planlama davranışı ayrılıyor. 3. turda üç maddelik plan yazılıyor. | Uygulamada |
| u66 | Ses Dedektifi | dinleme | İki kayıt sırayla dinleniyor, seçenekler dinlemeden önce görünmüyor (tarayıcıda doğrulandı). Ortak konu ile ortak mesaj ayrılıyor; 3. turda ortak ileti sesli söyleniyor. | Uygulamada |
| u67 | Yetenek Galerisi | okuma | Kapaklar etiketsiz; başlık ancak görsel kanıt işaretlenince seçiliyor. 2. turda güçlü/zayıf kanıt karşılaştırılıyor; 3. turda yeni başlığa kapak ve tanıtım yazılıyor. | Uygulamada |
| u68 | Olay Baloncukları | dinleme | Hikâye yalnız sesli; yazılı metin ilk turda görünmüyor. Geçen olay, çıkarılabilen olay ve hiç geçmeyen olay ayrılıyor; 3. turda üç olay sırayla anlatılıyor. | Uygulamada |
| u69 | Ön Bilgi Köprüsü | konuşma | Dinlenen bilgi ile öğrencinin ön bilgisi köprünün iki yanında; uyuşma ve çelişme ayrı ele alınıyor. 3. turda "Önceden… şimdi…" kalıbıyla sesli anlatım yapılıyor. | Uygulamada |
| u70 | Dijital Sözlük Avı | yazma | Uzay meteoru kaldırıldı; arama, madde başı ve anlam seçimi adım adım uygulanıyor. Birden çok anlamdan bağlama uyanı seçiliyor; 3. turda anlam ve yeni cümle yazılıyor. | Uygulamada |
| u71 | Notalı Noktalama | yazma | Piyano tuşları virgül, iki nokta ve tırnak; üçünün görevi ayrı örneklerle çalışılıyor. 3. turda eksik işaretler çocuk tarafından ekleniyor. | Uygulamada |
| u72 | Sahne Kuralları | konuşma | Beden bütünlüğü görünüyor; göz teması, duruş, el hareketi ve sahne alanı ayrı ölçüt. 3. turda kısa sahne denemesi yapılıp öz değerlendirme yapılıyor. | Uygulamada |
| u73 | Vurgu Avcısı | konuşma | Cümle sabit, büyüteç metni örtmüyor; vurgu yeri değişince anlamın değiştiği üç örnekle gösteriliyor. 3. turda istenen anlam sesle kuruluyor. | Uygulamada |
| u74 | Zaman Makinesi | dinleme | Olay yalnız sesli veriliyor; önce-sonra tahminleri metinle tutarlılığa göre ayrılıyor. 3. turda öncesi ve sonrası için birer cümle yazılıyor. | Uygulamada |
| u75 | Hologram Laboratuvarı | dinleme | Ses ve görsel ayrı; doğru eşleşme ayırt edici görsel ayrıntıya dayanıyor (hörgüç sayısı). 3. turda çocuk bir hologramı iki cümleyle betimliyor. | Uygulamada |
| u76 | Manyetik Zıtlık Deneyi | konuşma | Mıknatıs yalnız gerçek zıt çiftleri çekiyor; zıtlık ile ilgisizlik ayrılıyor. 3. turda iki zıt çiftle karşılaştırma cümleleri yazılıyor. | Uygulamada |
