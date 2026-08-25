from __future__ import annotations

import html
import json
import re
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer,
    Table, TableStyle,
)


ROOT = Path("/Users/ceyda/Documents/New project")
OUT = ROOT / "output/pdf/4_sinif_fen_bilimleri_oyunlari_detayli_duzeltmeler.pdf"
GAMES_JSON = ROOT / "tmp/pdfs/fen4_games.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

games = json.loads(GAMES_JSON.read_text(encoding="utf-8"))
assert len(games) == 48

pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

PAGE_W, PAGE_H = A4
MX, TOP, BOTTOM = 17 * mm, 18.5 * mm, 15.5 * mm
INK = colors.HexColor("#272038")
PURPLE = colors.HexColor("#493B73")
TEAL = colors.HexColor("#168A8A")
CORAL = colors.HexColor("#E45F58")
GOLD = colors.HexColor("#DFA52C")
BLUE = colors.HexColor("#3E73A8")
GREEN = colors.HexColor("#4D8D69")
PALE_PURPLE = colors.HexColor("#F2EEFA")
PALE_TEAL = colors.HexColor("#EAF7F5")
PALE_CORAL = colors.HexColor("#FFF0ED")
PALE_GOLD = colors.HexColor("#FFF7E4")
PALE_BLUE = colors.HexColor("#EDF4FA")
MID = colors.HexColor("#7A7687")

base = getSampleStyleSheet()["BodyText"]
body = ParagraphStyle("body", parent=base, fontName="Arial", fontSize=7.7, leading=9.65, textColor=INK, spaceAfter=0.7 * mm)
small = ParagraphStyle("small", parent=body, fontSize=6.95, leading=8.55, spaceAfter=0.45 * mm)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=4.4 * mm, firstLineIndent=-2.8 * mm, bulletIndent=0, spaceAfter=0.55 * mm)
bullet_small = ParagraphStyle("bullet_small", parent=small, leftIndent=4.4 * mm, firstLineIndent=-2.8 * mm, bulletIndent=0, spaceAfter=0.38 * mm)
h1 = ParagraphStyle("h1", parent=body, fontName="Arial-Bold", fontSize=20.5, leading=24, textColor=PURPLE, spaceAfter=3.5 * mm)
h2 = ParagraphStyle("h2", parent=body, fontName="Arial-Bold", fontSize=9.7, leading=11.4, textColor=TEAL, spaceBefore=0.8 * mm, spaceAfter=0.45 * mm)
cover_kicker = ParagraphStyle("cover_kicker", parent=body, fontName="Arial-Bold", fontSize=10, textColor=TEAL, alignment=TA_CENTER, spaceAfter=6 * mm)
cover_title = ParagraphStyle("cover_title", parent=body, fontName="Arial-Bold", fontSize=24, leading=29, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=5 * mm)
cover_sub = ParagraphStyle("cover_sub", parent=body, fontSize=11.5, leading=16, alignment=TA_CENTER, spaceAfter=8 * mm)
game_title = ParagraphStyle("game_title", parent=body, fontName="Arial", fontSize=12.4, leading=14.7, textColor=colors.white, spaceAfter=0)
badge = ParagraphStyle("badge", parent=body, fontName="Arial-Bold", fontSize=14.5, leading=16, textColor=colors.white, alignment=TA_CENTER, spaceAfter=0)
box_title = ParagraphStyle("box_title", parent=body, fontName="Arial-Bold", fontSize=8.7, leading=10.2, textColor=CORAL, spaceAfter=0.45 * mm)
round_head = ParagraphStyle("round_head", parent=small, fontName="Arial-Bold", fontSize=7.2, leading=8.4, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=0)
round_text = ParagraphStyle("round_text", parent=small, fontSize=6.45, leading=7.75, spaceAfter=0)
theme_title = ParagraphStyle("theme_title", parent=cover_title, fontSize=20.5, leading=25, textColor=colors.white)


def clean(value):
    value = re.sub(r"<[^>]+>", "", str(value or ""))
    return html.escape(html.unescape(value).replace("—", "-").replace("–", "-"))


def P(text, style=body):
    return Paragraph(text, style)


def bullets(items, style=bullet):
    return [Paragraph(item, style, bulletText="•") for item in items]


def header(number, title, subtitle, accent):
    t = Table(
        [[P(str(number), badge), P(f"<b>{clean(title)}</b><br/><font size='7.2' color='#F1EEF8'>{clean(subtitle)}</font>", game_title)]],
        colWidths=[14 * mm, 162 * mm],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "CENTER"), ("LEFTPADDING", (1, 0), (1, 0), 9),
        ("RIGHTPADDING", (1, 0), (1, 0), 7), ("ROUNDEDCORNERS", [8]),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def box(title, items, bg, title_color):
    title_style = ParagraphStyle("dynamic_box_title", parent=box_title, textColor=title_color)
    content = [P(title, title_style)] + bullets(items, bullet_small)
    t = Table([[content]], colWidths=[176 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 0.45, colors.HexColor("#D7D3DF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROUNDEDCORNERS", [6]),
    ]))
    return t


def rounds_table(items):
    t = Table(
        [[P("1. TUR", round_head), P("2. TUR", round_head), P("3. TUR", round_head)],
         [P(clean(items[0]), round_text), P(clean(items[1]), round_text), P(clean(items[2]), round_text)]],
        colWidths=[58.7 * mm, 58.7 * mm, 58.6 * mm],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALE_GOLD), ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFCF5")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDCFAB")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
    ]))
    return t


