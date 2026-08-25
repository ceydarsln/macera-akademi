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
OUT = ROOT / "output/pdf/3_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf"
GAMES_JSON = ROOT / "tmp/pdfs/turkish3_games.json"
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
    """Satır yüksekliği sabitlenmiyor: 3. sınıf kazanım metinleri üç satıra
       taşabildiği için kutu içeriğe göre büyüyor, yazı dışarı düşmüyor."""
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
    canv.drawString(MX, 8.2 * mm, "3. Sınıf Türkçe - Ayrıntılı Oyun Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 8.2 * mm, str(canv.getPageNumber()))
    canv.restoreState()


ENGINE = {
    "beltSort": ("bant (yürüyen bant) motoru", "Başlıktaki stüdyo, laboratuvar veya adalet sahnesi yerine karanlık fabrika bandı görünüyor; kart banttan akarken ekran kenarında kırpılabiliyor ve okuma süresi bant hızına bağlı kalıyor."),
    "memoryPairs": ("hafıza kartı motoru", "Sahne başlıktan bağımsız yıldızlı uzay; kartlar tavandan iniyor ve 'Başla! Kartları çevir' yazısı üst kart sırasının üzerine biniyor. Can göstergesi 6 kalp ile genel 3 can standardından ayrılıyor."),
    "catchDrop": ("radar/kapsül yakalama motoru", "Seçenekler kapsül içinde tek tek yukarıdan düşüyor; ipucu 'Kapsülün altındaki sarı noktayı çanağın ortasına getir' diliyle veriliyor ve karar süresi düşme hızına bağlanıyor."),
    "serveOrder": ("tepsi-servis motoru", "Başlıktaki yayınevi, kütüphane, müze veya dilekçe masası yerine ahşap servis tezgâhı açılıyor; müşteri balonundaki simgeler tepsideki kart simgeleriyle birebir aynı olduğundan görev simge kopyalamaya dönüşebiliyor."),
    "punctFix": ("tamirhane motoru", "Tezgâh ve işaret sandığı düzeni işlevsel; ancak görev metni ile 'Kalan: ... büyük harf · ... işaret' satırı üst üste binebiliyor ve yönerge kimi turda doğru işaretin adını baştan söylüyor."),
    "dragSlider": ("tren-tünel motoru", "Ses ve gürültü oyunlarında bile kırmızı bir tren dört tünelden birine giriyor; sayaç '0/4 tren' yazıyor ve hiçbir düzeyde gerçek ses örneği dinletilmiyor."),
    "sentenceBuild": ("matbaa/baskı kızağı motoru", "Kelime kartlarından büyük harfle başlayan kart ilk sözcüğü, nokta kartı son konumu ele veriyor; makine yalnız tek sabit dizilişi kabul ediyor."),
    "wordHighlight": ("dedektif tutanağı motoru", "Denemede soru başlığı iki yandan kırpıldı, metin tutanak panelinden taşarak alttaki kutunun başlığıyla üst üste bindi ve büyüteç görseli sözcüğün üzerini örttü."),
    "orderSequence": ("roket-yakıt motoru", "Zaman şeridi, kitap, döngü ve tören başlıklarında bile kartlar uzayda süzülüyor, seçilenler YAKIT hunisine gidiyor; kenardaki kartlar ekrandan taşabiliyor."),
    "dragMatch": ("eşleştirme köprüsü motoru", "Köprü görseli yok; hedef satırların solunda küçük boş kareler, altta PARÇALAR havuzu var. Uzun cümleler parça çiplerine sığmayıp taşıyor ve alttaki yazılarla üst üste biniyor."),
    "typeWord": ("daktilo motoru", "Daktilo kâğıdı ve harf tuşları yerinde; ancak dikte edilen hedef sözcük tilkinin konuşma balonunda yazılı olarak da görünüyor ve harf havuzunun ilk harfleri sözcüğün sırasını izliyor."),
    "codeGrid": ("kargo/robot ızgara motoru", "Izgara, engel ve hedef okunaklı; fakat 'ayrıntılı yönerge yaz' hedefine karşılık yalnız yön okları dizilebiliyor; ekranda hiçbir yazılı yönerge üretilmiyor ve görev sayısı 2-3'te kalıyor."),
    "jumpPath": ("sırık/basamak motoru", "Basamak yazıları koyu yeşil zeminde düşük kontrastta kalıyor; hangi ifadenin doğru olduğunu belirleyecek bağlam cümlesi ekranda görünmüyor, seçim sesli yönergeye ve tahmine kalıyor."),
    "tallyChart": ("çetele motoru", "Arkadaş balonundaki cümle sütun adını birebir içeriyor ('Ben masal severim' → MASAL); sütun altlarında çetele çizgisi yerine rakam sayacı artıyor."),
}

TYPE_RISK = {
    "beltSort": "Bant hızı okuma ve karar süresine karışıyor; kart okunmadan kutu seçilebiliyor, kenarda kırpılan kart ise hiç okunamadan puan/can etkiliyor.",
    "memoryPairs": "Eşleştirme, kavramı açıklamadan kart konumunu ezberleyerek de çözülür; görsel hafıza başarısı dil bilgisi başarısı gibi kayda geçer.",
    "catchDrop": "Doğru cevabı bilmek yetmiyor; düşen kapsüle yetişmek gerekiyor. Yanlış motor hareketi yanlış dil kararı gibi can kaybettiriyor.",
    "serveOrder": "Balondaki simge ile karttaki simge birebir eşleştiğinde öğrenci içeriği hiç okumadan simge kopyalayarak görevi bitirebilir.",
    "punctFix": "Yönergenin doğru işareti söylemesi ve 'Kalan' sayacı, kuralı düşünmek yerine deneme-yanılma ve eleme stratejisini ödüllendirir.",
    "dragSlider": "Ses düzeyi/gürültü kararı hiçbir gerçek ses duymadan verildiği için ölçülen şey işitsel farkındalık değil, etiket bilgisidir.",
    "sentenceBuild": "Büyük harfli kart ve nokta kartı dizilişi ele verir; ayrıca Türkçenin kurallı alternatif dizilişleri yanlış sayılırsa doğru dil sezgisi cezalandırılır.",
    "wordHighlight": "Kırpılan soru ve taşan metin cevabı rastlantıya bırakır; sözcüğü bulmak, görevini veya anlamını açıklama kanıtı üretmez.",
    "orderSequence": "Kartlardaki tarih ve numara ipuçları, içerik bilgisi olmadan sayı sıralamayla çözümü verir; roket-yakıt sahnesi başlıkla çelişip kavramı bulanıklaştırır.",
    "dragMatch": "Az sayıda hedefle deneme-yanılma hızla doğruya ulaşır; taşan yazılar okunamadığından eşleştirme gerekçesiz kalır.",
    "typeWord": "Hedef sözcük ekranda yazılı olduğundan dikte, dinleme-yazma yerine bakarak kopyalamaya dönüşür; harf havuzu sırayı ele verir.",
    "codeGrid": "Kazanım 'ayrıntılı yönerge yazar' olduğu hâlde öğrenci hiçbir sözlü/yazılı yönerge üretmez; ok dizmek yön kavramını ölçer, yazmayı ölçmez.",
    "jumpPath": "Bağlam cümlesi ekranda olmadığından seçim tahmine döner; düşük kontrastlı basamak yazıları okunamadan zıplanabilir.",
    "tallyChart": "Cümledeki sözcük sütun adıyla birebir aynı olduğundan görev sözcük kopyalamaya iner; rakam sayacı çetele kuralını (beşinci çizgi dördü keser) hiç göstermez.",
}

TYPE_FEEDBACK = {
    "beltSort": "Yanlış kutuda bant dursun; kart sabitlenip yeniden okunsun ve ölçüt (neden bu kutu değil) doğru söylenmeden hatırlatılsın. Kenarda kırpılan kart hiç puanlanmasın.",
    "memoryPairs": "Yanlış çiftte kartlar hemen kapanmasın; iki içerik yan yana sesli okunup farkı soran kısa bir ipucu verilsin. Can standardı diğer oyunlarla eşitlensin.",
    "catchDrop": "Yanlış yakalamada düşme dursun; seçenek sabitlenip metin/ses kanıtıyla yeniden karar verilsin. Kaçan kapsül can yakmasın, yalnız yeniden denensin.",
    "serveOrder": "Yanlış kartta tepsi kilitlenmesin; istek metni yeniden okunsun ve kartın neden uymadığı içerik üzerinden gösterilsin, simge üzerinden değil.",
    "punctFix": "Yanlış işarette cümle uygun tonlamayla seslendirilsin ve işaretin görevi hatırlatılsın; doğru işaret adı söylenmesin, 'Kalan' sayacı ipucu vermesin.",
    "dragSlider": "Yanlış düzey seçildiğinde o düzeyin gerçek ses örneği dinletilsin; doğru düzeyle kulaktan karşılaştırma yapılsın.",
    "sentenceBuild": "Yanlışta bütün dizi bozulmasın; yalnız son kart geri alınsın. Kurallı alternatif diziliş kurulduysa doğru kabul edilsin ve fark açıklansın.",
    "wordHighlight": "Yanlış sözcükte metin kaybolmasın; soru ile seçilen sözcük yan yana okunup ilişki karşılaştırılsın. Büyüteç hiçbir zaman hedefi örtmesin.",
    "orderSequence": "Yanlış adımda dizi silinmesin; yalnız son seçim geri alınsın ve 'önce/sonra' ilişkisini düşündüren ipucu verilsin.",
    "dragMatch": "Yanlış parça başlangıca dönsün; hedef parlatılmasın. Eşleşmenin dayandığı sözcük/bağlam ipucu kısa bir soruyla vurgulansın.",
    "typeWord": "Yanlış harfte doğru harf gösterilmesin; sözcük yeniden dinletilsin ve gerekirse hece hece söylensin. Tekrar dinleme hiçbir turda ceza olmasın.",
    "codeGrid": "Engele çarpınca robot dursun ve programdaki hatalı adım işaretlensin; tüm program silinmesin, yalnız hatalı adımdan itibaren düzeltilsin.",
    "jumpPath": "Yanlış basamakta düşme animasyonu ceza üretmesin; bağlam cümlesi yeniden gösterilip iki seçenek yan yana karşılaştırılsın.",
    "tallyChart": "Yanlış satırda cevap cümlesi yeniden dinletilsin; tür ile cümledeki ipucu arasındaki ilişki soruyla kurulsun, doğru satır parlatılmasın.",
}

TYPE_ACCEPT = {
    "beltSort": "İlk iki turda kartlar sabit gelecek; hız ancak üçüncü turda isteğe bağlı açılacak. Kart hiçbir konumda kırpılmayacak ve en az 44 px dokunma alanı korunacak.",
    "memoryPairs": "Kart konumları ve içerik her açılışta karışacak; can sayısı genel standartla (3) eşitlenecek ve her eşleşme en az bir gerekçe adımıyla doğrulanacak.",
    "catchDrop": "İlk turda düşme kapalı, seçenekler sabit olacak; başarı doğru karar + kanıt ile ölçülecek, yakalama refleksi puana karışmayacak.",
    "serveOrder": "Kartlarda etiket/simge değil içerik yazacak; balon simgesi ile kart simgesi eşleşerek cevabı vermeyecek ve her müşteri farklı içerik havuzu kullanacak.",
    "punctFix": "Yönerge işaret adını söylemeyecek; 'Kalan' sayacı ilk turdan sonra kapanacak; görev metni ile sayaç hiçbir çözünürlükte üst üste binmeyecek.",
    "dragSlider": "Tren-tünel sahnesi kaldırılacak; her düzey gerçek ses örneğiyle doğrulanacak ve başarı kaydına dinleme/üretim kanıtı eklenecek.",
    "sentenceBuild": "Kartlar küçük harfle gelecek; baş harf ve son işaret öğrencinin ayrı kararı olacak. Kurallı alternatif dizilişler kabul edilecek ve son turda serbest yazı alanı bulunacak.",
    "wordHighlight": "Metin panelden taşmayacak, soru tam görünecek, büyüteç veya başka öge sözcüğü örtmeyecek; çok sözcüklü cevaplar tek anlam birimi olarak seçilebilecek.",
    "orderSequence": "Roket-yakıt sahnesi kaldırılacak; sırayı ele veren tarih/numara ilk turda gizlenecek ve kartlar 390x844 ekranda tam içeride kalacak.",
    "dragMatch": "Parça yazıları çipe sığacak ve taşmayacak; hedef alanlar en az 44 px olacak; her eşleşme bir gerekçe sorusuyla doğrulanacak.",
    "typeWord": "Hedef sözcük ekranın hiçbir yerinde yazılı görünmeyecek; harf havuzu karışık dizilecek; tekrar dinleme cezasız olacak ve sayısı kaydedilecek.",
    "codeGrid": "Yön blokları yazılı yönerge kartlarına dönüşecek ve program cümle olarak okunacak; en az üç görev bulunacak; son görevde öğrenci yönergeyi kendisi yazacak.",
    "jumpPath": "Basamak yazıları zeminden ayrışan kontrastta olacak; karar bağlamı (cümle/hikâye) ekranda sürekli duracak; düşme animasyonu ceza üretmeyecek.",
    "tallyChart": "Cevap cümleleri tür adını birebir söylemeyecek; işaretler çetele çizgisiyle birikecek, beşinci çizgi dördünü kesecek ve bitişte tablo yorum sorusu sorulacak.",
}

MODALITY_RISK = {
    "writing": "Kazanım yazma/oluşturma istediği hâlde mevcut yapıda serbest sözcük, cümle veya metin üretme alanı yok; hazır kartı seçmek ya da dizmek gerçek yazma kanıtı değildir.",
    "speaking": "Kazanım konuşma istediği hâlde öğrenci ses üretmiyor; yalnız seçenek işaretlendiği için vurgu, tonlama, ses düzeyi ve uygun ifade gözlenemiyor.",
    "listening": "Dinleme hedefinde yazılı yönerge ve seçenekler cevabı taşıyabiliyor; ses kapatıldığında da oyun çözülebiliyorsa ölçme geçerli değildir.",
    "reading": "Okuma hedefi, metindeki kanıtı kullanmaktan çok görsel olarak en belirgin seçeneği bulmaya indirgenirse çıkarım ve anlama ölçülmez.",
}

MODALITY_NEW = {
    "writing": "Son turda öğrenci gerçek bir sözcük, cümle, yönerge veya form alanı üretsin; harf/kelime kartları yalnız erişim desteği olsun ve hazır kart seçimi tek başına başarı sayılmasın.",
    "speaking": "Örnek dinletildikten sonra öğrenci kısa bir ses kaydı alsın veya yetişkin/öz değerlendirme rubriğiyle konuşsun; ses düzeyi, vurgu, uygun hitap ve anlaşılabilirlik ayrı kaydedilsin.",
    "listening": "İlk dinleme turunda hedef metin ve cevap anahtarı görünmesin; ses en az iki kez tekrar edilebilsin ve tekrar dinleme ceza oluşturmasın.",
    "reading": "Öğrenci cevaptan önce metindeki görsel/sözel kanıtı işaretlesin; doğru seçenek ancak kanıtla tutarlı olduğunda kabul edilsin.",
}


DESIGNS = {
"y01": ("Gerçek kayıt stüdyosu kur: mikrofon, kayıt lambası ve konuşan-dinleyen iki karakter görünsün; davranışlar yazı kartı yerine kısa canlandırma sahnesi olarak gelsin ve sabit dursun.", "Davranış sahnelerine yakın çeldiriciler eklensin (söz almak için el kaldırmak / konuşanın sözünü iyi niyetle tamamlamak); öğrenci kararını sahnedeki kanıtla doğrulasın.", "Öğrenci hatalı davranış için uygun düzeltmeyi seçsin ve 'söz almak için ne yapmalıydı?' sorusunu kendi cümlesiyle söylesin veya yazsın."),
"y02": ("Kâşif çadırı ve hazine sandıkları sahnesi kur; kartlar sandıklardan çıksın, eşleşen erdem-davranış çifti yan yana sesli okunsun ve 'Başla' yazısı kartların üzerine binmesin.", "Yakın erdem çeldiricileri kullanılsın (yardımseverlik/cömertlik, dürüstlük/cesaret); öğrenci eşleşmeyi davranıştaki kanıt sözcükle doğrulasın.", "Öğrenci seçtiği erdem için kendi yaşamından bir davranış örneğini bir cümleyle söylesin veya yazsın."),
"y03": ("Kâhin çadırında küre sabit dursun; başlık ve kapak görseli birlikte gösterilsin, tahmin seçenekleri düşen kapsül yerine kürenin içinde sabit belirsin.", "İki makul tahminden başlık ve görsel kanıtına uyan seçilsin; öğrenci hangi ipucunu kullandığını işaretlesin.", "Tahminden sonra metnin ilgili bölümü açılıp tahmin doğrulansın; öğrenci 'Bence ... çünkü başlıkta ...' kalıbıyla tahmin cümlesi kursun."),
"y04": ("Gerçek editör masası çiz: metin ayrı panelde okunur dursun, tepsi kartlarında KONU/ANA FİKİR etiketi değil aday cümlelerin kendisi yazsın; balondaki simge kopyası kaldırılsın.", "Konu, ana fikir ve ayrıntı aday cümleleri yakın çeldiricilerle verilsin; öğrenci her kartı okuyup türünü kendisi belirlesin.", "Öğrenci yeni bir kısa metnin ana fikrini hazır kart olmadan kendi cümlesiyle yazsın ve metinden bir kanıt işaretlesin."),
"y05": ("Tamirhane tezgâhı gerçek atölye görseliyle kurulsun; görev metni ile 'Kalan' satırı ayrı satırlarda dursun ve yönerge doğru işaretin adını söylemesin ('uygun işareti koy' densin).", "Soru ve ünlem cümleleri tonlamalı seslendirmeyle ayırt edilsin; öğrenci işareti sese göre seçsin.", "Öğrenci iki bozuk cümleyi ekran klavyesiyle baştan doğru yazsın; büyük harf ve işaret kararları kayda geçsin."),
"y06": ("Tren-tünel sahnesi kaldırılsın; gerçek ortam görseli (kütüphane, bahçe, sınıf) ve ses düğmesi kullanılsın. Seçilen düzeyde örnek konuşma GERÇEKTEN o ses düzeyinde dinletilsin.", "Aynı ortamda farklı durumlar karşılaştırılsın: kütüphanede arkadaşa fısıltı, bahçede oyun sesi, sınıfta sunum sesi.", "Öğrenci aynı cümleyi seçtiği ses düzeyinde söyleyip kaydetsin; kayıt örnekle karşılaştırılarak öz değerlendirme yapılsın."),
"y07": ("Baskı makinesi gerçekten çalışsın: kurulan cümle baskıdan çıkıp panoya asılsın. Kartlar küçük harfle gelsin; baş harfi büyütme ve son işareti koyma öğrencinin ayrı kararı olsun.", "Beş-altı kartlık cümlede kurallı alternatif dizilişler kabul edilsin; araya anlamı bozan bir çeldirici sözcük eklensin.", "Öğrenci aynı sözcüklerden en az birini kullanarak kendi cümlesini ekran klavyesiyle yazsın."),
"y08": ("Tutanak paneli metni taşırmadan gösterilsin; soru başlığı tam okunsun, büyüteç kaldırılsın ya da yalnız kenarlıkta dursun; ikinci metin kutusu ayrı sayfada açılsın.", "Erdem sözcüğü bulunduktan sonra o erdemi gösteren kanıt cümlesi de işaretlensin.", "Öğrenci metnin ana duygusunu ve iki kanıtını 'Metinde ... hissettim çünkü ...' kalıbıyla söylesin veya yazsın."),
"y09": ("Roket ve YAKIT hunisi kaldırılsın; ekranda gerçek yatay zaman şeridi dursun. İlk turda kartlardaki tarihler gizlensin; sıralama olay metninden yapılsın, doğrulamada tarihler açılsın.", "Tarihi gizli yeni bir olay seti dinletilsin; öğrenci yalnız dinlediği bilgiyle sıralasın.", "Öğrenci sıraladığı olayları 'önce / daha sonra / en sonunda' bağlarıyla üç cümlede anlatsın."),
"y10": ("Ayna odası gerçek görselle kurulsun; kart açılınca sözcük seslendirilsin ve eşleşen zıt çift aynanın iki yüzünde yan yana gösterilsin.", "Bağlama duyarlı zıt çiftler eklensin (erken-geç, inmek-binmek); iki çiftin karışabildiği çeldirici düzen kullanılsın.", "Öğrenci bir zıt çifti aynı cümle içinde kullanarak karşılaştırma cümlesi kursun."),
"y11": ("Yazı denetim masası kur: kısaltma kartı sabit dursun, bant akışı kaldırılsın; kesme işareti ve ek renklendirilerek gösterilsin, kural kutusu ekranda kalsın.", "Okunuşa göre ek seçimi çalışılsın: TDK'ye, TRT'yle, cm'ye gibi örneklerde yanlış yazımlar çeldirici olsun.", "Öğrenci iki kısaltmaya gelen eki ekran klavyesiyle kendisi yazsın; kesme işaretini kendisi koysun."),
"y12": ("Gerçek köprü görseli kurulsun: sol kıyı neden, sağ kıyı sonuç; her doğru eşleşme köprüye kalas eklesin ve parça yazıları çipe sığsın.", "Aynı ilişki 'çünkü' ve 'bu yüzden' bağlarıyla iki yönde kurulsun; öğrenci bağı kendisi seçsin.", "Öğrenci Kurtuluş Savaşı'ndan öğrendiği bir olay için kendi neden-sonuç cümlesini kursun."),
"y13": ("Tarih kitabı sayfası gerçek dizgi görseliyle açılsın; özel ad türleri (kişi, yer, bayram, kurum) ayrı renk kodlarıyla çalışılsın.", "Karışık kategorili cümleler verilsin; cins isim çeldiricileri eklensin (ay adı 'mayıs' cümle içinde / 'Mayıs' tarih olarak).", "Öğrenci iki cümleyi ekran klavyesiyle baştan yazsın; büyük harf kararlarını bağımsız versin."),
"y14": ("Tilkinin balonunda hedef sözcük YAZILMASIN; yalnız 'Dinle düğmesine bas' yönergesi görünsün. Harf havuzu karışık dizilsin ve sözcüğün harf sırasını ele vermesin.", "Benzer sesli harflerle çeldirici kurulsun (c/ç, s/ş, g/ğ); sözcük iki kez dinletilip hece hece tekrar seçeneği sunulsun.", "Öğrenci yazdığı sözcüğü kısa bir cümle içinde kullansın; cümle diktesiyle tur tamamlansın."),
"y15": ("Radar-kapsül düzeni kaldırılsın; bilgi kartları panoda sabit dursun, her kartın yanında 'kaynağı gör' düğmesi olsun ve doğruluk kararı kanıtla verilsin.", "Kısmen doğru ama eksik ifadeler eklensin; öğrenci 'tamamen doğru / kısmen doğru / yanlış' ayrımı yapsın.", "Öğrenci yanlış bilgiyi doğru biçimiyle kendi cümlesinde söylesin veya yazsın."),
"y16": ("Gerçek bayram panosu sahnesi kurulsun; kurulan mesaj panoya asılıp sesli okunsun. Kartlar küçük harfle gelsin, işaret kararı öğrencide olsun.", "Hitap ve noktalama birlikte çalışılsın: 'Sevgili öğretmenim,' hitabından sonra virgül, kutlama cümlesinde ünlem.", "Öğrenci kendi bayram mesajını ekran klavyesiyle yazsın; mesaj panoda diğerlerinin yanına asılsın."),
"y17": ("Doğa istasyonu gerçek doğa görseliyle kurulsun; varlıklar fotoğraf/çizim olarak sabit gelsin, kart kenarda kırpılmasın.", "Ham-işlenmiş çeldiriciler eklensin: pamuk doğal, tişört yapay; süt doğal, peynir işlenmiş - ölçüt tartışması açılsın.", "Öğrenci yeni bir varlık ekleyip hangi kutuya neden koyduğunu bir cümleyle açıklasın."),
"y18": ("Yön okları yazılı yönerge kartlarına dönüşsün ('iki adım ileri git', 'sağa dön'); dizilen program panelde cümle olarak okunsun ve robot okurken uygulasın.", "Engeller değişsin ve daha uzun yönerge istensin; öğrenci hatalı bir programı okuyup hatayı bulsun.", "Öğrenci deprem çantasına giden yönergeyi sözcük kartları veya klavyeyle kendisi yazsın; robot yazılanı uygulasın."),
"y19": ("Dergi masası gerçek sayfa taslağıyla kurulsun; plan bölümleri (başlık, giriş, gelişme, sonuç, görsel) tepsiye değil taslak sayfadaki yerlerine yerleşsin.", "Bölüm adı ile bölüm içeriği eşleştirilsin: 'giriş' kartına uygun cümle seçilsin.", "Öğrenci verilen konu için üç maddelik kendi yazı planını kısa ifadelerle yazsın."),
"y20": ("Orman sahnesi ağaç kovuklarıyla kurulsun; kartlar kovuklardan çıksın ve eşleşen eş anlamlı çift aynı cümle içinde iki kez okunarak doğrulansın.", "Her cümlede birebir değiştirilemeyen eş anlamlılar karşılaştırılsın (ak-beyaz her bağlamda değişmez).", "Öğrenci bir eş anlamlı çiftin iki üyesiyle ayrı cümleler kurup anlamın korunduğunu kontrol etsin."),
"y21": ("Doğa günlüğü gerçek defter sayfası olarak açılsın; iki nokta ve tırnak işaretinin görevleri birer örnekle sayfa kenarında dursun.", "Konuşma aktarımı çalışılsın: gözlemcinin sözü tırnak içinde, öncesinde iki nokta.", "Öğrenci kendi doğa gözlemini bir cümleyle yazıp işaretlerini kendisi koysun."),
"y22": ("Roket kaldırılsın; gerçek su döngüsü şeması (deniz, buhar, bulut, yağmur) ekranda dursun ve adım kartları şemanın üzerindeki yerlerine yerleşsin.", "Kar ve dolu varyantlarıyla yeni döngü sıralansın; ara adım çeldiricisi eklensin.", "Öğrenci döngüyü 'önce / sonra / en sonunda' bağlarıyla kendi cümleleriyle anlatsın."),
"y23": ("Basamak yazıları zeminden ayrışan açık renkte olsun; karar için bağlam cümlesi ekranın üstünde sürekli görünsün ('Dün parka gittik. ___ eve döndük.').", "Yakın zaman ifadeleri çeldirici olsun (az önce/şimdi, dün/geçen hafta); sincap yanlışta düşmesin, basamak sallansın.", "Öğrenci seçtiği zaman ifadeleriyle kendi gününü üç cümlede sözlü anlatsın; kayıt veya rubrik kanıt olsun."),
"y24": ("Yarım metin ekranda görünür dursun: önceki cümleler panelde okunsun, tamamlama kartları metnin altında sabit olsun.", "İki makul tamamlamadan kişi, zaman ve konu tutarlılığına uyan seçilsin; öğrenci dayandığı ipucu cümlesini işaretlesin.", "Öğrenci metnin son cümlesini hazır kart olmadan ekran klavyesiyle kendisi yazsın."),
"y25": ("Gerçek kütüphane rafları ve kitap kapakları çizilsin; okurun isteği tür + ilgi cümlesi olarak okunsun ve kapaktan tür çıkarımı yapılsın.", "Aynı türde iki kitaptan okurun ilgisine uygun olan seçilsin; kapak ipuçları karşılaştırılsın.", "Öğrenci kendi okuma tercihini 'Ben ... severim çünkü ...' kalıbıyla söylesin veya yazsın."),
"y26": ("Metin paneli taşmadan yerleşsin; hatalı sözcüğe dokununca kalem otomatik düzeltmesin - öğrenci doğru yazımı iki seçenekten seçsin ya da klavyeyle yazsın.", "Farklı hata türleri karışsın: yazım, büyük harf, ayrı/bitişik 'de-da'; her düzeltmede kural kısa görünsün.", "Öğrenci üç hatalı kısa paragrafı bağımsız bulup düzeltsin; düzeltme sayısı ve türü kayda geçsin."),
"y27": ("İki metin ekranda YAN YANA görünsün; ileti kartı bantta akmasın, terazi görseli iki kefesiyle kararı taşısın.", "Konusu aynı, iletisi farklı metin çiftleri eklensin; 'aynı konu' ile 'aynı ileti' ayrımı vurgulansın.", "Öğrenci iki metnin ortak iletisini kendi cümlesiyle söylesin ve her metinden birer kanıt göstersin."),
"y28": ("Gerçek köprü sahnesi kurulsun; sözcükler yalın değil kısa cümle bağlamıyla verilsin ve eşleşen çift köprü üzerinde buluşsun.", "Bağlama göre uygun eş anlamlı seçilsin: 'yaşlı adam' - 'ihtiyar adam' olur; 'yaşlı ağaç' - 'ihtiyar ağaç' tartışılır.", "Öğrenci eş anlamlı çifti kullanarak bir konuşma cümlesi kursun ve sesli söylesin."),
"y29": ("Gerçek mektup şablonu açılsın: tarih, hitap, gövde ve imza alanları görünür olsun; işaretler bu gerçek yapının üzerinde çalışılsın.", "Hitap virgülü, tarih yazımı ve kapanış ifadesi birlikte çalışılsın.", "Öğrenci yazara iki cümlelik mini mektubu ekran klavyesiyle yazsın; hitap ve işaret kararları kayda geçsin."),
"y30": ("Cevap cümleleri sütun adını birebir söylemesin ('Kahramanlık maceraları okurum' → ÖYKÜ gibi çıkarım gereksin); işaretler rakam değil çetele çizgisiyle birikssin ve beşinci çizgi dördünü kessin.", "Çetele tamamlanınca sıklık tablosuna çevrilsin; 'en çok / en az' soruları sorulsun.", "Öğrenci kendi tercihine çetele ekleyip sonucu 'Sınıfımızda en çok ... seviliyor' cümlesiyle yorumlasın."),
"y31": ("Gerçek bir kitap açılıp kapanabilsin; bölümler (kapak, iç kapak, içindekiler, bölümler, arka kapak) sıralanınca kitap gerçekten kurulsun.", "Bölüm adı ile işlevi eşleştirilsin: 'içindekiler' hangi soruya cevap verir?", "Öğrenci eline aldığı hayalî kitap için bir bölümün işlevini kendi cümlesiyle açıklasın."),
"y32": ("Gerçek dilek kutusu ve form sahnesi kurulsun; önce istek/şikâyet/öneri türü seçilsin, sonra türe uygun cümle kurulsun.", "Aynı konu üç türde ifade edilsin: isteğin, şikâyetin ve önerinin dil farkı karşılaştırılsın.", "Öğrenci kendi dileğini iki cümleyle ekran klavyesinden yazsın ve kutuya atsın; nazik ifade rubriği uygulansın."),
"y33": ("Sanat atölyesi gerçek tezgâhla kurulsun; sanatçının isteği açıklayıcı kısa metin olarak okunsun ve malzemeler içerikten çıkarımla seçilsin.", "Amaca uymayan çekici malzeme çeldirici olsun; öğrenci seçimini amaçla gerekçelendirsin.", "Öğrenci hazırladığı tepsiyi 'Bu malzemeleri seçtim çünkü ...' cümlesiyle sunsun; sunum kaydedilsin veya rubrikle değerlendirilsin."),
"y34": ("Şenlik alanında üç gerçek stant (sanat, spor, bilim) kurulsun; etkinlik kartları görselli ve sabit gelsin, bant hızı kaldırılsın.", "Birden çok alana uyan etkinlikler eklensin (ritmik jimnastik: spor+sanat); öğrenci ölçüt seçip savunsun.", "Öğrenci kendi yeteneğini sınıflandırıp 'Ben ... alanındayım çünkü ...' cümlesini kursun."),
"y35": ("Tiyatro sahnesi kurulsun; replik seçilen işarete göre FARKLI TONDA seslendirilsin - işaret değişince aynı cümlenin sesi de değişsin.", "Aynı cümle üç işaretle karşılaştırılsın: 'Geldin.' / 'Geldin?' / 'Geldin!' anlam farkı dinletilsin.", "Öğrenci repliği seçtiği işarete uygun tonla okuyup kaydetsin; tonlama rubriğiyle değerlendirilsin."),
"y36": ("Sahne mikseri gerçek görselle kurulsun ve tren kaldırılsın; her düzey/vurgu seçiminde örnek sunum sesi GERÇEKTEN dinletilsin.", "Vurgu yeri değişince anlamın değiştiği örnekler dinletilsin: 'BEN yaptım' / 'ben YAPTIM'.", "Öğrenci kısa sunum cümlesini uygun vurgu ve düzeyle kaydetsin; örnekle karşılaştırıp öz değerlendirsin."),
"y37": ("Benzetme makinesi benzeyen-benzetilen-benzetme yönünü görsel olarak göstersin; kurulan benzetme resimlensin (pamuk gibi bulut).", "'Gibi' ve 'kadar' ile uygun/anlamsız benzetmeler karşılaştırılsın; anlamsız benzetme neden komik tartışılsın.", "Öğrenci doğadan bir varlık için özgün benzetme cümlesini kendisi yazsın veya söylesin."),
"y38": ("Kartlarda emoji yerine gerçek yüz/beden çizimleri olsun; eşleşince duygu kısa animasyonla canlandırılsın ve ayna motifi gerçekten çalışsın.", "Yakın duygular çeldirici olsun (şaşkınlık/korku, mutluluk/heyecan); beden ipucu ile yüz ipucu ayrı vurgulansın.", "Öğrenci verilen cümleyi seçtiği duyguya uygun jest ve mimikle canlandırsın; öz değerlendirme rubriği doldurulsun."),
"y39": ("Cümle sabit panelde dursun; anlam seçenekleri düşmesin, sabit kartlarda olsun. Öğrenci karar öncesi cümledeki bağlam ipucunu işaretleyebilsin.", "Yakın iki anlamdan bağlama uygun olan seçilsin; aynı sözcük ikinci bir cümlede farklı anlamla gösterilsin.", "Tahmin-sözlük-yeni cümle döngüsü tamamlansın: öğrenci tahminini sözlük anlamıyla karşılaştırıp yeni cümle yazsın."),
"y40": ("Hikâye metni ekranda görünür dursun; her basamakta 'sonra ne olur?' seçenekleri metindeki kanıta bağlansın ve basamak yazıları okunur kontrastta olsun.", "Doğrudan söylenmeyen, çıkarım gerektiren tahmin adımları eklensin.", "Öğrenci tahminini 'Bence ... olacak çünkü metinde ...' kalıbıyla gerekçelendirsin."),
"y41": ("Laboratuvar sahnesi korunsun ama cümle sabit okunur kartta dursun; koyu sözcük vurgulu gösterilsin ve bant hızı kaldırılsın.", "Aynı sözcüğün iki cümlede gerçek ve mecaz kullanımı yan yana karşılaştırılsın ('gözü doldu').", "Öğrenci mecaz anlamlı bir sözcükle kendi cümlesini kursun ve gerçek anlamından farkını söylesin."),
"y42": ("Köprü kalasları atasözlerini taşısın; doğru eşleşmede atasözünün anlattığı durum kısa canlandırmayla gösterilsin.", "Yakın anlamlı atasözü çeldiricileri eklensin; anlam ile birebir sözcük benzerliği ayrılsın.", "Öğrenci bir atasözünü uygun bir yaşam durumuna bağlayıp 'Bu durumda ... denir çünkü ...' cümlesi kursun."),
"y43": ("Yön blokları yazılı yönerge kartlarına dönüşsün; dizilen program panelde numaralı cümleler hâlinde görünsün ve robot okurken adım adım uygulasın.", "Hatalı verilen bir programı okuyup hatayı bulma ve yalnız o adımı düzeltme görevi eklensin.", "Öğrenci robotu hedefe götüren yönergeyi kendisi yazsın; yazılan yönerge çalıştırılarak sınansın."),
"y44": ("Deney masası gerçek araç görselleriyle kurulsun; bilim insanının isteği amaç-araç-adım içeren kısa deney planı olarak okunsun.", "Amaca uymayan çekici araç çeldirici olsun; öğrenci elemeyi gerekçelendirsin.", "Öğrenci basit bir deney için üç adımlı planı kendisi sıralayıp bir cümleyle açıklasın."),
"y45": ("Deney raporu gerçek şablonla açılsın: başlık, malzeme listesi (iki nokta ve virgüller), gözlem cümlesi ayrı bölümlerde çalışılsın.", "İki nokta ve virgülle listeleme birlikte kullanılsın: 'Malzemeler: su, tuz, kap.'", "Öğrenci kendi gözlem cümlesini işaretleriyle birlikte ekran klavyesiyle yazsın."),
"y46": ("Tren kaldırılsın; ölçer her ortamın GERÇEK ses kaydıyla çalışsın - öğrenci sesi dinleyip düzeyi ölçsün ve uygunluk kararını kendisi versin.", "Aynı ortamın farklı saatleri karşılaştırılsın (teneffüste sınıf / ders sırasında sınıf).", "Öğrenci kendi çalışma ortamı için üç maddelik uygunluk kontrol listesi işaretlesin ve bir öneri yazsın."),
"y47": ("Deyimin anlamı görselle desteklensin; deyim sözcükleri bölünmez tek blok olarak yerleşsin ve kurulan cümle sesli okunsun.", "Deyimin uygun bağlamı seçilsin: 'etekleri zil çalmak' hangi duruma uyar?", "Öğrenci öğrendiği deyimle kendi cümlesini yazsın; deyimin yerinde kullanımı rubrikle işaretlensin."),
"y48": ("Bilim panosu kurulsun; adımlar soru-kaynak-not-sunum akışıyla panoda görselleşsin, roket sahnesi kullanılmasın.", "Eksik adım bulma görevi eklensin: araştırmada hangi adım atlanmış?", "Öğrenci merak ettiği bir soru için mini araştırma planını sözlü anlatsın veya maddelerle yazsın."),
"y49": ("Müze salonu gerçek eser görselleriyle kurulsun; ziyaretçi isteği bilgi metninden çıkarım gerektirsin ve eser kartında görsel+kısa bilgi olsun.", "Benzer iki eserde ayırt edici bilgi vurgulansın (yapım yılı, malzeme, şehir).", "Öğrenci bir eseri iki cümleyle tanıtsın: adı, yeri ve bir özelliği; sunum kaydedilsin veya rubrikle izlensin."),
"y50": ("Metin taşmadan yerleşsin; yabancı sözcüğe dokununca kalem otomatik değiştirmesin - Türkçe karşılığı öğrenci seçsin ve değişen cümle yeniden okunsun.", "Birden çok Türkçe karşılıktan bağlama uygun olan seçilsin ('online' → çevrim içi).", "Öğrenci cümleyi Türkçe karşılıkla ekran klavyesinden yeniden yazsın."),
"y51": ("Bayram panosu gerçek pano görseliyle kurulsun; özel adlar (bayram, yer, kişi) karışık cümlelerde çalışılsın ve düzelen cümle panoya asılsın.", "Tarih yazımı ve kesme işareti eklensin: '23 Nisan'da', 'Ankara'ya'.", "Öğrenci pano için kendi kutlama cümlesini klavyeyle yazsın; büyük harfleri bağımsız kullansın."),
"y52": ("Türkiye haritası sahne olsun; eşleşen eser haritadaki şehrine yerleşsin ve kısa bilgi cümlesi okunarak eşleşme kanıtlansın.", "Aynı şehirden iki eser veya iki şehirden benzer eserler çeldirici olsun.", "Öğrenci bildiği ya da gezdiği bir eseri 'Bu eser ...dadır ve ...' cümlesiyle tanıtsın."),
"y53": ("Okul bahçesi tören sahnesi kurulsun; adımlar sıralandıkça tören gerçekten canlansın (bayrak yükselsin, marş başlasın), roket kullanılmasın.", "Karışık verilen adımlar içinde hatalı adımı bulma görevi eklensin.", "Öğrenci töreni 'önce / sonra / en sonunda' bağlarıyla kendi cümleleriyle anlatsın."),
"y54": ("Müze-çarşı sahnesi kurulsun; davranış kartları görselli ve sabit gelsin, kart kenarda kırpılmasın ve bant hızı kaldırılsın.", "Niyet-etki ayrımı çalışılsın: bilmeden zarar veren davranış nasıl düzeltilir?", "Öğrenci kültürü koruyan bir davranış önerisini kendi cümlesiyle söylesin veya yazsın."),
"y55": ("Kültür panosu gerçek olsun; kurulan cümle panoya asılıp sesli okunsun; kartlar küçük harfle gelsin, işaret öğrencinin kararı olsun.", "Duygu tonuna uygun sözcük seçimi çalışılsın: coşku cümlesinde hangi sözcük daha güçlü?", "Öğrenci vatan/kültür konulu kendi cümlesini klavyeyle yazsın; cümle panodaki şiire eklensin."),
"y56": ("Dikte edilen sözcük tilkinin balonunda yazılmasın; harf havuzu karışık dizilsin ve kültür sözcükleri görsel kartla desteklensin (ebru, çini).", "ğ, â ve ünlü uyumu içeren sözcükler eklensin; iki kez dinleme cezasız olsun.", "Öğrenci yazdığı kültür sözcüğünü bir cümle içinde kullansın."),
"y57": ("Adalet terazisi sahnesi kurulsun; ifade kartı sabit okunsun, karar sonrası kart terazinin doğru kefesine konsun ve bant kaldırılsın.", "Aynı konunun hak ve sorumluluk çifti birlikte verilsin: 'oyun oynamak hakkım' - 'oyuncakları toplamak sorumluluğum'.", "Öğrenci bir hakkına karşılık gelen sorumluluğu kendi cümlesiyle söylesin."),
"y58": ("Gerçek dilekçe şablonu açılsın: tarih, makam, istek metni, ad-soyad ve imza alanları görünür olsun; bölümler şablondaki yerlerine yerleşsin.", "Bölüm sırası ve içeriği eşleştirilsin: hangi bölümde ne yazar?", "Öğrenci kurgusal bir istek için kısa dilekçeyi klavyeyle doldursun; kişisel veri istenmesin."),
"y59": ("Bildiri panosu kurulsun; işaret seçimi cümlenin ANLAMINI nasıl değiştirdiği örnekleriyle gösterilsin ve seçilen işaretle cümle yeniden seslendirilsin.", "Aynı cümle farklı işaretlerle karşılaştırılsın; anlam farkı iki resimle gösterilsin.", "Öğrenci bir çocuk hakkını anlatan cümleyi uygun işaretle kendisi yazsın."),
"y60": ("Hedef sözcük balonda yazılmasın; bitişik yazım kuralı kutusu ekranda kalsın ve harf havuzu karışık dizilsin.", "Farklı pekiştirme türleri (m/p/r/s: masmavi, sapasağlam, tertemiz) dinletilsin; ayrı yazma çeldirici olsun.", "Öğrenci pekiştirmeli sözcüğü kendi cümlesinde kullanıp klavyeyle yazsın."),
"y61": ("Mahalle ve kaldırım gerçek görselle kurulsun; yön blokları yazılı yönerge kartları olsun, tehlike noktaları (kavşak, inşaat) gerekçesiyle gösterilsin.", "Aynı hedefe giden iki rotadan güvenli olanı seçilsin ve neden güvenli olduğu söylensin.", "Öğrenci okul yolunu anlatan üç adımlı yönergeyi kendisi yazsın; robot yazılanı uygulasın."),
"y62": ("Denge köprüsü gerçek görselle kurulsun: hak kalasları bir yandan, sorumluluk kalasları diğer yandan köprüyü dengede tutsun; parça yazıları sığsın.", "Bir hakka birden çok sorumluluğun bağlanabildiği örnekler eklensin.", "Öğrenci kendi yaşamından bir hak-sorumluluk çiftini cümleyle ifade etsin."),
"y63": ("Meclis kürsüsü sahnesi kurulsun; kurulan cümle mikrofonda SESLİ okunsun ve panoya oy için asılsın.", "Nazik-net üslup karşılaştırılsın: aynı istek kaba, çekingen ve uygun biçimde verilip uygun olan seçilsin.", "Öğrenci kendi isteğini iki cümleyle yazsın ve kürsüde sesli sunsun; nezaket rubriği uygulansın."),
"y64": ("Kalkan-yakalama mekaniği kaldırılsın; bilgi kartı sabit gelsin, öğrenci 'paylaşırım / paylaşmam' kararını gerekçe seçerek versin.", "Bağlama göre değişen örnekler eklensin: adını okulda söylersin, internette yazmazsın.", "Öğrenci güvenli paylaşım kuralını 'İnternette ... paylaşmam çünkü ...' kalıbıyla kendisi söylesin veya yazsın."),
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
        return f"Kaynakta {n.get('rounds','?')} ortam kartı var; dört sabit düzeyden seçim yapılıyor ve hiçbir ses örneği tanımlı değil."
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
    return f"Kaynakta {n.get('columns','?')} sütun ve {n.get('responses','?')} yanıt tanımlı; yanıt cümleleri tür adını birebir içeriyor."


def modality_evidence(m):
    return {
        "writing": "Başarı kaydına öğrencinin ürettiği yazı, düzelttiği bölüm ve kullandığı kural eklenmeli; yalnız seçilen/dizilen kart kimliği yeterli değildir.",
        "speaking": "Başarı kaydına kısa ses üretimi veya öğretmen/öz değerlendirme rubriği eklenmeli; yalnız seçilen seçenek konuşma kanıtı değildir.",
        "listening": "Başarı kaydına ilk dinlemedeki yanıt, tekrar sayısı ve işitsel kanıt eklenmeli; yazılı ipucuyla verilen cevap ayrı tutulmalıdır.",
        "reading": "Başarı kaydına seçilen yanıtla birlikte metinde işaretlenen kanıt ve gerekçe eklenmelidir.",
    }[m]


GROUP_FOCUS = {
    "Tema 1 · Değerlerimizle Yaşıyoruz": ["Değer kavramı yalnız doğru kartı seçmekle değil, davranış kanıtı ve öğrencinin gerekçesiyle kurulmalı.", "Stüdyo, yayınevi, tamirhane ve baskı makinesi başlıkları gerçek sahne ve eylem olarak görünmeli; bant, uzay ve tren şablonlarına düşmemeli.", "Yazma ve konuşma kazanımlarında son turda serbest üretim zorunlu olmalı."],
    "Tema 2 · Atatürk ve Kahramanlarımız": ["Tarihî içerik somut ve yaş düzeyine uygun olmalı; kartlardaki tarih sayıları ilk turda gizlenerek sıralama içerik bilgisine dayandırılmalı.", "Zaman şeridi, köprü ve dikte başlıkları roket-yakıt ve yazılı-balon tuzaklarından arındırılmalı.", "Dikte oyunlarında hedef sözcük ekranda görünmemeli; dinleme gerçek dinleme olmalı."],
    "Tema 3 · Doğayı Tanıyoruz": ["Doğa süreçleri (su döngüsü, mevsimler) gerçek şema ve görselle işlenmeli; adım kartları şemadaki yerine oturmalı.", "Yönerge yazma kazanımı ok dizmekten çıkarılıp gerçek yazılı yönergeye bağlanmalı.", "Zaman ifadeleri ve tamamlama görevlerinde bağlam cümlesi ekranda sürekli görünmeli."],
    "Tema 4 · Bilgi Hazinemiz": ["Kütüphane, kitap, mektup ve anket sahneleri gerçek nesnelerle kurulmalı; servis tezgâhı ve uzay şablonu kaldırılmalı.", "Çetele kuralına uygun işleme (beşinci çizgi dördü keser) ve tablo yorumu eklenmeli.", "Düzeltme oyunlarında doğru biçim otomatik gelmemeli; öğrenci gerçekten düzeltmeli."],
    "Tema 5 · Yeteneklerimizi Kullanıyoruz": ["Ses düzeyi, vurgu, tonlama ve jest-mimik hedefleri gerçek ses/beden üretimi ve gerçek ses örnekleriyle çalışmalı.", "Sahne mikseri ve ayna başlıkları tren-tünel ve uzay şablonlarından kurtarılmalı.", "Tahmin ve benzetme görevleri metin kanıtı ve öğrenci cümlesiyle tamamlanmalı."],
    "Tema 6 · Bilim Yolculuğu": ["Mecaz, deyim ve atasözü görevleri bağlam kanıtı ve kısa canlandırmayla anlamlandırılmalı.", "Deney planı, rapor ve araştırma adımları gerçek bilimsel akışla görselleşmeli.", "Kodlama görevlerinde program yazılı yönerge cümlelerine dönüşmeli."],
    "Tema 7 · Millî Kültürümüz": ["Eser, şehir, tören ve bayram içerikleri harita ve gerçek görsel kanıtla sunulmalı.", "Kültür sözcükleri dikte ve pano görevlerinde üretimle pekiştirilmeli; dikte cevabı ekranda görünmemeli.", "Kültürü koruma davranışları gerekçeli karar ve öğrenci önerisiyle işlenmeli."],
    "Tema 8 · Hak ve Sorumluluklarımız": ["Dilekçe, bildiri ve meclis görevleri gerçek şablon ve gerçek yazı/konuşma üretimiyle çalışmalı.", "Hak-sorumluluk ilişkisi terazi/denge görseliyle somutlaşmalı; bant ve kalkan-yakalama şablonları kaldırılmalı.", "Dijital gizlilik kararları hız oyunundan çıkarılıp karar + gerekçe yapısına bağlanmalı."],
}

GROUP_COLORS = [CORAL, TEAL, PURPLE, GOLD, BLUE, GREEN, CORAL, PURPLE]

mod_counts = {"writing": 0, "speaking": 0, "listening": 0, "reading": 0}
for g in games:
    mod_counts[modality(g)] += 1

doc = BaseDocTemplate(
    str(OUT), pagesize=A4, rightMargin=MX, leftMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
    title="3. Sınıf Türkçe Oyunları - Ayrıntılı Düzeltmeler", author="Macera Akademi oyun incelemesi",
)
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

story = [Spacer(1, 14 * mm), P("MACERA AKADEMİ", cover_kicker),
         P("3. Sınıf Türkçe Oyunları<br/>Ayrıntılı Düzeltmeler", cover_title),
         P("64 oyunun kaynak görevleri çıkarılarak ve 14 oyun motorunun tamamı 390x844 telefon görünümünde tek tek açılıp denenerek hazırlanmıştır.", cover_sub)]
cover_box = Table([[P("<b>Kapsam</b><br/>Bu belge y01-y64 arasındaki 3. sınıf Türkçe oyunlarının tamamını kapsar. Her oyun için denemede görülen mevcut yapı, eğitimsel risk, özgün sahne ve yeni oynanış, üç kademeli tur, geri bildirim ve ölçülebilir kabul koşulları ayrı ayrı verilir.")]], colWidths=[153 * mm])
cover_box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL), ("BOX", (0, 0), (-1, -1), 0.7, TEAL),
                               ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                               ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12)]))
