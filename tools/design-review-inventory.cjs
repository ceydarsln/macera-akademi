'use strict';
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url'),{chromium}=require('playwright'),sharp=require('sharp');
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'artifacts/tam-tasarim-incelemesi');
const ledger=JSON.parse(fs.readFileSync(path.join(ROOT,'artifacts/katalog-kabul-635/acceptance-ledger.json')));
async function main(){
 fs.mkdirSync(OUT,{recursive:true});
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files','--disable-speech-api']});
 const definitions=[];
 try{for(const slug of [...new Set(ledger.map(g=>g.slug))]){
  const games=ledger.filter(g=>g.slug===slug),page=await browser.newPage();
  await page.goto(pathToFileURL(path.join(ROOT,'app/src/main/assets/phaser',slug+'-pdf.html')).href+'?inventory=1#oyun='+games[0].id);
  const data=await page.evaluate(ids=>ids.map(id=>({id,...JSON.parse(JSON.stringify(GAMES[id],(k,v)=>typeof v==='function'?{functionSource:v.toString()}:v))})),games.map(g=>g.id));
  definitions.push(...data.map(g=>({...g,slug})));await page.close();
 }}finally{await browser.close()}
 fs.writeFileSync(path.join(OUT,'definitions.json'),JSON.stringify(definitions,null,2));
 const sheets=[];
 // Every game, every round: each row has one game with its three round screens.
 for(let offset=0;offset<ledger.length;offset+=6){
  const batch=ledger.slice(offset,offset+6),composite=[];
  for(let i=0;i<batch.length;i++){
   const g=batch[i],x=(i%2)*600,y=Math.floor(i/2)*460;
   const label=(g.id+' · '+g.title).replace(/[&<>]/g,'');
   composite.push({input:Buffer.from('<svg width="600" height="30"><rect width="600" height="30" fill="#173544"/><text x="8" y="21" font-size="16" fill="white">'+label+'</text></svg>'),left:x,top:y});
   for(let n=1;n<=3;n++){const f=path.join(ROOT,'artifacts/katalog-kabul-635/screens',g.slug+'-'+g.id+'-'+n+'.png');composite.push({input:await sharp(f).resize(195,422,{fit:'contain',background:'#eee'}).toBuffer(),left:x+(n-1)*200,top:y+32})}
  }
  const name='sheet-'+String(offset/6+1).padStart(3,'0')+'.jpg';
  await sharp({create:{width:1200,height:Math.ceil(batch.length/2)*460,channels:3,background:'#d9e5e8'}}).composite(composite).jpeg({quality:85}).toFile(path.join(OUT,name));
  sheets.push({file:name,ids:batch.map(g=>g.id)});
 }
 fs.writeFileSync(path.join(OUT,'sheets.json'),JSON.stringify(sheets,null,2));
 console.log(JSON.stringify({games:definitions.length,sheets:sheets.length,external:ledger.filter(g=>g.signals.externalTargets).map(g=>g.id)}));
}
main().catch(e=>{console.error(e);process.exitCode=1});
