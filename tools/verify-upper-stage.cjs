'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/ust-sinif-dorduncu-asama');
const IDS=['v02','v06','v07','v10','v18','v26','v27','v28','w03','w06','w07','w14','w19','w24','p31','p32','p33','p48','p53','u41','u63','u64','u80','u83','y06','z12','z13'];
const defs=JSON.parse(fs.readFileSync(path.join(ROOT,'artifacts/tam-tasarim-incelemesi/definitions.json')));
async function shot(p,stem,suffix){const file=stem+'-'+suffix+'.png';await p.screenshot({path:path.join(OUT,file)});return file}
async function geometry(p){return p.evaluate(()=>{const s=document.querySelector('#stage'),b=s.getBoundingClientRect(),prompt=document.querySelector('.prompt'),scene=document.querySelector('.scene');return {horizontal:document.documentElement.scrollWidth>innerWidth+2||scene.scrollWidth>scene.clientWidth+2,promptClipped:prompt.scrollHeight>prompt.clientHeight+2,targetsOutside:[...document.querySelectorAll('[data-target],[data-yuva],[data-sira-yuva]')].filter(e=>!s.contains(e)).length,clipped:[...s.querySelectorAll('button,[data-target],[data-yuva],[data-sira-yuva]')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&r.height&&(r.left<b.left-3||r.right>b.right+3||r.top<b.top-3||r.bottom>b.bottom+3)}).length}})}
(async()=>{fs.mkdirSync(OUT,{recursive:true});const selected=process.argv.slice(2),priorFile=path.join(OUT,'scenes.json'),prior=selected.length&&fs.existsSync(priorFile)?JSON.parse(fs.readFileSync(priorFile)):null;const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});const records=prior?prior.records.filter(r=>!selected.includes(r.id)):[],errors=prior?prior.errors.filter(e=>!selected.some(id=>e.startsWith(id))):[];
try{for(const id of process.argv.length>2?process.argv.slice(2):IDS){const g=defs.find(g=>g.id===id);for(const [width,height]of [[320,568],[390,844],[844,390]])for(let ri=0;ri<3;ri++){
 const p=await browser.newPage({viewport:{width,height}});p.on('pageerror',e=>errors.push(id+': '+e.message));const stem=id+'-'+width+'x'+height+'-tur'+(ri+1);
 try{
 await p.addInitScript(()=>{const timeout=window.setTimeout;window.setTimeout=(f,ms,...args)=>timeout(f,ms===25?1200:ms,...args);try{speechSynthesis.speak=()=>{};speechSynthesis.cancel=()=>{}}catch(_){}});
 await p.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser',g.slug+'-pdf.html')).href+'?test=1#oyun='+id);if(ri)await p.evaluate(i=>{roundIndex=i;render()},ri);await p.waitForTimeout(30);
 const r=await p.evaluate(()=>JSON.parse(JSON.stringify(round(),(k,v)=>typeof v==='function'?undefined:v))),shots=[await shot(p,stem,'baslangic')],initial=await geometry(p);assert(!initial.horizontal&&!initial.promptClipped&&!initial.clipped,JSON.stringify(initial));let moves=0,completed=false;
 if(r.kind==='timing'){
  await p.locator('#tahminOk').click();assert.equal(await p.locator('.senior-stopwatch').count(),1);await p.locator('#kronBasla').click();await p.waitForTimeout(500);assert.notEqual(await p.locator('#kron').textContent(),'0,0 sn');shots.push(await shot(p,stem,'kronometre'));await p.locator('#kronDur').click();assert(await p.evaluate(()=>state.olcum>0));await p.locator('#timingOk').click();moves=4;completed=true;
 }else if(r.kind==='kargo'){
  for(let j=0;j<r.islemler.length;j++){const it=r.islemler[j],shift=Math.round(Math.log10(it.hedef/it.baslangic));await p.locator(`#stage [data-kay="${shift}"]`).click();assert.equal(await p.evaluate(()=>state.deger),it.hedef);moves++;shots.push(await shot(p,stem,'kargo'+(j+1)));await p.locator('#kargoOk').click();moves++;if(j<r.islemler.length-1)await p.waitForTimeout(80)}completed=true;
 }else if(r.kind==='firin'){
  for(const [kind,n]of [['tepsi',r.enIyi.tepsi],['tek',r.enIyi.tek]])for(let j=0;j<n;j++){await p.locator(`#stage [data-firin="${kind}"]`).click();moves++}assert.equal(await p.evaluate(()=>state.tepsiSay*round().tepsi+state.tekSay),r.hedef);completed=true;
 }else if(r.kind==='sayidogru'){
  await p.locator('[data-range]').focus();await p.keyboard.press('Home');for(let j=0;j<Math.round((r.target-r.min)/(r.step||1));j++){await p.locator('[data-range]').focus();await p.keyboard.press('ArrowRight');moves++}assert.equal(await p.evaluate(()=>state.value),r.target);await p.locator('[data-ok]').click();moves++;if(r.after){await p.waitForTimeout(60);await p.locator(`[data-cz="${r.after.choices.findIndex(c=>c.correct)}"]`).click();moves++}completed=true;
 }else if(r.kind==='kule'){
  if(id==='p48'){const preview=await p.locator('.senior-symmetry-preview svg').boundingBox();assert(preview&&preview.width>200&&preview.height>100,'Simetri çizimi görünür boyutta olmalı')}
  for(let j=0;j<r.order.length;j++){await p.locator(`[data-card="${r.order[j]}"]`).click();await p.locator(`#stage [data-slot="${j}"]`).click();moves++;assert.equal(await p.evaluate(()=>state.slots.filter(Boolean).length),moves);if(moves===r.order.length-1)shots.push(await shot(p,stem,'ayna-noktalari'))}completed=true;
 }else if(r.kind==='tara'){
  for(const it of r.items){const point=await p.locator(`[data-tara="${it.id}"]`).evaluate(e=>{const svg=e.ownerSVGElement,p=svg.createSVGPoint();if(e.tagName.toLowerCase()==='line'){p.x=(+e.getAttribute('x1')+ +e.getAttribute('x2'))/2;p.y=(+e.getAttribute('y1')+ +e.getAttribute('y2'))/2}else{p.x=+e.getAttribute('cx');p.y=+e.getAttribute('cy')}const q=p.matrixTransform(e.getScreenCTM());return{x:q.x,y:q.y}});await p.mouse.click(point.x,point.y);moves++;assert.equal(await p.evaluate(()=>state.tapped.length),moves)}if(r.after){await p.waitForTimeout(60);await p.locator(`[data-cz="${r.after.choices.findIndex(c=>c.correct)}"]`).click();moves++}completed=true;
 }else if(r.kind==='drag'&&id[0]==='v'){
  const targets=p.locator('#stage [data-target]');assert.equal(await targets.count(),r.targets.length);
  for(const piece of r.pieces.filter(x=>x.target)){await p.locator(`[data-piece="${piece.id}"]`).click();await p.locator(`#stage [data-target="${piece.target}"]`).click();moves++;assert.equal(await p.evaluate(()=>state.done),moves);if(moves===1)shots.push(await shot(p,stem,'yerlesti'))}completed=true;
 }else if(['choice','estimate'].includes(r.kind)&&r.choices){const i=r.choices.findIndex(c=>c.correct);await p.locator(`[data-choice="${i}"],[data-scene-choice="${i}"],[data-est="${i}"],[data-scene-estimate="${i}"]`).first().click();moves++;completed=true;
 }else if(r.kind==='graph'){
  const wrong=r.columns.find(c=>c.id!==r.sources[0].id);await p.locator(`#stage [data-graph="${wrong.id}"]`).click();assert.equal(await p.evaluate(()=>state.i),0);await p.waitForTimeout(500);
  for(const src of r.sources){await p.locator(`#stage [data-graph="${src.id}"]`).click();moves++;assert.equal(await p.evaluate(()=>state.i),moves);if(moves===1)shots.push(await shot(p,stem,'veri'))}completed=true;
 }else if(r.kind==='process'){
  for(const action of r.sequence){const ix=r.actions.findIndex(a=>a.id===action);await p.locator(`[data-scene-action="${action}"],[data-action="${ix}"]`).first().click();moves++;assert.equal(await p.evaluate(()=>state.steps.length),moves);if(moves===1)shots.push(await shot(p,stem,'islem'))}completed=true;
 }else if(r.kind==='order'){
  for(const id of r.order){await p.locator(`[data-scene-order="${id}"],[data-order="${id}"]`).first().click();moves++}completed=true;
 }else if(r.kind==='memory'){
  const cards=await p.evaluate(()=>state.cards);for(const pair of [...new Set(cards.map(c=>c.pair))]){for(let i=0;i<cards.length;i++)if(cards[i].pair===pair){await p.locator(`[data-card="${i}"]`).click();moves++}await p.waitForTimeout(35)}completed=true;
 }else if(r.kind==='esle'){
  for(let i=0;i<r.yuvalar.length;i++){await p.locator(`[data-et="${r.yuvalar[i].dogru}"]`).click();await p.locator(`#stage [data-yuva="${i}"]`).click();moves++;assert.equal(await p.evaluate(()=>state.yerlesen.filter(x=>x!=null).length),moves)}completed=true;
 }else if(r.kind==='sira'){
  for(const i of r.dogru){await p.locator(`[data-kart="${i}"]`).click();moves++}completed=!r.sonYaz;
 }else if(['yaz','duzelt'].includes(r.kind)&&await p.locator('#yaziAlan,#duzeltAlan').count()){
  const field=p.locator('#stage textarea');assert.equal(await field.count(),1);await field.fill(r.ornekCevap||'Bugün kendi cümlemi yazıyorum.');moves++;assert.equal(await p.evaluate(()=>state.yazi),await field.inputValue());await field.press('End');await field.press('Space');assert.equal(await field.evaluate(e=>document.activeElement===e),true);assert.equal(await p.locator('#stage textarea').count(),1);
 }
 if(moves){await p.waitForTimeout(35);shots.push(await shot(p,stem,completed?'sonuc':'ilerleme'));const after=await geometry(p);assert(!after.horizontal&&!after.promptClipped&&!after.clipped,JSON.stringify(after));if(completed)assert(await p.evaluate(i=>locked||roundIndex>i||state.gecis,ri),'Bitiş doğrulanmadı')}
 records.push({id,title:g.title,width,height,round:ri+1,kind:r.kind,moves,completed,coverage:moves?'native-click-or-keyboard':'initial-layout-only',shots,initial});
 }catch(e){errors.push(stem+': '+e.stack);await shot(p,stem,'HATA');console.error(errors.at(-1))}finally{await p.close()}
 }console.log('SCENE',id)}
}finally{await browser.close();fs.writeFileSync(path.join(OUT,'scenes.json'),JSON.stringify({records,errors,note:'Real browser clicks/keyboard; fast 25ms transition displayed for 1200ms in test only. Initial layout-only records are not interaction proof. No physical-device or audio acceptance.'},null,2))}console.log('SCENES',records.length,'MOVES',records.reduce((s,r)=>s+r.moves,0),'ERRORS',errors.length);assert.equal(errors.length,0,errors.join('\n'))})();
