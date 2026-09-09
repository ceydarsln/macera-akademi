'use strict';

const API_URL = '../api/teacher.php';
const TOKEN_KEY = 'macera_teacher_token';
const SUBJECTS = {
  math: ['➗', 'Matematik'], turkish: ['📚', 'Türkçe'], count: ['🔢', 'Sayma'],
  life: ['🌱', 'Hayat Bilgisi'], social: ['🌍', 'Sosyal Bilgiler'], science: ['🔬', 'Fen Bilimleri']
};
const CONTEST_CATEGORIES = [
  ['topla', '➕', 'Toplama', [1, 2, 3, 4]], ['cikar', '➖', 'Çıkarma', [1, 2, 3, 4]],
  ['carp', '✖️', 'Çarpma', [2, 3, 4]], ['bol', '➗', 'Bölme', [3, 4]],
  ['sayi', '🔢', 'Sayılar ve Örüntü', [1, 2]], ['kesir', '🍕', 'Kesirler', [3, 4]],
  ['saat', '🕐', 'Saat ve Para', [2, 3]], ['hece', '🔤', 'Hece ve Sözcük', [1, 2]],
  ['eszit', '🔁', 'Eş ve Zıt Anlam', [2, 3, 4]], ['essesli', '🎭', 'Eş Sesli Sözcükler', [3, 4]],
  ['nokta', '✍️', 'Noktalama ve Yazım', [3, 4]], ['mix', '🎲', 'Karışık Dersler', [1, 2, 3, 4]]
];

const state = {
  token: localStorage.getItem(TOKEN_KEY) || '',
  authMode: 'login', teacher: null, tab: 'dashboard', loading: true, busy: false,
  error: '', ok: '', catalog: [], students: [], assignments: [], contests: [],
  counts: {students: 0, assignments: 0, contests: 0},
  assignGrade: 1, assignSubject: 'math', contestGrade: 1, selected: new Set(), modal: null
};

const app = document.getElementById('app');
const toastNode = document.getElementById('toast');

function esc(value) {
  return String(value ?? '').replace(/[&<>'"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'}[c]));
}

function todayIso() {
  const d = new Date();
  const z = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${z(d.getMonth() + 1)}-${z(d.getDate())}`;
}

function addDays(iso, days) {
  const d = new Date(`${iso}T12:00:00`);
  d.setDate(d.getDate() + days);
  const z = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${z(d.getMonth() + 1)}-${z(d.getDate())}`;
}

function trDate(iso) {
  if (!iso) return 'süresiz';
  const d = new Date(`${iso}T12:00:00`);
  return Number.isNaN(d.getTime()) ? iso : new Intl.DateTimeFormat('tr-TR').format(d);
}

function toast(message) {
  toastNode.textContent = message;
  toastNode.classList.add('show');
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => toastNode.classList.remove('show'), 2800);
}

async function api(action, payload = {}) {
  const headers = {'Content-Type': 'application/json'};
  if (state.token) headers['X-Macera-Token'] = state.token;
  const response = await fetch(API_URL, {
    method: 'POST', headers, credentials: 'same-origin',
    body: JSON.stringify({...payload, action})
  });
  let body;
  try { body = await response.json(); } catch (_) { body = null; }
  if (!response.ok || !body?.ok) {
    const error = new Error(body?.error?.message || 'Sunucuyla bağlantı kurulamadı.');
    error.code = body?.error?.code || 'network_error';
    error.status = response.status;
    if (response.status === 401) clearSession(false);
    throw error;
  }
  return body.data || {};
}

function setMessage(type, message) {
  state.error = type === 'error' ? message : '';
  state.ok = type === 'ok' ? message : '';
  render();
}

function clearSession(showMessage = true) {
  state.token = '';
  state.teacher = null;
  state.loading = false;
  localStorage.removeItem(TOKEN_KEY);
  if (showMessage) state.ok = 'Oturum kapatıldı.';
}

async function boot() {
  try {
    const response = await fetch('catalog.json', {cache: 'no-cache'});
    if (response.ok) state.catalog = await response.json();
  } catch (_) {
    state.catalog = [];
  }
  if (!state.token) {
    state.loading = false;
    render();
    return;
  }
  try {
    const data = await api('me');
    state.teacher = data.teacher;
    setDefaults();
    await refreshAll(false);
  } catch (error) {
    clearSession(false);
    state.error = error.message;
  }
  state.loading = false;
  render();
}

