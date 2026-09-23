/* Cümleyle kurulan köprü ve gözlemlenebilen hareket yolları. */
window.SceneBridgesMotion=(()=>{
 const esc=SceneWorkshop.escape;
 const plain=s=>String(s).replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim();
 function bridge({r,state,wrong,finish,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('bridge-scene');
  state.bridgePlaced={};state.placed={};state.done=0;
  const draw=()=>{
   stage.innerHTML='<div class="bridge-world"><header>EŞ ANLAM KÖPRÜSÜ <small>Cümleyi doğru sözcükle karşı kıyıya geçir</small></header><div class="bridge-river"><span class="bridge-bank bank-left" aria-hidden="true"></span><span class="bridge-bank bank-right" aria-hidden="true"></span><div class="bridge-spans">'+r.targets.map((t,i)=>{
    const p=r.pieces.find(x=>x.id===state.bridgePlaced[t.id]);
    return '<button class="bridge-span '+(p?'bridge-complete ':'')+(state.bridgeFresh===t.id?'bridge-build':'')+'" data-target="'+t.id+'" aria-label="'+esc(plain(t.html))+' sözcüğünün köprü boşluğu"><span class="bridge-step">'+(p?p.html:'<span class="bridge-gap">Cümleyi buraya bırak</span>')+'</span><strong>'+t.html+'</strong><i class="bridge-bolt" aria-hidden="true"></i></button>';
   }).join('')+'</div></div><p class="bridge-counter" role="status">'+state.done+' / '+r.pieces.length+' köprü geçidi kuruldu</p></div>';
   task.innerHTML='<div class="bridge-sources">'+[2,0,3,1].map(i=>r.pieces[i]).map(p=>'<button class="bridge-source" data-piece="'+p.id+'" '+(state.bridgePlaced[p.target]?'disabled':'')+'>'+p.html+'</button>').join('')+'</div><p class="bridge-help">Cümleyi doğru sözcüğün köprü boşluğuna sürükle veya seçip dokun.</p>';
   task.querySelectorAll('[data-piece]').forEach(b=>b.onclick=()=>{state.bridgeSelected=b.dataset.piece;task.querySelectorAll('[data-piece]').forEach(x=>x.classList.toggle('selected',x===b))});
   stage.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>{if(state.bridgeSelected)place(state.bridgeSelected,b.dataset.target)});
   SceneWorkshop.bindDrag('[data-piece]:not(:disabled)','[data-target]',(a,b)=>place(a.dataset.piece,b.dataset.target));state.bridgeFresh=null;
  };
  const place=(pid,tid)=>{const p=r.pieces.find(x=>x.id===pid);
   if(locked()||state.bridgeComplete||!p||state.bridgePlaced[p.target])return;
   if(p.target!==tid)return wrong(r.hint);
   state.bridgePlaced[tid]=pid;state.placed[tid]=1;state.done++;state.bridgeSelected=null;state.bridgeFresh=tid;draw();
   if(state.done===r.pieces.length){state.bridgeComplete=true;finish(r)}
  };draw();
 }
 function object(label){
  const s=label.toLocaleLowerCase('tr');const svg=x=>'<svg viewBox="0 0 80 80" aria-hidden="true" focusable="false">'+x+'</svg>';
  if(/tekerlek|bisiklet/.test(s))return svg('<circle cx="40" cy="42" r="28" fill="#e4e9dd" stroke="#405c68" stroke-width="7"/><circle cx="40" cy="42" r="7" fill="#4c7184"/><path d="M40 14v56M12 42h56M20 22l40 40m0-40L20 62" stroke="#7694a2" stroke-width="3"/>');
  if(/salıncak/.test(s))return svg('<path d="M21 69L32 13h19l10 56M31 14h20" fill="none" stroke="#6b8b87" stroke-width="5"/><path d="M38 22l-5 34m13-34l5 34M27 57h31" stroke="#c58654" stroke-width="5"/>');
  if(/top|topaç/.test(s))return svg('<circle cx="40" cy="42" r="27" fill="#dd835b" stroke="#a7513a" stroke-width="4"/><path d="M18 30q23 4 44 24M30 17q23 22 14 51" fill="none" stroke="#f6c492" stroke-width="4"/>');
  if(/tambur|vantilatör/.test(s))return svg('<circle cx="40" cy="42" r="29" fill="#d6e7e9" stroke="#507b89" stroke-width="5"/><path d="M40 39Q15 8 15 34q4 14 22 12M41 40Q76 22 63 51q-8 10-22-6M40 40Q16 73 46 65q10-4-1-22" fill="#5a9bab"/><circle cx="40" cy="42" r="6" fill="#345c71"/>');
  if(/sarkaç/.test(s))return svg('<path d="M40 12v37" stroke="#7d715e" stroke-width="5"/><circle cx="40" cy="55" r="14" fill="#d3af5f" stroke="#896b36" stroke-width="3"/><path d="M17 14h46" stroke="#7d715e" stroke-width="6"/>');
  if(/araba|tren/.test(s))return svg('<path d="M11 37h58v22H11z" fill="#d8745e" stroke="#8d4c3c" stroke-width="3"/><path d="M22 22h34l9 15H15z" fill="#a9d5db" stroke="#527b89" stroke-width="3"/><circle cx="25" cy="61" r="7" fill="#344d5a"/><circle cx="56" cy="61" r="7" fill="#344d5a"/>');
  if(/bayrak/.test(s))return svg('<path d="M22 12v60" stroke="#715944" stroke-width="6"/><path d="M25 15q17-9 37 0v28q-19-8-37 0z" fill="#d65e5f" stroke="#a14d4b" stroke-width="3"/>');
  if(/çocuk/.test(s))return svg('<circle cx="40" cy="19" r="9" fill="#d9a977"/><path d="M29 30h22l6 21H23z" fill="#6e9abb"/><path d="M33 51l-8 20m22-20l8 20" stroke="#45627a" stroke-width="7"/>');
  return svg('<circle cx="40" cy="40" r="26" fill="#e4ae5e" stroke="#8c6745" stroke-width="4"/>');
 }
 const modes=[['rotate','sway','turn'],['rotate','roll','slide']];
 function motion({r,index,state,wrong,finish,next,fast,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('motion-scene');
  state.motionLanes=state.motionLanes||r.kutular.map(()=>[]);
  const i=state.ix||0,k=r.kartlar[i];if(!k)return;
  const mode=modes[index][k.dogru];
  const draw=()=>{
   stage.innerHTML='<div class="motion-world"><header>HAREKET PARKI <small>Nesneyi izle, sonra uygun hareket yoluna taşı</small></header><div class="motion-observe"><button class="motion-object" data-sinif-kart="1" aria-label="'+esc(k.t)+'">'+object(k.t)+'</button><div class="motion-observe-text"><strong>'+esc(k.t)+'</strong><button class="motion-watch" type="button">▶ Hareketi izle</button></div></div><div class="motion-lanes">'+r.kutular.map((b,j)=>{
    const name=typeof b==='string'?b:b.ad,alt=typeof b==='string'?'':b.alt,items=state.motionLanes[j];
    return '<button class="motion-lane motion-lane-'+j+' '+(state.motionFresh===j?'motion-lane-fresh':'')+'" data-kutu="'+j+'" aria-label="'+esc(name)+' hareket yolu"><span class="motion-route route-'+modes[index][j]+'" aria-hidden="true"></span><span class="motion-lane-copy"><strong>'+esc(name)+'</strong><small>'+esc(alt)+'</small></span><span class="motion-objects">'+items.map((x,n)=>'<span class="motion-mini '+(state.motionFresh===j&&n===items.length-1?'motion-lane-arrive':'')+'" title="'+esc(x)+'">'+object(x)+'</span>').join('')+'</span></button>';
   }).join('')+'</div><p class="motion-feedback" role="status">'+esc(state.not||'Önce hareketi gözlemle.')+'</p></div>';
   task.innerHTML='<p class="motion-help">'+(i+1)+' / '+r.kartlar.length+' gözlem · Nesneyi sahnedeki hareket yoluna sürükle veya seçip dokun.</p>';
   const source=stage.querySelector('[data-sinif-kart]');source.onclick=()=>{state.motionSelected=!state.motionSelected;source.classList.toggle('selected',state.motionSelected)};
   stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>{if(state.motionSelected)place(+b.dataset.kutu)});
   stage.querySelector('.motion-watch').onclick=()=>{const el=source.querySelector('svg');el.classList.remove('watch-'+mode);void el.offsetWidth;el.classList.add('watch-'+mode)};
   SceneWorkshop.bindDrag('[data-sinif-kart]','[data-kutu]',(_,b)=>place(+b.dataset.kutu));state.motionFresh=null;
  };
  const place=j=>{
   if(locked()||state.gecis||state.motionComplete)return;
   if(j!==k.dogru)return wrong(k.hint||r.ipucu);
   state.motionLanes[j].push(k.t);state.sayim[j]++;state.ix=i+1;state.not=k.neden||'';state.motionFresh=j;state.motionSelected=false;
   draw();stage.querySelector('[data-sinif-kart]').disabled=true;
   next(()=>{if(state.ix>=r.kartlar.length){state.motionComplete=true;finish()}else motion({r,index,state,wrong,finish,next,fast,locked})},fast?30:850);
  };draw();
 }
 return {bridge,motion};
})();
