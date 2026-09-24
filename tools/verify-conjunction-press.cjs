'use strict';
const assert=require('assert');
const path=require('path');
const {pathToFileURL}=require('url');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const url=pathToFileURL(path.join(root,'app/src/main/assets/phaser/turkce4-pdf.html')).href+'?test=1&conjunction-mobile#oyun=z33';
const sizes=[[320,568],[390,844],[844,390]];
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 const results=[];
 try{for(const [width,height] of sizes){
  const page=await browser.newPage({viewport:{width,height}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(url);await page.locator('[data-sentence-slot]').waitFor();
  const state=await page.evaluate(()=>{const slot=document.querySelector('[data-sentence-slot]').getBoundingClientRect(),words=[...document.querySelectorAll('[data-kutu]')].map(e=>e.getBoundingClientRect());return {horizontal:document.documentElement.scrollWidth>innerWidth+1,slot:{top:slot.top,bottom:slot.bottom,width:slot.width,height:slot.height},words:words.map(b=>({top:b.top,bottom:b.bottom,width:b.width,height:b.height}))}});
  assert(!state.horizontal,`${width} yatay taşma`);
  assert(state.slot.width>=44&&state.slot.height>=44&&state.slot.top>=0&&state.slot.bottom<=height,`${width} cümle yuvası görünmüyor: ${JSON.stringify(state.slot)}`);
  assert(state.words.every(b=>b.width>=44&&b.height>=44&&b.top>=0&&b.bottom<=height),`${width} sözcükler görünmüyor: ${JSON.stringify(state.words)}`);
  const right=await page.evaluate(()=>round().kartlar[0].dogru),count=state.words.length;
  await page.locator(`[data-kutu="${(right+1)%count}"]`).click();assert.equal(await page.evaluate(()=>state.ix),0,`${width} yanlış sözcük kabul edildi`);
  const from=await page.locator(`[data-kutu="${right}"]`).boundingBox(),to=await page.locator('[data-sentence-slot]').boundingBox();assert(from&&to);
  await page.mouse.move(from.x+from.width/2,from.y+from.height/2);await page.mouse.down();await page.mouse.move(to.x+to.width/2,to.y+to.height/2,{steps:12});await page.mouse.up();
  await page.waitForFunction(()=>state.ix===1);assert.equal(await page.locator('.conjunction-slot.conjunction-filled').count(),1,`${width} cümle doldurulmadı`);
  assert.deepEqual(errors,[]);results.push({viewport:`${width}x${height}`,wrongRejected:true,dragInserted:true});await page.close();
 }}finally{await browser.close()}
 console.log(JSON.stringify({passed:results.length,results}));
})().catch(e=>{console.error(e);process.exitCode=1});
