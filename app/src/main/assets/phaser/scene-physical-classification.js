/* Somut sınıflandırmalar: hedef, etiket kutusu değil sahnedeki nesnenin kendisidir. */
window.ScenePhysicalClassification=(()=>{
 const esc=SceneWorkshop.escape;
 const W={
  z17:{name:'ENERJİ ARAŞTIRMA ALANI',kind:'energy-book',zones:[['Yenilenen üretim','Güneş • rüzgâr • su','renew'],['Yer altı rezervi','Çıkarıldıkça azalır','fossil']]},
  z49:{name:'YAŞAYAN MÜZE',kind:'museum',zones:[['Vitrindeki eser','Görülebilen yapı ve nesne','exhibit'],['Canlı gösteri alanı','Yaşatılan bilgi ve sanat','performance']]},
  g15:{name:'MADEN ATÖLYESİ',kind:'metal',zones:[['Sağlam iskelet','Demir tezgâhı','iron'],['İletken tel','Bakır makara','copper'],['Hafif kaplama','Alüminyum levha','aluminium']]},
  g16:{name:'KAZI SINIFLANDIRMA MASASI',kind:'geology',zones:[['Tek kristal','Mineral örneği','mineral'],['Birleşik yapı','Kayaç kesiti','rock'],['Canlı izi','Fosil kalıbı','fossilprint']]},
  g26:{name:'KUVVET DENEY PARKURU',kind:'force-park',zones:[['Yolu değişen cisim','Hareket izi','moving'],['Biçimi değişen cisim','Şekil izi','shaping'],['İki iz bir arada','Hareket + biçim','both']]},
  g30:{name:'EVDE KUVVET GÖZLEMİ',kind:'force-home',zones:[['Harekete başlama','Başlangıç çizgisi','start'],['Yavaşlama ve durma','Fren alanı','brake'],['Biçim değiştirme','Esnek malzeme','bend']]},
  g42:{name:'HASAT BAHÇESİ',kind:'garden',zones:[['Toprağın altı','Kök ve yumru bölümü','roots'],['Kısa gövde','Yerin üstündeki bitki','stem'],['Ağaç dalları','Çok yıllık ağaç','canopy']]},
  f19:{name:'HÂL DEĞİŞİMİ LABORATUVARI',kind:'phase',zones:[['Isınan buz kabı','Katıdan sıvıya','melting'],['Soğutucu kalıp','Sıvıdan katıya','freezing'],['Kuruyan kumaş','Sıvıdan gaza','evaporating'],['Soğuk cam yüzeyi','Gazdan sıvıya','condensing']]},
  f20:{name:'ISI AKIŞI DENEYİ',kind:'heat',zones:[['Isı kaynağı','Maddeye doğru akış','heating'],['Soğuk ortam','Maddeden dışarı akış','cooling']]},
  f33:{name:'ŞEHİR ENERJİ ŞEBEKESİ',kind:'energy-city',zones:[['Döngüyle çalışan hat','Güneş • rüzgâr • su','green-grid'],['Yakıt deposu hattı','Kömür • petrol • gaz','fuel-grid']]},
  f37:{name:'GECE IŞIK GÖZLEMİ',kind:'light',zones:[['Doğanın ışığı','Kendiliğinden oluşur','natural-light'],['İnsan yapımı ışık','Üretilmiş aygıt','made-light']]},
  h24:{name:'İKİ KUTLAMA SAHNESİ',kind:'holiday',zones:[['Tören meydanı','Ülkemizin tarihindeki olay','national'],['Bayramlaşma evi','İnanç ve paylaşma geleneği','religious']]}
 };
 const itemIcons={
  z17:['☀️','🪨','🌬️','🛢️','💧','🔥'],z49:['🏛️','🎶','🎭','🏰','🎨','🏛️'],
  g15:['🔌','🏗️','🥣','🔌','🔨','✈️'],g16:['💎','🪨','🐚','💎','🪨','🐚'],
  g26:['⚽','🫓','🛷','🏀','📄','🛹'],g30:['🛷','🛷','❄️','🎠','🎠','📏'],
  g42:['🧅','🥬','🍒','🥕','🫑','🌰'],f19:['🧊','💧','👕','🥤','🧈','🪟'],
  f20:['🧊','💧','💦','☁️'],f33:['☀️','🪨','🌬️','🛢️','💧','🔥'],
  f37:['☀️','💡','⭐','🕯️','⚡','🐞','📱'],h24:['🇹🇷','🤝','🇹🇷','🥩','🇹🇷','🍬']
 };
 const S=(body,bg)=>`<svg viewBox="0 0 180 105" role="presentation" aria-hidden="true"><rect width="180" height="105" fill="${bg}"/>${body}</svg>`;
 const art={
  renew:S('<circle cx="32" cy="28" r="16" fill="#ffce4c"/><path d="M5 72h170" stroke="#7da950" stroke-width="6"/><path d="M95 35v57M95 35l-25-22M95 35l27-25M95 35l17 30" stroke="#f1f7f1" stroke-width="5"/><circle cx="95" cy="35" r="5" fill="#758a8d"/><path d="M126 66l32-10v29h-32z" fill="#38698a"/><path d="M126 72h32M126 79h32" stroke="#a9d9f1" stroke-width="3"/>','#acdce9'),
  fossil:S('<path d="M0 64h180v41H0z" fill="#614839"/><path d="M0 79h180M0 92h180" stroke="#83684c" stroke-width="5"/><path d="M30 64v-28h47v28M37 37v-15h33v15" fill="#b7a091" stroke="#503a2d" stroke-width="4"/><path d="M48 79l10-10 11 10-10 9zM112 78l11-9 11 12-10 10z" fill="#202b32"/><path d="M142 60v-29h10v29" stroke="#5a5e64" stroke-width="7"/>','#c9b49c'),
  exhibit:S('<rect x="20" y="15" width="140" height="76" rx="6" fill="#dfe7dd" stroke="#8a997b" stroke-width="5"/><path d="M32 74h116" stroke="#ac795a" stroke-width="8"/><path d="M65 71V37q26-25 50 0v34" fill="#e5cba5" stroke="#a88461" stroke-width="4"/><path d="M84 39v28m13-27v28" stroke="#ad855f" stroke-width="5"/>','#eadcca'),
  performance:S('<path d="M0 0h42l-8 80H0M180 0h-42l8 80h34" fill="#9f394a"/><path d="M33 81h114" stroke="#854f36" stroke-width="10"/><circle cx="90" cy="36" r="13" fill="#d5aa7c"/><path d="M75 49q15-8 30 0l12 29H63z" fill="#335576"/><path d="M65 59l-20-14m70 14l20-14" stroke="#d5aa7c" stroke-width="7"/>','#f4d9a3'),
  iron:S('<path d="M18 37h143v16H18zM45 54v35h21V54m48 0v35h21V54" fill="#5c707b" stroke="#344854" stroke-width="4"/><path d="M36 79h108" stroke="#9db3bb" stroke-width="7"/>','#e6ebed'),
  copper:S('<path d="M31 83V25h20v58M130 83V25h20v58" fill="#a6aeb4"/><path d="M51 45q38-38 79 0t-79 0m0 16q38-38 79 0t-79 0m0 16q38-38 79 0t-79 0" fill="none" stroke="#b76c3d" stroke-width="7"/>','#e8e1d2'),
  aluminium:S('<path d="M22 68l116-35 23 12-123 36z" fill="#c8d9e3" stroke="#7490a0" stroke-width="4"/><path d="M77 51l-16-28 20-5 20 25m18-2l12-24 13-3-8 25" fill="#9eb6c3"/>','#d9eafa'),
  mineral:S('<path d="M39 80l14-55 31-9 20 19 18-14 22 55z" fill="#99b4cb" stroke="#4c789b" stroke-width="4"/><path d="M84 16v62m20-43l-20 43m38-57l-38 57" stroke="#eaf4fa" stroke-width="4"/>','#e5eff3'),
  rock:S('<path d="M19 76l21-40 32 18 29-33 38 22 22 33z" fill="#897965" stroke="#564d44" stroke-width="4"/><path d="M26 70l31-12 27 11 32-21 33 20" fill="none" stroke="#c8ae8c" stroke-width="7"/>','#dfd4be'),
  fossilprint:S('<path d="M18 84l17-62 110-6 19 69z" fill="#c3ab83" stroke="#826a51" stroke-width="4"/><path d="M87 53m-28 0a28 22 0 1 0 56 0a28 22 0 1 0-56 0" fill="none" stroke="#f7e7c9" stroke-width="5"/><path d="M87 53q24-2 10 10-12 10-21-1-8-9 3-17" fill="none" stroke="#f7e7c9" stroke-width="5"/>','#e8dcc2'),
  moving:S('<circle cx="61" cy="55" r="19" fill="#edaf4b" stroke="#855a31" stroke-width="4"/><path d="M88 55h57m-15-15l17 15-17 15" fill="none" stroke="#d95e4f" stroke-width="6"/><path d="M10 84h160" stroke="#8a9c82" stroke-width="5"/>','#d7ecdb'),
  shaping:S('<path d="M35 70q45-52 97 0q-28 25-97 0z" fill="#e6af70" stroke="#9c6947" stroke-width="4"/><path d="M89 10v34m-13-12l13 14 13-14" fill="none" stroke="#4f7ba7" stroke-width="6"/>','#f6ead3'),
  both:S('<circle cx="61" cy="64" r="20" fill="#efb15d" stroke="#885838" stroke-width="4"/><path d="M50 48q8 17 0 29M85 63h55m-13-14l15 14-15 14" fill="none" stroke="#d46058" stroke-width="6"/>','#e6ead5'),
  start:S('<rect x="35" y="43" width="70" height="33" rx="6" fill="#668ca7"/><circle cx="49" cy="81" r="9" fill="#283f53"/><circle cx="91" cy="81" r="9" fill="#283f53"/><path d="M115 58h44m-16-14l17 14-17 14" fill="none" stroke="#d69044" stroke-width="6"/>','#e8ece6'),
  brake:S('<circle cx="55" cy="66" r="23" fill="#668c9e" stroke="#304b5b" stroke-width="6"/><path d="M116 26l-18 45m28-39l-18 45" stroke="#c36255" stroke-width="10"/><path d="M32 88h120" stroke="#849b91" stroke-width="5"/>','#e2eaec'),
  bend:S('<path d="M26 32q64 71 129 0" fill="none" stroke="#c49d68" stroke-width="12"/><path d="M81 13v27m-13-12l13 13 13-13" fill="none" stroke="#6991b2" stroke-width="5"/>','#f4eadb'),
  roots:S('<path d="M0 34h180v71H0z" fill="#865c3d"/><path d="M0 49h180M0 77h180" stroke="#a57750" stroke-width="4"/><path d="M82 18v43m0 0l-17 24m17-24l22 22" stroke="#e7c56f" stroke-width="9"/><path d="M82 32q-30-25-39-6m39 3q24-23 42-4" fill="none" stroke="#57965d" stroke-width="7"/>','#b9d7a0'),
  stem:S('<path d="M0 82h180" stroke="#82694d" stroke-width="10"/><path d="M90 79V28M90 48q-28-25-36-7m36 18q24-24 35-5" fill="none" stroke="#477d49" stroke-width="8"/><circle cx="111" cy="33" r="12" fill="#d6604b"/><circle cx="70" cy="58" r="10" fill="#dd714c"/>','#c7e4b6'),
  canopy:S('<path d="M0 86h180" stroke="#789650" stroke-width="8"/><path d="M88 87V40m0 18l-24-18m24 11l27-17" stroke="#806040" stroke-width="13"/><circle cx="87" cy="26" r="29" fill="#52935c"/><circle cx="57" cy="35" r="22" fill="#62a066"/><circle cx="116" cy="35" r="25" fill="#5e9e5c"/><circle cx="70" cy="29" r="7" fill="#d95b4b"/><circle cx="105" cy="44" r="7" fill="#dc5e4c"/>','#cbe7b9'),
  melting:S('<path d="M30 40h120l-17 49H48z" fill="#dceef1" stroke="#719aa9" stroke-width="4"/><path d="M49 73h82" stroke="#6fb3d2" stroke-width="14"/><rect x="73" y="26" width="34" height="33" rx="4" fill="#f2fdff" stroke="#9dd5e4" stroke-width="3"/><path d="M55 22h70" stroke="#e8a75b" stroke-width="6"/>','#f6ebe2'),
  freezing:S('<rect x="35" y="31" width="110" height="58" rx="7" fill="#b8dbe8" stroke="#628ba0" stroke-width="5"/><path d="M72 32v55m36-55v55M36 60h108" stroke="#ebf8fa" stroke-width="4"/><path d="M28 18h125" stroke="#83b7d0" stroke-width="6"/>','#dfeef5'),
  evaporating:S('<path d="M30 47h120v41H30z" fill="#acc9df" stroke="#6387a8" stroke-width="4"/><path d="M25 40h130" stroke="#6d7982" stroke-width="4"/><path d="M52 15q-9 15 0 25m34-25q-9 15 0 25m34-25q-9 15 0 25" fill="none" stroke="#7eabc1" stroke-width="4"/>','#f8eee0'),
  condensing:S('<rect x="45" y="16" width="92" height="73" rx="5" fill="#c5e4ee" stroke="#6497ac" stroke-width="6"/><path d="M67 40q-7 18 0 21 7-4 0-21m33-9q-7 18 0 21 7-4 0-21m20 24q-7 18 0 21 7-4 0-21" fill="#499ed0"/>','#e8f1f6'),
  heating:S('<path d="M44 35h92l-8 53H52z" fill="#cde6ef" stroke="#5f859a" stroke-width="5"/><path d="M40 95h100" stroke="#d26d45" stroke-width="8"/><path d="M65 88V60m25 28V60m25 28V60" stroke="#e45438" stroke-width="6"/><path d="M56 66l9-12 9 12m7 0l9-12 9 12m7 0l9-12 9 12" fill="none" stroke="#e45438" stroke-width="4"/>','#f6e8dc'),
  cooling:S('<path d="M42 36h96l-8 51H50z" fill="#cce2e9" stroke="#678e9d" stroke-width="5"/><path d="M60 63v27m30-27v27m30-27v27" stroke="#549ac1" stroke-width="6"/><path d="M51 82l9 12 9-12m12 0l9 12 9-12m12 0l9 12 9-12" fill="none" stroke="#549ac1" stroke-width="4"/>','#e3f1f4'),
  'green-grid':S('<circle cx="35" cy="23" r="15" fill="#ffd257"/><path d="M10 85h160" stroke="#6a9d65" stroke-width="8"/><path d="M85 36v53M85 36L59 22M85 36l26-23M85 36l21 28" stroke="#e9f3f1" stroke-width="5"/><rect x="126" y="58" width="39" height="24" fill="#35799f"/><path d="M128 64h35m-35 7h35" stroke="#aad4e8" stroke-width="3"/>','#b9e4ed'),
  'fuel-grid':S('<path d="M0 80h180" stroke="#7c6d5e" stroke-width="10"/><rect x="26" y="42" width="110" height="41" fill="#5d6972"/><path d="M37 42V16h19v26m37 0V25h17v17" fill="#8c9091"/><path d="M42 14q-10-7-3-12m13 9q-8-8-1-12" fill="none" stroke="#9caaa9" stroke-width="5"/><circle cx="148" cy="78" r="10" fill="#242c35"/>','#c9c3b9'),
  'natural-light':S('<path d="M0 73h180v32H0z" fill="#263d59"/><circle cx="42" cy="29" r="16" fill="#fbd263"/><path d="M86 22l4 10 10 4-10 4-4 10-4-10-10-4 10-4zM131 19l2 8 8 2-8 3-2 8-3-8-8-3 8-2z" fill="#fff8c6"/>','#162a52'),
  'made-light':S('<path d="M0 77h180v28H0z" fill="#444d67"/><path d="M67 78V29h51v49" fill="#556f8b"/><rect x="81" y="41" width="21" height="19" fill="#ffe19b"/><path d="M137 77V27h17v50" stroke="#b0a9a1" stroke-width="5"/><circle cx="145" cy="24" r="14" fill="#ffe8a1"/><path d="M117 70l27-45" stroke="#ffdc96" stroke-width="3"/>','#283450'),
  national:S('<path d="M0 81h180" stroke="#9caa9a" stroke-width="8"/><path d="M61 81V14" stroke="#d0d7d7" stroke-width="6"/><path d="M64 18h48v28H64z" fill="#d9504c"/><circle cx="85" cy="31" r="9" fill="white"/><circle cx="89" cy="29" r="8" fill="#d9504c"/><path d="M109 29l3 6-7-3h8l-7 4z" fill="white"/><path d="M19 81V54h30v27m77 0V54h30v27" fill="#b9c8d2"/>','#b5dbed'),
  religious:S('<path d="M18 87h144" stroke="#b28c67" stroke-width="9"/><rect x="36" y="23" width="108" height="65" rx="6" fill="#ead0a7" stroke="#a67c58" stroke-width="4"/><path d="M83 88V49q15-20 30 0v39" fill="#8d634e"/><path d="M56 45h18m51 0h10" stroke="#faf1da" stroke-width="8"/><circle cx="25" cy="70" r="11" fill="#d99a66"/><circle cx="156" cy="70" r="11" fill="#d99a66"/>','#e7e4c7')
 };
 function render({id,r,state,wrong,finish,next,fast,locked}){
  const cfg=W[id],i=state.ix||0,k=r.kartlar[i];if(!cfg||!k)return;
  state.worldPlaced=null;state.worldSelected=false;
  const stage=document.querySelector('#stage'),task=document.querySelector('#task'),scene=document.querySelector('.scene');
  scene.classList.add('world-scene');scene.dataset.world=id;
  const itemIcon=itemIcons[id]?.[i]||'✥';
  const paint=()=>{stage.innerHTML=`<div class="world-field world-${cfg.kind}"><header><b>${cfg.name}</b><span>${i+1} / ${r.kartlar.length}</span></header><div class="world-zones zones-${cfg.zones.length}">${cfg.zones.map((z,j)=>`<div class="world-zone"><strong class="world-zone-name">${esc(z[0])}</strong><button class="world-destination ${state.worldPlaced===j?'world-placed':''}" data-kutu="${j}" aria-label="${esc(z[0])} sahnesine bırak">${art[z[2]]}<span class="world-arrival">${state.worldPlaced===j?`<span class="world-arrival-icon">${itemIcon}</span>${esc(k.t)}`:''}</span></button><span class="world-zone-hint">${esc(z[1])} · ${(state.sayim||[])[j]||0}</span></div>`).join('')}</div><p class="world-result" role="status">${state.worldPlaced!==null?esc(k.neden||'Nesne yerleşti.'):esc(state.not||'Kartı sahnedeki uygun yere bırak.')}</p></div>`};
  paint();task.innerHTML=`<button class="world-source" data-sinif-kart="1" aria-label="${esc(k.t)}; seç veya sürükle"><span class="world-source-mark">${itemIcon}</span><span>${esc(k.t)}${k.sahne?`<small>${esc(k.sahne)}</small>`:''}</span><span class="world-grip" aria-hidden="true">⠿</span></button><p class="world-help">Kartı sahnedeki nesneye sürükle. İstersen dokunarak seçip hedefe dokun.</p>`;
  const source=task.querySelector('[data-sinif-kart]');
  const place=j=>{if(locked()||state.gecis||state.worldPlaced!==null)return;if(j!==k.dogru)return wrong(k.hint||'Sahnedeki kanıta yeniden bak.');
   state.worldPlaced=j;state.worldSelected=false;state.sayim=state.sayim||r.kutular.map(()=>0);state.sayim[j]++;state.ix=i+1;state.not=k.neden||'';source.hidden=true;paint();
   next(()=>{if(state.ix>=r.kartlar.length)finish();else render({id,r,state,wrong,finish,next,fast,locked})},fast?30:840)};
  source.onclick=()=>{if(locked()||state.gecis)return;state.worldSelected=!state.worldSelected;source.classList.toggle('selected',state.worldSelected)};
  stage.querySelectorAll('[data-kutu]').forEach(b=>b.onclick=()=>place(+b.dataset.kutu));
  SceneWorkshop.bindDrag('[data-sinif-kart]','#stage [data-kutu]',(_el,target)=>place(+target.dataset.kutu));
 }
 return {render,ids:Object.keys(W)};
})();