function setDefaults() {
  const grade = Number(state.teacher?.class?.grade || 1);
  state.assignGrade = grade;
  state.contestGrade = grade;
  state.assignSubject = subjectsFor(grade)[0] || 'math';
}

async function refreshAll(draw = true) {
  if (draw) { state.loading = true; render(); }
  const [overview, students, assignments, contests] = await Promise.all([
    api('overview'), api('students_list'), api('assignments_list'), api('contests_list')
  ]);
  state.teacher = overview.teacher;
  state.counts = overview.counts;
  state.students = students.list || [];
  state.assignments = assignments.list || [];
  state.contests = contests.list || [];
  state.loading = false;
  if (draw) render();
}

async function refreshAssignments() {
  const [overview, assignments, students] = await Promise.all([
    api('overview'), api('assignments_list'), api('students_list')
  ]);
  state.teacher = overview.teacher; state.counts = overview.counts;
  state.assignments = assignments.list || []; state.students = students.list || [];
  render();
}

async function refreshContests() {
  const [overview, contests] = await Promise.all([api('overview'), api('contests_list')]);
  state.teacher = overview.teacher; state.counts = overview.counts; state.contests = contests.list || [];
  render();
}

function subjectsFor(grade) {
  return [...new Set(state.catalog.filter(c => Number(c.gr) === Number(grade)).map(c => c.s))];
}

function catalogFor(grade, subject) {
  return state.catalog.filter(c => Number(c.gr) === Number(grade) && c.s === subject);
}

function gameTitle(id) {
  for (const group of state.catalog) {
    const game = (group.g || []).find(item => item[0] === id);
    if (game) return game[1];
  }
  return id;
}

function renderMessage() {
  if (state.error) return `<div class="message error">⚠️ ${esc(state.error)}</div>`;
  if (state.ok) return `<div class="message ok">✓ ${esc(state.ok)}</div>`;
  return '';
}

function renderAuth() {
  const register = state.authMode === 'register';
  return `<div class="auth-shell">
    <section class="auth-story">
      <div class="auth-brand"><span class="brand-mark">MA</span> Macera Akademi</div>
      <h1>Sınıfınızın macerası tek panelde.</h1>
      <p>Öğrencilerin ilerlemesini izleyin, müfredat oyunlarından ödev hazırlayın ve sınıf yarışmaları açın.</p>
      <div class="feature-list">
        <span><b>👩‍🎓</b> Öğrenci ilerlemesini anlık izleyin</span>
        <span><b>📝</b> 658 oyundan ödev oluşturun</span>
        <span><b>🏆</b> Günlük ve haftalık yarışmalar açın</span>
      </div>
    </section>
    <section class="auth-side"><div class="auth-card">
      <h2>${register ? 'Öğretmen hesabı açın' : 'Tekrar hoş geldiniz'}</h2>
      <p class="sub">${register ? 'Sınıf kodunuz hesapla birlikte otomatik oluşturulur.' : 'Öğretmen panelinize giriş yapın.'}</p>
      <div class="auth-tabs">
        <button type="button" data-auth="login" class="${register ? '' : 'on'}">Giriş</button>
        <button type="button" data-auth="register" class="${register ? 'on' : ''}">Kayıt</button>
      </div>
      ${renderMessage()}
      <form id="authForm">
        ${register ? `<div class="field"><label>AD SOYAD</label><input name="fullName" maxlength="120" autocomplete="name" required></div>
          <div class="grid2"><div class="field"><label>SINIF ADI</label><input name="className" maxlength="120" placeholder="Örn. 3-A" required></div>
          <div class="field"><label>SINIF DÜZEYİ</label><select name="grade">${gradeOptions(1)}</select></div></div>
          <div class="field"><label>E-POSTA (İSTEĞE BAĞLI)</label><input name="email" maxlength="190" type="email" autocomplete="email"></div>` : ''}
        <div class="field"><label>KULLANICI ADI</label><input name="username" maxlength="80" autocomplete="username" required></div>
        <div class="field"><label>ŞİFRE</label><input name="password" type="password" minlength="8" maxlength="200" autocomplete="${register ? 'new-password' : 'current-password'}" required></div>
        <button class="btn btn-primary btn-block" ${state.busy ? 'disabled' : ''}>${state.busy ? 'Bekleyin…' : (register ? 'Hesap ve sınıf oluştur' : 'Giriş yap')}</button>
      </form>
      <p class="note">Bu panel ve öğrenci uygulaması aynı güvenli MySQL veritabanını kullanır.</p>
    </div></section>
  </div>`;
}

