from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle
from pypdf import PdfReader
from pathlib import Path


ROOT = Path("/Users/ceyda/Documents/New project")
OUT = ROOT / "output/pdf/2_sinif_matematik_oyunlari_detayli_duzeltmeler.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

PAGE_W, PAGE_H = A4
MX, TOP, BOTTOM = 17 * mm, 19 * mm, 16 * mm
INK = colors.HexColor("#262139")
PURPLE = colors.HexColor("#493B73")
TEAL = colors.HexColor("#168A8A")
CORAL = colors.HexColor("#E45F58")
GOLD = colors.HexColor("#E2A62D")
BLUE = colors.HexColor("#3E73A8")
PALE_PURPLE = colors.HexColor("#F2EEFA")
PALE_TEAL = colors.HexColor("#EAF7F5")
PALE_CORAL = colors.HexColor("#FFF0ED")
PALE_GOLD = colors.HexColor("#FFF7E4")
PALE_BLUE = colors.HexColor("#EDF4FA")
MID = colors.HexColor("#7A7687")

base = getSampleStyleSheet()["BodyText"]
body = ParagraphStyle("body", parent=base, fontName="Arial", fontSize=8.4, leading=11.0, textColor=INK, spaceAfter=1.1 * mm)
small = ParagraphStyle("small", parent=body, fontSize=7.7, leading=9.7, spaceAfter=0.8 * mm)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=4.7 * mm, firstLineIndent=-3.0 * mm, bulletIndent=0, spaceAfter=0.85 * mm)
bullet_small = ParagraphStyle("bullet_small", parent=small, leftIndent=4.7 * mm, firstLineIndent=-3.0 * mm, bulletIndent=0, spaceAfter=0.7 * mm)
h1 = ParagraphStyle("h1", parent=body, fontName="Arial-Bold", fontSize=21, leading=25, textColor=PURPLE, spaceAfter=4 * mm)
h2 = ParagraphStyle("h2", parent=body, fontName="Arial-Bold", fontSize=10.4, leading=12.5, textColor=TEAL, spaceBefore=1.4 * mm, spaceAfter=0.9 * mm)
cover_kicker = ParagraphStyle("cover_kicker", parent=body, fontName="Arial-Bold", fontSize=10, textColor=TEAL, alignment=TA_CENTER, spaceAfter=6 * mm)
cover_title = ParagraphStyle("cover_title", parent=body, fontName="Arial-Bold", fontSize=25, leading=30, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=5 * mm)
cover_sub = ParagraphStyle("cover_sub", parent=body, fontSize=12, leading=17, alignment=TA_CENTER, spaceAfter=9 * mm)
game_title = ParagraphStyle("game_title", parent=body, fontName="Arial", fontSize=13.7, leading=16, textColor=colors.white, spaceAfter=0)
badge = ParagraphStyle("badge", parent=body, fontName="Arial-Bold", fontSize=16, leading=17, textColor=colors.white, alignment=TA_CENTER, spaceAfter=0)
box_title = ParagraphStyle("box_title", parent=body, fontName="Arial-Bold", fontSize=9.4, leading=11.4, textColor=CORAL, spaceAfter=0.8 * mm)
round_head = ParagraphStyle("round_head", parent=small, fontName="Arial-Bold", fontSize=8.0, leading=9.4, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=0)
round_text = ParagraphStyle("round_text", parent=small, fontSize=7.25, leading=9.1, spaceAfter=0)
theme_title = ParagraphStyle("theme_title", parent=cover_title, fontSize=24, leading=29, textColor=colors.white)


def P(text, style=body):
    return Paragraph(text, style)


def bullets(items, style=bullet):
    return [Paragraph(x, style, bulletText="•") for x in items]


def header(number, title, subtitle, accent):
    t = Table([[P(str(number), badge), P(f"<b>{title}</b><br/><font size='8' color='#F1EEF8'>{subtitle}</font>", game_title)]],
              colWidths=[15 * mm, 161 * mm], rowHeights=[19 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("RIGHTPADDING", (1, 0), (1, 0), 8),
        ("ROUNDEDCORNERS", [8]),
    ]))
    return t


def box(title, items, bg, title_color, compact=False):
    title_style = ParagraphStyle("dynamic_box_title", parent=box_title, textColor=title_color)
    content = [P(title, title_style)] + bullets(items, bullet_small if compact else bullet)
    t = Table([[content]], colWidths=[176 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D7D3DF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROUNDEDCORNERS", [6]),
    ]))
    return t