def footer(canv, doc):
    if canv.getPageNumber() == 1:
        return
    canv.saveState()
    canv.setStrokeColor(colors.HexColor("#D9D5E5"))
    canv.setLineWidth(0.6)
    canv.line(MX, PAGE_H - 12.3 * mm, PAGE_W - MX, PAGE_H - 12.3 * mm)
    canv.setFont("Arial", 7.2)
    canv.setFillColor(MID)
    canv.drawString(MX, 8.2 * mm, "4. Sınıf Fen Bilimleri - Ayrıntılı Oyun Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 8.2 * mm, str(canv.getPageNumber()))
    canv.restoreState()


ENGINE = {
    "beltSort": ("bant (yürüyen bant) motoru",
        "Başlıktaki laboratuvar, Dünya, mıknatıs istasyonu veya şehir sahnesi yerine karanlık fabrika bandı açılıyor. "
        "Denemede (Hâl Değişimi Bandı) karar verilecek kart bandın sol kenarında kırpıldı - “Çaydanlıktan buhar çıkar” ifadesinden yalnız “buhar” görünüyordu. "
        "Dört kutulu turlarda kutu etiketleri (“ERİME (katı-sıvı)” gibi) iki satıra taşıp kutu dışına çıkıyor. "
        "Kaynakta her kart için bir wrongHint alanı tanımlı ve bu ipuçları yanlış cevapta doğru kutunun adını doğrudan söylüyor."),
    "serveOrder": ("tepsi-servis motoru",
        "Başlıktaki araştırma çantası, kantin, deney masası, atölye veya şehir maketi yerine ahşap servis tezgâhı açılıyor; "
        "kart havuzu ve etiketler sabit. Ürün/model oluşturma kazanımlarında ekranda hiçbir şey inşa edilmiyor, yalnız kart tepsiye konuyor."),
    "catchDrop": ("radar/kapsül yakalama motoru",
        "Seçenekler kapsül içinde tek tek yukarıdan düşüyor; ipucu “Kapsülün altındaki sarı noktayı çanağın ortasına getir” diliyle veriliyor "
        "ve karar süresi düşme hızına bağlanıyor. Altı radar oyununun tamamında yönerge birebir aynı: “Radarı sürükleyerek doğru cevabı yakala”."),
    "sentenceBuild": ("matbaa/baskı kızağı motoru",
        "Kelime kartlarından büyük harfle başlayan kart ilk sözcüğü, soru işareti kartı son konumu ele veriyor; makine yalnız tek sabit dizilişi kabul ediyor."),
    "orderSequence": ("roket-yakıt motoru",
        "Bilimsel araştırma adımları, deney basamakları, su döngüsü, devre kurma ve Dünya'nın katmanları gibi tamamen yeryüzüne ait konularda bile "
        "kartlar uzayda süzülüyor ve seçilenler YAKIT hunisine gidiyor; kenardaki kartlar ekrandan taşabiliyor."),
    "memoryPairs": ("hafıza kartı motoru",
        "Sahne başlıktan bağımsız yıldızlı uzay; kartlar tavandan iniyor ve “Başla! Kartları çevir” yazısı üst kart sırasının üzerine biniyor. "
        "Can göstergesi 6 kalp ile genel 3 can standardından ayrılıyor."),
    "dragMatch": ("eşleştirme köprüsü motoru",
        "Köprü görseli yok; hedef satırların solunda boş kareler, altta PARÇALAR havuzu var. "
        "Denemede (Çözüm Köprüsü) altı parçanın altısında da son sözcük çipe sığmayıp kesildi: "
        "“Yüksek elektrik tüketimi”, “Su kaynaklarının azalması”, “Çöp dağlarının büyümesi” gibi ifadeler yarım okunuyordu. "
        "Buna karşılık parça-hedef emoji sızıntısı bu derste yok denecek kadar az (40 eşleşmede yalnız 1)."),
    "dragSlider": ("tren-tünel motoru",
        "Dünya'nın dönme süresi ya da erime/kaynama sıcaklığı sorulurken sahnede kırmızı bir tren tünellerden birine giriyor ve sayaç “tren” birimiyle ilerliyor. "
        "Tünel etiketleri sabit sayı seçenekleri; ölçülen olgunun kendisi (dönen Dünya, ısınan madde) ekranda hiç canlanmıyor."),
    "holdFill": ("kronometre motoru",
        "Başlıkta ısıtma deneyi yazıyor ama ekranın ortasında büyük bir KRONOMETRE duruyor; ocak, tencere, madde veya termometre görseli yok. "
        "Denemede görev metni (“Termometreyi 100 °C'ye getir”), “Hedef 100 °C” satırı ve ölçek üzerindeki sarı çizgi hedefi üç ayrı yerde veriyordu. "
        "Gösterge sıfırdan hedefe düz doğrusal artıyor."),
    "graphBuild": ("grafik kurma motoru",
        "Dört sütunlu boş bir grafik, kategori etiketleri ve altta blok deposu var; yapı bu dersin en oturmuş motoru. "
        "Ancak denemede kaynak satırında yalnız birim açıklaması yazıyordu (“Şehrin elektrik üretimi (1 şimşek = %10)”); "
        "hangi kaynağın kaç blok olduğu hiçbir yerde belirtilmemişti. Sayaç ise toplam blok sayısını veriyordu."),
    "codeGrid": ("kargo/robot ızgara motoru",
        "Izgara, engel ve hedef okunaklı; bisiklet ve okul simgeleri konuya uygun. "
        "Ancak ekrandaki şey bir şehir planı değil düz bir labirent ızgarası: sokak, kavşak, ölçek veya plan ögesi yok "
        "ve yön blokları yalnız yukarı/aşağı/sol/sağ oklarından oluşuyor."),
}

TYPE_RISK = {
    "beltSort": "Bant hızı okuma ve karar süresine karışıyor; kenarda kırpılan kart hiç okunamadan can etkiliyor. Daha ağırı: wrongHint ipuçları yanlış cevapta doğru kutunun adını söylüyor, yani bir kez yanlış yapmak cevabı öğreniyor demek oluyor.",
    "serveOrder": "Deney tasarlama, ürün geliştirme ve model kurma kazanımları hazır kart seçmeye iniyor; öğrenci hiçbir şey inşa etmediği için tasarım becerisi ölçülmüyor.",
    "catchDrop": "Doğru cevabı bilmek yetmiyor; düşen kapsüle yetişmek gerekiyor. Kanıt değerlendirme ve arıza teşhisi gibi düşünme gerektiren konular refleks oyununa bağlanıyor; ayrıca altı oyunun ortak yönergesi konuyu hiç anlatmıyor.",
    "sentenceBuild": "Büyük harfli kart ve soru işareti kartı dizilişi ele veriyor; araştırma sorusu kurma kazanımı hazır kartları sıralamaya indirgeniyor.",
    "orderSequence": "Roket-yakıt sahnesi konuyla çelişip kavramı bulanıklaştırıyor; deney basamakları ve bilimsel süreç gibi ciddiyet gerektiren içerikler uzay oyununa dönüşüyor.",
    "memoryPairs": "Eşleştirme, kavramı açıklamadan kart konumunu ezberleyerek de çözülür; görsel hafıza başarısı fen başarısı gibi kayda geçer.",
    "dragMatch": "Kırpılan parça yazıları okunamadığı için eşleştirme tahmine dayanıyor; öğrenci sorunun ne olduğunu tam göremeden çözümünü seçmek zorunda kalıyor.",
    "dragSlider": "Ölçülen olgu ekranda canlanmadığı için öğrenci soyut bir sayıyı tren tüneliyle eşleştiriyor; Dünya'nın dönüşü ya da maddenin ısınması gözlemlenmiyor, ezberlenmiş sayı seçiliyor.",
    "holdFill": "Hedef sıcaklık üç yerde söylendiği için deney kararı öğrenciye bırakılmıyor; oyun bir zamanlama-refleks alıştırmasına dönüşüyor. Daha önemlisi gösterge düz doğrusal arttığı için hâl değişimi sırasında sıcaklığın sabit kaldığı - bu temanın çekirdek kavramı - yanlış modelleniyor.",
    "graphBuild": "Hedef değerler ekranda gösterilmediği için oyun deneme-yanılmayla çözülmek zorunda; “verilerle değerlendirir” kazanımının veri okuma kısmı hiç çalışmıyor.",
    "codeGrid": "Kazanım sürdürülebilir yaşam alanı modelini PLANLAMAYI istiyor; oyun ise hazır bir labirentte engellerden kaçırıyor. Şehir planı ögeleri bulunmadığı için planlama kararı (neden bu güzergâh?) hiç kurulmuyor.",
}

TYPE_FEEDBACK = {
    "beltSort": "Yanlış kutuda bant dursun ve wrongHint doğru kutunun adını SÖYLEMESİN; kart sabitlenip yeniden okunsun, ölçüt soruyla hatırlatılsın. Kenarda kırpılan kart hiç puanlanmasın.",
    "serveOrder": "Yanlış kartta tepsi kilitlenmesin; istek yeniden okunsun ve kartın neden uymadığı deney/model amacı üzerinden gösterilsin.",
    "catchDrop": "Yanlış yakalamada düşme dursun; seçenek sabitlenip yeniden karar verilsin. Kaçan kapsül can yakmasın.",
    "sentenceBuild": "Yanlışta bütün dizi bozulmasın; yalnız son kart geri alınsın. Anlamlı alternatif soru kurulduysa doğru kabul edilsin.",
    "orderSequence": "Yanlış adımda dizi silinmesin; yalnız son seçim geri alınsın ve “bu adımdan önce neyi bilmemiz gerekir?” sorusu sorulsun.",
    "memoryPairs": "Yanlış çiftte kartlar hemen kapanmasın; iki içerik yan yana okunup farkı soran kısa bir ipucu verilsin. Can standardı diğer oyunlarla eşitlensin.",
    "dragMatch": "Yanlış parça başlangıca dönsün; hedef parlatılmasın. Eşleşmenin dayandığı bilimsel ilişki kısa bir soruyla vurgulansın.",
    "dragSlider": "Yanlış değerde doğru sayı tek başına verilmesin; olgu animasyonla gösterilip (Dünya bir tam tur atarken saat ilerlesin) yeniden karar verilsin.",
    "holdFill": "Hedefi geçince ceza verilmesin; maddede ne olduğu görünsün (su kaynamaya başlar, çikolata yanar) ve öğrenci sonucu gözleyerek yeniden denesin.",
    "graphBuild": "Yanlış sütuna blok konursa blok geri dönsün; veri satırı yeniden okunsun ve hangi kategoriye ait olduğu sorulsun. Grafik silinmesin.",
    "codeGrid": "Engele çarpınca bisiklet dursun ve programdaki hatalı adım işaretlensin; tüm program silinmesin. Hata plan üzerinde (“burada ana caddeye girdin”) tarif edilsin.",
}

TYPE_ACCEPT = {
    "beltSort": "İlk iki turda kartlar sabit gelecek; hız ancak üçüncü turda isteğe bağlı açılacak. Kart hiçbir konumda kırpılmayacak, kutu etiketi kutu içinde kalacak ve wrongHint metinleri doğru kutunun adını içermeyecek.",
    "serveOrder": "Seçilen öge ekranda gerçekten bir şey oluşturacak (tabak dolacak, devre kurulacak, maket yükselecek); ürün/model kazanımları yalnız kart seçmeyle tamamlanmış sayılmayacak.",
    "catchDrop": "İlk turda düşme kapalı, seçenekler sabit olacak; başarı doğru karar ve gerekçeyle ölçülecek. Her oyunun yönergesi kendi konusunu anlatacak.",
    "sentenceBuild": "Kartlar küçük harfle gelecek; baş harf ve soru işareti öğrencinin kararı olacak. Son turda öğrenci kendi araştırma sorusunu yazacak.",
    "orderSequence": "Roket-yakıt sahnesi kaldırılacak; adımlar konusuna ait bir sahnede (laboratuvar tezgâhı, su döngüsü şeması, devre masası) sıralanacak ve kartlar ekranda tam içeride kalacak.",
    "memoryPairs": "Kart konumları ve içerik her açılışta karışacak; can sayısı genel standartla (3) eşitlenecek ve her eşleşme bir gerekçe adımıyla doğrulanacak.",
    "dragMatch": "Parça yazıları çipe tam sığacak; hiçbir sözcük kesilmeyecek. Hedef alanlar en az 44 px olacak ve her eşleşme bir gerekçe sorusuyla doğrulanacak.",
    "dragSlider": "Tren-tünel sahnesi kaldırılacak; ölçülen olgu ekranda canlanacak (Dünya dönecek, termometre ısınan maddeyle birlikte yükselecek) ve karar gözleme dayanacak.",
    "holdFill": "Hedef sıcaklık görev metninde, “Hedef” satırında ve ölçek işaretinde yazılı olmayacak; öğrenci maddeye ve amaca bakarak karar verecek. Ekranda gerçek ocak, kap ve madde bulunacak; hâl değişimi sırasında sıcaklığın sabit kaldığı gösterilecek.",
    "graphBuild": "Kategori hedefleri ya kaynak satırında okunur biçimde verilecek ya da öğrenci nesneleri sayarak kendisi çıkaracak; toplam blok sayacı gizlenecek ve grafiğe sayı ölçeği eklenecek.",
    "codeGrid": "Izgara gerçek bir şehir planına dönüşecek: sokaklar, kavşaklar ve en az iki işaret noktası bulunacak. Güzergâh seçimi gerekçelendirilecek ve görev metni rotayı söylemeyecek.",
}


DESIGNS = {
"f01": ("Gerçek bir laboratuvar sahnesi çizilsin; ifade bir bilim insanının defterinden okunsun, kart bantta akmasın ve kırpılmasın. wrongHint metinleri doğru kutuyu söylemesin.",
        "Bilimsel görünen ama kanıtsız ifadeler çeldirici olsun; ölçüt (test edilebilirlik, tekrarlanabilirlik) tartışılsın.",
        "Öğrenci bir iddiayı bilimsel yapmak için hangi kanıtın gerektiğini söylesin."),
"f02": ("Genel radar yönergesi kaldırılsın; kaynak kartları (ansiklopedi, blog, kurum sitesi, sosyal medya) sabit dursun ve her kartta yazar, tarih, kurum görünsün.",
        "Aynı bilgiyi veren iki kaynak ölçütlerle karşılaştırılsın.",
        "Öğrenci seçtiği kaynağı “güvenilir çünkü...” diye gerekçelendirsin."),
"f03": ("Gerçek bir araştırma masası çizilsin; adımlar defterde satır satır oluşsun ve roket kaldırılsın.",
        "Atlanan adımın sonucu gösterilsin: soru sormadan veri toplamak neden işe yaramaz?",
        "Öğrenci kendi merak ettiği konu için adımları sırayla yazsın."),
"f04": ("Gerçek bilim insanı çalışma sahneleri kullanılsın; eşleşince özelliğin davranışa nasıl döküldüğü kısa animasyonla gösterilsin.",
        "Yakın özellikler çeldirici olsun (meraklı/aceleci, sabırlı/kararsız).",
        "Öğrenci kendisinde gördüğü bir bilim insanı özelliğini örnekle anlatsın."),
"f05": ("Gerçek bir çanta ve masa sahnesi çizilsin; seçilen kaynak çantaya girsin ve içeriği görünsün.",
        "Güvenilir görünen ama uygun olmayan kaynaklar çeldirici olsun.",
        "Öğrenci kendi araştırması için üç kaynak seçip nedenini söylesin."),
"f06": ("Gerçek bir araştırma defteri açılsın; kurulan soru deftere yazılsın ve iyi soru ölçütleri (test edilebilir mi?) yanında dursun. Kartlar küçük harfle gelsin.",
        "Test edilebilir ve edilemez sorular karşılaştırılsın.",
        "Öğrenci kendi araştırma sorusunu hazır kart olmadan yazsın."),
"f07": ("Gerçek bir besin masası ve içerik etiketi çizilsin; besin kartı tabakta görünsün ve bant durdurulsun.",
        "Birden çok içerik taşıyan besinler eklensin; “en çok hangisi?” ölçütü tartışılsın.",
        "Öğrenci kendi öğününde hangi içeriğin baskın olduğunu söylesin."),
"f08": ("Gerçek besin fotoğrafları kullanılsın; eşleşince vitaminin vücuttaki etkisi kısa sahneyle gösterilsin. A vitamini ile havuç arasındaki aynı emoji kullanımı kaldırılsın - tek sızıntı noktası burası.",
        "Bir besinde birden çok vitamin bulunabildiği gösterilsin.",
        "Öğrenci bir vitamini ve kaynağını kendi cümlesiyle anlatsın."),
"f09": ("Gerçek bir tabak çizilsin; seçilen besin tabağa yerleşsin ve tabağın dengesi (protein/karbonhidrat/sebze oranı) görsel olarak oluşsun.",
        "Dengesiz tabak örnekleri karşılaştırılsın; eksik grup gösterilsin.",
        "Öğrenci kendi dengeli öğününü kurup neden dengeli olduğunu açıklasın."),
"f10": ("Gerçek vücut şeması kullanılsın; kart çevrilince içeriğin görevi ilgili organda/dokuda canlansın.",
        "Bir içeriğin birden çok görevi olduğu gösterilsin.",
        "Öğrenci bir besin içeriğinin görevini kendi cümlesiyle anlatsın."),
"f11": ("Gerçek bir deney tezgâhı çizilsin; adımlar tezgâhta uygulanan işler olarak sıralansın ve roket kaldırılsın.",
        "Değişken kavramı işlensin: hangi adımda neyi sabit tutuyoruz?",
        "Öğrenci bir besin testi deneyini adım adım anlatsın."),
"f12": ("Genel radar yönergesi kaldırılsın; beslenme-sağlık ilişkisi gerçek bir öncesi-sonrası sahnesiyle gösterilsin ve seçenekler sabit dursun.",
        "Kısa ve uzun vadeli etkiler ayrı örneklerle karşılaştırılsın.",
        "Öğrenci bir beslenme alışkanlığının sağlığa etkisini neden-sonuç kurarak anlatsın."),
"f13": ("Gerçek bir Dünya kesiti çizilsin; öge kartı ilgili kürenin üzerine yerleşsin ve bant durdurulsun. Dört kutu etiketi kutu içinde kalsın.",
        "Birden çok küreye ait olabilen ögeler çeldirici olsun (bulut, nehir yatağı).",
        "Öğrenci çevresinden bir ögeyi hangi küreye koyacağını gerekçesiyle söylesin."),
"f14": ("Gerçek bir Dünya kesit modeli çizilsin; katmanlar kesitin üzerine içten dışa yerleşsin ve roket kaldırılsın.",
        "Katmanların kalınlık ve sıcaklık farkı gösterilsin.",
        "Öğrenci katmanları içten dışa kendi sözcükleriyle anlatsın."),
"f15": ("Gerçek bir Dünya-Güneş animasyonu kullanılsın; eşleşen hareket ekranda gerçekleşsin (Dünya dönerken gece-gündüz oluşsun).",
        "Dönme ve dolanma karıştırılabilecek biçimde sunulup ayırt ettirilsin.",
        "Öğrenci bir hareketin sonucunu gözleyerek anlatsın."),
"f16": ("Genel radar yönergesi kaldırılsın; Dünya'nın şekline dair kanıtlar (ufukta kaybolan gemi, uydu görüntüsü, gölge) gerçek görsellerle sunulsun.",
        "Gözleme dayalı kanıt ile duyuma dayalı iddia ayrılsın.",
        "Öğrenci Dünya'nın şekline dair bir kanıtı kendi cümlesiyle açıklasın."),
"f17": ("Tren-tünel sahnesi kaldırılsın; ekranda dönen bir Dünya ve saat/takvim olsun. Öğrenci süreyi bu animasyonu gözleyerek belirlesin.",
        "Dönme (24 saat) ile dolanma (365 gün) yan yana karşılaştırılsın.",
        "Öğrenci hangi hareketin hangi süreye karşılık geldiğini gerekçesiyle söylesin."),
"f18": ("Gerçek Dünya kesiti kullanılsın; kart çevrilince kürenin içeriği o kesitte vurgulansın.",
        "Küreler arası geçiş bölgeleri gösterilsin (deniz yüzeyi, atmosfer sınırı).",
        "Öğrenci bir küreyi ve içeriğini kendi cümlesiyle tanıtsın."),
"f19": ("Gerçek bir mutfak/laboratuvar sahnesi çizilsin; olay kısa animasyonla gösterilsin (çaydanlıktan buhar yükselsin). KRİTİK: kart hiçbir kenarda kırpılmasın - denemede “Çaydanlıktan buhar çıkar” ifadesinden yalnız “buhar” görünüyordu ve bu sözcük tek başına cevabı ele veriyordu.",
        "Kart metinlerinde hâl değişiminin adını çağrıştıran sözcükler kullanılmasın; olay gözlemle anlatılsın.",
        "Öğrenci evinde gözlediği bir hâl değişimini adlandırıp anlatsın."),
"f20": ("Gerçek bir ısı akışı animasyonu kullanılsın; eşleşince ısının maddeye girdiği veya çıktığı ok olarak gösterilsin.",
        "Isı alan ve veren değişimler yan yana karşılaştırılsın.",
        "Öğrenci bir hâl değişiminin ısı alıp vermediğini gerekçesiyle söylesin."),
"f21": ("KRONOMETRE kaldırılsın; ekranda gerçek ocak, kap ve madde olsun. KRİTİK: hedef sıcaklık görev metninde, “Hedef” satırında ve ölçek işaretinde olmak üzere üç yerde yazılı - hepsi kaldırılsın, öğrenci maddeye ve amaca bakarak karar versin.",
        "Hâl değişimi sırasında sıcaklığın SABİT kaldığı gösterilsin - şu anki düz doğrusal artış bu temanın çekirdek kavramını yanlış modelliyor.",
        "Öğrenci ısıtmayı ne zaman durduracağını maddede gördüğü değişime bakarak söylesin."),
"f22": ("Gerçek bir su döngüsü şeması çizilsin; damla şemanın üzerinde yolculuk etsin ve roket kaldırılsın.",
        "Her adımda hangi hâl değişiminin olduğu sorulsun.",
        "Öğrenci su döngüsünü hâl değişimi adlarıyla anlatsın."),
"f23": ("Tren-tünel sahnesi kaldırılsın; ekranda ısınan bir madde ve termometre olsun, sıcaklık maddeyle birlikte değişsin.",
        "Farklı maddelerin erime/kaynama noktaları karşılaştırılsın.",
        "Öğrenci bir maddenin hâl değiştirdiği sıcaklığı gözleyerek söylesin."),
"f24": ("Gerçek bir deney tezgâhı çizilsin; seçilen malzeme tezgâha yerleşsin ve deney düzeneği görünür biçimde kurulsun.",
        "Güvenlik malzemeleri (gözlük, eldiven) ayrı bir ölçüt olarak istensin.",
        "Öğrenci kendi deneyi için malzeme listesi yazsın."),
"f25": ("Gerçek bir mıknatıs ve malzeme kutusu çizilsin; madde kartı mıknatısa yaklaştığında çekilip çekilmediği animasyonla görünsün ve bant durdurulsun.",
        "Metal olup çekilmeyen maddeler (alüminyum, bakır) çeldirici olsun; “her metal çekilmez” kuralı kurulsun.",
        "Öğrenci evinden bir nesneyi tahmin edip test etsin."),
"f26": ("Gerçek iki mıknatıs çizilsin; kutuplar yaklaştırılınca itme/çekme animasyonla gösterilsin.",
        "Aynı ve zıt kutup eşleşmeleri örüntü olarak sunulup genelleme yaptırılsın.",
        "Öğrenci kuralı kendi cümlesiyle ifade etsin: “Aynı kutuplar...”"),
"f27": ("Genel radar yönergesi kaldırılsın; mıknatısın kullanıldığı gerçek nesneler (hoparlör, buzdolabı kapağı, pusula) sahnede görünsün.",
        "Mıknatısın görünmeyen kullanımları eklensin (elektrik motoru, kart okuyucu).",
        "Öğrenci evinde mıknatıs kullanılan bir yeri bulup anlatsın."),
"f28": ("Gerçek kullanım sahneleri kullanılsın; kart çevrilince mıknatısın oradaki işi animasyonla gösterilsin.",
        "Aynı kullanımın farklı yerlerde karşımıza çıktığı gösterilsin.",
        "Öğrenci bir mıknatıs kullanımını ve nedenini anlatsın."),
"f29": ("Gerçek bir deney tezgâhı çizilsin; adımlar tezgâhta uygulanan işler olarak sıralansın ve roket kaldırılsın.",
        "Tahmin-test-sonuç döngüsü vurgulansın: tahmin yanlış çıkarsa ne yapılır?",
        "Öğrenci bir mıknatıs deneyini tahminiyle birlikte anlatsın."),
"f30": ("Gerçek bir atölye tezgâhı çizilsin; seçilen malzeme ile pusula adım adım kurulsun ve sonunda iğne kuzeyi göstersin.",
        "Gereksiz ama cazip malzemeler çeldirici olsun.",
        "Öğrenci pusulanın neden kuzeyi gösterdiğini açıklasın."),
"f31": ("Gerçek bir devre şeması çizilsin; eşleşen eleman devrede yerini alsın ve görevi çalışırken görünsün (pil akım versin, ampul yansın).",
        "Benzer görevli elemanlar çeldirici olsun (anahtar/duy).",
        "Öğrenci bir devre elemanının görevini kendi cümlesiyle anlatsın."),
"f32": ("Gerçek bir devre masası çizilsin; adımlar masada uygulanan işler olarak sıralansın ve son adımda devre gerçekten çalışsın. Roket kaldırılsın.",
        "Yanlış sırada kurulan devrenin neden çalışmadığı gösterilsin.",
        "Öğrenci devre kurma adımlarını kendi sözcükleriyle anlatsın."),
"f33": ("Gerçek enerji kaynağı görselleri çizilsin (güneş paneli, rüzgâr türbini, kömür ocağı); kart kaynağın sahnesinde görünsün ve bant durdurulsun.",
        "Tartışmalı örnekler eklensin (biyokütle, hidroelektrik); ölçüt savunulsun.",
        "Öğrenci bir kaynağı neden o gruba koyduğunu açıklasın."),
"f34": ("Gerçek bir elektrik atölyesi çizilsin; seçilen eleman tezgâha konsun ve devre görünür biçimde tamamlansın.",
        "Eksik eleman senaryoları eklensin: pil olmadan devre çalışır mı?",
        "Öğrenci basit bir devre için gereken elemanları kendisi sıralasın."),
"f35": ("Genel radar yönergesi kaldırılsın; ekranda çalışmayan gerçek bir devre olsun ve öğrenci arızayı devreye bakarak bulsun.",
        "Birden çok olası arıza verilsin; öğrenci test ederek elesin.",
        "Öğrenci arızayı ve nasıl bulduğunu kanıtıyla anlatsın."),
"f36": ("KRİTİK: hedef değerler ekranda görünmüyor - kaynak satırında yalnız birim açıklaması var. Veriler ya kaynak satırında okunur biçimde verilsin ya da öğrenci şehrin enerji santrallerini sayarak kendisi çıkarsın. Toplam blok sayacı gizlensin.",
        "Grafik tamamlanınca “hangi kaynak baskın, yenilenebilir payı ne kadar?” soruları sorulsun.",
        "Öğrenci grafiği yorumlayıp şehir için bir enerji önerisi getirsin."),
"f37": ("Gerçek gündüz ve gece sahneleri çizilsin; ışık kaynağı kartı kendi ortamında görünsün ve bant durdurulsun.",
        "Işık yaymayan ama parlayan cisimler (ay, ayna) çeldirici olsun; kaynak-yansıtıcı ayrımı kurulsun.",
        "Öğrenci çevresinden bir doğal ve bir yapay kaynak söylesin."),
"f38": ("Gerçek bir karanlık kutu deneyi çizilsin; adımlar kutuda uygulanan işler olarak sıralansın ve son adımda sonuç görülsün. Roket kaldırılsın.",
        "Değişken kontrolü vurgulansın: ışık dışında ne sabit tutuluyor?",
        "Öğrenci deneyin sonucunu ve nedenini anlatsın."),
"f39": ("Genel radar yönergesi kaldırılsın; ekranda karanlık bir oda olsun ve öğrenci ışığı açıp kapayarak görmenin koşullarını gözlesin.",
        "Işık, göz ve cisim üçlüsü ayrı ayrı test edilsin.",
        "Öğrenci görmek için nelerin gerektiğini gözlemine dayanarak söylesin."),
"f40": ("Gerçek bir gece şehri sahnesi çizilsin; ışık kirliliği durumu ekranda görünsün ve eşleşen etki canlılarda canlansın (kuşlar yön şaşırsın).",
        "Farklı canlıların farklı etkilenmesi gösterilsin.",
        "Öğrenci ışık kirliliğinin bir etkisini kendi cümlesiyle anlatsın."),
"f41": ("Gerçek bir sokak sahnesi çizilsin; seçilen çözüm sokakta uygulansın ve gökyüzü kararıp yıldızlar görünsün.",
        "Çözümlerin maliyet ve etkisi karşılaştırılsın; gerekçelendirme istensin.",
        "Öğrenci kendi mahallesi için bir çözüm önerip gerekçelendirsin."),
"f42": ("Gerçek ışık kaynağı görselleri kullanılsın; kart çevrilince kaynağın özelliği (sıcaklık, süreklilik, parlaklık) gösterilsin.",
        "Benzer görünen kaynakların farkları karşılaştırılsın.",
        "Öğrenci iki ışık kaynağını bir özelliğe göre karşılaştırsın."),
"f43": ("Gerçek bir şehir sahnesi çizilsin; uygulama şehirde görünsün ve sonucu (yeşil alan artsın, hava kirlensin) canlansın. Bant durdurulsun.",
        "Kısa vadede iyi uzun vadede kötü uygulamalar çeldirici olsun.",
        "Öğrenci bir uygulamayı sürdürülebilirlik ölçütüyle değerlendirsin."),
"f44": ("Gerçek bir maket tepsisi çizilsin; seçilen öge makete yerleşsin ve şehir gözle görülür biçimde kurulsun. Kazanım MODEL geliştirmeyi istiyor.",
        "Ögeler arası ilişki sorulsun: toplu taşıma olmadan yaya bölgesi işe yarar mı?",
        "Öğrenci kendi şehir modelini üç ögeyle kurup anlatsın."),
"f45": ("Gerçek bir proje panosu çizilsin; adımlar panoda görselleşsin ve roket kaldırılsın.",
        "Değerlendirme ve paylaşma adımları vurgulansın: proje bitince ne yapılır?",
        "Öğrenci kendi projesi için adımları sırayla yazsın."),
"f46": ("KRİTİK: altı parçanın altısında da son sözcük çipe sığmayıp kesiliyor (“...tüketimi”, “...azalması”, “...büyümesi” okunmuyor). Yazılar tam sığacak biçimde yerleşsin ve sorun-çözüm ilişkisi şehir sahnesinde canlansın.",
        "Bir soruna birden çok çözüm önerilip karşılaştırılsın.",
        "Öğrenci kendi çevresinden bir sorun ve çözüm önersin."),
"f47": ("Hedef değerler ekranda görünsün ya da öğrenci anket cevaplarını sayarak veriyi kendisi çıkarsın; toplam simge sayacı gizlensin ve grafiğe ölçek eklensin.",
        "Grafik tamamlanınca “en çok hangi ulaşım, sürdürülebilir olan hangisi?” soruları sorulsun.",
        "Öğrenci grafiği yorumlayıp okuluna bir ulaşım önerisi getirsin."),
"f48": ("Izgara gerçek bir şehir planına dönüşsün: sokaklar, kavşaklar, park ve okul işaretlensin. Güzergâh seçimi gerekçelendirilsin (neden ana cadde değil?).",
        "Farklı başlangıç noktaları ve güvenlik ölçütleri verilsin.",
        "Öğrenci çizdiği bisiklet yolunu ve neden o yolu seçtiğini anlatsın."),
}

assert set(DESIGNS) == {g["id"] for g in games}


def config_summary(game):
    n = game.get("n", {})
    t = game["type"]
    if t == "beltSort":
        wh = n.get("wrongHint")
        ek = f" {wh} kartın tamamında wrongHint metni tanımlı ve doğru kutunun adını içeriyor." if wh else ""
        return f"Kaynakta {n.get('items','?')} kart ve {n.get('bins','')} kutuları tanımlı; yapı tek gerçek-zamanlı bant turu.{ek}"
    if t == "memoryPairs":
        return f"Kaynakta {n.get('pairs','?')} çift tanımlı; tek tur var ve kart içerikleri sabit."
    if t == "catchDrop":
        return f"Kaynakta {n.get('rounds','?')} düşen-seçenek turu var; doğru ve çeldiriciler önceden sabit, hız ile karar aynı puana bağlanıyor."
    if t == "serveOrder":
        return f"Kaynakta {n.get('customers','?')} istek tanımlı; kart havuzu sabit ve seçilen öge ekranda bir şey inşa etmiyor."
    if t == "sentenceBuild":
        return f"Kaynakta {n.get('rounds','?')} cümle kurulumu var; her sorunun tek doğru dizilişi tanımlı."
    if t == "orderSequence":
        return f"Kaynakta {n.get('items','?')} kartlık tek sıra var; doğru sıra sabit ve yeni tur üretilmiyor."
    if t == "dragMatch":
        return f"Kaynakta {n.get('sources','?')} parça ve {n.get('targets','?')} hedef var; tek sabit eşleştirme turu."
    if t == "dragSlider":
        return f"Kaynakta {n.get('rounds','?')} tur var; sabit sayı seçeneklerinden biri seçiliyor ve ölçülen olgunun animasyonu tanımlı değil."
    if t == "holdFill":
        return f"Kaynakta {n.get('rounds','?')} ısıtma turu var; hedef sıcaklık üç turun üçünde de görev metninde açıkça söyleniyor."
    if t == "graphBuild":
        return f"Kaynakta {n.get('categories','?')} kategori ve toplam {n.get('blocks','?')} blok tanımlı; kategori hedefleri kaynakta var ama ekranda gösterilmiyor."
    if t == "codeGrid":
        return f"Kaynakta {n.get('rounds','?')} görev haritası var; program yalnız ekran yönü oklarından oluşuyor ve plan ögesi tanımlı değil."
    return f"Kaynakta {n.get('rounds','?')} tur tanımlı."


GROUP_FOCUS = {
    "Tema 1 · Bilime Yolculuk": [
        "Bilimsel bilgi ölçütü kanıtla kurulmalı; wrongHint ipuçları doğru kutuyu söylememeli.",
        "Kaynak güvenilirliği radar refleksinden çıkarılıp yazar-tarih-kurum bilgisiyle değerlendirilmeli.",
        "Araştırma sorusu kazanımı son turda öğrencinin kendi sorusuna bağlanmalı.",
    ],
    "Tema 2 · Sağlıklı Besleniyorum": [
        "Besin içeriği ve vitamin kazanımları gerçek besin görselleriyle çalışmalı.",
        "Dengeli tabak kazanımında tabak ekranda gerçekten kurulmalı; oranlar görünmeli.",
        "Deney kazanımlarında değişken kontrolü vurgulanmalı; roket sahnesi kaldırılmalı.",
    ],
    "Tema 3 · Dünya'mızı Keşfedelim": [
        "Küre ve katman kazanımları gerçek Dünya kesiti üzerinde çalışmalı.",
        "Dünya'nın hareketleri animasyonla gözlemlenmeli; süre kararı tren-tünel yerine gözleme dayanmalı.",
        "Şekil kanıtı gerçek gözlem görselleriyle (ufuk, gölge, uydu) sunulmalı.",
    ],
    "Tema 4 · Maddenin Değişimi": [
        "Isıtma deneyinde hedef sıcaklık söylenmemeli ve hâl değişimi sırasında sıcaklığın sabit kaldığı doğru modellenmeli.",
        "Hâl değişimi kartlarında cevabı çağrıştıran sözcükler kullanılmamalı; olay gözlemle anlatılmalı.",
        "Su döngüsü ve ısı alışverişi gerçek şema ve animasyonla gösterilmeli.",
    ],
    "Tema 5 · Mıknatısı Keşfediyorum": [
        "Çekme testi animasyonla görünmeli; metal olup çekilmeyen maddeler çeldirici olarak eklenmeli.",
        "Kutup etkileşimi iki gerçek mıknatısla gösterilip genelleme yaptırılmalı.",
        "Pusula atölyesinde ürün ekranda gerçekten kurulmalı ve iğne kuzeyi göstermeli.",
    ],
    "Tema 6 · Enerji Dedektifleri": [
        "Devre kazanımlarında devre ekranda gerçekten kurulmalı ve çalışmalı.",
        "Arıza teşhisi radar refleksinden çıkarılıp gerçek bir devre üzerinde yapılmalı.",
        "Enerji grafiğinde hedef değerler ekranda okunur olmalı.",
    ],
    "Tema 7 · Işığın Peşinde": [
        "Görme kazanımı karanlık oda deneyiyle gözlemlenmeli; radar yönergesi kaldırılmalı.",
        "Işık kaynağı ile yansıtıcı cisim ayrımı çeldiricilerle kurulmalı.",
        "Işık kirliliği kazanımı gece şehri sahnesinde canlandırılıp çözüm gerekçelendirilmeli.",
    ],
    "Tema 8 · Sürdürülebilir Şehirler": [
        "Model kurma kazanımlarında maket ekranda gerçekten yükselmeli.",
        "Çözüm köprüsünde parça yazıları kesilmemeli; sorun-çözüm ilişkisi şehir sahnesinde görünmeli.",
        "Bisiklet yolu kazanımı labirentten çıkarılıp gerçek şehir planına ve güzergâh gerekçesine bağlanmalı.",
    ],
}

GROUP_COLORS = [CORAL, TEAL, PURPLE, GOLD, BLUE, GREEN, CORAL, PURPLE]

# Kaç oyun ortak "genel yönerge" kullanıyor?
generic_prompt = [g for g in games if "doğru cevabı yakala" in g["instruction"].lower()]
belt_n = sum(1 for g in games if g["type"] == "beltSort")
answer_leak = ["h02", "h09", "h10", "h26", "h29", "h05", "h18"]

wrong_hint_total = sum(g["n"].get("wrongHint", 0) for g in games)
generic_count = sum(1 for g in games if "doğru cevabı yakala" in g["instruction"].lower())

doc = BaseDocTemplate(
    str(OUT), pagesize=A4, rightMargin=MX, leftMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
    title="4. Sınıf Fen Bilimleri Oyunları - Ayrıntılı Düzeltmeler", author="Macera Akademi oyun incelemesi",
)
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

story = [Spacer(1, 14 * mm), P("MACERA AKADEMİ", cover_kicker),
         P("4. Sınıf Fen Bilimleri Oyunları<br/>Ayrıntılı Düzeltmeler", cover_title),
         P("36 oyunun kaynak yapılandırması çıkarılarak ve 13 oyun motoru 390x844 telefon görünümünde tek tek açılıp denenerek hazırlanmıştır.", cover_sub)]
cover_box = Table([[P("<b>Kapsam</b><br/>Bu belge h01-h36 arasındaki 2. sınıf hayat bilgisi oyunlarının tamamını kapsar. Her oyun için denemede görülen mevcut yapı, eğitimsel risk, özgün sahne ve yeni oynanış, üç kademeli tur, geri bildirim ve ölçülebilir kabul koşulları ayrı ayrı verilir.")]], colWidths=[153 * mm])
cover_box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL), ("BOX", (0, 0), (-1, -1), 0.7, TEAL),
                               ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                               ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12)]))
