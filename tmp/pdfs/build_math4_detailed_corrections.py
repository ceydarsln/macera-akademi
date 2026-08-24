from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle


ROOT = Path("/Users/ceyda/Documents/New project")
OUT = ROOT / "output/pdf/4_sinif_matematik_oyunlari_detayli_duzeltmeler.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

PAGE_W, PAGE_H = A4
MX, TOP, BOTTOM = 17 * mm, 19 * mm, 16 * mm
INK = colors.HexColor("#262139")
PURPLE = colors.HexColor("#493B73")
TEAL = colors.HexColor("#168A8A")
CORAL = colors.HexColor("#E45F58")
GOLD = colors.HexColor("#E2A62D")
BLUE = colors.HexColor("#3E73A8")
PALE_PURPLE = colors.HexColor("#F2EEFA")
PALE_TEAL = colors.HexColor("#EAF7F5")
PALE_CORAL = colors.HexColor("#FFF0ED")
PALE_GOLD = colors.HexColor("#FFF7E4")
PALE_BLUE = colors.HexColor("#EDF4FA")
MID = colors.HexColor("#7A7687")

base = getSampleStyleSheet()["BodyText"]
body = ParagraphStyle("body", parent=base, fontName="Arial", fontSize=8.25, leading=10.6, textColor=INK, spaceAfter=1.0 * mm)
small = ParagraphStyle("small", parent=body, fontSize=7.45, leading=9.3, spaceAfter=0.65 * mm)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=4.7 * mm, firstLineIndent=-3.0 * mm, bulletIndent=0, spaceAfter=0.75 * mm)
bullet_small = ParagraphStyle("bullet_small", parent=small, leftIndent=4.7 * mm, firstLineIndent=-3.0 * mm, bulletIndent=0, spaceAfter=0.55 * mm)
h1 = ParagraphStyle("h1", parent=body, fontName="Arial-Bold", fontSize=21, leading=25, textColor=PURPLE, spaceAfter=4 * mm)
h2 = ParagraphStyle("h2", parent=body, fontName="Arial-Bold", fontSize=10.2, leading=12.2, textColor=TEAL, spaceBefore=1.1 * mm, spaceAfter=0.7 * mm)
cover_kicker = ParagraphStyle("cover_kicker", parent=body, fontName="Arial-Bold", fontSize=10, textColor=TEAL, alignment=TA_CENTER, spaceAfter=6 * mm)
cover_title = ParagraphStyle("cover_title", parent=body, fontName="Arial-Bold", fontSize=25, leading=30, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=5 * mm)
cover_sub = ParagraphStyle("cover_sub", parent=body, fontSize=12, leading=17, alignment=TA_CENTER, spaceAfter=9 * mm)
game_title = ParagraphStyle("game_title", parent=body, fontName="Arial", fontSize=13.4, leading=15.6, textColor=colors.white, spaceAfter=0)
badge = ParagraphStyle("badge", parent=body, fontName="Arial-Bold", fontSize=16, leading=17, textColor=colors.white, alignment=TA_CENTER, spaceAfter=0)
box_title = ParagraphStyle("box_title", parent=body, fontName="Arial-Bold", fontSize=9.2, leading=11.0, textColor=CORAL, spaceAfter=0.7 * mm)
round_head = ParagraphStyle("round_head", parent=small, fontName="Arial-Bold", fontSize=7.9, leading=9.1, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=0)
round_text = ParagraphStyle("round_text", parent=small, fontSize=7.0, leading=8.65, spaceAfter=0)
theme_title = ParagraphStyle("theme_title", parent=cover_title, fontSize=22, leading=27, textColor=colors.white)


def P(text, style=body):
    return Paragraph(text, style)


def bullets(items, style=bullet):
    return [Paragraph(item, style, bulletText="•") for item in items]


def header(number, title, subtitle, accent):
    table = Table([[P(str(number), badge), P(f"<b>{title}</b><br/><font size='8' color='#F1EEF8'>{subtitle}</font>", game_title)]],
                  colWidths=[15 * mm, 161 * mm], rowHeights=[19 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "CENTER"), ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("RIGHTPADDING", (1, 0), (1, 0), 8), ("ROUNDEDCORNERS", [8]),
    ]))
    return table


def box(title, items, bg, title_color, compact=False):
    title_style = ParagraphStyle("dynamic_box_title", parent=box_title, textColor=title_color)
    content = [P(title, title_style)] + bullets(items, bullet_small if compact else bullet)
    table = Table([[content]], colWidths=[176 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D7D3DF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROUNDEDCORNERS", [6]),
    ]))
    return table


