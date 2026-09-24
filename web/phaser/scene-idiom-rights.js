/* Deyim makinesi ve hak-sorumluluk köprüsü: hedefler sahnenin çalışan parçaları. */
window.SceneIdiomRights=(()=>{
 const esc=SceneWorkshop.escape;
 const pictures={
  y47:[
   {icon:'🙌',scene:'Çocuk sevinçle zıplıyor.',className:'joy'},
   {icon:'🧍',scene:'Bir çocuk herkese tepeden bakıyor.',className:'pride'},
   {icon:'📖',scene:'Bir sayfayı kısa süre inceliyor.',className:'glance'},
   {icon:'👂',scene:'Konuşanı dikkatle dinliyor.',className:'listen'}
  ],
  y62:[
   {icon:'🗑️',scene:'Çöp kutusu',className:'clean'},
   {icon:'👂',scene:'Dinleme sırası',className:'speech'},
   {icon:'📚',scene:'Kitap iade rafı',className:'library'},
   {icon:'⏳',scene:'Oyun sırası',className:'play'}
  ]
 };
 function render({id,r,state,wrong,finish,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  const isBridge=id==='y62',scene=document.querySelector('.scene');
  scene.classList.add(isBridge?'rights-bridge-scene':'idiom-machine-scene');
  state.placed={};state.done=0;state.idiomSelected=null;state.idiomFresh=null;
  const draw=()=>{
   const slots=r.targets.map((t,i)=>{
    const picture=pictures[id][i],placed=state.placed[t.id];
    return `<button class="${isBridge?'rights-plank':'idiom-chamber'} ${picture.className} ${placed?'filled':''} ${state.idiomFresh===t.id?'just-filled':''}" data-target="${t.id}" aria-label="${esc(picture.scene)}: ${esc(t.html.replace(/<[^>]+>/g,''))}"><span class="scene-part-art" aria-hidden="true">${picture.icon}</span><span class="scene-part-hint">${esc(picture.scene)}</span><span class="scene-part-socket">${placed?`<strong>${r.pieces.find(p=>p.id===placed).html}</strong>`:t.html}</span></button>`;
   }).join('');
   stage.innerHTML=isBridge
    ?`<div class="rights-workbench"><header>🌉 DENGE KÖPRÜSÜ <small>Hakları, köprüdeki sorumluluklarına bağla</small></header><div class="rights-river"><div class="river-bank left">HAKLAR</div><div class="rights-planks">${slots}</div><div class="river-bank right">SORUMLULUKLAR</div></div><p class="scene-part-count" role="status">${state.done} / ${r.pieces.length} köprü bağlantısı</p></div>`
    :`<div class="idiom-workbench"><header>⚙️ DEYİM MAKİNESİ <small>Deyimi yaşandığı sahnenin yuvasına tak</small></header><div class="idiom-case"><div class="idiom-conveyor">${slots}</div><div class="idiom-gears" aria-hidden="true"><span>⚙</span><span>⚙</span></div></div><p class="scene-part-count" role="status">${state.done} / ${r.pieces.length} deyim işlendi</p></div>`;
   task.innerHTML=`<div class="scene-part-sources">${r.pieces.map(p=>`<button class="scene-part-source" data-piece="${p.id}" ${state.placed[p.target]?'disabled':''}>${p.html}</button>`).join('')}</div><p class="scene-part-instruction">Kartı sahnedeki yerine sürükle veya seçip yuvaya dokun.</p>`;
   task.querySelectorAll('[data-piece]').forEach(b=>b.onclick=()=>{state.idiomSelected=b.dataset.piece;task.querySelectorAll('[data-piece]').forEach(x=>x.classList.toggle('selected',x===b))});
   stage.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>{if(state.idiomSelected)place(state.idiomSelected,b.dataset.target)});
   SceneWorkshop.bindDrag('[data-piece]:not(:disabled)','[data-target]',(a,b)=>place(a.dataset.piece,b.dataset.target));
   state.idiomFresh=null;
  };
  const place=(pid,tid)=>{
   const p=r.pieces.find(x=>x.id===pid);
   if(locked()||state.idiomComplete||!p||state.placed[p.target])return;
   if(p.target!==tid)return wrong(r.hint);
   state.placed[tid]=pid;state.done++;state.idiomFresh=tid;state.idiomSelected=null;draw();
   if(state.done===r.pieces.length){state.idiomComplete=true;scene.classList.add('scene-part-complete');finish(r)}
  };
  draw();
 }
 return {render};
})();
