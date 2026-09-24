/* Z33: bağlaç, kategori kutusuna değil cümlenin gerçek boşluğuna girer. */
window.SceneConjunctionPress=(()=>{
 const esc=SceneWorkshop.escape;
 function render({r,state,wrong,finish,next,fast,locked}){
  const i=state.ix||0,k=r.kartlar[i];if(!k)return;
  const stage=document.querySelector('#stage'),task=document.querySelector('#task'),scene=document.querySelector('.scene');scene.classList.add('conjunction-scene');
  const parts=k.t.split('«___»');
  const sentence=selected=>parts.length===2?`${esc(parts[0])}<span class="conjunction-slot ${selected?'conjunction-filled':''}" data-sentence-slot="1" aria-label="Cümledeki boşluk">${selected?esc(selected):'___'}</span>${esc(parts[1])}`:esc(k.t);
  const draw=selected=>{stage.innerHTML=`<div class="conjunction-press"><header>BAĞLAÇ MATBAASI <small>Cümle ${i+1} / ${r.kartlar.length}</small></header><div class="conjunction-roller" aria-hidden="true"><i></i><span>⌁</span><i></i></div><div class="conjunction-paper"><span class="conjunction-paper-title">CÜMLE ŞERİDİ</span><p>${sentence(selected)}</p></div><div class="conjunction-word-bank"><strong>SÖZCÜK HARFLERİ</strong><div>${r.kutular.map((word,j)=>`<button class="conjunction-word" data-kutu="${j}" aria-label="${esc(word)} bağlacını boşluğa yerleştir" ${selected?'disabled':''}>${esc(word)}</button>`).join('')}</div></div><p class="conjunction-result" role="status">${esc(selected?k.neden||'Sözcük cümleye yerleşti.':state.not||'Bağlacı tutup cümledeki boşluğa bırak.')}</p></div>`};
  draw(null);task.innerHTML='<p class="conjunction-guide">Bağlacı cümle şeridindeki boşluğa sürükle. Dokunarak da yerleştirebilirsin.</p>';
  const insert=j=>{if(locked()||state.gecis||state.conjunctionFilled)return;if(j!==k.dogru)return wrong(k.hint||'İki bölüm arasındaki anlam ilişkisini düşün.');state.conjunctionFilled=true;state.sayim[j]++;state.ix=i+1;state.not=k.neden||'';draw(r.kutular[j]);next(()=>{state.conjunctionFilled=false;if(state.ix>=r.kartlar.length)finish();else render({r,state,wrong,finish,next,fast,locked})},fast?30:820)};
  stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>insert(+b.dataset.kutu));
  SceneWorkshop.bindDrag('[data-kutu]','[data-sentence-slot]',(source)=>insert(+source.dataset.kutu));
 }
 return {render};
})();
