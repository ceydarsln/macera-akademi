# 1. Sınıf Matematik PDF Düzeltme Takibi

Kaynak belgeler:

- `output/pdf/1_sinif_matematik_kullanici_duzeltmeleri_duzenlenmis.pdf`
- `output/pdf/1_sinif_matematik_duzeltmeleri_devam.pdf`

Uygulama kaynağı: `web/phaser/matematik-pdf-phaser.html`

## Ortak kabul maddeleri

- [x] Her oyun tam üç farklı tur içeriyor; bitiş yalnız üçüncü doğru turdan sonra gerçekleşiyor.
- [x] Her turun yönergesi açılışta Türkçe okunuyor ve hoparlörle yeniden dinlenebiliyor.
- [x] `+`, `-`, `−` ve `=` işaretleri konuşmada artı, eksi ve eşittir olarak dönüştürülüyor.
- [x] Yanlışta yalnız bir can eksiliyor, “Tekrar dene” okunuyor; üç can sonunda “Canların bitti” ve yeniden başlat düğmesi gösteriliyor.
- [x] Sürüklenen yanlış parça kaybolmuyor; başlangıç yerine dönüyor. Hedefler telefon için büyük ve toleranslı.
- [x] Her doğru turun sonunda oyunun hikâyesine bağlı bir sonuç/başarı animasyonu oynuyor.
- [x] Eski genel uzay gemisi, asteroit, kepçe ve boş kart şablonları bu 49 oyunda kullanılmıyor.
- [x] Ana uygulamadaki tilki konuşma balonu, alt sahnenin etkin tur yönergesiyle güncelleniyor.
- [x] Web kaynağı tek kanonik kaynak; `tools/aynala.sh` ile APK varlığına aynı içerik kopyalanıyor.

## Ana PDF — 38 oyun

| Sayfa | Kimlik | Oyun | Uygulanan ana düzeltme |
|---:|:---:|---|---|
| 3 | m01 | Trafik Polisi | Hareketli renkli araçlar, gerçek yol/kavşak, geniş sağ-sol garajları, üç farklı trafik turu |
| 4 | m02 | Pusula Korsanı | Animasyonlu papağan, 5×5 harita, başlangıç bayrağı, yönergeden hesaplanan işaretsiz doğru kare |
| 5 | m03 | Dağcı Keçi | Büyük dağ, kalın basamaklar, komuta göre zıplayan keçi ve baştan görünen zirve bayrağı |
| 6 | m05 | Çorap Eşleştirmece | Büyük sepet/mandal, gerçek boy-renk-desen farkı taşıyan çoraplar, yanlış parçanın dönüşü |
| 7 | m09 | Çarkıfelek Dişlileri | Rakam yazmayan, gerçek diş sayılı SVG çarklar ve aynı çentik sayılı yuvalar |
| 8 | m10 | Parmak Canavarları | Beşer ayrı hareketli parmaklı iki büyük el, 5+2, 5+5 ve 1+5 turları |
| 9 | m11 | Uzaylı Asansörü | Uzaylıları tek tek kabine sürükleme, 20 hücreli onluk-birlik çerçevesi, 8/12/16 |
| 10 | m12 | Pazar Kasası | Görünür pazar, sepet ve tek tek sürüklenen 10/15/20 portakal |
| 11 | m14 | Sihirli Olta | Ad değişikliği; gerçek olta sürükleme, sabit yüksek kontrast balık renkleri, 3 renk turu |
| 12 | m15 | Şipşak Hafıza | Her tur ve platformda 10 saniyelik görünür önizleme, geri sayım çubuğu, yanlışta yeniden gösterim |
| 13 | m17 | Uzaylı Apartmanı | Beş katlı bina, aşağıdan yukarı katlar, geniş kat hedefi ve paket teslim animasyonu |
| 14 | m18 | Dondurma Kulesi | Külah üzerinde aşağıdan yukarı 3/3/4 top, gerçek renkli toplar ve geniş yuvalar |
| 15 | m20 | Şampiyonlar Kürsüsü | Tüm blokları kapsayan geniş bırakma alanları, üç farklı yarış ve madalya/konfeti |
| 16 | m22 | Gökyüzü Asansörü | Cam kabin, kat göstergesi, yukarı-aşağı düğmeleri, 2/4/6. kat teslimleri |
| 17 | m23 | Obur Canavarın Tabakları | Konuşan canavar, rakamsız görünür çilek tabakları, daha çok/az/eşit turları |
| 18 | m24 | Adalet Terazisi | Gerçek iki kefe, görünür elmalar, sürükleyerek 5=5, 6=6 ve hazır 7=7 denge turları |
| 19 | m25 | İkiz Kardeşlerin Sepetleri | Yazılı etiket yerine meyve/piknik/oyuncak sepetlerinde yedişer gerçek görsel fark |
| 20 | m26 | Uzay Üssü Geri Sayımı | Rampa, büyük roket, sesli 10/15/20 geri sayımları ve dumanlı fırlatma animasyonu |
| 21 | m28 | Yeraltı Madencisi | Halat-ray-kabin görünümü, katla uyumlu azalan sayaç, 10→1, 15→5, 20→1 |
| 22 | m31 | Eriyen Kardan Adam | Azalan üç sayı örüntüsü, erime aşamaları ve doğru cevapta yeniden tamamlanma |
| 23 | m32 | Kavanozdaki Şekerler | Soru işareti yerine sürekli görünür 8/14/20 şeker, tahmin ve cezasız gerçek sonuç karşılaştırması |
| 24 | m33 | Örüntü Treni ve Eksik Vagon | Gerçek lokomotif/kancalı şekil gövdeli vagon, sürüklenen eksik vagon ve hareketli bitiş |
| 25 | m34 | Hızlı Tahminci Karınca | Tahminden önce görünür 3/5/7 yaprak, 5 ile karşılaştırma ve animasyonlu doğrulama |
| 26 | m35 | Cüce Adımı | Ad değişikliği; görünür oda sınırları, cüce ayak izi ve 6/9/12 adım ölçümleri |
| 27 | m36 | Kırtasiye Düzenleyici | Kalem/silgi/defter boyunca tek tek dizilen 8/3/6 ataş ve sesli sıra sayımı |
| 28 | m37 | Küçük İcatlar Pazarı | Gerçek hareketli terazi, elma/araba/kitap ve tek tek eklenen 8/5/10 bilye |
| 29 | m38 | Market Arabası Dedektifi | Görünür elma ekleme/çıkarma olayından artı-eksi ve sonuç seçimi |
| 30 | m39 | Okul Servisi Yolcuları | Binen/inen görünür öğrenciler, büyük artı-eksi düğmeleri ve iki aşamalı üçüncü tur |
| 31 | m41 | Şimşek Tahmincisi | Yazısız belirgin büyük-küçük taş, önce 10 ile tahmin sonra kesin sonuç aşaması |
| 32 | m42 | İksir Karıştırıcı | İki şişede sayılabilir damlalar, kazanda birleşme ve yalnız rakam cevapları |
| 33 | m43 | Hedefe Vuran Roket | Eksi diye seslendirme, sürüklenebilir roket/nişan ve sonuç gezegenine uçuş |
| 34 | m44 | Sihirli Terazi | Kefelerde rakam yerine 5/7/9 gerçek elma ve sepetteki elmaları sürükleyerek eşitleme |
| 35 | m45 | Matematiksel İkizler | Referans işlem, üç karışık işlem seçeneği ve gerçekten eşit sonuçlu ikizler |
| 36 | m46 | Balon Patlatmaca | Hareketli sayılı balonlar ve doğru balona fiziksel olarak sürüklenen çizgi-film iğnesi |
| 37 | m47 | Halat Çekme Turnuvası | İşlem sonucu kadar görünür takım üyesi, sol/eşit/sağ kararı ve halat sonucu |
| 38 | m48 | Sihirli Ayna | İki yüzlü ayna, sürüklenebilir sayı taşları ve eşit sayıda yıldız yansıması |
| 39 | m49 | İksir Laboratuvarı | İşlem sonuçlarıyla uyumlu iki büyük tüp seviyesi ve büyük EŞİT/EŞİT DEĞİL düğmeleri |
| 40 | m50 | Zaman Makinesi | Uzay temasız retro makine, ters işlem dişlisi ve gerçek top azaltma/geri sarma hikâyesi |

