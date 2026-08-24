from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle


ROOT = Path("/Users/ceyda/Documents/New project")
OUT = ROOT / "output/pdf/1_sinif_turkce_oyunlari_detayli_duzeltmeler.pdf"
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
body = ParagraphStyle("body", parent=base, fontName="Arial", fontSize=8.35, leading=10.7, textColor=INK, spaceAfter=1.0 * mm)
small = ParagraphStyle("small", parent=body, fontSize=7.5, leading=9.35, spaceAfter=0.65 * mm)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=4.7 * mm, firstLineIndent=-3.0 * mm, bulletIndent=0, spaceAfter=0.75 * mm)
bullet_small = ParagraphStyle("bullet_small", parent=small, leftIndent=4.7 * mm, firstLineIndent=-3.0 * mm, bulletIndent=0, spaceAfter=0.55 * mm)
h1 = ParagraphStyle("h1", parent=body, fontName="Arial-Bold", fontSize=21, leading=25, textColor=PURPLE, spaceAfter=4 * mm)
h2 = ParagraphStyle("h2", parent=body, fontName="Arial-Bold", fontSize=10.2, leading=12.2, textColor=TEAL, spaceBefore=1.1 * mm, spaceAfter=0.7 * mm)
cover_kicker = ParagraphStyle("cover_kicker", parent=body, fontName="Arial-Bold", fontSize=10, textColor=TEAL, alignment=TA_CENTER, spaceAfter=6 * mm)
cover_title = ParagraphStyle("cover_title", parent=body, fontName="Arial-Bold", fontSize=25, leading=30, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=5 * mm)
cover_sub = ParagraphStyle("cover_sub", parent=body, fontSize=12, leading=17, alignment=TA_CENTER, spaceAfter=9 * mm)
game_title = ParagraphStyle("game_title", parent=body, fontName="Arial", fontSize=13.5, leading=15.7, textColor=colors.white, spaceAfter=0)
badge = ParagraphStyle("badge", parent=body, fontName="Arial-Bold", fontSize=16, leading=17, textColor=colors.white, alignment=TA_CENTER, spaceAfter=0)
box_title = ParagraphStyle("box_title", parent=body, fontName="Arial-Bold", fontSize=9.25, leading=11.0, textColor=CORAL, spaceAfter=0.7 * mm)
round_head = ParagraphStyle("round_head", parent=small, fontName="Arial-Bold", fontSize=7.9, leading=9.1, textColor=PURPLE, alignment=TA_CENTER, spaceAfter=0)
round_text = ParagraphStyle("round_text", parent=small, fontSize=7.05, leading=8.75, spaceAfter=0)
theme_title = ParagraphStyle("theme_title", parent=cover_title, fontSize=22, leading=27, textColor=colors.white)


def P(text, style=body):
    return Paragraph(text, style)


def bullets(items, style=bullet):
    return [Paragraph(item, style, bulletText="•") for item in items]


def header(number, title, subtitle, accent):
    t = Table([[P(str(number), badge), P(f"<b>{title}</b><br/><font size='8' color='#F1EEF8'>{subtitle}</font>", game_title)]],
              colWidths=[15 * mm, 161 * mm], rowHeights=[19 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "CENTER"), ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("RIGHTPADDING", (1, 0), (1, 0), 8), ("ROUNDEDCORNERS", [8]),
    ]))
    return t


def box(title, items, bg, title_color, compact=False):
    title_style = ParagraphStyle("dynamic_box_title", parent=box_title, textColor=title_color)
    content = [P(title, title_style)] + bullets(items, bullet_small if compact else bullet)
    t = Table([[content]], colWidths=[176 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg), ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D7D3DF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROUNDEDCORNERS", [6]),
    ]))
    return t


def rounds_table(items):
    t = Table([[P("1. TUR", round_head), P("2. TUR", round_head), P("3. TUR", round_head)],
               [P(items[0], round_text), P(items[1], round_text), P(items[2], round_text)]],
              colWidths=[58.7 * mm, 58.7 * mm, 58.6 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALE_GOLD), ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFCF5")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDCFAB")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
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
    canv.drawString(MX, 8.5 * mm, "1. Sınıf Türkçe - Ayrıntılı Oyun Düzeltmeleri")
    canv.drawRightString(PAGE_W - MX, 8.5 * mm, str(canv.getPageNumber()))
    canv.restoreState()


def G(n, theme, title, sub, observed, risk, new, rounds, feedback, acceptance):
    return dict(n=n, theme=theme, title=title, sub=sub, observed=observed, risk=risk,
                new=new, rounds=rounds, feedback=feedback, acceptance=acceptance)


