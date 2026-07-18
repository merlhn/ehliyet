/*
 * Panel kabuğu — /panel/ altındaki alt sayfalara (sınav, kılavuz) yan menüyü
 * enjekte eder ve oturum kontrolü yapar. Menü markup'ı panel-menu.js'ten gelir.
 *
 * Firebase BİLEREK statik import edilmiyor: SDK açılışın kritik yolunda yer
 * alınca ana iş parçacığını ~130ms bloklayıp kare düşmesine yol açıyordu.
 * Menü hemen kurulur, oturum kontrolü sonra yürür.
 */
import { MENU_CSS, menuHTML } from './panel-menu.js';

const TEMEL_CSS = `
:root{--pk-yan:186px}
body{margin-left:var(--pk-yan)}
@media(max-width:820px){ :root{--pk-yan:0px} body{margin-left:0} }
`;

/**
 * Sınav sürerken menüden ayrılmak cevapları kaybettirir; sayfa
 * `window.SINAV_DEVAM_EDIYOR` true iken tıklamalar onay ister.
 */
function cikisOnayi(e) {
  if (!window.SINAV_DEVAM_EDIYOR) return;
  if (!confirm('Sınav devam ediyor. Sayfadan ayrılırsan cevapların kaybolur. Yine de çıkmak istiyor musun?')) {
    e.preventDefault();
  }
}

function menuyuKur() {
  if (document.querySelector('.pk-yan')) return;
  document.body.insertAdjacentHTML('afterbegin', menuHTML());
  document.querySelectorAll('.pk-yan a').forEach(a => a.addEventListener('click', cikisOnayi));
}

const stil = document.createElement('style');
stil.textContent = TEMEL_CSS + MENU_CSS;
document.head.appendChild(stil);

// Menü hemen kurulur; Firebase beklenirse sayfa önce menüsüz çizilip sağa kayıyordu.
if (document.body) menuyuKur();
else document.addEventListener('DOMContentLoaded', menuyuKur, { once: true });

// Oturum kontrolü ayrı ve gecikmeli yürür; yalnızca yönlendirmeden sorumlu.
function oturumuDogrula() {
  import('./firebase.js')
    .then(({ kullaniciDinle }) => kullaniciDinle(user => { if (!user) location.replace('/'); }))
    .catch(err => console.error('Oturum kontrolü yüklenemedi:', err));
}

if ('requestIdleCallback' in window) requestIdleCallback(oturumuDogrula, { timeout: 2000 });
else setTimeout(oturumuDogrula, 300);
