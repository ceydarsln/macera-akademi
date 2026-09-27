'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/fen-hayat-tamamlama');
const cases=[['f30','fen4'],['f32','fen4'],['f34','fen4'],['f40','fen4'],['f41','fen4'],['g45','fen3'],['h13','hayatbilgisi2'],['h29','hayatbilgisi2']];
const selected=process.argv.slice(2),resultFile=path.join(OUT,'results.json');
async function drag(p,from,to,cancel=false){const a=p.locator(from),b=p.locator(to);await a.scrollIntoViewIfNeeded();const x=await a.boundingBox(),y=await b.boundingBox();assert(x&&y);await p.mouse.move(x.x+x.width/2,x.y+x.height/2);await p.mouse.down();await p.mouse.move(y.x+y.width/2,y.y+y.height/2,{steps:12});if(cancel)await a.dispatchEvent('pointercancel',{pointerId:1});await p.mouse.up();await p.waitForTimeout(40)}
async function tap(p,s){await p.locator(s).click();await p.waitForTimeout(60);if(await p.evaluate(()=>!!state.gecis))await p.waitForFunction(()=>!state.gecis)}
async function data(p){return p.evaluate(()=>JSON.parse(JSON.stringify(round(),(k,v)=>typeof v==='function'?undefined:v)))}
async function geometry(p){return p.evaluate(()=>{const scene=document.querySelector('.scene'),prompt=document.querySelector('.prompt');return{horizontal:document.documentElement.scrollWidth>innerWidth+3||scene.scrollWidth>scene.clientWidth+3,prompt:prompt.scrollHeight>prompt.clientHeight+3}})}
(async()=>{fs.mkdirSync(OUT,{recursive:true});const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});const prior=selected.length&&fs.existsSync(resultFile)?JSON.parse(fs.readFileSync(resultFile)):null,records=prior?prior.records.filter(r=>!selected.includes(r.id)):[],errors=prior?prior.errors.filter(e=>!selected.some(id=>e.startsWith(id+'-')||e.startsWith(id+':'))):[];
try{const jobs=cases.filter(([id])=>!selected.length||selected.includes(id)).flatMap(([id,slug])=>[[320,568],[390,844],[844,390]].map(([width,height])=>({id,slug,width,height})));let next=0;await Promise.all(Array.from({length:3},async()=>{while(next<jobs.length){const {id,slug,width,height}=jobs[next++];const p=await browser.newPage({viewport:{width,height}});p.setDefaultTimeout(7000);p.on('pageerror',e=>errors.push(id+': '+e.message));let shots=[],moves=0,checks=[];
try{
 await p.addInitScript(()=>{const timer=window.setTimeout;window.setTimeout=(fn,ms,...a)=>timer(fn,ms===25?1500:ms===30?500:ms,...a);try{speechSynthesis.speak=()=>{};speechSynthesis.cancel=()=>{}}catch(_){}});
 const url=pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser',slug+'-pdf.html')).href+'?test=1#oyun='+id;await p.goto(url);
 const photograph=async(label)=>{if(id==='f30'&&label.endsWith('kurulum3'))await p.waitForTimeout(720);const file=`${id}-${width}x${height}-${label}.png`;await p.screenshot({path:path.join(OUT,file),fullPage:true});shots.push(file)};
 for(let ri=0;ri<3;ri++){
  assert.equal(await p.evaluate(()=>roundIndex),ri);await p.evaluate(()=>{lives=3});const r=await data(p);await photograph('tur'+(ri+1)+'-baslangic');assert.deepEqual(await geometry(p),{horizontal:false,prompt:false});
  if(r.kind==='kur'){
   const correct=r.havuz.findIndex(h=>r.istekler[0].gerekli.includes(h.id));await drag(p,`[data-h="${correct}"]`,'[data-kur-hedef]',true);assert.equal(await p.evaluate(()=>state.icerik.length),0);checks.push('drag-cancel');
   const bad=r.havuz.findIndex(h=>!r.istekler[0].gerekli.includes(h.id));if(bad>=0){await drag(p,`[data-h="${bad}"]`,'[data-kur-hedef]');assert.equal(await p.evaluate(()=>state.icerik.length),0);checks.push('wrong-material');await p.waitForTimeout(600)}
   for(let j=0;j<r.istekler.length;j++){for(const name of r.istekler[j].gerekli){const n=r.havuz.findIndex(h=>h.id===name);if(await p.evaluate(n=>state.icerik.includes(n),n))continue;await drag(p,`[data-h="${n}"]`,'[data-kur-hedef]');moves++;if(j<r.istekler.length-1&&await p.evaluate(()=>state.gecis))await p.waitForFunction(()=>!state.gecis)}await photograph('tur'+(ri+1)+'-kurulum'+(j+1))}
   assert.equal(await p.evaluate(()=>state.ix),r.istekler.length);assert.equal(await p.locator('#stage [data-kur-hedef]').count(),1);
   if(id==='f30'){assert(await p.locator('#stage .compass-needle.north').count());assert(await p.locator('#stage').textContent().then(s=>s.includes('pusula çalışıyor')));checks.push('north-alignment')}
   if(id==='f34'){assert((await p.locator('#stage').textContent()).includes('ampul yanıyor'));checks.push('final-bulb-lit')}
  }else if(r.kind==='sira'){
   await drag(p,`[data-kart="${r.dogru[0]}"]`,'[data-sira-hedef]',true);assert.equal(await p.evaluate(()=>state.dizi.length),0);checks.push('drag-cancel');
   await drag(p,`[data-kart="${r.dogru[1]}"]`,'[data-sira-hedef]');assert.equal(await p.evaluate(()=>state.dizi.length),0);checks.push('wrong-order');await p.waitForTimeout(600);
   for(let j=0;j<r.dogru.length;j++){await drag(p,`[data-kart="${r.dogru[j]}"]`,'[data-sira-hedef]');moves++;if(id==='f32'&&j===3)assert(!(await p.locator('#stage').textContent()).includes('ampul yanıyor'));if(j===r.dogru.length-2)await photograph('tur'+(ri+1)+'-anahtar-acik')}
   if(id==='f32')assert((await p.locator('#stage').textContent()).includes('ampul yanıyor'));
  }else if(r.kind==='esle'){
   const fen=slug==='fen4',src=fen?'data-parca':'data-et';const items=fen?r.parcalar:r.etiketler;const slot=j=>fen?r.parcalar[j].yuva:r.yuvalar.findIndex(y=>y.dogru===j);
   await drag(p,`[${src}="0"]`,`[data-yuva="${slot(0)}"]`,true);assert((await p.evaluate(()=>state.yerlesen)).every(x=>x==null));checks.push('drag-cancel');
   await drag(p,`[${src}="0"]`,`[data-yuva="${(slot(0)+1)%r.yuvalar.length}"]`);assert((await p.evaluate(()=>state.yerlesen)).every(x=>x==null));checks.push('wrong-target');await p.waitForTimeout(600);
   for(let j=0;j<items.length;j++){const i=slot(j);await drag(p,`[${src}="${j}"]`,`[data-yuva="${i}"]`);moves++;if(r.yuvalar[i].gerekce){await tap(p,`[data-ger="${r.yuvalar[i].gerekce.secenekler.findIndex(o=>o.dogru)}"]`);moves++}assert.equal(await p.evaluate(i=>state.yerlesen[i],i),j);if(j===0)await photograph('tur'+(ri+1)+'-yerlesti')}
  }else if(r.kind==='karar'){
   const questions=r.sorular||[r];for(let j=0;j<questions.length;j++){const q=questions[j],opts=q.secenekler;const good=o=>o.dogru||o.correct;
    if(j===0){const bad=opts.findIndex(o=>!good(o));if(bad>=0){const before=await p.evaluate(()=>({ix:state.ix,faz:state.faz}));await tap(p,`[data-sec="${bad}"]`);assert.deepEqual(await p.evaluate(()=>({ix:state.ix,faz:state.faz})),before);checks.push('wrong-answer');await p.waitForTimeout(600)}}
    if(id==='f34'&&j===2){assert.equal(await p.locator('.series-cell').count(),2);await photograph('tur'+(ri+1)+'-seri-iki-pil');checks.push('two-series-cells-visible')}
    await tap(p,`[data-sec="${opts.findIndex(good)}"]`);moves++;const reason=q.gerekce||(typeof q.neden==='object'?q.neden:null);if(reason){await tap(p,`[${q.gerekce?'data-sec':'data-neden'}="${reason.secenekler.findIndex(good)}"]`);moves++}}
  }else if(r.kind==='yaz'){
   const confirm=slug==='fen4'?'#onayBtn':'#yazOk';await p.locator('#yaziAlan').fill('a');if(await p.locator(confirm).isEnabled())await tap(p,confirm);assert.equal(await p.evaluate(()=>locked),false);checks.push('short-text-rejected-or-disabled');await p.waitForTimeout(600);await p.locator('#yaziAlan').fill(r.ornekCevap);await tap(p,confirm);moves++;
  }else if(r.kind==='musluk'){
   assert.equal(await p.locator('.lavabo #musluk').count(),1);await tap(p,'#muslukOk');assert.equal(await p.evaluate(()=>state.ix),0);checks.push('empty-water-rejected');await p.waitForTimeout(600);
   for(let j=0;j<r.isler.length;j++){const target=(r.isler[j].enAz+r.isler[j].enCok)/2;const box=await p.locator('#musluk').boundingBox();await p.mouse.move(box.x+box.width/2,box.y+box.height/2);await p.mouse.down();await p.waitForTimeout(target*30);await p.mouse.up();const amount=await p.evaluate(()=>state.yuzde);assert(amount>=r.isler[j].enAz&&amount<=r.isler[j].enCok);await photograph('tur'+(ri+1)+'-su'+(j+1));await tap(p,'#muslukOk');moves++;if(j<r.isler.length-1)await p.waitForFunction(()=>!state.gecis)}
  }else if(r.kind==='konus'){
   await tap(p,'#ornekDinle');await tap(p,'#konusBasla');const box=await p.locator('#konusTut').boundingBox();assert(box,'Konuşma süresi kontrolü yok');await p.mouse.move(box.x+box.width/2,box.y+box.height/2);await p.mouse.down();await p.waitForTimeout(1400);await p.mouse.up();await p.waitForTimeout(80);await tap(p,'#konusBitti');for(let j=0;j<r.olcutler.length;j++)await tap(p,`[data-ol="${j}"]`);await tap(p,'#konusOk');moves+=r.olcutler.length+4;checks.push('self-assessment-not-recording');
  }else throw Error('Desteklenmeyen tur: '+r.kind);
  await photograph('tur'+(ri+1)+'-sonuc');assert.deepEqual(await geometry(p),{horizontal:false,prompt:false});await p.waitForFunction(i=>roundIndex>i,ri,{timeout:8000});
 }
 assert.equal(await p.locator('.overlay').count(),1);await Promise.all([p.waitForEvent('domcontentloaded'),p.locator('.overlay button').click()]);await p.waitForFunction(()=>typeof roundIndex!=='undefined'&&roundIndex===0&&!locked);checks.push('three-natural-transitions','game-end','restart');records.push({id,slug,width,height,moves,checks,shots});console.log('PASS',id,width);
}catch(e){errors.push(`${id}-${width}: ${e.stack}`);console.error(errors.at(-1));await p.screenshot({path:path.join(OUT,`${id}-${width}-HATA.png`),fullPage:true})}finally{await p.close()}}}));
}finally{await browser.close();fs.writeFileSync(path.join(OUT,'results.json'),JSON.stringify({records,errors,note:'Native browser mouse/keyboard, no answer-state injection. Lives reset to three at each round for separate negative tests; real game-over behavior is not covered. Test-only 25/30 ms timers shown for 1500/500 ms. Speech playback disabled; self-assessment is not actual speech recognition. Not physical-device or user visual approval.'},null,2))}
assert.equal(errors.length,0,errors.join('\n'));console.log('SCIENCE',records.length,'game/screen runs',records.length*3,'rounds')})();