games = [
G(1, "Tema 1", "Gökyüzü Çizeri", "Harf yönü, çizgi sırası ve yazma hazırlığı",
  ["Oyun büyük A harfini üç çizgiyle izletiyor. Başlangıç noktası ve gri kılavuz açık; sol alttan tepeye, tepeden sağ alta ve orta çizgi sırası kullanılıyor.", "Başlık gökyüzü/uçak temasını taşısa da ilerleme göstergesi '0/1 rakam' yazıyor. Harf yalnız tek bir büyük A örneğiyle ve tek ölçekte çalışılıyor; küçük a, kalem kaldırma, serbest yazma ve farklı satır boyutu yok."],
  ["Harf çalışmasının 'rakam' diye etiketlenmesi kavram ve seslendirme tutarlılığını bozar.", "Yalnız noktaları takip etmek, kılavuz ortadan kalkınca aynı harfi bağımsız yazabildiğini göstermez.", "Çizginin dışına küçük bir motor sapması can kaybettirirse el-göz koordinasyonu ile harf bilgisini birbirine karıştırır."],
  ["İlerleme etiketi 'harf' olarak düzeltilsin; uçak yalnız yazım çizgisinin üzerinde ilerlesin ve her hamlede kalem kaldırma noktası açıkça gösterilsin.", "İlk aşamada yoğun noktalar, ikinci aşamada yalnız başlangıç-bitiş noktaları, üçüncü aşamada çizgisiz satır kullanılsın.", "Büyük A'dan sonra aynı sesin küçük a biçimi ayrı ve yaş düzeyine uygun yazı karakteriyle çalışılsın.", "Çizgi toleransı geniş ve kademeli olsun; yanlış yönde tüm harf silinmeden yalnız son bölüm geri alınabilsin.", "Harf tamamlanınca çocuk sesi dinlesin, A/a kartını ve A sesiyle başlayan bir görseli eşleştirerek yazıyı sesten koparmasın."],
  ["Yoğun noktalı büyük A: üç çizgi doğru sırayla izlenir; her hamlenin yön oku görünür.", "Seyrek noktalı büyük A ve küçük a: başlangıç-bitiş işaretleriyle, daha az kılavuzla yazılır.", "Çizgisiz satırda A/a bağımsız yazılır; ardından 'arı' görselindeki başlangıç sesiyle eşleştirilir."],
  ["Yanlış yönde uçak son doğru noktada dursun; 'başlangıçtan tepeye doğru' gibi yön ipucu verilsin, çizgi tamamı silinmesin.", "Doğru hamlede iz yalnız görsel efektle değil, başlangıç ve bitiş noktalarının sırayla numaralanmasıyla doğrulansın.", "Bitişte harf adı yerine önce ses /a/ dinletilsin; büyük ve küçük biçimler yan yana gösterilsin."],
  ["Sayaçta 'rakam' sözcüğü hiçbir yerde görünmeyecek; metin, ses ve ilerleme 'harf' diyecek.", "Üç kılavuz düzeyi ve en az bir bağımsız yazma turu tamamlanmadan oyun bitmeyecek.", "Çizim kabulü yalnız doğru şekle değil doğru başlangıç, yön ve hamle sırasına bağlı olacak; motor sapması ağır ceza almayacak."]),

G(2, "Tema 1", "Sesli Sepet", "Kelime içindeki hedef sesi işitsel olarak ayırt etme",
  ["A sesi geçen Elma, Armut ve Ayı; Top, Kedi ve Kuş çeldiricileriyle birlikte su altı kartlarında gösteriliyor. Alt bölümde sepet bulunmasına karşın sahnenin ana görünümü balık/balon motoru.", "Bütün nesnelerin hem resmi hem yazılı adı açık. Tek hedef A ve tek sabit altılı grup kullanılıyor; çocuk sesi dinlemeden kelimelerin yazımındaki A harfini görerek de doğru seçim yapabiliyor."],
  ["İşitsel tanıma kazanımı, yazılı kelimede harf arama görevine dönüşebilir.", "A sesinin kelime başında, ortasında ve sonunda bulunduğu konumlar ayrı ayrı fark ettirilmediği için ses çözümleme yüzeysel kalır.", "Balık/sepet karışımı tema, 'sesi sepete toplama' hikâyesini zayıflatır ve seçilen nesnelerin gerçekten sepete girmesini göstermiyor."],
  ["Ana sahne gerçek bir pazar/oyuncak sepeti olsun; nesne kartlarında ilk turda yalnız resim bulunsun, kelime yazısı cevap sonrasında açılsın.", "Her nesnenin adı ayrı dinleme düğmesiyle ve doğal hece vurgusuyla çalınsın; otomatik konuşma bittikten sonra tekrar dinlenebilsin.", "Çocuk hedef sesi duyduğu konumu baş-orta-son şeridinde işaretlesin; sonra nesneyi sepete sürüklesin.", "Bir turda yalnız hedef sesi seçme, bir turda hedef sesi olmayanları ayırma, bir turda iki yakın sesi karşılaştırma kullanılmalı.", "Aynı nesne havuzu her açılışta tekrarlanmasın; yazılı etiket yalnız işitsel karar kaydedildikten sonra doğrulama olarak gösterilsin."],
  ["Resim + ses: arı, elma, masa, top ve kuş dinlenir; /a/ içerenler sepete alınır.", "Hedef sesin yeri: arı başta, masa ortada, elma sonda /a/ sesiyle baş-orta-son şeridine yerleştirilir.", "Yakın karşılaştırma: /a/ ve /e/ dinlenir; anne, elma, ev, at ve kedi iki ayrı sepete ayrılır."],
  ["Yanlış seçimde nesnenin adı yavaş ve hecelenmeden doğal biçimde tekrar çalınsın; hedef sesin geçtiği harf doğrudan gösterilmesin.", "Doğru seçimde nesne gerçekten sepete düşsün; sesin bulunduğu konum renkli bir noktayla ancak cevap sonrasında açılsın.", "Bitişte seçilen sözcükler sesli tekrar edilirken yazılı biçimleri görünür olsun; işitsel ve görsel temsil bağlansın."],
  ["İlk turda kelime yazıları gizli olacak; başarı yalnız görsel harf aramayla elde edilemeyecek.", "Baş, orta ve son konumlarının üçü de en az ikişer örnekle çalışılacak.", "Seslendirme ile ekrandaki nesne adı birebir tutarlı olacak; yanlışta can eksiltmeden tekrar dinleme sağlanacak."]),

G(3, "Tema 1", "Su Altı Baloncukları", "Büyük-küçük harfi görsel olarak ayırt etme",
  ["Hedef N/n; N, M, n, H, N, Z ve K kartları su altı sahnesinde gösteriliyor. Yönerge baloncuk patlatmayı söylese de kartlar balık simgesi taşıyor ve seçilenler alt sepet/kova alanına gidiyor.", "İki büyük N ve bir küçük n doğru kabul ediliyor. Harfler tek yazı tipinde, tek boyutta ve tek sabit dizide; benzer biçimli harflerin hangi özelliğe göre ayrıldığı gösterilmiyor."],
  ["Baloncuk-balık-sepet kavramlarının karışması, çocuğun neye dokunacağını gereksiz yere zorlaştırır.", "Tek fontta doğru harfi seçmek, farklı kitap/yazı biçimlerinde N/n'yi tanımayı garanti etmez.", "Sadece hızla patlatma hedeflenirse biçim ayrıntısını incelemek yerine deneme-yanılma ve motor hız ödüllenir."],
  ["Gerçek yuvarlak baloncuklar kullanılsın; seçilince patlasın, sepet/kova kaldırılarak tek tema korunsun.", "Hedef kart büyük N ve küçük n biçimini yan yana göstersin; çocuk önce ortak ses ilişkisini dinlesin.", "Çeldiriciler N-M, n-m, N-H gibi anlamlı görsel yakınlıklardan seçilsin; fark çizgileri cevap sonrasında büyütülsün.", "İkinci ve üçüncü turda harf boyutu, konumu ve iki güvenli okul yazı tipi değişsin; aşırı dekoratif font kullanılmasın.", "Süre baskısı ilk düzeyde kapalı olsun; doğru seçim sayısından önce yanlış seçimin türü kaydedilsin."],
  ["Sabit büyük kartlarda N, M, H, Z arasından bütün N'ler seçilir.", "N/n birlikte hedeflenir; n-m-h küçük harfleri farklı boyut ve konumlarda ayırt edilir.", "Karışık büyük-küçük turda aynı sesi gösteren N ve n eşleştirilir; M/m ayrı aileye gönderilir."],
  ["Yanlış M seçiminde N ile M yan yana büyütülüp orta çizgi/çapraz yapı karşılaştırılsın; doğru harf söylenip geçilmesin.", "Doğru baloncuk gerçek patlama ve kısa /n/ sesiyle doğrulansın; harf adı uzun biçimde tekrar edilmesin.", "Bitişte N-n harf ailesi ile 'nar' görseli eşleştirilsin; görsel tanıma sesle ilişkilendirilsin."],
  ["Yönerge, görsel nesne ve sonuç alanı aynı baloncuk temasını kullanacak.", "En az iki yazı boyutu ve iki güvenli yazı biçimi test edilecek; küçük n ile m/h çeldiricileri bulunacak.", "İlk düzeyde süre veya hareket baskısı olmayacak; bütün harfler karar verilene kadar sabit ve tam görünür kalacak."]),

G(4, "Tema 2", "Hece Treni", "Sesleri birleştirerek açık ve kapalı hece kurma",
  ["Başlık tren olsa da oyun köprü/eşleştirme motorunda açılıyor. Ekranda yalnız hedef T ve kaynak A bulunuyor; A kartını T yuvasına taşıyınca AT oluşuyor.", "Yönerge ve üst konuşma cevabı 'AT' diye baştan söylüyor. Oyun yalnız bir kapalı hece örneği içeriyor; alt başlıktaki açık ve kapalı hece karşılaştırması, ses uzatma ve birleştirme süreci yok."],
  ["Çocuk /a/ ve /t/ seslerini soldan sağa birleştirmek yerine hazır A kartını tek hedefe sürüklüyor.", "Tek örnek, ünlüyle biten açık hece ile ünsüzle biten kapalı hece farkını öğretmez.", "Tren hikâyesinin görünmemesi ve cevabın baştan yazılması, görevi anlamlı okuma yerine zorunlu sürüklemeye indirger."],
  ["Gerçek tren lokomotifi ve iki vagon çizilsin; her vagonda bir ses kartı bulunsun, vagonlar birleşirken sesler aralıksız kaynaşsın.", "Çocuk sesi tek tek dinlesin, vagonları soldan sağa dizsin ve birleşik heceyi ancak sonrasında görsün.", "Açık hece için ünsüz+ünlü (NA, NE), kapalı hece için ünlü+ünsüz (AN, AT) ayrı renkli istasyonlarda karşılaştırılsın.", "Tek doğru hedef yerine iki veya üç olası ses kartı verilsin; hedef görseli/sesi heceyi doğrudan yazmadan yönlendirsin.", "Son turda vagon sırası değiştirilerek AN-NA gibi aynı iki sesten farklı hecelerin ve anlamlı kelime parçalarının oluştuğu gösterilsin."],
  ["/a/ + /t/ sesleri yavaşça yaklaştırılır; çocuk AT'ı dinleyip kurar, yazı sonuçta açılır.", "/n/ + /a/ = NA açık hecesi ve /a/ + /n/ = AN kapalı hecesi karşılaştırılır.", "NE, EN, TA, AT heceleri karışık ses vagonlarından kurulur; çocuk heceyi dinleyip doğru iki vagonu ve sırayı seçer."],
  ["Yanlış sırada vagonlar çarpışmamalı; iki ses ayrı ayrı çalınıp aralarındaki sıra oku vurgulansın.", "Doğru birleşmede sesler kopuk harf adlarıyla değil kesintisiz /aaa-t/ veya /nnn-a/ biçiminde kaynaştırılsın.", "Bitişte açık-kapalı etiketi, hecenin son sesine bakılarak çocuk tarafından seçilsin; etiket otomatik verilmesin."],
  ["Ekranda gerçek tren/vagon sahnesi bulunacak; köprü motoru ve tek boş hedef kullanılmayacak.", "En az iki açık ve iki kapalı hece, aynı seslerin ters sırasını da içerecek şekilde çalışılacak.", "Hedef hece başlangıçta yazılı olarak gösterilmeyecek; öğrenci sesi birleştirmeden doğru cevabı kopyalayamayacak."]),

G(5, "Tema 2", "Zıp Zıp Kurbağa", "Heceleri akıcı ve doğru tanıma",
  ["Başlık kurbağa ve nilüfer yaprağını anlatıyor; gerçek ekran su altındaki balık kartları ve kova/sepet motorunu kullanıyor. AN, EN, İN, NA ve NE aynı anda görünür; hedef NE konuşma alanında yazılıdır.", "Yalnız tek hedef hece ve tek sabit seçenek grubu var. 'Hızlı okuma/görsel hafıza' alt başlığına rağmen kartlar saklanmıyor, tur tekrarlanmıyor ve okuma süresi doğruluk sonrası ölçülmüyor."],
  ["Çocuk sesli komutu dinlemeden üstte yazan NE'yi görüp aynı etiketi seçebilir.", "Balık-kova sahnesi kurbağa/nilüfer hikâyesiyle çelişir; doğru seçim zıplama eylemine dönüşmez.", "Hız ödülü erken verilirse benzer AN-NA, EN-NE hecelerinde doğruluk ve yön sırası zarar görebilir."],
  ["Gerçek gölet, kurbağa ve sabit nilüfer yaprakları çizilsin; her yaprakta bir hece büyük ve yüksek kontrastla gösterilsin.", "İlk turda hedef yalnız sesli verilsin; yazılı hedef karar sonrasında açılarak kopyalama engellensin.", "Kurbağa yalnız doğru yaprağa zıplasın; kartlar hareket etmesin ve süre ilk iki turda değerlendirilmesin.", "Akıcılık düzeyinde heceler kısa süre gösterilip kapanabilir, fakat önce doğruluk eşiği geçilmeli; yanlışta süre değil ses-sıra ilişkisi açıklanmalı.", "AN-NA ve EN-NE gibi ters sıralı heceler özellikle karşılaştırılsın; her sesin soldan sağa okuma yönü parmak iziyle izlenebilsin."],
  ["Sesli hedef NE; AN, EN, NA, NE yaprakları sabitken doğru yaprağa zıplanır, hedef yazısı gizlidir.", "AN-NA ve EN-NE çiftleri art arda dinlenir; aynı harflerin sırasının heceyi değiştirdiği görülür.", "Beş hecelik akıcılık dizisi doğru okunduktan sonra süre kaydedilir; yanlış hece tekrar dinlenip dizi yeniden başlatılmaz."],
  ["Yanlış yaprakta kurbağa başlangıçta kalsın; seçilen ve duyulan hecenin ilk/son sesleri farklı renkle gösterilsin.", "Doğru zıplayışta hece sesli okunup yaprakta kısa süre büyüsün; yalnız konfetiyle geçilmesin.", "Bitişte önce doğruluk yüzdesi, sonra isteğe bağlı akıcılık süresi gösterilsin; hız tek başarı ölçütü olmasın."],
  ["Kurbağa, gölet ve nilüfer görselleri gerçekten kullanılacak; balık/kova motoru görünmeyecek.", "Hedef hece ilk turda yazıyla gösterilmeyecek ve en az dört farklı hedef hece rastgele kullanılacak.", "Akıcılık puanı yalnız yüzde 90 ve üzeri doğruluktan sonra hesaplanacak; motor hatası can kaybettirmeyecek."]),

G(6, "Tema 2", "Mıknatıslı Uzay Gemisi", "Ses sırasını seçerek hece inşa etme",
  ["Roket ve yakıt hunisi uzay temasına kısmen uyuyor; E, T, K ve S kartları roket çevresinde hareket ediyor. Hedef ET hem yönergede hem konuşma alanında yazılı; ayrıca 'önce E, sonra T' ifadesi çözüm sırasını doğrudan veriyor.", "Tek sabit ET hecesi iki dokunuşla tamamlanıyor. Meteor/mıknatıs çekme görseli gerçek bir birleşme şeridi oluşturmuyor; yanlış sıra ile oluşan farklı hece seslendirilmiyor."],
  ["Çocuk hece kurmak yerine açıkça söylenen iki harfe sırayla dokunuyor.", "Hareketli kartı yakalama motor becerisi, sesleri doğru sırada birleştirme becerisine karışıyor.", "Tek ET örneği, aynı harflerle TE'nin farklı bir hece olduğuna veya başka ünlü-ünsüz birleşimlerine genellenmiyor."],
  ["Harf meteorları karar verilene kadar sabit yörüngede dursun; geminin mıknatısı seçilen harfi görünür hece şeridine çeksin.", "Hedef ilk düzeyde resim ve sesle verilsin, yazıyla hece gösterilmesin; yönerge 'önce E sonra T' gibi cevabı söylemesin.", "İlk ve ikinci ses yuvası ayrı olsun; seçilen harfler soldan sağa yerleşirken sürekli birleştirme sesi çalınsın.", "ET-TE, EN-NE, AT-TA çiftleri aynı iki harfle karşılaştırılsın; sıra değişiminin ses ve anlamı değiştirdiği gözlensin.", "Son turda çocuk duyduğu heceyi kurduktan sonra aynı heceyle başlayan/bitiren basit kelime görselini seçsin."],
  ["Sesli hedef /et/; E ve T meteorları seçilip ET kurulur, yazı sonuçta görünür.", "Aynı E-T meteorları ters sırada TE olur; ET ve TE sesleri karşılaştırılır.", "EN, NE, AT ve TA karışık dört harf havuzundan dinlenerek kurulur; uygun kelime görseliyle ilişkilendirilir."],
  ["Yanlış harf şeritte kalıcı ceza oluşturmasın; geri gönder düğmesiyle yalnız son seçim düzeltilebilsin.", "Yanlış sırada iki ses ayrı ve birleşik biçimde dinletilsin; hedefin yazılı cevabı açılmasın.", "Doğru hecede gemi iki meteoru tek kapsülde birleştirsin ve heceyi doğal biçimde seslendirsin."],
  ["Yönerge hedef harfleri ve sırasını doğrudan söylemeyecek; hedef yazısı cevap kaydedilmeden görünmeyecek.", "Kartlar hareket etmeyecek; en az üç ters sıra çifti ve dört farklı hece kullanılacak.", "Seçilen harflerin ekrandaki sırası, seslendirme sırası ve oluşan hece her tur birebir aynı olacak."]),

G(7, "Tema 3", "Kelime Fabrikası", "Heceleri birleştirerek anlamlı kelime oluşturma",
  ["Başlık fabrika olsa da oyun köprü/eşleştirme motorunda açılıyor. İki hedef '1. Hece' ve '2. Hece'; parçalar NE, A, LET ve AN. Üst konuşma alanı ALET cevabını baştan gösteriyor.", "A ve LET kartlarını yuvalara sürüklemek tek doğru çözüm. Kelimenin resmi/anlamı, hecelerin sesli kaynaşması, hece sınırı ve yeni kelime turu yok; 'fabrika üretimi' yalnız etiket eşlemesi olarak kalıyor."],
  ["Çocuk kelimeyi sentezlemek yerine ekrandaki ALET yazısını kopyalayıp A-LET parçalarını yerleştirir.", "Tek kelime ve sabit hece sınırı, farklı iki/üç heceli kelimelere aktarım sağlamaz.", "Doğru kelimenin anlamını seçme aşaması olmadığı için rastlantısal veya mekanik parça sırası da başarı sayılabilir."],
  ["Gerçek üretim bandında hece kasaları, soldan sağa iki veya üç montaj yuvası ve sonunda resim paketi bulunsun.", "Hedef ilk turda resim + ses, ikinci turda yalnız resim, üçüncü turda kısa bağlam cümlesiyle verilsin; kelime yazısı başlangıçta gizlensin.", "Heceler yuvaya geldiğinde ayrı ayrı ve sonra kesintisiz kelime olarak seslendirilsin; hece sınırı kısa renk geçişiyle gösterilsin.", "Anlamlı kelime oluşunca doğru resim üretim bandından çıksın; anlamsız dizide fabrika durup ses sırasını tekrar dinletsin.", "ALET dışında NANE, ANNE, ELMA gibi öğretim grubuna uygun kelimeler ve en az bir üç heceli sözcük kullanılmalı."],
  ["Alet resmi/sesi verilir; A + LET seçilir, ALET yazısı yalnız üretim sonunda açılır.", "NANE için NA + NE; ANNE için AN + NE heceleri benzer çeldiriciler arasından sıralanır.", "Üç heceli basit bir kelime resim/bağlamdan kurulur; çocuk oluşan kelimeyi cümlede uygun boşluğa yerleştirir."],
  ["Yanlış hecede kart yerine dönerken iki parçanın birleşik sesi çalınsın; cevap kelime doğrudan gösterilmesin.", "Doğru kelimede heceler ayrı renklerini koruyup ardından tek renk kelime kartında birleşsin; anlam resmi görünür olsun.", "Bitişte çocuk kelimeyi bir kez sesli dinlesin ve doğru görseli seçsin; yalnız yuvaları doldurmak yeterli olmasın."],
  ["Fabrika sahnesi gerçekten kullanılacak; köprü hedefleri ve başlangıçta görünen cevap kaldırılacak.", "En az dört farklı iki heceli ve bir üç heceli kelime, her açılışta değişen sırayla kullanılacak.", "Başarı için hem doğru hece sırası hem doğru anlam görseli tamamlanacak; anlamsız hece dizisi kabul edilmeyecek."]),

G(8, "Tema 3", "Gizemli Sandık", "Kelimeyi okuyup anlamıyla eşleştirme",
  ["Yönerge sandıkta ANNE yazdığını ve doğru resimli anahtarı seçmeyi söylüyor; gerçek sahne su altındaki balık kartları ve kova/sepet. Sandık, kilit veya anahtar görünmüyor.", "Seçenekler 'Anne', 'Baba', 'Elma', 'Kedi' diye hem resim hem aynı yazılı etiketle sunuluyor. Hedef ANNE ile doğru seçenek Anne birebir yazı eşlemesi; yalnız tek soru var."],
  ["Okuduğunu anlama, aynı kelimeyi büyük-küçük harfle bulma görevine dönüşüyor.", "Metin, cümle veya bağlam olmadığı için kelimenin anlamını çıkarma ve mekanik okumadan anlama geçişi gerçekleşmiyor.", "Başlık-sahne çelişkisi çocuğun beklenen eylemini belirsizleştiriyor; yanlış seçimin neden yanlış olduğuna dair anlam geri bildirimi yok."],
  ["Gerçek sandık ve üç-dört görsel anahtar çizilsin; anahtarların üzerinde kelime yazısı bulunmasın, yalnız resim olsun.", "İlk turda sandıkta tek kelime; ikinci turda kısa cümle; üçüncü turda iki cümlelik mini durum verilsin.", "Çocuk metni dinleyebilir fakat otomatik ses, okumadan önce cevabı vurgulamasın; dinleme düğmesi erişim desteği olarak açıkça işaretlensin.", "Doğru anahtar seçilince sandık açılıp kelimenin/cümlenin anlamına uygun nesne veya kısa olay animasyonu çıksın.", "Sözcük havuzu ANNE ile sınırlı kalmasın; resimsel olarak açık, öğretim grubuna uygun kelimeler ve basit kim/ne/nerede soruları kullanılmalı."],
  ["Sandıkta 'ANNE' yazısı; etiket taşımayan anne-baba-elma-kedi resim anahtarlarından anne seçilir.", "'Nane al.' kısa cümlesi okunur; nane görseli bulunan anahtar seçilir ve sandıktan nane çıkar.", "'Ece elma alır. Elma nerede?' mini metninde doğru nesne/konum anahtarı seçilip bir anlam sorusu yanıtlanır."],
  ["Yanlış resimde hedef kelime yeniden gösterilir ve görselin adı sesli söylenir; doğru resim doğrudan parlatılmaz.", "Doğru anahtar kilide gerçekten girsin; sandıktan çıkan nesne metindeki anlamı görsel olarak doğrulasın.", "Bitişte çocuk kelimeyi/cümleyi tekrar okuyup bir anlam sorusunu yanıtlasın; yalnız tek dokunuşla bitmesin."],
  ["Sandık, kilit ve anahtar görselleri gerçek sahnede bulunacak; balık/kova motoru kullanılmayacak.", "Doğru seçenek üzerinde hedef kelimenin aynısı yazmayacak; karar resim/anlam üzerinden verilecek.", "En az üç farklı kelime, iki kısa cümle ve bir mini metin turu olmadan 'okuduğunu anlama' oyunu tamamlanmış sayılmayacak."]),

G(9, "Tema 3", "Sihirli Daktilo", "Duyduğu kelimeyi görmeden doğru harflerle yazma",
  ["Oyun NANE kelimesini dinletip dört boşluğa harf seçtiriyor. Fakat üst konuşma alanında NANE açıkça yazıyor; 'bakmadan yazma' daha başlamadan bozuluyor.", "Harf paletinin ilk satırı N-A-N-E biçiminde doğru kelime sırasıyla dizilmiş. GÖSTER düğmesi başlangıçtan erişilebilir; yalnız tek kelime ve tek macera var."],
  ["Çocuk sesi çözümleyip dikte yapmak yerine üstteki kelimeyi kopyalayabilir veya ilk sıradaki dört harfe soldan sağa basabilir.", "Hazır GÖSTER ve sabit harf dizilimi deneme-yanılmayı teşvik eder; işitsel kısa süreli bellek ölçülmez.", "Tek NANE örneği, farklı ses sayısı, yinelenen harf, hece sınırı ve yazım doğruluğuna genellenmez."],
  ["Konuşma alanında hedef kelime asla yazılmasın; yalnız nötr 'Dinle ve yaz' yönergesi bulunsun. Ekran okuyucu metni de hedefi açıklamamalı.", "Harf paleti her denemede karıştırılsın; hedef harfler aynı satırda doğru sırayla dizilmesin ve gerekli yinelenen harf adedi teknik olarak doğru çalışsın.", "DİNLE sınırsız veya yaşa uygun sayıda tekrar edilebilsin; tekrar dinleme ceza oluşturmasın. GÖSTER ancak iki bağımsız denemeden sonra, kademeli ipucu olarak açılsın.", "İlk ipucu hece sayısı, ikinci ipucu ilk ses, son yardım kısa süreli kelime ön izlemesi olsun; ön izleme kapandıktan sonra giriş temiz değil korunmuş biçimde düzeltilebilsin.", "Kelime havuzu NANE, ANNE, ALET, ELMA gibi farklı yapıdaki sözcüklerden oluşsun; son tur kısa iki kelimelik öbeğe geçsin."],
  ["NANE yalnız sesle dinlenir; karışık harflerden N-A-N-E yazılır, hedef hiçbir yerde görünmez.", "ANNE ve ALET dönüşümlü gelir; çift N ile tek N farkı işitsel/hece desteğiyle yazılır.", "'ELMA AL' gibi kısa öbek dinlenir; boşluk ayrı bir tuş/yuva olarak kullanılır ve yazım sonrasında resimle anlam kontrolü yapılır."],
  ["Yanlış harfte bütün kelime silinmesin; hatalı konum boş kalıp ses yeniden dinlenebilsin. Hangi doğru harfin gerektiği doğrudan söylenmesin.", "Doğru yazımda daktilo kâğıdı kelimeyi hece sınırı göstermeden doğal bütün olarak yazsın; ardından sesle karşılaştırılsın.", "Bitişte yazılan kelimeye uygun resim seçilerek rastlantısal harf dizisinin değil doğru sözcüğün üretildiği doğrulansın."],
  ["Hedef kelime konuşma balonunda, erişilebilir metinde veya başka bir ekranda yazılı görünmeyecek.", "Harfler her tur karışık olacak; hedef kelimenin harfleri doğru sırada aynı satırda dizilmeyecek.", "GÖSTER ilk iki denemede kapalı olacak; en az dört kelime ve bir kısa öbek bağımsız dikteyle tamamlanacaktır."]),
]


