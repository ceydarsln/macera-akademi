'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/sahne-duzeltmeleri-8-2026-09-23');
const cases=[{id:'y19',title:'Doğa Dergisi Masası',animation:'column-print'},{id:'y58',title:'Dilekçe Masası',animation:'letter-write'}];
async function drag(page,source,target,cancel=false){
 const a=page.locator(source).first(),b=page.locator(target);await a.scrollIntoViewIfNeeded();
 const x=await a.boundingBox(),y=await b.boundingBox();
 assert(await page.evaluate(({source,target})=>[document.querySelector(source),document.querySelector(target)].every(e=>{const r=e.getBoundingClientRect();return e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))}),{source,target}),'Sürükleme kaynağı/hedefi erişilemiyor');
 await page.mouse.move(x.x+x.width/2,x.y+x.height/2);await page.mouse.down();await page.mouse.move(y.x+y.width/2,y.y+y.height/2,{steps:10});if(cancel)await a.dispatchEvent('pointercancel',{pointerId:1});await page.mouse.up();
}
async function main(){
 fs.mkdirSync(OUT,{recursive:true});const errors=[],results=[];
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 try{for(const c of cases){
  const page=await browser.newPage({viewport:{width:390,height:844}});page.on('pageerror',e=>errors.push(c.id+': '+e.message));
  await page.addInitScript(()=>{try{speechSynthesis.speak=()=>{}}catch(_){}});
  await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser/turkce3-pdf.html')).href+'?pages='+c.id+'#oyun='+c.id);
  await page.screenshot({path:path.join(OUT,c.id+'-yeni.png')});
  const first=await page.evaluate(()=>round().order[0]),source='[data-card="'+first+'"]',target='[data-slot="0"]';
  await drag(page,source,target,true);assert.equal(await page.evaluate(()=>state.done),0);assert.equal(await page.locator('.scene-drag-ghost').count(),0);
  await drag(page,source,'[data-slot="1"]');assert.equal(await page.evaluate(()=>state.done),0);await page.waitForTimeout(400);
  await page.locator(source).focus();await page.keyboard.press('Enter');await page.locator(target).focus();await page.keyboard.press('Enter');assert.equal(await page.evaluate(()=>state.done),1);
  await page.emulateMedia({reducedMotion:'reduce'});await page.evaluate(()=>render());await drag(page,source,target);assert.equal(await page.evaluate(()=>state.done),1);assert(!(await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).includes(c.animation));
  await page.emulateMedia({reducedMotion:'no-preference'});
  let placements=0;const animations=[];
  for(let round=0;round<2;round++){
   await page.evaluate(i=>{roundIndex=i;render()},round);
   const pieces=await page.evaluate(()=>round().kind==='kule'?round().order.map((id,i)=>({source:'[data-card="'+id+'"]',target:'[data-slot="'+i+'"]'})):round().pieces.map(p=>({source:'[data-piece="'+p.id+'"]',target:'[data-target="'+p.target+'"]'})));
   for(let n=0;n<pieces.length;n++){
    await drag(page,pieces[n].source,pieces[n].target);assert.equal(await page.evaluate(()=>state.done),n+1);
    assert.equal(await page.locator('.page-content').filter({has:page.locator('.paper-lines')}).count(),pieces.length-n-1);
    const names=await page.evaluate(()=>document.getAnimations().map(a=>a.animationName));assert(names.includes(c.animation));animations.push(c.animation);placements++;
   }
   await page.waitForTimeout(680);await page.screenshot({path:path.join(OUT,c.id+'-tamam-tur'+(round+1)+'.png')});
   await page.waitForFunction(i=>roundIndex===i+1,round);
  }
  const layouts=[];
  for(const v of [{width:320,height:568},{width:390,height:844},{width:844,height:390}]){
   await page.setViewportSize(v);
   for(let i=0;i<3;i++){
    await page.evaluate(i=>{roundIndex=i;render()},i);
    const l=await page.evaluate(()=>{const p=document.querySelector('.prompt'),s=document.querySelector('.scene');return {horizontal:document.documentElement.scrollWidth>innerWidth+2||s.scrollWidth>s.clientWidth+2,prompt:p.scrollHeight>p.clientHeight+3}});
    assert(!l.horizontal&&!l.prompt,JSON.stringify({v,i,l}));layouts.push({v,round:i+1,...l});
    if(v.width===390)await page.screenshot({path:path.join(OUT,c.id+'-tur'+(i+1)+'.png')});
    if(i===0&&v.width!==390){
     // Küçük ekran: seç, gerekiyorsa kaydır, gerçek sayfa hedefine dokun.
     await page.locator(source).click();await page.locator(target).click();assert.equal(await page.evaluate(()=>state.done),1);
     await page.screenshot({path:path.join(OUT,c.id+'-'+v.width+'x'+v.height+'.png')});
    }
   }
  }
  results.push({id:c.id,placements,cancel:true,wrong:true,keyboard:true,reducedMotion:true,animations,layouts});await page.close();console.log('✓ '+c.id+': '+placements+' gerçek yerleştirme');
 }
 assert.deepEqual(errors,[]);fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({testedAt:new Date().toISOString(),results,errors},null,2));
 fs.writeFileSync(path.join(OUT,'index.html'),'<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sayfanın kendisinde düzenleme</title><style>body{font:16px system-ui;background:#e4e9df;color:#2c474a;margin:0}main{max-width:1200px;margin:auto;padding:22px}section{background:#fffcf2;margin:24px 0;padding:18px;border-radius:16px}.images{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}figure{margin:0}img{width:100%;border-radius:10px}figcaption{font-size:12px;padding:8px}a{color:#276986}@media(max-width:650px){.images{grid-template-columns:1fr}}</style><main><h1>Sayfanın kendisinde düzenleme</h1><p>İlk iki turda parçalar doğrudan dergi sayfasına veya dilekçe kâğıdına yerleşir. Üçüncü yazma turu korunmuştur. PNGler sabittir; hareketi görmek için oyunu açın.</p>'+cases.map(c=>'<section><h2>'+c.id.toUpperCase()+' · '+c.title+'</h2><div class="images"><figure><figcaption>Yeni sayfa · tur 1</figcaption><img src="'+c.id+'-yeni.png"></figure><figure><figcaption>Bölümler yerleşti</figcaption><img src="'+c.id+'-tamam-tur1.png"></figure><figure><figcaption>İçerikler sayfada · tur 2</figcaption><img src="'+c.id+'-tamam-tur2.png"></figure></div><p><a href="../tasarim-denetimi-2026-09-21/screens/turkce3-'+c.id+'.png">Önceki ilk tur</a> · <a href="../../app/src/main/assets/phaser/turkce3-pdf.html?review=pages#oyun='+c.id+'">Oyunu aç</a> · <a href="'+c.id+'-tur3.png">Korunan yazma turu</a></p></section>').join('')+'</main></html>');
 }finally{await browser.close()}
}
main().catch(e=>{console.error(e);process.exitCode=1});
