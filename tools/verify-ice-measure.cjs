'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/dondurma-olcum-denetimi');
const sizes=[[320,568],[390,844],[844,390]],ids=['m18','m36'];
async function drag(page,source,target,cancel=false){
 const a=await source.boundingBox(),b=await target.boundingBox();assert(a&&b,'sürükleme koordinatları');
 await page.mouse.move(a.x+a.width/2,a.y+a.height/2);await page.mouse.down();await page.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:9});
 if(cancel)await source.dispatchEvent('pointercancel',{pointerId:1});
 await page.mouse.up();
}
(async()=>{
 fs.mkdirSync(OUT,{recursive:true});const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 const records=[],errors=[];
 try{for(const id of ids)for(const [width,height] of sizes){
  const page=await browser.newPage({viewport:{width,height}});page.on('pageerror',e=>errors.push(`${id} ${width}: ${e.message}`));
  await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser/matematik-pdf.html')).href+`?test=1&ice-measure#oyun=${id}`);
  for(let round=0;round<3;round++){
   await page.waitForFunction(i=>roundIndex===i&&!locked&&!!document.querySelector('[data-piece]'),round,{timeout:6000});
   const geom=await page.evaluate(()=>{const visual=document.querySelector('#visual').getBoundingClientRect(),source=document.querySelector('[data-piece]').getBoundingClientRect(),targets=[...document.querySelectorAll('#visual [data-target]')].map(e=>e.getBoundingClientRect());return {horizontal:document.documentElement.scrollWidth>innerWidth+1,promptClipped:document.querySelector('.prompt').scrollHeight>document.querySelector('.prompt').clientHeight+2,source:{top:source.top,bottom:source.bottom,width:source.width,height:source.height},targets:targets.map(b=>({left:b.left,right:b.right,top:b.top,bottom:b.bottom,width:b.width,height:b.height})),visual:{left:visual.left,right:visual.right,top:visual.top,bottom:visual.bottom}}});
   assert(!geom.horizontal&&!geom.promptClipped,JSON.stringify({id,width,height,round,geom}));
   assert(geom.source.width>=44&&geom.source.height>=44&&geom.source.top>=0&&geom.source.bottom<=height+2,JSON.stringify({id,width,height,round,source:geom.source}));
   assert(geom.targets.every(b=>b.width>=44&&b.height>=40&&b.left>=geom.visual.left&&b.right<=geom.visual.right&&b.top>=geom.visual.top&&b.bottom<=geom.visual.bottom),JSON.stringify({id,width,height,round,targets:geom.targets,visual:geom.visual}));
   const stem=`${id}-${width}x${height}-tur${round+1}`;await page.screenshot({path:path.join(OUT,stem+'.png')});
   if(id==='m18'){
    if(round===0){const top=await page.evaluate(()=>round().pieces.find(p=>p.target==='p'+round().targets.length).id);
     await drag(page,page.locator(`[data-piece="${top}"]`),page.locator(`[data-target="p${geom.targets.length}"]`));
     assert.equal(await page.locator('.ice-scoop-slot .placed span').count(),0,`${stem} üst kat erkenden doldu`);
     await page.waitForTimeout(420)}
    for(let i=1;i<=geom.targets.length;i++){
     const piece=await page.evaluate(i=>round().pieces.find(p=>p.target==='p'+i).id,i);
     await drag(page,page.locator(`[data-piece="${piece}"]`),page.locator(`[data-target="p${i}"]`));
     await page.waitForFunction(({count,ri})=>roundIndex>ri||Object.keys(state.placed||{}).length===count,{count:i,ri:round},{timeout:2200});
     if(await page.evaluate(i=>roundIndex===i,round))assert.equal(await page.locator('.ice-scoop-slot .placed span').count(),i,`${stem} top yerleşmedi`);
    }
   }else{
    const total=await page.evaluate(()=>round().targetCount);
    await drag(page,page.locator('[data-piece="supply"]'),page.locator('.measurement-workbench header'));
    assert.equal(await page.evaluate(()=>state.loaded),0,`${stem} ölçüm çizgisi dışı kabul edildi`);
    for(let i=1;i<=total;i++){
     await drag(page,page.locator('[data-piece="supply"]'),page.locator('.measurement-workbench [data-target="loadTarget"]'));
     const seen=await page.evaluate(()=>({loaded:state.loaded,roundIndex,lives,locked,feedback:document.querySelector('#feedback')?.textContent}));
     if(seen.loaded!==i){await page.screenshot({path:path.join(OUT,stem+'-hata.png')});throw Error(`${stem} ataş ${i} yerleşmedi: ${JSON.stringify(seen)}`)}
     if(i<total)assert.equal(await page.locator('.measurement-workbench .clip-ruler i.filled').count(),i,`${stem} görsel sayacı yanlış`);
    }
   }
   await page.waitForTimeout(400);
   await page.screenshot({path:path.join(OUT,stem+'-sonuc.png')});records.push({id,viewport:`${width}x${height}`,round:round+1,realDrag:true,wrongRejected:id==='m36'||round===0,geometry:geom});
   if(round<2)await page.waitForFunction(i=>roundIndex===i+1&&!locked,round,{timeout:6000});
  }
  await page.waitForFunction(()=>!!document.querySelector('.overlay'),null,{timeout:6000});
  await page.locator('.overlay button').click();
  assert(await page.evaluate(()=>roundIndex===0&&lives===3&&!locked),`${id} ${width} tekrar başlatma başarısız`);
  await page.close();
 }
 assert.deepEqual(errors,[]);fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({checks:records,errors},null,2));
 fs.writeFileSync(path.join(OUT,'index.html'),`<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dondurma ve ölçüm denetimi</title><style>body{font:16px system-ui;background:#edf3f5;color:#183b50;margin:20px}main{max-width:1240px;margin:auto}section{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}article{background:white;padding:12px;border-radius:14px}img{width:100%;height:auto}a{color:#12698b}</style><main><h1>M18 Dondurma Kulesi · M36 Kırtasiye Ölçümü</h1><p>Üç tur, üç ekran boyutu, gerçek sürükleme ve yanlış hedef kontrolü. Bu iki oyun için hedefli kabul kanıtıdır; 635 oyunun toplu tasarım onayı değildir.</p><section>${records.map(r=>{const stem=`${r.id}-${r.viewport}-tur${r.round}`;return `<article><h2>${r.id.toUpperCase()} · ${r.viewport} · tur ${r.round}</h2><a href="${stem}.png"><img loading="lazy" src="${stem}.png" alt="Başlangıç"></a><a href="${stem}-sonuc.png">Yerleştirme sonucunu gör</a></article>`}).join('')}</section></main>`);
 console.log(JSON.stringify({passed:records.length,errors}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
