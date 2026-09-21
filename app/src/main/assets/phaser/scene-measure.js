/* Ölçme sahneleri: çizimler temsili ölçektedir, fiziksel ekran santimetresi değildir. */
window.SceneMeasure=(()=>{
 const esc=SceneWorkshop.escape;
 const fractions=[[[2,4,1,2],[2,8,1,4],[4,6,2,3]],[[2,6,1,3],[6,8,3,4],[3,9,1,3]],[[6,10,3,5],[4,8,1,2],[9,12,3,4]]];
 const lengths=[[{n:1,max:5,unit:'cm',end:10,to:'mm',factor:10},{n:5,max:5,unit:'cm',end:50,to:'mm',factor:10},{n:3,max:5,unit:'cm',end:30,to:'mm',factor:10}],
  [{n:1,max:2,unit:'m',end:100,to:'cm',factor:100},{n:1,max:3,unit:'km',end:1000,to:'m',factor:1000},{n:2,max:2,unit:'m',end:200,to:'cm',factor:100},{n:3,max:3,unit:'km',end:3000,to:'m',factor:1000}]];
 const svg=(body,view='0 0 240 95')=>`<svg viewBox="${view}" aria-hidden="true" focusable="false">${body}</svg>`;
 function strip(n,d,color,y=0){return `<rect x="16" y="${y}" width="208" height="23" rx="2" fill="#fcf6df" stroke="#435d68"/><rect x="16" y="${y}" width="${208*n/d}" height="23" fill="${color}"/>${Array.from({length:d+1},(_,i)=>`<path d="M${16+208*i/d} ${y}v23" stroke="#435d68" stroke-width="1"/>`).join('')}`}
 function fractionSource(pair){return `<b>${pair[0]} / ${pair[1]}</b>${svg(strip(pair[0],pair[1],'#539cad',10),'0 0 240 45')}`}
 function fractionDock(pair,done,fresh,round){const[a,b,c,d]=pair;
  const op=round===2?`÷${a/c}`:`×${a/c}`;
  return `<div class="fraction-machine ${fresh?'fraction-settle':''}"><div class="fraction-label"><b>${c} / ${d}</b><small>${round===1?op:'Aynı bütün'}</small></div>${svg(`<path d="M16 3v88" stroke="#cc7055" stroke-width="2" stroke-dasharray="3 3"/>${strip(c,d,'#e8b253',8)}<text x="224" y="46" font-size="10" text-anchor="end" fill="#37535e">referans</text>${done?`<g class="fraction-insert">${strip(a,b,'#539cad',57)}</g><path d="M${16+208*c/d} 8v72" stroke="#358771" stroke-width="2" stroke-dasharray="4 3"/>`:'<rect x="16" y="57" width="208" height="23" fill="#ffffff66" stroke="#698e95" stroke-dasharray="4 4"/>'}`)}<div class="measure-result">${done?`${round===2?`${a}/${b} → ${c}/${d}`:`${c}/${d} → ${a}/${b}`} · pay ve payda ${op}`:'Şeridi alt yuvaya bırak'}</div></div>`;
 }
 function ruler(item,done,fresh){const W=208,segments=item.unit==='cm'?50:item.unit==='m'?20:30;
  return `<div class="ruler-instrument ${fresh?'ruler-loaded':''}"><header>${item.end} ${item.to}<small>${item.unit==='km'?'Yol ölçüm planı':'Cetvel tezgâhı'}</small></header>${svg(`<rect x="16" y="43" width="208" height="35" rx="3" fill="#f5d484" stroke="#9d773a"/>${Array.from({length:segments+1},(_,i)=>`<path d="M${16+W*i/segments} 43v${i%5===0?18:8}" stroke="#6f5635"/>`).join('')}<text x="16" y="91" font-size="10">0</text><text x="224" y="91" text-anchor="end" font-size="10">${item.max*item.factor} ${item.to}</text><path d="M${16+W*item.n/item.max} 9v73" stroke="#cc7055" stroke-width="2" stroke-dasharray="3 3"/>${done?`<g class="measured-bar"><rect x="16" y="14" width="${W*item.n/item.max}" height="23" rx="3" fill="#4c9baa"/><text x="${16+W*item.n/item.max/2}" y="30" text-anchor="middle" font-size="11" fill="white">${item.n} ${item.unit}</text></g>`:`<rect x="16" y="14" width="${W*item.n/item.max}" height="23" rx="3" fill="#dde9e366" stroke="#618792" stroke-dasharray="4 3"/>`}`)}<div class="measure-result">${done?`${item.n} ${item.unit} = ${item.end} ${item.to} · sayı ×${item.factor}`:'Çubuğu 0 çizgisine hizala'}</div></div>`;
 }
 function lengthSource(item){return `<b>${item.n} ${item.unit}</b>${svg(`<rect x="16" y="8" width="${208*item.n/item.max}" height="23" rx="3" fill="#4c9baa"/><path d="M16 36h208" stroke="#a7b7b8" stroke-dasharray="3 3"/>`,'0 0 240 45')}`}
 const angles=[90,35,140,180,360],names=['Duvar–zemin','Az açılmış makas','Çok açılmış kitap','Dümdüz yol','Tam dönüş'];
 function object(index){
  const d=angles[index],x=50+75*Math.cos(d*Math.PI/180),y=100-75*Math.sin(d*Math.PI/180);
  const guides=`<path d="M50 100h75M50 100L${x} ${y}" fill="none" stroke="#eea936" stroke-width="3" stroke-dasharray="4 3"/>`;
  let body='';
  if(index===0)body='<path d="M50 25v75h80" fill="none" stroke="#a2795c" stroke-width="15"/><path d="M43 48h14m-14 22h14m26 24v13m24-13v13" stroke="#eadac7" stroke-width="3"/>';
  if(index===1)body=`<path d="M50 100h76M50 100L${x} ${y}" stroke="#7c929c" stroke-width="9" stroke-linecap="round"/><path d="M50 100l-23 16m23-16l-23-13" stroke="#486b79" stroke-width="7"/><ellipse cx="17" cy="121" rx="12" ry="9" fill="none" stroke="#d9655d" stroke-width="6"/><ellipse cx="17" cy="83" rx="12" ry="9" fill="none" stroke="#d9655d" stroke-width="6"/><circle cx="50" cy="100" r="5" fill="#eed9a3"/>`;
  if(index===2)body=`<path d="M50 100L${x} ${y}l-8-10L48 82l79-3v21z" fill="#fff4d5" stroke="#766390" stroke-width="5"/><path d="M50 100V83" stroke="#9479aa" stroke-width="3"/>`;
  if(index===3)body='<path d="M-26 100h151" stroke="#647a81" stroke-width="20"/><path d="M-26 100h151" stroke="#ffe4a1" stroke-width="2" stroke-dasharray="9 7"/>';
  if(index===4)body='<circle cx="50" cy="100" r="60" fill="none" stroke="#4c8f9a" stroke-width="6"/><path d="M50 100h60" stroke="#dc8652" stroke-width="6"/><path d="M95 48l14 9 2-18" fill="none" stroke="#4c8f9a" stroke-width="6"/>';
  return svg(body+(index<4?guides:''),'-40 0 190 190');
 }
 function angleDock(index,done,fresh){const d=angles[index],R=75,cx=50,cy=100;
  return `<div class="angle-instrument ${fresh?'angle-loaded':''}"><header>${['DİK AÇI','DAR AÇI','GENİŞ AÇI','DOĞRU AÇI','TAM AÇI'][index]}<small>${d}°</small></header><div class="angle-overlay">${svg(`<circle cx="50" cy="100" r="76" fill="#f7faf7" stroke="#99afb7" stroke-width="2"/>${Array.from({length:24},(_,i)=>{const a=i*Math.PI/12;return `<path d="M${cx+70*Math.cos(a)} ${cy+70*Math.sin(a)}L${cx+76*Math.cos(a)} ${cy+76*Math.sin(a)}" stroke="#6c8b96"/>`}).join('')}<path d="M${cx} ${cy}h${R}" stroke="#637f8b" stroke-width="4"/><g class="angle-sweep" style="transform-origin:${cx}px ${cy}px;--sweep:${-d}deg"><path d="M${cx} ${cy}h${R}" stroke="#d2863e" stroke-width="4"/></g><circle cx="50" cy="100" r="4" fill="#345c70"/>`,'-40 0 190 190')}${done?`<span class="docked-object">${object(index)}</span>`:''}</div><div class="measure-result">${done?names[index]:'Nesneyi açı modeline bırak'}</div></div>`;
 }
 function render({id,r,index,state,finish,wrong}){
  state.placed={};state.done=0;state.measureMatches={};
  const kind=id==='p11'?'fraction':id==='p16'?'ruler':'angle',scene=document.querySelector('.scene'),stage=document.querySelector('#stage'),task=document.querySelector('#task');
  scene.classList.add('measure-scene',`measure-${kind}`);
  const draw=()=>{
   stage.innerHTML=`<div class="measure-bench"><h2>${kind==='fraction'?'DENK KESİR TEZGÂHI':kind==='ruler'?'BİRİM ÖLÇÜM ATÖLYESİ':'NESNELERİN AÇILARI'}</h2><p>${kind==='fraction'?'Bütünler eşit boyda. Boyalı uçlar aynı çizgide mi?':kind==='ruler'?'Çubukların başlangıcı 0, bitişi kırmızı çizgi.':'Nesnedeki iki kolu modelin kollarıyla karşılaştır.'}</p><div class="measure-docks">${r.targets.map((t,i)=>{
    const done=!!state.measureMatches[t.id],fresh=state.measureFresh===t.id;
    return `<button class="measure-dock" data-target="${t.id}" aria-label="${esc(t.html.replace(/<[^>]*>/g,' '))}">${kind==='fraction'?fractionDock(fractions[index][i],done,fresh,index):kind==='ruler'?ruler(lengths[index][i],done,fresh):angleDock(index===2?i+3:i,done,fresh)}</button>`;
   }).join('')}</div><small class="measure-foot">${kind==='fraction'?'Tur '+(index+1)+' · '+state.done+'/'+r.pieces.length+' şerit':kind==='ruler'?'Çizimler temsili ölçektedir; ekran üzerindeki gerçek cm değildir.':'Tur '+(index+1)+' · '+state.done+'/'+r.pieces.length+' nesne'}</small></div>`;
   const order=r.pieces.length===4?[2,0,3,1]:r.pieces.length===3?[2,0,1]:[1,0];
   task.innerHTML=`<div class="measure-sources">${order.map(i=>{const p=r.pieces[i],done=!!state.measureMatches[p.target];return `<button class="measure-source" data-piece="${p.id}" ${done?'disabled':''}>${kind==='fraction'?fractionSource(fractions[index][i]):kind==='ruler'?lengthSource(lengths[index][i]):object(index===2?i+3:i)+`<b>${names[index===2?i+3:i]}</b>`}</button>`}).join('')}</div><p class="measure-help">Sürükle veya parçaya, sonra sahnedeki yuvasına dokun.</p>`;
   task.querySelectorAll('[data-piece]').forEach(b=>b.onclick=()=>{state.tapPiece=b.dataset.piece;task.querySelectorAll('[data-piece]').forEach(x=>x.classList.toggle('selected',x===b))});
   stage.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>{if(state.tapPiece)place(state.tapPiece,b.dataset.target)});
   SceneWorkshop.bindDrag('[data-piece]:not(:disabled)','[data-target]',(a,b)=>place(a.dataset.piece,b.dataset.target));state.measureFresh=null;
  };
  const place=(pid,tid)=>{const p=r.pieces.find(x=>x.id===pid);if(state.measureComplete||!p||state.measureMatches[p.target])return;if(p.target!==tid)return wrong(r.hint);
   state.measureMatches[tid]=pid;state.placed[tid]=1;state.done++;state.tapPiece=null;state.measureFresh=tid;draw();
   if(state.done===r.pieces.length){state.measureComplete=true;finish(r)}
  };draw();
 }
 return {render,object};
})();
