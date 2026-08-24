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
OUT = ROOT / "output/pdf/3_sinif_matematik_oyunlari_detayli_duzeltmeler.pdf"
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
body = ParagraphStyle("body", parent=base, fontName="Arial", fontSize=8.35, leading=10.85, textColor=INK, spaceAfter=1.0 * mm)
small = ParagraphStyle("small", parent=body, fontSize=7.6, leading=9.55, spaceAfter=0.75 * mm)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=4.7 * mm, firstLineIndent=-3.0 * mm, bulletIndent=0, spaceAfter=0.8 * mm)
bullet_small = ParagraphStyle("bullet_small", parent=small, leftIndent=4.7 * mm, firstLineIndent=-3.0 * mm, bulletIndent=0, spaceAfter=0.65 * mm)
h1 = ParagraphStyle("h1", parent=body, fontName="Arial-Bold", fontSize=21, leading=25, textColor=PURPLE, spaceAfter=4 * mm)
h2 = ParagraphStyle("h2", parent=body, fontName="Arial-Bold", fontSize=10.3, leading=12.4, textColor=TEAL, spaceBefore=1.3 * mm, spaceAfter=0.8 * mm)
cover_kicker = ParagraphStyle("cover_kicker", parent=body, fontName="Arial-Bold", fontSize=10, textColor=TEAL, alignment=TA_CENTER, spaceAfter=6 * mm)
cover_title = ParagraphStyle("cover_title", parent=body, fontName="Arial-Bold", fontSize=25, leading=30, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=5 * mm)
cover_sub = ParagraphStyle("cover_sub", parent=body, fontSize=12, leading=17, alignment=TA_CENTER, spaceAfter=9 * mm)
game_title = ParagraphStyle("game_title", parent=body, fontName="Arial", fontSize=13.6, leading=15.8, textColor=colors.white, spaceAfter=0)
badge = ParagraphStyle("badge", parent=body, fontName="Arial-Bold", fontSize=16, leading=17, textColor=colors.white, alignment=TA_CENTER, spaceAfter=0)
box_title = ParagraphStyle("box_title", parent=body, fontName="Arial-Bold", fontSize=9.3, leading=11.2, textColor=CORAL, spaceAfter=0.75 * mm)
round_head = ParagraphStyle("round_head", parent=small, fontName="Arial-Bold", fontSize=8.0, leading=9.3, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=0)
round_text = ParagraphStyle("round_text", parent=small, fontSize=7.15, leading=8.9, spaceAfter=0)
theme_title = ParagraphStyle("theme_title", parent=cover_title, fontSize=23, leading=28, textColor=colors.white)


def P(text, style=body):
    return Paragraph(text, style)


def bullets(items, style=bullet):
    return [Paragraph(item, style, bulletText="•") for item in items]


def header(number, title, subtitle, accent):
    table = Table(
        [[P(str(number), badge), P(f"<b>{title}</b><br/><font size='8' color='#F1EEF8'>{subtitle}</font>", game_title)]],
        colWidths=[15 * mm, 161 * mm], rowHeights=[19 * mm],
    )
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
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROUNDEDCORNERS", [6]),
    ]))
    return table