story += [cover_box, Spacer(1, 8 * mm), P("İnceleme yöntemi", h2)]
story += bullets([
    "2. sınıf hayat bilgisi listesindeki 36 oyunun kaynak yapılandırmaları çıkarıldı; altı öğrenme alanı ve on üç motor karşılaştırıldı.",
    "Bant, servis, radar, matbaa, roket, hafıza, köprü, tren, tuş takımı, çetele, kargo ve kronometre motorları 390x844 telefon görünümünde açıldı; kart akışı, yerleşim, dokunma alanları ve cevabı taşıyan ögeler doğrudan gözlendi.",
    "Düzeltmeler kazanım-mekanik uyumu, başlık-sahne uyumu, cevabı sızdıran ögeler, yerleşim/kırpılma hataları, üç kademeli tur ve test edilebilir kabul koşulunu birlikte ele alır.",
])
story += [PageBreak()]

story += [P("Testten çıkan öncelikli bulgular", h1)]
story += [box(f"1. Yanlış cevap verildiğinde doğru cevap ekrana yazılıyor - {wrong_hint_total} kartta",
    [f"Sekiz bant oyununun tamamında her kart için bir wrongHint metni tanımlı ve bu metinler yanlış kutuya bırakıldığında doğru kutunun adını doğrudan söylüyor: “Kanıtsız his BİLİMSEL DEĞİLDİR!”, “Katı - sıvı = ERİME!”, “Tekrarlanabilirlik BİLİMSEL bilginin özelliğidir!”. Toplam {wrong_hint_total} bant kartının {wrong_hint_total} tanesi bu şekilde. Bir kez yanlış yapmak cevabı öğrenmek anlamına geldiği için ikinci denemede düşünmeye gerek kalmıyor; bu, oyunlarda uygulanan “yanlışta doğru cevabı açma” ilkesinin tam tersi."],
    PALE_CORAL, CORAL), Spacer(1, 1.7 * mm)]