def rounds_table(items):
    t = Table([
        [P("1. TUR", round_head), P("2. TUR", round_head), P("3. TUR", round_head)],
        [P(items[0], round_text), P(items[1], round_text), P(items[2], round_text)],
    ], colWidths=[58.7 * mm, 58.7 * mm, 58.6 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALE_GOLD),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFCF5")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDCFAB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
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
    canv.line(MX, PAGE_H - 12.5 * mm, PAGE_W - MX, PAGE_H - 12.5 * mm)
    canv.setFont("Arial", 7.4)
    canv.setFillColor(MID)
    canv.drawString(MX, 8.5 * mm, "2. Sınıf Matematik - Ayrıntılı Oyun Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 8.5 * mm, str(canv.getPageNumber()))
    canv.restoreState()


def G(n, theme, title, sub, observed, risk, new, rounds, feedback, acceptance):
    return dict(n=n, theme=theme, title=title, sub=sub, observed=observed, risk=risk,
                new=new, rounds=rounds, feedback=feedback, acceptance=acceptance)


games = [
G(1, "Tema 1", "Şeker Canavarının Makinesi", "Sayının farklı gösterimleri",
  ["Oyunu açınca şeker canavarı yerine su altı sahnesi, hareketli kartlar ve kepçe görülüyor; başlık ile gerçek sahne birbirini desteklemiyor.", "45'in dört gösterimi tek sabit soruda seçiliyor; kartların hareket etmesi yazıları okumayı ve yanlış seçimin nedenini anlamayı zorlaştırıyor."],
  ["Çocuk sayı temsilleri arasındaki bağı kurmak yerine hareket eden etiketi yakalamaya odaklanabilir.", "Tek sayı kullanıldığı için onluk-birlik, sayı adı ve çözümleme ilişkisi genellenemiyor."],
  ["Gerçek bir şeker makinesi ve göbeğinde hedef sayı bulunan sevimli canavar çizilsin.", "Şekerler bantta sabit ve okunaklı ilerlesin; doğru olanlar canavarın ağzına sürüklensin.", "Her doğru şeker yendiğinde hedef sayının ilgili bölümü ışıklansın: rakam, sayı adı, onluk-birlik ve çözümleme.", "Yanlış şeker makineye geri dönsün; oyun doğru cevabı doğrudan söylemeden hangi temsilin uyuşmadığını göstersin."],
  ["34 için 34, otuz dört, 3 onluk 4 birlik ve 30 + 4 seçilir.", "58 için dört doğru temsil, 85 ve 50 + 8 gibi karıştırıcılarla ayrılır.", "Hedef 72 olur; çocuk önce onluk-birliği kurar, sonra kalan üç temsili eşler."],
  ["Yanlış seçimde 54 ile 45'in basamakları renkli onluk çubuklarıyla karşılaştırılsın.", "Doğru dört temsil tamamlanınca canavar doysun, makine hedef sayıyı sesli ve matematiksel dille özetlesin.", "Üç turda kart sırası ve hedef sayı değişsin; doğru kartlar aynı konumda kalmasın."],
  ["Sahne su altı/kepçe şablonu içermeyecek; canavar ve şeker makinesi ekranda gerçek rol oynayacak.", "Her turda dört temsil de hedef sayıyla birebir uyumlu olacak ve 3 tur baştan sona oynanabilecek."]),

G(2, "Tema 1", "Kargo Treni Yüklemesi", "Onluk ve birlik ile sayı kurma",
  ["Açılışta tren, vagon ve yük istasyonu görünmüyor; ortada boş bir dikdörtgen ve altta iki düğme bulunuyor.", "Yönerge yükleri vagona koymayı söylerken etkileşim kutuya dokunup sayacı artırmaya dayanıyor; 10 birlik değişimi yalnız yazıyla anlatılıyor."],
  ["Basamak değeri fiziksel gruplama olmadan soyut sayaç işlemine dönüşüyor.", "Çocuk 10 birliğin neden 1 onluğa eşit olduğunu görmeden yalnız toplam değeri tamamlayabilir."],
  ["Lokomotif, iki vagon ve istasyonda gerçek onluk kasaları ile birlik paketleri çizilsin.", "Çocuk kasaları ve paketleri sürüklesin; vagondaki nesneler gerçekten sayılabilsin.", "On birlik birikince paketler animasyonla bağlanıp tek onluk kasaya dönüşsün; ters değişim de yapılabilsin.", "Vagonun üstünde 3 onluk + 4 birlik = 34 ifadesi yalnız işlem sonunda görünsün."],
  ["34 yüklenir: 3 onluk kasa, 4 birlik paket.", "47 yüklenir; önce 2 onluk ve 27 birlik verilir, çocuk değişim yapar.", "62 yüklenir; bir fazla onluk konur, çocuk fazlayı geri alıp dengeyi düzeltir."],
  ["Fazla yükte tren yalnız 'ağır' demesin; hangi vagonun hedefi aştığı kırmızı ölçerle gösterilsin.", "Doğru yükte tüm paketler tek tek sayılıp lokomotif hareket etsin.", "Değişim için sesli ifade: On birlik bir onluk eder."],
  ["Tren ve yükler sahnenin ana etkileşimi olacak; boş kutu içine sayaç doldurmak yeterli sayılmayacak.", "Hedef, onluk sayısı, birlik sayısı ve toplam değer her turda aynı sonucu vermeli."]),

G(3, "Tema 1", "Zıpzıp Kurbağa", "Sayı sırasındaki eksiği bulma",
  ["Sayı kartları okunaklı olsa da sahnede kurbağa ve karşı kıyıya ilerleme eylemi görünmüyor; nilüferler kart etiketi olarak kalıyor.", "Tek dizi 18, 19, ?, 21 biçiminde ve artış kuralı sabit; oyun bir seçim sorusu gibi bitiyor."],
  ["Hikaye ile matematik eylemi ayrışıyor; doğru sayının kurbağayı neden ilerlettiği görülmüyor.", "Yalnız birer artan örüntü, önceki-sonraki sayı ve farklı başlangıçları ölçmüyor."],
  ["Nehir üzerinde aralıklı gerçek nilüferler ve başlangıçta kurbağa çizilsin.", "Eksik nilüfer suyun üstünde boş kalsın; sayı taşı seçilip boşluğa sürüklensin.", "Doğru taşta kurbağa bütün nilüferlere sırayla zıplayıp sayıları sesli okusun.", "Sayı doğrusu altta kısa süre görünerek eksik sayının iki komşusu vurgulansın."],
  ["18, 19, ?, 21 dizisinde 20 bulunur.", "36, ?, 38, 39 dizisinde 37 bulunur; boşluk ortada değildir.", "64, 65, 66, ? dizisinde 67 bulunur; seçenekler 57, 67, 76 olarak hazırlanır."],
  ["Yanlış taş suya düşmeden geri döner; Önce 19'dan sonra gelen sayıyı düşün denir.", "Doğru cevapta zıplama sırası ile yazılı sayı aynı anda ilerler.", "Tur sonunda önceki sayı, sonraki sayı ve eksik sayı birlikte özetlenir."],
  ["Kurbağa en az bir kez gerçek bir rota boyunca hareket edecek.", "Üç turda boşluğun yeri ve sayı aralığı değişecek; seçenekler yalnız konuma göre ezberlenemeyecek."]),

G(4, "Tema 1", "Uzaylı Trambolini", "Ritmik sayma",
  ["Oyunda uzaylı ve trambolin yerine roket ile yakıt hunisi görülüyor; sayı kartları uzayda hareket ediyor.", "Kazanım metni birer, ikişer, beşer ve onar saymayı söylerken mevcut tek görev üçer ritmik sayma istiyor."],
  ["Hikaye uyumsuzluğuna ek olarak kazanım-görev uyuşmazlığı ölçme geçerliğini düşürüyor.", "Hareketli kartlar sıralama bilgisinden çok hedef yakalama becerisini öne çıkarıyor."],
  ["Ay yüzeyinde beş trambolin ve zıplayan uzaylı karakteri bulunsun.", "Her trambolinde sayı sabit ve büyük yazılsın; çocuk doğru sıradaki tramboline dokunsun.", "Ritmik sayma türü tur başında sesli belirtilsin ve adım büyüklüğü renkli bir yayla gösterilsin.", "Yanlış trambolin uzaylıyı fırlatmasın; önceki sayı ile hedef arasındaki fark nesne gruplarıyla gösterilsin."],
  ["İkişer sayma: 2, 4, 6, 8, 10.", "Beşer sayma: 5, 10, 15, 20, 25.", "Onar sayma: 10, 20, 30, 40, 50; başlangıç trambolini değişir."],
  ["Yanlış seçimde Bir sonraki sayı için 2 ekle gibi kural ipucu verilsin.", "Doğru sırada uzaylı her trambolinde sayıyı seslendirsin.", "Tur sonunda sayı dizisi sabit kalıp çocukla birlikte tekrar okunsun."],
  ["Görevler kazanımdaki 2, 5 ve 10'ar saymayı kapsayacak; üçer sayma ana değerlendirme olmayacak.", "Roket-yakıt şablonu kullanılmayacak; trambolinler hem görsel hem etkileşimsel olacak."]),

G(5, "Tema 1", "Sihirli Pasta Süsleme", "Örüntüyü sürdürme",
  ["Çilek ve mum kartları düz bir satırda gösteriliyor; pasta, kesme tahtası veya süsleme alanı yok.", "Tek AB örüntüsü ve tek eksik öğe kullanıldığı için çocuk kuralı açıklamadan yalnız sıradaki simgeyi seçebiliyor."],
  ["Örüntü oluşturma, gerçek bir model kurmak yerine statik test sorusuna dönüşüyor.", "AAB, ABB veya büyüyen örüntüler görülmediği için genelleme sınırlı kalıyor."],
  ["Dönen büyük bir pasta ve çevresinde eşit aralıklı boş süs yuvaları çizilsin.", "Çilek, mum, yıldız ve krema parçaları alttan sürüklenerek pastaya yerleştirilsin.", "Çocuk yalnız boşluğu doldurmasın; bir turda örüntüyü iki adım sürdürsün, bir turda yanlış süsü bulsun.", "Kural tamamlanınca pasta bir tam tur dönsün ve tekrar eden birim çerçevelensin."],
  ["Çilek-mum-çilek-mum-? dizisine mum eklenir.", "Çilek-çilek-mum örüntüsü iki adım sürdürülür.", "Yıldız-krema-krema dizisinde yanlış konmuş yıldız bulunup düzeltilir."],
  ["Yanlış süs yuvaya oturmaz; tekrar eden küçük grup parlayarak ipucu verir.", "Doğru süs fiziksel olarak pastaya yapışır ve sıra sesli okunur.", "Tur bitişinde çocuk kuralı görsel seçeneklerden seçer: bir çilek, bir mum gibi."],
  ["Pasta gerçek oyun alanı olacak; örüntü yalnız kart satırı olarak kalmayacak.", "Üç tur en az iki farklı örüntü yapısı ve iki farklı görev türü içerecek."]),

G(6, "Tema 1", "Uçan Balonları Kurtar", "Tahmin ve onarlı sayma",
  ["Balonlar ve bulut yerine boş bir pano, soru işareti ve 20-30-40 düğmeleri görülüyor.", "Tahmin seçildikten sonra gerçek balonların açılıp onarlı gruplar halinde sayılması sahnede gösterilmiyor."],
  ["Tahmin, gözleme dayalı olmadan üç seçenekten rastgele seçime dönüşebilir.", "Gerçek miktar ile onarlı gruplama ilişkisi görünmediği için strateji geliştirilemez."],
  ["Bulutun arkasından kenarları kısmen görünen gerçek balon demetleri çizilsin.", "Çocuk tahminini sayı doğrusu veya 10'luk demet düğmeleriyle işaretlesin.", "Tahminden sonra rüzgar bulutu açsın; balonlar onarlı ağlara ayrılıp 10, 20, 30 diye sayılsın.", "Tahmin ile gerçek sonuç yan yana gösterilip fark kaç balon sorulsun."],
  ["Yaklaşık 20 balon: gerçek sonuç 22.", "Yaklaşık 30 balon: gerçek sonuç 28.", "Yaklaşık 40 balon: gerçek sonuç 37; balonlar daha dağınık yerleştirilir."],
  ["Uzak tahminde ceza yerine Önce dolu onluk gruplarını ara ipucu verilsin.", "Yakın tahmin ayrıca takdir edilsin; tek bir tam sayı zorunlu tutulmasın.", "Açılma animasyonu bitmeden gerçek sayı yazıyla gösterilmesin."],
  ["Tahminden önce miktarın en az bir bölümü görünür olacak.", "Her turda gerçek balonlar onarlı gruplara ayrılıp sayılabilecek; boş pano kabul edilmeyecek."]),

G(7, "Tema 1", "Hayvanat Bahçesi Fotoğrafçısı", "Küçükten büyüğe sıralama",
  ["Hayvanat bahçesi ve fotoğrafçı yerine roket-yakıt sahnesi var; hayvanlar küçük hareketli etiketlere dönüşüyor.", "Yalnız 12, 15 ve 18 sayıları kullanılıyor; sıralama tamamlanınca hayvanların fiziksel bir sıraya girdiği görülmüyor."],
  ["Hareketli hedefler okuma ve dokunma yükünü artırıyor; matematiksel sıralama ikinci planda kalıyor.", "Üç sayıyla tek tur, basamak karşılaştırması stratejisini ölçmüyor."],
  ["Hayvanat bahçesi girişinde üç-beş hayvan ve yerde numaralı fotoğraf noktaları bulunsun.", "Çocuk hayvanları formalarındaki sayıya göre soldan sağa sürükleyerek dizer.", "Onluk basamağı aynı olan sayılarda birlikler, farklı olanlarda önce onluklar vurgulansın.", "Doğru sıra oluşunca fotoğrafçı deklanşöre bassın ve sıra sabitlensin."],
  ["12, 15, 18 küçükten büyüğe dizilir.", "27, 21, 29, 24 dört hayvanla sıralanır.", "46, 64, 41, 59, 50 beş hayvanla sıralanır; onluklar farklıdır."],
  ["Yanlış komşulukta iki forma büyütülüp Hangi onluk daha küçük? denir.", "Doğru her yerleştirmede sayı sesli okunur, tüm sıra bitmeden başarı verilmez.", "Tur sonunda küçükten büyüğe ok yönü görünür."],
  ["Roket ve yakıt hunisi kaldırılacak; hayvanlar sabit sürükleme nesnesi olacak.", "Sıralama en az üç farklı sayı kümesinde ve değişen öğe sayısıyla çalışacak."]),

G(8, "Tema 2", "Sihirli Şefin Kesme Tahtası", "Bütün, yarım ve çeyrek",
  ["Pizza görseli ve bölme seçenekleri konuya uygun; ancak çocuk pizzayı kesmiyor, yalnız 2'ye Böl düğmesine dokunuyor.", "Yanlış seçim doğrudan Önce iki eş parçaya bölmeliyiz diyerek cevabı söylüyor; eş parça koşulu deneyimlenmiyor."],
  ["Doğru düğmeyi tanıma, eş parçalar oluşturma becerisinin yerini alıyor.", "Aynı pizza ve aynı sıra tekrarlandığında cevap kolayca ezberlenebilir."],
  ["Kesme çizgisi çocuk tarafından pizzanın üzerinde sürüklenerek yerleştirilsin.", "Parçalar eş değilse iki parçanın alan farkı renkli kaplamayla gösterilsin; çocuk çizgiyi düzeltsin.", "Yarım aşamasında iki parça ayrılıp yeniden bütünleştirilebilsin; çeyrekte dört eş parçanın tamamı sayılabilsin.", "Pizza dışında sandviç ve kek gibi ikinci modeller de kullanılsın."],
  ["Pizzayı iki eş parçaya bölerek yarımları oluştur.", "İki yarımı yeniden bölerek dört çeyrek oluştur.", "Dört çeyrekten iki yarımı, iki yarımdan bir bütünü yeniden birleştir."],
  ["Yanlış çizgide cevap söylenmeden Parçaların büyüklüklerini karşılaştır ipucu verilsin.", "Doğru kesimde parçalar ayrılıp eş oldukları üst üste getirilerek kanıtlansın.", "Bitişte 1 bütün = 2 yarım = 4 çeyrek görsel modellerle okunmalı."],
  ["Çocuk en az bir turda kesme çizgisini kendisi belirleyecek.", "Eşlik yalnız yazıyla değil parçaların üst üste gelmesiyle doğrulanacak."]),

G(9, "Tema 2", "Kumbara Canavarı", "Kuruş ve TL ilişkisi",
  ["Sahnede kumbara canavarı yalnız küçük bir simge; ana alan boş bir kutu ve para düğmelerinden oluşuyor.", "1 TL hedefi tek turda 100 kuruşa ulaşma sayacı olarak oynanıyor; gerçek madeni para boyutu ve iki farklı çözüm yolu görünmüyor."],
  ["Çocuk para değerini nesne olarak değil sayı artıran buton olarak algılayabilir.", "Farklı para bileşimlerinin aynı değere ulaştığı gösterilmezse esneklik gelişmez."],
  ["Büyük, ağzı açılıp kapanan kumbara canavarı ve masada gerçekçi 10, 25 ve 50 kuruş yüzleri çizilsin.", "Paralar tek tek sürüklensin; içeride seçilen paralar yan yana kalıp toplamın nasıl oluştuğu görülsün.", "100 kuruşa ulaşınca canavar 1 TL madeni para çıkararak eşdeğerliği göstersin.", "Aynı hedef için birden fazla çözüm kabul edilsin ve tur sonunda kullanılan para sayısı karşılaştırılsın."],
  ["2 tane 50 kuruş ile 1 TL oluştur.", "4 tane 25 kuruş ile 1 TL oluştur.", "50 + 25 + 10 + 10 + 5 kuruş ile 1 TL oluştur; 5 kuruş parası da eklenir."],
  ["Fazla parada kumbara taşmak yerine son eklenen para dışarı zıplasın ve kalan fark söylensin.", "Doğru toplamda paralar gruplanıp Yüz kuruş bir Türk lirasıdır denilsin.", "İkinci doğru çözüm ayrıca Farklı paralar, aynı toplam diye vurgulansın."],
  ["Madeni para görselleri ve değerleri birbirinden ayırt edilebilir olacak.", "En az üç farklı para bileşimiyle 100 kuruş tamamlanabilecek."]),

G(10, "Tema 2", "Market Ekspresi", "Ürün için doğru parayı seçme",
  ["Market, kasa ve hikaye kitabı görünmüyor; fiyat ve para düğmeleri koyu bir sayaç ekranında kalıyor.", "50 TL seçildiğinde fazla ödeme için para üstü verme seçeneği yok; yalnız daha küçük para seç uyarısı var."],
  ["Günlük yaşam bağlamı kayboluyor ve çocuk ödeme yerine hedef sayıyı topluyor.", "Gerçek alışverişte fazla para ve para üstü ilişkisi ele alınmıyor."],
  ["Kasada kitap, fiyat etiketi, cüzdan ve para bölmeleri görünür olsun.", "Çocuk banknotları kasiyerin tepsisine sürüklesin; her banknot fiziksel olarak kalsın.", "Bir tur tam ödeme, bir tur iki ürünün toplamı, bir tur para üstü alma içersin.", "Kasiyer ödeme tamamlanmadan ürünü vermesin; işlem nesnelerle birlikte kurulmalı."],
  ["45 TL kitap için 20 + 20 + 5 TL verilir.", "28 TL defter ve kalem toplamı için 20 + 5 + 2 + 1 TL verilir.", "35 TL ürün için 50 TL verilir; 15 TL para üstü seçilir."],
  ["Eksik ödemede kalan tutar söylenir; fazla ödemede para üstü tepsisi açılır.", "Doğru ödeme banknotlar sayılarak ve toplam işlem okunarak doğrulanır.", "Yanlış banknot kaybolmaz; cüzdana geri alınabilir."],
  ["Ürün, fiyat, verilen para ve para üstü aynı sahnede tutarlı olacak.", "Tek sayaç kutusu yerine gerçek market etkileşimi üç turda çalışacak."]),

G(11, "Tema 2", "Zaman Makinesi Tamircisi", "Tam, yarım ve çeyrek saat",
  ["Saat çizimi açık ve konuya uygun; ancak yönerge akrep ve yelkovanı sürüklemeyi söylerken gerçek etkileşim dört ileri-geri düğmesiyle yapılıyor.", "İlk ekran 12:00 gösterirken hedef Saat 3; çocuğun hangi ibreyi ne kadar hareket ettirdiği doğrudan deneyimlenmiyor."],
  ["Yönerge-etkileşim çelişkisi çocuğu gereksiz deneme yapmaya yöneltebilir.", "İbrelerin birlikte hareketi ve saat-dakika ilişkisi buton artırımına indirgeniyor."],
  ["Akrep ve yelkovan uçlarından doğrudan sürüklenebilir olsun; seçilen ibre renkli parlasın.", "Yelkovan bir tur döndüğünde akrep bir saat ilerlesin; bu ilişki animasyonla gösterilsin.", "Dijital saat yalnız Onay sonrasında açılıp analog saatle karşılaştırılsın.", "Zaman makinesindeki çarklar doğru saatte çalışsın; yanlış onayda ibreler sabit kalsın."],
  ["Saat tam 3 yapılır.", "Saat 9 buçuk yapılır; yelkovan 6'da, akrep 9 ile 10 arasında olur.", "6'yı çeyrek geçe ve 1'e çeyrek kala iki alt görev olarak uygulanır."],
  ["Yanlış onayda Hangi ibre dakikayı gösteriyor? gibi kavramsal ipucu verilsin.", "Doğru saatte saat hem günlük dille hem dijital biçimde seslendirilsin.", "İbreler çeyrek saatlerde doğru ara konuma yerleşmeli; akrep tam sayı üzerinde kalmamalı."],
  ["Yönerge gerçekten sürükleme yaptıracak veya metin düğmelere göre yeniden yazılacak; ikisi çelişmeyecek.", "Dört hedef saatin analog ve dijital gösterimleri matematiksel olarak doğru olacak."]),

G(12, "Tema 2", "Mevsim Ağacı Takvimi", "Ay, mevsim ve yıl ilişkisi",
  ["Ay kartları dört mevsim satırına sürükleniyor; fakat takvim yaprakları ve büyüyen mevsim ağacı sahnede yok.", "Yalnız Ocak, Nisan, Temmuz ve Ekim kullanıldığı için ayların mevsim içindeki sırası ve bir yıldaki 12 ay ilişkisi kurulmamış."],
  ["Görev basit eşleştirmede kalıyor; takvim-zaman döngüsü ve mevsim geçişi görünmüyor.", "Her mevsimden tek örnek ay seçmek, sınır aylarını ve sıralamayı ölçmüyor."],
  ["Ortada dört mevsime bölünmüş büyük bir ağaç ve çevresinde 12 aylık dairesel takvim bulunsun.", "Ay yaprakları doğru dala sürüklendikçe ağacın rengi ve hava durumu değişsin.", "Her dalda aylar kendi içinde doğru sıraya dizilsin; yalnız kategoriye bırakmak yetmesin.", "Bir yıl tamamlanınca takvim çemberi dönüp yeniden Ocak'a gelsin."],
  ["Ocak, Nisan, Temmuz ve Ekim doğru mevsime yerleştirilir.", "Mart, Haziran, Eylül ve Aralık mevsim geçişleriyle eşleştirilir.", "12 ay dört dala sırayla yerleştirilir; her mevsimde üç ay olduğu görülür."],
  ["Yanlış dalda yaprak geri döner; o dalın hava/renk ipucu belirir.", "Doğru ayda mevsim adı ve ay adı birlikte okunur.", "Tur sonunda 12 ay, 4 mevsim, 1 yıl ilişkisi görsel çemberle özetlenir."],
  ["Ağaç ve takvim yalnız süs değil, yerleştirme hedefi olacak.", "Son turda tüm 12 ay doğru sıra ve doğru mevsimde bulunacak."]),

G(13, "Tema 2", "Terzinin Kumaşları", "Standart ölçü birimine ihtiyaç",
  ["Terzi ve kumaş yerine uzay gemisi ile hareketli meteor seçenekleri görülüyor; uzun metinler hareketli hedeflerin üzerine yazılmış.", "Kumaşın 5 karış ve 3 karış ölçülmesi yalnız cümlede geçiyor; iki farklı el büyüklüğü ve ölçme süreci gösterilmiyor."],
  ["Çocuk standart ölçü gereksinimini deneyimlemek yerine uzayda doğru metni yakalıyor.", "Karış farkının nedeni somutlaşmadığı için cevap ezberlenebilir."],
  ["Terzi masasında aynı kumaş, biri çocuk biri yetişkin olan iki el modeli çizilsin.", "Çocuk her iki el modelini kumaş boyunca boşluksuz sürükleyerek karış sayılarını görsün.", "Sonra cetvel ve metre ile ölçüm yapsın; aynı 60 cm sonucunun tekrarlandığını deneyimlesin.", "Ölçüm başlangıç ve bitiş noktaları net işaretlensin; arada boşluk ve üst üste binme engellensin."],
  ["Çocuk eliyle 5, terzi eliyle 3 karış ölçülür; fark açıklanır.", "Aynı kumaş iki farklı cetvelle 60 cm ölçülür.", "1 metrelik şerit üzerinde 100 santimetre işaretlenip metre-santimetre ilişkisi kurulur."],
  ["Yanlış açıklamada iki el üst üste gösterilerek büyüklük farkı görünür kılınsın.", "Doğru ölçümde cetvel birimleri tek tek izlenip sonuç sesli okunsun.", "Uzay lazeri ve hareketli cevap taşları bu oyunda kullanılmasın."],
  ["Kumaş gerçek ölçme eylemiyle en az iki farklı araç kullanılarak ölçülecek.", "Standart aracın aynı sonucu verdiği animasyonla kanıtlanacak."]),

G(14, "Tema 2", "Manav Terazisi", "Kütle tahmini ve ölçüm",
  ["Karpuz ve terazi görünmüyor; boş pano üzerinde 1, 5 ve 20 kg seçenekleri bulunuyor.", "Tahminden sonra ölçümün nasıl yapıldığı görülmeden 5 kg bilgisi açılıyor."],
  ["Nesne boyutu, günlük deneyim ve terazi göstergesi kullanılmadığı için tahmin rastgele olabilir.", "Tahmin ile ölçüm karşılaştırması gerçek bir gözlem süreci oluşturmuyor."],
  ["Manav tezgahında karpuz, elma kasası ve eşit kollu/dijital terazi çizilsin.", "Çocuk nesneyi önce eline alıp görsel ipuçlarıyla tahmin etsin, sonra teraziye sürüklesin.", "Gösterge ibresi animasyonla hareket edip tam kg değerinde dursun.", "Tahmin-gerçek farkı sayı doğrusunda gösterilsin; yakın tahmin ayrıca değerlendirilirsin."],
  ["Karpuz 5 kg tahmin edilir ve ölçülür.", "Elma kasası 8 kg; seçenekler 2, 8, 20 kg olur.", "Kabak 3 kg; çocuk sayısal tahmin girer ve farkı bulur."],
  ["Uzak tahminde nesneler arası karşılaştırma ipucu verilsin: Karpuz bir elmadan ağırdır.", "Doğru ölçümde terazi, nesne ve değer aynı anda görünür.", "Tur sonunda tahminim, gerçek sonuç ve fark başlıklarıyla özet sunulsun."],
  ["Her turda gerçek nesne ve çalışan terazi görülecek; boş pano kabul edilmeyecek.", "Kütle değerleri nesnelerin gerçekçi büyüklükleriyle makul olacak."]),

G(15, "Tema 3", "Fırıncının Sepeti", "Günlük yaşam problemi",
  ["Fırın ve simitler yerine uzay lazeri sahnesinde hareketli kaya seçenekleri görülüyor.", "15 simitten 4'ünün yenmesi yalnız metinle anlatılıyor; azalma eylemi ve kalan simitler sayılmıyor."],
  ["Problem çözme, hikayeyi modellemek yerine hareketli doğru şıkkı yakalamaya dönüşüyor.", "Çocuk neden çıkarma yaptığını nesne değişiminden çıkaramıyor."],
  ["Fırın tezgahında sepette 15 simit görünür ve dört simit karakterlere tek tek verilir.", "Çocuk önce olayın arttı mı azaldı mı olduğunu animasyondan seçsin, sonra işlemi kursun.", "Simitler onluk ve birlik gruplarına ayrılarak 15 - 4 işlemi somutlaştırılsın.", "Sonuç seçilmeden önce çocuk kalan simitleri gruplayıp sayabilsin."],
  ["15 simitten 4'ü yenir: 11 kalır.", "20 poğaçadan 6'sı satılır: 14 kalır.", "12 ekmeğe 7 yeni ekmek gelir: 19 olur; bu kez toplama seçilir."],
  ["Yanlış işlemde olay animasyonu geri oynatılıp miktarın yönü gösterilsin.", "Doğru çözümde hikaye, işlem ve sonuç aynı ekranda okunur.", "Kaya seçenekleri ve uzay gemisi kaldırılmalı; seçenekler gerekirse tezgah kartı olarak sabit durmalı."],
  ["Her turda nesne sayısı işlemle birebir eşleşecek.", "Toplama ve çıkarma en az birer turda olay üzerinden seçilecek."]),

G(16, "Tema 3", "Lunapark Balonları", "Tahmin ve zihinden işlem",
  ["Dart, lunapark ve balonlar görünmüyor; boş bir pano ve 30-40-50 düğmeleri var.", "22 + 19 için yalnız tek tahmin soruluyor; yuvarlama adımları seçimden sonra metin olarak açıklanıyor."],
  ["Çocuk tahmin stratejisini kurmadan en yakın onluğu rastgele seçebilir.", "Tek işlem, farklı yuvarlama ve parçalama yollarını karşılaştırmaya yetmiyor."],
  ["Lunapark standında 30, 40 ve 50 yazılı gerçek balonlar ve elde dart oku bulunsun.", "İşlem önce onluklara yuvarlanarak iki ayrı balon demeti üzerinde gösterilsin.", "Çocuk tahmin balonunu vurduktan sonra gerçek sonucu sayı doğrusu üzerinde kontrol etsin.", "Tahmin ile gerçek sonuç arasındaki fark görsel olarak iki adımlık sapma biçiminde gösterilsin."],
  ["22 + 19 yaklaşık 40, gerçek sonuç 41.", "37 + 24 yaklaşık 60, gerçek sonuç 61.", "48 - 21 yaklaşık 30, gerçek sonuç 27; toplama ve çıkarma karşılaştırılır."],
  ["Uzak tahminde Hangi sayıları en yakın onluğa çevirdin? sorusu gelsin.", "Doğru/çok yakın tahminde balon patlayıp gerçek sonuç açılır.", "Boş pano yerine balonların büyüklüğü, dart ve sayı doğrusu görünür olmalı."],
  ["Üç turda en az iki farklı tahmin stratejisi kullanılabilecek.", "Tahmin ve kesin sonuç ayrı aşamalar olarak ölçülecek."]),

G(17, "Tema 3", "Zaman Makinesi Asansörü", "Toplama ve çıkarmanın tersliği",
  ["Asansör ve katlar yerine uzay gemisiyle hareketli kaya seçenekleri var.", "0 + 5 = 5 ve 5 - 5 = 0 ilişkisi yalnız metinsel seçenek olarak sunuluyor; kabinin geri dönmesi görünmüyor."],
  ["Ters işlem ilişkisi fiziksel hareketle kurulamadığı için soru ezberlenebilir.", "Hareketli seçenekler uzun işlem cümlelerinin okunmasını güçleştiriyor."],
  ["Şeffaf bir asansör boşluğu, numaralı katlar ve yukarı-aşağı düğmeleri çizilsin.", "Kabinin her hareketinde kat sayacı ve işlem birlikte güncellensin.", "Çocuk gidiş hareketini izledikten sonra dönüş için ters yön ve ters işlemi seçsin.", "Başlangıç kata dönünce iki hareket izi farklı renklerde üst üste gelsin."],
  ["0'dan 5 kat çık, 5 kat in ve 0'a dön.", "8'den 3 kat in, 5'e gel; 3 kat çıkıp 8'e dön.", "4'e 7 ekle, sonra 7 çıkar; başlangıç sayısının değişmediğini göster."],
  ["Yanlış yönde kabin hareket etmeden ok ve işlem karşılaştırılsın.", "Doğru dönüşte Gidiş ve dönüş birbirinin tersidir denilsin.", "Her tur sonunda iki işlem yan yana, aynı üç sayı ile gösterilsin."],
  ["Asansör kabini gerçek katlar arasında hareket edecek.", "Ters işlem aynı sayıların ilişkisiyle üç farklı senaryoda kanıtlanacak."]),

G(18, "Tema 3", "Robot Paketleme Bandı", "Tekrarlı toplamadan çarpmaya",
  ["Dört kutu görünse de içleri başlangıçta boş; robotlar ve hareketli paketleme bandı görünmüyor.", "Kutulara sırayla dokunmak sayacı artırıyor; her kutuda 3 robotun gerçekten oluşması ve 3 + 3 + 3 + 3 bağlantısı yeterince güçlü değil."],
  ["Çarpma, eş gruplar yerine dört düğmeye basma dizisi olarak algılanabilir.", "Tek 4 x 3 örneği grup sayısı ile grup büyüklüğünün rollerini genellemez."],
  ["Yürüyen bantta robotlar gelsin; çocuk her kutuya tam üç robot sürüklesin.", "Her kutu dolduğunda 3, 6, 9, 12 diye ara toplam seslendirilsin.", "Alt bölümde 3 + 3 + 3 + 3 ve 4 grup x 3 robot ifadeleri animasyonla birbirine dönüşsün.", "Bir turda kutu sayısı, diğer turda kutu başına robot sayısı değişsin."],
  ["4 kutuya 3'er robot: 12.", "3 kutuya 5'er pil: 15.", "5 kutuya 2'şer sensör: 10; çocuk eksik bırakılmış kutuyu tamamlar."],
  ["Bir kutuda fazla/eksik robot varsa bant durur ve yalnız o kutu vurgulanır.", "Tüm gruplar eşit olduğunda bant çalışıp toplamı sayar.", "Doğru cevap yalnız çarpım değil, eş grup düzeniyle doğrulanır."],
  ["Her nesne kutu içinde ayrı ayrı görülecek ve sayılabilecek.", "Tekrarlı toplama ile çarpma ifadesi her turda aynı görsel gruplardan üretilecek."]),

G(19, "Tema 3", "Aç Tavşanlar", "Ardışık çıkarmadan bölmeye",
  ["Dört tavşan ve dört boş kutu görülüyor; havuçlar sepette görünmeden Herkese 1 öğe ver düğmesiyle sayaç ilerliyor.", "Başlık ardışık çıkarmadan bölmeye derken mevcut oynanış yalnız eşit paylaştırma yönünü gösteriyor."],
  ["Havuçların gerçekten azalması görünmediği için 20 - 4 - 4 - 4 - 4 - 4 ilişkisi kurulamıyor.", "Tek düğme, paylaştırma kararını çocuğun yerine otomatik yapıyor."],
  ["Ortada 20 gerçek havuçlu sepet ve çevresinde dört tavşan tabağı bulunsun.", "Çocuk bir turda sırayla her tabağa bir havuç sürüklesin; adaletsiz dağıtıma izin verilmesin.", "Her dağıtım turunda sepetten 4 havuç eksilsin ve ardışık çıkarma satırı güncellensin.", "Sepet boşalınca her tavşanın 5 havucu olduğu ve 20 : 4 = 5 ilişkisi gösterilsin."],
  ["20 havuç 4 tavşana: kişi başı 5.", "18 havuç 3 tavşana: kişi başı 6.", "16 havuç 4 tavşana dağıtılır; bir tabaktaki fazla havuç bulunup düzeltilir."],
  ["Bir tavşana arka arkaya iki havuç verilirse Sıradaki tavşanı unutma ipucu gelsin.", "Her tam turda kalan havuç sayısı sesli okunur.", "Bitişte paylaştırma ve ardışık çıkarma aynı ekran üzerinde bağlanır."],
  ["Sepetteki 20 havuç başlangıçtan itibaren görünür olacak.", "Çocuk dağıtımı kendisi yapacak; yalnız otomatik dağıt düğmesi yeterli sayılmayacak."]),

G(20, "Tema 3", "Uzay Lazerleri", "Çarpma ve bölmede zihinden işlem",
  ["Uzay teması başlıkla uyumlu; ancak cevaplar sürekli hareket eden küçük meteorların üzerinde ve uzun süre sabit kalmıyor.", "Beş soru aynı üçlü seçim düzeniyle arka arkaya geliyor; işlem sonucu nesne gruplarıyla doğrulanmıyor."],
  ["Hedef hareketi okuma hızını ve dokunma becerisini matematik başarısına karıştırıyor.", "Yanlış çarpım/bölümün hangi düşünme hatasından geldiği açıklanmıyor."],
  ["Meteorlar belirli atış noktalarında kısa süre sabit dursun; metin en az 44 px dokunma alanında gösterilsin.", "Her işlemden önce kısa dizi/grup modeli isteğe bağlı ipucu olarak açılabilsin.", "Lazer nişanı sürüklenip bırakıldığında seçilen meteora kilitlensin; rastgele kaçan hedef kullanılmasın.", "Çarpma ve bölme soruları ayrı dalga renkleriyle ayrılmalı."],
  ["3 x 5, doğru meteor 15.", "20 : 4, doğru meteor 5; dört eş grup ipucu bulunur.", "5 x 2 ile 2 x 5 aynı sonuç mu? İki dizi yan yana karşılaştırılır."],
  ["Yanlış meteor parçalanmaz; işlem modeli açılıp çocuk yeniden nişan alır.", "Doğru atışta işlem ve sonuç sesli okunur.", "Can sistemi okuma/dokunma hatasında ağır ceza vermemeli; üç denemeden sonra yönlendirici ipucu açılmalı."],
  ["Seçenekler okunabilecek süre boyunca sabit veya tahmin edilebilir hareket edecek.", "Üç turda çarpma, bölme ve değişme özelliği ayrı ayrı ölçülecek."]),

G(21, "Tema 3", "Tahterevalli Dengesi", "Eşitliğin anlamı",
  ["Ekranda iki boş hedef yuvası ve işlem kartları var; gerçek tahterevalli, sol taraftaki 2 x 5 yükü ve denge hareketi görünmüyor.", "Çocuk sonucu 10 olan iki kartı yerleştiriyor ama eşitliğin iki tarafı fiziksel olarak karşılaştırılmıyor."],
  ["Eşittir işareti, denge ilişkisi yerine doğru kutuya iki kart koyma kuralına dönüşüyor.", "Yanlış kartın 12 veya 13 ettiği nesnelerle gösterilmiyor."],
  ["Ortada gerçek tahterevalli; sol kefede 2 sıra 5 blok ve 10 birimlik yük bulunsun.", "Sağ tarafa işlem blokları sürüklendikçe tahterevalli sonuç farkına göre eğilsin.", "İşlem kartına dokununca sonucu nokta/nesne modeliyle açılabilsin.", "Bir turda tek işlem, bir turda iki işlemin toplamı, bir turda eksik değer dengelensin."],
  ["2 x 5 ile 6 + 4 ve 20 : 2 eş sonuçlu olarak seçilir.", "12 - 3 ile 3 x 3 dengelenir.", "7 + ? = 15 için 8 birimlik blok bulunur."],
  ["Yanlış blokta kefe gerçek fark kadar eğilir ve sonuçlar gösterilir.", "Doğru eşitlikte tahta yatay olur, eşittir işareti ortada parlar.", "İki doğru kart gerektiğinde her birinin rolü açıkça belirtilir; yalnız yuva sayısından tahmin edilmez."],
  ["Sol ve sağ miktarlar görünür olacak; boş hedef kutuları tek başına yeterli olmayacak.", "Denge açısı işlem sonuçlarının farkıyla tutarlı çalışacak."]),

G(22, "Tema 4", "X-Ray Dedektifi", "Nesneleri geometrik cisim olarak sınıflandırma",
  ["Cisim çizimleri ve nesne kartları okunaklı; ancak X-Ray tarayıcısı ve hareketli bant hikayesi yalnız yönergede kalıyor.", "Beş nesne tek turda sabit eşleştiriliyor; cisimleri farklı yön ve boyutta tanıma sınanmıyor."],
  ["Çocuk şekli kart üzerindeki hazır çizim/etiketten eşleyebilir, biçimsel özelliği incelemek zorunda kalmaz.", "Aynı nesneler tekrarlandığında cevaplar konumdan ezberlenebilir."],
  ["Nesneler gerçek bant üzerinde gelsin ve X-Ray penceresinde iç cisim modeli dönüşerek görünsün.", "Çocuk tarayıcı kolunu nesnenin üstüne getirip görünümü açtıktan sonra sınıfa sürüklesin.", "Hedef kutuları yazının yanında büyük 3B model gölgesi taşısın.", "Cisimler farklı yönde döndürülse de sınıf değişmediği gösterilsin."],
  ["Çadır, zar, konserve, top ve ayakkabı kutusu sınıflanır.", "Dondurma külahı, pil, hediye kutusu ve portakal eklenir.", "Aynı cisimler döndürülmüş X-Ray görüntülerinden tanınır; etiketler geç açılır."],
  ["Yanlış sınıfta iki model üst üste getirilip biçim farkı gösterilsin.", "Doğru taramada nesnenin adı ve benzediği cisim birlikte okunur.", "İkinci denemede hedef model kısa süre döndürülerek ipucu verir."],
  ["X-Ray ve bant gerçek etkileşim olacak; yalnız sürükle-bırak listesi kalmayacak.", "Üç turda nesne kümesi ve cisim yönleri değişecek."]),

G(23, "Tema 4", "Çılgın Robot Atölyesi", "Cisimlerle yapı oluşturma",
  ["Parça kartları altta, hedefler ise baş, gövde, bacak ve el yazılı satırlar halinde; robotun gövde silueti görünmüyor.", "Geometrik cisimle yapı oluşturma yerine sözel açıklamayı doğru cisim etiketiyle eşleştirme yapılıyor."],
  ["Sentezleme kazanımı, adlandırma/eşleştirme düzeyine düşüyor.", "Parçalar birleşmediği için cismin yapıda nasıl kullanıldığı görülmüyor."],
  ["Ortada bağlantı noktaları olan büyük robot iskeleti çizilsin.", "Küre, küp, silindir ve dikdörtgen prizma modelleri döndürülerek uygun bağlantıya sürüklensin.", "Her parça yerleşince gerçek 3B görünümle robotun parçasına dönüşsün.", "Son turda çocuk verilen parçalardan kendi robotunu kurup hangi cismi nerede kullandığını seçsin."],
  ["Küre baş, dikdörtgen prizma gövde, silindir bacak, küp el olur.", "İki silindir kol ve iki küp ayak eklenen ikinci robot kurulur.", "Serbest tasarımda en az üç farklı cisim kullanılarak çalışan robot oluşturulur."],
  ["Yanlış bağlantıda parça kaybolmaz; hedefin biçimsel ihtiyacı gölgeyle gösterilir.", "Doğru parça yerine kilitlenip robot hareket eder.", "Bitişte kullanılan cisimler robot üzerinde tek tek parlatılır ve adlandırılır."],
  ["Ekranda tamamlanan gerçek bir robot modeli oluşacak.", "Çocuk en az bir turda hazır metin hedefi olmadan yapı kuracak."]),

G(24, "Tema 4", "Sihirli Kilim Dokumacısı", "Şekillerle model oluşturma",
  ["Kilim yerine dört yazılı hedef satırı ve altta şekil kartları var; dokuma deseni veya şekilli boşluk görünmüyor.", "Çocuk Üç kenarlı boşluk gibi metni okuyup şekil adını eşliyor; model oluşturma yapılmıyor."],
  ["Okuma becerisi geometri becerisinin önüne geçiyor.", "Şekilleri birleştirerek yeni motif üretme kazanımı ölçülmüyor."],
  ["Büyük bir Anadolu kilimi ve üzerinde gerçek üçgen, kare, dikdörtgen ve daire biçimli boşluklar çizilsin.", "Şekil parçaları döndürülebilir ve sürüklenebilir olsun; dış sınır yuvayla fiziksel olarak uyuşsun.", "Parçalar birleşince yıldız, çiçek veya baklava motifi oluştursun.", "Bir turda örneği kopyalama, bir turda eksik motifi tamamlama, bir turda serbest simetrik desen kurma yapılsın."],
  ["Dört temel şekil kendi boşluğuna yerleştirilir.", "İki üçgen bir kare motifi oluşturacak biçimde birleştirilir.", "Simetrik kilimin eksik sağ yarısı verilen parçalarla tamamlanır."],
  ["Yanlış şekil yuvaya oturmaz; kenarların uyuşmadığı bölüm parlasın.", "Doğru parça dokuma efektiyle kilime dönüşsün.", "Tur sonunda kullanılan şekiller metin yerine motif üzerinde işaretlenerek sayılır."],
  ["Kilim gerçek yerleştirme yüzeyi olacak; yazılı hedef listesi ana oyun olmayacak.", "En az bir turda iki şekil birleşerek yeni bir model oluşturacak."]),

G(25, "Tema 4", "Uzaylıların Şekil Kapıları", "Dönse de büyüse de aynı şekil",
  ["Döndürülmüş şekiller çiziliyor ve konu kısmen görünür; ancak kapı/kalkan yerine uzay lazeri şablonundaki hareketli kaya seçenekleri kullanılıyor.", "Şekil kimliği çoğunlukla üç isimden seçimle ölçülüyor; çocuğun eş şekilleri karşılaştırması sınırlı."],
  ["Hareketli kayalar dokunmayı zorlaştırıyor ve kapı hikayesini zayıflatıyor.", "Yalnız ad seçimi, yön ve büyüklük değişimine rağmen özelliklerin korunmasını açıklatmıyor."],
  ["Üç uzay kapısı gerçek üçgen, kare ve dikdörtgen dış sınırına sahip olsun.", "Dönen meteor şekli doğru kapının boşluğuna sürüklensin; boyutu kapıya yaklaşırken ölçeklensin.", "Aynı şeklin farklı yön/boyut örnekleri yan yana üst üste getirilerek eşlik gösterilsin.", "Son turda çocuk hangi özelliklerin değiştiğini seçsin: yön, büyüklük; hangi özelliğin değişmediğini belirlesin: şekil türü."],
  ["145 derece dönmüş üçgen, üçgen kapısından geçer.", "Küçük ve dönmüş kare, kare kapısından geçer.", "Yan yatmış dikdörtgen ve büyük ters üçgen iki ardışık kapıda sınıflanır."],
  ["Yanlış kapıda meteor çarpıp kaybolmaz; dış sınırlar üst üste gösterilir.", "Doğru kapıda şekil dönüp kapıyla hizalanır.", "Seçenekler sabit kapılar olacak; uzayda kaçan kaya kullanılmayacak."],
  ["Kapı sınırı ile şekil sınırı matematiksel olarak aynı türü temsil edecek.", "Her turda en az bir yön ve bir büyüklük değişimi bulunacak."]),

G(26, "Tema 4", "Limonata Festivali", "Sıvı miktarını tahmin etme",
  ["Sürahi, bardak ve limonata yerine boş pano ile 4, 8, 15 bardak seçenekleri görülüyor.", "8 bardak sonucu seçilince gerçek doldurma ve taşma gözlenmeden cevap açılıyor."],
  ["Kapasite tahmini görsel büyüklük karşılaştırması olmadan rastgele seçime dönüşüyor.", "Standart olmayan ölçü biriminin tekrar tekrar kullanılması deneyimlenmiyor."],
  ["Şeffaf büyük sürahi, dolu limonata kabı ve aynı boy sekiz su bardağı çizilsin.", "Çocuk önce tahmin işaretini koysun, sonra bardakları tek tek sürahiye döksün.", "Sıvı seviyesi her bardakta eşit miktarda yükselsin; sekizinci bardakta tam dolsun.", "Farklı boy bardak kullanıldığında gereken sefer sayısının değiştiği ayrı tur eklensin."],
  ["Büyük sürahi 8 aynı bardakla doldurulur.", "Küçük şişe 4 bardakla doldurulur.", "Aynı sürahi küçük bardakla 12, büyük bardakla 6 seferde dolar; sonuçlar karşılaştırılır."],
  ["Yanlış tahminde hemen cevap verilmez; ölçüm tamamlanınca tahmin çizgisi gerçek sonucun yanında kalır.", "Taşma olursa son bardak geri alınabilir.", "Doğru ölçümde bardak sayısı ve sıvı seviyesi birlikte okunur."],
  ["Sıvı seviyesi fiziksel olarak artacak; boş pano kabul edilmeyecek.", "Kap ve ölçü aracı boyutlarıyla sefer sayıları tutarlı olacak."]),

G(27, "Tema 4", "Geometri İkizleri", "Nesne ve cisim eşleştirme",
  ["Hafıza kartı düzeni konuya uygun ve kartlar ters duruyor; ancak yalnız dört sabit çift kullanılıyor.", "Kartların arka yüzü birbirine çok benzer; eşleşme bulunduğunda nesne-cisim ilişkisini açıklayan kısa karşılaştırma sınırlı."],
  ["Aynı kart yerleri tekrarlandığında hafıza ezberi geometri bilgisinin önüne geçebilir.", "Yön değişimi kazanımı yalnız ipucu metninde kalabilir."],
  ["Her yeni turda kartların konumu, cisim çiziminin yönü ve nesne örnekleri değişsin.", "Çift açıldığında nesne ve 3B model ortada büyütülüp benzer dış biçimleri işaretlensin.", "Yanlış çifte iki saniye inceleme süresi verilsin; hemen kapanmasın.", "Son turda bir cisim için iki günlük nesne arasında doğru eşi seçme görevi eklensin."],
  ["Zar-küp, top-küre, konserve-silindir, çadır-üçgen prizma.", "Hediye kutusu-küp, portakal-küre, pil-silindir, ayakkabı kutusu-dikdörtgen prizma.", "Döndürülmüş cisim kartları ve yeni nesnelerle altı çiftlik hafıza turu."],
  ["Yanlış çiftte adlar okunmaz; çocuk biçimleri inceleyebilir.", "Doğru çifte Bu nesne ... cismine benzer denir ve benzer sınır çizgisi parlar.", "Bütün çiftler bitince cisimler ayrı bir sınıflama panosunda toplanır."],
  ["Kart dağılımı her açılışta değişecek.", "En az iki turda aynı cisim farklı nesne ve farklı yönle temsil edilecek."]),

G(28, "Tema 4", "Hangi Kova Daha Hızlı?", "Kapasite karşılaştırma",
  ["Havuz ve kaplar yerine uzay gemisi ile hareketli kaya seçenekleri var; kap adları metin olarak kayaların üstünde.", "En büyük kabın daha az sefer gerektirdiği gerçek doldurma ile gösterilmiyor."],
  ["Kapasite, nesnelerin fiziksel büyüklüğü görülmeden yalnız sözcük bilgisinden cevaplanıyor.", "Hareketli uzun seçenekler küçük ekranda okunması zor hedeflere dönüşüyor."],
  ["Aynı küçük havuz ve yanında çay bardağı, kepçe, yoğurt kabı gerçek boy oranlarıyla çizilsin.", "Çocuk bir kap seçip havuzu doldursun; her dökmede sefer sayacı artsın.", "Kap büyüdükçe aynı su miktarının daha az seferde taşındığı iki animasyon yan yana karşılaştırılsın.", "Son turda kapların adları kaldırılıp yalnız görsel kapasiteye göre sıralama yaptırılsın."],
  ["En büyük yoğurt kabıyla en hızlı doldurma seçilir.", "En küçük çay bardağıyla en çok sefer gerektiği deneyimlenir.", "Dört kap küçükten büyüğe sıralanır ve sefer sayıları tahmin edilir."],
  ["Yanlış tahminde gerçek doldurma durdurulmaz; sonuç gözlenip seçim yeniden yapılır.", "Doğru karşılaştırmada kap büyüklüğü ve sefer sayısı ters yönlü oklarla gösterilir.", "Uzay lazeri/kaya şablonu tamamen kaldırılır."],
  ["Kapların görsel hacimleri belirgin biçimde farklı olacak.", "Karşılaştırma en az iki gerçek doldurma deneyiyle kanıtlanacak."]),

G(29, "Tema 5", "Korsan Haritası", "Yön bloklarıyla rota kurma",
  ["Izgara, engeller ve yön düğmeleri işlevsel; ancak başlatıcı korsan yerine küçük bayrak simgesi gibi görünüyor ve dağ engeli yönergede geçmesine rağmen yalnız timsah var.", "Tek sabit rota ve güçlü ipucu, çocuğun plan kurmadan yolu ezberlemesine izin veriyor."],
  ["Yön kavramı çalışsa da rota karşılaştırma ve en güvenli yol ölçütü yalnız bir haritada kalıyor.", "Program satırındaki oklar küçükse hata ayıklama zorlaşabilir."],
  ["Korsan karakteri yönü belli bir figür olarak çizilsin; baktığı yön her adımda dönsün.", "Yön blokları program şeridine sürüklenip numaralansın; çalıştırmada aktif blok parlasın.", "Timsah, dağ ve bataklık gibi engeller farklı hareket kısıtlarıyla gösterilsin.", "Başarısız rotadan sonra program korunup yalnız yanlış adımdan itibaren düzenlenebilsin."],
  ["4x4 haritada timsahlardan kaçıp hazineye ulaş.", "5x4 haritada iki güvenli yol arasından daha kısa olanı seç.", "Sisli haritada bir engel sonradan açılır; programı bir blok değiştirerek düzelt."],
  ["Engele çarpınca hangi program bloğunda hata olduğu kırmızı çerçevelensin.", "Hedefe ulaşamayan ama güvenli rotada Eksik iki adım var gibi geri bildirim verilsin.", "Doğru rotada korsan her adımı ok yönüyle ve sesle uygulasın."],
  ["Korsanın ekran konumu ve program sonucu her adımda birebir uyacak.", "En az üç farklı harita ve değişen başlangıç/hedef konumu bulunacak."]),

G(30, "Tema 5", "Robot Kargo Teslimatı", "Ölçüt değişince planı yenileme",
  ["Izgara ve iki tur yapısı konuya yakın; ancak yönerge en kısa rotayı çiz diyor, gerçek etkileşim ok düğmeleriyle program kurmak.", "İkinci turda alt yolun kapanması iyi fikir olsa da ilk rotanın kopyası ve değişen bölüm görsel olarak karşılaştırılmıyor."],
  ["Çocuk yeniden planlama yerine her tur programı baştan kurup ezberleyebilir.", "Çizmek ile ok eklemek arasındaki yönerge çelişkisi gereksiz hata yaratır."],
  ["Yönerge Ok bloklarıyla en kısa rotayı kur olarak düzeltilsin veya parmakla yol çizme gerçekten uygulansın.", "İlk plan ikinci tura soluk kopya olarak taşınsın; yeni engel geldiğinde yalnız değişen bölüm düzenlensin.", "Adım sayacı iki rotanın uzunluğunu karşılaştırsın.", "Kargo dronu evde paketi gerçekten bırakıp dönüş rotasını da kısa bir görevde planlasın."],
  ["İlk yol çalışmasında alt sıradan en kısa rota kurulur.", "Alt yol kapanınca üst sıradan yeni rota kurulur; eski ve yeni plan karşılaştırılır.", "Hedef ev değişir ve çocuk iki geçerli rotadan daha kısa olanı seçer."],
  ["Kapalı hücreye giden blok programda işaretlenir; tüm program silinmez.", "Doğru ama daha uzun rotada Hedefe ulaştın; daha kısa yol bulabilir misin? denir.", "En kısa rotada adım sayısı ve değiştirilen blok sayısı özetlenir."],
  ["Yönerge ile gerçek girdi yöntemi aynı olacak.", "İkinci görev, ilk planın değişen koşula göre revizyonunu açıkça gösterecek."]),

G(31, "Tema 5", "Sihirli Ayna Gölü", "Simetrik eşi bulma",
  ["Bayrak ve üçgen çizimleri mevcut; ancak göl, su yüzeyi ve ayna çizgisi yerine uzay sahnesi ile hareketli kaya seçenekleri görülüyor.", "Simetri ekseni küçük bir noktalı işaret gibi kalıyor; yansımanın hangi eksene göre alındığı açık değil."],
  ["Çocuk şeklin aynalanmasını değil benzer seçenekler arasındaki görsel tahmini yapabilir.", "Hareketli seçenekler ayrıntılı yön karşılaştırmasını zorlaştırıyor."],
  ["Ekranın ortasında yatay su çizgisi veya dikey ayna ekseni açıkça çizilsin.", "Kaynak şekil eksene yaklaşınca yansıma adım adım oluşsun; eş noktalar ince çizgilerle bağlansın.", "Seçenekler su altındaki sabit üç gölge olarak dursun.", "Bir tur yatay, bir tur dikey eksen; bir tur eksik yarıyı sürükleyerek tamamlama yapılsın."],
  ["Bayrağın dikey aynadaki yansıması seçilir.", "Üçgenin su yüzeyine göre yatay yansıması seçilir.", "Kelebeğin eksik yarısı sürüklenerek eksene eş uzaklıkta tamamlanır."],
  ["Yanlış seçimde kaynak ve seçenek üst üste getirilip uyuşmayan yön gösterilir.", "Doğru seçim su dalgasıyla birleşir ve eş noktalar parlar.", "Seçenekler hareket etmeyecek; uzay gemisi/kaya kullanılmayacak."],
  ["Simetri ekseni bütün tur boyunca görünür ve yönü açık olacak.", "Yansıyan parçaların eksene uzaklıkları eşit olacak."]),

G(32, "Tema 5", "İp Baskısı Laboratuvarı", "Katlama ve simetri ekseni",
  ["Yarım kalp ve katlama çizgisi konuya uygun; ancak mevcut görev yalnız Kalp/Yıldız/Üçgen seçimi, çocuğun katlama veya baskı yapmasını gerektirmiyor.", "Tek kalp örneği tekrarlandığında simetri işlemi yerine şekil tanıma ölçülüyor."],
  ["Katlama yoluyla simetri oluşturma kazanımı pasif tahmine indirgeniyor.", "Eksenin iki tarafındaki eş uzaklık ve karşılık ilişkisi uygulanmıyor."],
  ["Çocuk ekranı katlama çizgisinden parmağıyla sürükleyerek kapatsın; açınca boya baskısı karşı tarafa geçsin.", "Baskı öncesi sonucu tahmin etsin, baskı sonrası iki yarıyı üst üste kontrol etsin.", "Nokta ve çizgiler eksene olan uzaklıklarına göre karşı tarafa yansısın.", "Kalp dışında kelebek ve yaprak yarımları da kullanılsın."],
  ["Yarım kalp katlanıp tam kalp oluşturur.", "Yarım kelebek baskıyla tamamlanır.", "Üç renkli nokta eksenin karşısına eş uzaklıkta basılır; çocuk hatalı noktayı düzeltir."],
  ["Yanlış tahminde doğru şekil söylenmez; yarımın dış sınırı izlettirilir.", "Doğru katlamada iki yarı üst üste getirerek eşlik kanıtlanır.", "Bitişte simetri ekseni ve eş nokta çiftleri kısa süre görünür kalır."],
  ["En az bir turda gerçek katlama/baskı hareketi yapılacak.", "Yansıyan noktalar eksene eş uzaklıkta hesaplanacak."]),

G(33, "Tema 5", "Uzaylı Gezgini", "Yer, yön ve konum sözcükleri",
  ["Kaya-araç-üs ilişkisi çoğunlukla metin ve emoji satırında anlatılıyor; seçenekler uzaydaki hareketli kayalar üzerinde.", "Araç ve üs gerçek bir haritada konum değiştirmediği için önünde, arkasında, sağında ve arasında kavramları gözlenmiyor."],
  ["Dilsel okuma, uzamsal ilişki kurmanın önüne geçiyor.", "Bakış yönü değiştiğinde sağ-sol/ön-arka ilişkisinin değişmesi denenmiyor."],
  ["Kareli uzay haritasında kaya, araç, üs ve kraterler gerçek konumlarda çizilsin.", "Araç okla baktığı yönü göstersin; çocuk yönergeye göre aracı sürüklesin veya yön düğmesine bassın.", "Her hareketten sonra konum cümlesi çocuk tarafından seçeneklerden tamamlanır.", "Bakış yönü değiştiğinde aynı nesnenin sağ/sol durumunun nasıl değiştiği animasyonla gösterilsin."],
  ["Araç kaya ile üs arasındaki kareye yerleştirilir.", "Araç kayaya bakarken kaya önünde olacak konuma döndürülür.", "Kraterin sağından geçip arkasındaki üsse ulaşan üç adımlı rota uygulanır."],
  ["Yanlış konumda doğru yer doğrudan parlamaz; referans nesne ve bakış oku vurgulanır.", "Doğru konumda cümle sesli tamamlanır.", "Hareketli meteor cevapları kaldırılıp sabit harita kullanılmalı."],
  ["Konum sözcükleri ekrandaki gerçek nesne ilişkisiyle birebir uyuşacak.", "Üç turda referans nesne ve aracın bakış yönü değişecek."]),

G(34, "Tema 5", "Geometri Terzisi", "Harflerde simetri",
  ["Harfler su altı sahnesinde hareket eden kartlara dönüşmüş; terzi, kumaş ve katlama çizgisi görünmüyor.", "A, H, M, T seçimi kullanılan yazı tipine bağlı; dikey eksen çizilmediği için simetri koşulu belirsiz kalıyor."],
  ["Çocuk harfin simetrisini incelemek yerine kepçeyle hareketli harf yakalıyor.", "Farklı fontlarda M veya T'nin simetrisi değişebileceğinden çizim standardı olmadan cevap tartışmalı olabilir."],
  ["Kumaş üzerinde standart blok harfler ve her harfin ortasında kesikli dikey katlama çizgisi bulunsun.", "Çocuk harfi çizgiden katlayıp iki yarının üst üste gelip gelmediğini gözlesin.", "Simetrik harfler kumaşa kesilip dikilsin; simetrik olmayanlarda uyuşmayan bölüm renkli kalsın.", "Kullanılan harf çizimleri uygulamaya gömülü vektörler olsun; sistem fontuna bağlı kalmasın."],
  ["A, H ve T dikey eksene göre incelenir.", "M, P ve S aynı yöntemle karşılaştırılır.", "Çocuk verilen altı harfe eksen çizer; dikey/yatay simetriyi ayrı sınıflar."],
  ["Yanlış seçimde harf katlanıp uyuşmayan kenarlar gösterilir.", "Doğru seçimde iki yarı üst üste oturur ve dikiş animasyonu oynar.", "Su altı kepçesi ve hareketli kartlar kaldırılır."],
  ["Harf geometrileri sabit vektör çizimler olacak.", "Her doğru karar gerçek katlama üst üste bindirmesiyle kanıtlanacak."]),

G(35, "Tema 5", "Kayıp Oyuncaklar Labirenti", "Ölçüte göre en uygun yolu seçme",
  ["Labirent, yatak ve oyuncak araba görünmüyor; A-B-C yol açıklamaları uzay kayaları üzerinde hareket ediyor.", "En güvenli yol ve en kısa yol karşılaştırması gerçek rota uzunluğu/engel yerleşimi olmadan metinden cevaplanıyor."],
  ["Mantıksal yol seçimi, doğru cümleyi bulma sorusuna indirgeniyor.", "Çocuk ölçüt değiştiğinde aynı haritayı yeniden değerlendirmiyor."],
  ["Oda içinde yatak, oyuncak araba ve üç çizilmiş rota bulunsun; su ve lego engelleri gerçek yol üzerinde görülsün.", "Çocuk önce ölçüt kartını seçsin: en güvenli, en kısa veya en az dönüşlü.", "Rotaya dokununca araba yolu gerçekten izlesin ve engelde dursun.", "Ölçüt değiştiğinde aynı harita korunup en uygun rota yeniden seçilsin."],
  ["En güvenli ölçütünde engelsiz uzun C yolu seçilir.", "En kısa ölçütünde engeli kaldırılmış A ve C yolları yeniden karşılaştırılır.", "Yeni oyuncak engeli geldiğinde rota planı değiştirilir ve gerekçe seçilir."],
  ["Yanlış rotada araba engelin yanında durur; neden uygun olmadığı görünür.", "Doğru seçimde ölçüt ile rota özelliği yan yana vurgulanır.", "Hareketli uzay seçenekleri yerine sabit labirent kullanılmalı."],
  ["Her rota uzunluğu ve engel durumu ekrandan ölçülebilecek.", "Aynı haritada en az iki farklı ölçütle farklı doğru cevap oluşacak."]),

G(36, "Tema 6", "Soru Dedektifi", "Araştırma sorusu belirleme",
  ["Araştırma ve sıradan soru dosyaları işlevsel; ancak soru kartları küçük, metinler sıkışık ve dedektif sahnesi yok.", "Görev yalnız hazır soruları sınıflıyor; çocuğun kendi araştırma sorusunu oluşturması veya kapsamını belirlemesi istenmiyor."],
  ["Okunabilirlik sorunu veri okuryazarlığı performansını etkileyebilir.", "Hazır etiket sınıflaması araştırma sorusu üretme kazanımını eksik bırakıyor."],
  ["Dedektif masasında büyüteç, iki dosya ve büyük soru kartları çizilsin.", "Kart büyütece getirildiğinde kimden veri toplanacağı ve birden fazla cevap ihtimali görsel ipuçlarıyla açılsın.", "İkinci turda çocuk konu, grup ve seçenek kartlarını birleştirerek kendi araştırma sorusunu kursun.", "Sorunun araştırılabilirliği için veri toplanabilir mi ve farklı cevap olabilir mi kontrolü yaptırılsın."],
  ["En sevilen mevsim ve renk araştırma sorusu olarak ayrılır.", "Bir haftada kaç gün var gibi tek bilgi cevabı sıradan soruya ayrılır.", "Konu: oyun; grup: sınıfımız; soru: Sınıfımızın en sevdiği oyun hangisidir? biçiminde kurulur."],
  ["Yanlış dosyada kart geri döner ve Birden fazla kişiden farklı cevap gelir mi? ipucu verilir.", "Doğru sınıflamada neden kısa cümleyle açıklanır.", "Kart yazıları küçük ekranda iki satırı geçmeyecek büyüklükte olmalı."],
  ["Araştırma sorusu ölçütleri yalnız renk koduyla değil sözlü gerekçeyle doğrulanacak.", "En az bir turda çocuk hazır seçenekleri birleştirerek yeni soru oluşturacak."]),

G(37, "Tema 6", "Mevsimler ve Çetele", "Veri toplayıp çetele tutma",
  ["İki sütunlu çetele ekranı ve tek tek gelen yanıtlar konuya uygun; ancak yalnız Yaz/Kış kategorileri ve sekiz sabit yanıt var.", "Çetele çizgisini atma eylemi sütuna dokunmaya dayanıyor; beşinci çizginin dört çizgiyi keserek grup oluşturması başlangıçta açıklanmıyor."],
  ["İki kategori veriyi sınırlıyor ve gerçek veri toplama kararı çocuğa bırakılmıyor.", "Beşli çetele yapısı yanlış çizilirse düzeltme/geri alma olanağı gerekli."],
  ["Her öğrenci karakteri konuşsun; çocuk yanıtı dinleyip doğru sütuna çetele çizgisi çeksin.", "Beşinci işaret otomatik çapraz çizgi olarak değil, çocuğun dört çizgiyi gruplayacağı kısa animasyonla gösterilsin.", "Geri al düğmesi ve sayım aşaması eklensin.", "Son turda üçüncü mevsim kategorisi ve boş/geçersiz yanıt bulunabilsin."],
  ["Yaz 5, Kış 3 yanıtı çeteleye işlenir.", "İlkbahar, Yaz, Kış üç sütununda 10 yanıt toplanır.", "Çetele tamamlandıktan sonra sıklık sayıları yazılır ve en çok/en az sorulur."],
  ["Yanlış sütunda karakter yanıtını tekrar eder; can eksilmeden düzeltme yapılır.", "Her beşli grup oluştuğunda Beş oldu diye seslendirilir.", "Bitişte çetele ve sayısal sıklık yan yana gösterilir."],
  ["Beşinci çetele işareti standart biçimde dört çizgiyi kesecek.", "Yanıt sayısı ile her sütundaki çetele toplamı birebir eşleşecek."]),

G(38, "Tema 6", "Uzaylı Meyve Hasadı", "Çeteleden sıklık tablosuna",
  ["Çetele çizimleri ve sayı kartları okunaklı; ancak uzaylı, hasat ve meyve kasaları görünmüyor.", "Çocuk yalnız 7, 4 ve 6 sayılarını boş kutulara sürüklüyor; çeteleyi nasıl saydığı veya beşli grubu kullandığı görünmüyor."],
  ["Görev doğru sayı eşleştirmeye dönüşebilir; çetele okuma stratejisi ölçülmez.", "Tek tablo tekrarlandığında sayı-konum eşleşmesi ezberlenebilir."],
  ["Uzay serasında üç renk meyve kasası ve her kasanın yanında çetele etiketi bulunsun.", "Çocuk önce çeteleyi beşli grup + kalan biçiminde dokunarak sayıp sonra sıklık kartını yerleştirsin.", "Doğru sayı gelince o kadar meyve kasaya animasyonla düşsün.", "Son turda çetelelerden biri eksik/yanlış çizilmiş olsun; çocuk önce düzeltip sonra sıklığa aktarsın."],
  ["Kırmızı 7, mavi 4, yeşil 6 sıklıkları yazılır.", "Yeni hasatta sarı 9, mor 5, mavi 3 aktarılır.", "Bir yanlış çetele düzeltilir; toplam meyve sayısı da bulunur."],
  ["Yanlış sayıda beşli grup ve kalan farklı renklerle ayrılır.", "Doğru aktarımda çetele, rakam ve gerçek meyve sayısı aynı anda görünür.", "Uzaylı şef doğru tablo tamamlanınca kasaları toplar."],
  ["Çetele sayma adımı görünür ve etkileşimli olacak.", "Her satırdaki çetele, sıklık sayısı ve meyve adedi aynı olacak."]),

G(39, "Tema 6", "Şekil Fabrikası", "Nesne grafiğinden şekil grafiğine",
  ["Grafik sütunları ve blok deposu işlevsel; ancak fabrika bandı/üretim süreci yok ve bloklar altta karışık yığın halinde.", "Kaynak satırda elma, armut ve muzlar hem simge hem parantez içi sayı ile veriliyor; çocuk nesneleri saymadan hazır sayıyı okuyabilir."],
  ["Nesne grafiğinden şekil grafiğine dönüşüm yerine verilen sayıyı sütuna doldurma yapılabilir.", "Her kategori farklı şekil kullanırken açık bir gösterge anahtarı yoksa grafik yorumlama karışabilir."],
  ["Fabrika bandında gerçek meyveler tek tek gelsin; çocuk her meyveyi makineye atınca karşılık gelen grafik bloğu üretilsin.", "İlk turda sayılar parantez içinde yazılmasın; çocuk nesne grafiğini sayarak aktarsın.", "Grafik anahtarı açıkça Her şekil 1 meyveyi gösterir desin.", "Bloklar sütuna sürüklenince hizalı hücreye otursun; fazla blok kabul edilmesin."],
  ["5 elma, 3 armut, 4 muz şekil grafiğine aktarılır.", "6 top, 2 kitap, 5 kalem yeni grafikte gösterilir.", "Her şekil 2 nesne kuralıyla 8, 6, 4 verileri yarı sayıda blokla gösterilir."],
  ["Eksik/fazla blokta kaynak nesnelerle sütun yan yana sayılır.", "Doğru sütun tamamlanınca fabrika makinesi ilgili etiketi basar.", "Grafik bitince kategori toplamları ve anahtar birlikte okunur."],
  ["Kaynak veri ilk turda hazır sayıyı vermeyecek; çocuk nesneleri sayacak.", "Grafik anahtarı ile blok sayısı bütün turlarda matematiksel olarak tutarlı olacak."]),

G(40, "Tema 6", "Canavar Kafeteryası", "Grafiği yorumlama",
  ["Bu oyun diğerlerinden farklı olarak açık renkli ve okunaklı bir grafik gösteriyor; ancak kafeterya, canavar müşteriler ve pişirme kararı yalnız başlıkta kalıyor.", "Dört soru tek sabit 4 dondurma-2 pasta grafiğine dayanıyor; kategori sayısı ve ölçek değişmiyor."],
  ["Çocuk aynı iki sayıyı kullanarak cevapları ezberleyebilir.", "Grafiği karar vermek için kullanma, yalnız çok-az-fark-toplam sorularına indirgeniyor."],
  ["Kafeterya tezgahında canavar siparişleri geldikçe grafik canlı güncellensin.", "Çocuk grafiği okuyup hangi tatlıdan kaç tane hazırlanacağını mutfak tepsisine sürüklesin.", "Grafik anahtarı ve kategori sayısı sonraki turlarda değişsin.", "Karar sonrasında hazırlanan miktar grafikle karşılaştırılsın; fazla/israf ve eksik sipariş görünür olsun."],
  ["4 dondurma, 2 pasta grafiğinde az-çok-fark-toplam bulunur.", "5 meyve suyu, 3 süt, 4 su grafiğine göre hazırlık yapılır.", "Her şekil 2 siparişi gösterir kuralıyla toplam ve fark yorumlanır."],
  ["Yanlış cevapta ilgili iki sütun çizgiyle hizalanıp fark görünür kılınsın.", "Doğru kararda mutfak gerçekten gereken sayıda ürün üretir.", "Tur sonunda Grafikten karar verdim cümlesi somut hazırlık sonucu ile bağlanır."],
  ["Her turda grafik verisi ve kategori düzeni değişecek.", "Sorular yalnız sayı seçimi değil, grafiğe dayalı gerçek hazırlık kararı da içerecek."]),

G(41, "Tema 6", "Zaman Yolcusu", "Veriler değişir mi?",
  ["Sınıflar ve zaman yolculuğu yerine uzay lazeri sahnesinde hareketli kaya seçenekleri görülüyor.", "2/A ve 2/B sonuçları yalnız cümleyle veriliyor; iki ayrı grafik yan yana gösterilmiyor."],
  ["Çocuk veri gruplarını karşılaştırmadan doğru ifadeyi metinden seçebilir.", "Kişi ve zaman değişkenlerinin veri üzerindeki etkisi görsel olarak ayırt edilmiyor."],
  ["Zaman kapısının iki yanında 2/A ve 2/B sınıfına ait gerçek grafikler gösterilsin.", "Çocuk aynı sorunun farklı gruplardaki sütunlarını renkli bağlarla karşılaştırsın.", "Bir yıl ileri kapısı açıldığında aynı sınıfın yeni grafiği eski grafiğin üstüne saydam olarak bindirilsin.", "Değişen veri kaynağı kartla belirtilsin: kişiler değişti, zaman değişti veya soru değişti."],
  ["2/A futbol, 2/B basketbol birinci; kişi grubu değişince sonuç farklıdır.", "Aynı sınıfta bir yıl sonra ilgi değişimi iki grafikle karşılaştırılır.", "Soru değiştiğinde eski ve yeni sonuçların doğrudan karşılaştırılamayacağı belirlenir."],
  ["Yanlış seçimde iki grafikte farklı olan sütunlar vurgulanır.", "Doğru cevapta değişimin nedeni kişi/zaman/soru kartıyla eşleştirilir.", "Uzay kayaları üzerinde uzun metinler kullanılmaz; seçenekler sabit panelde durur."],
  ["Her karşılaştırmada iki gerçek veri gösterimi aynı anda görülecek.", "Sonucun neden değiştiği veri kaynağındaki değişkenle tutarlı olacak."]),

G(42, "Tema 6", "Veri Laboratuvarı", "Kendi araştırmanı grafikle",
  ["Grafik oluşturma alanı çalışıyor; ancak kendi araştırmanı ifadesine rağmen soru ve veri hazır veriliyor: köpek 6, kedi 4, tavşan 2.", "Kaynakta sayılar yazılı olduğu için çocuk çeteleyi okuyup dönüştürmek yerine yalnız belirtilen kadar blok yerleştiriyor."],
  ["Tam veri döngüsü soru-veri-çetele-grafik aşamalarını çocuğa kurdurmuyor.", "Tek hazır veri seti, araştırma planı ve yorumlama becerisini ölçmüyor."],
  ["Çocuk önce üç araştırma sorusundan birini seçsin veya konu kartlarıyla soru kursun.", "Sanal sınıftaki karakterlerden yanıt toplayıp çetele tablosuna kendisi işlesin.", "Çetele sıklığa, sıklık da şekil grafiğine adım adım dönüştürülsün; önceki aşama ekranda referans olarak kalsın.", "Grafik bitince en çok, en az, fark ve sonuç değişebilir mi sorularıyla rapor tamamlanmalı."],
  ["Hazır evcil hayvan verisiyle çetele-grafik dönüşümü öğrenilir.", "Sevilen oyun araştırmasında 10 karakterden veri toplanır ve grafik kurulur.", "Çocuk seçtiği araştırma sorusunu, grafiğini ve iki cümlelik yorumunu tamamlar."],
  ["Yanlış blokta ilgili çetele satırı vurgulanır; sayı doğrudan söylenmez.", "Her aşama tamamlanınca veri kaybı olup olmadığı toplamlarla kontrol edilir.", "Bitişte soru, katılımcı sayısı, grafik ve sonuç tek rapor kartında sunulur."],
  ["Son tur gerçekten çocuk tarafından seçilen/kurulan bir araştırma sorusuna dayanacak.", "Yanıt sayısı, çetele toplamı, sıklık ve grafik blokları birebir eşleşecek."])
]


THEMES = {
    "Tema 1": ("Sayılar ve Nicelikler - Sayı temsili, sıralama, örüntü ve tahmin", CORAL,
               ["Hareketli kart yakalama yerine sayının yapısını gösteren sabit ve sayılabilir nesneler kullanılmalı.", "Her oyunda tek sabit örnek yerine üç değişen tur bulunmalı.", "Başlıkta anlatılan canavar, tren, kurbağa, pasta, balon veya hayvanat bahçesi gerçek sahnede görünmeli."]),
    "Tema 2": ("Kesirler, para, zaman ve ölçme", GOLD,
               ["Tahmin oyunları boş pano üzerinde seçenek sunmamalı; gözlenecek nesne ve ölçme eylemi görünmeli.", "Para, saat ve kesir oyunlarında butona basma yerine nesneyi sürükleme, kesme, ölçme ve karşılaştırma yaptırılmalı.", "Yönerge ile gerçek girdi yöntemi aynı olmalı."]),
    "Tema 3": ("İşlemlerden Cebirsel Düşünmeye", PURPLE,
               ["Fırın ve asansör gibi günlük hikayeler uzay lazeri şablonuna dönüştürülmemeli.", "Her işlem gerçek nesne değişimi veya eş grup modeliyle kurulmalı.", "Yanlış cevapta yalnız can eksiltmek yerine düşünme hatasının kaynağı gösterilmeli."]),
    "Tema 4": ("Nesnelerin Geometrisi - Cisimler, şekiller ve kapasite", TEAL,
               ["Model oluşturma oyunları yazılı eşleştirmede kalmamalı; robot ve kilim gerçekten oluşmalı.", "Kapasite oyunlarında gerçek kap, sıvı seviyesi ve tekrar sayısı görülmeli.", "Şekil ve cisimler farklı yön/boyutlarda yeniden test edilmeli."]),
    "Tema 5": ("Yer, yön, konum ve simetri", BLUE,
               ["Rota oyunlarında program, harita ve karakter hareketi adım adım eşleşmeli.", "Simetri ekseni sürekli görünür olmalı ve eş noktalar eksene eş uzaklıkta kurulmalı.", "Metin seçenekleri yerine gerçek labirent, ayna, göl, kumaş ve uzay haritası kullanılmalı."]),
    "Tema 6": ("Veriye Dayalı Araştırma", CORAL,
               ["Veri döngüsü soru kurma, veri toplama, çetele, sıklık, grafik ve yorum aşamalarının tamamını içermeli.", "Grafik anahtarı ve toplamlar her aşamada tutarlı olmalı.", "Hazır sayıları kopyalamak yerine nesneleri/çeteleyi sayma ve gerçek karar verme yaptırılmalı."])
}


doc = BaseDocTemplate(str(OUT), pagesize=A4, rightMargin=MX, leftMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
                      title="2. Sınıf Matematik Oyunları - Ayrıntılı Düzeltmeler",
                      author="Macera Akademi oyun incelemesi")
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

story = []
story += [Spacer(1, 16 * mm), P("MACERA AKADEMİ", cover_kicker),
          P("2. Sınıf Matematik Oyunları<br/>Ayrıntılı Düzeltmeler", cover_title),
          P("42 oyunun gerçek ekranları açılarak, kullanılan oyun motorları denenerek ve kaynak tanımlarıyla karşılaştırılarak hazırlanmıştır.", cover_sub)]
cover_box = Table([[P("<b>Kapsam</b><br/>Bu belge 2. sınıf matematik listesindeki v01-v42 oyunlarının tamamını kapsar. Her oyun için gözlenen mevcut sorun, eğitimsel risk, yeni sahne ve oynanış, üç farklı tur, geri bildirim akışı ve kabul ölçütü verilir.")]], colWidths=[153 * mm])
cover_box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL), ("BOX", (0, 0), (-1, -1), 0.7, TEAL),
                                ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                                ("TOPPADDING", (0, 0), (-1, -1), 13), ("BOTTOMPADDING", (0, 0), (-1, -1), 13)]))
