from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle
import os


ROOT = "/Users/ceyda/Documents/New project"
OUT = os.path.join(ROOT, "output/pdf/1_sinif_matematik_kullanici_duzeltmeleri_duzenlenmis.pdf")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

PAGE_W, PAGE_H = A4
MX, TOP, BOTTOM = 18 * mm, 20 * mm, 17 * mm
INK = colors.HexColor("#25213B")
PURPLE = colors.HexColor("#473A70")
TEAL = colors.HexColor("#178B8B")
CORAL = colors.HexColor("#E7635B")
GOLD = colors.HexColor("#E3A72F")
PALE_PURPLE = colors.HexColor("#F1EDF9")
PALE_TEAL = colors.HexColor("#E9F6F4")
PALE_CORAL = colors.HexColor("#FFF0ED")
PALE_GOLD = colors.HexColor("#FFF7E3")
MID = colors.HexColor("#7A7687")

base = getSampleStyleSheet()["BodyText"]
body = ParagraphStyle("body", parent=base, fontName="Arial", fontSize=9.0, leading=12.2, textColor=INK, spaceAfter=1.7 * mm)
small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, spaceAfter=1 * mm)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=5 * mm, firstLineIndent=-3.2 * mm, bulletIndent=0, spaceAfter=1.25 * mm)
h1 = ParagraphStyle("h1", parent=body, fontName="Arial-Bold", fontSize=20, leading=24, textColor=PURPLE, spaceAfter=5 * mm)
h2 = ParagraphStyle("h2", parent=body, fontName="Arial-Bold", fontSize=10.8, leading=13.5, textColor=TEAL, spaceBefore=2 * mm, spaceAfter=1.2 * mm)
cover_kicker = ParagraphStyle("cover_kicker", parent=body, fontName="Arial-Bold", fontSize=10, textColor=TEAL, alignment=TA_CENTER, spaceAfter=6 * mm)
cover_title = ParagraphStyle("cover_title", parent=body, fontName="Arial-Bold", fontSize=26, leading=30, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=5 * mm)
cover_sub = ParagraphStyle("cover_sub", parent=body, fontSize=12, leading=17, alignment=TA_CENTER, spaceAfter=10 * mm)
game_title = ParagraphStyle("game_title", parent=body, fontName="Arial", fontSize=14.2, leading=17, textColor=colors.white, spaceAfter=0)
badge = ParagraphStyle("badge", parent=body, fontName="Arial-Bold", fontSize=17, leading=17, textColor=colors.white, alignment=TA_CENTER, spaceAfter=0)
box_title = ParagraphStyle("box_title", parent=body, fontName="Arial-Bold", fontSize=9.8, leading=12, textColor=CORAL, spaceAfter=1.2 * mm)
round_head = ParagraphStyle("round_head", parent=small, fontName="Arial-Bold", fontSize=8.4, leading=10, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=0)
round_text = ParagraphStyle("round_text", parent=small, fontSize=7.8, leading=10.0, spaceAfter=0)


def P(text, style=body):
    return Paragraph(text, style)


def bullets(items):
    return [Paragraph(x, bullet, bulletText="•") for x in items]


def header(number, title, group, accent):
    t = Table([[P(str(number), badge), P(f"<b>{title}</b><br/><font size='8' color='#F0EDF8'>{group}</font>", game_title)]], colWidths=[16 * mm, 155 * mm], rowHeights=[20 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("RIGHTPADDING", (1, 0), (1, 0), 10),
        ("ROUNDEDCORNERS", [8]),
    ]))
    return t


def box(title, items, bg, title_color):
    title_style = ParagraphStyle("dynamic_box_title", parent=box_title, textColor=title_color)
    content = [P(title, title_style)] + bullets(items)
    t = Table([[content]], colWidths=[171 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.55, colors.HexColor("#D7D3DF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROUNDEDCORNERS", [7]),
    ]))
    return t


