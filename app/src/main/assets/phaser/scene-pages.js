/* Sözcük kartları hedef değil; yazı doğrudan yayın/dilekçe sayfasına oturur. */
window.ScenePages=(()=>{
 const esc=SceneWorkshop.escape;
 function render({id,r,state,wrong,finish,locked}){
  const letter=id==='y58',planning=r.kind==='kule';
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('page-scene',letter?'page-letter':'page-magazine');
  state.pageMatches={};state.done=0;state.placed={};state.slots=planning?Array(r.order.length).fill(null):[];
  const slots=planning?r.order.map((pid,i)=>({key:String(i),pid})):
   (letter?['t1','t2','t3','t4']:['t4','t1','t2','t3']).map(tid=>({key:tid,pid:r.pieces.find(p=>p.target===tid).id}));
  const parts=planning?r.cards.map(c=>({id:c.id,html:esc(c.label)})):r.pieces;
  const labels=letter?['Tarih','Makam','İstek metni','İmza bölümü']:['Başlık','Giriş','Gelişme','Sonuç'];
  const tree='<svg viewBox="0 0 240 55" aria-hidden="true"><path d="M0 50Q70 10 130 38T240 30V55H0" fill="#bfd2ab"/><g fill="#4f8064"><path d="M35 2L14 40h42zM92 6L73 40h39zM180 0l-22 40h43z"/></g><path d="M35 33v20m57-20v20m88-20v20" stroke="#7e684b" stroke-width="5"/></svg>';
  const draw=()=>{
   stage.innerHTML='<div class="page-desk"><header>'+ (letter?'DİLEKÇE MASASI':'DOĞA DERGİSİ · YAZI İŞLERİ')+'</header><div class="working-paper">'+(letter?'<span class="paper-clip" aria-hidden="true"></span><p class="paper-example">Örnek çalışma · kişisel bilgi yazma</p>':'<div class="magazine-masthead">DOĞANIN SESİ <small>Okul dergisi · örnek sayfa</small></div>')+slots.map((s,i)=>{
    const piece=parts.find(p=>p.id===state.pageMatches[s.key]),fresh=state.pageFresh===s.key;
    return '<button class="page-slot page-slot-'+i+'" '+(planning?'data-slot="'+s.key+'"':'data-target="'+s.key+'"')+' aria-label="'+esc(planning?'Sayfanın '+(i+1)+'. bölümü':labels[i])+'"><span class="page-slot-label">'+(planning?(i+1)+'. bölüm':labels[i])+'</span><span class="page-content '+(fresh?'page-ink':'')+'">'+(piece?piece.html:'<i class="paper-lines" aria-hidden="true"></i>')+'</span></button>'+(!letter&&i===0?tree:'');
   }).join('')+'<footer>'+ (letter?'Bu sayfa yalnız öğrenme amaçlı bir örnektir.':'1 · Doğayı tanı, anlat, koru.')+'</footer></div><p class="page-progress" role="status">'+state.done+' / '+parts.length+' bölüm yerleşti</p></div>';
   task.innerHTML='<div class="page-source-tray">'+[2,0,3,1].map(i=>parts[i]).map(p=>'<button class="page-source" '+(planning?'data-card="'+p.id+'"':'data-piece="'+p.id+'"')+' '+(Object.values(state.pageMatches).includes(p.id)?'disabled':'')+'>'+p.html+'</button>').join('')+'</div><p class="page-help">Parçayı kâğıttaki yerine sürükle. İstersen parçayı seçip sayfadaki yerine dokun.</p>';
   const source=planning?'[data-card]':'[data-piece]',target=planning?'[data-slot]':'[data-target]';
   const pid=e=>planning?e.dataset.card:e.dataset.piece,tid=e=>planning?e.dataset.slot:e.dataset.target;
   task.querySelectorAll(source).forEach(b=>b.onclick=()=>{if(locked()||state.pageComplete)return;state.pageSelected=pid(b);task.querySelectorAll(source).forEach(x=>x.classList.toggle('selected',x===b))});
   stage.querySelectorAll(target).forEach(b=>b.onclick=()=>{if(state.pageSelected)place(state.pageSelected,tid(b))});
   SceneWorkshop.bindDrag(source+':not(:disabled)',target,(a,b)=>place(pid(a),tid(b)));
   state.pageFresh=null;
  };
  const place=(pid,key)=>{
   if(locked()||state.pageComplete||Object.values(state.pageMatches).includes(pid)||state.pageMatches[key])return;
   const s=slots.find(s=>s.key===key);if(!s)return;
   if(s.pid!==pid)return wrong(r.hint);
   state.pageMatches[key]=pid;state.done++;state.placed[key]=1;if(planning)state.slots[+key]=pid;state.pageSelected=null;state.pageFresh=key;draw();
   if(state.done===parts.length){state.pageComplete=true;finish(r)}
  };draw();
 }
 return {render};
})();