def rounds_table(items):
    table = Table([[P("1. TUR", round_head), P("2. TUR", round_head), P("3. TUR", round_head)],
                   [P(items[0], round_text), P(items[1], round_text), P(items[2], round_text)]],
                  colWidths=[58.7 * mm, 58.7 * mm, 58.6 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALE_GOLD), ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFCF5")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDCFAB")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def footer(canv, doc):
    if canv.getPageNumber() == 1:
        return
    canv.saveState()
    canv.setStrokeColor(colors.HexColor("#D9D5E5"))
    canv.setLineWidth(0.6)
    canv.line(MX, PAGE_H - 12.5 * mm, PAGE_W - MX, PAGE_H - 12.5 * mm)
    canv.setFont("Arial", 7.4)
    canv.setFillColor(MID)
    canv.drawString(MX, 8.5 * mm, "4. Sınıf Matematik - Ayrıntılı Oyun Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 8.5 * mm, str(canv.getPageNumber()))
    canv.restoreState()


MOTOR = {
    "num": ("Yalnız son sayıyı tuşlamak, ara basamakları ve kullanılan stratejiyi görünmez bırakıyor.", "Yanlışta sonuç verilmeden ilgili basamak/model açılmalı; giriş silinip yeniden denenebilmelidir."),
    "belt": ("Kartın soldan kırpılarak gelmesi ve hareket etmesi, okuma hızını matematik başarısına karıştırıyor.", "Kart karar verilene kadar merkezde sabitlenmeli; yanlış kutuda kart korunup görsel gerekçe gösterilmelidir."),
    "match": ("Küçük ya da uzun kartları bir yuvaya taşımak ilişkiyi seçtiriyor, fakat ilişkinin neden doğru olduğunu kanıtlatmıyor.", "Doğruda iki temsil üst üste/yan yana gelerek eşliği göstermeli; yanlış kart başlangıç yerine dönmelidir."),
    "order": ("Roket çevresinde hareket eden kartlar ve yakıt hunisi oyun adındaki kule/süreç metaforuyla uyuşmuyor; kartlar ekran dışına taşabiliyor.", "Kartlar sabit bir sıra şeridinde yeniden düzenlenmeli; yanlış seçim sıralanan bölüm korunarak karşılaştırılmalıdır."),
    "slider": ("Tren-tünel sürgüsü konuya özgü modeli göstermiyor ve başlangıç seçimi kimi turda doğru cevabın üzerinde hazır geliyor.", "Sürgü her tur tarafsız konumda başlamalı; doğru değer konuya özgü model üzerinde kanıtlanmalıdır."),
    "path": ("Yapraklara zıplama motoru başlıktaki yapı/labirent bağlamını taşımıyor; rota çizgileri çeldiricileri de doğru yol gibi gösterebiliyor.", "Yol yalnız doğru seçimden sonra oluşmalı; yanlış düğümde önceki durum korunup işlem adımı gösterilmelidir."),
    "catch": ("Hareketli kapsülü yakalama, uzun soru metnini okuma ile eş zamanlı motor takip gerektiriyor.", "Seçenekler sabit kalmalı veya süre baskısı kapatılmalı; geri bildirim cevap etiketinden çok modeli açıklamalıdır."),
    "memory": ("Kapalı kartların konumunu hatırlama, uzun matematiksel ifadeyi anlama becerisinin önüne geçiyor.", "Eşleşme açıldığında iki kart birlikte okunmalı ve aralarındaki ilişki görünür bir modelle doğrulanmalıdır."),
    "serve": ("Tepsi/palet seçimi çoğunlukla soru metninde adı geçen etiketleri kopyalatıyor; ürün gerçekten oluşturulmuyor.", "Seçilen parçalar tepside kalmalı, birleştirilmeli ve yanlış seçim tek tek geri alınabilmelidir."),
    "hold": ("Basılı tutup hedef çizgisinde bırakma, ölçme ya da açı oluşturma yerine zamanlama hassasiyetini değerlendiriyor.", "Çocuk gerçek nesneyi sürükleyip ölçmeli; tolerans motor becerisini cezalandırmayacak biçimde ayarlanmalıdır."),
    "draw": ("Hazır nokta çiftlerine dokunmak çizme/ölçme eylemini daraltıyor; açılış sesi kimi turda keşfedilecek sonucu önceden söylüyor.", "Sonuç başlangıçta söylenmemeli; çizgi, köşe, uzunluk veya eksen çizim tamamlandıktan sonra sayılarak kanıtlanmalıdır."),
    "balance": ("Terazi görseli eşit değeri desteklese de sayısal ilişki hazır etiketlerden okunuyor; fiziksel ağırlık ile sayı değeri karışabiliyor.", "Kefelerdeki her birim açıkça sayılmalı ve eşitlik/çıkarma işlemi aynı ekranda sembolik olarak kurulmalıdır."),
    "mirror": ("Simetri görevi konuya uygundur; ancak renk seçme ve çok sayıda hücre dokunma sırasında geri alma gereklidir.", "Kaynak ve eş hücre eksene eş uzaklık kılavuzuyla gösterilmeli; silgi ve geri al bulunmalıdır."),
    "code": ("Izgara ve komutlar okunaklı olsa da görev geometrik yapı oluşturmak yerine yalnız engeller arasında yol bulmaya kayıyor.", "Komut çalışırken aktif blok parlamalı; rota korunmalı ve geometri hedefiyle bağlantı açıkça gösterilmelidir."),
    "tally": ("Hazır yanıtı doğru sütuna dokunarak işlemek temel çeteleyi gösteriyor, ancak çocuk veri üretmiyor ve işareti kendisi kurmuyor.", "Beşli çetele grubu görünür oluşmalı; geri alma ve toplam yanıt tutarlılığı sürekli denetlenmelidir."),
    "graph": ("Hazır sıklık sayısı kadar blok eklemek grafik kurmayı mekanik dokunma sayısına indiriyor.", "Eksen, ölçek ve birim anahtarı görünür olmalı; kaynak çetele ile grafik toplamı otomatik karşılaştırılmalıdır."),
}


def G(n, theme, title, sub, motor, obs, why, new, rounds, fb, qa):
    motor_risk, motor_fb = MOTOR[motor]
    return dict(n=n, theme=theme, title=title, sub=sub, observed=obs,
                risk=[motor_risk, why], new=new, rounds=rounds,
                feedback=[motor_fb] + fb,
                acceptance=[qa, "Üç turun her birinde metin, ses, görsel model ve kabul edilen sonuç birebir tutarlı olacak; kartlar kırpılmayacak ve en az 44 px dokunma alanı sunulacaktır."])


games = [
G(1,"Tema 1","Sayı Sarayı Kasası","Altı basamaklı sayıyı yaz","num",
  ["Koyu radar-kasa ekranı ve tuş takımı okunaklı; ilk görev 245 612 sayısını yazdırıyor.","Sorunun hemen altındaki açıklama 'binler bölüğü 245, birler bölüğü 612' diyerek sayının iki parçasını ve dolaylı olarak cevabın tamamını girişten önce veriyor."],
  "Çocuk basamakları ve bölükleri kendisi kurmadan ekrandaki iki grubu yan yana yazabilir; oyun sayı oluşturmayı değil kopyalamayı ölçer.",
  ["Kasa kapağına binler ve birler bölüğü için iki üçlü pencere yerleştirilsin.","Sayı adı sesli verilsin; rakam kartları karışık paletten ilgili basamaklara sürüklensin.","Her pencerenin altında yüz binler-binler ve yüzler-birler basamak adları açılıp sıfır içeren basamaklar da görünür kılınsın.","Tuş takımı yalnız son doğrulama için kullanılsın; cevap veren açıklama başlangıçta kaldırılıp isteğe bağlı katmanlı ipucu yapılsın."],
  ["245 612 sayı adıyla verilir; iki bölük ve altı basamak kurulur.","103 020'de sıfır bulunan on binler ve yüzler basamağı boş bırakılmaz.","500 000 ile 36 908 karşılaştırılır; eksik baştaki basamakların sayı değerini değiştirdiği konuşulur."],
  ["Yanlış rakamda yalnız ilgili basamak çerçevelensin; bütün sayı söylenmesin.","Doğruda iki bölük farklı renkte kapanıp sayı adı, rakamla yazılış ve çözümleme birlikte okunsun."],
  "İlk ekranda doğru sayı veya iki hazır üçlü grup görünmeyecek; sıfır içeren en az iki örnek çocuk tarafından bağımsız kurulacaktır."),
G(2,"Tema 1","Bölük Ayırma Bandı","Basamak hangi bölükte?","belt",
  ["Birler, binler bölüğü kutuları altta; sayı/rakam kartı banttan geliyor.","İlk kart ekranın sol kenarında ciddi biçimde kırpılıyor. Sekiz öğe aynı 245 612 sayısının basamak adları ve iki rakamıyla sınırlı."],
  "Kırpılma ve süre baskısı, bölük bilgisinden bağımsız hata üretir; tek sayı üzerinde tekrar genelleme sağlamaz.",
  ["Bant duraklı çalışsın ve sayı tablosu üstte kalıcı olsun.","Kartta hem vurgulanan rakam hem basamak adı gösterilsin; çocuk önce üçlü bölüğü çerçevelesin, sonra kutuya göndersin.","Her tur yeni altı basamaklı sayı üretilsin ve bölük ayırma çizgisi başlangıçta gizli olsun.","Son aşamada öğrenci sayıyı kendisi üçlü gruplara ayırıp bölük adlarını yazsın."],
  ["245 612'de 6 yüzler basamağında ve birler bölüğündedir.","103 020'de 3 binler basamağında, 0 onlar basamağında incelenir.","908 405 sayısı çocuk tarafından 908 | 405 biçiminde ayrılıp iki bölük adlandırılır."],
  ["Yanlış kutuda sayı tablosu açılıp kartın üçlü grubuna kadar bir kılavuz çizgi uzansın.","Doğruda kart doğru bölükteki gerçek basamak hücresine otursun."],
  "Kart karar verilene kadar tam görünür ve sabit olacak; en az üç farklı sayı ile iki bölük ve altı basamak dengeli test edilecektir."),
G(3,"Tema 1","Basamak Değeri Köprüsü","Rakamın değerini bul","match",
  ["Hedeflerde 200 000, 40 000, 5 000, 600 ve 10 değerleri okunabiliyor.","Alttaki 'yüz binler basamağındaki 2' gibi uzun kaynak kartları üst üste biniyor, kırpılıyor ve çoğu okunamıyor; 245 612'nin birler basamağındaki 2 hiç kullanılmıyor."],
  "Eksik basamak ve okunamayan kartlar tam basamak değeri yapısını bozuyor; çocuk yalnız görünen kısa kartları eşleyebilir.",
  ["Altı basamak yatay tabloya yerleştirilsin; her hücrede rakam, basamak adı ve değer için ayrı katman bulunsun.","Kaynak kartlar tek satırda sıkıştırılmasın; kaydırılabilir büyük kart paleti kullanılsın.","Kart hedefe geldiğinde 2 x 100 000 = 200 000 gibi çarpımsal ilişki çizilsin.","Birler basamağı dahil bütün altı basamak her turda yer alsın; sıfır değerli basamak özel olarak açıklansın."],
  ["245 612'nin altı rakamı altı değere eşleştirilir; birlik 2 de tamamlanır.","103 020'de 0 x 10 000 ve 0 x 100 değerleri görünür sıfır kartlarıyla kurulur.","670 405 için çocuk yalnız değeri verilen 70 000 ve 400 kartlarından ilgili rakam/basamağı çıkarır."],
  ["Yanlışta kartın rakamı ve hedef değerin kaç sıfır taşıdığı karşılaştırılsın.","Doğruda köprü bölümü basamak tablosundaki aynı renkle aydınlansın."],
  "Altı basamağın hiçbiri atlanmayacak; 320 px genişlikte bütün kart metinleri üst üste binmeden okunacaktır."),
G(4,"Tema 1","Sıralama Kulesi","Sayıları küçükten büyüğe sırala","order",
  ["Ekranda kule yerine roket ve yakıt hunisi var; beş sayı roket çevresinde hareket ediyor ve biri sol kenara taşabiliyor.","Yalnız 98 760, 99 999, 100 045, 103 020, 245 612 sabit dizisi kullanılıyor."],
  "Hareketli kartı doğru sırada yakalama, sayı karşılaştırma stratejisinden daha belirleyici olur; tek dizi ezberlenebilir.",
  ["Gerçek bir kulede her kat sabit bir sıra yuvası olsun; kartlar alt raftan sürüklenerek yerleştirilsin.","Karşılaştırmada önce basamak sayısı, sonra soldan ilk farklı basamak renklenerek gösterilsin.","Ara yerleştirme kabul edilsin; çocuk iki komşu kart arasına sayıyı koyabilsin.","Küçükten büyüğe ve büyükten küçüğe yönleri ayrı turlarda ok işaretiyle verilsin; roket/yakıt görseli kaldırılmalıdır."],
  ["98 760-245 612 küçükten büyüğe sıralanır.","600 500, 600 050, 605 000, 650 000 büyükten küçüğe sıralanır.","Beş kartlık sıralamaya 101 500 ara kartı doğru iki komşu arasına eklenir."],
  ["Yanlış komşulukta ilk farklı basamaklar yan yana büyütülsün.","Doğru dizide kule aşağıdan yukarıya sayıları seslendirerek tamamlanmalıdır."],
  "Kartlar hareket etmeyecek; en az üç farklı dizide yön değişecek ve başarı bütün komşu karşılaştırmalar doğru olduğunda verilecektir."),
G(5,"Tema 1","Yuvarlama Treni","En yakın onluk/yüzlük/binlik","slider",
  ["Tren ve tüneller başlıkla uyumlu; 3478 sayısı için değer seçiliyor.","Sürgü başlangıçta 4000 gibi bir hedefe hazır gelebiliyor; tüneller yalnız aday değerleri gösteriyor, sayı doğrusundaki gerçek uzaklıklar görünmüyor."],
  "Doğruya hazır seçim onay düğmesini ödüllendirir; uzaklık görülmeden yuvarlama yalnız ezber kuralına dönüşür.",
  ["Ray gerçek sayı doğrusu olsun ve komşu onluk/yüzlük/binlik noktalar arası eş ölçekle çizilsin.","3478'in alt ve üst sınırına uzaklıkları ray parçalarıyla saydırılsın.","Sürgü her tur ortadaki cevaptan bağımsız rastgele güvenli konumda başlasın.","Onluk, yüzlük ve binlik turları farklı renkli basamak penceresiyle ayrılmalı; sınırdaki 5 örneği ayrıca ele alınmalıdır."],
  ["3478 en yakın binliğe 3000; 478 ve 522 uzaklıkları karşılaştırılır.","3478 en yakın yüzlüğe 3500, en yakın onluğa 3480 olur.","6500 en yakın binlikte 7000'e gider; yarım durumda kullanılan kural açıklanır."],
  ["Yanlış tünelde tren durup iki komşu hedefe uzaklıkları gösterilsin.","Doğruda yuvarlanan basamak ve sağındaki basamaklar sayı üzerinde renklenmelidir."],
  "Sürgü hiçbir turda doğru cevaba hazır açılmayacak; sayı doğrusu aralıkları sayısal farklarla orantılı olacaktır."),
G(6,"Tema 1","Gökdelen Asansörü","Yüzer ve biner ileri-geri sayma","path",
  ["Gökdelen/asansör yerine yeşil yapraklar ve kurbağa benzeri zıplama rotası kullanılıyor.","Kaynak yalnız 1000'den 1500'e yüzerek ileri saymayı içeriyor; kazanımdaki biner ve geri sayma örneklenmiyor."],
  "Başlık-sahne uyumsuzluğu yanında tek yön/tek artış, ritmik sayma kuralının genellenmesini engeller.",
  ["Dikey gökdelen cephesi ve gerçek asansör kabini çizilsin; kat etiketleri sayı doğrusuna göre yükselsin.","Çocuk +100, -100, +1000, -1000 komutlarından uygun olanı seçsin ve kabin hareketi işlem oku göstersin.","Çeldirici katlar rota çizgisiyle bağlanmasın; yalnız seçilen hareketten sonra kablo/ışık oluşsun.","Başlangıç ve hedef kat her tur değişsin; sıfırlı sayılar düzgün seslendirilsin."],
  ["1000-1500 arası +100 ile çıkılır.","2800'den 2300'e -100 ile inilir.","3500, 4500, 5500, 6500 dizisinde +1000; ardından 6500'den 4500'e geri sayılır."],
  ["Yanlış katta kabin hareket etmeden beklesin ve seçilen komutun oluşturacağı sayı yazılsın.","Doğruda önceki kat, işlem oku ve yeni kat aynı anda gösterilsin."],
  "Yüzlük ve binlik adımlar ile ileri/geri yönlerin dördü de ayrı görevlerde tamamlanacaktır."),
G(7,"Tema 1","Örüntü Radarı","Eksik terimi ve kuralı bul","catch",
  ["Uzay radarı ve düşen sayı kapsülü kullanılıyor; uzun sayı dizisi üstte metin/sesle veriliyor.","Dört tur +5, -9, x2 ve -100 kurallarını kapsıyor; ancak dizinin tamamı kalıcı bir şerit olarak görünmediğinden öğrenci hareketli cevabı izlerken örüntüyü kaybedebiliyor."],
  "Örüntüyü temsil ve gerekçelendirme yerine hızlı sonuç yakalama ölçülür; toplamsal ve çarpımsal kurallar aynı görünümde ayrışmaz.",
  ["Radar ekranında dizinin bütün terimleri sabit yörünge noktalarında kalsın; eksik yer boş halka olsun.","Öğrenci önce iki ardışık farkı/oranı işaretleyip kural kartını seçsin, sonra eksik terimi yerleştirsin.","Cevap kapsülleri hareket etmeyecek; isteğe bağlı süreli mod yalnız temel tur tamamlandıktan sonra açılacak.","Artan, azalan ve çarpımsal örüntüler renkli oklarla birbirinden ayrılmalı."],
  ["7, 12, 17, ?, 27 için +5 ve 22 bulunur.","54, 45, 36, ?, 18 için -9 ve 27 bulunur.","6, 12, 24, ?, 96 için x2; 900, 800, ?, 600 için -100 karşılaştırılır."],
  ["Yanlışta iki komşu terim arasındaki fark/oran çizilsin; cevap söylenmesin.","Doğruda aynı kuralın bütün aralıklarda çalıştığı tarama animasyonuyla doğrulanmalıdır."],
  "Öğrenci her turda hem kuralı hem eksik terimi seçmeden başarı alamayacak; dizi karar süresince görünür kalacaktır."),
G(8,"Tema 1","Okunuş Eşleştirme","Sayıyı okunuşuyla eşleştir","memory",
  ["On iki kapalı kart 3 x 4 düzeninde; altı sayı-altı okunuş çifti bulunuyor.","Uzun altı basamaklı sayı adları kart açıldığında dar karta sığmak zorunda ve tur her açılışta aynı sabit çiftlerden oluşuyor."],
  "Başarı sayı okumaktan çok kart konumunu hatırlamaya dayanabilir; taşan metin okunabilirliği azaltır.",
  ["İlk düzeyde sayı ve okunuş kartları aynı anda açık iki sütunda eşleştirilsin.","Okunuş kartları genişleyebilir veya iki satır standart yüksekliğe sahip olsun; kelimeler bölük renkleriyle ayrılmalıdır.","İkinci düzeyde sınırlı sayıda kapalı kart kullanılabilir; her eşleşmede sayı bölüklere ayrılarak seslendirilsin.","Sayı havuzu her oyunda değişsin ve sıfır içeren basamaklar özellikle kapsansın."],
  ["245 612 ile 'iki yüz kırk beş bin altı yüz on iki' eşleştirilir.","103 020'de okunmayan sıfır basamakları tablo üzerinde gösterilir.","36 908 ve 500 000 dinleme turunda ses duyulup doğru rakamla yazılı sayı seçilir."],
  ["Yanlış çift açıldığında sayı bölük çizgisiyle ayrılıp okunuştaki eksik/fazla bölüm vurgulansın.","Doğruda çift sabit kalıp sesli okunsun; sırf konum hatası can kaybettirmesin."],
  "Uzun sayı adları 320 px ekranda eksiksiz görünür olacak; en az yarı turlarda kartlar başlangıçtan açık olup okuma doğrudan ölçülecektir."),

G(9,"Tema 2","Kesir Tasnif Bandı","Basit, bileşik ve tam sayılı kesir","belt",
  ["Üç kutu açıkça etiketli; kesir kartı banttan solda kırpılarak geliyor.","Sekiz örnek yalnız sembolik yazımdan sınıflandırılıyor; parça-bütün modeli yok ve yönerge sınıflama kuralını hazır veriyor."],
  "Öğrenci pay-payda işaretine bakarak kutu seçebilir; bileşik kesrin bir bütünü aşıp aşmadığını görmez.",
  ["Her kartın yanında aynı kesri gösteren kesir şeridi veya daire modeli bulunsun.","Öğrenci önce modelde kaç bütün ve kaç parça olduğunu işaretlesin, sonra sınıf kutusunu seçsin.","Tam sayılı ve bileşik gösterimler aynı miktar üzerinde dönüştürülebilsin.","Kart sabit dursun; sınıf adları tanım + örnekle açılabilir yardım panelinde yer alsın."],
  ["3/5 bir bütünden küçük modelle basit kesirdir.","7/5 = 1 tam 2/5 modeliyle bileşik kesir olarak sınıflanır.","2 tam 1/4 hem tam sayılı yazılır hem 9/4'e dönüştürülür."],
  ["Yanlışta pay ve payda sayıları yerine modelde tamamlanan bütün sayısı gösterilsin.","Doğruda sembol, model ve sınıf adı birlikte kalsın."],
  "Basit-bileşik-tam sayılı türlerin her biri en az üç örnekle ve mutlaka görsel modelle test edilecektir."),
G(10,"Tema 2","Pastane Siparişi","Bileşik kesri parçalarla kur","serve",
  ["Çeyrek pasta parçaları ve tepsi başlıkla uyumlu; ilk sipariş '4/4 = 1 bütün' ifadesini açıkça yazıyor.","5/4 ve 7/4 siparişlerinde fiş, kaç bütün ve kaç çeyrek gerektiğini de doğrudan söylüyor; çocuk yalnız etiketi kopyalıyor."],
  "Bileşik kesri bütüne ayırma stratejisi kurulmadan hazır çözüm servis edilir.",
  ["Fişte yalnız 5/4 gibi sembol veya görsel sipariş bulunsun; çözüm cümlesi gizlensin.","Çeyrek parçalar gerçek yuvarlak pastalarda birleşsin; dört parça dolunca yeni bütün tepsisi açılsın.","Aynı miktar 1 tam 1/4 olarak ikinci etikete dönüştürülsün ve çocuk eşitlik işaretini kurabilsin.","Parça paleti sonraki turda yarım/çeyrek karışık olsun; eşdeğer bileşimler kabul edilsin."],
  ["4/4 bir tam pasta olarak kurulur.","5/4 dört çeyrek + bir çeyrek olarak 1 tam 1/4'e dönüştürülür.","7/4 hem yedi çeyrekle hem 1 tam + 3/4 ile hazırlanır; iki sunum karşılaştırılır."],
  ["Eksik/fazla parçada tepsideki boşluk veya taşan bölüm görünür kalsın.","Doğruda dört çeyreğin bir bütüne birleşme animasyonu matematiksel kanıt olmalıdır."],
  "Sipariş metni çözümü önceden yazmayacak; en az iki bileşik kesir iki eşdeğer sunumla kurulacaktır."),
G(11,"Tema 2","Denk Kesir Köprüsü","Eşit değerdeki kesirler","match",
  ["Beş hedef kesir ve altta beş kaynak kesir okunaklı; kaynaklarda küçük yiyecek emojileri matematiksel olmayan süs olarak duruyor.","1/2-2/4, 1/3-2/6 gibi sabit eşleşmeler var; kesir alanı/şeridi eşitliği gösterilmiyor."],
  "Çocuk denkliği yalnız sayı örüntüsü olarak ezberleyebilir; neden aynı miktarı gösterdikleri kanıtlanmaz.",
  ["Her kart kesir şeridiyle çizilsin ve eşleşen şeritler aynı uzunlukta üst üste gelsin.","Pay ve paydanın aynı sayıyla genişletilmesi hücrelerin bölünme animasyonuyla gösterilsin.","Sadece iki katı değil, üç katı ve sadeleştirme örnekleri eklensin.","Yiyecek emojisi yerine tutarlı şerit/daire modeli kullanılsın; öğrenci sembol-model arasında geçiş yapsın."],
  ["1/2 = 2/4 şerit bölünerek kanıtlanır.","1/3 = 2/6 ve 3/4 = 6/8 üst üste karşılaştırılır.","6/10 sadeleştirilerek 3/5 bulunur; çocuk ortak çarpanı seçer."],
  ["Yanlışta iki şerit aynı başlangıç çizgisinde karşılaştırılsın ve uç farkı gösterilsin.","Doğruda genişletme/sadeleştirme katsayısı pay ve paydaya ayrı oklarla yazılsın."],
  "Her eşleşme yalnız sayısal kontrolle değil eş uzunlukta görsel modelle doğrulanacaktır."),
G(12,"Tema 2","Birim Kesir Kulesi","Birim kesirleri sırala","order",
  ["Roket/yakıt sahnesinde 1/2, 1/3, 1/4, 1/8 gibi kartlar hareket ediyor; bir kart ekran dışında kalabiliyor.","Beş sabit birim kesir büyükten küçüğe seçiliyor; parça boyutları görünmüyor."],
  "Paydası büyük olanın neden daha küçük olduğu anlaşılmadan kart adı ezberlenebilir; hareketli hedef erişimi bozar.",
  ["Aynı boydaki beş bütün, sırasıyla 2-3-4-6-8 eş parçaya bölünsün.","Çocuk her modelden tek parçayı çıkarıp dikey kule raflarına boyuna göre yerleştirsin.","Kart ve parça sabit dursun; payda sayısı arttıkça birim parçanın küçülmesi katmanlı animasyonla gösterilsin.","Büyükten küçüğe ve küçükten büyüğe sıralamalar ayrı turlarda yapılmalıdır."],
  ["1/2, 1/3, 1/4, 1/6, 1/8 büyükten küçüğe sıralanır.","1/10, 1/5, 1/4, 1/2 küçükten büyüğe sıralanır.","Bir model etiketsiz verilir; çocuk parça sayısından birim kesri adlandırıp doğru araya koyar."],
  ["Yanlış komşulukta iki bütün aynı boyda üst üste getirilip tek parçalar karşılaştırılsın.","Doğru kulede parçalar gerçek büyüklük sırasına göre hizalansın."],
  "Kartların tamamı ekranda sabit görünecek; sıralama her tur aynı boydaki bütün modelleriyle doğrulanacaktır."),
G(13,"Tema 2","En Büyük Kesir Radarı","Kesirleri karşılaştır","catch",
  ["Kesir seçenekleri düşen kapsüller; öğrenci radarı sürükleyerek en büyük ya da son turda en küçük kesri yakalıyor.","Soru üstte kalırken seçenekler tek tek hareket ediyor; kesir modelleri yok ve 'en büyük/en küçük' yönü tur içinde değişebiliyor."],
  "Motor takibi ve yönerge yönünü hatırlama, kesir karşılaştırma bilgisini gölgeleyebilir.",
  ["Dört kesir sabit radar halkalarında aynı anda dursun.","Eş payda turunda paylar; birim kesir turunda paydalar karşılaştırılırken kesir şeritleri açılabilsin.","Görev yönü büyük ok ve renkli başlıkla sürekli görünür olsun; tur ortasında gizlice değişmesin.","Son turda farklı payda için ortak model veya denk kesir stratejisi kullanılmalı; yalnız sezgisel seçim yapılmamalıdır."],
  ["3/8, 5/8, 7/8, 2/8 içinde 7/8 seçilir.","1/2, 1/4, 1/6, 1/8 içinde en büyük 1/2 bulunur.","2/3 ile 3/4 ortak 12'lik şeritlerde karşılaştırılır; 3/4 büyüktür."],
  ["Yanlışta ilgili kesir şeritleri aynı bütün üzerinde gösterilsin.","Doğruda karşılaştırma işareti çocuk tarafından yerleştirilip sesli okunsun."],
  "Hareketli yakalama zorunluluğu kaldırılacak; en büyük/en küçük yönü bütün tur boyunca görünür kalacaktır."),
G(14,"Tema 2","Kesir Hesap Makinesi","Paydaları eşit kesirlerle işlem","num",
  ["Tuş takımı yalnız payı girdiriyor; 2/7 + 3/7 için ekranda '2 + 3 = ?' ara işlemi hazır yazılı.","Dört tur sembolik toplama/çıkarma kullanıyor; yedi eş parçalı bütün görünmüyor."],
  "Paydaların neden aynı kaldığı anlaşılmadan yalnız tam sayı payları toplanıp çıkarılabilir.",
  ["Her işlemde aynı büyüklükte kesir şeridi/daire iki renkle gösterilsin.","Çocuk boyalı parçaları birleştirsin veya çıkarsın; payı modelden sayıp en son tuşlasın.","Payda alanı kilitli kalırken 'bütün kaç eş parçaya bölünmüş?' sorusu cevaplandırılsın.","Son turda sonuç bileşik kesirse tam sayılı kesre dönüşüm yapılmalıdır."],
  ["2/7 + 3/7 = 5/7 modelle kurulur.","6/8 - 2/8 = 4/8 ve 1/2 denkliği görülür.","5/4 + 2/4 = 7/4 = 1 tam 3/4 olarak tamamlanır."],
  ["Yanlış payda değişiminde bütünün bölme çizgileri korunup neden paydanın sabit olduğu açıklansın.","Doğruda boyalı parça sayısı, sembolik işlem ve sonuç aynı renkte eşleşsin."],
  "Her turda sonuç tuşlanmadan önce görsel model tamamlanacak; ipucu cevabı oluşturan tam işlemi başlangıçta vermeyecektir."),
G(15,"Tema 2","Çokluk Ölçeri","Bir çokluğun kesir kadarını bul","slider",
  ["24 elmanın 3/4'ü tren tünelleri ve sürgüyle 0-6-12-18-24 seçeneklerinden seçiliyor; seçili değer 12'de hazır açılıyor.","Sepet ve 24 elma görünmüyor; kesir kadarını bulma gruplama yerine tünel seçimine dönüşüyor."],
  "Çocuk 24'ü dört eş gruba ayırmadan seçenek deneyebilir; tren bağlamı çokluk modelini desteklemez.",
  ["Gerçek sepet ve 24 sayılabilir elma çizilsin; dört eş kasaya sürükle-bırakla paylaştırılsın.","Bir grubun 6 olduğu görüldükten sonra üç grup seçilerek 18 elde edilsin.","İkinci turda onluk çerçeve, üçüncü turda ters problem için boş grup sayısı kullanılsın.","Sürgü varsa yalnız son tahmin için kullanılmalı ve tarafsız başlamalı; tren sahnesi kaldırılmalıdır."],
  ["24'ün 3/4'ü dört eş gruptan üçü seçilerek 18 bulunur.","20'nin 2/5'i beş eş gruptan ikisiyle 8 olur.","Bir çokluğun 3/4'ü 9 ise bir grup 3, bütün 12 olarak tersine kurulur."],
  ["Eş olmayan grupta elmalar dağıtım alanında kalıp grup sayıları karşılaştırılsın.","Doğruda seçilen grup sayısı x her gruptaki nesne eşitliği yazılsın."],
  "Her turda bütün çokluk ve eş gruplar ekrandan sayılabilir olacak; yalnız doğru sayı tüneli seçmek başarı sayılmayacaktır."),
G(16,"Tema 2","Birim Dönüşüm Kartları","Uzunluk ve kütle dönüşümleri","memory",
  ["12 kapalı kartta cm-mm, m-cm, km-m, kg-g, ton-kg çiftleri bulunuyor.","Uzunluk ve kütle aileleri aynı destede karışık; açıklamadaki 'her adımda 10 ya da 1000 kat' cümlesi m-cm için 100 katsayısını dışlıyor."],
  "Yanlış genelleme ve konum hafızası, birim ölçeğini anlamanın önüne geçebilir.",
  ["Önce uzunluk ve kütle için iki ayrı merdiven/ölçek kurulsun.","Her geçiş oku kendi çarpanını göstersin: cm-mm x10, m-cm x100, km-m x1000; kg-g ve ton-kg x1000.","Kart eşleştirme açık iki sütunda yapılmalı; sonra isteğe bağlı hafıza düzeyi açılmalıdır.","Her eşleşme cetvel, metre şeridi veya kütle paketiyle gerçek büyüklük ilişkisine bağlanmalıdır."],
  ["1 cm = 10 mm ve 5 cm = 50 mm cetvel üzerinde gösterilir.","1 m = 100 cm, 1 km = 1000 m uzunluk merdiveninde dönüştürülür.","1 kg = 1000 g ve 1 ton = 1000 kg ayrı kütle ölçeğinde tamamlanır."],
  ["Yanlışta iki birimin aynı büyüklük ailesinde olup olmadığı sorulsun.","Doğruda dönüşüm oku ve kullanılan katsayı kartların arasında kalmalıdır."],
  "İpucu 10, 100 ve 1000 katsayılarının üçünü de doğru geçişte kullanacak; uzunluk ve kütle aileleri görsel olarak ayrılacaktır."),

G(17,"Tema 3","Zihin Radarı","Sayıyı parçalayarak hesapla","catch",
  ["47 + 38 gibi işlem sesle sorulurken sonuç kapsülleri hareket ediyor; parçalama adımları küçük metin olarak üst alanda kalıyor.","Dört turda strateji ifadeleri cevaba çok yaklaşıyor; yanlış ipucu 70 + 15 = 85 sonucunu doğrudan veriyor."],
  "Zihinden strateji seçimi yerine hareketli doğru sayıyı yakalama ve yazılı ara işlemi takip etme ölçülür.",
  ["Sayılar onluk ve birlik kartlarına ayrılabilir sabit çalışma masasında gösterilsin.","Öğrenci 47'yi 40+7, 38'i 30+8 olarak kendisi parçalasın; alternatif telafi stratejisi de kabul edilsin.","Sonuç seçenekleri sabit olsun ve ara işlem yalnız çocuk parçaları yerleştirdikçe oluşsun.","Aynı işlem iki stratejiyle çözüldüğünde sonuçların eş olduğu karşılaştırılsın."],
  ["47+38 onluk/birlik parçalama ile 85 olur.","63-27 önce 20 sonra 7 çıkarılarak 36 bulunur.","250+190 telafiyle 250+200-10; 500-240 yüzlük/onluk parçalamayla çözülür."],
  ["Yanlışta sonucun tamamı değil, yanlış parçalanan adım vurgulansın.","Doğruda öğrenci kullandığı stratejiyi adlandırıp işlem zincirini sesli görebilsin."],
  "Öğrenci ara parçaları kendisi oluşturmadan cevap seçilemeyecek; hareketli hedef zorunluluğu olmayacaktır."),
G(18,"Tema 3","Dört Basamak Kasası","Toplama ve çıkarma algoritması","num",
  ["3456 + 2178 gibi işlemler ve büyük tuş takımı okunaklı; yalnız son dört basamaklı sonuç giriliyor.","Elde ve onluk bozma metinle hatırlatılıyor fakat dikey basamak tablosu, elde rakamları ve bozulan onluklar görünmüyor."],
  "Algoritmanın yapılandırılması yerine hesap sonucu ölçülür; yanlış basamağın nerede oluştuğu anlaşılamaz.",
  ["İşlemler birler basamakları hizalı dikey tabloya yerleştirilsin.","Çocuk her sütunun sonucunu sırayla girsin; elde/bozma parçaları üst hücreye sürüklensin.","Sıfırlı çıkarma örneğinde binlikten birliğe kadar bozma zinciri somut taban bloklarıyla gösterilsin.","Kısa yol turu standart algoritmadan ayrı olarak seçilebilir strateji panelinde verilsin."],
  ["3456+2178 elde hücreleriyle 5634 olur.","7204-3856'da ardışık onluk bozma ile 3348 bulunur.","1999+2001 telafi stratejisiyle 4000; 5000-1234 blok değişimiyle 3766 olur."],
  ["Yanlışta yalnız hatalı sütun açılıp o sütundaki nesne değişimi gösterilsin.","Doğruda bütün sütunlar aşağıdan yukarı kontrol edilip sonuç bir kez okunmalıdır."],
  "Sonuç tek girişle kabul edilmeyecek; her turda basamak hizası, elde/bozma ve son sonuç ayrı ayrı doğrulanacaktır."),
G(19,"Tema 3","Tahmin Terazisi","Çarpma ve bölmede tahmin","slider",
  ["Başlık terazi olsa da tren-tünel sürgüsü açılıyor; 48 x 21 için 48≈50, 21≈20 ve 50x20=? metni baştan gösteriliyor.","Sürgü ilk turda doğru 1000 seçeneğinde hazır görünebiliyor; çocuk yuvarlamayı yapmadan onaylayabilir."],
  "Tahmin stratejisi ve makullük yargısı yerine hazır dönüşümün son işlemi ile varsayılan konum onaylanır.",
  ["İki sayı ayrı sayı doğrularında öğrenci tarafından uygun dost sayıya yuvarlansın.","Tahmin bağımsız kaydedilsin; gerçek sonuç daha sonra hesaplanıp aynı ölçek üzerinde gösterilsin.","Tahmin-gerçek farkı ve yakınlık yorumu çocuk tarafından seçilsin.","Terazi kullanılacaksa tahmin ve gerçek sonuç iki kefede sayısal uzaklıkla dengelensin; tren görseli kaldırılmalıdır."],
  ["48x21 için 50x20=1000, gerçek 1008, fark 8.","312÷4 için 320÷4=80, gerçek 78; bölünebilir yakın sayı seçilir.","29x31 yaklaşık 30x30=900; 596÷6 yaklaşık 600÷6=100 karşılaştırılır."],
  ["Yanlışta en yakın dost sayı seçenekleri sayı doğrusunda gösterilsin; doğru dönüşüm doğrudan verilmesin.","Doğruda tahmin, gerçek sonuç ve fark aynı kartta kalsın."],
  "Başlangıç sürgüsü hiçbir hedefte doğruya hazır gelmeyecek; her turda öğrenci yuvarlanan sayıları ve makullük yorumunu kendisi seçecektir."),
G(20,"Tema 3","Kısa Yol Bandı","10 ve 100 ile çarpma-bölme","belt",
  ["Dört işlem kutusu altta çok dar; etiketler ve sıfır simgeleri küçük/üst üste görünüyor.","İşlem kartı soldan kırpılıyor. 'Sıfır ekle/sil' kuralı yalnız sonunda sıfır bulunan doğal sayılarla sunuluyor."],
  "Kural mekanik sıfır manipülasyonuna indirgenir ve basamak değerinin neden değiştiği anlaşılmaz.",
  ["Her sayı basamak tablosunda sağa/sola kaydırılarak x10, x100, ÷10, ÷100 ilişkisi gösterilsin.","Kutular iki aşamada önce işlem yönü, sonra 10/100 olacak biçimde büyük dokunma alanlarına bölünsün.","Kartlar sabit ve tam görünür olsun; sonuç çocuk tarafından tahmin edilip tabloyla doğrulansın.","'Sıfır ekle/sil' tek kural olarak değil, doğal sayılarda basamak kaymasının görünür sonucu olarak ifade edilsin."],
  ["35x10=350 ve 35x100=3500 basamak kaymasıyla kurulur.","4200÷100=42 ve 830÷10=83 tabloda sola kaydırılır.","700÷10 ve 9000÷100 için sıfırların yalnız silinmediği, basamak değerinin değiştiği açıklanır."],
  ["Yanlışta sayının her rakamının önceki ve yeni basamak değerini gösteren oklar açılsın.","Doğruda işlem, tablo hareketi ve sonuç eş zamanlı okunmalıdır."],
  "Dört işlem türü dengeli örneklenecek; kutu metinleri 320 px'de taşmadan okunacak ve kartlar hareket etmeyecektir."),
G(21,"Tema 3","Robot Paketleme Bandı","Çarpma-bölme tersliği","match",
  ["Altı kutunun her birine yedi robot yerleştirmek için kutulara sırayla dokunuluyor; toplam 42 ayrı dokunuş gerekebiliyor.","Tek sabit 6x7 örneği var; çarpma-bölme ilişkisi ancak işlem bittikten sonra 'sağlama' düğmesiyle açılıyor."],
  "Yüksek dokunma yükü motor dayanıklılığı ölçer; tek örnek ters işlemin genellenmesine yetmez.",
  ["Robotlar tek tek değil 7'li paket kartları hâlinde altı kutuya sürüklensin; isteyen çocuk paketi açıp sayabilsin.","6 grup x 7, 42 robot ve 42÷6/42÷7 eşitlikleri aynı dizi modeli üzerinde kurulsun.","Bir turda grup sayısı, bir turda grup büyüklüğü, bir turda toplam bilinmeyen olsun.","En fazla 8 anlamlı dokunma ile tamamlanacak erişilebilir etkileşim tasarlansın."],
  ["6 kutu, her kutuda 7: 42; 42÷6=7 ve 42÷7=6.","5 paket, her pakette 8: 40 ve iki ters bölme işlemi.","Toplam 36 robot, 6'şarlı paketler: kutu sayısı 6 olarak bulunur."],
  ["Yanlışta gruplar bozulmadan eksik/fazla paket çerçevelensin.","Doğruda aynı nesne dizisi üzerinde dört sayı ailesi birlikte gösterilsin."],
  "Tek tur 12'den fazla dokunma istemeyecek; en az üç farklı sayı ailesi çarpma ve iki bölme işlemiyle tamamlanacaktır."),
G(22,"Tema 3","Yönerge Labirenti","Dört işlem yönergesini uygula","path",
  ["Robot, yeşil yaprak kapılar ve zikzak rota var; gerçek bir labirent duvarı/karar alanı yok.","12x4, +8, ÷7, +7 zinciri tek sabit rotadır; her adımda doğru işlem doğrudan yazılıyor."],
  "Çocuk yönerge üretmek veya yorumlamak yerine yazılı işlemin sonucuna sahip kapıyı buluyor; tek zincir ezberlenebilir.",
  ["Dallanabilen gerçek labirentte her kapıda işlem komutu ve sonuç ön izlemesi ayrı olsun.","Öğrenci yönerge kartlarını sıraya koyduktan sonra robot çalışsın; ara sonuçlar not defterinde kalsın.","İkinci turda eksik komut, üçüncü turda hedefe götüren yönergeyi çocuk yazsın.","Yanlış seçim yalnız o adıma geri dönsün; tamamlanan zincir silinmesin."],
  ["12x4=48, +8=56, ÷7=8, +7=15 zinciri uygulanır.","20'den 5'e ulaşan iki adımlı yönergede eksik ÷4 komutu bulunur.","10'dan 42'ye götüren üç adımlı bir yönerge çocuk tarafından seçeneklerden oluşturulur."],
  ["Yanlış kapıda önceki ara sonuç ve seçilen işlemin gerçek sonucu karşılaştırılsın.","Doğruda bütün komut zinciri tek satırda yeniden oynatılmalıdır."],
  "En az bir turda yönerge öğrenci tarafından oluşturulacak; tek önceden belirlenmiş rota oyunun tamamı olmayacaktır."),
G(23,"Tema 3","Problem Kurma Masası","Verilerle problem oluştur","serve",
  ["5 kutu, her kutuda 12, 8 kırık, soru ve '(5x12)-8' çözüm kartları tepside hazır.","Problem kurma başlığına rağmen çocuk cümle yazmıyor; hazır çözüm kartı nihai işlemi açıkça veriyor ve yalnız gereken etiketleri seçiyor."],
  "Problem yapılandırma ve dil üretimi yerine kart ayıklama ölçülür; çözüm önceden gösterildiği için muhakeme azalır.",
  ["Karakter, nesne, sayı, olay ve soru kökü kartlarıyla sürüklenebilir cümle şeridi oluşturulsun.","Çözüm kartı başlangıçta kaldırılıp problem kurulduktan sonra çocuk tarafından işlem olarak seçilsin.","Gereksiz bilgi turunda bilgi kartlarının çözümü değiştirip değiştirmediği ayrı kontrol sorusuyla sorgulansın.","Aynı verilerle toplama, çarpma veya iki işlemli farklı soru cümleleri kurulabilsin."],
  ["5 kutuda 12 kalem: toplam kaç kalem? tek çarpma problemi.","8 kırık eklendiğinde sağlam kaç kalem kaldı? iki işlemli problem.","Kutuların rengi gibi gereksiz bilgi ayrılır; çocuk aynı verilerle yeni geçerli problem kurar."],
  ["Dilbilgisel eksikte şerit üzerindeki eksik rol (veri/olay/soru) belirtilsin; çözüm verilmesin.","Doğruda kurulan problem sesli okunup işlemle veri arasında bağ çizilsin."],
  "Öğrenci en az bir turda kendi soru cümlesini kuracak; çözüm işlemi problem tamamlanmadan görünmeyecektir."),
G(24,"Tema 3","Eşitlik Terazisi","Eşitliğin iki tarafı","balance",
  ["12x4 sol kefede 48 değeriyle hazır; sağda 6x8, 96÷2, 50-2 gibi birden fazla doğru seçenek ve iki çeldirici var.","Terazi tek bir kart dokununca dengeleniyor; eşitliğin dönüşümleri veya bilinmeyen değer oluşturma yok."],
  "Çocuk eşitliği iki tarafı yapılandırmak yerine hazır 48 sonuçlarını tanıyabilir; fiziksel ağırlık metaforu soyut işlemi yüzeysel bırakır.",
  ["Sol ve sağ kefeler ayrı işlem bloklarından kurulabilsin; her adımda kefe değeri sayılabilsin.","Birden fazla doğru eşitlik kabul edilsin ve çocuk iki farklı çözüm üretmeye teşvik edilsin.","Eşitliğin iki tarafına aynı sayıyı ekleme/çıkarma dönüşümü görsel olarak uygulansın.","Bilinmeyen kutulu eşitliklerde eksik değer bloklarla bulunmalıdır."],
  ["12x4 = 6x8, 96÷2 ve 50-2 üç farklı biçimde kurulur.","72 = 80-8 = 36+36 eşitlik zinciri oluşturulur.","25x4 = ? + 35 ve 100-20 = 8x? gibi bilinmeyenler bulunur."],
  ["Yanlışta iki tarafın sayısal değerleri gösterilip fark kadar birim çerçevelensin.","Doğruda '=' işareti iki taraf arasında parlayıp eşitlik iki yönlü okunmalıdır."],
  "Her turda en az iki doğru eşdeğer ifade kabul edilecek; bir bilinmeyen ve bir eşit dönüşüm görevi bulunacaktır."),

G(25,"Tema 4","Açınım Ayırma Bandı","Açınımdan cismi belirle","belt",
  ["Küp, silindir, üçgen prizma ve dikdörtgen prizma kutuları okunaklı; açınım kartı soldan kırpılıyor.","Kart etiketi '6 dikdörtgen yüz' gibi cevabı sözel olarak büyük ölçüde veriyor; gerçek açınım çizimi ekranda tam görünmüyor."],
  "Öğrenci yüz düzenini katlayıp ilişkilendirmeden etiket-kutu eşlemesi yapabilir.",
  ["Kart orta alanda tam görünen ölçekli açınım olsun; yüz adedi etiketi başlangıçta gizlensin.","Çocuk yüzleri sayıp komşu yüzleri işaretlesin, sonra katlama animasyonunu çalıştırsın.","Her cisim için farklı geçerli açınımlar ve kapanmayan çeldirici ağlar kullanılsın.","Sınıflandırmadan sonra açınım 3B cisme katlanarak sonucu kanıtlasın."],
  ["Altı eş kareden geçerli küp açınımı seçilir.","İki daire + bir dikdörtgen silindire katlanır.","Üçgen/dikdörtgen prizma ağları ile kapatılamayan bir çeldirici karşılaştırılır."],
  ["Yanlışta açınım katlanmaya çalışıp çakışan/açık kalan yüzleri gösterilsin.","Doğruda tüm yüzler numaralanarak 3B cisimde yerlerine otursun."],
  "Açınım kartı hiçbir kenarda kırpılmayacak; karar her tur gerçek katlama simülasyonuyla doğrulanacaktır."),
G(26,"Tema 4","Küp Tarayıcısı","Köşe, ayrıt ve yüzleri tara","draw",
  ["Küpün sekiz köşesi büyük sarı noktalarla, ayrıtları çizgilerle görünür; etkileşim konuya yakın.","Açılış/erken ses 'küpün sekiz köşesi vardır' diyerek çocuk taramayı tamamlamadan sonucu açıklayabiliyor; arka ayrıtlar ve yüzler için 3B algı desteği sınırlı."],
  "Keşif sayma etkinliği cevabı dinleyip noktaları işaretlemeye dönüşür; aynı köşe/ayrıtı iki kez sayma stratejisi görünmez.",
  ["Sonuç sayıları başlangıçta gizlensin; her dokunuş numaralandırılsın ve tekrar dokunma ikinci kez sayılmasın.","Küp parmakla döndürülebilsin; arka ayrıtlar kesikli, görünür olduğunda düz çizgi olsun.","Yüz modu açınım ile 3B küp arasında geçiş yaparak altı yüzü ilişkilendirsin.","Tarama sonunda V-A-Y tablosu çocuk sayımlarından otomatik oluşsun."],
  ["Döndürülebilir küpte 8 köşe sayılır.","12 ayrıt ön/arka ayrımıyla taranır.","6 eş kare yüz açınımda seçilip tekrar küpe katlanır."],
  ["Tekrar dokunulan öğe 'zaten sayıldı' işareti versin; sayaç artmasın.","Doğruda köşe-ayrıt-yüz sayıları Euler bağıntısına girmeden yaş düzeyine uygun tabloda karşılaştırılsın."],
  "Cevap sayıları tarama bitmeden sesli/yazılı verilmeyecek; küp tüm yönlerden döndürülebilir olacaktır."),
G(27,"Tema 4","Üçgen Çeşitleri Bandı","Kenarlarına göre üçgenler","belt",
  ["Üç sınıf kutusu tanımıyla birlikte altta; üçgen kartı soldan kırpılıyor ve eş kenar tırnakları çok küçük kalıyor.","Aynı üç SVG çizimi tekrar ediliyor; kenar uzunlukları ölçülemiyor ve tırnak işaretine bağımlı kalıyor."],
  "Küçük işareti göremeyen çocuk yanlış değerlendirilir; üçgenleri gerçek kenar ölçülerinden sınıflandırma gelişmez.",
  ["Üçgen merkezde sabit ve büyük çizilsin; kenarlar cetvel şeridiyle ölçülebilsin.","Eş kenarlar aynı renk ve aynı tırnak sayısıyla çift kodlansın; renk tek başına zorunlu olmasın.","Çocuk ölçüleri tabloya yazdıktan sonra eşkenar-ikizkenar-çeşitkenar sınıfını seçsin.","Döndürülmüş ve farklı görünüşte yeni üçgenler üretilsin; sınıf yönelimden etkilenmesin."],
  ["6-6-6 kenarlı üçgen eşkenardır.","5-5-8 ikizkenar; eş kenarlar ölçülür.","4-6-7 çeşitkenar; üçgen döndürülüp sınıfın değişmediği görülür."],
  ["Yanlışta üç kenar ölçüsü yan yana yazılıp eş olan çiftler çerçevelensin.","Doğruda sınıf tanımı ölçülen değerlerle sesli okunmalıdır."],
  "Tırnaklar 320 px ekranda seçilebilir olacak; en az üç farklı yönelim ve ölçü seti kullanılacaktır."),
G(28,"Tema 4","Köşe-Kenar Stüdyosu","Şekli çiz, ilişkiyi keşfet","draw",
  ["Üç numaralı büyük nokta ve noktalı kâğıt görünür; çocuk iki noktaya dokunarak kenar çiziyor.","Açılış sesinde 'üçgenin üç köşesi ve üç kenarı vardır' sonucu çizimden önce söylenebiliyor; kare/dikdörtgen hazır köşe konumlarından çiziliyor."],
  "Keşfedilecek ilişki önceden verildiğinde çizim yalnız yönergeyi tamamlar; serbest şekil oluşturma ve ölçme sınırlanır.",
  ["İlk turda yalnız boş noktalı kâğıt ve 'kapalı bir üçgen çiz' görevi verilsin; sonuç gizli kalsın.","Çizilen her yeni kenar numaralansın; şekil kapanınca köşe ve kenar sayaçları birlikte oluşsun.","Kare/dikdörtgen turunda kenar uzunlukları ölçülüp eş/karşılıklı eş ilişkileri çocuk tarafından işaretlensin.","Köşegen çizilirse bunun kenar olmadığı, şeklin iç çizgisi olduğu görsel olarak açıklansın."],
  ["Serbest üçgen çizilir; 3 köşe ve 3 kenar sayılır.","Kare çizilip dört kenarın eşliği ölçülür.","Dikdörtgende karşılıklı kenarlar eşlenir; kare ile ortak/farklı özellik tablosu doldurulur."],
  ["Açık şekil kapanmadıysa son iki uç vurgulansın; cevap verilmesin.","Doğruda sayaç, çizimdeki gerçek noktaları ve çizgileri sırayla işaretlemelidir."],
  "Açılış sesi sonucu söylemeyecek; çocuk en az bir şekli hazır zorunlu köşe seti olmadan oluşturacaktır."),
G(29,"Tema 4","Çevre Hesap Makinesi","Kenarları topla","num",
  ["Kare, dikdörtgen ve üçgen problemleri metin olarak veriliyor; tuş takımıyla sonuç giriliyor.","Şekiller gerçek çizim ve kenar etiketleriyle gösterilmiyor; ipucu '7 x 4' veya '(12+5)x2' işlemini baştan veriyor."],
  "Çevre kavramı dış sınırı ölçmekten hazır formülü hesaplamaya indirgenir.",
  ["Her soruda ölçekli şekil çizilsin ve bilinen kenarlar doğrudan şeklin üzerine yazılsın.","Çocuk dış sınırı parmağıyla dolaşarak hangi kenarların toplandığını işaretlesin.","Kare/dikdörtgende eş kenar işaretleri eksik uzunlukları buldurmalı; formül ancak tur sonunda genelleme olarak açılmalı.","Ters çevre sorusunda çevre şeridi dört eş parçaya bölünerek kenar bulunmalıdır."],
  ["Kenar 7 cm kare: dört kenar dolaşılıp 28 cm.","12 x 5 cm dikdörtgen: 12+5+12+5=34 cm.","6-8-10 üçgen 24 cm; çevresi 36 cm karede kenar 9 cm ters problemle bulunur."],
  ["Yanlışta işaretlenmeyen veya iki kez sayılan kenar şekil üzerinde renklenmeli.","Doğruda dış sınır animasyonu ve toplam eşitliği birlikte görünmelidir."],
  "Her turda çizim, kenar birimi ve tuşlanan sonuç tutarlı olacak; başlangıç ipucu tam işlemi vermeyecektir."),
G(30,"Tema 4","İp Dolama Deneyi","Eğri kenarın çevresini ölç","hold",
  ["Ekranda ip ve dairesel kutu yerine kronometre kadranı, yatay hedef şeridi ve basılı tut düğmesi var.","Tam 1 turu zamanlamayla yakalayınca sonradan 24 cm/36 cm açıklanıyor; gerçek ip uzunluğu ölçülmüyor."],
  "Etkinlik ölçme aracı seçimini değil parmağı hedef çizgide bırakma becerisini değerlendirir; verilen santimetre sonucunun görsel dayanağı yoktur.",
  ["Dairesel kutu ve sürüklenebilir ip gerçekten çizilsin; ip başlangıç noktasından çevre boyunca mıknatıslansın.","Tam turda ipin iki ucu birleşsin; sonra ip otomatik düzleşip cetvel üzerine taşınsın.","Çocuk cetvel ölçeğinden santimetre sonucunu okusun ve kaydetsin.","Farklı çaplı iki kutu karşılaştırılarak çevrenin büyüklükle ilişkisi gözlensin; zamanlama toleransı kaldırılmalıdır."],
  ["Küçük kutu ip ile bir tur dolanır ve 24 cm okunur.","Büyük kutu 36 cm ölçülür; iki ip yan yana karşılaştırılır.","Düz kenarlı defterde ip yerine cetvel/şerit metre seçilir; araç uygunluğu gerekçelendirilir."],
  ["Eksik turda açık kalan yay, fazla turda üst üste binen ip görünür olsun.","Doğruda ip cetvelde sıfır noktasından başlayıp ölçümün sonuna kadar kalmalıdır."],
  "Kronometre/hold motoru ana etkileşim olmayacak; santimetre sonucu gerçek ip-cetvel modeli üzerinden okunacaktır."),
G(31,"Tema 4","Alan Tahmin Ölçeri","Birim karelerle alan tahmini","slider",
  ["6 x 3 dikdörtgen sorusu tren-tünel sürgüsünde; 18 seçeneği başlangıçta hazır görünebiliyor.","Dikdörtgen, 6'lı satırlar veya birim kareler ekranda yok; sonraki ataç/defter soruları da nesne alanını göstermiyor."],
  "Alanı kaplama ve tahmin yerine doğru sayıyı seçenekten seçme ölçülür; ölçü birimi büyüdükçe sayının azalması gözlenmez.",
  ["Dikdörtgen 6 x 3 şeffaf birim kare ızgarasıyla çizilsin; önce ızgara kısmen gizli tutularak tahmin alınsın.","Onaydan sonra kareler satır/sütun olarak sayılıp 6x3 ilişkisi kurulsun.","Ataç ve defter gibi standart olmayan birimler hedef yüzey üzerinde gerçek boyut oranıyla döşensin.","Tahmin, gerçek sayım ve fark kaydedilsin; sürgü tarafsız başlasın ve tren görseli kaldırılmalıdır."],
  ["6 x 3 dikdörtgen önce tahmin, sonra 18 birim kare sayımı.","Kitap kapağı yaklaşık 30 eş ataçla boşluksuz kaplanır.","Aynı kapak iki büyük defter birimiyle kaplanır; birim büyüyünce sayının azaldığı yorumlanır."],
  ["Uzak tahminde gerçek cevap verilmeden satır/sütun sayma stratejisi önerilsin.","Doğruda tahmin-gerçek-fark ve kullanılan birim aynı sonuç kartında yer alsın."],
  "Tahmin öncesinde ölçülecek yüzey ve birim görünür olacak; varsayılan seçim doğru cevapta başlamayacaktır."),
G(32,"Tema 4","Ölçme Aracı Deposu","Doğru ölçme aracını seç","serve",
  ["Cetvel, şerit metre, ip, birim kare, terazi, termometre ve kronometre kartları okunaklı.","Sorular nesne ve özelliği metinde açıkça söylüyor; çoğu tek etiket seçimi ve gerçek ölçüm uygulaması yapılmıyor."],
  "Araç adını tanıma ölçülür, aracın nasıl kullanıldığı ve neden alternatifin uygun olmadığı deneyimlenmez.",
  ["Öğrenci önce ölçülecek niceliği (uzunluk/çevre/alan) seçsin, sonra aracı alsın.","Seçilen araç sahne üzerinde gerçekten kullanılabilir olsun: cetvel sıfıra hizalanır, ip dolanır, birim kare döşenir.","Birden fazla araç gereken eğri çevrede sıra kartlarıyla ip + cetvel süreci kurulsun.","Yanlış araç fiziksel olarak neden işe yaramadığını kısa simülasyonla göstersin."],
  ["Defter çevresi cetvelle dört kenar ölçülerek bulunur.","Sınıf çevresi şerit metreyle bölümler hâlinde ölçülür.","Konserve tabanı ip ile dolanıp cetvelde okunur; alan için birim kare seçilir."],
  ["Yanlışta araç adı değil ölçülecek nicelik yeniden vurgulansın.","Doğruda araç seçimi gerçek ölçüm ve birimli sonuçla tamamlanmalıdır."],
  "Her araç seçimi en az bir gerçek kullanım adımı içerecek; yalnız kartı tepsiye koymak başarı sayılmayacaktır."),

G(33,"Tema 5","Açı Avcısı Radarı","Günlük yaşamda açıyı bul","catch",
  ["Uzay radarı ve düşen metin kapsülleri kullanılıyor; kitap köşesi, saat, makas gibi günlük nesneler yalnız yazıyla anılıyor.","Açı görseli, ışınlar ve dönüş yayı bulunmuyor; çocuk hareketli sözcüğü yakalıyor."],
  "Günlük yaşam durumunu açı modeline dönüştürme yerine metin çoktan seçmeli ve motor takip ölçülür.",
  ["Makas, kapı, saat ve kitap köşesi gerçek büyük çizimler olarak sabit kartlarda gösterilsin.","Çocuk açı köşesini ve iki kolu işaretlesin; ardından dönüş yayı çizilsin.","Dik açı için kâğıt köşesi referansı nesnenin üzerine sürüklensin.","Sorular hareket etmesin; nesne-açı modeli-günlük dil üçlü eşleştirme kullanılsın."],
  ["Kitap köşesinde dik açı işaretlenir.","Saat 12'den 3'e çeyrek tur ve 90 derece olarak modellenir.","Makas az/çok açılır; dönüş miktarı değişirken kol uzunluğunun açıya etkisi olmadığı görülür."],
  ["Yanlış bölgeye dokununca gerçek köşe ve kollar kısa kılavuzla gösterilsin.","Doğruda nesne saydamlaşıp altında aynı iki ışınlı açı modeli kalmalıdır."],
  "Her günlük örnek gerçek görselle sunulacak; hareketli sözcük yakalama ana değerlendirme yöntemi olmayacaktır."),
G(34,"Tema 5","Açı Döndürücü","Işını hedef açıya çevir","hold",
  ["Açı yerine kronometre benzeri dairesel kadran ve yatay hedef şeridi kullanılıyor; basılı tutup 90 derece çizgisinde bırakılıyor.","Hedef sayı ve işaret baştan görünür; iki gerçek ışın arasındaki açıklık oluşmuyor."],
  "Çocuk açı oluşturmak yerine ilerleme çubuğunu zamanlıyor; açı türü ve dönüş yayı görsel olarak öğrenilmez.",
  ["Sabit bir başlangıç ışını ve uçtan sürüklenebilir ikinci ışın çizilsin.","Dönüş sırasında derece yayı ve küçük aralık işaretleri canlansın; ölçü yalnız bırakınca okunabilsin.","Hedef önce açı türü (dar/dik/geniş), sonraki turda derece olarak verilsin.","Kronometre/hold şeridi kaldırılıp doğrudan açısal sürükleme ve klavye/ok erişim alternatifi kullanılmalıdır."],
  ["90 derece dik açı oluşturulur ve kâğıt köşesiyle doğrulanır.","45 derece dar açı, dik açının yarısı olarak çizilir.","135 derece geniş ve 180 derece doğru açı ardışık dönüşlerle karşılaştırılır."],
  ["Yanlışta ışın seçilen yerde kalsın; hedefe eksik/fazla derece farkı yay üzerinde gösterilsin.","Doğruda açı türü, derece ve günlük örnek aynı kartta açılmalıdır."],
  "Açı gerçek iki ışınla oluşturulacak; başarı basılı tutma süresine değil ışının geometrik konumuna bağlı olacaktır."),
G(35,"Tema 5","Açı Tasnif Bandı","Dar, dik ve geniş açı","belt",
  ["Üç sınıf kutusu açık; açı kartı soldan kırpılıyor ve ince çizgiler kartın içinde zor seçiliyor.","30, 45, 60, 90, 100, 120, 150 derece örnekleri var; açıölçer ya da dik açı referansı kart üzerinde görünür değil."],
  "Küçük çizimi görememe ve kart hareketi sınıflamayı bozar; derece etiketini ezberleme riski vardır.",
  ["Açı merkezde büyük ve sabit çizilsin; yanında döndürülebilir kâğıt köşesi referansı bulunsun.","Çocuk önce 'dik açıdan küçük/eşit/büyük' karşılaştırmasını, sonra tür adını seçsin.","90 derece kartında kare işaretinin anlamı açıklansın; diğer kartlarda derece sayısı ilk turdan sonra gizlensin.","Sınırda 89-90-91 gibi yakın açıların büyük görsel ve açıölçer doğrulaması eklensin."],
  ["45 ve 60 derece dar açı olarak sınıflanır.","90 derece kâğıt köşesiyle tam örtüşür ve diktir.","120/150 geniş; 89-90-91 yakın karşılaştırmasında referans dikkatle kullanılır."],
  ["Yanlışta dik açı şablonu seçilen açının üzerine bindirilsin.","Doğruda karşılaştırma cümlesi ve tür adı birlikte okunmalıdır."],
  "Açı kartları hareket etmeyecek/kırpılmayacak; derece etiketi olmadan en az iki örnek sınıflandırılacaktır."),
G(36,"Tema 5","Kâğıt Köşesi Deneyi","Standart birim neden gerekli?","slider",
  ["Kâğıt köşesi yerine tren-tünel sürgüsü var; 0-90-180-270-360 seçenekleri eşit tünellerde gösteriliyor.","Bir, iki, yarım ve dört kâğıt köşesi yalnız metinle anlatılıyor; gerçek köşe açının üzerine yerleştirilmiyor."],
  "Standart olmayan ölçme deneyimi yaşanmadan hazır derece eşitliği seçiliyor; başlıkta deney, sahnede tren bulunuyor.",
  ["Sürüklenebilir gerçek kâğıt köşesi şablonu ve hedef açı çizilsin.","Çocuk köşeyi ardışık yerleştirip kaç tam/yarım köşe sığdığını saysın.","Farklı boydaki kâğıt köşelerinin açısının yine 90 derece olduğu, ancak elle yapılan yarımın belirsizliği karşılaştırılsın.","Sonra açıölçer aynı açıya yerleştirilip derece standardı ile sonuç doğrulansın; tren motoru kaldırılmalıdır."],
  ["Bir köşe dik açıya tam oturur: 90 derece.","İki köşe doğru açı oluşturur: 180 derece.","Yarım köşe yaklaşık 45; dört köşe tam tur 360 derece; açıölçerle kesinleştirilir."],
  ["Üst üste binme/boşlukta şablonun konumu düzeltilsin; cevap söylenmesin.","Doğruda kâğıt köşesi sayısı ile derece ölçüsü aynı yay üzerinde gösterilsin."],
  "Kâğıt şablonu gerçek hedef açıya yerleştirilecek; derece sonucu yalnız sürgü seçimiyle elde edilmeyecektir."),
G(37,"Tema 5","Açı Özellik Köprüsü","Açıyı özelliğiyle eşleştir","match",
  ["Beş hedef tanım ve altta beş açı adı okunaklı; küçük ikonlar gerçek açı çizimi olmaktan çok simge niteliğinde.","Dar, dik, geniş, doğru ve tam açı tek sabit eşleştirme dizisinde tanımla eşleniyor."],
  "Tanım ezberi ölçülür; bir açının ölçüsünden türünü çıkarma ve sınır değerleri tartışma sınırlıdır.",
  ["Her kaynak kartta sürüklenebilir gerçek açı ve derece yayı bulunsun; tür adı ilk turdan sonra gizlensin.","Hedefler açık sayı aralıklarıyla ve doğru matematiksel sınırlarla yazılsın.","Açı kartı hedefe geldiğinde kâğıt köşesi/yarım tur şablonuyla doğrulansın.","Aynı hedefe farklı örnek açıların gelebileceği çoklu eşleme turu eklensin."],
  ["45 derece dar, 90 derece dik, 135 derece geniş olarak eşlenir.","180 doğru ve 360 tam açı modelleri yerleştirilir.","30, 70, 100, 160 açıları uygun aralık hedeflerine çoklu olarak sınıflanır."],
  ["Yanlışta hedef aralığı sayı doğrusu ve açı yayı üzerinde gösterilsin.","Doğruda açı çizimi ve tanım üst üste gelip tür adı oluşsun."],
  "Kartların tamamı gerçek açı çizimi taşıyacak; sınır ifadeleri 90/180/360 derecelerle matematiksel olarak tutarlı olacaktır."),
G(38,"Tema 5","Açı Kartları","Açıyı günlük örnekle eşleştir","memory",
  ["On iki kapalı kartta açı türleri ve günlük örnekler bulunuyor; ilk sahne yalnız kart arkalarını gösteriyor.","Eşler metinsel: dik açı-duvar/zemin, dar açı-az açılmış makas gibi; nesne resminin gerçek açısı görünmüyor."],
  "Konum hafızası ve sözcük çağrışımı, günlük nesnedeki açıyı belirleme yerine geçebilir.",
  ["İlk turda kartlar açık olsun; nesne görselindeki köşe ve kollar öğrenci tarafından işaretlensin.","Açı türü kartında gerçek iki ışın ve derece aralığı bulunsun.","Eşleşince nesne ile soyut açı saydam üst üste bindirilsin.","Kapalı hafıza turu ancak görsel eşleştirme öğrenildikten sonra isteğe bağlı tekrar olarak kullanılmalıdır."],
  ["Duvar-zemin ile 90 derece dik açı eşleştirilir.","Az açılmış makas ile dar; çok açılmış kitap ile geniş açı eşlenir.","Düz yol 180, tam dönüş 360; öğrenci günlük yeni örneği kendisi seçer."],
  ["Yanlış çiftte iki görsel açık kalıp açı açıklıkları karşılaştırılsın.","Doğru çiftte nesnenin açı yayı ve tür kartı aynı renk olmalıdır."],
  "En az bir turda bütün kartlar açıkken kavram eşleştirmesi ölçülecek; nesne kartları yalnız metin değil görsel taşıyacaktır."),
G(39,"Tema 5","Açı Çizim Stüdyosu","İki ışınla açı çiz","draw",
  ["Merkez V ve çevre noktaları var; bazı etiketler 'yukarı' yerine kırpılmış 'uka' gibi görünüyor.","Açılış sesi 'doksan derecelik dik açıyı çizdin' diyerek çizim yapılmadan başarı cümlesi söyleyebiliyor; görev hazır iki noktayı seçmeye indirgeniyor."],
  "Cevap önceden verilir ve çocuk kendi ışın yönünü üretmez; küçük/bozuk etiketler yanlış dokunma yaratır.",
  ["V köşesinden çıkan ilk ışın sabit, ikinci ışın serbestçe sürüklenebilir olsun.","Açıölçer isteğe bağlı araç olarak köşeye hizalansın; etiketler minimum 12 punto ve tam görünür olsun.","Tür adıyla çizim, dereceyle çizim ve verilen çizimi adlandırma ayrı görevler olsun.","Başarı sesi yalnız çizim doğrulandıktan sonra çalışmalı; açılışta nötr yönerge kullanılmalıdır."],
  ["90 derece dik açı serbest ışınla çizilir.","45 derece dar ve 135 derece geniş açı açıölçerle kurulur.","180 derece doğru açı çizilir; ardından etiketsiz 70 derece açı tür olarak adlandırılır."],
  ["Yanlışta ışın korunup hedefe derece farkı gösterilsin; otomatik doğru konuma sıçramasın.","Doğruda köşe, iki ışın ve derece yayı ayrı ayrı isimlendirilmelidir."],
  "Açılışta sonuç seslendirilmeyecek; serbest ışın konumu üzerinden en az üç farklı açı çizilecektir."),
G(40,"Tema 5","Derece Hesap Makinesi","Açı ölçülerini hesapla","num",
  ["Dik/doğru/tam açı soruları tuş takımında; şekil veya açıölçer görünmüyor.","İpuçları 90+90, 90÷2 ve 4x90 işlemlerini doğrudan veriyor; çocuk açı ilişkisini değil aritmetiği yapıyor."],
  "Dereceyi standart ölçü birimi olarak kullanma görsel ölçümden kopuyor; hazır işlem cevaba giden yolu tamamen söylüyor.",
  ["Her soruda ilgili açı yayı ve kâğıt köşesi parçaları çizilsin.","Çocuk 90 derecelik parçaları birleştirip/ikiye bölüp dereceyi modelden çıkarsın.","Açıölçer ölçeği üzerinde başlangıç ve bitiş çizgileri okunarak sonuç tuşlansın.","İpucu ilk aşamada yalnız referans dik açıyı göstermeli; tam aritmetik ifade son ipucuna bırakılmalıdır."],
  ["Bir dik açı modelden 90 derece okunur.","İki dik açı birleşip 180 doğru açı olur.","Dik açının yarısı 45; dört dik açı 360; 180-90 farkı 90 olarak modellenir."],
  ["Yanlışta açı yayı üzerindeki kaç dik açı parçası olduğu vurgulansın.","Doğruda model, işlem ve derece birimi birlikte doğrulanmalıdır."],
  "Her tuşlanan sonuç görünür açı modeliyle desteklenecek; ilk ipucu tam işlemi doğrudan yazmayacaktır."),

G(41,"Tema 6","Ayna Odası","Aynadaki eşi bul","mirror",
  ["Yarım mavi şekil ve dikey pembe ayna çizgisi okunaklı; üç metin seçeneği altta.","Doğru seçenek 'aynadaki gibi ters çevrilmiş' diye kendini sözel olarak ele veriyor; seçeneklerin gerçek şekil ön izlemesi yok."],
  "Simetrik parçayı görsel özelliklerinden seçmek yerine doğru cümleyi okumak yeterlidir.",
  ["Üç seçenekte gerçek şekil parçaları gösterilsin: doğru yansıma, aynı yön ve ölçeği bozulmuş çeldirici.","Parçalar ayna çizgisinin sağına sürüklenip katlama animasyonuyla denenebilsin.","Doğru yansımada eksene eş uzaklıktaki işaret noktaları eşleştirilsin.","Metinsel doğru cevabı ele veren etiketler kaldırılıp erişilebilir sesli betimleme nötr yazılmalıdır."],
  ["Kelebek yarısı dikey aynada tamamlanır.","Yatay eksende balık/ok şekli yansıtılır.","Eğik eksene göre basit üçgen motifin doğru yansıması seçilir."],
  ["Yanlış parça katlandığında örtüşmeyen alan kırmızı saydam görünmelidir.","Doğruda iki yarı katlanıp tam örtüşerek aynı boyut/eş uzaklık özelliğini kanıtlamalıdır."],
  "Doğru seçenek metninden anlaşılmayacak; bütün seçenekler aynı boyda gerçek şekil ön izlemesi taşıyacaktır."),
G(42,"Tema 6","Simetri Denetim Bandı","Simetrik mi, değil mi?","belt",
  ["A, F, H, R, T, G, M, L harfleri bantta; ilk kart soldan kırpılıyor.","Simetri kararları kullanılan harf tipine bağlı ve kartta sözü edilen pembe dikey eksen görünür olmadan harf adıyla sınıflama yapılıyor."],
  "Font değişince doğru cevap tartışmalı olabilir; ekseni görmeden ezberlenen harf kararı gerçek katlama yargısı değildir.",
  ["Harfler sistem fontu değil sabit vektör çizimler olarak gömülsün.","Denetlenen eksen kartın üzerinde sürekli çizilsin; kart karar verilene kadar merkezde sabit kalsın.","Karardan sonra iki yarı eksenden katlanıp uyuşan/uyuşmayan alanlar üst üste gösterilsin.","Harflerin yanında kelebek, vazo ve geometrik motifler kullanılarak font bağımlılığı azaltılsın."],
  ["Vektör A, H, T dikey eksende denetlenir.","F, R, L aynı eksende simetrik değildir.","Aynı motif yatay ve dikey eksenlerde ayrı değerlendirilerek eksen yönünün önemi görülür."],
  ["Yanlışta gerçek katlama sonucu gösterilsin; kart aniden kaybolmasın.","Doğruda iki yarı yarı saydam olarak tam çakışmalıdır."],
  "Bütün harf geometrileri sabit vektör olacak; test edilen eksen görünür ve kart tam ekranda olacaktır."),
G(43,"Tema 6","Simetri Dokuma Tezgâhı","Dikey simetriyle tamamla","mirror",
  ["8 x 6 ızgara, dikey pembe eksen ve dört renk paleti görünür; konu-motor uyumu güçlü.","13 verilen hücrenin karşılığı tek tek dolduruluyor; silgi/geri al görünmüyor ve yalnız renk kodu kullanılıyor."],
  "Uzun görevde tek dokunma hatası ağırlaşır; renk görme farklılığı olan çocuklar için eşleme zorlaşabilir.",
  ["Renklerin yanında desen/doku simgeleri de bulunsun; palet seçimi belirgin kalsın.","Kaynak hücre seçilince eksene uzaklığı sayan kılavuz ve olası eş hedef çerçevesi görünsün.","Silgi, geri al ve tümünü temizle seçenekleri eklensin.","İkinci turda eksen yatay, üçüncü turda bazı yanlış hücreleri denetleme görevi olsun."],
  ["Mevcut 8 x 6 desen dikey eksende tamamlanır.","6 x 8 yeni desen yatay eksende yansıtılır.","Tamamlanmış desendeki üç yanlış renk/konum bulunup eş uzaklık kuralıyla düzeltilir."],
  ["Yanlış hücrede kaynak ile eksene uzaklıkları sayan kareler gösterilsin.","Doğru eş çift aynı anda çerçevelenip katlama ön izlemesi versin."],
  "Geri al/silgi çalışacak; renk dışı doku kodları bulunacak ve bütün eş hücreler eksene eş uzaklıkta hesaplanacaktır."),
G(44,"Tema 6","Mozaik Ustası","Çift eksende simetri","mirror",
  ["6 x 6 ızgarada yatay/dikey pembe eksenler ve sol üstte beş kaynak hücre var; diğer üç bölge dolduruluyor.","Her kaynak için üç yansıma gerektiğinden görev 15 yerleştirme ister; üst metin ve paletin sol kenarı küçük ekranda sıkışabiliyor."],
  "Çift eksen koordinatları karışabilir; geri alma olmadan motor hatası kavramsal hata gibi cezalandırılır.",
  ["Kaynak hücre seçilince dikey, yatay ve çapraz eşlerin yön okları kısa süre görünsün.","Palet ve yönerge küçük ekranda kaydırmasız tam görünür olacak şekilde düzenlensin.","Silgi/geri al bulunsun; kaynak hücreler kilitli kalıp yanlışlıkla değişmesin.","Bitişte desen önce dikey, sonra yatay katlanarak iki eksen ayrı ayrı doğrulansın."],
  ["Beş kaynak hücre üç bölgeye doğru yansıtılır.","8 x 6 farklı motifte iki eksen dönüşümü kurulur.","Hazır mozaikte bir dikey, bir yatay ve bir çapraz eş hatası bulunup düzeltilir."],
  ["Yanlışta hangi eksen dönüşümünün bozulduğu açıkça söylensin.","Doğru dörtlü hücre grubu aynı desen işaretiyle bağlansın."],
  "Küçük ekranda palet/metin kırpılmayacak; geri alma bulunacak ve iki eksen için katlama testi ayrı ayrı geçecektir."),
G(45,"Tema 6","Simetri Doğrusu Çizimi","Katlanma çizgilerini bul","draw",
  ["Kare üzerinde sekiz büyük nokta var; öğrenci nokta çiftleriyle dört simetri doğrusu çiziyor.","Açılış sesi 'karenin dört simetri doğrusu vardır: iki orta çizgi ve iki köşegen' diyerek görevin tamamını önceden açıklıyor; çizim serbest değil."],
  "Keşif, söylenen dört çizgiyi nokta çiftlerinden tekrar etmeye dönüşür; neden katlama doğrusu oldukları denenmez.",
  ["Açılışta sayı ve çizgi türü söylenmesin; çocuk olası katlama çizgisini serbest sürüklesin.","Her çizimden sonra şekil eksenden katlanıp örtüşme testine girsin.","Kabul edilen çizgiler şekil üzerinde kalıp sayaç çocuk keşfettikçe artsın.","Dikdörtgenin köşegenleri için örtüşmeme kanıtı, dairede farklı çaplarla sayısızlık fikri gösterilsin."],
  ["Karede iki orta ve iki köşegen dört doğru keşfedilir.","Dikdörtgende yalnız yatay/dikey orta çizgiler kabul edilir; köşegen reddedilir.","Dairede merkezden geçen dört farklı çap denenir ve örüntüden sayısız doğru yargısına ulaşılır."],
  ["Yanlış çizgide katlanan iki yarının ayrışan bölgesi görünür olsun.","Doğruda çizgi kalıcılaşıp katlama tam örtüşmeyle sonuçlansın."],
  "Açılış sesi sonuç sayısını vermeyecek; her kabul edilen doğru gerçek katlama simülasyonunu geçecektir."),
G(46,"Tema 6","Kodlama Mimarı","Geometrik yapı için rota kodla","code",
  ["Izgara, robot, yapı hedefi, duvarlar ve yön düğmeleri okunaklı; üç rota turu bulunuyor.","Alt başlık 'yapıyı kodlama ile oluştur' olsa da çocuk yapı oluşturmuyor, yalnız robota hedefe giden yol yazıyor; birden fazla geçerli yolun nasıl değerlendirildiği açıklanmıyor."],
  "Kazanımdaki şekil-yapı ilişkisi rota bulmaya daralır; maksimum adım sınırı strateji ölçütü olmadan deneme-yanılmayı teşvik edebilir.",
  ["Her rota sonunda robotun geçtiği hücreler bir geometrik şekil/duvar planı oluştursun.","Komut şeridi blok bazında sürüklenip düzenlenebilsin; çalışırken aktif blok parlasın.","Birden fazla güvenli rota kabul edilsin, ardından kısa/uzun rota adım sayıları karşılaştırılsın.","Üçüncü turda verilen planın çevresini dolaşan kod veya hedef şekli çizen rota kurulmalıdır."],
  ["6 x 5 ızgarada engellerden kaçınarak yapıya ulaşılır.","Aynı hedefe iki geçerli rota bulunup adım sayıları karşılaştırılır.","Robot ızgarada bir dikdörtgenin dış sınırını çizerek başlangıca döner."],
  ["Çarpışmada ilk hatalı komut kırmızı olsun; programın geri kalanı silinmesin.","Doğruda rota, komut dizisi ve oluşan geometrik plan aynı renkle eşleşsin."],
  "Program tek blok düzeyinde düzenlenebilecek; en az bir tur hedefe ulaşmanın yanında geometrik bir şekil/yapı oluşturacaktır."),
G(47,"Tema 6","Simetri Sayısı Köprüsü","Şeklin simetri doğrusu sayısı","match",
  ["Kare, dikdörtgen, eşkenar/ikizkenar üçgen ve daire kartları beş sayı hedefiyle eşleniyor.","Şekil ikonları küçük ve simetri doğruları görünmüyor; öğrenci hazır sayı çiftlerini ezberleyebilir."],
  "Simetri doğrusu sayısı katlama/çizme ile doğrulanmadan sözel bilgi olarak kalır.",
  ["Her şekil büyük etkileşimli kartta açılsın; çocuk önce olası doğruları çizsin.","Her çizgi katlama testini geçerse sayaca eklensin; başarısızsa neden örtüşmediği gösterilsin.","Sayı kartı ancak çizim tamamlandıktan sonra seçilsin.","Çeşitkenar üçgen ve paralelkenar gibi sıfır simetri doğrulu çeldiriciler de eklensin."],
  ["Kare 4 ve dikdörtgen 2 doğru çizilerek sayılır.","Eşkenar üçgen 3, ikizkenar üçgen 1 doğruyla doğrulanır.","Dairede çok sayıda çap denenip sayısız; çeşitkenar üçgende 0 sonucu bulunur."],
  ["Yanlış sayıda eksik/fazla çizgiler şekil üzerinde sayılmalı.","Doğruda çizilen tüm doğrular görünür kalıp sayı kartına bağlanmalıdır."],
  "Sayı eşleştirmesi çizim/katlama aşaması tamamlanmadan kabul edilmeyecek; sıfır doğrulu bir örnek eklenecektir."),
G(48,"Tema 6","Simetri Adımları","Oluşturma sürecini sırala","order",
  ["Beş uzun süreç kartı roket çevresinde hareket ediyor; roket/yakıt metaforu simetri oluşturmayla ilişkili değil.","Sabit adımlar: doğruyu belirle, köşeleri işaretle, uzaklığı ölç, eş noktayı koy, birleştir. Gerçek şekil üzerinde uygulanmıyor."],
  "Sözel sıra ezberlenir; her adımın simetri çizimindeki işlevi ve eş uzaklık ilişkisi görülmez.",
  ["Kartlar sabit bir iş akışı şeridinde sürüklenerek sıralansın; roket kaldırılmalıdır.","Her kart yerleştirildiğinde aynı örnek şekil üzerinde ilgili işlem animasyonla uygulanmalı.","İkinci turda eksik adım, üçüncü turda yanlış sırayla yapılmış çizimde hata bulunmalıdır.","Ölçülen uzaklıklar kare hücre veya cetvel birimiyle iki tarafta açıkça yazılmalıdır."],
  ["Beş temel adım doğru sıraya konur ve bir üçgen yansıtılır.","Dört adımlı süreçte eksik 'eş uzaklıkta nokta koy' kartı bulunur.","Yanlış çizimde noktalar birleştirilmeden önce uzaklık ölçülmediği teşhis edilip süreç düzeltilir."],
  ["Yanlış sırada kart yerinde kalıp hangi ön koşulun eksik olduğu gösterilsin.","Doğru sırada bütün adımlar tek şekil üzerinde baştan sona yeniden oynatılsın."],
  "Kartlar sabit ve tam okunur olacak; süreç en az bir gerçek şekil yansıtma uygulamasıyla tamamlanacaktır."),

G(49,"Tema 7","Olasılık Bandı","İmkânsız, olabilir, kesin","belt",
  ["Üç kutu ve dokuz günlük olay örneği var; kartlar soldan kırpılarak geliyor.","Bazı ifadeler bağlama duyarlı: 'yarın güneş doğacak' ve 'insan kanatsız uçacak' gibi cümleler günlük dilde anlaşılır olsa da koşul belirtilmeden mutlak sınıf sunuyor."],
  "Dilsel/bağlamsal belirsizlik matematiksel olasılık kararını tartışmalı kılabilir; kart hareketi okuma hatası üretir.",
  ["Kart merkezde sabit dursun ve gerekli koşullar açık yazılsın: standart altı yüzlü zar, torbanın içeriği, kendi bedeniyle uçma gibi.","Öğrenci önce mümkün sonuçlar kümesini görsün, sonra imkânsız-olabilir-kesin sınıfını seçsin.","Kesinlik günlük varsayımdan değil tanımlı deneyden çıkarılsın.","Her seçimden sonra olayın neden o sınıfta olduğu seçenek sayımı veya koşul üzerinden açıklansın."],
  ["Standart zarda 7 gelmesi imkânsız, 3 gelmesi olabilir.","Yalnız kırmızı toplu torbadan kırmızı çekmek kesin.","5 kırmızı 5 mavi torbadan kırmızı çekmek olabilir; sonuç uzayı görünür."],
  ["Yanlışta deneydeki tüm mümkün sonuçlar listelensin; cevap adı doğrudan söylenmesin.","Doğruda olay cümlesi koşuluyla birlikte sınıf kutusunda kalmalıdır."],
  "Her olayın koşulu matematiksel olarak yeterli olacak; bağlama göre değişebilen mutlak ifadeler yeniden yazılacaktır."),
G(50,"Tema 7","Olasılık Ölçeği","Olayı ölçekte yerleştir","slider",
  ["Tren sürgüsü üç durakta imkânsız-olabilir-kesin gösteriyor; kaynak 0-5-10 sayısal ölçeğini her 'olabilir' olaya tam 5 veriyor.","'Bir taş suya atılınca batacak' kesin sayılıyor; taş türü ve su koşulu belirtilmediği için evrensel kesinlik değildir."],
  "Olabilir kategorisini her zaman orta olasılık gibi öğretmek yanlış genellemedir; nitel kategori ile nicel oran karışır.",
  ["Bu sınıf düzeyinde ölçek üç geniş bölge olarak kullanılsın; 0-5-10 kesin sayısal olasılık puanı gibi sunulmasın.","Deneysel örneklerde torba içeriği görünür olsun; olayın mümkün ama az/çok olabileceği yalnız karşılaştırma diliyle ele alınsın.","Kesin örnek için yalnız kırmızı toplu torba, imkânsız için torbada olmayan renk seçilsin.","Tren yerine açık uçlu olasılık çizgisi ve sürüklenen olay kartı kullanılsın; taş örneği koşullu yazılmalı veya çıkarılmalıdır."],
  ["Yalnız kırmızı toplu torbadan kırmızı çekmek kesin bölgesine yerleşir.","Kırmızı ve mavi toplu torbadan kırmızı çekmek olabilir bölgesindedir.","Torbada hiç yeşil yokken yeşil çekmek imkânsızdır; aynı olay içerik değişince yeniden sınıflanır."],
  ["Yanlışta torba içeriği saydırılıp mümkün sonuçlar gösterilsin.","Doğruda nitel sınıf söylenmeli; keyfî 5/10 gibi kesin olmayan sayısal değer zorunlu tutulmamalıdır."],
  "'Olabilir = her zaman 5/10' eşlemesi kaldırılacak; bütün kesin/imkânsız örnekler açık koşullarla mantıksal olarak doğru olacaktır."),
G(51,"Tema 7","Araştırma Planı Masası","Araştırma sürecini kur","serve",
  ["Problem, araştırma sorusu, plan, çetele, grafik, yorum ve iki çeldirici kartı bulunuyor.","Müşteri metni 'ilk iki adım', 'toplama aşamasının iki ögesi' diyerek hazır adları seçtiriyor; gerçek bir araştırma sorusu/plan oluşturulmuyor."],
  "Araştırma süreci sabit etiket sırası olarak ezberlenebilir; problem, hedef grup ve değişken ilişkisi kurulmaz.",
  ["Nötr bir merak durumu verilsin; öğrenci hedef grup, değişken ve araştırma sorusunu kartlardan kurup gerekirse metinle tamamlasın.","Veri toplama yöntemi ve çetele başlıkları seçilen soruya göre otomatik değil öğrenci tarafından belirlenmeli.","Süreç kartları en son özet olarak sıralansın; önce gerçek mini araştırma yürütülsün.","Tek cevaplı bilgi sorusunun neden dağılım üretmediği iki örnekle karşılaştırılsın."],
  ["'4/A'nın sevdiği kitap türü' için problem ve araştırma sorusu kurulur.","Hedef grup ve çetele kategorileri planlanır.","Toplanan küçük veri grafiğe çevrilir, yorumlanır ve altı adım geriye dönük sıralanır."],
  ["Yanlış kartta 'bu aşamada ne üretmek istiyoruz?' sorusu gösterilsin.","Doğruda kart yalnız etikete değil oluşturulan gerçek araştırma ürününe bağlanmalıdır."],
  "En az bir turda araştırma sorusu ve veri planı öğrenci tarafından oluşturulmadan süreç tamamlanmış sayılmayacaktır."),
G(52,"Tema 7","Veri Toplama Çetelesi","Gelen cevabı işle","tally",
  ["Yazın-kışın-baharda sütunları ve tek tek gelen 10 yanıt okunaklı; beşinci çizginin çapraz oluşacağı yazıyor.","Yanıtların çoğu 'yaz', 'kış', 'bahar' kelimesini doğrudan içeriyor; çocuk gerçek görüşme/karar yerine belirgin kelimeyi sütuna taşır."],
  "Çetele yapısı kısmen görünse de veri toplama ve kategori kodlama çok kolaylaştırılmıştır.",
  ["Önce araştırma sorusu ve kategoriler öğrenciyle belirlenip boş çetele hazırlanmalı.","Yanıtlar bazen dolaylı ifade içersin; kategori seçimi gerekçelendirilsin.","İlk dört çizgi dik, beşinci çapraz olarak görünür oluşsun; geri al ve düzeltme bulunsun.","Toplam çetele sayısı işlenen yanıt sayısıyla her adımda karşılaştırılsın."],
  ["10 mevsim yanıtı mevcut tabloya işlenir; beşli grup oluşur.","12 kitap türü yanıtı yeni kategorilere çetelelenir.","İki hatalı sütun girişi bulunup geri alınır; çetele sıklık sayılarına dönüştürülür."],
  ["Yanlış sütunda yanıt yeniden okunup kategori ölçütü vurgulansın.","Beşinci işarette grup tamamlanınca '5' sayısı ve çapraz çizgi birlikte görünmelidir."],
  "Geri alma çalışacak; beşli çetele standardı korunacak ve toplam işaret sayısı yanıt sayısına eşit olacaktır."),
G(53,"Tema 7","Grafik Fabrikası","Çeteleyi grafiğe dönüştür","graph",
  ["Kaynak sıklık 5-3-2 üstte doğrudan yazılı; öğrenci depodan toplam 10 renkli blok ekliyor.","Grafikte sayısal dikey eksen/ölçek etiketi zayıf; farklı yıldız/üçgen/daire blokları aynı 'bir kişi' birimini gereksizce çeşitlendiriyor."],
  "Grafik kurma hazır sayı kadar dokunmaya indirgenir; eş birim ve eksen okuma kavramı bulanıklaşır.",
  ["Kaynak standart çetele olarak gösterilsin; öğrenci her satırı 5+kalana göre okuyup sıklığı çıkarsın.","Tüm grafik birimleri aynı biçim/renk temel bloğu olsun; kategori rengi sütun arka planında kullanılsın.","Dikey eksen 0'dan başlayıp 1'er artan işaret ve 'kişi' birimi taşısın.","Bloklar sütunda tabandan boşluksuz yükselsin; yanlış sütun ve fazla blok geri alınabilsin."],
  ["5-3-2 verisi çeteleden sütun grafiğine dönüştürülür.","Yeni 2-6-4 veri setinde eksen 0-6 kurulur.","Bir hatalı grafikte boşluk, fazla blok ve yanlış sütun bulunup düzeltilir."],
  ["Yanlışta kaynak çetele satırı ile hedef sütun aynı renkte vurgulansın.","Doğruda her sütunun blok sayısı, eksen değeri ve sıklık sayısı birebir eşleşsin."],
  "Grafik 0 tabanlı açık eksen ve birim anahtarı taşıyacak; tüm veri blokları eş büyüklükte olacaktır."),
G(54,"Tema 7","Veri Terazisi","Grafikten fark ve toplam bul","balance",
  ["5 kişilik yaz ve 3 kişilik kış kefeleri var; sağ etiket '3/5' biçiminde göründüğü için kesir gibi okunabiliyor.","Öğrenci +1 kişi düğmesine iki kez basarak denge kuruyor; gerçek grafik ekranda yok ve son tur toplam görevi denge metaforundan uzaklaşıyor."],
  "Grafik yorumlama verilen sayıları tamamlama işlemine dönüşür; 3/5 gösterimi veri sayısı ile kesri karıştırabilir.",
  ["Üstte kaynak sütun grafiği sürekli görünür olsun; iki sütundaki noktalar satır satır eşleştirilsin.","Eşleşmeyen noktalar fark olarak sayılıp ardından teraziyle doğrulansın.","Etiketler '3 kişi / hedef 5 kişi' biçiminde yazılsın; kesir eğik çizgisi kullanılmasın.","Toplam sorusu için terazi yerine tüm sütunları birleştiren ayrı toplam paneli kullanılmalıdır."],
  ["5 ve 3 arasında eşleşmeyen 2 kişi bulunur.","5 ve 2 arasında fark 3'tür.","5+3+2=10 toplamı üç sütundaki bütün bloklar sayılarak bulunur."],
  ["Fazla blokta yalnız son ekleme geri alınsın ve iki taraf değeri gösterilsin.","Doğruda grafik eşlemesi, çıkarma işlemi ve terazi sonucu aynı sayıyı vermelidir."],
  "Kişi sayıları kesir biçiminde gösterilmeyecek; fark ve toplam farklı, uygun görsel stratejilerle çözülecektir."),
G(55,"Tema 7","Sonuç Değerlendirme","Araştırmayı yorumla","tally",
  ["Futbol-basketbol-voleybol sütunları ve sırayla gelen 10 hazır yanıt bulunuyor.","Yönerge 'Sıradaki düğmesi' diyor ancak ilk görünümde böyle bir düğme belirgin değil; öğrenci hazır oyları işlemenin sonunda yalnız tek çoktan seçmeli yorumu seçiyor."],
  "Kontrol yöntemi belirsiz ve yorumlama yalnız 'en çok' sorusuna daralıyor; verinin sınırlılığı/araştırma sorusu değerlendirilmez.",
  ["Gerçek kontrol düğmesi veya sütuna dokunma yönergede birebir aynı adla anlatılsın.","Veri toplama sonrası çetele otomatik sütun grafiğine dönüştürülsin; öğrenci en çok, en az, fark ve toplam sorularını yanıtlasın.","En az iki doğru yorum ve bir veriden çıkarılamayan iddia ayırt edilsin.","Sonuç cümlesi araştırma sorusuna, hedef gruba ve örneklem sınırına açıkça bağlansın."],
  ["5-3-2 spor verisinde en çok futbol, en az voleybol bulunur.","Futbol-basketbol farkı 2 ve toplam 10 hesaplanır.","'Bütün okul futbolu sever' iddiasının yalnız bu sınıf verisinden çıkarılamayacağı belirlenir."],
  ["Yanlış yorumda grafikte o iddiayı destekleyen/desteklemeyen sütunlar vurgulansın.","Doğruda yorum veri ve hedef grup adıyla tam cümle olarak oluşturulmalıdır."],
  "Yönerge-kontrol adı tutarlı olacak; en az üç farklı yorum türü ve bir çıkarılamayan iddia değerlendirilecektir."),
G(56,"Tema 7","Grafik Hesap Makinesi","Grafikten sayısal sonuç çıkar","num",
  ["Tuş takımı görünür; ancak grafik çizilmemiş, veriler üstte 5-3-2 olarak yazı ve hazır işlem ipucuyla veriliyor.","Son soru 'Futbolu seçenler, voleybolu seçenlerin kaç katıdır?' için 5 ve 2 değerlerine rağmen cevap 2 kabul ediliyor; doğru kesin oran 5/2 = 2,5'tir. 'Yaklaşık' ifadesi soruda yoktur."],
  "Grafik okuma yerine hazır aritmetik yapılır ve son tur matematiksel olarak yanlış cevabı öğretir.",
  ["Gerçek sütun/nokta grafiği ve açık '1 blok = 1 kişi' anahtarı ekranda gösterilsin; sayı listesi cevap yerine geçmesin.","İpucu ilk aşamada yalnız ilgili sütunları vurgulasın; 5+3+2 veya 5-2 işlemini baştan yazmasın.","Kat sorusu bu sınıf düzeyine uygun tam kat veren veriyle değiştirilsin (ör. 6 ve 2 = 3 kat) veya açıkça 'yaklaşık kaç kat' diye yazılsın.","2,5 kullanılacaksa ondalık/kesir kapsamı ve giriş aracı sınıf düzeyiyle doğrulanmalı; aksi hâlde soru çıkarılmalıdır."],
  ["Grafikten 5+3+2=10 toplamı bağımsız bulunur.","En çok 5 ile en az 2 arasındaki fark 3'tür.","Yeni grafikte 6 futbol, 2 voleybol seçilir; 6÷2=3 kat kesin ve yaş düzeyine uygun olur."],
  ["Yanlışta ilgili grafik sütunları çerçevelensin; işlem doğrudan verilmeden toplam/fark/kat stratejisi sorulsun.","Doğruda sayı, işlem, birim ve grafikteki gerçek bloklar birebir eşleşsin."],
  "5'in 2'nin kaç katı olduğu kesin soruda 2 kabul edilmeyecek; veri 6-2 olarak değiştirilecek veya soru 'yaklaşık' diye yeniden yazılacaktır."),
]


THEMES = {
    "Tema 1": ("Sayılar ve Nicelikler (1) - altı basamaklı sayılar, sıralama, yuvarlama ve örüntü", CORAL,
               ["Altı basamaklı sayılar bölük ve basamak modelleriyle kurulmalı; ipucu cevabı başlangıçta vermemeli.", "Hareketli bant/radar kartları sabit ve tam okunur olmalı; motor hızı değerlendirmeye karışmamalı.", "Yuvarlama, ritmik sayma ve örüntü kuralları farklı yön ve örneklerle genellenmelidir."]),
    "Tema 2": ("Sayılar ve Nicelikler (2) - kesirler, çokluk ve birim dönüşümleri", GOLD,
               ["Kesir sembolleri gerçek parça-bütün modelleriyle kanıtlanmalı.", "Bileşik, tam sayılı ve denk kesir dönüşümleri çocuk tarafından kurulmalı; sipariş metni çözümü söylememeli.", "Birim dönüşümlerinde 10, 100 ve 1000 katsayıları doğru aile ve geçişlerde kullanılmalıdır."]),
    "Tema 3": ("İşlemlerden Cebirsel Düşünmeye", PURPLE,
               ["Ara işlem, elde/onluk bozma ve zihinden strateji görünür olmalı; yalnız son sayı tuşlanmamalı.", "Çarpma-bölme tersliği aynı nesne dizisi üzerinde çoklu örneklerle kanıtlanmalı.", "Problem ve yönerge çocuk tarafından oluşturulmalı; hazır çözüm kartı başlangıçta görünmemelidir."]),
    "Tema 4": ("Nesnelerin Geometrisi (1) - cisim, şekil, çevre ve alan", TEAL,
               ["Açınımlar gerçek 3B katlama, şekiller serbest çizme ve ölçme eylemiyle doğrulanmalı.", "İp, cetvel, birim kare ve alan yüzeyi ekranda gerçek etkileşim nesnesi olmalı.", "Tren/kronometre gibi ortak motorlar ölçme bağlamının yerini almamalıdır."]),
    "Tema 5": ("Nesnelerin Geometrisi (2) - açılar", BLUE,
               ["Açı gerçek iki ışın, köşe ve dönüş yayıyla gösterilmeli; zamanlama çubuğuna indirgenmemeli.", "Dik açı referansı, kâğıt köşesi ve açıölçer gerçek şeklin üzerinde kullanılmalı.", "Açılış sesi çizilecek/keşfedilecek sonucu önceden söylememelidir."]),
    "Tema 6": ("Nesnelerin Geometrisi (3) - simetri ve kodlama", TEAL,
               ["Simetri ekseni görünür kalmalı; eş noktalar eksene eş uzaklıkta kurulmalıdır.", "Katlama ve üst üste bindirme kararın matematiksel kanıtı olmalı; metin doğru cevabı ele vermemeli.", "Kodlama yalnız hedefe ulaşma değil geometrik plan/şekil oluşturma ile ilişkilendirilmelidir."]),
    "Tema 7": ("Olasılık ve Veriye Dayalı Araştırma", CORAL,
               ["Olasılık olayları açık koşullarla yazılmalı; 'olabilir' keyfî biçimde her zaman 5/10 kabul edilmemeli.", "Araştırma sorusu, hedef grup, çetele, sıklık, grafik ve yorum tutarlı tek veri döngüsü oluşturmalı.", "Grafik Hesap Makinesi'ndeki 5/2 kat hatası yayımdan önce düzeltilmelidir."]),
}


doc = BaseDocTemplate(str(OUT), pagesize=A4, rightMargin=MX, leftMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
                      title="4. Sınıf Matematik Oyunları - Ayrıntılı Düzeltmeler", author="Macera Akademi oyun incelemesi")
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

story = [Spacer(1, 16 * mm), P("MACERA AKADEMİ", cover_kicker),
         P("4. Sınıf Matematik Oyunları<br/>Ayrıntılı Düzeltmeler", cover_title),
         P("56 oyunun gerçek ekranları açılarak, ilk oynanışları denenerek ve kaynak görevleriyle karşılaştırılarak hazırlanmıştır.", cover_sub)]
cover_box = Table([[P("<b>Kapsam</b><br/>Bu belge 4. sınıf matematik listesindeki p01-p56 oyunlarının tamamını kapsar. Her oyun için denemede görülen durum, eğitimsel risk, yeni sahne ve oynanış, üç farklı tur, geri bildirim akışı ve ölçülebilir kabul koşulları verilir.")]], colWidths=[153 * mm])
cover_box.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), PALE_TEAL), ("BOX", (0,0), (-1,-1), 0.7, TEAL),
                               ("LEFTPADDING", (0,0), (-1,-1), 14), ("RIGHTPADDING", (0,0), (-1,-1), 14),
                               ("TOPPADDING", (0,0), (-1,-1), 13), ("BOTTOMPADDING", (0,0), (-1,-1), 13)]))