function gradeOptions(selected) {
  return [1, 2, 3, 4].map(n => `<option value="${n}" ${Number(selected) === n ? 'selected' : ''}>${n}. sınıf</option>`).join('');
}

const NAV = [
  ['dashboard', '🏠', 'Genel Bakış'], ['students', '👩‍🎓', 'Öğrenciler'],
  ['assignments', '📝', 'Ödevler'], ['contests', '🏆', 'Yarışmalar'], ['settings', '⚙️', 'Ayarlar']
];

function renderNav(mobile = false) {
  return `<nav class="${mobile ? 'mobile-nav' : 'nav'}">${NAV.map(([id, icon, label]) =>
    `<button type="button" data-tab="${id}" class="${state.tab === id ? 'on' : ''}">${mobile ? `<b>${icon}</b>` : `${icon} `}${label}</button>`
  ).join('')}</nav>`;
}

function renderApp() {
  const teacher = state.teacher;
  const cls = teacher?.class || {code: '-', name: 'Sınıf', grade: 1};
  const label = NAV.find(item => item[0] === state.tab)?.[2] || 'Öğretmen Paneli';
  return `<div class="app-shell">
    <aside class="sidebar">
      <div class="side-brand"><span class="brand-mark">MA</span><span>Macera<br>Akademi</span></div>
      ${renderNav(false)}
      <div class="side-foot"><strong>${esc(teacher.fullName || teacher.username)}</strong>${esc(cls.name)} · ${esc(cls.grade)}. sınıf</div>
    </aside>
    <main class="main">
      <header class="topbar"><div><h1>${esc(label)}</h1><p>${esc(teacher.fullName || teacher.username)}</p></div>
        <div class="class-chip"><span>Sınıf kodu</span><b>${esc(cls.code)}</b></div></header>
      <div class="content">${state.loading ? '<div class="card">Veriler yükleniyor…</div>' : renderPage()}</div>
    </main>
    ${renderNav(true)}
    ${renderModal()}
  </div>`;
}

function renderPage() {
  const pages = {dashboard: renderDashboard, students: renderStudents, assignments: renderAssignments, contests: renderContests, settings: renderSettings};
  return `${renderMessage()}${(pages[state.tab] || renderDashboard)()}`;
}

function pageHead(title, text, action = '') {
  return `<div class="page-head"><div><h2>${title}</h2><p>${text}</p></div>${action}</div>`;
}

function renderDashboard() {
  const cls = state.teacher.class;
  const recent = state.students.slice(0, 5);
  return `${pageHead('Sınıfınız hazır ✨', `${esc(cls.name)} için genel durum ve hızlı işlemler.`)}
    <section class="stats">
      <article class="stat"><span class="emoji">👩‍🎓</span><strong>${state.counts.students}</strong><span>Kodu giren öğrenci</span></article>
      <article class="stat"><span class="emoji">📝</span><strong>${state.counts.assignments}</strong><span>Aktif ödev</span></article>
      <article class="stat"><span class="emoji">🏆</span><strong>${state.counts.contests}</strong><span>Aktif yarışma</span></article>
    </section>
    <section class="card"><div class="code-box"><div><span>Öğrencilerin kullanacağı sınıf kodu</span><strong>${esc(cls.code)}</strong><p>Öğrenci uygulamasında Profil → Öğretmen Kodu alanına yazılır.</p></div><button type="button" class="btn btn-green" data-action="copy-code">Kodu kopyala</button></div></section>
    <section class="card"><div class="card-head"><div><h3>Hızlı işlemler</h3><span class="note">Sık kullanılan araçlara geçin.</span></div></div>
      <div class="quick"><button data-tab="students"><span>👩‍🎓</span>Öğrencileri gör</button><button data-tab="assignments"><span>📝</span>Ödev oluştur</button><button data-tab="contests"><span>🏆</span>Yarışma aç</button></div></section>
    <section class="card"><div class="card-head"><h3>Son öğrenci durumları</h3><button class="btn btn-soft btn-small" data-action="refresh">Yenile</button></div>
      ${recent.length ? renderStudentTable(recent) : empty('🧭', 'Henüz öğrenci yok', 'Öğrenciler sınıf kodunu yazınca burada görünecek.')}
    </section>`;
}

function empty(icon, title, text) {
  return `<div class="empty"><div style="font-size:34px">${icon}</div><b>${title}</b><span>${text}</span></div>`;
}