story += [box("2. Isıtma deneyi hâl değişimini yanlış modelliyor",
    ["Isıtma Deneyi'nin ekranında ocak, kap veya madde yok; ortada büyük bir KRONOMETRE duruyor. Hedef sıcaklık üç ayrı yerde veriliyor: görev metni (“Termometreyi 100 °C'ye getir”), “Hedef 100 °C” satırı ve ölçek üzerindeki sarı çizgi. Bilimsel olarak daha önemlisi, gösterge sıfırdan hedefe düz doğrusal artıyor - oysa bu temanın çekirdek kavramı, hâl değişimi sırasında maddeye ısı verilmeye devam edilse bile sıcaklığın SABİT kalmasıdır. Oyun bu kavramı öğretmek yerine tersini gösteriyor."],
    PALE_GOLD, GOLD), Spacer(1, 1.7 * mm)]
story += [box("3. Grafik oyunlarında hedef değerler ekranda yok",
    ["Enerji Grafiği'nde kaynak satırında yalnız “Şehrin elektrik üretimi (1 şimşek = %10)” yazıyor; hangi kaynağın kaç şimşek olduğu hiçbir yerde belirtilmemiş. Hedefler kaynak dosyada tanımlı (Güneş 3, Rüzgâr 2, Hidro 2, Kömür 3) ama ekrana yazılmıyor. Şehir Verisi Grafiği'nde de durum aynı (Yürüyerek 5, Bisikletle 3, Servisle 4, Özel araç 2). İki oyun da ancak deneme-yanılmayla çözülebiliyor ve “verileri analiz eder” kazanımının okuma kısmı hiç çalışmıyor. Bu, 4. sınıf sosyal bilgilerdeki Su Tüketim Grafiği'nde raporladığım kusurun aynısı."],
    PALE_BLUE, BLUE), Spacer(1, 1.7 * mm)]
