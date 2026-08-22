/* =====================================================================
   SVG → PHASER ÇİZİCİ

   NEDEN: Katalogdaki 16 oyunun görseli satır içi SVG. Bu oyunlar
   şekil/geometri oyunları: "gelen şeklin kenarlarını say", "üçgen hangi
   çeşit", "açı dar mı dik mi". Metin olarak soyulunca ekranda "?" kalıyor
   ve oyun oynanamıyor. SVG'nin içinde şeklin GERÇEK koordinatları var;
   burada onları ayrıştırıp Phaser Graphics ile çiziyoruz — yazarın çizdiği
   şekil aynen görünüyor.

   Kapsam (katalogda kullanılan her şey):
     polygon, polyline, line, rect, circle, ellipse, text
     path: M, L, Z, A  (yay için SVG merkez dönüşümü uygulanıyor)
     <g transform="translate(...) scale(...) rotate(...)">
   ===================================================================== */
(function (kok) {
  'use strict';

  function sayilar(metin) {
    return (String(metin).match(/-?\d*\.?\d+(?:e[-+]?\d+)?/gi) || []).map(Number);
  }

  function ozellikler(etiket) {
    const o = {};
    const re = /([a-zA-Z][a-zA-Z0-9-]*)\s*=\s*"([^"]*)"/g;   /* x1,y1,x2,y2 gibi rakamlı adlar da */
    let m;
    while ((m = re.exec(etiket))) o[m[1]] = m[2];
    return o;
  }

  function renkSayi(deger) {
    if (!deger) return null;
    const d = String(deger).trim().toLowerCase();
    if (d === 'none' || d === 'transparent') return null;
    if (d[0] === '#') {
      let h = d.slice(1);
      if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
      return parseInt(h, 16);
    }
    const adlar = { black:0x000000, white:0xffffff, red:0xff0000, green:0x008000,
      blue:0x0000ff, gray:0x808080, grey:0x808080, orange:0xffa500,
      yellow:0xffff00, purple:0x800080, brown:0xa52a2a, pink:0xffc0cb };
    if (adlar[d] != null) return adlar[d];
    const rgb = d.match(/rgba?\(([^)]+)\)/);
    if (rgb) {
      const p = sayilar(rgb[1]);
      return ((p[0] & 255) << 16) | ((p[1] & 255) << 8) | (p[2] & 255);
    }
    return null;
  }

  /* --- dönüşüm dizisi (yığın olarak uygulanıyor) --- */
  function donusumCoz(metin) {
    const liste = [];
    const re = /(translate|scale|rotate|matrix)\s*\(([^)]*)\)/g;
    let m;
    while ((m = re.exec(metin || ''))) liste.push({ tur: m[1], p: sayilar(m[2]) });
    return liste;
  }

  function noktaDonustur(x, y, yigin) {
    for (let i = yigin.length - 1; i >= 0; i--) {
      const d = yigin[i];
      if (d.tur === 'translate') { x += d.p[0] || 0; y += d.p[1] || 0; }
      else if (d.tur === 'scale') {
        const sx = d.p[0] == null ? 1 : d.p[0];
        const sy = d.p[1] == null ? sx : d.p[1];
        x *= sx; y *= sy;
      } else if (d.tur === 'rotate') {
        const a = Phaser.Math.DegToRad(d.p[0] || 0);
        const cx = d.p[1] || 0, cy = d.p[2] || 0;
        const dx = x - cx, dy = y - cy;
        x = cx + dx * Math.cos(a) - dy * Math.sin(a);
        y = cy + dx * Math.sin(a) + dy * Math.cos(a);
      } else if (d.tur === 'matrix') {
        const [a, b, c, dd, e, f] = d.p;
        const nx = a * x + c * y + e, ny = b * x + dd * y + f;
        x = nx; y = ny;
      }
    }
    return { x: x, y: y };
  }

  /* --- SVG yayı (A) → merkez + açı: standart dönüşüm --- */
  function yayNoktalari(x1, y1, rx, ry, aciDeg, buyukYay, yon, x2, y2) {
    if (!rx || !ry) return [{ x: x2, y: y2 }];
    const fi = Phaser.Math.DegToRad(aciDeg || 0);
    const cosF = Math.cos(fi), sinF = Math.sin(fi);
    const dx2 = (x1 - x2) / 2, dy2 = (y1 - y2) / 2;
    const x1p = cosF * dx2 + sinF * dy2;
    const y1p = -sinF * dx2 + cosF * dy2;
    rx = Math.abs(rx); ry = Math.abs(ry);
    const lam = (x1p * x1p) / (rx * rx) + (y1p * y1p) / (ry * ry);
    if (lam > 1) { const k = Math.sqrt(lam); rx *= k; ry *= k; }
    const pay = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p;
    const bolum = rx * rx * y1p * y1p + ry * ry * x1p * x1p;
    let kat = Math.sqrt(Math.max(0, pay / (bolum || 1)));
    if (buyukYay === yon) kat = -kat;
    const cxp = kat * (rx * y1p) / ry;
    const cyp = kat * (-ry * x1p) / rx;
    const cx = cosF * cxp - sinF * cyp + (x1 + x2) / 2;
    const cy = sinF * cxp + cosF * cyp + (y1 + y2) / 2;

    const aci = (ux, uy, vx, vy) => {
      const nokta = ux * vx + uy * vy;
      const boy = Math.sqrt(ux * ux + uy * uy) * Math.sqrt(vx * vx + vy * vy);
      let a = Math.acos(Math.min(1, Math.max(-1, nokta / (boy || 1))));
      if (ux * vy - uy * vx < 0) a = -a;
      return a;
    };
    const bas = aci(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry);
    let genislik = aci((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry);
    if (!yon && genislik > 0) genislik -= 2 * Math.PI;
    else if (yon && genislik < 0) genislik += 2 * Math.PI;

    const adet = Math.max(6, Math.ceil(Math.abs(genislik) / 0.2));
    const noktalar = [];
    for (let i = 1; i <= adet; i++) {
      const t = bas + genislik * (i / adet);
      const px = cx + rx * Math.cos(t) * cosF - ry * Math.sin(t) * sinF;
      const py = cy + rx * Math.cos(t) * sinF + ry * Math.sin(t) * cosF;
      noktalar.push({ x: px, y: py });
    }
    return noktalar;
  }

  /* --- path "d" → çokgen dizileri --- */
  function pathCoz(d) {
    const parcalar = [];
    let simdi = [];
    const jetonlar = String(d).match(/[MmLlZzAaHhVv][^MmLlZzAaHhVv]*/g) || [];
    let x = 0, y = 0;
    jetonlar.forEach(function (j) {
      const komut = j[0];
      const p = sayilar(j.slice(1));
      const goreli = komut === komut.toLowerCase();
      switch (komut.toUpperCase()) {
        case 'M':
          if (simdi.length > 1) parcalar.push(simdi);
          x = goreli ? x + p[0] : p[0]; y = goreli ? y + p[1] : p[1];
          simdi = [{ x: x, y: y }];
          for (let i = 2; i + 1 < p.length; i += 2) {
            x = goreli ? x + p[i] : p[i]; y = goreli ? y + p[i + 1] : p[i + 1];
            simdi.push({ x: x, y: y });
          }
          break;
        case 'L':
          for (let i = 0; i + 1 < p.length; i += 2) {
            x = goreli ? x + p[i] : p[i]; y = goreli ? y + p[i + 1] : p[i + 1];
            simdi.push({ x: x, y: y });
          }
          break;
        case 'H':
          for (let i = 0; i < p.length; i++) { x = goreli ? x + p[i] : p[i]; simdi.push({ x: x, y: y }); }
          break;
        case 'V':
          for (let i = 0; i < p.length; i++) { y = goreli ? y + p[i] : p[i]; simdi.push({ x: x, y: y }); }
          break;
        case 'A':
          for (let i = 0; i + 6 < p.length; i += 7) {
            const hx = goreli ? x + p[i + 5] : p[i + 5];
            const hy = goreli ? y + p[i + 6] : p[i + 6];
            yayNoktalari(x, y, p[i], p[i + 1], p[i + 2], !!p[i + 3], !!p[i + 4], hx, hy)
              .forEach(function (n) { simdi.push(n); });
            x = hx; y = hy;
          }
          break;
        case 'Z':
          if (simdi.length > 1) { simdi.kapali = true; parcalar.push(simdi); }
          simdi = simdi.length ? [{ x: simdi[0].x, y: simdi[0].y }] : [];
          x = simdi.length ? simdi[0].x : x; y = simdi.length ? simdi[0].y : y;
          break;
      }
    });
    if (simdi.length > 1) parcalar.push(simdi);
    return parcalar;
  }

  /**
   * SVG metnini bir Phaser sahnesine çizer.
   * @param {Phaser.Scene} sahne
   * @param {string} svg   satır içi SVG metni
   * @param {number} x,y   merkez konumu
   * @param {number} boy   hedef kutu (px) — viewBox buna ölçeklenir
   * @returns {Phaser.GameObjects.Container}
   */
  function tekCiz(sahne, svg, boy, en) {
    en = en || boy;
    const kap = sahne.add.container(0, 0);
    const metin = String(svg || '');
    const vb = sayilar((metin.match(/viewBox\s*=\s*"([^"]+)"/) || [])[1] || '0 0 100 100');
    const vbX = vb[0] || 0, vbY = vb[1] || 0, vbEn = vb[2] || 100, vbBoy = vb[3] || 100;

    /* ---------- 1. GEÇİŞ: öğeleri çöz, viewBox koordinatlarında topla ----------
       Ölçeği viewBox'a göre değil ÇİZİMİN GERÇEK SINIRINA göre veriyoruz.
       Katalogdaki açı görsellerinde şekil viewBox'ın yarısını kullanıyor;
       viewBox'a ölçeklenince kartta ufacık kalıyor ve çocuk açıyı göremiyor. */
    const ogeler = [];
    const yigin = [], gSayilari = [];
    const re = /<(\/?)(g|polygon|polyline|line|rect|circle|ellipse|path|text)\b([^>]*)>([^<]*)/g;
    let m;
    while ((m = re.exec(metin))) {
      const kapanis = m[1] === '/';
      const ad = m[2];
      const oz = ozellikler(m[3] || '');
      const icerik = (m[4] || '').trim();

      if (ad === 'g') {
        /* Bir <g> birden çok dönüşüm taşıyabilir: translate + scale + rotate */
        if (kapanis) yigin.length -= (gSayilari.pop() || 0);
        else { const t = donusumCoz(oz.transform); yigin.push.apply(yigin, t); gSayilari.push(t.length); }
        continue;
      }
      if (kapanis) continue;

      const y2 = yigin.concat(donusumCoz(oz.transform));
      const D = function (nx, ny) { return noktaDonustur(nx, ny, y2); };

      const bicim = {
        dolgu: renkSayi(oz.fill == null ? '#000000' : oz.fill),
        kenar: renkSayi(oz.stroke),
        kalin: parseFloat(oz['stroke-width']) || 1,
        saydam: oz.opacity == null ? 1 : parseFloat(oz.opacity),
        kesik: (oz['stroke-dasharray'] || '').trim()
          ? sayilar(oz['stroke-dasharray']).filter(function (v) { return v > 0; }) : null
      };

      if (ad === 'polygon' || ad === 'polyline') {
        const p = sayilar(oz.points), n = [];
        for (let i = 0; i + 1 < p.length; i += 2) n.push(D(p[i], p[i + 1]));
        ogeler.push({ tur: 'yol', noktalar: n, kapali: ad === 'polygon', bicim: bicim });
      } else if (ad === 'line') {
        ogeler.push({ tur: 'yol', kapali: false, bicim: bicim,
          noktalar: [D(+oz.x1 || 0, +oz.y1 || 0), D(+oz.x2 || 0, +oz.y2 || 0)] });
      } else if (ad === 'rect') {
        const rx = +oz.x || 0, ry = +oz.y || 0, rw = +oz.width || 0, rh = +oz.height || 0;
        ogeler.push({ tur: 'yol', kapali: true, bicim: bicim,
          noktalar: [D(rx, ry), D(rx + rw, ry), D(rx + rw, ry + rh), D(rx, ry + rh)] });
      } else if (ad === 'circle' || ad === 'ellipse') {
        const cx = +(oz.cx || 0), cy = +(oz.cy || 0);
        const rx = ad === 'circle' ? +(oz.r || 0) : +(oz.rx || 0);
        const ry = ad === 'circle' ? +(oz.r || 0) : +(oz.ry || 0);
        const n = [];
        for (let a = 0; a < 360; a += 8) {
          const r = Phaser.Math.DegToRad(a);
          n.push(D(cx + Math.cos(r) * rx, cy + Math.sin(r) * ry));
        }
        ogeler.push({ tur: 'yol', noktalar: n, kapali: true, bicim: bicim });
      } else if (ad === 'path') {
        pathCoz(oz.d).forEach(function (parca) {
          ogeler.push({ tur: 'yol', kapali: !!parca.kapali, bicim: bicim,
            noktalar: parca.map(function (q) { return D(q.x, q.y); }) });
        });
      } else if (ad === 'text' && icerik) {
        const punto = parseFloat(oz['font-size']) || 12;
        ogeler.push({ tur: 'yazi', icerik: icerik, punto: punto,
          nokta: D(+oz.x || 0, (+oz.y || 0) - punto * 0.36),
          hiza: oz['text-anchor'] || 'start',
          kalinYazi: (parseInt(oz['font-weight'], 10) || 0) >= 600 || oz['font-weight'] === 'bold',
          aile: oz['font-family'] || 'Arial, Helvetica, sans-serif',
          renk: renkSayi(oz.fill) == null ? 0x2f2a45 : renkSayi(oz.fill) });
      }
    }
    if (!ogeler.length) { kap.setSize(boy, boy); return kap; }

    /* ---------- sınır kutusu ---------- */
    let x1 = Infinity, y1 = Infinity, x2 = -Infinity, y2b = -Infinity;
    let enKalin = 0;
    ogeler.forEach(function (o) {
      if (o.tur === 'yol') {
        enKalin = Math.max(enKalin, o.bicim.kenar != null ? o.bicim.kalin : 0);
        o.noktalar.forEach(function (n) {
          x1 = Math.min(x1, n.x); y1 = Math.min(y1, n.y);
          x2 = Math.max(x2, n.x); y2b = Math.max(y2b, n.y);
        });
      } else {
        const yarimEn = o.icerik.length * o.punto * 0.3;
        const solPay = o.hiza === 'middle' ? yarimEn : (o.hiza === 'end' ? yarimEn * 2 : 0);
        x1 = Math.min(x1, o.nokta.x - solPay);
        x2 = Math.max(x2, o.nokta.x - solPay + yarimEn * 2);
        y1 = Math.min(y1, o.nokta.y - o.punto * 0.6);
        y2b = Math.max(y2b, o.nokta.y + o.punto * 0.6);
      }
    });
    /* kalem kalınlığı payı */
    const pay = enKalin / 2 + 0.5;
    x1 -= pay; y1 -= pay; x2 += pay; y2b += pay;

    /* Çizim viewBox'ın çok küçük bir kısmındaysa içeriğe göre büyüt; ama
       viewBox'ı büyük ölçüde dolduruyorsa viewBox'a uy (kompozisyon bozulmasın). */
    const icEn = Math.max(1, x2 - x1), icBoy = Math.max(1, y2b - y1);
    const doluluk = Math.max(icEn / vbEn, icBoy / vbBoy);
    const iceriktenOlcek = doluluk < 0.82;
    const kaynakEn  = iceriktenOlcek ? icEn : vbEn;
    const kaynakBoy = iceriktenOlcek ? icBoy : vbBoy;
    const mX = iceriktenOlcek ? (x1 + x2) / 2 : vbX + vbEn / 2;
    const mY = iceriktenOlcek ? (y1 + y2b) / 2 : vbY + vbBoy / 2;
    /* Hem genişlik hem yükseklik sınırına sığdır (oran korunur) */
    const olcek = Math.min(en / kaynakEn, boy / kaynakBoy);
    const H = function (n) { return { x: (n.x - mX) * olcek, y: (n.y - mY) * olcek }; };

    /* ---------- 2. GEÇİŞ: çiz ---------- */
    const g = sahne.add.graphics();
    kap.add(g);
    ogeler.forEach(function (o) {
      if (o.tur === 'yazi') {
        const p = H(o.nokta);
        const t = sahne.add.text(p.x, p.y, o.icerik, {
          fontFamily: o.aile, fontSize: Math.max(9, o.punto * olcek) + 'px',
          fontStyle: o.kalinYazi ? 'bold' : 'normal',
          color: '#' + o.renk.toString(16).padStart(6, '0')
        });
        t.setOrigin(o.hiza === 'middle' ? 0.5 : (o.hiza === 'end' ? 1 : 0), 0.5);
        kap.add(t);
        return;
      }
      const n = o.noktalar.map(H);
      if (n.length < 2) return;
      const b = o.bicim;
      const kalin = Math.max(1, b.kalin * olcek);
      if (b.dolgu != null && o.kapali && n.length > 2) {
        g.fillStyle(b.dolgu, b.saydam);
        g.beginPath(); g.moveTo(n[0].x, n[0].y);
        for (let i = 1; i < n.length; i++) g.lineTo(n[i].x, n[i].y);
        g.closePath(); g.fillPath();
      }
      if (b.kenar == null) return;
      g.lineStyle(kalin, b.kenar, b.saydam);
      if (b.kesik) {
        /* kesikli çizgi: yolu desene göre parçalara böl */
        const desen = (b.kesik.length === 1 ? [b.kesik[0], b.kesik[0]] : b.kesik)
          .map(function (v) { return v * olcek; });
        const yol = o.kapali ? n.concat([n[0]]) : n;
        let di = 0, kalan = desen[0], cizili = true;
        for (let i = 0; i + 1 < yol.length; i++) {
          let ax = yol[i].x, ay = yol[i].y;
          const bx = yol[i + 1].x, by = yol[i + 1].y;
          let uz = Phaser.Math.Distance.Between(ax, ay, bx, by);
          while (uz > 0.01) {
            const adim = Math.min(kalan, uz), t = adim / uz;
            const nx = ax + (bx - ax) * t, ny = ay + (by - ay) * t;
            if (cizili) { g.beginPath(); g.moveTo(ax, ay); g.lineTo(nx, ny); g.strokePath(); }
            ax = nx; ay = ny; uz -= adim; kalan -= adim;
            if (kalan <= 0.01) { di = (di + 1) % desen.length; kalan = desen[di]; cizili = !cizili; }
          }
        }
      } else {
        g.beginPath(); g.moveTo(n[0].x, n[0].y);
        for (let i = 1; i < n.length; i++) g.lineTo(n[i].x, n[i].y);
        if (o.kapali) g.closePath();
        g.strokePath();
      }
    });

    kap.setSize(kaynakEn * olcek, kaynakBoy * olcek);
    return kap;
  }

  /**
   * Bir katalog görselini çizer. İçerik birden çok <svg> taşıyabilir
   * (ör. kesir oyunlarında yan yana dilim daireleri) ve SVG'den sonra
   * düz metin gelebilir (ör. "🟢 Yeşil meyve") — ikisi de korunuyor.
   */
  function ciz(sahne, icerik, x, y, boy, secenek) {
    const ayar = secenek || {};
    const metin = String(icerik || '');
    const bloklar = metin.match(/<svg[\s\S]*?<\/svg>/gi) || [];
    const kap = sahne.add.container(x, y);
    if (!bloklar.length) return kap;

    /* SVG dışında kalan okunur metin */
    let kalan = metin;
    bloklar.forEach(function (b) { kalan = kalan.replace(b, ' '); });
    kalan = kalan.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
    /* Mekanik etiketi ayrıca yazıyorsa metni burada tekrarlamayalım */
    if (ayar.metin === false) kalan = '';

    const enSinir = ayar.en || boy;
    const altYazi = kalan ? Math.round(boy * 0.22) : 0;
    const cizimBoy = boy - altYazi;

    /* Katalog SVG'leri açık zemin için renklendirilmiş (koyu kalem, açık dolgu).
       Koyu bir sahnede doğrudan çizilince görünmüyor; istenirse arkasına
       açık bir plaka koyuyoruz. */
    let plaka = null;
    if (ayar.zemin) {
      plaka = sahne.add.graphics();
      kap.add(plaka);
    }

    let icEn = 0, icBoy = 0;
    if (bloklar.length === 1) {
      const c = tekCiz(sahne, bloklar[0], cizimBoy, enSinir);
      c.y = -altYazi / 2;
      kap.add(c);
      icEn = c.width; icBoy = c.height;
    } else {
      /* yan yana diz: her biri eşit paya sığacak kadar küçülür */
      const bosluk = Math.max(2, enSinir * 0.04);
      const her = (enSinir - bosluk * (bloklar.length - 1)) / bloklar.length;
      const enBoy = Math.min(her, cizimBoy);
      const toplamEn = enBoy * bloklar.length + bosluk * (bloklar.length - 1);
      bloklar.forEach(function (b, i) {
        const c = tekCiz(sahne, b, enBoy, enBoy);
        c.x = -toplamEn / 2 + enBoy / 2 + i * (enBoy + bosluk);
        c.y = -altYazi / 2;
        kap.add(c);
      });
      icEn = toplamEn; icBoy = enBoy;
    }

    if (kalan) {
      const yazi = sahne.add.text(0, cizimBoy / 2 - altYazi / 2 + altYazi * 0.55, kalan, {
        fontFamily: 'system-ui, sans-serif',
        fontSize: Math.max(10, Math.round(boy * 0.15)) + 'px',
        fontStyle: 'bold', color: '#2f2a45', align: 'center',
        wordWrap: { width: boy * 1.6 }
      }).setOrigin(0.5);
      /* kutuya sığdır: uzun etiket taşmasın */
      if (yazi.width > boy) yazi.setScale(boy / yazi.width);
      kap.add(yazi);
    }

    let sonEn = ayar.en ? enSinir : boy, sonBoy = boy;
    if (plaka) {
      const pd = ayar.pay == null ? 7 : ayar.pay;
      const pEn = Math.max(18, icEn) + pd * 2;
      const pBoy = Math.max(18, icBoy) + pd * 2 + altYazi;
      plaka.fillStyle(ayar.zeminRenk == null ? 0xfdfcf7 : ayar.zeminRenk, 1);
      plaka.fillRoundedRect(-pEn / 2, -pBoy / 2, pEn, pBoy, 9);
      plaka.lineStyle(2, 0xd8d2c4, 1);
      plaka.strokeRoundedRect(-pEn / 2, -pBoy / 2, pEn, pBoy, 9);
      /* Çağıran yerleşimi kabın ölçüsüne göre yapıyor; plaka çizimden
         büyük olabildiği için gerçek ölçüyü bildiriyoruz — yoksa
         komşu kutular birbirine değiyor. */
      sonEn = pEn; sonBoy = pBoy;
    }

    kap.setSize(sonEn, sonBoy);
    return kap;
  }

  /** İçerikteki SVG dışı okunur metni döndürür ("<svg…/><br>🔴 Kırmızı meyve" → "🔴 Kırmızı meyve") */
  function metinAyikla(icerik) {
    let kalan = String(icerik || '');
    (kalan.match(/<svg[\s\S]*?<\/svg>/gi) || []).forEach(function (b) { kalan = kalan.replace(b, ' '); });
    return kalan.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
  }

  kok.SVGCIZ = { ciz: ciz, tekCiz: tekCiz, metinAyikla: metinAyikla, svgMi: function (m) { return typeof m === 'string' && m.indexOf('<svg') >= 0; } };
})(window);
