/* İki ayrı deney: besin numunesi analiz tüpüne, gözlem Dünya modeline girer. */
window.SceneNutritionEarth = (() => {
  const esc = SceneWorkshop.escape;
  const foods = {
    'Haşlanmış yumurta':'🥚', Pilav:'🍚', 'Zeytinyağı':'🫒', Portakal:'🍊',
    'Tavuk göğsü':'🍗', Ekmek:'🍞'
  };
  const vessels = [
    {icon:'●',tone:'protein',label:'PROTEİN',apparatus:'Kas yapı taşı'},
    {icon:'▤',tone:'carb',label:'KARBONHİDRAT',apparatus:'Enerji deposu'},
    {icon:'◕',tone:'fat',label:'YAĞ',apparatus:'Yağ damlası'},
    {icon:'✦',tone:'vitamin',label:'VİTAMİN ve MİNERAL',apparatus:'Koruyucu içerik'}
  ];
  const regions = [
    {icon:'☁',tone:'air',label:'HAVA KÜRE'},
    {icon:'≈',tone:'water',label:'SU KÜRE'},
    {icon:'▲',tone:'rock',label:'TAŞ KÜRE'},
    {icon:'♣',tone:'life',label:'CANLI KÜRE'}
  ];
  function nutrition(k, state, i, total) {
    const seen = state.scenePlaced;
    return `<div class="nutrition-lab"><header><b>BESİN ANALİZ TEZGÂHI</b><span>Numune ${i+1} / ${total}</span></header>
      <div class="nutrition-sample"><div class="nutrition-plate" aria-hidden="true"><span>${seen===null?(foods[k.t]||'🍽'):''}</span></div>
        <div class="nutrition-label"><small>PAKET / GÖZLEM ETİKETİ</small><strong>${esc(k.t)}</strong><p>${esc(k.gozlem||'İçerik etiketini incele.')}</p></div></div>
      <div class="nutrition-instruction">Numuneyi baskın içeriğin analiz kabına bırak.</div>
      <div class="nutrition-apparatus">${vessels.map((v,j)=>`<div class="nutrition-vessel ${v.tone}${seen===j?' nutrition-reacting':''}"><span class="nutrition-vessel-name">${esc(v.label)}</span><button class="nutrition-glass" data-kutu="${j}" aria-label="${esc(v.label)} analiz kabının içine bırak"><span class="nutrition-liquid"></span><span class="nutrition-symbol">${v.icon}</span>${seen===j?`<span class="nutrition-arrival">${foods[k.t]||'●'}</span>`:''}</button><span class="nutrition-vessel-foot">${v.apparatus}</span><span class="nutrition-count">${(state.sayim||[])[j]||0} analiz</span></div>`).join('')}</div>
      <p class="nutrition-result" role="status">${seen!==null?esc(k.neden||'Numune kaba yerleşti.'):esc(state.not||'')}</p></div>`;
  }
  function earth(k, state, i, total) {
    const seen=state.scenePlaced;
    return `<div class="earth-observatory"><header><b>DÜNYA GÖZLEM MODELİ</b><span>Gözlem ${i+1} / ${total}</span></header>
      <div class="earth-model"><div class="earth-halo" aria-hidden="true"></div><div class="earth-globe">
      ${regions.map((v,j)=>`<button class="earth-region ${v.tone}${seen===j?' earth-lit':''}" data-kutu="${j}" aria-label="Dünya modelinde ${esc(v.label)} bölgesi"><span class="earth-region-icon">${v.icon}</span><strong>${esc(v.label)}</strong>${seen===j?`<span class="earth-arrival">${esc(k.t)}</span>`:''}<small>${(state.sayim||[])[j]||0}</small></button>`).join('')}</div></div>
      <p class="earth-result" role="status">${seen!==null?esc(k.neden||'Gözlem Dünya modeline yerleşti.'):esc(state.not||'Kartı seçip Dünya modelindeki bölgeye bırak.')}</p></div>`;
  }
  function render({id,r,state,wrong,finish,next,fast,locked}) {
    const i=state.ix||0,k=r.kartlar[i];if(!k)return;
    state.scenePlaced=null;state.sceneSelected=false;
    const nutritionScene=id==='f07';
    const scene=document.querySelector('.scene'),stage=document.querySelector('#stage'),task=document.querySelector('#task');
    scene.classList.remove('nutrition-scene','earth-scene');scene.classList.add(nutritionScene?'nutrition-scene':'earth-scene');
    stage.innerHTML=nutritionScene?nutrition(k,state,i,r.kartlar.length):earth(k,state,i,r.kartlar.length);
    task.innerHTML=`<button class="scene-source ${nutritionScene?'food-source':'observation-source'}" data-sinif-kart="1" data-scene-source="1" aria-label="${esc(k.t)}; seç veya sürükle">${nutritionScene?`<span class="food-source-icon">${foods[k.t]||'🍽'}</span>`:'<span class="earth-source-mark">◉</span>'}<span>${esc(k.t)}</span><span class="source-grip" aria-hidden="true">⠿</span></button><p class="scene-source-help">${nutritionScene?'Besini analiz kabına':'Gözlem kartını Dünya modeline'} sürükle. Dokunarak seçip hedefe dokunabilirsin.</p>`;
    const source=task.querySelector('[data-scene-source]');
    const place=j=>{
      if(locked()||state.gecis||state.scenePlaced!==null||!state.sceneSelected)return;
      if(j!==k.dogru)return wrong(k.hint||'Gözlemi yeniden incele.');
      state.scenePlaced=j;state.sceneSelected=false;
      state.sayim=state.sayim||r.kutular.map(()=>0);state.sayim[j]++;
      state.ix=i+1;state.not=k.neden||'';
      source.disabled=true;source.classList.remove('selected');source.hidden=true;
      stage.innerHTML=nutritionScene?nutrition(k,state,i,r.kartlar.length):earth(k,state,i,r.kartlar.length);
      if(state.ix>=r.kartlar.length)next(finish,fast?30:850);
      else next(()=>render({id,r,state,wrong,finish,next,fast,locked}),fast?30:850);
    };
    source.onclick=()=>{if(locked()||state.gecis)return;state.sceneSelected=!state.sceneSelected;source.classList.toggle('selected',state.sceneSelected)};
    stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>place(+b.dataset.kutu));
    SceneWorkshop.bindDrag('[data-scene-source]','#stage [data-kutu]',(el,target)=>{state.sceneSelected=true;place(+target.dataset.kutu)});
  }
  return {render};
})();
