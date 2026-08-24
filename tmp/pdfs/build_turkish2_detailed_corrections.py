from __future__ import annotations

import html
import json
import re
import subprocess
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
OUT = ROOT / "output/pdf/2_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf"
EXTRACTOR = ROOT / "tmp/pdfs/extract_turkish2_games.mjs"
NODE = Path("/Users/ceyda/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node")
OUT.parent.mkdir(parents=True, exist_ok=True)


def load_games():
    raw = subprocess.run(
        [str(NODE), str(EXTRACTOR), "--full"], check=True, capture_output=True, text=True
    ).stdout
    return json.loads(raw)


games = load_games()
assert len(games) == 90

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
        [[P(str(number), badge), P(f"<b>{clean(title)}</b><br/><font size='7.5' color='#F1EEF8'>{clean(subtitle)}</font>", game_title)]],
        colWidths=[14 * mm, 162 * mm], rowHeights=[18 * mm],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "CENTER"), ("LEFTPADDING", (1, 0), (1, 0), 9),
        ("RIGHTPADDING", (1, 0), (1, 0), 7), ("ROUNDEDCORNERS", [8]),
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
    canv.drawString(MX, 8.2 * mm, "2. Sınıf Türkçe - Ayrıntılı Oyun Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 8.2 * mm, str(canv.getPageNumber()))
    canv.restoreState()


ENGINE = {
    "dragMatch": ("Eşleştirme Köprüsü", "Başlığa özgü sahne yerine aynı hedef kutuları ve PARÇALAR alanı kullanılıyor; etiket sürükleme, içeriğin kendisinden daha baskın."),
    "orderSequence": ("roket-yakıt motoru", "Kartlar vagon, film, zaman şeridi veya yönerge adımı olmak yerine roket çevresinde dolaşıyor; seçimden sonra YAKIT alanına gidiyor."),
    "choiceQuestion": ("Uzay Lazerleri", "Okuma, dinleme, konuşma veya sözlük görevi hareketli meteorlara nişan alma işlemine dönüşüyor; motor becerisi dil kararına karışıyor."),
    "catchDrop": ("radar/kapsül yakalama", "Yağmur veya paraşüt adı kullanılsa da işaretler kapsül içinde düşüyor; kontrol ipucu sarı nokta ve çanak diliyle veriliyor."),
    "wordHighlight": ("dedektif tutanağı", "Metin tek kartta ve büyüteç altında sunuluyor; çok sözcüklü cevaplarda satır kırılması ile büyüteç hedefi örtebiliyor."),
    "tapSelect": ("su altı balık-ağ motoru", "Tabela, sınıf, kitaplık veya çalışma odası yerine hareketli balık etiketleri ve TOPLANANLAR ağı görünüyor."),
}

TYPE_RISK = {
    "dragMatch": "Doğru kavramı açıklamak yerine etiketin hangi kutuya ait olduğunu deneme-yanılmayla bulmak da başarı getirebilir.",
    "orderSequence": "Kartların sürekli hareketi, olayların mantıksal sırasını düşünmek yerine nesneyi yakalama hızını ödüllendirir.",
    "choiceQuestion": "Doğru seçeneği bilmek yetmez; hareketli hedefe nişan almak gerekir. Yanlış motor hareketi yanlış dil cevabı gibi kayda geçebilir.",
    "catchDrop": "Öğrenci işaretin işlevini açıklamadan yalnız doğru sembolün düşeceği sütuna yetişebilir; hız baskısı kural bilgisini gölgeler.",
    "wordHighlight": "Tıklanabilir sözcük bulma, sözcüğün cümledeki görevini açıklama veya cevabı kendi sözleriyle üretme kanıtı sağlamaz.",
    "tapSelect": "Hareketli kartlar okunmadan ağla toplanabilir; seçim doğruluğu ile görsel takip ve dokunma hızı birbirine karışır.",
}

TYPE_FEEDBACK = {
    "dragMatch": "Yanlış sürüklemede parça başlangıca dönsün; hedef kutu parlamasın. İlişkinin hangi sözcük, görsel veya bağlam ipucuna dayandığı kısa bir karşılaştırmayla sorulsun.",
    "orderSequence": "Yanlış sırada bütün dizi silinmesin; yalnız son kart geri alınsın ve 'önce/sonra/çünkü' ilişkisini düşündüren ipucu verilsin.",
    "choiceQuestion": "Yanlış hedefte can kaybı yerine seçenek sabitlensin; öğrenci metindeki kanıtı işaretleyip yeniden karar versin. Nişan alma hatası ölçmeye katılmasın.",
    "catchDrop": "Yanlış yakalamada cümle sesli ve doğru tonla yeniden çalınsın; işaret doğrudan söylenmeden cümlenin soru, duygu veya bilgi oluşu hatırlatılsın.",
    "wordHighlight": "Yanlış sözcükte metin kaybolmasın; soru ile seçilen sözcük yan yana okunup kişi, zaman, neden veya anlam ilişkisi karşılaştırılsın.",
    "tapSelect": "Yanlış kart ekrandan kaçmasın; hareket dursun, seçilen ifade yüksek sesle okunsun ve öğrenciden neden uygun olmadığını seçmesi istensin.",
}

TYPE_ACCEPT = {
    "dragMatch": "Sürükleme alanları sabit, en az 44 px ve başlığın sahnesine ait olacak; etiket-konum ezberiyle başarı elde edilemeyecek.",
    "orderSequence": "Kartlar karar süresince sabit kalacak; doğru sıra her açılışta karıştırılacak ve en az bir gerekçe sorusuyla doğrulanacak.",
    "choiceQuestion": "Seçenekler sabit olacak; nişan alma veya hedef hareketi puanlanmayacak. Başarı doğru seçenek ile metin/ses kanıtının birlikte seçilmesine bağlı olacak.",
    "catchDrop": "İlk turda düşme hızı kapalı olacak; işaretin cümledeki işlevi en az bir açıklama veya tonlama göreviyle ölçülecek.",
    "wordHighlight": "Metin büyüteçle örtülmeyecek; çok sözcüklü cevaplar tek bir anlam birimi olarak seçilebilecek ve satır kırılması kabulü bozamayacak.",
    "tapSelect": "Kartlar ilk iki turda hareket etmeyecek; okuma süresi motor hızdan ayrılacak ve doğru seçim gerekçeyle tamamlanacak.",
}

MODALITY_RISK = {
    "writing": "Kazanım yazma/oluşturma istediği hâlde mevcut yapıda klavye, el yazısı, cümle kurma veya düzenleme alanı yok; hazır cevabı seçmek gerçek yazma kanıtı değildir.",
    "speaking": "Kazanım konuşma istediği hâlde öğrenci ses üretmiyor; yalnız seçenek işaretlendiği için vurgu, tonlama, akıcılık ve uygun ifade gözlenemiyor.",
    "listening": "Dinleme hedefinde yazılı yönerge ve seçenekler cevabı taşıyabiliyor; ses kapatıldığında da oyun çözülebiliyorsa ölçme geçerli değildir.",
    "reading": "Okuma hedefi, metindeki kanıtı kullanmaktan çok görsel olarak en belirgin seçeneği bulmaya indirgenirse çıkarım ve anlama ölçülmez.",
}

MODALITY_NEW = {
    "writing": "Son turda öğrenci gerçek bir sözcük, cümle, yönerge veya form alanı üretsin; harf kartı/klavye yalnız erişim desteği olsun ve hazır cümle seçimi tek başına başarı sayılmasın.",
    "speaking": "Örnek dinletildikten sonra öğrenci kısa bir ses kaydı alsın veya yetişkin/öz değerlendirme rubriğiyle konuşsun; vurgu, uygun hitap, sıra ve anlaşılabilirlik ayrı kaydedilsin.",
    "listening": "İlk dinleme turunda hedef metin ve cevap anahtarı görünmesin; ses en az iki kez tekrar edilebilsin ve tekrar dinleme ceza oluşturmasın.",
    "reading": "Öğrenci cevaptan önce metindeki görsel/sözel kanıtı işaretlesin; doğru seçenek ancak kanıtla tutarlı olduğunda kabul edilsin.",
}


DESIGNS = {
"u01": ("Gerçek bir kütüphane rafı ve başlığı kapalı üç kitap kapağı kullan; kapaktaki olay, karakter ve mekân ayrıntıları tıklanabilir olsun.", "İki benzer kapakta konu ile ayrıntıyı ayır; öğrenci seçimini kapaktaki iki kanıtla doğrulasın.", "Başlık ve kapak bazen uyumlu bazen çelişkili gelsin; öğrenci tahminini bir cümleyle yazsın."),
"u02": ("Roket yerine gerçek lokomotif ve üç sabit vagon çiz; olay kartları okunurken zaman bağları görünür fakat doğru sıra gizli olsun.", "Dört olaylı bir masalda ortadaki iki adım yakın anlamlı çeldiricilerle karıştırılsın.", "Görselsiz kısa metinden beş olayı sırala ve 'çünkü/sonunda' bağıyla anlat."),
"u03": ("Uzay yerine sözcüğün geçtiği cümleyi taşıyan orman tabelaları kullan; hedef sözcük seçilebilir ama anlam seçeneği sabit dursun.", "Aynı sözcüğü iki farklı cümlede göstererek bağlam değişince anlamın nasıl değiştiğini karşılaştır.", "Öğrenci tahmini seçtikten sonra kendi kısa cümlesini yazıp sözlük anlamıyla kontrol etsin."),
"u04": ("Gerçek yağmur damlaları ve hareket ettirilen şemsiye kullan; sarı nokta-kapsül dili kaldırılıp cümlenin ses tonu duyulsun.", "Nokta, soru ve ünlem aynı cümle gövdesinde anlam/ton değiştirerek karşılaştırılsın.", "Öğrenci iki cümleyi kendi yazsın, son işareti eklesin ve uygun tonla okusun."),
"u05": ("Erdem ağacında hikâye yaprak yaprak açılsın; cevap elması yalnız olay kanıtı seçildikten sonra sürüklenebilsin.", "Sorumluluk-saygı-yardımlaşma gibi yakın değerler iki kısa olayla karşılaştırılsın.", "Öğrenci seçtiği değeri kendi yaşamından bir örnek cümleyle ağacın yeni yaprağına yazsın."),
"u06": ("Robotu gerçek kaldırım ve yaya geçidinde adım adım yürüt; komut kartları sabit ve nezaket ifadesi ayrı söz balonu olsun.", "Aynı hedefe ulaşan iki komut dizisinden güvenli ve nazik olanı seçtir.", "Öğrenci yeni bir yardım durumu için dört adımlı yönerge yazıp robota uygulasın."),
"u07": ("Köprünün her eksik tahtası cümlenin anlam bağlantısını temsil etsin; tamamlanan cümle sahnede kısa animasyonla gerçekleşsin.", "İki doğruya yakın tamamlamadan bağlama en uygun olanı metindeki ipucuyla ayırt ettir.", "Öğrenci yeni bir başlangıç cümlesini kendi sözüyle tamamlasın ve nedeni açıklasın."),
"u08": ("Dedektif tutanağını satır aralığı geniş, büyüteç metni örtmeyecek biçimde kur; kim-ne zaman-nerede-niçin renk kodları ayrı olsun.", "İki cümlelik metinde açık bilgi ile çıkarıma dayalı bilgiyi ayır.", "Kısa paragraftan 5N1K tablosunu bağımsız doldur ve her cevabın geçtiği bölümü işaretle."),
"u09": ("Karakterin yüzü hazır emojiyle verilmesin; beden dili ve olay ipuçları sahnede ayrı ayrı görünsün.", "Aynı olayda iki karakterin farklı duygusunu nedenleriyle karşılaştır.", "Öğrenci karakterin duygusunu ve metindeki iki kanıtını bir cümleyle ifade etsin."),
"u10": ("Tohumların üzerinde ana fikirler; yapraklarda destekleyici ayrıntılar olsun. Önce ayrıntılar, sonra ana fikir eşleşsin.", "Konu ile ana fikir seçenekleri özellikle karşılaştırılsın; 'arılar' konu, 'çalışmak önemlidir' ana fikir olarak ayrıştırılsın.", "Yeni paragraf için öğrenci ana fikri kendi cümlesiyle yazıp iki ayrıntıyla desteklesin."),
"u11": ("Fosforlu kalem aynı anlamlı sözcük çiftlerini cümlede renklendirsin; hedef sözcük baştan cevabı söylemesin.", "Eş anlamlı sözcüklerin her cümlede birebir yer değiştiremeyebileceğini basit bağlamlarla göster.", "Öğrenci iki eş anlamlıyı farklı cümlelerde kullanıp anlamın korunduğunu kontrol etsin."),
"u12": ("Asansörün katları giriş-gelişme-sonuç olsun; cümleler sabit kartlarda ve zaman bağları görünür durumda sıralansın.", "Dört cümleli metinde uygun olmayan bir ayrıntıyı çıkarıp kalanları sırala.", "Öğrenci üç cümlelik bir paragraf yazsın ve her cümleyi ilgili kata yerleştirsin."),
"u13": ("Akvaryum baloncukları gerçek cümle parçaları olsun; virgül ve soru işareti yemleri doğru boşluğa bırakıldığında cümle sesli okunsun.", "Virgülün hitap ve sıralama görevleri ayrı örneklerle çalışılsın.", "Öğrenci iki cümleye işaret ekleyip tonlama farkını sesli okumayla kanıtlasın."),
"u14": ("Kütüphane kapılarında mevsim, zaman ve hava seçenekleri olsun; metindeki ipuçları mum ışığıyla tek tek bulunabilsin.", "Birden çok ipucunun aynı sonuca götürdüğü ve tek ipucunun yetersiz olduğu örnekler kullan.", "Öğrenci çıkarımını 'Bence... çünkü metinde...' kalıbıyla yazsın."),
"u15": ("Işıldak hedef sözcük yerine bağlam ipuçlarını aydınlatsın; seçenekler hareket etmeden sabit bilgi kartlarında dursun.", "Yakın anlamlı iki seçenek arasında cümleye en uygun olanı kanıtla seçtir.", "Tahmin, sözlük kontrolü ve yeni cümlede kullanım üç adımlı olarak tamamlanmalı."),
"u16": ("Harita üzerinde gerçek meşe, sağ dönüş, kaya ve kazı noktası bulunsun; yönerge okunduktan sonra metin isteğe bağlı küçülsün.", "Sağ-sol ve önce-sonra içeren dört adımlı yeni rota uygulat.", "Öğrenci arkadaşına üç adımlı bir hazine yönergesi yazıp başka bir rotada test etsin."),
"u17": ("Sohbet balonları gerçek karakterlerin yanında açılıp uygun hitap ve cevap seçildikten sonra diyalog devam etsin.", "Aynı isteğe arkadaş, öğretmen ve yabancı yetişkin için farklı uygun cevaplar karşılaştırılsın.", "Öğrenci kısa bir nezaket diyaloğunu sesli canlandırsın veya iki balon yazsın."),
"u18": ("Gerçek tren vagonlarında sözcükler, valizlerde zıtları bulunsun; köprü kutuları kaldırılıp çiftler yan yana seyahat etsin.", "Sıcak-soğuk gibi kolay çiftlerden önce-sonra ve erken-geç gibi bağlama duyarlı çiftlere geç.", "Öğrenci iki zıt çifti aynı kısa paragrafta kullanarak anlam farkını yazsın."),
"u19": ("Köprünün sol kıyısı neden, sağ kıyısı sonuç olsun; her kalas bağlantı sözcüğüyle birlikte yerleşsin.", "Çünkü ve bu yüzden kullanılarak aynı ilişki iki yönde ifade edilsin.", "Öğrenci bir doğa ve bir günlük yaşam neden-sonuç cümlesi yazsın."),
"u20": ("Gerçek yatay zaman şeridi ve tarihî görsel kartlar kullan; roket-yakıt sahnesini kaldır.", "Dört olayda 'önce/daha sonra/en sonunda' ipuçlarını ayırt ettir.", "Öğrenci sıraladığı olayları üç cümlelik sözlü anlatımla özetlesin."),
"u21": ("El yazması defter sabit sayfa olarak açılsın; parlayan sözcük ve bağlam ipuçları aynı görüş alanında kalsın.", "Bir sözcüğün iki yakın anlamını farklı tarihî cümlelerde karşılaştır.", "Öğrenci tahminini sözlükle kontrol edip yeni cümle kurarak yazsın."),
"u22": ("Paraşütler gerçekten gökyüzünden insin; kalkan kontrolü belirgin olsun ve kapsül/radar terimleri görünmesin.", "Aynı cümlenin işaret değişince tonunun ve anlamının nasıl değiştiğini dinlet.", "Öğrenci törenle ilgili üç cümleyi yazıp nokta-soru-ünlemle tamamlasın."),
"u23": ("Yırtık mektup görseli ve önceki cümleleri taşıyan sabit kâğıt kullan; devam seçeneği metnin üslubuna uysun.", "İki makul devam arasından kişi, zaman ve duygu tutarlılığına göre seçim yaptır.", "Öğrenci mektuba kendi iki cümlelik sonunu yazıp metinle bağını açıklasın."),
"u24": ("Gerçek Venn aynası kullan; Atatürk'ün çocukluğu ve öğrencinin yaşamı için kanıt kartları ayrı bölgelerde toplansın.", "Benzerlik ile aynı olma kavramlarını ayıran yeni özellikler ekle.", "Öğrenci bir benzer ve bir farklı yönü tam cümleyle yazsın."),
"u25": ("Tarihî sokak ve farklı gerçek tabela yüzeyleri kullan; su altı balıkları ile ağ tamamen kaldır.", "Aynı kelimeyi matbaa, el yazısı ve sade okul yazısında; benzer sözcük çeldiricileriyle ayırt ettir.", "Öğrenci seçtiği tabelayı yüksek sesle okuyup harf biçimi değişse de sözcüğün aynı kaldığını açıklasın."),
"u26": ("Telgraf metninde cümle başı ve özel adlar sabit satırlarda dursun; dokununca yalnız ilk harf düzeltilsin.", "Kişi, şehir, bayram ve kurum adlarını ayrı örneklerde çalıştır.", "Öğrenci iki cümleyi klavyeyle yeniden yazıp büyük harfleri bağımsız kullansın."),
"u27": ("Gerçek gramofon kaydı dinlet; terazide 'doğru/yanlış' seçmeden önce öğrencinin bildiği kanıtı seçmesini iste.", "Kısmen doğru fakat eksik bilgilerle bütünüyle yanlış bilgileri ayır.", "Öğrenci kararını 'Biliyorum çünkü...' cümlesiyle sesli veya yazılı gerekçelendirsin."),
"u28": ("23 Nisan tören alanında öğretmen, arkadaş ve misafir karakterleri görünsün; hitap seçilince kısa diyalog devam etsin.", "Selamlaşma, hitap ve vedalaşmayı aynı konuşmanın farklı yerlerinde uygulat.", "Öğrenci seçilen kişiyle iki turlu uygun diyaloğu sesli canlandırsın."),
"u29": ("Ağacın gövdesinde ana fikir, yapraklarda etiket taşımayan olay örnekleri olsun; balık-ağ motoru kaldır.", "Doğrudan destekleyen, ilgisiz ve ana fikre ters örnekleri ayrı dallara yerleştir.", "Öğrenci ana fikri destekleyen kendi örnek cümlesini yeni yaprağa yazsın."),
"u30": ("Stüdyoda ses dalgası, vurgu düğmesi ve iki gerçek ses kaydı kullan; meteorlara nişan alma yerine dinleyip karşılaştır.", "Aynı dizeyi düz, aşırı ve uygun vurguyla dinletip farkı buldur.", "Öğrenci dizeyi kaydedip vurgu, hız ve tonlama rubriğiyle öz değerlendirsin."),
"u31": ("Şifre kasasında konu, ana fikir ve ayrıntı için ayrı çarklar olsun; kasa yalnız ana ileti ve kanıt birlikte seçilince açılsın.", "Aynı konudaki iki metnin farklı ana iletilerini karşılaştır.", "Öğrenci ana iletiyi kendi cümlesiyle yazıp metinden bir kanıt eklesin."),
"u32": ("Gerçek orman sahnesinde canlılar yürüyen-uçan-sürünen bölgelerine gözlenen özellikleriyle yerleşsin.", "Aynı canlının birden çok özelliğini ve sınıflandırma ölçütünün değişebileceğini göster.", "Öğrenci yeni bir canlı ekleyip hangi gruba neden koyduğunu yazsın."),
"u33": ("Yağmur damlalarında mı/mi/mu/mü ayrı renk değil aynı görünümde olsun; seçim son ünlü dinlenip bulunarak yapılsın.", "Soru edatının ayrı yazımı ve ünlü uyumu birlikte çalışılsın.", "Öğrenci dört edatın her biriyle bir soru cümlesi yazsın ve sesli okusun."),
"u34": ("İklim makinesinde neden ve sonuç kabloları gerçek hava olaylarını bağlasın; etiket köprüsü yerine süreç animasyonu kullan.", "Tek neden-tek sonuçtan zincirleme iki sonuca geç.", "Öğrenci gözlediği bir hava olayı için neden-sonuç cümlesi kursun."),
"u35": ("Bukalemun şiir kâğıdında benzetilen ve benzeyen renkli ipuçlarıyla görünsün; seçenekler sabit dursun.", "Gibi ve kadar kullanılan uygun/uygunsuz benzetmeleri karşılaştır.", "Öğrenci doğadan bir varlık için özgün benzetme dizesi yazıp okusun."),
"u36": ("İzci günlüğü ve fenerle bağlam ipuçları aydınlatılsın; hareketli uzay hedefleri kaldır.", "Aynı sözcüğü iki farklı doğa cümlesinde anlam değişimiyle incele.", "Tahmin-sözlük-yeni cümle döngüsünü öğrenci bağımsız tamamlasın."),
"u37": ("Gerçek fotoğraf kadrajı sabit kalsın; cümleler balık değil fotoğraf alt yazısı kartları olsun.", "Görseli anlatan doğru cümleler olay, yer ve ayrıntı olarak sınıflansın.", "Öğrenci fotoğraf için en az iki bağlantılı cümle yazıp başlık eklesin."),
"u38": ("Kitap kapağı ve başlık büyük gösterilsin; konu seçenekleri ancak öğrenci iki görsel ipucunu işaretleyince açılsın.", "Aynı başlığa uyan iki kapaktan daha güçlü olanı kanıtla seçtir.", "Öğrenci yeni başlık için kapak taslağını seçip tahmin cümlesi yazsın."),
"u39": ("Terazide görüşün iki yanında katılıyorum/katılmıyorum alanları ve gerekçe ağırlıkları olsun.", "Aynı görüş için güçlü-zayıf gerekçeleri karşılaştır.", "Öğrenci kendi kararını ve nedenini tam cümleyle sesli veya yazılı ifade etsin."),
"u40": ("Papağanın gerçek ses kayıtlarını yavaş, çok hızlı, duraksamalı ve uygun biçimde dinlet; yazılı etiket cevabı vermesin.", "Hız, ses yüksekliği ve anlaşılırlığı ayrı ölçütlerle ayırt ettir.", "Öğrenci aynı cümleyi kaydedip papağanla karşılaştırarak öz düzeltme yapsın."),
"u41": ("Geri dönüşüm fabrikasında nesneler bant üzerinde sabit karar noktalarına gelsin; metindeki nesne ile kutu rengi tutarlı olsun.", "Malzeme türü ile atık/yeniden kullanım amacını ayrı sınıflandırmalarla göster.", "Öğrenci yeni üç nesneyi tabloya yazıp sınıflandırma gerekçesi eklesin."),
"u42": ("Orman postacısı gerçek mektup kartlarını yuvalara götürsün; kısa mesaj ayrıntı kartlarıyla genişletilsin.", "Kim-nerede-ne yaptı ayrıntılarıyla tek cümleyi iki bağlantılı cümleye dönüştür.", "Öğrenci kısa bir posta mesajını üç cümle olarak yazsın."),
"u43": ("Konuşmacı ve dinleyici hayvanlar sahnede görünsün; doğru davranışlar hareketli balık değil sabit sahne ayrıntıları olsun.", "Göz teması, ses yüksekliği, sıra ve beden dili ayrı örneklerle değerlendirilir.", "Öğrenci 30 saniyelik konuşma yapıp basit dinleyici rubriğiyle geri bildirim alsın."),
"u44": ("Gerçek sözlük sayfaları ve alfabetik ayraçlar kullan; roket yerine sözcük kartları sayfaya yerleşsin.", "İlk harf eşit olduğunda ikinci harfe bakarak sıralama yaptır.", "Öğrenci beş yeni sözcüğü bağımsız sözlük sırasına yazsın."),
"u45": ("Sessiz okuma ekranında süre yalnız başlangıç-bitiş arasında ölçülsün; metin bitince anlam soruları sabit kartlarda açılsın.", "Kısa metinde açık bilgi, çıkarım ve ana fikir sorularını ayır.", "Öğrenci okuma stratejisini ve zorlandığı bölümü öz değerlendirme kutusuna işaretlesin."),
"u46": ("Kitap kurdunun odasında ışık, masa, ses ve oturuş gerçek nesneler olarak düzenlensin; balık ağı kaldır.", "Birden çok uygun düzen arasından neden daha iyi olduğunu seçtir.", "Öğrenci kendi okuma köşesi için üç maddelik plan yazsın."),
"u47": ("Gerçeklik tarayıcısı her cümlede kanıt düğmesi açsın; doğru/yanlış seçmeden önce güvenilir bilgi kaynağı seçilsin.", "Olası, gerçek ve hayal ürünü ifadeleri ayrı kategorilerde çalıştır.", "Öğrenci seçtiği bir bilginin neden gerçekçi olduğunu cümleyle açıklasın."),
"u48": ("Tiyatro sahnesinde karakter yüzü ve bedeni görünür olsun; jest-mimik seçenekleri hareketli meteor yerine canlandırılsın.", "Aynı cümlenin sevinç, korku ve şaşkınlıkla farklı beden dilini karşılaştır.", "Öğrenci cümleyi seçilen duyguya uygun biçimde canlandırıp kaydetsin."),
"u49": ("Postane zarflarında tam adlar, damgalarda kısaltmalar bulunsun; eşleşince gerçek posta damgası basılsın.", "Noktalı ve noktasız kısaltmaları yaş düzeyine uygun örneklerle ayır.", "Öğrenci üç kısaltmayı cümle içinde doğru yazsın."),
"u50": ("Broşürün gerçek bölümleri - harita, saat, hayvan bilgisi - aynı sayfada görünür olsun; cümleler ilgili alana bağlansın.", "Metin ile görselin birbirini tamamladığı ve çeliştiği örnekleri karşılaştır.", "Öğrenci broşürden iki bilgi bulup kendi cümlesiyle yazsın."),
"u51": ("Editör masasında metin satır satır düzenlenebilsin; hatalı kelimeye dokununca doğru biçim otomatik gelmesin, seçenek veya klavye açılsın.", "Yazım, büyük harf ve noktalama hatalarını ayrı renk kodlarıyla buldur.", "Öğrenci kısa paragrafı yeniden okuyup bütün hataları bağımsız düzeltsin."),
"u52": ("Tablet ve basılı sözlük iki gerçek kaynak olarak açılsın; öğrenci kelimeyi arama kutusuna yazıp anlamı cümleyle eşleştirsin.", "Bir sözcüğün birden çok anlamından bağlama uyanı seçtir.", "Öğrenci kaynak adını, bulduğu anlamı ve yeni cümlesini yazsın."),
"u53": ("Kitap kapağı yapbozu sabit parçalarla başlık, görsel ve yazar alanını tamamlasın; balık-ağ görünmesin.", "Başlığa uygun fakat ayrıntısı yanlış iki kapağı karşılaştır.", "Öğrenci seçtiği kapağa bir alt başlık ve tahmin cümlesi yazsın."),
"u54": ("Dinleme odasında kapatılabilir televizyon, açık pencere, konuşan kişiler ve uygun oturuş nesneleri olsun.", "Dış çevre engeli ile öğrencinin kendi davranışını ayır.", "Öğrenci iyi dinleme ortamı için üç maddelik kontrol listesi yazsın."),
"u55": ("Kelime aşçısında sözcük kavanozları sabit; cümle tenceresinde bağlam ipuçları renklenmeden okunabilir olsun.", "Yakın anlamlı iki sözcüğün hangi cümlede uygun olduğunu karşılaştır.", "Öğrenci seçilen sözcükle yeni bir cümle yazıp anlamını doğrulasın."),
"u56": ("Mikrofon ve yatay gün çizelgesi kullan; olaylar roket yakıtı değil sabah-öğle-akşam kartları olsun.", "Dört olayı zaman ifadeleriyle sırala ve gereksiz ayrıntıyı çıkar.", "Öğrenci gününü üç bağlantılı cümleyle sesli anlatıp kayıt alsın."),
"u57": ("Matbaa bandında hatalı baskı sabitlenebilsin; dokununca otomatik çözüm yerine ilk harf/son işaret düzenleyici açılsın.", "Cümle başı, özel ad ve nokta hatalarını karışık metinde buldur.", "Öğrenci iki cümleyi klavyeyle doğru biçimde yeniden yazsın."),
"u58": ("Robotun tam bedeninin görüldüğü prova sahnesi kullan; hareket kartı seçildiğinde jest gerçek animasyonla gösterilsin.", "Aynı söz için uygun ve aşırı beden dilini karşılaştır.", "Öğrenci seçilen cümleyi uygun beden diliyle canlandırıp değerlendirsin."),
"u59": ("Uzaylı bilgi ekranında cümleler sabit veri kartları olarak dursun; gerçek dışı olan için kanıt görseli açılsın.", "Gerçek, mümkün ve hayal ürünü ifadeleri üç grupta sınıflandır.", "Öğrenci bir gerçek ve bir hayal cümlesi yazıp aralarındaki farkı açıklar."),
"u60": ("Gerçek Venn aynasında iki metnin mesaj kartları ortak ve farklı bölgelere yerleşsin.", "Konu benzerliği ile ileti benzerliğini ayrı örneklerde karşılaştır.", "Öğrenci ortak iletiyi ve her metne özgü bir farkı cümleyle yazsın."),
"u61": ("Dijital mektup ekranında hitap, gövde ve kapanış için gerçek yazı alanları olsun; hazır parçalar yalnız ilk turda destek versin.", "Arkadaş ve öğretmene yazışmada üslup farkını uygulat.", "Öğrenci kısa mektubu baştan sona kendi yazar; gönderme eylemi yok, yalnız ön izleme yapılır."),
"u62": ("Kütüphane raflarında kitap kapakları ve çocukların ilgi kartları birlikte görünsün; seçim gerekçesi ayrı alan olsun.", "Bir çocuğun birden çok ilgisine uyan iki metni amaç açısından karşılaştır.", "Öğrenci kendi ilgisini yazıp uygun metni seçerek nedenini açıklar."),
"u63": ("Gerçek film şeridinde olay kareleri sabit olsun; her kare altında kısa açıklama alanı bulunsun.", "Beş olay içinde geri dönüş veya aynı anda olma ipucunu ayırt ettir.", "Öğrenci sıralanan filmi üç cümlelik özet olarak yazar."),
"u64": ("Kürsü öncesi not kartları giriş-gelişme-sonuç panosuna yerleşsin; roket sahnesi kaldır.", "Ana fikir, örnek ve kapanış cümlesini uygun bölüme seçtir.", "Öğrenci bir dakikalık konuşma planını kendi üç maddesiyle yazar ve sunar."),
"u65": ("Yazarın odasında masa, ışık, oturuş, ses ve araçlar gerçek nesneler olarak düzenlensin.", "Fiziksel düzen ile planlama/odaklanma davranışlarını ayır.", "Öğrenci kendi yazma ortamı için düzenleme planı ve kontrol listesi yazar."),
"u66": ("İki gerçek ses kaseti sırayla dinlet; ortak ileti seçenekleri sesler bitmeden görünmesin.", "Ortak konu ile ortak mesajı farklı örneklerle ayır.", "Öğrenci iki kaydın ortak iletisini kendi cümlesiyle sesli söyler."),
"u67": ("Yetenek galerisi çerçevelerinde başlık ve etiket taşımayan kapak görselleri kullan.", "Aynı başlığa uyan iki kapakta güçlü-zayıf kanıtları karşılaştır.", "Öğrenci yeni bir yetenek başlığına kapak ve kısa tanıtım cümlesi tasarlar."),
"u68": ("Hikâye sesli dinletildikten sonra olay baloncukları sabit kalsın; yazılı hikâye ilk turda görünmesin.", "Geçen olay, çıkarılabilecek olay ve hiç geçmeyen olayı ayır.", "Öğrenci dinlediği üç olayı oluş sırasıyla anlatır veya yazar."),
"u69": ("Ön bilgi köprüsünün bir yanında dinlenen bilgi, diğer yanında öğrencinin bildiği görsel/not kartları olsun.", "Yeni bilgi ile ön bilginin uyuştuğu ve çeliştiği durumları karşılaştır.", "Öğrenci 'Önceden..., şimdi...' kalıbıyla iki cümle kurar."),
"u70": ("Dijital sözlükte arama, madde başı ve anlam seçimi gerçekten uygulanmalı; uzay meteoru kullanılmamalı.", "Birden çok anlam içinden cümleye uygun olanı seç.", "Öğrenci sözcüğü arar, anlamı yazar ve yeni cümlede kullanır."),
"u71": ("Piyano tuşları gerçek noktalama işaretlerini taşısın; basınca cümle uygun tonla seslendirilsin.", "Virgül, iki nokta ve tırnağın farklı görevlerini ayrı örneklerle çalıştır.", "Öğrenci eksik işaretleri klavyeyle ekleyip cümleyi sesli okur."),
"u72": ("Tiyatro sahnesinde doğru/yanlış davranışlar kısa animasyon olarak dursun; balık kartı yerine beden bütünlüğü görülsün.", "Göz teması, duruş, el hareketi ve sahne alanı kullanımını ayrı değerlendir.", "Öğrenci kısa sahne denemesi yapıp iki ölçütle öz değerlendirme gerçekleştirir."),
"u73": ("Vurgu stüdyosunda cümle sabit ve her sözcük ayrı ses düğmesiyle erişilebilir olsun; büyüteç metni örtmesin.", "Aynı cümlede vurgu yeri değişince anlamın nasıl değiştiğini karşılaştır.", "Öğrenci istenen anlama göre cümleyi kaydedip vurguyu öz değerlendirir."),
"u74": ("Zaman makinesinde önce-şimdi-sonra pencereleri olsun; ortadaki olay sabit, tahmin kartları zaman yerine yerleşsin.", "Birden çok olası tahminden metinle tutarlı olanı gerekçeyle ayır.", "Öğrenci olayın öncesi ve sonrası için birer cümle yazar."),
"u75": ("Hologram görselleri sabit, ses kayıtları ayrı oynatılabilir olsun; doğru eşleşme görsel ayrıntıya dayanmalı.", "Bir ses kaydına uyan iki görselde ayırt edici ayrıntıyı seçtir.", "Öğrenci bir hologramı iki cümleyle sözlü betimler."),
"u76": ("Deney raporunda hedef ve zıt sözcükler sabit satırda dursun; mıknatıs seçilen çifti gerçek kutuplara çeksin.", "Bağlama göre zıtlık oluşturan ve yalnız ilgisiz olan sözcükleri ayır.", "Öğrenci iki zıt çifti kullanarak karşılaştırma cümleleri kurar."),
"u77": ("Devre uçları iki cümle parçası, çipler ve/ama/çünkü/ile olsun; seçilince anlam ilişkisi animasyonla doğrulansın.", "Aynı iki cümlede farklı bağlaçların anlamı nasıl değiştirdiğini karşılaştır.", "Öğrenci dört bağlama ögesinden ikisiyle kendi cümlelerini kurar."),
"u78": ("Seyir defteri, sıcaklık/ışık/yüzey verileri ve gezegen görseli aynı ekranda sabit dursun.", "Doğrudan veri ile veriden yapılan çıkarımı ayrı sütunlarda sınıflandır.", "Öğrenci iki veriye dayanarak bir çıkarım cümlesi yazar."),
"u79": ("Kuş ve uçak yan yana sabit şemada gösterilsin; ortak ve farklı özellikler hareketli balık yerine işaretlenebilir olsun.", "Görünüş, hareket ve yapı ölçütlerini ayrı ayrı karşılaştır.", "Öğrenci bir ortak ve iki farklı özelliği tam cümleyle yazar."),
"u80": ("Gerçek atölye bandında hareket eden/duran, elektrikli/elektriksiz gibi açık ölçüt kutuları olsun.", "Aynı nesneyi farklı ölçütle yeniden sınıflandır.", "Öğrenci seçtiği ölçütü başlık olarak yazıp yeni üç nesneyi sınıflandırır."),
"u81": ("Kültür sözlüğünde gerçek madde başı, görsel ve örnek cümle bulunsun; uzay lazeri kaldır.", "Geleneksel sözcüğün tahmini ile sözlük anlamını karşılaştır.", "Öğrenci anlamı kendi sözüyle yazar ve yeni cümlede kullanır."),
"u82": ("Tarihî mekân fotoğrafları ve rehber cümleleri aynı kitap sayfasında eşleştirilsin; köprü kutuları kullanılmasın.", "Benzer iki mekânda mimari ipuçlarıyla doğru bilgiyi ayır.", "Öğrenci seçtiği mekân için bir rehber cümlesi yazar."),
"u83": ("Bayram sabahı ev içi zaman şeridi kullan; adımlar roket yerine sabah rutini görselleri olsun.", "Nazik ve kültürel olarak uygun sıralama ile rastgele sırayı karşılaştır.", "Öğrenci kendi ailesi için üç adımlı bayram yönergesi yazar."),
"u84": ("Gerçek form alanları ve Ali'nin bilgi kartı yan yana dursun; sürükleme sonrası alan etiketleri okunabilir kalsın.", "Ad-soyad, yaş, sınıf ve tarih alanlarını farklı bilgi türleri olarak ayır.", "Öğrenci kurgusal ikinci karakterin formunu klavyeyle bağımsız doldurur; kişisel veri istenmez."),
"u85": ("Karar ve neden iki ayrı adım olsun; neden seçenekleri ilk karar verilmeden görünmesin.", "Aynı görüş için ilgili, ilgisiz ve çelişkili gerekçeleri ayır.", "Öğrenci yeni bir görüşe katılımını kendi nedeni ile sözlü/yazılı ifade eder."),
"u86": ("Halı desenlerinde benzeyen-benzetilen çiftleri görselleştir; seçenekler sabit dursun.", "Gibi/kadar ile uygun ve anlamsız benzetmeleri karşılaştır.", "Öğrenci kültürel bir nesne için özgün benzetme cümlesi söyleyip yazar."),
"u87": ("Bayram şiirinin gerçek ses kaydı ve satırları senkron ilerlesin; hatalar balık kartı değil zaman çizgisinde işaretlensin.", "Atlama, yanlış okuma, aşırı hız ve uygunsuz duraklamayı ayrı örneklerle buldur.", "Öğrenci şiiri yeniden okuyup kendi kaydındaki bir hatayı düzeltir."),
"u88": ("Sınıf sohbetinde konuşan kişi, el kaldıranlar ve dinleyenler tam sahne olarak görünsün.", "Söz alma zamanı, dinleme duruşu ve söz kesmeme ayrı durumlarda seçilsin.", "Öğrenci gerçek mini sohbette bir kez uygun zamanda söz alıp öz değerlendirir."),
"u89": ("Hazine kutusunda metin, konu etiketi ve kanıt anahtarı üç adımda açılmalı; hareketli meteorlar kaldır.", "Konu ile ana fikir ve ayrıntıyı karşılaştıran iki metin kullan.", "Öğrenci metnin konusunu kendi sözüyle yazıp bir kanıt işaretler."),
"u90": ("Müze gezisinde görevli, arkadaş ve nine gerçek karakterler olarak görünsün; konuşma balonları uygun kişiye sürüklensin.", "Aynı isteği resmî, samimi ve saygılı aile üslubuyla yeniden kur.", "Öğrenci seçilen bir kişi için iki cümlelik uygun konuşmayı sesli canlandırır."),
}

assert set(DESIGNS) == {g["id"] for g in games}


def modality(game):
    out = game["outcome"]
    if "T.Y." in out:
        return "writing"
    if "T.K." in out:
        return "speaking"
    if "T.D." in out:
        return "listening"
    return "reading"


def config_summary(game):
    cfg = game["config"]
    t = game["type"]
    if t == "dragMatch":
        return f"Kaynakta {len(cfg.get('sources', []))} sürüklenebilir parça ve {len(cfg.get('targets', []))} hedef bulunuyor; yapı tek sabit eşleştirme turu olarak tanımlı."
    if t == "orderSequence":
        return f"Kaynakta {len(cfg.get('items', []))} kartlık tek sıra var; doğru sıra sabit ve yeni metin/olay turu üretilmiyor."
    if t == "choiceQuestion":
        steps = cfg.get("steps", [])
        opts = max([len(s.get("options", [])) for s in steps] or [0])
        return f"Kaynakta {len(steps)} çoktan seçmeli adım ve adım başına en çok {opts} seçenek bulunuyor; öğrenci serbest yanıt üretmiyor."
    if t == "catchDrop":
        return f"Kaynakta {len(cfg.get('rounds', []))} düşen-nesne turu var; doğru sembol ve yanlışlar önceden tanımlı, hız ile karar aynı puana bağlanıyor."
    if t == "wordHighlight":
        return f"Kaynakta tek metin üzerinde {len(cfg.get('rounds', []))} bulma adımı var; cevap sözcükleri önceden sabitlenmiş."
    return f"Kaynakta {len(cfg.get('items', []))} hareketli kart ve {len(cfg.get('correct', []))} doğru seçim tanımlı; yapı tek sabit seçim havuzu kullanıyor."


def modality_evidence(m):
    return {
        "writing": "Başarı kaydına öğrencinin ürettiği yazı, düzelttiği bölüm ve kullandığı kural eklenmeli; yalnız seçilen kart kimliği yeterli değildir.",
        "speaking": "Başarı kaydına kısa ses üretimi veya öğretmen/öz değerlendirme rubriği eklenmeli; yalnız seçilen seçenek konuşma kanıtı değildir.",
        "listening": "Başarı kaydına ilk dinlemedeki yanıt, tekrar sayısı ve işitsel kanıt eklenmeli; yazılı ipucuyla verilen cevap ayrı tutulmalıdır.",
        "reading": "Başarı kaydına seçilen yanıtla birlikte metinde işaretlenen kanıt ve gerekçe eklenmelidir.",
    }[m]


GROUP_FOCUS = {
    "Tema 1 · Değerlerimizle Varız": ["Değer kavramı yalnız doğru davranış kartını seçmekle değil, metindeki davranış kanıtı ve öğrencinin gerekçesiyle kurulmalı.", "Masal, kapak, ağaç, köprü ve robot başlıkları gerçek sahne ve eylem olarak görünmeli.", "Yazma ve konuşma kazanımlarında serbest üretim son turda zorunlu olmalı."],
    "Okuma-Anlama Atölyesi": ["Açık bilgi, çıkarım, ana fikir, sözcük anlamı ve metin yapısı birbirinden ayrılmalı.", "Metin büyüteç, hareketli nesne veya üst konuşma balonu tarafından örtülmemeli.", "Her doğru cevap metindeki görünür kanıtla doğrulanmalı."],
    "Tema 2 · Atatürk ve Millî Değerlerimiz": ["Tarihî içerik yaş düzeyine uygun, somut ve doğrulanabilir metin/görsellerle sunulmalı.", "Tören, tren, telgraf, gramofon ve stüdyo sahneleri ortak uzay/köprü motoruna düşmemeli.", "Hitap, vurgu ve ana ileti gerçek sözlü/yazılı üretimle ölçülmeli."],
    "Tema 3 · Doğada Neler Oluyor?": ["Doğa olayları neden-sonuç, sınıflandırma ve gözlem kanıtıyla görünür süreçlere bağlanmalı.", "Hareketli kart yakalama, okuma ve düşünme süresinden ayrılmalı.", "Tahmin-sözlük-yeni cümle döngüsü tamamlanmalı."],
    "Tema 4 · Okuma Serüvenimiz": ["Okuma, dinleme ve yazma ortamı gerçek nesnelerle düzenlenebilir olmalı.", "Düzeltme oyunlarında doğru biçim otomatik verilmemeli; öğrenci gerçekten düzenlemeli.", "Broşür, kapak, tiyatro ve matbaa görselleri başlığa özgü olmalı."],
    "Tema 5 · Yeteneklerimizi Tanıyoruz": ["İlgi ve yetenek metinleri karşılaştırma, planlama ve anlatma üretimine ilerlemeli.", "Mektup, konuşma planı ve yazma ortamı görevlerinde serbest yazı alanı bulunmalı.", "Dinleme ve vurgu kazanımları gerçek ses üretimiyle kanıtlanmalı."],
    "Tema 6 · Mucit Çocuk": ["Bilimsel veri, doğrudan bilgi ve çıkarım ayrı görsel alanlarda gösterilmeli.", "Devre, hologram, mıknatıs ve atölye başlıkları gerçek neden-sonuç eylemine dönüşmeli.", "Bağlaç ve karşılaştırma görevleri öğrenci cümlesiyle tamamlanmalı."],
    "Tema 7 · Kültür Hazinemiz": ["Kültür sözcükleri, tarihî mekânlar ve bayram davranışları somut görsel/metin kanıtıyla sunulmalı.", "Kişisel veri gerektiren form yerine kurgusal karakter kullanılmalı.", "Üslup, benzetme ve söz alma görevleri gerçek konuşma/yazma üretimi içermeli."],
}

GROUP_COLORS = [CORAL, TEAL, PURPLE, GOLD, BLUE, GREEN, CORAL, PURPLE]

doc = BaseDocTemplate(
    str(OUT), pagesize=A4, rightMargin=MX, leftMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
    title="2. Sınıf Türkçe Oyunları - Ayrıntılı Düzeltmeler", author="Macera Akademi oyun incelemesi",
)
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

story = [Spacer(1, 14 * mm), P("MACERA AKADEMİ", cover_kicker),
         P("2. Sınıf Türkçe Oyunları<br/>Ayrıntılı Düzeltmeler", cover_title),
         P("90 oyunun kaynak görevleri çıkarılarak, bütün oyun motorları tek tek açılarak ve altı etkileşim türü gerçek arayüzde oynanarak hazırlanmıştır.", cover_sub)]
cover_box = Table([[P("<b>Kapsam</b><br/>Bu belge u01-u90 arasındaki 2. sınıf Türkçe oyunlarının tamamını kapsar. Her oyun için denemede görülen mevcut yapı, eğitimsel risk, özgün sahne ve yeni oynanış, üç kademeli tur, geri bildirim ve ölçülebilir kabul koşulları ayrı ayrı verilir.")]], colWidths=[153 * mm])
cover_box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL), ("BOX", (0, 0), (-1, -1), 0.7, TEAL),
                               ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                               ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12)]))
