/* Sınıf oylaması: duyulan tercihi gerçek oy sandığına bırak ve çeteleyi izle. */
window.SceneVoting=(()=>{
 const esc=SceneWorkshop.escape;
 function render({r,state,wrong,finish,next,fast,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task'),scene=document.querySelector('.scene');
  scene.classList.add('voting-scene');stage.classList.add('voting-stage');
  state.votes=state.votes||r.kutular.map(()=>[]);
  const i=state.ix||0,k=r.kartlar[i];if(!k)return;
  const draw=()=>{
   stage.innerHTML=`<div class="vote-room"><header>SINIF GEZİSİ OYLAMASI <small>Arkadaşını dinle, oyunu sandığa bırak</small></header><div class="vote-teacher" aria-hidden="true"><span class="vote-head"></span><span class="vote-body"></span><span class="vote-board">GEZİ İÇİN OY VERİYORUZ</span></div><div class="vote-boxes">${r.kutular.map((name,j)=>`<button class="vote-box ${state.voteFresh===j?'vote-arrival':''}" data-kutu="${j}" aria-label="${esc(name)} oy sandığı"><span class="vote-box-title">${esc(name)}</span><span class="vote-box-lid"><i></i></span><span class="vote-box-window" aria-hidden="true">${state.votes[j].map(()=>'<i class="vote-slip"></i>').join('')}</span><span class="vote-box-total">${state.votes[j].length} oy</span></button>`).join('')}</div><button class="vote-source" data-sinif-kart="1" aria-label="${esc(k.t)} oy kartını taşı"><span class="vote-speaker" aria-hidden="true">●</span><span>${esc(k.t)}</span><span class="vote-grip" aria-hidden="true">⋮⋮</span></button><p class="vote-status" role="status">${i+1} / ${r.kartlar.length} oy${state.not?' · '+esc(state.not):''}</p></div>`;
   task.innerHTML='<p class="vote-help">Oy kartını arkadaşının seçtiği sandığın kapağına sürükle. İstersen önce karta, sonra sandığa dokun.</p>';
   const source=stage.querySelector('[data-sinif-kart]');source.onclick=()=>{state.voteSelected=!state.voteSelected;source.classList.toggle('selected',!!state.voteSelected)};
   stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>{if(state.voteSelected)place(+b.dataset.kutu)});
   SceneWorkshop.bindDrag('[data-sinif-kart]','[data-kutu]',(_,b)=>place(+b.dataset.kutu));state.voteFresh=null;
  };
  const place=j=>{
   if(locked()||state.gecis||state.voteComplete)return;
   if(j!==k.dogru)return wrong(k.hint||r.ipucu);
   state.votes[j].push(k.t);state.sayim[j]++;state.ix=i+1;state.not=k.neden||'';state.voteFresh=j;state.voteSelected=false;
   draw();stage.querySelector('[data-sinif-kart]').disabled=true;
   next(()=>{if(state.ix>=r.kartlar.length){state.voteComplete=true;finish()}else render({r,state,wrong,finish,next,fast,locked})},fast?30:780);
  };
  draw();
 }
 return {render};
})();
