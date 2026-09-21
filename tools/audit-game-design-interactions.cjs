'use strict';
// Seçilmiş tasarım bulgularının gerçek fare hareketiyle kanıtı; tam oyun testi değildir.
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'artifacts/tasarim-denetimi-2026-09-21/etkilesimler');
const checks = [
  { slug:'matematik', id:'m37', from:'[data-piece="supply"]', to:'[data-target="loadTarget"]' },
  { slug:'matematik2', id:'v02', from:'[data-piece]', to:'[data-target]' },
  { slug:'matematik4', id:'p15', from:'[data-add="kasa"]', to:'[data-tepsi]' },
  { slug:'turkce4', id:'z04', from:'[data-kart="0"]', to:'[data-sira-hedef]' },
  { slug:'fen4', id:'f03', from:'[data-kart="0"]', to:'[data-sira-hedef]' },
  { slug:'hayatbilgisi2', id:'h12', from:'[data-esya="0"]', to:'[data-canta-hedef]' }
];
async function snapshot(page) {
  return page.evaluate(() => {
    const root = document.querySelector('#stage,#visual');
    return { state: JSON.parse(JSON.stringify(state)),
      artwork: [...root.querySelectorAll('svg')].map(x=>x.outerHTML),
      targetText: [...document.querySelectorAll('[data-target],[data-tepsi],[data-sira-hedef],[data-canta-hedef]')].map(x=>x.textContent.trim()),
      scale: document.querySelector('.experiment-scale')?.getAttribute('style'),
      animations: document.getAnimations().map(a=>({name:a.animationName||'transition',target:a.effect?.target?.getAttribute?.('class')}))
    };
  });
}
(async()=>{
  fs.mkdirSync(OUT,{recursive:true});
  const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
  const result=[];
  try {
    for(const c of checks){
      const ctx=await browser.newContext({viewport:{width:390,height:844}});
      const page=await ctx.newPage();
      await page.addInitScript(()=>{try{speechSynthesis.speak=()=>{}}catch(_){}});
      await page.goto(pathToFileURL(path.join(ROOT,`app/src/main/assets/phaser/${c.slug}-pdf.html`)).href+`?audit-action=${c.id}#oyun=${c.id}`);
      await page.waitForTimeout(200);
      if(c.id==='f03'||c.id==='z04') c.from=`[data-kart="${await page.evaluate(()=>round().dogru[0])}"]`;
      if(c.id==='v02') c.to=`[data-target="${await page.evaluate(()=>round().pieces[0].target)}"]`;
      const name=`${c.slug}-${c.id}`, before=await snapshot(page);
      await page.screenshot({path:path.join(OUT,`${name}-once.png`)});
      const a=await page.locator(c.from).first().boundingBox(),b=await page.locator(c.to).first().boundingBox();
      if(!a||!b)throw Error(`${c.id}: hedef/kaynak yok`);
      await page.mouse.move(a.x+a.width/2,a.y+a.height/2);await page.mouse.down();
      await page.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:20});await page.mouse.up();
      await page.waitForTimeout(150);
      const after=await snapshot(page);
      await page.screenshot({path:path.join(OUT,`${name}-sonra.png`)});
      await page.waitForTimeout(800);
      await ctx.close();
      result.push({...c,before,after,svgChanged:JSON.stringify(before.artwork)!==JSON.stringify(after.artwork),stateChanged:JSON.stringify(before.state)!==JSON.stringify(after.state)});
      console.log(`${name}: durum değişti=${result.at(-1).stateChanged}, SVG değişti=${result.at(-1).svgChanged}`);
    }
    // Konuşma tuşunun gerçek basma/bırakma ömrü: durumu elle tamamlamıyoruz.
    const page=await browser.newPage({viewport:{width:390,height:844}});
    await page.addInitScript(()=>{try{speechSynthesis.speak=()=>{}}catch(_){}});
    await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser/turkce4-pdf.html')).href+'?audit-hold=z09#oyun=z09');
    const ri=await page.evaluate(()=>game.rounds.findIndex(r=>r.kind==='konus'));
    if(ri<0)throw Error('Z09 konuşma turu bulunamadı');
    await page.evaluate(i=>{roundIndex=i;render()},ri);
    await page.locator('#ornekDinle').click();await page.locator('#konusBasla').click();
    const b=await page.locator('#konusTut').boundingBox();
    await page.mouse.move(b.x+b.width/2,b.y+b.height/2);await page.mouse.down();
    await page.waitForTimeout(1400);await page.mouse.up();
    const release=await page.evaluate(()=>({basili:state.basili,sure:state.sure,bitti:!!document.querySelector('#konusBitti')}));
    await page.waitForTimeout(300);
    const later=await page.evaluate(()=>({basili:state.basili,sure:state.sure,bitti:!!document.querySelector('#konusBitti')}));
    result.push({slug:'turkce4',id:'z09',round:ri+1,hold:{release,later}});
    console.log('Z09 tuş bırakma:',JSON.stringify({release,later}));
    await page.close();
  }finally{await browser.close();fs.writeFileSync(path.join(OUT,'probes.json'),JSON.stringify(result,null,2));}
})().catch(e=>{console.error(e);process.exitCode=1});
