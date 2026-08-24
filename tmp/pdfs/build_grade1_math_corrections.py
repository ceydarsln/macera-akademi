from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfgen import canvas
import os


ROOT = "/Users/ceyda/Documents/New project"
OUT = os.path.join(ROOT, "output/pdf/1_sinif_matematik_duzeltmeleri_devam.pdf")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_ITALIC = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
pdfmetrics.registerFont(TTFont("Arial", FONT_REG))
pdfmetrics.registerFont(TTFont("Arial-Bold", FONT_BOLD))
pdfmetrics.registerFont(TTFont("Arial-Italic", FONT_ITALIC))

PAGE_W, PAGE_H = A4
MARGIN_X = 18 * mm
TOP = 20 * mm
BOTTOM = 17 * mm

INK = colors.HexColor("#25213B")
PURPLE = colors.HexColor("#473A70")
TEAL = colors.HexColor("#178B8B")
CORAL = colors.HexColor("#E7635B")
GOLD = colors.HexColor("#E3A72F")
PALE_PURPLE = colors.HexColor("#F1EDF9")
PALE_TEAL = colors.HexColor("#E9F6F4")
PALE_CORAL = colors.HexColor("#FFF0ED")
PALE_GOLD = colors.HexColor("#FFF7E3")
LIGHT_GREY = colors.HexColor("#F4F5F7")
MID_GREY = colors.HexColor("#7A7687")
WHITE = colors.white


class NumberBadge:
    @staticmethod
    def make(number, title, group, accent=PURPLE):
        data = [
            [
                Paragraph(str(number), badge_style),
                Paragraph(f"<b>{title}</b><br/><font size='8.2' color='#E9E5F5'>{group}</font>", game_title_style),
            ]
        ]
        table = Table(data, colWidths=[16 * mm, 155 * mm], rowHeights=[20 * mm])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), accent),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (0, 0), "CENTER"),
                    ("LEFTPADDING", (0, 0), (0, 0), 4),
                    ("RIGHTPADDING", (0, 0), (0, 0), 4),
                    ("LEFTPADDING", (1, 0), (1, 0), 10),
                    ("RIGHTPADDING", (1, 0), (1, 0), 10),
                    ("ROUNDEDCORNERS", [8]),
                ]
            )
        )
        return table


styles = getSampleStyleSheet()
body = ParagraphStyle(
    "BodyTR",
    parent=styles["BodyText"],
    fontName="Arial",
    fontSize=9.5,
    leading=13.1,
    textColor=INK,
    spaceAfter=2.2 * mm,
)
body_small = ParagraphStyle(
    "BodySmallTR",
    parent=body,
    fontSize=8.7,
    leading=11.5,
    spaceAfter=1.4 * mm,
)
bullet = ParagraphStyle(
    "BulletTR",
    parent=body,
    leftIndent=5 * mm,
    firstLineIndent=-3.2 * mm,
    bulletIndent=0,
    spaceAfter=1.5 * mm,
)
cover_kicker = ParagraphStyle(
    "CoverKicker",
    parent=body,
    fontName="Arial-Bold",
    fontSize=10,
    leading=13,
    textColor=TEAL,
    alignment=TA_CENTER,
    spaceAfter=6 * mm,
)
cover_title = ParagraphStyle(
    "CoverTitle",
    parent=body,
    fontName="Arial-Bold",
    fontSize=27,
    leading=31,
    textColor=PURPLE,
    alignment=TA_CENTER,
    spaceAfter=5 * mm,
)
cover_sub = ParagraphStyle(
    "CoverSub",
    parent=body,
    fontSize=12.5,
    leading=17,
    textColor=INK,
    alignment=TA_CENTER,
    spaceAfter=10 * mm,
)
h1 = ParagraphStyle(
    "H1TR",
    parent=body,
    fontName="Arial-Bold",
    fontSize=20,
    leading=24,
    textColor=PURPLE,
    spaceAfter=5 * mm,
)
h2 = ParagraphStyle(
    "H2TR",
    parent=body,
    fontName="Arial-Bold",
    fontSize=11,
    leading=14,
    textColor=TEAL,
    spaceBefore=2.6 * mm,
    spaceAfter=1.5 * mm,
)
callout_title = ParagraphStyle(
    "CalloutTitle",
    parent=body,
    fontName="Arial-Bold",
    fontSize=10.2,
    leading=13,
    textColor=PURPLE,
    spaceAfter=1.5 * mm,
)
game_title_style = ParagraphStyle(
    "GameTitle",
    parent=body,
    fontName="Arial",
    fontSize=15,
    leading=18,
    textColor=WHITE,
    spaceAfter=0,
)
badge_style = ParagraphStyle(
    "Badge",
    parent=body,
    fontName="Arial-Bold",
    fontSize=18,
    leading=18,
    textColor=WHITE,
    alignment=TA_CENTER,
    spaceAfter=0,
)
round_head = ParagraphStyle(
    "RoundHead",
    parent=body,
    fontName="Arial-Bold",
    fontSize=8.8,
    leading=11,
    textColor=PURPLE,
    alignment=TA_CENTER,
    spaceAfter=0,
)
round_text = ParagraphStyle(
    "RoundText",
    parent=body,
    fontSize=8.2,
    leading=10.6,
    spaceAfter=0,
)