def rounds_table(items):
    table = Table(
        [[P("1. TUR", round_head), P("2. TUR", round_head), P("3. TUR", round_head)],
         [P(items[0], round_text), P(items[1], round_text), P(items[2], round_text)]],
        colWidths=[58.7 * mm, 58.7 * mm, 58.6 * mm],
    )
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
    canv.drawString(MX, 8.5 * mm, "3. Sınıf Matematik - Ayrıntılı Oyun Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 8.5 * mm, str(canv.getPageNumber()))
    canv.restoreState()


def G(n, theme, title, sub, observed, risk, new, rounds, feedback, acceptance):
    return dict(n=n, theme=theme, title=title, sub=sub, observed=observed, risk=risk,
                new=new, rounds=rounds, feedback=feedback, acceptance=acceptance)


games = [
G(1, "Tema 1", "Mega Uzay Çekirdeği", "1000'e kadar sayı temsilleri",
  ["Uzay sahnesi ve yakalayıcı görünür; fakat cevaplar yukarıdan hareketli kapsüller hâlinde düşüyor. İlk soruda 452 istenirken ekranda 542 gibi bir çeldirici sürekli hareket ediyor.", "Sayı adı, çözümleme ve rakam gösterimi arasında ilişki kurulmadan yalnız doğru etiketi yakalamak yeterli oluyor; yüzlük-onluk-birlik somut olarak görünmüyor."],
  ["Hareketli hedefi yakalama hızı, basamak değeri bilgisini gölgeleyebilir.", "Yanlışta yalnız ipucu metni verilirse 452 ile 542 arasındaki basamak değişimi çocuk tarafından görülmez."],
  ["Çekirdeğin çevresinde yüzlük enerji plakaları, onluk çubuklar ve birlik küreleri bulunsun.", "Çocuk önce 4 yüzlük, 5 onluk ve 2 birlik modülünü çekirdeğe sürükleyip 452'yi kursun.", "Ardından sayı adı, çözümleme ve rakam kartları sabit yuvalarda eşleştirilsin; yazılar hareket etmesin.", "Çekirdek ancak bütün gösterimler aynı sayıyı temsil ettiğinde dolsun; her basamak kendi rengiyle izlensin."],
  ["4 yüzlük + 5 onluk + 2 birlik; 400 + 50 + 2; dört yüz elli iki; 452 eşleştirilir.", "376 sayısı 3 yüzlük, 7 onluk, 6 birlik olarak kurulur; 367 ve 736 karşılaştırılır.", "763 için sayı adı verilir; çocuk önce modeli kurar, sonra rakam kartını seçer."],
  ["542 seçilirse yüzlük ve birlik modülleri yer değiştirerek kırmızı çerçeveyle gösterilsin.", "Doğru gösterimde modüller tek tek sayılıp işlem sesli okunmalı.", "Can kaybı yalnız kavramsal yanlışta olmalı; hareket eden nesneyi kaçırma değerlendirmeden çıkarılmalı."],
  ["Üç turda ekrandaki model, yazı, ses ve sonuç birebir aynı sayıyı gösterecek.", "Cevaplar en az 2 saniye sabit ve okunabilir olacak; başarı bütün temsil türleri tamamlanınca verilecek."]),

G(2, "Tema 1", "Altın Kubbe", "Esnek sayı çözümleme",
  ["Tapınak başlığına rağmen ana alan koyu bir dikdörtgen yük bölmesi gibi görünüyor; 100'lük, 10'luk ve 1'lik taşlara dokunmak yalnız toplam sayacını artırıyor.", "Hedef 348 tek örnek olarak veriliyor. '10 birlik oldu' ve '10 onluk oldu' değişimleri metinde anlatılıyor; taşların gerçekten birleşip değiştiği görülmüyor."],
  ["Çocuk esnek çözümlemeyi değil, 348'e ulaşan bir sayaç bulmacasını çözebilir.", "10 birlik = 1 onluk ve 10 onluk = 1 yüzlük ilişkisi görünür değişim olmadan ezber cümlesi olarak kalır."],
  ["Altın kubbenin kapısında üç gerçek kilit yuvası ve taşların yerleştiği raflar çizilsin.", "Her yüzlük büyük plaka, her onluk çubuk, her birlik küçük taş olarak tek tek görülsün ve sürüklensin.", "On birlik aynı yuvada birleşince animasyonla bir onluk taşa; on onluk da bir yüzlüğe dönüşsün. Ters değişim için taşı bölme düğmesi olsun.", "Kapı, yalnız hedef değer ve seçilen çözümleme aynı olduğunda açılsın; alternatif doğru çözümler kabul edilsin."],
  ["348 = 3 yüzlük + 4 onluk + 8 birlik olarak kurulur.", "348 = 2 yüzlük + 14 onluk + 8 birlik kurulur; çocuk 10 onluğu yüzlüğe çevirebilir.", "506 = 5 yüzlük + 0 onluk + 6 birlik; sıfır onluğun boş basamak olduğu açıklanır."],
  ["Fazla taşta yalnız 'geçti' denmemeli; hangi basamakta fazlalık olduğu vurgulanmalı.", "Değişim anında eşitlik korunmalı ve toplam sayaç değişmemeli.", "Doğru çözüm sonunda iki farklı çözümleme yan yana gösterilip değerlerinin aynı olduğu kanıtlanmalı."],
  ["Taş sayıları ekrandan gerçekten sayılabilecek ve değişim animasyonu geri alınabilecek.", "Her tur en az iki matematiksel olarak eşdeğer çözümü kabul edecek; hedef yalnız 348'le sınırlı kalmayacak."]),

G(3, "Tema 1", "Hızlı Tren Sinyalleri", "Onluğa ve yüzlüğe yuvarlama",
  ["Tren, tüneller ve sürgü başlıkla uyumlu; ancak seçenek tünelleri eşit aralıklı görünürken sayısal aralıklar eşit değildir: 640, 660, 670, 680, 700.", "674 için sürgü başlangıçta 670'e yakın konumda açılıyor; çocuk işlem yapmadan hazır konumu onaylayabilir."],
  ["Eşit olmayan değerlerin eşit aralıkla yerleştirilmesi sayı doğrusu algısını bozabilir.", "Başlangıç konumunun doğru cevaba yakın olması yuvarlama stratejisini değil onay düğmesini kullanmayı ödüllendirir."],
  ["Tüneller gerçek sayı doğrusu üzerinde değer farklarıyla orantılı aralıkta yerleştirilsin.", "Tren her tur rastgele güvenli bir başlangıç noktasında gelsin; sürgü doğru cevapta hazır durmasın.", "674'ün 670'e uzaklığı 4, 680'e uzaklığı 6 ray parçasıyla gösterilsin; yüzlüğe yuvarlamada 600 ve 700 uzaklıkları karşılaştırılsın.", "Tünel seçildikten sonra tren gerçek ray makasından geçsin ve yuvarlama gerekçesi sayı doğrusu üzerinde kalsın."],
  ["674 en yakın onluğa 670'e yönlendirilir; iki uzaklık görünür.", "674 en yakın yüzlüğe 700'e yönlendirilir; 600'e 74, 700'e 26 uzaklık karşılaştırılır.", "235 en yakın yüzlüğe 200'e gider; 250 sınır örneği ayrıca 'yarım ve üzeri yukarı' kuralıyla denenir."],
  ["Yanlış tünelde tren çarpışmamalı; iki hedefe uzaklık ölçülüp yeniden seçim verilmeli.", "Doğruda birler/onlar basamağı renklenirken sayı doğrusu da sonucu doğrulamalı.", "5 ile biten sınır durumunda kullanılan kural açıkça seslendirilmelidir."],
  ["Sayı doğrusu üzerindeki geometrik uzaklıklar sayısal farklarla orantılı olacak.", "Üç tur farklı başlangıç konumuyla oynanacak ve sürgü hiçbir turda otomatik olarak doğru cevaba yerleşmeyecek."]),

G(4, "Tema 1", "Sihirli Fasulye Sırığı", "Sekizer ritmik sayma",
  ["Fasulye yaprakları ve zıplayan karakter görünür; fakat doğru sıra arasına 14, 20, 28, 36 ve 48 gibi çeldiriciler aynı rota çizgisi üzerinde karışık yerleştirilmiş.", "Görev yalnız 0'dan 40'a ileri sekizer saymayı içeriyor; kazanımda belirtilen ileri-geri ve farklı büyüklükte ritmik sayma genellenmiyor."],
  ["Bağlantı çizgisi çeldiricileri de yolun parçası gibi gösterdiği için görsel rota matematiksel kuralla çelişiyor.", "Tek yön ve tek başlangıç, ritmik saymanın kuralını uygulamaktan çok doğru yaprak yerlerini ezberletir."],
  ["Fasulye sırığında yalnız seçildikçe oluşan dallar kullanılsın; henüz seçilmeyen yapraklar bağlantısız dursun.", "Her doğru zıplayışta +8 yayı ve önceki-yeni sayı birlikte gösterilsin.", "İkinci tur aşağı doğru -8, üçüncü tur 10'ar veya 100'er sayma ile bulut katları arasında ilerlesin.", "Çeldiriciler doğru sayıdan ±2, ±4 veya bir sonraki adım olacak; fakat rota çizgisi doğru cevabı önceden söylemeyecek."],
  ["0, 8, 16, 24, 32, 40 ileri sayılır.", "64, 56, 48, 40, 32 geri sekizer sayılır.", "320, 420, 520, 620, 720 yüzer sayılır; adım büyüklüğü çocuk tarafından seçilir."],
  ["14 seçilirse 8 + 8 modeli sekizli iki yaprak grubu olarak açılsın.", "Doğru zıplayışta karakter yalnız hedef yaprağa gider ve sayı sesli okunur.", "Tur sonunda çocuk kural kartını seçsin: her adımda +8, -8 veya +100."],
  ["Görsel bağlantılar yalnız doğru seçim sonrasında oluşacak.", "İleri, geri ve en az iki farklı adım büyüklüğü ayrı turlarda test edilecek."]),

G(5, "Tema 1", "Meyve Paylaşımı", "Tek ve çift sayıları keşfetme",
  ["İki çocuk kutusu ve 14 elma için otomatik 'her ikisine 1 elma ver' düğmesi bulunuyor; elmalar başlangıçta sepette görünmüyor.", "Oyun yalnız 14'ün hiç artmadan paylaşılmasını gösteriyor. Tek sayı örneği bulunmadığı hâlde başlık ve alt başlık tek-çift ayrımını vaat ediyor."],
  ["Çocuk dağıtımı kendisi yapmadan düğmeye basarak sonucu izler; eşit paylaştırma kararı ölçülmez.", "Yalnız çift örnek kullanılması, 'artarsa tek, artmazsa çift' kuralının karşılaştırmayla keşfedilmesini engeller."],
  ["Sepetteki bütün elmalar başlangıçtan itibaren görünür ve tek tek sürüklenebilir olsun.", "Çocuk iki tabağa sırayla birer elma dağıtsın; dengesiz dağıtımda oyun yönlendirici uyarı versin.", "Çift turda sepet boşalsın, tek turda ortada kalan bir elma belirginleşsin.", "Son aşamada çocuk TEK/ÇİFT kartını seçip gerekçeyi tamamlasın: iki eş gruba ayrıldı / bir tane arttı."],
  ["14 elma iki kişiye 7'şer paylaştırılır; artan yok, sayı çifttir.", "13 armut iki kişiye 6'şar verilir; 1 artar, sayı tektir.", "21 ve 22 için nesneleri tamamen dağıtmadan son basamağa dayalı tahmin yapılır, sonra modelle kontrol edilir."],
  ["Bir tabağa fazla nesne konursa yalnız o nesne geri dönsün ve eşitlik karşılaştırılsın.", "Doğru sonuçta iki grup sayılıp kalan bölmesi ayrıca gösterilsin.", "Tek/çift kuralı hem paylaşım modeli hem son basamak örüntüsüyle özetlensin."],
  ["En az bir tek ve bir çift sayı gerçek nesnelerle dağıtılacak.", "Otomatik dağıt düğmesi ana etkileşim olmayacak; çocuk nesneleri yerleştirip sınıflandıracak."]),

G(6, "Tema 1", "Tek-Çift Laboratuvarı", "Toplamların tek-çift yapısı",
  ["İşlem kartları yürüyen bantta geliyor ve TEK/ÇİFT kazanlarına dokunuluyor; sahne okunaklı olsa da kartlar hareket ederken işlem için süre baskısı oluşuyor.", "Sekiz öğenin çoğu sonucu çift olan işlemlerden oluşuyor; iki tek, iki çift ve tek-çift ilişkileri dengeli sayıda örneklenmiyor."],
  ["Okuma hızı veya hareketli karta yetişme, kural bilgisinden bağımsız can kaybına yol açabilir.", "Sonucu hesaplayıp kutuya atmak, tek+tek ve çift+çift yapısını nesne çiftleriyle açıklamayı garanti etmez."],
  ["Kart oyuncu karar verene kadar bant üzerinde sabitlensin; süreli mod isteğe bağlı üst seviye olsun.", "Her sayı çiftler hâlinde noktalarla gösterilsin; eşleşmeden kalan nokta tekliği temsil etsin.", "Çocuk önce iki terimin tek/çift etiketini, sonra toplamın sınıfını seçsin.", "Tur bitiminde üç kural tabloya kendiliğinden yazılmasın; çocuk örneklerden kural kartlarını yerleştirsin."],
  ["7 + 5 ve 9 + 9 ile TEK + TEK = ÇİFT keşfedilir.", "8 + 6 ve 4 + 10 ile ÇİFT + ÇİFT = ÇİFT gösterilir.", "9 + 4 ve 5 + 2 ile TEK + ÇİFT = TEK; çocuk işlem yapmadan önce tahmin eder."],
  ["Yanlış sınıfta iki terimin nokta modelleri yan yana getirilip kalan eşsiz nokta gösterilsin.", "Doğruda işlem sonucu ve genel kural birlikte okunmalı.", "Kartı kaçırmak can eksiltmemeli; kart tekrar sabit konumda gelmeli."],
  ["Üç ilişki türü eşit ağırlıkta ve en az ikişer örnekle test edilecek.", "Çocuk en az bir turda sonucu hesaplamadan önce yapısal tahmin yapacak."]),

G(7, "Tema 1", "Mimarlık Akademisi", "Şekil-sayı örüntüsü",
  ["Yeşil yaprak rotası üzerinde '3 blok, 4 blok, 5 blok...' gibi çeldiriciler gösteriliyor; gerçek kule, blok yerleştirme veya iskele görünmüyor.", "Doğru 3, 6, 9, 12, 15 dizisi seçiliyor; şeklin her adımda üç blok büyüdüğü yalnız metinle anlatılıyor."],
  ["Şekil ile sayı arasındaki ilişki kurulmadan yalnız +3 dizisi çözülebilir.", "Başlıktaki mimarlık eylemi yaprak zıplama motoruna dönüştüğü için kazanımın görsel örüntü boyutu kaybolur."],
  ["Her adım için yan yana büyüyen gerçek blok kuleleri çizilsin.", "Çocuk her yeni kata üç blok sürükleyip önceki yapıyla farkı görsün.", "Kule altındaki sayı kartı bloklar yerleştirildikten sonra yazılsın; şekil ve sayı aynı anda vurgulansın.", "Bir turda eksik yapı tamamlatılsın, bir turda sonraki yapı tahmin edilsin, bir turda kural sözel olarak seçilsin."],
  ["1-5. adımlar 3, 6, 9, 12, 15 blokla kurulur.", "Kural her adımda +4 olur; 4, 8, 12, 16 örüntüsünde eksik kule tamamlanır.", "Basamaklı yapı 2, 5, 8, 11 bloktur; çocuk 5. adımı çizer ve kuralı açıklar."],
  ["Yanlış blok sayısında fazla/eksik parçalar renklenmeli; doğru sayı doğrudan verilmemeli.", "Doğru yapıda yeni eklenen blok grubu ayrı renkte parlasın.", "Tur sonunda çocuk 'her adımda ... blok ekleniyor' cümlesini sayı kartıyla tamamlasın."],
  ["Kule her tur gerçek bloklardan oluşacak; yaprak zıplama şablonu kullanılmayacak.", "Sayı dizisi, şekil büyümesi ve sözel kural aynı artış miktarını gösterecek."]),

G(8, "Tema 1", "Kavanozdaki Misketler", "Stratejik tahmin",
  ["Tahmin oyunu tren tüneli motoruyla açılıyor; kavanozlar ve misket grupları görünmüyor. Sürgü ve 10-30-50-70-100 tünelleri var.", "İpucu 'küçük kavanoz 10 misket' diyor ancak küçük kavanoz ekranda olmadığı için çocuk görsel ölçü birimi kullanamıyor."],
  ["Tahmin gözleme değil, metin ve hazır aralığa dayalı sayı seçimine dönüşür.", "70 hedefi ±10 toleransla kabul edilirken gerçek sonucun 68 olduğu ancak açıklamada söylenir; tahmin stratejisi görünmez."],
  ["Yan yana küçük referans kavanozu ve büyük hedef kavanozu gerçek misket yoğunluğuyla çizilsin.", "Küçük kavanozdaki 10 misket sayılabilir; çocuk bu kavanozdan kaç tane sığacağını hayalet kopyalarla işaretlesin.", "Tahmin sürgüsü sayı doğrusu üzerinde olsun; tren ve tünel görseli kaldırılmalı.", "Onaydan sonra büyük kavanoz boşalıp misketler 10'arlı gruplara dizilsin; tahmin, gerçek sonuç ve fark aynı ekranda kalsın."],
  ["68 misket için 7 civarı onluk grup tahmin edilir; gerçek 68 açılır.", "Büyük misketli kavanozda yaklaşık 25 tahmin edilir; gerçek 23 sayılır.", "Farklı biçimli kavanozda referans grup 5 olur; çocuk şekil ve yoğunluğu hesaba katarak tahmin eder."],
  ["Uzak tahminde 'kaç referans kavanozu sığar?' sorusu sorulsun; cevap söylenmesin.", "Yakın tahmin, kesin eşitlik aramadan takdir edilsin ve fark hesaplatılsın.", "Açıklama sırasında misketler gerçekten sayılabilir gruplara ayrılmalı."],
  ["Tahmin öncesinde hem referans miktar hem hedef çokluk görünür olacak.", "Tren/tünel motoru yerine kavanozun kendisi matematiksel ölçme aracına dönüşecek."]),

G(9, "Tema 2", "Pizza Şefi", "Bütün, yarım ve çeyrek",
  ["Pizza tepsisi ve bütün/yarım/çeyrek/sekizde bir parçaları görünür; fakat 1/8 paleti kazanımın odağı dışında ve siparişlerde hiç kullanılmayan dikkat dağıtıcı olarak kalıyor.", "Müşteri fişi doğru parçayı metinle açıkça söylüyor; çocuk modelden kesri çıkarmak yerine etiketi okuyup aynı etikete dokunabiliyor."],
  ["Kesir temsili yerine sözcük eşleme ölçülebilir.", "Parçalar tepside birleşip bir bütün oluşturmadığı için 2 çeyrek = 1 yarım ve 4 çeyrek = 1 bütün ilişkisi yalnız yazıda kalabilir."],
  ["Sipariş fişinde önce görsel pizza modeli, sonraki turlarda kesir sembolü veya sözel ifade ayrı ayrı kullanılsın.", "Parçalar tepsiye sürüklenince gerçek bir daire üzerinde birleşsin; boşluk ve taşma görünür olsun.", "Siparişte kullanılmayan 1/8 ilk düzeyde kaldırılmalı; zenginleştirme turunda açıklanarak eklenmeli.", "Aynı miktar farklı parça bileşimleriyle hazırlanabilsin; tepsi doğru toplam değeri kontrol etsin."],
  ["1/2 siparişi bir yarım dilimle hazırlanır.", "2/4 siparişi iki çeyrekle hazırlanır ve 1/2 ile karşılaştırılır.", "1 bütün siparişi 2 yarım, 4 çeyrek veya 1/2 + 2/4 biçimlerinden biriyle hazırlanır."],
  ["Yanlış parçada tepside kalan boşluk/taşan bölüm gösterilsin; doğru etiket doğrudan söylenmesin.", "Doğru serviste parçalar birleşip bütün üzerindeki kapladığı alanı göstersin.", "Tur sonunda eşdeğer miktarlar üst üste bindirilerek doğrulansın."],
  ["Müşteri metni doğru palet etiketini aynen tekrar etmeyecek.", "Kesirlerin eşdeğerliği gerçek pizza alanı üzerinde kanıtlanacak; yalnız sayaç kontrolü yeterli olmayacak."]),

G(10, "Tema 2", "Çikolata Fabrikası", "Eş parçalar ve birim kesir",
  ["Başlık çikolata dese de oyun alanında kahverengi yuvarlak bir disk/pizza görünümü var; çikolata tabletinin dikdörtgen kareleri yok.", "Çocuk lazer çizgisi çekmiyor; 2'ye, 3'e, 4'e veya 8'e Böl düğmesinden birine basıyor. Yanlış seçimde paydanın cevabı doğrudan veriliyor."],
  ["Eş parçaya ayırma becerisi, payda kadar düğmeyi seçmeye indirgenir.", "3'e Böl çeldiricisi varken eş parçaların alanını kontrol etme olanağı bulunmadığı için 'eş' kavramı deneyimlenmez."],
  ["Kare bölmeli gerçek bir çikolata tableti ve sürüklenebilir yatay/dikey lazer cetveli kullanılsın.", "Çocuk kesme çizgilerini kendi yerleştirsin; eş olmayan parçalar alan kaplamasıyla karşılaştırılsın.", "Kesim sonrası her parça ayrılıp üst üste getirilerek eşlik doğrulansın.", "Birim kesir etiketi ancak bütünün kaç eş parçaya ayrıldığı ve tek parçanın seçildiği görüldükten sonra açılsın."],
  ["Tablet iki eş parçaya ayrılır; bir parça 1/2 olarak seçilir.", "Tablet dört eş parçaya ayrılır; 1/4 ve 2/4 modelleri oluşturulur.", "Sekiz karelik tablet 8 eş parçaya ayrılır; eş olmayan bir kesim düzeltilir."],
  ["Eş olmayan çizgide 'parçaların alanlarını karşılaştır' ipucu verilsin.", "Doğru kesimde parçalar üst üste gelmeli ve her birine 1/payda etiketi gelmeli.", "Kesim sayısı ile parça sayısı ayrımı doğru kurulmalı: dört parça için gereken çizgi düzeni modele göre değişir."],
  ["Çikolata görseli gerçek tablet biçiminde olacak; yuvarlak pizza diski kullanılmayacak.", "Çocuk en az iki turda kesme çizgisini kendisi yerleştirip eşliği görsel olarak doğrulayacak."]),

G(11, "Tema 2", "Kesir Asansörü", "Pay ve payda ilişkisi",
  ["Yönergede dikey cam asansör ve katlara çıkma anlatılıyor; gerçek oyun yatay tren, tüneller ve ray sürgüsü olarak açılıyor. İlerleme göstergesi de '0/3 tren' yazıyor.", "0, 3/10, 5/10 ve 1 bütün tünelleri eşit aralıklı görünürken kesir sayı doğrusu modeli ve on eş parça görünmüyor."],
  ["Asansör hikâyesiyle tren motoru arasındaki çelişki çocuğun neyi sürükleyeceğini karıştırır.", "On eş parçanın tamamı görünmediği için payda 10'un anlamı, yalnız açıklama metniyle verilir."],
  ["Gerçek dikey bir asansör kuyusu 0 ile 1 arasında on eş kata bölünsün.", "Bütün 10 aralık çizgisi görünür; kabin parmakla dikey sürüklenip katlara mıknatıslanır.", "Payda bütün kat sayısını, pay geçilen kat sayısını farklı renklerde göstersin.", "Tren, ray ve tünel öğeleri tamamen kaldırılıp ilerleme sayacı 'görev' olarak düzeltilsin."],
  ["3/10 katına çıkılır; üç aralık tek tek sayılır.", "7/10 katına çıkılır; 3/10 ile uzaklık karşılaştırılır.", "10/10'a çıkılır ve 1 bütün eşitliği görsel olarak kurulur."],
  ["Yanlış katta kabin kalmalı; zemin ile seçilen kat arasındaki aralıklar sayılmalı.", "Doğru katta pay/payda açıklaması kat şeması üzerinde gösterilmeli.", "Seslendirme 'üç bölü on' demeli; tünel veya tren sözcüğü kullanmamalı."],
  ["Ekranda tam on eş aralık görünecek ve kabin gerçek dikey eksende hareket edecek.", "Başlık, yönerge, ilerleme etiketi, görsel motor ve ses aynı asansör metaforunu kullanacak."]),

G(12, "Tema 2", "Zaman Kulesi", "Analog ve dijital saat",
  ["Saat yüzü, hedef zaman ve dört ok düğmesi görünür; yönerge ise akrep ile yelkovanı parmakla çevirmeyi söylüyor.", "İbreler başlangıçta 12.00'de. 14.45 hedefinde akrebin 2 ile 3 arasında olması gerekirken düğme tabanlı motorun ara konumu nasıl kurduğu çocuk tarafından görülmüyor."],
  ["Yönerge-girdi çelişkisi doğru bilgiye rağmen başarısızlığa yol açabilir.", "Akrep yalnız saat rakamına kilitlenirse 09.30, 06.15 ve 14.45 gibi zamanlar analog olarak hatalı gösterilebilir."],
  ["Akrep ve yelkovan uçlarından doğrudan sürüklenebilir olsun; seçilen ibre farklı renkte parlasın.", "Yelkovan hareket ettikçe akrep orantılı biçimde sürekli ilerlesin; 45 dakikada iki ile üç arasının dörtte üçüne gelsin.", "Dijital hedef, günlük dil ve analog model üç ayrı kartta eşleştirilsin.", "Ok düğmeleri erişilebilirlik alternatifi olarak kalacaksa yönerge bunu açıkça söylesin."],
  ["14.45 ayarlanır; yelkovan 9'da, akrep 2 ile 3 arasında olur.", "09.30 ayarlanır; yelkovan 6'da, akrep 9 ile 10'un tam ortasındadır.", "06.15 ve 12.00 art arda ayarlanır; çeyrek geçe ve tam saat karşılaştırılır."],
  ["Yanlış onayda ibrelerin doğru konumu gösterilmemeli; hangi ibrenin dakika/saat olduğu sorulmalı.", "Doğruda analog, dijital ve sözel zaman aynı anda okunmalı.", "İbre konumları matematiksel olarak sürekli hesaplanmalı; akrep tam sayıya yapışmamalı."],
  ["Yönerge ile gerçek kontrol yöntemi aynı olacak.", "Dört hedefin tamamında akrep, geçen dakika oranına göre iki saat arasında doğru açıda bulunacak."]),

G(13, "Tema 2", "Zaman Tüneli Bandı", "Zaman birimi dönüşümleri",
  ["Dönüşüm kartları yürüyen bantta, 7-12-24-52-60 kutuları altta bulunuyor; kart metni bazen ekranın solundan kırpılmış biçimde geliyor.", "1 yıl = 52 hafta ifadesi kesin eşitlik gibi sunuluyor; takvim yılı yaklaşık 52 hafta + 1 gün olduğundan bağlam belirtilmiyor."],
  ["Kırpılan kartlar okuma hatasını matematik hatası gibi cezalandırabilir.", "Yaklaşık ilişkiyi tam eşitlik olarak öğretmek kavramsal yanlışa yol açar; ayrıca sayı kutuları birim etiketinden yoksundur."],
  ["Kart karar verilene kadar orta alanda sabit dursun ve iki satırdan fazla kırpılmasın.", "Kutularda yalnız 7, 12 gibi sayı değil '7 gün', '12 ay', '24 saat', '60 dakika/saniye' yazsın.", "Yıl-hafta ilişkisi 'yaklaşık 52 hafta' biçiminde sunulsun veya 365 gün = 52 hafta + 1 gün modeli gösterilsin.", "Dönüşüm sonrası takvim/saat görseli açılarak birimler gerçek gruplar hâlinde sayılabilsin."],
  ["1 hafta = 7 gün ve 1 yıl = 12 ay eşleştirilir.", "1 gün = 24 saat, 1 saat = 60 dakika, 1 dakika = 60 saniye dönüştürülür.", "365 gün = 52 hafta + 1 gün modeliyle yaklaşık ilişki açıklanır; artık yılda +2 gün gösterilir."],
  ["Yanlış kutuda sayı ve birim birlikte karşılaştırılsın; kart hemen kaybolmasın.", "Doğru eşlemede görsel gruplar kısa animasyonla sayılmalı.", "Kartı kaçırmak can götürmemeli; süre baskısı isteğe bağlı olmalı."],
  ["Bütün kutular sayı + birim etiketi taşıyacak.", "Yıl-hafta ifadesi matematiksel olarak doğru nitelikte, 'yaklaşık' veya kalan gün bilgisiyle verilecek."]),

G(14, "Tema 2", "Kronometre Arenası", "Süre tahmini",
  ["Kronometre, yatay hedef şeridi ve basılı tut düğmesi görünür; motor hedef sayıyı ve işaretli bölgeyi baştan açıkça gösteriyor.", "100 metreyi yaklaşık 10 saniye koşma örneği çoğu 3. sınıf öğrencisi için gerçekçi kişisel deneyim değildir; İstiklal Marşı'nın ilk kıtası için 15 saniye iddiası tempo değişimine bağlıdır."],
  ["Hedef zaten gösterildiğinde çocuk süre tahmini değil, ilerleyen çubuğu işarete getirme refleksi kullanır.", "Kişiden kişiye değişen eylemler tek doğru süreyle değerlendirilirse geçerli olmayan yargı oluşur."],
  ["İlk aşamada hedef sayı ve işaret kapalı olsun; çocuk eylemin süresini tahmin edip sayısal tahminini girsin.", "İkinci aşamada kronometre gerçek zamanla çalışsın; çocuk eylemi canlandırırken başlatıp durdursun.", "Kişisel hızdan bağımsız kısa eylemler seçilsin veya kabul aralıkları açıkça yaklaşık olarak verilsin.", "Tahmin-gerçek ölçüm-fark üçlü kartı sonunda gösterilsin; yalnız hedef şeridine yetişme oyunu olmasın."],
  ["Adını yazma süresi önce tahmin edilir, sonra gerçek kronometreyle ölçülür.", "10 kez el çırpma süresi tahmin ve ölçümle karşılaştırılır.", "Kısa bir yönergeyi okuma süresi her çocuk için ölçülür; sınıf sonuçlarının değişebileceği konuşulur."],
  ["Tahmin uzaksa can eksilmemeli; tahmin ile ölçüm arasındaki fark gösterilmeli.", "Doğruya yakın tahmin aralıkla değerlendirilmeli; tek milisaniye hedefi kullanılmamalı.", "Bitişte 'süre kişiye ve koşula göre değişebilir' açıklaması eklenmeli."],
  ["Hedef ölçümden önce görünmeyecek; tahmin bağımsız olarak kaydedilecek.", "En az iki turda gerçek kronometre ölçümü ve tahmin farkı raporlanacak."]),

G(15, "Tema 2", "Ölçüm İstasyonu", "Uygun uzunluk ve kütle birimi",
  ["Nesne kartları bantta gelirken cm, m, km, kg ve ton kutuları aynı sırada bulunuyor; gram kutusu yok olmasına rağmen ipucunda gram-kilogram-ton ilişkisi yazıyor.", "Uzunluk ve kütle birimleri aynı beşli satırda, nicelik türü ayrılmadan seçiliyor; kartlar ekranın solunda kısmen kırpılabiliyor."],
  ["Çocuk önce neyin ölçüldüğünü ayırt etmeden yalnız nesne-birim eşini ezberleyebilir.", "Gramın anlatılıp seçeneklerde bulunmaması ve uzunluk-kütlenin karışık sunulması kavramsal sınıflamayı zayıflatır."],
  ["İlk karar 'uzunluk mu, kütle mi?' olarak iki büyük istasyonda verilsin.", "Sonra ilgili istasyonda cm-m-km veya g-kg-ton ölçeği üzerinde uygun büyüklük seçilsin.", "Nesneler sabit ve tam görünür olsun; gerçekçi referans çizimleriyle karşılaştırılabilsin.", "Gram seçeneği eklenip kalem/silgi kütlesi gibi örnekler kullanılsın; birim ailesi renklerle ayrılmalı."],
  ["Kalem boyu cm, sınıf tahtası m, şehirler arası yol km olarak seçilir.", "Silgi kütlesi g, çocuk/karpuz kg, kamyon/gemi ton olarak sınıflanır.", "Aynı nesne için nicelik değiştirilir: kalemin boyu cm, kütlesi g; soru kökü dikkatle okunur."],
  ["Yanlış aile seçilirse önce 'uzunluk mu kütle mi?' sorusuna geri dönülsün.", "Doğru birimde nesne yaklaşık sayısal değerle birlikte gösterilsin.", "Kartı kaçırma can kaybı yaratmamalı ve metin hiçbir kenarda kırpılmamalı."],
  ["Gram, kilogram ve ton üçlüsü seçenek ve örneklerde eksiksiz bulunacak.", "Her turda nicelik türü ile birim seçimi iki ayrı öğrenme adımı olarak kaydedilecek."]),

G(16, "Tema 2", "Banka Gişesi", "Parada eşdeğerlik",
  ["Gişe ve para paleti görünür; ancak müşteri 'yalnız 5 TL'liklerle' derken 25 kr, 50 kr, 1 TL ve 10 TL düğmeleri de ekranda etkin görünmeye devam ediyor.", "Para görselleri küçük ve değerleri çoğunlukla etiketten okunuyor; seçilen paralar tepside fiziksel olarak sıralanıp gruplanmıyor."],
  ["Görev kısıtını okumayan çocuk yasak para türlerini deneyerek gereksiz hata alabilir.", "Aynı değerin farklı para gruplarıyla oluşturulması yerine sayaç toplamına ulaşma alışkanlığı gelişebilir."],
  ["Müşterinin izin verdiği para çekmeceleri açık, diğerleri kapalı ve neden kapalı olduğu görünür olsun.", "Paralar tepsiye sürüklenince gerçek yüzleriyle yan yana kalsın; 100 kuruş grupları çerçevelensin.", "Tek tür zorunluluğundan sonra serbest eşdeğer ödeme turu eklenip birden fazla çözüm kabul edilsin.", "Kuruş ve TL toplamı çift gösterimle yazılsın: 250 kr = 2 TL 50 kr."],
  ["10 TL yalnız iki 5 TL banknotla ödenir.", "1 TL iki 50 kuruş veya dört 25 kuruşla iki ayrı turda kurulur.", "2 TL 50 kuruş için 1 TL, 50 kr ve 25 kr paralarıyla iki farklı doğru bileşim üretilir."],
  ["Yasak para seçilemez; yalnız açıklayıcı kilit geri bildirimi verir.", "Fazla ödemede son para geri alınabilir ve hedefe kalan/fazla miktar gösterilir.", "Doğru ödemede paralar 1 TL gruplarına ayrılıp eşdeğerlik sesli okunur."],
  ["Her turda tepsideki para adedi, kuruş toplamı ve TL gösterimi birebir tutarlı olacak.", "En az bir hedef iki farklı doğru para bileşimiyle tamamlanabilecek."]),

G(17, "Tema 3", "Zihin Arenası", "Tahminî ve gerçek sonucu ilişkilendirme",
  ["Uzayda düşen sayı kapsülleri ve kalkan yakalayıcı kullanılıyor; işlem metni uzun olduğu için çocuk hem okumak hem hareketli hedefi izlemek zorunda kalıyor.", "342 + 279 için önce yaklaşık 600, sonra gerçek 621 soruluyor; ancak iki sonuç aynı sayı doğrusu veya hata payı üzerinde yan yana karşılaştırılmıyor."],
  ["Motor becerisi ve okuma hızı, zihinden işlem/tahmin performansına karışır.", "Tahmin ile gerçek sonuç arasındaki 21 fark görünmediğinde 'tahminin makullüğü' değerlendirilmeden iki ayrı cevap ezberlenebilir."],
  ["Arena ortasında sabit işlem panosu, iki aşamalı 'tahmin' ve 'kesin sonuç' hedefleri bulunsun.", "Çocuk sayıları yüzlüğe yuvarlarken 342'nin 300'e, 279'un 300'e gidişini sayı doğrularında işaretlesin.", "Gerçek işlem onluk-birlik parçalama veya basamak tablosuyla çözülsün; seçenekler hareket etmesin.", "Sonunda 600 ve 621 aynı eksende işaretlenip aralarındaki 21 birimlik fark ve tahminin yakınlığı yorumlansın."],
  ["342 + 279 yaklaşık 600, gerçek 621; fark 21 olarak bulunur.", "498 + 205 yaklaşık 700, gerçek 703; tahminin çok yakın olduğu görülür.", "612 - 287 yaklaşık 300, gerçek 325; toplama ve çıkarma tahminleri karşılaştırılır."],
  ["Yanlış yuvarlamada ilgili sayı doğrusu açılıp komşu yüzlükler gösterilsin.", "Kesin sonuç yanlışa düştüğünde elde/bozma yapılan basamak vurgulansın.", "Başarı yalnız iki cevabı bulunca değil, tahmin-gerçek farkını yorumlayınca verilsin."],
  ["Hareketli sayı kapsülleri ana cevap yöntemi olmayacak.", "Her tur tahmin, kesin sonuç, fark ve 'makul mü?' değerlendirmesini eksiksiz içerecek."]),

G(18, "Tema 3", "Akıllı Asansör", "Toplama ve çıkarmanın tersliği",
  ["Oyun başlığı ve yönergesi asansörü anlatırken gerçek sahne yatay tren tünelleri, ray ve sürgüden oluşuyor; ilerleme etiketi '0/4 tren' yazıyor.", "150 + 40 ve 190 - 40 sonuçları ayrı tünel seçimi olarak yapılıyor; kabinin yukarı çıkıp aynı yolu geri dönmesi görünmüyor."],
  ["Ters işlem ilişkisini taşıması gereken fiziksel geri dönüş metaforu kayboluyor.", "Eşit aralıklı görünen 130, 150, 170, 190, 210 tünelleri yalnız seçenek sırası hâline gelebilir."],
  ["Dikey ve numaralı gerçek asansör kuyusu çizilsin; 150'den 190'a çıkan yol mavi, dönüş kırmızı iz bıraksın.", "Kabin +40 için dört onluk adımı yukarı, -40 için aynı dört adımı aşağı hareket etsin.", "İkinci çiftte 80 + 25 ve 105 - 25, beşlik ara işaretlerle gösterilsin.", "Tren/tünel öğeleri ve 'tren' sayacı kaldırılıp 'görev' etiketi kullanılmalı."],
  ["150 + 40 = 190; ardından 190 - 40 = 150 ile başlangıca dönülür.", "80 + 25 = 105; 105 - 25 = 80 aynı güzergâhta gösterilir.", "240 - 60 = 180; ters işlem 180 + 60 = 240 olarak bu kez aşağıdan yukarı doğrulanır."],
  ["Yanlış katta başlangıç, hareket miktarı ve seçilen kat arasındaki fark işaretlensin.", "Doğru dönüşte iki yol izi üst üste gelerek tersliği kanıtlasın.", "Her çift sonunda aynı üç sayı ile iki ters işlem yan yana yazılmalı."],
  ["Görsel motor gerçekten asansör olacak ve dikey hareket kullanacak.", "Her turda ileri işlem ile tersi aynı başlangıç/varış noktaları üzerinde doğrulanacak."]),

G(19, "Tema 3", "Uzay Kargo Bandı", "10 ve 100 ile çarpma-bölme",
  ["İşlem kartları bantta, 'sağa 1/2 sıfır ekle' ve 'sağdan 1/2 sıfır sil' kutuları altta görünüyor; küçük ekranda kutu etiketleri sıkışıyor.", "Kural yalnız sıfır ekleme/silme olarak sunuluyor; basamak değerlerinin 10 veya 100 kat değişmesi açıklanmıyor."],
  ["Sıfır ekle/sil kestirmesi, sıfırla bitmeyen bölme durumlarına veya ondalık öğrenimine taşındığında yanlış genellemeye dönüşebilir.", "Kartı bantta yakalama baskısı uzun etiketleri okumayı zorlaştırır."],
  ["Kargo kutuları yüzlük-onluk-birlik basamak tablosunda sağa/sola kaydırılsın.", "45 × 10 işleminde 4 onluk 4 yüzlüğe, 5 birlik 5 onluğa geçsin; 450'nin neden oluştuğu görülmeli.", "Bölmede rakamlar bir basamak sağa kayarken boş basamakta sıfırın yer tutucu rolü gösterilsin.", "Kural kutuları kısa ve matematiksel olsun: ×10, ×100, ÷10, ÷100; açıklama karar sonrası açılsın."],
  ["45 × 10 = 450 ve 45 × 100 = 4500 basamak kaymasıyla kurulur.", "600 ÷ 100 = 6 ve 320 ÷ 10 = 32 tablo üzerinde gösterilir.", "70 × 10 ve 700 ÷ 10 ters çift olarak çözülür; sonuçların ilişkisi açıklanır."],
  ["Yanlış mühürde kart kaybolmamalı; basamak tablosu üzerinde deneme sonucu gösterilmeli.", "Doğruda 'sıfır ekledik' yerine 'basamak değeri 10 katına çıktı' da seslendirilmelidir.", "Bant, oyuncu karar verene kadar durabilmeli."],
  ["Her işlem basamak değeri modeliyle doğrulanacak.", "Kestirme, kapsamı belirtilmeden genel bir 'sıfır silme' kuralı olarak öğretilmeyecek."]),

G(20, "Tema 3", "Şeker Çiftliği", "Çarpma ve bölmenin ilişkisi",
  ["Sekiz boş kutu, her kutu için 0/4 sayaç ve dokunma düzeni görünür; şekerler kutuların içinde başlangıçta görünmüyor.", "Çocuk kutulara sırayla dokunarak otomatik doldurma yapıyor; 8 × 4 = 32 ve 32 ÷ 8 = 4 ilişkisi ancak son mesajda açıklanıyor."],
  ["Eş gruplar gerçek nesnelerle kurulmadığında çarpma, kutu düğmelerine basma dizisine dönüşür.", "Bölmeyle sağlama ayrı ve geç bir düğme olarak kalırsa ters ilişki aynı model üzerinde deneyimlenmez."],
  ["32 şeker banttan gelsin ve çocuk sekiz kutuya dörder sürüklesin; her kutuda nesneler sayılabilir olsun.", "Kutu doldukça 4, 8, 12 ... 32 ritmik sayma şeridi oluşsun.", "Çarpma ifadesi aynı kutuların altında 8 grup × 4 olarak kurulsun; sonra kutular bozulmadan 32 ÷ 8 = 4 yazılsın.", "Grup sayısı ve grup büyüklüğü sonraki turlarda değişsin; fazla/eksik grup bulunabilsin."],
  ["8 kutuya 4'er şeker: 8 × 4 = 32; 32 ÷ 8 = 4.", "6 sepete 5'er elma: 6 × 5 = 30; 30 ÷ 5 = 6 ilişkisi de incelenir.", "24 şeker 4 kutuya eşit dağıtılır; çocuk hem 4 × 6 hem 24 ÷ 4 = 6 ifadelerini seçer."],
  ["Fazla/eksik nesnede yalnız ilgili kutu vurgulanmalı; tüm düzen silinmemeli.", "Doğruda aynı görsel model üzerinde çarpma ve iki bölme sağlaması gösterilmeli.", "Çocuk şekerleri gerçekten yerleştirmeden başarı verilmemeli."],
  ["Her kutudaki nesneler ayrı ayrı görünür ve sayılabilir olacak.", "Çarpma ile bölme aynı gruplar korunarak üç turda iki yönlü ilişkilendirilecek."]),

G(21, "Tema 3", "Labirent Robotu", "Yönergeyi işlem diline dönüştürme",
  ["Robot ve sayılı kapılar görülüyor; fakat sahne gerçek labirent yerine fasulye sırığı/yaprak rotası motorunun yeşil basamaklı yolunu kullanıyor.", "Her adımda doğru sonuç kapısına dokunmak yeterli; robotun 12'den başlama, ×3, +14 gibi işlemleri bir program şeridinde uyguladığı görünmüyor."],
  ["İşlem zinciri, ayrı sonuç seçimlerine bölünerek bileşenlerin sıralı bağı zayıflar.", "Yanlış kapılar yol çizgisi üzerinde olduğundan görsel rota matematiksel yönergeyi temsil etmez."],
  ["Duvarları, kapıları ve başlangıç sayısı ekranı olan gerçek robot laboratuvarı çizilsin.", "Yönerge kartları sırayla program şeridine yerleştirilsin: 12 ile başla, 3 ile çarp, 14 ekle.", "Her çalıştırmada robot bir istasyona gidip mevcut sayacını güncellesin; ara sonuçlar kaybolmasın.", "İkinci görevde çocuk sözel yönergeyi işlem sembollerine, üçüncüde işlem zincirini sözel yönergeye dönüştürsün."],
  ["12 × 3 = 36, ardından 36 + 14 = 50 zinciri uygulanır.", "20 ÷ 4 = 5, ardından 5 + 7 = 12 uygulanır.", "Başlangıç 30; 5 çıkar, 3 ile çarp: (30 - 5) × 3 = 75. Parantez ve sıra görsel istasyonlarla anlatılır."],
  ["Yanlış programda robot doğru kapıya taşınmamalı; hatalı blok kırmızı olup ara sonuç gösterilmeli.", "Doğruda aktif program bloğu ve robotun sayacı aynı anda ilerlemeli.", "Bitişte çocuk işlem zincirini baştan sona sesli okuyabilmeli."],
  ["Yaprak/fasulye motoru kaldırılıp gerçek labirent ve program şeridi kullanılacak.", "Her turda tüm ara sonuçlar, görsel konumlar ve nihai kapı matematiksel olarak tutarlı olacak."]),

G(22, "Tema 3", "Doğa Dedektifleri", "Verilerden problem kurma",
  ["Kamp hikâyesi yerine roket ve yakıt hunisi kullanılıyor; dört hazır kart roket çevresinde duruyor.", "Kartlardan biri çözümü '3 × 4 = 12' olarak hazır veriyor. Çocuk problemi üretmek yerine önceden yazılmış cümleleri doğru sıraya dokunuyor."],
  ["Problem oluşturma kazanımı, sıralama ve okuma görevine indirgenir.", "Çözüm baştan verildiği için hangi işlemin neden seçildiği gerekçelendirilmez."],
  ["Gerçek kamp alanında üç çadır ve her çadırda dört çocuk modeli gösterilsin.", "Çocuk verilen veri kartlarından gerekli olanları seçsin; gereksiz bir ayrıntıyı dışarıda bırakabilsin.", "Soru kökü ve işlem çocuktan gelsin: kelime kartlarıyla problem cümlesi kurulsun, ardından model üzerinden çözüm seçilsin.", "Roket-yakıt motoru kaldırılmalı; kamp nesneleri problemin verilerini gerçekten temsil etmeli."],
  ["3 çadır, her çadırda 4 çocuk: toplam çocuk sayısı için problem kurulur.", "5 ağaçta 3'er kuş, 2 kuş uçuyor: iki işlemli bir problem oluşturulur.", "12 sandviç 4 gruba eşit paylaştırılır; aynı veriden bölme sorusu ve çarpma kontrolü kurulur."],
  ["Eksik problemde 'kim, kaç grup, her grupta kaç?' kontrol kartları açılmalı.", "Gereksiz veri seçildiğinde neden kullanılmadığı tartıştırılmalı; doğrudan çözüm verilmemeli.", "Doğru problem sonunda sahnedeki nesneler işlemle birebir sayılmalı."],
  ["Çözüm kartı başlangıçta seçenekler arasında bulunmayacak.", "Çocuk en az iki turda soru cümlesini ve işlemi kendisi oluşturacak; yalnız sıralama yeterli olmayacak."]),

G(23, "Tema 3", "Kozmik Tahterevalli", "Eşitliğin anlamı",
  ["Kozmik terazi, 8 × 3 sol kefesi ve sabit işlem seçenekleri görünür; görsel motor konuya büyük ölçüde uyuyor.", "İlk turda 15 + 9, 30 - 6 ve 6 × 4 olmak üzere üç doğru seçenek bulunuyor; ancak oyun tek blok mu yoksa birden fazla doğru ifade mi beklediğini açık söylemiyor."],
  ["Birden fazla doğru varken tek seçim beklenirse doğru matematiksel düşünme cezalandırılabilir.", "Kefe eğimi yalnız dekor olursa seçilen işlemin sayısal farkını açıklamaz."],
  ["Görev dili 'eşit olan bütün işlemleri bul' veya 'bir doğru işlem seç' diye kesinleştirilsin.", "Her işlem kartına dokunulduğunda sonucu küçük nesne grubu veya sayı doğrusu üzerinde açılabilsin.", "Kefe açısı seçilen değer ile hedef arasındaki farka orantılı değişsin.", "Bir turda çoklu doğru seçimi, bir turda eksik sayı, bir turda iki kartın toplamıyla denge kurma kullanılsın."],
  ["8 × 3 = 24 için 15 + 9, 30 - 6 ve 6 × 4 olan tüm doğru işlemler işaretlenir.", "36 ÷ 3 = 12 için 5 + 7, 4 × 3 ve 24 ÷ 2 karşılaştırılır.", "7 × 5 = 35; ardından 20 + ? = 35 için eksik 15 bloğu eklenir."],
  ["Yanlış değerde iki tarafın sonuçları görünmeli ve kefe fark kadar eğilmeli.", "Doğruda eşittir işareti ortada parlayıp iki değeri sesli okumalı.", "Çoklu doğru turunda bir doğru bulunca oyun bitmemeli; kalan eşdeğer ifadeler istenmeli."],
  ["Beklenen doğru cevap sayısı yönergede açık olacak.", "Görsel denge açısı ve yazılı değerler bütün seçimlerde aynı sayısal ilişkiyi gösterecek."]),

G(24, "Tema 3", "Fırıncının Tezgâhı", "Kısa ve verimli işlem stratejisi",
  ["Fırıncı müşterisi, tepsi ve 1 simit/12'lik tepsi seçenekleri görünür; ilk sipariş metni doğru yolu '4 tepsi × 12' diye baştan söylüyor.", "Çocuk tepsi düğmesine dört kez dokunarak 48'e ulaşıyor; uzun ve kısa yolu karşılaştırmadan en iyi strateji hazır biçimde veriliyor."],
  ["Strateji seçme kazanımı, verilen algoritmayı uygulamaya dönüşür.", "12'lik tepside gerçek 12 simit görünmezse çarpma yine sayaç artışı olarak algılanabilir."],
  ["İlk ekranda yalnız sipariş ve iki paketleme aracı görünsün; çözüm yolu çocuk tarafından seçilsin.", "12'lik tepside on iki simit 3 × 4 düzeninde gerçekten görünsün; tek simitler ayrı sürüklensin.", "İki doğru yol tamamlandıktan sonra dokunma/nesne sayısı ve süre karşılaştırılsın.", "İpucu kademeli olsun: önce 'daha büyük grupları kullan', sonra gerekirse 12'nin katları gösterilsin."],
  ["48 simit 4 adet 12'lik tepsiyle paketlenir; tek tek yolun 48 adım olduğu karşılaştırılır.", "30 simit 2 tepsi + 6 tek olarak hazırlanır; 48 - 18 işlemi modelle doğrulanır.", "41 simit 3 tepsi + 5 tek olarak hazırlanır; çocuk başka doğru ama daha uzun yolu da değerlendirir."],
  ["Doğru ama uzun yol yanlış sayılmamalı; 'doğru, daha kısa yol bulabilir misin?' denmeli.", "Her tepsi açıldığında içindeki 12 simit sayılabilir olmalı.", "Bitişte kullanılan grup sayısı, tekler ve toplam aynı denklemde gösterilmeli."],
  ["Sipariş metni çözümü önceden vermeyecek.", "En az iki turda birden fazla doğru yöntem kabul edilip verimlilik ayrı ölçüt olarak değerlendirilecek."]),

G(25, "Tema 4", "3D Geometri Tarayıcısı", "Küpün köşe, ayrıt ve yüzleri",
  ["Küp tel kafesi ve sekiz köşe noktası görünür; ancak açılış sesinde 'küpün sekiz köşesi vardır, şimdi ayrıtları tara' denerek ilk görevin cevabı ve sonraki aşama baştan açıklanıyor.", "Köşeler önden/arkadan aynı büyüklükte noktalarla gösteriliyor; ayrıt ve yüz modlarının nasıl seçileceği ekranda başlangıçta belirgin değil."],
  ["Cevabın sesli verilmesi keşfetme ve sayma görevini geçersizleştirir.", "2B tel kafeste arka/ön ilişkisi ve yüzlerin seçilebilir alanları açık değilse dokunma hataları geometri hatası gibi sayılabilir."],
  ["Açılış sesi yalnız 'bütün köşeleri bul' demeli; sayı sonucunu çocuk tamamlamadan söylememeli.", "Küp parmakla döndürülebilir 3B model olsun; seçilen köşe, ayrıt veya yüz kalıcı renk alsın.", "Arkadaki öğeler görünürlük için döndürülmeli; görünmeyen noktaya tahmini dokunma istenmemeli.", "Son aşamada küp açınımı açılıp altı yüz tek tek eşleştirilsin; terim tanımları keşiften sonra verilsin."],
  ["Küpün 8 köşesi döndürülerek taranır ve sayılır.", "12 ayrıt renklenir; iki yüzün birleştiği çizgi olduğu model üzerinde gösterilir.", "6 yüz küp ve açınım üzerinde eşleştirilir; kare yüzlerin hepsi sayılır."],
  ["Aynı öğeye ikinci dokunma sayacı artırmamalı; 'bunu buldun' geri bildirimi vermeli.", "Eksik öğede model doğru cevabı açmadan eksik bölgeyi döndürmeye teşvik etmeli.", "Tamamlamada 8-12-6 özeti, çocuğun taradığı renkli model üzerinde görünmeli."],
  ["İlk seslendirme cevap sayılarını vermeyecek.", "Model her öğeyi yalnız bir kez sayacak ve döndürme ile bütün köşe/ayrıt/yüzler erişilebilir olacak."]),

G(26, "Tema 4", "Şekil Kalesi", "Çokgenleri kenar sayısına göre sınıflama",
  ["Şekiller bantta gelirken üçgen, dörtgen, beşgen, altıgen ve sekizgen kapıları altta bulunuyor; ilk kart ekranın solundan kısmen kırpılmış görünebiliyor.", "Düzenli çokgenler ağırlıklı; içbükey, düzensiz veya farklı oranlı dörtgenler kullanılmıyor."],
  ["Kırpılan şekil kenar saymayı imkânsızlaştırabilir.", "Yalnız prototip düzenli şekiller kullanılırsa çocuk şekil adını genel özellikten değil görünüş kalıbından öğrenir."],
  ["Şekil karar verilene kadar ekran merkezinde sabit ve bütünüyle görünür dursun.", "Çocuk parmağıyla kenarları tek tek izlesin; her izlenen kenar numaralansın.", "Düzenli/düzensiz, dönmüş ve farklı boyutta çokgenler aynı sınıfa gönderilsin.", "Kapılar yalnız ad değil kenar sayısı ve küçük örneklerle açıklansın; süreli bant üst düzey seçeneğe dönüşsün."],
  ["Dönmüş üçgen, kare/dikdörtgen ve düzensiz dörtgen sınıflanır.", "Düzensiz beşgen, altıgen ve sekizgen kenarları izlenerek adlandırılır.", "İçbükey beşgen ile açık çizgi karşılaştırılır; kapalı şekil ve kenar koşulu tartışılır."],
  ["Yanlış kapıda şekil kaybolmamalı; kenarlar çocukla birlikte sayılmalı.", "Doğruda şekil döndürülüp sınıfının değişmediği gösterilmeli.", "Kartı kaçırmak can kaybı olmamalı ve şekil ekran sınırında kırpılmamalı."],
  ["Her şekil tamamı görünür ve en az 44 px dokunma alanında olacak.", "Üç turda düzenli, düzensiz, dönmüş ve en az bir içbükey çokgen bulunacak."]),

G(27, "Tema 4", "Köşegen Dedektifi", "Kare ve dikdörtgende köşegen",
  ["Kare, A-B-C-D noktaları ve 'iki köşeye sırayla dokun' mekanizması görünür; konuya uygun bir çizim motoru kullanılıyor.", "Açılış seslendirmesi 'karenin iki köşegeni vardır ve uzunlukları eşittir' diyerek görev sonucunu çocuk çizmeden önce veriyor."],
  ["Keşif sorusu, cevabı tekrarlama etkinliğine dönüşür.", "Yalnız izin verilen doğru parçaların kabulü, çocuğun kenar ile köşegen farkını gerekçelendirmesini sağlamayabilir."],
  ["Açılışta sayı verilmeden 'komşu olmayan köşeleri birleştir' denilsin.", "Çocuk iki noktayı seçince çizgi gerçekten oluşsun; komşu seçimde kenar ve köşegen farkı gösterilsin.", "Çizilen iki köşegen orta noktada kesişsin; uzunluklar cetvel veya üst üste getirme ile karşılaştırılsın.", "Üçgen karşı örneği eklenip neden köşegen bulunmadığı komşuluk ilişkisiyle açıklansın."],
  ["Karede A-C ve B-D köşegenleri keşfedilir ve ölçülür.", "Dikdörtgende K-M ve L-N çizilir; iki köşegenin eşitliği doğrulanır.", "Üçgende her köşe diğer iki köşeye komşudur; köşegen olmadığı çocuk tarafından açıklanır."],
  ["Komşu nokta seçiminde çizgi kenar rengine dönüşüp neden köşegen olmadığı söylenmeli.", "Doğru çizgiler kalıcı olmalı ve kesişim noktası vurgulanmalı.", "Cevap sayısı ve eşitlik bilgisi ancak çizim/ölçümden sonra açılmalı."],
  ["Açılış sesi sonucu vermeyecek.", "Kare ve dikdörtgen köşegen uzunlukları aynı ölçme yöntemiyle doğrulanacak; üçgen karşı örneği tamamlanacak."]),

G(28, "Tema 4", "Geometri Stüdyosu", "Araç kullanarak şekil çizme",
  ["Noktalı zemin ve numaralı köşeler görünür; çocuk iki noktaya dokunarak hazır kenarları oluşturuyor.", "Başlık 'cetvelle şekil çiz' dese de ekranda cetvel/gönye aracı yok; üçgen, kare ve altıgenin bütün noktaları ve doğru bağlantıları önceden belirlenmiş."],
  ["Çizim aracı kullanma kazanımı, bağlantı çiftlerini seçmeye indirgenir.", "Hazır noktalar şeklin boyut ve yönünü tamamen belirlediği için ölçme, dik açı ve eş kenar kontrolü yapılmaz."],
  ["Dijital cetvel ekrana sürüklenip iki nokta arasında hizalanmalı; çizgi cetvel kenarından çekilmeli.", "Kare turunda gönye ile dik açı kontrolü, eş kenar göstergesi ve uzunluk ölçümü kullanılmalı.", "Serbest nokta ızgarasında çocuk köşeleri kendisi seçebilsin; yalnız doğru kenarlar önceden kodlanmasın.", "Şekil tamamlandıktan sonra kenar/köşe sayısı ve kullanılan araç raporlanmalı."],
  ["Üç nokta seçilip cetvelle üçgen çizilir; farklı üçgenler kabul edilir.", "Dört eş kenar ve dört dik açı koşuluyla kare çizilir; dikdörtgen çeldirici karşılaştırılır.", "Altıgen için altı köşe serbest ızgarada belirlenir; kapalı olma ve altı kenar koşulu denetlenir."],
  ["Yanlış bağlantı silinebilir olmalı; tüm çizim baştan başlamamalı.", "Karede eş kenar veya dik açı eksikse hangi ölçütün sağlanmadığı belirtilmeli.", "Doğruda çizim üzerinde cetvel/gönye işaretleri kısa süre kalmalı."],
  ["Cetvel ve gönye gerçek etkileşim aracı olarak kullanılacak.", "En az bir turda köşe yerleri çocuk tarafından seçilecek ve şekil özellikleri ölçülerek doğrulanacak."]),

G(29, "Tema 4", "Çevre Avcıları", "Çevreyi tahmin etme ve ölçme",
  ["Oyun tren tüneli ve sürgü motoruyla açılıyor; kitap, silgi dizilimi veya cetvel görünmüyor.", "İlk soruda kenarlar 4 ve 3 silgi olarak zaten verildiği için 14 sonucu tahmin değil, 4 + 3 + 4 + 3 işlemiyle kesin hesaplamadır."],
  ["Tahmin kazanımı ile kesin işlem birbirine karışır.", "Tren metaforu çevre ölçme eylemini taşımadığı için bütün kenarları dolaşma fikri görünmez."],
  ["Gerçek kitap resmi ve kenar boyunca dizilebilen silgi birimleri kullanılsın.", "Tahmin aşamasında kenar sayıları verilmesin; çocuk görsel büyüklüğe bakıp yaklaşık sayı seçsin.", "Ölçüm aşamasında silgiler boşluk/üst üste binme olmadan dört kenara yerleştirilsin.", "İkinci tur standart cetvelle cm ölçülsün; tren, tünel ve ray görselleri kaldırılmalı."],
  ["Görsel kitaba yaklaşık 14 silgi tahmin edilir; sonra kenarlara dizilip gerçek sonuç bulunur.", "20 cm × 15 cm dikdörtgenin çevresi cetvelle ölçülüp 70 cm hesaplanır.", "Düzensiz çokgenin çevresi önce tahmin edilir, sonra her kenar ölçülüp toplamla karşılaştırılır."],
  ["Uzak tahminde ceza verilmemeli; tahmin ve gerçek sonuç farkı hesaplanmalı.", "Ölçümde her kenar tamamlanmadan sonuç açılmamalı.", "Doğru hesap kitap çevresinde dolaşan renkli çizgiyle kanıtlanmalı."],
  ["Tahmin aşamasında kesin kenar uzunlukları gösterilmeyecek.", "Gerçek ölçme nesne/araç üzerinde yapılacak; tren motoru kullanılmayacak."]),

G(30, "Tema 4", "İp Dolama Serüveni", "Eğri çevreyi ip ile ölçme",
  ["Yönerge konserve kutusunun tabanına ip dolamayı anlatıyor; gerçek oyun kronometre motoru, saat kadranı ve yatay süre şeridi gösteriyor.", "Çocuk basılı tutarak 1,0 'tur' değerine ulaşmaya çalışıyor; kutu, ip yolu ve ipin cetvelde açılması görünmüyor."],
  ["Çevre ölçme deneyimi, zaman çubuğunu hedefte bırakma refleksine dönüşür.", "1 tur kavramının fiziksel yol ve 24/36 cm ip uzunluğuyla ilişkisi kurulmaz."],
  ["Ortada silindir konserve ve kenarında başlangıç mandalı olan gerçek ip çizilsin.", "Çocuk ip ucunu kutunun çevresinde parmağıyla sürüklesin; iz tam turda başlangıca ulaşsın.", "Fazla/eksik dolama görsel olarak üst üste binen veya açık kalan ip ile görülsün.", "Tam tur ipi düz bir cetvel üzerine taşınıp santimetre değeri gerçek uzunlukla ölçülsün; kronometre kadranı kaldırılmalı."],
  ["Küçük kutu çevresine ip dolanır ve açıldığında 24 cm ölçülür.", "Büyük kutuda aynı işlem 36 cm verir; iki ipin uzunluğu karşılaştırılır.", "Düzensiz yaprak sınırı ip ile izlenir; ip açılıp cetvelle yaklaşık çevre bulunur."],
  ["İp başlangıca ulaşmadıysa açık kalan bölüm gösterilmeli; sayısal cevap tek başına verilmemeli.", "Tam turda ip kesilip düzleştirilmeli ve cetvel sıfırdan başlanarak okunmalı.", "Bitişte nesne büyüklüğü ile çevre uzunluğu arasındaki ilişki iki ip üst üste getirilerek gösterilmeli."],
  ["Kutu, ip ve cetvel gerçek etkileşimin parçası olacak.", "Basılı tutulan süre çubuğu ölçme yerine geçmeyecek; çevre fiziksel iz ve uzunlukla doğrulanacak."]),

G(31, "Tema 4", "Sıvı Laboratuvarı", "Litre tahmini ve ölçme",
  ["Musluk ve litre etiketleri bulunsa da ana görsel kronometre kadranı ve yatay süre şeridi; dereceli sürahi görünmüyor.", "Hedef 3 L baştan işaretli ve çocuk çubuğu bu çizgide bırakıyor. Bu, sıvı miktarını tahmin etmekten çok zamanlama görevidir."],
  ["Litre, kapta yükselen hacim yerine yatay ilerleme değeri olarak yanlış temsil edilir.", "Hedef görünürken bağımsız tahmin oluşmaz; hızlı akış yalnız motor becerisini zorlaştırır."],
  ["Şeffaf dereceli sürahi, musluk ve gerçek yükselen su seviyesi kullanılmalı.", "Önce işaretsiz kapta çocuk 3 L'nin yerini tahmin çizgisiyle koysun; sonra dereceler açılsın.", "Musluk basılı tutulduğunda su seviyesi kap geometrisine uygun yükselsin; yatay kronometre kaldırılmalı.", "Ölçüm sonrası su 1 litrelik kaplara aktarılıp litre sayısı bağımsız olarak doğrulansın."],
  ["3 L seviyesi tahmin edilir, doldurulur ve üç 1 L kapla doğrulanır.", "4 L farklı biçimli geniş kapta tahmin edilir; aynı litre için seviye yüksekliği değişir.", "2 L dar ve geniş kapta karşılaştırılır; miktarın kap şekliyle değişmediği gösterilir."],
  ["Taşma ceza yerine gözlem fırsatı olmalı; fazla su geri alınabilsin.", "Tahmin çizgisi ölçüm boyunca kalsın ve fark litre cinsinden gösterilsin.", "Doğru sonuç su seviyesi, derece çizgisi ve 1 L kaplarla üçlü doğrulanmalı."],
  ["Litre yatay zaman şeridiyle temsil edilmeyecek.", "Her turda gerçek kap seviyesi, derece ve toplam miktar matematiksel olarak tutarlı olacak."]),

G(32, "Tema 4", "Mozaik Atölyesi", "Şekillerle tasarım ve çevre",
  ["Üçgen, kare, beşgen ve altıgen parçaları ile sipariş tepsisi görünür; ancak şekiller gerçek mozaikte birleşmiyor.", "'Ev' için üçgen çevresi 18 + kare çevresi 16 = 34 cm deniyor. Parçalar kenardan birleşirse ortak kenar dış çevreden çıkar; bireysel çevreleri toplamak birleşik şeklin çevresini vermez."],
  ["Bu hesap birleşik şekillerde çevre konusunda doğrudan matematiksel yanlışa yol açabilir.", "Çocuk şekilleri yerleştirmeden etiketlerde yazan çevreleri toplayarak görevi tamamlar."],
  ["Şekiller kareli mozaik zeminde gerçek konumlara sürüklensin ve ortak kenarlar görünür olsun.", "Birleşik şeklin çevresi yalnız dış sınır boyunca renkli ip ile izlenip birim kenarlar sayılarak bulunsun.", "Ayrı parçaların çevre toplamı ile birleşik şeklin çevresi karşılaştırılsın; ortak kenarın iki kez çıkarıldığı somutlaştırılsın.", "Sipariş tepsisi yerine ev/petek/roket silueti gerçek parçalarla oluşmalı."],
  ["Kare üstüne üçgen çatı yerleştirilir; ortak kenar ölçüsü hesaba katılarak dış çevre bulunur.", "Üç eş altıgen yan yana petek oluşturur; yalnız dış kenarlar sayılır.", "İki kare ve iki üçgenden roket kurulur; çocuk dış sınırı işaretleyip çevreyi hesaplar."],
  ["Parçaların bireysel çevrelerini toplamak doğru kabul edilmemeli; ortak kenarlar vurgulanmalı.", "Doğru çözümde yalnız dış sınır kalın çizgiyle dolaşılmalı.", "Bitişte 'birleşince içte kalan kenarlar çevreye dahil değildir' açıklaması eklenmeli."],
  ["Bütün çevre sonuçları yerleşim geometrisine göre yeniden hesaplanacak.", "Her turda mozaik gerçekten kurulacak ve dış sınır üzerinde ölçme/sayma ile doğrulanacak."]),

G(33, "Tema 5", "Katlama Laboratuvarı", "Simetri doğrularını keşfetme",
  ["Kare ve sekiz sarı nokta görünür; çizgi oluşturma motoru konuya uygundur. Ancak açılış sesi 'karenin dört simetri doğrusu vardır: iki orta çizgi ve iki köşegen' diyerek bütün cevabı baştan veriyor.", "Daire turunda yalnız seçilmiş dört çap çizdirilip sonuçta 'sayısız' deniyor; sınırlı örnek ile sonsuz/sayısız olasılık arasındaki geçiş deneyimlenmiyor."],
  ["Keşif, verilen dört çizgiyi kopyalama görevine dönüşür.", "Çocuk, dikdörtgen köşegenlerinin neden simetri doğrusu olmadığını gerçek katlama veya üst üste bindirme olmadan ezberleyebilir."],
  ["Açılışta sayı ve tür verilmeden 'katlandığında iki tarafı çakıştıran bütün çizgileri bul' denilsin.", "Çocuk çizgiyi seçince şekil gerçekten katlanıp iki yarı saydam olarak üst üste gelsin.", "Dikdörtgen köşegeni denendiğinde köşelerin örtüşmediği animasyonla kanıtlansın.", "Dairede merkezden geçen farklı açılarda yeni çaplar serbestçe çizilsin; her yeni açının da çalışması sayısızlığı somutlaştırsın."],
  ["Karede dikey, yatay ve iki köşegen olmak üzere 4 doğru keşfedilir.", "Dikdörtgende yalnız dikey ve yatay orta çizgi kabul edilir; köşegen karşı örnek olarak katlanır.", "Dairede en az altı farklı merkezden geçen doğru denenir; her çapın simetri doğrusu olduğu genellenir."],
  ["Yanlış çizgide cevap söylenmeden katlama sonucu ve örtüşmeyen bölge gösterilsin.", "Doğru çizgiler kalıcı renk alsın ve yeni çizgi öncekiyle karıştırılmasın.", "Sayı sonuçları ancak çocuk çizip katladıktan sonra özetlenmeli."],
  ["Açılış sesi cevapları vermeyecek.", "Her doğru/yanlış yargı gerçek katlama veya üst üste bindirme animasyonuyla doğrulanacak."]),

G(34, "Tema 5", "Aynadaki İkizler", "Simetri parçalarının eşliği",
  ["Yarım kelebek benzeri şekil ve dikey ayna çizgisi görünür; ancak seçenekler gerçek parça görselleri yerine metin düğmeleridir.", "Doğru seçenek 'Eş parça (aynı boyut, aynadaki gibi)' diyerek kendini açıkça tanımlar; çocuk şekil, boyut ve yön karşılaştırması yapmadan doğru metni seçebilir."],
  ["Görsel eşlik kazanımı okuduğunu anlama sorusuna dönüşür.", "'Dönmüş parça' ile 'yansımış parça' arasındaki yön farkı gerçek şekiller olmadan anlaşılamaz."],
  ["Üç seçenek gerçek vektör parçalar olarak yan yana gösterilsin: doğru yansıma, döndürülmüş ve ölçeği küçültülmüş parça.", "Çocuk parçayı ayna ekseninin sağına sürüklesin; kaynakla eş noktalar ince çizgilerle bağlansın.", "Doğru parça eksen boyunca kapanıp yarımla tam şekil oluştursun.", "Metin ipuçları seçimden önce cevabı söylememeli; boyut, biçim, eksene uzaklık ve yön ayrı ölçütler olarak incelenmeli."],
  ["Yarım kelebek için doğru yansımış kanat seçilir.", "Asimetrik yaprak yarısının ayna görüntüsü döndürülmüş çeldiriciden ayrılır.", "Renkli noktalı yarım şekil yansıtılır; hem dış sınır hem nokta konumları eşleşir."],
  ["Yanlışta kaynak ve seçim yarı saydam üst üste getirilip uyuşmayan kısım gösterilsin.", "Doğruda eksene eş uzaklıktaki nokta çiftleri parlasın.", "Bitişte 'eş ama yönü aynaya göre ters' ifadesi görselle birlikte açıklansın."],
  ["Seçeneklerin üçü de gerçek şekil görseli olacak; metin doğru cevabı ele vermeyecek.", "Doğru yansıma dış sınır, boyut ve iç ayrıntılar bakımından eksene göre hesaplanarak eşleşecek."]),

G(35, "Tema 5", "Kilim Dokuma Tezgâhı", "Dikey simetri ile deseni tamamlama",
  ["8 × 6 ızgara, pembe dikey eksen, verilen renkli sol desen ve renk paleti görünür; konu ile motor uyumlu.", "Yönergede önce renk seçip aynadaki kareye dokunmak gerekiyor; çok sayıda hücrede tek tek renk seçmek tekrarlı ve hata düzeltme aracı görünmüyor."],
  ["Renk paletini her hücrede yeniden seçme yükü simetri düşüncesinden fazla zaman alabilir.", "Yanlış hücrede yalnız 'simetrik eş değil' demek, eksene uzaklık sayma stratejisini görünür kılmaz."],
  ["Bir kaynak hücreye dokunulduğunda eksene uzaklığı sütun adımlarıyla sayılmalı; karşı hücrede hayalet hedef belirsin.", "Renk seçimi kalıcı kalem gibi davranmalı; silgi/geri al düğmesi eklenmeli.", "Kolay turda kaynak-karşı hücre çifti, orta turda bütün yarım desen, zor turda birkaç yanlış dokunmuş hücreyi düzeltme kullanılmalı.", "Tamamlanınca kilim ortadan katlanıp iki yarının üst üste geldiği gösterilmeli."],
  ["Tek renkli 4 hücre eksene göre yansıtılır.", "Mevcut 6 satırlık çok renkli kilim bütünüyle tamamlanır.", "Tamamlanmış görünen kilimde üç hatalı hücre bulunur; eksene uzaklık ve renk kontrolüyle düzeltilir."],
  ["Yanlış hücrede kaynak ve hedef sütun adımları işaretlenmeli; doğru hücre doğrudan doldurulmamalı.", "Doğru her çiftte kısa bir ayna çizgisi oluşmalı.", "Bitişte katlama animasyonu bütün eş hücreleri üst üste getirmeli."],
  ["Geri al/silme bulunacak ve yanlış dokunma kalıcı olmayacak.", "Her renkli kaynak hücrenin tam bir ve yalnız bir simetrik eşi doğru koordinatta bulunacak."]),

G(36, "Tema 5", "Satranç Tahtası Macerası", "Simetrik konum bulma",
  ["A-H ve 1-8 etiketli tahta ile dikey eksen görünür; ancak şövalyeler küçük gri noktalar gibi çiziliyor ve satranç taşı kimliği kayboluyor.", "İpucu '(B4 → G4)' ilk eşlerden birinin koordinatını doğrudan veriyor; çocuk uzaklığı kendi bulmadan örneği kopyalayabilir."],
  ["Küçük işaretlerin görünürlüğü ve koordinat okuma yükü simetri bilgisini gölgeleyebilir.", "Hazır eşleme örneği ilk hedefi ele verir; kalanlar konum ezberine dönüşebilir."],
  ["Kaynak karelerde belirgin şövalye rozetleri ve eksen boyunca katlama gölgesi kullanılsın.", "Çocuk önce sütun/ sıra koordinatını sesli veya kartla belirlesin, sonra eksene olan sütun uzaklığını saysın.", "Hedef işaretleri başlangıçta verilmesin; doğru kareye dokunulduğunda yansıyan şövalye oluşsun.", "İpucu belirli cevabı değil yöntemi söylesin: eksenden kaç sütun uzaktaysa diğer tarafta da o kadar."],
  ["B4'ün dikey eksene göre eşi G4 bulunur.", "A2-H2 ve C7-F7 çiftleri farklı uzaklıklarda tamamlanır.", "Eksen yataya çevrilir; C7'nin yatay simetriğinde C2 bulunur ve iki eksen karşılaştırılır."],
  ["Yanlış karede kaynak ile seçilen karenin eksene uzaklıkları sayılıp karşılaştırılmalı.", "Doğru karede yansıma oku ekseni geçerek hedefe ulaşmalı.", "Küçük telefon ekranında taş ve hücre hedefleri yeterli boyutta olmalı."],
  ["Şövalyeler nokta değil ayırt edilebilir taş simgesi olarak görünecek.", "İpucu hiçbir turun gerçek kaynak-hedef koordinat çiftini önceden vermeyecek."]),

G(37, "Tema 5", "Kodlama Dedektifi", "Simetrik yönergeyi uygulama",
  ["Izgara, robot, hedef, engeller, yön düğmeleri ve program şeridi görünür; ilk yönerge 2 sağ, 3 aşağı, 1 sol olarak eksiksiz yazılı.", "İkinci turun simetrik rotası da 2 sol, 3 aşağı, 1 sağ biçiminde doğrudan veriliyor; çocuk simetri dönüşümünü üretmeden kopyalayabilir."],
  ["Yönerge takip becerisi çalışsa da simetrik yönerge oluşturma kısmı pasif kalır.", "Program hatasında bütün şeridin silinmesi gerekirse hata ayıklama yükü artar."],
  ["İlk tur verilen program uygulanarak mekanik öğrenilsin.", "İkinci turda ilk program sol tarafta görünürken simetrik program boş bırakılmalı; çocuk sağ ve sol blokları dönüştürsün.", "Aktif komut çalıştırmada parlasın; hata olduğunda program korunup yalnız hatalı blok düzenlenebilsin.", "Eksen ızgarada açıkça çizilmeli ve başlangıç/hedef hücreleri gerçekten birbirinin simetriği olmalı."],
  ["2 sağ, 3 aşağı, 1 sol yönergesi uygulanır.", "Simetrik başlangıçta çocuk 2 sol, 3 aşağı, 1 sağ programını kendisi kurar.", "Yeni rota 1 aşağı, 4 sağ, 2 yukarıdır; yatay simetride aşağı-yukarı dönüşümü üretilir."],
  ["Engele çarpınca hangi komutun çarpışmaya yol açtığı kırmızı olsun.", "Hedefe ulaşmayan programda kalan satır/sütun farkı gösterilsin.", "Doğruda orijinal ve simetrik program blokları çiftler hâlinde bağlansın."],
  ["En az iki turda simetrik yönerge çocuk tarafından üretilecek; hazır metin kopyalanmayacak.", "Program düzenleme tek blok bazında yapılabilecek ve eksen dönüşümü koordinatlarla tutarlı olacak."]),

G(38, "Tema 5", "Simetri Mimarı", "Simetrik yönerge kurgulama",
  ["Başlık 'yönergeyi kendin kurgula' diyor; gerçek ekran yalnız ızgara, başlangıç, hedef ve engelleri gösteriyor. İncelenecek sol taraftaki çizim ayrı bir görsel olarak görünmüyor.", "İpucu '3 aşağı, 3 sola, 2 aşağı' diye yolu büyük ölçüde veriyor; görev simetri kurmaktan engeller arasında rota bulmaya kayıyor."],
  ["Referans şekil olmadan hangi yapının simetrisinin istendiği anlaşılamaz.", "Hedefe ulaşan herhangi bir rota, simetrik olmasa da oyun tarafından kabul edilebilir; kazanım rota planlama ile karışır."],
  ["Ortada eksen, sol tarafta tamamlanmış renkli referans rota ve sağda boş yansıma ızgarası bulunsun.", "Çocuk referans rotanın her bölümünü eksene göre dönüştürerek komut şeridini kendisi yazsın.", "Engeller simetri görevini destekliyorsa iki tarafta da simetrik yerleşmeli; keyfî labirent engeli olmamalı.", "Çalıştırma sonunda iki rota aynı anda çizilip eksenden katlandığında üst üste gelmeli."],
  ["Sol rota 3 aşağı, 2 sağ; dikey simetriği 3 aşağı, 2 sol olarak kurulur.", "Basamaklı L rotasının yatay simetriği aşağı-yukarı dönüşümüyle yazılır.", "Çocuk kendi kısa rotasını solda çizer, sistem sağdaki komutlarını yazmasını ister ve katlayarak denetler."],
  ["Hedefe ulaşsa bile simetrik olmayan rota kabul edilmemeli; hücre çiftleri karşılaştırılmalı.", "Yanlışta ilk sapma noktası ve referanstaki eş hücre gösterilmeli.", "Doğruda iki rota eksen boyunca katlanıp tam örtüşmeli."],
  ["Referans çizim her tur ekranda görünür olacak.", "Başarı yalnız hedefe ulaşmaya değil, bütün rota hücrelerinin simetri koşulunu sağlamasına bağlı olacak."]),

G(39, "Tema 5", "Kalite Kontrol Bandı", "Şekillerde simetriyi denetleme",
  ["Harf kartları bantta ve SİMETRİKTİR/HATALIDIR kutuları altta; kart ilk girişte ekranın solundan kısmen kırpılabiliyor.", "A, H, M ve T'nin simetrik sayılması kullanılan yazı tipine bağlıdır. Kart üzerinde gerçek pembe simetri ekseni görünmüyor; yalnız yönergede söyleniyor."],
  ["Font değişikliği doğru cevabı tartışmalı hâle getirebilir.", "Ekseni görmeden harf adına göre ezberlenen karar, gerçek katlama ve örtüşme yargısı değildir."],
  ["Harfler sistem fontu yerine sabit vektör çizimleri olarak uygulamaya gömülsün.", "Her kartta denetlenecek dikey veya yatay eksen açıkça çizilsin.", "Karar sonrası kart eksenden katlanıp iki yarı üst üste bindirilsin; uyuşan/uyuşmayan alanlar gösterilsin.", "Harflerin yanında geometrik motifler de kullanılarak font bağımlılığı azaltılsın; kart karar verilene kadar sabit dursun."],
  ["Sabit vektör A, H ve T dikey eksende denetlenir.", "P, R, L ve S aynı eksende simetrik değildir; katlamayla kanıtlanır.", "Kelebek, vazo ve ok motiflerinde eksen yönü değiştirilerek simetri yargısı yapılır."],
  ["Yanlış kararda kart katlanıp uyuşmayan bölüm kırmızı gösterilmeli.", "Doğruda iki yarı saydam olarak tam çakışmalı.", "Kartın ekrana girişte kırpılması veya hareketi can kaybına yol açmamalı."],
  ["Harf geometrileri sabit vektör olacak ve test edilen eksen görünür kalacak.", "Her karar gerçek üst üste bindirme sonucu ile doğrulanacak."]),

G(40, "Tema 5", "Mozaik Ustası", "Yatay ve dikey eksende simetri",
  ["6 × 6 ızgara, yatay/dikey pembe eksenler ve sol üstte dört renkli hücre görünür; konu ile etkileşim genel olarak uyumlu.", "Yönerge her kaynak hücrenin üç yere yansıyacağını söylüyor; ancak eksen üzerindeki hücre veya tek/çift boyutlu ızgara durumları açıklanmıyor ve geri alma görünmüyor."],
  ["Çift eksen dönüşümünde kaynak, dikey eş, yatay eş ve çapraz eş koordinatları karışabilir.", "Yanlış renkte/hücrede düzeltme olmaması uzun görevde motor hatasını ağırlaştırır."],
  ["Kaynak hücre seçilince üç simetrik hedefe ince renkli kılavuz çizgileri gitsin; çocuk yine kendisi doldursun.", "Renk kalemi kalıcı seçilsin; silgi ve geri al bulunmalı.", "İkinci turda bazı yansımalar hazır, bazıları yanlış olsun; çocuk denetleyip düzeltsin.", "Tamamlandığında desen önce dikey, sonra yatay katlanarak dört bölgenin eşliği ayrı ayrı doğrulansın."],
  ["Dört kaynak hücre üç bölgeye yansıtılarak mevcut mozaik tamamlanır.", "8 × 6 ızgarada daha geniş desen çift eksende kurulur.", "Tamamlanmış desen içinde dört hatalı hücre bulunur; kaynak-üç eş koordinat grubu denetlenir."],
  ["Yanlış hücrede hangi eksene göre sorun olduğu belirtilmeli.", "Doğru dörtlü grup aynı anda çerçevelenmeli.", "Bitişte dikey ve yatay katlama ayrı animasyonlarla gösterilmeli."],
  ["Geri al/silme işlevi bulunacak.", "Her kaynak hücre için hesaplanan üç eş hücre renk ve koordinat bakımından tam tutarlı olacak."]),

G(41, "Tema 6", "Dedektif Bürosu", "Araştırma sorusunu ayırt etme",
  ["Soru kartları yürüyen bantta, 'veri toplanabilir' ve 'tek cevaplı' kutuları altta; kartlar girişte kısmen kırpılabiliyor.", "'Ali bugün ne yedi?' tek cevaplı sayılmış. Tek kişiye ait olsa da yanıt gözlem/görüşme ile veri olarak toplanabilir; ölçüt 'farklı kişilerden farklı cevap' diye aşırı dar tanımlanmış."],
  ["Araştırma sorusu ile her türlü veri toplama sorusu birbirine karışabilir.", "Tek birey hakkında zamana göre değişebilen bir soru, bağlam verilmeden kesin tek cevaplı sınıfına atılırsa yanlış genelleme oluşur."],
  ["Önce sorunun araştırma amacı, hedef grubu ve değişkeni belirletilsin.", "İki kutu 'istatistiksel araştırma sorusu' ve 'tek, sabit bilgi sorusu' olarak daha doğru adlandırılsın.", "Sorular karar verilene kadar sabit ve tam görünür olsun; neden birden fazla yanıt dağılımı beklenebileceği açıklansın.", "Çocuk son turda konu + grup + değişken kartlarından kendi araştırma sorusunu kursun."],
  ["Sınıfımızdaki öğrencilerin haftalık okuduğu kitap sayısı nedir? araştırma sorusudur.", "Bir hafta kaç gündür? tek sabit bilgi sorusudur.", "Konu 'ulaşım', grup '3/A', değişken 'okula geliş biçimi' kartlarıyla yeni araştırma sorusu kurulur."],
  ["Yanlışta 'kimlerden, hangi değişkene ait, bir dağılım oluşur mu?' kontrolü gösterilsin.", "Tartışmalı sorular bağlamla yeniden yazılsın; tek etiketle geçiştirilmesin.", "Doğru sınıflamada kısa gerekçe sesli ve yazılı sunulsun."],
  ["Araştırma soruları hedef grup ve değişken içerecek.", "'Ali bugün ne yedi?' gibi bağlama göre değişebilen maddeler ya yeniden yazılacak ya da gerekçeli olarak çıkarılacak."]),

G(42, "Tema 6", "Harçlık Anketi", "Çetele ile veri toplama",
  ["Üç sütun ve tek tek gelen yanıtlar görünür; doğru sütuna dokununca çetele oluşuyor. Konu haftalık harçlık olduğundan sosyoekonomik farklılıkları sınıf önünde görünür kılabilir.", "Beşinci çizginin nasıl dört çizgiyi kestiği yönergede yazıyor; ancak çocuk çetele işaretini kendisi çizmiyor ve yanlış dokunmayı geri alma görünmüyor."],
  ["Harçlık sorusu bazı çocuklar için mahrem veya rahatsız edici olabilir; öğrenme amacı için gereksiz hassas veri toplar.", "Sütuna dokunma, standart beşli çetele yapısını üretme ve sayma becerisini sınırlı ölçer."],
  ["Harçlık yerine 'haftada okunan kitap sayısı' veya 'sevilen meyve' gibi nötr sınıf verisi seçilsin.", "Çocuk ilk dört dik çizgiyi, beşinci çapraz çizgiyi parmağıyla çizebilsin; motor gerekirse çizgiyi standarda mıknatıslasın.", "Geri al düğmesi ve yanıt sayacı bulunsun; toplam çetele sayısı katılımcı sayısıyla sürekli karşılaştırılsın.", "Anket öncesinde soru, hedef grup ve veri toplama planı bir kartta açıklansın."],
  ["10 öğrencinin haftada okuduğu kitap sayısı 0-1-2+ kategorilerinde çetelelenir.", "12 öğrencinin sevdiği meyveler üç sütuna işlenir; beşli gruplar oluşur.", "Bir yanlış çetele girişi bulunup geri alınır; çeteleler sıklık sayılarına dönüştürülür."],
  ["Yanlış sütunda can eksilmeden yanıt tekrar dinlenip düzeltme yapılmalı.", "Beşinci işarette standart çapraz grup animasyonu ve 'beş' seslendirmesi olmalı.", "Bitişte yanıt sayısı ile tüm çetelelerin toplamı eşleştirilmeli."],
  ["Hassas harçlık verisi nötr bir araştırma konusuyla değiştirilecek.", "Beşli çetele standardı, geri alma ve toplam tutarlılık kontrolü eksiksiz çalışacak."]),

G(43, "Tema 6", "Sıklık Tablosu Fabrikası", "Çeteleyi sıklığa dönüştürme",
  ["Dört satır ve 3, 6, 5, 7 sayı kartları görünür; çeteleler düz dikey çizgi dizileri '|||||||' olarak gösteriliyor.", "Beşli gruplama çapraz çizgiyle görünmediği için çetele okuma stratejisi yalnız tek tek çizgi saymaya dayanıyor."],
  ["Bir önceki oyunda öğretilen beşli çetele standardıyla bu tablo çelişir.", "Sayı kartını satıra taşımak doğru olsa da beş + kalan biçiminde hızlı sayma ölçülmez."],
  ["Bütün çeteleler standart dört dik + beşinci çapraz grup biçiminde çizilsin.", "Çocuk önce beşli grubu çerçeveleyip kalan çizgileri saysın, sonra sıklık kartını sürüklesin.", "Satır başlıkları sade ve okunaklı olsun; parçalar karışık sırada her açılışta değişsin.", "Dönüşüm bitince çetele ve sayı aynı satırda kalıp toplam veri sayısı kontrol edilsin."],
  ["7 = bir beşli grup + 2 çizgi olarak okunur.", "5 ve 6 sıklıkları 5; 5 + 1 biçiminde dönüştürülür.", "9, 10 ve 12 içeren yeni tabloda birden fazla beşli grup okunur; toplam bulunur."],
  ["Yanlış sayıda beşli grup ve kalan farklı renklerle gösterilmeli.", "Doğruda sıklık sayısı, çetele grubu ve seslendirme eşleşmeli.", "Sürükleme hatasında kart kaybolmamalı ve geri alınabilmeli."],
  ["Çeteleler standart beşli gruplama biçiminde olacak.", "Her satırdaki çizgi toplamı, sıklık rakamı ve genel toplam birebir eşleşecek."]),

G(44, "Tema 6", "Nokta Grafiği Laboratuvarı", "Her nokta bir veriyi temsil eder",
  ["Üç sütun ve blok deposu görünür; kaynakta 4, 6 ve 3 sayıları doğrudan yazıyor. Depodaki parçalar renkli dikdörtgenler içinde beyaz daireler olduğundan 'nokta' birimi görsel olarak ikincil kalıyor.", "Çocuk hazır sayılar kadar bloğa dokunuyor; önceki çetele/sıklık verisinden dönüşüm sürecini kendisi yapmıyor."],
  ["Nokta grafiği, sayı kadar blok doldurma etkinliğine dönüşür.", "Farklı renk/şekilli bloklar her noktanın eşit bir veri birimi olduğu algısını zayıflatabilir."],
  ["Bütün veri işaretleri aynı boyda tek renk daire olsun; '1 nokta = 1 kişi' anahtarı grafiğin üstünde sabit kalsın.", "Kaynak veri standart çetele veya sıklık tablosu olarak verilsin; sayı gerekirse çocuk tarafından çıkarılsın.", "Noktalar sütunda tabandan başlayıp eş aralıklı hücrelere yerleşsin; boşluk bırakmaya izin verilmesin.", "Grafik bitince sütunlar en çok, en az, toplam ve fark sorularıyla yorumlansın."],
  ["4-6-3 sıklıkları her nokta 1 kişi kuralıyla kurulur.", "Yeni 5-2-7 veri seti çeteleden grafiğe dönüştürülür.", "Bir hatalı grafikte boşluk, fazla nokta ve yanlış sütun bulunup düzeltilir."],
  ["Yanlış sütunda kaynak satır ve hedef sütun birlikte vurgulanmalı.", "Fazla noktada yalnız son nokta geri alınabilmeli.", "Doğru grafikte nokta sayıları, sıklıklar ve toplam katılımcı sayısı aynı olmalı."],
  ["Noktalar standart, eş boyutlu ve birim anahtarıyla tutarlı olacak.", "Kaynak-sıklık-grafik toplamları her tur otomatik tutarlılık kontrolünden geçecek."]),

G(45, "Tema 6", "Grafik Terazisi", "Grafikten fark ve toplam çıkarma",
  ["Terazi görseli, 9 ve 5 değerleri ile +1 nokta bloğu konuya uyuyor; çocuk az olan kefeye dört kez nokta ekleyebiliyor.", "Oyun öncesinde gerçek nokta grafiği gösterilmiyor; değerler metin ve terazi etiketinden hazır veriliyor. Üçüncü turda 8+5+9 grupları seçme görevi denge metaforundan farklılaşıyor."],
  ["Grafiği yorumlama yerine verilen iki sayının farkını tamamlama ölçülür.", "Teraziye eklenen noktaların grafik sütunlarındaki birimlerle ilişkisi görünmezse veri bağlamı kaybolur."],
  ["Turun üstünde aynı meyve verilerinin gerçek nokta grafiği bulunmalı; teraziye değerler grafikten taşınmalı.", "Çocuk 9 ve 5 sütunlarını hizalayıp eşleşmeyen dört noktayı önce görsel olarak işaretlesin.", "Sonra az kefeye dört birim ekleyerek farkı doğrulasın; eklenen her nokta grafikteki eşleşmeyen noktaya bağlansın.", "Toplam turunda terazi yerine bütün sütunları sayan ayrı 'katılımcı sayısı' paneli kullanılmalı."],
  ["Çilek 9, muz 5: fark 4 görsel eşleme ve çıkarma ile bulunur.", "Çilek 9, elma 8: fark 1; yakın sütunlar karşılaştırılır.", "8 + 5 + 9 = 22 toplamı üç grafik sütunu üzerinden bulunur; fark ve toplam yöntemleri ayrılır."],
  ["Fazla eklemede kefe neden ağırlaştığını sayılarla göstermeli; bloklar geri alınabilmeli.", "Doğruda eşleşmeyen noktalar ve 9 - 5 = 4 aynı anda görünmeli.", "Toplam sorusunda çıkarma/dengeden farklı strateji açıkça adlandırılmalı."],
  ["Her soru gerçek grafik görünümünden başlatılacak.", "Fark ve toplam, uygun ayrı görsel stratejilerle ve grafik verileriyle tutarlı çözülecek."]),

G(46, "Tema 6", "Zaman ve Mekân Kapsülü", "Verinin gruba göre değişebilirliği",
  ["3/B öğrencilerinin tat tercihleri üç sütuna tek tek işleniyor; etkileşim veri toplamaya uygun.", "3/A için yalnız 'çikolatalı birinci çıkmıştı' cümlesi var; iki sınıfın gerçek tabloları/grafikleri yan yana karşılaştırılmıyor. Başlık zaman değişimini de ima etse de yalnız grup değişimi deneniyor."],
  ["Sonucun neden değiştiği sayısal dağılım karşılaştırılmadan metinden çıkarılır.", "Kişi, grup ve zaman etkileri ayrı örneklenmezse 'veriler her zaman değişir' gibi aşırı genelleme oluşabilir."],
  ["3/A'nın önceki sonuç tablosu ekranın solunda, 3/B'nin canlı tablosu sağda bulunsun.", "Aynı soru ve aynı seçeneklerin korunduğu açıkça gösterilsin; değişen tek değişken hedef grup olsun.", "İkinci turda aynı sınıfa farklı zamanda aynı soru sorulsun; üçüncü turda soru değişince doğrudan karşılaştırmanın uygun olmadığı tartışılsın.", "Toplama bittikten sonra iki dağılım aynı ölçekli grafiklerle üst üste veya yan yana gösterilsin."],
  ["3/A ve 3/B tat tercihleri karşılaştırılır; farklı grup farklı sonuç verebilir.", "Aynı 3/B sınıfına dönem başı ve sonu aynı soru sorulur; zamanla değişim yorumlanır.", "Soru/ seçenekler değiştirildiğinde iki sonucun doğrudan karşılaştırılamayacağı belirlenir."],
  ["Yanlış yargıda değişen ve sabit kalan araştırma öğeleri kartlarla gösterilmeli.", "Doğruda 'kesin değişir' değil 'değişebilir' dili kullanılmalı.", "Karşılaştırma gerçek frekanslar ve aynı ölçek üzerinden yapılmalı."],
  ["Her karşılaştırmada iki veri gösterimi aynı anda görünür olacak.", "Grup, zaman ve soru değişiminin etkileri ayrı turlarda doğru olasılık diliyle ele alınacak."]),

G(47, "Tema 6", "Çoklu Nokta Şifresi", "Ölçekli nokta grafiğini yorumlama",
  ["Dört büyük nokta, 'her nokta 5 yıldız' ipucu ve sayı tuş takımı görünür; etkileşim okunaklı.", "Soru başında '4 × 5 = ?' ipucu doğrudan yazdığı için ölçeği fark etme ve işlemi seçme adımı büyük ölçüde verilmiş oluyor."],
  ["Çocuk grafiğin anahtarını yorumlamak yerine hazır çarpma işlemini hesaplayabilir.", "Renk adları değişse de tüm sorular aynı ölçek 5 ve doğrudan nokta sayısı metniyle sunulduğundan genelleme sınırlıdır."],
  ["Grafik anahtarı ayrı köşede '● = 5 yıldız' olarak dursun; soru metni çarpma işlemini hazır vermesin.", "Noktalar çocuk tarafından sayılmalı; '4 nokta' ifadesi ilk turdan sonra kaldırılmalı.", "Ölçek 2, 5 ve 10 olarak turlar arasında değişsin; legend her tur dikkatle okunmalı.", "Son turda iki kategori farkı, nokta farkı × ölçek üzerinden kurulup önce görsel sonra sayısal çözülmeli."],
  ["4 nokta, her nokta 5: 20 yıldız bulunur.", "6 nokta, her nokta 2: 12 kitap; yeni ölçek okunur.", "5 ve 3 noktalı iki kategori, her nokta 10: fark 20 olarak bulunur."],
  ["Yanlışta yalnız legend vurgulanmalı; çarpma işlemi hemen yazılmamalı.", "Doğruda nokta sayısı, birim değeri ve gerçek toplam çarpma eşitliğinde birleşmeli.", "Sıfır ve silme tuşları çocuk hatasını düzeltmeye izin vermeli; giriş kalıcı ceza almamalı."],
  ["İpucu cevabı oluşturan işlemi baştan vermeyecek.", "En az üç farklı ölçek ve bir fark sorusu kullanılacak; bütün grafik anahtarları sonuçlarla tutarlı olacak."]),

G(48, "Tema 6", "Veri Mimarı", "Araştırma sürecini grafiğe dönüştürme",
  ["Dört sütun ve 18 blokluk depo görünür; kaynak soru, çetele-sıklık sonuçları ve kategori sayıları hazır olarak veriliyor.", "Başlık 'kendi araştırmanı' dese de çocuk soruyu seçmiyor, veri toplamıyor veya çeteleyi oluşturmuyor; yalnız belirtilen sayıda blok dolduruyor."],
  ["Tam araştırma döngüsü, hazır sıklığı grafiğe kopyalama aşamasına indirgenir.", "Renkli bloklardaki yıldız/üçgen/daire şekilleri her blok aynı veri birimini temsil ederken gereksiz görsel çeşitlilik yaratır."],
  ["Çocuk önce nötr üç konudan bir araştırma sorusu seçsin veya konu-grup-değişken kartlarıyla kursun.", "Sanal sınıf karakterlerinden yanıtları toplayıp standart çeteleye kendisi işlesin; çeteleyi sıklığa dönüştürsün.", "Grafikte tek tip blok veya nokta ve açık anahtar kullanılsın; kaynak aşamalar ekranın yanında referans olarak kalsın.", "Bitişte en çok, en az, fark, toplam ve sonucun değişebilirliği hakkında iki yorum seçilip proje kartına yazılsın."],
  ["Hazır kitap verisiyle yalnız çetele-sıklık-grafik dönüşümü öğrenilir.", "Çocuk 'sınıfımızın sevdiği oyun türü' sorusuyla 12 sanal yanıt toplar ve grafiği kurar.", "Kendi seçtiği konu için soru, hedef grup, veri, çetele, sıklık, grafik ve iki yorumdan oluşan proje tamamlanır."],
  ["Yanlış blokta ilgili çetele/sıklık satırı vurgulanmalı; hedef sayı doğrudan söylenmemeli.", "Her aşamada toplam katılımcı sayısı korunmalı ve tutarsızlık varsa sonraki aşama açılmamalı.", "Bitiş kartı çocuğun gerçek soru ve verisini göstermeli; yalnız hazır örnekle başarı verilmemeli."],
  ["Son turda araştırma sorusu ve veri seti çocuk tarafından seçilecek/oluşturulacak.", "Yanıt, çetele, sıklık, grafik ve yorum toplamları birebir tutarlı olacak; bütün süreç tamamlanmadan oyun bitmeyecek."]),

]


THEMES = {
    "Tema 1": ("Sayılar ve Nicelikler (1) - temsil, basamak, örüntü ve tahmin", CORAL,
               ["Sayılar yalnız hareketli etiket olarak kalmamalı; yüzlük-onluk-birlik ve sayılabilir nesneler görünmeli.", "İleri-geri ritmik sayma, tek-çift ve tahmin farklı örneklerle genellenmeli.", "Tren, tapınak, fasulye, kavanoz gibi hikâye nesneleri gerçek matematiksel eylemi taşımalı."]),
    "Tema 2": ("Sayılar ve Nicelikler (2) - kesir, zaman, ölçme ve para", GOLD,
               ["Kesirlerde parça-bütün ilişkisi gerçek modellerle kurulmalı; etiket eşleme yeterli olmamalı.", "Saat, kronometre ve ölçüm oyunlarında yönerge ile gerçek kontrol yöntemi aynı olmalı.", "Birim dönüşümleri sayı ve birimle birlikte, yaklaşık ilişkiler doğru dille sunulmalı."]),
    "Tema 3": ("İşlemlerden Cebirsel Düşünmeye", PURPLE,
               ["İşlem stratejileri hareketli hedef yakalamaya indirgenmemeli; ara adımlar ve görsel modeller korunmalı.", "Toplama-çıkarma ve çarpma-bölme tersliği aynı nesne/model üzerinde kanıtlanmalı.", "Problem kurma ve strateji seçme görevlerinde çözüm metinde önceden verilmemeli."]),
    "Tema 4": ("Nesnelerin Geometrisi (1) - cisim, şekil, çevre ve sıvı", TEAL,
               ["Küp, cetvel, ip, kap ve mozaik gerçek etkileşim nesnesi olacak; ortak kronometre/tren şablonları kullanılmayacak.", "Geometrik sonuçlar çizme, döndürme, ölçme ve üst üste getirmeyle kanıtlanmalı.", "Birleşik şekillerin çevresinde ortak kenarlar dış çevreye dahil edilmemeli."]),
    "Tema 5": ("Nesnelerin Geometrisi (2) - simetri ve kodlama", BLUE,
               ["Simetri ekseni bütün tur boyunca görünür olmalı; eş noktalar eksene eş uzaklıkta kurulmalı.", "Açılış sesi keşfedilecek sonucu vermemeli; katlama/üst üste bindirme ile kanıt sunmalı.", "Kodlama oyunlarında referans rota görünür olmalı ve simetrik komutlar çocuk tarafından üretilmeli."]),
    "Tema 6": ("Veriye Dayalı Araştırma", CORAL,
               ["Araştırma sorusu, hedef grup, veri toplama, çetele, sıklık, grafik ve yorum tek bir tutarlı döngü oluşturmalı.", "Çeteleler standart beşli gruplama biçiminde, grafikler açık birim anahtarıyla gösterilmeli.", "Hazır sayıları kopyalamak yerine çocuk veri üretmeli, dönüştürmeli ve sonuç hakkında gerekçeli yorum yapmalı."]),
}


doc = BaseDocTemplate(
    str(OUT), pagesize=A4, rightMargin=MX, leftMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
    title="3. Sınıf Matematik Oyunları - Ayrıntılı Düzeltmeler",
    author="Macera Akademi oyun incelemesi",
)
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

story = []
story += [
    Spacer(1, 16 * mm), P("MACERA AKADEMİ", cover_kicker),
    P("3. Sınıf Matematik Oyunları<br/>Ayrıntılı Düzeltmeler", cover_title),
    P("48 oyunun gerçek ekranları açılarak, ilk oynanışları denenerek ve kaynak tanımlarıyla karşılaştırılarak hazırlanmıştır.", cover_sub),
]
cover_box = Table([[P("<b>Kapsam</b><br/>Bu belge 3. sınıf matematik listesindeki w01-w48 oyunlarının tamamını kapsar. Her oyun için gözlenen mevcut durum, eğitimsel risk, yeni sahne ve oynanış, üç farklı tur, geri bildirim akışı ve ölçülebilir kabul koşulları verilir.")]], colWidths=[153 * mm])
cover_box.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL), ("BOX", (0, 0), (-1, -1), 0.7, TEAL),
    ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ("TOPPADDING", (0, 0), (-1, -1), 13), ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
]))
story += [cover_box, Spacer(1, 9 * mm), P("Hazırlama yaklaşımı", h2)]
story += bullets([
    "3. sınıf matematik listesindeki 48 oyunun tamamı tek tek açıldı; başlık, sahne, yönerge, sayaç, seçim alanı ve ilk etkileşim düzeni görsel olarak incelendi.",
    "Radar, tren, bant, paketleme, pizza, kesir-saat, kronometre, roket, terazi, geometri, simetri, kargo, çetele, köprü, grafik ve sayı tuş takımı motorları kaynak görevleriyle karşılaştırıldı.",
    "Düzeltmeler yalnız metin önerisi değildir; matematiksel doğruluk, çocuk eylemi, yanlış geri bildirimi, üç turlu genelleme ve test edilebilir kabul koşulu birlikte yazılmıştır.",
])
story += [PageBreak()]

