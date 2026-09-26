/* Adapt bound native controls; never replace the learning validator. */
(()=>{
 if(!/^[vwpuyz]/.test(GAME_ID))return;
 document.body.classList.add('upper-stage','upper-'+GAME_ID);document.documentElement.classList.add('upper-stage');
 if(typeof endDrag==='function'){const old=endDrag;endDrag=e=>{if(e.type==='pointercancel'&&drag)drag.moved=false;old(e)}}
 let graphRound=-1,graphCounts={};
 function adapt(){
  const stage=document.querySelector('#stage'),task=document.querySelector('#task');if(!stage||!task)return;
  const ta=task.querySelector('#yaziAlan,#duzeltAlan');
  if(ta){const focus=document.activeElement===ta,a=ta.selectionStart,b=ta.selectionEnd,paper=document.createElement('section');paper.className='upper-paper'+(ta.id==='duzeltAlan'?' upper-proof-paper':'');const header=document.createElement('header');header.textContent=ta.id==='duzeltAlan'?'DÜZELTME MASASI · SENİN DÜZENLEDİĞİN METİN':'YAZI MASASI · SENİN SAYFAN';paper.append(header,ta);const criteria=task.querySelector('.olcut');if(criteria)paper.append(criteria);(stage.querySelector('.u-world')||stage).append(paper);if(focus){ta.focus({preventScroll:true});ta.setSelectionRange(a,b)}}
  stage.querySelectorAll('.t3-yazi').forEach(el=>{if(el.closest('.upper-paper'))return;const paper=document.createElement('section');paper.className='upper-paper';el.replaceWith(paper);paper.append(el)});
  if(GAME_ID==='w03')task.querySelectorAll('[data-choice]').forEach((button,i)=>{const tunnel=stage.querySelectorAll('.tunnel')[i];if(tunnel)tunnel.append(button)});
  if(GAME_ID==='v02'&&round()?.kind==='choice'){const wagon=stage.querySelector('.senior-wagon');if(wagon)task.querySelectorAll('[data-choice]').forEach(button=>wagon.append(button))}
  if(GAME_ID==='v27'&&task.querySelector('[data-card]')){const desk=document.createElement('div');desk.className='upper-memory-desk';task.querySelectorAll('[data-card]').forEach(button=>desk.append(button));stage.append(desk)}
  if(GAME_ID==='p32'){const bench=stage.querySelector('.senior-tool-bench');if(bench)task.querySelectorAll('[data-action]').forEach(button=>bench.append(button))}
  if(round()?.kind==='graph'){
   const columns=[...stage.querySelectorAll('.bar-col')];
   task.querySelectorAll('[data-graph]').forEach((button,i)=>{if(!columns[i])return;const click=button.onclick;button.onclick=e=>{e.stopPropagation();click?.call(button,e)};columns[i].append(button)});
   if(graphRound!==roundIndex){graphRound=roundIndex;graphCounts={...state.counts}}
   round().columns.forEach((c,i)=>{const value=state.counts?.[c.id]||0;if(value!==graphCounts[c.id])columns[i]?.querySelector('.bar span:last-child')?.classList.add('upper-recorded');graphCounts[c.id]=value});
  }
  if(GAME_ID==='y06'&&!stage.querySelector('.upper-meter')){const meter=document.createElement('div');meter.className='upper-meter';meter.innerHTML='<b>Seçilen örnek ses düzeyi</b><progress max="1"></progress><small>Oynatma düzeyidir; mikrofon ölçümü değildir.</small>';meter.querySelector('progress').value=state.calan||0;stage.append(meter)}
 }
 let queued=false;new MutationObserver(()=>{if(queued)return;queued=true;queueMicrotask(()=>{queued=false;adapt()})}).observe(document.getElementById('app'),{childList:true,subtree:true});
})();