story += [cover_box, Spacer(1, 8 * mm), P("İnceleme yöntemi", h2)]
story += bullets(["2. sınıf profili seçildi; Türkçe listesindeki 90 oyunun tamamı ve kaynak yapılandırmaları karşılaştırıldı.",
                  "Eşleştirme, sıralama, çoktan seçmeli, düşen nesne, sözcük işaretleme ve dokunarak seçme motorları açıldı; örneklerde doğru sürükleme, sıra, yakalama, metin seçme ve lazer yönlendirme denendi.",
                  "Düzeltmeler başlık-sahne uyumu, okuma/dinleme/yazma/konuşma geçerliliği, serbest üretim, kademeli ipucu, üç tur ve test edilebilir kabul koşulunu birlikte ele alır."])
story += [PageBreak()]

story += [P("Testten çıkan öncelikli bulgular", h1)]
story += [box("1. 90 oyun yalnız altı ortak motora dağıtılmış", ["34 çoktan seçmeli oyun Uzay Lazerleri'ne; 21 sürükleme oyunu Eşleştirme Köprüsü'ne; 15 dokunma oyunu balık-ağ sahnesine; 10 sıralama oyunu roket-yakıt sahnesine; 7 sözcük bulma oyunu dedektif tutanağına; 3 işaret yakalama oyunu radar/kapsül sahnesine düşüyor."], PALE_CORAL, CORAL), Spacer(1, 1.7 * mm)]
story += [box("2. Başlık ile gerçek eylem sık sık çelişiyor", ["Masal Treni'nde vagon yerine roket ve YAKIT, Kelime Ormanı'nda orman yerine uzay meteorları, Tabela Avcısı'nda tarihî sokak yerine balık ve ağ, Noktalama Yağmuru'nda yağmur yerine kapsül/radar dili görülüyor."], PALE_GOLD, GOLD), Spacer(1, 1.7 * mm)]
story += [box("3. 36 yazma kazanımında gerçek yazı girişi yok", ["Bütün 90 oyun sürükleme, sıralama, seçenek, yakalama, işaretleme veya dokunma tiplerinden oluşuyor. Sözcük, cümle, yönerge, mektup, form ya da paragraf üretme alanı bulunmadığından yazma başarısı kart seçimine indirgeniyor."], PALE_BLUE, BLUE), Spacer(1, 1.7 * mm)]
story += [box("4. Konuşma ve dinleme de çoğunlukla seçime indirgeniyor", ["Vurgu, tonlama, hitap, beden dili ve anlatma hedeflerinde öğrenci ses üretmiyor. Dinleme hedefleri yazılı yönerge ve cevap seçenekleriyle ses açılmadan çözülebiliyor; tekrar dinleme ve ilk dinleme başarısı ayrı ölçülmüyor."], PALE_TEAL, TEAL), Spacer(1, 1.7 * mm)]
story += [box("5. Oyunların tamamı yüklendi, teknik çökme görülmedi", ["u01-u90 arasındaki 90 oyun tek tek açıldı; altı motorun tamamında tuval yüklendi ve konsol hatası oluşmadı. Temel sorun çalışmama değil, ölçme hedefi ile sahne/mekanik arasındaki eğitimsel uyumsuzluk."], PALE_PURPLE, PURPLE)]
story += [PageBreak()]

