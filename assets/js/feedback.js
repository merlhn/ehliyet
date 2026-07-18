/* Geri bildirim modalı — ön yüz.
   "Geri bildirim gönder" tetikleyicilerine (.foot-feedback ve [data-feedback]) bağlanır,
   bir kutu açar, kullanıcının yorumunu alır.
   NOT: Şu an gerçek mail servisi YOK. Gönderim simüle edilir; backend eklenince
   aşağıdaki sendFeedback() fonksiyonu gerçek gönderimle değiştirilecek. */
(function () {
  var TARGET_EMAIL = 'omerlhn@gmail.com'; // mail servisi eklenince hedef adres

  var CSS = ''
    + '.fb-overlay{position:fixed;inset:0;z-index:1000;display:none;align-items:center;justify-content:center;padding:20px;background:rgba(8,9,10,.45);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px)}'
    + '.fb-overlay.open{display:flex}'
    + '.fb-modal{width:100%;max-width:460px;background:#fff;border:1px solid #ececec;border-radius:20px;box-shadow:0 24px 60px rgba(0,0,0,.18);padding:26px;transform:translateY(10px);opacity:0;transition:transform .18s,opacity .18s;font-family:inherit}'
    + '.fb-overlay.open .fb-modal{transform:none;opacity:1}'
    + '.fb-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:6px}'
    + '.fb-title{font-size:19px;font-weight:600;letter-spacing:-.02em;margin:0;color:#08090a}'
    + '.fb-close{border:none;background:none;cursor:pointer;color:#6a6f76;padding:4px;margin:-4px -4px 0 0;border-radius:8px;line-height:0}'
    + '.fb-close:hover{background:#f3f3f3;color:#08090a}'
    + '.fb-sub{font-size:14px;color:#6a6f76;line-height:1.5;margin:0 0 18px}'
    + '.fb-label{display:block;font-size:13px;font-weight:500;color:#3a3d42;margin:0 0 6px}'
    + '.fb-opt{color:#9aa0a6;font-weight:400}'
    + '.fb-field{width:100%;font-family:inherit;font-size:14.5px;color:#08090a;border:1px solid #ececec;border-radius:12px;padding:11px 13px;outline:none;transition:.15s;background:#fff}'
    + '.fb-field::placeholder{color:#aab0b6}'
    + '.fb-field:focus{border-color:#08090a;box-shadow:0 0 0 3px rgba(8,9,10,.06)}'
    + 'textarea.fb-field{min-height:120px;resize:vertical;line-height:1.55}'
    + '.fb-row{margin-bottom:14px}'
    + '.fb-err{color:#c0362c;font-size:13px;margin:7px 0 0;display:none}'
    + '.fb-actions{display:flex;gap:10px;justify-content:flex-end;margin-top:20px}'
    + '.fb-btn{font-family:inherit;font-weight:500;font-size:14px;line-height:1;cursor:pointer;border-radius:999px;padding:11px 20px;transition:.15s;border:1px solid transparent}'
    + '.fb-btn-primary{background:#08090a;color:#fff;border-color:#08090a}'
    + '.fb-btn-primary:hover{background:#26282c}'
    + '.fb-btn-primary:disabled{opacity:.5;cursor:default}'
    + '.fb-btn-ghost{background:#fff;color:#08090a;border-color:#ececec}'
    + '.fb-btn-ghost:hover{background:#fafafa;border-color:#c8c8c8}'
    + '.fb-success{text-align:center;padding:12px 4px 4px}'
    + '.fb-check{width:52px;height:52px;border-radius:50%;background:#eaf7ee;color:#16a34a;display:flex;align-items:center;justify-content:center;margin:0 auto 16px}'
    + '.fb-success h3{margin:0 0 8px;font-size:19px;font-weight:600;letter-spacing:-.02em;color:#08090a}'
    + '.fb-success p{margin:0 auto;font-size:14.5px;color:#6a6f76;line-height:1.55;max-width:300px}'
    + '@media(max-width:520px){.fb-modal{padding:22px;border-radius:16px}}';

  var CLOSE_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>';
  var CHECK_SVG = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';

  var FORM_HTML = ''
    + '<div class="fb-head">'
    +   '<h2 class="fb-title">Geri bildirim gönder</h2>'
    +   '<button class="fb-close" type="button" aria-label="Kapat">' + CLOSE_SVG + '</button>'
    + '</div>'
    + '<p class="fb-sub">Bir hatayı bildir, öneride bulun ya da aklındakini yaz. Okuyoruz.</p>'
    + '<form class="fb-form" novalidate>'
    +   '<div class="fb-row">'
    +     '<label class="fb-label" for="fbMsg">Yorumun</label>'
    +     '<textarea id="fbMsg" class="fb-field" placeholder="Yaz..." required></textarea>'
    +     '<p class="fb-err" id="fbMsgErr">Lütfen bir şeyler yaz.</p>'
    +   '</div>'
    +   '<div class="fb-row">'
    +     '<label class="fb-label" for="fbEmail">E-posta <span class="fb-opt">(isteğe bağlı — sana dönebilmemiz için)</span></label>'
    +     '<input id="fbEmail" type="email" class="fb-field" placeholder="ornek@eposta.com">'
    +   '</div>'
    +   '<div class="fb-actions">'
    +     '<button type="button" class="fb-btn fb-btn-ghost fb-cancel">Vazgeç</button>'
    +     '<button type="submit" class="fb-btn fb-btn-primary fb-submit">Gönder</button>'
    +   '</div>'
    + '</form>';

  var SUCCESS_HTML = ''
    + '<div class="fb-success">'
    +   '<div class="fb-check">' + CHECK_SVG + '</div>'
    +   '<h3>Teşekkürler!</h3>'
    +   '<p>Geri bildirimin bize ulaştı. Zaman ayırdığın için sağ ol.</p>'
    +   '<button type="button" class="fb-btn fb-btn-primary fb-done" style="margin-top:20px">Kapat</button>'
    + '</div>';

  var overlay, content;

  function ensure() {
    if (overlay) return;
    var style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    overlay = document.createElement('div');
    overlay.className = 'fb-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.innerHTML = '<div class="fb-modal"><div class="fb-content"></div></div>';
    document.body.appendChild(overlay);
    content = overlay.querySelector('.fb-content');

    overlay.addEventListener('mousedown', function (e) { if (e.target === overlay) close(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('open')) close();
    });
  }

  function renderForm() {
    content.innerHTML = FORM_HTML;
    content.querySelector('.fb-close').addEventListener('click', close);
    content.querySelector('.fb-cancel').addEventListener('click', close);
    content.querySelector('.fb-form').addEventListener('submit', onSubmit);
  }

  function renderSuccess() {
    content.innerHTML = SUCCESS_HTML;
    content.querySelector('.fb-done').addEventListener('click', close);
  }

  function open(e) {
    if (e && e.preventDefault) e.preventDefault();
    ensure();
    renderForm();
    overlay.classList.add('open');
    document.documentElement.style.overflow = 'hidden';
    setTimeout(function () {
      var t = content.querySelector('#fbMsg');
      if (t) t.focus();
    }, 60);
  }

  function close() {
    if (!overlay) return;
    overlay.classList.remove('open');
    document.documentElement.style.overflow = '';
  }

  function onSubmit(e) {
    e.preventDefault();
    var msgEl = content.querySelector('#fbMsg');
    var emailEl = content.querySelector('#fbEmail');
    var msg = (msgEl.value || '').trim();
    if (!msg) {
      content.querySelector('#fbMsgErr').style.display = 'block';
      msgEl.focus();
      return;
    }
    var btn = content.querySelector('.fb-submit');
    btn.disabled = true;
    btn.textContent = 'Gönderiliyor...';
    sendFeedback({ message: msg, email: (emailEl.value || '').trim() })
      .then(function () { renderSuccess(); })
      .catch(function () {
        btn.disabled = false;
        btn.textContent = 'Gönder';
        alert('Bir sorun oluştu, lütfen tekrar dene.');
      });
  }

  /* ============================================================
     BACKEND ENTEGRASYONU BURAYA
     Şu an mail servisi YOK — gönderim yalnızca simüle ediliyor.
     Mail servisi eklenince bu fonksiyonu gerçek gönderimle değiştir:
       return fetch('/api/feedback', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(data)
       });
     ya da EmailJS / Formspree gibi bir servis çağrısı.
     Hedef adres: TARGET_EMAIL (omerlhn@gmail.com)
     ============================================================ */
  function sendFeedback(data) {
    return new Promise(function (resolve) {
      // TODO: gerçek gönderim yok — ön yüz simülasyonu.
      console.log('[feedback] gönderilecek →', TARGET_EMAIL, data);
      setTimeout(resolve, 550);
    });
  }

  function bind() {
    var triggers = document.querySelectorAll('.foot-feedback, [data-feedback]');
    for (var i = 0; i < triggers.length; i++) {
      triggers[i].addEventListener('click', open);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bind);
  } else {
    bind();
  }
})();
