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
    "beltSort": "Yanlış kutuda bant dursun; kart sabitlenip yeniden okunsun ve ölçüt doğru söylenmeden hatırlatılsın. Kenarda kırpılan kart hiç puanlanmasın.",
    "serveOrder": "Yanlış seçimde tepsi kilitlenmesin; sepetin toplamı ve kalan bütçe görünür kalsın, öğrenci ürün çıkarıp yeniden denesin.",
    "catchDrop": "Yanlış yakalamada düşme dursun; seçenek sabitlenip yeniden karar verilsin. Kaçan kapsül can yakmasın.",
    "sentenceBuild": "Yanlışta bütün dizi bozulmasın; yalnız son kart geri alınsın. Anlamlı alternatif diziliş kurulduysa doğru kabul edilsin.",
    "orderSequence": "Yanlış adımda dizi silinmesin; yalnız son seçim geri alınsın ve “önce ne olmalı?” sorusunu düşündüren ipucu verilsin.",
    "memoryPairs": "Yanlış çiftte kartlar hemen kapanmasın; iki içerik yan yana okunup farkı soran kısa bir ipucu verilsin. Can standardı diğer oyunlarla eşitlensin.",
    "dragMatch": "Yanlış parça başlangıca dönsün; hedef parlatılmasın. Eşleşmenin dayandığı bilgi kısa bir soruyla vurgulansın.",
    "surveyChart": "Yanlış işaretlemede cevap yeniden dinletilsin; sayım bitince sonuç doğrudan açıklanmasın, öğrenciye “en çok/en az hangisi, kaç fark var?” soruları sorulsun.",
    "codeGrid": "Engele çarpınca robot dursun ve programdaki hatalı adım işaretlensin; tüm program silinmesin. Hatalı adım yön adıyla (“burada batıya gittin”) tarif edilsin.",
    "graphBuild": "Yanlış sütuna blok konursa blok geri dönsün; veri satırı yeniden okunsun ve hangi kategoriye ait olduğu sorulsun. Grafik silinmesin.",
    "numPad": "Yanlış sayıda doğru cevap ekrana yazılmasın; grafikteki ilgili sütunlar vurgulanıp “bu ikisini karşılaştır” denilerek yeniden denensin.",
    "dragSlider": "Yanlış seçimde doğru değer tek başına verilmesin; seçilen sürenin bir günde neye denk geldiği görsel olarak canlandırılıp yeniden karar verilsin.",
}

TYPE_ACCEPT = {
    "beltSort": "İlk iki turda kartlar sabit gelecek; hız ancak üçüncü turda isteğe bağlı açılacak. Kart hiçbir konumda kırpılmayacak, kutu etiketi kutu içinde kalacak ve harita rengi turunda kart rengin kendisini gösterecek.",
    "serveOrder": "Karar için gereken bütün sayısal veri (fiyat, bütçe, kalan tutar) ekranda okunur biçimde bulunacak; sepet toplamı hiçbir ögenin arkasında kalmayacak.",
    "catchDrop": "İlk turda düşme kapalı, seçenekler sabit olacak; başarı doğru karar ve gerekçeyle ölçülecek. Her oyunun yönergesi kendi konusunu anlatacak.",
    "sentenceBuild": "Kartlar küçük harfle gelecek; baş harf ve son işaret öğrencinin kararı olacak. Son turda serbest yazı ya da sözlü ifade alanı bulunacak.",
    "orderSequence": "Roket-yakıt sahnesi kaldırılacak; sırayı ele veren tarih/numara ilk turda gizlenecek ve kartlar 390x844 ekranda tam içeride kalacak.",
    "memoryPairs": "Kart konumları ve içerik her açılışta karışacak; can sayısı genel standartla (3) eşitlenecek ve her eşleşme bir gerekçe adımıyla doğrulanacak.",
    "dragMatch": "Parça yazıları çipe tam sığacak; hiçbir sözcük kesilmeyecek. Emojiler cevabı eşleştirmeyecek, hedef alanlar en az 44 px olacak ve her eşleşme gerekçeyle doğrulanacak.",
    "surveyChart": "Cevap ifadeleri sütun adını birebir tekrar etmeyecek; sayım çetele çizgisiyle görünecek ve oyun ancak sonuç yorumu yapıldıktan sonra tamamlanacak.",
    "codeGrid": "Yön düğmeleri KUZEY/GÜNEY/DOĞU/BATI olarak adlandırılacak; haritada kuzey oku, ölçek ve en az iki işaret noktası bulunacak; görev metni rotayı söylemeyecek ve öğrenci son turda yolu kendisi tarif edecek.",
    "graphBuild": "Kategori hedefleri ya kaynak satırında okunur biçimde verilecek ya da öğrenci nesneleri sayarak kendisi çıkaracak; blok deposu grafiğin üzerine binmeyecek ve grafiğe sayı ölçeği eklenecek.",
    "numPad": "Ekranda gerçek bir grafik bulunacak ve soru o grafikten okunacak; işlem hazır yazılmayacak, öğrenci hangi verileri karşılaştıracağına kendisi karar verecek.",
    "dragSlider": "Tren-tünel sahnesi kaldırılacak; ölçülen kavram (bir günün saat çizelgesi, ekran karşısında geçen süre) ekranda görsel olarak canlandırılacak ve karar gerekçelendirilecek.",
}