story += [P("Testten çıkan öncelikli bulgular", h1)]
story += [box("1. Hikâye ile oyun motoru uyuşmuyor", ["Kesir Asansörü ve Akıllı Asansör yatay tren-tünel sahnesinde; İp Dolama ve Sıvı Laboratuvarı kronometre kadranında; Çevre Avcıları tren sahnesinde açılıyor. Doğa Dedektifleri kamp yerine roket-yakıt motoru kullanıyor."], PALE_CORAL, CORAL), Spacer(1, 2 * mm)]
story += [box("2. Yönerge ile gerçek kontrol çelişiyor", ["Zaman Kulesi ibreleri sürüklemeyi söylüyor fakat ok düğmeleri kullanıyor. Geometri Stüdyosu cetvel kullanmayı söylerken hazır noktalara dokunduruyor. Bazı oyunlarda açılış sesi keşfedilecek cevabı daha oyun başlamadan açıklıyor."], PALE_GOLD, GOLD), Spacer(1, 2 * mm)]
story += [box("3. Görsel kanıt ve ölçme eylemi eksik", ["Kavanozdaki Misketler'de kavanoz yok; İp Dolama'da ip ve kutu yok; Sıvı Laboratuvarı'nda dereceli sürahi yok. Sayı, çevre, litre ve süre çoğu kez ortak bir sürgü veya sayaçla temsil ediliyor."], PALE_BLUE, BLUE), Spacer(1, 2 * mm)]
story += [box("4. İçerik doğruluğu ve araştırma etiği", ["Mozaik Atölyesi ortak kenarları hesaba katmadan parça çevrelerini topluyor; bu sonuçlar birleşik şeklin çevresi değildir. Zaman Tüneli '1 yıl = 52 hafta' ifadesini yaklaşık/kalan gün açıklaması olmadan tam eşitlik gibi veriyor. Harçlık Anketi yerine daha nötr veri konusu seçilmesi önerildi."], PALE_TEAL, TEAL)]
story += [PageBreak()]