function renderStudentTable(list) {
  return `<div class="table-wrap"><table class="table"><thead><tr><th>ÖĞRENCİ</th><th>SINIF</th><th class="num">SEVİYE</th><th class="num">XP</th><th class="num">TAMAMLANAN</th><th>SON GÜNCELLEME</th></tr></thead><tbody>${list.map(s =>
    `<tr><td><b>${esc(s.username)}</b></td><td>${s.grade}. sınıf</td><td class="num">${s.level}</td><td class="num">${s.xp}</td><td class="num">${s.doneCount}</td><td>${esc(s.updatedAt || '-')}</td></tr>`
  ).join('')}</tbody></table></div>`;
}

function renderStudents() {
  return `${pageHead('Öğrenciler', 'Sınıf kodunu giren öğrencilerin güncel ilerlemesi.', '<button class="btn btn-soft" data-action="refresh">🔄 Yenile</button>')}
    <section class="card">${state.students.length ? renderStudentTable(state.students) : empty('👩‍🎓', 'Henüz öğrenci bağlanmadı', 'Sınıf kodunu öğrencilerle paylaşın.')}</section>`;
}

function assignmentProgress(assignment) {
  const ids = assignment.gameIds || [];
  if (!ids.length || !state.students.length) return {done: 0, partial: 0, percent: 0};
  let done = 0, partial = 0, total = 0;
  state.students.forEach(student => {
    const completed = student.doneIds || [];
    const count = ids.filter(id => completed.includes(id)).length;
    total += count;
    if (count >= ids.length) done++; else if (count > 0) partial++;
  });
  return {done, partial, percent: Math.round(total / (ids.length * state.students.length) * 100)};
}

function renderAssignments() {
  const subjects = subjectsFor(state.assignGrade);
  if (!subjects.includes(state.assignSubject)) state.assignSubject = subjects[0] || 'math';
  const groups = catalogFor(state.assignGrade, state.assignSubject);
  const subjectOptions = subjects.map(id => `<option value="${id}" ${id === state.assignSubject ? 'selected' : ''}>${SUBJECTS[id]?.[0] || '📘'} ${SUBJECTS[id]?.[1] || id}</option>`).join('');
  return `${pageHead('Ödevler', 'Müfredat oyunlarını seçip sınıfınıza gönderin.')}
    <section class="card"><h3>Yeni ödev oluştur</h3><p class="sub">Sınıf ve dersi seçin, ardından ödeve eklenecek oyunları işaretleyin.</p>
      <form id="assignmentForm">
        <div class="grid2"><div class="field"><label>SINIF DÜZEYİ</label><select id="assignGrade">${gradeOptions(state.assignGrade)}</select></div>
          <div class="field"><label>DERS</label><select id="assignSubject">${subjectOptions}</select></div></div>
        <div class="grid2"><div class="field"><label>ÖDEV BAŞLIĞI</label><input name="title" maxlength="160" placeholder="Örn. Hafta sonu matematik" required></div>
          <div class="field"><label>TESLİM TARİHİ</label><input name="due" type="date"></div></div>
        <div class="field"><label>ÖĞRETMEN NOTU</label><textarea name="note" maxlength="500" placeholder="İsteğe bağlı kısa açıklama"></textarea></div>
        <div class="catalog-tools"><b><span id="selectedCount">${state.selected.size}</span> oyun seçildi</b><div><button type="button" class="btn btn-soft btn-small" data-action="select-all">Tümünü seç</button> <button type="button" class="btn btn-soft btn-small" data-action="clear-games">Temizle</button></div></div>
        <div class="catalog">${groups.length ? groups.map(group => `<fieldset class="catalog-group"><legend>${esc(group.n)}</legend><div class="game-grid">${(group.g || []).map(game =>
          `<label class="game"><input type="checkbox" data-game-id="${esc(game[0])}" ${state.selected.has(game[0]) ? 'checked' : ''}><span>${esc(game[2])} ${esc(game[1])}</span></label>`
        ).join('')}</div></fieldset>`).join('') : '<div class="message error">Bu seçim için oyun kataloğu bulunamadı.</div>'}</div>
        <button class="btn btn-primary" ${state.busy ? 'disabled' : ''}>📝 Ödevi gönder</button>
      </form>
    </section>
    <section class="card"><div class="card-head"><h3>Hazırlanan ödevler</h3><button class="btn btn-soft btn-small" data-action="refresh-assignments">🔄 Yenile</button></div>
      ${state.assignments.length ? `<div class="list">${state.assignments.map(renderAssignmentRow).join('')}</div>` : empty('📝', 'Henüz ödev yok', 'İlk ödevinizi yukarıdaki formdan oluşturun.')}
    </section>`;
}

