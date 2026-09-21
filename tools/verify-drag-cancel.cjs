'use strict';
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url'),{chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/katalog-kabul-635');
const cases=[
 ['matematik3','w01'],['matematik4','p21'],['turkce3','y02'],
 ['matematik4','p10','[data-add="ceyrek"]','[data-tepsi]'],
 ['matematik3','w05','[data-share-piece]','[data-share="a"]'],
 ['turkce3','y07','[data-k="0"]','[data-cumle-serit]'],
 ['turkce4','z18','[data-kart="0"]','[data-sira-hedef]'],
 ['fen3','g01','[data-sinif-kart]','[data-kutu="0"]'],
 ['fen4','f01','[data-sinif-kart]','[data-kutu="0"]'],
 ['hayatbilgisi2','h02']
];
async function main(){
 fs.mkdirSync(OUT,{recursive:true});const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});const results=[];
 try{for(const [slug,id,from,to] of cases){
  const page=await browser.newPage({viewport:{width:900,height:900}});
  try{
   await page.addInitScript(()=>{try{speechSynthesis.speak=()=>{}}catch(_){}});
   await page.goto(pathToFileURL(path.join(ROOT,`app/src/main/assets/phaser/${slug}-pdf.html`)).href+'?cancel='+id+'#oyun='+id);
   let source=from,target=to;
   if(!source){const r=await page.evaluate(()=>JSON.parse(JSON.stringify(round())));if(r.kind==='drag'){const p=r.pieces.find(p=>p.target);source=`[data-piece="${p.id}"]`;target=`[data-target="${p.target}"]`}else{source='[data-sinif-kart]';target=`[data-kutu="${r.kartlar[0].dogru}"]`}}
   const before=await page.evaluate(()=>JSON.stringify({state,lives,roundIndex}));
   const a=await page.locator(source).first().boundingBox(),b=await page.locator(target).first().boundingBox();
   await page.mouse.move(a.x+a.width/2,a.y+a.height/2);await page.mouse.down();await page.mouse.move(b.x+b.width/2,b.y+b.height/2,{steps:9});
   await page.locator(source).first().dispatchEvent('pointercancel',{pointerId:1,clientX:b.x+b.width/2,clientY:b.y+b.height/2});await page.mouse.up();
   const after=await page.evaluate(()=>JSON.stringify({state,lives,roundIndex}));
   let normalDrop=null;
   if(before===after){
    const a2=await page.locator(source).first().boundingBox(),b2=await page.locator(target).first().boundingBox();
    await page.mouse.move(a2.x+a2.width/2,a2.y+a2.height/2);await page.mouse.down();await page.mouse.move(b2.x+b2.width/2,b2.y+b2.height/2,{steps:9});await page.mouse.up();
    normalDrop=before!==await page.evaluate(()=>JSON.stringify({state,lives,roundIndex}));
   }
   results.push({slug,id,unchanged:before===after,normalDrop,source,target});console.log(`${before===after&&normalDrop?'✓':'✗'} ${id}: iptal ${before===after?'durumu korudu':'durumu değiştirdi'}, normal bırakma ${normalDrop}`);
  }catch(e){results.push({slug,id,error:e.message});console.log('✗ '+id+': '+e.message)}finally{await page.close()}
 }}finally{await browser.close()}
 fs.writeFileSync(path.join(OUT,process.argv.includes('--baseline')?'cancel-before.json':'cancel-after.json'),JSON.stringify(results,null,2));
 if(results.some(r=>!r.unchanged||!r.normalDrop)&&!process.argv.includes('--baseline'))process.exitCode=1;
}
main().catch(e=>{console.error(e);process.exitCode=1});
