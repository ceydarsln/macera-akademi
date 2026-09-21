/* İkinci denetim paketi: her öğrenme hedefinin kendine ait çalışma yüzeyi. */
window.SceneDiscovery=(()=>{
 const esc=SceneWorkshop.escape;
 const plain=html=>{const el=document.createElement('div');el.innerHTML=html;return el.textContent};
 function picture(index,changed,context=false){
  const fill=changed?'#91cbd7':'#edb568';
  let shapes='';
  if(!context&&index===0)shapes=`<path d="M31 31h48v37q-24 15-48 0z" fill="${fill}"/><path d="M79 37q30 0 8 24" fill="none" stroke="${fill}" stroke-width="8"/>${changed?'<path d="M40 18l8 8m-8 0l8-8m13-5l8 8m-8 0l8-8" stroke="#538baf" stroke-width="3"/>':'<path d="M42 26q-8-8 0-17m16 17q-8-8 0-17" fill="none" stroke="#b57747" stroke-width="3"/>'}`;
  else if(!context&&index===1)shapes=`<path d="M25 65h${changed?35:75}v-17H25z" fill="${fill}"/><path d="M32 49v8m10-8v8m10-8v8" stroke="#61472d" stroke-width="2"/>`;
  else if(!context&&index===2)shapes=`<path d="M37 76V13h46v63" fill="#67534b"/><path d="M42 19h${changed?35:14}v56H42z" fill="${fill}"/><circle cx="${changed?69:49}" cy="48" r="3" fill="#fff"/>`;
  else if(!context&&index===3)shapes=`<path d="M35 69l8-41h34l8 41z" fill="${fill}"/><path d="M50 28q-1-23 20 0" fill="none" stroke="#526473" stroke-width="6"/><text x="60" y="57" text-anchor="middle" font-size="16" fill="#243e52">${changed?'1':'10'} kg</text>`;
  else if(index===1)shapes=`<circle cx="60" cy="44" r="32" fill="#fff6d7" stroke="#bd8857" stroke-width="5"/><path d="M60 22v22l${changed?'20 9':'-19 -9'}" stroke="#35495a" stroke-width="4" fill="none"/>`;
  else shapes=`<path d="M${changed?26:94} 45h${changed?62:-62}m${changed?62:-62} 0" stroke="${fill}" stroke-width="10"/><path d="M${changed?'71 28l18 17-18 17':'49 28L31 45l18 17'}" fill="none" stroke="${fill}" stroke-width="10"/><rect x="45" y="66" width="30" height="12" rx="3" fill="#687d85"/>`;
  return `<svg viewBox="0 0 120 90" aria-hidden="true">${shapes}</svg>`;
 }
 function matching({id,r,state,finish,wrong}){
  state.placed={};state.done=0;state.matches={};
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  const mode=id==='p03'?'bridge':id==='p08'?'reading':'mirror';
  document.querySelector('.scene').classList.add('discovery-scene',`discovery-${mode}`);
  const draw=()=>{
   const targets=r.targets.map((t,i)=>{
    const p=r.pieces.find(p=>state.matches[t.id]===p.id),done=!!p,fresh=state.fresh===t.id;
    if(mode==='bridge')return `<button class="bridge-span ${done?'built':''} ${fresh?'bridge-arrival':''}" data-target="${t.id}" aria-label="Köprü yuvası: ${esc(plain(t.html))}"><small>${t.html}</small><span class="bridge-deck">${p?p.html:'<i>＋</i>'}</span><span class="bridge-pier"></span></button>`;
    if(mode==='reading')return `<button class="reading-page ${done?'read':''} ${fresh?'page-arrival':''}" data-target="${t.id}"><b>${t.html}</b><span>${p?p.html:'<i class="writing-lines" aria-hidden="true"></i>'}</span>${done?'<em>✓ Okunuşu eşleşti</em>':''}</button>`;
    return `<button class="opposite-mirror ${done?'reflected':''}" data-target="${t.id}" aria-label="${esc(plain(t.html))} aynası"><span class="mirror-glass ${fresh?'mirror-turn':''}">${done?picture(i,true,r.pieces[0].html.includes('binmek')):'<span class="mirror-mist" aria-hidden="true">?</span>'}<b>${t.html}</b></span><span class="mirror-base">${p?p.html:'Sözcüğü aynaya bırak'}</span></button>`;
   }).join('');
   stage.innerHTML=mode==='bridge'?`<div class="place-bridge"><header>BASAMAK KÖPRÜSÜ <strong>${['245 612','103 020','670 405'][r._round]}</strong></header><div class="bridge-water"></div><div class="bridge-spans">${targets}</div><div class="bridge-traveller ${state.done===r.pieces.length?'crossing':''}" aria-hidden="true">🚲</div></div><p class="discovery-status" role="status">${state.done} / 6 köprü parçası yerleşti</p>`:mode==='reading'?`<div class="reading-desk"><header>SAYILARIN OKUMA DEFTERİ</header><div class="reading-pages">${targets}</div></div>`:`<div class="mirror-room"><header>ZIT ANLAM ATÖLYESİ</header><div class="mirror-grid">${targets}</div></div>`;
   const order=r.pieces.length===6?[4,1,5,0,3,2]:r.pieces.length===4?[2,0,3,1]:[2,0,1];
   task.innerHTML=`<div class="discovery-pieces">${order.map(i=>r.pieces[i]).map(p=>`<button class="piece ${state.matches[p.target]===p.id?'done':''}" data-piece="${p.id}" ${state.matches[p.target]===p.id?'disabled':''}>${p.html}</button>`).join('')}</div><p class="discovery-help">${mode==='bridge'?'Parçayı köprüdeki yerine':mode==='reading'?'Okunuşu defterdeki sayının sayfasına':'Sözcüğü karşıtının aynasına'} sürükle. İstersen parçaya, sonra hedefine dokun.</p>`;
   task.querySelectorAll('[data-piece]').forEach(b=>b.onclick=()=>{state.tapPiece=b.dataset.piece;task.querySelectorAll('[data-piece]').forEach(x=>x.classList.toggle('selected',x===b))});
   stage.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>{if(state.tapPiece)place(state.tapPiece,b.dataset.target)});
   SceneWorkshop.bindDrag('[data-piece]:not(:disabled)','[data-target]',(a,b)=>place(a.dataset.piece,b.dataset.target));
   state.fresh=null;
  };
  const place=(pid,tid)=>{
   if(state.complete)return;const p=r.pieces.find(x=>x.id===pid);if(!p||state.matches[p.target])return;
   if(p.target!==tid)return wrong(r.hint);
   state.matches[tid]=pid;state.placed[tid]=1;state.done++;state.tapPiece=null;state.fresh=tid;draw();
   if(state.done===r.pieces.length){state.complete=true;finish(r)}
  };
  draw();
 }
 function sourceBook(label,detail='',fresh=false){return `<span class="source-book ${fresh?'source-arrival':''}"><span class="source-spine"></span><b>${esc(label)}</b>${detail?`<small>${esc(detail)}</small>`:''}<i aria-hidden="true"></i></span>`}
 function researchBag(items,title,attr,fresh=-1){return `<div class="research-satchel"><div class="satchel-handle"></div><div class="satchel-lid"><strong>${esc(title)}</strong><span>${items.length} kaynak</span></div><div class="satchel-mouth" ${attr} aria-label="Açık araştırma çantasının içi">${items.map(x=>sourceBook(x.label,x.detail,x.index===fresh)).join('')}${!items.length?'<div class="satchel-empty" aria-hidden="true"><i></i><i></i><i></i></div>':''}</div><div class="satchel-front"><span></span><b>KAYNAK DOSYASI</b><span></span></div></div>`}
 return {matching,picture,sourceBook,researchBag};
})();