function renderAssignmentRow(a) {
  const p = assignmentProgress(a);
  const expired = a.due && a.due < todayIso();
  return `<article class="list-row ${a.active ? '' : 'off'}"><div class="list-icon">📝</div><div class="list-main">
    <strong>${esc(a.title)}</strong><p>${(a.gameIds || []).length} oyun · ${a.grade}. sınıf · ${esc(SUBJECTS[a.subj]?.[1] || a.subj)} · ${a.due ? `teslim ${trDate(a.due)}` : 'süresiz'}${a.note ? ` · ${esc(a.note)}` : ''}</p>
    <p>${(a.gameIds || []).slice(0, 4).map(gameTitle).map(esc).join(' · ')}${(a.gameIds || []).length > 4 ? ' …' : ''}</p>
    <div class="progress"><i style="width:${p.percent}%"></i></div><p><b>${p.done}</b>/${state.students.length} tamamladı${p.partial ? ` · ${p.partial} başladı` : ''} · %${p.percent} genel</p></div>
    <div class="row-actions"><span class="pill ${!a.active ? 'red' : expired ? 'yellow' : 'green'}">${!a.active ? 'kapalı' : expired ? 'süresi geçti' : 'açık'}</span>
      <button type="button" class="btn btn-soft btn-small" data-action="assignment-who" data-id="${esc(a.id)}">Kim yaptı?</button>
      <button type="button" class="btn btn-soft btn-small" data-action="assignment-toggle" data-id="${esc(a.id)}" data-active="${a.active ? '0' : '1'}">${a.active ? 'Kapat' : 'Aç'}</button>
      <button type="button" class="btn btn-danger btn-small" data-action="assignment-delete" data-id="${esc(a.id)}">Sil</button></div></article>`;
}

function categoriesFor(grade) {
  return CONTEST_CATEGORIES.filter(cat => cat[3].includes(Number(grade)));
}

function renderContests() {
  const categories = categoriesFor(state.contestGrade);
  return `${pageHead('Yarışmalar', 'Aynı sorularla günlük veya haftalık sınıf yarışması açın.')}
    <section class="card"><h3>Yeni yarışma</h3><p class="sub">Öğrenciler yarışmayı uygulamadaki Yarışma Arenası bölümünde görür.</p>
      <form id="contestForm"><div class="grid3">
        <div class="field"><label>SINIF DÜZEYİ</label><select id="contestGrade">${gradeOptions(state.contestGrade)}</select></div>
        <div class="field"><label>TÜR</label><select name="kind"><option value="daily">☀️ Günlük</option><option value="weekly">🗓️ Haftalık</option></select></div>
        <div class="field"><label>BAŞLANGIÇ</label><input name="startsAt" type="date" value="${todayIso()}" required></div>
      </div><div class="grid2">
        <div class="field"><label>KONU</label><select name="catId">${categories.map(cat => `<option value="${cat[0]}">${cat[1]} ${cat[2]}</option>`).join('')}</select></div>
        <div class="field"><label>BAŞLIK</label><input name="title" maxlength="160" placeholder="Örn. Cuma Çarpım Turnuvası"></div>
      </div><button class="btn btn-primary" ${state.busy ? 'disabled' : ''}>🏆 Yarışmayı aç</button></form>
      <p class="note">Günlük yarışma 1 gün, haftalık yarışma 7 gün açık kalır. Her yarışma 8 sorudur.</p>
    </section>
    <section class="card"><div class="card-head"><h3>Açılan yarışmalar</h3><button class="btn btn-soft btn-small" data-action="refresh-contests">🔄 Yenile</button></div>
      ${state.contests.length ? `<div class="list">${state.contests.map(renderContestRow).join('')}</div>` : empty('🏟️', 'Henüz yarışma yok', 'İlk yarışmanızı yukarıdaki formdan açın.')}
    </section>`;
}

