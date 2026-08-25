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
OUT = ROOT / "output/pdf/1_sinif_sayma_oyunlari_detayli_duzeltmeler.pdf"
GAMES_JSON = ROOT / "tmp/pdfs/sayma1_games.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

games = json.loads(GAMES_JSON.read_text(encoding="utf-8"))
assert len(games) == 20

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
    canv.drawString(MX, 8.2 * mm, "1. Sınıf Sayma - Ayrıntılı Oyun Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 8.2 * mm, str(canv.getPageNumber()))
    canv.restoreState()


# --- Rakam biçimi: hangi rakamda kavis var, köşeli çizim neyi bozuyor? ----
CURVED = {
    "s0": ("0", "Tam çember", "Ekranda sekizgen görünüyor; çocuk yuvarlak yerine köşeli bir kapalı şekil çiziyor. 0'ın tek ayırt edici özelliği kesintisiz yuvarlaklığı olduğu için rakam biçimi hiç öğretilmemiş oluyor."),
    "s2": ("2", "Üst kavis", "Kuğu boynunun kavisi kırık çizgiye dönüyor; 2'nin üst kavisi ile Z harfinin köşesi ayırt edilemez hâle geliyor."),
    "s3": ("3", "İki yarım daire", "İki kavis birer köşeli zikzak oluyor; 3 ile ters E biçimi karışıyor. Bu, 1. sınıfta en sık görülen ayna/biçim hatalarından birini pekiştiriyor."),
    "s5": ("5", "Göbek kavisi", "5'in göbeği köşeli çıkıyor; çocuk yuvarlak karnı değil kırık bir çizgi öğreniyor."),
    "s6": ("6", "Alt daire", "6'nın alt dairesi altıgen görünüyor (ekranda doğrulandı); daire kapanışının yuvarlaklığı kayboluyor."),
    "s8": ("8", "İki daire", "8 tamamen köşeli bir zikzak sekizgen olarak görünüyor (ekranda doğrulandı); rakamın iki yuvarlak gözü hiç oluşmuyor."),
    "s9": ("9", "Üst daire", "9'un üst dairesi altıgene dönüşüyor (ekranda doğrulandı); 9 ile 4 arasındaki biçim farkı bulanıklaşıyor."),
}

STRAIGHT_OK = {"s1": "1", "s4": "4", "s7": "7"}


ENGINE_TRACE = ("rakam (çizim atölyesi) motoru",
    "Ekranda kesikli kılavuz yol, sarı BAŞLA topu ve sıralı kontrol noktaları var; parmak BAŞLA'dan çıkıp noktalara sırayla değince iz ilerliyor. "
    "Yazım YÖNÜ doğru biçimde zorunlu tutuluyor - bu motorun en güçlü yanı. Ancak kılavuz yol düz çizgi parçalarıyla (lineTo) çiziliyor; kaynakta hiçbir eğri tanımı yok.")

ENGINE_WRITE = ("rakam (sayı yazma atölyesi) motoru",
    "İki basamaklı sayı için iki yuva açılıyor ve her basamağın nokta dizisi 0-9 şablon tablosundan üretiliyor. "
    "Yuvaların arkasında hedef sayının soluk hayalet kopyası duruyor, sağ üstte ise aynı sayı büyük puntoyla yazılı.")


TYPE_RISK_TRACE = (
    "Rakamın gerçek biçimi öğretilmiyor: kavisli rakamlar köşeli çokgen olarak çizdiriliyor. "
    "Bu ders tam olarak 'rakamın yazım yönünü ve biçimini kas hafızasına almak' üzerine kurulu olduğu için, "
    "yanlış biçimin tekrarlanması kazanımın kendisini ters yönde çalıştırıyor - çocuk defterine köşeli rakam yazmayı öğreniyor.")

TYPE_RISK_WRITE = (
    "Hedef sayı ekranda hem büyük puntoyla yazılı hem de yuvaların arkasında hayalet kopya olarak duruyor. "
    "'Duyduğu sayıyı rakamlarla yazar' kazanımı böylece dinleyip yazmaya değil, gördüğünü kopyalamaya iniyor; "
    "sayının hangi basamağa yazılacağı da düşünülmeden hayaletin üzerinden geçiliyor.")

RISK_COMMON = (
    "Yoldan sapınca (74 piksel) can gidiyor, ekran sarsılıyor ve kırmızı flaş patlıyor. 6-7 yaşındaki bir çocuk için "
    "parmakla çizimde sapma normal bir motor gelişim durumudur; ceza vermek yerine yol yeniden gösterilmelidir. Üç sapmada oyun bitiyor.")

SCENE_NOUN = {
    "cave": ("mağara", "uyuyan ayı"), "space": ("fırlatma rampası", "roket"),
    "lake": ("göl", "kuğu"), "pond": ("nilüfer havuzu", "kurbağa"),
    "sea": ("deniz", "yelkenli"), "apple": ("elma", "kurt"),
    "leaf": ("yaprak", "salyangoz"), "valley": ("vadi", "bumerang"),
    "track": ("yarış pisti", "yarış arabası"), "clouds": ("bulutlu gökyüzü", "balon"),
    "wizard": ("büyücü masası", "kazan"), "airlock": ("uzay istasyonu kapısı", "şifre paneli"),
    "map": ("hazine haritası", "pusula ve gemi"), "nest": ("dinozor yuvası", "numaralı yumurtalar"),
    "typewriter": ("daktilo", "kâğıt"), "opensky": ("açık gökyüzü", "uçak"),
    "robot": ("robot", "batarya yuvaları"), "wagons": ("tren", "renkli vagonlar"),
    "orchard": ("elma bahçesi", "sepet"), "iceberg": ("buzul", "penguen"),
}


def risk_scene(game):
    yer, kim = SCENE_NOUN[game["scene"]]
    return (f"Başlıktaki karakter ve mekân ekranda hiç yok: oyun ortak karanlık yıldız zemininde açılıyor. "
            f"Çocuk “{clean(game['title'])}” başlığını görüyor ama ne {yer} ne {kim} ekranda var; "
            f"hikâye motivasyonu ile görünen ekran arasında bağ kurulamıyor ve bitiş ödülü karşılıksız kalıyor.")


FEEDBACK_TRACE = [
    "Yoldan sapmada can gitmesin: iz sönümlensin, kılavuz kısa bir animasyonla yeniden gösterilsin ve çocuk aynı noktadan devam etsin.",
    "Ekran sarsıntısı ve kırmızı flaş kaldırılsın; bunun yerine yumuşak bir 'tekrar dene' sesi ve parmağın döneceği yeri gösteren ok kullanılsın.",
    "Doğru tamamlanan hamlede rakam kendi mürekkebiyle kalıcı olsun ve sahne ödülü (başlıktaki karakter) gerçekten canlansın.",
]

FEEDBACK_WRITE = [
    "Yanlış basamağa yazılırsa sayı silinmesin; hangi yuvanın onlar hangisinin birler olduğu nesnelerle (10'luk demet ve tek küpler) gösterilsin.",
    "Süre dolduğunda oyun bitmesin; süre yalnız isteğe bağlı bir hız rozeti olsun, doğruluk ölçümüne karışmasın.",
    "Bitişte çocuğun yazdığı sayı, söylenen sayı ve nesne miktarı yan yana gösterilerek üçü arasındaki bağ kurulsun.",
]

ACCEPT_TRACE = [
    "Kılavuz yol ve tamamlanan iz eğrisel çizilecek (Bezier/spline); 0, 2, 3, 5, 6, 8, 9 rakamlarında hiçbir köşe görünmeyecek.",
    "Başlıktaki sahne gerçekten çizilecek; cfg.scene motor tarafından okunup ilgili dekor kurulacak.",
    "Yoldan sapma can kaybettirmeyecek; en az üç farklı tur (kılavuzlu, soluk kılavuzlu, kılavuzsuz) bulunacak.",
    "Rakam adı ve yazım yönü her turda sesli okunacak; ses dosyası olmayan oyun tamamlanmış sayılmayacak.",
]

ACCEPT_WRITE = [
    "Hedef sayı ekranda yazılı görünmeyecek; yalnız sesli söylenecek ve istenirse tekrar dinlenebilecek.",
    "Yuvaların arkasındaki hayalet kopya en geç ikinci turda kalkacak; üçüncü tur tamamen boş yuvayla yapılacak.",
    "Onlar ve birler basamağı nesne temsiliyle (10'luk demet + birlikler) birlikte gösterilecek; sayı ile miktar eşleşecek.",
    "Her oyunda en az üç farklı sayı turu bulunacak ve sayılar her açılışta değişecek.",
]


DESIGNS = {
"s0": ("Gerçek bir mağara ağzı çizilsin: içeride uyuyan ayı görünsün, çizilen 0 mağaranın yuvarlak kapı taşı olsun ve tamamlanınca taş yuvarlanıp kapıyı kapatsın. Kılavuz kesintisiz eğri olsun, köşe kalmasın.",
       "Kılavuz soluklaşsın; yalnız BAŞLA topu ve yön oku kalsın. Çocuk çemberi kendi kapatsın.",
       "Kılavuzsuz boş taş yuvasına 0 çizilsin; ardından ekranda 'sıfır tane' anlamı bir boş sepetle gösterilip rakamla eşleştirilsin."),
"s1": ("Fırlatma rampası ve roket çizilsin; birinci hamle roketin burnu, ikinci hamle gövdesi olsun ve rakam bitince roket gerçekten yükselsin.",
       "Kılavuz soluklaşsın; iki hamlenin sırası çocuk tarafından hatırlansın.",
       "Kılavuzsuz yazılsın; sonra ekranda 1 tane nesne gösterilip rakamla eşleştirilsin."),
"s2": ("Göl, nilüfer ve kuğu çizilsin; birinci hamle kuğunun boynu (kesintisiz kavis), ikinci hamle su yüzeyi olsun. Kuğu tamamlanınca göle süzülsün.",
       "Kılavuz soluklaşsın; kavisin yuvarlaklığı korunarak çizilsin.",
       "Kılavuzsuz yazılsın; 2 kuğu sayılarak rakamla eşleştirilsin."),
"s3": ("Nilüfer yaprakları ve kurbağa çizilsin; iki kavis kurbağanın iki zıplayışı olsun ve her kavis tamamlanınca kurbağa bir yaprak ilerlesin. Kavisler kesintisiz eğri olsun.",
       "Kılavuz soluklaşsın; iki kavisin de yuvarlak kalması istensin.",
       "Kılavuzsuz yazılsın; 3 kurbağa sayılarak rakamla eşleştirilsin."),
"s4": ("Deniz, tekne gövdesi ve direk çizilsin; birinci hamle yelkenin kenarı, ikinci hamle direk olsun. Tamamlanınca yelken açılıp gemi hareket etsin.",
       "Kılavuz soluklaşsın; iki ayrı hamlenin bağımsızlığı korunsun.",
       "Kılavuzsuz yazılsın; 4 nesne sayılarak rakamla eşleştirilsin."),
"s5": ("Kırmızı bir elma ve içinden bakan kurt çizilsin; göbek kavisi kesintisiz eğri olsun ve şapka hamlesi tamamlanınca kurt elmadan çıksın.",
       "Kılavuz soluklaşsın; göbek kavisinin yuvarlaklığı korunsun.",
       "Kılavuzsuz yazılsın; 5 elma sayılarak rakamla eşleştirilsin."),
"s6": ("Yaprak üzerinde bir salyangoz çizilsin; 6'nın alt dairesi salyangozun kabuğu olsun ve spiral kesintisiz eğriyle örülsün. Tamamlanınca salyangoz yaprakta ilerlesin.",
       "Kılavuz soluklaşsın; dairenin kapanışı çocuk tarafından yapılsın.",
       "Kılavuzsuz yazılsın; 6 nesne sayılarak rakamla eşleştirilsin."),
"s7": ("Vadi manzarası ve bumerang çizilsin; yatay çizgi atış hattı, çapraz çizgi iniş yolu olsun ve tamamlanınca bumerang geri dönsün.",
       "Kılavuz soluklaşsın; köşenin keskinliği korunsun (7 gerçekten köşeli bir rakamdır).",
       "Kılavuzsuz yazılsın; 7 nesne sayılarak rakamla eşleştirilsin."),
"s8": ("Gerçek bir yarış pisti kuşbakışı çizilsin ve araba çizgiyi izlesin; 8'in iki gözü kesintisiz eğrilerle, hiç köşe olmadan oluşsun. Tamamlanınca araba turu bitirsin.",
       "Kılavuz soluklaşsın; tek hamlede kesintisiz çizim istensin.",
       "Kılavuzsuz yazılsın; 8 nesne sayılarak rakamla eşleştirilsin."),
"s9": ("Bulutlu bir gökyüzü ve balon çizilsin; 9'un dairesi balonun kendisi, düz çizgi ipi olsun. Daire kesintisiz eğri olsun ve tamamlanınca balon yükselsin.",
       "Kılavuz soluklaşsın; dairenin yuvarlaklığı korunsun.",
       "Kılavuzsuz yazılsın; 9 nesne sayılarak rakamla eşleştirilsin."),
"s10": ("Büyücü, kazan ve masa çizilsin; 1 asa, 0 kazanın ağzı olsun. İki basamak ayrı ayrı yazıldıktan sonra kazandan sihir çıksın. 0'ın kavisi eğrisel olsun.",
        "Kılavuz soluklaşsın; onlar-birler sırası çocuk tarafından korunsun.",
        "Hedef sayı yazılı görünmeden sesli söylensin; 10'luk bir demet ve 0 birlik nesneyle sayı-miktar bağı kurulsun."),
"n1": ("Uzay istasyonu kapısı (airlock) ve şifre paneli çizilsin; yazılan rakamlar panele düşsün ve doğru şifrede kapı gerçekten açılsın. Sağ üstteki büyük '14' yazısı ve hayalet şablon KALDIRILSIN.",
       "Sayı yalnız sesli söylensin; iki yuva boş dursun ve hangisinin onlar hangisinin birler olduğu etiketle gösterilsin.",
       "10'luk demet ve 4 birlik nesne gösterilip 'kaç eder?' sorusuyla sayı üretilsin, sonra yazılsın."),
"n2": ("Eski bir hazine haritası, pusula ve yelkenli çizilsin; adalar numaralı olsun. Yazılan sayı pusulaya işlensin ve gemi o adaya yol alsın. Ekrandaki yazılı '17' kaldırılsın.",
       "Sayı yalnız sesli söylensin; çocuk önce haritada 17 numaralı adayı bulsun, sonra yazsın.",
       "Ada numaraları karışık dizilsin; 17'nin 10'dan büyük 20'den küçük olduğu sayı doğrusunda gösterilsin."),
"n3": ("Dinozor yuvası ve numaralı yumurtalar çizilsin; yumurtaların üzerinde sayılar okunsun. KRİTİK: 'Hangi yumurtada 12 yazıyor?' sorusu sorulurken cevabın ekranda dört ayrı yerde yazılı olması (alt başlık, tilki balonu, hayalet şablon, görev metni) giderilsin.",
       "Seçenek sayısı artsın ve yakın çeldiriciler kullanılsın (12 / 21 / 20); basamak karışıklığı çalışılsın.",
       "Yumurtaya yazılan sayı kadar yavru dinozor çıksın; sayı ile miktar birebir eşleşsin."),
"n4": ("Eski bir daktilo ve kâğıt çizilsin; yazılan rakam tuşa basılmış gibi kâğıda düşsün. SÜRE BASKISI KALDIRILSIN - 45 saniyelik geri sayım 1. sınıf çocuğu için yazma kalitesini bozar ve kaygı üretir.",
       "Süre yalnız isteğe bağlı bir 'hız rozeti' olarak sunulsun; doğruluk puanına karışmasın.",
       "Kılavuzsuz yazılsın; 16'nın onlar ve birler basamağı nesneyle doğrulansın."),
"n5": ("Açık gökyüzü, bulutlar ve uçak çizilsin; uçak yazılan izi gerçekten takip edip arkasında duman bıraksın. Sağ üstteki büyük '19' kaldırılsın - bu oyunun amacı zaten kılavuzsuz yazmaktır, sayının yazılı durması amacı boşa çıkarıyor.",
       "Sayı yalnız sesli söylensin; yuvalar tamamen boş olsun.",
       "19'un 20'den bir eksik olduğu sayı doğrusunda gösterilip yazılsın."),
"n6": ("Robot ve batarya yuvaları çizilsin; yanan yuvanın sayısı panele yazılınca o yuva gerçekten dolsun. Üç tur zaten var - bu oyun tur yapısı bakımından örnek alınmalı.",
       "İkinci turda kılavuz soluklaşsın.",
       "Üçüncü turda kılavuz kalksın; 11, 15 ve 20 sayı doğrusuna yerleştirilerek büyüklük sırası kurulsun."),
"n7": ("Renkli vagonlardan oluşan bir tren çizilsin; renk seçimi vagona dokunarak yapılsın ve yazılan numara vagonun yan tarafına işlensin. Tren tamamlanınca hareket etsin.",
       "Renk ve sayı birlikte istensin (mavi vagona 12); iki bilgiyi aynı anda tutma çalıştırılsın.",
       "Vagonlar numara sırasına dizilsin; 12 ile 16 arasındaki büyüklük ilişkisi kurulsun."),
"n8": ("Elma bahçesi, ağaçlar ve sepet çizilsin; çiftçinin istediği kadar elma sepete toplansın ve yazılan sayı sepetin etiketine işlensin. Sayı ile toplanan elma sayısı birebir aynı olsun.",
       "Elmalar 10'luk kasa ve tek elma olarak gruplansın; 18 = 10 + 8 görünür olsun.",
       "Çiftçi farklı miktar istesin; çocuk önce nesneyi saysın sonra sayıyı yazsın."),
"n9": ("Buzul, deniz ve penguen çizilsin; yazılan sayı buzun üzerine işlenince buz kalınlaşıp penguen bir adım ilerlesin. İki tur var, üçe çıkarılsın.",
       "İkinci turda kılavuz soluklaşsın; 13 ve 20 sayı doğrusunda karşılaştırılsın.",
       "Üçüncü turda kılavuzsuz yazılsın; penguenin geçtiği buzların numaraları sırayla okunsun."),
}

assert set(DESIGNS) == {g["id"] for g in games}


def current_state(game):
    t = game["type"]
    bits = []
    if t == "numberTrace":
        eng, obs = ENGINE_TRACE
        bits.append(f"Kaynak yönerge: “{clean(game['instruction'])}” Gerçek ekranda görev <b>{eng}</b> içinde açılıyor. {obs}")
        stroke_txt = f"Kaynakta {game['strokes']} hamle ve toplam {sum(game['pts'])} kontrol noktası tanımlı"
        if game["id"] in CURVED:
            d, part, harm = CURVED[game["id"]]
            bits.append(f"{stroke_txt}; noktalar düz çizgilerle bağlandığı için <b>{d} rakamının {part.lower()}ı köşeli çıkıyor</b>. {harm}")
        else:
            d = STRAIGHT_OK.get(game["id"], "")
            bits.append(f"{stroke_txt}. {d} zaten düz çizgilerden oluştuğu için biçim bozulması yok; bu oyunun asıl eksiği sahne ve tur sayısı.")
    else:
        eng, obs = ENGINE_WRITE
        bits.append(f"Kaynak yönerge: “{clean(game['instruction'])}” Gerçek ekranda görev <b>{eng}</b> içinde açılıyor. {obs}")
        extra = ""
        if game.get("pick"):
            extra = f" Ayrıca bir seçim adımı var: “{clean(game['pick'])}” - ancak sorunun cevabı ekranın dört ayrı yerinde yazılı."
        if game.get("time"):
            extra += f" Tur {clean(game['time'])} ile sınırlı."
        if game.get("faint"):
            extra += " Kaynakta faintGuide açık: kılavuz kasten soluk çiziliyor."
        bits.append(f"Kaynakta hedef {clean(game['target'])} ve {game['rounds']} tur tanımlı.{extra}")
    bits.append(f"Kaynakta <b>scene: \"{game['scene']}\"</b> tanımlı ama motor bu alanı hiç okumuyor; sahne çizilmiyor ve oyun ortak karanlık yıldız zemininde açılıyor. Bitiş metni (“{clean(game['finale'])}”) ekranda karşılığı olmayan bir olayı anlatıyor.")
    return bits


def risks(game):
    out = []
    out.append(TYPE_RISK_TRACE if game["type"] == "numberTrace" else TYPE_RISK_WRITE)
    out.append(risk_scene(game))
    out.append(RISK_COMMON)
    if game.get("time"):
        out.append("Süre baskısı bu yaşta yazı kalitesini düşürür ve kaygı üretir; el yazısı öğreniminde hız, doğruluk oturmadan ölçülmemelidir.")
    if game["type"] == "numberTrace":
        out.append("Oyunda ses yok: rakamın adı ve yazım yönü seslendirilmiyor; okuma öncesi dönemdeki çocuk yalnız yazılı yönergeye bırakılıyor.")
    return out


GROUP_FOCUS = {
    "Rakam Yazma (0-5)": [
        "Kavisli rakamlarda (0, 2, 3, 5) kılavuz eğrisel çizilmeli; köşeli çokgen biçimi tamamen kaldırılmalı.",
        "Her oyunun başlığındaki sahne (mağara, göl, deniz, elma) gerçekten çizilmeli; ortak yıldız zemini kaldırılmalı.",
        "Rakam yazımı bittikten sonra o rakam kadar nesne sayılarak sayı-miktar bağı kurulmalı.",
    ],
    "Rakam Yazma (6-10)": [
        "6, 8 ve 9'un daireleri kesintisiz eğri olmalı; şu an üçü de çokgen olarak çiziliyor.",
        "Sahne ödülleri (salyangoz, bumerang, yarış arabası, balon) ekranda gerçekten canlanmalı.",
        "10 sayısıyla birlikte onlar-birler ayrımı nesne temsiliyle tanıtılmalı.",
    ],
    "İki Basamaklı Sayılar (10-20)": [
        "Hedef sayı ekranda yazılı görünmemeli; yalnız sesli söylenmeli - aksi hâlde kazanım kopyalamaya iner.",
        "Yuvaların arkasındaki hayalet şablon kademeli kalkmalı; son tur boş yuvayla yapılmalı.",
        "Onlar ve birler basamağı 10'luk demet + birlik nesnelerle görünür kılınmalı; süre baskısı kaldırılmalı.",
    ],
}

GROUP_COLORS = [CORAL, TEAL, BLUE]

trace_n = sum(1 for g in games if g["type"] == "numberTrace")
write_n = sum(1 for g in games if g["type"] == "numberWrite")
single_round = sum(1 for g in games if g["type"] == "numberTrace" or g.get("rounds", 1) == 1)
curved_n = len(CURVED)

doc = BaseDocTemplate(
    str(OUT), pagesize=A4, rightMargin=MX, leftMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
    title="1. Sınıf Sayma Oyunları - Ayrıntılı Düzeltmeler", author="Macera Akademi oyun incelemesi",
)
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

story = [Spacer(1, 14 * mm), P("MACERA AKADEMİ", cover_kicker),
         P("1. Sınıf Sayma Oyunları<br/>Ayrıntılı Düzeltmeler", cover_title),
         P("20 oyunun kaynak yapılandırması çıkarılarak, oyunlar 390x844 telefon görünümünde tek tek açılarak ve çizim motorunun kodu satır satır incelenerek hazırlanmıştır.", cover_sub)]
cover_box = Table([[P("<b>Kapsam</b><br/>Bu belge s0-s10 (rakam yazma) ve n1-n9 (iki basamaklı sayılar) oyunlarının tamamını kapsar. Her oyun için denemede görülen mevcut yapı, eğitimsel risk, özgün sahne ve yeni oynanış, üç kademeli tur, geri bildirim ve ölçülebilir kabul koşulları ayrı ayrı verilir.")]], colWidths=[153 * mm])
cover_box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL), ("BOX", (0, 0), (-1, -1), 0.7, TEAL),
                               ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                               ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12)]))
