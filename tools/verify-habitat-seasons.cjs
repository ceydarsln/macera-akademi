'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/sinif-sahneleri-denetimi');
const games=[{id:'z01',file:'turkce4-pdf.html',rounds:2},{id:'g43',file:'fen3-pdf.html',rounds:2},{id:'h26',file:'hayatbilgisi2-pdf.html',rounds:1}];
const sizes=[{width:320,height:568},{width:390,height:844},{width:844,height:390}];
async function main(){fs.mkdirSync(OUT,{recursive:true});const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});const report=[],errors=[];
try{for(const game of games)for(const size of sizes){const page=await browser.newPage({viewport:size});page.on('pageerror',e=>errors.push(game.id+': '+e.message));
 await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser',game.file)).href+'?test=1&review=classification#oyun='+game.id);
 await page.locator('[data-sinif-kart]').waitFor();
 for(let turn=0;turn<game.rounds;turn++){
  assert.equal(await page.evaluate(()=>roundIndex),turn);
  const first=await page.evaluate(()=>round().kartlar[0].dogru);const wrong=(first+1)%await page.locator('[data-kutu]').count();
  if(turn===0){const source=page.locator('[data-sinif-kart]:not(.scene-drag-ghost)'),s=await source.boundingBox(),t=await page.locator(`[data-kutu="${first}"]`).boundingBox();assert(s&&t);
   await page.mouse.move(s.x+s.width/2,s.y+s.height/2);await page.mouse.down();await page.mouse.move(t.x+t.width/2,t.y+t.height/2,{steps:8});await source.dispatchEvent('pointercancel',{pointerId:1});await page.mouse.up();assert.equal(await page.evaluate(()=>state.ix),0);
   await page.locator(`[data-kutu="${wrong}"]`).click();assert.equal(await page.evaluate(()=>state.ix),0);
  }
  if(size.width===390&&turn===0)await page.screenshot({path:path.join(OUT,game.id+'-ilk.png'),fullPage:true});
  const n=await page.evaluate(()=>round().kartlar.length);
  for(let i=0;i<n;i++){const j=await page.evaluate(()=>round().kartlar[state.ix].dogru);const source=page.locator('[data-sinif-kart]:not(.scene-drag-ghost)'),target=page.locator(`[data-kutu="${j}"]`);
   const s=await source.boundingBox(),t=await target.boundingBox();assert(s&&t,game.id+' kayıp kaynak/hedef');
   await page.mouse.move(s.x+s.width/2,s.y+s.height/2);await page.mouse.down();await page.mouse.move(t.x+t.width/2,t.y+t.height/2,{steps:8});await page.mouse.up();
   await page.waitForFunction(index=>state.ix>index,i,{timeout:3000}).catch(()=>{});
   assert.equal(await page.evaluate(()=>state.ix),i+1);
   if(i<n-1)await page.waitForFunction(index=>!state.gecis&&state.ix===index,i+1,{timeout:3000}).catch(()=>{});
  }
  await page.waitForFunction(index=>roundIndex>index,turn,{timeout:5000});
 }
 if(size.width===390)await page.screenshot({path:path.join(OUT,game.id+'-sonraki-tur.png'),fullPage:true});
 await page.evaluate(()=>{roundIndex=0;render()});
 const m=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,visible:[...document.querySelectorAll('[data-kutu],[data-sinif-kart]')].every(el=>{const b=el.getBoundingClientRect();return b.width>0&&b.height>0&&b.left>=0&&b.right<=innerWidth+1&&b.top>=0&&b.bottom<=innerHeight+1})}));assert(!m.overflow&&m.visible,JSON.stringify({game:game.id,size,m}));report.push({game:game.id,size,...m});
 if(size.width!==390)await page.screenshot({path:path.join(OUT,game.id+'-'+size.width+'x'+size.height+'.png'),fullPage:true});await page.close();
 }assert.deepEqual(errors,[]);fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({report,errors},null,2));console.log(JSON.stringify({passed:report.length,errors}));
 fs.writeFileSync(path.join(OUT,'index.html'),'<!doctype html><html lang="tr"><meta charset="utf-8"><title>Üç farklı sınıflandırma sahnesi</title><style>body{font:17px system-ui;background:#eaf0f1;margin:20px}section{display:flex;flex-wrap:wrap;gap:12px}img{width:300px;max-width:100%}</style><h1>Tartışma, yaşam alanı ve mevsim sahneleri</h1>'+games.map(g=>`<h2>${g.id.toUpperCase()}</h2><section><img src="${g.id}-ilk.png"><img src="${g.id}-sonraki-tur.png"><img src="${g.id}-320x568.png"><img src="${g.id}-844x390.png"></section>`).join(''));
}finally{await browser.close()}}
main().catch(e=>{console.error(e);process.exitCode=1});