story += [cover_box, Spacer(1, 8 * mm), P("İnceleme yöntemi", h2)]
story += bullets(["3. sınıf profili üzerinden Türkçe listesindeki 64 oyunun kaynak yapılandırmaları çıkarıldı ve sekiz tema tema karşılaştırıldı.",
                  "Bant, hafıza, radar, servis, tamirhane, tren, matbaa, dedektif, roket, köprü, daktilo, kargo, sırık ve çetele motorlarının tamamı 390x844 telefon görünümünde açıldı; kart akışı, kart düşüşü, sürükleme ve dokunma alanları denendi.",
                  "Düzeltmeler başlık-sahne uyumu, cevabı sızdıran arayüz ögeleri, yerleşim/kırpılma hataları, okuma/dinleme/yazma/konuşma geçerliliği, üç kademeli tur ve test edilebilir kabul koşulunu birlikte ele alır."])
story += [PageBreak()]

story += [P("Testten çıkan öncelikli bulgular", h1)]
story += [box("1. 64 oyun 14 ortak motora dağıtılmış; başlık ile sahne sık sık çelişiyor", ["8'er oyun bant, tamirhane ve matbaa; 7 oyun servis tezgâhı; 5'er oyun hafıza ve roket; 4'er oyun radar ve köprü; 3'er oyun tren, dedektif, daktilo ve kargo; 2 oyun sırık ve 1 oyun çetele motorunu kullanıyor. Zaman Şeridi uzayda roket-YAKIT sahnesinde, Ses Düzeyi Ayarı tren-tünel sahnesinde, Yayınevi Masası ahşap servis tezgâhında, Hikâye Kâhini kapsül-çanak sahnesinde açılıyor."], PALE_CORAL, CORAL), Spacer(1, 1.7 * mm)]
story += [box("2. Birçok oyunda arayüz cevabı kendisi söylüyor", ["Dikte oyunlarında (y14, y56, y60) hedef sözcük tilkinin balonunda yazılı olarak görünüyor; Yayınevi Masası'nda balondaki simgeler kart simgeleriyle birebir; Zaman Şeridi kartlarında tarihler sıralamayı sayıyla çözdürüyor; Cümle Kurma'da büyük harfli kart ile nokta kartı dizilişi ele veriyor; Okur Anketi'nde cevap cümlesi sütun adını birebir içeriyor; Noktalama Tamirhanesi yönergesi doğru işaretin adını söylüyor."], PALE_GOLD, GOLD), Spacer(1, 1.7 * mm)]
story += [box("3. Telefon boyutunda yerleşim ve kırpılma hataları görüldü", ["Dedektif metni tutanak panelinden taşıp alttaki kutunun başlığıyla üst üste biniyor ve soru başlığı iki yandan kırpılıyor; köprü oyunlarında uzun cümleler parça çiplerine sığmıyor; bant kartı ekran kenarında kırpılıyor; tamirhanede görev metni ile 'Kalan' satırı çakışıyor; sırık basamaklarında yazı-zemin kontrastı düşük."], PALE_BLUE, BLUE), Spacer(1, 1.7 * mm)]
story += [box(f"4. {mod_counts['writing']} yazma ve {mod_counts['speaking']} konuşma kazanımında gerçek üretim yok", ["Yazma hedefli oyunlar kart dizme, dokunma ve sürüklemeden oluşuyor; serbest yazı alanı hiçbirinde yok. 'Ayrıntılı yönerge yazar' kazanımındaki kargo oyunlarında yalnız yön oku diziliyor. Ses düzeyi, vurgu ve gürültü oyunlarında hiçbir gerçek ses örneği dinletilmiyor ve öğrenci ses üretmiyor."], PALE_TEAL, TEAL), Spacer(1, 1.7 * mm)]
story += [box("5. Tur ve can standardı tutarsız; teknik çökme yok", ["Hafıza oyunları 6 kalple, diğerleri 3 kalple açılıyor; kargo 2 görevde, bant tek 8-10 kartlık havuzda kalıyor; üç kademeli tur hiçbir motorda yok. y01-y64 arasındaki 64 oyunun tamamı yüklendi; motorlarda çökme veya konsol hatası görülmedi. Temel sorun çalışmama değil, ölçme hedefi ile sahne/mekanik arasındaki uyumsuzluk."], PALE_PURPLE, PURPLE)]
story += [PageBreak()]

