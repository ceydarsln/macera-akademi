'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/sahne-duzeltmeleri-9-2026-09-23');
const cases=[{id:'y52',file:'turkce3-pdf.html',title:'Eser Haritası',scene:'.map-board',source:'[data-piece]',target:'[data-target]',animation:'map-arrive'},
 {id:'g23',file:'fen3-pdf.html',title:'Geri Dönüşüm Kutuları',scene:'.recycle-yard',source:'[data-sinif-kart]',target:'[data-kutu]',animation:'recycle-fall'}];
const stateOf=page=>page.evaluate(()=>({round:roundIndex,done:state.done,ix:state.ix,score,locked}));
async function drag(page,source,target,cancel=false){
 const a=page.locator(source).first(),b=page.locator(target).first();await a.scrollIntoViewIfNeeded();
 let x=await a.boundingBox(),y=await b.boundingBox();assert(x&&y,source+' → '+target+' kutusu yok');
 assert(y.y+y.height/2>=0&&y.y+y.height/2<=page.viewportSize().height,'Hedef görünür alanda değil: '+JSON.stringify({source,target,x,y}));
 await page.mouse.move(x.x+x.width/2,x.y+x.height/2);await page.mouse.down();await page.mouse.move(y.x+y.width/2,y.y+y.height/2,{steps:10});
 if(cancel)await a.dispatchEvent('pointercancel',{pointerId:1});await page.mouse.up();
}
async function main(){
 fs.mkdirSync(OUT,{recursive:true});const errors=[],results=[];
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 try{for(const c of cases){
  const page=await browser.newPage({viewport:{width:390,height:844}});page.on('pageerror',e=>errors.push(c.id+': '+e.message));
  await page.addInitScript(()=>{try{speechSynthesis.speak=()=>{}}catch(_){}});
  await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser',c.file)).href+'?review=destinations#oyun='+c.id);
  await page.locator(c.scene).waitFor();await page.screenshot({path:path.join(OUT,c.id+'-tur1.png'),fullPage:true});
  const initial=await stateOf(page);assert.equal(initial.round,0);
  if(c.id==='y52'){
   await drag(page,'[data-piece="a"]','[data-target="t1"]',true);assert.equal((await stateOf(page)).done,0);
   await drag(page,'[data-piece="a"]','[data-target="t2"]');assert.equal((await stateOf(page)).done,0);
   await page.locator('[data-piece="a"]').focus();await page.keyboard.press('Enter');await page.locator('[data-target="t1"]').focus();await page.keyboard.press('Enter');assert.equal((await stateOf(page)).done,1);
   await page.emulateMedia({reducedMotion:'reduce'});await page.evaluate(()=>{roundIndex=0;render()});await drag(page,'[data-piece="a"]','[data-target="t1"]');assert.equal((await stateOf(page)).done,1);
   assert(!(await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).includes(c.animation));await page.emulateMedia({reducedMotion:'no-preference'});
   let count=0;for(let r=0;r<2;r++){
    await page.evaluate(i=>{roundIndex=i;render()},r);
    const pieces=await page.evaluate(()=>round().pieces.map(p=>({id:p.id,target:p.target})));
    for(const p of pieces){await drag(page,'[data-piece="'+p.id+'"]','[data-target="'+p.target+'"]');count++;assert.equal((await stateOf(page)).done,pieces.indexOf(p)+1);assert.equal(await page.locator('.map-artifact').count(),pieces.indexOf(p)+1);if(p===pieces[0])assert((await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).includes(c.animation))}
    await page.screenshot({path:path.join(OUT,c.id+'-tamam-tur'+(r+1)+'.png'),fullPage:true});await page.waitForFunction(i=>roundIndex===i+1,r);
   }
   results.push({id:c.id,placements:count,cancel:true,wrong:true,keyboard:true,reducedMotion:true});
  }else{
   await drag(page,'[data-sinif-kart]','[data-kutu="1"]',true);assert.equal((await stateOf(page)).ix,0);
   const right=await page.evaluate(()=>round().kartlar[0].dogru),wrong=(right+1)%4;
   await drag(page,'[data-sinif-kart]','[data-kutu="'+wrong+'"]');assert.equal((await stateOf(page)).ix,0);
   await page.locator('[data-sinif-kart]').focus();await page.keyboard.press('Enter');await page.locator('[data-kutu="'+right+'"]').focus();await page.keyboard.press('Enter');assert.equal((await stateOf(page)).ix,1);await page.waitForTimeout(900);
   await page.emulateMedia({reducedMotion:'reduce'});await page.evaluate(()=>render());await drag(page,'[data-sinif-kart]','[data-kutu="'+right+'"]');assert.equal((await stateOf(page)).ix,1);
   assert(!(await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).includes(c.animation));await page.waitForTimeout(900);await page.emulateMedia({reducedMotion:'no-preference'});
   await page.evaluate(()=>render());let count=0;const cards=await page.evaluate(()=>round().kartlar.map(x=>x.dogru));
   for(let i=0;i<cards.length;i++){
    await drag(page,'[data-sinif-kart]','[data-kutu="'+cards[i]+'"]');count++;assert.equal((await stateOf(page)).ix,i+1);assert.equal(await page.locator('.recycled-object').count(),i+1);if(i===0)assert((await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).includes(c.animation));
    if(i<cards.length-1)await page.waitForFunction(n=>state.ix===n&&!!document.querySelector('[data-sinif-kart]:not(:disabled)'),i+1);
   }
   await page.screenshot({path:path.join(OUT,c.id+'-tum-kutular.png'),fullPage:true});await page.waitForFunction(()=>roundIndex===1);
   results.push({id:c.id,placements:count,cancel:true,wrong:true,keyboard:true,reducedMotion:true});
  }
  const layouts=[];for(const v of [{width:320,height:568},{width:390,height:844},{width:844,height:390}]){
   await page.setViewportSize(v);for(let i=0;i<3;i++){
    await page.evaluate(i=>{roundIndex=i;render()},i);
    const l=await page.evaluate(()=>({horizontal:document.documentElement.scrollWidth>innerWidth+2,prompt:document.querySelector('.prompt').scrollHeight>document.querySelector('.prompt').clientHeight+3}));
    assert(!l.horizontal&&!l.prompt,JSON.stringify({v,i,l}));layouts.push({v,round:i+1,...l});
    if(i===0){const visible=await page.evaluate(({source,target})=>[source,target].map(s=>{const b=document.querySelector(s).getBoundingClientRect();return b.x+b.width/2>=0&&b.x+b.width/2<=innerWidth&&b.y+b.height/2>=0&&b.y+b.height/2<=innerHeight}),{source:c.source,target:c.target});assert(visible.every(Boolean),'Kaynak ve hedef aynı anda görünmüyor: '+JSON.stringify({id:c.id,v,visible}))}
    if(v.width===390)await page.screenshot({path:path.join(OUT,c.id+'-tur'+(i+1)+'.png'),fullPage:true});
    if(i===0&&v.width!==390){await page.screenshot({path:path.join(OUT,c.id+'-'+v.width+'x'+v.height+'.png'),fullPage:true});
     if(c.id==='y52'){const p=v.width===320?'d':'a',t=v.width===320?'t4':'t1';await drag(page,'[data-piece="'+p+'"]','[data-target="'+t+'"]');assert.equal((await stateOf(page)).done,1)}
     else{const t=await page.evaluate(()=>round().kartlar[0].dogru);await drag(page,'[data-sinif-kart]','[data-kutu="'+t+'"]');assert.equal((await stateOf(page)).ix,1);await page.waitForTimeout(900)}
    }
   }
  }
  results[results.length-1].layouts=layouts;await page.close();console.log('✓ '+c.id+': '+results[results.length-1].placements+' sürükleme, 3 ekran boyutu');
 }assert.deepEqual(errors,[]);fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({testedAt:new Date().toISOString(),results,errors},null,2));
 fs.writeFileSync(path.join(OUT,'index.html'),'<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sahnedeki gerçek hedefler</title><style>body{font:16px system-ui;background:#e6eee5;color:#234549;margin:0}main{max-width:1200px;margin:auto;padding:22px}section{background:#fffdf4;margin:24px 0;padding:18px;border-radius:16px}.images{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}figure{margin:0}img{width:100%;border-radius:10px}figcaption{font-size:12px;padding:8px}a{color:#276986}@media(max-width:650px){.images{grid-template-columns:1fr}}</style><main><h1>Sahnedeki gerçek hedefler</h1><p>İki ayrı tasarım: eserler haritanın şehir işaretlerine; atık nesneleri sahnedeki renkli kutuların içine bırakılır. Üç tur korunmuştur. PNGler sabittir; hareketi görmek için oyunu açın.</p>'+cases.map(c=>'<section><h2>'+c.id.toUpperCase()+' · '+c.title+'</h2><div class="images"><figure><figcaption>İlk tur</figcaption><img src="'+c.id+'-tur1.png"></figure><figure><figcaption>Yerleştirme sonrası</figcaption><img src="'+c.id+'-'+(c.id==='y52'?'tamam-tur1':'tum-kutular')+'.png"></figure><figure><figcaption>İkinci tur</figcaption><img src="'+c.id+'-tur2.png"></figure></div><p><a href="../tasarim-denetimi-2026-09-21/screens/'+(c.id==='y52'?'turkce3':'fen3')+'-'+c.id+'.png">Önceki görünüm</a> · <a href="../../app/src/main/assets/phaser/'+c.file+'?review=destinations#oyun='+c.id+'">Oyunu aç</a> · <a href="'+c.id+'-320x568.png">Dar telefon görünümü</a></p></section>').join('')+'</main></html>');
 }finally{await browser.close()}
}
main().catch(e=>{console.error(e);process.exitCode=1});