function renderContestRow(c) {
  const ended = c.endsAt && c.endsAt < todayIso();
  return `<article class="list-row ${c.active ? '' : 'off'}"><div class="list-icon">${c.kind === 'weekly' ? '🗓️' : '☀️'}</div><div class="list-main"><strong>${esc(c.title)}</strong><p>${esc(c.catLabel)} · ${c.grade}. sınıf · ${trDate(c.startsAt)} → ${trDate(c.endsAt)}</p></div>
    <div class="row-actions"><span class="pill ${!c.active ? 'red' : ended ? 'yellow' : 'green'}">${!c.active ? 'kapalı' : ended ? 'bitti' : 'açık'}</span>
      <button type="button" class="btn btn-soft btn-small" data-action="contest-board" data-id="${esc(c.id)}">Sıralama</button>
      <button type="button" class="btn btn-soft btn-small" data-action="contest-toggle" data-id="${esc(c.id)}" data-active="${c.active ? '0' : '1'}">${c.active ? 'Kapat' : 'Aç'}</button>
      <button type="button" class="btn btn-danger btn-small" data-action="contest-delete" data-id="${esc(c.id)}">Sil</button></div></article>`;
}

function renderSettings() {
  const t = state.teacher, cls = t.class;
  return `${pageHead('Ayarlar', 'Öğretmen ve sınıf bilgilerini yönetin.')}
    <section class="card"><h3>Profil ve sınıf</h3><form id="profileForm">
      <div class="grid2"><div class="field"><label>AD SOYAD</label><input name="fullName" maxlength="120" value="${esc(t.fullName)}" required></div><div class="field"><label>E-POSTA</label><input name="email" maxlength="190" type="email" value="${esc(t.email)}"></div></div>
      <div class="grid2"><div class="field"><label>SINIF ADI</label><input name="className" maxlength="120" value="${esc(cls.name)}" required></div><div class="field"><label>SINIF DÜZEYİ</label><select name="grade">${gradeOptions(cls.grade)}</select></div></div>
      <button class="btn btn-primary">Bilgileri kaydet</button></form></section>
    <section class="card"><h3>Şifre değiştir</h3><form id="passwordForm"><div class="grid2"><div class="field"><label>MEVCUT ŞİFRE</label><input name="oldPassword" type="password" autocomplete="current-password" required></div><div class="field"><label>YENİ ŞİFRE</label><input name="newPassword" type="password" minlength="8" autocomplete="new-password" required></div></div><button class="btn btn-soft">Şifreyi değiştir</button></form></section>
    <section class="card danger-zone"><h3>Sınıf kodunu yenile</h3><p class="sub">Mevcut kod pasif olur. Öğrencilerin yeni kodu tekrar girmesi gerekir; eski kayıtlar silinmez.</p><button class="btn btn-danger" data-action="regenerate">Yeni kod üret</button></section>
    <section class="card"><button class="btn btn-soft" data-action="logout">Oturumu kapat</button> <a class="btn btn-green" href="../">Öğrenci uygulamasına git</a></section>`;
}

function renderModal() {
  if (!state.modal) return '';
  if (state.modal.type === 'who') {
    const a = state.assignments.find(item => item.id === state.modal.id);
    if (!a) return '';
    const ids = a.gameIds || [];
    const rows = state.students.map(s => {
      const count = ids.filter(id => (s.doneIds || []).includes(id)).length;
      return {...s, count};
    }).sort((a1, b1) => b1.count - a1.count);
    return modalShell(`${esc(a.title)} — Kim yaptı?`, rows.length ? `<div class="table-wrap"><table class="table"><thead><tr><th>ÖĞRENCİ</th><th class="num">DURUM</th><th>TAMAMLAMA</th></tr></thead><tbody>${rows.map(s => `<tr><td>${esc(s.username)}</td><td class="num">${s.count}/${ids.length}</td><td><span class="pill ${s.count >= ids.length ? 'green' : s.count ? 'yellow' : 'red'}">${s.count >= ids.length ? 'tamamladı' : s.count ? 'devam ediyor' : 'başlamadı'}</span></td></tr>`).join('')}</tbody></table></div>` : empty('👩‍🎓', 'Öğrenci yok', 'Henüz sınıf kodunu giren öğrenci bulunmuyor.'));
  }
  if (state.modal.type === 'board') {
    const c = state.contests.find(item => item.id === state.modal.id);
    const list = state.modal.list || [];
    const body = state.modal.loading ? '<p>Yükleniyor…</p>' : list.length ? `<div class="table-wrap"><table class="table"><thead><tr><th class="num">#</th><th>ÖĞRENCİ</th><th class="num">PUAN</th><th class="num">DOĞRU</th></tr></thead><tbody>${list.map((s, i) => `<tr><td class="num">${i + 1}</td><td>${esc(s.username)}</td><td class="num"><b>${s.score}</b></td><td class="num">${s.correct}/8</td></tr>`).join('')}</tbody></table></div>` : empty('⏳', 'Henüz katılım yok', 'Öğrenciler yarışmayı tamamlayınca sıralama oluşur.');
    return modalShell(`${esc(c?.title || 'Yarışma')} — Sıralama`, body);
  }
  return '';
}

