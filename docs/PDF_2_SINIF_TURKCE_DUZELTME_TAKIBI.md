# 2. Sınıf Türkçe PDF Düzeltme Takibi

Kaynak: `output/pdf/2_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf` (u01–u90, 90 oyun).
Şartnamenin yapılandırılmış hâli: `tmp/spec_u.json` (katalog + `build_turkish2_detailed_corrections.py`).
Motor: `web/phaser/turkce2-pdf-phaser.html` (matematik3 çerçevesi + Türkçeye özgü mekanikler).

**Durum: 12/90 oyun uygulandı.**

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
