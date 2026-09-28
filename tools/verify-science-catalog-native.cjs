'use strict';
// Actual browser inputs only. Reading round definitions chooses answers; it never sets game state.
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url');
const {chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/fen-hayat-katalog-oynanis');
const selected=process.argv.slice(2).filter(a=>!a.startsWith('--')),resume=process.argv.includes('--retry'),defs=JSON.parse(fs.readFileSync(path.join(ROOT,'artifacts/tam-tasarim-incelemesi/definitions.json')));
const games=defs.filter(g=>['fen3','fen4','hayatbilgisi2'].includes(g.slug)&&(!selected.length||selected.includes(g.id)));
const solvers=Object.fromEntries(['fen3','fen4','hayatbilgisi2'].map(s=>[s,require('./pdf-'+s+'-smoke.js').solveRound]));
const {createHash}=require('crypto');
function fingerprint(slug){const file=path.join(ROOT,'app/src/main/assets/phaser',slug+'-pdf.html'),body=fs.readFileSync(file,'utf8'),files=[file,...[...body.matchAll(/(?:src|href)=["']([^"']+)["']/g)].map(m=>m[1].split(/[?#]/)[0]).filter(p=>/\.(js|css)$/.test(p)).map(p=>path.resolve(path.dirname(file),p)).filter(p=>p.startsWith(path.dirname(file)+path.sep)&&fs.existsSync(p))];const h=createHash('sha256');for(const f of [...new Set(files)].sort())h.update(path.basename(f)).update(fs.readFileSync(f));return h.digest('hex')}
async function click(p,s){await p.locator(s).click();await p.waitForTimeout(100);if(await p.evaluate(()=>!!state.gecis))await p.waitForFunction(()=>!state.gecis)}
async function hold(p,s,condition,arg){await p.locator(s).scrollIntoViewIfNeeded();const b=await p.locator(s).boundingBox();await p.mouse.move(b.x+b.width/2,b.y+b.height/2);await p.mouse.down();try{await p.waitForFunction(condition,arg,{polling:'raf',timeout:30000})}finally{await p.mouse.up()}}
async function range(p,s,value){await p.locator(s).focus();await p.keyboard.press('Home');const info=await p.locator(s).evaluate(e=>({min:+e.min,step:+e.step||1}));for(let i=0;i<Math.round((value-info.min)/info.step);i++)await p.keyboard.press('ArrowRight')}
async function solve(p,r,slug){
 if(r.kind==='sula'){await hold(p,'#tut',v=>state.verilen>=v,Math.ceil((r.uygunAlt+r.uygunUst)/2));await click(p,'#sulaOk')}
 else if(r.kind==='isit'){await hold(p,'#isitBtn',()=>state.oran>=1);await click(p,'#durBtn')}
 else if(r.kind==='olcum'){await range(p,'#olcek',r.dogru);await click(p,'#olcOk')}
 else if(r.kind==='mesafe'){for(const d of r.durumlar){await range(p,'#mesafeAlan',Math.round((d.enAz+d.enCok)/10)*5);await click(p,'#mesafeOk')}}
 else if(r.kind==='musluk'){for(const d of r.isler){await hold(p,'#musluk',v=>state.yuzde>=v,(d.enAz+d.enCok)/2);await click(p,'#muslukOk')}}
 else if(r.kind==='konus'){await click(p,'#ornekDinle');await click(p,'#konusBasla');await hold(p,'#konusTut',()=>state.sure>=1400);await click(p,'#konusBitti');for(let i=0;i<r.olcutler.length;i++)await click(p,`[data-ol="${i}"]`);await click(p,'#konusOk')}
 else await solvers[slug](p,r);
}
(async()=>{fs.mkdirSync(OUT,{recursive:true});const file=path.join(OUT,'results.json'),old=fs.existsSync(file)?JSON.parse(fs.readFileSync(file)):null,records=resume&&old?old.records.filter(r=>r.passed&&r.sourceHash===fingerprint(r.slug)):selected.length&&old?old.records.filter(r=>!selected.includes(r.id)):[];if(resume){const passed=new Set(records.map(r=>r.id));for(let i=games.length-1;i>=0;i--)if(passed.has(games[i].id))games.splice(i,1)}let next=0;
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
function save(){fs.writeFileSync(file,JSON.stringify({records,note:'Production timing; native mouse/keyboard, no answer/life/round injection. Correct three-round route and restart only. Negative paths, physical phones, audio and visual approval remain separate.'},null,2))}
try{await Promise.all(Array.from({length:3},async()=>{while(next<games.length){const g=games[next++],p=await browser.newPage({viewport:{width:390,height:844}});p.setDefaultTimeout(7000);const rec={id:g.id,slug:g.slug,sourceHash:fingerprint(g.slug),date:new Date().toISOString(),rounds:[],errors:[],passed:false};p.on('pageerror',e=>rec.errors.push(e.message));await p.addInitScript(()=>{try{speechSynthesis.speak=()=>{};speechSynthesis.cancel=()=>{}}catch(_){}});
try{await p.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser',g.slug+'-pdf.html')).href+'?native='+g.id+'#oyun='+g.id);assert.equal(await p.evaluate(()=>GAME_ID),g.id);
for(let ri=0;ri<3;ri++){assert.equal(await p.evaluate(()=>roundIndex),ri);const r=await p.evaluate(()=>JSON.parse(JSON.stringify(round(),(k,v)=>typeof v==='function'?undefined:v)));const before=`${g.id}-tur${ri+1}-baslangic.png`,after=`${g.id}-tur${ri+1}-sonuc.png`;await p.screenshot({path:path.join(OUT,before),fullPage:true});await solve(p,r,g.slug);const resultVisible=await p.evaluate(i=>roundIndex===i,ri);if(resultVisible)await p.screenshot({path:path.join(OUT,after),fullPage:true});await p.waitForFunction(i=>roundIndex>i||!!document.querySelector('.overlay'),ri,{timeout:12000});assert.equal(await p.evaluate(()=>lives),3);rec.rounds.push({round:ri+1,kind:r.kind,before,after:resultVisible?after:null});}
assert.equal(await p.locator('.overlay').count(),1);await p.screenshot({path:path.join(OUT,g.id+'-bitis.png'),fullPage:true});await Promise.all([p.waitForEvent('domcontentloaded'),p.locator('.overlay button').click()]);await p.waitForFunction(()=>roundIndex===0&&!locked);assert.equal(rec.errors.length,0);rec.passed=true;
}catch(e){rec.errors.push(e.message);await p.screenshot({path:path.join(OUT,g.id+'-hata.png'),fullPage:true})}finally{await p.close();records.push(rec);save();console.log(rec.passed?'PASS':'FAIL',g.id,rec.errors.join(' ').slice(0,200))}}}));}finally{await browser.close();save()}
console.log(records.filter(r=>r.passed).length+'/'+records.length);if(records.some(r=>!r.passed))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
