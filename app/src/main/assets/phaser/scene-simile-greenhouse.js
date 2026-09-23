/* Benzetme makinesi ve bitki serası: kartlar sahnedeki nesnelere bırakılır. */
window.SceneSimileGreenhouse=(()=>{
 const esc=SceneWorkshop.escape;
 const plain=s=>String(s).replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim();
 function simile({r,state,wrong,finish,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('simile-scene');
  state.similePairs={};state.placed={};state.done=0;
  const draw=()=>{
   stage.innerHTML='<div class="simile-machine"><header>⚙️ BENZETME MAKİNESİ <small>Ortak özelliği bul, kartı doğru girişe bırak</small></header><div class="simile-ports">'+r.targets.map((t,i)=>{
    const p=r.pieces.find(x=>x.id===state.similePairs[t.id]);
    return '<button class="simile-port '+(p?'simile-filled ':'')+(state.simileFresh===t.id?'simile-print':'')+'" data-target="'+t.id+'" aria-label="'+esc(plain(t.html))+' benzetme girişi"><span class="simile-port-number">0'+(i+1)+'</span><span class="simile-port-slot">'+(p?'<strong>'+p.html+'</strong>':'<span class="simile-slot-arrow">↓</span><small>Kartı buraya bırak</small>')+'</span><span class="simile-port-word">'+t.html+'</span></button>';
   }).join('')+'</div><div class="simile-paper" role="status">'+(state.done?'<b>ÇIKTI · '+state.done+' / '+r.pieces.length+'</b><span>'+r.targets.filter(t=>state.similePairs[t.id]).map(t=>{const p=r.pieces.find(x=>x.id===state.similePairs[t.id]);return plain(p.html).replace(/\s+/g,' ')+' '+plain(t.html)}).join(' • ')+'</span>':'<b>ÇIKTI · 0 / '+r.pieces.length+'</b><span>Doğru eşleşmeler burada yazılacak.</span>')+'</div></div>';
   task.innerHTML='<div class="simile-card-tray">'+r.pieces.map(p=>'<button class="simile-card" data-piece="'+p.id+'" '+(state.similePairs[p.target]?'disabled':'')+'>'+p.html+'</button>').join('')+'</div><p class="simile-help">Kartı makinedeki boş yuvaya sürükle. İstersen kartı seçip yuvaya dokun.</p>';
   task.querySelectorAll('[data-piece]').forEach(b=>b.onclick=()=>{state.simileSelected=b.dataset.piece;task.querySelectorAll('[data-piece]').forEach(x=>x.classList.toggle('selected',x===b))});
   stage.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>{if(state.simileSelected)place(state.simileSelected,b.dataset.target)});
   SceneWorkshop.bindDrag('[data-piece]:not(:disabled)','[data-target]',(a,b)=>place(a.dataset.piece,b.dataset.target));state.simileFresh=null;
  };
  const place=(pid,tid)=>{const p=r.pieces.find(x=>x.id===pid);
   if(locked()||state.simileComplete||!p||state.similePairs[p.target])return;
   if(p.target!==tid)return wrong(r.hint);
   state.similePairs[tid]=pid;state.placed[tid]=1;state.done++;state.simileSelected=null;state.simileFresh=tid;draw();
   if(state.done===r.pieces.length){state.simileComplete=true;finish(r)}
  };draw();
 }
 function greenhouse({r,state,wrong,finish,next,fast,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('greenhouse-scene');
  state.greenhouseNeeds=state.greenhouseNeeds||[];state.greenhouseExtras=state.greenhouseExtras||[];
  const i=state.ix||0,k=r.kartlar[i];if(!k)return;
  const icons=['💧','☀️','🌬️','🌡️','🎨','🎵','🪴','⭕'];
  const draw=()=>{
   const grown=Math.min(5,state.greenhouseNeeds.length);
   stage.innerHTML='<div class="greenhouse-workspace"><header>🌱 BİTKİ SERASI <small>Yaşaması için gerekliyse fideye, değilse yan rafa bırak</small></header><div class="greenhouse-bench"><div class="greenhouse-sky"><span class="greenhouse-sun" aria-hidden="true">☀</span><span class="greenhouse-cloud" aria-hidden="true">☁</span></div><div class="greenhouse-stations"><button class="greenhouse-plant '+(state.greenhouseFresh===0?'greenhouse-plant-grow':'')+'" data-kutu="0" aria-label="Fide ve toprağı: gerekli ihtiyaçları buraya bırak"><span class="greenhouse-plant-label">GEREKLİ → FİDEYE</span><span class="greenhouse-stem" style="--growth:'+grown+'"><i class="greenhouse-leaf greenhouse-leaf-left"></i><i class="greenhouse-leaf greenhouse-leaf-right"></i><i class="greenhouse-leaf greenhouse-leaf-top"></i></span><span class="greenhouse-soil"><span class="greenhouse-roots" aria-hidden="true">╱│╲</span></span><span class="greenhouse-pot"></span><span class="greenhouse-badges">'+state.greenhouseNeeds.map(x=>'<span>'+esc(x.icon)+'</span>').join('')+'</span></button><button class="greenhouse-extras" data-kutu="1" aria-label="Yan raf: bitkinin ihtiyacı olmayanlar buraya bırak"><span class="greenhouse-extras-label">GEREKLİ DEĞİL → YAN RAFA</span><span class="greenhouse-shelf"><span class="greenhouse-shelf-items">'+state.greenhouseExtras.map(x=>'<span>'+esc(x.icon)+'</span>').join('')+'</span></span><span class="greenhouse-shelf-leg"></span></button></div><button class="greenhouse-supply" data-sinif-kart="1" aria-label="'+esc(k.t)+' kartını taşı"><span class="greenhouse-supply-icon">'+icons[i]+'</span><strong>'+esc(k.t)+'</strong><span class="greenhouse-grip" aria-hidden="true">⋮⋮</span></button></div><p class="greenhouse-status" role="status">'+(i+1)+' / '+r.kartlar.length+' · '+esc(state.not||'Bu olmadan bitki yaşayabilir mi?')+'</p></div>';
   task.innerHTML='<p class="greenhouse-help">Kartı fideye veya yan rafa sürükle. İstersen kartı seçip hedefe dokun.</p>';
   const source=stage.querySelector('[data-sinif-kart]');source.onclick=()=>{state.greenhouseSelected=!state.greenhouseSelected;source.classList.toggle('selected',state.greenhouseSelected)};
   stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>{if(state.greenhouseSelected)place(+b.dataset.kutu)});
   SceneWorkshop.bindDrag('[data-sinif-kart]','[data-kutu]',(_,b)=>place(+b.dataset.kutu));state.greenhouseFresh=null;
  };
  const place=j=>{if(locked()||state.gecis||state.greenhouseComplete)return;
   if(j!==k.dogru)return wrong(k.hint||r.ipucu);
   (j===0?state.greenhouseNeeds:state.greenhouseExtras).push({text:k.t,icon:icons[i]});
   state.sayim[j]++;state.ix=i+1;state.not=k.neden||'';state.greenhouseFresh=j;state.greenhouseSelected=false;
   draw();stage.querySelector('[data-sinif-kart]').disabled=true;
   next(()=>{if(state.ix>=r.kartlar.length){state.greenhouseComplete=true;finish()}else greenhouse({r,state,wrong,finish,next,fast,locked})},fast?30:850);
  };draw();
 }
 return {simile,greenhouse};
})();