story += [P("Bütün oyunlarda ortak uygulama standardı", h1)]
standard_rows = [
    [P("Sahne", box_title), P("Başlıktaki ana nesne matematiksel eylemi gerçekten taşır; ortak motor teması hikâyenin yerini almaz.", small)],
    [P("Tur", box_title), P("Her oyun en az üç değişen tur içerir; sayı, sıra, konum, veri veya şekil değişir.", small)],
    [P("Yönerge", box_title), P("Söylenen kontrol yöntemi ekrandaki gerçek dokunma, sürükleme, çizme veya basılı tutma davranışıyla aynıdır.", small)],
    [P("Yanlış", box_title), P("Yanlışta cevap doğrudan söylenmez; basamak, model, ölçü, eksen, grafik veya ara işlem üzerinde hata kaynağı gösterilir.", small)],
    [P("Doğru", box_title), P("Doğru yanıt yalnız renk/konfetiyle değil, sonucu matematiksel olarak kanıtlayan animasyonla doğrulanır.", small)],
    [P("Erişim", box_title), P("Kartlar karar verilene kadar okunabilir; ekran kenarında kırpılmaz ve en az 44 px dokunma hedefi sunar.", small)],
    [P("Tutarlılık", box_title), P("Nesne sayısı, metin, ses, işlem, grafik anahtarı ve sonuç bütün turlarda birebir aynı veriyi gösterir.", small)],
]
standards = Table(standard_rows, colWidths=[28 * mm, 148 * mm])
standards.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8D4E2")), ("BACKGROUND", (0, 0), (0, -1), PALE_PURPLE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story += [standards, Spacer(1, 5 * mm)]
story += bullets([
    "Can sistemi kavramsal yanlış ile dokunma/okuma hatasını ayırmalı; kartı kaçırma veya küçük hedefe basamama ağır ceza oluşturmamalıdır.",
    "Tahmin görevlerinde hedef/gerçek sonuç önceden gösterilmemeli; tahmin bağımsız kaydedilip ölçümle karşılaştırılmalıdır.",
    "Başarı, tek ilk soruda değil bütün tur dizisi ve kabul ölçütleri tamamlandığında kaydedilmelidir.",
])
story += [PageBreak()]

