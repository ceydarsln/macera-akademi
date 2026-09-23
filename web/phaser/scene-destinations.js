/* Şematik harita ve gerçek atık kutuları; iki ayrı oyun davranışı. */
window.SceneDestinations=(()=>{
 const esc=SceneWorkshop.escape;
 const strip=s=>String(s).replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim();
 const positions=[
  [{x:11,y:26},{x:13,y:68},{x:52,y:50},{x:78,y:29}],
  [{x:14,y:15},{x:22,y:39},{x:34,y:62},{x:74,y:72}]
 ];
 const cityNames=[['Edirne','İzmir','Ankara','Trabzon'],['İstanbul · cami','İstanbul · saray','Bursa','Şanlıurfa']];
 function map({r,index,state,wrong,finish,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('destination-scene','destination-map');
  state.mapPlaced={};state.done=0;state.placed={};
  const draw=()=>{
   stage.innerHTML='<div class="map-workspace"><header>ESER HARİTASI <small>Şematik Türkiye yerleşimi · Tur '+(index+1)+'/3</small></header><div class="map-board"><svg viewBox="0 0 600 330" preserveAspectRatio="none" aria-hidden="true"><path d="M30 84L89 51L173 69L225 42L296 72L342 48L405 68L480 59L562 91L540 127L577 154L526 182L506 239L425 251L394 284L327 259L267 281L208 247L136 257L81 218L50 166L18 141Z" fill="#d9cbaa" stroke="#7d8f78" stroke-width="5"/><path d="M116 122q110 94 202 94t205-49" fill="none" stroke="#a8bb9e" stroke-width="4" stroke-dasharray="6 8"/><path d="M70 57q65-27 103-7M394 28q104-14 169 40" fill="none" stroke="#9bbfd0" stroke-width="10" opacity=".65"/></svg>'+r.targets.map((t,i)=>{
    const p=r.pieces.find(p=>p.id===state.mapPlaced[t.id]),pos=positions[index][i];
    return '<button class="map-pin map-pin-'+i+' '+(state.mapFresh===t.id?'map-arrival':'')+'" data-target="'+t.id+'" style="--x:'+pos.x+'%;--y:'+pos.y+'%" aria-label="'+esc(cityNames[index][i])+'"><span class="map-pin-dot" aria-hidden="true"></span><strong>'+esc(cityNames[index][i])+'</strong>'+(p?'<span class="map-artifact">'+esc(strip(p.html.split(/<br\s*\/?\s*>/i)[0]))+'</span>':'<span class="map-open">Eseri buraya bırak</span>')+'</button>';
   }).join('')+'</div><p class="map-note" role="status">'+state.done+' / '+r.pieces.length+' eser yerleşti'+(index===1?' · İstanbul’da iki farklı yapı var':'')+'</p></div>';
   task.innerHTML='<div class="map-sources">'+[2,0,3,1].map(i=>r.pieces[i]).map(p=>'<button class="map-source" data-piece="'+p.id+'" '+(state.mapPlaced[p.target]?'disabled':'')+'>'+p.html+'</button>').join('')+'</div><p class="map-help">Eseri şehir işaretine sürükle veya seçip işarete dokun.<span class="map-scroll-hint"> Diğer kartlar için yana kaydır.</span></p>';
   task.querySelectorAll('[data-piece]').forEach(b=>b.onclick=()=>{state.mapSelected=b.dataset.piece;task.querySelectorAll('[data-piece]').forEach(x=>x.classList.toggle('selected',x===b))});
   stage.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>{if(state.mapSelected)place(state.mapSelected,b.dataset.target)});
   SceneWorkshop.bindDrag('[data-piece]:not(:disabled)','[data-target]',(a,b)=>place(a.dataset.piece,b.dataset.target));
   state.mapFresh=null;
  };
  const place=(pid,tid)=>{
   const p=r.pieces.find(p=>p.id===pid);if(locked()||state.mapComplete||!p||state.mapPlaced[p.target])return;
   if(p.target!==tid)return wrong(r.hint);
   state.mapPlaced[tid]=pid;state.placed[tid]=1;state.done++;state.mapSelected=null;state.mapFresh=tid;draw();
   if(state.done===r.pieces.length){state.mapComplete=true;finish(r)}
  };draw();
 }
 const icon=(name)=>{
  const t=name.toLocaleLowerCase('tr'),svg=b=>'<svg viewBox="0 0 80 80" aria-hidden="true" focusable="false">'+b+'</svg>';
  if(/kavanoz/.test(t))return svg('<path d="M20 17h40l-4 52H24z" fill="#bde1e7" fill-opacity=".7" stroke="#577e86" stroke-width="3"/><path d="M19 15h42" stroke="#ba5e4d" stroke-width="8"/><path d="M31 30v24" stroke="white" stroke-width="4"/>');
  if(/muz/.test(t))return svg('<path d="M14 22q4 48 51 43Q39 76 24 54q-9-14-10-32" fill="#e8c659" stroke="#ad8a37" stroke-width="3"/><path d="M14 22l-2-8m53 51l4 5" stroke="#604737" stroke-width="5"/>');
  if(/gazete/.test(t))return svg('<rect x="10" y="14" width="60" height="54" fill="#f9f4e4" stroke="#627d88" stroke-width="3"/><path d="M17 24h45M17 31h45M17 39h17v20H17zm24 1h22m-22 8h22m-22 8h22" fill="none" stroke="#8da8ae" stroke-width="3"/>');
  if(/şişe/.test(t))return svg('<path d="M31 12h18v11l6 8v38H25V31l6-8z" fill="#91d0dc" fill-opacity=".8" stroke="#46879b" stroke-width="3"/><path d="M28 45h24" stroke="#d9f0ee" stroke-width="8"/><path d="M29 10h22" stroke="#3f8ca2" stroke-width="6"/>');
  if(/yumurta kabuğu/.test(t))return svg('<path d="M12 46l10-14 10 7 11-14 11 11 12-3 8 13q-11 25-32 25T12 46" fill="#f8efd7" stroke="#ae9c7d" stroke-width="3"/>');
  if(/viyol/.test(t))return svg('<path d="M8 32l14-14h43l8 14v30H8z" fill="#cbb78c" stroke="#897454" stroke-width="3"/><path d="M9 39h64M22 20l7 20m19-20l-1 20m18-20l-6 20" stroke="#897454" stroke-width="3"/><circle cx="22" cy="50" r="5" fill="#e8dac1"/><circle cx="43" cy="50" r="5" fill="#e8dac1"/><circle cx="62" cy="50" r="5" fill="#e8dac1"/>');
  if(/bardak/.test(t))return svg('<path d="M18 19h45l-7 48H25z" fill="#b9e0e8" fill-opacity=".65" stroke="#608f9c" stroke-width="3"/><path d="M37 23l-5 17 12 5-5 22m5-22l12-12" fill="none" stroke="white" stroke-width="3"/>');
  return svg('<path d="M18 12h44l-5 57H23z" fill="#b6cee4" stroke="#5d88a4" stroke-width="3"/><path d="M23 18h34" stroke="#f9f8e9" stroke-width="5"/><path d="M30 36h20v17H30z" fill="#f4ead5"/>');
 };
 function recycle({r,state,wrong,finish,next,fast,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('destination-scene','destination-recycle');
  state.recycleBins=state.recycleBins||r.kutular.map(()=>[]);
  const i=state.ix||0,k=r.kartlar[i];if(!k)return;
  const draw=()=>{
   stage.innerHTML='<div class="recycle-yard"><header>AYRIŞTIRMA PARKI <small>Atığı gerçek kutunun içine bırak</small></header><div class="recycle-bins">'+r.kutular.map((b,j)=>{
    const name=typeof b==='string'?b:b.ad,items=state.recycleBins[j];
    return '<button class="recycle-bin recycle-bin-'+j+'" data-kutu="'+j+'" aria-label="'+esc(name)+' atık kutusu"><span class="recycle-lid" aria-hidden="true"></span><strong>'+esc(name)+'</strong><span class="recycle-mouth"><span class="recycle-contents">'+items.map((x,n)=>'<span class="recycled-object '+(state.recycleFresh===j&&n===items.length-1?'recycle-fall':'')+'" title="'+esc(x)+'">'+icon(x)+'</span>').join('')+'</span></span><span class="recycle-counter">'+items.length+' atık</span></button>';
   }).join('')+'</div><p class="recycle-result" role="status">'+esc(state.not||'Nesnenin yapıldığı maddeyi incele.')+'</p></div>';
   task.innerHTML='<button class="recycle-source" data-sinif-kart="1" aria-label="'+esc(k.t)+'">'+icon(k.t)+'<span>'+esc(k.t)+'</span></button><p class="recycle-help">'+(i+1)+' / '+r.kartlar.length+' atık · Kutunun içine sürükle. İstersen nesneyi seçip kutuya dokun.</p>';
   const source=task.querySelector('[data-sinif-kart]');source.onclick=()=>{state.recycleSelected=!state.recycleSelected;source.classList.toggle('selected',state.recycleSelected)};
   stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>{if(state.recycleSelected)place(+b.dataset.kutu)});
   SceneWorkshop.bindDrag('[data-sinif-kart]','[data-kutu]',(_,b)=>place(+b.dataset.kutu));
   state.recycleFresh=null;
  };
  const place=j=>{
   if(locked()||state.gecis||state.recycleComplete)return;
   if(j!==k.dogru)return wrong(k.hint||r.ipucu);
   state.recycleBins[j].push(k.t);state.sayim[j]++;state.ix=i+1;state.not=k.neden||'';state.recycleFresh=j;state.recycleSelected=false;
   draw();task.querySelector('[data-sinif-kart]').disabled=true;
   next(()=>{if(state.ix>=r.kartlar.length){state.recycleComplete=true;finish()}else recycle({r,state,wrong,finish,next,fast,locked})},fast?30:850);
  };draw();
 }
 return {map,recycle,icon};
})();
