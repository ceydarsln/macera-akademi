'use strict';
// Teknik kanıt toplar; görsel tasarım onayı otomatik verilmez.
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url'),{execFileSync}=require('child_process');
const {chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/katalog-kabul-635');
const baseline=JSON.parse(fs.readFileSync(path.join(ROOT,'artifacts/tasarim-denetimi-2026-09-21/audit.json')));
const filter=process.argv.slice(2).filter(a=>!a.startsWith('--'));
const jobs=baseline.games.filter(g=>!filter.length||filter.includes(g.id));
const evidence=path.join(OUT,'results.json');
const prior=fs.existsSync(evidence)?JSON.parse(fs.readFileSync(evidence)):[];
const records=new Map(prior.map(r=>[r.id,r]));
const sceneEvidence=JSON.parse(fs.readFileSync(path.join(ROOT,'docs/OYUN_SAHNE_KANITLARI.json'))).games;
const sceneById=new Map(sceneEvidence.map(g=>[g.id,g]));
const packageLink=n=>'../sahne-duzeltmeleri'+(n===1?'':'-'+n)+'-'+(n>=8?'2026-09-23':'2026-09-21')+'/index.html';
const {createHash}=require('crypto');
function sourceHash(slug){
 const html=path.join(ROOT,'app/src/main/assets/phaser',slug+'-pdf.html'),body=fs.readFileSync(html,'utf8');
 const files=[html,...[...body.matchAll(/(?:src|href)=["']([^"']+)["']/g)].map(m=>m[1].split(/[?#]/)[0]).filter(p=>/\.(?:js|css)$/.test(p)).map(p=>path.resolve(path.dirname(html),p)).filter(p=>p.startsWith(path.dirname(html)+path.sep)&&fs.existsSync(p))];
 const hash=createHash('sha256');for(const file of [...new Set(files)].sort())hash.update(path.basename(file)).update(fs.readFileSync(file));
 return hash.digest('hex');
}
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const commit=execFileSync('git',['rev-parse','--short','HEAD'],{cwd:ROOT,encoding:'utf8'}).trim();
async function capture(page,context,g,n,result,iframe=false){
 const meta=await context.evaluate(()=>{
  const s=document.querySelector('#stage,#visual'),p=document.querySelector('.prompt');
  const visible=e=>{const b=e.getBoundingClientRect();return b.width&&b.height&&getComputedStyle(e).visibility!=='hidden'};
  // Gözlem cevapları bırakma hedefi değildir; deneyde hedef mıknatısın kendisidir.
  const targets=[...document.querySelectorAll('[data-target],[data-kutu],[data-yuva],[data-sira-hedef],[data-canta-hedef],[data-kur-hedef],[data-tepsi],[data-magnet-target]')].filter(e=>visible(e)&&!e.hasAttribute('data-observation-answer'));
  const r=round();return {actualId:GAME_ID,kind:r.kind||'choose',prompt:p?.textContent,promptClipped:p?p.scrollHeight>p.clientHeight+3:false,
   externalTargets:targets.filter(t=>!s?.contains(t)).map(t=>({text:t.textContent.trim().slice(0,100),class:t.getAttribute('class')})),
   horizontal:[...document.querySelectorAll('button,[data-piece]')].filter(visible).filter(e=>{const b=e.getBoundingClientRect();return b.left< -3||b.right>innerWidth+3}).map(e=>e.textContent.trim().slice(0,70)),
   targetCount:targets.length,sceneStateFunctions:['scene','sahne','art'].filter(k=>typeof r[k]==='function')};
 });
 if(meta.actualId!==g.id)throw Error('Yanlış oyun kimliği: '+meta.actualId);
 const file=`screens/${g.slug}-${g.id}-${n}.png`;
 if(iframe)await page.locator('#cerceve').screenshot({path:path.join(OUT,file)});else await page.screenshot({path:path.join(OUT,file)});
 result.rounds.push({round:n,...meta,screenshot:file});
}
function save(){
 const list=[...records.values()].sort((a,b)=>baseline.games.findIndex(g=>g.id===a.id)-baseline.games.findIndex(g=>g.id===b.id));
 fs.writeFileSync(evidence,JSON.stringify(list,null,2));
 fs.writeFileSync(path.join(OUT,'acceptance-ledger.json'),JSON.stringify(baseline.games.map(g=>{
  const r=records.get(g.id),s=sceneById.get(g.id);
  return {id:g.id,slug:g.slug,title:g.title,technical:{solve:r?.solve||'pending',rounds:r?.rounds.length||0,date:r?.date||null,sourceHash:r?.sourceHash||null},design:{status:'pending',scopedSceneUpdate:s||null,evidence:s?packageLink(s.package):null},signals:{externalTargets:r?.rounds.some(t=>t.externalTargets.length)||false,promptClipped:r?.rounds.some(t=>t.promptClipped)||false,horizontal:r?.rounds.some(t=>t.horizontal.length)||false}};
 }),null,2));
 const pass=list.filter(r=>r.solve==='passed').length,fail=list.filter(r=>r.solve==='failed').length;
 const cards=baseline.games.map(g=>{const r=records.get(g.id),scene=sceneById.get(g.id);return `<article data-scene="${scene?'updated':'pending'}" data-id="${g.id}" data-state="${r?.solve||'pending'}"><h3>${esc(g.id.toUpperCase())} · ${esc(g.title)}</h3><p>${r? r.solve==='passed'?'Üç tur teknik çözüm geçti':'Teknik kontrol başarısız':'Sırada'} · <strong>Tasarım onayı bekliyor</strong></p>${scene?`<p><b>Hedefli sahne düzeltmesi · tur ${scene.rounds.join(', ')}</b><br>${esc(scene.scope)} <a href="${packageLink(scene.package)}">Önce / sonra ve etkileşim kanıtı</a></p>`:'<p>Oyun özelinde tam tasarım kabulü kaydedilmedi.</p>'}${r?.error?`<pre>${esc(r.error)}</pre>`:''}<div class="rounds">${(r?.rounds||[]).map(t=>`<a href="${t.screenshot}"><img loading="lazy" src="${t.screenshot}" alt="${g.id} tur ${t.round}"><span>Tur ${t.round} · ${esc(t.kind)}</span></a>`).join('')}</div><a href="../../app/src/main/assets/phaser/${g.slug}-pdf.html?acceptance=${g.id}#oyun=${g.id}">Oyunu aç</a></article>`}).join('');
 fs.writeFileSync(path.join(OUT,'index.html'),`<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>635 oyun kabul takibi</title><style>body{font:15px system-ui;background:#edf2f5;color:#213b4c;margin:0}header{position:sticky;top:0;padding:16px;background:#fff;z-index:2;box-shadow:0 2px 10px #1232}main{max-width:1150px;margin:auto;padding:16px}article{background:white;padding:16px;margin:20px 0;border-radius:15px}.rounds{display:flex;gap:12px}.rounds a{width:33.33%}img{width:100%;border:1px solid #bcc}a{color:#13618a}pre{white-space:pre-wrap;font-size:12px;color:#a23}input,select{font:inherit;padding:10px;max-width:100%}</style><header><b>635 oyun · teknik geçti ${pass} · başarısız ${fail} · sırada ${635-list.length}</b><p>Teknik çözüm, tasarım veya gerçek sürükleme onayı değildir. ${sceneEvidence.length} oyunda hedefli sahne düzeltmesi kaydı var; bu kayıtlar bütün tur türlerinin tasarım onayı değildir. Ortak sürükleme iptali düzeltmesi ayrı bir teknik değişikliktir. Bu sayfa tüm oyunların kabul edildiği iddiasında bulunmaz.</p><p><a href="acceptance-ledger.json">635 oyunluk ayrı kabul kayıtları</a></p><input id="search" placeholder="Oyun adı / kimlik"><select id="state"><option value="">Hepsi</option><option value="failed">Teknik hata</option><option value="pending">Sırada</option><option value="passed">Teknik geçti</option></select><select id="design"><option value="">Tüm tasarım kayıtları</option><option value="updated">Hedefli sahne düzeltmesi</option><option value="pending">Sahne düzeltmesi kaydı yok</option></select></header><main>${cards}</main><script>function filter(){const q=document.querySelector('#search').value.toLocaleLowerCase('tr'),s=document.querySelector('#state').value,d=document.querySelector('#design').value;document.querySelectorAll('article').forEach(a=>a.hidden=!a.textContent.toLocaleLowerCase('tr').includes(q)||(s&&a.dataset.state!==s)||(d&&a.dataset.scene!==d))}document.querySelector('#search').oninput=filter;document.querySelector('#state').onchange=filter;document.querySelector('#design').onchange=filter;</script></html>`);
}
async function main(){
 fs.mkdirSync(path.join(OUT,'screens'),{recursive:true});save();
 if(process.argv.includes('--report-only'))return;
 if(filter.some(id=>!baseline.games.some(g=>g.id===id)))throw Error('Katalogda bulunmayan oyun kimliği: '+filter.filter(id=>!baseline.games.some(g=>g.id===id)).join(', '));
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 let next=0,completed=0;
 try{await Promise.all([0,1,2,3].map(async()=>{
  while(next<jobs.length){
   const g=jobs[next++];if(process.argv.includes('--resume')&&records.has(g.id))continue;
   const fen=g.slug==='fen3'||g.slug==='fen4';
   const result={id:g.id,slug:g.slug,title:g.title,commit,sourceHash:sourceHash(g.slug),date:new Date().toISOString(),solve:'running',design:'pending',rounds:[],errors:[]};
   const page=await browser.newPage({viewport:{width:fen?390:810,height:844}});page.setDefaultTimeout(12000);
   page.on('pageerror',e=>result.errors.push(e.message));
   await page.addInitScript(()=>{try{speechSynthesis.speak=()=>{};speechSynthesis.cancel=()=>{}}catch(_){}});
   try{
    if(fen){
     await page.goto(pathToFileURL(path.join(ROOT,`app/src/main/assets/phaser/${g.slug}-pdf.html`)).href+`?test=1&acceptance=${g.id}#oyun=${g.id}`);
     const {solveRound}=require('./pdf-'+g.slug+'-smoke.js');
     for(let i=0;i<3;i++){
      if(await page.evaluate(()=>roundIndex)!==i)throw Error('Beklenmeyen tur');
      await capture(page,page,g,i+1,result);
      const r=await page.evaluate(()=>JSON.parse(JSON.stringify(round(),(k,v)=>typeof v==='function'?undefined:v)));
      await solveRound(page,r);await page.waitForFunction(i=>roundIndex>i||!!document.querySelector('.overlay'),i,{timeout:15000});
     }
     if(!await page.evaluate(()=>!!document.querySelector('.overlay')&&lives===3))throw Error('Bitiş/can doğrulanmadı');
    }else{
     await page.exposeFunction('__captureRound',async({round})=>{const frame=page.frames().find(f=>f!==page.mainFrame());await capture(page,frame,g,round,result,true)});
     await page.goto(pathToFileURL(path.join(ROOT,'tools/dom_kosum.html')).href+'#ids='+g.id);
     await page.waitForFunction(()=>window.SONUC?.bitti,null,{timeout:120000});
     const res=await page.evaluate(()=>SONUC);if(!res.gecti.includes(g.id))throw Error(res.hatalar.join('\n'));
    }
    if(result.errors.length)throw Error(result.errors.join('\n'));result.solve='passed';
   }catch(e){result.solve='failed';result.error=e.message}
   finally{await page.close()}
   records.set(g.id,result);completed++;save();console.log(`${completed}/${jobs.length} ${g.id}: ${result.solve}${result.error?' '+result.error.slice(0,160):''}`);
  }
 }));}finally{await browser.close();save()}
 console.log('REPORT '+OUT);
 if(jobs.some(g=>records.get(g.id)?.solve!=='passed'))process.exitCode=1;
}
main().catch(e=>{console.error(e);process.exitCode=1});
