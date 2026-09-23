/* Kitap sayfaları ve enerji istasyonları: konuya özgü gerçek bırakma alanları. */
window.SceneBookPower=(()=>{
 const esc=SceneWorkshop.escape;
 const plain=s=>String(s).replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim();
 function book({r,state,wrong,finish,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('book-scene');
  state.bookPlaced={};state.placed={};state.done=0;
  const order=['t2','t4','t1','t3'];
  const draw=()=>{
   stage.innerHTML='<div class="book-workspace"><header>KİTABI KEŞFET <small>Bölüm kartını işlevini anlatan gerçek sayfaya bırak</small></header><div class="book-volume"><span class="book-spine" aria-hidden="true"></span><div class="book-pages">'+order.map((id,i)=>{
    const t=r.targets.find(x=>x.id===id),p=r.pieces.find(x=>x.id===state.bookPlaced[id]);
    return '<button class="book-page book-page-'+i+' '+(p?'book-filled ':'')+(state.bookFresh===id?'book-page-turn':'')+'" data-target="'+id+'" aria-label="'+esc(plain(t.html))+' kitabın sayfası"><span class="book-page-number">'+(i+1)+'. yüz</span><span class="book-page-question">'+t.html+'</span>'+(p?'<strong class="book-section-name">'+p.html+'</strong>':'<span class="book-page-guide">Bölümü sayfaya bırak</span>')+'<i class="book-page-corner" aria-hidden="true"></i></button>';
   }).join('')+'</div></div><p class="book-counter" role="status">'+state.done+' / '+r.pieces.length+' bölüm yerleşti</p></div>';
   task.innerHTML='<div class="book-sources">'+[2,0,3,1].map(i=>r.pieces[i]).map(p=>'<button class="book-source" data-piece="'+p.id+'" '+(state.bookPlaced[p.target]?'disabled':'')+'>'+p.html+'</button>').join('')+'</div><p class="book-help">Bölüm kartını ilgili sayfaya sürükle veya seçip sayfaya dokun.</p>';
   task.querySelectorAll('[data-piece]').forEach(b=>b.onclick=()=>{state.bookSelected=b.dataset.piece;task.querySelectorAll('[data-piece]').forEach(x=>x.classList.toggle('selected',x===b))});
   stage.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>{if(state.bookSelected)place(state.bookSelected,b.dataset.target)});
   SceneWorkshop.bindDrag('[data-piece]:not(:disabled)','[data-target]',(a,b)=>place(a.dataset.piece,b.dataset.target));state.bookFresh=null;
  };
  const place=(pid,tid)=>{const p=r.pieces.find(x=>x.id===pid);
   if(locked()||state.bookComplete||!p||state.bookPlaced[p.target])return;
   if(p.target!==tid)return wrong(r.hint);
   state.bookPlaced[tid]=pid;state.placed[tid]=1;state.done++;state.bookSelected=null;state.bookFresh=tid;draw();
   if(state.done===r.pieces.length){state.bookComplete=true;finish(r)}
  };draw();
 }
 function appliance(label){
  const s=label.toLocaleLowerCase('tr');const svg=x=>'<svg viewBox="0 0 80 80" aria-hidden="true" focusable="false">'+x+'</svg>';
  if(/buzdolabı/.test(s))return svg('<rect x="20" y="9" width="41" height="63" rx="4" fill="#d4e6e5" stroke="#507684" stroke-width="4"/><path d="M20 40h41M28 25v9m0 15v11" stroke="#507684" stroke-width="4"/>');
  if(/süpürge/.test(s))return svg('<path d="M39 10l4 54" stroke="#ae7c4b" stroke-width="8" stroke-linecap="round"/><path d="M22 60h38l-5 13H28z" fill="#d4b283" stroke="#8d7150" stroke-width="3"/>');
  if(/kaşık/.test(s))return svg('<ellipse cx="40" cy="22" rx="13" ry="15" fill="#d6b987" stroke="#99784e" stroke-width="3"/><path d="M40 38v31" stroke="#a47a4d" stroke-width="8" stroke-linecap="round"/>');
  if(/çamaşır/.test(s))return svg('<rect x="12" y="10" width="56" height="60" rx="5" fill="#d6e8ec" stroke="#5e8590" stroke-width="4"/><circle cx="40" cy="44" r="19" fill="#9bcbd6" stroke="#5e8590" stroke-width="4"/><circle cx="23" cy="19" r="3" fill="#5e8590"/>');
  if(/makas/.test(s))return svg('<path d="M24 54L60 16M56 56L21 16" stroke="#6d8491" stroke-width="7" stroke-linecap="round"/><circle cx="20" cy="59" r="10" fill="none" stroke="#bf795c" stroke-width="5"/><circle cx="61" cy="60" r="10" fill="none" stroke="#bf795c" stroke-width="5"/>');
  if(/fener/.test(s))return svg('<path d="M15 30h38l13-9v38l-13-9H15z" fill="#deb35b" stroke="#8d6736" stroke-width="4"/><path d="M22 29v22M68 25l8-7m-8 38l8 7" stroke="#f7e8a6" stroke-width="4"/>');
  if(/bisiklet/.test(s))return svg('<circle cx="21" cy="57" r="13" fill="none" stroke="#425967" stroke-width="5"/><circle cx="60" cy="57" r="13" fill="none" stroke="#425967" stroke-width="5"/><path d="M21 57l16-30 23 30H21l21-21M35 26h11" fill="none" stroke="#b95c51" stroke-width="5"/>');
  if(/araba/.test(s))return svg('<path d="M9 39h62v21H9z" fill="#db765e" stroke="#894c43" stroke-width="3"/><path d="M23 24h32l10 15H15z" fill="#b9dce1" stroke="#658993" stroke-width="3"/><circle cx="24" cy="61" r="8" fill="#364c57"/><circle cx="58" cy="61" r="8" fill="#364c57"/>');
  if(/kurutma/.test(s))return svg('<path d="M14 21h41l11 12-11 13H14z" fill="#c9d8df" stroke="#658797" stroke-width="4"/><path d="M34 46l-5 25h20l-4-25" fill="#7d9faf" stroke="#658797" stroke-width="4"/>');
  if(/açacağı/.test(s))return svg('<rect x="18" y="24" width="45" height="33" rx="7" fill="#e0b97f" stroke="#946f4b" stroke-width="4"/><circle cx="39" cy="40" r="10" fill="#91aeb4" stroke="#5e7980" stroke-width="3"/><path d="M63 37h13" stroke="#946f4b" stroke-width="5"/>');
  if(/kalemtıraş/.test(s))return svg('<path d="M19 24h43l-5 38H24z" fill="#d6a966" stroke="#8b684a" stroke-width="4"/><ellipse cx="40" cy="42" rx="13" ry="9" fill="#657e89"/><path d="M28 54l24-23" stroke="#eef2e8" stroke-width="3"/>');
  if(/saat/.test(s))return svg('<circle cx="40" cy="39" r="29" fill="#f5edd4" stroke="#76929b" stroke-width="5"/><path d="M40 18v22l15 10" fill="none" stroke="#577981" stroke-width="5"/>');
  if(/tost/.test(s))return svg('<rect x="12" y="31" width="56" height="34" rx="8" fill="#e2b771" stroke="#987349" stroke-width="4"/><path d="M18 31v-15h44v15" fill="#f0d39b" stroke="#987349" stroke-width="4"/>');
  if(/ütü/.test(s))return svg('<path d="M8 58h64l-11 12H17z" fill="#a3c9d4" stroke="#527d88" stroke-width="4"/><path d="M22 56q2-36 29-36l10 36z" fill="#d7ebeb" stroke="#527d88" stroke-width="4"/>');
  return svg('<rect x="17" y="16" width="46" height="50" rx="8" fill="#c1d9df" stroke="#678c98" stroke-width="4"/><circle cx="40" cy="42" r="12" fill="#e5c17b"/>');
 }
 function power({r,index,state,wrong,finish,next,fast,locked}){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('power-scene');
  state.powerStations=state.powerStations||r.kutular.map(()=>[]);
  const i=state.ix||0,k=r.kartlar[i];if(!k)return;
  const stationIcons=index===0?['⚡','✋']:['▣','▥','✋'];
  const draw=()=>{
   stage.innerHTML='<div class="power-workspace"><header>ENERJİ ATÖLYESİ <small>Aracın nasıl çalıştığını incele ve istasyona götür</small></header><div class="power-bench"><button class="power-object" data-sinif-kart="1" aria-label="'+esc(k.t)+'">'+appliance(k.t)+'<span>'+esc(k.t)+'</span></button><div class="power-stations power-stations-'+r.kutular.length+'">'+r.kutular.map((b,j)=>{
    const name=typeof b==='string'?b:b.ad,alt=typeof b==='string'?'':b.alt,items=state.powerStations[j];
    return '<button class="power-station power-station-'+j+' '+(state.powerFresh===j?'power-connected':'')+'" data-kutu="'+j+'" aria-label="'+esc(name)+' enerji istasyonu"><span class="power-station-symbol" aria-hidden="true">'+stationIcons[j]+'</span><strong>'+esc(name)+'</strong><small>'+esc(alt)+'</small><span class="power-shelf">'+items.map((x,n)=>'<span class="power-mini '+(state.powerFresh===j&&n===items.length-1?'power-arrive':'')+'" title="'+esc(x)+'">'+appliance(x)+'</span>').join('')+'</span><span class="power-count">'+items.length+' araç</span></button>';
   }).join('')+'</div></div><p class="power-feedback" role="status">'+esc(state.not||'Aracın çalışması için hangi enerji gerekir?')+'</p></div>';
   task.innerHTML='<p class="power-help">'+(i+1)+' / '+r.kartlar.length+' araç · Aracı sahnedeki uygun istasyona sürükle veya seçip dokun.</p>';
   const source=stage.querySelector('[data-sinif-kart]');source.onclick=()=>{state.powerSelected=!state.powerSelected;source.classList.toggle('selected',state.powerSelected)};
   stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>{if(state.powerSelected)place(+b.dataset.kutu)});
   SceneWorkshop.bindDrag('[data-sinif-kart]','[data-kutu]',(_,b)=>place(+b.dataset.kutu));state.powerFresh=null;
  };
  const place=j=>{if(locked()||state.gecis||state.powerComplete)return;
   if(j!==k.dogru)return wrong(k.hint||r.ipucu);
   state.powerStations[j].push(k.t);state.sayim[j]++;state.ix=i+1;state.not=k.neden||'';state.powerFresh=j;state.powerSelected=false;
   draw();stage.querySelector('[data-sinif-kart]').disabled=true;
   next(()=>{if(state.ix>=r.kartlar.length){state.powerComplete=true;finish()}else power({r,index,state,wrong,finish,next,fast,locked})},fast?30:850);
  };draw();
 }
 return {book,power};
})();