def p(text, style=body):
    return Paragraph(text, style)


def bullets(items):
    return [Paragraph(item, bullet, bulletText="•") for item in items]


def section_box(title, items, bg=LIGHT_GREY, title_color=PURPLE):
    content = [Paragraph(title, ParagraphStyle("box_title", parent=callout_title, textColor=title_color))]
    content.extend(bullets(items))
    table = Table([[content]], colWidths=[171 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#D7D3DF")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("ROUNDEDCORNERS", [7]),
            ]
        )
    )
    return table


def round_table(rounds):
    data = [[p("1. TUR", round_head), p("2. TUR", round_head), p("3. TUR", round_head)]]
    data.append([p(rounds[0], round_text), p(rounds[1], round_text), p(rounds[2], round_text)])
    table = Table(data, colWidths=[57 * mm, 57 * mm, 57 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PALE_GOLD),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFCF5")),
                ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#DDCFAB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def game_page(g):
    accent = g.get("accent", PURPLE)
    flow = [NumberBadge.make(g["no"], g["title"], g["group"], accent), Spacer(1, 5 * mm)]
    flow.append(section_box("Mevcut ekranda görülen sorun", g["observed"], PALE_CORAL, CORAL))
    flow.append(Spacer(1, 3.5 * mm))
    flow.append(p("Yeni sahne ve oynanış", h2))
    flow.extend(bullets(g["proposal"]))
    flow.append(Spacer(1, 1.5 * mm))
    flow.append(p("Üç farklı tur", h2))
    flow.append(round_table(g["rounds"]))
    flow.append(Spacer(1, 4 * mm))
    flow.append(section_box("Geri bildirim ve bitiş", g["feedback"], PALE_TEAL, TEAL))
    flow.append(Spacer(1, 3 * mm))
    flow.append(p(f"<b>Kabul ölçütü:</b> {g['acceptance']}", body_small))
    flow.append(PageBreak())
    return flow


def draw_header_footer(canv, doc):
    page = canv.getPageNumber()
    if page == 1:
        return
    canv.saveState()
    canv.setStrokeColor(colors.HexColor("#D9D5E5"))
    canv.setLineWidth(0.6)
    canv.line(MARGIN_X, PAGE_H - 13 * mm, PAGE_W - MARGIN_X, PAGE_H - 13 * mm)
    canv.setFont("Arial", 7.7)
    canv.setFillColor(MID_GREY)
    canv.drawString(MARGIN_X, 9 * mm, "1. Sınıf Matematik - Düzeltme Devamı")
    canv.drawRightString(PAGE_W - MARGIN_X, 9 * mm, str(page))
    canv.restoreState()


class NumberedCanvas(canvas.Canvas):
    pass


games = [
    {
        "no": 1,
        "title": "Kargo Robotunun Hatası",
        "group": "Toplama-Çıkarma İlişkisi / Ekleme ve İade",
        "accent": CORAL,
        "observed": [
            "Oyun şu anda uzay gemisi, asteroitler ve uçan işlem kartlarıyla oynanıyor; kargo robotu, depo, raf ve kutu görseli yok.",
            "6 + 4 = 10 ve 10 - 4 = 6 ilişkisi yalnız metinden okunuyor. Çocuk eklenen ve iade edilen kutuları görerek sayamıyor.",
        ],
        "proposal": [
            "Sahne bir kargo deposu olsun. Bant, raf, iade arabası ve hareket eden bir robot açıkça görünsün.",
            "Önce başlangıç kutuları görünür biçimde sayılsın; robot ek kutuları tek tek yerleştirsin. Fazla kutular farklı renkle parlasın.",
            "Çocuk fazla kutuları sürükleyerek İADE arabasına bıraksın; ardından büyük sayı ve işlem taşlarıyla ters işlemi seçsin.",
            "Sesli yönerge örneği: Robot 4 kutuyu fazla yükledi. 10 kutudan 4 kutuyu iade et ve hangi işlemin 6 kutuya döndürdüğünü bul.",
        ],
        "rounds": [
            "Raf 6 kutuyla başlar, robot 4 kutu ekler. Çocuk 4 kutuyu iade eder ve 10 - 4 = 6 işlemini tamamlar.",
            "8 kutuya 5 kutu eklenir. 13 kutudan 5'i iade arabasına taşınır; sonuç yeniden 8 olur.",
            "Robot rafa 9 kutu koyar, 3 kutu indirir. Çocuk kalan 6 kutuyu sayar ve sonuç kartını seçer.",
        ],
        "feedback": [
            "Yanlış kutu veya işlem seçilirse parça yerine döner; robot başını sallayıp Tekrar dene der. Bir can eksilir.",
            "Doğru cevapta bant çalışır, iade arabası çıkar ve robot yeşil onay ışığı yakar. Üç tur bitince Depo düzeldi mesajı gelir.",
        ],
        "acceptance": "Hiçbir turda uzay gemisi veya asteroit görünmeyecek; bütün sayılar ekrandaki gerçek kutu adediyle birebir aynı olacak.",
    },
    {
        "no": 2,
        "title": "Asansör Düğmeleri",
        "group": "Toplama-Çıkarma İlişkisi / Yukarı ve Aşağı",
        "accent": TEAL,
        "observed": [
            "Başlık asansör olmasına rağmen aynı uzay sahnesi kullanılıyor. Katlar, kabin, kapılar ve düğme paneli bulunmuyor.",
            "İşlemler asteroitlerin üzerinde uçuyor; yukarı çıkma ve aşağı inme hareketi görsel olarak kanıtlanmıyor.",
        ],
        "proposal": [
            "Kesiti görünen 10 katlı bir bina, gerçek asansör kabini ve büyük dokunmatik düğme paneli çizilsin.",
            "Kabin hareket ederken kat göstergesi 2, 3, 4, 5 diye değişsin. Başlangıç katı renkli bir bayrakla işaretlensin.",
            "Çocuk uygun işlem kartını panele taksın; doğruysa kabin gerçekten başlangıç katına dönsün.",
            "Yönerge kısa ve sesli olsun: 2. kattan 3 kat çıktık ve 5. kata geldik. 2. kata dönmek için hangi işlemi seçmeliyiz?",
        ],
        "rounds": [
            "2. kattan 3 kat yukarı çıkılır. Çocuk 5 - 3 = 2 kartını seçer; kabin 3 kat aşağı iner.",
            "4. kattan 5 kat yukarı çıkılır. 9 - 5 = 4 seçilince kat sayacı geriye doğru akar.",
            "7. kattan 3 kat aşağı inilir. Başlangıca dönmek için 4 + 3 = 7 seçilir ve kabin yukarı çıkar.",
        ],
        "feedback": [
            "Yanlış işlemde asansör hareket etmez, ilgili düğme kırmızı yanıp söner ve Tekrar dene denir.",
            "Doğru işlemde kapılar açılır, başlangıç bayrağı parlar ve kabindeki karakter sevinir.",
        ],
        "acceptance": "Her işlemde kat göstergesi ile kabinin gerçek konumu uyuşacak; çocuk yalnız metin okuyarak değil, hareketi izleyerek de ters işlemi anlayabilecek.",
    },
    {
        "no": 3,
        "title": "Ankara Simitçisi ve Oyuncakçı",
        "group": "Paralarımız / Değer ve Büyüklük Eşleştirme",
        "accent": GOLD,
        "observed": [
            "Mevcut ekranda simitçi, oyuncakçı veya Ankara sokağı yok; yalnız ürün adları ve beyaz para kartları var.",
            "Ürünlerin yanında fiyat etiketi görünmediği için 10 TL'nin neden simitle, 200 TL'nin neden oyuncak ayıyla eşleştiği çocuk tarafından çıkarılamıyor.",
            "Paralar gerçek/stilize banknot olarak değil yalnız yazı şeklinde gösteriliyor; görsel para tanıma kazanımı oluşmuyor.",
        ],
        "proposal": [
            "Sahnenin solunda Ankara simit arabası, sağında oyuncakçı vitrini olsun. Her ürünün altında büyük ve okunaklı oyun fiyatı bulunsun.",
            "Altta 5, 10, 20, 50, 100 ve 200 TL değerlerini renk ve büyüklük farkıyla gösteren stilize banknotlar yer alsın.",
            "Çocuk banknotu ürüne sürüklesin; doğruysa ürün alışveriş çantasına girsin. Fiyatlar piyasa bilgisi değil, oyun içi eğitim fiyatı olarak sunulsun.",
            "Banknota dokunulduğunda değeri sesli okunsun; yalnızca yazıya bağlı kalınmasın.",
        ],
        "rounds": [
            "Simit, su ve dondurma gibi üç ürün; 5, 10 ve 20 TL banknotlarıyla tekli eşleştirilir.",
            "Oyuncak ayı, top ve yapboz; 20, 50 ve 100 TL ile eşleştirilir. Banknot sırası karıştırılır.",
            "Bisiklet, oyuncak tren ve büyük kutu; 50, 100 ve 200 TL ile eşleştirilir. Ürün konumları değişir.",
        ],
        "feedback": [
            "Yanlış parada kasa kapalı kalır, banknot yerine döner ve Bu ürünün fiyatına tekrar bak denir.",
            "Doğru eşleştirmede kasa sesi duyulur, ürün çantaya girer ve fiyat etiketi yeşil olur.",
        ],
        "acceptance": "Her ürünün fiyatı başlamadan önce görünür olacak; doğru eşleşme gizli veriye veya deneme-yanılmaya bağlı kalmayacak.",
    },
    {
        "no": 4,
        "title": "Sihirli Büyüteç",
        "group": "Nesneler ve Geometrik Şekiller / Günlük Nesnelerde Şekil Avı",
        "accent": PURPLE,
        "observed": [
            "Oyun su altı/fener ağı şablonunda açılıyor. Büyüteç yok; nesneler gerçek sahne içinde değil, adları yazan küçük beyaz etiketler olarak yüzüyor.",
            "Çocuk şekli görselden ayırt etmek yerine Duvar Saati ve Top yazılarını okuyarak cevap verebiliyor.",
        ],
        "proposal": [
            "Bir çocuk odası ve park sahnesi kurulsun. Saat, top, kitap, hediye kutusu, pencere ve parti şapkası büyük gerçek nesneler olarak çizilsin.",
            "Ekranda tutulup sürüklenebilen gerçek bir büyüteç olsun. Büyüteç doğru nesnenin üstüne gelince şekil konturu kısa süre parlasın; seçim için çocuk nesneye dokunsun.",
            "İlk bölümdeki balık oyunu belgeye göre Sihirli Olta adına geçeceği için bu oyunda Sihirli Büyüteç adı korunabilir; iki oyun karışmaz.",
            "Nesne adları ekranda yazılmasın. Yönerge ve şekil adı sesli okunabilsin.",
        ],
        "rounds": [
            "Odada daireye benzeyen iki nesne bulunur: saat ve top. Kare/dikdörtgen nesneler dikkat dağıtıcıdır.",
            "Mutfakta kareye benzeyen nesneler bulunur: peçete ve fayans. Daire ve üçgen nesneler de görünür.",
            "Parkta üçgene benzeyen nesneler bulunur: çatı ve uyarı levhası. Nesnelerin yerleri değişir.",
        ],
        "feedback": [
            "Yanlış nesnede büyüteç buğulanır, nesne seçilmez ve Tekrar dene denir.",
            "Doğru nesnede büyüteç yıldız efekti verir; tüm doğru nesneler bulununca sahnedeki şekiller renkli konturla özetlenir.",
        ],
        "acceptance": "Cevap, nesne adını okumadan yalnız görsel şekil bilgisiyle bulunabilecek; balık ağı veya su altı teması tamamen kaldırılacak.",
    },
    {
        "no": 5,
        "title": "Akıllı Kasa Çekmecesi",
        "group": "Paralarımız / Görsel Tanıma ve Sınıflandırma",
        "accent": TEAL,
        "observed": [
            "Mevcut oyun 5 TL yazan kartı yine 5 TL yazan satıra taşımaktan ibaret. İki taraf da aynı metni verdiği için görsel para tanıma ölçülmüyor.",
            "Gerçek kasa çekmecesi, banknot rengi, büyüklüğü ve ayırt edici görsel özellikleri yok. Altı kart tek sırada küçük görünüyor.",
        ],
        "proposal": [
            "Üstten görünen açılır bir kasa çekmecesi çizilsin; her bölme ayrı ve geniş olsun.",
            "Banknotlar yalnız rakam kartı değil, değerleri ve ayırt edici renkleri görülen stilize TL görselleri olsun. Bir banknot her seferinde banttan gelsin.",
            "Çocuk banknotu doğru bölmeye sürüklesin. Banknota dokununca 20 Türk lirası gibi sesli okunsun.",
            "Bölmeler ilk turda sayıyla etiketli olabilir; sonraki turlarda etiket küçültülüp görsel tanıma ağırlığı artırılabilir.",
        ],
        "rounds": [
            "5 ve 10 TL banknotları karışık sırayla gelir. İki geniş çekmece bölmesine ayrılır.",
            "20 ve 50 TL banknotları farklı sıralarda gelir; renk ve değer karşılaştırılır.",
            "100 ve 200 TL banknotlarıyla sınıflandırma yapılır; son banknotlarda bütün bölmeler birlikte görünür.",
        ],
        "feedback": [
            "Yanlış bölmede çekmece kısa süre kapanır, para geri çıkar ve Değeri tekrar incele denir.",
            "Doğru bölmede para düzgünce yerleşir; tur bitince çekmece kapanır ve kasa ekranında tüm değerler özetlenir.",
        ],
        "acceptance": "Oyun aynı yazıyı aynı yazıyla eşleştirmeye indirgenmeyecek; banknot görseli Android WebView'da da net, taşmadan ve aynı renkte görünecek.",
    },
    {
        "no": 6,
        "title": "Tangram Sandviç Dükkanı",
        "group": "Nesneler ve Geometrik Şekiller / Şekiller Arası Dönüşüm",
        "accent": CORAL,
        "observed": [
            "İki küçük üçgen simgesi iki ayrı boş kutuya bırakılıyor; üçgenlerin birleşip kare oluşturduğu hiç gösterilmiyor.",
            "Sandviç dükkanı, müşteri, tost ekmeği, dönme-yapışma veya pişme animasyonu yok.",
        ],
        "proposal": [
            "Bir tost tezgahı, müşteri siparişi ve ortada büyük kare biçimli tost kalıbı olsun.",
            "İki gerçek üçgen ekmek parçası sürüklenip kalıbın iki yarısına yerleştirilsin. Gerekirse parçaya dokununca 90 derece dönsün; doğru yerde mıknatıs gibi birleşsin.",
            "Parçalar iki ayrı cevap kutusuna gitmesin; bitişte aralarındaki çizgi görünürken tek bir kare oluşturdukları açıkça görülsün.",
            "Şekil tamamlanınca tost makinesi kapanıp açılarak gerçek bir sandviç sunsun.",
        ],
        "rounds": [
            "İki eş üçgen parça birleştirilerek kare tost yapılır.",
            "İki kare parça yan yana getirilerek dikdörtgen tost yapılır; dikkat dağıtıcı bir üçgen parça bulunur.",
            "Dört küçük üçgen doğru yönlere çevrilerek daha büyük bir kare oluşturulur.",
        ],
        "feedback": [
            "Yanlış yönde parça yuvaya oturmaz, hafifçe geri döner ve Parçayı çevirip tekrar dene denir.",
            "Doğru birleşmede kenarlar parlar, tost pişer ve müşteri siparişi teslim alır.",
        ],
        "acceptance": "Her turda oluşan bütün şeklin sınırı açıkça görülecek; çocuk iki ayrı kutuyu doldurmuş değil, yeni bir şekil üretmiş olacak.",
    },
    {
        "no": 7,
        "title": "Geri Dönüşüm Fabrikası",
        "group": "Nesneler ve Geometrik Şekiller / Yapıyı Çözümleme",
        "accent": GOLD,
        "observed": [
            "Ekranda robot veya fabrika yok; beyaz/gri kare, dikdörtgen ve daire parçaları soyut kartlar halinde duruyor.",
            "Kare Kutusu ve Dikdörtgen Kutusu yazıları cevabı doğrudan veriyor; bütün bir yapının parçalara ayrılması gösterilmiyor.",
        ],
        "proposal": [
            "Başlangıçta 2 kare, 2 dikdörtgen ve 1 daireden oluşmuş bütün bir robot görülsün. Ayrıştır düğmesine basılınca robot parçaları bant üzerine düşsün.",
            "Kutularda yalnız yazı yerine büyük şekil siluetleri bulunsun; isimleri kutuya dokunulduğunda sesli okunabilsin.",
            "Çocuk banttaki parçaları uygun kutuya sürüklesin. Kare ve dikdörtgen oranları birbirinden açık biçimde farklı çizilsin.",
            "Tur sonunda ekranda 2 kare + 2 dikdörtgen + 1 daire özeti hem ikonla hem sesle verilsin.",
        ],
        "rounds": [
            "Basit robot 2 kare, 2 dikdörtgen ve 1 daireye ayrılır.",
            "Oyuncak kamyon daire tekerlekler, dikdörtgen gövde ve kare kabin olarak ayrıştırılır.",
            "Roket üçgen burun, dikdörtgen gövde, kare pencere ve daire ayrıntılara ayrılır.",
        ],
        "feedback": [
            "Yanlış kutuya bırakılan parça bant üzerine geri gelir ve Şeklin kenarlarına tekrar bak denir.",
            "Doğru sınıflandırma bittiğinde parçalar yeniden birleşerek nesneyi oluşturur; fabrika onay ışığı yanar.",
        ],
        "acceptance": "Her tur bütün nesneyle başlayıp parçalara ayrılacak ve yeniden birleşmeyle bitecek; yalnız bağımsız şekil kartları sınıflandırılmayacak.",
    },
    {
        "no": 8,
        "title": "Gölge Avcıları",
        "group": "Nesneler ve Geometrik Şekiller / İzdüşüm İlişkisi",
        "accent": PURPLE,
        "observed": [
            "Mevcut ekranda kamp sahnesi ve ışık kaynağı yok; Kare Gölge ve Üçgen Gölge yazıları cevabı zaten söylüyor.",
            "Parti şapkası ile çadır aynı üçgen kutuya gidiyor. Çocuk nesnenin kendine özgü siluetini değil yalnız genel şekil sınıfını eşliyor.",
        ],
        "proposal": [
            "Gün batımında bir kamp alanı kurulsun. Fenerin yönü ve yerde oluşan gerçek koyu siluetler açıkça görülsün.",
            "Her nesnenin kendine özgü tek bir gölgesi olsun; gölge üzerinde şekil adı yazmasın. Nesne gölgenin üstüne sürüklenince tam oturmalı.",
            "Boyut, yön ve çıkıntılar eşleşmenin parçası olsun; aynı genel şekle benzeyen iki nesne tek bir ortak yuvaya gönderilmesin.",
            "Yönerge: Fenerin oluşturduğu gölgeye dikkat et. Her nesneyi kendi gölgesinin üzerine sürükle.",
        ],
        "rounds": [
            "Top, hediye kutusu ve çadır; daire, kare ve üçgen siluetleriyle birebir eşleştirilir.",
            "Sulama kabı, çizme ve şemsiye; sap ve çıkıntıları farklı ayrıntılı gölgelerle eşleştirilir.",
            "Aynı nesneler farklı açılarda döndürülür; çocuk yönü de dikkate alarak doğru gölgeyi bulur.",
        ],
        "feedback": [
            "Yanlış gölgede nesnenin kenarları çakışmaz, parça yerine döner ve Gölgenin dış çizgisine tekrar bak denir.",
            "Doğru eşleşmede nesne gölgeyle kısa süre tek görüntü olur; tüm eşleşmelerde kamp fenerleri yanar.",
        ],
        "acceptance": "Ekrandaki gölgeler yazıyla adlandırılmayacak; doğru cevap gerçek siluet uyumundan anlaşılacak.",
    },
    {
        "no": 9,
        "title": "Dondurmacının Büyük Sorusu",
        "group": "Veriye Dayalı Araştırma / Tam Veri Döngüsü",
        "accent": TEAL,
        "observed": [
            "Yönerge 10 müşteriye sor diyor ama müşteri veya dondurmacı görünmüyor; sistem yalnız Çilekli/Çikolatalı yazan hazır kartı gösteriyor.",
            "Çocuk gerçek bir soru sorma, cevabı dinleme ve veri kaydetme döngüsünü yaşamıyor; yalnız kartı doğru sütuna tıklıyor.",
        ],
        "proposal": [
            "Bir dondurma tezgahı ve sıraya giren müşteriler olsun. Çocuk Sıradaki müşteriye sor düğmesine basınca karakter konuşarak tercihini söylesin.",
            "Her cevap için müşteri resmi veya dondurma topu ilgili resimli sütuna sürüklensin; sütunlar gerçek zamanlı büyüsün.",
            "Son müşteri sonrası grafik büyütülsün ve Hangi aromadan daha çok hazırlamalıyız? sorusu sesli sorulsun.",
            "Tat adlarının yanında büyük çilek, çikolata ve vanilya görselleri bulunsun; okuma yapamayan çocuk da sınıflandırabilsin.",
        ],
        "rounds": [
            "6 müşteri çilekli veya çikolatalı tercihini söyler. Çocuk iki sütunlu resim grafiğini oluşturur ve çoğu bulur.",
            "8 yeni müşteri farklı sırada cevap verir; bu kez çilekli çoğunluk olur. Konum ezberi engellenir.",
            "Üç aroma ve 9 müşteri kullanılır. İki aromanın eşit olabildiği sonuç da seçeneklere eklenir.",
        ],
        "feedback": [
            "Yanlış sütunda müşteri Ben bunu istememiştim diyerek tercihini tekrar seslendirir; işaret yanlış sütuna eklenmez.",
            "Doğru son kararda dondurmacı kazanan aromadan çok sayıda top hazırlar ve grafik sonucu sesli özetler.",
        ],
        "acceptance": "Çocuk her verinin kimden geldiğini görecek, kaydedecek, grafiği tamamlayacak ve grafikten karar verecek; dört aşama da ekranda bulunacak.",
    },
    {
        "no": 10,
        "title": "Sınıf Başkanı Seçimi",
        "group": "Veriye Dayalı Araştırma / Veri Toplama Planı ve Karar",
        "accent": CORAL,
        "observed": [
            "Mevcut sahnede sınıf, adaylar, öğrenciler, oy pusulası ve sandık yok. Hazır isim kartı üç boş sütundan birine dokunduruluyor.",
            "Ali, Ayşe ve Can yalnız ad olarak verildiği için oyun okuma becerisine gereğinden fazla dayanıyor.",
        ],
        "proposal": [
            "Sınıf ortamı, üç adayın büyük portresi ve ortada şeffaf oy sandığı bulunsun. Adayların adı, rengi ve portresi bütün ekranlarda aynı kalsın.",
            "Öğrenciler sırayla sandığa pusula atsın. Çocuk pusulayı açıp üzerindeki aday portresine göre ilgili çetele sütununa sürüklesin.",
            "Pusulaya dokunulduğunda aday adı sesli okunsun. Böylece isimleri henüz okuyamayan öğrenci de katılabilsin.",
            "Oylar bitince sütunlar birlikte görünür ve Sınıf başkanı kim oldu? sorusu portreli seçeneklerle sorulur.",
        ],
        "rounds": [
            "6 pusula ve iki adayla sayma alıştırması yapılır; çok oy alan aday seçilir.",
            "8 pusula ve üç aday kullanılır; pusulaların sırası değişir ve farklı aday kazanır.",
            "9 pusulada eşitlik ihtimali gösterilir. Eşit oy çıkarsa İkinci tur seçim gerekir seçeneği doğru kabul edilir.",
        ],
        "feedback": [
            "Yanlış sütunda pusula geri açılır, adayın portresi parlar ve Adaya tekrar bak denir.",
            "Doğru sonuçta kazanan aday kürsüye gelir; grafik ve toplam oylar ekranda kalır.",
        ],
        "acceptance": "Toplanan her oy çetelede bir işaret artıracak; aday portresi, isim ve sütun sayısı arasında hiçbir tutarsızlık olmayacak.",
    },
    {
        "no": 11,
        "title": "Veterinerin Randevu Defteri",
        "group": "Veriye Dayalı Araştırma / Veriden Araştırma Sorusu Çıkarma",
        "accent": GOLD,
        "observed": [
            "Yönergede tabloyu oku denmesine rağmen ekranda hiçbir tablo veya hayvan resmi yok. Veriler uzun cümlede Kediler 8, Köpekler 3, Kuşlar 5 biçiminde saklı.",
            "Sorular uzay gemisi ve asteroitler üzerinde uzun metin olarak uçuyor; veteriner kliniği ve randevu defteri görünmüyor.",
        ],
        "proposal": [
            "Veteriner kliniği sahnesi açılsın. Ortada üç sütunlu gerçek randevu defteri bulunsun: 8 kedi, 3 köpek ve 5 kuş, sayılabilir ikonlarla gösterilsin.",
            "Veteriner karakteri soruları konuşma animasyonuyla seslendirsin. Her cevap kartında yazıya ek olarak hayvan veya saat/para görseli bulunsun.",
            "Birinci turda tabloyla cevaplanabilecek soru seçilsin; ikinci turda en az gelen hayvan; üçüncü turda kedi ve kuşların toplamı bulunsun.",
            "Toplama sorusunda 8 kedi ve 5 kuş ikonu ortak alana kayarak 13 olacak biçimde görsel sayma desteği versin.",
        ],
        "rounds": [
            "Bu kayıtlarla en çok hangi hayvan geliyor sorusuna cevap verebilir miyiz? Uygun soru resimli kartlar arasından seçilir.",
            "En az gelen hayvan bulunur. 3 köpek ikonu renklenir ve çocuk Köpek kartına dokunur.",
            "Kedilerle kuşların toplamı sorulur. 8 + 5 ikonu birleşir; çocuk 13 sayısını seçer.",
        ],
        "feedback": [
            "Yanlış cevapta asteroit vurma yerine defterde ilgili sütun yumuşakça parlar ve Veriye tekrar bak denir.",
            "Üç doğru tur sonunda veteriner randevu planını tamamlar; hayvanlar sırayla muayene odasına girer.",
        ],
        "acceptance": "Tablo ekranda sürekli görünür olacak; yönergede söylenen 8, 3 ve 5 değerleri ikon sayılarıyla birebir eşleşecek ve uzay teması tamamen kaldırılacak.",
    },
]


doc = BaseDocTemplate(
    OUT,
    pagesize=A4,
    leftMargin=MARGIN_X,
    rightMargin=MARGIN_X,
    topMargin=TOP,
    bottomMargin=BOTTOM,
    title="1. Sınıf Matematik Düzeltmeleri - Devam",
    author="Macera Akademi oyun incelemesi",
    subject="Kargo Robotunun Hatası oyunundan 1. sınıf matematik bölümünün sonuna kadar düzeltme önerileri",
)
frame = Frame(MARGIN_X, BOTTOM, PAGE_W - 2 * MARGIN_X, PAGE_H - TOP - BOTTOM, id="normal")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=draw_header_footer)])