THEMES = {
    "Tema 1": ("Harf ve Ses Oyunları", CORAL,
               ["Harf adı ile ses birbirinden ayrılmalı; dinleme görevi yazılı cevabı önceden göstermemelidir.", "Büyük-küçük harf ve farklı güvenli yazı biçimleri, hız baskısı olmadan ayırt edilmelidir.", "Yazma görevleri kılavuzdan bağımsız yazmaya kademeli geçiş ve doğru yön/hamle sırası içermelidir."]),
    "Tema 2": ("Hece Oyunları", TEAL,
               ["Sesler harf adlarıyla kopuk okunmamalı; soldan sağa kesintisiz biçimde kaynaştırılmalıdır.", "Açık ve kapalı heceler aynı seslerin ters sırası dahil çoklu örneklerle karşılaştırılmalıdır.", "Kurbağa, tren ve uzay gemisi sahneleri gerçek oyun eylemini taşımalı; ortak balık/köprü motoru kullanılmamalıdır."]),
    "Tema 3": ("Kelime, Anlama ve Dikte Oyunları", PURPLE,
               ["Kelime cevabı başlangıçta görünmemeli; hece sentezi anlam resmi veya bağlamla doğrulanmalıdır.", "Okuduğunu anlama aynı kelimeyi eşleme değil, etiketsiz görsel, cümle ve mini metin sorularına ilerlemelidir.", "Dikte sırasında hedef kelime bütün görünür/erişilebilir alanlardan gizlenmeli ve harf paleti karıştırılmalıdır."]),
}


