'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/turkce-sahne-ucuncu-asama');
const IDS=['t02','t04','t06','t07','t09','t14','t21','t22','t30','t38','t46','t47','t48','t51','t54','t62','t64'];
async function drag(p,s,t,cancel=false){await s.scrollIntoViewIfNeeded();const a=await s.boundingBox(),b=await t.boundingBox();assert(a&&b);await p.mouse.move(a.x+a.width/2,a.y+a.height/2);await p.mouse.down();await p.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:6});if(cancel)await s.dispatchEvent('pointercancel',{pointerId:1});await p.mouse.up()}
async function geometry(p){return p.evaluate(()=>{const box=document.querySelector('#stage').getBoundingClientRect(),pr=document.querySelector('.prompt');const slots=[...document.querySelectorAll('[data-scene-slot],.sound-real-basket,.typewriter-keys button,.scene-key')];return {overflow:document.documentElement.scrollWidth>innerWidth+1,promptClipped:pr.scrollHeight>pr.clientHeight+2,slots:slots.length,clipped:slots.filter(e=>{const b=e.getBoundingClientRect();return b.left<box.left-1||b.right>box.right+1||b.top<box.top||b.bottom>box.bottom}).map(e=>e.outerHTML.slice(0,120)),small:slots.filter(e=>{const b=e.getBoundingClientRect();return b.width<43||b.height<43}).map(e=>e.outerHTML.slice(0,100))}})}
async function ready(p,ri,ai){await p.waitForFunction(([r,a])=>roundIndex===r&&!locked&&!state.gecis&&(state.asama||0)===a,[ri,ai])}
async function screen(p,name){await p.screenshot({path:path.join(OUT,name+'.png')});return name+'.png'}
(async()=>{fs.mkdirSync(OUT,{recursive:true});const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});const selected=process.argv.slice(2),priorFile=path.join(OUT,'results.json');const records=selected.length&&fs.existsSync(priorFile)?JSON.parse(fs.readFileSync(priorFile)).records.filter(r=>!selected.includes(r.id)):[],errors=[];
try{for(const id of process.argv.slice(2).length?process.argv.slice(2):IDS)for(const [width,height] of [[320,568],[390,844],[844,390]]){
 const p=await browser.newPage({viewport:{width,height}});p.on('pageerror',e=>errors.push(id+': '+e.message));
 try{await p.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser/turkce1-pdf.html')).href+'?test=1#oyun='+id);
 // Only lengthen the existing transition timer to photograph its real result.
 // No answer/state/renderer is replaced. Production timers are unchanged.
 await p.evaluate(()=>{const original=gecisBasla;gecisBasla=(fn,ms)=>original(fn,400)});
 for(let ri=0;ri<3;ri++){
  await ready(p,ri,0);const stem=`${id}-${width}x${height}-tur${ri+1}`,r=await p.evaluate(()=>round()),initial=await geometry(p);assert(!initial.overflow&&!initial.promptClipped&&!initial.clipped.length&&!initial.small.length,JSON.stringify({stem,initial}));const shots=[await screen(p,stem)];let moves=0;
  const stages=r.asamalar||[r];
  if(['tren','uzay','fabrika'].includes(r.kind))for(let ai=0;ai<stages.length;ai++){
   await ready(p,ri,ai);const a=stages[ai],attr=r.kind==='tren'?'data-ses':r.kind==='uzay'?'data-m':'data-h',field=r.kind==='fabrika'?'yuva':'yer',undo=r.kind==='tren'?'vagonGeri':r.kind==='uzay'?'uzayGeri':'fabGeri';
   const s=()=>p.locator(`[${attr}="${a.dogru[0]}"]`),t=()=>p.locator('[data-scene-slot="0"]');
   await drag(p,s(),t(),true);assert.equal(await p.locator('.scene-unit-slot.filled').count(),0,'İptal doldurdu');
   await drag(p,s(),p.locator('.assembly-world header'));assert.equal(await p.locator('.scene-unit-slot.filled').count(),0,'Başlık doldurdu');
   await drag(p,s(),p.locator('[data-scene-slot="1"]'));assert.equal(await p.locator('.scene-unit-slot.filled').count(),0,'Yanlış yuva doldurdu');
   const wrong=Array.from({length:(a.sesler||a.meteorlar||a.heceler).length},(_,i)=>i).find(i=>i!==a.dogru[0]);
   if(wrong!==undefined){await drag(p,p.locator(`[${attr}="${wrong}"]`),t());assert.equal(await p.locator('.scene-unit-slot.filled').count(),0,'Yanlış ses kabul edildi');await p.evaluate(()=>{lives=3;hud()});await p.waitForTimeout(580)}
   await drag(p,s(),t());moves++;assert.equal(await p.locator('.scene-unit-slot.filled').count(),1);
   await p.locator('#'+undo).click();assert.equal(await p.locator('.scene-unit-slot.filled').count(),0,'Geri alma çalışmadı');
   for(let k=0;k<a.dogru.length;k++){await drag(p,p.locator(`[${attr}="${a.dogru[k]}"]`),p.locator(`[data-scene-slot="${k}"]`));moves++;assert.equal(await p.locator('.scene-unit-slot.filled').count(),k+1)}
   const out=r.kind==='fabrika'?a.kelime:a.dogru.map(i=>(a.sesler||a.meteorlar)[i]).join('');assert.equal(await p.locator('.assembly-output').textContent(),out);assert.equal(await p.locator('.assembly-world.assembled').count(),1);shots.push(await screen(p,stem+`-birlesim${ai+1}`));
   const g=await geometry(p);assert(!g.clipped.length&&!g.small.length&&!g.overflow,JSON.stringify({stem,g}));
   const choice=a.tip?['data-tip',a.tip]:a.kelimeSec?['data-k',a.kelimeSec.secenekler.findIndex(c=>c.correct)]:a.anlamSec?['data-a',a.anlamSec.secenekler.findIndex(c=>c.correct)]:null;
   if(choice){await p.waitForFunction(()=>state.faz===1&&!state.gecis);await p.locator(`[${choice[0]}="${choice[1]}"]`).click()}
  }else if(r.kind==='dikte')for(let ai=0;ai<stages.length;ai++){
   await ready(p,ri,ai);const a=stages[ai];assert.equal(await p.locator('.typewriter-keys').count(),1);
   const wrong=await p.evaluate(()=>state.palet.find(h=>h!==asama(round()).kelime[0]));await p.locator('[data-hp]').filter({hasText:wrong===' '?'␣':wrong}).first().click();assert.equal(await p.evaluate(()=>state.yaz.length),0);await p.waitForTimeout(580);
   await p.locator(`[data-hp="${a.kelime[0]}"]`).click();await p.locator('#dikteSil').click();assert.equal(await p.evaluate(()=>state.yaz.length),0);
   for(const ch of a.kelime){await p.locator(`[data-hp="${ch}"]`).click();moves++}
   assert.equal(await p.evaluate(()=>state.yaz.join('')),a.kelime);shots.push(await screen(p,stem+`-yazi${ai+1}`));
   if(a.resimSec){await p.waitForFunction(()=>state.faz===1&&!state.gecis);await p.locator(`[data-r="${a.resimSec.secenekler.findIndex(c=>c.correct)}"]`).click()}
  }else if(r.kind==='sepet'){
   assert.equal(await p.locator('[data-sepet]').count(),r.sepetler.length,'Yinelenen sepet');
   await drag(p,p.locator('[data-n="0"]'),p.locator(`[data-sepet="${r.nesneler[0].sepet}"]`),true);assert.equal(await p.evaluate(()=>state.yerlesen.length),0);
   await drag(p,p.locator('[data-n="0"]'),p.locator(`[data-sepet="${1-r.nesneler[0].sepet}"]`));assert.equal(await p.evaluate(()=>state.yerlesen.length),0);await p.waitForTimeout(580);
   for(let i=0;i<r.nesneler.length;i++){await drag(p,p.locator(`[data-n="${i}"]`),p.locator(`[data-sepet="${r.nesneler[i].sepet}"]`));moves++;if(i===r.nesneler.length-2)shots.push(await screen(p,stem+'-sepet'));}
  }else if(r.kind==='konum'){
   for(let i=0;i<r.nesneler.length;i++){await p.waitForFunction(i=>(state.ix||0)===i&&!state.gecis,i);await p.locator(`[data-k="${r.nesneler[i].konum}"]`).click();moves++}
  }else if(r.kind==='sandik'){
   assert.equal(await p.locator('.reading-picture').count(),1);assert.equal(await p.locator('#stage .metin-kart').count(),0,'Resim yerine metin');
   const wrong=r.anahtarlar.findIndex(c=>!c.correct);await p.locator(`[data-a="${wrong}"]`).click();assert(!(await p.evaluate(()=>state.acildi)));await p.waitForTimeout(580);
   await p.locator(`[data-a="${r.anahtarlar.findIndex(c=>c.correct)}"]`).click();moves++;shots.push(await screen(p,stem+'-bulundu'));
   if(r.soru){await p.waitForFunction(()=>state.faz===1&&!state.gecis);await p.locator(`[data-s="${r.soru.secenekler.findIndex(c=>c.correct)}"]`).click()}
  }else throw Error('Unknown '+r.kind);
  await p.waitForFunction(i=>roundIndex>i,ri);await p.evaluate(()=>{lives=3;if(roundIndex<3)hud()});records.push({id,width,height,round:ri+1,kind:r.kind,stages:stages.length,moves,initial,shots,status:'passed'});
 }
 await p.waitForSelector('.overlay');await p.locator('.overlay button').first().click();await ready(p,0,0);console.log(id,width+'x'+height,'3 tur + yeniden başlatma geçti');
 }catch(e){errors.push(`${id} ${width}x${height}: ${e.stack}`);await screen(p,id+'-'+width+'-HATA');console.error(errors.at(-1))}finally{await p.close()}
 }
}finally{await browser.close();fs.writeFileSync(path.join(OUT,'results.json'),JSON.stringify({records,errors,timerNote:'Test extends transition display to 400ms; production answers and rules unchanged.'},null,2));const cards=records.map(r=>`<article><h2>${r.id.toUpperCase()} · Tur ${r.round} · ${r.width}×${r.height}</h2><p>${r.stages} alt aşama · ${r.moves} gerçek işlem</p><div>${r.shots.map(s=>`<a href="${s}"><img loading="lazy" src="${s}"></a>`).join('')}</div></article>`).join('');fs.writeFileSync(path.join(OUT,'index.html'),`<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Türkçe sahne bağlantıları</title><style>body{font:15px system-ui;background:#ecf2f6;color:#19374b;margin:20px}article{padding:16px;background:#fff;margin:18px 0;border-radius:15px}article div{display:flex;gap:10px;overflow:auto}img{width:230px;max-height:500px;object-fit:contain;vertical-align:top}a{color:#136788}</style><h1>3. aşama · Türkçe sahne bağlantıları</h1><p>17 oyun için tren, kapsül, üretim bandı, daktilo, sepet ve resim okuma. ${records.length} tur/ekran senaryosu geçti; ${errors.length} hata. Bu otomatik tarayıcı kanıtıdır; fiziksel cihaz, ses ve kullanıcı görsel onayı bekler.</p><a href="results.json">Test kayıtları</a>${errors.length?'<pre>'+errors.join('\n').replace(/</g,'&lt;')+'</pre>':''}${cards}</html>`)}assert.equal(errors.length,0,errors.join('\n'));
})();
