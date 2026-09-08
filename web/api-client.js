(function(){
  'use strict';

  const TOKEN_KEY = 'macera-api-token-v1';
  const UID_KEY = 'macera-api-uid-v1';
  const CACHE_KEY = 'cache-profile-v1';
  const PRODUCTION_API = 'https://maceraakademi.com.tr/api/index.php';
  let healthPromise = null;
  let currentUid = localRead(UID_KEY) || '';

  function localRead(key){
    try{ return window.localStorage.getItem(key) || ''; }catch(e){ return ''; }
  }
  function localWrite(key, value){
    try{
      if(value) window.localStorage.setItem(key, String(value));
      else window.localStorage.removeItem(key);
    }catch(e){}
  }
  function slugify(name){
    return String(name||'').trim().toLowerCase()
      .replace(/ç/g,'c').replace(/ğ/g,'g').replace(/ı/g,'i').replace(/i̇/g,'i')
      .replace(/ö/g,'o').replace(/ş/g,'s').replace(/ü/g,'u')
      .replace(/[^a-z0-9]+/g,'.').replace(/^\.+|\.+$/g,'');
  }
  function withTimeout(promise, ms, label){
    return Promise.race([promise,new Promise(function(_,reject){
      setTimeout(function(){const e=new Error(label||'zaman aşımı');e.code='app/timeout';reject(e);},ms);
    })]);
  }
  function cacheWrite(value){
    try{window.localStorage.setItem(CACHE_KEY,JSON.stringify(value));}catch(e){}
  }
  function cacheRead(){
    try{const value=window.localStorage.getItem(CACHE_KEY);return value?JSON.parse(value):null;}catch(e){return null;}
  }
  function mergeProgress(local,remote){
    if(!local)return remote;if(!remote)return local;
    return {
      uid:remote.uid||local.uid||'',username:remote.username||local.username,
      grade:remote.grade||local.grade,email:remote.email||local.email,
      level:Math.max(local.level||1,remote.level||1),xp:Math.max(local.xp||0,remote.xp||0),
      coins:Math.max(local.coins||0,remote.coins||0),
      completed:Object.assign({},remote.completed||{},local.completed||{}),
      settings:local.settings||remote.settings,
      owned:Array.from(new Set([].concat(remote.owned||[],local.owned||[]))),
      badges:Array.from(new Set([].concat(remote.badges||[],local.badges||[]))),
      coinsEarned:Math.max(local.coinsEarned||0,remote.coinsEarned||0),
      duelStats:Object.assign({},remote.duelStats||{},local.duelStats||{}),
      look:Object.assign({},LOOK_DEFAULT,remote.look||{},local.look||{}),
      teacherCode:remote.teacherCode||local.teacherCode||'',
      teacherUid:remote.teacherUid||local.teacherUid||'',
      teacher:remote.teacher||local.teacher||''
    };
  }
  function apiUrl(){
    try{
      const loc = window.location;
      const web = (loc.protocol === 'http:' || loc.protocol === 'https:') &&
                  loc.hostname !== 'appassets.androidplatform.net';
      if(web) return new URL('api/index.php', loc.href).toString();
    }catch(e){}
    return PRODUCTION_API;
  }
  function apiToken(){ return localRead(TOKEN_KEY); }
  function setApiSession(token, uid){
    localWrite(TOKEN_KEY, token || '');
    localWrite(UID_KEY, uid || '');
    currentUid = uid ? String(uid) : '';
  }
  function clearApiSession(){ setApiSession('', ''); }

  async function apiCall(action, payload, authenticated){
    const body = Object.assign({action:action}, payload || {});
    if(authenticated !== false){
      const token = apiToken();
      if(!token){
        const e = new Error('Oturum bulunamadı. Lütfen yeniden giriş yap.');
        e.code = 'unauthorized';
        throw e;
      }
      body._token = token;
    }
    let response;
    try{
      response = await fetch(apiUrl(), {
        method:'POST',
        headers:{'Content-Type':'application/json', 'X-Macera-Token':apiToken()},
        body:JSON.stringify(body),
        cache:'no-store',
        credentials:'omit'
      });
    }catch(cause){
      const e = new Error('Sunucuya ulaşılamadı. İnternet bağlantını kontrol et.');
      e.code = 'network_error'; e.cause = cause;
      throw e;
    }
    let result = null;
    try{ result = await response.json(); }catch(e){}
    if(!response.ok || !result || result.ok !== true){
      const info = result && result.error ? result.error : {};
      const e = new Error(info.message || ('Sunucu hatası (' + response.status + ')'));
      e.code = info.code || ('http_' + response.status);
      e.status = response.status;
      throw e;
    }
    return result.data || {};
  }

  async function initServer(){
    if(!healthPromise){
      healthPromise = withTimeout(apiCall('health', {}, false), 15000, 'Sunucu yanıt vermedi')
        .catch(function(err){ healthPromise = null; throw err; });
    }
    return healthPromise;
  }
  function currentAuthUser(){
    return Promise.resolve(apiToken() && currentUid ? {uid:String(currentUid)} : null);
  }
  function sunucuHata(err){
    const code = String(err && err.code || '');
    if(code === 'username_taken') return 'Bu kahraman adı zaten alınmış. Başka bir ad dene.';
    if(code === 'invalid_credentials') return 'Kahraman adı veya şifre yanlış.';
    if(code === 'wrong_password') return 'Eski şifre yanlış.';
    if(code === 'rate_limited') return 'Çok fazla deneme yapıldı. Biraz bekleyip tekrar dene.';
    if(code === 'session_expired' || code === 'unauthorized') return 'Oturumun süresi doldu. Tekrar giriş yap.';
    if(code === 'config_missing') return 'Sunucu kurulumu tamamlanmamış. Yapılandırma dosyası eksik.';
    if(code === 'database_unavailable') return 'MySQL veritabanına ulaşılamıyor.';
    if(code === 'network_error' || code === 'app/timeout') return 'Sunucuya ulaşılamadı. İnternet bağlantını kontrol et.';
    return err && err.message ? err.message : 'Bilinmeyen sunucu hatası';
  }

  async function dbRegister(f){
    try{
      await initServer();
      const guest = loadGuest();
      const profile = guest ? {
        level:guest.level||1, xp:guest.xp||0, coins:guest.coins||0,
        completed:guest.completed||{}, look:Object.assign({}, LOOK_DEFAULT, guest.look||{}),
        owned:Array.isArray(guest.owned)?guest.owned:[], badges:Array.isArray(guest.badges)?guest.badges:[],
        coinsEarned:guest.coinsEarned||0, duelStats:guest.duelStats||{},
        settings:guest.settings||{sound:true,music:true,taskNotif:true,rewardNotif:true}
      } : {
        level:1, xp:0, coins:0, completed:{}, look:Object.assign({}, LOOK_DEFAULT),
        owned:[], badges:[], coinsEarned:0, duelStats:{},
        settings:{sound:true,music:true,taskNotif:true,rewardNotif:true}
      };
      const result = await withTimeout(apiCall('register', {
        username:String(f.name||'').trim(), email:String(f.email||'').trim(),
        password:String(f.pass||''), grade:Number(f.grade)||1, profile:profile
      }, false), 20000, 'Hesap sunucusu yanıt vermedi');
      setApiSession(result.token, result.user && result.user.uid);
      if(guest){
        const count = Object.keys(profile.completed).filter(function(k){ return profile.completed[k]; }).length;
        clearGuest(); state.isGuest = false;
        if(count) setTimeout(function(){ toast(count + ' oyunluk ilerlemen hesabına taşındı ✅'); }, 900);
      }
      cacheWrite(result.user);
      return {ok:true, user:result.user};
    }catch(err){ return {ok:false, error:sunucuHata(err)}; }
  }

  async function dbLogin(name, pass){
    name = String(name||'').trim();
    if(!name) return {ok:false, error:'Kahraman adını yaz.'};
    if(!pass) return {ok:false, error:'Şifreni yaz.'};
    try{
      await initServer();
      const result = await withTimeout(apiCall('login', {username:name, password:pass}, false),
                                       20000, 'Hesap sunucusu yanıt vermedi');
      setApiSession(result.token, result.user && result.user.uid);
      cacheWrite(result.user);
      return {ok:true, user:result.user};
    }catch(err){
      const cached = cacheRead();
      if((err.code === 'network_error' || err.code === 'app/timeout') && apiToken() && cached &&
         slugify(cached.username) === slugify(name)){
        toast('İnternet yok — çevrimdışı devam ediliyor 📴');
        return {ok:true, user:cached};
      }
      return {ok:false, error:sunucuHata(err)};
    }
  }

  async function fetchProfile(){
    const result = await withTimeout(apiCall('me', {}), 15000, 'Profil alınamadı');
    if(!result.user) return null;
    currentUid = String(result.user.uid || currentUid || '');
    localWrite(UID_KEY, currentUid);
    const cached = cacheRead();
    const merged = cached && slugify(cached.username) === slugify(result.user.username)
      ? mergeProgress(cached, result.user) : result.user;
    merged.uid = result.user.uid;
    cacheWrite(merged);
    if(merged !== result.user) pushState(merged).catch(function(){});
    return merged;
  }

  async function pushState(s){
    const result = await apiCall('save_profile', {profile:s});
    if(result.class){
      s.teacherCode = result.class.code || s.teacherCode;
      s.teacher = result.class.teacherName || '';
      s.teacherUid = result.class.teacherUid || '';
    }
    return result;
  }

  async function saveState(){
    if(state.isGuest){ saveGuest(); return; }
    if(!state.loggedIn || !state.currentUser) return;
    const snapshot = {
      uid:myUid(), username:state.currentUser, grade:state.hero.grade, email:state.hero.email,
      level:state.hero.level, xp:state.hero.xp, coins:state.hero.coins,
      look:lookGet(), owned:ownedList(), badges:awardedList(),
      coinsEarned:state.hero.coinsEarned||0, duelStats:duelState().stats,
      teacherCode:state.hero.teacherCode||'', teacher:state.hero.teacher||'',
      teacherUid:state.hero.teacherUid||'', settings:state.settings, completed:state.completed
    };
    cacheWrite(snapshot);
    try{ await initServer(); await pushState(snapshot); }catch(e){}
    try{ await pushClassProgress(); }catch(e){}
  }

  async function doLogout(){
    if(state.isGuest){
      clearGuest();
    }else{
      try{ if(apiToken()) await apiCall('logout', {}); }catch(e){}
      clearApiSession();
      try{ window.localStorage.removeItem('cache-profile-v1'); }catch(e){}
    }
    state.isGuest = false; state.loggedIn = false; state.currentUser = null; state.completed = {};
    state.hero = {name:'',grade:1,className:'',teacher:'',teacherCode:'',teacherUid:'',email:'',fullName:'',level:1,xp:0,coins:0,coinsEarned:0,look:Object.assign({},LOOK_DEFAULT)};
    state.owned=[]; state.badges=[]; state.formError='';
    state.friends={loaded:false,loading:false,error:'',list:[],incoming:[],outgoing:[]};
    state.friendSearch={query:'',result:null,searching:false,error:'',existing:null,existingKind:null};
    state.msgs={loaded:false,loading:false,error:'',list:[]};
    go('welcome');
  }

  async function verifySessionInBackground(optimistic){
    if(!apiToken()){
      if(optimistic){
        try{ window.localStorage.removeItem('cache-profile-v1'); }catch(e){}
        clearApiSession(); await doLogout(); toast('Tekrar giriş yapman gerekiyor 🔑');
      }
      return;
    }
    try{
      await initServer();
      const user = await fetchProfile();
      if(user){
        const oldScreen = state.screen;
        window.applyUser(user);
        if(oldScreen==='welcome'||oldScreen==='login') go('home');
        else if(oldScreen!=='gamePlayer') renderAll();
      }
    }catch(err){
      if(err.code==='session_expired'||err.code==='unauthorized'){
        clearApiSession();
        try{ window.localStorage.removeItem('cache-profile-v1'); }catch(e){}
        if(optimistic){ await doLogout(); toast('Tekrar giriş yapman gerekiyor 🔑'); }
      }else if(optimistic){ setTimeout(function(){ toast('Çevrimdışı mod 📴'); },500); }
    }
  }

  function myUid(){ return currentUid || localRead(UID_KEY) || null; }
  async function writeUsernameIndex(){ return; }

  async function duelCreate(p){
    const r = await withTimeout(apiCall('duel_create', {
      oppUid:p.oppUid, grade:p.grade, catId:p.catId, catLabel:p.catLabel,
      seed:p.seed, score:p.score, correct:p.correct,
      answers:p.answers.map(function(a){return {ok:a.ok,ms:a.ms,score:a.score};})
    }),12000,'Meydan okuma gönderilemedi');
    return r.id;
  }
  async function duelRespond(p){
    await withTimeout(apiCall('duel_respond', {
      duelId:p.duelId, score:p.score, correct:p.correct,
      answers:p.answers.map(function(a){return {ok:a.ok,ms:a.ms,score:a.score};})
    }),12000,'Sonuç kaydedilemedi');
  }
  async function duelsLoad(){
    const d=duelState();
    if(!duelCanOnline()){d.loaded=true;return;}
    d.loading=true;d.error='';renderAll();
    try{
      const r=await withTimeout(apiCall('duels_list',{}),12000,'Yarışmalar alınamadı');
      d.list=Array.isArray(r.list)?r.list:[];d.loaded=true;
    }catch(err){d.error=sunucuHata(err);}
    d.loading=false;renderAll();
  }
  async function duelClaim(id){
    const d=duelState(),m=d.list.find(function(x){return x.id===id;}),me=myUid();
    if(!m||m.status!=='done'||(m.claimed||[]).indexOf(me)>=0)return;
    try{
      const claim=await withTimeout(apiCall('duel_claim',{duelId:id}),10000,'Ödül alınamadı');
      if(!claim.claimed){ toast('Bu düellonun ödülü daha önce alınmış.'); return; }
    }catch(err){ toast('Ödül alınamadı: '+sunucuHata(err)); return; }
    const res=m.winner==='draw'?'draw':(m.winner===me?'win':'loss');
    const mine=m.from===me?m.fromCorrect:m.toCorrect;
    const aw=duelAward(res,mine===DUEL_Q,false);
    m.claimed=(m.claimed||[]).concat([me]);
    d.result={kind:'claim',res:res,award:aw,myScore:(m.from===me?m.fromScore:m.toScore),
      oppScore:(m.from===me?m.toScore:m.fromScore),oppName:(m.from===me?m.toName:m.fromName),catLabel:m.catLabel};
    go('duelResult');
  }

  async function resolveTeacherUid(){
    if(state.hero.teacherUid)return state.hero.teacherUid;
    const code=myClassCode();if(!code)return '';
    try{
      const r=await apiCall('class_lookup',{code:code});
      if(r.class){state.hero.teacherUid=r.class.teacherUid||'';state.hero.teacher=r.class.teacherName||r.class.name||'';}
    }catch(e){}
    return state.hero.teacherUid||'';
  }
  async function pushClassProgress(){
    if(!clsCanOnline())return;
    const ids=Object.keys(state.completed).filter(function(k){return state.completed[k];});
    await withTimeout(apiCall('class_progress',{
      code:myClassCode(),grade:state.hero.grade,level:state.hero.level,xp:state.hero.xp,coins:state.hero.coins,
      doneIds:ids,duelWins:duelWins(),duelBest:duelState().stats.best||0
    }),10000,'İlerleme gönderilemedi');
  }
  async function clsLoad(){
    const c=clsState();
    if(!clsCanOnline()){c.loaded=true;c.assign=[];c.contests=[];renderAll();return;}
    c.loading=true;c.error='';renderAll();
    try{
      const r=await withTimeout(apiCall('class_data',{code:myClassCode()}),12000,'Sınıf verileri alınamadı');
      c.assign=Array.isArray(r.assignments)?r.assignments:[];
      c.contests=Array.isArray(r.contests)?r.contests:[];
      c.loaded=true;
    }catch(err){c.error=sunucuHata(err);}
    c.loading=false;renderAll();
  }
  async function contestSubmit(p){
    await withTimeout(apiCall('contest_submit',{
      contestId:p.contestId,score:p.score,correct:p.correct,grade:p.grade
    }),12000,'Skor gönderilemedi');
  }
  async function contestBoard(contestId){
    const c=clsState();c.board={id:contestId,loading:true,error:'',list:[]};renderAll();
    try{
      const r=await withTimeout(apiCall('contest_board',{contestId:contestId}),12000,'Sıralama alınamadı');
      c.board.list=Array.isArray(r.list)?r.list:[];
    }catch(err){c.board.error=sunucuHata(err);}
    c.board.loading=false;renderAll();
  }

  async function saveTeacherCode(){
    const el=document.getElementById('teacherCode');
    const code=el?el.value.trim().toUpperCase().replace(/\s+/g,''):'';
    let cls=null;
    if(code){
      try{const r=await apiCall('class_lookup',{code:code});cls=r.class||null;}
      catch(err){toast('Kod kontrol edilemedi: '+sunucuHata(err));return;}
      if(!cls){toast('Bu sınıf kodu bulunamadı.');return;}
    }
    state.hero.teacherCode=code;
    state.hero.teacher=cls?(cls.teacherName||cls.name||''):'';
    state.hero.teacherUid=cls?(cls.teacherUid||''):'';
    await saveState();
    if(state.cls){state.cls.loaded=false;state.cls.assign=[];state.cls.contests=[];}
    if(code){try{await pushClassProgress();}catch(e){} clsLoad();}
    toast(code?'Öğretmen kodu kaydedildi ✅':'Öğretmen kodu temizlendi');renderAll();
  }
  async function doChangePass(){
    const oldP=(document.getElementById('cpOld')||{}).value||'';
    const newP=(document.getElementById('cpNew')||{}).value||'';
    const newP2=(document.getElementById('cpNew2')||{}).value||'';
    if(newP.length<6)return setFormError('Yeni şifre en az 6 karakter olmalı.');
    if(newP!==newP2)return setFormError('Yeni şifreler birbiriyle aynı değil.');
    try{
      await apiCall('change_password',{oldPassword:oldP,newPassword:newP});
      state.formError='';toast('Şifren güncellendi 🔐');go('account');
    }catch(err){setFormError('Şifre güncellenemedi: '+sunucuHata(err));}
  }
  async function reallyDeleteAccount(){
    if(state.isGuest){state.confirmDelete=false;clearGuest();await doLogout();toast('İlerleme sıfırlandı.');return;}
    try{
      const password=(document.getElementById('delete-account-password')||{}).value||'';
      if(!password)throw new Error('Hesabı silmek için parolanı yaz.');
      await apiCall('delete_account',{password:password});
      state.confirmDelete=false;clearApiSession();
      try{window.localStorage.removeItem('cache-profile-v1');}catch(e){}
      await doLogout();toast('Hesabın ve tüm verilerin silindi.');
    }catch(err){state.confirmDelete=true;renderAll();setTimeout(function(){toast('Hesap silinemedi: '+sunucuHata(err));},50);}
  }

  async function friendLookup(name){
    const key=String(name||'').trim();
    if(key.length<3)return {ok:false,error:'Kahraman adını tam yaz (en az 3 harf).'};
    if(state.currentUser&&slugify(key)===slugify(state.currentUser))return {ok:false,error:'Bu senin kendi adın 🙂'};
    try{
      const r=await withTimeout(apiCall('friend_lookup',{username:key}),10000,'Sunucu yanıt vermedi');
      return r.user?{ok:true,user:r.user}:{ok:false,error:'Böyle bir kahraman bulunamadı. Adı doğru yazdığından emin ol.'};
    }catch(err){return {ok:false,error:sunucuHata(err)};}
  }
  async function friendsLoad(){
    if(state.isGuest)return;
    state.friends.loading=true;state.friends.error='';renderAll();
    try{
      const r=await withTimeout(apiCall('friends_list',{}),12000,'Arkadaş listesi alınamadı');
      state.friends.list=r.friends||[];state.friends.incoming=r.incoming||[];state.friends.outgoing=r.outgoing||[];
      state.friends.loaded=true;
    }catch(err){state.friends.error=sunucuHata(err);}
    state.friends.loading=false;renderAll();
  }
  async function friendRequestSend(uid,username){
    try{await apiCall('friend_request',{uid:uid});toast(username+' kişisine istek gönderildi 👋');
      state.friendSearch={query:'',result:null,searching:false,error:''};await friendsLoad();}
    catch(err){toast('Gönderilemedi: '+sunucuHata(err));}
  }
  async function friendRequestAccept(uid){
    try{await apiCall('friend_accept',{uid:uid});toast('Artık arkadaşsınız! 🎉');await friendsLoad();}
    catch(err){toast('Olmadı: '+sunucuHata(err));await friendsLoad();}
  }
  async function friendRemove(uid,silent){
    try{await apiCall('friend_remove',{uid:uid});if(!silent)toast('Arkadaşlıktan çıkarıldı');state.friendModal=null;await friendsLoad();}
    catch(err){toast('Olmadı: '+sunucuHata(err));}
  }
  async function messagesLoad(){
    if(state.isGuest)return;
    state.msgs.loading=true;state.msgs.error='';renderAll();
    try{const r=await apiCall('messages_list',{});state.msgs.list=r.list||[];state.msgs.loaded=true;}
    catch(err){state.msgs.error=sunucuHata(err);}
    state.msgs.loading=false;renderAll();
  }
  async function messagesMarkRead(){
    try{await apiCall('messages_read',{});state.msgs.list.forEach(function(m){m.readAt=m.readAt||'ok';});renderAll();}catch(e){}
  }
  async function messageSend(uid,presetId){
    if(!MESSAGE_PRESETS.some(function(p){return p.id===presetId;}))return;
    try{await apiCall('message_send',{uid:uid,presetId:presetId});toast('Mesaj gönderildi ✉️');state.friendModal=null;renderAll();}
    catch(err){toast('Gönderilemedi: '+sunucuHata(err));}
  }

  async function runDiagnostics(){
    diagResults=[];diagRunning=true;renderAll();
    const proto=(function(){try{return window.location.protocol;}catch(e){return'?';}})();
    diagAdd(proto==='file:'?'⚠️':'✅','Sayfa adresi',proto==='file:'?'Dosya cihazdan açılıyor; canlı API adresi kullanılacak.':proto+' — uygun.');
    const online=(function(){try{return navigator.onLine!==false;}catch(e){return true;}})();
    diagAdd(online?'✅':'❌','İnternet',online?'Tarayıcı çevrimiçi görünüyor.':'Tarayıcı çevrimdışı. Bağlantıyı aç.');
    try{
      const r=await withTimeout(apiCall('health',{},false),15000,'Sunucu yanıt vermedi');
      diagAdd('✅','PHP API','Sunucu yanıt verdi.');
      diagAdd(r.database==='mysql'?'✅':'⚠️','MySQL',r.database==='mysql'?'Veritabanı bağlantısı çalışıyor.':'Beklenmeyen veritabanı yanıtı.');
    }catch(err){diagAdd('❌','PHP/MySQL',sunucuHata(err));diagRunning=false;renderAll();return;}
    try{window.localStorage.setItem('__test__','1');window.localStorage.removeItem('__test__');diagAdd('✅','Cihaz depolaması','Çalışıyor — oturum açık kalabilir.');}
    catch(e){diagAdd('❌','Cihaz depolaması','Engelli. Gizli sekme veya tarayıcı ayarı olabilir.');}
    diagRunning=false;renderAll();
  }

  const originalApplyUser=window.applyUser;
  function applyUserWithSession(rec){
    if(rec&&rec.uid){currentUid=String(rec.uid);localWrite(UID_KEY,currentUid);}
    return originalApplyUser(rec);
  }

  window.initServer=initServer;
  window.withTimeout=withTimeout;
  window.cacheRead=cacheRead;
  window.cacheWrite=cacheWrite;
  window.currentAuthUser=currentAuthUser;
  window.firebaseHata=sunucuHata;
  window.dbRegister=dbRegister;
  window.dbLogin=dbLogin;
  window.fetchProfile=fetchProfile;
  window.pushState=pushState;
  window.saveState=saveState;
  window.doLogout=doLogout;
  window.verifySessionInBackground=verifySessionInBackground;
  window.myUid=myUid;
  window.writeUsernameIndex=writeUsernameIndex;
  window.duelCreate=duelCreate;
  window.duelRespond=duelRespond;
  window.duelsLoad=duelsLoad;
  window.duelClaim=duelClaim;
  window.resolveTeacherUid=resolveTeacherUid;
  window.pushClassProgress=pushClassProgress;
  window.clsLoad=clsLoad;
  window.contestSubmit=contestSubmit;
  window.contestBoard=contestBoard;
  window.saveTeacherCode=saveTeacherCode;
  window.doChangePass=doChangePass;
  window.reallyDeleteAccount=reallyDeleteAccount;
  window.friendLookup=friendLookup;
  window.friendsLoad=friendsLoad;
  window.friendRequestSend=friendRequestSend;
  window.friendRequestAccept=friendRequestAccept;
  window.friendRemove=friendRemove;
  window.messagesLoad=messagesLoad;
  window.messagesMarkRead=messagesMarkRead;
  window.messageSend=messageSend;
  window.runDiagnostics=runDiagnostics;
  window.applyUser=applyUserWithSession;
})();
