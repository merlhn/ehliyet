/*
 * Panel yan menüsü — /panel/ altındaki alt sayfalara (sınav, kılavuz) enjekte edilir.
 * Panelin kendi ana sayfası menüyü kendi şablonundan kurar; burası onun dışındaki
 * sayfalarda aynı kabuğu tekrar etmemek içindir.
 *
 * Ayrıca oturum kontrolü yapar: giriş yoksa ana sayfaya yönlendirir.
 */
import { kullaniciDinle } from './firebase.js';

const CSS = `
:root{--pk-yan:248px;--pk-line:#ececec}
body{margin-left:var(--pk-yan)}
.pk-yan{position:fixed;inset:0 auto 0 0;width:var(--pk-yan);border-right:1px solid var(--pk-line);
  display:flex;flex-direction:column;background:#fff;z-index:30;
  font-family:'Inter',-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;letter-spacing:-.011em}
.pk-marka{display:flex;align-items:center;gap:10px;height:60px;padding:0 18px;
  border-bottom:1px solid var(--pk-line);flex-shrink:0;text-decoration:none;color:#08090a}
.pk-marka img{width:26px;height:26px;object-fit:contain;flex-shrink:0}
.pk-marka span{font-size:15.5px;font-weight:600;letter-spacing:-.02em}
.pk-menu{display:flex;flex-direction:column;gap:2px;padding:14px 12px 0}
.pk-alt{margin-top:auto;display:flex;flex-direction:column;gap:2px;padding:0 12px 18px}
.pk-oge{display:flex;align-items:center;gap:11px;padding:10px 12px;border-radius:9px;
  font-size:14px;font-weight:450;color:#3a3d42;text-decoration:none;transition:.12s}
.pk-oge:hover{background:#f5f5f5;color:#08090a}
.pk-oge svg{flex-shrink:0}
@media(max-width:820px){
  :root{--pk-yan:0px}
  body{margin-left:0}
  .pk-yan{position:static;width:100%;height:auto;flex-direction:row;align-items:center;
    border-right:none;border-bottom:1px solid var(--pk-line);padding:0 14px;gap:6px;overflow-x:auto}
  .pk-marka{height:auto;padding:12px 10px 12px 0;border-bottom:none}
  .pk-menu,.pk-alt{flex-direction:row;padding:0;margin-top:0}
  .pk-oge{padding:8px 11px;font-size:13.5px;white-space:nowrap}
}
`;

const IKON = {
  ev: '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/></svg>',
  sinav: '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>',
  kart: '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg>',
  ayar: '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
};

function menuHTML() {
  return `
  <aside class="pk-yan">
    <a class="pk-marka" href="/panel/">
      <img src="/assets/img/marka/logo.png" alt="">
      <span>ehliyet.digital</span>
    </a>
    <nav class="pk-menu">
      <a class="pk-oge" href="/panel/?g=anasayfa">${IKON.ev}Ana Sayfa</a>
      <a class="pk-oge" href="/panel/?g=sinavlar">${IKON.sinav}Deneme Sınavları</a>
    </nav>
    <nav class="pk-alt">
      <a class="pk-oge" href="/panel/?g=odeme">${IKON.kart}Ödeme Geçmişi</a>
      <a class="pk-oge" href="/panel/?g=ayarlar">${IKON.ayar}Ayarlar</a>
    </nav>
  </aside>`;
}

/**
 * Sınav sürerken menüden çıkmak cevapları kaybettirir; bu yüzden sayfa
 * `window.SINAV_DEVAM_EDIYOR` true iken menü tıklamaları onay ister.
 */
function cikisOnayi(e) {
  if (!window.SINAV_DEVAM_EDIYOR) return;
  const devam = confirm('Sınav devam ediyor. Sayfadan ayrılırsan cevapların kaybolur. Yine de çıkmak istiyor musun?');
  if (!devam) e.preventDefault();
}

// Menü, oturum kontrolünden BAĞIMSIZ olarak hemen kurulur.
// Firebase'i beklersek sayfa önce menüsüz çizilir, oturum çözülünce body'ye
// 248px kenar boşluğu gelir ve içerik sağa kayar — kullanıcı bunu "sayfa yeniden
// render ediliyor" olarak görüyor. Menü anında basılınca kayma olmuyor.
const stil = document.createElement('style');
stil.textContent = CSS;
document.head.appendChild(stil);

function menuyuKur() {
  if (document.querySelector('.pk-yan')) return;
  document.body.insertAdjacentHTML('afterbegin', menuHTML());
  document.querySelectorAll('.pk-yan a').forEach(a => a.addEventListener('click', cikisOnayi));
}

if (document.body) menuyuKur();
else document.addEventListener('DOMContentLoaded', menuyuKur, { once: true });

// Oturum kontrolü ayrı yürür; yalnızca yönlendirmeden sorumlu.
kullaniciDinle((user) => {
  if (!user) location.replace('/');
});
