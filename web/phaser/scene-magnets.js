/* İki mıknatıs deneyi: önce gerçek nesneyi yaklaştır, sonra gözlemi kaydet. */
window.SceneMagnets=(()=>{
 const esc=SceneWorkshop.escape,svg=b=>'<svg viewBox="0 0 100 80" aria-hidden="true" focusable="false">'+b+'</svg>';
 const bar=(left,right)=>svg('<rect x="2" y="24" width="48" height="32" rx="3" fill="'+(left==='N'?'#b75550':'#3d799d')+'"/><rect x="50" y="24" width="48" height="32" rx="3" fill="'+(right==='N'?'#b75550':'#3d799d')+'"/><g fill="white" font-size="19" font-weight="bold" text-anchor="middle"><text x="26" y="47">'+left+'</text><text x="74" y="47">'+right+'</text></g>');
 function sample(i){
  const drawings=[
   '<path d="M15 35h60l13 5-13 5H15z" fill="#95a9b4" stroke="#466173" stroke-width="3"/><path d="M15 26v28" stroke="#466173" stroke-width="7"/>',
   '<ellipse cx="28" cy="40" rx="21" ry="13" fill="#eacdaa" stroke="#a68461" stroke-width="3"/><path d="M48 40h40" stroke="#eacdaa" stroke-width="10"/>',
   '<path d="M69 24H28q-19 0-19 17t19 17h45q19 0 19-17T73 24H34q-10 0-10 10t10 10h36" fill="none" stroke="#78919e" stroke-width="6"/>',
   '<path d="M24 12h52L66 69H34z" fill="#d9eff3" stroke="#588b9f" stroke-width="3"/><path d="M34 23l5 30" stroke="white" stroke-width="5"/>',
   '<path d="M18 16l56-5 13 19-7 36-57 4-11-20z" fill="#c1c8cc" stroke="#78858b" stroke-width="3"/><path d="M18 16l28 19 28-24M46 35L23 70m23-35l34 31m-34-31l41-5" fill="none" stroke="#eef2f3" stroke-width="3"/>',
   '<path d="M9 48q10-44 24 0t25-1 30-12" fill="none" stroke="#b77549" stroke-width="7"/>',
   '<circle cx="50" cy="40" r="29" fill="#b8c5ca" stroke="#627c89" stroke-width="4"/><circle cx="50" cy="40" r="23" fill="none" stroke="#edf1eb" stroke-width="2"/><text x="50" y="48" text-anchor="middle" font-size="23" fill="#39576a">Ni</text>',
   '<path d="M12 43l14-10h59v14H26z" fill="#dfb654" stroke="#97763a" stroke-width="3"/><path d="M12 43l14-10v14z" fill="#dcc6a1"/><path d="M12 43l7-5v7z" fill="#384858"/>'
  ];return svg(drawings[i]);
 }
 function render({id,r,state,wrong,finish,next,fast,locked}){
  const i=state.ix||0,k=r.kartlar[i];if(!k)return;
  const poles=id==='f26',pair=k.sahneEk||'NN';
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('magnet-scene',poles?'magnet-poles':'magnet-materials');
  state.magnetPhase='ready';state.magnetSelected=false;
  const left=poles?bar(pair[0]==='N'?'S':'N',pair[0]):bar('S','N');
  const item=poles?bar(pair[1],pair[1]==='N'?'S':'N'):sample(i);
  stage.innerHTML='<div class="magnet-workbench"><header>'+ (poles?'KUTUP DENEYİ':'MIKNATIS TEST TEZGÂHI')+'<small>Deney '+(i+1)+' / '+r.kartlar.length+'</small></header><p class="magnet-object-name">'+esc(k.t)+'</p><div class="magnet-apparatus"><div class="magnet-track" aria-hidden="true"></div><button class="magnet-fixed" data-magnet-target aria-label="Sabit mıknatısın ucu">'+left+'</button><button class="magnet-sample" data-magnet-source aria-label="'+esc(poles?'Hareketli mıknatıs':k.t)+'">'+item+'</button><span class="magnet-fixed-note">Sabit mıknatıs</span><span class="magnet-motion-note" aria-hidden="true">← Yaklaştır</span></div><p class="magnet-status" role="status">Nesneyi tutup soldaki mıknatısın ucuna yaklaştır.</p><div class="magnet-records"><strong>DENEY DEFTERİ</strong><ol>'+ (state.magnetRecords||[]).map(x=>'<li>'+esc(x)+'</li>').join('')+'</ol></div></div>';
  task.innerHTML='<div class="magnet-observation"><p>Gözlemden sonra sonucu seç:</p><div>'+r.kutular.map((b,j)=>'<button data-observation-answer data-kutu="'+j+'" disabled>'+esc(b)+'</button>').join('')+'</div><button class="magnet-repeat" data-magnet-repeat disabled>Deneyi tekrar yap</button></div><p class="magnet-help">Sürükle veya nesneyi seçip mıknatısa dokun. Bu bir ekran modelidir.</p>';
  const source=stage.querySelector('[data-magnet-source]'),target=stage.querySelector('[data-magnet-target]'),status=stage.querySelector('.magnet-status');
  task.querySelector('[data-magnet-repeat]').onclick=()=>{if(!locked()&&!state.gecis&&state.magnetPhase==='observed')render({id,r,state,wrong,finish,next,fast,locked})};
  const conduct=()=>{
   if(locked()||state.gecis||state.magnetPhase!=='ready')return;
   state.magnetPhase='moving';state.magnetSelected=false;source.classList.remove('selected');source.disabled=true;target.disabled=true;
   const motion=poles?(k.dogru===0?'repel':'attract'):(k.dogru===0?'attract':'still');
   source.classList.add('magnet-'+motion);stage.querySelector('.magnet-motion-note').textContent='';
   status.textContent='Hareketi gözle…';
   next(()=>{state.magnetPhase='observed';status.textContent=motion==='repel'?'Mıknatıslar birbirinden uzaklaştı.':motion==='attract'?'Nesne mıknatısa doğru hareket etti.':'Nesne mıknatısa doğru hareket etmedi.';
    task.querySelectorAll('[data-kutu],[data-magnet-repeat]').forEach(b=>b.disabled=false);
   },fast?20:1000);
  };
  source.onclick=()=>{if(state.magnetPhase!=='ready')return;state.magnetSelected=!state.magnetSelected;source.classList.toggle('selected',state.magnetSelected)};
  target.onclick=()=>{if(state.magnetSelected)conduct()};
  SceneWorkshop.bindDrag('[data-magnet-source]','[data-magnet-target]',conduct);
  task.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>{
   if(locked()||state.gecis||state.magnetPhase!=='observed')return;
   const j=+b.dataset.kutu;if(j!==k.dogru)return wrong('Nesnenin hareketini yeniden düşün: yaklaştı mı, uzaklaştı mı, yerinde mi kaldı?');
   state.magnetPhase='recorded';state.sayim[j]++;state.ix=i+1;state.vurgu=k.vurgu||'';state.not=k.neden;
   state.magnetRecords=state.magnetRecords||[];state.magnetRecords.push(k.t+' → '+r.kutular[j]);
   stage.querySelector('.magnet-records ol').insertAdjacentHTML('beforeend','<li class="magnet-ink">'+esc(state.magnetRecords.at(-1))+'</li>');
   status.textContent=k.neden;task.querySelectorAll('[data-kutu],[data-magnet-repeat]').forEach(x=>x.disabled=true);
   next(()=>{if(state.ix>=r.kartlar.length)finish();else render({id,r,state,wrong,finish,next,fast,locked})},fast?20:1000);
  });
 }
 return {render,sample,bar};
})();