doc = BaseDocTemplate(str(OUT), pagesize=A4, rightMargin=MX, leftMargin=MX, topMargin=TOP, bottomMargin=BOTTOM,
                      title="1. Sınıf Türkçe Oyunları - Ayrıntılı Düzeltmeler", author="Macera Akademi oyun incelemesi")
frame = Frame(MX, BOTTOM, PAGE_W - 2 * MX, PAGE_H - TOP - BOTTOM, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

story = [Spacer(1, 16 * mm), P("MACERA AKADEMİ", cover_kicker),
         P("1. Sınıf Türkçe Oyunları<br/>Ayrıntılı Düzeltmeler", cover_title),
         P("9 oyunun gerçek ekranları açılarak, ilk oynanışları denenerek ve kaynak görevleriyle karşılaştırılarak hazırlanmıştır.", cover_sub)]
cover_box = Table([[P("<b>Kapsam</b><br/>Bu belge 1. sınıf Türkçe listesindeki t01-t09 oyunlarının tamamını kapsar. Her oyun için denemede görülen durum, eğitimsel risk, uzun yeni sahne ve oynanış tasarımı, üç kademeli tur, geri bildirim ve ölçülebilir kabul koşulları verilir.")]], colWidths=[153 * mm])
cover_box.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), PALE_TEAL), ("BOX", (0,0), (-1,-1), 0.7, TEAL),
                               ("LEFTPADDING", (0,0), (-1,-1), 14), ("RIGHTPADDING", (0,0), (-1,-1), 14),
                               ("TOPPADDING", (0,0), (-1,-1), 13), ("BOTTOMPADDING", (0,0), (-1,-1), 13)]))
