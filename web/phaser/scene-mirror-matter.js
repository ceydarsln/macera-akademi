/* Jest/mimik aynası ve maddenin hâlleri deney tezgâhı. */
window.SceneMirrorMatter=(()=>{
 const esc=SceneWorkshop.escape;
 const plain=s=>String(s).replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim();
 const emotionKind=s=>{const t=plain(s).toLocaleLowerCase('tr');return /üzüntü/.test(t)?'sad':/öfke/.test(t)?'angry':/korku/.test(t)?'fear':/şaşkınlık/.test(t)?'surprise':/heyecan/.test(t)?'excited':'joy'};
 function mirror({r,state,wrong,finish,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');document.querySelector('.scene').classList.add('emotion-mirror-scene');
  state.mirrorPairs={};state.placed={};state.done=0;
  const draw=()=>{
   stage.innerHTML='<div class="emotion-room"><header>🪞 JEST VE MİMİK AYNASI <small>Yüz ve beden ipucunu doğru aynada göster</small></header><div class="emotion-mirrors">'+r.targets.map((t,i)=>{
    const p=r.pieces.find(x=>x.id===state.mirrorPairs[t.id]);
    const cue=p?.html.match(/<small>beden:\s*([^<]+)<\/small>/)?.[1];
    return '<button class="emotion-mirror '+(p?'emotion-reflected ':'')+(state.mirrorFresh===t.id?'emotion-reveal':'')+'" data-target="'+t.id+'" aria-label="'+esc(plain(t.html))+' aynası"><span class="emotion-frame"><span class="emotion-glass"><span class="emotion-face">'+(p?p.html.match(/<div[^>]*>(.*?)<\/div>/)?.[1]||'🙂':'?')+'</span><span class="emotion-body '+(p?'emotion-body-'+emotionKind(t.html):'')+'" aria-hidden="true"><i></i></span></span></span><strong>'+t.html+'</strong><span class="emotion-cue">'+(p?esc(cue||'Beden ipucuna bak'):'İfadeyi aynaya sürükle')+'</span></button>';
   }).join('')+'</div><p class="emotion-count" role="status">'+state.done+' / '+r.pieces.length+' ifade aynada</p></div>';
   task.innerHTML='<div class="emotion-cards">'+r.pieces.map(p=>'<button class="emotion-card" data-piece="'+p.id+'" '+(state.mirrorPairs[p.target]?'disabled':'')+'>'+p.html+'</button>').join('')+'</div><p class="emotion-help">Yüzü ve bedeni birlikte incele. Kartı aynaya sürükle veya seçip aynaya dokun.</p>';
   task.querySelectorAll('[data-piece]').forEach(b=>b.onclick=()=>{state.mirrorSelected=b.dataset.piece;task.querySelectorAll('[data-piece]').forEach(x=>x.classList.toggle('selected',x===b))});
   stage.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>{if(state.mirrorSelected)place(state.mirrorSelected,b.dataset.target)});
   SceneWorkshop.bindDrag('[data-piece]:not(:disabled)','[data-target]',(a,b)=>place(a.dataset.piece,b.dataset.target));state.mirrorFresh=null;
  };
  const place=(pid,tid)=>{const p=r.pieces.find(x=>x.id===pid);if(locked()||state.mirrorComplete||!p||state.mirrorPairs[p.target])return;if(p.target!==tid)return wrong(r.hint);state.mirrorPairs[tid]=pid;state.placed[tid]=1;state.done++;state.mirrorFresh=tid;state.mirrorSelected=null;draw();if(state.done===r.pieces.length){state.mirrorComplete=true;finish(r)}};draw();
 }
 function matterIcon(text){const s=text.toLocaleLowerCase('tr');if(/taş/.test(s))return'🪨';if(/buz/.test(s))return'🧊';if(/kalem/.test(s))return'✏️';if(/kum/.test(s))return'◌';if(/un —/.test(s))return'⚪';if(/bal —/.test(s))return'🍯';if(/sabun/.test(s))return'🧴';if(/süt/.test(s))return'🥛';if(/yağı/.test(s))return'🫒';if(/su —/.test(s))return'💧';if(/buhar/.test(s))return'♨️';return'💨'}
 function matter({r,state,wrong,finish,next,fast,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');document.querySelector('.scene').classList.add('matter-lab-scene');
  state.matterBins=state.matterBins||r.kutular.map(()=>[]);const i=state.ix||0,k=r.kartlar[i];if(!k)return;
  const draw=()=>{
   stage.innerHTML='<div class="matter-lab"><header>⚗️ MADDE DENEY TEZGÂHI <small>Örneği davranışına uygun deney kabına bırak</small></header><div class="matter-vessels">'+r.kutular.map((b,j)=>{
    const name=typeof b==='string'?b:b.ad,alt=typeof b==='string'?'':b.alt,items=state.matterBins[j];
    const vessel=j===0?'<span class="matter-tray"><span class="matter-samples">'+items.map(x=>'<i title="'+esc(x.text)+'">'+esc(x.icon)+'</i>').join('')+'</span></span>':j===1?'<span class="matter-beaker"><span class="matter-liquid">'+items.map(x=>'<i title="'+esc(x.text)+'">'+esc(x.icon)+'</i>').join('')+'</span></span>':'<span class="matter-balloon"><span class="matter-gas">'+items.map(x=>'<i title="'+esc(x.text)+'">'+esc(x.icon)+'</i>').join('')+'</span></span>';
    return '<button class="matter-vessel matter-vessel-'+j+' '+(state.matterFresh===j?'matter-arrive':'')+'" data-kutu="'+j+'" aria-label="'+esc(name)+' deney düzeneği"><span class="matter-vessel-name">'+esc(name)+'</span>'+vessel+'<small>'+esc(alt)+'</small><span class="matter-vessel-count">'+items.length+' örnek</span></button>';
   }).join('')+'</div><button class="matter-specimen" data-sinif-kart="1" aria-label="'+esc(k.t)+' örneğini taşı"><span class="matter-specimen-icon">'+matterIcon(k.t)+'</span><strong>'+esc(k.t)+'</strong><span class="matter-grip" aria-hidden="true">⋮⋮</span></button><p class="matter-status" role="status">'+(i+1)+' / '+r.kartlar.length+' · '+esc(state.not||'Örneği kaba koyunca biçimi veya dağılımı ne olur?')+'</p></div>';
   task.innerHTML='<p class="matter-help">Örneği tepsiye, kaba veya balona sürükle. İstersen seçip deney düzeneğine dokun.</p>';
   const source=stage.querySelector('[data-sinif-kart]');source.onclick=()=>{state.matterSelected=!state.matterSelected;source.classList.toggle('selected',state.matterSelected)};
   stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>{if(state.matterSelected)place(+b.dataset.kutu)});
   SceneWorkshop.bindDrag('[data-sinif-kart]','[data-kutu]',(_,b)=>place(+b.dataset.kutu));state.matterFresh=null;
  };
  const place=j=>{if(locked()||state.gecis||state.matterComplete)return;if(j!==k.dogru)return wrong(k.hint||r.ipucu);state.matterBins[j].push({text:k.t,icon:matterIcon(k.t)});state.sayim[j]++;state.ix=i+1;state.not=k.neden||'';state.matterFresh=j;state.matterSelected=false;draw();stage.querySelector('[data-sinif-kart]').disabled=true;next(()=>{if(state.ix>=r.kartlar.length){state.matterComplete=true;finish()}else matter({r,state,wrong,finish,next,fast,locked})},fast?30:850)};draw();
 }
 return {mirror,matter};
})();
