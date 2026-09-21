'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert');
const {pathToFileURL}=require('url');
const {chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/sahne-duzeltmeleri-2026-09-21');
const CASES=[
 {slug:'matematik4',id:'p24',title:'Eşitlik Terazisi',source:'[data-item="0"]',target:'.pan-right',animation:'beam-balance',check:()=>state.selected.length===1},
 {slug:'matematik4',id:'p15',title:'Çokluk Ölçeri',source:'[data-add="kasa"]',target:'.market-cart',animation:'crate-settle',check:()=>state.tray.length===1},
 {slug:'turkce4',id:'z04',title:'Kurallı Cümle Makinesi',source:'[data-kart="0"]',target:'.press-paper',animation:'press-turn',check:()=>state.dizi.length===1},
 {slug:'fen4',id:'f03',title:'Araştırma Adımları',source:'[data-kart="0"]',target:'.field-notebook',animation:'ink-write',check:()=>state.dizi.length===1},
 {slug:'hayatbilgisi2',id:'h12',title:'Afet Çantası',source:'[data-esya="0"]',target:'.bag-mouth',animation:'pack-object',check:()=>state.alinan.length===1}
];
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function drag(page,from,to){
 await page.locator(from).first().scrollIntoViewIfNeeded();const a=await page.locator(from).first().boundingBox();
 await page.mouse.move(a.x+a.width/2,a.y+a.height/2);await page.mouse.down();
 const b=await page.locator(to).boundingBox();
 await page.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:12});await page.mouse.up();
}
async function main(){
 fs.mkdirSync(OUT,{recursive:true});
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 const results=[],errors=[];
 try{
 for(const c of CASES){
  const page=await browser.newPage({viewport:{width:390,height:844}});page.on('pageerror',e=>errors.push(`${c.id}: ${e.message}`));
  await page.addInitScript(()=>{try{speechSynthesis.speak=()=>{}}catch(_){}});
  await page.goto(pathToFileURL(path.join(ROOT,`app/src/main/assets/phaser/${c.slug}-pdf.html`)).href+`?workshop=${c.id}#oyun=${c.id}`);
  await page.waitForTimeout(100);await page.screenshot({path:path.join(OUT,`${c.id}-yeni.png`)});
  for(let i=1;i<3;i++){
   await page.evaluate(i=>{roundIndex=i;state={};render()},i);await page.waitForTimeout(100);
   await page.screenshot({path:path.join(OUT,`${c.id}-tur${i+1}.png`)});
  }
  await page.evaluate(()=>{roundIndex=0;state={};render()});
  // İptal edilen sürükleme nesneyi bırakmamalı.
  const a=await page.locator(c.source).first().boundingBox(),b=await page.locator(c.target).boundingBox();
  await page.mouse.move(a.x+a.width/2,a.y+a.height/2);await page.mouse.down();await page.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:6});
  await page.locator(c.source).first().dispatchEvent('pointercancel',{pointerId:1});await page.mouse.up();
  assert(!await page.evaluate(c.check),`${c.id}: iptal edilen sürükleme kabul edildi`);
  assert.strictEqual(await page.locator('.scene-drag-ghost').count(),0);
  await drag(page,c.source,c.target);
  assert(await page.evaluate(c.check),`${c.id}: gerçek sürükleme yerleşmedi`);
  const animations=await page.evaluate(()=>document.getAnimations().map(a=>a.animationName));
  assert(animations.includes(c.animation),`${c.id}: eylem animasyonu bulunamadı (${animations})`);
  await page.waitForTimeout(850);await page.screenshot({path:path.join(OUT,`${c.id}-islem.png`)});
  if(c.id==='p24'){
   assert(await page.locator('.brass-scale').evaluate(el=>el.classList.contains('scale-loaded')));
   await drag(page,'[data-item="3"]',c.target);
   assert.strictEqual(await page.evaluate(()=>state.selected.length),1,'Yanlış ağırlık kabul edildi');
   assert(!await page.locator('.brass-scale').evaluate(el=>el.classList.contains('scale-loaded')),'Yanlış ağırlıkta terazi dengelendi');
   await page.screenshot({path:path.join(OUT,'p24-yanlis.png')});
  }
  if(c.id==='p15'){
   await page.locator('[data-rm="0"]').click();assert.strictEqual(await page.evaluate(()=>state.tray.length),0);
   assert.strictEqual(await page.locator('[data-add]').count(),4,'Geri konan kasa rafa dönmedi');
  }
  if(c.id==='h12'){
   assert.strictEqual(await page.locator('.bag-mouth .packed-item svg').count(),1);
   await drag(page,'[data-esya="1"]',c.target);assert.strictEqual(await page.evaluate(()=>state.alinan.length),1,'Gereksiz eşya çantaya girdi');
  }
  // Hareket azaltıldığında sonuç korunmalı, animasyon kapanmalı.
  await page.emulateMedia({reducedMotion:'reduce'});await page.evaluate(()=>{state={};render()});
  await drag(page,c.source,c.target);assert(await page.evaluate(c.check));
  assert(!(await page.evaluate(()=>document.getAnimations().map(a=>a.animationName))).includes(c.animation));
  const mobile=[];
  for(const viewport of [{width:320,height:568},{width:844,height:390}]){
   await page.setViewportSize(viewport);
   for(let i=0;i<3;i++){
    await page.evaluate(i=>{roundIndex=i;state={};render()},i);
    const layout=await page.evaluate(()=>{const p=document.querySelector('.prompt');return {promptClipped:p.scrollHeight>p.clientHeight+3,docOverflow:document.documentElement.scrollWidth>innerWidth+2}});
    assert(!layout.promptClipped,`${c.id}/${i+1}: yönerge kırpıldı`);assert(!layout.docOverflow,`${c.id}/${i+1}: yatay taşma`);mobile.push({viewport,round:i+1,...layout});
   }
  }
  results.push({id:c.id,animations,cancel:true,reducedMotion:true,mobile});await page.close();console.log(`✓ ${c.id}: sahne, animasyon, iptal, küçük/dikey-yatay ekran`);
 }
 // Önceki denetimde kırpılma bulunan 81 oyun / 124 turu yeniden ölç.
 const audit=JSON.parse(fs.readFileSync(path.join(ROOT,'artifacts/tasarim-denetimi-2026-09-21/audit.json'),'utf8'));
 const affected=audit.games.filter(g=>g.rounds.some(r=>r.clipping.length));
 const scenesOnly=process.argv.includes('--scenes-only');
 let rounds=scenesOnly?JSON.parse(fs.readFileSync(path.join(OUT,'verification.json'),'utf8')).header.rounds:0;
 for(const g of scenesOnly?[]:affected){
  const page=await browser.newPage({viewport:{width:390,height:844}});
  await page.addInitScript(()=>{try{speechSynthesis.speak=()=>{}}catch(_){}});
  await page.goto(pathToFileURL(path.join(ROOT,`app/src/main/assets/phaser/${g.slug}-pdf.html`)).href+`?header=${g.id}#oyun=${g.id}`);
  for(const r of g.rounds.filter(r=>r.clipping.length)){
   await page.evaluate(i=>{roundIndex=i;state={};render()},r.round-1);
   const good=await page.locator('.prompt').evaluate(el=>el.scrollHeight<=el.clientHeight+3&&getComputedStyle(el).overflow!=='hidden');
   assert(good,`${g.id}/${r.round}: yönerge hâlâ kırpılıyor`);rounds++;
  }await page.close();
 }
 assert.strictEqual(errors.length,0,errors.join('\n'));
 fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({results,errors,header:{games:affected.length,rounds}},null,2));
 const cards=CASES.map(c=>`<section><h2>${c.id.toUpperCase()} · ${esc(c.title)}</h2><div class="compare"><figure><figcaption>ÖNCE</figcaption><img loading="lazy" src="../tasarim-denetimi-2026-09-21/screens/${c.slug}-${c.id}.png"></figure><figure><figcaption>YENİ SAHNE</figcaption><img src="${c.id}-yeni.png"></figure><figure><figcaption>İŞLEMDEN SONRA</figcaption><img src="${c.id}-islem.png"></figure></div><p><a href="../../app/src/main/assets/phaser/${c.slug}-pdf.html?review=workshop#oyun=${c.id}">Oyunu aç ve animasyonu dene</a> · <a href="${c.id}-tur2.png">2. tur</a> · <a href="${c.id}-tur3.png">3. tur</a></p></section>`).join('');
 fs.writeFileSync(path.join(OUT,'index.html'),`<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Beş oyunda sahne düzeltmeleri</title><style>body{font:16px system-ui;background:#eef3f6;color:#19364b;margin:0}main{max-width:1200px;margin:auto;padding:20px}h1{font-size:27px}section{background:white;border-radius:18px;padding:18px;margin:24px 0}.compare{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}figure{margin:0}img{width:100%;border:1px solid #cfdae2;border-radius:12px}figcaption{font-size:12px;font-weight:800;letter-spacing:1px;padding:10px 0}a{color:#156386}@media(max-width:600px){.compare{grid-template-columns:1fr}h1{font-size:22px}}</style><main><h1>Beş oyunda gerçek sahne ve eylem animasyonu</h1><p>635 oyunun tamamı yenilenmiş değildir. Bu teslim P24, P15, Z04, F03 ve H12 sahnelerini ve 81 oyundaki yönerge kırpılmasını kapsar. Resimler sabittir; hareketi görmek için “Oyunu aç” bağlantısını kullanın.</p>${cards}<p>Doğrulama: ${affected.length} oyun / ${rounds} yönerge; 5 gerçek sürükleme ve eylem animasyonu; iptal ve azaltılmış hareket; küçük telefon ve yatay düzen. Üç tur çözüm testleri ayrı yürütüldü.</p></main></html>`);
 console.log(`✓ ${affected.length} oyun / ${rounds} yönerge kırpılması giderildi\n${OUT}`);
 }finally{await browser.close()}
}
main().catch(e=>{console.error(e);process.exitCode=1});
