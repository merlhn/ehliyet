#!/usr/bin/env python3
"""/deneme-sinavi/index.html'i panel/sinav-1'deki sınav motorundan üretir.

Sınav CSS'i ve JS'i panel sayfasından alınır, panel kabuğuna bağımlı kısımlar
(yan menü boşluğu, oturum zorunluluğu, /panel/ yönlendirmeleri) çıkarılır,
üstüne indekslenebilir bir açılış sayfası eklenir. 4 sınav da aynı sayfadan
?s=N ile yüklenir; giriş gerektirmez, giriş varsa sonuç kaydedilir.
?konu=<kategori> ile dört sınavın o konudaki soruları tek denemede toplanır
(süre soru başına 54 sn, geçme %70); konu denemeleri panele kaydedilmez.

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
"""

# ---------- JS ----------
sinav_js = kes(kaynak, '<script src="/assets/js/questions-1.js"></script>\n<script>\n',
                        '\n</script>\n  <script type="module" src="/assets/js/panel-kabuk.js"></script>')
sinav_js = degistir(sinav_js, "const Q = window.QUESTIONS;", "let Q = [];")
sinav_js = degistir(sinav_js, "const SINAV_ADI = 'Sınav 1';", "let SINAV_ADI = 'Sınav 1';\nlet SINAV_NO = 1;\nlet KONU = null;")
sinav_js = degistir(sinav_js, "const PASS_CORRECT = 35;", "let PASS_CORRECT = 35;")
sinav_js = degistir(sinav_js, "const DURATION = 45*60;", "let DURATION = 45*60;")
sinav_js = degistir(sinav_js, "return {correct,wrong,empty,points:correct*2};", "return {correct,wrong,empty,points: Q.length===50 ? correct*2 : Math.round(correct/Q.length*100)};")
sinav_js = degistir(sinav_js, '<span class="qno">Soru ${q.n}</span>', '<span class="qno">Soru ${cur+1}</span>')
_m = re.search(r'(      <p style="color:#444;max-width:660px.*?</p>\n)', sinav_js, re.S)
assert _m and '`' not in _m.group(1), 'puanlama paragrafi'
sinav_js = sinav_js[:_m.start()] + "      ${KONU ? '' : `" + _m.group(1).rstrip('\n') + "`}\n" + sinav_js[_m.end():]
sinav_js = degistir(sinav_js, "let answers = new Array(Q.length).fill(null); // seçilen index veya null",
                              "let answers = []; // seçilen index veya null")