DESIGNS = {
"sb01": ("Gerçek bir mahalle/okul sahnesi çizilsin; davranış iki kişi arasında kısa bir sahne olarak canlansın, kart bantta akmasın ve hiçbir kenarda kırpılmasın.",
        "Niyet ile etki ayrılsın: iyi niyetli ama bölücü sonuç doğuran davranışlar eklensin.",
        "Öğrenci toplumsal birliği güçlendirecek kendi fikrini söylesin veya yazsın."),
"sb02": ("Gerçek bir sınıf panosu çizilsin; kartlarda kategori etiketi yazmasın, öğrenci hangi kartın ilgi alanı, hangisinin güçlü yön olduğuna kendisi karar versin.",
        "Aynı özellik hem güçlü yön hem gelişime açık alan olabilecek biçimde sunulsun.",
        "Öğrenci kendi ilgi alanını ve geliştirmek istediği yönü kendi cümlesiyle yazsın."),
"sb03": ("Gerçek okul yaşamı sahneleri kullanılsın (tekerlekli sandalye, farklı dil, farklı inanç); saygı davranışı o sahnede uygulansın ve emoji eşleşmesi kaldırılsın.",
        "Saygı gibi görünüp dışlayan davranışlar çeldirici olsun (acıma, aşırı yardım).",
        "Öğrenci bir farklılığa nasıl saygı göstereceğini kendi cümlesiyle anlatsın."),
"sb04": ("Genel “doğru cevabı yakala” yönergesi kaldırılsın; sorular sosyal bilgiler dersinin somut bir katkısına bağlansın ve seçenekler sabit kartlarda dursun.",
        "Dersin farklı katkıları (harita okuma, tarih bilinci, ekonomi kararı) ayrı örneklerle karşılaştırılsın.",
        "Öğrenci dersten öğrendiği bir şeyi günlük yaşamında nerede kullandığını anlatsın."),
"sb05": ("Gerçek bir sınıf durumu canlansın; kurulan cümle panoya asılsın ve karşıdaki karaktere söylensin. Kartlar küçük harfle gelsin.",
        "Saygılı ve kırıcı iki ifade karşılaştırılsın; fark tartışılsın.",
        "Öğrenci kendi saygı cümlesini hazır kart olmadan kursun."),
"sb06": ("Gerçek bir sınıf anketi sahnesi kurulsun; cevap ifadesi sütun adını birebir tekrar etmesin ve sayım çetele çizgisiyle görünsün.",
        "Öğrencinin kendi cevabı da ankete katılsın; kendini sınıfla karşılaştırsın.",
        "Öğrenci sonucu yorumlayıp kendisini çoğunlukla/azınlıkla nerede bulduğunu söylesin."),
"sb07": ("Gerçek bir harita parçası ve harita anahtarı kutusu çizilsin; sembol haritanın üzerinde gösterilsin ve emoji eşleşmesi kaldırılsın.",
        "Benzer semboller çeldirici olsun (havaalanı/liman, il/ilçe merkezi).",
        "Öğrenci verilen bir haritada üç sembolü bulup ne anlattığını söylesin."),
"sb08": ("KRİTİK: kart rengin ADINI yazmak yerine RENGİN KENDİSİNİ göstersin - kazanım harita renklerini tanımaktır. Kart hiçbir kenarda kırpılmasın; denemede “Koyu yeşil ovalar” ifadesinden yalnız “ovalar” görünüyordu. Arkada gerçek bir fiziki harita dursun.",
        "Aynı rengin tonları ayrılsın (açık yeşil ova, koyu yeşil ova); yükselti basamağı kavramı verilsin.",
        "Öğrenci gerçek bir fiziki haritada renklere bakarak bir bölgeyi tarif etsin."),
"sb09": ("Bu dersteki sürüm yön adlarını kullandığı için diğer sınıflardan bir adım önde; bunu koruyarak yön düğmeleri de KUZEY/GÜNEY/DOĞU/BATI olarak adlandırılsın. Haritaya kuzey oku, ölçek ve sokak adları eklensin; görev metni rotayı söylemesin.",
        "Başlangıç noktası değişsin; öğrenci aynı hedefe farklı yönlerden gitsin.",
        "Öğrenci gittiği yolu “önce kuzeye iki adım, sonra doğuya...” diye kendisi tarif etsin."),
"sb10": ("Gerçek coğrafya görselleri kullanılsın (dağ, nehir, ova); kart çevrilince o unsurun insan yaşamına etkisi kısa sahneyle gösterilsin.",
        "Aynı unsurun hem olumlu hem sınırlayıcı etkisi karşılaştırılsın (nehir: sulama ama taşkın).",
        "Öğrenci yaşadığı yerin bir doğal unsurunun etkisini anlatsın."),
"sb11": ("Gerçek bir ev ve bina sahnesi çizilsin; her önlem o mekânda uygulanan somut bir işe dönüşsün ve roket kaldırılsın.",
        "Farklı afetler için (deprem, sel, yangın) önlem sırası karşılaştırılsın.",
        "Öğrenci evinde alınabilecek üç önlemi sırayla söylesin."),
"sb12": ("Gerçek bir plan kâğıdı açılsın; seçilen öge planın ilgili bölümüne yazılsın ve plan adım adım oluşsun. Kazanım ÜRÜN oluşturmayı istiyor.",
        "Eksik plan örnekleri karşılaştırılsın: buluşma yeri olmayan plan neden işe yaramaz?",
        "Öğrenci kendi ailesi için buluşma yerini ve iletişim kişisini yazarak planı tamamlasın."),
"sb13": ("Gerçek oyuncak fotoğrafları ve dönem görselleri kullanılsın; roket kaldırılsın. İlk turda tarihler gizlensin, sıralama oyuncağın malzemesi ve yapımından çıkarılsın.",
        "Kanıt kavramı işlensin: hangi ipucu bize eski olduğunu söylüyor?",
        "Öğrenci ailesinden bir oyuncak öyküsü toplayıp anlatsın."),
"sb14": ("Gerçek oyun sahneleri yan yana çizilsin (sokakta saklambaç / ekranda oyun); özellik iki sahnede karşılaştırılsın ve bant durdurulsun.",
        "Kısmen değişen özellikler eklensin (oyun kuralları aynı, araçlar farklı).",
        "Öğrenci bir oyunun değişen ve değişmeyen yanını söylesin."),
"sb15": ("Gerçek bir soy ağacı şablonu açılsın; seçilen öge ağacın ilgili dalına yerleşsin ve ürün gözle görülür biçimde oluşsun.",
        "Farklı kaynak türleri (fotoğraf, sözlü anlatım, belge) karşılaştırılsın.",
        "Öğrenci kendi aile ağacına iki kuşak ekleyip bir kaynak belirtsin."),
"sb16": ("Gerçek miras görselleri kullanılsın (cami, köprü, halk oyunu, yemek); kart çevrilince öge kısa bir sahneyle tanıtılsın.",
        "Somut ve somut olmayan miras ayrımı yapılsın; ölçüt tartışılsın.",
        "Öğrenci kendi çevresinden bir miras ögesi söyleyip türünü belirtsin."),
"sb17": ("Genel radar yönergesi kaldırılsın; soru somut bir miras ögesine bağlansın ve seçenekler sabit kartlarda dursun.",
        "Mirasın korunmadığı durumların sonucu gösterilsin.",
        "Öğrenci bir mirası tanımanın neden önemli olduğunu kendi cümleleriyle ifade etsin."),
"sb18": ("Gerçek kaynak görselleri kullanılsın (eski fotoğraf, mektup, nüfus cüzdanı, ses kaydı); eşleşince kaynağın anlattığı bilgi ortaya çıksın.",
        "Aynı olayı farklı anlatan iki kaynak karşılaştırılsın; kanıt kavramı işlensin.",
        "Öğrenci bir aile kaynağından çıkardığı bilgiyi anlatsın."),
"sb19": ("Gerçek yatay zaman şeridi ve dönem görselleri kullanılsın; roket kaldırılsın. İlk turda tarihler gizlensin.",
        "Olaylar arasındaki neden-sonuç bağı sorulsun: hangisi diğerini mümkün kıldı?",
        "Öğrenci Cumhuriyete giden yoldaki bir fedakârlığı kanıtıyla anlatsın."),
"sb20": ("Gerçek öncesi-sonrası sahneleri kurulsun (harf devrimi öncesi/sonrası bir tabela, kadınların seçim sandığı); emoji eşleşmesi kaldırılsın.",
        "Bir yeniliğin birden çok getirisi gösterilsin.",
        "Öğrenci bir Cumhuriyet yeniliğinin bugünkü karşılığını anlatsın."),
"sb21": ("Gerçek dönem fotoğrafları kullanılsın; durum kartı iki dönemin görselleri arasında karşılaştırılsın ve bant durdurulsun.",
        "Geçiş dönemine ait, iki tarafa da yakın örnekler çeldirici olsun.",
        "Öğrenci bir değişimi öncesi-sonrası olarak karşılaştırıp anlatsın."),
"sb22": ("Gerçek bir seçim sahnesi kurulsun: sandık, oy pusulası, aday panosu. Oy ifadesi aday adını birebir tekrar etmesin ve sayım çetele çizgisiyle görünsün.",
        "Berabere biten ve tek oyla kazanılan senaryolar eklensin; gizli oy ilkesi gösterilsin.",
        "Öğrenci sonucu yorumlasın ve seçilmeyen adayların fikirlerine ne olacağını söylesin."),
"sb23": ("Gerçek bir okul meclisi sahnesi kurulsun; kurulan cümle kürsüde okunsun ve panoya asılsın. Kartlar küçük harfle gelsin.",
        "Katılım öneren ve şikâyet eden ifadeler karşılaştırılsın.",
        "Öğrenci okulunda katılabileceği bir süreci ve fikrini kendisi yazsın."),
"sb24": ("Gerçek Millî Mücadele görselleri kullanılsın; kart çevrilince fedakârlığın anlamı kısa bir anlatımla açılsın.",
        "Cephede ve cephe gerisinde yapılan fedakârlıklar karşılaştırılsın.",
        "Öğrenci bir fedakârlığı kanıtıyla birlikte anlatsın."),
"sb25": ("KRİTİK: hedef değerler ekranda görünmüyor - kaynak satırında yalnız birim açıklaması var, hangi alanın kaç damla olduğu yazmıyor ve oyun deneme-yanılmayla çözülüyor. Veriler ya kaynak satırında okunur biçimde verilsin ya da öğrenci sayarak kendisi çıkarsın. Blok deposu grafiğin üzerine binmesin.",
        "Grafik tamamlanınca “en çok nerede su harcanıyor, kaç litre fark var?” soruları sorulsun.",
        "Öğrenci grafiği yorumlayıp evinde su tasarrufu için bir öneri getirsin."),
"sb26": ("KRİTİK: başlık “Grafik Dedektifi” olduğu hâlde ekranda grafik yok ve “60 + 40 = ?” işlemi hazır yazılı. Ekrana gerçek bir grafik konsun, soru o grafikten okunsun ve işlem yazılmasın.",
        "İki yılın grafiği yan yana verilsin; öğrenci değişimi karşılaştırsın.",
        "Öğrenci grafikten çıkardığı sonucu bir cümleyle ifade etsin - yalnız sayı değil yorum istensin."),
"sb27": ("Gerçek bir market rafı ve alışveriş sahnesi çizilsin; ürün kartı rafta bir ürün olarak görünsün ve bant durdurulsun.",
        "Bağlama göre değişen ürünler eklensin (yağmurluk yağmurlu günde ihtiyaç); ölçüt tartışılsın.",
        "Öğrenci kendi bir isteğini ve bir ihtiyacını ayırt edip nedenini söylesin."),
"sb28": ("KRİTİK: ürün kartlarında FİYAT yazmıyor - öğrenci 30 TL'yi tutturmayı bilemez. Her ürüne okunur bir fiyat etiketi konsun, sepet toplamı ve kalan bütçe hiçbir ögenin arkasında kalmadan görünsün.",
        "Bütçenin yetmediği durumlar eklensin; öğrenci ihtiyacı isteğe tercih etsin.",
        "Öğrenci kendi seçimini “şunu aldım çünkü...” diye gerekçelendirsin."),
"sb29": ("Gerçek üretim zinciri sahnesi çizilsin (tarla, değirmen, fırın, market, sofra); roket kaldırılsın ve adımlar bu mekânlarda görünsün.",
        "Farklı ürünler için zincir karşılaştırılsın (süt, ayakkabı).",
        "Öğrenci bir ürünün yolculuğunu üç aşamada anlatsın."),
"sb30": ("KRİTİK: altı parçanın beşinde son sözcük çipe sığmayıp kesiliyor (“...yetiştirmesi”, “...dikilmesi”, “...götürmesi” okunmuyor). Yazılar tam sığacak biçimde yerleşsin; emoji ipuçları kategoriyi ele vermesin.",
        "Aynı ürünün üç aşaması birlikte verilsin; öğrenci zinciri kursun.",
        "Öğrenci kendi yaşamından üretim, dağıtım ve tüketim örneği versin."),
"sb31": ("Gerçek bir ekran/uygulama arayüzü çizilsin; davranış o arayüzde bir eylem olarak görünsün ve bant durdurulsun.",
        "Görünüşte zararsız ama riskli davranışlar çeldirici olsun (tanıdık görünen hesap).",
        "Öğrenci kendi belirlediği bir güvenlik kuralını söylesin."),
"sb32": ("Genel radar yönergesi kaldırılsın; bilgi kartı sabit gelsin ve öğrenci “paylaşırım / paylaşmam” kararını gerekçe seçerek versin.",
        "Bağlama göre değişen örnekler eklensin: okul panosunda ad, internette adres; izin kavramı işlensin.",
        "Öğrenci dijital mahremiyet kuralını “... paylaşmam çünkü ...” kalıbıyla gerekçelendirsin."),
"sb33": ("Gerçek bilim insanı çocukluk anıları kullanılsın; eşleşince merakın hangi keşfe dönüştüğü kısa sahneyle gösterilsin ve emoji eşleşmesi kaldırılsın.",
        "Merakın hemen sonuç vermediği, uzun sürdüğü örnekler eklensin.",
        "Öğrenci kendi merak ettiği bir konuyu ve nasıl araştıracağını söylesin."),
"sb34": ("Gerçek bir mesajlaşma ekranı sahnesi kurulsun; adımlar o ekranda yapılan işler olarak sıralansın (ekran görüntüsü al, engelle, güvendiğin yetişkine göster). Roket kaldırılsın.",
        "Yanlış tepkiler çeldirici olsun (karşılık vermek, sessiz kalmak); sonucu gösterilsin.",
        "Öğrenci güvendiği yetişkinleri ve ne söyleyeceğini kendisi belirtsin."),
"sb35": ("Tren-tünel sahnesi kaldırılsın; ekranda bir günün saat çizelgesi olsun ve seçilen ekran süresi bu çizelgede yerini alsın; kalan zamanla neler yapılabileceği görünsün.",
        "Hafta içi ve hafta sonu karşılaştırılsın; yaşa uygun öneri aralığı gösterilsin.",
        "Öğrenci kendi ekran süresi kuralını nedeniyle birlikte söylesin."),
"sb36": ("Gerçek bir okul panosu çizilsin; kurulan kural cümlesi panoya asılsın ve gerekçe bölümü ayrı bir alan olsun. Kartlar küçük harfle gelsin.",
        "Kural ile gerekçe ayrı ayrı kurulsun: “ne yapmalı” ve “çünkü”.",
        "Öğrenci kendi dijital güvenlik kuralını gerekçesiyle yazsın."),
}

