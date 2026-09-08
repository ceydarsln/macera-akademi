# 2. Sınıf Türkçe PDF Düzeltme Takibi

Kaynak: `output/pdf/2_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf` (u01–u90, 90 oyun).
Şartnamenin yapılandırılmış hâli: `tmp/spec_u.json` (katalog + `build_turkish2_detailed_corrections.py`).
Motor: `web/phaser/turkce2-pdf-phaser.html` (matematik3 çerçevesi + Türkçeye özgü mekanikler).

**Durum: 90/90 oyun uygulandı — 2. sınıf Türkçe tamamlandı.**

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
| u77 | Devre Tamircisi | yazma | Bozuk cümlede özne, yüklem ve noktalama ayrı devre parçası; hangi parçanın eksik olduğu tek tek bulunuyor. 3. turda cümle çocuk tarafından baştan yazılıyor. | Uygulamada |
| u78 | Gözlem Kulesi | okuma | Manzara betimlemesinde renk, ses ve hareket ayrıntıları ayrı kanıt olarak işaretleniyor; ayrıntı ile genel ifade ayrılıyor. 3. turda kendi gözlemi yazılıyor. | Uygulamada |
| u79 | Karşılaştırma Matrisi | okuma | İki metin aynı ölçütlerde karşılaştırılıyor; benzerlik ve farklılık ayrı sütun. Kanıt işaretlenmeden karşılaştırma seçeneği açılmıyor. | Uygulamada |
| u80 | Geri Dönüşüm Bandı | dinleme | Atık türleri yalnız sesle veriliyor; kutu seçimi ayırt edici özelliğe dayanıyor. 3. turda çocuk kendi ayırma kuralını yazıyor. | Uygulamada |
| u81 | Kültür Sözlüğü | yazma | Yöresel sözcükler bağlamdan çıkarılıyor; madde başı, anlam ve örnek cümle üç ayrı adım. 3. turda çocuk kendi maddesini yazıyor. | Uygulamada |
| u82 | Tarihî Mekân Rehberi | konuşma | Mekân tanıtımı; ad, özellik ve ziyaret önerisi ayrı ölçüt. 3. turda kısa rehber konuşması yapılıp öz değerlendirme yapılıyor. | Uygulamada |
| u83 | Bayram Sabahı Yönergesi | yazma | Bayram hazırlığı sıralı yönergeye dönüştürülüyor; sıra bağlacı ve adım sayısı ölçüt. 3. turda yönerge çocuk tarafından yazılıyor. | Uygulamada |
| u84 | Kimlik Formu | yazma | Form alanları bilgi türüne göre dolduruluyor (ad, yaş, sınıf, tarih); her alanın hangi tür bilgiyi aldığı ayrı tur. 3. turda kurgusal bir karakterin formu klavyeyle dolduruluyor — çocuktan kendi kişisel bilgisi istenmiyor. | Uygulamada |
| u85 | Nedenini Söyle | yazma | Karar ve gerekçe iki ayrı adım; gerekçe seçenekleri karar verilmeden açılmıyor. İlgili, ilgisiz ve çelişkili gerekçe ayrılıyor. 3. turda görüş ve nedeni "çünkü" ile yazılıyor. | Uygulamada |
| u86 | Benzetme Halısı | konuşma | Benzeyen ve benzetilen halı desenlerinde eşleşiyor; "gibi/kadar" ile kurulan uygun benzetme anlamsızdan ayrılıyor. 3. turda kültürel bir nesne için özgün benzetme sesli kuruluyor. | Uygulamada |
| u87 | Okuma Hatası Dedektifi | okuma | Bayram şiiri gerçek kayıt olarak dinletiliyor; atlama, yanlış okuma, aşırı hız ve uygunsuz duraklama ayrı kategori. 3. turda dize yeniden okunup öz düzeltme yapılıyor. | Uygulamada |
| u88 | Söz Alma Sırası | konuşma | Tam sınıf sahnesi; söz alma zamanı, dinleme duruşu ve söz kesmeme ayrı ele alınıyor. 3. turda uygun zamanda konuyla ilgili soru sesli soruluyor. | Uygulamada |
| u89 | Hazine Kutusu: Konu Bulma | dinleme | Metin, konu etiketi ve kanıt üç ayrı adım; konu, ana fikir ve ayrıntı ayrılıyor. Kutu ancak konu ile kanıt birlikte verilince açılıyor. 3. turda konu kendi cümlesiyle yazılıp kanıt ekleniyor. | Uygulamada |
| u90 | Üslup Seçici | konuşma | Aynı istek müze görevlisine, arkadaşa ve nineye farklı üslupla kuruluyor; resmî üslubun işaretleri kanıtla gösteriliyor. 3. turda iki cümlelik konuşma canlandırılıyor. | Uygulamada |

