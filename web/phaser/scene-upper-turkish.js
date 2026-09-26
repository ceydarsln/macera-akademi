/* Physical destinations only for tasks whose meaning is actually physical. */
(()=>{
 if(!/^[uyz]/.test(GAME_ID))return;
 if(typeof esleCiz==='function'){
  const old=esleCiz;esleCiz=r=>{old(r);if(!['u41','u80','u64'].includes(GAME_ID))return;const slots=[...document.querySelectorAll('[data-yuva]')];if(!slots.length)return;const line=document.createElement('section');line.className=GAME_ID==='u64'?'upper-note-board':'upper-recycle-line';const bins=document.createElement('div');bins.className='upper-recycle-bins';slots[0].parentNode.replaceWith(line);line.append(bins);slots.forEach(slot=>{slot.classList.add('upper-recycle-bin');slot.querySelector('b')?.classList.add('bin-load');bins.append(slot)})};
 }
 if(typeof siraCiz==='function'){
  const old=siraCiz;siraCiz=r=>{old(r);if(!['u63','u83'].includes(GAME_ID))return;document.querySelector('.vagon-dizi')?.classList.add(GAME_ID==='u63'?'upper-film':'upper-holiday-steps')};
 }
})();