function modalShell(title, body) {
  return `<div class="modal" data-action="close-modal"><div class="modal-card" data-modal-card><div class="modal-head"><h3>${title}</h3><button class="icon-btn" data-action="close-modal">✕</button></div>${body}</div></div>`;
}

function render() {
  if (state.loading && !state.teacher) {
    app.innerHTML = '<main class="loading-screen"><div class="brand-mark">MA</div><p>Öğretmen paneli hazırlanıyor…</p></main>';
    return;
  }
  app.innerHTML = state.teacher ? renderApp() : renderAuth();
  bindForms();
}

function bindForms() {
  const auth = document.getElementById('authForm');
  if (auth) auth.onsubmit = submitAuth;
  const assignment = document.getElementById('assignmentForm');
  if (assignment) assignment.onsubmit = submitAssignment;
  const contest = document.getElementById('contestForm');
  if (contest) contest.onsubmit = submitContest;
  const profile = document.getElementById('profileForm');
  if (profile) profile.onsubmit = submitProfile;
  const password = document.getElementById('passwordForm');
  if (password) password.onsubmit = submitPassword;
  const assignGrade = document.getElementById('assignGrade');
  if (assignGrade) assignGrade.onchange = () => {
    state.assignGrade = Number(assignGrade.value); state.assignSubject = subjectsFor(state.assignGrade)[0] || 'math'; state.selected.clear(); render();
  };
  const assignSubject = document.getElementById('assignSubject');
  if (assignSubject) assignSubject.onchange = () => { state.assignSubject = assignSubject.value; state.selected.clear(); render(); };
  const contestGrade = document.getElementById('contestGrade');
  if (contestGrade) contestGrade.onchange = () => { state.contestGrade = Number(contestGrade.value); render(); };
}

async function submitAuth(event) {
  const data = Object.fromEntries(new FormData(event.currentTarget));
  event.preventDefault(); state.busy = true; state.error = ''; state.ok = ''; render();
  try {
    const result = await api(state.authMode === 'register' ? 'register' : 'login', data);
    state.token = result.token; state.teacher = result.teacher; localStorage.setItem(TOKEN_KEY, state.token);
    setDefaults(); state.busy = false; await refreshAll(false); render();
  } catch (error) { state.busy = false; state.error = error.message; render(); }
}

async function submitAssignment(event) {
  event.preventDefault();
  if (!state.selected.size) { setMessage('error', 'En az bir oyun seçin.'); return; }
  const form = Object.fromEntries(new FormData(event.currentTarget));
  state.busy = true; state.error = ''; render();
  try {
    await api('assignment_create', {...form, grade: state.assignGrade, subj: state.assignSubject, gameIds: [...state.selected]});
    state.selected.clear(); state.busy = false; state.ok = 'Ödev sınıfa gönderildi.'; await refreshAssignments();
  } catch (error) { state.busy = false; state.error = error.message; render(); }
}

async function submitContest(event) {
  event.preventDefault();
  const form = Object.fromEntries(new FormData(event.currentTarget));
  const cat = CONTEST_CATEGORIES.find(item => item[0] === form.catId);
  const start = form.startsAt || todayIso();
  const title = form.title || `${form.kind === 'weekly' ? 'Haftalık' : 'Günlük'} ${cat?.[2] || 'Sınıf'} Yarışması`;
  state.busy = true; state.error = ''; render();
  try {
    await api('contest_create', {...form, title, grade: state.contestGrade, startsAt: start, endsAt: addDays(start, form.kind === 'weekly' ? 6 : 0)});
    state.busy = false; state.ok = 'Yarışma açıldı.'; await refreshContests();
  } catch (error) { state.busy = false; state.error = error.message; render(); }
}

async function submitProfile(event) {
  event.preventDefault();
  try {
    const result = await api('profile_save', Object.fromEntries(new FormData(event.currentTarget)));
    state.teacher = result.teacher; setDefaults(); state.ok = 'Bilgiler kaydedildi.'; render();
  } catch (error) { setMessage('error', error.message); }
}

async function submitPassword(event) {
  event.preventDefault();
  try {
    await api('change_password', Object.fromEntries(new FormData(event.currentTarget)));
    event.currentTarget.reset(); toast('Şifre değiştirildi.');
  } catch (error) { setMessage('error', error.message); }
}

