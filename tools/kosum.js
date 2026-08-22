/* =====================================================================
   OTOMATİK OYUN KOŞUMU

   Uygulama sayfasının konsolunda çalışır. Her oyunu gerçekten OYNAR ve
   completeGame çağrılıp çağrılmadığına bakar; "açılıyor" yeterli sayılmaz.

   Kullanım:
     const k = await (await fetch('/kosum.js')).text(); (0,eval)(k);
     KOSUM.kur();                       // önbellek kırıcı + completeGame yakalayıcı
     KOSUM.sirala(['m01','m02']);       // ya da KOSUM.sinif(1,'math')
     KOSUM.durum();                     // ilerleme
     KOSUM.ozet();                      // bitince rapor

   ÖĞRENİLEN TUZAKLAR (hepsi gerçek hataydı):
     · game.step() elle çağrılınca loop.delta güncellenmiyor → her adımda
       elle yazılmalı, yoksa bazı sistemler ilerlemiyor.
     · Phaser 3.80 TweenManager DUVAR SAATİNİ kullanıyor: elle adım atmak
       tween'i ilerletmez. Kazanma zinciri (tween→delayedCall→bitir) ancak
       gerçek zaman geçince tamamlanır → "oturma" evresi şart.
     · Sayfa gizliyken iframe 0×0 ölçülür; fare olaylarının koordinatı
       çöker. ScaleManager eşlemesi her olaydan önce birim'e sabitlenir.
     · Kepçe/roket gibi kovalamacalarda hedefin ÜZERİNDEN geçecek şekilde
       nişan almak gerekir; peşinden sürüklenmek yakalamaz.
   ===================================================================== */