story += [cover_box, Spacer(1, 8 * mm), P("İnceleme yöntemi", h2)]
story += bullets([
    "Sayma dersindeki 20 oyunun kaynak yapılandırması (sahne, mürekkep, kılavuz, hamle noktaları, tur ve bitiş tanımları) çıkarıldı.",
    "Oyunlar 390x844 telefon görünümünde açıldı; 0, 8, 6, 9 rakamlarının ekrandaki biçimi, iki basamaklı sayı yuvaları, seçim adımı ve süreli tur doğrudan gözlendi.",
    "Çizim motorunun kaynak kodu incelendi: kılavuz çizim yöntemi, yakalama ve sapma toleransları, can kaybı koşulu ve sahne alanının okunup okunmadığı doğrulandı.",
    "Düzeltmeler rakam biçiminin doğruluğu, başlık-sahne uyumu, cevabı sızdıran ögeler, ceza mekanizması, tur sayısı ve sayı-miktar bağını birlikte ele alır.",
])
story += [PageBreak()]

story += [P("Testten çıkan öncelikli bulgular", h1)]
story += [box(f"1. Kavisli rakamlar köşeli çiziliyor - {curved_n} rakam etkileniyor",
    [f"Motor kılavuz yolu ve tamamlanan izi düz çizgi parçalarıyla bağlıyor; kaynakta hiçbir eğri tanımı yok. Bu yüzden 0 sekizgen, 8 köşeli zikzak, 6 ve 9'un daireleri altıgen olarak görünüyor (dördü de ekranda doğrulandı). Etkilenen rakamlar: 0, 2, 3, 5, 6, 8, 9. Bu dersin tek amacı rakamın biçimini ve yönünü kas hafızasına almak olduğu için, yanlış biçimin tekrar tekrar çizdirilmesi kazanımı ters yönde çalıştırıyor."],
    PALE_CORAL, CORAL), Spacer(1, 1.7 * mm)]
