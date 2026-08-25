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
OUT = ROOT / "output/pdf/4_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf"
GAMES_JSON = ROOT / "tmp/pdfs/turkish4_games.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

games = json.loads(GAMES_JSON.read_text(encoding="utf-8"))
assert len(games) == 64

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
    """Satır yüksekliği sabitlenmiyor: kazanım metinleri üç satıra taştığında
       kutu içeriğe göre büyüsün, yazı dışarı düşmesin."""
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
    canv.drawString(MX, 8.2 * mm, "4. Sınıf Türkçe - Ayrıntılı Oyun Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 8.2 * mm, str(canv.getPageNumber()))
    canv.restoreState()


ENGINE = {
    "beltSort": ("bant (yürüyen bant) motoru", "Başlıktaki tartışma, laboratuvar, denetim veya adalet sahnesi yerine karanlık fabrika bandı görünüyor. Denemede cümle kartı bandın sol kenarında tamamen kırpıldı; kart okunamadan kutuya karar verilmesi gerekiyordu. Üç kutulu turlarda kutu etiketleri kutu dışına taşıyor."),
    "serveOrder": ("tepsi-servis motoru", "Başlıktaki yayınevi, kütüphane, müze, mektup veya dilekçe masası yerine ahşap servis tezgâhı açılıyor. Denemede müşteri balonundaki aday cümlelerin her biri, tepsi kartlarıyla birebir aynı simgeyle önden işaretlenmişti (pin=KONU, ampul=ANA FİKİR, zincir=YAŞAM BAĞI, eşkenar=AYRINTI)."),
    "punctFix": ("tamirhane motoru", "Tezgâh ve işaret sandığı düzeni işlevsel; ancak görev metni hangi işaretin nereye geleceğini doğrudan tarif ediyor ('Malzemeler sıralanıyor: açıklamadan önce iki nokta, arasına virgül.'). 'Kalan: ... büyük harf · ... işaret' sayacı kalan hamle sayısını ele veriyor ve uzun başlıklar üst çubukta kırpılıyor."),
    "sentenceBuild": ("matbaa/baskı kızağı motoru", "Kelime kartlarından büyük harfle başlayan kart ilk sözcüğü, nokta kartı son konumu ele veriyor; makine yalnız tek sabit dizilişi kabul ediyor."),
    "catchDrop": ("radar/kapsül yakalama motoru", "Seçenekler kapsül içinde tek tek yukarıdan düşüyor; ipucu 'Kapsülün altındaki sarı noktayı çanağın ortasına getir' diliyle veriliyor ve karar süresi düşme hızına bağlanıyor."),
    "orderSequence": ("roket-yakıt motoru", "Zaman şeridi, su döngüsü, araştırma adımları ve miras zinciri başlıklarında bile kartlar uzayda süzülüyor, seçilenler YAKIT hunisine gidiyor; kenardaki kartlar ekrandan taşabiliyor."),
    "dragMatch": ("eşleştirme köprüsü motoru", "Köprü görseli yok; hedef satırların solunda boş kareler, altta PARÇALAR havuzu var. Denemede hem parça hem hedef satırı aynı anlamı gösteren simgeyle işaretliydi (100 simgesi ↔ 'Sayı: 100', gül ↔ 'Bir çiçek', güneş ↔ 'Bir mevsim'); ayrıca altı parçalı turda cümleler çipe sığmayıp alt satırdan kesildi."),
    "memoryPairs": ("hafıza kartı motoru", "Sahne başlıktan bağımsız yıldızlı uzay; kartlar tavandan iniyor ve 'Başla! Kartları çevir' yazısı üst kart sırasının üzerine biniyor. Can göstergesi 6 kalp ile genel 3 can standardından ayrılıyor."),
    "wordHighlight": ("dedektif tutanağı motoru", "Denemede soru başlığı iki yandan kırpıldı ('...di ki\" ayrı yazılır - birleşik olanı [b]...'), metin tutanak panelinden taşarak alttaki kutunun başlığıyla üst üste bindi ve büyüteç görseli tam da karar verilecek sözcüğün ('Benimki') üzerini örttü."),
    "jumpPath": ("sırık/basamak motoru", "Basamak yazıları koyu yeşil zeminde düşük kontrastta kalıyor; kararı belirleyecek bağlam cümlesi ekranda görünmüyor, seçim sesli yönergeye ve tahmine kalıyor."),
    "codeGrid": ("kargo/robot ızgara motoru", "Izgara, engel ve hedef okunaklı; fakat 'ayrıntılı yönerge yazar' hedefine karşılık yalnız yön okları dizilebiliyor; ekranda hiçbir yazılı yönerge üretilmiyor ve görev sayısı 2-3'te kalıyor."),
    "typeWord": ("daktilo motoru", "Daktilo kâğıdı ve harf tuşları yerinde; ancak dikte edilen hedef sözcük tilkinin konuşma balonunda yazılı olarak da görünüyor ve harf havuzunun ilk harfleri sözcüğün sırasını izliyor."),
    "dragSlider": ("tren-tünel motoru", "Su tüketimi tahmini istenirken sahnede kırmızı bir tren beş tünelden birine giriyor ve sayaç '0/3 tren' yazıyor. Görev tamamen sayısal tahmine indirgenmiş; kazanımın dayandığı metin ekranda hiç yok."),
    "tallyChart": ("çetele motoru", "Arkadaş balonundaki cümle sütun adını birebir içeriyor; sütun altlarında çetele çizgisi yerine rakam sayacı artıyor."),
    "surveyChart": ("çetele motoru (anket sürümü)", "Sahne 'ÇETELE TABLOSU' başlığıyla açılıyor ama oyun bir seçim; gelen oy balonu ('Ela') sütun başlığıyla birebir aynı olduğu için hiçbir çıkarım gerekmiyor ve sütunlarda çetele çizgisi yerine rakam artıyor."),
}

TYPE_RISK = {
    "beltSort": "Bant hızı okuma ve karar süresine karışıyor; kenarda kırpılan kart hiç okunamadan puan ve can etkiliyor. Yazım kuralı turlarında (de/da, ki) cümleyi görmeden karar vermek imkânsız olduğundan hata motor kaynaklı oluyor.",
    "serveOrder": "Balondaki simge ile karttaki simge birebir eşleştiğinde öğrenci metni hiç okumadan simge kopyalayarak görevi bitirebilir; konu, ana fikir ve yaşam bağlantısı ayrımı hiç kurulmaz.",
    "punctFix": "Görev metninin kuralı ve işaret yerini söylemesi, düşünmek yerine tarif edileni uygulamayı ödüllendirir; 'Kalan' sayacı kaç hamle kaldığını vererek eleme stratejisini kolaylaştırır.",
    "sentenceBuild": "Büyük harfli kart ve nokta kartı dizilişi ele verir; ayrıca Türkçenin kurallı alternatif dizilişleri yanlış sayılırsa doğru dil sezgisi cezalandırılır.",
    "catchDrop": "Doğru cevabı bilmek yetmiyor; düşen kapsüle yetişmek gerekiyor. Yanlış motor hareketi yanlış dil kararı gibi can kaybettiriyor.",
    "orderSequence": "Kartlardaki tarih ve numara ipuçları, içerik bilgisi olmadan sayı sıralamayla çözümü verir; roket-yakıt sahnesi başlıkla çelişip kavramı bulanıklaştırır.",
    "dragMatch": "Simge eşleşmesi cevabı doğrudan verdiği için sesteş, terim veya atasözü ayrımı hiç yapılmadan oyun bitirilebilir; taşan yazılar okunamadığından eşleştirme gerekçesiz kalır.",
    "memoryPairs": "Eşleştirme, kavramı açıklamadan kart konumunu ezberleyerek de çözülür; görsel hafıza başarısı dil bilgisi başarısı gibi kayda geçer.",
    "wordHighlight": "Kırpılan soru, taşan metin ve hedefi örten büyüteç cevabı rastlantıya bırakır; sözcüğü bulmak, yazım kuralını (de/da, ki, ayrı-birleşik) açıklama kanıtı üretmez.",
    "jumpPath": "Bağlam cümlesi ekranda olmadığından seçim tahmine döner; düşük kontrastlı basamak yazıları okunamadan zıplanabilir.",
    "codeGrid": "Kazanım 'ayrıntılı yönerge yazar' olduğu hâlde öğrenci hiçbir sözlü/yazılı yönerge üretmez; ok dizmek yön kavramını ölçer, yazmayı ölçmez.",
    "typeWord": "Hedef sözcük ekranda yazılı olduğundan dikte, dinleme-yazma yerine bakarak kopyalamaya dönüşür; harf havuzu sırayı ele verir.",
    "dragSlider": "Ölçülen şey Türkçe becerisi değil sayı tahmini; metin, ön bilgi ve günlük yaşam bağlantısı kurulmadığı için kazanım hiç yoklanmaz.",
    "tallyChart": "Cümledeki sözcük sütun adıyla birebir aynı olduğundan görev sözcük kopyalamaya iner; rakam sayacı çetele kuralını (beşinci çizgi dördü keser) hiç göstermez.",
    "surveyChart": "Oy ile sütun adı aynı olduğu için veri toplama mekanik tıklamaya iner; öğrenci sonucu yorumlamadan, çoğunluk ve azınlık ilişkisini kurmadan oyunu bitirebilir.",
}

TYPE_FEEDBACK = {
    "beltSort": "Yanlış kutuda bant dursun; kart sabitlenip yeniden okunsun ve ölçüt (neden bu kutu değil) doğru söylenmeden hatırlatılsın. Kenarda kırpılan kart hiç puanlanmasın.",
    "serveOrder": "Yanlış kartta tepsi kilitlenmesin; istek metni yeniden okunsun ve kartın neden uymadığı içerik üzerinden gösterilsin, simge üzerinden değil.",
    "punctFix": "Yanlış işarette cümle uygun tonlamayla seslendirilsin ve işaretin görevi hatırlatılsın; doğru işaret adı ve yeri söylenmesin, 'Kalan' sayacı ipucu vermesin.",
    "sentenceBuild": "Yanlışta bütün dizi bozulmasın; yalnız son kart geri alınsın. Kurallı alternatif diziliş kurulduysa doğru kabul edilsin ve fark açıklansın.",
    "catchDrop": "Yanlış yakalamada düşme dursun; seçenek sabitlenip metin/ses kanıtıyla yeniden karar verilsin. Kaçan kapsül can yakmasın, yalnız yeniden denensin.",
    "orderSequence": "Yanlış adımda dizi silinmesin; yalnız son seçim geri alınsın ve 'önce/sonra' ilişkisini düşündüren ipucu verilsin.",
    "dragMatch": "Yanlış parça başlangıca dönsün; hedef parlatılmasın. Eşleşmenin dayandığı sözcük veya bağlam ipucu kısa bir soruyla vurgulansın.",
    "memoryPairs": "Yanlış çiftte kartlar hemen kapanmasın; iki içerik yan yana sesli okunup farkı soran kısa bir ipucu verilsin. Can standardı diğer oyunlarla eşitlensin.",
    "wordHighlight": "Yanlış sözcükte metin kaybolmasın; soru ile seçilen sözcük yan yana okunup kural karşılaştırılsın. Büyüteç hiçbir zaman hedefi örtmesin.",
    "jumpPath": "Yanlış basamakta düşme animasyonu ceza üretmesin; bağlam cümlesi yeniden gösterilip iki seçenek yan yana karşılaştırılsın.",
    "codeGrid": "Engele çarpınca robot dursun ve programdaki hatalı adım işaretlensin; tüm program silinmesin, yalnız hatalı adımdan itibaren düzeltilsin.",
    "typeWord": "Yanlış harfte doğru harf gösterilmesin; sözcük yeniden dinletilsin ve gerekirse hece hece söylensin. Tekrar dinleme hiçbir turda ceza olmasın.",
    "dragSlider": "Yanlış tahminde gerçek değer tek başına verilmesin; metindeki veya günlük yaşamdaki karşılaştırma ölçüsü (kaç bardak, kaç kova) gösterilerek tahmin yeniden yapılsın.",
    "tallyChart": "Yanlış satırda cevap cümlesi yeniden dinletilsin; tür ile cümledeki ipucu arasındaki ilişki soruyla kurulsun, doğru satır parlatılmasın.",
    "surveyChart": "Yanlış işaretlemede oy yeniden dinletilsin; sayım bitince sonuç doğrudan açıklanmasın, öğrenciye 'en çok/en az kim, kaç fark var?' soruları sorulsun.",
}

TYPE_ACCEPT = {
    "beltSort": "İlk iki turda kartlar sabit gelecek; hız ancak üçüncü turda isteğe bağlı açılacak. Kart hiçbir konumda kırpılmayacak, kutu etiketi kutu içinde kalacak ve dokunma alanı en az 44 px olacak.",
    "serveOrder": "Kartlarda etiket/simge değil içerik yazacak; balondaki aday cümleler kart simgeleriyle eşleşerek cevabı vermeyecek ve her müşteri farklı içerik havuzu kullanacak.",
    "punctFix": "Görev metni kuralı ve işaretin yerini söylemeyecek; 'Kalan' sayacı ilk turdan sonra kapanacak; başlık ve görev metni hiçbir çözünürlükte kırpılmayacak.",
    "sentenceBuild": "Kartlar küçük harfle gelecek; baş harf ve son işaret öğrencinin ayrı kararı olacak. Kurallı alternatif dizilişler kabul edilecek ve son turda serbest yazı alanı bulunacak.",
    "catchDrop": "İlk turda düşme kapalı, seçenekler sabit olacak; başarı doğru karar + kanıt ile ölçülecek, yakalama refleksi puana karışmayacak.",
    "orderSequence": "Roket-yakıt sahnesi kaldırılacak; sırayı ele veren tarih/numara ilk turda gizlenecek ve kartlar 390x844 ekranda tam içeride kalacak.",
    "dragMatch": "Parça ve hedefteki simgeler cevabı eşleştirmeyecek (ya kaldırılacak ya da ayırt edici olmayacak); yazılar çipe sığacak, hedef alanlar en az 44 px olacak ve her eşleşme bir gerekçe sorusuyla doğrulanacak.",
    "memoryPairs": "Kart konumları ve içerik her açılışta karışacak; can sayısı genel standartla (3) eşitlenecek ve her eşleşme en az bir gerekçe adımıyla doğrulanacak.",
    "wordHighlight": "Metin panelden taşmayacak, soru tam görünecek, büyüteç veya başka öge sözcüğü örtmeyecek; karar sonrası öğrenci kuralı seçerek veya yazarak gerekçelendirecek.",
    "jumpPath": "Basamak yazıları zeminden ayrışan kontrastta olacak; karar bağlamı (cümle/hikâye) ekranda sürekli duracak; düşme animasyonu ceza üretmeyecek.",
    "codeGrid": "Yön blokları yazılı yönerge kartlarına dönüşecek ve program cümle olarak okunacak; en az üç görev bulunacak; son görevde öğrenci yönergeyi kendisi yazacak.",
    "typeWord": "Hedef sözcük ekranın hiçbir yerinde yazılı görünmeyecek; harf havuzu karışık dizilecek; tekrar dinleme cezasız olacak ve sayısı kaydedilecek.",
    "dragSlider": "Tren-tünel sahnesi kaldırılacak; ekranda tahminin dayanacağı kısa bilgi metni bulunacak ve öğrenci tahminini metindeki veriye bağlayarak gerekçelendirecek.",
    "tallyChart": "Cevap cümleleri tür adını birebir söylemeyecek; işaretler çetele çizgisiyle birikecek, beşinci çizgi dördünü kesecek ve bitişte tablo yorum sorusu sorulacak.",
    "surveyChart": "Oy ifadeleri sütun adını birebir tekrar etmeyecek; sayım çetele çizgisiyle görünecek ve oyun ancak sonuç yorumu (çoğunluk, fark, azınlık hakkı) yapıldıktan sonra tamamlanacak.",
}

MODALITY_RISK = {
    "writing": "Kazanım yazma/oluşturma istediği hâlde mevcut yapıda serbest sözcük, cümle veya metin üretme alanı yok; hazır kartı seçmek ya da dizmek gerçek yazma kanıtı değildir.",
    "speaking": "Kazanım konuşma istediği hâlde öğrenci ses üretmiyor; yalnız seçenek işaretlendiği için vurgu, tonlama, beden dili ve uygun ifade gözlenemiyor.",
    "listening": "Dinleme hedefinde yazılı yönerge ve seçenekler cevabı taşıyabiliyor; ses kapatıldığında da oyun çözülebiliyorsa ölçme geçerli değildir.",
    "reading": "Okuma hedefi, metindeki kanıtı kullanmaktan çok görsel olarak en belirgin seçeneği bulmaya indirgenirse çıkarım ve anlama ölçülmez.",
}

MODALITY_NEW = {
    "writing": "Son turda öğrenci gerçek bir sözcük, cümle, yönerge veya metin üretsin; kelime kartları yalnız erişim desteği olsun ve hazır kart dizmek tek başına başarı sayılmasın.",
    "speaking": "Örnek dinletildikten sonra öğrenci kısa bir ses kaydı alsın veya yetişkin/öz değerlendirme rubriğiyle konuşsun; gerekçe, uygun ifade ve anlaşılabilirlik ayrı kaydedilsin.",
    "listening": "İlk dinleme turunda hedef metin ve cevap anahtarı görünmesin; ses en az iki kez tekrar edilebilsin ve tekrar dinleme ceza oluşturmasın.",
    "reading": "Öğrenci cevaptan önce metindeki görsel/sözel kanıtı işaretlesin; doğru seçenek ancak kanıtla tutarlı olduğunda kabul edilsin.",
}


DESIGNS = {
"z01": ("Gerçek bir sınıf tartışma çemberi kur: görüş bir karakterin ağzından söylenip panoya asılsın, kart bantta akmasın ve hiçbir kenarda kırpılmasın.", "Kısmen katılınabilecek görüşler eklensin; öğrenci 'katılıyorum / kısmen / katılmıyorum' ayrımını yapsın.", "Öğrenci kararının nedenini 'Katılıyorum çünkü ...' kalıbıyla yazsın veya söylesin; bir de öneri eklesin."),
"z02": ("Gerçek editör masası çiz: metin ayrı panelde okunur dursun; tepsi kartlarında etiket değil aday cümleler yazsın ve balondaki simge kopyası tamamen kaldırılsın.", "Konu, ana fikir, yaşam bağlantısı ve ayrıntı adayları yakın çeldiricilerle verilsin; öğrenci her kartın türünü kendisi belirlesin.", "Öğrenci yeni bir metnin ana fikrini ve kendi yaşamıyla bağlantısını hazır kart olmadan iki cümleyle yazsın."),
"z03": ("Atölye tezgâhı gerçek matbaa görseliyle kurulsun; görev metni işaretin adını ve yerini söylemesin, yalnız 'cümlenin anlamına uygun işareti koy' desin.", "Aynı cümle farklı işaretlerle anlam değiştirsin; öğrenci tonlamalı seslendirmeden yararlanarak seçsin.", "Öğrenci iki bozuk cümleyi ekran klavyesiyle baştan doğru yazsın; büyük harf ve işaret kararları kayda geçsin."),
"z04": ("Baskı makinesi gerçekten çalışsın: kurulan cümle baskıdan çıkıp panoya asılsın. Kartlar küçük harfle gelsin; baş harf ve son işaret öğrencinin ayrı kararı olsun.", "Devrik ve kurallı cümle karşılaştırılsın; öğrenci hangisinin kurallı olduğunu ögelerin sırasıyla açıklasın.", "Öğrenci aynı sözcüklerden en az birini kullanarak kendi kurallı cümlesini ekran klavyesiyle yazsın."),
"z05": ("Gerçek bir sözlük sayfası açılsın: kart çevrilince madde başı, tanım ve örnek cümle birlikte görünsün; uzay zemini kaldırılsın.", "Yakın erdemler çeldirici olsun (hoşgörü/sabır, cömertlik/yardımseverlik); tanımdaki ayırt edici sözcük vurgulansın.", "Öğrenci seçtiği erdemi kendi tanımıyla yazsın ve bir davranış örneği eklesin."),
"z06": ("Cümle sabit panelde dursun; anlam seçenekleri düşmesin, sabit kartlarda olsun. Öğrenci karar öncesi cümledeki bağlam ipucunu işaretleyebilsin.", "Yakın iki anlamdan bağlama uygun olan seçilsin; aynı sözcük ikinci bir cümlede farklı anlamla gösterilsin.", "Tahmin-sözlük-yazma döngüsü tamamlansın: öğrenci tahminini sözlükle karşılaştırıp anlamı kendi cümlesiyle yazsın."),
"z07": ("Metin paneli taşmadan yerleşsin, büyüteç hedefi örtmesin; hatalı sözcüğe dokununca kalem otomatik düzeltmesin - öğrenci doğru yazımı seçsin veya klavyeyle yazsın.", "Farklı hata türleri karışsın: yazım, büyük harf, ayrı-birleşik; her düzeltmede kural kısa görünsün.", "Öğrenci kısa bir paragrafı bağımsız denetleyip bütün hataları düzeltsin; düzeltme sayısı ve türü kayda geçsin."),
"z08": ("Hikâye metni ekranda görünür dursun; her basamakta 'sonra ne olur?' seçenekleri metindeki kanıta bağlansın ve basamak yazıları okunur kontrastta olsun.", "Doğrudan söylenmeyen, çıkarım gerektiren tahmin adımları eklensin; olayın öncesi de sorulsun.", "Öğrenci tahminini 'Bence ... olacak çünkü metinde ...' kalıbıyla gerekçelendirsin."),
"z09": ("Roket ve YAKIT hunisi kaldırılsın; ekranda gerçek yatay zaman şeridi dursun. İlk turda kartlardaki tarihler gizlensin; sıralama olay metninden yapılsın, doğrulamada tarihler açılsın.", "Tarihi gizli yeni bir olay seti dinletilsin; öğrenci yalnız dinlediği bilgiyle sıralasın.", "Öğrenci sıraladığı olayları 'önce / daha sonra / en sonunda' bağlarıyla üç cümlede anlatsın."),
"z10": ("Tasnif masası kurulsun: sözcük çifti sabit kartta, her iki sözcük de bir örnek cümleyle birlikte görünsün; bant akışı kaldırılsın.", "Sesteş ile eş anlamlı karışabilen çiftler eklensin (yüz/yüz, gül/gül); ölçüt yazılış-anlam ilişkisiyle tartışılsın.", "Öğrenci bir sesteş çifti iki ayrı cümlede kullanarak anlam farkını yazsın."),
"z11": ("Gerçek köprü sahnesi kurulsun ve parça-hedef simge eşleşmesi KALDIRILSIN; karar yalnız cümledeki bağlamdan çıkarılabilsin. Cümleler çipe sığacak boyutta yerleşsin.", "Aynı sesteş sözcüğün üç farklı anlamı karşılaştırılsın; ayırt edici bağlam sözcüğü işaretlensin.", "Öğrenci bir sesteş sözcüğü iki farklı anlamda kendi cümlelerinde kullanarak yazsın."),
"z12": ("Tarih kitabı sayfası gerçek dizgi görseliyle açılsın; kesme işaretinin ayırdığı ek renkli gösterilsin ve kural kutusu ekranda kalsın.", "Kesme istemeyen durumlar çeldirici olsun (Türkçe eki alan cins isim, kurum adına gelen çokluk eki).", "Öğrenci iki özel ada gelen eki ekran klavyesiyle kendisi yazsın; kesme işaretini kendisi koysun."),
"z13": ("Radar-kapsül düzeni kaldırılsın; bilgi kartları panoda sabit dursun, her kartın yanında 'kaynağı gör' düğmesi olsun ve doğruluk kararı kanıtla verilsin.", "Kısmen doğru ama eksik ifadeler eklensin; öğrenci 'tamamen doğru / kısmen doğru / yanlış' ayrımı yapsın.", "Öğrenci yanlış bilgiyi doğru biçimiyle kendi cümlesinde yazsın ve dayandığı kaynağı belirtsin."),
"z14": ("Gerçek mektup kâğıdı açılsın: tarih, hitap, gövde, kapanış ve imza alanları görünür olsun; bölümler tepsiye değil kâğıttaki yerlerine yerleşsin.", "Bölüm ile içerik eşleştirilsin: hangi cümle hitap, hangisi kapanış? Uygun olmayan üslup çeldirici olsun.", "Öğrenci gaziye kısa mektubu ekran klavyesiyle yazsın; imzasına ad ve soyadını kendisi eklesin."),
"z15": ("Makine karşıtlığı görselleştirsin: seçilen zıt çift iki kefeli sahnede karşı karşıya gelsin; kartlar küçük harfle gelsin.", "Bağlama duyarlı zıt çiftler eklensin (ağır-hafif / ağır-kolay); hangi cümlede hangisinin zıddı olduğu tartışılsın.", "Öğrenci bir zıt çifti aynı cümlede kullanarak karşılaştırma cümlesini kendisi yazsın."),
"z16": ("Hedef sözcük tilkinin balonunda YAZILMASIN; yalnız 'Dinle düğmesine bas' yönergesi görünsün. Harf havuzu karışık dizilsin ve sözcüğün harf sırasını ele vermesin.", "Yazımı zor sözcükler eklensin (â, ğ, kesme işaretli özel ad); sözcük iki kez dinletilip hece hece tekrar seçeneği sunulsun.", "Öğrenci yazdığı sözcüğü kısa bir cümle içinde kullansın; cümle diktesiyle tur tamamlansın."),
"z17": ("Enerji istasyonu gerçek görsellerle kurulsun (güneş paneli, rüzgâr türbini, kömür ocağı); kaynak kartı sabit gelsin ve kenarda kırpılmasın.", "Tartışmalı örnekler eklensin (orman: yenilenebilir ama tükenebilir); öğrenci ölçütü seçip savunsun.", "Öğrenci bir kaynağı neden o kutuya koyduğunu bir cümleyle yazsın."),
"z18": ("Yön okları yazılı yönerge kartlarına dönüşsün ('iki adım ileri git', 'sağa dön'); dizilen program panelde numaralı cümleler hâlinde okunsun ve robot okurken uygulasın.", "Engeller değişsin ve daha uzun yönerge istensin; öğrenci hatalı bir programı okuyup hatayı bulsun.", "Öğrenci afet çantasına giden yönergeyi kelime kartları veya klavyeyle kendisi yazsın; robot yazılanı uygulasın."),
"z19": ("Orman sahnesi ağaç kovuklarıyla kurulsun; kartlar kovuklardan çıksın ve eşleşen eş anlamlı çift aynı cümle içinde iki kez okunarak doğrulansın.", "Her bağlamda birebir değiştirilemeyen eş anlamlılar karşılaştırılsın (kara-siyah her cümlede değişmez).", "Öğrenci bir eş anlamlı çiftin iki üyesiyle ayrı cümleler yazıp anlamın korunduğunu kontrol etsin."),
"z20": ("Doğa güncesi gerçek defter sayfası olarak açılsın; görev metni hangi işaretin nereye geleceğini söylemesin ve başlık üst çubukta kırpılmasın.", "Konuşma çizgisi ile tırnak işaretinin farkı iki örnekle karşılaştırılsın: aktarılan söz ve yazılan söz.", "Öğrenci kendi doğa gözlemini bir konuşma cümlesiyle yazıp işaretlerini kendisi koysun."),
"z21": ("Roket kaldırılsın; gerçek su döngüsü şeması (deniz, buhar, bulut, yağmur, akarsu) ekranda dursun ve adım kartları şemanın üzerindeki yerlerine yerleşsin.", "Kar ve yer altı suyu varyantlarıyla yeni döngü sıralansın; ara adım çeldiricisi eklensin.", "Öğrenci döngüyü kendi cümleleriyle üç adımda yazsın veya anlatsın."),
"z22": ("Yarım metin ekranda görünür dursun: önceki bölüm panelde okunsun, tamamlama kartları metnin altında sabit olsun.", "İki makul tamamlamadan kişi, zaman ve konu tutarlılığına uyan seçilsin; öğrenci dayandığı ipucu cümlesini işaretlesin.", "Öğrenci metnin devamını hazır kart olmadan iki cümleyle kendisi yazsın."),
"z23": ("Tren-tünel sahnesi kaldırılsın; ekranda kısa bir bilgi metni (musluk dakikada kaç litre akıtır) ve gerçek su sayacı bulunsun. Tahmin bu metne dayansın.", "Tahmin, gerçek değer ve fark birlikte gösterilsin; iki farklı kullanım karşılaştırılsın (duş / küvet).", "Öğrenci tasarruf önerisini 'Metne göre ... yaparsak ... litre tasarruf ederiz' kalıbıyla yazsın."),
"z24": ("Dergi masası gerçek sayfa taslağıyla kurulsun; plan bölümleri (başlık, giriş, gelişme, sonuç, görsel, kaynak) taslak sayfadaki yerlerine yerleşsin.", "Amaca göre farklı plan istensin: bilgilendirici yazı ile öykü planı karşılaştırılsın.", "Öğrenci verilen konu için kendi yazma planını dört maddeyle yazsın."),
"z25": ("Gerçek kütüphane rafları ve kaynak kapakları çizilsin; okurun amacı açıklayıcı cümle olarak okunsun ve tür kapaktan çıkarımla bulunsun.", "Aynı konuda ansiklopedi, öykü ve dergi karşılaştırılsın; amaca en uygun olan gerekçeyle seçilsin.", "Öğrenci kendi okuma amacını ve seçtiği türü 'Bu kaynağı seçtim çünkü ...' cümlesiyle yazsın."),
"z26": ("Anlam laboratuvarı kurulsun: cümle sabit okunur kartta dursun, koyu sözcük vurgulu gösterilsin ve bant hızı kaldırılsın; üç kutu etiketi kutu içinde kalsın.", "Aynı sözcüğün üç anlamı yan yana karşılaştırılsın (yüzey: gerçek / mecaz / terim).", "Öğrenci bir sözcüğü terim anlamıyla kendi cümlesinde kullanıp gerçek anlamından farkını yazsın."),
"z27": ("Köprü kalasları atasözlerini taşısın; simge eşleşmesi kaldırılsın ve doğru eşleşmede atasözünün anlattığı durum kısa canlandırmayla gösterilsin.", "Yakın anlamlı atasözü çeldiricileri eklensin; anlam ile birebir sözcük benzerliği ayrılsın.", "Öğrenci bir atasözünü uygun bir yaşam durumuna bağlayarak cümle kursun ve sesli söylesin."),
"z28": ("Gerçek e-posta ekranı açılsın: alıcı, konu, hitap, gövde ve kapanış alanları görünür olsun; işaretler bu gerçek yapının üzerinde çalışılsın.", "Resmî ve samimi yazışmanın üslup ve noktalama farkı karşılaştırılsın.", "Öğrenci yazara iki cümlelik e-postayı klavyeyle yazsın; hitap ve kapanış kararları kayda geçsin."),
"z29": ("Radar kaldırılsın; kaynak kartları (ansiklopedi, kişisel blog, kurum sitesi, sosyal medya) sabit dursun ve her kartta yazar, tarih, kurum bilgisi görünsün.", "Aynı bilgiyi veren iki kaynaktan hangisinin daha güvenilir olduğu ölçütlerle karşılaştırılsın.", "Öğrenci seçtiği kaynağı 'Bu kaynak güvenilir çünkü ...' cümlesiyle gerekçelendirsin."),
"z30": ("Cevap cümleleri sütun adını birebir söylemesin (çıkarım gereksin); işaretler rakam değil çetele çizgisiyle biriksin ve beşinci çizgi dördünü kessin.", "Çetele tamamlanınca sıklık tablosuna çevrilsin; 'en çok / en az / kaç fark' soruları sorulsun.", "Öğrenci kendi tercihini ekleyip sonucu 'Sınıfımızda en çok ... okunuyor, çünkü ...' cümlesiyle yorumlasın."),
"z31": ("Gerçek dilek kutusu ve form sahnesi kurulsun; önce istek/şikâyet/öneri türü seçilsin, sonra türe uygun cümle kurulsun.", "Aynı konu üç türde ifade edilsin: isteğin, şikâyetin ve önerinin dil farkı karşılaştırılsın.", "Öğrenci kütüphane için kendi önerisini iki cümleyle klavyeden yazsın; nazik ifade rubriği uygulansın."),
"z32": ("Araştırma masası kurulsun: adımlar (soru belirleme, kaynak tarama, not alma, yazma, kaynak gösterme) panoda görselleşsin, roket kullanılmasın.", "Eksik veya yer değiştirmiş adım bulma görevi eklensin; kaynak göstermenin neden son adım olduğu tartışılsın.", "Öğrenci merak ettiği bir soru için araştırma planını yazsın ve kullandığı kaynağı kurala uygun belirtsin."),
"z33": ("Bağlaç bandı durdurulsun; cümle sabit kartta ve boşluk vurgulu gösterilsin. Kutu etiketleri kutu içinde kalsın ve üç kutu 44 px'ten küçük olmasın.", "Aynı iki cümle farklı bağlaçlarla birleştirilip anlam farkı karşılaştırılsın (ve / ama / çünkü).", "Öğrenci üç bağlaçtan ikisiyle kendi cümlelerini yazsın."),
"z34": ("Makine bağlacın işlevini göstersin: seçilen bağlaç iki cümleyi görsel olarak birleştirsin (ekleme, karşıtlık, neden ayrı animasyonla).", "Yanlış bağlaç seçilince anlamın nasıl bozulduğu örnekle gösterilsin.", "Öğrenci neden-sonuç ilişkisini 'çünkü' ve 'bu yüzden' ile iki yönde kendisi yazsın."),
"z35": ("Sahne programı gerçek broşür olarak açılsın; arasözün ne olduğu bir örnekle sayfa kenarında dursun ve görev metni işaret adını söylemesin.", "Arasöz virgülü ile sıralama virgülü karşılaştırılsın; kısa çizginin farklı görevi ayrı örnekle verilsin.", "Öğrenci arasöz içeren bir cümleyi klavyeyle yazıp virgülleri kendisi koysun."),
"z36": ("Gerçek köprü görseli kurulsun: sol kıyı neden, sağ kıyı sonuç; simge eşleşmesi kaldırılsın ve her doğru eşleşme köprüye kalas eklesin.", "Aynı nedenin birden çok sonucu olabildiği örnekler eklensin; zincirleme neden-sonuç kurulsun.", "Öğrenci kendi yaşamından bir neden-sonuç cümlesini 'çünkü' ve 'bu yüzden' ile yazsın."),
"z37": ("Tiyatro sahnesi gerçek görselle kurulsun; kart açılınca sözcük seslendirilsin ve eşleşen çift aynı replikte iki kez okunarak doğrulansın.", "Konuşma dilinde daha uygun düşen eş anlamlı seçilsin; üslup farkı karşılaştırılsın.", "Öğrenci eş anlamlı çiftle kısa bir replik söyleyip kaydetsin veya rubrikle değerlendirilsin."),
"z38": ("Cümle sabit panelde dursun; anlam seçenekleri düşmesin. Öğrenci karar öncesi bağlam ipucunu işaretleyebilsin.", "Aynı sözcüğün mecaz ve gerçek anlamı iki cümlede karşılaştırılsın.", "Öğrenci tahminini sözlükle doğrulayıp anlamı kendi cümlesiyle yazsın."),
"z39": ("Sunum sahnesi kurulsun: kürsü, dinleyiciler ve not kartları görünsün; danışmanın isteği sunum amacına göre okunsun, simge kopyası kaldırılsın.", "Aynı konu farklı dinleyiciler için planlansın (sınıf / veli); ses tonu ve beden dili ögeleri ayrı seçilsin.", "Öğrenci bir dakikalık sunumunu planına göre yapsın ve kaydetsin; beden dili-ses tonu rubriğiyle değerlendirilsin."),
"z40": ("Metin taşmadan yerleşsin ve büyüteç hedefi örtmesin; hatalı sözcüğe dokununca doğru biçim otomatik gelmesin, öğrenci seçsin ya da yazsın.", "Ayrı-birleşik yazım kuralları karışık verilsin (de/da, ki, mi, pekiştirme); her düzeltmede kural kısa görünsün.", "Öğrenci kendi yazdığı kısa paragrafı denetleyip hatalarını bulsun ve düzeltsin."),
"z41": ("Bant durdurulsun ve cümle kartı ekranın tam ortasında, hiçbir kenarda kırpılmadan gösterilsin. [de] vurgulanıp cümle sesli okunsun; kural kutusu ekranda kalsın.", "'Dahi/bile' testi uygulatılsın: öğrenci sözcüğü cümleden çıkarıp anlamın bozulup bozulmadığını görsün.", "Öğrenci hem ayrı hem birleşik 'de' kullanarak iki cümleyi klavyeyle yazsın."),
"z42": ("Metin panelden taşmasın, soru başlığı tam görünsün ve büyüteç karar verilecek sözcüğü örtmesin; kural kutusu sayfada sabit kalsın.", "Bağlaç 'ki' ile ilgi eki '-ki/-kü' aynı metinde karşılaştırılsın; doğru yazılmış çeldiriciler bulunsun.", "Öğrenci 'ki' bağlacını ayrı yazarak kendi cümlesini yazsın."),
"z43": ("Yön blokları yazılı yönerge kartlarına dönüşsün; dizilen program panelde numaralı cümleler hâlinde görünsün ve robot okurken adım adım uygulasın.", "Hatalı verilen bir programı okuyup hatayı bulma ve yalnız o adımı düzeltme görevi eklensin.", "Öğrenci robotu hedefe götüren yönergeyi kendisi yazsın; yazılan yönerge çalıştırılarak sınansın."),
"z44": ("Deney masası gerçek araç görselleriyle kurulsun; bilim insanının isteği amaç-araç-adım içeren kısa plan olarak okunsun ve simge kopyası kaldırılsın.", "Amaca uymayan çekici araç çeldirici olsun; öğrenci elemeyi gerekçelendirsin.", "Öğrenci basit bir deneyin adımlarını örnek ekleyerek kendi cümleleriyle yazsın."),
"z45": ("Deney raporu gerçek şablonla açılsın; görev metni hangi işaretin nereye geleceğini SÖYLEMESİN ve 'Kalan' sayacı ilk turdan sonra kapansın.", "Yay ayraç (açıklama), eğik çizgi (birim) ve kısa çizginin farklı görevleri ayrı örneklerle çalışılsın.", "Öğrenci kendi gözlem cümlesini iki nokta ve yay ayraç kullanarak klavyeyle yazsın."),
"z46": ("Köprü kalasları bilim terimlerini taşısın; simge eşleşmesi kaldırılsın ve doğru eşleşmede terimin anlamı kısa görselle gösterilsin.", "Aynı sözcüğün günlük ve terim anlamı karşılaştırılsın (madde, kütle, çözelti).", "Öğrenci bir terimi tanımıyla birlikte kendi cümlesinde kullanarak yazsın."),
"z47": ("Yönerge makinesi adımı gerçekten uygulasın: kurulan cümle bir deney animasyonunu tetiklesin; kartlar küçük harfle gelsin.", "Eksik ve ayrıntılı yönerge karşılaştırılsın: 'suyu koy' ile 'bardağa yarıya kadar su koy' farkı gösterilsin.", "Öğrenci üç adımlı deney yönergesini ayrıntılarıyla kendisi yazsın."),
"z48": ("Bilim panosu kurulsun; adımlar soru-hipotez-deney-gözlem-sonuç akışıyla panoda görselleşsin, roket sahnesi kullanılmasın.", "Eksik adım bulma görevi eklensin: araştırmada hangi adım atlanmış?", "Öğrenci kendi araştırma sorusu için beş adımı sırayla yazsın."),
"z49": ("Müze salonu gerçek eser görselleriyle kurulsun; ziyaretçi isteği bilgi metninden çıkarım gerektirsin ve simge kopyası kaldırılsın.", "Somut ve somut olmayan miras ayrımı yapılsın (cami / âşıklık geleneği); ölçüt tartışılsın.", "Öğrenci bir mirası iki cümleyle tanıtsın ve günlük yaşamla bağını kursun."),
"z50": ("Bant durdurulsun ve cümle kartı tam görünsün; [ki] vurgulanıp cümle sesli okunsun. Kural kutusu ekranda kalsın.", "Bağlaç 'ki', ilgi eki '-ki' ve sıfat yapan '-ki' ayrı örneklerle karşılaştırılsın.", "Öğrenci hem ayrı hem birleşik 'ki' kullanarak iki cümleyi klavyeyle yazsın."),
"z51": ("Müze panosu gerçek pano görseliyle kurulsun; özel ad türleri (yapı, kişi, dönem, kurum) karışık cümlelerde çalışılsın ve düzelen cümle panoya asılsın.", "Kesme işareti ve büyük harf birlikte istensin; cins isim çeldiricileri eklensin.", "Öğrenci pano için kendi tanıtım cümlesini klavyeyle yazsın; büyük harf ve kesme kararlarını bağımsız versin."),
"z52": ("Türkiye haritası sahne olsun; eşleşen miras haritadaki şehrine yerleşsin ve kısa bilgi cümlesi okunarak eşleşme kanıtlansın.", "Aynı şehirden iki miras veya benzer mirasları olan iki şehir çeldirici olsun.", "Öğrenci bildiği bir mirası 'Bu miras ...dadır ve ...' cümlesiyle tanıtsın."),
"z53": ("Zincir gerçek atölye sahnesiyle kurulsun: usta, çırak ve ürün kuşak kuşak görünsün; roket kaldırılsın.", "Aktarımın kesintiye uğradığı ve yeniden canlandığı adımlar eklensin.", "Öğrenci bir el sanatının kuşaklar arası yolculuğunu üç cümleyle anlatsın veya yazsın."),
"z54": ("Makine eş anlamı görselleştirsin: seçilen çift aynı cümlede yer değiştirerek anlamın korunduğunu göstersin; kartlar küçük harfle gelsin.", "Her bağlamda değiştirilemeyen eş anlamlılar çeldirici olsun.", "Öğrenci eş anlamlı sözcük içeren kendi cümlesini klavyeyle yazsın."),
"z55": ("Metin taşmasın ve büyüteç örtmesin; yabancı sözcüğe dokununca kalem otomatik değiştirmesin - Türkçe karşılığı öğrenci seçsin ve değişen cümle yeniden okunsun.", "Birden çok Türkçe karşılıktan bağlama uygun olan seçilsin; karşılığı olmayan sözcükler çeldirici olsun.", "Öğrenci cümleyi Türkçe karşılıkla ekran klavyesinden yeniden yazsın."),
"z56": ("Kalkan-yakalama mekaniği kaldırılsın; davranış kartları sabit gelsin ve öğrenci 'koruyor / zarar veriyor' kararını gerekçe seçerek versin.", "Niyet ile etki ayrılsın: iyi niyetli ama zarar veren davranışlar eklensin.", "Öğrenci mirası koruyan bir davranış önerisini nedeniyle birlikte yazsın veya söylesin."),
"z57": ("Adalet meydanı sahnesi kurulsun; ifade kartı sabit okunsun, karar sonrası kart doğru sütuna konsun ve üç kutu etiketi kutu içinde kalsın.", "Aynı konunun hak, sorumluluk ve özgürlük yönleri birlikte verilsin; hak ile özgürlük farkı tartışılsın.", "Öğrenci bir hakkını, ona bağlı sorumluluğunu ve bir özgürlüğünü kendi cümleleriyle yazsın."),
"z58": ("Gerçek dilekçe şablonu açılsın: tarih, makam, istek metni, ad-soyad ve imza alanları görünür olsun; bölümler şablondaki yerlerine yerleşsin ve simge kopyası kaldırılsın.", "Uygun ve uygun olmayan üslupta istek cümleleri karşılaştırılsın.", "Öğrenci kurgusal bir istek için kısa dilekçeyi klavyeyle doldursun; kişisel veri istenmesin."),
"z59": ("Bildiri panosu kurulsun; işaret seçimi cümlenin ANLAMINI nasıl değiştirdiği örnekleriyle gösterilsin ve seçilen işaretle cümle yeniden seslendirilsin.", "Aynı cümle farklı işaretlerle karşılaştırılsın; anlam farkı iki görselle gösterilsin.", "Öğrenci bir çocuk hakkını anlatan cümleyi uygun işaretle kendisi yazsın."),
"z60": ("Denge köprüsü gerçek görselle kurulsun: hak kalasları bir yandan, sorumluluk kalasları diğer yandan köprüyü dengede tutsun; simge eşleşmesi kaldırılsın ve yazılar sığsın.", "Bir hakka birden çok sorumluluğun bağlanabildiği örnekler eklensin.", "Öğrenci kendi yaşamından bir hak-sorumluluk çiftini cümleyle ifade etsin."),
"z61": ("Meclis kürsüsü sahnesi kurulsun; kurulan cümle mikrofonda sesli okunsun ve panoya oylamaya asılsın. Kartlar küçük harfle gelsin.", "Gerekçeli ve gerekçesiz görüş karşılaştırılsın; ilgili-ilgisiz neden ayrımı yapılsın.", "Öğrenci görüşünü ve nedenini iki cümleyle yazsın, sonra kürsüde sesli sunsun."),
"z62": ("Kalkan-yakalama mekaniği kaldırılsın; bilgi kartı sabit gelsin, öğrenci 'paylaşırım / paylaşmam' kararını gerekçe seçerek versin.", "Bağlama göre değişen örnekler eklensin: okul panosunda ad, internette adres; izin kavramı işlensin.", "Öğrenci dijital mahremiyet kuralını 'İnternette ... paylaşmam çünkü ...' kalıbıyla kendisi yazsın."),
"z63": ("Sahne gerçek sınıf seçimi olsun: sandık, oy pusulası ve aday panosu görünsün. Oy ifadesi sütun adını birebir tekrar etmesin (aday özelliğinden çıkarım gereksin) ve sayım çetele çizgisiyle görünsün.", "Berabere biten ve tek oyla kazanılan senaryolar eklensin; çoğunluk kavramı somutlaştırılsın.", "Öğrenci sonucu 'Seçimi ... kazandı, ... oy aldı; ikinci ... oyla ...' biçiminde yorumlayıp azınlığın hakkını bir cümleyle belirtsin."),
"z64": ("Karar basamakları gerçek meclis sürecini göstersin (sorun, öneri, tartışma, oylama, uygulama); basamak yazıları okunur kontrastta olsun ve bağlam ekranda sürekli dursun.", "Atlanan adımın sonucu gösterilsin: tartışmasız oylama neden sorunlu?", "Öğrenci sınıfında çözülecek bir sorun için karar adımlarını sırayla yazsın ve görüşünü nedeniyle belirtsin."),
}

assert set(DESIGNS) == {g["id"] for g in games}


def modality(game):
    out = game["kaz"]
    if "T.Y." in out:
        return "writing"
    if "T.K." in out:
        return "speaking"
    if "T.D." in out:
        return "listening"
    return "reading"


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
        return f"Kaynakta {n.get('customers','?')} müşteri/istek tanımlı; kart havuzu ve simgeler sabit."
    if t == "punctFix":
        return f"Kaynakta {n.get('rounds','?')} cümle ve işaret seti ({n.get('marks','')}) tanımlı; cümleler sabit sırayla geliyor."
    if t == "dragSlider":
        return f"Kaynakta {n.get('rounds','?')} tahmin turu var; beş sabit sayı seçeneğinden biri seçiliyor ve tahminin dayanacağı metin tanımlı değil."
    if t == "sentenceBuild":
        return f"Kaynakta {n.get('rounds','?')} cümle kurulumu var; her cümlenin tek doğru dizilişi tanımlı."
    if t == "wordHighlight":
        return f"Kaynakta tek metin üzerinde {n.get('rounds','?')} bulma adımı var; cevap sözcükleri önceden sabitlenmiş."
    if t == "orderSequence":
        return f"Kaynakta {n.get('items','?')} kartlık tek sıra var; doğru sıra sabit ve yeni olay turu üretilmiyor."
    if t == "dragMatch":
        return f"Kaynakta {n.get('sources','?')} parça ve {n.get('targets','?')} hedef var; tek sabit eşleştirme turu."
    if t == "typeWord":
        return f"Kaynakta {n.get('rounds','?')} dikte sözcüğü tanımlı; harf havuzu sözcüğün harflerinden üretiliyor."
    if t == "codeGrid":
        return f"Kaynakta {n.get('rounds','?')} görev haritası var; program yalnız yön oklarından oluşuyor, yazı üretimi yok."
    if t == "jumpPath":
        return f"Kaynakta {n.get('steps','?')} basamak adımı tanımlı; her adım tek doğru etiketle sabit."
    if t == "surveyChart":
        return f"Kaynakta {n.get('options','?')} aday ve {n.get('responses','?')} oy tanımlı; oy ifadeleri aday adını birebir içeriyor ve sonuç yorumu adımı tanımlı değil."
    return f"Kaynakta {n.get('columns','?')} sütun ve {n.get('responses','?')} yanıt tanımlı; yanıt cümleleri tür adını birebir içeriyor."


def modality_evidence(m):
    return {
        "writing": "Başarı kaydına öğrencinin ürettiği yazı, düzelttiği bölüm ve kullandığı kural eklenmeli; yalnız seçilen/dizilen kart kimliği yeterli değildir.",
        "speaking": "Başarı kaydına kısa ses üretimi veya öğretmen/öz değerlendirme rubriği eklenmeli; yalnız seçilen seçenek konuşma kanıtı değildir.",
        "listening": "Başarı kaydına ilk dinlemedeki yanıt, tekrar sayısı ve işitsel kanıt eklenmeli; yazılı ipucuyla verilen cevap ayrı tutulmalıdır.",
        "reading": "Başarı kaydına seçilen yanıtla birlikte metinde işaretlenen kanıt ve gerekçe eklenmelidir.",
    }[m]


GROUP_FOCUS = {
    "Tema 1 · Erdemler": ["Görüş bildirme ve ana fikir kazanımları gerekçe üretimine bağlanmalı; katılma kararı tek başına yeterli sayılmamalı.", "Yayınevi, atölye ve baskı makinesi başlıkları gerçek sahne olarak görünmeli; servis tezgâhındaki simge kopyası kaldırılmalı.", "Yazma kazanımlarında son turda serbest üretim zorunlu olmalı."],
    "Tema 2 · Millî Mücadele ve Atatürk": ["Tarihî içerik somut olmalı; kartlardaki tarihler ilk turda gizlenerek sıralama içerik bilgisine dayandırılmalı.", "Sesteş, eş ve zıt anlam görevlerinde simge eşleşmesi cevabı vermemeli; karar bağlam cümlesinden çıkmalı.", "Dikte oyununda hedef sözcük ekranda görünmemeli; mektup kazanımı gerçek yazı alanı içermeli."],
    "Tema 3 · Doğa ve İnsan": ["Doğa süreçleri gerçek şema ve görselle işlenmeli; adım kartları şemadaki yerine oturmalı.", "Yönerge yazma kazanımı ok dizmekten çıkarılıp gerçek yazılı yönergeye bağlanmalı.", "Tahmin görevleri metne dayanmalı; tren-tünel sahnesi ve sayı tahmini Türkçe kazanımının yerine geçmemeli."],
    "Tema 4 · Kütüphanemiz": ["Kütüphane, e-posta ve anket sahneleri gerçek nesnelerle kurulmalı; servis tezgâhı ve uzay şablonu kaldırılmalı.", "Kaynak güvenilirliği ölçütlerle sorgulanmalı; yakalama refleksi karara karışmamalı.", "Çetele kuralına uygun işleme ve tablo yorumu eklenmeli."],
    "Tema 5 · Kendimizi Geliştiriyoruz": ["Bağlaç, arasöz ve neden-sonuç görevleri anlam farkını gösteren karşılaştırmalarla çalışmalı.", "Sunum kazanımı gerçek konuşma üretimi ve beden dili-ses tonu rubriği içermeli.", "Düzeltme oyunlarında metin taşmamalı, büyüteç hedefi örtmemeli ve doğru biçim otomatik gelmemeli."],
    "Tema 6 · Bilim ve Teknoloji": ["de/da ve ki yazım kurallarında cümle tam görünmeli; kart kırpılması karar hatasına dönüşmemeli.", "Terim anlamı ve deney raporu görevleri gerçek bilimsel bağlamla desteklenmeli.", "Kodlama ve yönerge görevlerinde program yazılı yönerge cümlelerine dönüşmeli."],
    "Tema 7 · Geçmişten Geleceğe Mirasımız": ["Miras, şehir ve kuşak aktarımı harita ve gerçek görsel kanıtla sunulmalı.", "Köprü oyunlarında simge eşleşmesi kaldırılmalı; karar bilgi ve bağlamdan çıkmalı.", "Türkçe koruma ve pano görevleri gerçek yazı üretimiyle tamamlanmalı."],
    "Tema 8 · Demokratik Yaşam": ["Hak, sorumluluk ve özgürlük ayrımı üç kutulu bantta değil gerekçeli kararla kurulmalı.", "Dilekçe, bildiri ve meclis görevleri gerçek şablon ve gerçek yazı/konuşma üretimiyle çalışmalı.", "Seçim ve gizlilik görevleri hız oyunundan çıkarılıp veri yorumu ve gerekçe yapısına bağlanmalı."],
}

GROUP_COLORS = [CORAL, TEAL, PURPLE, GOLD, BLUE, GREEN, CORAL, PURPLE]

mod_counts = {"writing": 0, "speaking": 0, "listening": 0, "reading": 0}
for g in games:
    mod_counts[modality(g)] += 1

doc = BaseDocTemplate(
    str(OUT), pagesize=A4, rightMargin=MX, leftMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
    title="4. Sınıf Türkçe Oyunları - Ayrıntılı Düzeltmeler", author="Macera Akademi oyun incelemesi",
)
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

story = [Spacer(1, 14 * mm), P("MACERA AKADEMİ", cover_kicker),
         P("4. Sınıf Türkçe Oyunları<br/>Ayrıntılı Düzeltmeler", cover_title),
         P("64 oyunun kaynak görevleri çıkarılarak ve 15 oyun motoru 390x844 telefon görünümünde tek tek açılıp denenerek hazırlanmıştır.", cover_sub)]
cover_box = Table([[P("<b>Kapsam</b><br/>Bu belge z01-z64 arasındaki 4. sınıf Türkçe oyunlarının tamamını kapsar. Her oyun için denemede görülen mevcut yapı, eğitimsel risk, özgün sahne ve yeni oynanış, üç kademeli tur, geri bildirim ve ölçülebilir kabul koşulları ayrı ayrı verilir.")]], colWidths=[153 * mm])
cover_box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL), ("BOX", (0, 0), (-1, -1), 0.7, TEAL),
                               ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                               ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12)]))
