/* Three distinct worlds; all decisions act on the visible scene. */
const originalStormStages = RENDERERS.stages;
RENDERERS.stages = (r,v,t) => {
 if(GAME_ID!=='m41')return originalStormStages(r,v,t);
 if(state.stage==null)state.stage=0;
 const data=[['12 + 6',18],['8 + 1',9],['14 − 3',11]][roundIndex],s=r.stages[state.stage];
 t.innerHTML='';
 v.innerHTML=`<div class="storm-world"><header>ŞİMŞEK VADİSİ</header><div class="storm-cloud">${data[0]}</div><p class="world-status" role="status">${state.stage?'Tahminin doğru. Şimdi kesin sonucu seç.':'Sonuç 10’dan küçük mü, büyük mü? Taşa dokun.'}</p><div class="storm-ground">${state.stage?`<div class="storm-results">${s.choices.map((c,i)=>`<button class="storm-result" data-choice="${i}">${esc(c.label)}</button>`).join('')}</div>`:s.choices.map((c,i)=>`<button class="storm-rock ${c.html==='🗿'?'large':'small'}" data-choice="${i}"><span>${c.html==='🗿'?'10’dan büyük':'10’dan küçük'}</span><i aria-hidden="true">⚡</i></button>`).join('')}</div><div class="storm-reveal" aria-live="polite"></div></div>`;
 v.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>{
  if(locked)return;const c=s.choices[+b.dataset.choice];
  if(!c.correct)return wrong(s.hint||r.hint||'İşlemi yeniden düşün.');
  b.classList.add('struck');
  if(state.stage===0){locked=true;v.querySelector('.world-status').textContent='Şimşek seçtiğin taşa düştü!';state.stage=1;setTimeout(()=>{locked=false;renderTask(r)},650)}
  else{v.querySelector('.storm-reveal').innerHTML=`${Array.from({length:data[1]},(_,i)=>`<i style="--delay:${i*20}ms"></i>`).join('')}<strong>${data[0]} = ${data[1]}</strong>`;success(r.story)}
 });
};
const originalTwinsChoose = RENDERERS.choose;
RENDERERS.choose=(r,v,t)=>{
 if(!['m45','m47'].includes(GAME_ID))return originalTwinsChoose(r,v,t);
 t.innerHTML='';
 if(GAME_ID==='m45'){
  const data=[['5 + 4',9,[9,10,10]],['7 + 2',9,[7,9,8]],['8 − 3',5,[5,6,6]]][roundIndex];
  const robot=(expr,cls='')=>`<span class="twin-robot ${cls}" aria-hidden="true"><i class="robot-head"><b>● ●</b></i><i class="robot-body">${expr}</i><i class="robot-feet"></i></span>`;
  v.innerHTML=`<div class="twins-workshop"><header>İKİZ ROBOT ATÖLYESİ</header><div class="twin-dock">${robot(data[0],'reference')}<span class="twin-link">?</span><div class="twin-partner" aria-label="İkiz robotun buluşma yeri"></div></div><p class="world-status" role="status">Aynı sonucu veren robota dokun; ikizini yanına getir.</p><div class="twin-candidates">${r.choices.map((c,i)=>`<button data-choice="${i}" aria-label="${esc(c.label)} robotunu eşleştir">${robot(esc(c.label))}</button>`).join('')}</div><div class="twin-proof" aria-live="polite"></div></div>`;
  bindChoice(r,(c,i,b)=>{if(!c.correct)return wrong(r.hint);v.querySelector('.twin-partner').innerHTML=robot(esc(c.label),'arriving');v.querySelector('.twin-link').textContent='=';b.disabled=true;b.classList.add('chosen');v.querySelector('.twin-dock').classList.add('matched');v.querySelector('.world-status').textContent='İkizler buluştu! İki işlemin sonucu aynı.';v.querySelector('.twin-proof').innerHTML=[data[0],c.label].map(expr=>`<div><strong>${esc(expr)} = ${data[1]}</strong><span>${Array.from({length:data[1]},()=>'<i></i>').join('')}</span></div>`).join('');success(r.story)});
 }else{
  const d=[['5 + 2','9 − 2',7,7],['4 + 4','3 + 6',8,9],['10 − 3','3 + 3',7,6]][roundIndex];
  const people=(n,side)=>Array.from({length:n},()=>`<i class="tug-person ${side}" aria-hidden="true"><b></b></i>`).join('');
  v.innerHTML=`<div class="tug-stadium"><header>HALAT ÇEKME SAHASI</header><div class="tug-scoreboard"><strong>Sol · ${d[0]}</strong><strong>Sağ · ${d[1]}</strong></div><div class="tug-field"><div class="tug-center"></div><div class="tug-assembly"><div class="tug-team left-team" role="img" aria-label="Sol takım ${d[2]} kişi">${people(d[2],'left')}</div><div class="tug-rope"><i class="tug-ribbon"></i></div><div class="tug-team right-team" role="img" aria-label="Sağ takım ${d[3]} kişi">${people(d[3],'right')}</div></div></div><p class="world-status" role="status">Takımları karşılaştır. Halat nereye gider?</p><div class="tug-decisions">${r.choices.map((c,i)=>`<button data-choice="${i}">${c.label==='Sol'?'← Sol':c.label==='Sağ'?'Sağ →':'Ortada kalır'}</button>`).join('')}</div></div>`;
  bindChoice(r,c=>{if(!c.correct)return wrong(r.hint);const direction=Math.sign(d[3]-d[2]),a=v.querySelector('.tug-assembly');a.style.setProperty('--pull',direction*17+'%');a.classList.add(direction?'pulled':'balanced');v.querySelector('.world-status').textContent=direction===0?`${d[2]} kişi = ${d[3]} kişi. Halat ortada kaldı.`:`Sol ${d[2]}, sağ ${d[3]} kişi. Halat ${direction>0?'sağa':'sola'} çekildi!`;success(r.story)});
 }
};
