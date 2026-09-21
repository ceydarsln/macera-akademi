'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/sahne-duzeltmeleri-4-2026-09-21');
const cases=[{id:'g07',slug:'fen3',title:'Canlı Sınıflama Masası',rounds:[0,1],animation:'specimen-settle'},{id:'z10',slug:'turkce4',title:'Sözcük Tasnifi',rounds:[0,1],animation:'book-shelve'},{id:'h07',slug:'hayatbilgisi2',title:'Alışkanlıklar Panosu',rounds:[0],animation:'habit-pin'}];
async function drag(page,target,cancel=false){
 const source=page.locator('[data-sinif-kart]').first();await source.scrollIntoViewIfNeeded();
 const a=await source.boundingBox(),b=await page.locator(`[data-kutu="${target}"]`).boundingBox();
 assert(b.y>=0&&b.y+b.height/2<844,`Hedef görünmüyor: ${target} y=${b.y}`);
 await page.mouse.move(a.x+a.width/2,a.y+a.height/2);await page.mouse.down();await page.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:10});if(cancel)await source.dispatchEvent('pointercancel',{pointerId:1});await page.mouse.up();
}
async function main(){
 fs.mkdirSync(OUT,{recursive:true});const results=[],errors=[];
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 try{for(const c of cases){
  const page=await browser.newPage({viewport:{width:390,height:844}});page.on('pageerror',e=>errors.push(c.id+': '+e.message));
  await page.addInitScript(()=>{try{speechSynthesis.speak=()=>{}}catch(_){}});
  await page.goto(pathToFileURL(path.join(ROOT,`app/src/main/assets/phaser/${c.slug}-pdf.html`)).href+`?collections=${c.id}#oyun=${c.id}`);
  if(c.id==='g07'){
   const shapes=await page.evaluate(()=>({bee:SceneCollections.specimen('Arı — uçar, bal yapar.'),plant:SceneCollections.specimen('Ayçiçeği — yapraklarında besin üretir.')}));
   assert(shapes.bee.includes('#d5ecf0'),'Arının kanat çizimi seçilmedi');
   assert(shapes.plant.includes('#e8bb53')&&!shapes.plant.includes('#d5ecf0'),'Bitki açıklaması arı çizimini seçti');
  }
  await page.screenshot({path:path.join(OUT,c.id+'-yeni.png')});const target=await page.evaluate(()=>round().kartlar[0].dogru);
  await drag(page,target,true);assert.strictEqual(await page.evaluate(()=>state.ix),0);assert.strictEqual(await page.locator('.scene-drag-ghost').count(),0);
  const bad=await page.evaluate(()=> (round().kartlar[0].dogru+1)%round().kutular.length);await drag(page,bad);assert.strictEqual(await page.evaluate(()=>state.ix),0);await page.waitForTimeout(400);
  await drag(page,target);assert.strictEqual(await page.evaluate(()=>state.ix),1);
  const animations=await page.evaluate(()=>document.getAnimations().map(a=>a.animationName));assert(animations.includes(c.animation),c.id+': '+animations);
  assert.strictEqual(await page.locator('.collection-content .collected').count(),1);
  await page.waitForTimeout(900);await page.screenshot({path:path.join(OUT,c.id+'-islem.png')});
  await page.emulateMedia({reducedMotion:'reduce'});await page.evaluate(()=>render());await drag(page,target);assert.strictEqual(await page.evaluate(()=>state.ix),1);assert(!(await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).includes(c.animation));await page.waitForTimeout(900);
  await page.emulateMedia({reducedMotion:'no-preference'});await page.evaluate(()=>render());await page.locator(`[data-kutu="${target}"]`).focus();await page.keyboard.press('Enter');assert.strictEqual(await page.evaluate(()=>state.ix),1);await page.waitForTimeout(900);
  const layouts=[];for(const v of [{width:320,height:568},{width:390,height:844},{width:844,height:390}]){
   await page.setViewportSize(v);for(let i=0;i<3;i++){
    await page.evaluate(i=>{roundIndex=i;render()},i);const l=await page.evaluate(()=>{const p=document.querySelector('.prompt'),s=document.querySelector('.scene');return {horizontal:document.documentElement.scrollWidth>innerWidth+2||s.scrollWidth>s.clientWidth+2,prompt:p.scrollHeight>p.clientHeight+3}});
    assert(!l.horizontal&&!l.prompt,c.id+JSON.stringify({v,i,l}));layouts.push({v,round:i+1,...l});if(v.width===390)await page.screenshot({path:path.join(OUT,`${c.id}-tur${i+1}.png`)});
   }
  }
  await page.setViewportSize({width:390,height:844});let placements=0;
  for(const i of c.rounds){
   await page.evaluate(i=>{roundIndex=i;render()},i);const cards=await page.evaluate(()=>round().kartlar);
   for(let j=0;j<cards.length;j++){
    await drag(page,cards[j].dogru);assert.strictEqual(await page.evaluate(()=>state.ix),j+1);assert.strictEqual(await page.locator('.collection-content .collected').count(),j+1);placements++;
    if(j===cards.length-1){await page.waitForTimeout(700);await page.screenshot({path:path.join(OUT,`${c.id}-tamam-tur${i+1}.png`)});await page.waitForTimeout(1100)}else await page.waitForTimeout(900);
   }
  }
  results.push({id:c.id,cancel:true,wrong:true,keyboard:true,reducedMotion:true,animations,layouts,placements});await page.close();console.log(`✓ ${c.id}: ${placements} sürükleme`);
 }
 assert.strictEqual(errors.length,0,errors.join('\n'));fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({results,errors},null,2));
 fs.writeFileSync(path.join(OUT,'index.html'),`<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dördüncü sahne düzeltme paketi</title><style>body{font:16px system-ui;background:#eef3e9;color:#26434f;margin:0}main{max-width:1200px;margin:auto;padding:22px}section{background:white;border-radius:20px;padding:18px;margin:25px 0}.compare{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}figure{margin:0}img{width:100%;border-radius:12px;border:1px solid #ccd8d8}figcaption{padding:8px;font-size:12px;font-weight:bold}a{color:#176578}@media(max-width:650px){.compare{grid-template-columns:1fr}}</style><main><h1>Doğa koleksiyonu, sözcük kütüphanesi ve alışkanlık panosu</h1><p>Yalnız sınıflama turları yeniden tasarlandı. Sözel/yazılı turların kuralları korundu. Bu paket 635 oyunun tasarım kabulü değildir. Hareketi görmek için oyunu açın.</p>${cases.map(c=>`<section><h2>${c.id.toUpperCase()} · ${c.title}</h2><div class="compare"><figure><figcaption>ÖNCE</figcaption><img loading="lazy" src="../tasarim-denetimi-2026-09-21/screens/${c.slug}-${c.id}.png"></figure><figure><figcaption>YENİ</figcaption><img src="${c.id}-yeni.png"></figure><figure><figcaption>İŞLEM SONRASI</figcaption><img src="${c.id}-islem.png"></figure></div><p><a href="../../app/src/main/assets/phaser/${c.slug}-pdf.html?review=collections#oyun=${c.id}">Oyunu aç</a> · <a href="${c.id}-tur2.png">2. tur</a> · <a href="${c.id}-tur3.png">3. tur</a></p></section>`).join('')}</main></html>`);
 }finally{await browser.close()}
}
main().catch(e=>{console.error(e);process.exitCode=1});