last_theme = None
accent_cycle = [CORAL, TEAL, GOLD, PURPLE]
for game in games:
    if game["theme"] != last_theme:
        last_theme = game["theme"]
        theme_name, accent, focus = THEMES[last_theme]
        theme_table = Table([[P(last_theme, badge), P(theme_name, theme_title)]], colWidths=[30 * mm, 146 * mm], rowHeights=[50 * mm])
        theme_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), accent), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (0, 0), "CENTER"), ("LEFTPADDING", (1, 0), (1, 0), 12),
            ("RIGHTPADDING", (1, 0), (1, 0), 12), ("ROUNDEDCORNERS", [10]),
        ]))
        story += [Spacer(1, 22 * mm), theme_table, Spacer(1, 10 * mm), P("Bu temadaki ana düzeltme odağı", h2)]
        story += bullets(focus)
        story += [Spacer(1, 6 * mm), box("Tema kabul eşiği", ["Bu temadaki bütün oyunlar üç tur tamamlanmadan bitmiş sayılmayacak.", "Hikâye nesnesi, matematiksel işlem ve geri bildirim aynı sahnede birbirini destekleyecek."], PALE_TEAL, TEAL), PageBreak()]

    accent = accent_cycle[(game["n"] - 1) % len(accent_cycle)]
    story += [header(game["n"], game["title"], game["sub"], accent), Spacer(1, 3.0 * mm)]
    story += [box("Denemede görülen mevcut durum", game["observed"], PALE_CORAL, CORAL, compact=True), Spacer(1, 1.4 * mm)]
    story += [box("Eğitimsel risk", game["risk"], PALE_GOLD, GOLD, compact=True), Spacer(1, 1.4 * mm)]
    story += [P("Yeni sahne ve oynanış", h2)]
    story += bullets(game["new"], bullet_small)
    story += [P("Üç farklı tur", h2), rounds_table(game["rounds"]), Spacer(1, 1.4 * mm)]
    story += [box("Geri bildirim ve bitiş", game["feedback"], PALE_TEAL, TEAL, compact=True), Spacer(1, 1.4 * mm)]
    story += [box("Kabul ölçütü", game["acceptance"], PALE_BLUE, BLUE, compact=True), PageBreak()]

