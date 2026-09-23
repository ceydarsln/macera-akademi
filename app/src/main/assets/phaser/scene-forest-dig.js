/* Sözcük kovukları ve kazı katmanları: iki oyuna özgü sahne davranışı. */
window.SceneForestDig=(()=>{
 const esc=SceneWorkshop.escape;
 const plain=s=>String(s).replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim();
 function forest({r,state,wrong,finish,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('forest-scene');
  state.forestPlaced={};state.placed={};state.done=0;
  const draw=()=>{
   stage.innerHTML='<div class="forest-world"><header>EŞ ANLAM ORMANI <small>Her kovuktaki sözcüğün eşini bul</small></header><div class="forest-grove">'+r.targets.map((t,i)=>{
    const p=r.pieces.find(p=>p.id===state.forestPlaced[t.id]);
    return '<div class="forest-tree forest-tree-'+i+'"><div class="forest-crown" aria-hidden="true"><i></i><i></i><i></i></div><button class="forest-hollow '+(p?'forest-filled ':'')+(state.forestFresh===t.id?'forest-grow':'')+'" data-target="'+t.id+'" aria-label="'+esc(plain(t.html))+' sözcüğünün kovuğu"><span class="forest-word">'+t.html+'</span>'+(p?'<span class="forest-pair">'+p.html+'</span>':'<span class="forest-empty">Eşini buraya bırak</span>')+'</button><div class="forest-roots" aria-hidden="true"></div></div>';
   }).join('')+'</div><p class="forest-counter" role="status">'+state.done+' / '+r.pieces.length+' sözcük çifti bulundu</p></div>';
   task.innerHTML='<div class="forest-sources">'+[2,0,3,1].map(i=>r.pieces[i]).map(p=>'<button class="forest-source" data-piece="'+p.id+'" '+(state.forestPlaced[p.target]?'disabled':'')+'>'+p.html+'</button>').join('')+'</div><p class="forest-help">Sözcüğü ağaç kovuğuna sürükle veya seçip kovuğa dokun.<span class="forest-scroll-hint"> Diğer kartlar için yana kaydır.</span></p>';
   task.querySelectorAll('[data-piece]').forEach(b=>b.onclick=()=>{state.forestSelected=b.dataset.piece;task.querySelectorAll('[data-piece]').forEach(x=>x.classList.toggle('selected',x===b))});
   stage.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>{if(state.forestSelected)place(state.forestSelected,b.dataset.target)});
   SceneWorkshop.bindDrag('[data-piece]:not(:disabled)','[data-target]',(a,b)=>place(a.dataset.piece,b.dataset.target));
   state.forestFresh=null;
  };
  const place=(pid,tid)=>{
   const p=r.pieces.find(x=>x.id===pid);if(locked()||state.forestComplete||!p||state.forestPlaced[p.target])return;
   if(p.target!==tid)return wrong(r.hint);
   state.forestPlaced[tid]=pid;state.placed[tid]=1;state.done++;state.forestSelected=null;state.forestFresh=tid;draw();
   if(state.done===r.pieces.length){state.forestComplete=true;finish(r)}
  };draw();
 }
 function toolIcon(label){
  const t=label.toLocaleLowerCase('tr');
  const svg=s=>'<svg viewBox="0 0 80 80" aria-hidden="true" focusable="false">'+s+'</svg>';
  if(t.includes('kürek'))return svg('<path d="M39 12v43" stroke="#89623d" stroke-width="8" stroke-linecap="round"/><path d="M26 48h28l-5 22H31z" fill="#b6c5c4" stroke="#597378" stroke-width="3"/><path d="M27 13h25" stroke="#89623d" stroke-width="7"/>');
  if(t.includes('fırça'))return svg('<path d="M40 14v38" stroke="#b9834b" stroke-width="8" stroke-linecap="round"/><path d="M25 48h30l-4 12H29z" fill="#8299a5"/><path d="M29 60h22l-3 11H32z" fill="#e7c68b" stroke="#ae8a54" stroke-width="2"/>');
  if(t.includes('kazma'))return svg('<path d="M42 19v53" stroke="#946739" stroke-width="8" stroke-linecap="round"/><path d="M14 26q25-25 52 0l-4 9Q40 20 19 35z" fill="#a9b7b5" stroke="#526e74" stroke-width="3"/>');
  if(t.includes('kazıyıcı'))return svg('<path d="M47 11L32 58" stroke="#aa7549" stroke-width="8" stroke-linecap="round"/><path d="M25 59l15-6-7 18-12-3z" fill="#aab9b9" stroke="#4c6e70" stroke-width="3"/>');
  if(t.includes('elek'))return svg('<ellipse cx="40" cy="43" rx="29" ry="20" fill="#e8d7b1" stroke="#806c4f" stroke-width="5"/><path d="M18 36h44M18 45h44M24 53h32M30 25v37m10-38v39m10-38v37" stroke="#a79b79" stroke-width="2"/>');
  return svg('<path d="M13 29h48l-8 27H22z" fill="#9eb7b6" stroke="#526f73" stroke-width="4"/><path d="M15 26h51" stroke="#725842" stroke-width="5"/><circle cx="26" cy="64" r="7" fill="#465961"/><circle cx="53" cy="64" r="7" fill="#465961"/>');
 }
 function dig({r,state,wrong,finish,next,fast,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('dig-scene');
  state.digZones=state.digZones||r.kutular.map(()=>[]);
  const i=state.ix||0,k=r.kartlar[i];if(!k)return;
  const draw=()=>{
   stage.innerHTML='<div class="dig-world"><header>KAZI ALANI <small>Fosilden uzak ve yakın iki çalışma bölgesi</small></header><div class="dig-board">'+r.kutular.map((b,j)=>{
    const items=state.digZones[j],name=typeof b==='string'?b:b.ad,alt=typeof b==='string'?'':b.alt;
    return '<button class="dig-zone dig-zone-'+j+' '+(items.length?'dig-used ':'')+(state.digFresh===j?'dig-activity':'')+'" data-kutu="'+j+'" aria-label="'+esc(name)+' çalışma bölgesi"><span class="dig-ground" aria-hidden="true"></span><span class="dig-fossil" aria-hidden="true"></span><strong>'+esc(name)+'</strong><small>'+esc(alt)+'</small><span class="dig-worksite">'+items.map((x,n)=>'<span class="dig-tool '+(state.digFresh===j&&n===items.length-1?'dig-tool-arrive':'')+'" title="'+esc(x)+'">'+toolIcon(x)+'</span>').join('')+'</span><span class="dig-count">'+items.length+' alet</span></button>';
   }).join('')+'</div><p class="dig-feedback" role="status">'+esc(state.not||'Aleti işe uygun toprak bölgesine bırak.')+'</p></div>';
   task.innerHTML='<button class="dig-source" data-sinif-kart="1" aria-label="'+esc(k.t)+'">'+toolIcon(k.t)+'<span>'+esc(k.t)+'</span></button><p class="dig-help">'+(i+1)+' / '+r.kartlar.length+' alet · Sahnedeki uygun bölgeye sürükle veya seçip dokun.</p>';
   const source=task.querySelector('[data-sinif-kart]');source.onclick=()=>{state.digSelected=!state.digSelected;source.classList.toggle('selected',state.digSelected)};
   stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>{if(state.digSelected)place(+b.dataset.kutu)});
   SceneWorkshop.bindDrag('[data-sinif-kart]','[data-kutu]',(_,b)=>place(+b.dataset.kutu));
   state.digFresh=null;
  };
  const place=j=>{
   if(locked()||state.gecis||state.digComplete)return;
   if(j!==k.dogru)return wrong(k.hint||r.ipucu);
   state.digZones[j].push(k.t);state.sayim[j]++;state.ix=i+1;state.not=k.neden||'';state.digFresh=j;state.digSelected=false;
   draw();task.querySelector('[data-sinif-kart]').disabled=true;
   next(()=>{if(state.ix>=r.kartlar.length){state.digComplete=true;finish()}else dig({r,state,wrong,finish,next,fast,locked})},fast?30:850);
  };draw();
 }
 return {forest,dig};
})();