## Canlı tarayıcı testinde bulunan ve düzeltilen kusurlar (u84–u90 partisi)

| # | Kusur | Nerede | Düzeltme |
|---|---|---|---|
| 1 | `esle` turunda etiket seçilince hiçbir görsel iz kalmıyordu; çocuk neyi seçtiğini göremiyordu. | `esleCiz` + CSS | Seçili etikete `.secili` (turuncu çerçeve + ✓), boş yuvalara nabız atan `.hedef` sınıfı. |
| 2 | Hızlı çift dokunuş tek hata için iki can götürüyordu (3 → 1). | `wrong()` | 550 ms ceza soğuması; her turda sıfırlanıyor. Dört hızlı yanlış dokunuş artık tek can. |
| 3 | "Hazırım" düğmesine örneği dinlemeden basmak can götürüyordu. | `konusCiz` | Ön koşul uyarısı `uyar()` ile cezasız. |
| 4 | Rubrikte ölçüt işaretlemeden bitirmek can götürüyordu (dürüst öz değerlendirmeyi cezalandırıyordu). | `konusCiz` | `uyar()`. |
| 5 | Boş metin gönderimi can götürüyordu; oysa eksik ölçüt ekranda zaten canlı görünüyor. | `yazCiz`, `duzeltCiz` | Eksik ölçüt ve "değişiklik yok" uyarıları `uyar()` ile cezasız; örnek cümleyi kopyalama hâlâ hata sayılıyor. |
| 6 | `ornekCevap` (u85) `enAzKelime` eşiğinin altındaydı; koşum zaman aşımına düşüyordu. | `GAMES.u85` | Örnek cevap 13 sözcüğe çıkarıldı. |

## Kabul ölçütü denetimi (tools/tr2_denetim.html)

`tools/hb2_denetim.html`'den (2. sınıf hayat bilgisi oturumu) uyarlanan tarayıcı aracı,
90 oyunun 270 turunu 390×844'te tek tek çizip dört ölçütü tarıyor: yatay/dikey kırpılma,
44 px dokunma alanı ve merkezine başka öğe binmesi, etiketlerde emoji ipucu, cevap sızıntısı.
İlk taramada çıkan ve düzeltilen bulgular:

| # | Bulgu | Kapsam | Düzeltme |
|---|---|---|---|
| 7 | Dokunma alanı 44 px'in altında: kelime bankası düğmeleri 29 px, sıralama kartları 33 px, yuva kartları 42 px, rubrik satırları. | 164 tur | `.kelime-bank button`, `.sira-kart`, `.rubrik button`, `.yuvakart` için `min-height:44px`. |
| 8 | `sira` turunda kartlar veri sırasında çiziliyordu; `dogru` çoğu turda `[0,1,2,…]` olduğu için doğru sıra ekrandan okunabiliyordu. | u02 tur 1 | `siraDizilim()` — oyun kimliği ve tur numarasından türeyen tohumlu (rastgelesiz) karıştırma; `data-kart` gerçek dizini taşıdığı için koşum etkilenmiyor. |
| 9 | Uzun etiketler dar sütunda yatayda kırpılıyordu ("mahallemizdeki çocuklar", "İlgilenmiyorum."). | u08 tur 3, u17 tur 1 | `.choice`/`.action` için `overflow-wrap:anywhere; hyphens:auto`. |