async function runAction(action, button) {
  state.error = ''; state.ok = '';
  if (action === 'copy-code') {
    try { await navigator.clipboard.writeText(state.teacher.class.code); toast('Sınıf kodu kopyalandı.'); }
    catch (_) { toast(`Sınıf kodu: ${state.teacher.class.code}`); }
  } else if (action === 'refresh') {
    try { await refreshAll(); toast('Veriler yenilendi.'); } catch (error) { setMessage('error', error.message); }
  } else if (action === 'refresh-assignments') {
    try { await refreshAssignments(); toast('Ödevler yenilendi.'); } catch (error) { setMessage('error', error.message); }
  } else if (action === 'refresh-contests') {
    try { await refreshContests(); toast('Yarışmalar yenilendi.'); } catch (error) { setMessage('error', error.message); }
  } else if (action === 'select-all' || action === 'clear-games') {
    const ids = catalogFor(state.assignGrade, state.assignSubject).flatMap(group => (group.g || []).map(game => game[0]));
    state.selected = action === 'select-all' ? new Set(ids) : new Set();
    document.querySelectorAll('[data-game-id]').forEach(input => { input.checked = action === 'select-all'; });
    const count = document.getElementById('selectedCount'); if (count) count.textContent = String(state.selected.size);
  } else if (action === 'assignment-who') {
    state.modal = {type: 'who', id: button.dataset.id}; render();
  } else if (action === 'assignment-toggle') {
    try { await api('assignment_toggle', {id: button.dataset.id, active: button.dataset.active === '1'}); await refreshAssignments(); }
    catch (error) { setMessage('error', error.message); }
  } else if (action === 'assignment-delete') {
    if (!confirm('Bu ödev kalıcı olarak silinsin mi?')) return;
    try { await api('assignment_delete', {id: button.dataset.id}); await refreshAssignments(); toast('Ödev silindi.'); }
    catch (error) { setMessage('error', error.message); }
  } else if (action === 'contest-toggle') {
    try { await api('contest_toggle', {id: button.dataset.id, active: button.dataset.active === '1'}); await refreshContests(); }
    catch (error) { setMessage('error', error.message); }
  } else if (action === 'contest-delete') {
    if (!confirm('Bu yarışma ve sıralaması kalıcı olarak silinsin mi?')) return;
    try { await api('contest_delete', {id: button.dataset.id}); await refreshContests(); toast('Yarışma silindi.'); }
    catch (error) { setMessage('error', error.message); }
  } else if (action === 'contest-board') {
    state.modal = {type: 'board', id: button.dataset.id, loading: true, list: []}; render();
    try { const result = await api('contest_board', {id: button.dataset.id}); state.modal = {type: 'board', id: button.dataset.id, loading: false, list: result.list || []}; render(); }
    catch (error) { state.modal = null; setMessage('error', error.message); }
  } else if (action === 'close-modal') {
    state.modal = null; render();
  } else if (action === 'regenerate') {
    if (!confirm('Mevcut kod pasif olacak ve öğrencilerin yeni kodu girmesi gerekecek. Devam edilsin mi?')) return;
    try { const result = await api('class_regenerate'); state.teacher.class = result.class; await refreshAll(false); state.ok = `Yeni sınıf kodu: ${result.class.code}`; render(); }
    catch (error) { setMessage('error', error.message); }
  } else if (action === 'logout') {
    try { await api('logout'); } catch (_) {}
    clearSession(true); render();
  }
}

document.addEventListener('change', event => {
  const input = event.target.closest('[data-game-id]');
  if (!input) return;
  if (input.checked) state.selected.add(input.dataset.gameId); else state.selected.delete(input.dataset.gameId);
  const count = document.getElementById('selectedCount'); if (count) count.textContent = String(state.selected.size);
});

document.addEventListener('click', event => {
  const auth = event.target.closest('[data-auth]');
  if (auth) { state.authMode = auth.dataset.auth; state.error = ''; state.ok = ''; render(); return; }
  const tab = event.target.closest('[data-tab]');
  if (tab) { state.tab = tab.dataset.tab; state.error = ''; state.ok = ''; state.modal = null; render(); window.scrollTo(0, 0); return; }
  const action = event.target.closest('[data-action]');
  if (!action) return;
  if (action.dataset.action === 'close-modal' && event.target.closest('[data-modal-card]') && !event.target.closest('.icon-btn')) return;
  runAction(action.dataset.action, action);
});

boot();
