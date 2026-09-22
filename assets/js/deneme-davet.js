/*
 * Deneme sınavı daveti — sitede toplam 15 sn (görünür sekmede) geçiren
 * ziyaretçiye tek seferlik bir davet kutusu açar ve deneme sınavına yönlendirir.
 *
 * Kurallar:
 *  - Süre sayfalar arası birikir (sessionStorage): 8 sn ana sayfa + 7 sn ders
 *    sayfası = 15 sn. Sekme arka plandayken sayaç durur.
 *  - Bir oturumda en fazla bir kez, 7 günde en fazla bir kez gösterilir.
 *  - Panel sayfalarında (kullanıcı zaten üründe) ve giriş ekranı açıkken çıkmaz.
 *  - Buton: giriş yapılmışsa doğrudan /panel/?g=sinavlar; değilse auth-ui.js'in
 *    giriş ekranını açar (sayfada yüklü değilse isteğe bağlı yüklenir).
 */
(function () {
  'use strict';

  var HEDEF = '/panel/?g=sinavlar';
  var ESIK_MS = 15000;
  var TEKRAR_GUN = 7;
  var K_SURE = 'deneme-davet-sure';       // sessionStorage: biriken görünür süre (ms)
  var K_OTURUM = 'deneme-davet-gosterildi'; // sessionStorage: bu oturumda gösterildi
  var K_SON = 'deneme-davet-son';         // localStorage: son gösterim zamanı (ms)

  if (location.pathname.indexOf('/panel') === 0) return;

  function oku(depo, k) { try { return depo.getItem(k); } catch (e) { return null; } }
  function yaz(depo, k, v) { try { depo.setItem(k, v); } catch (e) {} }

  if (oku(sessionStorage, K_OTURUM) === '1') return;
  var son = Number(oku(localStorage, K_SON) || 0);
  if (son && Date.now() - son < TEKRAR_GUN * 864e5) return;

  /* ---- Süre sayacı ---- */
  var biriken = Number(oku(sessionStorage, K_SURE) || 0);
  var baslangic = null;
  var zamanlayici = null;

  function gecen() { return biriken + (baslangic ? Date.now() - baslangic : 0); }
  function kaydet() { yaz(sessionStorage, K_SURE, String(Math.min(gecen(), ESIK_MS))); }

  function baslat() {
    if (baslangic || document.visibilityState !== 'visible') return;
    baslangic = Date.now();
    var kalan = Math.max(ESIK_MS - biriken, 0);
    zamanlayici = setTimeout(dene, kalan);
  }
  function durdur() {
    if (!baslangic) return;
    biriken += Date.now() - baslangic;
    baslangic = null;
    clearTimeout(zamanlayici);
    kaydet();
  }

  document.addEventListener('visibilitychange', function () {
    document.visibilityState === 'visible' ? baslat() : durdur();
  });
  window.addEventListener('pagehide', durdur);
  baslat();

  /* ---- Gösterim koşulları ---- */
  function meskul() {
    // Giriş ekranı, geri bildirim kutusu ya da başka bir diyalog açıkken bekle.
    if (document.querySelector('.auth-ort, [role="dialog"]:not([hidden])')) return true;
    var a = document.activeElement;
    return !!(a && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName));
  }

  function dene() {
    if (gecen() < ESIK_MS) return;
    if (meskul()) { zamanlayici = setTimeout(dene, 4000); return; }
    goster();
  }

  /* ---- Görünüm ---- */
  var CSS = '\n' +
    '.dd-ort{position:fixed;inset:0;z-index:190;display:flex;align-items:center;justify-content:center;' +
    'padding:20px;background:rgba(8,9,10,.45);opacity:0;transition:opacity .18s ease}\n' +
    '.dd-ort.acik{opacity:1}\n' +
    '.dd-kutu{position:relative;background:#fff;border-radius:20px;padding:30px 28px 24px;width:100%;max-width:400px;' +
    'box-shadow:0 24px 64px rgba(0,0,0,.22);text-align:center;color:#08090a;' +
    'font-family:"Inter","Inter-fallback",-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;letter-spacing:-.011em;' +
    'transform:translateY(10px) scale(.98);transition:transform .18s ease}\n' +
    '.dd-ort.acik .dd-kutu{transform:none}\n' +
    '.dd-kapat{position:absolute;top:12px;right:12px;width:36px;height:36px;border:none;background:none;border-radius:50%;' +
    'cursor:pointer;color:#6a6f76;display:flex;align-items:center;justify-content:center}\n' +
    '.dd-kapat:hover{background:#f5f5f5;color:#08090a}\n' +
    '.dd-ust{font-family:"Geist Mono",monospace;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:#6a6f76;margin:0 0 12px}\n' +
    '.dd-kutu h2{font-size:23px;line-height:1.2;letter-spacing:-.025em;font-weight:650;margin:0 0 10px}\n' +
    '.dd-kutu p{font-size:14.5px;line-height:1.55;color:#6a6f76;margin:0 0 18px}\n' +
    '.dd-ozet{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 20px}\n' +
    '.dd-ozet div{border:1px solid #ececec;border-radius:12px;padding:10px 6px;background:#fafafa}\n' +
    '.dd-ozet b{display:block;font-size:17px;font-weight:600;letter-spacing:-.02em}\n' +
    '.dd-ozet span{display:block;font-size:11.5px;color:#6a6f76;margin-top:2px}\n' +
    '.dd-btn{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;font-family:inherit;font-weight:500;' +
    'font-size:15px;line-height:1;padding:14px 18px;border-radius:12px;background:#08090a;color:#fff;border:1px solid #08090a;' +
    'cursor:pointer;transition:.15s;letter-spacing:-.01em}\n' +
    '.dd-btn:hover{background:#26282c;border-color:#26282c}\n' +
    /* Odak programatik verildiği için fare kullanıcısı halka görmesin; klavyede görünsün. */
    '.dd-btn:focus{outline:none}.dd-btn:focus-visible{outline:2px solid #08090a;outline-offset:3px}\n' +
    '.dd-vazgec{margin-top:12px;background:none;border:none;font:inherit;font-size:13.5px;color:#6a6f76;cursor:pointer;' +
    'padding:8px 12px;border-radius:8px;min-height:36px}\n' +
    '.dd-vazgec:hover{color:#08090a;background:#f5f5f5}\n' +
    /* Telefonda alttan açılan panel: başparmakla erişim daha kolay. */
    '@media(max-width:640px){.dd-ort{align-items:flex-end;padding:0}' +
    '.dd-kutu{max-width:none;border-radius:22px 22px 0 0;padding:28px 22px calc(20px + env(safe-area-inset-bottom));' +
    'transform:translateY(24px)}.dd-kutu h2{font-size:22px}}\n' +
    '@media(prefers-reduced-motion:reduce){.dd-ort,.dd-kutu{transition:none}.dd-kutu{transform:none}}\n';

  function olay(ad) {
    if (typeof gtag === 'function') gtag('event', 'deneme_davet', { eylem: ad, sayfa: location.pathname });
  }

  function goster() {
    if (document.querySelector('.dd-ort')) return;
    yaz(sessionStorage, K_OTURUM, '1');
    yaz(localStorage, K_SON, String(Date.now()));

    var stil = document.createElement('style');
    stil.id = 'deneme-davet-css';
    stil.textContent = CSS;
    document.head.appendChild(stil);

    var ort = document.createElement('div');
    ort.className = 'dd-ort';
    ort.setAttribute('role', 'dialog');
    ort.setAttribute('aria-modal', 'true');
    ort.setAttribute('aria-labelledby', 'dd-baslik');
    ort.innerHTML =
      '<div class="dd-kutu">' +
        '<button class="dd-kapat" type="button" aria-label="Kapat" data-kapat>' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6L6 18M6 6l12 12"/></svg>' +
        '</button>' +
        '<p class="dd-ust">Deneme sınavı</p>' +
        '<h2 id="dd-baslik">Kendini gerçek sınavda dene</h2>' +
        '<p>MEB e-sınav formatında ücretsiz deneme. Sonucun hesabına kaydedilir, hangi konuda eksiğin olduğunu görürsün.</p>' +
        '<div class="dd-ozet" aria-hidden="true">' +
          '<div><b>50</b><span>soru</span></div>' +
          '<div><b>45</b><span>dakika</span></div>' +
          '<div><b>70</b><span>geçme puanı</span></div>' +
        '</div>' +
        '<button class="dd-btn" type="button" data-basla>Deneme Sınavına Başla <span aria-hidden="true">→</span></button>' +
        '<button class="dd-vazgec" type="button" data-kapat>Şimdi değil</button>' +
      '</div>';
    document.body.appendChild(ort);

    var odak = document.activeElement;
    var eskiOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    ort.offsetHeight; // geçişin tetiklenmesi için yeniden hesaplama
    ort.classList.add('acik');
    ort.querySelector('[data-basla]').focus();
    olay('goster');

    function kapat(neden) {
      if (!ort.isConnected) return;
      ort.classList.remove('acik');
      document.body.style.overflow = eskiOverflow;
      document.removeEventListener('keydown', escile);
      setTimeout(function () { ort.remove(); }, 180);
      if (odak && odak.isConnected && odak.focus) odak.focus();
      if (neden) olay(neden);
    }
    function escile(e) { if (e.key === 'Escape') kapat('kapat'); }

    ort.querySelectorAll('[data-kapat]').forEach(function (b) {
      b.addEventListener('click', function () { kapat('kapat'); });
    });
    ort.addEventListener('click', function (e) { if (e.target === ort) kapat('kapat'); });
    document.addEventListener('keydown', escile);

    ort.querySelector('[data-basla]').addEventListener('click', function () {
      olay('tikla');
      kapat();
      // auth-ui.js giriş durumunu bilir: giriş varsa yönlendirir, yoksa giriş ekranını açar.
      var hazir = window.ehliyetGiris
        ? Promise.resolve(window.ehliyetGiris)
        : import('/assets/js/auth-ui.js').then(function () { return window.ehliyetGiris; });
      hazir.then(function (giris) {
        if (typeof giris === 'function') giris(HEDEF); else location.href = HEDEF;
      }).catch(function () { location.href = HEDEF; });
    });
  }
})();