assert set(DESIGNS) == {g["id"] for g in games}


def config_summary(game):
    n = game.get("n", {})
    t = game["type"]
    if t == "beltSort":
        return f"Kaynakta {n.get('items','?')} kart ve {n.get('bins','')} kutuları tanımlı; yapı tek gerçek-zamanlı bant turu, yeni içerik turu üretilmiyor."
    if t == "memoryPairs":
        return f"Kaynakta {n.get('pairs','?')} çift tanımlı; tek tur var ve kart içerikleri sabit."
    if t == "catchDrop":
        return f"Kaynakta {n.get('rounds','?')} düşen-seçenek turu var; doğru ve çeldiriciler önceden sabit, hız ile karar aynı puana bağlanıyor."
    if t == "serveOrder":
        return f"Kaynakta {n.get('customers','?')} istek tanımlı; kart havuzu sabit."
    if t == "sentenceBuild":
        return f"Kaynakta {n.get('rounds','?')} cümle kurulumu var; her cümlenin tek doğru dizilişi tanımlı."
    if t == "orderSequence":
        return f"Kaynakta {n.get('items','?')} kartlık tek sıra var; doğru sıra sabit ve yeni olay turu üretilmiyor."
    if t == "dragMatch":
        return f"Kaynakta {n.get('sources','?')} parça ve {n.get('targets','?')} hedef var; tek sabit eşleştirme turu."
    if t == "codeGrid":
        return f"Kaynakta {n.get('rounds','?')} görev haritası var; görev metinleri yön adlarını kullanıyor fakat düğmeler yalnız ekran yönü okları."
    if t == "graphBuild":
        return f"Kaynakta {n.get('categories','?')} kategori ve toplam {n.get('blocks','?')} blok tanımlı; kategori hedefleri kaynakta var ama ekranda gösterilmiyor."
    if t == "numPad":
        return f"Kaynakta {n.get('rounds','?')} soru var; sorular düz metin olarak veriliyor ve işlem satırı hazır yazılı."
    if t == "dragSlider":
        return f"Kaynakta {n.get('rounds','?')} tahmin turu var; sabit sözcük seçeneklerinden biri seçiliyor ve ölçülen kavramın görseli tanımlı değil."
    if t == "surveyChart":
        return f"Kaynakta {n.get('options','?')} seçenek ve {n.get('responses','?')} cevap tanımlı; cevap ifadeleri seçenek adını birebir içeriyor ve sonuç yorumu adımı tanımlı değil."
    return f"Kaynakta {n.get('columns','?')} sütun ve {n.get('responses','?')} yanıt tanımlı; yanıt cümleleri sütun adını birebir içeriyor."