def rounds_table(items):
    t = Table([
        [P("1. TUR", round_head), P("2. TUR", round_head), P("3. TUR", round_head)],
        [P(items[0], round_text), P(items[1], round_text), P(items[2], round_text)],
    ], colWidths=[57 * mm, 57 * mm, 57 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALE_GOLD),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFCF5")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDCFAB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def footer(canv, doc):
    if canv.getPageNumber() == 1:
        return
    canv.saveState()
    canv.setStrokeColor(colors.HexColor("#D9D5E5"))
    canv.setLineWidth(0.6)
    canv.line(MX, PAGE_H - 13 * mm, PAGE_W - MX, PAGE_H - 13 * mm)
    canv.setFont("Arial", 7.6)
    canv.setFillColor(MID)
    canv.drawString(MX, 9 * mm, "1. Sınıf Matematik - Düzenlenmiş Kullanıcı Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 9 * mm, str(canv.getPageNumber()))
    canv.restoreState()


games = [
    dict(n=1,t="Trafik Polisi",g="Uzamsal İlişkiler / Kavşak Yönetimi",a=CORAL,
         o=["Mevcut oynanış sabit araç kartlarını sağ/sol kutularına taşımaya dayanıyor; gerçek yol ve akan trafik hissi zayıf.","Yüklenen notta oyun Kavşak Polisi diye anılmış; uygulamadaki gerçek ad Trafik Polisi olduğu için başlık bu şekilde düzeltilmiştir."],
         p=["Üst bölümde yavaş hareket eden arabaların bulunduğu gerçek bir yol ve kavşak çizilsin.","Alt bölümde sağ ve sol yönü gösteren büyük garaj/çıkış alanları bulunsun. Çocuk hareket eden aracı tutup doğru alana sürüklesin.","Trafik polisi düdük ve el hareketiyle yönlendirsin; renkler Android sürümünde de aynı görünmelidir."],
         r=["2 kırmızı araba sağa, 2 mavi araba sola gönderilir.","3 sarı araba sola, 3 yeşil araba sağa gönderilir; araç sırası değişir.","Karışık altı araç sesli komuta göre sağ/sol şeride ayrılır."],
         f=["Yanlış alanda araç güvenli biçimde yola döner ve Tekrar dene denir.","Doğru araçlar kavşaktan geçer; üç tur bitince trafik akışı açılır."],
         c="Arabalar gerçekten hareket edecek; oyun sabit emoji kartlarını kutuya bırakmaya indirgenmeyecek."),
    dict(n=2,t="Pusula Korsanı",g="Uzamsal İlişkiler / Sesli Yönergeler",a=TEAL,
         o=["Yönergenin Papağan: diye düz okunması anlaşılmayı zorlaştırıyor; konuşan karakter hissi oluşmuyor.","Adımlar yalnız metinden takip edilirse 1. sınıf öğrencisi için gereksiz okuma yükü oluşuyor."],
         p=["Papağan kanat ve ağız animasyonuyla konuşsun; karakter adı metnin bir parçası gibi okunmasın.","Ortada kareli büyük bir hazine haritası, başlangıç noktası ve yön oku bulunsun.","Yönerge örneği: Hazine tam 2 adım sağda ve 1 adım yukarıda. Adımları say ve doğru kareye dokun."],
         r=["Başlangıçtan 2 sağ, 1 yukarı gidilen kare bulunur.","1 sol, 2 aşağı gidilen kare bulunur.","2 yukarı, 2 sağ gidilen kare bulunur; başlangıç yeri değişir."],
         f=["Yanlış karede papağan ipucu yönünü yeniden söyler; bir can eksilir.","Doğru karede kum açılır, sandık çıkar ve papağan sevinir."],
         c="Sesli yön ile haritadaki gerçek konum birebir uyuşacak; doğru kare metinle işaretlenmeyecek."),
    dict(n=3,t="Dağcı Keçi",g="Uzamsal İlişkiler / Yukarı-Aşağı ve Yükseklik",a=GOLD,
         o=["Oyunun temel fikri uygun; ancak dağ, patika ve keçi telefon ekranında çok küçük kaldığı için hareket yönü zor seçiliyor."],
         p=["Dağ ve keçi oyun alanının büyük bölümünü kaplayacak şekilde büyütülsün.","Patikadaki ileri ve yukarı adımlar kalın, yüksek kontrastlı taşlarla gösterilsin.","Her doğru komutta keçi bir taş ilerleyip zıplasın; zirve ve bayrak başlangıçtan itibaren görünür olsun."],
         r=["İleri, yukarı, ileri dizisiyle kısa patika tamamlanır.","Yukarı, ileri, yukarı, ileri dizisiyle orta rota tamamlanır.","Beş adımlı karışık rota ile zirveye ulaşılır."],
         f=["Yanlış komutta keçi hareket etmez, doğru yön kısa süre parlar.","Doğru dizide keçi zirveye çıkar ve bayrağı diker."],
         c="Keçinin ayağı, bulunduğu taş ve bir sonraki adım küçük telefon ekranında yakınlaştırma gerektirmeden görülecek."),
    dict(n=4,t="Çorap Eşleştirmece",g="Uzamsal İlişkiler / Desen ve Boyut Eşliği",a=PURPLE,
         o=["Sepet yalnız yazı/etiket gibi algılanıyor; örnek çorap ile ipteki seçenekler gerçek ve büyük bir sahne oluşturmuyor.","Yönerge, hangi çorabın nereye taşınacağını yeterince açık söylemiyor."],
         p=["Gerçek, büyük bir sepetin içinde tek örnek çorap bulunsun; ipte desen ve boyutu farklı büyük çoraplar asılı dursun.","Yönerge: Sepetteki çorabın tam eşini ipte bul ve sepetin yanındaki mandala sürükle.","Eşleşme renk, desen ve uzunluk ölçütlerinin tamamıyla yapılmalıdır."],
         r=["Kısa kırmızı çizgili çorabın eşi bulunur.","Uzun mavi benekli çorabın eşi bulunur.","Orta boy sarı yıldızlı çorabın eşi bulunur; seçenek sırası değişir."],
         f=["Yanlış çorap sepete geri döner ve Desenine ve boyuna tekrar bak denir.","Doğru çift mandalla ipe asılır ve birlikte sallanır."],
         c="Sepet ve çoraplar gerçek görsel nesne olacak; yalnız renk-boy adlarıyla cevap verilemeyecek."),
    dict(n=5,t="Çarkıfelek Dişlileri",g="Nesnelerin Geometrisi / Geometrik Eşlik",a=TEAL,
         o=["Dişli sayısı kartların ve yuvaların üzerinde doğrudan yazdığı için çocuk dişleri/çukurları saymadan eşleştirebiliyor."],
         p=["Makine üzerinde farklı sayıda çukuru bulunan gerçek dişli yuvaları çizilsin; sayı etiketleri kaldırılmış olsun.","Çocuk gevşek dişlilerin çıkıntılarını sayıp uygun yuvaya sürüklesin.","Doğru takılan iki dişli birbirine temas edip gerçekten dönmeye başlasın."],
         r=["4 ve 6 dişli iki çark doğru yuvalara takılır.","6 ve 8 dişli çarklar, 7 dişli dikkat dağıtıcıyla eşleştirilir.","5 ve 7 dişli çarklar farklı konumdaki yuvalara yerleştirilir."],
         f=["Uymayan dişli yuvaya girmez ve geri döner.","Tüm çarklar doğruysa makine çalışır, ışıklar yanar."],
         c="Hiçbir dişli veya yuva üzerinde cevap sayısı yazmayacak; diş ve çukur sayıları çizimle birebir doğru olacak."),
    dict(n=6,t="Parmak Canavarları",g="Sayılar ve Nicelikler / El-Parmak Temsilleri",a=CORAL,
         o=["Parmak sayısı metin ve küçük el simgeleriyle tarif ediliyor; canavarın gerçek elleri ve tek tek sayılabilen parmakları yeterince görünür değil."],
         p=["Büyük bir canavar ve iki büyük el çizilsin; açık/kapalı parmaklar ayrı ayrı hareket etsin.","Çocuk ekrandaki parmakları sayıp alttaki büyük sayı kartlarından birine dokunsun.","Soru cümlesi açık parmak sayısını söylemeyecek; yalnız Say ve doğru sayıya dokun denecektir."],
         r=["Bir elde 5, diğer elde 2 açık parmak: cevap 7.","İki el tamamen açık: cevap 10.","Bir elde 1, diğer elde 5 açık parmak: cevap 6."],
         f=["Yanlış sayıda canavar parmaklarını yeniden yavaşça açar ve Tekrar say der.","Doğru sayıda canavar alkışlar; parmakların üstünde sayma noktaları kısa süre görünür."],
         c="Çocuk doğru cevabı metinden değil, canavarın ekrandaki gerçek açık parmaklarını sayarak bulacak."),
    dict(n=7,t="Uzaylı Asansörü",g="Sayılar ve Nicelikler / Onluk Çerçeve",a=GOLD,
         o=["Oyun asansör adını taşısa da gerçek bir kabin ve aşağıda bekleyen uzaylılar yeterince görünmüyor; sayaç mekanik kalıyor."],
         p=["Büyük, kapıları açılan bir uzay asansörü ve aşağıda sıraya girmiş uzaylılar çizilsin.","Çocuk uzaylıları tek tek sürükleyerek kabine alsın; içeride 10'luk çerçeve ve birlik alanı görünsün.","Kabin doldukça sayaç ve uzaylı sayısı birlikte artsın."],
         r=["8 uzaylı kabine taşınır.","12 uzaylı 10 + 2 düzeninde yerleştirilir.","16 uzaylı 10 + 6 düzeninde tamamlanır."],
         f=["Fazla uzaylı kabine kabul edilmez ve sıraya döner.","Hedef sayı tamamlanınca kapılar kapanır, asansör ışınlanarak yükselir."],
         c="Asansörde görünen uzaylı adedi sayaçla aynı olacak; sürükleme alanları büyük ve toleranslı çalışacak."),
    dict(n=8,t="Pazar Kasası",g="Sayılar ve Nicelikler / Okuma-Dinleme ve Miktar",a=PURPLE,
         o=["Pazar ortamı, tezgah ve gerçek sepet yerine soyut sayma alanı kullanılıyor; portakallar alışveriş eylemi içinde görülmüyor."],
         p=["Canlı bir pazar yeri, portakal tezgahı, satıcı ve büyük bir alışveriş sepeti bulunsun.","Satıcı hedef sayıyı sesli söylesin. Çocuk portakalları tezgahtan tek tek sürükleyerek sepete atsın.","Sepetteki portakallar iki düzenli sıraya yerleşsin; çocuk son sayıyı görsel olarak kontrol edebilsin."],
         r=["ON portakal sepete taşınır.","ON BEŞ portakal taşınır; yazı ve ses birlikte verilir.","YİRMİ portakal iki onluk grup halinde tamamlanır."],
         f=["Hedeften fazla portakal sepete girmez ve satıcı Sayıyı tekrar kontrol et der.","Doğru sayıda sepet kasaya gider ve satıcı teşekkür eder."],
         c="Portakallar gerçek pazar tezgahından gerçek sepete sürüklenecek; yalnız sayaç düğmesine basılmayacak."),
    dict(n=9,t="Sihirli Olta",g="Sayılar ve Nicelikler / Gizli Alt Gruplar",a=TEAL,
         o=["Mevcut Sihirli Büyüteç adı oynanışla uyuşmuyor. Oltayla yakalama yerine genel seçim şablonu kullanılıyor.","Web'de görülen kırmızı/mavi balıkların renkleri APK'da farklı veya belirsiz görünebiliyor."],
         p=["Oyunun adı Sihirli Olta olarak değiştirilsin.","Altta gerçek bir olta, misina ve kanca olsun; çocuk oltayı sürükleyip istenen renkteki balıklara götürsün.","Kırmızı, mavi, sarı ve yeşil balık renkleri yüksek kontrastlı tanımlansın; web ve APK aynı renk değerlerini kullansın."],
         r=["3 kırmızı ve 2 mavi balık yakalanır.","4 sarı ve 1 yeşil balık yakalanır.","2 kırmızı ve 3 mavi balık, farklı yüzme düzeninde yakalanır."],
         f=["Yanlış renk balık kancadan kaçar ve istenen renk yeniden seslendirilir.","Doğru sayılar tamamlanınca balıklar sayılarak denize geri bırakılır."],
         c="Balık rengi isim etiketi olmadan seçilebilecek; aynı renkler web ve Android ekranında gözle ayırt edilecek."),
    dict(n=10,t="Şipşak Hafıza",g="Sayılar ve Nicelikler / Hızlı Görsel Hafıza",a=CORAL,
         o=["İlk önizleme APK'da görünmüyor; web'de ise yaklaşık 1,6 saniye gösterildiği için çocuk nesneleri inceleyemeden ekran kapanıyor."],
         p=["Önizleme her platformda eksiksiz görünsün ve 10 saniye açık kalsın; üstte görünür geri sayım çubuğu bulunsun.","Meyve grupları büyük, aralıklı ve net çizilsin. Süre bitince perde kapanıp soru gelsin.","Önizleme sırasında cevap sayısı yazılmasın; yalnız nesne grupları gösterilsin."],
         r=["3 elma ve 2 armut gösterilir; toplam 5 sorulur.","4 yıldız ve 3 ay gösterilir; toplam 7 sorulur.","2 top, 2 araba ve 1 ayı gösterilir; grup yapısı ve toplam sorulur."],
         f=["Yanlış cevapta görüntü kısa bir kez yeniden gösterilir; bir can eksilir.","Doğru cevapta perde açılır ve gruplar sayma vurgusuyla yeniden görünür."],
         c="Önizleme web ve APK'da 10 saniye boyunca görünür olacak; boş veya siyah ekran oluşmayacak."),
    dict(n=11,t="Uzaylı Apartmanı",g="Sıra Sayısı / Dikey Sıralama",a=GOLD,
         o=["Web sürümündeki apartman sahnesi uygun; ancak APK'da aynı görsel düzen ve hedef kat görünümü korunmuyor."],
         p=["Web'deki beş katlı uzaylı apartmanı, pencereler, uzaylılar ve paket APK'ya birebir aktarılmalı.","Katlar aşağıdan yukarı doğru açıkça sıralansın; hedef uzaylı pencereden el sallayarak ipucu versin.","Paket sürüklenince bina içinde küçük asansör animasyonu çalışsın."],
         r=["Paket 2. kattaki uzaylıya teslim edilir.","Paket 4. kata teslim edilir.","Paket 5. kata teslim edilir; katların renkleri değişir."],
         f=["Yanlış katta pencere kapanır ve Aşağıdan saymayı tekrar dene denir.","Doğru katta pencere açılır, uzaylı paketi alır."],
         c="Web ve APK ekran görüntüleri yan yana konduğunda bina, katlar, renkler ve paket konumu aynı olacak."),
    dict(n=12,t="Dondurma Kulesi",g="Sıra Sayısı / Yönergeyle Sıra Oluşturma",a=PURPLE,
         o=["Web oynanışı uygun; APK'da külah, top sırası veya sürükleme yerleşimi aynı görünmüyor."],
         p=["Büyük bir külah ve aşağıdan yukarı doğru üç belirgin yerleştirme yuvası bulunsun.","Dondurma topları gerçek renk/doku farkıyla çizilsin ve sürüklenerek doğru sıraya otursun.","Sesli yönerge her topun sırasını alttan başlayarak açıklasın; web tasarımı APK'da aynen korunmalıdır."],
         r=["1 çilek, 2 vanilya, 3 çikolata sırası kurulur.","1 çikolata, 2 limon, 3 çilek sırası kurulur.","Dört toplu farklı bir sıra kurulur; seçenekler karıştırılır."],
         f=["Yanlış sıradaki top külaha yapışmaz ve tabağa döner.","Doğru kule tamamlanınca dondurma parlayıp müşteriye verilir."],
         c="Toplar alttan yukarı gerçek fiziksel sırada görünecek; web ve APK aynı yuva toleransını kullanacak."),
    dict(n=13,t="Şampiyonlar Kürsüsü",g="Sıra Sayısı / Yarış ve Sıralama",a=TEAL,
         o=["Doğru hayvan doğrudan 1., 2. veya 3. kürsü bloğuna bırakıldığında her zaman kabul edilmiyor; çok dar bir üst bölgeyi hedeflemek gerekiyor."],
         p=["Her kürsü bloğunun tamamı geniş bırakma alanı olsun; üst yüzey, gövde ve numara bölgesi aynı hedefe bağlansın.","Sürüklenen hayvan doğru kürsüye yaklaşınca blok renkli çerçeveyle parlasın.","Hayvan bırakıldığında bloğun üstüne otomatik hizalansın."],
         r=["Çita 1., tavşan 2., kaplumbağa 3. yerleştirilir.","Tavşan 1., çita 2., kaplumbağa 3. yerleştirilir.","Üç yeni hayvan farklı yarış sonucuna göre yerleştirilir."],
         f=["Yanlış kürsüde hayvan başlangıç çizgisine döner.","Doğru sıralamada madalya töreni ve konfeti animasyonu oynar."],
         c="Hayvan doğru kürsü bloğunun herhangi bir belirgin yerine bırakıldığında kabul edilecek; piksel hassasiyetinde hedef gerekmeyecek."),
    dict(n=14,t="Gökyüzü Asansörü",g="Sıra Sayısı / Dikey Düzlem",a=CORAL,
         o=["Oyun işlevsel olsa da yapı gerçek bir asansörden çok kule/sayaç görünümünde kalıyor."],
         p=["Kabloları, kapıları, kat göstergesi ve büyük yukarı-aşağı düğmeleri olan gerçek bir cam asansör çizilsin.","Paket kabinin içinde görünür olsun; her dokunuşta kabin bir kat hareket etsin ve sayaç değişsin.","Hedef kat bulutlu bina cephesinde bayrakla işaretlensin."],
         r=["Paket 2. kata çıkarılır.","Paket 4. kata çıkarılır.","6. kata çıkılır; bir yanlış aşağı hareketi düzeltme imkanı bulunur."],
         f=["Hedef aşılırsa asansör durur ve kat göstergesi kırmızı yanar.","Doğru katta kapılar açılır ve paket teslim edilir."],
         c="Düğme sayısı, kabin hareketi ve kat göstergesi her dokunuşta aynı değeri gösterecek."),
    dict(n=15,t="Obur Canavarın Tabakları",g="Karşılaştırma / Daha Çok-Daha Az",a=GOLD,
         o=["Canavarın isteği Canavar: biçiminde düz okunuyor; karakter konuşma ve ağız animasyonuyla soruyu yöneltmiyor."],
         p=["Büyük canavar konuşurken ağzı ve gözleri hareket etsin; isteği karakterin kendi sesiyle söylensin.","Önünde sayıları yazmayan, çilekleri tek tek görülen üç tabak bulunsun.","Çocuk Daha çok, Daha az veya Eşit isteğine uygun tabağa dokunsun."],
         r=["3, 5 ve 7 çilekli tabaklardan Daha çok olan seçilir.","2, 4 ve 6 çilekli tabaklardan Daha az olan seçilir.","İki tabakta 5'er çilek bulunur; eşit olan çift seçilir."],
         f=["Yanlış tabakta canavar isteğini tekrar söyler ve çilekler kısa süre sayılır.","Doğru tabakta canavar çilekleri sevinçle yer."],
         c="Tabakların üzerinde cevap sayısı yazmayacak; karşılaştırma gerçek çilek adetleriyle yapılacak."),
    dict(n=16,t="Adalet Terazisi",g="Karşılaştırma / Eşitlik ve Denge",a=PURPLE,
         o=["Mevcut düzen eşitlik fikrini yeterince oyunlaştırmıyor; çocuk elmaları gerçek kefelere taşıyarak dengeyi kuramıyor."],
         p=["Ortada hareket eden gerçek bir terazi, iki geniş kefe ve altta elma sepeti bulunsun.","Başlangıçta kefelerde farklı miktarda elma açıkça görülsün. Çocuk sepetten eksik kefeye elmaları tek tek sürüklesin.","Her elma eklendiğinde terazi fiziksel olarak hareket etsin; eşitlendiğinde ortada dursun."],
         r=["Sol 5, sağ 3 elma: sağ kefeye 2 elma eklenir.","Sol 4, sağ 6 elma: sol kefeye 2 elma eklenir.","İki kefede 7'şer elma vardır; çocuk Eşit düğmesini seçer."],
         f=["Yanlış kefede terazi daha çok eğilir ve Elmaların sayısına tekrar bak denir.","Denge kurulunca kefeler parlar ve EŞİT sözcüğü sesli okunur."],
         c="Kefedeki elma sayıları ile terazinin eğimi fiziksel olarak tutarlı olacak; denge sürükleme ile kurulacak."),
    dict(n=17,t="İkiz Kardeşlerin Sepetleri",g="Karşılaştırma / Görsel Benzerlik ve Farklılık",a=TEAL,
         o=["Mevcut oyun Meyveler aynı, Renkler aynı gibi yazılı etiketlere dayanıyor; 1. sınıf öğrencisi için gereğinden fazla okuma istiyor."],
         p=["Oyun iki büyük sepet arasındaki görsel farkları bulma oyununa dönüştürülsün.","Sepetlerde meyve türü, renk, yön, yaprak, kurdele ve sayı farkları büyük ve net çizilsin.","Çocuk fark gördüğü nesneye dokunsun; doğru fark iki sepette aynı anda çerçevelensin."],
         r=["İki meyve sepetinde 7 görsel fark bulunur.","İki piknik sepetinde 7 farklı nesne/renk farkı bulunur.","İki oyuncak sepetinde 7 yön, desen ve sayı farkı bulunur."],
         f=["Aynı olan bir yere dokunulursa işaret oluşmaz ve Tekrar incele denir.","Yedi fark tamamlanınca ikiz kardeşler sepetleri değiş tokuş eder."],
         c="Cevap için cümle okumak gerekmeyecek; her turdaki yedi fark gerçek görsel ayrıntı olarak bulunacak."),
    dict(n=18,t="Uzay Üssü Geri Sayımı",g="Ritmik Sayma / Geriye Sayma",a=CORAL,
         o=["Geri sayım tamamlandığında yalnız başarı mesajı geliyor; roketin gerçekten fırladığı bir sonuç animasyonu yok."],
         p=["Gerçek fırlatma rampası, büyük roket, geri sayım ekranı ve egzoz ışıkları çizilsin.","Çocuk her doğru sayıda büyük geri say düğmesine bassın; sayı hem değişsin hem sesli okunsun.","1'e gelindiğinde ateşleme, duman, sarsıntı ve gökyüzüne yükselme animasyonu oynasın."],
         r=["10'dan 1'e geriye sayılır ve küçük roket fırlatılır.","15'ten 1'e geriye sayılır; sayılar farklı düzende görünür.","20'den 1'e eksiksiz geri sayılır ve ana roket fırlatılır."],
         f=["Yanlış sırada ateşleme durur ve Son sayıyı tekrar düşün denir.","Doğru geri sayımda roket ekrandan çıkar, yıldız izi bırakır."],
         c="Geri sayımın sonunda her platformda kesintisiz roket fırlatma animasyonu oynayacak."),
    dict(n=19,t="Yeraltı Madencisi",g="Ritmik Sayma / Derinlere İniş",a=GOLD,
         o=["Mevcut kule/sayaç görünümü gerçek maden asansörü ve asansör düğmeleri hissini vermiyor."],
         p=["Tahta-metal kabinli gerçek maden asansörü, halat, ray ve numaralı katlar çizilsin.","Kabinde büyük bir aşağı ok düğmesi bulunsun. Her dokunuşta gösterge 20, 19, 18, 17 diye değişsin ve kabin bir kat insin.","Madenci karakteri kabinde görünsün; hedef katta mücevher ışığı parlasın."],
         r=["10. kattan 1. kata inilir.","15. kattan 5. kata geriye sayılır.","20. kattan 1. kata eksiksiz inilerek maden bulunur."],
         f=["Yanlış yönde kabin hareket etmez ve Sonraki sayı hangisi? denir.","Hedef katta kapı açılır, madenci mücevherleri toplar."],
         c="Her düğme basışında kat etiketi bir azalacak ve kabinin gerçek konumu aynı katla hizalanacak."),
    dict(n=20,t="Eriyen Kardan Adam",g="Örüntüler / Azalan Sayı Örüntüsü",a=PURPLE,
         o=["Sayı kartları var ancak kardan adamın kartların üzerinde yavaş yavaş eridiği görsel zaman baskısı oluşmuyor."],
         p=["Her sayı kartında giderek küçülen kardan adam aşaması çizilsin; canlı kardan adam da süre boyunca yavaşça erisin.","Çocuk örüntünün eksik sayısını kardan adam tamamen erimeden seçsin.","Süre çubuğu kar tanesi biçiminde ve çocuk için sakin, anlaşılır hızda ilerlesin."],
         r=["15, 12, 9, ? örüntüsünde 6 seçilir.","12, 10, 8, ? örüntüsünde 6 seçilir.","20, 15, 10, ? örüntüsünde 5 seçilir."],
         f=["Yanlış seçimde erime bir aşama ilerler ve örüntü farkı görsel olarak gösterilir.","Doğru cevapta kar yağar, kardan adam yeniden tamamlanır."],
         c="Kardan adamın erime aşaması sayı örüntüsüyle uyumlu olacak; çocuk tamamlanmadan önce seçim yapabilecek."),
    dict(n=21,t="Kavanozdaki Şekerler",g="Tahmin / Tahmin ve Gerçek Sonuç",a=TEAL,
         o=["Kavanozun içindeki şekerler görünmüyor; yalnız soru işareti bulunduğu için çocuk gözleme dayalı tahmin yapamıyor."],
         p=["Şeffaf cam kavanoz içinde gerçek, renkli şekerler dağınık biçimde görünsün.","Çocuk yaklaşık sayıyı seçsin; ardından Kontrol et düğmesiyle şekerler kavanozdan çıkıp sıraya dizilsin.","Gerçek sonuç tek tek sesli sayılarak tahminle karşılaştırılsın."],
         r=["8 şekerli küçük kavanoz tahmin edilir.","14 şekerli orta kavanoz tahmin edilir.","20 şekerli büyük kavanoz tahmin edilir; şekerler kısmen üst üste görünür."],
         f=["Tahmin farklıysa ceza yerine Yaklaştın veya Biraz daha fazlaydı geri bildirimi verilir.","Sayım bitince tahmin ve gerçek sonuç yan yana gösterilir."],
         c="Kavanoz hiçbir turda soru işaretiyle kapatılmayacak; tahmin edilecek gerçek şeker grubu görünür olacak."),
    dict(n=22,t="Örüntü Treni ve Eksik Vagon",g="Örüntüler / Eksik Vagon",a=CORAL,
         o=["Mevcut örüntü küçük daire/kare simgeleriyle veriliyor; gerçek tren, lokomotif ve şekilli vagon sürükleme mekaniği yok."],
         p=["Ray üzerinde gerçek bir lokomotif ve gövdesi üçgen, daire veya kare biçiminde vagonlar bulunsun.","Örüntüdeki boş yere uygun vagon aşağıdaki seçeneklerden sürüklenerek takılsın.","Bağlantı kancaları birleşsin; doğru vagon sonrası tren hareket etsin."],
         r=["Daire, kare, daire, kare, ? örüntüsü tamamlanır.","Üçgen, üçgen, daire, üçgen, üçgen, ? tamamlanır.","Kare, daire, üçgen sırası iki kez tekrar edilerek eksik vagon bulunur."],
         f=["Yanlış vagon kancaya bağlanmaz ve seçeneklere döner.","Doğru örüntüde düdük çalar, tren istasyondan çıkar."],
         c="Vagon şekli yalnız üstündeki sembolde değil, vagonun gerçek dış sınırında görülecek."),
    dict(n=23,t="Hızlı Tahminci Karınca",g="Tahmin / 5'ten Az mı Çok mu",a=GOLD,
         o=["Karınca ve yaprak grubu görünür değil; soru işareti nedeniyle çocuk 5 ile görsel karşılaştırma yapamıyor."],
         p=["Animasyonlu karınca ve önünde dağınık gerçek yaprak yığını çizilsin.","Çocuk önce 5'ten az, tam 5 veya 5'ten çok seçeneğine dokunsun.","Tahminden sonra yapraklar tek sıra olur ve karınca her yaprağı taşıyarak sayar."],
         r=["3 yaprak: 5'ten az.","5 yaprak: tam 5.","7 yaprak: 5'ten çok; yaprak dizilimi daha dağınık olur."],
         f=["Tahmin farklıysa yapraklar sayılarak neden gösterilir; doğrudan ağır ceza verilmez.","Doğru tahminde karınca yaprakları yuvasına taşır."],
         c="Yapraklar tahminden önce görülecek; gerçek sayım tahminden sonra animasyonla doğrulanacak."),
    dict(n=24,t="Cüce Adımı",g="Ölçme / Uzunluk Tahmini",a=PURPLE,
         o=["Dev ve Cüce Ayakları adı iki ölçme aracını aynı anda çağrıştırıyor; oda, cüce ve ayak uzunluğu yeterince somut görünmüyor."],
         p=["Oyunun adı Cüce Adımı olarak değiştirilsin.","Gerçek bir oda, odanın bir ucunda cüce ve ayak/adım uzunluğunu gösteren belirgin ölçü işareti bulunsun.","Çocuk adım sayısını tahmin ettikten sonra cüce odayı yürüsün ve ayak izleri tek tek sayılsın."],
         r=["Kısa oda 6 cüce adımı olarak ölçülür.","Orta oda 9 cüce adımı olarak ölçülür.","Uzun oda 12 cüce adımı olarak ölçülür; tahmin seçenekleri değişir."],
         f=["Tahmin sonrası gerçek yürüyüş gösterilir; Yaklaştın mesajı kullanılabilir.","Doğru tahminde ayak izleri parlayıp ölçü sonucu sesli okunur."],
         c="Cücenin ayak uzunluğu ve odanın başlangıç-bitiş sınırları ekranda açıkça görülecek."),
    dict(n=25,t="Kırtasiye Düzenleyici",g="Ölçme / Ataş ile Uzunluk",a=TEAL,
         o=["Kalem ve ataşlar yalnız sembol/sayı biçiminde kalıyor; gerçek ölçme süreci ekranda oluşmuyor."],
         p=["Masa üzerinde büyük bir kalem ve yanında aynı boyda gerçek ataşlar bulunsun.","Çocuk önce tahmin etsin; sonra ataşları kalemin başlangıcından sonuna boşluksuz ve üst üste gelmeden sürükleyerek dizsin.","Her ataş yerleştiğinde sıra numarası sesli okunsun."],
         r=["Kalem 8 ataşla ölçülür.","Silgi 3 ataşla ölçülür.","Defter kenarı 6 büyük ataşla ölçülür."],
         f=["Boşluk veya üst üste binme varsa ataş hizaya dönüp Ölçerken aralık bırakma denir.","Doğru ölçümde nesne ve ataş sırası birlikte çerçevelenir."],
         c="Ataşlar nesnenin başından sonuna gerçek uç uca ölçüm oluşturacak; sonuç yalnız x 8 yazısıyla verilmemeli."),
    dict(n=26,t="Küçük İcatlar Pazarı",g="Ölçme / Kütle Tahmini",a=CORAL,
         o=["Elma ve bilye sayısı soyut sonuç kartıyla veriliyor; gerçek terazi, kefeler ve bilyelerin eklenme süreci görünmüyor."],
         p=["Pazar tezgahında gerçek bir eşit kollu terazi olsun; bir kefede nesne, yerde çok sayıda bilye bulunsun.","Çocuk kaç bilye gerektiğini tahmin etsin. Sonra bilyeleri diğer kefeye tek tek sürüklesin.","Her bilyede kefe hareket etsin; denge noktasında bilyeler birlikte sayılsın."],
         r=["Elma 8 bilyeyle dengelenir.","Oyuncak araba 5 bilyeyle dengelenir.","Küçük kitap 10 bilyeyle dengelenir."],
         f=["Fazla bilyede terazi ters yöne eğilir ve bir bilye geri alınabilir.","Denge kurulunca tahmin ve gerçek sonuç karşılaştırılır."],
         c="Bilye adedi, kefe hareketi ve gerçek sonuç her turda birbiriyle tam uyumlu olacak."),
    dict(n=27,t="Market Arabası Dedektifi",g="Cebirsel Düşünme / Günlük Toplama-Çıkarma",a=GOLD,
         o=["Sepetteki değişim yeterince animasyonlu gösterilmiyor; işlem artı mı eksi mi sorusu olaydan kopuk kalıyor."],
         p=["Gerçek market arabası ve içinde sayılabilir elmalar bulunsun. Önce başlangıç miktarı gösterilsin, sonra elmalar tek tek eklensin veya çıkarılsın.","Anlatıcı Arttıysa artıya, azaldıysa eksiye bas desin. Altta büyük + ve - düğmeleri olsun.","Seçim sonrası olayın işlemi ekranda nesnelerle birlikte kurulsun."],
         r=["5 elmaya 3 elma eklenir; + seçilir ve 5 + 3 = 8 kurulur.","9 elmadan 2 elma alınır; - seçilir ve 9 - 2 = 7 kurulur.","4 elmaya 5 elma eklenir; çocuk hem işareti hem sonucu seçer."],
         f=["Yanlış işarette elma animasyonu yeniden oynatılır ve Değişimi tekrar izle denir.","Doğru işlemde araba kasaya ilerler."],
         c="Arttı/azaldı kararı ekrandaki gerçek elma hareketinden anlaşılacak; elma adetleri işlemle aynı olacak."),
    dict(n=28,t="Okul Servisi Yolcuları",g="Cebirsel Düşünme / Günlük Toplama-Çıkarma",a=PURPLE,
         o=["Binen ve inen öğrenciler gerçek servis/durak animasyonuyla gösterilmiyor; soru metne dayalı kalıyor."],
         p=["Bir okul servisi, durak ve sayılabilir öğrenci karakterleri çizilsin.","Öğrenciler kapıdan tek tek binip otursun veya inip durağa geçsin. Anlatıcı Binenler için hangi işareti seçmeliyiz? diye sorsun.","Altta büyük + ve - butonları bulunsun; semboller artı ve eksi diye seslendirilsin."],
         r=["Servise 3 öğrenci biner; + seçilir.","Servisten 2 öğrenci iner; - seçilir.","Aynı yolculukta önce 2 öğrenci biner, sonra 3 öğrenci iner; iki işlem sırayla seçilir."],
         f=["Yanlış işarette kapı tekrar açılır ve hareket yavaşça yeniden gösterilir.","Doğru seçimde servis bir sonraki durağa gider."],
         c="Binen/inen karakter sayısı görünür olacak ve seçilen işlem işaretiyle aynı olayı temsil edecek."),
    dict(n=29,t="Şimşek Tahmincisi",g="Tahmin ve Zihinden İşlem",a=TEAL,
         o=["12 + 6 sorusundan sonra büyüklük tahmini yeterince görselleştirilmiyor; Büyük/Küçük yazılı taşlar yerine gerçek boyut farkı kullanılmalı."],
         p=["Fırtınalı bir sahnede biri belirgin büyük, diğeri belirgin küçük iki taş bulunsun; taşların üstünde Büyük/Küçük yazmasın.","İşlem sesli okunduktan sonra Sonuç 10'dan büyükse büyük taşı, küçükse küçük taşı vur denilsin.","İlk tahminden sonra ikinci ekranda yalnız sayılardan oluşan sonuç seçenekleri gösterilsin."],
         r=["12 + 6: büyük taş, sonra 18.","8 + 1: küçük taş, sonra 9.","14 - 3: büyük taş, sonra 11."],
         f=["Yanlış taşta şimşek düşmez ve 10 ile karşılaştır denir.","Doğru taşta şimşek efekti oynar; ardından kesin sonuç sorulur."],
         c="Taşların boyutu yazısız ayırt edilecek; işlem sembolleri seslendirmede artı/eksi olarak okunacak."),
    dict(n=30,t="İksir Karıştırıcı",g="Tahmin / Tahmin ve Gerçek Sonuç",a=CORAL,
         o=["7 ve 5 damla yalnız cümleyle anlatılıyor; iki şişe ve gerçek damla miktarları görünmüyor. Seçeneklerde uzun 10'dan fazla gibi ifadeler gereksiz okuma yükü yaratıyor."],
         p=["İki şeffaf şişe ve içinde tek tek sayılabilen damlalar bulunsun.","Şişeler kazana dökülürken damlalar birleşsin; çocuk son miktarı yalnız sayı kartlarından seçsin.","Yönerge iki miktarı sesli okusun; cevap seçeneklerinde yalnız rakamlar yer alsın."],
         r=["7 ve 5 damla karışır; cevap 12.","6 ve 3 damla karışır; cevap 9.","8 ve 4 damla karışır; cevap 12; renkler farklı olur."],
         f=["Yanlış sayıda damlalar iki gruba ayrılıp yeniden sayılır.","Doğru cevapta iksir renk değiştirip baloncuk çıkarır."],
         c="Şişelerdeki görünür damla sayısı işlemdeki sayılarla birebir aynı olacak; seçenekler yalnız rakam olacak."),
    dict(n=31,t="Hedefe Vuran Roket",g="Zihinden İşlem / Hızlı Çıkarma",a=GOLD,
         o=["Yönerge ve işlem seslendirmesi yeterince açık değil; eksi işareti bazı seslendirmelerde tire diye okunabiliyor."],
         p=["Yönerge Hedefi cevabın bulunduğu gezegene yönlendir olsun.","İşlem hem ekranda büyük yazılsın hem Dokuz eksi iki gibi doğru matematik diliyle seslendirilsin.","Çocuk roketin nişan çizgisini sürükleyip üzerinde doğru sonuç bulunan gezegene bıraksın."],
         r=["15 - 4 işlemi için 11 gezegeni seçilir.","12 - 5 işlemi için 7 gezegeni seçilir.","20 - 6 işlemi için 14 gezegeni seçilir."],
         f=["Yanlış gezegende roket fırlamaz, nişan başlangıca döner.","Doğru hedefte roket gezegene uçar ve bayrak bırakır."],
         c="- işareti hiçbir platformda tire diye okunmayacak; bütün işlem ve sonuçlar birbiriyle uyumlu olacak."),
    dict(n=32,t="Sihirli Terazi",g="Eşit İşaretinin Anlamı / Denge",a=PURPLE,
         o=["Yönergede 3 + 2 elma denmesi 1. sınıf öğrencisini işlem metnine yöneltiyor; kefedeki gerçek elmalar yerine sayı/işlem vurgusu ağır basıyor."],
         p=["Yönerge doğrudan Sol kefede 5 elma var. Diğer kefeyi eşitle biçiminde düzenlensin.","Bir sepette çok sayıda elma bulunsun; çocuk elmaları tek tek sürükleyerek boş kefeye koysun.","Karşı kefede 5 yazısı değil gerçekten 5 elma görünsün. İşlem, denge kurulduktan sonra özet olarak gösterilebilir."],
         r=["5 elmaya karşı 5 elma yerleştirilir.","7 elmaya karşı 7 elma yerleştirilir.","9 elmaya karşı 9 elma yerleştirilir; sepet konumu değişir."],
         f=["Fazla elmada terazi ters yöne eğilir; çocuk elmayı geri alabilir.","Eşitlikte kefeler ortalanır ve iki taraf da aynı sayıda denir."],
         c="Kefelerde yazılı rakam yerine gerçek elma adetleri kullanılacak; denge sürükleme ile kurulacak."),
    dict(n=33,t="Matematiksel İkizler",g="Eşitlik / Eşit Sonuçları Bulma",a=TEAL,
         o=["Yönerge kısa ancak yakalama hikayesi ve ikiz işlemlerin görsel ilişkisi yeterince belirgin değil."],
         p=["Yönerge 5 + 4 ile aynı sonucu veren ikizini bul ve yakala olarak düzenlensin.","Üstte referans işlem, altta yavaş hareket eden üç işlem kartı ve bir yakalama çemberi bulunsun.","Her karta dokunulduğunda işlem matematiksel biçimde sesli okunsun."],
         r=["5 + 4 işleminin ikizi 6 + 3 bulunur.","7 + 2 işleminin ikizi 10 - 1 bulunur.","8 - 3 işleminin ikizi 2 + 3 bulunur."],
         f=["Yanlış işlem çemberden kaçar ve referans sonuç nesnelerle gösterilir.","Doğru ikizler yan yana gelip aynı renkte parlar."],
         c="İkiz olarak kabul edilen iki işlemin sonucu gerçekten eşit olacak; doğru seçenek konuma göre ezberlenemeyecek."),
    dict(n=34,t="Balon Patlatmaca",g="Eşitlik / Denklemi Yorumlama",a=CORAL,
         o=["Mevcut sahne gerçek balon kalabalığı ve iğneyle sürükleyip patlatma hissini vermiyor; seçim genel dokunma mekaniğinde kalıyor."],
         p=["Ekranda üstlerinde büyük sayılar bulunan çok sayıda renkli balon yavaşça hareket etsin.","Üstte işlem yazsın ve sesli okunsun: İşlemi çöz, sonuca uygun balonu patlat.","Altta güvenli çizgi-film iğnesi bulunsun; çocuk iğneyi doğru balona sürüklesin."],
         r=["9 + 1 için 10 balonu patlatılır.","7 + 2 için 9 balonu patlatılır.","12 - 4 için 8 balonu patlatılır; balonların yerleri değişir."],
         f=["Yanlış balonda iğne esner ve balon patlamaz; bir can eksilir.","Doğru balon konfetiyle patlar, sonuç sesli okunur."],
         c="Balon sayısı seçenekleri okunaklı olacak; doğru sonuç balonu iğneyle fiziksel temas kurunca patlayacak."),
    dict(n=35,t="Halat Çekme Turnuvası",g="Eşitlik / Kuvvet Denkliği",a=GOLD,
         o=["Gerçek halat, iki takım ve sonuçlara uygun oyuncu sayısı görünmüyor; soru yalnız işlem metni ve yön seçimine dayanıyor."],
         p=["Ortada gerçek halat ve iki yanında çeken insanlardan oluşan takımlar bulunsun.","Takımların üstünde işlemler yazsın; her takımda işlemin sonucu kadar kişi görünsün. Örneğin 9 - 2 için tam 7 kişi olmalı.","Yönerge okunduktan sonra altta Sol, Eşit ve Sağ düğmeleri bulunsun; seçimden sonra yarış animasyonu oynasın."],
         r=["Sol 5 + 2, sağ 9 - 2: berabere.","Sol 4 + 4, sağ 3 + 6: sağ takım kazanır.","Sol 10 - 3, sağ 3 + 3: sol takım kazanır."],
         f=["Yanlış yönde işlem sonuçları nesne noktalarıyla gösterilir ve tekrar seçilir.","Doğru kararda halat gerçek kazanan tarafa kayar; eşitlikte ortada kalır."],
         c="Her takımın görünür kişi sayısı, üstündeki işlemin sonucu ile birebir aynı olacak."),
    dict(n=36,t="Sihirli Ayna",g="Eşitlik / İşlem Yansıtma",a=PURPLE,
         o=["Oyun adında ayna olmasına rağmen çift taraflı gerçek ayna ve sürüklenebilir eksik sayı alanı yeterince somut görünmüyor."],
         p=["Ortada iki yüzü görülen büyük, süslü bir ayna bulunsun. Sol tarafta tamamlanmış işlem, sağ tarafta aynı sonucu veren eksik işlem görünsün.","Alttaki sayı taşları sürüklenerek aynanın boşluğuna yerleştirilsin.","Doğru sayı takılınca iki tarafta aynı miktarda yıldız/nesne yansıması belirsin."],
         r=["6 + 2 = 8 ve 10 - ? = 8 için 2 yerleştirilir.","4 + 5 = 9 ve 12 - ? = 9 için 3 yerleştirilir.","7 + 3 = 10 ve 6 + ? = 10 için 4 yerleştirilir."],
         f=["Yanlış taş aynadan geri sekip yerine döner.","Doğru eşitlikte ayna ışık saçar ve iki taraf aynı anda parlar."],
         c="Aynanın iki tarafındaki işlemler ve görsel nesne sayıları aynı sonucu gösterecek."),
    dict(n=37,t="İksir Laboratuvarı",g="Eşitlik / Sıvı Seviyesi Denkliği",a=TEAL,
         o=["Soruda iki tüp anlatılıyor; ancak gerçek tüpler, seviyeler ve eşit/değil seçimini temsil eden açık düğmeler yeterince görünür değil."],
         p=["Yan yana iki büyük şeffaf deney tüpü çizilsin; üstlerinde işlemler, içlerinde sonuca uygun sıvı seviyeleri bulunsun.","Yönerge İki tüp eşitse EŞİT, eşit değilse EŞİT DEĞİL düğmesine dokun desin.","Altta büyük EŞİT ve EŞİT DEĞİL düğmeleri olsun; seçim sonrası işlemlerin sonuçları tüplerin yanında açığa çıksın."],
         r=["8 - 3 ve 1 + 4: EŞİT.","6 + 2 ve 10 - 3: EŞİT DEĞİL.","9 - 4 ve 2 + 3: EŞİT."],
         f=["Yanlış seçimde sıvı seviyeleri çizgiyle karşılaştırılır ve işlem yeniden seslendirilir.","Doğru seçimde tüpler aynı renkte parlar veya farklı renkte ayrışır."],
         c="Tüp seviyeleri işlem sonuçlarıyla matematiksel olarak uyumlu olacak; EŞİT ve EŞİT DEĞİL düğmeleri her platformda büyük ve net görünecek."),
    dict(n=38,t="Zaman Makinesi",g="Toplama-Çıkarma İlişkisi / Geri Sarma",a=CORAL,
         o=["Mevcut oynanış genel uzay gemisi/asteroit şablonunda kalıyor; retro zaman makinesi, çark ve geri sarma hikayesi görünmüyor."],
         p=["Uzay teması kaldırılıp ortada dönen çarkları ve ekranı olan büyük retro zaman makinesi çizilsin.","Ekranda başlangıç işlemi görünsün; altta dişli biçimindeki işlem seçenekleri bulunsun. Çocuk doğru ters işlem dişlisini boş yuvaya sürüklesin.","İşlemler sembol adıyla değil Dokuz eksi iki eşittir yedi biçiminde seslendirilsin.","Doğru dişlide çarklar ters yöne dönsün; 9 toptan 2'si kaybolup 7 top kalsın."],
         r=["5 + 3 = 8 işlemi 8 - 3 = 5 ile geri sarılır.","7 + 2 = 9 işlemi 9 - 2 = 7 ile geri sarılır.","4 + 6 = 10 işlemi 10 - 6 = 4 ile geri sarılır."],
         f=["Yanlış dişli yuvaya oturmaz ve makine çalışmaz; Tekrar dene denir.","Doğru dişlide saat geri akar, toplar azalır ve başlangıç sayısına dönülür."],
         c="Her turda ters işlem gerçek nesne animasyonuyla kanıtlanacak; uzay gemisi ve asteroitler görünmeyecek."),
]


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=MX, rightMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
                      title="1. Sınıf Matematik Kullanıcı Düzeltmeleri - Düzenlenmiş",
                      author="Macera Akademi oyun incelemesi",
                      subject="Yüklenen Oyunlar.pdf içindeki kullanıcı notlarının ayrıntılandırılmış ve düzeltilmiş hali")
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="normal")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=footer)])

