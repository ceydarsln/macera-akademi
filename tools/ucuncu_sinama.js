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
/* Her eval'de yeniden sarıyoruz; özgün işlevi bir kez saklıyoruz. KOSUM
   da aynı sayfada yüklüyse iki kayıt kanalını birlikte besliyoruz. */
if (!kok.__maceraTestCompleteAsil) kok.__maceraTestCompleteAsil = kok.completeGame;
if (!kok.__eskiCompleteGame) kok.__eskiCompleteGame = kok.__maceraTestCompleteAsil;
kok.completeGame = function(mesaj, puan){
  const K = kok.__KAYIT;
  K.bitti = true; K.mesaj = mesaj; K.puan = puan;
  if (!Array.isArray(kok.__bildirim)) kok.__bildirim = [];
  kok.__bildirim.push({ mesaj:String(mesaj), puan });
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
   Sonradan kataloğa bağlanan mekanikler
   fractionCut · clockSet · moneyBuild · placeValueLoad · drawSegments · solidScan
   ===================================================================== */
(function(kok){
'use strict';
const S = kok.SINAMA;

async function oyunHazir(id){
  const w = await S.ac(id);
  S.ilerlet(w, 30, 16);
  const sc = w.OYUN.scene.getScene('Game');
  if (!sc || !sc.sys || !sc.sys.isActive()) throw new Error('Game sahnesi açılmadı');
  return { w, sc };
}

function rapor(id, sc, ek){
  const bitti = !!S.KAYIT.bitti;
  return Object.assign({
    id, bitti, puan:S.KAYIT.puan, can:sc && sc.can,
    hata:S.KAYIT.hatalar.slice(), sonuc:bitti ? 'TAMAM' : 'bitmedi'
  }, ek || {});
}

S.oynaFractionCut = async function(id){
  const { w, sc } = await oyunHazir(id);
  let hamle = 0, not = '';
  for (let d = 0; d < 600 && !S.KAYIT.bitti; d++){
    if (!sc.sys.isActive()){ not = 'Game sahnesi kapandı'; break; }
    if (sc.kilit){ S.ilerlet(w, 12, 16); continue; }
    const t = sc.aktifTur, a = t && t.adimlar && t.adimlar[sc.adim];
    if (!a){ S.ilerlet(w, 12, 16); continue; }
    sc.kes(t, a.gerek); hamle++;
    S.ilerlet(w, 20, 16);
  }
  const r = rapor(id, sc, { hamle, not });
  if (!r.bitti && not) r.sonuc = not;
  return r;
};

S.oynaClockSet = async function(id){
  const { w, sc } = await oyunHazir(id);
  let onay = 0, ayar = 0, not = '';
  for (let d = 0; d < 900 && !S.KAYIT.bitti; d++){
    if (!sc.sys.isActive()){ not = 'Game sahnesi kapandı'; break; }
    if (sc.kilit){ S.ilerlet(w, 12, 16); continue; }
    const t = sc.aktifTur, a = t && t.adimlar && t.adimlar[sc.adim];
    if (!a){ S.ilerlet(w, 12, 16); continue; }
    let koruma = 0;
    while (sc.saat !== a.saat && koruma++ < 12){ sc.saatAyar(t, 1, 0); ayar++; }
    koruma = 0;
    while (sc.dakika !== a.dakika && koruma++ < 4){ sc.saatAyar(t, 0, 15); ayar++; }
    if (sc.saat !== a.saat || sc.dakika !== a.dakika){ not = 'hedef saat ayarlanamadı'; break; }
    sc.saatOnay(t); onay++;
    S.ilerlet(w, 20, 16);
  }
  const r = rapor(id, sc, { onay, ayar, not });
  if (!r.bitti && not) r.sonuc = not;
  return r;
};

S.oynaValueBuild = async function(id){
  const { w, sc } = await oyunHazir(id);
  let eklenen = 0, not = '';
  for (let d = 0; d < 900 && !S.KAYIT.bitti; d++){
    if (!sc.sys.isActive()){ not = 'Game sahnesi kapandı'; break; }
    if (sc.kilit){ S.ilerlet(w, 12, 16); continue; }
    const t = sc.aktifTur;
    if (!t){ not = 'aktif tur yok'; break; }
    const kalan = t.hedef - sc.toplam;
    if (kalan <= 0){ S.ilerlet(w, 12, 16); continue; }
    let ix = -1, deger = -1;
    t.jetonlar.forEach((j, i) => { if (j.deger <= kalan && j.deger > deger){ ix = i; deger = j.deger; } });
    if (ix < 0){ not = 'hedef kalanını oluşturan jeton yok: ' + kalan; break; }
    const once = sc.toplam;
    sc.tut(ix);
    if (!sc.tasinan){ not = 'jeton raftan alınamadı'; break; }
    sc.birak();
    for (let i = 0; i < 80 && sc.toplam === once && !sc.kilit; i++) S.ilerlet(w, 2, 16);
    if (sc.toplam === once && !sc.kilit){ not = 'jeton kaba düşmedi: ' + deger; break; }
    eklenen++;
  }
  const r = rapor(id, sc, { eklenen, toplam:sc.toplam, not });
  if (!r.bitti && not) r.sonuc = not;
  return r;
};

S.oynaDrawSegments = async function(id){
  const { w, sc } = await oyunHazir(id);
  let cizgi = 0, not = '';
  for (let d = 0; d < 1200 && !S.KAYIT.bitti; d++){
    if (!sc.sys.isActive()){ not = 'Game sahnesi kapandı'; break; }
    if (sc.kilit){ S.ilerlet(w, 12, 16); continue; }
    const t = sc.aktifTur;
    const cift = t && t.gerekli && t.gerekli.find(g =>
      !(sc.cizilen || []).some(x => (x[0] === g[0] && x[1] === g[1]) || (x[0] === g[1] && x[1] === g[0])));
    if (!cift){ S.ilerlet(w, 12, 16); continue; }
    const bul = ad => (sc.koseNesne || []).find(o => o && o.getData && o.getData('ad') === ad);
    const a = bul(cift[0]), b = bul(cift[1]);
    if (!a || !b){ not = 'çizgi noktası bulunamadı: ' + cift.join('–'); break; }
    sc.koseSec(t, a); sc.koseSec(t, b); cizgi++;
    S.ilerlet(w, 10, 16);
  }
  const r = rapor(id, sc, { cizgi, not });
  if (!r.bitti && not) r.sonuc = not;
  return r;
};

S.oynaSolidScan = async function(id){
  const { w, sc } = await oyunHazir(id);
  let taranan = 0, not = '';
  for (let d = 0; d < 1600 && !S.KAYIT.bitti; d++){
    if (!sc.sys.isActive()){ not = 'Game sahnesi kapandı'; break; }
    if (sc.kilit){ S.ilerlet(w, 12, 16); continue; }
    const t = sc.aktifTur;
    const oge = (sc.ogeNesne || []).find(o => o && o.getData && !o.getData('tarandi'));
    if (!oge){ S.ilerlet(w, 12, 16); continue; }
    sc.ogeTara(t, oge); taranan++;
    S.ilerlet(w, 4, 16);
  }
  const r = rapor(id, sc, { taranan, not });
  if (!r.bitti && not) r.sonuc = not;
  return r;
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