story += [P("Bütün 3. sınıf Türkçe oyunlarında ortak uygulama standardı", h1)]
rows = [
    [P("Sahne", box_title), P("Başlıktaki stüdyo, yayınevi, kütüphane, müze, meclis, tören alanı veya laboratuvar gerçek görsel ve oyun eylemi olarak kullanılmalı; ortak bant/uzay/tren/servis şablonu kaldırılmalı.", small)],
    [P("Cevap sızdırmama", box_title), P("Hedef sözcük, doğru işaret adı, tarih sırası, simge eşleşmesi veya sütun adı gibi cevabı taşıyan hiçbir öge ekranda bulunmamalı.", small)],
    [P("Yerleşim", box_title), P("390x844 ekranda hiçbir metin kırpılmamalı, taşmamalı, üst üste binmemeli; dokunma alanları en az 44 px olmalı.", small)],
    [P("Okuma", box_title), P("Metin sabit, okunabilir ve örtüsüz olmalı; öğrenci cevaptan önce metindeki kanıtı işaretlemeli.", small)],
    [P("Dinleme", box_title), P("İlk işitsel turda cevap yazısı gizli olmalı; tekrar dinleme cezasız ve sayısı kaydedilebilir olmalı.", small)],
    [P("Yazma", box_title), P("Yazma kazanımı son turda gerçek sözcük/cümle/yönerge üretimi içermeli; kart dizmek tek başına başarı sayılmamalı.", small)],
    [P("Konuşma", box_title), P("Ses düzeyi, vurgu, tonlama ve anlatma için gerçek ses örneği dinletilmeli ve kısa ses üretimi ya da rubrik bulunmalı.", small)],
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

story += [P("Son kabul kontrolü", h1), P("3. sınıf Türkçe bölümü tamamlanmadan önce", h2)]
story += bullets(["y01-y64 arasındaki 64 oyun üç kademeli turla baştan sona test edilir; görünen başlık, sahne, kontrol, ses ve hedef beceri kayıt altına alınır.",
                  "Zaman Şeridi gerçek zaman şeridi, Ses Düzeyi Ayarı ve Gürültü Ölçer gerçek ses örneği, Yayınevi Masası gerçek editör masası, Okur Anketi gerçek çetele çizgisi kullanır.",
                  f"{mod_counts['writing']} yazma kazanımında son tur gerçek yazı üretimi içerir; kart dizmek tek başına yazma başarısı sayılmaz.",
                  "Dikte oyunlarında hedef sözcük ekranda görünmez; konuşma oyunlarında kısa ses üretimi veya rubrik, dinleme oyunlarında yazısız ilk tur ve cezasız tekrar bulunur.",
                  "390x844 ekranda hiçbir metin kırpılmaz, taşmaz veya üst üste binmez; kartlar ekran içinde kalır ve dokunma alanları en az 44 px olur.",
                  "Kartlar ilk iki turda sabittir; bant/düşme hızı, yakalama refleksi ve nişan alma Türkçe doğruluk puanına karışmaz.",
                  "Her oyunda en az üç farklı içerik örneği, değişen seçenek sırası, açıklayıcı yanlış geri bildirimi ve ölçülebilir kabul kaydı bulunur; web ile APK birebir aynı davranır."])
story += [Spacer(1, 4 * mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 3. sınıf Türkçe listesindeki y01-y64 oyunlarını kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, metin/ses, mekanik, üç tur, geri bildirim, öğrenci kanıtı ve test gereksinimlerini ayrıntılı biçimde tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)

reader = PdfReader(str(OUT))
print({"pages": len(reader.pages), "games": len(games), "modalities": mod_counts, "bytes": OUT.stat().st_size, "output": str(OUT)})