story += [cover_box, Spacer(1, 9 * mm), P("İnceleme yaklaşımı", h2)]
story += bullets(["4. sınıf profili seçilerek matematik listesindeki 56 oyunun tamamı tek tek açıldı; başlık, yönerge, sayaç, ilk sahne, kart konumu ve kontrol biçimi görsel olarak denendi.",
                  "Bant, radar, tren, köprü, roket, sayı tuş takımı, tepsi, terazi, geometri, simetri, kargo, çetele ve grafik motorları kaynak görevleriyle karşılaştırıldı.",
                  "Düzeltmeler yalnız eleştiri değildir; çocuk eylemi, matematiksel kanıt, üç turlu genelleme, yanlış geri bildirimi ve test edilebilir kabul eşiği birlikte yazıldı."])
story += [PageBreak()]

story += [P("Testten çıkan öncelikli bulgular", h1)]
story += [box("1. Kart kırpılması ve tema-motor uyuşmazlığı", ["Bant oyunlarının kartları sol kenardan kırpılıyor. Sıralama/simetri adımları roket-yakıt, açı/alan/tahmin görevleri tren, ip/açı döndürme görevleri kronometre motoruyla açılıyor."], PALE_CORAL, CORAL), Spacer(1,2*mm)]
story += [box("2. Cevabı başlangıçta veren ipuçları", ["Sayı Sarayı iki bölüğü hazır yazıyor; Pastane Siparişi bileşik kesrin bütün-parça çözümünü söylüyor; Tahmin Terazisi yuvarlanmış işlemi gösteriyor; bazı çizim oyunlarının açılış sesi keşfedilecek sonucu önceden açıklıyor."], PALE_GOLD, GOLD), Spacer(1,2*mm)]
story += [box("3. Matematikten çok motor yükü", ["Radar oyunlarında uzun soruyla hareketli kapsül eş zamanlı izleniyor. Robot Paketleme 42 dokunuş, Grafik Fabrikası hazır sayı kadar blok dokunuşu istiyor. Bu yükler kavramsal başarıyı kirletiyor."], PALE_BLUE, BLUE), Spacer(1,2*mm)]
story += [box("4. Yayımdan önce zorunlu içerik düzeltmeleri", ["Birim Dönüşüm Kartları 'her adım 10 ya da 1000' diyerek 1 m = 100 cm geçişini dışlıyor. Olasılık Ölçeği bütün 'olabilir' olayları 5/10'a sabitliyor. Grafik Hesap Makinesi 5/2 oranını kesin soruda 2 kabul ediyor; doğru değer 2,5'tir."], PALE_TEAL, TEAL)]
story += [PageBreak()]

