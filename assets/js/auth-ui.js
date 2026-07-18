/*
 * Header'a giriş/profil kontrolü ekler. Her sayfaya tek satırla dahil edilir:
 *   <script type="module" src="/assets/js/auth-ui.js"></script>
 *
 * Stiller burada enjekte edilir; sayfaların CSS'i birbirinden farklı olduğu için
 * bileşen kendi görünümünü taşır ve her yerde aynı durur.
 */
import { girisYap, cikisYap, kullaniciDinle, profiliHazirla } from './firebase.js';

const CSS = `
.auth-slot{margin-left:auto;display:flex;align-items:center;position:relative}
.auth-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;
  font-family:inherit;font-weight:500;font-size:14px;line-height:1;cursor:pointer;
  border-radius:999px;padding:10px 18px;background:#08090a;color:#fff;border:1px solid #08090a;
  transition:.15s;white-space:nowrap;letter-spacing:-.01em}
.auth-btn:hover{background:#26282c;border-color:#26282c}
.auth-btn[disabled]{opacity:.5;cursor:default}
/* Google logosu koyu buton üzerinde okunmadığı için beyaz bir daireye oturtuluyor. */
.auth-g{width:18px;height:18px;border-radius:50%;background:#fff;flex-shrink:0;
  display:inline-flex;align-items:center;justify-content:center}
.auth-g svg{width:12px;height:12px;display:block}
.auth-user{display:flex;align-items:center;gap:9px;background:none;border:1px solid #ececec;
  border-radius:999px;padding:5px 12px 5px 5px;cursor:pointer;font:inherit;font-size:14px;
  color:#08090a;transition:.15s}
.auth-user:hover{border-color:#c8c8c8;background:#fafafa}
.auth-avatar{width:26px;height:26px;border-radius:50%;flex-shrink:0;background:#ececec;object-fit:cover}
.auth-ad{max-width:130px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.auth-menu{position:absolute;top:calc(100% + 8px);right:0;min-width:190px;background:#fff;
  border:1px solid #ececec;border-radius:12px;box-shadow:0 12px 34px rgba(0,0,0,.10);
  padding:6px;display:none;z-index:60}
.auth-menu.acik{display:block}
.auth-menu a,.auth-menu button{display:block;width:100%;text-align:left;background:none;border:none;
  font:inherit;font-size:14px;color:#08090a;text-decoration:none;padding:9px 12px;border-radius:8px;cursor:pointer}
.auth-menu a:hover,.auth-menu button:hover{background:#f5f5f5}
.auth-menu .ayrac{height:1px;background:#ececec;margin:5px 2px}
.auth-menu .mail{padding:8px 12px 4px;font-size:12.5px;color:#6a6f76;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

/* Dar ekranda buton küçülür ama "Giriş yap" metni KALIR: logo yöntemi anlatıyor,
   eylemi anlatmıyor — tek başına logo kullanıcıya ne olacağını söylemiyor.
   Giriş yapılmış hâlde kullanıcı adı gizlenir; avatar zaten anlaşılan bir işaret. */
@media(max-width:640px){
  .auth-btn{padding:7px 10px;font-size:10.5px;gap:5px}
  .auth-g{width:13px;height:13px}
  .auth-g svg{width:9px;height:9px}
  .auth-user{padding:4px}
  .auth-ad{display:none}
}
`;

function stilEkle() {
  if (document.getElementById('auth-ui-css')) return;
  const s = document.createElement('style');
  s.id = 'auth-ui-css';
  s.textContent = CSS;
  document.head.appendChild(s);
}

function slotBul() {
  const header = document.querySelector('header');
  if (!header) return null;
  let slot = header.querySelector('.auth-slot');
  if (!slot) {
    slot = document.createElement('div');
    slot.className = 'auth-slot';
    header.appendChild(slot);
  }
  return slot;
}

function esc(s) {
  return String(s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

const GOOGLE_LOGO = `
<span class="auth-g" aria-hidden="true"><svg viewBox="0 0 48 48">
  <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
  <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
  <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
  <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
</svg></span>`;

function girisGoster(slot) {
  // Etiket ayrı bir span'de: yükleniyor durumunda metni değiştirirken logo silinmesin.
  slot.innerHTML = `<button class="auth-btn" type="button" aria-label="Google ile giriş yap">
      ${GOOGLE_LOGO}<span data-etiket>Giriş yap</span>
    </button>`;

  slot.querySelector('button').addEventListener('click', async (e) => {
    const btn = e.currentTarget;
    const etiket = btn.querySelector('[data-etiket]');
    btn.disabled = true;
    etiket.textContent = 'Açılıyor…';
    try {
      await girisYap();
      // Giriş yapan kullanıcı panele iner; public site giriş yapmamışlar için vitrindir.
      location.href = '/panel/';
      return;
    } catch (err) {
      // Kullanıcı pencereyi kapattıysa bu bir hata değil, sessizce eski hale dön.
      if (err?.code !== 'auth/popup-closed-by-user' && err?.code !== 'auth/cancelled-popup-request') {
        console.error('Giriş başarısız:', err);
        alert('Giriş yapılamadı. Lütfen tekrar deneyin.');
      }
      btn.disabled = false;
      etiket.textContent = 'Giriş yap';
    }
  });
}

function kullaniciGoster(slot, user) {
  const ad = user.displayName || user.email || 'Hesabım';
  const foto = user.photoURL
    ? `<img class="auth-avatar" src="${esc(user.photoURL)}" alt="" referrerpolicy="no-referrer">`
    : `<span class="auth-avatar"></span>`;

  slot.innerHTML = `
    <button class="auth-user" type="button" aria-haspopup="true" aria-expanded="false">
      ${foto}<span class="auth-ad">${esc(ad)}</span>
    </button>
    <div class="auth-menu" role="menu">
      <div class="mail">${esc(user.email || '')}</div>
      <a href="/panel/">Panelim</a>
      <div class="ayrac"></div>
      <button type="button" data-cikis>Çıkış yap</button>
    </div>`;

  const btn = slot.querySelector('.auth-user');
  const menu = slot.querySelector('.auth-menu');

  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const acik = menu.classList.toggle('acik');
    btn.setAttribute('aria-expanded', String(acik));
  });
  document.addEventListener('click', () => {
    menu.classList.remove('acik');
    btn.setAttribute('aria-expanded', 'false');
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') menu.classList.remove('acik');
  });
  slot.querySelector('[data-cikis]').addEventListener('click', () => cikisYap());
}

stilEkle();

kullaniciDinle(async (user) => {
  const slot = slotBul();
  if (!slot) return;

  if (!user) {
    girisGoster(slot);
    return;
  }

  kullaniciGoster(slot, user);

  // Profil dokümanını oluştur/güncelle. Başarısız olsa bile arayüz çalışmaya
  // devam etmeli — kullanıcı girişini bir Firestore hatası yüzünden kaybetmesin.
  try {
    await profiliHazirla(user);
  } catch (err) {
    console.error('Profil kaydedilemedi:', err);
  }
});