GROUP_FOCUS = {
    "Alan 1 · Birlikte Yaşamak": [
        "Kişisel değerlendirme kazanımlarında kart etiketleri kaldırılmalı; öğrenci kendisi hakkında konuşmalı.",
        "Saygı ve birlik kazanımları gerçek okul/mahalle sahneleriyle canlandırılmalı; bant ve servis tezgâhı şablonu kaldırılmalı.",
        "Ortak “doğru cevabı yakala” yönergesi her oyunun kendi konusuna göre yeniden yazılmalı.",
    ],
    "Alan 2 · Evimiz Dünya": [
        "Harita kazanımlarında gerçek harita ögeleri bulunmalı: renk, sembol, kuzey oku, ölçek ve harita anahtarı.",
        "Renk oyununda kart rengin adını değil kendisini göstermeli; kırpılan bölüm tam da renk adı olduğu için karar imkânsızlaşıyor.",
        "Navigasyon oyununda yön düğmeleri coğrafi yön adlarını taşımalı ve öğrenci yolu kendisi tarif etmeli.",
    ],
    "Alan 3 · Ortak Mirasımız": [
        "Kanıta dayalı sıralama kazanımlarında tarihler ilk turda gizlenmeli; sıralama nesnenin özelliğinden çıkarılmalı.",
        "Kaynak ve miras oyunlarında gerçek görseller (fotoğraf, belge, eser) kullanılmalı.",
        "Ürün oluşturma kazanımları gerçek üretime bağlanmalı: soy ağacı ekranda oluşmalı.",
    ],
    "Alan 4 · Yaşayan Demokrasimiz": [
        "Cumhuriyet kazanımları öncesi-sonrası karşılaştırmasıyla somutlaştırılmalı; roket sahnesi kaldırılmalı.",
        "Seçim oyununda oy ifadesi aday adını tekrarlamamalı; gizli oy ve sonuç yorumu eklenmeli.",
        "Katılım kazanımı gerçek bir okul meclisi sahnesine ve öğrencinin kendi fikrine bağlanmalı.",
    ],
    "Alan 5 · Hayatımızdaki Ekonomi": [
        "Karar için gereken sayısal veri ekranda bulunmalı: grafik hedefleri ve ürün fiyatları şu an eksik.",
        "Grafik Dedektifi'nde gerçek bir grafik bulunmalı ve işlem hazır yazılmamalı.",
        "Ekonomi köprüsünde parça yazıları kesilmemeli; üretim-dağıtım-tüketim ayrımı okunabilir olmalı.",
    ],
    "Alan 6 · Teknoloji ve Sosyal Bilimler": [
        "Dijital güvenlik kazanımları gerçek arayüz sahneleriyle çalışmalı; gerekçelendirme adımı eklenmeli.",
        "Siber zorbalık adımları gerçek mesajlaşma ekranında uygulanmalı ve roket sahnesi kaldırılmalı.",
        "Ekran süresi kararı tren-tünel yerine bir günün saat çizelgesine bağlanmalı.",
    ],
}

