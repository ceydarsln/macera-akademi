/* =====================================================================
   MACERA AKADEMİ — BİRLEŞİK TEST KOŞUCUSU

   Uygulama sayfasının konsolunda tek satırla yükle:
     await (0,eval)(await (await fetch('/tools/macera_test.js')).text())

   Ardından:
     await MACERA_TEST.baslat()                         // tüm katalog + anlam
     await MACERA_TEST.baslat({ idler:['m01','u04'] }) // seçili oyunlar
     MACERA_TEST.durum()                               // ilerleme
     await MACERA_TEST.bekle()                         // bitiş raporu

   Bu giriş noktası üç eski aracın uzmanlığını korur:
     · KOSUM  — genel Phaser mekaniklerini gerçekten oynar
     · SINAMA — on beş özel mekanik için ayrıntılı oyuncuları çalıştırır
     · ANLAM  — katalog görevlerinin içerik tutarlılığını tarar
   Sonuçlar test-results/ altında tek JSON dosyasına yazılır.
   ===================================================================== */
(async function (kok) {
  'use strict';

  const SURUM = '1.1.0';
  if (kok.MACERA_TEST && kok.MACERA_TEST.surum === SURUM) {
    await kok.MACERA_TEST.hazirla();
    return kok.MACERA_TEST;
  }

  const KAYNAKLAR = [
    '/tools/ucuncu_sinama.js',
    '/tools/kosum.js',
    '/tools/anlam_denetimi.js'
  ];

  const OZEL_OYUNCULAR = {
    catchDrop: 'oynaCatchDrop',
    sentenceBuild: 'oynaSentenceBuild',
    punctFix: 'oynaPunctFix',
    codeGrid: 'oynaCodeGrid',
    wordHighlight: 'oynaWordHighlight',
    jumpPath: 'oynaJumpPath',
    numPad: 'oynaNumPad',
    graphBuild: 'oynaGraphBuild',
    dragSlider: 'oynaDragSlider',
    fractionCut: 'oynaFractionCut',
    clockSet: 'oynaClockSet',
    moneyBuild: 'oynaValueBuild',
    placeValueLoad: 'oynaValueBuild',
    drawSegments: 'oynaDrawSegments',
    solidScan: 'oynaSolidScan',
    numberTrace: 'oynaRakam',
    numberWrite: 'oynaRakam',
    tallyChart: 'oynaCetele',
    surveyChart: 'oynaCetele',
    holdFill: 'oynaHoldFill',
    mirrorGrid: 'oynaSimetri',
    foldMirror: 'oynaSimetri',
    tiltBalance: 'oynaTerazi',
    balanceScale: 'oynaTerazi',
    patternFill: 'oynaOruntu',
    countToTarget: 'oynaOruntu',
    groupMultiply: 'oynaPaketleme',
    shareDivide: 'oynaPaketleme',
    typeWord: 'oynaTypeWord'
  };

  /* v40 grafiği katalogdaki HTML çizimini kullandığı için bilerek DOM'da
     kalıyor. Phaser şartına takılmadan kendi oyuncusuna yönlendir. */
  const DOM_OYUNCULAR = { v40: 'oynaDomChoiceQuestion' };

  const GENEL_TIPLER = new Set([
    'beltSort', 'dragMatch', 'tapSelect', 'choiceQuestion',
    'estimateReveal', 'memoryPairs', 'serveOrder', 'orderSequence'
  ]);
  const OZEL_SAHNELER = new Set(['m02', 'm03', 'm04', 'm05', 'm06', 'm07', 'm16', 'm19']);

  const durum = {
    hal: 'yükleniyor',
    faz: 'araçlar',
    kosuId: null,
    baslangic: null,
    bitis: null,
    toplam: 0,
    biten: 0,
    aktifOyun: null,
    iptal: false,
    hata: null,
    rapor: null,
    soz: null,
    hazirlik: null
  };

  const bekle = (ms) => new Promise(coz => setTimeout(coz, ms));
  const iki = (n) => String(n).padStart(2, '0');
  const damga = (d) => d.getFullYear() + iki(d.getMonth() + 1) + iki(d.getDate()) + '-' +
    iki(d.getHours()) + iki(d.getMinutes()) + iki(d.getSeconds());

  async function kaynakYukle(yol) {
    const ayirac = yol.indexOf('?') >= 0 ? '&' : '?';
    const yanit = await fetch(yol + ayirac + 'v=' + Date.now(), { cache: 'no-store' });
    if (!yanit.ok) throw new Error(yol + ' yüklenemedi: HTTP ' + yanit.status);
    const kod = await yanit.text();
    (0, eval)(kod);
  }

  async function hazirla(zorla) {
    if (durum.hazirlik && !zorla) return durum.hazirlik;
    durum.hazirlik = (async () => {
      durum.hal = 'yükleniyor'; durum.faz = 'araçlar'; durum.hata = null;
      for (const yol of KAYNAKLAR) await kaynakYukle(yol);
      if (!kok.SINAMA || !kok.KOSUM || !kok.ANLAM)
        throw new Error('Test araçlarından biri küresel alana kurulamadı');
      kok.KOSUM.kur();
      durum.hal = 'hazır'; durum.faz = null;
      return API;
    })().catch(e => {
      durum.hal = 'hata'; durum.hata = String(e && e.stack || e);
      durum.hazirlik = null;
      throw e;
    });
    return durum.hazirlik;
  }

  function katalog() {
    let ham;
    try { ham = ALL_GAMES; }
    catch (e) { ham = kok.ALL_GAMES || []; }
    if (!Array.isArray(ham) || !ham.length)
      throw new Error('ALL_GAMES bulunamadı; koşucuyu uygulama sayfasında yükle');
    return ham.map(x => kok.getGame(x.id)).filter(Boolean);
  }

  const diziMi = (v) => Array.isArray(v) ? v : (v == null ? null : [v]);
  function seciliOyunlar(sec) {
    sec = sec || {};
    const idler = diziMi(sec.idler);
    const siniflar = diziMi(sec.sinif == null ? sec.grade : sec.sinif);
    const dersler = diziMi(sec.ders == null ? sec.subj : sec.ders);
    const tipler = diziMi(sec.tipler == null ? sec.tip : sec.tipler);
    const idK = idler && new Set(idler.map(String));
    const sinifK = siniflar && new Set(siniflar.map(Number));
    const dersK = dersler && new Set(dersler.map(String));
    const tipK = tipler && new Set(tipler.map(String));
    return katalog().filter(g =>
      (!idK || idK.has(String(g.id))) &&
      (!sinifK || sinifK.has(Number(g.grade))) &&
      (!dersK || dersK.has(String(g.subj))) &&
      (!tipK || tipK.has(String(g.type)))
    );
  }

  function motor(g) {
    if (DOM_OYUNCULAR[g.id]) return { ad: 'sinama', oyuncu: DOM_OYUNCULAR[g.id] };
    let phaser = false;
    try { phaser = !!kok.phaserOyunuMu(g); } catch (e) {}
    if (!phaser) return { ad: 'yok', neden: 'DOM oyunu için otomatik oyuncu yok' };
    if (OZEL_OYUNCULAR[g.type]) return { ad: 'sinama', oyuncu: OZEL_OYUNCULAR[g.type] };
    if (GENEL_TIPLER.has(g.type) || OZEL_SAHNELER.has(g.id)) return { ad: 'kosum' };
    return { ad: 'yok', neden: g.type + ' için otomatik oyuncu yok' };
  }

  function ortak(g, motorAdi, ham) {
    const sonuc = motorAdi === 'kosum' ? ham.durum : ham.sonuc;
    return {
      id: g.id,
      ad: g.title,
      sinif: g.grade,
      ders: g.subj,
      tip: g.type,
      motor: motorAdi,
      durum: sonuc || 'BİTMEDİ',
      basarili: sonuc === 'TAMAM',
      ayrinti: ham
    };
  }

  function desteksiz(g, neden) {
    return {
      id: g.id,
      ad: g.title,
      sinif: g.grade,
      ders: g.subj,
      tip: g.type,
      motor: 'yok',
      durum: 'DESTEKLENMİYOR',
      basarili: false,
      ayrinti: { neden }
    };
  }

  async function kosumCalistir(oyunlar, sonuclar) {
    if (!oyunlar.length || durum.iptal) return;
    durum.faz = 'kosum';
    const once = durum.biten;
    kok.KOSUM.sirala(oyunlar.map(g => g.id));
    while (kok.KOSUM.calisiyor) {
      durum.biten = once + kok.KOSUM.rapor.length;
      const siradaki = oyunlar[kok.KOSUM.rapor.length];
      durum.aktifOyun = siradaki ? siradaki.id : null;
      if (durum.iptal) kok.KOSUM.kuyruk.length = 0;
      await bekle(200);
    }
    const oyunHaritasi = new Map(oyunlar.map(g => [g.id, g]));
    kok.KOSUM.rapor.forEach(r => {
      const g = oyunHaritasi.get(r.id);
      if (g) sonuclar.push(ortak(g, 'kosum', r));
    });
    durum.biten = once + kok.KOSUM.rapor.length;
  }

  async function sinamaCalistir(oyunlar, sonuclar) {
    if (!oyunlar.length || durum.iptal) return;
    durum.faz = 'sinama';
    for (const g of oyunlar) {
      if (durum.iptal) break;
      durum.aktifOyun = g.id;
      let ham;
      try {
        const oyuncu = DOM_OYUNCULAR[g.id] || OZEL_OYUNCULAR[g.type];
        ham = await kok.SINAMA[oyuncu](g.id);
      } catch (e) {
        ham = { id: g.id, sonuc: 'ÇÖKTÜ', hata: [String(e && e.stack || e)] };
      }
      sonuclar.push(ortak(g, 'sinama', ham));
      durum.biten++;
      await bekle(0);
    }
  }

  async function kaydet(ad, veri, ekle) {
    const guvenli = String(ad || '').replace(/[^a-zA-Z0-9._-]/g, '_');
    if (!guvenli) throw new Error('Rapor dosyası adı boş olamaz');
    const yol = '/kaydet?ad=' + encodeURIComponent(guvenli) + (ekle ? '&tek=1' : '');
    const govde = typeof veri === 'string' ? veri : JSON.stringify(veri, null, 2);
    const yanit = await fetch(yol, { method: 'POST', body: govde });
    if (!yanit.ok) throw new Error('Rapor yazılamadı: HTTP ' + yanit.status);
    return guvenli;
  }

  function ozetle(rapor) {
    const mekanik = rapor.mekanik || [];
    return {
      planlanan: rapor.planlanan,
      mekanikSonuc: mekanik.length,
      tamam: mekanik.filter(x => x.basarili).length,
      sorunlu: mekanik.filter(x => !x.basarili && x.durum !== 'DESTEKLENMİYOR').length,
      desteklenmeyen: mekanik.filter(x => x.durum === 'DESTEKLENMİYOR').length,
      anlamBulgusu: (rapor.anlam || []).length,
      iptal: !!rapor.iptal
    };
  }

  async function calistir(sec) {
    const oyunlar = seciliOyunlar(sec);
    const kip = sec.kip || 'tum';
    const mekanikAcik = kip !== 'anlam';
    const anlamAcik = sec.anlam == null ? (kip === 'tum' || kip === 'anlam') : !!sec.anlam;
    const mekanik = [];
    const genel = [], ozel = [];

    if (mekanikAcik) {
      oyunlar.forEach(g => {
        const m = motor(g);
        if (kip === 'genel' && m.ad !== 'kosum') return;
        if (kip === 'ozel' && m.ad !== 'sinama') return;
        if (m.ad === 'kosum') genel.push(g);
        else if (m.ad === 'sinama') ozel.push(g);
        else mekanik.push(desteksiz(g, m.neden));
      });
    }

    durum.toplam = mekanik.length + genel.length + ozel.length;
    durum.biten = mekanik.length;
    durum.faz = mekanikAcik ? 'kosum' : 'anlam';

    await kosumCalistir(genel, mekanik);
    await sinamaCalistir(ozel, mekanik);

    let anlam = [];
    if (anlamAcik && !durum.iptal) {
      durum.faz = 'anlam'; durum.aktifOyun = null;
      anlam = kok.ANLAM.tara({}, oyunlar);
    }

    const sira = new Map(oyunlar.map((g, i) => [g.id, i]));
    mekanik.sort((a, b) => (sira.get(a.id) || 0) - (sira.get(b.id) || 0));
    const rapor = {
      semaSurumu: 1,
      kosucuSurumu: SURUM,
      kosuId: durum.kosuId,
      baslangic: durum.baslangic,
      bitis: new Date().toISOString(),
      secenekler: sec,
      planlanan: oyunlar.length,
      iptal: durum.iptal,
      mekanik,
      anlam
    };
    rapor.ozet = ozetle(rapor);

    const dosya = sec.dosya === false ? null : (sec.dosya || ('macera-test-' + damga(new Date()) + '.json'));
    if (dosya) {
      try { rapor.kayit = { dosya: await kaydet(dosya, rapor) }; }
      catch (e) { rapor.kayit = { hata: String(e.message || e) }; }
    }
    return rapor;
  }

  async function baslat(sec) {
    sec = Object.assign({}, sec || {});
    await hazirla();
    if (durum.hal === 'çalışıyor') throw new Error('Bir test koşusu zaten çalışıyor');
    durum.hal = 'çalışıyor'; durum.faz = 'hazırlık'; durum.iptal = false;
    durum.kosuId = 'kosu-' + damga(new Date());
    durum.baslangic = new Date().toISOString(); durum.bitis = null;
    durum.toplam = 0; durum.biten = 0; durum.aktifOyun = null;
    durum.hata = null; durum.rapor = null;
    durum.soz = calistir(sec).then(rapor => {
      durum.rapor = rapor; durum.bitis = rapor.bitis;
      durum.hal = rapor.iptal ? 'iptal' : 'bitti'; durum.faz = null; durum.aktifOyun = null;
      return rapor;
    }).catch(e => {
      durum.hal = 'hata'; durum.faz = null; durum.aktifOyun = null;
      durum.hata = String(e && e.stack || e);
      throw e;
    });
    return API.durum();
  }

  function disDurum() {
    return {
      hal: durum.hal,
      faz: durum.faz,
      kosuId: durum.kosuId,
      baslangic: durum.baslangic,
      bitis: durum.bitis,
      toplam: durum.toplam,
      biten: durum.biten,
      kalan: Math.max(0, durum.toplam - durum.biten),
      aktifOyun: durum.aktifOyun,
      hata: durum.hata
    };
  }

  function ozet(rapor) {
    rapor = rapor || durum.rapor;
    if (!rapor) return 'Henüz tamamlanmış rapor yok.';
    const o = rapor.ozet;
    return 'TAMAM ' + o.tamam + '/' + o.mekanikSonuc +
      ' · sorunlu ' + o.sorunlu +
      ' · desteklenmeyen ' + o.desteklenmeyen +
      ' · anlam bulgusu ' + o.anlamBulgusu +
      (rapor.kayit && rapor.kayit.dosya ? '\nrapor: test-results/' + rapor.kayit.dosya : '');
  }

  const API = {
    surum: SURUM,
    hazirla,
    baslat,
    durum: disDurum,
    bekle() { return durum.soz || Promise.resolve(durum.rapor); },
    sonuc() { return durum.rapor; },
    ozet,
    kaydet,
    durdur() {
      if (durum.hal !== 'çalışıyor') return false;
      durum.iptal = true;
      if (kok.KOSUM && Array.isArray(kok.KOSUM.kuyruk)) kok.KOSUM.kuyruk.length = 0;
      return true;
    },
    listele(sec) {
      return seciliOyunlar(sec).map(g => {
        const m = motor(g);
        return { id: g.id, ad: g.title, sinif: g.grade, ders: g.subj, tip: g.type, motor: m.ad, neden: m.neden };
      });
    }
  };

  kok.MACERA_TEST = API;
  await hazirla();
  return API;
})(window);