story += [box("2. Yirmi sahne tanımı kodda duruyor ama hiçbiri çizilmiyor",
    ["Her oyunun kaynağında kendine özgü bir sahne adı var (cave, lake, pond, sea, apple, leaf, valley, track, clouds, wizard, airlock, map, nest, typewriter, opensky, robot, wagons, orchard, iceberg, space). Motor cfg.ink, cfg.guide ve cfg.finale alanlarını okuyor fakat cfg.scene alanını hiç okumuyor. Sonuç: 'Uyuyan Ayı', 'Dinozor Kuluçkası', 'Sihirli Daktilo' gibi 20 farklı başlığın tamamı aynı karanlık yıldız zemininde açılıyor; ayı da mağara da daktilo da ekranda yok."],
    PALE_GOLD, GOLD), Spacer(1, 1.7 * mm)]
story += [box("3. İki basamaklı sayı oyunlarında hedef sayı ekranda yazılı",
    ["n1-n9 oyunlarında yazılması istenen sayı sağ üstte büyük puntoyla duruyor, alt başlıkta tekrar ediyor ve yuvaların arkasında soluk hayalet kopya olarak bekliyor. 'Duyduğu sayıyı rakamlarla yazar' kazanımı böylece dinleyip yazmaya değil kopyalamaya iniyor. Dinozor Kuluçkası'nda durum daha ağır: 'Hangi yumurtada 12 yazıyor?' sorusu sorulurken 12 sayısı ekranın dört ayrı yerinde yazılı ve seçenekler 15/12/18."],
    PALE_BLUE, BLUE), Spacer(1, 1.7 * mm)]