story = []

# Cover
story.append(Spacer(1, 28 * mm))
story.append(p("MACERA AKADEMİ OYUN İNCELEMESİ", cover_kicker))
story.append(p("1. Sınıf Matematik<br/>Düzeltmeleri - Devam", cover_title))
story.append(p("Kargo Robotunun Hatası oyunundan<br/>Veterinerin Randevu Defteri oyununa kadar", cover_sub))
cover_box = Table(
    [[
        p(
            "<b>Kapsam</b><br/>Yüklenen Oyunlar.pdf belgesindeki düzeltmeler Zaman Makinesi ile bitiyor. "
            "Bu belge, oyun listesindeki sırayı izleyerek sonraki 11 oyunu tamamlar.",
            body,
        )
    ]],
    colWidths=[145 * mm],
)
cover_box.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL),
            ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("ROUNDEDCORNERS", [9]),
        ]
    )
)
story.append(cover_box)
story.append(Spacer(1, 22 * mm))
story.append(p("Hazırlanma tarihi: 24 Ağustos 2026", ParagraphStyle("date", parent=body_small, alignment=TA_CENTER, textColor=MID_GREY)))
story.append(PageBreak())

# Global review and standards
story.append(p("İnceleme özeti", h1))
story.append(section_box("Kalan oyunlarda ortak görülen sorunlar", [
    "Oyun adı ve hikayesi değişse de sahne çoğu kez aynı genel motor şablonunda kalıyor. Kargo, asansör ve veteriner oyunlarında uzay gemisi/asteroit sahnesi kullanılıyor.",
    "Birçok gerçek nesne görseli, küçük emoji veya yalnız metin etiketiyle temsil ediliyor. Bu durum 1. sınıf öğrencisini okumaya bağımlı hale getiriyor.",
    "Bazı oyunlarda cevap, hedef kutunun adında açıkça yazıyor; bazı oyunlarda ise doğru eşleşmeyi çıkaracak bilgi hiç görünmüyor.",
    "Üç can, puan ve yönergeyi tekrar dinleme düğmesi mevcut. Bunlar korunmalı; üç farklı tur ve açık hata mesajı bütün oyunlara aynı standartta eklenmeli.",
], PALE_CORAL, CORAL))
story.append(Spacer(1, 5 * mm))
story.append(p("Bütün oyunlarda uygulanacak ortak standart", h2))
standards = [
    ("3 tur", "Her oyun, farklı sayılar/nesneler ve karıştırılmış konumlarla üç ayrı turdan oluşacak. Oyun ancak üçünün de doğru tamamlanmasıyla geçilecek."),
    ("Ses", "Yönerge oyun açılır açılmaz okunacak; hoparlör düğmesiyle tekrar dinlenecek. +, - ve = işaretleri artı, eksi ve eşittir diye seslendirilecek."),
    ("Hata", "Yanlışta Tekrar dene denecek ve yalnız bir can eksilecek. Üç can bitince Canların bitti mesajı ve oyunu yeniden başlat düğmesi gösterilecek."),
    ("1. sınıf erişimi", "Cevap için uzun metin okumak gerekmeyecek. Sayılar, nesneler, hareket ve ses aynı bilgiyi destekleyecek."),
    ("Dokunma", "Butonlar ve sürükleme parçaları büyük olacak; bırakma alanı toleranslı çalışacak ve parça yanlış hedefte yerine dönecek."),
    ("Web - APK eşitliği", "Web ve app/src/main/assets sürümleri aynı sahne, renk, ses, tur ve sonuçları gösterecek. Android WebView'da taşma, kırpılma ve renk kaybı olmayacak."),
]
std_rows = []
for label, desc in standards:
    std_rows.append([p(label, callout_title), p(desc, body_small)])
