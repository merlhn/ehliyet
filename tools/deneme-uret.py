#!/usr/bin/env python3
"""/deneme-sinavi/index.html'i panel/sinav-1'deki sınav motorundan üretir.

Sınav CSS'i ve JS'i panel sayfasından alınır, panel kabuğuna bağımlı kısımlar
(yan menü boşluğu, oturum zorunluluğu, /panel/ yönlendirmeleri) çıkarılır,
üstüne indekslenebilir bir açılış sayfası eklenir. Sitede herkese açık tek deneme
Sınav 1'dir (?basla=1 doğrudan başlatır). Sınava girişsiz başlanır; bitince sonuç
ve çözümler Google ile girişe kadar kilitli kalır (açılır pencere, sayfa değişmez),
giriş sonrası sonuç gösterilir ve panele kaydedilir. Analytics: başlangıçta start_exam_1, girişsiz bitişte
result_gate_view; kilitten girişte sign_up_end_of_exam_no_1 (yeni_uye) ve ardından
exam_1_complete. Bu akışta standart_sign_up gitmez (window.__girisAkisi, bkz. auth-ui.js). Web'de Sınav 1 bitişi
exam_1_complete olarak sonuç açıldığında gider; panel sınavları exam_complete gönderir. Kilitli sonuç 24 saat
localStorage'da tutulur; sayfa yenilenir ya da sonra geri gelinirse kilit ekranı
aynı cevaplarla yeniden açılır. Sınav 2–4 ve konu denemeleri panelde (giriş ister, ücretsiz). Eski
?basla=2..4 ve ?konu=<kategori> bağlantıları giriş penceresiyle panele gönderilir.

Kullanım (depo kökünden):  python3 tools/deneme-uret.py
panel/sinav-1/index.html değiştiğinde tekrar çalıştırılır.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
kaynak = (ROOT / 'panel/sinav-1/index.html').read_text(encoding='utf-8')
pillar = (ROOT / 'ehliyet-sinav-sorulari/index.html').read_text(encoding='utf-8')

def kes(metin, bas, son, dahil=False):
    i = metin.index(bas); j = metin.index(son, i + len(bas))
    return metin[i:j + len(son)] if dahil else metin[i + len(bas):j]

def degistir(metin, eski, yeni, adet=1):
    if metin.count(eski) != adet:
        sys.exit(f'BEKLENEN {adet} ESLESME, BULUNAN {metin.count(eski)}: {eski[:70]!r}')
    return metin.replace(eski, yeni)

# ---------- CSS ----------
sinav_css = kes(kaynak, '<style>', '</style>')
sinav_css = degistir(sinav_css,
    "  header{left:var(--pk-yan,186px);background:#fff;border-bottom:1px solid var(--line);\n"
    "    height:60px;padding:0 20px;display:flex;align-items:center;gap:18px;flex-wrap:wrap;position:sticky;top:0;z-index:20}",
    "  .sinav-modal>header{background:#fff;border-bottom:1px solid var(--line);\n"
    "    height:60px;padding:0 20px;display:flex;align-items:center;gap:18px;flex-wrap:wrap;position:static;z-index:20}")
sinav_css = degistir(sinav_css, "    header{height:auto;gap:8px 6px;padding:8px 12px}",
                                "    .sinav-modal>header{height:auto;gap:8px 6px;padding:8px 12px}")
# Sayfa geneli kurallar açılış sayfasının stilinden gelir.
sinav_css = degistir(sinav_css,
    "  body{margin:0;font-family:'Inter','Inter-fallback',-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:#fafafa;-webkit-font-smoothing:antialiased;letter-spacing:-.011em}\n", "")
sinav_css = degistir(sinav_css, "  *{box-sizing:border-box}\n", "")
sinav_css = degistir(sinav_css, ".result h1{margin:0 0 6px;", ".result h2{margin:0 0 6px;")
sinav_css = degistir(sinav_css, ".result h1{font-size:22px}", ".result h2{font-size:22px}")
sinav_css = degistir(sinav_css,
    "\n  /* Yan menünün yeri ilk boyamada ayrılır. panel-kabuk.js ertelenmiş bir modül\n"
    "     olduğu için burası olmazsa sayfa önce tam genişlikte çizilip sonra sağa kayar. */\n"
    "  body{margin-left:186px}\n  @media(max-width:820px){body{margin-left:0}}\n", "\n")
sinav_css = degistir(sinav_css, "  .logo{font-weight:600;color:#000;letter-spacing:-.01em;font-size:16px}\n  .logo span{background:#000;color:#fff;padding:2px 6px;border-radius:5px;margin-left:2px}\n", "")
# Overlay başta kapalı; açılınca body kaydırması kilitlenir.
sinav_css += ("\n  .sinav-overlay{display:none}\n  .sinav-overlay.acik{display:flex}\n"
              "  .modal{z-index:200}\n")

site_css = kes(pillar, '<style>', '</style>')
# Soru kartı stilleri bu sayfada kullanılmıyor; sadece kabuk + hero + cta + footer kalsın.
_a = site_css.index('  /* Question cards */'); _b = site_css.index('  /* CTA */')
site_css = site_css[:_a] + site_css[_b:]

acilis_css = """
  /* Açılış sayfası */
  .hero .ozet{display:flex;gap:28px;flex-wrap:wrap;margin-top:28px}
  .hero .ozet div{display:flex;flex-direction:column;gap:2px}
  .hero .ozet b{font-size:26px;font-weight:600;letter-spacing:-.03em;line-height:1}
  .hero .ozet span{font-size:13px;color:var(--muted)}
  .icerik{max-width:1100px;margin:0 auto;padding:0 28px 48px}
  .blok{padding:36px 0;border-top:1px solid var(--line)}
  .blok h2{margin:0 0 8px;font-size:24px;font-weight:600;letter-spacing:-.025em}
  .blok>p{margin:0 0 20px;font-size:15px;color:var(--muted);line-height:1.6;max-width:720px}
  .sinav-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
  @media(max-width:900px){.sinav-grid{grid-template-columns:repeat(2,1fr)}}
  @media(max-width:480px){.sinav-grid{grid-template-columns:1fr}}
  .sinav-kart{border:1px solid var(--line);border-radius:16px;padding:22px 20px;display:flex;flex-direction:column;gap:10px;background:#fff}
  .sinav-kart .no{font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
  .sinav-kart h3{margin:0;font-size:18px;font-weight:600;letter-spacing:-.02em}
  .sinav-kart p{margin:0 0 6px;font-size:13.5px;color:var(--muted);line-height:1.5;flex:1}
  .madde{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(2,1fr);gap:12px 28px}
  @media(max-width:700px){.madde{grid-template-columns:1fr}}
  .madde li{font-size:15px;line-height:1.6;color:#333;padding-left:22px;position:relative}
  .madde li::before{content:'';position:absolute;left:0;top:11px;width:8px;height:8px;border-radius:50%;background:#08090a}
  .dagilim{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:8px}
  @media(max-width:700px){.dagilim{grid-template-columns:repeat(2,1fr)}}
  .dagilim div{border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:#fafafa}
  .dagilim b{display:block;font-size:22px;font-weight:600;letter-spacing:-.03em}
  .dagilim span{font-size:13px;color:var(--muted)}
  .sss details{border-top:1px solid var(--line);padding:14px 0}
  .sss details:last-child{border-bottom:1px solid var(--line)}
  .sss summary{cursor:pointer;font-size:16px;font-weight:500;letter-spacing:-.01em;list-style:none;display:flex;justify-content:space-between;gap:12px}
  .sss summary::-webkit-details-marker{display:none}
  .sss summary::after{content:'+';color:var(--muted);font-weight:400}
  .sss details[open] summary::after{content:'–'}
  .sss p{margin:10px 0 0;font-size:15px;line-height:1.6;color:#444;max-width:760px}
  .baglantilar{display:flex;gap:12px;flex-wrap:wrap;margin-top:6px}
  .sonuc-kayit{max-width:660px;margin:18px auto 4px;border:1px solid var(--line);border-radius:14px;padding:18px 20px;background:#fafafa;text-align:left;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
  .sonuc-kayit p{margin:0;font-size:14px;line-height:1.55;color:#333;flex:1;min-width:220px}
  .sonuc-kayit button{background:#08090a;color:#fff;border:1px solid #08090a;border-radius:999px;padding:10px 18px;font:inherit;font-size:14px;font-weight:500;cursor:pointer;white-space:nowrap}
  .sonuc-kayit button:hover{background:#26282c}
  .h-yon{display:flex;gap:8px;order:3}
  .h-yon[hidden]{display:none}
  .h-yon a{text-decoration:none;display:inline-block}
  .sonuc-kilit{max-width:520px;margin:28px auto;padding:32px 28px;border:1px solid var(--line);border-radius:18px;background:#fff;text-align:center}
  .sonuc-kilit .kilit-ikon{width:52px;height:52px;margin:0 auto 14px;border-radius:50%;background:#f3f4f6;color:#08090a;display:flex;align-items:center;justify-content:center}
  .sonuc-kilit h2{margin:0 0 8px;font-size:22px;font-weight:600;letter-spacing:-.02em}
  .sonuc-kilit>p{margin:0 0 20px;font-size:15px;line-height:1.6;color:#444}
  .kilit-btn{background:#08090a;color:#fff;border:1px solid #08090a;border-radius:999px;padding:12px 22px;font:inherit;font-size:15px;font-weight:500;cursor:pointer}
  .kilit-btn:hover{background:#26282c}
  .kilit-btn:disabled{opacity:.6;cursor:default}
  .sonuc-kilit .kilit-hata{margin:12px 0 0;font-size:13.5px;color:#dc2626}
  .kilit-madde{list-style:none;padding:0;margin:20px 0 0;display:flex;flex-wrap:wrap;justify-content:center;gap:6px 18px;font-size:13px;color:var(--muted)}
  .kilit-madde li::before{content:'✓ ';color:#16a34a;font-weight:600}
"""

# ---------- JS ----------
sinav_js = kes(kaynak, '<script src="/assets/js/questions-1.js"></script>\n<script>\n',
                        '\n</script>\n  <script type="module" src="/assets/js/panel-kabuk.js"></script>')
sinav_js = degistir(sinav_js, "const Q = window.QUESTIONS;", "let Q = [];")
# Sayfanın tek <h1>'i açılıştaki "Ehliyet Deneme Sınavı"; sonuç ekranı başlığı <h2> olur.
sinav_js = degistir(sinav_js, "<h1>Sınav Sonucu</h1>", "<h2>Sınav Sonucu</h2>")
sinav_js = degistir(sinav_js, "let answers = new Array(Q.length).fill(null); // seçilen index veya null",
                              "let answers = []; // seçilen index veya null")
sinav_js = degistir(sinav_js, "  location.href='index.html';\n", "  kapat();\n")
# Girişsiz bitirilen sınavın sonucu (puan + inceleme modu) giriş yapılana kadar gizli.
sinav_js = degistir(sinav_js, "let finished = false;",
                              "let finished = false;\nlet sonucKilitli = false; // girişsiz bitirildiyse sonuç girişe kadar gizli\nlet kaydedildi = false;\nlet sureDoldu = false;")
sinav_js = degistir(sinav_js, "function render(){\n  const q = Q[cur];",
                              "function render(){\n  basligiGuncelle();\n  if (finished && sonucKilitli) { app.innerHTML = kilitHTML(); return; }\n  const q = Q[cur];")
sinav_js = degistir(sinav_js, "  finished=true; window.SINAV_DEVAM_EDIYOR=false;\n",
                              "  finished=true; window.SINAV_DEVAM_EDIYOR=false;\n  sonucKilitli = !window.__girisVar; sureDoldu = !!timeUp;\n  if (sonucKilitli) bekleyenSakla();\n")
sinav_js = degistir(sinav_js, "function restart(){\n  _examStarted=false;",
                              "function restart(){\n  _examStarted=false; kaydedildi=false; bekleyenSil();")
sinav_js = degistir(sinav_js, """  if(!_examStarted && typeof gtag==='function'){
    _examStarted=true;
    // Oturum panel-kabuk.js'te gecikmeli doğrulanır; girişsiz ziyaretçi yönlendirilirken exam_start gitmesin.
    const gonder = () => gtag('event','exam_start',{exam_name:SINAV_ADI, logged_in:true, kaynak:'panel', konu:''});
    window.__oturumDogrulandi ? gonder() : document.addEventListener('pk-oturum', gonder, { once:true });
  }""",
                              "  if(!_examStarted && typeof gtag==='function'){ _examStarted=true; gtag('event','start_exam_1',{exam_name:SINAV_ADI, logged_in:!!window.__girisVar, kaynak:'web', konu:''}); }")
# Web'de panel-kabuk yok; terk koşulu oturum doğrulamasını beklemez.
sinav_js = degistir(sinav_js, "  // Girişsiz ziyaretçi yönlendirilirken de sayfa kapanır; yalnızca doğrulanmış oturumda sayılır.\n"
                              "  if (window.__oturumDogrulandi && window.SINAV_DEVAM_EDIYOR",
                              "  if (window.SINAV_DEVAM_EDIYOR")
sinav_js = degistir(sinav_js, "      questions_total: Q.length,\n      kaynak: 'panel',\n      konu: ''\n",
                              "      questions_total: Q.length,\n      kaynak: 'web',\n      konu: ''\n")
# Sonuç kaydı: giriş yoksa da analytics gitsin, kayıt yalnızca giriş varsa.
sinav_js = degistir(sinav_js,
"""      const { auth, denemeleriGetir } = await import('/assets/js/firebase.js');
      const user = auth.currentUser;
      if (!user) return;
      const { denemeKaydet } = await import('/assets/js/firebase.js');
      const s = scoreObj();
      const order = ["İlk Yardım","Trafik ve Çevre","Araç Tekniği","Trafik Adabı"];
      const bolumler = {};
      Q.forEach((q,i) => {
        if (!bolumler[q.section]) bolumler[q.section] = {toplam:0,dogru:0};
        bolumler[q.section].toplam++;
        if (answers[i] === q.correct) bolumler[q.section].dogru++;
      });
      await denemeKaydet(user.uid, {
        sinav: SINAV_ADI,
        dogru: s.correct,
        yanlis: s.wrong,
        bos: s.empty,
        puan: s.points,
        gecti: s.correct >= PASS_CORRECT,
        bolumler
      });
      // exam_complete event
      if (typeof gtag === 'function') {
        let examCount = 0;
        try { const prev = await denemeleriGetir(user.uid); examCount = prev.length; } catch(_){}
        gtag('event', 'exam_complete', {
          exam_name: SINAV_ADI,
          score: s.points,
          correct: s.correct,
          wrong: s.wrong,
          empty: s.empty,
          questions_answered: s.correct + s.wrong,
          passed: s.correct >= PASS_CORRECT,
          exam_count: examCount,
          time_up: !!timeUp,
          logged_in: true,
          kaynak: 'panel',
          konu: ''
        });
      }""",
"""      const s = scoreObj();
      const { auth } = await import('/assets/js/firebase.js');
      const user = auth.currentUser;
      if (user) {
        if (sonucKilitli) { sonucKilitli = false; render(); }
        bekleyenSil();
        tamamlandiGonder(await sonucuKaydet(user));
      } else if (sonucKilitli && typeof gtag === 'function') {
        // Sonuç kilitli: exam_1_complete sonuç açılınca (girişten sonra) gider.
        gtag('event', 'result_gate_view', { exam_name: SINAV_ADI, questions_answered: s.correct + s.wrong });
      }""")
# Sonuç ekranına giriş yapmamış kullanıcı için kayıt daveti
sinav_js = degistir(sinav_js,
"""      <div class="row">
        <button class="nav-btn next" onclick="restart()">Tekrar Başla</button>
      </div>""",
"""      <div class="sonuc-kayit">
        <p><b>Sıradaki deneme hazır.</b> Bu sonuç paneline kaydedildi. Sınav 2, 3, 4 ve konu denemeleri de panelinde.</p>
        <button type="button" onclick="location.href='/panel/?g=sinavlar'">Diğer sınavları keşfet</button>
      </div>
      <div class="row">
        <button class="nav-btn next" onclick="restart()">Tekrar Başla</button>
        <button class="nav-btn" onclick="location.href='/panel/'">Panele Git</button>
      </div>""")
# Klavye kısayolları yalnızca sınav açıkken
sinav_js = degistir(sinav_js, "document.addEventListener('keydown',e=>{\n  if(e.key==='ArrowLeft') go(-1);",
                              "document.addEventListener('keydown',e=>{\n  if(!Q.length || !overlay.classList.contains('acik')) return;\n  if(e.key==='ArrowLeft') go(-1);")
sinav_js = degistir(sinav_js, "\nstartTimer();\nrender();", """
/* ---- Açık deneme: Sınav 1 ---- */
const overlay = document.getElementById('sinavOverlay');
let yuklenen = null;
function sinavYukle(){
  if (yuklenen) return Promise.resolve(yuklenen);
  return new Promise((res, rej) => {
    const s = document.createElement('script');
    s.src = '/assets/js/questions-1.js';
    s.onload = () => { yuklenen = window.QUESTIONS; res(yuklenen); };
    s.onerror = () => rej(new Error('Sınav yüklenemedi'));
    document.head.appendChild(s);
  });
}
// ---- Sonuç kilidi ----
let fb = null; // firebase.js; açılır pencere tıklamayla aynı anda açılsın diye önceden yüklenir
function kilitHTML(){
  const cevaplanan = answers.filter(a => a !== null).length;
  return `<div class="sonuc-kilit">
    <div class="kilit-ikon" aria-hidden="true"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg></div>
    <h2>Sınavı tamamladın</h2>
    <p>${Q.length} sorunun ${cevaplanan} tanesini cevapladın. Puanını, doğru ve yanlışlarını ve her sorunun doğru cevabını görmek için ücretsiz üye ol.</p>
    <button type="button" class="kilit-btn" onclick="sonucIcinGiris(this)">Google ile devam et, sonucu gör</button>
    <p class="kilit-hata" hidden>Giriş başlatılamadı. Lütfen tekrar dene.</p>
    <ul class="kilit-madde"><li>Ücretsiz, reklamsız</li><li>Sonucun hesabına kaydedilir</li><li>3 farklı deneme sınavına daha erişebilir ve her konu ile ilgili konu deneme sınavlarını görebilirsin</li></ul>
  </div>`;
}
async function sonucuKaydet(user){
  if (kaydedildi) return 0;
  kaydedildi = true;
  const { denemeKaydet, denemeleriGetir } = await import('/assets/js/firebase.js');
  const s = scoreObj();
  const bolumler = {};
  Q.forEach((q,i) => {
    if (!bolumler[q.section]) bolumler[q.section] = {toplam:0,dogru:0};
    bolumler[q.section].toplam++;
    if (answers[i] === q.correct) bolumler[q.section].dogru++;
  });
  await denemeKaydet(user.uid, {
    sinav: SINAV_ADI,
    dogru: s.correct,
    yanlis: s.wrong,
    bos: s.empty,
    puan: s.points,
    gecti: s.correct >= PASS_CORRECT,
    bolumler
  });
  try { return (await denemeleriGetir(user.uid)).length; } catch(_) { return 0; }
}
// Web'de Sınav 1 bitişi panelin exam_complete'inden ayrı sayılır; sonuç ekranı açıldığında gider
// (girişliyse bitişte, değilse kilitten girişte).
function tamamlandiGonder(examCount){
  if (typeof gtag !== 'function') return;
  const s = scoreObj();
  gtag('event', 'exam_1_complete', {
    exam_name: SINAV_ADI,
    score: s.points,
    correct: s.correct,
    wrong: s.wrong,
    empty: s.empty,
    questions_answered: s.correct + s.wrong,
    passed: s.correct >= PASS_CORRECT,
    exam_count: examCount,
    time_up: sureDoldu,
    logged_in: true,
    kaynak: 'web',
    konu: ''
  });
}
function sonucuAc(user){
  if (!sonucKilitli || !user) return;
  sonucKilitli = false;
  bekleyenSil();
  render();
  // Hesap az önce açıldıysa oluşturma ve son giriş zamanı aynıdır.
  const yeni = !!user.metadata && user.metadata.creationTime === user.metadata.lastSignInTime;
  if (typeof gtag === 'function') gtag('event', 'sign_up_end_of_exam_no_1', { exam_name: SINAV_ADI, yeni_uye: yeni });
  sonucuKaydet(user).catch(e => { console.error('Sonuç kaydedilemedi:', e); return 0; }).then(tamamlandiGonder);
}
// Kilitli sonuç yenilemede ve sonraki ziyarette kaybolmasın diye tarayıcıda tutulur.
const BEKLEYEN = 'ehliyet-bekleyen-sonuc';
function bekleyenSakla(){ try { localStorage.setItem(BEKLEYEN, JSON.stringify({ sinav: SINAV_ADI, answers, sureDoldu, t: Date.now() })); } catch(_){} }
function bekleyenSil(){ try { localStorage.removeItem(BEKLEYEN); } catch(_){} }
function bekleyenOku(){
  try {
    const b = JSON.parse(localStorage.getItem(BEKLEYEN) || 'null');
    if (b && b.sinav === SINAV_ADI && Array.isArray(b.answers) && Date.now() - b.t < 24*60*60*1000) return b;
  } catch(_){}
  bekleyenSil(); return null;
}
async function bekleyeniAc(b){
  try { Q = await sinavYukle(); } catch(_) { return; }
  if (b.answers.length !== Q.length) { bekleyenSil(); return; }
  answers = b.answers; cur = 0; finished = true; kaydedildi = false; sureDoldu = !!b.sureDoldu;
  sonucKilitli = !window.__girisVar;
  window.SINAV_DEVAM_EDIYOR = false;
  document.getElementById('finishBtn').textContent = 'Tekrar Başla';
  document.querySelector('.timer-label').style.display = 'none';
  timerEl.style.display = 'none';
  overlay.classList.add('acik');
  document.body.style.overflow = 'hidden';
  history.replaceState(null, '', '?basla=1');
  render();
  if (fb && fb.auth.currentUser) sonucuAc(fb.auth.currentUser);
}
function sonucIcinGiris(btn){
  const hata = btn.parentNode.querySelector('.kilit-hata');
  hata.hidden = true; btn.disabled = true;
  // auth-ui.js bu akıştan gelen yeni üyeyi standart_sign_up olarak saymaz.
  window.__girisAkisi = 'sinav1';
  const giris = fb ? fb.girisYap().then(() => fb) : import('/assets/js/firebase.js').then(m => m.girisYap().then(() => m));
  giris.then(m => sonucuAc(m.auth.currentUser)).catch(e => {
    window.__girisAkisi = null;
    btn.disabled = false;
    if (e?.code !== 'auth/popup-closed-by-user' && e?.code !== 'auth/cancelled-popup-request') { console.error('Giriş başarısız:', e); hata.hidden = false; }
  });
}
async function sinaviBaslat(){
  const btn = document.querySelector('[data-sinav]');
  btn.disabled = true; btn.textContent = 'Yükleniyor…';
  try { Q = await sinavYukle(); }
  catch (e) { btn.disabled = false; btn.textContent = 'Deneme Sınavına Başla'; alert('Sınav yüklenemedi, lütfen tekrar dene.'); return; }
  btn.disabled = false; btn.textContent = 'Deneme Sınavına Başla';
  _examStarted = false; kaydedildi = false; bekleyenSil();
  answers = new Array(Q.length).fill(null);
  cur = 0; finished = false; remaining = DURATION;
  timerEl.classList.remove('low');
  document.querySelector('.timer-label').style.display = '';
  timerEl.style.display = '';
  document.getElementById('finishBtn').textContent = 'Sınavı Bitir';
  overlay.classList.add('acik');
  document.body.style.overflow = 'hidden';
  // ?s= kullanılmaz: GA4 onu site içi arama sayıp view_search_results gönderir.
  history.replaceState(null, '', '?basla=1');
  clearInterval(timerId); startTimer(); render();
  overlay.querySelector('.wrap').scrollTop = 0;
}
function kapat(){
  if (finished && sonucKilitli) bekleyenSil(); // kişi kilit ekranından kendisi çıktı
  clearInterval(timerId);
  window.SINAV_DEVAM_EDIYOR = false;
  overlay.classList.remove('acik');
  document.body.style.overflow = '';
  history.replaceState(null, '', location.pathname);
}
function cikisIste(){
  if (window.SINAV_DEVAM_EDIYOR && !finished && !confirm('Sınav devam ediyor. Çıkarsan cevapların kaybolur. Çıkmak istiyor musun?')) return;
  if (window.__girisVar) { location.href = '/panel/'; return; } // giriş yapmış kullanıcı ürünün içine
  kapat();
}
// Sonuç görünürken sağ üstte "Tekrar Başla" yerine Web sitesi / Panel.
function basligiGuncelle(){
  const sonucGorunur = finished && !sonucKilitli;
  document.getElementById('finishBtn').hidden = sonucGorunur;
  document.getElementById('hYon').hidden = !sonucGorunur;
}
// Girişliyse hedefe gider, değilse giriş penceresi açılır ve giriş sonrası hedefe gidilir.
function girisYap(hedef = '/panel/?g=sinavlar'){
  const git = () => location.href = hedef;
  if (typeof window.ehliyetGiris === 'function') window.ehliyetGiris(hedef);
  else import('/assets/js/auth-ui.js').then(() => window.ehliyetGiris ? window.ehliyetGiris(hedef) : git()).catch(git);
}
document.querySelectorAll('[data-sinav]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); sinaviBaslat(); }));
document.querySelectorAll('[data-panel]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); girisYap(b.dataset.panel); }));

// Oturum durumu: sonuç kilidi ve analytics için. Firebase kritik yolda değil.
function oturumuIzle(){
  import('/assets/js/firebase.js')
    .then(m => { fb = m; m.kullaniciDinle(u => { window.__girisVar = !!u; if (u && sonucKilitli) sonucuAc(u); else if (finished) render(); }); })
    .catch(() => {});
}
if ('requestIdleCallback' in window) requestIdleCallback(oturumuIzle, { timeout: 2000 }); else setTimeout(oturumuIzle, 300);

// ?basla=1 Sınav 1'i doğrudan başlatır (soru, hap, ders ve konu sayfalarından gelen bağlantılar).
// Bekleyen kilitli sonuç varsa yeni sınav yerine o açılır.
// Sınav 2–4 ve konu denemeleri panele taşındı; eski bağlantılar giriş penceresiyle panele gider.
const _prm = new URLSearchParams(location.search);
const _konu = _prm.get('konu'), _no = _prm.get('basla');
if (['ilk-yardim','trafik-ve-cevre','arac-teknigi','trafik-adabi'].includes(_konu)) {
  history.replaceState(null, '', location.pathname); girisYap('/panel/konu-denemesi/?k=' + _konu);
} else if (['2','3','4'].includes(_no)) {
  history.replaceState(null, '', location.pathname); girisYap('/panel/sinav-' + _no + '/kilavuz/');
} else {
  const _bekleyen = bekleyenOku();
  if (_bekleyen) bekleyeniAc(_bekleyen);
  else if (_no) sinaviBaslat();
}""")

# ---------- Sınav kabuğu (overlay + onay modalı) ----------
sinav_govde = kes(kaynak, '<body>\n', '\n<script src="/assets/js/questions-1.js"></script>')
sinav_govde = degistir(sinav_govde, '<div class="sinav-overlay">', '<div class="sinav-overlay" id="sinavOverlay" role="dialog" aria-modal="true" aria-label="Deneme sınavı">')
sinav_govde = degistir(sinav_govde,
    """  <button class="exit-btn" onclick="location.href=(window.SINAV_DEVAM_EDIYOR && !confirm('Sınav devam ediyor. Çıkarsan cevapların kaybolur. Çıkmak istiyor musun?')) ? location.href : '/panel/'">‹ Çıkış</button>""",
    """  <button class="exit-btn" type="button" onclick="cikisIste()">‹ Çıkış</button>""")
# Sonuç ekranında (giriş yapılmış) sağ üstte siteye ve panele dönüş; "Tekrar Başla" alttaki satırda kalır.
sinav_govde = degistir(sinav_govde, '    <button class="finish-btn" id="finishBtn">Sınavı Bitir</button>\n',
    '    <button class="finish-btn" id="finishBtn">Sınavı Bitir</button>\n'
    '    <span class="h-yon" id="hYon" hidden><a class="exit-btn" href="/">Web sitesi</a><a class="finish-btn" href="/panel/">Panel</a></span>\n')

# ---------- Site kabuğu ----------
site_header = kes(pillar, '<body>\n', '  <main>')
# Pillar'a banner-ekle.py'nin koyduğu banner bu sayfada istenmez (kendi sayfasına çıkar).
site_header = re.sub(r'<!-- ust-banner -->.*?<!-- /ust-banner -->\n', '', site_header, flags=re.S)
site_footer = kes(pillar, '  <footer class="site-footer">', '  </footer>', dahil=True)
ga = kes(pillar, "<!-- Google tag (gtag.js) — sayfa yüklendikten sonra yüklenir -->", "</body>", dahil=False)
ga = "<!-- Google tag (gtag.js) — sayfa yüklendikten sonra yüklenir -->" + ga

TITLE = "Ehliyet Deneme Sınavı Çöz: 50 Soru, 45 Dakika | ehliyet.digital"
DESC = ("Ücretsiz ehliyet deneme sınavı: MEB e-sınav formatında 50 soru, 45 dakika. Girişsiz başla;"
        " puanın ve çözümlü cevaplar ücretsiz üyelikle açılır.")
assert len(DESC) <= 155, len(DESC)

html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://www.gstatic.com" crossorigin>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="https://ehliyet.digital/deneme-sinavi/">
<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="ehliyet.digital">
<meta property="og:title" content="Ehliyet Deneme Sınavı Çöz: 50 Soru, 45 Dakika">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="https://ehliyet.digital/deneme-sinavi/">
<meta property="og:locale" content="tr_TR">
<meta property="og:image" content="https://ehliyet.digital/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ehliyet.digital — Ehliyet deneme sınavı">
<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Ehliyet Deneme Sınavı Çöz: 50 Soru, 45 Dakika">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="https://ehliyet.digital/og-image.png">
<meta name="twitter:image:alt" content="ehliyet.digital — Ehliyet deneme sınavı">
<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/css/fonts.css" as="style" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="/assets/css/fonts.css"></noscript>
<link rel="alternate" type="application/rss+xml" title="ehliyet.digital RSS" href="/feed.xml">
<style>{site_css}{acilis_css}
  /* ---- Sınav motoru (panel/sinav-1 ile ortak) ---- */{sinav_css}</style>
</head>
<body>
{site_header}  <main>
    <div class="hero">
      <nav class="breadcrumb" aria-label="Gezinme">
        <a href="/">Ana Sayfa</a> <span class="sep">›</span> <a href="/ehliyet-sinav-sorulari/">Ehliyet Sınav Soruları</a> <span class="sep">›</span> <span>Deneme Sınavı</span>
      </nav>
      <h1>Ehliyet Deneme Sınavı</h1>
      <p>MEB e-sınavıyla birebir aynı formatta ücretsiz deneme: <b>50 soru, 45 dakika</b>, dört bölüm. Giriş yapmadan hemen başla, süre tutulur. Sınav bitince ücretsiz üye ol; puanını ve her sorunun doğru cevabını gör. Sorular gerçek ehliyet sınavında çıkmış sorulardan derlendi.</p>
      <div class="hero-actions">
        <button class="btn btn-primary btn-lg" type="button" data-sinav="1">Deneme Sınavına Başla</button>
        <a class="btn btn-outline btn-lg" href="#diger-denemeler">Diğer denemeler</a>
      </div>
      <div class="ozet" aria-label="Sınav özeti">
        <div><b>50</b><span>soru</span></div>
        <div><b>45</b><span>dakika</span></div>
        <div><b>70</b><span>geçme puanı</span></div>
        <div><b>4</b><span>bölüm</span></div>
      </div>
    </div>

    <div class="icerik">
      <section class="blok" id="diger-denemeler">
        <h2>Daha fazla deneme</h2>
        <p>Bu sayfadaki deneme herkese açık. Üç tam deneme daha ve konu bazlı denemeler panelde; hepsi ücretsiz, Google ile giriş yapman yeterli. Panelde sonuçların kaydedilir, puan gelişimini ve eksik konularını görürsün.</p>
        <div class="sinav-grid">
          <div class="sinav-kart"><span class="no">Deneme 2</span><h3>Sınav 2</h3><p>Görselli trafik işareti ve kavşak soruları ağırlıklı.</p><a class="btn btn-outline" href="/panel/sinav-2/kilavuz/" data-panel="/panel/sinav-2/kilavuz/" rel="nofollow">Çözmek için giriş yap!</a></div>
          <div class="sinav-kart"><span class="no">Deneme 3</span><h3>Sınav 3</h3><p>İlk yardım ve araç tekniği çeldiricileri yoğun.</p><a class="btn btn-outline" href="/panel/sinav-3/kilavuz/" data-panel="/panel/sinav-3/kilavuz/" rel="nofollow">Çözmek için giriş yap!</a></div>
          <div class="sinav-kart"><span class="no">Deneme 4</span><h3>Sınav 4</h3><p>Video ve görsel sorularıyla en güncel e-sınav formatı.</p><a class="btn btn-outline" href="/panel/sinav-4/kilavuz/" data-panel="/panel/sinav-4/kilavuz/" rel="nofollow">Çözmek için giriş yap!</a></div>
          <div class="sinav-kart"><span class="no">Konu bazlı</span><h3>Konu denemeleri</h3><p>İlk Yardım, Trafik ve Çevre, Araç Tekniği, Trafik Adabı: dört sınavın o konudaki soruları tek denemede.</p><a class="btn btn-outline" href="/panel/?g=sinavlar" data-panel="/panel/?g=sinavlar" rel="nofollow">Çözmek için giriş yap!</a></div>
        </div>
      </section>

      <section class="blok">
        <h2>Deneme sınavı nasıl çalışır?</h2>
        <p>Arayüz, süre ve puanlama gerçek e-sınavla aynı. Sınav sırasında sorular arasında ileri geri gidebilir, soru haritasından istediğin soruya atlayabilirsin.</p>
        <ul class="madde">
          <li><b>Girişsiz başla.</b> Sayfayı aç, sınava başla. Sınav bitince sonucunu görmek için Google ile ücretsiz giriş yaparsın; sonucun hesabına kaydedilir.</li>
          <li><b>50 soru, 45 dakika.</b> Süre dolunca sınav otomatik biter, işaretlediklerin puanlanır.</li>
          <li><b>Puanlama gerçek sınav gibi.</b> Her doğru 2 puan, yanlış doğruyu götürmez. Geçmek için 70 puan, yani en az 35 doğru.</li>
          <li><b>Ayrıntılı sonuç.</b> Puan, doğru, yanlış ve boş sayısı; konu bazlı performans grafiği.</li>
          <li><b>Çözümlü inceleme.</b> Sınav bitince her sorunun doğru cevabı ve senin işaretin yan yana gösterilir.</li>
          <li><b>Ücretsiz ve reklamsız.</b> Ücret veya reklam yok; üyelik de ücretsiz.</li>
        </ul>
      </section>

      <section class="blok">
        <h2>Gerçek ehliyet sınavıyla aynı soru dağılımı</h2>
        <p>MEB e-sınavında 50 soru dört bölümden gelir. Denemelerdeki dağılım da aynıdır, böylece hangi bölümde eksiğin olduğunu gerçek sınavdaki ağırlığıyla görürsün.</p>
        <div class="dagilim">
          <div><b>12</b><span>İlk Yardım</span></div>
          <div><b>23</b><span>Trafik ve Çevre</span></div>
          <div><b>9</b><span>Araç Tekniği</span></div>
          <div><b>6</b><span>Trafik Adabı</span></div>
        </div>
      </section>

      <section class="blok sss">
        <h2>Sık sorulan sorular</h2>
        <details><summary>Deneme sınavı ücretsiz mi?</summary><p>Evet. Bu sayfadaki denemeye girişsiz başlarsın; sonucu görmek için ücretsiz üye olman yeterli. Sınav 2, 3, 4 ve konu denemeleri de ücretsiz, panelde. Reklam yok.</p></details>
        <details><summary>Giriş yapmam gerekiyor mu?</summary><p>Sınava başlamak için hayır. Sınav bitince puanını ve çözümleri görmek için Google ile ücretsiz giriş yaparsın; sonucun hesabına kaydedilir ve panelde puan gelişimini, konu bazlı eksiklerini takip edersin. Diğer denemeler de panelde.</p></details>
        <details><summary>Sorular gerçek sınavdan mı?</summary><p>Sorular MEB MTSK e-sınavında çıkmış sorulardan derlendi. Dört denemede toplam 200 soru var. Aynı soruları tek tek cevaplarıyla incelemek için <a href="/ehliyet-sinav-sorulari/">ehliyet sınav soruları</a> sayfasına bakabilirsin.</p></details>
        <details><summary>Kaç doğru ile geçilir?</summary><p>Gerçek sınavda ve bu denemede 50 soruda en az 35 doğru gerekir. Her doğru 2 puandır, geçme notu 70'tir. Yanlış cevaplar doğruları götürmez, bu yüzden boş bırakmak yerine işaretlemek daha mantıklıdır.</p></details>
        <details><summary>Süre ne kadar?</summary><p>45 dakika, gerçek e-sınavla aynı. Süre dolduğunda sınav otomatik olarak biter ve o ana kadar işaretlediklerin puanlanır.</p></details>
        <details><summary>Sınav bitince ne görürüm?</summary><p>Puanını, doğru, yanlış ve boş sayılarını, bölüm bazlı başarı yüzdelerini ve her sorunun doğru cevabını görürsün. Yanlış yaptığın soruların konusunu <a href="/dersler/">ders notlarından</a> veya <a href="/hap-bilgiler/">hap bilgilerden</a> hızlıca tekrar edebilirsin.</p></details>
      </section>

      <section class="blok">
        <h2>Sınava hazırlanırken</h2>
        <p>Deneme sonucunda düşük çıkan bölüm için kısa yol: önce o konunun hap bilgilerini oku, sonra ders notuna geç, ardından yeni bir deneme çöz.</p>
        <div class="baglantilar">
          <a class="btn btn-outline" href="/ehliyet-sinav-sorulari/">Çıkmış sorular ve cevapları</a>
          <a class="btn btn-outline" href="/hap-bilgiler/">Hap bilgiler</a>
          <a class="btn btn-outline" href="/dersler/">Ders notları</a>
          <a class="btn btn-outline" href="/ehliyet-sinav-konulari/">Sınav konuları</a>
        </div>
      </section>
    </div>

    <section class="cta">
      <div class="cta-inner">
        <h2>Hazırsan başlayalım</h2>
        <p>50 soru, 45 dakika. Girişsiz başla, sınav bitince ücretsiz üye olup sonucunu gör.</p>
        <button class="btn btn-primary btn-lg" type="button" data-sinav="1">Deneme Sınavına Başla</button>
      </div>
    </section>
  </main>
{site_footer}

{sinav_govde}
<script>
{sinav_js}
</script>
  <script src="/assets/js/feedback.js" defer></script>
  <script type="module" src="/assets/js/auth-ui.js"></script>
  <script src="/assets/js/mobile-nav.js" defer></script>
{ga}</body>
</html>
"""

hedef = ROOT / 'deneme-sinavi/index.html'
hedef.parent.mkdir(exist_ok=True)
hedef.write_text(html, encoding='utf-8')
print('yazildi', hedef.relative_to(ROOT), len(html.splitlines()), 'satir')
