'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/sayi-cizimi-buyutme-denetimi');
async function trace(page,ri){
 for(let stroke=0;stroke<8;stroke++){
  const s=await page.evaluate(()=>({ri:roundIndex,locked,hamle:state.hamle,total:state.yollar?.length,p:document.querySelector('#izKatman .trace-ink-layer')?izNoktaEkran():null}));
  if(s.ri!==ri||s.locked||!s.p||s.hamle>=s.total)return;
  await page.mouse.move(s.p[0],s.p[1]);await page.mouse.down();
  for(let i=0;i<100;i++){
   const n=await page.evaluate(()=>({ri:roundIndex,locked,hamle:state.hamle,p:document.querySelector('#izKatman .trace-ink-layer')?izNoktaEkran():null}));
   if(n.ri!==ri||n.locked||n.hamle!==s.hamle||!n.p)break;
   await page.mouse.move(n.p[0],n.p[1],{steps:2});
  }
  await page.mouse.up();
 }
 throw Error('Çizim tamamlanmadı: '+JSON.stringify(await page.evaluate(()=>({id:GAME_ID,roundIndex,hamle:state.hamle,adim:state.adim,total:state.yollar?.length,faz:state.faz,basli:state.basli,point:izNoktaEkran(),viewport:[innerWidth,innerHeight]}))));
}
(async()=>{fs.mkdirSync(OUT,{recursive:true});const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});const records=[],errors=[];
try{for(const id of [...Array.from({length:10},(_,i)=>'s'+i),'s10','n1','n9'])for(const [width,height] of [[320,568],[390,844],[844,390]]){
 const page=await browser.newPage({viewport:{width,height}});page.on('pageerror',e=>errors.push(`${id}: ${e.message}`));await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser/sayma-pdf.html')).href+'?test=1#oyun='+id);
 for(let ri=0;ri<3;ri++){
  await page.waitForFunction(i=>roundIndex===i&&!locked,ri);const stem=`${id}-${width}x${height}-tur${ri+1}`;
  const writing=await page.evaluate(()=>round().kind==='yaz');
  if(writing){
   if(await page.evaluate(()=>round().nesneOnce)){
    const total=await page.evaluate(()=>({t:Math.floor(state.hedef/10),u:state.hedef%10}));
    for(let i=0;i<total.t;i++)await page.locator(`[data-demet="${i}"]`).click();
    for(let i=0;i<total.u;i++)await page.locator(`[data-birlik="${i}"]`).click();
   }
   await page.locator('[data-rakam]').first().waitFor();const num=await page.evaluate(()=>String(state.hedef));
   for(let digit=0;digit<num.length;digit++){
    await page.locator(`[data-rakam="${num[digit]}"]`).click();await page.locator('#izKatman').waitFor();
    if(digit===0)await page.screenshot({path:path.join(OUT,stem+'.png')});await trace(page,ri);
    if(digit<num.length-1)await page.locator('[data-rakam]').first().waitFor();
   }
   await page.locator('#yazOk').waitFor();await page.locator('#yazOk').click();
  }else{
   await page.locator('#izKatman').waitFor();
   const geom=await page.evaluate(()=>{const stage=document.querySelector('#stage').getBoundingClientRect(),svg=document.querySelector('#izKatman svg').getBoundingClientRect(),start=izNoktaEkran(),p=document.querySelector('.prompt');return {width:svg.width,height:svg.height,start,clipped:svg.left<stage.left||svg.right>stage.right||svg.top<stage.top||svg.bottom>stage.bottom||svg.bottom>innerHeight,promptClipped:p.scrollHeight>p.clientHeight+2,scale:document.querySelector('.trace-ink-layer').getAttribute('transform')}});
   assert(!geom.clipped&&!geom.promptClipped,JSON.stringify({stem,geom}));assert(geom.scale.includes('scale(1.3)'));await page.screenshot({path:path.join(OUT,stem+'.png')});
   // Start away from the target, then cancel. Neither may advance or cost a life.
   const b=await page.locator('#izKatman svg').boundingBox();await page.mouse.move(b.x+2,b.y+2);await page.mouse.down();await page.mouse.up();assert(await page.evaluate(()=>state.adim===0&&lives===3));
   const p=await page.evaluate(()=>izNoktaEkran());await page.mouse.move(...p);await page.mouse.down();const adim=await page.evaluate(()=>state.adim);await page.locator('#izKatman svg').dispatchEvent('pointercancel',{pointerId:1});await page.mouse.move(p[0]+30,p[1]+30);await page.mouse.up();assert(await page.evaluate(a=>state.adim===a&&!state.basli,adim));
   await trace(page,ri);
   if(ri===2){await page.waitForFunction(()=>state.faz===1&&!!document.querySelector('[data-choice],[data-nesne]'));const n=await page.evaluate(()=>round().sayimHedef);for(let i=0;i<n;i++)await page.locator(`[data-nesne="${i}"]`).click();const c=await page.evaluate(()=>round().sayimSec.findIndex(c=>c.correct));await page.locator(`[data-choice="${c}"]`).click()}
  }
  records.push({id,viewport:`${width}x${height}`,round:ri+1,realPointerDrawing:true});
 }
 await page.waitForSelector('.overlay');await page.locator('.overlay button').click();await page.waitForFunction(()=>roundIndex===0&&!locked&&lives===3);await page.close();
}
assert.deepEqual(errors,[]);fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({records,errors},null,2));fs.writeFileSync(path.join(OUT,'index.html'),`<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Büyük sayı çizimleri</title><style>body{font:16px system-ui;margin:20px;background:#eef4f6;color:#29465a}section{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:15px}article{background:white;padding:12px;border-radius:12px}img{width:100%}</style><h1>Sayı çizimi alanları</h1><p>${records.length} tur/ekran senaryosu; 0–9 rakamları ve üç iki-basamaklı temsilci. Gerçek fare çizimi; rakamlarda yanlış başlangıç/iptal, üç kılavuz düzeyi, miktar eşleme ve yeniden başlatma. Fiziksel telefon testi değildir.</p><section>${records.map(r=>`<article><h2>${r.id} · ${r.viewport} · tur ${r.round}</h2><img loading="lazy" src="${r.id}-${r.viewport}-tur${r.round}.png"><a href="../../app/src/main/assets/phaser/sayma-pdf.html#oyun=${r.id}">Oyunu oyna</a></article>`).join('')}</section>`);console.log(JSON.stringify({passed:records.length,errors}));
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
