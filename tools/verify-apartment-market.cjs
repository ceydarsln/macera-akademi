'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/apartman-market-denetimi');
async function main(){
 fs.mkdirSync(OUT,{recursive:true});const results=[],errors=[];
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 try{for(const id of ['m17','m38']){const page=await browser.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser/matematik-pdf.html')).href+'#oyun='+id);
  for(const size of [{width:320,height:568},{width:390,height:844},{width:844,height:390}]){
   await page.setViewportSize(size);
   for(let ri=0;ri<3;ri++){
    await page.evaluate(i=>{roundIndex=i;locked=false;lives=3;state={};render()},ri);
    const bounds=await page.evaluate(id=>{const stage=document.querySelector('#visual').getBoundingClientRect();const sels=id==='m17'?'.delivery-tower .target':'.apple-cart,.apple-transfer';return {overflow:document.documentElement.scrollWidth>innerWidth+1,clipped:[...document.querySelectorAll(sels)].some(el=>{const r=el.getBoundingClientRect();return r.left<stage.left||r.right>stage.right||r.top<stage.top||r.bottom>stage.bottom})}},id);
    assert(!bounds.overflow&&!bounds.clipped,JSON.stringify({id,size,ri,bounds}));
    await page.screenshot({path:path.join(OUT,`${id}-${size.width}-tur${ri+1}.png`),fullPage:true});
    if(id==='m17'){
     const correct=await page.evaluate(()=>round().pieces[0].target);
     const source=page.locator('[data-piece]'),target=page.locator(`[data-target="${correct}"]`);
     const dragTo=async(to,cancel=false)=>{await source.scrollIntoViewIfNeeded();const a=await source.boundingBox(),b=await page.locator(to).boundingBox();await page.mouse.move(a.x+a.width/2,a.y+a.height/2);await page.mouse.down();await page.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:8});if(cancel)await source.dispatchEvent('pointercancel',{pointerId:1});await page.mouse.up()};
     await dragTo(`[data-target="${correct}"]`,true);assert.equal(await page.locator('.placed span').count(),0);
     await dragTo(`[data-target="${correct==='f1'?'f2':'f1'}"]`);assert.equal(await page.locator('.placed span').count(),0);
     await dragTo(`[data-target="${correct}"]`);assert.equal(await target.locator('.placed span').count(),1);
     await page.screenshot({path:path.join(OUT,`${id}-${size.width}-tur${ri+1}-sonuc.png`),fullPage:true});
     await page.waitForTimeout(1150);
    }else{
     assert(await page.locator('[data-choice]').first().isDisabled());await page.locator('.apple-experiment button').click();
     await page.waitForFunction(()=>!document.querySelector('.apple-experiment button').disabled);
     assert.equal(await page.locator('.apple-cart i').count(),[8,7,9][ri]);assert.equal(await page.locator('.apple-transfer i').count(),[0,2,0][ri]);
     await page.screenshot({path:path.join(OUT,`${id}-${size.width}-tur${ri+1}-sonuc.png`),fullPage:true});
     const correct=await page.evaluate(()=>round().choices.findIndex(c=>c.correct));await page.locator(`[data-choice="${correct}"]`).click();assert(await page.evaluate(()=>locked));await page.waitForTimeout(1150);
    }
    results.push({id,size,round:ri+1,...bounds,interaction:true});
   }
  }await page.close();
 }assert.deepEqual(errors,[]);fs.writeFileSync(path.join(OUT,'verification.json'),JSON.stringify({results,errors},null,2));console.log(JSON.stringify({passed:results.length,errors}));
 fs.writeFileSync(path.join(OUT,'index.html'),'<!doctype html><html lang="tr"><meta charset="utf-8"><title>Apartman ve market</title><style>body{font:18px system-ui;background:#eaf2f2;margin:24px}section{display:flex;gap:16px;flex-wrap:wrap}img{width:320px;max-width:100%}h2{margin-top:35px}</style><h1>Apartman ve market — etkileşim kontrolü</h1><p>Görüntüler sabittir. Hareketi görmek için oyun bağlantısını açın.</p>'+['m17','m38'].map(id=>`<h2>${id.toUpperCase()}</h2><p><a href="../../app/src/main/assets/phaser/matematik-pdf.html#oyun=${id}">Oyunu aç</a></p><section><img src="${id}-390-tur1.png"><img src="${id}-390-tur1-sonuc.png"></section>`).join(''));
 }finally{await browser.close()}
}
main().catch(e=>{console.error(e);process.exitCode=1});