story += [cover_box, Spacer(1, 9 * mm), P("Hazırlama yaklaşımı", h2)]
story += bullets(["42 oyunun tamamı listeden tek tek açıldı ve ilk sahneleri görsel olarak kontrol edildi.",
                  "TapSelect, ChoiceQuestion, DragMatch, OrderSequence, EstimateReveal, MoneyBuild, ClockSet, FractionCut, CodeGrid, GraphBuild ve diğer kullanılan motorlar karşılaştırıldı.",
                  "Doğru/yanlış akışının örnekleri oynandı; özellikle hareketli hedef, cevap açıklama, yönerge-etkileşim uyumu ve görünür nesne kullanımı incelendi."])
story += [PageBreak()]

story += [P("Testten çıkan öncelikli bulgular", h1)]
story += [box("1. Hikaye-sahne uyumsuzluğu", ["Bazı oyunlar kendi hikayesi yerine ortak motorun temasını gösteriyor: Terzinin Kumaşları, Fırıncının Sepeti ve Zaman Makinesi Asansörü uzay lazeri sahnesinde; Geometri Terzisi su altı kepçesi sahnesinde; Hayvanat Bahçesi Fotoğrafçısı roket-yakıt sahnesinde açılıyor."], PALE_CORAL, CORAL), Spacer(1, 2 * mm)]
story += [box("2. Görsel kanıt eksikliği", ["Uçan Balonları Kurtar, Manav Terazisi, Lunapark Balonları ve Limonata Festivali gibi tahmin oyunlarında tahmin edilecek nesne görünmüyor; boş pano ve sayı seçenekleri kalıyor.", "Çılgın Robot Atölyesi ve Sihirli Kilim Dokumacısı gibi model oluşturma oyunları gerçek model yerine yazılı hedef kutularına parça eşletiyor."], PALE_GOLD, GOLD), Spacer(1, 2 * mm)]
story += [box("3. Yönerge ile etkileşimin çelişmesi", ["Zaman Makinesi Tamircisi akrep ve yelkovanı sürükle diyor, fakat düğmelerle adım adım ilerletiliyor.", "Robot Kargo Teslimatı rotayı çiz diyor, ancak ok düğmeleriyle program kuruluyor."], PALE_BLUE, BLUE), Spacer(1, 2 * mm)]
story += [box("4. Tek sabit örnek ve tekrar oynanabilirlik", ["Birçok oyun aynı sayı, aynı kart dizisi ve aynı doğru konumla tek kez oynanıyor.", "Bu belgede bütün oyunlar için en az üç değişen tur, konum karıştırma ve kabul ölçütü önerildi."], PALE_TEAL, TEAL)]
story += [PageBreak()]