story += [P("Bütün oyunlarda ortak uygulama standardı", h1)]
rows = [
    [P("Sahne", box_title), P("Başlıktaki ana nesne matematiksel eylemi gerçekten taşır; ortak tren/roket/kronometre motoru hikâyenin yerini almaz.", small)],
    [P("Tur", box_title), P("Her oyun en az üç değişen tur içerir; sayı, yön, şekil, veri veya temsil değişir.", small)],
    [P("Yönerge", box_title), P("Söylenen kontrol yöntemi gerçek dokunma, sürükleme, çizme ya da tuşlama davranışıyla birebir aynıdır.", small)],
    [P("İpucu", box_title), P("İlk ipucu doğru cevabı/işlemi vermez; model, basamak, ölçek veya stratejiye yönlendirir.", small)],
    [P("Yanlış", box_title), P("Yanlışta cevap söylenmez; hata kaynağı model üzerinde gösterilir ve çocuk yalnız ilgili adımı düzeltir.", small)],
    [P("Doğru", box_title), P("Doğru yanıt renk/konfetiden önce görsel veya sembolik matematiksel kanıtla doğrulanır.", small)],
    [P("Erişim", box_title), P("Kartlar karar verilene kadar tam görünür; en az 44 px dokunma hedefi, geri al ve gerektiğinde silgi sağlar.", small)],
    [P("Tutarlılık", box_title), P("Metin, ses, nesne sayısı, işlem, birim, grafik anahtarı ve sonuç aynı veriyi gösterir.", small)],
]
standards = Table(rows, colWidths=[28 * mm, 148 * mm])
standards.setStyle(TableStyle([("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#D8D4E2")), ("BACKGROUND", (0,0), (0,-1), PALE_PURPLE),
                               ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 8),
                               ("RIGHTPADDING", (0,0), (-1,-1), 8), ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7)]))