story += [box("4. Yoldan sapma can kaybettiriyor; süre baskısı var",
    ["Parmak kılavuz yoldan 74 piksel uzaklaşınca iz kopuyor, bir can gidiyor, ekran sarsılıyor ve kırmızı flaş patlıyor; üç sapmada oyun bitiyor. Bu yaşta parmakla çizimde sapma normal bir motor gelişim durumudur ve cezalandırılmamalıdır. Sihirli Daktilo'da ayrıca 45 saniyelik geri sayım var - hız, doğruluk oturmadan ölçülüyor."],
    PALE_TEAL, TEAL), Spacer(1, 1.7 * mm)]
story += [box(f"5. {single_round} oyun tek turluk; rakam çizme oyunlarında ses yok",
    [f"Toplam {len(games)} oyunun {single_round} tanesi tek geçişte bitiyor; yalnız Robotun Bataryası (3 tur), Karışık Vagonlar ve Buzul Penguenleri (2 tur) çok turlu. {trace_n} rakam çizme oyununun hiçbirinde seslendirme tanımı yok: rakamın adı ve yazım yönü sesli söylenmiyor, okuma öncesi dönemdeki çocuk yalnız yazılı yönergeye bırakılıyor. Motorun güçlü yanı da kayda geçmeli: yazım YÖNÜ doğru biçimde zorunlu tutuluyor, çocuk rakamı ters yönde çizemiyor."],
    PALE_PURPLE, PURPLE)]
