# Macera Akademi — Phaser şablonu kuralları

Bu dosya, **kataloğa bağlanmamış Phaser şablonlarını** bağlayacak oturum içindir.
Kurallar deneyle çıkarıldı; her biri gerçek bir hatanın karşılığıdır.

## 0. Dosya sahipliği (ÇAKIŞMAYI ÖNLER)

**Bu oturumun DOKUNABİLECEĞİ dosyalar:**

    ~/Downloads/rakam-phaser.html        (numberTrace, numberWrite)
    ~/Downloads/oruntu-phaser.html       (patternFill)
    ~/Downloads/terazi-phaser.html       (balanceScale)
    ~/Downloads/cetele-phaser.html       (tallyChart, surveyChart)
    ~/Downloads/paketleme-phaser.html    (countToTarget)
    ~/Downloads/para-phaser.html         (moneyPay / para oyunları)
    ~/Downloads/kesirsaat-phaser.html    (clockRead / kesir-saat)
    ~/Downloads/geometri-phaser.html     (shapeBuild)
    ~/Downloads/simetri-phaser.html      (symmetryDraw)
    ~/Downloads/daktilo-phaser.html      (typeWord)
    ~/Downloads/kronometre-phaser.html   (timeEstimate)

### Üç oturumun bölüşümü

| Oturum | Dosyalar |
|---|---|
| 1 (uygulama) | `macera-akademi-firebase-11.html`, `svgciz.js`, bant, kopru, lazer, balik, kavanoz, roket, hafiza, pizza, uzamsal |
| 2 (bağlanmamış şablonlar) | rakam, oruntu, terazi, cetele, paketleme, para, kesirsaat, geometri, simetri, daktilo, kronometre |
| 3 (bağlı ama test edilmemiş) | radar, matbaa, tren, tamirhane, kargo, dedektif, grafik, radarkod, sirik |

Portlar: 1 → 8866/8867, 2 → 8870, 3 → 8880.

**ASLA DOKUNULMAYACAK dosyalar** (diğer oturum üzerinde çalışıyor):

    macera-akademi-firebase-11.html      ← uygulama + katalog
    svgciz.js
    bant / kopru / lazer / balik / kavanoz / roket / hafiza / pizza / uzamsal / radar /
    matbaa / tren / tamirhane / kargo / dedektif / grafik / radarkod / sirik  (-phaser.html)

Kataloğa alan eklenmesi gerekiyorsa **dosyayı düzenleme**; gereksinimi
`~/Downloads/katalog_istekleri.md` dosyasına yaz, diğer oturum uygular.

## 1. Şablonun kataloğa bağlanması