story += [box("4. Köprü ve bant oyunlarında yazılar kesiliyor",
    ["Çözüm Köprüsü'nde altı parçanın altısında da son sözcük çipe sığmayıp kesildi: “Yüksek elektrik tüketimi”, “Su kaynaklarının azalması”, “Trafik ve hava kirliliği”, “Çöp dağlarının büyümesi” gibi ifadeler yarım okunuyordu - öğrenci sorunun ne olduğunu tam göremeden çözümünü seçmek zorunda kalıyor. Hâl Değişimi Bandı'nda ise kart bandın sol kenarında kırpıldı ve “Çaydanlıktan buhar çıkar” ifadesinden yalnız “buhar” göründü; bu sözcük tek başına BUHARLAŞMA cevabını ele veriyordu. Dört kutulu turlarda kutu etiketleri de kutu dışına taşıyor."],
    PALE_TEAL, TEAL), Spacer(1, 1.7 * mm)]
story += [box("5. Emoji sızıntısı bu derste yok denecek kadar az; teknik çökme yok",
    [f"Sekiz köprü oyunundaki 40 eşleşme tek tek karşılaştırıldı; parça ile hedefin aynı emojiyi paylaştığı yalnız 1 durum bulundu (Vitamin Köprüsü'nde havuç simgesi hem “A vitamini” parçasında hem “Havuç, ıspanak, kabak” hedefinde). Diğer derslerde bu kusur yaygındı; fen bilimlerinde neredeyse tamamen giderilmiş - bu dersin olumlu farkı. Buna karşılık {generic_count} radar oyununun tamamı aynı yönergeyi kullanıyor: “Radarı sürükleyerek doğru cevabı yakala”. f01-f48 arasındaki 48 oyunun tamamı yüklendi; motorlarda çökme veya konsol hatası oluşmadı."],
    PALE_PURPLE, PURPLE)]