story += [P("Son kabul kontrolü", h1), P("3. sınıf matematik bölümü tamamlanmadan önce", h2)]
story += bullets([
    "48 oyunun her biri üç farklı turla baştan sona oynanır; her tur için beklenen ve gerçekleşen sonuç kaydedilir.",
    "Başlık, sahne, yönerge, sayaç ve seslendirme aynı oyun metaforunu kullanır; tren, kronometre veya roket şablonu ilgisiz oyunda görünmez.",
    "Sayı, kesir, saat, birim, işlem, şekil, çevre, simetri, çetele ve grafik sonuçları ekrandaki nesnelerle birebir doğrulanır.",
    "Mozaik/birleşik şekil çevrelerinde içte kalan ortak kenarlar dış çevreye eklenmez; bütün sonuçlar yeniden hesaplanır.",
    "Açılış sesleri cevabı önceden vermez; yanlış geri bildirimi doğru seçeneği söylemeden düşünme stratejisi sunar.",
    "Tahmin görevlerinde gerçek hedef önceden gizlenir; ölçümden sonra tahmin-gerçek-fark raporu gösterilir.",
    "Çeteleler standart beşli gruplarla, grafikler açık birim anahtarıyla ve veri toplamları tutarlı olarak gösterilir.",
    "Küçük ekranda hiçbir kart/şekil kırpılmaz; gerekli geri al, silgi ve program düzenleme araçları bulunur.",
])
story += [Spacer(1, 4 * mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 3. sınıf matematik listesindeki w01-w48 oyunlarını kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, mekanik, tur, geri bildirim ve test gereksinimlerini ayrıntılı biçimde tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)

reader = PdfReader(str(OUT))
assert len(games) == 48
assert len(reader.pages) == 58, len(reader.pages)
for game in games:
    assert game["title"] in "\n".join(page.extract_text() or "" for page in reader.pages)
print(str(OUT))
print({"pages": len(reader.pages), "games": len(games), "bytes": OUT.stat().st_size})
