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
OUT = ROOT / "output/pdf/2_sinif_hayat_bilgisi_oyunlari_detayli_duzeltmeler.pdf"
GAMES_JSON = ROOT / "tmp/pdfs/hayatbilgisi2_games.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

games = json.loads(GAMES_JSON.read_text(encoding="utf-8"))
assert len(games) == 36

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
    canv.drawString(MX, 8.2 * mm, "2. Sınıf Hayat Bilgisi - Ayrıntılı Oyun Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 8.2 * mm, str(canv.getPageNumber()))
    canv.restoreState()


ENGINE = {
    "beltSort": ("bant (yürüyen bant) motoru",
        "Başlıktaki okul bahçesi, sağlık merkezi, hava istasyonu veya müze yerine karanlık fabrika bandı açılıyor. "
        "Denemede (Hava Olayı Bandı) karar verilecek kart bandın sol kenarında tamamen kırpıldı - “Çiçeklerin açması” ifadesinden yalnız “...ması” görünüyordu. "
        "Dört kutulu turda kutu etiketleri kutu içine sığmıyor ve her kutunun üzerindeki emoji cevabı görsel olarak ele veriyor."),
    "serveOrder": ("tepsi-servis motoru",
        "Başlıktaki pano, atölye, çanta veya rehberlik masası yerine ahşap servis tezgâhı açılıyor. "
        "Denemede (Güçlü Yönler Panosu) kartların üzerinde doğrudan “GÜÇLÜ:”, “GELİŞİM:”, “PLAN:” etiketleri yazılıydı; "
        "öğretmen “güçlü olduğun alanları ekle” derken hangi kartın güçlü olduğu kartın kendisinde yazıyordu."),
    "catchDrop": ("radar/kapsül yakalama motoru",
        "Seçenekler kapsül içinde tek tek yukarıdan düşüyor; ipucu “Kapsülün altındaki sarı noktayı çanağın ortasına getir” diliyle veriliyor "
        "ve karar süresi düşme hızına bağlanıyor. Üç ayrı oyunun yönergesi birbirinin aynı: “Radarı sürükleyerek doğru cevabı yakala”."),
    "sentenceBuild": ("matbaa/baskı kızağı motoru",
        "Kelime kartlarından büyük harfle başlayan kart ilk sözcüğü, nokta kartı son konumu ele veriyor; makine yalnız tek sabit dizilişi kabul ediyor."),
    "orderSequence": ("roket-yakıt motoru",
        "Karar adımları, acil çağrı basamakları, Atatürk'ün öğrencilik yılları ve teknoloji tarihi gibi tamamen dünyevi konularda bile "
        "kartlar uzayda süzülüyor ve seçilenler YAKIT hunisine gidiyor; kenardaki kartlar ekrandan taşabiliyor."),
    "memoryPairs": ("hafıza kartı motoru",
        "Sahne başlıktan bağımsız yıldızlı uzay; kartlar tavandan iniyor ve “Başla! Kartları çevir” yazısı üst kart sırasının üzerine biniyor. "
        "Can göstergesi 6 kalp ile genel 3 can standardından ayrılıyor."),
    "dragMatch": ("eşleştirme köprüsü motoru",
        "Köprü görseli yok; hedef satırların solunda boş kareler, altta PARÇALAR havuzu var. "
        "Denemede (Trafik İşareti Köprüsü) hem parça hem hedef aynı anlamı gösteren emojiyle işaretliydi ve parça yazıları çipten taşıp kesildi."),
    "dragSlider": ("tren-tünel motoru",
        "Kişisel alan mesafesi ya da israf miktarı sorulurken sahnede kırmızı bir tren dört tünelden birine giriyor ve sayaç “0/4 tren” yazıyor. "
        "Tünel etiketleri (çok yakın / yakın / uzak / çok uzak) soyut sözcükler; ölçülen şeyin kendisi ekranda hiç görünmüyor."),
    "numPad": ("radar-kod (tuş takımı) motoru",
        "Sayısal tuş takımı ve boş bir ekran çerçevesi var; telefon, ahize veya çağrı ekranı görseli yok. "
        "Denemede alt başlıkta doğrudan “112'yi tuşla” yazılıydı - yani cevap oyunun başlığında veriliyordu."),
    "tallyChart": ("çetele motoru",
        "Arkadaş balonundaki cümle sütun adını birebir içeriyor; sütun altlarında çetele çizgisi yerine rakam sayacı artıyor."),
    "surveyChart": ("çetele motoru (anket sürümü)",
        "Sahne “ÇETELE TABLOSU” başlığıyla açılıyor ama oyun bir oylama; gelen oy balonu sütun başlığıyla birebir aynı olduğu için "
        "hiçbir çıkarım gerekmiyor ve sütunlarda çetele çizgisi yerine rakam artıyor."),
    "codeGrid": ("kargo/robot ızgara motoru",
        "Izgara, engel ve hedef okunaklı. Ancak yön blokları yalnız yukarı/aşağı/sol/sağ oklarından oluşuyor - yani ekran yönleri; "
        "kuzey, güney, doğu, batı adları hiçbir yerde geçmiyor ve ekranda güneş, gölge, yosun gibi tek bir doğal yön işareti yok."),
    "holdFill": ("kronometre motoru",
        "Başlıkta musluk yazıyor ama ekranın ortasında büyük bir KRONOMETRE duruyor; lavabo, musluk, bardak veya diş fırçası görseli yok. "
        "Denemede görev metni (“Diş fırçalamak için 1 bardak su yeter!”), “Hedef 1 bardak” satırı ve ölçek üzerindeki sarı çizgi "
        "cevabı üç ayrı yerde veriyordu."),
}

TYPE_RISK = {
    "beltSort": "Bant hızı okuma ve karar süresine karışıyor; kenarda kırpılan kart hiç okunamadan can etkiliyor. Kutulardaki emoji ipuçları davranışı değerlendirmeden görsel eşleştirmeyle sonuca gitmeyi mümkün kılıyor.",
    "serveOrder": "Kartın üzerinde kategorisi yazılı olduğunda öğrenci içeriği hiç değerlendirmeden etiket kopyalayabilir; kişisel değerlendirme gerektiren kazanımlar hazır kart seçmeye iner.",
    "catchDrop": "Doğru cevabı bilmek yetmiyor; düşen kapsüle yetişmek gerekiyor. Yanlış motor hareketi yanlış hayat bilgisi kararı gibi can kaybettiriyor.",
    "sentenceBuild": "Büyük harfli kart ve nokta kartı dizilişi ele veriyor; ayrıca duyguyu ya da aile görüşünü kendi sözcükleriyle ifade etme kazanımı hazır kartları sıralamaya indirgeniyor.",
    "orderSequence": "Roket-yakıt sahnesi konuyla çelişip kavramı bulanıklaştırıyor; kartlardaki tarih veya numara ipuçları içerik bilgisi olmadan sıralamayı mümkün kılıyor.",
    "memoryPairs": "Eşleştirme, kavramı açıklamadan kart konumunu ezberleyerek de çözülür; görsel hafıza başarısı hayat bilgisi başarısı gibi kayda geçer.",
    "dragMatch": "Emoji eşleşmesi cevabı doğrudan verdiği için trafik levhası, yönetim birimi veya bilim insanı bilgisi hiç kullanılmadan oyun bitirilebilir; taşan yazılar okunamadığından eşleştirme gerekçesiz kalır.",
    "dragSlider": "Ölçülen kavram (mesafe, israf) ekranda hiç görünmüyor; öğrenci soyut bir sözcüğü tren tüneliyle eşleştiriyor. Kişisel alan gibi koruyucu bir konu, bedensel sınır deneyimi kurulmadan sözcük seçimine iniyor.",
    "numPad": "Aranacak numara oyunun alt başlığında yazılı olduğu için hatırlama hiç yoklanmıyor; ayrıca dört turun dördünde de cevap aynı olduğundan ilk turdan sonra düşünmeye gerek kalmıyor.",
    "tallyChart": "Cümledeki sözcük sütun adıyla birebir aynı olduğundan görev sözcük kopyalamaya iner; rakam sayacı çetele kuralını (beşinci çizgi dördü keser) hiç göstermez.",
    "surveyChart": "Oy ile sütun adı aynı olduğu için veri toplama mekanik tıklamaya iner; öğrenci sonucu yorumlamadan, çoğunluk ve azınlık ilişkisini kurmadan oyunu bitirebilir.",
    "codeGrid": "Kazanım doğadan yararlanarak YÖN belirlemeyi istiyor; oyun ise ekran yönleriyle (yukarı/sağ) labirent çözdürüyor. Güneş ekranda olmadığı için yönergedeki “güneş doğudan doğar” bilgisi hiçbir yerde kullanılmıyor - kazanım ile mekanik tamamen kopuk.",
    "holdFill": "Görev metni gereken miktarı doğrudan söylediği için tasarruf kararı öğrenciye bırakılmıyor; oyun bir zamanlama-refleks alıştırmasına dönüşüyor ve suyun nereye aktığı hiç görünmüyor.",
}

TYPE_FEEDBACK = {
    "beltSort": "Yanlış kutuda bant dursun; kart sabitlenip yeniden okunsun ve ölçüt doğru söylenmeden hatırlatılsın. Kenarda kırpılan kart hiç puanlanmasın.",
    "serveOrder": "Yanlış kartta tepsi kilitlenmesin; istek yeniden okunsun ve kartın neden uymadığı içerik üzerinden gösterilsin, etiket üzerinden değil.",
    "catchDrop": "Yanlış yakalamada düşme dursun; seçenek sabitlenip yeniden karar verilsin. Kaçan kapsül can yakmasın, yalnız yeniden denensin.",
    "sentenceBuild": "Yanlışta bütün dizi bozulmasın; yalnız son kart geri alınsın. Anlamlı alternatif diziliş kurulduysa doğru kabul edilsin.",
    "orderSequence": "Yanlış adımda dizi silinmesin; yalnız son seçim geri alınsın ve “önce ne olmalı?” sorusunu düşündüren ipucu verilsin.",
    "memoryPairs": "Yanlış çiftte kartlar hemen kapanmasın; iki içerik yan yana sesli okunup farkı soran kısa bir ipucu verilsin. Can standardı diğer oyunlarla eşitlensin.",
    "dragMatch": "Yanlış parça başlangıca dönsün; hedef parlatılmasın. Eşleşmenin dayandığı bilgi kısa bir soruyla vurgulansın.",
    "dragSlider": "Yanlış seçimde doğru değer tek başına verilmesin; iki figür arasındaki mesafe ya da akan su miktarı görsel olarak canlandırılıp yeniden karar verilsin.",
    "numPad": "Yanlış numarada doğru numara ekrana yazılmasın; “Bu numara itfaiyeye ulaşmaz” gibi sonucu gösteren bir geri bildirim verilip yeniden denensin.",
    "tallyChart": "Yanlış satırda cevap cümlesi yeniden dinletilsin; görev ile cümledeki ipucu arasındaki ilişki soruyla kurulsun, doğru satır parlatılmasın.",
    "surveyChart": "Yanlış işaretlemede oy yeniden dinletilsin; sayım bitince sonuç doğrudan açıklanmasın, öğrenciye “en çok/en az hangisi, kaç fark var?” soruları sorulsun.",
    "codeGrid": "Engele çarpınca robot dursun ve programdaki hatalı adım işaretlensin; tüm program silinmesin. Yanlış yönde ilerlerken güneşin konumu hatırlatılsın.",
    "holdFill": "Fazla su akıtıldığında ceza verilmesin; taşan su görünür olsun ve “ne kadarı boşa gitti?” sorusu sorulsun.",
}

TYPE_ACCEPT = {
    "beltSort": "İlk iki turda kartlar sabit gelecek; hız ancak üçüncü turda isteğe bağlı açılacak. Kart hiçbir konumda kırpılmayacak, kutu etiketi kutu içinde kalacak, kutu emojileri cevabı vermeyecek ve dokunma alanı en az 44 px olacak.",
    "serveOrder": "Kartlarda kategori etiketi (GÜÇLÜ:, GELİŞİM:, PLAN:) yazmayacak; yalnız içerik görünecek ve her istek farklı içerik havuzu kullanacak.",
    "catchDrop": "İlk turda düşme kapalı, seçenekler sabit olacak; başarı doğru karar ve gerekçeyle ölçülecek, yakalama refleksi puana karışmayacak. Her oyunun yönergesi kendi konusunu anlatacak.",
    "sentenceBuild": "Kartlar küçük harfle gelecek; baş harf ve son işaret öğrencinin kararı olacak. Son turda serbest yazı ya da sözlü ifade alanı bulunacak.",
    "orderSequence": "Roket-yakıt sahnesi kaldırılacak; sırayı ele veren tarih/numara ilk turda gizlenecek ve kartlar 390x844 ekranda tam içeride kalacak.",
    "memoryPairs": "Kart konumları ve içerik her açılışta karışacak; can sayısı genel standartla (3) eşitlenecek ve her eşleşme bir gerekçe adımıyla doğrulanacak.",
    "dragMatch": "Parça ve hedefteki emojiler cevabı eşleştirmeyecek; trafik oyununda gerçek levha görselleri kullanılacak, yazılar çipe sığacak ve hedef alanlar en az 44 px olacak.",
    "dragSlider": "Tren-tünel sahnesi kaldırılacak; ölçülen kavram (iki kişi arasındaki mesafe, akan su) ekranda görsel olarak canlandırılacak ve karar bu görsele dayanacak.",
    "numPad": "Aranacak numara başlıkta, alt başlıkta veya yönergede yazılı olmayacak; turlar arasında senaryo değişecek ve öğrenci numarayı hatırlayarak tuşlayacak.",
    "tallyChart": "Cevap cümleleri görev adını birebir söylemeyecek; işaretler çetele çizgisiyle birikecek, beşinci çizgi dördünü kesecek ve bitişte tablo yorum sorusu sorulacak.",
    "surveyChart": "Oy ifadeleri sütun adını birebir tekrar etmeyecek; sayım çetele çizgisiyle görünecek ve oyun ancak sonuç yorumu yapıldıktan sonra tamamlanacak.",
    "codeGrid": "Yön blokları KUZEY/GÜNEY/DOĞU/BATI olarak adlandırılacak; ekranda güneşin konumu (sabah/akşam) görünecek ve rota ancak bu bilgi kullanılarak çözülebilecek.",
    "holdFill": "Görev metni gereken miktarı söylemeyecek; öğrenci işin ne olduğuna bakarak kendisi karar verecek. Ekranda gerçek musluk, kap ve akan su bulunacak.",
}


DESIGNS = {
"h01": ("Gerçek bir okul bahçesi çizilsin: davranış iki çocuk arasında kısa bir sahne olarak canlansın, kart bantta akmasın ve hiçbir kenarda kırpılmasın.",
        "Duruma göre değişen davranışlar eklensin (şaka mı alay mı?); öğrenci ölçütü seçerek savunsun.",
        "Öğrenci arkadaşlığı güçlendiren kendi davranışını söylesin veya yazsın ve nedenini belirtsin."),
"h02": ("Gerçek bir sınıf panosu çizilsin; kartlarda “GÜÇLÜ:”, “GELİŞİM:”, “PLAN:” etiketleri KALDIRILSIN, yalnız içerik yazsın. Öğrenci hangi kartın hangi kategoriye girdiğine kendisi karar versin.",
        "Aynı beceri hem güçlü hem gelişime açık olabilecek biçimde sunulsun; öğrenci kendi durumuna göre seçsin.",
        "Öğrenci kendi güçlü yanını ve geliştirmek istediği bir alanı kendi cümlesiyle yazsın, sonra bunun için bir adım planlasın."),
"h03": ("Gerçek bir sınıf ortamı çizilsin: öğretmen anlatırken öğrencilerin duruşu, göz teması ve söz alma davranışı sahnede görünsün; kapsül-radar dili kaldırılsın.",
        "İyi görünen ama dinlemeyi engelleyen davranışlar çeldirici olsun (sessizce başka şeye bakmak).",
        "Öğrenci kısa bir dinleme denemesi yapıp duyduğunu kendi sözleriyle anlatsın."),
"h04": ("Gerçek bir sınıf durumu canlansın (sıra kapıldı, oyuna alınmadı); öğrenci duygusunu “Ben ... hissettim çünkü ...” kalıbıyla kursun ve kurulan cümle sahnedeki karaktere söylensin.",
        "Aynı duygunun kırıcı ve nazik iki ifadesi karşılaştırılsın.",
        "Öğrenci kendi yaşadığı bir durumu anlatan cümleyi hazır kart olmadan kendisi yazsın veya söylesin."),
"h05": ("Gerçek bir sınıf oylaması sahnesi kurulsun: kürsü, öneri panosu ve el kaldıran öğrenciler görünsün. Oy ifadesi sütun adını birebir tekrar etmesin ve sayım çetele çizgisiyle görünsün.",
        "Berabere biten ve tek oyla kazanılan senaryolar eklensin; çoğunluk kavramı somutlaştırılsın.",
        "Öğrenci sonucu yorumlasın ve azınlıkta kalanların görüşüne ne olacağını bir cümleyle belirtsin."),
"h06": ("Karar adımları gerçek sınıf sürecinde görselleşsin (sorun söylenir, öneriler alınır, tartışılır, oylanır, uygulanır); roket-yakıt sahnesi kaldırılsın.",
        "Atlanan adımın sonucu gösterilsin: tartışmasız oylama neden sorunlu?",
        "Öğrenci sınıfında çözülecek bir sorun için adımları sırayla söylesin."),
"h07": ("Gerçek bir gün akışı çizilsin (kahvaltı, oyun, ekran, uyku); alışkanlık kartı bu akışın içinde bir an olarak görünsün ve bant durdurulsun.",
        "Miktara göre değişen alışkanlıklar eklensin (biraz ekran / çok ekran); ölçüt tartışılsın.",
        "Öğrenci kendi günündeki bir alışkanlığı değerlendirip iyileştirme önerisi söylesin."),
"h08": ("Tren-tünel sahnesi KALDIRILSIN. Ekranda iki insan figürü olsun ve öğrenci aralarındaki mesafeyi doğrudan sürükleyerek ayarlasın; seçilen mesafe görsel olarak canlansın. Bu konu koruyucu bir kazanımdır, somut bedensel sınır deneyimi gerektirir.",
        "Tanıdık-yabancı, oyun-sıra bekleme gibi durumlar karşılaştırılsın; mesafenin duruma göre değiştiği gösterilsin.",
        "Öğrenci rahatsız olduğunda ne söyleyeceğini (“Lütfen biraz uzaklaşır mısın?”) uygulasın ve kime haber vereceğini belirtsin."),
"h09": ("GERÇEK trafik levhası görselleri kullanılsın - kazanım levhayı TANIMAYI istiyor, yazıyı okumayı değil. Parça ve hedefteki emoji eşleşmesi kaldırılsın; karar levhanın biçim ve rengine dayansın.",
        "Benzer görünen levhalar çeldirici olsun (yaya geçidi / okul geçidi); ayırt edici ayrıntı işaretlensin.",
        "Öğrenci bir sokak sahnesinde levhaya göre nasıl davranacağını uygulasın."),
"h10": ("Gerçek bir telefon ekranı ve ahize çizilsin. KRİTİK: alt başlıktaki “112'yi tuşla” ifadesi kaldırılsın - numara oyunun adında yazılıyken hatırlama ölçülemez.",
        "Farklı acil senaryolar verilsin (yangın, kaza, hastalık); numaranın hepsinde aynı olduğu sonucu öğrenci tarafından çıkarılsın.",
        "Öğrenci numarayı tuşladıktan sonra görevliye söyleyeceği bilgileri (ad, adres, olay) sırayla söylesin."),
"h11": ("Gerçek bir çağrı ekranı ve görevli sesi olsun; adımlar konuşma balonları hâlinde sıralansın ve roket sahnesi kaldırılsın.",
        "Eksik veya yanlış sıralı bir çağrı dinletilsin; öğrenci hatayı bulsun.",
        "Öğrenci kurgusal bir acil durumu baştan sona bildirsin; adres ve olay bilgisi kaydedilsin."),
"h12": ("Gerçek bir afet çantası ve ev sahnesi çizilsin; seçilen malzeme çantaya gerçekten girsin ve çantanın ağırlığı/doluluğu görünsün.",
        "Gerekli ama akla gelmeyen malzemeler (düdük, ilaç, fotokopi kimlik) ile gereksiz cazip nesneler karşılaştırılsın.",
        "Öğrenci kendi çantası için üç malzeme seçip nedenini söylesin."),
"h13": ("Gerçek günlük yaşam sahneleri (otobüs, market, ziyaret) kart arkasında canlansın; eşleşen söz o sahnede sesli söylensin.",
        "Aynı durumda birden çok uygun nezaket sözü olabileceği gösterilsin.",
        "Öğrenci bir durumu canlandırıp uygun sözü kendisi söylesin."),
"h14": ("Gerçek toplumsal ortamlar çizilsin (sıra, sofra, ziyaret); davranış o ortamda kısa sahne olarak görünsün ve bant durdurulsun.",
        "Kültürel bağlama göre değişen durumlar eklensin; ölçüt tartışılsın.",
        "Öğrenci bir görgü kuralını neden uyguladığını açıklasın."),
"h15": ("Gerçek aile sahneleri (hastalıkta bakım, birlikte sofra, destek) canlansın; kurulan cümle aile panosuna asılsın. Kartlar küçük harfle gelsin.",
        "Ailenin farklı işlevleri (sevgi, güven, paylaşım) ayrı örneklerle karşılaştırılsın.",
        "Öğrenci kendi ailesinden bir örneği kendi cümlesiyle anlatsın."),
"h16": ("Gerçek ev ve sınıf ortamı çizilsin; görev kartı o ortamda yapılacak iş olarak görünsün ve seçilen görev yerine getirilince sahne değişsin.",
        "Yaşa uygun olan ve olmayan sorumluluklar ayrılsın; öğrenci hangisinin kendi görevi olduğuna karar versin.",
        "Öğrenci bu hafta üstleneceği bir sorumluluğu seçip söylesin."),
"h17": ("“Radarı sürükleyerek doğru cevabı yakala” genel yönergesi kaldırılsın; soru ailenin işlevine dair somut bir sahneye bağlansın ve seçenekler sabit dursun.",
        "Ailenin farklı işlevleri karşılaştırılsın; yalnız maddi destek değil duygusal destek de vurgulansın.",
        "Öğrenci ailesinin kendisine nasıl destek olduğunu bir örnekle anlatsın."),
"h18": ("Gerçek sınıf görev panosu çizilsin; cevap cümleleri görev adını birebir söylemesin ve işaretler çetele çizgisiyle biriksin.",
        "Çetele tamamlanınca sıklık tablosuna çevrilsin; “en çok/en az hangi görev” sorusu sorulsun.",
        "Öğrenci kendi görevini ekleyip sonucu yorumlasın."),
"h19": ("Gerçek şehir haritası ve mekân fotoğrafları kullanılsın; ziyaretçinin isteği mekânın özelliğinden çıkarım gerektirsin ve etiket kopyası kaldırılsın.",
        "Tarihî mekân ile doğal güzellik ayrımı yapılsın; benzer iki mekân karşılaştırılsın.",
        "Öğrenci kendi çevresinden bir yeri iki cümleyle tanıtsın."),
"h20": ("Genel “doğru cevabı yakala” yönergesi kaldırılsın; soru gerçek mekân görselleri üzerinden sorulsun ve seçenekler sabit dursun.",
        "Aynı mekânın farklı özellikleri (yaşı, yapısı, kullanımı) ayrı sorularla incelensin.",
        "Öğrenci bir mekânın özelliğini kendi sözleriyle ifade etsin."),
"h21": ("Gerçek bir şehir sahnesi çizilsin: belediye, muhtarlık, valilik binaları görünsün ve eşleşme binanın işleviyle kurulsun. Emoji eşleşmesi kaldırılsın.",
        "Hangi işin hangi birime ait olduğu günlük örneklerle çalışılsın (çöp, nüfus kaydı, park).",
        "Öğrenci bir sorunu hangi birime iletmesi gerektiğini gerekçesiyle söylesin."),
"h22": ("Gerçek dönem görselleri ve okul sahneleri kullanılsın; roket kaldırılsın. İlk turda tarihler gizlensin, sıralama olay içeriğinden yapılsın.",
        "Atatürk'ün öğrencilik özellikleriyle öğrencinin kendi okul yaşamı karşılaştırılsın.",
        "Öğrenci en çok etkilendiği anıyı kendi cümlesiyle anlatsın."),
"h23": ("Gerçek bayram sahneleri (tören, ziyaret, ikram) kart arkasında canlansın; eşleşen bayramın anlamı kısa bir görselle gösterilsin.",
        "Millî ve dinî bayramların anlam farkı örneklerle karşılaştırılsın.",
        "Öğrenci bir bayramın neden kutlandığını kendi sözleriyle anlatsın."),
"h24": ("Gerçek bayram görselleri ve takvim kullanılsın; kart bantta akmasın ve millî/dinî ayrımı görsel kanıtla (tören mi, aile ziyareti mi) kurulsun.",
        "Aynı tarihte olan farklı kutlamalar ayrılsın; ölçüt tartışılsın.",
        "Öğrenci bir bayramı hangi gruba neden koyduğunu açıklasın."),
"h25": ("Gerçek mevsim manzaraları kart arkasında açılsın; eşleşen mevsimin özelliği kısa animasyonla gösterilsin (yaprak dökümü, kar yağışı).",
        "Aynı hava olayının farklı mevsimlerde görülebildiği durumlar eklensin.",
        "Öğrenci bulunduğu mevsimin özelliklerini gözleyip söylesin."),
"h26": ("Gerçek bir hava istasyonu ve mevsim panosu çizilsin. KRİTİK: kart hiçbir kenarda kırpılmasın - denemede “Çiçeklerin açması” ifadesinin yalnız son hecesi görünüyordu. Kutulardaki mevsim emojileri cevabı vermesin.",
        "Birden çok mevsimde görülebilen hava olayları eklensin; öğrenci “en çok” ölçütünü savunsun.",
        "Öğrenci yaşadığı yerin mevsim özelliklerini gözleme dayanarak anlatsın."),
"h27": ("KRİTİK: Yön blokları yukarı/aşağı/sol/sağ okları yerine KUZEY / GÜNEY / DOĞU / BATI olsun ve ekranda güneşin konumu (sabah doğuda, akşam batıda) görünsün. Rota ancak güneşe bakarak çözülebilsin; şu anki hâlinde kazanım ile mekanik tamamen kopuk.",
        "Sabah ve akşam senaryoları verilsin; aynı hedef için yön kararı değişsin.",
        "Öğrenci gölgeye veya güneşe bakarak bulunduğu yerde bir yönü söylesin."),
"h28": ("Gerçek bir ev ve afet hazırlığı sahnesi çizilsin; her adım evde yapılan somut bir işe dönüşsün (dolabı sabitle, çantayı hazırla, buluşma yeri belirle).",
        "Deprem, yangın ve sel için farklı önlem sıraları karşılaştırılsın.",
        "Öğrenci ailesiyle yapacağı üç hazırlığı sırayla söylesin."),
"h29": ("KRONOMETRE kaldırılsın; ekranda gerçek musluk, lavabo, bardak ve diş fırçası olsun, akan su görünsün. KRİTİK: görev metni (“1 bardak su yeter”), “Hedef 1 bardak” satırı ve ölçekteki sarı çizgi cevabı üç yerde veriyor - hepsi kaldırılsın, öğrenci işe bakarak kendisi karar versin.",
        "Farklı işler için gereken su karşılaştırılsın (diş fırçalama, bulaşık, çiçek sulama).",
        "Öğrenci taşan suyu görsün ve günlük yaşamında bir tasarruf önerisi söylesin."),
"h30": ("Tren-tünel sahnesi kaldırılsın; ekranda akan musluk ve dolan kova gibi somut bir israf görseli olsun ve tahmin bu görsele dayansın.",
        "Tahmin, gerçek değer ve fark birlikte gösterilsin; iki kullanım karşılaştırılsın.",
        "Öğrenci israfı azaltmak için bir davranış değişikliği önersin."),
"h31": ("Gerçek bir bilim müzesi sahnesi çizilsin; her bilim insanının katkısı kısa bir görselle (ampul yanar, mikrop büyür) gösterilsin ve emoji eşleşmesi kaldırılsın.",
        "Katkının günlük yaşamdaki karşılığı sorulsun: bu buluş olmasaydı ne olurdu?",
        "Öğrenci bir bilim insanının katkısını kendi cümlesiyle anlatsın."),
"h32": ("Gerçek teknoloji müzesi vitrini çizilsin; ürünler raf üzerinde sıralansın ve roket kaldırılsın. İlk turda tarihler gizlensin, sıralama ürünün biçiminden yapılsın.",
        "Farklı ürün aileleri karşılaştırılsın (telefon, aydınlatma, ulaşım).",
        "Öğrenci bir ürünün nasıl değiştiğini üç aşamada anlatsın."),
"h33": ("Gerçek müze vitrini ve günümüz rafı yan yana çizilsin; ürün kartı bu iki alandan birine yerleşsin ve bant durdurulsun.",
        "Eski-yeni ayrımının yanında benzerlik de sorulsun: ikisi de ne işe yarıyor?",
        "Öğrenci bir ürünün eski ve yeni hâlini karşılaştırıp farkı söylesin."),
"h34": ("Gerçek günlük yaşam sahneleri çizilsin (duvar resmi, sokak müziği, tiyatro afişi); eşleşen sanat dalı o sahnede canlansın.",
        "Aynı sanat dalının farklı yerlerde karşımıza çıktığı gösterilsin.",
        "Öğrenci çevresinde gördüğü bir sanat örneğini anlatsın."),
"h35": ("Gerçek bir sanat atölyesi çizilsin; malzeme seçilince sanatçı onu kullanarak bir şey üretsin ve etiket kopyası kaldırılsın.",
        "Birden çok sanat dalında kullanılabilen malzemeler çeldirici olsun.",
        "Öğrenci bir sanat dalını seçip gerekli malzemeleri kendisi sıralasın."),
"h36": ("Genel radar yönergesi kaldırılsın; buluş ve faydası gerçek bir öncesi-sonrası sahnesiyle gösterilsin (buzdolabından önce yiyecek nasıl saklanırdı?).",
        "Aynı buluşun birden çok faydası ve bir olumsuz yanı karşılaştırılsın.",
        "Öğrenci bir buluşun hayatını nasıl kolaylaştırdığını örnekle anlatsın."),
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
        return f"Kaynakta {n.get('customers','?')} istek tanımlı; kart havuzu ve etiketler sabit."
    if t == "dragSlider":
        return f"Kaynakta {n.get('rounds','?')} tahmin turu var; dört sabit sözcük seçeneğinden biri seçiliyor ve ölçülen kavramın görseli tanımlı değil."
    if t == "sentenceBuild":
        return f"Kaynakta {n.get('rounds','?')} cümle kurulumu var; her cümlenin tek doğru dizilişi tanımlı."
    if t == "orderSequence":
        return f"Kaynakta {n.get('items','?')} kartlık tek sıra var; doğru sıra sabit ve yeni olay turu üretilmiyor."
    if t == "dragMatch":
        return f"Kaynakta {n.get('sources','?')} parça ve {n.get('targets','?')} hedef var; tek sabit eşleştirme turu."
    if t == "codeGrid":
        return f"Kaynakta {n.get('rounds','?')} görev haritası var; program yalnız ekran yönü oklarından oluşuyor ve yön adı geçmiyor."
    if t == "numPad":
        return f"Kaynakta {n.get('rounds','?')} senaryo var; dördünde de doğru cevap aynı numara ve numara oyunun alt başlığında yazılı."
    if t == "holdFill":
        return f"Kaynakta {n.get('rounds','?')} doldurma turu var; hedef miktar görev metninde açıkça söyleniyor."
    if t == "surveyChart":
        return f"Kaynakta {n.get('options','?')} seçenek ve {n.get('responses','?')} oy tanımlı; oy ifadeleri seçenek adını birebir içeriyor ve sonuç yorumu adımı tanımlı değil."
    return f"Kaynakta {n.get('columns','?')} sütun ve {n.get('responses','?')} yanıt tanımlı; yanıt cümleleri sütun adını birebir içeriyor."


GROUP_FOCUS = {
    "Alan 1 · Ben ve Okulum": [
        "Kişisel değerlendirme gerektiren kazanımlarda (güçlü yönler, duygu ifadesi) kartların üzerindeki kategori etiketleri kaldırılmalı; öğrenci kendisi hakkında konuşmalı.",
        "Sınıf bahçesi, pano ve oylama sahneleri gerçek görsellerle kurulmalı; bant ve servis tezgâhı şablonu kaldırılmalı.",
        "Karar alma ve dinleme kazanımları gerçek üretim (söyleme, yazma, uygulama) ile tamamlanmalı.",
    ],
    "Alan 2 · Sağlığım ve Güvenliğim": [
        "Acil numara oyunun başlığında yazılı olmamalı; hatırlama gerçekten yoklanmalı.",
        "Trafik kazanımı gerçek levha görselleriyle çalışmalı - levhayı tanımak yazıyı okumak değildir.",
        "Kişisel alan koruyucu bir kazanımdır: tren-tünel yerine iki figür arasındaki gerçek mesafe deneyimi kurulmalı ve öğrenci ne söyleyeceğini uygulamalı.",
    ],
    "Alan 3 · Ailem ve Toplum": [
        "Aile ve nezaket kazanımları gerçek günlük yaşam sahneleriyle canlandırılmalı; uzay ve bant şablonu kaldırılmalı.",
        "Genel “doğru cevabı yakala” yönergesi her oyunun kendi konusuna göre yeniden yazılmalı.",
        "Sorumluluk kazanımı hazır kart seçmekten çıkıp öğrencinin üstleneceği gerçek bir göreve bağlanmalı.",
    ],
    "Alan 4 · Yaşadığım Yer ve Ülkem": [
        "Mekân, yönetim ve bayram kazanımları gerçek görsel kanıtla (fotoğraf, bina, tören) sunulmalı.",
        "Köprü oyunlarında emoji eşleşmesi kaldırılmalı; karar bilgiye dayanmalı.",
        "Atatürk'ün öğrencilik yılları roket sahnesinden çıkarılıp dönem görselleriyle anlatılmalı.",
    ],
    "Alan 5 · Doğa ve Çevre": [
        "Yön kazanımı ekran yönlerinden (yukarı/sağ) kurtarılıp gerçek yön adlarına ve güneşin konumuna bağlanmalı.",
        "Tasarruf oyunlarında gereken miktar söylenmemeli; öğrenci işe bakarak kendisi karar vermeli ve akan su görünmeli.",
        "Hava olayı bandında kart kırpılması giderilmeli; mevsim emojileri cevabı vermemeli.",
    ],
    "Alan 6 · Bilim, Teknoloji ve Sanat": [
        "Bilim insanı ve teknoloji kazanımları katkının somut sonucunu gösteren sahnelerle desteklenmeli.",
        "Zaman şeridi roket sahnesinden çıkarılıp gerçek müze vitrinine taşınmalı; tarihler ilk turda gizlenmeli.",
        "Sanat kazanımları günlük yaşamdaki gerçek karşılıklarıyla (duvar resmi, sokak müziği) canlandırılmalı.",
    ],
}

GROUP_COLORS = [CORAL, TEAL, PURPLE, GOLD, BLUE, GREEN]

# Kaç oyun ortak "genel yönerge" kullanıyor?
generic_prompt = [g for g in games if "doğru cevabı yakala" in g["instruction"].lower()]
belt_n = sum(1 for g in games if g["type"] == "beltSort")
answer_leak = ["h02", "h09", "h10", "h26", "h29", "h05", "h18"]

doc = BaseDocTemplate(
    str(OUT), pagesize=A4, rightMargin=MX, leftMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
    title="2. Sınıf Hayat Bilgisi Oyunları - Ayrıntılı Düzeltmeler", author="Macera Akademi oyun incelemesi",
)
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

story = [Spacer(1, 14 * mm), P("MACERA AKADEMİ", cover_kicker),
         P("2. Sınıf Hayat Bilgisi Oyunları<br/>Ayrıntılı Düzeltmeler", cover_title),
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
story += [box("1. Yön kazanımı ile oyun mekaniği tamamen kopuk",
    ["Doğadan Yön Bulma oyununun kazanımı “doğadan yararlanarak yön belirler”; yönergesi de “Güneş sabah doğudan doğar, akşam batıdan batar” bilgisini veriyor. Ancak ekranda güneş, gölge veya başka hiçbir doğal yön işareti yok; yön blokları yukarı/aşağı/sol/sağ oklarından oluşuyor - yani ekran yönleri ve kuzey-güney-doğu-batı adları hiçbir yerde geçmiyor. Üstelik görev metni “yukarı ve sağa ilerle” diyerek çözümü doğrudan söylüyor. Oyun bir labirent alıştırmasına dönüşmüş, yön kavramı hiç ölçülmüyor."],
    PALE_CORAL, CORAL), Spacer(1, 1.7 * mm)]
story += [box("2. Cevap ekranın kendisinde yazılı - en az yedi oyunda",
    ["Acil Çağrı Telefonu'nun alt başlığında “112'yi tuşla” yazıyor; numara oyunun adında dururken hatırlama ölçülemez ve dört turun dördünde de cevap aynı. Tasarruf Musluğu'nda gereken miktar üç ayrı yerde veriliyor: görev metni (“Diş fırçalamak için 1 bardak su yeter!”), “Hedef 1 bardak” satırı ve ölçek üzerindeki sarı çizgi. Güçlü Yönler Panosu'nda kartların üzerinde “GÜÇLÜ:”, “GELİŞİM:”, “PLAN:” etiketleri yazılı; öğretmen “güçlü olduğun alanları seç” derken hangisinin güçlü olduğu kartta yazıyor."],
    PALE_GOLD, GOLD), Spacer(1, 1.7 * mm)]
story += [box("3. Emoji eşleşmesi bilgiyi devre dışı bırakıyor",
    ["Trafik İşareti Köprüsü'nde parça ve hedef aynı emojiyle işaretli: okul geçidi levhası ile “Burada çocuklar geçer” aynı simgeyi, yeşil ışık ile “Geçebilirsin” aynı rengi taşıyor. Çocuk levhayı tanımadan simge eşleyerek bitirebiliyor. Daha temel bir sorun da var: kazanım levhayı TANIMAYI istiyor ama ekranda gerçek levha görseli yok, yalnız “DUR levhası” yazısı var. Hava Olayı Bandı'nda da dört kutunun üzerindeki mevsim emojileri (çiçek, güneş, yaprak, kar tanesi) cevabı görsel olarak veriyor."],
    PALE_BLUE, BLUE), Spacer(1, 1.7 * mm)]
story += [box("4. Kişisel alan gibi koruyucu bir kazanım tren oyununa indirgenmiş",
    ["Kişisel Alan Ölçeri'nin kazanımı “kişisel alan sınırlarını korur” - istismardan korunma bağlamında öğretilen bir konu. Ekranda ise kırmızı bir tren dört tünelden birine giriyor, sayaç “0/4 tren” yazıyor ve tünellerin üzerinde “çok yakın / yakın / uzak / çok uzak” soyut sözcükleri duruyor. İki insan arasındaki gerçek mesafe hiç görünmüyor, öğrenci rahatsız olduğunda ne söyleyeceğini uygulamıyor. İsraf Ölçeri de aynı tren motorunu kullanıyor."],
    PALE_TEAL, TEAL), Spacer(1, 1.7 * mm)]
story += [box(f"5. Kart kırpılması, ortak yönerge ve sahne eksikliği; teknik çökme yok",
    [f"Hava Olayı Bandı'nda karar verilecek kart bandın sol kenarında tamamen kırpıldı - “Çiçeklerin açması” ifadesinden yalnız “...ması” görünüyordu; aynı kusur {belt_n} bant oyununun tamamını tehdit ediyor. {len(generic_prompt)} radar oyununun yönergesi birbirinin aynı: “Radarı sürükleyerek doğru cevabı yakala” - oyunun konusu yönergede hiç geçmiyor. Otuz altı oyunun tamamı yüklendi; motorlarda çökme veya konsol hatası oluşmadı. Sorun çalışmama değil, kazanım ile sahne/mekanik arasındaki uyumsuzluk."],
    PALE_PURPLE, PURPLE)]
story += [PageBreak()]

story += [P("Bütün hayat bilgisi oyunlarında ortak uygulama standardı", h1)]
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

story += [P("Son kabul kontrolü", h1), P("2. sınıf hayat bilgisi bölümü tamamlanmadan önce", h2)]
story += bullets([
    "h01-h36 arasındaki 36 oyun üç kademeli turla baştan sona test edilir; görünen başlık, sahne, kontrol, ses ve ölçülen kazanım kayıt altına alınır.",
    "Doğadan Yön Bulma'da yön blokları kuzey/güney/doğu/batı olarak adlandırılır ve ekranda güneşin konumu görünür; rota ancak bu bilgiyle çözülebilir.",
    "Acil Çağrı Telefonu'nun başlığında ve yönergesinde numara yazılı olmaz; Tasarruf Musluğu'nda gereken miktar söylenmez.",
    "Trafik İşareti Köprüsü gerçek levha görselleriyle çalışır; parça-hedef emoji eşleşmesi bütün köprü oyunlarında kaldırılır.",
    "Kişisel Alan Ölçeri ve İsraf Ölçeri tren-tünel sahnesinden çıkarılır; ölçülen kavram ekranda görsel olarak canlandırılır.",
    "Bant oyunlarında kart hiçbir kenarda kırpılmaz; kutu etiketleri kutu içinde kalır ve kutu emojileri cevabı vermez.",
    "Radar oyunlarının ortak yönergesi her oyunun kendi konusuna göre yeniden yazılır.",
    "Her oyunda en az üç farklı içerik turu, açıklayıcı yanlış geri bildirimi ve öğrencinin kendi örneğini/uygulamasını içeren bir kapanış bulunur.",
])
story += [Spacer(1, 4 * mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 2. sınıf hayat bilgisi listesindeki h01-h36 oyunlarını kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, görsel kanıt, mekanik, üç tur, geri bildirim, öğrenci kanıtı ve test gereksinimlerini ayrıntılı biçimde tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)

reader = PdfReader(str(OUT))
print({"pages": len(reader.pages), "games": len(games), "genericPrompt": len(generic_prompt),
       "beltGames": belt_n, "bytes": OUT.stat().st_size, "output": str(OUT)})
