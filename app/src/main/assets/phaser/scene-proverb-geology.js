/* Atasözü yaşam sahneleri ve kayaç inceleme istasyonları. */
window.SceneProverbGeology=(()=>{
 const esc=SceneWorkshop.escape;
 const plain=s=>String(s).replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim();
 const scenes=[
  {icon:'🪙',name:'Birikim köşesi',action:'Her gün bir bozuk para kavanoza ekleniyor.',visual:'coin'},
  {icon:'🧰',name:'Saklama rafı',action:'Ayrılan eski bir parça sonra işe yarıyor.',visual:'shelf'},
  {icon:'👛',name:'Harcama masası',action:'Alışveriş, eldeki paraya göre planlanıyor.',visual:'wallet'},
  {icon:'🤝',name:'Ortak çalışma',action:'İki kişi ağır kutuyu birlikte kaldırıyor.',visual:'team'}
 ];
 function proverb({r,state,wrong,finish,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');document.querySelector('.scene').classList.add('proverb-scene');
  state.proverbPlaced={};state.placed={};state.done=0;
  const draw=()=>{
   stage.innerHTML='<div class="proverb-workspace"><header>🌉 ATASÖZÜ KÖPRÜSÜ <small>Sözü, yaşandığı küçük sahneye taşı</small></header><div class="proverb-dioramas">'+r.targets.map((t,i)=>{
    const d=scenes[i],p=r.pieces.find(x=>x.id===state.proverbPlaced[t.id]);
    return '<button class="proverb-diorama proverb-'+d.visual+' '+(p?'proverb-set ':'')+(state.proverbFresh===t.id?'proverb-action':'')+'" data-target="'+t.id+'" aria-label="'+esc(d.name+' — '+plain(t.html))+'"><span class="proverb-scene-name">'+esc(d.name)+'</span><span class="proverb-scene-art" aria-hidden="true"><span class="proverb-art-icon">'+d.icon+'</span><span class="proverb-art-result">'+(p?'✓':'?')+'</span></span><span class="proverb-situation">'+esc(d.action)+'</span><span class="proverb-caption">'+(p?'<strong>'+p.html+'</strong>':t.html)+'</span></button>';
   }).join('')+'</div><p class="proverb-count" role="status">'+state.done+' / '+r.pieces.length+' yaşam sahnesi tamamlandı</p></div>';
   task.innerHTML='<div class="proverb-cards">'+r.pieces.map(p=>'<button class="proverb-card" data-piece="'+p.id+'" '+(state.proverbPlaced[p.target]?'disabled':'')+'>'+p.html+'</button>').join('')+'</div><p class="proverb-help">Atasözünü anlattığı olayın içine sürükle. İstersen seçip sahneye dokun.</p>';
   task.querySelectorAll('[data-piece]').forEach(b=>b.onclick=()=>{state.proverbSelected=b.dataset.piece;task.querySelectorAll('[data-piece]').forEach(x=>x.classList.toggle('selected',x===b))});
   stage.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>{if(state.proverbSelected)place(state.proverbSelected,b.dataset.target)});
   SceneWorkshop.bindDrag('[data-piece]:not(:disabled)','[data-target]',(a,b)=>place(a.dataset.piece,b.dataset.target));state.proverbFresh=null;
  };
  const place=(pid,tid)=>{const p=r.pieces.find(x=>x.id===pid);if(locked()||state.proverbComplete||!p||state.proverbPlaced[p.target])return;if(p.target!==tid)return wrong(r.hint);state.proverbPlaced[tid]=pid;state.placed[tid]=1;state.done++;state.proverbFresh=tid;state.proverbSelected=null;draw();if(state.done===r.pieces.length){state.proverbComplete=true;finish(r)}};draw();
 }
 function specimenIcon(s){s=s.toLocaleLowerCase('tr');if(/kuvars|tuz/.test(s))return'◇';if(/granit|bazalt|kireç/.test(s))return'🪨';if(/kömür/.test(s))return'⬟';if(/demir/.test(s))return'⚙';if(/bakır/.test(s))return'◉';return'◈'}
 function geology({r,state,wrong,finish,next,fast,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');document.querySelector('.scene').classList.add('geology-scene');
  state.geologyBins=state.geologyBins||r.kutular.map(()=>[]);const i=state.ix||0,k=r.kartlar[i];if(!k)return;
  const draw=()=>{
   stage.innerHTML='<div class="geology-lab"><header>🔎 KAYAÇ–MADEN MASASI <small>Örneği uygun inceleme istasyonuna koy</small></header><div class="geology-stations">'+r.kutular.map((b,j)=>{
    const name=typeof b==='string'?b:b.ad,alt=typeof b==='string'?'':b.alt,items=state.geologyBins[j];
    const prop=j===0?'<span class="geology-crystal" aria-hidden="true">◇</span>':j===1?'<span class="geology-rock" aria-hidden="true"><i></i><i></i><i></i></span>':'<span class="geology-cart" aria-hidden="true"><i></i><i></i></span>';
    return '<button class="geology-station geology-station-'+j+' '+(state.geologyFresh===j?'geology-reveal':'')+'" data-kutu="'+j+'" aria-label="'+esc(name)+' inceleme istasyonu"><span class="geology-station-name">'+esc(name)+'</span><span class="geology-apparatus">'+prop+'</span><span class="geology-samples">'+items.map(x=>'<span title="'+esc(x.text)+'">'+esc(x.icon)+'</span>').join('')+'</span><small>'+esc(alt)+'</small><span class="geology-count">'+items.length+' örnek</span></button>';
   }).join('')+'</div><button class="geology-specimen" data-sinif-kart="1" aria-label="'+esc(k.t)+' örneğini taşı"><span class="geology-specimen-icon">'+specimenIcon(k.t)+'</span><strong>'+esc(k.t)+'</strong><span class="geology-grip" aria-hidden="true">⋮⋮</span></button><p class="geology-status" role="status">'+(i+1)+' / '+r.kartlar.length+' · '+esc(state.not||'Tek yapı mı, karışım mı, çıkarılıp kullanılan kaynak mı?')+'</p></div>';
   task.innerHTML='<p class="geology-help">Örneği kristal büyütecine, kayaç tepsisine veya maden arabasına sürükle.</p>';
   const source=stage.querySelector('[data-sinif-kart]');source.onclick=()=>{state.geologySelected=!state.geologySelected;source.classList.toggle('selected',state.geologySelected)};
   stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>{if(state.geologySelected)place(+b.dataset.kutu)});
   SceneWorkshop.bindDrag('[data-sinif-kart]','[data-kutu]',(_,b)=>place(+b.dataset.kutu));state.geologyFresh=null;
  };
  const place=j=>{if(locked()||state.gecis||state.geologyComplete)return;if(j!==k.dogru)return wrong(k.hint||r.ipucu);state.geologyBins[j].push({text:k.t,icon:specimenIcon(k.t)});state.sayim[j]++;state.ix=i+1;state.not=k.neden||'';state.geologyFresh=j;state.geologySelected=false;draw();stage.querySelector('[data-sinif-kart]').disabled=true;next(()=>{if(state.ix>=r.kartlar.length){state.geologyComplete=true;finish()}else geology({r,state,wrong,finish,next,fast,locked})},fast?30:850)};draw();
 }
 return {proverb,geology};
})();