story += [standards, Spacer(1,5*mm)]
story += bullets(["Can sistemi kavramsal yanlış ile kartı kaçırma/küçük hedefe basamama hatasını ayırmalıdır.",
                  "Tahmin görevlerinde gerçek sonuç veya doğru sürgü konumu tahmin kaydedilmeden görünmemelidir.",
                  "Başarı yalnız ilk doğru seçimde değil üç tur ve kabul ölçütleri tamamlandığında kaydedilmelidir."])
story += [PageBreak()]

last_theme = None
accent_cycle = [CORAL, TEAL, GOLD, PURPLE]
for game in games:
    if game["theme"] != last_theme:
        last_theme = game["theme"]
        theme_name, accent, focus = THEMES[last_theme]
        theme_table = Table([[P(last_theme, badge), P(theme_name, theme_title)]], colWidths=[30*mm,146*mm], rowHeights=[50*mm])
        theme_table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), accent), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                                         ("ALIGN", (0,0), (0,0), "CENTER"), ("LEFTPADDING", (1,0), (1,0), 12),
                                         ("RIGHTPADDING", (1,0), (1,0), 12), ("ROUNDEDCORNERS", [10])]))
        story += [Spacer(1,22*mm), theme_table, Spacer(1,10*mm), P("Bu temadaki ana düzeltme odağı", h2)] + bullets(focus)
        story += [Spacer(1,6*mm), box("Tema kabul eşiği", ["Bu temadaki bütün oyunlar üç tur tamamlanmadan bitmiş sayılmayacak.", "Hikâye nesnesi, matematiksel işlem ve geri bildirim aynı sahnede birbirini destekleyecek."], PALE_TEAL, TEAL), PageBreak()]

    accent = accent_cycle[(game["n"] - 1) % len(accent_cycle)]
    story += [header(game["n"], game["title"], game["sub"], accent), Spacer(1,2.4*mm)]
    story += [box("Denemede görülen mevcut durum", game["observed"], PALE_CORAL, CORAL, True), Spacer(1,1.1*mm)]
    story += [box("Eğitimsel risk", game["risk"], PALE_GOLD, GOLD, True), Spacer(1,1.1*mm)]
    story += [P("Yeni sahne ve oynanış", h2)] + bullets(game["new"], bullet_small)
    story += [P("Üç farklı tur", h2), rounds_table(game["rounds"]), Spacer(1,1.1*mm)]
    story += [box("Geri bildirim ve bitiş", game["feedback"], PALE_TEAL, TEAL, True), Spacer(1,1.1*mm)]
    story += [box("Kabul ölçütü", game["acceptance"], PALE_BLUE, BLUE, True), PageBreak()]