story = []
story += [Spacer(1, 27 * mm), P("MACERA AKADEMİ OYUN İNCELEMESİ", cover_kicker),
          P("1. Sınıf Matematik<br/>Düzeltmeleri - Düzenlenmiş Ana Bölüm", cover_title),
          P("Yüklenen kullanıcı notlarının<br/>ayrıntılandırılmış ve uygulamaya hazır hali", cover_sub)]
cover_box = Table([[P("<b>Kapsam</b><br/>Bu belge, Oyunlar.pdf içindeki kullanıcı düzeltmelerini oyun listesindeki gerçek adlarla eşleştirir. Trafik Polisi oyunundan Zaman Makinesi oyununa kadar not eklenmiş 38 oyunu kapsar. Daha önce hazırlanan Kargo Robotunun Hatası - Veterinerin Randevu Defteri devam belgesi bu PDF'e dahil edilmemiştir.")]], colWidths=[148 * mm])
cover_box.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL), ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
    ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("ROUNDEDCORNERS", [9]),
]))
story += [cover_box, Spacer(1, 18 * mm), P("Hazırlanma tarihi: 24 Ağustos 2026", ParagraphStyle("date", parent=small, alignment=TA_CENTER, textColor=MID)), PageBreak()]

story += [P("Ortak uygulama standardı", h1),
          box("Kullanıcı notlarından korunan ana kararlar", [
              "Her oyun üç farklı turdan oluşacak; yalnız bütün turlar tamamlanınca oyun geçilecek.",
              "Yönerge açılışta sesli okunacak ve hoparlör düğmesiyle tekrar dinlenebilecek.",
              "Yanlışta Tekrar dene denecek; üç can bitince Canların bitti mesajı gösterilecek.",
              "İlkokul 1. sınıf öğrencisi uzun metin okumadan görsel, hareket ve sesle cevabı anlayabilecek.",
              "Web sürümündeki bütün sahneler APK'ya aynı görünüm ve mekanikle aktarılacak.",
          ], PALE_CORAL, CORAL), Spacer(1, 5 * mm), P("Uygulama ayrıntıları", h2)]