Her şablonun başına bu köprü eklenir (bant-phaser.html'den birebir alınabilir):

```js
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
        oku(metin){ try{ if (window.parent.oku) window.parent.oku(metin); }catch(e){} },
        atla(){ try{ if (window.parent.sonrakiOyunaGec) window.parent.sonrakiOyunaGec(); }catch(e){} }
      };
    }
  }catch(e){}
  return null;
})();

const CFG = KOPRU ? KOPRU.cfg : VARSAYILAN;   /* VARSAYILAN: şablonun kendi demo verisi */
```

Kurallar:
- `Boot` sahnesi `scene.start(KOPRU ? 'Game' : 'Menu')` yapar — köprü varsa menü atlanır.
- Kazanınca **mutlaka** `KOPRU.bitir(BASARI, this.puan)` çağrılır, `return` ile çıkılır.
- MENÜ düğmesi yalnız `!KOPRU` iken görünür.
- Kaybetme ekranında "⏭ SIRADAKİ OYUN" düğmesi `KOPRU.atla()` çağırır.
- Sahne anahtarı **`Game`** olmalı (otomatik test bunu arıyor).

## 2. Metin temizleme (varlık çözme ŞART)

```js
function varlikCoz(m){
  return String(m)
    .replace(/&nbsp;/gi,' ').replace(/&lt;/gi,'<').replace(/&gt;/gi,'>')
    .replace(/&quot;/gi,'"').replace(/&#39;|&apos;/gi,"'")
    .replace(/&hellip;/gi,'…').replace(/&mdash;/gi,'—').replace(/&ndash;/gi,'–')
    .replace(/&times;/gi,'×').replace(/&divide;/gi,'÷').replace(/&deg;/gi,'°')
    .replace(/&rarr;/gi,'→').replace(/&larr;/gi,'←').replace(/&amp;/gi,'&');
}
function duzMetin(x){
  return varlikCoz(String(x == null ? '' : x).replace(/<br\s*\/?>/gi,' ')
    .replace(/<[^>]+>/g,'')).replace(/[“”]/g,'"').replace(/\s+/g,' ').trim();
}
```
Yapılmazsa ekranda `Pay &lt; payda` yazar (gerçek hata, düzeltildi).

## 3. Satır içi SVG içeriği

Katalogda bazı görseller `<svg>` metni olarak duruyor (`svg`, `emoji`, `label`, `b`, `prompt`
alanlarında). Metne çevirince kaybolur. Çizmek için:

```html
<script src="svgciz.js"></script>
```
```js
function svgAl(o){
  if (!o || !window.SVGCIZ) return null;
  const alanlar = ['svg','emoji','label','b','prompt'];
  for (let i=0;i<alanlar.length;i++) if (SVGCIZ.svgMi(o[alanlar[i]])) return o[alanlar[i]];
  return null;
}
const kap = SVGCIZ.ciz(this, cizim, x, y, boy, { metin:false, en:genislik, zemin:true, pay:5 });
```
- `zemin:true` → arkasına açık plaka koyar (katalog SVG'leri koyu zeminde görünmez).
- `en` verilirse dikdörtgen kutuya sığdırır, oranı korur.
- `metin:false` → SVG'den sonraki düz metni çizmez (mekanik zaten etiketi yazıyorsa).
- Kabın `width/height` değeri gerçek çizim ölçüsüdür; yerleşimi ona göre yap.

## 4. Netlik (bulanıklık önleme)

Bağlı şablonların hepsinde bulunan `NETLIK` bloğu birebir kopyalanır: oyun boyutu
DPR ile çarpılır, kamera zoom'lanır, `TextStyle.setStyle` çözünürlük yaması ve
`imlec(p)` imleç dönüşümü eklenir. Kopyalamazsan yazılar bulanık çıkar.
`this.input.on('pointerdown', p => ...)` içinde **her zaman** `imlec(p)` kullan —
ham `p.x` NETLIK katıyla ölçeklidir.

## 5. Tekrarlayan tuzaklar (hepsi gerçek hataydı)

- **Container tıklama alanı**: `setSize(W,H)` + argümansız `setInteractive()` kullan.
  `setInteractive(new Phaser.Geom.Rectangle(-W/2,-H/2,W,H), ...)` alanı kaydırır.
- **Arcade grup**: gövde ayarlarından ÖNCE `grup.add(nesne)` yap; grup kendi
  varsayılanlarını gövdeye basıyor.
- **overlap(grup, tekNesne)** callback parametrelerini ters verir; tek nesneyi de
  bir staticGroup içine koy.
- **Kenara değmek = yakalamak değil**: örtüşme ile karar verme; merkeze en yakın
  hedefi seç ve bir eşik koy (balık ve bant şablonlarında böyle çözüldü).
- **Üst üste binme**: kutuların/kartların ölçüsünü yazının GERÇEK ölçüsünden hesapla,
  önce ölç sonra yerleştir. Eşit aralık varsayma.
- **Devanagari rakam tuzağı**: `0x2f3b४6` gibi bir hex yazımı sessizce bozar; hex
  sabitlerini gözle kontrol et.

## 6. Test yöntemi (zorunlu)

1. Sunucu: `cd ~/Downloads && python3 -m http.server 8870`
2. Uygulamayı aç: `http://localhost:8870/MaceraAkademi-3/app/src/main/assets/macera-akademi.html`
3. Konsolda önbelleği kırarak oyunu aç:
   ```js
   window.phaserCerceve = function(g){
     const d = PHASER_OYUNLAR[g.id] || PHASER_TIPLER[g.type];
     return '<iframe class="phaser-cerceve" src="phaser/'+d+'.html?d='+Date.now()+
            '#oyun='+g.id+'" style="width:100%;height:100%;border:0;display:block"></iframe>';
   };
   openGame('s0');
   ```
4. Sayfa gizliyken Phaser'ın saati durur. Elle ilerlet:
   ```js
   const o = document.querySelector('iframe').contentWindow.OYUN;
   let t=0; for(let i=0;i<240;i++){ t+=16; o.step(t,16); }
   ```
5. **Tween'ler duvar saatiyle ilerler.** Phaser 3.80'de TweenManager gerçek
   zamanı kullanıyor; `game.step()` çağırmak tween'i ilerletmez. Kazanma
   zinciri genelde `tween.onComplete → time.delayedCall → bitir()` biçiminde
   olduğu için, senkron adım atarak test edersen oyun "bitmedi" görünür.
   Animasyon bekleyen her yerde GERÇEK zaman bekle:

   ```js
   const bekle = (ms) => new Promise(c => { const b=Date.now();
     (function tik(){ adimAt(4); if (Date.now()-b>=ms) return c(); setTimeout(tik,40); })(); });
   ```

   Hazır koşum: `~/Downloads/kosum.js` (fetch + eval ile yüklenir; `KOSUM.kur()`,
   `KOSUM.sirala([...])`, `KOSUM.ozet()`). İçinde loop.delta düzeltmesi,
   gerçek zamanlı bekleme, ölçek eşlemesi ve sekiz mekanik için oynayıcı var.

6. Fare olayı gönderirken iframe 0×0 ölçülebilir; ölçek eşlemesini sabitle:
   ```js
   const sm=o.scale; sm.canvasBounds.x=0; sm.canvasBounds.y=0; sm.displayScale.set(1,1);
   /* sonra clientX = oyunX * kamerazoom */
   ```
7. Her oyun **baştan sona oynanmalı** ve `completeGame` çağrısı görülmelidir.
   "Açılıyor" yeterli değildir.

## 8. Varlıklara kopyalama

Şablonu düzenledikten sonra:

    ~/Downloads/aynala.sh

CDN bağlantısını yerele çevirir, `svgciz.js`'e sürüm damgası basar ve
`MaceraAkademi-3/app/src/main/assets/` altına kopyalar.

## 9. Yeni mekaniği uygulamaya tanıtma

`macera-akademi-firebase-11.html` içindeki `PHASER_TIPLER` eşlemesine satır eklenmeli.
**Bunu sen yapma** — `katalog_istekleri.md` dosyasına şu biçimde yaz:

    PHASER_TIPLER += numberTrace:'rakam', numberWrite:'rakam'