story += [cover_box, Spacer(1, 8 * mm), P("İnceleme yöntemi", h2)]
story += bullets(["4. sınıf profili üzerinden Türkçe listesindeki 64 oyunun kaynak yapılandırmaları çıkarıldı ve sekiz tema karşılaştırıldı.",
                  "Bant, servis, tamirhane, matbaa, radar, roket, köprü, hafıza, dedektif, sırık, kargo, daktilo, tren ve çetele (anket sürümü dâhil) motorları 390x844 telefon görünümünde açıldı; kart akışı, sürükleme, dokunma alanları ve yerleşim denendi.",
                  "Düzeltmeler başlık-sahne uyumu, cevabı sızdıran arayüz ögeleri, yerleşim/kırpılma hataları, okuma/dinleme/yazma/konuşma geçerliliği, üç kademeli tur ve test edilebilir kabul koşulunu birlikte ele alır."])
story += [PageBreak()]

story += [P("Testten çıkan öncelikli bulgular", h1)]
story += [box("1. Simge eşleşmesi birçok oyunda cevabı doğrudan veriyor", ["Sesteş Köprüsü'nde her parça ve her hedef aynı anlamı gösteren simgeyle işaretli (100 simgesi ↔ 'Sayı: 100', gül ↔ 'Bir çiçek', güneş ↔ 'Bir mevsim'); çocuk tek bir cümle okumadan simge eşleyerek bitirebiliyor. Aynı kusur Yayınevi Masası'nda da var: balondaki aday cümleler tepsi kartlarıyla birebir aynı simgelerle önden etiketlenmiş."], PALE_CORAL, CORAL), Spacer(1, 1.7 * mm)]
story += [box("2. Yazım kuralı oyunlarında karar verilecek cümle ekranda okunamıyor", ["'de/da' Denetim Bandı'nda cümle kartı bandın sol kenarında tamamen kırpıldı; kararın dayanacağı cümle görünmüyordu. '“ki” Düzeltme Kalemi'nde soru başlığı iki yandan kesildi, metin panelden taşıp alttaki kutunun başlığıyla üst üste bindi ve büyüteç tam da karar verilecek sözcüğün üzerini örttü."], PALE_GOLD, GOLD), Spacer(1, 1.7 * mm)]
story += [box("3. Noktalama oyunlarının görev metni kuralı ve işaretin yerini söylüyor", ["Deney Raporu Dizgisi'nde görev satırı 'Malzemeler sıralanıyor: açıklamadan önce iki nokta, arasına virgül.' diyor; Üç Nokta ve Konuşma Çizgisi'nde 'Konuşma çizgisi (—) konuşan kişinin sözünden önce gelir.' yazıyor. Üstteki yönerge de kullanılacak işaretlerin adını sayıyor ve 'Kalan: ... işaret' sayacı kaç hamle kaldığını veriyor."], PALE_BLUE, BLUE), Spacer(1, 1.7 * mm)]
story += [box(f"4. {mod_counts['writing']} yazma ve {mod_counts['speaking']} konuşma kazanımında gerçek üretim yok", ["Yazma hedefli oyunlar kart dizme, dokunma ve sürüklemeden oluşuyor; serbest yazı alanı hiçbirinde yok. 'Ayrıntılı yönerge yazar' kazanımındaki iki kargo oyununda yalnız yön oku diziliyor. Sunum kazanımında öğrenci ses üretmiyor; dikte oyununda hedef sözcük ekranda yazılı görünüyor."], PALE_TEAL, TEAL), Spacer(1, 1.7 * mm)]
story += [box("5. Sahne başlıkla çelişiyor; teknik çökme görülmedi", ["Tasarruf Ölçer'de su tüketimi sorulurken kırmızı bir tren tünellere giriyor ve sayaç '0/3 tren' yazıyor; görev tamamen sayı tahminine indirgenmiş, kazanımın dayandığı metin ekranda yok. Sınıf Seçimi 'ÇETELE TABLOSU' başlığıyla açılıyor ama gelen oy ('Ela') sütun adıyla birebir aynı ve sayım çetele çizgisi yerine rakamla ilerliyor. z01-z64 arasındaki 64 oyunun tamamı yüklendi; motorlarda çökme veya konsol hatası oluşmadı."], PALE_PURPLE, PURPLE)]
story += [PageBreak()]