standard_rows = [
    [P("Ses", box_title), P("+, - ve = işaretleri artı, eksi ve eşittir diye okunacak; tire veya sembol adı kullanılmayacak.", small)],
    [P("Dokunma", box_title), P("Sürükleme parçaları ve hedefler büyük olacak; yanlış bırakılan parça kaybolmadan yerine dönecek.", small)],
    [P("Görsel doğruluk", box_title), P("Nesne adedi, işlem sonucu, animasyon ve sayaç birbirini her zaman doğrulayacak.", small)],
    [P("Web - APK", box_title), P("Renk, yerleşim, ses, tur sırası ve başarı animasyonu iki sürümde de aynı olacak.", small)],
    [P("Bitiş", box_title), P("Her oyunun doğru sonunda hikayeyle ilgili anlamlı bir animasyon oynayacak; yalnız puan artışıyla yetinilmeyecek.", small)],
]
st = Table(standard_rows, colWidths=[34 * mm, 137 * mm])
st.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), PALE_PURPLE), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D8D5E1")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story += [st, PageBreak()]

for x in games:
    story += [header(x["n"], x["t"], x["g"], x["a"]), Spacer(1, 4.5 * mm),
              box("Mevcut ekranda görülen sorun", x["o"], PALE_CORAL, CORAL), Spacer(1, 3 * mm),
              P("Yeni sahne ve oynanış", h2)]
    story += bullets(x["p"])
    story += [Spacer(1, 1 * mm), P("Üç farklı tur", h2), rounds_table(x["r"]), Spacer(1, 3.2 * mm),
              box("Geri bildirim ve bitiş", x["f"], PALE_TEAL, TEAL), Spacer(1, 2.5 * mm),
              P(f"<b>Kabul ölçütü:</b> {x['c']}", small), PageBreak()]