(function (kok) {
  'use strict';
  const K = { rapor: [], kuyruk: [], calisiyor: false, saat: 0, hata: [] };

  K.kur = function () {
    /* PHASER_OYUNLAR / PHASER_TIPLER birer const: window üzerinden
       görünmüyorlar, küresel kapsamdan okunmaları gerekiyor. */
    const eslem = () => {
      let ozel = {}, tip = {};
      try { ozel = PHASER_OYUNLAR; } catch (e) { ozel = kok.PHASER_OYUNLAR || {}; }
      try { tip = PHASER_TIPLER; } catch (e) { tip = kok.PHASER_TIPLER || {}; }
      return { ozel, tip };
    };
    kok.phaserCerceve = function (g) {
      const e = eslem();
      const d = e.ozel[g.id] || e.tip[g.type];
      return '<iframe class="phaser-cerceve" src="phaser/' + d + '.html?d=' + Date.now() +
        '#oyun=' + g.id + '" style="width:100%;height:100%;border:0;display:block;background:#101c2b"></iframe>';
    };
    kok.__bildirim = [];
    if (!kok.__cgAsil) {
      kok.__cgAsil = kok.completeGame;
      kok.completeGame = function (m, p) { kok.__bildirim.push({ mesaj: String(m), puan: p }); };
    }
    kok.addEventListener('error', e => K.hata.push(String(e.message)));
    return 'koşum kuruldu';
  };

  K.o = () => { const f = document.querySelector('iframe'); return f ? (f.contentWindow.OYUN || f.contentWindow.game || null) : null; };
  K.ilerlet = (n) => {
    const o = K.o();
    if (!o || !o.renderer || !o.isRunning) return false;
    try { for (let i = 0; i < n; i++) { K.saat += 16; o.loop.delta = 16; o.loop.time = K.saat; o.step(K.saat, 16); } }
    catch (e) { K.hata.push('step:' + e.message); return false; }
    return true;
  };
  K.sahne = () => {
    const o = K.o(); if (!o) return null;
    return o.scene.scenes.find(s => s.scene.isActive() &&
      ['Boot', 'Menu', 'Sonuc', 'GameOver'].indexOf(s.scene.key) < 0);
  };
  K.fare = (tur, gx, gy) => {
    const o = K.o(); if (!o) return;
    const W = document.querySelector('iframe').contentWindow, sc = K.sahne(); if (!sc) return;
    const sm = o.scale; sm.canvasBounds.x = 0; sm.canvasBounds.y = 0; sm.displayScale.set(1, 1);
    const zoom = sc.cameras.main.zoom, mgr = o.input;
    const e = new W.MouseEvent('mouse' + tur, {
      clientX: gx * zoom, clientY: gy * zoom, button: 0,
      buttons: tur === 'up' ? 0 : 1, bubbles: true
    });
    if (tur === 'move') mgr.onMouseMove(e); else if (tur === 'down') mgr.onMouseDown(e); else mgr.onMouseUp(e);
  };
  K.surukle = (n, hx, hy, son) => {
    K.fare('move', n.x, n.y); K.ilerlet(2);
    K.fare('down', n.x, n.y); K.ilerlet(3);
    for (let i = 1; i <= 6; i++) { K.fare('move', n.x + (hx - n.x) * i / 6, n.y + (hy - n.y) * i / 6); K.ilerlet(2); }
    K.fare('up', n.x, n.y); K.ilerlet(son || 70);
  };

  /* Gerçek zamanda bekle (adım atarak). Tween ve delayedCall duvar
     saatine bağlı olduğu için animasyon bekleyen her yerde şart. */
  K.bekle = (ms) => new Promise(coz => {
    const bas = Date.now();
    const tik = () => { K.ilerlet(4); if (Date.now() - bas >= ms) return coz(); setTimeout(tik, 40); };
    tik();
  });

  /* ---------------- mekanik oynayıcıları ---------------- */
  K.oyuncular = {
    beltSort(sc) {
      let sayilan = 0;
      for (let n = 0; n < 40 && !kok.__bildirim.length; n++) {
        let t = null;
        for (let i = 0; i < 60; i++) {
          if (!sc.kilit) { t = sc.tupler.getChildren().find(x => x.getData('veri') && !x.getData('islendi') && x.active); if (t) break; }
          K.ilerlet(15);
        }
        if (!t) break;
        const v = t.getData('veri');
        const kz = sc.kazanlar.find(x => x.getData('id') === v.kazan);
        if (!kz) return { not: 'kutu yok ' + v.kazan, sayilan };
        const p = sc.puan; K.surukle(t, kz.x, kz.y - 110); if (sc.puan > p) sayilan++;
      }
      return { sayilan };
    },
    dragMatch(sc) {
      if (!sc.hedefler) return K.oyuncular.dokunmali(sc);
      const gec = new Set(sc.hedefler.map(h => h.getData('hedefId')));
      let sayilan = 0;
      for (let n = 0; n < 30 && !kok.__bildirim.length; n++) {
        const p = sc.parcalar.getChildren().find(x => x.active && !x.getData('yerlesti') && gec.has(x.getData('hedefId')));
        if (!p) break;
        const h = sc.hedefler.find(x => x.getData('hedefId') === p.getData('hedefId'));
        const o = sc.puan; K.surukle(p, h.x, h.getData('merkezY')); if (sc.puan > o) sayilan++;
      }
      return { sayilan };
    },
    tapSelect(sc) {
      if (!sc.ogeler) return K.oyuncular.dokunmali(sc);
      let sayilan = 0; sc.suruklu = true;
      for (let n = 0; n < 20 && !kok.__bildirim.length; n++) {
        const o = sc.ogeler.getChildren().find(x => x.active && x.getData('dogru'));
        if (!o) break;
        const p = sc.puan; let ok = false;
        for (let i = 0; i < 400; i++) {
          const dx = o.x - sc.kepce.x, dy = o.y - sc.kepce.y;
          sc.hedef = { x: o.x + dx * 0.5, y: o.y + dy * 0.5 };   /* üzerinden geç */
          K.ilerlet(2);
          if (!o.active || sc.puan > p) { ok = true; break; }
        }
        if (ok) sayilan++; else return { not: 'öge yakalanamadı', sayilan };
        if (sc.can <= 0) return { not: 'canlar bitti', sayilan };
      }
      return { sayilan };
    },
    dokunmali(sc) {
      const kaplar = sc.children.list.filter(c => c.input && c.getData && c.getData('dogru') !== undefined);
      if (!kaplar.length) return { not: 'dokunulabilir doğru kap yok', sayilan: 0 };
      const d = kaplar.find(c => c.getData('dogru') === true);
      if (!d) return { not: 'doğru kap işaretli değil', sayilan: 0 };
      const p = sc.puan; d.emit('pointerdown'); K.ilerlet(200);
      return { sayilan: sc.puan > p ? 1 : 0, not: sc.puan > p ? '' : 'dokunuldu puan yok' };
    },
    choiceQuestion(sc) {
      let sayilan = 0; const g = sc.physics.world.gravity.y || 0, AZAMI = 900, MR = 13;
      const bekle = () => { for (let i = 0; i < 40; i++) { if (!sc.kilit && !sc.mermi) return; K.ilerlet(6); } };
      for (let n = 0; n < 20 && !kok.__bildirim.length; n++) {
        bekle();
        const m0 = sc.meteorlar.getChildren().find(x => x.active && x.getData('dogru') && !x.getData('vuruldu'));
        if (!m0) break;
        if (m0.input) {                       /* şerit düzeni: dokunmalı hedefleme */
          const p = sc.puan; m0.emit('pointerdown'); K.ilerlet(240);
          if (sc.puan > p) { sayilan++; continue; }
          return { not: 'dokunuldu puan yok', sayilan };
        }
        let ok = false, son = '';
        for (let dn = 0; dn < 3 && !ok; dn++) {
          bekle();
          const hepsi = sc.meteorlar.getChildren().filter(x => x.active && !x.getData('vuruldu'));
          const m = hepsi.find(x => x.getData('dogru')); if (!m) { ok = true; break; }
          const yanlis = hepsi.filter(x => x !== m), x0 = sc.gemi.x, y0 = sc.gemi.y - 24;
          const hk = (t) => ({ x: m.x + (m.body ? m.body.velocity.x : 0) * t, y: m.y + (m.body ? m.body.velocity.y : 0) * t });
          const temiz = (vx, vy, tS) => {
            for (let t = 0.03; t < tS - 0.02; t += 0.03) {
              const px = x0 + vx * t, py = y0 + vy * t + 0.5 * g * t * t;
              for (const w of yanlis) {
                const wx = w.x + (w.body ? w.body.velocity.x : 0) * t, wy = w.y + (w.body ? w.body.velocity.y : 0) * t;
                if (Math.hypot(px - wx, py - wy) < Math.max(w.body.width, w.body.height) / 2 + MR) return false;
              }
            }
            return true;
          };
          let sec = null;
          for (let t = 0.25; t <= 2.2; t += 0.02) {
            const h = hk(t);
            const vx = (h.x - x0) / t, vy = (h.y - y0 - 0.5 * g * t * t) / t;
            if (Math.hypot(vx, vy) > AZAMI) continue;
            if (!temiz(vx, vy, t)) continue;
            sec = { t, vx, vy, h: Math.hypot(vx, vy) }; break;
          }
          if (!sec) { son = 'temiz atış yok'; K.ilerlet(90); continue; }
          const p = sc.puan, c = sc.can; sc.atesEt({ x: sec.vx, y: sec.vy });
          let r = '';
          for (let i = 0; i < 300; i++) { K.ilerlet(3); if (sc.puan > p) { r = 'd'; break; } if (sc.can < c) { r = 'c'; break; } }
          if (r === 'd') { ok = true; sayilan++; }
          else { son = (r === 'c' ? 'can gitti' : 'sonuç yok') + ' (hız ' + Math.round(sec.h) + ')'; K.ilerlet(60); }
        }
        if (!ok) return { not: son, sayilan };
      }
      return { sayilan };
    },
    /* tahmin: giriş animasyonu bitip kilit açılınca doğru düğmeye bas.
       Kilit açılmasını GERÇEK zamanda beklemek gerekiyor (tween duvar saati). */
    async estimateReveal(sc) {
      const g = kok.getGame(kok.__simdikiId), c = g.cfg, gercek = Number(c.actualValue) || 0;
      const sec = (c.estimateOptions || []).map(o => ({ et: String(o.label || ''), deger: Number(o.value) }));
      if (!sec.length) return { not: 'estimateOptions yok', sayilan: 0 };
      let iyi = sec[0];
      sec.forEach(s => { if (Math.abs(s.deger - gercek) < Math.abs(iyi.deger - gercek)) iyi = s; });
      /* kilit açılana kadar bekle */
      let acik = false;
      for (let i = 0; i < 40; i++) { if (!sc.kilit) { acik = true; break; } await K.bekle(250); }
      if (!acik) return { not: 'sahne kilidi açılmadı', sayilan: 0 };
      const dg = sc.children.list.filter(x => x.type === 'Container' && x.input);
      const hedef = dg.find(d => d.list.some(t => t.type === 'Text' && String(t.text).trim() === iyi.et.trim()));
      if (!hedef) return { not: 'düğme yok (' + iyi.et + ')', sayilan: 0 };
      const p = sc.puan;
      hedef.emit('pointerdown');
      /* açılış sayımı uzun sürüyor: puan gelene kadar gerçek zamanda bekle */
      for (let i = 0; i < 80; i++) { if (sc.puan > p || kok.__bildirim.length) break; await K.bekle(250); }
      return { sayilan: sc.puan > p ? 1 : 0, not: sc.puan > p ? '' : 'tahmin puanlanmadı' };
    },
    /* hafıza: aynı çifti taşıyan iki kartı sırayla çevir.
       Kart çevirme animasyonu duvar saatiyle çalıştığı için taplar
       arasında GERÇEK zaman beklemek gerekiyor. */
    async memoryPairs(sc) {
      if (!sc.kartlar) return { not: 'kart grubu yok', sayilan: 0 };
      let sayilan = 0;
      for (let tur = 0; tur < 20 && !kok.__bildirim.length; tur++) {
        let hazir = null;
        for (let i = 0; i < 40; i++) {
          if (!sc.kilit && !sc.mesgul && !sc.acikKart) {
            hazir = sc.kartlar.getChildren().filter(k => k.active &&
              !k.getData('eslesti') && !k.getData('acik') && k.getData('oturdu'));
            if (hazir.length >= 2) break;
          }
          await K.bekle(120);
        }
        if (!hazir || hazir.length < 2) break;
        const a = hazir[0];
        const b = hazir.find(k => k !== a && k.getData('cift') === a.getData('cift'));
        if (!b) return { not: 'eşi bulunamadı (çift ' + a.getData('cift') + ')', sayilan };
        const p = sc.puan;
        sc.kartaDokun(a);
        await K.bekle(500);
        sc.kartaDokun(b);
        await K.bekle(1400);
        if (sc.puan > p) sayilan++;
        else return { not: 'çift eşleşmedi (çift ' + a.getData('cift') + ')', sayilan };
      }
      return { sayilan };
    },
    /* pizza: müşterinin istediği kalemleri tepsiye koy, servis et.
       Kalemler ya needs listesiyle ya da HEDEF TUTAR (targetValue+only) ile
       veriliyor; ikisi de destekleniyor. */
    async serveOrder(sc) {
      if (!sc.paletKutular) return { not: 'palet yok', sayilan: 0 };
      const g = kok.getGame(kok.__simdikiId);
      const musteriler = (g.cfg.customers || []);
      const palet = (g.cfg.palette || []).map(x => String(x.id));
      let sayilan = 0;
      for (let n = 0; n < musteriler.length + 2 && !kok.__bildirim.length; n++) {
        const ix = sc.musteriNo;
        const m = musteriler[ix];
        if (!m) break;
        for (let i = 0; i < 20; i++) { if (!sc.kilit) break; await K.bekle(200); }
        const bas = (pi, adet) => {
          const kutu = pi >= 0 ? sc.paletKutular[pi] : null;
          for (let k = 0; k < (adet || 1); k++) { if (kutu) { kutu.emit('pointerdown'); K.ilerlet(40); } }
        };
        if (m.needs && m.needs.length) {
          m.needs.forEach(ih => bas(palet.indexOf(String(ih.id)), ih.count == null ? 1 : ih.count));
        } else if (m.targetValue != null) {
          const izin = m.only && m.only.length ? m.only.map(String) : palet;
          const kalemler = (g.cfg.palette || [])
            .map((x, i) => ({ i, id: String(x.id), deger: Number(x.value) || 0 }))
            .filter(x => izin.indexOf(x.id) >= 0 && x.deger > 0)
            .sort((a, b) => b.deger - a.deger);
          let kalan = Number(m.targetValue);
          for (const kl of kalemler) {
            while (kalan >= kl.deger - 0.0001 && kalan > 0) { bas(kl.i, 1); kalan -= kl.deger; }
          }
          if (kalan > 0.0001) return { not: 'hedef tutar tutturulamadı (kalan ' + kalan + ')', sayilan };
        }
        await K.bekle(700);
        const p = sc.puan;
        try { sc.servisEt(); } catch (e) { return { not: 'servisEt hatası: ' + e.message, sayilan }; }
        await K.bekle(2200);
        if (sc.puan > p) sayilan++;
        else return { not: ix + '. müşteri servisi puanlanmadı', sayilan };
      }
      return { sayilan };
    },
    /* sıralama: her bırakıştan sonra GERÇEK zaman bekle — blok huniye
       düşerken sahne kilitleniyor ve bir sonraki blok geç üretiliyor. */
    async orderSequence(sc) {
      if (!sc.bloklar) return K.oyuncular.dokunmali(sc);
      const g = kok.getGame(kok.__simdikiId);
      const sira = ((g.cfg.order || g.cfg.sequence || [])).map(String);
      const ag = (sc.huniAgzi && sc.huniAgzi.getChildren) ? sc.huniAgzi.getChildren()[0] : null;
      const hx = ag ? ag.x : 240, hy = ag ? (ag.y - 70) : 640;
      let sayilan = 0;
      for (let n = 0; n < sira.length + 2 && !kok.__bildirim.length; n++) {
        if (sira.length && sc.adim >= sira.length) { await K.bekle(2500); break; }
        /* kilit açılsın, blok üretilsin */
        let b = null;
        for (let i = 0; i < 30; i++) {
          if (!sc.kilit) {
            const bekId = sira[sc.adim];
            if (bekId) b = sc.bloklar.getChildren().find(x => x.active && !x.getData('islendi') &&
              x.getData('veri') && String(x.getData('veri').id) === bekId);
            if (!b) b = sc.bloklar.getChildren().find(x => x.active && !x.getData('islendi'));
            if (b) break;
          }
          await K.bekle(200);
        }
        if (!b) break;
        const p = sc.puan;
        K.surukle(b, hx, hy, 200);
        await K.bekle(1300);
        if (sc.puan > p) sayilan++;
        else return { not: 'blok "' + (sira[sc.adim] || '?') + '" huniye girmedi (adım ' + sc.adim + ')', sayilan };
      }
      return { sayilan };
    },
    /* uzamsal.html içindeki özel sahneler */
    keci(sc) {
      const sira = (sc.sira || []).map(String);
      if (!sira.length) return { not: 'sıra yok', sayilan: 0 };
      const dugmeler = sc.children.list.filter(c => c.type === 'Container' && c.input);
      const anahtar = (sc.secenekler || []).map(s => String(s.key));
      let sayilan = 0;
      for (const adim of sira) {
        K.ilerlet(30);
        const ix = anahtar.indexOf(adim);
        const d = (ix >= 0 && dugmeler[ix]) ? dugmeler[ix] : null;
        if (!d) return { not: '"' + adim + '" düğmesi yok', sayilan };
        d.emit('pointerdown'); K.ilerlet(90); sayilan++;
      }
      return { sayilan };
    },
    suruklemeli(sc, hx, hy) {
      const nesneler = sc.children.list.filter(c => c.getData && c.getData('dogru') !== undefined && c.input);
      const d = nesneler.find(c => c.getData('dogru') === true);
      if (!d) return { not: 'doğru nesne yok', sayilan: 0 };
      const p = sc.puan; K.surukle(d, hx, hy, 120);
      return { sayilan: sc.puan > p ? 1 : 0, not: sc.puan > p ? '' : 'sürüklendi puan yok' };
    }
  };

  K.oyuncuSec = function (g, sc) {
    const k = sc.scene.key;
    if (k === 'Keci') return K.oyuncular.keci;
    if (k === 'Golge') return (s) => K.oyuncular.suruklemeli(s, 240, s.siluetY);
    if (k === 'Corap') return (s) => K.oyuncular.suruklemeli(s, 240, (s.ipY || 400) + 40);
    if (k !== 'Game') return K.oyuncular.dokunmali;
    return K.oyuncular[g.type];
  };

  /* Tween'ler duvar saatiyle ilerlediği için bitiş zincirini GERÇEK
     zamanda beklemek gerekiyor. */
  K.oturt = function (sure, bitince) {
    const bas = Date.now();
    const tik = () => {
      K.ilerlet(6);
      if (kok.__bildirim.length || Date.now() - bas > sure) return bitince();
      setTimeout(tik, 90);
    };
    tik();
  };

  K.tekOyna = function (id, bitince) {
    const g = kok.getGame(id); const k = { id, ad: g.title, tip: g.type, sinif: g.grade, ders: g.subj };
    const sc = K.sahne();
    if (!sc) { k.durum = 'SAHNE YOK'; return bitince(k); }
    k.sahne = sc.scene.key; K.ilerlet(150);
    const f = K.oyuncuSec(g, sc);
    if (!f) { k.durum = 'OYNAYICI YOK'; return bitince(k); }
    let sonuc;
    try { sonuc = f(sc); } catch (e) { k.durum = 'İSTİSNA'; k.not = e.message; return bitince(k); }
    /* Bitiş animasyonlarının süresi mekaniğe göre çok değişiyor:
       kavanoz 30 nesneyi tek tek sayıyor (~15 sn), hafıza kart çeviriyor.
       Bekleme penceresi kısa olursa oyun "bitmedi" görünüyor. */
    const OTURMA = { estimateReveal: 22000, memoryPairs: 9000, serveOrder: 9000, orderSequence: 6000 };
    Promise.resolve(sonuc).catch(e => ({ not: 'istisna: ' + e.message })).then((r0) => {
      const r = r0 || {};
      K.oturt(OTURMA[g.type] || 3500, () => {
        k.puan = sc.puan; k.can = sc.can;
        if (kok.__bildirim.length) { k.durum = 'TAMAM'; k.not = 'puan ' + kok.__bildirim[0].puan; }
        else { k.durum = 'BİTMEDİ'; k.not = r.not || ('sayılan ' + r.sayilan); }
        bitince(k);
      });
    });
  };

  K.sirala = function (idler) {
    K.kuyruk = idler.slice(); K.rapor = []; K.calisiyor = true;
    const sonraki = () => {
      if (!K.kuyruk.length) { K.calisiyor = false; return; }
      const id = K.kuyruk.shift();
      kok.__bildirim = []; kok.__simdikiId = id; K.saat = 0; K.hata = [];
      try { kok.openGame(id); }
      catch (e) { K.rapor.push({ id, durum: 'AÇILMADI', not: e.message }); return setTimeout(sonraki, 60); }
      let bek = 0;
      const hazir = () => { const o = K.o(); if (!o || !o.renderer || !o.isRunning) return false; K.ilerlet(30); return !!K.sahne(); };
      const dene = () => {
        let h = false; try { h = hazir(); } catch (e) { K.hata.push(e.message); }
        if (h || bek > 22) {
          K.tekOyna(id, (k) => {
            if (K.hata.length) k.not = (k.not || '') + ' [js:' + K.hata[0].slice(0, 40) + ']';
            K.rapor.push(k); setTimeout(sonraki, 60);
          });
        } else { bek++; setTimeout(dene, 200); }
      };
      setTimeout(dene, 400);
    };
    sonraki();
    return 'kuyruk: ' + idler.length;
  };

  K.sinif = function (sinif, ders) {
    /* ALL_GAMES bir const: window üzerinden görünmüyor, küresel kapsamdan oku */
    let hepsi;
    try { hepsi = ALL_GAMES; } catch (e) { hepsi = kok.ALL_GAMES || []; }
    const liste = hepsi.map(x => kok.getGame(x.id))
      .filter(g => g.grade === sinif && (!ders || g.subj === ders) && kok.phaserOyunuMu(g))
      .map(g => g.id);
    return K.sirala(liste);
  };
  K.durum = () => (K.calisiyor ? 'sürüyor ' : 'BİTTİ ') + K.rapor.length + '/' + (K.rapor.length + K.kuyruk.length);
  K.ozet = function () {
    const kotu = K.rapor.filter(r => r.durum !== 'TAMAM');
    return 'TAMAM ' + (K.rapor.length - kotu.length) + '/' + K.rapor.length +
      (kotu.length ? '\nsorunlu:\n' + kotu.map(r => '  ' + r.id + ' ' + r.tip + ' [' + (r.sahne || '-') + '] ' + r.durum + ' · ' + (r.not || '')).join('\n') : '');
  };

  kok.KOSUM = K;
})(window);