story += [P("Bütün 4. sınıf Türkçe oyunlarında ortak uygulama standardı", h1)]
rows = [
    [P("Sahne", box_title), P("Başlıktaki yayınevi, kütüphane, müze, laboratuvar, meclis veya atölye gerçek görsel ve oyun eylemi olarak kullanılmalı; ortak bant/uzay/tren/servis şablonu kaldırılmalı.", small)],
    [P("Cevap sızdırmama", box_title), P("Parça ile hedefi eşleyen simgeler, işaret adını ve yerini söyleyen görev metni, yazılı dikte sözcüğü, tarih sırası ve sütun adını tekrarlayan yanıt gibi cevabı taşıyan hiçbir öge bulunmamalı.", small)],
    [P("Yerleşim", box_title), P("390x844 ekranda hiçbir metin kırpılmamalı, taşmamalı, üst üste binmemeli; karar verilecek cümle tam görünmeli ve dokunma alanları en az 44 px olmalı.", small)],
    [P("Okuma", box_title), P("Metin sabit, okunabilir ve örtüsüz olmalı; öğrenci cevaptan önce metindeki kanıtı işaretlemeli.", small)],
    [P("Dinleme", box_title), P("İlk işitsel turda cevap yazısı gizli olmalı; tekrar dinleme cezasız ve sayısı kaydedilebilir olmalı.", small)],
    [P("Yazma", box_title), P("Yazma kazanımı son turda gerçek sözcük/cümle/yönerge/metin üretimi içermeli; kart dizmek tek başına başarı sayılmamalı.", small)],
    [P("Konuşma", box_title), P("Sunum, görüş bildirme ve anlatma hedeflerinde kısa ses üretimi ya da beden dili-ses tonu rubriği bulunmalı.", small)],
    [P("Tur ve yanlış", box_title), P("Her oyun en az üç kademeli tur içermeli; içerik her açılışta değişmeli. Yanlışta doğru cevap açılmamalı; motor/refleks hatası can kaybettirmemeli.", small)],
]
standards = Table(rows, colWidths=[28 * mm, 148 * mm])
standards.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8D4E2")), ("BACKGROUND", (0, 0), (0, -1), PALE_PURPLE),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
story += [standards, Spacer(1, 4 * mm)]
story += bullets(["Kartlar ve metinler ilk iki turda hareket etmeyecek; hız ancak doğruluk eşiğinden sonra isteğe bağlı akıcılık ölçütü olacak.",
                  "Ses, yazı, görsel, doğru cevap ve geri bildirim Türkçe karakterler dâhil birebir tutarlı olacak; web ve APK aynı davranacak.",
                  "Bir oyun yalnız tek sabit soru/kart havuzunu bitirdi diye tamamlanmış sayılmayacak."])
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
        story += [Spacer(1, 5 * mm), box("Bölüm kabul eşiği", ["Bu bölümdeki her oyun üç kademeli tur ve en az bir öğrenci üretimi/gerekçesi olmadan tamamlanmış sayılmayacak.", "Başlık, görünen sahne, seslendirme, kontrol ve ölçülen Türkçe becerisi aynı hedefi gösterecek."], PALE_TEAL, TEAL), PageBreak()]

    scene, level2, level3 = DESIGNS[game["id"]]
    m = modality(game)
    engine_name, engine_obs = ENGINE[game["type"]]
    instruction = clean(game["instruction"])
    observed = [
        f"Kaynak yönerge: “{instruction}” Gerçek ekranda görev <b>{engine_name}</b> ortak motorunda açılıyor. {engine_obs}",
        config_summary(game),
    ]
    risk = [TYPE_RISK[game["type"]], MODALITY_RISK[m], "Mevcut içerik aynı sabit örneklerle tekrarlandığı için çocuk cevabı/konumu ezberleyebilir; beceriyi yeni metin ve bağlama aktardığı gösterilemez."]
    new_play = [scene, level2, level3, MODALITY_NEW[m], modality_evidence(m)]
    rounds = [
        "Destekli: mevcut kazanım tek açık örnekle çalışılır; metin/ses kanıtı görünür, kartlar sabit, süre ve can cezası kapalıdır.",
        level2,
        level3,
    ]
    feedback = [TYPE_FEEDBACK[game["type"]], "Doğru yanıtta yalnız puan/konfeti değil; seçilen metin veya ses kanıtı ile kural kısa biçimde görünür olmalı.", "Bitiş ekranı üç turdaki doğruluk, ipucu/tekrar kullanımı ve öğrencinin ürettiği gerekçe/yazı/konuşma kanıtını ayrı göstermeli."]
    acceptance = [TYPE_ACCEPT[game["type"]], f"Başlıktaki sahne ve eylem gerçekten uygulanacak: {scene}", "En az üç farklı içerik turu ve her turda yeni örnek bulunacak; seçenek konumu ve doğru yanıt sırası değişecek.", modality_evidence(m)]

    accent = accent_cycle[(number - 1) % len(accent_cycle)]
    story += [header(number, game["title"], f"{game['id']} · {game['sub']} · {clean(game['kaz'])}", accent), Spacer(1, 1.8 * mm)]
    story += [box("Denemede görülen mevcut durum", observed, PALE_CORAL, CORAL), Spacer(1, 0.8 * mm)]
    story += [box("Eğitimsel risk", risk, PALE_GOLD, GOLD), Spacer(1, 0.7 * mm)]
    story += [P("Yeni sahne ve oynanış", h2)] + bullets(new_play, bullet_small)
    story += [P("Üç kademeli tur", h2), rounds_table(rounds), Spacer(1, 0.7 * mm)]
    story += [box("Geri bildirim ve bitiş", feedback, PALE_TEAL, TEAL), Spacer(1, 0.7 * mm)]
    story += [box("Kabul ölçütü", acceptance, PALE_BLUE, BLUE), PageBreak()]

