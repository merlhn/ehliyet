/*
 * Panel yan menüsü — TEK KAYNAK.
 *
 * Hem panelin kendi sayfası hem alt sayfalar (sınav, kılavuz) bu modülden menü
 * kurar. Daha önce markup iki ayrı yerde tekrarlanıyordu ve her değişiklikte
 * ikisini elle senkron tutmak gerekiyordu.
 *
 * NOT: Ders Notları ve Hap Bilgiler menüde yer alır ama ürün içi deneyimleri
 * henüz tasarlanmadı; şimdilik "Yakında geliştirilecek" ekranına çıkarlar.
 * Panelden public sayfalara (/dersler/, /hap-bilgiler/) bağlantı verilmez —
 * kullanıcıyı üründen çıkarır.
 */

export const MENU_CSS = `
.pk-yan{position:fixed;inset:0 auto 0 0;width:var(--pk-yan,186px);border-right:1px solid #ececec;
  display:flex;flex-direction:column;background:#fff;z-index:30;
  font-family:'Inter',-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;letter-spacing:-.011em}
.pk-marka{display:flex;align-items:center;gap:10px;height:60px;padding:0 18px;
  border-bottom:1px solid #ececec;flex-shrink:0;text-decoration:none;color:#08090a}
.pk-marka img{width:26px;height:26px;object-fit:contain;flex-shrink:0}
.pk-marka span{font-size:15.5px;font-weight:600;letter-spacing:-.02em}

.pk-ust{display:flex;flex-direction:column;gap:2px;padding:14px 10px 0}
.pk-alt{margin-top:auto;display:flex;flex-direction:column;gap:2px;padding:0 10px 18px}

.pk-oge{display:flex;align-items:center;gap:10px;padding:10px 10px;border-radius:9px;
  font-size:13px;white-space:nowrap;font-weight:450;color:#3a3d42;text-decoration:none;
  background:none;border:none;font-family:inherit;width:100%;text-align:left;cursor:pointer;transition:.12s}
.pk-oge:hover{background:#f5f5f5;color:#08090a}
.pk-oge.aktif{background:#f2f2f2;color:#08090a;font-weight:500}
.pk-oge svg{flex-shrink:0}

.pk-profil{display:flex;align-items:center;gap:10px;padding:14px 14px;border-top:1px solid #ececec;margin-top:8px;flex-shrink:0}
.pk-profil-avatar{width:32px;height:32px;border-radius:50%;flex-shrink:0;background:#ececec;object-fit:cover;
  display:inline-flex;align-items:center;justify-content:center;font-size:13px;font-weight:600;color:#08090a;overflow:hidden}
.pk-profil-avatar img{width:100%;height:100%;object-fit:cover;display:block}
.pk-profil-info{flex:1;min-width:0}
.pk-profil-ad{font-size:13px;font-weight:600;color:#08090a;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pk-profil-mail{font-size:11.5px;color:#6a6f76;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pk-cikis{background:none;border:none;cursor:pointer;color:#6a6f76;padding:4px;border-radius:6px;flex-shrink:0;transition:.12s}
.pk-cikis:hover{color:#08090a;background:#f5f5f5}

@media(max-width:820px){
  .pk-yan{position:static;width:100%;height:auto;flex-direction:row;align-items:center;
    border-right:none;border-bottom:1px solid #ececec;padding:0 14px;gap:6px;overflow-x:auto}
  .pk-marka{height:52px;padding:0 10px 0 0;border-bottom:none}
  .pk-ust,.pk-alt{flex-direction:row;padding:0;margin-top:0}
}
`;

const IKON = {
  ev: '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/></svg>',
  sinav: '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>',
  kitap: '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
  simsek: '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
  kart: '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg>',
  ayar: '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
};

/**
 * Menü markup'ını üretir.
 * @param {object} opt
 * @param {string} opt.aktif           seçili görünüm: anasayfa | sinavlar | odeme | ayarlar
 * @param {boolean} opt.baglantiOlarak true ise öğeler <a> (sayfa değiştirir),
 *                                     false ise <button> (panelde görünüm değiştirir)
 */
export function menuHTML({ aktif = '', baglantiOlarak = true } = {}) {
  const oge = (ad, ikon, etiket) => baglantiOlarak
    ? `<a class="pk-oge${aktif === ad ? ' aktif' : ''}" href="/panel/?g=${ad}">${ikon}${etiket}</a>`
    : `<button class="pk-oge${aktif === ad ? ' aktif' : ''}" type="button" data-gorunum="${ad}">${ikon}${etiket}</button>`;

  return `
  <aside class="pk-yan">
    <a class="pk-marka" href="/panel/">
      <img src="/assets/img/marka/logo.png" alt="">
      <span>ehliyet.digital</span>
    </a>

    <nav class="pk-ust">
      ${oge('anasayfa', IKON.ev, 'Ana Sayfa')}
      ${oge('sinavlar', IKON.sinav, 'Deneme Sınavları')}
      ${oge('dersler', IKON.kitap, 'Ders Notları')}
      ${oge('hapbilgiler', IKON.simsek, 'Hap Bilgiler')}
    </nav>

    <nav class="pk-alt">
      ${oge('ayarlar', IKON.ayar, 'Ayarlar')}
    </nav>

    <div class="pk-profil" data-pk-profil hidden>
      <span class="pk-profil-avatar" data-pk-avatar></span>
      <div class="pk-profil-info">
        <div class="pk-profil-ad" data-pk-ad></div>
        <div class="pk-profil-mail" data-pk-mail></div>
      </div>
      <button class="pk-cikis" type="button" data-pk-cikis title="Çıkış yap"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg></button>
    </div>
  </aside>`;
}