GROUP_COLORS = [CORAL, TEAL, PURPLE, GOLD, BLUE, GREEN]

# Kaç oyun ortak "genel yönerge" kullanıyor?
generic_prompt = [g for g in games if "doğru cevabı yakala" in g["instruction"].lower()]
belt_n = sum(1 for g in games if g["type"] == "beltSort")
answer_leak = ["h02", "h09", "h10", "h26", "h29", "h05", "h18"]

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
story += [box("1. Karar için gereken veri ekranda yok - iki oyun oynanamaz durumda",
    ["Su Tüketim Grafiği'nde kaynak satırında yalnız “Bir evin günlük su tüketimi (1 damla = 10 litre)” yazıyor; hangi alanın kaç damla olduğu hiçbir yerde belirtilmemiş. Hedef değerler kaynak dosyada tanımlı (banyo 6, mutfak 4, çamaşır 5, bahçe 2) ama ekrana hiç yazılmıyor, dolayısıyla oyun ancak deneme-yanılmayla çözülebiliyor. Bilinçli Alışveriş'te müşteri “Bütçem 30 TL” diyor fakat ürün kartlarında (ekmek, süt, defter, peynir, meyve, çikolata) fiyat yazmıyor; öğrenci 30 TL'yi nasıl tuttururacağını bilemez. Üstelik sepet toplamını gösteren “tepsi boş - 0 / 30” satırı ürün kartlarının arkasında kalıp okunmuyor."],
    PALE_CORAL, CORAL), Spacer(1, 1.7 * mm)]