sinav_js = degistir(sinav_js, "  location.href='index.html';\n", "  kapat();\n")
sinav_js = degistir(sinav_js, "  if(!_examStarted && typeof gtag==='function'){ _examStarted=true; gtag('event','exam_start',{exam_name:SINAV_ADI}); }",
                              "  if(!_examStarted && typeof gtag==='function'){ _examStarted=true; gtag('event','exam_start',{exam_name:SINAV_ADI, logged_in:!!window.__girisVar, kaynak:'acik', konu:KONU||''}); }")
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
          passed: s.correct >= PASS_CORRECT,
          exam_count: examCount,
          time_up: !!timeUp
        });
      }""",
"""      const s = scoreObj();
      const { auth, denemeleriGetir, denemeKaydet } = await import('/assets/js/firebase.js');
      const user = auth.currentUser;
      let examCount = 0;
      if (user && !KONU) {
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
        try { const prev = await denemeleriGetir(user.uid); examCount = prev.length; } catch(_){}
      }
      // exam_complete event — giriş olmasa da gider
      if (typeof gtag === 'function') {
        gtag('event', 'exam_complete', {
          exam_name: SINAV_ADI,
          score: s.points,
          correct: s.correct,
          wrong: s.wrong,
          empty: s.empty,
          passed: s.correct >= PASS_CORRECT,
          exam_count: examCount,
          time_up: !!timeUp,
          logged_in: !!user,
          kaynak: 'acik',
          konu: KONU || ''
        });
      }""")
# Sonuç ekranına giriş yapmamış kullanıcı için kayıt daveti
sinav_js = degistir(sinav_js,
"""      <div class="row">
        <button class="nav-btn next" onclick="restart()">Tekrar Başla</button>
      </div>""",
"""      ${window.__girisVar ? '' : `<div class="sonuc-kayit">
        <p><b>Sonucunu kaydet, gelişimini gör.</b> Google ile giriş yaparsan denemelerin hesabına kaydedilir; hangi konuda eksiğin olduğunu takip edersin.</p>
        <button type="button" onclick="girisYap()">Google ile giriş yap</button>
      </div>`}
      <div class="row">
        <button class="nav-btn next" onclick="restart()">Tekrar Başla</button>
        <button class="nav-btn" onclick="kapat()">Sınav Seçimine Dön</button>
      </div>""")
# Klavye kısayolları yalnızca sınav açıkken
sinav_js = degistir(sinav_js, "document.addEventListener('keydown',e=>{\n  if(e.key==='ArrowLeft') go(-1);",
                              "document.addEventListener('keydown',e=>{\n  if(!Q.length || !overlay.classList.contains('acik')) return;\n  if(e.key==='ArrowLeft') go(-1);")
sinav_js = degistir(sinav_js, "\nstartTimer();\nrender();", """
/* ---- Açık deneme: sınav seçimi ve yükleme ---- */
const overlay = document.getElementById('sinavOverlay');
const yuklenen = {};
function sinavYukle(n){
  if (yuklenen[n]) return Promise.resolve(yuklenen[n]);
  return new Promise((res, rej) => {
    const s = document.createElement('script');
    s.src = '/assets/js/questions-' + n + '.js';
    s.onload = () => { yuklenen[n] = window.QUESTIONS; res(yuklenen[n]); };
    s.onerror = () => rej(new Error('Sınav yüklenemedi'));
    document.head.appendChild(s);
  });
}
const KONULAR = {'ilk-yardim':'İlk Yardım','trafik-ve-cevre':'Trafik ve Çevre','arac-teknigi':'Araç Tekniği','trafik-adabi':'Trafik Adabı'};
async function konuYukle(slug){
  const hepsi = [];
  for (const n of [1,2,3,4]) { const q = await sinavYukle(n); hepsi.push(...q.filter(x => x.section === KONULAR[slug])); }
  return hepsi;
}
async function sinaviBaslat(n, konu){
  n = [1,2,3,4].includes(+n) ? +n : 1;
  konu = KONULAR[konu] ? konu : null;
  const btn = konu ? null : document.querySelector('[data-sinav="' + n + '"]');
  if (btn) { btn.disabled = true; btn.textContent = 'Yükleniyor…'; }
  try { Q = konu ? await konuYukle(konu) : await sinavYukle(n); }
  catch (e) { if (btn) { btn.disabled = false; btn.textContent = 'Sınava Başla'; } alert('Sınav yüklenemedi, lütfen tekrar dene.'); return; }
  if (btn) { btn.disabled = false; btn.textContent = 'Sınava Başla'; }
  KONU = konu;
  if (konu) { SINAV_ADI = KONULAR[konu] + ' Denemesi'; DURATION = Q.length * 54; PASS_CORRECT = Math.ceil(Q.length * 0.7); }
  else { SINAV_ADI = 'Sınav ' + n; DURATION = 45 * 60; PASS_CORRECT = 35; }
  SINAV_NO = n; _examStarted = false;
  answers = new Array(Q.length).fill(null);
  cur = 0; finished = false; remaining = DURATION;
  timerEl.classList.remove('low');
  document.querySelector('.timer-label').style.display = '';
  timerEl.style.display = '';
  document.getElementById('finishBtn').textContent = 'Sınavı Bitir';
  document.querySelector('.h-title').textContent = SINAV_ADI;
  overlay.classList.add('acik');
  document.body.style.overflow = 'hidden';
  history.replaceState(null, '', konu ? '?konu=' + konu : '?s=' + n);
  clearInterval(timerId); startTimer(); render();
  overlay.querySelector('.wrap').scrollTop = 0;
}
function kapat(){
  clearInterval(timerId);
  window.SINAV_DEVAM_EDIYOR = false;
  overlay.classList.remove('acik');
  document.body.style.overflow = '';
  history.replaceState(null, '', location.pathname);
}
function cikisIste(){
  if (window.SINAV_DEVAM_EDIYOR && !finished && !confirm('Sınav devam ediyor. Çıkarsan cevapların kaybolur. Çıkmak istiyor musun?')) return;
  kapat();
}
function girisYap(){
  const git = () => location.href = '/panel/?g=sinavlar';
  if (typeof window.ehliyetGiris === 'function') window.ehliyetGiris('/panel/?g=sinavlar');
  else import('/assets/js/auth-ui.js').then(() => window.ehliyetGiris ? window.ehliyetGiris('/panel/?g=sinavlar') : git()).catch(git);
}
document.querySelectorAll('[data-sinav]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); sinaviBaslat(b.dataset.sinav); }));

// Oturum durumu: sonuç ekranındaki kayıt daveti ve analytics için. Firebase kritik yolda değil.
function oturumuIzle(){
  import('/assets/js/firebase.js')
    .then(({ kullaniciDinle }) => kullaniciDinle(u => { window.__girisVar = !!u; if (finished) render(); }))
    .catch(() => {});
}
if ('requestIdleCallback' in window) requestIdleCallback(oturumuIzle, { timeout: 2000 }); else setTimeout(oturumuIzle, 300);

// ?basla=N sınavı, ?konu=<kategori> konu denemesini doğrudan başlatır (soru, hap ve konu sayfalarından gelen bağlantılar).
const _prm = new URLSearchParams(location.search);
if (KONULAR[_prm.get('konu')]) sinaviBaslat(1, _prm.get('konu'));
else if (_prm.get('basla')) sinaviBaslat(_prm.get('basla'));""")

# ---------- Sınav kabuğu (overlay + onay modalı) ----------
sinav_govde = kes(kaynak, '<body>\n', '\n<script src="/assets/js/questions-1.js"></script>')
sinav_govde = degistir(sinav_govde, '<div class="sinav-overlay">', '<div class="sinav-overlay" id="sinavOverlay" role="dialog" aria-modal="true" aria-label="Deneme sınavı">')
sinav_govde = degistir(sinav_govde,
    """  <button class="exit-btn" onclick="location.href=(window.SINAV_DEVAM_EDIYOR && !confirm('Sınav devam ediyor. Çıkarsan cevapların kaybolur. Çıkmak istiyor musun?')) ? location.href : '/panel/'">‹ Çıkış</button>""",
    """  <button class="exit-btn" type="button" onclick="cikisIste()">‹ Çıkış</button>""")

# ---------- Site kabuğu ----------
site_header = kes(pillar, '<body>\n', '  <main>')
site_footer = kes(pillar, '  <footer class="site-footer">', '  </footer>', dahil=True)
ga = kes(pillar, "<!-- Google tag (gtag.js) — sayfa yüklendikten sonra yüklenir -->", "</body>", dahil=False)
ga = "<!-- Google tag (gtag.js) — sayfa yüklendikten sonra yüklenir -->" + ga

TITLE = "Ehliyet Deneme Sınavı Çöz: 50 Soru, 45 Dakika | ehliyet.digital"
DESC = ("Giriş gerektirmeyen ücretsiz ehliyet deneme sınavı. MEB e-sınav formatında 50 soru, 45 dakika, "
        "anında puan ve çözümlü cevaplar. Çıkmış sorulardan 4 farklı deneme.")
assert len(DESC) <= 165, len(DESC)

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
      <p>MEB e-sınavıyla birebir aynı formatta ücretsiz deneme: <b>50 soru, 45 dakika</b>, dört bölüm. Giriş yapmadan hemen başla; süre tutulur, sınav bitince puanın ve her sorunun doğru cevabı anında gösterilir. Sorular gerçek ehliyet sınavında çıkmış sorulardan derlendi.</p>
      <div class="hero-actions">
        <button class="btn btn-primary btn-lg" type="button" data-sinav="1">Deneme Sınavına Başla</button>
        <a class="btn btn-outline btn-lg" href="#sinavlar">Diğer denemeler</a>
      </div>
      <div class="ozet" aria-label="Sınav özeti">
        <div><b>50</b><span>soru</span></div>
        <div><b>45</b><span>dakika</span></div>
        <div><b>70</b><span>geçme puanı</span></div>
        <div><b>4</b><span>farklı deneme</span></div>
      </div>
    </div>

    <div class="icerik">
      <section class="blok" id="sinavlar">
        <h2>Deneme sınavını seç</h2>
        <p>Dört deneme de MEB MTSK e-sınavında çıkmış sorulardan oluşur. Hepsi aynı format: 50 soru, 45 dakika, her doğru 2 puan.</p>
        <div class="sinav-grid">
          <div class="sinav-kart"><span class="no">Deneme 1</span><h3>Sınav 1</h3><p>Başlangıç için önerilen deneme. Dört konudan dengeli soru dağılımı.</p><button class="btn btn-primary" type="button" data-sinav="1">Sınava Başla</button></div>
          <div class="sinav-kart"><span class="no">Deneme 2</span><h3>Sınav 2</h3><p>Görselli trafik işareti ve kavşak soruları ağırlıklı.</p><button class="btn btn-primary" type="button" data-sinav="2">Sınava Başla</button></div>
          <div class="sinav-kart"><span class="no">Deneme 3</span><h3>Sınav 3</h3><p>İlk yardım ve araç tekniği çeldiricileri yoğun.</p><button class="btn btn-primary" type="button" data-sinav="3">Sınava Başla</button></div>
          <div class="sinav-kart"><span class="no">Deneme 4</span><h3>Sınav 4</h3><p>Video ve görsel sorularıyla en güncel e-sınav formatı.</p><button class="btn btn-primary" type="button" data-sinav="4">Sınava Başla</button></div>
        </div>
      </section>

      <section class="blok" id="konu-denemeleri">
        <h2>Konu bazlı deneme</h2>
        <p>Tek bir konuda eksiğin varsa dört sınavın o konudaki sorularını tek denemede çöz. Süre soru sayısına göre ayarlanır, geçme koşulu yüzde 70. Konu denemeleri panele kaydedilmez.</p>
        <div class="baglantilar">
          <a class="btn btn-outline" href="/deneme-sinavi/?konu=ilk-yardim">İlk Yardım denemesi</a>
          <a class="btn btn-outline" href="/deneme-sinavi/?konu=trafik-ve-cevre">Trafik ve Çevre denemesi</a>
          <a class="btn btn-outline" href="/deneme-sinavi/?konu=arac-teknigi">Araç Tekniği denemesi</a>
          <a class="btn btn-outline" href="/deneme-sinavi/?konu=trafik-adabi">Trafik Adabı denemesi</a>
        </div>
      </section>

      <section class="blok">
        <h2>Deneme sınavı nasıl çalışır?</h2>
        <p>Arayüz, süre ve puanlama gerçek e-sınavla aynı. Sınav sırasında sorular arasında ileri geri gidebilir, soru haritasından istediğin soruya atlayabilirsin.</p>
        <ul class="madde">
          <li><b>Giriş gerekmez.</b> Sayfayı aç, sınava başla. Sonuçlarını kaydetmek istersen Google ile giriş yapabilirsin.</li>
          <li><b>50 soru, 45 dakika.</b> Süre dolunca sınav otomatik biter, işaretlediklerin puanlanır.</li>
          <li><b>Puanlama gerçek sınav gibi.</b> Her doğru 2 puan, yanlış doğruyu götürmez. Geçmek için 70 puan, yani en az 35 doğru.</li>
          <li><b>Anında sonuç.</b> Puan, doğru, yanlış ve boş sayısı; konu bazlı performans grafiği.</li>
          <li><b>Çözümlü inceleme.</b> Sınav bitince her sorunun doğru cevabı ve senin işaretin yan yana gösterilir.</li>
          <li><b>Ücretsiz ve reklamsız.</b> Ücret, üyelik zorunluluğu veya reklam yok.</li>
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
        <details><summary>Deneme sınavı ücretsiz mi?</summary><p>Evet. Dört deneme de ücretsiz, reklam yok. Herhangi bir üyelik veya ödeme gerekmez.</p></details>
        <details><summary>Giriş yapmam gerekiyor mu?</summary><p>Hayır. Sınava doğrudan başlayabilirsin. Google ile giriş yaparsan denemelerin hesabına kaydedilir ve panelde puan gelişimini, konu bazlı eksiklerini takip edebilirsin.</p></details>
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
        <p>50 soru, 45 dakika. Sınav bitince puanını ve her sorunun cevabını hemen gör.</p>
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
