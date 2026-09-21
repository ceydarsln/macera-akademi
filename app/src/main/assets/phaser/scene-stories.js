/* Davranış kanıtları ve neden–sonuç için ayrı anlatı yüzeyleri. */
window.SceneStories=(()=>{
 const esc=SceneWorkshop.escape;
 function consequence(i,done){
  let body='';
  if(i===0)body=`<rect y="57" width="180" height="43" fill="#98a7a4"/><path d="M0 75h180" stroke="#eee3be" stroke-width="4" stroke-dasharray="20 12"/><path d="M8 25q3-24 27-18 25-10 28 15z" fill="#c1d3dc"/>${done?'<g class="story-rain" stroke="#5c99b5" stroke-width="3"><path d="M18 33l-7 13m27-13l-7 13m27-13l-7 13"/></g><ellipse class="story-puddle" cx="100" cy="64" rx="54" ry="8" fill="#8ec0d0"/>':''}`;
  if(i===1)body=`<path d="M21 39q32-9 59 0 30-9 57 0v46q-30-9-57 0-31-9-59 0z" fill="#fff5d5" stroke="#8c8062" stroke-width="3"/><path d="M80 39v46m-48-32h33m-33 11h33m31-11h28m-28 11h28" stroke="#c7bca2" stroke-width="2"/>${done?'<g class="story-certificate"><rect x="100" y="5" width="66" height="47" rx="4" fill="#f7efd3" stroke="#9daaa5" stroke-width="2"/><path d="M113 27l10 10 25-22" fill="none" stroke="#55977c" stroke-width="6"/></g>':''}`;
  if(i===2)body=`<rect x="26" y="50" width="125" height="32" rx="5" fill="#7794b5"/><rect x="23" y="76" width="8" height="19" fill="#7f684d"/><rect x="145" y="76" width="8" height="19" fill="#7f684d"/><rect x="28" y="49" width="36" height="17" rx="6" fill="#f7e9c9"/>${done?'<g class="story-sun"><circle cx="142" cy="22" r="14" fill="#e9b64e"/><path d="M142 2v-4m0 47v-4m-20-19h-4m48 0h-4" stroke="#d6a149" stroke-width="3"/></g><circle cx="61" cy="40" r="12" fill="#d9a77d"/><path d="M56 41q5 8 11 0" stroke="#7a5042" fill="none" stroke-width="2"/>':'<path d="M142 5q-15 21 11 23-29 14-31-9 0-10 20-14" fill="#eddcab"/><text x="62" y="38" font-size="16" fill="#57738b">z z</text>'}`;
  if(i===3)body=`<path d="M65 64h54l-8 33H73z" fill="#be8c69" stroke="#8b604a" stroke-width="3"/><g class="${done?'story-wilt':''}" style="transform-origin:91px 67px"><path d="M91 65V29m0 22q-26-24-26-2 0 12 26 10m0-10q26-24 26-2 0 10-26 10" fill="#80a176" stroke="#5d8b61" stroke-width="3"/><g fill="${done?'#bfaa83':'#e0b26a'}"><circle cx="79" cy="23" r="12"/><circle cx="99" cy="17" r="12"/><circle cx="101" cy="36" r="12"/></g><circle cx="91" cy="26" r="9" fill="#97744d"/></g>`;
  return `<svg viewBox="0 0 180 100" aria-hidden="true" focusable="false">${body}</svg>`;
 }
 function render({id,r,state,wrong,finish}){
  state.storyPlaced={};state.done=0;state.placed={};const mode=id==='y12'?'causes':'virtues';
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');document.querySelector('.scene').classList.add('story-scene',`story-${mode}`);
  const draw=()=>{
   stage.innerHTML=`<div class="story-workspace"><header>${mode==='causes'?'NEDEN OLDU, NE DEĞİŞTİ?':'ERDEM KÂŞİFİNİN GÜNLÜĞÜ'}</header><div class="story-targets">${r.targets.map((t,i)=>{
    const pid=state.storyPlaced[t.id],p=r.pieces.find(p=>p.id===pid),fresh=state.storyFresh===t.id;
    if(mode==='causes')return `<button class="cause-scene ${fresh?'cause-change':''}" data-target="${t.id}"><div class="cause-picture">${consequence(i,!!p)}</div><strong>${t.html}</strong><span class="cause-caption">${p?`${p.html} → ${t.html}`:'Nedenini sahneye bırak'}</span></button>`;
    return `<button class="virtue-page" data-target="${t.id}"><header>${t.html}</header><div class="virtue-evidence ${fresh?'virtue-ink':''}">${p?p.html:'<i aria-hidden="true"></i><i aria-hidden="true"></i><i aria-hidden="true"></i>'}</div><span class="virtue-stamp ${fresh?'stamp-arrival':''}">${p?'✓ KANIT BULUNDU':'Davranış kanıtı bekleniyor'}</span></button>`;
   }).join('')}</div><p class="story-count">${state.done} / ${r.pieces.length} ${mode==='causes'?'ilişki kuruldu':'kanıt toplandı'}</p></div>`;
   task.innerHTML=`<div class="story-sources">${[2,0,3,1].map(i=>r.pieces[i]).map(p=>`<button class="story-source" data-piece="${p.id}" ${state.storyPlaced[p.target]?'disabled':''}>${p.html}</button>`).join('')}</div><p class="story-help">${mode==='causes'?'Nedeni, sonucunun yaşandığı sahneye':'Davranışı, günlükteki erdem sayfasına'} sürükle. Dokunarak seçip yerleştirebilirsin.</p>`;
   task.querySelectorAll('[data-piece]').forEach(b=>b.onclick=()=>{state.tapPiece=b.dataset.piece;task.querySelectorAll('[data-piece]').forEach(x=>x.classList.toggle('selected',x===b))});
   stage.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>{if(state.tapPiece)place(state.tapPiece,b.dataset.target)});
   SceneWorkshop.bindDrag('[data-piece]:not(:disabled)','[data-target]',(a,b)=>place(a.dataset.piece,b.dataset.target));state.storyFresh=null;
  };
  const place=(pid,tid)=>{const p=r.pieces.find(p=>p.id===pid);if(!p||state.storyComplete||state.storyPlaced[p.target])return;if(p.target!==tid)return wrong(r.hint);
   state.storyPlaced[tid]=pid;state.placed[tid]=1;state.done++;state.tapPiece=null;state.storyFresh=tid;draw();
   if(state.done===r.pieces.length){state.storyComplete=true;finish(r)}
  };draw();
 }
 return {render};
})();
