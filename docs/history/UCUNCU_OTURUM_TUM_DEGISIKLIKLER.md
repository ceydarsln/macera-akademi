# Macera Akademi — Üçüncü Oturum · Tüm Değişiklikler
9 şablon · 164 oyun · hepsi otomatik botlarla baştan sona oynanarak sınandı.
Bu dosya kusur günlüğünü ve dokuz şablonun DEĞİŞTİRİLMİŞ TAM KAYNAK KODUNU içerir.

---
## 1. BÖLÜM — Kusur günlüğü (bulunan ve düzeltilen her kusur)
# Üçüncü oturum — kusur günlüğü (radar/matbaa/tren/tamirhane/kargo/dedektif/grafik/sirik/radarkod)

## radar-phaser.html · catchDrop (42 oyun)
radar-phaser.html (42 catchDrop oyununun tümü) · yakalama örtüşmeyle karar veriliyordu; kapsüller 120–244px, ekran 480px olduğu için ortaya düşen yanlış kapsülden kaçmak fiziksel olarak imkânsızdı — kusursuz oynayan sınama botu bile can kaybediyor, u33/y03'te oyunu tamamen kaybediyordu · overlap kaldırıldı; kapsülün altına parlak "çekirdek" çizildi, update() içinde merkeze en yakın kapsül seçilip |kapsülX − radarX| ≤ 42 eşiği uygulanıyor (SABLON_KURALLARI §5 "kenara değmek = yakalamak değil")
radar-phaser.html · yeni yakalama kuralı ekranda yazılı değildi, çocuk kutunun kenarını değdirip neden sayılmadığını anlamıyordu · oyun başında 4 saniye görünen "🎯 Kapsülün altındaki sarı noktayı çanağın ortasına getir" ipucu eklendi

## matbaa-phaser.html · sentenceBuild (25 oyun)
matbaa-phaser.html (100 turun 88'i: z61/z04/z31/z34/z22/sb05/sb23/z15/z47 … hepsi) · kızaktaki kartlar tek satıra diziliyordu; toplam genişlik 846px'e çıkarken kızak 452px — kartlar ekran dışına taşıyordu · punto/kart boyu cümlenin GERÇEK genişliğinden seçiliyor (21→15px), kartlar satırlara sarılıyor, kızak yüksekliği tura göre çiziliyor (olculeriSec/satirlaraBol/kizagiCiz)
matbaa-phaser.html (tüm 25 oyun) · kartlar yerçekimiyle masaya dökülüyordu; 8–10 kart 480px masada kilitlenip üst üste biniyordu, dokunulan kart yerine üstte kalan komşu tutuluyordu (z61'de 41 ıskalama üst üste) · her karta yuva verildi (masaYuvalariHesapla), yerçekimi kapatıldı, kartlar yuvasına süzülüyor; yanlış bırakılan kart fırlatılmak yerine yuvasına dönüyor
matbaa-phaser.html · dokunma alanı görselden ±12px genişti, komşu kartın alanı bu kartın merkezini örtüyordu · pay ±4px'e indirildi

## tren-phaser.html · dragSlider (21 oyun)
tren-phaser.html (110 tick: y06 sessiz/fısıltı/normal/bağırma, w11 3/10·1 bütün, w18 "150 ↖ başlangıç" …) · ticks[].label alanı hiç okunmuyordu, çocuk anlamlı ölçek yerine çıplak sayı görüyordu · duraklariUret artık {deger, etiket} döndürüyor; etiket varsa tünelde o yazılıyor, karşılaştırma yine değerle yapılıyor
tren-phaser.html (13 tur: p36 {v}°, y06 {v} / 10, p31 {v} cm …) · cfg.rounds[].format ayrıştırılıyor ama HİÇ kullanılmıyordu; açı oyununda "90" yazıyordu, "90°" değil · etiketi olmayan durakların yazısı format ile üretiliyor, "Seçilen: 90°" olarak gösteriliyor
tren-phaser.html · tünel etiketi sabit 24px yazılıyordu; 5 duraklı turda tünel 86px ve uzun etiketler komşu tünellerin üstüne biniyordu · etiketYaz() genişliğe sığan en büyük puntoyu (23→11px) seçip satır sarıyor

## tamirhane-phaser.html · punctFix (16 oyun)
tamirhane-phaser.html (93 büyük-harf düzeltmesinin 31'i özel ad: y05 ahmet/zeynep, y13 kemal/atatürk/selanik'te, y51 nisan …) · onarılacak sözcüğün altına kırmızı çizgi çiziliyor ve YALNIZ o sözcük titriyordu; hangi sözcüğün özel ad olduğunu bulmak görevin kendisiyken cevap işaretle veriliyordu · kırmızı tamir çizgisi ve titreme kaldırıldı, bütün sözcükler aynı görünüyor
tamirhane-phaser.html · işaret kaldırılınca çocuğun kaç düzeltme aradığını bilmesi gerekiyor · tezgâhın üstüne "Kalan: 🔠 2 büyük harf · ✒️ 1 işaret" sayacı eklendi (hangi sözcük olduğunu söylemiyor)
tamirhane-phaser.html · işaret kartlarının dokunma alanı ±12px payla komşu kartın alanına giriyordu (kartlar 44px, aralık 52px) · pay ±4px'e indirildi

## kargo-phaser.html · codeGrid (15 oyun)
kargo-phaser.html (32 turun 30'u: 6x5, 6x6, 7x6 ızgaralar — w38/y18/y43/y61/z18/z43/p46/h27/h62/sb09/f48/g48) · hücre 88px SABİTTİ; 7x6 ızgara 616x528px ediyor, 480x800 ekranda yanlardan ve program şeridinin üstünden taşıyordu, hücreler/dron/hedef ekran dışında kalıyordu · hücre ölçüsü tur başına hesaplanıyor (izgaraOlcuHesapla: 34–88px arası, banda ortalanıyor), duvar/hedef/dron emojileri de hücreye göre ölçekleniyor
kargo-phaser.html (32 tur) · duvar emojisi r.wallEmoji okunuyor ama çizimde genel '🚧' kullanılıyordu; turun timsah/kaya/dağ/su engeli hiç görünmüyordu · t.duvarEmoji çiziliyor
kargo-phaser.html (32 tur) · gorev ve ipucu aynı alandan (r.hint) besleniyordu, aynı cümle ekranda iki kez yazılıyor ve ızgaraya kalan yeri yiyordu · ikinci satır kaldırıldı, görev yazısı şeridin altına alındı

## dedektif-phaser.html · wordHighlight (14 oyun)
dedektif-phaser.html (9 tur OYNANAMAZ: y26 ×3, z07, z40 ×2, z42 ×2, u26) · cevap metindeki simgeyle TAM eşitlikle karşılaştırılıyordu; cevap "kütüpanede" iken simge "Kütüpanede" (cümle başı), cevap "paşa" iken "paşa," — doğru sözcüğe dokunan çocuk hata alıyor, 3 can bitince oyunu kaybediyordu · anahtar() ile kenar noktalaması atılıp Türkçe küçük harfe çevrilerek karşılaştırılıyor
dedektif-phaser.html (23 tur: u51, u57, y26, y50, z07, z40, z42 …) · rounds[].fixTo (yanlış yazımın doğru hâli: "kütüpanede → Kütüphanede", "festival → şenlik") hiç okunmuyordu; çocuk yanlışı buluyor ama doğrusunu görmüyordu · düzeltilmiş biçim deftere sarı kartla yazılıyor ve "yanlış → doğru" iletisi gösteriliyor
dedektif-phaser.html · defter kartının genişliği kaynak sözcüğün genişliğinden alınıyordu; düzeltilmiş biçim daha uzun olunca yazı kutudan taşıyordu · genişlik yazının gerçek ölçüsünden alınıyor

## grafik-phaser.html · graphBuild (11 oyun)
grafik-phaser.html (w48 hedef 7, g44 hedef 7) · sütun kapasitesi AZAMI 6 SABİTTİ; 7 blok isteyen sütunda 7. blok çizilen oyuğun üstüne taşıyordu · AZAMI verideki en büyük hedeften hesaplanıyor, blok boyu ona göre küçülüyor
grafik-phaser.html (11 oyunun tümü) · hedef sayı üç ayrı yerden ele veriliyordu: sütun etiketi "0 / 5" yazıyor, ızgarada hedef yüksekliğindeki çizgi sarı vurguluyor, depoda tam hedef sayısı kadar blok bulunuyordu — çocuk ekrandaki kaynak veriyi hiç okumuyordu · etiket yalnız geçerli sayıyı gösteriyor, ölçek çizgileri eşitlendi, depo hedef+2 fazlalı blok veriyor
grafik-phaser.html · sürükleme sırasında yalnız EKSİK sütunlar parlıyordu (hangi sütuna blok gerektiğini söylüyordu) · bütün sütunlar bırakma hedefi olarak parlıyor
grafik-phaser.html · sütun dolduğunda "Elma sütunu zaten dolu (5)." iletisi hedefi yazıyordu · "Verilere yeniden bak: Elma sütununda gereken kadar blok var." iletisiyle değiştirildi

## radarkod-phaser.html · numPad (10 oyun)
radarkod-phaser.html (p01 ve p18 — 8 tur, iki oyun baştan sona OYNANAMAZ) · AZAMI_BASAMAK 3 SABİTTİ ama cevaplar 245612, 103020, 500000, 36908, 5634, 3348, 4000, 3766; çocuk cevabı tuşlayamıyordu · basamak sınırı turların gerçek cevaplarından hesaplanıyor (3–7 arası)
radarkod-phaser.html · rakam kartları TUP_X−46+sıra×46 ile diziliyordu; 6 basamakta 230px ediyor, tüp 168px — kartlar tüpün dışına çıkıyordu · aralık ve kart genişliği tüpe sığacak şekilde hesaplanıyor, diziliş tüpün ortasına göre

## Beş şablonda ortak düğme kusuru
radarkod / kargo / tren / grafik / sirik -phaser.html · dugmeYap() geri çağrıyı basma tween'inin SONUNDA çalıştırıyordu (≈180ms); tuş takımında aynı tuşa üst üste basılınca bir basış yutuluyordu (sınamada "500000" yerine "50000" yazıldı) ve her dokunuş 180ms gecikmeyle işliyordu · işlem hemen yapılıyor, tween yalnız görsel geri bildirim olarak kaldı
tren-phaser.html (21 dragSlider oyununun TAMAMI) · tekSatir() TURLAR eşlemesinde çağrılıyor ama şablonda hiç tanımlı değildi; betik yüklenirken ReferenceError verip TURLAR kurulamıyor, oyunlar boş ekranla açılıyordu · duzMetin üzerinden tekSatir() tanımı eklendi
tren-phaser.html (21 oyunun tümü) · turun sonucu fizik çarpışmasıyla belirleniyordu: tren 430px/sn ile 36px'lik tünel ağzından geçiyor, kare gecikmesi 120ms'ye çıkınca bir karede 52px yol alıp ağzı atlıyor ve overlap hiç tetiklenmiyordu — tur sessizce sonuçsuz kalıyor, tren yukarı kaçıp raya dönüyor, çocuk neden bir şey olmadığını anlamıyordu · sonuç ONAYLA anındaki seçimden belirleniyor (sonucuVer/agizBul), uçuş yalnız canlandırma; overlap kaldırıldı
tren-phaser.html · update() içindeki "yukarı kaçan treni geri al" kurtarması onaylandi bayrağını sıfırlamıyordu, tur kilitli kalıyordu · kurtarma kaldırıldı (tren artık serbest uçmuyor)

## radar-phaser.html · ipucu şeridi konumu
radar-phaser.html · yeni eklenen "🎯 çekirdeği ortala" ipucu BOY-128'de radar çanağının üstüne biniyordu (ekran görüntüsünde görüldü) · şerit BOY-205'e taşındı, çanağın tam üstünde duruyor

## grafik-phaser.html · kaynak kutusu taşması
grafik-phaser.html (w48: "1 kitap: 5 · 2 kitap: 7 · 3 kitap: 4 · 4+ kitap: 2" gibi 3 satırlık kaynaklar) · çetele kaynağı kutusu 56px SABİTTİ; uzun metin kutudan taşıp altındaki sütun sayaçlarının ("0 / 0 / 0 / 0") üstüne biniyordu · kutu yüksekliği metnin gerçek ölçüsünden hesaplanıyor, konumu yönerge şeridinin altına bağlandı (seritAlt)

## Sınama kapsamı (otomatik oyuncularla baştan sona oynanarak) — TAMAMLANDI
catchDrop 42/42 · sentenceBuild 25/25 · dragSlider 21/21 · punctFix 16/16 · codeGrid 15/15 · wordHighlight 14/14 · graphBuild 11/11 · numPad 10/10 · jumpPath 10/10
**TOPLAM: 164/164 oyun baştan sona oynanıp completeGame çağrısı doğrulandı.**
Ölçüt: her oyunda otomatik bot oynadı, completeGame çağrısı görüldü (KAYIT.bitti), can kaybı ve kutu/etiket taşması ölçüldü, ekran görüntüsüyle görsel doğrulama yapıldı.
Dokuz şablonun tamamı tek başına da hatasız yükleniyor (konsol hatası yok, veri yapıları kuruluyor).


---
## 2. BÖLÜM — Değiştirilmiş şablonların tam kaynağı
Her şablon `~/Downloads/<ad>-phaser.html` yolundadır ve `aynala.sh` ile
`MaceraAkademi-3/app/src/main/assets/phaser/` altına kopyalanmıştır.


### radar-phaser.html — catchDrop (42 oyun)
Dosya boyu: 35608 bayt · 1010 satır

```html
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<title>Bilim İnsanı Radarı — Phaser 3</title>
<script src="https://cdn.jsdelivr.net/npm/phaser@3.80.1/dist/phaser.min.js"></script>
<style>
  html, body {
    margin: 0; padding: 0; height: 100%;
    background: #10162b; overflow: hidden;
    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
    -webkit-tap-highlight-color: transparent;
    touch-action: none;
  }
  #oyun { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }
  canvas { display: block; }
</style>
</head>
<body>
<div id="oyun"></div>
<script>
/* =====================================================================
   BİLİM İNSANI RADARI — Phaser 3
   ---------------------------------------------------------------------
   Kazanım: FB.3.1.2.b / c / ç — Bilim insanlarının ortak ve ortak olmayan
   özelliklerini belirler.

   Yapı:
     BootScene     → dokular üretilir (dışarıdan resim indirilmez)
     MenuScene     → başlangıç ekranı
     GameScene     → oyun (Arcade Physics)
     GameOverScene → sonuç ekranı

   Not: Görseller Phaser'ın Graphics API'siyle çalışma anında üretiliyor.
   Uygulama çevrimdışı bir kabuk (APK / iOS) içinde çalıştığı ve dış
   adreslere erişemediği için internetten resim çekmek yerine bu yol seçildi.
   ===================================================================== */

const EN  = 480;   /* oyun genişliği  */
const BOY = 800;   /* oyun yüksekliği */

const RENK = {
  gokUst:   0x2b3a67,
  gokAlt:   0x6f86c9,
  dogru:    0x34c47b,
  yanlis:   0xf07575,
  notr:     0xfdfdff,
  metin:    '#17323b',
  vurgu:    0xffd166,
  radar:    0x4a7fd6
};

/* Oyunun içeriği — mevcut oyundaki metinlerin aynısı */
/* ---------------- uygulama köprüsü ----------------
   Adres  radar.html#oyun=u04  biçiminde; katalog verisi üst pencereden
   okunuyor. 42 catchDrop oyunu bu şablonla oynanıyor.                  */
const KOPRU = (function(){
  try{
    const p = new URLSearchParams(location.hash.slice(1));
    const id = p.get('oyun');
    if (id && window.parent && window.parent !== window &&
        typeof window.parent.getGame === 'function'){
      const g = window.parent.getGame(id);
      if (g && g.cfg) return {
        oyun: g, cfg: g.cfg,
        bitir(mesaj, puan){ try{ window.parent.completeGame(mesaj || '', puan); }catch(e){} },
        /* Turun kendi metnini uygulamanın sesiyle okutur (Piper). */
        oku(metin){ try{ if (window.parent.oku) window.parent.oku(metin); }catch(e){} },
        /* Kaybetme ekranından: bu oyunu bırak, sıradakine geç. */
        atla(){ try{ if (window.parent.sonrakiOyunaGec) window.parent.sonrakiOyunaGec(); }catch(e){} }
      };
    }
  }catch(e){ /* çapraz kaynak engeli: tek başına oynanır */ }
  return null;
})();

/* HTML varlıklarını çöz: katalogda "Pay &lt; payda" gibi yazımlar var,
   çözülmezse ekranda "&lt;" olarak görünüyor ve öyle okunuyor. */
function varlikCoz(m){
  return String(m)
    .replace(/&nbsp;/gi, ' ')
    .replace(/&lt;/gi, '<').replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"').replace(/&#39;|&apos;/gi, "'")
    .replace(/&hellip;/gi, '…').replace(/&mdash;/gi, '—').replace(/&ndash;/gi, '–')
    .replace(/&times;/gi, '×').replace(/&divide;/gi, '÷').replace(/&deg;/gi, '°')
    .replace(/&rarr;/gi, '→').replace(/&larr;/gi, '←')
    .replace(/&amp;/gi, '&');            /* en sona: çift çözmeyi önler */
}

function duzMetin(x){
  return varlikCoz(String(x == null ? '' : x).replace(/<br\s*\/?>/gi,' ')
    .replace(/<[^>]+>/g,'')).replace(/[“”]/g,'"').replace(/\s+/g,' ').trim();
}

const VARSAYILAN = {
  instruction:'Doğru cevabı radarla yakala',
  catcher:'📡', catcherName:'radarı',
  rounds:[
    { sentence:'Bütün bilim insanlarında bulunan özellik nedir?', need:'Meraklı olmak',
      wrong:['Aynı ülkede doğmak','Aynı yaşta olmak','Aynı dili konuşmak'],
      wrongHint:'Ülke, yaş ve dil farklı olabilir — ortak özellik meraklı olmak!' },
    { sentence:'Deneyi ilk seferde başarısız olan bilim insanı ne yapar?', need:'Tekrar dener',
      wrong:['Hemen vazgeçer','Sonucu değiştirir','Başkasını suçlar'],
      wrongHint:'Bilim insanı sabırlıdır, tekrar dener!' },
    { sentence:'Bilim insanı bulgularını ne yapar?', need:'Başkalarıyla paylaşır',
      wrong:['Gizli tutar','Yakar','Sadece kendine saklar'],
      wrongHint:'Bilim paylaşarak ilerler!' },
    { sentence:'Yeni bir kanıt bulunduğunda bilim insanı ne yapar?', need:'Fikrini gözden geçirir',
      wrong:['Kanıtı saklar','Eski fikrinde ısrar eder','Konuyu bırakır'],
      wrongHint:'Bilim insanı açık görüşlüdür!' } ]
};

const CFG = KOPRU ? KOPRU.cfg : VARSAYILAN;

/* Yakalayıcı katalogdan geliyor: şemsiye, kova, kalkan, radar… Oyunun
   kendi temasını korumak için tabak görselinin üstüne o emoji konuyor. */
const YAKALAYICI     = CFG.catcher || '📡';
const YAKALAYICI_ADI = duzMetin(CFG.catcherName) || 'yakalayıcıyı';

const SORULAR = (CFG.rounds || []).map(t => ({
  seslen: duzMetin(t.say) || duzMetin(t.sentence || t.prompt),
  soru:   duzMetin(t.sentence || t.prompt),
  emoji:  YAKALAYICI,
  dogru:  duzMetin(t.need),
  yanlis: (t.wrong || []).map(duzMetin),
  ipucu:  duzMetin(t.wrongHint)
}));

const OYUN_ADI = KOPRU ? duzMetin(KOPRU.oyun.title) : 'RADAR YAKALAMA';
const OYUN_EMO = KOPRU ? (KOPRU.oyun.emo || '📡') : '📡';
const TALIMAT  = duzMetin(CFG.instruction) || ('Doğru cevabı ' + YAKALAYICI_ADI + ' ile yakala');
const BASARI   = duzMetin(CFG.successMsg) || 'Hepsini doğru yakaladın!';

const CAN_SAYISI = 3;

/* --- Tempo ayarları ---------------------------------------------------
   DUSUS_HIZI : kapsülün azami düşüş hızı (px/sn). 800px'lik ekranı
                geçmesi ≈ 800 / DUSUS_HIZI saniye sürer.
   ARALIK     : iki kapsül arasındaki bekleme (ms) — okumaya zaman tanır.
   ILK_BEKLEME: soru göründükten sonra ilk kapsülün düşmesine kadar. */
/* Çanağın ağzı 120px; çekirdeğin merkeze bu kadar yakın olması gerekiyor.
   Örtüşme ölçütü kullanılmıyor (bkz. GameScene.update). */
const YAKALAMA_ESIGI = 42;
const DUSUS_HIZI  = 78;
const ARALIK      = 2000;
const ILK_BEKLEME = 1200;

/* =====================================================================
   1) BOOT — dokuları üret
   ===================================================================== */
class BootScene extends Phaser.Scene {
  constructor() { super('Boot'); }

  create() {
    this.dokuKivilcim();
    this.dokuToz();
    this.dokuRadar();
    this.dokuGolge();
    /* Uygulama içinde çocuk oyunu listeden zaten seçti; menüyü atla. */
    this.scene.start(KOPRU ? 'Game' : 'Menu');
  }

  /* Küçük parlak nokta — doğru cevap patlaması için */
  dokuKivilcim() {
    const g = this.make.graphics({ add: false });
    g.fillStyle(0xffffff, 1);
    g.fillCircle(8, 8, 8);
    g.generateTexture('kivilcim', 16, 16);
    g.destroy();
  }

  /* Yumuşak gri yuvarlak — toz/duman için */
  dokuToz() {
    const g = this.make.graphics({ add: false });
    for (let r = 14; r > 0; r--) {
      g.fillStyle(0xffffff, 0.06);
      g.fillCircle(14, 14, r);
    }
    g.generateTexture('toz', 28, 28);
    g.destroy();
  }

  /* Radar çanağı — oyuncunun kontrol ettiği nesne */
  dokuRadar() {
    const W = 132, H = 72;
    const g = this.make.graphics({ add: false });

    /* ayak */
    g.fillStyle(0x35507f, 1);
    g.fillRoundedRect(W / 2 - 9, 38, 18, 30, 5);
    g.fillStyle(0x2a4068, 1);
    g.fillRoundedRect(W / 2 - 26, 62, 52, 10, 5);

    /* çanak */
    g.fillStyle(RENK.radar, 1);
    g.beginPath();
    g.arc(W / 2, 44, 58, Phaser.Math.DegToRad(200), Phaser.Math.DegToRad(340), false);
    g.closePath();
    g.fillPath();

    /* çanak iç dolgusu */
    g.fillStyle(0x7fb2f0, 1);
    g.beginPath();
    g.arc(W / 2, 44, 44, Phaser.Math.DegToRad(203), Phaser.Math.DegToRad(337), false);
    g.closePath();
    g.fillPath();

    /* parlama */
    g.fillStyle(0xdfeeff, 0.75);
    g.beginPath();
    g.arc(W / 2, 44, 24, Phaser.Math.DegToRad(206), Phaser.Math.DegToRad(300), false);
    g.closePath();
    g.fillPath();

    g.generateTexture('radar', W, H);
    g.destroy();
  }

  /* Zemin çizgisi için ince gölge */
  dokuGolge() {
    const g = this.make.graphics({ add: false });
    g.fillStyle(0x000000, 0.18);
    g.fillEllipse(40, 8, 80, 16);
    g.generateTexture('golge', 80, 16);
    g.destroy();
  }
}

/* =====================================================================
   Ortak: arka plan gökyüzü + yıldızlar
   ===================================================================== */
function gokyuzuCiz(scene) {
  const g = scene.add.graphics();
  g.fillGradientStyle(RENK.gokUst, RENK.gokUst, RENK.gokAlt, RENK.gokAlt, 1);
  g.fillRect(0, 0, EN, BOY);

  /* hafifçe parlayan yıldızlar */
  for (let i = 0; i < 40; i++) {
    const s = scene.add.circle(
      Phaser.Math.Between(10, EN - 10),
      Phaser.Math.Between(10, BOY - 120),
      Phaser.Math.FloatBetween(1, 2.4),
      0xffffff,
      Phaser.Math.FloatBetween(0.25, 0.8)
    );
    scene.tweens.add({
      targets: s,
      alpha: 0.1,
      duration: Phaser.Math.Between(900, 2200),
      yoyo: true,
      repeat: -1,
      delay: Phaser.Math.Between(0, 1500)
    });
  }
  return g;
}

/* =====================================================================
   2) MENU
   ===================================================================== */
class MenuScene extends Phaser.Scene {
  constructor() { super('Menu'); }

  create() {
    gokyuzuCiz(this);

    this.add.text(EN / 2, 180, YAKALAYICI, { fontSize: '97px' }).setOrigin(0.5);

    const baslik = this.add.text(EN / 2, 290, OYUN_ADI, {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '46px',
      fontStyle: 'bold',
      color: '#ffffff',
      align: 'center',
      lineSpacing: 6
    }).setOrigin(0.5);

    /* başlık hafifçe nefes alsın */
    this.tweens.add({
      targets: baslik,
      scale: 1.04,
      duration: 1400,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut'
    });

    this.add.text(EN / 2, 392, TALIMAT, {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '24px',
      color: '#cfe0ff',
      align: 'center',
      lineSpacing: 5
    }).setOrigin(0.5);

    /* Başla düğmesi */
    const dugme = this.add.container(EN / 2, 520);
    const zemin = this.add.graphics();
    zemin.fillStyle(RENK.dogru, 1);
    zemin.fillRoundedRect(-130, -34, 260, 68, 34);
    zemin.fillStyle(0xffffff, 0.18);
    zemin.fillRoundedRect(-130, -34, 260, 26, { tl: 34, tr: 34, bl: 0, br: 0 });
    const yazi = this.add.text(0, 0, '▶  BAŞLA', {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '29px',
      fontStyle: 'bold',
      color: '#ffffff'
    }).setOrigin(0.5);
    dugme.add([zemin, yazi]);
    dugme.setSize(260, 68).setInteractive({ useHandCursor: true });

    dugme.on('pointerover', () => this.tweens.add({ targets: dugme, scale: 1.06, duration: 120 }));
    dugme.on('pointerout',  () => this.tweens.add({ targets: dugme, scale: 1.0,  duration: 120 }));
    dugme.on('pointerdown', () => {
      this.tweens.add({
        targets: dugme, scale: 0.92, duration: 90, yoyo: true,
        onComplete: () => this.scene.start('Game')
      });
    });

    this.add.text(EN / 2, 700, `${SORULAR.length} soru  ·  ${CAN_SAYISI} can`, {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '20px',
      color: '#9fb4e6'
    }).setOrigin(0.5);
  }
}

/* =====================================================================
   3) GAME — Arcade Physics
   ===================================================================== */
class GameScene extends Phaser.Scene {
  constructor() { super('Game'); }

  create() {
    /* --- durum --- */
    this.soruIndex = 0;
    this.can       = CAN_SAYISI;
    this.puan      = 0;
    this.seri      = 0;
    this.kilit     = false;   /* cevap işlenirken ikinci çarpışmayı engelle */
    this.dususHizi = DUSUS_HIZI;
    this.aralik    = ARALIK;

    gokyuzuCiz(this);

    /* --- zemin (görünmez fizik gövdesi) --- */
    /* NOT: Phaser'da collider/overlap(grup, TEK nesne) çağrılırsa
       callback'e parametreler TERS gelir — (tekNesne, grupElemani).
       Zemin bu yüzden staticGroup içinde tutuluyor: grup-vs-grup
       kullanınca sıra (obj1Elemani, obj2Elemani) olarak korunuyor. */
    this.zemin = this.physics.add.staticGroup();
    this.zemin.add(
      this.physics.add.staticImage(EN / 2, BOY - 6, 'golge')
        .setVisible(false)
        .setDisplaySize(EN, 12)
        .refreshBody()
    );

    this.add.rectangle(EN / 2, BOY - 4, EN, 8, 0x1b2440, 1);

    /* --- parçacık yayıcılar --- */
    this.kivilcimlar = this.add.particles(0, 0, 'kivilcim', {
      speed: { min: 140, max: 380 },
      angle: { min: 0, max: 360 },
      scale: { start: 0.9, end: 0 },
      alpha: { start: 1, end: 0 },
      lifespan: 650,
      gravityY: 420,
      blendMode: 'ADD',
      emitting: false
    }).setDepth(50);

    this.tozlar = this.add.particles(0, 0, 'toz', {
      speed: { min: 40, max: 140 },
      angle: { min: 200, max: 340 },
      scale: { start: 1.1, end: 2.2 },
      alpha: { start: 0.55, end: 0 },
      lifespan: 700,
      emitting: false
    }).setDepth(40);

    /* --- radar (oyuncu) --- */
    this.radar = this.physics.add.image(EN / 2, BOY - 78, 'radar');
    this.radar.setImmovable(true);
    this.radar.body.setAllowGravity(false);
    this.radar.body.setSize(120, 40).setOffset(6, 6);
    this.radar.setDepth(20);
    this.radar.setCollideWorldBounds(true);

    /* Oyunun kendi yakalayıcısı (şemsiye, kova, kalkan…) tabağın üstünde
       duruyor ve update() içinde onu takip ediyor. */
    this.yakalayiciYazi = this.add.text(this.radar.x, this.radar.y - 4, YAKALAYICI,
      { fontSize: '36px' }).setOrigin(0.5).setDepth(21);

    /* sürükleme: parmağı/fareyi takip et */
    this.input.on('pointermove', (p) => {
      if (!p.isDown && this.input.activePointer.wasTouch) return;
      this.hedefX = Phaser.Math.Clamp(imlec(p).x, 70, EN - 70);
    });
    this.input.on('pointerdown', (p) => {
      this.hedefX = Phaser.Math.Clamp(imlec(p).x, 70, EN - 70);
    });
    this.hedefX = this.radar.x;

    /* klavye (masaüstünde denemek için) */
    this.tuslar = this.input.keyboard.createCursorKeys();

    /* --- düşen cevaplar --- */
    this.cevaplar = this.physics.add.group();

    /* Yakalama örtüşmeyle KARAR VERİLMİYOR. Kapsüller 120–244px genişliğinde;
       480px'lik ekranda ortaya düşen geniş bir kapsülden örtüşmeyle kaçmak
       fiziksel olarak imkânsızdı (kusursuz oynayan sınama botu bile can
       kaybediyor, hatta oyunu kaybediyordu). Artık kapsülün ALTINDAKİ
       çekirdek çanağa girmek zorunda: update() içinde merkeze en yakın
       kapsül seçiliyor ve YAKALAMA_ESIGI eşiği uygulanıyor. */
    this.physics.add.collider(this.cevaplar, this.zemin, this.yereDustu, null, this);

    this.arayuzKur();
    this.ipucuGoster();
    this.soruyuBaslat();
  }

  /* ---------- Arayüz (HUD) ---------- */
  arayuzKur() {
    /* Üst şerit. Katalogda cümle 99 karaktere çıkıyor; şerit sabit
       yükseklikte kalınca yazı HUD satırının üstüne biniyordu, bu yüzden
       şerit en uzun cümlenin gerçek yüksekliğine göre çiziliyor. */
    let enUzun = '';
    SORULAR.forEach(x => { if (x.soru.length > enUzun.length) enUzun = x.soru; });
    const olcu = this.add.text(0, 0, YAKALAYICI + '  ' + enUzun, {
      fontFamily: 'system-ui, sans-serif', fontSize: '22px', fontStyle: 'bold',
      align: 'center', wordWrap: { width: EN - 60 }, lineSpacing: 4
    }).setVisible(false);
    const yaziBoy = olcu.height; olcu.destroy();

    const seritBoy = Math.max(128, yaziBoy + 74);
    const serit = this.add.graphics().setDepth(60);
    serit.fillStyle(0x0f1730, 0.97);   /* opak: düşen kapsüller altından sızmasın */
    serit.fillRoundedRect(10, 10, EN - 20, seritBoy, 18);
    const satirY = 10 + seritBoy - 26;

    this.soruYazi = this.add.text(EN / 2, 20 + yaziBoy / 2, '', {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '22px',
      fontStyle: 'bold',
      color: '#ffffff',
      align: 'center',
      wordWrap: { width: EN - 60 },
      lineSpacing: 4
    }).setOrigin(0.5).setDepth(61);

    this.puanYazi = this.add.text(30, satirY, 'Puan 0', {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '21px',
      fontStyle: 'bold',
      color: '#ffd166'
    }).setOrigin(0, 0.5).setDepth(61);

    this.canYazi = this.add.text(EN - 30, satirY, '❤️❤️❤️', {
      fontSize: '21px'
    }).setOrigin(1, 0.5).setDepth(61);

    this.ilerlemeYazi = this.add.text(EN / 2, satirY, '', {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '19px',
      fontStyle: 'bold',
      color: '#9fb4e6'
    }).setOrigin(0.5).setDepth(61);

    /* seri (combo) rozeti */
    this.seriYazi = this.add.text(EN / 2, seritBoy + 34, '', {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '24px',
      fontStyle: 'bold',
      color: '#ffd166'
    }).setOrigin(0.5).setDepth(61).setAlpha(0);
  }

  /* Yakalama artık çekirdek hizalamasıyla; kural ekranda yazılı olmazsa
     çocuk kutunun kenarını değdirip neden sayılmadığını anlamıyor. */
  ipucuGoster() {
    /* Şerit çanağın ÜSTÜNDE kalmalı: BOY-128'de tabağın ağzını örtüyordu. */
    const t = this.add.text(EN / 2, BOY - 205,
      '🎯 Kapsülün altındaki sarı noktayı çanağın ortasına getir', {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '17px',
      fontStyle: 'bold',
      color: '#ffe9a8',
      backgroundColor: '#1b2440',
      padding: { x: 10, y: 7 },
      align: 'center',
      wordWrap: { width: EN - 60 }
    }).setOrigin(0.5).setDepth(62);
    this.tweens.add({ targets: t, alpha: 0, delay: 4200, duration: 900,
      onComplete: () => t.destroy() });
  }

  arayuzuTazele() {
    this.puanYazi.setText('Puan ' + this.puan);
    this.canYazi.setText('❤️'.repeat(Math.max(0, this.can)) + '🖤'.repeat(Math.max(0, CAN_SAYISI - this.can)));
    this.ilerlemeYazi.setText(`${Math.min(this.soruIndex + 1, SORULAR.length)} / ${SORULAR.length}`);
  }

  /* ---------- Soru döngüsü ---------- */
  soruyuBaslat() {
    const s = SORULAR[this.soruIndex];
    this.soruYazi.setText(s.emoji + '  ' + s.soru);
    /* turun kendi metnini uygulamanın sesiyle okut */
    if (KOPRU) KOPRU.oku(s.seslen);
    this.arayuzuTazele();
    this.kilit = false;

    /* Zorluk basamağı: ilk sorular çok sakin, sonrakiler biraz canlanıyor.
       Yine de en hızlı hâlinde bile ekranı geçmek ~6 saniye sürüyor. */
    this.dususHizi = DUSUS_HIZI + this.soruIndex * 6;   /* px/sn üst sınır */
    this.aralik    = Math.max(1500, ARALIK - this.soruIndex * 100); /* ms */

    /* soru yazısı yumuşakça belirsin */
    this.soruYazi.setAlpha(0).setScale(0.9);
    this.tweens.add({
      targets: this.soruYazi, alpha: 1, scale: 1,
      duration: 260, ease: 'Back.easeOut'
    });

    /* cevapları karıştırıp sırayla düşür */
    const liste = Phaser.Utils.Array.Shuffle([
      { metin: s.dogru, dogruMu: true },
      ...s.yanlis.map(m => ({ metin: m, dogruMu: false }))
    ]);

    this.dusenSayisi = 0;
    if (this.dusurucu) this.dusurucu.remove();
    if (this.ilkBekleme) this.ilkBekleme.remove();

    /* Önce soruyu okusun, sonra kapsüller gelmeye başlasın */
    this.ilkBekleme = this.time.delayedCall(ILK_BEKLEME, () => {
      this.dusurucu = this.time.addEvent({
        delay: this.aralik,
        repeat: liste.length - 1,
        startAt: this.aralik,          /* ilki hemen düşsün, sonrakiler aralıklı */
        callback: () => {
          const c = liste[this.dusenSayisi++];
          if (c) this.cevapDusur(c.metin, c.dogruMu);
        }
      });
    });
  }

  /* Bir cevap kapsülü oluştur ve yerçekimiyle bırak */
  cevapDusur(metin, dogruMu) {
    const yazi = this.add.text(0, 0, metin, {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '20px',
      fontStyle: 'bold',
      color: RENK.metin,
      align: 'center',
      wordWrap: { width: 210 }
    }).setOrigin(0.5);

    const W = Math.min(EN - 40, Math.max(120, yazi.width + 34));
    const H = Math.max(48, yazi.height + 24);

    const kap = this.add.graphics();
    kap.fillStyle(RENK.notr, 1);
    kap.fillRoundedRect(-W / 2, -H / 2, W, H, H / 2);
    kap.lineStyle(3, 0xd8e2f5, 1);
    kap.strokeRoundedRect(-W / 2, -H / 2, W, H, H / 2);

    const x = Phaser.Math.Between(W / 2 + 14, EN - W / 2 - 14);
    const kapsul = this.add.container(x, -H, [kap, yazi]);
    kapsul.setSize(W, H);
    kapsul.setDepth(10);

    /* --- Arcade Physics gövdesi ---
       ÖNEMLİ: gruba ekleme İLK sırada olmalı. Phaser'ın Arcade Group'u
       add() sırasında kendi varsayılanlarını (gravity, bounce, drag…)
       gövdeye uyguluyor; önce ayar yapıp sonra eklersek ayarlar siliniyor. */
    this.cevaplar.add(kapsul);
    /* Container gövdesi container'ın orijininde merkezlenir; ek offset
       verilirse çarpışma kutusu görselden kayar. */
    kapsul.body.setSize(W, H);
    /* Düşüş HIZI çocuğun okuyup karar verebileceği kadar yavaş olmalı.
       Yerçekimi açık kalıyor ama azami hızı sınırlıyoruz: kapsül kısa sürede
       "son hıza" ulaşıp sabit ve okunabilir bir tempoyla süzülüyor.
       Ekranı geçme süresi ≈ 800px / DUSUS_HIZI saniye. */
    kapsul.body.setVelocity(Phaser.Math.Between(-14, 14), 0);
    kapsul.body.setGravityY(90);
    kapsul.body.setMaxVelocity(70, this.dususHizi);
    kapsul.body.setBounce(0.45, 0.30);
    kapsul.body.setDragX(18);
    kapsul.body.setCollideWorldBounds(true);
    kapsul.body.onWorldBounds = false;

    /* Yakalama çekirdeği: kapsülün altından sarkan parlak nokta. Çanağa
       giren şey bu; çocuk kutunun kenarını değil çekirdeğini hizalıyor.
       Kutu ne kadar geniş olursa olsun kaçmak da hizalamak da mümkün. */
    const cekirdek = this.add.graphics();
    cekirdek.fillStyle(dogruMu ? RENK.vurgu : RENK.vurgu, 1);
    cekirdek.fillCircle(0, H / 2 + 6, 9);
    cekirdek.lineStyle(3, 0x8a6a12, 1);
    cekirdek.strokeCircle(0, H / 2 + 6, 9);
    cekirdek.fillStyle(0xffffff, 0.6);
    cekirdek.fillCircle(-3, H / 2 + 3, 3);
    kapsul.add(cekirdek);

    kapsul.setData('dogruMu', dogruMu);
    kapsul.setData('metin', metin);
    kapsul.setData('en', W);
    kapsul.setData('boy', H);

    /* düşerken hafif salınım */
    this.tweens.add({
      targets: kapsul,
      angle: Phaser.Math.Between(-7, 7),
      duration: 900,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut'
    });
  }

  /* ---------- Çarpışmalar ---------- */
  yakala(kapsul) {
    /* Bir kapsül yalnız bir kez sayılır: eşik bölgesinde birkaç kare
       kalabiliyor (tek hatada üç can birden giderdi). */
    if (this.kilit || !kapsul.active || kapsul.getData('yakalandi')) return;
    kapsul.setData('yakalandi', true);

    if (kapsul.getData('dogruMu')) {
      this.kilit = true;
      this.dogruCevap(kapsul);
    } else {
      this.yanlisCevap(kapsul);
    }
  }

  dogruCevap(kapsul) {
    const x = kapsul.x, y = kapsul.y;

    /* 🎉 kıvılcım patlaması */
    this.kivilcimlar.setParticleTint(RENK.dogru);
    this.kivilcimlar.explode(34, x, y);

    /* puan: seri arttıkça daha çok */
    this.seri++;
    const kazanc = 100 + (this.seri - 1) * 25;
    this.puan += kazanc;

    /* radar sevinç zıplaması + squash */
    this.tweens.add({
      targets: this.radar,
      scaleX: 1.22, scaleY: 0.82,
      duration: 110, yoyo: true, ease: 'Quad.easeOut'
    });

    /* skor yazısı büyüyüp küçülsün */
    this.puanYazi.setText('Puan ' + this.puan);
    this.tweens.add({
      targets: this.puanYazi,
      scale: 1.55,
      duration: 140,
      yoyo: true,
      ease: 'Back.easeOut'
    });

    /* uçan +puan yazısı */
    const ucan = this.add.text(x, y, '+' + kazanc, {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '33px',
      fontStyle: 'bold',
      color: '#7ce0a3'
    }).setOrigin(0.5).setDepth(70);
    this.tweens.add({
      targets: ucan, y: y - 90, alpha: 0, scale: 1.3,
      duration: 750, ease: 'Cubic.easeOut',
      onComplete: () => ucan.destroy()
    });

    if (this.seri >= 2) this.seriGoster();

    this.cameras.main.flash(150, 90, 220, 150);
    this.temizleVeIlerle();
  }

  yanlisCevap(kapsul) {
    /* kapsül sekerek geri fırlasın */
    kapsul.body.setVelocityY(-380);
    kapsul.body.setVelocityX(Phaser.Math.Between(-220, 220));

    this.tozlar.explode(16, kapsul.x, kapsul.y);

    /* 📷 kamera sarsıntısı + kırmızı çakma */
    this.cameras.main.shake(220, 0.012);
    this.cameras.main.flash(180, 220, 90, 90);

    this.can--;
    this.seri = 0;
    this.arayuzuTazele();

    /* can yazısı sallansın */
    this.tweens.add({
      targets: this.canYazi,
      angle: { from: -12, to: 12 },
      duration: 70, yoyo: true, repeat: 3,
      onComplete: () => this.canYazi.setAngle(0)
    });

    const uyari = this.add.text(EN / 2, BOY / 2, SORULAR[this.soruIndex].ipucu, {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '21px',
      fontStyle: 'bold',
      color: '#ffffff',
      backgroundColor: '#b5453b',
      padding: { x: 14, y: 10 },
      align: 'center',
      wordWrap: { width: EN - 80 }
    }).setOrigin(0.5).setDepth(80).setAlpha(0);
    this.tweens.add({ targets: uyari, alpha: 1, duration: 150 });
    this.time.delayedCall(1500, () => {
      this.tweens.add({
        targets: uyari, alpha: 0, duration: 250,
        onComplete: () => uyari.destroy()
      });
    });

    if (this.can <= 0) {
      this.kilit = true;
      this.time.delayedCall(700, () => this.bitir(false));
    }
  }

  /* Doğru cevap kaçıp yere düştüyse: yeniden gönder */
  yereDustu(kapsul, zemin) {
    /* yerde zıpladıktan sonra kaybolsun */
    if (!kapsul.getData('silinecek')) {
      kapsul.setData('silinecek', true);
      this.tozlar.explode(8, kapsul.x, kapsul.y + 10);
      this.time.delayedCall(650, () => {
        if (!kapsul.active) return;
        const dogruMu = kapsul.getData('dogruMu');
        const metin = kapsul.getData('metin');
        kapsul.destroy();
        /* doğru cevabı kaçırdıysa tekrar düşür ki oyun tıkanmasın */
        if (dogruMu === true && !this.kilit) this.cevapDusur(metin, true);
      });
    }
  }

  seriGoster() {
    this.seriYazi.setText('🔥 ' + this.seri + ' SERİ!').setAlpha(1).setScale(0.6);
    this.tweens.add({
      targets: this.seriYazi,
      scale: 1, duration: 220, ease: 'Back.easeOut'
    });
    this.tweens.add({
      targets: this.seriYazi,
      alpha: 0, delay: 900, duration: 400
    });
  }

  temizleVeIlerle() {
    if (this.dusurucu) this.dusurucu.remove();
    if (this.ilkBekleme) this.ilkBekleme.remove();

    /* ekrandaki kapsülleri toplayarak yok et */
    this.cevaplar.getChildren().slice().forEach((k, i) => {
      this.tweens.add({
        targets: k,
        alpha: 0, scale: 0.4,
        duration: 260, delay: i * 40,
        onComplete: () => k.destroy()
      });
    });

    this.time.delayedCall(700, () => {
      this.soruIndex++;
      if (this.soruIndex >= SORULAR.length) this.bitir(true);
      else this.soruyuBaslat();
    });
  }

  bitir(kazandi) {
    /* Uygulama içindeyken kazanma ekranını uygulama gösteriyor: XP, altın,
       kutlama ve sıradaki oyuna otomatik geçiş onun akışında. */
    if (kazandi && KOPRU){ KOPRU.bitir(BASARI, this.puan); return; }
    this.scene.start('GameOver', { kazandi, puan: this.puan, can: this.can });
  }

  /* ---------- Her karede ---------- */
  update() {
    /* klavye desteği */
    if (this.tuslar.left.isDown)  this.hedefX = Phaser.Math.Clamp(this.hedefX - 9, 70, EN - 70);
    if (this.tuslar.right.isDown) this.hedefX = Phaser.Math.Clamp(this.hedefX + 9, 70, EN - 70);

    /* radar hedefe yumuşakça kaysın (ani sıçrama olmasın) */
    const fark = this.hedefX - this.radar.x;
    this.radar.body.setVelocityX(fark * 11);

    /* yakalayıcı emojisi tabakla birlikte kaysın */
    if (this.yakalayiciYazi) this.yakalayiciYazi.setX(this.radar.x);

    /* --- yakalama ölçütü: çekirdek çanağa girdi mi? ---
       Çanağın ağzı radar.y - 30 ile radar.y + 22 arasında. Çekirdek bu
       şeride girdiğinde ve merkez farkı eşiğin altındaysa yakalanır.
       Birden çok kapsül aynı anda uygunsa merkeze EN YAKIN olan seçilir. */
    if (!this.kilit){
      let sec = null, enYakin = 1e9;
      this.cevaplar.getChildren().forEach(k => {
        if (!k.active || k.getData('yakalandi')) return;
        const cy = k.y + (k.getData('boy') || k.height) / 2 + 6;   /* çekirdek merkezi */
        if (cy < this.radar.y - 30 || cy > this.radar.y + 22) return;
        const d = Math.abs(k.x - this.radar.x);
        if (d <= YAKALAMA_ESIGI && d < enYakin){ enYakin = d; sec = k; }
      });
      if (sec) this.yakala(sec);
    }

    /* ekranın altından kaçan kapsülleri temizle */
    this.cevaplar.getChildren().slice().forEach(k => {
      if (k.y > BOY + 120) k.destroy();
    });
  }
}

/* =====================================================================
   4) GAME OVER
   ===================================================================== */
class GameOverScene extends Phaser.Scene {
  constructor() { super('GameOver'); }

  init(veri) {
    this.kazandi = !!veri.kazandi;
    this.puan    = veri.puan || 0;
    this.canKalan = veri.can || 0;
  }

  create() {
    gokyuzuCiz(this);

    const emoji = this.kazandi ? '🏆' : '💪';
    const baslik = this.kazandi ? 'RADAR TAMAM!' : 'TEKRAR DENE';
    const altYazi = this.kazandi
      ? 'Bilim insanlarının ortak\nözelliklerini keşfettin'
      : 'Bilim insanı sabırlıdır —\nsen de tekrar dene!';

    const ikon = this.add.text(EN / 2, 190, emoji, { fontSize: '101px' }).setOrigin(0.5).setScale(0);
    this.tweens.add({ targets: ikon, scale: 1, duration: 520, ease: 'Back.easeOut' });

    this.add.text(EN / 2, 300, baslik, {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '40px', fontStyle: 'bold', color: '#ffffff'
    }).setOrigin(0.5);

    this.add.text(EN / 2, 372, altYazi, {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '22px', color: '#cfe0ff', align: 'center', lineSpacing: 5
    }).setOrigin(0.5);

    /* puan sayacı sıfırdan yukarı saysın */
    const puanYazi = this.add.text(EN / 2, 470, 'Puan 0', {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '36px', fontStyle: 'bold', color: '#ffd166'
    }).setOrigin(0.5);

    const sayac = { v: 0 };
    this.tweens.add({
      targets: sayac, v: this.puan,
      duration: 900, ease: 'Cubic.easeOut',
      onUpdate: () => puanYazi.setText('Puan ' + Math.round(sayac.v)),
      onComplete: () => {
        this.tweens.add({ targets: puanYazi, scale: 1.3, duration: 160, yoyo: true, ease: 'Back.easeOut' });
        if (this.kazandi) this.konfeti();
      }
    });

    this.add.text(EN / 2, 522, `Kalan can: ${'❤️'.repeat(this.canKalan) || '—'}`, {
      fontFamily: 'system-ui, sans-serif', fontSize: '20px', color: '#9fb4e6'
    }).setOrigin(0.5);

    this.dugmeYap(EN / 2, 610, '🔁  TEKRAR OYNA', RENK.dogru, () => this.scene.start('Game'));

    /* Uygulama içinde: bu oyunda takılan çocuk sıradakine geçebilsin. */

    if (KOPRU) this.dugmeYap(EN / 2, 684, '⏭  SIRADAKİ OYUN', 0x4a679e, () => KOPRU.atla());
    if (!KOPRU) this.dugmeYap(EN / 2, 692, '🏠  ANA MENÜ', 0x4a7fd6, () => this.scene.start('Menu'));
  }

  konfeti() {
    const p = this.add.particles(0, 0, 'kivilcim', {
      x: { min: 0, max: EN },
      y: -20,
      speedY: { min: 120, max: 300 },
      speedX: { min: -60, max: 60 },
      scale: { start: 0.8, end: 0.2 },
      lifespan: 2600,
      quantity: 3,
      frequency: 90,
      tint: [0xffd166, 0x7ce0a3, 0xff9db0, 0x7ad7ff]
    }).setDepth(90);
    this.time.delayedCall(2200, () => p.stop());
  }

  dugmeYap(x, y, metin, renk, geriCagri) {
    const c = this.add.container(x, y);
    const g = this.add.graphics();
    g.fillStyle(renk, 1);
    g.fillRoundedRect(-140, -30, 280, 60, 30);
    g.fillStyle(0xffffff, 0.16);
    g.fillRoundedRect(-140, -30, 280, 24, { tl: 30, tr: 30, bl: 0, br: 0 });
    const t = this.add.text(0, 0, metin, {
      fontFamily: 'system-ui, sans-serif',
      fontSize: '25px', fontStyle: 'bold', color: '#ffffff'
    }).setOrigin(0.5);
    c.add([g, t]);
    c.setSize(280, 60).setInteractive({ useHandCursor: true });
    c.on('pointerover', () => this.tweens.add({ targets: c, scale: 1.05, duration: 110 }));
    c.on('pointerout',  () => this.tweens.add({ targets: c, scale: 1.0,  duration: 110 }));
    c.on('pointerdown', () => {
      this.tweens.add({
        targets: c, scale: 0.93, duration: 90, yoyo: true,
        onComplete: geriCagri
      });
    });
    return c;
  }
}

/* =====================================================================
   OYUNU BAŞLAT
   ===================================================================== */
/* =====================================================================
   NETLİK — cihazın piksel yoğunluğunda çizim
   ---------------------------------------------------------------------
   Oyun 480x800 mantıksal tuvalde çiziliyordu; telefon bunu 1080 piksele
   büyütünce yazılar ve kenarlar bulanıklaşıyordu. Çözüm: tuvali cihazın
   gerçek piksel sayısında açmak, dünyayı ise kamerayı NETLIK katına
   yakınlaştırarak yine 480x800 koordinatta tutmak. Böylece Graphics ile
   çizilen her şey (kartlar, şeritler, kutular) vektör keskinliğinde,
   yazılar da NETLIK çözünürlüğünde üretiliyor; oyun kodunun tek satırı
   değişmiyor.
   ===================================================================== */
const NETLIK = Math.min(3, Math.max(1, Math.round((window.devicePixelRatio || 1) * 2) / 2));

/* Phaser yazıyı kendi ara tuvaline çiziyor; çözünürlük verilmezse 1x
   üretilip yakınlaştırmada bulanıklaşır. Bütün yazılara varsayılan
   olarak NETLIK veriyoruz. */
(function(){
  const TS = Phaser.GameObjects.TextStyle.prototype;
  const eskiSetStyle = TS.setStyle;
  TS.setStyle = function(style, updateText, setDefaults){
    if (style && style.resolution === undefined) style.resolution = NETLIK;
    return eskiSetStyle.call(this, style, updateText, setDefaults);
  };
})();

/* Tuval NETLIK katına büyüdüğü için Phaser imleç konumunu da o ölçekte
   veriyor (0–960). Oyun koordinatına (0–480) çeviren yardımcı: sürükleme
   olayları zaten dünya koordinatı verdiği için yalnız pointer olaylarında
   kullanılıyor. */
function imlec(p){ return { x: p.x / NETLIK, y: p.y / NETLIK }; }

/* Her sahne başlarken kamerayı NETLIK katına yakınlaştırıp fizik
   dünyasını mantıksal ölçüde tutuyoruz: tuval büyüdü, dünya büyümedi.
   Sahne örnekleri oyun kurulumundan sonra eşzamansız oluştuğu için
   kanca Systems.start üzerine takılıyor — yeniden başlatmalarda da
   kendiliğinden çalışıyor. */
(function(){
  const SS = Phaser.Scenes.Systems.prototype;
  const eskiStart = SS.start;
  SS.start = function(veri){
    const sonuc = eskiStart.call(this, veri);
    const sc = this.scene;
    try{
      if (sc.cameras && sc.cameras.main){
        sc.cameras.main.setZoom(NETLIK);
        sc.cameras.main.centerOn(EN / 2, BOY / 2);
      }
      if (sc.physics && sc.physics.world) sc.physics.world.setBounds(0, 0, EN, BOY);
    }catch(e){ /* netlik ayarı oyunu engellemesin */ }
    return sonuc;
  };
})();

window.OYUN = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'oyun',
  width: EN * NETLIK,
  height: BOY * NETLIK,
  backgroundColor: '#10162b',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 300 },
      debug: false
    }
  },
  scene: [BootScene, MenuScene, GameScene, GameOverScene]
});

</script>
</body>
</html>
```

### matbaa-phaser.html — sentenceBuild (25 oyun)
Dosya boyu: 38118 bayt · 1018 satır

```html
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<title>Cümle Kurma Makinesi — Phaser 3</title>
<script src="https://cdn.jsdelivr.net/npm/phaser@3.80.1/dist/phaser.min.js"></script>
<style>
  html, body { margin:0; padding:0; height:100%; background:#141a24; overflow:hidden;
    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
    -webkit-tap-highlight-color: transparent; touch-action:none; }
  #oyun { width:100%; height:100%; display:flex; align-items:center; justify-content:center; }
  canvas { display:block; }
</style>
</head>
<body>
<div id="oyun"></div>
<script>
/* =====================================================================
   CÜMLE KURMA MAKİNESİ — Phaser 3 (mekanik: sentenceBuild · 25 oyun)
   ---------------------------------------------------------------------
   Kazanım: T.Y.3.2.g / T.Y.3.3.b — Okuduklarını kendi ifadeleriyle
   yazar; sözcükleri yerinde kullanır.

   Sahneler : Boot → Menu → Game → GameOver
   Fizik    : Arcade.
              · Her turda kelime kartları hazneden masaya YERÇEKİMİYLE
                dökülür ve birbirinin üstüne gerçekten yığılır.
              · Kart kızağa sürüklenir; doğruysa yerine oturur.
              · Yanlış kelime kızaktan geri tepilir, masaya savrulur.
              · Tur bitince kartlar makineye çekilir, kâğıt basılır.
   Görsel   : Bütün dokular Graphics ile çalışma anında üretilir —
              uygulama çevrimdışı kabukta (APK / iOS) çalışacağı için
              dışarıdan resim çekilmiyor.
   ===================================================================== */

const EN = 480, BOY = 800;

const RENK = {
  zeminUst : 0x1b2432,
  zeminAlt : 0x2f3d52,
  dogru    : 0x34c47b,
  yanlis   : 0xf07575,
  kart     : 0xfdfbf5,
  kartKnr  : 0xd9d0bd,
  metin    : '#23303f',
  makine   : 0x44566e,
  kagit    : 0xfdfbf5,
  vurgu    : 0xffd166
};

/* ---------------------------------------------------------------------
   İÇERİK — uygulamadaki y07 oyununun birebir aynısı.
   Başka bir sentenceBuild oyununa geçmek için yalnızca bu blok değişir.
   kelimeler[] DOĞRU sırada yazılır; oyunda karıştırılarak dökülür.
   ------------------------------------------------------------------- */
/* ---------------- uygulama köprüsü ----------------
   Adres  matbaa.html#oyun=y13  biçiminde; katalog verisi üst pencereden
   okunuyor. Kazanınca completeGame() çağrılır; XP, altın, kutlama ve
   sıradaki oyuna geçiş uygulamanın kendi akışında kalır.               */
const KOPRU = (function(){
  try{
    const p = new URLSearchParams(location.hash.slice(1));
    const id = p.get('oyun');
    if (id && window.parent && window.parent !== window &&
        typeof window.parent.getGame === 'function'){
      const g = window.parent.getGame(id);
      if (g && g.cfg) return {
        oyun: g, cfg: g.cfg,
        bitir(mesaj, puan){ try{ window.parent.completeGame(mesaj || '', puan); }catch(e){} },
        /* Turun kendi metnini uygulamanın sesiyle okutur (Piper). */
        oku(metin){ try{ if (window.parent.oku) window.parent.oku(metin); }catch(e){} },
        /* Kaybetme ekranından: bu oyunu bırak, sıradakine geç. */
        atla(){ try{ if (window.parent.sonrakiOyunaGec) window.parent.sonrakiOyunaGec(); }catch(e){} }
      };
    }
  }catch(e){ /* çapraz kaynak engeli: tek başına oynanır */ }
  return null;
})();

/* HTML varlıklarını çöz: katalogda "Pay &lt; payda" gibi yazımlar var,
   çözülmezse ekranda "&lt;" olarak görünüyor ve öyle okunuyor. */
function varlikCoz(m){
  return String(m)
    .replace(/&nbsp;/gi, ' ')
    .replace(/&lt;/gi, '<').replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"').replace(/&#39;|&apos;/gi, "'")
    .replace(/&hellip;/gi, '…').replace(/&mdash;/gi, '—').replace(/&ndash;/gi, '–')
    .replace(/&times;/gi, '×').replace(/&divide;/gi, '÷').replace(/&deg;/gi, '°')
    .replace(/&rarr;/gi, '→').replace(/&larr;/gi, '←')
    .replace(/&amp;/gi, '&');            /* en sona: çift çözmeyi önler */
}

function duzMetin(x){
  return varlikCoz(String(x == null ? '' : x).replace(/<br\s*\/?>/gi,' ')
    .replace(/<[^>]+>/g,'')).replace(/[“”]/g,'"').replace(/\s+/g,' ').trim();
}

const VARSAYILAN = {
  instruction:'Kelimeleri sırayla kızağa taşı',
  tip:'Cümle büyük harfle başlar, uygun noktalama işaretiyle biter.',
  rounds:[
    { prompt:'Dedemle ilgili bir cümle kur.',
      words:['Dedem','bana','masal','anlattı','.'],
      wrongHint:'Cümle özneyle başlar: “Dedem…”', okMsg:'Baskı tamam! 🖨️' },
    { prompt:'Bu kez bir SORU cümlesi kur.',
      words:['Sen','de','bizimle','oynar','mısın','?'],
      wrongHint:'“Sen” ile başla, sonuna soru işaretini koy.', okMsg:'Soru cümlesi hazır! ❓' },
    { prompt:'Şimdi bir ÜNLEM cümlesi kur.',
      words:['Ne','kadar','nazik','bir','çocuksun','!'],
      wrongHint:'“Ne” ile başla, sonuna ünlem koy.', okMsg:'Ünlem cümlesi hazır! ❗' } ]
};

const CFG = KOPRU ? KOPRU.cfg : VARSAYILAN;

const TURLAR = (CFG.rounds || []).map(r => ({
  gorev:     duzMetin(r.prompt),
  kelimeler: (r.words || []).map(duzMetin),
  ipucu:     duzMetin(r.wrongHint),
  tamam:     duzMetin(r.okMsg) || 'Baskı tamam! 🖨️',
  aciklama:  duzMetin(r.revealHtml) || duzMetin(r.revealSay)
}));

const OYUN_ADI = KOPRU ? duzMetin(KOPRU.oyun.title) : 'CÜMLE KURMA MAKİNESİ';
const OYUN_EMO = KOPRU ? (KOPRU.oyun.emo || '🖨️') : '🖨️';
const TALIMAT  = duzMetin(CFG.instruction) || 'Kelimeleri sırayla diz';
const IPUCU    = duzMetin(CFG.tip);
const BASARI   = duzMetin(CFG.successMsg) || 'Bütün cümleleri doğru kurdun!';

const CAN_SAYISI = 3;

/* --- Yerleşim -------------------------------------------------------- */
const KIZAK_UST = 214;   /* baskı kızağının üst kenarı */
const KIZAK_ASGARI = 78; /* tek satırlık kızak yüksekliği */
const KIZAK_AZAMI  = 122;/* masaya değmeden büyüyebileceği azami yükseklik */
const KIZAK_PAY    = 8;  /* kızağın iç boşluğu */
const MASA_UST  = 340;   /* kartların döküldüğü alan */
const MASA_ALT  = 592;
const MAKINE_Y  = 690;

/* =====================================================================
   1) BOOT — dokuları üret
   ===================================================================== */
class BootScene extends Phaser.Scene {
  constructor(){ super('Boot'); }

  create(){
    this.dokuKivilcim();
    this.dokuToz();
    this.dokuKagit();
    /* Uygulama içinde çocuk oyunu listeden zaten seçti; menüyü atla. */
    this.scene.start(KOPRU ? 'Game' : 'Menu');
  }

  dokuKivilcim(){
    const g = this.make.graphics({ add:false });
    g.fillStyle(0xffffff, 1);
    g.fillCircle(8, 8, 8);
    g.generateTexture('kivilcim', 16, 16);
    g.destroy();
  }

  dokuToz(){
    const g = this.make.graphics({ add:false });
    for (let r = 14; r > 0; r--){
      g.fillStyle(0xffffff, 0.06);
      g.fillCircle(14, 14, r);
    }
    g.generateTexture('toz', 28, 28);
    g.destroy();
  }

  /* Basılan kâğıt yaprağı */
  dokuKagit(){
    const W = 300, H = 120;
    const g = this.make.graphics({ add:false });
    g.fillStyle(RENK.kagit, 1);
    g.fillRoundedRect(0, 0, W, H, 8);
    g.lineStyle(2, 0xcfc6b2, 1);
    g.strokeRoundedRect(0, 0, W, H, 8);
    /* satır çizgileri */
    g.lineStyle(1, 0xe4dcc9, 1);
    for (let y = 26; y < H - 10; y += 20) g.lineBetween(14, y, W - 14, y);
    g.generateTexture('kagit', W, H);
    g.destroy();
  }
}

/* =====================================================================
   Ortak yardımcılar
   ===================================================================== */
function atolyeCiz(sc){
  const g = sc.add.graphics();
  g.fillGradientStyle(RENK.zeminUst, RENK.zeminUst, RENK.zeminAlt, RENK.zeminAlt, 1);
  g.fillRect(0, 0, EN, BOY);

  /* duvardaki mürekkep lekeleri */
  for (let i = 0; i < 22; i++){
    const s = sc.add.circle(
      Phaser.Math.Between(8, EN - 8),
      Phaser.Math.Between(8, BOY - 8),
      Phaser.Math.FloatBetween(2, 5),
      0xffffff,
      Phaser.Math.FloatBetween(0.03, 0.1)
    );
    sc.tweens.add({
      targets:s, alpha:0.02,
      duration:Phaser.Math.Between(1600, 3400),
      yoyo:true, repeat:-1, delay:Phaser.Math.Between(0, 2000)
    });
  }
  return g;
}

function dugmeYap(sc, x, y, metin, renk, geriCagri){
  const c = sc.add.container(x, y);
  const g = sc.add.graphics();
  g.fillStyle(renk, 1);
  g.fillRoundedRect(-140, -30, 280, 60, 30);
  g.fillStyle(0xffffff, 0.16);
  g.fillRoundedRect(-140, -30, 280, 24, { tl:30, tr:30, bl:0, br:0 });
  const t = sc.add.text(0, 0, metin, {
    fontFamily:'system-ui, sans-serif', fontSize:'25px',
    fontStyle:'bold', color:'#ffffff'
  }).setOrigin(0.5);
  c.add([g, t]);
  c.setSize(280, 60).setInteractive({ useHandCursor:true });
  c.on('pointerover', () => sc.tweens.add({ targets:c, scale:1.05, duration:110 }));
  c.on('pointerout',  () => sc.tweens.add({ targets:c, scale:1.00, duration:110 }));
  c.on('pointerdown', () => sc.tweens.add({
    targets:c, scale:0.93, duration:90, yoyo:true, onComplete:geriCagri
  }));
  return c;
}

/* =====================================================================
   2) MENU
   ===================================================================== */
class MenuScene extends Phaser.Scene {
  constructor(){ super('Menu'); }

  create(){
    atolyeCiz(this);

    this.add.text(EN / 2, 174, OYUN_EMO, { fontSize:'90px' }).setOrigin(0.5);
    const kagit = this.add.image(EN / 2, 236, 'kagit').setScale(0.5).setAlpha(0.9);
    this.tweens.add({
      targets:kagit, y:248, duration:1600,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });

    const baslik = this.add.text(EN / 2, 336, OYUN_ADI, {
      fontFamily:'system-ui, sans-serif', fontSize:'40px', fontStyle:'bold',
      color:'#ffffff', align:'center', lineSpacing:5
    }).setOrigin(0.5);
    this.tweens.add({
      targets:baslik, scale:1.04, duration:1400,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });

    this.add.text(EN / 2, 424, TALIMAT, {
      fontFamily:'system-ui, sans-serif', fontSize:'22px',
      color:'#cfe0ff', align:'center'
    }).setOrigin(0.5);

    const kart = this.add.graphics();
    kart.fillStyle(0x0f1721, 0.92);
    kart.fillRoundedRect(32, 462, EN - 64, 70, 16);
    kart.lineStyle(2, 0x44566e, 1);
    kart.strokeRoundedRect(32, 462, EN - 64, 70, 16);
    this.add.text(EN / 2, 497, IPUCU, {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#ffd166', align:'center', wordWrap:{ width:EN - 96 }, lineSpacing:4
    }).setOrigin(0.5);

    dugmeYap(this, EN / 2, 606, '▶  BAŞLA', RENK.dogru, () => this.scene.start('Game'));

    this.add.text(EN / 2, 712, `${TURLAR.length} cümle  ·  ${CAN_SAYISI} can`, {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', color:'#9fb4cc'
    }).setOrigin(0.5);
  }
}

/* =====================================================================
   3) GAME
   ===================================================================== */
class GameScene extends Phaser.Scene {
  constructor(){ super('Game'); }

  create(){
    this.can    = CAN_SAYISI;
    this.puan   = 0;
    this.seri   = 0;
    this.tur    = 0;
    this.kilit  = true;
    this.suruklenen = null;

    atolyeCiz(this);

    this.kivilcimlar = this.add.particles(0, 0, 'kivilcim', {
      speed:{ min:140, max:380 }, angle:{ min:0, max:360 },
      scale:{ start:0.9, end:0 }, alpha:{ start:1, end:0 },
      lifespan:650, gravityY:380, blendMode:'ADD', emitting:false
    }).setDepth(90);

    this.tozlar = this.add.particles(0, 0, 'toz', {
      speed:{ min:40, max:150 }, angle:{ min:200, max:340 },
      scale:{ start:1.1, end:2.3 }, alpha:{ start:0.5, end:0 },
      lifespan:700, emitting:false
    }).setDepth(80);

    this.sahneKur();

    /* Kart grubu ve çarpışmaları BİR KEZ kurulur. Her turda yeniden
       oluşturulursa eski kartlar sahnede kalıyor ve collider'lar
       turdan tura birikiyordu. */
    this.kartlar = this.physics.add.group();
    this.physics.add.collider(this.kartlar, this.masa);
    this.physics.add.collider(this.kartlar, this.kartlar);

    this.arayuzKur();
    this.surukleKur();
    this.turuBaslat();
  }

  /* ---------- sabit sahne parçaları ---------- */
  sahneKur(){
    /* Baskı kızağı: yüksekliği turdan tura değişiyor (uzun cümleler iki
       ya da üç satıra diziliyor), bu yüzden her turda yeniden çiziliyor. */
    this.kizakG = this.add.graphics().setDepth(5);
    this.kizakEtiket = this.add.text(24, KIZAK_UST + 8, 'BASKI KIZAĞI', {
      fontFamily:'system-ui, sans-serif', fontSize:'14px', fontStyle:'bold',
      color:'#7f95ad'
    }).setDepth(6);
    this.kizakAlt = KIZAK_UST + KIZAK_ASGARI;
    this.kizagiCiz(KIZAK_ASGARI);

    /* masa yüzeyi */
    const m = this.add.graphics().setDepth(4);
    m.fillStyle(0x22303f, 1);
    m.fillRoundedRect(10, MASA_ALT, EN - 20, 20, 8);
    m.fillStyle(0x35485e, 1);
    m.fillRoundedRect(10, MASA_ALT, EN - 20, 7, { tl:8, tr:8, bl:0, br:0 });

    /* NOT: Phaser'da collider(grup, TEK nesne) callback'e parametreleri
       ters veriyor; bu yüzden engeller staticGroup içinde tutuluyor. */
    this.masa = this.physics.add.staticGroup();
    this.masa.add(this.add.rectangle(EN / 2, MASA_ALT + 6, EN - 24, 14, 0, 0));
    /* Yan duvarlar TAM BOY olmalı. Kısa tutulunca kartlar duvarın üst
       kenarına oturup havada asılı kalıyordu (hiç düşmüyorlardı). */
    this.masa.add(this.add.rectangle(4,      BOY / 2, 12, BOY * 2, 0, 0));
    this.masa.add(this.add.rectangle(EN - 4, BOY / 2, 12, BOY * 2, 0, 0));

    /* baskı makinesi */
    const g = this.add.graphics().setDepth(6);
    g.fillStyle(RENK.makine, 1);
    g.fillRoundedRect(46, MAKINE_Y - 46, EN - 92, 92, 14);
    g.fillStyle(0x35485e, 1);
    g.fillRoundedRect(46, MAKINE_Y - 46, EN - 92, 26, { tl:14, tr:14, bl:0, br:0 });
    g.fillStyle(0x1b2432, 1);
    g.fillRoundedRect(76, MAKINE_Y - 8, EN - 152, 16, 6);     /* kâğıt yuvası */
    g.fillStyle(RENK.vurgu, 1);
    g.fillCircle(EN - 76, MAKINE_Y - 32, 6);
    this.add.text(EN / 2, MAKINE_Y + 26, 'BASKI MAKİNESİ', {
      fontFamily:'system-ui, sans-serif', fontSize:'16px', fontStyle:'bold',
      color:'#8fa6bd'
    }).setOrigin(0.5).setDepth(7);
  }

  /* Kızağı verilen yükseklikte çiz; alt kenarı this.kizakAlt'a yaz. */
  kizagiCiz(boy){
    this.kizakAlt = KIZAK_UST + boy;
    this.kizakG.clear();
    this.kizakG.fillStyle(0x0f1721, 0.9);
    this.kizakG.fillRoundedRect(14, KIZAK_UST, EN - 28, boy, 12);
    this.kizakG.lineStyle(2, 0x5c718c, 1);
    this.kizakG.strokeRoundedRect(14, KIZAK_UST, EN - 28, boy, 12);
  }

  /* Bir yazının punto başına gerçek genişliği (varsayım yapmıyoruz:
     "Söylediklerinizi" gibi 16 harflik kelimeler tek başına 190px). */
  yaziEni(metin, punto){
    const t = this.add.text(0, 0, metin, {
      fontFamily:'system-ui, sans-serif', fontSize:punto + 'px', fontStyle:'bold'
    }).setVisible(false);
    const w = t.width; t.destroy();
    return w;
  }

  /* Genişlikleri satırlara böl (aç gözlü sarma, aralar 6px). */
  satirlaraBol(enler, kullanilir){
    const satirlar = [];
    let simdi = [], toplam = 0;
    enler.forEach((en, i) => {
      const ek = (simdi.length ? 6 : 0) + en;
      if (simdi.length && toplam + ek > kullanilir){
        satirlar.push(simdi); simdi = [i]; toplam = en;
      } else {
        simdi.push(i); toplam += ek;
      }
    });
    if (simdi.length) satirlar.push(simdi);
    return satirlar;
  }

  /* Turun kartları kızağa sığacak punto/kart boyunu seç.
     KUSUR: 100 turun 88'inde kartlar tek satıra diziliyordu ve toplam
     genişlik 846px'e çıkıyordu — 452px'lik kızaktan taşıp ekran dışına
     çıkıyorlardı. Artık ölçü cümlenin GERÇEK genişliğinden hesaplanıyor. */
  olculeriSec(kelimeler){
    const denemeler = [{ punto:21, boy:46 }, { punto:19, boy:42 },
                       { punto:17, boy:38 }, { punto:15, boy:34 }];
    const kullanilir = EN - 28 - KIZAK_PAY * 2;         /* 436 */
    let son = null;
    for (let i = 0; i < denemeler.length; i++){
      const d = denemeler[i];
      const enler = kelimeler.map(k => Math.max(40, this.yaziEni(k, d.punto) + 20));
      const satirlar = this.satirlaraBol(enler, kullanilir);
      const boy = satirlar.length * d.boy + (satirlar.length - 1) * 5 + KIZAK_PAY * 2;
      son = { punto:d.punto, kartBoy:d.boy, enler, satirlar, boy };
      if (satirlar.length <= 3 && boy <= KIZAK_AZAMI &&
          enler.every(e => e <= kullanilir)) break;
    }
    son.boy = Math.max(KIZAK_ASGARI, Math.min(KIZAK_AZAMI, son.boy));
    return son;
  }

  /* ---------- tur kurulumu ---------- */
  turuBaslat(){
    const t = TURLAR[this.tur];
    this.olcu = this.olculeriSec(t.kelimeler);
    this.kizagiCiz(this.olcu.boy);
    this.sira = 0;
    this.turHatasiz = false;
    this.kizakKartlari = [];
    this.kilit = true;

    this.gorevYazi.setText(t.gorev);
    this.tweens.add({
      targets:this.gorevYazi, scale:{ from:0.85, to:1 }, duration:280, ease:'Back.easeOut'
    });

    /* önceki turdan kalan kart varsa temizle */
    this.kartlar.clear(true, true);

    /* kelimeler karıştırılıp masadaki YUVALARA yerleşir.
       KUSUR: kartlar yerçekimiyle masaya dökülüyordu; 8–10 kart 480px'lik
       masada birbirine kilitlenip ÜST ÜSTE biniyordu ve dokunulan kart
       yerine üstte kalan komşu tutuluyordu (sınamada 41 ıskalama üst üste).
       Artık her kartın kendi yuvası var: düşme canlandırması korunuyor,
       ama kartlar birbirine girmiyor. */
    const karisik = Phaser.Utils.Array.Shuffle(
      t.kelimeler.map((k, i) => ({ kelime:k, sira:i }))
    );
    const yuvalar = this.masaYuvalariHesapla(karisik.map(v => v.kelime));
    karisik.forEach((v, i) => {
      this.time.delayedCall(i * 90, () => this.kartYap(v, yuvalar[i]));
    });

    this.time.delayedCall(karisik.length * 90 + 700, () => {
      this.kilit = false;
    });

    this.arayuzuTazele();
  }

  /* Masadaki yuvalar: kelime genişliklerine göre satırlara sarılmış,
     ortalanmış ve masa yüzeyine yayılmış konumlar. */
  masaYuvalariHesapla(kelimeler){
    const punto  = (this.olcu && this.olcu.punto) || 21;
    const kBoy   = (this.olcu && this.olcu.kartBoy) || 46;
    const bosluk = 10;
    const kullanilir = EN - 36;
    const enler = kelimeler.map(k => Math.max(40, this.yaziEni(k, punto) + 20));
    const satirlar = this.satirlaraBol(enler.map(e => e + bosluk - 6), kullanilir);

    const alanBoy  = MASA_ALT - MASA_UST - 14;
    const satirAdim = Math.min(kBoy + 14, satirlar.length > 1
      ? (alanBoy - kBoy) / (satirlar.length - 1) : alanBoy);
    const ilkY = MASA_UST + 10 + kBoy / 2 +
      Math.max(0, (alanBoy - ((satirlar.length - 1) * satirAdim + kBoy)) / 2);

    const yuvalar = [];
    satirlar.forEach((satir, si) => {
      let toplam = 0;
      satir.forEach(i => { toplam += enler[i] + bosluk; });
      toplam -= bosluk;
      let x = EN / 2 - toplam / 2;
      satir.forEach(i => {
        yuvalar[i] = { x:x + enler[i] / 2, y:ilkY + si * satirAdim };
        x += enler[i] + bosluk;
      });
    });
    return yuvalar;
  }

  kartYap(v, yuva){
    const punto = (this.olcu && this.olcu.punto) || 21;
    const yazi = this.add.text(0, 0, v.kelime, {
      fontFamily:'system-ui, sans-serif', fontSize:punto + 'px', fontStyle:'bold',
      color: RENK.metin
    }).setOrigin(0.5);

    const W = Math.max(40, yazi.width + 20);
    const H = (this.olcu && this.olcu.kartBoy) || 46;

    const g = this.add.graphics();
    g.fillStyle(RENK.kart, 1);
    g.fillRoundedRect(-W / 2, -H / 2, W, H, 9);
    g.lineStyle(2, RENK.kartKnr, 1);
    g.strokeRoundedRect(-W / 2, -H / 2, W, H, 9);
    g.fillStyle(0x000000, 0.05);
    g.fillRoundedRect(-W / 2, H / 2 - 8, W, 8, { tl:0, tr:0, bl:9, br:9 });

    const c = this.add.container(yuva.x, MASA_UST - 70, [g, yazi]).setDepth(20);
    c.setSize(W, H);

    /* Arcade gövdesi — gruba ÖNCE ekle: Arcade Group add() sırasında
       kendi varsayılanlarını gövdeye basıyor. Container gövdesi zaten
       container orijininde merkezlenir; setOffset verilmez. */
    this.kartlar.add(c);
    c.body.setSize(W, H);
    c.body.setAllowGravity(false);      /* yuva düzeninde yerçekimi yok */
    c.body.setVelocity(0, 0);

    c.setData('kelime', v.kelime);
    c.setData('sira', v.sira);
    c.setData('yerlesti', false);
    c.setData('en', W);
    c.setData('yuva', yuva);

    /* kart yuvasına süzülsün (düşme hissi korunuyor, çarpışma yok) */
    this.yuvayaGonder(c, 260);

    /* Dokunma alanını Phaser'a bırakıyoruz: Container'a elle
       Rectangle(-W/2,-H/2,…) verilince kaydırma bir kez daha uygulanıyor ve
       alan sola-yukarı kayıyor — nesneyi tutmak için sol üstüne basmak
       gerekiyordu. setSize + argümansız setInteractive() alanı ortalıyor.
       Parmak payı KÜÇÜK tutuluyor: ±12px payla kartlar masada yığılırken
       komşunun alanı bu kartın merkezini örtüyordu ve dokunulan kart
       yerine üstte çizilen komşu tutuluyordu (sınamada yanlış kelime
       kızağa gidip can eksiltti). */
    c.setSize(W + 8, H + 8);
    c.setInteractive();
    this.input.setDraggable(c);

    this.tozlar.explode(3, c.x, c.y);
    return c;
  }

  /* Kartı yuvasına taşı. Konum gövde üzerinden yürüyor: x/y tween'lenirse
     gövde bir sonraki karede kartı geri çekiyor. */
  yuvayaGonder(kart, sure){
    const y = kart.getData('yuva');
    if (!y) return;
    const bx = kart.x, by = kart.y;
    this.tweens.add({
      targets:{ t:0 }, t:1, duration:sure || 240, ease:'Quad.easeOut',
      onUpdate:(tw, o) => {
        if (!kart.active || !kart.body) return;
        kart.body.reset(bx + (y.x - bx) * o.t, by + (y.y - by) * o.t);
      }
    });
  }

  /* ---------- sürükleme ---------- */
  surukleKur(){
    this.input.on('dragstart', (p, kart) => {
      if (this.kilit || kart.getData('yerlesti')) return;
      this.suruklenen = kart;
      kart.setDepth(70);
      kart.body.setVelocity(0, 0);
      this.tweens.add({ targets:kart, scale:1.14, duration:120, ease:'Back.easeOut' });
      this.kizakVurgula(true);
    });

    this.input.on('drag', (p, kart, x, y) => {
      if (this.kilit || kart.getData('yerlesti')) return;
      kart.x = Phaser.Math.Clamp(x, 34, EN - 34);
      kart.y = Phaser.Math.Clamp(y, KIZAK_UST - 10, BOY - 40);
    });

    this.input.on('dragend', (p, kart) => {
      if (this.kilit || kart.getData('yerlesti')) return;
      this.suruklenen = null;
      this.kizakVurgula(false);
      this.tweens.add({ targets:kart, scale:1, duration:120 });

      /* kızağa bırakıldı mı? */
      if (kart.y > KIZAK_UST - 24 && kart.y < this.kizakAlt + 24){
        if (kart.getData('sira') === this.sira) this.dogru(kart);
        else                                    this.yanlis(kart);
        return;
      }
      /* masaya geri dönsün: rastgele düşürülürse komşuların üstüne
         biniyordu, yuvasına geri süzülüyor. */
      kart.setDepth(20);
      this.yuvayaGonder(kart, 220);
    });
  }

  kizakVurgula(acik){
    if (!this.kizakIsik){
      this.kizakIsik = this.add.graphics().setDepth(5);
    }
    this.kizakIsik.clear();
    if (!acik) return;
    this.kizakIsik.lineStyle(3, RENK.vurgu, 0.9);
    this.kizakIsik.strokeRoundedRect(14, KIZAK_UST, EN - 28, this.kizakAlt - KIZAK_UST, 12);
  }

  /* Kızaktaki kartları satırlara sararak diz. Tek satır varsayımı
     cümlelerin çoğunda kartları ekran dışına taşıyordu. */
  kizagiDiz(){
    const bosluk    = 6;
    const kartBoy   = (this.olcu && this.olcu.kartBoy) || 46;
    const kullanilir = EN - 28 - KIZAK_PAY * 2;

    /* satırlara böl */
    const enler = this.kizakKartlari.map(k => k.getData('en'));
    const satirlar = this.satirlaraBol(enler, kullanilir);

    /* satır yüksekliği kızağa sığacak şekilde sıkıştırılabilir */
    const boy = this.kizakAlt - KIZAK_UST;
    const satirAdim = satirlar.length > 1
      ? Math.min(kartBoy + 5, (boy - KIZAK_PAY * 2 - kartBoy) / (satirlar.length - 1))
      : 0;
    const ilkY = KIZAK_UST + KIZAK_PAY + kartBoy / 2;

    satirlar.forEach((satir, si) => {
      let toplam = 0;
      satir.forEach(i => { toplam += enler[i] + bosluk; });
      toplam -= bosluk;
      let x = EN / 2 - toplam / 2;
      const y = ilkY + si * satirAdim;
      satir.forEach(i => {
        const k = this.kizakKartlari[i];
        const hedefX = x + enler[i] / 2;
        x += enler[i] + bosluk;
        const basX = k.x, basY = k.y;
        /* Konumu gövde üzerinden taşı: x/y tween'lenirse gövde bir sonraki
           karede kartı geri çeker. */
        this.tweens.add({
          targets:{ t:0 }, t:1, duration:200, ease:'Quad.easeOut',
          onUpdate:(tw, o) => {
            if (k.body) k.body.reset(basX + (hedefX - basX) * o.t,
                                     basY + (y - basY) * o.t);
          }
        });
      });
    });
  }

  /* ---------- sonuçlar ---------- */
  dogru(kart){
    /* Kelime başına sabit puan. Seri bonusu kelime başına verilirse
       uzun cümlelerde puan katlanarak şişiyordu; bonus tur sonunda,
       hatasız tur serisine göre veriliyor. */
    const kazanc = 50;
    this.puan += kazanc;
    this.sira++;

    kart.setData('yerlesti', true);
    kart.disableInteractive();
    kart.setDepth(30);
    kart.body.setAllowGravity(false);
    kart.body.setVelocity(0, 0);
    kart.setAngle(0);

    this.kizakKartlari.push(kart);
    this.kizagiDiz();

    this.kivilcimlar.setParticleTint(RENK.dogru);
    this.kivilcimlar.explode(14, kart.x, kart.y);

    this.puanYazi.setText('Puan ' + this.puan);
    this.tweens.add({
      targets:this.puanYazi, scale:1.4, duration:120, yoyo:true, ease:'Back.easeOut'
    });

    const ucan = this.add.text(kart.x, kart.y - 24, '+' + kazanc, {
      fontFamily:'system-ui, sans-serif', fontSize:'24px', fontStyle:'bold',
      color:'#7ce0a3'
    }).setOrigin(0.5).setDepth(95);
    this.tweens.add({
      targets:ucan, y:ucan.y - 50, alpha:0,
      duration:600, ease:'Cubic.easeOut', onComplete:() => ucan.destroy()
    });

    this.arayuzuTazele();

    if (this.sira >= TURLAR[this.tur].kelimeler.length){
      this.kilit = true;
      /* tur hatasız bittiyse seri büyür */
      this.seri = this.turHatasiz ? 1 : this.seri + 1;
      this.turHatasiz = false;
      const bonus = 100 + (this.seri - 1) * 25;
      this.puan += bonus;
      this.sonBonus = bonus;
      this.time.delayedCall(400, () => this.bas());
    }
  }

  yanlis(kart){
    this.seri = 0;
    this.turHatasiz = true;      /* bu tur artık hatasız sayılmaz */
    this.can--;
    this.arayuzuTazele();

    /* Kızak yanlış kelimeyi geri tükürür: kart silkelenip YUVASINA döner.
       Serbest fırlatma kartı komşuların üstüne bırakıyordu. */
    kart.setDepth(20);
    this.tweens.add({
      targets:kart, angle:{ from:-14, to:14 }, duration:70, yoyo:true, repeat:2,
      onComplete:() => { kart.setAngle(0); this.yuvayaGonder(kart, 240); }
    });

    this.tozlar.explode(12, kart.x, kart.y);
    this.cameras.main.shake(220, 0.011);
    this.cameras.main.flash(170, 220, 90, 90);

    this.tweens.add({
      targets:this.canYazi, angle:{ from:-12, to:12 },
      duration:70, yoyo:true, repeat:3,
      onComplete:() => this.canYazi.setAngle(0)
    });

    this.mesajGoster(TURLAR[this.tur].ipucu, '#b5453b');

    if (this.can <= 0){
      this.kilit = true;
      this.time.delayedCall(900, () => this.bitir(false));
    }
  }

  /* ---------- baskı ---------- */
  bas(){
    const t = TURLAR[this.tur];
    const cumle = t.kelimeler.join(' ').replace(/ ([.!?])/g, '$1');

    /* kartlar makineye çekilsin */
    this.kizakKartlari.forEach((k, i) => {
      k.body.enable = false;
      this.tweens.add({
        targets:k, x:EN / 2, y:MAKINE_Y - 20, scale:0.3, alpha:0.15,
        duration:380, delay:i * 45, ease:'Quad.easeIn',
        onComplete:() => k.destroy()
      });
    });

    this.time.delayedCall(this.kizakKartlari.length * 45 + 420, () => {
      this.cameras.main.shake(260, 0.006);
      this.tozlar.explode(14, EN / 2, MAKINE_Y);

      /* kâğıt makineden çıkar */
      const kagit = this.add.image(EN / 2, MAKINE_Y - 10, 'kagit')
        .setScale(0.9).setDepth(75).setAlpha(0);
      const yaziK = this.add.text(EN / 2, MAKINE_Y - 26, cumle, {
        fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
        color:'#23303f', align:'center', wordWrap:{ width:250 }, lineSpacing:3
      }).setOrigin(0.5).setDepth(76).setAlpha(0);
      const yaziA = this.add.text(EN / 2, MAKINE_Y + 12, t.aciklama, {
        fontFamily:'system-ui, sans-serif', fontSize:'16px',
        color:'#6b7c8f', align:'center', wordWrap:{ width:250 }
      }).setOrigin(0.5).setDepth(76).setAlpha(0);

      this.tweens.add({
        targets:[kagit, yaziK, yaziA], alpha:1, y:'-=132',
        duration:620, ease:'Quad.easeOut'
      });

      this.kivilcimlar.setParticleTint(RENK.vurgu);
      this.kivilcimlar.explode(24, EN / 2, MAKINE_Y - 40);
      this.mesajGoster(t.tamam + '   +' + this.sonBonus, '#1f6d4a');
      this.cameras.main.flash(150, 80, 210, 140);

      this.tur++;
      this.arayuzuTazele();

      this.time.delayedCall(2100, () => {
        this.tweens.add({
          targets:[kagit, yaziK, yaziA], alpha:0, duration:300,
          onComplete:() => { kagit.destroy(); yaziK.destroy(); yaziA.destroy(); }
        });
        if (this.tur >= TURLAR.length) this.bitir(true);
        else                            this.turuBaslat();
      });
    });
  }

  mesajGoster(metin, arka){
    if (this.mesaj) this.mesaj.destroy();
    this.mesaj = this.add.text(EN / 2, 322, metin, {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#ffffff', backgroundColor:arka,
      padding:{ x:13, y:8 }, align:'center', wordWrap:{ width:EN - 70 }
    }).setOrigin(0.5).setDepth(96).setAlpha(0);
    const t = this.mesaj;
    this.tweens.add({ targets:t, alpha:1, duration:150 });
    this.time.delayedCall(1500, () => {
      if (!t.active) return;
      this.tweens.add({
        targets:t, alpha:0, duration:250,
        onComplete:() => { if (this.mesaj === t) this.mesaj = null; t.destroy(); }
      });
    });
  }

  /* ---------- arayüz ---------- */
  arayuzKur(){
    /* Katalogda yönerge 120 karaktere çıkıyor; sabit yükseklikli şerit
       yazıyı iki yandan kesiyordu. Şerit metnin gerçek boyuna göre. */
    const yon = this.add.text(EN / 2, 22, OYUN_EMO + '  ' + TALIMAT, {
      fontFamily:'system-ui, sans-serif',
      fontSize: (TALIMAT.length > 92 ? '16px' : (TALIMAT.length > 54 ? '17px' : '20px')),
      fontStyle:'bold', color:'#ffffff', align:'center',
      wordWrap:{ width:EN - 52 }, lineSpacing:3
    }).setOrigin(0.5, 0).setDepth(61);

    const seritBoy = Math.max(104, yon.height + 62);
    const serit = this.add.graphics().setDepth(60);
    serit.fillStyle(0x0f1721, 0.97);
    serit.fillRoundedRect(10, 10, EN - 20, seritBoy, 18);
    yon.setDepth(61);
    const satirY = 10 + seritBoy - 22;
    this.seritAlt = 10 + seritBoy;

    this.puanYazi = this.add.text(30, satirY, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0, 0.5).setDepth(61);

    this.canYazi = this.add.text(EN - 30, satirY, '', { fontSize:'20px' })
      .setOrigin(1, 0.5).setDepth(61);

    this.ilerlemeYazi = this.add.text(EN / 2, satirY, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#9fb4cc'
    }).setOrigin(0.5).setDepth(61);

    this.gorevYazi = this.add.text(EN / 2, this.seritAlt + 34, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', fontStyle:'bold',
      color:'#ffffff', align:'center', wordWrap:{ width:EN - 50 }
    }).setOrigin(0.5).setDepth(61);

    this.arayuzuTazele();
  }

  arayuzuTazele(){
    this.canYazi.setText(
      '❤️'.repeat(Math.max(0, this.can)) +
      '🖤'.repeat(Math.max(0, CAN_SAYISI - this.can))
    );
    this.ilerlemeYazi.setText(`${this.tur} / ${TURLAR.length} cümle`);
  }

  bitir(kazandi){
    /* Uygulama içindeyken kazanma ekranını uygulama gösteriyor. */
    if (kazandi && KOPRU){ KOPRU.bitir(BASARI, this.puan); return; }
    this.scene.start('GameOver', {
      kazandi, puan:this.puan, can:this.can,
      tur:this.tur, toplam:TURLAR.length
    });
  }

  /* ---------- her kare ---------- */
  update(){
    if (this.kilit || !this.kartlar) return;
    /* masadan kaçan kartı geri getir */
    this.kartlar.getChildren().forEach(k => {
      if (!k.active || k.getData('yerlesti') || this.suruklenen === k) return;
      if (k.y > BOY + 60 || k.x < -60 || k.x > EN + 60){
        const y = k.getData('yuva');
        k.body.reset(y ? y.x : EN / 2, y ? y.y : MASA_UST + 40);
        k.body.setVelocity(0, 0);
      }
    });
  }
}

/* =====================================================================
   4) GAME OVER
   ===================================================================== */
class GameOverScene extends Phaser.Scene {
  constructor(){ super('GameOver'); }

  init(veri){ this.veri = veri; }

  create(){
    const { kazandi, puan, can, tur, toplam } = this.veri;
    atolyeCiz(this);

    const emo = this.add.text(EN / 2, 190, kazandi ? '🖨️' : '💪', { fontSize:'97px' })
      .setOrigin(0.5).setScale(0);
    this.tweens.add({ targets:emo, scale:1, duration:520, ease:'Back.easeOut' });

    this.add.text(EN / 2, 300, kazandi ? 'BASKI USTASI!' : 'TEKRAR DENE', {
      fontFamily:'system-ui, sans-serif', fontSize:'35px', fontStyle:'bold',
      color: kazandi ? '#7ce0a3' : '#ffd166', align:'center'
    }).setOrigin(0.5);

    this.add.text(EN / 2, 360,
      kazandi ? BASARI : `${tur} / ${toplam} cümle bastın — bir daha deneyelim mi?`, {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#cfe0ff',
      align:'center', wordWrap:{ width:EN - 70 }, lineSpacing:5
    }).setOrigin(0.5);

    const puanYazi = this.add.text(EN / 2, 456, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'42px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0.5);
    const sayac = { v:0 };
    this.tweens.add({
      targets:sayac, v:puan, duration:900, ease:'Cubic.easeOut',
      onUpdate:() => puanYazi.setText('Puan ' + Math.round(sayac.v))
    });

    this.add.text(EN / 2, 506,
      'Kalan can: ' + (can > 0 ? '❤️'.repeat(can) : '—'), {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#9fb4cc'
    }).setOrigin(0.5);

    if (kazandi){
      const konfeti = this.add.particles(EN / 2, -20, 'kivilcim', {
        speed:{ min:90, max:260 }, angle:{ min:60, max:120 },
        scale:{ start:0.8, end:0 }, alpha:{ start:1, end:0 },
        lifespan:2000, gravityY:180, quantity:2, frequency:70,
        tint:[0xffd166, 0x7ce0a3, 0x7fb2f0, 0xf07575]
      }).setDepth(5);
      this.time.delayedCall(2600, () => konfeti.stop());
    }

    dugmeYap(this, EN / 2, 606, '↻  TEKRAR OYNA', RENK.dogru, () => this.scene.start('Game'));

    /* Uygulama içinde: bu oyunda takılan çocuk sıradakine geçebilsin. */

    if (KOPRU) dugmeYap(this, EN / 2, 680, '⏭  SIRADAKİ OYUN', 0x4a679e, () => KOPRU.atla());
    if (!KOPRU) dugmeYap(this, EN / 2, 684, '☰  MENÜ',        0x44566e, () => this.scene.start('Menu'));
  }
}

/* =====================================================================
   OYUNU BAŞLAT
   ===================================================================== */
/* =====================================================================
   NETLİK — cihazın piksel yoğunluğunda çizim
   ---------------------------------------------------------------------
   Oyun 480x800 mantıksal tuvalde çiziliyordu; telefon bunu 1080 piksele
   büyütünce yazılar ve kenarlar bulanıklaşıyordu. Çözüm: tuvali cihazın
   gerçek piksel sayısında açmak, dünyayı ise kamerayı NETLIK katına
   yakınlaştırarak yine 480x800 koordinatta tutmak. Böylece Graphics ile
   çizilen her şey (kartlar, şeritler, kutular) vektör keskinliğinde,
   yazılar da NETLIK çözünürlüğünde üretiliyor; oyun kodunun tek satırı
   değişmiyor.
   ===================================================================== */
const NETLIK = Math.min(3, Math.max(1, Math.round((window.devicePixelRatio || 1) * 2) / 2));

/* Phaser yazıyı kendi ara tuvaline çiziyor; çözünürlük verilmezse 1x
   üretilip yakınlaştırmada bulanıklaşır. Bütün yazılara varsayılan
   olarak NETLIK veriyoruz. */
(function(){
  const TS = Phaser.GameObjects.TextStyle.prototype;
  const eskiSetStyle = TS.setStyle;
  TS.setStyle = function(style, updateText, setDefaults){
    if (style && style.resolution === undefined) style.resolution = NETLIK;
    return eskiSetStyle.call(this, style, updateText, setDefaults);
  };
})();

/* Tuval NETLIK katına büyüdüğü için Phaser imleç konumunu da o ölçekte
   veriyor (0–960). Oyun koordinatına (0–480) çeviren yardımcı: sürükleme
   olayları zaten dünya koordinatı verdiği için yalnız pointer olaylarında
   kullanılıyor. */
function imlec(p){ return { x: p.x / NETLIK, y: p.y / NETLIK }; }

/* Her sahne başlarken kamerayı NETLIK katına yakınlaştırıp fizik
   dünyasını mantıksal ölçüde tutuyoruz: tuval büyüdü, dünya büyümedi.
   Sahne örnekleri oyun kurulumundan sonra eşzamansız oluştuğu için
   kanca Systems.start üzerine takılıyor — yeniden başlatmalarda da
   kendiliğinden çalışıyor. */
(function(){
  const SS = Phaser.Scenes.Systems.prototype;
  const eskiStart = SS.start;
  SS.start = function(veri){
    const sonuc = eskiStart.call(this, veri);
    const sc = this.scene;
    try{
      if (sc.cameras && sc.cameras.main){
        sc.cameras.main.setZoom(NETLIK);
        sc.cameras.main.centerOn(EN / 2, BOY / 2);
      }
      if (sc.physics && sc.physics.world) sc.physics.world.setBounds(0, 0, EN, BOY);
    }catch(e){ /* netlik ayarı oyunu engellemesin */ }
    return sonuc;
  };
})();

window.OYUN = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'oyun',
  width: EN * NETLIK,
  height: BOY * NETLIK,
  backgroundColor: '#141a24',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 760 } }
  },
  scene: [BootScene, MenuScene, GameScene, GameOverScene]
});

</script>
</body>
</html>
```

### tren-phaser.html — dragSlider (21 oyun)
Dosya boyu: 37836 bayt · 1017 satır

```html
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<title>Hızlı Tren Sinyalleri — Phaser 3</title>
<script src="https://cdn.jsdelivr.net/npm/phaser@3.80.1/dist/phaser.min.js"></script>
<style>
  html, body { margin:0; padding:0; height:100%; background:#101c17; overflow:hidden;
    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
    -webkit-tap-highlight-color: transparent; touch-action:none; }
  #oyun { width:100%; height:100%; display:flex; align-items:center; justify-content:center; }
  canvas { display:block; }
</style>
</head>
<body>
<div id="oyun"></div>
<script>
/* =====================================================================
   HIZLI TREN SİNYALLERİ — Phaser 3  (mekanik: dragSlider · 21 oyun)
   ---------------------------------------------------------------------
   Kazanım: MAT.3.1.3.c — 1000'e kadar sayıları en yakın onluklara ve
   yüzlüklere göre tasnif eder.

   Sahneler : Boot → Menu → Game → GameOver
   Fizik    : Arcade.
              · Makas kolu sürüklenir; tren ray boyunca ona yapışır.
              · Onaylanınca tren GERÇEK HIZLA tünele doğru fırlar.
              · Doğru tünel açık: tren içeri girer.
              · Yanlış tünel kapalı: tren bariyere çarpıp geri seker,
                dumanı tüter, kamera sarsılır.
   Görsel   : Bütün dokular Graphics ile çalışma anında üretilir —
              uygulama çevrimdışı kabukta (APK / iOS) çalışacağı için
              dışarıdan resim çekilmiyor.
   ===================================================================== */

const EN = 480, BOY = 800;

const RENK = {
  gokUst  : 0x16302a,
  gokAlt  : 0x2d5a49,
  dogru   : 0x34c47b,
  yanlis  : 0xf07575,
  ray     : 0x6b7a86,
  travers : 0x5a4632,
  tunel   : 0x3d4f5c,
  tunelIc : 0x121b22,
  tren    : 0xd9534f,
  vurgu   : 0xffd166
};

/* ---------------------------------------------------------------------
   İÇERİK — uygulamadaki w03 oyununun birebir aynısı.
   Başka bir dragSlider oyununa geçmek için yalnızca bu blok değişir.
   duraklar[] = hem tünel hem de kolun yapışacağı değerler.
   tolerans   : verilirse |seçim - hedef| <= tolerans kabul edilir
                (tahmin oyunları için; burada 0).
   ------------------------------------------------------------------- */
/* ---------------- uygulama köprüsü ----------------
   Adres  tren.html#oyun=w04  biçiminde; katalog verisi üst pencereden
   okunuyor. Kazanınca completeGame() çağrılır.                          */
const KOPRU = (function(){
  try{
    const p = new URLSearchParams(location.hash.slice(1));
    const id = p.get('oyun');
    if (id && window.parent && window.parent !== window &&
        typeof window.parent.getGame === 'function'){
      const g = window.parent.getGame(id);
      if (g && g.cfg) return {
        oyun: g, cfg: g.cfg,
        bitir(mesaj, puan){ try{ window.parent.completeGame(mesaj || '', puan); }catch(e){} },
        /* Turun kendi metnini uygulamanın sesiyle okutur (Piper). */
        oku(metin){ try{ if (window.parent.oku) window.parent.oku(metin); }catch(e){} },
        /* Kaybetme ekranından: bu oyunu bırak, sıradakine geç. */
        atla(){ try{ if (window.parent.sonrakiOyunaGec) window.parent.sonrakiOyunaGec(); }catch(e){} }
      };
    }
  }catch(e){ /* çapraz kaynak engeli: tek başına oynanır */ }
  return null;
})();

/* HTML varlıklarını çöz: katalogda "Pay &lt; payda" gibi yazımlar var,
   çözülmezse ekranda "&lt;" olarak görünüyor ve öyle okunuyor. */
function varlikCoz(m){
  return String(m)
    .replace(/&nbsp;/gi, ' ')
    .replace(/&lt;/gi, '<').replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"').replace(/&#39;|&apos;/gi, "'")
    .replace(/&hellip;/gi, '…').replace(/&mdash;/gi, '—').replace(/&ndash;/gi, '–')
    .replace(/&times;/gi, '×').replace(/&divide;/gi, '÷').replace(/&deg;/gi, '°')
    .replace(/&rarr;/gi, '→').replace(/&larr;/gi, '←')
    .replace(/&amp;/gi, '&');            /* en sona: çift çözmeyi önler */
}

function duzMetin(x){
  return varlikCoz(String(x == null ? '' : x).replace(/<br\s*\/?>/gi,' ')
    .replace(/<[^>]+>/g,'')).replace(/[“”]/g,'"').replace(/\s+/g,' ').trim();
}

/* KUSUR: tekSatir() TURLAR eşlemesinde çağrılıyor ama HİÇ TANIMLI DEĞİLDİ.
   Betik yüklenirken ReferenceError veriyor, TURLAR kurulamıyor ve 21
   dragSlider oyununun tamamı boş ekranla açılıyordu. */
function tekSatir(x){ return duzMetin(x).replace(/\n/g,' '); }

const VARSAYILAN = {
  instruction:'Makası çevir, treni doğru tünele yolla',
  confirmLabel:'🚦  MAKASI ÇEVİR',
  tip:'Yuvarlanacak basamağın sağındaki rakam 5 veya daha büyükse yukarı yuvarlanır.',
  rounds:[
    { prompt:'Trende 674 yazıyor.<br>En yakın ONLUĞA yuvarla!',
      min:640, max:700, step:10, target:670,
      ticks:[{v:640},{v:660},{v:670},{v:680},{v:700}],
      wrongHint:'674’ün birler basamağı 4 — 670’e daha yakın!', okMsg:'Tam isabet! 🚦' },
    { prompt:'Aynı sayı 674 · Şimdi en yakın YÜZLÜĞE yuvarla!',
      min:600, max:800, step:100, target:700,
      ticks:[{v:600},{v:700},{v:800}],
      wrongHint:'674’ün onlar basamağı 7 — 700’e daha yakın!', okMsg:'Mükemmel! 🚦' } ]
};

const CFG = KOPRU ? KOPRU.cfg : VARSAYILAN;

/* Katalog kaydırağı min–max–step ile tanımlıyor, şablon ise ayrık
   DURAKLAR listesiyle çalışıyor. Varsa ticks kullanılıyor; yoksa
   min’den max’a step ile üretiliyor (en fazla 12 durak — daha fazlası
   ekrana sığmıyor, o durumda step büyütülüyor). */
/* Durak = { deger, etiket }.
   KUSUR: eskiden yalnız t.v okunuyordu, ticks[].label ATILIYORDU. 110 tick
   etiketi değerinden farklı ("sessiz/fısıltı/normal/bağırma", "3/10",
   "1 bütün", "150 ↖ başlangıç"); çocuk anlamlı ölçeği değil çıplak sayıyı
   görüyordu. Etiket varsa o yazılıyor, karşılaştırma yine değerle. */
function duraklariUret(r){
  const bicimle = (v) => String(r.format || '{v}').replace('{v}', String(v));
  if (Array.isArray(r.ticks) && r.ticks.length){
    return r.ticks.map(t => {
      const v = (typeof t === 'object' ? t.v : t);
      if (v == null) return null;
      const et = (typeof t === 'object' && t.label != null) ? String(t.label) : bicimle(v);
      return { deger:Number(v), etiket:duzMetin(et) };
    }).filter(Boolean);
  }
  const mn = Number(r.min), mx = Number(r.max);
  let adim = Number(r.step) || 1;
  if (!isFinite(mn) || !isFinite(mx))
    return [{ deger:Number(r.target) || 0, etiket:bicimle(Number(r.target) || 0) }];
  while ((mx - mn) / adim > 11) adim *= 2;
  const d = [];
  for (let v = mn; v <= mx + 1e-9; v += adim) d.push(Math.round(v * 1000) / 1000);
  if (d.indexOf(Number(r.target)) < 0) d.push(Number(r.target));
  return d.sort((a, b) => a - b).map(v => ({ deger:v, etiket:bicimle(v) }));
}

const TURLAR = (CFG.rounds || []).map(r => ({
  seslen:   tekSatir(r.say) || tekSatir(r.prompt),
  gorev:    duzMetin(r.prompt),
  duraklar: duraklariUret(r),
  hedef:    Number(r.target),
  tolerans: Number(r.tolerance || 0),
  bicim:    String(r.format || '{v}'),
  ipucu:    duzMetin(r.wrongHint),
  tamam:    duzMetin(r.okMsg) || 'Tam isabet! 🚦',
  aciklama: duzMetin(r.revealHtml) || duzMetin(r.revealSay)
}));

const OYUN_ADI = KOPRU ? duzMetin(KOPRU.oyun.title).replace(/\n/g,' ') : 'HIZLI TREN SİNYALLERİ';
const OYUN_EMO = KOPRU ? (KOPRU.oyun.emo || '🚄') : '🚄';
const TALIMAT  = duzMetin(CFG.instruction).replace(/\n/g,' ') || 'Kaydırağı doğru değere getir';
const IPUCU    = duzMetin(CFG.tip).replace(/\n/g,' ');
const ONAY     = duzMetin(CFG.confirmLabel) || '🚦  ONAYLA';
const BASARI   = duzMetin(CFG.successMsg) || 'Bütün turları doğru bitirdin!';

const CAN_SAYISI = 3;

/* --- Yerleşim -------------------------------------------------------- */
const RAY_Y     = 356;   /* trenin üstünde durduğu ray */
const TUNEL_Y   = 306;   /* tünel ağızlarının merkezi */
const KOL_Y     = 566;   /* makas kolunun kızağı */
const TREN_HIZI = 430;   /* onaydan sonra trenin hızı (px/sn) */

/* =====================================================================
   1) BOOT — dokuları üret
   ===================================================================== */
class BootScene extends Phaser.Scene {
  constructor(){ super('Boot'); }

  create(){
    this.dokuKivilcim();
    this.dokuDuman();
    this.dokuTren();
    this.dokuKol();
    /* Uygulama içinde çocuk oyunu listeden zaten seçti; menüyü atla. */
    this.scene.start(KOPRU ? 'Game' : 'Menu');
  }

  dokuKivilcim(){
    const g = this.make.graphics({ add:false });
    g.fillStyle(0xffffff, 1);
    g.fillCircle(8, 8, 8);
    g.generateTexture('kivilcim', 16, 16);
    g.destroy();
  }

  dokuDuman(){
    const g = this.make.graphics({ add:false });
    for (let r = 14; r > 0; r--){
      g.fillStyle(0xffffff, 0.06);
      g.fillCircle(14, 14, r);
    }
    g.generateTexture('duman', 28, 28);
    g.destroy();
  }

  /* Lokomotif — sağa bakar */
  dokuTren(){
    const W = 96, H = 58;
    const g = this.make.graphics({ add:false });

    /* gövde */
    g.fillStyle(RENK.tren, 1);
    g.fillRoundedRect(6, 16, 80, 30, { tl:6, tr:14, bl:6, br:14 });
    /* kabin */
    g.fillStyle(0xb8433f, 1);
    g.fillRoundedRect(10, 4, 34, 26, 6);
    /* pencere */
    g.fillStyle(0x9fd0ff, 1);
    g.fillRoundedRect(16, 9, 22, 14, 4);
    /* baca */
    g.fillStyle(0x4a4a4a, 1);
    g.fillRoundedRect(62, 2, 14, 16, 3);
    /* ön tampon */
    g.fillStyle(0x8d99ae, 1);
    g.fillRoundedRect(84, 22, 8, 20, 3);
    /* tekerler */
    g.fillStyle(0x2a2a2a, 1);
    g.fillCircle(24, 48, 10);
    g.fillCircle(50, 48, 10);
    g.fillCircle(74, 48, 8);
    g.fillStyle(0x8d99ae, 1);
    g.fillCircle(24, 48, 4);
    g.fillCircle(50, 48, 4);
    g.fillCircle(74, 48, 3);

    g.generateTexture('tren', W, H);
    g.destroy();
  }

  /* Makas kolu — sürüklenen tutamak */
  dokuKol(){
    const W = 58, H = 64;
    const g = this.make.graphics({ add:false });
    /* taban */
    g.fillStyle(0x44566e, 1);
    g.fillRoundedRect(10, 44, 38, 16, 6);
    /* gövde */
    g.fillStyle(0x8d99ae, 1);
    g.fillRoundedRect(24, 14, 10, 34, 5);
    /* topuz */
    g.fillStyle(RENK.vurgu, 1);
    g.fillCircle(29, 14, 14);
    g.fillStyle(0xffffff, 0.55);
    g.fillCircle(24, 9, 5);
    g.generateTexture('kol', W, H);
    g.destroy();
  }
}

/* =====================================================================
   Ortak yardımcılar
   ===================================================================== */
function manzaraCiz(sc){
  const g = sc.add.graphics();
  g.fillGradientStyle(RENK.gokUst, RENK.gokUst, RENK.gokAlt, RENK.gokAlt, 1);
  g.fillRect(0, 0, EN, BOY);

  /* uzaktaki tepeler */
  g.fillStyle(0x1f4438, 1);
  g.fillEllipse(90, 250, 260, 130);
  g.fillEllipse(300, 236, 300, 150);
  g.fillEllipse(450, 258, 220, 120);

  /* süzülen bulutlar */
  for (let i = 0; i < 5; i++){
    const b = sc.add.graphics();
    b.fillStyle(0xffffff, 0.07);
    const bx = Phaser.Math.Between(0, EN), by = Phaser.Math.Between(60, 200);
    b.fillEllipse(bx, by, Phaser.Math.Between(90, 150), Phaser.Math.Between(26, 40));
    sc.tweens.add({
      targets:b, x:'+=' + Phaser.Math.Between(60, 140),
      duration:Phaser.Math.Between(9000, 16000),
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });
  }
  return g;
}

function dugmeYap(sc, x, y, metin, renk, geriCagri, genislik){
  const W = genislik || 280;
  const c = sc.add.container(x, y);
  const g = sc.add.graphics();
  g.fillStyle(renk, 1);
  g.fillRoundedRect(-W / 2, -30, W, 60, 30);
  g.fillStyle(0xffffff, 0.16);
  g.fillRoundedRect(-W / 2, -30, W, 24, { tl:30, tr:30, bl:0, br:0 });
  const t = sc.add.text(0, 0, metin, {
    fontFamily:'system-ui, sans-serif', fontSize:'24px',
    fontStyle:'bold', color:'#ffffff'
  }).setOrigin(0.5);
  c.add([g, t]);
  c.setSize(W, 60).setInteractive({ useHandCursor:true });
  c.on('pointerover', () => sc.tweens.add({ targets:c, scale:1.05, duration:110 }));
  c.on('pointerout',  () => sc.tweens.add({ targets:c, scale:1.00, duration:110 }));
  /* KUSUR: geri çağrı basma TWEEN'inin sonunda çalışıyordu (≈180ms).
     Tuş takımında aynı tuşa üst üste basıldığında bir basış yutuluyordu
     (sınamada "500000" yerine "50000" yazıldı) ve her dokunuş 180ms
     gecikmeyle işliyordu. Artık işlem HEMEN yapılıyor, tween yalnız
     görsel geri bildirim. */
  c.on('pointerdown', () => {
    sc.tweens.add({ targets:c, scale:0.93, duration:90, yoyo:true });
    if (geriCagri) geriCagri();
  });
  return c;
}

/* =====================================================================
   2) MENU
   ===================================================================== */
class MenuScene extends Phaser.Scene {
  constructor(){ super('Menu'); }

  create(){
    manzaraCiz(this);

    const tren = this.add.image(-60, 300, 'tren').setScale(1.2);
    this.tweens.add({
      targets:tren, x:EN + 70, duration:4200, repeat:-1, ease:'Linear'
    });

    const baslik = this.add.text(EN / 2, 396, OYUN_ADI, {
      fontFamily:'system-ui, sans-serif', fontSize:'42px', fontStyle:'bold',
      color:'#ffffff', align:'center', lineSpacing:5
    }).setOrigin(0.5);
    this.tweens.add({
      targets:baslik, scale:1.04, duration:1400,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });

    this.add.text(EN / 2, 474, TALIMAT, {
      fontFamily:'system-ui, sans-serif', fontSize:'21px',
      color:'#cfeee0', align:'center', wordWrap:{ width:EN - 60 }
    }).setOrigin(0.5);

    const kart = this.add.graphics();
    kart.fillStyle(0x0d1f19, 0.92);
    kart.fillRoundedRect(30, 508, EN - 60, 82, 16);
    kart.lineStyle(2, 0x3f6b58, 1);
    kart.strokeRoundedRect(30, 508, EN - 60, 82, 16);
    this.add.text(EN / 2, 549, IPUCU, {
      fontFamily:'system-ui, sans-serif', fontSize:'17px', fontStyle:'bold',
      color:'#ffd166', align:'center', wordWrap:{ width:EN - 90 }, lineSpacing:4
    }).setOrigin(0.5);

    dugmeYap(this, EN / 2, 650, '▶  BAŞLA', RENK.dogru, () => this.scene.start('Game'));

    this.add.text(EN / 2, 736, `${TURLAR.length} tren  ·  ${CAN_SAYISI} can`, {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', color:'#9fc9b6'
    }).setOrigin(0.5);
  }
}

/* =====================================================================
   3) GAME
   ===================================================================== */
class GameScene extends Phaser.Scene {
  constructor(){ super('Game'); }

  create(){
    this.can   = CAN_SAYISI;
    this.puan  = 0;
    this.seri  = 0;
    this.tur   = 0;
    this.kilit = true;

    /* Phaser sahne örneğini yeniden kullanır: TEKRAR OYNA'da bu alanlar
       önceki oyunun YOK EDİLMİŞ gruplarına işaret ediyordu ve
       turuBaslat() içindeki clear() çağrısı çöküyordu. */
    this.tunelGrubu    = null;
    this.trenGrubu     = null;
    this.tunelGorsel   = null;
    this.tunelCarpisma = null;
    this.mesaj         = null;
    this.onaylandi     = false;
    this.sonuclandi    = false;

    manzaraCiz(this);

    this.kivilcimlar = this.add.particles(0, 0, 'kivilcim', {
      speed:{ min:140, max:380 }, angle:{ min:0, max:360 },
      scale:{ start:0.9, end:0 }, alpha:{ start:1, end:0 },
      lifespan:650, gravityY:320, blendMode:'ADD', emitting:false
    }).setDepth(90);

    this.dumanlar = this.add.particles(0, 0, 'duman', {
      speed:{ min:30, max:110 }, angle:{ min:250, max:290 },
      scale:{ start:0.7, end:2.1 }, alpha:{ start:0.55, end:0 },
      lifespan:900, emitting:false
    }).setDepth(80);

    this.rayCiz();
    this.trenKur();
    this.kolKur();
    this.arayuzKur();
    this.turuBaslat();
  }

  /* ---------- ray ve traversler ---------- */
  rayCiz(){
    const g = this.add.graphics().setDepth(4);
    /* zemin şeridi */
    g.fillStyle(0x274a3d, 1);
    g.fillRect(0, RAY_Y + 6, EN, 46);
    /* traversler */
    g.fillStyle(RENK.travers, 1);
    for (let x = 6; x < EN; x += 26) g.fillRoundedRect(x, RAY_Y + 12, 16, 28, 3);
    /* raylar */
    g.fillStyle(RENK.ray, 1);
    g.fillRect(0, RAY_Y + 10, EN, 5);
    g.fillRect(0, RAY_Y + 36, EN, 5);

    /* makas kolunun kızağı */
    const k = this.add.graphics().setDepth(4);
    k.fillStyle(0x0d1f19, 0.9);
    k.fillRoundedRect(30, KOL_Y - 12, EN - 60, 24, 12);
    k.lineStyle(2, 0x3f6b58, 1);
    k.strokeRoundedRect(30, KOL_Y - 12, EN - 60, 24, 12);
  }

  /* ---------- tren ---------- */
  trenKur(){
    this.tren = this.physics.add.image(90, RAY_Y - 4, 'tren').setDepth(30);
    this.tren.body.setAllowGravity(false);
    this.tren.body.setSize(88, 50);

    /* bacadan tüten duman */
    this.baca = this.add.particles(0, 0, 'duman', {
      speed:{ min:14, max:44 }, angle:{ min:250, max:290 },
      scale:{ start:0.34, end:1.1 }, alpha:{ start:0.4, end:0 },
      lifespan:900, frequency:220
    }).setDepth(29);
    this.baca.startFollow(this.tren, 22, -26);
  }

  /* ---------- makas kolu ---------- */
  kolKur(){
    this.kol = this.add.image(EN / 2, KOL_Y - 22, 'kol').setDepth(40);
    this.kol.setInteractive({ useHandCursor:true, draggable:true });

    this.degerYazi = this.add.text(EN / 2, KOL_Y + 44, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'29px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0.5).setDepth(41);

    const tasi = (x) => {
      if (this.kilit) return;
      const d = this.enYakinDurak(x);
      this.secili = d.index;
      this.kol.x = d.x;
      this.treniHizala();
      this.degerYaziTazele();
    };

    this.input.on('dragstart', () => {
      if (this.kilit) return;
      this.tweens.add({ targets:this.kol, scale:1.14, duration:110, ease:'Back.easeOut' });
    });
    this.input.on('drag', (p, obj, x) => tasi(x));
    this.input.on('dragend', () => {
      this.tweens.add({ targets:this.kol, scale:1, duration:110 });
    });
    /* kızağa dokunmak da kolu oraya taşısın */
    this.input.on('pointerdown', (p) => {
      if (this.kilit) return;
      const im = imlec(p);
      if (im.y > KOL_Y - 60 && im.y < KOL_Y + 30) tasi(im.x);
    });
  }

  /* Ekrandaki x'e en yakın durak */
  enYakinDurak(x){
    let iyi = 0, enAz = Infinity;
    this.durakX.forEach((dx, i) => {
      const f = Math.abs(dx - x);
      if (f < enAz){ enAz = f; iyi = i; }
    });
    return { index:iyi, x:this.durakX[iyi] };
  }

  treniHizala(){
    /* tren seçilen tünelin hizasına kayar (henüz girmez) */
    const hedefX = this.durakX[this.secili];
    this.tweens.add({
      targets:{ v:this.tren.x }, v:hedefX,
      duration:220, ease:'Quad.easeOut',
      onUpdate:(tw, o) => { if (this.tren.body) this.tren.body.reset(o.v, RAY_Y - 4); }
    });
  }

  degerYaziTazele(){
    const t = TURLAR[this.tur];
    const d = t.duraklar[this.secili];
    /* Birim gösterimi (format) eskiden hiç uygulanmıyordu: açı oyununda
       "90" yazıyordu, "90°" değil. */
    this.degerYazi.setText('Seçilen:  ' + (d ? d.etiket : ''));
  }

  /* ---------- tur kurulumu ---------- */
  turuBaslat(){
    const t = TURLAR[this.tur];
    if (KOPRU) KOPRU.oku(t.seslen);
    this.kilit = true;
    this.onaylandi = false;
    this.sonuclandi = false;

    /* önceki turun tünelleri */
    if (this.tunelGrubu) this.tunelGrubu.clear(true, true);
    if (this.tunelGorsel) this.tunelGorsel.forEach(o => o.destroy());

    this.tunelGrubu  = this.physics.add.staticGroup();
    this.tunelGorsel = [];
    this.durakX      = [];

    const n = t.duraklar.length;
    t.duraklar.forEach((durak, i) => {
      const x = EN * (i + 0.5) / n;
      this.durakX.push(x);
      this.tunelYap(durak, x, i);
    });

    this.gorevYazi.setText(t.gorev);
    this.tweens.add({
      targets:this.gorevYazi, scale:{ from:0.86, to:1 }, duration:280, ease:'Back.easeOut'
    });

    /* tren ve kol ortadaki durağa */
    this.secili = Math.floor(n / 2);
    this.kol.x = this.durakX[this.secili];
    this.tren.body.reset(this.durakX[this.secili], RAY_Y - 4);
    this.tren.setAlpha(1).setScale(1).setAngle(0);
    this.tren.body.setVelocity(0, 0);
    this.degerYaziTazele();

    /* çarpışma: tren ↔ tünel ağızları (grup-vs-grup, parametre sırası korunur) */
    this.trenGrubu = this.trenGrubu || this.physics.add.group();
    if (!this.trenGrubu.contains(this.tren)){
      this.trenGrubu.add(this.tren);
      this.tren.body.setAllowGravity(false);
      this.tren.body.setSize(88, 50);
    }
    /* KUSUR: turun sonucu FİZİK ÇARPIŞMASIYLA belirleniyordu. Tren 430px/sn
       ile 36px'lik tünel ağzından geçiyor; kare gecikmesi 120ms'ye çıkarsa
       bir karede 52px yol alıp ağzı ATLIYOR, overlap hiç tetiklenmiyor ve
       tur sessizce sonuçsuz kalıyordu (tren yukarı kaçıp raya geri dönüyor,
       çocuk neden bir şey olmadığını anlamıyor). Sonuç artık ONAYLA
       anındaki seçimden belirleniyor; uçuş yalnız canlandırma. */
    if (this.tunelCarpisma){ this.tunelCarpisma.destroy(); this.tunelCarpisma = null; }

    this.time.delayedCall(320, () => { this.kilit = false; });
    this.arayuzuTazele();
  }

  /* Etiketi verilen genişliğe sığdıran en büyük puntoyu bul.
     KUSUR: etiket sabit 24px yazılıyordu; 5 duraklı turda tünel 86px
     genişliğinde ve "150 ↖ başlangıç" gibi etiketler komşu tünellerin
     üstüne biniyordu. */
  etiketYaz(x, y, W, H, metin){
    const puntolar = [23, 20, 18, 16, 14, 12, 11];
    let t = null;
    for (let i = 0; i < puntolar.length; i++){
      if (t) t.destroy();
      t = this.add.text(x, y, metin, {
        fontFamily:'system-ui, sans-serif', fontSize:puntolar[i] + 'px',
        fontStyle:'bold', color:'#ffffff', align:'center',
        wordWrap:{ width:W - 8 }, lineSpacing:1
      }).setOrigin(0.5).setDepth(11);
      if (t.width <= W - 6 && t.height <= H) break;
    }
    return t;
  }

  tunelYap(durak, x, i){
    const deger  = durak.deger;
    const etiket = durak.etiket;
    const W = Math.min(128, EN / TURLAR[this.tur].duraklar.length - 10);
    const H = 84;

    const g = this.add.graphics().setDepth(10);
    /* tünel kemeri */
    g.fillStyle(RENK.tunel, 1);
    g.fillRoundedRect(x - W / 2, TUNEL_Y - H / 2, W, H, { tl:W / 2, tr:W / 2, bl:0, br:0 });
    /* iç karanlık */
    g.fillStyle(RENK.tunelIc, 1);
    g.fillRoundedRect(x - W / 2 + 9, TUNEL_Y - H / 2 + 12, W - 18, H - 12,
                      { tl:(W - 18) / 2, tr:(W - 18) / 2, bl:0, br:0 });
    /* taş dokusu */
    g.lineStyle(2, 0x51697a, 0.6);
    g.strokeRoundedRect(x - W / 2, TUNEL_Y - H / 2, W, H, { tl:W / 2, tr:W / 2, bl:0, br:0 });

    /* Etiket tünelin İÇİNDE dursun: alt kenara yazılınca ray üstündeki
       tren üzerine biniyor ve sayı okunmuyordu. */
    const et = this.etiketYaz(x, TUNEL_Y + 2, W, 62, etiket);

    this.tunelGorsel.push(g, et);

    /* Ağız algılayıcısı. Trenin ray üzerindeki gövdesiyle ÇAKIŞMAMALI:
       çakışırsa tur, oyuncu makası çevirmeden kendiliğinden geçiyor. */
    const agiz = this.add.rectangle(x, TUNEL_Y - 10, W - 22, 36, 0, 0);
    this.tunelGrubu.add(agiz);
    agiz.setData('deger', deger);
    agiz.setData('index', i);
  }

  /* ---------- onay ---------- */
  /* Seçilen durağın tünel ağzı nesnesi (parçacık/bariyer konumu için). */
  agizBul(si){
    const liste = this.tunelGrubu ? this.tunelGrubu.getChildren() : [];
    for (let i = 0; i < liste.length; i++)
      if (liste[i].getData('index') === si) return liste[i];
    return { x:this.durakX[si] || EN / 2, y:TUNEL_Y };
  }

  onayla(){
    if (this.kilit) return;
    this.kilit = true;

    const t = TURLAR[this.tur];
    this.onaylandi = true;
    const si = this.secili;
    this.secilenDeger = t.duraklar[si].deger;

    /* Tren tünele doğru süzülür. Konum gövde üzerinden yürüyor ki fizik
       bir sonraki karede treni geri çekmesin. */
    this.tren.body.reset(this.durakX[si], RAY_Y - 4);
    this.tren.body.setVelocity(0, 0);
    this.tweens.add({ targets:this.tren, angle:-90, duration:260, ease:'Quad.easeOut' });
    this.baca.setFrequency(60);
    this.dumanlar.explode(10, this.tren.x, this.tren.y + 20);
    this.cameras.main.shake(140, 0.004);

    const basY = RAY_Y - 4, bitY = TUNEL_Y - 6;
    this.tweens.add({
      targets:{ p:0 }, p:1, duration:420, ease:'Quad.easeIn',
      onUpdate:(tw, o) => {
        if (this.tren && this.tren.body)
          this.tren.body.reset(this.durakX[si], basY + (bitY - basY) * o.p);
      },
      onComplete:() => this.sonucuVer(si)
    });
  }

  /* Turu sonuçlandır: seçim ONAYLA anında bilindiği için çarpışma beklemeye
     gerek yok (bkz. turuBaslat'taki not). */
  sonucuVer(si){
    if (this.sonuclandi) return;
    if (this.tur >= TURLAR.length) return;
    this.sonuclandi = true;
    const t = TURLAR[this.tur];
    const agiz = this.agizBul(si);
    const fark = Math.abs(t.duraklar[si].deger - t.hedef);
    if (fark <= (t.tolerans || 0)) this.dogru(agiz);
    else                           this.yanlis(agiz);
  }

  /* Artık bağlı değil: sonucu sonucuVer() belirliyor. Geriye dönük
     uyumluluk için bırakıldı. */
  tuneleGirdi(tren, agiz){
    if (this.tur >= TURLAR.length) return;               /* oyun bitti */
    if (!this.onaylandi || this.sonuclandi) return;      /* makas çevrilmeden sayılmaz */
    if (agiz.getData('index') !== this.secili) return;   /* yalnız hedeflenen tünel */
    this.sonuclandi = true;

    const t = TURLAR[this.tur];
    const fark = Math.abs(agiz.getData('deger') - t.hedef);
    if (fark <= (t.tolerans || 0)) this.dogru(agiz);
    else                           this.yanlis(agiz);
  }

  dogru(agiz){
    const t = TURLAR[this.tur];
    this.seri++;
    const kazanc = 100 + (this.seri - 1) * 25;
    this.puan += kazanc;

    /* tren tünelin karanlığına girip kaybolur */
    this.tweens.add({
      targets:this.tren, y:TUNEL_Y - 30, alpha:0, scale:0.75,
      duration:420, ease:'Quad.easeIn',
      onComplete:() => {
        this.tren.body.setVelocity(0, 0);
        this.kivilcimlar.setParticleTint(RENK.dogru);
        this.kivilcimlar.explode(28, agiz.x, TUNEL_Y);
      }
    });

    this.puanYazi.setText('Puan ' + this.puan);
    this.tweens.add({
      targets:this.puanYazi, scale:1.5, duration:140, yoyo:true, ease:'Back.easeOut'
    });

    const ucan = this.add.text(agiz.x, TUNEL_Y + 60, '+' + kazanc, {
      fontFamily:'system-ui, sans-serif', fontSize:'31px', fontStyle:'bold',
      color:'#7ce0a3'
    }).setOrigin(0.5).setDepth(95);
    this.tweens.add({
      targets:ucan, y:ucan.y - 70, alpha:0, scale:1.2,
      duration:760, ease:'Cubic.easeOut', onComplete:() => ucan.destroy()
    });

    this.mesajGoster(t.tamam + '  ·  ' + t.aciklama, '#1f6d4a');
    this.cameras.main.flash(150, 80, 210, 140);
    if (this.seri >= 2) this.seriGoster();

    this.tur++;
    this.arayuzuTazele();

    this.time.delayedCall(2000, () => {
      this.baca.setFrequency(220);
      /* Oyun bitiyorsa bayrağı BIRAKMA: sahne değişene kadar geçen
         karelerde tren hâlâ tünelde ve overlap yeniden tetikleniyordu
         (TURLAR[tur] artık tanımsız olduğu için hata veriyordu). */
      if (this.tur >= TURLAR.length){ this.bitir(true); return; }
      this.sonuclandi = false;
      this.turuBaslat();
    });
  }

  yanlis(agiz){
    const t = TURLAR[this.tur];
    this.seri = 0;
    this.can--;
    this.arayuzuTazele();

    /* GERÇEK FİZİK: tünel kapalı — tren çarpıp geri seker */
    this.tren.body.setVelocityY(300);
    this.tren.body.setVelocityX(Phaser.Math.Between(-90, 90));
    this.tweens.add({ targets:this.tren, angle:Phaser.Math.Between(-12, 12), duration:220, yoyo:true });

    this.dumanlar.explode(20, this.tren.x, this.tren.y - 10);
    this.cameras.main.shake(260, 0.014);
    this.cameras.main.flash(180, 220, 90, 90);

    /* tünel ağzında kırmızı bariyer yanıp sönsün */
    const bar = this.add.graphics().setDepth(12);
    bar.fillStyle(RENK.yanlis, 0.85);
    bar.fillRoundedRect(agiz.x - 44, TUNEL_Y - 6, 88, 12, 6);
    this.tweens.add({
      targets:bar, alpha:0, duration:700, delay:300,
      onComplete:() => bar.destroy()
    });

    this.tweens.add({
      targets:this.canYazi, angle:{ from:-12, to:12 },
      duration:70, yoyo:true, repeat:3,
      onComplete:() => this.canYazi.setAngle(0)
    });

    this.mesajGoster(t.ipucu, '#b5453b');

    this.time.delayedCall(1300, () => {
      this.sonuclandi = false;
      this.baca.setFrequency(220);
      if (this.can <= 0){ this.bitir(false); return; }
      /* tren raya geri dönsün, oyuncu yeniden denesin */
      this.tren.body.reset(this.durakX[this.secili], RAY_Y - 4);
      this.tren.body.setVelocity(0, 0);
      this.tren.setAngle(0);
      this.onaylandi = false;
      this.kilit = false;
    });
  }

  seriGoster(){
    this.seriYazi.setText('🔥 ' + this.seri + ' SERİ!').setAlpha(1).setScale(0.6);
    this.tweens.add({ targets:this.seriYazi, scale:1, duration:220, ease:'Back.easeOut' });
    this.tweens.add({ targets:this.seriYazi, alpha:0, delay:900, duration:400 });
  }

  mesajGoster(metin, arka){
    if (this.mesaj) this.mesaj.destroy();
    this.mesaj = this.add.text(EN / 2, 452, metin, {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#ffffff', backgroundColor:arka,
      padding:{ x:13, y:9 }, align:'center', wordWrap:{ width:EN - 60 }, lineSpacing:3
    }).setOrigin(0.5).setDepth(96).setAlpha(0);
    const t = this.mesaj;
    this.tweens.add({ targets:t, alpha:1, duration:150 });
    this.time.delayedCall(1900, () => {
      if (!t.active) return;
      this.tweens.add({
        targets:t, alpha:0, duration:250,
        onComplete:() => { if (this.mesaj === t) this.mesaj = null; t.destroy(); }
      });
    });
  }

  /* ---------- arayüz ---------- */
  arayuzKur(){
    /* Katalogda yönerge 120 karaktere çıkıyor; sabit yükseklikli şerit
       yazıyı iki yandan kesiyordu. Şerit metnin gerçek boyuna göre. */
    const yon = this.add.text(EN / 2, 22, OYUN_EMO + '  ' + TALIMAT, {
      fontFamily:'system-ui, sans-serif',
      fontSize: (TALIMAT.length > 92 ? '16px' : (TALIMAT.length > 54 ? '17px' : '20px')),
      fontStyle:'bold', color:'#ffffff', align:'center',
      wordWrap:{ width:EN - 52 }, lineSpacing:3
    }).setOrigin(0.5, 0).setDepth(61);

    const seritBoy = Math.max(104, yon.height + 62);
    const serit = this.add.graphics().setDepth(60);
    serit.fillStyle(0x0b1712, 0.97);
    serit.fillRoundedRect(10, 10, EN - 20, seritBoy, 18);
    yon.setDepth(61);
    const satirY = 10 + seritBoy - 22;
    this.seritAlt = 10 + seritBoy;

    this.puanYazi = this.add.text(30, satirY, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0, 0.5).setDepth(61);

    this.canYazi = this.add.text(EN - 30, satirY, '', { fontSize:'20px' })
      .setOrigin(1, 0.5).setDepth(61);

    this.ilerlemeYazi = this.add.text(EN / 2, satirY, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#9fc9b6'
    }).setOrigin(0.5).setDepth(61);

    this.gorevYazi = this.add.text(EN / 2, this.seritAlt + 34, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'22px', fontStyle:'bold',
      color:'#ffffff', align:'center', wordWrap:{ width:EN - 50 }, lineSpacing:4
    }).setOrigin(0.5).setDepth(61);

    this.seriYazi = this.add.text(EN / 2, this.seritAlt + 96, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'24px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0.5).setDepth(62).setAlpha(0);

    dugmeYap(this, EN / 2, 682, ONAY, RENK.dogru, () => this.onayla(), 300).setDepth(45);

    this.arayuzuTazele();
  }

  arayuzuTazele(){
    this.canYazi.setText(
      '❤️'.repeat(Math.max(0, this.can)) +
      '🖤'.repeat(Math.max(0, CAN_SAYISI - this.can))
    );
    this.ilerlemeYazi.setText(`${this.tur} / ${TURLAR.length} tren`);
  }

  bitir(kazandi){
    /* Uygulama içindeyken kazanma ekranını uygulama gösteriyor. */
    if (kazandi && KOPRU){ KOPRU.bitir(BASARI, this.puan); return; }
    this.scene.start('GameOver', {
      kazandi, puan:this.puan, can:this.can,
      tur:this.tur, toplam:TURLAR.length
    });
  }

  /* ---------- her kare ---------- */
  update(){
    /* "Yukarı kaçan treni geri al" kurtarması KALDIRILDI: tren artık
       serbest uçmuyor, uçuş tween'i tünel ağzında bitiyor. Eski kurtarma
       onaylandi bayrağını sıfırlamadığı için tur kilitli kalıyordu. */
    /* rayın altına düşen treni geri al */
    if (this.tren && this.tren.body && this.tren.y > RAY_Y + 90){
      this.tren.body.reset(this.durakX[this.secili], RAY_Y - 4);
      this.tren.body.setVelocity(0, 0);
    }
  }
}

/* =====================================================================
   4) GAME OVER
   ===================================================================== */
class GameOverScene extends Phaser.Scene {
  constructor(){ super('GameOver'); }

  init(veri){ this.veri = veri; }

  create(){
    const { kazandi, puan, can, tur, toplam } = this.veri;
    manzaraCiz(this);

    const emo = this.add.text(EN / 2, 190, kazandi ? '🚄' : '💪', { fontSize:'97px' })
      .setOrigin(0.5).setScale(0);
    this.tweens.add({ targets:emo, scale:1, duration:520, ease:'Back.easeOut' });

    this.add.text(EN / 2, 300, kazandi ? 'ŞEF MAKASÇI!' : 'TEKRAR DENE', {
      fontFamily:'system-ui, sans-serif', fontSize:'35px', fontStyle:'bold',
      color: kazandi ? '#7ce0a3' : '#ffd166', align:'center'
    }).setOrigin(0.5);

    this.add.text(EN / 2, 360,
      kazandi ? BASARI : `${tur} / ${toplam} treni yolladın — bir daha deneyelim mi?`, {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#cfeee0',
      align:'center', wordWrap:{ width:EN - 70 }, lineSpacing:5
    }).setOrigin(0.5);

    const puanYazi = this.add.text(EN / 2, 456, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'42px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0.5);
    const sayac = { v:0 };
    this.tweens.add({
      targets:sayac, v:puan, duration:900, ease:'Cubic.easeOut',
      onUpdate:() => puanYazi.setText('Puan ' + Math.round(sayac.v))
    });

    this.add.text(EN / 2, 506,
      'Kalan can: ' + (can > 0 ? '❤️'.repeat(can) : '—'), {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#9fc9b6'
    }).setOrigin(0.5);

    if (kazandi){
      const konfeti = this.add.particles(EN / 2, -20, 'kivilcim', {
        speed:{ min:90, max:260 }, angle:{ min:60, max:120 },
        scale:{ start:0.8, end:0 }, alpha:{ start:1, end:0 },
        lifespan:2000, gravityY:180, quantity:2, frequency:70,
        tint:[0xffd166, 0x7ce0a3, 0x7fb2f0, 0xf07575]
      }).setDepth(5);
      this.time.delayedCall(2600, () => konfeti.stop());
    }

    dugmeYap(this, EN / 2, 606, '↻  TEKRAR OYNA', RENK.dogru, () => this.scene.start('Game'));

    /* Uygulama içinde: bu oyunda takılan çocuk sıradakine geçebilsin. */

    if (KOPRU) dugmeYap(this, EN / 2, 680, '⏭  SIRADAKİ OYUN', 0x4a679e, () => KOPRU.atla());
    if (!KOPRU) dugmeYap(this, EN / 2, 684, '☰  MENÜ',        0x3f6b58, () => this.scene.start('Menu'));
  }
}

/* =====================================================================
   OYUNU BAŞLAT
   ===================================================================== */
/* =====================================================================
   NETLİK — cihazın piksel yoğunluğunda çizim
   ---------------------------------------------------------------------
   Oyun 480x800 mantıksal tuvalde çiziliyordu; telefon bunu 1080 piksele
   büyütünce yazılar ve kenarlar bulanıklaşıyordu. Çözüm: tuvali cihazın
   gerçek piksel sayısında açmak, dünyayı ise kamerayı NETLIK katına
   yakınlaştırarak yine 480x800 koordinatta tutmak. Böylece Graphics ile
   çizilen her şey (kartlar, şeritler, kutular) vektör keskinliğinde,
   yazılar da NETLIK çözünürlüğünde üretiliyor; oyun kodunun tek satırı
   değişmiyor.
   ===================================================================== */
const NETLIK = Math.min(3, Math.max(1, Math.round((window.devicePixelRatio || 1) * 2) / 2));

/* Phaser yazıyı kendi ara tuvaline çiziyor; çözünürlük verilmezse 1x
   üretilip yakınlaştırmada bulanıklaşır. Bütün yazılara varsayılan
   olarak NETLIK veriyoruz. */
(function(){
  const TS = Phaser.GameObjects.TextStyle.prototype;
  const eskiSetStyle = TS.setStyle;
  TS.setStyle = function(style, updateText, setDefaults){
    if (style && style.resolution === undefined) style.resolution = NETLIK;
    return eskiSetStyle.call(this, style, updateText, setDefaults);
  };
})();

/* Tuval NETLIK katına büyüdüğü için Phaser imleç konumunu da o ölçekte
   veriyor (0–960). Oyun koordinatına (0–480) çeviren yardımcı: sürükleme
   olayları zaten dünya koordinatı verdiği için yalnız pointer olaylarında
   kullanılıyor. */
function imlec(p){ return { x: p.x / NETLIK, y: p.y / NETLIK }; }

/* Her sahne başlarken kamerayı NETLIK katına yakınlaştırıp fizik
   dünyasını mantıksal ölçüde tutuyoruz: tuval büyüdü, dünya büyümedi.
   Sahne örnekleri oyun kurulumundan sonra eşzamansız oluştuğu için
   kanca Systems.start üzerine takılıyor — yeniden başlatmalarda da
   kendiliğinden çalışıyor. */
(function(){
  const SS = Phaser.Scenes.Systems.prototype;
  const eskiStart = SS.start;
  SS.start = function(veri){
    const sonuc = eskiStart.call(this, veri);
    const sc = this.scene;
    try{
      if (sc.cameras && sc.cameras.main){
        sc.cameras.main.setZoom(NETLIK);
        sc.cameras.main.centerOn(EN / 2, BOY / 2);
      }
      if (sc.physics && sc.physics.world) sc.physics.world.setBounds(0, 0, EN, BOY);
    }catch(e){ /* netlik ayarı oyunu engellemesin */ }
    return sonuc;
  };
})();

window.OYUN = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'oyun',
  width: EN * NETLIK,
  height: BOY * NETLIK,
  backgroundColor: '#101c17',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 620 } }
  },
  scene: [BootScene, MenuScene, GameScene, GameOverScene]
});

</script>
</body>
</html>
```

### tamirhane-phaser.html — punctFix (16 oyun)
Dosya boyu: 36777 bayt · 1020 satır

```html
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<title>Noktalama Tamirhanesi — Phaser 3</title>
<script src="https://cdn.jsdelivr.net/npm/phaser@3.80.1/dist/phaser.min.js"></script>
<style>
  html, body { margin:0; padding:0; height:100%; background:#191521; overflow:hidden;
    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
    -webkit-tap-highlight-color: transparent; touch-action:none; }
  #oyun { width:100%; height:100%; display:flex; align-items:center; justify-content:center; }
  canvas { display:block; }
</style>
</head>
<body>
<div id="oyun"></div>
<script>
/* =====================================================================
   NOKTALAMA TAMİRHANESİ — Phaser 3   (mekanik: punctFix · 16 oyun)
   ---------------------------------------------------------------------
   Kazanım: T.Y.3.3.f / g — Büyük harfleri ve noktalama işaretlerini
   kuralına uygun kullanır.

   Sahneler : Boot → Menu → Game → GameOver
   Fizik    : Arcade.
              · Noktalama işaretleri sandığa YERÇEKİMİYLE dökülür ve
                üst üste yığılır.
              · İşaret yuvaya sürüklenir; yanlışsa geri fırlayıp
                sandığa düşer.
              · Bozuk sözcükler tezgâhta titrer, onarılınca yerine oturur.
   Görsel   : Bütün dokular Graphics ile çalışma anında üretilir —
              uygulama çevrimdışı kabukta (APK / iOS) çalışacağı için
              dışarıdan resim çekilmiyor.
   ===================================================================== */

const EN = 480, BOY = 800;

const RENK = {
  zeminUst : 0x231d33,
  zeminAlt : 0x3b3150,
  dogru    : 0x34c47b,
  yanlis   : 0xf07575,
  kart     : 0xfdfbff,
  kartKnr  : 0xd6cfe4,
  bozuk    : 0xf0a0a0,
  yuva     : 0x2b2440,
  isaret   : 0xffe6a8,
  metin    : '#2a2140',
  vurgu    : 0xffd166
};

/* ---------------------------------------------------------------------
   İÇERİK — uygulamadaki y05 oyununun birebir aynısı.
   Başka bir punctFix oyununa geçmek için yalnızca bu blok değişir.
   onarim: { buyuk:[sözcük indeksleri], isaret:{ indeks: 'işaret' } }
           isaret anahtarı = o sözcüğün SAĞINDAKİ yuva.
   ------------------------------------------------------------------- */
/* ---------------- uygulama köprüsü ----------------
   Adres  tamirhane.html#oyun=u04  biçiminde; katalog verisi üst pencereden
   okunuyor. Kazanınca completeGame() çağrılır.                          */
const KOPRU = (function(){
  try{
    const p = new URLSearchParams(location.hash.slice(1));
    const id = p.get('oyun');
    if (id && window.parent && window.parent !== window &&
        typeof window.parent.getGame === 'function'){
      const g = window.parent.getGame(id);
      if (g && g.cfg) return {
        oyun: g, cfg: g.cfg,
        bitir(mesaj, puan){ try{ window.parent.completeGame(mesaj || '', puan); }catch(e){} },
        /* Turun kendi metnini uygulamanın sesiyle okutur (Piper). */
        oku(metin){ try{ if (window.parent.oku) window.parent.oku(metin); }catch(e){} },
        /* Kaybetme ekranından: bu oyunu bırak, sıradakine geç. */
        atla(){ try{ if (window.parent.sonrakiOyunaGec) window.parent.sonrakiOyunaGec(); }catch(e){} }
      };
    }
  }catch(e){ /* çapraz kaynak engeli: tek başına oynanır */ }
  return null;
})();

/* HTML varlıklarını çöz: katalogda "Pay &lt; payda" gibi yazımlar var,
   çözülmezse ekranda "&lt;" olarak görünüyor ve öyle okunuyor. */
function varlikCoz(m){
  return String(m)
    .replace(/&nbsp;/gi, ' ')
    .replace(/&lt;/gi, '<').replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"').replace(/&#39;|&apos;/gi, "'")
    .replace(/&hellip;/gi, '…').replace(/&mdash;/gi, '—').replace(/&ndash;/gi, '–')
    .replace(/&times;/gi, '×').replace(/&divide;/gi, '÷').replace(/&deg;/gi, '°')
    .replace(/&rarr;/gi, '→').replace(/&larr;/gi, '←')
    .replace(/&amp;/gi, '&');            /* en sona: çift çözmeyi önler */
}

function duzMetin(x){
  return varlikCoz(String(x == null ? '' : x).replace(/<br\s*\/?>/gi,' ')
    .replace(/<[^>]+>/g,'')).replace(/[“”]/g,'"').replace(/\s+/g,' ').trim();
}

const VARSAYILAN = {
  instruction:'Sözcüğe dokun, işareti yuvaya tak',
  tip:'Cümle başı ve özel adlar büyük harfle · Bitmiş cümle: nokta',
  marks:['.', ',', '?', '!'],
  rounds:[
    { prompt:'Cümle başını büyük harfle başlat, sonuna nokta koy.',
      tokens:['ali','kardeşine','kitabını','verdi'],
      fixes:[{type:'caps',at:0},{type:'punct',at:3,mark:'.'}],
      okMsg:'Onarıldı! ✍️' },
    { prompt:'Bu bir SORU cümlesi — uygun işareti bul.',
      tokens:['sen','de','bizimle','gelir','misin'],
      fixes:[{type:'caps',at:0},{type:'punct',at:4,mark:'?'}],
      okMsg:'Soru işareti yerinde! ❓' } ]
};

const CFG = KOPRU ? KOPRU.cfg : VARSAYILAN;

/* Katalog düzeltmeleri  fixes:[{type:'caps',at} | {type:'punct',at,mark}]
   biçiminde veriyor; şablon ise  onarim:{buyuk:[i], isaret:{i:mark}}
   bekliyor. Dönüşüm burada. */
function onarimCevir(fixes){
  const buyuk = [], isaret = {};
  (fixes || []).forEach(d => {
    if (!d) return;
    if (d.type === 'caps') buyuk.push(Number(d.at));
    else if (d.type === 'punct') isaret[Number(d.at)] = String(d.mark);
  });
  return { buyuk, isaret };
}

const ISARETLER = (CFG.marks || ['.', ',', '?', '!']).map(String);

const TURLAR = (CFG.rounds || []).map(r => ({
  gorev:     duzMetin(r.prompt),
  sozcukler: (r.tokens || []).map(x => duzMetin(x)),
  onarim:    onarimCevir(r.fixes),
  tamam:     duzMetin(r.okMsg) || 'Onarıldı! ✍️',
  aciklama:  duzMetin(r.revealHtml) || duzMetin(r.revealSay)
}));

const OYUN_ADI = KOPRU ? duzMetin(KOPRU.oyun.title).replace(/\n/g,' ') : 'NOKTALAMA TAMİRHANESİ';
const OYUN_EMO = KOPRU ? (KOPRU.oyun.emo || '✍️') : '✍️';
const TALIMAT  = duzMetin(CFG.instruction).replace(/\n/g,' ') || 'Sözcüğe dokun, işareti yuvaya tak';
const IPUCU    = duzMetin(CFG.tip).replace(/\n/g,' ');
const BASARI   = duzMetin(CFG.successMsg) || 'Bütün düzeltmeleri yaptın!';

const CAN_SAYISI = 3;

/* --- Yerleşim -------------------------------------------------------- */
const TEZGAH_UST = 232;   /* sözcük satırlarının başladığı yer */
const SATIR_BOY  = 52;
const SANDIK_UST = 470;
const SANDIK_ALT = 606;

/* =====================================================================
   1) BOOT — dokuları üret
   ===================================================================== */
class BootScene extends Phaser.Scene {
  constructor(){ super('Boot'); }

  create(){
    this.dokuKivilcim();
    this.dokuToz();
    /* Uygulama içinde çocuk oyunu listeden zaten seçti; menüyü atla. */
    this.scene.start(KOPRU ? 'Game' : 'Menu');
  }

  dokuKivilcim(){
    const g = this.make.graphics({ add:false });
    g.fillStyle(0xffffff, 1);
    g.fillCircle(8, 8, 8);
    g.generateTexture('kivilcim', 16, 16);
    g.destroy();
  }

  dokuToz(){
    const g = this.make.graphics({ add:false });
    for (let r = 14; r > 0; r--){
      g.fillStyle(0xffffff, 0.06);
      g.fillCircle(14, 14, r);
    }
    g.generateTexture('toz', 28, 28);
    g.destroy();
  }
}

/* =====================================================================
   Ortak yardımcılar
   ===================================================================== */
function atolyeCiz(sc){
  const g = sc.add.graphics();
  g.fillGradientStyle(RENK.zeminUst, RENK.zeminUst, RENK.zeminAlt, RENK.zeminAlt, 1);
  g.fillRect(0, 0, EN, BOY);

  for (let i = 0; i < 24; i++){
    const s = sc.add.circle(
      Phaser.Math.Between(6, EN - 6),
      Phaser.Math.Between(6, BOY - 6),
      Phaser.Math.FloatBetween(1.5, 3.5),
      0xffffff,
      Phaser.Math.FloatBetween(0.04, 0.12)
    );
    sc.tweens.add({
      targets:s, alpha:0.02,
      duration:Phaser.Math.Between(1400, 3000),
      yoyo:true, repeat:-1, delay:Phaser.Math.Between(0, 2000)
    });
  }
  return g;
}

function dugmeYap(sc, x, y, metin, renk, geriCagri){
  const c = sc.add.container(x, y);
  const g = sc.add.graphics();
  g.fillStyle(renk, 1);
  g.fillRoundedRect(-140, -30, 280, 60, 30);
  g.fillStyle(0xffffff, 0.16);
  g.fillRoundedRect(-140, -30, 280, 24, { tl:30, tr:30, bl:0, br:0 });
  const t = sc.add.text(0, 0, metin, {
    fontFamily:'system-ui, sans-serif', fontSize:'25px',
    fontStyle:'bold', color:'#ffffff'
  }).setOrigin(0.5);
  c.add([g, t]);
  c.setSize(280, 60).setInteractive({ useHandCursor:true });
  c.on('pointerover', () => sc.tweens.add({ targets:c, scale:1.05, duration:110 }));
  c.on('pointerout',  () => sc.tweens.add({ targets:c, scale:1.00, duration:110 }));
  c.on('pointerdown', () => sc.tweens.add({
    targets:c, scale:0.93, duration:90, yoyo:true, onComplete:geriCagri
  }));
  return c;
}

/* =====================================================================
   2) MENU
   ===================================================================== */
class MenuScene extends Phaser.Scene {
  constructor(){ super('Menu'); }

  create(){
    atolyeCiz(this);

    this.add.text(EN / 2, 178, OYUN_EMO, { fontSize:'90px' }).setOrigin(0.5);
    const isaretler = this.add.text(EN / 2, 252, '.   ,   ?   !', {
      fontFamily:'system-ui, sans-serif', fontSize:'48px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0.5);
    this.tweens.add({
      targets:isaretler, y:262, duration:1500,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });

    const baslik = this.add.text(EN / 2, 348, OYUN_ADI, {
      fontFamily:'system-ui, sans-serif', fontSize:'40px', fontStyle:'bold',
      color:'#ffffff', align:'center', lineSpacing:5
    }).setOrigin(0.5);
    this.tweens.add({
      targets:baslik, scale:1.04, duration:1400,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });

    this.add.text(EN / 2, 434, TALIMAT, {
      fontFamily:'system-ui, sans-serif', fontSize:'22px',
      color:'#ded4ff', align:'center'
    }).setOrigin(0.5);

    const kart = this.add.graphics();
    kart.fillStyle(0x1a1526, 0.92);
    kart.fillRoundedRect(28, 470, EN - 56, 86, 16);
    kart.lineStyle(2, 0x554873, 1);
    kart.strokeRoundedRect(28, 470, EN - 56, 86, 16);
    this.add.text(EN / 2, 513, IPUCU, {
      fontFamily:'system-ui, sans-serif', fontSize:'17px', fontStyle:'bold',
      color:'#ffd166', align:'center', wordWrap:{ width:EN - 86 }, lineSpacing:4
    }).setOrigin(0.5);

    dugmeYap(this, EN / 2, 622, '▶  BAŞLA', RENK.dogru, () => this.scene.start('Game'));

    this.add.text(EN / 2, 716, `${TURLAR.length} cümle  ·  ${CAN_SAYISI} can`, {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', color:'#b3a6dd'
    }).setOrigin(0.5);
  }
}

/* =====================================================================
   3) GAME
   ===================================================================== */
class GameScene extends Phaser.Scene {
  constructor(){ super('Game'); }

  create(){
    this.can   = CAN_SAYISI;
    this.puan  = 0;
    this.seri  = 0;
    this.tur   = 0;
    this.kilit = true;
    this.suruklenen = null;

    /* Phaser sahne örneğini yeniden kullanır — TEKRAR OYNA'da eski
       (yok edilmiş) gruplara işaret etmesinler. */
    this.sozcukler = null;
    this.yuvalar   = null;
    this.isaretler = null;
    this.mesaj     = null;

    atolyeCiz(this);

    this.kivilcimlar = this.add.particles(0, 0, 'kivilcim', {
      speed:{ min:140, max:380 }, angle:{ min:0, max:360 },
      scale:{ start:0.85, end:0 }, alpha:{ start:1, end:0 },
      lifespan:620, gravityY:340, blendMode:'ADD', emitting:false
    }).setDepth(90);

    this.tozlar = this.add.particles(0, 0, 'toz', {
      speed:{ min:40, max:150 }, angle:{ min:200, max:340 },
      scale:{ start:1, end:2.2 }, alpha:{ start:0.5, end:0 },
      lifespan:680, emitting:false
    }).setDepth(80);

    this.sahneKur();
    this.arayuzKur();
    this.surukleKur();
    this.turuBaslat();
  }

  /* ---------- sabit sahne ---------- */
  sahneKur(){
    /* tezgâh */
    const g = this.add.graphics().setDepth(4);
    g.fillStyle(0x1a1526, 0.9);
    g.fillRoundedRect(14, TEZGAH_UST - 30, EN - 28, 190, 14);
    g.lineStyle(2, 0x554873, 1);
    g.strokeRoundedRect(14, TEZGAH_UST - 30, EN - 28, 190, 14);
    this.add.text(24, TEZGAH_UST - 22, 'TEZGÂH', {
      fontFamily:'system-ui, sans-serif', fontSize:'14px', fontStyle:'bold',
      color:'#8a7cb8'
    }).setDepth(5);

    /* işaret sandığı */
    const k = this.add.graphics().setDepth(4);
    k.fillStyle(0x1a1526, 0.9);
    k.fillRoundedRect(24, SANDIK_UST - 26, EN - 48, SANDIK_ALT - SANDIK_UST + 46, 14);
    k.lineStyle(2, 0x554873, 1);
    k.strokeRoundedRect(24, SANDIK_UST - 26, EN - 48, SANDIK_ALT - SANDIK_UST + 46, 14);
    this.add.text(EN / 2, SANDIK_UST - 12, 'İŞARET SANDIĞI', {
      fontFamily:'system-ui, sans-serif', fontSize:'14px', fontStyle:'bold',
      color:'#8a7cb8'
    }).setOrigin(0.5).setDepth(5);

    /* NOT: Phaser'da collider(grup, TEK nesne) callback'e parametreleri
       ters veriyor; engeller staticGroup içinde. */
    this.sandikDuvar = this.physics.add.staticGroup();
    this.sandikDuvar.add(this.add.rectangle(EN / 2, SANDIK_ALT + 8, EN - 60, 16, 0, 0));
    this.sandikDuvar.add(this.add.rectangle(30,      BOY / 2, 14, BOY * 2, 0, 0));
    this.sandikDuvar.add(this.add.rectangle(EN - 30, BOY / 2, 14, BOY * 2, 0, 0));

    this.isaretler = this.physics.add.group();
    this.physics.add.collider(this.isaretler, this.sandikDuvar);
    this.physics.add.collider(this.isaretler, this.isaretler);
  }

  /* ---------- tur kurulumu ---------- */
  turuBaslat(){
    const t = TURLAR[this.tur];
    this.kilit = true;
    this.nesil = (this.nesil || 0) + 1;

    if (this.sozcukNesne) this.sozcukNesne.forEach(o => o.destroy());
    if (this.yuvaNesne)   this.yuvaNesne.forEach(o => o.destroy());
    this.isaretler.clear(true, true);

    this.sozcukNesne = [];
    this.yuvaNesne   = [];
    this.kalanBuyuk  = t.onarim.buyuk.slice();
    this.kalanIsaret = Object.keys(t.onarim.isaret).map(Number);

    this.gorevYazi.setText(t.gorev);
    this.tweens.add({
      targets:this.gorevYazi, scale:{ from:0.86, to:1 }, duration:280, ease:'Back.easeOut'
    });

    this.cumleyiDiz(t);
    this.sandigiDoldur();
    this.kalanTazele();

    this.time.delayedCall(500, () => { this.kilit = false; });
    this.arayuzuTazele();
  }

  /* Sözcükleri ve her sözcüğün sağındaki yuvayı satır sararak diz */
  cumleyiDiz(t){
    const SOL = 30, SAG = EN - 30, YUVA_EN = 22, ARA = 7;

    /* önce genişlikleri ölç */
    const olcu = t.sozcukler.map(s => {
      const gecici = this.add.text(0, 0, s, {
        fontFamily:'system-ui, sans-serif', fontSize:'22px', fontStyle:'bold'
      });
      const w = Math.max(40, gecici.width + 18);
      gecici.destroy();
      return w;
    });

    /* satırlara böl */
    const satirlar = [];
    let satir = [], genislik = 0;
    olcu.forEach((w, i) => {
      const parca = w + YUVA_EN + ARA;
      if (genislik + parca > SAG - SOL && satir.length){
        satirlar.push({ ogeler:satir, genislik:genislik - ARA });
        satir = []; genislik = 0;
      }
      satir.push({ i, w });
      genislik += parca;
    });
    if (satir.length) satirlar.push({ ogeler:satir, genislik:genislik - ARA });

    /* çiz */
    satirlar.forEach((s, si) => {
      let x = EN / 2 - s.genislik / 2;
      const y = TEZGAH_UST + 16 + si * SATIR_BOY;
      s.ogeler.forEach(({ i, w }) => {
        this.sozcukYap(t, i, x + w / 2, y, w);
        x += w;
        this.yuvaYap(t, i, x + YUVA_EN / 2, y, YUVA_EN);
        x += YUVA_EN + ARA;
      });
    });
  }

  sozcukYap(t, i, x, y, w){
    const buyukGerek = t.onarim.buyuk.indexOf(i) >= 0;
    const c = this.add.container(x, y).setDepth(20);

    const g = this.add.graphics();
    const yazi = this.add.text(0, 0, t.sozcukler[i], {
      fontFamily:'system-ui, sans-serif', fontSize:'22px', fontStyle:'bold',
      color: RENK.metin
    }).setOrigin(0.5);

    c.add([g, yazi]);
    c.setSize(w, 40);
    c.setData('index', i);
    c.setData('buyukGerek', buyukGerek);
    c.setData('onarildi', false);
    c.setData('cizim', g);
    c.setData('yazi', yazi);
    c.setData('en', w);
    this.sozcukCiz(c, false);

    /* Dokunma alanını Phaser'a bırakıyoruz: Container'a elle
       Rectangle(-W/2,-H/2,…) verilince kaydırma bir kez daha uygulanıyor ve
       alan sola-yukarı kayıyor — nesneyi tutmak için sol üstüne basmak
       gerekiyordu. setSize + argümansız setInteractive() alanı ortalıyor.
       Alan görselden bir miktar geniş: parmak payı. */
    c.setSize(w + 20, 40 + 20);
    c.setInteractive();
    c.on('pointerdown', () => this.sozcugeDokun(c));

    /* Titreme kaldırıldı: yalnız onarılacak sözcük titriyordu ve cevabı
       ele veriyordu (bkz. sozcukCiz). */
    this.sozcukNesne.push(c);
    return c;
  }

  sozcukCiz(c, onarildi){
    const g = c.getData('cizim'), w = c.getData('en');
    g.clear();
    g.fillStyle(RENK.kart, 1);
    g.fillRoundedRect(-w / 2, -20, w, 40, 9);
    g.lineStyle(2, onarildi ? RENK.dogru : RENK.kartKnr, 1);
    g.strokeRoundedRect(-w / 2, -20, w, 40, 9);
    /* KUSUR: burada onarılacak sözcüğün altına kırmızı çizgi çiziliyordu
       ve o sözcük ayrıca titriyordu. 93 büyük-harf düzeltmesinin 31'i özel
       ad (Ahmet, Zeynep, Atatürk, Selanik'te, Nisan…); hangi sözcüğün özel
       ad olduğunu BULMAK görevin kendisiydi, işaret onu ele veriyordu.
       Artık bütün sözcükler aynı görünüyor; yönerge ne aranacağını
       söylüyor, kaç düzeltme kaldığı üst şeritte yazıyor. */
  }

  yuvaYap(t, i, x, y, w){
    const gerek = t.onarim.isaret[i];
    const c = this.add.container(x, y).setDepth(19);
    const g = this.add.graphics();
    g.fillStyle(RENK.yuva, 1);
    g.fillRoundedRect(-w / 2, -20, w, 40, 7);
    g.lineStyle(2, 0x554873, 1);
    g.strokeRoundedRect(-w / 2, -20, w, 40, 7);
    c.add(g);
    c.setSize(w, 40);
    c.setData('index', i);
    c.setData('gerek', gerek || null);
    c.setData('dolu', false);
    c.setData('cizim', g);
    c.setData('en', w);
    this.yuvaNesne.push(c);
    return c;
  }

  /* ---------- işaret sandığı ---------- */
  sandigiDoldur(){
    /* Kopya sayısı GERÇEK ihtiyaçtan hesaplanıyor. Körlemesine iki kopya
       üretmek katalogdaki 13 işaretli oyunlarda 26 kart demek oluyordu ve
       kartlar tek sırada üst üste biniyordu. Bir işaretten en fazla kaç
       tane gerekiyorsa o kadar (en az 1) üretiliyor. */
    const gerekSayisi = {};
    TURLAR.forEach(t => {
      const say = {};
      Object.keys(t.onarim.isaret || {}).forEach(k => {
        const m = t.onarim.isaret[k];
        say[m] = (say[m] || 0) + 1;
      });
      Object.keys(say).forEach(m => {
        gerekSayisi[m] = Math.max(gerekSayisi[m] || 0, say[m]);
      });
    });

    const liste = [];
    ISARETLER.forEach(m => {
      const n = Math.max(1, gerekSayisi[m] || 0);
      for (let i = 0; i < n; i++) liste.push(m);
    });
    Phaser.Utils.Array.Shuffle(liste);

    /* Kartları sandık içinde ızgaraya dağıt (satırda en çok 8 kart).
       Nesil kontrolü: tur hızlı değişirse önceki turun bekleyen dağıtım
       çağrıları yeni turda fazladan kart üretiyordu. */
    const nesil = this.nesil;
    const satirda = Math.min(8, Math.max(1, liste.length));
    liste.forEach((m, i) => {
      const sr = Math.floor(i / satirda);
      const sc = i % satirda;
      const buSatir = Math.min(satirda, liste.length - sr * satirda);
      const x = EN / 2 + (sc - (buSatir - 1) / 2) * Math.min(52, (EN - 110) / Math.max(1, buSatir - 1 || 1));
      this.time.delayedCall(i * 60, () => {
        if (this.nesil !== nesil) return;
        this.isaretYap(m, x);
      });
    });
  }

  isaretYap(m, x){
    const W = 44, H = 44;
    const c = this.add.container(Phaser.Math.Clamp(x, 52, EN - 52), SANDIK_UST - 40).setDepth(24);

    const g = this.add.graphics();
    g.fillStyle(RENK.isaret, 1);
    g.fillRoundedRect(-W / 2, -H / 2, W, H, 10);
    g.lineStyle(2, 0xd7b45e, 1);
    g.strokeRoundedRect(-W / 2, -H / 2, W, H, 10);
    const yazi = this.add.text(0, -2, m, {
      fontFamily:'system-ui, sans-serif', fontSize:'29px', fontStyle:'bold',
      color:'#4a3a12'
    }).setOrigin(0.5);

    c.add([g, yazi]);
    c.setSize(W, H);

    /* Arcade gövdesi — gruba ÖNCE ekle: Arcade Group add() sırasında
       kendi varsayılanlarını gövdeye basıyor. */
    this.isaretler.add(c);
    c.body.setSize(W, H);
    c.body.setBounce(0.3, 0.3);
    c.body.setDragX(140);

    c.setData('isaret', m);
    c.setData('takildi', false);

    /* Dokunma alanını Phaser'a bırakıyoruz: Container'a elle
       Rectangle(-W/2,-H/2,…) verilince kaydırma bir kez daha uygulanıyor ve
       alan sola-yukarı kayıyor — nesneyi tutmak için sol üstüne basmak
       gerekiyordu. setSize + argümansız setInteractive() alanı ortalıyor.
       Parmak payı küçük: 44px kartlar sandıkta 52px aralıkla duruyor,
       ±12px pay komşunun alanına giriyordu. */
    c.setSize(W + 8, H + 8);
    c.setInteractive();
    this.input.setDraggable(c);
    return c;
  }

  /* ---------- sözcüğe dokunma (büyük harf) ---------- */
  sozcugeDokun(c){
    if (this.kilit || c.getData('onarildi')) return;

    if (!c.getData('buyukGerek')){
      this.yanlisHamle('Bu sözcük büyük harfle başlamaz.', c.x, c.y);
      this.tweens.add({ targets:c, x:{ from:c.x - 5, to:c.x + 5 },
        duration:60, yoyo:true, repeat:2, onComplete:() => this.cumleyiHizala() });
      return;
    }

    const i = c.getData('index');
    const t = TURLAR[this.tur];
    const s = t.sozcukler[i];
    c.getData('yazi').setText(s.charAt(0).toLocaleUpperCase('tr') + s.slice(1));
    c.setData('onarildi', true);
    this.sozcukCiz(c, true);
    this.tweens.killTweensOf(c);
    c.setAngle(0);

    this.tweens.add({ targets:c, scale:1.16, duration:130, yoyo:true, ease:'Back.easeOut' });
    this.kivilcimlar.setParticleTint(RENK.dogru);
    this.kivilcimlar.explode(12, c.x, c.y);

    this.kalanBuyuk = this.kalanBuyuk.filter(v => v !== i);
    this.kalanTazele();
    this.puanEkle(50, c.x, c.y - 20);
    this.turuKontrolEt();
  }

  cumleyiHizala(){ /* sarsıntı tween'i sonrası konumu düzeltmek için yer tutucu */ }

  /* ---------- sürükleme (noktalama) ---------- */
  surukleKur(){
    this.input.on('dragstart', (p, k) => {
      if (this.kilit || k.getData('takildi')) return;
      this.suruklenen = k;
      k.setDepth(70);
      k.body.setAllowGravity(false);
      k.body.setVelocity(0, 0);
      this.tweens.add({ targets:k, scale:1.16, duration:120, ease:'Back.easeOut' });
      this.yuvalariVurgula(true);
    });

    this.input.on('drag', (p, k, x, y) => {
      if (this.kilit || k.getData('takildi')) return;
      k.x = Phaser.Math.Clamp(x, 30, EN - 30);
      k.y = Phaser.Math.Clamp(y, TEZGAH_UST - 40, BOY - 40);
    });

    this.input.on('dragend', (p, k) => {
      if (this.kilit || k.getData('takildi')) return;
      this.suruklenen = null;
      this.yuvalariVurgula(false);
      this.tweens.add({ targets:k, scale:1, duration:120 });

      const yuva = this.enYakinYuva(k);
      if (yuva) this.yuvayaTak(k, yuva);
      else {
        k.body.setAllowGravity(true);
        k.body.setVelocity(Phaser.Math.Between(-40, 40), 40);
      }
    });
  }

  enYakinYuva(k){
    let iyi = null, enAz = 44;
    this.yuvaNesne.forEach(y => {
      if (y.getData('dolu')) return;
      const d = Phaser.Math.Distance.Between(k.x, k.y, y.x, y.y);
      if (d < enAz){ enAz = d; iyi = y; }
    });
    return iyi;
  }

  yuvalariVurgula(acik){
    this.yuvaNesne.forEach(y => {
      if (y.getData('dolu')) return;
      const g = y.getData('cizim'), w = y.getData('en');
      g.clear();
      g.fillStyle(acik ? 0x3b3160 : RENK.yuva, 1);
      g.fillRoundedRect(-w / 2, -20, w, 40, 7);
      g.lineStyle(2, acik ? RENK.vurgu : 0x554873, 1);
      g.strokeRoundedRect(-w / 2, -20, w, 40, 7);
    });
  }

  yuvayaTak(k, yuva){
    const gerek = yuva.getData('gerek');

    if (gerek && gerek === k.getData('isaret')){
      /* doğru işaret — yuvaya otursun */
      k.setData('takildi', true);
      k.disableInteractive();
      k.body.enable = false;
      k.setDepth(22);
      this.tweens.add({
        targets:k, x:yuva.x, y:yuva.y, scale:0.82,
        duration:200, ease:'Back.easeOut'
      });
      yuva.setData('dolu', true);
      const g = yuva.getData('cizim'), w = yuva.getData('en');
      g.clear();
      g.fillStyle(0x1e5d43, 1);
      g.fillRoundedRect(-w / 2, -20, w, 40, 7);
      g.lineStyle(2, RENK.dogru, 1);
      g.strokeRoundedRect(-w / 2, -20, w, 40, 7);

      this.kivilcimlar.setParticleTint(RENK.dogru);
      this.kivilcimlar.explode(14, yuva.x, yuva.y);
      this.kalanIsaret = this.kalanIsaret.filter(v => v !== yuva.getData('index'));
      this.kalanTazele();
      this.puanEkle(50, yuva.x, yuva.y - 20);
      this.turuKontrolEt();
      return;
    }

    /* GERÇEK FİZİK: yanlış işaret yuvadan fırlayıp sandığa düşer */
    k.body.setAllowGravity(true);
    k.body.setVelocityY(-320);
    k.body.setVelocityX(Phaser.Math.Between(-160, 160));
    this.tweens.add({ targets:k, angle:Phaser.Math.Between(-220, 220), duration:600 });
    this.yanlisHamle(
      gerek ? 'Buraya başka bir işaret gerekiyor.' : 'Bu yuvaya işaret konmaz.',
      yuva.x, yuva.y
    );
  }

  /* ---------- ortak sonuç yardımcıları ---------- */
  puanEkle(kazanc, x, y){
    this.seri++;
    const p = kazanc + (this.seri - 1) * 10;
    this.puan += p;
    this.puanYazi.setText('Puan ' + this.puan);
    this.tweens.add({
      targets:this.puanYazi, scale:1.4, duration:120, yoyo:true, ease:'Back.easeOut'
    });
    const ucan = this.add.text(x, y, '+' + p, {
      fontFamily:'system-ui, sans-serif', fontSize:'24px', fontStyle:'bold',
      color:'#7ce0a3'
    }).setOrigin(0.5).setDepth(95);
    this.tweens.add({
      targets:ucan, y:ucan.y - 50, alpha:0,
      duration:620, ease:'Cubic.easeOut', onComplete:() => ucan.destroy()
    });
  }

  yanlisHamle(mesaj, x, y){
    this.seri = 0;
    this.can--;
    this.arayuzuTazele();
    this.tozlar.explode(12, x, y);
    this.cameras.main.shake(210, 0.011);
    this.cameras.main.flash(160, 220, 90, 90);
    this.tweens.add({
      targets:this.canYazi, angle:{ from:-12, to:12 },
      duration:70, yoyo:true, repeat:3,
      onComplete:() => this.canYazi.setAngle(0)
    });
    this.mesajGoster(mesaj, '#b5453b');

    if (this.can <= 0){
      this.kilit = true;
      this.time.delayedCall(900, () => this.bitir(false));
    }
  }

  turuKontrolEt(){
    if (this.kalanBuyuk.length || this.kalanIsaret.length) return;

    const t = TURLAR[this.tur];
    this.kilit = true;
    const bonus = 100;
    this.puan += bonus;
    this.puanYazi.setText('Puan ' + this.puan);

    /* onarılan cümle tezgâhtan kalksın */
    this.sozcukNesne.concat(this.yuvaNesne).forEach((o, i) => {
      this.tweens.add({
        targets:o, y:o.y - 26, alpha:0.9, duration:260, delay:i * 22, yoyo:true
      });
    });

    this.kivilcimlar.setParticleTint(RENK.vurgu);
    this.kivilcimlar.explode(26, EN / 2, TEZGAH_UST + 40);
    this.cameras.main.flash(150, 80, 210, 140);
    this.mesajGoster(t.tamam + '  ·  ' + t.aciklama, '#1f6d4a');

    this.tur++;
    this.arayuzuTazele();

    this.time.delayedCall(2300, () => {
      if (this.tur >= TURLAR.length){ this.bitir(true); return; }
      this.turuBaslat();
    });
  }

  mesajGoster(metin, arka){
    if (this.mesaj) this.mesaj.destroy();
    this.mesaj = this.add.text(EN / 2, 424, metin, {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#ffffff', backgroundColor:arka,
      padding:{ x:13, y:8 }, align:'center', wordWrap:{ width:EN - 70 }, lineSpacing:3
    }).setOrigin(0.5).setDepth(96).setAlpha(0);
    const t = this.mesaj;
    this.tweens.add({ targets:t, alpha:1, duration:150 });
    this.time.delayedCall(2000, () => {
      if (!t.active) return;
      this.tweens.add({
        targets:t, alpha:0, duration:250,
        onComplete:() => { if (this.mesaj === t) this.mesaj = null; t.destroy(); }
      });
    });
  }

  /* ---------- arayüz ---------- */
  arayuzKur(){
    /* Katalogda yönerge 120 karaktere çıkıyor; sabit yükseklikli şerit
       yazıyı iki yandan kesiyordu. Şerit metnin gerçek boyuna göre. */
    const yon = this.add.text(EN / 2, 22, OYUN_EMO + '  ' + TALIMAT, {
      fontFamily:'system-ui, sans-serif',
      fontSize: (TALIMAT.length > 92 ? '16px' : (TALIMAT.length > 54 ? '17px' : '20px')),
      fontStyle:'bold', color:'#ffffff', align:'center',
      wordWrap:{ width:EN - 52 }, lineSpacing:3
    }).setOrigin(0.5, 0).setDepth(61);

    const seritBoy = Math.max(104, yon.height + 62);
    const serit = this.add.graphics().setDepth(60);
    serit.fillStyle(0x140f1f, 0.97);
    serit.fillRoundedRect(10, 10, EN - 20, seritBoy, 18);
    yon.setDepth(61);
    const satirY = 10 + seritBoy - 22;
    this.seritAlt = 10 + seritBoy;

    this.puanYazi = this.add.text(30, satirY, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0, 0.5).setDepth(61);

    this.canYazi = this.add.text(EN - 30, satirY, '', { fontSize:'20px' })
      .setOrigin(1, 0.5).setDepth(61);

    this.ilerlemeYazi = this.add.text(EN / 2, satirY, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#b3a6dd'
    }).setOrigin(0.5).setDepth(61);

    this.gorevYazi = this.add.text(EN / 2, this.seritAlt + 34, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', fontStyle:'bold',
      color:'#ffffff', align:'center', wordWrap:{ width:EN - 50 }, lineSpacing:4
    }).setOrigin(0.5).setDepth(61);

    /* Kalan düzeltme sayacı: tezgâhın hemen üstünde. */
    this.kalanYazi = this.add.text(EN / 2, TEZGAH_UST - 44, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'17px', fontStyle:'bold',
      color:'#ffd166', align:'center'
    }).setOrigin(0.5).setDepth(61);

    this.arayuzuTazele();
  }

  /* Kaç düzeltme kaldığı — hangi sözcük olduğunu söylemeden yön verir. */
  kalanTazele(){
    if (!this.kalanYazi) return;
    const b = (this.kalanBuyuk || []).length;
    const i = (this.kalanIsaret || []).length;
    const parca = [];
    if (b) parca.push('🔠 ' + b + ' büyük harf');
    if (i) parca.push('✒️ ' + i + ' işaret');
    this.kalanYazi.setText(parca.length ? 'Kalan:  ' + parca.join('   ·   ') : '✅ Cümle tamam');
  }

  arayuzuTazele(){
    this.canYazi.setText(
      '❤️'.repeat(Math.max(0, this.can)) +
      '🖤'.repeat(Math.max(0, CAN_SAYISI - this.can))
    );
    this.ilerlemeYazi.setText(`${this.tur} / ${TURLAR.length} cümle`);
  }

  bitir(kazandi){
    /* Uygulama içindeyken kazanma ekranını uygulama gösteriyor. */
    if (kazandi && KOPRU){ KOPRU.bitir(BASARI, this.puan); return; }
    this.scene.start('GameOver', {
      kazandi, puan:this.puan, can:this.can,
      tur:this.tur, toplam:TURLAR.length
    });
  }

  /* ---------- her kare ---------- */
  update(){
    if (!this.isaretler) return;
    /* sandıktan kaçan işareti geri getir */
    this.isaretler.getChildren().forEach(k => {
      if (!k.active || k.getData('takildi') || this.suruklenen === k) return;
      if (k.y > BOY + 60 || k.x < -60 || k.x > EN + 60){
        k.body.reset(Phaser.Math.Between(70, EN - 70), SANDIK_UST - 30);
        k.body.setVelocity(0, 0);
        k.setAngle(0);
      }
    });
  }
}

/* =====================================================================
   4) GAME OVER
   ===================================================================== */
class GameOverScene extends Phaser.Scene {
  constructor(){ super('GameOver'); }

  init(veri){ this.veri = veri; }

  create(){
    const { kazandi, puan, can, tur, toplam } = this.veri;
    atolyeCiz(this);

    const emo = this.add.text(EN / 2, 190, kazandi ? '✍️' : '💪', { fontSize:'97px' })
      .setOrigin(0.5).setScale(0);
    this.tweens.add({ targets:emo, scale:1, duration:520, ease:'Back.easeOut' });

    this.add.text(EN / 2, 300, kazandi ? 'BAŞ TAMİRCİ!' : 'TEKRAR DENE', {
      fontFamily:'system-ui, sans-serif', fontSize:'35px', fontStyle:'bold',
      color: kazandi ? '#7ce0a3' : '#ffd166', align:'center'
    }).setOrigin(0.5);

    this.add.text(EN / 2, 360,
      kazandi ? BASARI : `${tur} / ${toplam} cümle onardın — bir daha deneyelim mi?`, {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#ded4ff',
      align:'center', wordWrap:{ width:EN - 70 }, lineSpacing:5
    }).setOrigin(0.5);

    const puanYazi = this.add.text(EN / 2, 456, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'42px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0.5);
    const sayac = { v:0 };
    this.tweens.add({
      targets:sayac, v:puan, duration:900, ease:'Cubic.easeOut',
      onUpdate:() => puanYazi.setText('Puan ' + Math.round(sayac.v))
    });

    this.add.text(EN / 2, 506,
      'Kalan can: ' + (can > 0 ? '❤️'.repeat(can) : '—'), {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#b3a6dd'
    }).setOrigin(0.5);

    if (kazandi){
      const konfeti = this.add.particles(EN / 2, -20, 'kivilcim', {
        speed:{ min:90, max:260 }, angle:{ min:60, max:120 },
        scale:{ start:0.8, end:0 }, alpha:{ start:1, end:0 },
        lifespan:2000, gravityY:180, quantity:2, frequency:70,
        tint:[0xffd166, 0x7ce0a3, 0xbfaeff, 0xf07575]
      }).setDepth(5);
      this.time.delayedCall(2600, () => konfeti.stop());
    }

    dugmeYap(this, EN / 2, 606, '↻  TEKRAR OYNA', RENK.dogru, () => this.scene.start('Game'));

    /* Uygulama içinde: bu oyunda takılan çocuk sıradakine geçebilsin. */

    if (KOPRU) dugmeYap(this, EN / 2, 680, '⏭  SIRADAKİ OYUN', 0x4a679e, () => KOPRU.atla());
    if (!KOPRU) dugmeYap(this, EN / 2, 684, '☰  MENÜ',        0x554873, () => this.scene.start('Menu'));
  }
}

/* =====================================================================
   OYUNU BAŞLAT
   ===================================================================== */
/* =====================================================================
   NETLİK — cihazın piksel yoğunluğunda çizim
   ---------------------------------------------------------------------
   Oyun 480x800 mantıksal tuvalde çiziliyordu; telefon bunu 1080 piksele
   büyütünce yazılar ve kenarlar bulanıklaşıyordu. Çözüm: tuvali cihazın
   gerçek piksel sayısında açmak, dünyayı ise kamerayı NETLIK katına
   yakınlaştırarak yine 480x800 koordinatta tutmak. Böylece Graphics ile
   çizilen her şey (kartlar, şeritler, kutular) vektör keskinliğinde,
   yazılar da NETLIK çözünürlüğünde üretiliyor; oyun kodunun tek satırı
   değişmiyor.
   ===================================================================== */
const NETLIK = Math.min(3, Math.max(1, Math.round((window.devicePixelRatio || 1) * 2) / 2));

/* Phaser yazıyı kendi ara tuvaline çiziyor; çözünürlük verilmezse 1x
   üretilip yakınlaştırmada bulanıklaşır. Bütün yazılara varsayılan
   olarak NETLIK veriyoruz. */
(function(){
  const TS = Phaser.GameObjects.TextStyle.prototype;
  const eskiSetStyle = TS.setStyle;
  TS.setStyle = function(style, updateText, setDefaults){
    if (style && style.resolution === undefined) style.resolution = NETLIK;
    return eskiSetStyle.call(this, style, updateText, setDefaults);
  };
})();

/* Tuval NETLIK katına büyüdüğü için Phaser imleç konumunu da o ölçekte
   veriyor (0–960). Oyun koordinatına (0–480) çeviren yardımcı: sürükleme
   olayları zaten dünya koordinatı verdiği için yalnız pointer olaylarında
   kullanılıyor. */
function imlec(p){ return { x: p.x / NETLIK, y: p.y / NETLIK }; }

/* Her sahne başlarken kamerayı NETLIK katına yakınlaştırıp fizik
   dünyasını mantıksal ölçüde tutuyoruz: tuval büyüdü, dünya büyümedi.
   Sahne örnekleri oyun kurulumundan sonra eşzamansız oluştuğu için
   kanca Systems.start üzerine takılıyor — yeniden başlatmalarda da
   kendiliğinden çalışıyor. */
(function(){
  const SS = Phaser.Scenes.Systems.prototype;
  const eskiStart = SS.start;
  SS.start = function(veri){
    const sonuc = eskiStart.call(this, veri);
    const sc = this.scene;
    try{
      if (sc.cameras && sc.cameras.main){
        sc.cameras.main.setZoom(NETLIK);
        sc.cameras.main.centerOn(EN / 2, BOY / 2);
      }
      if (sc.physics && sc.physics.world) sc.physics.world.setBounds(0, 0, EN, BOY);
    }catch(e){ /* netlik ayarı oyunu engellemesin */ }
    return sonuc;
  };
})();

window.OYUN = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'oyun',
  width: EN * NETLIK,
  height: BOY * NETLIK,
  backgroundColor: '#191521',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 780 } }
  },
  scene: [BootScene, MenuScene, GameScene, GameOverScene]
});

</script>
</body>
</html>
```

### kargo-phaser.html — codeGrid (15 oyun)
Dosya boyu: 33512 bayt · 908 satır

```html
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<title>Robot Kargo Teslimatı — Phaser 3</title>
<script src="https://cdn.jsdelivr.net/npm/phaser@3.80.1/dist/phaser.min.js"></script>
<style>
  html, body { margin:0; padding:0; height:100%; background:#0f1a26; overflow:hidden;
    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
    -webkit-tap-highlight-color: transparent; touch-action:none; }
  #oyun { width:100%; height:100%; display:flex; align-items:center; justify-content:center; }
  canvas { display:block; }
</style>
</head>
<body>
<div id="oyun"></div>
<script>
/* =====================================================================
   ROBOT KARGO TESLİMATI — Phaser 3   (mekanik: codeGrid · 15 oyun)
   ---------------------------------------------------------------------
   Kazanım: MAT.2.3.6 — Beklenmedik durumda planı yeniden yapılandırır,
   mantıksal denetleme yapar.

   Sahneler : Boot → Menu → Game → GameOver
   Fizik    : Arcade.
              · Dron programı çalışınca GERÇEK HIZLA hücreden hücreye
                uçar (physics.moveTo), hedefe varınca durur.
              · Kapalı kareye girmeye çalışırsa çarpar, geri seker,
                pervane dumanı çıkar, kamera sarsılır.
              · Hedefe varınca kargo yerçekimiyle eve düşer.
   Görsel   : Bütün dokular Graphics ile çalışma anında üretilir —
              uygulama çevrimdışı kabukta (APK / iOS) çalışacağı için
              dışarıdan resim çekilmiyor.
   ===================================================================== */

const EN = 480, BOY = 800;

const RENK = {
  gokUst  : 0x16283a,
  gokAlt  : 0x2b4a63,
  dogru   : 0x34c47b,
  yanlis  : 0xf07575,
  hucre   : 0x1e3a52,
  vurgu   : 0xffd166
};

/* ---------------------------------------------------------------------
   İÇERİK — uygulamadaki v30 oyununun birebir aynısı.
   Başka bir codeGrid oyununa geçmek için yalnızca bu blok değişir.
   Koordinatlar [sütun, satır]; sol üst köşe [0,0].
   ------------------------------------------------------------------- */
/* ---------------- uygulama köprüsü ----------------
   Adres  kargo.html#oyun=v29  biçiminde; katalog verisi üst pencereden
   okunuyor. Kazanınca completeGame() çağrılır.                          */
const KOPRU = (function(){
  try{
    const p = new URLSearchParams(location.hash.slice(1));
    const id = p.get('oyun');
    if (id && window.parent && window.parent !== window &&
        typeof window.parent.getGame === 'function'){
      const g = window.parent.getGame(id);
      if (g && g.cfg) return {
        oyun: g, cfg: g.cfg,
        bitir(mesaj, puan){ try{ window.parent.completeGame(mesaj || '', puan); }catch(e){} },
        /* Turun kendi metnini uygulamanın sesiyle okutur (Piper). */
        oku(metin){ try{ if (window.parent.oku) window.parent.oku(metin); }catch(e){} },
        /* Kaybetme ekranından: bu oyunu bırak, sıradakine geç. */
        atla(){ try{ if (window.parent.sonrakiOyunaGec) window.parent.sonrakiOyunaGec(); }catch(e){} }
      };
    }
  }catch(e){ /* çapraz kaynak engeli: tek başına oynanır */ }
  return null;
})();

/* HTML varlıklarını çöz: katalogda "Pay &lt; payda" gibi yazımlar var,
   çözülmezse ekranda "&lt;" olarak görünüyor ve öyle okunuyor. */
function varlikCoz(m){
  return String(m)
    .replace(/&nbsp;/gi, ' ')
    .replace(/&lt;/gi, '<').replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"').replace(/&#39;|&apos;/gi, "'")
    .replace(/&hellip;/gi, '…').replace(/&mdash;/gi, '—').replace(/&ndash;/gi, '–')
    .replace(/&times;/gi, '×').replace(/&divide;/gi, '÷').replace(/&deg;/gi, '°')
    .replace(/&rarr;/gi, '→').replace(/&larr;/gi, '←')
    .replace(/&amp;/gi, '&');            /* en sona: çift çözmeyi önler */
}

function duzMetin(x){
  return varlikCoz(String(x == null ? '' : x).replace(/<br\s*\/?>/gi,' ')
    .replace(/<[^>]+>/g,'')).replace(/[“”]/g,'"').replace(/\s+/g,' ').trim();
}
function tekSatir(x){ return duzMetin(x).replace(/\n/g,' '); }

const VARSAYILAN = {
  instruction:'Yön bloklarını diz, sonra çalıştır',
  heroEmoji:'🚁', goalEmoji:'🏠',
  rounds:[
    { cols:4, rows:3, start:[0,0], goal:[3,2], walls:[[1,1],[2,1]], wallEmoji:'🚧',
      hint:'Orta sıranın ortası kapalı — alt sıradan dolaşabilirsin.',
      wallMsg:'Yol çalışmasına girdin! Başka yol dene.',
      missMsg:'Eve ulaşamadın, adımlarını kontrol et.' } ]
};

const CFG = KOPRU ? KOPRU.cfg : VARSAYILAN;

const KAHRAMAN = CFG.heroEmoji || '🚁';
const HEDEF    = CFG.goalEmoji || '🏠';
/* Duvar emojisi tur başına değişebiliyor (timsah, dağ, kaya); tur
   verisinde yoksa genel değer kullanılıyor. */
const DUVAR    = '🚧';

const TURLAR = (CFG.rounds || []).map(r => ({
  sutun:      Number(r.cols) || 4,
  satir:      Number(r.rows) || 3,
  baslangic:  r.start || [0, 0],
  hedef:      r.goal  || [1, 1],
  duvarlar:   r.walls || [],
  duvarEmoji: r.wallEmoji || DUVAR,
  azamiAdim:  (r.maxSteps == null ? null : Number(r.maxSteps)),
  /* KUSUR: gorev ve ipucu aynı alandan (r.hint) besleniyordu; aynı cümle
     ekranda iki kez yazılıyor ve ızgaraya ayrılacak yeri yiyordu. */
  gorev:      tekSatir(r.hint) || 'Rotayı kur ve çalıştır.',
  duvarMsj:   tekSatir(r.wallMsg) || 'Engele çarptın! Başka yol dene.',
  kacirMsj:   tekSatir(r.missMsg) || 'Hedefe ulaşamadın, adımlarını kontrol et.'
}));

const OYUN_ADI = KOPRU ? tekSatir(KOPRU.oyun.title) : 'ROBOT KARGO TESLİMATI';
const OYUN_EMO = KOPRU ? (KOPRU.oyun.emo || '🚁') : '🚁';
const TALIMAT  = tekSatir(CFG.instruction) || 'Yön bloklarını diz, sonra çalıştır';
const IPUCU    = tekSatir(CFG.tip);
const BASARI   = tekSatir(CFG.successMsg) || 'Rotayı doğru kurdun!';

const CAN_SAYISI = 3;

/* --- Yerleşim -------------------------------------------------------- */
/* KUSUR: hücre 88px SABİTTİ. Katalogdaki 32 turun 30'u 6x5, 6x6 ya da 7x6;
   7x6 ızgara 616x528px ediyor ve 480x800 ekranda hem yanlardan hem de
   program şeridinin üstünden taşıyordu — hücreler, dron ve hedef ekran
   dışında kalıyordu. Ölçü artık tur başına hesaplanıyor. */
const HUCRE_AZAMI = 88;
const HUCRE_ASGARI = 34;
const IZGARA_BANT_UST = 206;  /* ızgaraya ayrılan dikey bandın üstü */
const IZGARA_BANT_ALT = 520;  /* program şeridinin üstünde bırakılan pay */
const SERIT_Y   = 556;   /* program şeridi */
const TUS_Y     = 646;   /* yön tuşları */
const DRON_HIZI = 300;   /* hücreler arası uçuş hızı (px/sn) */

const YONLER = [
  { ad:'yukari', ok:'▲', dx: 0, dy:-1 },
  { ad:'sol',    ok:'◀', dx:-1, dy: 0 },
  { ad:'sag',    ok:'▶', dx: 1, dy: 0 },
  { ad:'asagi',  ok:'▼', dx: 0, dy: 1 }
];

/* =====================================================================
   1) BOOT — dokuları üret
   ===================================================================== */
class BootScene extends Phaser.Scene {
  constructor(){ super('Boot'); }

  create(){
    this.dokuKivilcim();
    this.dokuDuman();
    /* Uygulama içinde çocuk oyunu listeden zaten seçti; menüyü atla. */
    this.scene.start(KOPRU ? 'Game' : 'Menu');
  }

  dokuKivilcim(){
    const g = this.make.graphics({ add:false });
    g.fillStyle(0xffffff, 1);
    g.fillCircle(8, 8, 8);
    g.generateTexture('kivilcim', 16, 16);
    g.destroy();
  }

  dokuDuman(){
    const g = this.make.graphics({ add:false });
    for (let r = 14; r > 0; r--){
      g.fillStyle(0xffffff, 0.06);
      g.fillCircle(14, 14, r);
    }
    g.generateTexture('duman', 28, 28);
    g.destroy();
  }
}

/* =====================================================================
   Ortak yardımcılar
   ===================================================================== */
function gokyuzuCiz(sc){
  const g = sc.add.graphics();
  g.fillGradientStyle(RENK.gokUst, RENK.gokUst, RENK.gokAlt, RENK.gokAlt, 1);
  g.fillRect(0, 0, EN, BOY);

  for (let i = 0; i < 5; i++){
    const b = sc.add.graphics();
    b.fillStyle(0xffffff, 0.06);
    b.fillEllipse(Phaser.Math.Between(0, EN), Phaser.Math.Between(50, 190),
                  Phaser.Math.Between(90, 160), Phaser.Math.Between(24, 40));
    sc.tweens.add({
      targets:b, x:'+=' + Phaser.Math.Between(50, 130),
      duration:Phaser.Math.Between(9000, 15000),
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });
  }
  return g;
}

function dugmeYap(sc, x, y, metin, renk, geriCagri, genislik, yukseklik){
  const W = genislik || 280, H = yukseklik || 60;
  const c = sc.add.container(x, y);
  const g = sc.add.graphics();
  g.fillStyle(renk, 1);
  g.fillRoundedRect(-W / 2, -H / 2, W, H, H / 2);
  g.fillStyle(0xffffff, 0.16);
  g.fillRoundedRect(-W / 2, -H / 2, W, H * 0.4, { tl:H / 2, tr:H / 2, bl:0, br:0 });
  const t = sc.add.text(0, 0, metin, {
    fontFamily:'system-ui, sans-serif', fontSize: H > 50 ? '20px' : '17px',
    fontStyle:'bold', color:'#ffffff'
  }).setOrigin(0.5);
  c.add([g, t]);
  c.setSize(W, H).setInteractive({ useHandCursor:true });
  c.on('pointerover', () => sc.tweens.add({ targets:c, scale:1.05, duration:110 }));
  c.on('pointerout',  () => sc.tweens.add({ targets:c, scale:1.00, duration:110 }));
  /* KUSUR: geri çağrı basma TWEEN'inin sonunda çalışıyordu (≈180ms).
     Tuş takımında aynı tuşa üst üste basıldığında bir basış yutuluyordu
     (sınamada "500000" yerine "50000" yazıldı) ve her dokunuş 180ms
     gecikmeyle işliyordu. Artık işlem HEMEN yapılıyor, tween yalnız
     görsel geri bildirim. */
  c.on('pointerdown', () => {
    sc.tweens.add({ targets:c, scale:0.92, duration:90, yoyo:true });
    if (geriCagri) geriCagri();
  });
  return c;
}

/* =====================================================================
   2) MENU
   ===================================================================== */
class MenuScene extends Phaser.Scene {
  constructor(){ super('Menu'); }

  create(){
    gokyuzuCiz(this);

    const d = this.add.text(EN / 2 - 70, 200, KAHRAMAN, { fontSize:'67px' }).setOrigin(0.5);
    this.add.text(EN / 2 + 80, 214, HEDEF, { fontSize:'59px' }).setOrigin(0.5);
    this.tweens.add({
      targets:d, y:186, x:EN / 2 - 40, duration:1500,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });

    const baslik = this.add.text(EN / 2, 336, OYUN_ADI, {
      fontFamily:'system-ui, sans-serif', fontSize:'40px', fontStyle:'bold',
      color:'#ffffff', align:'center', lineSpacing:5
    }).setOrigin(0.5);
    this.tweens.add({
      targets:baslik, scale:1.04, duration:1400,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });

    this.add.text(EN / 2, 424, TALIMAT, {
      fontFamily:'system-ui, sans-serif', fontSize:'22px',
      color:'#cfe0ff', align:'center'
    }).setOrigin(0.5);

    const kart = this.add.graphics();
    kart.fillStyle(0x0d1826, 0.92);
    kart.fillRoundedRect(30, 462, EN - 60, 84, 16);
    kart.lineStyle(2, 0x3d6285, 1);
    kart.strokeRoundedRect(30, 462, EN - 60, 84, 16);
    this.add.text(EN / 2, 504, IPUCU, {
      fontFamily:'system-ui, sans-serif', fontSize:'17px', fontStyle:'bold',
      color:'#ffd166', align:'center', wordWrap:{ width:EN - 90 }, lineSpacing:4
    }).setOrigin(0.5);

    dugmeYap(this, EN / 2, 614, '▶  BAŞLA', RENK.dogru, () => this.scene.start('Game'));

    this.add.text(EN / 2, 712, `${TURLAR.length} görev  ·  ${CAN_SAYISI} can`, {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', color:'#9fc2e6'
    }).setOrigin(0.5);
  }
}

/* =====================================================================
   3) GAME
   ===================================================================== */
class GameScene extends Phaser.Scene {
  constructor(){ super('Game'); }

  create(){
    this.can     = CAN_SAYISI;
    this.puan    = 0;
    this.seri    = 0;
    this.tur     = 0;
    this.kilit   = true;
    this.calisiyor = false;

    /* Phaser sahne örneğini yeniden kullanır — TEKRAR OYNA'da eski
       nesnelere işaret etmesinler. */
    this.izgaraNesne = null;
    this.blokNesne   = null;
    this.program     = null;
    this.mesaj       = null;
    this.dron        = null;   /* yeniden başlatmada eski nesneye
                                  işaret edip body'siz kalıyordu */
    this.pervane     = null;
    this.ucuyor      = false;

    gokyuzuCiz(this);

    this.kivilcimlar = this.add.particles(0, 0, 'kivilcim', {
      speed:{ min:140, max:380 }, angle:{ min:0, max:360 },
      scale:{ start:0.9, end:0 }, alpha:{ start:1, end:0 },
      lifespan:650, gravityY:340, blendMode:'ADD', emitting:false
    }).setDepth(90);

    this.dumanlar = this.add.particles(0, 0, 'duman', {
      speed:{ min:40, max:150 }, angle:{ min:0, max:360 },
      scale:{ start:0.9, end:2.1 }, alpha:{ start:0.5, end:0 },
      lifespan:700, emitting:false
    }).setDepth(80);

    this.arayuzKur();
    this.tuslariKur();
    this.turuBaslat();
  }

  /* ---------- ızgara ---------- */
  /* Turun ızgarasını ekrana sığdıran hücre ölçüsü ve sol-üst köşe. */
  izgaraOlcuHesapla(){
    const t = TURLAR[this.tur];
    const gorevAlt = this.gorevYazi
      ? this.gorevYazi.y + this.gorevYazi.height + 12 : IZGARA_BANT_UST;
    const ust = Math.max(IZGARA_BANT_UST, gorevAlt);
    const enPay  = (EN - 36) / t.sutun;
    const boyPay = (IZGARA_BANT_ALT - ust) / t.satir;
    const h = Math.max(HUCRE_ASGARI, Math.min(HUCRE_AZAMI, Math.floor(Math.min(enPay, boyPay))));
    this.hucre = h;
    this.izgaraSol = EN / 2 - (t.sutun * h) / 2;
    /* ızgara banda dikey olarak ortalanıyor */
    this.izgaraUst = ust + Math.max(0, (IZGARA_BANT_ALT - ust - t.satir * h) / 2);
  }

  hucreMerkezi(sx, sy){
    const h = this.hucre || HUCRE_AZAMI;
    return {
      x: this.izgaraSol + sx * h + h / 2,
      y: this.izgaraUst + sy * h + h / 2
    };
  }

  duvarMi(sx, sy){
    const t = TURLAR[this.tur];
    if (sx < 0 || sy < 0 || sx >= t.sutun || sy >= t.satir) return 'disari';
    return t.duvarlar.some(d => d[0] === sx && d[1] === sy) ? 'duvar' : null;
  }

  izgarayiCiz(){
    const t = TURLAR[this.tur];
    this.izgaraOlcuHesapla();
    const H = this.hucre;
    const pay = Math.max(3, Math.round(H * 0.09));
    const yuvar = Math.max(4, Math.round(H * 0.11));
    const g = this.add.graphics().setDepth(5);
    const solX = this.izgaraSol;

    /* zemin */
    g.fillStyle(0x14283a, 0.94);
    g.fillRoundedRect(solX - 8, this.izgaraUst - 8, t.sutun * H + 16, t.satir * H + 16, 14);
    g.lineStyle(2, 0x3d6285, 1);
    g.strokeRoundedRect(solX - 8, this.izgaraUst - 8, t.sutun * H + 16, t.satir * H + 16, 14);

    this.izgaraNesne = [g];

    for (let sy = 0; sy < t.satir; sy++){
      for (let sx = 0; sx < t.sutun; sx++){
        const m = this.hucreMerkezi(sx, sy);
        const duvar = this.duvarMi(sx, sy) === 'duvar';
        g.fillStyle(duvar ? 0x4a2a2a : 0x1e3a52, 1);
        g.fillRoundedRect(m.x - H / 2 + pay, m.y - H / 2 + pay, H - pay * 2, H - pay * 2, yuvar);
        g.lineStyle(2, duvar ? 0x8a4a4a : 0x2f5877, 1);
        g.strokeRoundedRect(m.x - H / 2 + pay, m.y - H / 2 + pay, H - pay * 2, H - pay * 2, yuvar);

        if (duvar){
          /* Duvar emojisi tur verisinden: timsah, kaya, dağ… genel 🚧 yerine
             turun kendi engeli çizilsin (r.wallEmoji okunuyordu ama
             kullanılmıyordu). */
          const e = this.add.text(m.x, m.y, t.duvarEmoji,
            { fontSize: Math.round(H * 0.46) + 'px' }).setOrigin(0.5).setDepth(8);
          this.izgaraNesne.push(e);
        }
      }
    }

    /* hedef */
    const h = this.hucreMerkezi(t.hedef[0], t.hedef[1]);
    const he = this.add.text(h.x, h.y, HEDEF,
      { fontSize: Math.round(H * 0.52) + 'px' }).setOrigin(0.5).setDepth(8);
    this.tweens.add({
      targets:he, scale:1.1, duration:900, yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });
    this.izgaraNesne.push(he);
  }

  /* ---------- tur kurulumu ---------- */
  turuBaslat(){
    const t = TURLAR[this.tur];
    this.kilit = true;
    this.calisiyor = false;
    this.program = [];

    if (this.izgaraNesne) this.izgaraNesne.forEach(o => o.destroy());
    if (this.blokNesne)   this.blokNesne.forEach(o => o.destroy());
    this.blokNesne = [];

    /* Görev yazısı ızgaradan ÖNCE yazılıyor: ızgaranın dikey bandı yazının
       gerçek yüksekliğine göre hesaplanıyor. */
    this.gorevYazi.setText(t.gorev);
    this.izgarayiCiz();

    /* dron başlangıç hücresine */
    const b = this.hucreMerkezi(t.baslangic[0], t.baslangic[1]);
    if (!this.dron){
      this.dron = this.physics.add.existing(
        this.add.text(b.x, b.y, KAHRAMAN, { fontSize:'46px' }).setOrigin(0.5).setDepth(30)
      );
      this.dronPunto = 46;
      this.dron.body.setAllowGravity(false);
      this.pervane = this.add.particles(0, 0, 'duman', {
        speed:{ min:8, max:26 }, angle:{ min:70, max:110 },
        scale:{ start:0.24, end:0.8 }, alpha:{ start:0.28, end:0 },
        lifespan:520, frequency:200
      }).setDepth(29);
      this.pervane.startFollow(this.dron, 0, 16);
    }
    this.dron.setPosition(b.x, b.y);
    this.dron.body.reset(b.x, b.y);
    this.dron.setAlpha(1).setScale(1);
    /* dron da hücre ölçüsüne uysun (küçük ızgarada kareyi taşıyordu) */
    this.dron.setFontSize(Math.round(this.hucre * 0.52) + 'px');
    this.hucreX = t.baslangic[0];
    this.hucreY = t.baslangic[1];

    this.tweens.add({
      targets:this.gorevYazi, scale:{ from:0.86, to:1 }, duration:280, ease:'Back.easeOut'
    });

    this.seridiTazele();
    this.time.delayedCall(350, () => { this.kilit = false; });
    this.arayuzuTazele();
  }

  /* ---------- program şeridi ---------- */
  seridiTazele(){
    if (this.blokNesne) this.blokNesne.forEach(o => o.destroy());
    this.blokNesne = [];

    const g = this.add.graphics().setDepth(9);
    g.fillStyle(0x0d1826, 0.92);
    g.fillRoundedRect(20, SERIT_Y - 26, EN - 40, 52, 12);
    g.lineStyle(2, 0x3d6285, 1);
    g.strokeRoundedRect(20, SERIT_Y - 26, EN - 40, 52, 12);
    this.blokNesne.push(g);

    if (!this.program.length){
      const bos = this.add.text(EN / 2, SERIT_Y, 'program boş — yön ekle', {
        fontFamily:'system-ui, sans-serif', fontSize:'17px', color:'#6f93b5'
      }).setOrigin(0.5).setDepth(10);
      this.blokNesne.push(bos);
      return;
    }

    const en = 38, ara = 5;
    const toplam = this.program.length * (en + ara) - ara;
    let x = EN / 2 - toplam / 2;
    this.program.forEach((yon, i) => {
      const c = this.add.container(x + en / 2, SERIT_Y).setDepth(10);
      const bg = this.add.graphics();
      bg.fillStyle(i === this.adim && this.calisiyor ? RENK.vurgu : 0x2f5877, 1);
      bg.fillRoundedRect(-en / 2, -18, en, 36, 8);
      const t = this.add.text(0, 0, yon.ok, {
        fontFamily:'system-ui, sans-serif', fontSize:'22px', fontStyle:'bold',
        color: i === this.adim && this.calisiyor ? '#2a2140' : '#ffffff'
      }).setOrigin(0.5);
      c.add([bg, t]);
      this.blokNesne.push(c);
      x += en + ara;
    });
  }

  /* ---------- yön tuşları ---------- */
  tuslariKur(){
    const n = YONLER.length;
    YONLER.forEach((y, i) => {
      const x = EN * (i + 0.5) / n;
      dugmeYap(this, x, TUS_Y, y.ok, 0x2f5877, () => this.blokEkle(y), 92, 56).setDepth(12);
    });

    dugmeYap(this, EN / 2 - 84, TUS_Y + 76, '⟲  SİL', 0x6b4a8a, () => this.blokSil(), 150, 52).setDepth(12);
    dugmeYap(this, EN / 2 + 84, TUS_Y + 76, '▶  ÇALIŞTIR', RENK.dogru, () => this.calistir(), 178, 52).setDepth(12);
  }

  blokEkle(yon){
    if (this.kilit || this.calisiyor) return;
    if (this.program.length >= 12){
      this.mesajGoster('Program dolu — SİL ile kısalt.', '#3d6285');
      return;
    }
    this.program.push(yon);
    this.seridiTazele();
  }

  blokSil(){
    if (this.kilit || this.calisiyor) return;
    this.program.pop();
    this.seridiTazele();
  }

  /* ---------- programı çalıştır ---------- */
  calistir(){
    if (this.kilit || this.calisiyor) return;
    if (!this.program.length){
      this.mesajGoster('Önce yön bloğu ekle.', '#3d6285');
      return;
    }
    this.calisiyor = true;
    this.adim = 0;
    this.pervane.setFrequency(60);
    this.sonrakiAdim();
  }

  sonrakiAdim(){
    const t = TURLAR[this.tur];

    if (this.adim >= this.program.length){
      /* program bitti — hedefte miyiz? */
      if (this.hucreX === t.hedef[0] && this.hucreY === t.hedef[1]) this.basarili();
      else                                                          this.kacirdi();
      return;
    }

    this.seridiTazele();
    const yon = this.program[this.adim];
    const yx = this.hucreX + yon.dx, yy = this.hucreY + yon.dy;
    const engel = this.duvarMi(yx, yy);

    if (engel){ this.carpti(engel, yx, yy); return; }

    /* GERÇEK FİZİK: dron hedef hücreye uçar */
    const m = this.hucreMerkezi(yx, yy);
    this.hedefNokta = m;
    this.physics.moveTo(this.dron, m.x, m.y, DRON_HIZI);
    this.ucuyor = true;
    this.hucreX = yx; this.hucreY = yy;
  }

  carpti(tur, yx, yy){
    const t = TURLAR[this.tur];
    this.calisiyor = false;
    this.ucuyor = false;
    this.dron.body.setVelocity(0, 0);
    this.seri = 0;
    this.can--;
    this.arayuzuTazele();

    /* GERÇEK FİZİK: dron engele çarpıp geri seker */
    const yon = this.program[this.adim];
    this.dron.body.setVelocity(-yon.dx * 260, -yon.dy * 260);
    this.tweens.add({ targets:this.dron, angle:Phaser.Math.Between(-25, 25), duration:220, yoyo:true });
    this.dumanlar.explode(16, this.dron.x, this.dron.y);
    this.cameras.main.shake(240, 0.013);
    this.cameras.main.flash(170, 220, 90, 90);

    /* çarpılan kare kısa süre kırmızı yansın */
    if (tur === 'duvar'){
      const m = this.hucreMerkezi(yx, yy);
      const uyari = this.add.graphics().setDepth(9);
      uyari.fillStyle(RENK.yanlis, 0.5);
      const H = this.hucre || HUCRE_AZAMI, py = Math.max(3, Math.round(H * 0.09));
      uyari.fillRoundedRect(m.x - H / 2 + py, m.y - H / 2 + py, H - py * 2, H - py * 2,
                            Math.max(4, Math.round(H * 0.11)));
      this.tweens.add({ targets:uyari, alpha:0, duration:700, delay:200,
        onComplete:() => uyari.destroy() });
    }

    this.mesajGoster(tur === 'duvar' ? t.duvarMsj : 'Haritanın dışına çıkamazsın!', '#b5453b');
    this.pervane.setFrequency(200);

    this.time.delayedCall(1100, () => {
      if (this.can <= 0){ this.bitir(false); return; }
      this.baslangicaDon();
    });
  }

  kacirdi(){
    const t = TURLAR[this.tur];
    this.calisiyor = false;
    this.seri = 0;
    this.can--;
    this.arayuzuTazele();
    this.dumanlar.explode(12, this.dron.x, this.dron.y);
    this.cameras.main.shake(200, 0.009);
    this.mesajGoster(t.kacirMsj, '#b5453b');
    this.pervane.setFrequency(200);

    this.time.delayedCall(1100, () => {
      if (this.can <= 0){ this.bitir(false); return; }
      this.baslangicaDon();
    });
  }

  baslangicaDon(){
    const t = TURLAR[this.tur];
    const b = this.hucreMerkezi(t.baslangic[0], t.baslangic[1]);
    this.dron.body.setVelocity(0, 0);
    this.dron.body.reset(b.x, b.y);
    this.dron.setAngle(0);
    this.hucreX = t.baslangic[0];
    this.hucreY = t.baslangic[1];
    this.program = [];
    this.adim = 0;
    this.calisiyor = false;
    this.seridiTazele();
    this.kilit = false;
  }

  basarili(){
    const t = TURLAR[this.tur];
    this.calisiyor = false;
    this.kilit = true;
    this.seri++;
    const kazanc = 200 + (this.seri - 1) * 50;
    this.puan += kazanc;

    this.dron.body.setVelocity(0, 0);
    this.pervane.setFrequency(200);

    const h = this.hucreMerkezi(t.hedef[0], t.hedef[1]);
    this.kivilcimlar.setParticleTint(RENK.dogru);
    this.kivilcimlar.explode(32, h.x, h.y);
    this.cameras.main.flash(150, 80, 210, 140);

    /* GERÇEK FİZİK: kargo drondan bırakılıp eve düşer */
    const kargo = this.physics.add.existing(
      this.add.text(this.dron.x, this.dron.y + 8, '📦', { fontSize:'29px' })
        .setOrigin(0.5).setDepth(31)
    );
    kargo.body.setAllowGravity(true);
    kargo.body.setVelocityY(60);
    this.time.delayedCall(600, () => {
      this.kivilcimlar.explode(10, kargo.x, kargo.y);
      kargo.destroy();
    });

    this.puanYazi.setText('Puan ' + this.puan);
    this.tweens.add({
      targets:this.puanYazi, scale:1.5, duration:140, yoyo:true, ease:'Back.easeOut'
    });
    const ucan = this.add.text(h.x, h.y - 30, '+' + kazanc, {
      fontFamily:'system-ui, sans-serif', fontSize:'31px', fontStyle:'bold',
      color:'#7ce0a3'
    }).setOrigin(0.5).setDepth(95);
    this.tweens.add({
      targets:ucan, y:ucan.y - 60, alpha:0, duration:760,
      ease:'Cubic.easeOut', onComplete:() => ucan.destroy()
    });

    this.mesajGoster('Kargo teslim edildi! 📦', '#1f6d4a');
    this.tur++;
    this.arayuzuTazele();

    this.time.delayedCall(2100, () => {
      if (this.tur >= TURLAR.length){ this.bitir(true); return; }
      this.turuBaslat();
    });
  }

  mesajGoster(metin, arka){
    if (this.mesaj) this.mesaj.destroy();
    this.mesaj = this.add.text(EN / 2, 208, metin, {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#ffffff', backgroundColor:arka,
      padding:{ x:12, y:7 }, align:'center', wordWrap:{ width:EN - 60 }
    }).setOrigin(0.5).setDepth(96).setAlpha(0);
    const t = this.mesaj;
    this.tweens.add({ targets:t, alpha:1, duration:150 });
    this.time.delayedCall(1700, () => {
      if (!t.active) return;
      this.tweens.add({
        targets:t, alpha:0, duration:250,
        onComplete:() => { if (this.mesaj === t) this.mesaj = null; t.destroy(); }
      });
    });
  }

  /* ---------- arayüz ---------- */
  arayuzKur(){
    /* Katalogda yönerge 120 karaktere çıkıyor; sabit yükseklikli şerit
       yazıyı iki yandan kesiyordu. Şerit metnin gerçek boyuna göre. */
    const yon = this.add.text(EN / 2, 22, OYUN_EMO + '  ' + TALIMAT, {
      fontFamily:'system-ui, sans-serif',
      fontSize: (TALIMAT.length > 92 ? '16px' : (TALIMAT.length > 54 ? '17px' : '20px')),
      fontStyle:'bold', color:'#ffffff', align:'center',
      wordWrap:{ width:EN - 52 }, lineSpacing:3
    }).setOrigin(0.5, 0).setDepth(61);

    const seritBoy = Math.max(104, yon.height + 62);
    const serit = this.add.graphics().setDepth(60);
    serit.fillStyle(0x0b1421, 0.97);
    serit.fillRoundedRect(10, 10, EN - 20, seritBoy, 18);
    yon.setDepth(61);
    const satirY = 10 + seritBoy - 22;
    this.seritAlt = 10 + seritBoy;

    this.puanYazi = this.add.text(30, satirY, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0, 0.5).setDepth(61);

    this.canYazi = this.add.text(EN - 30, satirY, '', { fontSize:'20px' })
      .setOrigin(1, 0.5).setDepth(61);

    this.ilerlemeYazi = this.add.text(EN / 2, satirY, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#9fc2e6'
    }).setOrigin(0.5).setDepth(61);

    this.gorevYazi = this.add.text(EN / 2, this.seritAlt + 26, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#ffffff', align:'center', wordWrap:{ width:EN - 50 }, lineSpacing:3
    }).setOrigin(0.5, 0).setDepth(61);

    this.arayuzuTazele();
  }

  arayuzuTazele(){
    this.canYazi.setText(
      '❤️'.repeat(Math.max(0, this.can)) +
      '🖤'.repeat(Math.max(0, CAN_SAYISI - this.can))
    );
    this.ilerlemeYazi.setText(`${this.tur} / ${TURLAR.length} görev`);
  }

  bitir(kazandi){
    /* Uygulama içindeyken kazanma ekranını uygulama gösteriyor. */
    if (kazandi && KOPRU){ KOPRU.bitir(BASARI, this.puan); return; }
    this.scene.start('GameOver', {
      kazandi, puan:this.puan, can:this.can,
      tur:this.tur, toplam:TURLAR.length
    });
  }

  /* ---------- her kare ---------- */
  update(){
    if (!this.ucuyor || !this.dron || !this.dron.body) return;
    const h = this.hedefNokta;
    if (Phaser.Math.Distance.Between(this.dron.x, this.dron.y, h.x, h.y) < 6){
      this.ucuyor = false;
      this.dron.body.reset(h.x, h.y);
      this.dron.body.setVelocity(0, 0);
      this.adim++;
      this.time.delayedCall(140, () => {
        if (this.calisiyor) this.sonrakiAdim();
      });
    }
  }
}

/* =====================================================================
   4) GAME OVER
   ===================================================================== */
class GameOverScene extends Phaser.Scene {
  constructor(){ super('GameOver'); }

  init(veri){ this.veri = veri; }

  create(){
    const { kazandi, puan, can, tur, toplam } = this.veri;
    gokyuzuCiz(this);

    const emo = this.add.text(EN / 2, 190, kazandi ? '🚁' : '💪', { fontSize:'97px' })
      .setOrigin(0.5).setScale(0);
    this.tweens.add({ targets:emo, scale:1, duration:520, ease:'Back.easeOut' });

    this.add.text(EN / 2, 300, kazandi ? 'KARGO TESLİM!' : 'TEKRAR DENE', {
      fontFamily:'system-ui, sans-serif', fontSize:'35px', fontStyle:'bold',
      color: kazandi ? '#7ce0a3' : '#ffd166', align:'center'
    }).setOrigin(0.5);

    this.add.text(EN / 2, 360,
      kazandi ? BASARI : `${tur} / ${toplam} görevi tamamladın — bir daha deneyelim mi?`, {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#cfe0ff',
      align:'center', wordWrap:{ width:EN - 70 }, lineSpacing:5
    }).setOrigin(0.5);

    const puanYazi = this.add.text(EN / 2, 456, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'42px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0.5);
    const sayac = { v:0 };
    this.tweens.add({
      targets:sayac, v:puan, duration:900, ease:'Cubic.easeOut',
      onUpdate:() => puanYazi.setText('Puan ' + Math.round(sayac.v))
    });

    this.add.text(EN / 2, 506,
      'Kalan can: ' + (can > 0 ? '❤️'.repeat(can) : '—'), {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#9fc2e6'
    }).setOrigin(0.5);

    if (kazandi){
      const konfeti = this.add.particles(EN / 2, -20, 'kivilcim', {
        speed:{ min:90, max:260 }, angle:{ min:60, max:120 },
        scale:{ start:0.8, end:0 }, alpha:{ start:1, end:0 },
        lifespan:2000, gravityY:180, quantity:2, frequency:70,
        tint:[0xffd166, 0x7ce0a3, 0x7fb2f0, 0xf07575]
      }).setDepth(5);
      this.time.delayedCall(2600, () => konfeti.stop());
    }

    dugmeYap(this, EN / 2, 606, '↻  TEKRAR OYNA', RENK.dogru, () => this.scene.start('Game'));

    /* Uygulama içinde: bu oyunda takılan çocuk sıradakine geçebilsin. */

    if (KOPRU) dugmeYap(this, EN / 2, 680, '⏭  SIRADAKİ OYUN', 0x4a679e, () => KOPRU.atla());
    if (!KOPRU) dugmeYap(this, EN / 2, 684, '☰  MENÜ',        0x3d6285, () => this.scene.start('Menu'));
  }
}

/* =====================================================================
   OYUNU BAŞLAT
   ===================================================================== */
/* =====================================================================
   NETLİK — cihazın piksel yoğunluğunda çizim
   ---------------------------------------------------------------------
   Oyun 480x800 mantıksal tuvalde çiziliyordu; telefon bunu 1080 piksele
   büyütünce yazılar ve kenarlar bulanıklaşıyordu. Çözüm: tuvali cihazın
   gerçek piksel sayısında açmak, dünyayı ise kamerayı NETLIK katına
   yakınlaştırarak yine 480x800 koordinatta tutmak. Böylece Graphics ile
   çizilen her şey (kartlar, şeritler, kutular) vektör keskinliğinde,
   yazılar da NETLIK çözünürlüğünde üretiliyor; oyun kodunun tek satırı
   değişmiyor.
   ===================================================================== */
const NETLIK = Math.min(3, Math.max(1, Math.round((window.devicePixelRatio || 1) * 2) / 2));

/* Phaser yazıyı kendi ara tuvaline çiziyor; çözünürlük verilmezse 1x
   üretilip yakınlaştırmada bulanıklaşır. Bütün yazılara varsayılan
   olarak NETLIK veriyoruz. */
(function(){
  const TS = Phaser.GameObjects.TextStyle.prototype;
  const eskiSetStyle = TS.setStyle;
  TS.setStyle = function(style, updateText, setDefaults){
    if (style && style.resolution === undefined) style.resolution = NETLIK;
    return eskiSetStyle.call(this, style, updateText, setDefaults);
  };
})();

/* Tuval NETLIK katına büyüdüğü için Phaser imleç konumunu da o ölçekte
   veriyor (0–960). Oyun koordinatına (0–480) çeviren yardımcı: sürükleme
   olayları zaten dünya koordinatı verdiği için yalnız pointer olaylarında
   kullanılıyor. */
function imlec(p){ return { x: p.x / NETLIK, y: p.y / NETLIK }; }

/* Her sahne başlarken kamerayı NETLIK katına yakınlaştırıp fizik
   dünyasını mantıksal ölçüde tutuyoruz: tuval büyüdü, dünya büyümedi.
   Sahne örnekleri oyun kurulumundan sonra eşzamansız oluştuğu için
   kanca Systems.start üzerine takılıyor — yeniden başlatmalarda da
   kendiliğinden çalışıyor. */
(function(){
  const SS = Phaser.Scenes.Systems.prototype;
  const eskiStart = SS.start;
  SS.start = function(veri){
    const sonuc = eskiStart.call(this, veri);
    const sc = this.scene;
    try{
      if (sc.cameras && sc.cameras.main){
        sc.cameras.main.setZoom(NETLIK);
        sc.cameras.main.centerOn(EN / 2, BOY / 2);
      }
      if (sc.physics && sc.physics.world) sc.physics.world.setBounds(0, 0, EN, BOY);
    }catch(e){ /* netlik ayarı oyunu engellemesin */ }
    return sonuc;
  };
})();

window.OYUN = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'oyun',
  width: EN * NETLIK,
  height: BOY * NETLIK,
  backgroundColor: '#0f1a26',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 520 } }
  },
  scene: [BootScene, MenuScene, GameScene, GameOverScene]
});

</script>
</body>
</html>
```

### dedektif-phaser.html — wordHighlight (14 oyun)
Dosya boyu: 30674 bayt · 844 satır

```html
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<title>5N1K Dedektifi — Phaser 3</title>
<script src="https://cdn.jsdelivr.net/npm/phaser@3.80.1/dist/phaser.min.js"></script>
<style>
  html, body { margin:0; padding:0; height:100%; background:#16171f; overflow:hidden;
    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
    -webkit-tap-highlight-color: transparent; touch-action:none; }
  #oyun { width:100%; height:100%; display:flex; align-items:center; justify-content:center; }
  canvas { display:block; }
</style>
</head>
<body>
<div id="oyun"></div>
<script>
/* =====================================================================
   5N1K DEDEKTİFİ — Phaser 3      (mekanik: wordHighlight · 14 oyun)
   ---------------------------------------------------------------------
   Kazanım: T.O.2.1 — Metindeki kim, ne zaman, nerede, niçin bilgilerini
   bulur.

   Sahneler : Boot → Menu → Game → GameOver
   Fizik    : Arcade.
              · Bulunan sözcük metinden KOPUP dedektif defterine
                fırlar, yerçekimiyle düşüp diğerlerinin üstüne yığılır.
              · Yanlış sözcük yerinde sarsılır, mürekkep sıçrar.
              · Büyüteç parmağı takip eder, altındaki sözcüğü büyütür.
   Görsel   : Bütün dokular Graphics ile çalışma anında üretilir —
              uygulama çevrimdışı kabukta (APK / iOS) çalışacağı için
              dışarıdan resim çekilmiyor.
   ===================================================================== */

const EN = 480, BOY = 800;

const RENK = {
  zeminUst : 0x1d1f2b,
  zeminAlt : 0x33374a,
  dogru    : 0x34c47b,
  yanlis   : 0xf07575,
  kagit    : 0xf7f2e4,
  kagitKnr : 0xd9d0b8,
  sozcuk   : 0xfdfbf5,
  metin    : '#2a2620',
  defter   : 0x243b2e,
  vurgu    : 0xffd166
};

/* ---------------------------------------------------------------------
   İÇERİK — uygulamadaki u08 oyununun birebir aynısı.
   Başka bir wordHighlight oyununa geçmek için yalnızca bu blok değişir.
   cevap[] : o turda bulunması gereken sözcükler (metindeki hâliyle).
   ------------------------------------------------------------------- */
/* ---------------- uygulama köprüsü ----------------
   Adres  dedektif.html#oyun=u08  biçiminde; katalog verisi üst pencereden
   okunuyor. Kazanınca completeGame() çağrılır.                          */
const KOPRU = (function(){
  try{
    const p = new URLSearchParams(location.hash.slice(1));
    const id = p.get('oyun');
    if (id && window.parent && window.parent !== window &&
        typeof window.parent.getGame === 'function'){
      const g = window.parent.getGame(id);
      if (g && g.cfg) return {
        oyun: g, cfg: g.cfg,
        bitir(mesaj, puan){ try{ window.parent.completeGame(mesaj || '', puan); }catch(e){} },
        /* Turun kendi metnini uygulamanın sesiyle okutur (Piper). */
        oku(metin){ try{ if (window.parent.oku) window.parent.oku(metin); }catch(e){} },
        /* Kaybetme ekranından: bu oyunu bırak, sıradakine geç. */
        atla(){ try{ if (window.parent.sonrakiOyunaGec) window.parent.sonrakiOyunaGec(); }catch(e){} }
      };
    }
  }catch(e){ /* çapraz kaynak engeli: tek başına oynanır */ }
  return null;
})();

/* HTML varlıklarını çöz: katalogda "Pay &lt; payda" gibi yazımlar var,
   çözülmezse ekranda "&lt;" olarak görünüyor ve öyle okunuyor. */
function varlikCoz(m){
  return String(m)
    .replace(/&nbsp;/gi, ' ')
    .replace(/&lt;/gi, '<').replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"').replace(/&#39;|&apos;/gi, "'")
    .replace(/&hellip;/gi, '…').replace(/&mdash;/gi, '—').replace(/&ndash;/gi, '–')
    .replace(/&times;/gi, '×').replace(/&divide;/gi, '÷').replace(/&deg;/gi, '°')
    .replace(/&rarr;/gi, '→').replace(/&larr;/gi, '←')
    .replace(/&amp;/gi, '&');            /* en sona: çift çözmeyi önler */
}

function duzMetin(x){
  return varlikCoz(String(x == null ? '' : x).replace(/<br\s*\/?>/gi,' ')
    .replace(/<[^>]+>/g,'')).replace(/[“”]/g,'"').replace(/\s+/g,' ').trim();
}
function tekSatir(x){ return duzMetin(x).replace(/\n/g,' '); }

const VARSAYILAN = {
  instruction:'Sorulan bilgiyi metinde bul, üstüne dokun',
  title2:'🗒️ DEDEKTİF NOTU',
  text:'Ali yaşlı komşusuna yardım etmek için pazar günü erkenden markete gitti',
  rounds:[
    { prompt:'KİM?', answer:['Ali'], hint:'Olayı yapan kişiyi bul.',
      wrongHint:'Bu bir kişi adı değil. Tekrar dene!' },
    { prompt:'NEREYE?', answer:['markete'], hint:'Gittiği yeri bul.',
      wrongHint:'Bu bir yer değil.' } ]
};

const CFG = KOPRU ? KOPRU.cfg : VARSAYILAN;

const METIN  = tekSatir(CFG.text);
const DEFTER = tekSatir(CFG.title2) || '🗒️ NOT';

/* Sözcük eşleştirme ölçütü.
   KUSUR: karşılaştırma tam eşitlikle yapılıyordu ve 9 tur OYNANAMAZ
   durumdaydı: cevap "kütüpanede" iken metindeki simge "Kütüpanede"
   (cümle başı büyük harf), cevap "paşa" iken simge "paşa," (virgüllü).
   Doğru sözcüğe dokunan çocuk hata alıyor, üç canı bitince oyunu
   kaybediyordu. Artık kenar noktalaması atılıp Türkçe küçük harfe
   çevrilerek karşılaştırılıyor. */
function anahtar(m){
  return String(m == null ? '' : m)
    .replace(/^[\s.,;:!?'"“”‘’()\[\]…—–-]+/, '')
    .replace(/[\s.,;:!?'"“”‘’()\[\]…—–-]+$/, '')
    .toLocaleLowerCase('tr');
}

const TURLAR = (CFG.rounds || []).map(r => ({
  soru:  tekSatir(r.prompt),
  cevap: (r.answer || []).map(x => tekSatir(x)),
  ipucu: tekSatir(r.hint),
  /* Katalogda yanlış yazılmış sözcüğün DOĞRU hâli duruyor (23 tur:
     "kütüpanede → Kütüphanede", "yalnış → Yanlış", "festival → şenlik").
     Bu alan hiç okunmuyordu; çocuk yanlış sözcüğü buluyor ama doğrusunu
     hiç görmüyordu — turun öğretici yarısı kayboluyordu. */
  duzelt: tekSatir(r.fixTo),
  hata:  tekSatir(r.wrongHint) || 'Bu değil, tekrar bak!'
}));

const OYUN_ADI = KOPRU ? tekSatir(KOPRU.oyun.title) : '5N1K DEDEKTİFİ';
const OYUN_EMO = KOPRU ? (KOPRU.oyun.emo || '🔍') : '🔍';
const TALIMAT  = tekSatir(CFG.instruction) || 'Sorulan bilgiyi metinde bul';
const IPUCU    = tekSatir(CFG.tip) || 'Büyüteci gezdir, doğru sözcüğü bulunca dokun.';
const BASARI   = tekSatir(CFG.successMsg) || 'Bütün ipuçlarını buldun!';

const CAN_SAYISI = 3;

/* --- Yerleşim -------------------------------------------------------- */
const KAGIT_UST  = 236;
const SATIR_BOY  = 44;
const DEFTER_UST = 494;
const DEFTER_ALT = 664;

/* =====================================================================
   1) BOOT — dokuları üret
   ===================================================================== */
class BootScene extends Phaser.Scene {
  constructor(){ super('Boot'); }

  create(){
    this.dokuKivilcim();
    this.dokuMurekkep();
    this.dokuBuyutec();
    /* Uygulama içinde çocuk oyunu listeden zaten seçti; menüyü atla. */
    this.scene.start(KOPRU ? 'Game' : 'Menu');
  }

  dokuKivilcim(){
    const g = this.make.graphics({ add:false });
    g.fillStyle(0xffffff, 1);
    g.fillCircle(8, 8, 8);
    g.generateTexture('kivilcim', 16, 16);
    g.destroy();
  }

  /* Mürekkep lekesi — yanlış dokunuşta sıçrar */
  dokuMurekkep(){
    const g = this.make.graphics({ add:false });
    g.fillStyle(0x2a2620, 1);
    g.fillCircle(9, 9, 9);
    g.generateTexture('murekkep', 18, 18);
    g.destroy();
  }

  /* Büyüteç */
  dokuBuyutec(){
    const R = 40, W = 108, H = 108;
    const g = this.make.graphics({ add:false });
    /* sap */
    g.lineStyle(11, 0x8a5a2f, 1);
    g.lineBetween(R + 26, R + 26, W - 10, H - 10);
    /* cam */
    g.fillStyle(0xbfe6ff, 0.16);
    g.fillCircle(R + 4, R + 4, R - 4);
    /* çerçeve */
    g.lineStyle(7, 0xd8c9ae, 1);
    g.strokeCircle(R + 4, R + 4, R - 4);
    g.lineStyle(3, 0x8a7c62, 1);
    g.strokeCircle(R + 4, R + 4, R - 8);
    /* parlama */
    g.fillStyle(0xffffff, 0.34);
    g.fillEllipse(R - 10, R - 12, 22, 13);
    g.generateTexture('buyutec', W, H);
    g.destroy();
  }
}

/* =====================================================================
   Ortak yardımcılar
   ===================================================================== */
function odaCiz(sc){
  const g = sc.add.graphics();
  g.fillGradientStyle(RENK.zeminUst, RENK.zeminUst, RENK.zeminAlt, RENK.zeminAlt, 1);
  g.fillRect(0, 0, EN, BOY);

  for (let i = 0; i < 20; i++){
    const s = sc.add.circle(
      Phaser.Math.Between(6, EN - 6),
      Phaser.Math.Between(6, BOY - 6),
      Phaser.Math.FloatBetween(1.5, 3.5),
      0xffffff,
      Phaser.Math.FloatBetween(0.03, 0.1)
    );
    sc.tweens.add({
      targets:s, alpha:0.015,
      duration:Phaser.Math.Between(1600, 3200),
      yoyo:true, repeat:-1, delay:Phaser.Math.Between(0, 2000)
    });
  }
  return g;
}

function dugmeYap(sc, x, y, metin, renk, geriCagri){
  const c = sc.add.container(x, y);
  const g = sc.add.graphics();
  g.fillStyle(renk, 1);
  g.fillRoundedRect(-140, -30, 280, 60, 30);
  g.fillStyle(0xffffff, 0.16);
  g.fillRoundedRect(-140, -30, 280, 24, { tl:30, tr:30, bl:0, br:0 });
  const t = sc.add.text(0, 0, metin, {
    fontFamily:'system-ui, sans-serif', fontSize:'25px',
    fontStyle:'bold', color:'#ffffff'
  }).setOrigin(0.5);
  c.add([g, t]);
  c.setSize(280, 60).setInteractive({ useHandCursor:true });
  c.on('pointerover', () => sc.tweens.add({ targets:c, scale:1.05, duration:110 }));
  c.on('pointerout',  () => sc.tweens.add({ targets:c, scale:1.00, duration:110 }));
  c.on('pointerdown', () => sc.tweens.add({
    targets:c, scale:0.93, duration:90, yoyo:true, onComplete:geriCagri
  }));
  return c;
}

/* =====================================================================
   2) MENU
   ===================================================================== */
class MenuScene extends Phaser.Scene {
  constructor(){ super('Menu'); }

  create(){
    odaCiz(this);

    const b = this.add.image(EN / 2, 206, 'buyutec').setScale(1.15);
    this.tweens.add({
      targets:b, x:EN / 2 + 26, y:194, angle:-12, duration:1700,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });

    const baslik = this.add.text(EN / 2, 336, OYUN_ADI, {
      fontFamily:'system-ui, sans-serif', fontSize:'44px', fontStyle:'bold',
      color:'#ffffff', align:'center', lineSpacing:5
    }).setOrigin(0.5);
    this.tweens.add({
      targets:baslik, scale:1.04, duration:1400,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });

    this.add.text(EN / 2, 424, TALIMAT, {
      fontFamily:'system-ui, sans-serif', fontSize:'21px',
      color:'#d5dced', align:'center', wordWrap:{ width:EN - 60 }
    }).setOrigin(0.5);

    const kart = this.add.graphics();
    kart.fillStyle(0x14161f, 0.92);
    kart.fillRoundedRect(30, 466, EN - 60, 84, 16);
    kart.lineStyle(2, 0x4b5168, 1);
    kart.strokeRoundedRect(30, 466, EN - 60, 84, 16);
    this.add.text(EN / 2, 508, IPUCU, {
      fontFamily:'system-ui, sans-serif', fontSize:'17px', fontStyle:'bold',
      color:'#ffd166', align:'center', wordWrap:{ width:EN - 90 }, lineSpacing:4
    }).setOrigin(0.5);

    dugmeYap(this, EN / 2, 618, '▶  BAŞLA', RENK.dogru, () => this.scene.start('Game'));

    this.add.text(EN / 2, 714, `${TURLAR.length} ipucu  ·  ${CAN_SAYISI} can`, {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', color:'#9aa3bb'
    }).setOrigin(0.5);
  }
}

/* =====================================================================
   3) GAME
   ===================================================================== */
class GameScene extends Phaser.Scene {
  constructor(){ super('Game'); }

  create(){
    this.can   = CAN_SAYISI;
    this.puan  = 0;
    this.seri  = 0;
    this.tur   = 0;
    this.kilit = true;

    /* Phaser sahne örneğini yeniden kullanır — TEKRAR OYNA'da eski
       nesnelere işaret etmesinler. */
    this.sozcukNesne = null;
    this.mesaj       = null;
    this.buyutec     = null;

    odaCiz(this);

    this.kivilcimlar = this.add.particles(0, 0, 'kivilcim', {
      speed:{ min:130, max:340 }, angle:{ min:0, max:360 },
      scale:{ start:0.85, end:0 }, alpha:{ start:1, end:0 },
      lifespan:600, gravityY:320, blendMode:'ADD', emitting:false
    }).setDepth(90);

    this.murekkepler = this.add.particles(0, 0, 'murekkep', {
      speed:{ min:60, max:180 }, angle:{ min:200, max:340 },
      scale:{ start:0.9, end:0 }, alpha:{ start:0.8, end:0 },
      lifespan:620, gravityY:420, emitting:false
    }).setDepth(80);

    this.sahneKur();
    this.arayuzKur();
    this.metniDiz();
    this.turuBaslat();
  }

  /* ---------- sabit sahne ---------- */
  sahneKur(){
    /* not kâğıdı */
    const g = this.add.graphics().setDepth(4);
    g.fillStyle(RENK.kagit, 1);
    g.fillRoundedRect(20, KAGIT_UST - 26, EN - 40, 214, 12);
    g.lineStyle(2, RENK.kagitKnr, 1);
    g.strokeRoundedRect(20, KAGIT_UST - 26, EN - 40, 214, 12);
    for (let y = KAGIT_UST + 28; y < KAGIT_UST + 186; y += SATIR_BOY){
      g.lineStyle(1, 0xe4dcc9, 1);
      g.lineBetween(32, y, EN - 32, y);
    }
    this.add.text(32, KAGIT_UST - 18, 'OLAY YERİ TUTANAĞI', {
      fontFamily:'system-ui, sans-serif', fontSize:'14px', fontStyle:'bold',
      color:'#a89a7c'
    }).setDepth(5);

    /* dedektif defteri */
    const d = this.add.graphics().setDepth(4);
    d.fillStyle(RENK.defter, 0.95);
    d.fillRoundedRect(20, DEFTER_UST - 30, EN - 40, DEFTER_ALT - DEFTER_UST + 50, 14);
    d.lineStyle(2, 0x3f6b58, 1);
    d.strokeRoundedRect(20, DEFTER_UST - 30, EN - 40, DEFTER_ALT - DEFTER_UST + 50, 14);
    this.add.text(EN / 2, DEFTER_UST - 16, DEFTER, {
      fontFamily:'system-ui, sans-serif', fontSize:'16px', fontStyle:'bold',
      color:'#7fbfa0'
    }).setOrigin(0.5).setDepth(5);

    /* NOT: Phaser'da collider(grup, TEK nesne) callback'e parametreleri
       ters veriyor; engeller staticGroup içinde. */
    this.defterDuvar = this.physics.add.staticGroup();
    this.defterDuvar.add(this.add.rectangle(EN / 2, DEFTER_ALT + 8, EN - 56, 16, 0, 0));
    this.defterDuvar.add(this.add.rectangle(26,      BOY / 2, 14, BOY * 2, 0, 0));
    this.defterDuvar.add(this.add.rectangle(EN - 26, BOY / 2, 14, BOY * 2, 0, 0));

    this.defterdekiler = this.physics.add.group();
    this.physics.add.collider(this.defterdekiler, this.defterDuvar);
    this.physics.add.collider(this.defterdekiler, this.defterdekiler);

    /* büyüteç — parmağı takip eder */
    this.buyutec = this.add.image(EN / 2, KAGIT_UST + 80, 'buyutec')
      .setScale(0.78).setDepth(50).setAlpha(0.9);
    this.input.on('pointermove', (p) => {
      const im = imlec(p);
      this.buyutec.setPosition(im.x + 22, im.y + 22);
      this.sozcukleriTara(im.x, im.y);
    });
  }

  /* Büyütecin altındaki sözcüğü hafifçe büyüt */
  sozcukleriTara(px, py){
    if (!this.sozcukNesne) return;
    this.sozcukNesne.forEach(c => {
      if (c.getData('bulundu')) return;
      const yakin = Math.abs(c.x - px) < c.getData('en') / 2 + 6 &&
                    Math.abs(c.y - py) < 22;
      const hedef = yakin ? 1.12 : 1;
      if (c.scaleX !== hedef) c.setScale(hedef);
    });
  }

  /* ---------- metni sözcük kartlarına böl ---------- */
  metniDiz(){
    const SOL = 34, SAG = EN - 34, ARA = 7;
    const kelimeler = METIN.split(' ');
    this.sozcukNesne = [];

    /* genişlikleri ölç */
    const olcu = kelimeler.map(k => {
      const g = this.add.text(0, 0, k, {
        fontFamily:'system-ui, sans-serif', fontSize:'21px', fontStyle:'bold'
      });
      const w = g.width + 14;
      g.destroy();
      return w;
    });

    /* satırlara böl */
    const satirlar = [];
    let satir = [], gen = 0;
    olcu.forEach((w, i) => {
      if (gen + w + ARA > SAG - SOL && satir.length){
        satirlar.push({ ogeler:satir, gen:gen - ARA });
        satir = []; gen = 0;
      }
      satir.push({ i, w });
      gen += w + ARA;
    });
    if (satir.length) satirlar.push({ ogeler:satir, gen:gen - ARA });

    satirlar.forEach((s, si) => {
      let x = EN / 2 - s.gen / 2;
      const y = KAGIT_UST + 18 + si * SATIR_BOY;   /* başlığın altında başla */
      s.ogeler.forEach(({ i, w }) => {
        this.sozcukYap(kelimeler[i], i, x + w / 2, y, w);
        x += w + ARA;
      });
    });
  }

  sozcukYap(kelime, i, x, y, w){
    const c = this.add.container(x, y).setDepth(20);
    const g = this.add.graphics();
    const yazi = this.add.text(0, 0, kelime, {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', fontStyle:'bold',
      color: RENK.metin
    }).setOrigin(0.5);
    c.add([g, yazi]);
    c.setSize(w, 34);
    c.setData('kelime', kelime);
    c.setData('index', i);
    c.setData('bulundu', false);
    c.setData('cizim', g);
    c.setData('en', w);
    this.sozcukCiz(c, false);

    /* Dokunma alanını Phaser'a bırakıyoruz: Container'a elle
       Rectangle(-W/2,-H/2,…) verilince kaydırma bir kez daha uygulanıyor ve
       alan sola-yukarı kayıyor — nesneyi tutmak için sol üstüne basmak
       gerekiyordu. setSize + argümansız setInteractive() alanı ortalıyor.
       Alan görselden bir miktar geniş: parmak payı. */
    c.setSize(w + 20, 34 + 20);
    c.setInteractive();
    c.on('pointerdown', () => this.sozcugeDokun(c));
    this.sozcukNesne.push(c);
    return c;
  }

  sozcukCiz(c, bulundu){
    const g = c.getData('cizim'), w = c.getData('en');
    g.clear();
    g.fillStyle(bulundu ? 0xd8f0e2 : RENK.sozcuk, bulundu ? 1 : 0.001);
    g.fillRoundedRect(-w / 2, -17, w, 34, 7);
    if (bulundu){
      g.lineStyle(2, RENK.dogru, 1);
      g.strokeRoundedRect(-w / 2, -17, w, 34, 7);
    }
  }

  /* ---------- tur ---------- */
  turuBaslat(){
    const t = TURLAR[this.tur];
    this.kilit = true;
    this.kalan = t.cevap.slice();

    this.soruYazi.setText(t.soru);
    this.ipucuYazi.setText(t.ipucu);
    this.tweens.add({
      targets:this.soruYazi, scale:{ from:0.8, to:1 }, duration:300, ease:'Back.easeOut'
    });

    this.time.delayedCall(300, () => { this.kilit = false; });
    this.arayuzuTazele();
  }

  sozcugeDokun(c){
    if (this.kilit || c.getData('bulundu')) return;
    const kelime = c.getData('kelime');
    const k = anahtar(kelime);

    if (!this.kalan.some(x => anahtar(x) === k)){ this.yanlis(c); return; }

    /* doğru sözcük */
    c.setData('bulundu', true);
    c.disableInteractive();
    this.sozcukCiz(c, true);
    this.kalan = this.kalan.filter(x => anahtar(x) !== k);

    this.kivilcimlar.setParticleTint(RENK.dogru);
    this.kivilcimlar.explode(14, c.x, c.y);
    this.seri++;
    const kazanc = 100 + (this.seri - 1) * 20;
    this.puan += kazanc;
    this.puanYazi.setText('Puan ' + this.puan);
    this.tweens.add({
      targets:this.puanYazi, scale:1.4, duration:120, yoyo:true, ease:'Back.easeOut'
    });

    /* GERÇEK FİZİK: sözcük metinden kopup deftere fırlar.
       Doğru hâli varsa deftere DÜZELTİLMİŞ biçim yazılıyor ve
       "yanlış → doğru" kısa iletisi gösteriliyor. */
    const t = TURLAR[this.tur];
    if (t.duzelt){
      this.deftereAt(c, t.duzelt, true);
      this.mesajGoster(kelime + '  →  ' + t.duzelt, '#1f6d4a');
    } else {
      this.deftereAt(c, kelime);
    }
    this.arayuzuTazele();

    if (!this.kalan.length){
      this.kilit = true;
      this.time.delayedCall(650, () => this.turuBitir());
    }
  }

  deftereAt(kaynak, kelime, duzeltilmis){
    const c = this.add.container(kaynak.x, kaynak.y).setDepth(26);
    const yazi = this.add.text(0, 0, kelime, {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#1f4a35'
    }).setOrigin(0.5);
    /* Genişlik kaynağın değil YAZININ gerçek ölçüsünden: düzeltilmiş
       biçim ("Kütüphanede") yanlışından uzun olabiliyor ve kutudan
       taşıyordu. */
    const w = Math.max(kaynak.getData('en'), yazi.width + 14);
    const g = this.add.graphics();
    g.fillStyle(duzeltilmis ? 0xfff3cf : 0xd8f0e2, 1);
    g.fillRoundedRect(-w / 2, -17, w, 34, 7);
    g.lineStyle(2, duzeltilmis ? RENK.vurgu : RENK.dogru, 1);
    g.strokeRoundedRect(-w / 2, -17, w, 34, 7);
    c.add([g, yazi]);
    c.setSize(w, 34);

    /* Arcade gövdesi — gruba ÖNCE ekle: Arcade Group add() sırasında
       kendi varsayılanlarını gövdeye basıyor. */
    this.defterdekiler.add(c);
    c.body.setSize(w, 34);
    c.body.setBounce(0.3, 0.3);
    c.body.setDragX(120);
    /* deftere doğru fırlat */
    c.body.setVelocity((EN / 2 - kaynak.x) * 1.1, -160);
    this.tweens.add({ targets:c, angle:Phaser.Math.Between(-14, 14), duration:520 });
  }

  yanlis(c){
    const t = TURLAR[this.tur];
    this.seri = 0;
    this.can--;
    this.arayuzuTazele();

    this.tweens.add({
      targets:c, x:{ from:c.x - 5, to:c.x + 5 },
      duration:55, yoyo:true, repeat:3,
      onComplete:() => this.tweens.add({ targets:c, x:c.x, duration:1 })
    });
    this.murekkepler.explode(12, c.x, c.y);
    this.cameras.main.shake(210, 0.011);
    this.cameras.main.flash(160, 220, 90, 90);
    this.tweens.add({
      targets:this.canYazi, angle:{ from:-12, to:12 },
      duration:70, yoyo:true, repeat:3,
      onComplete:() => this.canYazi.setAngle(0)
    });
    this.mesajGoster(t.hata, '#b5453b');

    if (this.can <= 0){
      this.kilit = true;
      this.time.delayedCall(900, () => this.bitir(false));
    }
  }

  turuBitir(){
    const t = TURLAR[this.tur];
    const bonus = 100;
    this.puan += bonus;
    this.puanYazi.setText('Puan ' + this.puan);
    this.kivilcimlar.setParticleTint(RENK.vurgu);
    this.kivilcimlar.explode(20, EN / 2, DEFTER_UST + 30);
    this.cameras.main.flash(150, 80, 210, 140);
    this.mesajGoster('İpucu bulundu: ' + t.soru + '  →  ' + t.cevap.join(' '), '#1f6d4a');

    this.tur++;
    this.arayuzuTazele();

    this.time.delayedCall(1700, () => {
      if (this.tur >= TURLAR.length){ this.bitir(true); return; }
      this.turuBaslat();
    });
  }

  mesajGoster(metin, arka){
    if (this.mesaj) this.mesaj.destroy();
    this.mesaj = this.add.text(EN / 2, 442, metin, {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#ffffff', backgroundColor:arka,
      padding:{ x:12, y:7 }, align:'center', wordWrap:{ width:EN - 60 }
    }).setOrigin(0.5).setDepth(96).setAlpha(0);
    const t = this.mesaj;
    this.tweens.add({ targets:t, alpha:1, duration:150 });
    this.time.delayedCall(1500, () => {
      if (!t.active) return;
      this.tweens.add({
        targets:t, alpha:0, duration:250,
        onComplete:() => { if (this.mesaj === t) this.mesaj = null; t.destroy(); }
      });
    });
  }

  /* ---------- arayüz ---------- */
  arayuzKur(){
    /* Katalogda yönerge 120 karaktere çıkıyor; sabit yükseklikli şerit
       yazıyı iki yandan kesiyordu. Şerit metnin gerçek boyuna göre. */
    const yon = this.add.text(EN / 2, 22, OYUN_EMO + '  ' + TALIMAT, {
      fontFamily:'system-ui, sans-serif',
      fontSize: (TALIMAT.length > 92 ? '16px' : (TALIMAT.length > 54 ? '17px' : '20px')),
      fontStyle:'bold', color:'#ffffff', align:'center',
      wordWrap:{ width:EN - 52 }, lineSpacing:3
    }).setOrigin(0.5, 0).setDepth(61);

    const seritBoy = Math.max(104, yon.height + 62);
    const serit = this.add.graphics().setDepth(60);
    serit.fillStyle(0x12141c, 0.97);
    serit.fillRoundedRect(10, 10, EN - 20, seritBoy, 18);
    yon.setDepth(61);
    const satirY = 10 + seritBoy - 22;
    this.seritAlt = 10 + seritBoy;

    this.puanYazi = this.add.text(30, satirY, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0, 0.5).setDepth(61);

    this.canYazi = this.add.text(EN - 30, satirY, '', { fontSize:'20px' })
      .setOrigin(1, 0.5).setDepth(61);

    this.ilerlemeYazi = this.add.text(EN / 2, satirY, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#9aa3bb'
    }).setOrigin(0.5).setDepth(61);

    this.soruYazi = this.add.text(EN / 2, 148, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'33px', fontStyle:'bold',
      color:'#ffd166', align:'center'
    }).setOrigin(0.5).setDepth(61);

    this.ipucuYazi = this.add.text(EN / 2, 186, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'17px',
      color:'#b9c1d6', align:'center', wordWrap:{ width:EN - 60 }
    }).setOrigin(0.5).setDepth(61);

    this.arayuzuTazele();
  }

  arayuzuTazele(){
    this.canYazi.setText(
      '❤️'.repeat(Math.max(0, this.can)) +
      '🖤'.repeat(Math.max(0, CAN_SAYISI - this.can))
    );
    this.ilerlemeYazi.setText(`${this.tur} / ${TURLAR.length} ipucu`);
  }

  bitir(kazandi){
    /* Uygulama içindeyken kazanma ekranını uygulama gösteriyor. */
    if (kazandi && KOPRU){ KOPRU.bitir(BASARI, this.puan); return; }
    this.scene.start('GameOver', {
      kazandi, puan:this.puan, can:this.can,
      tur:this.tur, toplam:TURLAR.length
    });
  }

  /* ---------- her kare ---------- */
  update(){
    /* Sahne kapanırken grup yok edilir ama referans truthy kalır;
       children denetimi olmadan getChildren() patlıyor. */
    if (!this.defterdekiler || !this.defterdekiler.children) return;
    /* defterden kaçan kartı geri getir */
    this.defterdekiler.getChildren().forEach(c => {
      if (!c.active) return;
      if (c.y > BOY + 60 || c.x < -60 || c.x > EN + 60){
        c.body.reset(Phaser.Math.Between(90, EN - 90), DEFTER_UST + 10);
        c.body.setVelocity(0, 0);
      }
    });
  }
}

/* =====================================================================
   4) GAME OVER
   ===================================================================== */
class GameOverScene extends Phaser.Scene {
  constructor(){ super('GameOver'); }

  init(veri){ this.veri = veri; }

  create(){
    const { kazandi, puan, can, tur, toplam } = this.veri;
    odaCiz(this);

    const emo = this.add.text(EN / 2, 190, kazandi ? '🔍' : '💪', { fontSize:'97px' })
      .setOrigin(0.5).setScale(0);
    this.tweens.add({ targets:emo, scale:1, duration:520, ease:'Back.easeOut' });

    this.add.text(EN / 2, 300, kazandi ? 'DAVA ÇÖZÜLDÜ!' : 'TEKRAR DENE', {
      fontFamily:'system-ui, sans-serif', fontSize:'35px', fontStyle:'bold',
      color: kazandi ? '#7ce0a3' : '#ffd166', align:'center'
    }).setOrigin(0.5);

    this.add.text(EN / 2, 360,
      kazandi ? BASARI : `${tur} / ${toplam} ipucu buldun — bir daha deneyelim mi?`, {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#d5dced',
      align:'center', wordWrap:{ width:EN - 70 }, lineSpacing:5
    }).setOrigin(0.5);

    const puanYazi = this.add.text(EN / 2, 456, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'42px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0.5);
    const sayac = { v:0 };
    this.tweens.add({
      targets:sayac, v:puan, duration:900, ease:'Cubic.easeOut',
      onUpdate:() => puanYazi.setText('Puan ' + Math.round(sayac.v))
    });

    this.add.text(EN / 2, 506,
      'Kalan can: ' + (can > 0 ? '❤️'.repeat(can) : '—'), {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#9aa3bb'
    }).setOrigin(0.5);

    if (kazandi){
      const konfeti = this.add.particles(EN / 2, -20, 'kivilcim', {
        speed:{ min:90, max:260 }, angle:{ min:60, max:120 },
        scale:{ start:0.8, end:0 }, alpha:{ start:1, end:0 },
        lifespan:2000, gravityY:180, quantity:2, frequency:70,
        tint:[0xffd166, 0x7ce0a3, 0x7fb2f0, 0xf07575]
      }).setDepth(5);
      this.time.delayedCall(2600, () => konfeti.stop());
    }

    dugmeYap(this, EN / 2, 606, '↻  TEKRAR OYNA', RENK.dogru, () => this.scene.start('Game'));

    /* Uygulama içinde: bu oyunda takılan çocuk sıradakine geçebilsin. */

    if (KOPRU) dugmeYap(this, EN / 2, 680, '⏭  SIRADAKİ OYUN', 0x4a679e, () => KOPRU.atla());
    if (!KOPRU) dugmeYap(this, EN / 2, 684, '☰  MENÜ',        0x4b5168, () => this.scene.start('Menu'));
  }
}

/* =====================================================================
   OYUNU BAŞLAT
   ===================================================================== */
/* =====================================================================
   NETLİK — cihazın piksel yoğunluğunda çizim
   ---------------------------------------------------------------------
   Oyun 480x800 mantıksal tuvalde çiziliyordu; telefon bunu 1080 piksele
   büyütünce yazılar ve kenarlar bulanıklaşıyordu. Çözüm: tuvali cihazın
   gerçek piksel sayısında açmak, dünyayı ise kamerayı NETLIK katına
   yakınlaştırarak yine 480x800 koordinatta tutmak. Böylece Graphics ile
   çizilen her şey (kartlar, şeritler, kutular) vektör keskinliğinde,
   yazılar da NETLIK çözünürlüğünde üretiliyor; oyun kodunun tek satırı
   değişmiyor.
   ===================================================================== */
const NETLIK = Math.min(3, Math.max(1, Math.round((window.devicePixelRatio || 1) * 2) / 2));

/* Phaser yazıyı kendi ara tuvaline çiziyor; çözünürlük verilmezse 1x
   üretilip yakınlaştırmada bulanıklaşır. Bütün yazılara varsayılan
   olarak NETLIK veriyoruz. */
(function(){
  const TS = Phaser.GameObjects.TextStyle.prototype;
  const eskiSetStyle = TS.setStyle;
  TS.setStyle = function(style, updateText, setDefaults){
    if (style && style.resolution === undefined) style.resolution = NETLIK;
    return eskiSetStyle.call(this, style, updateText, setDefaults);
  };
})();

/* Tuval NETLIK katına büyüdüğü için Phaser imleç konumunu da o ölçekte
   veriyor (0–960). Oyun koordinatına (0–480) çeviren yardımcı: sürükleme
   olayları zaten dünya koordinatı verdiği için yalnız pointer olaylarında
   kullanılıyor. */
function imlec(p){ return { x: p.x / NETLIK, y: p.y / NETLIK }; }

/* Her sahne başlarken kamerayı NETLIK katına yakınlaştırıp fizik
   dünyasını mantıksal ölçüde tutuyoruz: tuval büyüdü, dünya büyümedi.
   Sahne örnekleri oyun kurulumundan sonra eşzamansız oluştuğu için
   kanca Systems.start üzerine takılıyor — yeniden başlatmalarda da
   kendiliğinden çalışıyor. */
(function(){
  const SS = Phaser.Scenes.Systems.prototype;
  const eskiStart = SS.start;
  SS.start = function(veri){
    const sonuc = eskiStart.call(this, veri);
    const sc = this.scene;
    try{
      if (sc.cameras && sc.cameras.main){
        sc.cameras.main.setZoom(NETLIK);
        sc.cameras.main.centerOn(EN / 2, BOY / 2);
      }
      if (sc.physics && sc.physics.world) sc.physics.world.setBounds(0, 0, EN, BOY);
    }catch(e){ /* netlik ayarı oyunu engellemesin */ }
    return sonuc;
  };
})();

window.OYUN = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'oyun',
  width: EN * NETLIK,
  height: BOY * NETLIK,
  backgroundColor: '#16171f',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 700 } }
  },
  scene: [BootScene, MenuScene, GameScene, GameOverScene]
});

</script>
</body>
</html>
```

### grafik-phaser.html — graphBuild (11 oyun)
Dosya boyu: 34021 bayt · 902 satır

```html
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<title>Veri Laboratuvarı — Phaser 3</title>
<script src="https://cdn.jsdelivr.net/npm/phaser@3.80.1/dist/phaser.min.js"></script>
<style>
  html, body { margin:0; padding:0; height:100%; background:#101a22; overflow:hidden;
    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
    -webkit-tap-highlight-color: transparent; touch-action:none; }
  #oyun { width:100%; height:100%; display:flex; align-items:center; justify-content:center; }
  canvas { display:block; }
</style>
</head>
<body>
<div id="oyun"></div>
<script>
/* =====================================================================
   VERİ LABORATUVARI — Phaser 3      (mekanik: graphBuild · 11 oyun)
   ---------------------------------------------------------------------
   Kazanım: MAT.2.4.1 (c-f) — Topladığı verileri sıklık tablosundan
   şekil grafiğine dönüştürür.

   Sahneler : Boot → Menu → Game → GameOver
   Fizik    : Arcade.
              · Bloklar depoya YERÇEKİMİYLE dökülür ve yığılır.
              · Sütuna bırakılan blok düşer, öncekilerin üstüne oturur —
                çubuk grafik gerçekten fizikle inşa edilir.
              · Yanlış sütuna bırakılan blok geri fırlar.
   Görsel   : Bütün dokular Graphics ile çalışma anında üretilir —
              uygulama çevrimdışı kabukta (APK / iOS) çalışacağı için
              dışarıdan resim çekilmiyor.
   ===================================================================== */

const EN = 480, BOY = 800;

const RENK = {
  zeminUst : 0x16242f,
  zeminAlt : 0x27414f,
  dogru    : 0x34c47b,
  yanlis   : 0xf07575,
  sutun    : 0x1b2f3c,
  vurgu    : 0xffd166
};

/* ---------------------------------------------------------------------
   İÇERİK — uygulamadaki v42 oyununun birebir aynısı.
   Başka bir graphBuild oyununa geçmek için yalnızca bu blok değişir.
   sekil: 'yildiz' | 'daire' | 'ucgen'
   ------------------------------------------------------------------- */
/* ---------------- uygulama köprüsü ----------------
   Adres  grafik.html#oyun=v39  biçiminde; katalog verisi üst pencereden
   okunuyor. Kazanınca completeGame() çağrılır.                          */
const KOPRU = (function(){
  try{
    const p = new URLSearchParams(location.hash.slice(1));
    const id = p.get('oyun');
    if (id && window.parent && window.parent !== window &&
        typeof window.parent.getGame === 'function'){
      const g = window.parent.getGame(id);
      if (g && g.cfg) return {
        oyun: g, cfg: g.cfg,
        bitir(mesaj, puan){ try{ window.parent.completeGame(mesaj || '', puan); }catch(e){} },
        /* Turun kendi metnini uygulamanın sesiyle okutur (Piper). */
        oku(metin){ try{ if (window.parent.oku) window.parent.oku(metin); }catch(e){} },
        /* Kaybetme ekranından: bu oyunu bırak, sıradakine geç. */
        atla(){ try{ if (window.parent.sonrakiOyunaGec) window.parent.sonrakiOyunaGec(); }catch(e){} }
      };
    }
  }catch(e){ /* çapraz kaynak engeli: tek başına oynanır */ }
  return null;
})();

/* HTML varlıklarını çöz: katalogda "Pay &lt; payda" gibi yazımlar var,
   çözülmezse ekranda "&lt;" olarak görünüyor ve öyle okunuyor. */
function varlikCoz(m){
  return String(m)
    .replace(/&nbsp;/gi, ' ')
    .replace(/&lt;/gi, '<').replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"').replace(/&#39;|&apos;/gi, "'")
    .replace(/&hellip;/gi, '…').replace(/&mdash;/gi, '—').replace(/&ndash;/gi, '–')
    .replace(/&times;/gi, '×').replace(/&divide;/gi, '÷').replace(/&deg;/gi, '°')
    .replace(/&rarr;/gi, '→').replace(/&larr;/gi, '←')
    .replace(/&amp;/gi, '&');            /* en sona: çift çözmeyi önler */
}

function duzMetin(x){
  return varlikCoz(String(x == null ? '' : x).replace(/<br\s*\/?>/gi,' ')
    .replace(/<[^>]+>/g,'')).replace(/[“”]/g,'"').replace(/\s+/g,' ').trim();
}
function tekSatir(x){ return duzMetin(x).replace(/\n/g,' '); }

const VARSAYILAN = {
  instruction:'Blokları doğru sütuna yığ',
  source:'📋 Çetele → 🐶 Köpek: 6 · 🐱 Kedi: 4 · 🐰 Tavşan: 2',
  tip:'Sıklık tablosundaki her sayı kadar blok koy.',
  categories:[
    { id:'kopek', label:'Köpek', emoji:'🐶', target:6, shape:'yildiz' },
    { id:'kedi',  label:'Kedi',  emoji:'🐱', target:4, shape:'daire' },
    { id:'tavsan',label:'Tavşan',emoji:'🐰', target:2, shape:'ucgen' } ]
};

const CFG = KOPRU ? KOPRU.cfg : VARSAYILAN;

/* Katalogda şekil adı serbest metin; şablonun bildiği üç şekle
   eşliyoruz, tanımadığı gelirse sırayla dağıtıyoruz. */
const SEKILLER = ['yildiz','daire','ucgen'];
const PALET    = [0xe08a3c, 0x8c6fd0, 0x4fb286, 0x4a7fd6, 0xd9534f];

const KATEGORILER = (CFG.categories || []).map((c, i) => ({
  id:     String(c.id),
  ad:     tekSatir(c.label),
  emoji:  c.emoji || '🔹',
  hedef:  Number(c.target) || 0,
  sekil:  SEKILLER.indexOf(String(c.shape)) >= 0 ? String(c.shape) : SEKILLER[i % 3],
  renk:   PALET[i % PALET.length]
}));

const OYUN_ADI = KOPRU ? tekSatir(KOPRU.oyun.title) : 'VERİ LABORATUVARI';
const OYUN_EMO = KOPRU ? (KOPRU.oyun.emo || '🔬') : '🔬';
const TALIMAT  = tekSatir(CFG.instruction) || 'Blokları doğru sütuna yığ';
const KAYNAK   = tekSatir(CFG.source);
const IPUCU    = tekSatir(CFG.tip);
const BASARI   = tekSatir(CFG.successMsg) || 'Grafiği doğru kurdun!';

const CAN_SAYISI = 3;

/* --- Yerleşim -------------------------------------------------------- */
/* Blok, sütuna YAN YANA iki tane sığmayacak kadar geniş olmalı;
   sığarsa çubuk grafik istiflenmiyor, bloklar yan yana diziliyor. */
const BLOK_EN   = 72;
const SUTUN_EN  = 88;
const TABAN_Y   = 524;   /* sütunların tabanı */
/* KUSUR: AZAMI 6 SABİTTİ ama w48 ve g44 oyunlarında bir sütun 7 blok
   istiyor; 7. blok çizilen sütun oyuğunun ÜSTÜNE taşıyordu. Kapasite
   verideki en büyük hedeften hesaplanıyor, blok boyu da ona göre
   küçülüyor (kaynak metni y=156'da; tavan 200'ün altına inmemeli). */
const AZAMI     = Math.max(4, KATEGORILER.reduce((a, k) => Math.max(a, k.hedef), 0));
const BLOK_BOY  = Math.max(26, Math.min(40, Math.floor((TABAN_Y - 212) / AZAMI)));
/* Depo kutusu, sütun etiketlerinin (TABAN_Y+50) altında kalmalı. */
const DEPO_UST  = 616;
const DEPO_ALT  = 730;

/* =====================================================================
   1) BOOT — dokuları üret
   ===================================================================== */
class BootScene extends Phaser.Scene {
  constructor(){ super('Boot'); }

  create(){
    this.dokuKivilcim();
    this.dokuToz();
    KATEGORILER.forEach(k => this.dokuBlok(k));
    /* Uygulama içinde çocuk oyunu listeden zaten seçti; menüyü atla. */
    this.scene.start(KOPRU ? 'Game' : 'Menu');
  }

  dokuKivilcim(){
    const g = this.make.graphics({ add:false });
    g.fillStyle(0xffffff, 1);
    g.fillCircle(8, 8, 8);
    g.generateTexture('kivilcim', 16, 16);
    g.destroy();
  }

  dokuToz(){
    const g = this.make.graphics({ add:false });
    for (let r = 14; r > 0; r--){
      g.fillStyle(0xffffff, 0.06);
      g.fillCircle(14, 14, r);
    }
    g.generateTexture('toz', 28, 28);
    g.destroy();
  }

  /* Kategori bloğu — üstünde kendi şekli */
  dokuBlok(k){
    const W = BLOK_EN, H = BLOK_BOY;
    const g = this.make.graphics({ add:false });

    g.fillStyle(k.renk, 1);
    g.fillRoundedRect(0, 0, W, H, 8);
    g.fillStyle(0xffffff, 0.18);
    g.fillRoundedRect(0, 0, W, 12, { tl:8, tr:8, bl:0, br:0 });
    g.lineStyle(2, 0x00000022, 1);
    g.strokeRoundedRect(0, 0, W, H, 8);

    const cx = W / 2, cy = H / 2 + 1, r = 11;
    g.fillStyle(0xffffff, 0.95);

    if (k.sekil === 'daire'){
      g.fillCircle(cx, cy, r);
    } else if (k.sekil === 'ucgen'){
      g.beginPath();
      g.moveTo(cx, cy - r);
      g.lineTo(cx + r, cy + r * 0.8);
      g.lineTo(cx - r, cy + r * 0.8);
      g.closePath(); g.fillPath();
    } else {                               /* yıldız */
      g.beginPath();
      for (let i = 0; i < 10; i++){
        const a = Phaser.Math.DegToRad(-90 + i * 36);
        const yr = i % 2 === 0 ? r : r * 0.45;
        const x = cx + Math.cos(a) * yr, y = cy + Math.sin(a) * yr;
        if (i === 0) g.moveTo(x, y); else g.lineTo(x, y);
      }
      g.closePath(); g.fillPath();
    }

    g.generateTexture('blok_' + k.id, W, H);
    g.destroy();
  }
}

/* =====================================================================
   Ortak yardımcılar
   ===================================================================== */
function laboratuvarCiz(sc){
  const g = sc.add.graphics();
  g.fillGradientStyle(RENK.zeminUst, RENK.zeminUst, RENK.zeminAlt, RENK.zeminAlt, 1);
  g.fillRect(0, 0, EN, BOY);

  for (let i = 0; i < 20; i++){
    const s = sc.add.circle(
      Phaser.Math.Between(6, EN - 6),
      Phaser.Math.Between(6, BOY - 6),
      Phaser.Math.FloatBetween(1.5, 3.4),
      0xffffff,
      Phaser.Math.FloatBetween(0.03, 0.11)
    );
    sc.tweens.add({
      targets:s, alpha:0.015,
      duration:Phaser.Math.Between(1500, 3200),
      yoyo:true, repeat:-1, delay:Phaser.Math.Between(0, 2000)
    });
  }
  return g;
}

function dugmeYap(sc, x, y, metin, renk, geriCagri){
  const c = sc.add.container(x, y);
  const g = sc.add.graphics();
  g.fillStyle(renk, 1);
  g.fillRoundedRect(-140, -30, 280, 60, 30);
  g.fillStyle(0xffffff, 0.16);
  g.fillRoundedRect(-140, -30, 280, 24, { tl:30, tr:30, bl:0, br:0 });
  const t = sc.add.text(0, 0, metin, {
    fontFamily:'system-ui, sans-serif', fontSize:'25px',
    fontStyle:'bold', color:'#ffffff'
  }).setOrigin(0.5);
  c.add([g, t]);
  c.setSize(280, 60).setInteractive({ useHandCursor:true });
  c.on('pointerover', () => sc.tweens.add({ targets:c, scale:1.05, duration:110 }));
  c.on('pointerout',  () => sc.tweens.add({ targets:c, scale:1.00, duration:110 }));
  /* KUSUR: geri çağrı basma TWEEN'inin sonunda çalışıyordu (≈180ms).
     Tuş takımında aynı tuşa üst üste basıldığında bir basış yutuluyordu
     (sınamada "500000" yerine "50000" yazıldı) ve her dokunuş 180ms
     gecikmeyle işliyordu. Artık işlem HEMEN yapılıyor, tween yalnız
     görsel geri bildirim. */
  c.on('pointerdown', () => {
    sc.tweens.add({ targets:c, scale:0.93, duration:90, yoyo:true });
    if (geriCagri) geriCagri();
  });
  return c;
}

/* =====================================================================
   2) MENU
   ===================================================================== */
class MenuScene extends Phaser.Scene {
  constructor(){ super('Menu'); }

  create(){
    laboratuvarCiz(this);

    /* küçük örnek grafik */
    KATEGORILER.forEach((k, i) => {
      const x = EN / 2 - 80 + i * 80;
      for (let n = 0; n < Math.min(k.hedef, 4); n++){
        const b = this.add.image(x, 250 - n * 30, 'blok_' + k.id).setScale(0.62);
        this.tweens.add({
          targets:b, y:b.y - 5, duration:900 + n * 90,
          yoyo:true, repeat:-1, ease:'Sine.easeInOut'
        });
      }
    });

    const baslik = this.add.text(EN / 2, 350, OYUN_ADI, {
      fontFamily:'system-ui, sans-serif', fontSize:'40px', fontStyle:'bold',
      color:'#ffffff', align:'center', lineSpacing:5
    }).setOrigin(0.5);
    this.tweens.add({
      targets:baslik, scale:1.04, duration:1400,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });

    this.add.text(EN / 2, 432, TALIMAT, {
      fontFamily:'system-ui, sans-serif', fontSize:'22px',
      color:'#cfe6f5', align:'center'
    }).setOrigin(0.5);

    const kart = this.add.graphics();
    kart.fillStyle(0x0d1720, 0.92);
    kart.fillRoundedRect(30, 468, EN - 60, 84, 16);
    kart.lineStyle(2, 0x39657c, 1);
    kart.strokeRoundedRect(30, 468, EN - 60, 84, 16);
    this.add.text(EN / 2, 510, IPUCU, {
      fontFamily:'system-ui, sans-serif', fontSize:'17px', fontStyle:'bold',
      color:'#ffd166', align:'center', wordWrap:{ width:EN - 90 }, lineSpacing:4
    }).setOrigin(0.5);

    dugmeYap(this, EN / 2, 620, '▶  BAŞLA', RENK.dogru, () => this.scene.start('Game'));

    const toplam = KATEGORILER.reduce((a, k) => a + k.hedef, 0);
    this.add.text(EN / 2, 716, `${toplam} blok  ·  ${CAN_SAYISI} can`, {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', color:'#9fc2d6'
    }).setOrigin(0.5);
  }
}

/* =====================================================================
   3) GAME
   ===================================================================== */
class GameScene extends Phaser.Scene {
  constructor(){ super('Game'); }

  create(){
    this.can   = CAN_SAYISI;
    this.puan  = 0;
    this.seri  = 0;
    this.kilit = true;
    this.suruklenen = null;

    /* Phaser sahne örneğini yeniden kullanır — TEKRAR OYNA'da eski
       nesnelere işaret etmesinler. */
    this.bloklar    = null;
    this.mesaj      = null;
    this.engeller   = null;   /* `||` deseniyle eski yok edilmiş gruba
                                 tutunuyordu — TEKRAR OYNA çöküyordu */
    this.vurguCizim = null;

    laboratuvarCiz(this);

    this.kivilcimlar = this.add.particles(0, 0, 'kivilcim', {
      speed:{ min:130, max:350 }, angle:{ min:0, max:360 },
      scale:{ start:0.85, end:0 }, alpha:{ start:1, end:0 },
      lifespan:620, gravityY:340, blendMode:'ADD', emitting:false
    }).setDepth(90);

    this.tozlar = this.add.particles(0, 0, 'toz', {
      speed:{ min:40, max:150 }, angle:{ min:200, max:340 },
      scale:{ start:1, end:2.2 }, alpha:{ start:0.5, end:0 },
      lifespan:680, emitting:false
    }).setDepth(80);

    this.sahneKur();
    this.arayuzKur();
    this.surukleKur();
    this.bloklariDok();

    this.time.delayedCall(1400, () => { this.kilit = false; });
  }

  sutunX(i){
    const n = KATEGORILER.length;
    return EN * (i + 0.5) / n;
  }

  /* ---------- sütunlar ve depo ---------- */
  sahneKur(){
    const g = this.add.graphics().setDepth(4);
    const tavan = TABAN_Y - AZAMI * BLOK_BOY - 12;

    this.engeller = this.physics.add.staticGroup();
    this.sayacYazi = [];
    this.sutunGorsel = [];

    KATEGORILER.forEach((k, i) => {
      const x = this.sutunX(i);

      /* sütun oyuğu */
      g.fillStyle(RENK.sutun, 0.92);
      g.fillRoundedRect(x - SUTUN_EN / 2, tavan, SUTUN_EN, TABAN_Y - tavan + 8, 10);
      g.lineStyle(2, 0x39657c, 1);
      g.strokeRoundedRect(x - SUTUN_EN / 2, tavan, SUTUN_EN, TABAN_Y - tavan + 8, 10);

      /* Ölçek çizgileri EŞİT: hedef yüksekliği vurgulanınca kaç blok
         gerektiği ızgaradan okunuyordu, çocuk veriye hiç bakmıyordu. */
      for (let n = 1; n <= AZAMI; n++){
        const y = TABAN_Y - n * BLOK_BOY;
        g.lineStyle(1, 0x2f5568, 0.6);
        g.lineBetween(x - SUTUN_EN / 2 + 6, y, x + SUTUN_EN / 2 - 6, y);
      }

      /* etiket */
      this.add.text(x, TABAN_Y + 26, k.emoji, { fontSize:'29px' }).setOrigin(0.5).setDepth(6);
      this.add.text(x, TABAN_Y + 50, k.ad, {
        fontFamily:'system-ui, sans-serif', fontSize:'17px', fontStyle:'bold',
        color:'#cfe6f5'
      }).setOrigin(0.5).setDepth(6);

      /* Etiket yalnız GEÇERLİ sayıyı gösteriyor; "0 / 5" yazınca hedef
         ekranda yazılı oluyordu ve kaynak veriyi okumak gereksizdi. */
      const sy = this.add.text(x, tavan - 16, '0', {
        fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
        color:'#ffd166'
      }).setOrigin(0.5).setDepth(6);
      this.sayacYazi.push(sy);

      /* NOT: Phaser'da collider(grup, TEK nesne) callback'e parametreleri
         ters veriyor; engeller staticGroup içinde. */
      this.engeller.add(this.add.rectangle(x, TABAN_Y + 8, SUTUN_EN - 10, 16, 0, 0));
      /* Yan duvarlar tavanın üstüne taşar: blok yığının üstünde
         doğduğunda hâlâ iki duvar arasında kalsın. */
      const duvarBoy = TABAN_Y - tavan + 160;
      this.engeller.add(this.add.rectangle(x - SUTUN_EN / 2 - 2, TABAN_Y - duvarBoy / 2 + 8,
                                           10, duvarBoy, 0, 0));
      this.engeller.add(this.add.rectangle(x + SUTUN_EN / 2 + 2, TABAN_Y - duvarBoy / 2 + 8,
                                           10, duvarBoy, 0, 0));
    });

    /* depo */
    const d = this.add.graphics().setDepth(4);
    d.fillStyle(0x0d1720, 0.9);
    d.fillRoundedRect(20, DEPO_UST - 26, EN - 40, DEPO_ALT - DEPO_UST + 46, 14);
    d.lineStyle(2, 0x39657c, 1);
    d.strokeRoundedRect(20, DEPO_UST - 26, EN - 40, DEPO_ALT - DEPO_UST + 46, 14);
    this.add.text(EN / 2, DEPO_UST - 12, 'BLOK DEPOSU', {
      fontFamily:'system-ui, sans-serif', fontSize:'14px', fontStyle:'bold',
      color:'#7fa8bd'
    }).setOrigin(0.5).setDepth(5);

    this.engeller.add(this.add.rectangle(EN / 2, DEPO_ALT + 8, EN - 56, 16, 0, 0));
    this.engeller.add(this.add.rectangle(26,      BOY / 2, 14, BOY * 2, 0, 0));
    this.engeller.add(this.add.rectangle(EN - 26, BOY / 2, 14, BOY * 2, 0, 0));

    this.bloklar = this.physics.add.group();
    this.physics.add.collider(this.bloklar, this.engeller);
    this.physics.add.collider(this.bloklar, this.bloklar);

    /* sütun doluluk sayaçları */
    this.sayac = KATEGORILER.map(() => 0);
  }

  /* ---------- blokları depoya dök ---------- */
  bloklariDok(){
    /* Stok FAZLALI: her kategoriden hedef+2 blok. Tam sayıda blok
       verilince kaç blok gerektiği stoktan sayılabiliyordu; çocuk
       kaynak veriyi okumak yerine eldeki blokları bitiriyordu. */
    const liste = [];
    KATEGORILER.forEach((k, i) => {
      for (let n = 0; n < k.hedef + 2; n++) liste.push(i);
    });
    Phaser.Utils.Array.Shuffle(liste);

    /* Nesil kontrolü: sahne yeniden başlatılırsa önceki dökümün
       bekleyen çağrıları YOK EDİLMİŞ gruba blok eklemeye çalışıyordu. */
    const nesil = this.nesil = (this.nesil || 0) + 1;
    liste.forEach((ki, n) => {
      const x = 56 + (n % 8) * ((EN - 112) / 7);
      this.time.delayedCall(n * 60, () => {
        if (this.nesil !== nesil) return;
        this.blokYap(ki, x);
      });
    });
  }

  blokYap(ki, x){
    if (!this.bloklar || !this.bloklar.children) return;   /* sahne kapanmış */
    const k = KATEGORILER[ki];
    const b = this.physics.add.image(
      Phaser.Math.Clamp(x, 52, EN - 52), DEPO_UST - 40, 'blok_' + k.id
    ).setDepth(24);

    this.bloklar.add(b);
    b.body.setSize(BLOK_EN, BLOK_BOY);
    b.body.setBounce(0.22, 0.22);
    b.body.setDragX(140);

    b.setData('kat', ki);
    b.setData('yerlesti', false);

    b.setInteractive({ useHandCursor:true });
    this.input.setDraggable(b);
    return b;
  }

  /* ---------- sürükleme ---------- */
  surukleKur(){
    this.input.on('dragstart', (p, b) => {
      if (this.kilit || b.getData('yerlesti')) return;
      this.suruklenen = b;
      b.setDepth(70);
      b.body.setAllowGravity(false);
      b.body.setVelocity(0, 0);
      this.tweens.add({ targets:b, scale:1.16, duration:120, ease:'Back.easeOut' });
      this.sutunlariVurgula(true);
    });

    this.input.on('drag', (p, b, x, y) => {
      if (this.kilit || b.getData('yerlesti')) return;
      b.x = Phaser.Math.Clamp(x, 40, EN - 40);
      b.y = Phaser.Math.Clamp(y, 190, BOY - 40);
    });

    this.input.on('dragend', (p, b) => {
      if (this.kilit || b.getData('yerlesti')) return;
      this.suruklenen = null;
      this.sutunlariVurgula(false);
      this.tweens.add({ targets:b, scale:1, duration:120 });

      const si = this.hangiSutun(b);
      if (si < 0){
        /* depoya geri düşsün */
        b.body.setAllowGravity(true);
        b.body.setVelocity(Phaser.Math.Between(-40, 40), 40);
        return;
      }
      this.sutunaBirak(b, si);
    });
  }

  hangiSutun(b){
    if (b.y > TABAN_Y + 10) return -1;         /* grafik alanının altında */
    for (let i = 0; i < KATEGORILER.length; i++){
      const x = this.sutunX(i);
      if (Math.abs(b.x - x) < SUTUN_EN / 2) return i;
    }
    return -1;
  }

  sutunlariVurgula(acik){
    if (!this.vurguCizim) this.vurguCizim = this.add.graphics().setDepth(5);
    this.vurguCizim.clear();
    if (!acik) return;
    const tavan = TABAN_Y - AZAMI * BLOK_BOY - 12;
    KATEGORILER.forEach((k, i) => {
      /* Eskiden yalnız EKSİK sütunlar parlıyordu: hangi sütuna blok
         gerektiğini söylüyordu. Artık hepsi bırakma hedefi olarak parlar. */
      const x = this.sutunX(i);
      this.vurguCizim.lineStyle(3, RENK.vurgu, 0.85);
      this.vurguCizim.strokeRoundedRect(x - SUTUN_EN / 2, tavan, SUTUN_EN,
                                        TABAN_Y - tavan + 8, 10);
    });
  }

  sutunaBirak(b, si){
    const k = KATEGORILER[si];
    const dogruKat = b.getData('kat') === si;

    if (dogruKat && this.sayac[si] < k.hedef){
      /* GERÇEK FİZİK: blok sütuna düşüp yığının üstüne oturur */
      b.setData('yerlesti', true);
      b.disableInteractive();
      b.setDepth(22);
      /* Blok, yığının ÜSTÜNDEKİ boş yere bırakılır ve kısa mesafe düşer.
         Rastgele yükseklikten bırakılınca bloklar birbirinin içine girip
         sıkışıyor ve istif bozuluyordu. */
      const oturY = TABAN_Y - this.sayac[si] * BLOK_BOY - BLOK_BOY / 2;
      b.setData('oturY', oturY);
      b.setData('sutunIdx', si);
      b.body.setAllowGravity(true);
      b.body.reset(this.sutunX(si), oturY - 70);
      b.body.setVelocity(0, 60);

      this.sayac[si]++;
      this.sayacTazele(si);
      this.kivilcimlar.setParticleTint(k.renk);
      this.kivilcimlar.explode(10, b.x, b.y);

      this.seri++;
      const kazanc = 60 + (this.seri - 1) * 10;
      this.puan += kazanc;
      this.puanYazi.setText('Puan ' + this.puan);
      this.tweens.add({
        targets:this.puanYazi, scale:1.35, duration:120, yoyo:true, ease:'Back.easeOut'
      });

      if (this.sayac[si] === k.hedef){
        this.mesajGoster(k.ad + ' sütunu tamam: ' + k.hedef + ' blok ✓', '#1f6d4a');
        this.tweens.add({
          targets:this.sayacYazi[si], scale:1.4, duration:160, yoyo:true, ease:'Back.easeOut'
        });
      }
      this.bittiMi();
      return;
    }

    /* GERÇEK FİZİK: yanlış sütun bloğu geri tükürür */
    b.body.setAllowGravity(true);
    b.body.setVelocityY(-300);
    b.body.setVelocityX(Phaser.Math.Between(-160, 160));
    this.tozlar.explode(12, b.x, b.y);
    this.cameras.main.shake(210, 0.011);
    this.cameras.main.flash(160, 220, 90, 90);

    if (!dogruKat){
      this.seri = 0;
      this.can--;
      this.arayuzuTazele();
      this.tweens.add({
        targets:this.canYazi, angle:{ from:-12, to:12 },
        duration:70, yoyo:true, repeat:3,
        onComplete:() => this.canYazi.setAngle(0)
      });
      this.mesajGoster('Bu blok ' + KATEGORILER[b.getData('kat')].ad +
                       ' sütununa ait.', '#b5453b');
      if (this.can <= 0){
        this.kilit = true;
        this.time.delayedCall(900, () => this.bitir(false));
      }
    } else {
      /* doğru kategori ama sütun dolu — ceza yok, uyarı yeter */
      this.mesajGoster('Verilere yeniden bak: ' + k.ad +
                       ' sütununda gereken kadar blok var.', '#3d6285');
    }
  }

  sayacTazele(i){
    this.sayacYazi[i].setText(this.sayac[i] + ' / ' + KATEGORILER[i].hedef);
    this.sayacYazi[i].setColor(this.sayac[i] === KATEGORILER[i].hedef ? '#7ce0a3' : '#ffd166');
  }

  bittiMi(){
    const tamam = KATEGORILER.every((k, i) => this.sayac[i] === k.hedef);
    if (!tamam) return;
    this.kilit = true;
    this.puan += 200;
    this.puanYazi.setText('Puan ' + this.puan);
    this.kivilcimlar.setParticleTint(RENK.vurgu);
    this.kivilcimlar.explode(30, EN / 2, TABAN_Y - 120);
    this.cameras.main.flash(160, 80, 210, 140);
    this.mesajGoster('Grafik tamam! 📊', '#1f6d4a');
    this.time.delayedCall(1600, () => this.bitir(true));
  }

  mesajGoster(metin, arka){
    if (this.mesaj) this.mesaj.destroy();
    this.mesaj = this.add.text(EN / 2, 560, metin, {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#ffffff', backgroundColor:arka,
      padding:{ x:12, y:7 }, align:'center', wordWrap:{ width:EN - 60 }
    }).setOrigin(0.5).setDepth(96).setAlpha(0);
    const t = this.mesaj;
    this.tweens.add({ targets:t, alpha:1, duration:150 });
    this.time.delayedCall(1500, () => {
      if (!t.active) return;
      this.tweens.add({
        targets:t, alpha:0, duration:250,
        onComplete:() => { if (this.mesaj === t) this.mesaj = null; t.destroy(); }
      });
    });
  }

  /* ---------- arayüz ---------- */
  arayuzKur(){
    /* Katalogda yönerge 120 karaktere çıkıyor; sabit yükseklikli şerit
       yazıyı iki yandan kesiyordu. Şerit metnin gerçek boyuna göre. */
    const yon = this.add.text(EN / 2, 22, OYUN_EMO + '  ' + TALIMAT, {
      fontFamily:'system-ui, sans-serif',
      fontSize: (TALIMAT.length > 92 ? '16px' : (TALIMAT.length > 54 ? '17px' : '20px')),
      fontStyle:'bold', color:'#ffffff', align:'center',
      wordWrap:{ width:EN - 52 }, lineSpacing:3
    }).setOrigin(0.5, 0).setDepth(61);

    const seritBoy = Math.max(104, yon.height + 62);
    const serit = this.add.graphics().setDepth(60);
    serit.fillStyle(0x0c141c, 0.97);
    serit.fillRoundedRect(10, 10, EN - 20, seritBoy, 18);
    yon.setDepth(61);
    const satirY = 10 + seritBoy - 22;
    this.seritAlt = 10 + seritBoy;

    this.puanYazi = this.add.text(30, satirY, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0, 0.5).setDepth(61);

    this.canYazi = this.add.text(EN - 30, satirY, '', { fontSize:'20px' })
      .setOrigin(1, 0.5).setDepth(61);

    this.ilerlemeYazi = this.add.text(EN / 2, satirY, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#9fc2d6'
    }).setOrigin(0.5).setDepth(61);

    /* çetele kaynağı — kutu YÜKSEKLİĞİ SABİTTİ (56px); w48 gibi uzun
       kaynak metinleri (3 satıra sarılan "1 kitap: 5 · 2 kitap: 7 · 3
       kitap: 4 · 4+ kitap: 2") kutudan taşıp altındaki sütun sayaçlarının
       üstüne biniyordu. Kutu artık metnin gerçek yüksekliğine göre. */
    const kYazi = this.add.text(0, 0, KAYNAK, {
      fontFamily:'system-ui, sans-serif', fontSize:'17px', fontStyle:'bold',
      wordWrap:{ width:EN - 60 }, lineSpacing:3
    }).setVisible(false);
    const kYukseklik = Math.max(56, kYazi.height + 24);
    kYazi.destroy();

    const kUst = this.seritAlt + 6;
    const k = this.add.graphics().setDepth(6);
    k.fillStyle(0x0d1720, 0.92);
    k.fillRoundedRect(20, kUst, EN - 40, kYukseklik, 12);
    k.lineStyle(2, 0x39657c, 1);
    k.strokeRoundedRect(20, kUst, EN - 40, kYukseklik, 12);
    this.add.text(EN / 2, kUst + kYukseklik / 2, KAYNAK, {
      fontFamily:'system-ui, sans-serif', fontSize:'17px', fontStyle:'bold',
      color:'#cfe6f5', align:'center', wordWrap:{ width:EN - 60 }, lineSpacing:3
    }).setOrigin(0.5).setDepth(7);
    this.kaynakAlt = kUst + kYukseklik;

    this.arayuzuTazele();
  }

  arayuzuTazele(){
    this.canYazi.setText(
      '❤️'.repeat(Math.max(0, this.can)) +
      '🖤'.repeat(Math.max(0, CAN_SAYISI - this.can))
    );
    const toplam = KATEGORILER.reduce((a, k) => a + k.hedef, 0);
    const kondu = this.sayac ? this.sayac.reduce((a, v) => a + v, 0) : 0;
    this.ilerlemeYazi.setText(`${kondu} / ${toplam} blok`);
  }

  bitir(kazandi){
    /* Uygulama içindeyken kazanma ekranını uygulama gösteriyor. */
    if (kazandi && KOPRU){ KOPRU.bitir(BASARI, this.puan); return; }
    const toplam = KATEGORILER.reduce((a, k) => a + k.hedef, 0);
    const kondu = this.sayac.reduce((a, v) => a + v, 0);
    this.scene.start('GameOver', {
      kazandi, puan:this.puan, can:this.can, kondu, toplam
    });
  }

  /* ---------- her kare ---------- */
  update(){
    if (!this.bloklar || !this.bloklar.children) return;
    this.arayuzuTazele();

    /* Yuvasına inen blok oraya KİLİTLENİR. Serbest fizikle bırakılınca
       bloklar birbirinin içine girip istif bozuluyordu. */
    this.bloklar.getChildren().forEach(b => {
      if (!b.active || !b.getData('yerlesti') || b.getData('kilitli')) return;
      const oy = b.getData('oturY');
      if (b.y >= oy - 1){
        b.setData('kilitli', true);
        b.body.reset(this.sutunX(b.getData('sutunIdx')), oy);
        b.body.setVelocity(0, 0);
        b.body.setAllowGravity(false);
        b.body.setImmovable(true);
        this.tozlar.explode(4, b.x, b.y + BLOK_BOY / 2);
      }
    });

    /* alandan kaçan bloğu depoya geri getir */
    this.bloklar.getChildren().forEach(b => {
      if (!b.active || b.getData('yerlesti') || this.suruklenen === b) return;
      if (b.y > BOY + 60 || b.x < -60 || b.x > EN + 60){
        b.body.reset(Phaser.Math.Between(70, EN - 70), DEPO_UST - 30);
        b.body.setVelocity(0, 0);
      }
    });
  }
}

/* =====================================================================
   4) GAME OVER
   ===================================================================== */
class GameOverScene extends Phaser.Scene {
  constructor(){ super('GameOver'); }

  init(veri){ this.veri = veri; }

  create(){
    const { kazandi, puan, can, kondu, toplam } = this.veri;
    laboratuvarCiz(this);

    const emo = this.add.text(EN / 2, 190, kazandi ? '🔬' : '💪', { fontSize:'97px' })
      .setOrigin(0.5).setScale(0);
    this.tweens.add({ targets:emo, scale:1, duration:520, ease:'Back.easeOut' });

    this.add.text(EN / 2, 300, kazandi ? 'GRAFİK HAZIR!' : 'TEKRAR DENE', {
      fontFamily:'system-ui, sans-serif', fontSize:'35px', fontStyle:'bold',
      color: kazandi ? '#7ce0a3' : '#ffd166', align:'center'
    }).setOrigin(0.5);

    this.add.text(EN / 2, 360,
      kazandi ? BASARI : `${kondu} / ${toplam} blok yerleştirdin — bir daha deneyelim mi?`, {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#cfe6f5',
      align:'center', wordWrap:{ width:EN - 70 }, lineSpacing:5
    }).setOrigin(0.5);

    const puanYazi = this.add.text(EN / 2, 456, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'42px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0.5);
    const sayac = { v:0 };
    this.tweens.add({
      targets:sayac, v:puan, duration:900, ease:'Cubic.easeOut',
      onUpdate:() => puanYazi.setText('Puan ' + Math.round(sayac.v))
    });

    this.add.text(EN / 2, 506,
      'Kalan can: ' + (can > 0 ? '❤️'.repeat(can) : '—'), {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#9fc2d6'
    }).setOrigin(0.5);

    if (kazandi){
      const konfeti = this.add.particles(EN / 2, -20, 'kivilcim', {
        speed:{ min:90, max:260 }, angle:{ min:60, max:120 },
        scale:{ start:0.8, end:0 }, alpha:{ start:1, end:0 },
        lifespan:2000, gravityY:180, quantity:2, frequency:70,
        tint:[0xffd166, 0x7ce0a3, 0x8c6fd0, 0xe08a3c]
      }).setDepth(5);
      this.time.delayedCall(2600, () => konfeti.stop());
    }

    dugmeYap(this, EN / 2, 606, '↻  TEKRAR OYNA', RENK.dogru, () => this.scene.start('Game'));

    /* Uygulama içinde: bu oyunda takılan çocuk sıradakine geçebilsin. */

    if (KOPRU) dugmeYap(this, EN / 2, 680, '⏭  SIRADAKİ OYUN', 0x4a679e, () => KOPRU.atla());
    if (!KOPRU) dugmeYap(this, EN / 2, 684, '☰  MENÜ',        0x39657c, () => this.scene.start('Menu'));
  }
}

/* =====================================================================
   OYUNU BAŞLAT
   ===================================================================== */
/* =====================================================================
   NETLİK — cihazın piksel yoğunluğunda çizim
   ---------------------------------------------------------------------
   Oyun 480x800 mantıksal tuvalde çiziliyordu; telefon bunu 1080 piksele
   büyütünce yazılar ve kenarlar bulanıklaşıyordu. Çözüm: tuvali cihazın
   gerçek piksel sayısında açmak, dünyayı ise kamerayı NETLIK katına
   yakınlaştırarak yine 480x800 koordinatta tutmak. Böylece Graphics ile
   çizilen her şey (kartlar, şeritler, kutular) vektör keskinliğinde,
   yazılar da NETLIK çözünürlüğünde üretiliyor; oyun kodunun tek satırı
   değişmiyor.
   ===================================================================== */
const NETLIK = Math.min(3, Math.max(1, Math.round((window.devicePixelRatio || 1) * 2) / 2));

/* Phaser yazıyı kendi ara tuvaline çiziyor; çözünürlük verilmezse 1x
   üretilip yakınlaştırmada bulanıklaşır. Bütün yazılara varsayılan
   olarak NETLIK veriyoruz. */
(function(){
  const TS = Phaser.GameObjects.TextStyle.prototype;
  const eskiSetStyle = TS.setStyle;
  TS.setStyle = function(style, updateText, setDefaults){
    if (style && style.resolution === undefined) style.resolution = NETLIK;
    return eskiSetStyle.call(this, style, updateText, setDefaults);
  };
})();

/* Tuval NETLIK katına büyüdüğü için Phaser imleç konumunu da o ölçekte
   veriyor (0–960). Oyun koordinatına (0–480) çeviren yardımcı: sürükleme
   olayları zaten dünya koordinatı verdiği için yalnız pointer olaylarında
   kullanılıyor. */
function imlec(p){ return { x: p.x / NETLIK, y: p.y / NETLIK }; }

/* Her sahne başlarken kamerayı NETLIK katına yakınlaştırıp fizik
   dünyasını mantıksal ölçüde tutuyoruz: tuval büyüdü, dünya büyümedi.
   Sahne örnekleri oyun kurulumundan sonra eşzamansız oluştuğu için
   kanca Systems.start üzerine takılıyor — yeniden başlatmalarda da
   kendiliğinden çalışıyor. */
(function(){
  const SS = Phaser.Scenes.Systems.prototype;
  const eskiStart = SS.start;
  SS.start = function(veri){
    const sonuc = eskiStart.call(this, veri);
    const sc = this.scene;
    try{
      if (sc.cameras && sc.cameras.main){
        sc.cameras.main.setZoom(NETLIK);
        sc.cameras.main.centerOn(EN / 2, BOY / 2);
      }
      if (sc.physics && sc.physics.world) sc.physics.world.setBounds(0, 0, EN, BOY);
    }catch(e){ /* netlik ayarı oyunu engellemesin */ }
    return sonuc;
  };
})();

window.OYUN = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'oyun',
  width: EN * NETLIK,
  height: BOY * NETLIK,
  backgroundColor: '#101a22',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 760 } }
  },
  scene: [BootScene, MenuScene, GameScene, GameOverScene]
});

</script>
</body>
</html>
```

### sirik-phaser.html — jumpPath (10 oyun)
Dosya boyu: 29312 bayt · 795 satır

```html
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<title>Sihirli Fasulye Sırığı — Phaser 3</title>
<script src="https://cdn.jsdelivr.net/npm/phaser@3.80.1/dist/phaser.min.js"></script>
<style>
  html, body { margin:0; padding:0; height:100%; background:#0d1f16; overflow:hidden;
    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
    -webkit-tap-highlight-color: transparent; touch-action:none; }
  #oyun { width:100%; height:100%; display:flex; align-items:center; justify-content:center; }
  canvas { display:block; }
</style>
</head>
<body>
<div id="oyun"></div>
<script>
/* =====================================================================
   SİHİRLİ FASULYE SIRIĞI — Phaser 3    (mekanik: jumpPath · 10 oyun)
   ---------------------------------------------------------------------
   Kazanım: MAT.3.1.4.b — 80 içinde sekizer, 1000 içinde onar ve yüzer
   ileri-geri ritmik sayarken örüntü bulur.

   Sahneler : Boot → Menu → Game → GameOver
   Fizik    : Arcade.
              · Peri, seçilen yaprağa GERÇEK PARABOLİK atışla zıplar:
                çıkış hızı, verilen yerçekimi altında hedefe düşecek
                şekilde hesaplanır (vx = dx/t, vy = (dy - ½gt²)/t).
              · Yanlış yaprak kırılır, peri yerçekimiyle düşer, yere
                çarpıp son doğru yaprağa geri taşınır.
   Görsel   : Bütün dokular Graphics ile çalışma anında üretilir —
              uygulama çevrimdışı kabukta (APK / iOS) çalışacağı için
              dışarıdan resim çekilmiyor.
   ===================================================================== */

const EN = 480, BOY = 800;

const RENK = {
  gokUst  : 0x12331f,
  gokAlt  : 0x2f6b45,
  dogru   : 0x34c47b,
  yanlis  : 0xf07575,
  yaprak  : 0x4fa86a,
  yaprakUst: 0x74c98c,
  sirik   : 0x6b8f3c,
  vurgu   : 0xffd166
};

/* ---------------------------------------------------------------------
   İÇERİK — uygulamadaki w04 oyununun birebir aynısı.
   Başka bir jumpPath oyununa geçmek için yalnızca bu blok değişir.
   Konumlar yüzde: x 0-100 (sol-sağ), y 0-100 (üst-alt).
   ------------------------------------------------------------------- */
/* ---------------- uygulama köprüsü ----------------
   Adres  sirik.html#oyun=w04  biçiminde; katalog verisi üst pencereden
   okunuyor. Kazanınca completeGame() çağrılır.                          */
const KOPRU = (function(){
  try{
    const p = new URLSearchParams(location.hash.slice(1));
    const id = p.get('oyun');
    if (id && window.parent && window.parent !== window &&
        typeof window.parent.getGame === 'function'){
      const g = window.parent.getGame(id);
      if (g && g.cfg) return {
        oyun: g, cfg: g.cfg,
        bitir(mesaj, puan){ try{ window.parent.completeGame(mesaj || '', puan); }catch(e){} },
        /* Turun kendi metnini uygulamanın sesiyle okutur (Piper). */
        oku(metin){ try{ if (window.parent.oku) window.parent.oku(metin); }catch(e){} },
        /* Kaybetme ekranından: bu oyunu bırak, sıradakine geç. */
        atla(){ try{ if (window.parent.sonrakiOyunaGec) window.parent.sonrakiOyunaGec(); }catch(e){} }
      };
    }
  }catch(e){ /* çapraz kaynak engeli: tek başına oynanır */ }
  return null;
})();

/* HTML varlıklarını çöz: katalogda "Pay &lt; payda" gibi yazımlar var,
   çözülmezse ekranda "&lt;" olarak görünüyor ve öyle okunuyor. */
function varlikCoz(m){
  return String(m)
    .replace(/&nbsp;/gi, ' ')
    .replace(/&lt;/gi, '<').replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"').replace(/&#39;|&apos;/gi, "'")
    .replace(/&hellip;/gi, '…').replace(/&mdash;/gi, '—').replace(/&ndash;/gi, '–')
    .replace(/&times;/gi, '×').replace(/&divide;/gi, '÷').replace(/&deg;/gi, '°')
    .replace(/&rarr;/gi, '→').replace(/&larr;/gi, '←')
    .replace(/&amp;/gi, '&');            /* en sona: çift çözmeyi önler */
}

function duzMetin(x){
  return varlikCoz(String(x == null ? '' : x).replace(/<br\s*\/?>/gi,' ')
    .replace(/<[^>]+>/g,'')).replace(/[“”]/g,'"').replace(/\s+/g,' ').trim();
}
function tekSatir(x){ return duzMetin(x).replace(/\n/g,' '); }

const VARSAYILAN = {
  instruction:'Sekizer sayarak sıradaki yaprağa zıpla',
  heroEmoji:'🧚',
  start:{ x:50, y:93 },
  nodes:[ {id:'n8',label:'8',x:26,y:80}, {id:'n14',label:'14',x:73,y:80},
          {id:'n16',label:'16',x:70,y:64}, {id:'n20',label:'20',x:24,y:64} ],
  steps:[ { prompt:'0’dan başlıyoruz — sekizer say!', target:'n8',
            okMsg:'Sekiz! 🌱', wrongHint:'0 + 8 = 8.' },
          { prompt:'8’den sonra 8 daha ekle.', target:'n16',
            okMsg:'On altı! 🌿', wrongHint:'8 + 8 = 16.' } ]
};

const CFG = KOPRU ? KOPRU.cfg : VARSAYILAN;

const PERI      = CFG.heroEmoji || '🧚';
const BASLANGIC = { x:Number((CFG.start||{}).x) || 50, y:Number((CFG.start||{}).y) || 93 };

const YAPRAKLAR = (CFG.nodes || []).map(n => ({
  id:String(n.id), etiket:tekSatir(n.label), x:Number(n.x), y:Number(n.y)
}));

const ADIMLAR = (CFG.steps || []).map(a => ({
  soru:  duzMetin(a.prompt),
  hedef: String(a.target),
  tamam: tekSatir(a.okMsg) || 'Doğru! 🌱',
  ipucu: tekSatir(a.wrongHint) || tekSatir(a.hint)
}));

const OYUN_ADI = KOPRU ? tekSatir(KOPRU.oyun.title) : 'SİHİRLİ FASULYE SIRIĞI';
const OYUN_EMO = KOPRU ? (KOPRU.oyun.emo || '🌱') : '🌱';
const TALIMAT  = tekSatir(CFG.instruction) || 'Sıradaki yaprağa zıpla';
const IPUCU    = tekSatir(CFG.tip);
const BASARI   = tekSatir(CFG.successMsg) || 'Buluta ulaştın!';

const CAN_SAYISI = 3;

/* --- Yerleşim --------------------------------------------------------
   Yüzde koordinatlar bu dikey banda eşlenir (HUD'un altı ↔ zemin). */
const ALAN_UST = 196;
const ALAN_ALT = 716;
const UCUS_SURE = 0.62;   /* zıplayışın havada kalma süresi (sn) */

/* =====================================================================
   1) BOOT — dokuları üret
   ===================================================================== */
class BootScene extends Phaser.Scene {
  constructor(){ super('Boot'); }

  create(){
    this.dokuKivilcim();
    this.dokuToz();
    this.dokuYaprak();
    /* Uygulama içinde çocuk oyunu listeden zaten seçti; menüyü atla. */
    this.scene.start(KOPRU ? 'Game' : 'Menu');
  }

  dokuKivilcim(){
    const g = this.make.graphics({ add:false });
    g.fillStyle(0xffffff, 1);
    g.fillCircle(8, 8, 8);
    g.generateTexture('kivilcim', 16, 16);
    g.destroy();
  }

  dokuToz(){
    const g = this.make.graphics({ add:false });
    for (let r = 14; r > 0; r--){
      g.fillStyle(0xffffff, 0.06);
      g.fillCircle(14, 14, r);
    }
    g.generateTexture('toz', 28, 28);
    g.destroy();
  }

  /* Yaprak platformu */
  dokuYaprak(){
    const W = 92, H = 44;
    const g = this.make.graphics({ add:false });
    /* yaprak gövdesi */
    g.fillStyle(RENK.yaprak, 1);
    g.fillEllipse(W / 2, H / 2 + 3, W - 6, H - 12);
    g.fillStyle(RENK.yaprakUst, 1);
    g.fillEllipse(W / 2, H / 2 - 1, W - 14, H - 22);
    /* orta damar */
    g.lineStyle(2, 0x2f7a4a, 0.8);
    g.lineBetween(10, H / 2 + 1, W - 10, H / 2 + 1);
    /* yan damarlar */
    for (let i = -2; i <= 2; i++){
      g.lineStyle(1, 0x2f7a4a, 0.5);
      g.lineBetween(W / 2 + i * 15, H / 2 + 1, W / 2 + i * 15 + 6, H / 2 - 7);
      g.lineBetween(W / 2 + i * 15, H / 2 + 1, W / 2 + i * 15 + 6, H / 2 + 9);
    }
    g.generateTexture('yaprak', W, H);
    g.destroy();
  }
}

/* =====================================================================
   Ortak yardımcılar
   ===================================================================== */
function bahceCiz(sc){
  const g = sc.add.graphics();
  g.fillGradientStyle(RENK.gokUst, RENK.gokUst, RENK.gokAlt, RENK.gokAlt, 1);
  g.fillRect(0, 0, EN, BOY);

  /* bulutlar */
  for (let i = 0; i < 4; i++){
    const b = sc.add.graphics();
    b.fillStyle(0xffffff, 0.07);
    b.fillEllipse(Phaser.Math.Between(0, EN), Phaser.Math.Between(140, 320),
                  Phaser.Math.Between(100, 170), Phaser.Math.Between(26, 42));
    sc.tweens.add({
      targets:b, x:'+=' + Phaser.Math.Between(50, 120),
      duration:Phaser.Math.Between(10000, 17000),
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });
  }
  return g;
}

function dugmeYap(sc, x, y, metin, renk, geriCagri){
  const c = sc.add.container(x, y);
  const g = sc.add.graphics();
  g.fillStyle(renk, 1);
  g.fillRoundedRect(-140, -30, 280, 60, 30);
  g.fillStyle(0xffffff, 0.16);
  g.fillRoundedRect(-140, -30, 280, 24, { tl:30, tr:30, bl:0, br:0 });
  const t = sc.add.text(0, 0, metin, {
    fontFamily:'system-ui, sans-serif', fontSize:'25px',
    fontStyle:'bold', color:'#ffffff'
  }).setOrigin(0.5);
  c.add([g, t]);
  c.setSize(280, 60).setInteractive({ useHandCursor:true });
  c.on('pointerover', () => sc.tweens.add({ targets:c, scale:1.05, duration:110 }));
  c.on('pointerout',  () => sc.tweens.add({ targets:c, scale:1.00, duration:110 }));
  /* KUSUR: geri çağrı basma TWEEN'inin sonunda çalışıyordu (≈180ms).
     Tuş takımında aynı tuşa üst üste basıldığında bir basış yutuluyordu
     (sınamada "500000" yerine "50000" yazıldı) ve her dokunuş 180ms
     gecikmeyle işliyordu. Artık işlem HEMEN yapılıyor, tween yalnız
     görsel geri bildirim. */
  c.on('pointerdown', () => {
    sc.tweens.add({ targets:c, scale:0.93, duration:90, yoyo:true });
    if (geriCagri) geriCagri();
  });
  return c;
}

/* =====================================================================
   2) MENU
   ===================================================================== */
class MenuScene extends Phaser.Scene {
  constructor(){ super('Menu'); }

  create(){
    bahceCiz(this);

    const y1 = this.add.image(EN / 2 - 60, 236, 'yaprak').setScale(0.9);
    const y2 = this.add.image(EN / 2 + 66, 190, 'yaprak').setScale(0.9);
    const p = this.add.text(EN / 2 - 60, 206, PERI, { fontSize:'42px' }).setOrigin(0.5);
    this.tweens.add({
      targets:p, x:EN / 2 + 66, y:160, duration:1200,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });
    this.tweens.add({ targets:[y1, y2], angle:4, duration:1600, yoyo:true, repeat:-1 });

    const baslik = this.add.text(EN / 2, 350, OYUN_ADI, {
      fontFamily:'system-ui, sans-serif', fontSize:'38px', fontStyle:'bold',
      color:'#ffffff', align:'center', lineSpacing:5
    }).setOrigin(0.5);
    this.tweens.add({
      targets:baslik, scale:1.04, duration:1400,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });

    this.add.text(EN / 2, 436, TALIMAT, {
      fontFamily:'system-ui, sans-serif', fontSize:'22px',
      color:'#d6f0dd', align:'center', wordWrap:{ width:EN - 60 }
    }).setOrigin(0.5);

    const kart = this.add.graphics();
    kart.fillStyle(0x0a1a12, 0.92);
    kart.fillRoundedRect(30, 472, EN - 60, 74, 16);
    kart.lineStyle(2, 0x3f7a53, 1);
    kart.strokeRoundedRect(30, 472, EN - 60, 74, 16);
    this.add.text(EN / 2, 509, IPUCU, {
      fontFamily:'system-ui, sans-serif', fontSize:'17px', fontStyle:'bold',
      color:'#ffd166', align:'center', wordWrap:{ width:EN - 90 }, lineSpacing:4
    }).setOrigin(0.5);

    dugmeYap(this, EN / 2, 616, '▶  BAŞLA', RENK.dogru, () => this.scene.start('Game'));

    this.add.text(EN / 2, 712, `${ADIMLAR.length} zıplayış  ·  ${CAN_SAYISI} can`, {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', color:'#a5d6b7'
    }).setOrigin(0.5);
  }
}

/* =====================================================================
   3) GAME
   ===================================================================== */
class GameScene extends Phaser.Scene {
  constructor(){ super('Game'); }

  create(){
    this.can   = CAN_SAYISI;
    this.puan  = 0;
    this.seri  = 0;
    this.adim  = 0;
    this.kilit = true;
    this.uctu  = false;

    /* Phaser sahne örneğini yeniden kullanır — TEKRAR OYNA'da eski
       nesnelere işaret etmesinler. */
    this.yaprakNesne = null;
    this.peri        = null;
    this.mesaj       = null;

    bahceCiz(this);

    this.kivilcimlar = this.add.particles(0, 0, 'kivilcim', {
      speed:{ min:120, max:330 }, angle:{ min:0, max:360 },
      scale:{ start:0.8, end:0 }, alpha:{ start:1, end:0 },
      lifespan:600, gravityY:300, blendMode:'ADD', emitting:false
    }).setDepth(90);

    this.tozlar = this.add.particles(0, 0, 'toz', {
      speed:{ min:40, max:140 }, angle:{ min:0, max:360 },
      scale:{ start:0.9, end:2 }, alpha:{ start:0.5, end:0 },
      lifespan:660, emitting:false
    }).setDepth(80);

    this.sahneKur();
    this.arayuzKur();
    this.yapraklariKur();
    this.periKur();
    this.adimiBaslat();
  }

  /* yüzde → ekran koordinatı */
  nokta(xy){
    return {
      x: xy.x * EN / 100,
      y: ALAN_UST + (xy.y - 16) * (ALAN_ALT - ALAN_UST) / (93 - 16)
    };
  }

  /* ---------- sabit sahne ---------- */
  sahneKur(){
    /* fasulye sırığı — yaprakları birbirine bağlayan sarmal gövde */
    const g = this.add.graphics().setDepth(3);
    g.lineStyle(9, RENK.sirik, 0.85);
    const b = this.nokta(BASLANGIC);
    g.beginPath();
    g.moveTo(b.x, b.y);
    YAPRAKLAR.slice().sort((p, q) => q.y - p.y).forEach(y => {
      const n = this.nokta(y);
      g.lineTo(n.x, n.y + 10);
    });
    g.strokePath();

    /* zemin */
    const z = this.add.graphics().setDepth(4);
    z.fillStyle(0x1c4a2c, 1);
    z.fillRoundedRect(-10, ALAN_ALT + 18, EN + 20, 60, 12);
    z.fillStyle(0x2a6b3f, 1);
    z.fillRoundedRect(-10, ALAN_ALT + 18, EN + 20, 14, { tl:12, tr:12, bl:0, br:0 });

    /* NOT: Phaser'da collider(grup, TEK nesne) callback'e parametreleri
       ters veriyor; engel staticGroup içinde. */
    this.zemin = this.physics.add.staticGroup();
    this.zemin.add(this.add.rectangle(EN / 2, ALAN_ALT + 26, EN + 40, 16, 0, 0));
  }

  /* ---------- yapraklar ---------- */
  yapraklariKur(){
    this.yaprakNesne = [];
    YAPRAKLAR.forEach(y => {
      const n = this.nokta(y);
      const c = this.add.container(n.x, n.y).setDepth(12);
      const res = this.add.image(0, 0, 'yaprak');
      const et  = this.add.text(0, -1, y.etiket, {
        fontFamily:'system-ui, sans-serif', fontSize:'24px', fontStyle:'bold',
        color:'#12331f'
      }).setOrigin(0.5);
      c.add([res, et]);
      c.setSize(92, 44);
      c.setData('id', y.id);
      c.setData('kirik', false);
      /* Dokunma alanını Phaser'a bırakıyoruz: Container'a elle
         Rectangle(-W/2,-H/2,…) verilince kaydırma bir kez daha uygulanıyor ve
         alan sola-yukarı kayıyor — nesneyi tutmak için sol üstüne basmak
         gerekiyordu. setSize + argümansız setInteractive() alanı ortalıyor.
         Alan görselden bir miktar geniş: parmak payı. */
      c.setSize(92 + 28, 44 + 28);
      c.setInteractive();
      c.on('pointerdown', () => this.yapragaZipla(c));
      this.tweens.add({
        targets:c, angle:Phaser.Math.Between(-3, 3),
        duration:Phaser.Math.Between(1400, 2200), yoyo:true, repeat:-1,
        ease:'Sine.easeInOut'
      });
      this.yaprakNesne.push(c);
    });
  }

  yapragiBul(id){ return this.yaprakNesne.find(c => c.getData('id') === id); }

  /* ---------- peri ---------- */
  periKur(){
    const b = this.nokta(BASLANGIC);
    this.peri = this.physics.add.existing(
      this.add.text(b.x, b.y - 28, PERI, { fontSize:'42px' }).setOrigin(0.5).setDepth(30)
    );
    this.peri.body.setAllowGravity(false);
    this.peri.body.setSize(34, 34);

    this.izler = this.add.particles(0, 0, 'kivilcim', {
      speed:0, scale:{ start:0.4, end:0 }, alpha:{ start:0.7, end:0 },
      lifespan:340, frequency:40, tint:0xffe9a8, emitting:false
    }).setDepth(29);
    this.izler.startFollow(this.peri);

    this.physics.add.collider(this.peri, this.zemin, this.yereDustu, null, this);
    this.durakId = null;   /* şu an üstünde durduğu yaprak */
  }

  /* ---------- adım ---------- */
  adimiBaslat(){
    const a = ADIMLAR[this.adim];
    this.kilit = true;
    this.soruYazi.setText(a.soru);
    this.tweens.add({
      targets:this.soruYazi, scale:{ from:0.86, to:1 }, duration:280, ease:'Back.easeOut'
    });
    this.time.delayedCall(300, () => { this.kilit = false; });
    this.arayuzuTazele();
  }

  /* ---------- zıplama ---------- */
  yapragaZipla(hedefC){
    if (this.kilit || this.uctu) return;
    if (hedefC.getData('kirik')) return;
    if (hedefC.getData('id') === this.durakId) return;

    this.kilit = true;
    this.uctu  = true;
    this.hedefYaprak = hedefC;

    /* GERÇEK FİZİK: verilen yerçekimi altında hedefe düşecek çıkış hızı
       vx = dx / t ,  vy = (dy - ½ g t²) / t                          */
    const g  = this.physics.world.gravity.y;
    const hx = hedefC.x, hy = hedefC.y - 28;
    const dx = hx - this.peri.x, dy = hy - this.peri.y;
    const t  = UCUS_SURE;

    this.peri.body.setAllowGravity(true);
    this.peri.body.setVelocity(dx / t, (dy - 0.5 * g * t * t) / t);
    this.izler.start();
    this.tozlar.explode(6, this.peri.x, this.peri.y + 16);
    this.tweens.add({ targets:this.peri, angle:dx > 0 ? 14 : -14, duration:200, yoyo:true });
  }

  /* update() içinden: peri hedefe vardı */
  konduHedefe(){
    const c = this.hedefYaprak;
    this.uctu = false;
    this.izler.stop();
    this.peri.body.setAllowGravity(false);
    this.peri.body.setVelocity(0, 0);
    this.peri.body.reset(c.x, c.y - 28);
    this.peri.setAngle(0);

    const a = ADIMLAR[this.adim];
    if (c.getData('id') === a.hedef) this.dogru(c);
    else                             this.yanlis(c);
  }

  dogru(c){
    this.durakId = c.getData('id');
    this.seri++;
    const kazanc = 150 + (this.seri - 1) * 25;
    this.puan += kazanc;
    this.adim++;

    this.kivilcimlar.setParticleTint(RENK.dogru);
    this.kivilcimlar.explode(22, c.x, c.y);
    this.tweens.add({
      targets:c, scaleX:1.14, scaleY:0.86, duration:130, yoyo:true, ease:'Quad.easeOut'
    });
    this.cameras.main.flash(140, 80, 210, 140);

    this.puanYazi.setText('Puan ' + this.puan);
    this.tweens.add({
      targets:this.puanYazi, scale:1.45, duration:130, yoyo:true, ease:'Back.easeOut'
    });
    const ucan = this.add.text(c.x, c.y - 44, '+' + kazanc, {
      fontFamily:'system-ui, sans-serif', fontSize:'26px', fontStyle:'bold',
      color:'#7ce0a3'
    }).setOrigin(0.5).setDepth(95);
    this.tweens.add({
      targets:ucan, y:ucan.y - 54, alpha:0, duration:700,
      ease:'Cubic.easeOut', onComplete:() => ucan.destroy()
    });

    this.mesajGoster(ADIMLAR[this.adim - 1].tamam, '#1f6d4a');
    this.arayuzuTazele();

    this.time.delayedCall(900, () => {
      if (this.adim >= ADIMLAR.length){ this.bitir(true); return; }
      this.adimiBaslat();
    });
  }

  yanlis(c){
    const a = ADIMLAR[this.adim];
    this.seri = 0;
    this.can--;
    this.arayuzuTazele();

    /* GERÇEK FİZİK: yaprak kırılır, peri düşer */
    c.setData('kirik', true);
    c.disableInteractive();
    this.tweens.killTweensOf(c);
    this.tweens.add({
      targets:c, angle:Phaser.Math.Between(50, 90), alpha:0.25, y:c.y + 26,
      duration:520, ease:'Quad.easeIn'
    });

    this.peri.body.setAllowGravity(true);
    this.peri.body.setVelocity(Phaser.Math.Between(-70, 70), 60);
    this.tweens.add({ targets:this.peri, angle:Phaser.Math.Between(-220, 220), duration:700 });
    this.dusuyor = true;

    this.tozlar.explode(14, c.x, c.y);
    this.cameras.main.shake(240, 0.013);
    this.cameras.main.flash(170, 220, 90, 90);
    this.tweens.add({
      targets:this.canYazi, angle:{ from:-12, to:12 },
      duration:70, yoyo:true, repeat:3,
      onComplete:() => this.canYazi.setAngle(0)
    });
    this.mesajGoster(a.ipucu, '#b5453b');
  }

  /* Peri yere çarptı — son güvenli yaprağa geri koy */
  yereDustu(){
    if (!this.dusuyor) return;
    this.dusuyor = false;
    this.uctu = false;
    this.izler.stop();
    this.tozlar.explode(16, this.peri.x, this.peri.y + 14);
    this.cameras.main.shake(160, 0.008);

    this.time.delayedCall(700, () => {
      if (this.can <= 0){ this.bitir(false); return; }
      const geri = this.durakId ? this.yapragiBul(this.durakId) : null;
      const n = geri ? { x:geri.x, y:geri.y - 28 }
                     : (() => { const b = this.nokta(BASLANGIC); return { x:b.x, y:b.y - 28 }; })();
      this.peri.body.setAllowGravity(false);
      this.peri.body.setVelocity(0, 0);
      this.peri.body.reset(n.x, n.y);
      this.peri.setAngle(0);
      this.kilit = false;
    });
  }

  seriGoster(){}

  mesajGoster(metin, arka){
    if (this.mesaj) this.mesaj.destroy();
    this.mesaj = this.add.text(EN / 2, 168, metin, {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#ffffff', backgroundColor:arka,
      padding:{ x:12, y:7 }, align:'center', wordWrap:{ width:EN - 60 }
    }).setOrigin(0.5).setDepth(96).setAlpha(0);
    const t = this.mesaj;
    this.tweens.add({ targets:t, alpha:1, duration:150 });
    this.time.delayedCall(1500, () => {
      if (!t.active) return;
      this.tweens.add({
        targets:t, alpha:0, duration:250,
        onComplete:() => { if (this.mesaj === t) this.mesaj = null; t.destroy(); }
      });
    });
  }

  /* ---------- arayüz ---------- */
  arayuzKur(){
    /* Katalogda yönerge 120 karaktere çıkıyor; sabit yükseklikli şerit
       yazıyı iki yandan kesiyordu. Şerit metnin gerçek boyuna göre. */
    const yon = this.add.text(EN / 2, 22, OYUN_EMO + '  ' + TALIMAT, {
      fontFamily:'system-ui, sans-serif',
      fontSize: (TALIMAT.length > 92 ? '16px' : (TALIMAT.length > 54 ? '17px' : '20px')),
      fontStyle:'bold', color:'#ffffff', align:'center',
      wordWrap:{ width:EN - 52 }, lineSpacing:3
    }).setOrigin(0.5, 0).setDepth(61);

    const seritBoy = Math.max(104, yon.height + 62);
    const serit = this.add.graphics().setDepth(60);
    serit.fillStyle(0x081409, 0.97);
    serit.fillRoundedRect(10, 10, EN - 20, seritBoy, 18);
    yon.setDepth(61);
    const satirY = 10 + seritBoy - 22;
    this.seritAlt = 10 + seritBoy;

    this.puanYazi = this.add.text(30, satirY, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0, 0.5).setDepth(61);

    this.canYazi = this.add.text(EN - 30, satirY, '', { fontSize:'20px' })
      .setOrigin(1, 0.5).setDepth(61);

    this.ilerlemeYazi = this.add.text(EN / 2, satirY, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#a5d6b7'
    }).setOrigin(0.5).setDepth(61);

    this.soruYazi = this.add.text(EN / 2, 140, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#ffffff', align:'center', wordWrap:{ width:EN - 40 }
    }).setOrigin(0.5).setDepth(61);

    this.arayuzuTazele();
  }

  arayuzuTazele(){
    this.canYazi.setText(
      '❤️'.repeat(Math.max(0, this.can)) +
      '🖤'.repeat(Math.max(0, CAN_SAYISI - this.can))
    );
    this.ilerlemeYazi.setText(`${this.adim} / ${ADIMLAR.length} zıplayış`);
  }

  bitir(kazandi){
    /* Uygulama içindeyken kazanma ekranını uygulama gösteriyor. */
    if (kazandi && KOPRU){ KOPRU.bitir(BASARI, this.puan); return; }
    this.scene.start('GameOver', {
      kazandi, puan:this.puan, can:this.can,
      adim:this.adim, toplam:ADIMLAR.length
    });
  }

  /* ---------- her kare ---------- */
  update(){
    if (!this.peri || !this.peri.body) return;

    /* uçuş: hedefe yaklaşınca kon */
    if (this.uctu && !this.dusuyor && this.hedefYaprak){
      const hx = this.hedefYaprak.x, hy = this.hedefYaprak.y - 28;
      const d = Phaser.Math.Distance.Between(this.peri.x, this.peri.y, hx, hy);
      /* aşağı doğru inerken ve yeterince yakınken kon */
      if (d < 22 && this.peri.body.velocity.y > -40){ this.konduHedefe(); return; }
      /* ekrandan kaçtıysa düşüşe geç */
      if (this.peri.y > ALAN_ALT + 40 || this.peri.x < -40 || this.peri.x > EN + 40){
        this.uctu = false; this.dusuyor = true;
      }
    }
  }
}

/* =====================================================================
   4) GAME OVER
   ===================================================================== */
class GameOverScene extends Phaser.Scene {
  constructor(){ super('GameOver'); }

  init(veri){ this.veri = veri; }

  create(){
    const { kazandi, puan, can, adim, toplam } = this.veri;
    bahceCiz(this);

    const emo = this.add.text(EN / 2, 190, kazandi ? '☁️' : '💪', { fontSize:'97px' })
      .setOrigin(0.5).setScale(0);
    this.tweens.add({ targets:emo, scale:1, duration:520, ease:'Back.easeOut' });

    this.add.text(EN / 2, 300, kazandi ? 'BULUTA ULAŞTIN!' : 'TEKRAR DENE', {
      fontFamily:'system-ui, sans-serif', fontSize:'35px', fontStyle:'bold',
      color: kazandi ? '#7ce0a3' : '#ffd166', align:'center'
    }).setOrigin(0.5);

    this.add.text(EN / 2, 360,
      kazandi ? BASARI : `${adim} / ${toplam} zıplayışı başardın — bir daha deneyelim mi?`, {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#d6f0dd',
      align:'center', wordWrap:{ width:EN - 70 }, lineSpacing:5
    }).setOrigin(0.5);

    const puanYazi = this.add.text(EN / 2, 456, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'42px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0.5);
    const sayac = { v:0 };
    this.tweens.add({
      targets:sayac, v:puan, duration:900, ease:'Cubic.easeOut',
      onUpdate:() => puanYazi.setText('Puan ' + Math.round(sayac.v))
    });

    this.add.text(EN / 2, 506,
      'Kalan can: ' + (can > 0 ? '❤️'.repeat(can) : '—'), {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#a5d6b7'
    }).setOrigin(0.5);

    if (kazandi){
      const konfeti = this.add.particles(EN / 2, -20, 'kivilcim', {
        speed:{ min:90, max:260 }, angle:{ min:60, max:120 },
        scale:{ start:0.8, end:0 }, alpha:{ start:1, end:0 },
        lifespan:2000, gravityY:180, quantity:2, frequency:70,
        tint:[0xffd166, 0x7ce0a3, 0x74c98c, 0xf07575]
      }).setDepth(5);
      this.time.delayedCall(2600, () => konfeti.stop());
    }

    dugmeYap(this, EN / 2, 606, '↻  TEKRAR OYNA', RENK.dogru, () => this.scene.start('Game'));

    /* Uygulama içinde: bu oyunda takılan çocuk sıradakine geçebilsin. */

    if (KOPRU) dugmeYap(this, EN / 2, 680, '⏭  SIRADAKİ OYUN', 0x4a679e, () => KOPRU.atla());
    if (!KOPRU) dugmeYap(this, EN / 2, 684, '☰  MENÜ',        0x3f7a53, () => this.scene.start('Menu'));
  }
}

/* =====================================================================
   OYUNU BAŞLAT
   ===================================================================== */
/* =====================================================================
   NETLİK — cihazın piksel yoğunluğunda çizim
   ---------------------------------------------------------------------
   Oyun 480x800 mantıksal tuvalde çiziliyordu; telefon bunu 1080 piksele
   büyütünce yazılar ve kenarlar bulanıklaşıyordu. Çözüm: tuvali cihazın
   gerçek piksel sayısında açmak, dünyayı ise kamerayı NETLIK katına
   yakınlaştırarak yine 480x800 koordinatta tutmak. Böylece Graphics ile
   çizilen her şey (kartlar, şeritler, kutular) vektör keskinliğinde,
   yazılar da NETLIK çözünürlüğünde üretiliyor; oyun kodunun tek satırı
   değişmiyor.
   ===================================================================== */
const NETLIK = Math.min(3, Math.max(1, Math.round((window.devicePixelRatio || 1) * 2) / 2));

/* Phaser yazıyı kendi ara tuvaline çiziyor; çözünürlük verilmezse 1x
   üretilip yakınlaştırmada bulanıklaşır. Bütün yazılara varsayılan
   olarak NETLIK veriyoruz. */
(function(){
  const TS = Phaser.GameObjects.TextStyle.prototype;
  const eskiSetStyle = TS.setStyle;
  TS.setStyle = function(style, updateText, setDefaults){
    if (style && style.resolution === undefined) style.resolution = NETLIK;
    return eskiSetStyle.call(this, style, updateText, setDefaults);
  };
})();

/* Tuval NETLIK katına büyüdüğü için Phaser imleç konumunu da o ölçekte
   veriyor (0–960). Oyun koordinatına (0–480) çeviren yardımcı: sürükleme
   olayları zaten dünya koordinatı verdiği için yalnız pointer olaylarında
   kullanılıyor. */
function imlec(p){ return { x: p.x / NETLIK, y: p.y / NETLIK }; }

/* Her sahne başlarken kamerayı NETLIK katına yakınlaştırıp fizik
   dünyasını mantıksal ölçüde tutuyoruz: tuval büyüdü, dünya büyümedi.
   Sahne örnekleri oyun kurulumundan sonra eşzamansız oluştuğu için
   kanca Systems.start üzerine takılıyor — yeniden başlatmalarda da
   kendiliğinden çalışıyor. */
(function(){
  const SS = Phaser.Scenes.Systems.prototype;
  const eskiStart = SS.start;
  SS.start = function(veri){
    const sonuc = eskiStart.call(this, veri);
    const sc = this.scene;
    try{
      if (sc.cameras && sc.cameras.main){
        sc.cameras.main.setZoom(NETLIK);
        sc.cameras.main.centerOn(EN / 2, BOY / 2);
      }
      if (sc.physics && sc.physics.world) sc.physics.world.setBounds(0, 0, EN, BOY);
    }catch(e){ /* netlik ayarı oyunu engellemesin */ }
    return sonuc;
  };
})();

window.OYUN = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'oyun',
  width: EN * NETLIK,
  height: BOY * NETLIK,
  backgroundColor: '#0d1f16',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 900 } }
  },
  scene: [BootScene, MenuScene, GameScene, GameOverScene]
});

</script>
</body>
</html>
```

### radarkod-phaser.html — numPad (10 oyun)
Dosya boyu: 31656 bayt · 852 satır

```html
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<title>Çoklu Nokta Şifresi — Phaser 3</title>
<script src="https://cdn.jsdelivr.net/npm/phaser@3.80.1/dist/phaser.min.js"></script>
<style>
  html, body { margin:0; padding:0; height:100%; background:#05101c; overflow:hidden;
    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
    -webkit-tap-highlight-color: transparent; touch-action:none; }
  #oyun { width:100%; height:100%; display:flex; align-items:center; justify-content:center; }
  canvas { display:block; }
</style>
</head>
<body>
<div id="oyun"></div>
<script>
/* =====================================================================
   ÇOKLU NOKTA ŞİFRESİ — Phaser 3        (mekanik: numPad · 10 oyun)
   ---------------------------------------------------------------------
   Kazanım: MAT.3.4.1.e — Her verinin birden fazla durumu temsil ettiği
   nokta grafiğini yorumlar.

   Sahneler : Boot → Menu → Game → GameOver
   Fizik    : Arcade.
              · Tuşa basılan rakam kartı şifre tüpüne YERÇEKİMİYLE
                düşer, öncekilerin üstüne yığılır.
              · SİL tuşu en üstteki rakamı yukarı fırlatır.
              · Şifre yanlışsa tüp devrilir, rakamlar dökülür.
              · Doğruysa yıldızlar tüpten fışkırır.
   Görsel   : Bütün dokular Graphics ile çalışma anında üretilir —
              uygulama çevrimdışı kabukta (APK / iOS) çalışacağı için
              dışarıdan resim çekilmiyor.
   ===================================================================== */

const EN = 480, BOY = 800;

const RENK = {
  uzayUst : 0x071426,
  uzayAlt : 0x123650,
  dogru   : 0x34c47b,
  yanlis  : 0xf07575,
  tup     : 0x7fe7ff,
  rakam   : 0xfdfbff,
  tus     : 0x1d4460,
  vurgu   : 0xffd166
};

/* ---------------------------------------------------------------------
   İÇERİK — uygulamadaki w47 oyununun birebir aynısı.
   Başka bir numPad oyununa geçmek için yalnızca bu blok değişir.
   ------------------------------------------------------------------- */
/* ---------------- uygulama köprüsü ----------------
   Adres  radarkod.html#oyun=w47  biçiminde; katalog verisi üst pencereden
   okunuyor. Kazanınca completeGame() çağrılır.                          */
const KOPRU = (function(){
  try{
    const p = new URLSearchParams(location.hash.slice(1));
    const id = p.get('oyun');
    if (id && window.parent && window.parent !== window &&
        typeof window.parent.getGame === 'function'){
      const g = window.parent.getGame(id);
      if (g && g.cfg) return {
        oyun: g, cfg: g.cfg,
        bitir(mesaj, puan){ try{ window.parent.completeGame(mesaj || '', puan); }catch(e){} },
        /* Turun kendi metnini uygulamanın sesiyle okutur (Piper). */
        oku(metin){ try{ if (window.parent.oku) window.parent.oku(metin); }catch(e){} },
        /* Kaybetme ekranından: bu oyunu bırak, sıradakine geç. */
        atla(){ try{ if (window.parent.sonrakiOyunaGec) window.parent.sonrakiOyunaGec(); }catch(e){} }
      };
    }
  }catch(e){ /* çapraz kaynak engeli: tek başına oynanır */ }
  return null;
})();

/* HTML varlıklarını çöz: katalogda "Pay &lt; payda" gibi yazımlar var,
   çözülmezse ekranda "&lt;" olarak görünüyor ve öyle okunuyor. */
function varlikCoz(m){
  return String(m)
    .replace(/&nbsp;/gi, ' ')
    .replace(/&lt;/gi, '<').replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"').replace(/&#39;|&apos;/gi, "'")
    .replace(/&hellip;/gi, '…').replace(/&mdash;/gi, '—').replace(/&ndash;/gi, '–')
    .replace(/&times;/gi, '×').replace(/&divide;/gi, '÷').replace(/&deg;/gi, '°')
    .replace(/&rarr;/gi, '→').replace(/&larr;/gi, '←')
    .replace(/&amp;/gi, '&');            /* en sona: çift çözmeyi önler */
}

function duzMetin(x){
  return varlikCoz(String(x == null ? '' : x).replace(/<br\s*\/?>/gi,' ')
    .replace(/<[^>]+>/g,'')).replace(/[“”]/g,'"').replace(/\s+/g,' ').trim();
}
function tekSatir(x){ return duzMetin(x).replace(/\n/g,' '); }

const VARSAYILAN = {
  instruction:'Ölçeği çöz, sayıyı tuşla',
  tip:'Ölçekli grafikte: nokta sayısı × bir noktanın değeri = gerçek sayı',
  rounds:[
    { question:'Mavi takımyıldız: 4 nokta<br>Gerçekte kaç yıldız var?', answer:20,
      unit:'yıldız', hint:'Her nokta 5 yıldız → 4 × 5 = ?',
      wrongHint:'Her nokta 5 yıldız! 4 × 5 hesapla.', okMsg:'4 × 5 = 20 yıldız ✅' } ]
};

const CFG = KOPRU ? KOPRU.cfg : VARSAYILAN;
const PALET = [0x4a7fd6, 0xd9534f, 0x4fb286, 0xe0a83c, 0x8c6fd0];

/* Şablon soruyu nokta grafiğiyle canlandırıyor; katalogda nokta sayısı
   ayrı alan değil, soru metninde geçiyor. Metindeki "N nokta" kalıbından
   çıkarıyoruz — bulunamazsa nokta çizilmiyor, soru yine tuşlanabiliyor. */
function noktaSayisi(soru){
  const m = tekSatir(soru).match(/(\d+)\s*nokta/i);
  return m ? Math.min(12, Number(m[1])) : 0;
}

const TURLAR = (CFG.rounds || []).map((r, i) => ({
  seslen:    tekSatir(r.say) || tekSatir(r.question),
  soru:      duzMetin(r.question),
  noktalar:  noktaSayisi(r.question),
  noktaRenk: PALET[i % PALET.length],
  cevap:     Number(r.answer),
  birim:     tekSatir(r.unit),
  ipucu:     tekSatir(r.hint),
  hata:      tekSatir(r.wrongHint) || 'Tekrar hesapla.',
  tamam:     tekSatir(r.okMsg) || 'Doğru! ✅'
}));

const OYUN_ADI = KOPRU ? tekSatir(KOPRU.oyun.title) : 'ÇOKLU NOKTA ŞİFRESİ';
const OYUN_EMO = KOPRU ? (KOPRU.oyun.emo || '📡') : '📡';
const TALIMAT  = tekSatir(CFG.instruction) || 'Sonucu hesapla ve tuşla';
const IPUCU    = tekSatir(CFG.tip);
const OLCEK    = '';
const BASARI   = tekSatir(CFG.successMsg) || 'Bütün şifreleri çözdün!';

const CAN_SAYISI = 3;
/* KUSUR: 3 SABİTTİ. p01'in dört turu (245612, 103020, 500000, 36908) ve
   p18'in dört turu (5634, 3348, 4000, 3766) 4–6 basamaklı; çocuk cevabı
   TUŞLAYAMIYORDU — iki oyun baştan sona oynanamaz durumdaydı.
   Basamak sınırı turların gerçek cevaplarından hesaplanıyor. */
const AZAMI_BASAMAK = Math.max(3, Math.min(7,
  TURLAR.reduce((a, t) => Math.max(a, String(Math.abs(t.cevap) || 0).length), 0)));


/* --- Yerleşim -------------------------------------------------------- */
const TUP_X    = EN / 2;
const TUP_UST  = 336;
const TUP_ALT  = 448;
const TUP_EN   = 168;
const TUS_UST  = 512;   /* tuş takımının ilk satırı */
const TUS_ARA  = 62;
const RAKAM_BOY = 34;
/* Kart genişliği ve aralığı tüpe sığacak şekilde: 6 basamakta 46px aralık
   230px eder, tüp ise 168px — kartlar tüpün dışına diziliyordu. */
const RAKAM_ARA = Math.min(46, Math.floor((TUP_EN - 20) / AZAMI_BASAMAK));
const RAKAM_EN  = Math.max(18, RAKAM_ARA - 8);

/* =====================================================================
   1) BOOT — dokuları üret
   ===================================================================== */
class BootScene extends Phaser.Scene {
  constructor(){ super('Boot'); }

  create(){
    this.dokuKivilcim();
    this.dokuToz();
    this.dokuYildiz();
    /* Uygulama içinde çocuk oyunu listeden zaten seçti; menüyü atla. */
    this.scene.start(KOPRU ? 'Game' : 'Menu');
  }

  dokuKivilcim(){
    const g = this.make.graphics({ add:false });
    g.fillStyle(0xffffff, 1);
    g.fillCircle(8, 8, 8);
    g.generateTexture('kivilcim', 16, 16);
    g.destroy();
  }

  dokuToz(){
    const g = this.make.graphics({ add:false });
    for (let r = 14; r > 0; r--){
      g.fillStyle(0xffffff, 0.06);
      g.fillCircle(14, 14, r);
    }
    g.generateTexture('toz', 28, 28);
    g.destroy();
  }

  /* Beş köşeli yıldız — doğru cevapta fışkırır */
  dokuYildiz(){
    const R = 11, W = R * 2 + 4, H = R * 2 + 4;
    const g = this.make.graphics({ add:false });
    g.fillStyle(RENK.vurgu, 1);
    g.beginPath();
    for (let i = 0; i < 10; i++){
      const a = Phaser.Math.DegToRad(-90 + i * 36);
      const yr = i % 2 === 0 ? R : R * 0.45;
      const x = W / 2 + Math.cos(a) * yr, y = H / 2 + Math.sin(a) * yr;
      if (i === 0) g.moveTo(x, y); else g.lineTo(x, y);
    }
    g.closePath(); g.fillPath();
    g.generateTexture('yildiz', W, H);
    g.destroy();
  }
}

/* =====================================================================
   Ortak yardımcılar
   ===================================================================== */
function uzayCiz(sc){
  const g = sc.add.graphics();
  g.fillGradientStyle(RENK.uzayUst, RENK.uzayUst, RENK.uzayAlt, RENK.uzayAlt, 1);
  g.fillRect(0, 0, EN, BOY);

  for (let i = 0; i < 44; i++){
    const s = sc.add.circle(
      Phaser.Math.Between(4, EN - 4),
      Phaser.Math.Between(4, BOY - 4),
      Phaser.Math.FloatBetween(1, 2.3),
      0xffffff,
      Phaser.Math.FloatBetween(0.2, 0.85)
    );
    sc.tweens.add({
      targets:s, alpha:0.06,
      duration:Phaser.Math.Between(800, 2400),
      yoyo:true, repeat:-1, delay:Phaser.Math.Between(0, 1800)
    });
  }
  return g;
}

function dugmeYap(sc, x, y, metin, renk, geriCagri, genislik, yukseklik){
  const W = genislik || 280, H = yukseklik || 60;
  const c = sc.add.container(x, y);
  const g = sc.add.graphics();
  g.fillStyle(renk, 1);
  g.fillRoundedRect(-W / 2, -H / 2, W, H, Math.min(H / 2, 16));
  g.fillStyle(0xffffff, 0.16);
  g.fillRoundedRect(-W / 2, -H / 2, W, H * 0.38, { tl:Math.min(H / 2, 16), tr:Math.min(H / 2, 16), bl:0, br:0 });
  const t = sc.add.text(0, 0, metin, {
    fontFamily:'system-ui, sans-serif', fontSize: H > 52 ? '20px' : '17px',
    fontStyle:'bold', color:'#ffffff', align:'center'
  }).setOrigin(0.5);
  c.add([g, t]);
  c.setSize(W, H).setInteractive({ useHandCursor:true });
  c.on('pointerover', () => sc.tweens.add({ targets:c, scale:1.06, duration:100 }));
  c.on('pointerout',  () => sc.tweens.add({ targets:c, scale:1.00, duration:100 }));
  /* KUSUR: geri çağrı basma TWEEN'inin sonunda çalışıyordu (≈180ms).
     Tuş takımında aynı tuşa üst üste basıldığında bir basış yutuluyordu
     (sınamada "500000" yerine "50000" yazıldı) ve her dokunuş 180ms
     gecikmeyle işliyordu. Artık işlem HEMEN yapılıyor, tween yalnız
     görsel geri bildirim. */
  c.on('pointerdown', () => {
    sc.tweens.add({ targets:c, scale:0.9, duration:80, yoyo:true });
    if (geriCagri) geriCagri();
  });
  return c;
}

/* =====================================================================
   2) MENU
   ===================================================================== */
class MenuScene extends Phaser.Scene {
  constructor(){ super('Menu'); }

  create(){
    uzayCiz(this);

    this.add.text(EN / 2, 186, OYUN_EMO, { fontSize:'88px' }).setOrigin(0.5);
    /* nokta → yıldız dönüşümü canlandırması */
    for (let i = 0; i < 4; i++){
      const n = this.add.circle(EN / 2 - 72 + i * 48, 262, 11, 0x4a7fd6, 1);
      this.tweens.add({
        targets:n, scale:1.3, duration:800, delay:i * 160,
        yoyo:true, repeat:-1, ease:'Sine.easeInOut'
      });
    }

    const baslik = this.add.text(EN / 2, 348, OYUN_ADI, {
      fontFamily:'system-ui, sans-serif', fontSize:'40px', fontStyle:'bold',
      color:'#ffffff', align:'center', lineSpacing:5
    }).setOrigin(0.5);
    this.tweens.add({
      targets:baslik, scale:1.04, duration:1400,
      yoyo:true, repeat:-1, ease:'Sine.easeInOut'
    });

    this.add.text(EN / 2, 430, TALIMAT, {
      fontFamily:'system-ui, sans-serif', fontSize:'22px',
      color:'#cfe6ff', align:'center'
    }).setOrigin(0.5);

    const kart = this.add.graphics();
    kart.fillStyle(0x061726, 0.92);
    kart.fillRoundedRect(30, 466, EN - 60, 84, 16);
    kart.lineStyle(2, 0x2f5f80, 1);
    kart.strokeRoundedRect(30, 466, EN - 60, 84, 16);
    this.add.text(EN / 2, 508, IPUCU, {
      fontFamily:'system-ui, sans-serif', fontSize:'17px', fontStyle:'bold',
      color:'#ffd166', align:'center', wordWrap:{ width:EN - 90 }, lineSpacing:4
    }).setOrigin(0.5);

    dugmeYap(this, EN / 2, 618, '▶  BAŞLA', RENK.dogru, () => this.scene.start('Game'));

    this.add.text(EN / 2, 714, `${TURLAR.length} şifre  ·  ${CAN_SAYISI} can`, {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', color:'#8fb8d6'
    }).setOrigin(0.5);
  }
}

/* =====================================================================
   3) GAME
   ===================================================================== */
class GameScene extends Phaser.Scene {
  constructor(){ super('Game'); }

  create(){
    this.can   = CAN_SAYISI;
    this.puan  = 0;
    this.seri  = 0;
    this.tur   = 0;
    this.kilit = true;

    /* Phaser sahne örneğini yeniden kullanır — TEKRAR OYNA'da eski
       nesnelere işaret etmesinler. */
    this.rakamlar  = null;
    this.engeller  = null;
    this.noktaNesne = null;
    this.mesaj     = null;

    uzayCiz(this);

    this.kivilcimlar = this.add.particles(0, 0, 'kivilcim', {
      speed:{ min:130, max:350 }, angle:{ min:0, max:360 },
      scale:{ start:0.85, end:0 }, alpha:{ start:1, end:0 },
      lifespan:620, gravityY:300, blendMode:'ADD', emitting:false
    }).setDepth(90);

    this.tozlar = this.add.particles(0, 0, 'toz', {
      speed:{ min:40, max:150 }, angle:{ min:200, max:340 },
      scale:{ start:0.9, end:2 }, alpha:{ start:0.5, end:0 },
      lifespan:660, emitting:false
    }).setDepth(80);

    this.yildizlar = this.add.particles(0, 0, 'yildiz', {
      speed:{ min:120, max:300 }, angle:{ min:230, max:310 },
      scale:{ start:1, end:0.2 }, alpha:{ start:1, end:0 },
      lifespan:1100, gravityY:420, rotate:{ start:0, end:360 }, emitting:false
    }).setDepth(88);

    this.sahneKur();
    this.arayuzKur();
    this.tuslariKur();
    this.turuBaslat();
  }

  /* ---------- sabit sahne ---------- */
  sahneKur(){
    /* şifre tüpü */
    this.tupCizim = this.add.graphics().setDepth(6);
    this.tupCiz();

    /* NOT: Phaser'da collider(grup, TEK nesne) callback'e parametreleri
       ters veriyor; engeller staticGroup içinde. */
    this.engeller = this.physics.add.staticGroup();
    this.tupTaban = this.add.rectangle(TUP_X, TUP_ALT + 8, TUP_EN - 12, 16, 0, 0);
    this.tupSol   = this.add.rectangle(TUP_X - TUP_EN / 2 + 2, (TUP_UST + TUP_ALT) / 2 - 40,
                                       12, TUP_ALT - TUP_UST + 120, 0, 0);
    this.tupSag   = this.add.rectangle(TUP_X + TUP_EN / 2 - 2, (TUP_UST + TUP_ALT) / 2 - 40,
                                       12, TUP_ALT - TUP_UST + 120, 0, 0);
    this.engeller.addMultiple([this.tupTaban, this.tupSol, this.tupSag]);

    this.rakamlar = this.physics.add.group();
    this.physics.add.collider(this.rakamlar, this.engeller);
    this.physics.add.collider(this.rakamlar, this.rakamlar);
  }

  tupCiz(renk){
    const g = this.tupCizim;
    const x = TUP_X - TUP_EN / 2, y = TUP_UST, w = TUP_EN, h = TUP_ALT - TUP_UST;
    g.clear();
    g.fillStyle(0x0a2033, 0.85);
    g.fillRoundedRect(x, y, w, h, 12);
    g.lineStyle(3, renk || RENK.tup, 0.85);
    g.strokeRoundedRect(x, y, w, h, 12);
    /* köşe işaretleri */
    g.lineStyle(3, renk || RENK.tup, 1);
    [[x, y], [x + w, y], [x, y + h], [x + w, y + h]].forEach(([px, py], i) => {
      const sx = i % 2 === 0 ? 1 : -1, sy = i < 2 ? 1 : -1;
      g.lineBetween(px, py + sy * 4, px + sx * 18, py + sy * 4);
      g.lineBetween(px + sx * 4, py, px + sx * 4, py + sy * 18);
    });
    this.add.text ? 0 : 0;
  }

  /* ---------- tuş takımı ---------- */
  tuslariKur(){
    /* 1-9 üç satır, sonra 0 · SİL · ONAY */
    for (let i = 1; i <= 9; i++){
      const sut = (i - 1) % 3, sat = Math.floor((i - 1) / 3);
      const x = EN / 2 - 118 + sut * 118;
      const y = TUS_UST + sat * TUS_ARA;
      dugmeYap(this, x, y, String(i), RENK.tus, () => this.rakamGir(i), 104, 52).setDepth(12);
    }
    const y4 = TUS_UST + 3 * TUS_ARA;
    dugmeYap(this, EN / 2 - 118, y4, '0',   RENK.tus,   () => this.rakamGir(0), 104, 52).setDepth(12);
    dugmeYap(this, EN / 2,       y4, '⌫ SİL', 0x6b4a8a, () => this.rakamSil(),  104, 52).setDepth(12);
    dugmeYap(this, EN / 2 + 118, y4, '✓ GİR', RENK.dogru, () => this.onayla(),  104, 52).setDepth(12);
  }

  rakamGir(d){
    if (this.kilit) return;
    if (this.girilen.length >= AZAMI_BASAMAK){
      this.mesajGoster('En fazla ' + AZAMI_BASAMAK + ' basamak — SİL ile düzelt.', '#2f5f80');
      return;
    }
    this.girilen.push(d);
    this.rakamDusur(d);
    this.girisTazele();
  }

  /* GERÇEK FİZİK: rakam kartı tüpe düşer, yığının üstüne oturur */
  rakamDusur(d){
    if (!this.rakamlar || !this.rakamlar.children) return;
    const sira = this.girilen.length - 1;
    /* Kartlar tüpün ortasına göre dizilir; basamak sayısı kaç olursa olsun
       tüpün içinde kalır. */
    const sol = TUP_X - (AZAMI_BASAMAK - 1) * RAKAM_ARA / 2;
    const c = this.add.container(sol + sira * RAKAM_ARA, TUP_UST - 60).setDepth(20);
    const g = this.add.graphics();
    g.fillStyle(RENK.rakam, 1);
    g.fillRoundedRect(-RAKAM_EN / 2, -RAKAM_BOY / 2, RAKAM_EN, RAKAM_BOY, 7);
    g.lineStyle(2, 0xc9d6ee, 1);
    g.strokeRoundedRect(-RAKAM_EN / 2, -RAKAM_BOY / 2, RAKAM_EN, RAKAM_BOY, 7);
    const t = this.add.text(0, 0, String(d), {
      fontFamily:'system-ui, sans-serif',
      fontSize: Math.max(14, Math.min(24, RAKAM_EN - 14)) + 'px',
      fontStyle:'bold', color:'#12324a'
    }).setOrigin(0.5);
    c.add([g, t]);
    c.setSize(RAKAM_EN, RAKAM_BOY);

    this.rakamlar.add(c);
    c.body.setSize(RAKAM_EN, RAKAM_BOY);
    c.body.setBounce(0.24, 0.24);
    c.body.setDragX(120);
    c.setData('rakam', d);
    this.tozlar.explode(3, c.x, c.y + 12);
    return c;
  }

  rakamSil(){
    if (this.kilit) return;
    if (!this.girilen.length) return;
    this.girilen.pop();
    /* en son eklenen kart yukarı fırlar ve yok olur */
    const liste = this.rakamlar.getChildren();
    const c = liste[liste.length - 1];
    if (c){
      c.body.enable = false;
      this.tweens.add({
        targets:c, y:c.y - 90, alpha:0, angle:Phaser.Math.Between(-120, 120),
        duration:340, ease:'Quad.easeOut', onComplete:() => c.destroy()
      });
      this.tozlar.explode(6, c.x, c.y);
    }
    this.girisTazele();
  }

  girisTazele(){
    const s = this.girilen.join('');
    this.girisYazi.setText(s.length ? s + ' ' + TURLAR[this.tur].birim : '— — —');
  }

  /* ---------- tur ---------- */
  turuBaslat(){
    const t = TURLAR[this.tur];
    if (KOPRU) KOPRU.oku(t.seslen);
    this.kilit = true;
    this.girilen = [];
    this.nesil = (this.nesil || 0) + 1;

    this.rakamlar.clear(true, true);
    if (this.noktaNesne) this.noktaNesne.forEach(o => o.destroy());
    this.noktaNesne = [];

    /* tüp duvarlarını geri aç */
    [this.tupTaban, this.tupSol, this.tupSag].forEach(r => { r.body.enable = true; });
    this.tupCizim.setAngle(0);
    this.tupCiz();

    this.soruYazi.setText(t.soru);
    this.ipucuYazi.setText(t.ipucu);
    this.tweens.add({
      targets:this.soruYazi, scale:{ from:0.88, to:1 }, duration:280, ease:'Back.easeOut'
    });

    /* nokta grafiği */
    const n = t.noktalar;
    for (let i = 0; i < n; i++){
      const x = EN / 2 - (n - 1) * 17 + i * 34;
      const nk = this.add.circle(x, 268, 12, t.noktaRenk, 1).setDepth(10);
      this.tweens.add({
        targets:nk, scale:1.18, duration:800, delay:i * 110,
        yoyo:true, repeat:-1, ease:'Sine.easeInOut'
      });
      this.noktaNesne.push(nk);
    }

    this.girisTazele();
    this.time.delayedCall(320, () => { this.kilit = false; });
    this.arayuzuTazele();
  }

  /* ---------- onay ---------- */
  onayla(){
    if (this.kilit) return;
    if (!this.girilen.length){
      this.mesajGoster('Önce bir sayı tuşla.', '#2f5f80');
      return;
    }
    this.kilit = true;
    const t = TURLAR[this.tur];
    const deger = parseInt(this.girilen.join(''), 10);
    if (deger === t.cevap) this.dogru();
    else                   this.yanlis(deger);
  }

  dogru(){
    const t = TURLAR[this.tur];
    this.seri++;
    const kazanc = 200 + (this.seri - 1) * 50;
    this.puan += kazanc;

    this.tupCiz(RENK.dogru);
    this.rakamlar.getChildren().forEach(c => {
      const g = c.list[0];
      g.clear();
      g.fillStyle(0xd8f0e2, 1);
      g.fillRoundedRect(-19, -RAKAM_BOY / 2, 38, RAKAM_BOY, 7);
      g.lineStyle(2, RENK.dogru, 1);
      g.strokeRoundedRect(-19, -RAKAM_BOY / 2, 38, RAKAM_BOY, 7);
    });

    /* GERÇEK FİZİK: yıldızlar tüpten fışkırır */
    this.yildizlar.explode(Math.min(t.cevap, 30), TUP_X, TUP_UST + 20);
    this.kivilcimlar.setParticleTint(RENK.dogru);
    this.kivilcimlar.explode(24, TUP_X, TUP_ALT - 20);
    this.cameras.main.flash(150, 80, 210, 140);

    this.puanYazi.setText('Puan ' + this.puan);
    this.tweens.add({
      targets:this.puanYazi, scale:1.5, duration:140, yoyo:true, ease:'Back.easeOut'
    });
    const ucan = this.add.text(TUP_X, TUP_UST - 34, '+' + kazanc, {
      fontFamily:'system-ui, sans-serif', fontSize:'29px', fontStyle:'bold',
      color:'#7ce0a3'
    }).setOrigin(0.5).setDepth(95);
    this.tweens.add({
      targets:ucan, y:ucan.y - 52, alpha:0, duration:760,
      ease:'Cubic.easeOut', onComplete:() => ucan.destroy()
    });

    this.mesajGoster(t.tamam, '#1f6d4a');
    this.tur++;
    this.arayuzuTazele();

    this.time.delayedCall(2100, () => {
      if (this.tur >= TURLAR.length){ this.bitir(true); return; }
      this.turuBaslat();
    });
  }

  yanlis(deger){
    const t = TURLAR[this.tur];
    this.seri = 0;
    this.can--;
    this.arayuzuTazele();

    /* GERÇEK FİZİK: tüp devrilir, rakamlar dökülür */
    this.tupCiz(RENK.yanlis);
    this.tweens.add({ targets:this.tupCizim, angle:16, duration:420, yoyo:true });
    this.tupTaban.body.enable = false;
    this.rakamlar.getChildren().forEach(c => {
      c.body.setVelocity(Phaser.Math.Between(-120, 160), Phaser.Math.Between(-180, -60));
      this.tweens.add({ targets:c, angle:Phaser.Math.Between(-200, 200), duration:620 });
    });

    this.tozlar.explode(16, TUP_X, TUP_ALT);
    this.cameras.main.shake(240, 0.013);
    this.cameras.main.flash(170, 220, 90, 90);
    this.tweens.add({
      targets:this.canYazi, angle:{ from:-12, to:12 },
      duration:70, yoyo:true, repeat:3,
      onComplete:() => this.canYazi.setAngle(0)
    });

    this.mesajGoster(deger + ' değil — ' + t.hata, '#b5453b');

    this.time.delayedCall(1800, () => {
      if (this.can <= 0){ this.bitir(false); return; }
      this.turuBaslat();      /* aynı tur yeniden */
    });
  }

  mesajGoster(metin, arka){
    if (this.mesaj) this.mesaj.destroy();
    this.mesaj = this.add.text(EN / 2, 474, metin, {
      fontFamily:'system-ui, sans-serif', fontSize:'17px', fontStyle:'bold',
      color:'#ffffff', backgroundColor:arka,
      padding:{ x:12, y:7 }, align:'center', wordWrap:{ width:EN - 60 }
    }).setOrigin(0.5).setDepth(96).setAlpha(0);
    const t = this.mesaj;
    this.tweens.add({ targets:t, alpha:1, duration:150 });
    this.time.delayedCall(1700, () => {
      if (!t.active) return;
      this.tweens.add({
        targets:t, alpha:0, duration:250,
        onComplete:() => { if (this.mesaj === t) this.mesaj = null; t.destroy(); }
      });
    });
  }

  /* ---------- arayüz ---------- */
  arayuzKur(){
    /* Katalogda yönerge 120 karaktere çıkıyor; sabit yükseklikli şerit
       yazıyı iki yandan kesiyordu. Şerit metnin gerçek boyuna göre. */
    const yon = this.add.text(EN / 2, 22, OYUN_EMO + '  ' + TALIMAT, {
      fontFamily:'system-ui, sans-serif',
      fontSize: (TALIMAT.length > 92 ? '16px' : (TALIMAT.length > 54 ? '17px' : '20px')),
      fontStyle:'bold', color:'#ffffff', align:'center',
      wordWrap:{ width:EN - 52 }, lineSpacing:3
    }).setOrigin(0.5, 0).setDepth(61);

    const seritBoy = Math.max(104, yon.height + 62);
    const serit = this.add.graphics().setDepth(60);
    serit.fillStyle(0x04101b, 0.97);
    serit.fillRoundedRect(10, 10, EN - 20, seritBoy, 18);
    yon.setDepth(61);
    const satirY = 10 + seritBoy - 22;
    this.seritAlt = 10 + seritBoy;

    this.puanYazi = this.add.text(30, satirY, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0, 0.5).setDepth(61);

    this.canYazi = this.add.text(EN - 30, satirY, '', { fontSize:'20px' })
      .setOrigin(1, 0.5).setDepth(61);

    this.ilerlemeYazi = this.add.text(EN / 2, satirY, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'19px', fontStyle:'bold',
      color:'#8fb8d6'
    }).setOrigin(0.5).setDepth(61);

    /* ölçek bilgisi */
    const o = this.add.graphics().setDepth(6);
    o.fillStyle(0x061726, 0.9);
    o.fillRoundedRect(84, 124, EN - 168, 28, 9);
    o.lineStyle(2, 0x2f5f80, 1);
    o.strokeRoundedRect(84, 124, EN - 168, 28, 9);
    this.add.text(EN / 2, 138, OLCEK, {
      fontFamily:'system-ui, sans-serif', fontSize:'16px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0.5).setDepth(7);

    this.soruYazi = this.add.text(EN / 2, 186, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'20px', fontStyle:'bold',
      color:'#ffffff', align:'center', wordWrap:{ width:EN - 44 }, lineSpacing:4
    }).setOrigin(0.5).setDepth(61);

    this.ipucuYazi = this.add.text(EN / 2, 226, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'16px',
      color:'#8fb8d6', align:'center'
    }).setOrigin(0.5).setDepth(61);

    this.girisYazi = this.add.text(EN / 2, TUP_ALT + 34, '', {
      fontFamily:'system-ui, sans-serif', fontSize:'24px', fontStyle:'bold',
      color:'#7fe7ff'
    }).setOrigin(0.5).setDepth(28);

    this.arayuzuTazele();
  }

  arayuzuTazele(){
    this.canYazi.setText(
      '❤️'.repeat(Math.max(0, this.can)) +
      '🖤'.repeat(Math.max(0, CAN_SAYISI - this.can))
    );
    this.ilerlemeYazi.setText(`${this.tur} / ${TURLAR.length} şifre`);
  }

  bitir(kazandi){
    /* Uygulama içindeyken kazanma ekranını uygulama gösteriyor. */
    if (kazandi && KOPRU){ KOPRU.bitir(BASARI, this.puan); return; }
    this.scene.start('GameOver', {
      kazandi, puan:this.puan, can:this.can,
      tur:this.tur, toplam:TURLAR.length
    });
  }

  /* ---------- her kare ---------- */
  update(){
    if (!this.rakamlar || !this.rakamlar.children) return;
    this.rakamlar.getChildren().forEach(c => {
      if (!c.active || !c.body || !c.body.enable) return;
      if (c.y > BOY + 50 || c.x < -50 || c.x > EN + 50){
        c.body.reset(TUP_X, TUP_UST - 40);
        c.body.setVelocity(0, 0);
      }
    });
  }
}

/* =====================================================================
   4) GAME OVER
   ===================================================================== */
class GameOverScene extends Phaser.Scene {
  constructor(){ super('GameOver'); }

  init(veri){ this.veri = veri; }

  create(){
    const { kazandi, puan, can, tur, toplam } = this.veri;
    uzayCiz(this);

    const emo = this.add.text(EN / 2, 190, kazandi ? '📡' : '💪', { fontSize:'97px' })
      .setOrigin(0.5).setScale(0);
    this.tweens.add({ targets:emo, scale:1, duration:520, ease:'Back.easeOut' });

    this.add.text(EN / 2, 300, kazandi ? 'ÖLÇEK UZMANI!' : 'TEKRAR DENE', {
      fontFamily:'system-ui, sans-serif', fontSize:'35px', fontStyle:'bold',
      color: kazandi ? '#7ce0a3' : '#ffd166', align:'center'
    }).setOrigin(0.5);

    this.add.text(EN / 2, 360,
      kazandi ? BASARI : `${tur} / ${toplam} şifreyi çözdün — bir daha deneyelim mi?`, {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#cfe6ff',
      align:'center', wordWrap:{ width:EN - 70 }, lineSpacing:5
    }).setOrigin(0.5);

    const puanYazi = this.add.text(EN / 2, 456, 'Puan 0', {
      fontFamily:'system-ui, sans-serif', fontSize:'42px', fontStyle:'bold',
      color:'#ffd166'
    }).setOrigin(0.5);
    const sayac = { v:0 };
    this.tweens.add({
      targets:sayac, v:puan, duration:900, ease:'Cubic.easeOut',
      onUpdate:() => puanYazi.setText('Puan ' + Math.round(sayac.v))
    });

    this.add.text(EN / 2, 506,
      'Kalan can: ' + (can > 0 ? '❤️'.repeat(can) : '—'), {
      fontFamily:'system-ui, sans-serif', fontSize:'21px', color:'#8fb8d6'
    }).setOrigin(0.5);

    if (kazandi){
      const konfeti = this.add.particles(EN / 2, -20, 'yildiz', {
        speed:{ min:90, max:260 }, angle:{ min:60, max:120 },
        scale:{ start:0.9, end:0.2 }, alpha:{ start:1, end:0 },
        lifespan:2000, gravityY:180, quantity:2, frequency:70,
        rotate:{ start:0, end:360 }
      }).setDepth(5);
      this.time.delayedCall(2600, () => konfeti.stop());
    }

    dugmeYap(this, EN / 2, 606, '↻  TEKRAR OYNA', RENK.dogru, () => this.scene.start('Game'));

    /* Uygulama içinde: bu oyunda takılan çocuk sıradakine geçebilsin. */

    if (KOPRU) dugmeYap(this, EN / 2, 680, '⏭  SIRADAKİ OYUN', 0x4a679e, () => KOPRU.atla());
    if (!KOPRU) dugmeYap(this, EN / 2, 684, '☰  MENÜ',        0x2f5f80, () => this.scene.start('Menu'));
  }
}

/* =====================================================================
   OYUNU BAŞLAT
   ===================================================================== */
/* =====================================================================
   NETLİK — cihazın piksel yoğunluğunda çizim
   ---------------------------------------------------------------------
   Oyun 480x800 mantıksal tuvalde çiziliyordu; telefon bunu 1080 piksele
   büyütünce yazılar ve kenarlar bulanıklaşıyordu. Çözüm: tuvali cihazın
   gerçek piksel sayısında açmak, dünyayı ise kamerayı NETLIK katına
   yakınlaştırarak yine 480x800 koordinatta tutmak. Böylece Graphics ile
   çizilen her şey (kartlar, şeritler, kutular) vektör keskinliğinde,
   yazılar da NETLIK çözünürlüğünde üretiliyor; oyun kodunun tek satırı
   değişmiyor.
   ===================================================================== */
const NETLIK = Math.min(3, Math.max(1, Math.round((window.devicePixelRatio || 1) * 2) / 2));

/* Phaser yazıyı kendi ara tuvaline çiziyor; çözünürlük verilmezse 1x
   üretilip yakınlaştırmada bulanıklaşır. Bütün yazılara varsayılan
   olarak NETLIK veriyoruz. */
(function(){
  const TS = Phaser.GameObjects.TextStyle.prototype;
  const eskiSetStyle = TS.setStyle;
  TS.setStyle = function(style, updateText, setDefaults){
    if (style && style.resolution === undefined) style.resolution = NETLIK;
    return eskiSetStyle.call(this, style, updateText, setDefaults);
  };
})();

/* Tuval NETLIK katına büyüdüğü için Phaser imleç konumunu da o ölçekte
   veriyor (0–960). Oyun koordinatına (0–480) çeviren yardımcı: sürükleme
   olayları zaten dünya koordinatı verdiği için yalnız pointer olaylarında
   kullanılıyor. */
function imlec(p){ return { x: p.x / NETLIK, y: p.y / NETLIK }; }

/* Her sahne başlarken kamerayı NETLIK katına yakınlaştırıp fizik
   dünyasını mantıksal ölçüde tutuyoruz: tuval büyüdü, dünya büyümedi.
   Sahne örnekleri oyun kurulumundan sonra eşzamansız oluştuğu için
   kanca Systems.start üzerine takılıyor — yeniden başlatmalarda da
   kendiliğinden çalışıyor. */
(function(){
  const SS = Phaser.Scenes.Systems.prototype;
  const eskiStart = SS.start;
  SS.start = function(veri){
    const sonuc = eskiStart.call(this, veri);
    const sc = this.scene;
    try{
      if (sc.cameras && sc.cameras.main){
        sc.cameras.main.setZoom(NETLIK);
        sc.cameras.main.centerOn(EN / 2, BOY / 2);
      }
      if (sc.physics && sc.physics.world) sc.physics.world.setBounds(0, 0, EN, BOY);
    }catch(e){ /* netlik ayarı oyunu engellemesin */ }
    return sonuc;
  };
})();

window.OYUN = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'oyun',
  width: EN * NETLIK,
  height: BOY * NETLIK,
  backgroundColor: '#05101c',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 760 } }
  },
  scene: [BootScene, MenuScene, GameScene, GameOverScene]
});

</script>
</body>
</html>
```

---
## 3. BÖLÜM — Sınama koşucusu (ucuncu_sinama.js)
Dokuz mekaniğin otomatik oyuncuları. Uygulama sayfasının konsolunda:

```js
(0,eval)(await (await fetch('/ucuncu_sinama.js')).text());
SINAMA.topluBaslat(SINAMA.oynaCatchDrop, ['u04'], 'sonuc.jsonl');
```

```js
/* Üçüncü oturumun sınama koşucusu — radar/matbaa/tren/tamirhane/kargo/
   dedektif/grafik/radarkod/sirik şablonlarını otomatik oynatır.
   Uygulama sayfasının konsolunda:  (0,eval)(await (await fetch('/ucuncu_sinama.js')).text()) */
(function(kok){
'use strict';

/* --- önbelleği kır: şablonun son hâli yüklensin --- */
kok.phaserCerceve = function(g){
  const d = PHASER_OYUNLAR[g.id] || PHASER_TIPLER[g.type];
  return '<iframe class="phaser-cerceve" src="phaser/'+d+'.html?d='+Date.now()+
         '#oyun='+g.id+'" style="width:100%;height:100%;border:0;display:block"></iframe>';
};

/* --- completeGame / hata kaydı --- */
/* Kayıt penceredeki TEK nesne olmalı: sarmalayıcı ilk eval'in kapanışını
   tutuyor, yeniden eval'de yeni bir nesne yaratılırsa bitiş kaydı eskisine
   yazılır ve "bitmedi" görünür (gerçek bir yanılgıydı). */
const KAYIT = kok.__KAYIT || (kok.__KAYIT = { bitti:null, mesaj:null, puan:null, hatalar:[] });
/* Her eval'de yeniden sarıyoruz; özgün işlevi bir kez saklıyoruz. */
if (!kok.__eskiCompleteGame) kok.__eskiCompleteGame = kok.completeGame;
kok.completeGame = function(mesaj, puan){
  const K = kok.__KAYIT;
  K.bitti = true; K.mesaj = mesaj; K.puan = puan;
  return undefined;                         /* uygulamanın akışını çalıştırmıyoruz */
};

const bekle = (ms) => new Promise(r => setTimeout(r, ms));

function cerceve(){ return document.querySelector('iframe.phaser-cerceve'); }

async function ac(id){
  KAYIT.bitti = null; KAYIT.mesaj = null; KAYIT.puan = null; KAYIT.hatalar = [];
  const eskiCerceve = cerceve();
  if (eskiCerceve) eskiCerceve.remove();
  openGame(id);
  let f = null;
  for (let i=0;i<60;i++){ f = cerceve(); if (f && f.contentWindow) break; await bekle(50); }
  if (!f) throw new Error('iframe açılmadı');
  const w = f.contentWindow;
  w.addEventListener('error', e => KAYIT.hatalar.push('hata: '+e.message));
  w.addEventListener('unhandledrejection', e => KAYIT.hatalar.push('reddedildi: '+e.reason));
  /* konsol hatalarını da yakala */
  const ce = w.console.error;
  w.console.error = function(){ KAYIT.hatalar.push('console.error: '+Array.from(arguments).map(String).join(' ')); return ce.apply(this, arguments); };
  for (let i=0;i<300;i++){
    if (w.OYUN && w.OYUN.isBooted && w.OYUN.renderer && w.OYUN.scene && w.OYUN.scene.keys) break;
    await bekle(50);
  }
  if (!w.OYUN) throw new Error('OYUN yok');
  if (!w.OYUN.renderer) throw new Error('render katmanı hazırlanmadı');
  /* Yazı tipi yüklenmeden ölçüm yapılırsa kutular gerçek boyundan küçük
     çıkıyor (elle ilerletmede oyun saati gerçek saatten hızlı akıyor). */
  /* fonts.ready gizli sekmede hiç çözülmeyebiliyor: süre sınırı koy. */
  try{
    await Promise.race([ w.document.fonts.ready, bekle(1500) ]);
  }catch(e){}
  await bekle(120);
  /* ölçek eşlemesini sabitle (gizli iframe 0x0 ölçülebiliyor) */
  try{ const sm = w.OYUN.scale; sm.canvasBounds.x=0; sm.canvasBounds.y=0; sm.displayScale.set(1,1); }catch(e){}
  return w;
}

/* Sahne hazır olana kadar bekle (RAF çalışıyorsa kendiliğinden gelir) */
async function sahne(w, ad, sn){
  ad = ad || 'Game';
  const bit = Date.now() + (sn||6)*1000;
  while (Date.now() < bit){
    const s = w.OYUN.scene.getScene(ad);
    if (s && s.sys && s.sys.isActive() && s.sys.settings.status >= 5) return s;
    await bekle(60);
  }
  return w.OYUN.scene.getScene(ad);
}

/* RAF çalışıyor mu? Çalışmıyorsa elle ilerlet. */
async function rafVarMi(w){
  const a = w.OYUN.loop.frame; await bekle(220);
  return w.OYUN.loop.frame > a;
}
function ilerlet(w, kare, dt){
  const o = w.OYUN; dt = dt || 16;
  if (S_PIN) S_PIN(w);
  let t = o.loop.now || 0;
  for (let i=0;i<kare;i++){ t += dt; o.step(t, dt); }
}

let S_PIN = null;
kok.SINAMA = { ac, sahne, bekle, rafVarMi, ilerlet, KAYIT, cerceve,
  pinKur(f){ S_PIN = f; } };
return 'SINAMA hazır';
})(window);

/* =====================================================================
   catchDrop (radar) otomatik oyuncu
   ===================================================================== */
(function(kok){
'use strict';
const S = kok.SINAMA;

S.oynaCatchDrop = async function(id, sec){
  sec = sec || {};
  const w = await S.ac(id);
  S.ilerlet(w, 12, 16);
  const sc = w.OYUN.scene.getScene('Game');
  const rp = { id, tur:0, turSayisi:null, canKayip:0, yanlisYakalama:[],
    enGenisKapsul:0, kacinilamaz:[], bitti:false, puan:null, hata:[], adim:0, sonuc:null };
  if (!sc || !sc.sys.isActive()){ rp.sonuc='Game sahnesi açılmadı'; rp.hata=S.KAYIT.hatalar.slice(); return rp; }
  try{ rp.turSayisi = w.eval('SORULAR.length'); }catch(e){}

  /* yanlış yakalamayı olay olarak yakala: kenara değme mi, gerçek hata mı? */
  const eskiYanlis = sc.yanlisCevap.bind(sc);
  sc.yanlisCevap = function(kapsul){
    const en = kapsul.getData('en') || kapsul.width;
    rp.yanlisYakalama.push({ tur:sc.soruIndex, metin:kapsul.getData('metin'),
      en:Math.round(en), kapsulX:Math.round(kapsul.x), radarX:Math.round(sc.radar.x),
      fark:Math.round(Math.abs(kapsul.x - sc.radar.x)),
      kacinilabilir: ((kapsul.x - (en/2+60)) >= 70) || ((kapsul.x + (en/2+60)) <= 410) });
    return eskiYanlis(kapsul);
  };

  const gorulen = new Set();
  let sonCan = sc.can, sonIndex = sc.soruIndex;
  const ESIK = 42;                            /* şablondaki YAKALAMA_ESIGI */

  for (let adim = 0; adim < 9000; adim++){
    rp.adim = adim;
    const liste = sc.cevaplar.getChildren().filter(k => k.active);
    let dogru = null;
    liste.forEach(k => {
      const en = k.getData('en') || k.width;
      if (en > rp.enGenisKapsul) rp.enGenisKapsul = en;
      const anahtar = k.getData('metin')+'|'+sc.soruIndex;
      if (!k.getData('dogruMu') && !gorulen.has(anahtar)){
        gorulen.add(anahtar);
        /* kaçınılabilirlik: çekirdek merkezinden ESIK kadar uzaklaşmak
           radarın 70..410 aralığında mümkün mü? */
        if (!((k.x - ESIK - 1) >= 70) && !((k.x + ESIK + 1) <= 410))
          rp.kacinilamaz.push({tur:sc.soruIndex, metin:k.getData('metin'), en:Math.round(en), x:Math.round(k.x)});
      }
      if (k.getData('dogruMu') && !k.getData('yakalandi')) dogru = k;
    });

    /* Çekirdeğin çanak şeridine ne kadar yakın olduğuna bakarak hedef seç. */
    const cekirdekY = (k) => k.y + ((k.getData('boy')||k.height)/2) + 6;
    const yakinYanlis = liste.filter(k => !k.getData('dogruMu') && !k.getData('yakalandi') &&
      cekirdekY(k) > sc.radar.y - 200 && cekirdekY(k) < sc.radar.y + 30);
    let enIyi = sc.hedefX, enIyiSkor = -1e9;
    for (let x = 70; x <= 410; x += 6){
      let ceza = 0;
      yakinYanlis.forEach(k => { const d = Math.abs(k.x - x); if (d <= ESIK + 14) ceza -= (ESIK + 14 - d) * 10; });
      let odul = 0;
      if (dogru) odul = -Math.abs(dogru.x - x) * 0.6;
      const skor = ceza + odul;
      if (skor > enIyiSkor){ enIyiSkor = skor; enIyi = x; }
    }
    sc.hedefX = enIyi;

    S.ilerlet(w, 1, 16);

    if (sc.can < sonCan){ rp.canKayip += (sonCan - sc.can); sonCan = sc.can; }
    if (sc.soruIndex !== sonIndex){ sonIndex = sc.soruIndex; rp.tur = sonIndex; }
    if (S.KAYIT.bitti){ rp.bitti = true; rp.puan = S.KAYIT.puan; break; }
    if (!sc.sys.isActive()){ rp.sonuc = 'sahne değişti (canlar bitti)'; break; }
  }
  rp.hata = S.KAYIT.hatalar.slice();
  rp.can = sc.can;
  if (!rp.sonuc) rp.sonuc = rp.bitti ? 'TAMAM' : 'bitmedi';
  return rp;
};

/* Arka planda koştur: araç çağrısı 30 saniyede zaman aşımına uğruyor,
   bu yüzden toplu koşu beklemeden başlatılıp durumu yoklanıyor. */
S.topluBaslat = function(oyuncu, idler, dosya){
  /* Nesil kilidi: takılan eski bir koşu hâlâ iframe'i değiştiriyorsa iki
     döngü birbirini boğuyordu (sonuç hiç yazılmıyordu). Yeni koşu nesli
     artırır, eskisi ilk adımda kendini durdurur. */
  const nesil = (kok.__TOPLU_NESIL = (kok.__TOPLU_NESIL || 0) + 1);
  const d = { calisiyor:true, biten:[], kalan:idler.slice(), sonuc:[], dosya, nesil };
  kok.__TOPLU = d;
  (async () => {
    for (const id of idler){
      if (kok.__TOPLU_NESIL !== nesil){ d.calisiyor = false; d.durdu = true; return; }
      let r;
      try{ r = await oyuncu(id); }
      catch(e){ r = { id, sonuc:'ÇÖKTÜ: '+e.message, hata:[String(e && e.stack || e)] }; }
      d.sonuc.push(r); d.biten.push(id); d.kalan = d.kalan.filter(x => x !== id);
      if (dosya) try{ await fetch('/kaydet?ad='+dosya+'&tek=1', {method:'POST', body:JSON.stringify(r)+'\n'}); }catch(e){}
    }
    d.calisiyor = false;
  })();
  return 'başladı: '+idler.length+' oyun';
};

S.ozetSatir = (r) => r.id+' → '+r.sonuc+
    (r.canKayip ? ' · can-'+r.canKayip : '') +
    ((r.yanlisYakalama&&r.yanlisYakalama.length) ? ' · yanlış:'+r.yanlisYakalama.length : '') +
    ((r.kacinilamaz&&r.kacinilamaz.length) ? ' · KAÇINILAMAZ:'+r.kacinilamaz.length : '') +
    ((r.hata&&r.hata.length) ? ' · HATA:'+r.hata.length : '');

S.durum = function(){
  const d = kok.__TOPLU || {};
  return { calisiyor:d.calisiyor, biten:(d.biten||[]).length, kalan:(d.kalan||[]).length,
           satir:(d.sonuc||[]).map(S.ozetSatir) };
};

/* Bir liste oyunu sırayla oynat, sonucu sunucuya yaz */
S.toplu = async function(oyuncu, idler, dosya){
  const sonuc = [];
  for (const id of idler){
    let r;
    try{ r = await oyuncu(id); }
    catch(e){ r = { id, sonuc:'ÇÖKTÜ: '+e.message, hata:[String(e && e.stack || e)] }; }
    sonuc.push(r);
  }
  if (dosya) await fetch('/kaydet?ad='+dosya, {method:'POST', body:JSON.stringify(sonuc,null,1)});
  return sonuc.map(r => r.id+' → '+r.sonuc+
    (r.canKayip ? ' · can-'+r.canKayip : '') +
    ((r.yanlisYakalama&&r.yanlisYakalama.length) ? ' · yanlış:'+r.yanlisYakalama.length : '') +
    ((r.kacinilamaz&&r.kacinilamaz.length) ? ' · KAÇINILAMAZ:'+r.kacinilamaz.length : '') +
    ((r.hata&&r.hata.length) ? ' · HATA:'+r.hata.length : ''));
};
})(window);

/* =====================================================================
   Gerçek imleç olayları — dokunma alanlarını da sınar
   ===================================================================== */
(function(kok){
'use strict';
const S = kok.SINAMA;

/* Phaser'ın MouseManager'ı mousedown/mousemove/mouseup dinliyor
   (onPointerDown yok); PointerEvent göndermek hiçbir şey yapmıyordu.
   Ölçek eşlemesi her olaydan ÖNCE sabitleniyor: gizli iframe 103x173
   ölçülüyor ve ScaleManager displayScale'i 9.25'e çekiyor. */
S.pinle = function(w){
  try{
    const sm = w.OYUN.scale;
    sm.canvasBounds.x = 0; sm.canvasBounds.y = 0;
    sm.displayScale.set(1, 1);
  }catch(e){}
};

S.olay = function(w, tur, gx, gy){
  const ad = { pointerdown:'mousedown', pointermove:'mousemove', pointerup:'mouseup' }[tur] || tur;
  const N = S.netlik(w);
  S.pinle(w);
  const e = new w.MouseEvent(ad, {
    clientX: gx * N, clientY: gy * N,
    buttons: (ad === 'mouseup' ? 0 : 1), button: 0,
    bubbles: true, cancelable: true, view: w
  });
  w.OYUN.canvas.dispatchEvent(e);
  S.pinle(w);
};

S.netlik = function(w){ try{ return w.eval('NETLIK'); }catch(e){ return 1; } };
S.pinKur(S.pinle);

/* Bir nesneyi hedefe sürükle: bas → birkaç ara adım → bırak */
S.surukle = function(w, x1, y1, x2, y2, adim){
  adim = adim || 6;
  S.olay(w, 'pointerdown', x1, y1);
  S.ilerlet(w, 2, 16);
  for (let i = 1; i <= adim; i++){
    S.olay(w, 'pointermove', x1 + (x2 - x1) * i / adim, y1 + (y2 - y1) * i / adim);
    S.ilerlet(w, 2, 16);
  }
  S.olay(w, 'pointerup', x2, y2);
  S.ilerlet(w, 3, 16);
};

/* dugmeYap() düğmeleri geri çağrıyı BASMA TWEEN'i bittikten sonra
   çalıştırıyor (scale 0.93, 90ms, yoyo → ~180ms). Kısa ilerletmede tuş
   basılmış ama işlem henüz olmamış görünüyordu ("tuş takımı yazmıyor").
   Bu yüzden bırakmadan sonra tween'i bitirecek kadar ilerletiyoruz. */
S.dokun = function(w, x, y, kare){
  S.olay(w, 'pointerdown', x, y);
  S.ilerlet(w, 3, 16);
  S.olay(w, 'pointerup', x, y);
  S.ilerlet(w, kare == null ? 16 : kare, 16);
};

/* =====================================================================
   sentenceBuild (matbaa) otomatik oyuncu
   ===================================================================== */
S.oynaSentenceBuild = async function(id){
  const w = await S.ac(id);
  S.ilerlet(w, 12, 16);
  const sc = w.OYUN.scene.getScene('Game');
  const rp = { id, tur:0, turSayisi:null, canKayip:0, yanlisBirakma:0,
    kacirilanTutma:0, tasma:[], bitti:false, puan:null, hata:[], sonuc:null };
  if (!sc || !sc.sys.isActive()){ rp.sonuc = 'Game sahnesi açılmadı'; rp.hata = S.KAYIT.hatalar.slice(); return rp; }
  try{ rp.turSayisi = w.eval('TURLAR.length'); }catch(e){}
  const KIZAK_UST = w.eval('KIZAK_UST');

  let sonCan = sc.can, kalkan = 0;

  for (let d = 0; d < 900; d++){
    if (S.KAYIT.bitti){ rp.bitti = true; rp.puan = S.KAYIT.puan; break; }
    if (!sc.sys.isActive()){ rp.sonuc = 'sahne değişti (canlar bitti)'; break; }
    if (sc.kilit){ S.ilerlet(w, 6, 16); continue; }

    const hedefSira = sc.sira;
    const kart = sc.kartlar.getChildren().find(k =>
      k.active && !k.getData('yerlesti') && k.getData('sira') === hedefSira);
    if (!kart){ S.ilerlet(w, 6, 16); if (++kalkan > 300){ rp.sonuc = 'sıradaki kart bulunamadı'; break; } continue; }

    /* kart yerine oturana kadar bekle (havada sürüklemek kayabiliyor) */
    if (kart.body && Math.abs(kart.body.velocity.y) > 12){ S.ilerlet(w, 6, 16); continue; }

    const bx = kart.x, by = kart.y;
    /* Doğru kartı tuttuk mu? Yanlış kart tutulursa masaya geri bırakılır
       (kızağa götürülürse can gider) ve ıskalama sayılır. */
    S.olay(w, 'pointerdown', bx, by);
    S.ilerlet(w, 2, 16);
    if (sc.suruklenen !== kart){
      rp.yanlisTutma = (rp.yanlisTutma || 0) + 1;
      if (sc.suruklenen) rp.yanlisTutmaOrnek = (rp.yanlisTutmaOrnek || []).concat([
        { istenen:kart.getData('kelime'), tutulan:sc.suruklenen.getData('kelime'),
          x:Math.round(bx), y:Math.round(by) }]).slice(0, 6);
      S.olay(w, 'pointerup', bx, by + 40);
      S.ilerlet(w, 4, 16);
      if (rp.yanlisTutma > 40){ rp.sonuc = 'dokunma alanı sürekli komşu kartı tutuyor'; break; }
      continue;
    }
    for (let i = 1; i <= 7; i++){
      S.olay(w, 'pointermove', bx + (EN_OYUN(w)/2 - bx) * i / 7, by + (KIZAK_UST + 26 - by) * i / 7);
      S.ilerlet(w, 2, 16);
    }
    S.olay(w, 'pointerup', EN_OYUN(w) / 2, KIZAK_UST + 26);
    S.ilerlet(w, 3, 16);

    /* Tur geçişi sırasında (kilit) sayma: kartlar yok edilirken hamle
       sonuçsuz görünüyor ama kusur değil. */
    if (sc.sira === hedefSira && !sc.kilit && kart.active){
      if (kart.getData('yerlesti')) { /* olmaz */ }
      else if (sc.can < sonCan){ rp.yanlisBirakma++; sonCan = sc.can; rp.canKayip++; }
      else if (Math.abs(kart.x - bx) < 3 && Math.abs(kart.y - by) < 3){
        rp.kacirilanTutma++;
        rp.iskaOrnek = (rp.iskaOrnek || []).concat([{ kelime:kart.getData('kelime'),
          x:Math.round(bx), y:Math.round(by), tur:sc.tur }]).slice(0, 5);
      }
    }
    if (sc.can < sonCan){ rp.canKayip += (sonCan - sc.can); sonCan = sc.can; }
    if (sc.tur !== rp.tur){
      /* tur bitti: kızaktaki kartlar taşmış mı? */
      rp.tur = sc.tur;
    }
    /* kızak taşması: yerleşmiş kartların kenarları ekran içinde mi? */
    (sc.kizakKartlari || []).forEach(k => {
      const en = k.getData('en') || k.width;
      if (k.x - en/2 < 10 || k.x + en/2 > EN_OYUN(w) - 10)
        rp.tasma.push({ tur:sc.tur, kelime:k.getData('kelime'),
          sol:Math.round(k.x - en/2), sag:Math.round(k.x + en/2) });
    });
    if (rp.kacirilanTutma > 12){ rp.sonuc = 'kart tutulamıyor (dokunma alanı)'; break; }
  }
  rp.hata = S.KAYIT.hatalar.slice();
  rp.can = sc.can;
  if (!rp.sonuc) rp.sonuc = rp.bitti ? 'TAMAM' : 'bitmedi';
  return rp;
};

function EN_OYUN(w){ try{ return w.eval('EN'); }catch(e){ return 480; } }
S.EN_OYUN = EN_OYUN;
})(window);

/* =====================================================================
   punctFix (tamirhane) otomatik oyuncu
   ===================================================================== */
(function(kok){
'use strict';
const S = kok.SINAMA;

S.oynaPunctFix = async function(id){
  const w = await S.ac(id);
  S.ilerlet(w, 14, 16);
  const sc = w.OYUN.scene.getScene('Game');
  const rp = { id, tur:0, turSayisi:null, canKayip:0, bitti:false, puan:null,
    hata:[], sonuc:null, iska:0, tasma:[], ipuc:0 };
  if (!sc || !sc.sys.isActive()){ rp.sonuc = 'Game sahnesi açılmadı'; rp.hata = S.KAYIT.hatalar.slice(); return rp; }
  try{ rp.turSayisi = w.eval('TURLAR.length'); }catch(e){}
  const EN = S.EN_OYUN(w);
  let sonCan = sc.can;

  for (let d = 0; d < 1200; d++){
    if (S.KAYIT.bitti){ rp.bitti = true; rp.puan = S.KAYIT.puan; break; }
    if (!sc.sys.isActive()){ rp.sonuc = 'sahne değişti (canlar bitti)'; break; }
    if (sc.kilit){ S.ilerlet(w, 6, 16); continue; }
    rp.tur = sc.tur;

    /* satır/kutu taşması: sözcük ve yuvalar ekran içinde mi? */
    (sc.sozcukNesne || []).concat(sc.yuvaNesne || []).forEach(o => {
      const en = o.getData ? (o.getData('en') || o.width) : o.width;
      if (o.x - en/2 < 6 || o.x + en/2 > EN - 6 || o.y > 470)
        rp.tasma.push({ tur:sc.tur, x:Math.round(o.x), y:Math.round(o.y), en:Math.round(en) });
    });

    /* 1) büyük harf gerektiren sözcüğe dokun */
    if ((sc.kalanBuyuk || []).length){
      const i = sc.kalanBuyuk[0];
      const c = (sc.sozcukNesne || []).find(o => o.getData('index') === i);
      if (c){ S.dokun(w, c.x, c.y);
        if ((sc.kalanBuyuk || []).indexOf(i) >= 0){ rp.iska++; if (rp.iska > 30){ rp.sonuc='sözcüğe dokunma işlemiyor'; break; } }
        continue; }
    }

    /* 2) işaret gerektiren yuvaya doğru kartı sürükle */
    if ((sc.kalanIsaret || []).length){
      const i = sc.kalanIsaret[0];
      const yuva = (sc.yuvaNesne || []).find(o => o.getData('index') === i && !o.getData('dolu'));
      const gerek = yuva && yuva.getData('gerek');
      const kart = (sc.isaretler ? sc.isaretler.getChildren() : []).find(k =>
        k.active && !k.getData('takildi') && k.getData('isaret') === gerek);
      if (yuva && kart){
        S.surukle(w, kart.x, kart.y, yuva.x, yuva.y, 7);
        if (!yuva.getData('dolu')){ rp.iska++; if (rp.iska > 30){ rp.sonuc='işaret yuvaya takılamıyor'; break; } }
        if (sc.can < sonCan){ rp.canKayip += (sonCan - sc.can); sonCan = sc.can; }
        continue;
      }
      if (!kart){ rp.sonuc = 'sandıkta gereken işaret yok: ' + gerek; break; }
    }
    S.ilerlet(w, 6, 16);
  }
  rp.hata = S.KAYIT.hatalar.slice();
  rp.can = sc.can;
  if (!rp.sonuc) rp.sonuc = rp.bitti ? 'TAMAM' : 'bitmedi';
  return rp;
};
})(window);

/* =====================================================================
   codeGrid (kargo) otomatik oyuncu — BFS ile rota kurup ÇALIŞTIR'a basar
   ===================================================================== */
(function(kok){
'use strict';
const S = kok.SINAMA;

function bfs(t){
  const duvar = new Set((t.duvarlar || []).map(d => d[0] + ',' + d[1]));
  const bas = t.baslangic.join(','), hed = t.hedef.join(',');
  const kuyruk = [[t.baslangic[0], t.baslangic[1], []]];
  const gor = new Set([bas]);
  const yon = [[1,0,'sag'],[-1,0,'sol'],[0,1,'asagi'],[0,-1,'yukari']];
  while (kuyruk.length){
    const [x, y, yol] = kuyruk.shift();
    if (x + ',' + y === hed) return yol;
    for (const [dx, dy, ad] of yon){
      const nx = x + dx, ny = y + dy, k = nx + ',' + ny;
      if (nx < 0 || ny < 0 || nx >= t.sutun || ny >= t.satir) continue;
      if (duvar.has(k) || gor.has(k)) continue;
      gor.add(k); kuyruk.push([nx, ny, yol.concat([ad])]);
    }
  }
  return null;
}

S.oynaCodeGrid = async function(id){
  const w = await S.ac(id);
  S.ilerlet(w, 14, 16);
  const sc = w.OYUN.scene.getScene('Game');
  const rp = { id, tur:0, turSayisi:null, canKayip:0, bitti:false, puan:null,
    hata:[], sonuc:null, tasma:[], blokYetmez:[], cozumsuz:[] };
  if (!sc || !sc.sys.isActive()){ rp.sonuc = 'Game sahnesi açılmadı'; rp.hata = S.KAYIT.hatalar.slice(); return rp; }
  let TURLAR; try{ TURLAR = w.eval('JSON.stringify(TURLAR)'); TURLAR = JSON.parse(TURLAR); }catch(e){ rp.sonuc='TURLAR okunamadı'; return rp; }
  rp.turSayisi = TURLAR.length;
  const EN = S.EN_OYUN(w);
  let sonCan = sc.can, sonTur = -1, dongu = 0;

  while (dongu++ < 400){
    if (S.KAYIT.bitti){ rp.bitti = true; rp.puan = S.KAYIT.puan; break; }
    if (!sc.sys.isActive()){ rp.sonuc = 'sahne değişti (canlar bitti)'; break; }
    if (sc.kilit || sc.calisiyor){ S.ilerlet(w, 8, 16); continue; }
    const tur = sc.tur;
    rp.tur = tur;

    /* ızgara ekrana sığıyor mu? */
    if (tur !== sonTur){
      sonTur = tur;
      const t = TURLAR[tur];
      const H = sc.hucre, sol = sc.izgaraSol, ust = sc.izgaraUst;
      const sag = sol + t.sutun * H, alt = ust + t.satir * H;
      if (sol < 4 || sag > EN - 4 || alt > 530)
        rp.tasma.push({ tur, hucre:H, sol:Math.round(sol), sag:Math.round(sag), alt:Math.round(alt) });

      const yol = bfs(t);
      if (!yol){ rp.cozumsuz.push(tur); rp.sonuc = 'tur ' + tur + ' çözümsüz'; break; }
      if (yol.length > 12){ rp.blokYetmez.push({ tur, gerek:yol.length }); rp.sonuc = 'program şeridi yetmiyor'; break; }
      rp.yol = yol.length;

      /* yön tuşlarına bas: tuşlar EN*(i+0.5)/4, TUS_Y */
      const TUS_Y = w.eval('TUS_Y');
      const sira = ['yukari','sol','sag','asagi'];
      for (const ad of yol){
        const i = sira.indexOf(ad);
        S.dokun(w, EN * (i + 0.5) / 4, TUS_Y);
      }
      if (sc.program.length !== yol.length){
        rp.sonuc = 'yön tuşu işlemiyor (' + sc.program.length + '/' + yol.length + ')';
        break;
      }
      /* ÇALIŞTIR: EN/2+84, TUS_Y+76 */
      S.dokun(w, EN / 2 + 84, TUS_Y + 76);
      if (!sc.calisiyor && sc.tur === tur){
        rp.sonuc = 'ÇALIŞTIR düğmesi işlemiyor';
        break;
      }
    }
    if (sc.can < sonCan){ rp.canKayip += (sonCan - sc.can); sonCan = sc.can; }
    S.ilerlet(w, 10, 16);
  }
  rp.hata = S.KAYIT.hatalar.slice();
  rp.can = sc.can;
  if (!rp.sonuc) rp.sonuc = rp.bitti ? 'TAMAM' : 'bitmedi';
  return rp;
};
})(window);

/* =====================================================================
   wordHighlight (dedektif) otomatik oyuncu
   ===================================================================== */
(function(kok){
'use strict';
const S = kok.SINAMA;

S.oynaWordHighlight = async function(id){
  const w = await S.ac(id);
  S.ilerlet(w, 14, 16);
  const sc = w.OYUN.scene.getScene('Game');
  const rp = { id, tur:0, turSayisi:null, canKayip:0, bitti:false, puan:null,
    hata:[], sonuc:null, tasma:[], eslesmeyen:[] };
  if (!sc || !sc.sys.isActive()){ rp.sonuc = 'Game sahnesi açılmadı'; rp.hata = S.KAYIT.hatalar.slice(); return rp; }
  let TURLAR; try{ TURLAR = JSON.parse(w.eval('JSON.stringify(TURLAR)')); }catch(e){ rp.sonuc='TURLAR okunamadı'; return rp; }
  rp.turSayisi = TURLAR.length;
  const anahtar = (m) => w.eval('anahtar')(m);
  const EN = S.EN_OYUN(w);
  let sonCan = sc.can;

  for (let d = 0; d < 900; d++){
    if (S.KAYIT.bitti){ rp.bitti = true; rp.puan = S.KAYIT.puan; break; }
    if (!sc.sys.isActive()){ rp.sonuc = 'sahne değişti (canlar bitti)'; break; }
    if (sc.kilit){ S.ilerlet(w, 8, 16); continue; }
    rp.tur = sc.tur;

    /* sözcük kartları kâğıdın içinde mi? */
    (sc.sozcukNesne || []).forEach(o => {
      const en = o.getData('en') || o.width;
      if (o.x - en/2 < 8 || o.x + en/2 > EN - 8)
        rp.tasma.push({ tur:sc.tur, kelime:o.getData('kelime'), x:Math.round(o.x), en:Math.round(en) });
    });

    const kalan = (sc.kalan || []).slice();
    if (!kalan.length){ S.ilerlet(w, 8, 16); continue; }
    const hedef = (sc.sozcukNesne || []).find(o => !o.getData('bulundu') &&
      kalan.some(x => anahtar(x) === anahtar(o.getData('kelime'))));
    if (!hedef){
      rp.eslesmeyen.push({ tur:sc.tur, kalan });
      rp.sonuc = 'cevap metinde bulunamıyor: ' + kalan.join(', ');
      break;
    }
    S.dokun(w, hedef.x, hedef.y);
    if (sc.can < sonCan){ rp.canKayip += (sonCan - sc.can); sonCan = sc.can; }
    S.ilerlet(w, 4, 16);
  }
  rp.hata = S.KAYIT.hatalar.slice();
  rp.can = sc.can;
  if (!rp.sonuc) rp.sonuc = rp.bitti ? 'TAMAM' : 'bitmedi';
  return rp;
};
})(window);

/* =====================================================================
   jumpPath (sirik) · numPad (radarkod) · graphBuild (grafik) oyuncuları
   ===================================================================== */
(function(kok){
'use strict';
const S = kok.SINAMA;

S.oynaJumpPath = async function(id){
  const w = await S.ac(id);
  S.ilerlet(w, 14, 16);
  const sc = w.OYUN.scene.getScene('Game');
  const rp = { id, adim:0, adimSayisi:null, canKayip:0, bitti:false, puan:null,
    hata:[], sonuc:null, tasma:[], hedefYok:[] };
  if (!sc || !sc.sys.isActive()){ rp.sonuc='Game sahnesi açılmadı'; rp.hata=S.KAYIT.hatalar.slice(); return rp; }
  let ADIMLAR; try{ ADIMLAR = JSON.parse(w.eval('JSON.stringify(ADIMLAR)')); }catch(e){ rp.sonuc='ADIMLAR okunamadı'; return rp; }
  rp.adimSayisi = ADIMLAR.length;
  const EN = S.EN_OYUN(w), BOY = w.eval('BOY');
  let sonCan = sc.can;

  for (let d = 0; d < 900; d++){
    if (S.KAYIT.bitti){ rp.bitti = true; rp.puan = S.KAYIT.puan; break; }
    if (!sc.sys.isActive()){ rp.sonuc='sahne değişti (canlar bitti)'; break; }
    if (sc.kilit || sc.uctu){ S.ilerlet(w, 8, 16); continue; }
    rp.adim = sc.adim;

    /* yapraklar ekran içinde mi? */
    (sc.yaprakNesne || []).forEach(o => {
      if (o.x < 14 || o.x > EN - 14 || o.y < 40 || o.y > BOY - 20)
        rp.tasma.push({ id:o.getData('id'), x:Math.round(o.x), y:Math.round(o.y) });
    });

    const a = ADIMLAR[sc.adim];
    if (!a){ S.ilerlet(w, 8, 16); continue; }
    const hedef = (sc.yaprakNesne || []).find(o => o.getData('id') === a.hedef);
    if (!hedef){ rp.hedefYok.push({ adim:sc.adim, hedef:a.hedef }); rp.sonuc='hedef yaprak yok: '+a.hedef; break; }
    S.dokun(w, hedef.x, hedef.y);
    if (sc.can < sonCan){ rp.canKayip += (sonCan - sc.can); sonCan = sc.can; }
    S.ilerlet(w, 30, 16);
  }
  rp.hata = S.KAYIT.hatalar.slice();
  rp.can = sc.can;
  if (!rp.sonuc) rp.sonuc = rp.bitti ? 'TAMAM' : 'bitmedi';
  return rp;
};

S.oynaNumPad = async function(id){
  const w = await S.ac(id);
  S.ilerlet(w, 14, 16);
  const sc = w.OYUN.scene.getScene('Game');
  const rp = { id, tur:0, turSayisi:null, canKayip:0, bitti:false, puan:null,
    hata:[], sonuc:null, basamakYetmez:[], kartTasma:[] };
  if (!sc || !sc.sys.isActive()){ rp.sonuc='Game sahnesi açılmadı'; rp.hata=S.KAYIT.hatalar.slice(); return rp; }
  let TURLAR, AZAMI, EN, TUS_UST, TUS_ARA, TUP_X, TUP_EN;
  try{
    TURLAR = JSON.parse(w.eval('JSON.stringify(TURLAR)'));
    AZAMI = w.eval('AZAMI_BASAMAK'); EN = w.eval('EN');
    TUS_UST = w.eval('TUS_UST'); TUS_ARA = w.eval('TUS_ARA');
    TUP_X = w.eval('TUP_X'); TUP_EN = w.eval('TUP_EN');
  }catch(e){ rp.sonuc='sabitler okunamadı: '+e.message; return rp; }
  rp.turSayisi = TURLAR.length;
  const tusYeri = (d) => {
    if (d === 0) return { x: EN/2 - 118, y: TUS_UST + 3*TUS_ARA };
    const i = d - 1;
    return { x: EN/2 - 118 + (i % 3) * 118, y: TUS_UST + Math.floor(i / 3) * TUS_ARA };
  };
  const gir = { x: EN/2 + 118, y: TUS_UST + 3*TUS_ARA };
  let sonCan = sc.can;

  for (let d = 0; d < 400; d++){
    if (S.KAYIT.bitti){ rp.bitti = true; rp.puan = S.KAYIT.puan; break; }
    if (!sc.sys.isActive()){ rp.sonuc='sahne değişti (canlar bitti)'; break; }
    if (sc.kilit){ S.ilerlet(w, 8, 16); continue; }
    const t = TURLAR[sc.tur];
    if (!t){ S.ilerlet(w, 8, 16); continue; }
    rp.tur = sc.tur;
    const cevap = String(t.cevap);
    if (cevap.length > AZAMI){
      rp.basamakYetmez.push({ tur:sc.tur, cevap, azami:AZAMI });
      rp.sonuc = 'cevap tuşlanamıyor: ' + cevap + ' (' + AZAMI + ' basamak sınırı)';
      break;
    }
    /* önce ekranı temizle (SİL çalışmazsa sonsuz döngüye girmesin) */
    let sil = 0;
    while (sc.girilen.length && sil++ < 12) S.dokun(w, EN/2, TUS_UST + 3*TUS_ARA, 5);
    if (sc.girilen.length){ rp.sonuc = 'SİL tuşu işlemiyor'; break; }
    /* Basamakları TEK TEK bas ve her birinin işlediğini doğrula: aynı tuşa
       üst üste basılınca bir basış yutulabiliyor (düğme basma tween'i). */
    let kayip = 0;
    for (const ch of cevap){
      const p = tusYeri(Number(ch));
      const onceki = sc.girilen.length;
      for (let deneme = 0; deneme < 4 && sc.girilen.length === onceki; deneme++){
        S.dokun(w, p.x, p.y, 5);
        if (sc.girilen.length === onceki) kayip++;
      }
      if (sc.girilen.length === onceki){
        rp.sonuc = 'tuş işlemiyor: ' + ch;
        break;
      }
    }
    rp.yutulanBasis = (rp.yutulanBasis || 0) + kayip;
    if (rp.sonuc) break;
    if (sc.girilen.join('') !== cevap){
      rp.sonuc = 'tuş takımı yazmıyor: ' + sc.girilen.join('') + ' ≠ ' + cevap;
      break;
    }
    /* rakam kartları tüpün içinde mi? */
    (sc.rakamlar ? sc.rakamlar.getChildren() : []).forEach(c => {
      if (c.x < TUP_X - TUP_EN/2 + 2 || c.x > TUP_X + TUP_EN/2 - 2)
        rp.kartTasma.push({ tur:sc.tur, x:Math.round(c.x), sinir:[Math.round(TUP_X-TUP_EN/2), Math.round(TUP_X+TUP_EN/2)] });
    });
    S.dokun(w, gir.x, gir.y);
    if (sc.can < sonCan){ rp.canKayip += (sonCan - sc.can); sonCan = sc.can; }
    S.ilerlet(w, 16, 16);
    await S.bekle(0);
  }
  rp.hata = S.KAYIT.hatalar.slice();
  rp.can = sc.can;
  if (!rp.sonuc) rp.sonuc = rp.bitti ? 'TAMAM' : 'bitmedi';
  return rp;
};

S.oynaGraphBuild = async function(id){
  const w = await S.ac(id);
  S.ilerlet(w, 20, 16);
  const sc = w.OYUN.scene.getScene('Game');
  const rp = { id, canKayip:0, bitti:false, puan:null, hata:[], sonuc:null,
    tasma:[], blokYok:[], hedefler:null };
  if (!sc || !sc.sys.isActive()){ rp.sonuc='Game sahnesi açılmadı'; rp.hata=S.KAYIT.hatalar.slice(); return rp; }
  let KAT, TABAN_Y, BLOK_BOY, AZAMI;
  try{
    KAT = JSON.parse(w.eval('JSON.stringify(KATEGORILER)'));
    TABAN_Y = w.eval('TABAN_Y'); BLOK_BOY = w.eval('BLOK_BOY'); AZAMI = w.eval('AZAMI');
  }catch(e){ rp.sonuc='sabitler okunamadı: '+e.message; return rp; }
  rp.hedefler = KAT.map(k => k.hedef);
  /* sütun kapasitesi hedefi karşılıyor mu? */
  KAT.forEach((k, i) => { if (k.hedef > AZAMI) rp.tasma.push({ kategori:k.ad, hedef:k.hedef, kapasite:AZAMI }); });
  let sonCan = sc.can, bosDongu = 0;

  for (let d = 0; d < 700; d++){
    if (S.KAYIT.bitti){ rp.bitti = true; rp.puan = S.KAYIT.puan; break; }
    if (!sc.sys.isActive()){ rp.sonuc='sahne değişti (canlar bitti)'; break; }
    if (sc.kilit){ S.ilerlet(w, 8, 16); continue; }

    /* eksik sütun bul, o kategoriden bir blok sürükle */
    let si = -1;
    for (let i = 0; i < KAT.length; i++) if (sc.sayac[i] < KAT[i].hedef){ si = i; break; }
    if (si < 0){ S.ilerlet(w, 10, 16); if (++bosDongu > 40){ rp.sonuc='hedefler tuttu ama oyun bitmedi'; break; } continue; }

    const blok = (sc.bloklar ? sc.bloklar.getChildren() : []).find(b =>
      b.active && !b.getData('yerlesti') && b.getData('kat') === si);
    if (!blok){ rp.blokYok.push({ kategori:KAT[si].ad }); rp.sonuc='depoda '+KAT[si].ad+' bloğu kalmadı'; break; }

    const hy = TABAN_Y - sc.sayac[si] * BLOK_BOY - BLOK_BOY / 2;
    S.surukle(w, blok.x, blok.y, sc.sutunX(si), Math.max(hy, TABAN_Y - AZAMI * BLOK_BOY + 10), 7);
    if (sc.can < sonCan){ rp.canKayip += (sonCan - sc.can); sonCan = sc.can; }
    S.ilerlet(w, 12, 16);
  }
  rp.hata = S.KAYIT.hatalar.slice();
  rp.can = sc.can;
  rp.sayac = sc.sayac;
  if (!rp.sonuc) rp.sonuc = rp.bitti ? 'TAMAM' : 'bitmedi';
  return rp;
};
})(window);

/* =====================================================================
   dragSlider (tren) otomatik oyuncu
   ===================================================================== */
(function(kok){
'use strict';
const S = kok.SINAMA;

S.oynaDragSlider = async function(id){
  const w = await S.ac(id);
  S.ilerlet(w, 14, 16);
  const sc = w.OYUN.scene.getScene('Game');
  const rp = { id, tur:0, turSayisi:null, canKayip:0, bitti:false, puan:null,
    hata:[], sonuc:null, etiketTasma:[], hedefYok:[], etiketOrnek:[] };
  if (!sc || !sc.sys.isActive()){ rp.sonuc='Game sahnesi açılmadı'; rp.hata=S.KAYIT.hatalar.slice(); return rp; }
  let TURLAR; try{ TURLAR = JSON.parse(w.eval('JSON.stringify(TURLAR)')); }catch(e){ rp.sonuc='TURLAR okunamadı: '+e.message; return rp; }
  rp.turSayisi = TURLAR.length;
  const EN = S.EN_OYUN(w);
  let sonCan = sc.can, sonTur = -1;

  for (let d = 0; d < 700; d++){
    if (S.KAYIT.bitti){ rp.bitti = true; rp.puan = S.KAYIT.puan; break; }
    if (!sc.sys.isActive()){ rp.sonuc='sahne değişti (canlar bitti)'; break; }
    if (sc.kilit){ S.ilerlet(w, 8, 16); if ((d & 7) === 0) await S.bekle(0); continue; }
    const t = TURLAR[sc.tur];
    if (!t){ S.ilerlet(w, 8, 16); await S.bekle(0); continue; }
    rp.tur = sc.tur;

    if (sc.tur !== sonTur){
      sonTur = sc.tur;
      /* tünel etiketleri komşusuna binmiyor mu? */
      const W = Math.min(128, EN / t.duraklar.length - 10);
      (sc.tunelGorsel || []).forEach(o => {
        if (o.type === 'Text' && o.width > W - 4)
          rp.etiketTasma.push({ tur:sc.tur, metin:o.text, en:Math.round(o.width), tunel:Math.round(W) });
      });
      /* etiketler gerçekten katalogdaki label'ı gösteriyor mu? */
      const etiketler = (sc.tunelGorsel || []).filter(o => o.type === 'Text').map(o => o.text);
      if (rp.etiketOrnek.length < 2) rp.etiketOrnek.push({ tur:sc.tur, etiketler, beklenen:t.duraklar.map(x => x.etiket) });
    }

    /* hedef durağı bul (tolerans içinde en yakın) */
    let si = -1;
    for (let i = 0; i < t.duraklar.length; i++){
      if (Math.abs(t.duraklar[i].deger - t.hedef) <= (t.tolerans || 0)){ si = i; break; }
    }
    if (si < 0){ rp.hedefYok.push({ tur:sc.tur, hedef:t.hedef }); rp.sonuc='hedef durak listede yok: '+t.hedef; break; }

    /* kolu o durağa taşı (kızağa dokunmak yeterli) */
    const KOL_Y = w.eval('KOL_Y');
    S.dokun(w, sc.durakX[si], KOL_Y - 10, 4);
    if (sc.secili !== si){
      rp.sonuc = 'makas kolu taşınmıyor: ' + sc.secili + ' ≠ ' + si;
      break;
    }
    S.ilerlet(w, 20, 16);
    /* ONAYLA: EN/2, 682 */
    S.dokun(w, EN / 2, 682, 8);
    S.ilerlet(w, 80, 16);
    if (sc.can < sonCan){ rp.canKayip += (sonCan - sc.can); sonCan = sc.can; }
    await S.bekle(0);
  }
  rp.hata = S.KAYIT.hatalar.slice();
  rp.can = sc.can;
  if (!rp.sonuc) rp.sonuc = rp.bitti ? 'TAMAM' : 'bitmedi';
  return rp;
};
})(window);

/* =====================================================================
   Ekran görüntüsü: tuvali sunucuya PNG olarak yazdır
   ===================================================================== */
(function(kok){
'use strict';
const S = kok.SINAMA;
S.goruntuAl = async function(ad){
  const f = S.cerceve(); if (!f) return 'iframe yok';
  const w = f.contentWindow;
  try{
    /* WebGL tuvalinde preserveDrawingBuffer kapalı olabilir: kareyi
       yeniden çizdirip hemen okuyoruz. */
    w.OYUN.renderer.snapshot(() => {});
    S.ilerlet(w, 1, 16);
    const veri = w.OYUN.canvas.toDataURL('image/png');
    await fetch('/kaydet?ad=' + ad + '.b64', { method:'POST', body:veri });
    return 'yazıldı: ' + ad + ' (' + veri.length + ' bayt)';
  }catch(e){ return 'hata: ' + e.message; }
};
})(window);
```