story += [P("Bütün 2. sınıf Türkçe oyunlarında ortak uygulama standardı", h1)]
rows = [
    [P("Sahne", box_title), P("Başlıktaki tren, kütüphane, yağmur, müze, stüdyo veya laboratuvar gerçek görsel ve oyun eylemi olarak kullanılmalı; ortak uzay/balık/köprü şablonu kaldırılmalı.", small)],
    [P("Okuma", box_title), P("Metin sabit, okunabilir ve örtüsüz olmalı; öğrenci cevaptan önce metindeki kanıtı işaretlemeli.", small)],
    [P("Dinleme", box_title), P("İlk işitsel turda cevap yazısı gizli olmalı; tekrar dinleme cezasız ve sayısı kaydedilebilir olmalı.", small)],
    [P("Yazma", box_title), P("Yazma kazanımı son turda gerçek sözcük/cümle/metin üretimi içermeli; hazır kart seçimi tek başına başarı sayılmamalı.", small)],
    [P("Konuşma", box_title), P("Vurgu, tonlama, hitap ve anlatma için kısa ses üretimi ya da öğretmen/öz değerlendirme rubriği bulunmalı.", small)],
    [P("Tur", box_title), P("Her oyun en az üç kademeli tur içermeli; içerik, seçenek sırası ve görsel örnek her açılışta değişmeli.", small)],
    [P("Yanlış", box_title), P("Yanlışta doğru cevap açılmamalı; motor hatası can kaybettirmemeli ve yalnız son adım düzeltilebilmeli.", small)],
    [P("Kanıt", box_title), P("Başarı kaydı yalnız doğru kartı değil; metin/ses kanıtı, gerekçe ve üretim örneğini de içermeli.", small)],
]
standards = Table(rows, colWidths=[28 * mm, 148 * mm])
standards.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8D4E2")), ("BACKGROUND", (0, 0), (0, -1), PALE_PURPLE),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
story += [standards, Spacer(1, 4 * mm)]
story += bullets(["Kart ve metinler ilk iki turda hareket etmeyecek; hız ancak doğruluk eşiğinden sonra isteğe bağlı akıcılık ölçütü olacak.",
                  "Ses, yazı, görsel, doğru cevap ve geri bildirim Türkçe karakterler dâhil birebir tutarlı olacak.",
                  "Bir oyun yalnız tek sabit soru/etiket havuzunu bitirdi diye tamamlanmış sayılmayacak."])
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
        f"Destekli: mevcut kazanım tek açık örnekle çalışılır; metin/ses kanıtı görünür, kartlar sabit, süre ve can cezası kapalıdır.",
        level2,
        level3,
    ]
    feedback = [TYPE_FEEDBACK[game["type"]], "Doğru yanıtta yalnız puan/konfeti değil; seçilen metin veya ses kanıtı ile kural kısa biçimde görünür olmalı.", "Bitiş ekranı üç turdaki doğruluk, ipucu/tekrar kullanımı ve öğrencinin ürettiği gerekçe/yazı/konuşma kanıtını ayrı göstermeli."]
    acceptance = [TYPE_ACCEPT[game["type"]], f"Başlıktaki sahne ve eylem gerçekten uygulanacak: {scene}", "En az üç farklı içerik turu ve her turda yeni örnek bulunacak; seçenek konumu ve doğru yanıt sırası değişecek.", modality_evidence(m)]

    accent = accent_cycle[(number - 1) % len(accent_cycle)]
    story += [header(number, game["title"], f"{game['id']} · {game['subtitle']} · {clean(game['outcome'])}", accent), Spacer(1, 1.8 * mm)]
    story += [box("Denemede görülen mevcut durum", observed, PALE_CORAL, CORAL), Spacer(1, 0.8 * mm)]
    story += [box("Eğitimsel risk", risk, PALE_GOLD, GOLD), Spacer(1, 0.7 * mm)]
    story += [P("Yeni sahne ve oynanış", h2)] + bullets(new_play, bullet_small)
    story += [P("Üç kademeli tur", h2), rounds_table(rounds), Spacer(1, 0.7 * mm)]
    story += [box("Geri bildirim ve bitiş", feedback, PALE_TEAL, TEAL), Spacer(1, 0.7 * mm)]
    story += [box("Kabul ölçütü", acceptance, PALE_BLUE, BLUE), PageBreak()]