std_table = Table(std_rows, colWidths=[34 * mm, 137 * mm])
std_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), PALE_PURPLE),
    ("BACKGROUND", (1, 0), (1, -1), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D8D5E1")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(std_table)
story.append(PageBreak())

for game in games:
    story.extend(game_page(game))

# Final implementation checklist
story.append(p("Uygulama ve kabul sırası", h1))
story.append(p("Önceliklendirme", h2))
priority_rows = [
    [p("P0", round_head), p("Kargo Robotunun Hatası, Asansör Düğmeleri, Ankara Simitçisi ve Oyuncakçı, Veterinerin Randevu Defteri", body_small), p("Sahne/yönerge ciddi biçimde uyuşmuyor veya gerekli veri görünmüyor.", body_small)],
    [p("P1", round_head), p("Akıllı Kasa Çekmecesi, Tangram Sandviç Dükkanı, Geri Dönüşüm Fabrikası, Gölge Avcıları", body_small), p("Kazanım metin kartına indirgenmiş; gerçek görsel mekanik kurulmalı.", body_small)],
    [p("P2", round_head), p("Sihirli Büyüteç, Dondurmacının Büyük Sorusu, Sınıf Başkanı Seçimi", body_small), p("Temel oynanış var ama hikaye, veri döngüsü ve 1. sınıf erişimi güçlendirilmeli.", body_small)],
]
priority_table = Table(priority_rows, colWidths=[16 * mm, 85 * mm, 70 * mm])
priority_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), PALE_GOLD),
    ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#D8D5E1")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 7),
    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(priority_table)