story += [PageBreak()]

story += [P("Bütün fen bilimleri oyunlarında ortak uygulama standardı", h1)]
rows = [
    [P("Kazanım-mekanik", box_title), P("Ölçülen kavram mekaniğin içinde bulunmalı: yön oyununda güneş ve yön adları, mesafe oyununda iki figür arası gerçek mesafe, tasarruf oyununda akan su görünmeli.", small)],
    [P("Sahne", box_title), P("Başlıktaki okul bahçesi, pano, atölye, müze, hava istasyonu veya şehir gerçek görsel olarak kullanılmalı; ortak bant/uzay/tren/servis şablonu kaldırılmalı.", small)],
    [P("Cevap sızdırmama", box_title), P("Numara veya miktar başlıkta ve görev metninde yazılı olmamalı; kartlarda kategori etiketi bulunmamalı; parça ile hedefi eşleyen emoji kullanılmamalı.", small)],
    [P("Görsel kanıt", box_title), P("Tanıma gerektiren kazanımlarda (trafik levhası, tarihî mekân, teknoloji ürünü) gerçek görsel kullanılmalı; yazıyla anlatmak tanıma yerine geçmez.", small)],
    [P("Yerleşim", box_title), P("390x844 ekranda hiçbir kart kırpılmamalı, yazı taşmamalı; karar verilecek içerik tam görünmeli ve dokunma alanları en az 44 px olmalı.", small)],
    [P("Yönerge", box_title), P("Her oyunun yönergesi kendi konusunu anlatmalı; “doğru cevabı yakala” gibi ortak metinler oyuna özel yeniden yazılmalı.", small)],
    [P("Tur ve yanlış", box_title), P("Her oyun en az üç kademeli tur içermeli; içerik her açılışta değişmeli. Yanlışta doğru cevap açılmamalı; motor/refleks hatası can kaybettirmemeli.", small)],
    [P("Üretim", box_title), P("Hayat bilgisi kazanımları davranışa dönüşmeli: son turda öğrenci kendi örneğini söylemeli, uygulamalı veya yazmalı.", small)],
]
standards = Table(rows, colWidths=[28 * mm, 148 * mm])
standards.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8D4E2")), ("BACKGROUND", (0, 0), (0, -1), PALE_PURPLE),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
story += [standards, Spacer(1, 4 * mm)]
story += bullets([
    "Kartlar ve metinler ilk iki turda hareket etmeyecek; hız ancak doğruluk eşiğinden sonra isteğe bağlı ölçüt olacak.",
    "Ses, yazı, görsel, doğru cevap ve geri bildirim Türkçe karakterler dâhil birebir tutarlı olacak; web ile APK aynı davranacak.",
    "Bir oyun yalnız tek sabit kart havuzunu bitirdi diye tamamlanmış sayılmayacak.",
])
story += [PageBreak()]