story += [P("Bütün oyunlarda ortak uygulama standardı", h1)]
standard_rows = [
    [P("Sahne", box_title), P("Başlıkta geçen ana karakter ve nesne gerçek oyun alanında görünür ve matematiksel eylemi taşır.", small)],
    [P("Tur", box_title), P("Her oyun en az üç farklı tur içerir; sayı, nesne sırası, konum ve seçenekler değişir.", small)],
    [P("Ses", box_title), P("Yönerge kısa, doğal Türkçe ile okunur; işlem sembolleri artı, eksi, çarpı, bölü ve eşittir diye seslendirilir.", small)],
    [P("Dokunma", box_title), P("Hareketli yazılı hedefler kullanılmaz; hedefler okunabilir, geniş ve küçük telefonda erişilebilir olur.", small)],
    [P("Yanlış", box_title), P("Yanlış cevap kaybolmaz; hata kaynağı nesne, sayı doğrusu, eş grup, ölçüm veya grafik üzerinde gösterilir.", small)],
    [P("Doğru", box_title), P("Doğru cevap yalnız renk/konfetiyle değil, matematiksel sonucu kanıtlayan animasyonla doğrulanır.", small)],
    [P("Tutarlılık", box_title), P("Ekrandaki nesne sayısı, işlem, seslendirme ve sonuç bütün platformlarda birebir aynı olur.", small)],
]
standards = Table(standard_rows, colWidths=[28 * mm, 148 * mm])
standards.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8D4E2")), ("BACKGROUND", (0, 0), (0, -1), PALE_PURPLE),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 8),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 7),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
story += [standards, Spacer(1, 5 * mm)]
story += bullets(["Can sistemi yalnız kavramsal hata için kullanılmalı; hareket eden hedefi kaçırma veya küçük dokunma alanı ağır cezalandırılmamalı.",
                  "Başarı kaydı, üç turun tamamı ve her turun matematiksel doğruluğu sağlandıktan sonra verilmelidir.",
                  "Tur tekrarında doğru seçenekler aynı konumda kalmamalı; ezberlenebilir sabit sıra kullanılmamalıdır."])