story += [P("Son kabul kontrolü", h1), P("2. sınıf Türkçe bölümü tamamlanmadan önce", h2)]
story += bullets(["u01-u90 arasındaki 90 oyun üç kademeli turla baştan sona test edilir; görünen başlık, sahne, kontrol, ses ve hedef beceri kayıt altına alınır.",
                  "Masal Treni gerçek vagon, Kelime Ormanı gerçek bağlam tabelası, Tabela Avcısı gerçek tarihî sokak, Noktalama Yağmuru gerçek damla/şemsiye sahnesi kullanır.",
                  "36 yazma kazanımında son tur gerçek yazı üretimi içerir; kart seçimi tek başına yazma başarısı sayılmaz.",
                  "Konuşma oyunlarında kısa ses üretimi veya öğretmen/öz değerlendirme rubriği; dinleme oyunlarında yazısız ilk tur ve cezasız tekrar bulunur.",
                  "Okuma oyunlarında cevap metindeki kanıtla; sözlük oyunlarında tahmin-araştırma-yeni cümle döngüsüyle doğrulanır.",
                  "Kartlar ilk iki turda sabittir; motor hızı, nişan alma veya nesne yakalama Türkçe doğruluk puanına karışmaz.",
                  "Her oyunda en az üç farklı içerik örneği, değişen seçenek sırası, açıklayıcı yanlış geri bildirimi ve ölçülebilir kabul kaydı bulunur."])
story += [Spacer(1, 4 * mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 2. sınıf Türkçe listesindeki u01-u90 oyunlarını kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, metin/ses, mekanik, üç tur, geri bildirim, öğrenci kanıtı ve test gereksinimlerini ayrıntılı biçimde tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)

reader = PdfReader(str(OUT))
assert len(reader.pages) == 102, len(reader.pages)
print({"pages": len(reader.pages), "games": len(games), "bytes": OUT.stat().st_size, "output": str(OUT)})