last_group = None
group_index = -1
accent_cycle = [CORAL, TEAL, GOLD, PURPLE, BLUE, GREEN]
for number, game in enumerate(games, start=1):
    if game["group"] != last_group:
        last_group = game["group"]
        group_index += 1
        accent = GROUP_COLORS[group_index]
        count = sum(1 for g in games if g["group"] == last_group)
        theme_table = Table([[P(f"Tema {group_index + 1}", badge), P(clean(last_group), theme_title)]], colWidths=[30 * mm, 146 * mm], rowHeights=[47 * mm])
        theme_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), accent), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                         ("ALIGN", (0, 0), (0, 0), "CENTER"), ("LEFTPADDING", (1, 0), (1, 0), 12),
                                         ("RIGHTPADDING", (1, 0), (1, 0), 12), ("ROUNDEDCORNERS", [10])]))
        story += [Spacer(1, 20 * mm), theme_table, Spacer(1, 8 * mm), P(f"Bu temada {count} oyun var. Ana düzeltme odağı", h2)]
        story += bullets(GROUP_FOCUS[last_group])
        story += [Spacer(1, 5 * mm), box("Tema kabul eşiği", ["Bu temadaki her oyun üç kademeli tur ve en az bir öğrenci üretimi/uygulaması olmadan tamamlanmış sayılmayacak.", "Başlık, görünen sahne, seslendirme, kontrol ve ölçülen hayat bilgisi kazanımı aynı hedefi gösterecek."], PALE_TEAL, TEAL), PageBreak()]

    scene, level2, level3 = DESIGNS[game["id"]]
    engine_name, engine_obs = ENGINE[game["type"]]
    instruction = clean(game["instruction"])
    observed = [
        f"Kaynak yönerge: “{instruction}” Gerçek ekranda görev <b>{engine_name}</b> içinde açılıyor. {engine_obs}",
        config_summary(game),
    ]
    risk = [TYPE_RISK[game["type"]],
            "Hayat bilgisi kazanımları davranışa dönüşmeyi gerektirir; oyun yalnız kart seçmeyle bitiyorsa öğrencinin günlük yaşamında bu davranışı uyguladığına dair hiçbir kanıt üretilmez.",
            "Mevcut içerik aynı sabit örneklerle tekrarlandığı için çocuk cevabı/konumu ezberleyebilir; kavramı yeni bir duruma aktardığı gösterilemez."]
    new_play = [scene, level2, level3,
                "Yönerge oyunun kendi konusunu anlatsın ve tekrar dinletilebilsin; ortak şablon metinler kullanılmasın.",
                "Başarı kaydına yalnız doğru kart değil; öğrencinin gerekçesi, verdiği örnek ve uyguladığı davranış eklensin."]
    rounds = [
        "Destekli: kavram tek açık örnekle çalışılır; görsel kanıt görünür, kartlar sabit, süre ve can cezası kapalıdır.",
        level2,
        level3,
    ]
    feedback = [TYPE_FEEDBACK[game["type"]],
                "Doğru yanıtta yalnız puan/konfeti değil; kararın dayandığı görsel veya bilgi kısa biçimde görünür olmalı.",
                "Bitiş ekranı üç turdaki doğruluk, ipucu kullanımı ve öğrencinin ürettiği gerekçe/örnek/uygulama kanıtını ayrı göstermeli."]
    acceptance = [TYPE_ACCEPT[game["type"]],
                  f"Başlıktaki sahne ve eylem gerçekten uygulanacak: {scene}",
                  "En az üç farklı içerik turu ve her turda yeni örnek bulunacak; seçenek konumu ve doğru yanıt sırası değişecek.",
                  "Başarı kaydına öğrencinin gerekçesi ve verdiği kendi örneği eklenecek; yalnız seçilen kart kimliği yeterli olmayacak."]

    accent = accent_cycle[(number - 1) % len(accent_cycle)]
    story += [header(number, game["title"], f"{game['id']} · {game['sub']} · {clean(game['kaz'])}", accent), Spacer(1, 1.8 * mm)]
    story += [box("Denemede görülen mevcut durum", observed, PALE_CORAL, CORAL), Spacer(1, 0.8 * mm)]
    story += [box("Eğitimsel risk", risk, PALE_GOLD, GOLD), Spacer(1, 0.7 * mm)]
    story += [P("Yeni sahne ve oynanış", h2)] + bullets(new_play, bullet_small)
    story += [P("Üç kademeli tur", h2), rounds_table(rounds), Spacer(1, 0.7 * mm)]
    story += [box("Geri bildirim ve bitiş", feedback, PALE_TEAL, TEAL), Spacer(1, 0.7 * mm)]
    story += [box("Kabul ölçütü", acceptance, PALE_BLUE, BLUE), PageBreak()]

