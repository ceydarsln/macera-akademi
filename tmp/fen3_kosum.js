/* fen3 otomatik koşum: her oyunun her turunu doğru hamlelerle bitirir.
   Konsolda: kosum(['g01',...]) → {id:'ok'|hata} döner.
   Kartların/etiketlerin ekran dizilişi tohumla karıştığı için hamleler
   DOM'dan değil veri modelinden (round()) seçilir; data-* dizinleri
   gerçek veri dizinini taşır. */
window.kosum=function(idler){
 const sonuc={};
 const bekle=ms=>new Promise(r=>setTimeout(r,ms));
 /* arka plan sekmesinde requestAnimationFrame hiç ateşlenmiyor: bekleme
    yalnız setTimeout üzerinden yapılır (motorun ?test=1 yaması sayesinde
    gizli sekmede de kısıtlanmadan çalışır). */
 const tik=()=>bekle(30);
 async function hamle(){
  const r=round(); if(!r)return false;
  if(state.gecis||locked||state.yuruyor)return true;
  const tikla=s=>{const e=document.querySelector(s);if(!e)throw new Error('bulunamadı: '+s);e.click();return true};
  switch(r.kind){
   case 'sinifla': return tikla(`[data-kutu="${r.kartlar[state.ix||0].dogru}"]`);
   case 'sira':    return tikla(`[data-kart="${r.dogru[(state.dizi||[]).length]}"]`);
   case 'karar': {
    const g=state.faz===1&&r.neden, sec=g?r.neden.secenekler:r.secenekler;
    return tikla(`[data-${g?'neden':'sec'}="${sec.findIndex(s=>s.correct)}"]`)}
   case 'esle': {
    const i=state.yerlesen.findIndex(v=>v==null);
    if(state.secEt==null)return tikla(`[data-et="${r.yuvalar[i].dogru}"]`);
    return tikla(`[data-yuva="${i}"]`)}
   case 'topla': {
    const j=r.gerekli.find(x=>(state.alinan||[]).indexOf(x)<0);
    return tikla(`[data-oge="${j}"]`)}
   case 'hafiza': {
    if(state.dogrula!=null)
     return tikla(`[data-hs="${r.ciftler[state.dogrula].secenekler.findIndex(s=>s.correct)}"]`);
    const hedef=r.ciftler.findIndex((c,i)=>(state.eslesti||[]).indexOf(i)<0);
    const yerler=[];state.kartlar.forEach((k,i)=>{if(k.cift===hedef)yerler.push(i)});
    const acik=state.acik||[];
    if(acik.length>=2)return true;
    return tikla(`[data-hk="${yerler[acik.length]}"]`)}
   case 'grafik': {
    const i=r.gruplar.findIndex((g,j)=>state.kondu[j]<g.sayi);
    return tikla(`[data-sut="${i}"]`)}
   case 'olcum': {
    const s=document.getElementById('olcek');s.value=r.dogru;s.oninput();
    return tikla('#olcOk')}
   case 'sula': {
    state.verilen=Math.round((r.uygunAlt+r.uygunUst)/2);
    return tikla('#sulaOk')}
   case 'tus': {
    const d=String(r.dogru);
    if((state.giris||'')===d)return tikla('[data-tus="ok"]');
    return tikla(`[data-tus="${d[(state.giris||'').length]}"]`)}
   case 'cumle': {
    if(state.faz===1)return tikla(`[data-bit="${r.bitirme.findIndex(b=>b.correct)}"]`);
    const dz=state.dizi||[];
    const yol=r.kabul.find(k=>dz.every((v,j)=>k[j]===v));
    return tikla(`[data-kel="${yol[dz.length]}"]`)}
   case 'gozlem': {
    if(state.soruNokta!=null)
     return tikla(`[data-gs="${r.noktalar[state.soruNokta].secenekler.findIndex(s=>s.correct)}"]`);
    const hedef=r.noktalar.findIndex((n,i)=>(state.kayit||[]).indexOf(i)<0);
    const n=r.noktalar[hedef],p=state.pos;
    if(!(state.prog||[]).length){
     const yol=[];let dx=n.x-p[0],dy=n.y-p[1];
     while(dy<0){yol.push('⬆️');dy++} while(dy>0){yol.push('⬇️');dy--}
     while(dx<0){yol.push('⬅️');dx++} while(dx>0){yol.push('➡️');dx--}
     if(n.yol)yol.length=0,n.yol.forEach(y=>yol.push(y));
     for(const y of yol)document.querySelector(`[data-yon="${y}"]`).click();
    }
    return tikla('[data-yon="git"]')}
   case 'yaz': {
    state.yazi=r.ornekCevap;renderYaz(r);state.yazi=r.ornekCevap;
    const ta=document.getElementById('yaziAlan');ta.value=r.ornekCevap;ta.oninput();
    return tikla('#yazOk')}
  }
  throw new Error('bilinmeyen tur türü: '+r.kind)}
 return (async()=>{
  for(const id of idler){
   try{
    game=GAMES[id];roundIndex=0;lives=3;score=0;locked=false;render();await tik();
    let adim=0;
    while(roundIndex<3&&adim++<400){await hamle();await bekle(18)}
    if(roundIndex<3)throw new Error('tur '+(roundIndex+1)+' bitmedi ('+round().kind+')');
    if(lives<3)throw new Error('can kaybı oldu');
    sonuc[id]='ok';
   }catch(e){sonuc[id]='HATA: '+e.message}
  }
  return sonuc})()};