story += [PageBreak()]

story += [P("Bütün sayma oyunlarında ortak uygulama standardı", h1)]
rows = [
    [P("Rakam biçimi", box_title), P("Kılavuz yol ve tamamlanan iz eğrisel çizilmeli (Bezier/spline); 0, 2, 3, 5, 6, 8, 9 rakamlarında hiçbir köşe görünmemeli. 1, 4 ve 7 düz kalmalı.", small)],
    [P("Yazım yönü", box_title), P("Mevcut sıralı kontrol noktası yapısı korunmalı - yönü zorunlu tutması bu motorun en değerli yanıdır. Ters yönde çizim kabul edilmemeli.", small)],
    [P("Sahne", box_title), P("cfg.scene motor tarafından okunmalı ve başlıktaki mekân/karakter gerçekten çizilmeli; bitiş ödülü ekranda görünen bir olaya bağlanmalı.", small)],
    [P("Cevap sızdırmama", box_title), P("Yazılacak sayı ekranda yazılı görünmemeli; yalnız sesli söylenmeli ve tekrar dinlenebilmeli. Hayalet şablon kademeli kalkmalı.", small)],
    [P("Ceza", box_title), P("Yoldan sapma can kaybettirmemeli; ekran sarsıntısı ve kırmızı flaş kaldırılmalı. Yerine kılavuz yeniden gösterilmeli ve çocuk aynı noktadan devam etmeli.", small)],
    [P("Ses", box_title), P("Her oyunda rakamın adı ve yazım yönü seslendirilmeli; yönergeyi tekrar okutan bir düğme bulunmalı.", small)],
    [P("Tur", box_title), P("Her oyun en az üç kademeli tur içermeli: kılavuzlu, soluk kılavuzlu, kılavuzsuz. Sayı oyunlarında sayılar her açılışta değişmeli.", small)],
    [P("Sayı-miktar", box_title), P("Rakam yazıldıktan sonra o kadar nesne sayılarak sayı ile miktar eşleştirilmeli; iki basamaklı sayılarda 10'luk demet ve birlikler gösterilmeli.", small)],
]
standards = Table(rows, colWidths=[28 * mm, 148 * mm])
standards.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8D4E2")), ("BACKGROUND", (0, 0), (0, -1), PALE_PURPLE),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
story += [standards, Spacer(1, 4 * mm)]
story += bullets([
    "Süre ve hız yalnız isteğe bağlı rozet olarak sunulacak; doğruluk ve biçim puanına karışmayacak.",
    "Dokunma alanları en az 44 px olacak; BAŞLA topu ve kontrol noktaları küçük parmaklar için yeterli büyüklükte kalacak.",
    "Ses, yazı, görsel ve bitiş ödülü birebir tutarlı olacak; web ile APK aynı davranacak.",
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
        theme_table = Table([[P(f"Bölüm {group_index + 1}", badge), P(clean(last_group), theme_title)]], colWidths=[30 * mm, 146 * mm], rowHeights=[47 * mm])
        theme_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), accent), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                         ("ALIGN", (0, 0), (0, 0), "CENTER"), ("LEFTPADDING", (1, 0), (1, 0), 12),
                                         ("RIGHTPADDING", (1, 0), (1, 0), 12), ("ROUNDEDCORNERS", [10])]))
        story += [Spacer(1, 20 * mm), theme_table, Spacer(1, 8 * mm), P(f"Bu bölümde {count} oyun var. Ana düzeltme odağı", h2)]
        story += bullets(GROUP_FOCUS[last_group])
        story += [Spacer(1, 5 * mm), box("Bölüm kabul eşiği", ["Bu bölümdeki her oyun üç kademeli tur, doğru rakam biçimi ve seslendirme olmadan tamamlanmış sayılmayacak.", "Başlık, görünen sahne, seslendirme, çizim ve bitiş ödülü aynı hikâyeyi anlatacak."], PALE_TEAL, TEAL), PageBreak()]

    scene, level2, level3 = DESIGNS[game["id"]]
    is_trace = game["type"] == "numberTrace"
    observed = current_state(game)
    risk = risks(game)
    new_play = [scene, level2, level3,
                "Rakamın adı ve yazım yönü her turda sesli söylensin; yönergeyi tekrar dinleten bir düğme bulunsun.",
                "Başarı kaydına yalnız 'bitirdi' değil; hangi turda kılavuzsuz yazabildiği, kaç kez yoldan saptığı ve biçimin ne kadar düzgün olduğu eklensin."]
    rounds = [
        "Kılavuzlu: kesikli yol, BAŞLA topu ve sıralı noktalar görünür; sapma ceza üretmez, rakam adı sesli söylenir.",
        level2,
        level3,
    ]
    feedback = (FEEDBACK_TRACE if is_trace else FEEDBACK_WRITE) + [
        "Bitiş ekranı üç turdaki biçim düzgünlüğünü, kılavuzsuz yazabilme durumunu ve sayı-miktar eşleştirmesini ayrı göstermeli.",
    ]
    acceptance = (ACCEPT_TRACE if is_trace else ACCEPT_WRITE) + [
        f"Başlıktaki sahne ve eylem gerçekten uygulanacak: {scene}",
    ]

    accent = accent_cycle[(number - 1) % len(accent_cycle)]
    story += [header(number, game["title"], f"{game['id']} · {game['sub']} · {clean(game['kaz'])}", accent), Spacer(1, 1.8 * mm)]
    story += [box("Denemede görülen mevcut durum", observed, PALE_CORAL, CORAL), Spacer(1, 0.8 * mm)]
    story += [box("Eğitimsel risk", risk, PALE_GOLD, GOLD), Spacer(1, 0.7 * mm)]
    story += [P("Yeni sahne ve oynanış", h2)] + bullets(new_play, bullet_small)
    story += [P("Üç kademeli tur", h2), rounds_table(rounds), Spacer(1, 0.7 * mm)]
    story += [box("Geri bildirim ve bitiş", feedback, PALE_TEAL, TEAL), Spacer(1, 0.7 * mm)]
    story += [box("Kabul ölçütü", acceptance, PALE_BLUE, BLUE), PageBreak()]

