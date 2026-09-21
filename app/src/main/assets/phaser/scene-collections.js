/* Dil, doğa ve günlük alışkanlıklar için farklı toplama yüzeyleri. */
window.SceneCollections=(()=>{
 const esc=SceneWorkshop.escape;
 const svg=body=>`<svg viewBox="0 0 100 80" aria-hidden="true" focusable="false">${body}</svg>`;
 function specimen(text){
  const t=text.toLocaleLowerCase('tr');
  if(/kaplumbağa/.test(t))return svg('<ellipse cx="51" cy="46" rx="28" ry="19" fill="#759563" stroke="#42614e" stroke-width="3"/><path d="M28 57l-8 10m25-6l-5 11m26-12l8 8M45 31v29m-19-15h53" stroke="#42614e" stroke-width="4"/><ellipse cx="84" cy="46" rx="10" ry="8" fill="#a9ba70"/><circle cx="88" cy="44" r="2"/>');
  if(/^arı(?:\s|—|$)/.test(t))return svg('<ellipse cx="42" cy="25" rx="13" ry="19" fill="#d5ecf0"/><ellipse cx="64" cy="25" rx="13" ry="19" fill="#d5ecf0"/><ellipse cx="49" cy="48" rx="27" ry="18" fill="#e9ba4d" stroke="#806c3b" stroke-width="3"/><path d="M38 34v29m17-29v30" stroke="#5b5547" stroke-width="7"/><circle cx="79" cy="42" r="12" fill="#e9ba4d"/><circle cx="83" cy="39" r="2"/>');
  if(/balık/.test(t))return svg('<path d="M23 41Q57 10 79 41Q54 75 23 41L7 22v40z" fill="#69a7b7" stroke="#3c6e85" stroke-width="3"/><circle cx="66" cy="35" r="3" fill="#244450"/><path d="M45 25l14 17-15 17" fill="#e2b76b"/>');
  if(/mercan/.test(t))return svg('<path d="M47 72V22m0 30L24 37V15m0 22L11 27m37 13l25-13V9m-1 18l17-8m-42 45l29-13" fill="none" stroke="#d88079" stroke-width="9" stroke-linecap="round"/>');
  if(/deniz yıldızı/.test(t))return svg('<path d="M50 5l11 25 29 3-23 19 6 25-24-16-24 16 8-26L11 34l28-4z" fill="#d99268" stroke="#9f604e" stroke-width="3"/><g fill="#e9bd89"><circle cx="50" cy="39" r="4"/><circle cx="48" cy="21" r="3"/><circle cx="33" cy="41" r="3"/><circle cx="65" cy="42" r="3"/><circle cx="43" cy="57" r="3"/><circle cx="60" cy="57" r="3"/></g>');
  if(/sünger/.test(t))return svg('<path d="M14 70L21 25q11-14 23 0l-3 45m0 0l6-49q10-18 24-2l5 51z" fill="#d5b061" stroke="#a3824e" stroke-width="3"/><g fill="#997e45"><ellipse cx="33" cy="26" rx="7" ry="4"/><ellipse cx="60" cy="22" rx="7" ry="4"/><circle cx="59" cy="41" r="3"/><circle cx="32" cy="53" r="4"/><circle cx="61" cy="59" r="4"/></g>');
  if(/şapkalı/.test(t))return svg('<path d="M40 38h20l6 34H34z" fill="#e8ddbd" stroke="#aa9b79" stroke-width="3"/><path d="M10 42Q15 2 50 9Q87 7 93 42z" fill="#c88b69" stroke="#965f4d" stroke-width="3"/><g fill="#f2ddbc"><circle cx="32" cy="28" r="5"/><circle cx="59" cy="22" r="5"/><circle cx="73" cy="35" r="4"/></g>');
  if(/küf|tüylü/.test(t))return svg('<rect x="10" y="27" width="80" height="43" rx="10" fill="#e9cda2" stroke="#a68d64" stroke-width="3"/><g fill="#829987" stroke="#567866" stroke-width="2"><circle cx="42" cy="42" r="12"/><circle cx="59" cy="45" r="10"/><circle cx="49" cy="58" r="8"/></g><path d="M29 31l-7-7m15 7v-12m20 13l8-12m-4 31l12 2" stroke="#a2b4a3" stroke-width="2"/>');
  if(/hamuru|maya/.test(t))return svg('<circle cx="50" cy="39" r="34" fill="#eff3dc" stroke="#81959c" stroke-width="5"/><g fill="#d3b593" stroke="#8a705b" stroke-width="2"><ellipse cx="35" cy="32" rx="9" ry="13"/><ellipse cx="59" cy="48" rx="10" ry="14"/><ellipse cx="69" cy="33" rx="5" ry="7"/></g>');
  if(/yosun/.test(t))return svg('<path d="M7 67h86v10H7z" fill="#9dd2d4"/><path d="M34 68q-21-24-8-47m25 47q24-36 6-53m12 54q20-14 14-37" stroke="#6aa16c" stroke-width="9" fill="none" stroke-linecap="round"/>');
  if(/çam/.test(t))return svg('<path d="M45 50h11v26H45z" fill="#896b4b"/><path d="M50 4L23 32h12L14 55h72L65 32h12z" fill="#5d997a" stroke="#356c58" stroke-width="3"/>');
  if(/kavak/.test(t))return svg('<path d="M46 34h8v44h-8z" fill="#967658"/><ellipse cx="50" cy="31" rx="20" ry="28" fill="#89ab67" stroke="#5a824c" stroke-width="3"/>');
  return svg(`<path d="M50 35v40m0-17Q22 30 22 52q0 14 28 11m0-10q28-30 28-9 0 14-28 17" fill="#7ea26c" stroke="#548655" stroke-width="3"/><g fill="${/gül/.test(t)?'#d78795':'#e8bb53'}">${Array.from({length:8},(_,i)=>`<ellipse cx="${50+17*Math.cos(i*Math.PI/4)}" cy="${25+17*Math.sin(i*Math.PI/4)}" rx="8" ry="9"/>`).join('')}</g><circle cx="50" cy="25" r="10" fill="#86674c"/>`);
 }
 function habit(text){
  if(/ellerini/.test(text))return svg('<path d="M10 50h80l-8 20H20z" fill="#b4d9dc" stroke="#688c9b" stroke-width="3"/><path d="M61 36V14H40v13" fill="none" stroke="#6b8795" stroke-width="7"/><path d="M41 32v17m7-15v13" stroke="#75b9d9" stroke-width="3"/><path d="M25 51q20-21 34 0" stroke="#dda77c" stroke-width="13" fill="none"/>');
  if(/dişlerini/.test(text))return svg('<path d="M28 12q12-7 22 0 12-7 22 0 12 14-4 42-8 23-15-1-4-13-10 2-10 25-19-4-13-24 4-39" fill="#fffdf0" stroke="#98b0b9" stroke-width="3"/><path d="M10 61l68-40" stroke="#d08e83" stroke-width="7"/><path d="M69 17l9 10m-5-15l10 10" stroke="#7caeb7" stroke-width="4"/>');
  if(/ekrana/.test(text))return svg('<rect x="12" y="16" width="76" height="47" rx="4" fill="#506d84"/><rect x="18" y="22" width="64" height="34" fill="#a8c6d8"/><path d="M50 63v8m-18 2h36" stroke="#506d84" stroke-width="5"/><path d="M69 22q-10 8 0 16-17 0-15-13z" fill="#eee1ab"/>');
  if(/koşup/.test(text))return svg('<circle cx="52" cy="15" r="9" fill="#d4a278"/><path d="M49 28l-10 22m6-14l-21 4m21-8l19 11 14-9m-39 16l20 7 9 17m-27-23L26 70H13" fill="none" stroke="#538b9b" stroke-width="8" stroke-linecap="round"/>');
  if(/içecek/.test(text))return svg('<path d="M28 17h45l-7 57H35z" fill="#d6b279" stroke="#916f4f" stroke-width="3"/><path d="M49 50L60 8h18" stroke="#b2706f" stroke-width="5" fill="none"/><rect x="35" y="29" width="30" height="16" rx="4" fill="#fbedd8"/>');
  return svg('<ellipse cx="49" cy="48" rx="36" ry="23" fill="#e8f1ea" stroke="#8ca4a5" stroke-width="3"/><ellipse cx="49" cy="48" rx="24" ry="14" fill="#f7efd7"/><path d="M23 26l48 38" stroke="#c9766b" stroke-width="5"/>');
 }
 function wordPair(text){const pair=text.split('\n')[0];return `<div class="word-pair"><span>${esc(pair)}</span><small>${esc(text.split('\n').slice(1).join(' '))}</small></div>`}
 function render({id,r,state,wrong,finish,next,fast,locked}){
  const kind=id==='g07'?'nature':id==='z10'?'library':'habits';
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');
  document.querySelector('.scene').classList.add('collection-scene',`collection-${kind}`);
  const i=state.ix||0,k=r.kartlar[i];if(!k)return;
  state.collections=state.collections||r.kutular.map(()=>[]);
  const visual=t=>kind==='nature'?specimen(t):kind==='habits'?habit(t):wordPair(t);
  stage.innerHTML=`<div class="collection-workspace"><header>${kind==='nature'?'DOĞA KOLEKSİYONU':kind==='library'?'SÖZCÜK KÜTÜPHANESİ':'GÜNLÜK ALIŞKANLIK PANOM'}<small>${i+1} / ${r.kartlar.length}</small></header><div class="collection-targets">${r.kutular.map((b,j)=>{
   const ad=typeof b==='string'?b:b.ad;
   return `<button class="collection-target" data-kutu="${j}" aria-label="${esc(ad)}"><strong>${esc(ad)}</strong>${kind==='library'?'<div class="shelf-arch"></div>':''}<div class="collection-content">${state.collections[j].map(t=>`<span class="collected">${visual(t)}<small>${esc(t.split('—')[0].split('.')[0].slice(0,45))}</small></span>`).join('')}${!state.collections[j].length?'<span class="collection-empty" aria-hidden="true">＋</span>':''}</div><span class="collection-count">${state.sayim[j]||0} ${kind==='nature'?'örnek':kind==='library'?'sözcük çifti':'alışkanlık'}</span></button>`;
  }).join('')}</div><p class="collection-reason" role="status">${esc(state.not||r.ipucu||'')}</p></div>`;
  task.innerHTML=`<button class="collection-source" data-sinif-kart="1" aria-label="${esc(k.t)}">${visual(k.t)}${kind==='library'?'':`<span>${esc(k.t)}</span>`}</button><p class="collection-guide">${kind==='nature'?'Örneği koleksiyondaki grubuna':kind==='library'?'Sözcük çiftini kütüphanedeki rafına':'Alışkanlığı panodaki yerine'} sürükle. İstersen hedefine dokun.</p>`;
  const place=j=>{
   if(locked()||state.gecis)return;if(j!==k.dogru)return wrong(k.hint||r.ipucu||'Ölçütü yeniden düşün.');
   state.collections[j].push(k.t);state.sayim[j]++;state.ix=i+1;state.not=k.neden||'';
   const target=stage.querySelector(`[data-kutu="${j}"]`);target.querySelector('.collection-empty')?.remove();
   target.querySelector('.collection-content').insertAdjacentHTML('beforeend',`<span class="collected collection-arrival">${visual(k.t)}<small>${esc(k.t.split('—')[0].split('.')[0].slice(0,45))}</small></span>`);
   target.querySelector('.collection-count').textContent=state.sayim[j]+' '+(kind==='nature'?'örnek':kind==='library'?'sözcük çifti':'alışkanlık');
   stage.querySelector('.collection-reason').textContent=state.not;task.querySelector('.collection-source').disabled=true;
   next(()=>{if(state.ix>=r.kartlar.length)finish();else render({id,r,state,wrong,finish,next,fast,locked})},fast?30:850);
  };
  stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>place(+b.dataset.kutu));
  task.querySelector('.collection-source').onclick=()=>task.querySelector('.collection-source').classList.toggle('selected');
  SceneWorkshop.bindDrag('[data-sinif-kart]','[data-kutu]',(_,b)=>place(+b.dataset.kutu));
 }
 return {render,specimen,habit};
})();