story += [PageBreak()]

last_theme = None
accent_cycle = [CORAL, TEAL, GOLD, PURPLE]
for game in games:
    if game["theme"] != last_theme:
        last_theme = game["theme"]
        theme_name, accent, focus = THEMES[last_theme]
        theme_table = Table([[P(last_theme, badge), P(theme_name, theme_title)]], colWidths=[30 * mm, 146 * mm], rowHeights=[50 * mm])
        theme_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), accent), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                         ("ALIGN", (0, 0), (0, 0), "CENTER"), ("LEFTPADDING", (1, 0), (1, 0), 12),
                                         ("RIGHTPADDING", (1, 0), (1, 0), 12), ("ROUNDEDCORNERS", [10])]))
        story += [Spacer(1, 22 * mm), theme_table, Spacer(1, 10 * mm), P("Bu temadaki ana düzeltme odağı", h2)]
        story += bullets(focus)
        story += [Spacer(1, 6 * mm), box("Tema kabul eşiği", ["Bu temadaki bütün oyunlar üç tur tamamlanmadan bitmiş sayılmayacak.", "Hikaye nesnesi, matematiksel işlem ve geri bildirim aynı sahnede birbirini destekleyecek."], PALE_TEAL, TEAL), PageBreak()]

    accent = accent_cycle[(game["n"] - 1) % len(accent_cycle)]
    story += [header(game["n"], game["title"], game["sub"], accent), Spacer(1, 3.0 * mm)]
    story += [box("Denemede görülen mevcut durum", game["observed"], PALE_CORAL, CORAL, compact=True), Spacer(1, 1.5 * mm)]
    story += [box("Eğitimsel risk", game["risk"], PALE_GOLD, GOLD, compact=True), Spacer(1, 1.5 * mm)]
    story += [P("Yeni sahne ve oynanış", h2)]
    story += bullets(game["new"], bullet_small)
    story += [P("Üç farklı tur", h2), rounds_table(game["rounds"]), Spacer(1, 1.5 * mm)]
    story += [box("Geri bildirim ve bitiş", game["feedback"], PALE_TEAL, TEAL, compact=True), Spacer(1, 1.5 * mm)]
    story += [box("Kabul ölçütü", game["acceptance"], PALE_BLUE, BLUE, compact=True), PageBreak()]