story += [cover_box, Spacer(1, 9 * mm), P("İnceleme yaklaşımı", h2)]
story += bullets(["1. sınıf profili seçilerek Türkçe listesindeki 9 oyunun tamamı tek tek açıldı; başlık, sahne, konuşma alanı, kontrol, seçenekler ve ilk görev görünümü incelendi.",
                  "Rakam/iz sürme, balık-sepet, köprü, roket, daktilo ve sıra motorları Türkçe kaynak görevleriyle karşılaştırıldı.",
                  "Düzeltmeler ses-harf ilişkisi, soldan sağa birleştirme, anlam kurma, bağımsız dikte, kademeli ipucu, üç tur ve ölçülebilir kabul koşulunu birlikte ele alır."])
story += [PageBreak()]

story += [P("Testten çıkan öncelikli bulgular", h1)]
story += [box("1. Türkçe hedefi başka motorların içinde kayboluyor", ["Gökyüzü Çizeri sayacında 'rakam' yazıyor. Hece Treni köprü, Zıp Zıp Kurbağa ve Gizemli Sandık balık/kova, Kelime Fabrikası köprü motorunda açılıyor. Başlık ve gerçek eylem birçok oyunda uyuşmuyor."], PALE_CORAL, CORAL), Spacer(1,2*mm)]
story += [box("2. Cevaplar başlangıçta açık", ["Hece Treni AT, Mıknatıslı Uzay Gemisi ET, Kelime Fabrikası ALET ve Sihirli Daktilo NANE cevabını konuşma alanında gösteriyor. Bazı yönergeler doğru harf sırasını da doğrudan söylüyor."], PALE_GOLD, GOLD), Spacer(1,2*mm)]
story += [box("3. Tek örnek, tek tur ve sınırlı genelleme", ["Dokuz oyunun tamamı tek sabit hedef üzerinden tanımlanmış: yalnız A yazma, N ayırt etme, AT/ET/NE hecesi, ALET/ANNE/NANE kelimesi. Açık-kapalı hece, farklı harf konumu ve cümle anlama genellenmiyor."], PALE_BLUE, BLUE), Spacer(1,2*mm)]
story += [box("4. Dikte ve anlama geçerliliği", ["Sihirli Daktilo hedef kelimeyi gösterdiği ve N-A-N-E harflerini doğru sırada dizdiği için bakmadan yazmayı ölçmüyor. Gizemli Sandık doğru seçeneğin üzerinde yine 'Anne' yazdığı için anlamayı değil aynı kelimeyi bulmayı ölçüyor."], PALE_TEAL, TEAL)]
story += [PageBreak()]