story += [P("Son kabul kontrolü", h1), P("4. sınıf Türkçe bölümü tamamlanmadan önce", h2)]
story += bullets(["z01-z64 arasındaki 64 oyun üç kademeli turla baştan sona test edilir; görünen başlık, sahne, kontrol, ses ve hedef beceri kayıt altına alınır.",
                  "Köprü ve servis oyunlarında parça-hedef simge eşleşmesi kaldırılır; karar yalnız cümle, bağlam ve bilgi kanıtından çıkar.",
                  "de/da ve ki denetim oyunlarında karar verilecek cümle ekranda tam görünür; kart hiçbir kenarda kırpılmaz.",
                  "Noktalama oyunlarının görev metni kuralı ve işaretin yerini söylemez; 'Kalan' sayacı ilk turdan sonra kapanır.",
                  f"{mod_counts['writing']} yazma kazanımında son tur gerçek yazı üretimi içerir; kart dizmek tek başına yazma başarısı sayılmaz.",
                  "Tasarruf Ölçer metne dayanan bir tahmine, Sınıf Seçimi ise gerçek çetele ve sonuç yorumuna dönüştürülür.",
                  "Her oyunda en az üç farklı içerik örneği, değişen seçenek sırası, açıklayıcı yanlış geri bildirimi ve ölçülebilir kabul kaydı bulunur; web ile APK birebir aynı davranır."])
story += [Spacer(1, 4 * mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 4. sınıf Türkçe listesindeki z01-z64 oyunlarını kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, metin/ses, mekanik, üç tur, geri bildirim, öğrenci kanıtı ve test gereksinimlerini ayrıntılı biçimde tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)

reader = PdfReader(str(OUT))
print({"pages": len(reader.pages), "games": len(games), "modalities": mod_counts, "bytes": OUT.stat().st_size, "output": str(OUT)})
