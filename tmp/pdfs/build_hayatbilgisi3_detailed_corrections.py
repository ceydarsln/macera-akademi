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
OUT = ROOT / "output/pdf/3_sinif_hayat_bilgisi_oyunlari_detayli_duzeltmeler.pdf"
GAMES_JSON = ROOT / "tmp/pdfs/hayatbilgisi3_games.json"
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
    canv.drawString(MX, 8.2 * mm, "3. Sınıf Hayat Bilgisi - Ayrıntılı Oyun Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 8.2 * mm, str(canv.getPageNumber()))
    canv.restoreState()


ENGINE = {
    "beltSort": ("bant (yürüyen bant) motoru",
        "Başlıktaki okul, sağlık merkezi, mahalle veya afet istasyonu yerine karanlık fabrika bandı açılıyor. "
        "Denemede (Afet Zaman Bandı) karar verilecek kart bandın sol kenarında tamamen kırpıldı - “Görevlilere haber vermek” ifadesinden yalnız “...ber” görünüyordu. "
        "Üç kutulu turda kutu etiketleri kutu dışına taşıyor ve kutu emojileri (çanta, uyarı, ambulans) cevabı görsel olarak ele veriyor."),
    "serveOrder": ("tepsi-servis motoru",
        "Başlıktaki plan masası, atölye, pano veya sergi yerine ahşap servis tezgâhı açılıyor; kart havuzu ve etiketler sabit. "
        "İstek metni ile kart etiketleri aynı sözcükleri kullandığında içerik değerlendirilmeden eşleştirme yapılabiliyor."),
    "catchDrop": ("radar/kapsül yakalama motoru",
        "Seçenekler kapsül içinde tek tek yukarıdan düşüyor; ipucu “Kapsülün altındaki sarı noktayı çanağın ortasına getir” diliyle veriliyor "
        "ve karar süresi düşme hızına bağlanıyor. Güvenlik ve kişilik gibi düşünme gerektiren konular refleks oyununa bağlanıyor."),
    "sentenceBuild": ("matbaa/baskı kızağı motoru",
        "Kelime kartlarından büyük harfle başlayan kart ilk sözcüğü, nokta kartı son konumu ele veriyor; makine yalnız tek sabit dizilişi kabul ediyor."),
    "orderSequence": ("roket-yakıt motoru",
        "Deprem anı, güvenlik adımları, Cumhuriyet tarihi ve iletişim tarihi gibi tamamen dünyevi konularda bile "
        "kartlar uzayda süzülüyor ve seçilenler YAKIT hunisine gidiyor; kenardaki kartlar ekrandan taşabiliyor."),
    "memoryPairs": ("hafıza kartı motoru",
        "Sahne başlıktan bağımsız yıldızlı uzay; kartlar tavandan iniyor ve “Başla! Kartları çevir” yazısı üst kart sırasının üzerine biniyor. "
        "Can göstergesi 6 kalp ile genel 3 can standardından ayrılıyor."),
    "dragMatch": ("eşleştirme köprüsü motoru",
        "Köprü görseli yok; hedef satırların solunda boş kareler, altta PARÇALAR havuzu var. "
        "Denemede (Meslek Köprüsü) altı parçanın altısı da hedefiyle aynı anlamı gösteren emojiyle işaretliydi: "
        "itfaiyeci ile “Yangınları söndürür” ateş emojisini, çiftçi ile “Yiyeceklerimizi üretir” başak emojisini paylaşıyordu. "
        "Altı parçalı turda “İnşaat işçisi” gibi uzun yazılar çipe sığmayıp iki satıra bölünüyor."),
    "jumpPath": ("sırık/basamak motoru",
        "Basamak yazıları koyu yeşil zeminde düşük kontrastta kalıyor; kararı belirleyecek bağlam (öğrencinin hangi alanda gelişmek istediği) "
        "ekranda görünmüyor, seçim sesli yönergeye ve tahmine kalıyor."),
    "tiltBalance": ("terazi motoru",
        "İki kefeli bir terazi ve “+1 sorumluluk” düğmesi var; blok eklendikçe kefe eğiliyor. "
        "Denemede sol kefede “3 hak = 3” etiketi, sağda “0 / 3” sayacı yazılıydı - yani kaç blok ekleneceği ekranda açıkça duruyordu."),
    "surveyChart": ("çetele motoru (anket sürümü)",
        "Sahne “ÇETELE TABLOSU” başlığıyla açılıyor ama oyun bir oylama; gelen oy balonu sütun başlığıyla birebir aynı olduğu için "
        "hiçbir çıkarım gerekmiyor ve sütunlarda çetele çizgisi yerine rakam artıyor."),
    "codeGrid": ("kargo/robot ızgara motoru",
        "Izgara, engel ve hedef okunaklı. Ancak ekrandaki şey bir kroki değil düz bir labirent ızgarası: sokak adı, yön oku, ölçek veya işaret noktası yok. "
        "Yön blokları yalnız yukarı/aşağı/sol/sağ oklarından oluşuyor; konum ifadeleri (sağında, karşısında, kuzeyinde) hiçbir yerde geçmiyor. "
        "Üstelik görev metni “etrafından dolaşarak okula ulaş” diyerek rotayı tarif ediyor."),
    "holdFill": ("kronometre motoru",
        "Başlıkta musluk yazıyor ama ekranın ortasında büyük bir KRONOMETRE duruyor; lavabo, musluk, kap veya kullanım sahnesi görseli yok. "
        "Görev metni gereken miktarı doğrudan söylüyor, “Hedef ... ” satırı tekrar ediyor ve ölçek üzerindeki işaret üçüncü kez gösteriyor."),
    "graphBuild": ("grafik kurma motoru",
        "Üç sütunlu boş bir grafik, kategori etiketleri ve altta blok deposu var; yapı bu dersin en oturmuş motoru. "
        "Ancak veriler kutuda hazır yazılı (“Kâğıt: 6 kutu · Plastik: 4 kutu · Metal: 3 kutu”) ve sayaç toplamı (0/13 blok) veriyor; "
        "grafikte eksen ölçeği ve sayı aralığı yok."),
}

TYPE_RISK = {
    "beltSort": "Bant hızı okuma ve karar süresine karışıyor; kenarda kırpılan kart hiç okunamadan can etkiliyor. Kutulardaki emoji ipuçları davranışı değerlendirmeden görsel eşleştirmeyle sonuca gitmeyi mümkün kılıyor.",
    "serveOrder": "İstek metni ile kart etiketi aynı sözcükleri taşıdığında öğrenci içeriği hiç değerlendirmeden eşleştirme yapabilir; özgün ürün oluşturma gibi üretim kazanımları hazır kart seçmeye iner.",
    "catchDrop": "Doğru cevabı bilmek yetmiyor; düşen kapsüle yetişmek gerekiyor. Güvenlik gibi düşünüp karar vermeyi gerektiren bir konuda hız baskısı yanlış alışkanlık üretir ve motor hatası yanlış karar gibi can kaybettirir.",
    "sentenceBuild": "Büyük harfli kart ve nokta kartı dizilişi ele veriyor; acil çağrıda ne söyleneceği ya da nazik teklif kurma gibi kazanımlar hazır kartları sıralamaya indirgeniyor.",
    "orderSequence": "Roket-yakıt sahnesi konuyla çelişip kavramı bulanıklaştırıyor; kartlardaki tarih veya numara ipuçları içerik bilgisi olmadan sıralamayı mümkün kılıyor. Deprem anı gibi hayati bir sıralamada sahne ciddiyeti zedeliyor.",
    "memoryPairs": "Eşleştirme, kavramı açıklamadan kart konumunu ezberleyerek de çözülür; görsel hafıza başarısı hayat bilgisi başarısı gibi kayda geçer.",
    "dragMatch": "Emoji eşleşmesi cevabı doğrudan verdiği için meslek, çocuk hakkı, yönetim birimi veya doğal varlık bilgisi hiç kullanılmadan oyun bitirilebilir; taşan yazılar okunamadığından eşleştirme gerekçesiz kalır.",
    "jumpPath": "Öğrencinin kendi gelişim alanı ekranda tanımlı olmadığı için “kısa vadeli mi uzun vadeli mi” kararı bağlamsız kalıyor; kazanım kişisel planlama isterken oyun genel doğru cevabı seçtiriyor.",
    "tiltBalance": "Model kavramsal olarak yanlış: haklar ile sorumluluklar bire bir sayısal denklik değildir. Çocuk hakları koşulsuzdur; eğitim hakkı, karşılığında bir sorumluluk yerine getirilmesine bağlı değildir. Terazi kurgusu “hakkın kadar sorumluluk yapmalısın, yoksa denge bozulur” mesajı veriyor. Üstelik eklenecek blok sayısı ekranda yazılı olduğu için düşünme de gerekmiyor.",
    "surveyChart": "Oy ile sütun adı aynı olduğu için veri toplama mekanik tıklamaya iner; öğrenci sonucu yorumlamadan, çoğunluk ve azınlık ilişkisini kurmadan oyunu bitirebilir.",
    "codeGrid": "Kazanım krokiyle KONUM belirlemeyi ve konumsal görselleştirmeyi istiyor; oyun ise ekran yönleriyle labirent çözdürüyor. Ekranda kroki ögesi (sokak, yön oku, işaret noktası) bulunmadığı ve konum ifadeleri hiç kullanılmadığı için kazanım ile mekanik kopuk.",
    "holdFill": "Görev metni gereken miktarı doğrudan söylediği için sürdürülebilirlik kararı öğrenciye bırakılmıyor; oyun bir zamanlama-refleks alıştırmasına dönüşüyor ve suyun nereye gittiği hiç görünmüyor.",
    "graphBuild": "Veriler hazır verildiği için “bilgi bulur ve kaydeder” kazanımının bulma yarısı hiç çalışmıyor; öğrenci sayıları okuyup blok kopyalıyor. Toplam blok sayacı da kaç blok gerektiğini ele veriyor.",
}

TYPE_FEEDBACK = {
    "beltSort": "Yanlış kutuda bant dursun; kart sabitlenip yeniden okunsun ve ölçüt doğru söylenmeden hatırlatılsın. Kenarda kırpılan kart hiç puanlanmasın.",
    "serveOrder": "Yanlış kartta tepsi kilitlenmesin; istek yeniden okunsun ve kartın neden uymadığı içerik üzerinden gösterilsin.",
    "catchDrop": "Yanlış yakalamada düşme dursun; seçenek sabitlenip yeniden karar verilsin. Kaçan kapsül can yakmasın.",
    "sentenceBuild": "Yanlışta bütün dizi bozulmasın; yalnız son kart geri alınsın. Anlamlı alternatif diziliş kurulduysa doğru kabul edilsin.",
    "orderSequence": "Yanlış adımda dizi silinmesin; yalnız son seçim geri alınsın ve “önce ne olmalı?” sorusunu düşündüren ipucu verilsin.",
    "memoryPairs": "Yanlış çiftte kartlar hemen kapanmasın; iki içerik yan yana sesli okunup farkı soran kısa bir ipucu verilsin. Can standardı diğer oyunlarla eşitlensin.",
    "dragMatch": "Yanlış parça başlangıca dönsün; hedef parlatılmasın. Eşleşmenin dayandığı bilgi kısa bir soruyla vurgulansın.",
    "jumpPath": "Yanlış basamakta düşme animasyonu ceza üretmesin; öğrencinin seçtiği gelişim alanı yeniden gösterilip iki seçenek karşılaştırılsın.",
    "tiltBalance": "Yanlış blok sayısında terazi devrilip ceza vermesin; hakkın koşulsuz olduğu, sorumluluğun ise o hakkı herkesin kullanabilmesi için taşındığı kısa bir örnekle hatırlatılsın.",
    "surveyChart": "Yanlış işaretlemede oy yeniden dinletilsin; sayım bitince sonuç doğrudan açıklanmasın, öğrenciye “en çok/en az hangisi, kaç fark var?” soruları sorulsun.",
    "codeGrid": "Engele çarpınca robot dursun ve programdaki hatalı adım işaretlensin; tüm program silinmesin. Hatalı adım krokideki işaret noktasına göre tarif edilsin.",
    "holdFill": "Fazla su akıtıldığında ceza verilmesin; taşan su görünür olsun ve “ne kadarı boşa gitti?” sorusu sorulsun.",
    "graphBuild": "Yanlış sütuna blok konursa blok geri dönsün; veri satırı yeniden okunsun ve hangi kategoriye ait olduğu sorulsun. Grafik silinmesin.",
}

TYPE_ACCEPT = {
    "beltSort": "İlk iki turda kartlar sabit gelecek; hız ancak üçüncü turda isteğe bağlı açılacak. Kart hiçbir konumda kırpılmayacak, kutu etiketi kutu içinde kalacak, kutu emojileri cevabı vermeyecek ve dokunma alanı en az 44 px olacak.",
    "serveOrder": "İstek metni ile kart etiketi aynı sözcükleri kullanmayacak; öğrenci içerikten çıkarım yapacak ve her istek farklı içerik havuzu kullanacak.",
    "catchDrop": "İlk turda düşme kapalı, seçenekler sabit olacak; başarı doğru karar ve gerekçeyle ölçülecek, yakalama refleksi puana karışmayacak.",
    "sentenceBuild": "Kartlar küçük harfle gelecek; baş harf ve son işaret öğrencinin kararı olacak. Son turda serbest yazı ya da sözlü ifade alanı bulunacak.",
    "orderSequence": "Roket-yakıt sahnesi kaldırılacak; sırayı ele veren tarih/numara ilk turda gizlenecek ve kartlar 390x844 ekranda tam içeride kalacak.",
    "memoryPairs": "Kart konumları ve içerik her açılışta karışacak; can sayısı genel standartla (3) eşitlenecek ve her eşleşme bir gerekçe adımıyla doğrulanacak.",
    "dragMatch": "Parça ve hedefteki emojiler cevabı eşleştirmeyecek; yazılar çipe sığacak, hedef alanlar en az 44 px olacak ve her eşleşme bir gerekçe sorusuyla doğrulanacak.",
    "jumpPath": "Öğrencinin geliştirmek istediği alan ilk adımda seçilecek ve ekranda sürekli görünecek; basamak yazıları zeminden ayrışan kontrastta olacak; düşme animasyonu ceza üretmeyecek.",
    "tiltBalance": "Bire bir sayısal denklik modeli KALDIRILACAK. Hakkın koşulsuz olduğu korunacak; kefeler “hak” ve “o hakkı herkesin kullanabilmesi için taşınan sorumluluk” olarak yeniden adlandırılacak ve eklenecek blok sayısı ekranda yazılı olmayacak.",
    "surveyChart": "Oy ifadeleri sütun adını birebir tekrar etmeyecek; sayım çetele çizgisiyle görünecek ve oyun ancak sonuç yorumu yapıldıktan sonra tamamlanacak.",
    "codeGrid": "Ekranda gerçek bir kroki bulunacak: sokaklar, yön oku ve en az iki işaret noktası. Rota konum ifadeleriyle (sağında, karşısında, kuzeyinde) tarif edilecek ve görev metni rotayı söylemeyecek.",
    "holdFill": "Görev metni gereken miktarı söylemeyecek; öğrenci işin ne olduğuna bakarak kendisi karar verecek. Ekranda gerçek musluk, kap ve akan su bulunacak.",
    "graphBuild": "Veriler hazır sayı olarak verilmeyecek; öğrenci önce nesneleri sayarak veriyi kendisi çıkaracak. Toplam blok sayacı gizlenecek ve grafiğe sayı ölçeği eklenecek.",
}


DESIGNS = {
"h37": ("Öğrenci ilk adımda kendi gelişim alanını seçsin (okuma, yüzme, resim) ve bu seçim ekranda sürekli görünsün; basamaklar o hedefe giden gerçek adımlar olsun.",
        "Kısa vadeli (bu hafta) ve uzun vadeli (bu yıl) adımlar karıştırılsın; öğrenci hangisinin önce geleceğine karar versin.",
        "Öğrenci kendi hedefi için bir kısa ve bir uzun vadeli planı kendi cümlesiyle söylesin veya yazsın."),
"h38": ("Gerçek bir plan masası ve takvim çizilsin; hedef kartları takvimin üzerine (bu hafta / bu ay / bu yıl) yerleşsin ve süre görünür olsun.",
        "Aynı hedefin kısa ve uzun vadeli parçaları ayrılsın: “her gün 10 sayfa” ile “yılda 20 kitap” ilişkilendirilsin.",
        "Öğrenci kendi hedefini takvime yerleştirip ilk adımı belirlesin."),
"h39": ("Gerçek bir okul ortamı çizilsin (sınıf, koridor, bahçe); ifade o ortamda kısa bir sahne olarak görünsün ve bant durdurulsun.",
        "Aynı konunun hem hak hem sorumluluk yüzü verilsin: “temiz sınıfta ders görmek” hakkı ile “çöpü kutuya atmak” sorumluluğu eşleştirilsin.",
        "Öğrenci bir hakkını ve ona bağlı sorumluluğunu kendi cümlesiyle ifade etsin."),
"h40": ("KRİTİK: bire bir sayısal denklik modeli kaldırılsın. Terazi yerine gerçek bir okul sahnesi kurulsun; her hak kartına dokununca “bu hakkı herkesin kullanabilmesi için ne yapmalıyım?” sorusu açılsın. Hakkın koşulsuz olduğu korunsun.",
        "Bir hakkın birden çok sorumlulukla, bir sorumluluğun birden çok hakla ilişkili olabildiği gösterilsin.",
        "Öğrenci sınıfında herkesin bir hakkını kullanabilmesi için üstleneceği bir sorumluluğu söylesin."),
"h41": ("Gerçek çocuk hakları görselleri (okul, sağlık ocağı, oyun parkı, aile) kullanılsın; parça-hedef emoji eşleşmesi kaldırılsın ve doğru eşleşmede hakkın karşılığı kısa sahneyle gösterilsin.",
        "Hakkın karşılanmadığı durumlar da gösterilsin; öğrenci farkı belirtsin.",
        "Öğrenci bir çocuk hakkını tanıtan kısa bir slogan veya afiş metni üretsin."),
"h42": ("Gerçek bir sınıf oylaması sahnesi kurulsun: proje panosu, kürsü ve el kaldıran öğrenciler görünsün. Oy ifadesi seçenek adını birebir tekrar etmesin ve sayım çetele çizgisiyle görünsün.",
        "Berabere biten ve tek oyla kazanılan senaryolar eklensin; çoğunluk kavramı somutlaştırılsın.",
        "Öğrenci kazanan projeyi nasıl hayata geçireceğini bir adımla anlatsın."),
"h43": ("Gerçek bir gün akışı çizilsin (uyku, kahvaltı, ekran, spor); davranış bu akışın içinde bir an olarak görünsün ve bant durdurulsun.",
        "Miktara göre değişen davranışlar eklensin (biraz tatlı / çok tatlı); ölçüt tartışılsın.",
        "Öğrenci kendi bir alışkanlığını gözden geçirip değiştireceği bir şeyi söylesin."),
"h44": ("Kapsül-radar düzeni kaldırılsın; tehlike durumu gerçek bir sahne olarak (yabancı biri, kaybolma, akran zorbalığı) gösterilsin ve seçenekler sabit kartlarda dursun.",
        "Benzer görünen ama farklı tepki gerektiren durumlar karşılaştırılsın; “önce kime haber verirsin?” sorulsun.",
        "Öğrenci güvendiği yetişkinleri ve ne söyleyeceğini kendisi belirtsin."),
"h45": ("Gerçek bir tehlike senaryosu sahnesi kurulsun; adımlar o sahnede yapılan işler olarak sıralansın ve roket kaldırılsın.",
        "Farklı tehlikeler için adım sırası değişsin; öğrenci hangi adımın önce geleceğini gerekçelendirsin.",
        "Öğrenci kurgusal bir durumda adımları baştan sona uygulasın."),
"h46": ("Gerçek bir trafik sahnesi çizilsin; kural seçilince sonucu animasyonla gösterilsin (kemer takılınca fren anında ne olur). Emoji eşleşmesi kaldırılsın.",
        "Kuralın uygulanmadığı durumun sonucu da gösterilsin; neden-sonuç bağı kurulsun.",
        "Öğrenci bir trafik kuralının nedenini kendi cümlesiyle açıklasın."),
"h47": ("Gerçek bir telefon ekranı ve görevli sesi olsun; kurulan cümle görevliye söylensin ve görevli eksik bilgi varsa sorsun. Kartlar küçük harfle gelsin.",
        "Eksik bilgi içeren cümleler çeldirici olsun (adres yok, olay belirsiz); öğrenci eksiği bulsun.",
        "Öğrenci kurgusal bir olayı kendi cümleleriyle bildirsin; adres ve olay bilgisi kaydedilsin."),
"h48": ("Gerçek bir afiş tuvali açılsın; seçilen öge afişin üzerine yerleşsin ve afiş adım adım oluşsun. Kazanım özgün ÜRÜN oluşturmayı istiyor, kart seçmeyi değil.",
        "İyi ve zayıf afiş örnekleri karşılaştırılsın: hangi mesaj daha net?",
        "Öğrenci kendi sloganını yazsın ve afişi tamamlasın."),
"h49": ("Gerçek bir mahalle sahnesi çizilsin: bir evin içi ve sokağı yan yana görünsün; özellik kartı hangi ölçekte geçtiğine göre yerleşsin ve bant durdurulsun.",
        "Hem ailede hem toplumda görülen özellikler çeldirici olsun; öğrenci ölçütü savunsun.",
        "Öğrenci ailesinin toplumun bir parçası olduğunu bir örnekle anlatsın."),
"h50": ("KRİTİK: altı parçanın altısındaki emoji eşleşmesi kaldırılsın - şu an itfaiyeci ateş emojisiyle, çiftçi başak emojisiyle hedefine bağlanıyor. Gerçek çalışma sahneleri kullanılsın ve yazılar çipe sığsın.",
        "Görünmeyen katkılar eklensin (temizlik işçisi, veri girişi); her mesleğin değerli olduğu gösterilsin.",
        "Öğrenci bir mesleğin katkısını kendi cümlesiyle anlatsın."),
"h51": ("Gerçek bir atölye sahnesi çizilsin; araç seçilince meslek sahibi onu kullanarak iş yapsın ve etiket kopyası kaldırılsın.",
        "Birden çok meslekte kullanılan araçlar çeldirici olsun.",
        "Öğrenci bir mesleği seçip gerekli araçları kendisi sıralasın."),
"h52": ("Gerçek erişilebilirlik sahneleri kullanılsın (rampa, işaret dili, sesli tabela); eşleşen çözüm o sahnede uygulansın ve engel ortadan kalksın.",
        "Aynı ihtiyaç için birden çok çözüm karşılaştırılsın.",
        "Öğrenci okulunda kolaylaştırılabilecek bir durumu ve çözümünü söylesin."),
"h53": ("Gerçek bir proje süreci görselleşsin (ihtiyacı fark et, araştır, planla, uygula, paylaş); roket kaldırılsın.",
        "Atlanan adımın sonucu gösterilsin: araştırmadan uygulamak neden sorunlu?",
        "Öğrenci kendi farkındalık projesi için adımları sırayla yazsın."),
"h54": ("Gerçek bir yardım durumu sahnesi kurulsun; kurulan cümle karşıdaki kişiye söylensin ve tepkisi görünsün. Kartlar küçük harfle gelsin.",
        "Yardımı dayatan ve izin isteyen ifadeler karşılaştırılsın: “Sana yardım edeyim” ile “Yardım etmemi ister misin?”",
        "Öğrenci kendi nazik teklifini hazır kart olmadan kursun."),
"h55": ("Gerçek tarihî mekân ve doğa fotoğrafları kullanılsın; davranış o mekânda kısa sahne olarak görünsün ve zararın izi kalsın.",
        "Niyet ile etki ayrılsın: iyi niyetli ama zarar veren davranışlar eklensin.",
        "Öğrenci çevresindeki bir mekânı korumak için yapacağı şeyi söylesin."),
"h56": ("Gerçek yönetim binaları ve görev sahneleri çizilsin; emoji eşleşmesi kaldırılsın ve eşleşme binanın işleviyle kurulsun.",
        "Hangi işin hangi birime ait olduğu günlük örneklerle çalışılsın; benzer görevli birimler ayrılsın.",
        "Öğrenci bir sorunu hangi birime ileteceğini gerekçesiyle söylesin."),
"h57": ("Gerçek dönem görselleri kullanılsın; kart çevrilince kişilik özelliği ile başarının nasıl bağlandığı kısa bir anlatımla gösterilsin.",
        "Aynı başarıya birden çok özelliğin katkısı olduğu gösterilsin.",
        "Öğrenci bir kişilik özelliğinin kendi yaşamındaki karşılığını söylesin."),
"h58": ("Kapsül-radar düzeni kaldırılsın; anlatılan davranış kısa bir anı olarak okunsun ve özellik seçenekleri sabit kartlarda dursun.",
        "Yakın anlamlı özellikler çeldirici olsun (kararlılık / inatçılık); fark tartışılsın.",
        "Öğrenci anıdaki davranıştan hangi özelliği çıkardığını gerekçesiyle söylesin."),
"h59": ("Gerçek bir okul panosu ve tören sahnesi çizilsin; seçilen kart panoya asılsın ve etiket kopyası kaldırılsın.",
        "Birliği güçlendiren ve zayıflatan davranışlar karşılaştırılsın.",
        "Öğrenci sınıfında beraberliği güçlendirecek bir davranış önersin."),
"h60": ("Gerçek yatay zaman şeridi ve dönem görselleri kullanılsın; roket kaldırılsın. İlk turda tarihler gizlensin, sıralama olay içeriğinden yapılsın.",
        "Olaylar arasındaki neden-sonuç bağı sorulsun: hangisi diğerini mümkün kıldı?",
        "Öğrenci Cumhuriyet'e giden yolu üç cümleyle anlatsın."),
"h61": ("Gerçek doğa görselleri kullanılsın; eşleşen fayda kısa bir sahneyle gösterilsin (ağaç gölge yapar, arı çiçeği tozlaştırır). Emoji eşleşmesi kaldırılsın.",
        "Bir varlığın birden çok faydası ve zincirleme etkisi gösterilsin.",
        "Öğrenci bir doğal varlığın insana faydasını kendi cümlesiyle anlatsın."),
"h62": ("KRİTİK: ekrandaki labirent ızgarası gerçek bir krokiye dönüşsün - sokaklar, yön oku, ölçek ve en az iki işaret noktası (market, park) bulunsun. Rota konum ifadeleriyle tarif edilsin; görev metni rotayı söylemesin.",
        "Aynı krokide farklı başlangıç noktaları verilsin; öğrenci konumunu “parkın karşısında” gibi ifadelerle belirtsin.",
        "Öğrenci kendi okuluna giden yolu krokide çizip konum ifadeleriyle anlatsın."),
"h63": ("Gerçek bir ev ve mahalle sahnesi çizilsin; davranış afetin hangi anında yapıldığı sahneyle görünsün. KRİTİK: kart hiçbir kenarda kırpılmasın - denemede “Görevlilere haber vermek” ifadesinden yalnız son hecesi görünüyordu. Kutu emojileri cevabı vermesin.",
        "Aynı davranışın farklı zamanlarda anlamı değişsin (çantayı hazırlamak öncesi, çantayı almak sonrası).",
        "Öğrenci ailesiyle yapacağı bir afet hazırlığını söylesin."),
"h64": ("Gerçek bir sınıf/ev sahnesi çizilsin; deprem anında adımlar o mekânda uygulanan hareketler olarak görünsün ve roket kaldırılsın. Bu hayati bir konudur, sahne ciddiyeti korumalı.",
        "Farklı mekânlar için (sınıf, sokak, asansör) adım sırası değişsin.",
        "Öğrenci bulunduğu odada çök-kapan-tutun uygulamasını yapsın."),
"h65": ("KRONOMETRE kaldırılsın; ekranda gerçek musluk, kap ve akan su olsun. Görev metni gereken miktarı SÖYLEMESİN; öğrenci işe bakarak kendisi karar versin.",
        "Farklı işler için gereken su karşılaştırılsın; ihtiyaç ile israf ayrımı kurulsun.",
        "Öğrenci taşan suyu görsün ve sürdürülebilirlik için bir davranış önersin."),
"h66": ("Veriler hazır sayı olarak verilmesin; öğrenci önce geri dönüşüm kutusundaki nesneleri sayarak veriyi kendisi çıkarsın. Toplam blok sayacı gizlensin ve grafiğe sayı ölçeği eklensin.",
        "Grafik tamamlanınca “en çok hangisi, kaç fark var?” soruları sorulsun.",
        "Öğrenci grafiği yorumlayıp sınıfı için bir öneri getirsin."),
"h67": ("Gerçek bir öncesi-sonrası sahnesi kurulsun (aşıdan önce/sonra, elektrikten önce/sonra); eşleşme bu karşılaştırmaya dayansın ve emoji eşleşmesi kaldırılsın.",
        "Bir gelişmenin birden çok etkisi ve olası bir olumsuz yanı karşılaştırılsın.",
        "Öğrenci bir bilimsel gelişmenin günlük yaşamına etkisini anlatsın."),
"h68": ("Gerçek bir günlük yaşam sahnesi çizilsin; durum ekranda canlansın (geç saatte telefon, uzaktaki akrabayla görüşme) ve bant durdurulsun.",
        "Aynı teknolojinin hem olumlu hem olumsuz kullanımı karşılaştırılsın; ölçüt kullanım biçimi olsun.",
        "Öğrenci kendi teknoloji kullanımını gözden geçirip bir kural belirlesin."),
"h69": ("Gerçek iletişim araçları müzesi vitrini çizilsin; ürünler raf üzerinde sıralansın ve roket kaldırılsın. İlk turda tarihler gizlensin.",
        "Her aracın hangi ihtiyacı çözdüğü sorulsun; hız ve erişim karşılaştırılsın.",
        "Öğrenci iletişimin nasıl değiştiğini üç aşamada anlatsın."),
"h70": ("Gerçek eser görselleri kullanılsın; kart çevrilince sanatçının eserinden kısa bir örnek görünsün veya duyulsun.",
        "Aynı sanatçının birden çok dalda üretebildiği durumlar gösterilsin.",
        "Öğrenci bir sanatçıyı ve katkısını kendi cümlesiyle tanıtsın."),
"h71": ("Gerçek bir sergi salonu çizilsin; seçilen öge duvara asılsın ve sergi adım adım kurulsun. Etiket kopyası kaldırılsın.",
        "Serginin bütünlüğü sorulsun: hangi öge eksik kalırsa ziyaretçi anlamaz?",
        "Öğrenci kendi eserini sergiye ekleyip tanıtım yazısını yazsın."),
"h72": ("Genel radar yönergesi kaldırılsın; gelişme ve etkisi gerçek bir öncesi-sonrası sahnesiyle gösterilsin ve seçenekler sabit kartlarda dursun.",
        "Aynı gelişmenin farklı alanlardaki etkileri karşılaştırılsın.",
        "Öğrenci bir gelişmenin hayatını nasıl değiştirdiğini örnekle anlatsın."),
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
    if t == "sentenceBuild":
        return f"Kaynakta {n.get('rounds','?')} cümle kurulumu var; her cümlenin tek doğru dizilişi tanımlı."
    if t == "orderSequence":
        return f"Kaynakta {n.get('items','?')} kartlık tek sıra var; doğru sıra sabit ve yeni olay turu üretilmiyor."
    if t == "dragMatch":
        return f"Kaynakta {n.get('sources','?')} parça ve {n.get('targets','?')} hedef var; tek sabit eşleştirme turu."
    if t == "jumpPath":
        return f"Kaynakta {n.get('steps','?')} basamak adımı tanımlı; her adım tek doğru etiketle sabit ve öğrencinin kendi hedefi tanımlı değil."
    if t == "tiltBalance":
        return f"Kaynakta {n.get('rounds','?')} denge turu var; her turda hak sayısı kadar sorumluluk bloğu eklenmesi bekleniyor ve bu sayı ekranda yazılı."
    if t == "codeGrid":
        return f"Kaynakta {n.get('rounds','?')} görev haritası var; program yalnız ekran yönü oklarından oluşuyor ve konum ifadesi geçmiyor."
    if t == "holdFill":
        return f"Kaynakta {n.get('rounds','?')} doldurma turu var; hedef miktar görev metninde açıkça söyleniyor."
    if t == "graphBuild":
        return f"Kaynakta {n.get('categories','?')} kategori ve toplam {n.get('blocks','?')} blok tanımlı; kategori sayıları hazır metin olarak veriliyor."
    if t == "surveyChart":
        return f"Kaynakta {n.get('options','?')} seçenek ve {n.get('responses','?')} oy tanımlı; oy ifadeleri seçenek adını birebir içeriyor ve sonuç yorumu adımı tanımlı değil."
    return f"Kaynakta {n.get('columns','?')} sütun ve {n.get('responses','?')} yanıt tanımlı; yanıt cümleleri sütun adını birebir içeriyor."


GROUP_FOCUS = {
    "Alan 1 · Ben ve Okulum": [
        "Hak-sorumluluk ilişkisi bire bir sayısal denklik olarak kurulmamalı; hakkın koşulsuz olduğu korunmalı.",
        "Kişisel planlama kazanımında öğrencinin kendi gelişim alanı ekranda tanımlı olmalı ve karar buna dayanmalı.",
        "Okul, pano ve oylama sahneleri gerçek görsellerle kurulmalı; bant, uzay ve servis tezgâhı şablonu kaldırılmalı.",
    ],
    "Alan 2 · Sağlığım ve Güvenliğim": [
        "Güvenlik kazanımları hız oyunundan çıkarılmalı; tehlike durumu sahne olarak gösterilip düşünerek karar verilmeli.",
        "Acil çağrı ve afiş kazanımları gerçek üretime bağlanmalı: öğrenci cümlesini kendisi kurmalı, afişi kendisi tamamlamalı.",
        "Trafik kuralı köprüsünde emoji eşleşmesi kaldırılmalı; kuralın nedeni sonucuyla birlikte gösterilmeli.",
    ],
    "Alan 3 · Ailem ve Toplum": [
        "Meslek köprüsündeki emoji eşleşmesi kaldırılmalı; altı parçanın altısı da şu an simgeyle çözülebiliyor.",
        "Aile-toplum ilişkisi ölçek farkını gösteren gerçek bir mahalle sahnesiyle kurulmalı.",
        "Yardımlaşma kazanımı izin isteyen nazik ifadeye ve gerçek erişilebilirlik çözümlerine bağlanmalı.",
    ],
    "Alan 4 · Yaşadığım Yer ve Ülkem": [
        "Miras, yönetim ve Atatürk kazanımları gerçek görsel kanıtla (fotoğraf, bina, dönem görseli) sunulmalı.",
        "Cumhuriyet Yolu roket sahnesinden çıkarılmalı; tarihler ilk turda gizlenip sıralama içerikten yapılmalı.",
        "Kişilik özelliği oyunları yakın anlamlı çeldiricilerle (kararlılık/inatçılık) derinleştirilmeli.",
    ],
    "Alan 5 · Doğa ve Çevre": [
        "Kroki kazanımı labirent ızgarasından çıkarılıp gerçek krokiye ve konum ifadelerine bağlanmalı.",
        "Afet oyunları hayati konudur: kart kırpılması giderilmeli, roket sahnesi kaldırılmalı, sahne ciddiyeti korunmalı.",
        "Sürdürülebilirlik oyunlarında gereken miktar söylenmemeli; grafik oyununda veri öğrenci tarafından sayılarak çıkarılmalı.",
    ],
    "Alan 6 · Bilim, Teknoloji ve Sanat": [
        "Bilimsel ve teknolojik gelişmeler öncesi-sonrası karşılaştırmasıyla somutlaştırılmalı.",
        "Zaman şeridi roket sahnesinden çıkarılıp gerçek müze vitrinine taşınmalı.",
        "Sanat kazanımları gerçek eser örnekleriyle desteklenmeli; sergi kurma gerçek üretime dönüşmeli.",
    ],
}

GROUP_COLORS = [CORAL, TEAL, PURPLE, GOLD, BLUE, GREEN]

# Kaç oyun ortak "genel yönerge" kullanıyor?
generic_prompt = [g for g in games if "doğru cevabı yakala" in g["instruction"].lower()]
belt_n = sum(1 for g in games if g["type"] == "beltSort")
answer_leak = ["h02", "h09", "h10", "h26", "h29", "h05", "h18"]

doc = BaseDocTemplate(
    str(OUT), pagesize=A4, rightMargin=MX, leftMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
    title="3. Sınıf Hayat Bilgisi Oyunları - Ayrıntılı Düzeltmeler", author="Macera Akademi oyun incelemesi",
)
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

story = [Spacer(1, 14 * mm), P("MACERA AKADEMİ", cover_kicker),
         P("3. Sınıf Hayat Bilgisi Oyunları<br/>Ayrıntılı Düzeltmeler", cover_title),
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
story += [box("1. Hak-Sorumluluk Terazisi kavramsal olarak yanlış bir model kuruyor",
    ["Oyun terazinin bir kefesine hakları, diğerine sorumlulukları koyup bire bir sayısal denklik kurduruyor: ekranda “3 hak = 3” etiketi ve “0 / 3” sayacı yazılı. Oysa haklar ile sorumluluklar sayıca eşitlenen bir takas değildir; çocuk hakları koşulsuzdur. Bir çocuğun eğitim hakkı, karşılığında bir sorumluluk yerine getirmesine bağlı değildir. Bu kurgu “hakkın kadar sorumluluk yapmalısın, yoksa denge bozulur” mesajı veriyor. Üstelik eklenecek blok sayısı ekranda yazılı olduğu için düşünme de gerekmiyor."],
    PALE_CORAL, CORAL), Spacer(1, 1.7 * mm)]
story += [box("2. Kroki kazanımı labirent ızgarasına indirgenmiş",
    ["Kroki Rehberi'nin kazanımı “krokiyi kullanarak bulunduğu yerin konumunu belirler ve konumsal görselleştirme yapar”. Ekranda ise sokak adı, yön oku, ölçek veya işaret noktası olmayan düz bir labirent ızgarası var; yön blokları yalnız yukarı/aşağı/sol/sağ oklarından oluşuyor ve konum ifadeleri (sağında, karşısında, kuzeyinde) hiçbir yerde geçmiyor. Görev metni de “etrafından dolaşarak okula ulaş” diyerek rotayı tarif ediyor. Bu, 2. sınıftaki Doğadan Yön Bulma oyununda raporladığım kusurun aynısı: aynı codeGrid motoru iki sınıfta da kazanımı taşımıyor."],
    PALE_GOLD, GOLD), Spacer(1, 1.7 * mm)]
story += [box("3. Meslek Köprüsü'nde altı eşleşmenin altısı da emojiyle çözülebiliyor",
    ["Parça ve hedef aynı anlamı gösteren emojiyi paylaşıyor: itfaiyeci ile “Yangınları söndürür” ateş emojisini, çiftçi ile “Yiyeceklerimizi üretir” başak emojisini, şoför ile “İnsanları güvenle taşır” araç emojisini taşıyor. Çocuk mesleklerin toplumsal katkısını hiç düşünmeden simge eşleyerek bitirebiliyor. Aynı kusur bu dersteki altı köprü oyununun tamamını ve 2. sınıf hayat bilgisi ile Türkçe derslerindeki köprü oyunlarını da etkiliyor. Ayrıca altı parçalı turda “İnşaat işçisi” gibi uzun yazılar çipe sığmıyor."],
    PALE_BLUE, BLUE), Spacer(1, 1.7 * mm)]
story += [box("4. Afet oyunlarında kart kırpılması ve sahne uyumsuzluğu",
    ["Afet Zaman Bandı'nda karar verilecek kart bandın sol kenarında tamamen kırpıldı - “Görevlilere haber vermek” ifadesinden yalnız “...ber” görünüyordu; üç kutunun etiketleri de kutu dışına taştı ve kutu emojileri (çanta, uyarı, ambulans) cevabı görsel olarak veriyor. Deprem Anı Adımları ise roket-YAKIT sahnesinde açılıyor. Bunlar hayati konular; sahnenin ciddiyeti koruması ve kararın dayandığı metnin tam görünmesi gerekir."],
    PALE_TEAL, TEAL), Spacer(1, 1.7 * mm)]
story += [box("5. Veriler ve miktarlar hazır veriliyor; teknik çökme yok",
    ["Geri Dönüşüm Grafiği bu dersin en oturmuş motoru, ancak veriler kutuda hazır yazılı (“Kâğıt: 6 kutu · Plastik: 4 kutu · Metal: 3 kutu”) ve sayaç toplamı (0/13 blok) veriyor; kazanımın “bilgi bulur” yarısı hiç çalışmıyor, öğrenci sayıları kopyalıyor. Sürdürülebilirlik Musluğu'nda da gereken miktar görev metninde, “Hedef” satırında ve ölçek işaretinde olmak üzere üç yerde söyleniyor - üstelik ekranda musluk değil bir kronometre duruyor. h37-h72 arasındaki 36 oyunun tamamı yüklendi; motorlarda çökme veya konsol hatası oluşmadı."],
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

story += [P("Son kabul kontrolü", h1), P("3. sınıf hayat bilgisi bölümü tamamlanmadan önce", h2)]
story += bullets([
    "h37-h72 arasındaki 36 oyun üç kademeli turla baştan sona test edilir; görünen başlık, sahne, kontrol, ses ve ölçülen kazanım kayıt altına alınır.",
    "Hak-Sorumluluk Terazisi'ndeki bire bir sayısal denklik modeli kaldırılır; hakkın koşulsuz olduğu korunur ve blok sayısı ekranda yazılı olmaz.",
    "Kroki Rehberi gerçek bir krokiye dönüşür: sokaklar, yön oku, ölçek ve işaret noktaları bulunur; rota konum ifadeleriyle tarif edilir.",
    "Altı köprü oyununda parça-hedef emoji eşleşmesi kaldırılır; karar bilgiye dayanır ve uzun yazılar çipe sığar.",
    "Afet Zaman Bandı'nda kart hiçbir kenarda kırpılmaz; kutu etiketleri kutu içinde kalır ve Deprem Anı Adımları roket sahnesinden çıkarılır.",
    "Geri Dönüşüm Grafiği'nde veriler hazır sayı olarak verilmez; öğrenci nesneleri sayarak veriyi kendisi çıkarır ve grafiğe ölçek eklenir.",
    "Sürdürülebilirlik Musluğu'nda gereken miktar söylenmez; kronometre yerine gerçek musluk, kap ve akan su bulunur.",
    "Her oyunda en az üç farklı içerik turu, açıklayıcı yanlış geri bildirimi ve öğrencinin kendi örneğini/uygulamasını içeren bir kapanış bulunur.",
])
story += [Spacer(1, 4 * mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 2. sınıf hayat bilgisi listesindeki h01-h36 oyunlarını kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, görsel kanıt, mekanik, üç tur, geri bildirim, öğrenci kanıtı ve test gereksinimlerini ayrıntılı biçimde tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)

reader = PdfReader(str(OUT))
print({"pages": len(reader.pages), "games": len(games), "genericPrompt": len(generic_prompt),
       "beltGames": belt_n, "bytes": OUT.stat().st_size, "output": str(OUT)})
