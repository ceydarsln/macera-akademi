'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/deyim-denge-denetimi');
async function main(){fs.mkdirSync(OUT,{recursive:true});const report=[],errors=[];
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 try{for(const id of ['y47','y62']){const page=await browser.newPage({viewport:{width:390,height:844}});page.on('pageerror',e=>errors.push(id+': '+e.message));
  await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser/turkce3-pdf.html')).href+'?review=idiom-rights#oyun='+id);await page.locator('[data-target]').first().waitFor();
  const drag=async(pid,tid,cancel=false)=>{const a=page.locator(`[data-piece="${pid}"]:not(.scene-drag-ghost)`),b=page.locator(`[data-target="${tid}"]`);await a.scrollIntoViewIfNeeded();const x=await a.boundingBox(),y=await b.boundingBox();assert(x&&y);await page.mouse.move(x.x+x.width/2,x.y+x.height/2);await page.mouse.down();await page.mouse.move(y.x+y.width/2,y.y+y.height/2,{steps:9});if(cancel)await a.dispatchEvent('pointercancel',{pointerId:1});await page.mouse.up()};
  await page.screenshot({path:path.join(OUT,id+'-ilk.png'),fullPage:true});
  await drag('a','t1',true);assert.equal(await page.evaluate(()=>state.done),0);
  await drag('a','t2');assert.equal(await page.evaluate(()=>state.done),0);
  await page.waitForTimeout(1000);
  const ps=await page.evaluate(()=>round().pieces.map(p=>({id:p.id,target:p.target})));
  for(let i=0;i<ps.length;i++){await drag(ps[i].id,ps[i].target);assert.equal(await page.evaluate(()=>state.done),i+1);assert.equal(await page.locator('.filled').count(),i+1)}
  await page.screenshot({path:path.join(OUT,id+'-sonuc.png'),fullPage:true});await page.waitForFunction(()=>roundIndex===1);
  for(const size of [{width:320,height:568},{width:390,height:844},{width:844,height:390}]){
   await page.setViewportSize(size);await page.evaluate(()=>{roundIndex=0;render()});
   const m=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+2,visible:[...document.querySelectorAll('[data-target],[data-piece]')].every(e=>{const b=e.getBoundingClientRect();return b.width>0&&b.height>0&&b.left>=0&&b.right<=innerWidth+1&&b.top>=0&&b.bottom<=innerHeight+1})}));
   assert(!m.overflow&&m.visible,JSON.stringify({id,size,m}));await page.screenshot({path:path.join(OUT,id+'-'+size.width+'x'+size.height+'.png'),fullPage:true});
   report.push({id,size,...m});
  }await page.close();
 }assert.deepEqual(errors,[]);fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({report,errors},null,2));console.log(JSON.stringify({passed:report.length,errors}));
 fs.writeFileSync(path.join(OUT,'index.html'),'<!doctype html><html lang="tr"><meta charset="utf-8"><title>Deyim Makinesi ve Denge Köprüsü</title><style>body{font:17px system-ui;background:#e6eff0;margin:20px}section{display:flex;flex-wrap:wrap;gap:12px}img{width:300px;max-width:100%}</style><h1>Deyim Makinesi ve Denge Köprüsü</h1>'+['y47','y62'].map(id=>`<h2>${id.toUpperCase()}</h2><p><a href="../../app/src/main/assets/phaser/turkce3-pdf.html#oyun=${id}">Oyunu aç</a></p><section><img src="${id}-ilk.png"><img src="${id}-sonuc.png"><img src="${id}-320x568.png"></section>`).join(''));
 }finally{await browser.close()}}
main().catch(e=>{console.error(e);process.exitCode=1});