story.append(Spacer(1, 6 * mm))
story.append(p("Son kabul kontrolü", h2))
story.extend(bullets([
    "11 oyunun her birinde üç farklı tur tamamlanabiliyor ve bütün tur değerleri ekrandaki nesne sayısıyla aynı.",
    "Yönerge tekrar dinleme düğmesi, üç can ve can bitti akışı hem web hem APK'da aynı çalışıyor.",
    "Uzay gemisi/asteroit, su altı ağı veya boş genel kutu şablonu, oyun hikayesi gerektirmiyorsa görünmüyor.",
    "Cevap hedefin isminde açıkça yazmıyor; doğru seçim görsel/matematiksel düşünmeyle bulunuyor.",
    "Yanlış sürükleme parçayı kaybetmiyor; yeniden deneme mümkün ve çocuk neden yanlış olduğunu görebiliyor.",
    "Telefon ekranında başlık, yönerge, canlar, oyun alanı ve alt kontroller üst üste binmiyor; Türkçe karakterler bozulmuyor.",
    "Her doğru turdan sonra anlamlı bir sahne animasyonu var; yalnız puan artışıyla yetinilmiyor.",
]))
story.append(Spacer(1, 8 * mm))
story.append(section_box("Tamamlanma tanımı", [
    "Bu listedeki 11 oyun düzeltilip üçer turla sınandığında 1. sınıf matematik bölümü belge açısından tamamlanmış kabul edilebilir.",
    "Sonraki sınıfa/derse geçmeden önce aynı oyunların web ve APK görüntüleri yan yana kontrol edilmelidir.",
], PALE_TEAL, TEAL))

doc.build(story)
print(OUT)
