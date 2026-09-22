'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/sahne-duzeltmeleri-7-2026-09-21');
const cases=[{id:'f25',title:'Mıknatıs Kutusu',count:8},{id:'f26',title:'Kutuplar',count:4}];
async function drag(page,{cancel=false,outside=false}={}){
 const a=page.locator('[data-magnet-source]').first(),b=page.locator('[data-magnet-target]');await a.scrollIntoViewIfNeeded();
 const x=await a.boundingBox(),y=await b.boundingBox();const end=outside?{x:8,y:75}:{x:y.x+y.width/2,y:y.y+y.height/2};
 if(!outside)assert(await page.evaluate(()=>{const a=document.querySelector('[data-magnet-source]'),b=document.querySelector('[data-magnet-target]');return [a,b].every(e=>{const r=e.getBoundingClientRect();return e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))})}),'Kaynak veya mıknatıs başka bir kontrolün altında kaldı');
 await page.mouse.move(x.x+x.width/2,x.y+x.height/2);await page.mouse.down();await page.mouse.move(end.x,end.y,{steps:12});
 if(cancel)await a.dispatchEvent('pointercancel',{pointerId:1});await page.mouse.up();
}
async function main(){
 fs.mkdirSync(OUT,{recursive:true});const errors=[],results=[];
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 try{for(const c of cases){
  const page=await browser.newPage({viewport:{width:390,height:844}});page.on('pageerror',e=>errors.push(c.id+': '+e.message));
  await page.addInitScript(()=>{try{speechSynthesis.speak=()=>{}}catch(_){}});
  await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser/fen4-pdf.html')).href+'?magnet='+c.id+'#oyun='+c.id);
  await page.screenshot({path:path.join(OUT,c.id+'-yeni.png')});
  assert.equal(await page.locator('[data-kutu]:disabled').count(),2,'Deneyden önce cevaplar açık');
  await drag(page,{cancel:true});assert.equal(await page.evaluate(()=>state.magnetPhase),'ready');assert.equal(await page.locator('.scene-drag-ghost').count(),0);
  await drag(page,{outside:true});assert.equal(await page.evaluate(()=>state.magnetPhase),'ready');
  await page.locator('[data-magnet-source]').focus();await page.keyboard.press('Enter');await page.locator('[data-magnet-target]').focus();await page.keyboard.press('Enter');
  await page.waitForFunction(()=>state.magnetPhase==='observed');
  assert.equal(await page.evaluate(()=>state.ix),0,'Deneyi yapmak cevabı otomatik kabul etti');
  const bad=await page.evaluate(()=>1-round().kartlar[0].dogru);await page.locator('[data-kutu="'+bad+'"]').click();assert.equal(await page.evaluate(()=>state.ix),0);await page.waitForTimeout(500);
  await page.locator('[data-magnet-repeat]').click();assert.equal(await page.evaluate(()=>state.magnetPhase),'ready');assert.equal(await page.evaluate(()=>state.ix),0);
  await page.emulateMedia({reducedMotion:'reduce'});await page.evaluate(()=>render());await drag(page);
  assert(!(await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).some(n=>n.startsWith('magnet-')),'Azaltılmış harekette animasyon var');
  await page.waitForFunction(()=>state.magnetPhase==='observed');await page.emulateMedia({reducedMotion:'no-preference'});await page.evaluate(()=>render());
  const cards=await page.evaluate(()=>round().kartlar);const animations=[];
  for(let n=0;n<cards.length;n++){
   await drag(page);assert.equal(await page.evaluate(()=>state.magnetPhase),'moving');
   const names=await page.evaluate(()=>document.getAnimations().map(a=>a.animationName));const expected=c.id==='f26'?(cards[n].dogru===0?'magnet-repel':'magnet-attract'):(cards[n].dogru===0?'magnet-attract':'magnet-still');
   assert(names.includes(expected),expected+' bulunamadı');animations.push(expected);
   assert.equal(await page.locator('[data-kutu]:disabled').count(),2,'Hareket sırasında cevap açık');
   await page.waitForFunction(()=>state.magnetPhase==='observed');
   if(n<2)await page.screenshot({path:path.join(OUT,c.id+'-deney'+(n+1)+'.png')});
   await page.locator('[data-kutu="'+cards[n].dogru+'"]').click();assert.equal(await page.evaluate(()=>state.ix),n+1);
   assert.equal(await page.locator('.magnet-records li').count(),n+1);
   if(n===cards.length-1)await page.screenshot({path:path.join(OUT,c.id+'-defter.png'),fullPage:true});
   if(n<cards.length-1)await page.waitForFunction(()=>state.magnetPhase==='ready');else await page.waitForFunction(()=>roundIndex===1);
  }
  const layouts=[];
  for(const v of [{width:320,height:568},{width:390,height:844},{width:844,height:390}]){
   await page.setViewportSize(v);
   for(let i=0;i<3;i++){
    await page.evaluate(i=>{roundIndex=i;render()},i);
    const l=await page.evaluate(()=>{const s=document.querySelector('.scene'),p=document.querySelector('.prompt');return {horizontal:document.documentElement.scrollWidth>innerWidth+2||s.scrollWidth>s.clientWidth+2,prompt:p.scrollHeight>p.clientHeight+3}});
    assert(!l.horizontal&&!l.prompt,JSON.stringify({v,i,l}));layouts.push({v,round:i+1,...l});
    if(v.width===390)await page.screenshot({path:path.join(OUT,c.id+'-tur'+(i+1)+'.png')});
    if(i===0&&v.width!==390){
     await drag(page);await page.waitForFunction(()=>state.magnetPhase==='observed');
     assert.equal(await page.evaluate(()=>state.ix),0);
     await page.screenshot({path:path.join(OUT,c.id+'-deney-'+v.width+'x'+v.height+'.png')});
    }
   }
  }
  results.push({id:c.id,placements:cards.length,cancel:true,outside:true,keyboard:true,wrong:true,replay:true,reducedMotion:true,animations,layouts});await page.close();console.log('✓ '+c.id+': '+cards.length+' gerçek deney');
 }
 assert.deepEqual(errors,[]);
 fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({results,errors},null,2));
 fs.writeFileSync(path.join(OUT,'index.html'),'<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mıknatıs deneyleri</title><style>body{font:16px system-ui;background:#e1eae4;color:#253f49;margin:0}main{max-width:1200px;margin:auto;padding:24px}section{background:#fffdf5;padding:18px;margin:24px 0;border-radius:18px}.images{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}img{width:100%;border-radius:12px}figure{margin:0}figcaption{font-size:12px;padding:8px}a{color:#236579}@media(max-width:700px){.images{grid-template-columns:repeat(2,1fr)}}</style><main><h1>Yazıya değil, mıknatısın kendisine</h1><p>İlk tur: nesneyi yaklaştır → hareketi gözle → sonucu kaydet. Karar ve yazma turları korundu. Bu sahneler fiziksel simülasyon değil, öğretici ekran modelleridir. Görüntüler sabittir; animasyon için oyunu açın.</p>'+cases.map(c=>'<section><h2>'+c.id.toUpperCase()+' · '+c.title+'</h2><div class="images"><figure><figcaption>Önce</figcaption><img loading="lazy" src="../tasarim-denetimi-2026-09-21/screens/fen4-'+c.id+'.png"></figure><figure><figcaption>Yeni deney düzeneği</figcaption><img src="'+c.id+'-yeni.png"></figure><figure><figcaption>İlk deney</figcaption><img src="'+c.id+'-deney1.png"></figure><figure><figcaption>İkinci deney</figcaption><img src="'+c.id+'-deney2.png"></figure></div><p><a href="../../app/src/main/assets/phaser/fen4-pdf.html?review=magnets#oyun='+c.id+'">Oyunu aç</a> · <a href="'+c.id+'-tur2.png">2. tur</a> · <a href="'+c.id+'-tur3.png">3. tur</a></p></section>').join('')+'</main></html>');
 }finally{await browser.close()}
}
main().catch(e=>{console.error(e);process.exitCode=1});