story += [P("Bütün Türkçe oyunlarında ortak uygulama standardı", h1)]
rows = [
    [P("Ses", box_title), P("Harf adı ile ses ayrılır; hece ve kelime doğal, kesintisiz seslendirilir. Dinleme tekrarına ceza verilmez.", small)],
    [P("Görünürlük", box_title), P("İşitsel tanıma ve dikte hedefi, cevap kaydedilmeden konuşma balonu veya erişilebilir metinde yazmaz.", small)],
    [P("Tur", box_title), P("Her oyun en az üç kademeli tur içerir; hedef harf, hece, kelime veya bağlam değişir.", small)],
    [P("Yönerge", box_title), P("Başlıkta söylenen uçak, sepet, tren, kurbağa, gemi, fabrika, sandık veya daktilo gerçek etkileşim nesnesidir.", small)],
    [P("Yanlış", box_title), P("Yanlışta doğru cevap verilmez; ses tekrar edilir, sıra/konum karşılaştırılır ve yalnız son adım düzeltilebilir.", small)],
    [P("Doğru", box_title), P("Doğru yanıt ses, yazı ve anlam resmi/olayıyla birlikte kanıtlanır; yalnız konfeti veya puan yetmez.", small)],
    [P("Erişim", box_title), P("Kartlar sabit ve en az 44 px olur; küçük motor sapması veya tekrar dinleme can kaybettirmez.", small)],
    [P("Bağımsızlık", box_title), P("Kılavuz, hedef yazısı ve hazır sıra aşamalı azalır; son tur bağımsız okuma/yazmayı gerçekten ölçer.", small)],
]
standards = Table(rows, colWidths=[28 * mm, 148 * mm])
standards.setStyle(TableStyle([("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#D8D4E2")), ("BACKGROUND", (0,0), (0,-1), PALE_PURPLE),
                               ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 8),
                               ("RIGHTPADDING", (0,0), (-1,-1), 8), ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7)]))
