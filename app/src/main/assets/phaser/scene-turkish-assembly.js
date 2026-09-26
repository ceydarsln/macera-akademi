/* Scene connections, scoped to the audited first-grade Turkish games.
 * Existing answer/phase/speech handlers remain the authority for pedagogy. */
(() => {
 const ids=['t02','t04','t06','t07','t09','t14','t21','t22','t30','t38','t46','t47','t48','t51','t54','t62','t64'];
 if(!ids.includes(GAME_ID))return;
 document.body.classList.add('connected-turkish');
 document.documentElement.classList.add('connected-turkish-root');
 const titles={t04:'SES VAGONLARI',t14:'İLK HECE İSTASYONU',t21:'HECE EKSPRESİ',t30:'DAĞ TRENİ',t38:'GECE TRENİ',t46:'BEŞİNCİ HECE İSTASYONU',t06:'MIKNATISLI UZAY GEMİSİ',t22:'HECE KAPSÜLÜ',t48:'UZAYDA SES BİRLEŞİMİ',t07:'KELİME ÜRETİM BANDI',t47:'MEYVE PAKETLEME ATÖLYESİ',t51:'UZUN KELİME PRESİ',t54:'CÜMLE MATBAASI',t64:'CÜMLE BAHÇESİ'};
 function node(cls,html=''){const e=document.createElement('div');e.className=cls;e.innerHTML=html;return e}
 function bridge(button,targetSelector,onDrop){
  const click=button.onclick;let skip=false,start=null,ghost=null;
  button.onclick=e=>{if(skip){skip=false;return}if(!locked&&!state.gecis&&!button.disabled)click?.(e)};
  button.style.touchAction='none';
  button.onpointerdown=e=>{
   if(e.button!==0||locked||state.gecis||button.disabled)return;
   skip=false;start={x:e.clientX,y:e.clientY};button.setPointerCapture(e.pointerId);window.addEventListener('pointerup',button.onpointerup);window.addEventListener('pointercancel',button.onpointercancel);
  };
  button.onpointermove=e=>{
   if(!start||Math.hypot(e.clientX-start.x,e.clientY-start.y)<8&&!ghost)return;
   if(!ghost){ghost=button.cloneNode(true);for(const a of [...ghost.attributes])if(a.name==='id'||a.name.startsWith('data-'))ghost.removeAttribute(a.name);ghost.className='assembly-ghost';ghost.setAttribute('aria-hidden','true');document.body.append(ghost)}
   ghost.style.left=e.clientX+'px';ghost.style.top=e.clientY+'px';
  };
  function clear(){ghost?.remove();ghost=null;start=null;window.removeEventListener('pointerup',button.onpointerup);window.removeEventListener('pointercancel',button.onpointercancel)}
  button.onpointercancel=()=>{skip=true;clear()};
  button.onlostpointercapture=()=>{if(start){skip=true;clear()}};
  button.onpointerup=e=>{
   if(!start)return;const dragged=!!ghost;skip=dragged;
   const target=dragged?document.elementFromPoint(e.clientX,e.clientY)?.closest(targetSelector):null;
   clear();if(!dragged)return;
   if(target&&!locked&&!state.gecis)onDrop(target,()=>click?.(e));
  };
 }
 function assembly(r,kind){
  const a=asama(r),stage=$('#stage'),slots=[...stage.querySelectorAll('.vagon')];
  const captions=[...stage.querySelectorAll('.caption')],context=stage.querySelector('.metin-kart');
  const produced=kind==='factory'?state.uretildi:!!state.kuruldu;
  const out=kind==='factory'?a.kelime:state.kuruldu;
  const world=node(`assembly-world ${kind}-assembly assembly-${GAME_ID}${produced?' assembled':''}`,`<header>${titles[GAME_ID]}</header>`);
  const machine=node('assembly-machine');
  if(kind==='train')machine.append(node('assembly-engine','<span class="engine-chimney"></span><span class="engine-window"></span><span class="engine-boiler"></span>'));
  if(kind==='space')machine.append(node('capsule-nose'));
  const line=node('assembly-line');
  slots.forEach((s,i)=>{const unit=node('assembly-unit'),filled=s.classList.contains('dolu'),next=s.classList.contains('aktif');s.className='scene-unit-slot'+(filled?' filled':'')+(next?' next-slot':'');s.dataset.sceneSlot=i;s.setAttribute('aria-label',(kind==='train'?'Vagon':kind==='space'?'Kapsül yuvası':'Bant kasası')+' '+(i+1)+(next?' · sıradaki boş yuva':''));unit.append(s);line.append(unit)});
  machine.append(line);
  if(kind==='space')machine.append(node('capsule-thruster'));
  world.append(machine);
  const result=node('assembly-output',produced?esc(out):'');result.setAttribute('aria-live','polite');world.append(result);
  if(a.hedefIm)world.append(node('assembly-sample',`${a.hedefIm}<small>${produced?esc(a.kelime):'Dinle ve üret'}</small>`));
  if(context){context.className='assembly-context';context.innerHTML=esc(a.baglam).replace('{K}',produced?`<span class="sentence-insert">${esc(a.kelime)}</span>`:'<span class="sentence-gap">……</span>');world.append(context)}
  captions.forEach(c=>world.append(c));stage.replaceChildren(world);
  const field=kind==='factory'?'yuva':'yer',selector=kind==='train'?'[data-ses]':kind==='space'?'[data-m]':'[data-h]';
  $$(selector).forEach(b=>bridge(b,'[data-scene-slot]',(t,commit)=>{
   const y=state[field]||a.dogru.map(()=>null),next=y.indexOf(null);
   if(+t.dataset.sceneSlot!==next)return uyar('Soldan sağa, sıradaki boş yuvaya yerleştir.');
   commit();
  }));
 }
 const train=trenCiz,space=uzayCiz,factory=fabrikaCiz;
 trenCiz=r=>{train(r);assembly(r,'train')};
 uzayCiz=r=>{space(r);assembly(r,'space')};
 fabrikaCiz=r=>{factory(r);assembly(r,'factory')};
 if(GAME_ID==='t54'){
  GAMES.t54.rounds[1].asamalar[0].baglam='{K} … yaptı.';
  GAMES.t54.rounds[1].asamalar[1].baglam='Kuşlar {K} yaptı.';
  GAMES.t54.rounds[1].result='Ürettiğin iki kelime cümleye yerleşti: Kuşlar yuva yaptı.';
 }
 function typewriter(r){
  const stage=$('#stage'),slots=stage.querySelector('.dikte-yuva'),word=stage.querySelector('.hece-kutu'),captions=[...stage.querySelectorAll('.caption')];
  const world=node('typewriter-world','<header>SİHİRLİ DAKTİLO</header>'),paper=node('typewriter-paper');
  if(slots)paper.append(slots);else if(word)paper.append(word);
  if(state.onizleme)paper.append(node('typewriter-preview',esc(asama(r).kelime)));
  const body=node('typewriter-body','<span class="typewriter-roller"></span>');world.append(paper,body);
  const keys=$('#task .palet');if(keys){keys.classList.add('typewriter-keys');body.append(keys)}
  captions.forEach(c=>world.append(c));stage.replaceChildren(world);
 }
 const dict=dikteCiz,dictResult=dikteResim;
 dikteCiz=r=>{dict(r);if(GAME_ID==='t09')typewriter(r)};
 dikteResim=r=>{dictResult(r);if(GAME_ID==='t09')typewriter(r)};
 const basket=sepetCiz,position=konumCiz;
 sepetCiz=r=>{
  basket(r);if(GAME_ID!=='t02')return;
  const sources=[...$$('[data-n]')],targets=[...$$('[data-sepet]')];
  const world=node('sound-basket-world','<header>SESLİ SEPET</header>'),table=node('sound-object-table'),baskets=node('sound-real-baskets');
  sources.forEach(b=>{table.append(b);bridge(b,'[data-sepet]',t=>{state.secili=[+b.dataset.n];t.click()})});
  targets.forEach((b,i)=>{b.className='sound-real-basket';b.innerHTML=`<span class="basket-handle"></span><span class="basket-content">${(state.yerlesen||[]).filter(x=>x.sepet===i).map(x=>r.nesneler[x.n].im).join('')}</span><small>${esc((r.sepetler||[{ad:r.sepetAd||'Sepet'}])[i].ad)}</small>`;baskets.append(b)});
  world.append(table,baskets,node('caption',esc(state.not||r.gorev)));$('#stage').replaceChildren(world);$('#task').innerHTML='<div class="caption">Nesneyi sepete sürükle veya nesneye, ardından sepete dokun.</div>';
 };
 konumCiz=r=>{position(r);if(GAME_ID!=='t02')return;const strip=$('#task .serit'),obj=$('#stage .resim-kart'),caption=$('#stage .caption');const w=node('sound-position-board','<header>SESİN YERİNİ BUL</header>');if(obj)w.append(obj);if(strip)w.append(strip);if(caption)w.append(caption);$('#stage').replaceChildren(w)};
 function picture(classroom){
  const pupil=(x,y,color,book)=>`<g transform="translate(${x} ${y})"><circle cy="-29" r="15" fill="#d8a071"/><path d="M-16-36Q0-55 16-36" fill="#57382d"/><path d="M-20-10Q0-25 20-10L24 34H-24Z" fill="${color}"/><path d="M-12 34v26m24-26v26" stroke="#2b425c" stroke-width="10"/>${book?'<path d="M-30-1L0 7 30-1v28L0 35-30 27Z" fill="#fff6cb" stroke="#805732" stroke-width="3"/><path d="M0 7v28" stroke="#805732"/>':''}</g>`;
  return `<svg class="reading-picture" viewBox="0 0 600 300" role="img" aria-label="${classroom?'Sınıfta öğretmen ve öğrenciler':'Bahçede çocuk ve hayvan'}"><rect width="600" height="300" fill="${classroom?'#fff0c8':'#cdeffe'}"/>${classroom?`<rect x="240" y="20" width="330" height="130" rx="8" fill="#266755" stroke="#ad793e" stroke-width="10"/><path d="M310 65h120m-120 25h170" stroke="white" stroke-width="4"/>${pupil(190,125,'#7356ac',false)}<path d="M200 107l77-47" stroke="#d8a071" stroke-width="10"/><rect y="250" width="600" height="50" fill="#c89164"/>${pupil(100,208,'#ed7958',true)}${pupil(380,208,'#59a5db',true)}<path d="M45 249h125m150 0h125" stroke="#945c34" stroke-width="16"/>`:`<rect y="205" width="600" height="95" fill="#85bc6a"/><path d="M430 205V50" stroke="#966437" stroke-width="35"/><circle cx="420" cy="70" r="65" fill="#438d55"/><circle cx="475" cy="92" r="60" fill="#438d55"/>${pupil(250,200,'#e78153',true)}<g transform="translate(355 260)"><ellipse rx="40" ry="18" fill="#c5946a"/><circle cx="-30" cy="-9" r="18" fill="#c5946a"/><path d="M-45-20l3-20 14 12m1 0 15-12-1 24" fill="#c5946a"/><path d="M-40-9h8m5 0h8" stroke="#594132" stroke-width="2"/><path d="M28 0q40-25 43 0" fill="none" stroke="#c5946a" stroke-width="10"/></g><circle cx="70" cy="45" r="24" fill="#f6cd4d"/>`}</svg>`;
 }
 if(GAME_ID==='t62')GAMES.t62.rounds.forEach(r=>{r.gorev=r.gorev.replace('Metne göre','Resme göre');r.result=r.result.replace('Bir sahneyi anlatan metni okuyup','Resmi inceleyip').replace('Metinde','Resimde');r.anahtarlar.forEach(a=>{if(!a.correct)a.hint='Resimdeki ayrıntılara tekrar bak: seçtiğin nesne veya eylem var mı?'});if(r.soru){r.soru.gorev=r.soru.gorev.replace('Metne göre','Resme göre');r.soru.secenekler.forEach(c=>{if(!c.correct)c.hint='Resimdeki kişiye veya hayvana dikkatle bak.'})}});
 const chest=sandikCiz;
 sandikCiz=r=>{
  chest(r);if(GAME_ID!=='t62')return;
  const old=$('#stage .metin-kart'),illustration=node('reading-illustration',picture(roundIndex===2));
  if(roundIndex!==2){const groups=illustration.querySelectorAll('svg>g');groups[0].setAttribute('transform','translate(360 200)');groups[1].setAttribute('transform','translate(450 260)')}
  old?.replaceWith(illustration);$('#stage .world-prop')?.remove();
  const listen=$('#metinDinle');if(listen)listen.textContent='🔊 Erişim desteği: resim betimlemesini dinle';
  if(state.acildi){const label=$('#stage .resim-kart .ad');if(label)label.textContent=(roundIndex===2?'Resimde yok: ':'Bulduğun ayrıntı: ')+r.cikan.ad;if(state.not==='Sandık açıldı.')$('#stage .caption').textContent='Resimdeki ayrıntıyı buldun.'}
 };
})();