story += [box("2. Grafik Dedektifi'nde grafik yok, işlem hazır yazılı",
    ["Oyunun başlığı “Grafik Dedektifi”, alt başlığı “Grafikten çıkarım yap”, kazanımı ise “tüketim oranlarını karşılaştırır ve çıkarım yapar”. Ekranda ise hiçbir grafik bulunmuyor; soru düz metin olarak veriliyor ve hemen altında “60 + 40 = ?” işlemi yazılı duruyor. Grafik olmadan grafik okuma ölçülemez; işlem de verildiği için geriye kalan tek beceri toplama yapmak oluyor. Sosyal bilgiler kazanımı bir matematik alıştırmasına dönüşmüş."],
    PALE_GOLD, GOLD), Spacer(1, 1.7 * mm)]
story += [box("3. Harita rengi oyununda renk gösterilmiyor, üstelik renk adı kırpılıyor",
    ["Kazanım “harita renklerini tespit eder ve anlamlandırır” diyor, ama bant kartı rengin kendisini değil adını yazıyor - beyaz zeminde siyah yazı. Daha da kötüsü, denemede kart bandın sol kenarında kırpıldı ve “Koyu yeşil ovalar” ifadesinden yalnız “ovalar” görünüyordu; yani kararın dayandığı renk bilgisi tam da kaybolan bölümdeydi. Kutuların üzerinde renk örnekleri var, kart tarafında yok."],
    PALE_BLUE, BLUE), Spacer(1, 1.7 * mm)]