story += [P("Son kabul kontrolü", h1), P("4. sınıf matematik bölümü tamamlanmadan önce", h2)]
story += bullets(["56 oyunun her biri üç farklı turla baştan sona oynanır; beklenen ve gerçekleşen sonuçlar kayıt altına alınır.",
                  "Başlık, sahne, yönerge, sayaç ve seslendirme aynı oyun metaforunu kullanır; ilgisiz tren, roket veya kronometre şablonu görünmez.",
                  "Bütün bant kartları ekranın ortasında sabit ve tam görünür; radar görevlerinde süre baskısız seçenek bulunur.",
                  "Kesir, birim, açı, simetri, olasılık ve grafik sonuçları ekrandaki gerçek modelle kanıtlanır.",
                  "Açılış sesleri cevabı önceden vermez; yanlış geri bildirimi cevabı söylemeden hata kaynağını gösterir.",
                  "Robot Paketleme gibi görevler gereksiz tekrar dokunuşu istemez; erişim hedefleri en az 44 px olur.",
                  "Birim dönüşümü geçişleri 10/100/1000 katsayılarıyla doğru, olasılık olayları açık koşullarla yazılmış olur.",
                  "Grafik Hesap Makinesi'nde 5/2 oranı 2 kabul edilmez; soru/veri kesin ve yaş düzeyine uygun biçimde düzeltilir."])
story += [Spacer(1,4*mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 4. sınıf matematik listesindeki p01-p56 oyunlarını kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, mekanik, tur, geri bildirim ve test gereksinimlerini ayrıntılı biçimde tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)
reader = PdfReader(str(OUT))
all_text = "\n".join(page.extract_text() or "" for page in reader.pages)
assert len(games) == 56
assert len(reader.pages) == 67, len(reader.pages)
assert all(game["title"] in all_text for game in games)
print(str(OUT))
print({"pages": len(reader.pages), "games": len(games), "bytes": OUT.stat().st_size})
