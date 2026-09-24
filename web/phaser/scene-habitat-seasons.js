/* Üç ayrı sınıflandırma sahnesi: tartışma çemberi, yaşam alanları ve mevsim bahçesi. */
window.SceneHabitatSeasons=(()=>{
 const esc=SceneWorkshop.escape;
 const plain=x=>typeof x==='string'?x:x.ad;
 const setups={
  z01:{title:'TARTIŞMA ÇEMBERİ',help:'Görüş kartını konuşmak istediğin çocuğun balonuna sürükle.',name:'discussion'},
  g43:{title:'YAŞAM ALANLARI',help:'Canlının özelliklerini oku; kartı yaşayabileceği ortama sürükle.',name:'habitat'},
  h26:{title:'MEVSİM BAHÇESİ',help:'Hava olayını ait olduğu mevsim bahçesine sürükle.',name:'seasons'}
 };
 const habitatScenes={
  SUDA:'water',ORMANDA:'forest','ÇÖLDE':'desert',KUTUPTA:'polar',
  'YALNIZ SUDA':'water','HEM SUDA HEM KARADA':'shore','YALNIZ KARADA':'forest'
 };
 const seasonScenes={İLKBAHAR:'spring',YAZ:'summer',SONBAHAR:'autumn',KIŞ:'winter'};
 function art(id,label,j){
  if(id==='z01')return '<span class="hs-child" aria-hidden="true"><i class="hs-head"></i><i class="hs-body"></i></span>';
  const visual=id==='g43'?(habitatScenes[label]||'forest'):(seasonScenes[label]||'spring');
  if(id==='g43')return '<span class="hs-landscape hs-'+visual+'" aria-hidden="true"><i class="hs-sun"></i><i class="hs-ground"></i><i class="hs-feature"></i></span>';
  return '<span class="hs-season hs-'+visual+'" aria-hidden="true"><i class="hs-sun"></i><i class="hs-trunk"></i><i class="hs-leaves"></i><i class="hs-weather"></i></span>';
 }
 function render({id,r,state,wrong,finish,next,fast,locked}){
  const cfg=setups[id],stage=document.querySelector('#stage'),task=document.querySelector('#task'),scene=document.querySelector('.scene');
  if(!cfg)return false;
  scene.classList.add('hs-scene','hs-'+cfg.name+'-scene');stage.classList.add('hs-stage');
  state.hsBins=state.hsBins||r.kutular.map(()=>[]);
  const i=state.ix||0,k=r.kartlar[i];if(!k)return true;
  const draw=()=>{
   const stations=r.kutular.map((x,j)=>{const label=plain(x),items=state.hsBins[j];
    return `<button class="hs-station hs-${cfg.name}-station ${state.hsFresh===j?'hs-arrival':''}" data-kutu="${j}" aria-label="${esc(label)}: ${id==='z01'?'konuşma alanı':id==='g43'?'yaşam alanı':'mevsim bahçesi'}"><span class="hs-art">${art(id,label,j)}<span class="hs-receptacle ${items.length?'occupied':''}" aria-hidden="true">${items.length?esc(items[items.length-1]):id==='z01'?'…':'◌'}</span></span><strong class="hs-label">${esc(label)}</strong><span class="hs-placed" aria-hidden="true">${items.map(()=>'<i></i>').join('')}</span><small>${items.length} kart</small></button>`;
   }).join('');
   stage.innerHTML=`<div class="hs-workspace"><header>${cfg.title}<small>${esc(r.soru)}</small></header><div class="hs-stations">${stations}</div><button class="hs-source" data-sinif-kart="1" aria-label="${esc(k.t)} kartını taşı"><span class="hs-grip" aria-hidden="true">⋮⋮</span><span>${esc(k.t)}</span></button><div class="hs-status" role="status">${i+1} / ${r.kartlar.length}${state.not?' · '+esc(state.not):''}</div></div>`;
   task.innerHTML=`<p class="hs-instruction">${cfg.help} İstersen karta, sonra hedefe dokun.</p>`;
   const source=stage.querySelector('[data-sinif-kart]');source.onclick=()=>{state.hsSelected=!state.hsSelected;source.classList.toggle('selected',!!state.hsSelected)};
   stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>{if(state.hsSelected)place(+b.dataset.kutu)});
   SceneWorkshop.bindDrag('[data-sinif-kart]','[data-kutu]',(_,b)=>place(+b.dataset.kutu));state.hsFresh=null;
  };
  const place=j=>{
   if(locked()||state.gecis||state.hsComplete)return;
   if(j!==k.dogru)return wrong(k.hint||r.ipucu||'Karttaki ipucunu yeniden düşün.');
   state.hsBins[j].push(k.t);state.sayim[j]++;state.ix=i+1;state.not=k.neden||'';state.hsFresh=j;state.hsSelected=false;
   draw();stage.querySelector('[data-sinif-kart]').disabled=true;
   next(()=>{if(state.ix>=r.kartlar.length){state.hsComplete=true;finish()}else render({id,r,state,wrong,finish,next,fast,locked})},fast?30:780);
  };
  draw();return true;
 }
 return {render};
})();
