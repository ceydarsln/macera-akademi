'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/iksir-denetimi');
(async()=>{fs.mkdirSync(OUT,{recursive:true});const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});const records=[],errors=[];
 try{for(const id of ['m42','m49'])for(const [width,height] of [[320,568],[390,844],[844,390]]){
  const page=await browser.newPage({viewport:{width,height}});page.on('pageerror',e=>errors.push(e.message));await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser/matematik-pdf.html')).href+'?test=1#oyun='+id);
  for(let ri=0;ri<3;ri++){
   await page.waitForFunction(i=>roundIndex===i&&!locked,ri);
   const geometry=await page.evaluate(()=>{const v=document.querySelector('#visual').getBoundingClientRect(),p=document.querySelector('.prompt');return {overflow:document.documentElement.scrollWidth>innerWidth+1,promptClipped:p.scrollHeight>p.clientHeight+2,clipped:[...document.querySelectorAll('.potion-bottle,.potion-cauldron,.experiment-tube,[data-pour]')].some(e=>{const b=e.getBoundingClientRect();return b.left<v.left||b.right>v.right||b.top<v.top||b.bottom>v.bottom}),smallButton:[...document.querySelectorAll('[data-pour],[data-choice]')].some(e=>{const b=e.getBoundingClientRect();return b.width<44||b.height<44})}});
   assert(!Object.values(geometry).some(Boolean),JSON.stringify({id,width,height,ri,geometry}));const stem=`${id}-${width}x${height}-tur${ri+1}`;await page.screenshot({path:path.join(OUT,stem+'.png')});
   if(id==='m42'){
    assert(await page.locator('[data-choice]').first().isDisabled());
    for(let i=0;i<2;i++){await page.locator(`[data-pour="${i}"]`).click();await page.waitForFunction(i=>state.poured[i]&&!state.pouring,i);}
    assert.equal(await page.locator('.potion-cauldron .potion-drop').count(),[12,9,12][ri]);assert(!(await page.locator('[data-choice]').first().isDisabled()));
   }else assert.deepEqual(await page.locator('.experiment-tube').evaluateAll(es=>es.map(e=>e.children.length)),[[5,5],[8,7],[5,5]][ri]);
   const correct=await page.evaluate(()=>round().choices.findIndex(c=>c.correct));if(ri===0){await page.locator(`[data-choice="${(correct+1)%await page.locator('[data-choice]').count()}"]`).click();assert(await page.evaluate(()=>!locked&&roundIndex===0&&lives===2));await page.waitForTimeout(420)}
   await page.locator(`[data-choice="${correct}"]`).click();await page.waitForTimeout(450);if(id==='m49')assert.equal(await page.locator('.tube-compare-mark').textContent(),ri===1?'≠':'=');await page.screenshot({path:path.join(OUT,stem+'-sonuc.png')});records.push({id,viewport:`${width}x${height}`,round:ri+1,...geometry});
  }
  await page.waitForFunction(()=>!!document.querySelector('.overlay'));await page.locator('.overlay button').click();assert(await page.evaluate(()=>roundIndex===0&&lives===3&&!locked));await page.close();
 }
 assert.deepEqual(errors,[]);fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({records,errors},null,2));fs.writeFileSync(path.join(OUT,'index.html'),`<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>İksir laboratuvarları</title><style>body{font:16px system-ui;background:#edf5f3;margin:20px;color:#214c55}main{max-width:1200px;margin:auto}section{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}article{background:white;padding:12px;border-radius:14px}img{width:100%}</style><main><h1>M42 ve M49 · deney sahneleri</h1><p>18 tur/ekran senaryosu; dökme, yanlış/doğru yanıt, doğal tur geçişi ve yeniden başlatma doğrulandı. Görüntü, animasyonun kendisi değil sonuç kanıtıdır.</p><section>${records.map(r=>{const s=`${r.id}-${r.viewport}-tur${r.round}`;return `<article><h2>${r.id.toUpperCase()} · ${r.viewport} · tur ${r.round}</h2><a href="${s}.png"><img loading="lazy" src="${s}.png"></a><a href="${s}-sonuc.png">Deney sonucunu gör</a><p><a href="../../app/src/main/assets/phaser/matematik-pdf.html#oyun=${r.id}">Oyunu aç</a></p></article>`}).join('')}</section></main>`);console.log(JSON.stringify({passed:records.length,errors}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
