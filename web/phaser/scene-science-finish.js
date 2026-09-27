/* Complete the visible experiment result without changing answer validators. */
(()=>{
 if(!['f30','f32','f34','f40','f41','g45','h13','h29'].includes(GAME_ID))return;
 document.body.classList.add('science-finish');
 if(['f32','f34'].includes(GAME_ID)){
  const drawDecision=kararCiz;let decisionKey=null;kararCiz=r=>{const key=roundIndex+':'+(state.ix||0);if(key!==decisionKey){state.not='';decisionKey=key}drawDecision(r)};
  const r=GAMES[GAME_ID].rounds[1];r.sahne=s=>{const i=s.ix||0,parts=i===0?['kablo','ampul','anahtar']:i===1?['pil','ampul','anahtar']:['pil','kablo','ampul','anahtar'];let diagram=SAHNE.devre({kurulan:parts,anahtarAcik:GAME_ID==='f32'&&i===2});
   if(GAME_ID==='f34'&&i===1)diagram=diagram.replace('</svg>','<path d="M44 36H276" stroke="#9d764d" stroke-width="7"/><text x="160" y="19" text-anchor="middle" font-size="10" fill="#59482f">Tahta çubuk · yalıtkan</text></svg>');
   if(GAME_ID==='f34'&&i===2){diagram=diagram.replace(/<rect x="128" y="94"[^>]*\/><text x="160" y="109"[^>]*>[^<]*<\/text>/,'<g class="series-cells" role="img" aria-label="Aynı yönde seri bağlanmış iki pil"><path d="M116 104H204" stroke="#40505c" stroke-width="4"/><rect class="series-cell" x="118" y="94" width="38" height="20" rx="3" fill="#e8b62c" stroke="#a97c14" stroke-width="2"/><rect class="series-cell" x="164" y="94" width="38" height="20" rx="3" fill="#e8b62c" stroke="#a97c14" stroke-width="2"/><text x="137" y="108" text-anchor="middle" font-size="10" fill="#6b4d08">+ −</text><text x="183" y="108" text-anchor="middle" font-size="10" fill="#6b4d08">+ −</text></g>');diagram=diagram.replace('</svg>','<circle cx="160" cy="34" r="25" fill="#ffe46b" opacity=".3"/><text x="160" y="17" text-anchor="middle" font-size="10" fill="#806516">İki özdeş pil · seri bağlı</text></svg>')}
   return diagram;
  };if(GAME_ID==='f34')r.sorular[2].durum='Aynı devreye ikinci özdeş pil, aynı yönde seri bağlanıyor.';
 }
 if(GAME_ID==='f41'){
  const r=GAMES.f41.rounds[0],names=['Lamba siperi','Aşağı yönlü yol lambası','Gece zamanlayıcısı','Hareket sensörü','Düşük parlaklık ayarı','Pencere perdesi'];
  r.havuz.forEach((h,i)=>{h.t=names[i];h.ic='';});
  r.istekler[0]={ad:'Işığı gökyüzüne değil yola yönlendir',gerekli:['yesil','yaya'],neden:'Siper ve aşağı yönlü lamba, ışığın gökyüzüne kaçmasını azaltır.'};
  r.istekler[1]={ad:'Işığı yalnız gerektiğinde kullan',gerekli:['toplu','bisiklet'],neden:'Zamanlayıcı ve hareket sensörü, kullanılmayan zamanda gereksiz ışığı azaltır.'};
  r.istekler[2]={ad:'Gereğinden parlak ışığı ve dışarı sızan ışığı azalt',gerekli:['gunes','bina'],neden:'Uygun parlaklık ve perde, gereksiz ışığın çevreye yayılmasını azaltır.'};
  const writing=GAMES.f41.rounds[2];writing.denetim[0]={ad:'Maket çözümünden söz et: lamba, siper, sensör, zamanlayıcı, parlaklık veya perde',desen:'lamba|siper|sensör|zamanlayıcı|parlaklık|perde'};writing.ornekCevap='Maketimde aşağı yönlü lamba ve zamanlayıcı kullandım çünkü gökyüzüne kaçan ışık azalır ve gereksiz enerji kullanılmaz.';
  SAHNE.maket=items=>{const has=id=>items.some(i=>i.id===id),directed=has('yesil')&&has('yaya'),timed=has('toplu'),dim=has('gunes'),sensor=has('bisiklet');
   return SVG(320,170,`<rect width="320" height="170" fill="#172940"/><path d="M0 120H320V170H0" fill="#47605b"/><path d="M0 147H320" stroke="#afb69d" stroke-width="9"/>${Array.from({length:8},(_,i)=>`<circle cx="${25+i*36}" cy="${18+i%3*10}" r="2" fill="#d9e8eb"/>`).join('')}<rect x="235" y="65" width="65" height="60" fill="#6c7790"/><rect x="248" y="77" width="27" height="28" fill="${has('bina')?'#657788':'#f3dc8b'}"/>${has('bina')?'<path d="M248 77l13 28 14-28" fill="#a37491"/>':''}<path d="M92 131V68q0-17 27-17" fill="none" stroke="#a3b4bd" stroke-width="7"/><ellipse cx="124" cy="54" rx="15" ry="5" fill="${timed?'#79909b':'#efd978'}"/>${has('yesil')?'<path d="M104 49Q124 31 144 49Z" fill="#97aab4"/>':''}${!timed?`<path d="${directed?'M113 60L76 140H174L136 60Z':'M112 46L54 4H190L135 46Z'}" fill="#f9e48f" opacity="${dim?'.18':'.55'}"/>`:''}${sensor?'<circle cx="93" cy="82" r="7" fill="#d0e7ea"/><path d="M103 76q17 8 0 17" fill="none" stroke="#d0e7ea" stroke-width="2"/>':''}<text x="160" y="164" text-anchor="middle" font-size="10" fill="#eef5f3">${timed?'Gece geç saat: zamanlayıcı ışığı kapattı':directed?'Işık yola yöneldi':'Işık yukarı kaçıyor · yönünü düzelt'}</text>`)+`<div class="caption">${items.map(i=>names[r.havuz.findIndex(h=>h.id===i.id)]).filter(Boolean).join(' · ')||'Gece aydınlatma maketi'}</div>`;
  };
 }
 if(['f30','f34','f41'].includes(GAME_ID)){
  const draw=kapHtml;kapHtml=r=>{const host=document.createElement('div');host.innerHTML=draw(r);host.querySelectorAll('[data-kur-hedef]').forEach(e=>e.removeAttribute('data-kur-hedef'));const model=host.querySelector('svg');if(model){model.setAttribute('data-kur-hedef','1');model.setAttribute('aria-label','Malzemeyi deney düzeneğine bırak')}return host.innerHTML};
 }
 if(GAME_ID==='h29'){
  const draw=muslukCiz;muslukCiz=r=>{draw(r);const button=document.querySelector('#musluk'),sink=document.querySelector('.lavabo');if(!button||!sink)return;
   button.className='tap-handle'+(state.basili?' basili':'');button.setAttribute('aria-label','Su akıtmak için musluk kolunu basılı tut');sink.append(button);
   const down=button.onpointerdown,begin=e=>{if(state.basili)return;state.not='';document.querySelector('#stage>.caption')?.remove();down(e)};button.onpointerdown=e=>{if(state.basili)return;button.setPointerCapture(e.pointerId);begin(e)};button.onpointerleave=null;
   button.onkeydown=e=>{if([' ','Enter'].includes(e.key)){e.preventDefault();if(!e.repeat&&!state.basili)begin({preventDefault(){}})}};
   button.onkeyup=e=>{if([' ','Enter'].includes(e.key)){e.preventDefault();button.onpointerup()}};button.onblur=()=>button.onpointercancel();
  };
 }
 if(GAME_ID==='g45'){
  const pictures={
   'Çöl':'<rect width="240" height="100" fill="#f8dfa4"/><circle cx="205" cy="24" r="17" fill="#df9b36"/><path d="M0 78Q70 30 150 79Q190 50 240 70V100H0" fill="#d7aa61"/><path d="M60 85V35M60 55H45V43M60 64H76V48" fill="none" stroke="#658149" stroke-width="8"/>',
   'Yağmur ormanı':'<rect width="240" height="100" fill="#b2d8c5"/><path d="M30 100V20M83 100V15M160 100V25M211 100V13" stroke="#715c39" stroke-width="13"/><g fill="#4b805b"><circle cx="30" cy="30" r="32"/><circle cx="83" cy="24" r="33"/><circle cx="160" cy="35" r="31"/><circle cx="211" cy="24" r="34"/></g>',
   'Kutup':'<rect width="240" height="100" fill="#cce5f1"/><path d="M0 80L60 15 114 80 174 30 240 85V100H0" fill="#fff"/><path d="M0 87H240" stroke="#91bed3" stroke-width="8"/>',
   'Gölet':'<rect width="240" height="100" fill="#a9cf8f"/><ellipse cx="120" cy="67" rx="100" ry="30" fill="#67b3d1"/><path d="M30 65V15M38 67V24M208 75V22" stroke="#658449" stroke-width="5"/><ellipse cx="105" cy="65" rx="15" ry="7" fill="#f3d065"/>',
   'Bozkır':'<rect width="240" height="100" fill="#cde8ee"/><path d="M0 65H240V100H0" fill="#b2b369"/><path d="M15 100l6-22m25 22l-5-17m33 17l5-20m45 20l-6-19m40 19l7-16m32 16l-7-20" stroke="#77914d" stroke-width="4"/>',
   'Yaprak döken orman':'<rect width="240" height="100" fill="#e4e6c0"/><path d="M35 100V45M112 100V36M198 100V47" stroke="#795d39" stroke-width="10"/><g fill="#cb944d"><circle cx="35" cy="38" r="27"/><circle cx="112" cy="32" r="30"/><circle cx="198" cy="40" r="26"/></g>'
  };
  const draw=esleCiz;esleCiz=r=>{draw(r);const area=document.querySelector('.esle-alan');if(!area)return;area.classList.add('habitat-grid');area.querySelectorAll('[data-yuva]').forEach((button,i)=>{const name=r.etiketler[r.yuvalar[i].dogru].t;button.classList.add('habitat-card');button.insertAdjacentHTML('afterbegin',`<svg viewBox="0 0 240 100" role="img" aria-label="Yaşam alanı örneği">${pictures[name]||''}</svg>`)});
  };
 }
 const finish=good;good=message=>{if(locked)return;const result=document.createElement('div');result.className='science-result';result.setAttribute('role','status');result.textContent=round().result||message||'İşlem tamamlandı. Sonuç sahnede görünüyor.';document.querySelector('#stage')?.append(result);document.querySelector('#task')?.replaceChildren();finish(message)};
})();