Aracın ilk sürümü `kanit` turlarında 12 "doğru seçenek metinde yazılı" bulgusu üretti; bunlar
yanlış pozitif: ana fikir, sözlük anlamı ve "birinci/ikinci kapak" turlarında doğru seçeneğin
metinde geçmesi tasarım gereğidir — çocuk zaten kanıtı işaretleyerek seçiyor. Bu kural,
"seçenekler kanıt işaretlenmeden açılmasın" denetimiyle değiştirildi.

Düzeltmelerden sonra: **270/270 tur temiz.**

### Peer oturumunun (2. sınıf hayat bilgisi / 4. sınıf Türkçe) bildirdiği ve burada da doğrulanan kusur

`render()` sonundaki `requestAnimationFrame(()=>speak(round().prompt))` geri çağrısı bir sonraki
karede çalışıyor; gizli sekmede rAF hiç çalışmadığı için kuyrukta bekliyor ve sekme görünür
olunca dönüyor. O ana kadar oyun bitmişse `round()` undefined olup TypeError fırlatıyordu.
Yeniden üretildi (`render(); roundIndex=3;` ardından iki kare) ve üç motorda da düzeltildi
(`turkce2-pdf`, `sayma-pdf`, `matematik3-pdf`): geri çağrı hem `round()` varlığını hem de tur
numarasının değişmediğini doğruluyor — böylece geciken kare bir önceki turun yönergesini de okumuyor.


Test kapsamı: 375×812 ve 1280×800; boş gönderim, 4000 karakterlik girdi, etiketsiz yuva dokunuşu,
art arda hızlı dokunuş, sınırsız tekrar dinleme, tur geçişleri ve bitiş ekranı. Konsolda hata yok,
ağ isteklerinin tamamı 200. Koşum: `tools/dom_kosum.html#ids=u01…u90` → 90/90.

## Ses yedeği (26 Ağustos 2026)

Bu motorda hedef şartname gereği ekrana **kasten yazılmıyor**, yalnız sesle veriliyor.
Cihazda Türkçe ses paketi yoksa (ya da kullanıcı sesi kapattıysa) kataloğun `speakNow`
işlevi `false` dönüyor ve `oku()` bunu iletiyor — fakat hiçbir motor bu dönüşü
kontrol etmiyordu. Sonuç: sessiz cihazda oyun **çözülemez** hâle geliyordu; çocuk ne
duyuyor ne görüyordu. Kataloğun kendi yorumunda mekanizma zaten tarif edilmişti
("Dönüş değeri sayesinde alt oyun … adil görsel ipucuna düşebilir") ama kullanan yoktu.

Ölçülen etki (düzeltmeden önce, çözülemeyen tur sayısı):
1. sınıf Türkçe 94 tur / 35 oyun · 1. sınıf sayma 30 tur / 10 oyun ·
2. sınıf Türkçe 14 tur / 12 oyun — **toplam 138 tur / 57 oyun**.

Uygulanan çözüm:

- `speak()` artık gerçekten seslendirme olup olmadığını `sesVar` bayrağında tutuyor.
  Köprü (`parent.oku`) varsa **onun cevabı bağlayıcıdır**; motorun kendi
  `speechSynthesis`'ine düşmek köprünün "ses yok" sinyalini maskeliyordu.
  Köprü yoksa `getVoices()` içinde Türkçe ses aranıyor; liste boşsa
  (ilk çağrıda olabiliyor) yanlış alarm verilmiyor.
- Seslendirme olmuyorsa turun gizli hedefi `🔇 Ses açılamadı, hedef gösteriliyor: …`
  şeridiyle görünür kılınıyor. Hedef tur boyunca sabit kalıyor; "zaten açıldı"
  koşulları şeridi turun ortasında bayatlatıyordu.
- Ses çalışırken şerit hiç çizilmiyor, hedef gizli kalıyor (gerileme testi yapıldı).

Gerekçe: çözülemeyen oyun, görünen hedeften kötüdür. Şartnamenin "hedef ekranda
yazılı olmayacak" kuralı sesin çalıştığı durumda aynen geçerli; yedek yalnız
oyunun oynanamaz hâle geldiği durumda devreye giriyor.

Bu motorda etkilenen kipler: dinle kipi.
