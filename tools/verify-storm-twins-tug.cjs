'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/tahmin-ikizler-halat-denetimi');
(async()=>{fs.mkdirSync(OUT,{recursive:true});const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});const records=[],errors=[];
try{for(const id of ['m41','m45','m47'])for(const [width,height] of [[320,568],[390,844],[844,390]]){
 const page=await browser.newPage({viewport:{width,height}});page.on('pageerror',e=>errors.push(e.message));await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser/matematik-pdf.html')).href+'?test=1#oyun='+id);
 for(let ri=0;ri<3;ri++){
  await page.waitForFunction(i=>roundIndex===i&&!locked,ri);
  const geometry=await page.evaluate(()=>{const v=document.querySelector('#visual').getBoundingClientRect(),p=document.querySelector('.prompt');return {overflow:document.documentElement.scrollWidth>innerWidth+1,promptClipped:p.scrollHeight>p.clientHeight+2,clipped:[...document.querySelectorAll('#visual [data-choice]')].some(e=>{const b=e.getBoundingClientRect();return b.left<v.left||b.right>v.right||b.top<v.top||b.bottom>v.bottom||b.bottom>innerHeight}),smallButton:[...document.querySelectorAll('#visual [data-choice]')].some(e=>{const b=e.getBoundingClientRect();return b.width<44||b.height<44})}});
  assert(!Object.values(geometry).some(Boolean),JSON.stringify({id,width,height,ri,geometry}));const stem=`${id}-${width}x${height}-tur${ri+1}`;await page.screenshot({path:path.join(OUT,stem+'.png')});
  let correct=await page.evaluate(()=>{const r=round();return (r.stages?r.stages[state.stage||0]:r).choices.findIndex(c=>c.correct)});
  const before=await page.evaluate(()=>lives);await page.locator(`[data-choice="${(correct+1)%await page.locator('[data-choice]').count()}"]`).click();assert(await page.evaluate(n=>!locked&&lives===n-1,before));await page.waitForTimeout(400);
  // A wrong answer must not change the scene's outcome.
  assert.equal(await page.locator('.struck,.matched,.pulled,.balanced').count(),0);
  if(id==='m41'){
   await page.locator(`[data-choice="${correct}"]`).click();assert.equal(await page.locator('.struck').count(),1);await page.waitForFunction(()=>state.stage===1&&!locked);correct=await page.evaluate(()=>round().stages[1].choices.findIndex(c=>c.correct));
  }
  if(id==='m47')assert.deepEqual(await page.locator('.tug-team').evaluateAll(es=>es.map(e=>e.children.length)),[[7,7],[8,9],[7,6]][ri]);
  await page.locator(`[data-choice="${correct}"]`).click();await page.waitForTimeout(380);
  if(id==='m41')assert.equal(await page.locator('.storm-reveal i').count(),[18,9,11][ri]);
  if(id==='m45'){assert.equal(await page.locator('.twin-partner .twin-robot').count(),1);assert.equal(await page.locator('.twin-proof i').count(),[18,18,10][ri]);assert.equal(await page.locator('.twin-link').textContent(),'=')}
  if(id==='m47'){const pull=await page.locator('.tug-assembly').evaluate(e=>e.style.getPropertyValue('--pull'));assert.equal(pull,['0%','17%','-17%'][ri]);assert.equal(await page.locator(ri?'.pulled':'.balanced').count(),1);assert(await page.evaluate(()=>{const v=document.querySelector('#visual').getBoundingClientRect();return [...document.querySelectorAll('.tug-person')].every(e=>{const b=e.getBoundingClientRect();return b.left>=v.left&&b.right<=v.right})}),'Takım sahne dışında kaldı')}
  await page.screenshot({path:path.join(OUT,stem+'-sonuc.png')});records.push({id,viewport:`${width}x${height}`,round:ri+1,wrongRejected:true,...geometry});
  // Replenish one spent life so all rounds can exercise rejection without ending the game.
  await page.evaluate(()=>lives=3);
 }
 await page.waitForFunction(()=>!!document.querySelector('.overlay'));await page.locator('.overlay button').click();assert(await page.evaluate(()=>roundIndex===0&&lives===3&&!locked));await page.close();
}
assert.deepEqual(errors,[]);fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({records,errors},null,2));
fs.writeFileSync(path.join(OUT,'index.html'),`<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tahmin, ikizler ve halat</title><style>body{font:16px system-ui;margin:20px;background:#eef4f4;color:#21465a}main{max-width:1200px;margin:auto}section{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}article{background:white;padding:12px;border-radius:14px}img{width:100%}</style><main><h1>M41 · M45 · M47</h1><p>27 tur/ekran senaryosu: yanlış ve doğru yanıt, sahne sonucu, doğal tur geçişi ve yeniden başlatma. Ekran görüntüsü animasyonun kendisi değildir; oyunu açarak hareketi deneyebilirsin.</p><section>${records.map(r=>{const s=`${r.id}-${r.viewport}-tur${r.round}`;return `<article><h2>${r.id.toUpperCase()} · ${r.viewport} · tur ${r.round}</h2><a href="${s}.png"><img loading="lazy" src="${s}.png"></a><a href="${s}-sonuc.png">Sonucu gör</a><p><a href="../../app/src/main/assets/phaser/matematik-pdf.html#oyun=${r.id}">Oyunu oyna</a></p></article>`}).join('')}</section></main>`);console.log(JSON.stringify({passed:records.length,errors}));
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