story += [standards, Spacer(1,5*mm)]
story += bullets(["Hız yalnız doğruluk eşiği geçildikten sonra ikincil akıcılık ölçütü olarak gösterilmelidir.",
                  "Yazı tipi, ses kaydı, seçenek etiketi ve kabul edilen cevap Türkçe karakterler dahil birebir tutarlı olmalıdır.",
                  "Başarı tek ilk soruda değil, üç tur ve kabul ölçütleri tamamlandığında kaydedilmelidir."])
story += [PageBreak()]

last_theme = None
accent_cycle = [CORAL, TEAL, GOLD, PURPLE]
for game in games:
    if game["theme"] != last_theme:
        last_theme = game["theme"]
        theme_name, accent, focus = THEMES[last_theme]
        theme_table = Table([[P(last_theme, badge), P(theme_name, theme_title)]], colWidths=[30*mm,146*mm], rowHeights=[50*mm])
        theme_table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), accent), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                                         ("ALIGN", (0,0), (0,0), "CENTER"), ("LEFTPADDING", (1,0), (1,0), 12),
                                         ("RIGHTPADDING", (1,0), (1,0), 12), ("ROUNDEDCORNERS", [10])]))
        story += [Spacer(1,22*mm), theme_table, Spacer(1,10*mm), P("Bu temadaki ana düzeltme odağı", h2)] + bullets(focus)
        story += [Spacer(1,6*mm), box("Tema kabul eşiği", ["Bu temadaki bütün oyunlar üç kademeli tur tamamlanmadan bitmiş sayılmayacak.", "Ses, yazı, görsel anlam ve gerçek oyun eylemi aynı hedefi gösterecek; cevap başlangıçta görünmeyecek."], PALE_TEAL, TEAL), PageBreak()]

    accent = accent_cycle[(game["n"] - 1) % len(accent_cycle)]
    story += [header(game["n"], game["title"], game["sub"], accent), Spacer(1,2.4*mm)]
    story += [box("Denemede görülen mevcut durum", game["observed"], PALE_CORAL, CORAL, True), Spacer(1,1.0*mm)]
    story += [box("Eğitimsel risk", game["risk"], PALE_GOLD, GOLD, True), Spacer(1,1.0*mm)]
    story += [P("Yeni sahne ve oynanış", h2)] + bullets(game["new"], bullet_small)
    story += [P("Üç kademeli tur", h2), rounds_table(game["rounds"]), Spacer(1,1.0*mm)]
    story += [box("Geri bildirim ve bitiş", game["feedback"], PALE_TEAL, TEAL, True), Spacer(1,1.0*mm)]
    story += [box("Kabul ölçütü", game["acceptance"], PALE_BLUE, BLUE, True), PageBreak()]