## Devam PDF’i — 11 oyun

| Sayfa | Kimlik | Oyun | Uygulanan ana düzeltme |
|---:|:---:|---|---|
| 3 | m51 | Kargo Robotunun Hatası | Kargo deposu, raf/bant/robot, fazla kutuları İADE arabasına sürükleme ve ters işlem |
| 4 | m52 | Asansör Düğmeleri | Katları görünür bina/kabin, hareketle uyumlu sayaç ve başlangıca döndüren işlem |
| 5 | m53 | Ankara Simitçisi ve Oyuncakçı | Ankara sokağı, görünür eğitim fiyatları, renk-boy farkı taşıyan stilize banknotlar |
| 6 | m54 | Sihirli Büyüteç | Su altı teması kaldırıldı; oda/mutfak/parkta adsız gerçek nesnelerden şekil avı |
| 7 | m55 | Akıllı Kasa Çekmecesi | Geniş gerçek çekmece bölmeleri ve stilize 5–200 TL banknot sınıflandırması |
| 8 | m56 | Tangram Sandviç Dükkanı | Tek kalıpta birleşen parçalar, dokunarak 90° döndürme ve kare/dikdörtgen üretimi |
| 9 | m57 | Geri Dönüşüm Fabrikası | Bütün robot/kamyon/roketten ayrılan parçaları yazısız şekil siluetlerine sınıflandırma |
| 10 | m58 | Gölge Avcıları | Kamp/fener sahnesi ve her nesneye özgü adsız siluet, boyut-yön-çıkıntı eşleştirmesi |
| 11 | m59 | Dondurmacının Büyük Sorusu | Müşteriye sorma, cevabı dinleme, resimli grafiğe kaydetme ve grafikten karar verme |
| 12 | m60 | Sınıf Başkanı Seçimi | Portreli adaylar/pusulalar, her oyda bir artan çetele ve kazanan/eşitlik kararı |
| 13 | m61 | Veterinerin Randevu Defteri | Sürekli görünür 8 kedi/3 köpek/5 kuş tablosu, üç veri sorusu ve görsel 8+5 desteği |

## Otomatik veri doğrulaması

- [x] Beklenen oyun kimliği: 49
- [x] Eksik oyun kimliği: 0
- [x] Toplam tur: 147
- [x] Üçten farklı tur içeren oyun: 0
- [x] Yerel Chrome etkileşim testi: 49/49 oyun, 147/147 tur
- [x] Telefon görünümü: 390×844 çözünürlükte 49 ilk tur ekranı görsel olarak tarandı
- [x] Görsel taramada bulunan dikey dondurma yuvası, gerçek kürsü yüksekliği, maden kat-konum eşliği, vagon dış sınırı, 10 katlı asansör ve randevu tablosu sorunları düzeltildi
