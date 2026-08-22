/* =====================================================================
   ANLAM DENETİMİ

   Otomatik oynama taraması "oyun bitiyor mu?" sorusunu yanıtlıyor.
   Bu dosya farklı bir soruyu yanıtlıyor: "görev anlamlı mı?"

   Yakalamaya çalıştığı kusurlar gerçek örneklerden çıkarıldı:
     · m07: "izde 4 çizgi var, aynı sayıda çizgisi olan ayakkabıya dokun"
            diyor ama ayakkabıların üstünde "(4 çizgi)" YAZIYOR — çocuk
            çizgi saymıyor, sayıyı okuyor. Üstelik karşılaştırılacak iz
            hiç çizilmemiş.
     · m13: sekiz özdeş koyundan yalnız belirli dördü "doğru" sayılıyordu.
     · m06: anahtarların yanında "(ters)" yazıyordu.

   Kullanım (uygulama sayfasının konsolunda):
     ANLAM.tara()            → tüm katalog
     ANLAM.tara({grade:1})   → yalnız 1. sınıf
   ===================================================================== */
(function (kok) {
  'use strict';

  const dz = (s) => String(s == null ? '' : s)
    .replace(/<[^>]*>/g, ' ').replace(/&[a-z#0-9]+;/gi, ' ')
    .replace(/\s+/g, ' ').trim();

  const sayilar = (s) => (String(s).match(/\d+/g) || []).map(Number);

  /* Bir oyunun bütün "seçilebilir öge" etiketlerini toplar. */
  function ogeler(g) {
    const c = g.cfg || {};
    const liste = [];
    (c.items || []).forEach(i => liste.push({ id: i.id, etiket: dz(i.label), ham: i, gorsel: i.emoji || i.svg || '' }));
    (c.sources || []).forEach(i => liste.push({ id: i.id, etiket: dz(i.label), ham: i, gorsel: i.emoji || i.svg || '' }));
    (c.steps || []).forEach((a, ai) => (a.options || []).forEach((o, oi) =>
      liste.push({ id: 'adim' + ai + '.' + oi, etiket: dz(o.label), ham: o, gorsel: o.emoji || o.svg || '', dogru: !!o.correct })));
    return liste;
  }

  function dogruKumesi(g) {
    const c = g.cfg || {};
    const k = new Set((c.correct || []).map(String));
    (c.items || []).forEach(i => { if (i.correct) k.add(String(i.id)); });
    return k;
  }

  const svgVar = (o) => /<svg/i.test(JSON.stringify(o || {}));

  /* ---- KURAL 1: cevap etikette yazılı ------------------------------
     Yönergede geçen sayı/özellik, doğru ögenin etiketinde birebir
     yazıyorsa çocuk gözlem yapmadan okuyarak seçer. */
  function k1_cevapEtiketteYazili(g) {
    const yon = dz(g.cfg && g.cfg.instruction);
    const liste = ogeler(g);
    if (liste.length < 2) return null;
    const dogrular = dogruKumesi(g);

    /* a) parantez içinde sayı+birim ya da özellik: "(4 çizgi)", "(ters)" */
    const parantezli = liste.filter(o => /\(\s*(\d+\s*\p{L}+|ters|yamuk|uzun|kısa|düz|eğik|geniş|dar)\s*\)/iu.test(o.etiket));
    if (parantezli.length >= 2)
      return 'ögelerin etiketinde cevap yazılı: ' + parantezli.slice(0, 3).map(o => '"' + o.etiket + '"').join(', ');

    /* b) yönergedeki sayı yalnızca doğru ögenin etiketinde geçiyor */
    const yonSayilar = sayilar(yon);
    if (yonSayilar.length && dogrular.size) {
      for (const n of yonSayilar) {
        const iceren = liste.filter(o => sayilar(o.etiket).indexOf(n) >= 0);
        if (!iceren.length) continue;
        const hepsiDogru = iceren.every(o => dogrular.has(String(o.id)) || o.dogru);
        const digerleriYok = liste.length - iceren.length >= 1;
        if (hepsiDogru && digerleriYok && iceren.length < liste.length)
          return 'yönergedeki "' + n + '" sayısı yalnız doğru ögenin etiketinde yazıyor (okuyarak bulunur)';
      }
    }
    return null;
  }

  /* ---- KURAL 2: ayırt edilemez ögeler ------------------------------ */
  function k2_ayirtEdilemez(g) {
    if (!(g.cfg && g.cfg.items)) return null;
    if (g.cfg.anyOf) return null;                 /* "herhangi N tanesi" kuralı */
    const dogrular = dogruKumesi(g);
    if (!dogrular.size) return null;
    const grup = {};
    (g.cfg.items || []).forEach(i => {
      const k = dz(i.label) + '||' + String(i.emoji || '');
      (grup[k] = grup[k] || []).push(dogrular.has(String(i.id)));
    });
    const kotu = Object.entries(grup).filter(([k, v]) => v.length > 1 && new Set(v).size > 1);
    if (kotu.length)
      return 'aynı görünen ögelerin bazısı doğru bazısı yanlış: ' +
        kotu.map(([k, v]) => '"' + k.split('||')[0].slice(0, 16) + '" ×' + v.length).join(', ');
    return null;
  }

  /* ---- KURAL 3: karşılaştırılacak görsel yok -----------------------
     Yönerge bir ÖLÇÜTE atıfta bulunuyor ("izde 4 çizgi var", "soldaki
     şekil", "yukarıdaki örüntü") ama o ölçüt ekranda çizilmiyor. */
  const OLCUT_KALIP = /(izde|izdeki|soldaki|sağdaki|yukarıdaki|aşağıdaki|ekrandaki|resimdeki|şekildeki|örnekteki|kutudaki|tabaktaki)\s/i;
  function k3_olcutGorseliYok(g) {
    const c = g.cfg || {};
    const yon = dz(c.instruction);
    if (!OLCUT_KALIP.test(yon)) return null;
    /* ölçüt görseli sayılabilecek alanlar */
    const olcutAlan = c.reference || c.model || c.target || c.pattern || c.actualDisplay || c.prompt;
    if (olcutAlan) return null;
    if (svgVar(c)) return null;                   /* çizim var, muhtemelen gösteriliyor */
    return 'yönerge bir ölçüte atıf yapıyor ("' + (yon.match(OLCUT_KALIP) || [''])[0].trim() +
           '…") ama o görsel katalogda yok — çocuk neyle karşılaştıracak?';
  }

  /* ---- KURAL 4: içerik sığ ----------------------------------------- */
  function k4_icerikSig(g) {
    const c = g.cfg || {};
    if (g.type === 'choiceQuestion') {
      const adim = (c.steps || []).filter(s => s && s.options);
      if (adim.length === 1 && (adim[0].options || []).length <= 2)
        return 'tek soru, iki seçenek — oyun birkaç saniyede biter';
      if (adim.length === 1) return 'tek soruluk oyun (içerik sığ)';
    }
    const n = (c.items || []).length;
    if ((g.type === 'tapSelect' || g.type === 'beltSort') && n && n < 3)
      return 'yalnız ' + n + ' öge var';
    return null;
  }

  /* ---- KURAL 5: yönerge verisiyle uyuşmuyor ------------------------ */
  function k5_yonergeVeriUyusmaz(g) {
    const c = g.cfg || {};
    const yon = dz(c.instruction);
    const dogrular = dogruKumesi(g);
    /* "4 koyuna dokun" gibi sayı emri: doğru sayısıyla tutuyor mu? */
    const emir = yon.match(/(\d+)\s*(?:tane\s*)?\p{L}*(?:'?[a-zçğıöşü]*)\s*(?:dokun|seç|yakala|topla|bul)/iu);
    if (emir && dogrular.size) {
      const istenen = Number(emir[1]);
      const hedef = c.anyOf ? Number(c.anyOf) : dogrular.size;
      if (istenen !== hedef)
        return 'yönerge ' + istenen + ' istiyor ama veride ' + hedef + ' doğru tanımlı';
    }
    return null;
  }

  /* ---- KURAL 6: doğru cevap tanımsız ------------------------------- */
  function k6_dogruYok(g) {
    const c = g.cfg || {};
    if (['tapSelect'].indexOf(g.type) >= 0 && !c.anyOf && !dogruKumesi(g).size)
      return 'doğru cevap tanımlı değil';
    if (g.type === 'choiceQuestion') {
      const eksik = (c.steps || []).filter(s => s && s.options && !s.options.some(o => o.correct));
      if (eksik.length) return eksik.length + ' adımda doğru seçenek işaretlenmemiş';
    }
    return null;
  }

  const KURALLAR = [
    ['cevap-etikette', k1_cevapEtiketteYazili],
    ['ayirt-edilemez', k2_ayirtEdilemez],
    ['olcut-gorseli-yok', k3_olcutGorseliYok],
    ['icerik-sig', k4_icerikSig],
    ['yonerge-uyusmaz', k5_yonergeVeriUyusmaz],
    ['dogru-yok', k6_dogruYok]
  ];

  function tara(sec) {
    sec = sec || {};
    const hepsi = (kok.ALL_GAMES || []).map(x => kok.getGame(x.id)).filter(g => g &&
      (sec.grade == null || g.grade === sec.grade) &&
      (sec.subj == null || g.subj === sec.subj));
    const bulgular = [];
    hepsi.forEach(g => {
      KURALLAR.forEach(([ad, f]) => {
        let s = null;
        try { s = f(g); } catch (e) { s = 'kural hatası: ' + e.message; }
        if (s) bulgular.push({ id: g.id, sinif: g.grade, ders: g.subj, ad: g.title, tip: g.type, kural: ad, aciklama: s });
      });
    });
    return bulgular;
  }

  function ozet(bulgular) {
    const k = {};
    bulgular.forEach(b => { (k[b.kural] = k[b.kural] || []).push(b.id); });
    return Object.entries(k).map(([ad, v]) => ad + ': ' + v.length + ' → ' + v.slice(0, 14).join(',') + (v.length > 14 ? '…' : '')).join('\n');
  }

  kok.ANLAM = { tara, ozet, KURALLAR };
})(window);