story += [box("4. Ekonomi Köprüsü'nde altı parçanın beşinde son sözcük kesiliyor",
    ["Parça çipleri yazıya dar geldiği için “Çiftçinin domates yetiştirmesi”, “Fabrikada ayakkabı dikilmesi”, “Ailenin salata yapıp yemesi”, “Tırın sebzeyi hâle götürmesi” ve “Marketin rafa ürün dizmesi” ifadelerinin son sözcükleri okunmuyor. Öğrenci eylemin ne olduğunu tam göremeden üretim, dağıtım ve tüketim ayrımı yapmak zorunda kalıyor. Hedef kartlarındaki tanımlar (“ÜRETİM - mal veya hizmet oluşturmak”) iyi kurulmuş; sorun yalnız yerleşimde."],
    PALE_TEAL, TEAL), Spacer(1, 1.7 * mm)]
story += [box("5. Navigasyon oyunu diğer sınıflardan daha iyi; teknik çökme yok",
    ["Harita Navigasyonu bu dersin olumlu farkı: görev metni “kuzeye ve doğuya ilerle” diyerek gerçek yön adlarını kullanıyor ve yönerge ekran yönü ile coğrafi yön arasındaki çeviriyi açıklıyor - 2. sınıf Doğadan Yön Bulma ve 3. sınıf Kroki Rehberi'nde bu yoktu. Yine de yön düğmeleri hâlâ yalnız ok işaretleri taşıyor, haritada kuzey oku ve ölçek yok, görev metni rotayı söylüyor. sb01-sb36 arasındaki 36 oyunun tamamı yüklendi; motorlarda çökme veya konsol hatası oluşmadı."],
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
        theme_table = Table([[P(f"Alan {group_index + 1}", badge), P(clean(last_group), theme_title)]], colWidths=[30 * mm, 146 * mm], rowHeights=[47 * mm])
        theme_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), accent), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                         ("ALIGN", (0, 0), (0, 0), "CENTER"), ("LEFTPADDING", (1, 0), (1, 0), 12),
                                         ("RIGHTPADDING", (1, 0), (1, 0), 12), ("ROUNDEDCORNERS", [10])]))
        story += [Spacer(1, 20 * mm), theme_table, Spacer(1, 8 * mm), P(f"Bu alanda {count} oyun var. Ana düzeltme odağı", h2)]
        story += bullets(GROUP_FOCUS[last_group])
        story += [Spacer(1, 5 * mm), box("Alan kabul eşiği", ["Bu alandaki her oyun üç kademeli tur ve en az bir öğrenci üretimi/uygulaması olmadan tamamlanmış sayılmayacak.", "Başlık, görünen sahne, seslendirme, kontrol ve ölçülen hayat bilgisi kazanımı aynı hedefi gösterecek."], PALE_TEAL, TEAL), PageBreak()]

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
    "sb01-sb36 arasındaki 36 oyun üç kademeli turla baştan sona test edilir; görünen başlık, sahne, kontrol, ses ve ölçülen kazanım kayıt altına alınır.",
    "Su Tüketim Grafiği'nde kategori hedefleri ekranda okunur; Bilinçli Alışveriş'te her ürünün fiyatı ve kalan bütçe görünür - iki oyun da şu an veri eksikliğinden oynanamıyor.",
    "Grafik Dedektifi'ne gerçek bir grafik eklenir; soru grafikten okunur ve işlem hazır yazılmaz.",
    "Harita Rengi Bandı'nda kart rengin kendisini gösterir ve hiçbir kenarda kırpılmaz.",
    "Ekonomi Köprüsü'nde parça yazıları çipe tam sığar; hiçbir sözcük kesilmez.",
    "Harita Navigasyonu'nda yön düğmeleri kuzey/güney/doğu/batı olarak adlandırılır, haritaya kuzey oku ve ölçek eklenir, görev metni rotayı söylemez.",
    "Roket-YAKIT sahnesi beş sıralama oyununun tamamından kaldırılır; köprü oyunlarında emoji eşleşmesi giderilir.",
    "Her oyunda en az üç farklı içerik turu, açıklayıcı yanlış geri bildirimi ve öğrencinin kendi örneğini/gerekçesini içeren bir kapanış bulunur.",
])
story += [Spacer(1, 4 * mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 2. sınıf hayat bilgisi listesindeki h01-h36 oyunlarını kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, görsel kanıt, mekanik, üç tur, geri bildirim, öğrenci kanıtı ve test gereksinimlerini ayrıntılı biçimde tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)

reader = PdfReader(str(OUT))
print({"pages": len(reader.pages), "games": len(games), "genericPrompt": len(generic_prompt),
       "beltGames": belt_n, "bytes": OUT.stat().st_size, "output": str(OUT)})
