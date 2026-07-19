/*
 * Çıkış onayı — "Çıkış yap" tıklanınca oturumu hemen kapatmak yerine küçük bir
 * onay ekranı açar; yanlışlıkla tıklamada kullanıcı platformdan atılmaz.
 *
 * Kullanım (hem public header hem panel):
 *   const { cikisOnayiAc } = await import('/assets/js/cikis-onay.js');
 *   cikisOnayiAc(async () => { await cikisYap(); location.href = '/'; });
 *
 * Görünüm giriş ekranıyla (auth-ui.js) aynı dildedir ama sınıf adları ayrıdır:
 * panel auth-ui.js'i yüklemiyor, bu modül stilini kendisi taşımak zorunda.
 */

const CSS = `
.co-ort{position:fixed;inset:0;z-index:220;display:flex;align-items:center;justify-content:center;
  padding:20px;background:rgba(8,9,10,.45);opacity:0;transition:opacity .16s ease}
.co-ort.acik{opacity:1}
.co-kutu{background:#fff;border-radius:18px;padding:30px 28px 24px;width:100%;max-width:360px;
  box-shadow:0 24px 64px rgba(0,0,0,.22);text-align:center;font-family:inherit;
  transform:translateY(8px) scale(.98);transition:transform .16s ease}
.co-ort.acik .co-kutu{transform:none}
.co-kutu h2{font-size:20px;line-height:1.25;letter-spacing:-.02em;font-weight:650;color:#08090a;margin:0 0 8px}
.co-kutu p{font-size:14px;line-height:1.55;color:#6a6f76;margin:0 0 20px}
.co-cik{display:block;width:100%;font-family:inherit;font-weight:500;font-size:15px;line-height:1;
  cursor:pointer;border-radius:12px;padding:14px 18px;background:#08090a;color:#fff;
  border:1px solid #08090a;transition:.15s}
.co-cik:hover{background:#26282c;border-color:#26282c}
.co-cik[disabled]{opacity:.5;cursor:default}
.co-vazgec{margin-top:12px;background:none;border:none;font:inherit;font-size:13.5px;color:#6a6f76;
  cursor:pointer;padding:6px 10px;border-radius:8px}
.co-vazgec:hover{color:#08090a;background:#f5f5f5}
@media(prefers-reduced-motion:reduce){.co-ort,.co-kutu{transition:none}.co-kutu{transform:none}}
`;

let acikEkran = null;

function kapat() {
  if (!acikEkran) return;
  const { ort, odak } = acikEkran;
  acikEkran = null;
  ort.classList.remove('acik');
  // Geçiş bitmeden kaldırırsak kapanış animasyonu görünmez.
  setTimeout(() => ort.remove(), 160);
  // Klavyeyle gezen kullanıcı ekranı açtığı yere geri dönmeli.
  if (odak?.isConnected) odak.focus();
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') kapat();
});

/**
 * Onay ekranını açar. Kullanıcı "Çıkış yap"ı onaylarsa `cikis` çağrılır;
 * oturumu kapatmak ve gerekiyorsa yönlendirmek çağıranın işidir.
 * Vazgeçerse ekran kapanır, hiçbir şey olmaz.
 */
export function cikisOnayiAc(cikis) {
  if (acikEkran) return;

  if (!document.getElementById('cikis-onay-css')) {
    const s = document.createElement('style');
    s.id = 'cikis-onay-css';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  const ort = document.createElement('div');
  ort.className = 'co-ort';
  ort.setAttribute('role', 'dialog');
  ort.setAttribute('aria-modal', 'true');
  ort.setAttribute('aria-labelledby', 'co-baslik');
  ort.innerHTML = `
    <div class="co-kutu">
      <h2 id="co-baslik">Çıkış yapmak istediğine emin misin?</h2>
      <p>Oturumun kapanır; deneme sonuçların hesabında saklanmaya devam eder.</p>
      <button class="co-cik" type="button" data-onay>Çıkış yap</button>
      <button class="co-vazgec" type="button" data-vazgec>Vazgeç</button>
    </div>`;

  document.body.appendChild(ort);
  acikEkran = { ort, odak: document.activeElement };
  // auth-ui.js'teki gerekçenin aynısı: rAF arka plandaki sekmede çalışmayabilir,
  // geçişi başlatmak için tarayıcı yeniden hesaplamaya zorlanıyor.
  void ort.offsetHeight;
  ort.classList.add('acik');

  const onay = ort.querySelector('[data-onay]');
  onay.focus();

  onay.addEventListener('click', async () => {
    onay.disabled = true;
    onay.textContent = 'Çıkış yapılıyor…';
    try {
      await cikis();
      kapat();
    } catch (err) {
      console.error('Çıkış başarısız:', err);
      onay.disabled = false;
      onay.textContent = 'Çıkış yap';
    }
  });

  ort.querySelector('[data-vazgec]').addEventListener('click', kapat);
  // Kutunun dışına tıklamak kapatır; kutunun içi kapatmaz.
  ort.addEventListener('click', (e) => { if (e.target === ort) kapat(); });
}