story += [P("Son kabul kontrolü", h1), P("1. sınıf Türkçe bölümü tamamlanmadan önce", h2)]
story += bullets(["9 oyunun her biri üç kademeli turla baştan sona oynanır; hedef, seslendirme, yazı ve kabul edilen cevap kayıt altına alınır.",
                  "Gökyüzü Çizeri ilerlemesinde 'rakam' değil 'harf' yazar; bağımsız A/a yazma turu bulunur.",
                  "Sesli Sepet'in ilk işitsel turunda kelime yazıları görünmez; sesin baş-orta-son konumu çalışılır.",
                  "Hece Treni açık ve kapalı heceleri gerçek vagon ve kesintisiz ses birleştirmeyle öğretir.",
                  "Zıp Zıp Kurbağa gerçek nilüfer sahnesinde, hedef yazısı gizli ve doğruluk öncelikli çalışır.",
                  "Kelime Fabrikası başlangıçta cevabı göstermez; hece sırası anlam resmiyle doğrulanır.",
                  "Gizemli Sandık'ta anahtar seçeneklerinde hedef kelimenin aynısı yazmaz; cümle ve mini metin turu bulunur.",
                  "Sihirli Daktilo hedef kelimeyi hiçbir görünür/erişilebilir alanda göstermez; harfler her tur karışır ve GÖSTER iki denemeden önce açılmaz."])
story += [Spacer(1,4*mm), box("Belge kapsamının sonu", ["Bu PDF yalnız 1. sınıf Türkçe listesindeki t01-t09 oyunlarını kapsar.", "Düzeltmeler oyun kodunu değiştirmez; uygulanacak sahne, ses, mekanik, tur, geri bildirim ve test gereksinimlerini ayrıntılı biçimde tanımlar."], PALE_TEAL, TEAL)]

doc.build(story)
reader = PdfReader(str(OUT))
all_text = "\n".join(page.extract_text() or "" for page in reader.pages)
assert len(games) == 9
assert len(reader.pages) == 16, len(reader.pages)
assert all(game["title"] in all_text for game in games)
print(str(OUT))
print({"pages": len(reader.pages), "games": len(games), "bytes": OUT.stat().st_size})
