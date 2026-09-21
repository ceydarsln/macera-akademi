'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url');
const {chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/sahne-duzeltmeleri-2-2026-09-21');
const cases=[
 {slug:'matematik4',id:'p03',title:'Basamak Değeri Köprüsü',source:'[data-piece="a"]',target:'[data-target="v1"]',bad:'[data-target="v2"]',animation:'bridge-fit',check:()=>state.done===1},
 {slug:'matematik4',id:'p08',title:'Okunuş Eşleştirme',source:'[data-piece="a"]',target:'[data-target="n1"]',bad:'[data-target="n2"]',animation:'page-settle',check:()=>state.done===1},
 {slug:'turkce3',id:'y10',title:'Zıt Anlam Aynası',source:'[data-piece="a"]',target:'[data-target="t1"]',bad:'[data-target="t2"]',animation:'mirror-reveal',check:()=>state.done===1},
 {slug:'fen3',id:'g05',title:'Keşif Çantası',source:'[data-oge="0"]',target:'.satchel-mouth',badSource:'[data-oge="4"]',animation:'source-pack',check:()=>state.alinan.length===1},
 {slug:'fen4',id:'f05',title:'Araştırma Çantası',source:'[data-h="0"]',target:'.satchel-mouth',badSource:'[data-h="4"]',animation:'source-pack',check:()=>state.icerik.length===1}
];
async function drag(page,source,target,cancel=false){
 await page.locator(source).scrollIntoViewIfNeeded();
 const a=await page.locator(source).boundingBox(),b=await page.locator(target).boundingBox();
 assert(b.y>=0&&b.y+b.height/2<844,`Hedef erişilemiyor: ${source} -> ${target} y=${b.y}`);
 await page.mouse.move(a.x+a.width/2,a.y+a.height/2);await page.mouse.down();await page.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:10});
 if(cancel)await page.locator(source).first().dispatchEvent('pointercancel',{pointerId:1});
 await page.mouse.up();
}
async function main(){
 fs.mkdirSync(OUT,{recursive:true});const results=[],errors=[];
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 try{for(const c of cases){
  const page=await browser.newPage({viewport:{width:390,height:844}});page.on('pageerror',e=>errors.push(c.id+': '+e.message));
  await page.addInitScript(()=>{try{speechSynthesis.speak=()=>{}}catch(_){}});
  await page.goto(pathToFileURL(path.join(ROOT,`app/src/main/assets/phaser/${c.slug}-pdf.html`)).href+`?discovery=${c.id}#oyun=${c.id}`);
  await page.screenshot({path:path.join(OUT,`${c.id}-yeni.png`)});
  await drag(page,c.source,c.target,true);assert(!await page.evaluate(c.check),'İptal edilen sürükleme kabul edildi');assert.strictEqual(await page.locator('.scene-drag-ghost').count(),0);
  await drag(page,c.badSource||c.source,c.bad||c.target);assert(!await page.evaluate(c.check),'Yanlış eşleşme kabul edildi');await page.waitForTimeout(400);
  await drag(page,c.source,c.target);assert(await page.evaluate(c.check),c.id+' sürükleme sonucu');
  const animations=await page.evaluate(()=>document.getAnimations().map(a=>a.animationName));assert(animations.includes(c.animation),c.id+': animasyon eksik '+animations);
  await page.waitForTimeout(800);await page.screenshot({path:path.join(OUT,`${c.id}-islem.png`)});
  await page.emulateMedia({reducedMotion:'reduce'});await page.evaluate(()=>render());await drag(page,c.source,c.target);assert(await page.evaluate(c.check));assert(!(await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).includes(c.animation));
  await page.emulateMedia({reducedMotion:'no-preference'});
  for(let i=1;i<3;i++){await page.evaluate(i=>{roundIndex=i;render()},i);await page.screenshot({path:path.join(OUT,`${c.id}-tur${i+1}.png`)});}
  const layouts=[];for(const v of [{width:320,height:568},{width:390,height:844},{width:844,height:390}]){
   await page.setViewportSize(v);for(let i=0;i<3;i++){
    await page.evaluate(i=>{roundIndex=i;render()},i);
    const l=await page.evaluate(()=>{const p=document.querySelector('.prompt');return {horizontal:document.documentElement.scrollWidth>innerWidth+2,prompt:p.scrollHeight>p.clientHeight+3}});
    assert(!l.horizontal&&!l.prompt,c.id+': taşma '+JSON.stringify({v,i,l}));layouts.push({v,round:i+1,...l});
   }
  }
  // Küçük dikey ekranda yalnız ilk nesne değil bütün sürükleme turları.
  await page.setViewportSize({width:390,height:844});let placements=0;
  const rounds=c.id==='p03'?[0,1,2]:['y10','g05'].includes(c.id)?[0,1]:[0];
  for(const i of rounds){
   await page.evaluate(i=>{roundIndex=i;render()},i);
   const steps=await page.evaluate(()=>{
    const r=round();if(r.kind==='drag')return r.pieces.map(p=>({from:`[data-piece="${p.id}"]`,to:`[data-target="${p.target}"]`}));
    if(r.kind==='topla')return r.gerekli.map(j=>({from:`[data-oge="${j}"]`,to:'.satchel-mouth'}));
    return r.istekler.flatMap(s=>s.gerekli.map(id=>({from:`[data-h="${r.havuz.findIndex(h=>h.id===id)}"]`,to:'.satchel-mouth'})));
   });
   for(let j=0;j<steps.length;j++){
    if(c.id==='f05')await page.waitForFunction(()=>!state.gecis);
    await drag(page,steps[j].from,steps[j].to);
    const n=await page.evaluate(()=>state.done??state.alinan?.length??state.icerik?.length);
    assert.strictEqual(n,j+1,c.id+' bütün nesneler sürüklenebilmeli');placements++;
   }
   if(c.id==='f05')assert.strictEqual(await page.locator('.satchel-mouth .source-book').count(),4,'Son kaynak görünmeli');
   await page.screenshot({path:path.join(OUT,`${c.id}-tamam-tur${i+1}.png`)});
   await page.waitForTimeout(1000); // Eski turun zamanlayıcısı yeni testi etkilemesin.
  }
  results.push({id:c.id,animations,cancel:true,wrong:true,reducedMotion:true,layouts,placements});await page.close();console.log('✓ '+c.id+' · '+placements+' sürükleme');
 }
 assert.strictEqual(errors.length,0,errors.join('\n'));
 fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({results,errors},null,2));
 fs.writeFileSync(path.join(OUT,'index.html'),`<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>İkinci sahne düzeltme paketi</title><style>body{font:16px system-ui;background:#eff2e9;color:#263e46;margin:0}main{max-width:1200px;margin:auto;padding:22px}section{background:white;border-radius:20px;padding:18px;margin:25px 0}.compare{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}figure{margin:0}img{width:100%;border-radius:12px;border:1px solid #ccd8d8}figcaption{padding:8px;font-size:12px;font-weight:bold}a{color:#176578}@media(max-width:650px){.compare{grid-template-columns:1fr}}</style><main><h1>İkinci paket · 5 oyunda sahne düzeltmesi</h1><p>Köprü, okuma defteri, zıtlık aynaları ve araştırma çantaları. Ekran görüntüleri sabittir; animasyonları oyun bağlantılarında deneyebilirsiniz. Diğer oyunların tamamlandığı anlamına gelmez.</p>${cases.map(c=>`<section><h2>${c.id.toUpperCase()} · ${c.title}</h2><div class="compare"><figure><figcaption>ÖNCE</figcaption><img loading="lazy" src="../tasarim-denetimi-2026-09-21/screens/${c.slug}-${c.id}.png"></figure><figure><figcaption>YENİ</figcaption><img src="${c.id}-yeni.png"></figure><figure><figcaption>İŞLEMDEN SONRA</figcaption><img src="${c.id}-islem.png"></figure></div><p><a href="../../app/src/main/assets/phaser/${c.slug}-pdf.html?review=discovery#oyun=${c.id}">Oyunu aç</a> · <a href="${c.id}-tur2.png">2. tur</a> · <a href="${c.id}-tur3.png">3. tur</a></p></section>`).join('')}</main></html>`);
 }finally{await browser.close()}
}
main().catch(e=>{console.error(e);process.exitCode=1});