story += [P("Son kabul kontrolü", h1), P("4. sınıf fen bilimleri bölümü tamamlanmadan önce", h2)]
story += bullets([
    "f01-f48 arasındaki 48 oyun üç kademeli turla baştan sona test edilir; görünen başlık, sahne, kontrol, ses ve ölçülen kazanım kayıt altına alınır.",
    f"Sekiz bant oyunundaki {wrong_hint_total} wrongHint metni yeniden yazılır; hiçbiri doğru kutunun adını içermez.",
    "Isıtma Deneyi'nde hedef sıcaklık söylenmez, kronometre yerine gerçek ocak ve madde bulunur ve hâl değişimi sırasında sıcaklığın sabit kaldığı doğru gösterilir.",
    "Enerji Grafiği ile Şehir Verisi Grafiği'nde kategori hedefleri ekranda okunur; iki oyun da şu an veri eksikliğinden deneme-yanılmaya bağlı.",
    "Çözüm Köprüsü'nde parça yazıları çipe tam sığar; Hâl Değişimi Bandı'nda kart hiçbir kenarda kırpılmaz ve kart metinleri cevabı çağrıştıran sözcük içermez.",
    "Altı radar oyununun ortak yönergesi her oyunun kendi konusuna göre yeniden yazılır.",
    "Roket-YAKIT sahnesi sekiz sıralama oyununun tamamından kaldırılır; adımlar kendi konusuna ait sahnede sıralanır.",
    "Ürün ve model kazanımlarında (deney masası, pusula, devre, şehir maketi) seçilen öge ekranda gerçekten bir şey inşa eder.",
    "Her oyunda en az üç farklı içerik turu, açıklayıcı yanlış geri bildirimi ve öğrencinin kendi gözlemini/gerekçesini içeren bir kapanış bulunur.",
])
story += [Spacer(1, 4 * mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 2. sınıf hayat bilgisi listesindeki h01-h36 oyunlarını kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, görsel kanıt, mekanik, üç tur, geri bildirim, öğrenci kanıtı ve test gereksinimlerini ayrıntılı biçimde tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)

reader = PdfReader(str(OUT))
print({"pages": len(reader.pages), "games": len(games), "genericPrompt": len(generic_prompt),
       "beltGames": belt_n, "bytes": OUT.stat().st_size, "output": str(OUT)})