story += [P("Son kabul kontrolü", h1), P("2. sınıf matematik bölümü tamamlanmadan önce", h2)]
story += bullets(["42 oyunun her biri üç farklı turla baştan sona oynanır ve sonuçlar kayıt altına alınır.",
                  "Başlıkta geçen sahne/karakter her oyunda görünür; ortak motor teması hikayeyi bastırmaz.",
                  "Bütün sayı, para, saat, ölçü, işlem, şekil, rota, simetri ve grafik verileri ekrandaki nesnelerle birebir karşılaştırılır.",
                  "Yönerge ile gerçek dokunma/sürükleme/çizme yöntemi aynı olur.",
                  "Yanlış cevapta doğru seçenek doğrudan söylenmeden görsel ve kavramsal ipucu verilir.",
                  "Hareketli yazı hedefleri kaldırılır; küçük telefonda metinler okunur ve dokunma alanları yeterli büyüklükte olur.",
                  "Üç turda doğru konumlar, sayılar ve seçenek sıraları değişir.",
                  "Başarı, yalnız ilk soruda değil bütün tur dizisi tamamlanınca verilir."])
story += [Spacer(1, 4 * mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 2. sınıf matematik listesindeki 42 oyunu kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, mekanik, tur ve test gereksinimlerini ayrıntılı olarak tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)

reader = PdfReader(str(OUT))
assert len(games) == 42
assert len(reader.pages) >= 50
print(str(OUT))
print({"pages": len(reader.pages), "games": len(games), "bytes": OUT.stat().st_size})