story += [P("Son kabul kontrolü", h1), P("Bu bölüm tamamlanmadan önce", h2)]
story += bullets([
    "Not eklenmiş 38 oyunun her birinde üç farklı tur baştan sona oynanır.",
    "Bütün sayı, nesne, kat, yolcu, elma, damla ve takım adetleri ekrandaki işlemle karşılaştırılır.",
    "Yönerge tekrar dinleme, üç can, Tekrar dene ve Canların bitti akışları web ile APK'da sınanır.",
    "Sihirli Olta ve Cüce Adımı ad değişiklikleri menü, başlık, seslendirme ve başarı ekranlarında birlikte uygulanır.",
    "Şipşak Hafıza önizlemesi APK'da görünür; para/balık/nesne renkleri iki platformda aynı kalır.",
    "Sürükleme hedefleri dar noktalara bağlı olmaz; özellikle Şampiyonlar Kürsüsü telefon ekranında toleranslı çalışır.",
    "Zaman Makinesi dahil her oyunda genel şablon yerine oyunun kendi hikayesini gösteren sahne kullanılır.",
])
story += [Spacer(1, 6 * mm), box("Belge kapsamının sonu", [
    "Bu PDF, kullanıcının ilk belgedeki kendi düzeltmelerini düzenleyip ayrıntılandırır.",
    "Kargo Robotunun Hatası ile başlayan kalan 11 oyun, daha önce hazırlanan ayrı devam PDF'inde yer almaktadır.",
], PALE_TEAL, TEAL)]

doc.build(story)
print(OUT)