story += [P("Son kabul kontrolü", h1), P("Sayma dersi tamamlanmadan önce", h2)]
story += bullets([
    "s0-s10 ve n1-n9 arasındaki 20 oyun üç kademeli turla baştan sona test edilir; görünen başlık, sahne, ses, çizim biçimi ve bitiş ödülü kayıt altına alınır.",
    "0, 2, 3, 5, 6, 8 ve 9 rakamları eğrisel çizilir; hiçbirinde köşe görünmez. 1, 4 ve 7 düz kalır.",
    "cfg.scene motor tarafından okunur; 20 sahnenin tamamı çizilir ve bitiş metni ekranda görünen bir olaya bağlanır.",
    "n1-n9 oyunlarında hedef sayı ekranda yazılı görünmez; yalnız sesli söylenir ve hayalet şablon en geç ikinci turda kalkar.",
    "Yoldan sapma can kaybettirmez; ekran sarsıntısı ve kırmızı flaş kaldırılır. Sihirli Daktilo'daki geri sayım isteğe bağlı rozete dönüşür.",
    "Her rakam çizme oyununda rakamın adı ve yazım yönü seslendirilir; yönergeyi tekrar okutan düğme bulunur.",
    "Her oyunda rakam yazıldıktan sonra o kadar nesne sayılarak sayı-miktar bağı kurulur; iki basamaklı sayılarda 10'luk demet ve birlikler gösterilir.",
    "Yazım yönünü zorunlu tutan mevcut kontrol noktası yapısı korunur - bu motorun doğru çalışan yanıdır ve bozulmamalıdır.",
])
story += [Spacer(1, 4 * mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 1. sınıf sayma dersindeki s0-s10 ve n1-n9 oyunlarını kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, rakam biçimi, ses, mekanik, üç tur, geri bildirim ve test gereksinimlerini ayrıntılı biçimde tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)

reader = PdfReader(str(OUT))
print({"pages": len(reader.pages), "games": len(games), "trace": trace_n, "write": write_n,
       "curvedBroken": curved_n, "singleRound": single_round, "bytes": OUT.stat().st_size, "output": str(OUT)})
