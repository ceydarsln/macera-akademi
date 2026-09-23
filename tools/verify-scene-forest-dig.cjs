'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/sahne-duzeltmeleri-10-2026-09-23');
const cases=[{id:'y20',file:'turkce3-pdf.html',title:'Eş Anlam Ormanı',source:'[data-piece]',target:'[data-target]',animation:'forest-bloom'},
 {id:'g18',file:'fen3-pdf.html',title:'Kazı Seti',source:'[data-sinif-kart]',target:'[data-kutu]',animation:'dig-settle'}];
async function drag(page,source,target,cancel=false){
 const a=page.locator(source).first(),b=page.locator(target).first();await a.scrollIntoViewIfNeeded();
 const x=await a.boundingBox(),y=await b.boundingBox();assert(x&&y,'Kaynak veya hedef yok: '+source+' → '+target);
 assert(y.y+y.height/2>=0&&y.y+y.height/2<=page.viewportSize().height,'Hedef görünür değil');
 await page.mouse.move(x.x+x.width/2,x.y+x.height/2);await page.mouse.down();await page.mouse.move(y.x+y.width/2,y.y+y.height/2,{steps:10});
 if(cancel)await a.dispatchEvent('pointercancel',{pointerId:1});await page.mouse.up();
}
async function main(){
 fs.mkdirSync(OUT,{recursive:true});const errors=[],results=[];
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 try{for(const c of cases){
  const page=await browser.newPage({viewport:{width:390,height:844}});page.on('pageerror',e=>errors.push(c.id+': '+e.message));
  await page.addInitScript(()=>{try{speechSynthesis.speak=()=>{}}catch(_){}});
  await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser',c.file)).href+'?review=forest-dig#oyun='+c.id);
  if(c.id==='g18')await page.evaluate(()=>{roundIndex=1;render()});
  await page.locator(c.id==='y20'?'.forest-grove':'.dig-board').waitFor();await page.screenshot({path:path.join(OUT,c.id+'-ilk.png'),fullPage:true});
  let count=0;
  if(c.id==='y20'){
   await drag(page,'[data-piece="a"]','[data-target="t1"]',true);assert.equal(await page.evaluate(()=>state.done),0);
   await drag(page,'[data-piece="a"]','[data-target="t2"]');assert.equal(await page.evaluate(()=>state.done),0);
   await page.locator('[data-piece="a"]').focus();await page.keyboard.press('Enter');await page.locator('[data-target="t1"]').focus();await page.keyboard.press('Enter');assert.equal(await page.evaluate(()=>state.done),1);
   await page.emulateMedia({reducedMotion:'reduce'});await page.evaluate(()=>render());await drag(page,'[data-piece="a"]','[data-target="t1"]');assert.equal(await page.evaluate(()=>state.done),1);
   assert(!(await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).includes(c.animation));await page.emulateMedia({reducedMotion:'no-preference'});
   await page.evaluate(()=>render());const pieces=await page.evaluate(()=>round().pieces.map(p=>({id:p.id,target:p.target})));
   for(const p of pieces){await drag(page,'[data-piece="'+p.id+'"]','[data-target="'+p.target+'"]');count++;assert.equal(await page.evaluate(()=>state.done),count);assert.equal(await page.locator('.forest-pair').count(),count);if(count===1)assert((await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).includes(c.animation))}
   await page.screenshot({path:path.join(OUT,c.id+'-tamam.png'),fullPage:true});await page.waitForFunction(()=>roundIndex===1);
  }else{
   const first=await page.evaluate(()=>round().kartlar[0].dogru),bad=(first+1)%2;
   await drag(page,'[data-sinif-kart]','[data-kutu="'+first+'"]',true);assert.equal(await page.evaluate(()=>state.ix),0);
   await drag(page,'[data-sinif-kart]','[data-kutu="'+bad+'"]');assert.equal(await page.evaluate(()=>state.ix),0);
   await page.locator('[data-sinif-kart]').focus();await page.keyboard.press('Enter');await page.locator('[data-kutu="'+first+'"]').focus();await page.keyboard.press('Enter');assert.equal(await page.evaluate(()=>state.ix),1);await page.waitForTimeout(900);
   await page.emulateMedia({reducedMotion:'reduce'});await page.evaluate(()=>render());await drag(page,'[data-sinif-kart]','[data-kutu="'+first+'"]');assert.equal(await page.evaluate(()=>state.ix),1);
   assert(!(await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).includes(c.animation));await page.waitForTimeout(900);await page.emulateMedia({reducedMotion:'no-preference'});
   await page.evaluate(()=>render());const cards=await page.evaluate(()=>round().kartlar.map(k=>k.dogru));
   for(let i=0;i<cards.length;i++){await drag(page,'[data-sinif-kart]','[data-kutu="'+cards[i]+'"]');count++;assert.equal(await page.evaluate(()=>state.ix),count);assert.equal(await page.locator('.dig-tool').count(),count);if(i===0)assert((await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).includes(c.animation));if(i<cards.length-1)await page.waitForFunction(n=>state.ix===n&&!!document.querySelector('[data-sinif-kart]:not(:disabled)'),i+1)}
   await page.screenshot({path:path.join(OUT,c.id+'-tamam.png'),fullPage:true});await page.waitForFunction(()=>roundIndex===2);
  }
  const layouts=[];for(const v of [{width:320,height:568},{width:390,height:844},{width:844,height:390}]){
   await page.setViewportSize(v);for(let i=0;i<3;i++){
    await page.evaluate(i=>{roundIndex=i;render()},i);
    const l=await page.evaluate(()=>({horizontal:document.documentElement.scrollWidth>innerWidth+2,prompt:document.querySelector('.prompt').scrollHeight>document.querySelector('.prompt').clientHeight+3}));assert(!l.horizontal&&!l.prompt,JSON.stringify({c:c.id,v,i,l}));layouts.push({v,round:i+1,...l});
    if(v.width===390)await page.screenshot({path:path.join(OUT,c.id+'-tur'+(i+1)+'.png'),fullPage:true});
    if(i===(c.id==='g18'?1:0)&&v.width!==390){const visible=await page.evaluate(({source,target})=>[source,target].map(s=>{const b=document.querySelector(s).getBoundingClientRect();return b.x+b.width/2>=0&&b.x+b.width/2<=innerWidth&&b.y+b.height/2>=0&&b.y+b.height/2<=innerHeight}),{source:c.source,target:c.target});assert(visible.every(Boolean),'Kaynak ve hedef aynı anda görünmüyor: '+JSON.stringify({c:c.id,v,visible}));await page.screenshot({path:path.join(OUT,c.id+'-'+v.width+'x'+v.height+'.png'),fullPage:true});
     if(c.id==='y20'){const p=v.width===320?'d':'a',t=v.width===320?'t4':'t1';await drag(page,'[data-piece="'+p+'"]','[data-target="'+t+'"]');assert.equal(await page.evaluate(()=>state.done),1)}else{const t=await page.evaluate(()=>round().kartlar[0].dogru);await drag(page,'[data-sinif-kart]','[data-kutu="'+t+'"]');assert.equal(await page.evaluate(()=>state.ix),1);await page.waitForTimeout(900)}
    }
   }
  }
  results.push({id:c.id,placements:count,cancel:true,wrong:true,keyboard:true,reducedMotion:true,animation:true,layouts});await page.close();console.log('✓ '+c.id+': '+count+' gerçek sürükleme');
 }assert.deepEqual(errors,[]);fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({testedAt:new Date().toISOString(),results,errors},null,2));
 const sections=cases.map(c=>{const before=c.id==='y20'?'<a href="../tasarim-denetimi-2026-09-21/screens/turkce3-y20.png">Önceki ilk tur</a> · ':'';
  return '<section><h2>'+c.id.toUpperCase()+' · '+c.title+'</h2><div class="images"><figure><figcaption>Yenilenen tur · '+(c.id==='y20'?'1':'2')+'</figcaption><img src="'+c.id+'-ilk.png"></figure><figure><figcaption>Yerleştirme sonrası</figcaption><img src="'+c.id+'-tamam.png"></figure><figure><figcaption>Dar telefon</figcaption><img src="'+c.id+'-320x568.png"></figure></div><p>'+before+'<a href="../../app/src/main/assets/phaser/'+c.file+'?review=forest-dig#oyun='+c.id+'">Oyunu aç</a> · <a href="'+c.id+'-tur2.png">İkinci tur</a></p></section>'}).join('');
 fs.writeFileSync(path.join(OUT,'index.html'),'<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Orman ve kazı sahneleri</title><style>body{font:16px system-ui;background:#e7eee7;color:#28474a;margin:0}main{max-width:1200px;margin:auto;padding:22px}section{background:#fffdf4;margin:24px 0;padding:18px;border-radius:16px}.images{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}figure{margin:0}img{width:100%;border-radius:10px}figcaption{font-size:12px;padding:8px}a{color:#276986}@media(max-width:650px){.images{grid-template-columns:1fr}}</style><main><h1>Orman ve kazı sahneleri</h1><p>Y20 sözcükleri ağaç kovuklarına, G18 aletleri kazı katmanlarına bırakır. PNGler sabittir; hareketi oyunda inceleyin.</p>'+sections+'</main></html>');
 }finally{await browser.close()}
}
main().catch(e=>{console.error(e);process.exitCode=1});
