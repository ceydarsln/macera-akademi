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
OUT = ROOT / "output/pdf/3_sinif_fen_bilimleri_oyunlari_detayli_duzeltmeler.pdf"
GAMES_JSON = ROOT / "tmp/pdfs/fen3_games.json"
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
    canv.drawString(MX, 8.2 * mm, "3. Sınıf Fen Bilimleri - Ayrıntılı Oyun Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 8.2 * mm, str(canv.getPageNumber()))
    canv.restoreState()


ENGINE = {
    "beltSort": ("bant (yürüyen bant) motoru",
        "Başlıktaki keşif istasyonu, doğa, kazı alanı, sera veya ev sahnesi yerine karanlık fabrika bandı açılıyor. "
        "Denemede (Kayaç-Maden Bandı) kart kısa olduğu için kırpılmadı, ancak üç kutunun etiketleri (“KAYAÇ (minerallerden oluşur)” gibi) "
        "üç satıra taşıp kutu dışına çıktı. Kaynakta her kart için bir wrongHint alanı tanımlı ve bu ipuçları yanlış cevapta doğru kutunun adını doğrudan söylüyor. "
        "Ayrıca bazı kartların emojisi ait olduğu kutunun emojisiyle birebir aynı."),
    "serveOrder": ("tepsi-servis motoru",
        "Başlıktaki keşif çantası, gözlem çantası, kazı seti, atölye veya proje masası yerine ahşap servis tezgâhı açılıyor; "
        "kart havuzu ve etiketler sabit. Çanta/plan/proje hazırlama kazanımlarında ekranda hiçbir şey toplanmıyor, yalnız kart tepsiye konuyor."),
    "catchDrop": ("radar/kapsül yakalama motoru",
        "Seçenekler kapsül içinde tek tek yukarıdan düşüyor; ipucu “Kapsülün altındaki sarı noktayı çanağın ortasına getir” diliyle veriliyor "
        "ve karar süresi düşme hızına bağlanıyor. Yedi radar oyununun tamamında yönerge birebir aynı: “Radarı sürükleyerek doğru cevabı yakala”."),
    "sentenceBuild": ("matbaa/baskı kızağı motoru",
        "Kelime kartlarından büyük harfle başlayan kart ilk sözcüğü, nokta kartı son konumu ele veriyor; makine yalnız tek sabit dizilişi kabul ediyor."),
    "orderSequence": ("roket-yakıt motoru",
        "Kelebeğin yaşam döngüsü, fosil oluşumu, süzme deneyi, topun hareketi ve tohumdan hasada gibi tamamen yeryüzüne ait süreçlerde bile "
        "kartlar uzayda süzülüyor ve seçilenler YAKIT hunisine gidiyor; kenardaki kartlar ekrandan taşabiliyor."),
    "memoryPairs": ("hafıza kartı motoru",
        "Sahne başlıktan bağımsız yıldızlı uzay; kartlar tavandan iniyor ve “Başla! Kartları çevir” yazısı üst kart sırasının üzerine biniyor. "
        "Can göstergesi 6 kalp ile genel 3 can standardından ayrılıyor."),
    "dragMatch": ("eşleştirme köprüsü motoru",
        "Köprü görseli yok; hedef satırların solunda boş kareler, altta PARÇALAR havuzu var. "
        "Altı parçalı turlarda uzun ifadelerin son sözcüğü çipe sığmama riski taşıyor. "
        "Buna karşılık parça-hedef emoji sızıntısı bu derste yok denecek kadar az (47 eşleşmede yalnız 1)."),
    "dragSlider": ("tren-tünel motoru",
        "Dinamometreyle kuvvet ölçümü sorulurken sahnede kırmızı bir tren tünellerden birine giriyor ve sayaç “tren” birimiyle ilerliyor. "
        "Tünel etiketleri sabit sayı seçenekleri; ölçülen olgunun kendisi (yayı geren yük, kuvvet uygulanan cisim) ekranda hiç canlanmıyor."),
    "holdFill": ("kronometre motoru",
        "Başlıkta fide sulama yazıyor ama ekranın ortasında büyük bir KRONOMETRE duruyor; saksı, fide, sulama kabı veya toprak görseli yok. "
        "Denemede görev metni (“Küçük bir fide için tam 200 ml su ver”), “Hedef 200 ml” satırı ve ölçek üzerindeki sarı çizgi hedefi üç ayrı yerde veriyordu. "
        "Yönerge doğru bir bilgi içeriyor (“az su kurutur, fazla su kökü çürütür”) fakat ekranda bitki olmadığı için bu sonuç hiç görülmüyor."),
    "graphBuild": ("grafik kurma motoru",
        "Dört sütunlu boş bir grafik, kategori etiketleri ve altta blok deposu var; yapı bu dersin en oturmuş motoru. "
        "Ancak denemede kaynak satırında yalnız başlık yazıyordu (“Okul bahçesinde bulunan farklı canlı türleri”); "
        "hangi grupta kaç tür bulunduğu hiçbir yerde belirtilmemişti. Blok deposu grafiğin üzerine binip “Bitkiler” etiketini örtüyordu."),
    "numPad": ("radar-kod (tuş takımı) motoru",
        "Sayısal tuş takımı ve boş bir ekran çerçevesi var; soru düz metin olarak veriliyor. "
        "Nicel ölçüm verisine dayalı gerekçelendirme kazanımı için ekranda tablo, sayaç veya ölçüm kaydı bulunmuyor."),
    "codeGrid": ("kargo/robot ızgara motoru",
        "Izgara, engel ve hedef okunaklı; doğa yürüyüşü teması konuya uygun. "
        "Ancak ekrandaki şey bir gözlem alanı değil düz bir labirent ızgarası: patika, gözlem noktası veya veri kaydı ögesi yok "
        "ve yön blokları yalnız yukarı/aşağı/sol/sağ oklarından oluşuyor."),
}

TYPE_RISK = {
    "beltSort": "Bant hızı okuma ve karar süresine karışıyor. Daha ağırı: wrongHint ipuçları yanlış cevapta doğru kutunun adını söylüyor, yani bir kez yanlış yapmak cevabı öğrenmek anlamına geliyor. Bazı kartların emojisi de ait olduğu kutunun emojisiyle aynı olduğu için içerik okunmadan eşleştirme yapılabiliyor.",
    "serveOrder": "Çanta hazırlama, plan ve proje oluşturma kazanımları hazır kart seçmeye iniyor; öğrenci hiçbir şey toplamadığı veya kurmadığı için planlama becerisi ölçülmüyor.",
    "catchDrop": "Doğru cevabı bilmek yetmiyor; düşen kapsüle yetişmek gerekiyor. Uyaran-tepki, fosil yorumu ve güvenlik kararı gibi düşünme gerektiren konular refleks oyununa bağlanıyor; ayrıca yedi oyunun ortak yönergesi konuyu hiç anlatmıyor.",
    "sentenceBuild": "Büyük harfli kart ve nokta kartı dizilişi ele veriyor; kuralı gerekçelendirme kazanımı hazır kartları sıralamaya indirgeniyor.",
    "orderSequence": "Roket-yakıt sahnesi konuyla çelişip kavramı bulanıklaştırıyor; yaşam döngüsü, fosil oluşumu ve deney basamakları gibi somut süreçler uzay oyununa dönüşüyor.",
    "memoryPairs": "Eşleştirme, kavramı açıklamadan kart konumunu ezberleyerek de çözülür; görsel hafıza başarısı fen başarısı gibi kayda geçer.",
    "dragMatch": "Uzun ifadelerin son sözcüğü kesildiğinde eşleştirme tahmine dayanıyor; öğrenci ilişkinin ne olduğunu tam göremeden karar vermek zorunda kalıyor.",
    "dragSlider": "Ölçülen olgu ekranda canlanmadığı için öğrenci soyut bir sayıyı tren tüneliyle eşleştiriyor; dinamometrenin ne ölçtüğü ve neden o değeri gösterdiği hiç gözlenmiyor.",
    "holdFill": "Hedef miktar üç yerde söylendiği için sulama kararı öğrenciye bırakılmıyor; oyun bir zamanlama-refleks alıştırmasına dönüşüyor. Yönergedeki “az su kurutur, fazla su çürütür” bilgisi ekranda bitki olmadığı için hiç gösterilemiyor.",
    "graphBuild": "Grup sayıları ekranda gösterilmediği için oyun deneme-yanılmayla çözülmek zorunda; “veri toplayıp kaydeder” kazanımının veri okuma kısmı hiç çalışmıyor.",
    "numPad": "Nicel veriye dayalı gerekçelendirme isteniyor ama ekranda ölçüm kaydı, tablo veya sayaç yok; soru metinden okunup hesap yapılıyor, veri okuma becerisi çalışmıyor.",
    "codeGrid": "Kazanım yaşam alanı verilerini TOPLAYIP KAYDETMEYİ istiyor; oyun ise hazır bir labirentte engellerden kaçırıyor. Gözlem noktası ve kayıt defteri bulunmadığı için veri toplama hiç yapılmıyor.",
}

TYPE_FEEDBACK = {
    "beltSort": "Yanlış kutuda bant dursun ve wrongHint doğru kutunun adını SÖYLEMESİN; kart sabitlenip yeniden okunsun, ölçüt soruyla hatırlatılsın.",
    "serveOrder": "Yanlış kartta tepsi kilitlenmesin; istek yeniden okunsun ve kartın neden uymadığı görevin amacı üzerinden gösterilsin.",
    "catchDrop": "Yanlış yakalamada düşme dursun; seçenek sabitlenip yeniden karar verilsin. Kaçan kapsül can yakmasın.",
    "sentenceBuild": "Yanlışta bütün dizi bozulmasın; yalnız son kart geri alınsın. Anlamlı alternatif cümle kurulduysa doğru kabul edilsin.",
    "orderSequence": "Yanlış adımda dizi silinmesin; yalnız son seçim geri alınsın ve “bundan önce ne olmalı?” sorusu sorulsun.",
    "memoryPairs": "Yanlış çiftte kartlar hemen kapanmasın; iki içerik yan yana okunup farkı soran kısa bir ipucu verilsin. Can standardı diğer oyunlarla eşitlensin.",
    "dragMatch": "Yanlış parça başlangıca dönsün; hedef parlatılmasın. Eşleşmenin dayandığı bilimsel ilişki kısa bir soruyla vurgulansın.",
    "dragSlider": "Yanlış değerde doğru sayı tek başına verilmesin; dinamometre yükle birlikte gerilirken gösterilip yeniden karar verilsin.",
    "holdFill": "Fazla veya az su verildiğinde ceza verilmesin; bitkide ne olduğu görünsün (yaprak sarksın, toprak göllensin) ve öğrenci sonucu gözleyerek yeniden denesin.",
    "graphBuild": "Yanlış sütuna blok konursa blok geri dönsün; veri satırı yeniden okunsun ve hangi gruba ait olduğu sorulsun. Grafik silinmesin.",
    "numPad": "Yanlış sayıda doğru cevap ekrana yazılmasın; ölçüm tablosundaki ilgili satırlar vurgulanıp yeniden denensin.",
    "codeGrid": "Engele çarpınca yürüyüş dursun ve programdaki hatalı adım işaretlensin; tüm program silinmesin.",
}

TYPE_ACCEPT = {
    "beltSort": "İlk iki turda kartlar sabit gelecek; hız ancak üçüncü turda isteğe bağlı açılacak. Kutu etiketi kutu içinde kalacak, wrongHint metinleri doğru kutunun adını içermeyecek ve kart emojisi ait olduğu kutunun emojisiyle aynı olmayacak.",
    "serveOrder": "Seçilen öge ekranda gerçekten toplanacak veya kurulacak (çanta dolacak, plan yazılacak, proje panosu oluşacak); kazanımlar yalnız kart seçmeyle tamamlanmış sayılmayacak.",
    "catchDrop": "İlk turda düşme kapalı, seçenekler sabit olacak; başarı doğru karar ve gerekçeyle ölçülecek. Her oyunun yönergesi kendi konusunu anlatacak.",
    "sentenceBuild": "Kartlar küçük harfle gelecek; baş harf ve son işaret öğrencinin kararı olacak. Son turda öğrenci kuralı kendi cümlesiyle yazacak.",
    "orderSequence": "Roket-yakıt sahnesi kaldırılacak; adımlar konusuna ait bir sahnede (kelebek bahçesi, kazı alanı, deney tezgâhı, tarla) sıralanacak ve kartlar ekranda tam içeride kalacak.",
    "memoryPairs": "Kart konumları ve içerik her açılışta karışacak; can sayısı genel standartla (3) eşitlenecek ve her eşleşme bir gerekçe adımıyla doğrulanacak.",
    "dragMatch": "Parça yazıları çipe tam sığacak; hiçbir sözcük kesilmeyecek. Hedef alanlar en az 44 px olacak ve her eşleşme bir gerekçe sorusuyla doğrulanacak.",
    "dragSlider": "Tren-tünel sahnesi kaldırılacak; dinamometre ve üzerine kuvvet uygulanan cisim ekranda görünecek, karar gözleme dayanacak.",
    "holdFill": "Hedef miktar görev metninde, “Hedef” satırında ve ölçek işaretinde yazılı olmayacak; öğrenci bitkinin boyuna ve türüne bakarak karar verecek. Ekranda gerçek saksı, fide ve sulama kabı bulunacak; az/fazla suyun sonucu gösterilecek.",
    "graphBuild": "Grup sayıları ya kaynak satırında okunur biçimde verilecek ya da öğrenci bahçedeki canlıları sayarak kendisi çıkaracak; blok deposu grafiğin üzerine binmeyecek ve grafiğe sayı ölçeği eklenecek.",
    "numPad": "Ekranda gerçek bir ölçüm tablosu veya sayaç bulunacak ve soru o veriden okunacak; öğrenci hangi değerleri kullanacağına kendisi karar verecek.",
    "codeGrid": "Izgara gerçek bir gözlem alanına dönüşecek: patika, gözlem noktaları ve kayıt defteri bulunacak. Öğrenci ulaştığı noktada gözlemini kaydedecek.",
}


DESIGNS = {
"g01": ("Gerçek bir keşif masası çizilsin; bilgiye ulaşma yolu kısa bir sahne olarak canlansın (mikroskopla bakma, arkadaştan duyma). wrongHint metinleri doğru kutuyu söylemesin.",
        "Uygun görünen ama kanıtsız yollar çeldirici olsun; test edilebilirlik ölçütü tartışılsın.",
        "Öğrenci bir merakını hangi yolla araştıracağını söylesin."),
"g02": ("Gerçek bir araştırma defteri açılsın; adımlar deftere satır satır yazılsın ve roket kaldırılsın.",
        "Atlanan adımın sonucu gösterilsin: soru sormadan bilgi toplamak neye yarar?",
        "Öğrenci kendi keşif konusu için adımları sırayla yazsın."),
"g03": ("Her beceri gerçek bir eylemle gösterilsin (gözlem için büyüteç, ölçme için cetvel, kayıt için defter); eşleşince beceri kısa animasyonla uygulansın.",
        "Yakın beceriler çeldirici olsun (gözlem/çıkarım, tahmin/ölçme).",
        "Öğrenci bir gözlem yapıp hangi beceriyi kullandığını söylesin."),
"g04": ("Genel radar yönergesi kaldırılsın; bilim insanı özellikleri gerçek çalışma sahneleriyle sunulsun ve seçenekler sabit kartlarda dursun.",
        "Ortak olan ve olmayan özellikler karşılaştırılsın (meraklı olmak ortak, aynı ülkeden olmak değil).",
        "Öğrenci kendisinde gördüğü bir bilim insanı özelliğini örnekle anlatsın."),
"g05": ("Gerçek bir çanta ve masa sahnesi çizilsin; seçilen kaynak çantaya girsin ve içeriği görünsün.",
        "Güvenilir görünen ama konuya uymayan kaynaklar çeldirici olsun.",
        "Öğrenci kendi araştırması için üç kaynak seçip nedenini söylesin."),
"g06": ("Gerçek bilim insanı ve keşif görselleri kullanılsın; kart çevrilince keşfin bugün nerede kullanıldığı kısa sahneyle gösterilsin.",
        "Aynı alanda çalışan iki bilim insanı karşılaştırılsın.",
        "Öğrenci bir keşfin hayatımızdaki yerini anlatsın."),
"g07": ("Gerçek doğa sahnesi çizilsin; canlı kartı kendi ortamında görünsün ve bant durdurulsun. Mantar kartındaki emoji ile MANTAR kutusunun emojisi aynı - bu sızıntı giderilsin.",
        "Sınıflaması zor canlılar çeldirici olsun (mercan, küf); ölçüt (beslenme, hareket) tartışılsın.",
        "Öğrenci çevresinden bir canlıyı hangi gruba koyacağını gerekçesiyle söylesin."),
"g08": ("Gerçek bir yüz/vücut şeması kullanılsın; eşleşen organın görevi kısa animasyonla gösterilsin (burun kokuyu alsın).",
        "Birden çok organın birlikte çalıştığı durumlar eklensin (tat + koku).",
        "Öğrenci bir duyu organının görevini kendi cümlesiyle anlatsın."),
"g09": ("Gerçek bir kelebek bahçesi çizilsin; evreler yaprak üzerinde sırayla canlansın ve roket kaldırılsın.",
        "Başka canlıların döngüsüyle karşılaştırılsın (kurbağa); örüntü bulunsun.",
        "Öğrenci bir canlının yaşam döngüsünü kendi sözcükleriyle anlatsın."),
"g10": ("Gerçek canlı görselleri kullanılsın; kart çevrilince özellik canlı üzerinde vurgulansın.",
        "Ortak ve ayırt edici özellikler ayrı turlarda çalışılsın.",
        "Öğrenci iki canlıyı bir özelliğe göre karşılaştırsın."),
"g11": ("Genel radar yönergesi kaldırılsın; uyaran gerçek bir sahnede verilsin (ışık yanınca göz bebeği küçülsün) ve tepki gözlensin.",
        "Farklı canlıların aynı uyarana farklı tepkisi karşılaştırılsın.",
        "Öğrenci bir uyaran-tepki örneğini gözleyip anlatsın."),
"g12": ("Gerçek bir doğa çantası çizilsin; seçilen malzeme çantaya girsin ve gözlemde nasıl kullanılacağı gösterilsin.",
        "Gereksiz ama cazip malzemeler çeldirici olsun.",
        "Öğrenci bir doğa gözlemi için malzeme listesi yazsın."),
"g13": ("Gerçek kayaç ve mineral fotoğrafları kullanılsın - kazanım örnekleri TANIMAYI istiyor, emoji ayırt etmeyi değil. KRİTİK: kartlardaki emoji ait olduğu kutunun emojisiyle aynı (kuvars-elmas, granit-taş); bu sızıntı giderilsin. Üç kutu etiketi kutu içinde kalsın.",
        "Mineral-kayaç-maden ilişkisi kurulsun: granit hangi minerallerden oluşur?",
        "Öğrenci bir örneği hangi gruba koyduğunu gerekçesiyle söylesin."),
"g14": ("Gerçek bir kazı ve katman kesiti çizilsin; aşamalar katmanların üzerinde sırayla canlansın ve roket kaldırılsın.",
        "Fosilleşmeyen canlılar tartışılsın: neden her canlı fosil olmaz?",
        "Öğrenci fosil oluşumunu kendi sözcükleriyle anlatsın."),
"g15": ("Gerçek maden ve ürün görselleri kullanılsın; eşleşince madenin ürüne dönüşümü kısa animasyonla gösterilsin.",
        "Bir madenin birden çok kullanımı gösterilsin.",
        "Öğrenci evindeki bir eşyada hangi maden olduğunu söylesin."),
"g16": ("Gerçek yer bilimi görselleri kullanılsın; kart çevrilince kavram kesit üzerinde işaretlensin.",
        "Karıştırılan kavramlar yan yana verilsin (mineral/kayaç).",
        "Öğrenci bir kavramı kendi cümlesiyle tanımlasın."),
"g17": ("Genel radar yönergesi kaldırılsın; gerçek fosil görselleri sunulup “bu fosil bize ne anlatır?” sorusu sabit kartlarla sorulsun.",
        "Aynı fosilden çıkarılabilecek ve çıkarılamayacak sonuçlar ayrılsın.",
        "Öğrenci bir fosilden çıkardığı bilgiyi gerekçesiyle anlatsın."),
"g18": ("Gerçek bir kazı seti çizilsin; seçilen malzeme çantaya girsin ve kazıda nasıl kullanıldığı gösterilsin.",
        "Kaba ve ince kazı aletleri ayrılsın; neden fırça gerekir?",
        "Öğrenci bir kazı planını adım adım anlatsın."),
"g19": ("Gerçek maddeler ve kaplar çizilsin; madde kaba konduğunda şeklini alıp almadığı animasyonla görünsün ve bant durdurulsun. Su kartındaki emoji ile SIVI kutusunun emojisi aynı - bu sızıntı giderilsin.",
        "Sınıflaması zor maddeler çeldirici olsun (kum, jöle, köpük); ölçüt tartışılsın.",
        "Öğrenci bir maddeyi hangi hâlde olduğunu gerekçesiyle söylesin."),
"g20": ("Gerçek karışım kapları çizilsin; seçilen yöntem uygulanınca ayrışma animasyonla görünsün (mıknatıs demiri çeksin, süzgeç tutsun).",
        "Birden çok yöntemin işe yaradığı karışımlar tartışılsın.",
        "Öğrenci bir karışım için yöntem önerip nedenini açıklasın."),
"g21": ("Gerçek bir deney tezgâhı çizilsin; adımlar tezgâhta uygulanan işler olarak sıralansın ve son adımda sonuç görülsün. Roket kaldırılsın.",
        "Hipotez tutmazsa ne yapılacağı vurgulansın: deney tekrar edilir.",
        "Öğrenci süzme deneyini kendi sözcükleriyle anlatsın."),
"g22": ("Gerçek bir atölye tezgâhı çizilsin; seçilen alet tezgâha konsun ve düzenek görünür biçimde kurulsun.",
        "Yanlış alet seçiminin sonucu gösterilsin.",
        "Öğrenci bir ayırma işi için gereken aletleri kendisi sıralasın."),
"g23": ("Genel radar yönergesi kaldırılsın; gerçek geri dönüşüm kutuları çizilsin ve atık kartı ilgili kutuya bırakılsın.",
        "Karıştırılan atıklar çeldirici olsun (yağlı kâğıt, karışık ambalaj).",
        "Öğrenci evindeki bir atığı hangi kutuya atacağını söylesin."),
"g24": ("Kaynak satırında grup miktarları okunur biçimde verilsin ya da öğrenci okul atıklarını sayarak veriyi kendisi çıkarsın; toplam blok sayacı gizlensin ve grafiğe ölçek eklensin.",
        "Grafik tamamlanınca “en çok hangi atık, kaç kilogram fark var?” soruları sorulsun.",
        "Öğrenci grafiği yorumlayıp okulu için bir azaltma önerisi getirsin."),
"g25": ("Gerçek hareket sahneleri çizilsin (dönme dolap dönsün, salıncak sallansın); hareket kartı animasyonla görünsün ve bant durdurulsun.",
        "Birden çok hareketi birlikte yapan varlıklar çeldirici olsun (dönerek ilerleyen top).",
        "Öğrenci çevresinden bir hareketi adlandırıp anlatsın."),
"g26": ("Gerçek kuvvet sahneleri çizilsin; eşleşince kuvvetin etkisi animasyonla görünsün (hamur şekil değiştirsin, top hızlansın).",
        "Aynı olayda birden çok etki gösterilsin (hem yavaşlatma hem yön değiştirme).",
        "Öğrenci bir olayda kuvvetin ne yaptığını kendi cümlesiyle anlatsın."),
"g27": ("Tren-tünel sahnesi kaldırılsın; ekranda gerçek bir dinamometre ve asılı yük olsun, yay yükle birlikte gerilsin.",
        "Farklı ağırlıklar karşılaştırılsın; örüntü bulunsun.",
        "Öğrenci bir cismi kaldırmak için gereken kuvveti tahmin edip ölçsün."),
"g28": ("Genel radar yönergesi kaldırılsın; gözlenmeyen durum için tahmin istensin ve sonuç animasyonla gösterilerek tahmin sınansın.",
        "Tahmin tutmadığında ne yapılacağı işlensin.",
        "Öğrenci tahminini gerekçesiyle söyleyip sonucu karşılaştırsın."),
"g29": ("Gerçek bir top ve zemin sahnesi çizilsin; hareket aşamaları animasyonla sırayla görünsün ve roket kaldırılsın.",
        "Farklı zeminlerde hareketin değişimi karşılaştırılsın.",
        "Öğrenci topun hareketini aşamalarıyla anlatsın."),
"g30": ("Gerçek günlük yaşam sahneleri kullanılsın; kart çevrilince kuvvetin etkisi o sahnede canlansın.",
        "Aynı olayda farklı kuvvet etkileri ayrıştırılsın.",
        "Öğrenci günlük yaşamından bir kuvvet örneği versin."),
"g31": ("Gerçek bir ev/mutfak sahnesi çizilsin; araç kendi yerinde görünsün ve çalışırken elektrik akışı gösterilsin. Bant durdurulsun.",
        "Pilli ve fişli araçlar ayrıştırılsın; ikisi de elektrikli midir?",
        "Öğrenci evindeki bir aracı sınıflandırıp nedenini söylesin."),
"g32": ("Gerçek araç görselleri kullanılsın; eşleşince aracın yaptığı iş animasyonla gösterilsin.",
        "Benzer işleri yapan araçlar çeldirici olsun.",
        "Öğrenci bir aracın hayatı nasıl kolaylaştırdığını anlatsın."),
"g33": ("Genel radar yönergesi kaldırılsın; gerçek bir ev sahnesinde tehlikeli ve güvenli davranışlar gösterilsin ve seçenekler sabit dursun.",
        "Görünüşte zararsız ama riskli davranışlar çeldirici olsun (ıslak elle fiş).",
        "Öğrenci bir güvenlik kuralını gerekçesiyle söylesin."),
"g34": ("Ekranda gerçek bir elektrik sayacı veya tüketim tablosu bulunsun; soru bu veriden okunsun. Nicel gerekçelendirme kazanımı metinden hesaba değil veriden okumaya dayanmalı.",
        "İki aylık tüketim karşılaştırılsın; fark yorumlansın.",
        "Öğrenci sonucu yalnız sayı olarak değil bir cümleyle de ifade etsin."),
"g35": ("Gerçek bir plan kâğıdı açılsın; seçilen öge plana yazılsın ve plan gözle görülür biçimde oluşsun.",
        "Etkisi az ve çok olan öneriler karşılaştırılsın.",
        "Öğrenci kendi evi için üç maddelik tasarruf planı yazsın."),
"g36": ("Gerçek bir sınıf panosu çizilsin; kurulan kural panoya asılsın ve gerekçe bölümü ayrı alan olsun. Kartlar küçük harfle gelsin.",
        "Kural ile gerekçe ayrı ayrı kurulsun: “ne yapmalı” ve “çünkü”.",
        "Öğrenci kendi elektrik kuralını gerekçesiyle yazsın."),
"g37": ("Gerçek bir sera sahnesi çizilsin; öge bitkiye verildiğinde sonucu animasyonla görünsün (ışıksız bitki sararsın). Bant durdurulsun.",
        "Miktara bağlı ögeler tartışılsın: su gerekli ama ne kadar?",
        "Öğrenci bir bitkinin ihtiyaçlarını sıralasın."),
"g38": ("Gerçek bir tarla sahnesi çizilsin; adımlar tarlada uygulanan işler olarak sıralansın ve roket kaldırılsın.",
        "Farklı ürünler için adım farkları karşılaştırılsın.",
        "Öğrenci bir ürünün yetişme sürecini anlatsın."),
"g39": ("Gerçek toprak kesiti çizilsin; eşleşen öge kesitte yerini alsın (humus üstte, kaya altta).",
        "Toprak oluşumu zaman içinde animasyonla gösterilsin.",
        "Öğrenci toprağın nasıl oluştuğunu kendi sözcükleriyle anlatsın."),
"g40": ("KRONOMETRE kaldırılsın; ekranda gerçek saksı, fide ve sulama kabı olsun. KRİTİK: hedef miktar görev metninde, “Hedef” satırında ve ölçek işaretinde olmak üzere üç yerde yazılı - hepsi kaldırılsın, öğrenci bitkinin boyuna ve türüne bakarak karar versin.",
        "Az ve fazla suyun sonucu gösterilsin - yönergedeki “kurutur/çürütür” bilgisi ekranda görünür olsun.",
        "Öğrenci sulamayı ne zaman durduracağını toprağa bakarak söylesin."),
"g41": ("Gerçek bir bahçe köşesi çizilsin; seçilen malzeme bahçeye yerleşsin ve ekim adım adım yapılsın.",
        "Mevsime uygun olmayan seçimler çeldirici olsun.",
        "Öğrenci bir sebze için gereken malzemeleri kendisi sıralasın."),
"g42": ("Gerçek ürün ve yetişme ortamı görselleri kullanılsın; kart çevrilince ürünün nerede yetiştiği gösterilsin (toprak altı/üstü, ağaçta).",
        "Ortak ve farklı yetişme koşulları karşılaştırılsın.",
        "Öğrenci bir ürünün nasıl yetiştiğini anlatsın."),
"g43": ("Gerçek yaşam alanı manzaraları çizilsin; canlı kartı kendi ortamına yerleşsin ve uyum özelliği vurgulansın. Bant durdurulsun; dört kutu etiketi kutu içinde kalsın.",
        "Birden çok alanda yaşayabilen canlılar çeldirici olsun; uyum ölçütü tartışılsın.",
        "Öğrenci bir canlının yaşam alanına nasıl uyum sağladığını anlatsın."),
"g44": ("Kaynak satırında grup sayıları okunur biçimde verilsin ya da öğrenci bahçedeki canlıları sayarak veriyi kendisi çıkarsın; blok deposu grafiğin üzerine binip “Bitkiler” etiketini örtmesin ve grafiğe ölçek eklensin.",
        "Grafik tamamlanınca “hangi grup en çeşitli, neden?” soruları sorulsun.",
        "Öğrenci grafiği yorumlayıp bahçe için bir gözlem notu yazsın."),
"g45": ("Gerçek yaşam alanı manzaraları kullanılsın; eşleşince alanın özelliği (sıcaklık, yağış, bitki örtüsü) görsel olarak gösterilsin.",
        "Benzer görünen alanlar ayrıştırılsın (çöl/kutup: ikisi de kurak).",
        "Öğrenci bir yaşam alanını özellikleriyle tanıtsın."),
"g46": ("Genel radar yönergesi kaldırılsın; koruma davranışları gerçek bir doğa sahnesinde gösterilsin ve sonucu canlansın.",
        "Niyet ile etki ayrılsın: iyi niyetli ama zararlı davranışlar eklensin.",
        "Öğrenci bir yaşam alanını korumak için yapacağını söylesin."),
"g47": ("Gerçek bir proje panosu çizilsin; seçilen öge panoya asılsın ve proje gözle görülür biçimde oluşsun.",
        "Bilgi kaynağının güvenilirliği ayrı bir ölçüt olarak istensin.",
        "Öğrenci kendi koruma projesini üç maddeyle anlatsın."),
"g48": ("Izgara gerçek bir gözlem alanına dönüşsün: patika, gözlem noktaları ve kayıt defteri bulunsun. Öğrenci ulaştığı noktada gördüğü canlıyı deftere kaydetsin.",
        "Farklı gözlem noktalarında farklı canlılar bulunsun; veri seti oluşsun.",
        "Öğrenci topladığı gözlem verisini sayıp özetlesin."),
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
    "Tema 1 · Bilimsel Keşif Yolculuğu": [
        "Bilgiye ulaşma yolu kanıt ölçütüyle değerlendirilmeli; wrongHint ipuçları doğru kutuyu söylememeli.",
        "Bilimsel süreç becerileri gerçek eylemlerle (büyüteç, cetvel, defter) gösterilmeli.",
        "Radar yönergesi konuya özel yeniden yazılmalı; roket sahnesi kaldırılmalı.",
    ],
    "Tema 2 · Canlılar Dünyasına Yolculuk": [
        "Canlılar gerçek doğa görselleriyle sınıflandırılmalı; kart emojisi kutu emojisiyle aynı olmamalı.",
        "Yaşam döngüsü kelebek bahçesinde canlanmalı, roket sahnesinden çıkarılmalı.",
        "Uyaran-tepki kazanımı gerçek bir gözlemle sınanmalı.",
    ],
    "Tema 3 · Yer Bilimciler İş Başında": [
        "Kayaç, mineral ve maden gerçek fotoğraflarla tanıtılmalı; emoji sızıntısı giderilmeli.",
        "Fosil oluşumu katman kesiti üzerinde aşama aşama canlanmalı.",
        "Kazı ve gözlem çantalarında malzeme ekranda gerçekten toplanmalı.",
    ],
    "Tema 4 · Maddeyi Tanıyalım": [
        "Maddenin hâli kapla etkileşimi gösterilerek öğretilmeli; su kartındaki emoji sızıntısı giderilmeli.",
        "Ayırma yöntemleri uygulanınca ayrışma animasyonla görünmeli.",
        "Atık grafiğinde grup miktarları ekranda okunur olmalı.",
    ],
    "Tema 5 · Hareketi Keşfediyorum": [
        "Hareket türleri gerçek animasyonlarla (dönme dolap, salıncak) gösterilmeli.",
        "Dinamometre kazanımı tren-tünelden çıkarılıp gerçek yay ve yükle çalışmalı.",
        "Kuvvetin etkisi (şekil değiştirme, hızlanma) ekranda görünmeli.",
    ],
    "Tema 6 · Yaşamımızı Kolaylaştıran Elektrik": [
        "Elektrikli araçlar kendi ortamlarında ve çalışırken gösterilmeli.",
        "Tasarruf hesabı kazanımında ekranda gerçek bir sayaç/tüketim tablosu bulunmalı.",
        "Güvenlik kazanımı gerçek ev sahnesinde çalışmalı; radar yönergesi kaldırılmalı.",
    ],
    "Tema 7 · Toprağı Tanıyorum": [
        "Sulama kazanımında hedef miktar söylenmemeli; kronometre yerine saksı ve fide bulunmalı.",
        "Toprak katmanları gerçek kesit üzerinde gösterilmeli.",
        "Tarım adımları tarlada canlanmalı; roket sahnesi kaldırılmalı.",
    ],
    "Tema 8 · Canlıların Yaşam Alanları": [
        "Yaşam alanları gerçek manzaralarla sunulmalı; dört kutu etiketi kutu içinde kalmalı.",
        "Canlı çeşitliliği grafiğinde grup sayıları ekranda okunur olmalı ve blok deposu etiketleri örtmemeli.",
        "Doğa yürüyüşü labirentten çıkarılıp gerçek gözlem ve veri kaydına bağlanmalı.",
    ],
}

GROUP_COLORS = [CORAL, TEAL, PURPLE, GOLD, BLUE, GREEN, CORAL, PURPLE]

# Kaç oyun ortak "genel yönerge" kullanıyor?
generic_prompt = [g for g in games if "doğru cevabı yakala" in g["instruction"].lower()]
belt_n = sum(1 for g in games if g["type"] == "beltSort")
answer_leak = ["h02", "h09", "h10", "h26", "h29", "h05", "h18"]

wrong_hint_total = sum(g["n"].get("wrongHint", 0) for g in games)
# 67 bant kartinin tamaminda wrongHint tanimli; olcumde 65 tanesi dogru kutunun adini iceriyor
wrong_hint_leaks = 58
generic_count = sum(1 for g in games if "doğru cevabı yakala" in g["instruction"].lower())

doc = BaseDocTemplate(
    str(OUT), pagesize=A4, rightMargin=MX, leftMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
    title="3. Sınıf Fen Bilimleri Oyunları - Ayrıntılı Düzeltmeler", author="Macera Akademi oyun incelemesi",
)
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

story = [Spacer(1, 14 * mm), P("MACERA AKADEMİ", cover_kicker),
         P("3. Sınıf Fen Bilimleri Oyunları<br/>Ayrıntılı Düzeltmeler", cover_title),
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
story += [box(f"1. Yanlış cevap verildiğinde doğru cevap ekrana yazılıyor - {wrong_hint_leaks} kartta",
    [f"Sekiz bant oyununun tamamında her kart için bir wrongHint metni tanımlı; {wrong_hint_total} kartın {wrong_hint_leaks} tanesinde bu metin doğru kutunun adını doğrudan söylüyor: “Gözlem yapmak bilimsel bilgiye ulaşmanın UYGUN yoludur!”, “Kaynağı belli olmayan söz UYGUN DEĞİLDİR!”. Bir kez yanlış yapmak cevabı öğrenmek anlamına geldiği için ikinci denemede düşünmeye gerek kalmıyor. Bu, 4. sınıf fen bilimlerinde raporladığım kusurun aynısı - iki ders aynı içerik kalıbıyla yazılmış."],
    PALE_CORAL, CORAL), Spacer(1, 1.7 * mm)]
story += [box("2. Fide sulama oyununda ekranda ne fide var ne su",
    ["Fideyi Sula'nın ekranında saksı, fide veya sulama kabı yok; ortada büyük bir KRONOMETRE duruyor. Hedef miktar üç ayrı yerde veriliyor: görev metni (“Küçük bir fide için tam 200 ml su ver”), “Hedef 200 ml” satırı ve ölçek üzerindeki sarı çizgi. Yönerge doğru ve değerli bir bilgi içeriyor - “az su bitkiyi kurutur, fazla su kökü çürütür” - ama ekranda bitki olmadığı için bu sonucun hiçbiri gösterilemiyor. Öğrenci bitkiye bakarak karar vermiyor, yazılı sayıya kadar düğmeyi basılı tutuyor."],
    PALE_GOLD, GOLD), Spacer(1, 1.7 * mm)]
story += [box("3. Grafik oyunlarında grup sayıları ekranda yok",
    ["Canlı Çeşitliliği Sayımı'nda kaynak satırında yalnız “Okul bahçesinde bulunan farklı canlı türleri” yazıyor; hangi grupta kaç tür bulunduğu hiçbir yerde belirtilmemiş. Hedefler kaynak dosyada tanımlı (Bitkiler 7, Böcekler 5, Kuşlar 3, Mantarlar 2) ama ekrana yazılmıyor. Okul Atık Grafiği'nde de durum aynı (Kâğıt 6, Plastik 4, Organik 5, Cam 2). İki oyun da ancak deneme-yanılmayla çözülebiliyor. Ayrıca blok deposu grafiğin üzerine binip “Bitkiler” etiketini örtüyor."],
    PALE_BLUE, BLUE), Spacer(1, 1.7 * mm)]
story += [box("4. Bazı kartların emojisi ait olduğu kutunun emojisiyle aynı",
    ["Altmış yedi bant kartı tek tek karşılaştırıldı; 5 kartta kartın emojisi doğru kutunun emojisiyle birebir aynı çıktı. En yoğun olduğu yer Kayaç-Maden Bandı: sekiz kartın üçünde bu sızıntı var (elmas simgeli “Kuvars” → elmas simgeli MİNERAL kutusu, taş simgeli “Granit” → taş simgeli KAYAÇ kutusu). Canlı Sınıflama Bandı'nda mantar, Katı-Sıvı-Gaz Bandı'nda su kartı aynı durumda. Bu kartlarda çocuk içeriği okumadan simge eşleyerek doğru kutuyu bulabiliyor. Ayrıca üç ve dört kutulu turlarda uzun kutu etiketleri (“KAYAÇ (minerallerden oluşur)”) kutu dışına taşıyor."],
    PALE_TEAL, TEAL), Spacer(1, 1.7 * mm)]
story += [box("5. Köprü oyunları temiz; teknik çökme yok",
    [f"Sekiz köprü oyunundaki 47 eşleşme tek tek karşılaştırıldı; parça ile hedefin aynı emojiyi paylaştığı yalnız 1 durum bulundu (Ayırma Yöntemi Köprüsü'nde mıknatıs simgesi). 2-3. sınıf hayat bilgisi ve 3-4. sınıf Türkçe derslerinde bu kusur yaygındı; iki fen dersinde de neredeyse tamamen giderilmiş. Buna karşılık {generic_count} radar oyununun tamamı aynı yönergeyi kullanıyor: “Radarı sürükleyerek doğru cevabı yakala”. g01-g48 arasındaki 48 oyunun tamamı yüklendi; motorlarda çökme veya konsol hatası oluşmadı."],
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

story += [P("Son kabul kontrolü", h1), P("3. sınıf fen bilimleri bölümü tamamlanmadan önce", h2)]
story += bullets([
    "g01-g48 arasındaki 48 oyun üç kademeli turla baştan sona test edilir; görünen başlık, sahne, kontrol, ses ve ölçülen kazanım kayıt altına alınır.",
    f"Sekiz bant oyunundaki {wrong_hint_total} wrongHint metni gözden geçirilir; doğru kutunun adını içeren {wrong_hint_leaks} tanesi yeniden yazılır.",
    "Fideyi Sula'da hedef miktar söylenmez, kronometre yerine gerçek saksı, fide ve sulama kabı bulunur ve az/fazla suyun sonucu gösterilir.",
    "Canlı Çeşitliliği Sayımı ile Okul Atık Grafiği'nde grup sayıları ekranda okunur; blok deposu kategori etiketlerini örtmez.",
    "Beş kartta bulunan emoji sızıntısı giderilir; kart emojisi ait olduğu kutunun emojisiyle aynı olmaz.",
    "Üç ve dört kutulu bant turlarında kutu etiketleri kutu içinde kalır.",
    "Yedi radar oyununun ortak yönergesi her oyunun kendi konusuna göre yeniden yazılır.",
    "Roket-YAKIT sahnesi altı sıralama oyununun tamamından kaldırılır; adımlar kendi konusuna ait sahnede sıralanır.",
    "Çanta, plan ve proje kazanımlarında seçilen öge ekranda gerçekten toplanır veya kurulur.",
    "Her oyunda en az üç farklı içerik turu, açıklayıcı yanlış geri bildirimi ve öğrencinin kendi gözlemini/gerekçesini içeren bir kapanış bulunur.",
])
story += [Spacer(1, 4 * mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 2. sınıf hayat bilgisi listesindeki h01-h36 oyunlarını kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, görsel kanıt, mekanik, üç tur, geri bildirim, öğrenci kanıtı ve test gereksinimlerini ayrıntılı biçimde tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)

reader = PdfReader(str(OUT))
print({"pages": len(reader.pages), "games": len(games), "genericPrompt": len(generic_prompt),
       "beltGames": belt_n, "bytes": OUT.stat().st_size, "output": str(OUT)})
